//! Built-in, hardware-independent switch configuration intent.
//!
//! The lane map is sourced from ixp-lab-sw2's stock Seastone_2 HWSKU,
//! not its active SONIX breakout profile. See docs/evidence/seastone2/.
//! Constructing or binding a preset performs no RPCs and changes no hardware.
use crate::sai_tui::Inventory;
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, BTreeSet};

pub const SEASTONE2_ID: &str = "seastone2-32x100g-1x10g";
pub const PLATFORM: &str = "x86_64-cel_seastone_2-r0";
pub const MAPPING_SHA256: &str = "2bf2f5c9868646d7209a9aaa6281c4d30a8caa1cdb9eb45a7e801581679f5aa9";

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Preset {
    pub id: String,
    pub title: String,
    pub platform: String,
    pub ports: Vec<Port>,
    pub erspan: Erspan,
    pub ingress_denies: Vec<Deny>,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Port {
    pub name: String,
    pub alias: String,
    pub lanes: Vec<u32>,
    pub speed_mbps: u32,
    pub interface: Interface,
    pub mirror_egress: bool,
    pub ingress_acl: bool,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "snake_case", deny_unknown_fields)]
pub enum Interface {
    Access {
        vlan: u16,
        ipv4_address: String,
        ipv6_address: String,
    },
    Routed {
        ipv4_address: String,
    },
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Erspan {
    pub transport_port: String,
    pub source_ip: String,
    pub destination_ip: String,
    /// Deliberately static illustrative peer, selected by user request.
    pub destination_mac: String,
    pub ttl: u8,
}
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "match", rename_all = "snake_case", deny_unknown_fields)]
pub enum Deny {
    SourceMac { mac: String },
    TcpDestinationPort { port: u16 },
    SourceIpv6 { prefix: String },
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct BoundPreset {
    pub preset: Preset,
    /// SONiC port name -> actual, observed port OID. Never synthesized.
    pub port_oids: BTreeMap<String, String>,
}

pub fn catalog() -> Vec<(&'static str, &'static str)> {
    vec![(
        SEASTONE2_ID,
        "Seastone 2: 32×100G dual-stack VLANs + 10G ERSPAN",
    )]
}

pub fn get(id: &str) -> Result<Preset, String> {
    if id != SEASTONE2_ID {
        return Err(format!("unknown switch preset {id}"));
    }
    let mut ports = Vec::new();
    for index in 0..32_u32 {
        let vlan = 101 + index as u16;
        ports.push(Port {
            name: format!("Ethernet{}", index * 4),
            alias: format!("Eth{}/1", index + 1),
            lanes: (index * 4 + 1..=index * 4 + 4).collect(),
            speed_mbps: 100_000,
            interface: Interface::Access {
                vlan,
                ipv4_address: format!("10.{vlan}.0.1/24"),
                // Decimal digits of VLAN ID, interpreted as IPv6 hex text.
                ipv6_address: format!("2001:db8:{vlan}::1/64"),
            },
            mirror_egress: true,
            ingress_acl: true,
        });
    }
    ports.push(Port {
        name: "Ethernet128".into(),
        alias: "Eth33/1".into(),
        lanes: vec![129],
        speed_mbps: 10_000,
        interface: Interface::Routed {
            ipv4_address: "192.0.2.1/30".into(),
        },
        mirror_egress: false,
        ingress_acl: false,
    });
    Ok(Preset {
        id: id.into(),
        title: catalog()[0].1.into(),
        platform: PLATFORM.into(),
        ports,
        erspan: Erspan {
            transport_port: "Ethernet128".into(),
            source_ip: "192.0.2.1".into(),
            destination_ip: "192.0.2.2".into(),
            destination_mac: "02:00:00:00:00:02".into(),
            ttl: 64,
        },
        ingress_denies: vec![
            Deny::SourceMac {
                mac: "02:00:00:00:00:aa".into(),
            },
            Deny::TcpDestinationPort { port: 4444 },
            Deny::SourceIpv6 {
                prefix: "2001:db8:dead::1/128".into(),
            },
        ],
    })
}

fn lanes(text: &str) -> Result<BTreeSet<u32>, String> {
    let mut result = BTreeSet::new();
    for raw in text.split(',') {
        let lane: u32 = raw
            .parse()
            .map_err(|_| format!("invalid lane list {text:?}"))?;
        if !result.insert(lane) {
            return Err(format!("duplicate lane {lane}"));
        }
    }
    Ok(result)
}

/// Fail closed for breakout, missing/extra ports, overlapping lane reports,
/// wrong speeds, duplicate OIDs, and incomplete discovery. Lane order is not
/// significant. This validates topology, not an independently attested chassis ID.
pub fn bind(preset: Preset, inventory: &Inventory) -> Result<BoundPreset, String> {
    // Built-ins are immutable recipes, not arbitrary input silently trusted as
    // validated topology. A future external format needs its own full validator.
    if preset != get(&preset.id)? {
        return Err("modified built-in preset is not a validated recipe".into());
    }
    let observed: Vec<_> = inventory
        .objects
        .as_deref()
        .unwrap_or_default()
        .iter()
        .filter(|o| o.kind.as_deref() == Some("port"))
        .collect();
    if observed.len() != preset.ports.len() {
        return Err(format!(
            "{} requires exactly {} physical ports in stock HWSKU mode; discovered {}. Breakout reconfiguration is not automatic",
            preset.title, preset.ports.len(), observed.len()
        ));
    }
    let mut seen_oids = BTreeSet::new();
    let mut seen_lanes = BTreeSet::new();
    let mut physical = Vec::new();
    for object in observed {
        let oid = crate::command::oid(object.key.as_deref().ok_or("port has no OID")?, false)?;
        if !seen_oids.insert(oid.clone()) {
            return Err(format!("duplicate discovered port OID {oid}"));
        }
        let attrs = object
            .attributes
            .as_ref()
            .ok_or("port attributes unavailable")?;
        let port_lanes = lanes(attrs.get("lanes").ok_or("port lane getter unavailable")?)?;
        for lane in &port_lanes {
            if !seen_lanes.insert(*lane) {
                return Err(format!(
                    "ambiguous physical lane {lane} occurs on multiple ports"
                ));
            }
        }
        let speed: u32 = attrs
            .get("speed")
            .ok_or("port speed getter unavailable")?
            .parse()
            .map_err(|_| "invalid port speed")?;
        physical.push((oid, port_lanes, speed));
    }
    let mut port_oids = BTreeMap::new();
    for port in &preset.ports {
        let expected: BTreeSet<_> = port.lanes.iter().copied().collect();
        let (oid, _, speed) = physical
            .iter()
            .find(|(_, actual, _)| *actual == expected)
            .ok_or_else(|| {
                format!(
                    "{} ({}) requires lanes {:?}; missing or broken out",
                    port.name, port.alias, port.lanes
                )
            })?;
        if *speed != port.speed_mbps {
            return Err(format!(
                "{} requires {} Mbps; observed {}. Configure the stock port mode separately",
                port.name, port.speed_mbps, speed
            ));
        }
        port_oids.insert(port.name.clone(), oid.clone());
    }
    Ok(BoundPreset { preset, port_oids })
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::sai_tui::Object;

    fn inventory(preset: &Preset) -> Inventory {
        Inventory::new(
            preset
                .ports
                .iter()
                .enumerate()
                .map(|(i, p)| {
                    Object::new(
                        "port".to_owned(),
                        format!("0x{:x}", 0x700 + i * 3),
                        BTreeMap::from([
                            (
                                "lanes".into(),
                                p.lanes
                                    .iter()
                                    .rev()
                                    .map(u32::to_string)
                                    .collect::<Vec<_>>()
                                    .join(","),
                            ),
                            ("speed".into(), p.speed_mbps.to_string()),
                        ]),
                    )
                })
                .rev()
                .collect::<Vec<_>>(),
            Vec::<String>::new(),
        )
    }

    #[test]
    fn complete_intent_and_exact_address_spelling() {
        let p = get(SEASTONE2_ID).unwrap();
        assert_eq!(p.ports.len(), 33);
        let mut all_lanes = BTreeSet::new();
        for (index, port) in p.ports[..32].iter().enumerate() {
            let vlan = 101 + index as u16;
            assert_eq!(port.speed_mbps, 100_000);
            assert_eq!(
                port.interface,
                Interface::Access {
                    vlan,
                    ipv4_address: format!("10.{vlan}.0.1/24"),
                    ipv6_address: format!("2001:db8:{vlan}::1/64"),
                }
            );
            assert!(port.mirror_egress && port.ingress_acl);
            for lane in &port.lanes {
                assert!(all_lanes.insert(*lane));
            }
        }
        assert_eq!(all_lanes, (1..=128).collect());
        let transport = &p.ports[32];
        assert_eq!(transport.lanes, [129]);
        assert_eq!(transport.speed_mbps, 10_000);
        assert!(!transport.mirror_egress && !transport.ingress_acl);
        assert_eq!(
            transport.interface,
            Interface::Routed {
                ipv4_address: "192.0.2.1/30".into()
            }
        );
        assert_eq!(p.ingress_denies.len(), 3);
        assert_eq!(p.erspan.destination_mac, "02:00:00:00:00:02");
        let roundtrip: Preset = serde_json::from_str(&serde_json::to_string(&p).unwrap()).unwrap();
        assert_eq!(roundtrip, p);
    }

    #[test]
    fn generated_map_matches_collected_stock_hwsku_and_rejects_active_breakout() {
        let evidence: serde_json::Value = serde_json::from_str(include_str!(
            "../../docs/evidence/seastone2/ixp-lab-sw2-sanitized.json"
        ))
        .unwrap();
        let source = &evidence["files"]
            ["/usr/share/sonic/device/x86_64-cel_seastone_2-r0/Seastone_2/port_config.ini"];
        assert_eq!(source["source_sha256"], MAPPING_SHA256);
        let lines: Vec<_> = source["evidence"]
            .as_str()
            .unwrap()
            .lines()
            .filter(|line| !line.trim().is_empty() && !line.starts_with('#'))
            .collect();
        let p = get(SEASTONE2_ID).unwrap();
        assert_eq!(lines.len(), p.ports.len());
        for (line, port) in lines.iter().zip(&p.ports) {
            let fields: Vec<_> = line.split_whitespace().collect();
            assert_eq!(fields[0], port.name);
            assert_eq!(
                lanes(fields[1]).unwrap(),
                port.lanes.iter().copied().collect()
            );
            assert_eq!(fields[2], port.alias);
            assert_eq!(fields[4].parse::<u32>().unwrap(), port.speed_mbps);
        }
        let active = evidence["files"]["/etc/sonic/config_db.json"]["evidence"]["PORT"]
            .as_object()
            .unwrap();
        let inventory = Inventory::new(
            active
                .values()
                .enumerate()
                .map(|(i, port)| {
                    Object::new(
                        "port".to_owned(),
                        format!("0x{:x}", i + 1),
                        BTreeMap::from([
                            ("lanes".into(), port["lanes"].as_str().unwrap().into()),
                            ("speed".into(), port["speed"].as_str().unwrap().into()),
                        ]),
                    )
                })
                .collect::<Vec<_>>(),
            Vec::<String>::new(),
        );
        assert_eq!(active.len(), 36);
        assert!(bind(p, &inventory).unwrap_err().contains("Breakout"));
    }

    #[test]
    fn binding_uses_observed_lanes_not_inventory_order_or_guessed_oid() {
        let p = get(SEASTONE2_ID).unwrap();
        let bound = bind(p.clone(), &inventory(&p)).unwrap();
        assert_eq!(bound.port_oids["Ethernet0"], "0x700");
        assert_eq!(bound.port_oids["Ethernet128"], "0x760");
    }

    #[test]
    fn incompatible_inventory_and_changed_recipe_fail_closed() {
        let p = get(SEASTONE2_ID).unwrap();
        let good = inventory(&p);
        let mut bad = good.clone();
        bad.objects.as_mut().unwrap().pop();
        assert!(bind(p.clone(), &bad).is_err());
        for (field, value) in [
            ("lanes", "1,1,2,3"),
            ("lanes", "1,2,3,4"),
            ("speed", "100000"),
            ("lanes", "bad"),
        ] {
            let mut bad = good.clone();
            bad.objects.as_mut().unwrap()[0]
                .attributes
                .as_mut()
                .unwrap()
                .insert(field.into(), value.into());
            assert!(bind(p.clone(), &bad).is_err(), "{field}={value}");
        }
        let mut changed = p;
        changed.ports[0].mirror_egress = false;
        assert!(bind(changed, &good).is_err());
        assert!(get("unknown").is_err());
    }
}
