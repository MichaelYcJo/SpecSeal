# 1790297084 — review round 2 report (verifying round)

Target SHA: `66df04dfe74d6eefc073339c7ea69f9b8f7b331f`. Fix range under review:
`166ceb65..a98929d3`, 4 commits. This round checked round 1's four verdicts and
judged the units round 1's `New units` row names (`ROW_ID`, `ledger_rows`, and
the four new cases) as new code. It did not re-read the branch.

## Summary

Round 1's finding 1 is closed for the shape it was written for. A row whose
id the pattern reads, corrected in place under an unchanged heading, now stays
measured when one anchor, every anchor, or a cited heading is renamed. Both
extra cases the fix pass added go red under their mutation. The other three
round-1 verdicts hold, with two residuals written up as ⬜.

The id rule stands on an assumption the tree does not hold, and that leads to
three new findings:

1. **🟡 1: an id is not unique in its section.** 13 groups of rows in
   `seal/releases/0.14.0.md` and `seal/releases/0.5.0.md` share one id. Each
   group is a claim split across rows (G5 has four rows). When a range removes
   one of those rows because its code left, a sibling row with the same id
   keeps it measured. At `8f70ca94` that removed row took the exit, so this is
   a regression toward reporting. The fix pass edited the one case that
   exercised this shape, changing its neighbour from `R1` to `R2`. That made
   the case pass without closing the shape.
2. **🟡 2: the pattern misses an id shape the latest release uses.**
   `seal/releases/0.15.3.md` has 14 rows with ids like `P1-1 ·`. `ROW_ID` does
   not match them, so those rows fall back to their anchors. If one is
   corrected in place while its anchor is renamed, the correction goes silent.
3. **🟡 3: the stated bound is narrower than what goes silent, and two
   documents state no bound.** The function docstring says only *a row with no
   id whose every anchor was renamed* goes silent. Three more shapes are
   silent, all measured by probes at the target:
   - a row with an id whose ledger section is retitled in the same range;
   - a row with an id that moves to another section of the same file;
   - a row with no id where one anchor is renamed and a still-resolving anchor
     is dropped from the corrected row.

   Two documents state no bound at all: the module docstring (line 194) and
   `docs/review-chain-spec.md:924`. The rows the rule does not read an id from
   are a large share of the ledger, not an edge case: 298 of about 800
   anchored rows, 21 of them in `seal/ledger.md`.

## Answers to round 1

- **Finding 1 (the row corrected in place goes silent): verified for rows
  with an id.** *Executed:* at the target, all five cases in the fix range's
  new units pass. The round-1 shapes exit 1: one anchor renamed, every anchor
  renamed, a cited heading retitled. The heading half of the key goes red when
  removed (mutation B below). *Read:* the rule at
  `skills/code-review/scripts/survivor_check.py:1103` matches the docstring for
  the shape it covers. What stays open is the population the rule does not
  reach. That is 🟡 2 and 🟡 3 below.
- **Finding 2 (the fragment reword takes the exit): answered.** *Read:* the
  plan's *What breaks* now holds the sentence round 1 asked for, and it agrees
  with `CLAUDE.md`'s REMOVED-not-re-pointed rule. This round made no code
  claim to re-check.
- **Finding 3 (tied entries print in hash-seed order): verified for ties at
  different coordinates.** *Executed:* reverting the tie-break turns
  `test_places_tied_on_score_print_in_path_order_whatever_the_hash_seed` red,
  so the 16-seed case does catch the defect. It reaches its two places through
  different phrases, as commit `e785a803` says. There is one residual, ⬜ 4:
  two sentences on one line still tie on path and line.
- **Finding 4 (P3 and the changelog overclaim): verified.** *Executed:*
  `bin/evidence-check .` exits 0 at the target. *Read:* P3 carries the new
  clause and a `Corrected 2026-09-25` note, and its `removed_ledger_rows` hash
  is re-stamped to `22d1fc62`. The changelog sentence *A row reworded in
  place … is still measured* is true: a reword that leaves every anchor
  resolving never takes the exit. P3's closing *so …* clause still claims more
  than the rule does, which is ⬜ 5.
