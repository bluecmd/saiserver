//! A single schema drives command validation and field-specific interactive help.
use std::{collections::BTreeMap, net::IpAddr};

pub type Attrs = BTreeMap<String, String>;
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Command {
    Create {
        kind: String,
        attrs: Attrs,
    },
    Set {
        kind: String,
        key: String,
        attrs: Attrs,
    },
    Remove {
        kind: String,
        key: String,
    },
    Get {
        kind: String,
        key: String,
    },
    Counters {
        key: String,
    },
    Help {
        kind: Option<String>,
    },
}
impl Command {
    pub fn mutates(&self) -> bool {
        matches!(
            self,
            Self::Create { .. } | Self::Set { .. } | Self::Remove { .. }
        )
    }
    pub fn target(&self) -> Option<(&str, &str)> {
        match self {
            Self::Set { kind, key, .. } | Self::Remove { kind, key } | Self::Get { kind, key } => {
                Some((kind, key))
            }
            _ => None,
        }
    }
    pub fn attributes(&self) -> Option<(&str, &Attrs)> {
        match self {
            Self::Create { kind, attrs } | Self::Set { kind, attrs, .. } => Some((kind, attrs)),
            _ => None,
        }
    }
}

#[derive(Clone, Copy)]
pub enum Value {
    Bool,
    Number(u64, u64),
    Oid(&'static [&'static str], bool),
    Enum(&'static [&'static str]),
    Ip,
    Cidr,
    Mac,
}
#[derive(Clone, Copy)]
pub struct Field {
    pub name: &'static str,
    pub value: Value,
    pub required: bool,
    pub writable: bool,
    pub help: &'static str,
}
macro_rules! f {
    ($n:literal, $v:expr, $r:literal, $w:literal, $h:literal) => {
        Field {
            name: $n,
            value: $v,
            required: $r,
            writable: $w,
            help: $h,
        }
    };
}
use Value::*;
pub const KINDS: &[&str] = &[
    "port",
    "vlan",
    "bridge_port",
    "vlan_member",
    "virtual_router",
    "router_interface",
    "next_hop",
    "neighbor",
    "route",
    "acl_table",
    "acl_entry",
    "acl_group",
    "acl_group_member",
    "fdb",
    "switch",
];
pub fn fields(kind: &str) -> &'static [Field] {
    match kind {
        "port" => &[
            f!(
                "admin",
                Bool,
                false,
                true,
                "true/false; administrative link state"
            ),
            f!(
                "pvid",
                Number(1, 4094),
                false,
                true,
                "untagged ingress VLAN ID, 1..4094; membership is a separate operation"
            ),
            f!(
                "ingress_acl",
                Oid(&["acl_table", "acl_group"], true),
                false,
                true,
                "table/group OID; 0x0 detaches"
            ),
            f!(
                "egress_acl",
                Oid(&["acl_table", "acl_group"], true),
                false,
                true,
                "table/group OID; 0x0 detaches"
            ),
        ],
        "vlan" => &[f!(
            "vlan_id",
            Number(1, 4094),
            true,
            false,
            "802.1Q VLAN ID 1..4094; create-only"
        )],
        "bridge_port" => &[
            f!(
                "port",
                Oid(&["port"], false),
                true,
                false,
                "existing port OID; create-only"
            ),
            f!(
                "bridge",
                Oid(&["bridge"], false),
                false,
                false,
                "bridge OID; default bridge if omitted; create-only"
            ),
            f!("admin", Bool, false, true, "true/false; default true"),
            f!(
                "learning",
                Enum(&["hardware", "disable"]),
                false,
                true,
                "hardware or disable"
            ),
        ],
        "vlan_member" => &[
            f!(
                "vlan",
                Oid(&["vlan"], false),
                true,
                false,
                "VLAN OID, not numeric VLAN ID; create-only"
            ),
            f!(
                "bridge_port",
                Oid(&["bridge_port"], false),
                true,
                false,
                "bridge port OID; create-only"
            ),
            f!(
                "tagging",
                Enum(&["tagged", "untagged"]),
                true,
                true,
                "tagged=trunk; untagged=access egress; set port pvid separately"
            ),
        ],
        "virtual_router" => &[
            f!("ipv4", Bool, false, true, "true/false; default true"),
            f!("ipv6", Bool, false, true, "true/false; default true"),
        ],
        "router_interface" => &[
            f!(
                "virtual_router",
                Oid(&["virtual_router"], false),
                true,
                false,
                "VR OID; create-only"
            ),
            f!(
                "port",
                Oid(&["port"], false),
                false,
                false,
                "exactly one of port/vlan; create-only"
            ),
            f!(
                "vlan",
                Oid(&["vlan"], false),
                false,
                false,
                "exactly one of port/vlan; create-only"
            ),
            f!(
                "src_mac",
                Mac,
                false,
                true,
                "six colon-separated hexadecimal octets"
            ),
            f!(
                "mtu",
                Number(68, u32::MAX as u64),
                false,
                true,
                "L3 MTU 68..4294967295; hardware may impose a lower limit"
            ),
            f!("ipv4", Bool, false, true, "true/false IPv4 forwarding"),
            f!("ipv6", Bool, false, true, "true/false IPv6 forwarding"),
        ],
        "next_hop" => &[
            f!(
                "router_interface",
                Oid(&["router_interface"], false),
                true,
                false,
                "RIF OID; immutable"
            ),
            f!("ip", Ip, true, false, "IPv4 or IPv6 address; immutable"),
        ],
        "neighbor" => &[
            f!(
                "router_interface",
                Oid(&["router_interface"], false),
                true,
                false,
                "RIF OID; create-only; key is RIF@IP"
            ),
            f!(
                "ip",
                Ip,
                true,
                false,
                "IPv4 or IPv6 neighbor address; create-only"
            ),
            f!(
                "mac",
                Mac,
                true,
                true,
                "destination MAC; six colon-separated hexadecimal octets"
            ),
        ],
        "route" => &[
            f!(
                "virtual_router",
                Oid(&["virtual_router"], false),
                true,
                false,
                "VR OID; create-only; key is VR@CIDR"
            ),
            f!(
                "prefix",
                Cidr,
                true,
                false,
                "IPv4/IPv6 CIDR, canonicalized to network; create-only"
            ),
            f!(
                "next_hop",
                Oid(&["next_hop", "router_interface"], false),
                true,
                true,
                "next hop or RIF OID; server validates hardware support"
            ),
            f!(
                "action",
                Enum(&["forward", "drop"]),
                false,
                true,
                "forward or drop"
            ),
        ],
        "acl_table" => &[
            f!(
                "stage",
                Enum(&["ingress", "egress"]),
                true,
                false,
                "ingress/egress; port bind-point; create-only"
            ),
            f!(
                "family",
                Enum(&["ipv4", "ipv6"]),
                true,
                false,
                "ipv4/ipv6 src/dst matching; create-only"
            ),
        ],
        "acl_entry" => &[
            f!(
                "table",
                Oid(&["acl_table"], false),
                true,
                false,
                "ACL table OID; create-only"
            ),
            f!(
                "priority",
                Number(0, u32::MAX as u64),
                true,
                true,
                "unsigned 32-bit priority; hardware limits are authoritative"
            ),
            f!(
                "action",
                Enum(&["permit", "deny"]),
                true,
                true,
                "permit or deny"
            ),
            f!(
                "src",
                Cidr,
                false,
                true,
                "source IPv4/IPv6 CIDR; must match table family; capability dependent"
            ),
            f!(
                "dst",
                Cidr,
                false,
                true,
                "destination IPv4/IPv6 CIDR; must match table family; capability dependent"
            ),
            f!(
                "protocol",
                Number(0, 255),
                false,
                true,
                "IP protocol / next-header number 0..255"
            ),
            f!(
                "enable",
                Bool,
                false,
                true,
                "true/false; hardware capability dependent"
            ),
        ],
        "acl_group" => &[f!(
            "stage",
            Enum(&["ingress", "egress"]),
            true,
            false,
            "parallel port-bound group; ingress/egress; create-only"
        )],
        "acl_group_member" => &[
            f!(
                "group",
                Oid(&["acl_group"], false),
                true,
                false,
                "ACL group OID; create-only"
            ),
            f!(
                "table",
                Oid(&["acl_table"], false),
                true,
                false,
                "ACL table OID; create-only"
            ),
            f!(
                "priority",
                Number(0, u32::MAX as u64),
                true,
                false,
                "unsigned 32-bit priority; create-only"
            ),
        ],
        _ => &[],
    }
}

