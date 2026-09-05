# 1788501054-a-check-reports-clean-while-something-is-missing — review round 15

| Field | Value |
|---|---|
| Target SHA | e1ff293 |
| Ran by | specseal:warden on opus |
| PR | #162, draft until this record is committed; returned to ready at its commit, once the pull request's own run is green |
| Broad gate | locally at the tree of this record — `e1ff293` plus the three files this commit adds: **2101 passed · 1 skipped**, `uvx ruff check` and `format --check` clean on the repository, `evidence_check.py .` unscoped `545 ok · 1 drifted · 0 broken` (S8), `chain_check` exit 0 at the commit; on the pull request at `e1ff293`, run 33944384316, **all six jobs green including `pytest (windows-latest, 3.12)`** — the platform half of round 14's 🔴 1, answered; at this record's own commit, carried by the orchestrator before `gh pr ready` |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

<!-- THE RUN ENDS HERE. Round 14's four findings are closed on this round's
own grounds, and the one thing this round found — a record cell CI refused
at `2972528` — was fixed by the orchestrator at `e1ff293` inside this
round's own target, so this round read the fix rather than commissioning
one. Nothing after this record closes on a fix; the cell above says so and
`chain_check` counts it as the terminal record.

The one cell that could be read two ways is 🔴 5's verdict. It is
`answered`, not `fixed`: `fixed` would make this a record that wrote fixes,
which the floor then walks past looking for a verifying round that does not
exist. The fix is in the diff this round was given (`7beb9cc..e1ff293`,
three commits), it was executed in a clone on both sides, and CI at
`e1ff293` is green on the case that refused it. A round that verified a fix
already in its target has no fixes of its own to check.

Three times on this branch a parsed cell held prose punctuation the parser
read as structure — round 4's cell, round 13's semicolon, round 14's comma —
and each time the local `chain_check` had been run at HEAD before the record
was committed, so it never saw the cell. The check that would have caught
all three is one more `chain_check` after the record commit, and the
inherited-coordinates table says so for the next reader. -->

## What this round was asked

The verifying round at `git diff 7beb9cc..e1ff293` — **three commits**,
the orchestrator's, given as two and re-taken as three after the target
moved mid-round: `35fbf67` the fixes, `2972528` the records, `e1ff293` one
record cell.

Round 14 had found the case for round 13's fix asserting the POSIX answer
on both platforms, the identity rule spelled twice, round 12's Deferred
row closing a Windows question on grounds that do not reach it, and the
printed ledger name still collapsing `lnk/..` through `relpath`. The job:
for each verdict round 14 recorded as `fixed` or `answered`, is it closed
on this round's grounds — with `file_identity`, the one unit the fixes
added, a finding surface reviewed by nobody. Six things to break: the
per-platform assertion and its predicate; `file_identity` as code — guard,
fallback, dangling links, directories, non-`OSError` failures — and
whether a third spelling fold survives anywhere in the file (§12); round
12's row against `overview.md:51` and the case docstring; whether #163
names the class completely; `Contract changes: none` by AST and the depth;
the ledger, the terminal state per record and the squash. Axes named
beside the table: **platform**, **identity**.

