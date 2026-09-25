# Round 3 report — 1790260564-a-moved-file-counts-as-written

The verifying round, and the last: round 2 closed on a fix, so the run's one
reopening is spent. Target SHA `2ac16c8b`; the surface is round 2's fix range
`34bee5db..cc0a2c7c` (d81e801f, cc0a2c7c) and the one unit its `New units`
row names, `test_a_missing_common_dir_reader_refuses_rather_than_placing_nothing`.
Base `origin/release/v0.15.3` = `c52e8350`.

Worked in a `git clone --no-local` of the worktree at the target SHA, under
this round's scratchpad directory; the clone and the probe script are removed.
Carried from rounds 1 and 2 without re-deriving: the coordinates of `hook`,
`local_specs`, `on_its_branch`, `whole_range` and `report`, and the O-series
fixtures. Every verdict below is re-derived.

## What the fix pass claimed, and what the code does

| Claim (fix pass and round 2's record) | Found |
|---|---|
| ⬜ 1: the parentheticals in `whole_range`'s #439 paragraph and `report`'s docstring include the stacked-child cut | Read `survivor_check.py:1588-1597` and `:1690-1697`. `whole_range` now says *one `on_its_branch` accepts*; `report` says *one `on_its_branch` refuses*. Both are true of `on_its_branch` at `:1400-1440`, which has five refusals. Confirmed |
| ⬜ 1: the 121-column line is wrapped | Executed: no line in the touched hunks is over 88 columns; `ruff check` and `ruff format --check` on the two files exit 0. Confirmed |
| ⬜ 1: the #554 test comment includes the cut | Read `tests/test_a_corrected_sentence_survives_elsewhere.py:3489-3494`: *and on no local branch that one was cut from*. Confirmed |
| ⬜ 1: ledger 0.15.1 U1 corrected in place | Read the U1 row. Its first local-mode clause reads *one `on_its_branch` refuses*, its second *whose branch holds the tip and no branch it was cut from does*. Both match the code. A `Re-read` and a `Corrected` note are dated. Confirmed |
| ⬜ 1: E4, G5 and the 0.13.1 and 0.9.5 rows re-read and re-stamped | Word diff: only the `whole_range` and `report` hashes moved, each with a dated `Re-read` note. `evidence-check --strict` exit 0, 0 drifted. Confirmed |
| ⬜ 2: answered with no code change; round 1's sixth verdict corrected in the record | Read `round-1.md:32`: the verdict now names both halves apart and says the second was left on the orchestrator's instruction, with a dated correction note. That is what round 2's ⬜ 2 asked for. Confirmed |
| ⬜ 3: `hook(path, name, what)` names what each file answers | Read `:1358-1372`, `:1382-1384` and `:1415-1417`. The two call sites are the only callers in the tree (`git grep`). Each passes its own sentence, and the docstring no longer says whose. Confirmed |
| ⬜ 3: the new case pins the `optin.py` refusal | Executed: red against `34bee5db`'s script, green at the target; two mutations killed (below). Confirmed |
| ⬜ 3: a `survivors.md` row covers O5's docstring | Read O5 at `tests/test_a_corrected_sentence_survives_elsewhere.py:3699-3707`. It is about `hooks/routing.py`, and *says whose a local-mode declaration is* is true of that reader. Executed the fix range with and without the row: exit 0 excused, exit 1 standing at `:3700`. Confirmed |
| ⬜ 4: answered with no code change; the overview's Not done gains the detached-HEAD bound | Read `overview.md:34`. The sentence matches round 2's executed probe. The O1 ledger residual was not touched and still names the reused branch name as *the exposure that remains* (⬜ 3 below) |

## Findings

This round opened three notes, none needing a fix. Each is a coordinate a
correction left standing, one class beside what the fix pass corrected.

### ⬜ 1 — Two plugin documents still state the local-mode refusal as the tip being off the branch

`agents/smith.md:226` and `skills/code-review/orchestration.md:95`. Both
were written by this branch (`git diff c52e8350 2ac16c8b`).

**What is wrong.** Both say a declaration never reaches a range that
touches nothing in its work item, *(in local mode, one whose tip is off the
branch … `routing.md` names)*. After the cut, a stacked parent's run is
also never reached, although its tip is on the child's branch. That is the
same shape round 2's ⬜ 1 named in `report`'s docstring. The fix pass
corrected the coordinates the finding listed and left these two.

**Why it is ⬜.** The sentence is a *never*, and the set it names only grew,
so it stays true. Round 1's fix pass read E4 and G5 the same way and
recorded that the claim holds. The authority, `docs/review-chain-spec.md:870-872`,
states the cut. No behaviour and no fact is wrong.

### ⬜ 2 — The changelog fragment carries the sentence the #554 test comment was corrected away from

`seal/specs/1790260564-a-moved-file-counts-as-written/changelog.md:27`.

**What is wrong.** *the row holds over a range whose tip is on that branch*
is the exact wording round 2's ⬜ 1 had corrected in the test comment. A
stacked parent's run is a range whose tip is on the child's branch, and the
child's row does not hold over it. The sentence continues *and another
branch's range still refuses it*, which covers that case when read
generously. The fragment is gathered into `CHANGELOG.md` at the release, so
this is the one copy of the pre-cut rule that reaches a reader outside the
repository.

**Why it is ⬜.** It is under `seal/specs/`, so it is a correction to the
run's paperwork, not a defect in the tool.

### ⬜ 3 — O1's residual still says the reused branch name is the only exposure left

`seal/ledger/1790260564-a-moved-file-counts-as-written.md`, row O1's
residual cell.

**What is wrong.** The cell ends *Once the cut is refused, the reused name
above is the exposure that remains.* Round 2's ⬜ 4 executed a second
exposure. A parent's run from a detached HEAD, with no local head naming
the parent, is excused by a stacked child's row. The fix pass wrote that
bound into `overview.md:34` and left O1's cell as it was. Round 2 left
the O1 question to the orchestrator, and the fix range does not answer it.
`overview.md` is removed at settle, so the ledger residual is the copy that
outlives the work item.

**Why it is ⬜.** It is a ledger row, so the correction is to the run's
paperwork. The code does what its docstring says (*on no local branch*).

## Regression tests to plant

None. The unit the fix created is planted and was seen red.

## Facts for the evidence ledger

- O1's residual, as in ⬜ 3: a parent's run from a detached HEAD whose parent has no local head is excused by a stacked child's row. It is the same range as the child's own run at an older tip (round 2's ⬜ 4, executed).

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
| ⬜ 1 | two plugin documents state the local-mode refusal as the tip being off the branch, without the cut | `agents/smith.md:226` | open | read; also `skills/code-review/orchestration.md:95`; true as a *never*, the same reading E4 and G5 got, and incomplete beside `docs/review-chain-spec.md:870-872` |
| ⬜ 2 | the changelog fragment still says the row holds over a range whose tip is on that branch | `seal/specs/1790260564-a-moved-file-counts-as-written/changelog.md:27` | open | read; paperwork correction; the wording round 2's ⬜ 1 corrected in the test comment |
| ⬜ 3 | O1's residual names the reused branch name as the only exposure left | `seal/ledger/1790260564-a-moved-file-counts-as-written.md` | open | read; paperwork correction; round 2's ⬜ 4 executed a second exposure, now written only in `overview.md` |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| round 1's note 4 — the `corrected` line can name a move's origin | #592 | the owner, through the issue |

Needs a fix: no

Loses a record or crashes: no

## Proof block

Files opened this round: `seal/specs/1790260564-a-moved-file-counts-as-written/rounds/round-2.md`,
`rounds/round-2-report.md` (lines 1-40 and 90-125), `rounds/round-1.md:32`,
`skills/code-review/scripts/survivor_check.py` (lines 230-240, 1355-1475,
and the diff hunks at 1588-1597 and 1690-1697), `tests/test_a_corrected_sentence_survives_elsewhere.py`
(lines 74-78, 3489-3494, 3690-3718), `agents/smith.md:220-232`,
`skills/code-review/orchestration.md:90-100`, `overview.md` (diff),
`survivors.md` (diff), `changelog.md:22-32`, `spec.md:200-208`, the ledger
rows O1, U1, E4 and G5 in full, the word diffs of `seal/releases/0.13.1.md`,
`0.15.0.md`, `0.15.1.md`, `0.9.5.md` and the work item's ledger fragment, and
the diff of `docs/review-chain-spec.md` from `c52e8350`.
