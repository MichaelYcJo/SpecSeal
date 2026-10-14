# Feature Specification: every doc states the current rule only

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Part C of #923. The shape, the check, the restatement arms and the non-inferiority proof are #923's frame (`seal/specs/1791933022-every-agent-skill-and-doc-states-the-current-rule-only/spec.md` §*The shape of a compact file*, §*A rule stated twice is caught, in three arms*, §*Non-inferiority, proved per phase*) and are applied here, never redesigned. This file holds what is specific to `docs/`: the measurement, the targets, the coupling and the order.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Nothing here asks a person; a rewrite is proved by #923's suite where an agent case opens the file, and by its census and the tests that hold the rule where none does |
| `CONTRIBUTING.md` §*What a change to a gate must carry*, §*House rules* | No gate is added; a re-pointed pin is seen red first (contract §15). Every document with a `.ko.md` edition moves with its English one, so the `one-root-by-lifetime` pair is rewritten in one phase to one outline (`tests/test_both_editions_carry_the_same_folds.py`) |
| `docs/the-record-layout.md` §*The size a reader takes whole*, §*docs/*, §*A change writes fragments, never a shared file* | ≤ 1,000 lines and 64 KB per file; the index row for the one-root pair is rewritten to the question the pair answers after this work; rows and the changelog go to this item's fragments |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*, §*A claim held by a test* | 348 released rows anchor into `docs/` (table below); each is read against the new text one at a time — `Re-read ·` through `--reverify --into` where the claim holds, `Corrected ·` by hand where it went or where a test holds it; never a bulk pass (the owner, 2026-10-08) |
| `docs/the-reader-registry.md` §*A frame names what its work removes* | `## Removes` below, read by the records arm |
| `skills/settle/SKILL.md` §2, `tests/test_a_document_has_room_for_the_next_fold.py` | A `docs/` file is a fold target: its headings stay so fold markers and anchors keep their coordinates, and a rewritten file leaves room under the ceiling |
| `tests/test_the_rules_have_one_owner.py`, `tests/test_the_ledger_rules_have_one_home.py`, `tests/test_the_rules_claude_md_names_have_one_home.py` | Nine review-chain rules, four ledger rules and four `CLAUDE.md` rules each have one owning sentence in a `docs/` file; a rewrite keeps the owner's sentence or re-points the pin in the same commit |
| `tests/test_no_passage_is_pasted_into_a_second_file.py` (`BASELINE`) | A pair this work drains lowers its entry in the same commit; two branches lowering one entry re-measure at the merge (the case prints the count) |
| `skills/implement/SKILL.md` §3 | A `docs/` file is text an agent reads and acts on when a skill sends it there: the top rung |

## The problem, measured

`executed` at 92cc85dd (= `origin/release/v0.22.0` a8d83663 plus the routing commit): `wc -lc docs/*.md`; `scratchpad/941/measure.py` (its output `measure.txt`), which runs #930's `budget_check.classify` at 661dc60b and the same classifier with #923's widened marks and list-item opener, counts bold-led paragraphs, ledger anchors over `seal/ledger.md` and `seal/releases/*.md`, test literals ≥ 25 characters found verbatim, `BASELINE` runs and `§*…*` citations from outside; opens are `Read` calls on the path over the 530 transcript files of 16 sessions under `~/.claude/projects/-Users-michael-Documents-GitHub-SpecSeal/` (transcripts that open it · calls, confounded by work items that edited the file's subject).

| File | Lines | Bytes | History #930 · widened | Bold paras · > 8 lines | Non-bold para lines | Kept est. B | Released rows (anchors) | Pin modules (literals) | `BASELINE` runs | § cited from outside | Opened |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `worktree-guard-spec.md` | 999 | 74,355 | 39 · 36 | 50 · 16 | 463 | 33,259 | 79 (103, all headings) | 9 (52) | 1 | 4 | 23 · 486 |
| `review-chain-spec.md` | 999 | 70,140 | 25 · 27 | 65 · 22 | 246 | 43,041 | 27 (27) | 37 (110) | 203 | 10 | 13 · 76 |
| `round-record-spec.md` | 1,000 | 69,835 | 17 · 18 | 60 · 24 | 290 | 43,953 | 28 (28) | 23 (60) | 229 | 7 | 3 · 92 |
| `one-root-by-lifetime.ko.md` | 700 | 63,111 | 33 · 25 | 42 · 9 | 183 | 44,172 | 6 (6) | 30 (39) | 0 | 0 | 2 · 16 |
| `review-handoff-protocol.md` | 859 | 55,638 | 22 · 24 | 42 · 11 | 355 | 27,174 | 11 (12) | 25 (81) | 143 | 5 | 7 · 32 |
| `the-evidence-ledger.md` | 714 | 52,159 | 4 · 2 | 46 · 24 | 70 | 25,962 | 53 (53) | 25 (116) | 104 | 7 | 22 · 130 |
| `one-root-by-lifetime.md` | 728 | 52,013 | 39 · 33 | 42 · 9 | 198 | 36,241 | 6 (6) | 32 (53) | 12 | 5 | 3 · 16 |
| `commit-review-gate-spec.md` | 633 | 44,198 | 15 · 19 | 23 · 8 | 298 | 16,621 | 22 (26) | 15 (39) | 42 | 4 | 13 · 268 |
| `the-pact.md` | 410 | 34,343 | 0 · 0 | 22 · 19 | 15 | 13,998 | 14 (18) | 8 (29) | 79 | 6 | 4 · 36 |
| `release-checklist.md` | 451 | 27,564 | 11 · 9 | 12 · 5 | 223 | 10,606 | 34 (36) | 31 (62) | 2 | 3 | 8 · 50 |
| `branch-and-release.md` | 442 | 27,016 | 11 · 9 | 28 · 10 | 113 | 14,302 | 13 (13) | 17 (64) | 5 | 3 | 3 · 36 |
| `issues-and-milestones.md` | 407 | 25,081 | 8 · 7 | 26 · 8 | 113 | 12,447 | 14 (14) | 15 (42) | 2 | 3 | 1 · 4 |
| `the-commit-gate-inside-git.md` | 271 | 23,228 | 8 · 0 | 17 · 11 | 11 | 9,503 | 10 (12) | 11 (19) | 22 | 2 | 2 · 26 |
| `the-record-layout.md` | 335 | 22,593 | 11 · 11 | 14 · 5 | 109 | 13,991 | 15 (19) | 34 (48) | 0 | 9 | 6 · 68 |
| `the-broad-gate.md` | 256 | 18,297 | 0 · 0 | 17 · 10 | 11 | 10,226 | 10 (10) | 5 (27) | 50 | 1 | 12 · 98 |
| `the-review-and-parity-arms.md` | 261 | 17,440 | 3 · 7 | 9 · 2 | 114 | 8,249 | 5 (7) | 21 (35) | 22 | 2 | 1 · 8 |
| `the-reader-registry.md` | 180 | 12,907 | 2 · 2 | 8 · 3 | 66 | 5,116 | 1 (1) | 2 (2) | 0 | 1 | 3 · 72 |
| `measuring-a-run.md` | 135 | 9,440 | 2 · 3 | 10 · 4 | 16 | 6,109 | 0 | 20 (20) | 46 | 0 | 1 · 2 |
| `the-agent-set.md` | 131 | 8,712 | 0 · 0 | 11 · 3 | 21 | 5,624 | 0 | 5 (7) | 70 | 0 | 3 · 10 |
| **19 files** | 9,911 | 708,070 | 250 · 232 | | | 380,594 | 348 (391) | — (905) | | 73 | |

Three readings of it. The marks find 250 history lines; the paragraphs that open with no rule hold 2,915 lines, and `worktree-guard-spec.md` alone has 463 of them against 309 rule lines — the narrative the check cannot name is twelve times what it can. The ledger's 391 anchors are heading paths except five quoted lines, so a rewrite that keeps every heading drifts rows and breaks almost none. Who sends an agent to a doc: `review-chain-spec`, `review-handoff-protocol` and `round-record-spec` are cited by `agents/warden.md`, `agents/smith.md`, `skills/code-review/*` and `skills/implement/SKILL.md`; `the-evidence-ledger` and `the-record-layout` by the implement, evidence-check and settle skills; `commit-review-gate-spec` and `the-commit-gate-inside-git` by the contract's §9; `the-pact` by evidence-check and the orchestration file; `worktree-guard-spec` and `one-root-by-lifetime` by one orchestration or settle sentence each; the other eight by no agent definition or skill — hooks, tests and the release procedure read them.

## Targets

The bar each phase is held to; the `bytes:` ceiling written is the value the rewrite reaches under it. The basis is the kept-shape estimate (headings, fences, tables, the first paragraph under each heading and each bold-led paragraph capped at 8 lines) rounded up, which is #923's preliminary bar for every file it named.

| File | Bytes → target | Lines → at most | Basis |
|---|---|---|---|
| `worktree-guard-spec.md` | 74,355 → 35,000 | 999 → 600 | kept 33,259; 463 narrative lines go, 16 long rules split |
| `review-chain-spec.md` | 70,140 → 45,000 | 999 → 600 | kept 43,041; 203 shared runs become links |
| `round-record-spec.md` | 69,835 → 45,000 | 1,000 → 600 | kept 43,953 |
| `review-handoff-protocol.md` | 55,638 → 28,000 | 859 → 450 | kept 27,174; four history sections go whole |
| `the-evidence-ledger.md` | 52,159 → 27,000 | 714 → 450 | kept 25,962; the work is inside 24 rules over 8 lines |
| `one-root-by-lifetime.md` · `.ko.md` | 52,013 → 22,000 · 63,111 → 27,000 | 728 · 700 → 350 each | the sections that still rule hold 28,406 B today (opt-in 2,578 · first setup 9,045 · dependency rule 3,756 · tree 3,701 · release 2,223 · naming 2,208 · what the repository decides 4,895); 13 sections are history (24,598 B); the Korean edition runs 1.21× the English |
| `commit-review-gate-spec.md` | 44,198 → 17,000 | 633 → 300 | kept 16,621 |
| `the-pact.md` | 34,343 → 15,000 | 410 → 250 | kept 13,998; 19 of 22 rules over 8 lines |
| `branch-and-release.md` | 27,016 → 15,000 | 442 → 250 | kept 14,302 |
| `release-checklist.md` | 27,564 → 11,000 | 451 → 200 | kept 10,606; the steps are fences |
| `issues-and-milestones.md` | 25,081 → 13,000 | 407 → 220 | kept 12,447 |
| `the-commit-gate-inside-git.md` | 23,228 → 10,000 | 271 → 150 | kept 9,503 |
| `the-record-layout.md` | 22,593 → 14,000 | 335 → 220 | kept 13,991; §*What is decided and not built yet* goes |
| `the-broad-gate.md` | 18,297 → 11,000 | 256 → 160 | kept 10,226 |
| `the-review-and-parity-arms.md` | 17,440 → 9,000 | 261 → 140 | kept 8,249 |
| `the-reader-registry.md` | 12,907 → 6,000 | 180 → 90 | kept 5,116; the two census sections go |
| `measuring-a-run.md` | 9,440 → 6,500 | 135 → 90 | kept 6,109 |
| `the-agent-set.md` | 8,712 → 6,000 | 131 → 90 | kept 5,624 |
| **total** | 708,070 → 362,500 (51 %) | 9,911 → ≤ 5,360 | `history:<every docs file>` 0 |

## Scope

**In.** The 19 files rewritten to #923's shape, one file or one cluster per phase (`plan.md`). For each: every released row anchored on it read and answered in `seal/ledger/1791934661-every-doc-states-the-current-rule-only.md`; every test literal it pins green on the new sentence or removed with a row; every `§*…*` citation into it from outside resolving (headings kept; a heading that is itself history goes with its section and every citing file is edited in the same phase); the `BASELINE` entries it drains lowered; its `history:` row to 0 and its `bytes:` row to what it reached (#930's `docs-history:` row to 0 where #923's phase 1 has not merged yet); a rule census per file in `phases/phase-N.md` naming each bold-led rule's new coordinate or `## Removes` row with `Exercised by: <case>/<grader>` or `not exercisable — <why>`; an eval record for each phase whose files an agent case opens (§*Which case reaches which doc*). The `one-root-by-lifetime` pair rewritten to what still rules, both editions in one phase, and `docs/the-record-layout.md` §*docs/*'s row for it rewritten. The five policy-preamble copies (#755 cluster e: `measuring-a-run`, `the-agent-set`, `the-broad-gate`, `the-evidence-ledger`, `the-pact`, 11–15 runs per pair) become one sentence naming `skills/implement/SKILL.md` §1.

**Out, and whose.** The check, the harness, the baseline and the record test: #923 phases 1–2, which this item waits on (`plan.md` §*Dependency*). Every file outside `docs/`: `skills/`, `templates/`, `CONTRIBUTING.md`, `CLAUDE.md` are #940; `agents/` and the preloaded skills are #923; `README.md`'s links into `docs/` headings must still resolve, and the README is otherwise nobody's in 0.22.0. `docs/experiments/`: dated records, no policy, excluded by `docs/the-record-layout.md` §*docs/*. Renaming any `docs/` file: 18 test, 8 skill and 4 hook references name `one-root-by-lifetime.md`, and a new name buys no reader anything. A test module that asserts on no `docs/` text: #929 and #942, by #923's boundary. Which `.ko.md` sentences say what the English says: `test_both_editions_carry_the_same_folds.py` holds outline, markers and `Enforced by:` targets, and this item adds no sentence-level mirror check.

## Which case reaches which doc

A `docs/` file is read on demand, so #923's suite exercises it only where a case's agent is sent there. From the citations above: the warden's replay, seeded and rule cases reach `review-chain-spec`, `review-handoff-protocol` and `round-record-spec`; the smith's rule cases reach `review-handoff-protocol`, `the-evidence-ledger`, `the-record-layout` (the fragment, the phase record), and `commit-review-gate-spec` with `the-commit-gate-inside-git` through the contract's §9 (the heredoc and `Edit` graders); the sealer's cases reach `the-broad-gate` where `skills/broad-gate` sends it there. The other ten files no agent case opens: `worktree-guard-spec`, the release trio, `the-review-and-parity-arms`, `the-pact`, `the-reader-registry`, `measuring-a-run`, `the-agent-set`, and the one-root pair. Their census rows read `not exercisable — no agent case opens this file; held by <the test node ids that pin or enforce it>`, and the rule's loss is caught by that test going red or by the ledger row that anchors it. Where a run of a suite that should reach a file never opened it, the record says so and the rows fall back to the same form (Q3).

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 one doc at its target | phase 1 closes on `docs/worktree-guard-spec.md` | ≤ 35,000 B and ≤ 600 lines (`wc -lc`); `history:` (or `docs-history:`) 0 and `bytes:` at the reached value, checker exit 0; before and after in `phases/phase-1.md` from `measure.py` |
| S2 every released row answered | any phase | `git diff --stat origin/release/v0.22.0 -- seal/releases seal/ledger.md` empty; for each row the file anchored (79 in phase 1) one `Re-read ·` or `Corrected ·` row in the fragment dated the day it was read; `evidence-check` exit 0; the phase record lists the rows corrected and why |
| S3 every pin answered | any phase | each module in the file's pin list green on a narrow run; a dropped literal is an `overview.md` divergence row naming module and literal; a re-pointed pin seen red on the old sentence first |
| S4 every link resolves | any phase | `measure.py`'s citation pass finds every `§*…*` into the file resolving; `grep -rn 'docs/<file>' agents skills templates hooks .github tests docs README*.md CLAUDE.md CONTRIBUTING.md` names no heading that is gone |
| S5 the census is complete | any phase | every bold-led rule of the old file → new coordinate or `## Removes` row, each `Exercised by:` or `not exercisable — <why>`; #923's record test refuses a row with neither |
| S6 an eval record where a case reaches the file | phases 2–5, 7, 9 | `seal/specs/<id>/evals/<agent>-phase-N.md` with `Verdict: pass`, written by #923's comparator; the record test green |
| S7 the pairs drained | phases 2–5, 7, 9 | `BASELINE` lowered for each pair whose count fell, same commit; the case green |
| S8 the one-root pair | phase 6 | both editions one outline and one marker multiset (`test_both_editions_carry_the_same_folds.py` green); the three dated-section cases of `test_settle_reads_before_it_removes.py` removed with rows; `DESIGN_RECORD` and `RECORDS_OF_A_MOMENT` entries removed where the pair no longer names an old root or a running version, or kept with the reason; the index row rewritten |
| S9 the owners' sentences stand | phases 2–5, 8, 9 | `test_the_rules_have_one_owner.py`, `test_the_ledger_rules_have_one_home.py`, `test_the_rules_claude_md_names_have_one_home.py` green |
| S10 room for the fold | every phase | `fold-check --ceiling 1000` exit 0; `Over the ceiling` stays `none`; no doc over its line target |
| S11 no prompt, no CI | the whole item | no new job, step, dependency or question; the eval runs are the orchestrator's, as #923 states |

## Data & interfaces

Files edited: `docs/*.md` (19); `seal/budgets.md` rows lowered; the pin modules named per phase in `plan.md`; `tests/test_no_passage_is_pasted_into_a_second_file.py#BASELINE`. Written: `seal/ledger/1791934661-every-doc-states-the-current-rule-only.md`; `phases/phase-N.md` with the census and the before/after table; `evals/<agent>-phase-N.md` through #923's comparator; `changelog.md`; `overview.md`. No script, hook or test of this item's own.

## Removes

| Removes | Coordinate | Where it lands, or why it can go |
|---|---|---|
| the 0.4.0 design narrative | `docs/one-root-by-lifetime.md#"## The problem, as measured"`, `#"## What happens to the existing directories at the switch"`, `#"## What it touches in this repository"`, `#"## What does not change"`, `#"## Order"`, `#"## Out of scope"`, `#"## Decided after the thread"`, `#"## Decisions left open"` | #74 and its comments; the released ledger rows of 1788331011 |
| the four dated decision sections | `docs/one-root-by-lifetime.md#"## Decided when \`settle\` was built (2026-09-22)"`, `#"## Decided when the fold stopped being a work item (2026-09-23)"`, `#"## Decided when a joined project's \`specs/\` was read and never taken (2026-10-01)"`, `#"## Decided when the process record stopped waiting for the fold (2026-10-04)"` | #458, #517, #729, #688 and their work items' records at their release tags; each rule they carry with an `Enforced by:` line moves into the section that owns its subject |
| the same thirteen sections of the Korean edition | `docs/one-root-by-lifetime.ko.md#"## 문제를 숫자로 보면"` through `#"## 과정의 기록이 fold 를 기다리지 않게 되면서 정해진 것 (2026-10-04)"` | as above; the mirror moves with the English (`CONTRIBUTING.md` §*House rules*) |
| the three cases pinning the dated sections | `tests/test_settle_reads_before_it_removes.py#test_the_design_record_takes_the_later_decision_as_a_dated_section`, `#test_the_design_record_takes_d1_as_a_dated_section`, `#test_both_editions_took_the_same_decisions` | they pin "a record of a moment is not rewritten", which the owner's answer to #923 Q1 reverses; the mirror is `tests/test_both_editions_carry_the_same_folds.py` |
| the spawn-prompt history | `docs/review-handoff-protocol.md#"## What every spawn prompt used to carry"`, `#"## Problem"`, `#"## Status"`, `#"## Layout">"### Why the records moved a second time"` | #265, #292 and `docs/the-agent-set.md` §*One contract every agent receives*; the rule that records stay through the merge keeps its section |
| the built-and-closed decisions | `docs/the-record-layout.md#"## What is decided and not built yet"` | #727, #728, #729, #730 are built; F3's rules move to §*seal/specs/<work-item-id>/*, F4's homes are already `CLAUDE.md`'s |
| the landing census | `docs/the-reader-registry.md#"## The census: the units that stood undeclared at landing"`, `#"## The counts at landing"` | work item 1791384152's records at the 0.20.0 tag |
| the policy-preamble copies | `docs/measuring-a-run.md#"It is a policy document: it outranks the SDD set, and a work item that finds"`, and the same quoted line in `docs/the-agent-set.md`, `docs/the-broad-gate.md`, `docs/the-evidence-ledger.md`, `docs/the-pact.md` | one sentence each naming `skills/implement/SKILL.md` §1 (#755 cluster e) |

Sentence-level removals inside a rewritten section are the rewrite itself: `survivor-check` reads every sentence a range removed and refuses one still standing elsewhere, the census names each rule's new coordinate, and a pin dropped with its sentence is an `overview.md` divergence row. Released rows anchored on a heading named above — 6 on `the-record-layout` §*What is decided and not built yet*, 2 on `review-handoff-protocol`'s spawn-prompt subsections, 1 each on the pair's *Decided after the thread* and *Decided when a joined project's `specs/`* sections in both editions — are `Corrected ·` onto the section that holds the claim now, one row each.

## Open questions → questions.md

Framed 2026-10-14 by framer, before the build.
