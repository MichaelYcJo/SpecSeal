# Round 2 report — 1790263216-the-older-statements-name-what-enforces-them (#565)

| Field | Value |
|---|---|
| Round | 2, the verifying round |
| Target SHA | da07ecbd |
| Range reviewed | `7e9bf98f..c231af28` (round 1's fixes, 2 commits), plus the merges f52abbe1 and da07ecbd |
| Where it was read | a `git clone --no-local` of the worktree at da07ecbd, under the round's scratch directory |
| Reviewed by | specseal:warden on Opus 5.5 |

## What this round was asked, and where it looked

This round answers round 1's eight verdicts, checks the four new targets
against their rules, and reads the two merges. It stayed inside the fix
range. It widened in one place only: each target was also run against a
reword of the statement's own bold opening, because the question was
whether each target goes red when its rule is broken.

The orchestrator's account was read in full and treated as claims. That
covers the prompt, the commit messages of 6826f53f, c231af28 and f52abbe1,
and the closed `round-1.md`. Each claim below says what it asserted and what
the tree showed.

## Round 1's verdicts

**Findings 1 to 4: each line now names a case that reads its rule, and each
case goes red when the rule's instruction is broken.** This was executed one
mutation at a time, with the file restored from its kept bytes after each run
and the clean tree run first (20 passed):

| Decision | Instruction reworded | Target | Statement's own bold opening reworded |
|---|---|---|---|
| D6 | `CONTRIBUTING.md`, then `CLAUDE.md`: *resolve it hunk by hunk and read both sides* | red both times | green |
| D13 | `skills/settle/SKILL.md`: *A fold opens no directory under `seal/specs/`* | first target red | second target red: it asserts the policy's opening verbatim |
| D14 | `skills/settle/SKILL.md`: *retire the case* | red | green |
| D32 | the contract's §15: *before it is committed as a case* | red, 1 of 16 | green |

The right-hand column is an observation, not a finding. For D6, D14 and D32,
nothing in `tests/` reads the owner document's own sentence. The only reader
of each rule is the pin on the text a session acts on: the two guides for
D6, the settle skill for D14, and the contract's §15 for D32. D32's statement
names §15 as the rule's home. `spec.md` §*What a decision is* gives the pin on
that text as the right target for this kind of rule, and round 1 chose these
same targets. So the lines are right. A future edit that rewords only the
owner's sentence would still pass every case, and the ❓ row below carries
that together with the decisions no round has opened.

**Finding 5: D33's line is now honest.** It says `nothing — no case reads the
opening yet` and says what would read it, which is case 4's form. The only
place in `tests/` that mentions *Three and five count rounds* is the rule-13
comment at `tests/test_the_rules_have_one_owner.py:230`. That comment says
the phrase is **not** pinned there. `fold-check` reads the line and exits 0.

**Finding 6: the release checklist now names only `Target SHA`.** Both §0's
never-rebase item and the merge sentence in the release PR step now say that.
A sweep of `docs`, `skills`, `agents`, `templates`, `hooks`, `CONTRIBUTING.md`
and the READMEs for *rider* near *SHA* or *commit* found three kinds of hit,
and none of them says a stamp names a commit. They are D89's own correction,
`templates/sdd-round.md`'s history of the old stamp, and a dated past-tense
record at `docs/branch-and-release.md:126`. `survivor-check` over the PR
range, `58629718...da07ecbd`, exits 0. Over the fix range alone it exits 1
and names two places. Neither is a rider sentence. One is another
statement's `Enforced by:` line that correctly shares D33's former targets
(`docs/review-chain-spec.md:519`). The other is the spec's own template
example (`spec.md:201`). CI reads the PR range.

**Finding 7 (answered) stands.** D90's *A third reader* is still a dated
measurement. Its claim about the plugin directory is untouched by the fix
range. The overview's *Not done* names it at lines 51 to 55.

**Finding 8 is closed.** Phase 2 now says that the seven skips are D21's
target parametrised. Phase 1's D6 row now carries a correction that
withdraws *allowed to fail*. No workflow carries `continue-on-error`: grep
exits 1.

**The counts moved with the fixes.** `grep -rn 'Enforced by: nothing' docs/`
returns 9 lines: 4 of case 1, 0 of case 2, 2 of case 3 and 3 of case 4, as
the overview, Q2 and the changelog fragment now say. 106 and 9 add up to the
115.

## The two merges

**f52abbe1 kept every note as a union, and every row it re-stamped carries a
note.** A probe replayed the three-way merge. The base is e9dfe623, this
branch's side is 1d0262d7, and #587's side is 6e850fb1. For every ledger row
that the two sides left different, the probe checked each `Re-read`,
`Corrected` or `Re-verified` segment that either side added or both kept
against the result. It found none missing, across 37 rows in 14 files.

The commit message's classification matches the probe. F6, D1, E1, E2, G5,
R4 and S4 were edited by both sides. Each of the seven carries one new dated
note written at the merge. F5 and C2 took #587's side and C1 took this side.
X1 in #588's fragment and S9 in 0.11.1 were not in the conflict list, and
each also gained a merge note. X1's note goes with a hash that matches
neither side (`40fa761a`). No row changed at the merge without either side
having edited it.

In the one conflicted document hunk, only this branch had changed the
paragraph's prose. #587's change was the `Enforced by:` line below it, and
both sides wrote that line identically. So taking this side lost nothing.

`correction-check --range 7e9bf98f..da07ecbd` examined three merges and found
no dropped marker. `evidence-check .` at da07ecbd reports 2115 ok, 0 drifted
and 0 broken.

**da07ecbd's `-s ours` dropped nothing.** Its tree is byte-identical to
f52abbe1's tree. The release tip it records, 58629718, has a tree identical
to 6e850fb1, which is #587's final tip and which f52abbe1 had already merged.
Every file where 58629718 differs from f52abbe1 is one this work item
touched, except #588's fragment. That fragment differs only by X1's merge
note and re-stamp.

## A correction to this run's paperwork

**⬜ 1: four phase rows still record the decision that round 1's fixes
replaced, and D6's row alone says so.** Look at `phases/phase-1.md:51`
(D13), `:52` (D14), `phases/phase-2.md:39` (D32) and `phases/phase-3.md:22`
(D33). Each row's catching-unit cell still reads what the fix pass changed.
c231af28 gave D6's row a *Corrected in round 1's fix pass* note, so a reader
comparing phase rows with documents will find D6 annotated and these four
silent. The overview's *Not done* does name all five moves. This is a record
correction and is left out of `Needs a fix`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | Four phase rows (D13, D14, D32, D33) still state the decision round 1's fixes replaced, and only D6's row carries a correction note | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/phases/phase-1.md:51` | open | read; also `phase-1.md:52`, `phase-2.md:39`, `phase-3.md:22`; a correction to the run's paperwork, the overview's *Not done* already names the moves |
| 🟢 | round 1's finding 1 is closed — D6 names the pin on its instruction | `docs/the-evidence-ledger.md:153` | confirmed | executed: the target red with CONTRIBUTING.md's instruction reworded and red with CLAUDE.md's; read: no `continue-on-error` in any workflow; the owner's own opening reworded leaves it green, and nothing in `tests/` reads that sentence |
| 🟢 | round 1's finding 2 is closed — D13 names two pins | `docs/the-evidence-ledger.md:346` | confirmed | executed: the first target red with the settle skill's sentence reworded; the second red with the policy's own bold opening reworded |
| 🟢 | round 1's finding 3 is closed — D14 names the pin on settle's three answers | `docs/the-evidence-ledger.md:359` | confirmed | executed: red with *retire the case* reworded; the owner's opening reworded leaves it green |
| 🟢 | round 1's finding 4 is closed — D32 names the contract's §15 pin | `docs/round-record-spec.md:941` | confirmed | executed: red 1 of 16 with §15's phrase reworded; the statement names §15 as the rule's home; its own opening reworded leaves it green |
| 🟢 | round 1's finding 5 is closed — D33 says no case reads its opening | `docs/review-chain-spec.md:112` | confirmed | read: the one mention in `tests/` is the rule-13 comment saying the phrase is not pinned; executed: `fold-check` exit 0 |
| 🟢 | round 1's finding 6 is closed — the checklist names `Target SHA` alone | `docs/release-checklist.md:29` | confirmed | read: also line 260; the class sweep finds no sentence saying a stamp names a commit; executed: `survivor-check` over the PR range exit 0 |
| 🟢 | round 1's finding 7 stays answered | `docs/branch-and-release.md:146` | confirmed | read: the fix range does not touch D90, and the overview's *Not done* carries it |
| 🟢 | round 1's finding 8 is closed — both phase records corrected | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/phases/phase-2.md:82` | confirmed | read at c231af28; phase 1's D6 row withdraws *allowed to fail* |
| 🟢 | f52abbe1 kept every note as a union, and every re-stamped row carries a dated note | `seal/releases/0.15.1.md` | verified | executed: the probe found 0 missing notes over 37 rows; `correction-check` 0 dropped over 3 merges; `evidence-check` 2115 ok, 0 drifted |
| 🟢 | da07ecbd's `-s ours` dropped nothing from the release branch | da07ecbd | verified | executed: its tree equals f52abbe1's; 58629718's tree equals 6e850fb1's, which f52abbe1 merged |
| 🟢 | the fix pass's four re-stamps (S9, C1, C3, E2) each carry a dated note | `seal/releases/0.13.1.md` | confirmed | read in 6826f53f; also `0.11.1.md` and `0.15.1.md`; executed: `evidence-check` 0 drifted |
| 🟢 | the counts moved with the fixes: 9 `nothing` lines, 4/0/2/3 | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/overview.md:28` | confirmed | executed: the grep returns 9, split as stated |
| ❓ | Whether the read decisions no round has opened catch their breaking edits, including owner statements whose only reader is a guide's or skill's copy (as D6, D14 and D32 are) | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/phases/` | ❓ out of verified scope | carried from round 1; a verifying round stays in the fix range; the orchestrator decides whether a later work item takes it |

## Paste-ready fixes

### ⬜ 1

```
 **Corrected in round 1's fix pass:** the line now names `test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row` and `test_the_skill_says_what_a_fold_does_to_the_ledger`, the pins on the rule's instruction and on the policy's own opening.
```
```
 **Corrected in round 1's fix pass:** the line now names `test_the_skill_names_the_floors_a_fold_has_to_answer`, the pin on settle's three answers.
```
```
 **Corrected in round 1's fix pass:** the line now names `test_each_section_holds_its_rule`, the pin on the contract's §15.
```
```
 **Corrected in round 1's fix pass:** rule 13 pins the statement's third bold sentence and not its opening, so the line now says `nothing — no case reads the opening yet`.
```

Each sentence is appended to the catching-unit cell of the D13, D14, D32 and
D33 rows respectively.

## Executed probes

| What was run | Result |
|---|---|
| clean run of the five node ids the four fixed lines name | exit 0, 20 passed |
| D6: CONTRIBUTING.md's, then CLAUDE.md's *resolve it hunk by hunk and read both sides* reworded | red each time (1 failed) |
| D6: the policy's bold opening reworded to *take the newer side* | green (1 passed): no case reads the owner's sentence |
| D13: the settle skill's *A fold opens no directory* reworded | 1 failed, 1 passed |
| D13: the policy's *A fold is not a work item, and it adds nothing to the ledger.* reworded | 1 failed, 1 passed |
| D14: the settle skill's *retire the case* reworded | 1 failed |
| D14: the policy's bold opening reworded to *lowered until the run passes* | green (1 passed) |
| D32: the contract's §15 *before it is committed as a case* reworded | 1 failed, 15 passed |
| D32: the statement's bold opening reworded | green (16 passed) |
| tree state after every restore | clean |
| notes-union probe over f52abbe1 (base e9dfe623, sides 1d0262d7 and 6e850fb1) | exit 0; 0 missing notes; 7 rows edited by both sides, each with one new merge note; no row changed only at the merge |
| `git merge-tree --write-tree 1d0262d7 6e850fb1` | 6 conflicted files, as the commit message says |
| `git diff f52abbe1 da07ecbd`, `git diff 6e850fb1 58629718` | both empty |
| `bin/correction-check --range 7e9bf98f..da07ecbd` | exit 0; 3 merges, no correction marker dropped |
| `bin/evidence-check .` at da07ecbd | exit 0; 2115 ok, 0 drifted, 0 broken |
| `bin/fold-check` at da07ecbd | exit 0; 136 statements read, cutoff 0 binds 136; 14 documents under 1000 lines |
| `bin/survivor-check --range 58629718...da07ecbd` | exit 0; 88 removed sentences, none standing |
| `bin/survivor-check --range 7e9bf98f..c231af28` | exit 1; 2 places, neither a rider sentence: the ownership statement's line and the spec's template example |
| `bin/test` over the folded-statement, room, editions, merge-correction and one-owner modules | exit 0, 184 passed |
| `bin/test tests/test_release_hygiene.py -k "ledger or row or reading or overwide"` | exit 0, 6 passed |
| `grep -rn 'Enforced by: nothing' docs/` | 9 lines |
| the broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

Both probe files, named with the `test_tmp_` prefix, were deleted before the
hand-over, and so was the clone.

Nothing this round found needs a fix. Only ⬜ 1 is still open. It is
paperwork, and `docs/review-chain-spec.md` §*A finding located in a record is
a correction, not a round* says it owes no fix pass and no reader. It closes
`answered`, with `corrected at <sha>` or the grounds for leaving it in the
cell beside. `round_record.py new` was run as a dry run on this report
inside the clone, and it leaves `Pass` unchecked until that close. Once
`Pass` is checked, the broad gate is due. The next step is then spawning
the sealer, not a run the orchestrating session puts together itself.

Needs a fix: no
Loses a record or crashes: no

## Proof block

Opened in this round: `seal/specs/1790263216-the-older-statements-name-what-enforces-them/rounds/round-1.md`,
`round-1-report.md` (header), `spec.md` (§*What a decision is* and the
scenarios), `overview.md` (*Not done*), `phases/phase-1.md`, `phase-2.md` and
`phase-3.md` (the D6, D13, D14, D32 and D33 rows), `survivors.md`; the diffs of
6826f53f, c231af28 and f52abbe1, and da07ecbd's tree against f52abbe1;
`docs/the-evidence-ledger.md` (lines 120 to 212 and 320 to 356),
`docs/round-record-spec.md` (lines 915 to 942), `docs/review-chain-spec.md`
(lines 70 to 112 and 505 to 519), `docs/branch-and-release.md` (lines 120 to
160), `templates/sdd-round.md` (lines 68 to 80);
`tests/test_a_merge_cannot_silently_drop_a_correction.py` (lines 711 to 800),
`tests/test_settle_reads_before_it_removes.py` (lines 910 to 966),
`tests/test_the_agent_contract_holds_the_universal_rules.py` (the §15 pin and
the parametrised case), `tests/test_the_rules_have_one_owner.py` (lines 222
to 240), `tests/test_the_release_tail_does_not_end_at_the_tag.py` (lines 180
to 196), `.github/workflows/hygiene.yml` (the survivor and correction legs),
and `bin/test`.
