# 1788445862-a-phase-hands-the-next-one-a-record — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | c5ad90e |

## What this phase was asked

Build phase 3 only, of the 4-phase table in `plan.md`: give
`templates/sdd-round.md` a new `## What this round was asked` section,
placed after the field table's closing HTML comment and before
`## Verdicts`, with its own comment explaining the gap it answers — #81's
round 1 was the cheapest round measured (7.6 minutes, 29 tool calls, one 🔴
four 🟡) because its prompt named eight specific things to try to break, a
fact recoverable today only from a transcript. Give `skills/code-review/SKILL.md`
the instruction, beside "A round record starts from `templates/sdd-round.md`"
(around its "Cross-session records" section), that the orchestrator copies
the round-specific spawn content into that section when writing `round-N.md`
right after posting — the same "phase-specific content, not the boilerplate
the contract/agents already carry" framing phase 2 gave `agents/smith.md`.
Add the plan's Phase 3 test cases to a new module
`tests/test_a_segments_record_says_what_it_was_asked.py`: the round
template's new section exists outside comments as a placeholder;
`skills/code-review/SKILL.md` carries the copy instruction; a cross-file
consistency case comparing the round-side and phase-side section headings
and instruction wording, so the two do not drift into two different
conventions for one behavioral guarantee — mindful of phase 2's
angle-bracket-vs-bare-form finding when writing that comparison. Every new
case shown red first. Phase 4 was explicitly out of scope: stop once phase
3's own scope is committed and its narrow verification is green.

Same extra step as phases 1 and 2: once the round-side section and
instruction existed, use them — rather than improvise — to write this file,
noting that a mid-session `specseal:smith` spawn cannot pick up
`agents/smith.md`'s own edited instruction to do this automatically, because
the loaded agent persona and skills come from the plugin's version cache,
frozen for this session rather than this branch's working tree (given as
background fact, not investigated here).

## What this phase found

**The cross-file consistency case could not compare byte-identical text, and
that is the same finding phase 2 already made, one file over.** The plan's
Phase 3 row asks for a comparison "so the two do not drift into two different
conventions", but the two headings are `## What this round was asked` and
`## What this phase was asked` — they cannot be byte-identical, because
`round` and `phase` are the words that make each record about its own
segment. What has to match is the skeleton around that one word, and the
same split phase 2 found for `phase-N.md` vs. `phase-<N>.md` reappears here
in a different shape: `templates/sdd-round.md`'s own path comment already
said `rounds/round-<N>.md` before this phase touched the file (bracketed,
matching `templates/sdd-phase.md`'s own `phases/phase-<N>.md`), while every
file that only points at either record from prose uses the bracket-free
form. This phase's new consistency test checks the heading skeleton and the
copy-instruction wording, not the templates' self-descriptions — flattening
those to match would re-break the distinction phase 2 already recorded the
reasoning for.

**A constant-to-constant comparison cannot be shown red.** The first draft
of `test_the_heading_skeleton_matches_across_round_and_phase` compared two
Python string literals (`ROUND_HEADING`, `PHASE_HEADING`) to each other —
true by construction, and it stayed green even with both templates reverted
to their pre-phase-3 state, because nothing in it ever opened a file. Fixed
by extracting the heading through a regex (`^## What this (\w+) was asked$`)
run against the actual template text, so the test fails when the real
heading in either file stops matching the skeleton, not only when someone
edits the test's own constants.

**Multi-word phrase pins need whitespace-normalized reads when the prose is
line-wrapped.** `never the boilerplate` and `cheapest round` each landed
split across a line break by this repository's own wrap width, so a raw
substring check on the two-word phrase failed even though the words were
both present and adjacent in the rendered prose. Fixed the same way
`test_the_fixes_name_their_surface.py`'s `flat()` already does it: collapse
whitespace before checking a multi-word phrase, and keep raw-text reads only
for the structural checks (heading order, section boundaries) where a real
line break is part of what is being verified.

**Mutation testing for this phase's units.** No new production code unit was
added — the deliverable is a template section, a skill paragraph, and a test
module. The equivalent check was run directly: the two implementation files
(`templates/sdd-round.md`, `skills/code-review/SKILL.md`) were stashed as a
pair, all nine new cases were confirmed failing against the pre-phase-3
state, and the stash was restored and the suite re-run green. That is the
same act as breaking a unit and watching its covering cases go red, applied
to the whole phase's diff at once rather than one function at a time,
because the diff itself is the unit here.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | — |
