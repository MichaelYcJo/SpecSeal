# Implementation Plan: the run outlives its last finding

<!-- seal/specs/1788472135-the-run-outlives-its-last-finding/plan.md — HOW, in phases.
This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

## Summary

Issues #110 and #117, on one branch because apart they undo each other.

#110 gives the round cap the floor it never had. The cap is a ceiling — three
rounds, five while a 🔴 is open — and nothing says when to stop below it, so it
gets spent: #81 ran seven rounds, and rounds 5 through 7 found nothing that
loses a record and nothing that crashes. The floor is that condition, stated
as a stopping rule and recorded in a row of the round record.

#117 bounds what a fix pass may create. Across four rounds of #82, three
consecutive rounds found their finding **inside the previous round's fixes** —
by construction the fix ships reviewed and the unit it added ships unreviewed,
in one commit. The rule is *a fix pass may add a unit; that unit's fix may
not.*

The rounds #110 removes are the rounds that were reading those units. Shipping
#110 alone cuts the eyes and leaves the generation, which is why the two land
together.

This changes what two skills instruct every future session to do, what two
agents read, and what a gate refuses at the pull request — the top rung of the
`implement` skill's ladder — so this plan comes before implementation, per this
branch's pre-answered routing (`smith`, `through the review chain`,
`open the pull request`, into `release/v0.8.0`).

## Technical context

**Where the cap is defined, and where the floor goes beside it.**

- `docs/review-chain-spec.md:32` (`## The review run has a bound, and an end`)
  through `:100`. The bound table sits at `:47-51`; `:82` already carries the
  one condition that resembles a floor — *a round that opens nothing needing a
  fix does not consume the cap* — and it is not this one. That rule is about
  the cap's arithmetic; this one is about when to stop below the cap at all.
  The two have to be readable side by side without either reading as a
  restatement.
- `skills/code-review/SKILL.md:254` (`## Orchestrator: the run ends with a
  verifying round`) through `:296`. The floor lands here because the reader who
  meets the cap is the reader who needs the floor, and because this section is
  where the verifying round is defined — the round the floor must leave
  standing.
- `templates/sdd-round.md:11-19`, the field table. The new row joins it.
  `tests/test_the_pull_request_language_is_the_repositorys.py:955`
  (`ROUND_RECORD_FIELDS`) is hand-copied from that table and pins it, so the
  list grows in the same phase as the row.

**Where the reviewer's own answer is written.**

- `agents/warden.md:93-99`. The `Needs a fix` line already lives here as a line
  of the reviewer's report, copied by the orchestrator rather than inferred
  from the verdict table. The floor answer takes the same shape for the same
  reason: the orchestrator inferring it from a verdict table is a reading, and
  the reviewer's is the finding.

**Where a fix pass is described to the agent that runs it.**

- `agents/smith.md:145-160`. The cap and the verifying round are stated here;
  what a fix pass may add is not stated anywhere the smith reads.

**The gate, and the two shapes it already refuses in.**

- `skills/code-review/scripts/chain_check.py:1375` (`fix_surface`) reads
  `Contract changes` and `New units` on every record, wired in at `:1800`.
  `:1466-1483` is the per-entry walk that refuses a unit listed without its
  reach; the depth walk is the same shape on the other row.
- `:333` `STRICT_FROM` and `:373` `SURFACE_FROM` are the grandfathering
  pattern — a unix second read from the work item's directory name, compared
  against the id of the work item that wrote the rule. Both carry the same
  recorded reasoning, and it applies unchanged here: a merged record has no
  honest repair, and a check whose first production act is red on history
  nobody can fix is a check people learn to skip.
- `:1355` (`says_none`) is the tolerance both rows share, and the depth walk
  inherits it: `none` stays an answer, with or without a reason.
- `tests/test_the_fixes_name_their_surface.py` is the sibling test file for
  the rows this work extends, including the cutoff-second case at `:234`.

