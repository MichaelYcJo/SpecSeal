### Fixed

- `survivor-check` no longer lets a work item's own `survivors.md` silence the
  survivors it quotes. The file is out of the search on both sides — the pool
  it reads at the tip and the range it measures — so a row's quote is neither
  wording the fix wrote (which subtracted the survivor before `--exempt` was
  read, #507) nor one more carrier of the phrase (which diluted the score
  under the floor, #308). A survivor is found, the row is read against it,
  and it prints under `exempt` with the row's grounds; a range that edits
  only the exemption file removes no sentence. On three pull requests of one
  release the file had silenced 29 of the 36 rows written into it; over the
  same three ranges 14 rows now print and the rest match nothing at that
  range, with or without the file.
- A work item's `phases/phase-N.md` is out of the survivor sweep on both
  sides too, the way a round record already was: it records what a phase was
  asked, found and removed, so wording it quotes is neither a survivor to
  correct nor a correction to chase. Before, a phase record carrying the old
  wording was reported beside the real survivor and diluted it, and a phase
  record the range closed subtracted what it quoted. What the sweep gives up
  with that — a correction hidden in an HTML comment beside a claim still
  rendered in bold, which it caught once only because the record was in the
  pool — is named in `seal/follow-up.md`.
