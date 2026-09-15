# Implementation Plan: the record chain disagrees with itself in five places

<!-- seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

Approved 2026-09-15 by the repository owner, when `smith` was spawned.

## Summary

Six repairs to one subsystem, in six phases plus a closing one. Four change
what a reader of a record or a refusal sees; two remove a case that passes for
the wrong reason.

The order is not the issue numbers. It is **cause before consequence, and the
generator before the things that read what it wrote**: the two repairs inside
`close` come first because the second reads the map the first builds, the
rendering repair comes next because every record this branch writes afterwards
carries it, and the two case-module repairs come last because their class
enumeration has to sweep the cases the earlier phases plant.

## Technical context

| What | Coordinate | What it does today |
|---|---|---|
| the inherited table's writer | `round_record.py#inherited_rows` | one row per `Location` of every earlier record, **first seen wins**, across rounds and within a record — it skips a `Location` it has already emitted |
| the forward reach | `round_record.py#reach_forward` | fills round N+1's `Why` cells from the map `close` hands it; refuses an unreadable table and a coordinate round N's table lacks; **silent** when it filled nothing |
| the map | `round_record.py#close`, the `now` dict | `now[seen[location]] = (...)` over every verdict row — a plain assignment, so **last wins** |
| the fix-table note cut | `round_record.py#fix_table`, the cut at `:3115` | `(third[:start] + third[end:]).strip(chain.SEPARATORS)` — the set is `" —–-:,"` and holds no period |
| the blocking predicate | `chain_check.py#open_blocking` | `BLOCKING in "".join(seen)` — the whole row, not the `#` cell |
| the refusal that prints it | `chain_check.py`, the `Pass` arm at `:3266` | prints `BLOCKING` the constant beside `verdict_of`'s word, so one sentence can name two severities |
| the rule's real check | `tests/test_one_word_one_meaning.py#test_no_instructing_document_leaves_an_instance_anonymous` | sweeps `SEAL_SWEPT`, which **includes** `skills/code-review/scripts/round_record.py`, and skips a hit whose next character is a letter |
| the duplicate pin | `tests/test_the_seal_is_taken_once_by_the_sealer.py:1307` | `assert "the seal" not in out` with no next-character guard |

Two facts were opened rather than taken from the issues.

- **The sweep does cover the module #406's refusal text lives in.** The exit
  sentence is `round_record.py:3985`, and `SEAL_SWEPT` at
  `tests/test_one_word_one_meaning.py:183` lists that file. So deleting the
  duplicate pin loses no coverage of the rule — it loses only a reading of the
  rule that the rule's owner does not make. *(read)*
- **The call site already argues for itself.** The comment at
  `round_record.py:3105-3112` says the previous widening was made *"HERE and not
  in `chain.SEPARATORS`, which the `deferred` home reader below and
  `chain_check`'s own readers share."* #414's decision is that comment applied a
  second time, not a new judgment. *(read)*

### The failure scenario of the chosen approach, in six months

The accounting refusal of phase 2 is the one that can age badly. It asserts a
relationship between two records — every coordinate of round N appears in round
N+1's inherited table — and that relationship holds because one function wrote
both sections. **The day somebody edits `inherited_rows` to emit fewer rows, the
reach starts refusing well-formed pairs and the message will send the reader to
correct a table that is already right** — which is, precisely, the failure the
silence was introduced to end. The mitigation is that the refusal names the
coordinates it could not account for rather than stating a rule, so the reader
sees what is missing and can tell a truncation from a changed writer.

## How this branch avoids sawing off the limb it sits on

`round_record.py` writes this branch's own round records and `chain_check.py`
reads the last one at the pull request. Four rules keep the repair from landing
in the middle of the record chain that judges it.

1. **Every phase closes before the first `round-record new` of this branch.**
   Routing is build, then the review chain, then the pull request, so round 1 is
   spawned after phase 7 — the ordering holds by construction. It is written
   down anyway, because the thing that would break it is a fix pass mid-rounds,
   and by then nobody is re-reading this section.

