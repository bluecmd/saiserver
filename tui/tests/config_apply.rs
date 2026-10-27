//! Offline staged-plan tests: the only service is an in-memory failure-injecting mock.
use sai_tui::{
    apply::{apply, ApplyStatus},
    client::{Failure, Service},
    config::{
        self, AttributeValue as V, Attributes, LoadResult, ObjectRef, Operation, Plan,
        PortIdentity, Staging, Target,
    },
    sai_tui::{Inventory, Object},
};
use std::{
    collections::BTreeMap,
    sync::{
        atomic::{AtomicBool, Ordering},
        Arc,
    },
};

fn literal(s: &str) -> V {
    V::Literal(s.into())
}
fn existing(kind: &str, oid: &str) -> ObjectRef {
    ObjectRef::Existing {
        kind: kind.into(),
        oid: oid.into(),
    }
}
fn symbol(kind: &str, name: &str) -> ObjectRef {
    ObjectRef::Created {
        kind: kind.into(),
        symbol: name.into(),
    }
}
fn attrs(values: &[(&str, V)]) -> Attributes {
    values
        .iter()
        .map(|(k, v)| (k.to_string(), v.clone()))
        .collect()
}
fn create(kind: &str, name: &str, values: &[(&str, V)]) -> Operation {
    Operation::Create {
        kind: kind.into(),
        bind: Some(name.into()),
        attrs: attrs(values),
    }
}
fn set(reference: ObjectRef, values: &[(&str, V)]) -> Operation {
    Operation::Set {
        target: Target::Object(reference),
        attrs: attrs(values),
    }
}
fn plan(operations: Vec<Operation>) -> Plan {
    Plan {
        id: "test-plan".into(),
        title: "Offline test plan".into(),
        operations,
        ports: vec![],
    }
}
fn vlan() -> Operation {
    create("vlan", "vlan", &[("vlan_id", literal("100"))])
}
fn inventory() -> Inventory {
    Inventory::new(
        vec![Object::new(
            "port".to_owned(),
            "0x1".to_owned(),
            BTreeMap::from([
                ("lanes".into(), "12,13,14,15".into()),
                ("speed".into(), "100000".into()),
                ("admin".into(), "false".into()),
            ]),
        )],
        vec![],
    )
}
fn failure(category: &str, status: Option<i32>) -> Failure {
    Failure {
        category: category.into(),
        status,
        message: "injected".into(),
    }
}
struct Mock {
    inventory: Inventory,
    calls: Vec<String>,
    mutations: usize,
    snapshots: usize,
    fail_mutation: Option<usize>,
    fail_get: Option<usize>,
    fail_snapshot: Option<usize>,
    mismatch: Option<usize>,
    wrong_reply_kind: bool,
    wrong_get_key: bool,
    malformed_reply_key: bool,
    fixed_oid: Option<String>,
    snapshot_only_ports: bool,
    change_kind_at: Option<usize>,
    change_speed_at: Option<usize>,
    cancel: Arc<AtomicBool>,
    cancel_mutation: Option<usize>,
    cancel_snapshot: Option<usize>,
}
impl Mock {
    fn new() -> Self {
        Self {
            inventory: inventory(),
            calls: vec![],
            mutations: 0,
            snapshots: 0,
            fail_mutation: None,
            fail_get: None,
            fail_snapshot: None,
            mismatch: None,
            wrong_reply_kind: false,
            wrong_get_key: false,
            malformed_reply_key: false,
            fixed_oid: None,
            snapshot_only_ports: false,
            change_kind_at: None,
            change_speed_at: None,
            cancel: Arc::new(AtomicBool::new(false)),
            cancel_mutation: None,
            cancel_snapshot: None,
        }
    }
    fn mutated(&mut self) -> Result<(), Failure> {
        self.mutations += 1;
        if self.cancel_mutation == Some(self.mutations) {
            self.cancel.store(true, Ordering::Release);
        }
        if self.fail_mutation == Some(self.mutations) {
            Err(failure("transport/protocol", None))
        } else {
            Ok(())
        }
    }
}
impl Service for Mock {
    fn snapshot(&mut self) -> Result<Inventory, Failure> {
        self.calls.push("snapshot".into());
        self.snapshots += 1;
        if self.cancel_snapshot == Some(self.snapshots) {
            self.cancel.store(true, Ordering::Release);
        }
        if self.change_kind_at == Some(self.snapshots) {
            for object in self.inventory.objects.as_mut().unwrap() {
                if object.kind.as_deref() == Some("acl_table") {
                    object.kind = Some("acl_group".into());
                }
            }
        }
        if self.change_speed_at == Some(self.snapshots) {
            self.inventory.objects.as_mut().unwrap()[0]
                .attributes
                .as_mut()
                .unwrap()
                .insert("speed".into(), "42".into());
        }
        if self.fail_snapshot == Some(self.snapshots) {
            Err(failure("transport/protocol", None))
        } else {
            let mut snapshot = self.inventory.clone();
            if self.snapshot_only_ports {
                snapshot
                    .objects
                    .as_mut()
                    .unwrap()
                    .retain(|o| o.kind.as_deref() == Some("port"));
            }
            Ok(snapshot)
        }
    }
    fn get(&mut self, kind: &str, key: &str) -> Result<Object, Failure> {
        self.calls.push(format!("get {kind} {key}"));
        if self.fail_get == Some(self.mutations) {
            return Err(failure("transport/protocol", None));
        }
        let mut object = self
            .inventory
            .objects
            .as_ref()
            .unwrap()
            .iter()
            .find(|o| o.kind.as_deref() == Some(kind) && o.key.as_deref() == Some(key))
            .cloned()
            .ok_or_else(|| failure("server", Some(-7)))?;
        if self.mismatch == Some(self.mutations) {
            object.attributes.as_mut().unwrap().clear();
        }
        if self.wrong_get_key {
            object.key = Some("0x9999".into());
        }
        Ok(object)
    }
    fn create(&mut self, kind: &str, attrs: &BTreeMap<String, String>) -> Result<Object, Failure> {
        self.calls.push(format!("create {kind}"));
        let key = self
            .fixed_oid
            .clone()
            .unwrap_or_else(|| format!("0x{:x}", 0x100 + self.mutations));
        let mut object = Object::new(kind.to_owned(), key, attrs.clone());
        self.inventory
            .objects
            .as_mut()
            .unwrap()
            .push(object.clone());
        self.mutated()?;
        if self.wrong_reply_kind {
            object.kind = Some("port".into());
        }
        if self.malformed_reply_key {
            object.key = Some("not-an-oid".into());
        }
        Ok(object)
    }
    fn set(
        &mut self,
        kind: &str,
        key: &str,
        attrs: &BTreeMap<String, String>,
    ) -> Result<Object, Failure> {
        self.calls.push(format!("set {kind} {key}"));
        let object = self
            .inventory
            .objects
            .as_mut()
            .unwrap()
            .iter_mut()
            .find(|o| o.kind.as_deref() == Some(kind) && o.key.as_deref() == Some(key))
            .unwrap();
        object.attributes.as_mut().unwrap().extend(attrs.clone());
        let object = object.clone();
        self.mutated()?;
        Ok(object)
    }
    fn remove(&mut self, kind: &str, key: &str) -> Result<(), Failure> {
        self.calls.push(format!("remove {kind} {key}"));
        self.inventory
            .objects
            .as_mut()
            .unwrap()
            .retain(|o| !(o.kind.as_deref() == Some(kind) && o.key.as_deref() == Some(key)));
        self.mutated()
    }
    fn counters(&mut self, _: &str) -> Result<BTreeMap<String, u64>, Failure> {
        panic!("unexpected counter RPC")
    }
}
fn staged(plan: Plan, mock: &Mock) -> Staging {
    let mut stage = Staging::default();
    stage.load(plan, &mock.inventory, true).unwrap();
    stage
}
fn sequence() -> Plan {
    plan(vec![
        vlan(),
        create(
            "bridge_port",
            "bridge",
            &[("port", V::Reference(existing("port", "1")))],
        ),
        create(
            "vlan_member",
            "member",
            &[
                ("vlan", V::Reference(symbol("vlan", "vlan"))),
                ("bridge_port", V::Reference(symbol("bridge_port", "bridge"))),
                ("tagging", literal("untagged")),
            ],
        ),
        set(existing("port", "1"), &[("pvid", literal("100"))]),
        Operation::Remove {
            target: Target::Object(symbol("vlan_member", "member")),
        },
    ])
}

