# 1790835051 — review round 2 report

Ran by `specseal:warden on claude-opus-5-5`, at `a0c66d18ab7f7783d2fc14526dcbe8fb81d132a0`,
in a `git clone --no-local` of the worktree checked out at that SHA
(`<scratchpad>/1790835051/round-2/clone`). The worktree was only read, and
the one file written in it is this report.

This is a verifying round. Its target is round 1's fix range
`090cb32f..bab8dc4a` (five commits), plus the merge `f3b18cff`, which no
round had read. It answers whether each of round 1's four `fixed` verdicts is
closed, and judges the six units round 1's `New units` row names.

## In one view

```
round 1                       fix          this round
🟡 1 --check stops early   -> eec243df  -> closed, class closed   (executed: red at 090cb32f, mutation, byte identity)
⬜ 2 35 rows, no note      -> 2331a820  -> closed                 (read: 48 notes, sample against the code)
⬜ 3 "the chain arm's key" -> c7867e1c  -> closed, behaviour right (read: routing.py vs chain_check.py)
⬜ 4 the ask's two lines   -> ff99ce10  -> closed                 (executed: red at 090cb32f, mutation)
survivor at commit-review-gate-spec.md:765 -> bab8dc4a -> grounds hold
merge f3b18cff             -> changes nothing this branch's code or documents do or say
```

Nothing this round found needs a fix. One correction to this work item's own
`spec.md` is left, and it is paperwork.

## Round 1's yellow finding 1 is closed, and so is its class

Round 1 found that `seal --check` returned before three refusals the write
path raises inside callees. The fix composes the record above the `--check`
return and writes it below. I read `seal` at the target
(`skills/code-review/scripts/round_record.py:4446-4614`).

The order is now: `seal_home`, the six `raise` sites, `kept_broad_gate`,
then the composition. For a record, the composition calls `field_index` and
`cell`. For `broad-gate.md` it calls `new_broad_gate_file`, which calls
`cell`. Then `hiders_close` runs on the composed text at `:4602`, and the
`--check` guard follows at `:4606`. The next statement is `write_record` at
`:4611`.

Nothing between the guard and `write_record` can refuse, because there is
nothing between them. `write_record` (`:696`) calls `hiders_close` again on
the same text, so it raises nothing the line at `:4602` has not raised
already. Its `open` can still raise an `OSError`, and that is a write
failing, not a refusal. The chain check after the write is excluded by
`spec.md` S1 in so many words (*runs no `chain_check`*). None of
`kept_broad_gate`, `same_run` or `new_broad_gate_file` has a `raise` of its
own. So the ten refusals the docstring names are the whole of what refuses
before the write.

Executed:

- **The new cases fail on the defect.** I copied `090cb32f`'s
  `round_record.py` and `broad_gate.py` over the clone's files and ran the
  seven new or changed cases. All seven failed, exit 1. The files were then
  restored.
- **The position case fails on a narrower mutation.** I removed only the
  `hiders_close` call above the return. Two cases failed: the position case,
  with *`hiders_close` is not asked above the `--check` return*, and the
  `open-comment` id of `test_seal_check_refuses_what_the_write_path_refuses`,
  where `--check` printed `round-record: checked … raises no refusal`.
- **A full `seal` is byte-identical to before.** The smith's probe covered
  four shapes. I covered five: a settled last record, the same record sealed
  a second time at a new commit (so an `earlier run` is kept), a direct item
  with no `broad-gate.md`, a direct item sealed a second time, and a capped
  item. Each was copied twice and sealed once by `090cb32f`'s tree and once by
  the target's. Exit codes, stdout and stderr, and the record's bytes were
  equal in all five. The first run of the probe failed only because
  `run_check` names its temporary payload file in a line it prints. With that
  one name normalised, all five passed.
- **The write path's refusals are unchanged without `--check`.** On the three
  hand-edited shapes, the full `seal` at both trees exited 2 with the same
  text and left the record unchanged. `--check` at the target printed exactly
  what the full run printed. A pipe in `--broad-gate` was refused the same way
  by all three: old, new, and new with `--check`.

The new behavioural case covers `field_index` twice and `hiders_close` once.
It does not cover `cell`. Only the position case pins `cell` by name, and my
probe showed that `--check` does refuse a pipe. The value the preflight hands
over is `<sha> against <sha>`, so the preflight cannot reach that refusal. I
do not count this as a finding.

## Round 1's finding 2 is closed

