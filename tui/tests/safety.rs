//! Failure injection at the shared executor boundary (no lab required).
use sai_tui::{
    client::{execute, Failure, Service},
    command::{approve, parse},
    sai_tui::{Inventory, Object},
};
use std::collections::BTreeMap;

fn failure(category: &str, status: Option<i32>) -> Failure {
    Failure {
        category: category.into(),
        status,
        message: "injected failure".into(),
    }
}
struct Mock {
    calls: Vec<String>,
    kind: String,
    key: String,
    mutation_error: bool,
    getter_error: Option<Failure>,
    snapshot_error_at: Option<usize>,
    snapshot_count: usize,
    wrong_key: bool,
    mismatch: bool,
}
impl Mock {
    fn new(kind: &str, key: &str) -> Self {
        Self {
            calls: vec![],
            kind: kind.into(),
            key: key.into(),
            mutation_error: false,
            getter_error: None,
            snapshot_error_at: None,
            snapshot_count: 0,
            wrong_key: false,
            mismatch: false,
        }
    }
    fn object(&self, observed: bool) -> Object {
        Object::new(
            self.kind.clone(),
            if self.wrong_key && observed {
                "0x999".into()
            } else {
                self.key.clone()
            },
            BTreeMap::from([
                (
                    "admin".into(),
                    if observed && self.mismatch {
                        "false".into()
                    } else {
                        "true".into()
                    },
                ),
                ("vlan_id".into(), "100".into()),
                (
                    "source".into(),
                    if observed {
                        "actual getter".into()
                    } else {
                        "mutation reply".into()
                    },
                ),
            ]),
        )
    }
}
impl Service for Mock {
    fn snapshot(&mut self) -> Result<Inventory, Failure> {
        self.calls.push("snapshot".into());
        self.snapshot_count += 1;
        if self.snapshot_error_at == Some(self.snapshot_count) {
            Err(failure("transport/protocol", None))
        } else {
            Ok(Inventory::new(vec![], vec!["limited".into()]))
        }
    }
    fn get(&mut self, kind: &str, key: &str) -> Result<Object, Failure> {
        self.calls.push(format!("get {kind} {key}"));
        if let Some(e) = &self.getter_error {
            Err(e.clone())
        } else {
            Ok(self.object(true))
        }
    }
    fn create(&mut self, _: &str, _: &BTreeMap<String, String>) -> Result<Object, Failure> {
        self.calls.push("create".into());
        if self.mutation_error {
            Err(failure("transport/protocol", None))
        } else {
            Ok(self.object(false))
        }
    }
    fn set(&mut self, _: &str, _: &str, _: &BTreeMap<String, String>) -> Result<Object, Failure> {
        self.calls.push("set".into());
        if self.mutation_error {
            Err(failure("transport/protocol", None))
        } else {
            Ok(self.object(false))
        }
    }
    fn remove(&mut self, _: &str, _: &str) -> Result<(), Failure> {
        self.calls.push("remove".into());
        Ok(())
    }
    fn counters(&mut self, _: &str) -> Result<BTreeMap<String, u64>, Failure> {
        unreachable!()
    }
}
#[test]
fn success_shows_actual_getter_not_the_requested_attributes() {
    let mut mock = Mock::new("port", "0x1");
    let cmd = parse("set port 1 admin=true").unwrap();
    let result = execute(&mut mock, &cmd, approve(&cmd, true).unwrap());
    assert!(result.ok);
    assert_eq!(
        result.value["mutation"]["value"]["attributes"]["admin"],
        "true"
    );
    assert_eq!(
        result.value["readback"]["value"]["attributes"]["source"],
        "actual getter"
    );
    assert_eq!(mock.calls, ["snapshot", "set", "get port 0x1", "snapshot"]);
}
#[test]
fn mismatched_requested_value_is_visible_partial_effect_failure() {
    let mut mock = Mock::new("port", "0x1");
    mock.mismatch = true;
    let cmd = parse("set port 1 admin=true").unwrap();
    let result = execute(&mut mock, &cmd, approve(&cmd, true).unwrap());
    assert!(!result.ok);
    assert_eq!(result.value["attribute_mismatches"][0]["field"], "admin");
    assert_eq!(result.value["attribute_mismatches"][0]["observed"], "false");
    assert_eq!(mock.calls, ["snapshot", "set", "get port 0x1", "snapshot"]);
}
#[test]
fn create_readback_and_failed_composite_create_readback() {
    let mut mock = Mock::new("vlan", "0x2");
    let cmd = parse("create vlan vlan_id=100").unwrap();
    assert!(execute(&mut mock, &cmd, approve(&cmd, true).unwrap()).ok);
    assert_eq!(
        mock.calls,
        ["snapshot", "create", "get vlan 0x2", "snapshot"]
    );
    let mut mock = Mock::new("neighbor", "0x1@2001:db8::1");
    mock.mutation_error = true;
    let cmd =
        parse("create neighbor router_interface=1 ip=2001:db8::1 mac=00:11:22:33:44:55").unwrap();
    let result = execute(&mut mock, &cmd, approve(&cmd, true).unwrap());
    assert!(!result.ok);
    assert_eq!(
        mock.calls,
        [
            "snapshot",
            "create",
            "get neighbor 0x1@2001:db8::1",
            "snapshot"
        ]
    );
}
#[test]
fn lost_oid_create_reply_cannot_be_retried_or_fabricated() {
    let mut mock = Mock::new("vlan", "0x2");
    mock.mutation_error = true;
    let cmd = parse("create vlan vlan_id=100").unwrap();
    let result = execute(&mut mock, &cmd, approve(&cmd, true).unwrap());
    assert!(!result.ok);
    assert!(result.value["readback"].is_null());
    assert!(result.value["readback_unavailable_reason"].is_string());
    assert_eq!(mock.calls, ["snapshot", "create", "snapshot"]);
}
#[test]
fn failed_post_snapshot_still_reports_partial_effect_nonzero() {
    let mut mock = Mock::new("port", "0x1");
    mock.snapshot_error_at = Some(2);
    let cmd = parse("set port 1 admin=true").unwrap();
    let result = execute(&mut mock, &cmd, approve(&cmd, true).unwrap());
    assert!(!result.ok);
    assert_eq!(result.value["readback"]["ok"], true);
    assert_eq!(result.value["snapshot"]["ok"], false);
    assert_eq!(mock.calls, ["snapshot", "set", "get port 0x1", "snapshot"]);
}
#[test]
fn arbitrary_getter_error_or_existing_object_is_not_removal_verification() {
    for error in [
        None,
        Some(failure("transport/protocol", None)),
        Some(failure("server", Some(-2))),
    ] {
        let mut mock = Mock::new("vlan", "0x2");
        mock.getter_error = error;
        let cmd = parse("remove vlan 2").unwrap();
        let result = execute(&mut mock, &cmd, approve(&cmd, true).unwrap());
        assert!(!result.ok);
        assert_eq!(result.value["removal_verified_absent"], false);
    }
}
#[test]
fn preflight_failure_and_absent_confirmation_send_no_mutation() {
    let mut mock = Mock::new("port", "0x1");
    let cmd = parse("set port 1 admin=true").unwrap();
    assert!(!execute(&mut mock, &cmd, None).ok);
    assert!(mock.calls.is_empty());
    mock.snapshot_error_at = Some(1);
    assert!(!execute(&mut mock, &cmd, approve(&cmd, true).unwrap()).ok);
    assert_eq!(mock.calls, ["snapshot"]);
}
#[test]
fn mismatched_getter_object_is_not_successful_readback() {
    let mut mock = Mock::new("port", "0x1");
    mock.wrong_key = true;
    let cmd = parse("set port 1 admin=true").unwrap();
    let result = execute(&mut mock, &cmd, approve(&cmd, true).unwrap());
    assert!(!result.ok);
    assert_eq!(result.value["readback"]["error"]["category"], "protocol");
}
