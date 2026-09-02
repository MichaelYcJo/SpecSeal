# Implementation Plan: the tree that must stay clean has no way to opt in

Pre-approved 2026-09-02 by the repository owner: every row of `questions.md`
takes its default, and the orchestrator's spawn of phase 1 is the approval.

<!-- seal/specs/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in/plan.md —
HOW, in phases. This is the Design Gate's artifact: the work changes where
every gate finds the root and what a skill asks, so approval of this plan is
the gate. Each phase is sized for one smith spawn; the spawn that wrote this
built nothing. -->

## Summary

The READ side of local mode shipped in 0.4.0: `optin.home_at` looks at
`<repo>/seal/` and then `<git-common-dir>/seal/`. This work adds the CREATE
side and finishes the joiners. Three readers still spell `seal/` under the
repository root (`evidence-advisor.py`, `ledger-migrate.py`,
`evidence_check.py`) and one prints a path a session would type in the wrong
place (the commit gate); those move to the resolved root. The `implement`
skill's once-per-repo moment becomes the question — shared or local, shared
first — and the shared answer writes a hygiene workflow from a new template.
Three phases, one spawn each: the code and a local-mode fixture; first setup
and the documents; the record.

## Technical context

Coordinates are as of `d877282` on this branch. Every fact marked
*executed* was run by the framing spawn; the rest were read.

- `hooks/optin.py#home_at` — the two places, in order; `git_common_dir`
  answers a `.git` DIRECTORY without a process and asks git otherwise, and
  joins the answer so a relative and an absolute reply both land. **Executed**:
  `tests/test_optin_home.py` green at `d877282`, 31 cases, including the
  linked-worktree resolver case. Nothing here changes; S2 and S3 add cases.
- `hooks/routing.py#declarations` — `optin.home_at(root)` then
  `optin.WORK_ITEMS` under it; `WORK_ITEMS = "seal/specs"` at line 64 is
  the git-facing spelling `chain_check.py` lists a tree under. Every hook that
  reads a declaration goes through this: `commit-review-gate.py:843`
  (`routing.declared`), `implementer-notice.py:103,114`,
  `review-history-guard.py:148`. They resolve already.
- `hooks/evidence-advisor.py:111` and `hooks/ledger-migrate.py:67` — glob
  `seal/ledger.md`, `seal/ledger/*.md`, `docs/**/_evidence.md` under
  `optin.repo_root(cwd)`. Both already import `optin`; the fix is the join.
- `skills/evidence-check/scripts/evidence_check.py:1378-1382` — the default
  patterns under `root`; `:813` — `os.path.join(root, "seal", "parity.md")`.
  The module imports nothing from `hooks/`, because `evidence-ci` vendors it
  (`skills/evidence-ci/SKILL.md` step 3). Q2 (a): import `optin` by path
  when present, else `<root>/seal/`.
- `hooks/commit-review-gate.py:860,886` — the stop text spells
  `seal/specs/<work-item-id>/routing.md`. `top` and `git_dir` are in scope
  at `judge()`; `optin.home_at(top)` gives the root to make it relative to.
- `hooks/root-migrate.py#main` — the `if not units` block stamps only on
  `os.path.isdir(under(root, NEW))`. Q3 (a) reads either place there.
  `PREFIXES` and `moves()` write into `NEW` = `<repo>/seal/` and stay so.
- `skills/implement/SKILL.md:78-116` — the bootstrap section. Line 111,
  "This release creates the root at `<repo>/seal/` and nowhere else; the
  question of where it goes arrives with local mode", is the sentence this
  work replaces. The parity question at lines 103-108 stays after the new
  one. **Executed**: `grep -rn 'seal/README\|create.*seal/' skills agents
  templates` — the `implement` skill is the only creator of the root.
- `.github/workflows/hygiene.yml` — six steps; the two that ship with the
  plugin are `unverified_check.py --baseline origin/<base> seal/specs/` and
  `chain_check.py --baseline origin/<base>`, preceded by the
  `+refs/pull/*/head:refs/remotes/pull/*/head` fetch that `chain_check.py`
  needs to resolve a squashed round's `Target SHA`. The other four read
  `plugin.json`, `.github/scripts/` and `README.ko.md`, none of which a
  user repository has.
- `templates/evidence-check.yml` — the model for a template's header: what
  it does, how to install it, what to change.
- `templates/seal-README.md` — "its presence at the repository root is what
  opts the repository into the workflow"; true of shared mode only.
  `hooks/root-migrate.py#rewrite_readme` writes this template into a
  migrated (shared) repository, so the text must read correctly there too.
- `tests/conftest.py#declare_routing` builds `repo / "seal" / "specs" /
  item`; `test_gate_judges_the_repo_it_commits_to.py:85` and
  `test_a_path_the_command_wrote_out.py:269` each define
  `make_repo(path, opted_in)` creating `seal/`. `test_optin_home.py` already
  has a `local_home(repo)` helper; phase 1 moves it into `conftest.py`.
