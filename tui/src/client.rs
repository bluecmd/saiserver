//! Real SaiTui calls (inherited by switch_sai_rpc), strict binary protocol over
//! buffered TCP. Each call gets a fresh connection and an absolute deadline.
use crate::{
    command::{self, Approval, Command, Value as FieldValue},
    sai_tui::{Inventory, Object, RpcError, SaiTuiSyncClient, TSaiTuiSyncClient},
};
use serde::Serialize;
use serde_json::{json, Value};
use std::{
    collections::BTreeMap,
    io::{self, Read, Write},
    net::{SocketAddr, TcpStream},
    time::{Duration, Instant},
};
use thrift::{
    protocol::{TBinaryInputProtocol, TBinaryOutputProtocol},
    transport::{TBufferedReadTransport, TBufferedWriteTransport},
    TConfiguration,
};

#[derive(Clone, Debug, Serialize)]
pub struct Failure {
    pub category: String,
    pub status: Option<i32>,
    pub message: String,
}
impl std::fmt::Display for Failure {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "{} status={:?}: {}",
            self.category, self.status, self.message
        )
    }
}
impl std::error::Error for Failure {}
impl From<thrift::Error> for Failure {
    fn from(e: thrift::Error) -> Self {
        if let thrift::Error::User(ref user) = e {
            if let Some(rpc) = user.downcast_ref::<RpcError>() {
                return Self {
                    category: "server".into(),
                    status: rpc.status,
                    message: rpc
                        .message
                        .clone()
                        .unwrap_or_else(|| "RpcError without message".into()),
                };
            }
        }
        // Thrift's Display omits useful error details; retain Debug as well.
        Self {
            category: "transport/protocol".into(),
            status: None,
            message: format!("{e}: {e:?}"),
        }
    }
}
fn local(message: impl Into<String>) -> Failure {
    Failure {
        category: "validation".into(),
        status: None,
        message: message.into(),
    }
}

struct DeadlineStream {
    stream: TcpStream,
    deadline: Instant,
    remaining: usize,
}
impl DeadlineStream {
    fn timeout(&self) -> io::Result<Duration> {
        self.deadline
            .checked_duration_since(Instant::now())
            .filter(|d| !d.is_zero())
            .ok_or_else(|| {
                io::Error::new(io::ErrorKind::TimedOut, "absolute RPC deadline exceeded")
            })
    }
}
impl Read for DeadlineStream {
    fn read(&mut self, buffer: &mut [u8]) -> io::Result<usize> {
        self.stream.set_read_timeout(Some(self.timeout()?))?;
        if self.remaining == 0 {
            return Err(io::Error::new(
                io::ErrorKind::InvalidData,
                "response exceeds 16 MiB",
            ));
        }
        let len = buffer.len().min(self.remaining);
        let n = self.stream.read(&mut buffer[..len])?;
        self.remaining -= n;
        Ok(n)
    }
}
impl Write for DeadlineStream {
    fn write(&mut self, buffer: &[u8]) -> io::Result<usize> {
        self.stream.set_write_timeout(Some(self.timeout()?))?;
        self.stream.write(buffer)
    }
    fn flush(&mut self) -> io::Result<()> {
        self.stream.set_write_timeout(Some(self.timeout()?))?;
        self.stream.flush()
    }
}
type WireClient = SaiTuiSyncClient<
    TBinaryInputProtocol<TBufferedReadTransport<DeadlineStream>>,
    TBinaryOutputProtocol<TBufferedWriteTransport<DeadlineStream>>,
