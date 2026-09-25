# 1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction — review round 2

| Field | Value |
|---|---|
| Target SHA | 66df04dfe74d6eefc073339c7ea69f9b8f7b331f |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 609 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a shared id keeps a removed row measured), 🟡 2 (the `P1-1` id shape is not read), 🟡 3 (the silent set is stated narrower than it is, and not at all in the module docstring or `docs/review-chain-spec.md`). |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2 of work item 1790297084 is the verifying round over round 1's fixes (166ceb65..a98929d3) at 66df04df. For each round-1 verdict closed as fixed or answered, it asks whether it is actually closed. It reads the units the fixes created, ROW_ID and ledger_rows among them, as a finding surface, and probes the row-id rule in both directions against the ledgers as they stand.

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
```text
    heading retitled. A row with no id the pattern reads falls back to its
    anchors: it still stands where a live row of the file cites every anchor
    of it that still resolves. So what stays silent is a row corrected in
    place, with an anchor renamed or gone, that the id does not name -- it
    has no id `ROW_ID` reads, its section heading changed or it moved
    section in the same range, or its id lost a sibling row -- and whose
    corrected line cites no still-resolving anchor of it, or drops one."""
```
```text
A row corrected in place stays measured,
because that is the one ledger act that IS a correction -- even where the
same range renamed its units or retitled a heading it cites, as #589's did,
provided its id stands under the same heading. A row the id does not name
falls back to its anchors, and goes silent when the correction renamed every
anchor it kept (`removed_ledger_rows` states the whole set) --
```
```text
went with the code; a row corrected in place is still read, unless it
carries no id the sweep reads and the same range renamed every anchor it
kept. In a `.py` file only
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/survivor_check.py:1083` | round 1's 🟡 1 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1501` | round 1's ⬜ 3 — fixed |
| round-1 | `seal/ledger/1790297084-the-sweep-reads-removed-and-moved-text-as-a-correction.md` | round 1's ⬜ 4 — answered |
| round-1 | `skills/code-review/scripts/survivor_check.py:1273` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1341` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1003` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
