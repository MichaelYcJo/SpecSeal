# 1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date — review round 3

| Field | Value |
|---|---|
| Target SHA | 5853965728be4cab3087b88ffe1c0a58179672e9 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #771 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 3 of work item `1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date` (#746, PR #771). This is the verifying round for round 2's fixes, `538f7e6e..080a03a3`. That range includes the merge of `release/v0.18.1` at `78d795fa`. Round 2 met the floor and its fix was the run's one reopening, so this record ends the run whatever it finds. A finding left open takes the filing ladder and needs a `Who answers it`.

Check whether each round-2 verdict is closed:
- 🟡5: `docs/the-pact.md`'s trigger paragraph, `skills/evidence-check/SKILL.md`'s signatory paragraph and the usage text now name the stale-refused row. A pin item holds them.
- ⬜7: the section comment.
- ⬜6 is deferred to #774.

The fix added no unit.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's yellow finding 5 is closed — the pact doc's bold trigger names a row `--into` refuses for a stale `--checked`, and the skill and the usage follow it | `docs/the-pact.md:115` | confirmed | read against `evidence_check.py:3596-3612` and `record_pact_changes`; executed: the pinned sentence fails with `538f7e6e`'s pact doc and passes at the target; the two modules pass (440) |
| 🟢 | round 2's ⬜ 7 is closed — the section comment says the refused row records its pact change | `tests/test_a_signatory_records_a_pact_change.py:1585` | confirmed | read; the cases under it assert the record and pass at the target |
| carried | round 2's ⬜ 6, an outranked coordinate recorded as a move to its own hash | `skills/evidence-check/scripts/evidence_check.py:3602` | deferred #774 | already deferred in round 2; #774 is open with the matching title |
| 🟢 | the merge of `release/v0.18.1` resolved no conflict in this item's files | `71a394b5` | confirmed | executed: `git show --remerge-diff 71a394b5` prints no hunk |
| ⬜ 8 | `templates/config.md` and the record writer's section comment still name a moved hash or a BROKEN coordinate as when a pact change is recorded, leaving the refused row out | `templates/config.md:405` | open | read; the same class as round 2's yellow 5, enumerated by `git grep`; neither says *whole trigger*, the second copy is `evidence_check.py:3706` |
| ⬜ 9 | the usage's new signatory sentence and the skill's new clause are pinned by nothing, though the account says a pin holds them | `skills/evidence-check/scripts/evidence_check.py:77` | open | read: the pin's four parameters; executed: the two proposed parameters pass at the target and fail with `538f7e6e`'s files; the skill copy is `skills/evidence-check/SKILL.md:328` |
| ⬜ 10 | the pact paragraph's `Enforced by:` line names none of the cases that hold its new trigger clause | `docs/the-pact.md:145` | open | read; `fold-check` reads presence and resolution only; no `Enforced by:` line changed anywhere in `78d795fa..HEAD` |
| ⬜ 11 | F2's Evidence cell describes phase 1's three pins, while the claim now adds the pact doc, the skill and the usage's signatory paragraph; no coordinate holds the usage sentence | `seal/ledger/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date.md:2` | open | read; a correction to the run's paperwork |
| ⬜ 12 | round 2's record says its deferral is proposed while #774 is filed | `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/rounds/round-2.md:140` | open | read; `gh issue view 774` returns the issue, OPEN; no file under the work item names it |
| ⬜ 13 | the re-read row the fix wrote affirms a released claim about a Notes trace that its cited skill section does not state | `seal/ledger/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date.md:11` | open | read: `SKILL.md:283-365` names no Notes trace, and the checker writes one only on an `--into` row (`evidence_check.py:3659`); inherited from two earlier readings |

## Paste-ready fixes

