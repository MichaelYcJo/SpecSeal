# 1789540097-three-checks-that-do-not-see-what-they-are-named-for — review round 3

| Field | Value |
|---|---|
| Target SHA | f2bfc452 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 425 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The last record of the run. Round 1 met the floor and round 2 — a verifying
round that opened two findings — closed on a fix, so the one reopening is
spent and this record ends the run whatever it finds.

Its target is the diff of round 2's fixes, `b935679f..f2bfc452`, and its job is
the answers: are round 2's two verdicts actually closed. Round 2's record names
no new units, and verifying that claim was part of the round rather than taken
from it.

The class this work item repairs has moved one layer outward at every round, so
the round was asked where it is now rather than only whether the last repair
holds. It was also asked to check three things about the branch's own records:
that a stalled fix pass's self-written verdicts were restored to what the
reviewer wrote, that a confirmation row no longer quotes a raw blocking marker,
and that a proposed unit name carries its marker.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 2's finding 6 is closed — the hard-wrapped spelling is the one case input carrying a newline, and the flattening is the only thing that finds it | `tests/test_chain_hooks_hardening.py:907` | confirmed | Executed: `flat_body = EMPHASIS.sub("", body)` is exit 1 · 1 failed, 50 passed on `test_the_sweep_refuses_a_planted_instruction_in_every_spelling`. Baseline at this SHA exit 0 · 51 passed |
| 🟢 | Round 2's finding 7 is closed for the read and the loop | `tests/test_chain_hooks_hardening.py:1128-1151` | confirmed | Executed, each mutation alone with the function and constants untouched: read truncated to ten bytes exit 1 · 1 failed, 50 passed; loop iterable replaced by `()` exit 1 · 1 failed, 50 passed |
| 🟢 | Round 2's finding 7 is genuinely still open for the call, and the grounds for leaving it are sound | `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/overview.md:39` | confirmed | Executed: `batch_instructions("")` in place of `batch_instructions(body)` is exit 0 · 51 passed, so the claim is not overstated. Read: the row names the repository owner as answerer and `CONTRIBUTING.md` asks a separate argument for a change to what the suite guards |
| 🟡 8 | The wholeness assertion pins a 1000-byte floor, not wholeness, so every definition can be truncated while the guard stays green | `tests/test_chain_hooks_hardening.py:1150` | deferred #426 | Executed: `f.read(2000)` is exit 0 · 51 passed, where `f.read(10)` is exit 1. The smallest definition is `agents/scribe.md` at 3764 bytes, so 1001–3763 truncates all five in silence. The comment at `:1147` claims the assertion pins that each file arrived WHOLE. Fix measured: green untouched, and exit 1 under the ten-byte read, the 2000-byte read and the emptied loop |
| 🟡 9 | `close` prefixes its own grounds onto a Grounds cell that already carries them, so restoring one cell of two doubles the record in silence | `skills/code-review/scripts/round_record.py:3771` | deferred #427 | Executed: `round-2.md` restored to `1575d770`, only the two Verdict cells set back to `open`, `round-record close` re-run with the same fix table and range — the resulting finding-6 row is byte-identical to the committed `f2bfc452` row. The `already closed` refusal above reads only the Verdict cell, so it does not fire. `close` exited 1 on the unrelated `Pass` notice and said nothing about the duplication |
| 🟢 | The confirmation row's rewording is the right one of the three ways out the refusal names | `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/rounds/round-2.md:43` | confirmed | Executed: with the raw marker restored at `6e3f504d`'s state, `close` refuses — the row is read as open because a cell carries a blocking marker while its verdict reads `confirmed`, which is not a closing word. Read: a closing word would misstate the row and an unticked `Pass` would misstate the round |
| 🟢 | The proposed unit name is absent from the tree, so the marker on it is true | `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/overview.md:39` | confirmed | Executed: `bin/evidence-check .` exit 0 · 1327 ok · 0 drifted · 0 broken, records arm 4 work items · 670 names · 0 refused. Read: the name stands in this work item's prose once and inside fenced blocks in the two round records, which are exempt |
| 🟢 | `New units \| none` is true of the fix diff | `tests/test_chain_hooks_hardening.py` | confirmed | Executed: no added `def` or `class` line under `tests/` across `b935679f..f2bfc452`. The fix adds one tuple entry, a list, two appended fields and two assertions |
| 🟢 | Four of round 2's five corrections landed at their coordinates, and the fifth is correctly placed elsewhere | `phases/phase-3.md:32`, `phases/phase-6.md:72`, `survivors.md:8`, `survivors.md:33`, `seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md` | confirmed | Read: each correction is present as described. The fifth stands in the ledger fragment rather than at `rounds/round-1.md:44`, on the stated grounds that an earlier round's fix table is a record this pass may not edit, and `rounds/round-1.md` is untouched by the range |
| ⬜ | `round-2.md`'s two amber rows each carry the fix grounds twice, written by the commit whose message says both cells were restored | `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/rounds/round-2.md:44`, `:45` | correction | Executed: `fixed at 64f36eee` occurs 0 times at `6e3f504d`, 1 at `1575d770`, 2 at `f2bfc452`; same counts for the answered row's opening clause. Restoring the file to its `1575d770` content is the whole repair — those two rows are the only difference between the two commits |
| ⬜ | `round-2-report.md` still carries the raw blocking marker the record dropped, so the record can no longer be regenerated from its own report | `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/rounds/round-2-report.md:258` | correction | Executed: `round-record new --report` copies the cell through without refusing; `close` then refuses on it. So a regeneration reproduces the refusal and the rewording has to be retyped, which is the failure the report-file convention closed |
| ⬜ | `survivors.md`'s range table and one row's Grounds are stale at HEAD, and the row claims to be live over a range that reports nothing | `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/survivors.md:14`, `:15`, `:32` | correction | Executed at `f2bfc452`: `27a2d403..HEAD` with no exempt file reports `phases/phase-3.md:39`, not `:36`; `9087705b..HEAD` reports nothing at all, exit 0. Both exempted runs are exit 0, so no check is broken. The table was written in `6e3f504d`, the same commit that moved the phase-3 line it cites |
| ❓ | The full suite, the repository-wide lint and the typecheck | the whole tree at this SHA | out of verified scope | `agent-contract` §2 assigns the broad gate to the sealer and `agents/warden.md` hands me none of the three. Not yet run. Answered by the sealer, spawned by the orchestrator now that the rounds have settled |

