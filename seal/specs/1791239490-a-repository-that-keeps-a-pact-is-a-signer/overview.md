# 1791239490-a-repository-that-keeps-a-pact-is-a-signer — overview

📋 implement applied
· spec:     spec.md, plan.md, questions.md of this work item; docs/the-pact.md; docs/the-evidence-ledger.md §*A released row is read again in the branch's fragment*; seal/config.md
· evidence: seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md — 28 `Corrected ·` rows, 39 `Re-read ·` rows, 7 new rows (R1-R7)
· verified: executed — each phase's slice and the mutation breaks named in phases/phase-1.md, phase-2.md, phase-3.md; unverified — the full suite, lint and typecheck (the sealer)

## Why this work exists

`signatory` was a word a reader stops at; `signer` replaces it in every live
text, and a pact or pact review record written under the old header keeps
working with a printed line instead of a refusal.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| S4's two tables | spec: "a `\| Signer \|` table and, below, a `\| Signatory \|` one / the `Signer` table is read, the other is not" · code: the `Signer` rows are read and the old table is refused wherever it stands — below under a heading, above under a heading, above after a blank line (one refusal naming the old header, `read_table`), and directly below with no heading (the walk's stray-row refusal, which already names it). The spec covered "below" only; the "above" shapes were met in round 1 | refused, never silent | a file with two tables comes from no rename, and reading one while the other's rows go unread drops a signer at exit 0 (round 1 of #822, yellow 1). Corrected in round 1's fix pass: this row first said the heading shapes were read silently, and omitted the "above" shapes |
| The old tuple and the rename sentence | spec §*Data & interfaces*: "the old tuple and the rename sentence as module constants in one unit" · code: one function, `hooks/config.py#renamed_header`, derives the old header from the new one and builds the sentence; `RENAMED_IN` is the one module constant | a function | one unit writes the old word once, for both headers, and the sweep excludes that unit by name; two constants per header would have written it twice and left a pair for the exclusion to name (added in round 1's fix pass, white 4) |
| `tests/test_one_word_one_meaning.py` in phase 1 | plan: the sweep's file moves in phase 2 · code: its `PACT_PRINTED` identifiers and pinned definition sentence moved in phase 1, the sweep in phase 2 | split | phase 1 removed `pact_signatories` and `_signatory` and changed the pinned sentence; leaving the module for phase 2 would have committed it red · NAME NOT IN TREE |
| Where the sweep holds the old word | spec item 8 and plan: `PACT_LOOSE` gains `signator(?:y\|ies)` · code: a separate `PACT_RENAMED` and its own case, `PACT_LOOSE` unchanged | separate | the two excluded spans would otherwise also drop out of the `home`/`member`/`keeper` sweep; the separate constant excludes them from the old word alone (`phases/phase-2.md`) |
| Two drift-only released rows | plan: one `Corrected ·` row per family whose anchor moved, the rest re-read · code: P11 (0.18.0) and E6 (0.18.2) also take a `Corrected ·` row, though no anchor of theirs moved | `Corrected ·` | each claim named the old word as a fact, so a re-read would have dated a claim false as written (`phases/phase-3.md`) |
| S11's exact list | spec: the live hits are the config unit, the compat statement, the fold markers and this work item's files · tree: the compatibility test cases spell `\| Signatory \|` as well | the cases spell it | a case that took the old header from `hooks/config.py#renamed_header` would pass with that constant changed while every 0.18.x pact stopped reading; the literal is what pins the compatibility (`phases/phase-2.md` lists each file) |

## Not verified

| Item | Who must answer |
|---|---|
| the full suite, the repository-wide lint and the typecheck over the finished branch | the sealer, once, after the review rounds settle |

## Not done

Nothing.

## Fed back into the spec

- `docs/the-pact.md` §*The words* gains the statement under this work item's
  marker: an old header reads, `pact-check` names the rename in no exit class,
  and `chain-check`'s notice carries the sentence. Inferred during
  implementation where it says a `Signer` table that will not read is refused
  as it stands rather than falling back.
