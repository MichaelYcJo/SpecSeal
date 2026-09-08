# Implementation Plan: the baseline is the moving pull-request base

<!-- seal/specs/1788873600-the-baseline-is-the-moving-pull-request-base/plan.md — HOW, in phases.
The Design Gate's artifact; the owner answered it before the run. -->

## Summary

`--baseline REF` is resolved once, to `git merge-base REF HEAD`, and every read
of the base below that resolution uses the resolved commit. One substitution at
one site, because all three of the module's base reads already funnel through
`args.baseline` in `main`.

A report names the revision it compared against **in the shortest form that is
true**: the ref alone where the merge base is the ref's own commit, and
`the merge-base of <ref> and HEAD (<short>)` where the base has moved past the
fork. The extra words appear exactly where they carry information, and every
existing case runs with `--baseline HEAD`, where the two are the same commit.

## Technical context

`skills/verify/scripts/unverified_check.py#main` holds the whole baseline
block: `repo_root`, then `resolves`, then the outside-the-repo check, then the
missing-path check, then the per-file row comparison, then the set comparison.
Three of those call git with `args.baseline`.

`resolves(root, ref)` is loaded and called by
`skills/code-review/scripts/chain_check.py` (`reader.resolves`) and through it
by `round_record.py`, so its name and signature are fixed. The module's own
docstrings say twice why a second reader is refused — *"There used to be two,
and while both existed every property added to one had to be added to the other
by hand. Four pairs drifted apart across three review rounds"* — so `resolves`
is reimplemented over one new `commit_of` rather than left beside it.

`chain_check.py#changed` under `--worktree` already takes the merge base
explicitly, and that work item's `phases/phase-1.md` records the choice as
*"stated rather than pinned"* because no fixture there moved the base. This
work item pins it for this module.

**What breaks in six months.** A caller with a shallow clone whose base ref
resolves but whose common ancestor does not gets exit 2 where it used to get a
comparison against the base tip. That is a louder failure than the quiet wrong
answer it replaces, and the module already exits 2 for the shallow clone that
lacks the base ref at all — but a caller who is not CI meets it, and
`questions.md` Q2 names it.

**What is measured and what is inferred.** In CI the arm cannot fire at all:
`actions/checkout@v4` on a `pull_request` event checks out the merge of the
head into the base, so the squashed sibling's `overview.md` is in the working
tree and the set comparison finds nothing missing — and `git merge-base
origin/<base> HEAD` on that commit is the base tip itself, so the repair is a
no-op there. That reading of `actions/checkout`'s default ref is **not executed
here** and is recorded in the overview's `## Not verified`. Where it fires is
the local gate, `docs/release-checklist.md` step 3, which is where 0.9.2's
three branches met it. The repair is correct under both checkout shapes, which
is what makes the inference safe to build on.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Resolve `--baseline` to the merge base once, at the single resolution point | A shallow clone with no reachable common ancestor now exits 2 rather than comparing against the base tip. Q2 | **taken** |
| Merge base for the file-is-gone arm only, as the ticket's repair section reads it | Two arms of one refusal read two different revisions, and one report names both. This module's history is four pairs of readers drifting apart across three review rounds; adding a fifth pair to fix one is the shape it keeps closing | rejected |
| Scope the arm to the work items the pull request's diff touches | It answers the ticket and loses the case the arm exists for: a branch that deletes a work item's whole directory does not touch it in the diff under any name the check would recognise, which is `test_renaming_the_work_item_directory_fails_the_baseline`. `docs/one-root-by-lifetime.md` names this as the `settle` item's own problem, so it is that item's to take | rejected, and left to `settle` |
| Rebase the stale branch, the standing workaround | Orphans every `Target SHA` in every round record and every `Verified … at <sha>` rider stamp. This repository has a patch release about that class | rejected by `CLAUDE.md`'s merge table |
| Merge the release branch into the stale branch, the other standing workaround | Works, and is what 0.9.2 paid three times: a merge, a re-run broad gate, a re-pushed pull request and a `docs/flow.md` conflict each, roughly quadratic in the items a release carries | rejected — it is the cost, not the repair |
| Drop the file-is-gone arm | Deleting the file becomes cheaper and quieter than deleting one row from it, which is the arm's own reason for existing | rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | One resolution point in `unverified_check.py`; all three base reads and all three report labels downstream of it; exit 2 for no common commit | `./bin/test tests/test_unverified_rows_close.py -q`, with S1–S7 seen red against the pre-fix module and the whole module green after | |
| 2 | Every document that states the old footing, and `docs/flow.md`'s 0.9.3 section | `./bin/test tests/test_unverified_rows_close.py tests/test_release_hygiene.py tests/test_no_real_identifiers.py -q` | |

## Operational impact

- **A caller's invocation does not change.** `hygiene.yml` and
  `templates/hygiene.yml` keep passing `origin/${{ github.base_ref }}`, and
  `docs/release-checklist.md` step 3 keeps passing `origin/main`.
- **A shallow clone with no reachable merge base becomes exit 2.** Both
  workflows set `fetch-depth: 0`, so neither is in that state. Q2.
- **No new dependency and no new argument.** `git merge-base` is plumbing that
  has shipped in every git this repository's other checkers already require.
- **`templates/hygiene.yml` changes only in a comment**, so a repository that
  installed an earlier copy keeps a workflow that still works — it pins the
  plugin version it clones, and the behaviour it describes is the clone's.
