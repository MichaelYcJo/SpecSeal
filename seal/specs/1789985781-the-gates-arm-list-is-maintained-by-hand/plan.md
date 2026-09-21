# Implementation Plan: the gate's arm list is maintained by hand (#468)

<!-- seal/specs/1789985781-the-gates-arm-list-is-maintained-by-hand/plan.md — HOW,
in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-21 by the repository owner's `automation` routing answer, when `smith` was spawned.

## Summary

The gate gains a declared partition of every step of `hygiene.yml`'s `release`
job: each step is mirrored by a named arm or excluded with a written reason.
A structural case asserts the partition is total in both directions, so a step
added to the workflow fails the suite until somebody classifies it. The arms
the partition finds missing are added. The stamp says what the seal did not
answer.

## Technical context

**The gate's five arms**, at `broad_gate.py#gate`: the declared row from
`seal/config.md`, then `evidence_check.py --strict`, `unverified_check.py
--baseline`, `chain_check.py --baseline`, `survivor_check.py --range`. Each is
a `run(...)` recorded into `checks`, and the panel reads that dict.

**The workflow's thirteen**, `hygiene.yml`'s `release` job, in file order:
every issue this pull request claims · a change to what ships must move the
version · every changelog fragment reached the released file · every ledger
fragment folded into the gathered ledger · the unverified record is readable ·
the pull request heads a round record may name · a declared review chain has
the round record it claimed · wording this branch removed is not still
standing elsewhere · no merge on this branch dropped a correction the ledger
had made · the milestone this release claims is the work it carries · the mode
the row declares is the mode the folder is in · the CLAUDE.md block is the
template's, line for line · both READMEs move together.

**Read the step names from the YAML, not from a list retyped here.** That list
is this document's reading of the file and will rot; the case must take them
from `hygiene.yml` itself. #424's finding 4 is the precedent — a reader driven
by nothing is a reader nobody can tell is partial — and its repair was to make
the reader take text so it could be driven.

**The precedent for the pin's shape** is
`tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py`, written for
#354's identical problem: two readers grading one tree and nothing holding
them together. Its structural half is the model.

**Constraints.**

- `broad_gate.py` runs with no third-party dependency, so **no YAML parser**.
  The step names are `- name:` lines; read them as text, and let the case fail
  loudly rather than guess if the shape changes.
- `seal_stamp.letter` gives a panel value 23 columns and cuts at the frame;
  `broad_gate.PANEL_VALUE_WIDTH` states it and the elision #424's sibling
  shipped keeps the tail.
- The plugin ships to repositories with no `hygiene.yml`. A7 is that case.
- `agent-contract` §15: the pin is driven red **from both sides**.

**The failure scenario at six months.** Somebody adds a step to the `release`
job, the suite goes red, and they write an exclusion reason to make it green
rather than an arm. The partition is then total and the seal is still short.
That is a real hole and this design does not close it — what it buys is that
the omission is now a sentence somebody wrote and signed rather than a silence.
Naming it is the mitigation; #423's comment is the precedent for preferring a
written wrong answer to an unwritten one.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A declared partition plus a two-way totality case** | An exclusion written to silence the case rather than to state a truth. Named above rather than closed | **chosen.** It is the only candidate under which the seventh arm cannot arrive silently |
| Add `correction-check` and stop | The eighth arrives exactly as the seventh did, and the suite is as quiet about it. This is the fix the issue's title suggests and the one its body argues against | rejected |
| The pin alone, no new arm | Tells a reader the gate is short and leaves it short. Every seal until somebody acts is knowingly partial | rejected as the whole answer; it is half of the chosen one |
| Generate the gate's arms from the workflow at runtime | Correct by construction, unreadable, and it puts a YAML parse into a script that runs with no dependencies | rejected |
| Make the workflow take its list from the gate | The workflow is the side the merge is judged by; it does not read a list the branch can edit | rejected |
| Classify steps by a category enum rather than prose | `EXCLUDED` tells the next reader nothing, and the reason is the whole value of the row — it is what a person checks when they wonder whether the seal covers them | rejected; `spec.md` §Scope 5 |
| Put the partition only in the test module | The gate can then say nothing about what it did not answer, which is `spec.md` §Scope 4 and A6 | rejected as the default; `questions.md` Q1 is where it becomes the answer if A7 forces it |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The step reader — names out of `hygiene.yml`'s `release` job as text — and the classification of all thirteen, with M1's number recorded | A1 and A2 red against the reader's absence and against a renamed step. The reader driven over shapes the file does not have, so it is not a reader nothing drives | ffcb4d8 |
| 2 | The arms the partition found missing, whatever the count | A5 red against the gate as it stands. A3 red when an arm is deleted while its row stands | 99f9bf1 |
| 3 | The stamp saying what the seal did not answer | A6 over the rendered output, red when the branch that prints it is deleted; W1's choice recorded | 0ec4571 |
| 4 | A4, A7, and the documents — `skills/verify/SKILL.md`, the changelog fragment, the `seal/ledger/` fragment | A4 red against a reason reduced to a category. A7 red against the gate breaking where no workflow exists | f30601b |

Phase 1 changes no behaviour on purpose: the reader and the classification are
where the cases are, and separating them lets phase 2's cases be about the
arms rather than about the reading.

## Operational impact

- **Failure direction: the gate refuses more.** It gains arms; it loses none.
  A branch that would have sealed green and met a red leg now meets the
  refusal at the gate, which is the cheaper place.
- **Prompt budget: zero.** No question is added to any session.
- **The seal gets slower** by however long the new arms take. `correction-check`
  over this repository's history is sub-second; anything slower is named in
  `overview.md` with its measurement.
- **No new dependency, no new env var, no migration.**
- **Platform honesty.** Reading text out of a file and running Python scripts;
  the fixtures run on every matrix leg. Not run on Windows or Linux from this
  machine — CI is the answerer.
- **A repository with no `hygiene.yml` is unaffected** — A7.
