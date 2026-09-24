# Review round 3 — `fix/547-the-fold-writes-each-release-to-its-own-file`

Target SHA `ccf9ee26`, base `release/v0.15.1` at `6b912e66`. This is the
last round of the run. Round 2 opened two 🟡 and spent the one reopening, so
this round verifies round 2's fix range `0dad7d21..3f5e9d75` and nothing
else: `94e6d6cd` (the orchestrator's owner-authorized `CLAUDE.md` edit),
`b1af1403` and `3f5e9d75` (the smith's). `ccf9ee26` only closes round 2's
record. I worked in a `git clone --no-local` of the worktree at the target,
and every probe ran in that clone or in `git archive` copies of it.

Round 2's eight findings are closed at their coordinates. One new finding is
in the sentence the fix for round 2's 🟡 2 wrote. The comparison that
sentence gives the release session can be taken in no step of the sequence it
sits in. The "before" count has no place before `--split`. The "after" command
globs `seal/ledger/*.md`, and the fold has already emptied that directory by
§3, so zsh refuses the glob and the count prints `0`. The failure is loud,
not silent, and nothing is lost. But the release that reads this sentence is
0.15.1, the one release that runs `--split`.

## Round 2's fixes, checked against the code

**🟡 1 — `CLAUDE.md` names the release files (read).** The instead-of table
row (`CLAUDE.md:134`) and the removal rule (`CLAUDE.md:138-142`) now say
`seal/ledger.md` or a `seal/releases/<X.Y.Z>.md`. I read them against the twin
in `CONTRIBUTING.md:196-213`, which says the same. *`CONTRIBUTING.md` carries
the same sentence* is true again. Row C8 (`seal/ledger.md:2368`) is
re-stamped, and `evidence_check.py --strict .` reads it OK.

**🟡 2 — a command prints the comparison (executed).** The checklist now
gives two `grep -c '^|'` commands in place of a count no command printed. I
ran both on an archive of `ccf9ee26`. Before `--split` the first printed
`1027`. After the split the second printed `1027`, in bash and in zsh alike.
So the closure holds: the comparison exists and its two numbers are equal.
Where the sentence places that comparison is this round's 🟡 1.

**⬜ 3 — a line in more than one place is named (executed).** With the
script from `94e6d6cd` (b1af1403's parent) swapped into the clone, both new
cases fail. `test_a_line_the_standing_area_also_holds_is_named_not_moved`
fails because the split rewrote the anchor to `seal/releases/0.2.0.md`
instead of naming it.
`test_a_line_two_moved_sections_and_the_standing_area_hold_is_named` fails
because nothing was named: the anchor was kept in silence. Both pass at the
target. The real-tree dry run at the target is byte-identical to the one
from the parent script (`cmp` exit 0), and it names nothing it cannot place.

I also checked the class the fix belongs to. `rewrite_self_anchors` reads a
heading anchor's first part through the same `moved` and `kept` maps as a
line anchor, and `split` fills both maps with every non-blank line, headings
included. So a heading that stands both in the standing area and in a moved
section falls into the same `both` set and is named too. That is read, not
executed.

**⬜ 4 — the escaped quote is pinned (executed).**
`test_the_split_reads_an_escaped_quote_the_way_the_checker_does` passes with
the parent script. That is expected, because it pins `63fbfa52`'s fix and not
`b1af1403`'s. So I showed it red two other ways. A mutant that drops the
`\\"` alternative from the locator group of `SELF_ANCHOR_RE` turns it red (and
the module with it). The script from `63fbfa52^` turns it red too, on
*could not place*, with the locator cut at `wrote, \"`.

**⬜ 5, ⬜ 6, ⬜ 7 (read).** Both conflict headings (`CLAUDE.md:147`,
`CONTRIBUTING.md:225`) name a fragment two stacked branches both edited.
`test_a8_both_rule_documents_say_what_to_do_at_the_conflict` passed in the
module run. The two test docstrings are in the past tense or name the
release file. The three long lines are wrapped.

**⬜ 8 (carried).** This range does not touch `templates/seal-README.md`,
so round 2's answer stands as it was written.

## The ledger sentences in `CLAUDE.md` and `CONTRIBUTING.md`, read once more

I read every sentence about the ledger in `CLAUDE.md:101-192` and in
`CONTRIBUTING.md:44-120` and `:192-270`. Each sentence that says where rows
stand, where a branch must not append, what a removal touches, or what
conflicts now names the release files beside `seal/ledger.md`. The checker
sentence names all three globs. One heading still speaks of a single file:
`CLAUDE.md:123`, *a change writes fragments, never the shared file*. The rule
under it still holds for the release files, so it reads badly and says
nothing false. That is ⬜ 2, and it is the owner's heading. Row C8 anchors on
it, so renaming it also means re-anchoring that row.

## The comparison the checklist gives cannot be taken where it stands

`docs/release-checklist.md:150-160` sits in §3, *Verify before committing*.
By then §2 has already run `--split` and then `--version X.Y.Z` in one
block. The sentence asks for two readings taken **before** the split: that
`evidence_check.py --strict .` exits 0, and a table-line count. §2's command
block has no step that takes either one. A session following the checklist
in order first meets the request after the tree it describes is gone. It can
recover the numbers from `HEAD`, but the checklist does not say so.

The "after" half fails differently. At §3 the fold has removed every
fragment. The paragraph's own first sentence says this is *the first time
`seal/ledger/` is empty*. On the archive, after `--split` and then
`--version 0.15.1`:

- bash: `cat` warns that `seal/ledger/*.md` does not exist, and the count
  still prints `1027`.
- zsh: `no matches found: seal/ledger/*.md`, `cat` never runs, and
  `grep -c` prints `0` with exit 1.

The step-2 block uses `sed -i ''`, so the release runs on macOS, where zsh is
the default shell. The Bash tool in this harness is zsh as well. A release
session that takes the reading as written sees `0` against `1027`. It stops,
which is the safe direction. Nothing ships wrong. But the comparison written
to confirm that every row landed in one file cannot confirm it.

A command with no glob gives the same count in every state and in both
shells. `find seal/ledger.md seal/releases seal/ledger -name '*.md' -exec cat
{} + 2>/dev/null | grep -c '^|'` printed `1027` before the split and `1027`
after the split and the fold, in bash and in zsh. The fold keeps the table
lines too: the fragments' rows moved into `seal/releases/0.15.1.md`, and the
count did not change. So one command, run in §2 before `--split` and again in
§3, is the whole comparison.

This paragraph was written by this run, at `3f5e9d75`, inside the fix range.
`docs/review-chain-spec.md` §*The cap bounds rounds, and not the fixes of the
round it stopped* says a finding in a unit the run's own fixes created
belongs to the branch whatever round it surfaced in. The spec also says a
document's ownership is read from the fix range, not from `New units`. The
prompt asked me to defer, so the verdict row names a home. Whether the rule
makes this the branch's fix instead is the orchestrator's call.

## Regression tests to plant

None for 🟡 1: the defect is in prose a shell runs, and no case in this
repository executes the checklist's commands. If one is wanted, the
destination is `tests/test_release_hygiene.py`. The case would run the
checklist's count command under `zsh -c` on a copy with `seal/ledger/`
absent and assert that it prints the pre-split number.

## Facts for the evidence ledger

- The table-line count across every ledger file is conserved by `--split`
  and then `--version 0.15.1` on an archive of `ccf9ee26`: 1027 before, after
  the split, and after the fold. The `ok` total runs 1736, then 1932, then
  1929, with 0 drifted and 0 broken each time (executed). It belongs in row P2
  of this work item's fragment if the orchestrator wants the fold half on
  record. Today P2 records the split half only.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | §3's table-line comparison cannot be taken as written. The before-count and the before `--strict` run have no step before §2's `--split`. At §3 the after-command globs `seal/ledger/*.md`, which the fold has emptied, so zsh refuses the glob and `grep -c` prints `0` | `docs/release-checklist.md:155` | open | executed — archive of `ccf9ee26`, split then fold: zsh prints `no matches found` and `0` (exit 1), bash prints `1027` with a `cat` warning; the proposed `find` form prints `1027` in every state in both shells; the paragraph was written at `3f5e9d75`, so §*The cap bounds rounds* may make it the branch's; the answerer is the orchestrator |
| ⬜ 2 | The heading of `CLAUDE.md`'s fragment rule still says *the shared file* while its table and removal rule now cover the release files too | `CLAUDE.md:123` | deferred the owner | read — the rule under the heading holds for the release files, so nothing is false; renaming it re-anchors row C8; `CLAUDE.md` is the owner's |
| 🟢 | round 2's should-fix finding 1 is closed — `CLAUDE.md`'s table and removal rule name `seal/releases/<X.Y.Z>.md` | `CLAUDE.md:134`, `CLAUDE.md:139` | verified | read — against `CONTRIBUTING.md:196-213`; C8 re-stamped and OK under `--strict` |
| 🟢 | round 2's should-fix finding 2 is closed — a command prints the comparison, and the two numbers are equal | `docs/release-checklist.md:155` | verified | executed — `1027` before and `1027` after `--split`, bash and zsh; where the sentence places it is 🟡 1 |
| 🟢 | round 2's ⬜ 3 is closed — a line in more than one place is named, not moved or kept | `.github/scripts/fold_ledger.py#split` | verified | executed — both new cases red with `94e6d6cd`'s script and green at the target; the real-tree dry run is byte-identical and names nothing; the heading form of the class goes through the same maps (read) |
| 🟢 | round 2's ⬜ 4 is closed — the escaped quote is pinned | `tests/test_the_ledger_fragments_fold_at_release.py#test_the_split_reads_an_escaped_quote_the_way_the_checker_does` | verified | executed — red on the mutant dropping the `\\"` alternative and on `63fbfa52^`'s script; green on `94e6d6cd`'s, which is expected |
| 🟢 | round 2's ⬜ 5, ⬜ 6 and ⬜ 7 are closed — the conflict headings name a fragment, two docstrings, three wraps | `CLAUDE.md:147`, `CONTRIBUTING.md:225` | verified | read; `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` passed in the module run |
| carried | round 2's ⬜ 8 stays answered — the shipped template names no repository's release files by design | `templates/seal-README.md:79` | answered | carried from round 2; this range does not touch the template |
| 🟢 | The split and then the fold on a copy of the real ledger at the target: every row in exactly one file, 0 drifted and 0 broken | `.github/scripts/fold_ledger.py#split` | verified | executed — 1027 table lines in all three states; `--strict` exit 0 in all three |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_ledger_fragments_fold_at_release.py`, `tests/test_a_merge_cannot_silently_drop_a_correction.py`, `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` and `tests/test_release_hygiene.py`, in the clone at `ccf9ee26` | `240 passed`, and exit 0 on a second run read directly |
| The three new cases at the target | exit 0 |
| The three new cases with `fold_ledger.py` from `94e6d6cd` checked out into the clone, then restored | `2 failed, 1 passed`: the two ⬜ 3 cases fail on their named-anchor assertions; the escaped-quote case passes |
| The escaped-quote case with the `\\"` alternative removed from the first group of `SELF_ANCHOR_RE` (a substitution asserted to match once), then restored | the case exits 1, and so does the module |
| The escaped-quote case with `fold_ledger.py` from `63fbfa52^`, then restored | fails on *could not place*, locator cut at `wrote, \"` |
| `git status --short` in the clone after each restore | empty |
| Archive of `ccf9ee26`: `cat seal/ledger.md seal/ledger/*.md \| grep -c '^\|'` in bash and in zsh | `1027`, `1027` |
| `evidence_check.py --strict .` before the split | exit 0, `1736 ok · 0 drifted · 0 broken` |
| `fold_ledger.py --split` | exit 0, 29 sections, 2 rewrites at `seal/releases/0.13.1.md:66`, no *could not place* |
| `cat seal/ledger.md seal/releases/*.md seal/ledger/*.md \| grep -c '^\|'` after the split, bash and zsh | `1027`, `1027` |
| `evidence_check.py --strict .` after the split | exit 0, `1932 ok · 0 drifted · 0 broken` |
| `fold_ledger.py --version 0.15.1` after the split | exit 0, two fragments folded into `seal/releases/0.15.1.md`, `seal/ledger/` gone |
| The same after-command after the fold | bash: a `cat` warning and `1027`; zsh: `no matches found: seal/ledger/*.md` and `0`, exit 1 |
| `evidence_check.py --strict .` after the fold | exit 0, `1929 ok · 0 drifted · 0 broken` |
| `find seal/ledger.md seal/releases seal/ledger -name '*.md' -exec cat {} + 2>/dev/null \| grep -c '^\|'`, before the split and after split and fold, bash and zsh | `1027` in all four |
| `fold_ledger.py --split --dry-run` on two archives of `ccf9ee26`, one with the target script and one with `94e6d6cd`'s | both exit 0; `cmp` exit 0 |
| `evidence-check --strict .` in the clone with this report copied in | exit 0; `1736 ok · 0 drifted · 0 broken`; records arm `340 names read · 0 refused · 0 drifted` (332 before the report); no line needed `NAME NOT IN TREE` |
| The broad gate — the full suite, repository-wide lint and typecheck | not yet — the sealer's, after the rounds settle; not taken in this round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 2 — the fragment rule's heading says *the shared file* | the owner's `CLAUDE.md` | the owner |

## Paste-ready fixes

### 🟡 1 — `docs/release-checklist.md`, step 2's second block

```bash
python3 .github/scripts/gather_changelog.py --version X.Y.Z
# At the release that splits: the two readings §3 compares against, before --split.
find seal/ledger.md seal/releases seal/ledger -name '*.md' -exec cat {} + 2>/dev/null | grep -c '^|'
python3 skills/evidence-check/scripts/evidence_check.py --strict . >/dev/null 2>&1; echo $?
python3 .github/scripts/fold_ledger.py --split              # see below
python3 .github/scripts/fold_ledger.py --version X.Y.Z
sed -i '' 's/"version": "A.B.C"/"version": "X.Y.Z"/' .claude-plugin/plugin.json
```

### 🟡 1 — `docs/release-checklist.md` §3, replacing the sentences from `evidence_check.py --strict .` through *every row in exactly one file.*

```markdown
green; `evidence_check.py --strict .` exits 0 here as it did in step 2
before the split, with no drifted and no broken row. Its `ok` total rises,
because the checker counts a `(coordinate, hash)` pair once per file and the
split puts pairs two releases shared into two files, so the total is not the
comparison. The table lines are:
`find seal/ledger.md seal/releases seal/ledger -name '*.md' -exec cat {} + 2>/dev/null | grep -c '^|'`
prints here the number it printed in step 2 before the split, which is every
row in exactly one file, the fold's included. It names no glob, so no shell
refuses it once the fold has emptied `seal/ledger/`.
```


**Orchestrator's note on 🟡 1's verdict, 2026-09-24.** The reviewer wrote `deferred` because the spawn prompt said to defer anything this last round opened. That instruction contradicted `docs/review-chain-spec.md` §*The cap bounds rounds, and not the fixes of the round it stopped*: the paragraph at `docs/release-checklist.md:155` was written inside this run's own fix range (3f5e9d75), so the branch owns it and fixes it whatever round it surfaced in, and one verifying round reads the fix. The verdict is therefore `open`; the reviewer's own text above already named that section as the question.

Needs a fix: yes — 🟡 1 (the release checklist's before-and-after table-line comparison has no step before the split and misfires in zsh after the fold)
Loses a record or crashes: no

## Proof block

Files opened this round, at `ccf9ee26` unless named:

- `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/rounds/round-2.md`
- `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/rounds/round-2-report.md` (head and headings)
- `git diff 0dad7d21..3f5e9d75` over `CLAUDE.md`, `CONTRIBUTING.md`, `docs/release-checklist.md`, `.github/scripts/fold_ledger.py`, `.github/workflows/hygiene.yml`, `skills/evidence-check/scripts/correction_check.py`, `seal/ledger.md`, `seal/ledger/1790208593-the-fold-writes-each-release-to-its-own-file.md`, `tests/test_the_ledger_fragments_fold_at_release.py`, `tests/test_a_merge_cannot_silently_drop_a_correction.py`, `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`
- `.github/scripts/fold_ledger.py:468-471` and `:495-640`
- `CLAUDE.md:99-195`
- `CONTRIBUTING.md:40-120` and `:185-272`
- `docs/release-checklist.md:66-170`
- `docs/review-chain-spec.md:63-90`
- `seal/ledger/1790208593-the-fold-writes-each-release-to-its-own-file.md`, rows P2 and D1
- `seal/ledger.md:2368` (row C8)
- `bin/test`
- `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/rounds/round-1.md`, its verdict rows only

Round 1's report was not re-opened. Its coordinates reached this round
through round 2's record, and this range touches none of round 1's closures.
