# a ledger row that will not parse is counted — questions for the planner

<!-- seal/specs/1790297087-a-ledger-row-that-will-not-parse-is-counted/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

The owner pressed `automation` for the whole of `release: 0.15.4`, so nobody
answers this file before the build. Every row carries the default the build
proceeds on, and a person row's default is reversible after the fact.

## What the tickets left open and the tree answered

Listed so nobody reopens them. The grounds are in `spec.md` *Grounding* and in
`plan.md` *Alternatives considered*.

- **A verdict of its own, not `BROKEN`.** #299 and `seal/follow-up.md` said
  the naming needed a person. The documents settle it: `BROKEN` is reserved
  for the major unit (`docs/the-evidence-ledger.md`), and the other
  unparseable coordinate already has its own verdict because "the remedy
  differs" (`evidence_check.py#old_format_rows`).
- **Named `MALFORMED`, not `UNREADABLE`.** `UNREADABLE` is already a verdict
  of the records arm (`skills/evidence-check/SKILL.md` *Verdicts*).
- **Where the rule looks.** The `Code grounds` cell only. A scan of whole
  rows was measured: it refuses seven correct things in eight in this
  repository, one of them the template's own notation row.
- **A row whose grounds cell cites nothing is in the class.** The owner's
  second comment on #299: "any coordinate cell the anchor pattern rejects,
  whatever the reason".
- **`--reverify` names a `MALFORMED` row and does not heal it.** `SKILL.md`
  *Known limits* says every row the check refuses gets a line back from
  `--reverify`, and the suite pins `@00000000` as the placeholder workflow.
- **Whether any row is skipped right now** (#299, second *Not verified*
  row). Measured: five rows, in `seal/ledger.md` (three),
  `seal/releases/0.4.0.md` and `seal/releases/0.12.0.md`. The build repairs
  them in phase 1.
- **Where the row is dropped** (#299, first *Not verified* row). In the
  parse: a coordinate that matches neither pattern reaches no finding list.
- **The `seal/follow-up.md` row goes in this branch**, although #299's
  *Housekeeping* paragraph said otherwise. `skills/implement/SKILL.md` §1
  outranks the ticket, and the ticket's reason was two work items in flight
  on 2026-09-09.
- **#322 needs no code.** It was fixed in `97e29b7a`, and every tracked `.py`
  file compiles under `-W error` with no error (executed 2026-09-25).

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Should `MALFORMED` fail the build with or without `--strict`, in every repository that installs the plugin? | a person — the repository owner. The tree answers what the verdict is and gives a precedent for its grading (`OLD-FORMAT`, exit 2 under both readings). It cannot answer whether a **patch** release may start refusing rows in somebody else's build, which is what #585 calls a product decision. The milestone's own test ("every refusal added here enforces a rule a document already states") is met, which is why the default goes ahead | **(a) exit 2 under both readings**, like `OLD-FORMAT`: an installing repository with a malformed row goes red on update, and the output names the row and the remedy. **(b) grade like `DRIFTED`**: exit 1 with the lenient notice, 2 under `--strict`. The broad gate and the vendored CI template both pass `--strict`, so they still refuse; only a bare run softens. The change from (a) to (b) is one branch in `exit_code` and its case | (a) | ⬜ |
| Q2 | Should #322's class, an invalid escape sequence in a Python string, be guarded by lint from now on? | a person — the repository owner. It changes what the broad gate refuses, `CONTRIBUTING.md`'s *What a change to a gate must carry* asks for an argument for that, and the milestone says this release adds no gate | **(a) no guard.** #322 closes as fixed at `97e29b7a`, with the class measured at zero today, and a future instance becomes an import failure the Python release that makes it one will show. **(b) add ruff's `W605` to `ruff.toml`'s `select`**, with the argument that file's header asks each selection to carry, in a release that allows a new gate | (a), and the pull request says `Closes #322` with the grounds | ⬜ |
| Q3 | Does each of the five live rows' claim still hold once its coordinate parses? | the work — phase 1 re-reads each against its code | Holds: correct the coordinate, `--reverify`, `Corrected <date>` note. Does not hold: correct the claim or take the row out under `CLAUDE.md`'s rules, with any new claim in this work item's fragment | decided per row in phase 1, recorded in `phases/phase-1.md` | ✅ six of seven hold and were corrected in place with a `Corrected 2026-09-25` note; the rider-stamp row in `seal/ledger.md` does not (its quoted line is gone and a stamp names no commit since #239), so it is removed and the current claim is a row in this work item's fragment (`a77eed92`, `phases/phase-1.md`) |
| Q4 | Which unit carries the claim of `seal/releases/0.12.0.md`'s `claude_block.py#<module>@00000000` row? | the work — phase 1 reads `.github/scripts/claude_block.py` and the claim | Only the code knows. The same file's *Round 1's 🟡 4* row repaired the identical coordinate in its own row, and it shows one way to do it | whatever unit phase 1 finds | ✅ `TEMPLATE`, the constant naming `templates/claude-md-block.md`, and `write`, which regenerates `CLAUDE.md`'s region from it; `claude_block.py --check` exit 0 on 2026-09-25 (`a77eed92`) |
| Q5 | Does any existing test fixture write a row whose second cell holds no coordinate, in a module that runs the checker? Rule (b) would turn it `MALFORMED` | a measurement — phase 2's boundary run of the modules listed in `plan.md` | A fixture row meant as a claim gets a coordinate. One that is not meant as a claim was never a ledger row, and the case says why it is there | phase 2 runs the modules and settles each one | ⬜ |

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
