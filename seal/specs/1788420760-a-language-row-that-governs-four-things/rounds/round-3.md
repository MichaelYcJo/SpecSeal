# a-language-row-that-governs-four-things — review round 3

<!-- The verifying round for round 2's fixes (target: the diff
2b9f43b..adc3b9d). It answered the question it was asked with *yes, again* —
in the same commit, three lines from the constant it had just pulled out.
Round 4 verifies. Written by the review orchestrator, which implemented this
work item. -->

| Field | Value |
|---|---|
| Target SHA | the fix diff from 2b9f43b, reviewed at adc3b9d |
| PR | none yet |
| Broad gate | not yet — round 4 verifies these fixes |
| Fixes checked by | round-4 |
| Contract changes | `chain_check.verdict_table` reports through `VERDICT_COLUMN` → `chain_check.main` |
| New units | none — five names added to an existing derivation |
| Needs a fix | yes — 🟡 1 (🔴 went on the list by hand while its constant sat three lines below the one that was derived, and four more deferred as *no constant* have constants) |

- [ ] Pass

## What this round was asked to attack

One question: **round 2 found a fix deriving one level and leaving the next by
hand. Did this fix do it again?** Then five places — `VERDICT_COLUMN` as a
real contract change in a checker; whether `ROUND_RECORD_FIELDS` is itself
hand-written and checked against anything; whether any literal's backticked
form is a substring of another; a sixth way the skill could grow a move; and
whether case-folding the strip introduces a false positive.

## The answer

**Yes, again.** `VERDICT_COLUMN` was pulled out of `chain_check.py` so the
derivation could reach it, and `BLOCKING = "🔴"` — three lines below it — was
added to the list by typing the emoji. Deleting it left every case green.

And round 2's own deferral was wrong about its cost. Four of the seven strings
it recorded as having no constant have one: `NO_FIXES`, `NOBODY`,
`PR_FIELD` and `unverified_check.CLOSED`. The deferral said the fix was *a
change to three scripts*; it was five lines in one test file and two
backticks in a document. **A deferral is a decision somebody makes from the
cost written beside it.**

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| r2 🟡 1 | the list had lost `Needs a fix` and three headings | `templates/config.md` | answered — reproduced | reviewer deleted each in turn against the new pinned-case derivation |
| r2 🟡 2 | `Verdict` on the list, pinned by nothing | `chain_check.py` | answered — and one message still spelled the column by hand, fixed at 133ddf3 | reviewer checked no other site matches that column, and that `.lower()` → `.casefold()` is identical on all four spellings of an ASCII header. 159 cases across three caller files pass |
| r2 🟡 3 | `fixed` held by `agreed, fixed` | `tests/…` | answered — reproduced | reviewer deleted the standalone entry: red. No literal's backticked form is a substring of another |
| r2 🟡 4 | 🔴 unlisted | `templates/config.md` | **answered at the coordinate and unpinned** — this round's 🟡 1 | reviewer deleted the phrase: green |
| r2 🟡 5, 🟡 6 | #105's two assertions | `tests/…` | answered — see that work item's record | reviewer ran six mutations |
| 🟡 1 | 🔴 is on the list and `chain.BLOCKING` is not in the derivation. Four more the previous round deferred as having no constant — `NO_FIXES`, `NOBODY`, `PR_FIELD`, `CLOSED` — do have one, and three of those four were unpinned as well. The deferral's recorded cost was wrong by an order of magnitude | `tests/…`, `templates/config.md` | fixed at 133ddf3 — five names added, the two emoji backticked so the assertion's delimited form reaches them, and the message that spelled `Verdict` by hand now reads the constant | reviewer executed each deletion. Orchestrator reproduced four of them and confirmed each reddens naming its own string |
| ❓ 2 | three strings are still matched with no constant to derive from — `Pass`, `round-N` and the `<!-- specs/… -->` marker, each behind a regular expression | `chain_check.py`, `fold_ledger.py` | deferred — a regular expression has no literal to name, and giving each one would be a change to the checkers for a list now checked from two directions | the repository owner |
| 🟢 3 | `_governs_nothing()`, the backticked assertion, and the case-folded strip | — | pass | reviewer executed each; folding removes a false positive rather than adding one |

## Executed probes

| What was run | Result |
|---|---|
| reviewer: the 🔴 phrase deleted from the list | green — 🟡 1 |
| reviewer: `NO_FIXES`, `NOBODY`, `CLOSED` deleted | green each; `PR` red, already held by the pinned-case derivation |
| reviewer: `.lower()` against `.casefold()` on four header spellings; three caller files | identical; 159 passed |
| reviewer: every literal's backticked form against every other | no substring collisions |
| reviewer: six moves inserted into the skill | `cp -r` and `shutil.copytree` green — #105's finding |
| orchestrator: four list deletions and three move insertions | each reddens its own case |
| orchestrator: full suite, `ruff check .`, `ruff format --check .`, `evidence_check --strict` | 1647 passed · 1 skipped; clean; 85 files; 455 ok · 0 drifted · 0 broken |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| rounds 1–2 | `templates/config.md`'s *What no row governs* and its two derivations | changed in every round |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Three strings behind regular expressions with no literal to derive | this record | the repository owner |
| The mirror paragraph; whether `routing.md` and the todo files are governed | round 1's record | the repository owner |
