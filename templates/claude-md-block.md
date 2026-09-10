<!-- specseal:start -->
## Tooling
- Python: prefer uv · Node.js: prefer pnpm (always respect the project's existing manager).

## Safety
- **3+ Fix Rule** — same bug, 3 failed fix attempts → STOP. Re-examine the architecture, then ask.
- **Verification Gate** — no "done / fixed / passes" claim without running the check that proves it and reading its full output.
- **Verification Scope** — narrow and often, broad once. A slice runs what you just wrote; the handoff to review runs nothing broad; the full suite, lint, and typecheck run once, after the rounds settle. A broad run with an edit after it was spent, not banked.

## Session cost
- **Batch independent reads and runs** — every coordinate a task names in one call, every case from one file in one command. Round-trips are most of a round; cut the trips, never the investigation.

## Git
- Run lint/format/typecheck before committing.
- Worktrees only for concurrent sessions on the same tree — single-session work uses `git switch` (worktree-guard hook enforces this).
- **Routing, decided at the start** — **first, if this repository has `seal/` at neither `<repo>/seal/` nor `$(git rev-parse --git-common-dir)/seal/`: stop and follow the Bootstrap section of `skills/implement/orchestration.md`, the `implement` skill's orchestrator half.** Writing the file below is what CREATES that directory, creating it is what opts the repository in, and WHERE it lands — committed with the repository, or under the git directory and on this machine only — is the user's decision and not yours. Then, before the first edit, write `seal/specs/<work-item-id>/routing.md` from `templates/sdd-routing.md` and commit it — the write **in a command of its own**, never batched with the commit. The gate reads that file from the working tree, so a declaration on disk silences the very commit that adds it and no first-commit waiver is needed; but the gate is a `PreToolUse` hook that denies the WHOLE Bash call, so `write && git add && git commit` in one call writes nothing and the declaration the gate then reports missing is the file that was lost. This is the one place the batching rule above misleads. **Ask all three axes as one `multiSelect` question with three checkboxes**, never one at a time: implementation (`smith` · `the session` — an optional row), review (`through the review chain` · `straight to the PR`) and destination (`open the pull request` · `stop before the pull request`). What is checked is the answer, and each box is a row of that file — asking the reviewer in the middle and the pull request at the end is three waits for one decision. The commit gate reads that file, so a declared work item commits silently for either review answer, and CI reads the same file at the pull request. For a change belonging to no work item, `[no-review]` still waives one command (`[no-parity]` too where a migration config is declared) — in front of the command, quotes included, `: '[no-review]'; git commit …`, because after `git commit` a bare word is a pathspec and git rejects it. Deciding at the commit is what stops a release mid-run.
<!-- specseal:end -->
