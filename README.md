# SpecSeal

[![tests](https://github.com/MichaelYcJo/SpecSeal/actions/workflows/test.yml/badge.svg)](https://github.com/MichaelYcJo/SpecSeal/actions/workflows/test.yml)

**Specs, sealed** — when code moves away from its spec, the build turns red.

![SpecSeal demo: evidence-check catches spec-code drift](./assets/demo.gif)

Coding agents make claims. SpecSeal makes them carry **marks**: a maker's
mark that can only be stamped by actually reading the spec, a warden's seal
without which no commit passes the gate, and a ledger where every clause
points at the code that grounds it. When the code moves and the ledger
doesn't, the build turns red.

No claim without a mark. No mark without a test. No merge without the seal.

Distributed as a Claude Code **plugin**; the ledger, the drift checker, and
the handoff protocol work anywhere git does.

## Why the always-on context is ~15 lines

A seal is small; that is the point. Based on
[arxiv 2602.11988](https://arxiv.org/abs/2602.11988), redundant context
*reduces* task success and inflates reasoning cost — the model already knows
SOLID, DRY, and "read before edit". SpecSeal ships only what changes default
behavior; everything else loads when summoned (skills) or works outside the
context entirely (hooks).

## The chancery

| Who / what | Office |
|---|---|
| **smith** (agent) | Forges and reforges the work, and stamps it with the maker's mark — a proof block that cannot be filled without reading the spec |
| **warden** (agent) | Keeper of the seal. Tests the work — spec compliance first, then quality — and only then grants the mark the commit gate demands |
| **scribe** (agent) | Copies faithfully, never editorializes. Fetches what the original code truly does, as coordinates, and keeps the ledger honest |
| Skills | The methodologies each office follows (`implement`, `code-review`, `legacy-parity`, `evidence-check`, `writing-style`, plus quality utilities) |
| Hooks | The gates themselves — auto-registered by the plugin, no settings wiring |
| CLAUDE.md block | The ~15 always-on lines (language, tooling, two safety rules, git) |

## The chain

```
smith forges → verify → warden tests → report to the user
      ↑                                        │
      └── reforging (user's call) ← user decides
commit  → passes only with the warden's seal on this cycle (hook-enforced, approvable)
```

The smith forges and stamps; the warden grants the seal; the scribe keeps
the ledger.

## The ledger

Cross-session memory lives in the repo, not the session:

| Root | Lifetime | Holds |
|---|---|---|
| `docs/` | permanent | policies, the evidence ledger (spec clause ↔ code coordinates), follow-ups |
| `specs/` | one work item | SDD set: spec, plan, questions, closing overview |
| `_ai/` | between sessions | review rounds and todo handoffs — committed, drained, then deleted per PR |

Missing files bootstrap from `templates/`. The handoff convention is
specified tool-agnostically in
[docs/review-handoff-protocol.md](./docs/review-handoff-protocol.md) — any
agent that reads and writes files in a git repo can conform.

And the ledger is *checked*, not merely kept: the `evidence-check` skill
ships a CI-ready script that fails the build when a spec-to-code coordinate
stops resolving, and flags ranges touched since the ledger's baseline commit
for re-verification. Specs rot silently everywhere else — here the rot is a
red build.

## The gates

Hooks are scripts the plugin auto-registers; they run on your machine at
tool events. Full decision tables:
[docs/worktree-guard-spec.md](./docs/worktree-guard-spec.md) ·
[docs/review-chain-spec.md](./docs/review-chain-spec.md).

| Gate | Fires | Does | Where |
|---|---|---|---|
| commit-review-gate | before `git commit` | asks when the cycle bears no seal (`[no-review]` skips, visibly) | repos with `_ai/` at the root — silent elsewhere |
| review-history-guard | after posting/reading a PR review via `gh` | reminds to write / read `_ai/review-history/PR-n/` | same opt-in |
| worktree-guard | before branch switches and worktree creation | blocks switches under another ACTIVE session; quiet sessions get a question, not a wall — with forensics (host app, per-signal ages, last message) | any git repo |
| session-lease | after every tool call | stamps "this session works this tree" into `.git/specseal-leases/` — declaration beats inference | any git repo |
| lint-python | after writing a `.py` file | ruff auto-format (uv → uvx → global; silently skips if none) | any project |

No gate sends anything anywhere — they read local process/git/file state and
print their verdicts to Claude Code.

## Honoring the original (migrations)

A repo that declares `docs/parity.md` (original repo, baseline commit) gets
three-way judgment — policy ↔ original ↔ new, with *preserve the original*
as the fallback — and the scribe fetches the original's facts. Repos without
the config never see any of it.

## Cheat sheet

**Runs by itself (the gates above — nothing to invoke).**

**Run it yourself:**

| Command | Does |
|---|---|
| `python3 <plugin>/skills/evidence-check/scripts/evidence_check.py . [--strict]` | ledger drift check (the demo GIF) — works without any agent |
| `/preset-setup` | approval-gated semantic merge of the CLAUDE.md block |
| `/security-audit` · `/testing` | coverage checklists |
| `bash install.sh [--project]` / `bash uninstall.sh` | add / remove the CLAUDE.md marker block |

**Inline switches:**

| Switch | Effect |
|---|---|
| `[no-review]` in a commit command | skips the review gate once, visibly |
| `[worktree-ok]` in a worktree command | softens the single-stream worktree deny to ask |
| `WORKTREE_GUARD_IDLE_MIN=n` | idle threshold in minutes (default 5) |
| `SPECSEAL_LANG=ko\|en` | gate prompt language (default: English / system locale) |

## Install

```bash
# 1. Plugin (agents + skills + gates)
claude
> /plugin marketplace add MichaelYcJo/SpecSeal
> /plugin install specseal@specseal

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
for human-facing docs only (this README). One deliberate exception: the
writing-style skill carries per-language prose rules (Korean and English
sections) — independent norms, not mirrors, so the drift argument does not
apply. Response language is set by the CLAUDE.md block, independent of
instruction language.

## License

MIT
