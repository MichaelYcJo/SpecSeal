# 1788360817-the-pull-request-language-is-fixed-inside-a-skill — review round 3

<!-- The verifying round for round 2's fixes (target: the diff a29ad72..c055de2).
It closed all eight of round 2's items and opened four 🟡 of its own, so it is
a finding round and consumes the cap: three of three. No 🔴 is open, so the
bound is three and the run ends after these are answered. The way past the
bound without spending a round is the one the format prescribes: a fix pass,
then a verifying round at the diff of those fixes, which consumes nothing if
it opens nothing. Written by the review orchestrator. -->

| Field | Value |
|---|---|
| Target SHA | c055de2 (the fix diff from a29ad72); HEAD ca317e2 at review time, record-only |
| PR | none yet |
| Broad gate | not yet — findings are open |
| Fixes checked by | round-4 |
| Contract changes | `shipped_templates` → `unreachable_templates`, `test_every_template_is_named_by_a_document_that_ships`, `test_the_templates_check_reads_prose_only_and_descends` — signature unchanged, the set of returnable values narrowed: an untracked file is no longer returned; `mirror_to_refuse` → `test_the_existing_mirrors_are_consistent_with_the_rule`, `test_a_language_this_file_has_no_code_for_does_not_raise`, `test_a_language_spelled_differently_is_the_same_language`, `test_a_language_that_is_genuinely_absent_still_answers_none` — widened: an emphasised or lower-case spelling now answers a code where it answered `None` |
| New units | `tests/test_the_pull_request_language_is_the_repositorys.py#as_language_name`, `#CODES_BY_NAME`, `#ROUND_RECORD_FIELDS`, and five cases: `test_a_language_spelled_differently_is_the_same_language`, `test_a_language_that_is_genuinely_absent_still_answers_none`, `test_the_round_template_carries_every_field_the_skill_names`, `test_the_sentence_no_longer_claims_an_order`, `test_an_untracked_file_under_templates_is_not_a_template`. No unit removed |
| Needs a fix | yes — 1 (`shipped_templates` globs the working tree while its corpus reads `git ls-files`, so an untracked `templates/.DS_Store` turns the check red at a file `git status` hides), 2 (`mirror_to_refuse` skips the mirror check for a language it does know, spelled `**Korean**` or `korean`), 3 and 4 (two sentences added last round describe files that do not read that way) |

- [ ] Pass

## Verdicts

