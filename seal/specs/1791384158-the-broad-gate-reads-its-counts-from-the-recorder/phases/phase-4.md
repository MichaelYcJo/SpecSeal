# 1791384158-the-broad-gate-reads-its-counts-from-the-recorder — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 22c40aaf |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

`plan.md` phase 4: `publish-release.yml`'s suite step sets the recorder's
four variables and drops `--junitxml`; `release_seal.py` loads
`broad_gate.py` through `module`, reads the record under `SUITE_RECORDS` with
`SUITE_KEY`, refuses a record with no keyed session, an unread line, an
unended session, or a `failed` or `error` count, and the JUnit reader goes;
`docs/release-checklist.md`'s by-hand lines name the new variables. Case
S12, and `DRY_RUN=1 python3 .github/scripts/release_seal.py` executed once
over a record a local `bin/test` run wrote with the four variables set.

## What this phase found

**The dry run, executed.** `bin/test -q` over this phase's two modules with
`PYTHONPATH`, `PYTEST_ADDOPTS`, `SPECSEAL_RECORD_DIR` and
`SPECSEAL_RECORD_KEY` set printed `72 passed in 2.73s`, exit 0. Then
`DRY_RUN=1` with `TAG=v0.20.0`, `REPO` this repository, `SUITE_RECORDS` that
directory and `SUITE_KEY` that key, exit 0, printed:

```
SEALED   v0.20.0
tag      5623d728
         main
PRs      8 merged
issues   14 closed
suite    72 passed, 0 skipped
items    7 . 22 rounds
capped   4 of 7
deferred 8 issues
drew …/seal.png from release-seal.svg with rsvg-convert
no seal: the glance table is not in the note exactly once …
```

The `suite` row is the record's, and equals pytest's own line. The run
stopped at the glance table because 0.20.0's note already carries its seal,
which is the refusal that protects a published note; nothing was uploaded
or edited. Run again with a key no session carries, the line read `no seal:
the suite's counts cannot be read: no record under … carries the key
seal-other` with its `::warning::`. `gh pr list` and `gh release view` were
called read-only; the scratch directory was removed afterwards.

**The key is the run's own.** The suite step's key is `seal-${{
github.run_id }}`, written once in each of the two steps, and the drawing
step's `SUITE_KEY` and `SUITE_RECORDS` are held equal to the suite step's
`SPECSEAL_RECORD_KEY` and `SPECSEAL_RECORD_DIR` by the workflow case. The
directory is made in the step (`mkdir -p`), because the recorder writes no
record into a directory that is not there and the seal would then say `no
seal` for want of a directory.

**`test_the_publishing_workflow_installs_the_pins_the_runner_holds` was not
touched**, and passes: the install line is unchanged, and no new package is
needed — the recorder imports nothing but pytest.

**Two guards survived the first mutants.** An empty `SUITE_RECORDS` or
`SUITE_KEY` would fall to the no-session refusal anyway, so removing either
guard kept the case red for the wrong reason; each refusal now names its own
reason and the case matches it (22c40aaf).

Shown red: at 5623d728's `release_seal.py` and workflow, the re-aimed cases
failed, 25 of 29 — every `wired` case, because the old script read
`SUITE_XML`, which no case sets now, and the two workflow cases. Mutation:
each of the seven refusal conditions dropped, the skipped count fixed at 0,
and the key read from the old variable were each red through
`bin/mutation-check`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the JUnit reader `suite_counts(path)` and its `xml.etree` import | `suite_counts(directory, key)` over `broad_gate.read_record` |
| `--junitxml` in the `seal` job's suite step, and `SUITE_XML` | the recorder's four variables in the suite step; `SUITE_RECORDS` and `SUITE_KEY` in the drawing step |
| the checklist's *with `TAG`, `REPO` and `SUITE_XML` set* | the by-hand route naming the recorder's variables, `SUITE_RECORDS` and `SUITE_KEY` |
