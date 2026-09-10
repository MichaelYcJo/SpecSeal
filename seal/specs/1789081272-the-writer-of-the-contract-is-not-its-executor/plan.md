# Implementation Plan: the writer of the contract is not its executor

Approved 2026-09-11 by the repository owner, when `smith` was spawned.

<!-- One line ahead of `templates/sdd-plan.md`, the same deliberate divergence
`questions.md` carries: phase 3 is what brings the template to this shape, and
the line is written in the spelling `templates/sdd-routing.md`'s `Answered`
line already has. Nothing else tells a later session or CI that a person saw
this plan. -->

## Summary

Five phases. The definition first, because every case parametrised on
`agents/*.md` starts covering it the moment it lands and a definition that
arrives red tells you which of them you missed. Then the two moves — the
skills out of the design gate, the drawing-holds check into the smith. Then
the two templates. Then the fourth axis. Then the measurement, which is the
only phase whose failure mode is a wrong number rather than a wrong sentence.

The order is not free. Phase 1 is what makes phases 2 and 8-of-scope
mechanically checkable: with the fifth file in the glob, `agents/sealer.md`'s
*three definitions that stay silent* is a sentence a case can count against,
and until it lands the count is four and true.

## Technical context

Existing code and documents this builds on.

| Coordinate | What it gives |
|---|---|
| `agents/sealer.md` | the model for a definition that arrives complete: contract opening, `## What you are`, the one write named under §6, the report shape. It is the newest definition and the one written after §6 stopped carving exceptions |
| `skills/agent-contract/SKILL.md` §6 | the grant mechanism. A write is granted by being written into the definition that takes it, so `agents/framer.md` naming three files is the whole permission |
| `agents/smith.md` phase 2, the paragraph beginning `Two skills are yours to call when the gate needs them` | what moves out |
| `agents/smith.md` phase 3 | where *the smith's first act on a drawing is to say whether it holds* lands, beside the phase record it already writes |
| `templates/sdd-phase.md` | #121's channel, already shipped. The handover half of a phase prompt has a durable home, which is what made this ticket designable |
| `hooks/routing.py` `parse()` and its docstring | the terms the third axis is read on, written out at length. The fourth copies them |
| `hooks/routing.py` `table_rows()` docstring | *unknown labels are left in rather than filtered … cannot gain a third axis later* — the promise this axis arrives on |
| `skills/verify/scripts/session_cost.py`, the block comment above `DELEGATING` | the join, measured: a segment's transcript opens at its spawn's result stamp, 61 of 67 within one second, the six misses being subagents of subagents |
| `skills/verify/scripts/session_cost.py` `subagent_transcripts()`, `token_totals()` | the walk and the token sum already exist. What is missing is time |
| `tests/test_broad_gate_rule.py#test_only_one_definition_assigns_the_broad_gate` | written for this release's arrival, and its docstring says so |
| `tests/test_every_agent_reads_the_contract.py`, `tests/test_a_moved_rule_leaves_its_definition.py` | both glob, so both cover the fifth file on the day it lands |

**Constraints.**

- `agents/framer.md` must not carry `spawned for exactly that` — S2.
- `agents/framer.md` goes into `tests/test_docs_line_wrap.py`'s `COVERED` at
  birth, wrapped from its first line. `smith.md` and `scribe.md` are outside
  it because bringing them under is a sweep; a new file has no sweep to owe.
- `docs/flow.md` step 2 is pinned twice — the terminal phrase and the order of
  the draft PR against the rounds. S12.
- No real identifiers anywhere, fixtures included
  (`tests/test_no_real_identifiers.py`).

