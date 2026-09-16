# Feature Specification: the record chain disagrees with itself in five places

<!-- seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/spec.md — WHAT this work
delivers and how we'll know. The policy documents in docs/ outrank this file;
cite them, don't restate. -->

## What is wrong, in one picture

Six issues, one subsystem — the round record generator, the pull-request chain
check, and the two case modules that read them. They are not six unrelated
defects. Five of the six are one shape: **a reader that answers about the wrong
thing and says nothing about it.**

```
the generator writes round N's verdicts forward into round N+1
  ├─ #404  the two sides pick a different row at one coordinate      → the wrong verdict carries
  └─ #405  the refusal that caught a broken table became silence     → a truncated table passes

the chain check reads a row's severity at the pull request
  └─ #408  it reads the whole row, not the `#` cell                  → a 🟢 row is failed as 🔴

the cases that guard both
  ├─ #407  a fixture's substitution is never asserted                → the case passes vacuously
  └─ #406  a pin refuses the one spelling its own rule allows        → correct text goes red

and one cause closed at its instance
  └─ #414  nine cells repaired by hand, the generator untouched      → the next record carried it
```

The sixth, #414, is the class rule stated as a defect: `agent-contract` §12
says the fix is owed to every instance the same cause produces, and the run that
met this one repaired the instances and left the cause standing.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-chain-spec.md` §*Two records, and what each of them says* | A record is committed before the fixes it commissions, so both spawn orders are reachable and the forward reach cannot be replaced by ordering `close` before `new`. This is why #404 and #405 are repairs to the reach rather than to a procedure |
| `skills/agent-contract/SKILL.md` §12 | A defect belongs to a class. #414 is that rule violated; #407 and #414 each carry a class this work has to enumerate rather than close at the coordinate the issue names |
| `skills/agent-contract/SKILL.md` §14 | Three of the six change text a person reads and acts on — a refusal message (#408), a refusal's exit sentence (#406), a rendered fix note (#414). Each new text is pinned in the same commit |
| `skills/agent-contract/SKILL.md` §15 | Every case this work plants is seen red first, against the pre-fix module or with the sentence it pins removed. This is the work item's own subject one level in |
| `CLAUDE.md` §*a thing more than one party can have is named with whose* | Names `tests/test_one_word_one_meaning.py` as the check that holds the rule. #406 is the decision about a second check claiming the same rule with a stricter reading |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | The changelog entry goes to this directory's `changelog.md`, evidence rows to `seal/ledger/1789455558-….md`. Never `CHANGELOG.md`, never `seal/ledger.md` |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | Every fixture this work touches keeps neutral values. `tests/test_no_real_identifiers.py` is the check |

## Scope

### In

| # | What changes | Coordinate |
|---|---|---|
| #404 | `close`'s forward map takes the **first** row at a coordinate, the way `inherited_rows` does | `skills/code-review/scripts/round_record.py#close` |
| #405 | The unconditional silence at `filled == 0` becomes a refusal conditioned on whether round N+1's inherited table accounts for round N's coordinates | `skills/code-review/scripts/round_record.py#reach_forward` |
| #414 | The fix-table note strips a trailing period, widened at the call site | `skills/code-review/scripts/round_record.py#fix_table` (the cut at `:3115`) |
| #408 | A row's severity is read from its `#` cell, and an unrecognised verdict word gets its own message | `skills/code-review/scripts/chain_check.py#open_blocking` and its caller |
| #406 | The duplicate `"the seal" not in out` pin is removed; the sweep keeps the rule alone | `tests/test_the_seal_is_taken_once_by_the_sealer.py:1307` |
| #407 | The fixture asserts its substitution landed, and the case it feeds gains a positive assertion | `tests/test_the_fixes_close_the_record.py#one_finding_inside_one_earlier_unit` |

Each of the six carries a class enumeration, not a coordinate fix. What the
class is for each one is `plan.md`'s business.

### Out, and why each one is out

| Excluded | Why |
|---|---|
| **Refusing a coordinate that carries two verdict rows** (#404's alternative) | A repeated `Location` inside one record is the ordinary shape, not a malformed one — the committed corpus carries it in dozens of records. Refusing it would refuse records this repository already wrote. The reasoning and the re-measurement are `plan.md` §*Alternatives considered* |
| **Widening `chain.SEPARATORS`** (#414's alternative) | Five readers share that constant, and the comment six lines above the call site already gives that reason. Widening it changes what `deferred`'s home reader and `chain_check`'s own readers accept |
| **The nine cells already repaired by hand at `9919b265`, and `round-2.md`'s two** | They live on `fix/401-402-the-broad-gate-row-runs-unchecked-and-is-never-asked-for`, a branch this one did not cut from. Editing another branch's records here would collide at its merge. The cause is what this work removes; the instances are that branch's |
| **A `## Inherited coordinates` reader in `chain_check.py`** | #405 established that `close`'s reach is the section's only reader, and adding a second reader at the pull request is mechanism nobody asked for. If that section should also be checked at the pull request, it is a separate work item with its own frame |
| **The five `nobody`/`deferred`/vocabulary readers that share `chain.SEPARATORS`** | Reading them is how #414's class is bounded; changing them is not in this work. If one of them turns out to have the same stray-punctuation shape, it becomes a row in `seal/follow-up.md` with an answerer, not a seventh phase |
| **Anything in `seal/ledger.md`** | This branch removes no code an existing shared-ledger row cites. Its rows go to `seal/ledger/1789455558-….md` |
| **The full suite, the repository-wide lint, the typecheck** | `agent-contract` §2 assigns the broad gate to `agents/sealer.md`, once, after the rounds settle. No phase of this work runs it |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 — one coordinate, two rows | **Given** round 1 carries `🔴 1 … open` and, below it, an unnumbered `🟢 … verified` at the same `Location`, **when** `close --round 1` runs with finding 1 closed `fixed`, **then** round 2's inherited row for that coordinate reads round 1's `🔴 1 — fixed` | A case in `tests/test_the_fixes_close_the_record.py` asserting the `Why` cell's text, red against the last-wins map |
| A2 — the two sides agree by construction | **Given** any record whose verdict table repeats a `Location`, **when** both `inherited_rows` and `close`'s map read it, **then** they name the same row | A case building a three-row repeat and asserting the `#` cell the two sides agree on |
| A3 — a re-review round still passes | **Given** round 2 whose every coordinate round 1 already claimed, **when** `close --round 1` runs, **then** exit 0 and nothing is said about the reach | `test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused` stays green |
| A4 — a truncated inherited table is refused | **Given** round 2 generated normally and then every body row of its `## Inherited coordinates` deleted, **when** `close --round 1` runs, **then** it exits 2 and names the coordinates round 2 no longer accounts for, and **nothing is written** to either record | A case asserting exit 2, the named coordinates, and both files byte-identical to before the run |
| A5 — the corpus is not refused | **Given** every committed `round-N.md` pair in `seal/specs/`, **when** the new accounting predicate is applied, **then** no pair is unaccounted | A measurement run over the corpus, its figure recorded in `overview.md` |
| A6 — the note carries no stray period | **Given** a fix table whose third cell opens `` `6233b769`. ``, **when** `close` renders the verdict row, **then** the grounds read `fixed at 6233b769 — <note>` with one separator between the dash and the note | A case asserting the rendered cell, red against the un-widened strip |
| A7 — a 🟢 row quoting a 🔴 is not a blocking finding | **Given** a last round whose 🟢 row's Grounds quote an earlier round's 🔴 and whose verdict is closed, **when** `chain-check` runs at the pull request, **then** it says nothing about that row | A case in `tests/test_chain_check_at_the_pull_request.py`, red against the whole-row join |
| A8 — an unrecognised verdict is still refused, by its own name | **Given** a row whose verdict cell reads `verified`, **when** `chain-check` runs, **then** it refuses the row with a message that names the verdict word as outside the vocabulary, names the vocabulary, and **does not name 🔴** | A case asserting the new sentence and asserting the old one absent (§14) |
| A9 — `the sealer` is not refused | **Given** a refusal whose exit sentence reads *…before the sealer runs*, **when** the suite runs, **then** nothing goes red | The rewritten sentence committed with the pin removed; `test_one_word_one_meaning.py` green |
| A10 — an anonymous seal is still refused | **Given** that same sentence rewritten to leave the instance anonymous, **when** `test_one_word_one_meaning.py` runs, **then** it goes red naming the file and the span | Executed as the red-first mechanism for A9 |
| A11 — a fixture that fails to substitute says so | **Given** `one_finding_inside_one_earlier_unit` with its pattern altered so the substitution misses, **when** the fixture runs, **then** it fails at its own assertion rather than producing a record the case reads | Executed against a deliberately broken pattern |
| A12 — the case asserts the judgment it is named for | **Given** the depth-1 judgment made, **when** the case runs, **then** a positive assertion holds that is false when `depth_two` returned at its guard | A case assertion on the record's own text, red when round 1 names no unit |

## Data & interfaces

No schema, no endpoint, no payload. Four surfaces change, and all four are text
a person reads:

| Surface | Before | After |
|---|---|---|
| Round N+1's `Why` cell at a repeated coordinate | the last verdict row at that `Location` | the first — the row `inherited_rows` attributed it to |
| `close`'s behaviour on a truncated inherited table | exit 0, silent | exit 2, naming the unaccounted coordinates, nothing written |
| A `fixed` row's Grounds | `fixed at <sha> — . <note>` | `fixed at <sha> — <note>` |
| `chain-check` on a row with an unrecognised verdict | *this 🔴 row reads `verified` — a blocking finding…* | a sentence naming the verdict as outside the vocabulary, with the vocabulary, and no 🔴 |

Each of the four is pinned by a case in the same commit (`agent-contract` §14).

## The constraint that shapes the plan

**This is the machinery that reviews this work item.** `round_record.py` writes
this branch's own round records and `chain_check.py` reads the last one at the
pull request. A repair landing between two of this branch's rounds would leave
its own records written by two different generators.

`plan.md` §*How this branch avoids sawing off the limb it sits on* states the
ordering rule and the guard. It is a scope clause as much as a plan clause: **no
phase of this work runs `round-record` against this work item's own
`rounds/` directory.**

## Open questions → questions.md

The five judgments the issues left open are decided in `plan.md`
§*Alternatives considered*, with the grounds beside each and the measurement
that would overturn it named.

**Nothing in `questions.md` blocks the build.** Its two person rows are about
records and ticket fields outside this branch, and each carries a default that
continues. The rest are a measurement or the work.
