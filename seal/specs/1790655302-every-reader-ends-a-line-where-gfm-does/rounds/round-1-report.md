# 1790655302-every-reader-ends-a-line-where-gfm-does — round 1 report

| Field | Value |
|---|---|
| Round | 1 |
| Target | `fix/664-every-reader-ends-a-line-where-gfm-does` at `260c86ac`, diff `3fc0c5bd...260c86ac` |
| Reviewed by | specseal:warden on claude-opus-5-5, in a `git clone --no-local` of the target |
| Earlier rounds | none |

## What this round found, in the order one causes the next

1. Phase 6 steps over a marker line that does not start its GFM line. The
   test it uses is wrong for one shape, so a rider behind a leading break is
   now invisible to the check (finding 1).
2. The phase 6 fix of `inferred_anchor` has one changed line that no case
   pins (finding 2).
3. `rider_check.py` still holds the class's write-back instance, in
   `write_block` (finding 3).
4. The class case exempts `rider_check.py` and three F files whole, so a new
   `.splitlines(` call in any of them, this item's own `gfm_places` among
   them, passes unnamed (finding 4). That is why nothing in the tree pointed
   at finding 3.
5. One of this item's own phase records holds a raw U+2028 (finding 5,
   paperwork).

Everything the prompt named as a way a record could leave the root held
when I checked it. S20 held on the merged tree for 12 gate runs (executed).
The coupled `round_record.py` pairs agree, and `swallowed`'s strict zip
still holds. The release scripts' counts and refusals did not move on this
tree.

## Findings from execution

### 🟡 1 — A rider behind a leading break is no longer read, and the check reads clean

`.github/scripts/rider_check.py:250` (`gfm_places`) and `:318–322`
(`comment_blocks`).

`gfm_places` calls a piece a head only when it starts exactly at a GFM
line's first byte (`at in heads`). The hasher's side does not use that
rule. `region_lines` hands `comment_blocks` the GFM lines, and
`comment_blocks` opens a block on `line.lstrip()`, which strips a form feed,
U+2028 and the other six. That is Python's own rule too: a form feed in a
line's indentation is legal. Suppose a rider's line is a form feed, or any
of the eight, and then `#` and the marker. The hasher cuts that line out of
the region as a rider block, and the reader now steps over it because the
piece does not start at the GFM line's first byte. The rider is read by
nobody. Its stamp is never compared, and the run prints `0 drifted`.

Before this branch the reader read that rider. The drift reached the report.

Executed (probe, head code against base code on the same fixtures, with a
drifted stamp):

| Fixture | base | head |
|---|---|---|
| `.py`, a form feed then the `#` rider, on one line | reader (5, 5), 1 drifted | reader none, 0 drifted, 0 problems |
| `.yml`, the same | reader (3, 3), 1 drifted | reader none, 0 drifted, 0 problems |
| `.md`, a U+2028 then the HTML rider | reader (8, 8), 1 problem | reader none, 0 problems |
| `.py`, the form feed on the line above (control) | 1 drifted | 1 drifted |

Why it matters: this is the silent direction of the gate the phase exists
to harden. No file in the tree has this shape today, so the defect is
latent. The fix below goes back to exactly the rule the hasher applies.

Planted against head, the regression case under §*Regression tests to
plant* failed for all eight characters. With the fix it passed, and so did
the item's module and `tests/test_a_rider_reaches_its_file.py` (115 passed,
executed). With the fix, `rider_check.py --root .` on the tree still reads
19 ok.

### 🟡 2 — The `between` line of `inferred_anchor` is pinned by no case

`.github/scripts/rider_check.py:689–690`.

The phase 6 spawn asked for one mutant killed per changed branch. I
reverted `between` to `text.splitlines()[rider.end : first[0] - 1]` and it
survived the item's module, `test_the_record_is_generated.py`,
`test_chain_hooks.py` and `test_a_document_has_room_for_the_next_fold.py`
(265 passed, executed). The gap case gives the same answer either way,
because its gap is blank on both numberings.

