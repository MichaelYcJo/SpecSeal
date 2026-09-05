# 1788501054-a-check-reports-clean-while-something-is-missing — review round 14

| Field | Value |
|---|---|
| Target SHA | 54819ca |
| Ran by | specseal:warden on opus |
| PR | #162, draft |
| Broad gate | `37dcaea` locally — 2100 passed · 1 failed, the repository-records case on a record cell fixed at `54819ca`; on the pull request at `54819ca`, ubuntu, macOS, ledger, lint and hygiene green and **`pytest (windows-latest, 3.12)` red** on 🔴 1. Not clear at the reviewed head; at `35fbf67` not re-taken — spent by these fixes, re-taken once the chain ends |
| Fixes checked by | nobody — written at `35fbf67`; the verifying round that opens them sets this cell |
| Contract changes | none — `resolve_patterns` and `skipped_by_narrowing` are the two changed units by AST, each body replaced by a call to `file_identity` computing the value the inline lines did; signature, arity, return type and the set of returnable values unchanged for both |
| New units | `file_identity` (depth 1) → `resolve_patterns`, `skipped_by_narrowing` |
| Needs a fix | yes — 🔴 1, the Windows leg is red at the reviewed head on one of round 13's own three cases, which asserts the POSIX answer on both platforms where Win32 collapses `..` lexically before the filesystem is consulted; 🟡 2, the printed ledger name still collapses `lnk/..` through `os.path.relpath` in four sites, so a BROKEN row is reported under a different existing file; 🟡 3, round 12's Deferred row closes a Windows question its grounds do not reach; 🟡 4, the identity rule now has two verbatim spellings against the sentence `skipped_by_narrowing` closes with |
| Loses a record or crashes | no |

- [ ] Pass

<!-- THE SAME SHAPE ONE ROUND LATER, IN THE CASE WRITTEN TO CLOSE IT. Round
12's 🔴 8 was a fix green on macOS and red on Windows; round 14's 🔴 1 is the
case for round 13's fix, green on macOS and red on Windows — §13, on the
machine that cannot remove the guarantee it rests on. Both platforms are
right about their own semantics and the checker is right on both; only the
assertion was POSIX-only.

The orchestrator had a repair in the worktree before this round posted —
uncommitted, so the target did not move — and the round read it and
declined it for a reason this file's first case already states: it derived
the expected answer from `os.path.realpath`, and *a fixture that asks for
its own expected value agrees with a broken checker*. The repair branches
on the platform and states each platform's answer instead.

One finding goes to the tracker rather than to a fix: 🟡 2 needs a new
printing helper to close, the run's exit code and row are already right, and
issue #161's first rule is that a fix pass does not add mechanism. Written
and committed before the fixes it commissions, so both fix-surface rows
start pending.

THE FIX SURFACE ABOVE is the reach-back, filled at `35fbf67`. `Contract
changes` is `none` by AST with docstrings stripped: `file_identity` is the
one unit added, `resolve_patterns` and `skipped_by_narrowing` the two
changed, and each changed body is a call computing what its inline lines
did. `file_identity` is depth 1 — extracted from `resolve_patterns`, which
predates the run, to answer a finding in it. 🟡 2 is `answered` rather
than `fixed` because nothing in this tree closes it; #163 carries the class
and the Deferred table names it. -->

## What this round was asked

The verifying round at `git diff 1380c9f..54819ca` — **three commits**, the
orchestrator's, given as a count the round re-took: 3.

Round 13 had found phase 15's `normpath` half a repair and a regression; the
fix folds by inode and returns the pattern's own spelling, with three cases
seen red first. Six things to break: what the inode fold folds and must not;
the zero-inode fallback forced; the three cases against §15 and whether exit
2 comes from the row; `Contract changes` and its reach; R13, R8 and the
fragment header; the terminal state per record and the squash. The
**platform** axis was named beside the table: what the fix rests on now.

