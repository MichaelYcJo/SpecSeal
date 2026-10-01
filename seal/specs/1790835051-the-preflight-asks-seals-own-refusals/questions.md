# the preflight asks seal's own refusals — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Answered before the first edit

The routing batch of 2026-10-01 answered `automation` for #702 (`routing.md`
§*Why this way*). The ticket itself left no product question open: it says
the preflight asks `seal`'s refusals without writing, that `seal` stays the
authority, and that the full gate is unchanged, and the tree answers how.

## Judgments the tree answered

Each of these the ticket left open or did not state, and the tree settled.
The grounds are in `spec.md` §Scope or `plan.md` §*Alternatives considered*;
this list exists so a reader can tell a question that was decided from one
that was never met.

1. **How the refusals are asked without writing — a `--check` flag on
   `seal`, not an extracted predicate.** The same subprocess, the same `raise`
   sites in the same order, stopped before `kept_broad_gate`; the gate keeps
   its output and reads its exit code the way it does for a real seal
   (`plan.md`, alternative E says what the in-process predicate would cost).
   The flag's name follows `seal.py mode --check`, `fold_ledger.py --check`
   and `claude_block.py --check`.
2. **How the preflight learns the work item — from the checked-out branch's
   declaration, `routing.item_dir(root, branch)`.** The commit gate and the
   chain arm already key on that branch, the orchestrator types nothing new,
   and #638's `--preflight --record` refusal stands (alternatives A, B, C).
3. **The class is every refusal `seal` raises before the write**, not the
   two instances the ticket names: `seal_home`'s refusal for a chain
   declaration with no round record is included, and the two SHA refusals are
   asked as today even though the gate's own value cannot trip them
   (contract §12).
4. **No declaration for the branch is a line, not a failure.** A branch that
   reaches the preflight undeclared is one no sealer is coming for; refusing
   there would fire on every `no work item` run (`CONTRIBUTING.md` §*What a
   change to a gate must carry*, the outage clause). `spec.md` S8.
5. **The ask is not an arm and takes no `PARTITION` row.** It mirrors no CI
   step, and two AST readers of `gate()` would refuse it as one (S7,
   alternative F).
6. **The ask runs after the arms and does not stop them.** A chain refusal
   and a `seal` refusal are both named in one run, which is the *every check
   that failed* property #638 kept.
7. **A `seal` refusal is exit 1 in the preflight, not 2.** It is a finding
   about the record, like a chain refusal; the preflight's 2 means *nothing
   ran*, and here everything did. The ask's own exit 2 is quoted on its
   per-check line.
8. **The `PREFLIGHT` heads keep #638's shape; the tail changes.** 1790815615
   §*Not done* already records that #666's names do not reach the heads; the
   tail is the sentence that says what the run did, and what it did has
   changed.
9. **`agents/sealer.md`, `chain_check.py`, `docs/`, both READMEs, `hooks/`,
   `hygiene.yml` are out of scope**, each with its reason in `spec.md` §Scope.
10. **#638's changelog fragment gets one appended, dated sentence.** Both
    entries ship in 0.17.0 in id order; leaving the first saying the gap
    stands would put a false sentence in a release section (alternative H).
    Its `overview.md` and `phases/phase-2.md` are past-state records and are
    left as they stand.
11. **The drifted ledger rows are re-read in phase 4**, not re-anchored: a
    row whose anchored unit this work edits is read against the edit and
    re-stamped, its claim corrected in place where false (`CLAUDE.md` §*Repo
    rule — a change writes fragments*). Twenty-six rows across eleven files,
    counted at `e83db346`, are named in `plan.md` §*Technical context*.
12. **`seal/follow-up.md` holds nothing this work is the prerequisite for.**
    Read 2026-10-01; its rows concern the ledger, riders, the checker's
    silences and `CHANGELOG.md` §0.12.2, none of them the preflight or `seal`.

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | The exact wording of three new printed lines: `seal --check`'s success line, the preflight's stderr line naming the record asked (and its twin for none asked), and the amended `PREFLIGHT_TAIL`. `spec.md` §*Data & interfaces* fixes what each must say and what it must not (never `round-record: sealed`; the heads unchanged); the words are the phase's, pinned by the case that reads them (contract §14) | the work (phases 1 and 2) | (a) each line a constant beside `PREFLIGHT_TAIL` / in `round_record.py`, read by its case through the module · (b) literals in the cases. (a) is what #638's cases do (`NOT_RUN`, `PREFLIGHT_PASSED`) | (a) | ⬜ |
| Q2 | How S5's fixture reaches a `Target SHA` that descends from HEAD: a commit on a side branch from HEAD handed to `generate(repo, 2, …, target=<sha>)` with `feature` checked out again, or another shape the phase finds cheaper. The predicate itself is covered at the subcommand by S1, so the preflight case is about the plumbing (the gate hands `seal --check` the tree it stands on) | the work (phase 2) | (a) the side-branch target · (b) if `new` refuses a target off the branch for a reason the tree does not show today, S5 is recorded as covered by S1 alone in `phases/phase-2.md` and `overview.md` §*Not verified* names the orchestrator's next real run as its witness | (a) | ⬜ |
| Q3 | What the ask adds to a preflight's wall clock, on the sealer fixture and on this repository — one `round_record.py` subprocess. #638 measured the fixture at 1.57 s and this repository at 10.79 s (round 1) | a measurement (phase 2, written to `phases/phase-2.md` and `overview.md`) | the number, once, with the machine and the moment. No case asserts a time | measure and record | ⬜ |
| Q4 | Over 0.17.0's successors, how many sealer runs were refused at `round_record.py seal` after a suite. #638's Q3 counts record-arm failures; this counts the three refusals this work moves. The target is 0 | a measurement (the flow-log sweep that follows 0.17.0, by whoever runs it — the owner's sweep, per #51) | the count, read from the flow logs, posted where the sweep posts | nothing to assume; the ask ships either way | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build. **This work item has none**: the ticket, the routing
  batch and the tree answered everything a person would have been asked.
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
