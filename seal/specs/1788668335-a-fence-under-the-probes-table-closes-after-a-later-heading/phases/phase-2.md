# 1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading — phase 2

<!-- seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 5083595 |
| Ran by | <left for the orchestrator — the spawn prompt named no model, and the template's own rule is that a segment transcribes this value or leaves it, never sources it from its own idea of what it is> |

## What this phase was asked

The closing set, and the last build phase. Write `overview.md` from
`templates/sdd-overview.md` with a real row under *Where spec and
implementation diverged* — `spec.md` said the reported shape would not
reproduce if `section_body` stopped at the next `##`, and the measured reason
is different — and a second row for `spec.md` §Scope item 4, whose answer is
that the late-closed shape is not the one member of the class left open.
`spec.md` itself is not to be edited. Write the ledger fragment at
`seal/ledger/<work-item-id>.md`, never appended to `seal/ledger.md`, with the
row phase 1 named and whatever else earns one — the scope rule itself and the
measured fact that `REPORT_TABLES` and `TERMINAL_LINES` had no reader are
candidates, and a claim not verified by opening the code gets none. Then run
**both** `evidence-check` forms and read the whole output, expecting this
branch's own edits to `round_record.py` to have drifted rows in
`seal/ledger.md`; re-read each before re-stamping, and take the hash from a
copy rather than letting a blanket `--reverify` re-stamp a row nobody read.
Write `changelog.md` in the shape of work item 1788661274's, carrying the
rule in one line plus the fact that the ticket's own diagnosis was one member
short. Tick #169's box in `docs/flow.md` and nothing else.

Then the judgment phase 1 handed over: does a reviewer need to be told *close
a fence before the next section* somewhere they read before writing a report
— `agents/warden.md` §Report or `templates/sdd-round.md` — rather than only
in a code comment and a refusal they meet after the fact. Judge it and say
which. Phase 1's own judgment that the prose-heading member is not worth a
follow-up is to be recorded in `overview.md` rather than silently dropped.

## What this phase found

**The judgment goes against adding the sentence, to either file.** The five
grounds are in `overview.md` §Not done and the two that decided it are these.
The sentence would not be the rule: *close a fence before the next section*
is stricter than `swallowed` — a fence crossing a prose heading is accepted —
and looser than it, because `Needs a fix:` is a line a fence may not cross
and is not a section, so a reader who follows the sentence exactly can still
be refused. And the rule is derived rather than authored: `swallowed` reads
`REPORT_TABLES` and `TERMINAL_LINES`, so a sentence naming those lines is the
second list `plan.md` rejected #169's `SECTIONS` tuple for, moved one file
over to where nothing can see it drift. Neither file was touched, so
`test_the_wardens_report_headers_are_the_generators_constants` had nothing
new to read; it ran anyway with its module, green.

**The handoff's ledger fact was one drift short, and the extra one is not
this branch's.** The prompt named one pre-existing drift on the unscoped read,
`templates/config.md#"# Repository config"`. The read returns two:
`docs/issues-and-milestones.md#"## A label answers *what it is about*, and
survives the move"` in work item 1788661274's fragment drifts as well. Both
that file and that fragment are byte-identical to `774e76b` on this branch,
which is the proof that the drift stands at the base rather than an inference
from it — nothing here could have caused it. `.github/workflows/test.yml`
reports drift as a `::warning::` rather than a failure, so neither blocks the
pull request. Both are named in `overview.md` §Not verified with the
orchestrator as answerer.

**The handoff's prediction about this branch's own drift was right, and it
was two rows rather than one.** `seal/ledger.md`'s R1 and R9 both cite
`round_record.py#build`, which phase 1 moved by three lines. Both were opened
at `5721a31` before anything was written: R1's claim is that every field row
is derived from something a person did not type, that `cell` refuses a value
it cannot write, and that nothing is committed — `swallowed` adds a refusal
and derives nothing, writes nothing and touches no cell. R9's claim is that
the round paragraph is copied from the `--asked` file into the section
between the field table and `## Verdicts` — `swallowed` sits above that read,
so a report that has lost a section is refused before the paragraph is looked
at, and the read itself is untouched. The hash was taken from the scoped
run's own report of the same anchor (`00000000 -> c4ef9d43`) and written into
both rows by hand, with a re-read sentence and the date; no blanket
`--reverify` was run.

**Four rows earned a place in the fragment, not one.** Phase 1 named the
derivation from the two constants (F1). Three more are judgments whose repair
looks obvious from outside and whose repair is the bug coming back: the rule
being read over the whole report so that `fenced_after`'s never-closed raise
is gone rather than kept (F2), the second half of the condition that makes
the guard refuse a report **losing** a section rather than a fence
**mentioning** one (F3), and the guard reading no `#` character at all, so a
Python comment at column 0 inside a fence is not a heading (F4). F1's tidy-up
and F4's look like the same simplification from outside and fail differently,
which is why they are separate rows rather than one.

**The adjacent gap is named and not acted on.** `agents/warden.md` §Report
tells the reviewer what the report must contain and does not mention a fenced
block at all; the convention reaches them only through
`templates/sdd-round.md`, which `skills/code-review/SKILL.md` points at for
the **record's** shape, while `docs/review-chain-spec.md` says the
declaration is *"the reviewer's, made in the report"*. It predates this
branch and `spec.md` §Out puts what a fence is copied for outside this work
item, so it is written into `overview.md` §Not done for the orchestrator to
file rather than fixed here.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — this phase adds three documents, ticks one checkbox and re-stamps two existing ledger rows in place; nothing left the tree | none |