The smith counted 48 rows rather than 35. I counted again from
`git diff -U0 090cb32f bab8dc4a -- seal/releases seal/ledger`. It shows 56
rows rewritten: 48 under `seal/releases/` and 8 in this work item's own
fragment. All 48 in the release files name `1790835051` or `#702`. The 8
without that name are R1–R3, R10, R11 and their neighbours in the fragment
itself, which have no reason to name their own work item.

Read: I spot-checked seven notes chosen at random against the code they
describe.

- **0.15.1 G1:** the note says `main`'s `--preflight` help now names the ask,
  and the help at `skills/verify/scripts/broad_gate.py:3272` does.
- **0.12.0 and 0.15.4, on `templates/config.md` §*Broad gate*:** each note
  quotes the section's new sentence, and `templates/config.md:169-172`
  carries it.
- **0.10.0 S10, 0.11.5 and 0.12.0 on `seal`:** the 2026-10-02 note says the
  record is composed above the guard and that no `raise` was added. Both are
  true at `:4588-4611`.
- **0.10.0 S12:** the note says the ask's line names a record only where
  the file is on disk. That is `on_disk` at `broad_gate.py:2988`.
- **0.12.0, the one-word rule:** the note says the added comments leave no
  instance anonymous. `bin/test tests/test_one_word_one_meaning.py` exited 0
  (executed).

Every note I checked says what the edit did, and the claim it then calls
true is true.

## Round 1's finding 3 is closed, and keeping the behaviour is right

The text now says that `item_dir` reads the working tree and that the chain
arm reads HEAD. Read, and true:

- `hooks/routing.py#item_dir` (`:355`) filters `declarations(root)`, which
  walks the working tree with `os.listdir` (`:290-333`). Untracked files are
  included.
- The chain arm's `declared_for_this_branch` keys on the branch and filters
  `tracked_declarations` (`skills/code-review/scripts/chain_check.py:1242`,
  called at `:1307`). That function lists `HEAD` with `git ls-tree` whatever
  `--worktree` says.

Keeping the behaviour is right. The ask exists to put `seal`'s refusals in
front of the suite, and `seal` reads the records on disk. An ask keyed on HEAD
would read a different declaration from the one the commit gate reads. The
sealer is also handed `--record <item>` explicitly, so the HEAD reading does
not decide what is sealed either. The comment at `broad_gate.py:2862-2869`,
the module docstring at `:124-131` and the dated correction in `spec.md`
say the same thing in the same terms.

## Round 1's finding 4 is closed

Read:

- `PREFLIGHT_ASKED` (`broad_gate.py:2779`) now reads *asked … of {home},
  found through the one declaration naming {branch}*. It no longer calls a
  record a work item.
- `{home}` is the record where `os.path.isfile` finds it, and the work item's
  directory otherwise (`:2988-2989`). A refused ask names the directory as
  before.
- `PREFLIGHT_NOT_ASKED` (`:2785`) says *either none does or more than one
  does*. `item_dir` returns `""` for both, so the line cannot say which one
  applies, and it does not pretend to.

Executed: the two-declarations case, the settled case and the direct case
each failed at `090cb32f`. When `on_disk` was reduced to
`record is not None`, the direct case failed at its line assertion, and the
settled case still passed, as it should.

## The survivor `bab8dc4a` excused has sound grounds

`docs/commit-review-gate-spec.md:765` reads *the same key the commit gate
reads*. It names the commit gate alone, and the commit gate's `for_branch`
reads `declarations`, the working-tree walk. So the sentence is true, and
the survivor matched it only because of the clause round 1's finding 3
removed. The section is about the review-reminder hook, which this work does
not touch, and the document is ratified policy outside `spec.md`'s scope.

## The merge `f3b18cff` changes nothing this branch says or does

Read, plus two runs:

- The merge brought no change to `round_record.py`, `broad_gate.py`,
  `hooks/routing.py` or this branch's test module. Its code changes are in
  `arm_check.py`, `mutation_check.py`, `session_cost.py` and their tests.
- `skills/verify/SKILL.md` auto-merged. The preflight sentence this branch
  added appears in `git diff 5180b89e f3b18cff` with the same words it has in
  `git diff 821e592d bab8dc4a`. The release side's hunks are in the
  `arm-check` section only.
- In `seal/releases/0.15.1.md` the release side edited N2 alone
  (`git diff -U0 821e592d 5180b89e`). The merged file equals the branch's
  except for N2, and it equals the release's except for G1, N3 and N4. So
  each row came from the side that edited it.
