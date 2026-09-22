# `settle` — questions for the planner

<!-- seal/specs/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## What the tree answered, so nobody reopens it

These were open in #458 or in #83 and are **not** rows below. Each is decided
in `spec.md` or in `plan.md`'s Alternatives table with the grounds, and each
is overturnable by opening what was opened.

| Settled | Answer | Where |
|---|---|---|
| What goes up — the whole conclusion or only what is still true | Only what is still true, and the session decides which; the command writes no prose into `docs/` | `spec.md` §*Grounding* G1 |
| What groups | The ledger anchor's enclosing file, rolled up to a segment — written already for 83 of 98, with the other 15 named | `spec.md` §*What groups, measured on this tree* |
| When it runs | By hand, named in `docs/release-checklist.md`; not inside the release-preparation commit and not a check that fails a build | `spec.md` §*Grounding* G5 |
| Delete, move, or keep `overview.md` alone | Delete the directory whole | `plan.md` Alternatives |
| Where a segment's policy lands | An existing `docs/*.md` where the segment has one, a new top-level `docs/<segment>.md` where it does not. No `docs/policy/` directory | `spec.md` §*Grounding* G2 |
| Whether this closes #83 | It closes #83. #101 and #216 stay open | `spec.md` §*What the tree answered* |
| Whether `docs/one-root-by-lifetime.md`'s 2026-09-02 text is rewritten | No — a dated section is added, in both editions | `plan.md` Alternatives |
| Which two readers a removal reaches, and how | One fails and one goes vacuous; a third the document never named is the survivor sweep | `spec.md` §*The two readers* |
| Whether any check really reads the shipped work items — the ticket says 0 | **False as stated.** 14 test modules read the real corpus and at least 6 carry a population floor a fold turns red; the ticket's 0 is `evidence-check`'s own arm generalised | `spec.md` §*The ticket's headline claim is false* |

## The rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | **Does this release also fold this repository's own 97 released work items, or does the fold become a work item of its own?** The ticket's value is 15M of sediment retired, and shipping the mechanism alone retires none of it. Against folding here, and the first item is measured: **14 test modules read this repository's own `seal/specs/` corpus and at least 6 carry a population floor that a fold turns red** (`spec.md` §*The ticket's headline claim is false* has the coordinates), so the mechanism's own review round would run on a tree whose suite the commit under review had just broken; the unverified-record step goes red unless phase 1 and the fold sit in one diff; a `survivors.md` range-row becomes mandatory; and the release's diff turns mostly into deletions with the mechanism buried inside them. For folding here: the sediment is the ticket's whole subject, and a mechanism nobody runs is the state `settle` has been in since the root existed. | **a person** | **its own work item** — this branch ships the mechanism, phase 6 is a dry run whose report is the input to that item, nothing is removed · **this branch** — a seventh phase writes nine segments' policy, answers six population floors, retires 97 directories and carries a `survivors.md` range-row; phases 1–5 are unchanged either way | **its own work item.** The build does not wait: phases 1–6 are identical under both answers, and the second answer adds a phase rather than changing one | ⬜ |
| Q2 | **What does a `tests/` anchor roll up to?** 852 of 1,772 ledger coordinates — 48% — anchor under `tests/`, and the ticket's segment table says *tests excluded* without saying where they go. A case pinning `round_record.py`'s behaviour is evidence about that segment, not about a segment called `tests`. | **the work** | fold a test anchor into the segment of the code it pins (needs a rule for a case that pins prose in a document) · treat `tests/` as its own segment · leave a test-only work item ungrouped and name it, the way the 15 without a ledger row are named | **fold into the segment the case pins, and name what cannot be resolved.** Phase 2 decides it against the real corpus and records the rule it used | ✅ **the default, spelled as a majority over the work item's code anchors.** A work item's segment is the file the most of its non-`tests/` coordinates anchor in, ties broken by path order; test anchors are dropped in favour of code anchors, and an item whose anchors are all under `tests/` is named `tests only`. Measured on this repository in phase 2: **two** of 97 released items land there, so the 48% under `tests/` costs two named items rather than a segment called `tests`. `phases/phase-2.md` carries the reasoning |
| Q3 | **Does `gather_changelog.py --check` pass vacuously after a fold, or fail?** `spec.md` §*The two readers* says it passes having examined nothing, and that is **read** from `fragments()` and `ungathered()`, not executed. One command over a scratch tree with a fragment removed and its marker absent settles it, and the answer decides whether phase 1's second half is a soundness fix or a blocker. | **a measurement** | one run of the existing script against a scratch root · it exits 0 having examined nothing (the read), or it exits 1 | **it passes vacuously**, and phase 1 changes it because a check that passes having examined nothing reads as *all gathered* | ✅ **it passes vacuously.** Executed 2026-09-22 in phase 1, against the shipped script: a scratch root holding a `CHANGELOG.md` with one entry and no marker, and a `seal/specs/<id>/` directory with no `changelog.md` in it, gave `0 changelog fragments, all gathered` at exit 0. The read in `spec.md` §*The two readers* is confirmed and there is no divergence. Phase 1 changed it to print the marker count beside the fragment count and to refuse a corpus carrying neither |
| Q4 | **Where does the fold record live?** `settle` runs incrementally and must record what it folded, and the one place it may not be is inside `seal/specs/<id>/`, which is what the fold removes. `spec.md` §*Data & interfaces* fixes that constraint and leaves the home open. | **the work** | reuse the `<!-- specs/<id> -->` marker in the `docs/` document the item folded into, so the record is the provenance comment and there is no second file to keep in step · a file directly under `seal/`, permanent by lifetime · a row in `seal/config.md` | **reuse the marker.** It is already the convention `fold_ledger.py#marker` and `gather_changelog.py#marker` share, and a record derived from the destination cannot disagree with it | ✅ **the default.** Decided in phase 2, and the reason is stronger than the row's: because the record is derived from the destination it splits the work into two states a run can be interrupted between — folded, and folded and retired — which is what A4's *an interrupted run resumes* needs. A file of its own would have to be written twice and could disagree with the tree between the writes. The reader is `skills/verify/scripts/unverified_check.py#folded_items` |

**`Who can answer` takes one of three values and nothing else** — a person, a
measurement, or the work. Q1 is the only row that would stop anybody, and it
does not stop this build: its two answers differ by whether a seventh phase
exists, not by what phases 1–6 contain.

Answered rows feed back into `docs/` (policy clause or open-questions section)
before this directory's work merges.