The third found 🔴 1 — through CI rather than through a probe, because the
leg had already run at the reviewed head.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The Windows leg is red at the reviewed head on `test_the_path_returned_is_the_one_the_pattern_named`. Win32 collapses `..` lexically before the filesystem is consulted, so `x/lnk/../ledger.md` names `x/ledger.md` there — the clean ledger — and the case asserts the POSIX answer unconditionally | `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py:523` | **fixed** `35fbf67` | **Executed** — CI run 33942403876 at `54819ca`: `assert 0 == 2`, `1 failed · 2076 passed · 25 skipped`; the five other jobs green. **Orchestrator read the log**: the run printed `x\ledger.md · 1 ok` — the checker opened exactly the file Win32 says the pattern names. §13: the case rests on POSIX following the symlink before it meets the `..`, and no run on the machine that wrote it could remove that. The orchestrator's uncommitted repair derived the answer from `realpath`; declined — branch on the platform and state each answer |
| 🟡 2 | The class round 13 named is closed for the file that is **opened** and open for the file that is **named**: `main` and three other sites print `os.path.relpath(ledger, root)`, and `relpath` normalises lexically as `normpath` does | `evidence_check.py:1645`, `:1043`, `:1301`, `:1426` | answered — the run's exit and row are right, and the name a person reads is the class issue #163 carries, opened at this round's fix | **Executed** on the fix's own fixture at HEAD: header `x/ledger.md` over rows read from `<root>/ledger.md`. Exit 2 and the row are right; the name a person reads is wrong. POSIX-only. Closing it needs a printing helper — a new unit from a fix pass — so it goes to the tracker, below |
| 🟡 3 | Round 12's corrected Deferred row closes *whether `st_ino == 0` arrives on windows-latest* on grounds that do not reach it: cases that **build** a zero cannot show that one **arrives**. `overview.md:51` and the case's own docstring keep it open | `rounds/round-12.md:104` | **fixed** `35fbf67` | **Read**, three carriers compared. Round 13's 🟡 5 asked for the closure to land, not whether it was true |
| 🟡 4 | The identity rule has two verbatim spellings, nine lines each, thirty lines apart — against `skipped_by_narrowing`'s own closing sentence: *the identity rule has to have one spelling; two would be one rule today and two after the first edit to either* | `evidence_check.py:924-932`, `:1022-1030` | **fixed** `35fbf67` | **Read**; the extraction **executed** by the round, 46 passed, ruff clean. Round 13's 🔴 1 was a fix composed where a copy existed; the repair copied the rule instead of extracting it |
| 🟢 5 | §15 — the three new cases seen red | the `normpath` revert, in a clone | answered | **Executed**: `3 failed · 18 passed`, each for its stated reason |
| 🟢 6 | The returned spelling, against every lexical normalisation | mutations of `out.append(p)` | answered | **Executed**: `normpath(p)` and `abspath(p)` each kill the `..` case, `realpath(p)` kills the unstattable-ledger case. No mutation of the returned value survives |
| 🟢 7 | The inode fold folds what it must and nothing more | eight pattern shapes | answered | **Executed**: two different files stay two; a dangling symlink is returned, not swallowed, and reaches BROKEN `ledger unreadable`; hard link + target under two patterns → one, keeping the first pattern's spelling; `./seal/a.md`+`seal/a.md` → one |
| 🟢 8 | The zero-inode fallback, forced | `os.stat` faked to `st_ino = 0` | answered | **Executed**: two spellings of one file → one key; two files → two; symlink + target and case spellings → two, the declared over-reporting direction. The guard is held: dropping `and info.st_ino` from the new copy alone turns `test_an_inode_of_zero_does_not_fold_two_files_into_one` red |
| 🟢 9 | Exit 2 in the `..` case comes from the row | the fixture by hand | answered | **Executed**: `BROKEN src/service.py#gone locator not found`, one finding |
| 🟢 10 | `Contract changes` and `New units` on round 13 | `rounds/round-13.md:10-11` | answered | **Executed**, AST: `resolve_patterns` the one changed unit; exactly the three named cases added. Three call expressions across two functions; *set of returnable values* is the template's fourth trigger |
| 🟢 11 | R13, R8, the header | the fragment | answered | **Executed**: `544 ok · 1 drifted · 0 broken`, S8 alone; twelve rows counted, header says twelve; every anchor resolves |
| 🟢 12 | The terminal state per record, and the squash | a clone | answered | **Executed**: `round-14.md` with `Pass` ticked and round 13's cell set → **exit 0**; at HEAD exactly round 13's honest pair; `merge --squash 54819ca` → **290 passed**, `evidence_check .` identical |
| ❓ 13 | `questions.md` Q2, Q3, Q4 | `questions.md` | out of verified scope | **Read**, unchanged. The repository owner |

## Executed probes

| What was run | Result |
|---|---|
| `git rev-list --count 1380c9f..54819ca` | **3** |
| CI run 33942403876 at `54819ca`, windows-latest, read | `tests/…:523 assert 0 == 2` — the checker read `x\ledger.md`, which is what Win32 says the pattern names |
| the `normpath` fold restored, in a clone | **3 failed · 18 passed** |
| three mutations of the returned value | one case red each; none survives |
| eight pattern shapes; four with `st_ino` faked to 0 | 🟢 7, 🟢 8 |
| the symlink-then-`..` fixture at HEAD, by hand | header `x/ledger.md` over `BROKEN src/service.py#gone` — 🟡 2 |
| the `file_identity()` extraction, two suites | **46 passed**, ruff clean |
| `round-14.md` in a clone with round 13's cell set | **exit 0** |
| `chain_check` at HEAD, counted per record | round 13's honest pair only |
| `merge --squash 54819ca`, seven suites | **290 passed** |
| `evidence_check.py .` **unscoped** · `bin/unverified-check` · ruff on the two changed files | `544 ok · 1 drifted · 0 broken` — S8 · exit 0 · clean |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 12, 13, 14 | the Windows leg | Three consecutive fixes green on macOS and red there. The next reader asks what each new case rests on before it is committed |
| rounds 1, 13, 14 | `evidence_check.py#skipped_by_narrowing` and `#resolve_patterns` | One identity rule; round 14 found it spelled twice and this round's fix extracts it |
| round 14 | the four `relpath` print sites | The named-file half of the class, deferred to the tracker |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 2 — the printed ledger name collapses `lnk/..` through `relpath`; the run's exit and row are right, the name a person reads is not. Closing it needs a printing helper, and issue #161's first rule says a fix pass does not add mechanism | issue #163, milestone 0.8.1 | the repository owner |
| Whether `st_ino == 0` **arrives** on `windows-latest` — reopened; the leg's run showed what the checker does with a zero, not that one arrives | `rounds/round-12.md:104` corrected at `35fbf67`; `overview.md:51` as it stands | the windows CI leg, as before |
| `questions.md` Q2, Q3, Q4 · issues #158–#161 · S8 | as before | the repository owner |
