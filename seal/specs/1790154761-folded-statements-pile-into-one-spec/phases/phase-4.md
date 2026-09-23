# 1790154761-folded-statements-pile-into-one-spec — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | aebb98ae |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Write the `changelog.md` fragment, the ledger fragment
`seal/ledger/1790154761-folded-statements-pile-into-one-spec.md` (the three
test modules' units, settle §2, the evidence-ledger paragraph, the Korean
section) and `overview.md`, with `## Not verified` naming the broad gate and
the sealer as its answerer. Carry Q1, Q2 and Q4's defaults into the overview.

## What this phase found

- **Phase 1's edit drifted two rows in the shared `seal/ledger.md`.** Both
  anchor inside `CONTRIBUTING.md`'s `## House rules`, where the README rule
  was widened. `evidence-check --strict .` exited 2 on them. Both claims were
  re-read and still hold (the fold-refusal sentence is unchanged, and C8's
  `a8` case was executed green), so `--reverify` over `seal/ledger.md` moved
  both hashes and each row got a `Re-read 2026-09-23` marker. The strict
  check then exited 0.
- **A minor anchor holding escaped backticks did not resolve.** The first E1
  anchor into `CONTRIBUTING.md` quoted the rule's opening line with
  `` \`.ko.md\` `` in it, and `--reverify` left it as DRIFTED. It now quotes a
  line of the same paragraph that carries no backticks.
- `unverified-check` on the overview reads 3 open rows and exits 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
