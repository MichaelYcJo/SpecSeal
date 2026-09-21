# 1789996780-the-census-and-the-tie-that-nothing-holds — review round 2

| Field | Value |
|---|---|
| Target SHA | 11b9f9e3 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 480 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `1d1f072a25e473826dcac62d56cff1fb5e533253..952a247efc9e4e965c9b02c8b385f38d0e61fb2c`, 2 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — N1, the census note's false claim about the instrument |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is the verifying round, spawned against the diff of round 1's fixes
rather than the branch. Round 1 recorded eight findings as fixed; this round
answered each one and judged the one surface the fix pass added that nobody
had reviewed, `ledger_text`. Finding 1's claim was re-enumerated by
construction — every comment token and every docstring token of both touched
modules, matched for digit runs and number words, rather than by a grep for a
phrase — and both flagged sites now carry hedges that cannot go stale, with no
measured corpus figure left in the module. Findings 4 and 5 were re-measured
by mutation and each new assert was seen red with its own message. Finding 3's
departure from the paste-ready text was settled by execution, and the pass was
wrong about why: round 1's 13 and the pass's 15 are two readings of one phrase
— *the count rose* against *the count differs* — and both reproduce at three
tips, so the census note now states as fact an instability that does not
exist. The corpus did not move across the fix range: every digit of the census
note reproduces at `11b9f9e3` exactly as at `55ae1b63`, which is what makes
the C3/C4 decision not to write a second marker measurably right rather than
merely argued.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's finding 1, confirmed closed — the module states a corpus figure at three sites, not the one A1 permits | `skills/evidence-check/scripts/correction_check.py#read_blobs`, `skills/evidence-check/scripts/correction_check.py#standing` | **closed** | Executed, re-enumerated by construction rather than by grep: both modules tokenised and every comment and docstring line carrying a digit run or a number word listed (128 / 324 lines). No measured corpus figure stands in `correction_check.py` outside the census note. Both sites reworded to quantities a release cannot falsify; `1.07 MB` and `0 of 189` are gone |
| 🟢 | round 1's finding 2, confirmed closed — a third docstring in the test module states *185 rows … against `Corrected`'s 10* | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_a_merge_that_reverts_a_re_read_row_is_reported` | **closed** | Executed, same enumeration over the test module's 145 figure-carrying prose lines. The docstring now states the shape and points at the census note; the module's remaining figures are past-tense records that name their moment or fixture-scale statements |
| 🟢 | round 1's finding 3, confirmed closed — the census note's last figure cannot be re-taken from the instrument the note names | `skills/evidence-check/scripts/correction_check.py#MARKER` | **closed, and the fix introduced N1** | Executed: `git log -S'Re-read again' -- seal/ledger.md` returns 9 at `55ae1b63`, `11b9f9e3` and `origin/main`, so the figure and the instrument now agree. The same edit's justifying sentence is false — see N1 |
| 🟢 | round 1's finding 4, confirmed closed — `site_row` is unpinned and the stated grounds do not hold | `tests/test_a_merge_cannot_silently_drop_a_correction.py#site_row` | **closed** | Executed, mutation re-run in a clone: `site_row`'s whole body replaced with `return ""` now gives **1 failed / 49 passed** where round 1 measured 50 passed, and it fails on the new assert's own line, `assert '' == 'R1 · a claim'`. A11 untouched — two asserts, no case added |
| 🟢 | round 1's finding 5, confirmed closed — the corpus reader raises `FileNotFoundError` on a tracked path the worktree has lost | `tests/test_a_merge_cannot_silently_drop_a_correction.py#ledger_corpus` | **closed** | Executed, both directions: the work item's fragment deleted from the worktree unstaged now gives **50 passed**; restoring the pre-fix one-line reader in the same tree state gives **1 failed / 49 passed**. The index route is right — `git show :<path>` reads the entry `git ls-files` listed |
| ⬜ | round 1's finding 6, confirmed closed — row C1's third correction carries a half-applied edit | `seal/ledger.md`, row C1 Notes | **closed** | Read. The duplicated aside is gone and the sentence parses: *after every marker this work item writes into it — this one, row C2's, and the two that record C3 and C4 being re-read — was already in place: 429 marker occurrences in the file*. Executed: 429 re-measured true at `11b9f9e3` |
| ⬜ | round 1's finding 7, confirmed closed — the sibling `spec.md` keeps *Six commits … introduced `Re-read again`* | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md` | **closed** | Executed: the sentence now reads *Nine commits … measured at the tip of the branch for #469, #470 and #471 with `git log -S`*, and `git log -S` returns 9 at that tip. Corpus, instrument and moment all present, and it carries none of N1's false clause |
| ⬜ | round 1's finding 8, confirmed closed — `evidence_check.py` states *all 1520 lines of `seal/ledger.md`* with no moment | `skills/evidence-check/scripts/evidence_check.py#OLD_COORD_RE` | **closed for the named site; the class is one name short — N2** | Read: the line count is gone and the timings now name the moment their `Verified` stamp dates. The same block still states *805 ledger rows* with no moment, three lines below |
| 🟡 1 | The census note states as fact that round 1 and the fix pass got different totals *for that variant on the same question days apart*, presenting an under-specified instrument as instability in the history | `skills/evidence-check/scripts/correction_check.py#MARKER` | **fixed** `7956f85c` | fixed at 7956f85c; Executed at three tips over all 213 commits: *the count rose* returns 13 every time, *the count differs* returns 15 every time, every parent returns 8, `git log -S` returns 9. Nothing moved across the fix range or between this branch and `main`. The gap was the predicate, not the day |
| ⬜ 2 | The rider block corrected for a moment-less corpus figure still states *805 ledger rows* three lines below the sentence that corrected it | `skills/evidence-check/scripts/evidence_check.py#OLD_COORD_RE` | **fixed** `952a247e` | fixed at 952a247e; Executed: 625 rows carry an anchor coordinate in `seal/ledger.md` at `11b9f9e3`; across that file and the live fragment together it is 629 <!-- CORRECTED 2026-09-22 by round 3, in the closing commit. What stood here: "625 rows carry an anchor coordinate across seal/ledger.md and the live fragment at 11b9f9e3". 625 is the shared file alone. The fragment is byte-identical at both SHAs, so this is a scope word in the record rather than drift in the tree — and it is the work item's own class, a figure whose corpus is named wider than the one it was taken over. Corrected in place with the round named, never deleted silently. -->; the shared file holds 887 table lines. Neither is 805. `agent-contract` §12, and `overview.md` records four short closes in this lineage already |
| ⬜ 3 | The same edit left one comment line at 138 characters in a block that wraps at 75, ending mid-sentence | `skills/evidence-check/scripts/evidence_check.py#OLD_COORD_RE` | **fixed** `952a247e` | fixed at 952a247e; Executed: measured at 138 against a next-longest of 90 in the file and 103 across both scripts. `ruff check` and `ruff format --check` both pass — `E501` is not selected — so nothing catches it |
| 🟢 | The new unit `ledger_text` reads the right blob and its guards fire in the asserted order | `tests/test_a_merge_cannot_silently_drop_a_correction.py#ledger_text` | verified | Executed: the index route broken to return `""` reddens on the new assert's own message and never reaches `assert corpus` below it. `git show :<path>` is the index entry `git ls-files` listed, so listing and content come from one place |
| ⬜ | `ledger_text`'s worktree-wins branch is held by nothing — deleting it leaves the module green | `tests/test_a_merge_cannot_silently_drop_a_correction.py#ledger_text` | answered | Executed: the `if on_disk and target.exists()` branch removed leaves **50 passed**. Answered rather than opened because the code records the reason — a two-route comparison would redden for anyone with an edited ledger — and A11 bounds the case count. The behaviour as shipped is correct |
| 🟢 | The corpus did not move across the fix range, which is what makes the C3/C4 decision right | `seal/ledger.md`, rows C3 and C4 | verified | Executed: every digit of the census note re-measured identical at `11b9f9e3` and `55ae1b63` — 429 / 429, 426 on 204 rows, 3 in prose, 385 bare, 44 in ten spellings, run lengths and bound sweep all exact. Two more markers would have made it 431. `CLAUDE.md` puts the reading date in the `Checked` column, both rows carry `2026-09-22` there, and `correction-check` exits 0 |
| 🟢 | A11 over the fix range — no exit code, verdict or printed line can have changed | `skills/evidence-check/scripts/correction_check.py`, `skills/evidence-check/scripts/evidence_check.py` | verified | Executed: both revisions of both scripts parsed and dumped with every docstring removed give identical syntax trees |
| ⬜ | `correction_check.py`'s module docstring states *37 merge commits, 24 of them with a parent carrying a ledger with markers*, with no moment and no instrument, and it was never true of the tip | `skills/evidence-check/scripts/correction_check.py` | deferred #481 | Executed: 32 and 25 at all four tips read; `--all` gives 38; only 31 merges were reachable at `3878566d`, the commit that wrote it. Outside this branch's diff, written by merged work item 1789969379, and a figure about the history rather than about the corpus finding 1's claim is scoped to |
| ❓ | out of verified scope — the full suite, the repository-wide lint and the typecheck | repository-wide | out of verified scope | The prompt withholds them and `agent-contract` §2 assigns them elsewhere. Eight test modules were run by this round; nothing here speaks for the rest. The `sealer` is the answerer |

