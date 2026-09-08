# 1788873630-the-orchestrator-sections-leave-the-reviewers-payload — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | c5cf5d2 |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Make every live reference name the file its heading is now in. The task said
to treat the ticket's enumeration as something to verify by construction over
the tree rather than a list to trust, and named `docs/flow.md`'s reference as
this work item's own business.

## What this phase found

**The ticket's *no reference crosses the seam* is literally true and
substantively wrong, and the reason is the shape of the grep.** It searched
for the string `Orchestrator:`, which matches the five `##` headings and none
of the seven `###` subsections inside them. Re-taken by construction — every
heading in the block, `##` and `###`, against every tracked file with
whitespace collapsed so a wrapped reference still matches — eight of the
twelve headings are named outside the file:

| Heading | Live references outside the skill |
|---|---|
| `### A fix pass adds the unit that pins it, and that unit ships unreviewed` | `agents/smith.md`, `skills/implement/SKILL.md` |
| `### And commit the record before commissioning the fixes` | `tests/test_a_record_precedes_the_fixes_it_commissions.py`, `tests/test_the_rules_have_one_owner.py` |
| `### Then say who checked them, in the record` · `### And name the fix surface, in the same record` · `### And say what ran the round` | `tests/test_the_rules_have_one_owner.py` |
| `## Orchestrator: the pull request opens before round 1, and a phase is re-run` | `docs/flow.md`, `docs/review-handoff-protocol.md` (twice) |
| `## Orchestrator: a fix pass resumes the implementer` · `## Orchestrator: the run ends with a verifying round` | `seal/ledger.md` |

The ticket's own sentence names `agents/smith.md` as carrying no
`Orchestrator:` reference at all. It carries a reference to a subsection of
one, which is the reference that matters.

**A second class the heading grep cannot see: a bare path.** A reference can
name the file with no heading at all and still point at moved material, so
every one of the fifteen live files naming `skills/code-review/SKILL.md` was
read in context. One qualified — `chain_check.py`'s `stopping_floor`
docstring cites the file for a sentence that moved. Four others cite it for
`§Findings format`, which stayed, and needed nothing.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| Nothing. Five references change the file they name; no text leaves the tree | none |
