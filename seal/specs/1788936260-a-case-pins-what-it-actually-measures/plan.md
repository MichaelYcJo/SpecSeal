# Implementation Plan: a case pins what it actually measures

## Summary

#310 first, because it is verified transcription and it is the smaller half.
Then the checker #262 asks for: enumerate a module's arms from its own syntax
tree, mutate each, run the suite, report the arms nothing kills.

## Technical context

**The enumeration is an AST walk and the rule is #262's own.** An arm is an
`ExceptHandler` — counting each member of an except tuple separately — or an
`If`, `While` or `IfExp`, counting each member of a boolean test separately.
Executed with that rule on `hooks/review-history-guard.py`: `reader` 5,
`is_closed` 4, `gh_segments` 5, `main` 17, total **31**.

**#262's table says 33 and the file has changed twice since.** That is not a
discrepancy to resolve — it is the ticket's argument arriving early. A number
counted by hand and written into a document rots; the checker's whole purpose
is that nobody types it again. Record both numbers and where the difference
came from; do not "fix" the ticket's table.

**The mutation is where the design is.** Killing an arm means changing its
sense — a test inverted, a guard removed, an except handler made unreachable —
and then asking whether any case notices. Two properties matter more than
elegance:

- **The module must be restored byte-for-byte after every arm**, verified by
  hash, never by `git checkout`. That is how four fix passes did it by hand
  today and the one that skipped the check found a mutation it had recorded as
  killed while never applying it.
- **An arm that cannot be constructed is not a gap.** `reader` has one such
  arm and it carries a sentence saying so. The checker reports what nothing
  kills; it does not claim each report is a defect.

**Failure scenario, in six months.** The checker's own enumeration goes short
— a new arm shape the walk does not know, a `match` statement, a comprehension
guard — and it reports nine unwatched arms out of thirty-one while the module
has thirty-four. That is the failure of the thing it replaces, one level up,
and the only defence is that the walk is derived from the grammar rather than
from a list: it must enumerate node **types** it does not recognise as a
refusal rather than skipping them silently.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A checker enumerating arms from the source, mutating each** | Its own walk goes short on an arm shape it does not know — answered by refusing unknown node types rather than skipping them | **Chosen.** #262 asks for exactly this and names `reader_blanking_passes` as the precedent |
| Nine cases for the nine unwatched arms | Closes today's list and not the class. #262 refuses it by name, and #210 is the measured instance of a written list rotting | Rejected |
| A coverage tool with branch coverage | Answers *was the line executed*, not *would a case notice if it were wrong*. Two of #262's nine arms are behaviour-preserving and coverage cannot tell them from gaps | Rejected — and worth stating, because it is the obvious substitute |
| Mutation testing over the whole tree (`mutmut`, `cosmic-ray`) | A dependency and a runtime measured in hours, for a repository whose suite is five minutes. #262 asks for one module's arms | Rejected for now; the checker's report is what would justify it later |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #310 — the four assertions replaced by the verified whole-clause version | the five mutation arms re-run here, all red; the case green as shipped | `be3e80c` |
| 2 | The arm enumeration: an AST walk with #262's counting rule, refusing node types it does not know | a fixture module whose arms are known by construction, plus the real module's 31 with the per-function split | |
| 3 | The mutation and the report: each arm mutated, the suite run, the unkilled arms named with function, arm and line; the module restored and hash-verified after each | a fixture with one watched and one unwatched arm | |
| 4 | The run over `hooks/review-history-guard.py`, its count recorded, and the fragments | executed, with the number in the changelog fragment and a ledger row | |

## Operational impact

A new checker that a person or CI runs; it changes no behaviour of the plugin
itself. Prompt budget **zero** — no hook, no question. Platform honesty: an
AST walk and file writes, no process inspection; the suite it invokes is
`bin/test`, which already runs on all three platforms in CI.
