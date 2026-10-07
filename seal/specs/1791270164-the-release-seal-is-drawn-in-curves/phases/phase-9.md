# 1791270164-the-release-seal-is-drawn-in-curves — phase 9

| Field | Value |
|---|---|
| Phase | 9 |
| Commit | 14c24b95 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md`'s phase 9 row: the changelog fragment rewritten for the open layout, the 28-cell frame and the placeholder S naming #857, an entry for the release PNG, and one for the gallery if it is to be named; the ledger fragment's corrected rows rewritten, rows for S1–S11 added, the released rows the build falsified corrected and the re-reads it moved written; `overview.md` closed; `handoff.md` retired; `survivors.md` brought up to date; `evidence-check --strict .` and `survivor-check --range origin/release/v0.20.0...HEAD` clean.

The spawn added the figures to start from — phase 6's report of 114 drifted, 15 broken and 28 refused — and `plan.md`'s Status for phases 7, 8 and 9.

## What this phase found

**At the start the strict check read 169 drifted, 28 broken and 26 refused.** Phases 7 and 8 had moved more coordinates since phase 6's count: the release script and its cases, the line-wrap list, `CONTRIBUTING.md` §*Running the checks* and the checklist's §6. Every row carrying a drifted or broken coordinate was printed with its claim (a scratch script over the report) and read against the code before anything was written.

**Sixteen released rows were false, and each has a `Corrected ·` row.** 0.10.0 S2; 0.12.2 R5; 0.15.7 N7; 0.17.0 B1, B2, L1, L2, L3, L4, N5, N9, N10, P1 and P2; 0.18.0 D2, R1, R2, C1 and W3. B1, B2, L1–L3, S2 and D2 were this fragment's own corrections, rewritten in place for the open layout, as `plan.md` §Alternatives says a correction of a row that never shipped is. The rest are new. 0.15.7 N7 was the one broken citation that was not a removed unit: its claim also gave the ladder's three rungs, and it cited `test_several_files_come_out_as_one_message_oldest_first`, which phase 6 renamed. <!-- NAME NOT IN TREE -->

**Every other drifted row was read and holds.** `evidence-check --reverify --into seal/ledger/1791270164-…md --checked 2026-10-07` re-stamped 22 coordinates in place across three fragments — this one, `1791270161-…` and `1791270165-…`, whose rows phases 5–8 had drifted through `skills/verify/SKILL.md`, `VERSIONS_OF_ANOTHER_PRODUCT`, `OUT_OF_CLASS`, `test.yml`'s `pytest` job and `CONTRIBUTING.md` — and wrote 20 `Re-read ·` rows here for released rows, naming no row it left. A second run after `d6839f6e` wrote the 21st, for 0.18.0 R3, whose `add_pillow` and failed-install case that commit moved; R3's claim holds. A re-read of a row another work item's fragment holds is that fragment's row re-stamped in place, the remedy `docs/the-evidence-ledger.md` names for a citation into a fragment. `1791270165-…`'s `Re-read · P1` is false like the row it reads, and is superseded by this fragment's `Corrected · P1` rather than edited.

**The fragment's own new rows are S1, S3a, S4a, S7, S9 and S10.** S2 and S2a are `Corrected · L2`, S3 is L1, S4 and S11 are L3, S5 is B2, S5a is N5, P1 and P2, S6 is R1, and S8 is L4 — one claim each, in the row the released claim it replaces already had.

**The 26 refusals were names this work item's own records cite and the tree no longer has.** Each line now carries `NAME NOT IN TREE`: five in `spec.md` §*What phase 3 built*, ten in `plan.md` (the case lists of §*Technical context* and §*What phases 5–6 re-aim*, and the phase 9 row's `R0_CELLS`), and eleven in phases 1–3's records. The framer's two files took a marker and no other change. Phase 8's record added one more, for `broken_compose`.

**One survivor was live, and it was a sentence a person reads.** `bin/test`, topping up an adopted environment, printed that Pillow *draws the release seal the suite's pixel case pins*. It now says Pillow is what the pixel case decodes the seal with, and `test_a_failed_pillow_install_is_a_sentence_and_pytest_is_still_called` pins the sentence, seen red through `bin/mutation-check` with the old one put back (`d6839f6e`). The other 32 places the range reported are `survivors.md`'s new rows: released ledger rows this fragment corrects, released work items' frames and memos, a case that asserts a removed sentence is absent, and a comment telling a row's history.

**`handoff.md` described the 2026-10-07 machine move at phase 2** and no state since; it is removed. `routing.md` still says the session *leaves `handoff.md` here*; that file is the orchestrating session's and is left as written.

**What was run.** `bin/evidence-check --strict .` exit 0 (`total: 6779 ok · 0 drifted · 0 broken`, nothing refused). `survivor-check --range origin/release/v0.20.0...HEAD --exempt seal/specs/1791270164-…/survivors.md` exit 0, *every survivor is excused by a row above (48)*; without `--exempt` it reads no exemption file and exits 1 over the same 48. The S8 `grep` returns only history: the module docstring's and comments' accounts of the retired sheet, `panel`'s history paragraph, the gallery's README, and an unrelated *bucketed by area*. `bin/test tests/test_the_suite_has_a_command_that_is_cheap_twice.py`, 98 passed. The stamp, panel, range and steps slices ran once at `2753ce1d`, 559 passed, to ground the rows' **Executed** cells.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `handoff.md` | nowhere: `overview.md` §*Where the run stopped* and `plan.md`'s Status column say where the run stands |
| the fragment's 14-cell and parchment-sheet claims (`Corrected ·` S2, B2, L1, L2, L3, D2) and its `Re-read ·` N7 and L4 | the same rows rewritten for the open layout, and `Corrected ·` N7 and L4 |
| the changelog's two 14-cell entries | five entries: the open layout, the placeholder S, the rows, one stamp per message, the release PNG |
