# Implementation Plan: a rider read ends where the hasher cuts

<!-- seal/specs/1790683267-a-rider-read-ends-where-the-hasher-cuts/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-29 by the orchestrating session, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. -->

## Summary

`rider_check.py#riders_in` stops deciding where a rider ends. It asks
`#comment_blocks` over GFM lines, the hasher's blocks, and cuts each block's
`str.splitlines` pieces at every piece that carries the marker. What the
reader reads is then inside what `#region_lines` cuts by construction. The
TEXT path in `#comment_blocks` that round 2 of G added, and the whitespace
flag in `#gfm_places` that only that path read, go with it. One class case
and one verdict case pin it. One phase.

## Technical context

- **The reader today** (`.github/scripts/rider_check.py` at `6321dbdc`,
  identical to `7ffa520c`, spec M1). `#riders_in` calls
  `comment_blocks(text.splitlines(), rel, text)`. With TEXT, `#comment_blocks`
  steps over a mid-line marker piece unless its GFM line is in the hasher's
  `cut` set, and then runs each block over pieces by its own `-->` and
  comment-kind tests. That second walk is where the two shapes escape.
- **The hasher** (`#region_lines`) calls `comment_blocks(checker.gfm_lines(text), rel)`
  and cuts the returned blocks by GFM line number. It is not edited.
- **The fix** is round 3's paste-ready `riders_in` (G's
  `rounds/round-3-report.md` §*Paste-ready fixes*), with one change the floor
  forces. The pasted code pairs each start with the next through
  `zip(…, strict=True)`. `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR`
  refuses that text anywhere in a shipped script, a comment included, and
  ruff's B905 refuses a bare `zip`. `itertools.pairwise` arrived in 3.10 too,
  so it is refused on the same grounds although the pattern would not see it.
  Build the pairs by index, the shape `#write_block` took at `7ffa520c`:
  a list of ends built as `[*starts[1:], inside[-1] + 1]`, and
  `range(len(starts))` over both. **No length check.** In `write_block` the
  two lengths come from different data and can differ. Here the ends are
  built from the starts, so a check could never fire, and a check that cannot
  fire is not added.
- **Why every block has a start.** `comment_blocks` opens a block only on a
  line carrying the marker, the marker is six ASCII characters, and none of
  the eight can fall inside it. So some piece on the block's first line
  carries it, and `inside` and `starts` are never empty.
- **What removing the TEXT path takes with it.** In `#comment_blocks`: the
  `text` parameter, the `if text is not None` block (`places`, `cut`, the
  step-over), `quoted_lines(lines, text)` becoming `quoted_lines(lines)`, and
  the two docstring paragraphs about TEXT, rewritten to say the lines are GFM
  lines and that `riders_in` splits the returned blocks. In `#gfm_places`:
  the second tuple element and its *Whitespace, not nothing* paragraph. The
  whitespace rule now lives where the hasher applies it, `lstrip` on the GFM
  line (spec M6), and the reader inherits it rather than restating it. In
  `#inferred_anchor`: `places[rider.start - 1][0]` becomes
  `places[rider.start - 1]`, and the same for `end`. In
  `tests/test_every_reader_ends_a_line_where_gfm_does.py#test_a_rider_the_hasher_cuts_is_read`:
  the same `[0]`.
- **The new `riders_in` docstring** says what the reader reads and why it
  asks the hasher, and names #664's rounds 1 to 3 and #682 as the history of
  the second rule. It does not spell `zip(` with `strict=` (S9).
- **`#quoted_lines` keeps its TEXT parameter** (spec §*Scope*, out). After
  this item, the one caller that passes it a text is
  `tests/test_the_hooks_hide_what_a_renderer_hides.py`. Its docstring stays
  true of the function.
- **G14's enumeration** (`OUT_OF_CLASS`) keeps its counts: `riders_in`
  still makes one `.splitlines(` call, and `gfm_places` one (spec M11). Its
  reason cell for `riders_in` may say what the pieces are for. It is not
  required.