- Executed: `bin/evidence-check .` unscoped exits 0 with 0 drifted, and
  `bin/correction-check --range 821e592d...a0c66d18` exits 0 over 2 merges.
  So the hashes the resolution kept match the merged text, and no
  correction marker was dropped.

## The six new units

All six are at depth 1. I judged each as code, asking whether it is correct
and whether it fails on its defect.

- `hand_edited_last`, `without_the_row`, `with_the_row_twice` and
  `with_an_open_comment` (`tests/test_the_seal_is_taken_once_by_the_sealer.py:4535-4563`)
  are correct. If the row format drifted, the line match would stop removing
  the row. The case would then see `--check` exit 0 and fail, so these
  helpers cannot make the case pass on nothing. The comment opener is
  spelled in two parts, so a record that quotes it stays readable.
- `test_seal_check_refuses_what_the_write_path_refuses` (`:4575`) asserts
  the exit, the write path's own sentence, the absence of a chain check, and
  unchanged bytes. All three ids were red at `090cb32f`, and `open-comment`
  was red under the narrower mutation.
- `test_a_direct_item_preflights_green_and_names_the_work_item_it_asked`
  (`:4821`) asserts that no `broad-gate.md` exists before or after, that the
  line names the directory, and that the file name appears nowhere in stderr.
  It was red at `090cb32f` and red under the `on_disk` mutation.

No unit at depth 2 is needed.

## ⬜ 1 — `spec.md` S1 still counts seven refusals

`seal/specs/1790835051-the-preflight-asks-seals-own-refusals/spec.md:35`.
S1 says `--check` raises *every refusal it raises today — the six
`raise Refused` sites of `seal()` plus `seal_home`'s*. Since `eec243df` the
same check also asks the three refusals raised by callees, and `seal`'s
docstring counts ten. The fix pass added dated corrections to this file for
round 1's findings 2 and 3, and not for this. This is the run's own
paperwork, so it is a correction and not a fix. Nothing machine-reads the
sentence. It closes `answered` with `corrected at <sha>`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's yellow finding 1 is closed — `seal --check` asks `field_index`, `cell` and `hiders_close` above its return, and nothing between the return and `write_record` refuses | `skills/code-review/scripts/round_record.py:4602` | confirmed | Executed: 7 new or changed cases red at `090cb32f`; removing the `hiders_close` call killed the position and open-comment cases; a full `seal` byte-identical to `090cb32f` over five shapes; the write path's refusals identical with and without `--check`. Read: the guard at `:4606`, `write_record` at `:4611` |
| 🟢 | round 1's finding 2 is closed — each of the 48 re-stamped release rows carries a dated note naming #702 | `seal/releases/0.10.0.md` | confirmed | Read: 56 rows rewritten, 48 in release files all naming the work item, 8 in its own fragment; seven notes checked against the code. Executed: `test_one_word_one_meaning.py` exit 0 |
| 🟢 | round 1's finding 3 is closed — the text says `item_dir` reads the working tree and the chain arm reads HEAD, which is true, and the behaviour is right to keep | `skills/verify/scripts/broad_gate.py:2862` | confirmed | Read: `hooks/routing.py:290-370` against `skills/code-review/scripts/chain_check.py:1242` and `:1307` |
| 🟢 | round 1's finding 4 is closed — the ask names a record only where it is on disk, and the not-asked line says none or more than one | `skills/verify/scripts/broad_gate.py:2988` | confirmed | Executed: three cases red at `090cb32f`; the direct case red with `on_disk` reduced to `record is not None` |
| 🟢 | The survivor `bab8dc4a` excused is true as it stands | `docs/commit-review-gate-spec.md:765` | confirmed | Read: it names the commit gate alone, whose `for_branch` reads the working tree |
| 🟢 | The merge `f3b18cff` changes nothing this branch's code or documents do or say | `seal/releases/0.15.1.md` | confirmed | Read: rows G1, N3 and N4 from the branch, N2 from the release; the `SKILL.md` preflight sentence intact. Executed: `evidence-check .` 0 drifted; `correction-check` exit 0 over 2 merges |
| 🟢 | The six new units are correct and each case fails on its defect | `tests/test_the_seal_is_taken_once_by_the_sealer.py:4535` | confirmed | Executed: red at `090cb32f` and under two mutations; the `cell` refusal is pinned by name only, and the preflight's value cannot reach it |
| ⬜ 1 | `spec.md` S1 counts seven refusals where `--check` now asks ten | `seal/specs/1790835051-the-preflight-asks-seals-own-refusals/spec.md:35` | open | Read. Paperwork; a correction closing `answered` with `corrected at <sha>`, outside `Needs a fix` |

