# Questions — 1788632199

## Asked and answered, 2026-09-06, before the first edit

Asked as one batch covering the whole rest of 0.8.2, so that a night's run
would not stop on any of them.

| # | Question | Answer | What it decided |
|---|---|---|---|
| 1 | #156 enumerates four answers — `bin/` entry, `pyproject.toml` with a test extra, a line of prose, or "out of scope, say so" | **`bin/test` plus the line in `CONTRIBUTING.md` that names it** | `spec.md` §Scope. The issue itself calls this the one matching what is already here: five `bin/` pairs exist so a reader can type a command rather than a path into a plugin directory |
| 2 | Routing | **smith · through the review chain · open the pull request**, the same as #170 | `routing.md`. The three remaining 0.8.2 items are the first readings of #161's target, and a reading taken under different conditions is not a comparison |
| 3 | How far the unattended run goes | **to the tag** — each item squashed into `release/v0.8.2`, then the release commit, the release pull request, a merge commit into `main`, and `v0.8.2` | not this work item's, but it is why nothing here waits for a person |
| 4 | What happens if this item's chain caps or its broad gate goes red | **stop this item, carry on with the others**, and report what stopped in the morning | the item's own state is left in its draft pull request rather than rolled back |

## Assumed, not asked

| # | Assumption | Why it does not wait |
|---|---|---|
| 5 | The issue's premise that no file names a command is wrong for `CONTRIBUTING.md`, and the work is therefore about the command's COST rather than its absence | verified by reading the file: §*Running the checks* names `uvx --with pytest python3 -m pytest tests/ -q`. Correcting a ticket's premise is the implementer's job, and the ticket ranks below what the repository actually contains |
| 6 | `bin/test` runs the full suite and is therefore the orchestrator's command, not a segment's | `skills/agent-contract/SKILL.md` §2 already forbids the full suite to smith and warden; this work item may not make that easier to ignore, and `spec.md` §Scope's last *Out* says so |

## Raised in phase 2, for the owner

| # | Question | Why it does not stop the work |
|---|---|---|
| 7 | The plugin ships from the repository root, so 0.8.2 will put `.github/scripts/run_tests.py` and `tests/` into every user's plugin cache beside `bin/test`. Both of the runner's guards — *no runner beside it* and *no tests directory* — are therefore unreachable there. Does a deliberate invocation out of a cache need a guard of its own, or is it accepted? | Neither answer changes phase 2. A plugin user cannot reach the command by typing it, because `test` is a shell builtin and PATH never offers it; reaching the runner means typing a path into a versioned cache directory on purpose. Adding a guard is mechanism on phase 1's surface, so phase 2 corrected the false reason and left the decision here |

**Question 7 is confirmed, not hypothetical.** Review round 1 measured it
rather than reasoning about it. **[executed, round 1]** `ls -a` on the 0.8.1
plugin cache lists `.github`, `bin` and `tests`, so a 0.8.2 cache will hold
the runner and a `tests/` directory beside each other; a deliberate path into
such a cache therefore passes **both** of the runner's guards, builds a
`.venv` inside the cache directory, and runs for five minutes. **[executed,
round 1]** `command -v test` returns `test is a shell builtin` in `sh`, `bash`
and `zsh` with a clone's `bin/` first on `PATH`, so the builtin is the whole
of what keeps a user out.

That is the state, and it is still the owner's decision rather than a defect
to close: round 1 raised it as ⬜ and the fix pass left it, because a third
guard is mechanism on phase 1's surface and a fix pass adds none. What
changed here is only that the question no longer reads as a possibility
nobody checked.
