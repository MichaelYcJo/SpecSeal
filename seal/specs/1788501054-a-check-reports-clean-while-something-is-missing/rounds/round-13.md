# 1788501054-a-check-reports-clean-while-something-is-missing — review round 13

| Field | Value |
|---|---|
| Target SHA | 3bf0fd6 |
| Ran by | github-actions on windows-latest, python 3.12 — the `pytest (windows-latest, 3.12)` job of run 33939786295 on pull request #162. No warden ran this round: the CI leg is the reader every record since round 2 named as this class's answerer, and it answered |
| PR | #162, opened ready at `3bf0fd6` and returned to draft at this record until round 14 ticks `Pass` |
| Broad gate | `e48d682` locally (2097 passed · 0 failed); on the pull request, ubuntu and macOS green, **windows red on one case**, lint and ledger and release green |
| Fixes checked by | nobody — this round's fixes are not yet written; the round that opens them sets this cell |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1, `resolve_patterns` deduplicates on the spelling `glob.glob` returns, and on Windows a literal pattern comes back with `/` while a wildcard comes back with `\`, so one file matched by two patterns is read twice and its rows counted twice — the defect R8's case exists to refuse, refused only on the platform where the spelling differs |
| Loses a record or crashes | no |

- [ ] Pass

<!-- THE READER THE RECORDS NAMED, ANSWERING. Rounds 2 through 12 each carried
a Deferred row naming *the windows CI leg at this pull request* as the
answerer for what the checker does where the platform differs. The leg ran at
`3bf0fd6` and answered with one red case — not the `st_ino == 0` question it
was asked, which passed, but the unit beside it: R8's deduplication, added by
round 3's fix pass, which folds paths by string and so had a platform inside
it after all. That is the shape round 1's 🟡 9 named for `skipped_by_narrowing`
and this branch fixed there with the inode fold; `resolve_patterns` kept the
string fold because its concern is the same glob hit spelled two ways, and
nobody had removed the platform guarantee for it (agent-contract §13).

This record is written by the orchestrator from the job's log, before the
fix, with the verdict open — the ordering rule applies to a record whatever
ran the round. The fix is one line and a case that can be seen red off
Windows too, because the class is *one file, two spellings*, and `./seal/ledger.md`
against `seal/ledger.md` is that class on every platform. -->

## What this round was asked

Nothing — no spawn prompt. `.github/workflows/test.yml` runs `pytest tests/ -q
-n auto` on three platforms at every pull request, and the records since
round 2 had deferred one question to its Windows leg by name: whether
`st_ino == 0` actually arrives there, and the `normcase` pairing the
fallback's recorded limit describes. Both passed. What the leg found instead
was in the unit beside them.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | One file matched by two patterns is read twice on Windows. `resolve_patterns` returns `sorted({p for pat in patterns for p in glob.glob(pat, recursive=True)})`, and `glob.glob` keeps a literal pattern's spelling (`seal/ledger.md`) while joining a wildcard's matches with `os.sep` (`seal\ledger.md`). Two strings, one file, and the set does not collapse them; every row in the ledger is counted twice | `skills/evidence-check/scripts/evidence_check.py#resolve_patterns`; `tests/test_a_narrowed_ledger_read_says_what_it_skipped.py::test_one_file_matched_by_two_patterns_is_read_once` | open | **Executed by the CI leg**: `1 failed, 2072 passed, 25 skipped` on windows-latest; the failing assertion shows `seal\ledger.md` listed twice with `1 ok` each and `total: 2 ok`. **Orchestrator read the function and the log**: the fold is on the raw string, and the log's two spellings are the two the docstring above predicts for a literal and a wildcard. The other two platforms return one spelling for both, which is why R8's case was green through twelve rounds and every local run. The `st_ino` question the leg was asked passed on the same run |

## Executed probes

| What was run | Result |
|---|---|
| `pytest tests/ -q -n auto` on windows-latest, python 3.12, at `3bf0fd6` — run 33939786295 | **1 failed · 2072 passed · 25 skipped** — the one is 🔴 1 |
| the same on ubuntu-latest and macos-latest | green |
| `lint`, `ledger`, `release` jobs on the pull request | green |
| `gh run view --log-failed`, read by the orchestrator | `assert 'total: 1 ok' in '…seal\\ledger.md … 1 ok … seal\\ledger.md … 1 ok …'` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1, 3 | `evidence_check.py#skipped_by_narrowing`'s inode fold, and R3 | The same class — a path folded by spelling has a platform inside it — was found there in round 1 and fixed with the inode; `resolve_patterns` kept the string fold one function over |
| round 3 | `evidence_check.py#resolve_patterns` and R8 | R8 records the deduplication as *executed*; it was executed on one platform |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `st_ino == 0` arrives on `windows-latest` — **answered**: the leg ran the cases that build a zero inode and the fallback, and they passed | this row | closed by the leg's own run |
| `questions.md` Q2, Q3, Q4 · issues #158–#161 · S8 | as before | the repository owner |
