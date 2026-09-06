# 1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading — overview

<!-- seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/overview.md -->

📋 implement applied
· spec:     `spec.md`, `plan.md` §Alternatives, `questions.md`, `routing.md`,
            `phases/phase-1.md`; `skills/agent-contract/SKILL.md` §§2, 4, 5,
            9, 12, 14; `skills/implement/SKILL.md` §§1–4;
            `skills/writing-style/SKILL.md`; `docs/review-chain-spec.md`
            §*The fix surface* and §*What the record carries*;
            `templates/sdd-round.md` §Executed probes; `agents/warden.md`
            §Report; `CLAUDE.md` §*a change writes fragments*
· evidence: `seal/ledger/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading.md`
            F1–F5, eighteen coordinates; and `seal/ledger.md` R1 and R9
            re-read and re-stamped, because phase 1 moved `build`
· verified: **executed** — `tests/test_the_record_is_generated.py` (55
            passed), the eight modules that touch `round_record.py` plus
            `tests/test_a_rider_reaches_its_file.py` (302 passed), the
            (copy × hider) grid cell by cell before and after the fix, four
            mutations each turning exactly one case red, `ruff check` and
            `ruff format --check` on the two files this pass touched, and
            both `evidence-check` forms. **read** — `swallowed`, `build`,
            `fix_table`, `chain_check.py#SEPARATORS` and the seven constants,
            at `aed3ca0`. **unverified** — the full suite, the
            repository-wide lint and the typecheck, which are the
            orchestrator's (§2)

## Why this work exists

`round_record.py new` accepted a reviewer's report whose fenced block closed
below a later heading, wrote a record with that whole section missing, and
exited 0 — so a round could lose its own Deferred table and say
`nothing to drain`; the generator now refuses the report and names the
heading the fence swallowed.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Why the reported shape survives `fenced_after`'s never-closed refusal | `spec.md`: *"`fenced_after` walks `section_body(reader, lines, heading)`, and if that body stops at the next `##` heading then `## Deferred` never enters the range and the fence reads as unclosed — which the existing refusal already catches. Either the body reaches past the heading, or the reported shape no longer reproduces."* The code does neither: `readable` is `blank_fences(strip_comments(...))`, so a heading inside a fence is **blanked before `section_body` walks anything**, and the body does not stop there because there is no heading left to stop at | the measured reason | The spec located the question in `section_body`'s boundary behaviour, and the answer is one pass earlier, in what `readable` hands it. **The conclusion the spec drew from it was wrong as well**: it offered *"If it does not reproduce, this work item says so with the executed evidence and closes the issue on that grounds"* as a live branch, and the shape reproduces — executed at `c4d7077`, exit 0, the Deferred table inside the fence and the record's own Deferred section reading `nothing to drain`. A guard was owed, and `plan.md`'s third alternative is closed by that execution rather than by argument |
| How many members of the class are still open | `spec.md` §Grounding carries the ticket's claim forward — *"the issue calls the late-closed shape *the one member of the class left open* — check that claim"* — and the check returns **no**. Decomposing on one boolean over one span gives seven members, of which **two** lose a whole table with the generator exiting 0 (`## Deferred`, which #169 reported, and `## Executed probes`, which it did not) and three more are caught only by a message blaming the reviewer for a section they did write | the measurement, over the ticket | The ticket is a request and not an authority (`implement` §1), and `questions.md` A4 assumed exactly that before the first edit. The count is what decides where the guard lives: a fence taking `## Executed probes` leaves the report with no probes section, so `build` never calls `fenced_after` at all and the `SECTIONS` membership test #169 proposed **cannot reach the second silent member from inside that function**. `phases/phase-1.md` carries the seven-member table with each member's measured exit at `c4d7077` |

<!-- CORRECTED 2026-09-06 at `e7d3447`, round 1's ⬜ 6. The second row's
     *two*, and `phases/phase-1.md`'s *how the enumeration is known to be
     complete*, were both read as statements about the class. They are
     statements about one partition of it. -->

**What the second row's count is a count of.** Seven members and two silent
losers are exact for the partition that was taken: one closer state and one
span, measured against `REPORT_TABLES`' headings and `TERMINAL_LINES`, in the
one text `swallowed` reads, for the one input that text comes from. It was
then read as an enumeration of *how a report loses a section silently*, which
it is not, and round 1 found three places the same boolean had never been
applied — the second text `fenced_after` reads (🔴 1), the table rows under a
standing heading (🟡 2), and the round paragraph (🟡 3). Each of the three
lost a section with the generator writing the record. The qualifier is the
correction and the method is unchanged: the fix still keys on the span rather
than on the name, and it now keys on it in both texts, over the rows as well
as the headings, for both inputs.

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck — contract §2 keeps them out of a build phase | the orchestrator, once the review rounds settle |
| two ledger rows drift on the unscoped `evidence-check` read and neither is this branch's: `templates/config.md#"# Repository config"` in `seal/ledger.md`, and `docs/issues-and-milestones.md#"## A label answers *what it is about*, and survives the move"` in #155's fragment. Both target files and both rows are byte-identical to `774e76b` on this branch, so both drifts stand at the base commit; CI reports drift as a warning rather than a failure (`.github/workflows/test.yml`) | the orchestrator — the second one was not in the handoff, which named the first alone |

