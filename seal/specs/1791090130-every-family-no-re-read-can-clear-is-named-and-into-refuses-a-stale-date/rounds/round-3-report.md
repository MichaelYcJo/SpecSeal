# 1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date — review round 3 report

| Field | Value |
|---|---|
| Round | 3 |
| Target SHA | `5853965728be4cab3087b88ffe1c0a58179672e9` |
| Base | `release/v0.18.1` at `78d795fa` |
| Fix range verified | `538f7e6e..080a03a3` (the merge `71a394b5` and the fix `080a03a3`), and the closing commit `58539657` |
| Reviewed by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` of the worktree at the target, under the session's scratchpad; nothing was written in the worktree but this file |

## What this round was asked

Round 3 of work item `1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date` (#746, PR #771). This is the verifying round for round 2's fixes, `538f7e6e..080a03a3`. That range includes the merge of `release/v0.18.1` at `78d795fa`. Round 2 met the floor and its fix was the run's one reopening, so this record ends the run whatever it finds. A finding left open takes the filing ladder and needs a `Who answers it`.

Check whether each round-2 verdict is closed:
- 🟡5: `docs/the-pact.md`'s trigger paragraph, `skills/evidence-check/SKILL.md`'s signatory paragraph and the usage text now name the stale-refused row. A pin item holds them.
- ⬜7: the section comment.
- ⬜6 is deferred to #774.

The fix added no unit.

## What this round found

The target moved once during the round: the spawn read `080a03a3`, and the
orchestrator then closed round 2's record at `58539657`. The diff between
the two is `rounds/round-2.md` alone (7 lines each way), so every reading
below holds at `58539657`.

### Round 2's yellow 5 is closed, and the code says what the new sentence says

The account claimed that the pact doc, the skill and the usage now name a
row `--into` refuses for a stale `--checked` among what records a pact
change. Read against the code: the refusal arm of `reverify_into`
(`skills/evidence-check/scripts/evidence_check.py:3596-3612`) appends every
drifted coordinate of the refused row to the moves, and
`record_pact_changes` (`evidence_check.py:3778`) filters them by `Pact
notify` exactly as it filters a written row's. So the new clause of the
bold sentence at `docs/the-pact.md:115-119` — *finds the code under such a
row moved where `--into` refuses it a `Re-read ·` row for a stale
`--checked`* — names a trigger the code has, and *that test is the whole
trigger* is true again. The added sentence at `docs/the-pact.md:123-125`
(*recorded by the run that refuses it, because its repair may be a
`Corrected ·` row*) matches round 1's reasoning for the fix.

The skill clause at `skills/evidence-check/SKILL.md:328-329` says *such a
row* — a row citing a clause — and adds *while the code under it moved*,
which matches. The usage sentence at `evidence_check.py:77-78` inherits the
paragraph's *citing a clause of a declared pact*, which also matches.

The account also claimed *a pin item holds them*. That is true of one of
the three. The new parameter of
`test_the_home_and_the_usage_say_a_stale_row_is_left` pins the pact doc's
sentence only; the skill clause and the usage sentence are pinned by
nothing (⬜ 9 below). Executed: the pinned case fails with `538f7e6e`'s
`docs/the-pact.md` swapped into the clone, so the pin was seen red (§15).

The one subtlety in the new sentence is round 2's ⬜ 6: an outranked
coordinate whose own hash did not move is recorded as a move to the same
hash. That is the case where *the code under such a row moved* is not
literally true of the coordinate, and it is already deferred, now as #774.

### Round 2's ⬜ 7 is closed

`tests/test_a_signatory_records_a_pact_change.py:1585` now reads *records
its pact change*, which is what the cases under it assert (A5 and the
after-today case pass at the target).

### The merge carried nothing into this item's files

`git show --remerge-diff 71a394b5` prints no hunk, so the merge resolved no
conflict. The two narrow modules and the item's ledger fragment were run at
the target after it (Executed probes).

### Three more statements of the same class name the trigger without the refused row

Round 2 named the class as *statements of when a pact change is recorded*,
and the fix covered the pact doc, the skill and the usage. Enumerated with
`git grep` over every statement that records a pact change, outside the
round records and the released files, two more say when one is recorded
and leave the refused row out:

- `templates/config.md:405-407` — *When `evidence-check --reverify` moves
  the hash of a ledger row here — or leaves a coordinate of one BROKEN — it
  records a pact change*. This is what a signatory reads when choosing its
  `Pact notify` value.
- `skills/evidence-check/scripts/evidence_check.py:3706-3709`, the section
  comment over `record_pact_changes`, in the same two-part shape.

Neither says *the whole trigger*, so each is incomplete rather than false,
which is why round 2 held the skill and the usage to the same grade. The
behaviour is right, and nothing a person does on reading either goes wrong
for long: the refusal names its own `recorded` line. It is ⬜ 8.

The other hits are true as written: `reverify`'s MOVES docstring
(`evidence_check.py:2994`) is about the in-place writer, `reverify_into`'s
docstring (`evidence_check.py:3555-3556`) already says a refused row's
moves still go to MOVES, and `skills/implement/orchestration.md:548`,
`pact_check.py:52` and `hooks/config.py:620` say *when its code moved*
without naming a form.

### The pact paragraph's `Enforced by:` line names none of the cases that hold its new clause

The bold sentence at `docs/the-pact.md:115` is a folded statement, and its
`Enforced by:` line (`docs/the-pact.md:145`) names #756's eleven cases.
After this fix, the sentence names a third trigger whose cases are
`test_a_row_refused_for_a_stale_date_records_its_move_once` and
`test_a_row_dated_after_today_has_its_move_recorded_before_its_correction`,
and neither is named there. `fold-check` reads only that the line exists and
resolves, so nothing goes red. This is ⬜ 10. The same holds for every
folded section this item edits — no `Enforced by:` line changed in
`78d795fa..HEAD` — so whether an edit to a folded statement owes its line
a new target is a question for the orchestrator rather than for this fix
alone.

### Paperwork (corrections, outside `Needs a fix`)

- **⬜ 11, the F2 ledger row's Evidence cell describes phase 1 only.**
  `seal/ledger/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date.md:2`.
  The claim now adds *`docs/the-pact.md`, the evidence-check skill and the
  usage's signatory paragraph name such a row*, but the Evidence cell still
  reads *each of the three pinned sentences removed through
  `bin/mutation-check`, each red* with phase 1's date. There are now four
  pinned sentences, the fourth seen red by this round and not by the cell.
  The usage's signatory sentence is held by no coordinate either: the
  usage's quote anchor names the refusal sentence
  (*outranks gets no Re-read row, is named,*), and its hash did not move
  with this edit.
- **⬜ 12, round 2's record says the deferral is proposed while #774 is
  filed.** `rounds/round-2.md:37` reads *deferred to a new issue* and its
  Deferred row (`rounds/round-2.md:140`) reads *proposed: a new issue*.
  #774 is open with the matching title, and no file under the work item
  names it.
- **⬜ 13, the fix wrote a re-read row affirming a claim this round could
  not find in its cited section.**
  `seal/ledger/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date.md:11`
  re-reads `seal/releases/0.18.0.md:79`, whose claim ends *so the trace goes
  in the Notes, on every row a re-stamp touched*, against `skills/evidence-check/SKILL.md`
  §*Re-verifying is recomputing the hash*. That section
  (lines 283-365) never mentions the Notes, and the checker writes a
  `Re-read <date>` note only on an `--into` row (`evidence_check.py:3659`),
  never on an in-place re-stamp. The two readings before this one (the
  0.18.0 correction and #756's re-read) say the same thing, so this is
  inherited rather than introduced; the re-stamp happened only because the
  fix edited that section. It is a question about the released row's claim,
  not about this item's code.

The fix range's `3 commits` in `rounds/round-2.md:11` counts the squash of
#766 that the merge brought in; the fix itself is one commit. That is how
`round_record.py close` counts a range with a merge in it, and it is noted
here rather than raised.

### Read, not executed

Whether the full suite, the repository lint and the typecheck pass is
`unverified`. That is the sealer's run, after this round, and this round
leaves nothing that needs a fix, so it has come due.

## Regression tests to plant

- `tests/test_a_released_row_is_read_again_in_a_fragment.py`, the
  parametrized pin `test_the_home_and_the_usage_say_a_stale_row_is_left`:
  two more parameters, for the usage's signatory sentence and the skill's
  clause (⬜ 9, fenced below). Both were seen green at the target and red
  with `538f7e6e`'s two files, in a probe deleted after its one run.

## Facts for the evidence ledger

- F2's Evidence cell should carry round 3's execution of the fourth pin:
  *the pact doc's sentence removed (the file at `538f7e6e`), red* — and a
  coordinate for the usage's signatory sentence if F2 keeps claiming it
  (⬜ 11).

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

## Paste-ready fixes

### ⬜ 8

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

### ⬜ 9

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

### ⬜ 10

```text
docs/the-pact.md, the `Enforced by:` line under §A signatory records a pact
change's first paragraph: append

