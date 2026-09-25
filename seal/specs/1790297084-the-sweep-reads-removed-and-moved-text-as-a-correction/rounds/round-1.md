# 1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction — review round 1

| Field | Value |
|---|---|
| Target SHA | 8f70ca948a7bb7156d7f18bfd11ef7d5e8b6eaf4 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 609 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1, a row corrected in place and re-pointed at a renamed unit or a retitled heading takes the removed-row exit and its correction goes unreported. |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item 1790297084 reviews the build at 8f70ca94 against spec.md and plan.md (frame a3e8a499, approved 2e0e2fa7). It covers the survivor sweep leaving a removed ledger row's cells out of the removed wording (#603, including the fourth condition the build added from a measurement), a retired directory taking part in the pairing (#591), and the corrected coordinate naming the correction (#592). The classes are every row shape the exclusion takes while a person corrected its claim (the unsafe direction), every fold range, and every tie in the pairing order.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A row corrected in place goes silent when no anchor it had still resolves at `b`: one anchor renamed, every anchor renamed, or a retitled heading | `skills/code-review/scripts/survivor_check.py:1083` | open | Executed: three probe cases exit 0 at 8f70ca94 and 1 at 7b557144. Contradicts the docstring, ledger P3, the changelog fragment and the `docs/review-chain-spec.md` clause. The id-in-section fix was executed: the three exit 1, the module is green with one fixture id changed, and the six Q2 squashes are unchanged |
| ⬜ 2 | A row moved to the fragment with its claim reworded and one anchor gone takes the exit | `skills/code-review/scripts/survivor_check.py:1083` | open | Executed: exit 0 at target, 1 at base. Consistent with `CLAUDE.md` (*REMOVED, not re-pointed … write the new claim as a new row*). A sentence for `plan.md`'s *What breaks* is the whole fix |
| ⬜ 3 | Report entries tied on score print in hash-seed order | `skills/code-review/scripts/survivor_check.py:1501` | open | Read. Pre-existing, noted in `overview.md`. No test depends on the order |
| ⬜ 4 | Ledger P3 and the changelog fragment claim 🟡 1's shapes are measured | `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md` | open | Correction to the run's paperwork. It becomes true with 🟡 1's fix, and P3 is re-read and re-stamped with it |
| 🟢 | #591: retired departures only move the verdict toward reporting | `skills/code-review/scripts/survivor_check.py:1273` | confirmed | Read. Traced both effects of a retired departure. The module passes at target (executed) |
| 🟢 | #592: the pairing's order is total and does not depend on the hash seed | `skills/code-review/scripts/survivor_check.py:1341` | confirmed | Read. The sort tuple ends in both path strings, and `arrivals` iterates in `fresh` order |
| 🟢 | A missing `evidence_check.py` is refused at exit 2 | `skills/code-review/scripts/survivor_check.py:1003` | confirmed | Read and executed (the refusal case passes in the module run). Matches C's #590 class, and E keeps the three names |

## Paste-ready fixes

