# 1788360817-the-pull-request-language-is-fixed-inside-a-skill — review round 1

<!-- seal/specs/1788360817-the-pull-request-language-is-fixed-inside-a-skill/rounds/round-1.md
— what this round did, written by the review orchestrator after opening the
coordinates the reviewer named. `docs/review-handoff-protocol.md` carries the
format. -->

| Field | Value |
|---|---|
| Target SHA | ec3e252 |
| PR | none yet |
| Broad gate | not yet — findings are open |
| Fixes checked by | nobody — the fixes landed at d7e609a and round 2, the verifying round, is what opens them; this cell is set to it when that record exists |
| Contract changes | `items` → `configured_language`, `test_the_template_is_one_item_value_table_whose_first_row_is_the_language`, `test_the_check_can_fail`, `test_a_row_of_another_table_ends_this_one`, `test_a_second_table_further_down_is_not_read_as_more_rows` — signature and return type unchanged, the set of returnable values narrowed: a row following a row of another table is no longer returned |
| New units | `tests/test_the_pull_request_language_is_the_repositorys.py#configured_language`, `#LANGUAGE_CODES`, `#UNNAMED`, and eleven cases: `test_the_default_is_stated_where_the_path_is`, `test_every_way_of_not_naming_a_language_lands_on_english`, `test_an_unreadable_config_lands_on_english_too`, `test_the_skill_names_every_way_of_not_naming_one`, `test_a_config_holding_the_templates_default_row_reads_as_english`, `test_a_korean_row_is_what_flips_the_refused_mirror_name`, `test_a_row_of_another_table_ends_this_one`, `test_a_second_table_further_down_is_not_read_as_more_rows`, `test_every_template_is_named_by_a_document_that_ships`. One unit removed: `test_absence_means_english_in_both_of_its_spellings`, whose five cases are now five |
| Needs a fix | yes — 🟡 1 (no document names `templates/config.md`, so the file a repository is told to write has no source), 🟡 4 (this branch drifted two ledger rows in another work item's fragment and the smith's scoped check could not see them), 🟡 5 (a legitimate `seal/config.md` turns a new test red) |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 0 | Stage 1: all three of the issue's done-when rows are in the code. The template exists with the `Pull request language` row defaulting to English; the skill reads it before writing any of the four surfaces; the response language is excluded by name | `templates/config.md`, `skills/commit-pr-convention/SKILL.md:46-80, 84, 106-108, 114, 128, 73-76` | pass | reviewer read; executed 71 passed over the new file and its neighbours, 49 passed over the document-shape tests |
| 🟢 0b | `seal/README.md` is byte-identical to `templates/seal-README.md` | both files | pass | reviewer executed `cmp` |
| 🟡 1 | Nothing in `skills/`, `agents/`, `hooks/`, `docs/` or the READMEs names `templates/config.md`, so a session told to write the file has no source for it; the only mention is `tests/test_docs_line_wrap.py:64`, a line-width list. `templates/parity.md` is named by `skills/parity-setup/SKILL.md:46` and `skills/implement/SKILL.md:176`; `templates/sdd-routing.md` by three readers. The exclusions live in the template, and the test at `:150-152` justifies putting them there by saying the person writing the config reads the template — a path that does not exist | `skills/commit-pr-convention/SKILL.md:58`, `templates/config.md` | open | orchestrator grep confirmed: one hit, in the line-width list. Fix: name the template where the skill tells the reader the file may not exist (reviewer's paste-ready paragraph) |
| 🟡 2 | The root is resolved two ways for the config (`<repo>/seal/` or `<git-common-dir>/seal/`) and one way for the mirror: `SKILL.md:137` and `templates/config.md:38` write `seal/specs/<id>/pr.ko.md` literally. In local mode that path is under the git directory, where `seal/README.md:14-16` says nothing is ever a commit candidate — and the reason the skill gives for the location at `:141-143` ("versioned with the code; survives the merge") is exactly what fails there | `skills/commit-pr-convention/SKILL.md:135-143`, `templates/config.md:37-40` | open | reviewer read. Fix: resolve the mirror's home the same way, and say where it goes when that root cannot be committed |
| 🟡 3 | The absent-file rule answers two absences (no file, no row) and not the third: an empty value, or a file that cannot be read or parsed. The whole design fails toward English; this one direction is unstated, so a session meeting it may stop, ask, or guess | `skills/commit-pr-convention/SKILL.md:61-63` | open | reviewer executed the parser: an empty cell reads as `('Pull request language', '')`. Fix: name every way of failing to name a language and land them all on English |
| 🟡 4 | This branch added three lines to `templates/seal-README.md`, whose whole text is the anchor of two rows in **another** work item's fragment, so the tree now reads `325 ok · 1 drifted` where the base reads `299 ok · 0 drifted`. `overview.md:16` records `27 ok · 0 drifted`, which is true of this item's own fragment and cannot see the rows this change broke. CI does not fail: `.github/workflows/test.yml:88-97` turns drift into a warning and fails only at exit ≥ 2 — so the cost is a stale row folded into `ledger.md` at the release, not a red build | `seal/ledger/1788354065-…md:36, :61` | open | orchestrator executed `evidence_check.py --strict .`: `325 ok · 1 drifted · 0 broken`. Fix: re-read both claims and `--reverify`, then say in `overview.md` that a whole-document anchor makes any edit to that document another item's drift |
| 🟡 5 | `test_the_existing_mirrors_are_consistent_with_the_rule` asserts `seal/config.md` does **not** exist. Its message says the assertion above is wrong "if its row is not English", but the file turns it red whatever the row says — including the template's own default | `tests/test_the_pull_request_language_is_the_repositorys.py:217-220` | open | reviewer executed: a config holding exactly the template's default row makes it `1 failed, 23 passed`. Fix: read the row instead of the file's absence (reviewer's snippet) |
| 🟡 6 | `items()` treats a row of a different table as transparent rather than as the end of this one: a three-cell row between two two-cell rows is skipped and the row after it is absorbed. Same family as the separator-row defect the smith found and fixed | `tests/test_the_pull_request_language_is_the_repositorys.py:248-252` | open | reviewer executed 13 table shapes; twelve fail safely (empty result or a mismatch), this one is silent. Fix: any line that is not a row ends the table |
| 🟡 7 | **Found by the orchestrator, outside this diff.** `.github/scripts/fold_ledger.py` globs `seal/specs/*/evidence-todo.md`, and two work items keep that file at `seal/specs/<id>/rounds/evidence-todo.md` (#79 and #80). The protocol puts the two todo files at the work-item level, not under `rounds/` (`docs/review-handoff-protocol.md:25-31`), so the release guard is blind to those two. Both are drained today, so nothing is hidden now; the first open row written there will pass the release silently | `.github/scripts/fold_ledger.py:47`, `seal/specs/1788331011-…/rounds/evidence-todo.md`, `seal/specs/1788354065-…/rounds/evidence-todo.md` | deferred — not this work item's; see Deferred | orchestrator executed the glob both ways: three files seen, two unseen |
| ❓ 8 | `overview.md:61-64` says `docs/flow.md` was left untouched, and the branch tip `ec3e252` moves one of its lines (the sealer from 0.5.0 to 0.6.0) | `seal/specs/1788360817-…/overview.md:61-64`, `ec3e252` | answered by the orchestrator: the commit is mine, made after the memo, and it is a release-planning decision rather than this work item's. It rides here because `release/v0.5.0` takes no direct push and a one-line docs change does not earn a pull request of its own; the pull request body names it and `overview.md` is corrected | orchestrator |
| ❓ 9 | `docs/one-root-by-lifetime.md:449-450` still calls `pr.ko.md` the owner's per-user setting, which this change makes a function of the repository's row | that line | left open — the issue put the design record out of scope by name, and a reader meeting both sentences is the cost | the repository owner |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: `pytest` over the new file, the line-wrap tests and the first-setup tests | 71 passed |
| reviewer: `pytest` over the document-shape tests (old roots, release hygiene, the work-item set, one-word-one-meaning) | 49 passed |
| reviewer: `cmp seal/README.md templates/seal-README.md` | identical |
| reviewer: `evidence_check.py --strict .` at `ec3e252` and at the base | `325 ok · 1 drifted` against `299 ok · 0 drifted` |
| reviewer: a `seal/config.md` holding the template's default row, then the new test file | 1 failed, 23 passed |
| reviewer: `items()` against 13 table shapes | 12 fail safely; the interleaved second table is silent |
| orchestrator: `evidence_check.py --strict .` | `325 ok · 1 drifted · 0 broken` |
| orchestrator: `grep -rn "templates/config.md"` over skills, agents, hooks, docs, the READMEs, tests | one hit, `tests/test_docs_line_wrap.py:64` |
| orchestrator: `glob("seal/specs/*/evidence-todo.md")` and `…/rounds/evidence-todo.md` | 3 seen by the guard, 2 not |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 7 — two work items keep `evidence-todo.md` under `rounds/`, where the release guard cannot see it | issue #96, on the 0.5.0 milestone and in `docs/flow.md` before the release line, because the release runs that guard | the orchestrator, before the release |
| ❓ 9 — the design record still calls `pr.ko.md` a per-user setting | `docs/one-root-by-lifetime.md:449-450`, named in the pull request body | the repository owner |
