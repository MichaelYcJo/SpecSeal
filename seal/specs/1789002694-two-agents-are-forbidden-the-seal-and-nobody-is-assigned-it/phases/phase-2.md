# 1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `0c04bc3` |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

Build `plan.md`'s row 2 and nothing past it. `skills/verify/scripts/broad_gate.py`
with `bin/broad-gate` and its `.cmd` twin: the `Broad gate` row read from
`seal/config.md` through `hooks/config.py#config_rows` (refused when absent,
exit 2, nothing run), then the repository's command and the four plugin
checks in order — `evidence_check.py --strict .`, `unverified_check.py
--baseline <base> seal/specs/`, `chain_check.py --baseline <base>`,
`survivor_check.py --range <base>...HEAD` with every
`seal/specs/*/survivors.md` as `--exempt` — the scripts resolved relative to
the gate's own file, every exit code read directly, every output kept under
`--keep-output` (default a temp dir) and a failing one's first lines quoted;
the reactive base comparison only when the repository command fails and
names `FAILED tests/x.py::…` lines — `git worktree add <tmp> <base>`, the
runner on those files there, `git worktree remove --force`, each labelled
`new` or `failing on base too`; the stamp on success with the panel rows
`SEALED` · blank · `tree` · `base` · blank · `suite` · `lint clean` · `ledger N
ok . 0 broken` · `chain exit 0` · blank · `rounds N` (only with `--record`);
`NOT SEALED` on failure. `round_record.py seal`: a third subparser setting
the LAST record's `Broad gate` cell alone, refusing while `Needs a fix` reads
`yes`, while `Pass` is unchecked, and for a `--broad-gate` SHA the record's
`Target SHA` descends from, then `chain_check --worktree` as `new` and
`close` do; `broad-gate --record <item>` invokes it on success.
`templates/config.md`'s `Broad gate` section, `skills/config/SKILL.md`'s
fourth row, this repository's row: `bin/test -q && uvx ruff check . && uvx
ruff format --check .` (without `-n auto` — `pytest-xdist` is not installed
by `run_tests.py`, measured). Tests part 2: S1–S4 on fixture repositories
driven from Python (§8), a fixture whose base already fails one test, the
refusal without the row, the subcommand's three refusals with every other
line byte-for-byte untouched; every case seen red first, mutations after.
Then, once, `bin/broad-gate --base origin/release/v0.10.0` on the real
repository, output read and wall clock noted — the command verified as a
command, not the work item's gate.

Mid-phase, the coordinator added two things. One: `close` cannot re-write the
`Broad gate` cell of a record whose fix table has already been applied
(executed on the other work item — refused with *the fix table has a row for
finding 17 (`answered`), which the reviewer already closed … no cell was
written*; the only way through was a fix table with a header and no rows), so
`seal`'s docstring names that as the failure it removes, `seal` takes neither
`--fixes` nor `--range`, and a case pins `seal` on a record whose verdicts are
all closed. Two: a row for phase 4 — #330, below.

One fact came `unverified` with this phase as its answerer: whether the
plugin checks' exit codes distinguish *nothing compared* (2) from *failed*
(1) uniformly.

## What this phase found

**The exit codes are not uniform, and the gate does not need them to be.**
Measured by reading each `main`: `unverified_check.py`, `chain_check.py` and
`survivor_check.py` return 2 for *nothing was compared* (no repository, a
base that does not resolve, no `overview.md` under the path, an exemption
file that will not parse) and 1 for a finding; `evidence_check.py` returns 2
for a BROKEN or old-format row, for a refused record stamp, and — under
`--strict` — for drift, with 1 reserved for drift without `--strict`. So a 2
from the ledger check is a failure and a 2 from the other three is a refusal.
The gate reads every non-zero as *not sealed* and prints the check's name,
its `exit N` and its first lines, so a reader sees which of the two it was in
the quoted text; the panel's `chain exit 0` row prints only when every check
exited 0, which is the one state all four spell the same way.

**The gate runs `chain_check.py` judged as a DRAFT pull request, on
purpose.** The gate runs before `seal` writes the cell, so at that moment the
last record honestly reads `not yet` — and `chain_check.broad_gate` judged as
READY fails exactly that cell as the run that never happened (measured on the
`--record` fixture: exit 1, *`Broad gate` is `not yet` on the last round
record, and this is a ready pull request*). `draft_env` writes a draft
payload into the output directory and points `GITHUB_EVENT_PATH` at it unless
the environment already carries one, which is the shape
`round_record.run_check` already uses for a record being generated. Inside a
workflow the payload GitHub wrote is left alone.

**A settled fixture is round 1 → fix → `close` → round 2, not round 1 → round
2.** The first shape of the S4 fixture generated two records and no fix, and
`chain_check` refused it: round 1's `Fixes checked by` named `round-2` while
its `Contract changes` still read *not yet written*. The fixture now applies
a fix table with `close` between the rounds, which is also exactly the state
the coordinator's fact describes — every verdict closed, `close` refusing a
table — so the S4 case pins `seal` where `close` cannot go.

**The base comparison re-runs what stands before the row's first `&&`.** The
row is one shell line and nothing in it says which part is the suite runner;
every row this plugin has seen puts it first. `first_command` splits on the
first `&&` and appends the failing files, shell-quoted. `templates/config.md`
and the config skill say to put the runner first for this reason. A file the
base does not carry cannot fail there, so it reads `new` — measured: the real
run's failing file is one the base has, and the scratch worktree's `bin/test`
built its own `.venv` with `uv` in about ten seconds out of the run's 367,
because `run_tests.py` resolves the root relative to the worktree's own copy.

**`--record`'s success is the checks green AND the cell written.** A refusal
from `seal` — the rounds have not settled — is exit 2 and no stamp, and the
case that pins it runs the gate on an item whose last record reads `Needs a
fix: yes`. The alternative, stamp first and report the refusal after, prints
*sealed* over a record that says the run came too early.

**The real run, once, at `0c04bc3` against `origin/release/v0.10.0`: `NOT
SEALED`, exit 1, 367 seconds wall clock, 354 of them the suite.** Two
failures, both true and neither this phase's to fix:

- `suite` — `1 failed, 3084 passed, 2 skipped`;
  `tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`,
  labelled `new` by the comparison (the base has no such directory). This
  work item has no `overview.md` yet; `plan.md` writes it in phase 4.
- `ledger` — exit 2 under `--strict`: three `seal/ledger.md` rows DRIFTED,
  `templates/config.md#"# Repository config"`, `skills/config/SKILL.md#"##
  Procedure"`, `skills/code-review/scripts/round_record.py#where` — every
  one an anchor this phase edited. **For phase 4**: re-read each claim and
  run `evidence-check --reverify` over them; the real repository cannot seal
  until the rows stand, and phase 4's Verified-by already names the command.

