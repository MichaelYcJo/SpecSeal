# Round 3 — the verifying round, and the last of this run

Round 3 of #120 at `ce0f9fe`, on
`docs/120-the-contract-is-settled-against-the-agents-that-exist` against
`release/v0.10.0` (`d35c874`), draft pull request #338. The target is the fix
diff `de7d693..ce0f9fe` — five commits, 13 files, +306 / −19 — and not the
branch.

**Round 2's eight verdicts are closed.** Seven were re-derived by reverting the
fix alone and running the case it names; the eighth was discharged by the
orchestrator before the fix pass began and is confirmed in the record rather
than re-run. The two that changed no assertion were re-derived by measurement
instead, because a revert cannot make a case that does not exist go red.

**One thing the fix pass created is open.** `BLOCK_START` — the guard the fix
pass's own grounds call *load-bearing rather than tidy* — is pinned by no case
and does not stop the shapes that actually follow a terminal line. Everything
else in the fix range holds.

## The findings

**🟡 1 — the guard that makes the join safe is pinned by nothing, and it
misses the prose it was written to stop.**
`skills/code-review/scripts/round_record.py:1223`.

Finding 3's fix joins a wrapped terminal line instead of matching one physical
line. Joining is safe only while the run stops before prose, and the run stops
at three things: a blank line, the other terminal label, and a line matching
`BLOCK_START`. Two of the three are pinned. The third is not.

Deleting the `BLOCK_START` branch and running
`tests/test_the_record_is_generated.py` leaves 103 cases green. Deleting the
blank-line branch turns `test_prose_below_the_terminal_block_is_not_swallowed`
red; deleting the other-label branch turns
`test_the_two_terminal_lines_are_copied_after_the_colon` red. So the guard the
fix pass singled out is the one guard a later edit can remove in silence.

It also does not cover what it was written for. `BLOCK_START` enumerates seven
markdown openers. Written directly under the terminal pair with no blank line,
each of the following is joined into the cell:

| Line under the pair | Cell that ships |
|---|---|
| `The proof block follows and this line is prose.` | `no The proof block follows and this line is prose.` |
| `**Proof.** Read in the repository under review.` | `no **Proof.** Read in the repository under review.` |
| `---` | `no ---` |
| `<div>proof</div>` | `no <div>proof</div>` |
| `1) Proof: a numbered item.` | `no 1) Proof: a numbered item.` |
| `Proof` over a setext underline | `no Proof =====` |

`chain_check.py` then reads that cell through `yes_or_no`, which takes a space
as a separator, so `no <prose>` is a plain `no` with a reason and the pull
request says nothing. The old parser wrote `no`, so this direction is a
regression this branch introduced.

Two things bound it, and both were measured rather than assumed. A swallowed
line carrying a pipe is refused — *`Loses a record or crashes` cannot carry a
pipe* — so the record's table cannot be broken and no record is lost. And
`agents/warden.md` now tells the reviewer to leave a blank line under the pair,
which every report in this tree already does.

What is owed is the case, and §15 is why: a guard nothing pins is a guard the
next edit tidies away, and this one was declared load-bearing in a fix table
that will be read as though it were verified. The paste-ready case below is
green with the guard and red without it; I ran both.

How wide the enumeration should be is a second question and not mine to
settle. The branch's own contract argues against widening it — §7 says the
shapes are deliberately not enumerated *because every enumeration in this
repository has rotted* — and `overview.md` already defers the join-or-refuse
decision to the owner. The honest repair is the case plus a docstring that
says the blank line is the guard and the opener list is a courtesy. Both are
below.

**🟡 2 — the protocol that defines a conforming tool never learned that a
wrapped line is one value.** `docs/review-handoff-protocol.md:142`.

§14 was answered in `agents/warden.md`, which is the reviewer's instruction.
It was not answered in the document that says what a tool reading these
reports must do. That document describes both rows as *what stands after the
colon in its `<label>:` line* and sets conformance rules elsewhere in the same
section, so a second implementation built from it truncates exactly where
`round_record.py` used to — and produces a different record from the same
report. `templates/sdd-round.md:37` carries the same sentence and the same
silence.

