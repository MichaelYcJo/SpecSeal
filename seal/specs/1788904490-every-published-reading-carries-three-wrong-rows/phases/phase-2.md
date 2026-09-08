# 1788904490-every-published-reading-carries-three-wrong-rows — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 0253001 |
| Ran by | the session on `claude-opus-5[1m]` — `routing.md` names `the session`, so there is no spawn and no segment transcript of its own |

## What this phase was asked

#202 — a streamed message is counted at its completed row.

## What this phase found

**The fix is one line of meaning and the fixture is the work.** Every case
written before this one passes under first-row-wins and under
largest-row-wins alike, because a single-row message cannot tell them apart.

**Last-row-wins and largest-row-wins agree everywhere they were measured** —
all 13,425 messages on this machine, 0 rows out of order — so the case that
separates them had to be constructed rather than found. It is here because the
claim otherwise rests on an ordering the transcript format does not promise.

**The second reader carries the same rule and it is not a defect there.**
`load` also keeps the first row of a split message, and the fields it reads
are fixed when the request is made: measured identical first-row and last-row
over the same 13,425 messages. What it also carried was a per-turn
`output_tokens` that **nothing in the module read** — the first partial count,
in a field with no consumer, which is how the defect in `token_totals` came to
be written in the first place. Removed rather than repaired.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `load`'s third per-turn tuple element (`output_tokens`) | Nowhere — it had no reader. `questions.md` Q4 holds the shape a future consumer should take, and the comment where the element was says the same |