- **Round 1's three confirmations (#591, #592, the refusal when
  `evidence_check.py` is missing): carried.** *Read:* the fix range's diff of
  the script touches `ROW_ID`, `ledger_rows`, `removed_ledger_rows`, the
  module docstring and `score`'s sort key. It does not touch `corrected`,
  `paired_across_paths` or `evidence`. *Executed:* at the target,
  `58629718^..58629718` still exits 0 against 52 sentences, which matches Q2.

## Findings

### 🟡 1: a split claim's sibling row keeps a removed row measured

`skills/code-review/scripts/survivor_check.py:1019` says a row id "is unique
inside its section". The tree says otherwise. Under one heading,
`seal/releases/0.14.0.md` has G3 twice, D3 twice and G5 four times, at lines
36–44. `seal/releases/0.5.0.md` has ten more groups: S1, S1b, S6, S12, S13, S16,
S17c, S19, S19b and S19e. In each group the claim is split across rows under
one id.

`CLAUDE.md` says: *a row whose anchor a change removes is REMOVED*. Suppose a
range removes one G5 row because its unit left the code, and the other three
G5 rows stay. `(heading, "G5")` still stands at `b`, so the check at line 1103
keeps the removed row measured. A document that still states its claim is then
reported as a survivor. That is the loss the module docstring prices as "a red
build to somebody who did not write the line".

*Executed:* in a probe, two rows share `R1` and the range removes one of them
along with its unit. The target exits 1. The script at `8f70ca94` exits 0. The
case the tree already had for this shape,
`test_a_removed_row_sharing_one_live_anchor_with_another_row_takes_the_exit`,
failed under round 1's candidate fix. The fix pass then changed its neighbour's
id to `R2` (line 4238) instead of changing the rule.

Once an id can repeat within a section, it only identifies a row if no row
with that id disappeared. The fix below counts rows per `(heading, id)` at both
ends. A key that stands fewer times at `b` than at `a` lost a row. The id does
not say which row it lost, so every row under that key falls back to its
anchors. The fix below also restores the neighbour's id to `R1`, which makes
that case pin the shape again. The fix does not cover a range that removes a
row and gives its id to a new row with a different claim. That range is
byte-for-byte the same as a correction in place, and it stays measured, which
is the safe direction. This report does not count it as a finding.

### 🟡 2: `ROW_ID` misses the id shape of the latest release file

The pattern `[A-Z][A-Za-z]*\d+[a-z]?` does not match `P1-1`, `P2-3` and
similar ids. `seal/releases/0.15.3.md` has 14 rows written that way, and it
is the release file most likely to be corrected next. These rows have ids to
any person who reads them, but the rule treats them as id-less. A row like
this, corrected in place while its only anchor is renamed, goes silent.

*Executed:* the probe exits 0 at the target and exits 1 once the pattern also
accepts `-\d+`. None of those 14 ids repeats within its section (a `uniq -d`
over the file found none). Other id shapes appear in 41 more rows: `S4 / S12`
and `S1–S4` (a row covering several ids), and `🔴 1`. Those rows fall back to
their anchors, which is where 🟡 3's bound statement has to describe them.

### 🟡 3: the bound is stated for one silent shape out of four, and the module docstring states none

The function docstring (`survivor_check.py:1067`) says: *What stays silent is a
row with no id whose every anchor was renamed as it was corrected.* That
sentence is true, but other rows go silent too. Every probe below exits 0 at
the target. Each of these shapes also exited 0 at `8f70ca94`, so none is a
regression inside the fix range. All of them are silent compared with the
base, and the docstring does not name them.

- A row with an id whose ledger section heading is retitled in the same range,
  with its only anchor renamed.
