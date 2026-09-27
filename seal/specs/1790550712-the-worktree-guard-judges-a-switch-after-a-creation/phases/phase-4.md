# 1790550712-the-worktree-guard-judges-a-switch-after-a-creation — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | see `plan.md`'s Status cell for phase 4 |
| Ran by | unknown — the spawn prompt named no agent or model for this record; the orchestrator may fill this row |

## What this phase was asked

Records. The ledger fragment's W1–W7 rows, in a `seal/ledger/` directory this
work creates. Every drifted row re-read and re-stamped in its own file with a
dated note, or corrected in place where an edit made it false. The work item's
`changelog.md`. The S12 grep sweep run again by construction, outcome words
and Korean reason strings included, adding any copy the 19 missed. Q4's count
for the PR body, aggregates only. `overview.md` closed. Verified by
`evidence-check --strict` exiting 0 and the S12 greps returning only records of
the past.

## What this phase found

**Twelve rows, eleven anchors, three files.** `evidence-check` named eleven
drifted coordinates; each row citing one was read against this work's edits.
Two claims had become false and were corrected in place:
`seal/releases/0.15.5.md` A1 (*not marked `isSidechain: true`*) and A4's note
(*a switch written after a creation … is never judged*). The other ten hold and
carry a `Re-read 2026-09-28` note saying what moved. `seal/releases/0.9.4.md`
has two rows labelled `S3` from two work items, so the note there was placed by
the row's full opening rather than its label.

**`plan.md`'s stamps made the strict check exit 2.** The records arm reads a
live work item's `plan.md`, and its §*Ledger rows this work re-reads* stamped
seven anchors at the base's hashes. Under `--strict` a drifted record stamp is
exit 2, like a drifted ledger row. They were re-stamped to the state their rows
were re-read against, with a builder's note. `skills/evidence-check/SKILL.md`
says record drift *does not fail the run*, which the code contradicts; that is
recorded in `overview.md` §*Not done* for the orchestrator.

**W8 joined W1–W7**: the heredoc case phase 3 added is a claim about the tree,
so it has a row.

**The S12 sweep, executed.** One `git grep` per old phrase family, excluding
`seal/specs/*/rounds/*`, `seal/specs/*/phases/*`, the released `CHANGELOG.md`
and this work item's own directory:

| Phrase family | What remains |
|---|---|
| *classifies the first*, *FIRST segment it can read*, *stops at the first verdict*, *one silent exit* | `seal/releases/0.9.4.md` S3's note, which now carries a re-read note saying the sentence it cites was corrected |
| *isSidechain: true*, *is True*, *not marked `isSidechain`* | 0.15.5 A1's correction note; `seal/specs/1790381327-…/overview.md`, a closed work item's memo; this work's new test docstring |
| *No other Claude session is working in this tree*, *작업 중인 다른 Claude 세션은 없지만* | only this work's tests, which assert the old wording is absent |
| *exactly five*, *32 command-word*, *1260*, *230*, *falls to `ask`*, *costs one prompt*, *heredoc line that IS* | the correction notes in `seal/releases/0.9.1.md`; the module docstring's sentence that the heredoc residual is closed, which is true; this work's new test comments quoting the old text |
| *true of two of them* | nothing |
| `/usr/bin/git` with an outcome word | every hit now says the allow is refused and the guard is silent |

A second pass over `README.md`, `README.ko.md`, `skills/`, `agents/`,
`templates/`, `CONTRIBUTING.md` and `docs/` for the guard's verdict words and
tokens found nothing this work falsified: the README rows describe the switch
direction without an order of segments.

**Q4, executed** (`questions.md` Q4): 0 of 44 creation commands, over 49,370
Bash commands in this machine's 728 transcripts, are followed by a switch or a
checkout in the same command. The script ran from the session's scratch
directory and printed counts only.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
