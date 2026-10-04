### Fixed

- A `Pact` or `Pact notify` row in `seal/config.md` that the table's reader
  does not reach is now refused, never read as the default (#759). Before, a
  `| Pact notify | always |` written below a blank line that ended the table
  was read as `when the pact is touched`. `evidence-check --reverify` then
  re-stamped a moved ledger row citing no clause and recorded no pact change.
  That re-stamp cleared the drift that was the only trigger for the record.
  The reader now compares every line shaped as either row with a value
  against the lines it took as rows, as `str.splitlines` cuts the file and as
  GFM does. It refuses each such line in a sentence that names the line and
  says where it goes, and `Pact notify` then has no value. So `--reverify`
  leaves the moved row at exit 1, `pact-check` at the pact's repository exits
  2, and a signatory's CI prints a notice without moving its exit. A row
  with no leading pipe directly under the table, which GFM shows as one of
  its rows, is refused too. So is an item spelled with an invisible format
  character such as U+200B, which the sentence shows as its code point. A
  `Pact` row the reader does not reach always refuses. A `Pact notify` row
  it does not reach refuses only where a `Pact` value stands. A row inside a closed code fence or a closed HTML
  comment is an example and is not refused.

- A vendored copy of `evidence_check.py` looks for the two rows as GFM cuts
  the file as well as line by line, with or without a leading pipe and with
  format characters removed, so it leaves a moved row wherever the
  plugin's reader now refuses a notify row (#759). Before, a `Pact notify`
  row holding a character only `str.splitlines` ends a line at was missed,
  and the copy re-stamped the row unrecorded.
