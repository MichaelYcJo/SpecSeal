# the seal names what it sealed and counts only the steps that run — questions for the planner

<!-- seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

**One row below needs a person, and it carries a default the build proceeds
on** — the owner pressed `automation` for the whole 0.17.0 run on 2026-10-01
(`routing.md`), so the default is built unless the owner reverses it when the
plan is read. Every other row is a measurement's or the work's. The ticket
left the following judgments open; the tree answered them, the grounds are
in `spec.md` (§Grounding, §*What was measured*) and `plan.md`'s Alternatives
table, and they are listed here so nobody reopens them as questions:

- **Which name goes beside the base commit.** The resolved ref (`Base.ref`,
  e.g. `origin/release/v0.16.0`), not the spelling the caller typed. #423's
  repair was that a reader must be able to tell the ref CI reads from a
  local one behind it; the ticket's example shows the given name, and the
  tree wins.
- **How many steps CI skips for a feature base.** Four, not the ticket's
  three: the milestone step also exits on `base_ref != main`
  (`hygiene.yml` line 347). So the honest rows are `4 of 9 not answered`
  on a feature seal and `8 of 11` on a release seal.
- **Whether the `Broad gate` cell changes.** No. `chain_check.broad_gate`
  takes the first SHA-shaped word; the names go on the lines and the stamp
  only (ticket §Keep, and the tree agrees).
- **What `#659` in the ticket's `item` example is.** The pull request of
  work item 1790635412 (its issue is #585, which the branch name on the
  `tree` row carries). Read from that item's `round-3.md` `| PR |` row, which
  `chain_check.PR_FIELD`/`PR_RE` already read; no network lookup.
- **What `capped` is read off.** The last record's `Needs a fix` beginning
  `yes` on a record `seal` accepted — the tree's own definition of the
  capped shape (`skills/verify/SKILL.md` §*The broad gate*). The deferred
  count and homes come from the verdict table through `chain_check`'s
  reader, never a second parser.
- **When the `gate` row prints.** Where a tree copy ran and its
  `broad_gate.py` differs byte for byte from the installed copy, whose path
  `main` hands the child in the environment on redirect. Version equality
  and redirect-happened were both rejected (`plan.md` Alternatives).
- **The width.** `PANEL_VALUE_WIDTH` is 23 and four of the ticket's values
  are 26–33 columns (measured). The panel is not widened; a value that
  does not fit continues on an unlabelled row under its label, and a branch
  or ref name is elided at the frame (head kept for the branch, tail kept
  for the ref, as the `from` row already does). Q1 below is the owner's
  door to reverse this.
- **What the `row` fold means at 23 columns.** `suite` keeps the counts and
  the row's `exit N` continues under it; `row` is gone. Dropping the exit as
  a constant was rejected because `chain exit 0` is as constant and the
  ticket keeps it.
- **`ledger` and `drifted`.** On a drawn panel both counts are 0 under
  `--strict`; the row is kept in the ticket's shape on a continuation line,
  and the count that varies is added where it varies, at the end of the
  `NOT SEALED` form's `ledger` entry.
- **Separators.** ASCII on the panel (` . ` as the `ledger` row already
  uses, `->`), because the letter twin exists for a console that is not
  UTF-8 and `errors="replace"` would print `?` for `·` and `→`.
- **The sample.** `SAMPLE_ROWS` mirrors the panel's labels, held by a case;
  it has read `lint clean` since #400 kept it *unchanged*, which the real
  panel's own comment calls a counterfeit.
- **Old values files and older hooks.** A values file without `branch` draws
  today's label; a hook older than the gate draws the new rows under its
  old label. Both are asserted, neither is repaired.
