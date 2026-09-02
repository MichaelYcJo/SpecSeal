# 1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in — overview

<!-- The closing memo (implement skill, step 4). Written by phase 3 from the
executed facts of phases 1 and 2. Not a summary of the work: `git diff
--stat` holds the file list and the diff holds the detail. Only what the diff
cannot show goes here. Facts that must outlive this work item are in
`seal/ledger/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in.md`,
not here. -->

📋 implement applied
· spec:     `docs/one-root-by-lifetime.md` §"The opt-in signal is the root itself, wherever the mode put it", §"What first setup asks", §"Decided after the thread"; `spec.md` S1–S14 and the Data & interfaces list; `plan.md` alternative A, "What breaks in six months" and the Phases table; `questions.md` Q0-a–Q9; `changelog.md`; `seal/follow-up.md` (holds no items); `CLAUDE.md` §"A change writes fragments, never the shared file"
· evidence: `seal/ledger/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in.md`, 17 rows — 4 for the root at either place, 6 for the joiners, 6 for first setup and the documents, 1 for what phase 3 fed back; hashes written by `evidence_check.py --reverify .`, never typed. In `seal/ledger.md`, 19 rows whose anchors phases 1 and 2 had changed (`root-migrate.py#main`, the advisor and migration hooks, the gate's `judge`, the checker's `cross_repo_intent` and `main`, the skill's bootstrap section, the three fixtures, one routing assertion) were re-read and re-hashed, their claims still holding; two were edited: the §1788331011 S12 row lost its `hooks/ledger-migrate.py#LEDGER_GLOBS` anchor, a unit #80 removed (dropped, not re-pointed; the new claim is this fragment's S6 row), and its S14 row now says the mode question comes before the parity question
· verified: see the fragment — every row Executed except the S5 feedback row, which says Read, and the runner half of the template row, which says Not executed; phase 3 re-ran in a scratch fixture the `evidence-check .` output of phase 1, git's exit 128 for a pathspec outside the tree, the two CI checks' exits for a repository with no records, and the README's two switch commands; the ten phase-1 and phase-2 test files in one command, 188 passed; `evidence_check.py --strict .` at `282 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, exit 0, after the fragment's hashes were written; `unverified_check.py seal/specs/` reads this memo (4 open); `gather_changelog.py --dry-run --version 0.5.0` picks the fragment; no `.py` changed, so ruff had nothing to run on; the full suite, lint and typecheck deliberately not run — the broad gate runs once after the review rounds settle

## Why this work exists

A repository whose tree must not carry this plugin's files had no way to run
the workflow; after this, the root can live under the common git directory
instead of in the tree, first setup asks which once, and every hook, the
checker and the commit gate's own stop text find the root wherever it is.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| How the template puts the plugin on the runner | S5 and Q4 said *an `actions/checkout` of the plugin repository at `ref: v<version>` … into `${{ runner.temp }}`*. `templates/hygiene.yml` runs `git clone --quiet --depth 1 --branch v<version> … "$RUNNER_TEMP/specseal"` in a `run:` step | code; S5 says so since phase 3 (Q9) | `actions/checkout` resolves `path:` under `GITHUB_WORKSPACE` and refuses one outside it, so the two halves of the spec's sentence could not both hold; the plugin has to land outside the tree in a work item whose point is that the tree carries nothing extra. Found by reading the action, not by running the workflow — the Not verified row below |
| What the migration hook's notice promises in local mode | `hooks/ledger-migrate.py`'s docstring and notice say the write is *fully visible in `git diff`, with the old text safe in git history* and end *review the diff and commit*. Under `.git/seal/` nothing is in a diff and nothing reaches history: the rewritten ledger is the only copy | code left as it is; recorded here | Phase 1 changed the hook's globs and `dirty()` (S6) and nothing else, per `plan.md` row 1. The sentences are true of shared mode, which is every repository that had a ledger before this release; a local-mode ledger is new in 0.5.0 and this is its first migration path. The rewrite is still deterministic and all-or-nothing per row, and #81's export is the copy a local root has. Whether the notice should say something different in local mode is a wording decision for the owner, named in the pull request body |
| The design record's own text | §"Shared or local" said the hygiene workflow *would refuse a pull request with no round records* in local mode; `chain_check.py` exits 0 for a repository that declared nothing and `unverified_check.py` exits 2 for a path that is nowhere, so it would go green having examined nothing. §"Decisions left open" still listed the `scratch` opt-out, which #79 closed as `.git/specseal-scratch` | the record was corrected in phase 2 (Q8), in both editions, and the four decisions of this work item were added to §"Decided after the thread" | The record is the policy `spec.md` cites, and a policy the code contradicts gets fixed rather than followed (`implement` §1). Phase 3 executed the two exits the correction rests on |
| The stamp when nothing old is left | S9 as read at `d877282`: the hook stamps only when `<repo>/seal/` is a directory. Code stamps when `seal/` is a directory at either place | code; S9 said so from the frame (Q3 (a)) | Not a divergence from the spec as written, recorded because it is the one behaviour change in a hook that existed before this work: a local-mode repository that later checks out a branch carrying `.specseal/` is no longer moved into the tree it chose to keep clean |

