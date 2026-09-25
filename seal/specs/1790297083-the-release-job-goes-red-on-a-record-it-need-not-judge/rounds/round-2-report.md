# Round 2 report — work item 1790297083, the verifying round

Target: `e36888e3`, the tip after round 1's fixes and its closed record. Fix
range read: `1f21376f..8decc62c`, 5 commits, 21 files. Round 1's `New units`
row reads `none`, and nothing in the range adds a function, a template
section or a test, so there is no unreviewed unit to judge as code. The one
code hunk is a docstring qualifier in `written_late`.

## What this round was asked

For each round-1 verdict closed as fixed or answered, whether it is actually
closed. For 🟡 1 in particular, whether each of the eight copies the fix pass
widened to under contract §12 says the same thing as the code, and whether a
ninth copy exists in a shipped document or template that the widening missed.

## What the fix pass claimed, and what the code does

The draft behaviour every copy now describes is `chain_check.checked_by`,
read in the clone: with `strict` false (a draft), `Pass` beside `nobody` on
the last record of a work item begun on or after `STRICT_FROM` returns a
notice rather than an error. The notice says to spawn one verifying round and
that *Ready for review* re-runs the check and fails the pull request if the
cell still says `nobody`. With `strict` true (ready, or a state that cannot be
read) the same pair is an error. Both `.github/workflows/test.yml` and
`hygiene.yml` list `ready_for_review` among their trigger types, so the
re-run the copies promise is real. Executed: the draft and `nobody` cases of
`tests/test_the_last_rounds_fixes_are_checked.py`, 14 passed.

The eight copies, each read against that behaviour:

| Copy | What it says now | Same meaning as the code |
|---|---|---|
| `README.md:213-218` | fails a ready pull request; on a draft the pair prints and names the verifying round | yes |
| `README.md:610-618` | fails a ready pull request; on a draft prints, names the round, *Ready for review* re-runs | yes |
| `README.ko.md:210-212` | fails a PR that is ready for review; on a draft only prints and says to spawn the verifying round | yes, and it matches the English line 213 paragraph, which also omits the re-run |
| `README.ko.md:605-613` | fails a ready PR; on a draft prints, says to spawn the verifying round, *Ready for review* re-runs | yes, and it matches English line 610 clause for clause |
| `skills/code-review/orchestration.md:295` | fails a ready pull request; on a draft prints and names the verifying round; *Ready for review* re-runs | yes, and it agrees with line 519 of the same file |
| `skills/implement/orchestration.md:547` | fails a ready pull request; on a draft prints and names the verifying round | yes |
| `agents/sealer.md:113-114` | `nobody — <why>` beside a checked `Pass` fails a ready pull request | yes. The `seal` refusal it describes is right in either state |
| `templates/sdd-round.md:119-126` | FAILS a ready pull request; on a draft prints and names the verifying round; *Ready for review* re-runs | yes |

"Names the verifying round" in the English copies and "tells you to spawn the
verifying round" in the Korean ones are the same claim about the same notice
text. None of the eight says a draft fails, and none says a ready pull
request passes.

## Findings

### 🟡 1 — the smith's own definition still says the pair fails the pull request at every stage

`agents/smith.md:301-303`, read:

> That pair, `nobody` beside a checked `Pass` on the last record, **fails the
> pull request** for any work item begun after the rule landed

This is the ninth copy of the rule, and it carries exactly the defect round
1's 🟡 1 named in the other three: no draft exception. Since `cfb2b745` the
eight copies around it say the pair fails only a ready pull request, so the
agent that writes the fixes now reads the one version of the rule that
contradicts both the check and every other document.

Why it matters: the smith is the reader this paragraph exists for. It is told
the draft pull request goes red the moment `close` ticks `Pass`. That is the
state #598 instance 4 was about, and this work item changed it. A fix pass
that believes it can push the pull request red has a reason to do what the
orchestration document forbids, such as waiting to commit the closed record.
The paragraph's conclusion (spawn the verifying round) is still right. Its
stated consequence is wrong for the stage the pull request is actually in.

How the widening missed it: the sentence is worded differently from the
other copies (`**fails the pull request** for any work item begun after`),
and `survivor-check` looks for removed wording standing elsewhere, so it had
nothing to match. The copy predates this run (blame: `c414d02d`, 2026-09-01).
It is a pre-existing sentence of the class the fix was owed under §12, not a
unit this run's fixes created.

Enumeration, executed: `git grep` over every tracked file outside `tests/`,
`CHANGELOG.md` and `seal/` for the rule's wording (`beside a checked Pass`,
`Pass beside`, `nobody beside`, the Korean `Pass 옆` and `Pass 가 체크`, and
`nobody` beside `fail|refus|깨|막`). Every hit was read in context. The copies
that state the rule without the draft half, other than this one and ⬜ 2:

- `docs/round-record-spec.md:96` and `:584`, and `chain_check.py:124` and
  `:2622`, each sit in a file that states the draft half in full nearby
  (`round-record-spec.md:46` and its table row at `:63`, and
  `chain_check.py:151` and `:2209`). Not a defect.
