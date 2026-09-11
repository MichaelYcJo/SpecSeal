# Implementation Plan: docs/flow.md is deleted, and what it carried is placed where it is read

<!-- seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/plan.md —
HOW, in phases. This is the Design Gate's artifact. -->

Approved 2026-09-11 by the repository owner, when `smith` was spawned.

## Summary

`docs/flow.md` is deleted. Of its 120 lines, three numbered steps are
procedure and move into `skills/implement/orchestration.md`; one sentence is
a standing tracker rule and moves into `docs/issues-and-milestones.md`; the
18 checkbox rows and their grounds move to the tracker, which already holds
the state they duplicate; and the two rules about maintaining the file itself
end with it. Four live files that cite it are repaired, and the two 0.4.0
records lose the clause that names it.

## Technical context

The live surface is nine files, and only nine. `grep -rln "flow\.md"` over
the tracked tree returns `CHANGELOG.md`, `seal/ledger.md`, 150-odd files
under `seal/specs/`, and then:

| File | Hits | What it is |
|---|---|---|
| `docs/flow.md` | — | the file itself, 120 lines |
| `docs/release-checklist.md:18,38,40,79` | 4 | two step-0 bullets, a measurement paragraph, a step-2 instruction |
| `docs/issues-and-milestones.md:26,27,110` | 3 | the second scheduling act, and *says the same thing from the ticket's side* |
| `docs/one-root-by-lifetime.md:531` · `.ko.md:509` | 2 | the 0.4.0 design record, both editions |
| `tests/test_the_rules_have_one_owner.py:61,500` | 2 | `FLOW` and the two cases reading it |
| `tests/test_release_hygiene.py:109,483,574` | 3 | the exemption entry, its docstring, two fixture usages |
| `tests/test_a_corrected_sentence_survives_elsewhere.py:612` | 1 | a comment citing the deleted-section rule |
| `skills/code-review/scripts/survivor_check.py:29,110` | 2 | module docstring |
| `skills/verify/scripts/broad_gate.py:324` | 1 | a docstring naming #103's class |

`CHANGELOG.md`, `seal/ledger.md` and `seal/specs/` are outside the scanned
set or are records; `seal/ledger.md` needs checking for a row whose anchor
this change removes, which `CLAUDE.md` says is a REMOVED row rather than a
re-pointed one.

**What breaks in six months.** The order a ticket runs in becomes a section
of a skill, and a skill is loaded rather than browsed. A person who used to
open `docs/flow.md` each morning has to know that `skills/implement/
orchestration.md` is where the sequence went — which is what S1's moved cases
protect, and what the changelog entry has to say plainly.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Keep the file and split it per work item, the way `CHANGELOG.md` and `seal/ledger.md` were cured | The fragments would need a gather command and a release step to run it, which is machinery for a file no machine reads. The cure was built because checkers read those two | Rejected — the cost is the same and the benefit is not |
| Keep the file and add a merge driver for it | A merge driver is repository configuration a clone has to install. The conflict is a symptom; the file being shared state is the defect | Rejected |
| Delete the file and move nothing | `## Order inside a ticket` is procedure a session acts on, and the case pinning it is a real ordering claim. Deleting it removes a rule nobody replaced | Rejected — this is the issue's own `Done when` |
| Delete the file and move the rows into one planning issue per release | Re-creates a second place to read, which is what the file was | Q1 option (b); not the default |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `## Order inside a ticket` lands in `skills/implement/orchestration.md` as an `Orchestrator:`-prefixed section; `tests/test_the_rules_have_one_owner.py`'s `FLOW` and its two cases move to it | the two cases seen red against the pre-move text, green after; `bin/test -q tests/test_the_rules_have_one_owner.py` |`7ed455b` |
| 2 | `docs/issues-and-milestones.md` gains the sizing rule and loses the second scheduling act; `docs/release-checklist.md` loses its four steps | read; `grep -c "flow\.md"` is 0 in both; the module that scans them stays green |`75fb4ae` |
| 3 | The live citations are repaired — and the two 0.4.0 records lose the clause naming the file (Q3 (c)) — `test_release_hygiene.py`'s exemption entry and two fixtures, `test_a_corrected_sentence_survives_elsewhere.py`'s comment, both `survivor_check.py` docstring citations, `broad_gate.py`'s | each touched module run on its own, exit code read | `2206a0c` |
| 4 | `docs/flow.md` is deleted; `seal/ledger.md` is checked for a row this removes and the row is marked REMOVED if one exists | `grep -rn "flow\.md"` over the tracked tree returns only `CHANGELOG.md` and `seal/specs/`; `bin/evidence-check` | `89f4f8a` |
| 5 | The tracker carries what the file carried — every scheduled milestone's description states purpose and order, and a ticket whose position has grounds not in its body gains a comment (Q1 (a)) | `gh api repos/:owner/:repo/milestones` read back; the comment urls | **closed 2026-09-11 by the session, before the spawn** |

Phase 5, as executed. The four scheduled release milestones (40 · 42 · 43 ·
44) each carry purpose and order grounds; #103 and #330 gained the two
comments whose grounds were in `docs/flow.md` and in no ticket body
(`issues/103#issuecomment-5629515078`,
`issues/330#issuecomment-5629515284`). Six bodies were checked against the
file's rows before writing; #198, #350, #343 and #345 already carried theirs
and got nothing.

**The file was already stale, which is a finding rather than a step.**
`docs/flow.md`'s `## 0.11.1` section lists #331, #335, #339 and #149 as this
release's. The milestones — re-classified on 2026-09-11 under #223 — put
#331 and #335 in 0.11.3 and #339 and #149 in 0.11.2. The descriptions were
written from the milestones, not from the file, and the divergence belongs
in the closing memo.

| 6 | `seal/specs/<id>/changelog.md` and `seal/ledger/<id>.md` fragments; the closing memo. **The changelog entry is the record of the removal** (Q3): it names all four parts of `docs/flow.md` and where each went, the clause dropped from the 0.4.0 record included, so nothing has to be left behind as a marker | the fragments exist and `fold_ledger.py --check` is clean | |

Phase 5 is the session's, not the builder's: writing to GitHub is outward-facing
and a subagent does not make that call. Phases 1–4 and 6 are the builder's.

**Status is empty, or the commit that closed the phase.** A tick is refused
and so is `done`.

## Operational impact

No migration, no new dependency, no compatibility break. One removal a person
will notice: the file they opened each morning is gone, and the changelog
entry has to say where each of its four parts went. That entry is the only
place the removal is recorded — no marker is left in any file the work
deletes from, which is the owner's call of 2026-09-11 and the reason Q3
resolved to a plain deletion.
