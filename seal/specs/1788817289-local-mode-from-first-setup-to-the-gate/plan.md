# Implementation Plan: local mode from first setup to the gate

<!-- seal/specs/1788817289-local-mode-from-first-setup-to-the-gate/plan.md -->

## Summary

Four vertical slices, in the order a repository meets them: the preset that
sends a session to the mode question, the gate that names a root nobody chose
a mode for, the record tool that refuses a local-mode item, and the check that
reports a declaration missing while it sits there. Each slice ends with a
case seen red first.

The build order is the reverse of that — #225's two halves first, because
they are the smaller change and their tests need no gate wiring, and #151's
two after. Nothing in either pair depends on the other.

## Technical context

**What resolves a root today.**

- `skills/code-review/scripts/round_record.py:1389` — `root = args.root or
  reader.repo_root(item)`; the refusal is `:1391`. `reader.repo_root` is
  `skills/verify/scripts/unverified_check.py:458`, a `git rev-parse
  --show-toplevel` run from the item. Executed 2026-09-08 against a
  local-mode probe: exit 128, `fatal: this operation must be run in a work
  tree`. That is not a path git failed to recognise; it is git refusing a
  work-tree question asked from inside the git directory.
- `git -C <item inside .git> rev-parse --git-common-dir` **does** answer
  (exit 0), and so does `git -C <item> worktree list --porcelain`, whose
  first entry is the main worktree. Executed in both a main tree and a linked
  worktree. That is the seam this fix uses: git itself knows which trees
  belong to the clone the item sits in, so nothing here does path arithmetic
  on `.git`.
- `hooks/optin.py#home_paths` already returns the two places in order and
  `home_at` answers *where is it*. `hooks/commit-review-gate.py:805
  declaration_hint` is the precedent — it was fixed for local mode in #80 and
  spells the path under whichever root `home_at` finds.

**What reports a declaration.**

- `skills/code-review/scripts/chain_check.py:1018` — `git ls-tree -r HEAD --
  seal/specs/`, where the prefix is `routing.WORK_ITEMS`, a
  repository-relative string. Local mode commits nothing under it.
- `:1078-1083` — the *this pull request declared neither way … Add
  seal/specs/<work-item>/routing.md to declare* message, reached from
  `declared_for_this_branch`. Executed 2026-09-08 against a local-mode probe
  holding a matching declaration: exit 0, that exact sentence.

**What records a mode.**

- `skills/implement/scripts/seal.py:1234 declared(home)` is the only code
  reader of `config.md` in the tree. The language rows are read by models
  reading the file, not by code, so moving the parser costs no other caller.
- `hooks/commit-review-gate.py:522 already_asked` is the deny-once-then-ask
  budget, keyed by `<git-dir>/specseal-commit-choice/<session>`. The new gate
  needs its own directory name or answering one question would silence the
  other.

**What breaks in six months.** The mode gate is the piece with a future
cost: it fires until somebody runs `seal mode`, so a repository that never
does pays one prompt per session forever. That is deliberate — #151's second
Done-when asks for exactly a state that keeps naming itself — but it means
the gate must degrade to `ask` after the first denial in a session, or an
unattended run in such a repository stalls. `already_asked` is what makes
that true, and the case for it is S10.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| `round_record`: resolve the root from `os.getcwd()` | One git call and no path arithmetic, but it answers for wherever the shell happens to be. A record written for an item in another clone would be judged against this one's refs | Rejected — the same defect `commit-review-gate.py`'s docstring records for `-C` |
| `round_record`: `dirname(git-common-dir)` | Correct for a plain `.git`, wrong for `--separate-git-dir` and for anything that moves the git directory. Silent when wrong | Rejected |
| `round_record`: ask git which worktrees the clone has | One extra git call, only on the path that used to refuse outright. Git owns the answer | **Taken** |
| `chain_check`: read an untracked declaration | Argued in `spec.md` §*The sharp question* | Rejected; B kept as a follow-up |
| Mode question as a third arm of `commit-review-gate.py` | Reuses the budget and the target resolution, and renders into ONE deny where the review arm already fires — so it costs FEWER interruptions, not more. **The stated objection was wrong** (the waiver form is a five-line change); what rejects it is that `tests/test_gate_judges_the_repo_it_commits_to.py` and `tests/test_chain_hooks_hardening.py` pin a two-arm prompt and compare a whole reason against a released version | Rejected — corrected during the build, `phases/phase-3.md` |
| Mode question as a `SessionStart` notice | Costs zero prompts, which is what this project's first goal wants. It cannot meet #151's first Done-when: in a fresh repository the root does not exist yet at session start, so the notice fires only in the session AFTER the one that opted in and committed | Rejected as the only mechanism |
| Mode gate fires on any Bash command, judging the SESSION's repository | Names the state on the session's first call, where `skills/implement/SKILL.md` §1 wants questions, and needs no command-line reading at all. The interruption count is unchanged, because the budget is per session. It does reach a session doing something unrelated — once | **Taken — this row was `Rejected` and the build overturned it**, after the two designs above were tried; `phases/phase-3.md` and `overview.md` carry the reasoning |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `round_record.py#where` resolves a local-mode item, through git's own worktree list; the refusal that stays names both places it looked | S1–S4; `tests/test_local_mode_reaches_the_review_chain.py`, each case seen red first | `02ef9d7`, `589cf25` |
| 2 | `chain_check.py` names the root it searched; in local mode it says nothing under that root is committed and stops naming a file to add | S5, S6; same file plus `tests/test_chain_check_at_the_pull_request.py` | `50e3e0b` |
| 3 | `hooks/config.py` (the `Mode` row, read once for the tree) and `hooks/mode-gate.py` (deny once, then ask), wired into `pre-bash` — fired on any Bash call rather than at a commit, see `phases/phase-3.md` | S7–S10; `tests/test_the_mode_question_is_asked_once.py` | `0d0ea84`, `e580e40` |
| 4 | The preset block sends a session to the bootstrap before it writes `routing.md`, and the bootstrap records the answer | S11, S12; new cases in `tests/test_first_setup_asks_once.py` | `1ef820b` |
| 5 | The records — changelog and ledger fragments, `pr-notes.md`, `overview.md` | the fragments exist and `unverified-check` reads the memo | |

## Operational impact

- **A new prompt.** One deny per session per repository, in a repository that
  has `seal/` and no `Mode` row, on the session's first Bash call. Zero once
  `seal mode` has been run once, and zero in a repository with no root. Budget
  argued in `pr-notes.md`.
- **`~/.claude/CLAUDE.md` goes stale.** Phase 4 edits the block `install.sh`
  distributes, so a machine that installed an earlier release keeps the old
  text until `install.sh` runs again. No migration exists for that today and
  none is added here.
- No migrations, no new env vars, no new dependencies, no compatibility
  break: `--root` still overrides, and every shared-mode path is unchanged.