- `docs/review-chain-spec.md:314` narrates the floor walk at ready, and the
  same file states the draft half at `:638` and `:908`. Not a defect.
- `docs/review-handoff-protocol.md:274` is the portable protocol, which
  leaves the choice to the project. Not a copy of this project's rule.
- `round_record.py:1526` is a docstring about `close` on a capped run's last
  record. It says the check refuses the pair, which is true at ready. Not a
  defect.
- No `.ko.md` file other than `README.ko.md` mentions `Fixes checked by`.

The fix drifts four ledger rows anchored at
`agents/smith.md#"## Phases"`: `seal/releases/0.6.0.md:18`,
`seal/releases/0.8.1.md:37`, `seal/releases/0.12.0.md:64` and
`seal/releases/0.15.1.md:94`. Each is re-read against the edit and
re-stamped in place with a dated `Re-read` note, as the fix pass did for the
rows it drifted.

### ⬜ 2 — `seal`'s refusal says the orchestration document fails a pull request, without "ready"

`skills/code-review/scripts/round_record.py:4494-4497` (read). The `seal`
subcommand refuses `nobody` on the last record and explains:
*"`skills/code-review/orchestration.md` fails a pull request whose last
record reads `nobody` beside a checked `Pass`"*. That document now says it
fails a ready one and prints on a draft. `seal` runs before the draft goes
ready, so the sentence describes a failure the pull request is not in at that
moment.

The refusal and its instruction (spawn the verifying round first) are right
in either state, which is why this is ⬜ rather than 🟡: nothing a sealer does
after reading it changes. It is the same class as 🟡 1, but in a message
rather than a document. A change to it is a change someone reads, so under
§14 it takes a pin. `tests/test_the_seal_is_taken_once_by_the_sealer.py`
pins only `Spawn the verifying round first` today, at `:2936` and `:3054`.

## Round 1's verdicts, answered

- **🟡 1** (three copies with no draft exception). The three named places and
  the five the widening added are correct (table above). The class is not
  closed, because the ninth copy is 🟡 1 of this round.
- **⬜ 2** (handoff protocol names the untouched record and not the restored
  one). `docs/review-handoff-protocol.md:190-191` now reads *"a record the
  pull request does not touch, or restores byte-for-byte from the base's own
  history"*. That matches the reachability arm and `written_late` as round 1
  confirmed them. Verified, read.
- **⬜ 3** (`written_late` docstring). The docstring now says *"an ordinary
  record with no fix verdict pays no extra `git log`"*. The body at
  `chain_check.py:3232-3236` returns before `restored_from` exactly when
  `commissioned_fixes` is empty, so the qualifier is the true one. Verified,
  read.
