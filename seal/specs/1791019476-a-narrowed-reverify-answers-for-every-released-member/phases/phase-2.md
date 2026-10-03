# 1791019476-a-narrowed-reverify-answers-for-every-released-member — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 62aa88a6 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build ⬜ 17: plant the S6 case pinning both substrings and see it red
against the old wording; give `family_view`'s emission loop D5's three
forms; add one sentence to the home's family paragraph saying that a
`Checked` date the calendar does not have orders nothing and is named as
written; add the changelog's second entry. Q2(b) is decided as the frame
chose.

## What this phase found

**D5 left one form unworded, and the case pins the choice.** D5 says the
second form names "each such string in cell order, joined by `, `", and
gives the wording for one string only. For two the line reads `the reading
dated 2026-13-45, 2026-02-30, dates the calendar does not have`: the plural
is the one change. A cell holding one calendar date beside an impossible one
is named by the calendar date, as before, because `checked` already orders
by it.

**Red first, executed.** The case is parametrized over three cells. Against
the wording at `6c104aa8`, the two cells holding impossible dates failed,
each reading `matches only the reading of no date`. The empty cell passed,
which is the third form kept.

**Mutations, executed with `bin/mutation-check` over the case, each red:**
the no-date test inverted; the plural dropped; only the first string named;
the calendar-date test inverted.

**The narrow run at the phase boundary, executed.** `bin/test` over the same
40 modules as phase 1: 2,289 passed, 7 skipped, 1 failed. The failure is
`test_a_record_states_what_the_tree_has.py`'s own-records case, which fails
on the base for the reason phase 1 records.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the emission loop's `checked(key) or 'no date'` wording | `family_view`'s `reading` helper, beside `checked` |
