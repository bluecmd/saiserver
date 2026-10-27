use clap::Parser;
use sai_tui::{
    client::{self, Client, Service},
    command::{self, Command},
    rates::Rates,
    ui,
};
use serde_json::json;
use std::{
    io::{self, Write},
    net::SocketAddr,
    process::ExitCode,
    thread,
    time::{Duration, Instant, SystemTime, UNIX_EPOCH},
};

#[derive(Parser, Debug)]
#[command(
    version,
    about = "SAI management: binary/buffered Thrift; all mutations require explicit confirmation",
    after_help = "Use --command 'help' or --command 'help KIND' for the full field schema.\nNo authentication: use an isolated lab or SSH tunnel. Endpoint must be a numeric IP:port (IPv6: [::1]:9090), avoiding unbounded DNS resolution."
)]
struct Args {
    #[arg(long, default_value = "127.0.0.1:9090")]
    endpoint: SocketAddr,
    #[arg(long,default_value_t=2000,value_parser=clap::value_parser!(u64).range(100..=60000))]
    timeout_ms: u64,
    /// Print one real discovery snapshot as JSON, then exit.
    #[arg(long, conflicts_with = "command")]
    snapshot: bool,
    /// Validated command (quote as one argument). No mutation without --yes.
    #[arg(long)]
    command: Option<String>,
    /// Explicitly approve the batch mutation. Never enables automatic retries.
    #[arg(long, requires = "command")]
    yes: bool,
    /// Number of samples for --command 'counters PORT_OID' (JSON lines).
    #[arg(long,default_value_t=1,value_parser=clap::value_parser!(u32).range(1..=10000))]
    samples: u32,
    /// UI counter polling and batch sampling interval; actual elapsed time drives rates.
    #[arg(long,default_value_t=1000,value_parser=clap::value_parser!(u64).range(100..=60000))]
    interval_ms: u64,
}
fn emit(value: &serde_json::Value, pretty: bool) -> io::Result<()> {
    let mut out = io::stdout().lock();
    if pretty {
        serde_json::to_writer_pretty(&mut out, value)?;
    } else {
        serde_json::to_writer(&mut out, value)?;
    }
    writeln!(out)?;
    out.flush()
}
fn run(args: Args) -> Result<bool, Box<dyn std::error::Error>> {
    let mut client = Client {
        endpoint: args.endpoint,
        timeout: Duration::from_millis(args.timeout_ms),
    };
    let interval = Duration::from_millis(args.interval_ms);
    if let Some(text) = args.command {
        // Reject invalid/unconfirmed commands before opening a socket.
        let command = command::parse(&text).map_err(io::Error::other)?;
        let approval = command::approve(&command, args.yes).map_err(io::Error::other)?;
        if let Command::Counters { key } = &command {
            let mut rates = Rates::new(interval);
            for index in 0..args.samples {
                let start = Instant::now();
                let timestamp = SystemTime::now().duration_since(UNIX_EPOCH)?.as_secs_f64();
                match client.counters(key) {
                    Ok(counters) => {
                        let sample = rates.sample(Instant::now(), &counters);
                        emit(
                            &json!({"ok":true,"key":key,"sample":index+1,"unix_seconds":timestamp,"counters":counters,"rates":sample}),
                            false,
                        )?;
                    }
                    Err(error) => {
                        let sample = rates.disconnected(&error.to_string());
                        emit(
                            &json!({"ok":false,"key":key,"sample":index+1,"error":error,"rates":sample}),
                            false,
                        )?;
                        return Ok(false);
                    }
                }
                if index + 1 < args.samples {
                    thread::sleep(interval.saturating_sub(start.elapsed()));
                }
            }
            return Ok(true);
        }
        if args.samples != 1 {
            return Err(io::Error::other("--samples applies only to counters commands").into());
        }
        if command.mutates() {
            eprintln!("Explicit --yes approval: {command:?}. Sending once; failures can have partial effects.");
        }
        let result = client::execute(&mut client, &command, approval);
        emit(
            &json!({"ok":result.ok,"command":text,"result":result.value}),
            true,
        )?;
        return Ok(result.ok);
    }
    if args.samples != 1 {
        return Err(io::Error::other("--samples requires --command 'counters PORT_OID'").into());
    }
    if args.snapshot {
        match client.snapshot() {
            Ok(inventory) => {
                emit(
                    &json!({"ok":true,"inventory":client::inventory_json(&inventory)}),
                    true,
                )?;
                Ok(true)
            }
            Err(error) => {
                emit(&json!({"ok":false,"error":error}), true)?;
                Ok(false)
            }
        }
    } else {
        ui::run(client, interval)?;
        Ok(true)
    }
}
fn main() -> ExitCode {
    match run(Args::parse()) {
        Ok(true) => ExitCode::SUCCESS,
        Ok(false) => ExitCode::FAILURE,
        Err(error) => {
            let _ = emit(&json!({"ok":false,"error":error.to_string()}), false);
            eprintln!("sai-tui: {error}");
            ExitCode::FAILURE
        }
    }
}
