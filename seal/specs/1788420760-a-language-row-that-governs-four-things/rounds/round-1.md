# a-language-row-that-governs-four-things — review round 1

<!-- The first round on #106, reviewed together with #105 on one branch
because the failure that matters is the two disagreeing. This record carries
#106's findings; #105's are in its own directory. Target: the whole branch
from 022e466. Written by the review orchestrator, which implemented this work
item — the routing says why, and the round was a fresh warden reading it. -->

| Field | Value |
|---|---|
| Target SHA | the whole branch from its base 022e466, reviewed at 9a28262 |
| PR | none yet |
| Broad gate | not yet — 🔴 were open |
| Fixes checked by | round-2 |
| Contract changes | none — no unit changed |
| New units | two parametrised cases and three helpers in `tests/test_the_pull_request_language_is_the_repositorys.py` |
| Needs a fix | yes — 🔴 1 (`## Verdicts` and the `Verdict` column are not in the exclusion list), 🔴 2 (`## Not verified` is not either), 🔴 3 (two READMEs name a row that no longer exists), 🔴 4 (the skill that writes round records does not know the row), 🟡 5–10 |

- [ ] Pass

## What this round was asked to attack

The pairing itself: **every document that names a row, checked against every
other**, because a row named one way in one and another way in another is the
defect two work items on one branch exist to catch. Then the exclusion list
against what the checkers actually read — open `chain_check.py`,
`unverified_check.py`, `fold_ledger.py` and `gather_changelog.py` and find
every string matched literally. Then whether `evidence_check.py` survives
Korean prose in a ledger row, whether anything implies a fallback between the
two rows, whether #105 routes rather than reimplements, whether the five #82
anchors this branch re-pointed still support their claims, and which
assertions are satisfied by a substring that would still be there if the claim
were false.

## The finding that carried the rest

`Record language` is enforced by nothing. One list — *what a checker reads
literally* — is all that keeps a repository which sets it from breaking its
own gates, and that list was **written by hand and copied into three files**.
Two strings were missing from every copy, and both are load-bearing.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `chain_check.py` matches `## Verdicts` as a section heading and `Verdict` as a column name, and neither is in the exclusion list. Translating the heading makes the checker report a record that says nothing about what it found; translating the column makes it report no verdict column at all | `templates/config.md`, and its two copies | fixed at 2b9f43b — and the list is derived rather than copied now | reviewer called `chain_check.verdict_table` with each translated in turn and read the two distinct errors. This repository's own `ROUND_RECORD_FIELDS` already counted eleven fields where the new list counted six |
| 🔴 2 | `unverified_check.py` matches `## Not verified` in `overview.md`, which all three documents name as a `Record language` surface. The heading is not in the list, and that check runs on every pull request — a repository setting the row goes red for good | `templates/config.md` | fixed at 2b9f43b | reviewer called `check_text` with the heading translated and the table left English: `no '## Not verified' section` |
| 🔴 3 | `templates/seal-README.md` and its byte-identical copy still called the row *the pull request language*, and counted one language row where there are two. The bootstrap writes that file into every repository it sets up | `templates/seal-README.md:78`, `seal/README.md:78` | fixed at 2b9f43b | reviewer read both; a ledger row pins them byte-identical, so they were wrong together and nothing reddened |
| 🔴 4 | `skills/code-review/SKILL.md` — the skill that writes round records, and the one `commit-pr-convention` names as a reader of this row — does not mention `Record language` or `config.md` at all. A session that loaded that skill directly had nowhere to read it | `skills/code-review/SKILL.md` | fixed at 2b9f43b — a section naming the row, what stays English, and that the posted report follows the other row | reviewer grepped the file |
| 🟡 5 | the list said the verdict word is `agreed` where `chain_check.CLOSED_WORDS` holds `agreed, fixed`. Anyone keeping `agreed` in English on the list's authority writes a verdict that never closes. `none`, read at three call sites, was absent entirely | `templates/config.md` | fixed at 2b9f43b, and the derived case now covers both | reviewer called `verdict_of` and read the normalised value against the set |
| 🟡 6 | the list's grounds are *what a checker reads*, and `Needs a fix` is read by no checker — only by a test | `templates/config.md` | fixed at 2b9f43b — the heading now says *a checker or a pinned case*, which is true of every item | reviewer grepped `hooks/`, `skills/*/scripts/` and `.github/scripts/` |
| 🟡 7 | four of the six documents naming a row were green with the wrong row. Changing `agents/warden.md`, `agents/smith.md`, `skills/implement/SKILL.md` or `skills/commit-pr-convention/SKILL.md` to `Pull request language` reddened nothing | `tests/…` | fixed at 2b9f43b — a parametrised case over all eight readers | reviewer ran eleven document mutations against 124 cases: seven red, four green |
| 🟡 10 | three rows of `spec.md`'s criteria table render with the wrong column count: an unescaped pipe inside a backticked example | `spec.md:62-67` | fixed at 2b9f43b — `\|`, the spelling this repository's ledgers already use | reviewer read |
| ❓ 11 | the mirror paragraph — which row decides whether `pr.ko.md` or `pr.en.md` is the mirror — sits under a heading that now reads *What no row governs*. Nothing breaks; the next reader of that section will stop at it | `templates/config.md` | deferred — the heading is right for the rest of the section and moving one paragraph is a judgment about where a reader looks | reviewer read |
| ❓ 12 | `routing.md`, `tests-todo.md` and `evidence-todo.md` are records the protocol names, and no row governs their prose. Deliberate or missed is not written down anywhere | `templates/config.md` | deferred — the repository owner | reviewer read |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: `chain_check.verdict_table` with the heading and the column translated | two distinct errors — 🔴 1 |
| reviewer: `unverified_check.check_text` with the heading translated | `no '## Not verified' section` — 🔴 2 |
| reviewer: `chain_check.verdict_of` on six verdict cells | `agreed` alone is outside `CLOSED_WORDS` — 🟡 5 |
| reviewer: eleven document mutations against 124 cases | seven red, four green — 🟡 7 |
| reviewer: `seal mode` through shared, the documented rollback, local, and `--check` | every side effect and the output format match what #105's skill says |
| reviewer: `evidence_check.py`'s anchor regex against Korean prose in a claim cell | passes — #106's claim about ledger rows holds |
| reviewer: the five #82 anchors this branch re-pointed | all five still supported by the section they now name |
| orchestrator: the derived case with each heading deleted from the list in turn | reddens naming the missing string, one case per literal |
| orchestrator: six document and skill mutations | each reddens its own case |
| orchestrator: full suite, `ruff check .`, `ruff format --check .`, `evidence_check --strict` | 1630 passed · 1 skipped; clean; 85 files; 455 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| — | none; this is the first round | — |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The mirror paragraph under *What no row governs* | this record | the repository owner |
| Whether `routing.md` and the two todo files should be governed by `Record language` | this record | the repository owner |
