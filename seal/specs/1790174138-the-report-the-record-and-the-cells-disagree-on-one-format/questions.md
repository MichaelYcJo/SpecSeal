# the report, the record and the cells disagree on one format — questions for the planner

<!-- seal/specs/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Judgments the tickets left open that the tree answered

Listed so nobody reopens them. The grounds are in `spec.md` §Scope and
`plan.md` §Alternatives; each is overturnable there, not here.

- **Nine tickets → eight in, #159 deferred.** The ledger's `Corrected <date>`
  marker and `correction-check --range` (arrived after #159 was filed) answer
  the ticket's *not git history* objection: the pre-squash range on a pull
  request into a release branch is history the hygiene workflow already
  reads. Building the same for round records is a work item of its own.
  `plan.md` carries the sketch.
- **#174 → the cell is a list, newest first, and `seal` keeps what it
  replaces.** The milestone description names the one-entry cell as the
  defect; `chain_check.broad_gate` already reads the first SHA-shaped word as
  the run; a first seal is byte-identical to today.
- **#436 → under `RANGE_FROM`, no new cutoff.** Zero committed records at or
  after it hold the pending value beside a `round-N` (read: 23 records).
- **#505 → a section ends at a heading of its own level or shallower**, in
  `section_body` and, unless the phase records why not, in `swallowed`'s
  section-end scan.
- **#382 → resolve, do not refuse.** The refusal for an unresolvable revision
  already shipped; the cell gets the commit the revision resolves to.
- **#503 → example rows in the reviewer's skeleton, not a new rule.** The
  rule has been in `skills/code-review/SKILL.md` since 2026-09-08 and the
  reviewer holds that file; the control round in #503 was one example.
- **`✅` → documented as not a marker, not refused.** `finding_number` admits
  it as a no-id row; no committed record carries one.
- **A literal `<!--` in a report → the reviewer writes `&lt;!--`.** Code-span
  parsing is declined twice in the tree (`chain_check.says_none`'s docstring;
  the rider at `round_record.py#inherited_rows`).
- **#437's third requirement, no 🟡 anywhere in a carried row** → stated as
  the safe superset. Reading found `open_blocking` selecting on 🔴 only;
  no reader of a 🟡 outside the `#` cell was found. The standard says *the
  inherited severity in words*, which is right either way.
- **#218 → built on 0's reader, after the rebase**, never on cbb58091.
- **Build order** → phase 1 rebases; documents last (phase 5) so they
  describe the generator as landed.

## Residue

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | #159 is deferred to the release after 0.15.0 although the milestone lists it under step A. Does the owner want it pulled back in? The build does not wait on the answer: pulling it in adds a phase (a trailing `Corrected` comment under the field table, a range check in `hygiene.yml` on pull requests into `release/*`, the four gate-change answers) and removes none | a person | deferred — the sketch in `plan.md` §Alternatives goes to the next framer, and the orchestrator relays it to #159 · pulled in — a sixth phase after phase 4, built on the ledger's `correction_check.py` as the model | deferred | ⬜ |
| Q2 | Does `bound_line` still agree with `chain_check.stopping_floor` over every record sequence of length ≤ 3 (floor × `Needs a fix` × verdict) after 0's reader lands and #218's change is applied on top of it? #218 measured 584 sequences and one disagreeing class of 16; the frame could not run it because 0's code is not in this tree yet | a measurement | 0 disagreements — inheritance item 2 holds, record the count in `phases/phase-1.md` · disagreements remain — the phase names the class and fixes it before A9 is planted | 0 | ⬜ |
| Q3 | How many live records end inside an HTML comment, in `seal/specs/*/**/*.md` and on the branches open against `release/v0.15.0`? #217 walked three unshipped work items on 2026-09-12 and found none; the frame did not re-walk the 18 directories at cbb58091 | a measurement | 0 — #217's arm fires on nothing at the pull request, ship as framed · more than 0 — the record is malformed and the branch that owns it closes the comment; nothing in the arm changes | 0 | ⬜ |
| Q4 | The separator between `Broad gate` entries, and the exact words around the earlier entry. `spec.md` §Data & interfaces gives the three constraints the readers impose (no `\|`, no SHA-shaped word, no `<!--`, newest SHA first); which characters satisfy them best is visible only against the template's cell comment and the six documents once they are being written | the work | a `;` between bare entries · a `;` then `earlier run:` · one entry per line is NOT available, a table cell is one line | `; earlier run: <sha> against <base>` | ⬜ |
| Q5 | What 0's phase 1 named its reopening reader, and whether 0's phase 2 already moved `floor_and_fixes`'s count walk while making `bound_line` read through it. `spec.md` A9 and A11 are written against the function's role; the names are read off the tree after the rebase | the work | unchanged count walk — #218's paste-ready applies as written minus its `FLOOR_YES` line · moved — the phase re-derives `running` from 0's shape and says so in `phases/phase-1.md` | unchanged | ⬜ |
| Q6 | Whether `swallowed`'s section-end scan (the `next(... startswith("#") ...)` at the `REPORT_TABLES` loop) takes the same-level rule with `section_body`, or must keep ending at any heading because a hidden table under a `###` is what it exists to find | the work | same rule — one definition of a section in the module · keeps its own — `phases/phase-2.md` states the reason and A3's reviewer reads it | same rule | ⬜ |
| Q7 | Does `round_record.py new` at cbb58091 accept a `✅` in the `#` cell as a no-id row, as reading `finding_number` says (no digit, not in `OWED_MARKERS`, `idless` on)? `spec.md` documents `✅` as *admitted and not a marker*, and a sentence about what the generator does should be executed once before it is written | a measurement | accepted — the sentence stands · refused — the sentence changes to *refused*, and the refusal's message is the reviewer's instruction | accepted | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build. **Q1 is the one row of this kind, and it does not
  block**: its default continues the build unchanged, and the other answer
  adds work rather than changing any phase already listed.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Q2, Q3 and Q7.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer. Q4, Q5 and Q6.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
