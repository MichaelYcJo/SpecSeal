# 1790208593-the-fold-writes-each-release-to-its-own-file — review round 2

| Field | Value |
|---|---|
| Target SHA | c7d64f2a1540a8b6c35fd00ea6c2ae4780246b99 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | 558 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (`CLAUDE.md`'s removal rule and table name `seal/ledger.md` alone against their widened twin), 🟡 2 (the release checklist's distinct count has no command that prints it) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2, the verifying round, reviewed at c7d64f2a: round 1's fix range `635627c7..47ca9ce6` — the smith's five fix commits and the orchestrator's owner-authorized `CLAUDE.md` edit — the generalized `seal/README.md` template, and the two merges that followed #552's squash (dff99894, C's final tip with 9f5902e5 as the merge base, three conflicts resolved as a union of notes; c7d64f2a, the squash recorded with no content change after the trees were verified identical). It asked whether each round-1 finding is closed at its coordinates, whether the two owner edits say what the code does, whether every resolved row keeps both sides' notes and C's corrections, and whether `--split` over a copy of the real ledger still puts every row in one file with no status changed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `CLAUDE.md`'s removal rule and its instead-of table name `seal/ledger.md` alone, while the twin in `CONTRIBUTING.md` names the release files too; *`CONTRIBUTING.md` carries the same sentence* is false | `CLAUDE.md:139` (and `:134`) | open | read — against `CONTRIBUTING.md:198` and `:210`; phase 5 enumerated two paragraphs and not this one; the answerer is the orchestrator under the owner's authorization for `47ca9ce6`, or the owner |
| 🟡 2 | The release checklist says `evidence_check.py --strict .` reports a count of distinct (status, coordinate) pairs; nothing prints that count | `docs/release-checklist.md:152` | open | executed — the checker's output at the target is per-file and total ok/drifted/broken only; the count needed an in-process probe; the table-line count by `grep -c` reads 1027 before and after |
| ⬜ 3 | The split rewrites a line anchor whose line the standing area also holds, which turns a row the checker resolved by hash to the kept copy into DRIFTED; a line that two moved sections share and the standing area holds is kept in silence | `.github/scripts/fold_ledger.py:579` | open | executed — probe: `6 ok · 0 drifted` before, the anchor listed as a rewrite, `5 ok · 1 drifted` exit 1 after; the fix names it, and the real-tree dry run is unchanged; not on the real ledger |
| ⬜ 4 | The escaped-quote symptom of round 1's first finding is fixed and pinned by no case | `tests/test_the_ledger_fragments_fold_at_release.py:842` | open | executed — a mutant dropping the `\\"` alternative passes the fold module (62 passed); the proposed case is red on the mutant and on the pre-fix script, and green at the target |
| ⬜ 5 | The conflict rule's heading names `seal/ledger.md` and the release files but not a fragment, and this branch's own merge conflicted in one; the account said it names every ledger file | `CLAUDE.md:146` (and `CONTRIBUTING.md:225`) | open | read — `dff99894`'s conflicts in `seal/ledger/1790206437-a-second-fold-writes-a-second-heading.md`; the answerer is the owner |
| ⬜ 6 | Two test docstrings still say the fold writes into the shared file, in the present tense | `tests/test_a_merge_cannot_silently_drop_a_correction.py:1135` (and `tests/test_the_record_is_held_to_the_floor_and_the_depth.py:504`) | open | read — the twins of round 1's eighth finding and of `1d0c61b8`'s survivor, one in the same file as that survivor |
| ⬜ 7 | Three edited lines are left unwrapped, at 110–146 characters | `.github/workflows/hygiene.yml:123` (and `CLAUDE.md:147`, `skills/evidence-check/scripts/correction_check.py:238`) | open | read — no wrap case covers these files, so nothing reports them |
| ⬜ 8 | This repository's `seal/README.md` layout, verbatim from the template, leaves out `releases/`, which holds most of the rows after the split | `templates/seal-README.md:79` | open | read — the template already lists optional entries (`parity.md`, `follow-up.md`); a question for the owner |
| 🟢 | Round 1's should-fix finding 1 is closed — the split reads an anchor by the checker's rule | `.github/scripts/fold_ledger.py#split` | verified | executed — the real-tree dry run names nothing it cannot place; both new units red with `63fbfa52` reverted and green at the target |
| 🟢 | Round 1's should-fix findings 2 and 3 are closed — six carriers say no row's status changes and the `ok` count may rise | `docs/release-checklist.md:152`, `.github/scripts/fold_ledger.py:19` | verified | executed — 1736 then 1932 ok, 0 drifted, 0 broken, 1713 distinct both times; the checklist's replacement reading is finding 2 of this round |
| 🟢 | Round 1's should-fix findings 4 and 5 are closed — the policy document and the four comments name the release files | `docs/the-evidence-ledger.md:109` | verified | read — also `evidence_check.py:4`, `:2140`, `correction_check.py:234`, `hygiene.yml:122` |
| 🟢 | Round 1's findings 8 and 9 are closed — the incident is in the past tense, and each rewrite prints its own line | `docs/review-chain-spec.md:1424`, `.github/scripts/fold_ledger.py:592` | verified | read and executed — the case is red with `63fbfa52` reverted |
| 🟢 | Round 1's findings 6, 7 and 10 are answered in the records | `seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/overview.md` | verified | read — `overview.md`, `changelog.md`, `phases/phase-1.md`, `phases/phase-2.md` |
| 🟢 | Round 1's two deferrals to the owner are resolved — the README pair is generalized and `CLAUDE.md`'s fold paragraph names the release file | `CLAUDE.md:176`, `templates/seal-README.md:79` | verified | read — `cmp` exit 0; the fold writes `release_path(args.version)`; `default_patterns` reads the three addresses |
| 🟢 | The split on a copy of the real ledger at the target: every row in one file, a second split refuses, 0 drifted and 0 broken, the distinct count equal | `.github/scripts/fold_ledger.py#split` | verified | executed — 1027 table lines with an equal multiset, 1713 distinct pairs, `nothing to split` exit 1 |
| 🟢 | The two merges keep every note from both sides and C's corrections, and change no file past `dff99894` | `seal/ledger.md`, `seal/ledger/1790206437-a-second-fold-writes-a-second-heading.md`, `.github/scripts/fold_ledger.py:59` | verified | executed — the word-run union probe; empty diffs; one tree `ee72105a`; `correction-check` exit 0 |

## Paste-ready fixes

```markdown
| rows appended to `seal/ledger.md` or a `seal/releases/<X.Y.Z>.md` | `seal/ledger/<work-item-id>.md` |
```
```markdown
**Appended is the word, and a removal is not one.** A branch that removes code
an existing ledger row cites — in `seal/ledger.md` or a
`seal/releases/<X.Y.Z>.md` — must touch that file to leave the ledger true:
the row is removed there, and the new claim is written into the branch's own
fragment. `CONTRIBUTING.md` carries the same sentence, and the two
used to disagree: one forbade editing the file at all while the other forbade
appending to it, which left a branch in this position with no reading that
permits the only correct act.
```
```markdown
green; `evidence_check.py --strict .` exits 0 before and after the split,
with no drifted and no broken row. Its `ok` total rises, because the checker
counts a `(coordinate, hash)` pair once per file and the split puts pairs two
releases shared into two files, so the total is not the comparison. The
table lines are: `cat seal/ledger.md seal/ledger/*.md | grep -c '^|'` before
the split prints the number that
`cat seal/ledger.md seal/releases/*.md seal/ledger/*.md | grep -c '^|'`
prints after it, which is every row in exactly one file. And
`correction-check` over the next release's merges stays silent across the
moved rows. So the whole gate runs on this tree, and
every exit code is read directly rather than through a `| tail`.
```
```python
    twice = {k for k, v in moved.items() if v is None}
    moved = {k: v for k, v in moved.items() if v is not None}
    rest = [line for n, line in enumerate(lines) if n not in inside]
    kept = {" ".join(line.split()) for line in rest if line.strip()}
    # A line that stands in more than one place is several places to the
    # checker, and the row's own hash picks between them
    # (`evidence_check.py#check_text`). The split reads no hash, so an anchor
    # to such a line is named for a person rather than moved or kept by guess.
    both = (kept & moved.keys()) | (kept & twice)
    moved = {k: v for k, v in moved.items() if k not in both}
    kept -= both
```
```python
def test_a_line_the_standing_area_also_holds_is_named_not_moved(split_tree):
    """#547, round 2's ⬜ 3. A line in the standing area and in a moved
    section is two places to the checker, which the row's hash decides; the
    split reads no hash, so it names the anchor and moves nothing."""
    path = split_tree / "seal" / "ledger.md"
    text = path.read_text(encoding="utf-8").replace(
        "## An area from before the fragments\n\n",
        "## An area from before the fragments\n\nShared line.\nMore standing text.\n\n",
    ).replace("### 1700000002-beta\n\n", "### 1700000002-beta\n\nShared line.\n\n")
    a, b = ec.resolve("seal/ledger.md", '"Shared line."', text)[0]
    h = ec.content_hash(text.splitlines()[a - 1 : b])
    row = f'| a standing line | `seal/ledger.md#"Shared line."@{h}` | read | 2026-09-01 | |\n'
    at = text.index("\n", text.index("| the old claim |")) + 1
    path.write_text(text[:at] + row + text[at:], encoding="utf-8")
    r = run("--split", root=split_tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert 'seal/ledger.md  seal/ledger.md#"Shared line."' in r.stdout, r.stdout
    after_line, after_rc = check(split_tree)
    assert after_rc == 0 and "0 drifted" in after_line, after_line
```
```python
def test_the_split_reads_an_escaped_quote_the_way_the_checker_does(split_tree):
    """#547, round 1's 🟡 1, its fourth symptom. A locator holding `\\"` is
    one locator to the checker; the split reads it whole and rewrites it."""
    path = split_tree / "seal" / "ledger.md"
    said = 'A sentence beta wrote, "quoted" inside.'
    text = path.read_text(encoding="utf-8").replace(
        "### 1700000002-beta\n\n", f"### 1700000002-beta\n\n{said}\n\n"
    )
    h = ledger_hash(text, said)
    escaped = said.replace('"', '\\"')
    row = f'| a quoted line | `seal/ledger.md#"{escaped}"@{h}` | read | 2026-09-01 | |\n'
    at = text.index("\n", text.index("| the old claim |")) + 1
    path.write_text(text[:at] + row + text[at:], encoding="utf-8")
    before_line, before_rc = check(split_tree)
    assert before_rc == 0 and "0 broken" in before_line, before_line
    r = run("--split", root=split_tree)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "could not place" not in r.stdout, r.stdout
    assert f'`seal/releases/0.2.0.md#"{escaped}"@{h}`' in ledger(split_tree), r.stdout
    after_line, after_rc = check(split_tree)
    assert after_rc == 0 and "0 broken" in after_line, after_line
```
```markdown
**When a ledger file conflicts — `seal/ledger.md`, a
`seal/releases/<X.Y.Z>.md`, or a fragment two stacked branches both edited —
resolve it hunk by hunk and read both sides.**
```
```python
    Read through the module's own `LEDGER`, `FRAGMENTS` and `RELEASES` rather than a list
    written here, because a hard-coded list goes blind exactly when the
    fragments are folded at a release -- into the shared file until #547,
    into that release's own file since -- which `fold_ledger.py` did at
    0.12.2, leaving `seal/ledger/` an empty glob in this tree. Tracked files
    only, which is what `ledger_listing` reads through `git ls-tree` at each
    commit.
```
```python
    orchestrator fixes it anyway — the finding was a false count that
    `fold_ledger.py` copied into the shared ledger at the release — commits
    the fix, and sets the verdict to `**fixed**`. Those fixes owe a reader, so
```
```
├── releases/            one file per release, where a repository's own fold
│                        writes one — read beside the two above
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_ledger_fragments_fold_at_release.py`, `tests/test_a_merge_cannot_silently_drop_a_correction.py` and `tests/test_release_hygiene.py`, in the clone at `c7d64f2a` | `161 passed`, exit 0 |
| `evidence_check.py .` on an archive of `c7d64f2a`, before `--split` | `1736 ok · 0 drifted · 0 broken`, exit 0 |
| In-process accounting (a probe file, deleted): table lines across every ledger file, `check_ledger` per file, distinct (status, coordinate) | before: 3 files, 1027 table lines, 1736 entries, 1713 distinct, all OK |
| `fold_ledger.py --split --dry-run` on that copy | exit 0; 29 sections; 2 anchors to rewrite, both at `seal/releases/0.13.1.md:66`; no *could not place*; `seal/ledger.md` byte-identical; no `seal/releases/` |
| `fold_ledger.py --split` on that copy | exit 0; output equal to the dry run apart from the verbs; 29 files; `seal/ledger.md` 103 lines |
| `evidence_check.py .` and `--strict .` after the split | `1932 ok · 0 drifted · 0 broken`, exit 0 both |
| The accounting probe after the split | 32 files, 1027 table lines, the same multiset digest once the rewrites are undone, 1932 entries, 1713 distinct, all OK |
| `cat` of every ledger file piped to `grep -c '^\|'`, before and after | 1027 and 1027 |
| A second `fold_ledger.py --split` | exit 1, `nothing to split: seal/ledger.md heads no release` |
| `fold_ledger.py --check` on the split copy | exit 1, on the two unfolded fragments only |
| The two new units against the script with `63fbfa52` reverted | both fail: *could not place* in stdout, and `'8' != '8'` |
| The escaped-quote case (a probe file, deleted): pre-fix script, target, and a mutant dropping `\\"` from the locator group | pre-fix red (*could not place*, locator cut at `wrote, \"`); target green; the fold module passes on the mutant (62 passed) and the case is red on it |
| The shared-line case (a probe file, deleted), at the target and with the ⬜ 3 fix | target: `6 ok` before, the anchor listed as a rewrite, `5 ok · 1 drifted` exit 1 after; fixed: named under *could not place*, `6 ok · 0 drifted` after; fold module green; real-tree dry run output byte-identical |
| The merge union probe (a probe file, deleted): every changed row of the three ledger files in `dff99894` against `9f5902e5`, both parents and the result | no run either side added is missing, nothing C removed is restored, no row dropped; one tokenisation flag, and that row was read by hand |
| `git diff 76bc951d 6b912e66`, the worktree's `origin/release/v0.15.1`, and the trees of `dff99894` and `c7d64f2a` | empty, `6b912e66` and empty, one tree `ee72105a` |
| `correction-check --range 6b912e66...c7d64f2a` and `--range 9f5902e5...c7d64f2a` | two merges each, no marker dropped, exit 0 |
| `evidence-check --strict .` in the clone with this report copied in | exit 0; records arm `328 names read · 0 refused · 0 drifted` (322 before the report); no line needed `NAME NOT IN TREE` |
| The fenced case for ⬜ 3, with its fix and at the target | green with the fix, red at the target on the *could not place* assertion |
| The broad gate — the full suite, repository-wide lint and typecheck | not yet — the sealer's, after the rounds settle; not taken in this round, and not due while finding 1 and finding 2 are open |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
