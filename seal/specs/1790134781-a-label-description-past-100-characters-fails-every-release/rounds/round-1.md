# 1790134781-a-label-description-past-100-characters-fails-every-release — review round 1

| Field | Value |
|---|---|
| Target SHA | a479a38700cc5ce66efeaa29236a148dd5e034a3 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #524 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Fix range | `24f8a928dbccd0e582bedfacf77bc6429483aec5..a6bdf34d6cc051447ccdcd37b02fe1e1d0fdeb90`, 2 commits |
| Contract changes | none |
| New units | test_a_failed_step_cannot_skip_the_independent_steps_after_it (depth 1) |
| Needs a fix | yes — finding 1, the roll step still depends on the label step succeeding |
| Loses a record or crashes | no |
<!-- New units: .github/workflows/close-issues-on-release.yml read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

Round 1 read the whole branch against its base: the shortened `size: now` description, the shared 100-character constant and the two cases that hold every declared description to it, the T2 re-read in `seal/ledger.md`, and the new C1 row. Stage 1 compared against #515's body and `docs/issues-and-milestones.md` §*A label answers what it is about, and survives the move*, because the ladder called for no `spec.md`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The roll step has no `if:`, so any failure of the label step skips the flow-measurement roll, which is #515's second cost | `.github/workflows/close-issues-on-release.yml:56-61` | **fixed** `59d067e` | fixed at 59d067e; The workflow has three steps in sequence with the default `success()` condition. The probe was red at `a479a38` and green with `if: ${{ !cancelled() }}`, and the neighbouring workflow cases stayed green |
| 2 | ⬜ The module docstring's case index omits the new cap case, and its §15 paragraph points every case's red run at `1790076050` | `tests/test_a_declared_label_reaches_the_tracker.py:10-34` | **fixed** `59d067e` | fixed at 59d067e; Read. The index lists A9 to A12. The new case's red run is in C1 |
| 3 | ⬜ correction: `overview.md` says five single-unit mutations, and C1 and the hand-back list four | `seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/overview.md:6` | answered | corrected at a6bdf34 — `overview.md` now says four single-unit mutations and why one unit was run twice; Read. C1 names four mutations |
| 🟢 | The shortened description keeps what the label means and when it comes off | `.github/scripts/tracker_labels.py:111-114` | not a defect | 95 characters, measured. The first clause is the document's words minus the subject, and the close it names is the moment the document names |
| 🟢 | `LABEL_DESCRIPTION_LIMIT` lives beside one of its two users | `.github/scripts/label_merged_on_release_branch.py:104-113` | not a defect | Two functions call `gh label create`. The other reaches the constant through its existing `signal` import |
| 🟢 | T2 is edited in the shared ledger | `seal/ledger.md:2498` | not a defect | `CONTRIBUTING.md:204-215` gives the `--reverify` arm for a claim that still holds. `evidence-check --strict` returned 1468 ok |
| 🟢 | No other place in the tree states the old description or the 119-character state as current | tree at `a479a38` | not a defect | Read, `git grep`. The old text survives only as a quotation in `overview.md` |

## Paste-ready fixes

```yaml
      # The roll reads the version in the tree and the open flow-measurement
      # issue, and nothing the steps above write. So a failure above must not
      # skip it: #515's over-long label description failed the label step and
      # cost a release its roll. The job still goes red on that failure.
      - name: roll the flow-measurement issue to the next version
        if: ${{ !cancelled() }}
        env:
          GH_TOKEN: ${{ github.token }}
          REPO: ${{ github.repository }}
        shell: bash
        run: python3 .github/scripts/roll_flow_measurement_issue.py
```
```python
def test_a_failed_label_write_cannot_skip_the_roll():
    """#515's second cost. The label step failing skipped the roll behind it,
    because a step with no `if:` runs only when every step before it
    succeeded. The label reconcile is not a gate, so its failure must not
    decide whether the log rolls."""
    with open(WORKFLOW, encoding="utf-8") as f:
        text = f.read()
    steps = re.split(r"^      - ", text, flags=re.M)
    roll = [s for s in steps if s.startswith("name: roll the flow-measurement issue")]
    assert roll, "the workflow no longer has the roll step"
    assert re.search(r"^        if: \$\{\{ !cancelled\(\) \}\}\s*$", roll[0], re.M), (
        "the roll runs only when every step before it succeeded, so a failed "
        "label write skips it again"
    )
```
```text
  A13  every declared description fits the tracker's cap, read from
       `LABEL_DESCRIPTION_LIMIT` (#515); its red run is recorded in
       work item 1790134781's ledger row C1
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the two changed case files | 44 passed, exit 0 |
| The cap case with the 119-character description restored | 2 failed (cap case and A9), exit 1. Reverted |
| `evidence-check --strict` on this work item's ledger fragment and on `seal/ledger.md` | 5 ok and 1468 ok, 0 drifted, exit 0 both |
| A `test_tmp_*` case asserting the roll step carries `if: ${{ !cancelled() }}` | red at `a479a38`, green with the line added. Reverted and deleted |
| That probe plus `test_a_declared_label_reaches_the_tracker.py` and `test_a_release_rolls_the_flow_measurement_issue.py`, with the fix | 52 passed, exit 0 |
| `test_release_hygiene.py -k "close or workflow or token"`, with the fix | 8 passed, exit 0 |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it. It is the sealer's, and it comes due once the rounds leave nothing open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
