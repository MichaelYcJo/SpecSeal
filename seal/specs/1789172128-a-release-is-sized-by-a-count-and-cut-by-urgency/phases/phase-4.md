# 1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | see `plan.md`'s Status cell for phase 4 |
| Ran by | unknown — the spawn prompt named no model, and the template gives this row to the spawning session rather than to the segment. The orchestrating session fills it |

## What this phase was asked

Plant the case that holds the sweep, asserting the new wording present and
*three or four is the size* absent, **seen red before phase 2's edit is
applied** — shown by reverting the sentence rather than by reasoning (§15).
Then handle S3's ledger row per Q8, and write this work item's own rows into
`seal/ledger/1789172128-….md` in one pass. Re-run `bin/evidence-check .` and
compare the exit code with phase 1's.

## What this phase found

**The case is `tests/test_a_release_is_sized_by_a_criterion.py`, seven units,
and every one of them has been seen red.** Five went red by reverting the
document to `6de3f54` — phase 1's commit, which is the tree before phase 2
touched `docs/` — and running the module: `5 failed, 2 passed`, exit 1. The
document was then restored from a copy taken before the revert, never with
`git checkout --`, and `git diff --stat` printed nothing.

The two that stayed green are the sweep and the sweep's own can-fail case, and
they stayed green correctly: with the old sentence restored the document is
still the one owner, and the pattern still matches it. So each was broken on its
own, one at a time, with a script that kept the file's bytes and asserted the
restore landed:

| Unit | Mutation | Exit |
|---|---|---|
| `test_one_document_states_a_releases_size` | a second statement of a release's size appended to `docs/release-checklist.md` | 1, naming that file and line |
| `test_the_sweep_can_fail` | `STATES_A_SIZE` replaced by a pattern no document carries | 1 |

After both restores the module is green again — 7 passed — and `git status`
showed only the new test file.

**`test_the_sweep_can_fail` exists because the sweep's value is entirely in its
pattern.** A regex that stops matching answers *no offender* for every file in
the tree and passes, which is `verify`'s counterfeit seal in one line. So the
pattern is run against the document that does state the rule, and the sweep is
allowed to report nothing only while that still matches.

**The sweep scans `.py` as well as `.md` and excludes only this module by
path.** Scanning one suffix was the cheap way past the self-match — the module
names the old wording in its own constants — and it would have left a comment
in any other test module free to state a second answer.

**Q8 is answered remove-and-rewrite, and the reading is the row's own text.**
S3 claimed *the rule that a release is sized in work items, three or four, is
stated in exactly one document*. The heading it was anchored to survives, so
the checker calls it DRIFTED rather than BROKEN — but the claim names the rule's
**wording**, and after phase 2 the tree does not state that rule. Re-verifying
would have left a row asserting a rule nothing says, and `--reverify` recomputes
a hash and cannot correct a claim. `CONTRIBUTING.md` §*Changing cited code is
the case the rule has to answer* gives exactly two answers and this is the
second one. So the row is removed from
`seal/ledger/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked.md`,
which now carries three rows, and its substance comes back as R1 of this work
item's fragment. Editing another work item's fragment is what Q8 flagged as
unsettled; both fragments already sit in `release/v0.11.1`, the fragment rule is
about two concurrent branches not queueing at one file, and the alternative was
folding a false row into `seal/ledger.md` at the release.

**The frame found one drifted row and there were two.** `bin/evidence-check .`
after phase 3 reported a second: `seal/ledger.md` cites
`docs/issues-and-milestones.md#"## A label answers *what it is about*, and
survives the move"` at `@993881ca` from **two** rows — G5 and S4 — and phase 3
edited that section. Neither claim went with the edit, so both were re-read and
re-verified rather than removed:

- **G5** holds that the rolling log's title format lives in this document
  rather than in the shipped skill. The label paragraphs are additions at the
  end of the section; the title format and the skill are untouched. The four
  cases the row names were re-run, exit 0.
- **S4** holds that the document states what the version check refuses — at or
  above the running one, below kept as history — and that **two** documents
  state that rule, not three. Phase 2's new paragraph names the same check, so
  this was the row worth opening: it says the two releases it cites *sit at or
  above the running version* and points down at this section as where the rule
  lives. It states no boundary of its own, which is the same deference
  `docs/release-checklist.md`'s row already makes, so the count is unchanged.

Both rows carry the re-read with the date and what was checked, and
`bin/evidence-check --reverify .` moved that one anchor from `@993881ca` to
`@a580e3ca`. It reported a line for every row it touched, including the
fragment's placeholder hashes, and named no BROKEN — which is the evidence that
each anchor resolves, since `--reverify` cannot invent one.

**S10's exit code moved from 0 to 1, and it is a warning by construction.**

| Ran | Exit | Reading |
|---|---|---|
| `bin/evidence-check .` (phase 1, before the edit) | 0 | `1137 ok · 0 drifted` |
| `bin/evidence-check .` (after phase 3, before the ledger work) | 1 | two DRIFTED anchors, both in the edited document |
| `bin/evidence-check --reverify .` | 0 | every touched row named, no BROKEN |
| `bin/evidence-check .` (after the ledger work) | 1 | ledger arm `1144 ok · 0 drifted · 0 broken`; the **records** arm reports one DRIFTED at `spec.md:159` |

The remaining exit 1 is the records arm, not the ledger: this work item's own
`spec.md` quotes S3's old stamp `@95e3a483` in §*The ledger row this edit
moves*, and that anchor's content is what phase 2 changed.
`skills/evidence-check/SKILL.md` §*The records arm* names this exact state —
*a live work item's branch is editing the very units its records stamp, so
failing on drift would be red by construction* — and `.github/workflows/test.yml`
turns exit 1 into a warning annotation and fails only at 2 or above. The
release that ships this work item folds the fragment away, at which point the
records arm stops reading it. `spec.md` is left as written: the stamp it quotes
is what the row said when the frame was drawn, which is what that sentence is
about.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| Row **S3** of `seal/ledger/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked.md` | **R1** of `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`, which carries the claim's surviving substance — one document owns what a release's size is decided by — and names the row it replaces |
