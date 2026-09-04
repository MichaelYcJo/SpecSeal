# Feature Specification: the roll opens the next log with no body

<!-- seal/specs/1788486395-the-roll-opens-the-next-log-with-no-body/spec.md — WHAT this
work delivers and how we'll know. The policy documents in docs/ outrank this
file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log* | It names the rolling log and never the durable one, so the instruction a session follows sends every reading — including the ones that only mean something across versions — to the issue that gets deleted at the release |
| `.github/scripts/roll_flow_measurement_issue.py` docstring | *"The invariant is exactly one open `flow-measurement` issue at a time … this fails loudly rather than guessing."* That invariant is what a session may not repair by creating one, and what a person tidying the tracker can break by closing one |
| `docs/issues-and-milestones.md` | The tracker's own authority, added on 2026-09-04. This work points at it rather than restating the three milestone kinds or the hazard |
| `hooks/version-check.py` docstring | *"telling someone a release exists and installing software on their machine are different acts, and only the first is a notice's job."* The same line separates *naming a broken invariant* from *repairing it* |
| `CLAUDE.md` §*The goal a design is chosen against* | Decides the shape of every part below: nothing here adds a question, and the parts that could fail a release are set best-effort instead |

## Scope

**In.**

- `skills/verify/SKILL.md` says which reading goes to the rolling log and which
  to the durable one, and **how a repository declares its durable one** — a
  second label, since the skill ships to repositories that have no #51.
- The same section separates two zeroes: a repository that never measured from
  one that stopped. Today both are a silent no-op.
- `roll_flow_measurement_issue.py`'s `open_issue` gives the issue it opens a
  **body** — the issue just closed, and the durable ledger — where today it
  passes `--body ""`.
- The same call adds this repository's index label and its `log:` milestone,
  both **best-effort**: a failure there says so in the body of the issue just
  created and does not fail the release.
- This repository's own durable log gets the new label.
- Tests, a changelog fragment, and a ledger fragment.

**Out.**

- **A session creating a `flow-measurement` issue.** Two sessions finishing
  segments together both read zero and both create, and the next release fails
  on two-or-more. Creation stays with the script.
- What a measurement must *say* to be worth keeping — that is #137.
- The tracker's conventions themselves. `docs/issues-and-milestones.md` owns
  them as of PR #140; this work points at it.
- Changing the rolling log's own lookup key. `flow-measurement` keeps its
  meaning and its invariant.

## Two layers of label, because two audiences

| Label | Known to | Means |
|---|---|---|
| `flow-measurement` | the plugin | the rolling per-version log. **Exactly one open** — the invariant the roll and the skill both depend on |
| `flow-baseline` | the plugin | this repository's durable ledger, where a reading that spans versions goes. New |
| `measurement` | **this repository only** | the index across the whole concern, rolling and durable, open and closed. `.github/` is not shipped, so the script may name it |

The first two are the plugin's vocabulary and go in `skills/verify/SKILL.md`.
The third is this repository's and goes only in `.github/scripts/`, which
`tests/test_the_release_check_watches_what_ships.py` classifies as staying home.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A per-segment reading has one home | Given a smith or warden segment ends · When the session measures it · Then it posts to the open `flow-measurement` issue, as today | the skill's existing cases still pass |
| A cross-version reading has a different home | Given a reading that compares against a previous version's numbers · When the session writes it · Then the skill sends it to the `flow-baseline` issue | a case reads the section for both labels and the rule that separates them |
| A repository that never measured is still a no-op | Given no `flow-measurement` issue has ever existed · When a segment ends · Then nothing is measured, nothing fails, nothing asks | the existing no-op case, unchanged |
| A repository that stopped measuring is named | Given the label has issues but none open · When a segment ends · Then the session says the invariant is broken rather than passing over it | a case pins the distinction and the `--state all` lookup |
| A session does not repair it | Given either zero case · When the session responds · Then it opens no issue | a case pins the refusal and its reason |
| The next rolling log is born complete | Given a release reaches `main` · When the roll opens the next log · Then that issue carries a body linking the closed one and the durable ledger, the index label, and the `log:` milestone | `test_a_release_rolls_the_flow_measurement_issue.py`, extending `test_one_open_issue_closes_it_and_opens_the_next` |
| A missing milestone does not fail a release | Given the milestone has been renamed or deleted · When the roll runs · Then the issue is still created and its body says the milestone could not be set | a case with the milestone call failing |

## Data & interfaces

`open_issue(repo, version)` gains the body and two best-effort arguments. Its
return value is read by `main` for the failure message and must keep saying
what it says.

The body's shape, so a reader of the 0.9.0 log has a path in both directions:

```markdown
Rolls from #<the issue just closed>. Baselines and the observations that span
versions live in #<the durable ledger>; this issue takes one comment per
segment and is closed when <version> ships.
```

## Open questions → questions.md

One, answered in the batch before the first edit: a repository declares its
durable log with a **second label**. Recorded there with what the two
alternatives would have cost.