Round 2's eight items first, each reproduced rather than read; then what this round opened.

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r2 🔴 1 | `KeyError` on a language the template licenses | `tests/…#mirror_to_refuse` | answered — the fix is round 2's, this round reproduced its closure | reviewer executed: `French` → `None`, `English` → `pr.en.md`, `Korean` → `pr.ko.md`; the case skips naming the language |
| r2 🟡 2 | the reader resolved one home where the skill resolves two | `tests/…#configured_language`, `#config_homes` | answered — reproduced | reviewer executed in a scratch repository: a Korean row under the git dir reads back Korean; with a Japanese row at the tree root beside it, the tree root wins. Read `hooks/optin.py:130-159` and confirmed the same order |
| r2 🟡 4 | the templates check admitted Python comments | `tests/…#shipped_templates`, `#unreachable_templates` | answered — reproduced; the fix carried in this round's 1 | reviewer executed: the corpus is `.md` only, the glob descends and sees dotfiles, and both exposed templates are now named by prose |
| r2 🟡 3 | the mirror-home prose was pinned by nothing | `tests/…#test_the_mirrors_home_is_resolved_and_excludes_the_git_directory` | answered — reproduced | reviewer executed phrase counts: each pinned phrase occurs exactly once in each document, so the case cannot pass on an unrelated sentence |
| r2 🟡 5 | a separator below the rows and a repeated header did not end the table | `tests/…#items` | answered — reproduced | reviewer executed both shapes and three more; a dash-only row and an empty row above the first row are still tolerated |
| r2 🟡 7 | the mirror check no longer caught `pr.kr.md` | `tests/…:237-246` | answered | reviewer read: the unknown-code assertion runs unconditionally, before the skip |
| r2 🟡 6 | the memo named one of two `docs/flow.md` lines | `overview.md:78-93` | answered | reviewer read: both commits named, with the command that finds them |
| r2 ❓ 8 | four ways or five | three places | answered | reviewer read all three: four, with the comment saying five ids exercise it |
| r2 drift | the five ledger rows the Bootstrap edit moved | `seal/ledger.md:358`, `seal/ledger/1788354065-…md` ×4 | answered — re-reads, not re-hashes | reviewer opened `skills/implement/SKILL.md:85-160` against each of the five claims and reports all five hold; only the section hash moved |
| 🟡 1 | `shipped_templates` globs the working tree with `include_hidden=True` while the corpus it is compared against comes from `git ls-files`. The two disagree wherever `.gitignore` does, and `.gitignore:5` ignores `.DS_Store` — a file this repository's root already carries, and one opening `templates/` in Finder creates. The check then fails naming a file that is not a template and that `git status` will not show. Before round 2's fix the plain `*` glob skipped dotfiles, so this is a regression that fix carried in | `tests/test_the_pull_request_language_is_the_repositorys.py:681-696` | open | reviewer executed with an untracked `templates/.DS_Store`: `unreachable_templates` returns it and the case fails; orchestrator confirmed `.gitignore:5` and one `.DS_Store` at the root. Fix: read `git ls-files templates` — the same list the corpus reads (reviewer's paste-ready helper), and make the unit case's fixture a repository so it exercises that path |
| 🟡 2 | `mirror_to_refuse` looks the value up exactly, so `**Korean**` and `korean` answer `None` and the mirror case **skips** — with a message saying the file has no code for the language, which is false. `templates/config.md:24-26` says the reader is a model rather than a lookup table, and round 2's own probe table records `configured_language` returning `**Korean**` for an emphasised row. The skip is right for `French` and wrong for a language the dictionary holds under another spelling | `tests/test_the_pull_request_language_is_the_repositorys.py:348-359` | open | reviewer executed end to end: a config holding `\| Pull request language \| **Korean** \|` makes the case skip. Fix: strip emphasis and compare case-insensitively (reviewer's snippet), keeping `None` for a language genuinely absent |
| 🟡 3 | `skills/code-review/SKILL.md:145-147` says `templates/sdd-round.md` "carries those fields in the order the row above lists them". It does not: the header table and the sections interleave that order, and the template also carries `PR`, which the row does not list. This matters more than usual because that sentence is now the only place in the whole prose corpus that names the file | `skills/code-review/SKILL.md:145-147` | open | reviewer read both, and executed the census showing the sentence is the file's only mention. Fix: keep the half that names the source, drop the claim about order (reviewer's replacement) |
| 🟡 4 | `skills/implement/SKILL.md:90-94` replaced "created empty" with "written from `templates/ledger.md` … starts with **no rows** and no baseline to stamp". The template ships a `\| Item \| Value \|` table with two rows and placeholder rows in two more, and the live `seal/ledger.md:21-24` carries the first of them. The meaning intended is *no evidence rows*, which the same section's fourth bullet says | `skills/implement/SKILL.md:90-94` | open | orchestrator opened both. Fix: say the clause tables arrive empty, which is true and is the thing a session needs to know |
| 🟢 5 | The claim this round was asked to test rather than accept — that the two sentences added to skills are guidance rather than tokens — holds. Before the diff neither template was named by any prose, and a session reading "create it from `templates/`" could not tell which file. Findings 3 and 4 are against the accuracy of the sentences, not their existence | `skills/code-review/SKILL.md`, `skills/implement/SKILL.md` | pass | reviewer read the pre-diff text of both |
| 🟡 6 | What stops the next unreachable template being closed the same cheap way: nothing in the check. `unreachable_templates` is a substring test over concatenated prose and cannot tell a document that tells a session to start from a template from one that merely contains its path. Executed census: six of the twelve templates are named by exactly one document, so for half the directory the check's whole strength is one sentence being honest. All six are honest today | `tests/…:699-716`, `seal/ledger/1788360817-…md:48` | open, and the answer is the ledger row rather than the check | reviewer executed the census. Fix: narrow the row's clause to what executes and move the judgment into its Notes cell |
| 🟢 7 | Two blindness guards fire: an empty corpus reports all twelve unreachable, and a missing `templates/` directory makes the helper's own assertion fail | `tests/…#shipped_templates`, `#unreachable_templates` | pass | reviewer executed both |
| 🟢 8 | An unreadable config in the resolved root does **not** fall through to the other home, which is what the docstring says and what `hooks/optin.py#home_at` does: the root is a place, not a search | `tests/…#configured_language:401-404` | pass | reviewer executed: a `seal/config.md` that is a directory beside a good one under the git dir answers English |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the test file | 46 passed |
| reviewer: `evidence_check.py --strict .` unscoped | `350 ok · 0 drifted · 0 broken` |
| reviewer: `fold_ledger.py --check`, `gather_changelog.py --check` | both name the two unreleased fragments; the pre-release state |
| reviewer: `unreachable_templates` with an untracked `templates/.DS_Store` | returns it, the case goes red; `[]` once removed |
| reviewer: the proposed `git ls-files templates` helper here and on a scratch repository | 12 paths here; three there, the `.DS_Store` dropped |
| reviewer: `configured_language` with an unreadable root config beside a good one under the git dir | `English`, no fall-through |
| reviewer: `mirror_to_refuse` over seven values | `**Korean**` and `korean` answer `None`; the proposed version answers `pr.ko.md` |
| reviewer: `items()` over a dash-only row, an empty row, a trailing repeated header | first row only in all three |
| reviewer: phrase counts for the three pinned mirror phrases | 1 · 1 · 1 in each document |
| reviewer: the reachability census over all twelve templates | six named by exactly one document, all honest |
| orchestrator: `.gitignore:5` and the root's `.DS_Store`; `shipped_templates` and `mirror_to_refuse` opened | as recorded |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 2 | `tests/…#shipped_templates`, `#mirror_to_refuse`, `#configured_language`, `#items` | the four helpers this run's fixes created or changed; round 4 opens the fix diff again |
| round 1 | `skills/commit-pr-convention/SKILL.md:46-80, 145-160` | where every prose fix of this work item lives |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 7 of round 1 — the release guard's blind spot | issue #96, on the 0.5.0 milestone and in `docs/flow.md` before the release line | the orchestrator, before the release |
| ❓ 9 of round 1 — the design record still calls `pr.ko.md` a per-user setting | `docs/one-root-by-lifetime.md:449-450`, named in the pull request body | the repository owner |
