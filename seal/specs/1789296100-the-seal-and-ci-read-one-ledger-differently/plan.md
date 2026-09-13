# Implementation Plan: the lenient ledger run says what the broad gate will say

<!-- seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

Approved <date> by <who>, when `smith` was spawned.

## Summary

`evidence_check.py` gains one printed line, on the one exit code where its two
readers disagree. Where the run's answer is exit 1 — drift, nothing broken,
`--strict` absent — it says that `broad-gate` runs this same check with
`--strict` and that this tree would come back refused. Every other exit code
prints nothing new, because every other exit code is a state all four readers
already grade alike.

Then the documents stop describing one reader: the SKILL, both READMEs,
`CONTRIBUTING.md` and the `ledger` job's own comment name the strict reader
beside the lenient one. A case holds the three statements of the fact — the
gate's flag, the wrapper's absence of one, and the SKILL's sentence — against
each other, so the next edit to any of them goes red rather than going quiet.

## Technical context

- `skills/evidence-check/scripts/evidence_check.py:2471-2478` — the exit block.
  `2 if args.strict else 1` is the whole disagreement, and the condition for the
  new line is *this run is about to return 1*. Computing the return value first
  and printing on it needs no new predicate and cannot drift from the grading.
- `skills/evidence-check/scripts/evidence_check.py:2405-2470` — the summary
  block the line is appended after: the `total:` line, then the records arm's
  heading and its counts.
- `skills/verify/scripts/broad_gate.py:570` — `run(LEDGER, [py, EVIDENCE,
  "--strict", root], root, keep)`. The sentence the checker prints has to stay
  true of this line, which is what S4's case is for.
- `skills/verify/scripts/broad_gate.py:18` — the header that states the strict
  form. It is the only statement of it outside the call site today.
- `bin/evidence-check:12` and `bin/evidence-check.cmd` — pure pass-through, a
  POSIX/Windows pair held in lockstep by
  `tests/test_chain_hooks_hardening.py:274-293`. This plan does not touch
  either beyond the usage comment in the POSIX file's header.
- `.github/workflows/test.yml:69-93` — the `ledger` job. It reads the exit code,
  not the text, so the added stdout line reaches the log and moves nothing.
- `tests/test_a_record_states_what_the_tree_has.py:551-576` — the case that
  already exercises exit 1 and exit 2 over one drifted fixture. It is the
  nearest existing case and it pins the flag's effect, not the readers'
  disagreement; the new module is what pins the disagreement.

**What breaks in six months.** Someone adds a sixth check to `broad_gate.py`
that carries a flag the documented form does not, and nothing about this work
catches it — S4's case is written for the ledger call site by name. The class
enumeration in `spec.md` is what a later session reads instead of re-deriving
it, and the enumeration is by construction from `broad_gate.py`'s own list, so
a sixth call site is visible in the same place the other five are.

## What a change to a gate must carry

`CONTRIBUTING.md` asks four things of a change in this neighbourhood.

- **A test seen red.** Phase 1 writes both cases against the unfixed tree and
  records how each was seen failing. `agent-contract` §15: not planted until
  seen red.
- **Failure direction.** This change makes nothing block and nothing allow: no
  exit code moves in any reader. Wrong-silent loses one sentence a session
  would have read; wrong-printed states something true on a tree where the gate
  would in fact refuse. Both are cheap, and the cheaper mistake is the printed
  one, which is the direction the condition errs toward — it prints on every
  exit 1, including runs nobody will ever seal.
- **Prompt budget.** Zero. Nothing here asks a person anything, at any point,
  in any session. That is the whole argument for the shape: the fact arrives in
  output somebody is already reading rather than in a document somebody must
  remember to open.
- **Platform honesty.** No process inspection, no git call, no filesystem
  probing. One `print` in a script CI already runs on ubuntu, macOS and Windows.
  The wrapper pair is untouched, so nothing about the `.cmd` lockstep changes.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Chosen: the line is printed by `evidence_check.py`, on exit 1 only** | Output changes for every caller at once, so a caller that parses stdout could break. Bounded: the line is appended after the totals, so substring assertions survive, and S7 runs the two ledger modules to show it | **Taken.** One place to state the fact, and it reaches all four readers — both wrappers free, CI's `ledger` job, and a bare `python3 …` call |
