# 1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records — phase 4a

| Field | Value |
|---|---|
| Phase | 4a |
| Commit | 8c9c245 |
| Ran by | specseal:smith on fable-5.1 |

The `Ran by` value is transcribed the way phases 1 to 3's were: the agent is
the definition this segment was spawned from, and the model is what the
harness's own system prompt states. Neither half is the segment's idea of
what it is.

## What this phase was asked

Build phase 4a of `plan.md` and only phase 4a, on branch
`feat/161-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records`,
with routing answered and the question batch closed — ask nobody anything.
Phase 4b, a second smith after this one, does `docs/review-handoff-protocol.md`,
`agents/warden.md`, `agents/smith.md`, `skills/implement/SKILL.md` and
`docs/flow.md`; none of those was to be edited here.

The three files that OWN the rules, one carrier stating each rule and the
others linking to it in one sentence, keeping every measured incident:

1. `skills/code-review/SKILL.md` — §*a fix pass resumes the implementer*
   says the fix pass hands over a `## Fixes` table and `round_record.py
   close` applies it (rule 5, owner `agents/smith.md`, link); the *Nothing
   here runs away* and *Unless the verifying round reopens* paragraphs
   rewritten to the one reopening and the `capped` end, linking to the
   spec's subsection; rule 1 as its own paragraph, linking to the spec; rule
   2 owned here, the first level before the depth, with the measurement
   (round 4's fix pass on the last branch built a rule, a reader and two
   cases to close one 🟡, costing round 5's 🔴, #159 and half of round 6);
   the four reach-back sections naming `round_record.py new` and `close`
   with the rule and its grounds kept, and *forgetting it is silent* saying
   the reach-back is no longer a habit; 🟡 as a defect the release would
   ship and a new ⬜ line (rule 3, owner); a new subsection owning rules 6,
   7 and 9. Wrapped under 88 columns.
2. `docs/review-chain-spec.md` — the *Nothing here can loop … no third
   case* paragraph rewritten to the bound and linked to §*The reopening —
   one, and then the run is capped*, the sentence at `:104` kept; rule 1
   owned under §*The last round verifies* with the count (33 of 65 findings
   located in records, records 55 % of the diff); rule 8, the moratorium,
   under §*What the record carries*, plus one sentence that the record is
   written by `round_record.py` from the two agents' reports.
3. `templates/sdd-round.md` — the top comment says the record is generated
   by `new` and closed by `close`, the comments document fields a generated
   record does not carry, and the ordering rule is what the two subcommands
   produce; the *at most one more … Unless … Or whose verdicts* passage
   re-pointed at the spec's subsection, keeping the fact that the walk reads
   the verdict column; `deferred <home>` in the verdict vocabulary comment.
4. Pins: every changed sentence pinned, existing pins re-pointed and never
   deleted, every module reading the three files run before and after, each
   new pin seen red with its sentence stashed. New pins in
   `tests/test_the_rules_have_one_owner.py`: one case per rule that the owner
   states it and each link names the owner; one case that a walk over `docs
   skills agents templates` holds *at most one more round record* and
   *Unless th* to the owner and links, asserting on the three owned files
   and on a ceiling phase 4b can only lower.

Coordinates handed over and opened: `skills/code-review/SKILL.md` §§ at
`:218`, `:254-300`, `:303-337`, `:339`, `:375`, `:395`, `:420-437`, `:440`,
`:472`, `:549-560`; `docs/review-chain-spec.md:32-145`, `:1005-1078` and
`:814` (the reopening subsection); `templates/sdd-round.md` whole;
`round_record.py#main`'s argparse; `chain_check.py` `CAPPED_EXIT`,
`DEFERRED`, `REOPEN_FROM`; `phases/phase-3.md`. Every line number named
resolved to the section it was said to name at `c8adff3`.

## What this phase found

**The three owner files were also carriers of *the orchestrator writes the
record*, and 4b cannot reach them.** `plan.md` gives phase 4b the sweep for
that sentence, over the five linking carriers; five copies sat in this
phase's files — `skills/code-review/SKILL.md` §Cross-session records twice
(*the orchestrator writes three files*, *Copy it in right after posting*),
`docs/review-chain-spec.md` §What ran the round twice (*the orchestrator
writes that file*) and §When the record was written once. All five now say
the generator writes the record and the orchestrator runs it; the grep 4b
inherits for that sentence returns `agents/warden.md` alone.

**A pinned phrase read raw goes red at a line break.**
`test_skill_carries_the_copy_instruction` reads `skills/code-review/SKILL.md`
unflattened for *right after posting*, and the rewrite had wrapped the
phrase across a line. The instruction — WHEN the round paragraph is copied
in — is still a fact, so the sentence kept it on one line rather than the
pin being widened. `test_docs_line_wrap.py` is the other constraint on the
same file, so a phrase of three words has to fit where the wrap leaves it.

**The running version may not appear in prose that outlives it.**
*Measured on the last 0.8.0 branch* went red in `test_release_hygiene.py`;
the sentence names the issues instead (#153 and #150), which is also the
coordinate a reader can open.

**The `cannot loop` pin would have stayed green over a rewrite that made
it false.** Its needle, *Nothing here can loop*, is a prefix of the new
sentence *Nothing here can loop more than once*, so the old pin passed on
the new text unchanged. It is re-pointed at the longer phrase, at *the run
ends `capped`*, and at the absence of *There is no third case to run away*,
and the insertion of that last sentence is one of the forty mutations.

**Rule 5's owner phrase lives in a file this phase did not edit.** The pin
file reads `agents/smith.md` for *hands over a fix table under `## Fixes`*
(phase 2's sentence) as the owner of rule 5, and the skill's link names
`agents/smith.md`. Phase 4b edits that file and has to keep the phrase.

**The count-rule ceilings after this phase are 4 and 0.** *at most one more
round record* stands in `docs/review-handoff-protocol.md:314`,
`docs/review-chain-spec.md:104`, the skill and the template — the owner and
three links, of which the protocol's is 4b's to keep or lower. *Unless th*
stands nowhere in `docs`, `skills`, `agents` or `templates`.

**Left as ⬜, not fixed.** `templates/sdd-round.md`'s severity comment under
the verdicts table still reads *🟡 needs grounds · 🟢 matches* with no ⬜;
the skill owns rule 3 and a generated record carries no comment, so the line
reads short rather than wrong, and it was not touched.

**Seen red, and how.** Every new pin was red with its sentence stashed: 36
stashes and 4 insertions (the *habit* sentence, a second *at most one more
round record*, an *Unless the* in the template, *There is no third case to
run away* in the spec), 40 mutations, 0 alive, each restored from bytes kept
in the loop and `tests/__pycache__` cleared between. The 23 modules reading
the three files passed before the edits (932); after them one failed
(`0.8.0` in prose, fixed) and after the pins one more (the raw-read *right
after posting*, fixed); the five modules reading the last edit passed (136).
Every unit this phase added is a test case; no code unit was added.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The unbounded exception, stated twice — `skills/code-review/SKILL.md` §The cap is a ceiling *Unless the verifying round reopens the run* and `templates/sdd-round.md` *Unless that verifying round reopens the run* | `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* (phase 3), which both files now link to |
| *There is no third case to run away* and *Nothing here runs away* — the claim that the verifying round cannot loop, in the spec and the skill | the same subsection; the spec's paragraph now states the bound and names the third case |
| *The habit that makes all of it moot is one pass over the three cells with the fix diff open* — the reach-back as something to remember | `round_record.py new` (the checker cell) and `close` (the two surface rows), named in the same paragraph |
| *🟡 fix or justify — divergence with grounds; quote the grounds, confirm intent*, the threshold-less definition | the same line, now *a defect the release would ship*, with ⬜ beneath it |