- A row with an id moved to another section of the same file, corrected, with
  its anchor renamed.
- A row with no id and two anchors. One anchor is renamed, and the corrected
  row drops the other anchor, which still resolves.
- A row whose id the pattern does not read (🟡 2).

Two statements a reader relies on state no bound:

- The module docstring at line 194 says: *A row corrected in place stays
  measured … even where the same range renamed its units.*
- `docs/review-chain-spec.md:924` says: *a row corrected in place is still
  read.*

About 300 anchored rows carry no id the pattern reads: 298 by this round's
survey, about 37% of the ledger. `seal/ledger.md` has 21 of them,
`seal/releases/0.4.0.md` has 83 and `seal/releases/0.12.0.md` has 37. For all
of these rows, both statements are false whenever the correction renames
every anchor it keeps.

Closing the shape for rows with no id would need a way to pair rows other than
by id, such as a one-for-one replace in the diff of the ledger's lines. That is
a design choice, and this round does not prescribe it. The fix below makes the
three documents say what the code does. With 🟡 2's pattern, it also closes the
shape for the 14 rows whose id the tree does write.

### ⬜ 4: two sentences on one line still tie on score, path and line

The sort key at `survivor_check.py:1539` ends at `row[1].line`. Two tied
candidates on the same line still print in the order `found` inserted them,
and that order comes from iterating a set of n-grams. *Executed:* one file
holds both halves of a removed sentence on a single line. Over 16 seeds, the
target printed two different outputs. Adding `row[1].raw` to the key gave one
output. The report's places and scores are unchanged, which is why this is ⬜.
The `Re-read` notes on `seal/releases/0.9.3.md` S3 (line 87) and
`seal/releases/0.15.1.md` H1 (line 105) say the order "no longer follows the
hash seed". That is true only once this key is total, and the fix below makes
it total.

### ⬜ 5: P3's closing clause claims more than its condition

This finding is a correction to the run's paperwork, at
`seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md`,
P3. The condition P3 states is exact. The clause after it (*so … a row
corrected in place, re-pointed … stays measured*) is not qualified. It is
false for the shapes 🟡 3 lists. Re-stamp P3 when 🟡 1 or 🟡 2 changes
`removed_ledger_rows`.

## Regression tests to plant

All of them go in `tests/test_a_corrected_sentence_survives_elsewhere.py`.

- 🟡 1: restore the neighbour's id to `R1` in
  `test_a_removed_row_sharing_one_live_anchor_with_another_row_takes_the_exit`.
  It went red at the target in round 1's probe, and it passes under the fix
  below (executed).
- 🟡 2: the hyphenated-id case fenced below. It exits 0 at the target, so it
  is red there, and it passes under the fix (executed as a probe).
- ⬜ 4: the same-line tie case fenced below. The target printed two outputs,
  so it is red there, and it passes under the fix (executed as a probe).

## Facts for the evidence ledger

- P3's claim should gain the count condition from 🟡 1 and the id shape from
  🟡 2. It should also end its *so* clause with the silent set 🟡 3 states,
  and its anchor should be re-stamped with that fix.
- *Executed* 2026-09-25: of the ledger's anchored rows, 298 have no id that
  `ROW_ID` reads at the target. 13 `(heading, id)` groups repeat within a
  section, all in `seal/releases/0.14.0.md` and `seal/releases/0.5.0.md`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | An id several rows share in one section (a split claim) keeps a removed row of the group measured; regression from `8f70ca94`, and the one case of the shape had its fixture changed to pass | `skills/code-review/scripts/survivor_check.py:1103` | open | Executed: shared-id probe exits 1 at target, 0 at `8f70ca94`; 13 such groups in `seal/releases/0.14.0.md` and `seal/releases/0.5.0.md`; the comment at line 1019 claims uniqueness |
