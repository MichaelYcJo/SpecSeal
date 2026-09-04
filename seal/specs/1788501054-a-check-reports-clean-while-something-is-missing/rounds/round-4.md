# 1788501054-a-check-reports-clean-while-something-is-missing — review round 4

| Field | Value |
|---|---|
| Target SHA | 97e9b52 |
| Ran by | specseal:warden on opus |
| PR | not yet opened |
| Broad gate | not yet — no broad run has happened on this branch at all, and it is now deliberately held until 🔴 1 is fixed: the suite is not green at HEAD, so a broad run taken first is spent rather than banked |
| Fixes checked by | nobody — this round's fixes are not yet written; the round that opens them sets this cell |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — one 🔴 and six 🟡. The 🔴 is the orchestrator's own record cell, and it makes this repository's own suite red at HEAD: `round-3.md`'s `New units` carries prose inside its sixth entry, `depth_problems` refuses it, and the hygiene workflow runs that check on every pull request. The heaviest 🟡 is that one of the four limits round 3's fix pass recorded as unreachable is false — `says_not_yet`'s separator guard is load-bearing for a bare `none`, and removing the conjunct the paragraph calls redundant turns 19 cases red |
| Loses a record or crashes | no |

- [ ] Pass

<!-- The second verifying round of this run, and it reopened the run again.
The floor's bound allows it: a verifying round that opens something IS a
finding round, and the count stops at the first later record whose `Needs a
fix` says `yes`, this record included.

Written and committed before the fix pass it commissions, so both fix-surface
rows start pending. That is also why 🔴 1 cannot be fixed by this file: the
malformed cell is in `round-3.md`, and the fix belongs to the pass this record
opens. `read_record` reads `git show HEAD:<rel>`, so the branch stays red until
that fix is COMMITTED — a working-tree edit does not clear it. -->

## What this round was asked

The verifying round at `git diff 1171182..97e9b52` — **five commits**, and the
prompt said so as a count it told the round to re-take, because round 3's
prompt had said three where there were four. The round re-took it: `git
rev-list --count` returns 5.

Round 3's eight verdicts as the agenda, and what `round-3.md`'s `New units`
names — six units plus two widened cases — as the finding surface.

**Nine specific things to try to break**, named with coordinates: the four
mutations the fix pass recorded as unreachable rather than closing; the two
`# RIDER:` comments; the six new and two widened cases against §15; the depth
claims as a measurement; class C's nine ledger rows across three files; the
in-place correction of `round-2.md:10` and the line it argues; **the
orchestrator's own two rows, which sit inside the target**; class B, which had
then recurred three rounds running; and 🟡 5's judgment with the two claims it
rests on kept separate.

