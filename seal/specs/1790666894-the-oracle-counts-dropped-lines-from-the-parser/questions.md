# the oracle counts a paragraph's dropped lines from the parser (#677) — questions for the planner

<!-- seal/specs/1790666894-the-oracle-counts-dropped-lines-from-the-parser/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row needs a person.** Q1 to Q3 are measurements, and the phase that
meets each one runs it. None of them blocks the build: each has a default
that the phase takes and records.

**Decided from the tree, so not reopened here.** Each is argued in `spec.md`
or in `plan.md`'s Alternatives table, where the next reader can overturn it by
opening what the frame opened.

- The count comes from the parser's `paragraph` and `lheading` rules and from
  no others. The other four places that push an `inline` token hold one line
  or are switched off (`spec.md` §*Why these two rules and no others*).
- Wrapping the two rules changes no interruption behaviour, because both
  already have an empty `alt` list and `Ruler.at` resets it to one.
- R1-1 is REMOVED, not narrowed. Its claim is the helper's marker reading,
  which goes with the helper (`spec.md` §*The ledger*).
- H's P1-1 is corrected in place and F's P1-2 is re-read, both where they
  live.
- The lines of H's records that name the helper take the
  ` · NAME NOT IN TREE` marker in phase 1's commit, as H did for F.
- `_inline_html_lines` loses its `lines` parameter.
- The class's rows go in a new case, and the 13 marker rows already in
  `test_the_oracle_names_each_kind_it_hides` stay where they are.
- The report left two of its five failing shapes as probes (four columns
  into a quote, and two indented `>`). They are planted too.
- The ticket's second box asks for each row to be seen red against the
  hand-written helper. The setext row is green there, which round 3 executed,
  so it is seen red with the `lheading` wrapper removed. §15 allows either
  (`spec.md` §*How each row is seen red*).
- The character set in S4 is computed from `str.isspace` and
  `str.splitlines`, not listed.
- No `docs/` change. No policy document describes the count.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does markdown-it-py 4.2.0 give CommonMark's answer on every row of S1 to S4? The expected answers in `spec.md` were read from the specification and not run. The frame has no code to run them against, and reading cannot settle what the parser does on nested and lazy shapes | a measurement — phase 1 for S1 and S2, phase 2 for S3 and S4, by running each row | Agrees: the row stands as written. Differs: the oracle follows its parser. The row pins the parser's answer by name with a comment naming the departure, as the `past the first closer` row does, and `overview.md` gets a divergence row. The walk is not changed toward the parser | Plant CommonMark's answer. Where the parser differs, pin the parser's answer and record the departure | ⬜ |
| Q2 | Which S3 rows are red with the oracle at `cd56113c`, beyond the five S1 shapes the report executed? The frame traced S3m through the old helper by reading and found it right, but did not trace every row | a measurement — phase 2, one run of the S3 rows against `git show cd56113c:tests/commonmark_oracle.py` | Any count is acceptable. It says how much of the class the old helper already had, and it is recorded, not required. §15 is met by the count-forced-to-0 run | Record the count and the ids in `phases/phase-2.md` | ⬜ |
| Q3 | Does S5 in `FOUND` keep `test_the_walk_is_exact_somewhere` above its floor, and which of H's record lines does the records arm name once the helper is gone? Grep finds 38 lines in six files, but the arm reads only backticked mentions outside a closed fence, so the set it names is smaller and only the arm knows it | a measurement — phase 1, one run of the property module and one of `bin/evidence-check` over the tree | Floor holds: S5 stays. Floor fails: S5 leaves `FOUND`, S1a pins the shape alone, and the phase record says so. For the records: mark exactly the lines the arm names, and no others | S5 stays unless the floor fails; mark only what the arm names | ✅ phase 1, `cbfe84f8`: the floor holds and S5 stays (`test_the_walk_is_exact_somewhere` green, module 95 passed); the arm named 26 refusals on 24 lines in five files, none in `round-1-report.md`, and those 24 lines alone carry the marker |

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