A shape that tells them apart: a form feed inside a string above the rider,
and a `print(s)` statement between the rider and `x = 1`. At `3fc0c5bd`,
`inferred_anchor` answers `x`, so `--migrate` would put a hash behind a
claim nobody made. At head it answers `None`, which is right. The mutant
answers `x` (executed, direct call on both trees).

The code is right. The fix is the missing pin, so the next edit cannot
quietly take it back.

## Findings from reading, confirmed by execution

### 🟡 3 — `--reverify` and `--migrate` write a break inside a rider back as a line break

`.github/scripts/rider_check.py:573–583` (`write_block`), with
`Rider.__init__` at `:374`.

`Rider.body` joins the rider's `str.splitlines` pieces with `"\n"`.
`write_block` then writes `body.splitlines()` back with `"\n"` after each
one. A form feed or U+2028 inside a rider becomes a real line break in the
file. That is the class's write-back symptom, the one spec §*The class*
names ("the character turned into a line break").

Phase 6's own case shape triggers it: a `#` rider whose last line carries
`{FF}# more`. `reverify` on that file raised the file's LF count from 6 to
7 and dropped the form feed. That happened on base and on head alike
(executed). With the fix below, the form feed is kept and the count stays
at 6.

This defect is not introduced here. The spec's *Out* table left
`write_block` to F "(F's files)". F has landed without touching it, and
phase 6 then took `rider_check.py` into this item. #664 is the class, and
this is its last write-back reader. I report it at the severity it has,
and the orchestrator decides whether it is fixed here or deferred to a
named home.

### 🟡 4 — The class case lets a new `.splitlines(` into four files, one of which this item edits

`tests/test_every_reader_ends_a_line_where_gfm_does.py:633–641` and `:681`.

`F_FILES` exempts `hooks/config.py`, `hooks/routing.py`, `hooks/blocks.py`
and `.github/scripts/rider_check.py` by path. The reason in the comment,
"a count pinned here would redden on F's merge", stopped being true when F
merged at `3fc0c5bd`. The exemption now covers a file this item edited:
`gfm_places` added a `text.splitlines(keepends=True)` call, and no
`OUT_OF_CLASS` row names it.

I planted `(text or '').splitlines()` in `comment_blocks` and ran the case
as shipped. It passed (executed). With the replacement below it failed,
naming `('.github/scripts/rider_check.py', 'comment_blocks')`. Without the
plant, the module passed, 57 cases (executed).

The spec's S19 scoped the case to "outside F's files". So this is the
frame's scope going stale when F merged, and phase 6 never re-drew it.
Finding 3 is what that cost.

## Paperwork

### ⬜ 5 — `phases/phase-4.md` holds the character its sentence says it cannot

`seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/phases/phase-4.md:28`.

The line reads "holds `<U+2028>` as six ASCII characters". The code span
holds the raw U+2028, not the six characters the sentence describes, so the
sentence is false as written. A scan of every tracked file at `260c86ac`
finds the eight characters in three files: this one, item C's
`rounds/round-1-report.md` (spec M1), and item F's
`seal/specs/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule/rounds/round-1-report.md`
(five lines, all inside quoted code). No gate's output moved because of
them (S20 below). This is a correction to the run's paperwork. It is not a
fix.

## The account, checked

