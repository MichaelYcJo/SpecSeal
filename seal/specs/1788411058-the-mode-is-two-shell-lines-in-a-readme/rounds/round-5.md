# 1788411058-the-mode-is-two-shell-lines-in-a-readme — review round 5

<!-- The verifying round for round 4's fixes (target: the diff
abb6319..112b104). It found nothing needing a fix, which by the stopping rule
closes the run: a round that finds nothing leaving the root and nothing
crashing ends it. Written by the review orchestrator, which did not implement
this work item. -->

| Field | Value |
|---|---|
| Target SHA | the fix diff from abb6319, reviewed at 112b104 |
| PR | none yet |
| Broad gate | filled in at the gate's commit |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |

- [x] Pass

## What this round was asked to attack

Round 4's fix was a claim — *every command this file prints for a person to
run carries `:/`* — and the round was asked to check it is now **true and
complete**: enumerate every such string rather than only the ones round 4
named, including the shared-mode export refusal's `mv` and `git rm` block and
anything a message quotes as an example, and for each ask whether it works
from a subdirectory and under the failure its own message diagnoses. Then
whether `-f` is right on the root, and whether round 4's case passes for the
reason it names.

The prompt carried the rules directly rather than pointing at
`docs/review-handoff-protocol.md`: that section lives on `release/v0.5.0` and
this branch was cut before it merged, which round 4's prompt got wrong.

## The answer

**Nothing to open.** Eight strings, all eight executed from a subdirectory and
under their own diagnosed failure, all eight correct. The class this run met
five times is closed at the place the enumeration reaches.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r4 🟡 1 | three printed commands read from the working directory | `#install_workflow`, `#switch` | answered — reproduced. Reverting `:/` at `seal.py:1590` reddens the planted case | reviewer executed all eight strings from a subdirectory |
| r4 🟡 2 | `git add {root}` without `-f` | `skills/implement/scripts/seal.py:2000` | answered — reproduced. Reverting `-f` at `:1590` reddens | reviewer executed both under the ignore rule each message diagnoses |
| r4 🟡 3 | the second reset sentence unpinned | `tests/…` | answered — reverting `:/` there now reddens | reviewer ran the mutation |
| 🟡 1 | two of round 4's three fixes are pinned by nothing: reverting `seal.py:2000` to `git add {root}`, and `seal.py:1970`'s `:/`, both leave 76 cases green. The case round 4 planted ignores `.github/` only, so the root's own `git add` never fails and its prescription never prints. **The behaviour is right; the guard against a regression is missing** | `tests/test_the_mode_is_a_row_and_a_command.py` | deferred to `tests-todo.md` — a missing regression guard for correct behaviour is a test to plant, not a fix, and fixing it here would need a round to read it | reviewer ran five mutations; two survived |
| ❓ 2 | `git add -f :/{root}` forces past **every** ignore rule, not only the one the message diagnoses: with `seal/` and `*.zip` both ignored, a zip inside the root was staged too. Without `-f` the command does not work at all, so there is no narrower spelling | `skills/implement/scripts/seal.py:2000` | deferred — the prescription is wider than the diagnosis and there is no alternative; whether that trade is right is the owner's | reviewer executed it |
| 🟢 3 | `seal import <name>` in the export's closing line is written for the other machine, so pasting it on this one answers `is not a file` | `skills/implement/scripts/seal.py:481` | pass — not this class, and the error names the absolute path | reviewer read and executed |

## Every string this file prints for a person to paste

| Coordinate | From a subdirectory | Under its own diagnosed failure |
|---|---|---|
| `git add -f :/<workflow>` | works | stages under `.github/` ignored |
| `git rm -r --cached :/<root>` | works (128 without `:/`) | — |
| `git add -f :/<root>` | works (128 without `:/`) | stages under `<root>/` ignored |
| `git reset -- :/<root> :/<workflow>`, twice | works | — |
| the shared-mode export refusal's `git rm` and `mv` | works — both paths come from `git rev-parse` | moved to `.git/seal` from `docs/` |
| `mv "<source>" "<destination>"` | works — both absolute | — |
| `git commit` | works — no path | — |
| `seal import <name>` | written for the other machine | — |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: all eight strings enumerated and run from a subdirectory | eight correct |
| reviewer: five mutations of round 4's changes | three redden their own case, two survive — 🟡 1 |
| reviewer: `git add -f :/seal` with `seal/` and `*.zip` both ignored | a zip inside the root staged too — ❓ 2 |
| reviewer: the touched case file | 76 passed |
| orchestrator: full suite, `ruff check .`, `evidence_check --strict` | see the Broad gate row |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–4 | `#switch`, `#install_workflow`, `#remove_workflow`, `#indexed`, `#gitlinks_under_root` | five units changed in every round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Two of round 4's fixes have no regression guard | `tests-todo.md` | the next commit that opens that test file |
| `-f` forces past every ignore rule, not only the diagnosed one | this record | the repository owner |
| `:/` on a git older than 1.9.0 | the pull request's CI matrix, or a stated minimum git version | the repository owner |
| Four `git()` callers reading a failure as a success in `seal export`/`import` | issue #111 | the repository owner |
| `if: always()` on `chain_check.py`'s step; the discarded workflow status strings | round 2's record | the repository owner |
| `bin/seal`'s example list, `--check` with both roots, `config.md` as a directory, the Windows pathspec spelling | round 1's record, `questions.md` Q2, `overview.md`, the windows leg | the repository owner |
