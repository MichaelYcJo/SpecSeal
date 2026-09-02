# 1788360817-the-pull-request-language-is-fixed-inside-a-skill — review round 2

<!-- The verifying round for round 1's fixes (target: the diff 1280de9..d7e609a).
It opened a 🔴 and six 🟡, so it is a finding round and consumes the cap: two
of three used, five allowed while a 🔴 is open. Written by the review
orchestrator after opening the coordinates. -->

| Field | Value |
|---|---|
| Target SHA | d7e609a (the fix diff from 1280de9); HEAD f075bf7 at review time, record-only commits after it |
| PR | none yet |
| Broad gate | not yet — a 🔴 is open |
| Fixes checked by | round-3 |
| Contract changes | `items` → `configured_language`, `test_the_template_is_one_item_value_table_whose_first_row_is_the_language`, `test_the_check_can_fail`, `test_a_row_of_another_table_ends_this_one`, `test_a_second_table_further_down_is_not_read_as_more_rows`, `test_a_separator_below_the_rows_ends_the_table`, `test_a_repeated_header_ends_the_table`, `test_junk_above_the_first_row_is_still_tolerated`; `configured_language` → `test_the_existing_mirrors_are_consistent_with_the_rule`, `test_a_config_holding_the_templates_default_row_reads_as_english`, `test_a_korean_row_is_what_flips_the_refused_mirror_name`, `test_every_way_of_not_naming_a_language_lands_on_english`, `test_an_unreadable_config_lands_on_english_too`, `test_the_reader_finds_a_config_under_the_git_directory`, `test_the_tree_root_still_wins_over_the_git_directory`. Both keep their signature and return type; `items` no longer returns a row after a separator or a repeated header, and `configured_language` may now return a value read from under the git directory |
| New units | `tests/test_the_pull_request_language_is_the_repositorys.py#mirror_to_refuse`, `#config_homes`, `#shipped_templates`, `#unreachable_templates`, and nine cases: `test_a_language_this_file_has_no_code_for_does_not_raise`, `test_the_reader_finds_a_config_under_the_git_directory`, `test_the_tree_root_still_wins_over_the_git_directory`, `test_the_mirrors_home_is_resolved_and_excludes_the_git_directory`, `test_a_separator_below_the_rows_ends_the_table`, `test_a_repeated_header_ends_the_table`, `test_a_mirror_named_for_a_country_is_caught`, `test_junk_above_the_first_row_is_still_tolerated`, `test_the_templates_check_reads_prose_only_and_descends`. No unit removed |
| Needs a fix | yes — 🔴 1 (`LANGUAGE_CODES[configured_language()]` raises `KeyError` for any language the template licenses and the dictionary does not hold, so round 1 🟡 5 is not closed), 🟡 2 (`configured_language` resolves the root one way where the skill resolves two, which is round 1 🟡 2 reproduced inside its own fix), 🟡 4 (the templates check admits a Python comment, so two templates are as unreachable as `config.md` was); 🟡 3, 5, 6, 7 and ❓ 8 are smaller |

- [ ] Pass

## Verdicts