```python
# A row's own id -- `R1`, `S3`, `G5` -- heads its first cell, before the ` · `
# that opens the claim, and is unique inside its section. A row corrected in
# place keeps it under the same heading, whatever its anchors did.
ROW_ID = re.compile(r"^\s*\|\s*([A-Z][A-Za-z]*\d+[a-z]?)\s*·")


def ledger_rows(lines, live_lines):
    """`[(line number, heading, row id or None, line)]` for the live table
    rows of `lines`, 1-based, each under the last live heading above it."""
    out, heading = [], None
    for number, (line, live) in enumerate(live_lines(lines), start=1):
        if not live:
            continue
        if line.startswith("#"):
            heading = line.strip()
        elif line.lstrip().startswith("|"):
            match = ROW_ID.match(line)
            out.append((number, heading, match and match.group(1), line))
    return out
```
```python
    rows, standing, named = [], {}, {}
    for path in ledgers:
        lines = after.get(path, "").splitlines()
        standing[path] = [
            cited(line)
            for line, live in live_lines(lines)
            if live and line.lstrip().startswith("|")
        ]
        named[path] = {
            (heading, row_id)
            for _number, heading, row_id, _line in ledger_rows(lines, live_lines)
            if row_id
        }
        kept = set(lines)
        for number, heading, row_id, line in ledger_rows(
            before[path].splitlines(), live_lines
        ):
            if line in kept:
                continue
            # The same id under the same heading at `b` is this row, corrected
            # in place -- measured whatever its anchors did, so a correction
            # re-pointed at a renamed unit or a retitled heading stays loud.
            if row_id and (heading, row_id) in named[path]:
                continue
            anchors = cited(line)
            if anchors:
                rows.append((path, number, anchors))
```
```text
    **A row that still stands, re-pointed, is not removed.** #589's range
    corrected `seal/releases/0.15.1.md` R1 in place and renamed one of its
    tests in the same commit, so the old name left and the corrected claim
    took the exit. A row keeps its id -- `R1 ·` at the head of its first
    cell -- when it is corrected in place, so a removed row whose id still
    stands under the same heading at `b` is that row, and it stays measured
    whatever its anchors did: one anchor renamed, every anchor renamed, or a
    heading retitled. A row with no id falls back to its anchors: it still
    stands where a live row of the file cites every anchor of it that still
    resolves. What stays silent is a row with no id whose every anchor was
    renamed as it was corrected."""
```
```python
    neighbour = ledger_row("A neighbouring claim.", ("pkg/mod.py#other",)).replace(
        "R1 ·", "R2 ·"
    )
```
```python
def test_a_row_corrected_in_place_while_its_only_anchor_is_renamed_is_a_correction(
    tmp_path,
):
    """A row with one anchor, corrected in place and re-pointed at the
    renamed unit. No anchor of the old row resolves at the tip, so the
    anchor rule has nothing to match; the row's id standing under the same
    heading is what says it is the same row. Red at 8f70ca94: exit 0."""
    repo = tmp_path / "probe"
    renamed = MODULE.replace("def helper(", "def helper_renamed(")
    head = ledger_range(
        repo, ledger_row(REPAIRED, ("pkg/mod.py#helper_renamed",)), renamed
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"a one-anchor row corrected in place took the exit:\n{text}"
    assert coordinates_in(text) == {"docs/x.md:3"}, text
    assert set(corrected_lines(text)) == {f"{LEDGER}:5"}, text


def test_a_row_corrected_in_place_while_its_heading_is_retitled_is_a_correction(
    tmp_path,
):
    """A row anchored on a document heading. The range retitles the heading
    and corrects the row in place, re-pointed at the new title. Red at
    8f70ca94: exit 0."""
    repo = tmp_path / "probe"
    os.makedirs(repo)

    def row(claim, title):
        anchor = f'`docs/p.md#"## {title}"@0123abcd`'
        return f"| R1 · {claim} | {anchor} | **Read** 2026-01-01 | 2026-01-01 | |\n"

    build(
        repo,
        {
            LEDGER: LEDGER_HEAD + row(FOUND, "Old title"),
            "docs/p.md": "# p\n\n## Old title\n\nBody.\n",
            "docs/x.md": f"# x\n\n{RESTATED}\n",
            **FILLER,
        },
        "a row anchored on a heading, and a document stating its claim",
    )
    head = build(
        repo,
        {
            LEDGER: LEDGER_HEAD + row(REPAIRED, "New title"),
            "docs/p.md": "# p\n\n## New title\n\nBody.\n",
        },
        "retitle the heading and correct the row in place",
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"a row re-pointed at a new heading took the exit:\n{text}"
    assert coordinates_in(text) == {"docs/x.md:3"}, text
```
```text
  The same holds for a row removed from a shared file whose claim is
  rewritten, reworded, as a new row in the work item's fragment: the old
  row's wording takes the exit, because `CLAUDE.md` makes the new row a new
  claim. A document still stating the old wording is not reported.
```
```python
    return sorted(
        found.values(), key=lambda row: (-row[0], row[1].path, row[1].line)
    )
```
```text
P3's claim, after "and no live row of that file at the tip cites every
anchor of it that still resolves there": insert "and no live row under the
same heading at the tip carries its row id". Re-read and re-stamp P3's
`removed_ledger_rows` anchor in the commit that lands 🟡 1.

changelog.md, the #603 entry: "A row reworded in place, or removed while all
its anchors still resolve, is still measured" stays as written. It is true
once 🟡 1 lands, and the fix is what makes it true.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q -rs` at 8f70ca94, in the round's clone | 143 passed, 0 skipped (S13 over 58629718 ran) |
| Probe file test_tmp_b1.py (five cases built on the module's `ledger_range` helpers) at 8f70ca94 | 4 failed, 1 passed: single-anchor re-point, both-anchors re-point, heading re-point and the fragment reword each exit 0. The two-anchor control exits 1 |
| The same probe file with the base's `survivor_check.py` (7b557144) swapped in | 5 passed: all four shapes exit 1 at the base |
| `survivor-check --range 58629718^..58629718` and `16b77284^..16b77284`, base script and target script | 58629718: base exit 1, 8 places, 98 sentences; target exit 0, 52. 16b77284: exit 0, 73, both ways. Matches `phases/phase-3.md` |
| Candidate fix for 🟡 1 applied in the clone: the probe file and the module | 1 failed (the fragment reword, ⬜ 2, as expected), 147 passed, after the one fixture change to `R2` |
| Probe file test_tmp_b2.py, the two cases fenced under 🟡 1's fixes exactly as written, at 8f70ca94 and then with the candidate fix applied | 2 failed at the target, 2 passed under the fix |
| Before the fixture change: the module under the candidate fix | `test_a_removed_row_sharing_one_live_anchor_with_another_row_takes_the_exit` failed: its neighbour carries the removed row's id `R1` in the same section |
| The six 0.15.3 squashes under the candidate fix | 58629718 exit 0/52; 16b77284 exit 0/73; 7a7d3ae9 exit 1, 14 places, 25; e1f1d4ec exit 1, 17 places, 140; 3f364874 exit 0/84; 6256bbc8 exit 0/23. Identical to `questions.md` Q2 |
| An id probe over the six squashes: does a removed row's id stand under its heading at `b`? | 58629718: 0.14.0.md S1 and P1 and 0.15.1.md S1 all absent at `b`, in section and anywhere in the file. Other squashes: no removed rows |
| `bin/evidence-check .` at 8f70ca94 | exit 0 |
| The broad gate: full suite, repository-wide lint and typecheck | not yet — nobody has run it. The sealer runs it once, after the rounds settle |

```python
def test_tmp_single_anchor_corrected_in_place_while_renamed(tmp_path):
    repo = tmp_path / "probe"
    renamed = MODULE.replace("def helper(", "def helper_renamed(")
    head = ledger_range(
        repo,
        ledger_row(REPAIRED, ("pkg/mod.py#helper_renamed",)),
        renamed,
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1  # exit 0 at 8f70ca94, exit 1 at 7b557144
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
