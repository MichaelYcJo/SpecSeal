# 1790208643-the-spec-is-split-and-its-sentences-are-settled — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 6c5c5295 |
| Ran by | specseal:smith on Claude Opus 5.5 (1M context) — the agent as the spawn prompt's first line names it, the model as the commit trailer it prescribes names it |

## What this phase was asked

The split, exactly as `plan.md` §*Where each section goes* says, with the
moved sections carrying A, B and C's sentences unchanged — a move is silent to
the sweep and a move-and-edit is a source — and the rewordings in §*What the
move has to reword* and no others. Re-point the ledger anchors the move
changes by `CONTRIBUTING.md`'s rename paragraph (a `Re-read <date> — moved by
#526's split` note and `--reverify`, never REMOVED). Do not edit `CLAUDE.md`.

## What this phase found

**The frame holds, and the split was made by line ranges asserted at each
boundary.** The script read every range by its first line, asserted that each
section ends on a blank line and that the ranges use every source line exactly
once, and wrote the three files (executed). A line-multiset comparison with
headings normalised shows the three files hold every source line except the
three lines of the old opening paragraph, which were rewritten (executed).

**M1** (executed, `wc -l`): `docs/review-chain-spec.md` 878,
`docs/commit-review-gate-spec.md` 523, `docs/round-record-spec.md` 885. All
three are under 1,000 lines, so the four-file fallback is not taken.

**S2, the markers** (executed, `unverified_check.live_lines` and
`FOLD_MARKER`): 9, 4 and 16 live markers, 29 in total, 26 distinct ids, with
digest `8f8c4d85f213eb9b`, the same as the base's. `bin/settle` exit 0, and its
output is byte-identical to the phase-0 run (`diff` exit 0).

**S1, the ceiling, seen red first** (executed, `bin/test
tests/test_a_document_has_room_for_the_next_fold.py -q -p no:xdist`, exit 1,
before the constants were emptied):

```
E       AssertionError: docs/review-chain-spec.md is 878 lines, no longer over the ceiling of 1000. Remove its entry; MichaelYcJo/SpecSeal#526 was its home
E         docs/review-chain-spec.md carries 9 fold markers and is frozen at 29 until MichaelYcJo/SpecSeal#526 splits it. …
4 failed, 12 passed in 0.14s
```

It is green once `OVER_CEILING` and `FROZEN_IDS_DIGEST` are empty and the
evidence ledger's bullet says no document is listed.

**The rewordings: the plan's list, one row corrected, and five more the build
met.** Each is a positional reference that dangles in its new file.

| Where | What changed | Plan row |
|---|---|---|
| R, opening | names the three files and what each is the authority for | yes |
| R, *The floor* | *like the two above* → `Fixes checked by` and the fix surface's two rows in the record document. **The plan said `Pass` and `Fixes checked by`, and that is wrong**: `Pass` is read on the last record only, and §*The fix surface* opens *Two more rows, read on every record the same way `Fixes checked by` is* | yes, corrected |
| R, *The floor*'s table and the paragraph under it | *the grandfathering above* → *the grandfathering those rows use*; *the reason the rows above are* → *the reason those rows are* | no |
| R, *`Needs a fix`* | *where the three above grandfather only an absent row* → names the floor above and the fix range and fix surface in the record document | no |
| R, *Two records* | *The refusal table under §`Fixes checked by`* → names the record document | no |
| R, *When the record was written* | *like the four above* → the floor above, and `Fixes checked by`, the fix surface and `Ran by` in the record document | yes |
| R, *What the record carries* | *a way this document already refuses* → this document or the record document; *the arrow's and the comma's limits above* → in the record document; *the third declaration in this document* → *the third declaration, the other two being that document's*; the moratorium's *Every field this document describes* → this document and the record document | yes, the first three; the moratorium no |
| R, *What a draft is excused* | *every arm above* → every arm of the pull-request check, this document's and the record document's | no |
| G, *The declaration* | one pointer sentence under the at-pull-request table; *(§*Two records…*)* → names `docs/review-chain-spec.md` | yes, the first; the second no |
| C, *What ran the round* | *like the three above* → `Fixes checked by` and the fix surface above and the floor in the run document | yes |

Two lines of the gate document were re-wrapped with no word changed (a
139-column and an 89-column line, both in §*Which repository*), so the file
meets `tests/test_docs_line_wrap.py` and joins `COVERED`.

**M2, the sweep** (executed, `bin/survivor-check --range
origin/release/v0.15.1...HEAD`): at `6c5c5295`, exit 0, *no removed wording is
still standing*, against 1,149 removed sentences. None of the rewordings is
reported, because no old positional sentence has a copy elsewhere, so
`survivors.md` needs no row for the split. An earlier run at `7bcc646e`
reported one place, exit 1: a re-wrap of the record document's one 89-column
line — a path and its comma in §*The fix surface* — had reworded
*confirmed at* into *as finding 11 of … confirmed*, and `seal/ledger.md` row R4
quotes the old wording. That line was restored byte for byte in `6c5c5295`,
and `docs/round-record-spec.md` stays out of `COVERED`, with the reason in
the comment there. The frame's plan to cover both new files does not hold for
that one.

