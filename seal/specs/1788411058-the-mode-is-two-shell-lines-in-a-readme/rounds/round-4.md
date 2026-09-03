# 1788411058-the-mode-is-two-shell-lines-in-a-readme — review round 4

<!-- The verifying round for round 3's fixes (target: the diff
62805af..abb6319). Round 3's three fixes all hold. The round found a fifth
member of the class — three more printed commands read from the working
directory — and nothing that leaves the root or crashes. Round 5 reads these
fixes and, by the stopping rule, ends the run. Written by the review
orchestrator, which did not implement this work item. -->

| Field | Value |
|---|---|
| Target SHA | the fix diff from 62805af, reviewed at abb6319 |
| PR | none yet |
| Broad gate | 112b104 — `pytest tests/ -q -n auto` 1596 passed · 1 skipped; `ruff check .` clean; `evidence_check.py --strict .` 435 ok · 0 drifted · 0 broken |
| Fixes checked by | round-5 |
| Contract changes | none — three printed strings and one flag |
| New units | one test case |
| Needs a fix | yes — 🟡 1 (three printed recovery commands are read from the working directory), 🟡 2 (`git add seal` fails under the ignore rule its own message diagnoses), 🟡 3 (the second `git reset` sentence was pinned by nothing) |

- [x] Pass

## What this round was asked to attack

One question, for the fourth time: **did round 3's fixes create a fifth member
of the class** — a path this command touches whose guard was reasoned about a
different member? Named to look at: `:/` itself against a linked worktree, a
`GIT_WORK_TREE`, a nested repository, an old git, and a path that does not
exist; **every command string this file prints for a person to run**, checked
from a subdirectory; and whether the three new cases pass for the reason they
name.

The round was also told the stopping rule: finding nothing that leaves the
root and nothing that crashes ends the run.

**One instruction in that prompt was wrong.** It pointed at
`docs/review-handoff-protocol.md` §*What every spawn prompt carries*, which
exists on `release/v0.5.0` and not on this branch — this branch was cut before
that pull request merged. The reviewer read the sections that are there and
said so, which is the right handling; the orchestrator sent a coordinate it
had not checked against the tree under review.

## The answer

Yes, and it is the smallest one yet. Round 3 gave `:/` to the two `git reset`
sentences. The same file prints three more commands for a person to run, and
all three stayed relative — `git add -f <workflow>`, `git rm -r --cached
<root>`, `git add <root>`. From a subdirectory each exits 128 with `did not
match any files`.

All three are **recovery** lines, handed over after something has already
failed. The third also lacked `-f`, so it failed at the repository root too,
under the very ignore rule the message beside it diagnoses.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r3 🔴 1 | the pathspec from a subdirectory | two sentences | answered — reproduced. `:/` holds in a linked worktree (resolving to that worktree's top, leaving the main one alone), under `GIT_WORK_TREE`, in a nested repository, and for a path that does not exist | reviewer executed six shapes on git 2.50.1 |
| r3 🟡 2 | two empty cases | `tests/…` | answered — each new case reddens for its own reason and touches no other | reviewer ran three mutations |
| r3 🟡 3 | the version-mismatch message | `#remove_workflow` | answered | reviewer read |
| 🟡 1 | three printed recovery commands are read from the working directory and exit 128 from a subdirectory. Round 3's own explanation — *a git pathspec is read from where you stand* — stands three lines above one of them in the same output | `skills/implement/scripts/seal.py:1590`, `:1969`, `:1999` | fixed at 112b104 — `:/` on all three, and the reason stated once rather than implied twice | reviewer executed each, reaching `:1969` by holding `.git/index.lock`. The planted case runs the printed command from the subdirectory it was printed in |
| 🟡 2 | `git add seal` is named after diagnosing an ignore rule matching the root, and fails at the root under that rule. The message beside it, for the same failure on the workflow's path, has carried `-f` since it was written | `skills/implement/scripts/seal.py:1999` | fixed at 112b104 | reviewer executed both spellings |
| 🟡 3 | the subdirectory case runs the FIRST reset sentence and asserts `":/" in out`, which the first sentence satisfies alone — so removing `:/` from the second survived every case in the file | `tests/…:284` | fixed at 112b104 — both sentences counted and both required to carry it | reviewer's mutation survived; the orchestrator's now reddens |
| 🟢 4 | `:/` on a git without the magic prefix (before 1.9.0, 2014) | — | not judged — only 2.50.1 was available. Deferred | reviewer said so plainly |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: three mutations of round 3's fixes | each reddens its own case, nothing else |
| reviewer: `:/` across six repository shapes | correct in all six |
| reviewer: the three printed commands from a subdirectory | 128, 128, 128 |
| reviewer: `git add seal` at the root under its own diagnosed ignore rule | exit 1 |
| reviewer: removing `:/` from the second reset sentence | survived all 75 cases |
| orchestrator: two mutations, one per fix | each reddens its own case |
| orchestrator: full suite, `ruff check .`, `evidence_check --strict` | 1596 passed · 1 skipped; clean; 435 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–3 | `#switch`, `#install_workflow`, `#remove_workflow`, `#indexed`, `#gitlinks_under_root` | five units changed in every round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `:/` on a git older than 1.9.0 | the pull request's CI matrix, or a stated minimum git version | the repository owner |
| Four `git()` callers that read a failure as a success in `seal export`/`import` | issue #111 | the repository owner |
| Whether `chain_check.py`'s step should carry `if: always()`; whether the workflow status strings should be read or dropped | round 2's record | the repository owner |
| `bin/seal`'s example list, `--check` with both roots, `config.md` as a directory, the Windows pathspec spelling | round 1's record, `questions.md` Q2, `overview.md`, the windows leg | the repository owner |
