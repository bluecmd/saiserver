//! Compile validated preset intent into dependency-ordered, explicitly reviewed operations.
use crate::{
    command,
    config::{
        self, AttributeValue as V, Attributes, ObjectRef as R, Operation as Op, Plan, PortIdentity,
        Target,
    },
    presets::{self, BoundPreset, Deny, Interface},
    sai_tui::{Inventory, Object},
};
use std::collections::BTreeMap;

fn literal(value: impl ToString) -> V {
    V::Literal(value.to_string())
}
fn reference(kind: &str, oid: &str) -> R {
    R::Existing {
        kind: kind.into(),
        oid: oid.into(),
    }
}
fn attributes(values: Vec<(&str, V)>) -> Attributes {
    values.into_iter().map(|(k, v)| (k.into(), v)).collect()
}
fn create(ops: &mut Vec<Op>, kind: &str, symbol: &str, values: Vec<(&str, V)>) -> R {
    ops.push(Op::Create {
        kind: kind.into(),
        bind: Some(symbol.into()),
        attrs: attributes(values),
    });
    R::Created {
        kind: kind.into(),
        symbol: symbol.into(),
    }
}
fn entry(ops: &mut Vec<Op>, kind: &str, values: Vec<(&str, V)>) {
    ops.push(Op::Create {
        kind: kind.into(),
        bind: None,
        attrs: attributes(values),
    });
}
fn attr<'a>(object: &'a Object, name: &str) -> Result<&'a str, String> {
    object
        .attributes
        .as_ref()
        .and_then(|a| a.get(name))
        .map(String::as_str)
        .ok_or_else(|| {
            format!(
                "{}.{} getter unavailable",
                object.kind.as_deref().unwrap_or("object"),
                name
            )
        })
}
fn key(object: &Object) -> Result<&str, String> {
    object
        .key
        .as_deref()
        .ok_or_else(|| "object key missing".into())
}

