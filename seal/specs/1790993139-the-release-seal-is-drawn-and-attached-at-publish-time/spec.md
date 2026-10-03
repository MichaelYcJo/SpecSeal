# Feature Specification: the release seal is drawn and attached at publish time

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Three issues of milestone 52 (`release: 0.18.0`), routed as one work item
because all three sit in the seal stamp's renderer or its reserve:

- **#718, boxes 2 and 3.** The tag push draws one seal for the whole release,
  attaches it to the GitHub Release, and puts it where the note's
  `### 📊 At a glance` table stood. Any failure leaves today's note. The PNG is
  pinned against the terminal form it is drawn from.
- **#721.** One line of `seal_stamp.py#admitted`'s docstring is rewrapped.
- **#722.** A gate failure's exception type name is capped in UTF-16 units, so
  no foreign class name can carry the report past `MESSAGE_RESERVE`.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Nothing here stops to ask, and nothing here can stop a release. Every seal failure ends as a log line and a `::warning::`, never as a red job and never as a question |
| `docs/branch-and-release.md` §*Every act the release performs once it reaches `main`* (the bullet *The release note publishes itself*) | The note is published by the tag push and **never republished**. The seal is a second act on a release the same run just created, and it touches nothing else. The section is amended to say so, with its `Enforced by:` line |
| `docs/release-checklist.md` §6, the box *A GitHub Release exists at `vX.Y.Z`* | The box gains what the job now does after the note and where its log says why a seal is missing |
| `.github/scripts/publish_release_note.py`, module docstring (*The summary adds no way to fail*) | The seal is held to the same rule. A failed draw, upload or edit costs the image and never the counts — owner, #718's first comment |
| `CONTRIBUTING.md` §*Running the checks* (*the gates themselves are stdlib-only Python*; markdown-it-py is *test-only*) | Pillow may enter only as a test-and-release dependency, pinned once, beside `MARKDOWN_IT`. Nothing under `hooks/` or `skills/` imports it |
| `CONTRIBUTING.md` §*Running the checks* (*Python 3.12 is the supported floor*) and `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR` | A new script under `.github/scripts/` counts as shipped Python. It uses no `zip(..., strict=)` and no `*.UTC`, or it carries the guard block and a `CLASSIFIED` row. Pillow 12.3.0 requires Python ≥ 3.10, which the floor already exceeds |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | Changelog in `seal/specs/<id>/changelog.md`. New ledger rows in `seal/ledger/<id>.md`. Rows in `seal/releases/0.16.0.md`, `0.17.0.md` and `0.15.1.md` that cite an edited unit are re-read and re-stamped where they live, and corrected in place where the edit makes them false |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | Fixtures use `example/repo`, `example.com` and `/Users/x/`, as `tests/test_a_release_publishes_its_note.py` already does |
| `skills/agent-contract/SKILL.md` §12, §14 and §15 | #722 is a class, not a coordinate: every field the failure report takes from a record without a fixed vocabulary is bounded. Every changed line a person reads is pinned in the same commit. Every new case is seen red first |

## Scope

### In

1. **#718 box 2: the seal is drawn and attached at publish time.**
   `publish-release.yml` keeps its `publish` job as it is. A second job,
   `seal`, runs after it and only when that job created the release in this
   run. It runs the suite at the tag, draws the seal, uploads `seal.png` with
   `gh release upload`, and edits the note so the glance table becomes the
   image plus one line of the table's counts. The draw and edit live in a new
   `.github/scripts/release_seal.py`.
2. **#718 box 3: the PNG is pinned against the terminal output.** For every
   cell of `seal_stamp.compose`, the PNG carries the colours `seal_stamp.block`
   gives that cell, through xterm's 256-colour table, and is transparent where
   `block` paints nothing.
