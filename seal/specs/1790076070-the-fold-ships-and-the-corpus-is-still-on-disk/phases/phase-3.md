# 1790076070-the-fold-ships-and-the-corpus-is-still-on-disk — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 21373d00 |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

`docs/review-chain-spec.md` — the record generator's 14 items, each sentence
carrying its marker. Verified by `./bin/settle` no longer listing those 14,
and by `tests/test_docs_line_wrap.py` and `tests/test_release_hygiene.py`.

## What this phase found

### The destination already carried the rules, so the fold is not a restatement

`docs/review-chain-spec.md` is 1,789 lines and already holds a section per
parsed field — `Fix range`, `Fixes checked by`, `New units`, `Ran by`, the
reopening, the depth, the written-late arm. Folding these 14 specs by
splicing their sentences in would have produced the failure
`skills/settle/SKILL.md` §2 names by name: "97 quoted fragments under their
provenance comments".

So the standing statement is about the thing the document did **not** have a
section for — the **writer**. The sections above say what each field means;
the new one says what `round_record.py` does about them. Four parts, and the
14 markers sit on the sentence each work item produced:

| Part | Items |
|---|---|
| A record is derived, not typed | `1788597030`, `1788844127`, `1789338080` |
| What it refuses before anything is written | `1788789985`, `1788817290`, `1789356180`, `1789296200` |
| What it copies, and what copying costs | `1788749195`, `1788873610`, `1788668335`, `1789347354` |
| What `close` derives | `1789621028`, `1789455558`, `1789425391` |

### What was dropped rather than folded

**Every `## Out` clause, and the two moratoria.** A scope exclusion is a
statement about one change's boundary, not a rule that governs anything
after it. Naming two of them, because they read like standing rules and are
not:

- `1788817290` out: *widening the literal-set comparison to a changed
  input-to-value mapping.* What survives is the **stated hole**, which is
  folded — a limit a document states is a rule a reader acts on; the
  decision not to close it that week is not.
- `1788597030`'s *moratorium for 0.8.x: no new parsed field* was already in
  the document and stays exactly where it is. It is scoped to a release
  series two minors back, and this fold neither extends nor removes it —
  removing it is somebody's decision, not a side effect of a cleanup.

**`1789425391`'s six ticket rows.** Five of the six were coordinate repairs
inside the generator, already true of the code. What still governs is the
one property they share, and that is what the folded sentence says: a
checker's own cases have to be able to fail. The five coordinates went
nowhere, and their argument is in the commits.

**`1789455558`'s `#406` and `#407` rows** — a duplicate pin removed and a
fixture taught to assert its own substitution. Both are the
`skills/implement/SKILL.md` rule about an edit that must be able to fail,
already stated there; a second copy in a behaviour spec would be the
duplication that work item was itself about.

### The destinations were right, and one was checked rather than assumed

`plan.md` sends `bin/round-record`'s item (`1789338080`) to this document
with the other thirteen, although its subject is a wrapper script rather
than the chain. Reading its `spec.md`: what it established is that **a
script a shipped document tells an agent to run is reachable by a command**,
and the documents it corrected are the chain's. It belongs here. No
destination moved in this phase.

### The marker is read where the plan said it is

Confirmed by running the reader rather than by reading it: after this phase
`unverified_check.folded_items('.')` returns exactly the 14 ids, and
`./bin/settle` reports **69 work items in 36 segments** where it reported 83
in 38. Two segments closed whole, which is what a segment-shaped phase is
supposed to do.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| nothing from the tree — this phase only adds prose to `docs/review-chain-spec.md` | none. The 14 directories are removed in phase 11, by `settle --retire`, and only because this phase's markers now cover them |
