# 1790260564-a-moved-file-counts-as-written — review round 3

| Field | Value |
|---|---|
| Target SHA | 2ac16c8bc1b2cd2da3998fafffb3005a6144f4ea |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 589 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `e2a798f485b2b7a40195264dec2aa897b762b338..e2a798f485b2b7a40195264dec2aa897b762b338`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item 1790260564 is the last, verifying round: the diff of round 2's fixes, 34bee5db..cc0a2c7c, at 2ac16c8b. Round 2 closed on a fix and spent the one reopening, so this record ends the run. Its job is whether round 2's four verdicts are closed and whether the new case is correct.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's note 1 is closed — the two parentheticals, the long line and the #554 test comment state the cut | `skills/code-review/scripts/survivor_check.py:1593` | confirmed | read `:1588-1597`, `:1690-1697`, the test comment at `:3489-3494` and ledger U1 against `on_its_branch` at `:1400-1440`; executed: ruff check and format check exit 0 on both files, `evidence-check --strict` exit 0. The rest of the class is this round's ⬜ 1 and ⬜ 2 |
| 🟢 | round 2's note 2 is closed — round 1's sixth verdict now records its two halves apart | `seal/specs/1790260564-a-moved-file-counts-as-written/rounds/round-1.md` | confirmed | read `round-1.md:32`: first half fixed at c315e8c3, second half left on the orchestrator's instruction, with a dated correction note |
| 🟢 | round 2's note 3 is closed — each missing hook's refusal names what that file answers, and the `optin.py` refusal is pinned | `skills/code-review/scripts/survivor_check.py:1358` | confirmed | read `hook` and both call sites, the only two in the tree; executed: the new case red against `34bee5db`'s script and green at the target; the `survivors.md` row for O5's docstring excuses the one survivor the fix range leaves, exit 1 without it |
| 🟢 | the new unit `test_a_missing_common_dir_reader_refuses_rather_than_placing_nothing` is correct | `tests/test_a_corrected_sentence_survives_elsewhere.py:3710` | verified | executed: red against `34bee5db`'s script with the old sentence; mutation swapping the two `what` strings, red; mutation dropping `what` from the refusal, red; O5 green in all three. It calls `local_specs` directly, so no git call is reached before the refusal |
| 🟢 | round 2's note 4 is closed — the detached-HEAD bound is recorded as not done | `seal/specs/1790260564-a-moved-file-counts-as-written/overview.md` | confirmed | read `overview.md:34` against round 2's executed probe; the O1 residual it left is this round's ⬜ 3 |
| carried | round 1's note 4 — the `corrected` line can name a move's origin | `skills/code-review/scripts/survivor_check.py:1140` | deferred #592 | already deferred in round 1; not in the fix diff |
| ❓ | round 1's question on the settle fold's verbatim arrival in `docs/` | `skills/code-review/scripts/survivor_check.py:1047` | ❓ out of verified scope | carried from rounds 1 and 2: not in the fix diff and not answered by either fix pass; the orchestrator answers whether it is #563's class and where it goes |
| ⬜ 1 | two plugin documents state the local-mode refusal as the tip being off the branch, without the cut | `agents/smith.md:226` | answered | both sentences are never-statements that stay true with the narrower condition; the full set of refusals is stated in whole_range, report and docs/review-chain-spec.md, which round 2 corrected; read; also `skills/code-review/orchestration.md:95`; true as a *never*, the same reading E4 and G5 got, and incomplete beside `docs/review-chain-spec.md:870-872` |
| ⬜ 2 | the changelog fragment still says the row holds over a range whose tip is on that branch | `seal/specs/1790260564-a-moved-file-counts-as-written/changelog.md:27` | answered | a record correction, corrected at e2a798f4; read; paperwork correction; the wording round 2's ⬜ 1 corrected in the test comment |
| ⬜ 3 | O1's residual names the reused branch name as the only exposure left | `seal/ledger/1790260564-a-moved-file-counts-as-written.md` | answered | a record correction, corrected at e2a798f4; read; paperwork correction; round 2's ⬜ 4 executed a second exposure, now written only in `overview.md` |

## Paste-ready fixes

