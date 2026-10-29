//! Lists a saiserver's ports and VLAN membership, like `show interfaces brief`,
//! through the generated Rust bindings of the bounded SaiTui API
//! (`@saiserver//:thrift_rust`) and its matching runtime
//! (`@saiserver//:thrift_rust_runtime`, imported as `thrift`).
//!
//! Usage: show_interfaces_rust [HOST [PORT]]   (default: 127.0.0.1 9090)
use sai_tui_rpc::{Object, SaiTuiSyncClient, TSaiTuiSyncClient};
use std::collections::BTreeMap;
use std::net::TcpStream;
use std::process::ExitCode;
use thrift::protocol::{TBinaryInputProtocol, TBinaryOutputProtocol};
use thrift::transport::{TBufferedReadTransport, TBufferedWriteTransport};

/// "-" if the SDK reported no such attribute, "?" if its getter is unsupported.
fn attribute(object: &Object, name: &str) -> String {
    let attributes = object.attributes.as_ref();
    match attributes.and_then(|a| a.get(name)) {
        Some(value) => value.clone(),
        None if attributes.is_some_and(|a| a.contains_key(&format!("unavailable.{name}"))) => {
            "?".into()
        }
        None => "-".into(),
    }
}

fn admin(value: &str) -> String {
    match value {
        "true" => "up".into(),
        "false" => "down".into(),
        other => other.into(),
    }
}

/// sai_port_oper_status_t
fn oper(value: &str) -> String {
    match value {
        "1" => "up",
        "2" => "down",
        "3" => "testing",
        "4" => "absent",
        "-" | "?" => value,
        _ => "unknown",
    }
    .into()
}

/// SAI reports port speed in Mb/s.
fn speed(value: &str) -> String {
    match value.parse::<u64>() {
        Ok(mbps) if mbps % 1000 == 0 => format!("{}G", mbps / 1000),
        Ok(mbps) => format!("{mbps}M"),
        Err(_) => value.into(),
    }
}

fn key(object: &Object) -> String {
    object.key.clone().unwrap_or_default()
}

fn print(objects: &[Object]) {
    let of_kind = |kind: &str| -> Vec<&Object> {
        objects
            .iter()
            .filter(|o| o.kind.as_deref() == Some(kind))
            .collect()
    };
    let ports = of_kind("port");
    let members = of_kind("vlan_member");
    let port_of_bridge_port: BTreeMap<String, String> = of_kind("bridge_port")
        .into_iter()
        .map(|b| (key(b), attribute(b, "port")))
        .collect();

    println!(
        "{:<14} {:<16} {:<6} {:<6} {:<8} PVID",
        "Port", "Lanes", "Speed", "Admin", "Oper"
    );
    for port in &ports {
        println!(
            "{:<14} {:<16} {:<6} {:<6} {:<8} {}",
            key(port),
            attribute(port, "lanes"),
            speed(&attribute(port, "speed")),
            admin(&attribute(port, "admin")),
            oper(&attribute(port, "oper_status")),
            attribute(port, "pvid"),
        );
    }

    // VLAN key -> tagging mode -> member ports, in port order.
    let mut by_vlan: BTreeMap<String, BTreeMap<String, Vec<String>>> = BTreeMap::new();
    for port in &ports {
        for member in &members {
            if port_of_bridge_port.get(&attribute(member, "bridge_port")) != Some(&key(port)) {
                continue;
            }
            by_vlan
                .entry(attribute(member, "vlan"))
                .or_default()
                .entry(attribute(member, "tagging"))
                .or_default()
                .push(key(port));
        }
    }
    let mut vlans = of_kind("vlan");
    vlans.sort_by_key(|v| attribute(v, "vlan_id").parse::<u64>().unwrap_or(u64::MAX));
    println!("\n{:<5} {:<9} Ports", "VLAN", "Mode");
    for vlan in vlans {
        let id = attribute(vlan, "vlan_id");
        match by_vlan.get(&key(vlan)) {
            Some(modes) if !modes.is_empty() => {
                for (mode, ports) in modes {
                    println!("{:<5} {:<9} {}", id, mode, ports.join(" "));
                }
            }
            _ => println!("{:<5} {:<9} -", id, "-"),
        }
    }
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().collect();
    let host = args.get(1).map_or("127.0.0.1", String::as_str);
    let port = args.get(2).map_or("9090", String::as_str);
    let address = format!("{host}:{port}");
    let snapshot = TcpStream::connect(&address)
        .map_err(thrift::Error::from)
        .and_then(|stream| {
            let read = stream.try_clone()?;
            SaiTuiSyncClient::new(
                TBinaryInputProtocol::new(TBufferedReadTransport::new(read), true),
                TBinaryOutputProtocol::new(TBufferedWriteTransport::new(stream), true),
            )
            .tui_snapshot()
        });
    match snapshot {
        Ok(inventory) => {
            print(&inventory.objects.unwrap_or_default());
            ExitCode::SUCCESS
        }
        Err(e) => {
            eprintln!("{address}: {e}");
            ExitCode::FAILURE
        }
    }
}
