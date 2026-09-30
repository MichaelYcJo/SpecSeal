# 1790683267-a-rider-read-ends-where-the-hasher-cuts — round 1 report

| Field | Value |
|---|---|
| Round | 1 |
| Target | the build range `f7b7d247..0abe93a7` (5 commits), read at branch HEAD `0abe93a7` |
| Base | `origin/release/v0.16.0` at `346b4af7`, whose `rider_check.py` is the reader the build starts from |
| Reviewed by | specseal:warden on claude-opus-5-5, in a `git clone --no-local` of the branch at `0abe93a7`, with a second clone at `346b4af7` loaded beside it |
| Earlier rounds | none for this item. G's `rounds/round-3-report.md` was read for its coordinates |

## What this round found, in the order one causes the next

1. The build does what the spec asks, and the acceptance sentence holds on
   every input this round could generate (executed). `riders_in` now takes
   the hasher's blocks, so a rider read off the cut cannot happen by
   construction. A differential over 120,000 generated texts found no rider
   read off the cut at HEAD. At the base, 20,154 texts had one.
2. The other direction also holds (executed). On 64,482 generated texts
   without the eight characters, and on the 25 tree files that carry the
   marker, HEAD and the base read identical riders. Every difference between
   the two readers is on a text where the base broke the property.
3. The removed text path had no other reader (read and executed). The
   `-->` rule is not a defect in the rider reading. A CommonMark renderer
   ends the HTML block where the checker does, and it shows the stamp line
   as paragraph text (executed).
4. Five ⬜ remain, and none of them changes what ships. Two are sentences
   narrower than the code: `comment_blocks`' docstring (⬜ 1) and three
   ledger notes (⬜ 2). One is a stale comment (⬜ 3), one is an oracle case
   that now guards a path nobody takes (⬜ 4), and one is a pre-existing,
   out-of-class location number (⬜ 5).

Nothing here needs a fix. The broad gate, the sealer's run, now comes due.

## Spec compliance

### Push 1: the class, not the two shapes

**The smith claimed** K1 holds by construction and measured it on 576
differential texts, 84 case texts, 25 tree files and 60,000 generated texts.
**This round built its own differential** and did not reuse the smith's
corpus. It generates one to nine lines per text. The pieces come from both
comment kinds, closed and open HTML comments, a lone `-->`, `# note`, fences,
headings, list and quote markers, code, and the marker in prose, strings and
table cells. They are joined on a line by nothing, spaces or one of the eight
characters, sometimes with a leading break, and the lines end in LF, CRLF or a
lone CR. Each text is read as `.py`, `.yml` and `.md`. For each text the probe
asked four things:

- The hasher did not move. `comment_blocks` over `checker.gfm_lines` gives
  the same blocks at HEAD and at the base in 120,000 of 120,000 texts.
- Every piece of every rider read lies inside one block the hasher returns.
- The riders' starts are exactly the marker pieces inside a cut block, and no
  rider's tail carries the marker.
- Every piece of a cut block, from its first marker piece on, is read by
  exactly one rider, so no stamp in a cut block is left unread.

At HEAD all four held in 120,000 texts (55,518 with one of the eight),
over 135,604 riders read. At the base, 20,154 texts broke one of them. That
count is the probe's proof it can fail, and it is far above G's 4 of 13,237
because this generator puts a break into about half its lines.

An end-to-end half planted 6,971 texts in a temporary tree, with anchors that
resolve (`def a()` in Python, `# doc` in markdown) and raw line ends. It ran
`reverify`, then `check`, then `reverify` again. At HEAD no rider was drifted
after a `reverify`, the second `reverify` wrote nothing, and nothing raised.
At the base, 8 texts stayed drifted after a `reverify` and were rewritten
again on the second. That is #682's symptom, and the probe reached it through
shapes nobody named.

