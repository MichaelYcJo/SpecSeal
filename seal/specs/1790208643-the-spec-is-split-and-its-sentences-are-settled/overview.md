# the spec is split and its sentences are settled — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     written at the close of phase 6 — phases 0–2, 4 and 5 are built and phases 3 and 6 wait for #558
· evidence: written at the close of phase 6 — until then each phase record names the rows it re-pointed or re-stamped
· verified: written at the close of phase 6 — until then each phase record labels what was executed and what was read

## Why this work exists

`docs/review-chain-spec.md` was the one document over the 1,000-line ceiling,
so no fold could place a chain rule there. It is now three documents, each
under the ceiling: the run, the hooks, and the round record. The sentences
the milestone's other tickets asked for are settled in the documents where
they live after the split.

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

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck over the branch | the sealer, once, after the review rounds settle (`agents/sealer.md`) |
| Where #558's per-release ledger file leaves the rows phase 1 re-pointed in `seal/ledger.md` | the resumed smith at phase 3, after #558 squashes and the release branch is merged in again |

## Not done

Phase 3 (#488, #509) and phase 6 (the records) are not built. Both are
written against step D's text of `docs/the-evidence-ledger.md`, `CLAUDE.md`,
`CONTRIBUTING.md` and the release checklist, and D (#558) had not squashed
when this build ran.

Phase 4 found two ledger rows that phase 6 corrects beside G6 and G7, because
they are ledger corrections written against D's shape of the file.
`1789985781`'s G1 still says *Half a pin is #423's finding 4* (#474 item 3's
class, a carrier the ticket did not list). A5's Clause says `seal` *keeps that
run behind it* and does not name the same-run replace (#556's class).

## Fed back into the spec

none
