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
