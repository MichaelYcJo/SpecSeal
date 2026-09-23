# 1790154760-the-ledger-grows-and-nothing-takes-a-row-out — overview

📋 implement applied
· spec:     `spec.md` (Grounding, Measurements §1–§3, Scope, scenarios), `plan.md` (Technical context, Alternatives, Phases), `questions.md` Q1–Q4, `routing.md`; `docs/the-evidence-ledger.md` §*A bound over the corpus is stated with its instrument and the moment it was taken*; `CLAUDE.md` §*a change writes fragments, never the shared file*
· evidence: `seal/ledger/1790154760-the-ledger-grows-and-nothing-takes-a-row-out.md` C1, C2 added; `seal/ledger.md` rows on `py_spans` and on `scan_candidates` (two) re-read, marked `Re-read 2026-09-23` and re-verified
· verified: executed — the three new cases red then green, four mutants red, the before/after timings and output diffs in `phases/phase-1.md`, `--strict .` exit 0, the phase slices; read — the callers of `py_spans` for Q2

## Why this work exists

Every `git commit` here waited about 15 s on the evidence advisor because the
checker parsed a file once per ledger row; it now parses each file once, and a
commit waits about 1.7 s.

## #519's three questions, and the measurement that answers each

- **Is the ledger's size a cost?** Yes, and at every commit: 15.2–15.4 s in
  the advisor before, 1.73–1.77 s after (`phases/phase-1.md`). The cost was
  the parsing and not the rows: 1,328 parses of 126 files (`spec.md` §2).
- **Is any row dead?** No. All 1,482 anchors resolve, this work's six included, and none drifts
  (`evidence_check.py --strict .`, exit 0 at this branch's head), and no rule
  lets a row leave except with its code (`spec.md` §1).
- **Do the release sections repeat `docs/`?** Mostly not: median Clause word
  overlap 0.21 with the folded prose (`spec.md` §3).

So the work took no row out. `questions.md` Q1 (close #519 or keep it open
for a retirement rule argued on other grounds) is a person's, and the build
took its default: the pull request closes #519.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| What stays identical | `spec.md` scenario 1: the advisor "prints exactly what it printed before". Stdout, exit code and every finding are identical. Stderr differs in one way: Python prints a `SyntaxWarning` at each parse of a source that raises one, so the BROKEN path's repo-wide scan printed the warning for `tests/test_a_row_points_by_content.py` 143 times in the perturbed run before and once after | the memo, with the collapsed warning | The warning is Python's, about a test file's docstring escape, and is not a finding; `spec.md` Scope item 1 says "Every finding the checker prints stays byte-identical", which holds. The clean path, which is what a commit runs, prints nothing on stderr before or after |
| Copy or share the memo's answer | `plan.md`: return the cached object if phase 1's read finds no mutating caller, else a copy or an immutable value. The read found none | a fresh dict of fresh lists per call | It costs 0.155 s of internal time under the profiler for 1,334 calls, and without it the first future caller that mutates rewrites every later answer for that text, silently. A case pins it. A tuple freeze of the stored value was built and removed, because no case could tell it was there |
| How many places carried "114 ms" | `spec.md` Scope item 2 names the advisor's docstring. `evidence_check.py#scan_candidates`'s docstring and one test's docstring stated the same number | all three corrected, and in round 1's fix pass two more | One stale fact written three times (`agent-contract` §12). The advisor carries the measurement; the other two now state the property ("the clean path pays nothing for it") without a number to go stale. **Corrected 2026-09-23** in round 1's fix pass: the class was enumerated by one literal. Enumerated by what it says, a stated cost of the check or its hooks, `hooks/ledger-migrate.py` and `skills/evidence-check/SKILL.md` were two more; both now carry a measurement re-taken with its instrument and date (ledger row C3) |
| A stamp in the framer's `spec.md` | `spec.md` Scope item 4 wrote the `py_spans` row's framing-time anchor in anchor shape. The records arm of `--strict` reads a stamp in any record of a work item that has a ledger fragment, so the moment this work wrote its fragment the sentence read BROKEN (a short path, and a hash this work changes on purpose), exit 2 | the sentence keeps its words and its hash, written as "the `evidence_check.py#py_spans` row (hash `4045ba55` at framing)", which the records arm does not read as a stamp; the same in `phases/phase-2.md` | The stamp stated a past state, which is what the sentence meant, and the tree has to pass the check CI runs. `spec.md` is the framer's file, so this is disclosed here and in the hand-back rather than made silently |
| A `SyntaxWarning` on every `--strict` run | The records arm resolves names this work's records give in `tests/test_a_row_points_by_content.py`, whose `test_an_old_format_ledger_is_loud_never_invisible` docstring held a `` \` `` escape Python warns about. That put one warning on stderr of every `--strict` run of this tree | the docstring is raw (`r"""`), which keeps its value byte for byte and ends the warning. `--strict .` prints nothing on stderr again | `spec.md` Scope keeps the checker's output unchanged, and the warning was this work's records surfacing a defect that predates them |
| Where the one-broken-anchor diff was taken | `spec.md` scenario 1: diff the advisor's output on a tree with one broken anchor | the advisor's own `failing_rows`, in process, on a scratch `seal/` home holding a copy of `seal/ledger.md` with one anchor renamed; identical rows before and after | `main` turns those rows into lines with code this work did not touch, and a scratch home kept the worktree's ledger clean |

## Not verified

| Item | Who must answer |
|---|---|
| Q1: whether #519 closes with this work or stays open for a row-retirement rule; the build took the default, close | the repository owner |
| The full suite, the repository-wide lint and format check, and the broad gate on this branch | the sealer, spawned by the orchestrator after the review rounds settle |
| The `ledger` CI job's and `broad_gate.py`'s `LEDGER` check's wall time on Linux after the change; every timing here was taken on macOS | the orchestrator, reading the pull request's CI run |

## Not done

What the remaining 2 s goes to is recorded and not acted on: the 126 parses
that remain are about half of it, and splitting each file's text once per row
is the next largest (`phases/phase-1.md`). `spec.md` puts both out of scope,
and a later item can start from those numbers.

Posting the before/after numbers to the `flow-measurement` issue and to #51 is
the orchestrator's act, not the build's (`plan.md` §Operational impact).

## Fed back into the spec

none
