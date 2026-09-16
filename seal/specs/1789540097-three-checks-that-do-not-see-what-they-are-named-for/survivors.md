# 1789540097-three-checks-that-do-not-see-what-they-are-named-for — survivors

<!-- Places `survivor-check` reported as still carrying wording this range
removed, and which are judged correct to leave standing. Each row quotes the
STANDING text, so the exemption stops holding as soon as that text changes.
Run: `bin/survivor-check --range 27a2d403..HEAD --exempt <this file>`. -->

All three are records rather than instructions, and all three now carry the
correction beside the standing text rather than instead of it. That is the
distinction this file is for: a record asserts a PAST state, which is what
lets one sit beside a contract at all.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/phases/phase-3.md` | `**The repair was itself held by nothing, and that is the shape this work item exists to repair.**` | The paragraph is phase 3's own finding, and it was true when it was written — hoisting the patterns is why the phase added a unit `plan.md` does not name. Round 1's 🔴 1 showed the repair incomplete rather than wrong, and **the correction is appended in the same section**, naming the round and the fix. Rewriting the paragraph would delete the reasoning that produced the defect, which is the one thing a phase record exists to keep |
| `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/plan.md` | `**No mutation, because nothing in the tree reads a docstring** — planting a reader is new mechanism aimed at the file `seal/follow-up.md` already holds open for the owner` | Round 1's 🟡 5 is right that this reason does not hold — the follow-up row is about a different act. `plan.md` is the **framer's** document and its Verified-by cells are the design the gate approved; a fix pass does not rewrite an approved contract after the fact, because doing so erases what was actually approved. The reason that is true is written in `phases/phase-6.md` §*What this phase found* and in `overview.md` §*Not done*, both naming 🟡 5. If the orchestrator wants the plan itself amended, that is a decision above this pass |
| `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/overview.md` | `**#422's window still crosses headings, and that is deliberate.**` | **A false positive of the similarity matcher.** The two phrases it shares with the removed phase-6 text — *md out rules*, *out with grounds* — are both halves of the sentence *`spec.md` §\*Out\* rules it out with grounds*, which two unrelated paragraphs cite because they cite the same section. This paragraph is about the 140-character window crossing headings; the removed text was about pinning a docstring number. Nothing here is a leftover |