This one can be answered with grounds if the owner reads the protocol as
describing records rather than report parsing. A one-line paste-ready is
below.

**⬜ 3 — the fix table spells the count it says it is not spelling.**
`seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/rounds/round-2-fixes.md:3`.

The line reads *Range `de7d693..HEAD`, four commits at the time of writing*,
and the sentence after it says the count *is deliberately not spelled as a
number that can go stale between this line and the last commit*, citing round
2's own finding 6. `de7d693..ce0f9fe` holds five. The hedge makes the line
true rather than false, so this is a correction and not a defect — but it is
the shape round 2 opened, one document over, and the reader who checks it will
have to do the arithmetic to find out it is fine.

## What I checked and did not open

**Finding 2's narrow guard is right for this branch.** Measured with the
module's own `longest_shared` over every `skills/**/*.md` against every
contract section at `ce0f9fe`: `skills/code-review/SKILL.md` against §7 is now
10 words, which is `LONGEST_KEPT_APPLICATION` exactly. The two pairs that would
go red on a widened glob are `skills/implement/SKILL.md` against §5 at 30 and
against §9 at 15, both over the 15-word window and both predating this branch.
Widening is a sweep over content nobody here wrote. The fix pass's reasoning
holds and the item already has a named answerer.

**Finding 3's swallow case was green before and after, and it is not an empty
case.** The fix pass disclosed this itself. §15 asks that a new case be seen
red against the old code *or with the sentence it pins deleted*; the fix pass
did neither, so I did the second. Deleting the blank-line branch turns
`test_prose_below_the_terminal_block_is_not_swallowed` red on exactly its own
assertion. The case pins the blank-line guard. What it does not pin, and never
did, is `BLOCK_START` — finding 1.

**Round 1's repaired cell matches the report it was repaired from.**
`rounds/round-1.md:12` now carries `yes — findings 1 through 8. Finding 1 is
the one that reopens the defect this work item was filed against.`, which is
`rounds/round-1-report.md:503-504` joined at the wrap, character for
character. The HTML comment beside it breaks nothing that reads the record:
`chain_check.py` over the branch reports only the three states a draft pull
request mid-run is expected to be in — `Fixes checked by` is `nobody` on
`round-2.md`, its `Pass` is unchecked, and `Broad gate` is `not yet`. None of
them is about the repaired cell, and none is a finding.

**The new `BOUNDS` entry closes round 2's exact mutant.** A fifth definition
carrying the old parenthetical in unrelated prose and no bound is now red on
that file alone. It passed before.

**The six items already open with named answerers were read before anything
was opened.** None of the three findings above duplicates one. The closest is
`overview.md`'s join-or-refuse row, which asks whether a report ever *loses* a
line to the join; finding 1 is the other direction — a report that gains one —
and the guard that was supposed to close it.

## The class this round enumerated

The fix pass changed a shared parser and a shared checker's vocabulary, so the
class is everything that reads a terminal line or a record cell.

| Reader | What it reads | State |
|---|---|---|
| `terminal_value` in `round_record.py` | the report's two terminal lines | the only reader of them in the tree; changed by this range |
| `chain_check.py`'s floor and needs readers | the record's two rows, through `yes_or_no` | unchanged, and it accepts `no <prose>` — finding 1 |
| the record's markdown table | the cell text | protected: a pipe in the value is refused with a message naming the value |
| `agents/warden.md` | the report format a reviewer writes | given the wrap rule and a pinned spelling rule |
| `docs/review-handoff-protocol.md`, `templates/sdd-round.md` | the record format a conforming tool writes | not given it — finding 2 |
| `skills/code-review/orchestration.md`, `docs/review-chain-spec.md`, `skills/code-review/SKILL.md` | what the two rows mean for the run | unaffected: they read the record's meaning, never the report's lines |

## The units this range created, judged as code

`BLOCK_START` (depth 1) is finding 1. The three cases —
`test_a_terminal_line_that_wraps_is_one_value`,
`test_a_wrapped_terminal_line_and_its_unwrapped_twin_produce_one_cell` and
`test_prose_below_the_terminal_block_is_not_swallowed` (each depth 1) — are
correct as written. Reverting `terminal_value` to the one-physical-line form
turns the first two red on their own assertions and leaves the third green,
which is the split the fix pass reported.

