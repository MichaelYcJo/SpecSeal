# 1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file — phase 2

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | bcc412bf |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

Spec I3, I4 and I8, `plan.md` phase 2: the `framing` row and the rewritten
tying paragraph in `docs/review-handoff-protocol.md`; the step-1 clause in
`skills/verify/SKILL.md` §*Measure the segment*; the `session-cost --segments`
cell in `README.md` and `README.ko.md`. `test_the_protocol_names_a_bar_per_segment_kind`
extended for the row and a case that the tying paragraph names `--segments`,
each red at the base; the advisory case and the draft case green unchanged;
the flow-log module and the README readers green.

## What this phase found

- **Three cases, all red at the base.** The framing assertion inside
  `test_the_protocol_names_a_bar_per_segment_kind`; the new
  `test_the_tying_paragraph_says_which_reading_applies_the_bars`, scoped to the
  bars section by the module's existing `bars_section`; and
  `tests/test_a_segment_feeds_the_flow_log.py::test_every_page_describing_the_segments_mode_names_its_grade`,
  which holds the SKILL.md clause and both README rows (S13). The last was
  red on its first assertion, the SKILL.md one.
- **The tying paragraph keeps the pinned sentence word for word.**
  *batching advisory below 1.2 and stays there* stands, and *cannot tell a
  reviewer's transcript from an edit-test loop* now reads *the plain reading
  cannot tell…*, with the reason a lone transcript carries no kind. The
  `--segments` half is a paragraph of its own after it.
- **Q5, first half: no draft bump.** Every draft in the protocol's Status
  history adds a record field or a handoff requirement, and the two earlier
  edits to this table (#565, #639) bumped nothing; a new lens row is neither.
  `test_the_title_and_the_status_section_agree_on_the_draft` is green.
- **The README cells name the exemption in prose**, so a plugin user meets
  *a smith's edit-test loop is exempt* without opening the protocol, which
  does not ship to their repository. The Korean edition is written as Korean
  sentences rather than a translation of the English clause.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sentence *the script cannot tell a reviewer's transcript from an edit-test loop*, as a claim about the whole script | narrowed in place to the plain reading; `seal/releases/0.4.0.md`'s row that repeated it is corrected in phase 4 |