2. **No phase runs `round-record` against `seal/specs/1789455558-…/rounds/`.**
   Every phase exercises the generator in a throwaway clone, through the `repo`
   fixture the existing cases already use. The one directory the generator must
   not be pointed at during the build is this work item's own.

3. **No phase changes `inherited_rows`.** This is what makes a round N+1 table
   already on disk still readable by the repaired reach: the writer of that
   section is untouched, so phase 2's accounting is a claim about a section this
   work did not move. A round that opens a finding against `inherited_rows`
   is answered in the round record and, if it needs a change, becomes its own
   issue — changing that function between two of this branch's rounds is what
   would leave the pair written by two different generators.

4. **Phase 4's repair is exercised by this branch's own pull request, on
   purpose.** `chain-check` reads this work item's last round record with the
   repaired severity predicate. If phase 4 is wrong, the cheapest place to find
   out is a pull request whose author is still holding the diff. The risk is
   named rather than avoided, because avoiding it means shipping the repair
   unexercised.

A fix pass during the rounds may repair `round_record.py` and `chain_check.py`
— that is ordinary, and rule 3 is the only line it must not cross.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **#404 — refuse a coordinate carrying two verdict rows**, rather than resolving it first-wins | The refusal fires on records this repository has already written. A repeated `Location` inside one verdict table is what a verifying round produces whenever it re-reads a coordinate it also opens a finding at, and `agents/warden.md` asks for exactly that. `close` would then refuse a pair of records the generator itself wrote — which is the shape that was already measured and repaired once at `df404e2` | **Rejected.** Phase 1 re-counts the corpus rather than inheriting the count (Q4) |
| **#404 — first-wins on both sides** | Somebody later changes `inherited_rows` to last-wins and the two drift apart again, silently | **Chosen.** The two sides then agree *by construction* rather than by both being right: `close`'s map and `inherited_rows` resolve a repeat the same way, so there is no row left for them to disagree about. The disagreement is the defect; the picking is not |
| **#405 — leave the silence and add a reader in `chain_check.py`** | A second reader of the same section at the pull request, with no first reader's context. It also arrives too late: the wrong `Why` cell is already committed by then | **Rejected**, and named in `spec.md` as out of scope |
| **#405 — refuse whenever `filled == 0`**, the pre-`df404e2` behaviour | Refuses a re-review round whose every coordinate an earlier round claimed, which is the ordinary shape. This is round 1's 🔴 2 of the previous work item, already answered | **Rejected.** It is the state this work is repairing away from, not toward |
| **#405 — refuse when round N+1's table does not account for every coordinate of round N**, checked on every run | Fires where round N gained a verdict row after round N+1's `new` had already run — a hand-corrected record. That is a real shape and the refusal would be right about it, but the reader has to be told which coordinates, or the message is a rule they cannot act on | **Chosen**, conditional on the corpus measurement in Q3. The message names the unaccounted coordinates. If the corpus produces one unaccounted pair, narrow to `filled == 0` and record the shape that forced it |
| **#406 — give the assertion the sweep's next-character guard** | Two checks then claim one rule with two implementations, and the day the guard is widened in one it is not widened in the other. That is this issue happening again with the copies one step closer together | **Rejected** |
| **#406 — delete the assertion; the sweep owns the rule alone** | The refusal's text loses one reader in the module a reader of that refusal opens | **Chosen.** The loss is smaller than it reads: `SEAL_SWEPT` already lists the module the refusal text lives in, and the two *positive* pins beside it — `the only value \`seal\` accepts` and `` `seal` runs with `Pass` ticked `` — stay, so §14's requirement that the refusal's text survive a reword is still met by that file. `CLAUDE.md` names the sweep as the check for this rule; a second stricter one is not a second check, it is a disagreement |
| **#408 — read the severity from the `#` cell and stop there** | A row whose verdict word the vocabulary does not hold stops being refused at all, and *an unrecognised verdict counting as closed* is what the comment above `CLOSED_WORDS` calls the tolerant read the file exists to refuse | **Rejected.** Directionally right about the row, wrong about the verdict |
| **#408 — read the severity from the `#` cell, and give the unrecognised verdict its own arm and its own sentence** | Two messages where there was one, and a reader has to tell them apart | **Chosen.** That is the point: the reader who is stopped has to know which of the two is wrong. The 🔴 arm keeps its sentence; the new arm names the verdict word, names the vocabulary, and does not mention 🔴 — because sending a reader to look for a 🔴 that is not there is the cost this ticket measured |
| **#414 — widen `chain.SEPARATORS`** | Five readers share the constant. A period would then be stripped from a `deferred` home, from `chain_check`'s own cell readers, and from `nobody — <why>` reasons, where a trailing period is part of a sentence rather than decoration | **Rejected**, and the comment at `round_record.py:3105-3112` rejected it once already for the same reason |
| **#414 — widen at the call site** | The next cut somewhere else in the file repeats it, because the widening is local | **Chosen**, with the class enumerated rather than assumed (Q5): the other `strip(chain.SEPARATORS)` sites read a whole cell rather than cutting a span out of one, so they leave nothing behind — phase 3 confirms that by reading them |
| **#414 — write the next fix table's note without a leading period** | Repairs the next record and leaves the cause standing. It is what happened at `9919b265`, and the next record the generator wrote carried the defect again | **Rejected.** `agent-contract` §12 |
| **#407 — assert the substitution, or add the positive assertion** | Either alone leaves half the vacuity: a guard with no positive assertion proves the fixture is the right state and not that the case judged anything; a positive assertion with no guard can still read a record the fixture failed to build | **Both.** The issue asks for both and they close different halves |

