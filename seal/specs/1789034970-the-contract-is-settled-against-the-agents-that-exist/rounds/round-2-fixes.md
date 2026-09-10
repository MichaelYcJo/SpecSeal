# Round 2's fix pass — the contract is settled against the agents that exist

Range `de7d693..HEAD`, four commits at the time of writing, on
`docs/120-the-contract-is-settled-against-the-agents-that-exist`. The count is
deliberately not spelled as a number that can go stale between this line and
the last commit — round 2's finding 6 is that exact mistake in round 1's table,
where *eight commits* named a range holding six. Read by
`round_record.py close`, which is given the range and does not read it from
here.

**This is the last fix pass.** Round 1 met the floor, so a record after round 3
ends the run whatever it finds. Nothing below is a rushed edit; what could not
be closed properly is a deferral with a named answerer, and there is one.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `54e31b2` |
| 2 | fixed | `60c352e` |
| 3 | fixed | `463a6f6` |
| 4 | fixed | `60c352e` |
| 5 | answered | Discharged by the orchestrator before this pass began: `close` was applied to `rounds/round-1.md`, which now carries `round-2` in `Fixes checked by`, `none` in `Contract changes` and the eleven units in `New units`. Nothing here redid it |
| 6 | fixed | `60c352e` |
| 7 | fixed | `60c352e` |
| 8 | fixed | `60c352e` |

## What each fix decided, where the report left a choice

**Finding 3 joins rather than refuses, and the direction is why.** A value cut
at a wrap still reads as a finished sentence, so nobody looks; a value that
swallowed a following line reads as wrong at a glance. A refusal would also
stop `new` on a report that broke no rule anybody had written down. So the
value is joined, and the run stops at a blank line, at the other terminal
label, or at a line opening a new markdown block. That last guard is
load-bearing rather than tidy: ` ` is in `chain.SEPARATORS`, so a swallowed
prose line parses as a `no` with a reason and lands in the cell looking
deliberate. §14 is answered in `agents/warden.md`, which now says the lines may
wrap, that a wrapped line is one value, and to leave a blank line under the
pair.

**Finding 3's other half was a hand-edit to a generated record.**
`rounds/round-1.md`'s `Needs a fix` cell is repaired from
`rounds/round-1-report.md:503-504`, with an HTML comment beside it naming what
was dropped, why, and that the parser is fixed in the same range. A generated
file edited by hand is worth saying out loud.

**Finding 2 trims rather than widens the glob.** The longest run
`skills/code-review/SKILL.md` shares with §7 falls from 16 words to 10, which
is `LONGEST_KEPT_APPLICATION` exactly, measured with the module's own
`longest_shared` over every `skills/**/*.md`. Widening
`tests/test_a_moved_rule_leaves_its_definition.py`'s glob to reach the skills
would go red on two pairs this work item did not write —
`skills/implement/SKILL.md` against §5 at 30 words and against §9 at 15 — so it
is a sweep, and round 2's record already defers it to the owner.

**Findings 4 and 8 change no assertion.** Finding 4 adds the miss the case can
still have to its own docstring, the way the count case beside it already
states its own. Finding 8 reorders two assertions so the tree fact is read
first and both messages name the three things that move together at 0.11.0 —
§2's prose, `COUNT_WORD`, and the comparison against `["sealer.md"]`.

## Narrow runs

| Run | Exit |
|---|---|
| Finding 1's case with the vocabulary entry replaced and `agents/scribe.md` untouched | 1 — red on that file alone |
| Three modules after the bound landed | 0 — 164 passed |
| The mutant round 2 showed passing: a fifth definition carrying the old parenthetical in unrelated prose, no bound | 1 — now red on that file, where it passed before |
| Finding 3's wrap case and same-cell case against the parser as it stood | 1 — *the wrapped remainder was dropped, which is how round 1's record shipped* |
| `tests/test_the_record_is_generated.py` after | 0 — 103 passed |
| The three record modules after the hand-repair | 0 — 211 passed |
| Finding 7's two assertions with `agents/warden.md` stashed | 1 |
| Finding 8's reorder, §2's count reworded to *Two definitions* | 1 — the message names all three literals |
| `tests/test_broad_gate_rule.py` after | 0 — 18 passed |
| `longest_shared` over every `skills/**/*.md` against every contract section | `skills/code-review/SKILL.md` §7: 16 → 10 |
| `bin/evidence-check .` | 0 — 1111 ok · 0 drifted · 0 broken |
| `.github/scripts/rider_check.py` | 0 |
| `bin/survivor-check --range de7d693..HEAD --exempt …` | 0 — two exempt, both comprehension idioms inside the file the range edited |
| `bin/survivor-check --range origin/release/v0.10.0...HEAD --exempt …` | 0 — five exempt |

## What is left open, and who answers it

| Item | Who must answer |
|---|---|
| Whether the 15-word duplication guard should reach the skills a definition preloads. Two of the three pairs over the window predate this branch, so widening the glob is a sweep this work item cannot take without going red on content it did not write | the repository owner, at the release that takes the sweep — already round 2's own Deferred row |
| Whether `§2`'s naming survives the framer. Unchanged by either round; finding 8 only asks that the case name the literals that move with it | the repository owner, at 0.11.0 — `questions.md` Q2 |
| The full suite, the repository-wide lint and the typecheck | **the sealer**, spawned once the rounds settle |
| Whether the widened §7 actually stops a probe leaving a worktree. It names no mechanism, by the owner's Q3 answer, so nothing in the tree can check it | a review round, and then the next probe that makes one |
| Whether the routing criterion changes how the `Implementation` row is answered | the release after this one, against `routing.md` files written under the new template |
| Whether `terminal_value` should have refused a wrapped line rather than joining it. Decided here, with the grounds above, and it is a decision a person can overturn cheaply — the guard list is four lines | the repository owner, if a report ever loses a line to the join |
