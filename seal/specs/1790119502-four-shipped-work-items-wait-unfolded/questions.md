# four shipped work items wait unfolded — questions for the planner

<!-- seal/specs/1790119502-four-shipped-work-items-wait-unfolded/questions.md —
decisions only a human can make. The run is `automation`: nobody is asked, so
every row says why the tree could not settle it, and every default continues. -->

## What the ticket left open and the tree answered — do not reopen

| Settled | Where the grounds are |
|---|---|
| which top-level `docs/` file receives each of the four statements | `spec.md` §*Destinations*, chosen against the anchored ledger units in G1 |
| how a path into a retired directory is resolved — the path dropped, the work item id named with the `docs/` section carrying its marker. The frame's answer was a pin to `b0cbd34`; the orchestrator replaced it during the build because the history is rewritten after this release *(Corrected 2026-09-23 in round 1's fix pass: the SHA pin G2 names was replaced during the build.)* | `spec.md` G2 and its replacement line; `phases/phase-2.md` |
| that no ledger row anchors inside the four directories (#511) | `spec.md` G3, measured; `plan.md` phase 5 step 2 re-checks it |
| that every floor holds after the removal and none needs a new answer | `spec.md` §*The population floors*, re-measured per reader |
| that the 11 ungrouped stay kept | `spec.md` O5 — #497's rule, and the tree gives no reason to reopen it |
| that open `## Not verified` rows in the four overviews need a home before the removal, and which | `spec.md` G4, L1–L11 |
| that the 26 older dangling citations are named and not repaired here | `spec.md` O3 |
| that `seal/ledger.md` cannot stay byte-identical, and what may change in it | `spec.md` G1 and A8 |

## The rows that remain

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | The release this fold follows left the close-issues workflow red: run `35796513013` failed at `tracker_labels.py --apply` because `size: now`'s description is longer than the 100 characters GitHub allows, so the label was never created, and the step after it — rolling the flow-measurement log — was **skipped**, which leaves #496 titled for the release before. Does 0.13.2 carry the repair, or does it go to the backlog? | **a person** — whether a ticket must be in effect before the next work item starts is the sizing judgment `docs/issues-and-milestones.md` gives to whoever files it, and the repository owner is who sizes this release. The tree says what broke; it cannot say how urgent it is | its own work item in this release — the next merge to `main` creates the label and rolls the log · the backlog — every release until then goes red at that step and the log stays unrolled | this branch does not touch the script or the workflow (`spec.md` O4). The orchestrator raises the issue before the pull request, and the pull request body names it | ✅ default taken 2026-09-23 under `automation`: filed as #515 in the `release: 0.13.2` milestone, and this branch leaves the script alone |
| Q2 | Does every module that reads the real `seal/specs/` stay green once the four are gone? | **a measurement** — the floor table predicts yes from counts, and a count is not a run | green → nothing to do · red → the phase records the reader and answers it by `skills/settle/SKILL.md` §3, never by a smaller literal | assume green, as the table predicts; run them in phase 5 step 4 | ✅ green, measured 2026-09-23 on the folded tree: the 44 modules `grep -rln "seal/specs" tests/` names, `2315 passed, 1 skipped`, exit 0, and no literal moved (`phases/phase-5.md`) |
| Q3 | Does `chain_check.py --baseline origin/release/v0.13.2` print `retired:` for all four removed declarations? | **a measurement** — #497 built the arm on 88 removals against a different base; one run on this one settles it | four `retired:` lines → nothing to do · a refusal → the marker is not on a live line at the top level of `docs/`, which is this branch's to fix | assume yes; run it in phase 5 step 4 and record the output whatever it says | ✅ yes, measured 2026-09-23: four `retired:` lines on both `origin/release/v0.13.2` and `origin/main`, and the only error is this work item's own absent round record (`phases/phase-5.md`) |
