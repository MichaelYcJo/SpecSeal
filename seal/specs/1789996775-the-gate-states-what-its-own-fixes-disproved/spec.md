# Feature Specification: the gate states what its own fixes disproved

<!-- seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/spec.md
— WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Three sets of standing statements, all left open when #423 capped before it
could spend them as reopenings: #461, #464 and #465. Not one of them changes
what the gate does. Every one of them makes a reader believe something the
same work item measured to be false.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `skills/agent-contract/SKILL.md` §4 — *Label what was executed apart from what was read* | The rule #464's second half is about. A claim stated as flatly as a measured one, with no label and no answerer, reads as measured |
| `skills/agent-contract/SKILL.md` §12 — *A defect belongs to a class — enumerate the class* | Why S4 reaches `CHANGELOG.md` as a question rather than stopping at the three files #464 lists. The same sentence stands in a fourth place, and the three preceding rounds each fixed one coordinate of a claim that had more |
| `skills/agent-contract/SKILL.md` §14 — *A fix that changes what a person sees documents it and pins it* | `moved_line`'s printed text is read by a sealer and quoted into a report (`agents/sealer.md`). A2 changes it, so A2 owes a case that pins the new text |
| `skills/agent-contract/SKILL.md` §15 — *A new case is not planted until it has been seen red* | Every case this work plants is shown failing first — against the code as it stands, or with the sentence it pins deleted |
| `CLAUDE.md` §*A change writes fragments, never the shared file* — *Appended is the word, and a removal is not one* | Why this branch may touch `seal/ledger.md` at all. A branch that leaves an existing row's claim false must repair it there; new claims go in this work item's own fragment |
| `CONTRIBUTING.md` §*House rules* — *One branch does edit `CHANGELOG.md`, and it is the one based on `main`* | The clause that pulls the other way from §12 for `CHANGELOG.md` §0.12.2, and the reason S4 is a person's question rather than a decided criterion |
| `docs/one-root-by-lifetime.md` §*The dependency rule* | Why a correction made only inside `seal/specs/<id>/` does not outlive the release: `settle` folds and removes that directory, and it is treated as already gone for every permanent purpose |
| `skills/implement/SKILL.md` §*Document layout — two roots, three lifetimes* | The distinction A5 rests on. A round record carries the SHA it reviewed, so it asserts a PAST state; a `spec.md` clause, a `plan.md` row and an `overview.md` line assert a present one |

## Scope

### In

1. **#461 — `skills/verify/scripts/broad_gate.py#names_a_branch`'s docstring
   names a class the command does not refuse**, and the one spelling that
   slips through makes `moved_line` quote a ref nothing reads. The docstring
   first (A1); then the printed line (A2).
2. **#464 — two statements the same work item's fixes disproved.** The
   `panel` docstring's leading argument and its elision grounds (A3); the
   `spec.md` `seal_stamp.letter` row that repeats the retired reasoning (A5);
   and the missing evidence label on the baseline half of the direction claim
   (A4).
3. **#465 — three statements in
   `tests/test_the_gate_asks_the_range_ci_will_ask.py` say the branch left
   `tests/test_the_seal_is_taken_once_by_the_sealer.py` byte-identical**, and
   the branch changed it (A6).
4. **The evidence rows this work drifts or falsifies** (A7): `moved_line` and
   `panel` are ledger anchors, and R4's claim is one of the statements #461
   disproves.

### Explicitly out

- **Hand-rolling a pattern in place of `git check-ref-format`.** #461's own
  *Not this*, and round 1's finding 6 already replaced exactly that with
  git's answer after a hand-written guard moved the defect one step down to
  `origin/HEAD`.
- **Weakening A3 of `seal/specs/1789956662-…/spec.md`.** #465's *Not this*.
  That clause is right; the three comments are what drifted from it. A6 is a
  correction to the comments and touches no `spec.md` acceptance row.
- **The round records and phase records of work item 1789956662** —
  `rounds/round-N.md`, `rounds/round-N-report.md`, `phases/phase-N.md`. A5
  says why, and it is not an omission: those files assert a past state at a
  named SHA, they are the audit trail every correction this work writes
  cites, and `phases/phase-1.md`'s superseded reading is excused on the
  record by round 3's finding 15 — *`phases/phase-2.md` records the
  divergence in the next record along, which is how a phase record is meant
  to be read in sequence*.
