# 1788700685-two-value-shaped-odd-rows-end-the-report — overview

📋 implement applied
· spec:     `seal/specs/1788700685-.../spec.md` (Grounding, Scope, all four acceptance rows), `plan.md` (Technical context, Alternatives, Phases), `phases/phase-1.md`, `CLAUDE.md` (the ledger-coordinate rules, the fragment rule, the merge-method table), `skills/implement/SKILL.md` §§1–4, `skills/agent-contract/SKILL.md` §§1–5, §7, §9, §12, §15, `seal/config.md` (no `Record language` row → English), `seal/follow-up.md`
· evidence: `seal/ledger/1788700685-two-value-shaped-odd-rows-end-the-report.md` — R1 the normalisation at `parse_time`, R2 the non-positive-span guard at `share`, R3 the enumeration's two axes and its one open member. `seal/ledger.md`'s R6 corrected in place (the axis named) and its `count` and `parse_time` anchors re-stamped; R1's `count` anchor re-stamped
· verified: **executed** — the probe against the pre-fix module (deleted after one run), `./bin/evidence-check .` unscoped before and after, `--reverify` scoped to this work item's fragment, `tests/test_session_cost.py`, `tests/test_a_rider_reaches_its_file.py`, `tests/test_release_hygiene.py`, `tests/test_the_rules_have_one_owner.py`, `tests/test_the_set_a_work_item_always_has.py`, `tests/test_unverified_rows_close.py`. **read** — `seal/ledger.md`'s R6 as written at 0.8.2, `docs/flow.md`'s 0.8.3 section. **unverified** — the full suite, lint and typecheck; see the table below

## Why this work exists

Two operands a transcript can carry ended `session_cost`'s report, and the
ledger row that already claimed no operand could was stating its guarantee one
axis wider than the enumeration behind it — so the next editor reading *no
member survived* would have taken a closed class for granted.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the naive stamp raises | `spec.md` §Scope: *"a transcript mixing a zone-aware stamp with a naive one, so **`analyse`'s subtractions** raise `TypeError`"*. `plan.md` §Technical context: *"`session_cost.py#analyse` — `(calls[-1]["end"] - calls[0]["start"])`, the per-call sum, the turn gap and the family sum: four subtractions, one class"*. The code: a two-call transcript raises in `load`'s `calls.sort`, **before `analyse` is entered** | The implementation, and the record corrected | Measured twice — phase 1 at `load:210` against `analyse:224`, and phase 2 against the module at `6863669`: a one-call transcript exits 1 with `TypeError: can't subtract offset-naive and offset-aware datetimes`, a two-call one with `TypeError: can't **compare** offset-naive and offset-aware datetimes`. The two documents follow #175's own framing. Nothing was rewritten to match them: the fix is at `parse_time`, which closes both the subtractions and the orderings, and a guard written where the documents point would have left the commoner shape standing. `seal/ledger/1788700685-….md` R1 states the site |
| How many sites there are | `plan.md` §Technical context: *"four subtractions, one class"* and *"`data['command_s'] / data['span_s']`, and **three more divisions** by the same denominator, including the `idle > data['span_s'] * 0.1` guard"* — four of each. The code: **six** subtractions plus **two orderings**, and **three** divisions | The implementation, and the record corrected | An AST walk over the module returned 56 arithmetic and ordering sites and classified each; the two the subtraction list missed are the `exact`/`stripped` duration and `slowest`'s, and the orderings are `load`'s `calls.sort` and `analyse`'s `max(turn_end, …)`. The fourth division the plan counted is `idle > span_s * 0.1`, a multiplication, safe at zero — which is also why the early draft's second guard on the idle block was removed before phase 1's commit: at a span of zero `0 > 0` is already false. `phases/phase-1.md` §*The enumeration* carries the walk; `plan.md` is left as approved, since it is the contract this work executed against rather than a description of the result |
| Whether #170's row is falsified | The task framing offers *falsified (a removal, per this repository's rule)* or *under-specified (the axis named in place)*, and #175 reads the row as claiming a class it does not close | Under-specified — corrected in place | Three tests, each measured. The anchors: `evidence-check` unscoped reports 0 broken and every anchor R6 cites resolves, so the removal rule — which fires when a change takes an anchor's code out of the tree — does not apply. The mechanism: the four funnels still type-check and phase 1 ADDED to two of them. The reach: R6's own Verified cell records its construction as fields × seven JSON types × absent, and against the module it was stamped against all eight variants of the `timestamp` field exit 0 while a naive stamp and a zero span exit 1 — so the two shapes are outside the cross product by construction rather than members it missed. The useful half of the row is the method, which is what phase 1 re-ran to find these two; deleting the row would have taken its own reproduction instructions with it |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck. `agent-contract` §2 reserves the broad gate; this work item ran the modules it touched, and the orchestrator ran `uvx ruff check` and `uvx ruff format --check` on phase 1's two changed files at `e8ef34d`. Phase 2 changed no Python file, so it ran neither | the orchestrator, once the review rounds settle |
| Whether `templates/config.md#"# Repository config"` and `skills/code-review/scripts/round_record.py#swallowed` still state true claims. Both were already DRIFTED at this branch's base — the first unscoped run at `e8ef34d` carries them, and phase 1's only code commit touches neither file — so re-verifying them is a re-reading this work item did not do and must not stamp on someone else's behalf | the orchestrator, or the branch whose edits drifted them |
| Whether any transcript-derived operand reaches an arithmetic site through a path neither axis of the enumeration covers. Both axes were closed mechanically — an AST walk for the operations, the readers' own field surface for the values — but a field added to `load` or `token_totals` later is outside both until the walk is re-run | whoever next adds a field to either reader; `seal/ledger/1788700685-….md` R3 carries the method |

## Not done

**`NaN` and `Infinity` in a `usage` field were deferred, and round 1 showed
the deferral rested on a false measurement.** The reasoning was that they
print `nan` and exit 0, so `spec.md` §Scope — operands that END the report —
put them outside this work item. The reading behind it was taken on
`output_tokens`, which is the one usage field that never reaches
`token_thirds`, where `round()` raises on a non-finite float. Every other
usage field ends the report with exit 1 and stdout empty, on both arms, which
is worse than either shape the work item was opened for and inside its own In
criterion. Closed at `count` with `math.isfinite`, the rider's own prescribed
one-liner; the rider is gone with it, because a rider that has been acted on
is spent. The deferral is kept in `phases/phase-1.md` as written, with the
correction above it: how a single measurement was read as a class is the
finding, and deleting the reasoning would delete it.

**`plan.md`'s Technical context is left as approved.** Its two counts are wrong
and the divergence table says so with both sides quoted. It is the contract
this work executed against, and editing a contract after the fact to match the
result is the one thing that makes an approval unreadable later.

**`docs/flow.md` gains the row for #175 alone.** #180 and #182 are other
branches' rows to write, and a session writing another branch's line into a
shared file is the collision the fragment convention exists to prevent.

## Fed back into the spec

**One clause, inferred during implementation, and it lives in the ledger rather
than in `spec.md`.** `seal/ledger/1788700685-….md` R3 states the class as
enumerable on two independent axes — the operations, closed by an AST walk over
the module, and the values that can enter, closed by the two readers' own field
surface — each decomposing into the type a value carries and the value it
carries within that type. `spec.md` names the two axes in its Grounding but not
the decomposition, which is what made the third shape findable and what a later
planner may overturn.
