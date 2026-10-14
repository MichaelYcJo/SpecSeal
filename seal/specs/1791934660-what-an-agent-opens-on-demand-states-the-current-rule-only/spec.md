# Feature Specification: what an agent opens on demand states the current rule only

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Part B of #923. Its frame at 17e69e32 (`seal/specs/1791933022-every-agent-skill-and-doc-states-the-current-rule-only/`) owns the compact-file shape, the check (`bytes:` and `history:` rows, the enforcer gate, `--candidates`, `restated`), the non-inferiority proof (the behaviour suite under `evals/behaviour/`, the baseline, the five pass rules, the record test) and the ledger and pin coupling plan. This file applies them to the files an agent opens during a run and adds only what those files need that the preload set did not: a reader the suite has no agent for, and templates whose content is comments.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Nothing asks a person; every row only lowers; the proof scores itself |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The widened record test and the orchestrator cases are gates: seen red, failure direction stated (they block more), prompt budget zero, `Reads:` lines, this `## Removes` |
| `docs/the-record-layout.md` §*Every kind of record, at a glance*, §*The size a reader takes whole* | One home per rule, the copy is the defect; a file read whole ≤ 1,000 lines and 64 KB, which `skills/verify/SKILL.md` sits over at 1,020 |
| `docs/the-agent-set.md` §*What a spawn costs* | A section marked `Orchestrator:` reaches that role only; the acts table in `skills/implement/orchestration.md` is held by `tests/test_every_orchestrator_act_names_its_delivery.py` against both files, so the two rewrites keep every marked heading and the table's rows |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*, §*A claim held by a test* | 542 released rows anchor into this set; each one an edit drifts gets a `Re-read ·` row in `seal/ledger/1791934660-….md`, each one it breaks a `Corrected ·` row, never in bulk |
| `docs/the-reader-registry.md` §*A frame names what its work removes* | `## Removes` below |
| #923 `spec.md` §*The shape of a compact file*, §*A rule stated twice is caught, in three arms*, §*Non-inferiority, proved per phase*; `plan.md` §*The split* row B | Applied, not redesigned; the targets there for B are re-measured here |
| `skills/implement/SKILL.md` §*3. The SDD file set* | The files are what a session and every agent read and act on: top rung |

## The problem, measured

`executed` 2026-10-14 at 58d545f7 (= `origin/release/v0.22.0` + `routing.md`) with `scratchpad/940/measure.py` and `measure2.py`, which reuse #923's methods; the history classifier is #930's `budget_check.classify` at 661dc60b, and "widened" adds #923's four marks and the list-item opener. Opens are tool calls over 18 sessions' transcripts (17 with any prose read; 513 subagent spawns, kind read off the prompt's head: 152 warden, 94 framer, 90 smith, 87 sealer, 90 unclassified); a `Skill` load counts as an open of its `SKILL.md`; the user's `~/.claude/skills/` copies are excluded.

