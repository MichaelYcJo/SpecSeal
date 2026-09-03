# 1788411058-the-mode-is-two-shell-lines-in-a-readme — review round 2

<!-- The verifying round for round 1's fixes (target: the diff
7b00c85..e3d71b2). Eight of round 1's ten closed; two closed at the coordinate
and left the class open, and the round found four more members of it — three
created by those fixes. Round 3 verifies. Written by the review orchestrator,
which did not implement this work item. -->

| Field | Value |
|---|---|
| Target SHA | the fix diff from 7b00c85, reviewed at e3d71b2; 92fa96e is round 1's record and carries no code |
| PR | none yet |
| Broad gate | not yet — 🔴 were open |
| Fixes checked by | round-3 |
| Contract changes | `gitlinks_under_root` returns a pair → `refusals`; `install_workflow` → `switch`; `remove_workflow` → `switch`; `plugin_workflow` → `install_workflow`, `remove_workflow`; `switch` → `mode` |
| New units | `plugin_workflow`, and five test cases |
| Needs a fix | yes — 🔴 1 (`install_workflow` reports a failed `git add` as staged), 🔴 2 (the changelog fragment names `seal mode reset`, a command that does not exist), 🟡 3 (the way back leaves the workflow it wrote), 🟡 4 (`gitlinks_under_root` reads a git failure as no submodule), 🟡 5 (`switch` calls a tracked file untracked), 🟡 6 (`git reset` unstages the whole index), 🟡 7 (the both-directions conclusion is not what the workflow does), 🟡 8 (the by-hand path is hidden), 🟡 9 (three untested boundaries), 🟡 10 (the class table's row 4) |

- [ ] Pass

## What this round was asked to attack

The fixes as unreviewed code, and **whether each belongs to the class round 1
named** — a path this command touches whose guard was reasoned about a
different member. Specifically: `CONFIG_PATHSPEC` against a quoted path, a
rename line, a path with a space and the local-mode spelling; whether
`gitlinks_under_root` can miss or invent one and what it does when git fails;
every status pair against `indexed`'s three exceptions; the way back run
rather than read; the seven planted cases mutated; and both mirrors.

It was told one judgment to make rather than check: **do the fixes read as
aimed at the class or at the coordinates**, and if at the coordinates, which
member is still open.

## The judgment it was asked for

> The record aimed at the class. The code aimed at the coordinates.

`spec.md`'s *What the switch touches* table was genuinely re-enumerated — row
3b appeared and row 3 gained a condition. The code was not: three of round
1's four fixes created a new member of the same class, and one left an old
member standing.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r1 🔴 1 | the row this command wrote | `#indexed` | answered — reproduced. `M ` and `MM` still refuse. One new member: 🟡 5 | reviewer ran every status pair × `moved` × six paths: only `??`, `D `/` D` when moved, and ` M seal/config.md` pass |
| r1 🔴 2 | the way back it names | five places | **closed at the coordinate.** Four are right; the fifth became 🔴 2, and the way itself became 🟡 3 and 🟡 6 | reviewer read the fragment's bytes |
| r1 🔴 3 | the untracked workflow | `#remove_workflow` | answered, and too widely — 🟡 3 | reviewer executed the whole way back |
| r1 🔴 4 | the failed stage | `#switch` | **closed at the coordinate.** The same class stands at `install_workflow` (🔴 1) and `gitlinks_under_root` (🟡 4) | reviewer executed with an ignore rule on `.github/` |
| r1 🟡 5, 6, 7, 9 | the two rows, the fail-open check, the submodule, the header | — | answered — each reproduced, each mutant reddens | reviewer executed |
| r1 🟡 8 | the stale green conclusion | three documents | **closed at the numbers, reopened at the conclusion** — 🟡 7 | reviewer read the workflow's step order |
| r1 🟡 10 | five wide claims | five documents | answered; one narrowed too far — 🟡 8 | reviewer read each |
| 🔴 1 | `install_workflow`'s `git add` goes through `git()`, which reads a failure as `""`, and the result is discarded. An ignore rule matching `.github/` leaves the file written, nothing staged, and `wrote … and staged it` printed — then `Now commit`. The workflow never reaches the commit, so the checks never run and the switch loses what it was for. `refusals` cannot see it: an ignored path prints no porcelain line | `skills/implement/scripts/seal.py:1548` | fixed at 62805af | reviewer executed it; orchestrator reproduced with `.gitignore` holding `.github/`. The planted case reddens when the call is neutered |
| 🔴 2 | the changelog fragment — which becomes the release note — reads `seal mode reset`, a command that does not exist. Round 1's fix replaced `local` with `reset` across a line break and took the preceding `seal mode` with it. The finding was that the command named a way back that does not work; the fix named one that does not exist | `changelog.md:34-35` | fixed at 62805af | reviewer read the bytes |
| 🟡 3 | the way back leaves `.github/workflows/hygiene.yml` behind: the switch writes and stages it, `git reset` untracks it, and round 1's guard then refuses to remove it. That guard's grounds — *git holds no copy* — were reasoned about somebody else's file and applied to one this command wrote seconds earlier. Five documents say the way back walks the whole thing back | `skills/implement/scripts/seal.py:1588` | fixed at 62805af — removed when it is byte for byte what `plugin_workflow()` writes, kept otherwise | reviewer executed the whole sequence; the case now asserts the file is gone |
| 🟡 4 | `gitlinks_under_root` asks through `git()`, so a timeout or a git that is not on PATH answers *no submodule*. Every other guard in the file refuses the unanswerable question; the new one was the only one that passed it | `skills/implement/scripts/seal.py:1700` | fixed at 62805af — a pair, `None` for unreadable, and `refusals` refuses | reviewer forced the failure |
| 🟡 5 | `switch` reads `indexed`'s answer as *is this untracked*. That function has three exceptions and one means untracked, so a tracked, modified `config.md` was announced as untracked — in a note whose subject is what the index can lose. Round 1's own `Contract changes` row named both call sites and only one was opened | `skills/implement/scripts/seal.py:1812` | fixed at 62805af — `line[:2] == "??"` | reviewer executed it |
| 🟡 6 | `git reset` unstages the whole index, and the command tells a person to run it after a switch that stages two paths. Work staged anywhere else goes with it | `skills/implement/scripts/seal.py:1799`, `:1913` | fixed at 62805af — a pathspec, in both sentences and four documents | reviewer executed with `A mine.txt` staged |
| 🟡 7 | three documents say a workflow left behind fails in both directions at once. `unverified_check.py` runs second, exits 2, and nothing carries `continue-on-error` — so the job stops and `chain_check.py` never runs. Right exit codes, wrong conclusion, for the second time on the same sentence | `templates/hygiene.yml:16`, both design records | fixed at 62805af — the sentence says what the workflow does, and the case asserts it | reviewer read the step order |
| 🟡 8 | `commit-pr-convention` said the mode's row is filled by `seal mode` rather than by hand, and `templates/config.md` tells a person to edit the row and run `--apply`. Round 1 narrowed a wide claim into a false one | `skills/commit-pr-convention/SKILL.md:71` | fixed at 62805af | reviewer read both |
| 🟡 9 | three boundaries with no case: a STAGED edit to `config.md` (the property round 1 wrote into its own fix), `remove_workflow`'s `git rm` return code, and the submodule guard's reach | `tests/…` | fixed at 62805af — five cases planted, each mutation-tested | reviewer ran 35 mutations: 26 killed, 8 survived, three of them real gaps |
| 🟡 10 | the class table's row 4 did not gain the condition the commit added | `spec.md:260` | fixed at 62805af | reviewer read |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the whole way back, a second switch without reset, a resume from a by-hand `mv`, a staged file outside the root | 🟡 3, correct, correct, 🟡 6 |
| reviewer: `.gitignore` holding `.github/` or the one file | `staged it`, and `git ls-files -- .github` empty — 🔴 1 |
| reviewer: every status pair × `moved` × six paths through `indexed` | only three shapes pass; quoted paths and rename lines refuse |
| reviewer: `git()` forced to fail, against `gitlinks_under_root` | `[]` — 🟡 4 |
| reviewer: 35 mutations of the units `e3d71b2` changed | 26 killed · 8 survived · 1 not applicable |
| orchestrator: the ignore-rule stage failure, before and after | `staged it`; then the failure named with what a commit would carry |
| orchestrator: five mutations, one per fix | each reddens its own case and no other |
| orchestrator: full suite, `ruff check .`, `evidence_check --strict` | 1592 passed · 1 skipped; clean; 435 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 | `#indexed`, `#remove_workflow`, `#install_workflow`, `#gitlinks_under_root`, `#switch` | five units, every one changed in both rounds |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `chain_check.py`'s step should carry `if: always()` — which would make the old sentence true rather than the sentence follow the workflow | this record | the repository owner |
| Whether `install_workflow`/`remove_workflow`'s status string should be read by `switch` or dropped; today both callers discard it | this record | the repository owner |
| `CONFIG_PATHSPEC` uses `/` deliberately, which is git's spelling and not the platform's | the pull request's windows leg | the windows leg |
| `bin/seal`'s example list, `--check` with both roots, `config.md` as a directory | round 1's record, `questions.md` Q2, `overview.md` | the repository owner |