#[test]
fn loading_replacement_cancel_and_invalid_preserve_state_with_zero_rpcs() {
    let mut mock = Mock::new();
    let mut stage = staged(plan(vec![vlan()]), &mock);
    let old = stage.plan().unwrap().clone();
    let approval = stage.approve(true).unwrap();
    assert_eq!(
        stage.load(sequence(), &mock.inventory, false).unwrap(),
        LoadResult::Cancelled
    );
    let mut invalid = sequence();
    invalid
        .operations
        .push(set(existing("port", "1"), &[("admin", literal("yes"))]));
    assert!(stage.load(invalid, &mock.inventory, true).is_err());
    assert_eq!(stage.plan(), Some(&old));
    assert!(mock.calls.is_empty());
    // Failed/cancelled replacement also preserves the prior approval.
    let cancel = mock.cancel.clone();
    assert_eq!(
        apply(&mut stage, Some(approval), &mut mock, &cancel).status,
        ApplyStatus::Completed
    );
}

#[test]
fn approval_is_separate_single_use_revision_and_instance_bound() {
    let mut mock = Mock::new();
    let cancel = mock.cancel.clone();
    let mut stage = staged(plan(vec![vlan()]), &mock);
    assert!(stage.approve(false).is_err());
    assert!(matches!(
        apply(&mut stage, None, &mut mock, &cancel).status,
        ApplyStatus::Rejected(_)
    ));
    let stale = stage.approve(true).unwrap();
    stage
        .load(plan(vec![vlan()]), &mock.inventory, true)
        .unwrap();
    assert!(matches!(
        apply(&mut stage, Some(stale), &mut mock, &cancel).status,
        ApplyStatus::Rejected(_)
    ));
    let foreign = stage.approve(true).unwrap();
    let mut other = staged(plan(vec![vlan()]), &mock);
    assert!(matches!(
        apply(&mut other, Some(foreign), &mut mock, &cancel).status,
        ApplyStatus::Rejected(_)
    ));
    let superseded = stage.approve(true).unwrap();
    let latest = stage.approve(true).unwrap();
    assert!(matches!(
        apply(&mut stage, Some(superseded), &mut mock, &cancel).status,
        ApplyStatus::Rejected(_)
    ));
    assert!(mock.calls.is_empty());
    assert_eq!(
        apply(&mut stage, Some(latest), &mut mock, &cancel).status,
        ApplyStatus::Completed
    );
    let calls = mock.calls.len();
    assert!(matches!(
        apply(&mut stage, None, &mut mock, &cancel).status,
        ApplyStatus::Rejected(_)
    ));
    assert_eq!(mock.calls.len(), calls);
}

