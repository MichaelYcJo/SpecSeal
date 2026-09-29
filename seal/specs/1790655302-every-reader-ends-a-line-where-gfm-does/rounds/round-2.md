# 1790655302-every-reader-ends-a-line-where-gfm-does — review round 2

| Field | Value |
|---|---|
| Target SHA | 7c3391691d656aed15ca14e47adad3d23f8195c2 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #675 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a rider behind a comment on its GFM line is cut by the hasher and read by nobody), 🟡 2 (`write_block` writes a CRLF file back as LF) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 2, verifying, over round 1's fix diff `7bfea5f4..21b871ef` at HEAD `7c339169`. Asked whether each verdict round 1 closed is closed, with three pushes: `gfm_places` against the hasher's `lstrip` on every leading whitespace, `write_block` keeping every line end byte for byte, and any `splitlines(` still slipping past the class case.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A rider behind a comment on its GFM line, or behind a second rider on that line, is cut by the hasher and stepped over by the reader, so its stamp is compared by nobody and the run reads clean | `.github/scripts/rider_check.py:331` | open | `check()` on a `.py` fixture: base 1 drifted, head 0 drifted and 0 problems. The `.yml` and `.md` shapes are read at base and unread at head, while the hasher cuts each. The fix reads all three, and the controls stay stepped over |
| 🟡 2 | `write_block` reads and writes in the default newline mode, so a CRLF or lone-CR file comes back LF throughout, while the fix's comment says each piece keeps its end | `.github/scripts/rider_check.py:584` | open | `reverify` probe: CRLF 6 to 0, lone CR 6 to 0. With `newline=""` on both opens every byte is kept, and the planted case is red with the read reverted |
| ⬜ 3 | Ledger row G15 and the changelog fragment say a CRLF rider keeps its CR | `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md:23` | open | False at `21b871ef` by the probe under 🟡 2. True once 🟡 2's fix lands and G15 is re-read. A correction to the run's paperwork, not a fix |
| 🟢 | round 1's finding 1 is closed — a rider behind leading whitespace, the eight breaks included, is read again | `.github/scripts/rider_check.py:261` | confirmed | 16 new cases red at `7bfea5f4`. The 576-prefix differential agrees. The same class through a comment prefix is this round's finding 1 |
| 🟢 | round 1's finding 2 is closed — the `between` slice is pinned | `.github/scripts/rider_check.py:704` | confirmed | The mutant reverting `between` fails the new case |
| 🟢 | round 1's finding 3 is closed — a form feed or U+2028 inside a rider is written back as it stood | `.github/scripts/rider_check.py:592` | confirmed | The new case is red at `7bfea5f4`. The last-line case is red against a mutant. CRLF is this round's finding 2 |
| 🟢 | round 1's finding 4 is closed — the class case names F's units one by one | `tests/test_every_reader_ends_a_line_where_gfm_does.py:637` | confirmed | A second call in `riders_in` and a module-level call in `hooks/routing.py` each fail the case |
| 🟢 | round 1's finding 5 is closed — `phases/phase-4.md` holds no raw U+2028 | `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/phases/phase-4.md:28` | confirmed | Count of U+2028 in the file at `7c339169`: 0 |
| ❓ | `write_block`'s default-mode write on a platform whose separator is CRLF, and the new cases on CI's Linux and Windows legs | `.github/scripts/rider_check.py:596` | ❓ out of verified scope | Only macOS ran here. The pull request's CI run answers it |

## Paste-ready fixes

```python
        places = gfm_places(_blocks.gfm_lines, text)
        # Stepped over only where `region_lines` does not cut the GFM line
        # either. A GFM line that opens a comment is cut whole, so a rider
        # behind `# note` and a form feed, or behind a second rider on the
        # same line, is the hasher's: stepping over it left its stamp
        # compared by nobody (round 2 of #664).
        cut = {
            number
            for a, b in comment_blocks(_blocks.gfm_lines(text), rel)
            for number in range(a, b + 1)
        }
        quoted = quoted | {
            k
            for k, (number, head) in enumerate(places)
            if not head and number not in cut
        }
