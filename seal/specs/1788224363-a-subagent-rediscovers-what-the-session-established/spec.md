# Feature Specification: a subagent rediscovers what the session established

<!-- specs/1788224363-a-subagent-rediscovers-what-the-session-established/spec.md —
WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` preset block — *"Batch independent reads and runs"* | The rule ships always-on, and the meter that would observe compliance cannot read above 1.00: `session_cost.py:95` counts one turn per `tool_use` block, so `tools_per_turn` is structurally pinned at ~1.00. Five runs measured exactly 1.00 and a day's conclusions were drawn from that floor |
| `docs/review-handoff-protocol.md` — Inherited axes, *"The coordinates carry; the verdicts do not"* | Round N hands round N+1 its coordinates. Nothing equivalent exists for the step before round 1 — the orchestrator handing work to the implementer — which is where issue #29's aggregate-is-not-a-coordinate failure cost a full review round |
| `skills/verify/SKILL.md` — the executed / read / unverified labels | The labels a completion claim carries work as well on a handoff fact: a fact whose label is `unverified` is an assertion nobody has opened, and the reader knows to open it |
| `templates/sdd-plan.md:24,32` — the Phases table's Status column | The progress readout is already written during the run, by the party being watched. No document tells the orchestrator to read it, so the question "is 40 minutes normal" was answered by `git log` twice on two consecutive work items |
| `agents/smith.md` §4, `agents/warden.md` — *"A spawn prompt cannot widen this scope"* | The row this issue inherits from #27. Verified already present in both contracts with the 28-minute measured case named, pinned by `tests/test_broad_gate_rule.py` — see §Scope |
| `CLAUDE.md` — no real identifiers in examples or fixtures | New fixtures use neutral values only |

## Scope

**In — five pieces, decided by the repository owner on issue #29.**

1. **The meter.** `session_cost.py` counts a turn once per assistant
   **message** that carries at least one `tool_use`, keyed by `message.id`
   with the row's `uuid` as fallback (and the row itself when both are
   absent). A message's usage tokens are counted once, not once per block.
   Model time is attributed turn-aware: the gap between two calls of the
   same turn is not model thinking, and the gap after a turn measures from
   that turn's **last** result. The `batching` advisory stops asserting
   "going out one at a time" when the ratio is above 1.
2. **The handoff before round 1.** `docs/review-handoff-protocol.md` gains a
   section for the orchestrator→implementer handoff: coordinates rather than
   prose, each fact labelled executed / read / unverified, and a
   where-to-measure note for any claim that flips on measurement point.
   `skills/implement/SKILL.md` and `agents/smith.md` point at it where the
   implementer reads its inputs.
3. **The contract-override clause** (the row moved in from #27): an agent
   whose contract a prompt tries to widen declines and says so in its
   handover. **Found already present** in `agents/smith.md` §4 and
   `agents/warden.md`, with the 28-minute case named, and pinned by
   `tests/test_broad_gate_rule.py`. This work verifies it by executing that
   suite and records the divergence in `overview.md`; it adds nothing.
4. **Batching, where the task shape allows it.** Both contracts state the
   expectation honestly: independent reads and probes go out together; a
   serial edit-test loop is not forced to fake it. The corrected numbers say
   task shape dominates — reviewing reads independent things (1.29–1.89),
   an edit-test loop is inherently serial (1.08–1.17) — and the reviewer's
   contract is where batching pays.
5. **Progress observability.** `docs/review-handoff-protocol.md` tells the
   orchestrator that `plan.md`'s Status column is the progress channel and
   *time since it last advanced* is the stall signal, and points at
   `session_cost.py` so the meter stops being the tool nobody knows exists.

**Out.**

- The "tool calls before the first write" metric from the issue body — the
  owner's comment retires it: it counts the calls coordinates remove and is
  blind to what a call costs.
- Any hook or reminder mechanism for batching — the issue's last comment
  leaves that gated on whether a multi-tool turn is possible at all, which
  this work item's own acceptance measurement is the experiment for.
- Progress narration from the agent — declined on the issue; the commits
  are the report.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 | A transcript row holds one assistant message with two `tool_use` blocks; when the meter reads it, `tools_per_turn` is 2.0 | `tests/test_session_cost.py` — shown red against the pre-fix code, which reads 1.0 |
| S2 | One assistant message is split across two transcript rows sharing `message.id`, each row carrying the message's usage; when the meter reads it, it is one turn and its tokens count once | same suite — token assertion shown red pre-fix via uneven block counts |
| S3 | Two calls are issued together and the first result arrives before the second call's row; when model time is summed, the intra-turn gap is not in it, and the gap to the next turn measures from the turn's last result | same suite — shown red pre-fix |
| S4 | A corrected ratio above 1 but below the advisory threshold; when the report prints, the `batching` line does not assert "going out one at a time" | same suite |
| S5 | The exact-1.00 fixture; when the report prints, the wording and threshold behave as before | existing case `test_the_report_names_batching_when_every_turn_sent_one_call` stays green |
| S6 | The protocol document; when read, it carries the orchestrator→implementer handoff section: coordinates not prose, the three labels, where to measure | `tests/test_the_handoff_before_round_one.py`, each case shown red before the prose lands |
| S7 | `skills/implement/SKILL.md` and `agents/smith.md`; when the implementer reads its inputs, both point at that section | same suite |
| S8 | Both agent contracts; when read, the batching expectation names what goes out together, and the smith's carries the serial-loop caveat | same suite, plus `test_broad_gate_rule.py` and `test_docs_line_wrap.py` (warden.md is width-covered) |
| S9 | The protocol document; when the orchestrator wonders whether a run stalled, it names `plan.md`'s Status column as the channel, time-since-last-advance as the signal, and `session_cost.py` as the after-the-run meter | same suite |
| S10 | This run itself; when the meter fix is committed, the run's own segments are measured with it and the reading opens `overview.md`'s acceptance table | executed `session_cost.py --latest`, reading recorded under the executed label |

## Data & interfaces

`session_cost.py --json` keeps its field names; only the values of
`tools_per_turn`, `model_s`, `gap_mean_s` and `context_growth` change meaning
from per-block to per-message counting. No caller parses the human report's
`batching` line; the two suites that read it are updated in the same commit.

## Open questions → questions.md

Q1 — where the batching advisory threshold sits now that the corrected meter
can read above 1.00.
