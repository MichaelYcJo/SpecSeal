# a-language-row-that-governs-four-things — review round 2

<!-- The verifying round for round 1's fixes (target: the diff
9a28262..2b9f43b), reviewed with #105 on one branch. Round 1's ten all landed
at the coordinates they named; this round found the fix's own derivation
hand-written one level up, and a field removed from the list it was fixing.
Round 3 verifies. Written by the review orchestrator, which implemented this
work item. -->

| Field | Value |
|---|---|
| Target SHA | the fix diff from 9a28262, reviewed at 2b9f43b |
| PR | none yet |
| Broad gate | not yet — round 3 verifies these fixes |
| Fixes checked by | round-3 |
| Contract changes | `chain_check.verdict_table` and `verdict_row` match the column through `VERDICT_COLUMN` → `chain_check.main`, `tests/test_chain_hooks.py` |
| New units | `chain_check.VERDICT_COLUMN`, and one parametrised case |
| Needs a fix | yes — 🟡 1 (the list lost `Needs a fix` and never held three section headings), 🟡 2 (`Verdict` is on the list and pinned by nothing), 🟡 3 (`fixed` is pinned by `agreed, fixed`), 🟡 4 (🔴 is read and unlisted), 🟡 5 and 🟡 6 belong to #105 |

- [ ] Pass

## What this round was asked to attack

One question: **is the derived list actually derived, or does it only look
derived?** Then five places — the derivation's own hand-written set of
constant names against every literal both checkers match; whether the section
slice can silently become empty; which literals are substrings of one another;
whether the eight-document list is complete and its strip sound; and whether
#105's two replaced assertions are still satisfiable with the claim false.

## The answer

**Derived one level down and hand-written one level up.** `_literal_strings()`
reaches fourteen strings by naming constants by hand, and seven more are
matched literally with no constant to reach. The same fix that derived the
list **removed `Needs a fix` from it** and added `Broad gate` on identical
grounds — neither is in any checker, both are read by the pinned case that is
the other half of the list's stated grounds, and nothing was checking that
half.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r1 🔴 1, 🔴 2, 🟡 5, 🟡 6 | the missing literals and the wrong verdict word | `templates/config.md` | answered — and the list lost a field in the same commit, which is 🟡 1 | reviewer compared the section against every module-level constant in both checkers |
| r1 🔴 3, 🔴 4, 🟡 7, 🟡 10 | the two READMEs, the review skill, the eight-document case, the pipes | — | answered — reproduced | reviewer read each and ran five strip mutations against the document case: four red |
| 🟡 1 | the fix removed `Needs a fix` and added `Broad gate` on identical footing — neither is in any checker, both are read by `ROUND_RECORD_FIELDS`, which is the *pinned case* half of the grounds round 1 widened the heading to include. Three headings that case reads were never on the list | `templates/config.md`, `tests/…` | fixed at adc3b9d — the field and the three headings are back, and a second parametrised case derives from that pinned list | reviewer compared the section against `ROUND_RECORD_FIELDS`: seven of eleven present. The new case reddens naming each missing field |
| 🟡 2 | `Verdict` was on the list with nothing pinning it: `chain_check.py` matched it as a bare `"verdict"` at three call sites, so the derivation had no constant to reach, and `"Verdict" in section` would have been satisfied by `## Verdicts` anyway | `chain_check.py:959,972`, `templates/config.md` | fixed at adc3b9d — `VERDICT_COLUMN`, matched case-folded at all three sites, and derived | reviewer deleted the column's mention from the section: green. It reddens now |
| 🟡 3 | `fixed` was held by `agreed, fixed` alone — deleting the standalone entry left the case green. The section spells every literal in backticks, so the delimited form closes it | `tests/…` | fixed at adc3b9d — every literal asserted backticked | reviewer executed the deletion |
| 🟡 4 | `chain_check.py` reads 🔴 from a record and the list names only the ✅ that closes a row. The risk is small and the asymmetry is the finding | `templates/config.md` | fixed at adc3b9d | reviewer read |
| 🟢 5 | `_governs_nothing()` cannot silently truncate | — | pass | reviewer ran three mutations — the heading renamed, the section moved last, a fenced `## ` inside it — each turning all fourteen cases red loudly |
| 🟢 6 | `ROW_READERS` is complete | — | pass, with one hole fixed | reviewer grepped the shipped files: three others touch the words and none tells a session which row to read. The lower-case spelling survived the strip, and is the one that exists in this tree — closed at adc3b9d by case-folding |
| ❓ 7 | seven strings are matched literally with no constant to derive from — `no fixes to check`, `nobody`, `PR`, `Pass`, `round-N`, `✅`, the `<!-- specs/… -->` marker. All are on the list; the list is again the only thing holding them | `chain_check.py`, `fold_ledger.py` | deferred — giving each a constant is a change to three scripts for a list that is now checked from two directions | the repository owner |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: every module-level string constant in both checkers against the derivation and the section | fourteen derived; 🔴 neither derived nor listed; seven listed but underived |
| reviewer: `ROUND_RECORD_FIELDS` against the section | seven of eleven present — 🟡 1 |
| reviewer: each of the fourteen literals deleted from the section in turn | thirteen red, `fixed` green — 🟡 3 |
| reviewer: the `Verdict` mention deleted | green — 🟡 2 |
| reviewer: the heading renamed, the section moved last, a `## ` inside a fence | all fourteen red, three times |
| reviewer: five `Pull request language` mutations on a row reader | four red, lower-case green |
| reviewer: six mutations of `skills/config/SKILL.md` | two red, four green — #105's 🟡 5 and 🟡 6 |
| orchestrator: seven mutations, one per fix | each reddens its own case, naming the missing string or field |
| orchestrator: full suite, `ruff check .`, `ruff format --check .`, `evidence_check --strict` | 1642 passed · 1 skipped; clean; 85 files; 455 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 1 | `templates/config.md`'s *What no row governs*, `tests/test_the_pull_request_language_is_the_repositorys.py`'s derivation | the list and its two derivations, changed in both rounds |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Seven literals matched with no constant to derive from | this record | the repository owner |
| The mirror paragraph under *What no row governs*; whether `routing.md` and the two todo files are governed | round 1's record | the repository owner |
