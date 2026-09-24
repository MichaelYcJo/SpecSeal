# the spec is split and its sentences are settled — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `seal/specs/1790208643-…/{routing,spec,plan,questions}.md`; `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*, §*A row is a content anchor*, §*A correction a merge dropped*; `CLAUDE.md` §*Repo rule — a change writes fragments*, §*commit early*; `CONTRIBUTING.md` §*House rules*, §*What a change to a gate must carry*; `docs/release-checklist.md` §0–§3; `docs/branch-and-release.md` (D's fold paragraphs); `skills/settle/SKILL.md` §2; `skills/agent-contract/SKILL.md` §1–§16; `templates/sdd-phase.md`, `templates/sdd-overview.md`; MichaelYcJo/SpecSeal#526, #488, #509, #466, #474, #55, #316, #222, #268, #556, #561, #562
· evidence: `seal/ledger/1790208643-the-spec-is-split-and-its-sentences-are-settled.md` S1–S3, E1–E2, N1–N4, P1, C1–C2 (stamped by `--reverify`); in `seal/ledger.md` and three sibling fragments: 18 rows re-pointed for the split, every row a phase drifted re-read with a dated note, G6, G7, G1 and A5 corrected in place, 22 rows' cell pipes escaped
· verified: executed — each phase's modules, the red runs the phase records quote, the mutation and planting probes, `evidence-check --strict .` at every phase, the survivor sweep, `correction-check`, `unverified-check`, `rider_check.py`, ruff over every edited `.py`, #561's zsh measurement, and at hand-back every module that reads an edited document or script; read — each ledger row's claim against its edit, the citations against the section map; unverified — the broad gate (the sealer), the `CLAUDE.md` paste (the orchestrator)

## Why this work exists

`docs/review-chain-spec.md` was the one document over the 1,000-line ceiling,
so no fold could place a chain rule there. It is now three documents, each
under the ceiling: the run, the hooks, and the round record. The sentences
the milestone's other tickets asked for are settled in the documents where
they live after the split, and two ledger defects the 0.15.1 release would have
met at step 2 are fixed before it runs.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The declaration's tail | `spec.md` §*What was measured* and `plan.md` §Technical context: a 17-line tail | the 35 lines from *Which declaration applies* to *Deleting the routing file restores today's behavior exactly*, moved whole | the frame quotes those two sentences as the tail's ends, and the text between them is 35 lines at the merged base (`phases/phase-0.md`) |
| *The floor*'s *like the two above* | `plan.md` §*What the move has to reword*: names `Pass` and `Fixes checked by` | names `Fixes checked by` and the fix surface's two rows | `Pass` is read on the last record only, and §*The fix surface* opens *Two more rows, read on every record the same way `Fixes checked by` is* (`phases/phase-1.md`) |
| Six rewordings not on the plan's list | `plan.md`: *a rewording not on this list is a finding for the reviewer to weigh* | made, and listed in `phases/phase-1.md` | each is a positional reference that dangles in its new file; the survivor sweep reports none of them |
| `COVERED` | `spec.md` §Scope: both new documents join `tests/test_docs_line_wrap.py#COVERED` | the gate document joins, and the record document does not | the record document's one 89-column line is a path and its comma, and fitting it rewords a sentence `seal/ledger.md` row R4 quotes, which the sweep reported (`phases/phase-1.md`) |
| S18 | *`git diff --stat` names no file under `hooks/`* | four hooks' comments and docstrings re-pointed, with no behaviour change | `spec.md` §*Data & interfaces* lists those lines as re-pointed, and S4 fails without them |
| The shipped citations | `spec.md` §*Data & interfaces*: 20 lines in 15 files | 22 lines | `hooks/commit-review-gate.py:308` names a section the gate document holds, and `skills/code-review/SKILL.md:290` is C's (#552), which landed after the frame was drawn |
| The ledger anchors | `spec.md`: 23 anchors; 3 heal under `--reverify`, 15 re-pointed by hand | 24 anchors, the 24th in C's fragment; all 12 broken anchors re-pointed by hand | the checker skips the repository-wide scan over 200 files, so no moved anchor healed on its own (`phases/phase-1.md`) |
| #222 | `spec.md` §Scope: one paragraph in `depth_two`'s docstring | withdrawn; #559's paragraph stands | an outside contribution closed #222 first and the owner chose it; the orchestrator removed this item's paragraph at `4a077852` (`phases/phase-3.md`) |
| #488's third arm in `CONTRIBUTING.md` | `spec.md` §Scope: a third arm beside the two answers | a sentence saying the two answers are both writes to the file the row is in, and neither an append | the first answer already is the drift-by-edit case; what was missing is that it is the exception rather than an append (`phases/phase-3.md`) |
| #488's carriers | `spec.md` §Scope: three carriers | four: `skills/evidence-check/SKILL.md` §*`correction-check`* stated the exception too, and the sweep found it | corrected in the same phase; `correction_check.py`'s #424 narrative exempted with grounds (`survivors.md`) |
| #562's three doubled rows | the issue: escape each unescaped pipe | the second date-and-notes pair in three Notes cells escaped too, not merged | which pair is the row's is a judgment about a claim, outside an escape (`phases/phase-8.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck over the branch | the sealer, once, after the review rounds settle (`agents/sealer.md`) |
| ✅ Where #558's per-release ledger file leaves the rows phase 1 re-pointed in `seal/ledger.md` | answered at phase 3: `seal/releases/` does not exist until the 0.15.1 release runs `--split`, so the rows stand in `seal/ledger.md` and the split carries them byte for byte, measured on a scratch clone (`phases/phase-3.md`, `phases/phase-7.md`) |
| The `CLAUDE.md` copy of #488 and #509 — `phases/phase-3.md`'s two replacements; `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` is red on `CLAUDE.md` until they land | the orchestrator, who edits `CLAUDE.md`; then `evidence-check --reverify .` for row C8 |

## Not done

`CLAUDE.md` is not edited by this item; its copy of #488 and #509 is the
orchestrator's paste (`phases/phase-3.md`).

#526's items 2 and 3 (the `Enforced by:` retrofit and the shape and ceiling
checks as plugin commands) moved to #565 and #566, filed by the orchestrator
so #526 closes with what this item shipped. #331 is deferred to the next
milestone. The three ledger rows #562 found carrying a second date-and-notes
pair in one Notes cell (G5 and S4 of #386's section, and *The eleven modules
that pin the path*) are escaped and not rewritten as one note each, because
merging them is a reading of each claim. `docs/round-record-spec.md` stays
out of the wrap list for the reason `phases/phase-1.md` gives.

## Fed back into the spec

none