pub fn help(kind: Option<&str>) -> String {
    let mut out = String::from("create KIND name=value... | set KIND KEY name=value... | remove KIND KEY | get KIND KEY\ncounters PORT_OID | help [KIND]\nEvery mutation requires review; immutable fields require remove + create (separately confirmed).\nOID references must be nonzero decimal/0x hex (ACL binding accepts 0x0). Unknown inventory references are server-validated: discovery is not exhaustive.\n");
    for k in KINDS
        .iter()
        .filter(|k| kind.is_none_or(|wanted| wanted == **k))
    {
        out.push_str(&format!("\n{k}:\n"));
        if matches!(*k, "port") {
            out.push_str("  existing ports only; cannot create/remove\n");
        }
        if matches!(*k, "fdb" | "switch") {
            out.push_str("  read-only\n");
        }
        for f in fields(k) {
            out.push_str(&format!(
                "  {} [{}{}]: {}\n",
                f.name,
                if f.required {
                    "required on create; "
                } else {
                    "optional; "
                },
                if f.writable {
                    "writable"
                } else {
                    "create-only"
                },
                f.help
            ));
        }
    }
    out
}

pub fn oid(value: &str, zero: bool) -> Result<String, String> {
    let number = if let Some(hex) = value.strip_prefix("0x") {
        if hex.is_empty() || !hex.bytes().all(|b| b.is_ascii_hexdigit()) {
            return Err("expected decimal or 0x hexadecimal OID".into());
        }
        u64::from_str_radix(hex, 16)
    } else {
        if value.is_empty() || !value.bytes().all(|b| b.is_ascii_digit()) {
            return Err("expected decimal or 0x hexadecimal OID".into());
        }
        value.parse::<u64>()
    }
    .map_err(|_| "OID outside u64 range")?;
    if number == 0 && !zero {
        return Err("reference OID must be nonzero".into());
    }
    Ok(format!("0x{number:x}"))
}
pub fn cidr(value: &str) -> Result<String, String> {
    let (ip, prefix) = value.split_once('/').ok_or("expected IP/prefix-length")?;
    let ip: IpAddr = ip.parse().map_err(|_| "invalid IPv4/IPv6 address")?;
    if prefix.is_empty() || !prefix.bytes().all(|b| b.is_ascii_digit()) {
        return Err("invalid prefix length".into());
    }
    let n: u32 = prefix.parse().map_err(|_| "invalid prefix length")?;
    match ip {
        IpAddr::V4(ip) if n <= 32 => Ok(format!(
            "{}/{}",
            std::net::Ipv4Addr::from(u32::from(ip) & if n == 0 { 0 } else { u32::MAX << (32 - n) }),
            n
        )),
        IpAddr::V6(ip) if n <= 128 => Ok(format!(
            "{}/{}",
            std::net::Ipv6Addr::from(
                u128::from(ip) & if n == 0 { 0 } else { u128::MAX << (128 - n) }
            ),
            n
        )),
        _ => Err("IPv4 prefix must be 0..32; IPv6 0..128".into()),
    }
}
fn mac(value: &str) -> Result<String, String> {
    let octets: Vec<_> = value.split(':').collect();
    if octets.len() != 6
        || octets
            .iter()
            .any(|x| x.len() != 2 || !x.bytes().all(|b| b.is_ascii_hexdigit()))
    {
        return Err("expected MAC aa:bb:cc:dd:ee:ff".into());
    }
    Ok(value.to_ascii_lowercase())
}
pub(crate) fn value(rule: Value, raw: &str) -> Result<String, String> {
    match rule {
        Bool if matches!(raw, "true" | "false") => Ok(raw.into()),
        Bool => Err("expected true or false".into()),
        Number(min, max) => {
            if raw.is_empty() || !raw.bytes().all(|b| b.is_ascii_digit()) {
                return Err(format!("expected integer {min}..{max}"));
            }
            let n: u64 = raw
                .parse()
                .map_err(|_| format!("expected integer {min}..{max}"))?;
            if !(min..=max).contains(&n) {
                return Err(format!("expected integer {min}..{max}"));
            }
            Ok(n.to_string())
        }
        Oid(_, zero) => oid(raw, zero),
        Enum(options) if options.contains(&raw) => Ok(raw.into()),
        Enum(options) => Err(format!("expected {}", options.join("/"))),
        Ip => raw
            .parse::<IpAddr>()
            .map(|ip| ip.to_string())
            .map_err(|_| "invalid IPv4/IPv6 address".into()),
        Cidr => cidr(raw),
        Mac => mac(raw),
    }
}
pub fn key(kind: &str, raw: &str) -> Result<String, String> {
    if matches!(kind, "route" | "neighbor" | "fdb") {
        let (a, b) = raw
            .split_once('@')
            .ok_or("expected OID@CIDR, OID@IP or OID@MAC key")?;
        let b = match kind {
            "route" => cidr(b)?,
            "neighbor" => value(Ip, b)?,
            _ => mac(b)?,
        };
        Ok(format!("{}@{}", oid(a, false)?, b))
    } else {
        oid(raw, false)
    }
}

