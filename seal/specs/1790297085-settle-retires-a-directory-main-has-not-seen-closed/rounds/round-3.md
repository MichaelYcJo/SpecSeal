# 1790297085-settle-retires-a-directory-main-has-not-seen-closed — review round 3

| Field | Value |
|---|---|
| Target SHA | 67fda0558d1c9df8f768fd413f65416f6c571a76 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 605 |
| Broad gate | 38e25f79 against 7b557144 |
| Fixes checked by | no fixes to check |
| Fix range | `fea1aefa0a275cf3d5a0b63e1fdb4d198f0cfc4e..2ae2b3959a6967186f14ee70f42cec0421f000b2`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item 1790297085 is the verifying round after the run's one reopening. It reads round 2's fixes (4c7fb0b3..a20a02a3) at 67fda055 and ends the run whatever it finds. For each round-2 verdict closed as fixed or answered, it asks whether it is actually closed, and it searches the class of sentences placing CI's question at the fork once more, in English and Korean. It also reads PR #605's CI at that tip.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The skill names *kept until the closure reaches <base>* as the heading for every directory kept at the base; since bc63b91d the moved case prints *kept: the closure has not reached <base>* | `skills/settle/SKILL.md#"### 1. Read what is waiting"` | deferred #611 | #611 — the skill's second kept-at-base heading, filed with the round's paste-ready text; Read. The directory is still kept and the remedy printed, so behaviour is unaffected. Capped run: candidate `deferred` to a new from-review issue the orchestrator files (with ⬜ 3), answered by the repository owner |
| ⬜ 2 | 0.14.0 D3's re-read note says both heading wordings open *kept until the closure reaches <base>*; ledger M2's claim names that heading for the moved case | `seal/releases/0.14.0.md` D3; `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md` M2 | answered | corrected at 2ae2b3959a6967186f14ee70f42cec0421f000b2: `seal/releases/0.14.0.md` D3's re-read note and ledger fragment M2 name both heading wordings; Read. Paperwork correction, outside Needs a fix; the stale clause comes from round 2's ⬜ 4 fix and not from round 2's ⬜ 3 |
| ⬜ 3 | bc63b91d reworded the report's summary line and pinned nothing on it | `skills/settle/scripts/settle.py#report` | deferred #611 | #611 — the summary line's pin, filed with the round's assertion; Read: no case asserts either wording; agent-contract §14. Capped run: candidate `deferred` to the same new issue as ⬜ 1, answered by the repository owner |
| ⬜ 4 | The unverified-check documents say CI compares at the fork; on the merge ref it compares at the base's tip | `.github/workflows/hygiene.yml` unverified step comment; `templates/hygiene.yml` same; `skills/verify/scripts/unverified_check.py` module docstring, `#merge_base`, `#main` help; `README.md` and `README.ko.md` unverified-check rows; `docs/one-root-by-lifetime.md` and `.ko.md`; `skills/verify/SKILL.md` baseline paragraph | deferred #612 | #612 — the pre-existing unverified-check sentences, filed as a documents issue; Read. Predates this run (#272), and every conclusion holds on the merge ref. Capped run: candidate `deferred` to a new from-review issue, answered by the repository owner |
| 🟢 | round 2's finding 1 is closed — both README rows and the skill say CI asks at the fork only until `--released-at` moves past it, and the skill names the merge | `README.md` and `README.ko.md` settle rows; `skills/settle/SKILL.md#"### 1. Read what is waiting"` | verified | Executed: each of the four new pins red with its sentence reverted, green restored; read against `base_heading` |
| 🟢 | round 2's finding 2 is closed — settle.py says the fork and CI can disagree in either direction | `skills/settle/scripts/settle.py` module docstring; `#main` comment | verified | Read against round 2's executed probe; a grep for the clause finds it nowhere it is false |
| 🟢 | round 2's finding 3 is closed at its five coordinates | changelog fragment #602; plan.md chosen row; 0.14.0 D3; ledger M2; spec.md Data and interfaces | answered | Read; the heading clause D3 and M2 still carry is this round's ⬜ 2 |
| 🟢 | round 2's finding 4 is closed — the moved heading opens with what has not happened | `skills/settle/scripts/settle.py#RULE_MOVED_HEADING` | verified | Executed: the moved-base case red with the old opening restored |
| 🟢 | round 2's finding 5 is closed — the documents case reads the raw README row | `tests/test_settle_reads_before_it_removes.py#test_the_documents_say_the_closure_has_to_reach_the_base` | verified | Executed: red with either README row reverted |
| 🟢 | round 2's open question is closed — 51564382 turns the windows-latest leg green | `tests/test_a_script_copied_alone_exits_2.py#names_path` | verified | Executed by CI: windows failed at b589cf91 on the chain_check.py case alone, passed at 6576a226 with 4683 passed |
| carried | round 1's finding 6, seal.py and payload_meter.py copied alone | `spec.md` Scope Out | deferred #610 | already deferred in round 1; #610 is open |
| 🟢 | PR 605's tests at this tip pass on all three operating systems, windows-latest included | `tests/test_a_script_copied_alone_exits_2.py#names_path`; `tests/test_settle_reads_before_it_removes.py#test_the_documents_say_the_closure_has_to_reach_the_base` | verified | Executed by CI at 67fda055 and read from its logs: windows-latest 4683 passed, 45 skipped. The `release` check is red on `Pass` ticked beside `Fixes checked by: nobody` in round-2.md, which is the state this round's record exists to change |