| The account claimed | What I found |
|---|---|
| S20: every moved gate prints the same bytes on this tree as at base | Held on the merged tree. I ran each gate from head code and from base code (the 13 moved files checked out at `3fc0c5bd`) over one content root, head's. All 12 runs matched in exit code, stdout and stderr: `unverified-check` (plain and `--baseline`), `survivor-check` on two ranges, `correction-check`, `fold-check`, `evidence-check`, `chain-check`, `payload-meter --sections --json`, the gatherer's `--dry-run` for 0.16.0, `rider_check.py` and `claude_block.py --check`. `survivor-check` over `551c7967...260c86ac` and `chain-check` exit 1 on both sides alike |
| Phase 1: over every tracked file only item C's report differs between the splits | True at `2e392d46`, where it was measured. At `260c86ac`, `readable` and `live_lines` also differ on item F's round 1 report and on this item's `phase-4.md` (finding 5). No gate output changed |
| Coupled readers move together; `swallowed` zips with `strict=True` | Confirmed. Every `raw` / `readable` pair in `round_record.py` reads `gfm_lines`. Reverting `readable` alone, `swallowed` alone, or `build`'s `raw` alone each failed a behavioural case (executed) |
| One mutant per moved call site, killed | True, but for seven sites the only killer is the S19 count case: `open_hider`, `hiders_close`, `inherited_rows`, `reach_forward`, `reach_back`, `close` and `seal` in `round_record.py`. With that case deselected, each revert to `splitlines` survived 265 cases (executed). I do not raise this as a finding: a `split("\n")` partner is equivalent on text read through `open()`, and the count case does catch the realistic regression |
| `claude_block` and the transcript tails stay on LF alone | Confirmed by reading and by the S15 and S16 cases. `worktree-guard`'s tails decode bytes, so a CRLF record keeps a CR that `json.loads` accepts as whitespace |
| The release scripts' counts and refusals do not change on a real release | The gatherer's dry run for 0.16.0, `fold-check` and `survivor-check` matched base on this tree (executed). The `insert` index fix is pinned by S5 and by the lone-CR case, and its mutant was killed (executed) |
| The class case names every remaining `splitlines(` call | Outside the four `F_FILES`, yes (57 passed, executed). Inside them, no (finding 4) |

## Regression tests to plant

All three go into `tests/test_every_reader_ends_a_line_where_gfm_does.py`,
below the phase 6 cases. The first two are fenced under finding 1 and
finding 2. The third is fenced under finding 3. I saw the first fail for all
eight characters at head and pass with the fix. The second passes at head,
and the direct call on base code answers `x`, the answer it rejects. I did
not plant the third as a pytest case. Its fixture was run as a probe on
base and head, and with the fix (see *Executed probes*).

## Facts for the evidence ledger

- `rider_check.py#region_lines` hands `comment_blocks` GFM lines, and
  `comment_blocks` opens a block on `lstrip()`, so a line whose only prefix
  before `#` or the HTML opener is whitespace (including the eight) is a
  rider block to the hasher. Read at `260c86ac`.
- `rider_check.py#write_block` rebuilds the rider's lines from `Rider.body`
  with `"\n"`, so a break inside a rider becomes an LF on write. Executed at
  `3fc0c5bd` and `260c86ac`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A rider whose GFM line starts with one of the eight before the marker is stepped over by the reader but cut by the hasher, so its stamp is never checked and the run reads clean | `.github/scripts/rider_check.py:250` | open | Probe: `.py`, `.yml` and `.md` fixtures read 1 drifted or 1 problem at base and nothing at head. The planted case failed for all eight at head and passed with the fix |