pub fn parse(input: &str) -> Result<Command, String> {
    if input.len() > 8192 {
        return Err("command exceeds 8192 bytes".into());
    }
    let words = shell_words::split(input).map_err(|e| e.to_string())?;
    let w: Vec<&str> = words.iter().map(String::as_str).collect();
    if w.first() == Some(&"help") {
        if w.len() > 2 || w.get(1).is_some_and(|k| !KINDS.contains(k)) {
            return Err("help [known KIND]".into());
        }
        return Ok(Command::Help {
            kind: w.get(1).map(|s| s.to_string()),
        });
    }
    if w.first() == Some(&"counters") {
        if w.len() != 2 {
            return Err("counters PORT_OID".into());
        }
        return Ok(Command::Counters {
            key: oid(w[1], false)?,
        });
    }
    if w.len() < 2 || !matches!(w[0], "create" | "set" | "remove" | "get") || !KINDS.contains(&w[1])
    {
        return Err("expected create/set/remove/get KIND; use help for kinds and fields".into());
    }
    let (op, kind) = (w[0], w[1]);
    if op != "get" && (matches!(kind, "switch" | "fdb") || (kind == "port" && op != "set")) {
        return Err(format!(
            "{kind}: operation {op} is not supported (read-only/existing-only)"
        ));
    }
    let target = if op != "create" {
        Some(key(kind, w.get(2).ok_or("missing resource key")?)?)
    } else {
        None
    };
    if op == "get" || op == "remove" {
        if w.len() != 3 {
            return Err("get/remove takes exactly KIND KEY".into());
        }
        let key = target.expect("key checked");
        return Ok(if op == "get" {
            Command::Get {
                kind: kind.into(),
                key,
            }
        } else {
            Command::Remove {
                kind: kind.into(),
                key,
            }
        });
    }
    let mut attrs = Attrs::new();
    for arg in &w[if op == "create" { 2 } else { 3 }..] {
        let (name, raw) = arg.split_once('=').ok_or("expected name=value")?;
        let f = fields(kind)
            .iter()
            .find(|f| f.name == name)
            .ok_or_else(|| format!("{kind}.{name}: unknown field; use help {kind}"))?;
        if op == "set" && !f.writable {
            return Err(format!(
                "{kind}.{name}: create-only; remove and recreate the object explicitly"
            ));
        }
        let v = value(f.value, raw).map_err(|e| format!("{kind}.{name}: {e}; {}", f.help))?;
        if attrs.insert(name.into(), v).is_some() {
            return Err(format!("duplicate field {name}"));
        }
    }
    if op == "create" {
        for f in fields(kind).iter().filter(|f| f.required) {
            if !attrs.contains_key(f.name) {
                return Err(format!("{kind}.{}: required; {}", f.name, f.help));
            }
        }
        if kind == "router_interface" && (attrs.contains_key("port") == attrs.contains_key("vlan"))
        {
            return Err("router_interface: specify exactly one of port or vlan".into());
        }
    } else if attrs.is_empty() {
        return Err("set requires at least one writable field".into());
    }
    if kind == "acl_entry"
        && attrs
            .get("src")
            .zip(attrs.get("dst"))
            .is_some_and(|(s, d)| s.contains(':') != d.contains(':'))
    {
        return Err("acl_entry.src/dst must use the same IP family".into());
    }
    Ok(if op == "create" {
        Command::Create {
            kind: kind.into(),
            attrs,
        }
    } else {
        Command::Set {
            kind: kind.into(),
            key: target.expect("key checked"),
            attrs,
        }
    })
}

