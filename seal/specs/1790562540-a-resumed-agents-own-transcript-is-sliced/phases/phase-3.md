# 1790562540-a-resumed-agents-own-transcript-is-sliced — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 53c55a21 |
| Ran by | unknown — the spawn prompt named neither the agent nor the model, and this row is the spawning session's to fill |

## What this phase was asked

The ledger and the real transcript. `evidence-check` at the tip names the
drifted rows; each is re-read against the edit and re-stamped in its own file
with a dated note, and `Corrected <date>` goes on any claim the edit made
false. New rows go in
`seal/ledger/1790562540-a-resumed-agents-own-transcript-is-sliced.md`: the
trigger, the `own_file` key, `unnamed` over walked files, and the hint's
condition. S12: the ticket's three commands on a real resumed agent
transcript on this machine (`questions.md` Q1), with the slices from both
routes shown equal.

## What this phase found

**The drifted set was the frame's set, anchor for anchor.** `evidence-check`
at `b07698cc` (executed, exit 1, lenient): 2,502 ok and 11 drifted anchors
over 14 rows, in `seal/releases/0.11.3.md` (`#measure_segments`,
`#report_breaches`, two section rows), `0.13.1.md` (`#emit`,
`test_the_posted_body_does_not_carry_the_transcripts_path`, one section row),
`0.15.6.md` (`#report_segments` and the section), `0.8.0.md` (one), `0.8.2.md`
(two) and `0.9.5.md` (four). `plan.md` counted two section rows in `0.13.1.md`;
the second mention at its line 78 is prose above the table, not a row.

**No claim went false, so no row is `Corrected`.** Each of the 14 was re-read
against this branch's edits and carries a `Re-read 2026-09-28 by work item
1790562540 (#637)` note saying what changed and why the claim holds, with its
`Checked` cell set to that date. The one worth naming: 0.11.3's `report_breaches`
row says the §6 line names *the agent*; on an own file it names the row's
label, which is the file, and the note says so. Then `evidence-check
--reverify` (exit 0) rewrote the eleven hashes.

**Six new rows**, A1–A6, in the work item's fragment: the trigger (marker,
nothing beside, directory never), equal numbers by either route, the `--json`
shape with `own_file` and `unnamed` 0, the page, the plain hint and its
condition, and the two `SKILL.md` sentences. Written with a zero hash and
stamped by the same `--reverify`.

**After both (executed):** `evidence-check` exit 0, 2,535 ok, 0 drifted;
`evidence-check --strict` exit 0; `correction-check --range
origin/release/v0.15.7...HEAD` exit 0 (no merge commit in the range).

**S12, the ticket's three commands (executed 2026-09-28, at `b07698cc`).**
The file was picked with `resume_cuts` itself, over every `agent-*.jsonl`
under this repository's project directories: 336 files, 47 with at least one
coordinator message, none with transcripts beside it. The issue's figure of
55 was not reproduced here; it is not this work's number. `subagents/`
directories: 52, none under an agent's own `agent-<id>/`, which is the frame's
measurement again. The chosen file is a `specseal:smith` segment
(`<project>/<session>/subagents/agent-<id>.jsonl`) with 2 coordinator
messages, in a session whose main transcript has 20 segment transcripts
beside it.

1. `session_cost.py <agent file>`: exit 0. The page opens with *2
   coordinator messages in this transcript, so the span below covers every
   stretch of work and the waits between them — `--segments` prints one row
   per stretch*, then `span 106.5m (233 tool calls)`, idle 37.7m (35%).
2. `session_cost.py --segments <agent file>`: exit 0. The header reads *…:
   an agent's own transcript, cut at 2 coordinator messages into 3 slices*,
   and three rows print: 34.2m / 175 calls / 1.32 / 9s / 61,255,310 tokens;
   10.5m / 28 / 1.04 / 10s / —; 11.1m / 30 / 1.07 / 12s / —.
3. `session_cost.py --segments <session main transcript>`: exit 0. *20
   segment transcripts beside this one, 20 spawns in it, joined within 1.0s;
   0 segments named by nobody, and 0 spawns that claimed none.* The same
   agent prints as `specseal:smith 1/3`, `2/3`, `3/3` with the same three
   rows.

Compared through `--json` rather than by eye: the own file's three rows and
the walked run's three rows for that transcript are equal once the four
label fields are dropped. The three slices' calls sum to 233, the plain
reading's count, and their spans sum to 55.8m against its 106.5m. So `questions.md`
Q1 is answered the way S3 answered it on the fixture, and no new shape was
found.

**Narrow run (executed, at 53c55a21):** `evidence-check` exit 0 and
`--strict` exit 0 again; `bin/test` over phase 1's 43 modules plus
`tests/test_the_ledger_fragments_fold_at_release.py`,
`tests/test_a_merge_cannot_silently_drop_a_correction.py` and
`tests/test_a_question_says_who_can_answer_it.py`: 2,179 passed, 7 skipped,
exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
