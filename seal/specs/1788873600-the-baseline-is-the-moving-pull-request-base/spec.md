# Feature Specification: the baseline is the moving pull-request base

<!-- seal/specs/1788873600-the-baseline-is-the-moving-pull-request-base/spec.md — WHAT this work
delivers and how we'll know. The policy documents in docs/ outrank this file. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | The arm's refusal is a stop that reaches a person, and it reaches them for a state nobody created. It is the most expensive kind of check this repository recognises, and the repair is what makes the release run unattended |
| `CLAUDE.md` §*Repo rule — the merge method is fixed per direction* | Rules the rebase repair out by construction. A feature branch squashes and `main` takes a merge commit; nothing in that table rewrites a branch's commits, and two mechanisms point at them by SHA |
| `skills/agent-contract/SKILL.md` §12 | The finding names the file-is-gone arm. The class is every read of the baseline in this module, which is two arms, and the enumeration is below |
| `skills/agent-contract/SKILL.md` §14 | The arm's refusal text is read and acted on, so a changed footing is documented in the same commit and pinned |
| `skills/agent-contract/SKILL.md` §15 | The moved-base case has to be seen red against the old code, or the change is indistinguishable from making the arm inert |
| `docs/release-checklist.md` step 0 | Carries the workaround this removes. The paragraph goes with the repair, and the never-rebase rule inside it does not |

## Scope

**In.** `skills/verify/scripts/unverified_check.py` resolves `--baseline REF`
to `git merge-base REF HEAD` once, and every read of the base below that point
uses the resolved commit: the row-count arm's `git show`, the file-is-gone
arm's `git ls-tree`, and the missing-path arm that asks whether a deleted scan
path held anything. A report names the revision it actually compared against.
A `REF` that shares no history with `HEAD` is exit 2, because a comparison
against nothing is not a comparison.

The documents that state the old footing, all of them, in the same commit:
`docs/release-checklist.md` step 0, `docs/one-root-by-lifetime.md` and its
Korean mirror, `README.md` and `README.ko.md`, `skills/verify/SKILL.md`, and
the workflow comments in `.github/workflows/hygiene.yml` and
`templates/hygiene.yml`. And `docs/flow.md`'s 0.9.3 section, which is this
branch's to correct because the item joined the release after the section was
written.

**Out.** The two other refusals. The malformed-section arm reads the working
tree only. The exit-2 arm for a ref that does not resolve is about the ref
itself and keeps naming the ref the caller typed. `chain_check.py` and the
inline `git diff` steps in `hygiene.yml` are outside because they already read
`<base>...HEAD`, which is the merge base — the enumeration below is what
establishes that rather than assuming it.

**Out, and named because the ticket raises it.** Rebasing the stale branch.
Every round record names its branch's commits by `Target SHA` and every
`# RIDER:` carries a `Verified … at <sha>` stamp, so a rebase orphans both.

## The class, enumerated by construction

Every call in this repository that hands a caller-supplied baseline ref to git
and compares the answer against this branch:

| Site | What it asks git | Merge-base already? |
|---|---|---|
| `unverified_check.py#overviews_at` | `git ls-tree -r --name-only <ref>` — the SET of overviews at the base | **no** — the arm the ticket names |
| `unverified_check.py#show` | `git show <ref>:<path>` — one file's rows at the base | **no** — the ticket calls this arm indifferent, and it is not: it reads the base revision, so a base that gains a row in this branch's own overview reports rows this branch never had |
| `unverified_check.py` missing-path check | `overviews_at` again, for a scan path that is gone | **no** — same call, same resolution point |
| `chain_check.py#changed`, default path | `git diff … <base>...HEAD` | yes, by `...` |
| `chain_check.py#changed`, `--worktree` | `git merge-base <base> HEAD` explicitly | yes, stated in that work item's `phases/phase-1.md` |
| `hygiene.yml` version step | `git diff --name-only "$base"...HEAD` | yes, by `...` |
| `hygiene.yml` READMEs step | `git diff --name-only "$base"...HEAD` | yes, by `...` |
| `hygiene.yml` version step | `git show "$base:.claude-plugin/plugin.json"` | **no, and correctly so** — it asks what version the base carries, which is a question about the base and not about this branch |

So the class is three call sites in one module, all downstream of one
resolution point, and the repair is at that point rather than at any of them.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the moved base | Given a base that squashed a sibling work item after this branch forked · When the check runs against that base · Then exit 0, and nothing is reported as having left the record | `test_a_work_item_squashed_after_the_fork_is_not_this_branchs_removal` |
| S2 not inert | Given the same moved base and a branch that also deleted its own `overview.md` · When the check runs · Then exit 1, naming that file | `test_the_moved_base_does_not_excuse_this_branchs_own_deletion` |
| S3 the row arm, moved base | Given the base gained a row in this branch's own `overview.md` after the fork · When the check runs · Then exit 0 | `test_a_row_the_base_gained_after_the_fork_is_not_a_deletion` |
| S4 the row arm, not inert | Given the same moved base and a row deleted on the branch · When the check runs · Then exit 1 | `test_the_moved_base_does_not_excuse_a_deleted_row` |
| S5 no common commit | Given a baseline ref sharing no history with `HEAD` · When the check runs · Then exit 2 and `nothing was compared` | `test_a_baseline_that_shares_no_history_with_head_exits_2` |
| S6 the report says what it read | Given a base whose commit is not the merge base · When a refusal is printed · Then it names the merge base and its short commit | `test_a_moved_base_report_names_the_merge_base_it_compared` |
| S7 and says it in the shortest true form | Given a base that IS the merge base · When a refusal is printed · Then it names the ref alone | the existing baseline cases, which assert `present at HEAD and not here` |
| S8 the documents agree | Given the repair · When each of the eight documents that describe this arm is read · Then each states the merge base as the revision compared against | `test_the_documents_state_the_merge_base_footing`, parametrized over the eight |

## Data & interfaces

`--baseline REF` keeps its name, its position and its meaning to a caller:
*the branch this pull request merges into*. What changes is which commit of
that branch is read — the last one this branch agreed with, rather than its
tip. `resolves(root, ref)` keeps its name and signature, because
`chain_check.py` loads this module and calls it; it is reimplemented over the
new `commit_of` so the two cannot drift.

`hygiene.yml` and `templates/hygiene.yml` pass `origin/${{ github.base_ref }}`
and keep doing so. The invocation does not change; only what the module makes
of it.

## Open questions → questions.md

Two, both recorded with the repository owner as their answerer: whether the
row-count arm was meant to keep the moving base, and what exit 2 on a shallow
clone with no reachable merge base costs a caller who is not CI.
