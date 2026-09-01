# 1788302682-the-release-check-never-watched-bin — review round 1

| Field | Value |
|---|---|
| Target SHA | 2df3c18 |
| PR | none yet |
| Broad gate | not yet — the one full run follows the chain |
| Fixes checked by | nobody — the fix pass for 🟡 2 and 🟡 3 has not run yet; the verifying round sets this |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no — 🟡 2 and 🟡 3 close by taking the supplied snippets or by answering with grounds; nothing blocks |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 0 | Stage 1: both checkboxes of issue #10 are answered — `bin` is in the pattern, and every candidate outside the five roots is classified with a reason; `spec.md` cites the issue and the policy rather than restating the diff | `.github/workflows/hygiene.yml:40` · `specs/1788302682-the-release-check-never-watched-bin/questions.md:24-32` | pass | `install.sh:6-8` and `:16-18` say it distributes a CLAUDE.md block and is run as `bash install.sh` from a clone; `hooks/version-check.py:71` opens `plugin.json` and no other repository file; the `docs/` citations in shipped files are bare paths that resolve in the user's repository, so the loader never reads the plugin's copy. Orchestrator re-read `hygiene.yml:35-40` and the doc paragraph and agrees |
| 🟢 1 | `bin/` ships — reproduced rather than taken from the account | `bin/evidence-check:3-5` | pass (executed) | warden's `command -v evidence-check` resolves into the plugin cache's `bin/`; the reference's *File locations* row was read by the smith, not by the reviewer, and the executed evidence stands on its own |
| 🟡 2 | The document pin checks one direction: it asserts the six roots are *present* in the paragraph, so a seventh root or a sentence excluding one would pass while the pattern pin at `:119-126` holds set equality | `tests/test_the_release_check_watches_what_ships.py:147` | open | spec §Scope 2 says the document names *the same* roots. Orchestrator ran the reviewer's extraction on the current paragraph and it yields exactly the six; a set-equality assertion is the supplied fix |
| 🟡 3 | When the step is renamed, `ships_pattern` fails with a bare `IndexError` rather than a message — a loud failure, but one that says nothing | `tests/test_the_release_check_watches_what_ships.py:80` | open | `:82` already shows the shape: an `assert STEP in text` with a message, one line earlier |
| 🟢 4 | `tracked_top_level_entries` reads git, not the filesystem, so an untracked local file cannot fail CI and a tracked entry cannot be missed; `ships_pattern` refuses to match nothing | `tests/test_the_release_check_watches_what_ships.py:78-90` | pass | `git ls-files` with `check=True`; `assert found` at `:82`; the step name occurs once in the workflow and the new comment carries neither `- name:` nor `grep -E '` |
| 🟢 5 | The ledger row anchored on the hygiene step covers the pattern line | `.specseal/map/1788302682-the-release-check-never-watched-bin.md:10` | pass (executed) | warden changed `bin` to `bin2` at `hygiene.yml:40` and the row read DRIFTED at 22-51; restored, 71 ok |
| 🟢 6 | Windows: `open(..., encoding="utf-8")`, no `grep` spawn, `git ls-files` prints `/` on every platform | `tests/test_the_release_check_watches_what_ships.py:73-75, 86-90` | pass | read |
| 🟢 7 | Fragments, not the shared files: `CHANGELOG.md` and `.specseal/map.md` are untouched; the changelog fragment has the siblings' shape; commit subjects are `<prefix>: lowercase symptom` | `specs/1788302682-the-release-check-never-watched-bin/changelog.md` · `git diff --stat 4d36435..2df3c18` | pass | read |
| 🟢 8 | The smith's `New units` list omits the module constants `ROOT`, `WORKFLOW`, `RELEASE_DOC`, `STEP` | `tests/test_the_release_check_watches_what_ships.py:31-34` | answered | a completeness note for this record, not a defect; the constants are listed in round 2's `New units` row with the fix diff |

## Executed probes

| What was run | Result |
|---|---|
| pytest (3.12) new file + `test_release_hygiene` + `test_the_changelog_is_gathered_at_release` + `test_no_real_identifiers` + `test_docs_line_wrap`, `-rs` | 76 passed, 0 skipped — warden's run and the orchestrator's re-run agree |
| `evidence_check.py --strict .` | 71 ok · 0 drifted · 0 broken (warden and orchestrator) |
| anchor probe: `bin` → `bin2` at `hygiene.yml:40`, then `--strict` | the new hygiene row DRIFTED, content changed at 22-51; restored |
| M1: `docs\|` added to the workflow pattern | `test_nothing_that_stays_home_is_watched[docs]` and the set-equality pin red (2 failed, 27 passed) |
| M2: `"docs"` added to `SHIPS` | 4 failed including `test_the_two_lists_do_not_overlap` |
| `"evals"` removed from `STAYS_HOME` | `test_every_top_level_entry_is_classified` red, naming `['evals']` |
| `ruff check` / `ruff format --check` on the new test file | clean |
| `git diff --quiet` after every mutation | exit 0 |
| orchestrator: the reviewer's token extraction on the current doc paragraph | exactly the six roots of `SHIPS` |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain — 🟡 2 and 🟡 3 go to the fixing session (smith, resumed).
