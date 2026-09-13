# 1789296100-the-seal-and-ci-read-one-ledger-differently — overview

📋 implement applied
· spec:     `spec.md`, `plan.md`, `questions.md` and `routing.md` in this directory · `CLAUDE.md` §*The goal a design is chosen against*, §*a change writes fragments, never the shared file*, §*a thing more than one party can have is named with whose* · `CONTRIBUTING.md` §*What a change to a gate must carry* · `skills/agent-contract/SKILL.md` §§1, 2, 4, 9, 12, 14, 15 · `skills/implement/SKILL.md` §§2–4 · `agents/sealer.md` §*The one run*
· evidence: four rows in `seal/ledger/1789296100-the-seal-and-ci-read-one-ledger-differently.md` — the notice, the grading unit, the gate's ledger call site, and the five documents. Seven existing `seal/ledger.md` rows re-read and re-verified, their claims unchanged
· verified: executed — the new module, the three ledger modules, the wrapper-pair and document modules, three mutations, and the CI `ledger` step's own shell body over a drifted fixture. Read, not executed — `hooks/evidence-advisor.py`'s silence on drift. Unverified — the full suite, the repository-wide lint and the typecheck; see *Not verified*

## Why this work exists

Three readers of one exit code ran one checker over one tree and graded it
differently, and
nothing said so — a session that ran the documented command and read exit 1
had no way to learn that `broad-gate` reads the same tree as a refusal. Now
the run that is lenient says which reading you took.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The structural case's coordinate for the gate's ledger call | `spec.md` and `plan.md` both cite `skills/verify/scripts/broad_gate.py:570` | the case walks from `checks[LEDGER]` until the parentheses balance and never reads a line number | `CLAUDE.md` §*commit early*: *a ledger coordinate names content, never a position*. A case pinned to line 570 would go red for a reformatting that has nothing to do with the flag. The documents keep the line number, which is what a reader opens; the case does not, which is what a checker measures |
| Where `overview.md` is opened | `plan.md` phase 4 lists it among the closing records | opened in phase 3 | `tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview` was already red on this branch from the framer's own commit (`17164d7`), which wrote `spec.md` with no memo beside it. Waiting until phase 4 would have left an existing case red across the review rounds. **This is not this work item's scheduling, which is how the row read until round 1 corrected it — it is a class, and it is now #379.** `agents/framer.md` tells the framer to write `spec.md`, `plan.md` and `questions.md` and *nothing else — not `overview.md`*, while that case fails the moment a directory holds a spec or a plan without a memo beside it. The two cannot both be satisfied, so every framed work item is red from its framer commit until whichever phase opens the memo. Executed: all three framer commits of this release wrote exactly the three files and no memo — `17164d7` (#354), `81be6ac` (#345), `332c656` (#350) — and `feat/350-a-segments-own-wall-clock-is-in-no-column` was still red on it at its tip during round 1. Which side gives is the owner's call and #379 is where it is asked; moving the memo earlier is a work-around this branch keeps |
| Whether `seal/ledger.md` is touched | `spec.md` S8 and `plan.md` phase 4 both say the shared ledger is untouched; seven of its rows were re-read, re-stamped and re-dated | touched, and the rows re-verified in place | This work's edits changed content under seven anchors that file cites. `broad-gate` passes `--strict`, so leaving them drifted is exit 2 and a branch that comes back refused. `CLAUDE.md` §*a change writes fragments* forbids APPENDING and carves out removal; re-verification is the third case and it is what leaves the ledger true. Not one row was appended — the new claims are all in this work item's own fragment. Phase 4's verification row reads *`CHANGELOG.md` is not in it*, narrowing `git diff --stat` to one of the two files S8 names without saying it had narrowed, which is where S8's other half went quiet. Added in round 1's fix pass; the grounds were in `phases/phase-4.md` and not in the table a later session opens |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the sealer, once the review rounds settle — `agent-contract` §2 keeps the broad gate out of this segment's hands |
| `hooks/evidence-advisor.py`'s behaviour on a drifted tree — read from its docstring and its `status in ("BROKEN", "OLD-FORMAT")` filter, never run | the review chain, or a later work item. It is the fourth reader and the only one this change does not touch; nothing here alters it, so the risk is that the reader count in `spec.md` is wrong rather than that behaviour moved |
| `broad-gate`'s own end-to-end run against this branch, showing the sentence absent at exit 2 in the gate's real invocation rather than in a fixture | the sealer. The fixture case covers the grading; only the gate's own run covers the wiring |

## Not done

**`bin/evidence-check` and `bin/evidence-check.cmd` were left alone** beyond
nothing at all — not even the usage comment `plan.md` allowed. The wrapper's
header already shows `evidence-check . --strict` as a form a reader can type,
and the fact about who passes that flag now arrives in the output of every run
that needs it. Adding it to the POSIX header and not the `.cmd` sibling would
be exactly the surviving wording `survivor-check` reports; adding it to both
duplicates a sentence that is already printed.

**The malformed-coordinate row in `seal/follow-up.md` was left** — a row whose
hash does not parse produces no row at all. `spec.md` scopes it out, it is a
different defect in the same file, and it needs a judgment the owner has not
given.

**The class was enumerated and one member fixed.** `spec.md`'s five-row table
over `broad_gate.py`'s own call list is the enumeration, and the chain check's
draft/ready mirror at #4 has the shape without the defect. Nothing was done
about a sixth call site that does not exist yet.

## Fed back into the spec

Two corrections, both made in round 1's fix pass and both *inferred during
implementation* — a planner may overturn either.

| Clause | What changed |
|---|---|
| §*Data & interfaces*, the coordinates this work builds on | `skills/verify/scripts/broad_gate.py#main` → `#gate`. Phase 4 found the ledger call site in `gate` (516-641) and not in `main` (644-678) and recorded it in the fragment's Notes cell; the contract itself went on naming the wrong unit, so a reader who opened it had to open two other files to get the right one |
| The opening paragraph's reader count | *Three readers* → *three readers of one exit code*. `spec.md` §*The class* already said a session counting readers gets four; the opening said three, which is the same divergence round 1 found across three shipped documents, one file in |

No new clause was added. Q1 was answered by the owner before the build started
and the wording shipped as answered; Q2 and Q3 were closed by measurement
inside the phases they belonged to, and their answers are in `questions.md` and
in the phase records.