## Executed probes

| What was run | Result |
|---|---|
| `bin/evidence-check .`, unscoped, at `a0c66d18` | exit 0; 3451 ok, 0 drifted, 0 broken, 0 malformed, 0 overflow; records: 8 work items read, 0 refused, 0 drifted |
| `bin/correction-check --range 821e592d...a0c66d18 --root .` | exit 0; 2 merge commits examined, no correction marker dropped |
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -k "write_path or check_returns or seal_check or preflight or direct_item or two_declarations or detached or undeclared or settled_item_preflights"` at the target | exit 0; 27 passed |
| The seven new or changed cases (`-k "write_path_refuses or check_returns or direct_item_preflights or settled_item_preflights or two_declarations"`) with `090cb32f`'s `round_record.py` and `broad_gate.py` copied over the clone's | exit 1; 7 failed; files restored by `git checkout` |
| The same seven with two mutations: the `hiders_close` call above the return removed, and `on_disk` reduced to `record is not None` | exit 1; 3 failed (the position case, `open-comment`, the direct case), 4 passed; files restored |
| A one-run probe file in the clone's tests (deleted after): a full `seal` by `090cb32f`'s tree and by the target's over copies of five shapes (settled, settled sealed twice, direct, direct sealed twice, capped) | first run exit 1 only on the temporary payload name `run_check` prints; rerun with that name normalised: exit 0, 5 passed, with the same exit, the same output and the same record bytes |
| The same probe: the three hand-edited shapes sealed in full by both trees and with `--check` by the target, and a pipe in `--broad-gate` | exit 0, 4 passed: exit 2 everywhere, identical text, record bytes unchanged, `--check`'s output equal to the full run's |
| `bin/test tests/test_one_word_one_meaning.py` | exit 0; 18 passed |
| The broad gate (full suite, repository-wide lint, typecheck) over this branch | not yet: it is the sealer's, and it comes due once this round's record is written |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

```diff
--- a/seal/specs/1790835051-the-preflight-asks-seals-own-refusals/spec.md
+++ b/seal/specs/1790835051-the-preflight-asks-seals-own-refusals/spec.md
@@ -40,2 +40,6 @@
   verify-and-exit flag in this repository takes (`seal.py mode --check`,
   `fold_ledger.py --check`, `claude_block.py --check`).
+  **Corrected 2026-10-02 by round 2 (⬜ 1):** the refusals are ten, not
+  seven. The write path's callees `field_index`, `cell` and `hiders_close`
+  refuse too, and `--check` asks them since round 1's fix pass
+  (`eec243df`), which composes the record above its return.
```

Needs a fix: no
Loses a record or crashes: no

The run ends here: nothing this round found needs a fix, and ⬜ 1 is a
correction to this work item's own `spec.md`. What comes due is the sealer's
spawn.

## Proof block

Files opened in the clone at `a0c66d18`:

- `seal/specs/1790835051-the-preflight-asks-seals-own-refusals/rounds/round-1.md`
- `seal/specs/1790835051-the-preflight-asks-seals-own-refusals/rounds/round-1-report.md` (head)
- `seal/specs/1790835051-the-preflight-asks-seals-own-refusals/spec.md` (S1, §Out)
- `seal/specs/1790835051-the-preflight-asks-seals-own-refusals/survivors.md`
- `seal/ledger/1790835051-the-preflight-asks-seals-own-refusals.md` (R3, R10, R11)
- `skills/code-review/scripts/round_record.py` (`seal`, `write_record`, `kept_broad_gate`, `new_broad_gate_file`, `field_index`, `cell`, `hiders_close`, `run_check`)
- `skills/verify/scripts/broad_gate.py` (module docstring, `sealed_record`, `seal_record`, the ask in `gate`, `main`'s help)
- `skills/code-review/scripts/chain_check.py` (`tracked_declarations`, `declared_for_this_branch`)
- `hooks/routing.py` (`declarations`, `for_branch`, `item_dir`)
- `tests/test_the_seal_is_taken_once_by_the_sealer.py` (the fixtures and the cases named above)
- `docs/commit-review-gate-spec.md:755-770`
- `docs/review-chain-spec.md` §*The last round verifies*, and the correction paragraph
- `templates/config.md:165-178`
- the diffs `090cb32f..bab8dc4a`, `bab8dc4a..f3b18cff`, `5180b89e..f3b18cff` and `821e592d..5180b89e` on the files named above, and every rewritten row of `seal/releases/` in the fix range
