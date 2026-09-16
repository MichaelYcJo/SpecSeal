# 1789518345-who-asks-the-routing-question-and-what-checks-the-answer — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 2f302790 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

The vocabulary. `hooks/routing.py` gains the fifth row with its two answers
and the row recording which answer was pressed, both optional and both
lenient, on the terms `Planning` has. `templates/sdd-routing.md` gains both
rows with the comment a session follows.
`test_the_fourth_axis_is_a_record_and_not_a_fourth_checkbox` is read first and
reworded where it names `Planning` by position rather than by name.

The spawn answered Q1 by keeping the frame's names. A correction arrived
mid-phase and overturned half of it: the owner's row name is `Automation`, not
`Attendance`, and its values are `yes` · `no` rather than the frame's
sentence-length pair. Question 1's third option stays `no work item`.

## What this phase found

**The row name the owner chose is the one the frame's Alternatives table
rejected, and the frame's reason for rejecting it does not survive contact
with the question's final shape.** `plan.md` rejected `Automation` as reading
*turn everything on*, which is what the three party boxes already say. That
holds where the row sits alone; it stops holding once question 1's first
option is itself labelled `automation`. A person presses `automation` and
reads `Automation` in the file, and one word across the button and the row is
what #88 asks for one level down. The collision sweep was run before the name
landed: all 40 occurrences of the word in the tree are the ordinary English
noun — *this repository's own automation*, *costs no automation anything* —
and none is a vocabulary word a machine reads, so
`tests/test_one_word_one_meaning.py` has nothing to say about it.

**What the shorter values cost, and where it is paid.** `nobody at the
keyboard` carried its own meaning; `no` does not, and its first reading —
*a person did this by hand* — is wrong. The row means *this run may stop to
ask*. That half now lives in the template comment and in the constant's
comment rather than in the value, which is the trade: a value a person types
correctly, against a meaning they have to read one line up for.

**The two constants sit one letter apart and are deliberately not renamed
apart.** `AUTOMATION` is the row and `PRESSED_AUTOMATION` is the label. A
second word for one of them is what makes a reader hunt for a difference that
is not there, so the pair is pinned instead:
`test_the_row_name_and_the_option_label_are_one_word_two_cases` asserts both
crossings read as unanswered rather than as a confident wrong answer.

**The case phase 1 was told to open was named for a position, and both its
assertions were.** `test_the_fourth_axis_is_a_record_and_not_a_fourth_checkbox`
counted the boxes at three and refused the string `four axes`. Neither is
about `Planning`, and both would have gone red at phase 2 for a change #88's
rule permits — a fifth row that genuinely IS a person's decision. A reader
meeting that red would have read it as the rule being broken. It is renamed
`test_the_planning_row_is_a_record_and_not_a_checkbox` and asserts by name:
no checkbox table anywhere in the section may mention `framer` or `Planning`.
`checkbox_tables()` finds those tables by a column named for a box rather than
by the one header spelling the old case hard-coded, so phase 2's two-question
shape is read by the same helper.

**The corpus case is the strongest red-first direction available for these two
rows**, and it was not in the plan's first mutation. No committed declaration
in the tree carries either row, so the population
`test_every_declaration_in_this_repository_still_parses` sweeps is all 84 —
and taking the `.get` default off the new row is red there and nowhere else.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `test_the_fourth_axis_is_a_record_and_not_a_fourth_checkbox`'s box COUNT (`len(boxes) == 3`) | nowhere — the count was never the rule. `spec.md` §*The ceiling* is what now holds the number, and phase 2 lands it beside the question it measures |
| The same case's `"four axes" not in flat(skill)` assertion | nowhere, for the same reason. The declaration's row count and the question's box count were one number and are now two, and neither is what #88's rule is about |