## Round 2's eight closures, re-derived

Every finding of round 2 answered here, with this round's own grounds, as
`agents/warden.md` requires. They sit outside the verdict table on purpose:
the table's `#` is this round's own finding ids and a record generated from
it takes them as keys.

| Round 2 finding | What it was | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | the bound case passed on a sentence about worker findings | `tests/test_every_agent_reads_the_contract.py:158` | answered | Reverting `agents/scribe.md` alone turns the case red on that file. Round 2's own mutant — a fifth definition carrying the old parenthetical in unrelated prose, no bound — is now red where it passed |
| 2 | a 16-word verbatim run out of §7 in a second document | `skills/code-review/SKILL.md:154` | answered | `longest_shared` over every `skills/**/*.md` at `ce0f9fe`: this pair is 10, exactly `LONGEST_KEPT_APPLICATION`. The guard stays narrow with grounds — the two pairs over the window predate the branch |
| 3 | a wrapped terminal line lost everything after the wrap | `skills/code-review/scripts/round_record.py:1228` | answered | Reverting `terminal_value` to the physical-line form turns `test_a_terminal_line_that_wraps_is_one_value` and its twin red. `rounds/round-1.md:12` matches `rounds/round-1-report.md:503-504` joined at the wrap. Finding 1 above is what the fix created |
| 4 | the release case's docstring claimed a shape it does not catch | `tests/test_broad_gate_rule.py:347` | answered | The docstring now states the miss and names the trade the case beside it states. No assertion changed, so nothing goes red; read in the diff |
| 5 | `round-1.md` still read *the fixes are not yet written* | `rounds/round-1.md:9` | answered | Discharged by the orchestrator before the fix pass. `Fixes checked by` is `round-2`, `Contract changes` is `none`, and eleven units stand in `New units` |
| 6 | the fix table stated its range as eight commits | `rounds/round-1-fixes.md:3` | answered | Now *`e972b5f..b8aa637`, seven commits*, and that range holds seven. The survivor-check row beside it gained the commit it was taken at |
| 7 | the broad-gate state routed into a table headed `What was run` | `agents/warden.md:240` | answered | Reverting `agents/warden.md` alone turns `test_the_reviewer_carries_the_gate_state_into_a_section_its_report_has` red on the new spelling assertion. §4 is named in the definition and pinned |
| 8 | the count case's first message pointed at §2 | `tests/test_broad_gate_rule.py:281` | answered | The tree assertion now fires first. Rewording §2's count sentence reports *§2 no longer states the count this case checks … `COUNT_WORD` and the comparison against `['sealer.md']` move with it*, naming all three literals |

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The guard that makes the join safe is pinned by nothing, and misses the prose it was written to stop | `skills/code-review/scripts/round_record.py:1223` | open | Deleting the `BLOCK_START` branch leaves 103 cases green, where deleting either other branch turns a named case red. Plain prose, `**bold**`, `*emph*`, an indented line, `---`, `___`, an HTML tag, `1)` and a setext underline are all joined into the cell; the old parser wrote `no` |
| 2 | The protocol that defines a conforming tool never learned that a wrapped line is one value | `docs/review-handoff-protocol.md:142` | open | §14 was answered in `agents/warden.md` alone. The protocol and `templates/sdd-round.md:37` both say *what stands after the colon in its `<label>:` line* and neither says the line may wrap, so a second implementation truncates where this one used to |
| 3 | The fix table spells the count it says it is not spelling | `rounds/round-2-fixes.md:3` | open | *four commits at the time of writing* against `de7d693..ce0f9fe`, which holds five. Hedged, so true rather than false; a correction, and the shape round 2's finding 6 opened |

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
| round-2 | `tests/test_every_agent_reads_the_contract.py:158` | round 2's 1 — answered, mutant re-run |
| round-2 | `skills/code-review/SKILL.md:154` | round 2's 2 — answered by measurement |
| round-2 | `skills/code-review/scripts/round_record.py:1228` | round 2's 3 — answered, and finding 1 is what the fix created |
| round-2 | `tests/test_broad_gate_rule.py:347` | round 2's 4 — answered, docstring only |
| round-2 | `rounds/round-1.md:9` | round 2's 5 — answered by the orchestrator |
| round-2 | `rounds/round-1-fixes.md:3` | round 2's 6 — answered |
| round-2 | `agents/warden.md:240` | round 2's 7 — answered |
| round-2 | `tests/test_broad_gate_rule.py:281` | round 2's 8 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| How wide the stop list under a terminal line should be, and whether joining should give way to refusing. `overview.md` already carries the join-or-refuse row; this adds the direction it does not name — a report that gains a line rather than losing one | `overview.md` §Not verified, beside the row already there | The repository owner, at the release that revisits the join |
| Whether the 15-word duplication guard should reach the skills a definition preloads | Already `overview.md` §Not verified and round 2's Deferred | The repository owner, at the release that takes the sweep |
| Whether §2's naming survives the framer | Already `questions.md` Q2 | The repository owner, at 0.11.0 |

