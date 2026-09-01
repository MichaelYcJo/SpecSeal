# the last round's fixes are reviewed by nobody — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `specs/1788212517-the-last-rounds-fixes-are-reviewed-by-nobody/{routing,spec,plan,questions}.md`; `docs/review-chain-spec.md` (the bound at `:34-56`, the two-records section at `:115-119`, the declaration table); `docs/review-handoff-protocol.md` (the record's field table, the `Pass` section, Conformance); `skills/implement/SKILL.md`; `skills/code-review/SKILL.md`; `CLAUDE.md`; `CONTRIBUTING.md` via the merge-method table; `.specseal/follow-up.md` (empty — nothing here was its prerequisite); issue #33; the incident record `specs/1788184145-…/rounds/round-3.md`
· evidence: `.specseal/map.md` — one section, *Who checked the last round's fixes*, seven rows, stamped `46b66d9`. Round 1's fixes added three and moved the coordinates of three more, which had drifted by hundreds of lines while `evidence_check` still read them as OK
· verified: executed — `tests/test_the_last_rounds_fixes_are_checked.py` (57 cases, each shown red under a mutation with the tree restored and re-checked green after every one), the fourteen narrow prose and chain files, `chain_check.py` run against this repository at baselines `origin/main` and `origin/release/v0.0.2`, `evidence_check.py` (24 ok · 0 drifted · 0 broken), `unverified_check.py`, `ruff check` and `ruff format --check` on the changed Python files. Unverified — the full suite, `ruff check .` and `ruff format --check .` across the tree, which belong after the rounds settle. A spawn prompt for round 1's fixes said so explicitly and it is the same rule either way

## Why this work exists

A review run ended with the orchestrator fixing what the last round found and
ticking `- [x] Pass` on that round's own record; those fixes were read by
nobody. The run now ends with a verifying round pointed at the diff of the
previous round's fixes, and every round record has to say who opened its own.

## What the field is, and where it stopped being only a disclosure

`| Fixes checked by |` takes three values — a later round, `no fixes to
check`, or `nobody — <why>` — and `chain_check.py` refuses everything else,
`the session that wrote them` included.

Most of what it refuses is what the repository can contradict: a missing row,
a checker that does not exist, a checker whose number is later and whose
`Target SHA` is not, and `no fixes to check` beside a verdict that closed with
a fix.

One refusal is not that shape, and it arrived as an answer rather than as
scope. A checked `Pass` beside `nobody — <why>` is two claims that can both be
true of one honest record, and the memo shipped saying the state therefore
passes and prints forever. **The repository owner answered Q1 during round 1
of this work item's own review, with a third option**: refuse it, for work
items whose directory name begins with a unix second at or after
`chain_check.py`'s `STRICT_FROM`, and grandfather everything before.

What that buys is both halves. A check whose first production act is red on
merged history nobody can repair is a check people learn to skip — and
`specs/1788184145-…/rounds/round-3.md` is exactly that history, in exactly
that state. A check whose strongest statement is a print does not stop a
failure mode measured at a 100% hit rate. Grandfathering gets the refusal
without the unfixable red, and the failure names the way out: one verifying
round, which under the cap rule costs no round.

## What the record still cannot enforce