#[test]
fn successful_dependency_sequence_uses_returned_oids_and_audits_every_step() {
    let mut mock = Mock::new();
    let cancel = mock.cancel.clone();
    let mut stage = staged(sequence(), &mock);
    assert_eq!(
        stage.plan().unwrap().ports,
        vec![PortIdentity::capture(&mock.inventory, "1").unwrap()]
    );
    let approval = stage.approve(true).unwrap();
    let report = apply(&mut stage, Some(approval), &mut mock, &cancel);
    assert_eq!(report.status, ApplyStatus::Completed);
    assert!(!report.partial_effects);
    assert_eq!(report.completed_steps(), 5);
    assert_eq!(report.bindings["vlan"].key, "0x100");
    assert_eq!(report.bindings["bridge"].key, "0x101");
    assert_eq!(
        report.steps[2].outcome.value["readback"]["value"]["attributes"]["vlan"],
        "0x100"
    );
    assert_eq!(
        report.steps[2].outcome.value["readback"]["value"]["attributes"]["bridge_port"],
        "0x101"
    );
    assert!(report.steps.iter().all(|s| s.verified && s.mutation_sent));
    assert_eq!(
        mock.calls,
        [
            "snapshot",
            "snapshot",
            "create vlan",
            "get vlan 0x100",
            "snapshot",
            "snapshot",
            "create bridge_port",
            "get bridge_port 0x101",
            "snapshot",
            "snapshot",
            "create vlan_member",
            "get vlan_member 0x102",
            "snapshot",
            "snapshot",
            "set port 0x1",
            "get port 0x1",
            "snapshot",
            "snapshot",
            "remove vlan_member 0x102",
            "get vlan_member 0x102",
            "snapshot"
        ]
    );
}

