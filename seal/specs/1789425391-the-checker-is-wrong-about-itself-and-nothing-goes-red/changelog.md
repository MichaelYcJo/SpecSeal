- **A verdict row the record itself calls `open` is no longer written with
  `Pass` ticked over it (issue #395).** The rule that decides whether a row owes
  an answer read the `#` cell and not the `Verdict` cell beside it, so a row
  carrying 🟢, ❓, ⬜ or no marker at all came through `round-record new` at exit
  0, silently, while its own table said the finding was open. Six shapes did
  this and three of them carried no severity marker, so the residual the
  documents described did not cover them even as prose.

  **What is matched is the one word `open`**, ended by a space, a comma or
  nothing — so `open — deferred` and `open, comment only` are reached and
  `opened in round 2` is not. It is not a test of the closing vocabulary: a
  confirmation row reads `verified`, which is in no vocabulary, and refusing
  everything outside the closed words would refuse every confirmation. Of the 25
  no-digit cells the rule admits in this repository's committed records, not one
  reads `open`, so no existing record changes.

  **Slipping through now takes two mistakes in two different cells** — a wrong
  severity marker AND a verdict worded as something other than `open`.

- **A verdict row too short to have a `Verdict` cell is refused by name instead
  of crashing (#395).** A digit in the `#` cell keyed the row, and four readers
  downstream index the verdict column by position — so a short row reached them
  as a traceback at exit 1. Both `round-record new` and `round-record close`
  now refuse it at exit 2, quoting the row. A four-cell row that merely lacks
  its `Grounds` is still admitted and written at the width the reviewer left,
  rather than padded with a column nobody wrote.

- **`round-record seal` no longer writes a cell its own check then refuses
  (#335).** On the **last** round record, `Fixes checked by` may only read `no
  fixes to check`. A `round-N` there names a later round, and the last record
  has none — the value passed the old shape test, the `Broad gate` cell was
  written, and the chain check the same command runs one step later refused the
  very row. The refusal now comes first, with nothing written, and it says which
  value the last record may hold and why each of the other two is refused.

  What a user with a run in that state meets is a refusal at exit 2 where they
  previously met a written cell and a failing check a step later. That is
  strictly the better message and it is a behaviour change: the way out is to
  spawn the verifying round first, and its record is the one the cell belongs
  on.

- **A depth-2 refusal names the finding whose fix actually added the unit
  (#333).** The walk compared the file, so a fix range answering two findings in
  one file attributed every unit added there to whichever row it reached first —
  and the message then sent the reader to a row that had not added the unit, and
  named the wrong enclosing unit with it. It now resolves the adding commit from
  the fix table's own rows.

  Where a single commit answers two findings nothing can resolve it, and there
  the refusal still fires: it says the attribution is file-level and names every
  candidate finding rather than asserting one.

- **Two round records committed together no longer state the same findings as
  open and as fixed (#342).** `round-record new` writes round N's `## Inherited
  coordinates` from round N-1's verdict cells, which read `open` at that moment
  because a record is committed before the fixes it commissions. Nothing carried
  the words forward when those fixes landed. `round-record close` now brings
  every row it inherited to the word the verdict cell carries, and prints how
  many it filled. It refuses rather than guesses where the later record is
  unreadable, and says nothing at all where the later round does not exist yet.

- **The suite now fails when the checks over this repository's own round records
  stop checking anything (#142).** Three readers said they read what git carries
  and called `git ls-files`, which reads the index — so a record staged and not
  committed was listed and then silently skipped, and the case reported nothing
  about it. All three read HEAD now. And nothing tested the tests: emptying the
  failure collection left every case green, so each walk has a control that runs
  the same loop over a record known to be refused.

- **The gate and the generator are bound at the word they share (#334).**
  `broad-gate --record` tells a refusal before the write apart from a check that
  failed after it by reading the word `sealed` in the generator's own output,
  and the case for the second reading drove a stand-in whose text the case wrote
  itself — so changing the real message left 130 cases green. A case now drives
  the real pair in both endings.
