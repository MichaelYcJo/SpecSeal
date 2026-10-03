# 1790835051-the-preflight-asks-seals-own-refusals — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 569db6af |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The preflight asks: `seal_record(..., check=True)`, the item from
`routing.item_dir(root, branch)`, the `seal` entry in `failures`, the stderr
line for the record asked and for none asked, `PREFLIGHT_TAIL`, and the
module docstring. S3, S4, S5, S6 and S8 in the sealer module, each red
against phase 1's tree, then red under the ask dropped and under `--check`
dropped from the argv. The ask's wall clock measured once (Q3). Q2's fixture
for S5 and Q1's wording for the gate's lines are this phase's.

## What this phase found

**`seal_record` keeps its `(code, text)` return.** The first build returned
the `Check` so the failure form could quote it, and
`test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed` went red: it
stubs `seal_record` in process with a `(code, text)` tuple, and S10 says that
case stays green unchanged. So the return is unchanged, `check` is the only
new parameter, and the preflight builds the `Check` the failure form needs
from the code, the text and `<keep>/seal.txt` — the path `run` keeps a check
named `seal` at. That path is spelled twice, once in `run` and once at the
ask; the docstring of `seal_record` names the rule.

**The routing reader is loaded with the gate's own `load`, before any arm
runs.** `plan.md` offered `round_record`'s loader or a direct load. The gate's
`load` raises the gate's `Refused`, so a copy of the plugin missing
`hooks/routing.py` is exit 2 with nothing run, and resolving the item before
the arms is what makes that true. `hooks/routing.py` puts its own directory on
`sys.path` before it imports `optin` and `blocks`, so no loader has to arrange
that. The constant is `ROUTING`, beside `RECORD`.

**The stderr line names the record only where the ask passed.** Where `seal
--check` exited 0, `sealed_record` names the record it read, and its
docstring now says it is asked under a preflight too, still only after exit
0. Where it refused, the line names the work item directory: `seal_home` may
be the refusal, and the failure form already quotes `seal`'s sentence. Q1 is
answered (a): `PREFLIGHT_ASKED` with `ASKED_PASSED` or `ASKED_REFUSED`,
`PREFLIGHT_NOT_ASKED`, and `PREFLIGHT_DETACHED`, each read by its case off the
module.

**`PREFLIGHT_TAIL` says what every run did, not what an asked one did.** The
spec's wording was *the record arms and `seal`'s refusals*. On an undeclared
branch nothing is asked, and that tail would be false on every such run. The
tail now reads *the record arms, and `seal`'s refusals where a work item is
declared for the branch*, which is true either way. S6 pins the whole first
line against `head + PREFLIGHT_TAIL`.

**A detached HEAD has its own line and its own case.** S8 named none and two
declarations. A detached HEAD reaches the same skip through `branch_name`
returning None, and *no single work item declares a detached HEAD* is not a
sentence anyone can act on, so it prints `PREFLIGHT_DETACHED`. The case
declares the item and gives it an unchecked `Pass`, so an ask that ran
anyway is a `seal.txt` and a failing run.

**Two declarations do not fail at `seal`, and the run is not exit 0.** S8
said *the same line and exit* for two declarations. The line is the same and
no `seal.txt` is written. The case asserts that `seal` is not among the
failures and leaves the exit to the chain arm, whose own handling of the pair
is not this work's.

**Q2 is answered (a), with one step the plan did not name.** `new` accepted
a `--target` on a side branch cut from HEAD. But `generate` commits the
record, which moves HEAD past the commit the target descends from. So the
case runs `git reset --soft HEAD~1` after it: the record stays in the work
tree, where `seal --check` reads it, and HEAD is again the commit the target
descends from.

**The other documents that said what the preflight runs were enumerated.**
The `--preflight` help text, the comment above the preflight constants, and
`PREFLIGHT_RECORD`'s closing clause each said *the record arms alone*. All
three now name the ask (contract §12). The module docstring's sentence *runs
no `round_record.py seal`* became false and was removed. The new paragraph
after it says what is asked instead.

**Q3, measured once on 2026-10-01 at 16:03 KST, Apple M3 Pro.** On the
sealer's fixture with a settled item, three preflights with the ask took
9.97, 9.23 and 8.42 s; the same tree with the branch renamed, so nothing is
asked, took 8.10, 8.17 and 8.38 s. The medians are 9.23 s against 8.17 s, so
the ask added about 1 s. `seal --check` alone took 0.72 s on the fixture and
0.57 s on this repository's own work item. This machine was slower than
#638's measurement: the fixture preflight took 8 s here against #638's 1.57 s
on the same fixture shape, so the absolute numbers are this moment's. The
difference is the reading. On this branch today `seal --check` refuses:
`routing.md` declares the chain and `rounds/` is empty. That is the expected
answer before round 1, because the preflight is the step after the rounds
settle.

**Red, as shown.** Against phase 1's gate, S3, S4 and S5 exited 0, S6 had no
`seal.txt`, and both S8 cases met no line. The detached-HEAD case was written
after the build and shown red by mutation C below. Four mutations ran through
`bin/mutation-check` after the commit. A, the ask dropped (`if False and
args.preflight and asked`), turned S3 to S6 red. B, `--check` dropped from
the argv, turned S3 to S6 red: each asserts `--check` in `seal.txt`'s command
line, and S6 also on the written cell. C, the not-asked line dropped
(`elif False:`), turned all three not-asked cases red. D, the `seal` failure
entry replaced by `pass`, turned S3, S4 and S5 red: each preflight printed
`PREFLIGHT PASSED` over a `seal --check` that had refused. Every mutation
restored `broad_gate.py` to its committed bytes.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The docstring sentence that the preflight *runs no `round_record.py seal`* | the paragraph after it in the same docstring, which says the preflight runs `seal --check` and writes nothing |