#[test]
fn whole_plan_rejects_invalid_final_steps_types_injection_and_bounds_locally() {
    let mock = Mock::new();
    let invalid_ops = vec![
        set(
            existing("port", "1"),
            &[("admin", literal("true set port 1 admin=false"))],
        ),
        set(
            existing("port", "1"),
            &[("admin", V::Reference(existing("port", "1")))],
        ),
        set(existing("port", "1"), &[("speed", literal("25000"))]),
        create(
            "vlan_member",
            "m",
            &[
                ("vlan", literal("1")),
                ("bridge_port", literal("2")),
                ("tagging", literal("tagged")),
            ],
        ),
        create(
            "vlan_member",
            "m",
            &[
                ("vlan", V::Reference(existing("port", "1"))),
                ("bridge_port", V::Reference(existing("bridge_port", "2"))),
                ("tagging", literal("tagged")),
            ],
        ),
        create(
            "vlan_member",
            "m",
            &[
                ("vlan", V::Reference(existing("vlan", "1"))),
                ("bridge_port", V::Reference(existing("bridge_port", "2"))),
                ("tagging", literal("tagged")),
            ],
        ),
        create("vlan", "v", &[("vlan_id", literal("4095"))]),
        create("vlan", "v", &[]),
        create("vlan set port 1", "v", &[("vlan_id", literal("100"))]),
        set(existing("vlan", "1"), &[("vlan_id", literal("100"))]),
        set(existing("port", "0"), &[("admin", literal("true"))]),
        set(
            existing("port", "1"),
            &[(
                "ingress_acl",
                V::Reference(existing("acl_table", "1 admin=false")),
            )],
        ),
        create("bridge_port", "bp", &[("port", V::NullOid)]),
    ];
    let mut stage = Staging::default();
    for invalid in invalid_ops {
        assert!(stage
            .load(plan(vec![vlan(), invalid]), &mock.inventory, true)
            .is_err());
    }
    assert!(stage
        .load(
            plan(vec![vlan(); config::MAX_OPERATIONS + 1]),
            &mock.inventory,
            true
        )
        .is_err());
    assert!(stage.load(plan(vec![]), &mock.inventory, true).is_err());
    assert!(stage.plan().is_none());
    assert!(mock.calls.is_empty());
}

#[test]
fn forward_unknown_duplicate_wrong_kind_cycles_and_removed_symbols_are_rejected() {
    let mock = Mock::new();
    let set_symbol = |kind, name| set(symbol(kind, name), &[("admin", literal("true"))]);
    for operations in [
        vec![
            set_symbol("bridge_port", "later"),
            create(
                "bridge_port",
                "later",
                &[("port", V::Reference(existing("port", "1")))],
            ),
        ],
        vec![set_symbol("bridge_port", "missing")],
        vec![vlan(), vlan()],
        vec![vlan(), set_symbol("bridge_port", "vlan")],
        vec![
            create(
                "bridge_port",
                "a",
                &[("port", V::Reference(symbol("port", "b")))],
            ),
            create(
                "port",
                "b",
                &[("ingress_acl", V::Reference(symbol("acl_table", "a")))],
            ),
        ],
        vec![
            vlan(),
            Operation::Remove {
                target: Target::Object(symbol("vlan", "vlan")),
            },
            Operation::Remove {
                target: Target::Object(symbol("vlan", "vlan")),
            },
        ],
    ] {
        assert!(config::validate(&plan(operations), &mock.inventory).is_err());
    }
    assert!(mock.calls.is_empty());
}