## Paste-ready fixes

```python
        read.append((relative, len(body.encode("utf-8"))))
```
```python
    # The file's OWN size, not a floor. A floor pins that the read was not
    # tiny, which is a different claim: round 3 measured `f.read(2000)` green
    # while every one of the five definitions was truncated, because the
    # smallest is 3764 bytes. Byte length on both sides, so the comparison
    # survives the emoji and em-dashes these files carry.
    assert all(
        size == os.path.getsize(os.path.join(ROOT, name)) for name, size in read
    ), f"the sweep read a definition it did not read in full: {read}"
```
```python
        if old.startswith(grounds):
            raise Refused(
                f"finding {number}'s Grounds already begins with the text this "
                f"fix table writes, so this row was closed once already and "
                f"only its Verdict was reopened. Restore the Grounds cell to "
                f"what the reviewer wrote as well, or leave the row as it "
                f"stands — writing it again would carry the fix grounds twice"
            )
        cells[GROUNDS_COL] = grounds + (f"; {old}" if old else "")
```
```
git show 1575d770:seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/rounds/round-2.md \
  > seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/rounds/round-2.md
```
```
| 🟢 | round 1's blocking finding is closed — all five of round 1's mutations are red, each on the case that calls the same function the sweep calls | `tests/test_chain_hooks_hardening.py:856` | confirmed | Executed: five mutations of `batch_instructions`, constants untouched, each exit 1 · 1 failed, 50 passed, each failing `test_the_sweep_refuses_a_planted_instruction_in_every_spelling`; baseline restored to exit 0 · 51 passed after each |
```
```markdown
**Which rows are live depends on the range, and round 2's correction is that
the preamble used to claim of all three what was true of one.** Measured at
`f2bfc452`:

| Range | What it reports with no exempt file |
|---|---|
| `27a2d403..HEAD` — the build's own range | exactly one place, `phases/phase-3.md:39` |
| `9087705b..HEAD` — round 2's fix range | nothing at all, exit 0 |
```
```markdown
| `tests/test_waiver_decided_at_start.py` | `definitions = sorted(glob.glob(os.path.join(ROOT, "agents", "*.md")))` | **Reported over `9087705b..64f36eee`, and a false positive; it is reported by no range at HEAD.** The two phrases it shares with the sweep round 2's fix changed — *definitions files for path*, *path root for* — are the idiom for walking a glob, not wording this range removed. It is also not the same defect: this case looks for `AskUserQuestion`, which `agents/smith.md` and `agents/framer.md` each contain once, so its loop body **does** execute on the committed corpus. Measured at `64f36eee`: 2 occurrences across the five definitions |
```

## Executed probes