- **⬜ 4** (restoration exit reaches untouched records). It was answered with
  no code. `spec.md` Scope 2's `written_late` bullet and the
  `docs/review-chain-spec.md` restoration row now both state that the arm asks
  it of an untouched record, and why (a squashed-then-merged branch's own
  record is the base's claim). The code has no touched-check before
  `restored_from`, so the sentence describes it. Answered, read. Round 1's
  probe 3 Q2 is the execution, carried and not re-run.
- **⬜ 5** (changelog "three records"). The fragment reads *"three shapes of
  record"*, and the three it lists are shapes. Verified, read.

The ledger half of the fix range is re-stamps with `Re-read` notes on rows
that `2381b8dc`, `cfb2b745` and `c50e47c7` drifted. I spot-read the notes
against their edits; each describes the edit it follows. `evidence_check.py .`
in the clone reports 0 drifted and 0 broken in every file.

## Regression tests to plant

- `tests/test_the_last_rounds_fixes_are_checked.py`: a case that reads every
  shipped document naming `Fixes checked by` or `nobody — <why>` (the agents,
  the skills, the templates, both READMEs) and fails where a sentence says the
  pair fails a pull request without also saying *ready*, or where a file
  states the refusal and never mentions a draft. Round 1 and this round each
  found copies by grep, and survivor-check could not see a differently worded
  one. The case is what keeps a tenth copy from arriving the same way. Seen
  red first by running it against `agents/smith.md` as it stands at
  `e36888e3`.
- `tests/test_the_seal_is_taken_once_by_the_sealer.py`: if ⬜ 2 is fixed,
  extend the two existing asserts at `:2936` and `:3054` to pin `fails a
  ready pull request`.

## Facts for the evidence ledger

- `agents/smith.md#"## Phases"`: the four rows named under 🟡 1 are re-read
  and re-stamped where they are when the fix lands. No new claim is needed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the ninth copy of the `Pass`-beside-`nobody` rule says the pair fails the pull request with no draft exception; round 1's 🟡 1 class, missed by the widening | `agents/smith.md:301` | open | read. Contradicts `checked_by`'s `strict` branch and the eight fixed copies. Worded differently, so survivor-check could not match it. Found by the enumerating grep (executed) |
| ⬜ 2 | `seal`'s refusal says the orchestration document fails a pull request, without "ready" | `skills/code-review/scripts/round_record.py:4496` | open | read. The refusal and its instruction are right in either state, so ⬜. A change needs a pin (§14) |
| 🟢 | round 1's 🟡 1: the eight copies it names or widened to now match the code | `README.md:213`, `README.md:610`, `README.ko.md:210`, `README.ko.md:605`, `skills/code-review/orchestration.md:295`, `skills/implement/orchestration.md:547`, `agents/sealer.md:113`, `templates/sdd-round.md:119` | verified | read, each against `chain_check.checked_by`'s `strict` branch. Executed: 14 draft and `nobody` cases passed. The class stays open through 🟡 1 of this round |
| 🟢 | round 1's ⬜ 2 is closed: the handoff protocol names the restored record | `docs/review-handoff-protocol.md:190` | verified | read |
| 🟢 | round 1's ⬜ 3 is closed: the `written_late` qualifier is the true one | `skills/code-review/scripts/chain_check.py#written_late` | verified | read, the early return on empty `commissioned_fixes` precedes `restored_from` |
| 🟢 | round 1's ⬜ 4 is answered in spec.md and the review-chain spec row, and the code matches | `docs/review-chain-spec.md` restoration row | answered | read. The code has no touched-check before `restored_from`. Round 1's probe 3 Q2 carried, not re-run |
| 🟢 | round 1's ⬜ 5 is closed: the changelog counts shapes | `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/changelog.md:1` | verified | read |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_last_rounds_fixes_are_checked.py -k "draft or nobody"` at `e36888e3`, in the round's clone | 14 passed, exit 0 |
| `evidence_check.py .` at `e36888e3`, in the round's clone | exit 0; every ledger file reports 0 drifted and 0 broken |
| `git grep` over every tracked file outside `tests/`, `CHANGELOG.md` and `seal/` for the rule's wording, English and Korean, then each hit read in context | nine copies state the rule without leaning on a nearby full statement. Eight are correct and one (`agents/smith.md:301`) is 🟡 1. A message copy is ⬜ 2 |
| `git grep` of the ledger for anchors into `agents/smith.md` | four rows at `#"## Phases"@12c56e52`, which 🟡 1's fix drifts |
| the broad gate: full suite, lint, typecheck | not yet. The sealer's, once, after the rounds settle; this round ran none of it |

## Paste-ready fixes

### 🟡 1

`agents/smith.md`, replacing lines 301-303:

```
last fixes nobody opened. That pair, `nobody` beside a checked `Pass` on the
last record, **fails a ready pull request** for any work item begun after the
rule landed. On a draft it prints and names the verifying round, and *Ready
for review* re-runs the check. The way out is the verifying round above,
which costs no round.
```

Then re-read the four rows anchored at `agents/smith.md#"## Phases"`
(`seal/releases/0.6.0.md:18`, `0.8.1.md:37`, `0.12.0.md:64`, `0.15.1.md:94`)
and re-stamp each with a note in this shape:

```
**Re-read 2026-09-25 by work item 1790297083's round 2 fix pass (#598).** One sentence of `## Phases` gained the draft half of the `Pass`-beside-`nobody` rule. Nothing this row claims moved, so the claim holds.
```

### ⬜ 2

`skills/code-review/scripts/round_record.py`, the `seal` refusal:

```
            "`skills/code-review/orchestration.md` fails a ready pull request "
            f"whose last record reads `{chain.NOBODY}` beside a checked "
            "`Pass`. "
```

And in `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside each of
the two existing asserts:

```
    assert "fails a ready pull request" in out, out
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1, the ninth copy of the `Pass`-beside-`nobody` rule in `agents/smith.md` that still says it fails the pull request at every stage

Loses a record or crashes: no

The broad gate is not yet run. It is not due at this round: 🟡 1 leaves a
fix to write, and the sealer's spawn comes due after that fix's verifying
answer.

## Proof block

Files opened this round:

- `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/rounds/round-1.md`
- `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/routing.md`
- `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/spec.md` (Scope 2 and Scope 4, and the acceptance table)
- `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/changelog.md`
- the diff `1f21376f..8decc62c` in full, the ledger hunks word by word, and `8decc62c..e36888e3`
- `skills/code-review/scripts/chain_check.py`: 118-160, 416-474, 2196-2360, 2612-2626, 3227-3260
- `skills/code-review/scripts/round_record.py`: 1520-1532, 4470-4505
- `agents/smith.md`: 294-310; `agents/sealer.md`: 111-114
- `docs/review-chain-spec.md`: 308-320, 632-648, 902-915
- `docs/review-handoff-protocol.md`: 184-192, 268-282
- `docs/round-record-spec.md`: 44-66, 90-100, 580-590
- `skills/code-review/orchestration.md`: 295, 515-525; `skills/implement/orchestration.md`: 547
- `README.md`: 205-218, 608-618; `README.ko.md`: 208-213, 603-613; `templates/sdd-round.md`: 116-126
- `tests/test_the_last_rounds_fixes_are_checked.py`: 806-845
- `.github/workflows/test.yml` and `hygiene.yml`, the trigger types
