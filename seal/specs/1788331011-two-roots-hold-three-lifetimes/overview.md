# 1788331011-two-roots-hold-three-lifetimes — overview

<!-- The closing memo (implement skill, step 4). Opened by phase 1 at its
first divergence; phase 3 closes it. Not a summary of the work: `git diff
--stat` holds the file list and the diff holds the detail. Only what the diff
cannot show goes here. Facts that must outlive this work item are in
`seal/ledger/1788331011-two-roots-hold-three-lifetimes.md`, not here. -->

📋 implement applied
· spec:     `docs/one-root-by-lifetime.md` §"The opt-in signal is the root itself" and §"What happens to the existing directories at the switch"; `spec.md` S1–S16, "The move, in order", "What the session prints, and what it refuses", "The opt-in, read one way", the per-file table; `plan.md` alternative A and the Phases table; `questions.md` Q1–Q8 at their defaults; `changelog.md`; `seal/follow-up.md` (empty of items)
· evidence: `seal/ledger/1788331011-two-roots-hold-three-lifetimes.md`, 13 rows (phase 1); 12 rows in other fragments re-verified at `a4206b0`
· verified: see the fragment — every row executed; the full suite, lint and typecheck deliberately not run (the broad gate runs once after the rounds settle)

## Why this work exists

`specs/<id>/` and `.specseal/` held three lifetimes in two roots and the opt-in
was one of the two directories; after this, `seal/` holds all three, laid out
by lifetime, and its presence is the opt-in — so every gate, checker and
release script reads one root, and a repository on the old layout is moved
once at session start rather than left to find out.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The marker when nothing old is left | Spec table row 5: *nothing old left → nothing printed, stamped if not already*. Code stamps only when `seal/` exists at the root; a repository with neither layout is left alone | code | The stamp's one job is the once-per-repository rule, which is consulted only where something old exists; the case it guards is an old branch checked out after the move (pinned by `test_a_moved_repository_is_stamped_so_an_old_branch_is_not_moved_again`). Stamping every repository the plugin ever opens would list them all in `~/.claude/specseal/root-migrated` for nothing |
| What counts as dirty | S6: *`git status --porcelain -- .specseal specs` prints anything*. Code ignores an entry whose index column is `R` or `D` with a clean worktree column | code | S7 is unreachable otherwise: a stopped run leaves staged renames whose SOURCE paths are under the old roots, so the literal rule refuses every resume as dirty. A staged addition or modification, anything untracked, and anything with a worktree change still refuse (`test_a_staged_edit_under_the_old_roots_is_work_in_progress_too`) |
| `--follow` on the README | S1: *`git log --follow` on any moved file reaches its history*. `seal/README.md` does not: rewritten whole from the template in the same commit, git pairs no rename | spec, knowingly not met for one file | Q5 (a) chose the overwrite; the old text is in history under `.specseal/README.md`, and the file is plugin-owned. Every other moved file follows |
| Which renames are excluded | S10: *never a renamed one*. Code excludes exact renames (`R100`) only; a rename carrying an edit is judged | code | The prompt's own words, *a `routing.md` that the pull request only renamed*: an edit on the way over is the pull request's, and the check exists to read it (`test_a_declaration_the_pull_request_renamed_and_edited_is_judged`) |
| Two routing cases inverted | `tests/test_routing_is_recorded.py` pinned *writing a declaration creates no plugin home*; a declaration under `seal/specs/` creates `seal/`, which is the opt-in | code, with the two cases rewritten to pin the consequence | The design record makes the root the signal and puts the whole work item under it; the hazard those cases guarded (four gates switched on by answering a routing question) is answered by the `implement` skill's once-per-repo moment creating `seal/` on purpose (S14, phase 2) |
| `conftest.py#declare_routing` in phase 1 | `plan.md` puts the shared fixtures in phase 3 | one line moved forward | The S11 test files cannot pass while the fixture writes `specs/<item>/routing.md`, and the spawn prompt allows exactly that case; the rest of the fixture sweep stays in phase 3 |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, repository-wide lint and the typecheck on this branch | the orchestrator's broad gate, once after the review rounds settle |
| `hooks/root-migrate.py` on Windows — porcelain's two columns and the `/`-joined pathspecs are written for it, nothing here ran there | CI's windows leg on the pull request |
| a real repository other than this one migrated by the hook at an actual session start under `dispatch.py` (the fixture run and this repository's run both called `main()` directly) | the repository owner, at the first session start after installing this branch's plugin in another opted-in repository |

## Not done

- The four private `git_dir()` copies (`implementer.py`, `review-skill-gate.py`, `session-lease.py`, `worktree-guard.py`) are not folded into `optin.git_common_dir`; `plan.md` names the fifth lookup and this phase adds it without removing one, because the four answer the GIT dir where this one answers the COMMON dir and the difference matters in a linked worktree.
- Prose paths in released round records, overviews and plans still read `specs/<id>/`, per the spec's Out list.
- `tests/test_waiver_decided_at_start.py` and `tests/test_routing_is_recorded.py` still assert `specs/<work-item-id>/routing.md` in the skill and agent texts; the assertions pass by substring and phase 2 re-points the texts.

## Fed back into the spec

none — the four judgments above are recorded here rather than written into
`spec.md`; phase 3 decides whether S6 and the table's row 5 should say what the
code does.
