# 1790381327-an-automation-run-creates-its-worktrees-without-asking — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 8f7aef54 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Re-read and re-stamp the drifted rows in `seal/releases/0.9.1.md` and
`seal/releases/0.9.4.md` (S3, S4), with row 142's *the Agent path still asks*
re-read rather than corrected. New claims into
`seal/ledger/1790381327-an-automation-run-creates-its-worktrees-without-asking.md`.
The `changelog.md` fragment. Verified by `evidence-check` on the ledger files,
and by `rider_check.py` showing the two riders gone and nothing new.

## What this phase found

**Eight rows drifted, not the five the plan named.** `evidence-check --strict`
after phase 3 reported six in `0.9.1.md` and two in `0.9.4.md`. Besides the
`guard_worktree_creation` and `main` rows, the `judge_creation` row drifted
(phase 2 gave it the transcript argument), and so did both
`only_creates_a_worktree` rows (phase 2 corrected its docstring). Each was
re-read against the edit, its `Checked` cell set to 2026-09-26, and its hash
rewritten by `evidence-check --reverify`.

**Six claims were false, and each was corrected in place with a dated note.**

- Row 141 said this function answers `silent` on the Agent path. The Agent
  path left the function in phase 3.
- Row 142 said *with no record*, single-stream Bash still denies. With the
  `automation` answer present it allows. The plan expected this row to be
  re-read only, and it is right that *the Agent path still asks* holds. The
  premise before it did not.
- Rows 143 and 144 said the shapes outside the allow bound *fall to* or
  *answer* `ask`. With consent present they have answered `silent` since
  #257. The bound itself holds.
- Row 145 said *with no record* too. It now says *and no `automation` answer*.
- Row 146's property is about a session with no consent, and it now says so.
  Its sweep figures predate both #257 and this work, and they were not re-run.
- 0.9.4's S3 said the first creation of a session is always a question. It
  also named the unreachable branch phase 2 removed, and its note says so now.
  S4 held and was re-stamped with a Re-read note.

**The fragment turned on the records check for this work item.** A work item
with a ledger fragment is unshipped, so `evidence-check` reads its records for
backticked names the tree lacks. It found the harness payload field
permission_mode in `spec.md` and `plan.md`, and the two parameters phase 3
removed in `phases/phase-3.md`. Each line now carries `NAME NOT
IN TREE`.

**`rider_check.py`: 22 ok, 0 drifted, 0 broken.** `hooks/worktree-guard.py`
carries two riders where the release base carried four: the two this work
item answered are gone, and nothing new was added.

**`survivor-check` over `origin/release/v0.15.5...HEAD` reported six
places**, five at the phase-4 commit and a sixth once this phase's records were
committed. Each still holds, and each went into `survivors.md` with a quote and
its grounds: three docstrings of cases that pass unchanged, two passages of the
spec whose facts still hold, and a dated ledger note that a later
**Corrected** note on the same row answers.

**Mutation of the units the branch added, beyond the phase cases.**
`_clone_of` answering "" and `_content` answering `[]` each turned
`test_the_routing_preset_is_consent` red. `consent` reading the answer before
the record turned `test_the_allow_says_which_consent_it_read` red, and
dropping its record branch turned
`test_a_second_creation_in_the_same_session_is_allowed` red. The autouse
fixture in `tests/conftest.py` had nothing behind it at first: removing its
`setattr` turned nothing red, because no test session id names a real
transcript. `test_no_case_reads_the_real_projects_root` now pins it, and it
went red with the `setattr` removed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