`| Needs a fix |` is the answer a run ends on — the reviewer's own, copied
into the record rather than re-derived from the verdict table, because a 🟡
answered with grounds is a finding that needs no fix. **No check reads it.**
The field exists because round 1 found the warden being told to answer a
question its report format had no field for, which is how the thing a run ends
on comes to live in a transcript. Enforcing it would mean a third migration of
every existing record in one release, and that is not what a fix pass is for;
it is Q4 with the round cap.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which records the field is read on | `spec.md` and `plan.md` both said the LAST record only, matching where `Pass` is read | **Every** record | Found by mutation, not by reading. With the read scoped to the last record, `round-N` is unreachable — a checker must be a LATER round and the last record has none — so breaking the sibling lookup outright left the case meant to cover it green. A vocabulary with one dead value out of three is a defect a reviewer finds; the documents were corrected rather than the test weakened. It costs a repository updating the plugin every record in a touched work item, and that is Q2 |
| What an unrecognised value does | `spec.md`'s first draft said it is *read as `nobody` with no reason* | Refused outright, naming the three values | `hooks/routing.py`'s Review and Destination axes are strict for the same reason: a tolerant read turns prose into an answer. Here the specific prose that would pass is `the session that wrote them`, which is the exact state the field exists to refuse |
| Whether `chain_check.py` refuses `Pass` beside `nobody` | Issue #33 says CI *could* then refuse a record where the fixer and the checker are the same. The first version of this work refused a record that NAMES the fixer as the checker and only disclosed one that names nobody, priced as Q1 | Refuses both, with the second grandfathered for work items begun before the rule landed | The owner answered Q1 during round 1 and the answer was a third option. The disclosure argument survives where it applies — a record that is not the review's verdict, and an unchecked `Pass`, both still only print — and stops applying where the disclosure stands beside the claim that the review passed |
| How a verdict cell is spelled | `verdict_of` lowercased the cell and stripped a full stop, matching the bare `fixed` the sets are written with | Emphasis comes off first, and then the vocabulary is matched against what is left. Round 1 took the commit off by cutting; the row below is where that half was replaced | Executed, by counting. Not one verdict cell in this repository is a bare `fixed`; all fourteen read `**fixed**`, most with a commit after the word. So `closed_with_a_fix` answered False on every record that exists and the refusal separating an honest `nobody` from a silent pass had never once run, while `open_blocking` read a 🔴 genuinely closed as `**fixed** \`sha\`` as still open. Round 1 of this work item's review, 🔴 1 |
| How the verdict word is separated from the commit after it | Round 1's fix located where the citation began and CUT the cell there | The vocabulary is matched as a PREFIX of the cell and no commit is recognised at all | Executed. The cutting pattern required a digit inside the hex run, because `defaced` and `acceded` are seven characters of [0-9a-f] and ordinary English. On a real abbreviation with no digit — about one in 959 — it did not cut late, it did not cut at all, so `**fixed** \`deadbee\`` normalized to `fixed deadbee` and a 🔴 that was properly closed read as still open. The comment stating that cutting late "costs nothing" described a late cut that did not exist. Prefix matching makes the digit question disappear rather than move: verified against all 34 verdict cells in `specs/*/rounds/round-*.md`, 34 recognised. Round 2's 🔴 1, and the repository owner's answer was to change the structure rather than add a second special case |
| Which `Target SHA` each side is read at when a row names two | Round 1's fix compared the checker's NEWEST against this record's FIRST | Both sides at their newest | Executed. `templates/sdd-round.md` allows two SHAs — *both, if HEAD moved mid-review* — so round 1 writing `A and B` and round 2 writing `B` exited 0, where two records at a single shared SHA correctly exited 1. A round that read exactly what this round read was passing as its checker, and how many commits each row happens to list is not a fact about who read what. Round 2 |
| What makes a named checker later | The round number in its filename | The number **and** its own `Target SHA` | Rounds are cheap to number and expensive to run. Two records carrying one `Target SHA` mean round 2 opened the tree round 1 opened, and the fixes that closed round 1 were written after both — so nothing the cell claims happened, and the number alone said nothing about it. Only positively established inversions are refused: the same commit, or the checker's tree an ancestor of this one's. A squash discards both commits, and *cannot be compared* stays a pass |
| The separator between `nobody` and its reason | The first version accepted `—`, `–`, `-`, `:` and `,` | The space too | Executed. Every document shows `nobody — <why>`, with a space before the dash, and the first version refused exactly that spelling. Found by the case asserting it passes, which is the shape a test is for |
| How the edits were made | The environment asked for edits through Bash (`sed`, heredocs); the spawn prompt required the `Edit` tool | The `Edit` tool | `agents/smith.md` phase 3 and `skills/implement/SKILL.md:393`, and work item #34 exists to enforce it. Disclosed rather than done quietly |
| `skills/code-review/SKILL.md`'s records heading | It still read `.specseal/handoff/PR-<n>/`, a directory `docs/review-handoff-protocol.md` says was never once created | Corrected to `specs/<work-item-id>/` in the same edit | Option A is written into that section. A heading naming a dead path directly above new instructions is worse than either alone, and the file is not in `test_the_documents_that_instruct_never_name_the_old_directory`'s list, which is why it survived the move |
| Migrating those same records for `Needs a fix` | The protocol requires the field, and the three records predate it | Left without it | The two fields ask different kinds of question. `Fixes checked by` asks who opened the fixes, and the repository holds the answer — which round followed, and whether one did. `Needs a fix` asks what the reviewer concluded, and a reviewer who was never asked left no answer anywhere; deriving one from the verdict table is the exact derivation the field is defined against. So the Required column reads *from the round that wrote it*, and nothing is fabricated |
| Migrating another work item's merged records | Nothing asked for it | Three rows added to `specs/1788184145-…/rounds/round-{1,2,3}.md` | Its declaration is added relative to `main`, so the release pull request reads all three records, and no fallback ships. Each value is what the records already say: round 2 opened round 1's fixes and found seven things, round 3 confirmed round 2's seven verdicts, and round 3's own fixes were opened by nobody. Nothing else in those files changed, and each carries a comment saying which work item added the row |

