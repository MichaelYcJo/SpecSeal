# Feature Specification: a payload is written again on every spawn

<!-- seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Issue #292. The first work item of 0.10.0, and the one the other three are
measured with: #120 removes sections from a payload, and a before-and-after
number is the only thing that says whether that worked.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | The deliverable is a check that can fail, not a sentence. A section marked for one role that sits in another role's payload is caught by a test, not by a reader |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The new test and the new hygiene step each carry a red-first case, a stated failure direction, a prompt budget (zero — nothing here asks anyone anything), and platform honesty |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | Changelog and ledger rows go to this work item's fragments; rows this work removes from `seal/ledger.md` are REMOVED there, and the new claims are written here |
| `docs/flow.md` §*0.10.0 — the agent set* | The meter comes before #120's trimming. This work item ships the meter and a first before-and-after of its own |
| #292 §*What to build* and §*Not this* | Two units: a meter in tokens, and an audience marker with a check behind it. Not: replacing rules with coordinates, a speed claim, trimming `agent-contract` per role |
| `skills/code-review/orchestration.md` (#265) | The shape `implement` follows: the orchestrator's sections move to a sibling file, the headings keep their names, the skill's first section is the pointer |
| `skills/agent-contract/SKILL.md` §16 | Every `seal/…` path in the moved text keeps meaning what it meant |

## Scope

**In.**

1. **A payload meter, in tokens.** `skills/verify/scripts/payload_meter.py`
   with a `bin/payload-meter` wrapper (and its `.cmd` twin, the way every
   other `bin/` entry has one). For each `agents/*.md` it resolves the
   definition's own `skills:` list to files and reports the payload's
   composition — the definition, each injected `SKILL.md`, and the two
   `CLAUDE.md` files the harness injects — in bytes, characters and tokens,
   per file and as a total, with `--sections` splitting each file at its
   `##`/`###` headings. `--json` writes the same as data; `--baseline
   <json>` prints the delta against an earlier run; `--calibrate <main
   transcript>` reads the measured whole-payload token count of every
   agent the transcript spawned, from the first assistant message of each
   subagent transcript, and derives one bytes-per-token ratio per agent.
   Every token figure carries a **basis**: `measured` where it came from a
   transcript, `estimated (<ratio>, from <agent>)` where it came from a
   ratio — never a bare number.
2. **An audience marker with a check behind it.** The marker is the heading
   prefix `Orchestrator:` that `skills/code-review/SKILL.md` already used
   and `orchestration.md` keeps. `implement` adopts it: the sections
   addressed to the session that spawns agents are marked and moved to
   `skills/implement/orchestration.md`, and `skills/implement/SKILL.md`
   opens with the pointer section `code-review` has. A new test module
   fails when a heading carrying the marker sits in a file some agent's
   `skills:` list injects, and when an `orchestration.md` is itself listed
   under any `skills:`.
3. **The cut, named by paragraph so nobody re-judges it.** Out of
   `skills/implement/SKILL.md`, in full: `### Bootstrap — create what's
   missing` and `### Parity setup — deriving what can be derived`. Out of
   `### 1. Read the spec before the code`: from the paragraph opening
   **How this work is routed is one of them, and it has three axes** up to
   and not including **Once the batch is answered, the session runs to the
   pull request** — the axis table, the checkbox table, the two commands
   about writing `routing.md`, the four-combination table, the wake/quiet
   table with its `# RIDER:`, the `straight to the PR` sentence, the branch
   table, the gather sentence, and the standing-waiver paragraph. Two
   paragraphs inside that span STAY, because #292 assigns the waiver
   mechanics to the implementer: **`[no-review]` still works and is
   unchanged** and **For a change that belongs to no work item at all**,
   merged into one paragraph that no longer refers to a table the reader
   cannot see. Everything before the span (judgment precedence, the four
   bullets, the one-batch rule, the two sharpeners, the yes/no tell) and
   everything after it stays.
4. **The 22 test modules that name `skills/implement/SKILL.md`** are each
   run; a case whose pinned sentence moved is re-pointed at
   `orchestration.md`, never duplicated and never deleted, and each
   re-pointed case is shown red against the file it left (§15). The 22 are
   listed in `plan.md`.
5. **Every document that sends a reader to a moved section** names the new
   file: the `CLAUDE.md` block's *load the `implement` skill, and follow its
   Bootstrap section*, `README.md` and `README.ko.md` where they name the
   Bootstrap, `agents/smith.md`, `templates/*.md`, `docs/*.md`.
6. **The `CLAUDE.md` block has one source.** `templates/claude-md-block.md`
   holds the marker block; `install.sh` reads it from there instead of from
   the repository's `CLAUDE.md`; `.github/scripts/claude_block.py --write`
   regenerates the block inside `CLAUDE.md` from it and `--check` exits 1
   when the two differ; the hygiene workflow runs `--check`; the
   `preset-setup` and `update` skills, which read the block at runtime,
   name the template path. The repository's `CLAUDE.md` keeps the generated
   copy, by the owner's answer (Q1).
7. **The `# RIDER:` inside the moved span is answered, not carried.** It
   asks for the arm to be named in the sentence *when this section is next
   opened*. This is that opening: name the arm and delete the rider.
8. **The ledger.** Twelve rows in `seal/ledger.md` anchor on
   `skills/implement/SKILL.md#<heading>`. A row whose anchor moves with its
   text is REMOVED from `seal/ledger.md` and re-stated as a new row in this
   work item's fragment at the new coordinate; a row whose anchor stays is
   left alone and re-verified only if its hash drifted.
9. **The before and the after.** `payload-before.json` (taken before the
   first edit, from the six calibration transcripts) and
   `payload-after.json` are committed under this work item, and the delta
   table goes into `changelog.md` and the pull request body.
10. `changelog.md`, `seal/ledger/<id>.md`, `overview.md`, a
    `phases/phase-N.md` per phase, and the tick in `docs/flow.md`.

**Out.**

- **Trimming `agent-contract` per role.** #120's, and it lands last in this
  release for a reason `docs/flow.md` states.
- **`agents/smith.md`'s own routing paragraph** (its design gate, step 2,
  from *How the work is routed belongs in that batch* through the waiver
  example and its `# RIDER:`). It restates the span this work moves, and by
  #292's own judgment it is the orchestrator's — but it moves with the
  design gate in #84, which takes that whole step to the framer. Moving it
  twice is the duplication #107 measured, so it waits one work item.
