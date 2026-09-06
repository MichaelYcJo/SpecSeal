- **A fenced block in a reviewer's report must close, and its span must not
  cross a line `round_record.py new` reads the report by.** A fence that
  crosses one hid a whole section from every later reading, and each reading
  had its own wrong answer for the absence: the record got the empty template
  for `## Executed probes` and `## Deferred`, `nothing to drain` for a
  Deferred section the reviewer had in fact written, and exit 0 both times.
  Where the section was required the message blamed the reviewer for a
  section they had written — `the report has no ## Verdicts section`. The
  refusal now names the heading the fence swallowed and says what to do about
  it, so the writer is told what to fix rather than that something is wrong.
  **#169 called the late-closed fence *the one member of the class left
  open*, and it was not.** Decomposing on one boolean over one span — a fence
  has a closer or it has not, and where it has one the span either crosses a
  line the generator reads by or it does not — gives seven members, of which
  two silently lost a whole table rather than the one #169 named, and three
  more were caught only by the message that blames the reviewer. The issue's
  proposed fix, a membership test against a tuple of section constants inside
  `fenced_after`, reaches neither of the two: a fence that takes
  `## Executed probes` leaves the report with no probes section, so `build`
  never calls `fenced_after` at all and no guard living in that function
  could see the shape. **The guard therefore lives over the whole report and
  keys on the span rather than on the name**, and it derives the lines a
  fence may not cross from `REPORT_TABLES`' headings and `TERMINAL_LINES` —
  the module's own statement of what it reads, which nothing in the module
  read before this. A section added later is guarded, and gets a case, by
  being added there; no second list exists to go stale, which is what the
  membership test would have been by the next section. **What is refused is a
  report losing a section, never a fence mentioning one.** A reviewer of this
  generator pastes record-shaped blocks, headings and all, and a rule reading
  the mention would stop the tool on its own review rounds — so the guard
  asks whether the heading still stands outside the fence. A `#` at column 0
  is a Markdown heading and a Python comment both, and only the fence tells
  them apart, which is why nothing in the guard reads the `#` character.
  **That seven-member count is a count of one partition and not of the ways a
  report loses a section silently, and reading it as the second cost three
  more refusals.** The partition was taken against the headings and the
  terminal lines, in the one text the report-wide check reads, for the one
  input it reads. Applied to what it had not been: the generator reads the
  report a second time, verbatim, when it copies a fenced block — so an
  opener inside an HTML comment is invisible to the check and an opener to
  the copy, and the record went out with two sections unreadable at exit 0.
  It reads the table ROWS under a standing heading, not the heading alone —
  so a fence taking the rows left `## Deferred` in place and the record read
  `nothing to drain` beside a row the reviewer wrote. And it reads a second
  input, the round paragraph, which is spliced above every section a reader
  looks up and had never passed through the guard at all — an open fence
  there blanked the record from `## Verdicts` down, and the record was
  written before the failure. All three are refused now, each with a message
  naming what the fence took and what to do about it. The row rule keeps the
  same limit as the heading rule: a fence quoting rows beside a table that
  still stands is copied as it always was, which is what lets a reviewer of
  this generator paste record-shaped blocks into a report it will accept.
  **A fence is not the only hider, and that list of three was one short.**
  Every text reaches the generator through `readable`, which blanks in two
  passes and runs `strip_comments` first — so an HTML comment opened and
  never closed blanks every line below it exactly as an open fence does, one
  pass earlier, where no fence question can see it. The missing member was
  created by the fix for the round paragraph above: that guard asked the
  fence question of the comment-stripped text while the paragraph is spliced
  into the record verbatim, so an unterminated comment wrote the record and
  left four of its five sections unreadable to every downstream reader. Both
  the report and the round paragraph now ask both questions, the comment's
  first — an open comment blanks the closing fence of every block below it,
  so the other order names a fence that is closed in the text as written. On
  the report the same question replaces a message that sent the writer to add
  a `Needs a fix:` line they had in fact written. **What is left is one cell,
  named rather than assumed**: a comment that is balanced in the report and
  half in the record, because a copied row and a copied block are both slices
  of it. Refusing that takes a question about balance across a slice rather
  than about a hider that never closes, since a copied block may legitimately
  carry a whole comment — so it is recorded at the coordinate with what it
  costs, a straddle in a verdict row losing three whole sections. (#169)
