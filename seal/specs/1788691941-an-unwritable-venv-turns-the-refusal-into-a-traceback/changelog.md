- **A virtualenv the operator has made read-only ended `bin/test` in a
  traceback printed underneath a refusal it had already given.** The ignore
  that keeps `.venv` out of `git status` is written from a `finally` in
  `ensure`, which is what makes it an exit-level guarantee rather than a list
  of remembered paths — and it is also what puts the write on the two exits
  whose entire product is a sentence. `write_text` was unguarded, so on a
  `.venv` this process cannot write to, the floor refusal reached stderr and a
  `PermissionError` followed it. The write is guarded now and says what it
  could not do: it names the ignore, the reason, and that the virtualenv stays
  visible to `git status` until the reader removes that directory or makes it
  writable. The refusals above it keep their wording and their exit codes, and
  the runner does not try to win the argument — a read-only `.venv` is the
  operator's. **The class is closed by construction rather than by a list**:
  `hide_from_git` holds the only write this module makes to the working tree
  itself, and everything else that lands there is a builder subprocess's,
  whose failure is already a return code the caller reads. The module
  docstring says so, and says the guard belongs to the module rather than to
  the function, because the class is one write only for as long as nobody adds
  a second. **A `chmod 555` fixture is not a guarantee, and asserting only *no
  traceback* would have hidden that**: root bypasses the permission bits and
  Windows ignores every bit but read-only, so on two of the three platforms CI
  runs the write succeeds and a case asserting absence would pass for the
  wrong reason. One case builds the real fixture and is skipped where `chmod`
  does not stop a write, with the reason written into the skip so it travels
  into pytest's own report; a second makes the write itself refuse, so the
  wording is pinned everywhere. Neither can pass on a write that succeeded.
  (#177)

- **A ledger row whose guarantee a change makes conditional gains the
  condition; it is not removed.** Two rows were in that position and both are
  repaired in place, because a row is removed when a change takes away the
  code it cites and this one took nothing away. The virtualenv row's claim —
  invisible to git on every exit of `ensure` — was never about the write
  landing, and on the one path where it does not land the row had been false
  before this change as well, in the worse way: the write raised through the
  `finally` and replaced the refusal with a traceback. So what was wrong was
  an unstated precondition rather than the mechanism, and the mechanism is
  exactly what the guard was written to keep. The new claims went into the
  work item's own fragment, which is where the fragment rule puts them.

- **A case that reads three named constants catches a rename and cannot see a
  fourth constant added beside them.** `docs/review-chain-spec.md` names the
  five values that can stand in the reach half of a `Contract changes` entry,
  and the case holding the document to them read `PYTEST`, `PYTEST_ONLY` and
  `NO_SITE` out of `round_record.py` by name. That is three ways of catching
  an edit to a value that exists and no way at all of catching one being
  added — the drift the paragraph exists against, where the document goes
  stale and the suite stays green. The set is now **derived** from
  `call_sites`' own `return` statements, so a value the function gains has to
  reach the document before the suite is green again. Measured rather than
  argued: with a sixth value added to the function, the derived case exits 1
  naming it and the named case passes. **Both are kept**, because neither
  covers the other — a constant renamed with its value untouched is still the
  same word in the document, so only the named form fails on that edit. What
  the derivation does not reach is recorded beside it rather than closed: a
  value another function hands back, one formatted at run time, and the two
  the section names as categories rather than as words, which are the
  reviewed repository's own names and have no finite set to derive — and that
  limit is executed rather than only stated, by two fixtures that are its two
  sides. **The derivation reads the generator's text as an argument, and that
  is what makes it testable at all**: today's `call_sites` names a constant in
  every return and writes no literal into one, so against the real module the
  arm that reads a literal is unreachable and a mutation deleting it survives
  — which is what the mutation loop found, in the very case written to close a
  list that would go stale. Six mutations over the derivation, one at a time,
  each now killed by a named case. (#177)