3. **Each item in #718's last comment is answered here** (the owner listed
   them as what the automation still needs):

   | Item | Answer |
   |---|---|
   | The suite count needs a source | **A run at the tag, in the `seal` job.** It is the same command as `test.yml`'s ubuntu leg, plus `--junitxml`. The counts come from the JUnit XML, which is pytest's documented output format, not from a log. The seal is drawn only when that run passed: a `SEALED` above a red suite would be false |
   | Rounds, capped and deferred | **Capped** comes from the `chain: capped` label, read in the same `gh pr list` call that gets the pull requests (`labels` and `headRefName` added to its fields). **Items and rounds** come from the round records at the tag. A pull request is a work item where exactly one `routing.md` at the tag names its head branch (`hooks/routing.py#item_dir`), and its rounds are `hooks/routing.py#rounds`. **Deferred** is the set of distinct issue numbers named in a Verdicts cell whose verdict word is `deferred`, read with `skills/code-review/scripts/chain_check.py#verdict_table` and `#verdict_of`. Measured on 0.17.0's tree (`233f0455`, against the merged pull requests' head branches): 10 items, **27 rounds**, which matches the hand count, and 6 capped labels, which also matches. The deferred rule gives **12** distinct issues against the hand count of 13, which is `questions.md` Q10 |
   | The panel's labels are free text | **A fixed row set** — `SEALED`, `tag`, the continuation `main`, `PRs`, `issues`, `suite`, `items`, `capped`, `deferred` — held as one constant. The label column is set by `seal_stamp.letter`'s `{label:<8}`, not by the longest label: `deferred` is exactly eight, so a case requires every label to be eight characters or fewer. A value wider than `broad_gate.PANEL_VALUE_WIDTH` (23) moves to a continuation row; it is never cut at the frame |
   | The download URL is served as `application/octet-stream` | **Kept.** Measured 2026-10-03 on 0.17.0's asset: `github.com/…/releases/download/v0.17.0/seal.png` answers `302` with `x-content-type-options: nosniff`, and the target answers `200` with `content-type: application/octet-stream`, `content-disposition: attachment`, and **no `nosniff`**. The Fetch standard applies `nosniff` blocking to script and style destinations, not images, and an `<img>` ignores `content-disposition`. The note keeps descriptive alt text and the counts line beneath the image, so a browser that does not draw it still shows every number. A check on the published page is `questions.md` Q9 |

4. **#721.** `admitted`'s docstring paragraph is replaced with the
   paste-ready text in
   `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/rounds/round-3.md`
   §*Paste-ready fixes*. It is verbatim and changes nothing else.
5. **#722.** `hooks/dispatch.py#record` caps `type(exc).__name__` in UTF-16
   units with the cutter `first_line` uses, under a named `NAME_CAP` of
   **40 units**. `describe` applies both caps again when it reads a record,
   because `read_record`'s docstring says an older or newer plugin may have
   written that record. `seal_stamp.py`'s `MESSAGE_RESERVE` comment is
   re-measured over `dispatch.describe` with a name at the cap. Arithmetic,
   from read figures: two gates at 909 with a 19-unit name gives
   `909 + 2 × (40 − 19) = 951`, which is under the 1,000 reserve. The smith
   measures it rather than trusting this sum.

### Out, and why

