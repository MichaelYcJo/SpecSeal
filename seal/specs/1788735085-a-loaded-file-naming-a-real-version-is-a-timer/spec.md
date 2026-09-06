# Feature Specification: a loaded file may not name a version that has not shipped

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` § *The goal a design is chosen against — verification that runs unattended* | Of #179's three candidates, the sweep and the exemption both leave a person to remember; the widened check is the only one that catches the next author without one |
| `CONTRIBUTING.md` § *What a change to a gate must carry* | This change alters what a gate refuses, and adds a fourth entry to `RECORDS_OF_A_MOMENT`; both owe the argument that document asks for |
| `docs/issues-and-milestones.md` §*A rolling log is titled after the version it rolled from* | The repository already decided its answer to this class once — an illustrative `1.2.3` with the reason beside it — and #179's own line is the place that decision was not applied |
| `docs/review-chain-spec.md` § *The fix surface* | #98's correction lives inside `shipped_templates`' hashed region, so two ledger rows anchored on it are re-read rather than re-pointed |

## Scope

**In.**

- `tests/test_release_hygiene.py::test_no_loaded_file_hardcodes_the_running_version` refuses **every version at or above the running one** in the loaded set, not only the running one — so a document naming a version that does not exist yet goes red on the commit that writes it rather than on the release that ships it.
- The three exemptions that rule needs, each named and argued in the test: the illustrative version the repository already writes (`1.2.3`), `docs/experiments/` as records of a moment, and a version belonging to another product.
- `docs/issues-and-milestones.md:28` stops naming `0.9.0`.
- **#98**, riding this branch: the three places saying `-z` alone turns git's path quoting off and `core.quotePath=false` does not — a comment in `tests/test_the_pull_request_language_is_the_repositorys.py`, the section name in `seal/ledger/1788360817-…md`, and the round-5 summary — say what the arguments do. The two ledger rows anchored on `shipped_templates` are re-verified, because the comment lives inside that unit's hashed region.
- The fold-in #98's body names: the docstring at `tests/…:884-886` says two fixture documents carry the only mention of one template, where each carries the only mention of one template.

**Out.**

- Rewriting a version a released record names. `docs/one-root-by-lifetime.md` and `docs/flow.md` keep theirs, and `docs/issues-and-milestones.md:156` — *the branch `release/v0.3.0` shipped as 0.2.0* — is history that must stay readable. A rule that refuses it is the wrong rule.
- Any change to what `-z` and `core.quotePath=false` are passed. #98 is comment-and-record only, and its own body says so: the tests pass either way.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A version that has not shipped is refused when it is written | Given a loaded file naming `0.9.0` while `plugin.json` ships `0.8.3`; when the hygiene suite runs; then it fails and names the file, the version and the line | The case, seen red against `docs/issues-and-milestones.md:28` as the tree stands before phase 2 |
| A past version stays readable | Given `docs/issues-and-milestones.md:156` naming `0.2.0` in a sentence about what a branch shipped; when the suite runs; then it passes | The same case, green on the unmodified line; a fixture asserting a below-running version is allowed |
| The illustrative version is not a timer | Given a loaded file writing `1.2.3` where a real version would be wrong; when the suite runs; then it passes, and the failure message tells the next author to write that value | The case, plus an assertion that the illustrative value is not one this repository has shipped or is shipping |
| Another product's version is not this repository's | Given `skills/implement/scripts/seal.py` naming bash `4.4.17`; when the suite runs; then it passes because that version is declared with the product it belongs to | The case over the tree as it stands |
| A dated experiment record keeps the version it measured on | Given `docs/experiments/2026-09-03-…md` naming Claude Code `2.1.259`; when the suite runs; then it passes, because rewriting the number would falsify the record | The case over the tree as it stands, and the argument in the test's docstring |
| The comment says what the argument does | Given `tests/…:757-761`; when it is read; then `-z` is credited with what it alone does — turning off the escaping of control characters and separating on the one byte a filename cannot hold — and `core.quotePath=false` is not said to leave the quoting on | The three places read against the measurement in #98's body, re-executed |
| The ledger row is re-read, not re-pointed | Given the two rows anchored on `shipped_templates`; when the comment inside that unit changes; then the rows are re-verified with the hash the change produced | `./bin/evidence-check .` unscoped, and `--reverify` on the two rows |

## Data & interfaces

No runtime interface changes. One check's refusal widens; one document line changes; three comment-or-record sentences change.

## Open questions → questions.md

None open. What #179 left undecided is settled in `plan.md`'s Alternatives, against the goal `CLAUDE.md` states.
