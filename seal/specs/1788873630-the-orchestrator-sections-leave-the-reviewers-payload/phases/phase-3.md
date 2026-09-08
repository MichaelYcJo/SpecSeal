# 1788873630-the-orchestrator-sections-leave-the-reviewers-payload — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | c5cf5d2 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Fix the test modules the split breaks. The task named eleven that pin the
path and two that need more than a path swap, and said to treat the eleven as
an enumeration to verify by construction — *if there are twelve, the ticket
was written by reading*, and saying so is worth more than a silent twelfth
fix.

## What this phase found

**There are 21, and the eleven are the wrong eleven.** Eleven modules name
`skills/code-review/SKILL.md` as a path — that count is exactly right — but
ten more name it as the Python tuple `("skills", "code-review", "SKILL.md")`,
which no path grep reaches. This session's own first check had the ticket's
hole: it greped the path over `tests/`, got eleven, and confirmed the ticket.
The tuple form was found only when a failing test turned out to be in a
module the count did not contain.

**Failure and membership are different sets.** Of the ticket's eleven, six
pass untouched, because what they pin stayed in the reviewer's half. Five
modules the ticket never named broke:
`test_a_record_says_what_ran_it.py`, `test_review_axes.py`,
`test_the_fixes_name_their_surface.py`,
`test_the_handoff_names_the_form_it_ran.py` and
`test_the_last_rounds_fixes_are_checked.py`. Plus the twelfth the ticket also
missed, `test_a_record_precedes_the_fixes_it_commissions.py`. Eleven modules
failed in total — a different eleven.

**`tests/test_docs_line_wrap.py` is the one no test run could have
reported.** It checks a fixed list of paths, `COVERED`, which named
`skills/code-review/SKILL.md`. 418 lines of wrap-covered prose left that file
and the new file was not on the list, so the coverage was lost with nothing
going red. Added to `COVERED`; both files measure zero prose lines over 88
columns.

**Two cases had to be counted across both halves rather than re-pointed**,
which is what keeps them meaning what they were written to mean. Both copies
of the sentence they count moved into the new file together, so a count taken
in the new file alone would go green again the day one copy moves back — and
the disagreement that shape produces is the whole reason each case exists.
`test_a_fix_pass_may_add_a_unit.py`'s exit-sentence count and
`test_the_rules_have_one_owner.py`'s reopening-link count now sum over
`SKILL.md` and `orchestration.md`. The two absence halves —
`UNLESS` and *The habit that makes all of it moot* — read both halves for the
same reason: an absence checked in one file is satisfied by the sentence
coming back in the other.

**One over-replacement, caught by the run rather than by reading.**
`test_the_run_stops_at_the_last_finding.py` reads the floor, which moved, and
in exactly one case reads the record-contents table row, which stayed. The
module now carries both names, and the case that reads the reviewer's half
says in its docstring why it is the one.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| Nothing. Sixteen references in twelve modules change the file they name; no case is deleted and no assertion is weakened | none |
