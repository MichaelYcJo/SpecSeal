# 1788501054-a-check-reports-clean-while-something-is-missing — review round 13

| Field | Value |
|---|---|
| Target SHA | c590961 |
| Ran by | specseal:warden on opus |
| PR | #162, draft since 🔴 8 arrived; returned to ready when the last record's `Pass` is ticked |
| Broad gate | `e48d682` locally (2097 passed · 0 failed); on the pull request at `c590961`, **all six jobs green including `pytest (windows-latest, 3.12)`** — the platform half of round 12's 🔴 8, answered. Spent by 🔴 1's fix and re-taken after it |
| Fixes checked by | nobody — this round's fixes are not yet written; the round that opens them sets this cell |
| Contract changes | `resolve_patterns` — the spelling it returns changed, from a normalized one to the pattern's own → `main`, `skipped_by_narrowing` |
| New units | `test_one_file_matched_under_two_cases_is_read_once` (depth 1) → pytest only; `test_a_symlink_and_a_hard_link_to_a_ledger_are_that_ledger` (depth 1) → pytest only; `test_the_path_returned_is_the_one_the_pattern_named` (depth 1) → pytest only |
| Needs a fix | yes — 🔴 1, `os.path.normpath` in `resolve_patterns` collapses `lnk/..` lexically and so returns a path naming a different file than the pattern matched, and the checker opens that path — a ledger with a broken row goes unread and the run exits 0; 🟡 2, the class is half closed — case, symlink and hard link still count one file twice; 🟡 3 through 🟡 6 share its fix or are record corrections |
| Loses a record or crashes | no |

- [ ] Pass

<!-- THE ONE-LINE FIX WAS COMPOSED WHERE A COPY EXISTED. `skipped_by_narrowing`,
thirty lines down in the same file, states the identity this branch chose in
round 1 for exactly this class — *two names are one file when they reach one
inode* — and gives the reason a fold on the spelling has a platform inside
it. `resolve_patterns` got `normpath` instead: it closes the separator half
the Windows leg found and no more, and it changes the path the caller opens.
That is round 11's lesson one more time — copy the direction the other
carriers agree on, never compose a fourth — arriving in a fix the same
orchestrator wrote an hour later.

The reader that found it built the fixture the fix pass did not: a pattern
that crosses a symlink before a `..`. Executed both sides of the diff, the
pre-fix tree exits 2 naming the broken row and the post-fix tree exits 0
having read a different file. A run that reports clean while something is
missing, produced by this work item, a third time.

Written and committed before the fixes it commissions, so both fix-surface
rows start pending.

THE FIX SURFACE ABOVE is the reach-back, filled at `404e769`, and the reason
sits here rather than in the cell. `Contract changes` names `resolve_patterns`
because the SPELLING it returns changed — a normalized one at `3026a33`, the
pattern's own now — and that is a change to the set of returnable values
the row exists to name, even with signature, arity and return type intact;
both callers were revisited, `main` because it opens and
`skipped_by_narrowing` because it stats. An AST comparison of `1380c9f`
against `404e769` with docstrings stripped finds it the one changed unit,
nothing added or removed. The three new units are cases in a file that
predates the run, each answering a finding in `resolve_patterns`, which
also predates it — depth 1. -->

## What this round was asked

The verifying round at `git diff 3bf0fd6..c590961` — **three commits**, the
orchestrator's, given as a count the round re-took: 3.

Round 12's 🔴 8, the Windows leg's finding, was fixed by folding
`resolve_patterns`' matches with `os.path.normpath`, and the record shape
that finding forced — the row in round 12's own table, the removed
`round-13.md` — was explained. Six things to break: what `normpath` does and
does not fold, with `..` across a symlink named as the question; the new case
against §15 and whether anything but the fold satisfies it; the record
shape, against the ordering rule and the floor's walk counted per record;
what the removed record carried and where it went; R8's re-read; and the
terminal state and the squash. The **platform** axis was named beside the
table's floor: what this fix rests on, and whether the new case removes it.

