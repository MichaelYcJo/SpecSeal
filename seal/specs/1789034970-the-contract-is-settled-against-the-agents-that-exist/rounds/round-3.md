# 1789034970-the-contract-is-settled-against-the-agents-that-exist — review round 3

| Field | Value |
|---|---|
| Target SHA | ce0f9fe |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 338 |
| Broad gate | 8310982 against release/v0.10.0 |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 1's missing case. Finding 2 is answerable with grounds and finding 3 is a correction. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of #120 at `ce0f9fe`, the verifying round and the last record this run has, on `docs/120-the-contract-is-settled-against-the-agents-that-exist` against `release/v0.10.0` (`d35c874`), draft pull request #338. The fix range is `de7d693..ce0f9fe`, five commits, 13 files (+306 / −19), closing round 2's eight findings — seven `fixed`, one `answered` and already discharged by the orchestrator running `close`. The round was told its position by `round_record.py` rather than left to judge it: one reopening remained, round 1 met the floor and round 2's verdicts closed on a fix, so this record ends the run whatever it finds — which is a reason to say clearly of anything opened whether it must be fixed before shipping or belongs in an issue with a named answerer, and not a reason to pass anything. The first job was the eight closures, re-derived by reverting each fix alone, running the case it names and quoting the assertion it breaks on. Three were named as the places a closure most easily goes wrong: the parser change to `terminal_value`, which now joins a wrapped continuation and stops at a blank line, at the other terminal label or at a line opening a new markdown block, with the fix pass's own disclosure that its swallow-direction case was green before and after and guards rather than pins; `round-1.md`'s cell repaired by hand from the report with an HTML comment beside it; and `BOUNDS`, where round 2's own mutant — a fifth definition carrying the old parenthetical with no bound — had to be re-run rather than a mutant of the fixer's choosing. The class to enumerate was what else in the tree reads a terminal line or a record cell, because the pass changed a shared parser and a shared checker's vocabulary and `chain.SEPARATORS` is the neighbour the fix pass named itself. Two things were handed over as measured rather than pinned, for the round to weigh: findings 2, 4 and 6 changed no assertion, and the duplication guard was left globbing `agents/*.md` on the grounds that `skills/implement/SKILL.md` sits at 30 words against §5 and 15 against §9, both predating this branch, so widening is a sweep rather than a fix. Facts handed over as executed by the orchestrator at `ce0f9fe`: eleven modules, 398 passed, exit 0, and `round-1.md:12` read directly as carrying the full sentence. Handed over as read: the fix pass's 25 modules at 1,112 passed, `evidence-check` 1,111 ok, `rider_check`, `survivor-check` over both ranges and `unverified-check` all exit 0, six red demonstrations. Handed over as unverified: the full suite, the repository-wide lint and the typecheck, the sealer's once this round settles. Six items were already open with named answerers in `overview.md` and the fix table, and duplicating one was named as costing the record its meaning. The ruling from round 2 stood: §2's list is three named acts and the plugin's own record checkers are not among them, so `bin/evidence-check .` was the round's to run. One fact about this chain rather than a general rule was handed over: round 1 spawned two `Explore` subagents and disclosed neither, and round 2, told that, did the same class of enumeration by hand.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The guard that makes the join safe is pinned by nothing, and misses the prose it was written to stop | `skills/code-review/scripts/round_record.py:1223` | deferred #339 | #339 |
| 2 | The protocol that defines a conforming tool never learned that a wrapped line is one value | `docs/review-handoff-protocol.md:142` | deferred #340 | #340 |
| 3 | The fix table spells the count it says it is not spelling | `rounds/round-2-fixes.md:3` | deferred #344 | #344 |

## Paste-ready fixes

