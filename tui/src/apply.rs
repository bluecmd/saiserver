//! One-shot staged apply. No retry, rollback, persistence, or background worker.
//! The caller owns the cancellation flag and must set it on TUI close. An already
//! sent mutation cannot be undone; its independent readback is still attempted.
use crate::{
    client::{self, Failure, Outcome, Service},
    command::{self, Command},
    config::{self, ApplyApproval, Bindings, ObjectRef, Operation, Plan, ResolvedObject, Staging},
    sai_tui::{Inventory, Object},
};
use std::{
    collections::{BTreeMap, BTreeSet},
    sync::atomic::{AtomicBool, Ordering},
};

#[derive(Debug, PartialEq, Eq)]
pub enum ApplyStatus {
    Completed,
    Rejected(String),
    Cancelled,
    Failed { step: usize, reason: String },
}
#[derive(Debug)]
pub struct StepAudit {
    /// Zero-based index in the staged plan.
    pub index: usize,
    pub command: Command,
    pub mutation_sent: bool,
    pub verified: bool,
    /// Complete independent getter/snapshot evidence, including errors.
    pub outcome: Outcome,
}
#[derive(Debug)]
pub struct ApplyReport {
    pub status: ApplyStatus,
    pub steps: Vec<StepAudit>,
    pub bindings: Bindings,
    pub inventory: Option<Inventory>,
    /// True on an incomplete apply after ANY mutation was dispatched. Even an
    /// errored mutation may have taken effect. Inspect audits; never blindly retry.
    pub partial_effects: bool,
}
impl ApplyReport {
    pub fn completed_steps(&self) -> usize {
        self.steps.iter().filter(|s| s.verified).count()
    }
    fn stop(mut self, status: ApplyStatus) -> Self {
        self.partial_effects =
            status != ApplyStatus::Completed && self.steps.iter().any(|s| s.mutation_sent);
        self.status = status;
        self
    }
}

/// Consumes approval before preflight. Each operation is dispatched at most once,
/// in order, through the existing single-command executor. No approval means zero
/// RPCs. A fresh full-plan preflight precedes the first mutation. Calling again
/// requires a new explicit approval, even after preflight failure/cancellation.
pub fn apply(
    staging: &mut Staging,
    approval: Option<ApplyApproval>,
    service: &mut impl Service,
    cancelled: &AtomicBool,
) -> ApplyReport {
    let mut report = ApplyReport {
        status: ApplyStatus::Completed,
        steps: vec![],
        bindings: Bindings::new(),
        inventory: None,
        partial_effects: false,
    };
    let plan = match staging.begin_apply(approval) {
        Ok(plan) => plan,
        Err(error) => return report.stop(ApplyStatus::Rejected(error)),
    };
    if cancelled.load(Ordering::Acquire) {
        return report.stop(ApplyStatus::Cancelled);
    }
    let inventory = match service.snapshot() {
        Ok(inventory) => inventory,
        Err(error) => {
            return report.stop(ApplyStatus::Rejected(format!(
                "plan preflight snapshot: {error:?}"
            )))
        }
    };
    report.inventory = Some(inventory.clone());
    if let Err(error) = config::validate(&plan, &inventory) {
        return report.stop(ApplyStatus::Rejected(format!("plan preflight: {error}")));
    }
    // An explicit existing reference cannot also become a newly created identity,
    // even if that object is absent from limited discovery. Retain seen create
    // keys across snapshots as well; disappearance does not make reuse safe.
    let mut claimed_keys: BTreeSet<String> = inventory
        .objects
        .as_deref()
        .unwrap_or_default()
        .iter()
        .filter_map(|o| command::key(o.kind.as_deref()?, o.key.as_deref()?).ok())
        .collect();
    for reference in plan.operations.iter().flat_map(Operation::references) {
        if let ObjectRef::Existing { oid, .. } = reference {
            claimed_keys.insert(command::oid(oid, false).expect("full prevalidation"));
        }
    }
    for (index, operation) in plan.operations.iter().enumerate() {
        if cancelled.load(Ordering::Acquire) {
            return report.stop(ApplyStatus::Cancelled);
        }
        let command = match operation.command(&report.bindings) {
            Ok(command) => command,
            Err(error) => {
                return report.stop(ApplyStatus::Failed {
                    step: index,
                    reason: error,
                })
            }
        };
        let mut guarded = GuardedService {
            service,
            cancelled,
            plan: &plan,
            command: &command,
            operation,
            bindings: &report.bindings,
            sent: false,
            before: None,
        };
        let outcome = client::execute(
            &mut guarded,
            &command,
            command::approve(&command, true).expect("validated mutation"),
        );
        let sent = guarded.sent;
        let binding = if outcome.ok {
            verified_create(
                operation,
                &outcome,
                guarded.before.as_ref(),
                &mut claimed_keys,
            )
        } else {
            Err(
                "mutation or independent readback/snapshot failed; inspect audit, do not retry"
                    .into(),
            )
        };
        let verified = binding.is_ok();
        if let Some(inventory) = &outcome.inventory {
            report.inventory = Some(inventory.clone());
        }
        report.steps.push(StepAudit {
            index,
            command,
            mutation_sent: sent,
            verified,
            outcome,
        });
        match binding {
            Ok(Some((symbol, object))) => {
                report.bindings.insert(symbol, object);
            }
            Ok(None) => (),
            Err(reason) => {
                // A cancellation gate may have prevented dispatch entirely.
                let status = if !sent && cancelled.load(Ordering::Acquire) {
                    ApplyStatus::Cancelled
                } else {
                    ApplyStatus::Failed {
                        step: index,
                        reason,
                    }
                };
                return report.stop(status);
            }
        }
    }
    report
}

