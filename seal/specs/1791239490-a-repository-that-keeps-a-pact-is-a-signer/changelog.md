### Changed

- Every repository of a work item that keeps a pact is now a **signer**
  (#822). The word it replaces was one a reader stops at, and every text the
  plugin ships, every printed line and every identifier now says `signer`:
  `docs/the-pact.md`, the skills, the templates, both READMEs, `pact-check`,
  `chain-check` and `evidence-check`. `pact-check`'s summary counts
  `1 of 1 signer read` and `N of M signers read`, and `chain-check` at the
  pact's repository says `which lists N signers`. `pact`, `pact change`,
  `pact review`, `pact anchor`, `pact-check`, the `Pact` and `Pact notify`
  rows and every path under `seal/` keep their names.

- A new pact's table is headed `| Signer |` (`templates/pact.md`), and a new
  pact review record's `| Signer | Change | Verdict |`
  (`templates/pact-review.md`).

- A pact written in 0.18.x, headed `| Signatory |`, and a pact review record
  written in 0.18.1 or later, headed `| Signatory | Change | Verdict |`, keep
  working with no edit. `pact-check` reads each exactly as it reads the new
  header and prints one line for each such file before its other lines,
  naming the file, the old header, the new one and 0.19.0. The line is in no
  exit class, so the exit is what the new header gives. At the pact's
  repository `chain-check`'s notice carries the same sentence and its exit
  status does not move. A file holding a table under the new header is read
  from it alone, and an old header beside it is refused (`pact-check` exit
  2, a notice from `chain-check`), because its rows would otherwise go
  unread: move them into the new table and delete the old one. An old header
  written directly under the new table, with no blank line, is a row of that
  table as GitHub renders it; it is refused once, as a line to delete, and
  never read as a signer (#830). Rename the header when the file is next
  edited; no command rewrites a pact.

- For a script that calls the plugin's readers: `hooks/config.py`'s
  `pact_signatories` is `pact_signers`, `SIGNATORY_HEADER` is
  `SIGNER_HEADER`, and `pact_signers` and `pact_reviews` now return a third
  value, the header they read (`None` where the text holds neither). Four
  test files under `tests/` are renamed with the word, as
  `test_a_signer_declares_its_pact.py`, `test_a_signer_records_a_pact_change.py`,
  `test_a_signers_ci_prints_its_pact.py` and
  `test_a_pact_anchor_is_no_coordinate_of_the_signer.py`.
