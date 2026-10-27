# Handover: Seastone 2 switch presets (goal mvqt0lpg-p4imap)

Read this before doing anything else. All work is in **managed worktrees**;
the shared checkout `/home/bluecmd/saiserver` has other agents' uncommitted work
and must not be touched.

## Ground rules from the user

- Work ONLY in worktrees; PR only after explicit user approval. Nothing pushed.
- Sub-agents must use **OpenAI providers only** (`openai/gpt-6-astra`; Anthropic
  OAuth refresh is broken; claude-bridge hit a usage limit).
- Decisions already made: operational ARP/ND replies required (not
  metadata-only); ERSPAN collector IP `192.0.2.2` with static example MAC
  `02:00:00:00:00:02`; platform map = stock `Seastone_2` HWSKU from
  `ixp-lab-sw2` (NOT its active `SONIX` breakout SKU).

## Branches (all base 59d36d60 unless noted; base SHA 59d36d60b45f8d383...)

| Branch / worktree | State | Contents |
| --- | --- | --- |
| `feat/seastone2-switch-presets` → `/home/bluecmd/.herdr/worktrees/saiserver/feat-seastone2-switch-presets` | **main feature branch, clean, 10 commits** | Rust TUI presets (presets.rs, preset_plan.rs, config.rs, apply.rs, UI `p`/`a` workflow), ERSPAN+MAC/TCP ACL backend (`cherry-pick 1147ade`), interface_address backend (`cherry-pick 2777fad`), client schema extensions, docs, evidence, PTY tests |
| `feat/seastone2-preset-api` (w15) | 1 commit `1147ade`, already cherry-picked | src/tui_rpc.cpp mirror_session + ACL extensions. **CANDIDATE FOR REMOVAL after handover verification** |
| `feat/switch-preset-staging` (w16) | 1 commit `bef3ee2`, already cherry-picked | config.rs/apply.rs staging+apply. **CANDIDATE FOR REMOVAL** |
| `feat/seastone2-interface-address` (w17) | 1 commit `2777fad`, already cherry-picked | interface_address backend. **CANDIDATE FOR REMOVAL** |
| `feat/seastone2-address-integration` (w1A) → `/home/bluecmd/.herdr/worktrees/saiserver/feat-seastone2-address-integration` | **DIRTY, 0 commits, uncommitted** | Server integration: saiserver.cpp CLI/startup/callback registration, tui_rpc `interface_address` kind + snapshot attrs (`preset_api`, `interface_address_backend`), dynamic-loader wrapper additions, legacy RPC gating (bounded-only), Makefile, tests (startup_test, interface_address_rpc_test, dynamic_run.sh, fake_optional_sai), docs/server-api.md. **Tests pass but nothing is committed** |

## Test evidence (all offline; NO hardware)

Feature worktree:
- `cargo test --manifest-path tui/Cargo.toml --locked` → 56 Rust tests pass
- `cargo clippy --locked --all-targets -- -D warnings`, `cargo fmt --check` → clean
- `python3 tui/tests/preset_terminal_smoke.py tui/target/debug/sai-tui` → 5 pass (real PTY: load/cancel/apply-review send only ONE read-only snapshot RPC)
- `SAI_HEADER_DIR=/home/bluecmd/saiserver/.lab/sai/inc EXTRA_CPPFLAGS=-I/opt/linuxbrew/.linuxbrew/include EXTRA_LDFLAGS='-L/opt/linuxbrew/.linuxbrew/lib -Wl,-rpath,/opt/linuxbrew/.linuxbrew/lib' tests/server/run.sh` → PASS (includes ERSPAN/mirror/ACL)
- `SAI_HEADER_DIR=... tests/server/interface_address_run.sh` → PASS (pure packet + fake SAI)
- `./tests/test_fdb_events.sh` (with `CPATH=/opt/linuxbrew/.linuxbrew/include:/home/bluecmd/saiserver/.lab/sai/experimental`) → PASS
- Independent OpenAI review of planner found 2 issues (forwarding-before-ACL, disabled reused bridge port) → fixed in b0e5ac0, verified by follow-up review.

Integration worktree (w1A, all pass, exit 0):
- `tests/server/run.sh` (extended), `tests/server/interface_address_run.sh`,
  `tests/server/dynamic_run.sh` — startup/shutdown/callback/CLI/gating/fault/cleanup.

## Remaining work (ordered)

1. **Review + commit w1A integration** (highest priority, uncommitted).
   `cd .../feat-seastone2-address-integration`; review the diff (13 modified +
   5 new files, ~600 lines); verify `preset_api=1`/`interface_address_backend`
   snapshot attrs match what `preset_plan.rs` requires; commit on its branch
   with a message like "Integrate interface-address responder into saiserver".
2. **Cherry-pick that commit** into `feat/seastone2-switch-presets`, then run the
   FULL verification matrix above (Rust + clippy + fmt + PTY + all three
   shell-based server tests + fdb events). Fix any conflict.
3. **Check UI/preset wiring vs integrated server**: preset plan requires switch
   attrs `preset_api=1` and `interface_address_backend=enabled`; integration
   emits them. Confirm `interface_address` kind works end-to-end in the PTY
   snapshot flow if cheap; otherwise rely on `interface_address_rpc_test`.
4. **verify-document task** (goal task 4): finish docs/server-api.md
   cross-check, confirm docs/tui.md + docs/switch-presets.md are consistent with
   the final CLI flags (`--enable-interface-address`-style opt-in, static IPv6
   no-DAD ack, policer/software-admission ack). No new features.
5. **Update goal tasks** (`update_goal_task`): `seastone-preset` → complete once
   step 2 is green; `verify-document` → complete with evidence list.
6. **Cleanup**: after branch is green, `worktree_remove` w14, w15, w16, w17
   (their commits are already cherry-picked). Keep w1A until its commit is
   cherry-picked and verified. Branches are never deleted by removal.
7. **PR**: only after user approval. Push `feat/seastone2-switch-presets`,
   open PR to the repo's default branch (check `git remote -v`; if no remote
   push access, tell the user). Body should summarize: preset loading/apply
   safety model, Seastone 2 recipe (33 ports, VLANs 101–132, 65 addresses,
   ERSPAN egress on 32 ports, 4 independent denies, tagged-ingress drop,
   ports disabled until policy verified), interface-address responder
   (opt-in, static IPv6 no-DAD), verification evidence, and explicit
   "hardware behavior NOT verified" statements.

## Hard blockers / not done

- No hardware/lab testing (not authorized); ERSPAN wire format, ARP/ND replies,
  and SDK callback tag preservation are unverified on the Seastone 2 SDK.
- Sanitizers unavailable in this environment (missing libasan/libz3) — recorded
  by the api subagent; do not claim sanitizer runs.
- Stock HWSKU must be selected via separate SONiC maintenance on the switch;
  preset correctly rejects the active SONIX breakout (36 ports).

## If resuming in a new harness

- Goal: `mvqt0lpg-p4imap` (use `/goal-resume` if paused; it is currently running).
- Session continuity is not needed; HANDOVER.md + this file + branch history are
  the state. Start from step 1.
- Never modify `/home/bluecmd/saiserver` working tree (other agents' files:
  .gitignore, bazel files are dirty there and are NOT ours).