| File | Bytes | Lines | Hist #930 / widened | Rule paras · >8 lines · narrative lines | Kept estimate cap 8 / cap 5 | Released rows (quoted) | Pin modules / literals | #730 pairs / runs | Opens main/smith/warden/framer/sealer |
|---|---|---|---|---|---|---|---|---|---|
| `CLAUDE.md` | 9,261 | 97 | 0 / 0 | 7 · 0 · 47 | 5,634 / 5,634 | 10 (3) | 17 / 33 | 1 / 14 | 17/50/29/74/64 — and in every spawn's prefix, with the same block again from `~/.claude/CLAUDE.md` |
| `templates/claude-md-block.md` | 4,695 | 17 | 0 / 0 | 5 · 0 · 3 | 4,519 | 0 | 12 / 21 | 1 / 13 | 13/5/4/7/0; its 4 paragraphs are `CLAUDE.md`'s at Jaccard 1.0, by design (`claude_block.py`) |
| `CONTRIBUTING.md` | 23,896 | 397 | 9 / 10 | 27 · 7 · 146 | 13,162 / 10,988 | 60 (10) | 22 / 38 | 1 / 14 | 15/58/58/67/13 |
| `skills/verify/SKILL.md` | 59,722 | 1,020 | 32 / 21 | 57 · 19 · 328 | 32,300 / 25,334 | 74 (1) | 25 / 93 | 7 / 33 | 12/32/24/19/14 |
| `skills/evidence-check/SKILL.md` | 53,733 | 831 | 15 / 15 | 41 · 9 · 210 | 36,039 / 33,462 | 33 (2) | 19 / 46 | 7 / 99 | 5/16/15/22/1 |
| `skills/implement/orchestration.md` | 52,161 | 695 | 13 / 13 | 49 · 10 · 193 | 36,469 / 32,690 | 89 (0) | 37 / 118 | 8 / 37 | 15/20/19/20/15 |
| `skills/code-review/orchestration.md` | 46,760 | 753 | 19 / 23 | 42 · 14 · 251 | 25,717 / 20,960 | 32 (2) | 35 / 133 | 13 / 356 | 16/24/32/39/9 |
| `templates/config.md` | 41,405 | 587 | 4 / 4 | 43 · 5 · 137 | 28,621 / 25,918 | 151 (1) — 89 on `## Broad gate` | 27 / 136 | 2 / 11 | 11/25/22/27/21 |
| `templates/sdd-round.md` | 30,242 | 460 | 9 / 7 | comments 24,678 B | format 5,153 | 5 | 38 / 99 | 7 / 215 | 4/10/12/15/0; generated records carry none of it (32 records, 0 comment bytes) |
| `skills/settle/SKILL.md` | 25,437 | 478 | 1 / 1 | 32 · 7 · 119 | 15,676 / 13,269 | 12 | 11 / 54 | 1 / 14 | 5/6/7/13/0 |
| `skills/commit-pr-convention/SKILL.md` | 10,888 | 229 | 0 / 1 | 24 · 0 · 52 | 8,444 / 8,117 | 17 | 11 / 27 | 1 / 9 | under 10 in the tree's copy |
| `skills/config/SKILL.md` | 10,871 | 180 | 1 / 0 | 19 · 2 · 40 | 8,751 / 7,993 | 15 | 15 / 40 | 4 / 30 | 3/7/5/7/9 |
| `skills/update/SKILL.md` | 9,774 | 185 | 5 / 5 | 11 · 1 · 52 | 6,761 / 6,424 | 8 | 9 / 10 | 1 / 9 | 0 |
| `skills/writing-style/outside-the-review.md` | 7,861 | 110 | 1 / 1 | 19 · 0 · 14 | 6,079 | 0 | 0 | 1 / 3 | 0; the tree's own, not the owner's mirrored canon (`~/.claude/skills/writing-style/` holds `SKILL.md` alone) |
| `templates/seal-README.md` | 7,328 | 119 | 0 | 2 · 1 · 55 | 3,481 / 3,152 | 23, + 6 on `seal/README.md` | 14 / 29 | 1 / 1 | 1/5/4/6/0 |
| `templates/sdd-routing.md` | 6,912 | 114 | 0 | comments 6,339 B | format 386 | 0 | 8 / 19 | 1 / 10 | 14/7/4/13/1; **copied whole into every work item**: 108 `routing.md` in the tree, median 7,081 B, 84 % comment |
| `skills/evidence-ci/SKILL.md` | 5,599 | 107 | 0 / 1 | 11 · 1 · 27 | 4,054 / 3,592 | 1 | 8 / 13 | 0 | 0/6/3/7/0 |
| `templates/sdd-phase.md` | 4,500 | 83 | 3 / 3 | comments 3,554 B | format 456 | 3 (3) | 20 / 27 | 5 / 50 | 6/70/2/51/7 |
| `templates/ledger.md` | 4,263 | 97 | 0 | 3 · 0 · 35 | 1,407 | 1 (1) | 11 / 15 | 3 / 77 | 2/10/4/12/1 |
| `templates/sdd-plan.md` | 3,530 | 79 | 0 / 1 | comments 1,082 B | format 644 | 0 | 2 / 3 | 0 | 10/12/1/60/1 |
| `templates/sdd-spec.md` | 2,951 | 70 | 0 | comments 1,951 B | format 582 | 2 | 4 / 6 | 1 / 8 | 8/16/7/61/1 |
| `templates/sdd-overview.md` | 2,169 | 60 | 0 | comments 1,076 B | format 387 | 0 | 1 / 2 | 1 / 4 | 5/62/3/13/5 |
| `templates/pact.md` · `pact-review.md` · `parity.md` | 2,043 · 1,768 · 1,326 | | 0 | comments 1,837 · 1,598 · 0 | | 3 · 3 (3) · 0 | 1 / 1 each | 1/7 · 1/10 · 0 | ≤ 1 each |
| `templates/sdd-questions.md` | 1,934 | 36 | 1 / 1 | 5 · 0 · 2 | 1,524 | 0 | 1 / 5 | 1 / 4 | 8/13/0/59/1 |
| twelve small skills (`audit`, `build-fix`, `checkpoint`, `confidence-check`, `debug`, `feature-planner`, `gap-analysis`, `learn`, `parity-setup`, `preset-setup`, `security-audit`, `testing`) | 1,565–3,726; 28,961 together | | 1 line in all (`parity-setup`) | 0–7 rules each | | 0 | 0–5 | 0–6 | 0 opens in 513 spawns and 17 sessions |
| **The set: 38 files** | **462,890** | 7,757 | 114 / 107 | 446 rules, 77 over 8 lines, 0 `Enforced by:` | 264,773 | **542** | 984 literals | | |

