# 1790260566-a-row-inside-a-fence-reads-as-live — round 3 report

Target SHA `6c538abc`. This is the verifying round and the last one: round 2
closed on a fix and spent the reopening. Its target is round 2's fix diff,
`ff112c0d..e8fbe7b9`, one commit. I also read `ff112c0d` itself, because
round 2's ⬜ 3 was answered there as a record correction. I worked in a
`git clone --no-local` of the worktree at the target SHA, under this round's
scratch directory, and wrote nothing in the worktree except this file.

## How the pieces relate

1. Round 2 left three notes and no yellow. Two were fixed at `e8fbe7b9`, a
   stale comment and a missing case. The third was a sentence in a ledger
   note, corrected at `ff112c0d`.
2. All three are closed. The new case is the one unit the fix created, and
   it is correct: it fails with the half of `fenced_after` it pins removed,
   and only then.
3. The ledger edits the fix made keep every claim true, and the checkers
   agree. Nothing this round found needs a fix.

## Round 2's verdicts, one by one

**⬜ 1, `repoint`'s comment: closed.** Round 2 found the line-count comment
naming `follow`, a helper the round 1 fix removed. At
`hooks/root-migrate.py:435` the comment now says a mismatch "would be a
defect in the splice above", and the splice it means is the loop at
`hooks/root-migrate.py:421`. No `def follow` and no call to one remains in the
file. The only other `follow` in the neighbouring tests is git's `--follow`
option at `tests/test_the_root_migrates_itself.py:186`, which is unrelated.
The change is a comment, so the code is byte-identical apart from it (read).

**⬜ 2, the opener half of `fenced_after` had no case: closed.** Round 2
found that deleting the backtick-info opener rule left the whole
record-generator module green. The new case,
`tests/test_the_record_is_generated.py:2014`, feeds the paste-ready section a
line of three backticks followed by `x` and a backtick, then prose, then a
real fenced block. By CommonMark §4.5, which the docstring cites correctly, a
backtick fence's info string may not hold a backtick, so the first line opens
nothing and the prose must not reach the record.

I checked that the case pins what it claims (executed). With the opener
condition reduced to a bare match, the new case failed and the round 1 case
passed. With the closer's empty-info condition removed instead, the round 1
case failed and the new case passed. Each case goes red for its own half and
no other. The failing assertion under the opener mutation is the second one,
because the mutated walk still copies the real block and additionally copies
the prose (read, from the walk). The file was restored and the clone's status
was clean afterwards.

**⬜ 3, the merge note on D1 and E1: closed.** Round 2 found the note saying
one unit carries both sides' edits. At `ff112c0d` both notes in
`seal/releases/0.15.1.md` (D1 at line 70, E1 at line 92) now say each anchored
unit is one side's: the House rules section this branch's, the
evidence-ledger section the release side's. Each carries a
`Corrected 2026-09-25` marker. I checked the claim against the merge's parents
(executed, `git diff -U0` from the merge base `c52e8350` to each parent):

- This branch's only hunk in `CONTRIBUTING.md` is at base line 298, inside
  `## House rules` (base lines 198–335). Its hunk in
  `docs/the-evidence-ledger.md` is at base line 300, in the fold section, not
  the anchored one.
- The release side changed nothing in `CONTRIBUTING.md`. Its first hunk in
  `docs/the-evidence-ledger.md` is at base line 71, inside
  `## A row is a content anchor, and it names no commit` (base lines 15–75).
  Its other two hunks are at 192 and 205, past that section.

So the corrected sentence is true, and this was paperwork, as round 2 said.

## The unit the fix created

`test_a_backtick_line_whose_info_holds_a_backtick_opens_no_fix` is the one new
unit (`New units`, depth 1). Judged as code:

- It uses the module's own helpers, `declared`, `report(fixes=…)`,
  `generate` and `paste_ready`, the same way its sibling at line 1995 does.
- It asserts the exit code, that the real block arrives whole, and that the
  prose does not. The first two do not discriminate the mutation; the third
  does. That is the right shape for a pin whose failure mode is extra text.
- It passes at the target (executed).

I found nothing wrong with it.

## The ledger edits the fix made

- **R1-1** gained the new case as a second anchor, `@b1918daf`, and a sentence
  saying the case was seen red with that half removed. My mutation reproduces
  the sentence. `fenced_after`'s own hash, `f091142c`, is unchanged, which is
  right because `round_record.py` is not in the fix diff.