```
```text
    **A marker line that starts inside a GFM line, after something other
    than whitespace, opens no rider unless that GFM line opens a comment**,
    in any file type (#664, F's round 3, 🟡 3). It follows a break
    `str.splitlines` makes and GFM and `ast` do not, so `region_lines`, which
    cuts blocks out of GFM lines, never cut it: the rider's own stamp was
    hashed into the region it names, and no `--reverify` could make it read
    ok. Such a line is stepped over the way a quoted one is. Where the GFM
    line does open a comment, `region_lines` cuts it whole, so the reader
    reads every marker piece on it (#664 round 2). Only TEXT can say which
    lines those are, so `region_lines`, which passes none, has none to step
    over.
```
```python
@pytest.mark.parametrize(
    "rel, text",
    [
        ("mod.yml", f"a: 1\n# note{FF}# {'RIDER:'} about a. {STAMP}\nb: 2\n"),
        (
            "mod.yml",
            f"a: 1\n# {'RIDER:'} about a. {STAMP}{FF}# {'RIDER:'} about b. {STAMP}\n",
        ),
        ("doc.md", f"x\n{RIDER_MARK[:5]}a -->\u2028{RIDER_MARK} about a. {STAMP} -->\ny\n"),
    ],
    ids=["comment-then-break", "two-riders-one-line", "html-then-break"],
)
def test_a_rider_the_hasher_cuts_is_read(rel, text):
    """Round 2. `region_lines` cuts a GFM line that opens a comment whole,
    whatever follows a break inside it, so every marker piece on it is a
    rider to the reader too, or its stamp is compared by nobody."""
    riders = _load("specseal_riders_cut", RIDERS)
    blocks = riders.load_blocks()
    places = riders.gfm_places(blocks.gfm_lines, text)
    gfm = blocks.gfm_lines(text)
    read = sorted(places[r.start - 1][0] for r in riders.riders_in(rel, text))
    cut = sorted(
        n
        for a, b in riders.comment_blocks(gfm, rel)
        for n in range(a, b + 1)
        for _ in range(gfm[n - 1].count(riders.MARKER))
    )
    assert read == cut
```
```python
def write_block(root, rider, body):
    path = os.path.join(root, rider.rel)
    # `newline=""` both ways: the default translates CRLF and a lone CR to LF
    # on the read, so a CRLF file came back LF throughout (round 2 of #664).
    with open(path, encoding="utf-8", newline="") as f:
        lines = f.read().splitlines(True)
    # Each piece keeps the end it had, a last one with none keeping none.
    # BODY is the pieces joined with LF, and writing every piece back with
    # LF turned a form feed or U+2028 inside a rider into a line break
    # (round 1 of #664, 🟡 3). `restamp` writes no LF, so BODY splits into
    # exactly the pieces it was joined from.
    old = lines[rider.start - 1 : rider.end]
    ends = [piece[len(piece.splitlines()[0]) :] for piece in old]
    replacement = [
        piece + end for piece, end in zip(body.split("\n"), ends, strict=True)
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("".join(lines[: rider.start - 1] + replacement + lines[rider.end :]))
```
```python
def test_reverify_keeps_a_crlf_file_byte_for_byte(tmp_path):
    """Round 2. `write_block` opened the file with the default newline mode,
    so the read turned every CRLF into LF and the whole file came back LF."""
    riders = _load("specseal_riders_crlf", RIDERS)
    (tmp_path / "hooks").mkdir()
    path = tmp_path / "hooks" / "mod.py"
    text = (
        "def g():\r\n    return 1\r\n\r\n\r\n"
        f"# {'RIDER:'} about x. Verified 2026-01-01 against x@deadbeef\r\n"
        "x = 1\r\n"
    )
    path.write_bytes(text.encode("utf-8"))
    written, refused = riders.reverify(
        str(tmp_path), roots=("hooks",), today="2026-09-29"
    )
    assert len(written) == 1 and refused == []
    after = path.read_bytes()
    assert after.count(b"\r\n") == 6 and after.count(b"\n") == 6
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the item's module and `tests/test_a_rider_reaches_its_file.py`, in the clone at `7c339169` | 125 passed |
| The five new-or-changed cases with `rider_check.py` restored to `7bfea5f4` | 17 failed (16 leading-break cases and the write-back case). The `between`, last-line and class cases passed |
| `between` reverted to `text.splitlines()[rider.end : first[0] - 1]` | the new `between` case failed. The gap case passed |
| `write_block` mutant giving an endless last piece an LF | the last-line case failed |
| Class case with one more call planted in `riders_in` | failed: `('.github/scripts/rider_check.py', 'riders_in'): (2, 1)` |
| Class case with a module-level call planted in `hooks/routing.py` | failed, naming `('hooks/routing.py', '<module>')` |
| Differential over 576 whitespace-and-break prefixes, `.yml` and `.md`, reader against hasher at head | 0 disagree |
| `check()` on a `.py` rider with a drifted stamp behind eight prefixes, base against head | base 1 drifted for all eight. Head 1 drifted for the six whitespace prefixes, 0 drifted and 0 problems for `# note` then a form feed and for the code control |
| Reader against hasher on the comment-prefix, two-riders and HTML-prefix shapes, and two controls | head reads none of the three the hasher cuts. The controls are cut by neither |
| `reverify` on five byte shapes at head | LF and the U+2028 shape kept. CRLF 6 to 0, lone CR 6 to 0, CRLF with a form feed 6 to 0 with the form feed kept |
| 🟡 1 and 🟡 2 fixes and both new cases applied | 129 passed over the two modules. `rider_check.py --root .`: `19 ok · 0 drifted · 0 broken`. The 576-prefix differential still agrees. All five byte shapes kept. `check()` on the comment prefix: 1 drifted |
| 🟡 1's condition removed with the new case in place | the three shapes of the new case failed |
| 🟡 2's read reverted to the default mode with the new case in place | the CRLF case failed. With only the write reverted it passed on macOS |
| `bin/evidence-check` at `7c339169` | exit 0, 0 drifted, 0 refused |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
