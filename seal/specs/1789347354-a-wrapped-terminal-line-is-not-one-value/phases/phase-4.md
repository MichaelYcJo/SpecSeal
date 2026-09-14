# 1789347354-a-wrapped-terminal-line-is-not-one-value — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | ac49d7f |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

`skills/agent-contract/SKILL.md` §12's other instance: bring
`skills/code-review/scripts/survivor_check.py#BLOCK` to the same pattern, or
write the grounds for leaving it into the module and into `overview.md`. A
case at the `#N` shape, red against `BLOCK` as it stands, and
`tests/test_a_corrected_sentence_survives_elsewhere.py` whole. This is Q4, and
if the module goes red the sibling is a different judgement and the phase
becomes an issue with the measurement attached.

## What this phase found

**Q4 is answered as the plan assumed, by measurement rather than by
assumption.** It is the same class: `BLOCK`'s bare `[-*+>#]` matches `#120` at
the head of a line, so a hand-wrapped sentence continuing onto an issue number
was split at a boundary that is not in the markdown. The module stays green —
49 cases, 47 before, exit 0.

**The consequence differs from the record generator's, and the module comment
now says so.** Nothing is truncated; the sentence is mis-scored, and a
survivor whose evidence straddles the wrap becomes unreachable because no
n-gram crosses the false split. That is the distinction `spec.md` §4 asked for
rather than treating the two as interchangeable.

**A second gap, and it is not this branch's to close.** Mutating the
pre-existing whole-line alternative `[-*_=]{3,}\s*$` to match nothing left the
whole module green — nothing in the suite pins it. It predates this work and
closing it means writing a case for code this branch did not change, so it is
handed over rather than taken: `overview.md` §*Not verified* and the pull
request body. The two alternatives this phase DID add are each pinned by their
own arm, and each kills only that arm when its lookahead is dropped.

**No fence openers were added.** The record generator needs ` ``` ` and `~~~`
because it reads a report; this module runs after `blank_struck` and a fence
line inside a segment is prose that scores nothing. `>` keeps no space
requirement, because the markdown needs none. Both are written at the
constant.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `BLOCK`'s bare `[-*+>#]` class | The narrowed constant that replaces it, whose comment names the other two carriers of the pattern and says why they are not shared through an import |
