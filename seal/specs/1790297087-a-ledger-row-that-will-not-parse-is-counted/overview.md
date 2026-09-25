# 1790297087-a-ledger-row-that-will-not-parse-is-counted — overview

📋 implement applied
· spec:     this work item's `spec.md`, `plan.md`, `questions.md`; `docs/the-evidence-ledger.md` as `spec.md` §*Grounding* cites it; `skills/evidence-check/SKILL.md` §*A coordinate names content, never a position*, §*Verdicts and what to do*, §*Re-verifying is recomputing the hash*, §*Known limits*; `templates/ledger.md` §*Coordinates*; `CLAUDE.md` §*a change writes fragments, never the shared file*; `seal/follow-up.md`'s #299 row; #299, #322
· evidence: `seal/ledger/1790297087-a-ledger-row-that-will-not-parse-is-counted.md`, seven rows (the rider-stamp claim, five for the arm, one for the advisor); corrected in place with a `Corrected 2026-09-25` note — `seal/ledger.md` (the eval row, the separator row; the rider-stamp row removed), `seal/releases/0.4.0.md` (the hygiene-step row), `seal/releases/0.12.0.md` (the `claude_block.py` row); re-read and re-stamped with a dated `Re-read` note — `seal/releases/0.4.0.md` (five rows: re-verifying is separate, re-anchoring, an unreadable ledger, never silent, the fix-pass run), `seal/releases/0.15.3.md` (P2-1, P2-2), `seal/releases/0.11.3.md` (the lenient line's condition), `seal/releases/0.8.3.md` (`display_name`), `seal/releases/0.9.0.md` (R5), `seal/releases/0.14.0.md` (C3), `seal/releases/0.8.0.md` (R6), `seal/releases/0.13.1.md` (the retired-`spec.md` anchors row), `seal/releases/0.5.0.md` (S6, S12), `seal/releases/0.15.1.md` (R2); the fragment's seventh row is the advisor's
· verified: executed — every new case seen red (S1–S10 and the vendored cell rule against the phase-1 checker, S11 and the docstring pin against the phase-2 advisor, the mutation-driven cases under their mutations), each added unit mutated one at a time, `evidence_check.py --strict .` before and after each phase, the arm over the `ca2afdb9` ledgers, the modules reading each edited document, `tests/test_dispatch.py` whole, ruff on the changed files, and #322's `-W error` compile of every tracked `.py` file; read — the claims of every re-stamped row

## Why this work exists

A ledger row whose coordinate the checker could not parse was counted nowhere, so a typo in a hash or an unescaped quote took a claim out of the ledger while the build read clean; five such rows were standing in this repository.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The rider-stamp row in `seal/ledger.md` | `spec.md` §*In* item 6: *A claim that still holds gets its coordinate corrected … A claim that no longer holds is corrected or taken out* | Taken out, and the current claim written as a new row in this work item's fragment | The quoted line `STAMP = re.compile(…)` is no longer in `tests/test_a_rider_reaches_its_file.py` (it is `OLD_STAMP`, kept only to name the pre-#239 form), and the claim *the SHA is an ancestor of HEAD* has been false since #239. `CLAUDE.md`: *A row whose anchor a change removes is REMOVED, not re-pointed … Write the new claim as a new row in the work item's own fragment* |
| Two more coordinates that never parsed | `spec.md` §*The live instances* lists five, all in a `Code grounds` cell | Two more repaired in the same phase: the `test_what_the_reader_understands.py` fixture coordinate in `seal/ledger.md`'s eval row and the `CLOSED_WORDS` coordinate in its separator row, both in a Notes cell | Both are quoted locators with bare `"` inside, and `check_text` reads every anchor in a row, Notes included, so each was a claim meant to be checked and never was. The arm this work builds reads only the `Code grounds` cell, so it would not have named them; they were found by scanning every cell of every row (§12) |
| The `CLOSED_WORDS` coordinate | `plan.md` phase 1: *`\"` for the four quoted locators* | Cited by the constant's name, `chain_check.py#CLOSED_WORDS` | The one-line `CLOSED_WORDS = {…}` it quoted is no longer in the file: the set spans several lines and holds two more words. Escaping would have produced a coordinate that parses and resolves to nothing. It is a Notes coordinate and not one of the four `plan.md` counts |
| Rule (a)'s reach | `spec.md` §*In* item 1 (a): *still holds a `#` or `@` after every `ANCHOR_RE` and `OLD_COORD_RE` match in it is blanked* | A leftover, in a code span or a bare word alike, is a coordinate when, after every URL in it is blanked, it holds both marks, or a `#` with a path or a file name attached before it and a locator that is not digits only, or a path followed by `@` and a hex run. A word's closing punctuation is the sentence's. The build's rule (a span with one mark, a word with both) was replaced by round 1's fix, and round 1's (a `#` followed by a locator's first character, and no reading at all of a text holding `://`) by round 2's | Read literally, the spec's wording refuses prose: `#299`, `org/repo#299`, `@cache`, `#ifdef`, an address, a URL fragment. `spec.md`'s own wording of the class is *a coordinate somebody wrote that the pattern refused*, and a coordinate's own shape is a path before the mark. The second rule missed #299's own shape when the quoted line held a URL, a `path@hash`, and locators opening with a digit, a non-ASCII letter or nothing (round 2's 🟡 1). Each condition of the current rule is held by a case, and a mutation of each turns one red |
| How often a malformed text is counted | `spec.md` is silent; S1 asks for `1 malformed` on one row | Once per text as written, in a ledger file | `old_format_rows` counts its verdict that way, and `check_text` dedupes on the coordinate and hash, so the three counts on one line mean the same kind of thing |
| Where the row rule comes from | `spec.md` §*Data & interfaces*: *lives in the file, or loads from the shared reader with the same kind of fallback* | The second: `shared_reader` loads the reader once for `fence_rule` and `cell_rule`, and `vendored_split_row` is the fallback, held in step by a case | It is the arrangement the fence rule already has, for the same reason, and it keeps one row reader in the plugin's own copy |
| Cases beyond S1–S13 | `spec.md` lists S1–S13 | Two more S1 shapes (the bare minor anchor `seal/follow-up.md` measured, and `#<module>`), and three cases mutation asked for | Each added unit was mutated and five mutations left every listed case green (`phases/phase-2.md`) |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite | the sealer, once, after the review rounds settle |

## Not done

**#322 is closed as already fixed, and nothing was built for it.** The
docstring the issue cites became `r"""` in `97e29b7a` (#531, first shipped
in 0.14.0). Executed 2026-09-25: every tracked `.py` file (176) compiles with
warnings as errors under Python 3.12.11, with no error. `questions.md` Q2's
default (a) adds no lint guard for the class. The pull request can say
`Closes #322` on those grounds.

**A malformed coordinate outside the `Code grounds` cell is still silent.**
The arm reads one cell by design (`spec.md` §*Out*, `plan.md`
*Alternatives*). Phase 1 found two such coordinates, both in Notes cells, by
scanning every cell, and repaired them. Nothing will name the next one. The
same holds for a table whose header renamed the column. Both are stated in
`skills/evidence-check/SKILL.md` §*Known limits*.

**The records arm, `rider_check.py`, and a lint guard for #322's class stay
out**, as `spec.md` §*Out* sets. The records arm and `rider_check.py` read the
same coordinate shapes with the same silence over prose. The orchestrator
files an issue for them if the owner wants one.

**The advisor docstring's cost figure is not re-measured.** It is dated
2026-09-23 (1.7 s per commit). The new arm adds about 55 ms over this
repository's 33 ledger files. That is `malformed_rows` alone, in process,
beside `old_format_rows`' 318 ms, executed 2026-09-25. The figure is still
true as the dated measurement it states.

## Fed back into the spec

Inferred during implementation, for `docs/the-evidence-ledger.md` when
`settle` folds this item:

- Only a leftover the patterns refused is `MALFORMED`, and a leftover is a
  coordinate by its own shape: with every URL blanked, it holds both marks,
  or a path or file name with a `#` attached and a locator that is not
  digits only, or a path followed by `@` and a hash. An issue number, a
  directive, a decorator or an address beside a good anchor is not.
- A malformed text counts once per ledger file, like OLD-FORMAT.
- A table ends where its run of `|` lines ends. A header does not carry over
  a blank line.
