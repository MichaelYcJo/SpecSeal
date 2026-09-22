# 1790076060-the-cap-is-read-as-bounding-fixes-and-the-pile-is-nobodys — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 4b34b1b7 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

#492's rule, written into the document that owns the cap. Four things, all in
`docs/review-chain-spec.md`: that the cap bounds rounds and not the fixes of
the round it stopped; that a run the round cap stopped may write a fix; the
ownership test in the words *who owns the unit now*, with `New units` named as
where the evidence already sits and *when did the defect start* named as the
substitution that was made; and the reopening section's exit sentence
corrected so that `no fixes to check` is said of the record that wrote no
fixes rather than of every capped record, with the two exits named apart.

Two constraints came with it and they are constraints on the prose rather than
things to change: the phrase *at most one more round record* is at its ceiling
of four across the tree, so no new paragraph may repeat it; and the four swept
files may not contain the substring `Unless th`.

## What this phase found

**The frame holds.** Every coordinate `plan.md`'s Technical context table
names was opened and each was where it said, allowing for line drift from the
frame commit. The two facts the handoff said not to re-derive were opened
anyway, per §5, and both are as stated: `rounds/round-6.md` of
`1790039346-settle-reads-a-marker-inside-a-commented-out-draft` is a capped
record whose `Fixes checked by` reads `round-7` over five findings closed on
fixes, and `round-7.md` is the reader, `Fixes checked by: no fixes to check`,
`Broad gate | 5e2ede92 against 3cdfd8ad`. So the shape the new sentence
permits is a shape that already shipped green.

**The leftovers table is not where the section map said it was.** `plan.md`
puts the homes table under §*The review run has a bound, and an end*, which is
true of the `##` section and hides that the table sits inside the `###`
subsection *The last round verifies, and what it verifies is a diff* — which
two ledger rows are anchored on (`seal/ledger.md` lines 2171 and 2196). Phase
3 rewrites that table into the ladder, so the drift lands on those rows rather
than on a heading nothing cites. Recorded here because phase 3 has to read it
before it edits, not after.

**Where the new subsection went, and why it is a subsection.** The rule sits
between the cap's own prose and §*The bound has a floor*, as `### The cap
bounds rounds, and not the fixes of the round it stopped`. A heading rather
than four more paragraphs, because the carriers of phase 2 have to name it:
`tests/test_the_rules_have_one_owner.py`'s link shape is a sentence naming the
owner's **subsection**, and a rule with no heading cannot be linked that way.

**The permission is stated once and refused once, in the same document.** The
new subsection carries the permission and the reopening subsection carries a
paragraph saying the permission is not its. That is deliberate duplication of
the *subject* and not of the rule: the reopening paragraph states what its own
terminal record may not do and names the other subsection as the owner of what
it may. Written the other way round — one sentence covering both exits —
the document would name a state `chain_check.py`'s reopening walk refuses,
which is #341.

**The measured instance names a work item directory and no version.**
`tests/test_release_hygiene.py` refuses a loaded document naming the running
version or above; a `seal/specs/<id>/` path carries a unix second and no
version, so the citation is safe where `0.13.1` would not be.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase added two passages and altered no existing sentence. The reopening subsection's exit paragraph is unchanged; what followed it is new | none |
