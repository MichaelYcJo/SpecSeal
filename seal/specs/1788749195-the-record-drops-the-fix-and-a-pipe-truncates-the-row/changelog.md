- **The round record now carries the reviewer's paste-ready fix, and a `|`
  inside a cell no longer truncates the row (#187, #189).** The review skill
  requires a paste-ready fix for every 🔴 and every 🟡 and spends four
  paragraphs on what makes one paste-ready, and `round_record.py new` copied
  the report's four tables and dropped everything else — so not one of those
  blocks reached the file the fix pass is told to open instead of the report.
  Measured: a 162-line report carried three executed snippets, its record came
  out at 80 lines with none of them, and the fix pass rebuilt all three from a
  description and got its first reproduction wrong. The same loss then
  recurred five times on the next branch, whose orchestrator worked around it
  by posting each report as a pull-request comment — durable, and not a file
  any clone contains. **The record gains `## Paste-ready fixes`**, extracted
  by the mechanism the probes table has used since #161: every fenced block
  under the heading, copied whole, and nothing else of the section, so no
  prose nobody parses enters a file the pull-request check reads. A report
  that carries no fence under the heading is still a record — the section
  reads `no paste-ready fix in the report`, which says what was observed
  rather than that none was needed, and beside an open row in the verdict
  table that sentence is the gap written down. A verifying round that opens
  nothing writes no fix, which is why refusing there would stop an unattended
  run over a report that is correct.

  **And a `|` the reviewer wrote inside a cell reaches the record as text.**
  It used to make the row carry more cells than the header declares; every
  renderer drops the surplus, so the text from that character on was invisible
  in the rendered record while surviving in the raw file, and the checker read
  the shifted index. The two compounded: with the fenced blocks going nowhere,
  a table cell was the only durable home for a fix, and a fix is where a pipe
  comes from. Rows are now re-serialised with their pipes escaped rather than
  copied verbatim — in every table the record copies and in the fix table the
  implementer hands over. **A `|` inside a backtick code span is read as
  text**, which is the reviewer's own markup saying so, and that reading is
  taken only when it lands on exactly the header's width; otherwise the plain
  reading is capped at that width and a bare pipe past the last column stays
  in the last cell. A `|` inside an HTML comment is never a break in any
  reading — the row's width is counted on the comment-stripped report and the
  copy is rebuilt from the raw one, and where those two texts disagreed about
  a character the record lost a column at exactly header width, with the
  location standing in the verdict cell the checker reads. The obvious
  repair — fold the surplus into the last column, since the last column is
  the free-text one — was ruled out by measurement over this repository's own
  committed records: of 4128 body rows, eight are over-wide, all eight have
  their pipe inside a code span, one has it in a probes command where folding
  would move half the command into `Result`, and one has it in the Finding
  column where folding shifts that same verdict cell. Nothing here asks a
  person anything. **One report shape that produced a record before is now
  refused**: a fence opener hidden inside an HTML comment under the new
  heading, which would otherwise write a record carrying an open fence and
  blank every section below it.

  **The reviewer is told where the fix goes**, which is the half that keeps
  the section from arriving empty every round: the agent's report contract
  shows the heading beside the three table headings and no longer says the
  generator reads nothing else of the report, and the findings format says the
  fenced block is the only place a fix survives the session — a Grounds cell
  is one line, and this is what used to truncate it.

  **The pre-merge reminder no longer reads a narrated word as a closing
  note.** It stayed quiet once some round record said the rows were drained,
  and it decided that by matching `closed` against the record's raw text.
  Putting the reviewer's code into every record made that reachable
  everywhere, and this repository's own fixes carry the word. The record is
  now read through the same reader every other check uses, so a closing word
  counts only where a reader would read it — **not inside a fenced block and
  not inside an HTML comment.** The second half is the one that was already
  costing something: over this repository's 127 committed round records the
  repair changes the verdict on three, all three because their only closing
  word stands inside an HTML comment the round wrote to narrate itself — two
  of them in the record's header comment, the third in a note beside the field
  table saying the loop is *not closed by one more small fix* — and all three
  still have unresolved rows the reminder should have
  been naming. (#187, #189)
