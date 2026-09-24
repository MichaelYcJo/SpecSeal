# Review round 2 — `fix/547-the-fold-writes-each-release-to-its-own-file`

Target SHA `c7d64f2a`, base `release/v0.15.1` at `6b912e66`. This is the
verifying round. It read round 1's fix range `635627c7..47ca9ce6`, the two
owner-authorized edits inside it, and the two merges `dff99894` and
`c7d64f2a`. It did not re-read the branch. I worked in a
`git clone --no-local` of the worktree at the target. Every probe ran in
scratch copies of that clone, never in the worktree.

Round 1's ten findings are closed, and so are its two deferrals to the owner.
The split does on the real ledger what the prompt asked me to show. Every row
lands in exactly one file, a second split refuses, nothing drifts or breaks,
and the distinct (status, coordinate) count is 1713 before and after. Both
merges keep every note from both sides and every correction C made, and the
`-s ours` merge changes no file.

Two things need a fix, and both are sentences.

- **`CLAUDE.md` still states the removal rule for `seal/ledger.md` alone**
  (finding 1). It also says `CONTRIBUTING.md` carries the same sentence,
  and that stopped being true when this branch widened the twin in
  `CONTRIBUTING.md` to cover the release files. Phase 5 listed the two
  `CLAUDE.md` paragraphs that go false. Line 139 was a third, and the
  orchestrator's edit at `47ca9ce6` did not reach it.
- **The release checklist asks for a count that no command prints**
  (finding 2). Round 1's fix replaced *the same totals* with *the same count
  of distinct (status, coordinate) pairs*, and says `evidence_check.py
  --strict .` reports it. The checker prints only per-file and total
  ok/drifted/broken figures. I had to write a probe to take this reading, and
  the release that runs `--split` is the next one.

The six ⬜ findings behind those two do not ship a defect in this release.
They are one latent split case, one unpinned symptom of round 1's first
finding, and four places that fall short of the tree in their wording.

## Round 1's fixes, checked against the code

**Finding 1 (the split's anchor reading) is closed.** `SELF_ANCHOR_RE` now
has the checker's `@hash` look-ahead and reads `\"` inside the quotes, which
matches `evidence_check.py#ANCHOR_RE` term for term. The heading-path branch
tests `parts[0].strip()` against a pattern equal to the checker's
`heading_level`, and the whole-line branch collapses whitespace the way
`evidence_check.py#text_regions` does. The real-tree dry run at the target
prints no *could not place* entry. Both new units are correct as code. I saw
both of them fail against the script with `63fbfa52` reverted, on
*could not place* and on `'8' != '8'`.

**Finding 1's escaped-quote symptom is fixed, but no case pins it** (⬜ 4).
Round 1 listed four symptoms, and the planted case covers three of them. I
took out the `|\\"` alternative from the locator group. The mutant passes the
whole fold module (62 passed), and it leaves such an anchor unrewritten and
unnamed. The case under §Paste-ready fixes fails on the mutant, fails against
the pre-fix script (on *could not place*, with the locator cut short at
`wrote, \"`), and passes at the target.

**Findings 2 and 3 (the totals claim) are closed as sentences.** All six
carriers now say that no row's status changes and that the `ok` count can
rise. That is what I measured: 1736 ok before and 1932 after, 0 drifted and
0 broken both times, and 1713 distinct pairs both times. But the checklist's
new comparison is finding 2 of this round.

**Findings 4, 5, 8 and 9 are closed.** `docs/the-evidence-ledger.md:109`
names the release files and the reason that still holds. The four comments
are rewritten at `evidence_check.py:4`, `evidence_check.py:2140`,
`correction_check.py:234` and `hygiene.yml:122`. The past incident at
`docs/review-chain-spec.md:1424` is in the past tense. In the real-tree dry
run, each rewrite prints its own line: both rewrites sit on
`seal/releases/0.13.1.md:66`, which is correct because the two anchors share
one table row.

**Findings 6, 7 and 10 were answered, and the records say so.** `overview.md`
names the two false entries at `577f1671` and none on the fix. The changelog
fragment says a row's status does not change and the count can rise.
`phases/phase-1.md` and `phases/phase-2.md` carry the three answers.

## The split, run again on a copy of the real ledger

I exported the target tree, then ran the checker, the dry run, the split, the
checker again, a second split and `--check`. I also ran an in-process
accounting probe before and after. The results are in §Executed probes. Every
figure the prompt asked for holds: 1027 table lines before and after, with
the same multiset once the two rewrites are undone; 0 drifted and 0 broken;
1713 distinct (status, coordinate) pairs both times; and `nothing to split`,
exit 1, on the second run.

### ⬜ 3 · The split moves a line anchor that the checker resolved to a kept line

`.github/scripts/fold_ledger.py:579`, inside `split`. Round 1's fix keys
`moved` and `kept` on every non-blank line, not only on headings. That makes
a collision possible which the heading-only keys rarely allowed. A line can
stand once in a moved section and again in the standing area. The checker
reads that as two places and lets the row's own hash choose between them
(`evidence_check.py#check_text`). The split reads no hash, so it rewrites the
anchor into the release file whichever place the row meant.

I planted `Shared line.` in the standing area, inside a two-line paragraph,
and again in beta's section. I added a row resolved by hash to the standing
copy. The checker read `6 ok · 0 drifted` before the split. The dry run
listed the anchor as a rewrite to `seal/releases/0.2.0.md` with no warning,
and after the split the checker read `5 ok · 1 drifted`, exit 1. The same
thing happens to a line that two moved sections share and the standing area
also holds: the key drops out of `moved`, stays in `kept`, and is kept in
silence.

It is ⬜ and not 🟡 because the real ledger has no such anchor (only two
self-anchors, both on headings), and the split runs once. The checklist's
0-drifted reading after the split would also catch it. The fix under
§Paste-ready fixes names the anchor for a person instead. With the fix, that
probe reads `6 ok · 0 drifted` after the split, the fold module passes, and
the real-tree dry run prints byte-identical output.

## The two owner-authorized edits

**`templates/seal-README.md` and `seal/README.md` are byte-identical**
(`cmp` exit 0), and no line of the template names a fold destination. The
only fold lines are 79–84, *the shared ledger every fragment is read beside*
and *gathered at a release by the repository's own fold*. Line 67's export
destination is the fragment. The layout block now leaves out the directory
that holds most of this repository's rows after the split (⬜ 8, a question
for the owner).

