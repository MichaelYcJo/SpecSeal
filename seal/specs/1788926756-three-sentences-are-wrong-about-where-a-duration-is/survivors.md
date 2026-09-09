# three sentences are wrong about where a duration is — excused survivors

<!-- Read by `survivor-check --exempt`. The QUOTE is the anchor, so an
exemption stops applying the moment that text changes, and an excused survivor
is still printed with its grounds. There is no value meaning "check nothing". -->

The range reported three places and one of them was a real survivor, corrected
rather than excused: **#145's Q5 still described the span understatement as
unfixed and gave the grounds this work item removed.** Q5 is the question this
work item answers, so leaving it in the present tense would have left the
answer's own source page contradicting it. It now opens with the answer, the
date and where it landed, and its false half is corrected in place — with the
option table kept as it stood, because that table is what the answer was
chosen against.

The two below are both this work item's own documents, and in both cases the
standing text is **true**. `survivor-check` matched them because `plan.md`'s
phase-3 cell was reworded in the same range, not because anything false
survived.

**Writing the two rows below did not excuse those survivors — it hid them,
and that is a defect in the checker rather than in the rows.** Executed:
`examine` scores both candidates at **1.626** at `9d9e717`, above the 1.6
floor, and **0.758** at `6a22d56`, the commit that changed this file and
nothing else. The mechanism is the added-n-gram subtraction, not document
frequency. `corrected` returns the n-grams the range WROTE alongside the
sentences it removed, and `wanted` subtracts them from what the run looks
for at all — because a phrase the fix kept is not a phrase the fix
corrected. An exemption quote is by definition the survivor's own wording,
so writing the row puts those phrases on the written side and deletes them
from the search set. The reported phrase changes rather than weakening:
*span is taken from* at 1.626 before the row, a different and weaker *the
last result* at 0.758 after it. Dropping every `survivors.md` from `corpus`
moves the same candidates from 0.758 to 0.757, so document frequency is
worth a thousandth here and is not the cause.

What it costs is the guarantee this file's own header states. An exempted
survivor is supposed to stay printed under `exempt`, and the quote is
supposed to be an anchor that reports again the moment the standing text
changes. Neither holds once the quote leaves the search set: the rows below
print nothing, and a later edit to either standing sentence would be reported
by nobody. The two rows are still correct and still required by convention —
what is broken is that they are now also load-bearing in a way nobody
intended.

**It is not fixed here, and the surface is the diff side rather than the
corpus.** `corrected` has to skip a `survivors.md` the way `corpus` already
skips a `rounds/` record, which is `records_a_past_round` widened to a
second shape — a change to a gate CI reads, which is mechanism a fix pass
may not add (`skills/code-review/orchestration.md` §*A fix pass adds the
unit that pins it*). **#308** carries it, separate from #307, with the
mechanism and the surface corrected in its own comment. Excluding
`survivors.md` from `corpus` is the repair this note first named and it does
not work: measured, it moves the score by 0.001.

**Round 1's fix pass swept the CI range, `78d2c12..HEAD`, which is wider than
the `7ca5008..HEAD` the build swept.** The wider range reports two more
places, both below, and both are **shipped release notes**. Correcting them is
what this repository's own convention forbids: a released entry says what was
true at its release, and editing it to match a later change makes the history
lie about what shipped. #307 is open for the recurrence — the sweep reports
released notes as survivors every time a sentence they describe is later
changed — so the grounds are cited there rather than re-argued each round.

| Path | Quote | Grounds |
|---|---|---|
| `CHANGELOG.md` | `the span is taken from the last call to BEGIN, because the list is sorted by start` | **Shipped release note, true at its release.** It describes what 0.9.2's own change did and why: the old span rule is the thing that entry is explaining, so the sentence is a statement about the code as it stood then, not a claim about the tree now. #300 changed the rule afterwards, which is what the entry three sections down says. Correcting a released section would make it describe a repair that had not happened when it shipped. See #307 |
| `seal/specs/1788700685-two-value-shaped-odd-rows-end-the-report/changelog.md` | `the span is taken from the last call to BEGIN, because the list is sorted by start` | **The fragment the released section above was gathered from**, byte-identical to it by construction. It is another work item's shipped fragment, kept until its release folds it, and it is excused for the same reason and by the same grounds. Editing it would put the fragment and the released entry it produced out of step, which is the one thing the gather exists to keep true. See #307 |
| `seal/specs/1788926756-three-sentences-are-wrong-about-where-a-duration-is/spec.md` | `The disclosure in `skills/verify/SKILL.md` beside the span's own definition, because after item 3 the span means something a reader can state.` | The approved scope row, and it is exactly what was built: the disclosure sits beside the paragraph a reader meets before taking a reading, and the span now does mean something statable. What moved is `plan.md`'s phase-3 cell, which gained the ledger rows and the fragment count; the scope row itself needs no edit, and editing a scope row to match a plan cell would be the contract following the work rather than the reverse |
| `seal/specs/1788926756-three-sentences-are-wrong-about-where-a-duration-is/questions.md` | `Whether the disclosure sentence belongs beside the span's definition in `skills/verify/SKILL.md` or in the report's own output as well.` | Still open, and still the owner's — it is carried into `overview.md`'s `## Not verified` with the owner as its answerer. A question that has not been answered is not wording to correct, and deleting the row is what `unverified-check` exists to catch |