- **Exact per-file token counts.** They need a probe agent definition whose
  only preloaded skill is the file measured, and a definition written under
  `.claude/agents/` is read at session start, not at spawn — six such
  probes were tried this session and none was spawnable. `questions.md` Q4
  carries it as a measurement the next session can take; the meter's
  `--calibrate` is built to read it when it exists.
- **A speed claim.** Tokens per spawn only.
- **Reducing the two `CLAUDE.md` files' share of a payload.** Q1's answer
  keeps the repository copy; what the build step buys is that the two
  copies cannot drift, which they had (the issue measured `## Git` at 95 %
  identical). The meter reports the pair as its own line so the cost is a
  number rather than a suspicion.

## Measured before the first edit

Six spawns on 2026-09-10, each told *use no tools, reply with one word*,
each on `claude-fable-5-1`, read from the `usage` block of the first
assistant message of each `agent-*.jsonl`. `input_tokens` was 2 in all six,
so the whole prefix is in the two cache columns. **Executed.**

| Spawn | `cache_creation` | `cache_read` | Prefix total |
|---|---|---|---|
| `general-purpose` (no plugin skill; the baseline) | 21,723 | 17,763 | 39,488 |
| `specseal:scribe`, first | 28,291 | 17,763 | 46,056 |
| `specseal:scribe`, again within five minutes | 0 | 46,054 | 46,056 |
| `specseal:warden` | 64,188 | 0 | 64,190 |
| `specseal:smith`, first | 75,781 | 0 | 75,783 |
| `specseal:smith`, again within five minutes | 0 | 75,781 | 75,783 |

Two things the issue did not have, and the meter has to carry both.