pub fn build(bound: &BoundPreset, inventory: &Inventory) -> Result<Plan, String> {
    let rebound = presets::bind(bound.preset.clone(), inventory)?;
    if rebound.port_oids != bound.port_oids {
        return Err("port identities changed since preset selection".into());
    }
    let objects = inventory.objects.as_deref().unwrap_or_default();
    let switches: Vec<_> = objects
        .iter()
        .filter(|o| o.kind.as_deref() == Some("switch"))
        .collect();
    if switches.len() != 1 {
        return Err("exactly one observed switch is required".into());
    }
    let switch = switches[0];
    if attr(switch, "preset_api")? != "1" || attr(switch, "interface_address_backend")? != "enabled"
    {
        return Err(
            "server lacks preset API or operational ARP/NDP backend is not explicitly enabled"
                .into(),
        );
    }
    let mac = command::value(command::Value::Mac, attr(switch, "src_mac")?)?;
    let first = u8::from_str_radix(&mac[..2], 16).map_err(|_| "invalid source MAC")?;
    if first & 1 != 0 || mac == "00:00:00:00:00:00" {
        return Err("switch source MAC is not unicast".into());
    }
    let default_vlan = command::oid(attr(switch, "default_vlan")?, false)?;
    let mut bridge_ports = BTreeMap::new();
    for object in objects {
        match object.kind.as_deref() {
            Some("vlan")
                if attr(object, "vlan_id")
                    .ok()
                    .and_then(|v| v.parse::<u16>().ok())
                    .is_some_and(|v| (101..=132).contains(&v)) =>
            {
                return Err(
                    "preset VLAN already exists; implicit overwrite/reapply is not supported"
                        .into(),
                );
            }
            Some("bridge_port") => {
                if let Ok(port) = attr(object, "port") {
                    let port = command::oid(port, false)?;
                    if bound.port_oids.values().any(|p| p == &port)
                        && bridge_ports.insert(port, key(object)?.to_owned()).is_some()
                    {
                        return Err("multiple bridge ports on one preset port".into());
                    }
                }
            }
            Some("router_interface") => {
                if let Ok(port) = attr(object, "port") {
                    if bound.port_oids.values().any(|p| p == port) {
                        return Err("preset port already has a routed interface".into());
                    }
                }
            }
            _ => (),
        }
    }
    // Existing non-default membership or policies must not be silently destroyed.
    // Discovery is limited: runtime errors still stop the ordered apply without retry.
    let mut removals = Vec::new();
    for member in objects
        .iter()
        .filter(|o| o.kind.as_deref() == Some("vlan_member"))
    {
        if bridge_ports
            .values()
            .any(|bp| attr(member, "bridge_port").ok() == Some(bp.as_str()))
        {
            if command::oid(attr(member, "vlan")?, false)? != default_vlan {
                return Err(
                    "preset port has non-default VLAN membership; remove explicitly first".into(),
                );
            }
            removals.push(Op::Remove {
                target: Target::Object(reference("vlan_member", key(member)?)),
            });
        }
    }
    for oid in bound.port_oids.values() {
        let port = objects
            .iter()
            .find(|o| o.kind.as_deref() == Some("port") && o.key.as_ref() == Some(oid))
            .ok_or("selected port unavailable")?;
        for name in ["ingress_acl", "egress_acl"] {
            if command::oid(attr(port, name)?, true)? != "0x0" {
                return Err(format!(
                    "{oid} already has {name}; no implicit policy replacement"
                ));
            }
        }
        if !attr(port, "egress_mirror_sessions")?.is_empty() {
            return Err(format!("{oid} already has egress mirrors"));
        }
    }
    let mut ops = Vec::new();
    let vr = create(
        &mut ops,
        "virtual_router",
        "preset-vr",
        vec![("ipv4", literal(true)), ("ipv6", literal(true))],
    );
    let mut tables = BTreeMap::new();
    for family in ["mac", "ipv4", "ipv6"] {
        let mut attrs = vec![("stage", literal("ingress")), ("family", literal(family))];
        if family == "mac" {
            attrs.push(("src_mac_enabled", literal(true)));
        } else {
            attrs.push(("l4_dst_port_enabled", literal(true)));
        }
        tables.insert(
            family,
            create(&mut ops, "acl_table", &format!("acl-{family}"), attrs),
        );
    }
    let mut rule_index = 0;
    for deny in &bound.preset.ingress_denies {
        let matches: Vec<(&str, Vec<(&str, V)>)> = match deny {
            Deny::SourceMac { mac } => vec![("mac", vec![("src_mac", literal(mac))])],
            Deny::TcpDestinationPort { port } => ["ipv4", "ipv6"]
                .into_iter()
                .map(|family| {
                    (
                        family,
                        vec![("protocol", literal(6)), ("l4_dst_port", literal(port))],
                    )
                })
                .collect(),
            Deny::SourceIpv6 { prefix } => vec![("ipv6", vec![("src", literal(prefix))])],
        };
        for (family, mut attrs) in matches {
            attrs.extend([
                ("table", V::Reference(tables[family].clone())),
                ("priority", literal(1000 - rule_index)),
                ("action", literal("deny")),
                ("enable", literal(true)),
            ]);
            create(&mut ops, "acl_entry", &format!("deny-{rule_index}"), attrs);
            rule_index += 1;
        }
    }
    // No catch-all PERMIT entries in parallel tables: unmatched traffic continues,
    // while any matching DROP remains effective across independent deny tables.
    let group = create(
        &mut ops,
        "acl_group",
        "ingress-policy",
        vec![("stage", literal("ingress"))],
    );
    for (index, (family, table)) in tables.iter().enumerate() {
        create(
            &mut ops,
            "acl_group_member",
            &format!("group-{family}"),
            vec![
                ("group", V::Reference(group.clone())),
                ("table", V::Reference(table.clone())),
                ("priority", literal(index + 1)),
            ],
        );
    }
    let transport_oid = &bound.port_oids[&bound.preset.erspan.transport_port];
    let mirror = create(
        &mut ops,
        "mirror_session",
        "erspan",
        vec![
            (
                "monitor_port",
                V::Reference(reference("port", transport_oid)),
            ),
            ("src_ip", literal(&bound.preset.erspan.source_ip)),
            ("dst_ip", literal(&bound.preset.erspan.destination_ip)),
            ("src_mac", literal(&mac)),
            ("dst_mac", literal(&bound.preset.erspan.destination_mac)),
            ("ttl", literal(bound.preset.erspan.ttl)),
            ("tos", literal(0)),
        ],
    );
    ops.extend(removals);
    for port in &bound.preset.ports {
        let oid = &bound.port_oids[&port.name];
        let port_ref = reference("port", oid);
        let mut rif_attrs = vec![
            ("virtual_router", V::Reference(vr.clone())),
            ("src_mac", literal(&mac)),
            ("ipv4", literal(true)),
            ("ipv6", literal(true)),
        ];
        let addresses = match &port.interface {
            Interface::Access {
                vlan,
                ipv4_address,
                ipv6_address,
            } => {
                let vlan_ref = create(
                    &mut ops,
                    "vlan",
                    &format!("vlan-{vlan}"),
                    vec![("vlan_id", literal(vlan))],
                );
                let bridge = match bridge_ports.get(oid) {
                    Some(bp) => reference("bridge_port", bp),
                    None => create(
                        &mut ops,
                        "bridge_port",
                        &format!("bp-{vlan}"),
                        vec![
                            ("port", V::Reference(port_ref.clone())),
                            ("admin", literal(true)),
                            ("learning", literal("hardware")),
                        ],
                    ),
                };
                create(
                    &mut ops,
                    "vlan_member",
                    &format!("member-{vlan}"),
                    vec![
                        ("vlan", V::Reference(vlan_ref.clone())),
                        ("bridge_port", V::Reference(bridge)),
                        ("tagging", literal("untagged")),
                    ],
                );
                ops.push(Op::Set {
                    target: Target::Object(port_ref.clone()),
                    attrs: attributes(vec![("pvid", literal(vlan))]),
                });
                rif_attrs.push(("vlan", V::Reference(vlan_ref)));
                vec![ipv4_address, ipv6_address]
            }
            Interface::Routed { ipv4_address } => {
                if let Some(bp) = bridge_ports.get(oid) {
                    ops.push(Op::Remove {
                        target: Target::Object(reference("bridge_port", bp)),
                    });
                }
                rif_attrs.push(("port", V::Reference(port_ref.clone())));
                vec![ipv4_address]
            }
        };
        let rif = create(
            &mut ops,
            "router_interface",
            &format!("rif-{}", port.name),
            rif_attrs,
        );
        for address in addresses {
            entry(
                &mut ops,
                "interface_address",
                vec![
                    ("router_interface", V::Reference(rif.clone())),
                    ("ingress_port", V::Reference(port_ref.clone())),
                    ("address", literal(address)),
                ],
            );
            entry(
                &mut ops,
                "route",
                vec![
                    ("virtual_router", V::Reference(vr.clone())),
                    ("prefix", literal(command::cidr(address)?)),
                    ("next_hop", V::Reference(rif.clone())),
                    ("action", literal("forward")),
                ],
            );
        }
        if port.name == bound.preset.erspan.transport_port {
            entry(
                &mut ops,
                "neighbor",
                vec![
                    ("router_interface", V::Reference(rif.clone())),
                    ("ip", literal(&bound.preset.erspan.destination_ip)),
                    ("mac", literal(&bound.preset.erspan.destination_mac)),
                ],
            );
            let next_hop = create(
                &mut ops,
                "next_hop",
                "collector-next-hop",
                vec![
                    ("router_interface", V::Reference(rif)),
                    ("ip", literal(&bound.preset.erspan.destination_ip)),
                ],
            );
            entry(
                &mut ops,
                "route",
                vec![
                    ("virtual_router", V::Reference(vr.clone())),
                    (
                        "prefix",
                        literal(format!("{}/32", bound.preset.erspan.destination_ip)),
                    ),
                    ("next_hop", V::Reference(next_hop)),
                    ("action", literal("forward")),
                ],
            );
        }
    }
    // Bind policy/mirroring only after dependencies exist. The transport remains
    // unbound and is never a mirror source.
    for port in &bound.preset.ports {
        let mut attrs = vec![("admin", literal(true))];
        if port.ingress_acl {
            attrs.push(("ingress_acl", V::Reference(group.clone())));
        }
        if port.mirror_egress {
            attrs.push((
                "egress_mirror_sessions",
                V::References(vec![mirror.clone()]),
            ));
        }
        ops.push(Op::Set {
            target: Target::Object(reference("port", &bound.port_oids[&port.name])),
            attrs: attributes(attrs),
        });
    }
    let plan = Plan {
        id: bound.preset.id.clone(),
        title: bound.preset.title.clone(),
        operations: ops,
        ports: bound
            .port_oids
            .values()
            .map(|oid| PortIdentity::capture(inventory, oid))
            .collect::<Result<_, _>>()?,
    };
    config::validate(&plan, inventory)?;
    Ok(plan)
}

