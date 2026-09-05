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
