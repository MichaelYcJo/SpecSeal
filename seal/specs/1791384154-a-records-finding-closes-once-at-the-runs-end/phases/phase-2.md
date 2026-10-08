# 1791384154-a-records-finding-closes-once-at-the-runs-end — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 45077c75 |
| Ran by | smith on Opus 5.5 (filled by the orchestrating session, which spawned it with `model: opus`) |

## What this phase was asked

`round_record.py notes --item --fixes --at [--baseline]`: the run's-end test
shared with `seal`; `fix_table(…, notes=True)` admitting `corrected` and
refusing `fixed` with the rule's sentence; `--at` resolved, an ancestor of
HEAD, not an ancestor of the run's last `Target SHA`, required while a row
reads `corrected`; every open numbered ⬜ of the run takes a row, and a 🔴/🟡
row or a row for a note already closed is refused; cells written the way
`close` writes them; `Pass` re-derived per record; `reach_forward(…, into=K)`
for every later record; the chain check. `seal` and `seal --check` refuse
while a note is open. `close` itself unchanged. Q1 answered (a), so no
`behaviour_path` arm on `--at`. Verified by cases for S3, S4 (three), S5, S6
and S9, the `seal --check` cases, and `test_the_fixes_close_the_record.py`
untouched and green.

## What this phase found

**The two frame gaps phase 1 found are built here.** The notes table carries
a `Round` column (`round_of_cell`; a bare-id table is refused by its header,
naming the notes table's). An open note is left out of the landing that
`build` and `close` derive, and kept in `Pass`; without it no generated
record carrying a note could read `no fixes to check`, and every S4 case
would have had to hand-write the cell. `close`'s half of that change is in
the tree and unreachable until phase 3: `close` still demands a row for
every open ⬜, so no note reaches its landing open.

**The three lines a person reads that this phase writes (Q4)**, each pinned
by the case beside it:

- `notes` before the run's end — *round-N.md is the last record of the run
  and its `Fixes checked by` reads `<value>`, so the run has not ended. A
  note closes once, at the run's end — when the run's last record reads
  `Fixes checked by | no fixes to check`: …* (`test_notes_refuses_before_the_run_has_ended`)
- `fixed` in a notes table — *round-K's note N is `fixed`, and a note never
  closes on a fix word: …* (`test_fixed_on_a_note_is_refused_with_the_rule`)
- `seal` over an open note — *N note(s) of the run is/are still open:
  round-K.md's ⬜ N. The run has ended — … — and a note closes once, at the
  run's end, before the broad gate seals it: `round-record notes --item <dir>
  --fixes <table> --at <sha>`* (`test_the_seal_waits_for_the_notes`)

**`seal`'s new refusal sits before the `Pass` refusal and fires only where
the run has ended.** Before the end, the `Pass` and `Fixes checked by`
refusals are the true ones and `notes` would refuse as well; after it, a note
on the last record would otherwise meet *`Pass` is unchecked — a finding is
still open*, which names no way out. `seal`'s docstring counts seven `raise`
sites now, and `--check` eight with `seal_home`'s.

**The corrected grounds name `--at` in eight hex characters.** `close` writes
the commit as the fix table typed it; `notes` resolves `--at` (so `HEAD` is a
legal spelling at the keyboard) and writes the resolved commit, the length
`plan.md`'s Status cells use.

**A stopped run's notes are read only until the redesign's first record.**
`seal` and `chain_check.carried_notes` read the run the last record belongs
to, so a note a `second` left open stops being read once a later record
exists. `notes` is run at the `second`, before the framer is spawned
(`spec.md` S9), and nothing in the tree refuses the redesign's first record
over an earlier run's open note. `overview.md` §*Not done* says so.

**Q2, measured** (executed over the 33 records at `v0.19.0` and 5623d728;
every commit resolved through the 148 fetched `refs/remotes/pull/*/head`):
35 numbered ⬜ rows of 14 records closed `fixed`, and the commit named in 23
of them touched a `behaviour_path` — 14 distinct commits. Per commit rather
than per row, so 23 is an upper bound. `questions.md` Q2 holds the list of
kinds.

**The fixture for S9 sets the floor `yes` until the stop.** Three records
after a floor `no` are refused by the floor's count walk, which is the run
carrying on, not the stop; a run that reaches a `second` is one that kept
finding things.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
