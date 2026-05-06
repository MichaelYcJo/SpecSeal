# plugin-restructure — overview

📋 implement applied (retroactively — this overview was written after the
fact; the preset was not yet dogfooding itself when the work started)
· spec:     none existed — decisions were made in conversation; the durable
            ones are now ratified in docs/worktree-guard-spec.md and
            docs/review-chain-spec.md
· evidence: measurements recorded in the two docs above (idle-TUI repaint,
            attachment contamination, background-agent transcript location)
· verified: see "What was verified" below — executed vs read is labeled

## What was done

Converted claude_preset from a copy-installed rule set into a Claude Code
plugin: an implement → review agent chain (3 agents, 3 methodology skills),
enforcement hooks auto-registered via hooks.json, a three-axis document
layout (docs/specs/_ai) with bootstrap templates, and a marker-block
CLAUDE.md installer. The worktree-guard hook was then verified against live
sessions and its activity model rebuilt.

## Key judgments (and their grounds)

| Judgment | Chosen | Grounds |
|---|---|---|
| Distribution | Official plugin over submodule/symlink or copy install | hooks auto-register; no settings.json wiring; version-pinned team install |
| Reviewer skill delivery | agent frontmatter `skills` preload | reviewer agents have no Skill tool; preload delivers the methodology without per-prompt "Read this path first" instructions |
| CLAUDE.md merge | mechanical = marker block only; semantic dedup = /preset-setup with approval diff | scripts cannot judge meaning; a false-positive deletion destroys user rules silently |
| Commit gate decision | `ask`, not `deny` | user approving IS the waiver; deny with no override forces contortions |
| Gate opt-in | presence of `_ai/` at repo root | a global plugin must not nag repos that don't use the workflow |
| Session activity | 5-min threshold over three signals (input, output, transcript active-events) | input-only needed 60 min: autonomous turns type nothing (measured live: 52 min keystroke-quiet session writing its transcript that second) |
| Transcript freshness | tail's last ACTIVE event, not file mtime | idle sessions receive passive `attachment` appends — observed faking activity on three forgotten tabs |
| legacy-parity scope | separate skill + fact-finder agent, activated by docs/parity.md | 3-way judgment is migration-only; migrating projects reduce to a config file |

## What was verified (executed)

- install.sh: append / idempotent update / block replacement / --project /
  non-interactive fallback — all pass
- commit-review-gate: 5 stdin scenarios; review-history-guard: 6 scenarios
- worktree-guard: 10-scenario regression + live discrimination (forgotten
  tabs → ask with ages; autonomously working session → deny) + 3 fixture
  units for passive-event filtering

## Not verified (who must answer)

| Item | Who |
|---|---|
| install.sh interactive TTY branch | user, in a real terminal |
| plugin install end-to-end (`/plugin marketplace add` → hooks fire, `${CLAUDE_PLUGIN_ROOT}` resolves) | user, after push |
| double hook registration on machines whose personal settings.json already wires the same guards | user — remove the personal wiring when adopting the plugin |

## Remaining scope

writing-style skill (needs fresh example material before it can ship);
re-audit of the 8 persona agents and 18 generic commands kept from v0.1.
