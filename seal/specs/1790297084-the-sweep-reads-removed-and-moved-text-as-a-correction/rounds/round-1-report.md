# Round 1 report — 1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | 8f70ca94 |
| Base | `origin/release/v0.15.4` = 7b557144 |
| Build range | 2e0e2fa7..8f70ca94, on the frame a3e8a499 |
| Reviewed by | specseal:warden on claude-opus-5-5 |
| Issues | #603, #591, #592 |

Spec compliance first, then quality. The contract is `spec.md`, `plan.md`
and `questions.md`. The implementer's account (`overview.md`, the three phase
records, the commit messages, the spawn prompt) was read in full and treated
as claims. Each claim below says what was asserted and what the code did.

Carried rather than re-established: the ledger coordinates `evidence-check`
passes (it exits 0 at the target, executed), and the Q2 figures for #588,
#593, #594 and #595, which were re-run only under the candidate fix below
and matched. Nothing was carried from an earlier round, because this is
round 1.

## Findings

### 🟡 1 · A row corrected in place goes silent when every anchor it keeps is renamed

**Where:** `skills/code-review/scripts/survivor_check.py:1062` (the loop in
`removed_ledger_rows` that collects candidate rows) and `:1083` (the
condition at the end of the function, `if left and not (live and any(...))`).

**What is claimed.** The module docstring says a row corrected in place
stays measured "even where the same range renamed one of its units, as
#589's did". The ledger row P3 says the same ("a row corrected in place,
re-pointed … stays measured"). The changelog fragment says "A row reworded
in place … is still measured". `docs/review-chain-spec.md`'s first statement
now says "a row corrected in place is still read".

**What the code does.** The fourth condition keeps a row measured only when
a live row at `b` cites every anchor of it that *still resolves*. When no
anchor of the row still resolves, that set is empty, `live and …` is false,
and the row takes the exit. So the protection depends on how many anchors
the row had and how many the range left alone. Three shapes of one act, a
claim corrected in place and re-pointed at a renamed unit, all go silent at
the target:

- a row with a single anchor, `pkg/mod.py#helper`, corrected FOUND→REPAIRED
  and re-pointed at `helper_renamed`;
- a row with two anchors, both renamed in the same range;
- a row anchored on a document heading, `docs/p.md#"## Old title"`, whose
  heading the range retitles while it corrects the row and re-points it.

**Executed.** Each of the three exits 0 at the target with `docs/x.md`
still stating FOUND. The same three cases exit 1 with the base script
(7b557144), so this is the build turning a reported correction silent. The
builder's own two-anchor, one-renamed case passes in the same probe run as a
control.

**Why it matters.** This is the direction the frame calls the silent one.
`spec.md` judgment 1 exists to keep a correction in place measured, and the
fourth condition was added because Q2 found #589's R1 going silent. The
condition fixes the instance it was measured on (two anchors, one renamed)
and not the class. One-anchor rows are common in this ledger, and a heading
anchor is the ledger's own advice for a document, so a correction that
retitles a heading is a realistic way to hit it.

**The fix.** A row corrected in place keeps its identity, and the ledger
already writes one: the id at the head of the first cell (`R1 ·`, `S3 ·`),
unique inside a work item's section. A removed row whose id still stands
under the same heading at `b` is the same row, whatever its anchors did.
Keep the anchor-subset test for rows that carry no id (`seal/ledger.md` and
three release files have none).

**Executed with the fix applied in the clone:**

- the three silent shapes exit 1, and the control still exits 1;
- all 143 cases of the test module pass, after one fixture change:
  `test_a_removed_row_sharing_one_live_anchor_with_another_row_takes_the_exit`
  gives its neighbour the same id `R1` as the removed row, in one section,
  which the ledger never does. It needs `R2`;
- the six 0.15.3 squashes report what `questions.md` Q2 records: #587
  exit 0 against 52 sentences, #589 exit 0 against 73, #588 14 places
  against 25, #593 17 against 140, #594 0 against 84, #595 0 against 23.

Measured on #587 before the fix was written: none of its three removed rows
(0.14.0.md S1 and P1, 0.15.1.md S1) has its id standing anywhere in its file
at `b`. So the id rule keeps #587's fix.

