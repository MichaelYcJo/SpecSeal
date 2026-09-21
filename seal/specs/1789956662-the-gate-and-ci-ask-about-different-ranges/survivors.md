# the gate and CI ask about different ranges — excused survivors

<!-- Read by `survivor-check --exempt`. The QUOTE is the anchor, so an
exemption stops applying the moment that text changes, and an excused survivor
is still printed with its grounds. There is no value meaning "check nothing". -->

**As of `d656f4be`, none of the three rows below fires in this working tree**,
and the check is exit 0 over both the branch range and round 1's fix range
with no `--exempt` at all. Each row fired when it was written and stopped
firing when a later correction in the same pass moved the wording the match
rested on. They are kept rather than deleted for two reasons, and a reader who
disagrees with either should delete the row rather than leave it unexplained:

- **CI judges a different tree.** `actions/checkout` on a `pull_request` event
  checks out the merge of the head into the base, and these runs were taken
  over the working tree. A pair that falls below the floor here can clear it
  there.
- **A quote is an anchor, not a licence.** Each row stops applying the moment
  its standing text changes, so a row that excuses nothing costs nothing and
  cannot quietly excuse something else later.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789956662-the-gate-and-ci-ask-about-different-ranges/phases/phase-4.md` | `**The workflow's side is read as arguments, not as text.**` | This work item's own phase 4 record, quoting verbatim what that phase recorded before round 1's finding 4 measured the reader as too narrow. It is a past state kept on purpose: a record that quietly becomes true is a record nobody can audit. The rendered prose above the quotation states what the reader does now, so nothing false renders, and the quotation sits inside the correction that explains it. **The checker's pool already excludes a work item's `rounds/` records** — a record quoting a defective sentence is not a place that still instructs anybody — and a `phases/` record is the same kind of thing and is not excluded. Widening `records_a_past_round` is mechanism a fix pass may not add, so it is a follow-up and this row is the answer meanwhile |
| `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/overview.md` | `The two divergences above are corrections to measurements the frame carried, not clauses this work added.` | Another work item's closing memo, merged and shipped. What this range removed is **this** work item's `## Fed back into the spec`, which read `none — the divergences above are corrections to \"spec.md\"'s grounds rather than clauses this work added` until round 1's finding 8 replaced it with the two corrected clauses named. Two closing memos reached a near-identical sentence independently, because the section asks every work item the same question and `none` has one natural phrasing — so the match is the shape of the template rather than a copy anybody left behind. The standing sentence is true about the work item it belongs to, its `Fed back into the spec` section is correct as it stands, and a branch repairing the gate's base resolution has no business editing a shipped memo of a different work item to lower a similarity score |
| `skills/code-review/scripts/chain_check.py` | `merge_base = git(root, "merge-base", base, "HEAD")` | The removed wording is `broad_gate.py`'s old `base = git(root, "rev-parse", "--short", …)` followed by `if base is None:`, replaced by a call to the resolver. What the sweep matched is two phrases of PYTHON — `base git root` and `base is none` — which survive normalisation from any `git(root, …)` call assigned to something called `base` and guarded for `None`. The standing text is a different function asking git a different question in `chain_check.changed_paths`, and it carries no claim about how `broad-gate` resolves its base. Correcting it would mean renaming an unrelated local variable to make a sentence-similarity score go down. **Round 1's fix pass rewrote `resolve_base`, and the pair no longer scores above the floor in this working tree** — the row is kept rather than deleted because CI checks out the merge of the head into the base, which is a different tree from this one, and because the quote is the anchor: it stops applying the moment the standing text changes |