```text
agents/smith.md:225-226 -- replace
   it never reaches a range that touches nothing in your own work item (in
   local mode, one whose tip is off the branch your `routing.md` names). The
with
   it never reaches a range that touches nothing in your own work item (in
   local mode, one whose tip is off the branch your `routing.md` names or is
   also on a local branch that one was cut from). The

skills/code-review/orchestration.md:94-96 -- replace
item (in local mode, one whose tip is off the branch that work item's
`routing.md` names), because
with
item (in local mode, one whose tip is off the branch that work item's
`routing.md` names or is also on a local branch that one was cut from),
because
```
```text
seal/specs/1790260564-a-moved-file-counts-as-written/changelog.md:27 -- replace
  `routing.md`: the row holds over a range whose tip is on that branch, and
  another branch's range still refuses it.
with
  `routing.md`: the row holds over a range whose tip is on that branch and
  on no local branch that one was cut from, and another branch's range
  still refuses it.
```
```text
seal/ledger/1790260564-a-moved-file-counts-as-written.md, row O1's residual
cell -- replace
  Once the cut is refused, the reused name above is the exposure that remains.
with
  Once the cut is refused, two exposures remain: the reused name above, and
  a parent's run from a detached HEAD with no local head naming the parent,
  which a stacked child's row excuses because it is the same range as the
  child's own run at an older tip (round 2's ⬜ 4, executed).
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` in the clone at `2ac16c8b` | exit 0, 122 passed |
| the new case and O5 against `34bee5db`'s `survivor_check.py` (script swapped in the clone, restored) | exit 1: the new case failed with *which says whose a local-mode declaration is*; O5 passed |
| mutation: the two `what` strings swapped between `local_specs` and `on_its_branch` | exit 1: the new case failed; O5 passed |
| mutation: the refusal drops `what` | exit 1: the new case failed; O5 passed |
| `git status --porcelain` in the clone after the restore | empty |
| `bin/survivor-check --range 34bee5db..cc0a2c7c --root .`, with and without the work item's `survivors.md` | with: exit 0, 16 sentences, 1 excused; without: exit 1, O5's docstring at `tests/test_a_corrected_sentence_survives_elsewhere.py:3700` standing |
| `bin/survivor-check --range c52e8350...2ac16c8b --root . --exempt` the work item's `survivors.md` | exit 0, 73 sentences, no removed wording standing |
| `bin/evidence-check --strict .` | exit 0, 2085 ok, 0 drifted, 0 broken |
| `bin/correction-check --range c52e8350...2ac16c8b` | exit 0, no merge commit in the range |
| `.github/scripts/rider_check.py` | exit 0, 25 ok, 0 drifted, 0 broken |
| `ruff check` and `ruff format --check` on `survivor_check.py` and the test module only | exit 0 both |
| Broad gate: full suite, repository-wide lint, typecheck | not yet — not run by this round; the sealer's, once. This round leaves nothing needing a fix, so the sealer's spawn is what comes due |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/survivor_check.py:1404` | round 1's 🟡 1 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1594` | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1547` | round 1's ⬜ 3 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1140` | round 1's ⬜ 4 — deferred |
| round-1 | `skills/code-review/scripts/survivor_check.py:856` | round 1's ⬜ 5 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1353` | round 1's ⬜ 6 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1120` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:544` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1566` | round 1's 🟢 — confirmed |
| round-1 | `docs/review-chain-spec.md:867` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1047` | round 1's ❓ — out of verified scope |
| round-2 | `skills/code-review/scripts/survivor_check.py:1431` | round 2's 🟢 — confirmed |
| round-2 | `skills/code-review/scripts/survivor_check.py:1413` | round 2's 🟢 — confirmed |
| round-2 | `skills/code-review/scripts/survivor_check.py:1587` | round 2's 🟢 — confirmed |
| round-2 | `skills/code-review/scripts/survivor_check.py:857` | round 2's 🟢 — confirmed |
| round-2 | `skills/code-review/scripts/survivor_check.py:1382` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790260564-a-moved-file-counts-as-written/survivors.md` | round 2's 🟢 — confirmed |
| round-2 | `skills/code-review/scripts/survivor_check.py:1589` | round 2's ⬜ 1 — fixed |
| round-2 | `skills/code-review/scripts/survivor_check.py:1366` | round 2's ⬜ 3 — fixed |
| round-2 | `skills/code-review/scripts/survivor_check.py:1432` | round 2's ⬜ 4 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| round 1's note 4 — the `corrected` line can name a move's origin | #592 | the owner, through the issue |
