# three checks that do not see what they are named for — questions for the planner

<!-- seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Nothing here blocks the build, and that is a finding rather than an
omission.** Three questions survived the reading, one settled by running a
command and two by the phase that meets them. No row is a person's, because
every judgment the three tickets left open was already answered somewhere in
the tree.

**What the tree answered, so nobody reopens it:**

- **Whether these are three repairs or one** — `spec.md` §*One shape, three
  modules* answers it, on the ground #418 itself states for its own phrase
  set.
- **Whether this work item repairs the two cells of another work item's round
  record** — Q1 of work item `1789455558-…` answers it, by construction: the
  fourth work item cut from `release/v0.12.0` after `fix/401-402-…` merged,
  which also carries #413. Both clauses describe this branch, and Q1 refused
  the other two homes with grounds. Asking again would ask a person to repeat
  an answer they have already given.
- **Whether `agents/smith.md` and `agents/scribe.md` join the wrap test's
  covered list** — `seal/follow-up.md` holds it as an open row for the
  repository owner. This work corrects a documented number and does not touch
  the list, so it neither answers that row nor needs it answered.
- **Whether either paste-ready patch is adopted verbatim** —
  `plan.md`'s Alternatives table answers both, with the failure scenario that
  changed each one.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does keeping the *user* stem, anchored at both ends, refuse any sentence that stands in `agents/*.md` today? The issue's patch drops the stem; `plan.md` keeps it, because the anchor is what stops the plural and because the user is precisely the party who answers | **a measurement** — the module run over the definitions as they stand, which is phase 3's own command | **keep** — the guard still refuses a definition that tells an agent to collect what the user answers, and a false refusal has to be shown before the stem is dropped; **drop** — the guard goes quiet on that wording, for a plural the anchor already handles | **keep**. No batch phrase in any definition is within the window of any occurrence of the word today, so keeping it refuses nothing that stands. If phase 3 measures otherwise, the row is what records the reversal | ⬜ |
| Q2 | The one ledger row anchored on the guard phases 3 and 4 change claims the check decides by what a sentence claims rather than by the phrase it uses. Phase 4 is what makes the second half of that true. Is the row corrected in place, or removed and re-written in this work item's own fragment? | **the work** — phase 6 reads the row against what phases 3 and 4 shipped and decides there | **correct in place** — the anchor is untouched and the claim's subject is the same unit, which is the criterion `seal/ledger.md` S13 already states; **supersede** — a new row here and the old one removed, which `CLAUDE.md` reserves for a row whose anchor a change removes | **correct in place**, with the Checked date of the phase that re-read it. Nothing removes the anchor, so the case for superseding has to be made rather than assumed | ⬜ |
| Q3 | After the search phrases become constants, should the seam-safety case also assert that the two sweep cases actually read them? Without it, a later session can write a phrase inline and the set silently stops covering it — this work's own failure, one level up | **the work** — phase 2 finds out whether it is reachable without re-implementing the sweep | **assert it** — closes the six-month failure `plan.md` names; **leave it** — the member assertion beside it still goes red whenever the set of folded members moves, which is the other half of the same hole | **leave it**, and write the risk down beside the constants. An assertion that has to read the case bodies to know what they search for is the derivation #418 refuses, so it is only worth having if phase 2 finds a shape that is not one | ✅ **leave it** — phase 2, `9d90db85`+1. The two reachable shapes are both refused: recognising a search inside a case body is the derivation #418's *Not this* rules out, and counting each phrase in this module's own source is noise, because `the seal` stands in comments, two docstrings and the seam fixtures. The risk is written beside `SEAL_BARE`, naming the folded-member assertion as the other half's cover |
