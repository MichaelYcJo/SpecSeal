# Round 3 report — 1790562540 (#637), a resumed agent's own transcript is sliced

Round 3, the verifying round and the run's last. Round 2's fixes closed on a
fix, which spent the one reopening, so the run ends at this record whatever
it finds. The target is the diff of round 2's fixes, 47fceb97..8ccb2b35
(77365e87 one planted case, 8ccb2b35 the ledger note on A5), with the branch
at 3cfb9dce and draft PR #649. Two questions: is round 2's finding 1 closed,
and is the planted case, `test_no_hint_where_the_only_message_precedes_the_first_call`,
correct as code nobody has reviewed.

Worked in a `git clone --no-local` of the branch at 3cfb9dce under the
session scratchpad, in a directory for this work item and this round. That
directory was removed at the end of the round, and the clone's status read
clean before it went.

## What this round found, in one view

```
round 2's finding 1 ── closed
  the before-first-call shape is now pinned, and the mutant that
  survived round 2 now turns exactly this case red
      │
the planted case (new unit, depth 1) ── correct
  its fixture builds the shape its name states; the file is taken as an
  own file, cut at one message into one slice; its docstring's claim holds
      │
ledger A5 and round-2.md's close ── each claim checked, each holds
      │
nothing opened ── the broad gate comes due, and it is the sealer's spawn
```

## Round 2's finding 1 is closed

Round 2 found that the narrowed hint names two shapes that cut nothing, a
message after the last call and a message before the first, and that only the
first was pinned. The mutant *a call starts at or after the first message*
left both modules green.

77365e87 plants the second shape at `tests/test_session_cost.py:3725`, beside
the one-stretch case. Executed in the clone at 3cfb9dce, with the hint's
condition at `skills/verify/scripts/session_cost.py:2787` replaced by a
Python script that asserted its one match and restored the file:

- Unmutated, the two modules pass, 160 passed, exit 0.
- Under round 2's surviving mutant, 1 failed, 159 passed, exit 1. The one
  failure is the planted case, so it catches that mutant alone.
- Under the opposite mutant, *a call starts before the last message*, the
  one failure is the one-stretch case. The two cases each hold one half.
- Under R1 (any marker prints the line) and R2 (one stretch is enough), both
  cases fail. The new case adds to those kills and weakens none of them.

The fix pass's account said the same (1 failed, 159 passed under the mutant,
passing unmutated). That was a claim when it reached me. The runs above are
what confirm it.

## The planted case, judged as code

The case is correct. What I checked, and how:

- **It builds the shape its name states (read).** `write_run` puts the
  run's transcript at `main.jsonl` and the agent's file under
  `main/subagents/`. The agent's file holds `coordinator_message(600)` and
  then two calls from `worked` at 625s and 640s. So the only marker comes
  before the first call.
- **The file is taken as an own file, so the case is not green by accident
  (executed).** A case that passed because the marker went unread would
  prove nothing. On the same fixture `--segments` prints *cut at 1
  coordinator message into 1 slice*, and round 2's surviving mutant turns
  the case red. That mutant can only change the output where `resume_cuts`
  returned a cut, so the marker is read.
- **Nothing sits beside the file (read).** `own_file` names
  `main/subagents/agent-smith.jsonl`, and the fixture writes nothing under
  `main/subagents/agent-smith/`. So `beside` is empty and the cuts are taken.
- **Both assertions do work (read).** When the hint prints, it comes before
  the span line, so `out.startswith("span ")` fails as well as the
  not-in check. That is the same pair of assertions as the one-stretch case.
- **The docstring's claim holds (executed).** It says `--segments` prints one
  slice with the same span. On the fixture, the plain reading starts
  `span 0.3m (2 tool calls)`, and `--segments` prints one row,
  `agent-smith.jsonl`, 0.3m, 2 calls. The case does not assert this, and the
  one-stretch case does not either, so the two stay alike.

Two things I considered and did not open:

- The case and the one-stretch case differ only in where the message sits,
  so one parametrized case could hold both. I did not open this. The file
  writes one case per shape, each with its own docstring, and ledger row A5
  cites each case by name and hash. A merge would re-anchor A5 to save
  about twenty lines.
- The one-stretch case's name, *every call sits in one stretch*, covers both
  shapes while its docstring covers one. Round 2 noted this. With the new
  case beside it, the two together now cover what the name says.

## The ledger note and the record's close

- **Ledger A5 at 8ccb2b35 (read, then executed).** The row now cites the new
  case at `@4117b862`, and `evidence-check --strict .` in the clone gives exit
  0 with 0 drifted and 0 refused. The note says *the before-first case passes
  at d617b65c*. The case was committed later, at 77365e87, but `git diff
  47fceb97..3cfb9dce` touches nothing under `skills/`, `hooks/` or `agents/`,
  so the code at d617b65c is the code at the tip. The note's *1 failed, 159
  passed* is what I measured.
