# 1788331011-two-roots-hold-three-lifetimes — overview

<!-- The closing memo (implement skill, step 4). Opened by phase 1 at its
first divergence; phase 3 closes it. Not a summary of the work: `git diff
--stat` holds the file list and the diff holds the detail. Only what the diff
cannot show goes here. Facts that must outlive this work item are in
`seal/ledger/1788331011-two-roots-hold-three-lifetimes.md`, not here. -->

📋 implement applied
· spec:     `docs/one-root-by-lifetime.md` §"The opt-in signal is the root itself" and §"What happens to the existing directories at the switch"; `spec.md` S1–S16, "The move, in order", "What the session prints, and what it refuses", "The opt-in, read one way", the per-file table; `plan.md` alternative A and the Phases table; `questions.md` Q1–Q8 at their defaults; `changelog.md`; `seal/follow-up.md` (empty of items)
· evidence: `seal/ledger/1788331011-two-roots-hold-three-lifetimes.md`, 13 rows (phase 1), 6 rows (phase 2) and 4 rows (phase 3); 12 rows in other fragments re-verified at `a4206b0`, after phase 2's re-point 5 more re-verified and one re-anchored to the sentence it cites, and after phase 3's fixture substitution one row in `seal/ledger/1788310269-the-implementer-leaves-a-mark.md` re-read and re-verified, its claim now naming `seal/specs/<item>/routing.md`; after round 1, eight rows in a *What round 1 settled* section (one per fix, and the four drained from `rounds/evidence-todo.md`, re-run here), and the row above that one in the same other fragment re-worded to `seal/` with its anchor untouched
· verified: see the fragment — every row executed except the spec re-read in phase 3's last row, which says Read; `evidence_check.py --strict .` at `0 broken` at the close of phase 3 and again at the close of round 1's fix pass (totals in the fragment's last row); the full suite, lint and typecheck deliberately not run (the broad gate runs once after the rounds settle)

## Why this work exists

`specs/<id>/` and `.specseal/` held three lifetimes in two roots and the opt-in
was one of the two directories; after this, `seal/` holds all three, laid out
by lifetime, and its presence is the opt-in — so every gate, checker and
release script reads one root, and a repository on the old layout is moved
once at session start rather than left to find out.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The marker when nothing old is left | Spec table row 5 said *nothing old left → nothing printed, stamped if not already*. Code stamps only when `seal/` exists at the root; a repository with neither layout is left alone | code; the spec says so since phase 3 | The stamp's one job is the once-per-repository rule, which is consulted only where something old exists; the case it guards is an old branch checked out after the move (pinned by `test_a_moved_repository_is_stamped_so_an_old_branch_is_not_moved_again`). Stamping every repository the plugin ever opens would list them all in `~/.claude/specseal/root-migrated` for nothing |
| What counts as dirty | S6 said *`git status --porcelain -- .specseal specs` prints anything*. Code ignores an entry whose index column is `R` or `D` with a clean worktree column | code; the spec says so since phase 3 | S7 is unreachable otherwise: a stopped run leaves staged renames whose SOURCE paths are under the old roots, so the literal rule refuses every resume as dirty. A staged addition or modification, anything untracked, and anything with a worktree change still refuse (`test_a_staged_edit_under_the_old_roots_is_work_in_progress_too`) |
| `--follow` on the README | S1: *`git log --follow` on any moved file reaches its history*. `seal/README.md` does not: rewritten whole from the template in the same commit, git pairs no rename | spec, knowingly not met for one file; S1 says so since round 1 | Q5 (a) chose the overwrite; the old text is in history under `.specseal/README.md`, and the file is plugin-owned. Every other moved file follows |
| Which renames are excluded | S10: *never a renamed one*. Code excludes exact renames (`R100`) only; a rename carrying an edit is judged | code; S10 says so since round 1 | The prompt's own words, *a `routing.md` that the pull request only renamed*: an edit on the way over is the pull request's, and the check exists to read it (`test_a_declaration_the_pull_request_renamed_and_edited_is_judged`) |
| Two routing cases inverted | `tests/test_routing_is_recorded.py` pinned *writing a declaration creates no plugin home*; a declaration under `seal/specs/` creates `seal/`, which is the opt-in | code, with the two cases rewritten to pin the consequence | The design record makes the root the signal and puts the whole work item under it; the hazard those cases guarded (four gates switched on by answering a routing question) is answered by the `implement` skill's once-per-repo moment creating `seal/` on purpose (S14, phase 2) |
| `conftest.py#declare_routing` in phase 1 | `plan.md` puts the shared fixtures in phase 3 | one line moved forward | The S11 test files cannot pass while the fixture writes `specs/<item>/routing.md`, and the spawn prompt allows exactly that case; the rest of the fixture sweep stays in phase 3 |
| Which lines keep the old name | S15: *except the design record and its twin, and `hooks/root-migrate.py`* | code, with six line-level exceptions as well, each carrying a reason and each required to still have a line under it | `tests/test_handoff_outlives_the_merge.py` asserts the retired `.specseal/handoff` key is still named as history in both specifications; the marker text is Q2; the README says what nothing reads any more; `docs/flow.md` describes the move. Deleting those sentences to meet the literal clause would delete the reasons the clause exists for |
| Files outside `plan.md` row 2's list | the workflow, the templates, the skills, the three agents, four documents, `CONTRIBUTING.md`, `CLAUDE.md` | also `SECURITY.md` (one live sentence), five hook docstrings, `seal/README.md` (the template's copy) and four test files that pinned the old names | The row's own grep over `hooks/` expects `root-migrate.py` as the only hit, and a test that pins `.specseal/README.md` in the skill text cannot stay green while the skill says `seal/README.md`. No hook's code changed |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, repository-wide lint and the typecheck on this branch | the orchestrator's broad gate, once after the review rounds settle |
| `hooks/root-migrate.py` on Windows — porcelain's two columns and the `/`-joined pathspecs are written for it, nothing here ran there | CI's windows leg on the pull request |
| ✅ the hook under `dispatch.py session-start` rather than `main()` called directly | round 1's P7, re-run in the fix pass on an old-layout fixture with `HOME` redirected: the `systemMessage` line delivered, the marker written, `.specseal/` and `specs/` gone |
| a real repository other than this one, migrated at an actual session start after installing this branch's plugin | the repository owner, at the first session start in another opted-in repository |

