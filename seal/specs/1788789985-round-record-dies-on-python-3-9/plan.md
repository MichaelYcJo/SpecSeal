# Implementation Plan: round-record says which interpreter it needs

<!-- seal/specs/1788789985-round-record-dies-on-python-3-9/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

## Summary

`round_record.py` dies on an interpreter below the supported floor with an
interpreter traceback, after argument parsing, path resolution and the report
read have all succeeded — so the failure reads as a bug in the report. A
fifteen-line block at the top of the file turns that into a sentence naming the
floor, the version found and the interpreter it was found at, printed before
anything is read or written. The four `zip(..., strict=True)` sites stay.

The design gate was answered in the routing batch: `routing.md` records that the
0.9.1 run was routed once for all five of its work items, and that this item
raised no question needing a person, because `CONTRIBUTING.md` already states
the floor and the floor is what decides between the ticket's two repairs.

## Technical context

- `skills/code-review/scripts/round_record.py:103-114` — the module imports
  `argparse, ast, importlib.util, json, os, re, shutil, subprocess, sys,
  tempfile`. Every one of them exists on 3.9, so the guard can sit after them
  without risking an `ImportError` before the sentence.
- `:115-128` — `HERE`, `CHAIN`, `def load`, and then `chain = load(CHAIN,
  "specseal_chain_check")`, which reads and executes a sibling script **at
  module import**. Measured on 3.9.6: that load succeeds. It is the first
  module-level act that does real work, and the guard goes in front of it.
- `:761-767` — the comment that says what `strict=True` states, and the site the
  ticket's traceback names.
- `:99-100` — the documented exit codes, which the new path extends.
- `.github/scripts/run_tests.py:56-57` — `FLOOR = (3, 12)` and `FLOOR_TEXT`.
  The names and the derivation are copied, so the two files read alike.
- `ruff.toml:29` — `target-version = "py312"`, the other authority.
- `ruff.toml` `select` includes `E4`, so **E402** is live: code placed between
  imports would make every later import a lint failure. That is why the guard
  sits after the import block rather than after `import sys`, and the py_compile
  sweep is what makes that safe rather than hopeful.

**What breaks in six months.** Someone raises the floor to 3.13 in `run_tests.py`
and `round_record.py` keeps saying 3.12, so the sentence names a version that is
no longer the floor. `test_the_floor_is_the_number_the_runner_and_the_linter_hold`
is the answer: the suite fails at the commit that causes it. The residual risk is
a floor raised in a repository whose suite nobody runs, which is a risk this
repository already carries five times over for the same number.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Drop `strict=True` at the four sites, as the ticket's first suggestion offers | 3.9 gets a few lines further and dies at the next 3.10+ construct with the same bare traceback, and the invariant `:761-766` states — that the reader's two passes are the same file line for line — is gone, so a truncated hidden set reports clean | **rejected.** `CONTRIBUTING.md` §*Running the checks* says 3.12 is the supported floor, so this buys compatibility with a platform the repository does not support, at the price of a real check |
| Guard inside `main()`, first statement | `chain = load(CHAIN, …)` runs at import, before `main()` is called, so the script would still read and execute a second file before saying anything. On 3.9 that load succeeds today, so a reader watching it succeed is watching exactly the progress the ticket is about | rejected |
| Guard at the very top, after `import sys`, before the other imports | E402 fires on all nine later imports; nine `# noqa: E402` comments to buy an ordering the py_compile sweep proves is unnecessary | rejected |
| Import `FLOOR` from `.github/scripts/run_tests.py` | A guard with a second way to die, on the one machine that has no other way of being told what is wrong; and the `except` branch still has to name a floor, so the second spelling survives anyway | rejected — the argument is in `spec.md` §*Where the floor number lives* |
| A shared helper module both this file and the other scripts import | The import is the fragility above, once per adopter; and no location for it is nearer than the file it guards | rejected — the block is copyable and `spec.md` names it as the spelling to copy |
| `FLOOR = (3, 12)` in the file, pinned to `run_tests.FLOOR` by a test | The test has to be run for the pin to hold, and a floor raised without running the suite drifts until CI catches it — one push later | **chosen.** It is the mechanism the repository already uses for the same number in five other places |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The SDD set: `spec.md` with the enumeration table, this plan, `questions.md` | the class enumerated by three executed constructions, recorded with its own method error | `99d4df0` |
| 2 | The guard in `round_record.py` — `FLOOR`, `FLOOR_TEXT`, `BELOW_FLOOR`, `below_floor()`, the module-level refusal — and the docstring's exit-code line extended | `bin/test tests/test_a_script_says_which_interpreter_it_needs.py -q`, seen red first; and `/usr/bin/python3` (3.9.6) running the real script | `c67a210` |
| 3 | The records: the four deferrals in `seal/follow-up.md`, the changelog fragment, the ledger fragment, the phase records, `overview.md` | `bin/test tests/test_release_hygiene.py tests/test_a_record_states_what_the_tree_has.py -q`, `evidence_check --reverify`, and the two suites of phase 2 re-run | `5ed5fe7` |

## Operational impact

- **No migration, no new dependency, no new environment variable.** The guard is
  stdlib `sys` and nothing else.
- **One compatibility break, and it is the point.** An interpreter below 3.12
  that today gets partway through `round_record.py` now gets nothing at all.
  Nothing in this repository ran it on such an interpreter: CI pins the floor,
  `bin/test` refuses below it, and the ticket exists because a machine outside
  the repository did.
- **Exit code 2 gains a second meaning.** Anything reading that code by number
  cannot tell the two apart; nothing does today — the orchestrator reads the
  sentence.
