# 1791384160-a-fix-range-is-its-own-commits-across-a-merge — phase 7

| Field | Value |
|---|---|
| Phase | 7 |
| Commit | 9345fe9b |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 7, the records. Restate in the owner's terms:

- the ledger rows `Corrected · S1, S5, S8, S10` and `Corrected · S2, S3, S4,
  S6` (round 3's ⬜ 4);
- the `S7, S8, S9` row and both `S12` rows.

Re-read `changelog.md` against the owner sentence, and edit it only where it
states an example by shape or by time. Update `overview.md`'s divergence row
for the reframe and its *Not verified*, and `phases/phase-1.md`'s round 2
correction. Drop `survivors.md`'s two rows for the removed `spec.md` sentence,
and excuse any new survivor of the reframe's range. Run `evidence-check
--reverify --into` for the anchors phase 6 moved (S18).

## What this phase found

**Three more ledger rows needed the same restatement.** The plan named five.
The S9 row described its cases by history ("a topic merged into the
branch"), and the S1–S3 row described its case by whose unit it was. Both now
describe the cases in terms of what `own_commits` lists. The S6 row and the
`Corrected · A1` row were already in the owner's terms, so they are left as
they stand.

**The changelog stated three things by shape and none by the rule.** Its
first bullet said "a sibling's squash on a base that never merged the start
is left out". Its second bullet's title said the notice names the item's own
commits "whichever way a merge was made", which shape D on CI's merge ref
makes false. Its second bullet also ended "a topic branch merged in after the
build is now read too". The first bullet now states the owner sentence and
links the home. The second now says what the notice reads, including the CI
input, as the fragment section says it.

**Q3 is closed.** Round 1's record read PR #878's Windows shards on git
2.55.0.windows.5: no failure among the changed modules, and no skip on S10.
The overview's row is marked closed with that reading. The *Not verified*
section now holds one open row, the sealer's.

**`survivor-check` over the reframe's range, `a15c4057..HEAD`, named 14
places.** Two were derived claims in test comments: rule 17's account of
#860, and the S6 assertion's comment. Both are reworded, and that commit is
9345fe9b. The other twelve are now rows in `survivors.md`: released rows, the
framer's `spec.md` and `plan.md`, the guard's own quotation, S7's account of
the removed walk, other rules' comments, and `.test_durations`. Over the
whole branch, `origin/release/v0.21.0...HEAD`, the check exits 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `survivors.md`'s two rows for `spec.md:71` and `spec.md:191` | none: the reframe removed the sentence the first one excused, and the second shared only "descends from" with it |
| the overview's divergence row *where a sibling's commit sits* | the row *how the rule is stated*, which names the reframe |
| phase 1's two corrections by shape | one correction naming the owner sentence and the shape module |
