# <work item> — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     <policy/SDD files and clauses actually read>
· evidence: <seal/ledger/<work-item-id>.md rows added or updated>
· verified: <what was executed vs. what was only read>

## Scope confirmation

<Second-rung work only — it alters nothing observable and is more than one
line. The one line that replaces `plan.md`. Delete otherwise.>

## Why this work exists

<One line: why it was worth doing and what the result changes for whoever runs
it. Not a walk through the diff.>

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| | | | <quote, or "spec silent"> |

## Not verified

<!-- Read by `unverified-check`, so the shape is fixed: this table, or a single
line starting `none — <why>`. Leaving the placeholder row below fails the
check — fill it in or write the `none` line instead.

An item is closed by marking it, never by deleting the row:

    | ✅ <the item, kept> | <what closed it: the run, the session, the date> |

An unmarked row counts open. Deleting the row — or this whole file — fails the
next pull request, which is what keeps "I verified it" and "I tidied it away"
from being the same edit.

What the check compares is the NUMBER of rows, not their text, so the second
cell is read by people rather than by it: a closing that leaves the original
answerer in place still passes. -->

| Item | Who must answer |
|---|---|
| <what was not verified> | <who or what can answer it> |

## Not done

<Deliberate leavings — what was within reach and not taken, and on what
grounds. Prose, because these are decisions rather than pending claims. Or
"nothing".>

## Fed back into the spec

<Clauses this work added, marked as inferred-during-implementation — or "none".>
