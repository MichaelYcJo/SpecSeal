# 1791270162 — handoff

Written 2026-10-06 by the orchestrating session (Opus 5.5) when the 0.20.0 run moved to another machine. Read this first, then `overview.md` and `phases/phase-1.md`.

## Where it stands

- Framed by `framer` on Fable 5.1 (1f76a078). Phase 1, the corpus measurement, was built by `smith` on Opus 5.5 and is closed (1d28e9a9, 29bb0421). Nothing under `hooks/`, `tests/` or `.github/` changed.
- The branch is pushed so the other machine can fetch it. No pull request is open.

## Phase 2 waits on the owner

M3 is not zero. As framed, 595 recorded command shapes would stop with no plain spelling to rewrite them to. The frame says that every such shape becomes an owner row, and the smith opened three:

- **P2.** The frame's In 1 reads any `$( … )` body holding `git` as unrecognised. That clause alone accounts for 575 of the 595. Should a body be read recursively through the same three shapes? With that reading, M3 falls to 34.
- **P3.** What happens to `update-ref` (13) and `symbolic-ref` (1)?
- **P4.** What happens to an untokenizable command (5)?

P1 (where the allow-list comes from) is still unanswered, and its default (a), recorded subcommands only, stands. The phase-2 spawn prompt carries the answers to P2–P4.

## Found for phase 2 (W3)

- `hooks/cmdline.py#command_strings` returns no string for `eval "git switch x"`.
- A redirection after `git` (`git 2>/dev/null …`) is read as the subcommand word.

## Next

1. Ask the owner P2–P4 together, once, and P1 with them if they want to change its default.
2. Phase 2 by `plan.md`, then phase 3. Phase 3 rebases onto #841's twins sampling, which lands first (W4). Then phase 4. The framer estimated 3–5 hours of smith wall time in total.
3. Routing is `automation`: the draft pull request, the `warden` rounds (Opus 5.5), `broad-gate --preflight`, the sealer, then ready. The pull request goes into `release/v0.20.0` (squash) and closes #826, #732 and #734.
