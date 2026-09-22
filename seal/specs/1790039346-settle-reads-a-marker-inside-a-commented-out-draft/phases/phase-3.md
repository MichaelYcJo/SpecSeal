# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — phase 3

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `7605feb4` |
| Ran by | `specseal:smith` on Fable 5.1 — the agent definition names no model, the spawn passed no override, and the spawning session named its own model in the prompt |

## What this phase was asked

**A line is live by one rule, and every reader asks it.** `blank_code_spans` (NAME NOT IN TREE)
and `live_lines` in `unverified_check.py`; `folded_items` reads through
`live_lines` and the stub in phase 2's case also covers it; `coordinates`
reads both loops through `live_lines`, extracting coordinates from the
fence-blanked text; the three docstrings and the `FOLD_MARKER` comment say the
rule and its single-line limit, and `coordinates` stops attributing the fence
rule's second copy to #487. Findings 2 and 3 of round 3.

Verified by A2 red against the tree; A3 and A4 red by mutation (the span pass
removed); A5 red by mutation (the fragments loop back to a whole-file
`finditer`, round 3's M7); A8 executed at the tip and quoted in
`overview.md`; A9 over the four modules; A10 read. Ledger rows for the two
new units, `coordinates`, `folded_items` and the cases; S1 and S3 re-read in
the parent's fragment with a dated note; `changelog.md` written. Q1 measured
and written into its row; Q2 decided.

## What this phase found

**Every case was red where the plan said, and one was red in a way the plan
did not name.** Against the tree at `3cdfd8ad`: A2, A5, the seventh comment
shape in `docs/` (`` `<!--` `` a line above a marker), the stub assertion on
`live_lines` and the five span shapes — the last two as `AttributeError`,
the names not existing yet. A3 passed against the tree, as it should: it pins
the departure from the naive closure, and the tree had not taken the naive
closure. Then, with the code in and 173 cases green, four mutations applied
alone and restored from a byte copy:

| Mutation | Red |
|---|---|
| the span pass removed from `live_lines` | A3 · A4 · the `docs/` seventh comment shape — A4 naming `1788472135-the-run-outlives-its-last-finding`, `1788613827-a-runs-report-carries-one-comparison-table`, `1788844127-the-reviewers-report-reaches-the-record-retyped`, round 3's three lost markers |
| the fragments loop back to a whole-file `finditer` (M7) | A5, alone — the mutation that turned nothing red at `02b2038d` |
| `blank_code_spans` as round 3's loose regex `` `+[^`]*`+ `` | two of the five span shapes: the double-backtick span holding a single backtick, and an unmatched opener followed by a closed pair (NAME NOT IN TREE) |
| `folded_items` no longer asking the answer | the parked-draft case and two comment shapes — the switch to `live_lines` lost no pin |

Each pattern was asserted to match once, and `git status` was clean after
each restore.

**A2's fixture in the spec cannot be built as written, and the reason is the
scanner's rule, not the span rule.** Spec A2 says a commented-out draft
*holding a marker and a coordinate row* has its coordinate attributed to no
work item. HTML comments do not nest: a marker inside a draft closes the
draft with its own `-->`, so a row placed AFTER the marker is live again and
falls to whichever section was open — the first form of the case put it
there and saw `hooks/quoted.py` land in `gamma`. That is `comment_scan`'s
reading, which `seal/ledger.md:80` pins for every record reader, and it is
the c-3 shape the comment-shape family already parametrises. The case puts
the draft's row BEFORE its marker, where the comment really encloses it, and
pins the row after the marker landing in the open section with the reason
beside it. `overview.md` carries the divergence with both sides quoted.

**Q1 holds.** `bin/settle` at `7605feb4`: `released and unfolded: 81 work
items in 37 segments, 16 ungrouped, 0 skipped`, exit 0 read directly. The
probe behind it: 83 distinct ids sectioned by the fence-only reading, 80 by
the naive closure, 83 by the composed rule; 787 lines not live under the
naive rule, 761 under the composed one — the framer's figures at
`3cdfd8ad`, reproduced.

**Q2 is the sentence.** `blank_code_spans`'s docstring names the rule (NAME NOT IN TREE)
(CommonMark 6.1, equal-length backtick strings), the limit (single-line), the
shape it therefore does not blank, and the failure direction (fewer lines
live, a fold reported as a deletion). No case pins the multi-line shape: no
record here has carried one, a table row cannot, and a case for a shape
nobody has met would pin the naive rule's reading of it as though it were
chosen rather than tolerated.

> **Corrected 2026-09-22, round 1's finding 2.** The direction named in the
> paragraph above is the OPENER's, and it is not the only one. A multi-line
> span holding a MARKER is not blanked either; the marker survives, reads as
> a fold record although it is a quotation, and `settle --retire` removes the
> directory at exit 0 — the expensive direction, in a shape this phase's
> sentence said could not occur. Two things this phase asserted were wrong:
> that the limit's failure direction is the safe one, and that the shape has
> never occurred here. Measured after the finding: six top-level `docs/`
> documents carry fourteen multi-line code spans; none holds a delimiter or a
> marker, which is the whole of what keeps the door harmless. What was right
> is that the door is not this work's to close — the base's reader answers
> the same set, and closing it needs span state across lines. The docstring
> carries both halves now.

**The equal-length rule is pinned by a case of its own, which the plan did
not ask for.** The plan kept the loose regex as acceptable, so the difference
between the two was a property nobody would be told about if the next editor
simplified it back. Five shapes, one parametrised case; two of them red under
the loose regex.

**The reader still runs on 3.9.** `/usr/bin/python3` 3.9.6 imports the
module and answers `live_lines` and `blank_code_spans` correctly; the only (NAME NOT IN TREE)
constructs added are `enumerate`, `next(…, None)` and a list-slice
assignment. `tests/test_a_script_says_which_interpreter_it_needs.py` and
`tests/test_chain_hooks.py` are green together, 58 cases at exit 0, so
`readable()`'s pass list is untouched.

**What the frame got wrong about the tree, found while writing the ledger.**
`evidence-check --strict .` reads this work item's records once its fragment
exists, and reports two BROKEN coordinates at `spec.md:30` — the framer cited the
parent's S1 and S3 anchors, `folded_items` and `coordinates`, with the file's
basename alone (`unverified_check.py`, `settle.py`) and no directory. The
checker finds the same name at the full paths and says so. `spec.md` is the framer's
file and not on this builder's list, so it is left as it stands and named in
the hand-back; the eleven NOT-IN-TREE reports for `live_lines` and
`blank_code_spans` from the same run resolved themselves when the names (NAME NOT IN TREE)
landed.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `folded_items`'s two-call read (`blank_fences`, then `opens_outside_a_comment` over the result) and the `enumerate` comment beside it | `unverified_check.py#live_lines`, which composes the same two readers with the span pass between them and carries the comment |
| `coordinates`'s `blank_fences`-only read of both loops | both loops read `live_lines` |
| the sentence in `coordinates`'s docstring attributing the fence rule's second copy to #487 | none — #487 is about `open_rows`, and `open_rows`'s own docstring already names it correctly |
