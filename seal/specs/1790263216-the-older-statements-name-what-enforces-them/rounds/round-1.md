# 1790263216-the-older-statements-name-what-enforces-them — review round 1

| Field | Value |
|---|---|
| Target SHA | 2f24d6a43747f3451e7e8c484d4eac144a5f440b |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `7e9bf98fc0c0a0c33e7ba211d53f0e49e211efa2..c231af284b2be3832ab79e32fc31aa14fc45f6aa`, 2 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 to 🟡 6: four `nothing` lines whose case is wrong (D6's also states a falsehood about the workflow), D33's target that does not hold its rule, and the release checklist's two rider-stamp sentences |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of work item 1790263216 reviews the retrofit at 2f24d6a4, range e9dfe623..2f24d6a4 (stacked on #587), against spec.md's What a decision is and plan.md (frame 3d26fc04). It sampled every nothing line, 14 random read-only decisions (seed 565) and three chosen ones, with seven mutations. The classes are targets that resolve but would not catch their rule, nothing lines whose case is wrong, and statements whose prose changed beyond the bold opening.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | D6's line says `nothing — a person's act` for a rule whose instruction is pinned, and its reason says the correction-check leg is allowed to fail, which the workflow and `test_a9_the_leg_runs_the_check_and_is_allowed_to_fail` contradict | `docs/the-evidence-ledger.md:148` | **fixed** `6826f53f` | fixed at 6826f53f; executed: the pin `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` goes red when CONTRIBUTING.md's instruction is reworded; read: no `continue-on-error` in any workflow |
| 🟡 2 | D13's line says `nothing` for a rule whose settle instruction is pinned | `docs/the-evidence-ledger.md:343` | **fixed** `6826f53f` | fixed at 6826f53f; executed: `test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row` red when the skill's sentence is reworded |
| 🟡 3 | D14's line says `no case reads it yet`, and a case reads settle's three answers | `docs/the-evidence-ledger.md:358` | **fixed** `6826f53f` | fixed at 6826f53f; executed: `test_the_skill_names_the_floors_a_fold_has_to_answer` red when *retire the case* is reworded |
| 🟡 4 | D32's line says `nothing — a session's act` for the rule the statement itself locates in the contract's §15, which is pinned | `docs/round-record-spec.md:941` | **fixed** `6826f53f` | fixed at 6826f53f; executed: `test_each_section_holds_its_rule` red (1 of 16) when §15's phrase is reworded |
| 🟡 5 | D33's targets pin the statement's third bold sentence, not its bold opening *Three and five count rounds* | `docs/review-chain-spec.md:112` | **fixed** `6826f53f` | fixed at 6826f53f; executed: the opening reworded to say the numbers bound fixes, both targets green (26 passed) |
| 🟡 6 | The release checklist still says rider stamps name commits by SHA, the half D89 corrected; the survivor sweep cannot see a differently-worded carrier | `docs/release-checklist.md:30` | **fixed** `6826f53f` | fixed at 6826f53f; also `docs/release-checklist.md:261`; executed: `test_no_rider_stamp_names_a_commit` red on an old-form stamp, and survivor-check exits 0 over the range |
| ⬜ 7 | D90's *A third reader* counts a reader D89's correction removed, and its pin's docstring still enumerates the rider stamps | `docs/branch-and-release.md:146` | answered | D90's A third reader is a dated measurement; the fact about the plugin directory still holds, and the overview's Not done carries it; disclosed in the overview's *Not done*; the fact about the plugin directory stays right; the pin is `tests/test_the_release_tail_does_not_end_at_the_tag.py:188` |
| ⬜ 8 | Phase records: phase 2 says the 7 skips are not targets, and they are D21's target parametrised; phase 1's D6 row repeats *allowed to fail* | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/phases/phase-2.md:82` | answered | a record correction, corrected at c231af28; a correction to the run's paperwork; executed with `-rs` |
| 🟢 | The retrofit is complete: `fold-check` reads 136 statements, binds 136 at cutoff `0`, and holds 14 documents under the ceiling | `seal/config.md` | confirmed | executed at 2f24d6a4, with no flag and with `--shape-from 0`, both exit 0 |
| 🟢 | Every named test target is collected and passes | the 116 added `Enforced by:` lines | confirmed | executed: 174 node ids, 256 passed, 7 skipped, exit 0 (the skips are finding 8's) |
| 🟢 | The Korean edition carries byte-identical targets, and the editions case compares them | `docs/one-root-by-lifetime.ko.md` | confirmed | executed: the two editions' lines diff empty; the editions module passes; read: `enforcement` reads the span and value through the shape check's own functions |
| 🟢 | The ledger is true after the edits | `seal/ledger.md` | confirmed | executed: `bin/evidence-check .` 2094 ok, 0 drifted, 0 broken, exit 0 |
| ❓ | Whether the 58 `read` decisions this round did not open catch their breaking edits | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/phases/` | ❓ out of verified scope | a sample of 14 found one failure (D33), so the class may hold more; a verifying round or the smith's fix pass answers it by the same test against each remaining row |

## Paste-ready fixes

```
Enforced by: tests/test_a_merge_cannot_silently_drop_a_correction.py::test_a8_both_rule_documents_say_what_to_do_at_the_conflict
```
```
Enforced by: tests/test_settle_reads_before_it_removes.py::test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row, tests/test_settle_reads_before_it_removes.py::test_the_skill_says_what_a_fold_does_to_the_ledger
```
```
Enforced by: tests/test_settle_reads_before_it_removes.py::test_the_skill_names_the_floors_a_fold_has_to_answer
```
```
Enforced by: tests/test_the_agent_contract_holds_the_universal_rules.py::test_each_section_holds_its_rule
```
```
Enforced by: nothing — no case reads it yet. A pin on *Three and five count rounds* beside rule 13 in `tests/test_the_rules_have_one_owner.py` would; the ownership rule after it is held by `test_the_owner_states_the_rule` and `test_every_link_names_the_owner`.
```
```
      **Never rebase a work item's branch, for any reason** — every round
      record names its branch's commits by `Target SHA`, a rebase orphans
      them, and that is the class this repository has a patch release about.
```
```
green without a push. Press ***Create a merge commit***, never squash: the
review records name the release branch's commits by `Target SHA`, and a
squash discards them.
```
```
**Another reader points at those commits now, and it is outside this
```
```
    """A8. The rule already named the round records' `Target SHA`, which this
    repository can repair. This reader cannot be repaired from here, which is
    the whole reason it is worth writing down."""
    rule = squash_rule()
    assert "Another reader points at those commits now" in rule, (
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/fold-check` and `bin/fold-check --shape-from 0` at 2f24d6a4 | both exit 0; 136 statements read, the cutoff 0 binds 136; 14 documents held to 1000 lines, 0 listed |
| `bin/evidence-check .` | exit 0; 2094 ok, 0 drifted, 0 broken; 2 work items' records read, 0 refused |
| `bin/test` over the 174 node ids the added lines name | exit 0; 256 passed, 7 skipped; `-rs` shows all 7 as parametrisations of `test_every_script_a_shipped_document_names_is_wrapped_or_classified` for scripts no document names |
| `bin/test` over the editions, shape, ceiling, wrap and release-tail modules | exit 0; 103 passed |
| `bin/survivor-check --range e9dfe623..2f24d6a4` | exit 0; 81 removed sentences, none standing, so the checklist's reworded carriers are invisible to it |
| the Korean edition's `Enforced by:` lines compared with the English edition's | identical |
| M-a: D33's opening reworded to *Three and five bound the fixes a run may write.* | both targets green, 26 passed: the target does not catch it |
| M-b: CONTRIBUTING.md's *resolve it hunk by hunk and read both sides* reworded | `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` red |
| M-c: settle's *A fold opens no directory under `seal/specs/`* reworded | `test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row` red |
| M-d: settle's *retire the case* reworded | `test_the_skill_names_the_floors_a_fold_has_to_answer` red |
| M-e: the contract's §15 phrase *before it is committed as a case* reworded | `test_each_section_holds_its_rule` red, 1 of 16 |
| M-f: the rider stamp in `.github/scripts/fold_ledger.py` put back to *Verified 2026-09-08 at 8f967708* | `test_no_rider_stamp_names_a_commit` red |
| M-g: a version *99.1.0* written into `skills/settle/SKILL.md` | `test_no_loaded_file_names_a_version_at_or_above_the_running_one` red |
| the broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `CLAUDE.md` §*the merge method is fixed per direction* still says the rider stamp names a commit | already deferred by the smith: this work item's `survivors.md` row and the overview's *Not done* | the repository owner, whose file it is |
| The milestone description of `release: 0.15.3` says 101 | already deferred by the smith: `spec.md` §*The measured worklist* and the overview's *Not done* | the orchestrating session, which makes tracker posts |