## Paste-ready fixes

```markdown
tree and open at that base is listed under *kept until the closure reaches
<base>*, or, where `--released-at` has moved, *kept: the closure has not
reached <base>*, with every row open there, and `settle --retire` keeps it
and exits 1.
```
```markdown
D3, the end of the round-1 re-read note: … and the third heading comes in two
wordings chosen by `base_heading`: *kept until the closure reaches <base>*
where the ref has not moved, and *kept: the closure has not reached <base>*
where it has (**Corrected 2026-09-25 in round 3**: this said both open *kept
until the closure reaches <base>*, which round 2's ⬜ 4 fix changed); the
claim holds as corrected above

M2, in the claim: … is listed under *kept until the closure reaches <base>*
with every row open there, or, where the base has moved, under *kept: the
closure has not reached <base>*, whose heading says to merge `--released-at`
into this branch, …
```
```python
    # Round 3, ⬜ 3: the summary line counts the directories kept at the base.
    assert f"1 kept because the closure has not reached {BASE}" in text, text
```

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test` on `tests/test_settle_reads_before_it_removes.py` and `tests/test_a_script_copied_alone_exits_2.py`, in this round's clone at 67fda055 | exit 0, 131 passed |
| Probe (one file, run once, deleted): five reversions made one at a time in the clone, each followed by the documents case and the moved-base case (`-k`) and then restored — README.md's row, README.ko.md's row, the skill's *which is the base's tip*, the skill's *merging it into this branch and running `settle` again*, and the old opening of `RULE_MOVED_HEADING` | each exit 1, `1 failed, 1 passed`; `git status --short` in the clone empty afterwards |
| Probe (one file, run once, deleted): the ⬜ 3 fence added to the report case in the clone, run with `-k does_not_promise` at 67fda055 and again with the summary line put back to its old wording, then both files restored | exit 0, `1 passed`; then exit 1, `1 failed`; `git status --short` in the clone empty afterwards |
| `./bin/evidence-check --ledger <file> .` on the work item's ledger fragment, `seal/releases/0.13.0.md` and `seal/releases/0.14.0.md`, in the clone | exit 0 on each |
| `gh pr checks 605` at 67fda055, after the tests run finished | lint, ledger and all three pytest legs pass: ubuntu 4716 passed and 12 skipped, macos 4719 passed and 9 skipped, windows 4683 passed and 45 skipped. `release` fails on `chain_check.py` refusing `Pass` ticked beside `Fixes checked by: nobody` in round-2.md |
| CI logs read for PR 605's tests workflow at b589cf91 and 6576a226, windows-latest leg | b589cf91: failure, `1 failed, 4675 passed, 45 skipped`, the failure `test_a_script_copied_alone_exits_2_and_names_what_it_misses[chain_check.py]`; 6576a226: success, `4683 passed, 45 skipped` |
| The broad gate: the full suite, lint and typecheck | not yet. That run is the sealer's, once, after the rounds settle. This round ran two modules only |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/settle/scripts/settle.py#RULE_BASE_HEADING`, `#report`, `#retire`, `#main` | round 1's 🟡 1 — fixed |
| round-1 | `changelog.md` #602 entry; `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md` M2; `seal/releases/0.14.0.md` D3; `plan.md` §*Alternatives considered* | round 1's ⬜ 2 — answered |
| round-1 | `skills/settle/scripts/settle.py#main` | round 1's ⬜ 3 — fixed |
| round-1 | `skills/settle/scripts/settle.py#report` | round 1's ⬜ 4 — fixed |
| round-1 | `tests/test_settle_reads_before_it_removes.py#test_a_missing_sibling_reader_is_a_sentence_and_not_a_traceback` | round 1's ⬜ 5 — fixed |
| round-1 | `spec.md` §Scope *Out* | round 1's ⬜ 6 — deferred |
| round-1 | `fold_check.py#load`, `settle.py#load`, `round_record.py#load` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/gather_changelog.py#main`, `#section_lines` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.12.2.md`, `0.13.0.md`, `0.14.0.md`, `0.15.0.md`, `0.15.1.md`, `0.15.3.md` | round 1's 🟢 — confirmed |
| round-2 | `README.md` settle row; `README.ko.md` settle row; `skills/settle/SKILL.md#"### 1. Read what is waiting"` | round 2's 🟡 1 — fixed |
| round-2 | `skills/settle/scripts/settle.py` module docstring #602 paragraph; `skills/settle/scripts/settle.py#main` | round 2's 🟡 2 — fixed |
| round-2 | `changelog.md` #602 entry; `plan.md` Alternatives chosen row; `seal/releases/0.14.0.md` D3; `seal/ledger/1790297085-settle-retires-a-directory-main-has-not-seen-closed.md` M2; `spec.md` Data and interfaces | round 2's ⬜ 3 — answered |
| round-2 | `skills/settle/scripts/settle.py#RULE_MOVED_HEADING` | round 2's ⬜ 4 — fixed |
| round-2 | `tests/test_settle_reads_before_it_removes.py#test_the_documents_say_the_closure_has_to_reach_the_base` | round 2's ⬜ 5 — fixed |
| round-2 | `skills/settle/scripts/settle.py#base_heading`, `#survey`, `#report`, `#retire` | round 2's 🟢 — verified |
| round-2 | changelog fragment #602; ledger M2; 0.14.0 D3; plan.md Alternatives | round 2's 🟢 — answered |
| round-2 | `skills/settle/scripts/settle.py#report`, `#NO_BASE_SAYS` | round 2's 🟢 — verified |
| round-2 | `tests/test_settle_reads_before_it_removes.py#test_each_sibling_is_refused_with_its_own_purpose` | round 2's 🟢 — verified |
| round-2 | `spec.md` Scope Out | round 2's carried — deferred |
| round-2 | `docs/the-evidence-ledger.md`; `questions.md` first answered item | round 2's 🟢 — verified |
| round-2 | `seal/releases/0.13.0.md`; `seal/releases/0.14.0.md`; ledger fragment M1, M2, M3, M5 | round 2's 🟢 — verified |
| round-2 | `tests/test_a_script_copied_alone_exits_2.py#names_path` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `seal.py` and `payload_meter.py` die with a traceback when copied alone (already deferred in round 1) | #610 | the repository owner, who holds #610 |
| ⬜ 1 and ⬜ 3: the skill names one heading for both kept-at-base cases, and the reworded summary line is unpinned | candidate: a new from-review issue the orchestrator files | the repository owner, who decides whether settle's moved-case wording is followed up; without that agreement it is rung 4, this record and the pull request body |
| ⬜ 4: the unverified-check documents say CI compares at the fork | candidate: a new from-review issue the orchestrator files | the repository owner, who owns the #272 wording across the workflow, the template, the script and the READMEs |