- **R1-2** and **S8** move `repoint`'s hash from `c621a8f5` to `6b3bfe22`, the
  comment edit. S8 is a row in the shared release file `seal/releases/0.4.0.md`
  and carries a dated `Re-read` note naming the comment, as `CLAUDE.md` asks of
  an edited existing row. R1-2 is this work item's own fragment row, created on
  this branch, and was re-stamped without a note. That is within the fragment
  convention, and the release-hygiene module passes over it (executed).
- **0.13.1's section row** anchors a heading in `seal/releases/0.4.0.md`
  whose section moved only by S8's note. It was re-stamped to `45e1cac9` with a
  dated `Re-read` note saying so. The claim, that no row gained an anchor into a
  retired `spec.md`, still holds; evidence-check reports 0 broken.

`evidence-check` reports 2,158 ok, 0 drifted, 0 broken, and the records arm
0 refused. `correction-check` over `5e3aab5c..6c538abc` finds no merge in the
range, so there is nothing a merge could have dropped.

## The broad gate

Nobody has run the full suite, lint or typecheck on this branch. That is
correct, and it is not this round's to run. With this round leaving nothing
open, the gate has come due: the next step is the sealer's spawn.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's note 1 is closed — `repoint`'s line-count comment names the splice, not the removed `follow` | `hooks/root-migrate.py:435` | confirmed | read: the comment names the splice at line 421, no `follow` helper remains, and nothing but the comment changed |
| 🟢 | round 2's note 2 is closed — the opener half of `fenced_after` has its case | `tests/test_the_record_is_generated.py:2014` | confirmed | executed: green at the target; red with the opener half removed, green with the closer half removed; the round 1 case is red only for the closer half |
| 🟢 | round 2's note 3 is closed — the D1 and E1 merge note says which side edited which anchored unit | `seal/releases/0.15.1.md` | confirmed | executed: per-parent hunks from `c52e8350` put this branch's only House rules hunk at line 298 and the release side's only anchored evidence-ledger hunk at line 71; a record correction, corrected at ff112c0d |
| 🟢 | The new unit is correct — the case pins the backtick-info opener rule and nothing else | `tests/test_the_record_is_generated.py:2014` | verified | read and executed: CommonMark §4.5 is cited correctly; the discriminating assertion is the prose one |
| 🟢 | The fix's ledger edits keep every claim true | `seal/ledger/1790260566-a-row-inside-a-fence-reads-as-live.md` | verified | executed: evidence-check 0 drifted, 0 broken; release-hygiene module green; S8 and 0.13.1's section row carry dated re-read notes |
| ❓ | Behaviour on Linux and Windows | the fix diff | ❓ out of verified scope | macOS only here; CI's matrix answers it at the pull request |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the new case and round 1's case at `6c538abc` | 2 passed, exit 0 |
| The same two cases with `fenced_after`'s opener condition reduced to a bare match, in the clone | exit 1: the new case failed, round 1's case passed |
| The same two cases with the closer's empty-info condition removed instead | exit 1: round 1's case failed, the new case passed; file restored, clone status clean |
| `bin/test` over `test_the_record_is_generated`, `test_release_hygiene` and `test_the_root_migrates_itself` at `6c538abc` | 222 passed, exit 0 |
| `bin/evidence-check .` at `6c538abc` | exit 0; 2,158 ok, 0 drifted, 0 broken; records arm 525 names, 0 refused |
| `bin/correction-check --range 5e3aab5c..6c538abc` | exit 0; no merge commit in the range |
| `git diff -U0` from `c52e8350` to each parent of `32fb90bd`, over `CONTRIBUTING.md` and `docs/the-evidence-ledger.md` | this branch: House rules line 298 and the fold section line 300; release side: the content-anchor section line 71 and two hunks past it |
| The broad gate (full suite, lint, typecheck) | not yet: nobody has run it. It belongs to the sealer, and with this round it has come due |

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened this round, all in the clone at `6c538abc` unless noted:

- `hooks/root-migrate.py` (lines 400–450)
- `skills/code-review/scripts/round_record.py` (lines 1285–1360)
- `skills/evidence-check/scripts/evidence_check.py` (lines 170–215)
- `tests/test_the_record_is_generated.py` (lines 154–200, 1966–1980, and the new case's hunk)
- `seal/ledger/1790260566-a-row-inside-a-fence-reads-as-live.md`, `seal/releases/0.4.0.md`, `seal/releases/0.13.1.md`, `seal/releases/0.15.1.md` (the rows the fix diff and `ff112c0d` touch)
- `bin/test`
- `seal/specs/1790260566-a-row-inside-a-fence-reads-as-live/rounds/round-2.md` and `round-2-report.md` (in the worktree)