>;
#[derive(Clone, Debug)]
pub struct Client {
    pub endpoint: SocketAddr,
    pub timeout: Duration,
}
impl Client {
    fn connect(&self) -> Result<WireClient, Failure> {
        let deadline = Instant::now() + self.timeout;
        let stream =
            TcpStream::connect_timeout(&self.endpoint, self.timeout).map_err(|e| Failure {
                category: "connect".into(),
                status: None,
                message: format!("{}: {e}", self.endpoint),
            })?;
        stream.set_nodelay(true).map_err(|e| local(e.to_string()))?;
        let reader = stream.try_clone().map_err(|e| local(e.to_string()))?;
        let config = TConfiguration::builder()
            .max_message_size(Some(16 * 1024 * 1024))
            .max_string_size(Some(1024 * 1024))
            .max_container_size(Some(65536))
            .max_recursion_depth(Some(32))
            .build()
            .map_err(Failure::from)?;
        Ok(SaiTuiSyncClient::new(
            TBinaryInputProtocol::with_config(
                TBufferedReadTransport::new(DeadlineStream {
                    stream: reader,
                    deadline,
                    remaining: 16 * 1024 * 1024,
                }),
                true,
                config,
            ),
            TBinaryOutputProtocol::new(
                TBufferedWriteTransport::new(DeadlineStream {
                    stream,
                    deadline,
                    remaining: 0,
                }),
                true,
            ),
        ))
    }
}
/// The UI and batch executor share this boundary; mocks exercise readback and safety.
pub trait Service {
    fn snapshot(&mut self) -> Result<Inventory, Failure>;
    fn get(&mut self, kind: &str, key: &str) -> Result<Object, Failure>;
    fn create(&mut self, kind: &str, attrs: &BTreeMap<String, String>) -> Result<Object, Failure>;
    fn set(
        &mut self,
        kind: &str,
        key: &str,
        attrs: &BTreeMap<String, String>,
    ) -> Result<Object, Failure>;
    fn remove(&mut self, kind: &str, key: &str) -> Result<(), Failure>;
    fn counters(&mut self, key: &str) -> Result<BTreeMap<String, u64>, Failure>;
}
impl Service for Client {
    fn snapshot(&mut self) -> Result<Inventory, Failure> {
        self.connect()?.tui_snapshot().map_err(Into::into)
    }
    fn get(&mut self, kind: &str, key: &str) -> Result<Object, Failure> {
        self.connect()?
            .tui_get(kind.into(), key.into())
            .map_err(Into::into)
    }
    fn create(&mut self, kind: &str, attrs: &BTreeMap<String, String>) -> Result<Object, Failure> {
        self.connect()?
            .tui_create(kind.into(), attrs.clone())
            .map_err(Into::into)
    }
    fn set(
        &mut self,
        kind: &str,
        key: &str,
        attrs: &BTreeMap<String, String>,
    ) -> Result<Object, Failure> {
        self.connect()?
            .tui_set(kind.into(), key.into(), attrs.clone())
            .map_err(Into::into)
    }
    fn remove(&mut self, kind: &str, key: &str) -> Result<(), Failure> {
        self.connect()?
            .tui_remove(kind.into(), key.into())
            .map_err(Into::into)
    }
    fn counters(&mut self, key: &str) -> Result<BTreeMap<String, u64>, Failure> {
        self.connect()?
            .tui_port_counters(key.into())
            .map(|m| m.into_iter().map(|(k, v)| (k, v as u64)).collect())
            .map_err(Into::into)
    }
}
pub fn object_json(o: &Object) -> Value {
    json!({"kind":o.kind,"key":o.key,"attributes":o.attributes})
}
pub fn inventory_json(i: &Inventory) -> Value {
    json!({"objects":i.objects.as_deref().unwrap_or_default().iter().map(object_json).collect::<Vec<_>>(),"warnings":i.warnings.as_deref().unwrap_or_default()})
}
#[derive(Debug)]
pub struct Outcome {
    pub ok: bool,
    pub value: Value,
    pub inventory: Option<Inventory>,
}
fn result_json<T>(r: &Result<T, Failure>, f: impl FnOnce(&T) -> Value) -> Value {
    match r {
        Ok(v) => json!({"ok":true,"value":f(v)}),
        Err(e) => json!({"ok":false,"error":e}),
    }
}

