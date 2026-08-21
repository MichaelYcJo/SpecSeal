# SpecSeal

[![tests](https://github.com/MichaelYcJo/SpecSeal/actions/workflows/test.yml/badge.svg)](https://github.com/MichaelYcJo/SpecSeal/actions/workflows/test.yml)

**English** · [한국어](./README.ko.md)

**Specs, sealed** — when code moves under the line a spec cites, CI says so.

![SpecSeal demo: evidence-check catches spec-code drift](./assets/demo.gif)

Coding agents make claims. SpecSeal makes each claim leave something you can
open: a **proof block** the smith prints naming the policy files it read and
what it actually ran, a **review mark** (`.git/specseal-reviewed`, holding the
reviewed HEAD sha) that a commit hook looks for, and an **evidence ledger**
(`docs/**/_evidence.md`) pairing each spec clause with the `file:line` that
grounds it.

Commit without a current review mark and the hook asks before letting it
through. Move the lines a ledger row cites and the check script exits
non-zero. Neither is a wall — both are a record you have to walk past
knowingly.

Distributed as a Claude Code **plugin**; the ledger, the drift checker, and
the handoff protocol work anywhere git does.

## Why the always-on context is ~15 lines

A seal is small; that is the point. Based on
[arxiv 2602.11988](https://arxiv.org/abs/2602.11988), context files generally
do *not* improve task success while adding over 20% inference cost — the model already knows
SOLID, DRY, and "read before edit". SpecSeal ships only what changes default
behavior; everything else loads when summoned (skills) or works outside the
context entirely (hooks).

## What ships

| Who / what | What it concretely is |
|---|---|
| **smith** (Claude Code subagent) | Implements against the spec, then prints a three-line proof block: which policy files it opened, which ledger rows it touched, what it executed versus merely read. The block is a disclosure the skill requires, not something a hook verifies — but `none — <reason>` in a row is visible to you |
| **warden** (subagent) | Reviews spec compliance first, then quality. Passing writes the reviewed HEAD sha to `.git/specseal-reviewed`, which is what the commit gate looks for |
| **scribe** (subagent) | Records what the original code does as `file:line` coordinates and returns facts, not verdicts. Appears only in repos that declare `docs/parity.md` |
| Skills | The methodologies each one follows (`implement`, `code-review`, `legacy-parity`, `evidence-check`, `writing-style`, plus quality utilities) |
| Hooks | The gates themselves — auto-registered by the plugin, no settings wiring |
| CLAUDE.md block | 12 always-on lines: tooling preferences, two safety rules, one git rule. No response-language rule — that stays yours |

## The chain

```
smith forges → verify → warden tests → report to the user
      ↑                                        │
      └── reforging (user's call) ← user decides
commit  → the hook asks unless .git/specseal-reviewed matches HEAD; approving is the waiver
```

`verify` is the smith's own gate before it hands anything over: run the
checks, read the full output, and label each claim as executed, read, or
unverified. The warden then audits that record instead of re-deriving it.
Whether a report leads to more work, another review, or a commit is yours to
decide — the chain stops at the report.

## The ledger

Cross-session memory lives in the repo, not the session:

| Root | Lifetime | Holds |
|---|---|---|
| `docs/` | permanent | policies, the evidence ledger (`docs/**/_evidence.md` — each spec clause paired with the `file:line` that grounds it), follow-ups |
| `specs/` | one work item | SDD set: spec, plan, questions, closing overview |
| `_ai/` | between sessions | review rounds and todo handoffs — committed, drained, then deleted per PR |

Missing files bootstrap from `templates/`. The handoff convention is
specified tool-agnostically in
[docs/review-handoff-protocol.md](./docs/review-handoff-protocol.md) — any
agent that reads and writes files in a git repo can conform.

The ledger is *checked*, not merely kept. The `evidence-check` skill ships a
CI-ready script that exits 2 when a coordinate no longer resolves and 1 when
its lines were touched since the ledger's baseline commit; both fail a default
CI step, and `--strict` makes drift exit 2 as well. What it proves is narrow
and worth stating: that the citation still points somewhere, not that the
claim it supports is still true. Specs rot silently everywhere else — here
the rot shows up in CI.

## The gates

Hooks are scripts the plugin auto-registers; they run on your machine at
tool events. Full decision tables:
[docs/worktree-guard-spec.md](./docs/worktree-guard-spec.md) ·
[docs/review-chain-spec.md](./docs/review-chain-spec.md).

| Gate | Fires | Does | Where |
|---|---|---|---|
| commit-review-gate | before `git commit` | asks when `.git/specseal-reviewed` does not hold the current HEAD sha (`[no-review]` in the command skips it, and stays visible there) | repos with `_ai/` at the root — silent elsewhere |
| review-history-guard | after posting/reading a PR review via `gh` | reminds to write / read `_ai/review-history/PR-n/` | same opt-in |
| worktree-guard | before `git checkout`/`switch`, `git worktree add`, and Agent calls with `isolation: "worktree"` | one rule in two directions: denies a switch while another session is actively working this tree, and denies creating a worktree when yours is the only live stream (`[worktree-ok]` downgrades that to a question). Idle sessions and undetectable environments get a question, not a block. The reason names the other session's host app, how long each signal has been quiet, and its last message | any git repo |
| session-lease | after repo-touching tool calls (Bash · file edits) | writes a timestamp to `.git/specseal-leases/<session-id>`. The guard's process heuristics miss sessions not named `claude`; a lease says outright which session is working here | any git repo |
| lint-python | after Write/Edit/NotebookEdit on a `.py` file | runs `ruff check --fix` then `ruff format` on that file — lint autofixes included, so content can change (uv → uvx → global ruff; skips silently if none) | any project |

No gate transmits your code or your prompts anywhere. Two side effects are
worth stating outright: session-lease writes a timestamp file under
`.git/specseal-leases/`, and lint-python rewrites the `.py` file you just
saved. lint-python is also the one hook that may touch the network — if it
falls back to `uvx ruff`, uv fetches ruff from PyPI on first use.

One deliberate read to know about:
when the worktree-guard blocks a switch, it quotes the last user message
(80 chars) of the OTHER local session's transcript in its block reason, so
the human can recognize which conversation is being protected. That snippet
stays on your machine.

## Honoring the original (migrations)

A repo that declares `docs/parity.md` (original repo, baseline commit) gets
three-way judgment — policy ↔ original ↔ new, with *preserve the original*
as the fallback — and the scribe fetches the original's facts. Repos without
the config never see any of it.

You do not write that file by hand. The smith asks once, the first time it
sets up a repo's layout: *does this project port behavior from an existing
codebase?* Answer no and it never asks again. Answer yes and it proposes
candidates for the original — sibling checkouts, an upstream in `git remote
-v`, repos whose paths overlap — reads the baseline from whichever you
confirm, and writes the file. Deciding later is `/specseal:parity-setup`.

Your checkout path stays out of the committed file, in
`~/.claude/specseal/parity-paths.md` keyed by the origin remote, since it is
wrong for every other machine.

## Cheat sheet

**Runs by itself (the gates above — nothing to invoke).**

**Run it yourself:**

| Command | Does |
|---|---|
| `evidence-check . [--strict]` | ledger drift check (the demo GIF) — works without any agent. The plugin puts it on PATH; for CI, vendor the script into your repo (see `templates/evidence-check.yml`) |
| `/specseal:preset-setup` | approval-gated semantic merge of the CLAUDE.md block |
| `/specseal:parity-setup` | declare that this repo ports from another codebase — finds the original, records the baseline |
| `/specseal:security-audit` · `/specseal:testing` | prompt checklists the model walks — an OWASP-shaped security pass and a test-strategy pass |
| `bash install.sh [--project]` / `bash uninstall.sh` | add / remove the CLAUDE.md marker block |

**Inline switches:**

| Switch | Effect |
|---|---|
| `[no-review]` in a commit command | skips the review gate once, visibly |
| `[worktree-ok]` in a worktree command | softens the single-stream worktree deny to ask |
| `WORKTREE_GUARD_IDLE_MIN=n` | idle threshold in minutes (default 5) |
| `SPECSEAL_LANG=ko\|en` | worktree-guard's prompts (the other gates are English-only); default follows the system locale |

## Install

**Requirements**: `git`, and `python3` on PATH — the gates are Python
scripts (preinstalled on macOS and most Linux distros; on Windows install
Python 3 and make sure `python3` resolves). Optional: `uv`/`uvx` or `ruff`
for the Python auto-format hook — without them it silently skips.

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
`/specseal:preset-setup` inside Claude Code instead — every deletion goes through an
approval diff.

## First run

Two of the five gates wake only under a condition: the commit gate and the
review-history reminder act in a repo that has an `_ai/` directory at its
root, and stay silent everywhere else. You never create that directory by
hand — the smith builds the layout, `_ai/` included, the first time it works
in a repo.

The other three carry no condition. worktree-guard and session-lease act in
every git repo, and lint-python rewrites every `.py` file you save. Read the
Where column above before installing globally.

Agents run only when you name one:

```
> use the specseal:smith agent to implement <your ticket>
```

The smith reads the spec chain, implements, verifies, and hands off to the
warden for review — you decide what happens to the report. Anything the
layout needs and the repo lacks (`docs/policies/<domain>/_evidence.md` with
its baseline stamped, `_ai/README.md` carrying the export rules) the smith
creates from `templates/` as it goes.

Two things work with no agent at all: the ledger drift check
(`evidence_check.py`, the demo above) and every gate in the table.

## Limits

What this does not do is as load-bearing as what it does.

- **The gates ask; they do not block.** The commit gate emits a prompt, and
  approving it is the waiver. `[no-review]` in the command skips it outright.
  It is a speed bump for an agent about to commit unreviewed work, not a
  security control — anyone who can approve a prompt can commit.
- **evidence-check proves a citation still resolves, not that it is true.**
  `DRIFTED` means someone must re-verify, not that the claim is wrong. A
  coordinate that still resolves while the code's meaning changed reports
  `OK`.
- **The proof block is a disclosure, not enforcement.** No hook reads it. Its
  value is that a `none — <reason>` row is visible to you in the transcript.
- **Session detection is heuristic.** Extension-hosted sessions aren't named
  `claude`, and a session editing this tree from another cwd leaves no trace
  here. Leases close most of that gap, but only for sessions that have run a
  tool recently. Where detection is unusable the guard asks instead of
  deciding.
- **Windows is untested on real hardware.** Hooks run through an explicit
  `python3` rather than relying on shebangs and exec bits, which should be
  enough — but nobody has run them on Windows.
- **The conformance evals have never run.** `evals/` is written against
  `claude plugin eval`, which is early access; the suite awaits enablement.
  Treat it as authored, not as passing.

## Contributing

Changes to a gate carry a higher bar than the rest of the tree, because a gate
decides whether someone's commit proceeds: a test seen failing before the fix,
a stated failure direction, and honesty about platforms you could not test.
See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Language policy

Functional files (skills, agents, hooks, commands) are English-only — they
load into model context, and a translated mirror would drift. Korean exists
for human-facing docs only (this README). One deliberate exception: the
writing-style skill carries per-language prose rules (Korean and English
sections) — independent norms, not mirrors, so the drift argument does not
apply. Response language follows the user's own CLAUDE.md settings — the
distributed block does not impose one.

## License

MIT
