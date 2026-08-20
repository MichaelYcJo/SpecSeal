<!-- specseal:start -->
## Tooling
- Python: prefer uv · Node.js: prefer pnpm (always respect the project's existing manager).

## Safety
- **3+ Fix Rule** — same bug, 3 failed fix attempts → STOP. Re-examine the architecture, then ask.
- **Verification Gate** — no "done / fixed / passes" claim without running the actual check and reading its full output.

## Git
- Run lint/format/typecheck before committing.
- Worktrees only for concurrent sessions on the same tree — single-session work uses `git switch` (worktree-guard hook enforces this).
<!-- specseal:end -->

<!-- Below: repo-local development rules for SpecSeal itself.
     install.sh distributes only the marker block above. -->

## Repo rule — no real identifiers in examples or fixtures

Examples, fixtures, and docs use neutral values only: `example.com` for
domains, `/Users/x/` for user paths. Enforced by
`tests/test_no_real_identifiers.py` in CI — extend its allowlist consciously;
never make a test pass by inlining a real domain, path, or org name.
(Both incidents that forced a history rewrite entered exactly this way.)