| 🟡 2 | `ROW_ID` does not read the `P1-1 ·` id shape of `seal/releases/0.15.3.md` (14 rows), so those rows go silent when corrected in place with their anchor renamed | `skills/code-review/scripts/survivor_check.py:1021` | open | Executed: probe exits 0 at target, 1 with the widened pattern; no such id repeats in its section |
| 🟡 3 | The silent set is wider than the function docstring's stated bound, and the module docstring and `docs/review-chain-spec.md:924` state the correction as always measured | `skills/code-review/scripts/survivor_check.py:194` | open | Executed: section retitled, row moved section, id-less row renamed and narrowed each exit 0 at target and at `8f70ca94`; 298 anchored rows carry no id the pattern reads |
| ⬜ 4 | Two tied sentences on one line still print in hash-seed order | `skills/code-review/scripts/survivor_check.py:1539` | open | Executed: 16 seeds, two outputs at target, one with `row[1].raw` in the key; places and scores unchanged |
| ⬜ 5 | P3's closing *so* clause states the correction as always measured | `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md` | open | Read; correction to the run's paperwork, not counted in Needs a fix |
| 🟢 | round 1's finding 1 is closed for rows whose id the pattern reads under an unchanged heading | `skills/code-review/scripts/survivor_check.py:1103` | verified | Executed: five new-unit cases pass at target; the heading half of the key red when removed |
| 🟢 | round 1's finding 2 is answered by the plan sentence | `seal/specs/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction/plan.md` | answered | Read; matches `CLAUDE.md`'s REMOVED-not-re-pointed rule |
| 🟢 | round 1's finding 3 is closed for ties at distinct coordinates | `skills/code-review/scripts/survivor_check.py:1539` | verified | Executed: the 16-seed case red with the tie-break reverted; the same-line residual is ⬜ 4 |
| 🟢 | round 1's finding 4, P3 corrected and re-stamped | `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md` | verified | Executed: `bin/evidence-check .` exit 0 at target; the closing clause is ⬜ 5 |
| 🟢 | round 1's confirmations of #591, #592 and the missing-checker refusal | `skills/code-review/scripts/survivor_check.py` | verified | Read: the fix range does not touch `corrected`, `paired_across_paths` or `evidence`; executed: `58629718` exits 0 against 52 at target |

## Paste-ready fixes

### 🟡 1 and 🟡 2: `ROW_ID` and `removed_ledger_rows`

```python
import argparse
import collections
import importlib.util
```

```python
# A row's own id -- `R1`, `S3`, `G5`, `P1-1` -- heads its first cell, before
# the ` · ` that opens the claim. A row corrected in place keeps it under the
# same heading, whatever its anchors did. It is not always unique inside its
# section: a claim split across rows repeats it (`seal/releases/0.14.0.md`'s
# G5 is four rows), so an id names a row only while as many rows carry it at
# `b` as did at `a`.
ROW_ID = re.compile(r"^\s*\|\s*([A-Z][A-Za-z]*\d+[a-z]?(?:-\d+)?)\s*·")
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
        named[path] = collections.Counter(
            (heading, row_id)
            for _number, heading, row_id, _line in ledger_rows(lines, live_lines)
            if row_id
        )
        at_left = ledger_rows(before[path].splitlines(), live_lines)
        held = collections.Counter(
            (heading, row_id) for _number, heading, row_id, _line in at_left if row_id
        )
        kept = set(lines)
        for number, heading, row_id, line in at_left:
            if line in kept:
                continue
            # The same id under the same heading at `b`, carried by as many
            # rows as at `a`, is this row corrected in place -- measured
            # whatever its anchors did. A key standing fewer times at `b` lost
            # a row, and the id cannot say which, so its rows fall back to
            # their anchors.
            key = (heading, row_id)
            if row_id and named[path][key] >= held[key]:
                continue
            anchors = cited(line)
            if anchors:
                rows.append((path, number, anchors))
```

```python
    neighbour = ledger_row("A neighbouring claim.", ("pkg/mod.py#other",))
```

