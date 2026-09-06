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
            F1–F4, sixteen coordinates; and `seal/ledger.md` R1 and R9
            re-read and re-stamped, because phase 1 moved `build`
· verified: **executed** — `tests/test_the_record_is_generated.py` (49
            passed) and the nine modules named in `phases/phase-2.md`, both
            `evidence-check` forms. **read** — `swallowed`, `build`,
            `fenced_after`, the five constants and the six cases, at
            `5721a31`. **unverified** — the full suite, the repository-wide
            lint and the typecheck, which are the orchestrator's (§2)

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

**The second hider is enumerated, measured, and left as a message defect.**
Everything above is about fences, and `readable` blanks with two passes:
`strip_comments` runs first. An HTML comment opened and never closed blanks
the rest of the report the same way an open fence does, and `swallowed`
cannot see it for the same reason it could not see a comment-hidden fence —
it reads the text the comments have already been stripped from. **Executed
2026-09-06 at `c7663e1`**, calling `swallowed` and `terminal_value` directly
on two crafted reports:

| The `<!--` opens | What happens |
|---|---|
| above `## Deferred` | `swallowed` does not raise; `## Deferred` resolves to no section AND both terminal lines are gone, so `terminal_value` refuses with *the report has 0 `Needs a fix:` lines* |
| below the terminal lines | `swallowed` does not raise; nothing the generator reads is hidden, and the record is correct |

So it is **not** a silent loss, and the enumeration this branch corrected
does not grow by one. An unterminated comment runs to the end of the file, so
it always takes the terminal lines with it unless it opens below them — and
the terminal lines are last in the shape `agents/warden.md` §Report asks for.
What is left is the message: the writer is sent to add a line they did in
fact write, which is the exact defect §14 and this branch's own
`test_a_fence_that_swallows_a_terminal_line_names_the_fence` fixed for
fences. It is one refusal in the same place and shape as `NEVER_CLOSED`, and
it is not this fix pass's — round 1 did not find it, a fix pass answers the
findings it was given, and an unfound guard puts surface in front of the
verifying round that nobody asked for. It went to a `# RIDER:` at the line it
is about, in `swallowed`, and not to `seal/follow-up.md`: it is tied to a
coordinate, and that file's own header says a coordinate-tied row is a
deferral filed where its reader is not.

## Fed back into the spec

None. The guard's rule and its enumeration live in `phases/phase-1.md` and in
the ledger fragment, and no clause of `spec.md` was rewritten — the two rows
above are where it was found wrong, which is what this section is for.