**The other direction.** On 64,482 texts without the eight, HEAD and the base
read the same `(start, end, body)` for every rider. All 20,154 differing
texts were ones where the base broke the property. No text had a difference
with the base reader correct. `inferred_anchor` gave the same answer at both
versions for 43,145 Python riders both read alike, and it named a unit for
1,065 of them. `rider_check.py --root .` prints `18 ok · 0 drifted · 0 broken`
and exits 0 with either script over this tree. Its 25 marker-carrying files
give identical riders.

**§15.** The two new cases were run against the base `rider_check.py`, put
into the clone and then restored. 32 failed and 32 passed. The 32 failures
are the two #682 shapes under all eight characters, in both cases, which is
what phase 1 claims. The mutant "each rider runs to the block's end" turns 8
cases red over the three rider modules, all in the class case, which matches
the phase record's 8.

### Push 2: the removed text path

**The smith claimed** nothing else read `comment_blocks`' TEXT or the
second value of `gfm_places` (spec M8, M9). **Found:** every call of
`comment_blocks(` in the tree passes one or two positional arguments:
`region_lines`, `riders_in`, and the cases in
`tests/test_a_rider_reaches_its_file.py` and
`tests/test_every_reader_ends_a_line_where_gfm_does.py`. No hook, skill or
other script imports `rider_check.py` for these units. `gfm_places` is called
by `riders_in`, `inferred_anchor` and one case, and none of them indexes the
pair any more.

What else rode on the path:

- **Quoted lines and fences.** `riders_in` now reaches `quoted_lines` over
  GFM lines with no text, so it quotes whole GFM lines through
  `hooks/blocks.py#walk`, which is the hasher's reading. Before, it quoted
  pieces through `walk_text`. The one case that holds the rider's quoting to
  the CommonMark oracle still drives the text path (⬜ 4). A probe put the
  reader's new path through the same oracle and the same corpus: 6,066
  documents, 5,183 of them holding a break, and it never left both readings
  (executed).
- **The `.md` heading rule.** `hash_opens_a_comment` reads `rel`, and
  `riders_in` still passes it. The generator's `# Heading` and `# ...`
  pieces in `.md` produced no violation and no difference without the eight.
- **`quoted_lines`' own contract.** Unchanged, as J3 decided. Its TEXT
  parameter now has one caller, the oracle case.
- **`--reverify` and `--migrate` through `write_block`.** Riders are still
  numbered on `str.splitlines` pieces, and `write_block` splits the raw file
  the same way. The end-to-end half above exercised the write path with raw
  CRLF and lone CR. `migrate` reaches `write_block` the same way, and
  `inferred_anchor` agreed with the base (above). `migrate` itself was not
  run end to end.

### Push 3: the `-->` rule

A probe ran the markdown shape at the base and at HEAD, with a space and with
U+2028, through `reverify` and then `check`, and rendered each text with the
CommonMark parser the suite pins:

| Text | Base | HEAD | Renderer |
|---|---|---|---|
| a closed comment, a space, then the rider, stamp on the next line | BROKEN, no verification stamp | BROKEN, no verification stamp | shows the stamp line as paragraph text |
| the same with U+2028 | 1 drifted after `reverify` | BROKEN, no verification stamp | shows the stamp line as paragraph text |
| the rider alone, stamp on the next line (control) | 1 ok | 1 ok | hides it |
| the closed comment and the rider on one line, stamp included | 1 ok | 1 ok | hides it |

This is not a defect in the reading. An HTML comment block in CommonMark
ends at the first line holding `-->`, and a line that begins with a closed
comment is that line. The rider's opener is inside that block, and its stamp
line after it is visible text. The checker reads the rider as a person would
see it rendered: a comment with no stamp in it. So the verdict is the right
one, and it fails loudly (exit 2) rather than losing an alarm.

The sentence "no verification stamp" is loose for this shape, because a stamp
exists, outside the comment. That is a message improvement and not this
item's class. The class is two readers disagreeing, and here the reader and
the hasher share one rule. It does not need its own item unless the owner
wants the message to name the case.

### Push 4: the interpreter floor