## Not done

- The four private `git_dir()` copies (`implementer.py`, `review-skill-gate.py`, `session-lease.py`, `worktree-guard.py`) are not folded into `optin.git_common_dir`; `plan.md` names the fifth lookup and this phase adds it without removing one, because the four answer the GIT dir where this one answers the COMMON dir and the difference matters in a linked worktree.
- Prose paths in released round records, overviews and plans still read `specs/<id>/`, per the spec's Out list.
- `docs/review-handoff-protocol.md` carries one 89-column line after phase 2: a work item's path in backticks, which cannot be broken, in a file `tests/test_docs_line_wrap.py` does not cover.
- The READMEs' *coming up from 0.3.x* section describes a one-time move and has the same lifetime as `hooks/root-migrate.py`: nothing marks it as such in the README itself, so whoever deletes the hook once no repository is left to migrate has to know to delete the section. The fragment's S15 row says so; the README does not.
- The by-hand sequence in that section was run on a fixture, not on a repository that had actually used 0.3.x, and since round 1 a test reads the block out of each README and runs it on a copy of that fixture; the difference is only what else such a repository keeps under `.specseal/` and `specs/`, which the sequence's *anything else in there* step covers by hand.
- The hook and the by-hand block leave an ignored file under `.specseal/` where it is, and neither says so to the person; `.specseal/` holding only ignored files after the move is named in the spec's refusal table and nowhere a person reads.

## Fed back into the spec

Phase 3 rewrote three places in `spec.md` to what `hooks/root-migrate.py`
does, each marked here as *inferred during implementation* so a planner knows
it may be overturned:

- S6 — a staged rename or deletion with a clean worktree column is not dirty,
  and the reason (a resume has to see past its own earlier steps) is in the
  row; the four cases that pin it are named in its *Verifiable how* cell.
- The refusal table — the *clean, moved* row lists the shapes the printed line
  takes (a missing old home, a count of one, a foreign entry under `specs/`);
  the *scratch* row says it is tested before dirtiness; the *move failed* row
  says no ledger row is re-pointed until every unit has moved; the *nothing
  old left* row stamps only a repository that has `seal/`; and a sentence
  under the table gives the order the rows are tested in.
- "The move, in order", step 3 — a template that cannot be read leaves the
  moved README as it was.

Round 1's fix pass fed back the rest, each likewise *inferred during
implementation*:

- S1 — `git log --follow` reaches history on every moved file *except
  `seal/README.md`, rewritten from the template (Q5)*.
- S10 — a declaration the pull request only renamed is *an exact rename; one
  carrying an edit is judged*.
- "The move, in order", step 4 — every other *tracked* entry; the units are
  what `git ls-files` reports, an ignored file stays, and when git cannot
  answer the listing stands in and the dirty test refuses.
- Step 6 — `specs/<id>/` where `<id>` is a work item; a row citing an entry
  that stays, stays with it.
- The refusal table — the *clean, moved* row says `.specseal/` may remain
  holding only ignored files; the *move failed* row names the two shapes
  that do not resume by themselves and the line they end with; a new row for
  every unit moved and the re-point failed.
