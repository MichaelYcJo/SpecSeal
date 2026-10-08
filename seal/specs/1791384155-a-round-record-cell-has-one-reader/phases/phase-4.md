# 1791384155-a-round-record-cell-has-one-reader — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 4cdccc2b |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

J4 of `spec.md`: `pull_request_state` gains the `gh` source and prints it;
`--sealing` on `chain_check.main`, reaching the `Broad gate` arm of the last
record; the payload in `run_check` and the generator's own `gh` reader leave
`round_record.py`; the gate's payload writer leaves `broad_gate.py` and the
chain arm passes the flag. `docs/round-record-spec.md` §*`Pass` has to be
checked* third row and its paragraph by replacement. Verified by S7, S8 and
S9 red first, the environment-leak case re-pinned, and the four modules
green.

## What this phase found

- **The suite is the population J4 says now blocks.** It runs with `gh`
  logged out (#510), so every generator run had been judged as a draft by
  the payload `run_check` wrote, and with that gone 176 cases across five
  modules failed on the first run. The suite's pull request is a draft
  instead: `tests/conftest.py` puts a stub `gh` first on PATH that answers
  `pr view --json isDraft` with a draft and passes every other call to the
  `gh` behind it, and `gh_answers` picks `ready` or `unknown` for a case
  about either. Five helpers that meant "no payload, so ready" now say so
  (`unknown`). `CONTRIBUTING.md` §*Running the checks* says it.
- **Windows.** A stub `gh.cmd` is found by `shutil.which` through PATHEXT and
  not by a process call naming `gh`, so the check runs the path `which`
  found. A case pins the argument list.
- **`--sealing` is a wrap, not a parameter of the arm.** `sealing_excuses`
  turns the `Broad gate` arm's errors into notices carrying the flag's
  sentence, for the round-record home and the direct `broad-gate.md` home
  alike, so the arm's own judgment is untouched and nothing else is excused.
- **M1, measured:** no remote (`no git remotes found`), no pull request for
  the branch (`no pull requests found for branch "…"`) and a token GitHub
  refuses (`HTTP 401: Bad credentials`) each exit 1; a draft and a ready pull
  request exit 0 with `{"isDraft":true}` and `{"isDraft":false}`. The stub's
  `unknown` prints the second.
- **W2, decided:** under `--sealing` the runner's payload no longer fails the
  fixture's gate, so the environment-leak case asserts the judgment instead —
  the chain arm's kept output names the runner's payload as its source, where
  the same gate with the variable cleared names `gh`.
- The chain check over the tree reads the same as before except its first
  line, which now names `gh` and what it answered.
- 0.10.0's S7 claimed the gate judges as a draft; it is a `Corrected ·` row
  now, its coordinate on the removed writer retired. #869's fragment carries
  a `Re-read · S7` row that `--reverify` re-stamped; it was put back at its
  earlier hash, since a claim this work made false is not one it re-read.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the generator's `gh` reader of the draft state and the draft payload `run_check` wrote | `chain_check.pull_request_from_gh`, asked by `pull_request_state` |
| the broad gate's draft payload writer for the chain arm | `--sealing`, `chain_check.sealing_excuses` |
| `run_check` in the writers case's expected set | `write_record` alone (S8) |