Mid-round the orchestrator sent the moved target and what moved it: CI at
`2972528` had refused round 14's `New units` cell.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 1 | Round 14's 🔴 1 — the third case asserted the POSIX answer on both platforms | `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:540-560` | answered — closed at `35fbf67` | **Executed**, the POSIX branch: the case alone passes; `out.append(p)` mutated to `normpath(p)` or `abspath(p)` turns this case alone red (1 failed · 20 passed). **Read**, the Windows branch, against the leg's own log at run 33942403876: `x\ledger.md` · `total: 1 ok · 0 drifted · 0 broken` · exit 0 — the three things the branch asserts are the three things the log shows, and it rests on nothing else. **Executed by CI, read by the round**: at `2972528` the leg reported `1 failed · 2076 passed · 25 skipped` with the one failure the records case, and the skip count equal to `54819ca`'s, so this case ran there and passed; at `e1ff293` (run 33944384316) the leg is green, carried by the orchestrator. `os.name == "nt"` is the predicate the matrix runs (`test.yml`, native CPython on windows-latest); a POSIX-emulation Python answers `posix` and follows the symlink before the `..`, so the POSIX branch is right there, and it is not a platform this repository runs. The symlink-refused skip precedes the branch |
| 🟢 2 | Round 14's 🟡 4 — the identity rule spelled twice | `evidence_check.py#file_identity`, `#resolve_patterns`, `#skipped_by_narrowing` | answered — closed at `35fbf67` | **Executed**, AST with docstrings stripped, `7beb9cc` against `e1ff293`: `file_identity` added, `resolve_patterns` and `skipped_by_narrowing` changed, nothing removed, both signatures and return expressions unchanged. Twelve mutations, narrowed suite of 21: the `st_ino` guard dropped → `test_an_inode_of_zero_does_not_fold_two_files_into_one` alone red; the device dropped → the two-devices case alone; the `OSError` guard dropped → the unstattable case alone; the return normalised three ways → one case each; the key on the raw string → 3 red, on `normpath` → 2 red. **Read** §12: every `normcase`/`normpath`/`realpath`/`abspath` in the file opened — the locator's inside-the-repository check, the plugin-path check, the fallback itself, the CLI arguments — and none is a third fold on a ledger's identity. The dict comprehension keeps the loop's order, keys and values; a path in both `read` and the candidates is stat'd twice as before |
| 🟢 3 | Round 14's 🟡 3 — round 12's Deferred row closed the `st_ino` question on a built zero | `rounds/round-12.md:104` | answered — closed at `35fbf67` | **Read**, three carriers compared: `round-12.md:104` (open, the windows CI leg named), `overview.md:51` (the same sentence), the case's own docstring at `tests/…:229-231` (*whether a zero actually arrives on windows-latest is the CI leg's to answer*). One statement in three places |
| 🟢 4 | Round 14's 🟡 2 — the printed ledger name collapses `lnk/..` through `relpath` | `evidence_check.py:1056`, `:1314`, `:1439`, `:1658` | answered — nothing in the tree closes it and #163 carries it | **Read** #163: the four sites, the helper, the case and §15 are named, so `answered` is the verdict for a finding a fix pass declines on #161's first rule. **Read** §12: six `relpath(` calls in the file, not four. `:627` builds the locator scan's file list and is not a ledger name. **`:1625` prints the ledgers a narrowed run skipped and is in the class by shape** — a ledger path turned into a name for a person — and cannot mis-name today: its input is `default_patterns(root)` with `root` already `abspath`'d, so no `..` reaches it. One comment on #163, not a change — Deferred |
| 🔴 5 | Round 14's `New units` cell at `2972528` — `→ resolve_patterns, skipped_by_narrowing` — holds a comma, and the row's grammar reads a comma under one `(depth N)` as a second unit. The release job errored and every pytest leg failed on `test_this_repositorys_own_round_records_pass_the_per_record_checks` | `rounds/round-14.md:11` | answered — found by CI at `2972528`, fixed by the orchestrator at `e1ff293` inside this round's target, verified by this round | **Executed by CI, read by the round**: run 33943886862 `##[error] New units lists …`; run 33943886848, ubuntu `1 failed · 2099 passed`, the same case on all three legs. **Executed** in a clone at `2972528`: the case red; `chain_check` prints a third line on round 14 beyond its honest pair; the terminal state with a `round-15.md` laid on top → **exit 1**. Two spellings of the cell tried before the fix landed — `(depth 1)` alone, and the arrow tail without a comma — each passed the case and gave the terminal state exit 0; `e1ff293` is the second. **Executed** at `e1ff293`: 47 passed with the records case; `chain_check` prints exactly round 14's honest pair; the terminal state → **exit 0**; CI green. §12 **read**: round 14's is the one `New units` cell in this work item with a comma outside the depth marker; other work items' comma cells predate `DEPTH_FROM` and print. The orchestrator's own diagnosis holds — the local `chain_check` before the record commit read HEAD and never saw the cell — and neither `phase-17.md` nor `plan.md` row 17 claims a count at the record commit |
| 🟢 6 | `file_identity` as code — the finding surface | `evidence_check.py:895-918` | answered | **Executed**, a probe deleted after: a file, `./`, absolute, symlink and hard link → one identity; a directory → its inode (and `read()` then answers None → BROKEN `ledger unreadable`, as before); a dangling symlink and a missing path → the absolute spelling; **two dangling links to one missing target stay two** — `abspath` keeps them apart where `realpath` would fold them and swallow one. A NUL byte raises `ValueError` and a non-string `TypeError`, neither an `OSError`, and neither reaches it: `glob` returns only strings `lexists` is true for, and `--ledger` values are strings. Two mutations survive: `normcase` removed from the fallback — recorded in R3 and R10, unkillable off Windows; and **the fallback replaced by `realpath` — a new survivor**. The current code is the safe direction, so this is a case to plant, not a fix — `tests-todo.md` |
| 🟢 7 | `New units: file_identity (depth 1)` — the depth | `rounds/round-14.md:11` | answered | **Read** `templates/sdd-round.md:104-107`: depth 1 is a unit added to answer a finding in code that predates the run. 🟡 4's coordinates are `resolve_patterns` (predates the run) and `skipped_by_narrowing` (this work item's build phase, not a fix pass's unit) |
| 🟢 8 | The ledger — four anchors, the unscoped read | the fragment, R3, R8, R10, R13 | answered | **Executed**, a word-level diff of the fragment: three anchors moved (`skipped_by_narrowing` 3fa0838e→91696b61, `resolve_patterns` 275df75d→4ecfd731, the third case 73b87f97→3a33c35a) and one added (`file_identity@e8a4f000`, R3 and R13) — four, as the record says. `evidence_check.py .` unscoped at `2972528`, at `e1ff293` and on the squash: **`545 ok · 1 drifted · 0 broken`**, the drifted row S8 alone. `--reverify` was not run |
| 🟢 9 | The squash, and the suites | a `--no-local` clone, `origin/release/v0.8.0` + `merge --squash e1ff293` | answered | **Executed**: no conflict; thirteen suites — the two code suites, ten records suites and `test_no_real_identifiers` — **507 passed**; ruff check and format clean on the two changed files; `phase-17.md` and `plan.md` row 17 match the diff (**read**) |
| ❓ 10 | `questions.md` Q2, Q3, Q4 · S8 | `questions.md` | out of verified scope | **Read**, unchanged. The repository owner |

