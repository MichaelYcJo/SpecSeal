# 1790655302-every-reader-ends-a-line-where-gfm-does — round 2 report

| Field | Value |
|---|---|
| Round | 2, a verifying round |
| Target | the fix diff `7bfea5f4..21b871ef` (6 commits), read at branch HEAD `7c339169` |
| Reviewed by | specseal:warden on claude-opus-5-5, in a `git clone --no-local` of the branch, with a second clone at `3fc0c5bd` for base comparisons |
| Earlier rounds | round 1, read for its coordinates and its five verdicts |

## What this round found, in the order one causes the next

1. All five of round 1's findings are closed for the shapes round 1 recorded.
   Each new case fails against the code it was written for (executed).
2. Round 1's finding 1 was one instance of a wider class. The fix makes the
   reader agree with the hasher when only whitespace stands before a marker.
   The hasher also cuts a GFM line that opens a comment, whatever follows a
   break inside it. A rider behind `# note` and a form feed is therefore
   still cut by the hasher and read by nobody (🟡 1).
3. `write_block` now keeps each piece's end as it reads it. It still reads
   the file in the default newline mode, which turns CRLF and a lone CR into
   LF before the new expression sees them. The fix's own comment, ledger row
   G15 and the changelog fragment all say a CRLF rider keeps its CR. It does
   not (🟡 2, and ⬜ 3 for the paperwork).

The class case answers the third question with no finding: any new
`.splitlines(` call in a shipped `.py` file fails it (executed).

## The three questions the prompt asked

### Does `gfm_places` agree with the hasher's `lstrip` on every leading whitespace?

Yes, for whitespace. `gfm_places` tests `text[opened:at].strip()`, and
`comment_blocks` tests `line.lstrip()`. Both use `str.isspace`, so they
cannot disagree on which characters count as whitespace.

I ran a differential over 576 prefixes (executed). Each prefix was one of
`""`, space, tab, NBSP, U+3000 or `\x1f`, then one of the eight breaks, then
one of the same six. Each ran in a `.yml` `#` rider and in a markdown HTML
rider. For every prefix, the GFM lines the reader's riders start on equal
the GFM lines holding a marker inside the hasher's blocks. Through `check()`
on a `.py` rider with a drifted stamp, the prefixes form feed, tab, spaces
then form feed, form feed then tab, and two form feeds each report 1
drifted at head (executed).

No, for a comment. See 🟡 1.

### Does `write_block` keep every line end, CRLF included, byte for byte?

Only for LF files. I ran `reverify` on five byte shapes at head (executed):

| Shape | CRLF before → after | lone CR before → after | FF / U+2028 kept |
|---|---|---|---|
| LF | 0 → 0 | 0 → 0 | yes |
| CRLF | 6 → 0 | 6 → 0 (as part of CRLF) | n/a |
| lone CR | 0 → 0 | 6 → 0, each an LF now | n/a |
| CRLF with a form feed inside the rider | 6 → 0 | 6 → 0 | form feed kept |
| LF with a U+2028 inside the rider | 0 → 0 | 0 → 0 | yes |

The whole file changes, not only the rider. See 🟡 2.

### Can a new `splitlines(` still slip past the class case?

Not as a call in a shipped `.py` file. I planted one more call in
`riders_in`, a unit named with a count of 1, and the case failed with
`(2, 1)`. I planted a module-level call in `hooks/routing.py`, and the case
failed naming `('hooks/routing.py', '<module>')` (both executed, both
reverted).

By reading, I also checked where a call could sit outside the walk. No
shipped file without the `.py` suffix contains `splitlines(`. No tracked
`.py` file lies outside `hooks/`, `skills/`, `.github/scripts/` and
`tests/`. No file in `bin/` is Python. A call inside an f-string, a lambda
or a decorator is still an `ast.Call`, and the walk attributes it to some
unit. What the walk does not see is a reference that is not a call, such as
`map(str.splitlines, rows)`. None exists in the tree, and it is not the
shape the prompt asked about, so I raise nothing.

## Findings from execution

### 🟡 1 — A rider behind a comment on its GFM line is cut by the hasher and read by nobody

`.github/scripts/rider_check.py:331` (`comment_blocks`, the union that adds
non-head pieces to `quoted`), with `gfm_places` at `:261`.

