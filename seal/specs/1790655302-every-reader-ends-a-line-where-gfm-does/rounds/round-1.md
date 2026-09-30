# 1790655302-every-reader-ends-a-line-where-gfm-does — review round 1

| Field | Value |
|---|---|
| Target SHA | 260c86ac8c95bed1065f21feaa2fb92bacc05302 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #675 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `7bfea5f4b82d82322280d0f777571fe43a116dd8..21b871ef2fc7b69f460735148dcfe20bad8e9046`, 6 commits |
| Contract changes | none |
| New units | test_a_rider_behind_a_leading_break_is_still_read (depth 1); test_a_statement_between_the_rider_and_the_unit_is_read_on_asts_lines (depth 1); test_reverify_writes_a_break_inside_a_rider_back_as_it_stood (depth 1); test_reverify_leaves_a_last_rider_line_with_no_end_without_one (depth 1) |
| Needs a fix | yes — 🟡 1 (a rider behind a leading break goes unchecked), 🟡 2 (the `between` slice is unpinned), 🟡 3 (`write_block` writes a break back as LF), 🟡 4 (the class case exempts four files whole) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1, the first finding round, over the work item's own diff `3fc0c5bd...260c86ac`. Asked to test S20's byte-identical claim, coupled readers that could disagree on numbering, release scripts whose counts could change, the rider check reading a rider it should not or missing one it should, and whether the class-closing case lets a new `splitlines(` in.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A rider whose GFM line starts with one of the eight before the marker is stepped over by the reader but cut by the hasher, so its stamp is never checked and the run reads clean | `.github/scripts/rider_check.py:250` | **fixed** `fa723c22` | fixed at fa723c22 — `gfm_places` counts a piece as a line head when only whitespace stands before it on its GFM line; Probe: `.py`, `.yml` and `.md` fixtures read 1 drifted or 1 problem at base and nothing at head. The planted case failed for all eight at head and passed with the fix |
| 🟡 2 | The changed `between` slice in `inferred_anchor` has no case; reverting it to the `str.splitlines` list survives every module that covers the file | `.github/scripts/rider_check.py:690` | **fixed** `fa723c22` | fixed at fa723c22 — `inferred_anchor`'s `between` slice is pinned by a statement between the rider and the unit; Mutant survived 265 cases. A statement between rider and unit gives `x` at base and `None` at head |
| 🟡 3 | `write_block` writes a form feed or U+2028 inside a rider back as a line break on `--reverify` and `--migrate` | `.github/scripts/rider_check.py:579` | **fixed** `fa723c22` | fixed at fa723c22 — with `90dad0df` pinning the last line with no end: `write_block` gives each piece back its own line end; Probe on base and head: LF count 6 to 7, form feed gone. With the fix the form feed is kept. Pre-existing, left to F by the spec's *Out*, and in the class this item exists to close |
| 🟡 4 | The class case exempts four files whole, so a new `.splitlines(` call in `rider_check.py`, which this item edits, passes unnamed | `tests/test_every_reader_ends_a_line_where_gfm_does.py:636` | **fixed** `fa723c22` | fixed at fa723c22 — the class case names F's units with their counts instead of exempting F's files by path; Planted call in `comment_blocks` passed as shipped and failed with the replacement. The stated reason, F's merge, is past |
| ⬜ 5 | `phases/phase-4.md` holds a raw U+2028 in the sentence that says the fixture held six ASCII characters | `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/phases/phase-4.md:28` | answered | corrected at `5edae0fe`: `phases/phase-4.md` carries the escape in place of the raw character; Tracked-file scan at `260c86ac`. A correction to the run's paperwork, not a fix |
| 🟢 | S20 holds on the merged tree | the 12 gate runs in *Executed probes* | confirmed | Head code and base code over one content root matched in exit code, stdout and stderr |
| 🟢 | Coupled `round_record.py` readers agree on line numbering | `skills/code-review/scripts/round_record.py:1279` | confirmed | Every `raw` / `readable` pair reads `gfm_lines`. `swallowed`'s strict zip is reached by the S1 case, and its revert is killed |
| ❓ | The claims of the 61 ledger rows re-stamped in `seal/releases/0.4.0` to `0.15.5` and in items C's and F's fragments | `seal/releases/*.md`, `seal/ledger/*.md` | ❓ out of verified scope | `evidence-check` exits 0, so the hashes are consistent. I re-read none of the claims against the edits. The orchestrator answers whether a round reads them |
| ❓ | CI's Linux and Windows legs over the new cases, including `claude_block.py`'s `newline=""` CRLF path | `.github/scripts/claude_block.py:122` | ❓ out of verified scope | Only macOS ran here. The pull request's CI run answers it |

## Paste-ready fixes

