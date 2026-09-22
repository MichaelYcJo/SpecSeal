# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — phase 9

| Field | Value |
|---|---|
| Phase | 9 |
| Commit | adea8052 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

**new** `docs/the-broad-gate.md` — the gate, its arm list, the runner, the
sealer, and the three checks that could not see what they were named for.
Eleven items: `broad_gate.py` (6), `arm_check.py`, `run_tests.py` (2),
`agents/sealer.md`, and the ungrouped `1789540097`.

## What this phase found

### This new document survives the test phase 8's did not

Phase 8 refused its new file because `docs/review-chain-spec.md` already had
a section per gate. The same question asked here gets the opposite answer,
and the difference is worth writing down so the next fold can apply it:

- `docs/review-chain-spec.md` **reads** the `Broad gate` cell and says what
  a bad value fails. It says nothing about who takes the run.
- `docs/release-checklist.md` names the gate as **a step** at one moment in
  the release, and its §3 is about a tree in a particular state.
- `agents/sealer.md` holds the procedure, and an agent definition is not a
  policy document — it is instructions to one party, which the SDD set
  outranks rather than the other way round.

So the area was genuinely uncovered: no document said the broad gate is one
act, who owns it, or what it is allowed to say. That is the test — not
whether the words appear somewhere, but whether a reader with the question
has a document to open.

### The document's first section is about a rule that failed twice

`1789002694`'s finding is worth the top of the file because it is the
strongest argument in the fold. The rule forbidding two agents the broad gate
was written in two definitions and assigned to a holder that was not an
agent, so **both readers reasoned past it** — a prohibition nobody could
perform. It pairs with `1789034970`, which settled the shared contract
against the agents that exist, and the two together say where a rule lives: a
rule no role needs an exception to is shared; a rule about one act is in the
definition of whoever takes it.

### Eleven items, four subjects

| Section | Items |
|---|---|
| One act, one owner, and the owner is an agent | `1789002694`, `1789034970` |
| What the gate runs, and how the list is kept true | `1789985781`, `1789956662`, `1789445605`, `1789721571` |
| What the runner owes the person who typed it | `1788632199`, `1788691941` |
| A check that cannot fail is not a check | `1788936260`, `1789540097`, `1789996775` |

`1789540097` is one of the five ungrouped items folded, and `spec.md`'s rule
sends it here — its three checks are the gate's arms. Reading its `spec.md`
confirms it: the three are a cell-presence loop, a closed set of search
phrases, and a sweep whose subject had drifted. All three are the same
shape, and the shape is the section's own rule.

### What was dropped rather than folded

**`1789002694`'s counted-stitch chart.** Most of that work item is a
29×32 chart, a disc computed from it, an ASCII twin and a colour-transition
emitter. It is a stamp's rendering — a thing, not a rule — and it lives in
the module that draws it. What folded is the one sentence about ownership
that the same work item established while assigning the act.

**`1789996775`'s five ticket rows.** `#461`'s docstring, `#464`'s two
statements, the panel's elision grounds and a spec row repeating retired
reasoning are five corrections at five coordinates. The rule is the one they
share: a statement your own fixes disproved is corrected by the run that
disproved it, because nobody later knows why.

**`1788691941`'s `Out` clauses** — the three refusals whose wording and exit
codes deliberately did not change. A boundary, not a rule.

**`1789445605`'s two lists** of sanctioned and refused command values. Which
commands are on which list is a fact about one repository's checks at one
moment; the criterion for choosing a value is the rule, and it has an owner
named in the folded sentence.

### The wrap list's comment was corrected, not just extended

Phase 5 wrote *the five policy documents the first fold wrote* into
`test_docs_line_wrap.COVERED`. Phase 8 made that four, so the comment said
something false about the list beside it. Corrected in this phase's commit —
this is exactly `1789996775`'s rule applied to this branch's own prose, one
phase after it was folded.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the word *five* from the `COVERED` comment phase 5 wrote | the comment itself, which now names no count |
| nothing from the tree otherwise | none |
