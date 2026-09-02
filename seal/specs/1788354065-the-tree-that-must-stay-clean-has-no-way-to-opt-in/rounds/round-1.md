# 1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in — review round 1

<!-- seal/specs/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in/rounds/round-1.md —
what this round of the review chain did, written by the review orchestrator
right after the report was verified. The first round of the run: it judged
all three phases of plan.md against origin/release/v0.5.0. -->

| Field | Value |
|---|---|
| Target SHA | 2ade74d (HEAD did not move during the round) |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | nobody — the fix pass had not run when this record was written; round-2 is the verifying round and sets this cell |
| Contract changes | `hooks/commit-review-gate.py#judge` (the hint is built inside the review arm only, through a new helper) → `hooks/commit-review-gate.py#declaration_hint`, `hooks/dispatch.py#GROUPS`; `hooks/ledger-migrate.py#dirty` (a path whose `relpath` raises is skipped) → `hooks/ledger-migrate.py#main`; `hooks/ledger-migrate.py#main` (the closing sentence keyed on whether `home` is `<root>/seal`) → `hooks/dispatch.py#GROUPS`; `skills/code-review/scripts/chain_check.py#declared_for_this_branch` (one space in a printed line) → `templates/hygiene.yml`, `.github/workflows/hygiene.yml` |
| New units | `hooks/commit-review-gate.py#declaration_hint`; tests: `tests/test_gates_do_not_fail_open.py#test_the_commit_gates_hint_survives_a_root_with_no_relative_spelling`, `tests/test_local_mode_resolves_under_the_git_dir.py#test_the_ledger_migration_hook_survives_a_ledger_with_no_relative_spelling`, `#test_in_local_mode_the_migration_notice_does_not_promise_a_diff`, `#test_in_shared_mode_the_migration_notice_still_ends_with_the_diff`, `tests/test_first_setup_asks_once.py#COMMON`, `#TOP`, `#switch_block`, `#porcelain`, `#test_the_switch_block_lands_the_root_at_the_tree_root_from_a_subdirectory`, `#test_the_version_is_read_from_the_plugin_root_and_not_from_the_tree`, `tests/test_the_root_migrates_itself.py#test_a_stamped_local_mode_repository_leaves_an_old_layout_branch_alone` (planted f049003..50a6eda) |
| Needs a fix | yes — 🔴 1 (`commit-review-gate.py` relpath `ValueError` → fail-open), 🔴 2 (`ledger-migrate.py` the same exception), 🟡 3 (the switch commands depend on cwd), 🟡 4 (where the version is read); 🟡 5 closes with grounds or a sentence; ❓ 8 is the owner's |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | the commit gate's new hint path calls `os.path.relpath(home, top)` unconditionally, before the judgment; on Windows a linked worktree on another drive makes `ntpath.relpath` raise `ValueError`, `dispatch.py`'s `except Exception` swallows it, and empty output is an allow — a commit passes unjudged | `hooks/commit-review-gate.py#judge` (the `declaration =` block above `if optin.opted_in(cwd)`), `hooks/dispatch.py#run_gate` | fixed — 1f27eac | executed (P1, macOS with the exception injected): the exception leaves `main()`, stdout empty. Orchestrator opened both sites: confirmed. `tests/test_gates_do_not_fail_open.py` is the house rule. Fix: `try/except ValueError` → the absolute path; compute the hint only when the arm stands (🟢 6) |
| 🔴 2 | `ledger-migrate.py#dirty` builds `os.path.relpath(p, root)` in a comprehension; the same cross-drive shape raises out of `main()` at session start | `hooks/ledger-migrate.py#dirty` | fixed — 2078984 | executed (P1b). Orchestrator opened the site: unguarded. Fix: `except ValueError: continue` — another drive is outside the tree by definition |
| 🟡 3 | the READMEs' and the root README's switch commands are relative to the cwd: run from a subdirectory, `git rev-parse --git-common-dir` answers `../.git` and `mv … seal && git add seal` creates and stages `src/seal/`, after which neither place resolves and the repository is opted OUT | `README.md`, `README.ko.md` §Shared or local, `templates/seal-README.md`, `seal/README.md` | fixed — f53d615 | executed (P3): `A  src/seal/ledger/…`. Fix: both moves through `$(git rev-parse --show-toplevel)/seal`, "from the repository root" in the sentence above; the assertions in `tests/test_first_setup_asks_once.py` follow; the root README stays byte-identical to the template |
| 🟡 4 | the bootstrap says to read `version` from "the plugin's `.claude-plugin/plugin.json`" with no path: the session is in the user's repository and the file is in the plugin cache; a wrong read leaves `v<version>` in the workflow and CI's `git clone --branch` fails | `skills/implement/SKILL.md` §Bootstrap (the template paragraph), `README.md` §Shared or local ("copy the plugin's `templates/hygiene.yml` in") | fixed — f53d615 | read; `skills/update/SKILL.md` already spells `$CLAUDE_PLUGIN_ROOT/.claude-plugin/plugin.json`. Fix: the one-line `python3 -c` reading `$CLAUDE_PLUGIN_ROOT`, and `$CLAUDE_PLUGIN_ROOT/templates/hygiene.yml` in the README |
| 🟡 5 | in local mode the ledger-migrate line ends "review the diff and commit" and the docstring says the old text is safe in git history; under `.git/` there is no diff and no history — the rewrite is the only copy | `hooks/ledger-migrate.py#main` (the closing line), its docstring | fixed — 2078984 | read; overview.md had recorded it as a divergence for the owner |
| 🟢 6 | `optin.home_at(top)` now runs before `opted_in(cwd)` on every commit, one more git process in a linked worktree | `hooks/commit-review-gate.py#judge` | fixed — 1f27eac | read |
| 🟢 7 | `hooks/optin.py`'s docstring still says "where local mode will keep it (#80; nothing in 0.4.0 creates it)", false on this branch | `hooks/optin.py` (module docstring) | fixed — 4572d8f | read |
| ❓ 8 | phase 3 detached one of six anchors on §1788331011's S12 row in `seal/ledger.md` (`ledger-migrate.py#LEDGER_GLOBS`, removed in phase 1) and kept the row; CLAUDE.md says a row whose anchor a change removes is REMOVED, and says nothing about multi-anchor rows | `seal/ledger.md` §1788331011 S12 | fixed — 50a6eda | read |
| 🟢 9 | "the only directory this plugin adds to your tree" is half true: shared mode also writes `.github/workflows/hygiene.yml` | `README.md`, `README.ko.md` (the opt-in paragraph) | fixed — f53d615 | read |
| 🟢 10 | `chain_check.py`'s "examined nothing" line reads `routing.md todeclare`; the new template prints it in every user repository's CI | `skills/code-review/scripts/chain_check.py#declared_for_this_branch` | fixed — 4572d8f | read |

