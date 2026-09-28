# 1790635415-a-gate-that-fails-to-load-says-so — phase 1

<!-- seal/specs/1790635415-a-gate-that-fails-to-load-says-so/phases/phase-1.md -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | ef25f83d |
| Ran by | unknown — the spawn prompt did not hand this value over, and the template forbids a segment to source it from its own idea of what it is; the orchestrator fills it |

## What this phase was asked

Build `plan.md`'s Phase 1: a broken gate is said at turn end. `run_gate`
reports a load or run failure; `dispatch.py` writes the `.pending` record
(opt-in, session, exclusive create, `basename`d parts); the `stop` group
claims and says each pending record once, as the whole `systemMessage` when
the group printed nothing. Covers S1–S5, S8, S11, S12 and S13. S1 is seen red
against the unchanged `dispatch.py` before anything else is written, and
S11's two existing cases pass unedited. The spawn also said to stay out of
`evidence_check.py` (work item A, #585) and `hooks/config.py` and the
fence/comment readers (work item B, #584).

## What this phase found

- **The frame does not hold on one point, and it is `run_gate`'s return
  shape.** `plan.md` §*Technical context* says `run_gate` "will also return
  what failed" and that `main()` is its only caller, which the plan asked the
  work to confirm with a grep. `main()` is its only caller. But
  `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py#test_the_stop_group_reports_the_stop_event`
  monkeypatches `run_gate` with `lambda _gate, _payload: decision`, a function
  returning a string. So the return shape stays a gate's stdout, and a
  failure leaves `run_gate` through a module-level list, `dispatch.FAILED`,
  which `main()` clears at the start of each call and reads after the merge.
  No existing case was edited to make room.
- **The report path imports nothing under `hooks/` except `optin.py`, and
  that one is loaded by file path inside a guard.** `opted_in` catches
  `(Exception, SystemExit)` around the load and the call, and answers True,
  "cannot tell". It asks `optin.home_at(top, common)` rather than
  `optin.opted_in(cwd)`, because the caller already holds the toplevel and
  the common dir, so a main checkout pays no `git` process for the answer.
- **The opt-in is asked only for a gate not yet written down.** A gate that
  stays broken fails on every call, so after its first record the cost of a
  failing call is two `stat`s per failing gate, and `optin.py` is not loaded
  again.
- **S13's baseline could not be "the same call under another session".**
  `mode-gate.py` denies the first call of a session in a repository whose
  `seal/config.md` records no mode, so two calls under different ids differ
  on that gate's state. Each comparison in S13 and S2 is made against a copy
  of `hooks/` with the broken gate REMOVED rather than broken, which is also
  a failure, and so also recorded, and so a like-for-like comparison.
- **The PostToolUse format hook removed `import subprocess`** from
  `dispatch.py` when the first edit added it before any code used it, and no
  phase-1 case reached the linked-worktree branch of `common_dir`, the only
  code that uses it. `ruff check` found it before the commit. Phase 2's twin
  case now reaches that branch.
- **Wording (Q3), as built.** Line 1 is `SpecSeal: <n> gate(s) failed and
  was/were skipped`. Each gate's line is `<gate> failed to load in <group>
  (<Error>: <first line>); calls went ahead without it, and the other gates
  in <group> still decided.`, with `failed while running` for a run
  failure, and the last clause dropped for a group of one gate (`stop`,
  `pre-skill`, `post-agent`), where there are no other gates to have decided.
  The closing line is `Nothing was blocked, and each gate is said once per
  session. Updating or reinstalling the plugin usually repairs it.` A record
  whose body cannot be read still names its gate: `<gate> failed; calls went
  ahead without it.`
- **S1 went red at its first assertion, the record's absence**, before it
  reached `stop`. The `stop` half of the claim ("prints nothing") was true of
  that tree as well, since there was nothing for it to read.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