| What was run | Result |
|---|---|
| `tests/test_chain_hooks_hardening.py`, untouched at `f2bfc452` | exit 0 · 51 passed |
| Flattening dropped from `batch_instructions` | exit 1 · 1 failed, 50 passed |
| Sweep's read truncated to ten bytes | exit 1 · 1 failed, 50 passed |
| Sweep's loop iterable replaced by `()` | exit 1 · 1 failed, 50 passed |
| Sweep's call given `""` instead of the body | exit 0 · 51 passed — still unheld, as the record says |
| Sweep's read truncated to 2000 bytes | exit 0 · 51 passed — finding 8 |
| Proposed wholeness assertion, untouched tree | exit 0 · 51 passed |
| Proposed wholeness assertion + ten-byte read | exit 1 · 1 failed, 50 passed |
| Proposed wholeness assertion + 2000-byte read | exit 1 · 1 failed, 50 passed |
| Proposed wholeness assertion + emptied loop | exit 1 · 1 failed, 50 passed |
| `bin/evidence-check .` | exit 0 · 1327 ok · 0 drifted · 0 broken · records arm 0 refused |
| `bin/survivor-check --range 27a2d403..HEAD --exempt <survivors.md>` | exit 0 · one survivor excused at `phases/phase-3.md:39` |
| `bin/survivor-check --range 27a2d403..HEAD` (no exempt) | exit 1 · one place, `phases/phase-3.md:39` |
| `bin/survivor-check --range 9087705b..HEAD` (no exempt) | exit 0 · no removed wording is still standing |
| `chain_check.py --baseline <merge-base>` | exit 1 · `Broad gate` not yet, and `Pass` ticked beside `Fixes checked by: nobody` |
| `round-record close` on `1575d770`'s record with only the Verdict cells reopened | the 🟡 6 row is byte-identical to the committed `f2bfc452` row |
| `round-record close` on `6e3f504d`'s record, raw marker present | refuses at `rounds/round-2.md:43` on the blocking-marker rule |
| `round-record new --report <round-2-report.md>` | writes the record; does **not** refuse the raw marker |
| Raw batch-phrase hits across `agents/*.md` at this SHA | 0 |
| The broad gate — full suite, repository-wide lint, typecheck | **not yet run** · assigned to the sealer, not to this round |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_chain_hooks_hardening.py:1000-1013` | round 1's 🔴 1 — fixed |
| round-1 | `tests/test_chain_hooks_hardening.py:843`; compare `skills/code-review/scripts/chain_check.py:419` | round 1's 🟡 2 — fixed |
| round-1 | `tests/test_chain_hooks_hardening.py:866` | round 1's 🟡 3 — fixed |
| round-1 | `seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md:6` | round 1's 🟡 4 — fixed |
| round-1 | `plan.md:130`, `spec.md:126-128` | round 1's 🟡 5 — answered |
| round-1 | `questions.md:35`, `spec.md:148`, `tests/test_one_word_one_meaning.py:482`, `tests/test_one_word_one_meaning.py:193` | round 1's ⬜ — correction |
| round-1 | `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py:242-266` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_one_word_one_meaning.py:253`, `:388`, `:459-503` | round 1's 🟢 — confirmed |
| round-1 | `seal/specs/1789445605-…/rounds/round-2.md:39-40` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_docs_line_wrap.py:20-24`, `:59` | round 1's 🟢 — confirmed |
| round-1 | the whole tree at this SHA | round 1's ❓ — out of verified scope |
| round-2 | `tests/test_chain_hooks_hardening.py:856` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_chain_hooks_hardening.py:876` | round 2's 🟡 6 — fixed |
| round-2 | `tests/test_chain_hooks_hardening.py:1100-1104` | round 2's 🟡 7 — answered |
| round-2 | `tests/test_chain_hooks_hardening.py:839`, `:843` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_chain_hooks_hardening.py:949-962` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/survivors.md` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/phases/phase-3.md:36-55` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_one_word_one_meaning.py:482` | round 2's 🟢 — confirmed |
| round-2 | `phases/phase-3.md:31`, `phases/phase-6.md:73`, `survivors.md:9-11`, `rounds/round-1.md` 🟡 4 | round 2's ⬜ — correction |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 8 — the wholeness assertion's 1000-byte floor pins no wholeness | a new issue; the measured fix is below | the repository owner |
| 9 — `close` doubles a Grounds cell it has already written | a new issue; the proposed guard is below and is unmeasured | the repository owner |
| Round 2's finding 7, the sweep's own call | already deferred in round 2, to `overview.md` §*Not verified* | the repository owner |