Axes judged clean this round (reviewer's grounds, reproduced by the orchestrator where marked executed): (a) resolution order, both places, `<common>/seal` as a file, `.git` file vs directory, relative vs absolute answers — pinned by six new `test_optin_home.py` cases; (b) every gate returns on `git_common_dir` "" except 🔴 1's path; (c) the stamp rule — P5 executed: a stamped local repository checking out an old branch moves nothing, stages nothing; (d) hint paths from a linked worktree with spaces are typeable (P6); (e) the template parses, `on: pull_request` only so `base_ref` always exists, `github.com` allowed by the identifier test; (f) the question text pinned by the test; (g) the switch both ways from the root leaves only `A`/`D` and no `.gitignore` (P3); (h) no hook stages from `.git/`; the checker's dynamic import needs both `../SKILL.md` and `../../../hooks/optin.py`; (i) marks are per-worktree (`--git-dir`), the root is common; `--reverify` on `.git/seal/ledger.md` is last-writer-wins across worktrees, which the design record accepts. S6's joiner list re-derived by grep: complete.

<!-- The orchestrator first cited `chain_check.py#committed_declarations` in
this record and in evidence-todo.md; no such unit exists. The line is in
`declared_for_this_branch`. The fix pass found it when `--strict` reported
the fragment row BROKEN, and both files say the real name now. -->

## Executed probes

| What was run | Result |
|---|---|
| 15 test files, `pytest -q -n auto` | 394 passed |
| `ruff check` + `format --check` on the 15 changed `.py` | clean |
| `templates/hygiene.yml` parsed with pyyaml | `on.pull_request.types` 5, steps 5 |
| P1 `os.path.relpath` → `ValueError` injected into the gate's `main()`, local fixture | the exception leaves `main()`, stdout empty → an allow |
| P1b the same injection into `ledger-migrate.py#main` | the exception leaves `main()` |
| P2 local fixture: `chain_check.py --baseline main` / `unverified_check.py --baseline main seal/specs/` | exit 0 / exit 2 (S7 confirmed) |
| P3 the README switch both ways from the root; then local → shared from `src/` | root: `A seal/…` → `D seal/…`, the ledger returns; subdirectory: `A  src/seal/ledger/…` |
| P5 a local root only → start → an old branch checked out → start | stamped, the second start silent, status empty, `.specseal/` untouched |
| P6 main tree and worktree with spaces in the path; the gate's hint typed as a declaration | `../../a dir/main tree/.git/seal/specs/<work-item-id>/routing.md`; the gate silent afterwards |
| P7 `--git-dir` vs `--git-common-dir` in a linked worktree | per-worktree vs common |
| `evidence_check.py --strict .` / `unverified_check.py seal/specs/` / `chain_check.py --baseline origin/release/v0.5.0` | 282 ok · 0 broken / 14 · 32 · 15 · 0 / this item's `rounds/` named as holding no record |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

first round — nothing inherited.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ❓ 8 whether CLAUDE.md's REMOVED rule should say what a multi-anchor row does | the PR body (the orchestrator took the rule as written) | the repository owner |
| S11 Windows (the cross-drive shape of 🔴 1 is not on CI's windows leg either — a monkeypatched test pins it on every platform) | the PR's CI and the planted test | CI / the fix pass |
| Q9 the template on a real runner | the first shared-mode repository's CI, or the owner | the owner |
| `--reverify` last-writer-wins on `.git/seal/ledger.md` across worktrees | this record only; the design record §"Shared or local" accepts it | nobody — recorded |