`rider_check.py` carries no `zip(`, no `pairwise` and no `.UTC`. The only
`zip` is `write_block`'s comment, "a strict zip", which `ABOVE_THE_FLOOR`
does not match. The pairs are built as `[*starts[1:], inside[-1] + 1]` and
indexed over `range(len(starts))`. List unpacking needs 3.5. The floor case
passed, and ruff `check` and `format --check` are clean on both changed files
(executed).

### Push 5: the ledger

`evidence-check --strict .` gives `3082 ok · 0 drifted · 0 broken`, exit 0.
`correction-check --range 346b4af7...HEAD` examined 1 merge and found no
dropped marker, exit 0. The range is `origin/release/v0.16.0...HEAD`, since
`origin/release/v0.16.0` is `346b4af7` in the worktree. `survivor-check`
exits 1 without the exemptions and 0 with every `survivors.md` handed over
as the hygiene workflow does, with both rows shown as `exempt`.

Each claim was re-read at HEAD:

- **K1** is true. It is the property the differential above measured.
- **K2** is true. The verdict case passes, and the `-->` probe shows the
  markdown shape reads BROKEN "no verification stamp" before and after
  `reverify` at HEAD.
- **G13**. Its anchors resolve, and its `Re-read` note describes the fix.
  Its first clause, and the note's sentence that it "holds as written", are
  narrower than the code (⬜ 2).
- **S2** is true. Every block the reader reads is a block `region_lines`
  removes.
- **S3** is true. The opening and closing rules are untouched, and two
  riders on one GFM line stay two.
- **P5-1**. The correction is true about the step-over and the walk. Its
  "nowhere else" is the same narrowing as ⬜ 2.
- **R1-1**'s correction is true. On the rider side only `quoted_lines`
  takes a text, and `test_the_rider_check_never_leaves_both_readings` is
  its one caller that passes one.

The two `survivors.md` entries are still true. The case docstring's text,
`body` then a break then an opener, has no comment open above it and reads no
rider at HEAD. P5-1's round 2 note is dated history.

## Quality

### ⬜ 1 — `comment_blocks`' docstring states the mid-line rule narrower than the code

`.github/scripts/rider_check.py:307` says a mid-line marker piece "is a rider
exactly where its GFM line opens a comment". A GFM line can also continue an
HTML comment that an earlier block left open, because that block ended at the
next marker rather than at `-->`. Take `&lt;!-- RIDER: about a.` on one line,
then `more`, U+2028 and `RIDER: about b. … -->` on the next. That line opens
no comment. Yet `comment_blocks` opens a block there through `in_html`, and
HEAD reads the piece after the break as a rider. That reading is right: the
hasher cuts the line (executed, the continuation probe). Only the sentence is
narrower than the code. The same phrase is in `riders_in`'s own story in the
ledger (⬜ 2).

### ⬜ 2 — G13 and this item's notes on G13 and P5-1 repeat that narrowing

This is a correction to paperwork, so it is outside `Needs a fix`. G13's first
clause says the reader reads no rider whose marker starts mid-line after
something other than whitespace "unless that GFM line opens a comment".
This item's `Re-read` note on G13 says the clause "holds as written" because
a mid-line marker piece is read "exactly where its GFM line opens a comment".
P5-1's #682 correction says "and nowhere else". The continuation line in ⬜ 1
is a counterexample at HEAD, and it was one at the base too. K1 already states
the exact rule, *inside a block `comment_blocks` over GFM lines returns*.

### ⬜ 3 — `region_lines`' comment explains an argument that no longer exists

`.github/scripts/rider_check.py:476` reads "No TEXT: these are already GFM
lines … Handed the text, `walk_text` answers by `str.splitlines`". Since this
item, `comment_blocks` takes no text, so passing one is a `TypeError` and not
a choice. The overview keeps the comment because editing it "would move S2's
anchor for a sentence that holds". But S2 already carries this item's
`Re-read` note, so re-stamping it costs one hash. The sentence the comment
should say is the one this item made true: the reader cuts from the same GFM
lines.

### ⬜ 4 — the rider's oracle case drives a path the rider reader no longer takes