`unverified`, `chain` (as a draft: the notice that this item's `rounds/` is
empty) and `survivors` (`no removed wording is still standing`; one `not
yours` line for #328's whole-range row, which this range does not reach)
exited 0. Every output is a file, and the failure form named each one.

**Seen red, then mutated.** All fourteen part-2 cases ran with
`broad_gate.py` moved away (9 red among the gate cases) and with the `seal`
subcommand's registration removed (5 red), then thirteen mutation arms each
broke one unit and ran its case: a missing row defaulting to `true`; every
exit code read as 0; the base comparison saying `new` for everything; the
failure form drawing the disc; the `rounds` row dropped; a refused `seal`
still stamping; the ledger check run before the suite; the exit code not
kept with the output; `seal` ignoring `Needs a fix`, an unchecked `Pass`, a
premature SHA; `seal` writing a second cell; `seal` accepting a cell with no
SHA. Every arm red; both files restored from bytes held by the script and
sha256-compared after each arm; `tests/__pycache__` cleared between arms.
`tests/test_the_settings_have_a_front_door.py` was seen red against the
skill's *print all four* before its pinned clause and `ROWS` were re-pointed.

**For phase 3.** The sealer's command is `broad-gate --base <base> --record
<item>`; its stdout is a pipe, so the twin prints. The definition should say
that with `--record` a refusal from the record is exit 2 and not a seal, and
that the failure form carries `new` / `failing on base too` per file as words
the sealer reports and does not act on.

**For phase 4 — #330, opened by the owner during this phase, goes in
`docs/flow.md`'s 0.10.1 section.** *Every rule an agent follows is delivered
by mechanism, and every rule the orchestrator follows is a sentence.* The
broad gate is the first instance: an act only the orchestrator performed,
written as sentences in six documents and assembled differently every
session until `broad-gate` existed. #30 closes that instance and is the
template; the other two the issue names are the flow-log posting and the
routing question. `docs/flow.md`'s own rule places it on this branch — a
branch writes a row for any ticket its work opened, in the pull request
that earns it — so phase 4's edit to that file is two rows: #30's box
ticked in 0.10.0, and #330's row added to 0.10.1 in the section's shape
(the number, an em-dash, the symptom in one line, what places it there),
written from the issue rather than copied from the coordinator's line.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
