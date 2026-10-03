# Implementation Plan: the release seal is drawn and attached at publish time

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

The note keeps publishing exactly as it does now. After it, a separate job
in the same workflow runs the suite at the tag. It draws `seal_stamp.compose`'s
letter as a PNG, one cell to one rectangle, attaches the PNG, and replaces the
generated glance table with the image and one line of its counts. Every
failure in that job is a log line and a `::warning::`. Two small fixes in the
stamp's reserve ride along: #721's docstring and #722's type-name cap.

## Technical context

Coordinates are content anchors, as the ledger writes them:

- `.github/workflows/publish-release.yml#jobs.publish`: one job, `contents:
  write`, running `python3 .github/scripts/publish_release_note.py`.
- `.github/scripts/publish_release_note.py#release_body`: builds
  `GLANCE_HEADING` and its table inline. `#main` returns 0 before creating
  anything when `release_exists`. `#merged_pulls` is the one `gh pr list` call,
  fields `number,title,author,body`.
- `skills/verify/scripts/seal_stamp.py#compose`, `#block`, `#letter`,
  `#DEFAULT_SCALE` and the colour constants `PARCHMENT`, `SHEET_EDGE`, `INK`,
  `TITLE`, plus the disc's triples. `#letter` pads the label to eight
  (`{label:<8}`). `skills/verify/scripts/broad_gate.py#PANEL_VALUE_WIDTH` is 23.
- `hooks/routing.py#item_dir`, `#rounds`. `skills/code-review/scripts/chain_check.py#verdict_table`, `#verdict_of`.
- `hooks/dispatch.py#first_line` (the UTF-16 cutter), `#record` (writes
  `type(exc).__name__` uncapped), `#describe` (interpolates the record's
  `error` and `message` with no bound of its own).
- `.github/scripts/run_tests.py#MARKDOWN_IT`, `#PACKAGES`, and the function
  that tops up an adopted `.venv` with markdown-it-py. That function is the
  template for Pillow.
- The hand-drawn script, `release_seal_png.py`, in the 0.17.0 session's
  scratchpad. It is read-only and outside the tree; the spawn prompt carries
  its path, which names a real user directory and so is not repeated here. `rgb`, `draw` and the 14 × 28 cell are
  what `paint` and `png` start from. Its Menlo path is macOS-only, which is
  why `font()` has a chain.

**What breaks in six months.**

- #715 moves the round records. `chain_counts` then reads nothing and the
  three chain rows say `not read`. The image still ships, and nothing is wrong
  that a reader could miss. The defence is that `chain_counts` reaches round
  records only through `routing.rounds` and `chain_check`'s readers, so a
  layout change has to move those, and the readers' own cases go red first.
- A Pillow release changes `load_default`. The pin holds the version, so this
  happens only when a person moves the pin.
- The release-download URL stops drawing in some browser. The counts line
  and the alt text still carry every number.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **The PNG writer in stdlib**: zlib and struct for the raster, an embedded bitmap font for the text | Someone has to author a font. The result is not the Menlo-like letter the owner saw on 0.17.0's page. And a hand-made glyph table is a second drawing that nothing pins | rejected |
