# the broad gate row runs unchecked and is never asked for (#402, #401) — questions for the planner

<!-- seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

**No row here needs a person, and nothing here blocks the build.** Both
judgments the two tickets left open are answered in `spec.md` and `plan.md`
from documents already in the tree, and the section below says which and
where. What remains is one row a command settles and three the phase that
meets them settles.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does any fixture row in the existing gate cases take one of the three refused forms, so that phase 1's refusal turns a green case red for the wrong reason? | **a measurement** — phase 1's first act | Run `bin/test -q tests/test_the_seal_is_taken_once_by_the_sealer.py` with the refusal in place and read what moved. A fixture row that is refused is a fixture to rewrite, not a reason to narrow the refusal — the module's rows are bare `pytest` calls today, so the expected answer is none | none refused | ⬜ |
| Q2 | Which of the fifteen ledger rows this work drifts still hold after the edits, and which went with the code? | **a measurement** — phase 5, `bin/evidence-check --strict .` then re-reading each | Per `CONTRIBUTING.md` §*House rules*: a claim that still holds is re-read and `bin/evidence-check --reverify .` recomputes its hash; a claim that went with the code has its row **removed** from `seal/ledger.md` and the new claim written into this work item's fragment. The count is in `spec.md` §*Data & interfaces*, by anchor | re-verify; remove only where the claim is gone | ⬜ |
| Q3 | What is the refusal's function called, and what does its message call the three forms? | **the work** — phase 1 | `tests/test_one_word_one_meaning.py` and `CLAUDE.md` §*a thing more than one party can have is named with whose* bound the answer rather than give it. Two candidates are already spent: **refused** is what exit 2 means across the gate, the sealer and the round record, and **wrapped** has to stay about the value rather than about the row. What is settled is the criterion the name has to carry — *the value does not run as the command it reads as* | none — the constraint is what is settled, not the word | ⬜ |
| Q4 | Does the bootstrap's proposal read candidates off the repository, and from what? | **the work** — phase 4 | `skills/implement/orchestration.md` §*Orchestrator: Parity setup* is the shape: what the machine can derive is proposed and the person picks, and nothing is guessed. What it can derive here is a judgment about cost — a package manifest's test script, a `Makefile` target, a runner under `bin/` — against offering only *write it now* and *none yet*. A proposal with nothing in it is the objection the form exists to answer, so the floor is at least one derived candidate where one is findable | at least one derived candidate, and a decline that says what it costs | ⬜ |

## What is not a question, and why

**#402's judgment — what is refused beside backticks.** Decided in `spec.md`
§*What is refused, and what stays allowed*: the whole value wrapped in
backticks, the whole value wrapped in `$(…)`, and a trailing `&` that is not
part of `&&`. The criterion is written beside the list — *the value must run
as the command it reads as, and the exit code the gate reads must be that
command's* — and a pipe fails neither half, which is why it stays legal with
its cost stated. The grounds are the executed table in `spec.md`, `#402`'s own
steer, and `agent-contract` §12. No part of it turns on anybody's preference.

**The trailing `&` is the one line a reviewer is most likely to argue with**,
and it is argued for in `plan.md`'s alternatives table rather than left
implicit: it is enumerated from the class rather than reported from use, and
nothing has met it. It is written as a row a reviewer can open and contest, not
as a question to hold the build open for.

**#401's judgment — when the row is asked for.** Decided in `plan.md`'s
alternatives table: at bootstrap, in the same `AskUserQuestion` as the mode,
in the form of a proposal. The three candidates the ticket named are weighed
there against `CLAUDE.md`'s first goal and against the objection that a
repository being opted in may not yet know its broad command — which is what
makes the proposal the **form** rather than a rival timing.

**#401's third half — the criterion.** Three rules, in `spec.md` §*The
criterion for choosing a value*, owned by `templates/config.md` §*Broad gate*.
Two of them were derived under pressure by the reporting session and are
written nowhere today; the third exists in two places and is folded into the
one home rather than copied a third time.

**A trace for a knowing decline.** Decided against in `spec.md` §Scope, with
the mode row's own history as the argument rather than against it: #151's cost
was that a never-asked repository got shared mode *silently*, and nothing about
this row is silent. A repository that declined and one that was never asked
meet the same refusal at the same moment and are told the same correct thing.

**The three constraints the framing prompt put out of reach** — no default
value, the refusal on an absent row stays, the sealer picks nothing — are
recorded in `spec.md` §Scope as out of scope with their reasons, not carried
here as open.

**Routing.** Answered by the owner in one batch before the first edit and
committed at `routing.md` beside this file: review through the review chain,
destination open the pull request, planning the framer, implementation `smith`.

**The record language.** `seal/config.md` carries a `Mode` row and a `Broad
gate` row and no `Record language` row, so these documents are in English —
every way of not naming one lands on English (`skills/implement/SKILL.md`
§*The language the records are written in*).
