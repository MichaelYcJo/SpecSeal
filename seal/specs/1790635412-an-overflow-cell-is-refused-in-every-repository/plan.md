# Implementation Plan: an overflow cell is refused in every repository

<!-- seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/plan.md — HOW, in phases. -->

Approved 2026-09-29 by the orchestrating session, when `smith` was spawned.

## Summary

Four vertical slices, each ending green and committed. Phase 1 ships the arm
in `evidence_check.py` together with every page that states what the checker
refuses and how it grades it. The printed text and the grading change in one
commit with their pins (§14). Phase 2 makes the commit advisor print the new
verdict. Phase 3 makes this repository's case a caller of the shipped arm,
moves the policy statement onto it, and removes the two ledger rows whose
anchors go. Phase 4 keeps every drifted claim true where it stands, writes the
fragment and the changelog fragment, and runs the survivor sweep.

The branch touches neither `.claude-plugin/plugin.json` nor `CHANGELOG.md`.
The 0.16.0 release preparation moves the version and gathers
`seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/changelog.md`
(`docs/branch-and-release.md`, *The changelog entries arrive as fragments*).
The squash commit's prefix is `feat:`, because this adds a refusal a consumer
meets. `.github/scripts/publish_release_note.py` files `feat` under Features,
and the milestone calls this class a minor release.

## Technical context

- **Where the arm plugs in.** `evidence_check.py#check_ledger` extends its
  findings with `old_format_rows(text)` and `malformed_rows(text)`. The new
  `overflow_rows(text)` goes beside them. `main` owns `totals`, both summary
  lines and the call to `exit_code`. `exit_code` grades `MALFORMED` with
  `DRIFTED`, below `BROKEN`. `OVERFLOW` joins that branch.
- **The walk to extract.** `grounds_cells` splits `unquoted(text)` with
  `cell_rule()`, takes a row followed by a rule row as a header (every cell
  matches `RULE_CELL_RE`), resets on any non-row line, and treats a row with
  no header above it as a fragment row. That logic becomes `ledger_table_rows`, and
  `grounds_cells` keeps only its column choice:
  - the header's index of `Code grounds`, or `-1` for a table without one;
  - `LEDGER_COLUMNS.index(CODE_GROUNDS)` under no header. That is `1` today,
    now derived rather than written.
