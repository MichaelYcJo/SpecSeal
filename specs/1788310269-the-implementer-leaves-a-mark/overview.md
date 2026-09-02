# 1788310269-the-implementer-leaves-a-mark — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. -->

📋 implement applied
· spec:     this item's `spec.md`, `plan.md`, `questions.md`, `routing.md` ·
            the old item's `spec.md` and `plan.md` read from
            `wip/the-implementer-mark` · issue #26 in this repository ·
            `CLAUDE.md` on this branch · `CONTRIBUTING.md` §What a change to a
            gate must carry · `.specseal/follow-up.md` (no row for this) ·
            `templates/sdd-*.md` · `hooks/routing.py`, `hooks/dispatch.py`,
            `hooks/optin.py`, `hooks/console.py`, `hooks/review-history-guard.py`,
            `hooks/commit-review-gate.py#read_mark` / `#already_asked` /
            `#judge`, `hooks/hooks.json`
· evidence: 6 rows in `.specseal/map/1788310269-the-implementer-leaves-a-mark.md`;
            no row of `.specseal/map.md` removed — this change deletes no anchor
· verified: executed — the scope run (344 across the eleven files named in
            the plan, 1 failing only for the overview this file is; 137 across
            the wording pins), 11 mutations each red with bytecode caching off,
            the old branch's 15 tests against the old hooks in a scratch copy
            (15 passed), two hand probes (`cmdline.py` broken: the `pre-agent`
            group silent and the mark still written; the mutated notice
            printing on both commits), `ruff check` and `ruff format --check`
            on every touched `.py`, `evidence_check.py --strict .` at 141 ok ·
            0 broken. Read only — the phase-1 diff of the old branch against
            this tree, `hooks/hooks.json`'s routing, the two consumers of a
            declaration that do not change

## Why this work exists

The routing declaration's third axis was parsed and read by nothing, so a
session could declare `smith`, build the item itself, and leave a record saying
otherwise; now spawning `smith` leaves a mark in the git dir and a declaration
that says `smith` with no mark is said out loud once, after a commit, without
blocking anything.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| What "unfinished" meant on the old branch | The handoff read the old commit's title, `wip: … unfinished`, as code that might not work | The old test file passes 15/15 against the old hook files in a scratch copy on this tree's `conftest.py`. What was never written is the record — no `overview.md`, no changelog entry, no ledger rows, no Status column, no README row — and what was never measured is issue #26's objection about a second `pre-agent` gate. The hook code is carried with three changes: `console.to_utf8()` in the mark gate's `__main__`, the notice's path built with `os.path.join`, and the "written before the group decides" paragraph | Executed: the scratch run and the mutations. `plan.md` phase 1 |
| Whether to build it at all | Issue #26 (this repository) records the decision to defer this until one of two conditions is met, and neither is met in the form written | Built. The repository owner committed this item's `routing.md` on 2026-09-02 with `Implementation = smith` and a "Why this way" naming the mark and the notice as the unfinished half; the objection that could be measured (S13) was measured and does not hold — `run_gate` catches per gate. Whether the issue closes is `questions.md` Q1, left to the owner | `routing.md` is the later document and the owner's; the issue is quoted rather than overruled |
| The `dispatch.py` rider | *"`pre-agent` holds only the worktree guard"* — true when stamped, false once a second gate joins the group | Restated to *"the worktree guard is the only gate in `pre-agent` that decides anything"*, with the measurement that the mark gate neither widens nor narrows the silence, and re-stamped at `9edc59f`, a commit the release branch already carries | Executed: `cmdline.py` broken in a copy, `pre-agent` prints nothing and exits 0, the mark is still written |
| The template's comment | *"A wrong answer here is never contradicted by anything"* | *"…by anything that can stop a commit"* — a confident `smith` nobody performed now earns one printed line; a confident `the session` still earns nothing | The pin in `tests/test_waiver_decided_at_start.py` reads the placeholder row, not the comment, and stays green |
| Where the mark is keyed | The `specseal-reviewed` precedent keys on HEAD | On the branch name | A work item commits many times and the implementer does not change when it does; keyed on HEAD the notice would print after every commit (old plan, carried) |

## Not verified

| Item | Who must answer |
|---|---|
| The review chain. `routing.md` answers `through the review chain`, and no round ran in the session that built this: `rounds/` is empty, and CI requires a committed `round-N.md` for a work item routed this way | the orchestrator that spawned this item — spawn `specseal:warden` against `bd48cec..HEAD`, then a verifying round on the fixes |
| The broad gate: the full suite, `ruff check .`, `ruff format --check .`, `chain_check.py` and `unverified_check.py` with CI's invocations. The scope here was the eleven test files the plan names plus the wording pins | the orchestrator, once, after the review rounds settle — a broad run taken before them is spent by the first fix |
| The live harness payload for `PreToolUse` on `Agent`: the tests feed `tool_input.subagent_type` and `cwd` as `hooks.json`'s other gates receive them, and no real `smith` spawn was made in a repository with the plugin installed at this commit | the repository owner, in the first session that spawns `smith` on a declared branch after this merges — `ls .git/specseal-implementer` is the check for the mark, and a commit on a declared branch WITHOUT a mark should show the notice's one line (round 1 ❓ 9: whether a PostToolUse `print()` reaches the person) |
| The Windows leg — the notice's path is joined with `os.path.join` and every file open that reads or writes text names `encoding="utf-8"` (the empty session marker is the one exception, and it writes no bytes), but every run here was on macOS | CI at the pull request |
| Whether issue #26 closes, is amended, or stays open against a design that now ships (`questions.md` Q1) | the repository owner |

## Not done

**The notice does not follow `git -C` to another repository.** It judges the
repository at the session's `cwd`, the line `review-history-guard.py` draws
(`questions.md` Q3). Following it means re-deriving every target the commit
gate derives, to decide whether to print one line.

**The mark is written before the group decides.** A spawn the worktree guard
stops still leaves one (`questions.md` Q2). Writing it only on allow would
make the dispatcher know one gate's semantics, and the cost of the default is
a missed reminder once per session for a session that answered the guard by
not spawning smith at all.

**Phase 1 of the old plan was not re-applied.** On every file it touched the
tree is ahead of the old branch: `hooks/routing.py` has the `parse()`
docstring's later wording, `ROUNDS_DIR`, `_ordered` and the `rounds()` split;
`templates/sdd-routing.md` has the placeholder row and its comment;
`tests/test_routing_is_recorded.py` carries the four third-axis cases;
`skills/commit-pr-convention/SKILL.md` exists. No gap was found; the
`git apply --3way` conflicts the handoff measured are the tree being newer,
not the tree missing something.

**`docs/review-chain-spec.md` gained a section rather than a new document.**
The two hooks read the routing declaration the review chain is built on, and
the document already carries one section per hook that does; `docs/` is where
a norm is ratified, and the section states what the hooks do and what they
cost, not a new rule.

## Fed back into the spec

S13 and S14 in `spec.md`, marked *inferred during implementation*: S13 is
issue #26's objection turned into a test, and S14 is the Windows path lesson
`review-history-guard.py` already carried, applied to the notice before it
could be learned again. A planner may drop S14 if the notice stops naming a
path.
