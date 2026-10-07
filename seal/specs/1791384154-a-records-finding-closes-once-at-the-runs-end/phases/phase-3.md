# 1791384154-a-records-finding-closes-once-at-the-runs-end — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 1e9d98f0 |
| Ran by | smith on Opus 5.5 (filled by the orchestrating session, which spawned it with `model: opus`) |

## What this phase was asked

`close` carries a note: the `missing` demand excludes ⬜ rows, a ⬜ row in the
fix table is refused naming the rule and `notes`, and `close`'s print and
`new`'s output carry `N notes open across the run — closed once at its end by
notes`. The two fixtures that close a ⬜ through `close` move:
`test_a_correction_closed_answered_lands_on_no_fixes_to_check` closes its ⬜
through `notes`, and the `⬜ 2 … deferred #664` fixture row in the sealer test
is closed through `notes` or regraded. The `COMMISSIONS_NOTHING` comment and
`close`'s *One row per OPEN finding* comment reworded. Verified by cases for
S1 and S2, seen red against phase 2's `close`, and
`tests/test_a_finding_id_is_a_bare_integer.py` green with the message's new
clause.

## What this phase found

**A third fixture closed a ⬜ through `close`, and the frame's count of two
missed it.** `tests/test_a_finding_id_is_a_bare_integer.py#test_a_severity_marker_still_leads_the_cell`
is parametrized over six markers, ⬜ among them, and closes `| ⬜ 1 | fixed |`
through `close` — written as an f-string over the marker, so a grep for a
literal `⬜ <digit>` row does not find it. The case holds that the id is read
through the marker; for ⬜ it now holds it through the refusal, which names
`⬜ 1` by the id it read.

**The sealer test's `⬜ 2 … deferred #664` row stays as it is.** It is a
fixture record for `broad_gate.rounds_rows` (the capped run's panel), built
as text and never passed through `close`, and `deferred <home>` is one of the
three closings a note takes at the run's end. Nothing in it says how the note
was closed, so it reads the same under the new rule; the whole sealer module
passes.

**`close`'s refusal of a ⬜ row comes before its other two row refusals**, so
a row for a note already closed is named as a note rather than as a finding
the reviewer closed. Q4's two remaining lines, each pinned by the case beside
it:

- `close` over a ⬜ row — *the fix table has a row for ⬜ 3 of round 1, and a
  note takes no row in a fix table: it commissions nothing while the run
  runs — no fix pass and no reader — and closes once at the run's end, with
  every other note of the run, by `round-record notes --item <dir> --fixes
  <table> --at <sha>`. Take the row out. …*
  (`test_a_note_takes_no_row_in_a_fix_table`)
- the carried count, from `new` as its own line and from `close` as a clause
  of its summary — *N note(s) open across the run — closed once at its end
  by `round-record notes`* (`test_new_says_how_many_notes_the_run_carries`,
  `test_close_carries_a_note_open`)

**`close`'s `missing` message keeps *left with no row in the fix table***, the
phrase two cases assert is absent where it must not fire
(`tests/test_a_finding_id_is_a_bare_integer.py:1006`,
`tests/test_the_fixes_close_the_record.py:526`), and gains *a ⬜ note takes
none and is carried to the run's end*.

**The landing exclusion phase 2 put into `close` is reached here**, and only
by a record whose other rows closed without a fix word: with a `fixed` among
them the landing is pending anyway. A case for that shape was added, because
the one phase 2 carried could not tell the exclusion from its absence.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the demand that every open ⬜ take a row in its round's fix table | `skills/code-review/orchestration.md` §*A note closes once, at the run's end*, through `round-record notes` |
| *a ⬜ is "fixed in passing or not at all"* in `COMMISSIONS_NOTHING`'s comment | the same section; the comment now says a ⬜ is carried open and closed by `notes` |