```python
def test_a_hyphenated_id_corrected_while_its_anchor_is_renamed_is_a_correction(
    tmp_path,
):
    """`seal/releases/0.15.3.md` writes ids as `P1-1 ·`. A row with that id,
    corrected in place and re-pointed at the renamed unit, is the same row.
    Red at 66df04df: exit 0."""
    repo = tmp_path / "probe"
    renamed = MODULE.replace("def helper(", "def helper_renamed(")
    head = ledger_range(
        repo,
        ledger_row(REPAIRED, ("pkg/mod.py#helper_renamed",)).replace(
            "R1 ·", "P1-1 ·"
        ),
        renamed,
        ledger_before=LEDGER_HEAD + ledger_row(FOUND).replace("R1 ·", "P1-1 ·"),
    )
    code, text = run("--range", f"{head}^..{head}", "--root", str(repo))
    assert code == 1, f"a hyphenated id did not keep its row measured:\n{text}"
    assert coordinates_in(text) == {"docs/x.md:3"}, text
```

### 🟡 3: the bound, stated where each reader meets it

Function docstring, replacing its last two sentences:

```text
    heading retitled. A row with no id the pattern reads falls back to its
    anchors: it still stands where a live row of the file cites every anchor
    of it that still resolves. So what stays silent is a row corrected in
    place, with an anchor renamed or gone, that the id does not name -- it
    has no id `ROW_ID` reads, its section heading changed or it moved
    section in the same range, or its id lost a sibling row -- and whose
    corrected line cites no still-resolving anchor of it, or drops one."""
```

Module docstring, replacing *A row corrected in place stays measured, because
that is the one ledger act that IS a correction -- even where the same range
renamed its units or retitled a heading it cites, as #589's did --*:

```text
A row corrected in place stays measured,
because that is the one ledger act that IS a correction -- even where the
same range renamed its units or retitled a heading it cites, as #589's did,
provided its id stands under the same heading. A row the id does not name
falls back to its anchors, and goes silent when the correction renamed every
anchor it kept (`removed_ledger_rows` states the whole set) --
```

`docs/review-chain-spec.md:924`:

```text
went with the code; a row corrected in place is still read, unless it
carries no id the sweep reads and the same range renamed every anchor it
kept. In a `.py` file only
```

### ⬜ 4: a total tie order

```python
    return sorted(
        found.values(),
        key=lambda row: (-row[0], row[1].path, row[1].line, row[1].raw),
    )
```

```python
def test_two_tied_sentences_on_one_line_print_in_one_order_whatever_the_hash_seed(
    tmp_path,
):
    """Two tied candidates on the same line of one file. Red at 66df04df:
    two outputs over 16 seeds."""
    repo = tmp_path / "probe"
    os.makedirs(repo)
    removed = (
        "Alpha bravo charlie delta echo foxtrot golf hotel india juliet kilo "
        "lima mike november oscar papa."
    )
    build(
        repo,
        {
            "docs/a.md": f"# a\n\n{removed}\n",
            "docs/c.md": "# c\n\nAlpha bravo charlie zulu india juliet kilo. "
            "Echo foxtrot golf zulu mike november oscar.\n",
            **FILLER,
        },
        "a sentence, and one line carrying both halves of it",
    )
    head = build(repo, {"docs/a.md": "# a\n\nNothing here now.\n"}, "remove it")
    outputs = set()
    for seed in range(16):
        out = subprocess.run(
            [
                sys.executable,
                SCRIPT,
                "--range",
                f"{head}^..{head}",
                "--root",
                str(repo),
            ],
            cwd=ROOT,
            capture_output=True,
            encoding="utf-8",
            env={**os.environ, "PYTHONHASHSEED": str(seed)},
        )
        assert out.returncode == 1, out.stdout + out.stderr
        outputs.add(out.stdout)
    assert len(outputs) == 1, outputs
```

### ⬜ 5: P3