The first found 🔴 1 and 🟡 2. The Windows leg at `c590961` was mine to
carry, not the round's, and it is green.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `normpath` changes which file the checker opens. It collapses `..` lexically, so where a `--ledger` pattern crosses a symlink before a `..` the returned path names a different file than `glob` matched — and `main` opens the returned path | `evidence_check.py:911`, inside `resolve_patterns` | **fixed** `404e769` | **Executed** by the round, one fixture, both sides: `x/lnk -> y`, pattern `x/lnk/../ledger.md` names `<root>/ledger.md` (a BROKEN row); `normpath` returns `x/ledger.md` (a clean row). Pre-fix: `exit=2 · 0 ok · 1 broken · BROKEN src/service.py#gone`. Post-fix at `c590961`: `exit=0 · 1 ok · 0 broken`. A regression this diff introduces, and this work item's own title |
| 🟡 2 | The class is half closed. *One file, two spellings* is one of five ways a file reaches `resolve_patterns` under two names; the fix closes separators and `.`/`..` and leaves case, symlink and hard link counting one file twice | the same line | **fixed** `404e769` | **Executed** at `c590961` on this case-insensitive volume, six pairs of `--ledger` patterns: `seal/ledger.md`+`seal/*.md` → 1 ok; `./seal/ledger.md`+`seal/ledger.md` → 1 ok; `seal/../seal/ledger.md`+`seal/ledger.md` → 1 ok; **`seal/Ledger.md`+`seal/ledger.md` → 2 ok**; **a symlink to it → 2 ok**; **a hard link to it → 2 ok**. `--ledger SEAL/ledger.md` is the motivating example `skipped_by_narrowing`'s own docstring uses. **§13 stated**: the fix rests on *every alias differs only in separators and dot segments*; the new case removes the `os.sep` guarantee and nothing else |
| 🟡 3 | The docstring presents the hole as the virtue — *folds no case, so it is not the `normcase` mistake* — where not folding case is what leaves `Ledger.md` beside `ledger.md` counted twice. Repeated in the new case's docstring and in round 12's 🔴 8 grounds | `evidence_check.py:904-906`; `tests/…:435-436`; `rounds/round-12.md` 🔴 8 | **fixed** `404e769` | **Read**. `normcase` was wrong in `skipped_by_narrowing` for folding case on Windows alone — an asymmetry; here the omission is the defect. Superseded by the docstring the inode fold carries |
| 🟡 4 | `phase-15.md` gives a false reason for `Contract changes: none` — *which every caller already normalises or opens*. `open` is the caller for which a changed spelling is a changed file; 🔴 1 is that sentence measured | `phases/phase-15.md:68-70` | **fixed** `404e769` | **Read**. The verdict is still defensible on signature, arity and return type; the set of returnable values changed, and the stated reason for waving it through is the one the finding falsifies |
| 🟡 5 | The removed `round-13.md` closed a deferral and the closure did not land: it said the Windows leg's own question — `st_ino == 0` — was **answered** by the leg's run. Round 12's Deferred table still names the leg as owing it | `rounds/round-12.md:104` | **fixed** `404e769` | **Read**, line by line against `git show eabbd44:…/round-13.md`: everything else it carried is in 🔴 8's grounds, R8's Notes or `phase-15.md`; this one fact survives only as a parenthetical |
| 🟡 6 | Round 12's `PR` cell says *not yet opened* two rows above a cell naming pull request #162. Rounds 1–11 carry the same stale value as house practice; round 12 is the record `c590961` deliberately rewrote to post-pull-request facts, and left this one | `rounds/round-12.md:7` | **fixed** `404e769` | **Read**. A contradiction a reader meets inside one file, in the record whose own comment names the one wrong sentence it leaves standing |
| 🟢 7 | §15 — the new case seen red | `tests/…::test_one_file_matched_under_two_spellings_is_read_once` | answered | **Executed**: the line reverted in a clone → `total: 2 ok`; R8's original case stays green here, as it can only go red on Windows. `main` joins `--ledger` under `root` and normalises nothing, so both spellings reach `resolve_patterns` distinct — nothing but the fold satisfies it |
| 🟢 8 | The record shape — `written_late` and the floor's walk | `rounds/round-12.md` | answered | **Executed**: `3026a33` descends from `3bf0fd6`, the commit that added `round-12.md`, so the ordering test passes; `chain_check` at HEAD counted per record prints exactly round 12's honest pair and nothing on `round-11.md` — `wrote_fixes` returns True for round 12 and the count stops there |
| 🟢 9 | The terminal state, and the squash | a `--no-local` clone | answered | **Executed**: `round-13.md` with `no fixes to check` / `no` / `no` / `Pass` ticked and round 12's cell set to `round-13` → `chain_check` **exit 0**. `merge --squash c590961`, six suites **218 passed** |
| 🟢 10 | R8's claim, the anchors, the ledgers | `seal/ledger/1788501054-…md` R8 | answered | **Executed**: R8 still deduplicates and the total is still where a duplicate shows; `resolve_patterns@9bed738b` and both cases resolve; `evidence_check.py .` unscoped → `541 ok · 1 drifted · 0 broken`, S8 alone. The Notes' *executed* still means executed against separator and dot spellings alone — 🟡 2's shape |
| 🟢 11 | `New units`, and the unit as code | `rounds/round-12.md:11` | answered | **Executed**: `git diff 3bf0fd6..3026a33` adds exactly one top-level definition, the one named. It pins the class off Windows and is red under the revert; it does not cover the case/link half — 🟡 2 |
| ❓ 12 | `questions.md` Q2, Q3, Q4 | `questions.md` | out of verified scope | **Read**, unchanged. The repository owner |

