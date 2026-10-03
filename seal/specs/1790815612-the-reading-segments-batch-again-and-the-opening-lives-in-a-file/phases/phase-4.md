# 1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file — phase 4

<!-- seal/specs/<unix-epoch-seconds>-<slug>/phases/phase-<N>.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 0a35beff |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

Spec I10 and I11, `plan.md` phase 4: merge `origin/release/v0.17.0` in only
where item A (#641) or B (#638) has landed and touches what this phase reads,
never a rebase; `evidence-check` at the tip, every drifted row re-read and
re-stamped where it stands; `seal/releases/0.4.0.md`'s bars row corrected in
place; new rows in this work item's fragment. Then the tip's `--segments`
over the orchestrating session's transcript — handed over by the spawn prompt
as `/Users/x/.claude/projects/-Users-x-Documents-GitHub-SpecSeal/b5ffa967-bd00-4976-b4ed-5a1751a5b58e.jsonl`
— with this frame's row graded against 1.4 and its largest batch, labelled
executed and as one reading. The six framers of the run ran on Fable 5.1 and
the smiths on Opus 5.5 (the owner's split, 2026-10-01, as the spawn prompt
gave it).

## What this phase found

- **No merge.** `git log HEAD..origin/release/v0.17.0` was empty after a
  fetch: neither A nor B had landed, so the tip is this branch's own and
  `correction-check` over the range found no merge commit.
- **Q4: 22 rows in nine files, more than the spec counted.** `evidence-check`
  prints each drifted anchor once per ledger, so its 16 lines stood for 22
  rows: `seal/ledger.md` 97; `seal/releases/0.11.3.md` 47, 51, 52;
  `0.13.1.md` 89; `0.15.6.md` 41; `0.15.7.md` 12, 13, 14, 15, 17, 33, 41;
  `0.4.0.md` 114; `0.8.0.md` 104; `0.8.2.md` 41, 42, 145; `0.9.5.md` 12, 16,
  45, 54. Outside the spec's expected set: `seal/ledger.md` 97 (the
  `## The handoff before round 1` anchor encloses the bars subsection),
  `0.11.3.md` 47, 51, 52, `0.13.1.md` 89, `0.15.6.md` 41 and `0.15.7.md` 12,
  13, 14 — all of them on a unit the spec named, carried by rows in files the
  count did not reach. Each claim was read against this branch's edits.
  Twenty hold and got a dated `Re-read 2026-10-01` note. Two did not:
  - `0.4.0.md` 114 listed three bars and its note said *the script cannot
    tell segment kinds apart* — corrected in place, claim and note, with
    `Corrected 2026-10-01`.
  - `0.15.7.md` 13 (A2) said *only the label differs* between the two routes,
    and `kind` and `bar` differ too — corrected in place, claim and note.
  Then `evidence-check --reverify --checked 2026-10-01 --ledger <file>` per
  file, and the tip reads exit 0 (read directly, `>/dev/null 2>&1; echo $?`).
- **Shared tails made the edits position-sensitive.** Fourteen of those rows
  end in a byte-identical note from #642's fix pass, so an `Edit` on the tail
  alone matches several rows. Each was anchored on the tail plus the next
  line's start, rows followed by a blank line last, after the others had made
  their tails unique. No row was edited by a shell substitution.
- **The fragment.** Rows P1–P4 and G1–G3, written with placeholder hashes and
  filled by `--reverify` on the fragment alone; re-stamped once more after the
  counts line's wrap moved `report_grades`.
- **The reading (S15, Q1), executed:** the tip's `--segments` over the run's
  transcript, exit 0. Twelve rows: six `specseal:framer`, six
  `specseal:smith` (this one still running). The grade block read
  `every graded row meets its kind's bar` and `6 graded, 6 exempt, 0
  ungraded`. This frame's own row, `Frame #640 batching segments`: **50 calls
  over 12 turns, 4.17 tools per turn, largest batch 11 calls**, five largest
  turns 11, 7, 7, 6, 5, and the segment finished. The largest batch was read
  by grouping the segment's calls by the turn key `load` gives them; `--json`
  carries the ratio and not the per-turn maximum. The other five framers of
  the run read 1.81–4.64 with largest batches of 8–12. One reading of one
  frame on one model; nothing is drawn from it beyond `questions.md` Q1's own
  test, which it meets: the largest batch is well above six and nothing
  stalled, so A1's *about six* is loose and the owner may raise it.
- **The real page showed one ragged line.** The counts line ran *The bars
  are* alone at the end of a short line and the next line out to 86 columns;
  it is re-wrapped so the widest line of the block is 84, and the cases that
  read it were re-run green.
- **`survivor-check --range cd24f516..HEAD`**, exit 0: 49 removed sentences
  against 555 files at `0a35bef`, *no removed wording is still standing*. No
  `survivors.md` was needed, and the first call, naming one that did not
  exist, exited 2 on that alone.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
