# round 1's fix pass — the table `round_record.py close` applies

Range: `a0f0e9a..941dab5`. Two commits; the round record they answer is
`rounds/round-1.md`. Spelled parent-of-first-fix to last, because `a..b`
excludes `a` and `ea4fc64..` would drop the first fix commit from the diff
`close` measures.

**The pass was the builder's session resumed, not a fresh spawn** — the session
that wrote the branch still existed, and `skills/code-review/orchestration.md`
§*a fix pass resumes the implementer* makes that the rule rather than the
preference.

Finding 8 takes no row: the reviewer closed it `answered` in the report, on
grounds stronger than the phase's — S3 was **removed** rather than re-pointed,
so a current stamp would leave a row that no longer exists quoting current
content.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `ea4fc64`, `docs/issues-and-milestones.md:148-155`. Verified by the orchestrating session at all three coordinates before the round recorded it, and re-read after: the sentence said the label comes off *at the same moment* `merged: X.Y.Z` goes on, while `:209-210` puts that label at a push to `release/*` under a heading that says **before the release ships**, and `docs/branch-and-release.md:251-258` says the two moments are deliberately different. It now anchors on the later one the document already owns — *when the release that carried the ticket has gone out — the moment `main` moves and the issue closes* — followed by **Not when `merged: X.Y.Z` goes on**, which names the section that puts that a release earlier and the reason: that label answers *is this in yet*, where this one is spent only once the work is out. The fix is a sentence about two moments rather than a corrected moment, which is what stops the same conflation returning |
| 2 | fixed | `ea4fc64`. The sweep and its control read through a new `hits()` that searches each line, and each line joined to the next with the wrap collapsed — skipping the joined check where the next line matches alone, so a wrapped sentence is reported once at the line it starts on. **Re-derived by the orchestrating session rather than inherited**, and my first attempt was wrong: `hits()` takes a list of lines, and passing a string iterates characters and answers `[]`. Called correctly — a sentence wrapped across two lines is `[]` to a plain line scan and `[1]` to `hits()`; a whole-line statement reports once; two adjacent matching lines produce no double report. The module docstring no longer claims `flat()` for everything and says which reader each half uses, which is the half of finding 2 that was a false statement rather than a gap |
| 3 | fixed | `ea4fc64`. `STATES_A_SIZE` gained `release(?:'s)?\s+size`, `size\s+of\s+a\s+release` and `is\s+the\s+size` — the tokens Q6's wider recipe already carried and the planted pattern had dropped. **Measured by the orchestrating session, the same three shapes that escaped before:** `A release's size is three or four work items.`, `Three or four work items is the size of a release.` and `The size of a release is three work items.` are now all **caught**, and so is the sentence this branch replaced. The constant records that `\bis\s+the\s+size\b` can misfire on a sentence about the size of anything, and that nothing in the scanned set matches it today outside the two excluded files — a disclosure at the coordinate rather than a silent widening |
| 4 | fixed | `ea4fc64`. The label paragraph now says what two states mean for the argument it makes: the subject never carries a second value, so a spent label is removed whole rather than re-valued. This is the clause `spec.md` expected as an exception and the build had argued was unnecessary; it lands as an argument rather than a carve-out |
| 5 | fixed | `941dab5`. The false execution claim, and the one that mattered most because the row folds into `seal/ledger.md` at the release. R1 said `git grep -n "is the size"` exits 1 after the edit; it exits **0**. Confirmed by the orchestrating session both unscoped and scoped to exactly the set the row names, and again after the fix: `git grep -c` reports four hits, all inside `tests/test_a_release_is_sized_by_a_criterion.py`, the module the same phase planted. The row now records what the command answers and which reading was recorded as permanent. `phases/phase-2.md` keeps its `1` — true when taken — and gains the clause naming the commit from which it stops being true, which is the right treatment for a phase record rather than a rewrite |
| 6 | fixed | `941dab5`. `phases/phase-4.md` and `questions.md` Q8 said the `1789100139` fragment is now three rows; it is two — S1 and S5b. The third was the table header, counted by `grep -c "^| "` |
| 7 | fixed | `941dab5`. #351's `changelog.md:22` is **marked rather than excused**, which is what the round decided after measuring half the original exemption away: `CHANGELOG.md`'s top section is still the previous release, the `1789100139` fragment is ungathered, and `gather_changelog.py` concatenates in work-item id order, so that fragment lands above this one and the released section would state the replaced sentence in the present tense before correcting it far below. The bullet now says that wording is what this work moved and not what the document says today, pointing at the entry that replaces it. `survivors.md`'s row quotes the marking clause, so the exemption dies the moment the marking changes, and it records that the original second ground was withdrawn on the reviewer's measurement. The memo's matching `## Not verified` row is closed rather than deleted. **Round 2 corrected the anchor**: a marking clause is a later sentence than the candidate it marks, so that spelling exempts nothing, and the row is anchored on the surviving sentence instead |
| 9 | fixed | `941dab5`. `CLAUDE.md` added to `SCANNED`, with the reason — `tests/test_one_word_one_meaning.py:39`, the module this sweep was modelled on, reads it. 170 files scanned, no offender. Reach rather than a live defect, and closed because the gap was in the model it copied |

## What was run over the fix range

Executed by the fix pass, exit codes read directly with no pipe: `uvx ruff
check` and `uvx ruff format --check` on the module (0 each); five modules
narrowly (77 passed); a probe over the three noun forms, the replaced sentence,
a wrapped restatement, a double-report case and `tracked()`;
`git grep -n "is the size"` over R1's own file set; `bin/evidence-check .`
before, `--reverify`, and after; `bin/unverified-check` on the memo (3 open ·
1 closed); `bin/survivor-check` over `7e17f5e..HEAD`; and seven further record
modules (328 passed).

**The `survivor-check` exit 0 in both paragraphs of this record measures
nothing, and round 2's finding 3 is why.** `corrected` counts a review report's
verbatim quotation of the defective wording as wording the range wrote, so from
`a0f0e9a` — the commit that posts round 1's own record — the check stops
reporting the survivor it had reported at `b46ff77`. Re-measured at `95b3d83`
with `--exempt` and without it: exit 0 and the identical *no removed wording is
still standing* both times. Neither reading below is evidence that anything was
excused, and `survivors.md`'s four rows are consulted by nothing until **#365**
lands.

**Re-run by the orchestrating session at `941dab5`**, because a hand-back's
verification claim is a claim: eight modules one per call — the new module 7,
wrap 23, release-hygiene 32, one-word-one-meaning 13, no-real-identifiers 2,
row-points-by-content 102, record-states-the-tree 58, the-work-item-set 16 —
**exit 0 each**; `uvx ruff check` and `uvx ruff format --check` on the module,
**exit 0** each; `bin/survivor-check --range 7e17f5e..HEAD --exempt <survivors.md>`
**exit 0**; `bin/evidence-check .` **exit 1**, ledger arm **1144 ok · 0 drifted
· 0 broken**, records arm one drift at `spec.md:159` which round 1 decided
stays. The regex and `hits()` were exercised directly, and the finding-1
sentence read against the two coordinates it had contradicted.

**One unit added: `hits()`, depth 1.** The module it sits in was created by
build phase 4 rather than by an earlier round's fix pass, so this is *a fix
pass may add a unit* and not the refused depth-2 case. No case was added to pin
findings 2 or 3 — both were closed by correcting the unit, and the corrected
unit is measured by the probe rather than by a new test.

**Not run: the broad gate.** `agent-contract` §2 assigns it to the sealer,
once, after the rounds settle.
