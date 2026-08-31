---
name: gap-analysis
description: |
  Compare a design or spec document against what was actually built — API
  surface, data model, business logic — and list what is missing, extra, or
  divergent.
  Use when: a written design exists and someone needs to know how far the
  implementation has drifted from it.
  NOT for: checking that ledger coordinates still resolve (`evidence-check`),
  judging ported behavior against an original (`legacy-parity`), or reviewing
  a diff (`code-review`).
---

# gap-analysis — how far the build drifted from the document

A design document and the code it produced diverge in three directions, and
only one of them is obvious. Missing is easy to see. Extra — built but never
specified — and divergent — built to a different rule than written — are
what this looks for.

## Comparison dimensions

Four kinds, whatever the project is. The examples name a web service because
that is the common case, not because it is the only one — substitute the
equivalent and the dimension still holds.

1. **The surface others touch** — whatever a caller reaches for, and what
   comes back. HTTP paths, methods and status codes; a CLI's flags, exit codes
   and stdout shape; a library's exported names and signatures; a screen's
   controls and states; a queue's topics and message shapes.

2. **The shape of what persists** — entities and relationships, field names,
   types and constraints, and how existing data gets to the new shape. Tables
   and migrations; a file format and its version field; cache keys and their
   expiry; what a client keeps on disk between launches.

3. **The rules that decide** — feature completeness, edge cases, error
   scenarios, validation. This dimension is the same everywhere and is usually
   where the real divergence hides, because it is the one a document describes
   in prose rather than in a table.

4. **Conventions** — naming, folder structure, import patterns, error message
   format. Drift here is rarely a defect on its own; it is the signal that the
   document stopped being read partway through.

If a dimension does not apply — a pure library persists nothing — say so and
move on. Recording it as a match claims a walk you did not make; leaving it out
silently makes a partial walk look complete.

## Verdicts

Per item, one of four. These are the useful part and they stay:

- **Match** — implemented as designed
- **Partial** — implemented differently; say how
- **Missing** — not implemented
- **Extra** — implemented, not in *this* document. That is not the same as
  unspecified: a repository accumulates specifications, and the second one
  routinely authorises what the first never mentioned. Say where else you
  looked before calling it unspecified

**Do not compute a match rate.** A percentage over hand-counted items reads as
measured and is not: the denominator is whatever you chose to enumerate, so two
walks of the same document return two numbers, and neither can be wrong. This
repository's `verify` skill calls a check that cannot fail a counterfeit seal;
a score that cannot be wrong is the same shape.

It also flattens the thing that matters. One missing authorization rule and
twenty naming drifts are not "21 items", and no ratio built from them says
which one to fix. **Severity comes from what the gap is**, never from how many
there are.

**Do not count them per dimension either.** Deleting the rate while printing
the numerator and denominator side by side leaves the reader to do the
division, and they do — "14 match, 2 partial, 3 extra" is a percentage a
sentence later. The table below reports coverage instead, which is the one
thing the counts were genuinely load-bearing for: a dimension nobody walked
must not read as a dimension with nothing in it.

## What was not compared

The half a gap report usually omits, and the half that decides whether the rest
can be trusted. Before the findings, say:

- which parts of the document you walked, and which you did not reach
- which dimensions do not apply to this project, and why
- anything you could not settle from the code — a question, not a pass

An unwalked dimension is not a match. Silence about it is indistinguishable
from having checked it and found nothing.

## Output format

```
## Gap analysis: <feature>

Compared: <document sections> against <code areas>
Not reached: <sections skipped, and why> — or "none"
Does not apply: <dimension: reason> — or "none"

| Dimension | Walked | What that covered |
|---|---|---|
| Surface | fully / partly / no / n-a | <what you actually compared> |
| Persisted | | |
| Rules | | |
| Conventions | | |

### Gaps
Ordered by what breaks if it ships, not by dimension.
1. <what is missing or divergent> — `path:line` · <what it costs>

### Extras
In the code, not in the document you walked. Check the sibling documents
before taking one to a human — one grep for the identifier across the other
specifications is usually the whole check, and it is cheaper than the answer
you would otherwise ask someone to repeat.
1. <what was added> — `path:line` · elsewhere: <where you looked, or "not checked">

### Open questions
Could not be settled from the code alone.
1. <question> — <who can answer>
```

Nothing here says "proceed". Whether a set of gaps blocks a release is a
judgment for the person reading the report, and a threshold in this file would
be that judgment made in advance by someone who has not seen the gaps.