#[test]
fn symbolic_placeholder_inventory_checks_acl_family_before_any_rpc() {
    let mock = Mock::new();
    let p = plan(vec![
        create(
            "acl_table",
            "table",
            &[("stage", literal("ingress")), ("family", literal("ipv6"))],
        ),
        create(
            "acl_entry",
            "entry",
            &[
                ("table", V::Reference(symbol("acl_table", "table"))),
                ("priority", literal("1")),
                ("action", literal("deny")),
                ("src", literal("192.0.2.0/24")),
            ],
        ),
    ]);
    // The precise validator error identifies the IPv6 table; no Service was touched.
    assert!(config::validate(&p, &mock.inventory)
        .unwrap_err()
        .contains("ipv6"));
    assert!(mock.calls.is_empty());
}

#[test]
fn fresh_whole_plan_preflight_rejects_late_incompatibility_before_first_mutation() {
    let mut mock = Mock::new();
    let cancel = mock.cancel.clone();
    let p = plan(vec![
        vlan(),
        create(
            "next_hop",
            "nh",
            &[
                (
                    "router_interface",
                    V::Reference(existing("router_interface", "0x50")),
                ),
                ("ip", literal("192.0.2.1")),
            ],
        ),
    ]);
    let mut stage = staged(p, &mock);
    let approval = stage.approve(true).unwrap();
    mock.inventory.objects.as_mut().unwrap().push(Object::new(
        "vlan".to_owned(),
        "0x50".to_owned(),
        BTreeMap::new(),
    ));
    let report = apply(&mut stage, Some(approval), &mut mock, &cancel);
    assert!(matches!(report.status, ApplyStatus::Rejected(_)));
    assert_eq!(mock.calls, ["snapshot"]);
    assert_eq!(mock.mutations, 0);
}

#[test]
fn selected_ports_are_pinned_to_lanes_speed_and_presence_not_display_order() {
    for change in ["lanes", "speed", "missing"] {
        let mut mock = Mock::new();
        let cancel = mock.cancel.clone();
        let mut stage = staged(sequence(), &mock);
        let approval = stage.approve(true).unwrap();
        if change == "missing" {
            mock.inventory.objects.as_mut().unwrap().clear();
        } else {
            mock.inventory.objects.as_mut().unwrap()[0]
                .attributes
                .as_mut()
                .unwrap()
                .insert(change.into(), "42".into());
        }
        let report = apply(&mut stage, Some(approval), &mut mock, &cancel);
        assert!(matches!(report.status, ApplyStatus::Rejected(_)));
        assert_eq!(mock.mutations, 0);
    }
}

#[test]
fn stop_after_first_failure_or_uncertainty_with_no_retry_or_rollback() {
    for mode in [
        "mutation",
        "getter",
        "snapshot",
        "mismatch",
        "wrong getter",
        "wrong reply",
        "bad key",
    ] {
        let mut mock = Mock::new();
        let cancel = mock.cancel.clone();
        match mode {
            "mutation" => mock.fail_mutation = Some(2),
            "getter" => mock.fail_get = Some(2),
            "snapshot" => mock.fail_snapshot = Some(5),
            "mismatch" => mock.mismatch = Some(2),
            "wrong getter" => mock.wrong_get_key = true,
            "wrong reply" => mock.wrong_reply_kind = true,
            "bad key" => mock.malformed_reply_key = true,
            _ => unreachable!(),
        }
        let mut stage = staged(sequence(), &mock);
        let approval = stage.approve(true).unwrap();
        let report = apply(&mut stage, Some(approval), &mut mock, &cancel);
        assert!(
            matches!(report.status, ApplyStatus::Failed { .. }),
            "{mode}: {:?}",
            report.status
        );
        assert!(report.partial_effects);
        assert!(mock.mutations <= 2);
        assert_eq!(report.steps.len(), mock.mutations);
        assert_eq!(report.completed_steps(), mock.mutations - 1);
        assert!(!mock.calls.iter().any(|c| c.starts_with("remove")));
        assert!(!report.bindings.contains_key("bridge"));
        assert_eq!(mock.calls.last().unwrap(), "snapshot");
    }
}

