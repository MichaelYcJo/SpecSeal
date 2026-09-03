- **The release guard looked in one place for a file two work items kept in
  another (issue #96).** `fold_ledger.py` refuses a release while any work
  item still has an open row in `evidence-todo.md` — a fact a reviewer
  verified that never reached the ledger — and it finds those files with
  `seal/specs/*/evidence-todo.md`. Two work items kept theirs one directory
  deeper, under `rounds/`, so the guard was blind to two of five. Nothing
  was hidden: both carried a `drained` line. What was gone is the meaning of
  the guard's silence for those two, and the next open row written there
  would have passed a release without a word. The four misplaced files move
  to the level `docs/review-handoff-protocol.md` names, where every other
  work item already keeps them, and a test pins the layout rather than the
  glob — the glob is one line and the layout is written by hand once per
  work item, so the layout is the half that drifts. Found by asking what the
  guard's glob actually reaches, during another work item's review round.

  **And the rule is now said where a session meets it.** The reminder
  `hooks/review-history-guard.py` prints after a review is posted names the
  two todo files at the work item's own level, spelled from the same base as
  the round record beside them; `docs/review-chain-spec.md` and the
  `code-review` skill say the same, with the reason — `round-N` is the only
  member of the set that is plural, so it is the only one that gets a
  directory. The protocol already said where the files go, and the sentence
  a session actually reads at the moment it creates them did not.