**`CLAUDE.md`'s fold paragraph says what the code does.** The fold writes
`release_path(args.version)` (`fold_ledger.py:828`) and removes the fragment
(`:900`). `evidence_check.py#default_patterns` reads `ledger.md`,
`ledger/*.md` and `releases/*.md` under the seal home. *The move changes no
row's status* is what I measured. *`seal/ledger.md` keeps the notation and
the rows from before the fragments existed* is true after the split: 103
lines and 19 ok rows.

**The conflict rule's heading does not name every ledger file**, although the
prompt said it does (⬜ 5). It names `seal/ledger.md` and the release files,
and `CONTRIBUTING.md:225` does the same. Fragments are left out, and
`dff99894` conflicted in a fragment (F1 and F3 of
`seal/ledger/1790206437-a-second-fold-writes-a-second-heading.md`).

### 🟡 1 · `CLAUDE.md`'s removal rule names one ledger file, and its twin now names two

`CLAUDE.md:139`: *A branch that removes code an existing `seal/ledger.md` row
cites must touch that file … `CONTRIBUTING.md` carries the same sentence*.
This branch rewrote the twin at `CONTRIBUTING.md:210` as *Change what an
existing ledger row cites — in `seal/ledger.md` or a `seal/releases/` file*.
So the two now disagree about which files the rule covers, and the sentence
saying they agree is false. This is the failure the paragraph was written to
end: *the two used to disagree*. `CLAUDE.md:134`'s table has the same gap
next to `CONTRIBUTING.md:198`, which forbids appending to a release file.

It matters because after this release's split `seal/ledger.md` holds 19 of
1932 ok entries. `CLAUDE.md` is loaded into every session. Read literally,
its rule is about 1% of the rows. The heading *never the shared file* then
leaves a session unsure whether a release file is a file it may edit. This is
the §12 class of round 1's findings 4 and 5: a carrier that names the old
ledger file set. Phase 5 enumerated the two paragraphs that went false and
missed this one. A smith may not edit `CLAUDE.md` (`agents/smith.md`), so the
answerer is the orchestrator if the owner's authorization for `47ca9ce6`
covers these two lines, and the owner otherwise.

### 🟡 2 · The checklist asks for a count that no command prints

`docs/release-checklist.md:152`: *`evidence_check.py --strict .` reports no
drifted and no broken row before and after the split, and the same count of
distinct `(status, coordinate)` pairs*. The checker's options are `root`,
`--ledger`, `--map`, `--strict` and two more (`evidence_check.py:2382–2398`),
and none of them prints that count. Its output is the per-file and total
ok/drifted/broken lines. I took the figure only with an in-process probe that
imports the module.

The session that follows this step is the next release's. It either stops to
build an instrument, which is the stall this project's first goal exists to
remove, or it skips the reading. The fix keeps the two readings the checker
does print (the exit code, 0 drifted and 0 broken) and swaps the distinct
count for one a shell can take: the number of table lines across every ledger
file. That count measures the thing the reading is for, every row landing in
exactly one file. At the target it reads 1027 before and 1027 after.

## The two merges

- **The release tree is step C's tip.** `git diff 76bc951d 6b912e66` is
  empty. The worktree's `origin/release/v0.15.1` is `6b912e66`, and its diff
  against `76bc951d` is empty too. `dff99894` and `c7d64f2a` have one tree,
  `ee72105a`, so the `-s ours` merge changes no file.
