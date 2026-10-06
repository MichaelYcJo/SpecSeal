### Fixed

- When a pact's or a pact review record's old 0.18.x header sits directly
  under the new table, with no blank line above it, `pact-check` now quotes
  that line as the file holds it (#831). A `|Signatory|` line written without
  its spaces used to be named as a `| Signatory |` line, which a person
  searching the file for it would not find. The sentence and its remedy,
  delete the line, are otherwise unchanged.

- The check that keeps the word 0.19.0 renamed out of live text again sweeps
  whatever follows `docs/the-pact.md`'s statement about the old header
  (#831). A list item, a block quote, a fenced block, an HTML block, a
  thematic break or a setext underline directly under the statement's last
  line used to stay exempt with it.