- **`CHANGELOG.md` §0.12.2, unless Q1 is answered otherwise.** S4 is the
  question and A4 states what happens under its default.
- **The two em-dash clauses round 2's finding 10 noticed in `moved_line`'s
  second filling.** #461 does not ask for it, and A2 pins printed text; a
  prose sweep of a line under a pin is a separate edit with its own case. If
  the wording A2 chooses happens to leave one clause where there were two,
  that is A2's own text and not a second change.
- **Behaviour.** Nothing in this work item changes an exit code, a verdict or
  a resolution — with one bounded exception, A2, which changes one printed
  sentence for one input spelling and changes no exit code.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| A1 | Given `names_a_branch`'s docstring, when a reader asks which spellings the guard refuses, then it states the property `git check-ref-format --branch` actually has — it EXPANDS `@{-N}` and then checks, so `@{-1}` is accepted while `HEAD`, `HEAD~1`, `base@{u}` and `topic@{1}` are refused — and no sentence in it claims the class `@{…}` | The docstring names the accepted spelling explicitly; a probe over the five spellings of round 2's finding 10 confirms the stated property before it is written (Q2) |
| A2 | Given `--base @{-1}` in a checkout where it resolves, when `moved_line` prints, then the line does not name `origin/@{-1}` — or any other ref a runner's checkout cannot have — as the ref a runner reads; and the property is asked of git rather than of a pattern written in this file | A case driving `moved_line` with a given spelling no full refname can hold, seen red against the code as it stands (the current output quoted in round 2's finding 10 is the red), green after. §14: the new sentence is pinned by that case |
| A3 | Given `panel`'s docstring, when a reader takes its first paragraph, then they meet what is true now rather than the argument `phases/phase-3.md` records as *about a state that no longer arises*; and the elision's stated grounds no longer assume the dropped prefix is always `origin/` | Read against `phases/phase-3.md`'s CORRECTED comment and round 1's finding 2. No behaviour moves, so the check is that `panel`'s rows and rendering are unchanged — the existing case over `panel` and the rendered stdout stays green |
| A4 | Given the baseline half of the direction claim — *the two baselines move the same way, a baseline carried forward drops the rows the base's own newer commits added* — when it is stated in `seal/specs/1789956662-…/changelog.md`, `plan.md` §*Operational impact* and `overview.md`, then it carries an evidence label saying it was **read, not executed**, and names who answers it | Each of the three sites carries the label beside that clause. The measured half keeps no label it did not have. `seal/ledger.md`'s R3 row already labels the measured half `Executed` and is the shape to match. Under Q1's default `CHANGELOG.md` §0.12.2 keeps the unlabelled copy, and that divergence is a row of this work item's `overview.md` §*Not verified* naming the repository owner |
| A5 | Given a false or retired statement in work item 1789956662's `spec.md`, `plan.md`, `overview.md` or `changelog.md`, when this work corrects it, then it is corrected IN PLACE and never deleted silently, and an HTML-comment marker beside it quotes what stood there, says what disproved it with the coordinate, and names this work item and the issue | The marker's shape is fixed below and is the one `phases/phase-3.md`:34 and `phases/phase-4.md`:38 already use inside that same work item. Grep the four files for `CORRECTED` and confirm one marker per corrected statement; grep the four files for the corrected sentences and confirm none was deleted without one |
| A6 | Given `tests/test_the_gate_asks_the_range_ci_will_ask.py`, when a reader asks at `:19`, `:68` or `:377` what the fallback kept, then all three say what the branch did — the fallback leaves a remote-less repository resolving to the ref as given, and ONE assertion in `tests/test_the_seal_is_taken_once_by_the_sealer.py` moved because the `Broad gate` cell's base half now carries the commit | The three replacements are round 3's finding 15, paste-ready. `grep -n "byte-identical\|exactly as it did\|reading as it did"` over the module returns nothing that still claims the module was untouched. The module stays green |
| A7 | Given the evidence rows this work drifts, when the work item closes, then `seal/ledger.md`'s R4 and R5 of work item 1789956662 are re-read and re-stamped with a `Re-read <date>` note naming this work item; and R4, whose claim *it never says CI reads a ref CI does not read* is one of the statements #461 disproves, additionally carries a `Corrected <date>` marker saying it was verified as true when it was not, and what A2 changed to make it so | `evidence-check --reverify .` recomputes the hashes and names what it changed; `bin/evidence-check` reports 0 broken. New claims go in `seal/ledger/1789996775-the-gate-states-what-its-own-fixes-disproved.md`, never appended to `seal/ledger.md`. **Every row citing a drifted coordinate is read by hand BEFORE `--reverify` runs** — `seal/follow-up.md` measured that the drift report names a coordinate once while `--reverify` re-stamps every row that cites it, so the documented repair writes *somebody read this* over rows nobody opened. Counted in the tree: `moved_line` is cited by one row (R4), `panel` by two — R5 of work item 1789956662 and G6 of work item 1789985781 (#468) — and `names_a_branch` by none |
| A8 | Given any of A1–A7, when the run finishes, then no exit code, verdict or resolution has moved — the one printed sentence A2 changes excepted | The existing suite for `broad_gate.py` and both test modules stay green with nothing excused |

