# the baseline is the moving pull-request base — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show. -->

📋 implement applied
· spec:     `CLAUDE.md` §the goal a design is chosen against · §the merge method is fixed per direction · §a change writes fragments, never the shared file · `agent-contract` §1 §2 §3 §9 §12 §14 §15 · `implement` §1 §2 §3 §4 · `docs/release-checklist.md` step 0 and step 3 · `docs/one-root-by-lifetime.md` §would break on removal · `skills/verify/SKILL.md` §and something has to read the row afterwards · `seal/follow-up.md` (no row is a prerequisite of this work) · this work item's `spec.md`, `plan.md`, `questions.md`, `routing.md`
· evidence: R1–R4 in `seal/ledger/1788873600-the-baseline-is-the-moving-pull-request-base.md`; four rows re-verified in `seal/ledger.md` (S12, the fix-pass entry-points row, S5/Q4/Q9, S7) whose anchors this change drifted
· verified: **executed** — `tests/test_unverified_rows_close.py` 86 passed; the five neighbouring modules that load this reader 303 passed; `tests/test_release_hygiene.py` and seven other document-scanning modules 333 passed; `evidence_check.py --strict .` 938 ok · 0 drifted · 0 broken; the real invocation on this repository, exit 0 over 49 overviews, and a mistyped path exit 2; eleven mutations one at a time, ten dead on the first pass and the eleventh dead once its case existed. **read** — the full suite on the base, `2808 passed, 2 skipped in 439.63s`, executed by the orchestrator at `c0a65d5`. **unverified** — the suite on this branch, and CI's checkout shape; both rows below

## Why this work exists

Squashing one work item made every sibling branch of the same release fail a
check that was measuring correctly and reporting the wrong event, and the cost
grew with roughly the square of the items a release carries.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Which arms read the baseline | The ticket's repair section: *"Nothing else in the module changes: the other two arms already read only this branch's own files."* The code: `show(root, args.baseline, rel)` reads the base revision, so the row-count arm calls the base as much as the file-is-gone arm does | One resolution point, so all three reads take the merge base | The ticket's own *What has to be decided* section asks for this to be *"read rather than assumed"*, and reading it answers no. `check_text`'s docstring records the alternative's price: two readers of one thing, *"four pairs drifted apart across three review rounds — and each fix on one side opened a gap on the other."* `questions.md` Q1 |
| How a refusal names the revision | `spec.md` S6/S7 wanted the compared revision named; the existing cases assert `present at HEAD and not here` | One rule — the shortest name that is true — rather than two message shapes | Where the merge base is the ref's own commit the ref names it exactly, so this is not a conditional message. It also keeps every case written before this change asserting the text a reader still sees |
| What pins the documents | `spec.md` S8 first named `test_no_document_still_states_the_moving_base`, an absence check | `test_the_documents_state_the_merge_base_footing`, parametrized over the eight documents | An absence check goes green on a rewrite that says nothing, which is this module's own *zero reads as all-closed* failure. `test_the_skill_states_the_closing_convention` is the precedent for the positive form. The record was corrected rather than left: `evidence_check.py` refused the old name as NOT-IN-TREE |
| Where the never-rebase rule lives | `docs/release-checklist.md` step 0 carried it inside the workaround paragraph this change removes, and no other document in `docs/` states it | Kept in step 0, rewritten as a standing rule with its own grounds | Removing the workaround would have taken the only statement of the rule in `docs/` with it, which is #180's class exactly. `CLAUDE.md`'s merge table implies it; nothing in `docs/branch-and-release.md` said it |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite on this branch. Read, not executed: `2808 passed, 2 skipped in 439.63s` at `c0a65d5`, the base, run by the orchestrator on macOS | the orchestrator, in the broad gate after the rounds |
| That `actions/checkout@v4` on a `pull_request` event checks out the merge of the head into the base, which is what makes this arm unable to fire in CI and the repair a no-op there. Read from the action's documented default, not executed. The repair is correct under both checkout shapes, so nothing here rests on it | the repository owner, or the first CI run on a branch whose base has moved |
| Whether exit 2 is the right answer for a shallow clone whose base ref resolves while their common ancestor sits beyond the graft. Both workflows set `fetch-depth: 0`, so no CI leg is in that state | the repository owner — `questions.md` Q2 |
| Whether the row-count arm was meant to keep the moving base. Taken as no, on the reading of `show`; the ticket says the opposite in prose | the repository owner — `questions.md` Q1 |

## Not done

**The arm is not scoped to the work items a pull request touches.**
`docs/one-root-by-lifetime.md` wants that for `settle`, and the merge base does
not deliver it: a `settle` commit removes a merged work item's directory
relative to the fork point as well, so the arm still refuses. Scoping it by the
diff would trade this defect for a worse one — a directory deleted wholesale
appears in no diff under a name this check recognises, which is
`test_renaming_the_work_item_directory_fails_the_baseline`. The bullet in that
document is corrected where it named the compared revision and left standing
where it names the `settle` problem. `questions.md` Q3.

**`docs/flow.md`'s preamble was left alone.** Its sizing sentence says a
release here is three or four work items, and 0.9.3 now carries five. It is not
touched because a branch writes only its own section — that rule is what keeps
the file mergeable — and because the sentence already coexists with 0.9.1's
seven. Nothing is owed unless the owner wants the sentence re-stated.

**No mechanism was added for #180's class.** The eight documents that state
this arm's footing were enumerated by grep and corrected, and
`test_the_documents_state_the_merge_base_footing` pins them; the general
after-a-fix-pass grep #180 asks for is that work item's, on a sibling branch.

## Fed back into the spec

**`docs/release-checklist.md` step 0's never-rebase rule is now stated as a
standing rule rather than as a footnote to a workaround** — inferred during
implementation. Removing the workaround paragraph would have removed the only
statement of the rule in `docs/`, and a rule whose only home is a paragraph
about something else is one edit from gone. A planner may decide it belongs in
`docs/branch-and-release.md` beside the merge table instead; nothing here
depends on where it lives, only on its not having left.
