# Feature Specification: the tree that must stay clean has no way to opt in

<!-- seal/specs/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in/spec.md —
WHAT this work delivers and how we'll know. `docs/one-root-by-lifetime.md`
outranks this file; it is cited, not restated. The design is decided there;
the clauses below are that design as things a test can check. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/one-root-by-lifetime.md` §"The opt-in signal is the root itself, wherever the mode put it" | opted in means `seal/` exists at the mode's location, `<repo>/seal/` first and `.git/seal/` second; whichever exists says both "on" and which mode; no config key; cannot tell means not opted in |
| §"What first setup asks" | the once-per-repo moment in the `implement` skill becomes the question: one `AskUserQuestion`, two options, shared first as the default, each saying what it does; a repository with `seal/` at either place is never asked |
| §"Shared or local" | the table of what each mode gives up; local mode under the COMMON git dir so linked worktrees share it, never a commit candidate, no `.gitignore` line; the hygiene workflow installed in shared mode only; switching is a move and a commit |
| §"Decided after the thread" | the opt-in is the folder; nothing is deleted before `settle` |
| §"Decisions left open" row 4 | the `scratch` opt-out — closed by #79 as `.git/specseal-scratch`, which this work keeps (the record still lists it open; Q8) |
| `docs/review-handoff-protocol.md` §"Why the records moved a second time" | no second address ships as a fallback; here the second place is a MODE, read in a fixed order, and a repository with both is shared |
| `CONTRIBUTING.md` §"What a change to a gate must carry" | a test seen red, a stated fail direction, a prompt budget, platform honesty — S10, S11, S12 answer them |
| `CLAUDE.md` §"The goal a design is chosen against" | one question, at first setup, in the batch; no hook asks anything new |
| `tests/test_gates_do_not_fail_open.py` (house rule) | a reader that cannot decode answers "" rather than raising, and "" reads as not opted in |
| issue #80 "Done when" | the acceptance list; S1–S6 cover its four lines |

Owner decisions taken 2026-09-02, before this frame (recorded in
`questions.md` as answered): shared mode installs the hygiene workflow from
a new `templates/hygiene.yml` that installs the plugin at its marketplace
tag and runs the pull-request checks, written to
`.github/workflows/hygiene.yml` at the shared first setup only when absent;
local mode installs nothing; every other decision takes the record's
default, and where the record is silent the default named in `questions.md`.

## Scope

**In.**

- The CREATE side of local mode: the `implement` skill's bootstrap creates
  the root at the chosen place, and everything else that joins a path under
  the root resolves it through `optin.home()` (S6).
- The first-setup question (S4) and what each answer installs (S5).
- `templates/hygiene.yml` for a user repository's CI, and the sentence in it
  that says why local mode has none (S5, S7).
- `templates/seal-README.md` naming both places; the two READMEs, the
  `implement` skill, the two agents, `CONTRIBUTING.md`,
  `docs/branch-and-release.md`, and the record's decided-after table (Q8).
- A local-mode fixture in `tests/conftest.py`, and the tests each clause
  names.
- The record: `seal/ledger/<id>.md`, the closing memo, the changelog fragment.

**Out.**

- `seal export` / `seal import` (#81). Switching modes is a documented move
  (S8), not a command.
- `seal/config.md` (#82). Nothing here reads a key.
- `settle` (#83), and the orphan-branch design (#85).
- Changing what `root-migrate.py` moves or where it moves it. A repository
  on the old layout is shared by definition: `.specseal/` was committed, so
  the tree already carried the plugin's files, and the move keeps them in
  the tree (S9).
- This repository's own mode. It is shared and stays shared; nothing here
  creates `.git/seal/` in SpecSeal (S13).
- Running the hygiene checks in local mode by any other means (a local
  runner, a pre-push hook). The record says CI cannot run there and this
  work says so in the template (S7).

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | **Where the root lives, and no key** | Given a repository, when a hook asks `optin.home()`, then the answer is `<repo>/seal/` if that directory exists, else `<git-common-dir>/seal/` if that exists, else `""`. Nothing else is read: no git config key, no marker, no environment variable. A repository with both is shared | `tests/test_optin_home.py` — `test_new_home_opts_in`, `test_the_git_directory_is_the_second_place`, `test_the_shared_root_wins_when_both_exist`, `test_neither_means_out` (green at d877282, **executed** by this frame); a new case asserting `optin.py` reads no `git config` and no `SPECSEAL_*` variable for the mode (`grep` of the module source for `config` and `environ` finds nothing) |
| S2 | **`.git/seal/` is under the COMMON git dir, so linked worktrees share it** | Given a main tree with `.git/seal/` and a linked worktree of it (whose `.git` is a FILE), when a hook runs in the worktree, then `optin.home()` resolves to the main tree's `.git/seal/` — `git_common_dir` asks `git rev-parse --git-common-dir` when `.git` is not a directory and joins the answer, so a relative reply and an absolute one both land | new case in `tests/test_optin_home.py`: `git worktree add`, `local_home(main)`, `os.path.samefile(optin.home(str(other)), main/.git/seal)`; the existing `test_the_common_git_directory_is_asked_of_git_for_a_linked_worktree` covers the resolver |
| S3 | **Local mode is never a commit candidate and needs no `.gitignore` line** | Given a local-mode repository with a routing declaration, round records and a ledger fragment under `.git/seal/`, when `git status --porcelain` and `git add -A` run, then nothing under the root is listed or staged, and the repository has no `.gitignore` entry for it — git never lists its own directory | new case in `tests/test_optin_home.py`: write those files, assert `git status --porcelain` is empty, `git add -A` then `git diff --cached --name-only` is empty, and no `.gitignore` exists |
| S4 | **First setup asks once, in the `implement` skill's bootstrap, and never again** | Given a repository with `seal/` at neither place, when the `implement` skill reaches its bootstrap, then it asks ONE `AskUserQuestion` with two options, **shared** first as the default and **local** second, each option saying what it does (shared: creates `<repo>/seal/` in the tree, which the routing commit already mandated carries, and installs the hygiene workflow; local: creates `$(git rev-parse --git-common-dir)/seal/`, installs nothing, touches nothing in the tree), then the parity question as today, after it. Given `seal/` at either place, the question is not asked; the mode is read from where the folder is. The bootstrap creates the root at the COMMON git dir in a linked worktree too — the skill spells the path as `$(git rev-parse --git-common-dir)/seal/`, never `.git/seal/` literally, because `.git` is a file there | new `tests/test_first_setup_asks_once.py`: reads `skills/implement/SKILL.md`'s bootstrap section and asserts (a) both option names in that order, (b) each option's sentence names what it creates and what it installs, (c) `git rev-parse --git-common-dir` is named, (d) the never-again sentence names both places, (e) the parity question follows the mode question, (f) the 0.4.0 sentence "creates the root at `<repo>/seal/` and nowhere else" is gone. `tests/test_the_set_a_work_item_always_has.py` still green |
| S5 | **Shared installs the hygiene workflow from a template; local installs nothing** | Given the shared answer, when the bootstrap runs, then `.github/workflows/hygiene.yml` is written from `templates/hygiene.yml` only if that path is absent — an existing file is never overwritten and the skill says so. The template installs the plugin at its marketplace tag — `git clone --depth 1 --branch v<version>` of the plugin repository into `$RUNNER_TEMP/specseal`, the version pinned from the installed `plugin.json` at setup; *inferred during implementation* (Q9): `actions/checkout` refuses a `path:` outside the workspace, so the clone is a `run:` step and not that action — fetches `+refs/pull/*/head:refs/remotes/pull/*/head`, and runs the two shipped checks: `skills/verify/scripts/unverified_check.py --baseline origin/<base> seal/specs/` and `skills/code-review/scripts/chain_check.py --baseline origin/<base>`. The rows of this repository's `hygiene.yml` that do NOT travel: the version bump (reads `plugin.json`), the two `--check` gathers (read `.github/scripts/`, which does not ship), and the both-READMEs warning (this repository's language policy). Given the local answer, nothing is written under `.github/` | `tests/test_first_setup_asks_once.py`: the template names both scripts, the refspec, `v<version>`, the plugin repository and `RUNNER_TEMP`, and none of `plugin.json`, `gather_changelog`, `fold_ledger`, `README.ko.md`; the skill text names the template, "only when absent", and "local installs nothing". `tests/test_no_real_identifiers.py`, `tests/test_no_document_names_the_old_roots.py` (both scan `templates/`), `tests/test_the_release_check_watches_what_ships.py` green |
| S6 | **In local mode every gate resolves under `.git/seal/`** | Given a local-mode repository, when each reader below runs, then it finds what it reads under `optin.home()`. Per reader: `commit-review-gate.py` — reads the declaration through `routing.declared` → `home_at`: resolves already; `DOC_ROOTS` classifies paths in a diff, and a diff never holds `.git/…`, so it is unchanged and correct; its prompt text names `seal/specs/<id>/routing.md` and must spell the path under the resolved root instead. `routing.py` — `home_at`: resolves (0.4.0). `implementer-notice.py`, `review-history-guard.py` — through `routing.for_branch` / `item_dir`: resolve; the path they print is `os.path.relpath(item, top)`, which reads `.git/seal/specs/<id>/…` in a main tree and a `../` path from a linked worktree, both typeable. `review-skill-gate.py`, `implementer-mark.py`, `version-check.py` — `opted_in` only, join nothing. `evidence-advisor.py` — globs `seal/ledger.md`, `seal/ledger/*.md` under the REPOSITORY root: **joins**, must glob under `optin.home()`. `ledger-migrate.py` — `LEDGER_GLOBS` under the repository root: **joins**, the same fix. `evidence_check.py` — default patterns and the parity path (`anchors_in_parity_repo`) are joined under its `root` argument: **joins**; resolved per Q2. `root-migrate.py` — moves into `<repo>/seal/` only, by design (S9). `chain_check.py` — `git ls-tree HEAD -- seal/specs/`: reads git, cannot see `.git/seal/`, and is CI-only (S7). `unverified_check.py` — path arguments plus `--baseline <ref>`: CI-only (S7). `gather_changelog.py`, `fold_ledger.py` — this repository's release scripts, not shipped; a release is a pull request and this repository is shared | new `tests/test_local_mode_resolves_under_the_git_dir.py`, one case per joiner in a local fixture: the commit gate stays silent with a declaration at `.git/seal/specs/<id>/routing.md` naming the branch and fires without one, and its stop text names the resolved path; `implementer-notice` names `.git/seal/…`; `evidence-advisor` reports a BROKEN row from `.git/seal/ledger.md`; `ledger-migrate` migrates a pre-anchor ledger under `.git/seal/`; `evidence-check .` **executed** in a local fixture finds the ledger (output in the fragment) |
| S7 | **The hygiene checks cannot run in local mode, and the template says so** | Given a local-mode repository, when its owner asks why CI is not checking rounds, then the answer is in the template's header comment: the checks read committed files (`git ls-tree HEAD`, `--baseline <ref>`), local mode commits none, so a workflow there would go green having examined nothing — `chain_check.py` exits 0 for a repository that declared nothing and `unverified_check.py` exits 2 for a path that is nowhere. The header names the switch (S8) as the way to get CI | `tests/test_first_setup_asks_once.py`: the template header names local mode, "examined nothing", and the switch. **Read**, not executed: `chain_check.py:789` prints "check examined nothing" and exits 0; `unverified_check.py:611-627` returns 2 for a missing path |
| S8 | **Switching modes is documented, not automated** | Given either mode, when the person wants the other, then the READMEs' *Shared or local* section gives the move: local → shared is `mv "$(git rev-parse --git-common-dir)/seal" seal`, `git add seal`, commit; shared → local is `git rm -r --cached seal`, `mv seal "$(git rev-parse --git-common-dir)/seal"`, commit the removal — and the hygiene workflow is installed or removed by hand. The hooks need no restart: the next command reads the folder where it is. Export/import is #81 and is named as such | `tests/test_first_setup_asks_once.py`: both READMEs carry the section with both moves and "#81"; `tests/test_docs_line_wrap.py` on the READMEs; the two READMEs in one commit |
| S9 | **What `root-migrate.py` does beside `.git/seal/`** | **Read at d877282**, `hooks/root-migrate.py#main`: with nothing old (`moves(root)` empty) it stamps the marker only when `<repo>/seal/` is a directory, so a local-mode repository with nothing old is silent and never stamped, and re-lists at every session start. With an old `.specseal/` or `specs/<id>/` present it moves them into `<repo>/seal/` regardless of `.git/seal/`, because a repository on the old layout committed the plugin's files and is shared by definition; after the move `<repo>/seal/` wins by S1. This work changes one thing (Q3 default): with nothing old, stamp when `seal/` exists at EITHER place, so that checking out an old branch later in a local-mode repository does not stage a `<repo>/seal/` the person chose not to have. Everything else is unchanged | `tests/test_the_root_migrates_itself.py`, new cases: a repository with only `.git/seal/` says nothing and is stamped; a repository with `.git/seal/` and an old layout moves the old layout into `<repo>/seal/` with the existing message |
| S10 | **Fail direction of every new path** | Every path added here fails toward "not opted in" or "nothing written": `git_common_dir` answering "" (git absent, times out, or `stdout` decoded to `None`) makes `home_at` return "", and every gate does nothing; the checker with an unresolvable root reads `<root>/seal/` and prints "no evidence ledgers found", exit 0 — a CLI a person is watching, not a gate; the template is written only when absent, so a wrong answer never overwrites a workflow someone edited; the stamp rule (S9) stamps more, which is the quieter mistake — a missed move prints nothing, and the README's by-hand sequence is the way out. No gate blocks more than it did | `tests/test_gates_do_not_fail_open.py`: a new case sets `subprocess.run` to return `stdout=None` for `--git-common-dir` and asserts `optin.git_common_dir` returns "" and `optin.home` returns "" for a tree whose `.git` is a file; `tests/test_local_mode_resolves_under_the_git_dir.py`: a local fixture with `.git/specseal-scratch` keeps every gate silent |
| S11 | **Windows** | `.git` is a FILE in a linked worktree on every platform, and on Windows the path git answers uses forward slashes; `git_common_dir` asks git and normalises through `os.path.normpath(os.path.join(root, out))`, and every path printed to a person is built with `os.path.join`. Nothing here inspects a process or a drive letter | CI's windows leg runs S2, S3 and S6 (`.github/workflows/test.yml`, the matrix); the frame did not run it — **unverified** until the pull request, answered by CI |
| S12 | **Prompt budget** | This work adds exactly one question, at first setup, once per repository, in the batch the `implement` skill already asks (the parity question sits beside it). No hook asks anything new; no hook asks anything more often. A repository with `seal/` at either place meets the bootstrap and is not asked | `tests/test_first_setup_asks_once.py` (S4 (d)); `grep -rn AskUserQuestion hooks/` finds nothing new (read) |
| S13 | **This repository stays shared** | `seal/` is at the root of SpecSeal and `.git/seal/` is never created here; the existing hygiene test is unchanged | `tests/test_release_hygiene.py#test_this_repository_has_one_root_laid_out_by_lifetime` green and untouched |
| S14 | **The template README names both places** | `templates/seal-README.md` (and this repository's `seal/README.md`, rendered from it) says the root lives at `<repo>/seal/` in shared mode and at the common git dir in local mode, that its presence at either place is the opt-in, what local mode gives up (no CI, no other machine), and how to switch (S8) | `tests/test_first_setup_asks_once.py`: both files carry "git rev-parse --git-common-dir" and the word "local"; `tests/test_the_root_migrates_itself.py#test_the_readme_is_rewritten_from_the_new_template` green — the migration hook writes this template, and a migrated repository is shared, so the text must read correctly for both |

## Data & interfaces

- `hooks/optin.py` — `home_at(root)`, `home(cwd)`, `git_common_dir(root)`:
  signatures unchanged. No new constant; the mode is not a value anything
  returns.
- `hooks/evidence-advisor.py#failing_rows`, `hooks/ledger-migrate.py#ledgers`:
  glob `ledger.md` and `ledger/*.md` under `optin.home()` instead of under
  the repository root; `docs/**/_evidence.md` stays under the root.
- `skills/evidence-check/scripts/evidence_check.py#main`: the default
  patterns and `anchors_in_parity_repo` resolve `seal/` through a resolver
  chosen in Q2. `--ledger` is unchanged and overrides it.
- `hooks/commit-review-gate.py`: the stop text names the declaration path
  under the resolved root, relative to the repository (`os.path.relpath`).
- `hooks/root-migrate.py#main`: the stamp on "nothing old" reads either
  place (Q3).
- `templates/hygiene.yml` — new. Header comment (S7), one job, four steps:
  checkout with `fetch-depth: 0`, checkout of the plugin at its tag, the
  `refs/pull` fetch, the two checks.
- `tests/conftest.py`: `local_home(repo)` helper creating
  `<common>/seal/`; `declare_routing(repo, item, review, home=None)` writing
  under `home` when given; both `make_repo(path, opted_in)` helpers gain a
  `local=False` keyword.
- `skills/implement/SKILL.md` §Bootstrap: the question, what each answer
  creates and installs, the common-dir spelling, and one definitional
  sentence for sessions (Q1): every `seal/…` path in this plugin's skills
  and agents means `<repo>/seal/` where it exists and
  `$(git rev-parse --git-common-dir)/seal/` otherwise.

## Open questions → questions.md

Q1–Q8 in `questions.md`, each with a default the orchestrator approves.
