# Feature Specification: the refusal text is unobserved and an uppercase V is invisible

<!-- seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CONTRIBUTING.md` §"What a change to a gate must carry" | this branch edits a gate — the version check — so the widening has to be argued where it is declared, not only in a commit message |
| `docs/issues-and-milestones.md` §"A rolling log is titled after the version it rolled from" | the paragraph #206 corrects; it is also the paragraph the check's own message points an author at |
| `skills/agent-contract/SKILL.md` §15 | every case here is seen red before it is committed as a case |
| `seal/README.md` — a coordinate names content, never a position | the two ledger corrections are made in place; no row is re-pointed |

## Scope

**In.** `tests/test_release_hygiene.py` and the records that describe it:

- #203 — a case that reads what `refusal` returns and pins all seven of its
  elements, plus the correction of the neighbouring docstring and of the
  `seal/ledger.md` R3 note, both of which state a false limit as measured fact.
- #204 — the argument for `VERSION_TOKEN`'s leading `(?<![\w.])`, both
  characters, written beside the constant; then `v?` widened to `[vV]?`.
- #205 — "or a narrower prefix" deleted from one case docstring and from the
  `seal/ledger.md` R1 note, replaced by the reason it was never true.
- #206 — one sentence in `docs/issues-and-milestones.md`, so the three
  documents naming the check agree.

> **Corrected by review round 1 — two counts in the list above came from a
> reading of the source rather than from the source, and the scope they
> describe is unchanged.** `refusal` has **six** elements, not seven:
> `ast.parse` flattens the returned `+` chain to four operands whose first is
> one `JoinedStr` of three parts. And **two** documents state what the check
> refuses, not three — `docs/flow.md:30` describes the equality check #179
> replaced, so it names the ticket rather than the check.

**Out.**

- `docs/release-checklist.md` and `docs/flow.md`. Both state the rule
  correctly and are not to be "fixed".
- Any narrowing of either lookaround (#204 says so explicitly: round 1's
  finding was a lookaround narrowed for one shape taking another with it).
- Any assertion for #205's arrangement. Asserting an arrangement that changes
  no answer is the failure that ticket is about.
- `is_a_record_of_a_moment`'s own docstring, which says *an exact path* and is
  correct.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A refusal loses the file it refused | Given `refusal` builds its four pieces / When the offender join is deleted / Then a case goes red | delete it, run the module, see red |
| A refusal loses the version it is measured against | When the `{running}` interpolation is deleted / Then a case goes red | same |
| A refusal loses the reason | When the timer paragraph is deleted / Then a case goes red | same |
| A refusal loses a separator | When any one of the three separators is deleted / Then a case goes red, one per separator | three mutations, each on its own |
| This plugin's version in an uppercase spelling | Given a loaded file writes `V0.9.0` / When the check runs / Then it is refused and printed as written | `timers_in` fixture |
| A composite identifier keeps working | Given `py3.13.9`, `x0.9.0`, `PyV0.9.0` / When the check runs / Then none is refused | `timers_in` fixtures |
| The widening refuses nothing new in the tree | When the check runs over the loaded set / Then the offender list is unchanged | run the whole check, before and after |
| A reader learns what the check refuses | Given `docs/issues-and-milestones.md` / When they read the paragraph / Then it says at-or-above and that below is kept | read the three documents together |

## Data & interfaces

No schema, no interface. Two constants and one message builder in
`tests/test_release_hygiene.py`; the coordinates are in
`seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md`.

`VERSION_TOKEN` is the only behaviour change: `v?` → `[vV]?`, with both
lookarounds untouched.

## Open questions → questions.md

The routing batch was answered before this work item was spawned, and each
ticket carries its own *What would close it*. What surfaced during the work is
in `questions.md` with an answerer named.