What the table adds to #923's: the orchestrating session opens `skills/code-review/orchestration.md` in 16 of 17 sessions and `skills/implement/orchestration.md` in 15, and no agent in #923's suite is that reader. `templates/sdd-routing.md`'s comment is the one template body that is instanced — 108 copies, each re-read by the framer and the orchestrator of its work item — while `sdd-round.md`'s 24.7 KB of comment reaches no record and is read as a document 48 times. `CLAUDE.md` is in every prefix twice: the tree's and the user's global copy carry the same block (`~/.claude/CLAUDE.md`, 8,042 B), and `install.sh`/`update` are what carry a compact block there. On-demand prose per spawn over the whole corpus: smith median 296,676 B (max 982,618), framer 310,350 (max 1,292,712), warden 134,716, sealer 9,261 — larger than #923's four-session medians because `Skill` loads are counted here. Restatements inside the set: 3 shared enforcer targets, two the grammar's own `tests/test_x.py` examples (exempt by resolution) and one real, `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` in `skills/implement/SKILL.md` and `skills/implement/orchestration.md`, which #923 phase 1 links; 27 cross-file Jaccard pairs at ≥ 0.35, 10 at ≥ 0.5, of which 4 are the `CLAUDE.md`/block copies and 6 are restatements (§*Scope*). Growth: `skills/verify/SKILL.md` +1,158/−138 over 42 commits, 13 deleting nothing; `skills/code-review/orchestration.md` +1,256/−147 over 47, 16 deleting nothing; `templates/sdd-round.md` +518/−58 over 28, 10 deleting nothing.

## What this set needs that the preload set did not

**A template's content is its comments, and a comment is a rule for the cell it sits in.** The shape for a template: the format kept whole (rows, headings, markers, the fence a generator parses); one comment per cell or section of at most three live lines — what goes in the cell, the vocabulary a checker reads, and the link to the rule's home (`docs/round-record-spec.md`, `skills/implement/orchestration.md` §*how the work is routed*, `docs/the-reader-registry.md`); no story. The `bytes:` row is the ratchet; `history:` reads comment lines as it reads prose, since `classify` reads `unfenced` lines and a `<!-- -->` body is unfenced. `templates/sdd-routing.md` is the one whose saving is paid per work item: every `routing.md` written from it after this lands is the compact one, and the 108 standing copies are records and stay.