- **The commit-the-cell line.** Printed on a recorded seal only, on the same
  stream as `SEALED`, directly after it; never on `NOT SEALED` and never
  without `--record`.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | The panel keeps its 36-column frame and 23-column values, so a value that does not fit on one row continues on an unlabelled row beneath its label (`tree` / `base` names, `suite`'s exit, `ledger`'s drifted and broken, `rounds`' deferrals), and a branch or ref name is elided at the frame. The ticket drew each of these on one row, and that row does not fit: `551c7967 (origin/release/v0.16.0)` is 33 columns, `5081 passed, 10 skipped · exit 0` is 32, `2662 ok . 0 drifted . 0 broken` and `3 · capped · 2 deferred → #664` are 30. **Widen the panel instead?** The stamp is 81 columns at the 0.90 scale the owner chose over six renderings (#400); a panel wide enough for the longest of these (about 46 inner columns) makes it about 91 | **a person** — the repository owner. The stamp is the one artifact drawn for a person's eye, and the geometry was chosen by looking at it; nothing in the tree says what width the owner's terminal has or whether a taller panel beside the disc reads worse than a wider one. The tree could answer only that 23 is pinned and that 81 was seen | **Continuation rows (the default):** `PANEL_WIDTH` and `PANEL_VALUE_WIDTH` stay, the width case holds every value, the panel grows from 15 to about 21 rows against the disc's 20, and nothing is cut. **Widen the panel:** `PANEL_WIDTH` moves (and `test_the_panel_value_width_is_what_the_stamp_actually_gives` with it), the ticket's one-row values are used verbatim, the stamp is about 91 columns, and the owner looks at it once on the first real run — this is the only option under which the ticket's exact strings appear on the stamp. Either way the lines and the label carry the full names | Continuation rows, the panel unchanged in width | ✅ answered 2026-10-01 by the repository owner: the default — continuation rows, the panel unchanged in width |
| Q2 | Does `Needs a fix` beginning `yes` on the last record coincide with the capped runs in this tree — that is, over every `seal/specs/*/rounds/` whose last record has `Pass` checked, is the set with `Needs a fix \| yes …` the same set as the one whose verdict table holds a `deferred <home>`? Where they differ, which shape is the real capped run | **a measurement** — one script over `seal/specs/*/rounds/round-*.md` (`PASS_RE`, `field(rows, NEEDS)`, `verdict_table`), taken in phase 3 and recorded in `phases/phase-3.md`. No person's opinion is the instrument | **They coincide:** `capped` reads off the `Needs a fix` row and the deferred count off the table, as `spec.md` S4 says. **A record with `yes` and no deferral exists:** it is a capped run that fixed everything on the branch (`docs/review-chain-spec.md` §*The cap bounds rounds*); `capped` still prints and the continuation does not, which S4 already allows. **A record with deferrals and `no` exists:** a mid-run deferral by choice; the continuation prints and `capped` does not, which S4 also allows. Only a `yes` record `seal` accepted that is NOT a capped run would move the definition, and the tree's own documents say there is none | S4 as written | ✅ measured 2026-10-01 in phase 3 (`phases/phase-3.md`): of 36 last records with `Pass` checked, all 14 reading `yes` hold a deferral, and 10 reading `no` hold one too — the third option, which S4 allows. No `yes` record that is not a capped run; S4 stands |
| Q3 | Does the installed 0.16.0 `Stop` hook draw a values file the new gate writes — rows with `""` labels, two extra keys — unchanged, on the owner's screen, and under its old label | **a measurement**, on the first real seal of the 0.17.0 run, read by the owner the way #400's S17 was. Reading says yes (`read_values` requires only `[str, str]` pairs and a numeric `scale`; `label` ignores unknown keys) and A15 asserts it in the suite; what no case can see is the screen | **Drawn:** nothing. **Not drawn:** the `SEALED` line names `seal-stamp --from <path>`, which draws it by hand, and the cause is one the hook's docstring already lists or a new one to file | Drawn, carried as an `overview.md` `## Not verified` row with the owner as answerer | ⬜ |
| Q4 | The exact wording of the commit-the-cell line, the environment variable's name on the redirect, the clause the stderr coverage line adds for the steps left out, and the `rounds` continuation's spelling for several homes and for a `deferred (no home)` | **the work** — fixed by the cases that pin them (contract §14), within `spec.md` S2–S5's constraints: the line names the act and the reason and prints only on a recorded seal; the variable is documented beside `SESSION_VAR`; the clause says how many and why; the separators are ASCII | Constrained by `spec.md` §*Data & interfaces*; the phase that writes each records it in its `phases/phase-N.md` | As `spec.md` states | ⬜ |
| Q5 | Which existing cases read a panel row, the `SEALED` head, the label or `HISTORICAL_ROWS` and so go red when each surface changes. Found by `grep` at framing: the regions `spec.md` §*What was measured*, last row, lists — the sealer test's #475 and #400 blocks, the range test's A6/A7 and document pin, the partition test's A6 and A7, the stamp test's label pins, and the one prefix in `test_a_gate_that_fails_says_so.py` that must keep passing | **the work** — each phase meets its own and moves it, saying in `phases/phase-N.md` which pins moved and which were seen red first; a case the grep missed surfaces as a red run in that phase's slice and is handled there | Phase 1 and 2 move the listed ones; a vacuous assertion left behind (one that passes because the row it reads no longer exists) is a finding for the warden, so each moved case asserts the new row positively | As listed | ⬜ |

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
