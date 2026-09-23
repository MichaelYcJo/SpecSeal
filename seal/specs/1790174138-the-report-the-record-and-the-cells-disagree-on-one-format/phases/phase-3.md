# 1790174138-the-report-the-record-and-the-cells-disagree-on-one-format — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 9cd54120 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

What the checkers read out of a record — #436 and #217. `fix_range`'s
pending arm under `RANGE_FROM`, mirrored from `fix_surface`; `claim_lines`
holds an unclosed comment's lines the way it holds an unclosed fence's (the
ticket's `aside_held`). Cases A6, A7, A8. Ledger R5 and R6 re-read; a
sibling of R7 for `fix_range` in the fragment. Both are gate changes: the
four answers drafted into `overview.md` for the pull request body. Measure
Q3: how many live records end inside an HTML comment.

## What this phase found

**The frame holds for this phase.** `fix_range`'s `says_none` early return
was where `plan.md` put it, with nothing reading `Fixes checked by` above
it; `fix_surface`'s arm was the shape to mirror, cell, normalisation and
message alike; `claim_lines` had `aside = True` with nothing symmetric to
`held`. The ticket's paste-ready for #217 applied as written.

**Q3, executed: 0.** A walk over every `.md` under `seal/specs/` at
`9cd54120` — 144 files — with the arm's own region rules (a fence to its
marker, a comment to its `-->`) found none ending inside a comment. The same
walk over the records of the three branches open against
`release/v0.15.0` (#537, #538, #539, read through `git show` without a
checkout) found none either. The default holds: the arm fires on nothing at
the pull request, and nothing in it changes.

**The cutoff question #436 left open is answered as the frame chose:
`RANGE_FROM`, no new cutoff.** `fix_surface` keys its arm to `ORDER_FROM`
because its rows only began carrying the pending value from birth then;
`Fix range` was born carrying it, so the row's own cutoff excuses exactly
the records `ORDER_FROM` would and no fewer. The before-the-cutoff case pins
that the pair prints rather than fails one second before `RANGE_FROM`.

**Seen red at `65195f49`** (executed):

```
FAILED tests/test_chain_check_at_the_pull_request.py::test_a_fix_range_still_pending_after_a_round_read_the_fixes_fails
E       assert 0 == 1
FAILED tests/test_chain_check_at_the_pull_request.py::test_a_fix_range_still_pending_prints_for_a_work_item_begun_before_the_row
E       AssertionError: the state is reported
FAILED tests/test_a_record_states_what_the_tree_has.py::test_a_comment_the_record_never_closes_does_not_silence_what_follows
E       assert 0 == 1
```

The `nobody` case and the two aside pins were green at `65195f49` on
purpose: the first is the direction that must keep passing, and the other
two pin the new code's halves and were seen red by mutation instead —
`test_the_marker_exempts_a_line_a_never_closed_comment_held` under *a held
line ignores the marker*, `test_a_closed_comment_lets_go_of_the_lines_it_held`
under *a closed comment keeps what it held*. Both mutations survived the
first battery: the marker case's first fixture wrapped the marker in a
`<!-- -->` on the held line, which closes the comment and holds nothing, and
no existing case had a closed comment with a middle line. The two cases are
the repair, and the second battery killed both.

**Then green** (executed): the pull-request module's `fix_range` selection
13 passed; `tests/test_a_record_states_what_the_tree_has.py` 61 passed;
`tests/test_a_record_precedes_the_fixes_it_commissions.py` 51 passed (the
`fix_surface` arm's own cases, unchanged). A8 is inside the 61.

**Six mutations in the end, restored from kept bytes** (executed): M1 the
arm firing whatever the checker cell says — the `nobody` case and the
terminal `no fixes to check` case red; M2 the arm never firing — both
refusing cases red; M3 the arm never excused — the before-the-cutoff case
red; M4 an unclosed comment dropping its lines — A7 red; M5 and M6 as above.

**The four answers `CONTRIBUTING.md` §*What a change to a gate must carry*
asks for**, drafted here and carried to `overview.md` for the pull request
body:

- *Seen red:* the three cases above, quoted, at `65195f49`.
- *Failure direction:* both block more. #436 refuses a record whose `Fix
  range` still reads the template's pending words beside a `round-N`; the
  cheaper mistake is a deny that costs one `round-record close`, because the
  allow ships a record whose range claim is false about its own file. #217
  makes the records arm read lines an unclosed comment used to drop, so a
  name the tree lacks is now reported there; the allow was a way past the
  whole arm that cost one missing `-->`.
- *Prompt budget:* zero. Neither refusal asks a person anything; each lands
  at the pull request or at the generator's own `chain_check --worktree`
  with the repair named, and zero committed records are affected by either
  (Q3 above; the frame's 23-record count for #436).
- *Platform honesty:* nothing here rests on a platform guarantee. #436 reads
  two cells of one file; #217 reads lines of one file. Neither touches git,
  paths or a shell.

**Ledger:** A3 and A4 in the fragment. R5 (`claim_lines`), R6
(`fix_range`), S5 and 363 (the template's field table and the spec's
`### Review arm` region), and R7/R8 of `1789621028-…` (the spec's `Fix range`
subsection) each carry a dated re-read note; R7 of `1788472135-…`, which
anchors `says_not_yet` and `fix_surface`, did not drift — neither unit moved.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `claim_lines`' stated limit that an unclosed comment silences every line under it (the docstring's last paragraph and the `aside = True` with nothing symmetric to `held`) | the docstring's new paragraph, which states the narrower limit that remains: a fence inside a never-closed comment is not recognised |
