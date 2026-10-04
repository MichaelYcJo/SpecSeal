# 1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | d6753af8 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `settle --retire-process` to spec D3 and D4: scenarios S1–S4, S8 and
S9, and the dry-run section of S10. Write `skills/settle/SKILL.md`'s section
for the arm, its output and its guards in the same commit as the strings it
pins. See every new case red against the unbuilt flag. Answer Q6: where the
section goes in the skill and the exact wording of the output lines. Name
`encoding="utf-8"` on every file read the arm adds.

## What this phase found

**The frame held.** Every coordinate `spec.md` §*Grounding* names for this
phase was opened at e141980a, and none disagreed with the spec.

**Two of the four helpers the spec says to reuse answer the fold's question,
not this arm's, and each was narrowed rather than copied.**

- `anchored_rows` asks whether an anchor lies anywhere under
  `seal/specs/<id>/`. That is right for `--retire`, which takes the whole
  directory. This arm takes part of it, so a row anchored at `spec.md` would
  have held an item whose `spec.md` stays. `process_anchored` filters its
  rows to the anchors inside a file the arm takes, and counts the others as
  live, so the verdict reads *narrow* where a row also cites a file that
  stays. A case pins the negative direction.
- `citations` lists any citation into the directory. It gained an `inside`
  parameter, and `CITATION_RE` gained a lookahead group, `rest`, holding the
  path after the directory name. The lookahead consumes nothing, so a second
  citation on the same line is still found and `--retire`'s listing is
  unchanged.

**Q6, answered.** The section is `## The process record leaves first, fold or
no fold`, placed between *A fold is not a work item* and *The procedure*. It
is not a step of the procedure, because it is not part of the fold and runs
before it. The output strings are module constants (`PROCESS_HEADING`,
`PROCESS_TODO_HEADING`, `PROCESS_ANCHORED_HEADING`, `PROCESS_UNKNOWN_HEADING`,
`PROCESS_CITED_HEADING`, `PROCESS_DONE`) plus the `removed …` lines and the
closing count, `retired the process record of N work items (F files); K
kept`. `test_the_skill_quotes_every_line_the_arm_prints` holds the skill to
quoting each constant.

**Measured on this repository with the built dry run, executed.** `settle` at
`origin/main` = e141980a prints `525 files in 54 released work items`. The
spec's 525 matches. 54 rather than 55 because one released directory,
1788177600, holds only `routing.md` and `overview.md`.

**Red first, executed.** All 16 new cases failed against e141980a's
`settle.py`, before any edit to it. After the build, 15 passed and the skill
pin stayed red until the section was written.

**Every unit the arm added was broken once through `mutation-check`, and all
15 breaks went red.** The breaks covered: the `pr.*.md` match, the todo
guard, the unknown-file branch, `taken_by`'s directory test,
`process_anchored`'s filter, `cites_a_process_record`, the anchored guard in
`retire_process`, the kept count, the per-directory file count, `citations`'
`inside` filter, the mutually exclusive group, the nothing-left branch, the
dry run's takeable filter, the report's section call and `main`'s dispatch.

**Left as it stands, and named here.** `REMOVED_SAYS` and `RELEASED_SAYS`,
which `write_anchored` prints, speak of "a directory a retirement removes" and
"the fold's own fragment". This arm reuses them as they are, because the
action they prescribe is the same. A rewording would move `--retire`'s pinned
output, which is outside this work item. The cheat sheets in `README.md` and
`README.ko.md` carry `settle [--retire]` and are not among the carriers spec
D6 lists, so they were not edited.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