## Paste-ready fixes

Finding 1, first half — the case. Append to
`tests/test_the_record_is_generated.py`, under
`test_prose_below_the_terminal_block_is_not_swallowed`. Green with the guard,
red without it; I ran both.

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

Finding 1, second half — the docstring's claim. In
`skills/code-review/scripts/round_record.py`, replace the last paragraph of
`terminal_value`'s docstring:

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

Finding 1, third half — the same correction where a reviewer reads it. In
`agents/warden.md`, replace the sentence beginning *The generator joins it
across the wrap*:

```
The generator joins it across the wrap and stops at a blank line — so leave
one under the pair, which markdown wants anyway. It also stops at the other
terminal label and at some lines that open a markdown block, but that second
list names only the openers it happens to name: a proof paragraph written
straight under the pair with no blank line is joined into the cell. The blank
line is the guard.
```

Finding 2 — in `docs/review-handoff-protocol.md`, under *`Loses a record or
crashes` — the floor under a round cap*, add:

```
Either reviewer's line may wrap. A conforming tool reads the wrapped line as
one value, joining continuations until a blank line or the other label, and
the reviewer leaves a blank line under the pair so the join has somewhere to
stop. A tool that keeps the first physical line drops the rest with no
refusal, and one record shipped ending mid-clause that way.
```

Finding 3 — in
`seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/rounds/round-2-fixes.md`,
replace the first sentence:

```
Range `de7d693..ce0f9fe`, on
`docs/120-the-contract-is-settled-against-the-agents-that-exist`. The count is
deliberately left to the range rather than written out beside it — round 2's
finding 6 is that exact mistake in round 1's table, where *eight commits*
named a range holding six.
```

Needs a fix: yes — finding 1's missing case. Finding 2 is answerable with grounds and finding 3 is a correction.
Loses a record or crashes: no

## Proof

Read in the repository under review, in
`seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/`:
`rounds/round-1.md`, `rounds/round-1-report.md`, `rounds/round-1-fixes.md`,
`rounds/round-2.md`, `rounds/round-2-report.md`, `rounds/round-2-fixes.md`,
`overview.md`, `survivors.md`. In a `git clone --no-local` at `ce0f9fe`:
`skills/agent-contract/SKILL.md`, `skills/code-review/SKILL.md`,
`skills/code-review/orchestration.md`,
`skills/code-review/scripts/round_record.py`,
`skills/code-review/scripts/chain_check.py`, `agents/warden.md`,
`agents/scribe.md`, `docs/review-handoff-protocol.md`,
`docs/review-chain-spec.md`, `templates/sdd-round.md`, `seal/ledger.md`,
`bin/test`, `tests/test_the_record_is_generated.py`,
`tests/test_broad_gate_rule.py`, `tests/test_every_agent_reads_the_contract.py`,
`tests/test_a_moved_rule_leaves_its_definition.py`.

Probes: one `test_tmp_*` file in the clone, rewritten and deleted between
runs, and four driver scripts outside the clone that patched a file, ran a
module and restored it. Every run ended with the clone reporting a clean
working tree; the last one is quoted in the drivers' own output. The clone and
the virtual environment `bin/test` built inside it are this round's leavings
and are deleted. No subagent was spawned, and every enumeration above was run
in this session.