#[cfg(test)]
pub(crate) fn fixture() -> Inventory {
    let preset = presets::get(presets::SEASTONE2_ID).unwrap();
    let mut objects: Vec<_> = preset
        .ports
        .iter()
        .enumerate()
        .map(|(i, port)| {
            Object::new(
                "port".to_owned(),
                format!("0x{:x}", i + 1),
                BTreeMap::from([
                    (
                        "lanes".into(),
                        port.lanes
                            .iter()
                            .map(u32::to_string)
                            .collect::<Vec<_>>()
                            .join(","),
                    ),
                    ("speed".into(), port.speed_mbps.to_string()),
                    ("pvid".into(), "1".into()),
                    ("ingress_acl".into(), "0x0".into()),
                    ("egress_acl".into(), "0x0".into()),
                    ("egress_mirror_sessions".into(), "".into()),
                ]),
            )
        })
        .collect();
    objects.push(Object::new(
        "switch".to_owned(),
        "0x1000".to_owned(),
        BTreeMap::from([
            ("src_mac".into(), "02:00:00:00:01:01".into()),
            ("default_vlan".into(), "0x1001".into()),
            ("preset_api".into(), "1".into()),
            ("interface_address_backend".into(), "enabled".into()),
        ]),
    ));
    Inventory::new(
        objects,
        vec!["test inventory; not hardware evidence".to_owned()],
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::{
        apply,
        client::{Failure, Service},
        config::Staging,
    };
    use std::sync::atomic::AtomicBool;

    #[test]
    fn complete_plan_has_all_topology_addresses_and_independent_denies() {
        let inventory = fixture();
        let bound =
            presets::bind(presets::get(presets::SEASTONE2_ID).unwrap(), &inventory).unwrap();
        let plan = build(&bound, &inventory).unwrap();
        let validation = config::validate(&plan, &inventory).unwrap();
        let creates = |kind: &str| {
            validation
                .preview
                .iter()
                .filter_map(|cmd| match cmd {
                    command::Command::Create { kind: k, attrs } if k == kind => Some(attrs),
                    _ => None,
                })
                .collect::<Vec<_>>()
        };
        assert_eq!(plan.ports.len(), 33);
        assert_eq!(creates("vlan").len(), 32);
        assert_eq!(creates("router_interface").len(), 33);
        assert_eq!(creates("vlan_member").len(), 32);
        assert!(creates("vlan_member")
            .iter()
            .all(|a| a["tagging"] == "untagged"));
        let addresses = creates("interface_address");
        assert_eq!(addresses.len(), 65);
        for vlan in 101..=132 {
            assert!(addresses
                .iter()
                .any(|a| a["address"] == format!("10.{vlan}.0.1/24")));
            assert!(addresses
                .iter()
                .any(|a| a["address"] == format!("2001:db8:{vlan}::1/64")));
        }
        assert!(addresses.iter().any(|a| a["address"] == "192.0.2.1/30"));
        let mirrors = creates("mirror_session");
        assert_eq!(mirrors.len(), 1);
        assert_eq!(mirrors[0]["monitor_port"], bound.port_oids["Ethernet128"]);
        assert_eq!(mirrors[0]["dst_mac"], "02:00:00:00:00:02");
        let rules = creates("acl_entry");
        assert_eq!(rules.len(), 4);
        assert!(rules.iter().all(|a| a["action"] == "deny"));
        assert_eq!(
            rules.iter().filter(|a| a.contains_key("src_mac")).count(),
            1
        );
        assert_eq!(
            rules
                .iter()
                .filter(|a| a.get("l4_dst_port").is_some_and(|p| p == "4444")
                    && a.get("protocol").is_some_and(|p| p == "6"))
                .count(),
            2
        );
        assert_eq!(
            rules
                .iter()
                .filter(|a| a.get("src").is_some_and(|p| p == "2001:db8:dead::1/128"))
                .count(),
            1
        );
        let bindings: Vec<_> = validation
            .preview
            .iter()
            .filter_map(|cmd| match cmd {
                command::Command::Set { kind, key, attrs }
                    if kind == "port" && attrs.contains_key("egress_mirror_sessions") =>
                {
                    Some((key, attrs))
                }
                _ => None,
            })
            .collect();
        assert_eq!(bindings.len(), 32);
        assert!(bindings
            .iter()
            .all(|(key, attrs)| *key != &bound.port_oids["Ethernet128"]
                && attrs.contains_key("ingress_acl")));
        assert!(plan.operations.len() < config::MAX_OPERATIONS);
    }

    #[test]
    fn unsupported_backend_or_existing_policies_block_compilation() {
        let inventory = fixture();
        let bound =
            presets::bind(presets::get(presets::SEASTONE2_ID).unwrap(), &inventory).unwrap();
        for (kind, name, value) in [
            ("switch", "interface_address_backend", "disabled"),
            ("port", "ingress_acl", "0x123"),
            ("port", "egress_mirror_sessions", "0x123"),
        ] {
            let mut invalid = inventory.clone();
            invalid
                .objects
                .as_mut()
                .unwrap()
                .iter_mut()
                .find(|o| o.kind.as_deref() == Some(kind))
                .unwrap()
                .attributes
                .as_mut()
                .unwrap()
                .insert(name.into(), value.into());
            assert!(build(&bound, &invalid).is_err());
        }
    }

    struct Mock {
        inventory: Inventory,
        next: u64,
        mutations: usize,
    }
    impl Service for Mock {
        fn snapshot(&mut self) -> Result<Inventory, Failure> {
            Ok(self.inventory.clone())
        }
        fn get(&mut self, kind: &str, key: &str) -> Result<Object, Failure> {
            self.inventory
                .objects
                .as_ref()
                .unwrap()
                .iter()
                .find(|o| o.kind.as_deref() == Some(kind) && o.key.as_deref() == Some(key))
                .cloned()
                .ok_or_else(|| Failure {
                    category: "server".into(),
                    status: Some(-7),
                    message: "not found".into(),
                })
        }
        fn create(
            &mut self,
            kind: &str,
            attrs: &BTreeMap<String, String>,
        ) -> Result<Object, Failure> {
            self.mutations += 1;
            self.next += 1;
            let key = match kind {
                "interface_address" => {
                    format!("{}@{}", attrs["router_interface"], attrs["address"])
                }
                "neighbor" => format!("{}@{}", attrs["router_interface"], attrs["ip"]),
                "route" => format!("{}@{}", attrs["virtual_router"], attrs["prefix"]),
                _ => format!("0x{:x}", self.next),
            };
            let object = Object::new(kind.to_owned(), key, attrs.clone());
            self.inventory
                .objects
                .as_mut()
                .unwrap()
                .push(object.clone());
            Ok(object)
        }
        fn set(
            &mut self,
            kind: &str,
            key: &str,
            attrs: &BTreeMap<String, String>,
        ) -> Result<Object, Failure> {
            self.mutations += 1;
            let o = self
                .inventory
                .objects
                .as_mut()
                .unwrap()
                .iter_mut()
                .find(|o| o.kind.as_deref() == Some(kind) && o.key.as_deref() == Some(key))
                .unwrap();
            o.attributes.as_mut().unwrap().extend(attrs.clone());
            Ok(o.clone())
        }
        fn remove(&mut self, kind: &str, key: &str) -> Result<(), Failure> {
            self.mutations += 1;
            self.inventory
                .objects
                .as_mut()
                .unwrap()
                .retain(|o| !(o.kind.as_deref() == Some(kind) && o.key.as_deref() == Some(key)));
            Ok(())
        }
        fn counters(&mut self, _: &str) -> Result<BTreeMap<String, u64>, Failure> {
            unreachable!()
        }
    }
    #[test]
    fn complete_preset_applies_once_to_mock_with_real_symbol_resolution() {
        let mut mock = Mock {
            inventory: fixture(),
            next: 0x10000,
            mutations: 0,
        };
        let bound = presets::bind(
            presets::get(presets::SEASTONE2_ID).unwrap(),
            &mock.inventory,
        )
        .unwrap();
        let plan = build(&bound, &mock.inventory).unwrap();
        let expected = plan.operations.len();
        let mut staging = Staging::default();
        staging.load(plan, &mock.inventory, true).unwrap();
        assert_eq!(mock.mutations, 0);
        let approval = staging.approve(true).unwrap();
        let report = apply::apply(
            &mut staging,
            Some(approval),
            &mut mock,
            &AtomicBool::new(false),
        );
        assert_eq!(
            report.status,
            apply::ApplyStatus::Completed,
            "{:#?}",
            report.steps.last()
        );
        assert_eq!(report.completed_steps(), expected);
        assert_eq!(mock.mutations, expected);
        assert!(report.steps.iter().all(|s| s.outcome.inventory.is_none()));
        let transport = mock.get("port", &bound.port_oids["Ethernet128"]).unwrap();
        assert_eq!(
            transport.attributes.as_ref().unwrap()["egress_mirror_sessions"],
            ""
        );
        assert_eq!(transport.attributes.as_ref().unwrap()["ingress_acl"], "0x0");
        assert!(
            build(&bound, &mock.inventory).is_err(),
            "no implicit overwrite/reapply"
        );
    }
}
