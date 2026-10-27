//! RPC-free, typed staging for presets. The command schema remains authoritative.
//!
//! OID-valued fields must use `Reference` or `NullOid`, never text substitution.
//! Symbols name earlier OID creates only; composite entries can be created without
//! a binding and addressed by an explicit `Target::Entry`. Unknown existing OIDs
//! remain server-authoritative (inventory is incomplete), but selected ports must
//! be present. No device model or preset catalog is built into this module.
use crate::{
    client::validate_references,
    command::{self, Command, Value},
    sai_tui::{Inventory, Object},
};
use std::{
    collections::{BTreeMap, BTreeSet},
    sync::Arc,
};

pub const MAX_OPERATIONS: usize = 256;
pub type Attributes = BTreeMap<String, AttributeValue>;

#[derive(Clone, Debug, PartialEq, Eq)]
pub enum ObjectRef {
    Existing { kind: String, oid: String },
    Created { kind: String, symbol: String },
}
impl ObjectRef {
    pub fn kind(&self) -> &str {
        match self {
            Self::Existing { kind, .. } | Self::Created { kind, .. } => kind,
        }
    }
    pub(crate) fn resolve(&self, bindings: &Bindings) -> Result<ResolvedObject, String> {
        match self {
            Self::Existing { kind, oid } => Ok(ResolvedObject {
                kind: kind.clone(),
                key: command::oid(oid, false)?,
            }),
            Self::Created { kind, symbol } => {
                let object = bindings
                    .get(symbol)
                    .ok_or_else(|| format!("unknown/forward symbol {symbol}"))?;
                if &object.kind != kind {
                    return Err(format!("symbol {symbol} is {}, not {kind}", object.kind));
                }
                Ok(object.clone())
            }
        }
    }
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum AttributeValue {
    Literal(String),
    Reference(ObjectRef),
    NullOid,
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Target {
    Object(ObjectRef),
    /// Explicit existing composite key (e.g. VR@CIDR); never interpolated.
    Entry {
        kind: String,
        key: String,
    },
}
impl Target {
    fn resolve(&self, bindings: &Bindings) -> Result<ResolvedObject, String> {
        match self {
            Self::Object(reference) => reference.resolve(bindings),
            Self::Entry { kind, key } => {
                let key = command::key(kind, key)?;
                if !key.contains('@') {
                    return Err("use an explicit ObjectRef for OID targets".into());
                }
                Ok(ResolvedObject {
                    kind: kind.clone(),
                    key,
                })
            }
        }
    }
}
#[derive(Clone, Debug, PartialEq, Eq)]
pub enum Operation {
    Create {
        kind: String,
        bind: Option<String>,
        attrs: Attributes,
    },
    Set {
        target: Target,
        attrs: Attributes,
    },
    Remove {
        target: Target,
    },
}
impl Operation {
    pub(crate) fn references(&self) -> Vec<&ObjectRef> {
        let mut refs = Vec::new();
        if let Self::Set {
            target: Target::Object(r),
            ..
        }
        | Self::Remove {
            target: Target::Object(r),
        } = self
        {
            refs.push(r);
        }
        let attrs = match self {
            Self::Create { attrs, .. } | Self::Set { attrs, .. } => Some(attrs),
            _ => None,
        };
        if let Some(attrs) = attrs {
            refs.extend(attrs.values().filter_map(|v| match v {
                AttributeValue::Reference(r) => Some(r),
                _ => None,
            }));
        }
        refs
    }
    pub(crate) fn command(&self, bindings: &Bindings) -> Result<Command, String> {
        let (mut words, kind, attrs) = match self {
            Self::Create { kind, attrs, .. } => (
                vec!["create".into(), kind.clone()],
                kind.clone(),
                Some(attrs),
            ),
            Self::Set { target, attrs } => {
                let object = target.resolve(bindings)?;
                (
                    vec!["set".into(), object.kind.clone(), object.key],
                    object.kind,
                    Some(attrs),
                )
            }
            Self::Remove { target } => {
                let object = target.resolve(bindings)?;
                (
                    vec!["remove".into(), object.kind.clone(), object.key],
                    object.kind,
                    None,
                )
            }
        };
        if let Some(attrs) = attrs {
            for (name, value) in attrs {
                let field = command::fields(&kind)
                    .iter()
                    .find(|f| f.name == name)
                    .ok_or_else(|| format!("{kind}.{name}: unknown field"))?;
                let raw = match (field.value, value) {
                    (Value::Oid(kinds, _), AttributeValue::Reference(reference)) => {
                        let object = reference.resolve(bindings)?;
                        if !kinds.contains(&object.kind.as_str()) {
                            return Err(format!(
                                "{kind}.{name}: wrong reference kind {}",
                                object.kind
                            ));
                        }
                        command::oid(&object.key, false)?
                    }
                    (Value::Oid(_, true), AttributeValue::NullOid) => "0x0".into(),
                    (Value::Oid(..), _) => {
                        return Err(format!(
                            "{kind}.{name}: requires a typed reference (or permitted null)"
                        ))
                    }
                    (_, AttributeValue::Literal(raw)) => raw.clone(),
                    _ => {
                        return Err(format!(
                            "{kind}.{name}: expected a literal, not an OID reference"
                        ))
                    }
                };
                words.push(format!("{name}={raw}"));
            }
        }
        // Quote whole tokens, including names/kinds: data cannot inject syntax.
        command::parse(&shell_words::join(words))
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Plan {
    pub id: String,
    pub title: String,
    pub operations: Vec<Operation>,
    pub ports: Vec<PortIdentity>,
}
/// Stable identity requirements captured from the selected inventory, not row numbers.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct PortIdentity {
    pub oid: String,
    pub lanes: Option<Vec<u32>>,
    pub speed: Option<u32>,
}
impl PortIdentity {
    pub fn capture(inventory: &Inventory, oid: &str) -> Result<Self, String> {
        let oid = command::oid(oid, false)?;
        let object = inventory
            .objects
            .as_deref()
            .unwrap_or_default()
            .iter()
            .find(|o| {
                o.key
                    .as_deref()
                    .and_then(|k| command::oid(k, false).ok())
                    .as_ref()
                    == Some(&oid)
            })
            .ok_or_else(|| format!("selected port {oid} missing from inventory"))?;
        if object.kind.as_deref() != Some("port") {
            return Err(format!("selected {oid} is not a port"));
        }
        let attrs = object
            .attributes
            .as_ref()
            .ok_or("selected port has no attributes")?;
        let lanes = attrs
            .get("lanes")
            .map(|s| -> Result<Vec<u32>, String> {
                let lanes = s
                    .split(',')
                    .map(|n| {
                        n.parse::<u32>()
                            .map_err(|_| "invalid port lanes".to_string())
                    })
                    .collect::<Result<Vec<_>, _>>()?;
                if lanes.is_empty() || lanes.iter().collect::<BTreeSet<_>>().len() != lanes.len() {
                    return Err("invalid/duplicate port lanes".into());
                }
                Ok(lanes)
            })
            .transpose()?;
        let speed = attrs
            .get("speed")
            .map(|s| s.parse::<u32>().map_err(|_| "invalid port speed"))
            .transpose()?;
        Ok(Self { oid, lanes, speed })
    }
}

#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ResolvedObject {
    pub kind: String,
    pub key: String,
}
pub type Bindings = BTreeMap<String, ResolvedObject>;
#[derive(Clone, Debug)]
pub struct Validation {
    /// Preview only: generated OIDs are local placeholders, NEVER apply commands.
    pub preview: Vec<Command>,
    pub warnings: Vec<String>,
}

pub(crate) fn check_ports(ports: &[PortIdentity], inventory: &Inventory) -> Result<(), String> {
    let mut seen = BTreeSet::new();
    for expected in ports {
        let actual = PortIdentity::capture(inventory, &expected.oid)?;
        if !seen.insert(actual.oid.clone()) {
            return Err(format!("duplicate selected port {}", actual.oid));
        }
        if expected
            .lanes
            .as_ref()
            .is_some_and(|v| Some(v) != actual.lanes.as_ref())
            || expected.speed.is_some_and(|v| Some(v) != actual.speed)
        {
            return Err(format!("selected port {} lanes/speed changed", actual.oid));
        }
    }
    Ok(())
}
fn object_key(object: &Object) -> Option<String> {
    command::key(object.kind.as_deref()?, object.key.as_deref()?).ok()
}
pub(crate) fn check_identity(kind: &str, key: &str, inventory: &Inventory) -> Result<(), String> {
    for object in inventory.objects.as_deref().unwrap_or_default() {
        if object_key(object).as_deref() == Some(key) && object.kind.as_deref() != Some(kind) {
            return Err(format!("{key}: inventory kind does not match {kind}"));
        }
    }
    Ok(())
}
fn name_valid(name: &str) -> bool {
    !name.is_empty()
        && name.len() <= 128
        && name
            .bytes()
            .all(|b| b.is_ascii_alphanumeric() || b == b'_' || b == b'-' || b == b'.')
}

/// Validate EVERY step locally, simulating earlier creates/sets/removes. No Service
/// is accepted here. Warnings preserve the single-command incomplete-inventory policy.
pub fn validate(plan: &Plan, inventory: &Inventory) -> Result<Validation, String> {
    if !name_valid(&plan.id)
        || plan.title.trim().is_empty()
        || plan.title.len() > 256
        || plan.title.chars().any(char::is_control)
    {
        return Err("plan requires a bounded id and human title".into());
    }
    if plan.operations.is_empty() || plan.operations.len() > MAX_OPERATIONS {
        return Err(format!("plan requires 1..{MAX_OPERATIONS} operations"));
    }
    check_ports(&plan.ports, inventory)?;
    let mut simulated = inventory.clone();
    let objects = simulated.objects.get_or_insert_with(Vec::new);
    for object in objects.iter_mut() {
        if let Some(key) = object_key(object) {
            object.key = Some(key);
        }
    }
    let mut reserved: BTreeSet<String> = objects.iter().filter_map(|o| o.key.clone()).collect();
    let mut declared = BTreeMap::new();
    for op in &plan.operations {
        for reference in op.references() {
            if let ObjectRef::Existing { kind, oid } = reference {
                let key = command::oid(oid, false)?;
                if declared
                    .insert(key.clone(), kind)
                    .is_some_and(|previous| previous != kind)
                {
                    return Err(format!("{key}: conflicting existing reference kinds"));
                }
                reserved.insert(key);
            }
        }
    }
    let mut next = u64::MAX;
    let mut bindings = Bindings::new();
    let mut symbols = BTreeSet::new();
    let mut removed = BTreeSet::new();
    let mut result = Validation {
        preview: vec![],
        warnings: vec![],
    };
    for (index, op) in plan.operations.iter().enumerate() {
        let step = || -> Result<Command, String> {
            for reference in op.references() {
                let object = reference.resolve(&bindings)?;
                if removed.contains(&object.key) {
                    return Err(format!("reference to removed object {}", object.key));
                }
                check_identity(&object.kind, &object.key, &simulated)?;
                if object.kind == "port" {
                    PortIdentity::capture(&simulated, &object.key)?;
                }
            }
            let cmd = op.command(&bindings)?;
            if let Some((kind, key)) = cmd.target() {
                check_identity(kind, key, &simulated)?;
                if removed.contains(key) {
                    return Err(format!("target {key} already removed"));
                }
            }
            Ok(cmd)
        };
        let cmd = step().map_err(|e| format!("step {}: {e}", index + 1))?;
        result.warnings.extend(
            validate_references(&cmd, &simulated)
                .map_err(|e| format!("step {}: {e}", index + 1))?,
        );
        match (&cmd, op) {
            (Command::Create { kind, attrs }, Operation::Create { bind, .. }) => {
                while reserved.contains(&format!("0x{next:x}")) {
                    next -= 1;
                }
                let key = format!("0x{next:x}");
                next -= 1;
                reserved.insert(key.clone());
                // Composite creates have no OID output; do not fabricate one.
                if command::key(kind, &key).is_ok() {
                    simulated.objects.as_mut().unwrap().push(Object::new(
                        kind.clone(),
                        key.clone(),
                        attrs.clone(),
                    ));
                } else if bind.is_some() {
                    return Err("only standalone OID creates can bind symbols".into());
                }
                if let Some(symbol) = bind {
                    if !name_valid(symbol) || !symbols.insert(symbol.clone()) {
                        return Err(format!("invalid/duplicate symbol {symbol}"));
                    }
                    bindings.insert(
                        symbol.clone(),
                        ResolvedObject {
                            kind: kind.clone(),
                            key,
                        },
                    );
                }
            }
            (Command::Set { kind, key, attrs }, _) => {
                let objects = simulated.objects.as_mut().unwrap();
                if let Some(object) = objects.iter_mut().find(|o| o.key.as_ref() == Some(key)) {
                    object
                        .attributes
                        .get_or_insert_with(BTreeMap::new)
                        .extend(attrs.clone());
                } else {
                    objects.push(Object::new(kind.clone(), key.clone(), attrs.clone()));
                }
            }
            (Command::Remove { key, .. }, _) => {
                removed.insert(key.clone());
                simulated
                    .objects
                    .as_mut()
                    .unwrap()
                    .retain(|o| o.key.as_ref() != Some(key));
            }
            _ => unreachable!("only mutation operations are representable"),
        }
        result.preview.push(cmd);
    }
    Ok(result)
}

#[derive(Debug, PartialEq, Eq)]
pub enum LoadResult {
    Loaded,
    Cancelled,
}
/// Non-cloneable capability. Only an explicit, separate `Staging::approve` issues
/// one; reloading or issuing a newer approval invalidates it. Never persist it.
#[derive(Debug)]
pub struct ApplyApproval {
    revision: Arc<()>,
    ticket: Arc<()>,
}
#[derive(Default)]
pub struct Staging {
    current: Option<(Plan, Validation)>,
    revision: Arc<()>,
    ticket: Option<Arc<()>>,
}
impl Staging {
    pub fn plan(&self) -> Option<&Plan> {
        self.current.as_ref().map(|(plan, _)| plan)
    }
    pub fn validation(&self) -> Option<&Validation> {
        self.current.as_ref().map(|(_, validation)| validation)
    }
    /// Explicit load/replacement confirmation only. Cancel/error preserves the
    /// previous plan AND approval; this method cannot make RPCs or approve apply.
    pub fn load(
        &mut self,
        mut plan: Plan,
        inventory: &Inventory,
        confirmed: bool,
    ) -> Result<LoadResult, String> {
        if !confirmed {
            return Ok(LoadResult::Cancelled);
        }
        validate(&plan, inventory)?;
        // Pin every referenced existing port, even if the generator omitted pins.
        let mut ports = BTreeSet::new();
        for pin in &mut plan.ports {
            let actual = PortIdentity::capture(inventory, &pin.oid)?;
            ports.insert(actual.oid.clone());
            *pin = actual;
        }
        for op in &plan.operations {
            for reference in op.references() {
                if let ObjectRef::Existing { kind, oid } = reference {
                    if kind == "port" {
                        let pin = PortIdentity::capture(inventory, oid)?;
                        if ports.insert(pin.oid.clone()) {
                            plan.ports.push(pin);
                        }
                    }
                }
            }
        }
        let validation = validate(&plan, inventory)?;
        self.current = Some((plan, validation));
        self.revision = Arc::new(());
        self.ticket = None;
        Ok(LoadResult::Loaded)
    }
    pub fn approve(&mut self, explicit: bool) -> Result<ApplyApproval, String> {
        if !explicit {
            return Err("separate explicit apply approval required".into());
        }
        if self.current.is_none() {
            return Err("no staged plan".into());
        }
        let ticket = Arc::new(());
        self.ticket = Some(ticket.clone());
        Ok(ApplyApproval {
            revision: self.revision.clone(),
            ticket,
        })
    }
    pub(crate) fn begin_apply(&mut self, approval: Option<ApplyApproval>) -> Result<Plan, String> {
        let approval = approval.ok_or("separate explicit apply approval required")?;
        if !Arc::ptr_eq(&self.revision, &approval.revision)
            || !self
                .ticket
                .as_ref()
                .is_some_and(|t| Arc::ptr_eq(t, &approval.ticket))
        {
            return Err("stale or foreign plan approval".into());
        }
        self.ticket = None; // Consume even if cancellation/preflight later stops us.
        self.plan().cloned().ok_or_else(|| "no staged plan".into())
    }
}