```text
P3's claim: after "carries its row id", insert ", counted -- an id the tip
carries fewer times under that heading than the left end did names no row";
and end the "so" clause "... stays measured where its id stands under the same
heading or a live row cites every anchor of it that still resolves". Re-stamp
`removed_ledger_rows` with 🟡 1's fix, with a Corrected note naming this round.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -k` over the five fix-range cases, at `66df04df`, in the round's clone | 5 passed |
| Mutation A: `score`'s key reduced to `-row[0]`, then the 16-seed case | 1 failed. The case pins the tie order |
| Mutation B: heading dropped from the id's key (both halves), then the five cases | `test_a_removed_rows_id_standing_in_another_section_is_another_row` failed, 4 passed |
| Probe file of nine cases (`ledger_range` helpers), at `66df04df` | shared-id removed row exit 1; id reused by a new row exit 1; section retitled exit 0; row moved section exit 0; no id and anchor renamed exit 0; `P1-1 ·` id exit 0; no id, renamed and narrowed exit 0; control (no id, one renamed, other kept) exit 1; same-line tie 2 outputs over 16 seeds |
| The same probe file with `survivor_check.py` from `8f70ca94` | shared-id exit 0; id reused exit 0; control exit 1; the five silent shapes exit 0 as at target; same-line tie 2 outputs |
| The candidate fix (count guard, widened `ROW_ID`, `raw` in the sort key, neighbour back to `R1`) applied in the clone: the module and the probe file | 151 passed, 5 failed. The module passes all 147. The five failures are the shapes 🟡 3 states as the bound, plus the id reuse this report accepts |
| `survivor_check.py --range 58629718^..58629718`, at target and under the candidate fix | exit 0, 360 files, 52 sentences, both ways |
| `bin/evidence-check .` at target | exit 0 |
| Survey of every ledger file at target: rows per `(heading, id)`, id-less anchored rows, id shapes `ROW_ID` misses | 13 repeated groups (0.14.0.md, 0.5.0.md); 298 anchored rows with no id read; 55 rows whose first cell carries an id-like prefix the pattern misses, 14 of them `P1-1` in 0.15.3.md |
| The broad gate: full suite, repository-wide lint and typecheck | not yet. Nobody has run it. It is the sealer's, and it is not due while this round leaves 🟡 open |

```python
# The shared-id probe, as run (test_tmp file, deleted with the clone).
def test_tmp_shared_id_removed_row(tmp_path):
    other = ledger_row("A second half of the same claim.", ("pkg/mod.py#other",))
    code = go(tmp_path / "p", LEDGER_HEAD + ledger_row(FOUND) + other,
              LEDGER_HEAD + other, KEPT_MODULE)
    assert code == 0  # exit 1 at 66df04df, exit 0 at 8f70ca94
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1 (a shared id keeps a removed row measured), 🟡 2 (the `P1-1` id shape is not read), 🟡 3 (the silent set is stated narrower than it is, and not at all in the module docstring or `docs/review-chain-spec.md`).

Loses a record or crashes: no

## Proof block

Files opened this round, all at `66df04df` in the round's clone unless noted:

- `seal/specs/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction/rounds/round-1.md`, in the worktree
- `skills/code-review/scripts/survivor_check.py`: lines 170–215, 990–1130, 775–800, 1490–1580
- `tests/test_a_corrected_sentence_survives_elsewhere.py`: the fix range's diff, lines 85–115, 3570–3580, 4115–4140
- `seal/releases/0.14.0.md` lines 36–44 and `seal/releases/0.5.0.md` lines 204–222, the repeated ids
- `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md`: P3
- `seal/specs/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction/changelog.md`
- `docs/review-chain-spec.md` lines 918–930
- `bin/test`, head
- the fix range's diff of `plan.md`, `overview.md`, `seal/releases/0.15.1.md` and `seal/releases/0.9.3.md`

The round's clone and its probe files have been removed.
