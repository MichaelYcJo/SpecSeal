# Feature Specification: a fence that closes after a later heading is refused

<!-- seal/specs/1788668335-a-fence-under-the-probes-table-closes-after-a-later-heading/spec.md -->

Closes #169.

## The claim, and the first thing this work item owes

#169 reports that `round_record.py#fenced_after` refuses a fenced block under
`## Executed probes` that **never** closes, and accepts one that **closes after
`## Deferred`**. The record then carries `## Deferred` and its row inside the
fence, its own Deferred section reads `nothing to drain`, and `chain_check`
exits 0 on a draft.

**That reproduction is stamped at `da047ab`**, the terminal target of #161's
chain in 0.8.1. `round_record.py` has moved since — 0.8.1 shipped, and 0.8.2's
own work touched the module. **So the first obligation is to reproduce the
shape at this branch's HEAD**, not to apply the fix the issue wrote.

Reading the function suggests the reproduction is worth checking rather than
assumed: `fenced_after` walks `section_body(reader, lines, heading)`, and if
that body stops at the next `##` heading then `## Deferred` never enters the
range and the fence reads as unclosed — which the existing refusal already
catches. Either the body reaches past the heading, or the reported shape no
longer reproduces. **If it does not reproduce, this work item says so with the
executed evidence and closes the issue on that grounds** rather than adding a
guard for a state nothing can reach.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/agent-contract/SKILL.md` §15 | a case is not planted until it has been seen red; here that doubles as the reproduction the spec asks for first |
| `skills/agent-contract/SKILL.md` §12 | the issue calls the late-closed shape *the one member of the class left open* — check that claim, and enumerate the class by decomposing where a fence can close rather than by listing shapes |
| `docs/review-chain-spec.md` §*The fix surface* | the record's own generator is what this changes, so a branch that changes the checker validates its own records in CI |

## Scope

**In.**

1. Reproduce the reported shape at HEAD, with the exact input and the exact
   observed exit — or establish that it does not reproduce.
2. If it reproduces: refuse it, naming the heading the fence swallowed, so the
   message tells the writer what to fix rather than that something is wrong.
3. The two cases #169 names — the late-closed fence, and the *nothing else of
   the section* clause, which the issue records as having no case at all and
   surviving a mutation that copies the whole probes section.
4. Whatever the answer, the class: **where can a fence close, relative to the
   section it opened in?** Enumerate by decomposition, not by listing.

**Out.**

- **Changing what a fence is copied for.** `templates/sdd-round.md` says a
  probes row whose subject was a proposed replacement owes the replacement in
  a fenced block, and `fenced_after` exists to carry it. Nothing here changes
  that contract.
- **Widening the refusal to prose.** A fence is copied whole and nothing else
  of the section is; the second case exists to pin that, not to relax it.
- **Retro-fixing records already written.** Any record carrying the shape was
  written before the refusal existed and is not this branch's to edit.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| The reported shape is settled by execution | Given a report whose fence opens under the probes table and closes after `## Deferred` · when `new` runs at HEAD · then either it is refused naming the swallowed heading, or the observed behaviour is recorded with its exit and the issue answered on that evidence | executed, both ways, in `tests/test_the_record_is_generated.py` |
| A well-formed fence still copies | Given the shapes the two existing planted cases cover · when `new` runs · then they stay green | the existing cases |
| A comment at column 0 inside a fence is not a heading | Given a Python comment inside a fenced block · when the section is copied · then nothing is refused | a case |
| The section's prose does not enter the record | Given prose under the probes table outside any fence · when the section is copied · then the prose stays in the report | the second case #169 names |

## Data & interfaces

One function, `skills/code-review/scripts/round_record.py#fenced_after`, and
its cases. No CLI change, no record-format change, no new field.

## Open questions → questions.md
