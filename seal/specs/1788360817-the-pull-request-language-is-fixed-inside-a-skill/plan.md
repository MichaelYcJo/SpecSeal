# Implementation Plan: the pull request language is fixed inside a skill

<!-- seal/specs/1788360817-the-pull-request-language-is-fixed-inside-a-skill/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

## Summary

A repository states its pull request language in `seal/config.md`, one row of
a table the plugin owns, and `commit-pr-convention` reads it instead of
requiring English of everyone. Absence is the default and the default is
English, so a repository that says nothing behaves exactly as it does today.

This alters what a session reads and acts on, which is the top rung of the
`implement` skill's ladder — hence a spec and this plan before the first
edit, rather than a scope line.

## Technical context

The five places the skill fixes English:
`skills/commit-pr-convention/SKILL.md:47` (commit subject), `:68-70` (the
body, with the reason: a feature branch squashes, so the commit body becomes
the pull request body and the two cannot differ), `:74` (pull request title),
`:88` (pull request body), `:131` (the self-check *"Are the title and body
English?"*).

The shape to copy is `templates/parity.md` and the file it produces,
`seal/parity.md`: one `| Item | Value |` table in the root, read by a skill.
`seal/` holds `README.md`, `ledger.md`, `ledger/`, `follow-up.md`, `specs/`
today; `config.md` is new, in this repository and in the templates.

The root is resolved, never spelled: `hooks/optin.py#home_at` reads
`<repo>/seal/` then `<git-common-dir>/seal/`, so a skill naming only the
first leaves local mode (#80, merged at `8846cdd`) unable to carry a config
at all. The skill already spells `seal/specs/…` in its mirror section, so
the two-place sentence has to arrive with the new section.

`seal/README.md` is `templates/seal-README.md` verbatim —
`tests/test_first_setup_asks_once.py#test_the_seal_readme_is_the_template_verbatim`
pins the equality and `hooks/root-migrate.py#rewrite_readme` depends on it —
so the two move as one edit. `README.md` and `README.ko.md` move together
because the hygiene workflow warns when they do not.

**What breaks in six months.** The row is prose read by a model, so nothing
fails loudly when a session ignores it: a Korean repository gets an English
pull request and only a person notices. The alternative that fails loudly is
a language-detecting gate, and that one fails loudly in the wrong direction —
a false stop on a correct commit. The trade is recorded in `questions.md` Q3
and the untested half is named in `overview.md` §Not verified.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A row in the root's config table, read by the skill (chosen) | A session skips the row and writes English anyway; nothing catches it | **Taken.** It is the issue's own shape, it matches `parity.md`, and it costs one file that most repositories never create |
| A key in an existing file — `seal/README.md`, or a frontmatter field on the skill | The README is generated from a template and overwritten by `hooks/root-migrate.py#rewrite_readme`, so a repository's answer would be erased by a migration. A skill's frontmatter is the plugin's, not the repository's, so every repository would share one answer — the defect being fixed | Rejected |
| A `git config` key (`specseal.prLanguage`) | Per-clone, not per-repository: a second machine and CI start empty, and the answer is invisible in review because it is in no file. `docs/one-root-by-lifetime.md` settled the same question for the opt-in itself — there is no config key, the folder is the signal | Rejected |
| A hook that judges the commit message's language | Names, identifiers and quoted English make every detector wrong somewhere, and a wrong stop blocks a correct commit | Rejected — `questions.md` Q3 |
| Rename the mirror to a language-neutral `pr.mirror.md` | Twelve `git mv`s and every round record, overview and design record citing `pr.ko.md` goes stale, to fix a name that was only under-specified | Rejected — `questions.md` Q2 |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `templates/config.md`, and the skill reading it: a new *The language* section carrying the path, the default, the resolved root and the three exclusions (prefix, branch names, response language), plus the five surfaces reworded and the mirror generalised to `pr.<lang>.md` | S1–S8 read off the two files; `tests/test_docs_line_wrap.py` on the skill, which is a covered file | `5db37e8` |
| 2 | The tests that pin it (`tests/test_the_pull_request_language_is_the_repositorys.py`), the four documents that describe the root (`templates/seal-README.md`, `seal/README.md`, `README.md`, `README.ko.md`), and the record — ledger fragment, `changelog.md`, `overview.md` | the new file run red before the document edits and green after; `tests/test_docs_line_wrap.py`, `tests/test_first_setup_asks_once.py`, `tests/test_no_document_names_the_old_roots.py`, `tests/test_release_hygiene.py` | `56ec644`, and the record in the commit after it |
| 3 | Round 1's six open findings, and the four tests `tests-todo.md` prescribed. The skill names `templates/config.md` and the check covers the whole directory; the mirror's home is resolved and refused under the git directory; not naming a language becomes one rule with five cases; the mirror case reads the row instead of the file's absence; a foreign row ends the table; the drift this branch left in another item's fragment is re-read and re-verified | the four prescribed rows planted and green — 36 cases in the file, 350 in the slice; both new checks run against the PRE-fix text, where the old parser returned the row behind a foreign one and four templates were unreachable at `1280de9`; `evidence-check --strict .` unscoped, `335 ok · 0 drifted · 0 broken` | `d7e609a` |
| 4 | Round 2's 🔴 and six 🟡, and `tests-todo.md` rows 5–10. Two of round 1's fixes reproduced the defect they closed: the mirror case indexed a three-entry dictionary with a value the template licenses, and the reader shipped with the resolved-home prose resolved one home. Also the templates corpus (prose only, glob descends), a separator and a repeated header below the rows, every mirror's code checked against the known ones, the memo's second `docs/flow.md` line, and the count of ways settled at four | the six rows planted and green — 46 cases in the file, 411 in the slice; every defect reproduced against the pre-fix code first, including a one-home reader answering `English` for a Korean row under `.git/seal/`; `evidence-check --strict .` unscoped, `350 ok · 0 drifted · 0 broken` | `c055de2` |
| 5 | Round 3's four 🟡 and `tests-todo.md` rows 11–13, the last fix pass of the run. The templates listing and its corpus both read `git ls-files`, so a gitignored file cannot fail the check; a language spelled with emphasis or in another case resolves rather than skipping; and the two sentences round 2 added to `code-review` and `implement` are corrected to what the files they name actually read | the three rows planted and green — 66 cases in the file, 431 in the slice; both defects reproduced against the pre-fix code, the `.DS_Store` one in a scratch repository where `git status --porcelain` shows nothing about the file the glob reported; `evidence-check --strict .` unscoped, `355 ok · 0 drifted · 0 broken` | `85602b6` |
| 6 | Round 4's two findings, under the constraint round 4 imposed: **add no new unit.** Three rounds running, the unit a fix added carried the next round's finding, so the 3+ Fix Rule's answer is to stop growing the surface rather than to fix the defect a fourth time. `shipped_templates` gains `check=True`, `core.quotePath=false` and `-z`; its isolated case gains one existence assertion; and the three places calling `ROUND_RECORD_FIELDS` "the fields the skill names" come down to what runs. The memo records the pattern itself | 66 cases in the file, unchanged in number — the pass added none — and 431 in the slice; all three defects reproduced against the pre-fix code, including a Korean template name returned as `\355\225\234…` and reported unreachable, and the isolated case run with the helper stubbed to `[]`; `evidence-check --strict .` unscoped, `357 ok · 0 drifted · 0 broken` | `68cae4c` |

Phase 1 is the whole behaviour change and phase 2 is what keeps it. Splitting
them the other way — tests first — would put a red suite in front of a
document edit that no runtime reads, and buys nothing here: the pin is over
prose, so it can only be written against prose that exists.

**Status is empty, or the commit that closed the phase.** Re-read this column
after any rebase: these commits stop resolving at the squash, and a rebase
during the work orphans them earlier and more quietly.

## Operational impact

- **New file, optional.** `seal/config.md` is created by a repository that
  wants a non-default; nothing creates it, and nothing fails without it.
- **No migration.** Existing repositories keep English by absence.
- **No new dependency, no new environment variable, no hook change.**
- **One compatibility note.** `pr.ko.md` now means *the mirror, in Korean*
  rather than *the Korean translation of an English body*. Every existing
  file of that name in this repository keeps its meaning, because this
  repository's pull request language is English.
