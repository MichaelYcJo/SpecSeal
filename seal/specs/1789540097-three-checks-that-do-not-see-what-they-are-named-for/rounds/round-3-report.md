# Round 3 — the verifying round that ends the run

Target `f2bfc452`, confirmed at the head of
`test/413-418-422-three-checks-that-do-not-see-what-they-are-named-for`, tree
clean. Target diff `b935679f..f2bfc452`. Pull request 425, draft.

## What this round was asked

Round 2's two findings, and the branch's own records. The reopening is spent,
so this record ends the run whatever it finds: every finding below is routed
explicitly to the closing commit, to an issue, or left alone.

## How the findings relate

Round 2's fixes hold. Everything this round opened is one step outside them,
and the two halves have different causes.

1. **The code half.** Round 2's finding 7 was closed for the read and
   answered with grounds for the call. The read's new guard is real but its
   floor is a number rather than the file's own size, so a larger truncation
   walks past it. This is the same class the work item is named for, one
   layer further out again.
2. **The paperwork half.** The commit that repaired round 2's record,
   `f2bfc452`, restored one cell of the two it says it restored. `close` then
   wrote its own grounds on top of grounds it had already written, and the
   record shipped with the sentence twice. The rewording that went with it
   left the report and the record disagreeing.

## Round 2's finding 6 is closed

The hard-wrapped spelling at `tests/test_chain_hooks_hardening.py:907` walks
the same tuple the case already walked, and it is the only input in that
tuple carrying a newline.

Executed, in a throwaway clone at `f2bfc452`: dropping the flattening —
`flat_body = EMPHASIS.sub("", body)` — is exit 1, **1 failed, 50 passed**, on
`test_the_sweep_refuses_a_planted_instruction_in_every_spelling`. That
reproduces the orchestrator's re-measurement exactly and contradicts round 2's
own figure of exit 0, 51 passed, which was taken before the case existed.

## Round 2's finding 7 is half closed, and the half that is closed is weaker than the record says

The read and the loop are held. Executed, each mutation alone with
`batch_instructions` and the constants untouched:

- read truncated to ten bytes — exit 1, 1 failed, 50 passed
- loop iterable replaced by `()` — exit 1, 1 failed, 50 passed

The call is genuinely still open. `batch_instructions("")` in place of
`batch_instructions(body)` is exit 0, 51 passed. **The grounds for leaving it
open are sound**: closing it needs a walk a case drives with a planted
definition file, `CONTRIBUTING.md` asks a separate argument for a change to
what the suite guards, and `overview.md` §*Not verified* names the repository
owner as the answerer. Nothing about that reasoning rests on the account
alone — the exit code is what I checked, and the follow-up row is where the
row says it is.

**What the record claims and the code does not do.** The assertion at
`tests/test_chain_hooks_hardening.py:1150` reads
`assert all(size > 1000 for _, size in read)`, and the comment above it at
`:1147` says *what it pins is that each file arrived WHOLE*. It does not. It
pins that each file arrived with more than 1000 bytes.

Executed: replacing the read with `f.read(2000)` is **exit 0, 51 passed**. The
smallest definition, `agents/scribe.md`, is 3764 bytes, so a truncation
anywhere between 1001 and 3763 bytes truncates all five definitions and the
guard stays silent. Sizes measured at this SHA: `scribe.md` 3764,
`sealer.md` 8428, `framer.md` 15626, `smith.md` 21261, `warden.md` 26210.

Why it matters rather than reading as a nitpick: the sweep exists to be the
one thing connecting the guard to the committed corpus, and the corpus holds
zero batch phrases — measured, 0 raw pattern hits across all five definitions
at this SHA. A truncated read is therefore invisible in every other way. The
assertion is the whole of the connection, and it is the fifth thing in this
work item to be named for something it does not see.

The fix is measured. See `## Paste-ready fixes`.

## The commit that repaired round 2's record is the commit that corrupted it

`f2bfc452`'s message says *Both cells were restored to what the reviewer
wrote*. The **Verdict** cell was. The **Grounds** cell was not, and `close`
prefixes rather than replaces:

```
skills/code-review/scripts/round_record.py:3771
    cells[GROUNDS_COL] = grounds + (f"; {old}" if old else "")
```

Counted in the committed file content, not the diff:

| Commit | Copies of `fixed at 64f36eee` in `round-2.md` |
|---|---|
| `6e3f504d` | 0 — the reviewer's `open` still stood |
| `1575d770` | 1 — correct |
| `f2bfc452` | 2 |