**What breaks in six months.** Somebody gives `#comment_blocks` a reason to
look at pieces again: a new comment form, or a report of a rider that reads
oddly behind a form feed. The fix for that report will be written in the
reader, because the reader is where the symptom shows, and the reader and the
hasher will part a fourth time. The class case is what answers it. It
asserts the property, every piece read on a cut line and every marker piece
on a cut line read, over the eight characters and both comment kinds, so a
reader that grows its own rule again fails there before anything ships.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. Patch the reader's walk**: make the piece walk end the block where the GFM line ends when the hasher's block does, and read the comment kind from the GFM line rather than the piece | It is the third patch to a second rule, after round 1's head test and round 2's `cut` set. The reader's rule would still be a separate statement of the hasher's, and the next divergence would be a fourth round | rejected |
| **B. Round 3's fix, and leave `comment_blocks`' TEXT path in place**: change `riders_in` alone, and correct the one docstring sentence that says `riders_in` passes the text | The TEXT path stays in a shipped script with no caller and no test, and its docstring describes a step-over nothing applies. A later caller passing TEXT revives the second rule this item exists to remove. It saves no ledger work: the docstring edit moves `comment_blocks`' anchor, and G13, P5-1 and S3 are re-read either way (spec M10) | rejected. It is the smaller diff, and that is its only advantage |
| **C. Round 3's fix, and remove the TEXT path and the flag only it read** | The diff reaches two more units, `#gfm_places` and `#inferred_anchor`, one of which `--migrate` depends on. The index edit there is mechanical, and G13's `inferred_anchor` cases pin it | **chosen** |
| **D. Also drop `#quoted_lines`' TEXT parameter** | It reopens work item F's oracle case and R1-1's walk claim, which are not about where a rider ends | rejected, spec §*Scope* |
| **E. Make the hasher read pieces instead** | The hasher's lines are the ones `resolve_unit` and `ast` number (#664's work item C). Moving it would reopen the class C closed | rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `#riders_in` from the hasher's blocks; `#comment_blocks` without TEXT; `#gfm_places` returning line numbers; `#inferred_anchor` and round 2's case indexing them; every touched docstring true; the class case (S1–S4) and the verdict case (S5), each seen red at `6321dbdc`, S4 against its named mutant; the ledger (below); the changelog fragment; `phases/phase-1.md` and `overview.md` | S1–S11. Narrow: the item's module, `tests/test_a_rider_reaches_its_file.py`, `tests/test_the_hooks_hide_what_a_renderer_hides.py`, the floor case, `ruff check` and `ruff format --check` on the touched files, `evidence_check.py .`, and the probes S6 and S7 name. The broad gate is the sealer's | 28e9bdb2 |

**Order inside the phase, for the red to mean something.** Write the two
cases first and run them against `6321dbdc`'s `rider_check.py`, recording
which parameters fail. Then the fix. Then the removals, with the cases green
between each. Then the S4 mutant and the S6 and S7 probes, against the base
file loaded beside the new one the way G's round 3 did.

## Ledger

Drafted as the phase goes and written once, at its close.

- **New, in `seal/ledger/1790683267-a-rider-read-ends-where-the-hasher-cuts.md`.**
  K1: every piece of every rider `#riders_in` reads lies on a GFM line inside
  a block `#comment_blocks` over GFM lines returns, and every marker piece
  starting inside such a block starts exactly one rider, in every file type
  and across the eight characters. Anchored to `#riders_in`, `#comment_blocks`
  and the class case. K2: a break inside a cut line changes no verdict,
  anchored to the verdict case and `#riders_in`.
- **G13** (`seal/ledger/1790655302-…md`). Its claim is kept as written: it
  was false at `6321dbdc` for the two shapes and is true by construction now.
  A `Re-read` note says so and points at K1. Its three rider anchors move
  (`#comment_blocks`, `#gfm_places`, `#inferred_anchor`) and are re-stamped,
  and so is the round 2 case's anchor, whose `[0]` goes. Its clause that
  `#gfm_places` reads a piece on GFM's numbering still holds.
- **P5-1** (`seal/ledger/1790645290-…md`). Its own `Corrected` note says
  `comment_blocks` now steps over a mid-line marker piece in every file type,
  and that is false after this item. It takes a `Corrected` note: the
  step-over is gone, `riders_in` takes the hasher's blocks, and a Python file
  carrying a marker still loads the walk, now for `gfm_lines`. Its
  `#comment_blocks` anchor is re-stamped.
- **R1-1** (the same file). It lists `#comment_blocks` and `#riders_in` among
  the callers that hand the walk the text, which is false after this item and
  drifts no anchor it carries. It takes a `Corrected` note: on the rider side,
  only `#quoted_lines` takes the text, and no shipped caller passes one.
- **S3** (`seal/releases/0.9.1.md`). `#comment_blocks` moves. The opening and
  closing rules it states are untouched, so a `Re-read` note and a re-stamp.
- **S2** (the same file). Its anchor does not move. Its last note says
  `riders_in` "steps over a marker line that starts inside a GFM line, so no
  rider is read that `region_lines` does not cut", which describes a
  mechanism this item removes. A `Re-read` note records that the reader now
  reads the hasher's blocks, so the claim holds by construction.

## Operational impact

None. No new dependency, no environment variable, and no change to a format
anybody writes. The rider check's command line is unchanged.