- **The docstring is a union.** `fold_ledger.py:59–72` keeps C's measured
  figure (*seventeen ledger sections from `0.9.4` to `0.15.0`*, eighteen
  tags, `0.13.2`). It takes this branch's release-file wording for the join,
  for `--check` and for the refusal of a `seal/ledger.md` that heads a
  release. C's sentence about the join into a section of the shared ledger
  is replaced by this branch's, which is what the code now does.
- **The three rows are unions.** I compared every row of the three ledger
  files the merge touched against `9f5902e5`, both parents and the result, by
  word runs. Nothing either side added is missing, nothing C removed came
  back, and no row was dropped. The one flag was a tokenisation artefact
  (`list.` against `list`), and I read that row (F1) in full by hand. F1
  keeps C's two fix-pass notes (*seventeen ledger sections*, *thirty-one
  minutes*) and this branch's three notes. It takes this branch's anchors,
  with the retired case dropped, and re-stamps the join case to `4c5e5ca1`.
  F3 keeps C's measured gap and seventeen-section note and this branch's
  phase-4 note. The seam row keeps C's ⬜ 6 note and this branch's phase-5
  note, re-stamped to `deb05ae6`. `six releases` survives only where a note
  quotes it as the figure it replaced.
- `correction-check` over `6b912e66...c7d64f2a` and over
  `9f5902e5...c7d64f2a` finds two merges and no dropped marker, exit 0 both
  times.

## Regression tests to plant

- `tests/test_the_ledger_fragments_fold_at_release.py`: the escaped-quote
  case (⬜ 4), next to
  `test_the_split_names_only_the_anchors_it_cannot_place`.
- The same file: a case for ⬜ 3 if its fix is taken, planted from the probe
  in §Executed probes. After the fix the probe asserts *could not place* and
  `0 drifted`.

## Facts for the evidence ledger

- `SELF_ANCHOR_RE` and `evidence_check.py#ANCHOR_RE` read one locator
  grammar: a quoted body with `\"` allowed, an optional `>"claim"` and an
  `@hash` of 6–12 hex digits. Executed as above. This could be a row in the
  work item's fragment beside P1, anchored at `fold_ledger.py#split` and
  `evidence_check.py#ANCHOR_RE`.
- At `c7d64f2a` the split conserves 1027 table lines and 1713 distinct
  (status, coordinate) pairs, and the checker's `ok` rises from 1736 to 1932.
  This extends P2's figures, which were taken at `577f1671`.

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
| `cat` of every ledger file piped to `grep -c '^|'`, before and after | 1027 and 1027 |
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

## Paste-ready fixes

### 🟡 1

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

### 🟡 2

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

### ⬜ 3

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

### ⬜ 4

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

### ⬜ 5

```markdown
**When a ledger file conflicts — `seal/ledger.md`, a
`seal/releases/<X.Y.Z>.md`, or a fragment two stacked branches both edited —
resolve it hunk by hunk and read both sides.**
```

### ⬜ 6

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

### ⬜ 8

```
├── releases/            one file per release, where a repository's own fold
│                        writes one — read beside the two above
```

Needs a fix: yes — 🟡 1 (`CLAUDE.md`'s removal rule and table name `seal/ledger.md` alone against their widened twin), 🟡 2 (the release checklist's distinct count has no command that prints it)

Loses a record or crashes: no

## Proof block

Opened in this round, in the clone at `c7d64f2a` unless named otherwise:
`seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/rounds/round-1.md`
and `round-1-report.md` (worktree and clone); `phases/phase-5.md`;
`overview.md` and `changelog.md` (fix-range diff);
`.github/scripts/fold_ledger.py` (lines 440–640, the docstring by diff, and
the remerge diff); `skills/evidence-check/scripts/evidence_check.py` (lines
55–110, 228–420, 947–975, 1200–1370, 1783–1792);
`skills/code-review/scripts/chain_check.py` (lines 400–456);
`tests/test_the_ledger_fragments_fold_at_release.py` (lines 660–760 and the
two new units); `tests/test_a_merge_cannot_silently_drop_a_correction.py`
(lines 1125–1142); `tests/test_the_record_is_held_to_the_floor_and_the_depth.py`
(lines 500–507); `tests/test_a_record_states_what_the_tree_has.py` (lines
50–58); `CLAUDE.md` (lines 118–190); `CONTRIBUTING.md` (lines 195–240);
`seal/README.md` (lines 60–105); `templates/seal-README.md` (by grep and
`cmp`); `docs/release-checklist.md` (lines 80–160);
`docs/review-chain-spec.md` (lines 214–226); `docs/one-root-by-lifetime.md`
(lines 1–12, 94–100, 146–154); `.github/workflows/hygiene.yml` (lines
250–262); `bin/test`; the fix-range diff `635627c7..47ca9ce6`; the remerge
diffs of `dff99894` for `fold_ledger.py`, `seal/ledger.md` and
`seal/ledger/`; the F1 row at `9f5902e5`, both parents and the result.