**And the correction it carried:** the orchestrator's prose about a record had
been wrong five times on this branch, none of them visible to a check, and the
instruction was to open the record rather than the prose about it — including
the prose in that prompt. It found the sixth, and the sixth is the first one a
check can see.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `round-3.md`'s `New units` cell is malformed. The prose after the sixth `;`-separated entry lives INSIDE that entry, and `depth_problems` refuses an entry carrying more than one unit or a comma under a single `(depth N)` | `rounds/round-3.md:11` | open | **Executed** by the round in a `--no-local` clone, and re-executed by the orchestrator in the worktree: `test_this_repositorys_own_round_records_pass_the_per_record_checks` is **green at `ae271ba` and red at `97e9b52`**, and `chain_check --baseline origin/release/v0.8.0` exits 1 on **three** lines where two were expected — the third an error rather than a notice. `.github/workflows/hygiene.yml` runs that check on every pull request. The proposed replacement returns `([], [], [], [])` from `depth_problems` and takes the case to 1 passed once committed; it is below the probe table |
| 🟡 2 | The same cell gives one reason for two widenings and it is false for one of them. `says_not_yet` is round 2's own `New units` entry, so a unit answering a finding inside it is depth 2; `skipped_by_narrowing` was created by this branch's **phase 2**, not by a round's fix pass, so a unit there is depth 1 and that case was widened by choice | `rounds/round-3.md:11`, against `phases/phase-7.md` | open | **Read**, and confirmed against the two earlier records: neither `round-1.md`'s nor `round-2.md`'s `New units` names `skipped_by_narrowing`. The fix pass had written the correction down and the record wrote the corrected-away reasoning back in |
| 🟡 3 | One of the four limits round 3's fix pass recorded as unreachable is **false**. The docstring says the two guards duplicate `says_none`'s and cannot change the answer; `says_none` returns True by two routes and the second, `s == NONE_WORD`, leaves nothing after the word | `chain_check.py:1621` the claim, `:1633` the code, `:1563` the rider, `overview.md:66` the fourth copy | open | **Executed**, cache purged: dropping the `not rest` conjunct alone turns **19 red**; deleting the guard whole leaves 136 passing; deleting the `startswith` guard leaves 136 passing. Directly, `says_none("none")` is True and `says_not_yet("none")` is False by that conjunct. A bare `none` is what the template's own instruction produces. A recorded limit that is wrong is worse than one that is missing — this one tells the next battery to delete a load-bearing line |
| 🟡 4 | The rider stands in for a pin depth allows. Depth refuses a new **unit**, not a new **assertion**, and `test_the_declared_limit_names_what_escapes_with_the_words_unchanged` already loops over three files | `chain_check.py:1563`, `tests/test_a_record_precedes_the_fixes_it_commissions.py:738` | open | **Executed** — a `test_tmp_*` probe asserting the corrected wording passes at HEAD and fails when round 3's backwards sentence is restored; probe deleted. The rider's other claim is stale rather than wrong: the PREFIX behaviour IS held by a case, and what has no case is the docstring sentence |
| 🟡 5 | The new fallback sentence is false off Windows, which is round 1's 🟡 9 restated one branch over. `os.path.normcase` folds case on Windows alone, so two spellings of one file on a case-insensitive filesystem elsewhere get two identities | `evidence_check.py:949-951`, and the reachability paragraph at `:958-963` | open | **Executed** on this machine's case-insensitive filesystem: one inode, two fallback identities. The behaviour is the declared over-reporting direction and is not wrong; the sentence is. The second paragraph explains reachability through *CPython zeroes the inode on Windows alone* where the fallback is reached by `OSError` on every platform — `normcase` does survive mutation, so the limit's conclusion holds and only its reason is false |
| 🟡 6 | The declared limit is written in five places and pinned in three, and the pinning case's own docstring says three | `tests/test_a_record_precedes_the_fixes_it_commissions.py:733`, against `phases/phase-7.md:145` | open | **Read**, enumerated by grep over the tree. `phase-7.md`'s removal table names five copies; the case covers the spec, the ledger fragment and the changelog, leaving `chain_check.py:1595` and `overview.md:39` unpinned. That is the *a correction reaches one copy and not the rest* class the case exists to close, inside the case that closes it |
| 🟡 7 | `round-1.md`'s `Fixes checked by` was corrected in place with no trace in the record. A reader of that file cannot tell the reach-back was filled two rounds late | `rounds/round-1.md:9` | open | **Read**. The precedent phase 7 cites marks its correction inside the cell; this one is marked only in `phase-7.md`'s removal table. The obvious fix is refused by the checker: `CHECKER_RE` is `^round-\d+(?:\.md)?$`, so prose appended to the cell silences the arm. The record's trailing HTML comment is the place |
| 🟢 8 | Round 3's 🟡 1 — the arm's key is a cell the same lapse leaves unwritten | `rounds/round-1.md:9`, `docs/review-chain-spec.md` | answered | **Executed**: the cell reads `round-2` and `chain_check.py` prints nothing for that record. The limit is written in four places and pinned — mutating the sentence in the spec **or** in the template turns `test_a_forgotten_checker_cell_leaves_the_arm_nothing_to_key_on` red, both executed. The design half is deferred as `questions.md` Q4; the record's own trace is reopened as 🟡 7 |
| 🟢 9 | Round 3's 🟡 2 — two re-stamped ledger rows carried no re-read clause | `seal/ledger.md`, two fragments | answered | **Executed**, row by row: over the target range `changed=11 restamped=9 restamped_with_clause=9`, and over the whole branch `restamped=11 with_clause=11`. Nine rows across three files, each clause saying what the re-read FOUND. The two changed-but-not-restamped rows are R4 and R8, neither of which R6 obliges. The count has moved every round — three, four of eight, eight of ten, now nine of nine — and this is the first round it balances |
| 🟢 10 | Round 3's 🟡 3 — the terminal value missing from the spec's table | `docs/review-chain-spec.md:655` | answered | **Executed**: the row is there and pinned — mutating its text turns `test_the_terminal_value_is_in_the_specs_table_with_what_it_costs` red. Whether the arm should also REFUSE that pair is deferred as `questions.md` Q3 |
| 🟢 11 | Round 3's 🟡 4 — `says_not_yet`'s docstring stated its own match backwards | `chain_check.py` | answered | **Read**: it now says the constant is the prefix and the reason is what carries it. The pin was declared impossible and is not — reopened as 🟡 4 |
| 🟢 12 | Round 3's 🟡 5 — the declared limit narrower than the limit that exists | `docs/review-chain-spec.md`, ledger R7 | answered | **Executed** at HEAD, eleven spellings: the three declared escapes reproduce, and the plain template value, the en dash, the no-space form and the emphasised form are all still caught. The semicolon and comma spellings both escape, so the two are interchangeable. Nits are 🟡 6 and 🟡 3 |
| 🟢 13 | Round 3's 🟡 6 — `st_ino` over `st_dev` held by nothing | `evidence_check.py` | answered | **Executed**: the `st_dev` swap now dies, and so does dropping the truth test entirely. `test_two_devices_that_share_an_inode_number_are_two_ledgers` dies under `(st_ino,)` alone |
| 🟢 14 | Round 3's 🟡 7 — nothing pinned that the phrase must START the reason | `chain_check.py` | answered | **Executed**: `NOT_YET in rest` now turns `test_a_reason_the_checker_does_not_recognise_passes` red. Round 3's surviving mutation is dead |
| 🟢 15 | Round 3's 🟡 8 — `Contract changes` naming one call site where there are two | `rounds/round-2.md:10` | answered | **Read**: both second call sites are named and the correction is marked as round 3's. The line the fix pass argues — a round record's field rows are parsed and read as a finding surface, a phase record's prose asserts about its own moment — is sound and now written down. `phases/phase-3.md:53` and `phase-6.md:49` keep their stale sentences on the other side of it, both confirmed present. The one uneven application is `round-1.md:9`, which is 🟡 7 |
| 🟢 16 | The orchestrator's two rows at `97e9b52`, re-taken over the wider range | `rounds/round-3.md:10-11` | answered | **Executed**, AST comparison of `1171182` against `97e9b52` with docstrings stripped: **zero** top-level units added, removed or changed in either checker, so `Contract changes | none` is accurate and the range measured is wider than the row cites. `New units` names exactly the six the AST diff finds added, and both widened cases show as changed rather than added. What is wrong with the cell is its FORM and its REASON, not its content — 🔴 1 and 🟡 2 |

