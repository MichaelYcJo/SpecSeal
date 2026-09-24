# 1790208593-the-fold-writes-each-release-to-its-own-file — review round 3

| Field | Value |
|---|---|
| Target SHA | ccf9ee2659ec5dfb2453c8dd68d13c86ce993c1a |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | 558 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (the release checklist's before-and-after table-line comparison has no step before the split and misfires in zsh after the fold) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 3, the last round of the run — round 2 opened two 🟡 and spent the one reopening — reviewed at ccf9ee26: round 2's fix range `0dad7d21..3f5e9d75`, the orchestrator's `CLAUDE.md` edit under the owner's authorization and the smith's two commits. It asked whether the checklist's two table-line commands give equal counts before and after `--split` on a copy of the tree, whether the three new cases are red with the fixes' parent scripts, and whether any `CLAUDE.md` or `CONTRIBUTING.md` sentence still names one ledger file where the release files now hold rows. Its spawn prompt said to defer anything it opened; see the orchestrator's note in the report on why its one 🟡 is open instead.

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

## Paste-ready fixes

```bash
python3 .github/scripts/gather_changelog.py --version X.Y.Z
# At the release that splits: the two readings §3 compares against, before --split.
find seal/ledger.md seal/releases seal/ledger -name '*.md' -exec cat {} + 2>/dev/null | grep -c '^|'
python3 skills/evidence-check/scripts/evidence_check.py --strict . >/dev/null 2>&1; echo $?
python3 .github/scripts/fold_ledger.py --split              # see below
python3 .github/scripts/fold_ledger.py --version X.Y.Z
sed -i '' 's/"version": "A.B.C"/"version": "X.Y.Z"/' .claude-plugin/plugin.json
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/fold_ledger.py:460` | round 1's 🟡 1 — fixed |
| round-1 | `docs/release-checklist.md:152` | round 1's 🟡 2 — fixed |
| round-1 | `.github/scripts/fold_ledger.py:18` | round 1's 🟡 3 — fixed |
| round-1 | `docs/the-evidence-ledger.md:108` | round 1's 🟡 4 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:4` | round 1's 🟡 5 — fixed |
| round-1 | `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/overview.md:47` | round 1's ⬜ 6 — answered |
| round-1 | `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/changelog.md:8` | round 1's ⬜ 7 — answered |
| round-1 | `docs/review-chain-spec.md:1423` | round 1's ⬜ 8 — fixed |
| round-1 | `.github/scripts/fold_ledger.py:574` | round 1's ⬜ 9 — fixed |
| round-1 | `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/phases/phase-2.md` | round 1's ⬜ 10 — answered |
| round-1 | `.github/scripts/fold_ledger.py#split` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/fold_ledger.py` | round 1's 🟢 — confirmed |
| round-2 | `CLAUDE.md:139` (and `:134`) | round 2's 🟡 1 — fixed |
| round-2 | `.github/scripts/fold_ledger.py:579` | round 2's ⬜ 3 — fixed |
| round-2 | `tests/test_the_ledger_fragments_fold_at_release.py:842` | round 2's ⬜ 4 — fixed |
| round-2 | `CLAUDE.md:146` (and `CONTRIBUTING.md:225`) | round 2's ⬜ 5 — fixed |
| round-2 | `tests/test_a_merge_cannot_silently_drop_a_correction.py:1135` (and `tests/test_the_record_is_held_to_the_floor_and_the_depth.py:504`) | round 2's ⬜ 6 — fixed |
| round-2 | `.github/workflows/hygiene.yml:123` (and `CLAUDE.md:147`, `skills/evidence-check/scripts/correction_check.py:238`) | round 2's ⬜ 7 — fixed |
| round-2 | `templates/seal-README.md:79` | round 2's ⬜ 8 — answered |
| round-2 | `docs/release-checklist.md:152`, `.github/scripts/fold_ledger.py:19` | round 2's 🟢 — verified |
| round-2 | `docs/the-evidence-ledger.md:109` | round 2's 🟢 — verified |
| round-2 | `docs/review-chain-spec.md:1424`, `.github/scripts/fold_ledger.py:592` | round 2's 🟢 — verified |
| round-2 | `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/overview.md` | round 2's 🟢 — verified |
| round-2 | `CLAUDE.md:176`, `templates/seal-README.md:79` | round 2's 🟢 — verified |
| round-2 | `seal/ledger.md`, `seal/ledger/1790206437-a-second-fold-writes-a-second-heading.md`, `.github/scripts/fold_ledger.py:59` | round 2's 🟢 — verified |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 2 — the fragment rule's heading says *the shared file* | the owner's `CLAUDE.md` | the owner |
