### Fixed

- **A `seal/config.md` row written twice, and a config that will not read,
  now get one answer everywhere (#867).** A row written twice used to be
  read first-wins by most readers, last-wins by the ledger checker, and
  written first by `seal mode`, so a person could edit the row they saw
  while another one answered. Now it has no value: `evidence-check
  --reverify`, `correction-check`, `fold-check`, `broad-gate` and `seal
  mode` stop at exit 2 naming the row and how many times it is written, and
  `seal mode` names each line. A `config.md` that is there and cannot be
  read as UTF-8 — a directory of that name, bytes another encoding wrote —
  is refused the same way, naming the path, instead of being read as an
  empty config; an absent file still declares nothing. That matters most
  for `Ledger frozen from`: an unreadable config used to turn the freeze
  off, so `--reverify` re-stamped released rows in place. Hooks say
  nothing about either state: the mode gate stays silent rather than
  asking. In a `routing.md`, a `Review`, `Destination` or `Branch` row
  written twice makes the file no declaration, so the commit gate asks; a
  doubled optional row reads as unanswered.

- **The ledger coordinate has one grammar (#867).** `correction-check`,
  `settle` and the rider check read the checker's own pattern instead of
  copies. `correction-check` now names a dropped correction of a row
  anchored on a path with no extension (`bin/test`) or on a quoted heading
  holding a code span or `\|`, which it could not see before, and no longer
  takes a malformed example quoted in a row for a coordinate.

- **A markdown heading has one spelling, CommonMark's (#867).** A line
  beginning `#120)` used to end a round record's `## Verdicts` or an
  overview's `## Not verified` section above the rows below it, so those
  rows went uncounted. The ledger checker no longer reads a `## B` quoted
  inside a code fence as a heading, so a section anchor runs to the
  section's real end and an example heading in a fence is no anchor. A
  heading indented up to three spaces is a heading. Some released
  heading-path rows drifted once because their section's end moved; a
  repository that freezes its ledger re-reads them with `--reverify --into`,
  and one that does not with `--reverify`.
