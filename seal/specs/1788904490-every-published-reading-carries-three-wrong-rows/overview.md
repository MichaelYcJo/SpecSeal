# every published reading carries three wrong rows — overview

📋 implement applied
· spec:     `CLAUDE.md` (repo + user), `CONTRIBUTING.md` §What a change to a gate must carry, `docs/flow.md` §0.9.4, `seal/config.md`, `seal/ledger.md` §Coordinates, this item's `routing.md` · `spec.md` · `plan.md` · `questions.md`, `agent-contract` §§1–3 · 7 · 9 · 12 · 14 · 15, issues #200, #202 and #193
· evidence: `seal/ledger/1788904490-….md` — 5 rows (S1 · S2 for #200, S3 · S4 for #202, S5 for #193), 24 coordinates, `--strict` exit 0
· verified: **executed** — the three defects measured over the 180 transcripts on this machine before and after, every acceptance case seen red under a mutation of the thing it watches, 13 mutations with 0 survivors, the full suite. **Read, not executed** — nothing. **Not run** — the Linux and Windows legs (see *Not verified*)

## Why this work exists

`docs/flow.md` §0.9.4 puts three meter defects ahead of the two tickets that
read the meter's table. Two of them were found by taking this release line's
own per-segment readings, and **every per-segment reading this repository has
published carries all three**.

## Where spec and implementation diverged

| Divergence | Ticket says / code did | Chosen | Grounds |
|---|---|---|---|
| How #200 is closed | Three shapes, none decided: read the runner from `seal/config.md`, widen the pattern, or add a family for the project's own scripts | The widened pattern, **plus a fourth thing none of the three is**: the report names the slowest command it could not classify whenever `other` leads by time | The ticket's own objection to the cheap shape is *leaves the next repository with the same defect and no sign of it*. A sign is buildable and costs nothing per repository; the config row cannot help a repository on the day it installs, and it would put a `PreToolUse` parser inside a script whose argument is a transcript that need not belong to the repository the command runs in |
| The size of #200's second half | The ticket measures **one** file write charged to `test` | The classifier stops at the heredoc operator, which answers it for every family at once | Measured: **644** such calls over 180 transcripts, and `lint/type` and `build` carry the same kind — 361 → 175 and 177 → 47. A word list would have closed one word at a time on a body that can contain any word |
| #202's tie-break | *Keep the last row per id … or take the maximum, which does not assume the rows arrive in order* | The maximum | Measured: the two agree on all 13,425 messages with 0 rows out of order, so last-row-wins would have been green everywhere it was checked while resting on an ordering the format does not promise. The case that separates them was constructed |
| #202's *Not verified* row | Asks whether `load`'s own per-turn `output` takes the same first row | It does, **and nothing reads it** | `token_thirds` takes index 1 and `analyse` takes `len(turns)`; no other index appears in the module. Removed rather than repaired: a first partial count sitting in a field with no consumer is how the defect in `token_totals` came to be written |
| #193's second shape | *The filter drops a zero and keeps a negative* — written as one defect | Only the negative leaves | `count` answers 0 both for a field a harness never wrote and for one it wrote as 0, so the file cannot tell a turn that spent nothing from a turn nobody measured. Built as written, turns with no reading at all would have entered the mean |

## Not verified

| Item | Who must answer |
|---|---|
| The Linux and Windows legs. Everything here ran on macOS. Nothing added is platform-specific — a regex, a `max`, and a conjunct — but the path-invoked runner branch accepts `\` as a separator and no case on this machine exercises a Windows path end to end | CI |
| Whether the printed *`other` names nothing* line is acted on rather than read past. It is the whole argument for choosing the widened pattern over the config row, and it cannot be measured until a repository other than this one has run under it | the repository owner, at 0.9.5 or later |
| That a corrected reading changes what #51's bands say. The transcripts still exist and a re-run is cheap; what the corrected numbers mean is #145's and #149's question | #145, #149 |

## Not done

**The readings already published were not re-derived** (#200's closing
paragraph, `questions.md` Q1). They are marked instead — every reading before
0.9.4 carries all three defects — and the marking is posted to the open
flow-measurement log. Re-deriving them would answer #145's and #149's question
off one work item's convenience.

**`bin/evidence-check` still has no family** (`questions.md` Q3). It is 256
calls and the single slowest command in the segment #200 was found on. The
ticket's own third shape would put it in a `project` family, and the ticket's
own objection to that shape stands: a name that describes nothing is `other`
with a smaller cell. What changed is that the reader is now told it is there.

**No `seal/config.md` row was added** (`questions.md` Q2), and the condition
under which it becomes the right answer is written down rather than left as a
rejection.