```text
templates/config.md, §Pact, replace

repository hears about.** When `evidence-check --reverify` moves the hash of
a ledger row here — or leaves a coordinate of one BROKEN — it records a pact
change in `seal/pact-changes/<work-item-id>.md`, and `pact-check` at the

with

repository hears about.** When `evidence-check --reverify` moves the hash of
a ledger row here, finds the code under one moved where `--into` refuses it
a `Re-read ·` row for a stale `--checked`, or leaves a coordinate of one
BROKEN, it records a pact change in `seal/pact-changes/<work-item-id>.md`,
and `pact-check` at the
```
```python
# skills/evidence-check/scripts/evidence_check.py, the section comment over
# record_pact_changes, replace its third to sixth lines with:
# cites clauses as pact anchors in its ledger rows. When `--reverify` moves
# the hash of a row citing a clause of a declared pact -- in place, or into a
# `Re-read ·` row -- finds the code under one moved where `--into` refuses it
# a `Re-read ·` row for a stale `--checked`, or leaves a coordinate of one
# BROKEN, the code a clause binds moved, and the pact's repository is owed a
# look. The record is written here, by the same command, because the re-read
```
```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py,
# test_the_home_and_the_usage_say_a_stale_row_is_left: append to the list
        (
            "skills/evidence-check/scripts/evidence_check.py",
            "A row `--into` refuses a `Re-read ·` row for a stale --checked is "
            "recorded too, by the run that refuses it (#746).",
        ),
        (
            "skills/evidence-check/SKILL.md",
            "or `--into` refuses such a row a `Re-read ·` row for a stale "
            "`--checked` while the code under it moved, one row per ledger row "
            "is appended to",
        ),
# and to ids:
        "the usage: the signatory's record",
        "the skill: the signatory's record",
```
```text
docs/the-pact.md, the `Enforced by:` line under §A signatory records a pact
change's first paragraph: append

, tests/test_a_signatory_records_a_pact_change.py::test_a_row_refused_for_a_stale_date_records_its_move_once, tests/test_a_signatory_records_a_pact_change.py::test_a_row_dated_after_today_has_its_move_recorded_before_its_correction
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_released_row_is_read_again_in_a_fragment.py tests/test_a_signatory_records_a_pact_change.py -q` in the round's clone at `58539657` | exit 0, 440 passed |
| `bin/test` on `test_the_home_and_the_usage_say_a_stale_row_is_left` with `538f7e6e`'s `docs/the-pact.md` in the clone, then restored | exit 1, 1 failed (the pact's trigger) and 3 passed |
| `bin/evidence-check --strict --ledger` this item's fragment, at the target | exit 0, 80 ok, 0 drifted, 0 broken |
| `bin/test tests/test_docs_line_wrap.py tests/test_no_real_identifiers.py tests/test_a_folded_statement_names_what_enforces_it.py tests/test_one_word_one_meaning.py -q` at the target | exit 0, 91 passed |
| A probe module named by §7, pinning the usage's signatory sentence and the skill's clause, at the target, then with `538f7e6e`'s two files | 2 passed, then 2 failed; deleted after the run, files restored |
| `git show --remerge-diff 71a394b5` | no hunk |
| The broad gate (full suite, repository lint, typecheck) | not yet; the sealer's, and it has come due |

```text
# The pin probe: the two sentences of ⬜ 9, each read with whitespace
# collapsed, as the pin it would join reads them. Run once at 58539657
# (2 passed), once with `git show 538f7e6e:<file>` written over SKILL.md and
# evidence_check.py in the clone (2 failed); files restored, probe deleted.
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3645` | round 1's 🟡 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3591` | round 1's 🟡 2 — fixed |
| round-1 | `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/changelog.md:21` | round 1's ⬜ 3 — answered |
| round-1 | `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/overview.md:18` | round 1's ⬜ 4 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3506` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:2924` | round 1's 🟢 — confirmed |
| round-1 | `docs/the-evidence-ledger.md:178` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date.md:4` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:5` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_a_signatory_records_a_pact_change.py:74` | round 1's 🟢 — confirmed |
| round-2 | `docs/the-pact.md:115` | round 2's 🟡 5 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3602` | round 2's ⬜ 6 — deferred |
| round-2 | `tests/test_a_signatory_records_a_pact_change.py:1585` | round 2's ⬜ 7 — fixed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3496` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:5108` | round 2's 🟢 — confirmed |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:67` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_a_signatory_records_a_pact_change.py:1588` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| round 2's ⬜ 6, an outranked-OK coordinate recorded as a move to its own hash | #774; already deferred in round 2 | the owner of #774's record writer fix |
| ⬜ 8, `templates/config.md:405` and `evidence_check.py:3706` omit the refused row | proposed: a follow-up issue beside #774, since both name the record writer's trigger | the orchestrator, who decides whether to file it |
| ⬜ 9, the usage sentence and the skill clause unpinned | proposed: the same follow-up issue as ⬜ 8; the paste-ready parameters are below | the orchestrator, who decides whether to file it |
| ⬜ 10, the pact paragraph's `Enforced by:` line | proposed: a question on the fold's rule for an edit to a folded statement, not this item's alone | the orchestrator, who decides whether to file it |
| ⬜ 11 and ⬜ 12, the F2 Evidence cell and round 2's deferral naming #774 | corrections to this item's paperwork, before the seal | the orchestrator |
| ⬜ 13, the re-read row over `seal/releases/0.18.0.md:79` | proposed: a follow-up issue on the released row's claim | the orchestrator, who decides whether to file it |
| Without the freeze, one `--reverify` over every ledger moves the line a fragment's citing rows cite (round 1's deferral) | `overview.md` §*Not done*; already deferred in round 1 | the orchestrator, who decides whether to file it |