| 🟡 2 | The changed `between` slice in `inferred_anchor` has no case; reverting it to the `str.splitlines` list survives every module that covers the file | `.github/scripts/rider_check.py:690` | open | Mutant survived 265 cases. A statement between rider and unit gives `x` at base and `None` at head |
| 🟡 3 | `write_block` writes a form feed or U+2028 inside a rider back as a line break on `--reverify` and `--migrate` | `.github/scripts/rider_check.py:579` | open | Probe on base and head: LF count 6 to 7, form feed gone. With the fix the form feed is kept. Pre-existing, left to F by the spec's *Out*, and in the class this item exists to close |
| 🟡 4 | The class case exempts four files whole, so a new `.splitlines(` call in `rider_check.py`, which this item edits, passes unnamed | `tests/test_every_reader_ends_a_line_where_gfm_does.py:636` | open | Planted call in `comment_blocks` passed as shipped and failed with the replacement. The stated reason, F's merge, is past |
| ⬜ 5 | `phases/phase-4.md` holds a raw U+2028 in the sentence that says the fixture held six ASCII characters | `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/phases/phase-4.md:28` | open | Tracked-file scan at `260c86ac`. A correction to the run's paperwork, not a fix |
| 🟢 | S20 holds on the merged tree | the 12 gate runs in *Executed probes* | confirmed | Head code and base code over one content root matched in exit code, stdout and stderr |
| 🟢 | Coupled `round_record.py` readers agree on line numbering | `skills/code-review/scripts/round_record.py:1279` | confirmed | Every `raw` / `readable` pair reads `gfm_lines`. `swallowed`'s strict zip is reached by the S1 case, and its revert is killed |
| ❓ | The claims of the 61 ledger rows re-stamped in `seal/releases/0.4.0` to `0.15.5` and in items C's and F's fragments | `seal/releases/*.md`, `seal/ledger/*.md` | ❓ out of verified scope | `evidence-check` exits 0, so the hashes are consistent. I re-read none of the claims against the edits. The orchestrator answers whether a round reads them |
| ❓ | CI's Linux and Windows legs over the new cases, including `claude_block.py`'s `newline=""` CRLF path | `.github/scripts/claude_block.py:122` | ❓ out of verified scope | Only macOS ran here. The pull request's CI run answers it |

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

## Paste-ready fixes

### 🟡 1 — `gfm_places` calls a piece a head the way `comment_blocks` does

In `.github/scripts/rider_check.py`, replace the second loop of
`gfm_places`:

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

The docstring's "(the 1-based GFM line it starts in, whether it starts that
line)" then reads "whether only whitespace stands before it on that line".
The comment_blocks docstring paragraph "A marker line that starts inside a
GFM line" gains "after something other than whitespace". Case:

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

### 🟡 2 — pin the `between` slice

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

### 🟡 3 — `write_block` keeps each piece's own end

In `.github/scripts/rider_check.py`, above `write_block`, and replacing its
body:

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

`restamp` writes no `"\n"`, so `body.split("\n")` has one element per piece.
A last piece with no end keeps none, which is what the old `ending` branch
did by hand. Case:

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

With this fix, `write_block` makes one `.splitlines(` call, not two, so
finding 4's row for it reads `(1, F)`.

### 🟡 4 — name F's units instead of exempting F's files

In `tests/test_every_reader_ends_a_line_where_gfm_does.py`, replace the
`F_FILES` block:

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

and in the case:

```python
    found = splitlines_calls()
```

Needs a fix: yes — 🟡 1 (a rider behind a leading break goes unchecked), 🟡 2 (the `between` slice is unpinned), 🟡 3 (`write_block` writes a break back as LF), 🟡 4 (the class case exempts four files whole)
Loses a record or crashes: no

The broad gate is not due yet: this round leaves four findings open.

## Proof block

Files opened this round, all in the clone at `260c86ac` unless named:

- `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/overview.md`, `spec.md`, `phases/phase-6.md`, and parts of `phases/phase-1.md`, `phase-4.md` and `phase-5.md`
- the diff `3fc0c5bd...260c86ac` of every file under `.github/scripts`, `hooks` and `skills`, and of `tests/test_chain_hooks.py` and `tests/test_a_document_has_room_for_the_next_fold.py`
- `tests/test_every_reader_ends_a_line_where_gfm_does.py`, whole
- `.github/scripts/rider_check.py`, lines 138–757
- `skills/evidence-check/scripts/evidence_check.py`, `py_spans` and `resolve_unit` heads
- `skills/verify/scripts/payload_meter.py#_fence_rule`, `hooks/worktree-guard.py`'s two tail reads, `skills/code-review/scripts/survivor_check.py:585–595`
- the argument parsers of the 11 gate scripts, `bin/survivor-check`, and `.github/scripts/run_tests.py`'s `FLOOR`
- `CONTRIBUTING.md`'s headings and its *Running the checks* lines