## Executed probes

| What was run | Result |
|---|---|
| the five changed suites plus the rider suite, at HEAD in a `--no-local` clone | **1 failed, 217 passed** — the failure is 🔴 1 |
| the same one case at `ae271ba` and at `97e9b52` | 1 passed · 1 failed — `97e9b52` is where the branch went red |
| the same case, re-run by the orchestrator in the worktree | **1 failed** — the refusal names the sixth entry and quotes the prose inside it |
| `chain_check.py --baseline origin/release/v0.8.0`, by the round and again by the orchestrator | exit 1, **three** lines; the third is an error, and `round-1.md` and `round-2.md` print nothing |
| the proposed `New units` cell through `depth_problems`, then committed in the clone | `([], [], [], [])` · **1 passed** |
| six mutations across `says_not_yet` and `skipped_by_narrowing`, cache purged between runs | 3 died, 3 survived — the `not rest` conjunct is 🟡 3, at **19 red** when it alone is dropped |
| nine §15 mutations, one per new or widened case | **nine died** |
| a `test_tmp_*` probe pinning the corrected prefix sentence | green at HEAD, red under round 3's wording — probe deleted |
| eleven cell spellings through `says_none` and `says_not_yet` | the three declared escapes reproduce; the semicolon and comma forms both escape |
| the fallback identity for two case spellings of one file, on a case-insensitive filesystem | one inode, two identities — 🟡 5 |
| AST comparison of top-level units over `1171182..97e9b52`, docstrings stripped | 0 changed in either checker; 6 added; both widened cases changed |
| row-by-row ledger comparison over the target range and over the branch | `restamped=9 with_clause=9` and `restamped=11 with_clause=11` |
| `evidence_check.py .` **unscoped**, no `--reverify` | exit 1, `529 ok · 1 drifted · 0 broken` — S8 alone at `@45edf260` |
| `uvx ruff check` on the four changed Python files · `bin/unverified-check` | All checks passed · exit 0 |
| twelve doc- and record-reading suites | **242 passed** |
| `git status --porcelain` and `git rev-parse HEAD` after the round | empty, `97e9b52` — HEAD did not move, probe and clone removed |

