# Feature Specification: 1788310269-the-implementer-leaves-a-mark

<!-- specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* — *"Between two designs that catch the same defect, the one that stops to ask a person is the more expensive"* | Why the notice prints and never blocks, and why the mark adds no prompt. Both halves are chosen against this line |
| `CONTRIBUTING.md` §*What a change to a gate must carry* — a test seen red, a stated failure direction, a prompt budget | The three things this change has to state: the mutations that turn each test red, "fails toward a false reminder rather than a false silence", and a prompt budget of zero |
| `hooks/routing.py#parse` — *"NOTHING reads this one yet — the notice that would have is #26 — so a wrong answer here is recorded and never contradicted"* | The sentence this work makes false. The third axis is parsed and returned, and nothing has read the result until now |
| `hooks/dispatch.py#run_gate` — the `# RIDER:` — *"`pre-agent` holds only the worktree guard, so the Agent `isolation: "worktree"` path goes undefended with nobody told"* | Issue #26's second objection to building the mark. `run_gate` catches per gate, so a gate that fails to load is skipped and its neighbour still decides; this work pins that with the mark gate broken on disk |
| `hooks/review-history-guard.py` — *"Reminder-only (PostToolUse cannot block). Active only in repos with `.specseal/` at the root"* | The reminder pattern the notice copies: `PostToolUse`, `print()`, opt-in, resolved through `optin.repo_root` and `routing.item_dir` |
| `hooks/commit-review-gate.py#read_mark` and `<git-dir>/specseal-reviewed` | The precedent for where a mark lives: the repository's git dir, resolved by `git rev-parse`, never committed, never seen by CI |
| Issue #26 — *"the Implementation axis is self-reported, and nothing watches it"* | The recorded decision to defer this, with two objections and the two conditions that reopen it. `questions.md` Q1 carries whether this work closes it |

## Scope

**In.**

1. **The mark.** A gate in the `pre-agent` dispatch group reads the spawn
   payload's `subagent_type` and, when it names `smith` (`specseal:smith` or
   a project-local `smith`), writes the checked-out branch name into
   `<git-dir>/specseal-implementer`. Silent in every case: it prints nothing,
   so it can neither deny nor ask. Silent also in a repository with no
   `.specseal/`, where it writes nothing.
2. **The notice.** A `post-bash` reminder that, after a command which
   actually invokes `git commit`, reads the declaration in force for the
   checked-out branch and, where it answers `Implementation` with `smith` and
   no mark stands for that branch, prints one line naming the declaration.
   Once per repository per session. It never carries a permission decision.
3. **The shared address.** `hooks/implementer.py` owns the mark's file name,
   the git-dir resolution, the write, the read, and the `smith` test, so the
   writer and the reader cannot spell the path two ways.
4. The words that said nothing reads the axis — `hooks/routing.py#parse`'s
   docstring, `templates/sdd-routing.md`'s comment, the README's gate table,
   `docs/review-chain-spec.md`'s registration section — now say what does.

**Out.**

- Blocking on the axis. The old plan rejected it for prompt volume and this
  repository's first goal says the same; the case being caught is a session
  forgetting its own declaration, not an adversary.
- A CI check. The mark lives in the git dir and CI never sees one; `smith`
  produces no committed artifact a session could not also write.
- Treating the mark as proof against forgery. Every mark the plugin writes
  can be written by hand, `specseal-reviewed` included.
- Re-applying phase 1 of the old plan. The axis, the template row, the
  `commit-pr-convention` skill and the asking shape are in the tree at the
  branch point (`9edc59f`); this item diffs them and states the gap.
- Changing what `Review` or `Destination` mean, or what reads them. The
  commit gate's decision is byte-identical with the row and without it.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 Spawning smith leaves a mark | Given a repository with `.specseal/` · When the `pre-agent` group runs for `subagent_type: specseal:smith` · Then the group prints nothing and `<git-dir>/specseal-implementer` holds the checked-out branch | `tests/test_the_implementer_is_recorded.py::test_spawning_smith_leaves_a_mark`, through `dispatch.py pre-agent` |
