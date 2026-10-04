# one heredoc shape the reader matches exactly is data (#739, #763) — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Judgments the tickets left open that the tree answered (decided by the framer)

Each is settled from the tree, with the grounds where a reviewer can open them.
None of them needs a person. Overturning one means reopening the row of
`spec.md`'s disagreement table that it names.

- **Fresh code, nothing of #760's hooks carried.** The record fields come out of `_heredoc_split`'s pass and `heredoc_data` rests on a `shlex` line shape, and both are what the four passes broke (`spec.md` §*Carry or fresh*). Only #760's must-stop test lists and #739's body fixtures are carried, as fixtures.
- **The reducer is a module of its own**, `hooks/one_heredoc.py`, with no import from `cmdline`, `cmdline_base` or `tokens`. This is the owner's instruction that the decision not reuse the shared splitter, made checkable by an import list.
- **The opener is line 1, and LEAD is only a `cd`.** Anything else before the consumer needs a quote-aware reader to show the opener is at top level (`spec.md` disagreement row 1; `plan.md` alternatives D and G).
- **Nothing follows the delimiter on line 1.** A tail could hold a quote, a substitution or an operator that moves where the body starts (row 4). Follow-up commands go after the terminator, where they are lines of their own.
- **The consumer set is the four sink forms and `python3 -`.** `cat` to standard output alone was dropped: no recorded refusal uses it, and its value is in a pipe or a substitution, both excluded. `python` (unversioned) was dropped: nothing recorded uses it. A `gh … --body-file -` consumer was weighed and dropped (`plan.md` alternative F). `tee` stays because the owner named it and it costs two grammar alternatives.
- **R2f is made conservative by construction.** A sink allows nothing after it, and the LEAD is only a `cd`, so nothing on the command runs after the write. That answers #763's yellow 2 and the post-review yellow 3 without a list of runners.
- **A Python program's suffix is read the base's way.** A Python program on stdin is the class `docs/commit-review-gate-spec.md` already leaves unread (*What stays unread is a program whose operands are a script*). The owner approved this class as data in #760's Q2, at #760's `plan.md` approval line (`636ebdb5`).
- **Whole-text bans on CR, NUL and backslash-newline.** Each one is a byte where a reader and some shell were measured or can be shown to disagree (`spec.md` rows 2, 5 and 8). Body included, at the cost of `plan.md` alternative H.
- **`is_plain` and the consent reads keep the full command.** Reading `is_plain` over the full command can only keep the reading in. The consent reads are not this ticket.
- **`hooks/cmdline.py` is not edited.** Its other callers keep their outputs, and its boundary disagreements stay costless at the base, where every body is read.
- **Nested bodies, the commit-message substitution idiom included, keep today's reading.** A substitution's value goes wherever the enclosing command sends it. None of #739's refusals needs it.
- **The policy text goes in `docs/commit-review-gate-spec.md`, where the rule stands.** #744 (`aadf2efb`) lifted that file's freeze. #739's "frozen until #727" no longer holds.
- **The ladder rung.** It alters a gate's verdict, so a `spec.md` is required (`skills/implement/SKILL.md` §3).

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | May the corpus row "measured: a patch whose body loops over a commit string" leave `tests/test_no_shape_the_base_stops_reads_silent.py`'s must-stop corpus (and `tests/test_an_automation_run_meets_no_commit_prompt.py`'s four measured shapes) and be pinned silent? It is a LEAD `cd`, a Python program on stdin and a quoted delimiter, with no suffix, so it is exactly this shape. The tree cannot settle it alone, because two statements by the owner meet here: that module's constraint for `1790644505`, and #739 | a person — the repository owner | **Move it** (default): the shape is #739's, and the row is the one shape this work makes data. **Keep it**: the program consumer leaves the grammar, and refusal 1 stays refused | Moved. The owner answered this exact question in #760 (`questions.md` Q1 there), taking the default at #760's approval (`636ebdb5` on `fix/739-a-here-document-body-is-data-to-the-commit-gate`). The row and its grounds are unchanged by the redesign, so the answer carries | ⬜ decided-by-framer on the owner's #760 answer of 2026-10-04; the owner ticks it at this approval or overturns it |
| Q2 | Refusals 2 and 3 of #739, in the forms recorded, stay refused. Refusal 2 has an assignment LEAD, a parameter as the sink's target, and `gh` after the sink. Refusal 3 has a LEAD running a `$(…)` and a parameter as the program's argument. Each is covered when restated (`spec.md` §*#739's three refusals*). Is that cost accepted? | a person — the repository owner | **Accept** (default): the grammar stays one line-1 shape with no quote-aware reading, and the restated forms cost one extra call (refusal 2) or a moved path lookup (refusal 3). **Widen**: admit assignments, substitutions and parameters in LEAD and arguments, which needs a reader that proves line 1 is closed. That is the splitter problem again (`plan.md` D). Or admit programs after a sink, which reopens the runner list (`plan.md` E) | Accept | ⬜ decided-by-framer, open to the owner at approval |
| Q3 | Do bash 3.2, bash 5.x and zsh 5.9 cut every admitted string where the reader does, run directly and through `eval`? | a measurement — S6's agreement test; bash 5.x on CI's ubuntu leg, zsh where installed | If a shell disagrees on any admitted string, narrow the grammar until the string is rejected. Never special-case it | The shape as specified | ⬜ |
| Q4 | Does the moved row reach the shape on CI's Windows leg, where `shlex.quote` gives a single-quoted path with backslashes? | a measurement — the Windows leg of the test workflow, at the pull request | If not, narrow the moved-row test to say why. Do not widen `WORD` beyond one single-quoted word | Yes, through `WORD`'s single-quoted form | ⬜ |
| Q5 | Does `is_git_commit` still have a caller, and does the reduction sit in `main` alone or also in it? | the work — phase 2 | No caller: leave it, and say so in the phase record. A caller: apply the same reduction there | `grep` at `e141980a` finds no caller in `hooks/` or `tests/` (read, not run) | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