**The orchestrator is a reader with no agent, so its files get cases of their own.** `skills/implement/orchestration.md` §*Orchestrator: which of these acts runs itself* already maps every marked act to what notices when it is forgotten. An act with `check:` or `command:` is held by that check — a rewrite that drops its sentence is noticed by the same thing that notices the orchestrator forgetting it, and the census row says `held by: <path>`. The five `still a sentence` acts and the routing act's un-checked half (question 1 alone, before the first edit) get a rule-exercise case each under `evals/behaviour/orchestrator/`: a fixture repository at the state the act starts from, a prompt that says the owner pressed `automation` (a case's session has nobody to ask), a `max_turns` cap that ends the case at the artifact the act leaves, and mechanical graders over that artifact. The session under eval is the orchestrator, reading the target tree's `orchestration.md`, so old tree against new on the same cases is #923's comparison with `orchestrator` as a fifth agent name; its baseline is taken once, by the phase that writes the cases, against the merge base's plugin tree. Acts no fixture can reach — the pull request opened before round 1 (needs GitHub), closing the cycle, a fix pass resumed into a live agent — are census rows `not exercisable — <why>`, and their `check:` rows are what holds them (`chain_check.py`, `hooks/commit-review-gate.py`).

**Which suites a file's phase runs is measured, not guessed.** The agents whose spawns opened the file are the readers whose output the rewrite can change; the phase runs their full suites through #923's comparator and the orchestrator cases where the main session opens it. By the opens table that is all four agents for `CLAUDE.md`, `CONTRIBUTING.md`, `skills/verify/SKILL.md`, `templates/config.md`, the two `orchestration.md` and their templates; smith, warden and framer for `skills/evidence-check/SKILL.md`; none for the twelve small skills, whose rows are read against the shape and left. The census per phase maps each of the file's rules to `Exercised by: <case>/<grader>`, `held by: <check>` or `not exercisable — <why>`; the record test refuses a row with none, as #923 S13 says.

## Targets

The bar each phase is held to; the ceiling written into `seal/budgets.md` is the value the rewrite reached. Basis: the cap-5 kept estimate where the file is prose, the format's bytes plus three lines per cell where it is a template, and a read of what each file's rules are.

| File | Now | Target | File | Now | Target |
|---|---|---|---|---|---|
| `CLAUDE.md` | 9,261 | ≤ 5,000 | `templates/claude-md-block.md` | 4,695 | ≤ 2,600 |
| `skills/verify/SKILL.md` | 59,722 | ≤ 26,000 | `skills/evidence-check/SKILL.md` | 53,733 | ≤ 30,000 |
| `skills/code-review/orchestration.md` | 46,760 | ≤ 21,000 | `skills/implement/orchestration.md` | 52,161 | ≤ 30,000 (the acts table stays, ≈ 8 KB) |
| `templates/sdd-round.md` | 30,242 | ≤ 9,000 | `templates/sdd-routing.md` | 6,912 | ≤ 2,500 |
| `templates/sdd-phase.md` | 4,500 | ≤ 2,000 | `templates/sdd-plan.md` · `sdd-spec.md` · `sdd-overview.md` · `sdd-questions.md` | 3,530 · 2,951 · 2,169 · 1,934 | ≤ 2,200 · 2,000 · 1,500 · 1,500 |
| `templates/config.md` | 41,405 | ≤ 26,000 | `skills/config/SKILL.md` | 10,871 | ≤ 8,000 |
| `templates/seal-README.md` | 7,328 | ≤ 4,000 | `templates/ledger.md` · `pact.md` · `pact-review.md` | 4,263 · 2,043 · 1,768 | ≤ 2,500 · 1,200 · 1,000 |
| `CONTRIBUTING.md` | 23,896 | ≤ 11,500 | `skills/settle/SKILL.md` | 25,437 | ≤ 13,500 |
| `skills/commit-pr-convention/SKILL.md` | 10,888 | ≤ 8,000 | `skills/update/SKILL.md` | 9,774 | ≤ 6,500 |
| `skills/evidence-ci/SKILL.md` | 5,599 | ≤ 3,600 | `skills/writing-style/outside-the-review.md` | 7,861 | ≤ 6,000 |
| `templates/parity.md` and the twelve small skills | 30,287 | read against the shape; a row lowered only where the read cuts | `history:<every file in the set>` | 107 | 0 after its phase |
| **The set** | **462,890** | **≤ 258,000** (the 27 targets plus the 30,287 B read and left) | `preload:claude-md` | 9,261 | ≤ 5,000 |