| S2 Any other agent leaves none | When the same group runs for `specseal:warden`, `specseal:scribe`, `general-purpose`, `smith-helper` · Then no mark file exists | `::test_spawning_any_other_agent_leaves_none` — `smith-helper` is there because a substring test would read it as the agent |
| S3 The project-local spelling counts | When `subagent_type` is bare `smith` · Then the mark is written | `::test_the_project_local_spelling_of_the_agent_counts_too` |
| S4 A repository that never opted in gets no file | Given no `.specseal/` · When smith is spawned · Then nothing is written into its git dir | `::test_a_repository_that_never_opted_in_gets_no_files_written` |
| S5 The mark is branch-scoped | Given a mark for this branch · Then it does not stand for another branch name | `::test_the_mark_does_not_answer_for_another_branch` |
| S6 A declared smith with no mark is noticed after a commit | Given a declaration answering `smith` and no mark · When `post-bash` runs for `git commit -m x` · Then the output names the work-item directory and the axis | `::test_a_declared_smith_with_no_mark_is_noticed_after_a_commit` |
| S7 With the mark present nothing is said | Given the same declaration and a mark for this branch · Then the notice is absent | `::test_with_the_mark_present_nothing_is_said` |
| S8 Once per repository per session | When two commits run under one session id · Then the notice appears once; a second session id is told again | `::test_the_notice_is_said_once_per_repository_per_session` |
| S9 The other answer, no row, and an unreadable row are all silent | Given `the session`, or no `Implementation` row, or `whoever gets to it` · Then no notice | `::test_the_other_answer_is_not_a_defect`, `::test_a_declaration_without_the_row_says_nothing`, `::test_an_unreadable_answer_says_nothing_either` |
| S10 A command that does not commit says nothing | Given `ls -la`, `echo 'remember to git commit'`, `git status` · Then no notice | `::test_a_command_that_does_not_commit_says_nothing` |
| S11 The commit gate decides identically with the row and without | When `commit-review-gate.py` runs for the same commit under a declaration with and without the row · Then both outputs are byte-identical | `::test_the_commit_gate_decides_identically_with_the_row_and_without` |
| S12 The notice never carries a permission decision | When `implementer-notice.py` runs alone · Then its output has no `permissionDecision` | `::test_the_notice_never_carries_a_permission_decision` |
| S13 A broken mark gate does not take the worktree guard down | Given a copy of `hooks/` with `implementer-mark.py` unparseable or deleted · When `pre-agent` runs for an `isolation: "worktree"` spawn · Then the guard's verdict is what it was with the gate intact | `::test_a_broken_mark_gate_leaves_the_worktree_guards_verdict_alone` — issue #26's second objection, measured |
| S14 The path in the notice is spelled the way the platform spells it | When the notice prints · Then the file it names is built with `os.path.join`, never a literal `/` | `::test_the_notice_names_the_file_the_way_the_platform_spells_it` |

## Data & interfaces

```
hooks/implementer.py
  MARK = "specseal-implementer"
  git_dir(cwd) -> str          absolute git dir, or ""
  write(cwd, branch) -> bool   records `branch`; never raises
  stands(cwd, branch) -> bool  True when the mark holds `branch`
  is_smith(subagent_type) -> bool

hooks/dispatch.py
  GROUPS["pre-agent"] gains "implementer-mark.py"
  GROUPS["post-bash"] gains "implementer-notice.py"
```

`hooks/hooks.json` changes nothing: `PreToolUse` on `Agent|Task` already
routes to `dispatch.py pre-agent`, and `PostToolUse` on `Bash` to
`dispatch.py post-bash`.

No unit already in the tree changes signature or return.

## Open questions → questions.md

Three, none blocking: whether this work closes issue #26, the mark written
for a spawn the worktree guard then denies, and a smith spawned from a
directory other than the repository the declaration lives in.
