# 1790683267-a-rider-read-ends-where-the-hasher-cuts — overview

📋 implement applied
· spec:     this item's `spec.md` (Grounding, M1–M11, Scope, S1–S11, Data & interfaces, Failure direction, the changelog intent), `plan.md` (Technical context, Alternatives C, Phases, Ledger), `questions.md` J1–J10 and Q1–Q3, `routing.md`; G's `rounds/round-3-report.md` §🟡 1, §⬜ 2 and §Paste-ready fixes; `CLAUDE.md`'s fragment and ledger rules; `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR`
· evidence: K1 and K2 added in `seal/ledger/1790683267-a-rider-read-ends-where-the-hasher-cuts.md`; G13 re-read and re-stamped in `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md`; P5-1 corrected, re-read and re-stamped, and R1-1 corrected, in `seal/ledger/1790645290-the-hooks-and-the-rider-check-read-fences-and-comments-by-one-rule.md`; S2 re-read and S3 re-read and re-stamped in `seal/releases/0.9.1.md`
· verified: executed — the new cases red at the base and green after, one mutant per changed branch, the S4/S6/S7 probe, `rider_check.py --root .` at both versions, the three rider modules and the floor module, `tests/test_a_record_states_what_the_tree_has.py`, ruff on the changed files, `evidence-check --strict .`, `survivor-check`; not run — the full suite, which is the sealer's

## Why this work exists

The rider check read some riders past the line its hash cuts, so a stamp was hashed into the region it names and `--reverify` could never settle it. The reader now reads exactly the blocks the hasher cuts, so the two cannot part again by construction.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The class case's second assertion | S3: "every piece carrying the marker that starts inside a block the hasher returns starts exactly one rider". The first version of the case checked each rider's start and its containment, and a reader whose riders ran to the block's end passed it | the case also asserts that no piece after a rider's first carries the marker | the mutant is not equivalent: a stampless first rider would read the second's stamp on its line. "Exactly one rider" is the spec's own word, and the added assertion is what makes the case hold it |
| The comment above `_blocks` | spec §Scope lists the touched units' docstrings. The comment is outside them, and it said the walk loads at the first markdown file carrying the marker | corrected to "any type", naming `riders_in` | it was already false at the base (G's phase 6), and the load it describes is now `riders_in`'s. No ledger anchor covers it |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, repository-wide lint and typecheck over this branch | the sealer, once the review rounds settle |
| the new cases and the fix on Linux and Windows; only macOS ran them here | CI's Linux and Windows legs on the pull request |

## Not done

The `-->` test's own reach is not changed. A markdown block still ends at a line holding `-->` anywhere, so the markdown shape reads BROKEN "no verification stamp" rather than ok. The spec puts that out of scope, because it is older than #664 and not about line ends. Whether it deserves an issue is the orchestrator's call.

`quoted_lines` keeps its TEXT parameter (J3). No shipped caller passes one now. `tests/test_the_hooks_hide_what_a_renderer_hides.py` does, against the oracle.

`region_lines`' comment "No TEXT: …" is left as it stands. It is still true of `quoted_lines`, and editing it would move S2's anchor for a sentence that holds.

The reason cell for `riders_in` in `tests/test_every_reader_ends_a_line_where_gfm_does.py#OUT_OF_CLASS` is left as F's. The plan makes that optional, and S8 keeps existing cases unedited apart from the index.

## Fed back into the spec

none — the class case's added assertion is S3's own sentence, made checkable. It adds no clause.
