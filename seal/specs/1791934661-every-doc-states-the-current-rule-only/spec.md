# Feature Specification: every doc states the current rule only

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Part C of #923. The shape, the check and the non-inferiority proof are #923's frame (`seal/specs/1791933022-every-agent-skill-and-doc-states-the-current-rule-only/spec.md`) and are applied, never redesigned. Revised in place on 2026-10-14 by the framer, after phases 1, 6 and 8 were built, under the owner's rule of that day:

**The source of truth for a rule is one place, the test that holds it.** A doc holds a rule only where an agent that is not editing the component would decide wrongly without the sentence — what the component decides (the matrix), when it asks, its known limits, and the promises other components rely on — and each such rule ends with `Enforced by:`. Every other rule's home is the first sentence of the docstring of the test that holds it, or the code's docstring: internal mechanics, heuristics and parsing edge cases go this way, and a rule with no test gets one before it moves. The whole picture is `bin/rules <doc>` (#944 phase 1, NAME NOT IN TREE), which expands each section's `Enforced by:` targets to their docstrings on stdout; nothing is generated into the tree. Phases 1, 6 and 8 kept every rule in the doc beside its test (501, 316 + 313, 249 + 206 + 207 lines), which is two homes that can contradict each other; phase 10 brings them under the criterion.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Nothing here asks a person; a rewrite is proved by #923's suite where an agent case opens the file, and by the census and the tests that hold each rule where none does |
| `CONTRIBUTING.md` §*What a change to a gate must carry*, §*House rules* | No gate is added; a re-pointed pin is seen red first (contract §15); the one-root pair's two editions move together (`tests/test_both_editions_carry_the_same_folds.py`) |
| `docs/the-record-layout.md` §*The size a reader takes whole*, §*docs/*, §*A change writes fragments, never a shared file* | ≤ 1,000 lines and 64 KB per file; the index rows for the pair and for the deleted ledger document are rewritten; the changelog goes to this item's fragment |
| #944 (`seal/specs/1791940762-the-record-of-truth-is-tests-not-coordinates/spec.md` §*The replacement*, §*Effect on the other 0.22.0 items*) | The released ledger files retire: no `Re-read ·` or `Corrected ·` row is owed by any phase, headings are no longer bound by anchors, the survivor sweep is gone, and `docs/the-evidence-ledger.md` is a deletion whose still-ruling statements move to their homes |
| `docs/the-reader-registry.md` §*A frame names what its work removes* | `## Removes` below |
| `skills/settle/SKILL.md` §2, `tests/test_a_document_has_room_for_the_next_fold.py` | A `docs/` file is a fold target: fold markers and their `Enforced by:` lines move whole with their statement, and a rewritten file leaves room under the ceiling |
| `tests/test_the_rules_have_one_owner.py`, `tests/test_the_rules_claude_md_names_have_one_home.py` | Nine review-chain rules and four `CLAUDE.md` rules each have one owning sentence; a rewrite keeps the owner's sentence where the criterion keeps the rule in the doc, and re-points the pin to the rule's new home where it moves, in the same commit |
| `tests/test_no_passage_is_pasted_into_a_second_file.py` (`BASELINE`) | A pair this work drains lowers its entry in the same commit; two branches lowering one entry re-measure at the merge |
| `skills/implement/SKILL.md` §3 | A `docs/` file is text an agent reads and acts on when a skill sends it there: the top rung |

## The problem, measured

`executed` at 92cc85dd (`wc -lc docs/*.md`; `scratchpad/941/measure.py`, output `measure.txt`: #930's `budget_check.classify` at 661dc60b and the same classifier with #923's widened marks, bold-led paragraphs, test literals ≥ 25 characters found verbatim, `BASELINE` runs, `§*…*` citations from outside; opens are `Read` calls on the path over 530 transcript files of 16 sessions, confounded by work items that edited the file's subject). Ledger anchors were measured too (348 rows, 391 anchors, 386 on headings) and are now nobody's: #944 retires them.

| File | Lines | Bytes | History #930 · widened | Bold paras · > 8 lines | Non-bold para lines | Kept est. B | Pin modules (literals) | `BASELINE` runs | § cited from outside | Opened |
|---|---|---|---|---|---|---|---|---|---|---|
| `worktree-guard-spec.md` | 999 | 74,355 | 39 · 36 | 50 · 16 | 463 | 33,259 | 9 (52) | 1 | 4 | 23 · 486 |
| `review-chain-spec.md` | 999 | 70,140 | 25 · 27 | 65 · 22 | 246 | 43,041 | 37 (110) | 203 | 10 | 13 · 76 |
| `round-record-spec.md` | 1,000 | 69,835 | 17 · 18 | 60 · 24 | 290 | 43,953 | 23 (60) | 229 | 7 | 3 · 92 |
| `one-root-by-lifetime.ko.md` | 700 | 63,111 | 33 · 25 | 42 · 9 | 183 | 44,172 | 30 (39) | 0 | 0 | 2 · 16 |
| `review-handoff-protocol.md` | 859 | 55,638 | 22 · 24 | 42 · 11 | 355 | 27,174 | 25 (81) | 143 | 5 | 7 · 32 |
| `the-evidence-ledger.md` | 714 | 52,159 | 4 · 2 | 46 · 24 | 70 | 25,962 | 25 (116) | 104 | 7 | 22 · 130 |
| `one-root-by-lifetime.md` | 728 | 52,013 | 39 · 33 | 42 · 9 | 198 | 36,241 | 32 (53) | 12 | 5 | 3 · 16 |
| `commit-review-gate-spec.md` | 633 | 44,198 | 15 · 19 | 23 · 8 | 298 | 16,621 | 15 (39) | 42 | 4 | 13 · 268 |
| `the-pact.md` | 410 | 34,343 | 0 · 0 | 22 · 19 | 15 | 13,998 | 8 (29) | 79 | 6 | 4 · 36 |
| `release-checklist.md` | 451 | 27,564 | 11 · 9 | 12 · 5 | 223 | 10,606 | 31 (62) | 2 | 3 | 8 · 50 |
| `branch-and-release.md` | 442 | 27,016 | 11 · 9 | 28 · 10 | 113 | 14,302 | 17 (64) | 5 | 3 | 3 · 36 |
| `issues-and-milestones.md` | 407 | 25,081 | 8 · 7 | 26 · 8 | 113 | 12,447 | 15 (42) | 2 | 3 | 1 · 4 |
| `the-commit-gate-inside-git.md` | 271 | 23,228 | 8 · 0 | 17 · 11 | 11 | 9,503 | 11 (19) | 22 | 2 | 2 · 26 |
| `the-record-layout.md` | 335 | 22,593 | 11 · 11 | 14 · 5 | 109 | 13,991 | 34 (48) | 0 | 9 | 6 · 68 |
| `the-broad-gate.md` | 256 | 18,297 | 0 · 0 | 17 · 10 | 11 | 10,226 | 5 (27) | 50 | 1 | 12 · 98 |
| `the-review-and-parity-arms.md` | 261 | 17,440 | 3 · 7 | 9 · 2 | 114 | 8,249 | 21 (35) | 22 | 2 | 1 · 8 |
| `the-reader-registry.md` | 180 | 12,907 | 2 · 2 | 8 · 3 | 66 | 5,116 | 2 (2) | 0 | 1 | 3 · 72 |
| `measuring-a-run.md` | 135 | 9,440 | 2 · 3 | 10 · 4 | 16 | 6,109 | 20 (20) | 46 | 0 | 1 · 2 |
| `the-agent-set.md` | 131 | 8,712 | 0 · 0 | 11 · 3 | 21 | 5,624 | 5 (7) | 70 | 0 | 3 · 10 |
| **19 files** | 9,911 | 708,070 | 250 · 232 | | 2,915 | 380,594 | — (905) | | 73 | |

**After phases 1, 6 and 8** (`executed`, `wc -lc` at 359fed2f; the phase records hold the rest): `worktree-guard-spec` 501 lines · 34,973 B, `one-root-by-lifetime` 316 · 19,422 and `.ko` 313 · 23,684, `branch-and-release` 249 · 14,508, `release-checklist` 206 · 10,992, `issues-and-milestones` 207 · 11,903; `docs/` 7,976 lines · 554,452 B. Every rule was kept in the doc: phase 1's census has 50 rules kept and 0 moved.

**The criterion, measured on phase 1's file** (`executed`, `awk` over `docs/worktree-guard-spec.md` at 359fed2f, section by section). Sections the criterion keeps whole — *Premise*, the *Decision matrix* heading, §*B. Worktree creation*, *Declared work streams*, the *Activity* definition, *What a blocking prompt must show*, *Unknowns resolve conservatively*, *Known limits* — are 148 lines · 8,232 B. Sections it keeps in part are 335 lines · 27,000 B today: §*A. Branch switch* (78 · 6,683; the matrix table, the three shape bullets, *Which commands reach these rows* and *The failure direction* stay, ≈ 40 lines), the Agent-path subsection (14 · 799; one promise stays), *Creation consent* (115 · 8,398; the first-creation question, the routing answer as the second consent, *A `routing.md` is not read*, *What does not change* and *The prompt budget* stay, ≈ 30 lines; the five read rules, the record's five bullets, the segment class, the ladder and the walk move), *Decided before git runs* (18 · 1,631; one promise stays), *Choice sites* (63 · 5,399; *Once per session per direction*, the press rule and the bare-word token rule stay, ≈ 22 lines; the token-reading order and what the token cannot reach move), *Which tree* (53 · 3,362; *The tree judged is the one the command acts on* and *A broken reader costs a stop, never a silence* stay, ≈ 14 lines; the frozen reading moves), *Passive-event filtering* (7 · 290; moves). The sum is **≈ 265 lines · ≈ 17,700 B**, with *Known limits* carried whole at 81 lines; that is the bar phase 10 is held to, and what it reaches is the ceiling written.

## Targets

Two kinds of number. Phase 1's partition above is **measured**; every other file's bar is **derived** from it (the criterion kept 51 % of the compact file's bytes) applied to the kept-shape estimate of the unbuilt files and to the measured size of the built ones, and each phase's first act is to partition its own file the same way and record the sum before it rewrites. The ceiling written to `seal/budgets.md` is what the rewrite reached.

| File | Now → bar | Lines → at most | Basis |
|---|---|---|---|
| `worktree-guard-spec.md` | 34,973 → 18,000 | 501 → 270 | measured partition above; *Known limits* whole |
| `review-chain-spec.md` | 70,140 → 22,000 | 999 → 320 | 51 % of kept 43,041; the cycle, the bound, the two records and what each says, the floor stay; the fix table's arithmetic and the generator's refusals move to `round_record.py` and its tests |
| `round-record-spec.md` | 69,835 → 22,000 | 1,000 → 320 | 51 % of kept 43,953; the row vocabulary a person writes and the generator refuses stays; the derivation arithmetic moves |
| `review-handoff-protocol.md` | 55,638 → 14,000 | 859 → 220 | 51 % of kept 27,174; the layout and the handoff before round 1 stay |
| `the-evidence-ledger.md` | 52,159 → 0 | 714 → 0 | deleted; ≈ 8 KB of still-ruling statements (the fold, the live-line rule, the unverified baseline) move to `docs/the-record-layout.md`, `skills/settle/SKILL.md` and the docstrings of `unverified_check.py#live_lines` and the tests that hold them |
| `one-root-by-lifetime.md` · `.ko.md` | 19,422 → 10,000 · 23,684 → 12,500 | 316 · 313 → 170 each | 51 % of the built file; the opt-in signal, first setup's question, the modes' promises and the dependency rule stay; the mode-table mechanics and the import/export edge cases move |
| `commit-review-gate-spec.md` | 44,198 → 8,500 | 633 → 140 | 51 % of kept 16,621; registration, what the reading decides where git cannot, the deny shapes stay; the heredoc grammar's slots move to `commit-review-gate.py` and `test_edits_go_through_the_edit_tool.py` |
| `the-commit-gate-inside-git.md` | 23,228 → 5,000 | 271 → 80 | 51 % of kept 9,503; what git decides, the limits, the state table stay |
| `the-review-and-parity-arms.md` | 17,440 → 4,500 | 261 → 75 | 51 % of kept 8,249 |
| `the-pact.md` | 34,343 → 7,000 | 410 → 120 | 51 % of kept 13,998; the anchor grammar moves to `pact_check.py` |
| `the-broad-gate.md` | 18,297 → 5,500 | 256 → 90 | 51 % of kept 10,226; one act one owner, the list rule, the stamp's place stay |
| `the-record-layout.md` | 22,593 → 10,000 | 335 → 160 | 51 % of kept 13,991 plus the ledger statements that land here |
| `the-reader-registry.md` | 12,907 → 3,000 | 180 → 50 | 51 % of kept 5,116; the four classes and the `## Removes` grammar stay |
| `measuring-a-run.md` | 9,440 → 3,500 | 135 → 55 | 51 % of kept 6,109 |
| `the-agent-set.md` | 8,712 → 3,000 | 131 → 50 | 51 % of kept 5,624 |
| `branch-and-release.md` | 14,508 → 7,500 | 249 → 130 | 51 % of the built file; the merge table and the release acts stay |
| `release-checklist.md` | 10,992 → 9,000 | 206 → 180 | the steps are what a person types, so nearly all of it is contract; only the reasons beside boxes move |
| `issues-and-milestones.md` | 11,903 → 6,000 | 207 → 110 | 51 % of the built file; what each field means and what reads it stay |
| **total** | 708,070 → 171,000 (24 %) | 9,911 → ≤ 2,700 | `history:<every docs file>` 0 |

## Scope

**In.** The 19 files under the criterion, one file or one coupled cluster per phase (`plan.md`); `docs/the-evidence-ledger.md` deleted and its still-ruling statements moved. For each file: a partition pass first (every bold-led rule → *contract* or *mechanics*, with the test or unit that holds it), then the rewrite; every rule that stays ends with `Enforced by:`; every rule that moves becomes the first sentence of its test's docstring (or the code unit's), and a rule with no test gets one, seen red, before it moves; every test literal green on its new sentence or dropped with a row; every `§*…*` citation into the file resolving, the citing file edited in the same phase where a heading goes; the `BASELINE` entries it drains lowered; `history:` to 0 and `bytes:` to what it reached at the rebase onto #923 phase 1; a census in `phases/phase-N.md` mapping every old rule to a doc coordinate, a test name, a code unit or a `## Removes` row, each `Exercised by: <case>/<grader>` or `not exercisable — <why>`; an eval record where an agent case opens the file (§*Which case reaches which doc*). Phase 10 is the second pass over phases 1, 6 and 8's five files, so their pins are touched once more and not twice.

**Out, and whose.** `bin/rules`, the resolution gate (`enforced-unresolved`), the `unenforced` ratchet, the ledger's deletion and the survivor sweep's: #944. The check, the harness, the baseline and the record test: #923 phases 1–2. Every file outside `docs/`: #940 and #923, except a test docstring or code docstring that becomes a moved rule's home, which this item writes in the phase that moves the rule. `README.md`'s links into `docs/` headings must still resolve. `docs/experiments/`: no policy. Renaming any `docs/` file. A sentence-level mirror check for `.ko.md`. Released ledger rows: nobody's, retired by #944; phase 1's reading of its 19 family roots stands in `phases/phase-1.md` as a record.

## Which case reaches which doc

A `docs/` file is read on demand, so #923's suite exercises it only where a case's agent is sent there. The warden's cases reach `review-chain-spec`, `review-handoff-protocol` and `round-record-spec`; the smith's reach `review-handoff-protocol`, `the-record-layout`, and `commit-review-gate-spec` with `the-commit-gate-inside-git` through the contract's §9; the sealer's reach `the-broad-gate`. The other eleven files no agent case opens: their census rows read `not exercisable — no agent case opens this file; held by <test node ids>`, and a moved rule's row names the test whose docstring is its home. Where a run of a suite that should reach a file never opened it, the record says so and the rows take the same form (Q3). The owner set the cadence on 2026-10-14: each phase runs the behaviour cases mapped to the rules it changed, and each agent's full suite runs once at the item's end.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a file at its bar | a phase closes | bytes and lines at or under the bar (`wc -lc`), or the phase record says what the partition measured and why the bar moved; `history:` 0 and `bytes:` at the reached value once rebased; `measure.py` before and after in the phase record |
| S2 one home per rule | any phase | every bold-led rule of the old file is in the census exactly once with one home; a rule kept in the doc ends with `Enforced by:` naming a target that resolves, or `nothing — <why>`; a rule moved to a test is the first sentence of that test's docstring (`grep -n` of the sentence finds the test and no doc) |
| S3 the partition is recorded first | any phase | the phase record's census carries a *contract* or *mechanics* verdict per old rule with the question answered (*would an agent not editing this component decide wrongly without it?*), written before the rewrite's first commit |
| S4 a moved rule has a test | a rule with no test moves | the test exists, was seen red on the mutation that breaks the rule (contract §15), and its docstring opens with the rule |
| S5 every pin answered | any phase | each module in the file's pin list green narrow; a re-pointed pin seen red first; a dropped literal an `overview.md` divergence row |
| S6 every link resolves | any phase | `measure.py`'s citation pass finds every `§*…*` into the file resolving; `grep -rn 'docs/<file>'` names no heading that is gone |
| S7 an eval record where a case reaches the file | phases 2–4, 7, 9 | `evals/<agent>-phase-N.md` with `Verdict: pass`, written by #923's comparator; the full suites once at the end |
| S8 the pairs drained | phases 2–4, 7, 9 | `BASELINE` lowered for each pair whose count fell, same commit; the case green |
| S9 the ledger document is gone and its rules are not | phase 5 | `docs/the-evidence-ledger.md` absent; `grep -rn 'the-evidence-ledger'` over the tree names only `changelog/`; every statement whose `Enforced by:` target survives #944 stands at its new home with its marker; `fold-check` exit 0; `test_a_document_has_room_for_the_next_fold.py` green |
| S10 the owners' sentences stand or move with their pins | phases 2–4, 9, 10 | `test_the_rules_have_one_owner.py`, `test_the_rules_claude_md_names_have_one_home.py` green |
| S11 room for the fold | every phase | `fold-check --ceiling 1000` exit 0; `Over the ceiling` `none` |
| S12 `bin/rules` shows the whole | once #944 phase 1 lands | `bin/rules docs/<file>` prints each section's rules with their tests' docstrings; a rule moved by this item appears there and in no doc |
| S13 no prompt, no CI | the whole item | no new job, step, dependency or question |

## Data & interfaces

Files edited: `docs/*.md` (18 rewritten, 1 deleted); `seal/budgets.md` rows lowered at the rebase; test modules named per phase (docstrings gain a first sentence; pins re-pointed; new cases where a moved rule had none); code docstrings where a mechanics rule's home is the unit; `tests/test_no_passage_is_pasted_into_a_second_file.py#BASELINE`. Written: `phases/phase-N.md` with the partition and the census; `evals/<agent>-phase-N.md`; `changelog.md`; `overview.md`. No script, hook or checker of this item's own.

## Removes

| Removes | Coordinate | Where it lands, or why it can go |
|---|---|---|
| the ledger's policy document | `docs/the-evidence-ledger.md#"# The evidence ledger — what a row claims, and what reads it"` | #944 retires what it describes; the fold and live-line statements move to `docs/the-record-layout.md` and `skills/settle/SKILL.md`, the unverified baseline to `docs/the-record-layout.md`, the reader rules to `skills/verify/scripts/unverified_check.py#live_lines` and the tests that hold them |
| the ledger homes' pin | `tests/test_the_ledger_rules_have_one_home.py` | its four homes are in the deleted document; the fragment rule's home stays in `docs/the-record-layout.md` and `test_the_rules_claude_md_names_have_one_home.py`'s shape holds it |
| the guard's reading mechanics | `docs/worktree-guard-spec.md#"## Activity: what makes a session ACTIVE (heuristics, for sessions without a lease)">"### Passive-event filtering"`, `#"## Creation consent — the first creation is the question, not every one">"**What exactly is read**; every way of failing it is *no consent*:"`, `#"## Choice sites">"**Where the token is read from.** The command, and only the command. Not"` | the docstrings of `tests/test_worktree_guard_signals.py`, `tests/test_the_guard_asks_once_per_session.py` and `tests/test_worktree_guard.py` cases that hold each, named in phase 10's census |
| the 0.4.0 design narrative and the four dated sections of the one-root pair, both editions | `docs/one-root-by-lifetime.md#"## The problem, as measured"` … `#"## Decided when the process record stopped waiting for the fold (2026-10-04)"`, and the Korean twins | removed in phase 6 (`phases/phase-6.md`); #74, #458, #517, #688, #729 |
| the three cases pinning the dated sections | `tests/test_settle_reads_before_it_removes.py#test_the_design_record_takes_the_later_decision_as_a_dated_section`, `#test_the_design_record_takes_d1_as_a_dated_section`, `#test_both_editions_took_the_same_decisions` | removed in phase 6; the mirror is `tests/test_both_editions_carry_the_same_folds.py` |
| the spawn-prompt history | `docs/review-handoff-protocol.md#"## What every spawn prompt used to carry"`, `#"## Problem"`, `#"## Status"`, `#"## Layout">"### Why the records moved a second time"` | #265, #292, `docs/the-agent-set.md` |
| the built-and-closed decisions | `docs/the-record-layout.md#"## What is decided and not built yet"` | #727–#730 are built; F3's rules move to §*seal/specs/<work-item-id>/* |
| the landing census | `docs/the-reader-registry.md#"## The census: the units that stood undeclared at landing"`, `#"## The counts at landing"` | 1791384152's records at the 0.20.0 tag |
| the policy-preamble copies | `docs/measuring-a-run.md#"It is a policy document: it outranks the SDD set, and a work item that finds"`, and the same quoted line in `docs/the-agent-set.md`, `docs/the-broad-gate.md`, `docs/the-pact.md` | one sentence each naming `skills/implement/SKILL.md` §1 (#755 cluster e); the fifth copy leaves with the ledger document |

Mechanics rules inside every other section leave the docs by the census: each is a row naming the test or unit whose docstring holds it now, read by the warden's stage 1 and by `bin/rules`. No survivor row and no ledger row is written: #944 retired both readers.

## Open questions → questions.md

Framed 2026-10-14 by framer, before the build.