## Not done

**No sentence was added to `agents/warden.md` §Report or
`templates/sdd-round.md`, and that is a decision rather than an omission.**
`phases/phase-1.md` asked whether a reviewer needs to be told *close a fence
before the next section* somewhere they read before writing a report. Five
things settle it against:

- **The sentence would not be the rule.** *Close a fence before the next
  section* is stricter than the guard — a fence crossing a prose heading is
  accepted, measured at `c4d7077` and left that way by `spec.md` §Out — and
  looser than it, because `Needs a fix:` is a line a fence may not cross and
  is not a section. A reader who follows the sentence exactly can still be
  refused, and then the document does not explain the refusal.
- **The rule is derived, not authored.** `swallowed` reads `REPORT_TABLES`
  and `TERMINAL_LINES`, so what a fence may not cross changes the day a
  section is added. A sentence naming those lines is the second list
  `plan.md` rejected #169's `SECTIONS` tuple for, moved one file over — and
  there nothing can see it drift, where the parametrized case sees the
  constant drift today.
- **The reviewer is not the party who meets the refusal, and the sentence
  does not change that.** `round_record.py new` is run by the orchestrator
  (`docs/review-chain-spec.md`, `skills/implement/SKILL.md`'s round-record
  row), and contract §6 forbids the warden writing the record. The sentence
  would lower how often a report arrives with a late-closed fence; it would
  not move who repairs one.
- **The refusal already carries the fix at the moment of the act.**
  `SWALLOWED` names the swallowed heading and says *"Close the fence above
  that line, or move the block below the section"* — contract §14's shape,
  delivered to the party who can act on it.
- **#180 is open about rules that live in documents and get re-broken
  anyway.** A sentence would need a case under §14, and the case available
  is the shape `test_the_wardens_report_headers_are_the_generators_constants`
  already has: it reads §Report for a string. That pins the sentence's
  presence, never the rule, so it stays green while the sentence goes stale.

What that gives up, stated rather than left to be found: a reviewer who
writes a late-closed fence still costs one refused generation and one repair.
The measured frequency is one, over #161's fifteen-round chain, and what
changed is that the failure is now visible instead of silent — which is the
whole of what this work item was for.

**The prose-heading member of the class is left open**, which is phase 1's
judgment recorded here rather than dropped: no data is lost when a fence
crosses a heading the generator does not read, and closing it would refuse
the record-shaped blocks a reviewer of this very generator pastes — the tool
stopping inside its own review rounds. `spec.md` §Out already declines to
widen the refusal to prose, and the measurement agrees with it.

**One adjacent gap was found and not acted on.** The fenced-block convention
— *a probes row whose subject was a proposed replacement owes the replacement
itself* — reaches the reviewer only through `templates/sdd-round.md`, which
`skills/code-review/SKILL.md` points at for the **record's** shape, while
`agents/warden.md` §Report, which is where the reviewer is told what the
report must contain, does not mention a fenced block at all.
`docs/review-chain-spec.md` says the declaration is *"the reviewer's, made in
the report"*. That is one hop from where it is needed, it predates this
branch, and `spec.md` §Out puts what a fence is copied for outside this work
item — so it is named here for the orchestrator to file rather than fixed.

**A fence that takes SOME of a table's rows and leaves the rest is left
open**, and unlike the two above this one is a judgment made against a
finding rather than beside one. Round 1's 🟡 2 named it in its grounds — a
verdict row inside a fence under `## Verdicts` is dropped the same way the
whole Deferred table was. The whole-table shape is refused now; the partial
one is not, and it cannot be without giving up the limit the rest of the rule
is built on. Refusing a hidden row beside a table that still stands is
exactly F3's *mention* rather than *loss*: the fenced block a probes row owes
is often a record fragment, rows and all, sitting under a probes table that
stands — the shape
`test_a_fence_quoting_table_rows_is_kept_while_the_table_stands` pins. So the
rule cannot ask *is any row hidden here*; it asks *are the rows only hidden*,
and a partial loss is invisible to that question. Narrowing it to the two
sections whose fences are never copied would work and costs the thing
`plan.md` rejected #169's `SECTIONS` tuple for: a list of section names, in
the guard, going stale the day a section is added. What this gives up, stated
rather than left to be found: a reviewer who fences one verdict row loses
that finding from the record with nothing said. Nothing has produced that
shape yet — the two measured instances, #169's and round 1's, were both whole
sections or whole tables.

<!-- CORRECTED 2026-09-06 in round 2's fix pass, findings 7 and 8. Everything
     from here down said the second hider was enumerated and left open on
     purpose. Two things in that were wrong: the enumeration was one member
     short, and the member it missed was created by round 1's own fix; and the
     cost of what stays open was measured on a row where nothing follows it. -->

