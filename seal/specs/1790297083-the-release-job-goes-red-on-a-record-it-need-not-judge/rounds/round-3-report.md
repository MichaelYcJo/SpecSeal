# Round 3 report — work item 1790297083, the verifying round after the reopening

Target: `1aea54ae`, the tip after round 2's fixes and its closed record. Fix
range read: `e58b62d3..bc6f4a4c`, 1 commit, 17 files (6 outside `seal/`).
Round 2's `New units` row reads `none`, and the range adds no function, no
section and no case, only two assertions inside existing cases, so there is
no unreviewed unit to judge as code. The closing commit `1aea54ae` also
dropped a stale `@12c56e52` from two coordinates in `round-2-report.md`.

This round ends the run. What it finds cannot be fixed on this branch, so the
one finding below carries a `deferred` home and a named answerer.

## What this round was asked

Whether round 2's 🟡 1 (the ninth copy of the `Pass`-beside-`nobody` rule, in
`agents/smith.md`) and ⬜ 2 (`seal`'s refusal omitting "ready") are closed.
Whether the three places the fix pass widened to under contract §12 each say
what the code does. Whether the semicolon the fix pass used in
`agents/smith.md` kept the sentence's meaning. And one more search for the
rule's meaning, in English and Korean.

## What the fix pass claimed, and what the code does

The behaviour every copy has to describe is `chain_check.checked_by`, read at
`skills/code-review/scripts/chain_check.py:2323-2358`. With `strict` false (a
draft), `Pass` beside `nobody` on the last record of a work item begun on or
after `STRICT_FROM` returns a notice. That notice says to spawn one verifying
round, and that *Ready for review* re-runs the check and fails the pull
request if the cell still says `nobody`. With `strict` true (ready, or a
state that cannot be read) the same pair is an error.

### Round 2's 🟡 1 — closed

`agents/smith.md:301-305` (read) now says the pair **fails a ready pull
request**, that on a draft it prints and names the verifying round, and that
*Ready for review* re-runs the check. Each clause matches `checked_by`: the
draft notice does name the verifying round as the remedy, and the ready branch
is the error.

The semicolon. The fix pass joined *Ready for review re-runs the check* and
*the way out is the verifying round above* with a semicolon instead of a full
stop, because `tests/test_a_fix_pass_may_add_a_unit.py:61` opens the smith's
section at the lowercase phrase `the way out is the verifying round above`.
The meaning held. *The way out* still refers to the pair the paragraph is
about, and nothing in the draft clause competes for that reference. The
sentence is longer, and still one reading. Executed: that module passes at
`1aea54ae`, so the section is still bounded where the case expects.

The rider in `agents/smith.md:116` was re-stamped to `"## Phases"@035903e4`.
Executed: the rider module passes (29 cases).

### Round 2's ⬜ 2 — closed, and the pin was seen red

`skills/code-review/scripts/round_record.py:4496-4498` (read) now says the
orchestration document fails a **ready** pull request. Both cases that read
the refusal assert the phrase, at
`tests/test_the_seal_is_taken_once_by_the_sealer.py:2937` and `:3056`.

Contract §15, executed: in this round's clone I replaced `round_record.py`
with its `e58b62d3` version and ran the two cases. Both failed, each at the new
`fails a ready pull request` assertion and at no earlier line. The file was
restored and the clone's tree was clean afterwards.

### The three places the fix pass widened to — each correct

- `skills/code-review/scripts/chain_check.py:123-126` (read), the module
  docstring's cell table. It now says `nobody` fails a ready pull request
  beside a checked `Pass` on the last record, and that a draft prints it.
  Correct against `checked_by`.
- `docs/round-record-spec.md:584-585` (read), §*The fix surface*. It now says
  the check refuses the pair on the last record at a ready pull request.
  Correct.
- `docs/review-chain-spec.md:314-315` (read), §*The floor*. It now says the
  walk's terminal record is refused both ways, the second one at a ready pull
  request. Correct, and the paragraph's conclusion does not depend on the
  draft half. The other refusal it names, `no fixes to check` beside `fixed`,
  reads no `strict` and is refused at every stage, which is what the unchanged
  half of the sentence says.

Both documents' edited lines now run to about 100 characters where the
surrounding prose wraps near 78. That is cosmetic and not a finding.

The seventeen ledger rows the edits drifted each carry a `Re-read 2026-09-25`
note naming this work item's round 2 fix pass, and a new hash. Executed:
`evidence_check.py --strict .` exits 0.

### The search once more

Executed: one `git grep` over every tracked file outside `tests/`,
`CHANGELOG.md` and `seal/`, for the rule's English wordings (`beside a
checked/ticked Pass`, `Pass beside`, `nobody beside`, `fails the/a pull
request`, `refuses … nobody`, `nobody` near `fail`/`refus`) and its Korean
ones (`Pass 옆`, `Pass 가 체크`, `nobody` near `깨`/`막`/`실패`/`거부`). I read
each hit in context. I also listed every file that names `Fixes checked by`
and read each one's `nobody` lines. The only Korean files that carry the rule
are `README.ko.md:209-212` and `:605-610`, and both state the draft half.

Every copy round 2 named and every copy the fix pass widened now states the
draft half, or sits in a file that states it in full nearby. One copy is
worth a row, below.

### ⬜ 1 — the fix pass widened one of two twin paragraphs and left the other

`skills/code-review/scripts/chain_check.py:2622-2623` (read), in
`fix_surface`'s docstring, says `checked_by` "refuses it on the LAST record
beside a checked `Pass`". That paragraph is the docstring twin of
`docs/round-record-spec.md:582-587`. Both describe the pending arm's silence
for `nobody — <why>` in the same words: a notice on every record, a refusal
on the last, and a non-terminal record false by construction. The fix pass
added "at a ready pull request" to the spec's copy and not to the code's.

It is ⬜ and not 🟡. The fact it states is true at ready, and the same module
states the draft half in full at `chain_check.py:123-126`, `:152-158` and
`:2210-2219`. By round 2's own test, which judged both of these copies not a
defect, it ships no wrong behaviour and no wrong fact. What it leaves behind
is two copies of one paragraph that now disagree in wording. It also shows
that the fix pass's claim was incomplete: its commit message says a sweep
found three more statements with no draft half. The fix pass applied a
stricter test to `round-record-spec.md:584` than round 2 did, and under that
stricter test this twin qualifies too.

Why the sweep missed it, executed: `survivor-check --range
e58b62d3..bc6f4a4c` reports no removed wording standing. The twin says
*carrying it* where the spec said *carrying `nobody`*, so it scores under the
floor. `docs/round-record-spec.md:96` and `round_record.py:1526` are the other
two unqualified statements. Round 2 read both as not a defect, and the fix
pass did not widen to them. I read both again and agree: each sits next to a
full statement of the draft half (`round-record-spec.md:46-63`), or it
describes `close` on a capped run's last record, where the claim is true at
ready.

A fix would drift the `chain_check.py#fix_surface` anchors in
`seal/releases/0.4.0.md` (two rows), so whoever takes it re-reads and
re-stamps those rows as well. The paste-ready fix is below.

## CI at `1aea54ae`

Executed (`gh pr checks 608`, read five times while this round ran): `lint`,
`ledger`, `release`, `pytest (ubuntu-latest, 3.12)` and `pytest
(macos-latest, 3.12)` pass. `pytest (windows-latest, 3.12)` was still pending
at the last read, with 0 seconds elapsed, so it is ❓. The pull request is a
draft.

Executed, a probe of the record format: I copied this report into the
clone's work item and ran `round_record.py new` there. It exited 0 and wrote
a round-3 record with every row above, `Needs a fix` reading `no`, `Fixes
checked by` reading `no fixes to check`, and a note that the run is `capped`.
That record existed only in the clone, which was then deleted.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | `fix_surface`'s docstring says `checked_by` refuses `nobody` beside `Pass` on the last record without "at a ready pull request", while its twin in the round-record spec was widened by the fix pass | `skills/code-review/scripts/chain_check.py:2623` | deferred #598 | read. True at ready, and the module states the draft half at `:123`, `:152` and `:2210`, so no defect ships. Survivor-check does not reach it (executed). Deferred because the run is capped. The branch did not create the unit, and #598 owns the draft/`nobody` state (instance 4) |
| 🟢 | round 2's 🟡 1 is closed — `agents/smith.md` states the draft half | `agents/smith.md:301` | verified | read against `checked_by`'s `strict` branch. The semicolon join keeps the meaning, and `tests/test_a_fix_pass_may_add_a_unit.py` passes (executed) |
| 🟢 | round 2's ⬜ 2 is closed — `seal`'s refusal says "a ready pull request", pinned twice | `skills/code-review/scripts/round_record.py:4496` | verified | read. Executed: both pinning cases pass at the target and fail at the new assertion with the `e58b62d3` message (§15) |
| 🟢 | the widening to the module docstring's cell table is correct | `skills/code-review/scripts/chain_check.py:124` | verified | read against `checked_by` |
| 🟢 | the widening to the round-record spec's fix-surface section is correct | `docs/round-record-spec.md:585` | verified | read |
| 🟢 | the widening to the review-chain spec's floor section is correct | `docs/review-chain-spec.md:315` | verified | read. The other refusal it names reads no `strict`, which matches the unchanged half |
| 🟢 | the seventeen drifted ledger rows are re-read and re-stamped, and the rider is re-stamped | `seal/releases/` (11 files), `agents/smith.md:116` | verified | read, each added row carries the dated note. Executed: `evidence_check.py --strict .` exit 0; rider module 29 passed |
| 🟢 | the record correction in `round-2-report.md` drops a hash that would be stale again after the fix | `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/rounds/round-2-report.md:96` | verified | read. The ledger rows now carry `@cede28c2`, so a hash in the report prose would be wrong either way |
| ❓ | PR #608's `pytest (windows-latest, 3.12)` leg at `1aea54ae` | PR #608 checks | ❓ out of verified scope | still pending at this round's last read; the other five legs pass. The orchestrator answers it, from `gh pr checks 608` before the sealer's seal is taken |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_fix_pass_may_add_a_unit.py` and the two `seal` refusal cases of `tests/test_the_seal_is_taken_once_by_the_sealer.py`, at `1aea54ae`, in the round's clone | 11 passed, exit 0 |
| the same two `seal` refusal cases with `round_record.py` replaced by its `e58b62d3` version, then restored | 2 failed, each at `assert "fails a ready pull request" in out`; the clone was clean afterwards |
| `bin/test tests/test_a_rider_reaches_its_file.py` at `1aea54ae` | 29 passed, exit 0 |
| `evidence_check.py --strict .` at `1aea54ae` | exit 0; 0 drifted, 0 refused |
| `survivor-check --range e58b62d3..bc6f4a4c` | exit 0, no removed wording standing. It does not reach ⬜ 1 |
| `git grep` for the rule's English and Korean wordings over every tracked file outside `tests/`, `CHANGELOG.md` and `seal/`, each hit read in context | every copy states the draft half or sits beside a full statement; ⬜ 1 is the one twin the widening left |
| `gh pr checks 608` at `1aea54ae` | lint, ledger, release, pytest ubuntu and pytest macos pass; pytest windows pending |
| `round_record.py new --round 3` over this report, inside the clone | exit 0; the record parsed with every verdict row, `Needs a fix` no, run noted `capped`; the clone was then deleted |
| the broad gate: full suite, lint, typecheck | not yet. It is the sealer's, once, after this round; this round ran none of it |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1, `fix_surface`'s docstring twin of the widened spec paragraph | #598, as a comment carrying the paste-ready fix below | the orchestrator of this run, who posts the comment before the release closes #598, or files a `from-review` issue instead if the change should outlive that close |

## Paste-ready fixes

### ⬜ 1

In `skills/code-review/scripts/chain_check.py`, `fix_surface`'s docstring,
replace the four lines from `` `checked_by` prints a notice `` through
`reviews round N's fixes — and nothing refuses that today` with the
following. Then re-read and re-stamp the two `chain_check.py#fix_surface`
rows in `seal/releases/0.4.0.md`.

```
      `checked_by` prints a notice for it on every record and refuses it on
      the LAST record beside a checked `Pass` at a ready pull request. A
      non-terminal record carrying it is false by construction — a later
      record exists, and round N+1 reviews round N's fixes — and nothing
      refuses that today
```

Needs a fix: no

Loses a record or crashes: no

## The broad gate

Not yet. Nothing in this report needs a fix, so the gate has come due: what
comes due is the sealer's spawn, after the orchestrator reads the pending
Windows pytest leg.

## Proof block

Files opened this round, all at `1aea54ae` unless noted:

- `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/rounds/round-2.md`
- `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/rounds/round-2-report.md`
- the diffs of `bc6f4a4c` and `1aea54ae`
- `agents/smith.md:285-315`
- `skills/code-review/scripts/chain_check.py:95-180`, `:2197-2370`, `:2612-2630`, `:4540-4565`
- `skills/code-review/scripts/round_record.py:1518-1532`
- `docs/round-record-spec.md:44-50`, `:88-100`, `:570-592`
- `docs/review-chain-spec.md:295-325`, `:484-500`, `:632-642`, `:904-912`
- `skills/code-review/orchestration.md:515-540`
- `skills/verify/scripts/broad_gate.py:72-86`
- `README.ko.md:205-214`, `:603-610`
- `tests/test_a_fix_pass_may_add_a_unit.py:40-135`
- the lines matched by the class sweep, in every file listed under *The search once more*
