# Survivors — a repository that keeps a pact is a signer

This range renamed the pact word `signatory` to `signer` in every live text,
and removed the sentences that used the old word. `survivor-check --range
e6d5a05..5670147b` named one place that still shares wording with what it
removed.

- **A released record.** A row of a released ledger file states the tree at
  the release it shipped in. This repository declares `Ledger frozen from`,
  so a released row is never edited, and the rename's own decision (spec
  §*What does not change*) keeps released records in the word they were
  written with. Where the rename moved the code a released row cites, the
  row is re-read or corrected in this item's fragment instead.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.18.0.md` | `declared_pacts`, which `pact-check` reads a signatory's rows through | released row of 0.18.0, frozen; its claim is still true of the code under the new word, and the fragment re-reads it rather than editing the released file |