```python
    out, at, current, opened = [], 0, 0, 0
    for piece in text.splitlines(keepends=True):
        if at in heads:
            current, opened = heads[at], at
        # A piece starts its GFM line when nothing but whitespace stands before
        # it there -- the test `comment_blocks` applies to a GFM line with
        # `lstrip`, so a rider behind a leading form feed is one to both.
        out.append((current, not text[opened:at].strip()))
        at += len(piece)
    return out
```
```python
@pytest.mark.parametrize("char", SPLITLINES_ONLY, **BY_CODE_POINT)
def test_a_rider_behind_a_leading_break_is_still_read(char):
    """Only whitespace stands before the marker on its GFM line, so
    `region_lines` cuts the block (`comment_blocks` reads `lstrip`); the
    reader must read it too, or the rider's stamp is never checked and the
    run reads clean."""
    riders = _load("specseal_riders_leading", RIDERS)
    text = f"a = 1\n{char}# {'RIDER:'} about a. {STAMP}\nb = 2\n"
    assert [(r.start, r.end) for r in riders.riders_in("mod.py", text)] == [(3, 3)]
```
```python
def test_a_statement_between_the_rider_and_the_unit_is_read_on_asts_lines():
    """A form feed inside a string above the rider puts `str.splitlines` one
    line ahead of `ast`, so a gap read from its list skipped the `print(s)`
    standing between the rider and `x`, and `x` was inferred."""
    riders = _load("specseal_riders_between", RIDERS)
    checker = riders.load_checker()
    text = (
        f"s = 'a{FF}b'\n# {'RIDER:'} about x. Verified 2026-01-01 at abcdef1\n"
        "print(s)\nx = 1\n"
    )
    rider = riders.riders_in("mod.py", text)[0]
    assert riders.inferred_anchor(checker, "mod.py", text, rider) is None
```
```python
# Every character `str.splitlines` ends a piece at, CR and LF included.
PIECE_ENDS = "\r\n\x0b\x0c\x1c\x1d\x1e\x85  "


def write_block(root, rider, body):
    path = os.path.join(root, rider.rel)
    with open(path, encoding="utf-8") as f:
        lines = f.read().splitlines(True)
    old = lines[rider.start - 1 : rider.end]
    # Each piece keeps the end it had. BODY is the pieces joined with "\n", so
    # rebuilding them with "\n" wrote a U+2028 or a form feed inside a rider
    # back as a line break (#664).
    ends = [piece[len(piece.rstrip(PIECE_ENDS)) :] for piece in old]
    replacement = [
        piece + end for piece, end in zip(body.split("\n"), ends, strict=True)
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("".join(lines[: rider.start - 1] + replacement + lines[rider.end :]))
```
```python
def test_reverify_writes_a_break_inside_a_rider_back_as_it_stood(tmp_path):
    """`Rider.body` joins the pieces with LF, and `write_block` used to write
    them back with LF, so a form feed inside a rider became a line break."""
    riders = _load("specseal_riders_writeback", RIDERS)
    (tmp_path / "hooks").mkdir()
    path = tmp_path / "hooks" / "mod.py"
    text = (
        "def g():\n    return 1\n\n\n"
        f"# {'RIDER:'} about x. Verified 2026-01-01 against x@deadbeef{FF}# more\n"
        "x = 1\n"
    )
    path.write_text(text, encoding="utf-8")
    written, refused = riders.reverify(str(tmp_path), roots=("hooks",), today="2026-09-29")
    assert len(written) == 1 and refused == []
    after = path.read_text(encoding="utf-8")
    assert FF in after
    assert after.count("\n") == text.count("\n")
```
```python
# Work item F's units, named one by one now that F has landed: exempting its
# files whole let any new call in them through, `gfm_places` included.
OUT_OF_CLASS.update(
    {
        (".github/scripts/rider_check.py", "Rider.__init__"): (1, F),
        (".github/scripts/rider_check.py", "gfm_places"): (
            1,
            "the pieces `riders_in` reads, each placed on the GFM line it starts in",
        ),
        (".github/scripts/rider_check.py", "main"): (1, "the docstring's first line"),
        (".github/scripts/rider_check.py", "riders_in"): (1, F),
        (".github/scripts/rider_check.py", "write_block"): (2, F),
        ("hooks/blocks.py", "walk_text"): (1, F),
        ("hooks/config.py", "config_rows"): (1, F),
        ("hooks/config.py", "refusal"): (1, F),
        ("hooks/routing.py", "table_rows"): (1, F),
    }
)
```
```python
    found = splitlines_calls()
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the item's module and `tests/test_a_rider_reaches_its_file.py`, in the clone at `260c86ac` | 57 passed for the item's module alone. 106 passed for the two together |
| S20 probe: 12 gate runs from head code and from base code, the 13 moved files at `3fc0c5bd`, over head's content root | identical in all 12. `survivor-check` over `551c7967...260c86ac` and `chain-check` exit 1 on both sides |
| Reader over every tracked file: head `readable` and `live_lines(gfm_lines)` against base's `splitlines` forms | differ on three files: item C's round 1 report, item F's round 1 report, and this item's `phases/phase-4.md` |
| Rider probe, a leading break before the marker: `.py`, `.yml` and `.md`, base against head | base reads each rider. Head reads none, and `check` reports 0 drifted and 0 problems |
| Write-back probe, `reverify` on a `.py` rider holding a form feed | base and head: form feed lost, LF count 6 to 7. With the fix: kept, 6 to 6 |
| Mutants, one per moved call site, against the item's module and `test_the_record_is_generated.py`, with `PYTHONDONTWRITEBYTECODE=1` | 16 of 17 killed. `inferred_anchor`'s `between` survived (finding 2) |
| The same mutants with the S19 count case deselected, adding `test_chain_hooks.py` and `test_a_document_has_room_for_the_next_fold.py` | the seven `round_record.py` sites named in *The account* and `between` survived. `readable`, `swallowed`, `build`'s `raw`, fold-check's ceiling, the sweep's ledger split, the gatherer's index, the rider step-over, the anchor's `below` and the transcript tail were killed |
| `inferred_anchor` on a statement between the rider and the unit | base answers `x`. Head answers `None` |
| The class case as shipped, with a planted call in `comment_blocks` | passed (finding 4) |
| The class case with finding 4's replacement: once plain, once with the plant | plain: 57 passed. With the plant: failed, naming the unit |
| Findings 1 and 4 fixes and both new cases applied together | 115 passed over the item's module and `tests/test_a_rider_reaches_its_file.py`. `rider_check.py --root .` reads 19 ok |
| The broad gate: full suite, repository-wide lint, typecheck | not yet. That is the sealer's run, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
