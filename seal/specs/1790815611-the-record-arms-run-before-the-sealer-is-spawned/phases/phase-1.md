# 1790815611-the-record-arms-run-before-the-sealer-is-spawned — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 3f4c34a6 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and no model; the orchestrating session fills this row |

## What this phase was asked

`--preflight` in `skills/verify/scripts/broad_gate.py`: the branch in
`gate()`, the `--record` refusal, the verdict lines, the docstring and the
usage line; cases S1, S2, S3, S4 and S6 in
`tests/test_the_seal_is_taken_once_by_the_sealer.py`, each seen red first.
S5 holds by the three AST-reading cases staying green unchanged. Q4 — where
the preflight's first line lives — is this phase's to decide. A sibling
branch (`feat/666-…`, work item 1790815615) edits the same file, so the
hunks stay in `gate`, `main` and the docstring.

## What this phase found

**The frame holds, and one coordinate in the ticket does not.** #638 places
the sealer's spawn in a section called *The last record's `Broad gate` cell
is read at a READY pull request (#295)*. That is a bold paragraph lead inside
§*Orchestrator: the pull request opens before round 1, and a phase is re-run*
of `skills/code-review/orchestration.md`, which is the section `spec.md`
names, so the spec is right and the ticket's name is a paragraph's.
`skills/verify/SKILL.md` §*The broad gate* cites the same bold lead as a
section (`§*The last record's `Broad gate` cell is read at a READY pull
request*`). That reference predates this branch and is not edited here.

**Q4 is answered (b'), a third shape: the head is replaced in `gate()`, and
`seal_stamp.py` is untouched.** The plan's default was (a), a `head` keyword
on `seal_stamp.not_sealed`. 1790815615's own `plan.md`, phase 1, changes
`not_sealed`'s head and its arguments (*`not_sealed` takes the names*), so a
keyword added to that function here would collide with the sibling inside
the same function body. The preflight therefore calls `not_sealed` exactly
once, at the call site that already exists, and replaces the form's first
line with `preflight_line(PREFLIGHT_FAILED, …)`. The per-check lines are
still `not_sealed`'s, so the failure words live in one place, which was the
reason given for (a). The cost: it assumes the head is the form's first line
and is one line. S3 pins both, because it asserts that stdout opens with the
preflight's head and that no line begins `NOT SEALED`.

**S1's arm list is read from `gate()`'s syntax tree in source order, not
from `PARTITION`.** `PARTITION` carries no `ledger` arm, because the ledger
mirrors no workflow step. A list derived from it would miss the first record
arm, and a typed list would agree with the preflight in the plan's failure
scenario. `record_arms()` reads every `checks[...] = run(...)` in `gate()`,
sorts by line and drops `SUITE`. Mutation M8 moves `mode` under the row's
condition, which is that failure scenario, and S1 goes red on it.

**The coverage line had no case.** The spec drops it from a preflight, and
every fixture here has no workflow, so nothing pinned it. A seventh case
copies this repository's `hygiene.yml` into the fixture and asserts that the
full run prints `this seal answers` and the preflight does not. Mutation M4
turns it red.

**Two in-process cases build `argparse.Namespace` by hand** and had no
`preflight` attribute. Both gained `preflight=False` rather than the gate
reading the flag through `getattr`, so a caller that forgets it fails loudly.

**The kept output also holds `draft-event.json`**, which `draft_env` writes
for the chain arm. S1 compares the `.txt` files alone.

Seen red, all executed in this worktree: the six cases against the unedited
gate (argparse refuses `--preflight`; S4 and S6 by their sentences, because
the exit code alone would have matched), then eleven mutations each turned
at least one case red, restored from bytes kept before the first and with
both `__pycache__` directories cleared between them: M1 the row runs, M2
`--record` not refused, M3 the row line loses its suffix, M4 the coverage
line prints, M5 the head reads `NOT SEALED`, M6 no early return, M7 the line
loses its tail, M8 an arm moves under the row's condition, T1 `record_arms`
keeps the row, and T2 `no_seal_line` asked directly with `SEALED` and with
`NOT SEALED` lines.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
