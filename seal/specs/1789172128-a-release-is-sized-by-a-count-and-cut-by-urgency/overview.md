# a release is sized by a count and cut by urgency — overview

📋 implement applied
· spec:     `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/{spec,plan,questions,routing}.md`; issue #361 and its `## Done when`; `docs/issues-and-milestones.md` §*A milestone answers* when** and §*A label answers what it is about*; `docs/review-chain-spec.md` §*Five is a ceiling, not a target*; `CONTRIBUTING.md` §*Changing cited code is the case the rule has to answer*; `CLAUDE.md` §*a change writes fragments, never the shared file* and §*A row whose anchor a change removes is REMOVED, not re-pointed*; `skills/evidence-check/SKILL.md` §*The records arm*; `.github/workflows/test.yml`'s ledger job; `seal/config.md` (no `Record language` row → English); `seal/follow-up.md`
· evidence: `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md` — R1, R2, R3 added. `seal/ledger/1789100139-…md` — S3 removed, its substance carried by R1. `seal/ledger.md` — G5 and S4 re-read, dated 2026-09-12, re-anchored from `@993881ca` to `@a580e3ca`
· verified: **executed** — `tests/test_a_release_is_sized_by_a_criterion.py` (7 units, every one seen red first), `tests/test_docs_line_wrap.py`, `tests/test_release_hygiene.py`, `tests/test_one_word_one_meaning.py`, `tests/test_no_real_identifiers.py`, `tests/test_evidence_check.py`, `tests/test_a_row_points_by_content.py`, `tests/test_the_ledger_fragments_fold_at_release.py` and the five modules that read the edited document, all exit 0; `bin/evidence-check .` and `--reverify`; `bin/survivor-check` over the branch range; `uvx ruff check` and `uvx ruff format --check` on the new module; a `test_tmp_*` probe on `timers_in`, deleted. **read** — `tests/test_release_hygiene.py`'s constants and exemptions, `gh label list`, #361 and #362. **unverified** — the full suite, the repository-wide lint and the typecheck; the sealer takes those once after the rounds settle

## Why this work exists

Sizing a release used to mean reading a number that looked like a target, and a
session acting on that reading proposed two scheduling moves in one day that the
repository owner had to stop; the rule now states the criterion the last two
releases were actually cut on, and a label writes that judgement down per ticket
so it is not made again from scratch.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| What the paragraph may claim about automation | `spec.md` Scope: the paragraph says *nothing automated reads either for scheduling*, from #361's `## Done when` row *nothing automated reading either* | The narrower claim: **nothing schedules from either**, and the one thing that reads a milestone checks a cut release against its pool and never decides what goes into one | §*One thing reads a milestone, and it can stop a release* opens *This section said nothing automated reads a milestone until #359 … It is not true any more*. The wider wording would have put two answers in one document, which is the defect S6 names for the label section one section over. The row's substance — a person cannot expect the tracker to size a release — is kept |
| How the label is reconciled with §*A label answers what it is about* | `spec.md` Scope: the new label is *the second one*, with the section stating the exception; S6 asks the section to *state the exception* | No exception is written. The prefix makes `size:` a topic — sizing, which every release has — and only the value `now` is spent at the release, so the label does not break the rule | Writing a carve-out for a rule the label does not break would leave a permanent exception nobody can test. S6's substance is met: the section leaves no two rules disagreeing, and `flow-measurement` is still named as the standing precedent for a label that is not a topic. `chain: capped` is the in-tree shape the spelling was taken from |
| How S3's absence is verified | `spec.md` S3: `git grep -n "three or four is the size"` exits 1 after the edit | The case reads the document through a whitespace-flattening reader | That command exits 1 **before** the edit too: the line wrapped between `three` and `or four`, so the recipe proves nothing. Phase 1 measured it. `tests/test_one_word_one_meaning.py`'s own `flat()` helper exists for the same reason |
| How many ledger rows the edit moves | `spec.md` §*The ledger row this edit moves*: one row, S3 in another work item's fragment | Three rows touched — S3 removed, and `seal/ledger.md`'s G5 and S4 re-read and re-verified | `bin/evidence-check .` after phase 3 reported two DRIFTED anchors, not one: G5 and S4 both cite the label section, which phase 3 edited. Neither claim went with the edit. S4 was the one worth opening, because phase 2's new paragraph names the same version check — it states no boundary of its own and points at the owning section |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck | the orchestrating session — `agent-contract` §2 assigns the broad gate to the sealer, once, after the review rounds settle |
| whether `size: now` is the spelling the owner creates | the repository owner. Q2 chose the prefix form and left the string to whoever creates the label; Q3 leaves creation and application to the owner after this merges. Nothing pins the document against the tracker, and no check can see a label that was never created or created under a different spelling |
| whether #351's changelog fragment should keep quoting the replaced sentence | the reviewer, then the repository owner. `survivors.md` excuses it on the ground that the fragment's own claim is still true and this work item's entry sits in the same released section; the alternative reading is that a released section should not quote a sentence the same section replaces |
| `release: 0.11.1`'s milestone description, stale well past its `Size.` line | the repository owner. Q4 put milestone descriptions out of scope; its `Order, and why` paragraph still names #330, #343, #345, #350, #198, #103 and #354, all of which left for `release: 0.11.2` |

## Not done

**The checker's off-by-one is not repaired here.** `timers_in` refuses a version
this repository has demonstrably shipped for the length of one release, because
`plugin.json` is bumped at the release-preparation commit. Q1 chose the prose
citation and filed the defect as **#363**, on the ground that widening a checker
so a document may say something is the easiest way to green. #363 also records
the trap: derive *shipped* from git tags and never from `CHANGELOG.md`, because
the preparation commit adds the heading and bumps the version together.

**Nothing is written to the tracker.** No label created, none applied, no
milestone description edited, no issue moved — Q3 and Q4. #362 was held against
the criterion as the rule's own falsifiable test and takes no label
(`phases/phase-3.md`), and this work item assigns it no milestone: the criterion
answers *now or not now* and ordinary scheduling answers the rest.

**No checker reads the label, and none is proposed.** A workflow that scheduled
from it would be a gate, owing `CONTRIBUTING.md`'s four items and a prompt
budget. The document states that nothing reads it, which is part of the
deliverable rather than a gap.

## Fed back into the spec

**None as a clause.** Two findings belong to the frame's verification recipe
rather than to its claims, and both are recorded in the divergence table above
instead of being written back: S3's grep exits 1 before the edit, and the edit
moves three ledger rows rather than one. Neither changes what `spec.md` says the
work delivers.
