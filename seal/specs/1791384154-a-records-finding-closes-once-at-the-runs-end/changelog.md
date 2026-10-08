### Changed

- **A ⬜ note no longer costs a fix pass and a reader in every round: it is
  carried open and closed once, at the run's end (#837).** A note is a
  finding that reads badly while the behaviour and the fact stay right. It
  used to take a row in its own round's fix table, and a note closed `fixed`
  commissioned a verifying round for a sentence — on one run five notes were
  a record's only fix words and spent the run's one reopening. Now `close`
  leaves a note open and refuses a fix-table row for one, and `new` and
  `close` say how many notes the run carries. When the run has ended — its
  last record reads `Fixes checked by | no fixes to check` —
  `round-record notes --item <dir> --fixes <table> --at <sha>` closes every
  open note of the run in one pass, from a table that names the round beside
  the id, `| Round | # | Verdict | Commit or grounds |`, with the words
  `corrected`, `answered` and `deferred <home>`. A corrected note is written
  `answered` with `corrected at <sha>` as its grounds; `fixed` is refused.
  `notes` refuses before the run's end, `seal` refuses while a note of the
  run is open, `new` refuses a redesign's first record while the stopped
  run still carries one, and `chain-check` fails a ready pull request over
  an open note and, for a work item begun at or after `1791384163`, over a
  note closed `fixed` — every 0.21.0 work item is before that and prints. A record whose only open rows are notes now reads
  `no fixes to check` rather than waiting on a reader nothing commissioned.