| **Pillow imported from `seal_stamp.py`** | A shipped skill script grows a third-party import path. That breaks `CONTRIBUTING.md`'s *the gates themselves are stdlib-only*, for a function no user's session calls | rejected |
| **Pillow installed only in the workflow; the pixel case `importorskip`s** | The pin skips locally and runs only on CI. This repository refuses that split: `CONTRIBUTING.md` makes even `gh` behave the same on both | rejected |
| **Pillow test-and-release-only, pinned once in `run_tests.py` beside `MARKDOWN_IT`, drawn from `.github/scripts/release_seal.py`** | One more package in the suite's environment, and one more pin for the existing holding cases to keep in step | **chosen**. It follows #667's precedent for a test-only package |
| **Suite count from the release pull request's CI log** | The owner's comment: a log is not a stable API | rejected |
| **Suite count from a JUnit artifact `test.yml` uploads, downloaded by the publish job** | Couples `test.yml` to the release. Races the `push: main` run that starts at the same merge. Reads a tree that is not the tag's | rejected |
| **Suite run at the tag in the `seal` job, counts from `--junitxml`** | Minutes of runner time after every release, which nobody waits on. The note is already published by then | **chosen** |
| **Chain rows from the merged pull requests' bodies** (#718's table) | Measured on 0.17.0's eleven pull requests: no body carries a `specs/` marker, and the `## Review chain` sections are prose that no template or checker holds. A parser of them is a parser of one orchestrator's habits | rejected. Grounds in `questions.md` Q1 |
| **Chain rows from round records at the tag, through the shared readers, plus the `chain: capped` label** | #715 may move the records. Then the rows read `not read` rather than a wrong number | **chosen**. It reproduces 0.17.0's 27 rounds and 6 capped exactly |
| **Capped only, dropping rounds and deferred** | Loses what the owner's issue lists under *What it says* | rejected |
| **Draw first, then create the release with the image already in the note** | Publication waits on the suite. A draw failure sits inside the job that publishes. #718's fallback becomes a branch to get right rather than the default | rejected |
| **Note first, then the seal as a second job that edits it** | A window of minutes in which the note has no image. An orphaned asset if the edit fails after the upload | **chosen**. The fallback is the state the release is already in |
| **Edit any release at the tag on a re-run** | Overwrites a note that may have been edited by hand, which `publish_release_note.py`'s docstring names as the one way this could destroy a person's work | rejected. A `created` output gates the job |
| **#722: count the type name into the reserve** | A foreign name has no bound, so no fixed reserve can count it | rejected |
| **#722: cap the name at write and read, with `first_line`'s cutter** | A 40-unit cut can shorten a real class name | **chosen**. The cut name still identifies the class, and the text cap already does the same to messages |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #721 and #722. `admitted`'s docstring becomes round 3's paste-ready paragraph. `NAME_CAP = 40` and one UTF-16 cutter shared by `first_line` and the name. `record` caps at write, and `describe` caps `error` and `message` at read. The `MESSAGE_RESERVE` comment is re-measured over `describe` with a name and a message at their caps, for one, two and three gates. Ledger: `0.17.0.md` B1 corrected, B2 re-stamped, `0.16.0.md` G1–G3 re-read | S13, S14, S15, each seen red first. `bin/test tests/test_a_gate_that_fails_says_so.py tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py -q` | |
| 2 | The renderer's PNG and its pin. `release_seal.py` with `rgb`, `paint`, `font` and `png`. `PILLOW = "pillow==12.3.0"` in `run_tests.py#PACKAGES`, with the adopted-`.venv` top-up. The same string in `test.yml` and `CONTRIBUTING.md`'s fallback. The holding cases extended. `seal_stamp.py`'s docstring names the new importer | S6, S7, S16. The `paint`-against-`block` case runs without Pillow. The pixel case decodes a PNG drawn from the fixed rows. Both are seen red by swapping two codes in `rgb`. `bin/test tests/test_the_release_seal_is_drawn.py tests/test_the_suite_has_a_command_that_is_cheap_twice.py tests/test_a_script_says_which_interpreter_it_needs.py -q` | |
| 3 | The rows and their sources. `suite_counts` (JUnit), `chain_counts` (routing and chain_check readers, plus labels), `release_rows` (the fixed set with the continuation-row rule), `alt_text`. A measurement over 0.17.0's tree, recorded in `phases/phase-3.md`, with the deferred rule's 12 against the owner's 13 explained or left as Q10 | S8, S9, S10, S11. The 0.17.0 measurement is run against the tree at `233f0455`, with the merged pull requests' head branches written into a fixture, not fetched by a case | |
| 4 | Publishing. `publish_release_note.py`: `glance` and `sealed_glance` split out of `release_body`, and `created` written to `$GITHUB_OUTPUT`. `release_seal.main`: draw, upload, read the body, replace the table exactly once, edit. Every failure exits 0 with a line and a `::warning::`. `DRY_RUN`. `publish-release.yml` gets its `seal` job. Docs: `docs/branch-and-release.md`'s release-tail bullet and its `Enforced by:` line, `docs/release-checklist.md` §6's box, the workflow's header comment. The changelog fragment and the ledger fragment | S1, S2 (the fallback case #718 asks for), S3, S4, S5, S12. The existing module `tests/test_a_release_publishes_its_note.py` stays green, apart from the workflow case rewritten under S5. `bin/test tests/test_a_release_publishes_its_note.py tests/test_the_release_seal_is_drawn.py tests/test_the_release_tail_does_not_end_at_the_tag.py -q` | |

Phase 1 depends on nothing else and comes first because it is the smallest
slice that closes two issues. Phase 2 comes before 3 so the rows are drawn by
a renderer that is already pinned. Phase 4 is last because it is the only
phase that changes what the tag push does.

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

- **New dependency, test-and-release only:** `pillow==12.3.0`. Its wheels
  cover CPython 3.12 on manylinux, macOS (x86_64 and arm64) and Windows, read
  from PyPI on 2026-10-03. A `.venv` built before this branch takes one
  top-up install on its next `bin/test`. A plugin user installs nothing.
- **The tag push runs a second job:** the suite at the tag, then the draw.
  Its runner minutes are new and unmeasured. Nobody waits on it, because the
  note is already published.
- **The release note changes shape on success:** the glance table becomes an
  image and one line. On any failure it is today's note, and the job log
  carries a `::warning::` saying why.
- **No new permission.** `contents: write` already covers `gh release upload`
  and `gh release edit`. `gh pr list` reading `labels` and `headRefName`
  under that block is read, not executed. Today's call reads `author` and
  `body` under the same block on a public repository, and 0.17.0's note proves
  it ran. A refusal there fails the call, and S2's fallback leaves today's
  note.
- **Compatibility:** `publish_release_note.py`'s note is byte-identical to
  today's whenever the seal does not run.