/// Validate references known to discovery. Absence cannot imply nonexistence:
/// hardware enumeration is incomplete, so unknown OIDs remain server-authoritative.
pub fn validate_references(cmd: &Command, inventory: &Inventory) -> Result<Vec<String>, String> {
    let mut notes = Vec::new();
    if let Some((kind, attrs)) = cmd.attributes() {
        for field in command::fields(kind) {
            let Some(v) = attrs.get(field.name) else {
                continue;
            };
            if let FieldValue::Oid(kinds, _) = field.value {
                if v == "0x0" {
                    continue;
                }
                let known = inventory
                    .objects
                    .as_deref()
                    .unwrap_or_default()
                    .iter()
                    .find(|o| o.key.as_deref() == Some(v));
                if let Some(o) = known {
                    let actual = o.kind.as_deref().unwrap_or_default();
                    if !kinds.contains(&actual) {
                        return Err(format!(
                            "{kind}.{}: {v} is {actual}, expected {}",
                            field.name,
                            kinds.join("/")
                        ));
                    }
                } else {
                    notes.push(format!(
                        "{}.{}={} not in limited inventory; server must validate reference",
                        kind, field.name, v
                    ));
                }
            }
        }
    }
    if let Some(("acl_entry", attrs)) = cmd.attributes() {
        let objects = inventory.objects.as_deref().unwrap_or_default();
        let existing_table = cmd
            .target()
            .and_then(|(_, key)| {
                objects.iter().find(|o| {
                    o.kind.as_deref() == Some("acl_entry") && o.key.as_deref() == Some(key)
                })
            })
            .and_then(|o| o.attributes.as_ref())
            .and_then(|a| a.get("table"));
        if let Some(table) = attrs.get("table").or(existing_table) {
            let family = objects
                .iter()
                .find(|o| o.kind.as_deref() == Some("acl_table") && o.key.as_deref() == Some(table))
                .and_then(|o| o.attributes.as_ref())
                .and_then(|a| a.get("family"));
            if let Some(family) = family {
                for name in ["src", "dst"] {
                    if attrs
                        .get(name)
                        .is_some_and(|cidr| cidr.contains(':') != (family == "ipv6"))
                    {
                        return Err(format!("acl_entry.{name} must match table {family}"));
                    }
                }
            }
        }
    }
    Ok(notes)
}

fn checked_get(service: &mut impl Service, kind: &str, key: &str) -> Result<Object, Failure> {
    let object = service.get(kind, key)?;
    if object.kind.as_deref() != Some(kind)
        || object.key.as_deref() != Some(key)
        || object.attributes.is_none()
    {
        return Err(Failure {
            category: "protocol".into(),
            status: None,
            message: format!(
                "getter returned a mismatched/incomplete object: {object:?}; expected {kind} {key}"
            ),
        });
    }
    Ok(object)
}