#[test]
fn cancellation_before_apply_between_steps_and_during_preflight_stops_remainder() {
    for when in ["before", "after first", "preflight"] {
        let mut mock = Mock::new();
        let cancel = mock.cancel.clone();
        match when {
            "before" => cancel.store(true, Ordering::Release),
            "after first" => mock.cancel_mutation = Some(1),
            "preflight" => mock.cancel_snapshot = Some(2),
            _ => unreachable!(),
        }
        let mut stage = staged(sequence(), &mock);
        let approval = stage.approve(true).unwrap();
        let report = apply(&mut stage, Some(approval), &mut mock, &cancel);
        assert_eq!(report.status, ApplyStatus::Cancelled);
        assert_eq!(mock.mutations, usize::from(when == "after first"));
        assert_eq!(report.partial_effects, when == "after first");
        if when == "after first" {
            assert_eq!(report.completed_steps(), 1);
            assert_eq!(mock.calls.last().unwrap(), "snapshot");
        }
        if when == "before" {
            assert!(mock.calls.is_empty());
        }
        cancel.store(false, Ordering::Release);
        let calls = mock.calls.len();
        assert!(matches!(
            apply(&mut stage, None, &mut mock, &cancel).status,
            ApplyStatus::Rejected(_)
        ));
        assert_eq!(calls, mock.calls.len());
    }
}

#[test]
fn unknown_inventory_does_not_allow_conflicting_declared_reference_types() {
    let mock = Mock::new();
    let p = plan(vec![
        create(
            "next_hop",
            "nh",
            &[
                (
                    "router_interface",
                    V::Reference(existing("router_interface", "80")),
                ),
                ("ip", literal("::1")),
            ],
        ),
        create(
            "router_interface",
            "rif",
            &[
                (
                    "virtual_router",
                    V::Reference(existing("virtual_router", "0x50")),
                ),
                ("port", V::Reference(existing("port", "1"))),
            ],
        ),
    ]);
    assert!(config::validate(&p, &mock.inventory)
        .unwrap_err()
        .contains("conflicting"));
    assert!(mock.calls.is_empty());
}

#[test]
fn repeated_or_preexisting_returned_create_ids_are_ambiguous_even_with_limited_discovery() {
    for reuse in ["known", "prior create", "explicit reference"] {
        let mut mock = Mock::new();
        let cancel = mock.cancel.clone();
        mock.fixed_oid = Some(if reuse == "known" { "0x1" } else { "0x100" }.into());
        mock.snapshot_only_ports = true;
        let p = if reuse == "explicit reference" {
            plan(vec![
                vlan(),
                Operation::Remove {
                    target: Target::Object(existing("vlan", "0x100")),
                },
            ])
        } else {
            sequence()
        };
        let mut stage = staged(p, &mock);
        let approval = stage.approve(true).unwrap();
        let report = apply(&mut stage, Some(approval), &mut mock, &cancel);
        assert!(matches!(report.status, ApplyStatus::Failed { .. }));
        assert!(report.partial_effects);
        assert_eq!(mock.mutations, if reuse == "prior create" { 2 } else { 1 });
        assert!(!report.bindings.contains_key("bridge"));
    }
}

#[test]
fn per_step_preflight_checks_exact_declared_types_and_port_identity_again() {
    let mut mock = Mock::new();
    let cancel = mock.cancel.clone();
    mock.inventory.objects.as_mut().unwrap().push(Object::new(
        "acl_table".to_owned(),
        "0x50".to_owned(),
        BTreeMap::new(),
    ));
    let mut stage = staged(
        plan(vec![set(
            existing("port", "1"),
            &[("ingress_acl", V::Reference(existing("acl_table", "0x50")))],
        )]),
        &mock,
    );
    // Both kinds are allowed by ingress_acl, but only acl_table was approved.
    mock.change_kind_at = Some(2);
    let approval = stage.approve(true).unwrap();
    let report = apply(&mut stage, Some(approval), &mut mock, &cancel);
    assert!(matches!(report.status, ApplyStatus::Failed { .. }));
    assert_eq!(mock.mutations, 0);
    assert!(!report.partial_effects);

    let mut mock = Mock::new();
    let cancel = mock.cancel.clone();
    let mut stage = staged(sequence(), &mock);
    mock.change_speed_at = Some(4);
    let approval = stage.approve(true).unwrap();
    let report = apply(&mut stage, Some(approval), &mut mock, &cancel);
    assert!(matches!(report.status, ApplyStatus::Failed { step: 1, .. }));
    assert_eq!(mock.mutations, 1);
    assert!(report.partial_effects);
    assert_eq!(report.completed_steps(), 1);
    assert!(!report.steps[1].mutation_sent);
}

