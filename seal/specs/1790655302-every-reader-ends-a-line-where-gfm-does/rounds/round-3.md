# 1790655302-every-reader-ends-a-line-where-gfm-does — review round 3

| Field | Value |
|---|---|
| Target SHA | c7fef45f4d42569cc9e04a5c89cdf47726975740 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #675 — https://github.com/MichaelYcJo/SpecSeal/pull/675 |
| Broad gate | 7ffa520c against cd56113c |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 (a rider read on a line the hasher cuts runs on past it by the reader's own tests, so its stamp is hashed and `--reverify` never settles it) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, verifying and the run's last, over round 2's fix range `81a770bb..0fd554dd` at HEAD `c7fef45f`. Asked whether each of round 2's three verdicts is closed, with pushes on the recursive `comment_blocks` call's termination and its reach over files with no mid-line marker, and on the byte shapes CRLF, lone CR and CRLF with a form feed. Also asked two questions the fix pass carried: whether `gather_changelog.py`'s default-mode read and write is a defect in this item's class, and whether the raw U+2028 in `rounds/round-1.md` is ⬜ 5's defect again.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A rider whose marker piece round 2's fix now reads, on a line the hasher cuts, runs on past that line by the reader's own `-->` and comment-kind tests, so its stamp is hashed into the region it names and `--reverify` never makes it read ok | `.github/scripts/rider_check.py:339` | deferred #682 | Markdown rider behind a closed comment and U+2028: at `7c339169` 0 read. At `c7fef45f` 1 drifted after every `--reverify`. Fuzz over 13,237 texts: a read rider's marker or stamp off the cut in 0 texts at `7c339169` and 4 at `c7fef45f`. Deriving `riders_in` from the hasher's blocks brings it to 0, changes no text without the eight characters, and passes 193 cases |
| ⬜ 2 | G13 says every rider the reader reads is one `region_lines` cuts before the hash, which 🟡 1's two shapes make false | `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md:21` | deferred #682 | Executed under 🟡 1. True by construction once 🟡 1's fix lands and G13 is re-read. A correction to the run's paperwork, not a fix |
| 🟢 | round 2's finding 1 is closed — a rider behind a comment on its GFM line, or behind a second rider on it, is read | `.github/scripts/rider_check.py:339` | confirmed | The three parameters fail at `7c339169` and pass at HEAD. Recursion depth one, no error over 13,237 texts. No text without the eight characters, none of the 576 prefixes and none of 25 tree files changes riders. What the reader runs on from the piece is this round's finding 1 |
| 🟢 | round 2's finding 2 is closed — `write_block` keeps CRLF and lone-CR files byte for byte | `.github/scripts/rider_check.py:604` | confirmed | Six shapes byte-exact, mixed endings included. The write reverted fails the CRLF shape on a simulated CRLF platform |
| 🟢 | round 2's finding 3 is closed — G15 and the fragment's CRLF sentences are true | `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md:23` | confirmed | True at HEAD by the six shapes. `evidence_check.py .` exits 0 |
| 🟢 | The fix pass's question: `gather_changelog.py` reading and writing in the default newline mode is outside this item's class | `.github/scripts/gather_changelog.py:413` | confirmed | LF, CRLF and lone-CR inputs give byte-identical output and identical `--check`, dry-run and refusal stdout. A simulated CRLF-platform write stages the LF blob under `* text=auto eol=lf` |
| 🟢 | The raw U+2028 and U+2029 in round 1's record are what spec S1 keeps, not ⬜ 5's defect, and no check reaches them | `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/rounds/round-1.md:78` | confirmed | Inside a fenced string constant that lists them, copied from the report. Eight gates and six record-walking test modules give the same output raw and escaped |
| ❓ | `write_block`'s write and the new cases on CI's Linux and Windows legs | `.github/scripts/rider_check.py:604` | ❓ out of verified scope | Only macOS ran here, with the CRLF platform simulated. The pull request's CI run answers it |

## Paste-ready fixes

```python
def riders_in(rel, text):
    """Every rider in TEXT, numbered on its `str.splitlines` lines.

    The blocks are the hasher's: `comment_blocks` over GFM lines, which is
    what `region_lines` cuts. Each block's pieces -- the `str.splitlines`
    lines that start inside it -- are split at every piece carrying the
    marker, so two riders on one GFM line are two riders, and a piece before
    the first marker (`# note`, a closed HTML comment) is in none. A second
    rule over the pieces is what let the reader and the hasher disagree in
    rounds 1, 2 and 3 of #664: on a line's head, on its cut, and then on a
    block's extent and its comment kind.
    """
    global _blocks
    if MARKER not in text:
        return []
    if _blocks is None:
        _blocks = load_blocks()
    pieces = text.splitlines()
    by_line = {}
    for k, (number, _head) in enumerate(gfm_places(_blocks.gfm_lines, text)):
        by_line.setdefault(number, []).append(k)
    out = []
    for a, b in comment_blocks(_blocks.gfm_lines(text), rel):
        inside = [k for number in range(a, b + 1) for k in by_line.get(number, [])]
        starts = [k for k in inside if MARKER in pieces[k]]
        for s, e in zip(starts, [*starts[1:], inside[-1] + 1], strict=True):
            out.append(Rider(rel, s + 1, e, text))
    return out
```
```python
@pytest.mark.parametrize(
    "rel, text",
    [
        (
            "doc.md",
            f"x\n{RIDER_MARK[:5]}a -->{LS}{RIDER_MARK} about a.\n{STAMP} -->\ny\n",
        ),
        (
            "mod.py",
            f"a = 1\n# note{LS}{RIDER_MARK} about a.\n"
            f"b = 2  # {'RIDER:'} about b. {STAMP} -->\n",
        ),
    ],
    ids=["closed-comment-then-break", "hash-line-read-as-html"],
)
def test_every_piece_of_a_rider_read_is_on_a_line_the_hasher_cuts(rel, text):
    """Round 3. Reading a marker piece on a line the hasher cuts is half of
    agreeing with it: the block the reader runs on from that piece has to be
    the hasher's too, or its stamp is hashed into the region it names and no
    `--reverify` makes it read ok. The characters are built from their code
    points."""
    riders = _load("specseal_riders_extent", RIDERS)
    blocks = riders.load_blocks()
    places = riders.gfm_places(blocks.gfm_lines, text)
    cut = {
        n
        for a, b in riders.comment_blocks(blocks.gfm_lines(text), rel)
        for n in range(a, b + 1)
    }
    read = riders.riders_in(rel, text)
    assert read
    for rider in read:
        lines = {places[k][0] for k in range(rider.start - 1, rider.end)}
        assert lines <= cut, (rider.start, rider.end, sorted(lines), sorted(cut))
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the item's module and `tests/test_a_rider_reaches_its_file.py`, in the clone at `c7fef45f` | 130 passed |
| Round 2's two new cases with `rider_check.py` at `7c339169` | 5 failed: the three shapes, CRLF and CR |
| Fuzz, 13,237 generated texts holding the marker, `.py`, `.yml` and `.md`, head against `7c339169` | no exception. A read rider's marker or stamp off the hasher's cut: 0 texts at `7c339169`, 4 at HEAD. Texts without the eight characters whose riders differ: 0 |
| 576-prefix differential, reader against hasher and head against `7c339169` | 0 read but not cut. 0 differ |
| Three controls, code or prose before the break | 0 riders at both, 0 cut |
| The 25 files under the rider roots that carry the marker | same riders at both. `check()`: 19 ok, 0 drifted, 0 problems |
| Markdown rider behind a closed comment and U+2028, `check` and `--reverify` twice | `7c339169`: 0 read. HEAD: 1 drifted after each `--reverify`. The control settles to 1 ok at both |
| The same shape with a second rider in the one comment | HEAD reads the second rider off the cut |
| `reverify` on six byte shapes | all byte-exact apart from the stamp. `check()` 1 ok after each |
| `write_block`'s write reverted to the default mode, on a simulated CRLF platform | CRLF and LF files no longer byte-exact. Lone CR still byte-exact |
| `gather_changelog.py` over the tree's changelog and 29 fragments, in LF, CRLF and lone CR | `--check`, `--dry-run` and the refusal: identical stdout. The written file: byte-identical |
| `gather_changelog.py` write on a simulated CRLF platform, staged in a scratch repository under `* text=auto eol=lf` | ` M` before staging, `git diff` empty, `git diff --cached` empty after, same blob as the LF write |
| Eight hygiene gates and six record-walking test modules, round 1's record and report raw and escaped | same exit codes and output. Only the printed commit abbreviation and the run time differ. The modules: 528 passed both times |
| 🟡 1's fix and case applied | 193 passed over the item's module, `test_a_rider_reaches_its_file.py` and `test_the_hooks_hide_what_a_renderer_hides.py`. The fuzz: 0 off the cut, 0 changed without the eight. 576 prefixes agree. 25 tree files unchanged. `rider_check.py --root .`: `19 ok · 0 drifted · 0 broken`, exit 0. `ruff check` and `ruff format --check` clean on both files |
| 🟡 1's case against `rider_check.py` at `c7fef45f` | 2 failed, both shapes |
| `evidence_check.py .` at `c7fef45f` | exit 0 |
| The broad gate: full suite, repository-wide lint, typecheck | not yet. That is the sealer's run, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/rider_check.py:250` | round 1's 🟡 1 — fixed |
| round-1 | `.github/scripts/rider_check.py:690` | round 1's 🟡 2 — fixed |
| round-1 | `.github/scripts/rider_check.py:579` | round 1's 🟡 3 — fixed |
| round-1 | `tests/test_every_reader_ends_a_line_where_gfm_does.py:636` | round 1's 🟡 4 — fixed |
| round-1 | `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/phases/phase-4.md:28` | round 1's ⬜ 5 — answered |
| round-1 | the 12 gate runs in *Executed probes* | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/round_record.py:1279` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/*.md`, `seal/ledger/*.md` | round 1's ❓ — out of verified scope |
| round-1 | `.github/scripts/claude_block.py:122` | round 1's ❓ — out of verified scope |
| round-2 | `.github/scripts/rider_check.py:331` | round 2's 🟡 1 — fixed |
| round-2 | `.github/scripts/rider_check.py:584` | round 2's 🟡 2 — fixed |
| round-2 | `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md:23` | round 2's ⬜ 3 — answered |
| round-2 | `.github/scripts/rider_check.py:261` | round 2's 🟢 — confirmed |
| round-2 | `.github/scripts/rider_check.py:704` | round 2's 🟢 — confirmed |
| round-2 | `.github/scripts/rider_check.py:592` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_every_reader_ends_a_line_where_gfm_does.py:637` | round 2's 🟢 — confirmed |
| round-2 | `.github/scripts/rider_check.py:596` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 1 — a rider read on a line the hasher cuts runs on past it | #682, milestone `release: 0.16.0` | the work item #682 opens, in 0.16.0 |
| ⬜ 2 — G13 false for 🟡 1's two shapes | #682 | the same work item, re-reading G13 against its fix |
