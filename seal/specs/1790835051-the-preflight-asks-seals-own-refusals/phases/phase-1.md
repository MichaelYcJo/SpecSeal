# 1790835051-the-preflight-asks-seals-own-refusals — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 9b9220ff |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`round_record.py seal --check`: the flag in `main`, the early `return 0`
after the ancestry loop with its one line, the module header and `seal`'s
docstring. S1's four refusing cases and S2's three passing cases in
`tests/test_the_seal_is_taken_once_by_the_sealer.py`, each seen red first,
and the structural case holding the `--check` return as the last statement
before `kept_broad_gate`. Q1's wording for the success line is this phase's.

## What this phase found

**The frame holds for this phase.** Every coordinate `plan.md` §*Technical
context* names for `seal` was opened at `e83db346` and stands: `seal` at the
line it gives, the six `raise Refused` sites in the order it gives, the
parser at `main`, and `seal_home`'s refusal for a chain declaration with an
empty `rounds/`.

**Q1 is answered (a) for this phase.** The two lines are constants beside
`seal`, `CHECKED` and `CHECKED_NO_ROUND`, and S2 reads them off the module and
compares stdout with the formatted line as the whole output. Both begin
`round-record: checked`. The `broad-gate.md` home has its own line because
`--check` reads no round record there and asking it is still worth one: the
two SHA refusals are asked for that home too.

**The header had no paragraph about `seal` to amend.** The module docstring
describes `new` and `close` and never names the third subcommand. The
amendment went into the one sentence the flag makes false: the exit codes,
where 0 used to be the chain check's alone. `seal`'s own docstring carries
the full description, beside the refusal count it leaves unchanged.

**S1 and S2 are parametrized over fixture builders**, four and three, rather
than seven functions. Each builder returns the file whose bytes must not move,
which is the absent `broad-gate.md` for the two no-round shapes, so the
no-write assertion has one spelling for both homes.

**Red, as shown.** Against `e83db346` all eight cases were red: the seven
behavioural ones on `unrecognized arguments: --check` (argparse exit 2), and
the structural one on the statement before `kept_broad_gate` being the
ancestry `for` loop. After the commit, two mutations ran through
`bin/mutation-check`, each red: the guard disabled (`if False and
args.check`) failed all three S2 cases on the written cell, and the success
line's prefix replaced by `round-record: sealed` failed the two record-home
S2 cases.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
