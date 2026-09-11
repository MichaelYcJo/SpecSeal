# round 1 — the paragraph the reviewer was spawned with

| | |
|---|---|
| Target SHA | `ae2d0ac842ed774df02b6526d2c375c16f0b8413` — every measurement below was taken there |
| Review at | HEAD of the branch, which adds only this paragraph on top of the target |
| Base | `origin/release/v0.11.1` = `5646717` |
| Draft pull request | #358, opened before this round |
| Ran by | specseal:warden on Opus 5 |

## Scope handed to the round

Issue #351 — `docs/flow.md` is deleted, and its four parts are placed where
they are read. Six commits, `7ed455b` through `ae2d0ac`, on top of the frame
commit `6035bee`.

## Facts, with labels

**Executed by the orchestrating session** at `ae2d0ac`, exit codes read
directly with no pipe:

- `bin/test -q tests/test_the_rules_have_one_owner.py
  tests/test_release_hygiene.py
  tests/test_a_corrected_sentence_survives_elsewhere.py
  tests/test_one_word_one_meaning.py tests/test_docs_line_wrap.py
  tests/test_no_real_identifiers.py
  tests/test_no_document_names_the_old_roots.py
  tests/test_the_seal_is_taken_once_by_the_sealer.py` → **234 passed, exit 0**.
- `uvx ruff check` and `uvx ruff format --check` over the five changed Python
  files → **exit 0** each.
- `git grep -ln "flow\.md" -- '*.md' '*.py' '*.yml'`, less `CHANGELOG.md` and
  `seal/specs/`, returns **`seal/ledger.md` alone**, four Notes mentions.

**Executed by the builder**, recorded in `overview.md`'s `· verified` line
with its own numbers: the two moved cases seen red (3 failed, exit 1) then
green (45 passed, exit 0); `evidence-check --strict` 1121 ok · 0 drifted · 0
broken; `survivor-check` over this range, 33 survivors then all 33 excused;
`unverified-check`; repository-wide `ruff check` and `ruff format --check`.
Re-derive rather than inherit.

**Read, not executed** — `docs/flow.md`'s `## 0.11.1` section was already
stale against the milestones when it was deleted: it listed #331, #335, #339
and #149 as this release's, and the tracker puts #331 and #335 in 0.11.3,
#339 and #149 in 0.11.2.

**Unverified** — the broad gate. It is the sealer's, after this chain settles.

## Where a claim flips on measurement point

The `RECORDS_OF_A_MOMENT` entry's removal was measured **with the file still
tracked**: seven offending lines, all seven inside `docs/flow.md`. Measured
after the deletion the same check has nothing to report. That is why the
entry comes out in phase 4's commit rather than phase 3's, and it is
divergence 3 in `overview.md`.

## The command with two forms

`bin/evidence-check` unscoped reads the whole ledger; `--strict` is the form
this branch was checked with. Do not narrow it to this work item's fragment:
that narrowing is what once let fifteen drifted rows reach a pull request.
