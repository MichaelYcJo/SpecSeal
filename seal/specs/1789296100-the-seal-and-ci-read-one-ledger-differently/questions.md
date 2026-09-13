# 1789296100-the-seal-and-ci-read-one-ledger-differently — questions for the planner

<!-- seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | How much of the broad gate's answer does the new line assert? The tree it prints on is one the gate would refuse, and the line can say that with or without the number | **a person** | (a) **name the grading** — *`broad-gate` runs this check with `--strict`, where drift is exit 2; this tree would come back `NOT SEALED`*. A reader acts on the number and the word without opening a second file, and the assertion is pinned by the case in phase 1 · (b) **name the form only** — *`broad-gate` runs this check with `--strict`*. Weaker, and self-maintaining: nothing in the line can become false if the grading changes · (c) name the form and the exit code but not `NOT SEALED`, which is `seal_stamp`'s word rather than the checker's | **(a)**, with phase 1's structural case holding the line and `broad_gate.py:570` together, so the assertion cannot go stale in silence | ✅ |
| Q2 | How many existing cases assert on `evidence_check.py`'s stdout in a way one appended line breaks? | **a measurement** | `bin/test tests/test_a_row_points_by_content.py tests/test_a_record_states_what_the_tree_has.py tests/test_a_narrowed_ledger_read_says_what_it_skipped.py -q` before phase 2 and again after. Reading found only substring assertions over the totals lines, which an appended line survives — but that is a read, not a run | run it at the top of phase 2; do not queue it behind Q1 | ✅ |
| Q3 | Does the `ledger` job's step in `.github/workflows/test.yml` need an edit of its own, or does the script's line reach the `::warning::` block with the step unchanged? | **the work** | The step reads `$?` and never the text, so reading says the step needs nothing but a comment that stops arguing leniency without naming the reader that disagrees. The phase that opens the workflow will see whether the log ordering makes the warning and the sentence read as one message or as two | the step is unchanged; only its comment is edited, in phase 3 | ✅ |

**`Who can answer` takes one of three values and nothing else.** A person, a
measurement, or the work. Only the first blocks the build.

Four things a reading already settled, recorded as assumptions rather than
asked, because a different answer would not change what gets built:

- **The broad gate stays strict.** `agents/sealer.md` §*The one run* and the
  issue both state it as a constraint.
- **CI's `ledger` job stays lenient.** Its own comment
  (`.github/workflows/test.yml:70-74`) argues it: a mid-flight branch drifts
  legitimately, and a check that is always red gets ignored.
- **`hooks/evidence-advisor.py` stays silent on drift.** Same reasoning from
  the other side, in its own docstring.
- **The line prints on exit 1 and nowhere else.** Exit 0 and exit 2 are states
  every reader grades alike, so there is no disagreement to report and a line
  printed on every run is one people learn to skip.

**Q1 answered 2026-09-13 by the owner: (a), name the grading.** The line reads
`broad-gate runs this check with --strict, where drift is exit 2; this tree
would come back NOT SEALED`. The owner took the option whose assertion is
widest, on the grounds the default already carried: phase 1's structural case
holds that sentence and `broad_gate.py:570` against each other, so the
assertion cannot go stale in silence. `NOT SEALED` is `seal_stamp`'s word and
the checker is borrowing it — phase 1's case is what keeps the loan honest.

**Q2 answered by measurement at the top of phase 2: zero.** The three modules
were run before the edit and again after — **182 passed** both times. Reading
had found only substring assertions over the totals lines; the run says the
same, and an appended line breaks none of them.

**Q3 answered by measurement in phase 3: the step needs no edit.** The `ledger`
job's own shell body was run verbatim over a drifted fixture. It exited 0, and
the log ends with the checker's sentence on one line and
`::warning::evidence ledger reports drift` on the next — the two read as one
message, in that order. Only the job's comment was edited, which is what the
default said.