**The failure scenario of the chosen approach, at six months.** The framer
becomes a spawn the orchestrator makes out of habit and the frame it returns
is a summary of the ticket rather than a dossier a smith can build from. Every
`smith` then re-reads the repository anyway, the token count does not move,
and the separation argument is satisfied while the measured cost sits exactly
where it was. That is the shape #84's own last comment names, and phase 5 is
what makes it visible: if `smith`'s span and tokens do not fall against
#263's baseline — 378k tokens, 141 tool calls, 37 m 50 s — the frame was not
complete. The measurement is in scope for that reason and not as a
convenience.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| `framer` as a fifth agent definition, spawned where the ladder calls for a `spec.md` | The frame is thin, `smith` re-reads the repository, and the cost argument goes unmeasured while the separation argument reads as satisfied | **Chosen.** Phase 5 is what makes the failure visible instead of arguable |
| A second `smith` spawn with a framing prompt — what #107 actually ran | It measured well: the frame decided things the phases executed without re-deciding, 23.6 s per turn while deciding against 9.4–10.2 s while applying. What it cannot fix is the anchor: the writer of the contract and its executor are one agent type, so `warden`'s *spec compliance first* still has nothing to check against that a different party wrote | Rejected. The gain is real and is about the SEGMENT, not the agent; the anchor is what this ticket is for |
| The framer writes a prompt per phase | #107's orchestrator wrote five prompts of about a page each and every one was assembled from `plan.md`'s row plus the previous phase's handback — both already written down. Commissioning a document per storey from whoever drew the building | Rejected, and the ticket's own correction says so: the framer draws well enough that a spawn prompt is a pointer at the row |
| The previous phase writes the next one's prompt | Phases 3 and 4 of #107 did exactly this unasked, which is evidence it is natural — but it makes the drawing's author and the build order's author different parties again, one level down | Rejected as the mechanism, kept as the content: `phases/phase-N.md` is where a phase hands forward, and #121 already shipped it |
| A fourth checkbox in the routing question | Eight combinations become sixteen, and the box asks a person something the ladder already decided. #88 states the rule this would break: *the question grows only when a decision is genuinely a person's* | Rejected. `Planning` is a record |
| A second module beside `hooks/implementer.py` for the second mark | Two files whose `git_dir`, `write` and `stands` differ by a constant. This repository has paid for that shape twice already and written both down — contract §11 and §16 each record a rule that *sat in two definitions in near-identical words* while a third carried none | Rejected. One module, two constants, one reader — which is what `implementer.py`'s own docstring argues for |
| Leave `session-cost` alone and ship the framer on the separation argument | The one clause of #84's reasoning that was measurable was measured and pointed the other way — phases 1–2 came in at the baseline, 1.30 tools/turn against 1.27. Shipping a fifth agent with no way to read its cost is how the next argument gets made from taste | Rejected. The owner's answer of 2026-09-11 keeps it in |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `agents/framer.md` — contract opening verbatim, `## What you are`, the three writes named under §6, what it reads, the report shape. `tests/test_docs_line_wrap.py` `COVERED` gains it | `test_every_agent_reads_the_contract` and `test_a_moved_rule_leaves_its_definition` at five files · `test_only_one_definition_assigns_the_broad_gate` still `["sealer.md"]` · `test_docs_line_wrap` on the new path · each shown red first per §15 | `51ff098` |
| 2 | The two moves. `feature-planner` and `confidence-check` leave `agents/smith.md`'s design gate for `agents/framer.md`; the smith's first act on a frame becomes *say whether it holds*, with `phases/phase-N.md` named as where a *no* goes (Q3's default). `agents/sealer.md`'s *three definitions* reads four | a new case asserting the two skills are callable in exactly one `agents/*.md`, counted from the glob · a new case pinning the drawing-holds sentence and its home · a case counting the silent definitions from the glob rather than from a list | `dcfd693` |
| 3 | `templates/sdd-plan.md` gains `Approved <date> by <who>`, written when `smith` is spawned. `templates/sdd-questions.md` gains the answerer column — *a person* · *a measurement* · *the work* — and the sentence that the framer opens rows rather than answering them. `skills/implement/SKILL.md` §3's file table gains the two facts and names who writes each file | a case comparing the approval line's spelling against `templates/sdd-routing.md`'s `Answered` line · a case pinning the three answerer values and the opens-rather-than-answers sentence · both shown red first | |
| 4 | The fourth axis. `templates/sdd-routing.md` gains the `Planning` row; `hooks/routing.py` gains `PLANNING`, `BY_FRAMER`, `PLANNING_ANSWERS` and the `planning` key, read on the third axis's terms; `skills/implement/orchestration.md` gains the row as a record with #88 cited for why it is not a box | S8 and S9 · `test_every_declaration_in_this_repository_still_parses` over every declaration in the tree, none of which has the row · a case per answer · a case that the commit gate decides identically with the row and without it · the vocabulary parsed out of `templates/sdd-routing.md` so it cannot drift | |
| 4b | **The mark, Q1's answer against its own default.** `hooks/implementer.py` holds a SECOND mark rather than a second module beside it — the file is *named for the axis rather than for the agent* by its own docstring, and one reader for two axes is the whole reason it is a module. `hooks/implementer-notice.py` prints for either axis whose declared agent left no mark, still once per repository per session. The `pre-agent` gate that writes the mark learns `framer` beside `smith` | a case per axis for `write`/`stands`, each shown red first · a case that a mark for one axis does not answer for the other, the shape `stands`'s branch-scoping already has · a case that the notice fires once for two unfulfilled axes rather than twice · the notice's PostToolUse standing unchanged: it never blocks | |
| 5 | `session_cost.py` reports time per agent from the subagent transcripts: one row per segment, named by its spawn's `subagent_type`, with its own span, calls, tools-per-turn, gap and tokens; the segments it could not name counted and printed rather than dropped | a case over a built transcript tree with a named segment, an unnamed one and a nested one · the join asserted on the measured stamp rather than assumed · a case that a missing `subagents/` directory prints a reading rather than raising · executed, with the mutation per new unit | |
| 6 | `docs/flow.md` — step 2 loses *once #84 exists*, 0.11.0's section ticks its box. The fragments: `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md`. The closing memo | S12 executed · `fold_ledger.py --check` · the release-hygiene case | |

**Status is empty, or the commit that closed the phase.** Re-read the column
after any rebase.

What a phase discovers while building goes to
`seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes.

## Operational impact

- **A new agent reaches every user of the plugin.** `agents/framer.md` is
  shipped, so the agent set goes from four to five for everyone, and a
  session that spawns by name gains a name. Nothing existing is renamed and
  nothing is withdrawn.
- **`hooks/routing.py` gains a key.** Additive: every declaration already
  committed parses unchanged and reads `planning: None`. No migration, and no
  declaration has to be rewritten.
- **Two templates change shape.** A work item mid-flight that copied the old
  `plan.md` or `questions.md` keeps working — both additions are a line and a
  column, and nothing parses either file.
- No new dependency, no env var, no compatibility break.
