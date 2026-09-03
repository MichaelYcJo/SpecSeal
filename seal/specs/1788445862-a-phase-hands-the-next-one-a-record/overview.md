# a phase hands the next one a record — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     `docs/review-handoff-protocol.md` §Files, §Non-goals · `CONTRIBUTING.md`
  §What a change to a gate must carry · `skills/implement/SKILL.md` §3 The SDD
  file set, §Document layout, §The language the records are written in ·
  `spec.md`, `plan.md`, `questions.md`, `phases/phase-1.md`,
  `phases/phase-2.md`, `phases/phase-3.md`, `routing.md` (all read in full) ·
  `templates/sdd-phase.md`, `templates/sdd-round.md`, `templates/ledger.md`,
  `templates/sdd-overview.md` · `agents/smith.md` phase 3 · `skills/code-review/SKILL.md`
  Cross-session records · `seal/follow-up.md` (read in full — its one open row
  is unrelated, per plan.md's own Technical Context) · `docs/branch-and-release.md`
  (fragment/gather/fold convention)
· evidence: `seal/ledger/1788445862-a-phase-hands-the-next-one-a-record.md`,
  5 new rows (P1–P5), all **Executed** — verified against the actual template
  and skill text via `evidence-check --reverify` (16/16 coordinates resolved,
  `evidence-check` then reports 16 ok · 0 drifted · 0 broken)
· verified: executed — `uvx --with pytest python3 -m pytest
  tests/test_a_phase_hands_the_next_one_a_record.py
  tests/test_a_segments_record_says_what_it_was_asked.py
  tests/test_docs_line_wrap.py tests/test_review_axes.py
  tests/test_the_fixes_name_their_surface.py -q` → 79 passed, exit 0. Full
  suite, repository-wide lint, and typecheck are unverified by this branch —
  see below

## Why this work exists

A build phase now leaves the same committed, per-segment record a review
round already has, and both records now say what they were asked as well as
what they found — so what a phase discovers reaches the next phase, and a
later reader, without depending on an orchestrator retyping it into a spawn
prompt or on a transcript nobody reopens.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| `plan.md`'s Phase 2 row asks for a carrier-consistency check that `phases/phase-N.md` is "spelled identically across all four files phase 1 and 2 touch" | Spec/plan says: one identical spelling across all four. Code did: two checks — the three prose carriers (`templates/sdd-plan.md`, `agents/smith.md`, `skills/implement/SKILL.md`) pinned to the bare `phases/phase-N.md`; `templates/sdd-phase.md`'s own header comment pinned separately to the bracketed `phases/phase-<N>.md` | Code's reading, not the plan's literal count | Phase 2's own record: "the four files do need to agree on how this record is named — it just undercounts the one legitimate exception its own model (`templates/sdd-round.md`) had already set." `templates/sdd-round.md` already spelled its own path bracketed (`round-<N>.md`) before this branch touched the file, so matching that convention on the phase side is consistency with the sibling template, not a departure from the plan's intent |

The phase 3 heading-skeleton comparison and the phase 3 constant-vs-constant
test self-catch are not listed here: the plan's own Phase 3 row already
anticipated the bracket-vs-bare split ("mindful of phase 2's angle-bracket-
vs-bare-form finding when writing that comparison"), so nothing in the built
code contradicts what was specified — and the constant-comparison fix is a
test-construction correction, not a divergence between what was asked and
what was built.

## Not verified

| Item | Who must answer |
|---|---|
| ✅ Full test suite (repository-wide) | orchestrator, broad gate at 32d926b — `1839 passed, 1 skipped`; 4 pre-existing failures in `tests/test_the_records_can_be_carried_out_and_in.py` reproduce identically on unmodified `origin/release/v0.7.0` (root cause found and filed as #127 — the four tests build their expected zip name from local date, `seal export` writes it in UTC; not this branch's finding, this branch never touches `seal.py` or that test file) |
| ✅ Repository-wide lint | orchestrator, broad gate — `ruff check .` found 2 findings in this branch's own new test files (E741 ambiguous `l`, B905 `zip()` without `strict=`), fixed at 32d926b; `ruff check .` and `ruff format --check .` both clean afterward |
| ✅ Typecheck | orchestrator — this repository has no typecheck step at all; `CONTRIBUTING.md`'s "Running the checks" names only pytest, ruff, and `evidence_check.py`, so there is nothing to run |
| Whether the new `agents/smith.md` phase-record instruction is actually read by a subagent spawned under the next plugin release | not observable from this branch — phase 3's own record notes that a mid-session `specseal:smith` spawn loads its persona and skills from the plugin's version cache, frozen for the session rather than the working tree, so this is verifiable only after the next plugin release and a reload, by whichever session runs then |

## Not done

Nothing. Every item in `spec.md`'s Scope "In" list was built across phases
1–3, and every item in its "Out" list (`hooks/*.py`/`chain_check.py`
refusal logic, `docs/review-handoff-protocol.md` itself, the two #119
version-cache add-ons, `templates/config.md`'s "What no row governs" list,
#84's framer channel) was out of scope from the start rather than within
reach and set aside during the build.

## Fed back into the spec

None. Both design forks this work depended on — enforcement level 2 (a
template blank and a skill instruction) over level 3 (a gate refusal), and a
new file over a `plan.md` column — were pre-settled by the repository owner
before phase 1, marked "ALREADY DECIDED" in `plan.md`'s own Alternatives
table. The bracket-vs-bare-form naming judgment that surfaced while building
phase 2 is recorded above as a divergence and in the ledger as a scope
decision (P3); it is a naming convention for a record this work created, not
a rule `spec.md`'s Grounding clauses needed to state in advance, so it is
not written back as an inferred spec clause.