**The citations re-pointed: 22 shipped lines, not 20** (read, then each
replacement asserted to match once). The frame's 20, plus
`hooks/commit-review-gate.py:308` (*an unresolvable target*, which lives in
the gate document and which the frame's list missed) and
`skills/code-review/SKILL.md:290`, C's *One depth per finding* paragraph,
which cites §*The depth in `New units`* and landed after the frame was drawn.
The gate document (G): `docs/worktree-guard-spec.md:417`,
`docs/the-evidence-ledger.md:262`, `hooks/cmdline.py:1297,1375`,
`hooks/routing.py:26`, `hooks/mode-gate.py:63`,
`hooks/commit-review-gate.py:308,487,502`. The record document (C):
`skills/code-review/SKILL.md:284,290`, `skills/code-review/orchestration.md:304,348`,
`round_record.py:3051,3738`, `chain_check.py:552,2424`,
`templates/sdd-round.md:163`, `docs/review-handoff-protocol.md:378`,
`agents/warden.md:206`. Both READMEs name the gate document beside the run
document, and the Korean one says *세 문서* now. Every other line naming
`review-chain-spec` in `agents/`, `skills/`, `hooks/`, `templates/`, `docs/`,
both READMEs and `CONTRIBUTING.md` — 51 lines after the edit — names a
section still in the run document, or the run in general (read one by one).
A script over the same files that resolves every `§*…*` citation of the
three names against that file's headings found 36 resolving and one false
negative: this branch's own `§`Fixes checked by``, whose backticks the script
does not strip (executed).

**S18's wording does not hold as written.** It says `git diff --stat` names
no file under `hooks/`, but `spec.md` §*Data & interfaces* lists four hooks
whose comments cite a section the gate document now holds, and leaving them
would break S4. The edits are to comments and docstrings only, with no
behaviour change. The reviewer weighs whether S18 meant *no behaviour under
`hooks/`*.

**The ledger** (executed). The checker reported 12 anchors BROKEN and 16
DRIFTED after the split. The repository-wide scan that would heal a moved
anchor is skipped over 200 files, so none healed on its own and all 12 were
re-pointed by hand. 18 rows carry the 19 moved anchors, 17 in
`seal/ledger.md` and D1 in `seal/ledger/1790206437-…`, re-pointed as follows:

- `### Review arm …` and `### Parity arm …` (one row) move to the gate
  document at their level.
- *Five values can stand in the reach half …* (one row) moves to the record
  document.
- `### The floor …`, `### `Needs a fix` …`, `### The reopening …` (three
  rows) and `### What the record carries …` (one row) stay in the run
  document at the new level.
- `## A verdict row that commissions nothing` (two rows), `## The fix range`
  (three), `## The fix surface` (one) and `## The depth in `New units`` (four,
  one of them D1) move to the record document at the new level.

Each row's `Checked` cell is 2026-09-24 and its Notes cell ends *Re-read
2026-09-24 — moved by #526's split, the claim unchanged.* 18 more rows drifted
because a citation inside their anchored unit was re-pointed. Each was re-read
and noted *#526's split re-pointed a citation inside the anchored unit …; the
claim unchanged*: `chain_check.py`'s vocabulary comment, `#says_not_yet` (two
rows), `round_record.py#depth_two` (four, D1 among them), `#return_literals`,
`skills/code-review/SKILL.md` §*Findings format* (three),
`orchestration.md`'s two headings, `COVERED` (two), `#touches_code`,
`agents/warden.md` §*Role* (three), and the run document's §*Two records*.
P1 (`OVER_CEILING`, `FROZEN_IDS_DIGEST`) is noted with the listing emptied.
One row anchored on a section of `seal/ledger.md` itself drifted because
those notes landed inside it, and it was re-read and noted too.
`evidence-check --reverify .` re-stamped 39, then 1, then 6 rows. Then
`evidence-check --strict .` exit 0, `total: 1767 ok · 0 drifted · 0 broken`,
the same total as the base. D (#558) has not landed, so every one of these
rows is re-pointed in the file it is in today. The resumed phase 3 finds out
where D moved them.

**Phase 2's modules are red at this commit, as the plan's order makes them.**
`tests/test_one_word_one_meaning.py::test_the_two_prompts_are_named_by_who_they_address`
reads the deny/ask paragraph, which moved to the gate document (executed:
one failure among phase 1's modules). Its re-point is phase 2's.

**What `CLAUDE.md` needs: nothing from this phase.** It does not name
`docs/review-chain-spec.md`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/review-chain-spec.md`'s hook, record-row and generator sections | `docs/commit-review-gate-spec.md` and `docs/round-record-spec.md`, byte for byte except the rewordings above |
| The old three-line opening (*Authority for `hooks/commit-review-gate.py` and `hooks/review-history-guard.py`, and for the cycle contract …*) | the three new openings, each naming the other two |
| `OVER_CEILING` and `FROZEN_IDS_DIGEST`'s entries for `docs/review-chain-spec.md` | `docs/the-evidence-ledger.md`'s ceiling bullet, which now records the split |
