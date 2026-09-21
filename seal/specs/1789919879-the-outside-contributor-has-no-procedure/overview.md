# the outside contributor has no procedure — overview

📋 implement applied
· spec:     `seal/specs/1789919879-…/{spec,plan,questions,routing}.md`; `CLAUDE.md` §*The goal a design is chosen against*, §*a change writes fragments*, §*no real identifiers*, §*the merge method is fixed per direction*; `CONTRIBUTING.md` §*What a change to a gate must carry*, §*House rules*; `docs/branch-and-release.md` §*Work accumulates on a release branch*; `skills/agent-contract/SKILL.md` §§1–2, 7–9, 12, 15; `skills/implement/SKILL.md` §§1–4; `skills/writing-style/SKILL.md`
· evidence: R1 and R2 in `seal/ledger/1789919879-the-outside-contributor-has-no-procedure.md`; three rows in `seal/ledger.md` re-verified after this branch drifted their anchors
· verified: **executed** — the five narrow modules named below, twelve mutations, the workflow re-parsed as YAML, the refusal rendered through `bash`, `evidence-check` exit 0. **read** — every CI step behind the exemption list, against the frame's table. **unverified** — the full suite, lint and typecheck; the sealer answers

## Why this work exists

A first-time contributor's pull request was filed against `main` because
nothing this repository showed a contributor said where one goes, and the gate
that caught it told them to edit the one file they must not touch.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The precedent for phase 1's pin | `plan.md` phase 1 and `questions.md` Q6 both cite `tests/test_the_suite_has_a_command_that_is_cheap_twice.py#contributing_section`. `grep -rln contributing_section tests/` returns nothing | Built on `running_the_checks()` in that same file | The frame is right about the precedent and wrong about its name: `running_the_checks()` reads one `CONTRIBUTING.md` section to the next heading and asserts what it names, which is exactly the shape Q6 describes. The new module's docstring carries the correction so the next reader of Q6 is not sent after a function that does not exist |
| A name in the frame that the tree does not have | `spec.md`'s measurement table cited `issue_claims_check.py`'s `read_body` as grounds for *an empty body is a body*. The record checker refused it: `NOT-IN-TREE … spec.md:66` | Corrected to `body_from`, and this row carries the marker — it is a record OF the retired name, which is the case the marker exists for | The claim itself holds — `body_from`'s own docstring says an empty `PR_BODY` is a body and an absent one is the only thing worth an exit code. Only the coordinate was wrong. Round 1's 🔴 1 found this row and two in `phases/phase-5.md` refused for naming the retired coordinate they are about; the repair is the marker rather than stripping the backticks, because a line whose passing depends on an invisible absence of backticks goes red again at the next reformat <!-- NAME NOT IN TREE: read_body is the retired coordinate this row exists to record. Round 1 🔴 1. --> |
| The order of the two causes in the refusal | `spec.md` A1 asked for the base-branch case **before** `plugin.json`; the message ships `plugin.json` first, and `test_the_refusal_still_serves_the_release_and_puts_it_first` pins that order | The release case first, and A1 corrected to match | The step cannot tell its two readers apart — a release that forgot the bump and a contribution on the wrong base both arrive with `base_ref = main` — so the message names both causes and asserts neither. The release reader is the one the old text was already right for, which is why that clause keeps its place. `plan.md` §*The design constraint the message has to satisfy* fixes the order and `phases/phase-2.md` decides it as Q7. Round 1's 🟡 2 found that nothing recorded the disagreement: the decision was right and unwritten, so a reader checking the branch against its own acceptance criteria met an unmet one with no answer beside it |
| S5's budget of two pins | `spec.md` S5 scopes `tests/` to two pins, and phase 1 and phase 2 spent both | A third pin, as one parametrized case inside the module phase 1 already wrote | Round 1's 🟡 5. Q1's grounds — a concrete release branch is deleted after its release, so the sentence expires on a schedule — are about the rule, and this branch wrote the rule onto three more surfaces without guarding any of them. That is `agent-contract` §12's shape exactly: the defect was fixed at the coordinate it was found on. The budget is widened rather than the finding deferred because the surfaces it now covers are ones this branch created, and the pull request template is the one a maintainer reads on every pull request. No new module: the case went into the module phase 1 already wrote. S5 budgets two pins and this is a third, which is the divergence this row records |
| The first form of phase 2's guard case | Modelled on `tests/test_a_release_cannot_ship_an_untrue_milestone.py#hygiene_step`, a `re.S` span from `then` to `exit 0 … fi`. It survived the mutation it exists to catch | Rewritten to assert the guard closes before the next `if` | This step holds a **second** `if … exit 0 … fi` — the `-z "$ships"` early return — for the dotted span to reach; the precedent's step does not. The precedent's docstring warns about this exact mutation, so reading it was not enough and running the mutation was |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, after the review rounds settle — `agent-contract` §2 leaves the broad gate to it |
| That the repaired refusal reads well **in GitHub's rendered error panel**, as opposed to in the workflow file and a local `bash` run | whoever next opens a pull request into `main` that changes a shipping root without moving the version — the step is `ubuntu-latest` only and nothing here can run it |
| Whether a maintainer leaves the pull request template's comments in place in practice | the repository owner, after a few pull requests carry it |

## Not done

**`survivor_check.py`'s own refusal text is unchanged** (Q4, `spec.md` O7).
It is the one CI message that can send a contributor into a `seal/`
convention, and repairing it is a second gate change with its own red-test
bar, inside a work item already carrying one. Zero contributors have met it.
The trap is closed with a sentence in `CONTRIBUTING.md` instead; a contributor
who does meet it is the occurrence that buys the repair.

**No third test module for the pull request template.** `spec.md` S5 budgets
two pins and both are spent. The template joined two checks that already
existed — the wrap limit and the identifier scan — and both were mutated to
prove they reach it, rather than a third module being written to cover one
file.

**No ledger row for the template.** Its base-branch fact has no anchor worth
hashing: the only distinctive line resolves to a one-line region, and a row
anchored there would claim more than it can detect.

## Fed back into the spec

Two corrections, both recorded in the divergence table above and in
`phases/phase-1.md` and `phases/phase-5.md`, and both marked as found during
implementation so a planner may overturn them:

- Q6's precedent is `running_the_checks()`, not `contributing_section`.
- The measurement table's grounds for `issue_claims_check.py` is `body_from`.

No clause was added. Q7 was answered in `phases/phase-2.md` rather than
written back here, because the case it planted is what pins the answer.
