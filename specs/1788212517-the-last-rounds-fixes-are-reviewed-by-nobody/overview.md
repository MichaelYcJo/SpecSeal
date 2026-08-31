# the last round's fixes are reviewed by nobody — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `specs/1788212517-the-last-rounds-fixes-are-reviewed-by-nobody/{routing,spec,plan,questions}.md`; `docs/review-chain-spec.md` (the bound at `:34-56`, the two-records section at `:115-119`, the declaration table); `docs/review-handoff-protocol.md` (the record's field table, the `Pass` section, Conformance); `skills/implement/SKILL.md`; `skills/code-review/SKILL.md`; `CLAUDE.md`; `CONTRIBUTING.md` via the merge-method table; `.specseal/follow-up.md` (empty — nothing here was its prerequisite); issue #33; the incident record `specs/1788184145-…/rounds/round-3.md`
· evidence: `.specseal/map.md` — one new section, *Who checked the last round's fixes*, four rows, stamped `46b66d9`
· verified: executed — `tests/test_the_last_rounds_fixes_are_checked.py` (27 cases, each shown red under a mutation with the tree restored and re-checked green after every one), the twelve narrow prose and chain files (333 passed), `chain_check.py` run against this repository at baseline `origin/main`, `evidence_check.py` (18 ok · 0 drifted · 0 broken), `unverified_check.py`, `ruff check` and `ruff format --check` on the three changed Python files. Unverified — the full suite, which belongs after the rounds settle

## Why this work exists

A review run ended with the orchestrator fixing what the last round found and
ticking `- [x] Pass` on that round's own record; those fixes were read by
nobody. The run now ends with a verifying round pointed at the diff of the
previous round's fixes, and every round record has to say who opened its own.

## What the field is, and what it deliberately does not do

`| Fixes checked by |` takes three values — a later round, `no fixes to
check`, or `nobody — <why>` — and `chain_check.py` refuses everything else,
`the session that wrote them` included.

It refuses what the repository can contradict and nothing more. A checked
`Pass` beside `nobody` is **not** refused, and that is a decision rather than
an omission: `Pass` says no finding in this round's table is open, `nobody`
says who opened the fixes, and both can be true of the same honest record. The
one record in this repository that is in that state is
`specs/1788184145-…/rounds/round-3.md`, it is merged, and there is no honest
repair — writing a `round-4.md` for a review nobody ran fabricates one, and
unchecking its `Pass` fails the ready-pull-request rule instead. So the state
passes and prints, on every CI run, forever. That is Q1.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which records the field is read on | `spec.md` and `plan.md` both said the LAST record only, matching where `Pass` is read | **Every** record | Found by mutation, not by reading. With the read scoped to the last record, `round-N` is unreachable — a checker must be a LATER round and the last record has none — so breaking the sibling lookup outright left the case meant to cover it green. A vocabulary with one dead value out of three is a defect a reviewer finds; the documents were corrected rather than the test weakened. It costs a repository updating the plugin every record in a touched work item, and that is Q2 |
| What an unrecognised value does | `spec.md`'s first draft said it is *read as `nobody` with no reason* | Refused outright, naming the three values | `hooks/routing.py`'s Review and Destination axes are strict for the same reason: a tolerant read turns prose into an answer. Here the specific prose that would pass is `the session that wrote them`, which is the exact state the field exists to refuse |
| Whether `chain_check.py` refuses `Pass` beside `nobody` | Issue #33 says CI *could* then refuse a record where the fixer and the checker are the same | Refuses a record that NAMES the fixer as the checker; discloses one that names nobody | Those are two states, not one. `round-1` on `round-1.md` is the fixer certifying its own work and is refused. `nobody` is nobody certifying anything, which is a disclosure, and failing for a disclosure is what teaches people to write none — `unverified_check.py`'s own reasoning, one level up. Priced as Q1 rather than decided |
| The separator between `nobody` and its reason | The first version accepted `—`, `–`, `-`, `:` and `,` | The space too | Executed. Every document shows `nobody — <why>`, with a space before the dash, and the first version refused exactly that spelling. Found by the case asserting it passes, which is the shape a test is for |
| How the edits were made | The environment asked for edits through Bash (`sed`, heredocs); the spawn prompt required the `Edit` tool | The `Edit` tool | `agents/smith.md` phase 3 and `skills/implement/SKILL.md:393`, and work item #34 exists to enforce it. Disclosed rather than done quietly |
| `skills/code-review/SKILL.md`'s records heading | It still read `.specseal/handoff/PR-<n>/`, a directory `docs/review-handoff-protocol.md` says was never once created | Corrected to `specs/<work-item-id>/` in the same edit | Option A is written into that section. A heading naming a dead path directly above new instructions is worse than either alone, and the file is not in `test_the_documents_that_instruct_never_name_the_old_directory`'s list, which is why it survived the move |
| Migrating another work item's merged records | Nothing asked for it | Three rows added to `specs/1788184145-…/rounds/round-{1,2,3}.md` | Its declaration is added relative to `main`, so the release pull request reads all three records, and no fallback ships. Each value is what the records already say: round 2 opened round 1's fixes and found seven things, round 3 confirmed round 2's seven verdicts, and round 3's own fixes were opened by nobody. Nothing else in those files changed, and each carries a comment saying which work item added the row |

## Not verified

| Item | Who must answer |
|---|---|
| The full test suite at this branch's HEAD, plus `ruff check .` and `ruff format --check .` across the tree | the orchestrator, after the review rounds settle — the narrow suites and the three changed Python files are green, and a broad seal taken before the rounds is spent by the first fix |
| That a spawned reviewer actually recognises a fix diff as its target and stays inside it. The change is prose a session reads, so nothing in the suite can execute it | the repository owner, at the first review run that reaches its verifying round |
| Whether a run can reach a verifying round twice in practice — the cap rule permits it and no run has been through one | the repository owner. It is Q3, and the argument for why nothing loops is in `docs/review-chain-spec.md` rather than measured |

## Not done

**Option C of issue #33** — the chain runs until a round returns nothing — was
rejected by the repository owner before this work started, and nothing here
smuggles it back. The terminal condition built is *this round wrote no code
nobody read*, which a round closing a 🟡 with grounds satisfies; C's condition
is *this round found nothing at all*.

**`Pass` beside `nobody` still passes.** Q1 in `questions.md` prices both
sides with the repository owner as answerer. The cost of the strict version is
this repository's own release pull request going red on a record that is
already merged.

**The field is not read on records the pull request does not touch.** That is
`chain_check.py`'s existing rule for round records and it is unchanged here: a
record that arrived in an earlier merge is history, and its review was
enforced at the pull request that added it.

## Fed back into the spec

`docs/review-chain-spec.md` gains two clauses that no earlier document held,
both marked here as inferred during implementation and open to being
overturned:

- **A round that opens nothing needing a fix does not consume the cap.** The
  cap counted rounds, and the issue's own reading is that it could not tell a
  round that found nothing from a round whose fixes nobody read. Making it
  count rounds that found something is the smallest change that lets the
  verifying round exist without moving the numbers.
- **`Pass` and `Fixes checked by` are two claims, not one.** The protocol had
  already split *was it reviewed* from *did it pass*; this splits a third
  question out of the second, and `docs/review-handoff-protocol.md` moves to
  draft 0.5 for it with no fourth conformance rule — a rule the reference
  implementation only warns about is not a rule.
