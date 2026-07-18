<!-- specseal:start -->
## Language
- Respond in Korean (한글). Code, comments, identifiers, commit messages: English.

## Tooling
- Python: prefer uv · Node.js: prefer pnpm (always respect the project's existing manager).

## Safety
- **3+ Fix Rule** — same bug, 3 failed fix attempts → STOP. Re-examine the architecture, then ask.
- **Verification Gate** — no "done / fixed / passes" claim without running the actual check and reading its full output.

## Git
- No `Co-Authored-By` line. Run lint/format/typecheck before committing.
- Worktrees only for concurrent sessions on the same tree — single-session work uses `git switch` (worktree-guard hook enforces this).
<!-- specseal:end -->