```python
def test_a_heading_below_the_terminal_block_is_not_swallowed(repo):
    """`BLOCK_START`, which nothing else in this module reaches.

    The blank-line guard is pinned by the case above it; this is the other
    stop, and without it a `## Proof` heading written straight under the pair
    lands inside the floor cell. Round 3 of #120 measured the gap by deleting
    the branch and watching 103 cases stay green."""
    declared(repo)
    code, out, text = generate(
        repo, report_text=report(floor="no").rstrip("\n") + "\n## Proof\n"
    )
    assert code == 0, out
    assert fields(text)["Loses a record or crashes"] == "no", (
        "a heading under the terminal block was joined into the cell"
    )
```
```
    Truncation is the dangerous direction of the two. A value cut at a wrap
    still reads as a finished sentence, so nobody looks; a value that swallowed
    a following line reads as wrong at a glance. So the value is joined across
    the wrap, and the run stops at a blank line, at the other terminal label,
    or at a line opening a new markdown block.

    **The blank line is the guard; the opener list is a courtesy.** ` ` is in
    `chain.SEPARATORS`, so a swallowed prose line parses as a `no` with a
    reason and lands in the cell looking deliberate — and `BLOCK_START`
    catches only the openers it happens to name. Prose, `**bold**`, `---`, an
    HTML tag and a `1)` item are all joined. `agents/warden.md` asks for the
    blank line for this reason, and it is the only stop that covers every
    shape. What bounds the damage is that a joined value carrying a pipe is
    refused rather than written.
```
```
The generator joins it across the wrap and stops at a blank line — so leave
one under the pair, which markdown wants anyway. It also stops at the other
terminal label and at some lines that open a markdown block, but that second
list names only the openers it happens to name: a proof paragraph written
straight under the pair with no blank line is joined into the cell. The blank
line is the guard.
```
```
Either reviewer's line may wrap. A conforming tool reads the wrapped line as
one value, joining continuations until a blank line or the other label, and
the reviewer leaves a blank line under the pair so the join has somewhere to
stop. A tool that keeps the first physical line drops the rest with no
refusal, and one record shipped ending mid-clause that way.
```
```
Range `de7d693..ce0f9fe`, on
`docs/120-the-contract-is-settled-against-the-agents-that-exist`. The count is
deliberately left to the range rather than written out beside it — round 2's
finding 6 is that exact mistake in round 1's table, where *eight commits*
named a range holding six.
```

## Executed probes

| What was run | Result |
|---|---|
| Baseline: `tests/test_the_record_is_generated.py`, `tests/test_every_agent_reads_the_contract.py`, `tests/test_broad_gate_rule.py` at `ce0f9fe` in a `git clone --no-local` | exit 0, 147 passed |
| `terminal_value` reverted to the one-physical-line form, whole record module | exit 1 — `test_a_terminal_line_that_wraps_is_one_value` and `test_a_wrapped_terminal_line_and_its_unwrapped_twin_produce_one_cell` red, 101 passed |
| The `BLOCK_START` branch deleted, whole record module | **exit 0, 103 passed** — the guard is pinned by nothing |
| The blank-line branch deleted, whole record module | exit 1 — `test_prose_below_the_terminal_block_is_not_swallowed` red on its own assertion |
| The other-label branch deleted, whole record module | exit 1 — `test_the_two_terminal_lines_are_copied_after_the_colon` red |
| Nine shapes written under the terminal pair with no blank line, cell read out of the generated record | joined: plain prose, `**bold**`, `*emph*`, an indented line, `---`, `___`, an HTML tag, `1)`, a setext underline. Stopped: `#`, `- `, a fence, an HTML comment, a blank line |
| A swallowed line carrying a pipe | exit 2 — *`Loses a record or crashes` cannot carry a pipe*, and the message quotes the joined value. No record is written |
| The paste-ready case below, with `BLOCK_START` present and with its branch deleted | green with the guard, red without — *a heading under the terminal block was joined into the cell* |
| `agents/scribe.md` reverted to `de7d693` alone, `tests/test_every_agent_reads_the_contract.py` | exit 1 — *agents/scribe.md never says where its list of durable writes stops* |
| Round 2's mutant rebuilt: a fifth definition carrying the old parenthetical in unrelated prose, no bound | exit 1 on that file alone, where it passed at `b8aa637` |
| `skills/code-review/SKILL.md` reverted to `de7d693` alone, the two guard modules | exit 0, 138 passed — the fix changed no assertion, as disclosed |
| `agents/warden.md` reverted to `de7d693` alone, `tests/test_broad_gate_rule.py` and the report module | exit 1 — *the reviewer is sent to a table headed `What was run` with no word about how to write a `not yet` into it* |
| §2's count sentence reworded to *Two definitions*, `tests/test_broad_gate_rule.py` | exit 1, and the message names §2's prose, `COUNT_WORD` and the comparison against `['sealer.md']` |
| `longest_shared` over every `skills/**/*.md` against every contract section at `ce0f9fe` | over `LONGEST_KEPT_APPLICATION`: `skills/implement/SKILL.md` §5 at 30 and §9 at 15, `skills/config/SKILL.md` §16 at 12, then four pairs at 10 including `skills/code-review/SKILL.md` §7 |
| `bin/evidence-check .` unscoped at `ce0f9fe`, exit code read directly | exit 0 — 1111 ok · 0 drifted · 0 broken · 0 external · 0 old-format |
| `chain_check.py --baseline release/v0.10.0` over the branch | exit 1, and every line is a draft-run state: `Fixes checked by` is `nobody` on `round-2.md`, its `Pass` is unchecked, `Broad gate` is `not yet`. Nothing about the hand-repaired cell |
| `git rev-list --count` over the two ranges the fix tables name | `e972b5f..b8aa637` holds 7, matching round 1's corrected table; `de7d693..ce0f9fe` holds 5 against round 2's table's *four* |
| The broad gate | not yet. Unverified and the sealer's — this round ran no full suite, no repository-wide lint and no typecheck |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/SKILL.md:141` | round 1's 1 — fixed |
| round-1 | `agents/warden.md:157` | round 1's 2 — fixed |
| round-1 | `agents/warden.md:238` | round 1's 3 — fixed |
| round-1 | `agents/smith.md:22` | round 1's 4 — fixed |
| round-1 | `seal/ledger.md` (L7, L8, W1 and three orchestration rows) | round 1's 5 — fixed |
| round-1 | `skills/agent-contract/SKILL.md:64` | round 1's 6 — fixed |
| round-1 | `skills/agent-contract/SKILL.md:174` | round 1's 7 — fixed |
| round-1 | `templates/sdd-routing.md:29` | round 1's 8 — fixed |
| round-1 | `agents/warden.md:180`, `:283` | round 1's 9 — fixed |
| round-1 | `agents/sealer.md:104` | round 1's 10 — fixed |
| round-1 | `tests/test_a_moved_rule_leaves_its_definition.py:206` | round 1's 11 — answered |
| round-1 | `spec.md:44`, `plan.md:152` | round 1's 12 — answered |
| round-2 | `tests/test_every_agent_reads_the_contract.py:146` | round 2's 1 — open |
| round-2 | `skills/code-review/SKILL.md:154` | round 2's 2 — open |
| round-2 | `skills/code-review/scripts/round_record.py:1225` | round 2's 3 — open |
| round-2 | `tests/test_broad_gate_rule.py:339` | round 2's 4 — open |
| round-2 | `seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/rounds/round-1.md:9` | round 2's 5 — open |
| round-2 | `seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/rounds/round-1-fixes.md:3` | round 2's 6 — open |
| round-2 | `agents/warden.md:240` | round 2's 7 — open |
| round-2 | `tests/test_broad_gate_rule.py:281` | round 2's 8 — open |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| How wide the stop list under a terminal line should be, and whether joining should give way to refusing. `overview.md` already carries the join-or-refuse row; this adds the direction it does not name — a report that gains a line rather than losing one | `overview.md` §Not verified, beside the row already there | The repository owner, at the release that revisits the join |
| Whether the 15-word duplication guard should reach the skills a definition preloads | Already `overview.md` §Not verified and round 2's Deferred | The repository owner, at the release that takes the sweep |
| Whether §2's naming survives the framer | Already `questions.md` Q2 | The repository owner, at 0.11.0 |
