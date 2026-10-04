# a cd row's failing path is measured under its own directory (#761) — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Decided from the tree, not to be reopened here.** Each has its grounds in
`spec.md` §*Grounding* or `plan.md` §*Alternatives considered*:

- **Which of the issue's two fixes.** Absence is decided by the run at the
  base — pytest's own `file or directory not found` reply at the prefix that
  ran it — not the syntactic "a row that changes directory makes every
  unnamed file `new?`". Grounds: `agents/sealer.md` says `new` is earned by a
  re-run at the base; the syntactic test misses four of five members of the
  class (`spec.md` §*The class, enumerated by construction*); #758 round 2
  judged the same choice sound for the neighbouring `cd` shape.
- **Whether the extra run is worth it.** Yes: one run of the runner's prefix
  per failing file the base does not carry, only on a failing broad gate,
  stated in `templates/config.md` rule 3 where the row's author already reads
  the cost of their order (#634 kept lint-first knowing a cost of the same
  kind).
- **The kept file of a re-run.** `suite-at-base-<k>-<m>.txt`, so no run
  overwrites another and `NO_RUNNER`'s reason text stays true unedited.
- **`--pyargs` rows.** Left at `new?`; `spec.md` §*Out*.

No row below needs a person.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | What does pytest 9.1.1 print, and with what exit code, when one appended argument does not exist — plain, and under `pytest-xdist` 3.8.0 (`-n 2`), invoked from a directory below the scratch root? The tree cannot answer the xdist half: `xdist/dsession.py` `DSession.pytest_collection` returns `True`, so the missing argument is met in the workers, and how a worker's `UsageError` reaches the controller's output is not in any source a reading can settle. It matters here because this repository's own row ends in `bin/test -q`, which passes `-n auto` | a measurement — phase 1 | (a) both carry `file or directory not found: <arg>` on a line of its own: the reading matches that line, and S5's row asserts the drop. (b) xdist carries the text inside other output (a traceback, a `node down` line): the reading matches the text where it ends its line, wherever it sits. (c) xdist carries no such text: the not-found loop never fires for an xdist row, and Scope 3 does not apply; S5's row then asserts that the xdist output gives no file `new` or `failing on base too`, and if it would, the build stops at phase 2 and hands back the measured output, because the frame's premise (pytest's reply is readable) failed for the row this repository runs | Build for (a) or (b), whichever the measurement shows; (c) is a hand-back, not a silent build | ⬜ |
| Q2 | Which released ledger rows does the change drift, beyond `seal/releases/0.18.1.md` B3 and `Corrected · S5`, whose claims it makes false? | a measurement — `evidence-check` after phase 2 | Each drifted row whose claim still holds gets a `Re-read ·` row through `evidence-check --reverify --into seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md`; each whose claim no longer holds gets a `Corrected ·` row | B3 and `Corrected · S5` corrected (their sentences about the root split are false); every other drifted row re-read | ⬜ |
| Q3 | Does the not-found reading live in `verdicts_at_base`, in a new module-level helper, or inline? | the work — phase 2 | Any shape, on one constraint: every `run(...)` call stays written in `compare_at_base`'s own body, or `test_the_one_shell_site_is_run_and_it_applies_the_rewrite` goes red. A pure reader of the text (taking output and the appended files, returning the dropped file or none) can be unit-tested for S6 without a repository | A pure module-level reader beside `FAILED_RE`, called from the loop in `compare_at_base` | ⬜ |

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
