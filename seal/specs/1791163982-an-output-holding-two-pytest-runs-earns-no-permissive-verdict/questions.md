# an output holding two pytest runs earns no permissive verdict (#789) — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row waits on a person.** The run is `automation`, and every judgment
the ticket left open was answerable from the tree or a probe. Listed so
nobody reopens them:

- **How "more than one runner" is decided.** By reports, not by lines.
  Pytest writes the report only for the arguments the gate handed it, and a
  collection-only pass reaches each later runner without running a test.
  This meets the comment's warning: an inner pytester run never writes the
  gate's report. Grounds: `spec.md` Axis B and `plan.md` Alternatives A
  and H.
- **"Every candidate" or every file.** Every file. p1b's permissive word
  comes from the group of non-candidates (round 1 of #761, probe p1b).
- **Whether `run` keeps stdout and stderr apart**, the code half the comment
  named. No. The report makes the base reading independent of both streams,
  and the split would not close the stdout shape the frame measured
  (`plan.md` Alternative B).
- **Whether the text readers stay as a fallback.** No. The fallback is where
  every permissive word of the class came from (`plan.md` Alternative I).
- **Whether a two-runner row is measured or reads `new?`.** It reads
  `new?`, as the issue asks. Measuring it is `plan.md` Alternative F, out.
- **Whether appending `--junitxml` to the row needs a switch or a config
  row.** No. The comparison already appends the files, and `CLAUDE.md`'s
  first goal argues against a knob. Rule 3 tells the row's author what is
  appended and what a runner that drops it costs.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does this repository's own row hand `--junitxml` to pytest, so its words stay measured? The row is `uvx ruff check . && uvx ruff format --check . && bin/test -q`. `bin/test` execs `.github/scripts/run_tests.py`, whose `main` reads its argv and runs pytest with it. That was read, not executed. The tree cannot answer it because whether pytest receives the option is a run's output, not a reading | a measurement — phase 1 runs `bin/test -q <one failing file> --junitxml=<scratch path>` and checks that the report names the file | (a) it does: nothing more to do. (b) it does not: every failing file of this repository's gate reads `new?` until `run_tests.py` passes the option on, so the fix belongs in phase 1, because a gate that measures nothing here is not shippable | (a), and the phase-1 record says which was measured | ✅ (a), measured 2026-10-05: `bin/test` handed `--junitxml` to pytest under `-n auto` and the report named the failing file (`phases/phase-1.md`) |
| Q2 | Does the reader place every test pytest's report names on the right appended file, in shapes the frame did not probe? Those are doctest modules and text files, `--import-mode=importlib`, a rootdir below the directory pytest runs in with nested packages, and pytest 7 and 8. The frame measured function, class, parametrised, collection-error and setup-error tests, and a rootdir above and below, on pytest 9.1.1. The tree cannot answer it, because each shape is a report somebody has to produce | a measurement — phase 1 builds S9's table from real reports | Each shape either places, or reads `UNPLACED` (`new?`), which is never permissive. Placing more is a gain, and failing to place costs a word only | the either-direction dotted-component match of `spec.md` Scope 3; any test it cannot place on exactly one file reads `UNPLACED` | ✅ measured 2026-10-05 on pytest 9.1.1, 8.3.5 and 7.4.4: every listed shape places; a doctest text file beside a same-stem module is ambiguous by construction and reads `UNPLACED` (`phases/phase-1.md`, the `REPORTS` table) |
| Q3 | Do later groups start their walk at the prefix the first group settled at, rather than at prefix 1? It saves re-running lint parts once per group on lint-first rows. It is unknowable at framing time whether it is free: it moves which `suite-at-base-<k>-<n>.txt` files exist, and existing kept-file assertions read them | the work — phase 1 | (a) Walk from 1 per group, as today. No kept file moves. (b) Start at *k*. Fewer runs, and assertions that name earlier prefixes' files change | (a), unless phase 1 finds (b) moves no existing assertion; the phase record says which | ✅ (a): (b) would make rule 3's pinned cost sentence false, an existing assertion (`phases/phase-1.md`) |
| Q4 | The words of the four reasons and the rule-3 sentences. `spec.md` Scope 7 fixes what each must say, not its wording. The tree cannot fix the words before the code exists to describe | the work — phases 1 and 2; the pins follow the shipped text | — | the builder's words, carrying Scope 7's content, each pinned whole in the commit that ships it | ✅ the four reasons and the rule-3 sentences as shipped at b069308d and 39b96a9d, each pinned in its commit (`phases/phase-1.md`, `phases/phase-2.md`) |

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