, tests/test_a_signatory_records_a_pact_change.py::test_a_row_refused_for_a_stale_date_records_its_move_once, tests/test_a_signatory_records_a_pact_change.py::test_a_row_dated_after_today_has_its_move_recorded_before_its_correction
```

Needs a fix: no

Loses a record or crashes: no

## Proof block

Files opened this round:

- `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/rounds/round-2.md`, at `080a03a3` and at `58539657`
- `seal/specs/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date/rounds/round-2-report.md`
- `git show 080a03a3` (the whole fix diff) and `git diff 080a03a3 58539657`
- `docs/the-pact.md:64-72`, `:100-165`
- `skills/evidence-check/SKILL.md:283-331`, `:528-540`
- `skills/evidence-check/scripts/evidence_check.py:60-82`, `:2990-3010`, `:3540-3615`, `:3700-3720`, `:3778-3830`
- `tests/test_a_released_row_is_read_again_in_a_fragment.py:1975-2040`
- `tests/test_a_folded_statement_names_what_enforces_it.py:1-60`
- `templates/config.md:402-412`
- `skills/evidence-check/scripts/pact_check.py:48-56`
- `skills/implement/orchestration.md:544-552`
- `hooks/config.py:616-626`
- `seal/ledger/1791090130-every-family-no-re-read-can-clear-is-named-and-into-refuses-a-stale-date.md`, rows 1-2 and 11 (through the fix diff)
- `seal/releases/0.18.0.md:79`, `seal/releases/0.8.0.md:180` (by `grep`)
- `seal/config.md` (by `grep`: no `Pact` row, so this repository records no pact change)
- `gh issue view 774`