- **round-2.md's close at 3cfb9dce (read).** `Fix range` names
  47fceb97..8ccb2b35 and 2 commits, and `git log` shows those two.
  `New units` names the planted case at depth 1, which is the only unit the
  range adds. `Pass` is ticked with finding 1 set to fixed at 77365e87, and
  that is the commit that plants the case.

## Carried, not re-established

The verdicts of rounds 1 and 2 are carried: the marker is the trigger; no
marker-less output moved; the own-file slices equal the walked slices; the
narrowed condition in `main` is correct and cannot crash; the copied-out case
is pinned; the records count five readings in #535; the counts paragraph in
`skills/verify/SKILL.md` says a resumed agent's own file; the resumed
paragraph follows In 2. The fix range changes no line any of them rests on,
because it touches a test and a ledger row only (read). The modules those
verdicts' cases live in pass at the tip (executed, 160 passed).

## Regression tests to plant

None. The case round 2 asked for is planted, and this round opened nothing.

## Facts for the evidence ledger

None new. A5's note already carries what this round measured.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 1 is closed — the before-first-call shape is pinned | `tests/test_session_cost.py:3725` | confirmed | executed: 160 passed unmutated; round 2's surviving mutant gives 1 failed, 159 passed, and the failure is this case alone; the opposite mutant fails only the one-stretch case |
| 🟢 | The planted case is correct: its fixture builds the shape its name states, the file is cut as an own file, and both assertions bite | `tests/test_session_cost.py:3725` | confirmed | read: the helpers and the fixture; executed: `--segments` on the fixture prints one slice cut at one message, with the plain span 0.3m and no hint; R1 and R2 also turn it red |
| 🟢 | Ledger A5's new citation and note hold | `seal/ledger/1790562540-a-resumed-agents-own-transcript-is-sliced.md` | confirmed | executed: `evidence-check --strict .` exit 0, 0 drifted; read: no code under `skills/` changed in the range, so *passes at d617b65c* is the tip's code |
| 🟢 | round-2.md's close matches the range | `seal/specs/1790562540-a-resumed-agents-own-transcript-is-sliced/rounds/round-2.md` | confirmed | read: `Fix range`, `New units` and the fixed commit each match `git log 47fceb97..8ccb2b35` |
| carried | The closures of rounds 1 and 2 stand | `skills/verify/scripts/session_cost.py` | confirmed | read: the range touches a test and a ledger row only; executed: the two modules pass at 3cfb9dce |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_session_cost.py tests/test_session_cost_post.py` in the clone at 3cfb9dce, unmutated | exit 0, 160 passed |
| Mutant: the hint gated on *a call starts at or after the first message* (round 2's survivor), same two modules | exit 1, 1 failed, 159 passed: `test_no_hint_where_the_only_message_precedes_the_first_call` |
| Mutant: the hint gated on *a call starts before the last message*, same two modules | exit 1, 1 failed, 159 passed: `test_no_hint_where_every_call_sits_in_one_stretch` |
| Mutant R1: the line printed for any marker, same two modules | exit 1, 2 failed, 158 passed: both one-stretch cases |
| Mutant R2: one stretch enough, same two modules | exit 1, 2 failed, 158 passed: both one-stretch cases |
| The planted case's fixture, rendered plain, with `--segments` and with `--json` | each exit 0; plain starts `span 0.3m (2 tool calls)` with no hint; `--segments` reads *cut at 1 coordinator message into 1 slice*, one row, 0.3m, 2 calls |
| `bin/evidence-check --strict .` in the clone at 3cfb9dce | exit 0; 0 drifted, 0 refused |
| `git diff --stat 47fceb97..3cfb9dce` over `skills`, `hooks` and `agents` | empty |
| The broad gate: full suite, repository-wide lint, typecheck | not yet — nobody has run it; it comes due now, and it is the sealer's spawn |

Every mutant was written into the clone by one Python script, a scratch
probe module named test_tmp_r3_probe, which asserted that its replacement
matched once and restored the file in a `finally`. The mutant runs went
through the clone's own `bin/test`. The fixture was rendered with the clone's
`.venv` interpreter, because the system interpreter has no pytest to import
the test module's helpers with.

Needs a fix: no
Loses a record or crashes: no

Nothing in this round needs a fix, and there are no deferrals, so the filing
ladder has nothing to take. The rounds have settled, and the next act is the
sealer's spawn for the broad gate.

## Proof block

Files opened this round:

- `seal/specs/1790562540-a-resumed-agents-own-transcript-is-sliced/rounds/round-2.md`
- `seal/specs/1790562540-a-resumed-agents-own-transcript-is-sliced/rounds/round-2-report.md`
- `git diff 47fceb97..8ccb2b35` (the ledger fragment's A5 row and `tests/test_session_cost.py`) and `git diff 8ccb2b35..3cfb9dce` (round-2.md)
- `skills/verify/scripts/session_cost.py`: `main`, the hint condition and its comment
- `tests/test_session_cost.py`: `call`, `run`, `write_run`, `worked`, `coordinator_message`, `own_file`, `test_no_hint_where_there_is_nothing_to_split`, `test_no_hint_where_every_call_sits_in_one_stretch`, and the planted case
- `bin/test`