## Phases

Vertical slices — each phase ends with something runnable and verified. **Every
`Verified by` cell names its command and the mutation that makes the new case
red** (`agent-contract` §15). Exit codes are read directly, never through a pipe
(§1): `cmd >/dev/null 2>&1; echo $?`.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#404** — `close`'s forward map takes the first row at a coordinate (`setdefault` in place of the assignment), so it and `inherited_rows` resolve a repeat the same way. Class: every place `close` keys a map by a verdict cell. Q4's corpus count re-measured and written into `overview.md` | `bin/test tests/test_the_fixes_close_the_record.py`. **Red-first:** restore the plain assignment — the new case asserting round 2's `Why` cell reads `round 1's 🔴 1 — fixed` goes red with `round 1's 🟢 — verified`. **Second direction:** the corpus count re-run; a non-zero count is what forecloses the refusal alternative | `14b617c` |
| 2 | **#405** — the silence at `filled == 0` becomes a refusal when round N+1's inherited table does not account for every coordinate of round N, naming the unaccounted ones, with nothing written to either record. Q3's corpus measurement runs **first** and decides unconditional against `filled == 0` | `bin/test tests/test_the_fixes_close_the_record.py`. **Red-first:** delete the accounting and return `None` — the truncation case asserting exit 2 goes red at exit 0. **Opposite direction, equally required:** `test_a_round_whose_coordinates_an_earlier_round_claimed_is_not_refused` stays green, and is re-run with the accounting in place. **Third:** both records byte-identical after the refused run | `38521a2` |
| 3 | **#414** — the fix-table note cut strips a trailing period at the call site. Class enumerated: every `strip(chain.SEPARATORS)` site in `round_record.py` read, and each either repaired or recorded as leaving nothing behind (Q5) | `bin/test tests/test_the_record_is_generated.py tests/test_the_fixes_close_the_record.py`. **Red-first:** strip back to `chain.SEPARATORS` alone — the case asserting the rendered Grounds cell reads `fixed at <sha> — <note>` goes red on `— . <note>`. The case asserts the whole rendered cell, not the absence of a period, so it cannot pass on a cell the fixture failed to build | `1f098fd` |
| 4 | **#408** — severity read from the `#` cell; a verdict word outside the vocabulary refused by its own arm with its own sentence, naming the vocabulary and not naming 🔴. §14: both sentences pinned in this commit | `bin/test tests/test_chain_check_at_the_pull_request.py`. **Red-first, two mutations:** restore `BLOCKING in "".join(seen)` — the case where a 🟢 row's Grounds quote an earlier 🔴 goes red on a refusal that should not have fired; and delete the vocabulary clause from the new sentence — the §14 pin goes red. **Third:** the case asserting the old sentence is *absent* from the new arm's output | `cb38e54` |
| 5 | **#406** — `assert "the seal" not in out` deleted from `tests/test_the_seal_is_taken_once_by_the_sealer.py:1307`; the refusal's exit sentence at `round_record.py:3985` reworded to name the sealer. Class: `grep -rn '"the seal" not in' tests/ skills/` re-run, and the enumeration recorded | `bin/test tests/test_one_word_one_meaning.py tests/test_the_seal_is_taken_once_by_the_sealer.py`. **Red-first:** reword that sentence to leave the seal anonymous — `test_no_instructing_document_leaves_an_instance_anonymous` goes red naming `skills/code-review/scripts/round_record.py` and the span. That is what proves the sweep, not the deleted pin, is holding the rule. **Opposite direction:** the sentence naming `the sealer` is green, where before this phase it turned the deleted pin red | `f119f72` |
| 6 | **#407** — `one_finding_inside_one_earlier_unit` asserts its substitution landed; `test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one` gains a positive assertion. Class: all five `re.sub` sites in `tests/test_the_fixes_close_the_record.py` and `tests/test_the_record_is_generated.py` read, plus any the earlier phases planted, and each either guarded or recorded as already guarded | `bin/test tests/test_the_fixes_close_the_record.py tests/test_the_record_is_generated.py`. **Red-first, two mutations:** break the `New units` pattern so the substitution misses — the fixture's new guard fails, where today the case it feeds stays green; and make round 1 name no unit so `depth_two` returns at its guard — the new positive assertion goes red while the two existing negatives still hold, which is the vacuity stated as a measurement | `1376409` |
| 7 | The work item's own records — `changelog.md` and `seal/ledger/1789455558-….md` in this directory's convention, and `overview.md` carrying the four corpus measurements and every divergence | `bin/evidence-check --strict .`, exit 0 read directly. **Red-first:** one character changed in one new row's hash — the run reports that row drifted and the exit is non-zero, which is what shows the rows are anchored to content rather than accepted on sight. Then `bin/unverified-check --baseline origin/release/v0.12.0` | |

This table is also where the work records how far it got. There is no separate
task list. **Status is empty, or the commit that closed the phase** — a tick is
refused and so is `done`.

What a phase discovers and the next phase needs goes to
`seal/specs/1789455558-…/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

## Operational impact

No migration, no new environment variable, no new dependency.

**One compatibility break, and it is deliberate.** After phase 2, a
`round-N+1.md` whose `## Inherited coordinates` table has been edited or
truncated since `new` wrote it makes `close --round N` exit 2 where it exited 0.
Anybody holding such a record will meet a refusal that did not exist before. The
refusal names the coordinates it could not account for, which is what a person
needs to repair the table or to see that the record should be regenerated.

**Three changes of text a person reads**, each pinned in its own commit
(`agent-contract` §14): the new unaccounted-coordinates refusal, `chain-check`'s
unrecognised-verdict sentence, and the fix-table note's rendering.

**No broad run in any phase.** The full suite, the repository-wide lint and the
typecheck are one act with one owner — `agents/sealer.md`, once, after the
rounds settle (`agent-contract` §2). `seal/config.md` holds the command.
