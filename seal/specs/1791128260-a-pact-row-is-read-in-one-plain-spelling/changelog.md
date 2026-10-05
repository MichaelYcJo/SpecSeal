### Fixed

- A `Pact` or `Pact notify` row in `seal/config.md` is now read in one
  spelling, and every other line of that file that names a pact is refused
  (#759). Before, a `| Pact notify | always |` written below a blank line that
  ended the table was read as `when the pact is touched`, and so was a row
  whose item said `pact notify`, `**Pact notify**` or `` `Pact notify` ``.
  `evidence-check --reverify` then re-stamped a moved ledger row citing no
  clause and recorded no pact change, and the re-stamp cleared the drift that
  was the only trigger for the record. The reader now takes a row of the
  `| Item | Value |` table whose item is exactly `Pact` or `Pact notify`. Any
  other line that names a pact and holds a `|` is refused in a sentence naming
  the line: below the table, in a second table, in a block quote, in a fence
  or an HTML comment, or cut by a character only Python ends a line at. A row
  of the table whose item names a pact in another spelling is refused too.
  "Names a pact" is the letters `p`, `a`, `c`, `t` in order with only
  non-letters between them, as written or with character references decoded,
  so markup, invisible format characters and references inside the word are
  read through, and `impact` is not a pact. A refusal leaves `Pact notify`
  with no value: `--reverify` leaves the moved row at exit 1, `pact-check` at
  the pact's repository exits 2, and a signatory's CI prints a notice. A line
  with no `|` is not refused, so the pact can be named in prose. A letter
  written between the word's letters, such as `P<b></b>act`, or a look-alike
  letter from another script is not caught; `docs/the-pact.md` says so.

- A vendored copy of `evidence_check.py` reads `seal/config.md` by the same
  word and the same predicate as the plugin's reader. It leaves a moved row
  citing no clause wherever a line names a pact and is neither a plain
  `| Pact | … |` nor a plain `| Pact notify | … |` row, as well as where both
  plain rows carry a value. Before, it looked for one row shape line by line
  and missed a notify row spelled with markup, a format character, or a
  character only Python ends a line at, and re-stamped the row unrecorded.
