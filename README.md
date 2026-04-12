# claude_preset

Minimal, research-backed Claude Code preset, distributed as a **plugin**:
an implement → review agent chain, a document layout that survives across
sessions, and hooks that enforce the loop mechanically.

[한국어](./README.ko.md)

## Why so little always-loaded context

Based on [arxiv 2602.11988](https://arxiv.org/abs/2602.11988): redundant
context files *reduce* task success and inflate reasoning cost. Claude
already knows SOLID, DRY, and "read before edit". This preset ships only
what changes default behavior — everything else loads on demand (skills) or
runs outside the context entirely (hooks).

## What's inside

| Component | What it does |
|---|---|
| **Agents** — `engineer` · `code-reviewer` · `parity-checker` | Who: implementation, review, and migration fact-finding as separate contexts, each preloading its methodology skill |
| **Skills** — `implement` · `code-review` · `legacy-parity` + quality utilities (`verify`, `audit`, `debug`, …) | How: procedures loaded only when triggered |
| **Hooks** — commit-review-gate · review-history-guard · worktree-guard · lint-python | When: mechanical enforcement, auto-registered by the plugin (no settings.json wiring) |
| **CLAUDE.md block** | The ~15 lines that must live in always-loaded context (language, tooling, two safety rules, git) |

### The chain

```
engineer implements → verify → code-reviewer reviews → report to user
        ↑                                                    │
        └── fixes (user's call) ← user decides ──────────────┘
commit  → allowed once the cycle carries a review mark (hook-enforced, approvable)
```

Cross-session continuity lives in the repo, not the session:

| Root | Lifetime | Holds |
|---|---|---|
| `docs/` | permanent | policies, evidence ledger (spec clause ↔ code coordinates), follow-ups |
| `specs/` | one work item | SDD, overview |
| `_ai/` | between sessions | review rounds, todo handoffs — committed, drained, then deleted per PR |

Missing files bootstrap automatically from `templates/`.

### Migrations

A repo that declares `docs/parity.md` (original repo, baseline commit) gets
three-way judgment — policy ↔ original ↔ new, with *preserve the original*
as the fallback — and the `parity-checker` agent for original-code
fact-finding. Repos without the config never see any of it.

## Install

```bash
# 1. Plugin (skills + agents + hooks + commands)
claude
> /plugin marketplace add MichaelYcJo/claude_preset
> /plugin install claude-preset

# 2. CLAUDE.md block — pick ONE scope
bash install.sh            # interactive: global (~/.claude) or project (./)
bash install.sh --project  # non-interactive project scope
```

`install.sh` backs up to `CLAUDE.md.bak`, merges only its marker block
(idempotent — rerun to update), and never edits your own content: overlaps
are warned about, not resolved. For a reviewed, deduplicating merge run
`/preset-setup` inside Claude Code instead — every deletion goes through an
approval diff.

## Language policy

Functional files (skills, agents, hooks, commands) are English-only — they
load into model context, and a translated mirror would drift. Korean exists
for human-facing docs only (this README). Response language is set by the
CLAUDE.md block, independent of instruction language.

## License

MIT