- `tests/test_gates_do_not_fail_open.py` — the house rule: `stdout=None` from
  a decode failure must read as "" and never raise. `git_common_dir` has
  the same `subprocess.run` shape as `repo_root` and no case of its own.
- `tests/test_release_hygiene.py:523` — asserts `seal/` at this repository's
  root; unchanged (S13).
- `tests/test_no_document_names_the_old_roots.py` scans `templates/`,
  `skills/`, `agents/`, `docs/`, the READMEs, `CONTRIBUTING.md`,
  `CLAUDE.md`, `.github/workflows/`; `tests/test_docs_line_wrap.py` holds
  the READMEs, `CONTRIBUTING.md`, `agents/warden.md`,
  `skills/code-review/SKILL.md` to 88 columns. Phase 2 writes into both sets.
- The suite runs as `pytest tests/ -q -n auto` on three platforms
  (`.github/workflows/test.yml`); the windows leg is the only place S11 is
  checked.

**What breaks in six months.** Named so a reader can weigh it.

- A local-mode repository has no CI checking its rounds, and nothing tells
  a reviewer that. The template's header and the README say so; the
  pull request into such a repository is green on its own terms. That is the
  trade the record accepts and #81's reminder is the only nudge planned.
- A session that loads no skill and reads no agent file finds nothing that
  says where `seal/` is in local mode, except the hooks' own messages — which
  is why Q5 moves the commit gate's path to the resolved root rather than
  relying on the Q1 sentence alone.
- The vendored checker (`tools/evidence_check.py` in a user repository)
  reads `<root>/seal/` only. It runs in CI, which is shared mode; a person
  who runs the vendored copy by hand in a local-mode repository sees "no
  evidence ledgers found" and a green exit. `bin/evidence-check` runs the
  plugin's copy and resolves.
- The hygiene template pins a tag. A repository that never re-runs setup
  checks its rounds with the 0.5.0 checker forever, which is what pinning
  means; the header says how to move the line.
- `<repo>/seal/` and `.git/seal/` both present reads as shared, silently.
  The state arises from a half-done switch (S8); the README's sequence
  removes the old place last so the window is one command wide.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. The root at the common git dir, found by presence, chosen once at first setup** | a half-done switch leaves both places and the repository reads as shared; a session that loads nothing does not know where `seal/` is (Q1, Q5 answer it); no CI in local mode | **chosen** — the record's decision, and the two-place read already ships |
| B. A git config key (`specseal.mode`) beside the folder | says what the folder's place already says; every gate parses a config to answer a directory test; a clone with the key and no folder is a state with no meaning | rejected, `docs/one-root-by-lifetime.md` §"The opt-in signal is the root itself" |
| C. A gitignored `<repo>/seal/` | absent in every linked worktree, which is the outage the owner hit and the reason the ticket exists | rejected, §"Why local mode is under `.git/` and not gitignored" |
| D. `<repo>/seal` as a symlink into `.git/seal/` | the link is a commit candidate, git tracks it as a blob, and `root-migrate.py` already refuses a symlinked root for that reason | rejected |
| E. Ask the mode from a hook the first time a gate fires | a question at minute thirty, from a hook, in a session that may have nobody at the keyboard; the batch rule exists to end that | rejected, `CLAUDE.md` first goal, `CONTRIBUTING.md` prompt budget |
| F. Vendor the two checks into the user repository (the `evidence-ci` pattern) | `chain_check.py` loads `hooks/routing.py` and `hooks/optin.py` beside it; three files drift together and each re-run of setup diffs three | rejected, Q0-a (b) |
| G. Run the hygiene checks in local mode from a pre-push hook against the working tree | the checks read `git ls-tree HEAD` and `--baseline <ref>`; rewriting them to read a tree that is not committed is a second reader of every record, forever | rejected, out of scope |
| H. One `bin/seal-home` for sessions | two more shipped files and a spelling nobody outside the plugin recognises, for a rule one sentence states | not chosen, Q1 (b) |

## Phases

