# a cd row's failing path is measured under its own directory (#761) — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Decided, not to be reopened here.** Each has its grounds in `spec.md`
§*Grounding* or `plan.md` §*Alternatives considered*:

- **Which of the issue's two fixes.** Absence is decided by a run at the base,
  invoked as the row invokes it — not the syntactic "a row that changes
  directory makes every unnamed file `new?`". Grounds: `agents/sealer.md` says
  `new` is earned by a re-run at the base; the syntactic test misses most of
  the class (`spec.md` §*The class, enumerated by construction*); #758 round 2
  judged the same choice sound for the neighbouring `cd` shape.
- **How the run decides it** — the orchestrator's answer to Q4, below: the
  root split nominates, a solo run per candidate confirms.
- **The kept file of a solo run.** `suite-at-base-<k>-<n>.txt`, so no run
  overwrites another; `NO_RUNNER`'s parenthesis names both forms, and its pin
  moves with it.
- **The un-nominated direction** (a `cd` row whose base carries a same-named
  file at the root but not below the `cd`) stays `new?`; `plan.md`
  Alternatives, G.
- **`--pyargs` rows.** A solo run still prints `no tests ran` and exits 4, so
  they need nothing of their own; `spec.md` §*Out*.

No row below is open for a person.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | What does pytest 9.1.1 print, and with what exit code, when one appended argument does not exist — plain, and under `pytest-xdist` 3.8.0 (`-n 2`), invoked from a directory below the scratch root? The tree cannot answer the xdist half: `xdist/dsession.py` `DSession.pytest_collection` returns `True`, so the missing argument is met in the workers, and how a worker's `UsageError` reaches the controller's output is not in any source a reading can settle. It matters here because this repository's own row ends in `bin/test -q`, which passes `-n auto` | a measurement — phase 1 | (a) both carry `file or directory not found: <arg>` on a line of its own: the reading matches that line, and S5's row asserts the drop. (b) xdist carries the text inside other output (a traceback, a `node down` line): the reading matches the text where it ends its line, wherever it sits. (c) xdist carries no such text: the not-found loop never fires for an xdist row, and Scope 3 does not apply; S5's row then asserts that the xdist output gives no file `new` or `failing on base too`, and if it would, the build stops at phase 2 and hands back the measured output, because the frame's premise (pytest's reply is readable) failed for the row this repository runs | Build for (a) or (b), whichever the measurement shows; (c) is a hand-back, not a silent build | ✅ (a) plain, (c) under xdist: plain pytest prints `ERROR: file or directory not found: <arg>` on a line of its own on stderr and exits 4; under `-n 2` and `-n auto` the run exits 5 with `no tests ran in <t>s`, no `not found` text in any output setting tried, and the present file's test unrun. The build stopped after phase 1 (`phases/phase-1.md`), and Q4 holds what follows |
| Q2 | Which released ledger rows does the change drift, beyond `seal/releases/0.18.1.md` B3 and `Corrected · S5`, whose claims it makes false? | a measurement — `evidence-check` after phase 2 | Each drifted row whose claim still holds gets a `Re-read ·` row through `evidence-check --reverify --into seal/ledger/1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory.md`; each whose claim no longer holds gets a `Corrected ·` row | B3 and `Corrected · S5` corrected (their sentences about the root split are false); every other drifted row re-read | ✅ as the default: 39 coordinates drifted across 10 released files, and 4 more once phase 3 added an exemption row. B3 and `Corrected · S5` (`seal/releases/0.18.1.md`) take `Corrected ·` rows, and the 16 other released families take `Re-read ·` rows written by `evidence-check --reverify --into` with `--checked 2026-10-04`, each claim read first; after it, 0 drifted and 0 broken (`phases/phase-3.md`) |
| Q3 | Where does the nothing-collected reading live, and is the solo loop a second loop or the existing one called per candidate? | the work — phase 2 | Any shape, on one constraint: every `run(...)` call stays written in `compare_at_base`'s own body, or `test_the_one_shell_site_is_run_and_it_applies_the_rewrite` goes red. A pure reader of `(text, exit code)` can be unit-tested for S5 without a repository | A pure module-level reader beside `PYTEST_SUMMARY_RE`, called from a loop in `compare_at_base` | ✅ the default, with one change: `collected_nothing(text, code)` sits beside `verdicts_at_base`, and the candidates are not a second loop. The shell-site case counts `run` calls rather than the functions holding them, so one loop runs every other file as one group and each candidate as a group of one (`phases/phase-2.md`) |
| Q4 | Q1 measured (c): under `pytest-xdist` a run with one missing path prints no not-found reply, exits 5 with `no tests ran`, and runs none of the other files either. Approach A then turns this repository's own row (`bin/test -q`, `-n auto`) from two measured words into two `new?` wherever a branch adds a failing test module beside a failure the base shares (`phases/phase-1.md`, the before/after table). Which way does the work go? | a person — the orchestrator, who decides whether the framer redraws `plan.md` | (i) Build A as approved and state the xdist loss in `templates/config.md` rule 3: never counterfeit, weaker on this repository's row. (ii) A, and where a run at the runner's prefix prints `no tests ran` with no reply, run each appended file alone at that prefix (alternative E restricted to that event); costs one run per failing file on such a row, and what a lone `no tests ran` proves about absence is unmeasured. (iii) A, with `-p no:xdist` appended at the base so the reply is printed; unmeasured for a wrapper that does not pass it through, and it changes how the row runs at the base. (iv) Keep the root split and add A's loop for what the split leaves: #761 stays open for a `cd` row under xdist. Each of (ii)–(iv) is new mechanism, which a re-frame owns and a build does not | Nothing is built: the branch carries phase 1's record and nothing else | ✅ Answered 2026-10-04 by the orchestrator, with a fifth option rather than (i)–(iv): keep the root split as a pre-filter that nominates candidates (failing files the base lacks at the root) and decides nothing; confirm each candidate with a solo run at the base — a summary gives the measured word, pytest's nothing-collected reply (`no tests ran`, exit 4 or 5) gives `new`, anything else `new?`; every other file goes through the existing comparison unchanged. Grounds: it keeps this repository's root-run xdist row measured where (i)–(iii) weaken or alter it, and closes #761 under xdist where (iv) leaves it open. The re-frame drew it in `spec.md` Scope 1–7 and `plan.md` Alternatives H, and dropped the split's branch-root condition so the `cd` file both roots lack is a candidate too |

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