## Scope

**In.** The 38 files above, rewritten to #923's shape one phase at a time in the order `plan.md` gives, each phase: the file's `bytes:` and `history:` rows lowered to what it reached; its released rows re-read or corrected in this item's fragment; its pins re-pointed or removed with a row; its #730 `BASELINE` entries lowered; its census; the eval record of every reader whose suite the file's opens name. The orchestrator cases, their generator, and their baseline. The record test's scope widened from `agents/*.md` and preloaded skills to every file with a `bytes:` row, so an on-demand rewrite without a record is red the way a preload's is. The six restatements inside the set made one home and one link: `skills/code-review/orchestration.md` §*the orchestrator's half*'s contract paragraph (home `skills/implement/SKILL.md`, Jaccard 0.65); the response-language rule in `skills/commit-pr-convention/SKILL.md` and `templates/config.md` §*What no row governs* (home the template, 0.79); the minor-anchor rule in `skills/evidence-check/SKILL.md` and `templates/ledger.md` (home the skill, 0.52); `Measured (#153)` in both `skills/evidence-check/SKILL.md` and `skills/code-review/orchestration.md` (both go); the `A range that DELETES a shipped section` rule in `skills/code-review/orchestration.md` and `agents/smith.md` (0.53; `questions.md` Q5 names whose); `A round that opens nothing needing a fix` in `skills/code-review/orchestration.md` and `docs/review-chain-spec.md` (home the doc, the skill links; #941 keeps the doc's). `CLAUDE.md`'s block regenerated from its template by `claude_block.py --write`, so the two stay one source.