`tests/test_the_hooks_hide_what_a_renderer_hides.py:753` holds
`quoted_lines(lines, text)` to the oracle. It is titled "Half 1, S12's
reader", and after this item no shipped reader calls that form. What
`riders_in` runs is `quoted_lines` over GFM lines, mapped to pieces. That path
is held to the oracle only through `walk_text`, which calls the same `walk`.
This round's probe showed it holds (above), but no case in the tree says so.
J3 kept the TEXT parameter, correctly. The fix is to add the reader's half
beside it, not to drop the parameter.

### ⬜ 5 — a rider's location is a `str.splitlines` number, not the line an editor shows

`.github/scripts/rider_check.py:374`: `Rider.where` prints `rel:start`,
where `start` counts pieces. Below one of the eight characters, that number
runs ahead of the GFM line an editor or GitHub shows. The same holds on the
`restamped` and `REFUSED` lines. It is older than #664, since the spec keeps
riders numbered on pieces. It is not this item's class, and the verdict case
leaves the location out of its comparison on purpose. It is a candidate for
its own issue, and it is listed under Deferred for the orchestrator.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `comment_blocks`' docstring says a mid-line marker piece is a rider exactly where its GFM line opens a comment; a line continuing an HTML comment an earlier block left open is read too | `.github/scripts/rider_check.py:307` | open | executed: the continuation probe reads the piece after the break as a rider at HEAD, and the hasher cuts that line; the behaviour is right, the sentence is narrower |
| ⬜ 2 | G13's first clause, this item's `Re-read` note on G13 ("holds as written") and P5-1's #682 correction ("nowhere else") state the same narrower rule | `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md` G13; `seal/ledger/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule.md` P5-1 | open | a correction to paperwork, outside `Needs a fix`; the same counterexample as ⬜ 1, at HEAD and at the base; K1 states the exact rule |
| ⬜ 3 | `region_lines`' "No TEXT" comment explains an argument `comment_blocks` no longer takes | `.github/scripts/rider_check.py:476` | open | read; S2 already takes this item's `Re-read` note, so a re-stamp is the whole cost |
| ⬜ 4 | the rider's oracle case drives `quoted_lines(lines, text)`, which no shipped caller uses; the reader's GFM-lines path has no oracle case | `tests/test_the_hooks_hide_what_a_renderer_hides.py:753` | open | executed: the reader's path through the same oracle and corpus, 6,066 documents, 5,183 with a break, never leaves both readings |
| ⬜ 5 | `Rider.where` prints the `str.splitlines` piece number, which runs ahead of the GFM line below one of the eight characters | `.github/scripts/rider_check.py:374` | open | read; older than #664 and outside this item's class; see Deferred |
| 🟢 | K1 holds: every piece of every rider read lies in one block the hasher returns, and every marker piece in a cut block starts exactly one rider | `.github/scripts/rider_check.py:377` | confirmed | executed: 120,000 generated texts, 0 at HEAD against 20,154 at the base; end to end on 6,971 texts, 0 drifted after `reverify` at HEAD against 8 at the base |
| 🟢 | nothing changes for a text without the eight characters | `.github/scripts/rider_check.py:377` | confirmed | executed: 64,482 generated texts and the 25 tree files, identical riders; `inferred_anchor` identical on 43,145 riders; the tree reads `18 ok · 0 drifted · 0 broken` with either script |
| 🟢 | the removed text path and the second value of `gfm_places` had no other reader | `.github/scripts/rider_check.py:236` | confirmed | read: every call site in the tree; executed: the three rider modules pass |
| 🟢 | the `-->` rule is not a defect in the rider reading, and not this item's class | `.github/scripts/rider_check.py:341` | confirmed | executed: BROKEN with a space at both versions and with U+2028 at HEAD, and the CommonMark parser shows the stamp line as paragraph text; the reader and the hasher share the rule |
| 🟢 | the shipped script stays on the interpreter floor | `.github/scripts/rider_check.py:410` | confirmed | executed: the floor case and ruff; read: no `zip(`, `pairwise` or `.UTC` |
| 🟢 | the new cases were seen red at the base reader | `tests/test_every_reader_ends_a_line_where_gfm_does.py:1024` | confirmed | executed: 32 red against the base `rider_check.py`, the two shapes under all eight characters in both cases; the rider-to-block-end mutant turns 8 red |
| 🟢 | K1, K2, S2, S3 and R1-1 are true at HEAD, and the checks agree | `seal/ledger/1790683267-a-rider-read-ends-where-the-hasher-cuts.md` | confirmed | executed: `evidence-check --strict` exit 0, `correction-check` exit 0, `survivor-check` exit 0 with the exemptions; G13 and P5-1 are true apart from ⬜ 2 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_every_reader_ends_a_line_where_gfm_does.py`, `tests/test_a_rider_reaches_its_file.py`, `tests/test_the_hooks_hide_what_a_renderer_hides.py`, `tests/test_a_script_says_which_interpreter_it_needs.py`, `tests/test_a_record_states_what_the_tree_has.py` at `0abe93a7` | 446 passed, exit 0 |
| the two new cases with the base `rider_check.py` put in place, then restored | 32 failed, 32 passed: the two #682 shapes under all eight characters, in both cases |
| the mutant `ends = [inside[-1] + 1] * len(starts)` over the three rider modules, then restored | 8 failed, all in the class case |
| a reader-against-hasher differential, generated texts in `.py`, `.yml` and `.md`, HEAD and the base loaded side by side | 120,000 texts, 55,518 with one of the eight. The hasher was the same at both in all of them. HEAD: 0 texts break the property, over 135,604 riders. Base: 20,154 texts. Without the eight, 0 of 64,482 texts differ between the two, and every difference is on a text where the base broke the property |
| the same generator end to end, `reverify` then `check` then `reverify`, in a temporary tree with raw CRLF and CR ends | 6,971 texts per version. HEAD: 0 drifted after `reverify`, 0 rewritten on the second, 0 raised. Base: 8 drifted and rewritten again |
| `inferred_anchor`, HEAD against base, on Python riders both read alike | 43,145 riders, 0 differ, 1,065 named |
| the tree's marker-carrying files, HEAD against base; `rider_check.py --root .` with each script | 25 files, 18 riders, 0 differ; `18 ok · 0 drifted · 0 broken`, exit 0 with each |
| the reader's GFM-lines quoting against the CommonMark oracle, on the oracle case's corpus | 6,066 documents, 5,183 with a break, 0 leaving both readings |
| the `-->` shapes at base and HEAD, with a space and U+2028, through `reverify` and `check`, and rendered | see the table under Push 3 |
| a marker piece after a break on a line continuing an open HTML comment | cut `[(2, 2), (3, 3)]`; HEAD reads the piece after the break as rider (4, 4) and puts the piece before it in no rider; the base read that piece into the first rider, across two blocks |
| `bin/evidence-check --strict .` | `3082 ok · 0 drifted · 0 broken`, exit 0 |
| `bin/correction-check --range 346b4af7...HEAD` | 1 merge examined, no marker dropped, exit 0 |
| `survivor_check.py --range 346b4af7...HEAD` with every `survivors.md` passed through `--exempt` | 2 exempt, exit 0; without the exemptions exit 1 on the same two places |
| `ruff check` and `ruff format --check` on the two changed Python files | clean, exit 0 |
| the broad gate: the full suite, repository-wide lint and typecheck over this branch | not yet — not run by this round. It is the sealer's, and it comes due now, since nothing here needs a fix |

Every probe was a file in this round's scratch directory, outside the tree,
and was deleted after its run. The two clones went with it.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 5 — a rider's printed location is a `str.splitlines` number, older than #664 | not placed: a candidate for its own issue | the orchestrator, who files it or answers that it stays as is |
| the `-->` shape's sentence "no verification stamp" when a stamp sits outside the comment (Push 3) | not placed: a message improvement, outside this item's class | the orchestrator, if the owner wants the message to name the case |

## Paste-ready fixes

None of these is required, since every finding is ⬜. Each edit moves the
anchors noted beside it, and those rows then take a re-stamp.

### ⬜ 1

`.github/scripts/rider_check.py#comment_blocks`, the paragraph at line 302.
This moves the `comment_blocks` anchor in G13, P5-1, S3 and K1.

