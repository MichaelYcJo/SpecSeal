# 1790134781-a-label-description-past-100-characters-fails-every-release — review round 2

| Field | Value |
|---|---|
| Target SHA | d02c479ddf3307aa2918fa10be4036e3d541431d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #524 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `0e2935cc9420fc1a9fd87aca82c764d984f926e4..af590c9fd83a5237cc74ae95c223a005fa061776`, 2 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |
<!-- New units: .github/workflows/close-issues-on-release.yml read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

Round 2 is the run's verifying round. It read the diff of round 1's fixes, `24f8a92..a6bdf34`, to check that each of round 1's three verdicts is actually closed. It also read the unit those fixes created, `test_a_failed_step_cannot_skip_the_independent_steps_after_it`, as a finding surface, and judged the implementer's widening of finding 1 to the label step.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 1's finding 1: the roll step carries `if: ${{ !cancelled() }}` | `.github/workflows/close-issues-on-release.yml:65` | fixed `59d067e` | Verified this round. PyYAML reads the condition on the step, and the case goes red with it removed, on its own param |
| 🟢 | Round 1's finding 2: the module index and §15 paragraph name A13 and A14 and send them to C1 and C2 | `tests/test_a_declared_label_reaches_the_tracker.py:18-43` | fixed `59d067e` | Verified this round. Read, and the retirement claim is checked against f2943c0 |
| 🟢 | Round 1's finding 3: `overview.md` counts four mutations | `seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/overview.md:6` | answered | Verified this round. Read, and it matches C1's four |
| 🟢 | The fix was widened to the label step, so a failed close no longer skips the reconcile | `.github/workflows/close-issues-on-release.yml:57` | not a defect | The reconcile is idempotent and reads nothing the close writes. After a failed checkout it fails loudly on a missing script, in a job already red |
| 🟢 | `!cancelled()` rather than `always()` or `success() \|\| failure()` | `.github/workflows/close-issues-on-release.yml:57,65` | not a defect | `always()` also runs after a cancel, and GitHub's reference warns against it. The third is equal at a step, and the case pins one form |
| 🟢 | New unit `test_a_failed_step_cannot_skip_the_independent_steps_after_it` | `tests/test_a_declared_label_reaches_the_tracker.py:258-276` | not a defect | Seven mutations, executed. Each param goes red on its own, and a moved but equal condition stays green |
| 4 | ⬜ correction: the changelog fragment does not carry round 1's condition, so the released entry would name the description as the only repair | `seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/changelog.md:1-12` | answered | corrected at af590c9 — `changelog.md` now says a failed step no longer skips the label step or the flow-measurement roll unless the job is cancelled; Read. No commit in the fix range touches it, and a6bdf34's subject claims the records carry the condition |
| 5 | ⬜ correction: the verified line still lists the cap as unverified and omits the `!cancelled()` item | `seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/overview.md:6` | answered | corrected at af590c9 — `overview.md`'s proof-block `verified` line moves the cap to read, cites the REST reference and the expressions reference, and lists a real runner's `!cancelled()` as unverified; Read. The same file's table marks the cap ✅ read, and C1 says Read |
| 6 | ⬜ The comment and the new case say the two steps read nothing an earlier step writes, and both read checkout's tree | `.github/workflows/close-issues-on-release.yml:50-51`, `tests/test_a_declared_label_reaches_the_tracker.py:21,268` | **fixed** `e0b6601` | fixed at e0b6601; Read, `git grep`. Behaviour is right. The sentence means the close step and says every earlier step |
| 7 | ⬜ correction: C2's Read cell carries the same overstatement | `seal/ledger/1790134781-a-label-description-past-100-characters-fails-every-release.md` C2 | answered | corrected at af590c9 — C2's Read cell names only what the two steps actually depend on, carries `Corrected 2026-09-23`, and adds the expressions reference; Read. C2's Clause is unaffected |

## Paste-ready fixes

```markdown
- A failed step in the close-issues workflow no longer skips the steps
  behind it that do not depend on it: the label step and the
  flow-measurement roll now run unless the job was cancelled, so the next
  refusal of any kind costs a red job and not a release's roll.
  (`1790134781-a-label-description-past-100-characters-fails-every-release`,
  #515)
```
```markdown
read — the specifying section, the scripts, #515, and GitHub's REST reference for *Create a label* for the cap's value; unverified — how a real runner evaluates `!cancelled()` after a failed step, the live tracker, the broad gate
```
```yaml
      # This step and the roll below read nothing the close step writes, so
      # neither may be skipped by an earlier step failing: #515's over-long
```
```python
       failed, because neither reads what the close step writes (#515)
```
```python
    it succeeded. Neither step reads what the close step writes, so a failure
```
```markdown
nothing either reads is written by the close step before it
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_a_declared_label_reaches_the_tracker.py -k "failed_step or workflow"` at `d02c479` | 3 passed, exit 0 |
| A probe script (test_tmp prefix) that mutated the workflow seven ways and ran the new case after each, then restored the file | see the mutation table: each removal or changed form reds its own param alone; the condition moved below `env:` stays green; file restored, probe deleted, clone deleted |
| PyYAML (through `uv run --with pyyaml`) over the workflow | parses, exit 0; the label step and the roll carry `${{ !cancelled() }}`, and checkout and close carry none |
| `evidence-check --strict` on this work item's ledger fragment | 8 ok, 0 drifted, 0 broken, exit 0 |
| `evidence-check --strict` on `seal/ledger.md` | exit 0 |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet — nobody has run it. It is the sealer's, and with this round opening nothing that needs a fix it has come due: the next act is the sealer's spawn, once the orchestrator has written this round's record and applied the corrections |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/workflows/close-issues-on-release.yml:56-61` | round 1's 1 — fixed |
| round-1 | `tests/test_a_declared_label_reaches_the_tracker.py:10-34` | round 1's 2 — fixed |
| round-1 | `seal/specs/1790134781-a-label-description-past-100-characters-fails-every-release/overview.md:6` | round 1's 3 — answered |
| round-1 | `.github/scripts/tracker_labels.py:111-114` | round 1's 🟢 — not a defect |
| round-1 | `.github/scripts/label_merged_on_release_branch.py:104-113` | round 1's 🟢 — not a defect |
| round-1 | `seal/ledger.md:2498` | round 1's 🟢 — not a defect |
| round-1 | tree at `a479a38` | round 1's 🟢 — not a defect |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
