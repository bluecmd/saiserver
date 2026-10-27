use crate::{
    apply::{self, ApplyReport, ApplyStatus},
    client::{self, Client, Failure, Outcome, Service},
    command::{self, Approval, Command},
    config::{ApplyApproval, Staging},
    preset_plan,
    presets::{self, BoundPreset},
    rates::{RateSample, Rates, COUNTERS},
    sai_tui::{Inventory, Object},
};
use crossterm::{
    event::{self, Event, KeyCode, KeyEventKind, KeyModifiers},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use ratatui::{
    backend::CrosstermBackend,
    layout::{Constraint, Direction, Layout},
    style::{Color, Style},
    symbols::Marker,
    text::{Line, Span},
    widgets::{
        Axis, Block, Borders, Chart, Dataset, GraphType, List, ListItem, ListState, Paragraph,
        Tabs, Wrap,
    },
    Terminal,
};
use std::{
    collections::BTreeMap,
    io::{self, stdout},
    sync::{
        atomic::{AtomicBool, Ordering},
        mpsc::{self, Receiver, SyncSender},
        Arc,
    },
    thread,
    time::{Duration, Instant},
};

const PAGES: &[&str] = &["Ports", "VLANs", "L2 FDB", "L3", "ACL", "Counters", "Help"];
fn on_page(page: usize, kind: &str) -> bool {
    match page {
        0 | 5 => kind == "port",
        1 => matches!(kind, "vlan" | "vlan_member" | "bridge_port"),
        2 => kind == "fdb",
        3 => matches!(
            kind,
            "virtual_router"
                | "router_interface"
                | "interface_address"
                | "neighbor"
                | "route"
                | "next_hop"
        ),
        4 => kind.starts_with("acl_"),
        _ => false,
    }
}
#[derive(Debug)]
enum Job {
    Snapshot,
    Get(String, String),
    Run(Command, Option<Approval>),
    Counters(String),
    Apply(Box<Staging>, ApplyApproval, BoundPreset),
}
enum Reply {
    Snapshot(Result<Inventory, Failure>),
    Get(Result<Object, Failure>),
    Run(Outcome),
    Counters(String, Instant, Result<BTreeMap<String, u64>, Failure>),
    Applied(Box<Staging>, ApplyReport),
}
fn apply_job(
    service: &mut impl Service,
    mut staging: Box<Staging>,
    approval: ApplyApproval,
    bound: BoundPreset,
    cancelled: &AtomicBool,
) -> Reply {
    let fresh = service.snapshot();
    let check = fresh
        .as_ref()
        .map_err(|e| e.to_string())
        .and_then(|inventory| {
            let plan = preset_plan::build(&bound, inventory)?;
            if staging.plan() != Some(&plan) {
                return Err("configuration changed since review; reload and review again".into());
            }
            Ok(())
        });
    let report = match check {
        Ok(()) => apply::apply(&mut staging, Some(approval), service, cancelled),
        Err(error) => ApplyReport {
            status: ApplyStatus::Rejected(error),
            steps: vec![],
            bindings: BTreeMap::new(),
            inventory: fresh.ok(),
            partial_effects: false,
        },
    };
    Reply::Applied(staging, report)
}
fn apply_summary(report: &ApplyReport) -> String {
    format!("Preset apply {:?}: {} verified steps; partial effects={}. No retry/rollback. Inspect audit.", report.status, report.completed_steps(), report.partial_effects)
}
fn apply_audit(report: &ApplyReport) -> String {
    serde_json::to_string_pretty(&serde_json::json!({
        "status": format!("{:?}", report.status), "partial_effects": report.partial_effects,
        "steps": report.steps.iter().map(|s| serde_json::json!({"index":s.index,"command":format!("{:?}",s.command),"mutation_sent":s.mutation_sent,"verified":s.verified,"outcome":s.outcome.value})).collect::<Vec<_>>()
    })).unwrap_or_default()
}
fn worker(mut client: Client, cancelled: Arc<AtomicBool>) -> (SyncSender<Job>, Receiver<Reply>) {
    let (tx, rx) = mpsc::sync_channel(1);
    let (done, out) = mpsc::sync_channel(1);
    thread::spawn(move || {
        while let Ok(job) = rx.recv() {
            let reply = match job {
                Job::Snapshot => Reply::Snapshot(client.snapshot()),
                Job::Get(k, v) => Reply::Get(client.get(&k, &v)),
                Job::Run(cmd, approval) => Reply::Run(client::execute(&mut client, &cmd, approval)),
                Job::Apply(staging, approval, bound) => {
                    apply_job(&mut client, staging, approval, bound, &cancelled)
                }
                Job::Counters(key) => {
                    let result = client.counters(&key);
                    Reply::Counters(key, Instant::now(), result)
                }
            };
            if done.send(reply).is_err() {
                break;
            }
        }
    });
    (tx, out)
}
struct ApplyCancelGuard(Arc<AtomicBool>);
impl Drop for ApplyCancelGuard {
    fn drop(&mut self) {
        self.0.store(true, Ordering::Release);
    }
}
#[cfg(unix)]
struct SignalGuard(Vec<signal_hook::SigId>);
#[cfg(unix)]
impl Drop for SignalGuard {
    fn drop(&mut self) {
        for id in self.0.drain(..) {
            signal_hook::low_level::unregister(id);
        }
    }
}

/// Drop also handles initialization/draw/event errors. Panic hook restores before reporting.
struct TerminalGuard;
impl Drop for TerminalGuard {
    fn drop(&mut self) {
        let _ = disable_raw_mode();
        let _ = execute!(stdout(), LeaveAlternateScreen, crossterm::cursor::Show);
    }
}
#[derive(Debug)]
enum ReviewAction {
    Mutation(Command),
    LoadPreset(BoundPreset),
    ApplyPreset,
}
struct Review {
    text: String,
    action: ReviewAction,
}
struct App {
    inventory: Inventory,
    page: usize,
    selected: usize,
    busy: bool,
    status: String,
    failed: bool,
    input: Option<String>,
    review: Option<Review>,
    staged: Option<BoundPreset>,
    staging: Staging,
    details: String,
    scroll: u16,
    counters: BTreeMap<String, u64>,
    rates: Rates,
    last_rate: RateSample,
    counter_key: Option<String>,
    next_poll: Instant,
    tx: SyncSender<Job>,
    /// A preset apply is outstanding; quitting must wait for its audit.
    applying: bool,
}
impl App {
    fn objects(&self) -> Vec<&Object> {
        self.inventory
            .objects
            .as_deref()
            .unwrap_or_default()
            .iter()
            .filter(|o| on_page(self.page, o.kind.as_deref().unwrap_or_default()))
            .collect()
    }
    fn selected(&self) -> Option<&Object> {
        let objects = self.objects();
        objects
            .get(self.selected.min(objects.len().saturating_sub(1)))
            .copied()
    }
    fn target(&self) -> Option<(String, String)> {
        self.selected()
            .and_then(|o| Some((o.kind.clone()?, o.key.clone()?)))
    }
    fn dispatch(&mut self, job: Job) -> bool {
        if self.busy {
            self.status = "Busy: bounded worker has one outstanding request; wait or quit".into();
            return false;
        }
        let applying = matches!(job, Job::Apply(..));
        match self.tx.try_send(job) {
            Ok(()) => {
                self.busy = true;
                self.applying = applying;
                self.status =
                    "RPC in progress (bounded timeout); mutations are never retried".into();
                true
            }
            Err(e) => {
                self.failed = true;
                self.status = format!("worker unavailable: {e}; quit and reconnect");
                let (mpsc::TrySendError::Full(job) | mpsc::TrySendError::Disconnected(job)) = e;
                if let Job::Apply(staging, _, _) = job {
                    self.staging = *staging;
                }
                false
            }
        }
    }
    fn reset_selection(&mut self) {
        self.scroll = 0;
        self.details.clear();
        self.counter_key = None;
        self.counters.clear();
        self.rates.clear();
        self.last_rate = self.rates.disconnected("resource selection changed");
        self.next_poll = Instant::now();
    }
    fn show_presets(&mut self) {
        self.details = format!(
            "SWITCH CONFIGURATION PRESETS\n{}\n\n:presets lists presets; :preset load ID reviews a staged replacement.\n:preset show displays the staged configuration. Loading NEVER applies hardware changes.\nStock port lanes and speeds must match discovery. No automatic breakout changes.\nERSPAN uses a static example destination MAC; configure the collector accordingly.\nPress a (or :preset apply) to REVIEW application as a separate explicit action.",
            presets::catalog().iter().map(|(id, title)| format!("{id}\n  {title}")).collect::<Vec<_>>().join("\n")
        );
        self.scroll = 0;
    }
    fn prepare_apply(&mut self) -> Result<(), String> {
        if self.busy {
            return Err("wait for active RPC before reviewing apply".into());
        }
        let bound = self
            .staged
            .as_ref()
            .ok_or("no staged configuration; press p to load")?;
        let plan = preset_plan::build(bound, &self.inventory)?;
        if self.staging.plan() != Some(&plan) {
            return Err("configuration changed; reload and review again".into());
        }
        self.details = format!("REVIEW HARDWARE APPLICATION — {} operations\n{}\n\nDISRUPTIVE: all 33 physical ports are disabled first. ACLs are verified before forwarding setup; mirrors are verified before separate port enables. Failure/cancellation may leave ports DOWN. Default VLAN memberships listed below will be removed. This is NOT a transaction: no rollback or automatic retry.\nStops at first failure or uncertain readback; quitting stops remaining steps, not an already-sent mutation.\nIPv6 is static/no-DAD; verify address uniqueness. No dynamic neighbor learning or ICMP echo service.\nInventory is limited; undiscovered dependencies may cause partial failure.\n\n{:#?}\n\ny APPLIES ONCE; n/Esc cancels without changing hardware or staged state.", plan.operations.len(), plan.title, plan.operations);
        self.review = Some(Review {
            text: "preset apply".into(),
            action: ReviewAction::ApplyPreset,
        });
        self.scroll = 0;
        self.status =
            "REVIEW APPLY: y sends the displayed hardware operations ONCE; n/Esc cancels.".into();
        Ok(())
    }
    fn confirm_review(&mut self) -> Result<(), String> {
        if self.busy {
            return Err("wait for active RPC before confirmation".into());
        }
        let Some(review) = self.review.take() else {
            return Ok(());
        };
        match review.action {
            ReviewAction::Mutation(cmd) => {
                let approval = command::approve(&cmd, true)?;
                self.dispatch(Job::Run(cmd, approval));
            }
            ReviewAction::ApplyPreset => {
                let bound = self.staged.clone().ok_or("no staged preset")?;
                let plan = preset_plan::build(&bound, &self.inventory)?;
                if self.staging.plan() != Some(&plan) {
                    return Err("configuration changed; reload and review again".into());
                }
                let approval = self.staging.approve(true)?;
                let staging = Box::new(std::mem::take(&mut self.staging));
                self.dispatch(Job::Apply(staging, approval, bound));
            }
            ReviewAction::LoadPreset(bound) => {
                // Revalidate current discovery before replacing the old local state.
                let bound = presets::bind(bound.preset, &self.inventory)?;
                let plan = preset_plan::build(&bound, &self.inventory)?;
                self.staging.load(plan, &self.inventory, true)?;
                self.details =
                    serde_json::to_string_pretty(&bound.preset).map_err(|e| e.to_string())?;
                self.staged = Some(bound);
                self.failed = false;
                self.scroll = 0;
                self.status = "Preset staged locally. NO hardware changes sent. Applying requires separate confirmation.".into();
            }
        }
        Ok(())
    }
    fn cancel_review(&mut self) {
        self.review = None;
        self.status = "Cancelled: staged configuration preserved; no mutation sent".into();
    }
    fn prepare(&mut self, text: String) {
        let words: Vec<_> = text.split_whitespace().collect();
        if words.as_slice() == ["presets"] {
            self.show_presets();
            return;
        }
        if words.first() == Some(&"preset") {
            if words.as_slice() == ["preset", "apply"] {
                if let Err(error) = self.prepare_apply() {
                    self.failed = true;
                    self.status = error;
                }
                return;
            }
            if words.as_slice() == ["preset", "show"] {
                self.details = self
                    .staged
                    .as_ref()
                    .map(|s| serde_json::to_string_pretty(&s.preset).unwrap_or_default())
                    .unwrap_or_else(|| {
                        "No staged configuration. Press p to choose a preset.".into()
                    });
                self.scroll = 0;
                return;
            }
            if words.len() != 3 || words[1] != "load" {
                self.failed = true;
                self.status =
                    "Expected preset load ID or preset show; presets lists available choices"
                        .into();
                return;
            }
            if self.busy {
                self.status = "Wait for the active RPC before loading a preset".into();
                return;
            }
            match presets::get(words[2])
                .and_then(|p| presets::bind(p, &self.inventory))
                .and_then(|bound| {
                    preset_plan::build(&bound, &self.inventory)?;
                    Ok(bound)
                }) {
                Ok(bound) => {
                    self.details = format!("REPLACE STAGED CONFIGURATION ONLY — NO HARDWARE APPLICATION\nPrevious staged preset: {}\n\n{}\n\ny replaces local staged state; n/Esc preserves it. Applying is a SEPARATE confirmed action.\nAddresses require the operational server ARP/NDP service; RIFs alone are not addressed interfaces.\nStatic ERSPAN destination MAC is an example, not discovered from the collector.", self.staged.as_ref().map(|s| s.preset.title.as_str()).unwrap_or("none"), serde_json::to_string_pretty(&bound.preset).unwrap_or_default());
                    self.review = Some(Review {
                        text,
                        action: ReviewAction::LoadPreset(bound),
                    });
                    self.scroll = 0;
                    self.failed = false;
                    self.status = "REVIEW LOAD: y replaces staged state ONLY; n/Esc cancels. No hardware changes.".into();
                }
                Err(error) => {
                    self.failed = true;
                    self.status = format!(
                        "Preset not loaded; previous staged configuration preserved: {error}"
                    );
                }
            }
            return;
        }
        match command::parse(&text) {
            Err(e) => {
                self.failed = true;
                self.status = e;
                self.input = Some(text);
            }
            Ok(Command::Help { kind }) => {
                self.details = command::help(kind.as_deref());
                self.scroll = 0;
            }
            Ok(cmd) if cmd.mutates() => {
                if self.busy {
                    self.status = "Wait for the active read before reviewing a mutation".into();
                    self.input = Some(text);
                    return;
                }
                match client::validate_references(&cmd, &self.inventory) {
                    Ok(notes) => {
                        self.details = format!("REVIEW REQUEST — NO MUTATION SENT\n{cmd:#?}\n\nReference warnings:\n{}\n\ny confirms one mutation; n/Esc cancels. PgUp/PgDn scrolls this complete request. Separate getter + snapshot follow, even on ambiguous failure. No rollback or implicit retry.", notes.join("\n"));
                        self.scroll = 0;
                        self.review = Some(Review {
                            text,
                            action: ReviewAction::Mutation(cmd),
                        });
                        self.status="REVIEW: y sends this mutation ONCE; n/Esc cancels. No changes sent yet.".into();
                    }
                    Err(e) => {
                        self.failed = true;
                        self.status = e;
                        self.input = Some(text);
                    }
                }
            }
            Ok(cmd) => {
                self.dispatch(Job::Run(cmd, None));
            }
        }
    }
    fn reply(&mut self, reply: Reply) {
        self.busy = false;
        self.applying = false;
        match reply {
            Reply::Applied(staging, report) => {
                self.staging = *staging;
                self.failed = report.status != ApplyStatus::Completed;
                self.status = apply_summary(&report);
                self.details = apply_audit(&report);
                if report.partial_effects {
                    // Re-applying the same plan would duplicate whatever was
                    // already created; require an explicit reload instead.
                    self.staged = None;
                    self.status
                        .push_str(" Staged preset cleared; reload before any new apply.");
                }
                if let Some(inventory) = report.inventory {
                    self.inventory = inventory;
                }
                self.scroll = 0;
                self.last_rate = self.rates.disconnected("preset apply completed or stopped");
            }
            Reply::Snapshot(result) => {
                match result {
                    Ok(i) => {
                        self.details = serde_json::to_string_pretty(&client::inventory_json(&i))
                            .unwrap_or_default();
                        self.scroll = 0;
                        self.inventory = i;
                        self.failed = false;
                        self.status="Discovery refreshed from server; read warnings below. r refresh/reconnect".into();
                        self.selected = self.selected.min(self.objects().len().saturating_sub(1));
                    }
                    Err(e) => {
                        self.failed = true;
                        self.status=format!("Snapshot failed: {e}. Press r to reconnect, q to quit. Prior inventory may be stale.");
                        self.last_rate = self.rates.disconnected(&e.to_string());
                    }
                }
            }
            Reply::Get(r) => match r {
                Ok(o) => {
                    self.failed = false;
                    self.details =
                        serde_json::to_string_pretty(&client::object_json(&o)).unwrap_or_default();
                    self.scroll = 0;
                    self.status = "Actual getter readback (not a cache)".into();
                }
                Err(e) => {
                    self.failed = true;
                    self.details = format!("Getter failed: {e}");
                    self.status = format!("{e}; r reconnect");
                    self.last_rate = self.rates.disconnected(&e.to_string());
                }
            },
            Reply::Run(out) => {
                self.failed = !out.ok;
                self.details = serde_json::to_string_pretty(&out.value).unwrap_or_default();
                self.scroll = 0;
                if let Some(i) = out.inventory {
                    self.inventory = i;
                }
                self.status=if out.ok {"Command completed; inspect actual readback and warnings"} else {"COMMAND FAILED / POSSIBLE PARTIAL EFFECT. Inspect details; do NOT blindly retry. r refresh"}.into();
                // A control operation may reconnect or change a port. Do not bridge counter baselines.
                self.last_rate = self.rates.disconnected("management command completed");
            }
            Reply::Counters(key, when, result) => {
                if self.counter_key.as_deref() != Some(&key) {
                    return;
                }
                match result {
                    Ok(c) => {
                        self.last_rate = self.rates.sample(when, &c);
                        self.counters = c;
                        self.failed = false;
                        self.status =
                            format!("Live counters {key}: {}", self.last_rate.notes.join("; "));
                    }
                    Err(e) => {
                        self.failed = true;
                        self.counters.clear();
                        self.last_rate = self.rates.disconnected(&e.to_string());
                        self.status =
                            format!("Counters failed: {e}. r reconnect; next poll is read-only.");
                    }
                }
            }
        }
    }
}

pub fn run(client: Client, interval: Duration) -> io::Result<()> {
    let endpoint = client.endpoint;
    let old = std::panic::take_hook();
    std::panic::set_hook(Box::new(move |info| {
        let _ = disable_raw_mode();
        let _ = execute!(stdout(), LeaveAlternateScreen, crossterm::cursor::Show);
        old(info);
    }));
    let guard = TerminalGuard;
    #[cfg(unix)]
    let stopping = std::sync::Arc::new(std::sync::atomic::AtomicBool::new(false));
    #[cfg(unix)]
    let _signals = {
        let mut guard = SignalGuard(Vec::new());
        for signal in [
            signal_hook::consts::SIGTERM,
            signal_hook::consts::SIGINT,
            signal_hook::consts::SIGHUP,
        ] {
            guard
                .0
                .push(signal_hook::flag::register(signal, stopping.clone())?);
        }
        guard
    };
    enable_raw_mode()?;
    execute!(stdout(), EnterAlternateScreen)?;
    let mut terminal = Terminal::new(CrosstermBackend::new(stdout()))?;
    terminal.clear()?;
    let cancelled = Arc::new(AtomicBool::new(false));
    let _apply_cancel = ApplyCancelGuard(cancelled.clone());
    let rpc_timeout = client.timeout;
    let (tx, rx) = worker(client, cancelled.clone());
    let mut app = App {
        inventory: Inventory::default(),
        page: 0,
        selected: 0,
        busy: false,
        status: String::new(),
        failed: false,
        input: None,
        review: None,
        staged: None,
        staging: Staging::default(),
        details: String::new(),
        scroll: 0,
        counters: BTreeMap::new(),
        rates: Rates::new(interval),
        last_rate: RateSample::default(),
        counter_key: None,
        next_poll: Instant::now(),
        tx,
        applying: false,
    };
    app.dispatch(Job::Snapshot);
    let result = (|| -> io::Result<()> {
        loop {
            #[cfg(unix)]
            if stopping.load(std::sync::atomic::Ordering::Relaxed) {
                return Err(io::Error::new(io::ErrorKind::Interrupted, "termination signal received; an in-flight mutation may have partial effects; inspect server state"));
            }
            while let Ok(reply) = rx.try_recv() {
                app.reply(reply);
            }
            if app.page == 5
                && !app.busy
                && app.review.is_none()
                && app.input.is_none()
                && app.details.is_empty()
                && Instant::now() >= app.next_poll
            {
                if let Some((_, key)) = app.target() {
                    if app.counter_key.as_deref() != Some(&key) {
                        app.rates.clear();
                        app.last_rate = app.rates.disconnected("port changed");
                        app.counters.clear();
                        app.counter_key = Some(key.clone());
                    }
                    app.dispatch(Job::Counters(key));
                    app.next_poll = Instant::now() + interval;
                }
            }
            terminal.draw(|frame| draw(frame, &mut app, &endpoint.to_string()))?;
            if !event::poll(Duration::from_millis(50))? {
                continue;
            }
            let Event::Key(key) = event::read()? else {
                continue;
            };
            if key.kind != KeyEventKind::Press {
                continue;
            }
            if key.code == KeyCode::Char('c') && key.modifiers.contains(KeyModifiers::CONTROL) {
                break Ok(());
            }
            if app.review.is_some() {
                match key.code {
                    KeyCode::Char('y') => {
                        if let Err(error) = app.confirm_review() {
                            app.failed = true;
                            app.status = format!("Confirmation rejected: {error}");
                        }
                    }
                    KeyCode::Char('n') | KeyCode::Esc => {
                        app.cancel_review();
                    }
                    KeyCode::PageDown => app.scroll = app.scroll.saturating_add(8),
                    KeyCode::PageUp => app.scroll = app.scroll.saturating_sub(8),
                    _ => {}
                }
                continue;
            }
            if let Some(input) = &mut app.input {
                match key.code {
                    KeyCode::Enter => {
                        let text = app.input.take().expect("input exists");
                        app.prepare(text);
                    }
                    KeyCode::Esc => {
                        app.input = None;
                    }
                    KeyCode::Backspace => {
                        input.pop();
                    }
                    KeyCode::PageDown => app.scroll = app.scroll.saturating_add(8),
                    KeyCode::PageUp => app.scroll = app.scroll.saturating_sub(8),
                    KeyCode::Char(c) if input.len() + c.len_utf8() <= 8192 => input.push(c),
                    _ => {}
                }
                continue;
            }
            match key.code {
                KeyCode::Char('q') => break Ok(()),
                KeyCode::Tab | KeyCode::Right => {
                    app.page = (app.page + 1) % PAGES.len();
                    app.selected = 0;
                    app.reset_selection();
                }
                KeyCode::BackTab | KeyCode::Left => {
                    app.page = (app.page + PAGES.len() - 1) % PAGES.len();
                    app.selected = 0;
                    app.reset_selection();
                }
                KeyCode::Char(c @ '1'..='7') => {
                    app.page = (c as u8 - b'1') as usize;
                    app.selected = 0;
                    app.reset_selection();
                }
                KeyCode::Down | KeyCode::Char('j') => {
                    app.selected = (app.selected + 1).min(app.objects().len().saturating_sub(1));
                    app.reset_selection();
                }
                KeyCode::Up | KeyCode::Char('k') => {
                    app.selected = app.selected.saturating_sub(1);
                    app.reset_selection();
                }
                KeyCode::PageDown => app.scroll = app.scroll.saturating_add(8),
                KeyCode::PageUp => app.scroll = app.scroll.saturating_sub(8),
                KeyCode::Char('r') => {
                    app.dispatch(Job::Snapshot);
                }
                KeyCode::Enter | KeyCode::Char('g') => {
                    if let Some((k, v)) = app.target() {
                        app.dispatch(Job::Get(k, v));
                    }
                }
                KeyCode::Char('a') => {
                    if let Err(error) = app.prepare_apply() {
                        app.failed = true;
                        app.status = error;
                    }
                }
                KeyCode::Char('p') => {
                    app.show_presets();
                    app.input = Some(format!("preset load {}", presets::SEASTONE2_ID));
                }
                KeyCode::Char(':') => {
                    app.input = Some(String::new());
                    app.scroll = 0;
                }
                KeyCode::Char('l') => {
                    app.reset_selection();
                }
                KeyCode::Char('w') => {
                    app.details = format!(
                        "FULL INVENTORY WARNINGS\n{}",
                        app.inventory
                            .warnings
                            .as_deref()
                            .unwrap_or_default()
                            .join("\n\n")
                    );
                    app.scroll = 0;
                }
                KeyCode::Char('e') => {
                    if let Some((k, v)) = app.target() {
                        app.input = Some(format!("set {k} {v} "));
                        app.scroll = 0;
                    }
                }
                KeyCode::Char('d') => {
                    if let Some((k, v)) = app.target() {
                        app.prepare(format!("remove {k} {v}"));
                    }
                }
                KeyCode::Char('c') => {
                    let k = app.target().map(|t| t.0).unwrap_or_else(|| {
                        match app.page {
                            1 => "vlan",
                            3 => "virtual_router",
                            4 => "acl_table",
                            _ => "vlan",
                        }
                        .into()
                    });
                    app.input = Some(format!("create {k} "));
                    app.scroll = 0;
                }
                KeyCode::Char('?') => {
                    let k = app.target().map(|t| t.0);
                    app.details = command::help(k.as_deref());
                    app.scroll = 0;
                }
                _ => {}
            }
        }
    })();
    // An outstanding apply is cancelled between steps, but its audit is the
    // only record of what reached hardware: wait (bounded) for it and report
    // it after the terminal is restored.
    let report = app.applying.then(|| {
        cancelled.store(true, Ordering::Release);
        app.status =
            "Cancelling preset apply: waiting for the in-flight step and its readback".into();
        let _ = terminal.draw(|frame| draw(frame, &mut app, &endpoint.to_string()));
        let deadline = Instant::now() + rpc_timeout * 8;
        loop {
            match rx.recv_timeout(deadline.saturating_duration_since(Instant::now())) {
                Ok(Reply::Applied(_, report)) => break Some(report),
                Ok(_) => continue,
                Err(_) => break None,
            }
        }
    });
    // Otherwise no join: a bounded in-flight read may finish later; dropping
    // the channels stops the worker without delaying terminal restoration.
    let _ = terminal.show_cursor();
    drop(guard);
    match report {
        Some(Some(report)) => eprintln!("sai-tui: {}\n{}", apply_summary(&report), apply_audit(&report)),
        Some(None) => eprintln!("sai-tui: preset apply audit unavailable (worker did not finish in time); an in-flight mutation may have partial effects; inspect server state"),
        None => {}
    }
    result
}
fn pretty_bps(rate: Option<f64>) -> String {
    rate.map(|r| format!("{r:.1} bit/s"))
        .unwrap_or_else(|| "unavailable / baseline".into())
}
fn draw(frame: &mut ratatui::Frame<'_>, app: &mut App, endpoint: &str) {
    let rows = Layout::default()
        .direction(Direction::Vertical)
        .constraints([
            Constraint::Length(3),
            Constraint::Min(4),
            Constraint::Length(5),
            Constraint::Length(if app.review.is_some() { 6 } else { 3 }),
        ])
        .split(frame.area());
    frame.render_widget(
        Tabs::new(
            PAGES
                .iter()
                .enumerate()
                .map(|(i, s)| Line::from(format!("{} {s}", i + 1))),
        )
        .select(app.page)
        .highlight_style(Style::default().fg(Color::Cyan))
        .block(Block::default().borders(Borders::ALL).title(format!(
            "SAI {endpoint} | {} | q quit",
            if app.busy { "BUSY" } else { "ready" }
        ))),
        rows[0],
    );
    let panes = Layout::default()
        .direction(Direction::Horizontal)
        .constraints([Constraint::Percentage(32), Constraint::Percentage(68)])
        .split(rows[1]);
    let objects = app.objects();
    let items: Vec<ListItem<'_>> = objects
        .iter()
        .map(|o| {
            ListItem::new(format!(
                "{} {}",
                o.kind.as_deref().unwrap_or("?"),
                o.key.as_deref().unwrap_or("?")
            ))
        })
        .collect();
    let mut state = ListState::default().with_selected(if items.is_empty() {
        None
    } else {
        Some(app.selected.min(items.len() - 1))
    });
    frame.render_stateful_widget(
        List::new(items)
            .highlight_style(Style::default().bg(Color::DarkGray))
            .highlight_symbol("> ")
            .block(
                Block::default()
                    .borders(Borders::ALL)
                    .title("Resources | j/k select"),
            ),
        panes[0],
        &mut state,
    );
    if app.page == 5 && app.details.is_empty() && app.input.is_none() {
        let crows = Layout::default()
            .direction(Direction::Vertical)
            .constraints([Constraint::Length(8), Constraint::Min(3)])
            .split(panes[1]);
        let text = format!(
            "in: {}   out: {}\n{}\n{}",
            pretty_bps(app.last_rate.in_bps),
            pretty_bps(app.last_rate.out_bps),
            COUNTERS
                .iter()
                .map(|n| format!(
                    "{n}: {}",
                    app.counters
                        .get(*n)
                        .map(u64::to_string)
                        .unwrap_or_else(|| "unavailable".into())
                ))
                .collect::<Vec<_>>()
                .join("  "),
            app.last_rate.notes.join("; ")
        );
        frame.render_widget(
            Paragraph::new(text).wrap(Wrap { trim: false }).block(
                Block::default()
                    .borders(Borders::ALL)
                    .title("Live counters (unsigned u64; never cleared)"),
            ),
            crows[0],
        );
        let inbound: Vec<(f64, f64)> = app
            .rates
            .history
            .iter()
            .enumerate()
            .filter_map(|(i, s)| s.in_bps.map(|v| (i as f64, v)))
            .collect();
        let outbound: Vec<(f64, f64)> = app
            .rates
            .history
            .iter()
            .enumerate()
            .filter_map(|(i, s)| s.out_bps.map(|v| (i as f64, v)))
            .collect();
        let max = inbound
            .iter()
            .chain(&outbound)
            .map(|(_, v)| *v)
            .fold(1.0, f64::max);
        let datasets = vec![
            Dataset::default()
                .name("in")
                .marker(Marker::Braille)
                .graph_type(GraphType::Scatter)
                .style(Style::default().fg(Color::Green))
                .data(&inbound),
            Dataset::default()
                .name("out")
                .marker(Marker::Braille)
                .graph_type(GraphType::Scatter)
                .style(Style::default().fg(Color::Cyan))
                .data(&outbound),
        ];
        frame.render_widget(
            Chart::new(datasets)
                .block(
                    Block::default()
                        .borders(Borders::ALL)
                        .title("Traffic history bit/s | last 120 samples | gaps omitted"),
                )
                .x_axis(Axis::default().title("sample index").bounds([0.0, 119.0]))
                .y_axis(
                    Axis::default()
                        .bounds([0.0, max])
                        .labels([Span::raw("0"), Span::raw(format!("{max:.0}"))]),
                ),
            crows[1],
        );
    } else {
        let selected=app.selected().map(|o|serde_json::to_string_pretty(&client::object_json(o)).unwrap_or_default()).unwrap_or_else(||"No discovered objects on this page. :get KIND KEY can inspect known keys not enumerated. r reconnect/refresh".into());
        let text = if app.review.is_some()
            || app
                .input
                .as_deref()
                .is_some_and(|s| s.starts_with("preset"))
        {
            app.details.clone()
        } else if app.page == 6 {
            format!("KEYS: Tab/1..7 pages; j/k select; Enter/g actual getter; r snapshot/reconnect; p switch presets (load locally, apply separately); : command; c create draft; e set draft; d remove review; ? field help; w warnings; l live/clear details; PgUp/PgDn scroll; q/Ctrl-C quit.\n\nAccess: create vlan + bridge_port + untagged vlan_member, then set port pvid. Trunk: tagged vlan_member per VLAN; PVID only for intended native VLAN. Each step needs its own confirmation.\nSAI RIF + neighbor + next hop + route enables L3; SAI does not assign interface IP aliases.\nFDB may be notification-derived, not exhaustive. Hardware capability errors are preserved.\n\n{}",command::help(None))
        } else if let Some(input) = &app.input {
            let kind = input
                .split_whitespace()
                .nth(1)
                .filter(|k| command::KINDS.contains(k));
            format!(
                "COMMAND HELP\n{}\n\nSELECTED\n{selected}",
                command::help(kind)
            )
        } else if !app.details.is_empty() {
            app.details.clone()
        } else {
            format!("Discovered getter snapshot (r refresh, Enter get):\n{selected}")
        };
        let text = if app.page == 2 && app.review.is_none() {
            format!("FDB is read-only; this view may be notification-derived, NOT exhaustive ASIC inventory. Consult inventory warnings (w).\n\n{text}")
        } else {
            text
        };
        frame.render_widget(
            Paragraph::new(text)
                .wrap(Wrap { trim: false })
                .scroll((app.scroll, 0))
                .block(
                    Block::default()
                        .borders(Borders::ALL)
                        .title("Details / audit | PgUp/PgDn scroll"),
                ),
            panes[1],
        );
    }
    let warnings = app
        .inventory
        .warnings
        .as_deref()
        .unwrap_or_default()
        .join(" | ");
    let style = Style::default().fg(if app.failed {
        Color::Red
    } else {
        Color::Yellow
    });
    frame.render_widget(
        Paragraph::new(format!(
            "{}\nINVENTORY WARNINGS: {}",
            app.status,
            if warnings.is_empty() {
                "none reported (not proof of exhaustive enumeration)"
            } else {
                &warnings
            }
        ))
        .style(style)
        .wrap(Wrap { trim: false })
        .block(
            Block::default()
                .borders(Borders::ALL)
                .title("Status / warnings"),
        ),
        rows[2],
    );
    let bottom = if let Some(review) = &app.review {
        match &review.action {
            ReviewAction::Mutation(cmd) => format!("REVIEW MUTATION: {}\nParsed: {cmd:?}\nMay change live hardware. No rollback. y CONFIRM / n or Esc CANCEL", review.text),
            ReviewAction::ApplyPreset => "REVIEW HARDWARE APPLY: y APPLIES ONCE / n or Esc CANCEL\nMay change live hardware. No rollback or retries. Quitting stops only unsent operations.".into(),
            ReviewAction::LoadPreset(_) => format!("REVIEW LOCAL LOAD: {}\nReplaces staged configuration ONLY; does NOT apply hardware.\ny LOAD / n or Esc CANCEL", review.text),
        }
    } else if let Some(input) = &app.input {
        format!(":{input}\nEnter validate/review; Esc cancel. Field help is above; no mutation on Enter alone.")
    } else {
        "p load preset | a apply staged (review) | : command | c create | e edit | d remove (review) | ? help | w warnings | l live | r reconnect | Enter getter".into()
    };
    frame.render_widget(
        Paragraph::new(bottom).wrap(Wrap { trim: false }).block(
            Block::default()
                .borders(Borders::ALL)
                .title(if app.review.is_some() {
                    "Explicit confirmation required"
                } else {
                    "Command input"
                }),
        ),
        rows[3],
    );
}

#[cfg(test)]
mod tests {
    use super::*;
    use ratatui::backend::TestBackend;
    fn test_app() -> (App, Receiver<Job>) {
        let (tx, rx) = mpsc::sync_channel(1);
        let app = App {
            inventory: Inventory::default(),
            page: 1,
            selected: 0,
            busy: false,
            status: String::new(),
            failed: false,
            input: None,
            review: None,
            staged: None,
            staging: Staging::default(),
            details: String::new(),
            scroll: 0,
            counters: BTreeMap::new(),
            rates: Rates::new(Duration::from_secs(1)),
            last_rate: RateSample::default(),
            counter_key: None,
            next_poll: Instant::now(),
            tx,
            applying: false,
        };
        (app, rx)
    }
    #[test]
    fn staged_preset_confirmation_cancellation_and_invalid_load_send_no_rpc() {
        let (mut app, rx) = test_app();
        app.inventory = preset_plan::fixture();
        let load = format!("preset load {}", presets::SEASTONE2_ID);
        app.prepare(load.clone());
        assert!(matches!(
            app.review.as_ref().map(|r| &r.action),
            Some(ReviewAction::LoadPreset(_))
        ));
        assert!(app.staged.is_none());
        assert!(rx.try_recv().is_err());
        for (w, h) in [(120, 35), (30, 8), (1, 1)] {
            let mut terminal = Terminal::new(TestBackend::new(w, h)).unwrap();
            terminal
                .draw(|f| draw(f, &mut app, "127.0.0.1:9090"))
                .unwrap();
        }
        app.cancel_review();
        assert!(app.staged.is_none());
        app.prepare(load.clone());
        app.confirm_review().unwrap();
        let old = app.staged.clone();
        assert!(old.is_some());
        assert!(rx.try_recv().is_err());
        app.prepare(load.clone());
        app.cancel_review();
        assert_eq!(app.staged, old);
        app.prepare("preset load nonexistent".into());
        assert!(app.failed);
        assert_eq!(app.staged, old);
        app.prepare(load.clone());
        // Inventory may change between review and confirmation; fail closed.
        app.inventory.objects.as_mut().unwrap().pop();
        assert!(app.confirm_review().is_err());
        assert_eq!(app.staged, old);
        app.prepare(load);
        assert!(app.failed);
        assert_eq!(app.staged, old);
        assert!(rx.try_recv().is_err());
    }
    #[test]
    fn applying_requires_separate_confirmation_and_cancellation_preserves_stage() {
        let (mut app, rx) = test_app();
        app.inventory = preset_plan::fixture();
        app.prepare(format!("preset load {}", presets::SEASTONE2_ID));
        app.confirm_review().unwrap();
        let original = app.staging.plan().cloned();
        assert!(rx.try_recv().is_err());
        app.prepare_apply().unwrap();
        assert!(matches!(
            app.review.as_ref().map(|r| &r.action),
            Some(ReviewAction::ApplyPreset)
        ));
        assert!(rx.try_recv().is_err());
        app.cancel_review();
        assert_eq!(app.staging.plan(), original.as_ref());
        assert!(rx.try_recv().is_err());
        app.prepare("preset apply".into());
        app.confirm_review().unwrap();
        let staging = match rx.try_recv().unwrap() {
            Job::Apply(staging, _, _) => staging,
            _ => panic!("separate apply job required"),
        };
        assert_eq!(staging.plan(), original.as_ref());
        assert!(app.busy && app.applying);
        assert!(rx.try_recv().is_err());
        // A partially applied plan must be reloaded, never re-applied as-is.
        app.reply(Reply::Applied(
            staging,
            ApplyReport {
                status: ApplyStatus::Failed {
                    step: 1,
                    reason: "test".into(),
                },
                steps: vec![],
                bindings: BTreeMap::new(),
                inventory: None,
                partial_effects: true,
            },
        ));
        assert!(!app.busy && !app.applying && app.staged.is_none());
        assert!(app.prepare_apply().is_err());
        assert!(rx.try_recv().is_err());
    }
    #[test]
    fn bounded_ui_review_cancel_and_small_terminal_render() {
        let (mut app, rx) = test_app();
        app.prepare("create vlan vlan_id=100".into());
        assert!(app.review.is_some());
        assert!(rx.try_recv().is_err());
        app.review = None;
        assert!(rx.try_recv().is_err());
        for (w, h) in [(120, 35), (30, 8), (1, 1)] {
            let mut terminal = Terminal::new(TestBackend::new(w, h)).unwrap();
            for page in 0..7 {
                app.page = page;
                terminal
                    .draw(|f| draw(f, &mut app, "127.0.0.1:9090"))
                    .unwrap();
            }
        }
        assert!(app.dispatch(Job::Snapshot));
        assert!(!app.dispatch(Job::Snapshot));
        assert!(matches!(rx.try_recv(), Ok(Job::Snapshot)));
        assert!(rx.try_recv().is_err());
    }
}
