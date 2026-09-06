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
  line the generator reads by or it does not — gives seven members, two of
  which silently lost a whole table rather than one, and three more of which
  were caught only by the message that blames the reviewer. The issue's
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
  (#169)