Round 1's items first, then what this round opened.

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r1 🟡 3 | an empty value and an unreadable file had no stated direction | `skills/commit-pr-convention/SKILL.md:62-68` | answered — the fix is round 1's, this round reproduced its closure | reviewer executed all five shapes, a `config.md` that is a directory included; every one answers English |
| r1 🟡 4 | this branch drifted two rows of another item's fragment | `seal/ledger/1788354065-…md:36, :61` | answered — the fix is round 1's, this round reproduced its closure | reviewer executed `evidence_check.py --strict .` unscoped: `335 ok · 0 drifted · 0 broken`, and opened `templates/seal-README.md` against both claims rather than trusting the re-hash. Both hold |
| r1 🟡 6 | `items()` let a row of another table through | `tests/…:288-293` | answered for the shape round 1 named; the claim written around it is wider than the code — this round's 🟡 5 | reviewer executed the round-1 shape (fixed) and two more (not) |
| r1 🟡 5 | the mirror case asserted `seal/config.md` is absent | `tests/…:226` | **open** — it reads the row now and then indexes a three-entry dictionary with it, so a legitimate config still turns it red. This round's 🔴 1 | orchestrator opened `:225` and `templates/config.md:24-26`; reviewer executed a `French` config: `KeyError`, not an assertion |
| r1 🟡 1 | no document named `templates/config.md` | `skills/commit-pr-convention/SKILL.md:70` | answered for `config.md`; the directory-wide check meant to generalise it passes two templates that are not reachable — this round's 🟡 4 | reviewer read and executed the corpus grep |
| r1 🟡 2 | the mirror's home spelled one way | `SKILL.md:145-160`, `templates/config.md:44-49` | answered in prose; the executable reader shipped in the same fix repeats the defect — this round's 🟡 2 — and no case pins the prose — this round's 🟡 3 | reviewer read both documents and executed the reader against a local-mode fixture |
| r1 ❓ 8 | the memo said `docs/flow.md` was untouched | `overview.md:78` | answered for one of the two lines the branch now carries there — this round's 🟡 6 | reviewer read `git log main..HEAD -- docs/flow.md` |
| r1 `Starts from` | the new column in the SDD table | `skills/implement/SKILL.md` | pass | reviewer opened each named template and checked real work items carry its headings in its order: `spec.md` 12 of 13, `plan.md` 13 of 13, `overview.md`'s banner 13 of 15 |
| 🔴 1 | `forbidden = f"pr.{LANGUAGE_CODES[configured_language()]}.md"` raises `KeyError` for any value outside the three the dictionary holds. `templates/config.md:24-26` licenses "a language's English name" in as many words, and says the reader is a model rather than a lookup table — so `French`, or an emphasised `**Korean**`, is a legitimate config that breaks the check. Round 1 🟡 5 was exactly "a legitimate config turns this red" | `tests/test_the_pull_request_language_is_the_repositorys.py:225` | open | orchestrator opened the line and the template's licence; reviewer executed a `French` config: `1 failed`, a `KeyError` traceback rather than a message. Fix: `LANGUAGE_CODES.get(...)` and `pytest.skip` naming the language, since a table that must list every language is always one short |
| 🟡 2 | `configured_language` joins `<root>/seal/config.md` and stops, while `SKILL.md:46-50` — the sentence its docstring says it implements — resolves `<repo>/seal/` **or** `<git-common-dir>/seal/`. A local-mode repository's config is invisible to the one executable model of a session's reading this branch ships, and `test_the_root_is_resolved_rather_than_spelled` pins the skill saying two places beside a reader that knows one | `tests/…:307-315` | open | reviewer executed against a `.git/seal/config.md` holding a Korean row: returned `English`. Fix: try both homes in order (reviewer's snippet); `tests/conftest.py:178-185` already has the git-dir helper if the shell-out is preferred |
| 🟡 3 | round 1 🟡 2's prose fix is pinned by no case, in the file whose stated method is pinning prose ("each one pins a phrase chosen so that the drift it guards against cannot survive it"). `tests-todo.md` prescribed four rows and 🟡 2 was not among them, so nothing was skipped — the result is that the whole fix is prose a later edit can undo without a red build | `skills/commit-pr-convention/SKILL.md:145-160`, `templates/config.md:44-49` | open | reviewer read. Fix: the reviewer's three-assertion case over both documents |
| 🟡 4 | the templates check excludes `tests/` because "a test naming a template is the mention that looks like a reader and is not", then takes its corpus from `skills agents hooks docs …`, which hold Python. Two templates pass on nothing but comments: `templates/sdd-round.md` on four in `skills/code-review/scripts/chain_check.py:368, 841, 1083, 1104`, and `templates/ledger.md` on one Korean worked example in `skills/writing-style/SKILL.md:159` where the file is the specimen, not the subject. Worse, `skills/implement/SKILL.md:87-90` says `seal/ledger.md` is "created empty" while `templates/ledger.md` is 3 KB the live file visibly started from. Two silent narrowings beside it: the glob returns a subdirectory as one entry and never descends, and it skips dotfiles | `tests/…:436-489` | open | reviewer executed the corpus grep. Fix: narrow the corpus to prose documents and widen the glob to `**` (reviewer's snippets), then close the two by naming them — one sentence in `skills/code-review/SKILL.md`, one replacing "created empty" |
| 🟡 5 | the comment at `items()` and the ledger row both say "any line that is not a row of this table ends it", and two shapes do not end it: a separator below the rows, and a repeated `\| Item \| Value \|` header. `SEPARATOR` and `HEADER` are both tested before `ROW` and both `continue` — the round-1 defect one line further along. Nothing answers wrongly today because both callers read the first match | `tests/…:288-293`, `seal/ledger/1788360817-…md:50` | open | reviewer executed both shapes. Fix: a separator below the rows breaks; correct the row's claim to what the code does |
| 🟡 6 | the memo's correction names `ec3e252` and there are two: `e71ed28` also touches `docs/flow.md`, adding the `#96` row where round 1 deferred 🟡 7 — a review round's decision rather than this item's implementation. Both are the orchestrator's and both are defensible; a reader checking the memo against the branch finds the same mismatch round 1 found | `overview.md:78` | open | orchestrator confirms both commits are mine. Fix: the reviewer's replacement paragraph, naming both |
| 🟡 7 | the mirror case narrowed from `set(mirrors) == {"pr.ko.md"}` to `forbidden not in mirrors`, which is right in principle and drops the check that a mirror is named for a language at all. `pr.kr.md` — `kr` is the country, `ko` the language — is the mistake twelve files are one copy away from, and it would stay green | `tests/…:227` | open | reviewer read. Fix: assert every mirror's code is one this file knows |
| ❓ 8 | three places count the ways of not naming a language: `SKILL.md:64` and `configured_language`'s docstring say four, `UNNAMED` carries five ids and `seal/ledger/1788360817-…md:18` says five. Nothing behaves differently | those three | answered by the orchestrator: **four**. "Cannot be read or does not parse" is one way with two spellings, which is how the skill's sentence reads; the test may keep five ids for it, with a comment saying two exercise one way, and the ledger row is corrected to four | orchestrator |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: `evidence_check.py --strict .` unscoped | `335 ok · 0 drifted · 0 broken` |
| reviewer: `fold_ledger.py --check`, `gather_changelog.py --check` | both name the two unreleased fragments; the pre-release state |
| reviewer: the new test file | 36 passed |
| reviewer: the same file with `\| Pull request language \| French \|` in `seal/config.md` | 1 failed, `KeyError: 'French'` |
| reviewer: `configured_language` against `<tmp>/.git/seal/config.md` holding a Korean row | returned `English` |
| reviewer: `items()` against an adjacent second header, a stray separator, junk above the first row, and round 1's three-cell shape | round 1's shape fixed; the first two absorbed |
| reviewer: `configured_language` against an unknown language, a lower-case row, two language rows, an emphasised value | `French`, `English`, `Korean` (first wins), `**Korean**` |
| reviewer: the `Starts from` column against real work items | `spec.md` 12/13, `plan.md` 13/13, `overview.md` banner 13/15 |
| orchestrator: `tests/…:225` and `templates/config.md:24-26` opened together | the dictionary and the licence contradict each other |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 | `tests/test_the_pull_request_language_is_the_repositorys.py#items`, `#configured_language` | the two units round 1's fixes created; round 3 opens the fix diff again |
| round 1 | `skills/commit-pr-convention/SKILL.md:46-80, 145-160` | where every prose fix of this work item lives |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 7 of round 1 — the release guard's blind spot | issue #96, on the 0.5.0 milestone and in `docs/flow.md` before the release line | the orchestrator, before the release |
| ❓ 9 of round 1 — the design record still calls `pr.ko.md` a per-user setting | `docs/one-root-by-lifetime.md:449-450`, named in the pull request body | the repository owner |