## Not verified

| Item | Who must answer |
|---|---|
| The full test suite at this branch's HEAD, plus `ruff check .` and `ruff format --check .` across the tree | the orchestrator, after the review rounds settle — the narrow suites and the changed Python files are green, and a broad seal taken before the rounds is spent by the first fix. Still open after round 1's fixes, and for the same reason |
| That the `Needs a fix` row is actually filled in. No check reads it, so nothing can tell a record that answered from one that left the placeholder | the repository owner, at the first run whose reviewer writes the line. It is Q4's neighbour and priced the same way |
| ✅ Whether the `Pass`-beside-`nobody` refusal fires on a real record rather than on a fixture. Three of this repository's four records are grandfathered; the fourth is this work item's own, whose directory id IS `STRICT_FROM` | **Executed** 2026-09-01 in a fresh clone at `9b5501d`: a `round-2.md` written into this work item's own `rounds/` with `Fixes checked by: nobody — the run ended here` beside a checked `Pass` fails, quoting the record's path and naming the cutoff. The row previously said three records were all there were and no item here could reach the refusal until the next one — false from the moment round 1 wrote the fourth, and printed by `unverified_check.py` on every run since |
| That a spawned reviewer actually recognises a fix diff as its target and stays inside it. The change is prose a session reads, so nothing in the suite can execute it | the repository owner, at the first review run that reaches its verifying round |
| Whether a run can reach a verifying round twice in practice — the cap rule permits it and no run has been through one | the repository owner. It is Q3. **Executed** 2026-09-01, twice: a `round-2.md` written into a copy of this repository makes `chain_check --baseline origin/release/v0.0.2` exit 0, so a finished run's records satisfy the check end to end — Q3's first measurement, recorded in `questions.md`. It does not reach the question here, which is a SECOND verifying round, and that stays unobserved |

## Not done

**Option C of issue #33** — the chain runs until a round returns nothing — was
rejected by the repository owner before this work started, and nothing here
smuggles it back. The terminal condition built is *this round wrote no code
nobody read*, which a round closing a 🟡 with grounds satisfies; C's condition
is *this round found nothing at all*.

**`Pass` beside `nobody` still passes for work items begun before the rule
landed**, and that is Q1's answer rather than an omission. This repository's
own `specs/1788184145-…/rounds/round-3.md` is in that state and prints on
every run.

**The round cap is not enforced in code.** `chain_check.py` prints the record
count and nothing refuses a fourth round. Whether a cap exhausted while a
verifying round opens something is a third case the spec's paragraph denies is
Q4, and it is not this release's to answer.

**`| Needs a fix |` is written and not read.** See *What the record still
cannot enforce* above.

**The field IS read on records the pull request does not touch**, and an
earlier draft of this memo said the opposite. `chain_check.py` reads
`Fixes checked by` on **every** record of a work item whose declaration is in
the diff — the loop's own comment says so and the code does it — where the
`Target SHA` reachability claim is the thing that is skipped for an untouched
record. What that costs is now priced in Q2: editing one line of a work item's
`routing.md` puts the declaration in the diff, and then every historical
record in that item is read, merged ones included.

## Fed back into the spec

`docs/review-chain-spec.md` gains three clauses that no earlier document held,
all marked here as inferred during implementation and open to being
overturned. The third arrived as an answer rather than as an inference:

- **A round that opens nothing needing a fix does not consume the cap.** The
  cap counted rounds, and the issue's own reading is that it could not tell a
  round that found nothing from a round whose fixes nobody read. Making it
  count rounds that found something is the smallest change that lets the
  verifying round exist without moving the numbers.
- **`Pass` and `Fixes checked by` are two claims, not one.** The protocol had
  already split *was it reviewed* from *did it pass*; this splits a third
  question out of the second, and `docs/review-handoff-protocol.md` moves to
  draft 0.5 for it with no fourth conformance rule — whether an unread set of
  fixes fails a change request or only prints is a project's call, so the
  field's own section states both.
- **A check that fails for a state, rather than for a claim, grandfathers the
  records that predate it.** This is Q1's answer generalized, and the protocol
  carries it as guidance to any project that chooses to fail: a check whose
  first act is red on history nobody can repair loses the records it could
  have caught in exchange for the ones it never could. What the cutoff is
  keyed to has to be readable from the record itself, which is why this one
  uses the timestamp already in the work item's directory name.
