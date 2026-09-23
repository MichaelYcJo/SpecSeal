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