The replacement the fourth row ran, which is 🔴 1's fix — the six entries alone,
with the widening sentence moved out of the cell and corrected per 🟡 2:

```
| New units | `test_a_forgotten_checker_cell_leaves_the_arm_nothing_to_key_on` (depth 1) → pytest only; `test_the_terminal_value_is_in_the_specs_table_with_what_it_costs` (depth 1) → pytest only; `test_the_declared_limit_names_what_escapes_with_the_words_unchanged` (depth 1) → pytest only; `test_two_devices_that_share_an_inode_number_are_two_ledgers` (depth 1) → pytest only; `test_the_skipped_set_is_subtracted_from_the_list_the_defaults_come_from` (depth 1) → pytest only; `test_one_file_matched_by_two_patterns_is_read_once` (depth 1) → pytest only |
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1, 2, 3 | the re-stamped `seal/ledger.md` rows and the two fragments | Four rounds, four different counts of one class, and this is the first that balances. A fifth round opens it to check the arithmetic did not move again |
| round 3 | `chain_check.py#says_not_yet` | Round 3 found one surviving mutation here, round 4 found the paragraph written about the guards is false. Two rounds running, the same unit |
| round 3 | `evidence_check.py#skipped_by_narrowing` | Round 3 closed the identity test, round 4 found the sentence explaining the fallback false off Windows. Same unit, same shape |
| round 4 | `rounds/round-3.md:10-11` and `rounds/round-1.md:9` | The orchestrator's own cells. One makes the branch red and one was corrected without a trace |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| **The broad gate — the full suite, the repository-wide lint and the typecheck.** Still not run at all on this branch, and now held on purpose: the suite is not green at HEAD, so a broad run before 🔴 1's fix is spent rather than banked | `overview.md` §Not verified | the orchestrator, after 🔴 1 is fixed and the rounds settle |
| `plan.md:43`'s *575 cases green across the seventeen suites*, taken at `e94c3de`. Seventeen suites is the broad run §2 reserves, so the round did not re-take it. It can be true of `e94c3de` and false of HEAD | `overview.md` §Not verified | the orchestrator, at the broad run |
| Whether `st_ino == 0` actually arrives on `windows-latest` | `overview.md` §Not verified | the windows CI leg at this pull request — carried from rounds 2 and 3, unchanged |
| `questions.md` Q3 and Q4 — whether the arm should refuse a pending row beside `no fixes to check`, and whether it should key on the sibling records rather than `Fixes checked by`. Both confirmed written as questions with three labelled options and a stated current answer, neither decided | `questions.md` | the repository owner |
| `questions.md` Q2 and `seal/ledger.md` S8 | carried from rounds 1, 2 and 3 | the repository owner |
| The orchestrator's prose about a record was wrong a **sixth** time, and this one a check could see: the malformed cell at 🔴 1 is the same class as the five before it, arriving in a cell rather than in a prompt. The five before it were caught only because a round was told to open the record instead of the prose about it | this row | nobody yet — no check sees the class, only this instance. `docs/flow.md` has no numbered row for it |