**The payload IS cached across spawns of the same agent, for five minutes.**
The second smith and the second scribe wrote nothing and read their whole
prefix back, and every `cache_creation` block reads
`ephemeral_5m_input_tokens` with `ephemeral_1h_input_tokens` at 0 (NAME NOT IN TREE:
the transcript's own fields; the meter reads neither). The
issue's 49 readings saw a write every time because no two spawns of one
agent in a chain fall inside five minutes of each other — a round runs ten
to forty. So the sentence is narrower than *re-written on every spawn*: it is
**re-written on every spawn more than five minutes after the last one of the
same agent**, which in a review chain is every one. The lever that would
amortise it, a one-hour TTL for a subagent's prefix, is the harness's and
not this plugin's; the meter reports what a chain pays and says so.

**Bytes do not track tokens at one ratio across agents.** Subtracting the
baseline: smith's payload is 36,295 tokens for 98,189 B (2.71 B/token),
warden's 24,702 for 78,109 B (3.16), scribe's 6,568 for 22,598 B (3.44).
The Korean-heavy `writing-style` explains part of the spread — smith and
warden both carry it, scribe does not — and not all of it: swapping
`implement` + `agents/smith.md` for `code-review` + `agents/warden.md` costs
11,593 tokens for 20,080 B of English prose, twice what 3.4 B/token
predicts. Something in the smith's prefix is not in the byte accounting, and
it is not one of the files this work moves. The meter therefore reports a
per-agent measured ratio and labels every per-file figure as an estimate
from it, and Q4 is the probe that would settle the per-file numbers.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the meter reports composition | Given the plugin tree, when `payload-meter` runs, then one table per agent lists its definition, each injected skill and the two `CLAUDE.md` files with bytes, characters, tokens and a basis, plus a total; `--sections` splits each file at its headings; `--json` writes the same as data | a case over a fixture `agents/` + `skills/` tree with known sizes; the real tree run and its output read |
| S2 measured beside estimated | Given a main transcript whose `Agent` calls name `subagent_type` and whose results carry `agentId`, when `--calibrate <transcript>` runs, then each agent's row carries its measured prefix total minus the baseline agent's, and the ratio the estimates use; without `--calibrate`, every token figure reads `estimated` and names the ratio's origin | a fixture transcript pair (main + `subagents/`) with hand-written `usage` blocks; a case that a transcript naming no baseline agent says so instead of subtracting zero |
| S3 before and after | Given `payload-before.json`, when the meter runs with `--baseline` after the move, then the smith row shows the bytes and estimated tokens that left it, and the check's sum over the two `implement` files equals the file before the split | the two JSON files committed here, and the delta in `changelog.md` |
| S4 the check can fail | Given a copy of the tree with an `Orchestrator:` heading planted in a file some agent's `skills:` injects, when the new test module runs, then the case names the agent, the skill file and the heading; given an `orchestration.md` listed under a `skills:`, the same | the module's own red-first cases; and the real tree seen red between marking the three sections and moving them (the phase record says at which commit) |
| S5 the split | Given the move, then `skills/implement/SKILL.md` has no `Orchestrator:` heading, opens with a pointer section naming `orchestration.md`, and every moved heading appears in `orchestration.md` with its text unchanged except the arm sentence the rider asked for | `git diff` read in the round; the check green; the meter's after-run |
| S6 the re-pointed cases | Given each of the 22 modules, when its pinned sentence moved, then the case reads `orchestration.md` and is shown red with the sentence stashed from that file | the phase record lists each module and the red seen |
| S7 one source for the block | Given `templates/claude-md-block.md`, when `claude_block.py --check` runs with the repository's `CLAUDE.md` block edited by one byte, then exit 1 naming the first differing line; `--write` restores it; `install.sh` names the template as `SOURCE`; hygiene runs `--check` on every pull request | a test module with the one-byte mutation; `bash install.sh /tmp/x.md` on a scratch target read afterwards |
| S8 nothing asks anyone | Given all of the above, then no new question reaches a person in any session — the meter, the check and the block script each exit with a message | the pull request body's prompt-budget line, and `grep -rn AskUserQuestion` over the new files returning nothing |

## Data & interfaces

**`payload-meter`** — `payload-meter [--root DIR] [--agent NAME …]
[--sections] [--json] [--baseline FILE] [--calibrate TRANSCRIPT
[--baseline-agent general-purpose]]`. `--root` defaults to the plugin root
resolved from the script's own location, so it works from the version cache
and from a clone. The JSON shape:

```json
{"measured_at": "<iso date>", "root": "<path>", "ratios": {"smith": {"bytes_per_token": 2.71, "from": "agent-<id>.jsonl"}},
 "agents": {"smith": {"files": [{"path": "agents/smith.md", "bytes": 18413, "chars": 18391, "tokens": 6795, "basis": "estimated (2.71 B/token, from smith)"}],
                      "total": {"bytes": 113633, "chars": 105712, "tokens": 36295, "basis": "measured (agent-<id>.jsonl)"}}}}
```

**The marker** — a heading whose text starts `Orchestrator:`, at `##` or
`###`. Nothing else is machine-readable about it.

**`claude_block.py`** — `--write` and `--check`, the template path and the
target defaulting to the repository's own; exit 0 / 1 / 2 (2 for a target
with no markers, which is not a disagreement but a file the script cannot
place a block in).

**`skills/implement/orchestration.md`** — headings: `## Orchestrator:
Bootstrap — create what's missing`, `## Orchestrator: Parity setup —
deriving what can be derived`, `## Orchestrator: how the work is routed —
three axes, one question, one file`. The first two keep their old text
after the colon so a reader searching for the old heading still lands.

## Open questions → questions.md

Anything a planner must answer lives in `questions.md`, not inline —
unanswered questions buried in prose read as decided.
