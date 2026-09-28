# a resumed agent's own transcript is sliced (#637) — questions for the planner

<!-- seal/specs/1790562540-a-resumed-agents-own-transcript-is-sliced/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row needs a person, and none blocks the build.** Each row below has a
default the build goes ahead on.

**Judgments #637 left open that the tree answered.** They are listed here so
nobody reopens them. The grounds are in `spec.md` §*Scope* and `plan.md`'s
Alternatives table.

- Option 1 is triggered by the coordinator marker, not by the `subagents/`
  directory. Every marker-less file keeps today's empty branch byte for byte.
- Option 3 ships beside option 1: one added line in the plain reading, under
  the same condition, before the `span` line. Option 2 stays rejected.
- The own-file rows are labelled by the file's name and are not joined to a
  spawn. `unnamed` counts walked files only, so it is 0 here. The page
  prints no join counts and no §6 reconciliation line, and it does print the
  §6 breach list.
- `--json` carries the same rows, with an `own_file` key present only in that
  case. Every existing case's dict is unchanged.
- An agent's own file never has transcripts beside it on this machine: every
  `subagents/` directory is at `<session>/subagents/`, 52 of 52 (executed,
  2026-09-28). So the case of an own file with children beside it is out of
  scope rather than a question.
- Naming the rows from `agent-<id>.meta.json` is out of this item. Whether to
  file it is the orchestrator's call at the pull request, and it does not
  change what gets built.
- The ticket's fixture sentence (*two coordinator messages … two slices*)
  holds only for adjacent messages. The spec takes both shapes (S1, S2,
  S2b).
- The family units stay untouched for #642 (`plan.md` §*Technical context*).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | On a real resumed agent transcript on this machine, does `--segments <the agent's file>` print the same slices as `--segments <the session's main transcript>` prints for that agent (the ticket's *How to verify*, second bullet)? The frame could not settle it because the code does not exist yet. S3 settles the same question on a fixture | a measurement | the same numbers, in which case S12 is closed. Different numbers mean the fixture misses a real shape, and the phase that meets it records the divergence and adds the shape as a case | S3's fixture equality stands in until phase 3 runs the three commands. Pick the file with `resume_cuts` itself, so the choice does not rest on a text search that also matches transcripts quoting the sentence | ✅ measured 2026-09-28 at `b07698cc`: on a resumed `specseal:smith` file picked by `resume_cuts` (2 coordinator messages), both routes print three slices whose span, calls, tools per turn, mean gap and tokens are equal row for row, and their calls sum to the plain reading's 233 (`phases/phase-3.md`) |
| Q2 | The exact words of the own-file header, the `agent` legend line in that case, and the plain hint. The frame could not settle it because wording is fixed by writing it, and `spec.md` In 2 and In 4 fix only what each must say | the work | any wording that says what In 2 and In 4 require. It must not equate a segment with a spawn cycle (`tests/test_one_word_one_meaning.py`'s `segment` block), and each line is pinned by S5 and S8 | the builder's wording, pinned | ✅ written 2026-09-28 in phases 1 and 2: the header *`<path>`: an agent's own transcript, cut at N coordinator message(s) into M slice(s)*, the legend *No spawn was joined … Given the run's own transcript, the same slices carry its name*, and the hint *N coordinator message(s) in this transcript, so the span below covers every stretch of work and the waits between them — `--segments` prints one row per stretch*, each pinned (ledger A4, A5) |
