# 1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

📋 implement applied
· spec:     this work item's spec.md (items 1-12, S1-S14), plan.md (phases 1-6, Technical context), questions.md (Q1-Q13); CLAUDE.md §the fragment rule, §no real identifiers, §whose; seal/config.md (Fold shape from, Over the ceiling); skills/implement/SKILL.md §Document layout; docs/the-evidence-ledger.md; templates/config.md, templates/sdd-phase.md, templates/sdd-overview.md
· evidence: seal/ledger/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it.md P1-P11 added; 49 rows re-read and noted in seal/ledger.md and seal/releases/0.4.0, 0.5.0, 0.6.0, 0.8.3, 0.9.1, 0.9.3, 0.12.0, 0.13.1, 0.14.0, 0.15.3, 0.15.4, 0.15.5, 0.16.0 and 0.17.0, two corrected in place
· verified: executed — every new case seen red (stash or mutation-check), each phase's modules naming its files green, the three hygiene modules green, evidence-check --strict and fold-check exit 0, ruff on every touched Python file; unverified — the full suite, the repository-wide lint and typecheck (the sealer's)

## Why this work exists

A work item that commits in several repositories gets one routing answer in
each, a signatory names the pact it signs, and `pact-check` at the pact's
repository says where the signatories disagree with it.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where `normalise_remote` lives | `plan.md` §*Technical context*: "Their parsing and vocabulary live in `hooks/config.py`" and "`skills/implement/scripts/seal.py#normalise_remote` … Import it. Do not copy it." The code moved the function into `hooks/config.py` and left `seal.py` an alias | moved, with the alias | `seal.py` imports `hooks/config.py` by plain name, so the reader importing `seal.py` is a cycle, and `hooks/config.py`'s docstring: "`skills/implement/scripts/seal.py` … is a two-thousand-line command that a `PreToolUse` hook must not import -- so the READER moved here and the writer stayed there, and `seal.py` re-exports these names rather than keeping a second copy." One normaliser stays, which is what the plan's sentence protects |
| How many rows `/specseal:config` shows | `plan.md` phase 1: "`skills/config/SKILL.md`'s row table gains both rows, and every count of that table's rows is corrected (it says *all seven*)". The code added a third row, `Reference specs`, and says ten | ten | `templates/config.md` has shipped `Reference specs` since #688 and the skill's procedure is "Show every row, present or not". Nine would have been a second false count |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck at this branch's tip | the sealer, once the review rounds settle |

## Not done

- **#647's steps C and D**: the record of a pact change (`contract-changes`)
  and its trigger on a drifted signatory row, and the contract review. They
  are the second work item, stacked on this branch; `Pact notify` is read and
  printed and nothing acts on it.
- **No check that every share carries one id.** Stated in
  `orchestration.md` and `docs/the-pact.md` with the reason: an id minted
  twice cannot be told from a signatory's own work item citing the pact.
- **The code's `home`**, which names a `seal/` root in `pact_check.py` and
  `chain_check.py` as it does across this tree, was left as it is; S13 sweeps
  the shipped prose, where the owner's rule applies.

## Fed back into the spec

Clauses this work added, *inferred during implementation*, which a planner
may overturn:

- `hooks/config.py#pact_signatories` reads the pact's `| Signatory |` table
  through `config_rows`' walk; an absent table, an empty one and the
  template's unfilled row are refused. Spec item 8.1 said `pact-check` reads
  the table and named no reader.
- `pact-check` statuses beyond the five anchor verdicts: `NOT FOUND` (exit 1),
  and `ONE-SIDED`, `REFUSED` and `UNREADABLE` (exit 2). A signatory with no
  `seal/` root is `ONE-SIDED`. A map line is trusted only where the checkout
  it names has the signatory's origin, and two siblings with that origin are
  named and not chosen between.
- Each signatory read prints a `READ` line carrying its `Pact notify` value,
  which is how spec item 3's *prints it* is met at the pact's repository.
- "Another ref" is every branch, remote-tracking branch and tag HEAD does not
  hold; the ref named is the first such one holding the version.
