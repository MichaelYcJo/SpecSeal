<!-- specs/1788844300-the-guards-cases-cannot-observe-what-they-guard -->

### Fixed

- **The pre-merge reminder's reader had two failure arms nothing watched, and
  either one would have stopped a session's Bash call.** `reader()` loads the
  shared reader by relative path and answers `None` where it cannot, so a copy
  of the plugin without `skills/` leaves the reminder printing rather than
  raising — that is the whole reason it returns `None` instead of raising. Two
  of its arms were pinned by cases and two were not: a `.py` reader that does
  not parse, and a `.py` reader that parses and imports something this
  interpreter does not have. Deleting either arm left the whole module green,
  so nothing would have noticed the arm going away. Both have a case now, and
  each was seen red on its own arm with the other left green (#209).
  The second of them was named by no ticket and no ledger row. It turned up
  because the arms were enumerated out of the function's own source instead of
  read off the page: the except tuple has three members where every prose
  reading of it had counted two, which makes four reachable arms rather than
  three. The evidence ledger's row said three, and now says four.
  A fifth arm, `spec.loader is None`, gets a sentence rather than a case. No
  file path constructs it — a directory, a `.txt`, an extensionless file and an
  empty string all make `spec_from_file_location` answer `None` outright, while
  a `.py`, a `.pyc`, a `.so`, a missing `.py` and even a directory *named*
  `x.py` all come back with a real loader. It is defence in depth, and saying so
  is the honest close.
- **The case guarding what a closing word can hide behind was a list of two
  literals, so a third hiding place would have arrived unguarded and silent.**
  The reminder decides a round record is closed by reading it the way the
  shared reader does, which blanks fenced blocks and HTML comment bodies — a
  closing word inside either is not a closing note. The case covering that was
  parametrized over two hand-written entries with a comment saying a third
  reader pass would want a third entry, and nothing made it want one: adding a
  third pass and running the module left everything green, while a closing word
  inside an inline code span silently began reading as hidden. The
  parametrization is now compared against the passes the reader actually
  composes, read out of its own source, so a pass added later fails that case
  instead of passing quietly (#210). The direction was never dangerous — a
  further pass only makes the reminder fire more often — but the silence was.
- **A work item with no round records at all could have started reading as one
  whose rows were never drained.** `is_closed` answers *closed* when there are
  no records, which is what keeps the reminder quiet for the state most work
  items are in, and no case called it that way: mutating that answer to
  *not closed* left every case green. It has a case now. The arm is unreachable
  from the hook itself, which asks only when records exist, but it is reachable
  in one line of code — and where an arm can be reached directly, a case is the
  honest close rather than a sentence.