```python
    **LINES are GFM lines, and this is the one block rule** (#682). Both
    callers hand over `gfm_lines` of the file: `region_lines` cuts the blocks
    out of the region it hashes, and `riders_in` splits the same blocks at
    every `str.splitlines` piece carrying the marker. So a marker piece
    standing mid-line after a U+2028 or a form feed is a rider exactly where
    its GFM line lies inside a block this returns -- a comment it opens, or
    an HTML comment an earlier block left open -- which is where the hasher
    cuts it. Nothing here reads pieces: a reader that walked them by a second
    statement of this rule parted from the hasher in each of #664's three
    rounds.
```

### ⬜ 2

A note for G13 and P5-1, appended after this item's own note on each:

```text
**Corrected 2026-09-29 in round 1 of work item 1790683267 (#682):** "opens a comment" is narrower than the reader. A mid-line marker piece is read wherever its GFM line lies inside a block `comment_blocks` over GFM lines returns, which includes a line continuing an HTML comment an earlier block left open at a marker; K1 states the rule. This was so at `346b4af7` as well.
```

### ⬜ 3

`.github/scripts/rider_check.py#region_lines`, the comment at line 476. This
moves S2's anchor.

```python
    lines = checker.gfm_lines(text)  # the lines `resolve_unit` numbered (#664)
    # GFM lines, the ones `riders_in` hands `comment_blocks` too, so the blocks
    # cut here are exactly the blocks the reader reads (#682).
    blocks = comment_blocks(lines, rel)
```

