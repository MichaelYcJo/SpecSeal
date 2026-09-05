# 1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | d6b4fed |
| Ran by | specseal:smith on fable-5.1 |

The `Ran by` value is transcribed the way phases 1 and 2's were: the agent
is the definition this segment was spawned from, and the model is what the
harness's own system prompt states. Neither half is the segment's idea of
what it is.

## What this phase was asked

Build phase 3 of `plan.md` and only phase 3, on branch
`feat/161-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records`,
with routing answered and the question batch closed — ask nobody anything.

1. `deferred <home>` closes a finding: `deferred` in `CLOSED_WORDS` and not
   in `FIX_WORDS`, the import-time assertion kept; `deferred #170`,
   `**deferred** #170` and `deferred seal/follow-up.md` read as closed, and
   bare `deferred` stays OPEN. `no fixes to check` beside it is honest.
2. The floor's reopening is one: in `stopping_floor`, after a record whose
   floor row is `no`, walk `later` and count the records that `wrote_fixes`;
   at two, refuse, naming the second record by file and the floor record it
   follows, and saying the exit (`capped` — open findings become issues,
   verdicts read `deferred #N`, `Fixes checked by` reads `no fixes to
   check`, the pull request says `chain: capped`). Behind
   `REOPEN_FROM = 1788597030` in the shape of the six cutoffs; earlier items
   print. The existing `counted > 1` walk kept exactly as it is, and the
   docstring telling the two walks apart in one table.
3. `docs/review-chain-spec.md`: the subsection `##### The reopening — one,
   and then the run is capped` after `Needs a fix` and before the depth,
   stating the rule, what the refusal reads, the cutoff, the failure
   direction (blocks more, and what it lets through), the exit and the
   vocabulary; `deferred <home>` where the spec lists the closing words; a
   one-line `--worktree` mention where CI's `HEAD` read is described. The
   other carriers of the count rule are phase 4's (split into 4a, the
   owners, and 4b, the links, on 2026-09-05 — `plan.md`).
4. `tests/test_the_reopening_is_one.py`, mirroring the floor test and the
   stops-at-the-last-finding test: each refusal seen red at a named fixture
   before the code exists; the two-record run kept green; the three-record
   run refused naming the file; the cutoff at the boundary second;
   `deferred #170` closed and bare `deferred` open through the ready
   pull-request path; the capped run's legal end; this repository's own
   records under the new arm. One case in
   `tests/test_the_fixes_close_the_record.py`: a table of only `deferred #N`
   rows ticks `Pass`. Every new spec sentence pinned and seen red.

Coordinates handed over and opened: `chain_check.py` `CLOSED_WORDS`,
`FIX_WORDS`, `EMPHASIS`, `VOCAB`, `verdict_of`, `pass_checked`,
`checked_by`, `closed_with_a_fix`, `run_reopened`, `wrote_fixes`,
`stopping_floor`, `item_began`, the seven cutoff constants and `NOT_YET`,
`check_round`, `main`; `docs/review-chain-spec.md:32-182`, `:526-637`,
`:720-1010`; `templates/sdd-round.md:139-172`, `:196-215`;
`round_record.py` `verdict_words`, `terminal_value`, the `FIXES` constants
and `close`; `tests/conftest.py` `declare_routing`, `rounds_dir`; the two
sibling test files and `test_the_fixes_close_the_record.py` whole. The line
numbers the prompt named for `chain_check.py` had moved by phases 1 and 2,
as it said; every name resolved to the unit it was said to name.

## What this phase found

**Bare `deferred` needs a value in neither set, and `verdict_of` had none
to give.** Every unreadable verdict comes back as the normalized cell, which
counts open because it is in neither set. The bare word IS the closing word,
so returning the cell would count it closed. `HOME_WORDS = {DEFERRED}` names
the closing words that close nothing without a home, and `verdict_of` hands
the bare word back as `deferred (no home)` — in neither set, and still saying
what the cell said, so `open_blocking`'s message reads *this 🔴 row reads
`deferred (no home)`*. That is a line a person reads and is pinned.
Separators after the word count as nothing: `deferred —` is bare.

**The reopening walk counts `wrote_fixes` and never stops, and one fixture
tells it from the count.** A reopening record that answers the floor `yes`
is not a floor record, so the count never starts from it and stops at it
from the record before; only the reopening walk reaches the third record.
`test_the_records_between_do_not_matter` is that sequence, and every
refusal case asserts the count's own phrase is absent from the output, so
the case cannot be satisfied by the older walk. Reading `run_reopened`
instead of `wrote_fixes` is caught by the capped run's legal end, whose last
record answers `Needs a fix: yes` over deferrals and wrote nothing.

**The capped end's `Fixes checked by` is written by nobody.** `close` over a
table of only deferrals ticks `Pass` and leaves the cell at `nobody — the
fixes are not yet written`, as phase 2 decided, and the check it runs then
refuses `Pass` beside `nobody` on the last record — exit 1, with a message
that names the verifying round as the way out. A capped run has no verifying
round; its exit is `no fixes to check`, which `new` derives when every
verdict closed without a fix word and `close` does not. Probed once and
deleted (§7). `questions.md` A6 states the assumption and the two ways to
close it; nothing was built, because the plan names `close`'s cell as *left
as it stands* and a walk or a derivation is mechanism this phase was not
given.

**`templates/config.md`'s exclusion list is derived from `CLOSED_WORDS` by
a pin, so a verdict word is a config-template edit too.**
`test_the_exclusion_list_holds_every_string_a_checker_matches` went red on
`deferred` at the module-boundary run, and the list now names *the
`deferred` in `deferred <home>`*. The prompt named two files for this
phase; this is the third, and it is the pin doing what it was written for.

**The floor test's subsection bounds had to move.** Its `SUBSECTIONS` table
closed the `Needs a fix` slice at the depth heading, and the new subsection
sits between them; left alone, a claim about the `Needs a fix` table could
have been answered by the reopening's. The `needs a fix` entry now closes at
the new heading and `the reopening` has an entry of its own, seen red with
the `no timestamp prefix` phrase stashed from the new table alone.

**Seen red, and how.** Thirty of the thirty-seven new cases were red before
the code and the sentences existed — the walk's refusals, the cutoff, the
closed readings of `deferred <home>`, the capped end, the `close` tick, and
every spec pin. Seven passed before the code existed: the two-record run
(green by design, and kept), the four bare-`deferred` readings and the
ready-pull-request refusal of the bare word (open before the word existed
and open after), and the own-records case. The bare readings and the
refusal were shown red afterwards by mutation, the home guard removed. Mutation loop over
every unit this phase added: nine mutations, nine killed — the home guard
removed, the walk refusing at three, the walk reading `Needs a fix`, the
cutoff inclusive the wrong way, the cutoff a second off, the message naming
the first record, the message naming no exit, `deferred` left out of the
set, the grandfathered notice made an error. Restored from a kept copy each
time, `tests/__pycache__` cleared between. Every unit this phase added is
depth 1.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
