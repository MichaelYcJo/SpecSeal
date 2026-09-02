# Feature Specification: the release check never watched bin/

<!-- specs/1788302682-the-release-check-never-watched-bin/spec.md — WHAT this
work delivers and how we'll know. The policy documents in docs/ outrank this
file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/branch-and-release.md` §Two things carry the version | updates are keyed to `plugin.json`'s version; a change to what ships that leaves it alone reaches nobody — the whole reason the hygiene step exists |
| `CONTRIBUTING.md` §What a change to a gate must carry | this widens a CI gate, so it carries a test seen red, a stated failure direction, a prompt budget (zero — the step asks nobody anything) |
| `CLAUDE.md` §The goal a design is chosen against | the durable half is a pin that goes red on its own, never a rule a person has to remember at the release |
| Claude Code plugin reference, *File locations* — "Executables · `bin/` · Executables added to the Bash tool's `PATH` and invokable as bare commands while the plugin is enabled" | settles the issue's first checkbox: `bin/` ships, by the loader's own definition |

## Scope

**In:**

1. `bin/` joins the roots the hygiene step treats as *what ships*, in
   `.github/workflows/hygiene.yml`'s pattern.
2. The sentence in `docs/branch-and-release.md` that enumerates those roots
   says the same six the pattern does.
3. A test pins the pattern to the repository: every tracked top-level entry
   is classified as shipping or staying home, each shipping root is matched
   by the pattern, each home entry is not, and an entry nobody has classified
   fails — so the next `commands/` or `output-styles/` cannot fall out of the
   pattern unnoticed the way `bin/` did.
4. The issue's second checkbox answered per candidate, in `questions.md` and
   the pull request body.

**Out:** the step's other behaviour (it still runs only when the base is
`main`; it still reads the version from `plugin.json`); any change to
`plugin.json`'s version on this branch (the pull request targets the release
branch, where the version does not move); any new root added to the pattern
that does not exist in the repository today.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A release PR fixes only a wrapper | Given a PR into `main` whose diff touches only `bin/unverified-check`, when the hygiene step runs, then it demands a version bump | `tests/test_the_release_check_watches_what_ships.py::test_every_shipping_root_is_watched` — `bin/` is matched by the pattern read out of the workflow |
| A release PR touches only docs | Given a diff confined to `docs/`, `tests/`, `specs/` or `evals/`, when the step runs, then it says nothing that ships changed | `::test_nothing_that_stays_home_is_watched` |
| A new top-level directory appears | Given a directory no test has classified, when the suite runs, then it fails naming the directory and where to classify it | `::test_every_top_level_entry_is_classified` |
| A reader opens the release document | The roots it names are the roots the pattern names, `bin/` included | `::test_the_release_document_names_the_same_roots` |

## Data & interfaces

None — one regex in a workflow, one sentence in a document, one test file.

## Open questions → questions.md

The batch before the first edit found nothing that changes what is built; the
assumptions it settled are recorded in `questions.md`, the second checkbox's
per-candidate answers among them.
