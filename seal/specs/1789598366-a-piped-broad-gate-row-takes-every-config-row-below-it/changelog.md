<!-- seal/specs/1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A `Broad gate` row holding a pipe took every config row below it, and
  nothing said so** (#415). `seal/config.md` is markdown, but the one reader
  of its table matched a cell as *anything but a pipe*, so a row written
  `| Broad gate | bin/test -q | tee out.txt |` stopped being a row — and the
  reader's rule is that a line which is not a row ends the table. Every row
  under it fell back to its default with no message anywhere.

  - **A cell now carries markdown's own escape.** `\|` reaches the value as
    one literal pipe, reduced in the reader before any shell sees it, so
    `/bin/sh` and `cmd.exe` are both handed a plain `|`. Exactly those two
    characters are touched and no other backslash is: a row holding
    `C:\Users\x\Python\python.exe -m pytest` reads back with its separators
    intact, which a general unescape would have turned into a path to nothing.
    A bare pipe is still where a cell ends, because making it part of the
    value needs a greedy last cell — and a greedy last cell reads the rows of
    a three-column table written under this one as rows of this one.

    One spelling changed meaning, and it is the only one. A backslash written
    immediately against a cell-ending pipe is now that escape, so a row
    ending `C:\Users\x\tools\|` stopped being a row: the pipe it needed to
    close the cell is the one the backslash escaped. Writing a space before
    the closing pipe reads back exactly as it did before. No file in this
    repository is affected — every `| Item | Value |` table in the tree reads
    the same rows before and after.

  - **`seal mode` was writing a second `Mode` row into a person's file.** The
    reader and the writer read one table, so when the reader stopped above a
    person's `Mode` row the writer stopped there too and inserted its own —
    leaving the file two rows deep, which the writer's own comment says no
    command brings back into agreement. Measured, and now pinned.

  - **A line that will not parse is quoted back instead of being reported
    absent.** `broad-gate` used to say *has no `Broad gate` row* about a row
    sitting in front of the reader — a true sentence about the wrong cause.
    It now shows the line as written, names `\|` as the way to write the pipe,
    and says every row below it is lost too. A row that genuinely is not there
    gets the absent-row refusal exactly as before. `hooks/mode-gate.py` gains
    nothing and says nothing new: it is a `PreToolUse` hook, and a wrong
    refusal there stops a session with nobody able to get past it.

  - **The fourth copy of the table reader is closed.**
    `tests/test_the_pull_request_language_is_the_repositorys.py` had its own
    reimplementation of the loop, which agreed with the real one until this
    branch moved one of them. It calls the one reader now, asserted by where
    the code was compiled rather than by an import.

  What this does not repair is written beside it: a pipe written WITHOUT the
  escape still is not a row, and what changes for that person is the message
  rather than the outcome. A `Mode` row hidden below an unparseable line is
  still invisible to the mode gate, which still simply asks the question
  again. And the cost falls on the rows below a line that does not parse only
  when a row above it already parsed — the stop rule needs a row before it
  can stop.
