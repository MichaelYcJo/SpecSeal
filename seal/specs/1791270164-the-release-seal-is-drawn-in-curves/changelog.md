### Changed

- **The terminal seal is a 28-cell wax disc beside the run's text, with no
  sheet behind either (#832).** The stamp used to be a parchment sheet with
  the run's rows written on it and a red lily pressed over its corner. It is
  now two things on the terminal's own background: at the left a disc 28
  cells across and 14 lines tall, with a wax edge, a rim lit from the upper
  left, a groove and the field, every cell one of nine flat colours; and
  three columns right of it the text, a bold red `SEALED` and a dim rule,
  then the rows with dim labels. Nothing outside the disc is painted, so the
  text takes the terminal's own colours, whatever its theme. The block form writes a colour code only where
  something changes. The letter twin for a console that cannot draw
  half-blocks writes nine letters for the disc and the text in ASCII.

- **The disc's mark is a placeholder S, held in one file.** The mark is
  Georgia Bold's S on a 28 × 28 chart, `skills/verify/scripts/seal-mark.txt`,
  which the stamp reads when it loads and refuses with a sentence where the
  file is not that shape. The mark the seal will carry is chosen in #857;
  changing it is replacing that one file.

- **The rows read the way the owner drew them.** `base` shows its commit and
  its ref on one line. A blank line stands between what was sealed and what
  was run, and the result rows carry a green `✓`: `suite ✓ 6621 passed · 11
  skipped`, `ledger ✓ 3451 ok · 0 drifted · 0 broken`, and `chain ✓ exit 0`
  is back. `CI also` takes a dim `·`, and `·` and `→` replace the ASCII
  separators. A value may be 41 columns wide, so the widest stamp stays
  inside an 80-column terminal. A values file an older gate wrote still
  draws, in its old row shapes.

- **One sealed run's stamp goes out per `Stop` message.** A real run's stamp
  is about 5,300 UTF-16 units with the 28-cell disc, so the hook carries one
  per message and a second seal of the same turn arrives at the next one, as
  it did in the lily's day. A stamp too large for its disc alone is still
  drawn as the text with no disc.

- **The release note's seal is the owner's own drawing.** It used to be the
  terminal stamp blown up cell for cell, so every edge was a staircase. It
  is now the owner's 32 × 32 SVG with the same placeholder S, drawn by
  `rsvg-convert` at 320 pixels and shown at 160 in the note, so it is sharp
  on a high-density screen. The `seal` job installs `librsvg2-bin` for it;
  where the install or the drawing fails, the note keeps its counts table
  and the job log says why, as before. Release notes before 0.20.0 keep
  their images.
