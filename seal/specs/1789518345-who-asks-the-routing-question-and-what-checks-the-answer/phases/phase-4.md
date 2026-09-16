# 1789518345-who-asks-the-routing-question-and-what-checks-the-answer — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 72edbd49 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

Three acts removed from `agents/smith.md`'s phase 2 — the design gate, the
routing batch, the `routing.md` write — replaced by the sentence that phase 2
is the caller's spawn. **The waiver paragraph and its `# RIDER:` stay**: the
span is content, not the line range. Line 125's inference removed and not
rewritten elsewhere. Added: where `routing.md` declares a framer and no
`spec.md` exists, `smith` stops and says so rather than building.

## What this phase found

**The design gate had a second copy outside the named span, and removing only
the named one left the file with two answers.** `plan.md`'s Technical context
locates the design gate at lines 53–72. Sixty lines further down, inside the
same phase 2, the rung paragraph said *present 2–3 approaches with failure
scenarios and wait for an explicit go*. That IS the design gate by content,
and it survived a removal keyed on the span — leaving `agents/smith.md` saying
*phase 2 is your caller's spawn* in one paragraph and *wait for an explicit
go* in another, which is the disagreement across documents this work item is
about, arriving inside one file.

The repair is narrow on purpose. The rung CONDITION stays — `observable
behaviour` and the four defaults are what
`test_the_top_rung_names_behaviour_rather_than_a_count` requires of this file,
and a smith below the top rung still needs to know what the work owed. Only
the asking clause moved: the plan was drawn before the smith and somebody read
it, and that reading is the gate. **This is the one place phase 4 went past
the span its plan named**, and it is recorded here rather than left for a
reviewer to find.

**The third mutation the plan named had no case to make red.** It asks for
*the case that keeps the waiver example as smith's own application*. The
module's docstring names that example among the applications #107 kept
deliberately, but `test_a_citation_is_not_a_copy`'s `kept` dict for
`agents/smith.md` listed three phrases and the waiver was not one of them. So
the carve-out was stated in prose and held by nothing, and the plan's own
warning — that removing it *would turn that module's stated carve-out into a
lie* — was already half true before this branch. Two phrases were added to the
dict, and one of them is load-bearing twice over: `a bare word is a pathspec
and git rejects it` is the ten-word run that SETS `LONGEST_KEPT_APPLICATION`,
so deleting the example would also stop that measured constant describing the
tree.

**Two cases in the waiver module pinned acts that had moved**, and both had to
be inverted rather than deleted. `test_the_smith_carries_both_halves…`
required `three axes` and the four routing answers in `agents/smith.md`; it is
now `test_the_smith_carries_its_own_half_and_not_the_questions` and requires
their absence. `test_every_document_shows_the_third_axis_ROW…` required
`implementation (smith · the session` there; it now refuses it. Deleting
either would have left the paste-back invisible; inverting them is what makes
the same edit red from the other side.

**An absence alone leaves a hole a reader fills with the old behaviour**, so
each removal is paired. The removed inference is paired with the stop
instruction; the removed design gate is paired with
`test_what_replaced_them_says_whose_the_act_is`, which requires the file to
name `agents/framer.md` and `skills/implement/orchestration.md` as the acts'
new owners. A smith meeting a phase 2 that merely says less reasons its way
back to asking.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The design-gate paragraph from `agents/smith.md` phase 2 | `agents/framer.md` §*Yours is the one interactive phase* (the asking) and the caller's spawn (the approval). `plan.md`'s approval line is the gate's record and already existed |
| The routing batch — three axes, one `multiSelect`, three checkboxes | `skills/implement/orchestration.md` §*Orchestrator: how the work is routed*, in its new two-question shape (phase 2), and `agents/framer.md`, which now asks it |
| The `routing.md` write sentence | `agents/framer.md` §*The four writes*, where `routing.md` is the first row (phase 3) |
| The inference *Where no frame was drawn, the ladder put the work below the rung that calls for one* | **nowhere — it is unsound and is not rewritten elsewhere.** What replaces it is the stop instruction, which is an instruction for the same state and makes no claim about the rung |
| *present 2–3 approaches with failure scenarios and wait for an explicit go* from the rung paragraph | the same sentence, rewritten to say the `plan.md` was drawn before the smith and the reading of it is the gate. The rung CONDITION stays in place |
| `test_the_smith_carries_both_halves_rather_than_only_citing_them` (NAME NOT IN TREE — renamed by this work item)'s requirement that `agents/smith.md` carry the routing vocabulary | `test_the_smith_carries_its_own_half_and_not_the_questions`, which requires its absence, plus `test_the_smith_claims_no_act_another_definition_owns` for the three acts by name |