What still stays silent after the fix: a row carrying no id, corrected in
place with every anchor renamed. That is a smaller class than today's, and
the fix's docstring sentence names it.

### ⬜ 2 · A row moved to the fragment with its claim reworded goes silent, which the policy supports

**Where:** `skills/code-review/scripts/survivor_check.py:1083`.

A range deletes `helper`, removes a two-anchor row from `seal/ledger.md`,
and writes the claim reworded (FOUND→REPAIRED) as a new row in
`seal/ledger/<id>.md`, citing the anchor that still resolves. Executed: exit 0
at the target and exit 1 at the base. The fix for 🟡 1 does not change it,
because the new row is in another file and has another id.

This is judged consistent with the policy rather than a defect. `CLAUDE.md`
says a row whose anchor a change removes "is REMOVED, not re-pointed. Its
claim went with the code. Write the new claim as a new row in the work
item's own fragment." The new row is a new claim by that rule, and the
removed row's wording is not a correction. It is recorded so the next round
does not find it again as new, and so the planner can see a silent shape the
frame's *What breaks in six months* does not name. Its only other home would
be an issue. No code fix is owed. The fence below adds the sentence to
`plan.md`.

### ⬜ 3 · A report's entries tied on score print in hash-seed order (pre-existing)

**Where:** `skills/code-review/scripts/survivor_check.py:1501`
(`score`'s return).

Read, not executed. `score` walks `mine`, a `set` of n-gram tuples of
strings, so the insertion order of `reached`, and then of `found`, follows
`PYTHONHASHSEED`. The final sort keys on the score alone, so equal scores
keep that order. `overview.md` §*Not done* records it on #593's squash.
Nothing pins the order: `RELEASE_RANGES` compares sets
(`coordinates_in(text) == expected`), so no test is flaky because of it.
This build did not introduce it and does not touch `score`. A one-line
tie-break makes the report reproducible. The smith may take it here or
decline it as outside this work item's scope.

### ⬜ 4 · The paperwork claims 🟡 1's shapes are measured (correction)

**Where:** `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md`
row P3 ("a row corrected in place, re-pointed … stays measured"), and
`seal/specs/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction/changelog.md`
("A row reworded in place … is still measured").

Both are false at the target for the shapes in 🟡 1, and both become true
once 🟡 1 is fixed. The fix edits `removed_ledger_rows`, so P3's anchor
drifts and has to be re-read and re-stamped in the same commit. P3's claim
should then name the id rule beside the anchor-subset rule. This is a
correction to the run's own records, so it stays out of `Needs a fix`.

## Confirmed on the code

- **#591, retired departures cannot hide anything.** Read, backed by the
  module run. A retired directory is gone at `b`, so it adds nothing to
  `fresh`. Its departures can only (i) take an arrival out of `fresh`, which
  shrinks `written`, or (ii) take an arrival away from a live departure of
  the same key, which leaves that departure in `gone`. Both move toward
  reporting. Affinity between two live paths does not count keys that left
  a retired path, so a retired origin cannot reorder live pairings. Extra
  sources a fold creates are verbatim copies and score at most 1.0, under
  the floor. `skills/settle/SKILL.md`'s sentence, *A sentence the same
  branch removes from anywhere else is measured as before*, holds.
- **#592, the tie-breaks are total and do not depend on the hash seed.** The
  sort tuple ends in the two path strings. Its third element is the key's
  first index in `gone`, and `gone` follows `git diff --name-only` order,
  which is path order, so "then by path order" in the docstring is accurate.
  The greedy pop over every origin-destination pair drains `min(departures,
  arrivals)` per key, the same count the old one-for-one Counter took.
  `arrivals` iterates in `fresh` order.
- **The missing sibling is refused at exit 2.** `evidence()` raises
  `Refused` before import when the file is absent, and `main` maps `Refused`
  to 2, which is the class work item C's #590 settles. A sibling that is
  present and will not import is still a traceback, which C's spec also
  leaves as it is. Work item E's `evidence_check.py` (wt-299 at db92ea3b)
  keeps `ANCHOR_RE`, `resolve_unit` and `default_patterns` by name and adds
  no import, so the two meet cleanly at the release branch (read).
- **The line base.** `removed_ledger_rows` counts from 1 as `segments`
  does, and the case that holds the two together passes (executed, module
  run).

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

### 🟡 1's probe cases

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

### 🟡 1 — `skills/code-review/scripts/survivor_check.py`, above `removed_ledger_rows`

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

### 🟡 1 — the same file, the loop inside `removed_ledger_rows`

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

### 🟡 1 — the same file, the docstring of `removed_ledger_rows`: this replaces the paragraph that starts "A row that still stands, re-pointed, is not removed"

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

### 🟡 1 — `tests/test_a_corrected_sentence_survives_elsewhere.py`: the neighbour fixture, then two cases to plant after `test_a_row_corrected_in_place_while_an_anchor_is_renamed_is_a_correction`

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

Both cases, exactly as fenced here, fail at 8f70ca94 and pass with the
two code fences above applied (executed, a second probe file in the clone).
That is the red contract §15 asks for. The smith still shows them red
again on the branch before committing them.

### ⬜ 2 — `plan.md` §*What breaks in six months*, a second sentence under the #603 bullet

```text
  The same holds for a row removed from a shared file whose claim is
  rewritten, reworded, as a new row in the work item's fragment: the old
  row's wording takes the exit, because `CLAUDE.md` makes the new row a new
  claim. A document still stating the old wording is not reported.
```

### ⬜ 3 — `skills/code-review/scripts/survivor_check.py`, `score`'s return

```python
    return sorted(
        found.values(), key=lambda row: (-row[0], row[1].path, row[1].line)
    )
```

### ⬜ 4 — ledger P3 and the changelog fragment

```text
P3's claim, after "and no live row of that file at the tip cites every
anchor of it that still resolves there": insert "and no live row under the
same heading at the tip carries its row id". Re-read and re-stamp P3's
`removed_ledger_rows` anchor in the commit that lands 🟡 1.

changelog.md, the #603 entry: "A row reworded in place, or removed while all
its anchors still resolve, is still measured" stays as written. It is true
once 🟡 1 lands, and the fix is what makes it true.
```

## Regression tests to plant

| Case | Destination |
|---|---|
| A one-anchor row corrected in place while its only unit is renamed is still a correction | `tests/test_a_corrected_sentence_survives_elsewhere.py`, in the #603 block |
| A heading-anchored row corrected in place while the heading is retitled is still a correction | the same file and block |

## Facts for the evidence ledger

- After 🟡 1: a removed row whose id still stands under the same heading at
  the tip is read as corrected in place and stays measured. The anchors are
  `removed_ledger_rows` and the two cases above. The fact goes into P3 (⬜ 4)
  rather than a new row.
- #587's three removed rows carry ids that stand nowhere in their files at
  `58629718`. Executed, the id probe above.

Needs a fix: yes — 🟡 1, a row corrected in place and re-pointed at a
renamed unit or a retitled heading takes the removed-row exit and its
correction goes unreported.

Loses a record or crashes: no

## The broad gate

Nothing this round found is left open except 🟡 1 and three ⬜ rows. The
broad gate is not due yet. It comes due, as the sealer's spawn, once the
round that checks 🟡 1's fix closes with nothing open.

## Proof block

Files opened this round:

- `seal/specs/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction/`:
  `spec.md`, `plan.md`, `questions.md`, `overview.md`, `changelog.md`,
  `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`
- `skills/code-review/scripts/survivor_check.py`: the diff 7b557144..8f70ca94,
  plus `reader`, `retired_directories`, `LEDGER_SHAPES` through
  `removed_ledger_rows`, `corrected`, `paired_across_paths`, `read_blobs`,
  `Sentence`, `sentences`, `score`, `main`
- `skills/evidence-check/scripts/evidence_check.py`: the imports,
  `ANCHOR_RE`, `resolve_unit`, `default_patterns`
- `tests/test_a_corrected_sentence_survives_elsewhere.py`: the diff
  7b557144..8f70ca94, and the `RELEASE_RANGES` assertions
- `docs/review-chain-spec.md`: the diff 7b557144..8f70ca94
- `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md`,
  and the `seal/releases/*.md` rows the diff changes
- `seal/releases/0.15.1.md` at 16b77284, the diff of R1 and its neighbours
- `bin/test`
- work item C's `spec.md` (wt-602), the lines naming #590; work item E's
  diff to `evidence_check.py` (wt-299), the imports and the three names