#[test]
fn preflight_failure_and_lost_first_create_reply_never_dispatch_dependencies() {
    for mode in ["plan preflight", "command preflight", "lost create"] {
        let mut mock = Mock::new();
        let cancel = mock.cancel.clone();
        let mut stage = staged(sequence(), &mock);
        let approval = stage.approve(true).unwrap();
        match mode {
            "plan preflight" => mock.fail_snapshot = Some(1),
            "command preflight" => mock.fail_snapshot = Some(2),
            _ => mock.fail_mutation = Some(1),
        }
        let report = apply(&mut stage, Some(approval), &mut mock, &cancel);
        assert_ne!(report.status, ApplyStatus::Completed);
        assert_eq!(mock.mutations, usize::from(mode == "lost create"));
        assert_eq!(report.partial_effects, mode == "lost create");
        assert!(report.bindings.is_empty());
        assert!(!mock.calls.iter().any(|c| c == "create bridge_port"));
        if mode == "lost create" {
            assert!(report.steps[0].outcome.value["readback"].is_null());
            assert_eq!(
                mock.calls,
                ["snapshot", "snapshot", "create vlan", "snapshot"]
            );
        }
    }
}

#[test]
fn composite_entries_are_explicit_schema_checked_and_never_bound_to_fabricated_oids() {
    let mut mock = Mock::new();
    let cancel = mock.cancel.clone();
    let mut create = create(
        "neighbor",
        "n",
        &[
            (
                "router_interface",
                V::Reference(existing("router_interface", "3")),
            ),
            ("ip", literal("192.0.2.1")),
            ("mac", literal("00:11:22:33:44:55")),
        ],
    );
    assert!(config::validate(&plan(vec![create.clone()]), &mock.inventory).is_err());
    if let Operation::Create { bind, .. } = &mut create {
        *bind = None;
    }
    let p = plan(vec![
        create,
        Operation::Remove {
            target: Target::Entry {
                kind: "neighbor".into(),
                key: "3@192.0.2.1".into(),
            },
        },
    ]);
    mock.fixed_oid = Some("0x3@192.0.2.1".into());
    let mut stage = staged(p, &mock);
    let approval = stage.approve(true).unwrap();
    let report = apply(&mut stage, Some(approval), &mut mock, &cancel);
    assert_eq!(report.status, ApplyStatus::Completed);
    assert_eq!(report.completed_steps(), 2);
    assert!(report.bindings.is_empty());
    for key in ["3", "3@192.0.2.1 remove vlan 4"] {
        assert!(config::validate(
            &plan(vec![Operation::Remove {
                target: Target::Entry {
                    kind: "neighbor".into(),
                    key: key.into()
                }
            }]),
            &mock.inventory
        )
        .is_err());
    }
}

#[test]
fn null_binding_detach_and_generic_schema_kinds_need_no_platform_logic() {
    let mut mock = Mock::new();
    let cancel = mock.cancel.clone();
    let p = plan(vec![
        create(
            "acl_table",
            "acl",
            &[("stage", literal("ingress")), ("family", literal("ipv4"))],
        ),
        set(
            existing("port", "1"),
            &[("ingress_acl", V::Reference(symbol("acl_table", "acl")))],
        ),
        set(existing("port", "1"), &[("ingress_acl", V::NullOid)]),
    ]);
    let mut stage = staged(p, &mock);
    let approval = stage.approve(true).unwrap();
    assert_eq!(
        apply(&mut stage, Some(approval), &mut mock, &cancel).status,
        ApplyStatus::Completed
    );
}