### ⬜ 4

`tests/test_the_hooks_hide_what_a_renderer_hides.py#test_the_rider_check_never_leaves_both_readings`,
the loop body, with the reader's own half beside the text half:

```python
    blocks = riders.load_blocks()
    wrong = []
    for doc in CORPUS:
        text, lines = as_read(doc)
        hidden = set(oracle.hidden_text(text))
        new = riders.quoted_lines(lines, text)
        bad = leaves_both(new, set(), hidden, len(lines))
        # What `riders_in` runs since #682: whole GFM lines, mapped to pieces.
        quoted = riders.quoted_lines(blocks.gfm_lines(text))
        places = riders.gfm_places(blocks.gfm_lines, text)
        read = {k for k, number in enumerate(places) if number - 1 in quoted}
        bad += leaves_both(read, set(), hidden, len(lines))
        if bad:
            wrong.append((lines, bad))
```

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened at `0abe93a7` in the clone:
- `.github/scripts/rider_check.py` (lines 150–900, and the full diff against `f7b7d247`)
- `tests/test_every_reader_ends_a_line_where_gfm_does.py` (the diff, lines 736–760, the constants)
- `tests/test_the_hooks_hide_what_a_renderer_hides.py` (lines 22–33, 505–595, 670–760)
- `tests/test_a_script_says_which_interpreter_it_needs.py` (lines 467–529)
- `tests/block_shapes.py` (lines 25–40)
- `hooks/blocks.py` (lines 1–80, 365–420)
- `skills/evidence-check/scripts/evidence_check.py` (lines 290–310)
- `skills/verify/scripts/unverified_check.py` (lines 300–325)
- `skills/code-review/scripts/survivor_check.py` (lines 118–140, 245–270)
- `.github/workflows/hygiene.yml` (lines 250–275)
- this item's `spec.md`, `plan.md`, `questions.md`, `overview.md`, `phases/phase-1.md`, `survivors.md`, `changelog.md`, `routing.md`
- `seal/ledger/1790683267-a-rider-read-ends-where-the-hasher-cuts.md`, and rows G13, P5-1, R1-1, S2 and S3 where they stand
- `seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/rounds/round-3-report.md` (head) and `round-3.md` (Deferred)