## Paste-ready fixes

```python
# one-off somebody can be asked to stop writing: nine commits in this
# repository's history have introduced `Re-read again` into that file -- a
# figure taken with `git log -S'Re-read again' -- seal/ledger.md` rather than
# with the walk above, which counts sites in a file and not commits. Naming
# the second instrument is not pedantry, and *counts commits against the
# first parent* is not yet a name: read as *the count rose* and read as *the
# count differs* it is two instruments, each perfectly stable and each
# answering higher than `git log -S` does. Review round 1 of work item
# 1789996780 and the fix pass answering it reported different totals for what
# both called one variant, and round 2 settled it by running both readings at
# three tips -- the gap was the predicate, not the history and not the days
# between the two readings. The conclusion holds on every reading, which is
# why the figure stays; `git log -S` is named because its question has one
# reading.
```
```python
# near it: over the whole of `seal/ledger.md` and the `seal/ledger/*.md`
# fragments the slowest is 0.000533 s, on the longest row in the corpus at
# 8831 characters, and the 19 rows of 1150-1280 characters top out at
# 0.000178 s -- timings from this rider's own reading, which is what its
# `Verified` stamp below dates. No line count stands here: that one was a
# figure about a corpus that grows at every release, and it had gone stale.
# So it was enumerated as a member of that class and left rather
# than fixed. What the pathological shape needs is a run with no `:<digits>`
# to finish on, and a real row's paths terminate. Repairing it means changing
# which paths a coordinate may name, which every anchored row in the ledger
# depends on, and that is a change with its own argument to make.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_merge_cannot_silently_drop_a_correction.py -q` at the target SHA | exit 0 — 50 passed |
| `bin/test` over seven further modules that read these two scripts or their prose — the rider case, the real-identifier case, the one-word case, the script-reachability case, the CI-step case, the content-anchor case and the evidence-check case | exit 0 — 238 passed, 7 skipped. Eight modules green in all, this round |
| Construction enumeration: both touched scripts and the test module tokenised, every comment and every docstring line carrying a digit run or an English number word listed | 128 lines in `correction_check.py`, 324 in `evidence_check.py`, 145 in the test module. No measured corpus figure survives in `correction_check.py` outside the census note; the test module's remaining figures all name a moment or are fixture-scale |
| Mutation — `site_row`'s whole body replaced with `return ""`, module alone | 1 failed / 49 passed, failing on `assert '' == 'R1 · a claim'`. Round 1 measured 50 passed on the same mutation before the fix |
| Mutation — `ledger_text`'s index route replaced with `""`, module alone | 1 failed / 49 passed, on the new assert's own message, above `assert corpus` |
| Mutation — `ledger_text`'s `if on_disk and target.exists()` branch deleted, module alone | 50 passed — the worktree route is held by nothing |
| The work item's ledger fragment deleted from the worktree without staging, module alone | 50 passed. With the pre-fix one-line reader restored in the same state: 1 failed / 49 passed |
| An independent census over `seal/ledger.md` at `11b9f9e3`, walked verb by verb with no bound | 429 candidate sites against 429 `MARKER` occurrences; 426 on 204 rows; 3 in prose; 385 bare; 44 in ten spellings, every listed count exact; run lengths 0: 385, 1: 23, 2: 9, 3: 11, 5: 1; bound sweep 428 / 428 / 429 / 429 / 429. Identical to round 1's reading at `55ae1b63` |
| Commits introducing `Re-read again` into `seal/ledger.md`, four instruments, at `55ae1b63`, `11b9f9e3` and `origin/main` | `git log -S` 9 at all three; rose-from-first-parent 13 at all three; differs-from-first-parent 15 at all three; rose-against-every-parent 8 at all three. Over `--all`: 14 / 16 / 13 |
| Merge commits reachable and how many have a parent carrying a ledger with markers, at `55ae1b63`, `11b9f9e3`, `origin/main` and `origin/release/v0.12.3` | 32 and 25 at all four. `--all` gives 38. At `3878566d`, which wrote *37*, 31 were reachable |
| Rows carrying an anchor coordinate across `seal/ledger.md` and the live fragment at `11b9f9e3` | 625, against 887 table lines in the shared file. The rider's *805* is neither |
| Both revisions of both scripts parsed and dumped with docstrings removed, over the fix range | Identical syntax trees for each — A11 verified by construction rather than asserted |
| Longest comment line per file | 138 in `evidence_check.py`, introduced by this fix range; next longest 90 in the same file, 103 across both scripts |
| `bin/evidence-check .`, unscoped, no `--reverify` | exit 0. `1399 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records arm `1 work item read · 95 unread · 0 refused` |
| `bin/correction-check --range origin/release/v0.12.3...HEAD` | exit 0 |
| `bin/survivor-check --range origin/release/v0.12.3...HEAD --exempt …/survivors.md` | exit 0 |
| `bin/unverified-check` | exit 0 |
| `uvx ruff check` and `uvx ruff format --check` on the three touched files | exit 0 both. `All checks passed!` · `3 files already formatted` |
| The broad gate — full suite, repository-wide lint, typecheck | not yet. Withheld from this round by the prompt and by `agent-contract` §2; the `sealer` is the answerer. With N1 answered, the rounds have nothing else open and the spawn comes due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/correction_check.py:559`, `skills/evidence-check/scripts/correction_check.py:377` | round 1's 1 — fixed |
| round-1 | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_a_merge_that_reverts_a_re_read_row_is_reported` | round 1's 2 — fixed |
| round-1 | `skills/evidence-check/scripts/correction_check.py:250` | round 1's 3 — fixed |
| round-1 | `tests/test_a_merge_cannot_silently_drop_a_correction.py#site_row` | round 1's 4 — fixed |
| round-1 | `tests/test_a_merge_cannot_silently_drop_a_correction.py#ledger_corpus` | round 1's 5 — fixed |
| round-1 | `seal/ledger.md`, row C1 Notes | round 1's 6 — fixed |
| round-1 | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md:95` | round 1's 7 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:83` | round 1's 8 — fixed |
| round-1 | `skills/evidence-check/scripts/correction_check.py:220` | round 1's carried — verified |
| round-1 | `skills/evidence-check/scripts/correction_check.py#MARKER` | round 1's carried — verified |
| round-1 | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_the_bound_covers_every_candidate_marker_site_the_corpus_carries` | round 1's carried — verified |
| round-1 | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_a_tie_falls_to_the_first_parent` | round 1's carried — verified |
| round-1 | `tests/test_a_merge_cannot_silently_drop_a_correction.py#candidate_sites` | round 1's carried — verified |
| round-1 | `.github/workflows/hygiene.yml` | round 1's carried — verified |
| round-1 | `skills/evidence-check/scripts/correction_check.py` | round 1's carried — verified |
| round-1 | `seal/specs/1789996780-the-census-and-the-tie-that-nothing-holds/survivors.md` | round 1's carried — verified |
| round-1 | `skills/evidence-check/scripts/correction_check.py#standing` | round 1's carried — verified |
| round-1 | `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md` | round 1's carried — verified |
| round-1 | repository-wide | round 1's — — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `correction_check.py`'s module docstring states *37 merge commits, 24 of them with a parent carrying a ledger with markers* with no moment and no instrument, and 32 and 25 are what four tips read | an issue from this pull request. Outside this branch's diff — written by merged work item 1789969379 at `3878566d` — and a figure about the history rather than about the corpus | the repository owner, as an issue from this pull request |
| Q1 — whether this branch may amend the released `CHANGELOG.md` §0.12.2 | Already deferred in round 1: `questions.md` Q1, `overview.md` §*Not verified*, `seal/follow-up.md`, `survivors.md`'s first row. Re-found by this round and not re-litigated | the repository owner |
| Q2 — #469's issue body, whose histogram is neither corpus and sums to 412 | Already deferred in round 1: `questions.md` Q2 and `overview.md` §*Not verified* | the repository owner, or the orchestrator |
| The `test_a9_the_leg_asks_the_range_the_pull_request_is_about` slice on a bare literal | Already deferred in round 1: `overview.md` §*Not verified* | the repository owner, as an issue from this pull request |