### The correction marker, stated so `smith` does not have to invent one

A5's marker sits immediately after the statement it is about, and it reads:

```markdown
<!-- CORRECTED <date> by work item 1789996775 (#<issue>). What stood here:
"<the sentence, quoted>". It is false because <what disproved it, with the
coordinate>. Corrected in place with the issue named, never deleted silently:
a record of a past state that quietly becomes true is a record nobody can
audit. -->
```

Two things about it are deliberate and neither is decoration.

**The verb is `CORRECTED`, uppercase**, because that is the spelling the two
phase records of work item 1789956662 already use and because the shared
ledger's marker is `Corrected <date>` in sentence case. A grep for one must
not return the other: `correction-check` reads the ledger's spelling, over
ledger files alone, and an SDD record wearing the same token would read as a
ledger marker to a person running that grep by hand — which is the only way
the #424 incident was ever caught.

**It names this work item and the issue, not a round and a finding.** The
phase records could name a round because the round was theirs. A later work
item correcting a shipped record has no round of its own to point at, so the
pointer has to be the id and the issue number.

## Data & interfaces

No schema, no endpoint, no payload. The surfaces this work touches, with the
evidence coordinate where one exists:

| Surface | What moves | Ledger anchor |
|---|---|---|
| `skills/verify/scripts/broad_gate.py#names_a_branch` | docstring only (A1) | none — this unit is not a ledger anchor, so A1 drifts nothing |
| `skills/verify/scripts/broad_gate.py#moved_line` | one printed sentence for one input class, plus its paragraph (A2) | `skills/verify/scripts/broad_gate.py#moved_line@91a38149`, R4 of work item 1789956662 — re-stamped by this work's own `--reverify`, from `@f312f19b` |
| `skills/verify/scripts/broad_gate.py#panel` | docstring only (A3) | `skills/verify/scripts/broad_gate.py#panel@ea0e48ac`, R5 of the same — re-stamped twice by this work's own `--reverify`, from e2c844e8 through 1f0f969d |
| `tests/test_the_gate_asks_the_range_ci_will_ask.py` `:19`, `:68`, `:377` | three comments (A6) | none — the module's two anchored units, `test_the_survivor_arm_reports_what_ci_reports` and `test_the_gate_reaches_for_the_spelling_the_workflow_uses`, contain none of the three sites |
| `seal/specs/1789956662-…/spec.md` §*Affected surfaces*, `seal_stamp.py#letter` row | the retired reasoning (A5) | none |
| `seal/specs/1789956662-…/plan.md` §*Operational impact*, `overview.md`, `changelog.md` | the missing evidence label (A4, A5) | none |
| `seal/ledger.md`, R4 and R5 of work item 1789956662 | re-read, and R4 corrected (A7) | the rows themselves |
| `seal/ledger/1789996775-….md` | this work item's own new rows | new fragment |

## Open questions → questions.md

Four rows, and one of them is a person's. `questions.md` also lists, at its
head, the judgments the three tickets left open that the tree answered — so
nobody reopens them.

Framed 2026-09-21 by framer, before the build.