- **The fence and cell rules are already shared.** `unquoted` blanks only
  closed fences, through `fence_rule()`. That is the shared reader's
  `fence_opener` / `fence_closes` in the plugin's copy, and the vendored pair
  where `evidence-ci` has put the file alone. `cell_rule()` does the same for
  `split_row`. The arm writes no fence or cell reading of its own. B (#584)
  works on other readers and does not touch this file.
- **The docstring that counts walks.** `unverified_check.py#fence_opener`'s
  docstring names "`evidence_check.py#quoted_lines`, which the checker's four
  ledger walks read through". If `ledger_table_rows` takes `grounds_cells`' walk
  and `overflow_rows` reads through `ledger_table_rows`, the count of walks does not
  change and that file is not edited. If the build ends up adding a walk, the
  sentence is corrected in the same commit. Say which in `phases/phase-1.md`,
  because B may edit that docstring in parallel.
- **The notice and its pins.** `LENIENT_NOTICE` is held by
  `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`:
  - a copy of the sentence near its top;
  - `test_the_notice_borrows_the_word_the_failing_gate_prints`, which loops
    over the verdicts the notice must name;
  - the `grading` helper and `test_the_grading_is_one_function_and_the_line_reads_its_answer`,
    whose key tuples list every verdict;
  - `test_the_skill_states_the_grading_exit_code_returns_for_malformed`,
    which asserts the reader table's last header cell is `MALFORMED is`.
  Adding an `OVERFLOW is` column breaks that last assertion. Either the case
  generalises over both columns, or the page states both verdicts in one
  column. Either is fine if both gradings are held against `exit_code`.
- **Output shape.** `main` prints `f"  {status:8} {coord}  {detail}"` under
  each ledger's name. `OVERFLOW` fills the eight exactly. `reverify` prints no
  per-ledger heading, so its `LEFT` line carries `display_name(ledger, root)`
  and the line. Existing cases match the totals as substrings
  (`"0 old-format · 1 malformed" in r.stdout`), so appending `· N overflow`
  keeps them green (read; Q1 has the run confirm it).
- **The advisor.** `hooks/evidence-advisor.py#failing_rows` filters on
  `("BROKEN", "OLD-FORMAT", "MALFORMED")`, and `main` prints one block per
  verdict. `OVERFLOW` joins the filter and gets its own block, headed by the
  number of rows. The module docstring's "Three verdicts … all three are
  printed" becomes four.
- **This repository's case.** In `tests/test_release_hygiene.py`, the
  corpus case reads `ledger_files()` plus `seal/ledger/*.md`. The checker
  reads `resolve_patterns(default_patterns(root))`, which is the same set plus
  `docs/**/_evidence.md` (none in this tree). Reading the checker's own
  listing is what `tests/test_a_folded_statement_names_what_enforces_it.py`
  does for `fold-check`, and it keeps the two from diverging. That is the
  default. The builder may keep `ledger_files()` if the default listing needs
  a `seal/` root the planted tree cannot give cheaply.
- **Rows this branch will drift or remove.** Candidates were found by grep
  over anchors on 2026-09-29. `evidence-check` is the authority, and this
  list is not.
  - **Removed (anchors deleted in phase 3):** C2 in
    `seal/releases/0.15.1.md` and L1 in `seal/releases/0.15.3.md`. Each
    cites units phase 3 deletes. Their claims still hold, now by the shipped
    arm and the corpus case, so each is written anew in the fragment.
  - **Drifted by phase 1:**
    - `evidence_check.py`'s `check_ledger` (0.4.0, 0.8.3, 0.15.3);
    - `exit_code` (0.11.3, 0.15.4, 0.15.5);
    - `LENIENT_NOTICE` (0.11.3, 0.15.5);
    - `main` (0.4.0, 0.8.3, 0.9.0);
    - `reverify` (0.4.0, 0.8.3, 0.15.3, 0.15.4);
    - `grounds_cells` and `malformed_rows` (0.15.4);
    - `skills/evidence-check/SKILL.md` sections (0.8.0, 0.11.3, 0.14.0,
      0.15.5);
    - `skills/evidence-ci/SKILL.md`, `templates/evidence-check.yml`,
      `.github/workflows/test.yml` and
      `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`
      (0.15.5).
  - **Drifted by phase 2:** `hooks/evidence-advisor.py`'s `failing_rows`
    (0.4.0, 0.5.0, 0.15.1, 0.15.4) and `main` (0.4.0, 0.15.4).
  - **Drifted by phase 3:** rows on `docs/the-evidence-ledger.md`'s
    "## A row is a content anchor, and it names no commit" (0.15.1), and on
    the corpus case, beyond C2 and L1.
- **Hazard for every phase: `--reverify` re-stamps every drifted row in the
  file it is given** (`seal/follow-up.md` row 69). Run the lenient
  `bin/evidence-check --ledger <file> .` first. Reverify a file only when
  every row it reports drifted is one this phase re-read. Otherwise write the
  hash by hand from the checker's report. 1790260565's plan used the same
  rule.
- **The records arm will read this directory** once the fragment exists.
  Every compound name these records state in backticks has to exist at the
  tip. The names phase 3 removes sit on lines carrying the `NAME NOT IN
  TREE` marker. The three interface names in `spec.md` exist from phase 1 on.
- **`CLAUDE.md`: judged, nothing in it becomes false.** It names no verdict
  list and does not mention the width case. It says a fragment needs no
  header, and the arm counts a header-less row against the template's
  columns instead. No owner's edit is owed.

**What breaks in six months.**
- **A column added to the ledger template.** The `LEDGER_COLUMNS` pin goes
  red and the constant is updated in the same change. That is the intended
  failure.
- **A consumer's ledger holding a header-less table that is not ledger rows,
  six cells or wider.** It is named `OVERFLOW`, loudly and by line. The
  remedy is to give that table a header, which is the right answer for a
  table that is not ledger rows. 1790260565 accepted the same trade for this
  repository.
- **Work item C's `reverify` edit** lands on the lines this work adds beside
  the `MALFORMED` `LEFT` line. The overlap is two statements, and C is
  sequenced after this squash.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Fold the refusal into `MALFORMED` with its own remedy text | Three shipped sentences go false: the advisor's "malformed Code grounds text", `SKILL.md`'s "`MALFORMED` reads one cell of a row", the template's "a coordinate that does not parse". One word would then carry two meanings, which `CLAUDE.md`'s naming rule and `tests/test_one_word_one_meaning.py` exist to stop | rejected |
| Its own verdict, exit 2 under both readings, like `OLD-FORMAT` | A repository running the lenient recipe `evidence-ci` prints, and this repository's own `ledger` job, go red on update. The owner rejected exactly that for `MALFORMED` on 2026-09-26, and the reason given was not about patch against minor | rejected |
| **Its own verdict, `OVERFLOW`, graded like `DRIFTED` and `MALFORMED`** | A consumer running the bare lenient command sees exit 1 and a notice rather than a failure. The deciding readers (`broad-gate`, the vendored template) still refuse | **chosen** |
| Refuse any width mismatch (`!=`), as the old case did | Refuses short rows in other people's builds, which hide nothing and which no document forbids. More than the owner answered | rejected |
| Read the ledger row's width from `templates/ledger.md` at run time | The vendored copy has no template beside it, so the arm would behave differently in the two copies, or not load | rejected |
| **`LEDGER_COLUMNS` as a constant, pinned to the template by a case** | A template change without a constant change goes red, which is the point | **chosen** |
| Write `overflow_rows` with its own header walk beside `grounds_cells` | Two table walks in one file, which is the divergence this repository keeps undoing, and C would have two walks to choose from | rejected |
| **Extract `ledger_table_rows` from `grounds_cells`; both arms read through it** | A slip in the extraction changes `MALFORMED`. Every existing `MALFORMED` case runs before and after, and A7 is the gate | **chosen** |
| Keep this repository's `overwide_rows` beside the shipped arm | Two rules for one statement, already different in four places (`spec.md` *In* 6) | rejected |
| Delete this repository's corpus case, since the arm now covers the files | The `ledger` CI job is lenient, so an overflowing row on a contributor's pull request becomes a warning where it is a failing test today | rejected |
| **The corpus case calls the shipped arm; a planted-tree case makes it red-able** | The planted case tests the helper, not the real tree's content. The real tree is covered by the checker itself as well | **chosen** |
| Leave `--reverify` silent on an overflowing row, to keep out of C's function | `SKILL.md`'s *Known limits* says every verdict the check names gets a line back, because silence reads as a heal. A new verdict with no line breaks that sentence | rejected |
| Leave the advisor's filter as it is | The advisor's docstring promises every verdict a person must touch either way, and an overflowing row is one. The commit that writes the stray pipe is the one that should hear it | rejected |

## Phases

Vertical slices. Each ends committed, with its narrow run green. The broad
gate is `sealer`'s, not a phase's (`agent-contract` §2). Every new case is
shown red before it is committed (§15), and the phase record says how.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The arm and the pages that state it.** In `evidence_check.py`: `LEDGER_COLUMNS`, `ledger_table_rows`, `grounds_cells` reading through it, `overflow_rows`, the `check_ledger` call, the totals key and both summary lines, `exit_code`'s branch, `LENIENT_NOTICE` naming `OVERFLOW`, and `reverify`'s `LEFT` line with exit 1. Pages: `skills/evidence-check/SKILL.md` (the `--strict` flag row, the reader table except the advisor's cell, a verdict row, the two *Known limits* bullets), `skills/evidence-ci/SKILL.md`'s "1 is not only drift" paragraph, `templates/evidence-check.yml`'s comment, `.github/workflows/test.yml`'s comment and warning, and the command-table row in `README.md` and `README.ko.md`. New module for the arm with A1–A6, A8, A9 and A13. The lenient-notice module extended for A11. The changelog fragment's entry. | (1) A1, A2, A5, A9 and A13 **seen red** at `11e3104c`'s checker, run from a saved copy. A6 seen red with one column renamed in the constant. A11's page assertions seen red against `SKILL.md` before its edit. (2) A7: `bin/test tests/test_a_row_points_by_content.py tests/test_evidence_check.py` green before the extraction and after it, unchanged. (3) `bin/test` over the new module, `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, `tests/test_evidence_check.py` and `tests/test_a_row_points_by_content.py`. (4) `bin/evidence-check .` over this tree: `0 overflow` on every ledger (Q2). (5) Mutation: `overflow_rows` returning `[]`, and `>` changed to `>=`, each turns A1 red. | dd9f89e6 |
| 2 | **The commit hears it.** `hooks/evidence-advisor.py`: `OVERFLOW` in `failing_rows`' filter, its own block in `main`, and the module docstring's count and list. `SKILL.md`'s reader table fills the advisor's cell for `OVERFLOW`. A10 in `tests/test_dispatch.py`. | (1) A10 **seen red** against phase 1's advisor (no block printed). (2) `bin/test tests/test_dispatch.py tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`. (3) The pull-request lines `CONTRIBUTING.md` §*What a change to a gate must carry* asks for are drafted into `phases/phase-2.md`: the case seen red; the failure direction (it never blocks, so a crash loses one reminder); a prompt budget of zero. | ba9f879b |
| 3 | **This repository's case is a caller.** `tests/test_release_hygiene.py`: the corpus case's walk becomes a helper taking a root and calling `evidence_check.overflow_rows` over the checker's own listing. The corpus case calls it on `ROOT`. A planted-tree case calls it on a tree with one overflowing fragment row (A12). The old rule's five units and its two unit cases are deleted, since their shapes are in phase 1's module. `docs/the-evidence-ledger.md`: the paragraph's last sentence says the shipped checker names such a row `OVERFLOW` in every repository that installs the plugin, and this repository's case holds its own ledgers to it on every pull request. The `Enforced by:` line names `skills/evidence-check/scripts/evidence_check.py::overflow_rows` and the corpus case. C2 (`0.15.1.md`) and L1 (`0.15.3.md`) are removed from their files. 1790260565's `questions.md` Q1 is ticked. | (1) The planted case **seen red** with the helper's call to the arm replaced by `[]`. (2) `bin/test tests/test_release_hygiene.py tests/test_a_folded_statement_names_what_enforces_it.py tests/test_a_document_has_room_for_the_next_fold.py`. (3) `grep` over `tests/` for the five deleted names returns nothing. | e1ea265f |
| 4 | **The ledger stays true.** `seal/ledger/1790635412-an-overflow-cell-is-refused-in-every-repository.md` holds the new claims: the arm and its reading (phase 1), the advisor (phase 2), and the two rewritten claims C2 and L1 carried (phase 3). Every row `evidence-check` reports drifted by this branch is re-read in the file it stands in and gets a dated `Re-read … by work item 1790635412 (#585)` note, or `Corrected <date>` where the edit made it false. Hashes follow the hazard rule above. The changelog fragment is complete. `survivor-check` over the branch, with a `survivors.md` row for each released text it reports. | (1) Lenient `bin/evidence-check .` unscoped: no drifted, broken or overflowing row that this branch caused. (2) `bin/evidence-check --strict .`: exit 0. (3) `bin/survivor-check` over the branch: nothing unexempted. (4) `bin/test tests/test_the_ledger_fragments_fold_at_release.py tests/test_a_record_states_what_the_tree_has.py`, so the fragment folds and these records name only what the tree holds. | |

## Operational impact

- **A repository that installs 0.16.0 can see a ledger that passed start
  failing.** `broad-gate` and the vendored CI template pass `--strict`, so a
  row with more cells than its header is exit 2 there. A bare
  `evidence-check .` and `evidence-ci`'s lenient recipe get exit 1, with the
  notice naming `OVERFLOW`. The finding names the line and the remedy
  (escape the pipe as `\|`). A header-less table of six cells or more that
  is not ledger rows is named the same way, and the remedy there is a header.
- **Both totals lines gain a field at the end**, `· N overflow`. A reader
  matching the line up to `malformed` is unaffected. `broad_gate.py` reads
  only up to `broken`.
- **`--reverify` exits 1** on a ledger holding an overflowing row, and names
  it.
- **The commit advisor prints one more kind of block.** It never blocks a
  commit.
- **This repository's own case no longer refuses a row with fewer cells than
  its header.** No such row exists (`spec.md` *Out*).
- No migration, environment variable or dependency.