The reader steps over a marker piece when something other than whitespace
stands before it on its GFM line. The hasher does not use that rule.
`region_lines` passes GFM lines to `comment_blocks`. That function opens a
block on a line that contains the marker anywhere and whose `lstrip` starts
with `#` (outside markdown) or with an HTML comment opener. So a GFM line
`# note<FF># RIDER: …` is one rider block to the hasher and is cut from the
region. To the reader, the piece after the form feed starts mid-line after
`# note`, so it is stepped over. Nobody compares that rider's stamp, and
the run prints `0 drifted`.

Three shapes do this, and base read each of them (executed):

| Shape | base reader | head reader | head hasher |
|---|---|---|---|
| `.py`, `# note`, form feed, rider with a drifted stamp, through `check()` | 1 drifted | 0 drifted, 0 problems | cuts it |
| `.yml`, two riders on one GFM line joined by a form feed | reads both | reads the first | cuts the line |
| `.md`, a closed HTML comment, U+2028, then the HTML rider | reads it | reads none | cuts the line |
| `.yml` and `.md` controls, code or prose before the break | reads it | reads none | cuts nothing |

The controls show the rule F's round 3 wrote still holds where it should:
where the hasher does not cut the line, the reader steps over the piece.

This is round 1's finding 1 again with a different prefix. It is the same
class: the reader's test for a head disagrees with the hasher's test for a
cut. The fix repaired the whitespace instance. No file in the tree has
these shapes today, so the defect is latent. It is on the silent side of
the gate this item hardens.

The paste-ready fix asks the hasher's own question. It steps over a
mid-line piece only where `comment_blocks`, run over the GFM lines,
does not cut that line. With it, all three shapes read at head, the two
controls are still stepped over, and the 576-prefix differential still
agrees (executed). The case under *Paste-ready fixes* failed for all three
shapes with only the `number not in cut` condition removed (executed).

### 🟡 2 — `write_block` still writes a CRLF file back as LF

`.github/scripts/rider_check.py:584` (the read in `write_block`) and `:596`
(the write).

Both `open` calls use the default newline mode. The read translates CRLF
and a lone CR to LF before `splitlines(True)` runs, so `old` never holds a
CR, and the new `ends` expression has none to keep. The write then puts LF
everywhere. On a platform whose line separator is CRLF, the default write
also turns every LF in the file into CRLF. I did not run that; see the ❓
row.

The fix range claims the opposite in three places:

- the comment above the new expression, "Each piece keeps the end it had";
- ledger row G15, "a CRLF piece keeps its CR";
- the changelog fragment, "a CRLF rider came back as LF", stated as fixed.

At base the behaviour is the same (the old body wrote `"\n"` after every
line), so this is not a regression. The changelog now tells users it is
fixed, and the round 1 fix was accepted on that basis.

The fix is `newline=""` on both `open` calls. The rider's numbering is safe
with it. `Rider` is built from a text read in the default mode, and that
translation only replaces a break with another single break, so the piece
count is the same. `strict=True` in the zip would raise if it were not.
With the fix, all five shapes above keep every byte (executed). The case
under *Paste-ready fixes* failed with only the read reverted to the default
mode (executed). With only the write reverted, it passed on macOS, because
the write matters only where the separator is CRLF.

## Paperwork

### ⬜ 3 — G15 and the changelog fragment say a CRLF rider keeps its CR

`seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md:23`
(G15), and the last bullet of this item's `changelog.md`.

Both sentences are false at `21b871ef`. If 🟡 2's fix lands, both become
true. The fix drifts G15's `write_block` anchor, so G15 is re-read and
re-stamped against it. If 🟡 2 is answered with grounds instead, both
sentences have to drop the CRLF clause. This is a correction to the run's
paperwork. It is not a fix.

## Round 1's verdicts, checked