Executed, reproducing it: restore `round-2.md` to its `1575d770` content, set
only the two Verdict cells back to `open`, run `round-record close` with the
same fix table and range. The finding-6 row that comes out is **byte-identical to
the committed `f2bfc452` row**. `close` exited 1, but on the unrelated
`Pass` / `Fixes checked by` notice — it said nothing about the duplication.

So there are two separate items here, and they have different homes.

- **The record** — `rounds/round-2.md:44` and `:45` each carry the fix grounds
  twice. Under `seal/specs/`, so it is a correction for the closing commit.
  Restoring the file to its `1575d770` content is the whole repair: those two
  rows are the only difference between the two commits.
- **The tool** — `close` has no guard against a Grounds cell that already
  begins with its own output. Restoring one cell of two is enough to defeat
  the `already closed` refusal above it, which reads only the Verdict cell.
  Not under `seal/`, so it becomes an issue.

## The confirmation row's rewording is the right one of the three, and it left the report behind

Executed, isolating the refusal: restore `round-2.md` to `6e3f504d` (verdicts
`open`, raw marker present) and run `close`. It refuses at
`rounds/round-2.md:43`:

> `Pass` is checked, and this row is read as open because one of its cells
> carries a blocking marker, while its own verdict reads `confirmed` — not one
> of the words that close a row … Write one of those words, drop the marker,
> or leave `Pass` unchecked

The message names three ways out. Changing `confirmed` to a closing word would
misstate the row, which records a finding closing rather than a withdrawal;
leaving `Pass` unchecked would misstate the round. **Dropping the marker is
the only one of the three that keeps both true**, so the rewording is right.

What it cost: `rounds/round-2-report.md:258` still reads `🔴 1 is closed`. The
record and its own report now disagree on that cell, so the record can no
longer be regenerated from the report — regenerate, and `close` refuses again
and the rewording has to be retyped. That is the retyping #228 closed.
Correction for the closing commit.

Measured while checking this: `round-record new --report` does **not** refuse
the raw marker. It copies the cell through and writes the record; only `close`
refuses, one step later. Reported as an observation, not a finding — nothing
in the tree claims otherwise.

## The proposed name really is absent, and no unit was added

`overview.md:39` carries `<!-- NAME NOT IN TREE -->`. Checked: the name it
marks appears in this work item's `overview.md` prose and inside fenced blocks
in `rounds/round-2-report.md` and `rounds/round-2.md`, and nowhere else in the
tree. Fenced blocks are exempt, so the marker is true and is on the one prose
line that needs it. `bin/evidence-check .` reads the records arm at 4 work
items, 670 names, **0 refused**.

`New units | none` is true. The target diff adds no `def` and no `class` under
`tests/` — the fix added one tuple entry, a `read` list, two `append` fields
and two assertions.

## The five corrections

Four landed. One landed somewhere other than its coordinate, with grounds.

| Correction | Where | Verified |
|---|---|---|
| `phases/phase-3.md`'s *four definitions* | `:32-33` | now *five definitions*, naming all five |
| `phases/phase-6.md`'s deleted reason | `:72-74` | the replaced sentence is quoted in place rather than left dangling |
| `survivors.md`'s preamble | `:8-27` | rewritten, and it no longer claims of all rows what was true of one |
| `survivors.md`'s missing `spec.md` row | `:33` | added, with its own quote as its anchor |
| Round 1's finding 4 Grounds splitting BROKEN and DRIFTED | **not** at `rounds/round-1.md:44` | the false split still stands there; the correction is in `seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md`, which says round 1's fix table is *a record this pass may not edit* |

The fifth is correct as done. A later pass rewriting an earlier round's Grounds
is the act `f2bfc452` was trying to undo two sections above, and the ledger row
is where a reader checking the claim would go. Left alone deliberately.

## survivors.md's new range table is stale at HEAD

The preamble says *Measured at `64f36eee`*, and `64f36eee` is not HEAD. The
table was written in `6e3f504d`, **the same commit that edited
`phases/phase-3.md`** and moved the line it cites.

| `survivors.md` | Says | Measured at `f2bfc452` |
|---|---|---|
| `:14` | `27a2d403..HEAD` reports `phases/phase-3.md:36` | `phases/phase-3.md:39` |
| `:15` | `9087705b..HEAD` reports one place, `tests/test_waiver_decided_at_start.py:639` | **no place** — exit 0, *no removed wording is still standing* |
| `:32` | that row is **Live over `9087705b..HEAD`** | live over nothing |

