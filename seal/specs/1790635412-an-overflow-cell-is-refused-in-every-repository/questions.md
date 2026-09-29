# an overflow cell is refused in every repository — questions for the planner

<!-- seal/specs/1790635412-an-overflow-cell-is-refused-in-every-repository/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

The owner pressed `automation` for all of milestone 49 and answered #585's
question, **(b) ship it**, in the batch before the first edit
(`routing.md` §*Why this way*). #585's own condition for (b), that #444's
work item finish editing the checker first, is met: work item
1790260566-a-row-inside-a-fence-reads-as-live folded in 0.15.3. No row below
needs a person, and none blocks the build.

## What the ticket left open and the tree answered

Listed so nobody reopens them. The grounds for each are in `spec.md` *Scope*
and `plan.md` *Alternatives considered*.

- **A verdict of its own, not `MALFORMED`.** Folding the two would make
  three shipped sentences false and give one word two meanings. The word is
  `OVERFLOW`, the issue's own term.
- **Graded like `DRIFTED` and `MALFORMED`: exit 1 lenient, exit 2 under
  `--strict`.** The owner's answer of 2026-09-26 for `MALFORMED` gave a
  reason that applies unchanged. A lenient run should not start refusing rows
  on update, and the readers that decide still refuse.
- **Only more cells are refused, not fewer.** The rule, the issue, the
  owner's answer and the old case's own name all say *more*. A short row
  hides nothing, and the old case's `!=` finds no short row in today's tree
  (Q2 has the instrument).
- **Fences are read by the shared rule**, through `unquoted` and
  `fence_rule`, which the checker already asks. No new fence reading is
  written, which keeps this clear of B (#584).
- **The width of a header-less row is a constant, `LEDGER_COLUMNS`, pinned to
  the template by a case.** It is not read at run time, because the vendored
  copy has no template beside it.
- **One table walk, `ledger_table_rows`, extracted from `grounds_cells`.** Both arms
  read through it, and it is what C (#387) can build on.
- **This repository's case becomes a caller of the shipped arm.** It is not
  removed, because CI's `ledger` job is lenient and the pytest case is what
  fails a contributor's pull request. The case's own implementation is
  removed, and a planted-tree case makes it red-able.
- **`--reverify` and the commit advisor both name the new verdict.** Each
  already promises, in its own documentation, to name every verdict of that
  kind.
- **The README row** is the `evidence-check . [--strict]` row of the command
  table, in both editions. `SKILL.md`'s verdict table gets its row as well.
- **Version and changelog.** The branch touches neither `plugin.json` nor
  `CHANGELOG.md`. It writes this directory's `changelog.md`, and the 0.16.0
  release preparation moves the version. The squash prefix is `feat:`.
- **1790260565's Q1 is ticked by this branch**, as 1790381328 ticked
  1790297087's.

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Which existing cases change their expectation when the totals lines gain `· N overflow`, the notice gains a word, and `SKILL.md`'s reader table states a second verdict's grading? **Why the tree cannot answer it at framing:** it was read by `grep` (the totals are matched as substrings, and one case asserts the reader table's last header cell is `MALFORMED is`), and the run of the four modules settles it in seconds, where framing runs nothing | a measurement: phase 1's boundary run of `tests/test_a_row_points_by_content.py`, `tests/test_evidence_check.py`, `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` and `tests/test_dispatch.py` | A case that pins a sentence or a column this work changes takes the new text, with the grounds in `phases/phase-1.md`. A case that goes red because a verdict or an exit code moved for a row this work did not mean to touch is a trade the spec did not state: stop and state it, or narrow the arm | Update the pinned sentences and columns, and record each in `phases/phase-1.md` | ✅ measured at phase 1's boundary run: only the lenient-notice module went red, seven cases, each a pinned sentence or verdict key this work changes; each took the new text (`phases/phase-1.md`) |
| Q2 | Does the shipped arm name any row in this repository's ledgers? **Why the tree cannot answer it at framing:** the arm does not exist yet. A throwaway instrument using the shared `split_row`, `unquoted` and the header rule read 36 ledger files at `11e3104c` and found 891 body rows, 67 under no header, and none wider or narrower than its width. That is my instrument's reading, not the arm's output | a measurement: `bin/evidence-check .` after phase 1 | **Names none:** done. **Names rows:** each is escaped in the file it stands in, as keeping an existing claim true, with a dated note | The build proceeds on "none" | ✅ measured after phase 1: `bin/evidence-check .` read 36 ledger files and every line ends `0 overflow` (`phases/phase-1.md`) |
| Q3 | Which ledger rows beyond C2 and L1 does this branch drift, and does any edit make a claim false? **Why the tree cannot answer it at framing:** `plan.md`'s list was found by `grep` over anchors, and `evidence-check` is the authority | the work: phase 4's unscoped run | Claim holds: re-read, re-stamp by the hazard rule, dated `Re-read` note. Claim false: `Corrected <date>` note first | Whatever phase 4's run names | ✅ phase 4's unscoped run named 36 drifted coordinates in 28 rows of 11 release files, plus one row in `0.13.1.md` that anchors a section those notes changed; two claims were made false (they quoted the notice's verdict list as two words) and were corrected first, the rest hold. Each carries a dated note (`phases/phase-4.md`) |
| Q4 | Does `survivor-check` report wording this branch removes (the policy paragraph's old last sentence, C2 and L1's text) as still standing somewhere? **Why the tree cannot answer it at framing:** the sweep's exclusions are the sweep's to apply, and the sweep is a run | the work: phase 4 | A correct statement standing where it is (a released `CHANGELOG.md` section, a shipped work item's record) gets a `survivors.md` row with its grounds. A statement still presenting the old enforcement as current is corrected | Exempt what is history, correct what is current | ✅ `survivor-check` reported nine places; none states the old enforcement as current, and each is exempted in `survivors.md` with a quote and its grounds |

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
