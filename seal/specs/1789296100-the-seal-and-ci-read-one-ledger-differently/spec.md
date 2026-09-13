# Feature Specification: the lenient ledger run says what the broad gate will say

<!-- seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/spec.md — WHAT this
work delivers and how we'll know. The policy documents in docs/ outrank this
file; cite them, don't restate. -->

Issue #354. Three readers of one exit code run `evidence_check.py` over one
tree and grade the same ledger differently. The command every document names — `bin/evidence-check`
— comes back exit 1 on drift; `broad-gate`, the one reader that gates, runs the
same script with `--strict` and comes back exit 2, and the branch is `NOT
SEALED`. A session that runs the documented command more often never finds
this, because the documented command is not the one that decides.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CONTRIBUTING.md` §*What a change to a gate must carry* | This changes what a gate-adjacent command reports to a person, so the work owes a case seen red, a stated failure direction, a prompt budget and a platform answer. All four are in `plan.md` |
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | Between shapes that carry the same fact, the one that needs nobody to remember it wins. It is why the fact goes in the checker rather than in a sentence somebody must read |
| `skills/agent-contract/SKILL.md` §12 | The defect is a class — *a gate reads something more strictly than the command the documents name*. §*The class, enumerated by construction* below is the enumeration |
| `skills/agent-contract/SKILL.md` §14 | A change to what a person reads documents it and pins it in the same commit |
| `skills/agent-contract/SKILL.md` §15 | The case that pins this is not planted until it has been seen red |
| `agents/sealer.md` §*The one run, and why it is yours* | The strict gate is right and stays strict. Nothing here argues for making the broad gate lenient |
| `CLAUDE.md` §*A change writes fragments, never the shared file* | The changelog entry goes to this directory's `changelog.md`, the ledger rows to `seal/ledger/1789296100-….md` |
| `CLAUDE.md` §*no real identifiers in examples or fixtures* | The new module's fixtures use `example.com` and `/Users/x/` if they need either |

## What is true today, read and not executed

Every coordinate below was opened in this session; nothing was run.

| Reader | Coordinate | What it grades drift as |
|---|---|---|
| `broad-gate` | `skills/verify/scripts/broad_gate.py:570` — `run(LEDGER, [py, EVIDENCE, "--strict", root], …)` | exit 2, and the run prints `NOT SEALED` |
| CI's `ledger` job | `.github/workflows/test.yml:84-93` — `evidence_check.py .`, then `if [ "$code" -eq 1 ]; then echo "::warning::…"` | exit 1, rendered as a warning |
| `bin/evidence-check` | `bin/evidence-check:12` — `exec python3 "$here/../skills/evidence-check/scripts/evidence_check.py" "$@"` | exit 1. It adds no flag and holds no default |
| `hooks/evidence-advisor.py` | `hooks/evidence-advisor.py:129` — `if status in ("BROKEN", "OLD-FORMAT")` | not reported at all, deliberately: *a branch mid-flight legitimately drifts* |

The strict form is stated in exactly one place outside the call site:
`skills/verify/scripts/broad_gate.py:18`, the script's own header. `agents/sealer.md`,
`skills/verify/SKILL.md` §*The broad gate*, `README.md:43` and
`skills/evidence-check/SKILL.md` all describe the check without saying which
form the gate runs. Read in full; none of them names `--strict`.

The exit-code rule the whole change turns on is
`skills/evidence-check/scripts/evidence_check.py:2471-2478`:

```
if totals["OLD-FORMAT"]: return 2
if totals["BROKEN"] or refused: return 2
if totals["DRIFTED"] or drifted: return 2 if args.strict else 1
return 0
```

**Exit 1 is exactly the disagreement.** It happens only where nothing is broken,
nothing is old-format, nothing was refused, something drifted, and `--strict`
was absent. Every other exit code is a state the two readers already agree
about. So the tree where the documented command and the gate disagree is
identifiable at the one moment the checker already computes its answer.

## The class, enumerated by construction

`agent-contract` §12: the finding names an instance and the fix is owed to the
class. The class is *a gate invokes a check more strictly than the form the
documents name*, and it is enumerated from `broad_gate.py`'s own list of what
it runs — `skills/verify/scripts/broad_gate.py:566-587`, five call sites, not
from reading around the repository.

| # | Call site | What the gate passes | Member? |
|---|---|---|---|
| 1 | `checks[SUITE]` | the `Broad gate` row of `seal/config.md`, verbatim, and the gate prints the row before running it (`:568`) | **No.** The documented form *is* the row. The gate adds nothing |
| 2 | `checks[LEDGER]` | `evidence_check.py --strict <root>` | **Yes.** This is #354, and the only member |
| 3 | `checks[UNVERIFIED_NAME]` | `unverified_check.py --baseline <base> <specs>` | **No.** `--baseline` turns on the deleted-rows arm, and `README.md:262` documents that flag with exactly that effect; `skills/implement/SKILL.md` §4 names the baseline form as the one run at the pull request. The gate runs the documented pull-request form |
| 4 | `checks[CHAIN_NAME]` | `chain_check.py --baseline <base> --root <root>`, under `draft_env` | **No, and it is the mirror.** The draft payload *excuses* three requirements, so the gate is LOOSER here than a ready pull request's own `ledger`/chain job. It is stated in two places — `broad_gate.py:22-24` and `chain_check.py`'s docstring — and it is the correct reading at that moment, because the gate runs before `seal` writes the `Broad gate` cell |
| 5 | `checks[SURVIVORS_NAME]` | `survivor_check.py --range <base>...HEAD` plus every `survivors.md` as `--exempt` | **No.** The exemptions loosen, and the range is the documented pull-request form (`bin/survivor-check:10`) |

One member. The mirror at #4 is named here so a later session does not
re-enumerate: it has the shape but not the defect, because both sides of it are
written down.

`hooks/evidence-advisor.py` is a fourth reader of the same checker and is not a
member either — it gates nothing, and its own docstring says why it is silent
on drift. It is in the reader table above so that a session counting readers
gets four rather than the issue's three.

## Scope

**In.**

1. `evidence_check.py` says, on a run whose answer is exit 1 and only then,
   that the broad gate runs the same check with `--strict` and would refuse
   this tree. Every reader that runs the checker gets it: both wrappers, the CI
   `ledger` job, and a bare `python3 …/evidence_check.py .`.
2. A case pins the sentence and the flag against each other, so neither can move
   without the other going red.
3. Every document that describes the lenient reading names the strict one
   beside it: `skills/evidence-check/SKILL.md`, `README.md`, `README.ko.md`,
   `CONTRIBUTING.md`, and the `ledger` job's own comment in
   `.github/workflows/test.yml`.
4. The records this repository's conventions require: `changelog.md` and
   `seal/ledger/1789296100-….md` in this directory's own fragments.

**Out, each with the reason.**

| Not doing | Why |
|---|---|
| Making the broad gate lenient | `agents/sealer.md` §*The one run* — the gate is one act at the end over a tree nobody is still editing, and drift that was tolerable mid-flight is what should stop it. The issue states this as a constraint, not an option |
| Making CI's `ledger` job strict | `.github/workflows/test.yml:70-74` argues it in the job's own comment: a branch mid-flight legitimately drifts, and *a check that is always red gets ignored*. The disagreement is repaired by saying so, not by making three readers into one |
| Teaching `hooks/evidence-advisor.py` to report drift | Same comment, from the other side: *a line that prints on every commit is a line people learn to skip* (`hooks/evidence-advisor.py:20-22`). Its silence is a decision, not an oversight |
| Running the strict form inside a review round | The issue's shape 3. `agent-contract` §2 keeps the broad act out of a round's hands, and this would put a piece of it back |
| Closing the chain check's draft/ready mirror (#4 above) | It has the shape and not the defect — both readings are written down where a session looking at either one finds the other |
| Changing `bin/evidence-check` or `bin/evidence-check.cmd` beyond their header comments | `plan.md` §Alternatives holds the argument. Two shell re-implementations of one rule is the duplication `survivor-check` exists to catch |
| The malformed-coordinate row in `seal/follow-up.md` | A different defect in the same file — a row whose hash does not parse produces no row at all. It is not this work's prerequisite, and it needs a judgment the owner has not given |

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | The documented command says what the gate will say | Given a tree whose only ledger finding is drift · When `evidence_check.py .` runs with no `--strict` · Then it exits 1 **and** its output states that the broad gate runs the same check with `--strict`, and that this tree would come back refused | new module, behavioural case, seen red against the unfixed checker |
| S2 | The deciding form does not repeat itself | Given the same tree · When `evidence_check.py --strict .` runs · Then it exits 2 and the sentence is absent — the reader already ran the form that decides | same module |
| S3 | Silence where the readers agree | Given a clean tree, and separately a tree with a BROKEN anchor or an OLD-FORMAT row · When the checker runs either way · Then the sentence is absent: exit 0 and exit 2 are states every reader grades alike | same module |
| S4 | The disagreement cannot come back silently | Given the repository · When the case reads `broad_gate.py`'s ledger call site, `bin/evidence-check`'s pass-through, and the SKILL's sentence · Then it fails if any one of the three moves out of step with the others | structural case, seen red by removing `--strict` from `broad_gate.py:570` |
| S5 | No document describes one reader alone | Given `skills/evidence-check/SKILL.md`, `README.md`, `README.ko.md`, `CONTRIBUTING.md` and `.github/workflows/test.yml`'s `ledger` comment · When each describes drift's exit code · Then the strict reader is named beside the lenient one | S4's case over those files, plus reading |
| S6 | CI's `ledger` job still warns and does not fail | Given a drifted tree in CI · When the `ledger` job runs · Then it still exits 0 with a `::warning::`, and the new sentence reaches the log as part of the script's stdout | read the workflow; the added output is stdout only and no exit code moves |
| S7 | No existing reader's exit code moves | When the two ledger modules run · Then they pass unchanged | `bin/test tests/test_a_row_points_by_content.py tests/test_a_record_states_what_the_tree_has.py -q` |
| S8 | The records land in fragments | When the work closes · Then the changelog entry is in this directory and the ledger rows in `seal/ledger/1789296100-….md`, with `CHANGELOG.md` and `seal/ledger.md` untouched | `git diff --stat`; `bin/evidence-check` over the new fragment |

## Data & interfaces

No schema, no endpoint, no new dependency. One new output line from one
existing script, under one existing exit code, plus one new test module.

The line is printed on **stdout**, after the records arm's counts and before
the process returns, because the totals a reader compares it against are on
stdout and CI captures stdout into the job log.

Coordinates this builds on, to be cited by the ledger fragment rather than
duplicated here: `skills/evidence-check/scripts/evidence_check.py#main`,
`skills/verify/scripts/broad_gate.py#gate` — the ledger call site is in `gate`
(lines 516-641) and not in `main` (644-678), which phase 4 found and the
fragment records. Corrected here in round 1's fix pass, because a reader who
opens the contract should not have to open two other files to get the unit.

## Open questions → questions.md

Three rows, one of them a person's. `questions.md` in this directory.
