# 1788632199-the-repository-ships-no-way-to-run-its-own-suite — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 4eed667 |
| Ran by | <the spawning session fills this row> |

## What this phase was asked

The closing set, and one of its four files closes a red check: `overview.md`
first, then re-run `tests/test_chain_hooks_hardening.py`, where
`test_every_spec_directory_that_reached_the_ladder_has_an_overview` was the
one failure of 46. Two divergence rows were named as real rather than left to
judgment — the issue's premise, with both sides quoted, and the placement's
false reason, with what phase 1 claimed set against what `ls -a` shows. The
`## Not verified` table to name whoever answers `bin/test.cmd` on Windows
honestly, given no Windows here and no CI job that executes a `.cmd`.

Then the ledger fragment at `seal/ledger/<work-item-id>.md`, not appended to
`seal/ledger.md`, with `run_tests.py#FLOOR` and `CONTRIBUTING.md`'s section
named by phase 2 as rows worth writing and the rest left to judgment — the two
venv tools' differing `.gitignore` behaviour and the correction offered as
candidates, under the rule that **a claim not verified by opening the code gets
no row**. Both `evidence-check` forms to be run and read: the scoped
`--reverify --ledger <fragment>`, which keeps a re-stamp off a row somebody
else has to judge, and the unscoped `evidence_check.py .`, which is the only
form that shows what this branch's own edits drifted in `seal/ledger.md`. One
pre-existing drift was handed over as not this branch's:
`templates/config.md#"# Repository config"`.

Then the changelog fragment, its shape and heading level to be taken from
`seal/specs/1788613827-…/changelog.md` rather than invented, and `docs/flow.md`'s
`#156` box — that box and nothing else, since `#155` and `#169` are not this
branch's and `#170`'s is already ticked.

## What this phase found

**Two of the three drifts in `seal/ledger.md` were this branch's, and the
handoff had predicted one drift.** The orchestrator measured one at the base,
`templates/config.md`, and the unscoped read here returned three: the two
extra are `docs/review-handoff-protocol.md#"## The handoff before round 1"`
and `agents/smith.md#"## Phases"`, both drifted by phase 2's edits, and the
second is cited by two rows rather than one. All three were re-read and
re-stamped with a note; every claim held. **This is what the unscoped form
buys and the scoped form cannot**: three rows in a ledger this work item does
not own were falsified by a document edit two phases back, and nothing else in
the run would have surfaced them.

The re-stamp was done without letting `--reverify` touch the pre-existing
drift, which the scoped form cannot narrow to inside one file: `seal/ledger.md`
was copied to a scratch path, `--reverify --ledger <the copy>` computed the new
hashes there, and the three rows were then edited by hand in the real file. The
copy is what kept `templates/config.md`'s row from being re-stamped by a
session that never read it.

**`agents/smith.md#"## Phases"`'s own note had already priced this.** It says
the anchor is the whole numbered procedure, so the row drifts on any edit to
it, and that the minor-level narrowing is the escape hatch `templates/ledger.md`
reserves for a unit *measured* to drift on unrelated edits — one release not
being that measurement — with the instruction to *re-read the claim when it
drifts and re-stamp*. That is exactly what happened, at a cost of one read.
The measurement is now two releases rather than one, and it is recorded in the
row.

**Two facts were measured here rather than inherited from prose**, under §5.
Both venv tools: **[executed]** `uv venv --python ">=3.12"` (uv 0.10.4) writes
`.venv/.gitignore` containing `*`, and `python3.12 -m venv` (3.12.7) writes no
`.gitignore` at all. And the standard-library fallback end to end, with `uv`
stripped from `PATH`: `build()` announced `python -m venv`, returned `None`,
`has_pytest` came back `True`, and the ignore read `'*\n'`. Phase 1 had
executed the first pair and the missing-tool sentence, but the fallback's
*successful* branch had only ever been exercised against fakes, so the row
claiming the runner writes the ignore whichever strategy built the directory
rested on a path nothing had run. It runs.

**The issue's premise is wrong in a narrower place than `spec.md` says, and
the narrower reading is the one the overview records.** #156's literal
sentence — *"There is no `pyproject.toml`, no dev-requirements file, and
nothing in either README that names a command"* — is **true**, because
`CONTRIBUTING.md` is not a README. What fails against the tree is the headline,
*"The repository ships no way to run its own suite"*, and the third of its four
proposed answers, *"A line in `CONTRIBUTING.md` naming the command, whatever it
is"*, which asks for a line that was already at `dcbf404`. Quoting the wrong
sentence would have made the divergence row itself falsifiable, which is what
the row exists to prevent.

**Six rows, and the sixth is a reason rather than a behaviour.** Five state
something the code does; R6 states why the runner sits where it does. It earns
a row because the repair a false reason invites is not "fix the sentence" — a
reader who finds a placement justified by a fact they can disprove moves the
runner, and that is the expensive mistake. The row is the only place the true
reason and the falsified one sit together.

**The four candidate rows phase 2 did not name were tested against the
opening rule and three survived.** What was dropped: a row for `bin/test`'s
argument pass-through and root resolution, which is the sibling shape five
existing `bin/` pairs already carry and `test_every_posix_wrapper_resolves_its_own_directory`
pins across all six at once — a row would have been an inventory of the diff
rather than a judgment a later tidy-up would undo.

**What ran, and what it said.** All through `./bin/test` from the worktree —
this work item's own product, used to verify itself.

```
./bin/test tests/test_chain_hooks_hardening.py -q
  before overview.md:  1 failed, 45 passed in 4.29s
                       test_every_spec_directory_that_reached_the_ladder_has_an_overview
  after:               46 passed in 4.29s

./bin/test <the nine modules> -q
  335 passed, 1 warning in 18.44s
  the warning is tests/test_a_row_points_by_content.py:763, an invalid escape
  sequence in a docstring that predates this branch

./bin/test tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q
  37 passed in 0.67s, then 37 passed in 0.41s
  1.01 s and 0.66 s wall — two warm calls, the reuse this work item is about

evidence_check.py . --reverify --ledger seal/ledger/<this work item>.md
  31 rows re-verified, 0 broken; re-run afterwards: 0 rows re-verified

evidence_check.py .            (unscoped, exit 1 — drift warns, it does not fail)
  seal/ledger.md                       565 ok · 1 drifted · 0 broken
    DRIFTED templates/config.md#"# Repository config"   not this branch's, left
  seal/ledger/1788613827-…                33 ok · 0 drifted · 0 broken
  seal/ledger/1788632199-…                29 ok · 0 drifted · 0 broken
  total: 627 ok · 1 drifted · 0 broken · 0 external · 0 old-format
```

The fragment reads 29 where `--reverify` counted 31 because two coordinates
are cited twice — `run_tests.py#build` by R2 and R3, and
`CONTRIBUTING.md#"## Running the checks"` by R3 and R4.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none — the phase adds four files (three in `4eed667`, this record in the commit after it), ticks one checkbox, and re-stamps three rows in `seal/ledger.md` without removing any | none |
