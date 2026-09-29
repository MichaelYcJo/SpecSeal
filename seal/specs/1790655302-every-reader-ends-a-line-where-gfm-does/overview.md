# 1790655302-every-reader-ends-a-line-where-gfm-does — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show. -->

📋 implement applied
· spec:     `spec.md` (Grounding, M1–M8, Scope 1–7 and Out, the class enumerated, S1–S20, Data & interfaces, Failure direction), `plan.md` (Technical context, Alternatives A–H, Phases 1–5, Operational impact), `questions.md` D1–D13 and Q1–Q3; `CLAUDE.md` §*a change writes fragments* and §*commit early*; `skills/agent-contract/SKILL.md` §9, §12, §14, §15; `templates/sdd-phase.md`; item C's `phases/phase-5.md` and ledger fragment
· evidence: `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md` G1–G12; 61 rows in `seal/releases/0.4.0` to `0.15.5` and in the fragments of items 1790635413 and 1790635414 re-read against each edit and re-stamped with a dated note; 1790635414's H2 removed and rewritten as G3
· verified: executed — every new case red at `2e392d46` (a `git archive` in the scratch directory) or against a planted mutant, one mutant per moved call site and per added unit, each phase's readers' modules, S20 for every moved gate, `evidence-check .`; read — the 61 re-read claims; unverified — the suite, lint and typecheck (the sealer's) and CI's legs

## Why this work exists

A reader that split markdown or record text with `str.splitlines` read lines
no renderer shows below one of eight characters; after this, every reader
outside work item F's files ends a line where GFM, `ast` and git do.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The count of F's `hooks/config.py` sites | *The class, enumerated*: "`hooks/config.py` (3)" · `ast` finds two calls, `#config_rows` and `#refusal`; `#unfenced` names `text.splitlines()` in its docstring and makes no call | code; the class case exempts the file by path | F's file either way. The third was a docstring mention, which the spec's own M3 says it does not list |
| One function changed its signature | *Data & interfaces*: "No existing function changes its signature." · `chain_check.py#frame_mark(text)` became `frame_mark(reader, text)` | code | It had no reader to split with, and its one caller, `frame`, already held one. Loading the reader inside it would be a second load path for one call site |
| S8's scenario | "a ledger row with a U+2028 in its notes at `a` and `b` … the row is found standing" · a row unchanged at both ends is found standing at base too, because both ends cut it alike | the case is a row with no id, corrected in place, whose still-resolving anchor stands after the separator | That is the shape red at base: cut, the row lost the anchor, and the correction read as a removal (`phases/phase-2.md`) |
| `survivor_check.py#reader` | spec silent · it now caches the loaded module by path | code | `segments` asks it for `gfm_lines` once per corpus file, 504 on this tree, and it executed the module on every call. A case holds the cache and the refusal of a moved path |
| Readers #664 did not name, beyond the frame's list | the frame's phases · `gather_changelog.py#leaves_open`, `#section_lines`, `insert`'s fresh-section arm and `main`'s dry run got a case each; the spec named them only as moved | code | A moved call no case notices is a move nobody can check. Each was red at base |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck over this branch | the sealer, once the review rounds settle |
| CI's Linux and Windows legs over the new cases, the U+2028 fixtures and the `awk`-shaped `claude_block.py` case included | the pull request's CI run |

## Not done

- **`rider_check.py#inferred_anchor` still slices `text.splitlines()`.** It
  is F's file (#667, PR #672), and it compares that numbering with
  `checker.py_spans`, which is `ast`'s. Once F lands it should slice
  `checker.gfm_lines(text)`, the list `region_lines` slices since item C.
  The milestone 49 orchestrator answers it (questions.md Q1).
- **S17 does not hold `hooks/blocks.py#gfm_lines` equal yet.** F had not
  landed at phase 5, so the copy is not in this tree. Whichever of F and G
  lands second adds it to `test_every_copy_of_the_splitter_is_the_readers`.
  The milestone 49 orchestrator answers it.
- **`gather_changelog.py#main`'s heading line has no case.** It is
  `gfm_lines(block)[0]`, and `block`'s first line is `section`'s own
  `## <version> — <date>`, which cannot hold one of the eight. The mutant
  back on `splitlines` is equivalent.
- **Item C's `rounds/round-1.md` keeps the line break its report held as
  U+2028** (spec M2). A closed record asserts a past state and stays
  (questions.md D11).

## Fed back into the spec

none