| Left out | Grounds |
|---|---|
| Any write to the tree at publish time: `seal/releases/`, a seal file, a ledger row | #718's body: the seal lives with the Release. The job's checkout is discarded |
| Reading `seal/releases/` | #718's reason for keeping the tree out was that `seal/releases/` may not survive #715. Nothing here reads it |
| A seal on a release the run did not create: a re-pushed tag, a re-run job, or a release published by hand | `publish_release_note.py`'s rule *It never republishes*. The seal edits the note, so it is held to the same line. Drawing one by hand stays possible with `DRY_RUN=1`, followed by `gh release upload` |
| #720, a wide character in a branch name shifting the disc's row | Predates #717 and is its own issue. Every value in a release row is ASCII: a version, a short SHA, `main`, numbers |
| The NOT SEALED form, a seal for a release whose suite failed | The `NOT SEALED` drawing is the gate's, for a branch. A release whose suite fails at the tag gets today's note and a `::warning::`, which is the fallback |
| A Korean edition of the note or the alt text | The note is English today (`publish_release_note.py` composes no other language) |
| Changing `test.yml`'s jobs other than its install line | Pillow joins the install so the pixel pin runs on all three operating systems. No new job |
| Making `publish_release_note.py` read labels or the tree | The note's path stays exactly as it is, apart from the glance table being built by a named function and the `created` output. The seal's reads are `release_seal.py`'s |
| Moving `seal_stamp.py`'s renderer into a shared module | `release_seal.py` imports `compose`, `block`, `DEFAULT_SCALE` and the palette constants. `seal_stamp.py`'s docstring gains it in the list of importers. No code in `seal_stamp.py` moves |
| Retiring or folding this release's work items | `docs/release-checklist.md` §2b runs `settle --retire` on released work items, as a separate later pull request. At the tag, the release's own round records are still on disk, which is what the chain rows read (`questions.md` Q1) |

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | The seal replaces the glance table | Given the tag push created the release, the suite at the tag passed, and Pillow loaded. When the `seal` job runs. Then `seal.png` is a release asset, and the note's `### 📊 At a glance` heading is followed by `![<alt>](https://github.com/<repo>/releases/download/<tag>/seal.png)`, a blank line, and one line carrying every row the table had, in its order: `🔀 Pull requests **N** · ✅ Issues closed **M**`, plus ` · 🙌 Outside contributors **K**` where the table had that row. Nothing else in the note changes | A case drives `release_seal.main` with `gh` stubbed, then asserts the upload argv and the edited body byte for byte against the body `publish_release_note.release_body` produced. This is the shape 0.17.0's hand edit used (`gh release view v0.17.0`) |
| S2 | Any failure leaves today's note | Given each of these, one at a time: the suite step failed; the JUnit file is missing or unreadable; it counts a failure or an error; Pillow does not import; `compose` or the PNG writer raises, `SystemExit` included; `gh pr list` fails; `gh release upload` fails; `gh release view` fails; the glance table is not in the note exactly once in the generated shape; `gh release edit` fails. When the `seal` job runs. Then the process exits 0, prints one line naming the failure and `::warning::` with the same reason, and makes no `gh release edit` call, except in the last case, where the edit was the failing call | One parametrized case per branch, each seen red by removing the guard it pins. **This is the case #718's box 2 asks for** |
| S3 | A hand-edited note is left alone | Given the glance table was changed after publication. When the `seal` job runs. Then the note is not edited, the log says the table was not found in the generated shape, and the asset upload is skipped | Case: the body differs by one character inside the table, and no edit and no upload are called |
| S4 | The seal runs only on the release this run created | Given `publish_release_note.py` found a release already at the tag. Then it writes `created=false` to `$GITHUB_OUTPUT`, and the `seal` job's `if:` skips it. With no `$GITHUB_OUTPUT`, as on a laptop, nothing is written and nothing raises | Case on `main` with `GITHUB_OUTPUT` pointed at a temporary file, for both branches and for the variable unset. A workflow case asserts the `if:` names that output |
| S5 | The workflow cannot turn red for the seal | `seal` `needs: publish`. Every step of `seal` is `continue-on-error: true`. `publish` has no `needs` and is unchanged apart from writing its output. `permissions` stays `contents: write` alone | `tests/test_a_release_publishes_its_note.py#test_the_workflow_fires_on_the_tag_and_writes_nothing_else` is rewritten to name what the workflow writes now (one release, one asset, one edit), and it keeps refusing `issues:`, `pull-requests:` and `packages:`. The build renamed it `test_the_workflow_fires_on_the_tag_and_writes_one_release_one_asset_one_edit` (`phases/phase-4.md`) · NAME NOT IN TREE |
| S6 | The PNG carries the terminal form's colours | For every cell of `compose(rows, DEFAULT_SCALE)` over the fixed rows, the PNG's top and bottom halves have the colours `block(cell)` gives through xterm's table (`rgb`). A half `block` leaves empty is alpha 0. In every non-space text cell, the darkest pixel is nearer the cell's ink (`INK`, or `TITLE` on line 1) than `PARCHMENT` | A stdlib case asserts `paint` against `block` for every cell. A Pillow case decodes the PNG and samples each half away from glyph areas. Both are seen red by swapping two colours in `rgb`'s table |
| S7 | `rgb` is xterm's table | The four codes the sheet uses map to xterm's values: 230 → (255,255,215), 187 → (215,215,175), 94 → (135,95,0), 124 → (175,0,0). A triple passes through unchanged | Case. The four values are the ones in `seal_stamp.py`'s own comments |
| S8 | The rows are fixed and fit | `release_rows(...)` returns the fixed label set in order. Every label is eight characters or fewer. No value is wider than `PANEL_VALUE_WIDTH`, and a wider suite value moves `S skipped` to a continuation row. A count of 0 still draws its row | Cases, including a five-digit suite (`10003 passed, 166 skipped`, 25 characters) |
| S9 | The suite counts are read from JUnit | Given pytest's `<testsuites><testsuite tests= failures= errors= skipped=>`, passed is `tests − failures − errors − skipped`. More than one `testsuite` element is summed. A file that does not parse is a failure (S2), never a zero | Case over fixture XML in the shape pytest 8 writes |
| S10 | The chain rows read the tree at the tag | Given a fixture repository with `seal/specs/<id>/routing.md` naming a branch and `rounds/round-1.md`…`round-3.md` whose Verdicts cells include `deferred #12`, `**deferred** #13, #14` and `deferred seal/follow-up.md`. When `chain_counts` reads it for pull requests whose `headRefName` is that branch. Then items, rounds and deferred are 1, 3 and 3 (#12, #13, #14). A pull request no declaration names is not an item. A source that cannot be read leaves that row's value `not read`, and the log says why; the row is never dropped and never zero | Cases with a built fixture tree. A measurement over 0.17.0's tree, recorded in the phase file, is expected to give 10 items and 27 rounds |
| S11 | The alt text says what the image says | The alt text is one sentence carrying every value of the rows, in the shape of 0.17.0's. It contains no `]` or newline | Case |
| S12 | A dry run writes nothing | `DRY_RUN=1` writes the PNG to the path given in `SEAL_PNG` (default: a temporary directory), prints the rows and the edited body, and calls neither `gh release upload` nor `gh release edit` | Case with `gh` stubbed to fail on any write verb |
| S13 | #721 | `admitted`'s docstring is the paste-ready paragraph, and no line of it is longer than 79 columns | Case over `seal_stamp.admitted.__doc__` line widths, seen red against the 113-column line |
| S14 | #722, a long foreign class name | Given a gate that raises an exception whose class name is 120 characters, and a second whose name is 60 astral characters (120 units). When `record` writes them and `describe` reads them. Then each `error` field is at most `NAME_CAP` units, and an astral character that would cross the cap is left out whole. The two-gate report fits in `MESSAGE_RESERVE` with a name and a message at their caps | Case in `tests/test_a_gate_that_fails_says_so.py`, seen red with the cap removed. The reserve comment's re-measured figures are pinned by the case that already pins 533 and 909 |
| S15 | #722 when the record is old | Given a pending record written with a 300-unit `error` and a 400-unit `message`, the way a plugin older than 0.17.0 could write it. Then `describe` says each capped | Case, seen red with the read-side cap removed |
| S16 | Pillow is pinned once | `run_tests.py` holds `PILLOW = "pillow==12.3.0"` in `PACKAGES`. `test.yml`'s install line, `publish-release.yml`'s install line and `CONTRIBUTING.md`'s fallback carry that exact string. An adopted `.venv` without it is topped up, the way `markdown-it-py` is | The existing pin-holding cases in `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` are extended to Pillow |

## Data & interfaces

**`.github/scripts/release_seal.py`** (new). A stdlib module at import; Pillow
is imported inside `png` alone. The names below are a starting point for the
builder, not a contract:

| Unit | Does |
|---|---|
| `rgb(colour)` | A triple as is, a 256-colour code through xterm's cube and grey ramp. Raises `ValueError` for 0–15, which the sheet never uses |
| `paint(letter)` | `compose`'s cells → an ordered list of `("rect", x0, y0, x1, y1, rgb)` and `("text", cx, cy, char, rgb, bold)`, in a 14 × 28 px cell with each half 14 px tall. This is the hand-drawn script's loop, kept free of Pillow so the pin needs no third-party module |
| `font()` | The first font that loads: DejaVu Sans Mono under `/usr/share/fonts/truetype/dejavu/`, then Menlo, then Consolas, then `ImageFont.load_default(size=22)`. Each is tried at 22, with the bold face for line 1 where one exists. The log names the font used |
| `png(ops, size, path)` | Pillow: an RGBA image, transparent where nothing is painted |
| `suite_counts(path)` | JUnit XML → `(passed, skipped)`. Raises on a parse failure or on any failure or error |
| `chain_counts(root, pulls)` | `(items, rounds, capped, deferred)`. Each element is a number or `None` for not read |
| `release_rows(version, sha, pulls_n, issues_n, suite, chain)` | The fixed rows (S8) |
| `alt_text(rows)` | S11 |
| `main()` | Environment: `TAG`, `REPO`, `GH_TOKEN`, `SUITE_XML`, `SUITE_OUTCOME`, `DRY_RUN`, `SEAL_PNG`. Always exits 0 (S2) |

**`publish_release_note.py`.** `release_body` builds the glance block through
a named `glance(work, closed, people)`. A second function,
`sealed_glance(image_url, alt, work, closed, people)`, builds the success-path
replacement, so both shapes live in the file that owns the heading.
`main` writes `created=true` or `created=false` to `$GITHUB_OUTPUT` where that
variable is set. A write failure is printed and ignored. The exit codes and
the note's text are otherwise unchanged.

**`publish-release.yml`.**

```
publish:   (unchanged) + id/outputs: created
seal:      needs: publish · if: needs.publish.outputs.created == 'true'
           checkout (fetch-depth 0) · setup-python 3.12
           pip install pytest pytest-xdist markdown-it-py==4.2.0 pillow==12.3.0
           git config user · pytest tests/ -q -n auto --junitxml=$RUNNER_TEMP/suite.xml
           python3 .github/scripts/release_seal.py   (GH_TOKEN, TAG, REPO, SUITE_XML, SUITE_OUTCOME)
           every step continue-on-error: true
```

`GH_TOKEN` is set on the draw step alone, so the suite runs with no token in
its environment. `tests/conftest.py` would neutralise one anyway.

**The rows** (0.17.0's, which the owner saw):

```
SEALED   v0.17.0
tag      233f0455
         main
PRs      10 merged
issues   11 closed
suite    7003 passed, 66 skipped
items    10 . 27 rounds
capped   6 of 10
deferred 13 issues
```

**What was measured or read and is not repeated by this frame:** the
plugin's longest exception class name is `NoMutationDefined`, **17
characters**. #722's body and 0.17.0's round 3 both say 28. That figure is
false by `git grep` over `hooks`, `skills`, `bin` and `.github` at
`8c18d974`. The bound #722 needs comes from foreign names, so the correction
changes no decision. It does correct a sentence the smith should not copy.

**Ledger obligations** (read 2026-10-03, and to be done by the build):
- `seal/releases/0.17.0.md` B1 says the reserve holds the two-gate report at
  909. The re-measured figure makes that false, so it is corrected in place
  with a `Corrected <date>` note.
- B2 cites `seal_stamp.py#admitted`, which drifts with #721's rewrap. It is
  re-read and re-stamped.
- `seal/releases/0.16.0.md` G1, G2 and G3 cite `dispatch.py#record`,
  `#describe`, `#draw` and `#report`. Each is re-read against the cap.
- `seal/releases/0.15.1.md` P1 and `seal/releases/0.16.0.md` P1-1 cite
  `run_tests.py#PACKAGES` and `#MARKDOWN_IT`. P1-1's claim that markdown-it-py
  is *the suite's one test-only package* becomes false and is corrected in
  place.
- New rows go in `seal/ledger/1790993139-the-release-seal-is-drawn-and-attached-at-publish-time.md`.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-10-03 by framer, before the build.
