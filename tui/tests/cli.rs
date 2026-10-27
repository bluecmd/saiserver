use sai_tui::sai_tui::{Inventory, Object, RpcError, SaiTuiSyncHandler, SaiTuiSyncProcessor};
use serde_json::Value;
use std::{
    collections::BTreeMap,
    io,
    net::{SocketAddr, TcpListener},
    process::{Command, Output},
    sync::{Arc, Mutex},
    thread,
    time::{Duration, Instant},
};
use thrift::{
    protocol::{TBinaryInputProtocol, TBinaryOutputProtocol},
    server::TProcessor,
    transport::{TBufferedReadTransport, TBufferedWriteTransport},
};
struct Handler {
    log: Arc<Mutex<Vec<String>>>,
}
impl Handler {
    fn record(&self, s: &str) {
        self.log.lock().unwrap().push(s.into());
    }
}
impl SaiTuiSyncHandler for Handler {
    fn handle_tui_snapshot(&self) -> thrift::Result<Inventory> {
        self.record("snapshot");
        Ok(Inventory::new(
            vec![],
            vec!["notification-derived FDB; inventory limited to this process".into()],
        ))
    }
    fn handle_tui_get(&self, kind: String, key: String) -> thrift::Result<Object> {
        self.record("get");
        if key == "0xff" {
            Err(RpcError::new(-7, "not found".to_owned()).into())
        } else {
            Ok(Object::new(
                kind,
                key,
                BTreeMap::from([
                    ("observed".into(), "hardware".into()),
                    ("vlan_id".into(), "100".into()),
                ]),
            ))
        }
    }
    fn handle_tui_create(
        &self,
        kind: String,
        attrs: BTreeMap<String, String>,
    ) -> thrift::Result<Object> {
        self.record("create");
        Ok(Object::new(kind, "0x2".to_owned(), attrs))
    }
    fn handle_tui_set(
        &self,
        _: String,
        _: String,
        _: BTreeMap<String, String>,
    ) -> thrift::Result<Object> {
        self.record("set");
        Err(RpcError::new(-2, "IPv6 ACL unsupported on this ASIC".to_owned()).into())
    }
    fn handle_tui_remove(&self, _: String, _: String) -> thrift::Result<()> {
        self.record("remove");
        Ok(())
    }
    fn handle_tui_port_counters(&self, key: String) -> thrift::Result<BTreeMap<String, i64>> {
        self.record("counters");
        if key == "0xff" {
            return Err(RpcError::new(-2, "port counters unsupported".to_owned()).into());
        }
        let count = self.log.lock().unwrap().len() as i64;
        Ok(BTreeMap::from([
            ("in_octets".into(), 100 * count),
            ("out_octets".into(), -1),
        ]))
    }
}
fn server(count: usize) -> (SocketAddr, Arc<Mutex<Vec<String>>>, thread::JoinHandle<()>) {
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    listener.set_nonblocking(true).unwrap();
    let addr = listener.local_addr().unwrap();
    let log = Arc::new(Mutex::new(vec![]));
    let handler = Handler { log: log.clone() };
    let handle = thread::spawn(move || {
        let processor = SaiTuiSyncProcessor::new(handler);
        let deadline = Instant::now() + Duration::from_secs(5);
        for _ in 0..count {
            let s = loop {
                match listener.accept() {
                    Ok((s, _)) => break s,
                    Err(e) if e.kind() == io::ErrorKind::WouldBlock => {
                        assert!(Instant::now() < deadline, "missing expected RPC");
                        thread::sleep(Duration::from_millis(1));
                    }
                    Err(e) => panic!("{e}"),
                }
            };
            s.set_read_timeout(Some(Duration::from_secs(2))).unwrap();
            s.set_write_timeout(Some(Duration::from_secs(2))).unwrap();
            let mut input = TBinaryInputProtocol::new(
                TBufferedReadTransport::new(s.try_clone().unwrap()),
                true,
            );
            let mut output = TBinaryOutputProtocol::new(TBufferedWriteTransport::new(s), true);
            processor.process(&mut input, &mut output).unwrap();
        }
    });
    (addr, log, handle)
}
fn invoke(addr: SocketAddr, args: &[&str]) -> Output {
    Command::new(env!("CARGO_BIN_EXE_sai-tui"))
        .arg("--endpoint")
        .arg(addr.to_string())
        .args(args)
        .output()
        .unwrap()
}
fn value(o: &Output) -> Value {
    serde_json::from_slice(&o.stdout).unwrap_or_else(|e| panic!("bad JSON: {e}; {o:?}"))
}
#[test]
fn batch_requires_explicit_yes_and_reports_validation_in_stdout() {
    for command in [
        "create vlan vlan_id=100",
        "set port 1 admin=true",
        "remove vlan 1",
    ] {
        let o = invoke("127.0.0.1:1".parse().unwrap(), &["--command", command]);
        assert!(!o.status.success());
        assert!(value(&o)["error"]
            .as_str()
            .unwrap()
            .contains("confirmation"));
    }
    let o = invoke(
        "127.0.0.1:1".parse().unwrap(),
        &["--command", "create vlan vlan_id=9999", "--yes"],
    );
    assert!(!o.status.success());
    assert!(value(&o)["error"].as_str().unwrap().contains("vlan_id"));
}
#[test]
fn headless_snapshot_get_help_and_connection_failure() {
    let (addr, _, h) = server(1);
    let o = invoke(addr, &["--snapshot"]);
    assert!(o.status.success());
    assert!(value(&o)["inventory"]["warnings"][0]
        .as_str()
        .unwrap()
        .contains("limited"));
    h.join().unwrap();
    let (addr, _, h) = server(1);
    let o = invoke(addr, &["--command", "get neighbor 1@2001:db8::1"]);
    assert!(o.status.success());
    assert_eq!(value(&o)["result"]["value"]["key"], "0x1@2001:db8::1");
    h.join().unwrap();
    let o = invoke(
        "127.0.0.1:1".parse().unwrap(),
        &["--command", "help acl_entry"],
    );
    assert!(o.status.success());
    assert!(value(&o)["result"]["help"]
        .as_str()
        .unwrap()
        .contains("protocol"));
    let listener = TcpListener::bind("127.0.0.1:0").unwrap();
    let addr = listener.local_addr().unwrap();
    drop(listener);
    let o = invoke(addr, &["--snapshot", "--timeout-ms", "100"]);
    assert!(!o.status.success());
    assert_eq!(value(&o)["error"]["category"], "connect");
}
#[test]
fn successful_batch_create_runs_getter_and_snapshot() {
    let (addr, log, h) = server(4);
    let o = invoke(addr, &["--command", "create vlan vlan_id=100", "--yes"]);
    assert!(o.status.success(), "{o:?}");
    let v = value(&o);
    assert_eq!(
        v["result"]["readback"]["value"]["attributes"]["observed"],
        "hardware"
    );
    h.join().unwrap();
    assert_eq!(
        *log.lock().unwrap(),
        ["snapshot", "create", "get", "snapshot"]
    );
}
#[test]
fn batch_server_failure_preserves_status_and_partial_readback_nonzero() {
    let (addr, log, h) = server(4);
    let o = invoke(addr, &["--command", "set port 1 ingress_acl=2", "--yes"]);
    assert!(!o.status.success());
    let v = value(&o);
    assert_eq!(v["result"]["mutation"]["error"]["status"], -2);
    assert!(v["result"]["mutation"]["error"]["message"]
        .as_str()
        .unwrap()
        .contains("IPv6 ACL"));
    assert_eq!(v["result"]["readback"]["ok"], true);
    h.join().unwrap();
    assert_eq!(*log.lock().unwrap(), ["snapshot", "set", "get", "snapshot"]);
}
#[test]
fn batch_getter_error_is_nonzero() {
    let (addr, _, h) = server(1);
    let o = invoke(addr, &["--command", "get vlan 255"]);
    assert!(!o.status.success());
    assert_eq!(value(&o)["result"]["error"]["status"], -7);
    h.join().unwrap();
}
#[test]
fn acknowledged_but_unverified_mutation_exits_nonzero() {
    let (addr, log, h) = server(4);
    let o = invoke(addr, &["--command", "create vlan vlan_id=200", "--yes"]);
    assert!(!o.status.success());
    assert_eq!(
        value(&o)["result"]["attribute_mismatches"][0]["field"],
        "vlan_id"
    );
    h.join().unwrap();
    assert_eq!(
        *log.lock().unwrap(),
        ["snapshot", "create", "get", "snapshot"]
    );
}
#[test]
fn failed_counter_sampling_exits_nonzero_without_implicit_retry_or_zero_fill() {
    let (addr, log, h) = server(1);
    let o = invoke(addr, &["--command", "counters 255", "--samples", "2"]);
    assert!(!o.status.success());
    let v = value(&o);
    assert_eq!(v["error"]["status"], -2);
    assert!(v.get("counters").is_none());
    assert!(v["rates"]["in_bps"].is_null());
    h.join().unwrap();
    assert_eq!(*log.lock().unwrap(), ["counters"]);
}
#[test]
fn headless_counter_json_lines_unsigned_missing_and_actual_rates() {
    let (addr, log, h) = server(2);
    let o = invoke(
        addr,
        &[
            "--command",
            "counters 1",
            "--samples",
            "2",
            "--interval-ms",
            "100",
        ],
    );
    assert!(o.status.success());
    let lines: Vec<Value> = String::from_utf8(o.stdout)
        .unwrap()
        .lines()
        .map(|s| serde_json::from_str(s).unwrap())
        .collect();
    assert_eq!(lines.len(), 2);
    assert_eq!(lines[0]["counters"]["out_octets"].as_u64(), Some(u64::MAX));
    assert!(lines[0]["rates"]["in_bps"].is_null());
    assert!(lines[1]["rates"]["in_bps"].as_f64().unwrap() > 0.0);
    assert!(lines[1]["rates"]["interval_seconds"].as_f64().unwrap() >= 0.08);
    assert!(lines[1]["counters"].get("in_errors").is_none());
    assert!(lines[1]["rates"]["notes"]
        .as_array()
        .unwrap()
        .iter()
        .any(|n| n.as_str().unwrap().contains("in_errors unavailable")));
    h.join().unwrap();
    assert_eq!(*log.lock().unwrap(), ["counters", "counters"]);
}
