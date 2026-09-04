# Feature Specification: the run outlives its last finding

<!-- seal/specs/1788472135-the-run-outlives-its-last-finding/spec.md — WHAT this work
delivers and how we'll know. The policy documents in docs/ outrank this file;
cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-chain-spec.md` §*The review run has a bound, and an end* | The bound is stated as a ceiling — three rounds, five while a 🔴 is open — and nothing says when to stop below it. A ceiling with no floor is spent like a budget: #81 ran seven rounds, and rounds 5 through 7 found nothing that loses a record and nothing that crashes |
| `skills/code-review/SKILL.md` §*Orchestrator: the run ends with a verifying round* | The floor has to leave this round standing. A run still ends by reading its own last fixes, so the floor stops the finding rounds and not the one that verifies them |
| `agents/smith.md` §*Implementation done ≠ chain done* | A fix pass is where a new unit enters, and the smith is the file that says what a fix pass may do |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | `chain_check.py` is a gate at the pull request. A test seen red, a stated failure direction, and a prompt budget are what this change owes |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Decides the one question this work item was asked: whether the two new record rows are read by a check or left for a person to read. A row no check reads is only true while somebody is awake |

## Scope

**In.**

- The stopping floor of #110, stated in the two documents that own the cap
  (`docs/review-chain-spec.md`, `skills/code-review/SKILL.md`) and recorded in
  a row of `templates/sdd-round.md`.
- The reviewer's own answer to the floor, in `agents/warden.md`. The row's
  honest value is the finder's, the same way `Needs a fix` is — an
  orchestrator inferring it from a verdict table is the failure that row
  already records.
- The depth bound of #117 — *a fix pass may add a unit; that unit's fix may
  not* — in `skills/code-review/SKILL.md` and `agents/smith.md`, with
  `templates/sdd-round.md`'s existing `New units` row carrying the depth
  rather than only the names.
- Where a refused unit goes instead: a deferral with a named answerer, or an
  issue. This lands **before** the check that refuses, so the chain is never
  stopped at a rule with no exit.
- The refusals in `skills/code-review/scripts/chain_check.py`, grandfathered
  by work-item id the way `STRICT_FROM` and `SURFACE_FROM` already are.
- Tests, a changelog fragment, and a ledger fragment.

**Out.**

- The other three levers of #97 — what is worth pinning at all, whether a pin
  must derive from one source, and whether a pin may be deferred. Each changes
  pins that already exist and needs its own question batch.
- The cap's numbers. Three and five are unchanged; this adds the floor they
  never had.
- A round budget per work item. #110 rejects it by name: the number of rounds
  worth running is a property of what the rounds find, and fixing it in advance
  decides before the evidence exists.
- Triage of what the flow log finds. #109 is explicit that automating the
  judgment is the wrong next step.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A quiet round ends the run | Given round 4 opened nothing that loses a record and nothing that crashes · When its record says so · Then the run stops, and what it did find is deferred with a named answerer or becomes an issue | `docs/review-chain-spec.md` and `skills/code-review/SKILL.md` carry the sentence; a test pins it in both |
| The reviewer answers it, not the orchestrator | Given a warden segment ends · When it writes its report · Then the report carries the floor answer as a line of its own, and the orchestrator copies it into the row | `agents/warden.md` carries the line; a test pins its spelling against the template's row |
| The verifying round still runs | Given round 4 met the floor and its fixes are committed · When round 5 reads the diff of those fixes · Then that is allowed, and a sixth round is not | `chain_check.py` refuses a record that met the floor and is followed by more than one later round record; a test seen red first |
| A fix pass may add a unit | Given round 2's fixes answer a finding in code that predates the run · When they add a helper · Then the record names it at depth 1 and passes | `chain_check.py` accepts `unit (depth 1)`; a test |
| That unit's fix may not add another | Given round 3's finding is inside a unit round 2's fixes created · When round 3's fixes would add a unit to fix it · Then the record cannot say so and the check names the two places it may go instead | `chain_check.py` fails on depth 2 or above, and the failure names the deferral and the issue; a test seen red first |
| Old records are not made red | Given a work item begun before this rule · When its records carry no depth · Then the check prints and does not fail | A test at the cutoff second, mirroring `test_a_work_item_begun_at_the_cutoff_second_is_held_to_the_rule` |
| Nobody is asked anything | Given the whole rule · When a review run executes it end to end · Then no step puts a question in front of a person | The prompt budget stated in the PR body: zero added questions |

## Data & interfaces

Two row shapes in `templates/sdd-round.md`, both read by
`skills/code-review/scripts/chain_check.py`.

| Row | Shape | Refused |
|---|---|---|
| `Loses a record or crashes` | `no`, or `yes — <what>` | absent, empty, or a value that is neither. A `no` record followed by more than one later round record |
| `New units` (existing row, extended) | `none`, with or without a reason; otherwise `;`-separated entries, each `unit (depth N)` | an entry with no depth, or a depth of 2 or above |

Three constants follow the shape `chain_check.py` already uses for a rule that
cannot be applied backwards — a unix second read from the work item's directory
name, compared against the id of the work item that wrote the rule:

- `FLOOR_FROM` and `DEPTH_FROM`, both `1788472135` — this work item's own id, so
  the first records held to each rule are the ones written under it.

Nothing here reads git, and nothing here is a line number. A round record's
rows are content the author writes; the check reads the file the author wrote.

## Open questions → questions.md

One was asked and answered before the first edit and is recorded there rather
than here. Nothing else is open.
