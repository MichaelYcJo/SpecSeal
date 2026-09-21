# 1789996780-the-census-and-the-tie-that-nothing-holds — review round 3

| Field | Value |
|---|---|
| Target SHA | 979947f9 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 480 |
| Broad gate | af56a9da against 8531c858 |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 is the run's last round, spawned against the diff of round 2's fixes
— `1d1f072a..952a247e`, two commits — plus the closing record commit
`979947f9`. Its job was the answers, not new findings. Each of round 2's
three findings was opened and judged on this round's own grounds, and the
three things the fix pass disclosed were settled by execution rather than
accepted. The reopening is spent, so anything still standing leaves this
round with a named home rather than a fix pass.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 1, confirmed closed — the census note stated as fact an instability that does not exist | `skills/evidence-check/scripts/correction_check.py#MARKER` | **closed** | Executed at five tips of 192, 204, 213, 216 and 217 commits: *rose from the first parent* 13 at every one, *differs from the first parent* 15 at every one, `git log -S` 9 at every one. Both readings stable, both higher than `git log -S`. Round 1 recorded 13 and the fix pass 15, both calling it counting against the first parent. The false clause is gone and the replacement states no new digit |
| 🟢 | round 2's finding 2, confirmed closed — the rider block kept *805 ledger rows* with no moment | `skills/evidence-check/scripts/evidence_check.py#OLD_COORD_RE` | **closed** | Read: the figure is gone and *every anchored row in the ledger* replaces it, which no release can falsify. The clause is true — the path half of `OLD_COORD_RE` is byte-identical to `ANCHOR_RE`'s, so the repair is a change to what a coordinate of either shape may name. Executed: 805 matches no reading of the corpus at any of six tips back to `v0.12.1` |
| 🟢 | round 2's finding 3, confirmed closed — one comment line at 138 characters | `skills/evidence-check/scripts/evidence_check.py#OLD_COORD_RE` | **closed** | Executed: longest comment line in the file 138 before the range, 90 after, and the 90 is line 72 from `bf82bd3c` on 2026-09-01. The six added lines measure 76 and 77 against a block band of 73-80, so the fix added no new instance |
| 🟢 | The fix pass departed from round 2's second paste-ready block, and applying that block verbatim would have deleted a sentence | `skills/evidence-check/scripts/evidence_check.py#OLD_COORD_RE` | verified | Executed: block 1 is byte-present in `correction_check.py`; block 2 is not. It ends at *its own argument to make.* while the pre-fix text continued *If you open this pattern, make that argument or anchor the second repetition so the two stop overlapping.* The pass kept that sentence and reflowed a 63-character line. Both departures are improvements |
| 🟢 | Disclosure 2 settled — *differs from every parent* is `git log -S`'s own predicate, not a third reading | `skills/evidence-check/scripts/correction_check.py#MARKER` | **answered** | Executed over all 217 commits at `979947f9`: the two predicates name the same nine commits, both set differences empty. *Rose against every parent* returns 8 and is a strict subset. Round 2's 8 and the pass's 9 are both right and measure different questions. The shipped text scopes its two readings to the first parent and is untouched |
| 🟢 | Disclosure 3 settled — 759 and 887 are both right, and 805 is neither, at any tip | `seal/ledger.md`, `seal/ledger/1789996780-the-census-and-the-tie-that-nothing-holds.md` | **answered** | Executed at `979947f9`: shared file 625 anchored rows / 759 `cc.rows` / 887 pipe-lines / 128 separators; fragment 4 / 5 / 6. 887 − 759 is exactly the separator count, so the two readings differ by definition and not by measurement. Flat at six tips back to `v0.12.2`; 732 / 857 / 601 at `v0.12.1`. The shipped clause needs none of them |
| 🟢 | `New units: none` and `Contract changes: none` verified by construction rather than assumed | `skills/evidence-check/scripts/correction_check.py`, `skills/evidence-check/scripts/evidence_check.py` | verified | Executed: every added and every removed line in `1d1f072a..952a247e` begins with `#`; no `def` or `class` added; both revisions of both modules parse to identical syntax trees. A comment-only diff cannot move an exit code, a verdict or a printed line |
| 🟢 | The fix pass made no ledger edit in its range, which every figure in this work item depends on | `seal/ledger.md` | verified | Executed: `1d1f072a..979947f9` touches `round-2.md` and the two scripts only. The fragment is 6342 bytes at `11b9f9e3` and at `979947f9`, and `seal/ledger.md` is unchanged across the range |
| ⬜ | One comment line in the same attached block still runs to 90 characters where the block wraps at 73-80 | `skills/evidence-check/scripts/evidence_check.py#OLD_COORD_RE` | deferred — `seal/follow-up.md`, or an issue from this pull request if the orchestrator judges it earns one | Executed: line 72, 90 characters, blamed to `bf82bd3c` on 2026-09-01 and untouched by this branch. `ruff check` passes because `E501` is not selected. Named under `agent-contract` §12 because it is the class round 2's finding 3 belongs to, not a fix this run commissions |
| ⬜ | Round 2's grounds cell for its finding 2 names a corpus one file wider than the figure it carries | `seal/specs/1789996780-the-census-and-the-tie-that-nothing-holds/rounds/round-2.md`, finding 2's Grounds cell | correction | Executed: 625 is `seal/ledger.md` alone; the file and the live fragment together carry 629. The fragment is byte-identical at both SHAs, so this is a scope word in the record and not drift in the tree. Paperwork under `seal/specs/`, so out of `Needs a fix` |
| ⬜ | *Each perfectly stable* is a property of the two readings measured at a sample, stated without one | `skills/evidence-check/scripts/correction_check.py#MARKER` | **answered** | Executed at five tips spanning 192 to 217 commits: 13 and 15 at every one. The note's next clause names the sample it rests on, and the conclusion it draws is that the gap was the predicate, which does not need the property to hold forever. Closed on this round's own grounds |
| ⬜ | Q1, Q2 and the `test_a9_the_leg_asks_the_range_the_pull_request_is_about` fragility | `seal/specs/1789996780-the-census-and-the-tie-that-nothing-holds/questions.md`, `seal/specs/1789996780-the-census-and-the-tie-that-nothing-holds/overview.md` | deferred — already deferred in round 1 and carried by round 2 | Read. Re-found and not re-litigated. `bin/unverified-check` exits 0 and prints them as open rows against a named answerer, which is the shape a deferral is supposed to leave |
| ⬜ | `correction_check.py`'s module docstring states *37 merge commits, 24 of them …* | `skills/evidence-check/scripts/correction_check.py` | deferred #481 | Read. Already deferred in round 2 to issue #481, outside this branch's diff, and not re-litigated here |
| ❓ | out of verified scope — the full suite, the repository-wide lint and the typecheck | repository-wide | out of verified scope | The prompt withholds all three and `agent-contract` §2 assigns them elsewhere. Eight test modules were run by this round and are green; nothing here speaks for the rest of the suite. The `sealer` is the answerer, and with nothing open its spawn is now due |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the eight modules that read these two scripts or their prose — the merge-correction case, the rider case, the real-identifier case, the one-word case, the script-reachability case, the CI-step case, the content-anchor case and the evidence-check case, at `979947f9` | exit 0 — 288 passed, 7 skipped |
| `bin/evidence-check .`, unscoped, no `--reverify` | exit 0 — `1399 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records arm `1 work item read · 95 unread · 70 names read · 3 stamps read · 0 refused` |
| `bin/correction-check --range origin/release/v0.12.3...HEAD` | exit 0 — no merge commit in the range, so no correction can have been dropped at one |
| `bin/survivor-check --range origin/release/v0.12.3...HEAD --exempt …/survivors.md` | exit 0 — 1155 files examined against 82 removed sentences, no removed wording still standing |
| `bin/unverified-check` | exit 0 — 88 overviews · 298 open · 62 closed · 0 unreadable |
| `python3 .github/scripts/rider_check.py` | exit 0 — 26 ok · 0 drifted · 0 broken |
| `uvx ruff check` on both touched scripts | exit 0 — `All checks passed!` |
| `uvx ruff format --check` on both touched scripts | exit 0 — `2 files already formatted` |
| Five instruments for *commits that introduced `Re-read again` into `seal/ledger.md`*, at `979947f9`, `952a247e`, `11b9f9e3`, `55ae1b63` and `origin/main` (217 / 216 / 213 / 204 / 192 commits) | Invariant at all five: `git log -S` 9, rose-from-first-parent 13, differs-from-first-parent 15, rose-against-every-parent 8, differs-from-every-parent 9 |
| Set identity between `git log -S` and differs-from-every-parent over all 217 commits at `979947f9` | The same nine commits; both set differences empty. Rose-against-every-parent's 8 is a strict subset |
| Row census over `seal/ledger.md` and the live fragment at `979947f9`, three definitions | Shared file 625 anchored rows / 759 `cc.rows` / 887 pipe-lines / 128 separators. Fragment 4 / 5 / 6. 887 − 759 is exactly the separator count |
| The same three readings at `11b9f9e3`, `55ae1b63`, `origin/main`, `origin/release/v0.12.3`, `v0.12.2` and `v0.12.1` | 759 / 887 / 625 flat at the first five; 732 / 857 / 601 at `v0.12.1`. `805` appears in none of them |
| Comment-only check over `1d1f072a..952a247e` — every added and every removed line, and any added `def` or `class` | Every added and removed line begins with `#`; no `def` or `class` added; both revisions of both modules give identical syntax trees |
| Comment line length band — census block, rider block, and the six added lines | Census block 73-80, rider block 73-90, added lines 76 and 77. Longest comment line in `evidence_check.py` 138 before the range, 90 after, blamed to `bf82bd3c` on 2026-09-01 |
| Round 2's two paste-ready blocks compared byte-wise against the shipped files | Block 1 verbatim in `correction_check.py`. Block 2 diverges at its seventh line and ends one sentence short of the shipped text |
| Ledger and fragment across `1d1f072a..979947f9` | `seal/ledger.md` unchanged; fragment 6342 bytes at `11b9f9e3` and at `979947f9`. The range touches `round-2.md` and the two scripts only |
| The broad gate — the full suite, the repository-wide lint and the typecheck | not yet, and not run by this round. Withheld by the prompt and assigned elsewhere by `agent-contract` §2. With this round opening nothing that needs a fix, the `sealer` spawn is due |

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
| round-2 | `skills/evidence-check/scripts/correction_check.py#read_blobs`, `skills/evidence-check/scripts/correction_check.py#standing` | round 2's 🟢 — closed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py#OLD_COORD_RE` | round 2's ⬜ — closed for the named site; the class is one name short — n2 |
| round-2 | `tests/test_a_merge_cannot_silently_drop_a_correction.py#ledger_text` | round 2's 🟢 — verified |
| round-2 | `seal/ledger.md`, rows C3 and C4 | round 2's 🟢 — verified |
| round-2 | `skills/evidence-check/scripts/correction_check.py`, `skills/evidence-check/scripts/evidence_check.py` | round 2's 🟢 — verified |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| One comment line at `evidence_check.py:72` runs to 90 characters in a block whose band is 73-80, in the same attached comment run round 2's finding 3 cleaned | A row in `seal/follow-up.md`, or an issue from this pull request if the orchestrator judges a 90-character comment line earns one. Predates the branch by three weeks and no line of it is in the diff | the repository owner |
| Round 2's finding 2 grounds cell names `seal/ledger.md` and the live fragment for a figure that is the shared file alone — 625 against 629 | The record itself, as a correction the closing pass can make while it writes `Fixes checked by` | the orchestrator |
| `correction_check.py`'s module docstring states *37 merge commits, 24 of them with a parent carrying a ledger with markers* | Already deferred in round 2: issue #481. Re-found and not re-litigated | the repository owner |
| Q1 — whether this branch may amend the released `CHANGELOG.md` §0.12.2 | Already deferred in round 1 and carried by round 2: `questions.md` Q1, `overview.md` §*Not verified*, `seal/follow-up.md`, `survivors.md`'s first row | the repository owner |
| Q2 — #469's issue body, whose histogram is neither corpus and sums to 412 | Already deferred in round 1 and carried by round 2: `questions.md` Q2 and `overview.md` §*Not verified* | the repository owner, or the orchestrator |
| The `test_a9_the_leg_asks_the_range_the_pull_request_is_about` slice on a bare literal | Already deferred in round 1 and carried by round 2: `overview.md` §*Not verified* | the repository owner, as an issue from this pull request |
