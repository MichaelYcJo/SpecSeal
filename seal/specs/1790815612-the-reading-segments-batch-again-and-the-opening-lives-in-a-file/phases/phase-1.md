# 1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file — phase 1

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 82a70522 |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

Spec I1 and I2, `plan.md` phase 1: one section in `agents/framer.md` after
§*What you read, and how widely* — a skeleton `spec.md` inside the first few
calls; one read call bounded at about six reads or ranges and never the whole
list, citing §10 by number in the framer's own words; a large file by range;
the bar 1.4 and the band 1.46–1.79; no prohibition on parallel reads. Open the
changelog fragment with the entry. New cases for S1 and S2, each seen red;
the definition-reading modules green unchanged.

## What this phase found

- **The section is `## How a frame opens`.** The two new cases scope to it by
  heading (`framer_opening`), so a rename has to bring them along.
- **Red, three ways.** Both cases were red against the base (the section did
  not exist). The absence half was seen red separately by planting *Do not
  open with a parallel read burst.* in the section: the opening case failed on
  `'read burst'`. The number case was seen red by deleting *promises no
  saving*. Both mutations were reverted through `Edit` and the module re-run
  green.
- **The wording constraints held at the first draft.** No 15-word run of a
  contract section (`test_a_moved_rule_leaves_its_definition.py`), no batch
  phrase beside a person-answering word (the section uses *one call* and *go
  out together*, never *in one batch*), 88 columns.
- **`overview.md` was owed from the first commit.**
  `tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`
  refuses a work item with a `spec.md` and no `overview.md`, so the memo was
  opened in this phase rather than at the end.
- **The bound's grounds in the file are the ones a reader can open.** The
  definition cites #548 (0.15.1, 2.3–3.1, all finished) and #640 as where the
  number can be overturned. This frame's own batch sizes, which the spec also
  names as grounds, are Q1's measurement and are not quoted in the definition
  until phase 4 reads them.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
