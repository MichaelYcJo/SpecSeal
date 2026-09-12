# round 3's closing table — the run is capped, and nothing here closes on a fix

Named `round-3-closing.md` rather than `round-4-fixes.md` on purpose. Every
earlier table in this directory is named for the round that reads it, and this
one has no reader: round 1 met the floor, round 2 was its verifying round and
reopened the run on finding 16, and `docs/review-chain-spec.md` §*The
reopening — one, and then the run is capped* gives that reopening a bound of
one. So round 3 ends the run whatever it finds, and it found three things.

Range: none. **No fix commit exists and none may be written** — a fix now
would be read by nobody, which is the exact failure the verifying round exists
to prevent, and spending the reopening is what removes the reader. `close` is
run with an empty range for that reason, so both surface rows are derived from
nothing and land on `none`.

Findings 16, 17 and 5 take no row: round 3 closed them itself and a row here
would overwrite the reviewer's verdict with mine.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 18 | deferred #362 | Verified, not fixed. Re-derived by the orchestrating session rather than inherited, one input removed at a time with exit codes read directly: `REPO` absent → **exit 1**, `KeyError: 'REPO'`, loud as the line claims; `HEAD_BRANCH` absent → **exit 0**, printing `'' is not a release/vX.Y.Z branch — nothing to judge`; the hotfix skip's own line for comparison prints `'hotfix/x' is not a release/vX.Y.Z branch — nothing to judge`. So the two differ by the repr alone, and in a green step the empty one reads as the gate declining a branch it was never meant to judge. The docstring at `:50-51` calls `HEAD_SHA` *the one entry whose absence is silent rather than loud*, and by exit code two are. **It is answerable with grounds** — *silent* read as *produces no output naming the variable* is true of `HEAD_SHA` alone — which is why the round's `Needs a fix` row reads `no`; and it is worth an issue anyway, because the sentence is the whole argument for why the step's case covers every entry rather than that one. The superlative also stands at `tests/test_a_release_cannot_ship_an_untrue_milestone.py:494-496`, so the class is two coordinates (`agent-contract` §12). Behaviour is unaffected and both deletions are pinned by cases |
| 19 | deferred #362 | Verified, not fixed, and filed with finding 18 because they share one fix surface. Read and confirmed at the coordinates: the `Environment:` line names four inputs, the case at `tests/test_a_release_cannot_ship_an_untrue_milestone.py:493-497` loops over five and calls all five *read by `release_completeness_check.py`*, and the step's `env:` block at `.github/workflows/hygiene.yml:270-281` holds exactly those five keys. The fifth is `GH_TOKEN`, which reaches the script through `gh` rather than `os.environ`, so both boundaries are defensible and neither is stated. The sibling `label_merged_on_release_branch.py:48` draws the docstring's boundary, so the docstring agrees with its neighbour and the case is the odd one — and the case is also right that the step must pass all five. Settling which boundary *the script's inputs* means is what #362 is for |
| 20 | answered | **Corrected in this record's own closing commit, which is what a finding located in a record gets** — `skills/code-review/orchestration.md` §*The run ends with a verifying round*: a finding under `seal/specs/` owes no fix pass and no reader, and `Needs a fix` does not count it. Not `fixed`, because no fix pass wrote it and none may be commissioned here; marking it `fixed` would also leave `Fixes checked by` at `nobody`, which on this run's last record fails the pull request beside a ticked `Pass`. The grounds cell of finding 5 in `rounds/round-3-fixes.md` said the sweep's command returns *four* hits and then named a fifth in its own next sentence; re-run by this session, it returns **five** — `overview.md:9`, `overview.md:31`, `questions.md:17`, `plan.md:81` and `phases/phase-5.md:31`. Both copies are corrected, in that file and in the cell `close` had copied it into at `rounds/round-2.md`. The sweep itself was complete and every judgment in it was right; only the tally beside it was wrong |

## What was run

**Re-derived by the orchestrating session at `6612085`**, exit codes read
directly with no pipe, because a hand-back's verification claim is a claim:

- The three input-deletion probes above, offline — a missing `HEAD_BRANCH`
  returns before any `gh` call.
- The sweep's own command, `grep -rniE "\b(eight|nine)\b"` over the work item
  excluding `rounds/` → **five hits**, which is finding 20.
- Eight modules, one per call → **182 passed, exit 0 each**;
  `uvx ruff check` and `uvx ruff format --check` on the two changed Python
  files → **exit 0** each. Both taken at `64d830b`, round 3's target.
- The four coordinates behind findings 18, 19 and 20 opened and read.

**Not run: the broad gate.** It is the sealer's, and this record is where it
comes due.

## What the capped exit owes, and where each part went

| The rule's clause | Where it is |
|---|---|
| every finding still open becomes an issue | **#362**, holding findings 18 and 19 with the measured table and the boundary question a fix has to settle. Deliberately unmilestoned: `release: 0.11.1` holds exactly #351, #359 and #361 and the gate this branch adds requires that to stay true |
| its verdict reads `deferred #N` | the two rows above |
| `Fixes checked by` reads `no fixes to check` | written by `close`, from a table in which no verdict is a fix word |
| the pull request says `chain: capped` | the label, applied to #360 by the orchestrating session |
