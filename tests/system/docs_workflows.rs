//! Runs the "Explicit workflows" in docs/tui.md against a live saiserver,
//! through the real `sai-tui` CLI, exactly as a reader would type them.
//!
//! Each ```text block line is one command. `NAME_OID` placeholders are
//! filled from earlier results: a trailing `# -> NAME_OID[, OTHER_OID]`
//! annotation binds the key returned by that line's create. PORT_OID and
//! TRUNK_PORT_OID are the first two discovered switch ports. Every command
//! must succeed with verified readback. Afterwards everything created is
//! removed again, newest first, and the removal must also verify.
//!
//! `--known-unsupported "SECTION=MESSAGE"` pins a documented SDK limitation:
//! that section's first command must fail with MESSAGE in its output, and the
//! rest of the section is skipped. If it starts passing, the test fails too.
//!
//! Usage: docs_workflows [--known-unsupported SECTION=MESSAGE]... SAI_TUI DOC
use serde_json::Value;
use std::collections::BTreeMap;
use std::process::{exit, Command};
use std::thread::sleep;
use std::time::{Duration, Instant};

struct Step {
    section: String,
    line: usize,
    command: String,
    binds: Vec<String>,
}

/// The ```text blocks of the "## Explicit workflows" section, in order.
fn workflow_steps(doc: &str) -> Vec<Step> {
    let mut steps = Vec::new();
    let (mut in_section, mut in_block) = (false, false);
    let mut section = String::new();
    for (index, raw) in doc.lines().enumerate() {
        if raw.starts_with("## ") {
            in_section = raw == "## Explicit workflows";
            continue;
        }
        if !in_section {
            continue;
        }
        if let Some(heading) = raw.strip_prefix("### ") {
            section = heading.to_string();
            continue;
        }
        if raw.starts_with("```") {
            in_block = !in_block && raw == "```text";
            continue;
        }
        if !in_block || raw.trim().is_empty() {
            continue;
        }
        let (command, binds) = match raw.split_once('#') {
            Some((command, note)) => {
                let note = note.trim();
                let names = note.strip_prefix("->").unwrap_or_else(|| {
                    fail(&format!(
                        "docs line {}: comment is not `# -> NAME_OID`: {raw}",
                        index + 1
                    ))
                });
                (
                    command,
                    names.split(',').map(|n| n.trim().to_string()).collect(),
                )
            }
            None => (raw, Vec::new()),
        };
        steps.push(Step {
            section: section.clone(),
            line: index + 1,
            command: command.trim().to_string(),
            binds,
        });
    }
    if steps.is_empty() {
        fail("no workflow commands found in docs");
    }
    steps
}

fn fail(message: &str) -> ! {
    eprintln!("FAIL: {message}");
    exit(1)
}

fn run(tui: &str, args: &[&str]) -> (bool, Value) {
    let output = Command::new(tui)
        .args(args)
        .output()
        .unwrap_or_else(|e| fail(&format!("cannot run {tui}: {e}")));
    let text = String::from_utf8_lossy(&output.stdout);
    let json: Value = serde_json::from_str(&text).unwrap_or_else(|_| {
        fail(&format!(
            "{args:?}: not JSON (exit {:?}):\n{text}\n{}",
            output.status.code(),
            String::from_utf8_lossy(&output.stderr)
        ))
    });
    (
        output.status.success() && json["ok"] == Value::Bool(true),
        json,
    )
}

fn try_command(tui: &str, line: &str) -> (bool, Value) {
    let mutation = ["create ", "set ", "remove "]
        .iter()
        .any(|p| line.starts_with(p));
    let mut args = vec!["--command", line];
    if mutation {
        args.push("--yes");
    }
    run(tui, &args)
}

fn command(tui: &str, line: &str) -> Value {
    let (ok, json) = try_command(tui, line);
    if !ok {
        fail(&format!(
            "`{line}` did not verify:\n{}",
            serde_json::to_string_pretty(&json).unwrap()
        ));
    }
    json
}

fn snapshot(tui: &str) -> Value {
    let deadline = Instant::now() + Duration::from_secs(60);
    loop {
        let (ok, json) = run(tui, &["--snapshot"]);
        if ok {
            return json;
        }
        if Instant::now() > deadline {
            fail(&format!("no snapshot from server:\n{json}"));
        }
        sleep(Duration::from_millis(200));
    }
}