Vertical slices — each phase ends with something runnable and verified, and
each is one smith spawn. The test scope per phase is the files the phase
touches, run as one command; the full suite runs once after the review
rounds settle. Phase 1 is kept to code and tests only so the spawn ends
under ~250k context (#89 measured 347k for #79's phase 1, which carried the
move as well).

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The joiners and the local-mode fixture.** `tests/conftest.py`: `local_home(repo)` (creates `<common>/seal/`, works from a linked worktree), `declare_routing(..., home=None)`, both `make_repo` helpers with `local=False`. Code: `hooks/evidence-advisor.py` and `hooks/ledger-migrate.py` glob `ledger.md` and `ledger/*.md` under `optin.home()` (S6); `skills/evidence-check/scripts/evidence_check.py` resolves the defaults and the parity path per Q2 (a); `hooks/commit-review-gate.py` stop text names the declaration under the resolved root (Q5, S6); `hooks/root-migrate.py` stamps on either place when nothing is old (Q3, S9). Tests: `tests/test_optin_home.py` (S1 no-key case, S2, S3); new `tests/test_local_mode_resolves_under_the_git_dir.py` (S6 per joiner, S10 scratch); `tests/test_the_root_migrates_itself.py` (S9 two cases); `tests/test_gates_do_not_fail_open.py` (S10 `git_common_dir`); `tests/test_evidence_check.py` (Q2: the plugin copy resolves, a copy with no `hooks/` beside it reads `<root>/seal/`). Each new test seen red first (`CONTRIBUTING.md`) | those six test files green in one `pytest … -q -n auto`; `evidence-check .` **executed** in a local fixture with a ledger under `.git/seal/` and its output kept for the fragment; `ruff check` and `ruff format --check` on the touched files | `ca77fc7` — the fixture is in `8d05b00`, the joiners in `018f0c2`, the stamp in `529976d`, the checker in `ca77fc7` |
| 2 | **First setup and the documents.** `skills/implement/SKILL.md` §Bootstrap: the question (S4, Q6, Q7), what each answer creates and installs (S5), the common-dir spelling, the Q1 sentence in the layout section; `agents/smith.md` and `agents/warden.md` carry the Q1 sentence once. `templates/hygiene.yml` new (S5, S7, Q4). `templates/seal-README.md` and this repository's `seal/README.md` re-rendered (S14). `README.md` and `README.ko.md` together, in one commit: the gates table's opt-in column, a *Shared or local* subsection under *First run* with the switch (S8). `CONTRIBUTING.md` (the template ships), `docs/branch-and-release.md` (the hygiene workflow is a template a user repository installs), `docs/one-root-by-lifetime.md` and its `.ko.md` twin (Q8). New `tests/test_first_setup_asks_once.py` (S4, S5, S7, S8, S12, S14) | that test and `tests/test_docs_line_wrap.py`, `tests/test_no_document_names_the_old_roots.py`, `tests/test_no_real_identifiers.py`, `tests/test_the_set_a_work_item_always_has.py`, `tests/test_release_hygiene.py`, `tests/test_the_release_check_watches_what_ships.py`, `tests/test_the_root_migrates_itself.py` (the README-template case) green in one command; `git show --stat` of the READMEs' commit read | `3d69594` — the test, red at 7e44106, is in `96c7402`, the skill and agents in `d962cf8`, the template in `2af85e8`, the root README in `2eba4be`, the READMEs in `32e178c`, the guides and the record in `3d69594` |
| 3 | **The record.** `seal/ledger/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in.md` with the executed rows from phases 1 and 2 (the `evidence-check` output, the fixture, each joiner's coordinate); `overview.md` (divergences from the record found by the code, S7 and S9; the S11 windows row as unverified with CI as the answerer); `changelog.md` final; `questions.md` rows fed back per Q8; this Status column | `evidence_check.py --strict .` at 0 broken on this repository; the phase-1 and phase-2 test files green in one command; the fragment's rows opened against the code | `d86548e` — the fragment (17 rows), the memo, S5 rewritten to the clone, Q9 answered, the changelog's final wording, and the 19 re-hashed rows of `seal/ledger.md` in `d86548e`; `--strict .` at `282 ok · 0 drifted · 0 broken`, the ten test files 188 passed |

This table is also where the work records how far it got. **Status is empty,
or the commit that closed the phase.** Feature branches squash here, so
these commits stop resolving at the merge, and a rebase during the work
orphans them earlier; nothing measures from this column.

## Operational impact

- **A new question at first setup, once per repository**, in the batch the
  `implement` skill already asks. No hook asks anything new (S12).
- **A new file in a user repository's tree, in shared mode only**:
  `.github/workflows/hygiene.yml` from `templates/hygiene.yml`, written only
  when absent. It pins the plugin's tag; the header says how to move it.
- **A new place on disk, in local mode only**: `<git-common-dir>/seal/`.
  Nothing under `.git/` is committed, and a re-clone starts empty; #81 is
  the copy.
- **A behaviour change in the migration hook**: a repository whose root is
  at either place is stamped as moved when nothing old is left (S9). A
  repository still carrying an old layout is moved into `<repo>/seal/` as
  before.
- **`evidence-check`'s defaults resolve the root** when the plugin's copy
  runs; the vendored copy is unchanged in behaviour (`<root>/seal/`).
- **The version moves at the release**, not here: the pull request lands on
  `release/v0.5.0` and `plugin.json` is left alone.
- No new dependency. Everything is stdlib and `git`.
