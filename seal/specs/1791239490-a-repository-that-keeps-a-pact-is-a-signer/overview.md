# 1791239490-a-repository-that-keeps-a-pact-is-a-signer — overview

📋 implement applied
· spec:     spec.md, plan.md, questions.md of this work item; docs/the-pact.md; docs/the-evidence-ledger.md §*A released row is read again in the branch's fragment*; seal/config.md
· evidence: seal/ledger/1791239490-a-repository-that-keeps-a-pact-is-a-signer.md
· verified: see phases/phase-1.md, phase-2.md, phase-3.md

## Why this work exists

`signatory` was a word a reader stops at; `signer` replaces it in every live
text, and a pact or pact review record written under the old header keeps
working with a printed line instead of a refusal.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| S4's two tables | spec: "a `\| Signer \|` table and, below, a `\| Signatory \|` one / the `Signer` table is read, the other is not" · code: read from `Signer` alone where a heading stands between; directly below with no heading, the old rows are refused as rows past the table's end | the walk's existing rule | `hooks/config.py#gfm_table` refuses every `\| … \|` line after a table's end and before the next heading (round 3 of #735); moving that is not this work's, and the case pins all three shapes |
| `tests/test_one_word_one_meaning.py` in phase 1 | plan: the sweep's file moves in phase 2 · code: its `PACT_PRINTED` identifiers and pinned definition sentence moved in phase 1, the sweep in phase 2 | split | phase 1 removed `pact_signatories` and `_signatory` and changed the pinned sentence; leaving the module for phase 2 would have committed it red · NAME NOT IN TREE |
| Where the sweep holds the old word | spec item 8 and plan: `PACT_LOOSE` gains `signator(?:y\|ies)` · code: a separate `PACT_RENAMED` and its own case, `PACT_LOOSE` unchanged | separate | the two excluded spans would otherwise also drop out of the `home`/`member`/`keeper` sweep; the separate constant excludes them from the old word alone (`phases/phase-2.md`) |
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
