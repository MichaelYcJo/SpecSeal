# Feature Specification: the verifying round is bounded, not the cheapest (#639)

<!-- seal/specs/1790562542-the-verifying-round-is-bounded-not-cheapest/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

Every coordinate below was read on 2026-09-28 at `97a30dc6` (the routing
commit on `1fa25931`, which is `origin/release/v0.15.7` and `main`). The
issue's coordinates were written at `2037cf0`. Each quoted sentence was found
at the place the issue names, with the same words.

| Policy clause | What it fixes for this work |
|---|---|
| `docs/review-chain-spec.md` §*The last round verifies, and what it verifies is a diff* | This section owns the verifying round's rule. `skills/code-review/orchestration.md` §*Orchestrator: the run ends with a verifying round* says so twice ("`docs/review-chain-spec.md` §*The last round verifies* owns the rule"). So the measured basis is written here and nowhere else, and the other carriers point at it. The rule stays as it is: when the round runs, what it targets, what it does, and when it ends the run. Only the cost sentence changes |
| `docs/review-handoff-protocol.md` §*After the run — the per-segment bars* | The `verifying` row's verdict `exempt` stays. `seal/releases/0.4.0.md`'s row *"a verifying segment exempt"* is still true, and `tests/test_the_handoff_before_round_one.py#test_the_protocol_names_a_bar_per_segment_kind` pins `\| verifying \| exempt \|`. Only the Grounds cell changes. The exemption's recorded origin is #51 observation 1: *"verifying ~1.5 (fewer independent axes to open)"* (read from #51's body). It was never cost |
| `skills/agent-contract/SKILL.md` §12 | The class is **a sentence saying the verifying round costs less because its target is a diff**, in any words. The sweep below lists every member. The phrase is only one spelling of the class |
| `skills/agent-contract/SKILL.md` §14, §15 | Every sentence that changes is pinned in the commit that changes it. Every new pin is seen red before it is planted |
| `skills/agent-contract/SKILL.md` §5 | The figures come from the issue and are not this frame's findings (see *The measured basis*). The document names the issues they came from, so a reader can check the number |
| `docs/review-chain-spec.md` §*The survivor sweep — a corrected sentence standing somewhere else* | `survivor-check --range` is run by the implementer's verify phase on this branch's range. It is the tool's version of the sweep below |
| `CLAUDE.md` *a change writes fragments, never the shared file* | The changelog entry goes in `seal/specs/1790562542-the-verifying-round-is-bounded-not-cheapest/changelog.md`. A new ledger row goes in `seal/ledger/1790562542-the-verifying-round-is-bounded-not-cheapest.md`. Rows an edit drifts are re-read and re-stamped in the file they live in (plan.md, *Ledger rows this edit drifts*) |
| `docs/the-evidence-ledger.md` §*The marker is the fold's record* | This work item writes no `<!-- specs/<id> -->` marker into `docs/`. A marker on a live line records a fold. Writing it is `settle`'s act at retirement, and a marker written now would record a fold that has not happened |

## The measured basis, and whose it is

All figures below were **read**. This frame executed nothing to produce them.

- **#639's own body.** Over 0.14.0–0.15.5, 29 verifying rounds ran at a median of 0.83 × their own round 1's span. The range was 0.26–1.27, and five of the 29 were at or above round 1. The issue states this was *"executed over the metered blocks of #496, #535, #577, #601 and #619"*. Answerer: the author of #639. This frame did not re-derive it (questions.md Q1).
- **#456, 0.12.2** (the comment that measured three work items). *"Every one of the nine sits between 13.8 and 17.8 minutes and between 46 and 58 calls, whatever its target … Nine for nine, it is not."* It also gives the cause: *"What a round spends is the frame, the earlier records and the probes, and none of those shrink with the diff."*
- **#51 observation 1.** The source of the `verifying: exempt` bar: *"verifying ~1.5 (fewer independent axes to open)"*.

The #456 call counts also disprove the second clause of the protocol row, *"a segment that small is the nuance below in its every case"*. The nuance it points at is *"a 23-call round read 1.64"*, and #456 measured verifying rounds at 46–58 calls. So the row's size claim is in the class too, and it goes with the cost claim. That departs from the ticket's option 1, which says to ground the exemption on "the segment size". plan.md's Alternatives table records the departure.