## Executed probes

| What was run | Result |
|---|---|
| `git rev-list --count 7beb9cc..e1ff293` · `git diff 2972528..e1ff293` | **3** · one line of `round-14.md` |
| the two code suites at `2972528`, at `e1ff293` with the records case | 46 passed · 47 passed |
| twelve mutations of `evidence_check.py`, the narrowed suite of 21 | ten kill exactly the case they should; `normcase` out of the fallback → 21 passed (recorded); **fallback as `realpath` → 21 passed** (new — 🟢 6) |
| `file_identity` by hand, `test_tmp_file_identity.py`, deleted | 🟢 6 |
| AST `7beb9cc` vs `2972528` vs `e1ff293`, docstrings stripped | one added, two changed, none removed; signatures and returns unchanged |
| `test_this_repositorys_own_round_records_pass_the_per_record_checks` at `2972528` / `e1ff293` | **1 failed** / 1 passed |
| `chain_check --baseline origin/release/v0.8.0` at `2972528` / `e1ff293`, per record | three lines on round 14 / **exactly its honest pair** |
| the terminal state — `round-15.md` with `no fixes to check` · `no` · `Pass` ticked, round 14's cell set to `round-15` — at `2972528` / `e1ff293` | **exit 1** / **exit 0** |
| `merge --squash e1ff293` onto the base, thirteen suites · `evidence_check.py .` unscoped | **507 passed** · `545 ok · 1 drifted · 0 broken` |
| ruff check · format --check on the two changed files | clean · already formatted |
| CI logs read: 33942403876 (`54819ca`, windows) · 33943886848 and 33943886862 (`2972528`) · 33944384316 (`e1ff293`) | 🟢 1's Windows output · the records case on three legs and the hygiene error · six green, by the orchestrator |
| the `:1625` site's input and the `realpath` survivor, **re-taken by the orchestrator** before this record | `default_patterns(root)` over an `abspath`'d root, no `..` possible; two dangling links to one target → 2 identities under `abspath`, 1 under `realpath` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 12–15 | the Windows leg | Three consecutive fixes green here and red there; this round's Windows branch is the first written from the leg's own output, and the leg at `e1ff293` is green |
| rounds 1, 13, 14, 15 | `evidence_check.py#file_identity`, `#resolve_patterns`, `#skipped_by_narrowing` | One rule, one spelling, two readers. The next reader opens the fallback with the `realpath` case from `tests-todo.md` planted |
| rounds 4, 13, 14, 15 | a parsed cell's punctuation — `chain_check.py#depth_problems`, `docs/review-chain-spec.md` | Three times on this branch, each after a `chain_check` at HEAD before the record commit. Run it once more after the record is committed |
| rounds 14, 15 | the `relpath` print sites — five by shape | #163, with one site to add to its enumeration |

## Regression tests to plant

`tests-todo.md`, one row: the `realpath` survivor — two dangling links to one missing target must be named twice, seen red with the fallback as `realpath` first.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| #163's enumeration is one site short by shape: `evidence_check.py:1625` names skipped ledgers to a person too, and cannot mis-name today because its input carries no `..`. The helper either takes that site or the issue says why not | a comment on issue #163, posted at this record | the repository owner |
| `root = os.path.abspath(args.root)` collapses `--root x/lnk/..` lexically — a root argument, not a ledger path, outside #163's class and older than this branch | the same comment on #163 | the repository owner |
| The `realpath` survivor in `file_identity`'s fallback — safe direction today, unpinned | `tests-todo.md` | the next fix pass on this file, or 0.8.1 |
| Whether `st_ino == 0` arrives on `windows-latest` · `questions.md` Q2, Q3, Q4 · S8 · issues #158–#161, #163 | as before | the windows CI leg · the repository owner |
