### Changed

- The sealer's stamp is a letter (#717). The panel's text is written on a
  parchment sheet, one blank line inside it at the top and the bottom, and
  a wax disc is pressed over the sheet's lower right corner, half below its
  last line and half over its right edge, two clear cells from every line
  of text. The rope ring and the outer light-red band are gone; the
  fleur-de-lis is pressed into the wax in one red, lit from the upper left.
  The disc keeps truecolour, and the sheet, its edge, the ink and the red
  `SEALED` title are 256-colour codes. The owner chose the drawing, its
  colours and the 0.90 scale from renderings. Over the values of #702's
  seal the hook's message is 6,277 characters where it was 10,171. The
  letter twin a console that is not UTF-8 gets is the same footprint: `|`,
  `.---.` and `'---'` for the sheet, `m . G Y y` for the disc.

- The `Stop` hook holds its whole message under a budget, so the harness
  never replaces a stamp with a 2 KB preview of a file again. Measured with
  a scratch hook on Claude Code 2.1.287, the harness persists a
  `systemMessage` longer than 10,000 characters, counted as characters and
  not bytes. The hook keeps 1,000 of them back for the gate-failure report
  that can be prepended to the same message, and where a message is over
  9,000 it draws every stamp in it one rung smaller together — 0.90, 0.80,
  0.75 — and last without the disc. A stamp can come out smaller than its
  values file's `scale` says, or without its disc, and is never left
  undrawn. `seal-stamp` and the gate's own terminal drawing are not
  budgeted.

- A `SEALED` panel says only what a `SEALED` stamp can say. `chain  exit 0`,
  the suite's `exit 0` beneath its counts, the ledger's `0 drifted . 0
  broken` beneath its `ok` and every blank row are gone, because a drawn
  panel is green by construction. The counts stay, and `exit N` stays where
  a row has no count. `workflow  <n> of <m> not answered` reads
  `CI also  <n> more steps`; the total stays on the stderr line beside the
  step names. The `NOT SEALED` form keeps every arm's exit code.

- **Until 0.17.0 is installed, the installed 0.16.0 hook draws this release's
  values files with its own drawing**, rope and gold over the new rows. A
  person who wants the letter before then runs the tree's
  `skills/verify/scripts/seal_stamp.py --from <file>` by path, because
  `seal-stamp` on the PATH is the installed copy too.