## Scope

### Every carrier, enumerated

**The sweep.** 2026-09-28, over `agents/`, `skills/`, `docs/`, `templates/`, both READMEs, `CONTRIBUTING.md`, `CLAUDE.md`, `hooks/`, `bin/`, `evals/` and `tests/`. Terms searched: `cheapest`, `cheaper`, `cheap`, `cheaply`, `costs? less`, `less expensive`, `inexpensive`, and every line mentioning a verifying round within a four-line window of `small|short|quick|fast|light|brief|afford|bounded|cost|cheap|expens|minute|calls`. The Korean documents (`README.ko.md` and the three `docs/**/*.ko.md`) were searched separately for `가장 싼|저렴|비용`. **This was a reading, not a check.** `survivor-check` in phase 2 is the executed version.

| # | Coordinate | What it says now | Verdict |
|---|---|---|---|
| C1 | `skills/code-review/orchestration.md` §*Orchestrator: the run ends with a verifying round*, table row `Target` | "the **diff of those fixes**, not the branch. That is what keeps it bounded: it is the cheapest round of the run" | **edit** |
| C2 | `docs/review-handoff-protocol.md` §*After the run — the per-segment bars*, row `verifying`, Grounds cell | "it targets the diff of the last fixes and is the cheapest round of the run by design; a segment that small is the nuance below in its every case" | **edit** (both clauses) |
| C3 | `docs/review-chain-spec.md` §*The last round verifies, and what it verifies is a diff*, the paragraph beginning "What it costs is one extra spawn per work item" | "on a surface that is a diff rather than a branch — the cheapest round of the run" | **edit** |
| C4 | `agents/warden.md` §*Role*, the bullet **A verifying round has a diff for a target**, its second paragraph | "That surface is the whole reason the round is affordable, and widening it back to the branch is the shape of round this one exists to be cheaper than." | **edit**. The issue's phrase sweep missed this one. It makes the same claim in other words: the surface makes the round cheap. #456's cause statement contradicts it |
| C5 | `tests/test_the_last_rounds_fixes_are_checked.py#test_the_verifying_rounds_target_is_the_previous_rounds_fixes`, docstring | "Widened back to the branch it is an ordinary round, and the run gains a full walk it was promised it would not pay for." | **edit**. A test's prose in the same class, in the file whose needle changes anyway |
| C6 | `tests/test_the_last_rounds_fixes_are_checked.py#WHAT_IT_TARGETS`, the orchestration entry | the needle `"keeps it bounded: it is the cheapest round of the run \|"` | **edit**: it pins C1's new text, in C1's commit |

**Met and left alone, with the grounds for each.** A reviewer who disagrees overturns the row by opening the coordinate.

