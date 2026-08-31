# Feature Specification: the last round's fixes are reviewed by nobody

<!-- specs/1788212517-the-last-rounds-fixes-are-reviewed-by-nobody/spec.md — WHAT
this work delivers and how we'll know. The policy documents in docs/ outrank
this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-chain-spec.md:116` — *"The last round's checkbox speaks for the whole review: earlier verdicts are not archived, every one of them needs an answer in the round that follows"* | The clause closes the FINDINGS and is silent about the ANSWERS. The last round's answers have no round after them, so the rule as written is satisfied by a chain whose final fixes nobody opened |
| `docs/review-chain-spec.md:34-38` — rounds capped at three, five while a 🔴 is open | Neither cap knows the difference between a round that found nothing and a round whose fixes nobody read, so the cap ends the run at exactly the moment the gap opens |
| `docs/review-handoff-protocol.md:113` — the `Pass` checkbox | `Pass` is a claim about the findings. Nothing in the record says who opened the fixes that closed them, so the gap exists only in a transcript |
| `skills/code-review/SKILL.md:127` — *"an axis marked clean in round 1 can be broken by the fixes made for round 2, and inheriting that verdict is exactly how it goes unseen"* | The skill already knows fixes break things. It applies that only to earlier rounds' fixes, never to the last round's |
| `CLAUDE.md` — no real identifiers in examples or fixtures | New prose and the new test use neutral values only |

## Scope

**In, and both options of issue #33 together.**

**B — the record says who checked the fixes.** `round-N.md` gains a
`| Fixes checked by |` row beside `Pass`. Its vocabulary is three values and
nothing else: `round-N`, `no fixes to check`, or `nobody — <why>`.
`chain_check.py` reads that row on the last record and refuses a claim git
contradicts — a missing row, a round that does not exist or is not later than
this one, and `no fixes to check` written beside a verdict that closed with a
fix.

**A — the last round verifies, not just finds.** The policy and the procedure
say that a review run ends with a **verifying round**: spawned after the
previous round's fixes are committed, targeted at the diff of those fixes, and
answering whether each closed finding is actually closed. A verifying round
that opens nothing needing a fix does not consume the round cap, because the
cap exists to stop a loop that is not converging and a round that finds
nothing is the loop having converged.

The two meet at one place. Only a round later than this one can be named as
its checker, so the last record in a run can only honestly read `no fixes to
check` — the verifying round's terminal state — or `nobody — <why>`, which is
the gap, written down.

**Out, and deliberately.** Option C of the issue: the chain runs until a round
returns nothing. It is unbounded in the bad case, and at the cap it stops with
the same gap. What is built instead is bounded twice over — the verifying
round's surface is a diff rather than a branch, and its terminal condition is
*this round's findings needed no fix*, which a round closing a 🟡 with grounds
satisfies. C would require *this round found nothing at all*.

**Also out, and it is a trade rather than an omission.** `chain_check.py` does
not fail a record whose `Pass` is checked beside `nobody — <why>`. That is Q1
in `questions.md` with the cost priced and the repository owner as its
answerer; §Data & interfaces below says what the check does instead.

**Also out.** The commit gate is not touched, the round cap's numbers do not
change, and no waiver mechanism is added or widened.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A record that claims a checker it does not have is refused | Given a last round record whose `Fixes checked by` names `round-4` · When no `round-4.md` is committed · Then `chain_check.py` exits 1 naming the round it could not find | Executed — `tests/test_the_last_rounds_fixes.py` |
| A record cannot name itself or an earlier round as its own checker | Given `round-2.md` whose `Fixes checked by` reads `round-2` or `round-1` · When the check runs · Then it exits 1 saying the fixes were opened by the session that wrote them | Executed — the same file, and this is issue #33's refusal |
| A record cannot say there was nothing to check while its own table says otherwise | Given `Fixes checked by: no fixes to check` beside a verdict cell reading `fixed` · When the check runs · Then it exits 1 | Executed |
| The gap, when it is real, is legible in git and printed on every run | Given `Fixes checked by: nobody — the run reached the cap` · When the check runs · Then it exits 0 and prints a line naming the record and the state | Executed |
| A record with no such row is refused | Given a last record carrying `Target SHA` and `Pass` and no `Fixes checked by` · When the check runs · Then it exits 1 | Executed |
| The one record in this repository that predates the field says so | Given `specs/1788184145-…/rounds/round-3.md`, whose four findings were fixed at `d3fe44d` and opened by nobody · When the field is added · Then it reads `nobody — …` and cites #33 | Read, and executed through the check at the release baseline |
| An orchestrator learns when to spawn the verifying round | Given a session running the chain · When it reads `skills/code-review/SKILL.md` and `agents/warden.md` · Then it finds when the round is spawned, that its target is the fix diff, and that a round finding nothing does not consume the cap | Read |
| The wording survives the suite's own prose rules | Given the new paragraphs · When `test_docs_line_wrap`, `test_one_word_one_meaning`, `test_the_set_a_work_item_always_has` and `test_handoff_outlives_the_merge` run · Then all pass | Executed |
| The wording cannot be deleted without a check going red | Given any of the five documents that carry the rule · When a rewrite drops the field, its vocabulary, the verifying round or the cap rule · Then `tests/test_the_last_rounds_fixes.py` fails | Executed — each case shown red under a mutation before being called passing |

## Data & interfaces

One new field in a markdown record, and one new set of failures in a check
that already runs in CI.

`| Fixes checked by | <value> |`, in `round-N.md`'s field table beside
`Target SHA`, `PR` and `Broad gate`. Read on **every** record, where `Pass` is
read on the last one alone. The two scopes differ because the two facts do:
`Pass` is a verdict on the whole review and the last round's speaks for it,
while this is a fact about one round's own fixes and every round has one.
Reading only the last record leaves `round-N` unreachable — a checker has to
be later, and the last record has none.

| The cell says | `chain_check.py` |
|---|---|
| the row is absent | **fails** — the author can always add it, which is the line the check has always drawn |
| `round-N`, N greater than this record's own number, and `rounds/round-N.md` is committed | passes |
| `round-N`, N at or below this record's own number | **fails** — the checker is this round or one before the fixes existed, which is the fixer certifying its own work |
| `round-N` naming a record git does not carry | **fails** — a claim git contradicts |
| `no fixes to check`, and no verdict cell in this record closed with a fix | passes |
| `no fixes to check` beside a verdict cell reading a fix word | **fails** — a contradiction inside one file, the shape this check already refuses for `Pass` beside an open 🔴 |
| `nobody — <why>` | passes, and prints the state on every run |
| `nobody` with nothing after it | **fails** — the reason is the whole of what makes the state readable |
| anything else, `the session that wrote them` included | **fails**, naming the three values. Read loosely a session's own name would pass as an answer, and that is exactly the state the field exists to refuse — the direction `CLOSED_WORDS` already takes for a verdict cell |

A draft pull request is excused nothing here. The `Pass` excuse exists because
a review still running has not reached its verdict; a record that names a
checker it does not have is wrong at any stage.

## Open questions → questions.md

Q1 — whether a checked `Pass` beside `nobody — <why>` should fail the pull
request outright. Q2 — whether the field should be read on every round record
rather than the last one.
