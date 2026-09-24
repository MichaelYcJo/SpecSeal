# 1790206435-the-sweep-reads-a-code-idiom-as-removed-wording — phase 1

<!-- seal/specs/1790206435-the-sweep-reads-a-code-idiom-as-removed-wording/phases/phase-1.md — what this phase
of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 476af109 |
| Ran by | smith on Fable 5.1 |

## What this phase was asked

A Python file's prose is its comments, docstrings and string literals
(#543): the tokenizer-based reader in front of `segments`, code tokens
replaced so a sentence ends where each stood with line numbers intact, a
tokenizer error falling back to today's whole-file reading; a docstring
section stating the rule; cases S1, S2, S4, S5, S6 red first, with the four
real 0.15.0 squash commits on `main` as fixtures, skip-when-absent; S6's
expected counts A 5 → 1, 0 5 → 4, C 2 → 1, B 9 → 9 with prose coordinates
unchanged; `questions.md` Q1, Q2 and Q6 filled.

## What this phase found

**B's range is 8 after the reader, not 9, and the frame's expectation did
not hold there.** The whole-file reading named `seal/ledger.md:2053` at 2.47
against a "corrected sentence" that was
`test_the_docstring_names_both_sides_of_the_round_record_exclusion`'s
docstring joined to three of its assert-message literals by the code between
them — three runs, one from each literal. Read one literal per sentence, the
best of those sources (`tests/test_a_corrected_sentence_survives_elsewhere.py:663`,
*is no longer the first exclusion stated*) shares one run at 1.00, under the
floor. That is the rule the phase was asked to build — a code token between
two literals ends the sentence — applied to the range side, where the frame
had only counted it on the pool side. Under `questions.md` Q2's *Moved*
option the case pins the new set and this record names the coordinate:
`seal/ledger.md:2053`, 2.47 before, 1.00 after, no longer reported. The
`survivors.md` row of `1790174139` that excused it (`seal/ledger.md` · *is no
longer the first exclusion stated*) now silences nothing and is not edited
(spec judgment 8). Phase 2's S12 expectation for B therefore starts from 8,
and the changelog coordinate's loss takes it to 7.

**Every other prose coordinate is unchanged, and every score moved up or
stayed** (Q2), which is the weighting doing what the frame said it would:

| Range | Before → after | Coordinates lost | Scores before → after |
|---|---|---|---|
| 0 `cbb5809..576fe39` | 5 → 4 | `chain_check.py:2960` (a function body) | 2.88 → 3.00, 2.77, 2.00, 1.88 |
| C `576fe39..cc49ae6` | 2 → 1 | `fold_ledger.py:358` (a `main` body) | 3.42 |
| B `cc49ae6..3dd2407` | 9 → 8 | `seal/ledger.md:2053` (above) | 3.00, 2.50 → 2.52, 2.00, 1.91 → 1.92 ×2, 1.70, 1.65, 1.61 → 1.62 |
| A `3dd2407..d2f2c0d` | 5 → 1 | the four #543 names | 2.00 |

Executed 2026-09-24 at `476af109` with
`python3 skills/code-review/scripts/survivor_check.py --range <c>^..<c> --root .`
for each of the four commits; the reports are in the scratchpad beside the
framer's, and the framer's four were reproduced byte for byte at `a5c5cadd`
before the build (§5).

**Q1 — the founding survivors.** Before and after the reader, identically:
#269's pin `tests/test_the_rules_have_one_owner.py` 2.00 (two runs, *record
from this report once* and *has verified its findings*), and #267's R3 1.89
in the fragment and 1.78 in `seal/ledger.md`. Nothing new is named on either
range. The `FLOOR` comment's 1.89 and 1.79 are the calibration-time figures
and were already stale before this phase; they are not edited, because the
comment records what the floor was set against. One thing did move: the
pin's coordinate is `:450` where it was `:447`, because a sentence now starts
at its first literal rather than at the head of the code block it sits in.
The founding case asserts the path, so it is unchanged.

**Q6 — how the kinds are named, and what a code token leaves behind.**
`PROSE_TOKENS` is `{COMMENT, STRING}` plus `FSTRING_MIDDLE` and
`TSTRING_MIDDLE` where the interpreter has them, read off `tokenize` by name.
Each code token leaves a `|` at its first character, which `END` already
splits on, so `segments` is untouched. `STRUCTURE_TOKENS` — blanked with no
`|` — is `INDENT`, `FSTRING_START`, `FSTRING_END` and the `TSTRING` pair. It
began as the ten-name list the plan implied, and a mutation showed `NL`,
`NEWLINE`, `DEDENT`, `ENDMARKER` and `ENCODING` cannot change any output: they
stand at a line's end, past its text, or on the next token's own column, and
`python_prose`'s position guard writes nothing there. They were removed
rather than left as members that claim a role they do not have; the comment
says so. The joining of two literals across a line break lives in the guard.
The refusal set is `tokenize.TokenError`, `SyntaxError` (which
`IndentationError` subclasses) and `ValueError`.

**S4 is asked of the reader rather than of a range.** The spec's Then clause
is phrased over a range, but the line it names — `"first half", name,
"second half"` — reads `first half name second half` under the whole-file
reading, so a removed sentence whose words are `first half second half` was
never carried by it and a range case would have been green before. The case
reads the sentence keys directly and was red first with the key
`first half name second half`; the end-to-end shape is covered by S1.

**Seen red first, executed 2026-09-24 against the script at `a5c5cadd`:**
S1 at exit 1 naming `other.py:1` at 3.00; S4 with the joined key above; S6
red on three of four ranges (B was 9 as the frame expected, so green); the
docstring case red. S2 (comment and docstring carriers) and S5 (an
unterminated triple-quoted string) were green before and after, as the
direction that must not move.

**Mutations of the new unit, executed at `476af109` from Python with the
file restored byte-identical each time:**

| Mutation | Cases run | Result |
|---|---|---|
| the fallback returns `''` instead of the file | S5 | red |
| a code token leaves a space, not `\|` | S4, S1 | red (S4) |
| `sentences` never calls `python_prose` | S1, S4, S6 | red (6 of 6) |
| `COMMENT` out of `PROSE_TOKENS` | S2, S6 | red (S2 comment, S6 A) |
| `FSTRING_END` out of `STRUCTURE_TOKENS` | the f-string case | red |
| `INDENT` out of `STRUCTURE_TOKENS` | the f-string case, #269's two | green — noise only, as the comment states; no case pins it |
| `NL` out of `STRUCTURE_TOKENS` (the list as first written) | #269's two | green — which is what removed it from the set |

**Cost.** The module went from 70 cases in 19.9 s to 81 in 42.8 s; the four
real-range cases are about five seconds each, because each reads a
390-file tree at its tip.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the whole-file reading of a `.py` file, as the sweep's only reading of one | `survivor_check.py` §*What a sentence is in a Python file* keeps it as the fallback for a file the tokenizer refuses, and S5 pins that |