fn verified_create(
    operation: &Operation,
    outcome: &Outcome,
    before: Option<&Inventory>,
    claimed_keys: &mut BTreeSet<String>,
) -> Result<Option<(String, ResolvedObject)>, String> {
    let Operation::Create { kind, bind, .. } = operation else {
        return Ok(None);
    };
    // Do not use synthetic placeholder IDs, snapshot guesses, or the executor's
    // composite-key fallback. Require the actual reply AND independent getter.
    let reply = &outcome.value["mutation"]["value"];
    let observed = &outcome.value["readback"]["value"];
    let key = reply["key"].as_str().ok_or("create reply has no key")?;
    if reply["kind"].as_str() != Some(kind)
        || observed["kind"].as_str() != Some(kind)
        || observed["key"].as_str() != Some(key)
    {
        return Err("create reply and independent getter disagree on identity".into());
    }
    let key = command::key(kind, key)?;
    if before.is_some_and(|i| {
        i.objects.as_deref().unwrap_or_default().iter().any(|o| {
            o.key
                .as_deref()
                .and_then(|k| command::key(o.kind.as_deref().unwrap_or_default(), k).ok())
                .as_ref()
                == Some(&key)
        })
    }) {
        return Err("create returned an already inventoried key; identity is ambiguous".into());
    }
    if !claimed_keys.insert(key.clone()) {
        return Err(
            "create reused an existing/reference/prior-create key; identity is ambiguous".into(),
        );
    }
    bind.as_ref()
        .map(|symbol| {
            Ok((
                symbol.clone(),
                ResolvedObject {
                    kind: kind.clone(),
                    key: command::oid(&key, false)?,
                },
            ))
        })
        .transpose()
}

/// Keep the existing pre/post getter+snapshot behavior intact, while gating the
/// actual mutation if shutdown happens during its preflight. Reads still finish
/// after dispatch, even on cancellation. Check stable ports on every snapshot.
struct GuardedService<'a, S> {
    service: &'a mut S,
    cancelled: &'a AtomicBool,
    plan: &'a Plan,
    command: &'a Command,
    operation: &'a Operation,
    bindings: &'a Bindings,
    sent: bool,
    before: Option<Inventory>,
}
impl<S: Service> GuardedService<'_, S> {
    fn dispatch(&mut self) -> Result<(), Failure> {
        if self.cancelled.load(Ordering::Acquire) {
            return Err(local_failure("apply cancelled before mutation dispatch"));
        }
        self.sent = true;
        Ok(())
    }
}
fn local_failure(message: impl Into<String>) -> Failure {
    Failure {
        category: "plan safety".into(),
        status: None,
        message: message.into(),
    }
}
impl<S: Service> Service for GuardedService<'_, S> {
    fn snapshot(&mut self) -> Result<Inventory, Failure> {
        let inventory = self.service.snapshot()?;
        config::check_ports(&self.plan.ports, &inventory).map_err(local_failure)?;
        if !self.sent {
            for reference in self.operation.references() {
                let object = reference.resolve(self.bindings).map_err(local_failure)?;
                config::check_identity(&object.kind, &object.key, &inventory)
                    .map_err(local_failure)?;
            }
            if let Some((kind, key)) = self.command.target() {
                config::check_identity(kind, key, &inventory).map_err(local_failure)?;
            }
            self.before = Some(inventory.clone());
        }
        Ok(inventory)
    }
    fn get(&mut self, kind: &str, key: &str) -> Result<Object, Failure> {
        self.service.get(kind, key)
    }
    fn create(&mut self, kind: &str, attrs: &BTreeMap<String, String>) -> Result<Object, Failure> {
        self.dispatch()?;
        self.service.create(kind, attrs)
    }
    fn set(
        &mut self,
        kind: &str,
        key: &str,
        attrs: &BTreeMap<String, String>,
    ) -> Result<Object, Failure> {
        self.dispatch()?;
        self.service.set(kind, key, attrs)
    }
    fn remove(&mut self, kind: &str, key: &str) -> Result<(), Failure> {
        self.dispatch()?;
        self.service.remove(kind, key)
    }
    fn counters(&mut self, key: &str) -> Result<BTreeMap<String, u64>, Failure> {
        self.service.counters(key)
    }
}
