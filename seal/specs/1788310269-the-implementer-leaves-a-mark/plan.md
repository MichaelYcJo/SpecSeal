# Implementation Plan: 1788310269-the-implementer-leaves-a-mark

<!-- specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

## Summary

The routing declaration's third axis, `Implementation`, is parsed and never
read. Add the half that reads it: a silent `pre-agent` gate writes a mark into
the git dir when `smith` is spawned, and a `post-bash` reminder says once,
after a commit, when the declaration answers `smith` and no mark stands. The
old branch that designed this (`wip/the-implementer-mark`, pre-rewrite, no
common ancestor) left its code passing its own tests; what it never wrote is
the record around them, and what it never measured is the objection issue #26
raised against it.

## Technical context

| Coordinate | What it gives this work |
|---|---|
| `hooks/routing.py#parse` | Returns `implementation` as `smith`, `the session` or `None`; the docstring says nothing reads it and names #26 |
| `hooks/routing.py#for_branch` · `#item_dir` · `#current_branch` | How the notice finds the declaration in force and the directory to name |
| `hooks/dispatch.py#GROUPS` | `"pre-agent": ("worktree-guard.py",)` and the `post-bash` tuple — both gain one entry |
| `hooks/dispatch.py#run_gate` | The per-gate `except Exception: return ""`; its rider says a failed import reads as an allow. The isolation it also provides is what S13 pins |
| `hooks/review-history-guard.py#main` | The reminder shape: `optin.repo_root`, `optin.opted_in`, `routing.item_dir`, `os.path.relpath`, `print()` |
| `hooks/commit-review-gate.py#read_mark` · `#already_asked` | Mark in the git dir; a per-session marker file whose id is `os.path.basename`d so it cannot escape the directory |
| `hooks/cmdline.py#split_segments` · `#drop_heredoc_bodies` · `#drop_comments` · `#parse_git` | How the notice decides a command actually commits, without a regex reading prose |
| `hooks/console.py#to_utf8` | Every standalone gate calls it in `__main__`; both new entry points do |
| `hooks/optin.py#opted_in` | The opt-in every gate reads; a repository with no `.specseal/` gets no file written |
| `tests/test_gate_judges_the_repo_it_commits_to.py::test_the_worktree_guard_is_no_longer_load_bearing_for_this_gate` | The copy-`hooks/`-and-break-a-file shape S13 mirrors |

**What breaks in six months.** The mark is written by a `pre-agent` gate, and
`dispatch.py` renders a gate that fails to load as an allow with no output. A
mark that silently stops being written must turn the notice ON, not off: the
notice fires on *declared `smith` AND no mark*, so a dead gate produces a
false reminder somebody reads rather than a false silence nobody does. The
cost is one line per session in that state.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Block the commit when the declaration and the mark disagree | A fourth thing that can stop a commit, paid on every commit of every work item, to catch a session forgetting its own declaration. `CLAUDE.md`'s first goal says the design that stops to ask is the more expensive one | rejected — notice, never denial (carried from the old plan) |
| Check the axis at the pull request in `chain_check.py` | CI never sees a git dir; `smith` produces no committed artifact a session could not also write. The check would assert something nothing there can read | rejected (carried) |
| Emit the notice from the commit gate's allow | A `PreToolUse` gate that allows produces no output — allowing IS silence. The notice would be a line nobody sees | rejected — `post-bash` is the nearest site whose output is read |
| Key the mark on HEAD, like `specseal-reviewed` | A work item commits many times and the implementer does not change when it does; the notice would print after every commit | rejected — keyed on the branch name |
| One file: mark and notice in a single hook | The writer runs on `Agent|Task` and the reader on `Bash`; one module in two groups is two `main()`s under one name, or a `tool_name` switch. Two hooks and a shared address module is the shape `optin.py` already justifies | rejected |
| Wait for issue #26's reopening conditions | The repository owner routed this item and committed its `routing.md` with `Implementation = smith` on 2026-09-02; the second objection is measurable now (S13). Whether #26 closes is Q1 | the work proceeds; Q1 records the decision left |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | What of the old change is in the tree: `git diff wip/the-implementer-mark HEAD` over `hooks/routing.py`, `templates/sdd-routing.md`, `tests/test_routing_is_recorded.py`, `tests/test_review_axes.py`, `skills/commit-pr-convention/SKILL.md`; the old test file run against the old hooks in a scratch copy | **Executed**: the tree is AHEAD of the old branch on every phase-1 file (its `parse()` docstring, `ROUNDS_DIR`, `_ordered`, the template's placeholder row and comment all postdate it); the old 15 tests pass 15/15 in the scratch copy, so "unfinished" is the record, not the code | a3579aa — the record; no code moved |
| 2 | The mark: `hooks/implementer.py`, `hooks/implementer-mark.py`, `pre-agent` gains it; S1–S5 and S13 | **Executed**: S1–S5 through `dispatch.py pre-agent`; S13 with the gate unparseable and then deleted on a copy of `hooks/`; 5 mutations of the mark half each red | 2322674 |
| 3 | The notice: `hooks/implementer-notice.py`, `post-bash` gains it; S6–S12, S14 | **Executed**: S6–S12 and S14 through `dispatch.py post-bash` and the standalone hook; S11 byte-identical; 6 mutations of the notice half each red (one first survived through a stale `.pyc` and is red with bytecode caching off) | 2322674 |
| 4 | The words: `routing.py#parse` docstring, the template comment, the `dispatch.py` rider re-verified, README gate rows, a `docs/review-chain-spec.md` section | **Executed**: `tests/test_a_rider_reaches_its_file.py`, `tests/test_waiver_decided_at_start.py`, `tests/test_review_axes.py`, `tests/test_handoff_outlives_the_merge.py`, `tests/test_no_real_identifiers.py` green; the rider's claim re-measured with `cmdline.py` broken | 666fcb8 |
| 5 | The record: `changelog.md`, `.specseal/map/<id>.md` with content coordinates, `overview.md` with its Not verified table, `questions.md`, this column | `evidence_check.py --strict .` at 0 broken; the scope run green; `ruff check` and `ruff format --check` clean on touched files | **Executed**: 141 ok · 0 broken; 379 passed across the scope; ruff clean; `unverified_check.py --baseline origin/release/v0.3.0` reads 5 open rows, each with an answerer — d3c17b8 |

## Operational impact

- **Two new gates.** `pre-agent` gains one that prints nothing; `post-bash`
  gains one that prints at most one line per repository per session. Prompt
  budget: zero — neither can deny or ask.
- **Two new files under the git dir**: `specseal-implementer` (one line, the
  branch name) and `specseal-implementer-notice/<session-id>` (empty). Neither
  is committed; neither travels.
- **Failure direction.** Everything fails toward "no mark", which is toward a
  reminder, never toward a stop and never toward a silence that hides a dead
  gate.
- **Platform.** Paths the notice prints are built with `os.path.join`; every
  file open that reads or writes text names `encoding="utf-8"` (the one
  exception creates an empty marker and writes no bytes); no shell is spawned. The Windows leg is
  CI's to run.
- No migration, no dependency, no environment variable, no change to
  `hooks/hooks.json`.