## Not verified

| Item | Who must answer |
|---|---|
| S11, Windows — `git_common_dir` normalises git's forward-slash answer and every printed path is built with `os.path.join`; nothing here ran there | CI's windows leg at the pull request |
| Q9, the hygiene template on a runner — read against the action's documentation and the two scripts' exits, never run as a workflow; whether `git clone` into `$RUNNER_TEMP` and the two `python3 "$RUNNER_TEMP/specseal/…"` steps run green on a shared-mode repository | the repository owner, at the first shared-mode repository whose setup writes `.github/workflows/hygiene.yml` and opens a pull request |
| `evidence-check .` by CLI from a linked worktree — the worktree guard stops `git worktree add` on a session's command line, including for a scratch fixture, and it was not overridden; the shape is covered through `subprocess` in `tests/test_local_mode_resolves_under_the_git_dir.py` and `tests/test_optin_home.py`, and the stop text's `../` path by `test_the_stop_text_from_a_linked_worktree_is_a_path_a_person_can_type` | the repository owner, by hand in a linked worktree of a local-mode repository — `bin/evidence-check .` should list the main tree's `seal/ledger/` |
| the full suite, repository-wide lint and the typecheck on this branch | the orchestrator's broad gate, once after the review rounds settle |

## Not done

- `hooks/optin.py`'s docstring still says the common git directory is where
  local mode *will* keep the root — *"(#80; nothing in 0.4.0 creates it)"*.
  It was true when written and reads as a 0.4.0 statement; nothing in
  phases 1–2 touched the module's code, and the sentence is left for the
  release that moves the version to reword.
- `hooks/ledger-migrate.py`'s "review the diff and commit" notice and its
  docstring's "old text safe in git history" are left as they are under a
  local root — the divergence row above.
- `chain_check.py`'s line for a repository that declared nothing ends
  `routing.md todeclare`, a missing space, seen by phase 3's probe. Out of
  this work item's scope; one word in a shipped script, for the next change
  to that file.
- The two switch commands were executed on a fixture whose root held one
  file, not on a repository that had used either mode in earnest; the
  commit each direction ends with was not made there.
- Phase 1 did not execute `evidence-check .` from a linked worktree (the
  Not verified row above), and phase 3 did not either, for the same reason.

## Fed back into the spec

Phase 3 rewrote one clause in `spec.md` to what `templates/hygiene.yml` does,
marked *inferred during implementation* so a planner knows it may be
overturned:

- S5 — the template puts the plugin on the runner with
  `git clone --depth 1 --branch v<version>` into `$RUNNER_TEMP`, not with an
  `actions/checkout` step, and the test asserts the clone line rather than a
  `ref:` line (Q9).
