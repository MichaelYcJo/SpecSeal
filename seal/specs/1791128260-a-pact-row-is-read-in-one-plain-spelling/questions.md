# a pact row is read in one plain spelling — questions for the planner

<!-- seal/specs/1791128260-a-pact-row-is-read-in-one-plain-spelling/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Decided from the tree, not open.** These were judgments the ticket, the
owner's choice or the spawn left open. Each is answered in `spec.md` or in
`plan.md`'s Alternatives table, with the grounds there.

- **The accepted spelling.** A row the walk takes whose item is byte-equal
  to `Pact` or `Pact notify`. The walk's own whitespace handling around the
  cell stays. The value's handling is unchanged (`spec.md` §*What is read*).
- **The refusal class.** Every other GFM line that names a pact
  (`PACT_WORD`, raw or decoded) and holds a `|`. On a walked row, only the
  item is read (`spec.md` §*What is refused*).
- **The spawn's example rule** (letters only, containing `pact`). Not taken.
  It refuses `impact`, misses `P&#97;ct`, and refuses walked values (`plan.md`
  Alternatives).
- **Fences and HTML comments.** Read through. An example there refuses,
  because exempting it depends on modelling GFM's block grammar.
- **`templates/config.md`.** No code reads it as a config, and it is not
  made silent as one. Its own first table is the plain spelling.
  *Corrected in round 1's fix pass of PR #793:* a session copies it whole,
  so its §*Pact* is written with no line that names a pact and holds a pipe,
  and the template reads silent (`spec.md` §*What this over-refuses*).
- **A stray notify line with no `Pact` value.** Refused, like a stray `Pact`
  line, because telling them apart needs the item read through markup. A
  plain notify row with no pact stays ignored.
- **The vendored copy.** The same constant and predicate. It is blind where
  a line naming a pact with a `|` is not a plain `Pact` or `Pact notify` row,
  or where both plain rows carry a value. Every base vendored case keeps its
  verdict.
- **`NOTIFY_ROW_SHAPE`.** Renamed `PACT_WORD`. The released anchor that
  cites it (0.18.1 C1) is re-pointed by a `Corrected ·` row.
- **Every other config row.** Out, on #784's spec's grounds, which this
  item inherits unchanged.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Is the stated blind side acceptable as a documented limit? Two kinds of spelling read as the default with no refusal. One puts a letter that is not part of the word between its letters: a tag name in `P<b></b>act`, a link destination in `[P](x)act`, an entity name nobody decodes. The other uses a look-alike letter from another script, such as `Pаct` with Cyrillic U+0430. No round of #784 found either. Each needs markup inside a four-letter word, or a deliberately different alphabet. **Why the tree cannot answer it:** the owner's choice says "prefer refusing loudly over modelling", and closing these needs either a markup grammar or a confusables table. Whether this residue is worth either is a value somebody has to be accountable for, not a fact in a file | a person — the repository owner | (a) **Accept and document**: `docs/the-pact.md` §*What this does not see* names both kinds. No code. (b) **Add crude strips as unions**: remove `<…>` and `(…)` runs before matching, which can only add refusals. That is two more transforms and a step back toward a grammar. (c) **Add a confusables fold** for Latin look-alikes: a table to keep | (a), built and documented. The build does not wait | ⬜ open; default (a) built: `docs/the-pact.md` §*What this does not see* names both kinds, and `test_the_blind_side_is_read_as_no_line` pins them silent, so a change of answer turns it red |
| Q2 | Does cmark-gfm, at the version the suite pins, ever give a line with no `\|` a second cell? The `\|` condition (`spec.md`) rests on GFM §4.10: a body line with no pipe is one cell, and the rest are inserted empty. **Why reading cannot settle it:** it is a claim about the renderer, and `tests/gfm_table_oracle.py` can answer it in one call | a measurement — render `Pact notify always`, `Pact notify: always` and `Pact notify` directly under a two-column table through `tests/gfm_table_oracle.py#rows_under`, and check that the value cell is empty | If any pipe-less line renders a non-empty second cell, drop the `\|` condition and accept that a prose mention refuses. Otherwise keep it | the condition stands | ✅ measured 2026-10-05 in phase 1: each of the three renders an empty value cell under the pinned cmark-gfm, so the condition stands (`phases/phase-1.md`) |
| Q3 | Which existing cases of the four pact modules, and of any other module that builds a `seal/config.md` naming a pact, change verdict under the new reader? A fixture may hold a line that names a pact with a `\|` and is not a plain walked row: prose, a doc table, or a commented example. **Why reading cannot settle it:** the fixtures are spread through the four modules' helpers and literals, and one run of the modules at the head with the new reader names them all | a measurement — the four pact modules plus the S11 modules, run once in phase 1 | A changed case where the fixture's line is a pact row in another spelling is the rule working. Rewrite its expectation and name it in `phases/phase-1.md`. A changed case where the line is incidental prose means the fixture is rewritten to keep its own subject, also named there | the rule stands; each changed case is named with its reason | ✅ measured 2026-10-05 in phase 1: no existing case changed verdict, and no fixture was rewritten (`phases/phase-1.md`) |
| Q4 | The refusal sentence's final wording. **Why it is not fixed here:** it must read after three callers' prefixes, which `spec.md` §*Data* names, and the builder meets them in the cases | the work — phase 1, pinned by S12 | Any text that names the line, says the one spelling and the table, opens lower-case and ends with no full stop | `spec.md` §*Data*'s text | ✅ decided 2026-10-05 in phase 1: the frame's text, kept; pinned after all three prefixes in phase 2 (`phases/phase-1.md`) |

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
