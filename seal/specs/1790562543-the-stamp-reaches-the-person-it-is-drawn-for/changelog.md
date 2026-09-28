- **The sealer's stamp is drawn where the person sees it, once, after the
  orchestrator's text (issue #400).** A sealer's stdout is a pipe, and the
  stamp drawn there reached the person folded behind `ctrl+o`; the 0.15.6
  stopgap of re-printing the sealer's log drew it twice, colourless and cut.
  `broad-gate` now draws only on a terminal. On a pipe, a recorded green run
  writes the panel's rows to a values file under
  `<git-common-dir>/specseal-stamp/<session>/`, keyed by
  `CLAUDE_CODE_SESSION_ID`, and prints one line beginning `SEALED` that names
  the tree, the base commit and the file. A new `Stop` hook,
  `hooks/sealer-stamp.py` in a new `stop` group, draws each undrawn file of
  its own session once, as a JSON `systemMessage` whose first line names what
  was sealed, and draws nothing at a subagent's end. Every line that names a
  values file names `seal-stamp --from <path>` too, quoted for the shell,
  because the hook draws nothing and says nothing where it cannot: a `python3` under 3.12, a
  session outside the sealed clone, or a plugin older than the hook. A run
  with no session says so; a values file that cannot be written leaves the
  run sealed and says nothing will be drawn. The hook builds each stamp
  whole before it claims the file, so a malformed values file is left
  pending and takes no other file's drawing with it.
- **No stamp is drawn without a written cell (issue #400).** A green run
  without `--record`, on a terminal or off one, prints the `SEALED` line
  saying nothing was recorded, and draws and writes nothing. A red run, a
  refused record and a chain check failing after the write leave no values
  file.
- **`seal-stamp --from <file>` draws a sealed run's values file once (issue
  #400).** It claims the file by renaming it to `.drawn.json` before
  printing, so a second run refuses with one sentence and exit 2, and a file
  that is not a run's values is refused before it is claimed. Both
  `seal-stamp` and `broad-gate` now default to scale 0.90, the owner's choice
  over six rendered scales, with 0.75 recorded beside the constant as the
  candidate passed over.
- **The orchestrator never draws a stamp, and the sealer draws none either
  (issue #400).** `skills/code-review/orchestration.md` says the stamp is
  drawn at the end of the orchestrator's turn, so its result text comes
  first and it neither runs `seal-stamp` nor relays the sealer's log;
  `agents/sealer.md` says the gate draws nothing in a sealer. The **Form**
  bullet of `skills/verify/SKILL.md` and a new section of
  `docs/the-broad-gate.md` say where the stamp is drawn, and that what a
  person's screen shows is checked by nothing.