Round 2's own correction was that rows exempting nothing must not claim to
exempt something. The fix for it added a fourth row of the same shape, and the
new preamble pre-excuses it — *a row that exempts nothing costs nothing and is
not a claim that anything was reported* — while the row itself makes exactly
that claim. The preamble and the row contradict each other.

Nothing is broken by it: `bin/survivor-check --range 27a2d403..HEAD --exempt
<survivors.md>` is exit 0 with the one survivor excused, and the same over
`9087705b..HEAD` is exit 0. It is a correction for the closing commit.

## The broad gate has not run, and this report is what makes it due

`chain_check` at this SHA names it directly on `rounds/round-2.md`: *the one
full-suite run this design turns on has not happened, and the row is the only
place it is recorded*. Nothing below needs a fix, so the rounds have settled
and what comes due is the sealer's spawn — not a run for whoever reads this to
assemble. `agent-contract` §2 hands me none of the three and `agents/warden.md`
names none, so I ran none.

`round-2.md`'s `Fixes checked by` reads *nobody — the fixes are written and no
round has opened them*, which `chain_check` refuses beside a ticked `Pass`.
Round 3 is the answer to it, and `round-record new` sets the previous record's
cell itself — measured, it printed `set Fixes checked by of round-1.md to
round-2` on the probe run. No hand edit needed.

## What was read and not executed

- That `round-1.md:44`'s Grounds carries the split round 2 named. Read, not
  re-measured; round 2 measured both corruptions and `bin/evidence-check .` is
  green at this SHA, so the anchor's check has not failed.
- The proposed guard for `close` in `## Paste-ready fixes`. Written from the
  code, **not run**. Answered by whoever takes the issue.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 8 — the wholeness assertion's 1000-byte floor pins no wholeness | a new issue; the measured fix is below | the repository owner |
| 9 — `close` doubles a Grounds cell it has already written | a new issue; the proposed guard is below and is unmeasured | the repository owner |
| Round 2's finding 7, the sweep's own call | already deferred in round 2, to `overview.md` §*Not verified* | the repository owner |

## Paste-ready fixes

Finding 8 — `tests/test_chain_hooks_hardening.py`. Replace the append at
`:1133` and the assertion at `:1147-1152`:

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

Finding 9 — `skills/code-review/scripts/round_record.py`, in front of the
write at `:3771`. Not measured; the file write happens after this loop, so
raising here still precedes any change on disk:

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

Correction — `rounds/round-2.md`. The two rows are the only difference
between the two commits, so the file restore is the whole repair:

```
git show 1575d770:seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/rounds/round-2.md \
  > seal/specs/1789540097-three-checks-that-do-not-see-what-they-are-named-for/rounds/round-2.md
```

Correction — `rounds/round-2-report.md:258`, so the record matches the report
it is written from. Replace the Finding cell's opening:

```
| 🟢 | round 1's blocking finding is closed — all five of round 1's mutations are red, each on the case that calls the same function the sweep calls | `tests/test_chain_hooks_hardening.py:856` | confirmed | Executed: five mutations of `batch_instructions`, constants untouched, each exit 1 · 1 failed, 50 passed, each failing `test_the_sweep_refuses_a_planted_instruction_in_every_spelling`; baseline restored to exit 0 · 51 passed after each |
```

Correction — `survivors.md`. Re-measure at HEAD rather than at `64f36eee`,
and let the row say what it is:

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

## Decisions left for the orchestrator

- **The issue numbers.** Findings 8 and 9 are routed to issues this round may
  not open. The verdict cells read `deferred a new issue`; substitute the
  number when the issues are filed.
- **Whether the two issues are one.** They are the same shape — a guard whose
  own text claims more than it checks — but they sit in different files with
  different owners, so they are written as two.

## Proof block

Opened in the target tree: `seal/specs/1789540097-…/rounds/round-2.md`,
`rounds/round-2-report.md`, `rounds/round-2-fixes.md`, `rounds/round-1.md`,
`overview.md`, `survivors.md`, `phases/phase-3.md`, `phases/phase-6.md`,
`seal/ledger/1789540097-three-checks-that-do-not-see-what-they-are-named-for.md`,
`seal/ledger/1789518345-who-asks-the-routing-question-and-what-checks-the-answer.md`,
`tests/test_chain_hooks_hardening.py`,
`skills/code-review/scripts/round_record.py`,
`skills/code-review/scripts/chain_check.py`,
`skills/writing-style/SKILL.md` (user-level copy).

Executed in a `git clone --no-local` at `f2bfc452` with a `uv` virtual
environment inside it. Probe files and the clone are deleted; the target tree
is clean and holds one worktree.

Needs a fix: no
Loses a record or crashes: no

