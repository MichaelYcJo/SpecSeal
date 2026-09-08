<!-- specs/1788844300-the-guards-cases-cannot-observe-what-they-guard -->

### Fixed

- **An ordinary `gh` command piped into `jq` could have stopped a session's
  Bash call.** The same reminder decides which parts of a command line are `gh`
  commands by splitting on `|` and reading each piece with `shlex`. A pipe
  inside a quoted string — `gh pr view 123 --json comments | jq '.comments[] |
  .body'`, which is the reminder's own example — leaves a piece whose quoting
  is unbalanced, and `shlex` raises on it. One arm absorbs that, and no case
  watched it: deleting the arm left this module and every other module that
  touches the hook green, while the hook itself began exiting 1 with
  `ValueError: No closing quotation` on that command — out of a `PostToolUse`
  hook and into the session's Bash call, which is the one thing this hook is
  written never to do. It has a case now. The arm was found by applying the
  same enumeration to the two functions of the file the first pass had not
  walked, which is what a review round is for.
- **So could a command as ordinary as one ending in a newline.** The same
  splitter breaks on `\n` as well as on `|`, so any multi-line Bash command
  leaves a trailing piece with no tokens in it at all. Two index guards keep
  the reminder from reading a first word off such a piece, and no case watched
  either: deleting one left the module green while the hook exited 1 with
  `IndexError: list index out of range` on `gh pr view 1 --json comments` with
  a trailing newline and on `echo hi;`. `FOO=bar` gets there by the other
  route — it is one token, which the environment-assignment prefix arm
  consumes, so the index runs off the end just the same. All of it is covered
  now, together with the quoting arm above, by **one parametrized case rather
  than four** — they share a single input class, a piece the reminder cannot
  reduce to a first word — and the case closed a fourth decision as a
  by-product. What is still unwatched in that function misfiles a reminder
  rather than stopping anything, and went to a ticket, because writing a case
  for each closes today's list and not the class (#209, #210).
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
  What that comparison can see is passes the reader calls **by name**. A pass
  written instead as a regular-expression substitution on the text — the shape
  a text-level blanker is naturally written in, and the shape the ticket itself
  used as its example — is invisible to it, and left the comparison agreeing
  while the reminder's answer flipped. That shape is now refused outright with
  a message saying what to do about it, rather than passing unnoticed.
  The case also goes red when a reader pass is RENAMED, and its message used to
  offer only the repair for a pass that was added — adding a key, which for a
  rename leaves an extra key and the case still red. It now names both causes
  and the repair each one takes.
- **A work item with no round records at all could have started reading as one
  whose rows were never drained.** `is_closed` answers *closed* when there are
  no records, which is what keeps the reminder quiet for the state most work
  items are in, and no case called it that way: mutating that answer to
  *not closed* left every case green. It has a case now. The arm is unreachable
  from the hook itself, which asks only when records exist, but it is reachable
  in one line of code — and where an arm can be reached directly, a case is the
  honest close rather than a sentence.
