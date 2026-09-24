# a release writes the gathered text back — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     this work item's `spec.md`, `plan.md`, `questions.md`, `routing.md`; #557's and #555's bodies and #555's comment; step A's ledger fragment rows C2, C3, F1, R1, U2 and `rounds/round-3-report.md` §🟡 1; `seal/ledger.md` S3, S1, G5, E1; `CLAUDE.md` §*a change writes fragments*; `.github/scripts/gather_changelog.py`
· evidence: `seal/ledger/1790221963-a-release-writes-the-gathered-text-back.md` H1–H3 added; step A's fragment C2, F1, C3 corrected and R1, U2 re-read; `seal/ledger.md` S3, S1, G5, E1 re-read; all re-stamped by `--reverify`
· verified: executed — every case seen red before it was planted, eight mutations from Python, the module, the neighbouring modules, ruff, `evidence-check --strict`, the branch's sweep; read — the claims of the re-read rows against the new code

## Why this work exists

A release that renamed `## Unreleased` or reworded an entry let a gathered
changelog fragment subtract a survivor that a correction in the same commit
left standing, so the sweep passed a release it should have stopped, and the
guard that covers the other release shapes had no case behind it.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The paste-ready comment above `shipped` | #557: *Read at `a` by the path the gatherer globs, which the release does not delete* / written: the fragment stands at `a` *whether the release leaves the fragment or deletes it* | the code | The sentence was false for a deleting gatherer, the case G2 pins; `spec.md` §Scope asks for the sentences to be true of both gatherers. The code itself is #557's verbatim |
| Step A's `plan.md` gate row | `spec.md` §Scope and `plan.md` phase 4: *Step A's `plan.md` gate row gains the clause #557 supplies* / not edited | the spawn prompt | The orchestrator's spawn prompt: step A's `plan.md` is a finished work item's record of what it planned, squashed into `release/v0.15.1` (#550) and not yet released (corrected 2026-09-24 in round 1's fix pass, which found *shipped* here untrue: `CHANGELOG.md` carries no marker for it), and the gate row #557 gives lives in this work item's `plan.md` gate table, which already carries it. F1's corrected note says where the corrected bound is |
| Step A's ledger row C3 | `spec.md` §*Data & interfaces* names F1 and C2 as the rows to correct / C3 corrected too | the code | C3's note repeated *a release's gathering commit deletes each fragment*, one of the three sentences phase 1 removed from the docstring (`agent-contract` §12). Its anchors did not drift, which is why the table did not predict it |
| The module docstring's released-changelog paragraph | `spec.md` §*Data & interfaces*: its sentence saying the gathering commit deletes each fragment is changed / that sentence reworded, and one sentence added saying the gathered text is held and never written | the code | The module docstring is where a reader looks for the module's account of an exclusion; the new rule belongs in it beside the reworded sentence |
| Q4's premise | *as `tests/test_the_changelog_is_gathered_at_release.py` loads the gatherer* / that module runs it as a subprocess | the default, import by path | The import works because the gatherer puts `hooks/` on `sys.path` itself; G4 also asserts the body still sits directly under the marker |
| `Checked` cells of `seal/ledger.md` S3, S1, G5 | the plan: *only the `Checked` cell and the note* / both updated, to 2026-09-24 | as planned | The rows were re-read on this date |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck (`unverified` here; this segment ran the survivor-check module, the six other modules that name `survivor_check`, `tests/test_release_hygiene.py`, `tests/test_the_changelog_is_gathered_at_release.py`, `tests/test_no_real_identifiers.py` and `tests/test_one_word_one_meaning.py`) | the sealer, after the review rounds settle |
| The `Ran by` cell of `phases/phase-1.md` to `phase-4.md` | the orchestrating session, which knows what it spawned |

## Not done

H1d, a release that renames `## Unreleased` and writes a new entry of its
own quoting corrected wording, stays silent: that wording is the range's and
is written as any file's is. `spec.md` §*Out* holds it for the repository
owner, with the guard refinement that would close it in `plan.md`
§*Alternatives*.

The guard's own comment, *a gathered release writes none*, is left as it
is: inside the branch it guards, where the file lost nothing, it is true.

One shape reports less than the base after round 1's fix, and it is left
open: a range that deletes a sentence from another file with no rewording of
its own, where the only rewording is a gathered fragment's. The rewording
shares nothing with what `CHANGELOG.md` lost, so it is held and not written,
the deleted sentence stays one run, and its verbatim copy goes silent (a
fix-pass probe, exit 1 at `61f0d0d8` and 0 at the tip). By the sweep's rule
the rewording is the fragment's branch's wording and not this range's; the
repository owner decides whether a gathered rewording should count as
written by the release that gathers it. `plan.md` §*Operational impact*
phase 1 and ledger row H1 state it.

## Fed back into the spec

none — the clauses this work added are ledger rows H1–H3 and the corrected
F1 claim, not `docs/` text; `docs/review-chain-spec.md` §*The survivor
sweep* states nothing at this altitude (`spec.md` judgment 6).