**What breaks in six months.** The `New units` row grows a second thing it
carries, and a row that carries two things is a row somebody writes half of.
The mitigation is that the half is refused rather than tolerated — an entry
with no depth fails on any record, present-and-malformed being the one case
`fix_surface` already declines to grandfather. The residual risk is a record
author who writes `(depth 1)` on a unit that is really second-level, which no
check can see; the rule is a declaration, and the verifying round reading the
`New units` surface is what looks at it.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Record the two facts and read them with nothing | `Needs a fix` is this shape and says of itself that no check reads it. On a run nobody is watching, a row no check reads is true only while somebody is awake — which is the case this work item was asked against | Rejected — questions.md Q1 |
| Derive the depth instead of declaring it: match this round's verdict locations against the units earlier records named | Matching a verdict's free-text `Location` cell to a unit name is an enumeration over an unbounded domain. `chain_check.py`'s own docstring declines exactly this closing for the ASCII-arrow limit, and records the limit instead | Rejected — the same reasoning, so taking it here would contradict the file |
| A round budget per work item | #110 rejects it by name: the number of rounds worth running is a property of what the rounds find, and #104 looked small and cost four 🔴 in round 1. Fixing the count in advance decides before the evidence exists | Rejected — out of scope by the issue |
| Enforce the floor as *a record that met it is the last record* | It contradicts the verifying round. A round that met the floor may still have fixed a 🟡, and the round that reads those fixes is what sets its `Fixes checked by`. This shape would refuse the one round the run needs to end honestly | Rejected — the check refuses more than **one** later record instead, which bounds the run without forbidding the verification |
| A separate `Fix depth` row, one number per round | A single fix pass can answer a finding in code that predates the run and a finding inside an earlier pin, so one number per round cannot be true of both. #117 also names `New units` as the row that exists to make this visible | Rejected — the depth goes per entry, on the row that already names the entries |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The floor, stated and recorded: the stopping sentence in `docs/review-chain-spec.md` and `skills/code-review/SKILL.md`, the reviewer's report line in `agents/warden.md`, the `Loses a record or crashes` row in `templates/sdd-round.md`, and that row added to `ROUND_RECORD_FIELDS` | a new test pinning the sentence in all four files and the row in the template; the existing `ROUND_RECORD_FIELDS` case run and seen to fail before the list grows | `a0c134f` |
| 2 | The depth bound, stated, **with its exit written first**: where a refused unit goes — a deferral with a named answerer, or an issue — then the rule itself in `skills/code-review/SKILL.md` and `agents/smith.md`, and `New units`' entry shape in `templates/sdd-round.md` | a test pinning the rule and its exit in the three files, and the template's `New units` comment showing the `unit (depth N)` form a session can copy | `1b4d5a4` |
| 3 | The refusals in `chain_check.py`: an entry with no depth, a depth of 2 or above with the exit named in the failure, and a record that met the floor followed by more than one later round record — each grandfathered by `FLOOR_FROM` / `DEPTH_FROM` at `1788472135` | each refusal written against a fixture that does **not** satisfy it and seen red before the code that makes it green; then `pytest tests/test_the_fixes_name_their_surface.py` and the new file | `19ce128` |
| 4 | The fragments: `seal/specs/1788472135-the-run-outlives-its-last-finding/changelog.md` and `seal/ledger/1788472135-the-run-outlives-its-last-finding.md` | `.github/scripts/fold_ledger.py --check`, and `evidence-check` against the new rows | `2b547e2` |

**Status is empty, or the commit that closed the phase.** Fill it in as each
phase closes. What a phase discovers and the next phase needs goes to
`phases/phase-N.md`, from `templates/sdd-phase.md`.

Phase 2 precedes phase 3 deliberately, and the order is the point rather than
convenience: a rule that refuses without naming where the refused work goes
stops the chain at a wall. The exit is prose, the refusal is code, and the
prose ships first.

## Operational impact

- **No migration, no new environment variable, no new dependency.** The rows
  are content in a file a person already writes.
- **Compatibility break, bounded.** A repository that updates the plugin gets a
  gate that can fail a pull request on a record that would have passed before.
  It reaches work items whose directory id is at or after `1788472135` and no
  others; every earlier record prints instead, which is the trade
  `STRICT_FROM` and `SURFACE_FROM` already took and recorded.
- **Failure direction: blocks more.** Both refusals deny where they used to
  allow. That is the cheaper mistake here — a wrong deny costs one message on
  a pull request that a person is already reading, where a wrong allow ships a
  run that stopped reading its own pins.
- **Prompt budget: zero.** Nothing in this change puts a question in front of
  a person, in any session. The one question this work item had was answered in
  the batch before the first edit and is recorded in `questions.md`.