fn substitute(line: &str, labels: &BTreeMap<String, String>, doc_line: usize) -> String {
    let mut out = String::new();
    let mut word = String::new();
    let flush = |word: &mut String, out: &mut String| {
        if word.ends_with("_OID")
            && word
                .chars()
                .all(|c| c.is_ascii_uppercase() || c.is_ascii_digit() || c == '_')
        {
            match labels.get(word.as_str()) {
                Some(key) => out.push_str(key),
                None => fail(&format!(
                    "docs line {doc_line}: {word} is not bound by an earlier `# -> {word}`"
                )),
            }
        } else {
            out.push_str(word);
        }
        word.clear();
    };
    for c in line.chars() {
        if c.is_ascii_alphanumeric() || c == '_' {
            word.push(c);
        } else {
            flush(&mut word, &mut out);
            out.push(c);
        }
    }
    flush(&mut word, &mut out);
    out
}

fn main() {
    let mut args: Vec<String> = std::env::args().skip(1).collect();
    let mut known_unsupported = BTreeMap::new();
    while args.first().map(String::as_str) == Some("--known-unsupported") && args.len() > 1 {
        let spec = args.remove(1);
        args.remove(0);
        let (section, message) = spec
            .split_once('=')
            .unwrap_or_else(|| fail(&format!("bad --known-unsupported {spec}")));
        known_unsupported.insert(section.to_string(), message.to_string());
    }
    if args.len() != 2 {
        fail("usage: docs_workflows [--known-unsupported SECTION=MESSAGE]... SAI_TUI DOC");
    }
    let tui = args[0].as_str();
    let doc =
        std::fs::read_to_string(&args[1]).unwrap_or_else(|e| fail(&format!("{}: {e}", args[1])));
    let steps = workflow_steps(&doc);
    for section in known_unsupported.keys() {
        if !steps.iter().any(|s| &s.section == section) {
            fail(&format!(
                "--known-unsupported names no workflow section: {section}"
            ));
        }
    }

    let inventory = snapshot(tui);
    let ports: Vec<&Value> = inventory["inventory"]["objects"]
        .as_array()
        .unwrap_or_else(|| fail("snapshot has no objects"))
        .iter()
        .filter(|o| o["kind"] == "port")
        .collect();
    if ports.len() < 2 {
        fail(&format!(
            "need two switch ports, snapshot has {}",
            ports.len()
        ));
    }
    let port = ports[0]["key"].as_str().unwrap().to_string();
    let pvid = ports[0]["attributes"]["pvid"]
        .as_str()
        .unwrap_or("1")
        .to_string();
    let mut labels = BTreeMap::from([
        ("PORT_OID".to_string(), port.clone()),
        (
            "TRUNK_PORT_OID".to_string(),
            ports[1]["key"].as_str().unwrap().to_string(),
        ),
    ]);

    let mut created: Vec<(String, String)> = Vec::new();
    let mut skipped_section = None;
    let mut skipped = 0;
    for step in &steps {
        if skipped_section == Some(&step.section) {
            skipped += 1;
            continue;
        }
        let line = substitute(&step.command, &labels, step.line);
        println!("docs/tui.md:{}: {line}", step.line);
        if let Some(message) = known_unsupported.get(&step.section) {
            let (ok, json) = try_command(tui, &line);
            let text = json.to_string();
            if ok || !text.contains(message.as_str()) {
                fail(&format!("`{line}` was expected to fail with {message:?} (known SDK limitation), got:\n{json}"));
            }
            println!(
                "  known unsupported here ({message}); skipping the rest of \"{}\"",
                step.section
            );
            skipped_section = Some(&step.section);
            continue;
        }
        let json = command(tui, &line);
        if let Some(kind) = line
            .strip_prefix("create ")
            .and_then(|rest| rest.split_whitespace().next())
        {
            let key = json["result"]["mutation"]["value"]["key"]
                .as_str()
                .unwrap_or_else(|| fail(&format!("`{line}` returned no key:\n{json}")))
                .to_string();
            created.push((kind.to_string(), key.clone()));
            for name in &step.binds {
                labels.insert(name.clone(), key.clone());
            }
        } else if !step.binds.is_empty() {
            fail(&format!(
                "docs line {}: only create can bind a label",
                step.line
            ));
        }
    }

    println!(
        "cleanup: restoring {port} pvid={pvid}, removing {} objects",
        created.len()
    );
    command(tui, &format!("set port {port} pvid={pvid}"));
    for (kind, key) in created.iter().rev() {
        command(tui, &format!("remove {kind} {key}"));
    }
    snapshot(tui);
    println!("PASS: {} documented workflow commands and their cleanup ({skipped} skipped as known unsupported)", steps.len() - skipped);
}