**Out, and whose.** The preload set and `skills/legacy-parity/SKILL.md` (scribe's preload, in neither frame — `questions.md` Q4): #923. `docs/`: #941. The check and the harness: #923 phases 1–2, read and used, changed only where §*What this set needs* says (the record test's scope, a fifth agent name). The test suite's own size: #929, #942; a module here is touched only where it pins a sentence this work moves, and a `Kills:` line is #942's to add. `seal/config.md` (487 B, rows only) and `seal/README.md` (an instance of the template, 6 released rows): records of this repository, regenerated by nothing this item ships; the template is what every later bootstrap reads. The user's `~/.claude/CLAUDE.md` block: carried by `install.sh` and `update`, not by this tree. The 108 standing `routing.md` copies and every other record: history by design. `skills/writing-style/SKILL.md`: the owner's canon (#923 §*Scope*). `README.md`, `README.ko.md`: read by people (#755 d).

## Non-inferiority, per file

| File or group | Readers whose suites run (opens ≥ 10 % of the kind's spawns) | #923 cases that exercise its rules today | New cases or census reasons |
|---|---|---|---|
| `CLAUDE.md` + block | every agent (prefix) and the orchestrator | every rule-exercise case reads it in its prefix; the smith's build case shows the commit-and-routing rules (`routing.md` present, no heredoc, `git -C`) | O1 routing (below) for the block's routing bullet; the five repo-rule links are `held by:` their tests (`test_the_rules_claude_md_names_have_one_home.py`) |
| `skills/verify/SKILL.md` | smith, warden, framer, sealer | the proof and seal blocks (regex), the three labels, the sealer's `broad-gate.md` and `Broad gate` cell, `nothing left behind` | §*Measure the segment* is the orchestrator's post: `held by: session_cost.py` tests, `not exercisable` as an act; §*Counterfeits* rows that no grader shows are `held by:` the arm/mutation checks' tests |
| `skills/evidence-check/SKILL.md` + `templates/ledger.md` + `skills/evidence-ci/SKILL.md` | smith, framer, warden | the smith case's fragment (anchor shape regex) | one new smith case: a build whose edit drifts a released row, grader `Re-read ·` in the fragment; verdict and limit sections are the checker's own, `held by:` `tests/test_evidence_check.py` and siblings |
| `skills/code-review/orchestration.md` + `sdd-round.md` + `sdd-phase.md` | orchestrator; smith, warden, framer | the smith's phase record (`file_exists`, the asked-section regex); the warden's report shape | O2–O5 below; `check:`/`command:` acts `held by:` `chain_check.py`, `round_record.py` |
| `skills/implement/orchestration.md` + `sdd-routing.md` + `sdd-spec/plan/questions/overview.md` | orchestrator; framer, smith | the framer's three files (`file_exists`, the mark line regex), the smith's `overview.md` | O1; Bootstrap and parity setup `held by:` `hooks/mode-gate.py` and `not exercisable — hand-derived`; `What the answer writes` `held by:` `chain_check.py`, `hooks/routing.py` |
| `templates/config.md` + `skills/config/SKILL.md` + `seal-README.md` + pact and parity templates | smith, warden, framer, sealer | the sealer's broad run reads the `Broad gate` row; `pact-check` cases where #923 planted them | the row grammar `held by:` `hooks/config.py` tests (`test_one_table_walker_reads_what_gfm_renders.py`); the config skill's procedure `held by:` `test_the_mode_question_is_asked_once.py`, `test_first_setup_asks_once.py` |
| `CONTRIBUTING.md` + `settle` + `update` + `commit-pr-convention` + the small skills | smith, warden, framer, sealer (CONTRIBUTING); framer, sealer (settle); none for the rest | the contract cases' commit shape; the framer's and smith's commit-message cases where they commit | `settle` and `update` are release-time session acts: `held by:` `fold_check.py`, `test_settle_reads_before_it_removes.py`, `test_version_check.py`; the small skills have no case and no opens, census says so |

**The orchestrator cases**, K = 5, N = 2, `--concurrency 4`, each capped so that it ends at its artifact:

| Case | Fixture and prompt | Ground truth and graders |
|---|---|---|
| O1 the routing act | an opted-in fixture repository, an issue, "the owner pressed `automation`" | `seal/specs/*/routing.md` exists with the seven rows (regex on each vocabulary word); the first commit of the run adds that file and nothing else (the scaffold writes `git log --name-only` after the run, regex); no `AskUserQuestion` call (`tool_used` negated, where the harness has it — `questions.md` Q3) |
| O2 the record precedes the fixes | a clone at a round's `Target SHA`, the warden's report at its path | `rounds/round-1.md` exists, `round-record new` exit 0 on it; the commit adding it precedes any commit touching a reviewed file |
| O3 the run ends with a verifying round | the last record's `Fixes checked by` is `nobody`, the pull request is about to be marked ready | the last message names the verifying round and refuses ready; `tool_used` `Agent` |
| O4 a fix of a fix twice | records whose `Fix of a fix` row reads `second` | the next act is a framer spawn, not a fix pass: `tool_used` `Agent`, no `Edit` of a source file, the last message names the reframe |
| O5 verify before posting | a report file and the clone it was written against | the last message carries the four readings (regex on each) before any posting word |

Pass rule, cost and record: #923's, with `orchestrator` as the agent name in `evals/baseline-orchestrator.json` and `orchestrator-phase-N.md`. A run that spawns a real agent is bounded by `max_turns` and the cap is a `no result` under pass rule 5, so O3 and O4 are written to end at the spawn call.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a file reaches its target | a phase closes | `bytes:<file>` at or under its target in the checker's summary; `history:<file>` 0; before and after bytes in the phase record |
| S2 no released ledger file changes | every phase | `git diff --stat origin/release/v0.22.0 -- seal/releases seal/ledger.md` empty; a `Re-read ·` or `Corrected ·` row per drifted row in the fragment; `evidence-check` exit 0 |
| S3 every pin follows its sentence | every phase | each module that pinned a moved literal green on the new sentence, or the pin removed with an `overview.md` row naming module and literal |
| S4 an on-demand rewrite with no record is red | `skills/verify/SKILL.md` differs from the merge base and no `evals/<agent>-phase-N.md` names its readers | `tests/test_a_rewritten_definition_proved_non_inferior.py` red naming the file and the agents owed; green once the records exist and say `pass` |
| S5 a dropped orchestrator rule is caught | O1 run against a tree whose routing section no longer says the file is written before the first edit | the first-commit grader fails on the new side and passed on the old; `Verdict: fail` naming O1 |
| S6 the block has one source | phase 1 | `claude_block.py --check` exit 0; `tests/test_the_claude_md_block_has_one_source.py` green; `preload:claude-md` ≤ 5,000 |
| S7 a new work item's declaration is small | `routing.md` written from the rewritten template | ≤ 2,500 B; `hooks/routing.py` and `chain_check.py` parse it unchanged |
| S8 the acts table still holds | both `orchestration.md` rewritten | `tests/test_every_orchestrator_act_names_its_delivery.py` green: every marked heading kept, every row's act present |
| S9 marked sections stay marked | the same | `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` green; `preload:*` rows unchanged by this item |
| S10 a reader's output is not worse | each phase | the eval record of every agent in the file's readers column says `pass`; the test recomputes it |
| S11 the pairs drain | each phase | the file's `BASELINE` entries lowered in the same commit; `test_no_passage_is_pasted_into_a_second_file.py` green |
| S12 the six restatements are links | their phases | the enforcer gate exit 0; `--candidates origin/release/v0.22.0` lists none of the six; `restated` lower by six |
| S13 nothing asks a person | the whole change | no `AskUserQuestion`, no `input()`, no new prompt; every row lowers, so no `Budget raised:` line |
| S14 a template keeps what a generator parses | `sdd-round.md`, `sdd-phase.md`, `sdd-routing.md`, `ledger.md` | `round_record.py new`, `test_a_phase_hands_the_next_one_a_record.py`, `test_waiver_decided_at_start.py`, `test_a_row_points_by_content.py` green on the rewritten templates |

## Data & interfaces

`seal/budgets.md`: the `bytes:` and `history:` rows of the 38 files lowered phase by phase (no new row, no new family). `tests/test_a_rewritten_definition_proved_non_inferior.py`: scope read from `seal/budgets.md`'s `## File bytes` table rather than a fixed set, so every listed file that differs from the merge base owes a record (one case seen red: `skills/verify/SKILL.md` changed, no record). `evals/behaviour/orchestrator/O1…O5/` with `case.yaml`, `prompt.md`, `scaffold.sh`, `graders/*.md`; `evals/scripts/orchestrator_cases.py` (NAME NOT IN TREE until phase 3) building the fixtures from the tree's own records; `evals/scripts/noninferiority.py` reading `orchestrator` as an agent name. `.github/scripts/claude_block.py --write` after the block's rewrite. `tests/test_no_passage_is_pasted_into_a_second_file.py#BASELINE` entries lowered. Ledger: `seal/ledger/1791934660-what-an-agent-opens-on-demand-states-the-current-rule-only.md` — this spec's clauses on the orchestrator generator, the widened test and their cases, plus the `Re-read ·` and `Corrected ·` rows each phase writes. Changelog: this item's fragment with the per-file before/after table.

## Removes

| Removes | Coordinate | Where it lands, or why it can go |
|---|---|---|
| the five "why this row is here" sentences | `CLAUDE.md#"## Repo rule — the merge method is fixed per direction, and it is not a preference">"this row is the link, and it is here because a session about to"` and the four siblings | one sentence above the links says what a repo-rule row is |
| the routing procedure inside the block | `templates/claude-md-block.md#"## Git">"Routing, decided at the start"` paragraph beyond its first two sentences and the link | `skills/implement/orchestration.md` §*Orchestrator: how the work is routed* is the home; the block keeps the act and the link; `CLAUDE.md` follows by `--write` |
| the operator table's measured column | `skills/verify/SKILL.md#"### 2. Able to fail">"Measured 2026-09-09 on `hooks/review-history-guard.py`"` | #262 |
| the ten-failures story | `skills/verify/SKILL.md#"## The broad gate — after the rounds, then compare against the base">"Measured on one repository: a full suite showed ten failures, all ten"` | the rule keeps its why; the story is the issue's |
| the SQL-echo numbers | `skills/verify/SKILL.md#"## The cost of the run you repeat">"SQL echo logging for a slow suite, turned it off, and measured 131s → 137s."` | the rule (measure before you keep a recipe) stays; the numbers go |
| the move preambles | `skills/code-review/orchestration.md#"# code-review — the orchestrator's half">"The five sections `skills/code-review/SKILL.md` used to carry under an"`; `skills/implement/orchestration.md#"# implement — the orchestrator's half">"The sections `skills/implement/SKILL.md` used to carry for the session that"` | #265, #292, git history |
| the three-measurement resume story | `skills/code-review/orchestration.md#"## Orchestrator: a fix pass resumes the implementer">"Measured three times, with no counterexample: as a fresh spawn, one fix pass"` | the why keeps one figure and #33; the rest is #29's and #57's |
| the four-round #82 story | `skills/code-review/orchestration.md#"### A fix pass adds the unit that pins it, and that unit ships unreviewed">"Measured across four rounds of #82: round 1's fixes added `configured_language`"` | #82 |
| the #153 measurement, both copies | `skills/code-review/orchestration.md#"### The check a round runs reads everything, and only a write is narrowed">"Measured (#153): one work item's three review rounds and two fix passes all"`; `skills/evidence-check/SKILL.md#"## Verdicts and what to do">"Measured (#153): one work item's three review rounds and two fix passes all"` | #153 |
| the "until #330 there was no list" paragraph | `skills/implement/orchestration.md#"## Orchestrator: which of these acts runs itself">"`skills/code-review/orchestration.md`, and until #330 there was no list of"` | #330; the table and its four values stay |
| the timing paragraph under the limits | `skills/evidence-check/SKILL.md#"## Known limits">"2026-09-23, CLI wall time, median of five, Python 3.12 on macOS, on"` | `evidence_check.py`'s docstring, where a reader of the code looks |
| the comment stories of the round template | `templates/sdd-round.md#"<!-- #81: round 1 of that work item found five defects in 7.6 minutes and"`, `>"to collapse eight findings toward one key in silence (#227). The fix pass"`, `>"the word `confirmed` and never `fixed`, and no 🔴 anywhere in it (#437):"`, `>"carried none of the artefact those paragraphs are about (#187). Measured: a"` | #81, #227, #437, #187; the cell rule and its link to `docs/round-record-spec.md` stay |
| the routing template's reasoning | `templates/sdd-routing.md#"<!-- Review — `through the review chain` or `straight to the PR`."` comment beyond one line per row | `skills/implement/orchestration.md` §*What the answer writes* is the home and is linked |
| the dependency stories under the checks | `CONTRIBUTING.md#"## Running the checks">"(#667). Pillow decodes the release seal the tag push draws with"` and the lines citing #718, #832, #647, #337, #133, #156, #841, #864, #684 | the rows name each dependency and the check it serves; the issues hold why |
| "Two cautions, both measured the same day" | `skills/update/SKILL.md#"## …">"Two cautions, both measured the same day. `.in_use/` under a version"` | the two cautions stay as rules; the day goes |

Sentence-level removals inside a rewritten section are the rewrite itself, read by `survivor-check`, the phase's census and the suite, as #923 §*Removes* says. The second copy of each of the six restatements becomes a link and is not removed. A pin dropped with its sentence is an `overview.md` divergence row.

## Open questions → questions.md

Framed 2026-10-14 by framer, before the build.