| The issue's shape 1 as literally written: `bin/evidence-check` gains the line or an `--as-the-gate` flag | The wrapper `exec`s. To print conditionally it must stop exec'ing, capture the child's exit code and re-implement the rule — twice, once in `sh` and once in `.cmd`, held in lockstep by a case. And the fact still misses the CI job and the bare script call, which are two of the four readers | **Rejected.** Its intent is right and its location costs a duplicated rule while reaching fewer readers. This plan is shape 1's intent one file deeper |
| The issue's shape 2: documents only | It does nothing at all for a session that reads an exit code rather than the prose, which is the session #84 measured. `CLAUDE.md`'s first goal is verification that needs nobody to remember | **Rejected as the mechanism, folded in as phase 3.** The documents still have to stop describing one reader — that is `agent-contract` §14, documenting a change to what a person reads |
| The issue's shape 3: a review round runs the strict form | `agent-contract` §2 keeps the broad act out of a round's hands, and `agents/sealer.md` holds the reasoning. A round that ran a piece of the gate would spend the piece it ran | **Rejected.** The issue argues against it too |
| Make CI's `ledger` job strict so all three readers agree | Red by construction on every mid-flight branch, which is what the job's own comment refuses: *a check that is always red gets ignored* | **Rejected.** Three readers grading one tree differently is correct; not saying so is the defect |
| Print the line on every run, clean ones included | `hooks/evidence-advisor.py:20` measured this shape: *a line that prints on every commit is a line people learn to skip* | **Rejected.** The condition is exactly the disagreement, and the disagreement is exit 1 |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` — the behavioural case (S1–S3: a drifted fixture, run lenient, run strict, run clean, run broken) and the structural case (S4–S5: `broad_gate.py`'s ledger call site carries `--strict`, `bin/evidence-check` holds no default, and the SKILL states both readers). Both seen red before anything is fixed | `bin/test tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py -q` — red. The behavioural case red against the unfixed checker; the structural case shown red by deleting `--strict` from `broad_gate.py:570` and restoring it. The phase record says how each was seen failing | `eb0189d` |
| 2 | `evidence_check.py` prints the sentence where its answer is exit 1 and nowhere else. Phase 1's behavioural case goes green | the new module green, and `bin/test tests/test_a_row_points_by_content.py tests/test_a_record_states_what_the_tree_has.py -q` green — S7, that no existing reader moved | `acb496e` |
| 3 | The documents name both readers: `skills/evidence-check/SKILL.md` (the Run block, the `--strict` flag row, the `DRIFTED` verdict row), `README.md` and `README.ko.md`'s ledger paragraph, `CONTRIBUTING.md`'s check list, and the `ledger` job's comment in `.github/workflows/test.yml`, which today argues leniency without naming the reader that disagrees. Phase 1's structural case goes green | the new module green; `bin/test tests/test_a_narrowed_ledger_read_says_what_it_skipped.py tests/test_chain_hooks_hardening.py -q` green — the two modules that read the SKILL and the wrapper pair | `dd6fd94` |
| 4 | The records: `changelog.md` and `seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md` in this directory's own fragments, and `overview.md` closed. `CHANGELOG.md` and `seal/ledger.md` untouched | `bin/evidence-check .` over the new fragment; `bin/unverified-check seal/specs/`; `git diff --stat` showing neither shared file in it | |

Phase 3 is where the `README.ko.md` counterpart lives, and it is not optional:
`README.md:145-147` and `README.ko.md:140-142` state the same sentence in two
languages, so a change to one and not the other is exactly the surviving
wording `survivor-check` reports at the pull request.

## Operational impact

No migration, no environment variable, no dependency, no compatibility break.
One added line of output in one script, under an exit code that does not move.
A repository that pipes `evidence_check.py`'s stdout into something that parses
it by position would see one more line at the end of an exit-1 run; nothing in
this repository does, and the CI job reads the code rather than the text.