**The second hider is closed on both texts, and the enumeration that said it
could be left open was one member short.** Everything above this line is about
fences, and `readable` blanks with two passes: `strip_comments` runs first. An
HTML comment opened and never closed blanks every line below it exactly as an
open fence does — one pass earlier, where no fence question can see it.

Round 1 enumerated **what the boolean was applied to** and found four members:
the report as `swallowed` reads it, the second text `fenced_after` reads, the
table rows under a standing heading, and the round paragraph. Round 2 found
that list one short. The axis is two-dimensional — the text a hider is asked
about, and **which hider** — and the missing cell was created by round 1's own
fix: the round-paragraph guard asks `strip_comments(asked)` whether a fence is
still open, while `build` splices `asked` verbatim. That is 🔴 1's check/copy
asymmetry, inside the guard written to close 🟡 3.

**Re-run with both axes, and executed cell by cell at `aed3ca0`:**

| The copy | An open fence | An open HTML comment |
|---|---|---|
| the report as a whole | `NEVER_CLOSED` | **was** exit 2 on *the report has 0 `Needs a fix:` lines* — the writer sent to add a line they did write |
| the round paragraph, spliced whole | `ASKED_NEVER_CLOSED` | **was** exit 1 with the record WRITTEN and four of its five sections resolving to 0 occurrences — 🔴 7 |
| a fenced block, copied out of `raw` | `NEVER_CLOSED_VERBATIM` | unreachable: an opener inside the block whose closer stands outside it puts the block's own closing fence inside the comment, so the fence question answers first |
| a table row, copied out of `raw` | `SWALLOWED_TABLE` | the straddle — still open, below |

Both **was** cells are closed at `c7ebb29`: each text now asks both questions,
the comment's first. The order is load-bearing and has its own assertion in
each case — an open comment blanks the closing fence of every block below it,
so asked the other way round the refusal names a fence that is closed in the
text as written. Four mutations, each alone, turn exactly one case red:
deleting either comment question, and swapping either order.

**How the enumeration is known to be closed this time.** It is not a list of
shapes any more. The columns are the two passes `readable` is built from, and
the rows are the three copies the generator makes — `build` splices the round
paragraph whole, `table_of` copies a row out of `raw`, `fenced_after` copies a
block out of `raw` — which is every place a text the generator has read
reaches the record. A fourth copy would add a row, and a third hiding pass
would add a column; neither exists. Every cell above was executed rather than
argued, and the third row's *unreachable* is forced rather than sampled: for
the comment to be unbalanced across the block the closer has to stand outside
it, which puts the block's closing fence inside the comment.

**What stays open is the straddle, and its cost was understated.** A comment
can be whole in the report and half in the record, because both copies take a
SLICE of `raw`. Round 1's fix pass measured that on a **Deferred** row and
wrote *every section after it resolves to nothing* — and nothing follows the
Deferred section in a record, so the sentence was true of nothing. **Executed
2026-09-06 at `aed3ca0`, both rows:**

| Where the straddle is | What happens |
|---|---|
| a **Deferred** row | exit 0, the record written, every heading still resolving; the rows below the straddle silently absent |
| a **verdict** row | the record written, the run then fails, and `## Executed probes`, `## Inherited coordinates` and `## Deferred` each resolve to 0 occurrences — **three whole sections** |

The verdict row is the instance to weigh, and it is three sections rather than
a tail. It still has no guard, and the reason is unchanged: it needs a limit
argument the never-closed question does not, because a copied block may
legitimately carry a whole comment — so its question is balance across the
slice, not presence in it. That is a design call rather than a fix, and rule 2
of this pass refuses a fix pass the mechanism it would take. It stays at the
`# RIDER:` in `swallowed`, now carrying the verdict-row measurement, and not
in `seal/follow-up.md`: it is tied to a coordinate, and that file's own header
says a coordinate-tied row is a deferral filed where its reader is not.

**A pre-existing defect in `fix_table` was found by round 2 and deferred to a
rider.** `fix_table` cuts the sha out of the middle of its own code span and
leaves both backticks, because `chain.SEPARATORS` carries a space, two dashes,
a hyphen, a colon and a comma and no backtick — so a `fixed` cell lands in the
record as `fixed at e7d3447 — `` —`. Read 2026-09-06 at `aed3ca0`, and visible
in this work item's own `rounds/round-1.md`, rows 1 to 3. It predates this
branch. The repair belongs at the `note` line rather than in `chain.SEPARATORS`,
which is shared with the `deferred` home and with `chain_check`'s own readers.
The home is a `# RIDER:` at `fix_table` for the reason `seal/follow-up.md`'s
own header gives — it is tied to a coordinate, and this repository has a
tracker, so that file should hold none of it. An issue is the orchestrator's
to open if a schedule is wanted; contract §6 forbids this pass posting one.

## Fed back into the spec

None. The guard's rule and its enumeration live in `phases/phase-1.md` and in
the ledger fragment, and no clause of `spec.md` was rewritten — the two rows
above are where it was found wrong, which is what this section is for.