| Coordinate | What it says | Why it is outside the class |
|---|---|---|
| `skills/code-review/SKILL.md` (the `## What this round was asked` paragraph), `templates/sdd-round.md` (the #81 comment under `## What this round was asked`), `tests/test_a_segments_record_says_what_it_was_asked.py` (docstring and the `"cheapest round"` probe), `CHANGELOG.md` (a released entry) | #81's round 1 was "the cheapest round on record / measured" | This is a claim about a **finding** round (#81's round 1, 7.6 m / 29 calls), and it is credited to its spawn prompt, not to a diff target. The issue's reading is confirmed. There is a separate doubt about it, filed under *Out of scope* |
| `agents/smith.md` ("which costs no round"), `templates/sdd-round.md` ("The way out costs no round"), `docs/round-record-spec.md` ("the way out costs no round"), `skills/code-review/scripts/chain_check.py` (the `Pass`-beside-`nobody` message) | the verifying round "costs no round" | This is cap arithmetic, and the rule makes it true: a round that opens nothing needing a fix does not consume the cap. Each sentence is next to that clause. It says nothing about minutes or calls |
| `agents/warden.md` §*Role*, the paragraph "A round that exists to check one fix is scoped to that fix" | re-reading the whole diff "turns every returned finding into the price of a first round" | It compares one round at two scopes and says the wider one costs up to a first round. No measurement tested a widened re-check. What was measured is the verifying round, which stayed scoped and still cost about a round 1, and that does not contradict an upper bound |
| `README.md`, `README.ko.md` (the `Fixes checked by` paragraph) | "does not spend one of the three" / "3회 한도를 쓰지 않습니다" | Cap arithmetic, as above |
| `skills/code-review/orchestration.md` `round-N` row, `docs/round-record-spec.md`, `tests/test_the_last_rounds_fixes_are_checked.py` ("a number is cheap and a round is not" / "Rounds are cheap to number and expensive to run") | rounds are expensive | This agrees with #456. It is not a claim that the verifying round costs less |
| every other `cheap*` hit in the sweep | cost claims about other acts: a sealer, a fix pass, a probe, a check's direction of error, a release moment | None of them is about the verifying round |

### In

1. **C1: the `Target` row keeps "bounded" and drops "cheapest".** Keep: the target is the diff of those fixes, not the branch, and that is what keeps the round bounded. Add: its cost is set by the frame, the inherited records and the probes, so it runs close to a finding round. Point at `docs/review-chain-spec.md` §*The last round verifies* for the measurement. The cell carries no figure (plan.md, Alternatives A2). The cell contains no bare `|`.
2. **C2: the `verifying` row grounds `exempt` on what the round is.** The Grounds cell keeps *it targets the diff of the last fixes*. It adds the job: answering each closed verdict, which leaves fewer independent axes to open at once than a branch does, and it names #51 observation 1 as the place the exemption comes from. It contains no cost claim and no size claim: no "cheapest", no "small", no "by design" attached to either. The verdict cell stays `exempt`. The `**At very small rounds**` paragraph below the table is unchanged. It is the bar's own nuance, and no longer something the row points to.
3. **C3: the chain-spec paragraph states the cost as measured.** Keep *one extra spawn per work item* and *What it does not cost is a change to the numbers above*. Replace *— the cheapest round of the run* with three points. The surface is bounded to the diff. What the round spends is the frame, the earlier records and the probes, and none of those shrink with the diff. The measured basis, which carries: median 0.83 × the round 1 of the same work item, the count (29), the releases (0.14.0–0.15.5), the range (0.26–1.27), how many were at or above round 1 (five), and the issues it was read from (#496, #535, #577, #601, #619). Citing #456's nine-for-nine at 0.12.2 is optional. This paragraph is the one place the figure lives.
4. **C4: the warden stays inside the diff because of its job, not its price.** Keep *Recognise it from the prompt, which hands you a fix diff instead of a branch, and stay inside it.* Replace the affordability sentence with the real reason. The round's job is whether each closed verdict is actually closed. Widened back to the branch, it re-reviews what the earlier rounds already reviewed and becomes another finding round. The next paragraph (*Opening something anyway is allowed and is the point*) is unchanged.
5. **C5: the test docstring says the same thing as C4**, with no promise about cost.
6. **C6 and a gone/stands pin.**
   - C6's needle becomes C1's new text, in C1's commit.
   - A new module pins each of C1–C4 on two sides. The *stands* half is a phrase only the new wording uses. The *gone* half is the carrier's own old wording at `1fa25931`. The shape follows `tests/test_the_broad_gate_cell_keeps_every_run.py#GATE_CARRIERS` (A11 of 0.15.0).
   - A third case asserts that `cheapest round of the run` appears nowhere under `agents/`, `skills/`, `docs/`, `templates/`, `README.md` or `README.ko.md`. It turns the issue's acceptance grep into a pin that catches a fifth carrier.
7. **The records.** A changelog fragment. One ledger fragment row that anchors the four edited units and the new test. The seven drifted rows are re-read and re-stamped where they live (plan.md).

### Out

| What | Why | Who answers it |
|---|---|---|
| #51's body paragraph "The verifying round is the cheapest round of the run, measured" (#636) | It is not a file in this tree. The orchestrator edits #51 itself, and #51's header says #636 already revised it on 2026-09-28 | the orchestrating session |
| **Whether "#81's round 1 was the cheapest round on record" is true** | Outside the class (see above), but it looks doubtful. #51's baseline table lists #29's verifying round at 4.2 m / 10 calls, which is cheaper than 7.6 m / 29. #51 was opened on 2026-09-01 and #81 on 2026-09-02. But #51's body is revised in place, so this frame cannot tell whether that table stood when the #81 sentence was written. **Read, not verified**: this frame did not find the 7.6 m / 29 figure in #81's body or comments, and does not know which set "on record" meant. Four carriers hold the sentence (listed above) | the orchestrating session, which decides where it goes on `docs/review-chain-spec.md` §*Where a leftover goes*'s ladder |
| **Whether `verifying: exempt` still holds** | The exemption rests on #51 observation 1's single reading (~1.5). #456 measured verifying rounds at 1.35 and 1.38 tools per turn against 1.45 for their round 1, so the difference between the kinds may be small. This item keeps the exemption and corrects only its grounds. Changing the bar would alter the policy, which is another work item | a measurement: the next flow-measurement sweep (#51's owner) |
| `CHANGELOG.md` released sections | A released entry is not rewritten. `docs/review-chain-spec.md` §*What the sweep reads* excludes them for that reason | nobody. It is a record |
| Any change to what the verifying round is or does | The rule is right. Only its price tag was wrong | n/a |

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1: an orchestrator reads why the run ends with a verifying round | Given `skills/code-review/orchestration.md`, when it reads the `Target` row, then the row says the diff target bounds the round and that its cost follows the frame, the records and the probes. It does not say the round is the cheapest, and it points at the chain spec for the numbers | `bin/test tests/test_the_last_rounds_fixes_are_checked.py -q` with C6's new needle (executed), plus the new module's stands and gone halves for C1 |
| S2: a session judges a verifying segment against the bars | Given `docs/review-handoff-protocol.md`'s bars table, when it reads the `verifying` row, then it finds `exempt` and grounds taken from the round's target and job, with no cost claim or size claim | the new module's C2 pair, plus `tests/test_the_handoff_before_round_one.py#test_the_protocol_names_a_bar_per_segment_kind` still green (executed) |
| S3: a reader asks what a verifying round costs | Given `docs/review-chain-spec.md` §*The last round verifies*, when they read the cost paragraph, then they find one extra spawn, a bounded surface, the reason the cost does not shrink with the diff, and the median, count, releases, range and source issues | the new module's C3 pair (executed). A reviewer opens one source issue to check the figure (read) |
| S4: a warden is spawned on a fix diff | Given `agents/warden.md` §*Role*, when it reads the verifying-round bullet, then it is told to stay inside the diff because its job is the answers, and nothing says the surface makes the round affordable | the new module's C4 pair (executed) |
| S5: a later edit brings the phrase back anywhere | Given any file under `agents/`, `skills/`, `docs/`, `templates/`, `README.md` or `README.ko.md`, when it contains `cheapest round of the run`, then the new module fails and names the file | the tree-wide case (executed) |
| S6: every new pin can fail | Given each new or changed assertion, when the sentence it pins is restored to its old wording (gone half) or deleted (stands half), then that case is red | shown red once per carrier before commit and reported in the phase record (executed, §15) |
| S7: nothing else moved | Given the branch, when `survivor-check --range origin/release/v0.15.7..HEAD` runs, then every survivor it names is either corrected or deliberately exempted in this item's `survivors.md` with a reason | executed in phase 2 |
| S8: the ledger stays true | Given the seven rows plan.md names, when `evidence-check .` runs after the edits, then no row this branch drifted is left DRIFTED. Each was re-read against the edit and re-stamped with a dated note. A row whose claim the edit made false is corrected in place first (none is expected: plan.md) | `evidence-check .` before and after (executed) |
| S9: #81's sentence is untouched | Given the four #81 carriers, when the branch's diff is read, then none of them changed | `git diff --stat origin/release/v0.15.7...HEAD` (read) |

## Data & interfaces

No code path, no schema, no output. The interfaces are four sentences a
session reads and acts on (C1–C4), one test docstring (C5), one test needle
(C6), one new test module, a changelog fragment and ledger rows.

## Open questions → questions.md

Q1 (a measurement) is the only open row, and it does not block the build.
The judgments the tree answered are listed at the head of that file.

Framed 2026-09-28 by framer, before the build.