/// A review token cannot be synthesized by polling. Both frontends must explicitly approve.
#[derive(Clone, Copy, Debug)]
pub struct Approval(());
pub fn approve(command: &Command, explicit: bool) -> Result<Option<Approval>, String> {
    if command.mutates() {
        if !explicit {
            return Err("mutation requires explicit confirmation (--yes in batch mode)".into());
        }
        Ok(Some(Approval(())))
    } else {
        Ok(None)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn valid_contract_kinds() {
        for s in ["set port 1 admin=true pvid=100 ingress_acl=0x0", "create vlan vlan_id=100", "create bridge_port port=1 learning=disable", "create vlan_member vlan=2 bridge_port=3 tagging=untagged", "create virtual_router", "create router_interface virtual_router=1 vlan=2 src_mac=AA:BB:CC:DD:EE:FF mtu=9000 ipv6=true", "create next_hop router_interface=1 ip=2001:db8::1", "create neighbor router_interface=1 ip=192.0.2.1 mac=00:11:22:33:44:55", "create route virtual_router=1 prefix=2001:db8::1/64 next_hop=3", "create acl_table stage=ingress family=ipv6", "create acl_entry table=1 priority=4294967295 action=permit src=2001:db8::/32 protocol=255 enable=true", "create acl_group stage=ingress", "create acl_group_member group=1 table=2 priority=0", "get fdb 1@00:11:22:33:44:55", "get switch 1", "remove neighbor 1@::1", "set route 1@192.0.2.42/24 action=drop"] { assert!(parse(s).is_ok(),"{s}: {:?}",parse(s)); }
    }
    #[test]
    fn rejects_bad_fields_ranges_references_and_immutable() {
        for s in [
            "create port",
            "remove port 1",
            "create fdb",
            "set vlan 1 vlan_id=2",
            "set next_hop 1 ip=::1",
            "create vlan vlan_id=4095",
            "set port 1 pvid=0",
            "set port 1 admin=yes",
            "set port 1 lanes=3",
            "set port 1 admin=true admin=false",
            "create router_interface virtual_router=1",
            "create router_interface virtual_router=1 port=2 vlan=3",
            "create neighbor router_interface=0 ip=::1 mac=00:00:00:00:00:00",
            "create next_hop router_interface=-1 ip=bad",
            "create acl_entry table=1 priority=4294967296 action=deny",
            "set acl_entry 1 protocol=256",
            "set acl_entry 1 src=::/129",
            "set acl_entry 1 src=1.2.3.4/33",
            "set acl_entry 1 src=::/0 dst=1.2.3.0/24",
            "remove route 1",
            "get vlan 1 extra",
            "set port +1 admin=true",
            "set port 18446744073709551616 admin=true",
        ] {
            assert!(parse(s).is_err(), "{s}");
        }
    }
    #[test]
    fn canonical_networks_keys_and_confirmation() {
        assert_eq!(cidr("192.0.2.129/24").unwrap(), "192.0.2.0/24");
        assert_eq!(cidr("2001:db8::99/64").unwrap(), "2001:db8::/64");
        assert_eq!(cidr("::1/0").unwrap(), "::/0");
        assert_eq!(key("route", "12@192.0.2.4/24").unwrap(), "0xc@192.0.2.0/24");
        let c = parse("create virtual_router").unwrap();
        assert!(approve(&c, false).is_err());
        assert!(approve(&c, true).unwrap().is_some());
        assert!(approve(&parse("get port 1").unwrap(), false)
            .unwrap()
            .is_none());
        for k in KINDS {
            assert!(help(Some(k)).contains(k));
        }
    }
}
