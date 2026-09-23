# 1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | ee555887 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

#138 at the reader. In `skills/code-review/scripts/chain_check.py`, one
function answering *does this cell say the run reopened* — `True` / `False` /
`None` — used by `stopping_floor`'s own-row read and by `run_reopened`; a bare
`yes` refused on its own record under `NEEDS_FROM`'s grandfathering, in the
floor row's words; the module docstring's `Needs a fix` row naming the
refusal. The `Needs a fix` table in `docs/review-chain-spec.md` and the
comment in `templates/sdd-round.md` saying the same. Cases A1–A4 and A7 in
`tests/test_the_record_is_held_to_the_floor_and_the_depth.py`, each seen red
first. Measure Q1: how many records refused by the new arm exist at or after
`NEEDS_FROM`.

## What this phase found

**The frame holds for this phase.** Every coordinate `plan.md` §*Technical
context* names for #138 was opened at `659b4229` and says what the plan says:
`yes_or_no` returns `("yes", "")` for a bare `yes`, `stopping_floor`'s own-row
read computes only `word_needs`, `run_reopened` returns `word == FLOOR_YES`,
and `NEEDS_FROM == FLOOR_FROM == 1788472135` with the row grandfathered whole
through `needs_excused`.

**Q1, measured (executed, 2026-09-23): zero.** `grep -rn -E
'^\| *Needs a fix *\| *\**yes\**\.? *\|' seal/specs/*/rounds/*.md tests/`
found no file. The 20 live `Needs a fix` cells read `no` (5), `no — <why>`
(3) and `yes — <what>` (12). `git branch -r` lists `main`, `release/v0.14.0`
and `release/v0.15.0` only, and `gh pr list --state open` returns nothing, so
no open branch carries a record the arm would refuse. The default holds: no
cutoff, and the refusal sits under `NEEDS_FROM`'s grandfathering.

**Seven cases seen red at `659b4229` before the fix** (executed;
`bin/test tests/test_the_record_is_held_to_the_floor_and_the_depth.py -q -k
"bare_yes or says_reopened"`):

```
E  AssertionError: chain-check: judged as a ready pull request …   (A1: exit 0)
E  AssertionError: passing in silence would hide the state the row is read for   (A2)
E  AssertionError: chain-check: judged as a ready pull request …   (A3: exit 0)
E  AttributeError: module … has no attribute 'says_reopened'
E  AssertionError: docs/review-chain-spec.md does not say a bare `yes` in `Needs a fix` is refused …
E  AssertionError: templates/sdd-round.md does not say …
E  AssertionError: skills/code-review/scripts/chain_check.py does not say …
```

After the fix: 76 passed in the module (executed). A4's two existing cases
(`test_the_verifying_round_may_reopen_the_run_and_its_fixes_get_a_reader`,
`test_needs_a_fix_takes_a_reason_after_either_answer`) stayed green.
`tests/test_the_run_stops_at_the_last_finding.py`, `tests/test_docs_line_wrap.py`
and `tests/test_a_record_says_why_it_was_written_late.py`: 53 passed
(executed) — the count rule's carriers, the 88-column wrap and the
`Written late` reader that shares the vocabulary are untouched.

**Mutations, one at a time, restored from bytes the script kept** (executed
after the commit above; `git status` clean after each):

| Mutation | Killed by |
|---|---|
| M1 `says_reopened` answers `True` for a bare `yes` (the old reading) | A1, A2, A3 and the unit case — 4 failed |
| M2 `stopping_floor` loses the bare-`yes` branch (falls through to *neither answer*) | A1, A2, A3 — 3 failed |
| M3 `run_reopened` reads the cell through `yes_or_no` alone (the old code) | A3 alone — 1 failed, A1 and A2 green, which is what says A3 pins the walk and not the record's own row |
| M4 `templates/sdd-round.md` loses its sentence | A7 for that carrier — 1 failed |

**One reader, named.** The unit is `chain_check.py#says_reopened`, placed
after `yes_or_no`. Its `None` covers the bare `yes`, the empty cell and a word
outside the vocabulary alike, so the count walk cannot tell them apart — which
is the point: none of the three is a reopening. `stopping_floor` asks
`yes_or_no` a second time only to WORD the refusal (bare `yes` versus *neither
answer*); the answer to the reopening question is asked once.

**The pin phrase for A7 is not the floor's.** `docs/review-chain-spec.md`
already says *`yes` with nothing after it* of the floor row, of `nobody` and
of `unknown`, so a pin over those words would be live for the wrong row
(ledger R12). The three carriers share the sentence *`yes` alone is refused
the way the floor row's is*, which occurs nowhere else in any of them.

**What phase 2 needs to know.** The inline `== chain.FLOOR_YES` the plan
places in `round_record.py#bound_line` is in `round_record.py#floor_and_fixes`,
the helper `bound_line` calls; the ledger rows R3 and R4 anchor on both, so
the re-read reaches both. `says_reopened`'s docstring already names
`floor_and_fixes` as its third reader.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase adds a unit, a branch and three sentences and takes nothing out of the tree | none |
