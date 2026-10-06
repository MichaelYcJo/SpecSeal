# 1791270163 — handoff

Written 2026-10-06 by the orchestrating session (Opus 5.5) when the 0.20.0 run moved to another machine. Read this first, then `overview.md`.

## Where it stands

- Framed by `framer` on Fable 5.1 (68233513); built by `smith` on Opus 5.5. All three phases of `plan.md` are committed (ee631b6b, 94f22603, 944ad173, 3a0ecbca).
- The smith's slice checks, as it reported them (executed by the smith, not by this session): six modules 3447 passed, `bin/evidence-check` exit 0, `gather_changelog.py --dry-run --version 0.20.0` exit 0, `bin/unverified-check` and `bin/correction-check` exit 0.
- The branch is pushed so the other machine can fetch it. No pull request is open.

## Not run in this segment

- The broad gate (full suite, repository lint, typecheck). `ruff` was not on this machine's PATH, so the three changed Python files are not linted either.
- `survivor-check`: there was no review round, so there is no fix range.

## Next

1. Take the owner's answer for the `Review` and `Destination` rows. `routing.md` records "for now, framer + smith" from the owner. If the answer changes, rewrite `routing.md` in a command of its own and commit it.
2. If review: spawn `warden` on Opus 5.5 against `origin/release/v0.20.0`, then run the sealer.
3. If straight to the PR: the sealer's `broad-gate.md` is still owed at a ready pull request.
4. The pull request goes into `release/v0.20.0` (squash) and carries `Closes #831`.