pub fn execute(
    service: &mut impl Service,
    command: &Command,
    approval: Option<Approval>,
) -> Outcome {
    if command.mutates() && approval.is_none() {
        return Outcome {
            ok: false,
            value: json!({"error":"mutation not confirmed; no RPC sent"}),
            inventory: None,
        };
    }
    match command {
        Command::Help { kind } => Outcome {
            ok: true,
            value: json!({"help":command::help(kind.as_deref())}),
            inventory: None,
        },
        Command::Get { kind, key } => {
            let r = checked_get(service, kind, key);
            Outcome {
                ok: r.is_ok(),
                value: result_json(&r, object_json),
                inventory: None,
            }
        }
        Command::Counters { key } => {
            let r = service.counters(key);
            Outcome {
                ok: r.is_ok(),
                value: result_json(&r, |m| json!(m)),
                inventory: None,
            }
        }
        _ => mutate(service, command),
    }
}
fn mutate(service: &mut impl Service, cmd: &Command) -> Outcome {
    // Read-only preflight; no implicit retry, even if the response is lost.
    let preflight = service.snapshot();
    let notes = match &preflight {
        Ok(i) => match validate_references(cmd, i) {
            Ok(n) => n,
            Err(e) => {
                return Outcome {
                    ok: false,
                    value: json!({"error":e,"phase":"preflight; no mutation sent"}),
                    inventory: Some(i.clone()),
                }
            }
        },
        Err(e) => {
            return Outcome {
                ok: false,
                value: json!({"error":e,"phase":"preflight snapshot; no mutation sent"}),
                inventory: None,
            }
        }
    };
    let mut target = cmd.target().map(|(k, v)| (k.to_owned(), v.to_owned()));
    // Composite keys are knowable even if the mutation reply is lost.
    if let Command::Create { kind, attrs } = cmd {
        let identity = match kind.as_str() {
            "neighbor" => attrs.get("router_interface").zip(attrs.get("ip")),
            "route" => attrs.get("virtual_router").zip(attrs.get("prefix")),
            _ => None,
        };
        if let Some((oid, suffix)) = identity {
            target = Some((kind.clone(), format!("{oid}@{suffix}")));
        }
    }
    let mutation = match cmd {
        Command::Create { kind, attrs } => service.create(kind, attrs).map(|o| {
            if let Some(k) = o.key.as_ref().filter(|k| command::key(kind, k).is_ok()) {
                target = Some((kind.clone(), k.clone()));
            }
            object_json(&o)
        }),
        Command::Set { kind, key, attrs } => service.set(kind, key, attrs).map(|o| object_json(&o)),
        Command::Remove { kind, key } => service
            .remove(kind, key)
            .map(|_| json!({"removed_request_acknowledged":true})),
        _ => unreachable!(),
    };
    // Always attempt independent actual readbacks, including after an ambiguous failure.
    let readback = target.as_ref().map(|(k, v)| checked_get(service, k, v));
    let snapshot = service.snapshot();
    let removal = matches!(cmd, Command::Remove { .. });
    // After an acknowledged standalone-OID removal, SAI may report
    // INVALID_OBJECT_ID (-19), rather than ITEM_NOT_FOUND (-7). An invalid
    // parent OID on a composite key is NOT proof that an entry was removed.
    let acknowledged_oid_removal = mutation.is_ok()
        && matches!(cmd, Command::Remove { kind, .. } if !matches!(kind.as_str(), "neighbor" | "route" | "fdb"));
    let verified = match &readback {
        Some(Ok(_)) => !removal,
        Some(Err(e)) => {
            removal
                && e.category == "server"
                && (e.status == Some(-7) || (acknowledged_oid_removal && e.status == Some(-19)))
        }
        None => false,
    };
    let mut mismatches = Vec::new();
    if let (Some((kind, requested)), Some(Ok(observed))) = (cmd.attributes(), &readback) {
        for (name, expected) in requested {
            let actual = observed
                .attributes
                .as_ref()
                .and_then(|attrs| attrs.get(name));
            let normalized = actual.and_then(|raw| {
                command::fields(kind)
                    .iter()
                    .find(|f| f.name == name)
                    .and_then(|f| command::value(f.value, raw).ok())
            });
            if normalized.as_ref() != Some(expected) {
                mismatches.push(json!({"field":name,"requested":expected,"observed":actual,"reason":"readback does not verify requested value (missing is not success)"}));
            }
        }
    }
    let ok = mutation.is_ok() && verified && snapshot.is_ok() && mismatches.is_empty();
    let value = json!({
        "ok":ok,
        "mutation":result_json(&mutation,Clone::clone),
        "readback":readback.as_ref().map(|r|result_json(r,object_json)),
        "readback_target":target,
        "readback_unavailable_reason":if readback.is_none() {Some("Object key unavailable after create failure/invalid response; snapshot comparison required; do not retry blindly.")} else {None},
        "removal_verified_absent":removal && verified,
        "snapshot":result_json(&snapshot,inventory_json),
        "reference_warnings":notes,
        "attribute_mismatches":mismatches,
        "notice":if ok {"Observed state follows; inspect readback, not requested attributes."} else {"ERROR / POSSIBLE PARTIAL EFFECT: do not blindly retry. Inspect readback and snapshot. A failed create may have an unknown key; compare inventory."}
    });
    Outcome {
        ok,
        value,
        inventory: snapshot.ok(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::sai_tui::{SaiTuiSyncHandler, SaiTuiSyncProcessor};
    use std::{
        net::TcpListener,
        sync::{Arc, Mutex},
        thread,
    };
    use thrift::server::TProcessor;
    #[derive(Clone)]
    struct Handler(Arc<Mutex<Vec<String>>>);
    impl Handler {
        fn record(&self, s: &str) {
            self.0.lock().unwrap().push(s.into());
        }
    }
    impl SaiTuiSyncHandler for Handler {
        fn handle_tui_snapshot(&self) -> thrift::Result<Inventory> {
            self.record("snapshot");
            Ok(Inventory::new(
                vec![Object::new(
                    "port".to_owned(),
                    "0x1".to_owned(),
                    BTreeMap::new(),
                )],
                vec!["limited inventory".to_owned()],
            ))
        }
        fn handle_tui_get(&self, kind: String, key: String) -> thrift::Result<Object> {
            self.record("get");
            Err(RpcError::new(-7, format!("not found {kind} {key}")).into())
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
            Err(RpcError::new(-2, "unsupported capability".to_owned()).into())
        }
        fn handle_tui_remove(&self, _: String, _: String) -> thrift::Result<()> {
            self.record("remove");
            Ok(())
        }
        fn handle_tui_port_counters(&self, _: String) -> thrift::Result<BTreeMap<String, i64>> {
            self.record("counters");
            Ok(BTreeMap::from([("in_octets".into(), -1)]))
        }
    }
    fn server(calls: usize) -> (Client, Arc<Mutex<Vec<String>>>, thread::JoinHandle<()>) {
        let listener = TcpListener::bind("127.0.0.1:0").unwrap();
        let client = Client {
            endpoint: listener.local_addr().unwrap(),
            timeout: Duration::from_millis(500),
        };
        let log = Arc::new(Mutex::new(Vec::new()));
        let handler = Handler(log.clone());
        let handle = thread::spawn(move || {
            let processor = SaiTuiSyncProcessor::new(handler);
            for _ in 0..calls {
                let (s, _) = listener.accept().unwrap();
                s.set_read_timeout(Some(Duration::from_secs(2))).unwrap();
                let mut ip = TBinaryInputProtocol::new(
                    TBufferedReadTransport::new(s.try_clone().unwrap()),
                    true,
                );
                let mut op = TBinaryOutputProtocol::new(TBufferedWriteTransport::new(s), true);
                processor.process(&mut ip, &mut op).unwrap();
            }
        });
        (client, log, handle)
    }
    #[test]
    fn binary_buffered_boundary_all_methods_unsigned_and_errors() {
        let (mut c, log, h) = server(6);
        assert_eq!(
            c.snapshot().unwrap().warnings.unwrap(),
            vec!["limited inventory"]
        );
        let e = c.get("port", "0x1").unwrap_err();
        assert_eq!(e.status, Some(-7));
        assert!(e.message.contains("port 0x1"));
        assert_eq!(
            c.create("vlan", &BTreeMap::from([("vlan_id".into(), "100".into())]))
                .unwrap()
                .key
                .as_deref(),
            Some("0x2")
        );
        let e = c.set("port", "0x1", &BTreeMap::new()).unwrap_err();
        assert_eq!(e.status, Some(-2));
        assert_eq!(e.message, "unsupported capability");
        c.remove("vlan", "0x2").unwrap();
        assert_eq!(c.counters("0x1").unwrap()["in_octets"], u64::MAX);
        h.join().unwrap();
        assert_eq!(
            *log.lock().unwrap(),
            ["snapshot", "get", "create", "set", "remove", "counters"]
        );
    }
    #[test]
    fn confirmed_mutation_always_gets_real_readbacks_never_retries() {
        let (mut c, log, h) = server(4);
        let cmd = command::parse("set port 1 admin=true").unwrap();
        assert!(!execute(&mut c, &cmd, None).ok);
        assert!(log.lock().unwrap().is_empty());
        let r = execute(&mut c, &cmd, command::approve(&cmd, true).unwrap());
        assert!(!r.ok);
        assert_eq!(r.value["mutation"]["error"]["status"], -2);
        h.join().unwrap();
        assert_eq!(*log.lock().unwrap(), ["snapshot", "set", "get", "snapshot"]);
    }
    #[test]
    fn removal_checks_not_found_and_snapshots() {
        let (mut c, log, h) = server(4);
        let cmd = command::parse("remove vlan 2").unwrap();
        let r = execute(&mut c, &cmd, command::approve(&cmd, true).unwrap());
        assert!(r.ok);
        assert_eq!(r.value["removal_verified_absent"], true);
        h.join().unwrap();
        assert_eq!(
            *log.lock().unwrap(),
            ["snapshot", "remove", "get", "snapshot"]
        );
    }
    #[test]
    fn deadline_and_reconnect_after_stalled_peer() {
        let listener = TcpListener::bind("127.0.0.1:0").unwrap();
        let mut c = Client {
            endpoint: listener.local_addr().unwrap(),
            timeout: Duration::from_millis(70),
        };
        let h = thread::spawn(move || {
            let (mut s, _) = listener.accept().unwrap();
            // Valid strict header, but trickle it more slowly than the TOTAL
            // deadline. An inactivity-only timeout would never fire here.
            for byte in [0x80, 0x01, 0x00, 0x02, 0, 0, 0, 12] {
                if s.write_all(&[byte]).is_err() {
                    break;
                }
                thread::sleep(Duration::from_millis(20));
            }
            drop(s);
            let (s, _) = listener.accept().unwrap();
            let mut ip = TBinaryInputProtocol::new(
                TBufferedReadTransport::new(s.try_clone().unwrap()),
                true,
            );
            let mut op = TBinaryOutputProtocol::new(TBufferedWriteTransport::new(s), true);
            SaiTuiSyncProcessor::new(Handler(Arc::new(Mutex::new(Vec::new()))))
                .process(&mut ip, &mut op)
                .unwrap();
        });
        let start = Instant::now();
        assert!(c.snapshot().is_err());
        assert!(start.elapsed() < Duration::from_millis(250));
        // Explicit subsequent read reconnects successfully; there was no replay.
        c.timeout = Duration::from_millis(500);
        assert!(c.snapshot().is_ok());
        h.join().unwrap();
    }
    #[test]
    fn malformed_truncated_and_oversized_wire_responses_fail_boundedly() {
        for bytes in [
            vec![0x80, 0x01, 0, 2, 0, 0x20, 0, 0],
            vec![0x80, 0x01],
            vec![0x81, 0x01, 0, 2],
        ] {
            let listener = TcpListener::bind("127.0.0.1:0").unwrap();
            let mut c = Client {
                endpoint: listener.local_addr().unwrap(),
                timeout: Duration::from_millis(300),
            };
            let h = thread::spawn(move || {
                let (mut s, _) = listener.accept().unwrap();
                let mut request = [0; 128];
                let _ = s.read(&mut request);
                s.write_all(&bytes).unwrap();
            });
            assert_eq!(c.snapshot().unwrap_err().category, "transport/protocol");
            h.join().unwrap();
        }
    }
    #[test]
    fn known_reference_type_and_acl_family_are_validated() {
        let inventory = Inventory::new(
            vec![Object::new(
                "acl_table".to_owned(),
                "0x1".to_owned(),
                BTreeMap::from([("family".into(), "ipv6".into())]),
            )],
            vec![],
        );
        assert!(validate_references(
            &command::parse("create vlan_member vlan=1 bridge_port=2 tagging=tagged").unwrap(),
            &inventory
        )
        .is_err());
        assert!(validate_references(
            &command::parse("create acl_entry table=1 priority=1 action=deny src=192.0.2.0/24")
                .unwrap(),
            &inventory
        )
        .is_err());
        assert_eq!(
            validate_references(
                &command::parse("create next_hop router_interface=2 ip=::1").unwrap(),
                &inventory
            )
            .unwrap()
            .len(),
            1
        );
    }
}
