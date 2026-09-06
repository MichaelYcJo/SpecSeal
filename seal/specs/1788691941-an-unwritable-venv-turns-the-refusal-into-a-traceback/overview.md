# 1788691941-an-unwritable-venv-turns-the-refusal-into-a-traceback — overview

📋 implement applied
· spec:     `seal/specs/1788691941-…/spec.md` (Grounding, Scope, all four scenarios), `plan.md` (phases, alternatives), `phases/phase-1.md`, `routing.md`; `CLAUDE.md` §*A ledger coordinate names content* and §*a change writes fragments, never the shared file*; `docs/review-chain-spec.md` §*The fix surface*; `templates/sdd-phase.md`, `templates/sdd-overview.md`; `seal/config.md` (no `Record language` row — English)
· evidence: `seal/ledger/1788691941-an-unwritable-venv-turns-the-refusal-into-a-traceback.md` R1 (the guard and its sentence) and R2 (the derived reach vocabulary), both stamped by the scoped `--reverify`; `seal/ledger.md` R2 and R8 of the `1788632199` section, each given the precondition it had left unstated, with R2's `hide_from_git` anchor re-stamped `63e2d9b9` → `08f18fc6`
· verified: **executed** — both reach cases seen red against a sixth value in `call_sites`' returnable set (`1 failed, 1 passed`) and green after the restore; six mutations over `reach_values` one at a time, one survivor found and closed, all six dead on the re-run with the killing case named; `./bin/test tests/test_the_fixes_name_their_surface.py -q` → 43 passed, exit 0; `./bin/evidence-check .` unscoped before and after, 3 drifted → 2; `uvx ruff check` and `uvx ruff format --check` on the changed test module, exit 0. **Round 1's fix pass, executed** — the four mutations that measure which reach case catches what, correcting the argument this memo carried; the four over-collection fixtures seen red against the blanket `Return` walk they replace; all ten arms of `handed_back` mutated one at a time and each dead; the remedy pin red against the superseded wording and the refusal pin red against the message it replaced; both modules 102 passed, exit 0. **Read** — R2's and R8's claims and every coordinate they cite; `call_sites`; the fix-surface section. **Unverified** — the table below

## Why this work exists

`bin/test` states in its own docstring that every failure it produces is a
sentence rather than a traceback, and a `.venv` the operator has made
read-only was the one case where that was false; the branch also repairs the
two ledger rows this path proved had left a precondition unstated.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether R2 is falsified or under-specified | `spec.md` §Scope names the row *whose guarantee is false on exactly this path*, which reads toward falsification; `plan.md` §Technical context says *the row is not removed… it gains the caveat* | Under-specified — the caveat in place, the new claims in the fragment | `CLAUDE.md` states the removal rule over the anchor: *a row whose anchor a change removes is REMOVED*. Nothing this branch touched was removed, and the claim is about the mechanism (owed to a function's exits, not to a list) rather than about an outcome. The outcome half had always depended on the write landing, and on that path the row was false BEFORE this branch too, in the worse way |
| Which of #177's two closings the vocabulary case takes | The issue's *Done when* offers either, without ranking them | The derived case, plus the residual limit recorded beside it | `CLAUDE.md`'s goal statement: *between two designs that catch the same defect, the one that stops to ask a person is the more expensive*. A written limit and a derivation do not catch the same defect — the limit stops nothing — so the tie-break does not apply and the one that refuses the commit wins. `RECORDED_LIMIT` in the same module is the house form for the other closing and states its own condition: it is for a domain that cannot be enumerated, and this one can |
| Whether the existing named case is replaced | `spec.md`'s fourth scenario reads *a case derived from the function's own returnable set*, singular | Both kept | Four mutations measure the split, and the first attempt at this row got it wrong (round 1's finding 1). Under a sixth value the derived case fails and the named one passes. With `only the first is a unit name` dropped from the section the named case fails and the derived one passes — that, not a rename, is what the named case uniquely holds. A rename and a reword redden BOTH, because the derived case's floor reads the same three constants by attribute name. Neither covers the other, on the first two rows only |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck — two modules were run, `tests/test_the_fixes_name_their_surface.py` and `tests/test_the_suite_has_a_command_that_is_cheap_twice.py`, and nothing broader (`agent-contract` §2) | the orchestrator, once, after the review rounds settle |
| `templates/config.md#"# Repository config"` and `skills/code-review/scripts/round_record.py#swallowed`, both DRIFTED in `seal/ledger.md`. Neither file is on this branch's diff, so both predate the branch base | the branch that edited each unit, or the 0.8.3 release preparation |
| the fixture case on `windows-latest` and on a root CI leg, where `chmod 555` does not stop the write and the case skips rather than runs — the platform-independent case is what covers those legs | CI at the pull request |

## Not done

**The `.venv` is not made writable and the ignore is not written another
way.** A read-only virtualenv is the operator's; the runner says what it could
not do and carries on. Writing the rule into the repository's own `.gitignore`
instead was considered in `plan.md` and refused for the reason R2 records:
keeping the rule inside the directory is what makes removing the virtualenv
remove the rule with it.

**The derivation is not extended across function boundaries.** A reach value
another function hands back, or one formatted at run time, is outside what
`reach_values` reads. Closing that means resolving calls, which is the
unbounded enumeration `RECORDED_LIMIT` declines in the same module. The limit
is recorded in `reach_values`' docstring and **executed** rather than only
stated: two of the derivation fixtures are its two sides, and whoever closes
it will find the second of them red.

**`docs/review-chain-spec.md` was not edited.** The section is correct today —
that is why nothing shipped broken — and leaving it alone is also what keeps
R8's document anchor from drifting for a change that adds no value to it.

**The three other 0.8.3 rows 0.8.2's work opened — #175, #180, #182 — are not
written into `docs/flow.md`.** Each is another branch's to write, and the
release-preparation commit picks up whatever is left.

## Fed back into the spec

**R8's claim was narrowed, and that is a correction rather than an
addition** — *the document cannot drift from the generator* was true of a
rename and a reword and never of an addition, so it now says *those three*
and points at the row that carries the wider claim. Marked here as inferred
during implementation: a planner may overturn it by deciding the two cases
should be one.

Nothing was added to `spec.md`. Its fourth scenario offered both closings, and
taking one of them is the judgment it asked for rather than a clause it was
missing.