## Executed probes

| What was run | Result |
|---|---|
| `git rev-list --count 3bf0fd6..c590961` | **3** |
| the symlink-then-`..` fixture, pre-fix and at `c590961` | `exit=2 · 1 broken` → `exit=0 · 1 ok` — 🔴 1 |
| six alias pairs through `--ledger`, at `c590961` | three `1 ok`, three **`2 ok`** — 🟡 2 |
| the reviewer's inode-fold replacement, in a clone | 43 passed; all six pairs `1 ok`; two different files `2 ok`; the symlink fixture back to `exit=2` naming the broken row |
| the `normpath` line reverted, in a clone | the new case red with `total: 2 ok`; R8's case green here |
| `written_late` on `round-12.md` against `3026a33` | does not fire |
| `chain_check` at HEAD, counted per record | round-12's honest pair only |
| the terminal state with `round-13.md`, in a clone | **exit 0** |
| `merge --squash c590961`, six suites | **218 passed** |
| `evidence_check.py .` **unscoped** · `uvx ruff check` / `format --check` on both changed files · records and prose suites | `541 ok · 1 drifted · 0 broken` — S8 · clean · **141 passed** |
| the pull request's checks at `c590961`, **by the orchestrator** | ledger, lint, release, pytest on ubuntu, macOS and **windows** — all green |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1, 3, 12, 13 | `evidence_check.py#skipped_by_narrowing`'s inode fold, and `#resolve_patterns` | The same identity question, answered in round 1 one function down and composed differently here. The next reader opens both and checks they state one rule |
| round 12 | the record shape for a finding that arrives after the terminal record | Legal as a row in the terminal record; `phase-15.md` says why and #161 is where the schema gap goes |
| rounds 11, 13 | the orchestrator's fixes | Round 11: copy the direction the carriers agree on. Round 13: the same lesson, in code — the file already argued the identity |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The fix for 🔴 1 and 🟡 2 is one rewrite — the inode fold with the pattern's own spelling returned — and three cases seen red first; the docstring, `phase-15.md`'s paragraph and round 12's two cells are corrected with it; round 14 reads that diff | `phases/phase-16.md` | the orchestrator, on the owner's standing answer for this branch's fixes |
| A finding that arrives after a run's terminal record has no legal round of its own — it lives in the terminal record's table | `phases/phase-15.md`; a comment on issue #161 | the repository owner |
| `questions.md` Q2, Q3, Q4 · issues #158–#161 · S8 | as before | the repository owner |
