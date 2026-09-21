# the census and the tie that nothing holds — excused survivors

<!-- Read by `survivor-check --exempt`. The QUOTE is the anchor, so an
exemption stops applying the moment that text changes, and an excused survivor
is still printed with its grounds. There is no value meaning "check nothing". -->

`survivor-check` fired five times over this range and three of the five were
correct as defects, not merely as reports: row C2 of `seal/ledger.md`, the
`123 rows` figure in row C4, and the spelling census in work item 1789969379's
`spec.md` were all live statements of the class this work item exists to
close, and none of them appears in round 3's list of six. They were corrected
rather than excused, which is why only two rows stand here. That is Q5's real
answer: the check earned its run.

The two below survive for opposite reasons — one because a person has to
decide whether it may be touched at all, and one because the sentence is still
true and was never the thing the range corrected.

**Both rows are dormant at the branch tip and are kept deliberately.** They
fired at `57c31e7`, and the last commit of the range — which corrected a
seventh site of the same class — changed the set of removed sentences enough
that neither scores above the threshold any more. The rows stay because what
they excuse has not gone away: the released `CHANGELOG.md` §0.12.2 still
carries the false figure while the fragment beside it does not, which is Q1
and is disclosed in `overview.md` §*Not verified* and in `seal/follow-up.md`.
Each row is anchored on a quote, so it stops applying the moment that text
changes, and a dormant row excuses nothing it should not.

| Path | Quote | Grounds |
|---|---|---|
| `CHANGELOG.md` | `Counted in this repository: 404 marker occurrences on 190 rows, at least three spellings` | The released §0.12.2 section, and it is **Q1** — the repository owner's, still ⬜. `CONTRIBUTING.md` §*House rules* says one branch edits `CHANGELOG.md` and it is the one based on `main`, which this branch is not. The work item's changelog fragment beside it **is** corrected, so the two copies now diverge; `gather_changelog.py` decides by marker and never by content, so a corrected fragment is never re-gathered and nothing downstream can see the divergence. That is disclosed in `overview.md` §*Not verified* and carried in `seal/follow-up.md` rather than repaired here. The same answer governs work item 1789996775's Q1 about a different sentence in the same released section |
| `seal/specs/1789969379-a-conflict-resolved-by-side-reverts-the-other-sides-corrections/spec.md` | `One row, `R4 · the printed bound reads BOTH of the gate's walks …`, carries no other spelling, so it was invisible to the check entirely.` | The sentence is still true and it is not what the range corrected. **Measured at this branch's tip**, walking every row and keeping those whose every marker site carries a qualifier: exactly one row qualifies and it is R4. What moved in `correction_check.py` was the precision of the same fact — *carries no other spelling* became *carries a qualifier on every marker it has and no bare spelling at all* — because the shorter form can be read as *carries only one spelling of the qualifier*, which is a different claim. A past-state record stating the true version of a fact is not a survivor of the correction to a different sentence's wording, and rewording it here would edit a shipped record to quiet a checker |
