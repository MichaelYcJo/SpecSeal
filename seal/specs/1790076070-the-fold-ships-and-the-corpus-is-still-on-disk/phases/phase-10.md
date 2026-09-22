# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — phase 10

| Field | Value |
|---|---|
| Phase | 10 |
| Commit | 873a75c8 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

**new** `docs/measuring-a-run.md` and **new** `docs/the-agent-set.md`.
Thirteen items: `session_cost.py` (7) and the ungrouped `1788449488` to the
first; `skills/agent-contract/SKILL.md`, `agents/smith.md`,
`skills/implement/orchestration.md` (2) and `1789081272` — moved here by
phase 8 — to the second.

## What this phase found

### Both files pass the test phase 8's did not

Asked the same way as phase 9: is there a document a reader with this
question would open?

- **Measuring a run.** `docs/review-handoff-protocol.md` holds the *bars* a
  segment is judged against, and that is where they belong — a bar is part of
  what a handoff carries. Nothing held the measurement itself: what a segment
  is, whose transcript it is read from, what happens to a reading that was
  already published. The new document says so in its opening and points at
  the protocol rather than restating the bars.
- **The agent set.** `skills/agent-contract/SKILL.md` is the contract, and a
  contract is instructions to a party rather than a policy a work item is
  judged against. Nothing said *why* the split between shared rules and one
  agent's own is where it is, or why the framer and the smith are two
  parties. Both are judgments a later work item could overturn, which is what
  makes them policy.

### `1789081272` landed where phase 8 sent it

Its segment is `hooks/implementer-notice.py` and its subject is the framer.
Folded into `the-agent-set.md` §*The writer of a contract is not its
executor*, beside the contract's own split — which is where a reader asking
*why are there two agents here* looks. Phase 8's record carries the move.

### The two documents share a boundary, and it is stated in one of them

`1788993115` established the payload meter, and its standing rule — a
section marked for one role reaches that role and no other — is also
`1788873630`'s, which phase 4 folded into `docs/review-handoff-protocol.md`.
Two work items, one rule, two documents.

They are not duplicates and the difference is the reason each is where it
is: phase 4's is about **which file a heading lives in**, which is a fact
about the payload's composition; this one is about **what that costs**,
measured. The agent-set document states the cost and the protocol states the
placement, and neither restates the other.

### What was dropped rather than folded

**`1788904490`'s decision not to re-derive published readings.** It says the
transcripts still exist and that what a corrected reading would say belongs
to two other tickets. That is a scope boundary between work items. What
folded is the half that still governs: a published reading stays wrong after
the code is fixed, so the correcting work item says which readings are
affected.

**`1788613827`'s `--json` parity clause** and **`1789296300`'s tolerance
window.** Both are implementation contracts of one command — true, and
checkable in the code rather than in a policy document.

**`1789100139`'s deletion list.** Which file was deleted and which cases
moved with it is the commit. The rule is the one the deletion demonstrated:
a document whose own last instruction is *delete this when the boxes are
ticked* keeps being read as current, and its standing rules move out first.

**`1788433011`'s per-agent inventory** — which invariant moved from which
definition into which. A list of moves; the rule is the test a shared rule
has to pass.

### The fold is complete, and it was checked by name

`./bin/settle` reports **0 work items in 0 segments** unfolded, with the
eleven kept items listed as ungrouped and 88 listed as folded and waiting to
be retired. Checked against the plan's own set in both directions rather
than by reading the count:

| Question | Answer |
|---|---|
| markers at the top level of `docs/` | 88 |
| marked, not in the 88-item retire set | none |
| in the retire set, unmarked | none |
| marked while in the eleven-item keep set | none |

That last row is the one that matters most: the keep-list is enforced by not
writing those ids as markers, never by editing the script (`spec.md` G2), so
it is a property of the prose and has to be checked against the prose.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| nothing from the tree — prose and markers only | none. Phase 11 removes the 88 directories these markers now cover |
