# the broad gate hands cmd.exe a forward slash, and a case reaches a live gh (#448, #510) — questions for the planner

<!-- seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/questions.md -->

**No row here needs a person.** Every row has a default that lets the build
go ahead. Two rows are measurements and one belongs to the work.

**Judgments both tickets left open, which the tree answered.** They are listed
so that nobody reopens them, and the grounds for each are in `plan.md`'s
Alternatives table.

- **Which of #448's three candidate directions.** The answer is the rewrite
  of command words for `cmd.exe` (Alternative 3). The deciding fact is that
  `bin/test.cmd` exists so `cmd.exe` can call the runner. Running the row
  under `sh` would bypass that sibling and would alter the meaning of rows
  written in `cmd` syntax, and `templates/config.md` §*Broad gate* already
  describes both shells as the ones that run a row.
- **Whether "nothing ran" gets its own exit code.** It does not
  (Alternative 4). #448's own measurement shows `cmd /c` exiting 1 with a
  localised message, and under `sh` a 127 can come after the tests ran. What
  replaces it is a line in the failure form keyed on the missing pytest
  summary.
- **Whether #510's mechanism is a CI leg, a gate arm, or the suite.** It is
  the suite, through `tests/conftest.py` (Alternatives 5–9). CI is already
  unauthenticated. A gate arm costs a second full run on every seal and puts
  a policy on plugin users' rows.
- **Whether #510 also covers `git` against a remote, `uvx`, and `urllib`.**
  It does not. The class is a credential the developer's machine holds and
  the runner does not, and CI has network. A static read found no case that
  names a network remote (`spec.md` §*Scope*, Out).
- **Where the rewrite lives.** It lives in `run`, not in `gate`. That covers
  both `shell=True` callers, and it leaves `gate` unedited, which five ledger
  rows cite.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does `cmd.exe`, reached through `subprocess.run(..., shell=True)`, run `bin\probe` by resolving it to `bin\probe.cmd` through `PATHEXT`, with exit code and output passed through? The tree cannot answer this because this machine is macOS and no Windows run belongs to this work item. #448's table (`bin\test` exit 0, `bin/test` exit 1) is the ticket's claim, measured on the reporter's machine. | a measurement: scenario A4's executed case on CI's `windows-latest` leg at the pull request | **Yes:** phase 1 stands as built. **No** (for example `PATHEXT` is not consulted for a relative path with a directory part): the rewrite would also need to append `.cmd` where a sibling exists. That is a different transform, and it goes back through the review chain as a finding | Proceed as if yes, as #448's four-spellings table reports | ⬜ |
| Q2 | With `GH_CONFIG_DIR` set to an empty directory and the four token variables unset, does a `gh` that is authenticated through the OS keyring report "not logged in"? Reading cannot answer this, because whether `gh` reaches the keyring without a `hosts.yml` depends on the `gh` version. | a measurement: one probe in phase 3 on the builder's machine, before the conftest block is written. `GH_CONFIG_DIR=<empty dir> gh auth status; echo $?`, read directly (contract §1) | **Yes:** the block is those five lines. **No:** also set `GH_HOST` to a neutral host (`example.com`, per the repository's no-real-identifiers rule) that no keyring holds a token for, and record the probe in `phases/phase-3.md` | The block as `spec.md` Scope 3 states it, with the fallback held ready | ⬜ |
| Q3 | Does any case start a child process whose environment is built from nothing, so that it inherits neither the scrub nor `os.environ`? A static read on 2026-09-24 found only in-process `env=` parameters (`test_a_body_naming_two_issues_claims_one.py`'s `main(env={})`, `test_lint_python.py`'s `_ran(…, env=…)`), and every child `env=` it saw spreads `os.environ`. That read was not exhaustive over `Popen` or wrapper helpers. | the work: phase 3 greps every `subprocess`/`Popen` call in `tests/` with an `env=` argument that is not derived from `os.environ` | **None found:** the enumeration is recorded and nothing changes. **Some found:** each one either spreads `os.environ` or carries the scrub's variables, fixed in phase 3 and named in `phases/phase-3.md` | None escape | ⬜ |

**`Who can answer` takes one of three values and nothing else:** a person,
a measurement, or the work. The framer opens rows and does not own their
answers. `Status` is ticked by whoever answers.

Answered rows feed back into `docs/` (a policy clause, or an open-questions
section) before this directory's work merges.
