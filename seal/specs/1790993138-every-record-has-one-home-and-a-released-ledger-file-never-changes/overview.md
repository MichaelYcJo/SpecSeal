# 1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show, each part written when it happened. -->

📋 implement applied
· spec:     spec.md D1–D8, S1–S15 and §*The classes, enumerated*; plan.md's phases; questions.md Q1–Q6, M1–M3, W1–W3
· evidence: seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md
· verified: each phase record carries its runs, labelled executed or read

## Why this work exists

A re-read of a released ledger row used to edit the released file in place, so two branches re-reading one row conflicted at their squash; from this work on, the re-read is a citing row in the branch's own fragment, a released file never changes, and every kind of record has one home that the rest link to.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The literal a citation carries (W1) | D2: "The literal is a prefix of the row's first cell, long enough to be unique in its section." / `citation_for` takes the shortest unique word-prefix of the first run of the cell free of `\`, `"` and a backtick; where every prefix is on another line too, the cell's last run with its closing pipe; and the heading tried nearest first, then the enclosing path, then each enclosing heading outward | the code | M2, phase 1: a plain prefix left 68 of 1,083 coordinate-bearing released rows with no citation, every one a cell opening with a code span. Cutting at the quoting characters left 22, all under a heading holding a backtick, which cannot sit inside the citation's code span. With both rules, 0 of 1,083 fail. The closing-pipe fallback was found by the phase-1 case for a row whose whole first cell starts a longer row's. D2's semantics (a content coordinate naming one row) are unchanged |
| A released row whose anchor moved | D3: a code coordinate is "BROKEN by the same rules as today", and D4 writes a `Re-read ·` row for a *drifted* coordinate / under the freeze `--reverify` no longer re-points a released row in place, and a `Re-read ·` row cannot clear it, because the family union is keyed on the coordinate and the old and new spellings differ | `--into` names the row with its repair, a `Corrected ·` row in the fragment, and writes nothing for it | Spec silent on a moved anchor in a released row. Writing a `Corrected ·` row automatically would put a claim into the ledger that nobody wrote; the advisor's frozen repair line says the same |
| What the freeze row means to `evidence-check` | D5 keys the freeze on a work-item id for `correction-check` / `--reverify` writes no released file in a repository with the row, whatever its value | any value | D4: "In a repository that declares D5's row, `--reverify` without `--into` writes no released file"; the spec's sibling section says a sibling's own `--reverify` "refuses an in-place write to a released file" after it merges this in, which only a value-blind reading gives |
| `settle`'s anchored guard under the freeze | D6: `settle.py`'s per-row guidance "becomes: write a `Corrected ·` row, and never remove the row" / the guard also skips a row a correction supersedes, asking the checker's `family_view` | the code | Without the skip a released row answered as D6 says would hold its directory forever, because the guard reads every line; the checker no longer reads a superseded row's anchor, so the removal breaks nothing |

## Not verified

| Item | Who must answer |
|---|---|
| Whether the family union's failure direction (a coordinate whose content returns to a hash an earlier reading recorded reads OK again, spec D3) is acceptable in practice | the warden, reading D3 against the cases; the repository owner if it is contested |
| The freeze arm on a real pull request: the hygiene step passes `origin/<base>...HEAD`, and `frozen_changes` reads the base's version off that spelling; the cases drive a local `release/v0.1.0`, not CI's `origin/` form | CI, at this work item's pull request into `release/v0.18.0` |
| `ledger_kind` and the citation re-rooting compare paths through `os.path.normcase`; nothing was run on Windows | CI's `windows-latest` leg |
| The full suite, lint over the repository and the typecheck | the sealer, once the review rounds settle |

## Not done

`seal/config.md`'s `Over the ceiling` row and `docs/the-evidence-ledger.md`'s ceiling statement still name #715 as the issue that splits `docs/commit-review-gate-spec.md`, and that split is now #727 (F1). D7 says the row "stays as it is until then", F1's change removes it, and a pin (`tests/test_a_document_has_room_for_the_next_fold.py#test_the_evidence_ledger_states_the_values_the_config_rows_hold`) holds the row and the prose to one home, so re-pointing it was left to F1.

## Fed back into the spec

Each of these is *inferred during implementation*, and a planner may
overturn it:

- **W1's literal rule** (`evidence_check.py#citation_for`, `#unique_literal`),
  measured over the corpus as M2.
- **A released row whose anchor moved takes a `Corrected ·` row**, because a
  `Re-read ·` row cannot clear a coordinate whose spelling changed; the home
  states it (`docs/the-evidence-ledger.md` §*A released row is read again in
  the branch's fragment*).
- **The freeze row is value-blind to `evidence-check`**: any value stops
  `--reverify` writing a released file; the cutoff is `correction-check`'s.
- **`settle`'s anchored guard skips a row a correction supersedes**, so
  D6's guidance can be followed without holding a directory forever.
- **M1 kept the fold fragment's name**: every reader accepts
  `seal/ledger/<unix-seconds>-fold.md`.