| Round 1 | Is it closed? | Grounds |
|---|---|---|
| 🟡 1, a rider behind a leading break goes unread | Yes, for whitespace | 16 of the new parametrised cases failed with `rider_check.py` restored to `7bfea5f4` (executed). The 576-prefix differential agrees. The class remains open through a comment prefix (🟡 1 above) |
| 🟡 2, the `between` slice is unpinned | Yes | With `between` reverted to `text.splitlines()[rider.end : …]`, the new case failed and the gap case passed (executed) |
| 🟡 3, a form feed or U+2028 inside a rider comes back as a line break | Yes, for those characters | The new write-back case failed at `7bfea5f4` (executed). A U+2028 inside a rider is kept too (probe). The last-line case failed against a mutant that gives an endless last piece an LF (executed). CRLF is not kept (🟡 2 above) |
| 🟡 4, the class case exempts four files whole | Yes | The two plants above both failed the case. `F_FILES` is gone from the test module (NAME NOT IN TREE) |
| ⬜ 5, a raw U+2028 in `phases/phase-4.md` | Yes | The file holds no U+2028 at `7c339169` (executed count: 0) |

I carried nothing from round 1's conclusions. I carried its coordinates:
the line numbers of `gfm_places`, `write_block`, `inferred_anchor` and the
class case, re-opened at `7c339169`.

## The account, checked

| The fix range claimed | What I found |
|---|---|
| `gfm_places` calls a piece a head "when only whitespace stands before it on that line", matching `comment_blocks`' `lstrip` | True for whitespace (576 prefixes). Not the whole of what `comment_blocks` cuts (🟡 1) |
| `write_block` "keeps each piece's own end" | True for every end the default read leaves. CR is gone before the expression runs (🟡 2) |
| `restamp` writes no LF, so `BODY` splits into exactly the pieces it was joined from | True by reading `restamp` at `:574`. The five byte shapes raised nothing through `strict=True` (executed) |
| The class case names F's units with their counts | True. Both plants failed it |
| `evidence-check` holds after the ledger changes in `da292452` | Exit 0, 0 drifted, 0 refused at `7c339169` (executed) |

## Regression tests to plant

Both go into `tests/test_every_reader_ends_a_line_where_gfm_does.py`, below
round 1's cases. They are the two case fences under *Paste-ready fixes*.
With both fixes applied, the item's module and
`tests/test_a_rider_reaches_its_file.py` passed together, 129 cases
(executed), and `rider_check.py --root .` on the tree read `19 ok · 0
drifted · 0 broken` (executed). Each case was shown red as described under
its finding.

## Facts for the evidence ledger

- `rider_check.py#comment_blocks` opens a block on a GFM line that contains
  the marker anywhere and whose `lstrip` starts with a comment opener. So
  `region_lines` cuts a rider that stands after a break inside such a line.
  Read at `7c339169`, executed through `check()`.
- `rider_check.py#write_block` opens the file in the default newline mode.
  The read turns CRLF and a lone CR into LF, and the write rewrites the whole
  file in the platform's separator. Executed at `7c339169` on macOS.

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

## Paste-ready fixes

### 🟡 1 — step over a mid-line piece only where the hasher does not cut its line

In `.github/scripts/rider_check.py#comment_blocks`, replace the line that
adds non-head pieces to `quoted`:

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

The docstring paragraph that begins "A marker line that starts inside a GFM
line" then reads:

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

The changelog bullet "The rider check reads no rider whose marker line
follows one of the eight characters mid-line" gains "unless the line opens
a comment". Case:

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

### 🟡 2 — `write_block` opens the file with `newline=""` both ways

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

Case:

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

The class for §12 is a writer that reads in the default newline mode and
rewrites the file. `.github/scripts/gather_changelog.py:413` has the same
write. I did not open it further, because it is outside this fix diff and
its changelog bullet makes no CRLF claim.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1 (a rider behind a comment on its GFM line is cut by the hasher and read by nobody), 🟡 2 (`write_block` writes a CRLF file back as LF)
Loses a record or crashes: no

The broad gate is not due yet: this round leaves two findings open.

## Proof block

Files opened this round, in the clone at `7c339169` unless named:

- `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/rounds/round-1.md` and `round-1-report.md`, whole
- `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/changelog.md`, whole
- the diff `7bfea5f4..21b871ef` of `.github/scripts/rider_check.py` and `tests/test_every_reader_ends_a_line_where_gfm_does.py`, whole, and of `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md` for rows G12 to G15
- `.github/scripts/rider_check.py`, lines 205–624 and 684–708
- `tests/test_every_reader_ends_a_line_where_gfm_does.py`, lines 50–53, 585–720 and 733–735
- `.github/scripts/rider_check.py` at `3fc0c5bd`, `write_block`
- `.gitattributes`
- `bin/test`
