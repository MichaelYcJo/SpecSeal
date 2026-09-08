- **A fix repaired the coordinate a finding named and the same claim stayed
  standing somewhere else, seven times, and now a check looks.**
  `survivor-check --range <a>..<b>` takes the range a fix pass wrote and
  reports every place in the tree that still carries wording the range
  removed, naming the path, the standing text and the corrected sentence it
  matched. It runs at the fix pass, in the smith's verify step, and on every
  pull request. `agent-contract` §12 has said *do not fix the coordinate*
  since 0.7.0 and reaches every agent at startup; #229 measured the same class
  in another repository, over a documentation work item whose findings per
  round ran 13 → 8 → 5 → 6 and never converged, with 3 of its 4 rounds
  repeating an earlier finding in a different file. So this release ships the
  check rather than an eighth sentence. (#180)

  **It was built against two events in this repository's history and is seen
  failing on both.** One commit reworded a sentence in `agents/warden.md` and
  left its pin behind in a test module that then sat red through two review
  rounds and two broad gates, because no reviewer may run the broad gate
  (#269). Another corrected a docstring and left the identical claim in two
  ledger rows, one of them the shared file a reader meets first (#267). A
  literal grep finds neither: the first is one sentence split across two
  adjacent string literals, so no line holds it, and the second is a
  paraphrase whose longest identical run is three words.

  What a survivor scores is **the number of independent phrases it shares that
  occur nowhere else**, so the threshold means the same thing in a twenty-file
  repository and a thousand-file one, and it is calibrated over 77 real
  ranges rather than chosen. Two kinds of carrier are excluded with a written
  reason instead of a list: a work item's round records, which quote a
  finding's wording by design, and struck-through text, which is this
  repository's own mark for a claim it no longer makes.

  **A survivor a person judges legitimate is answered, not switched off.** A
  row in `seal/specs/<work-item-id>/survivors.md` names the path, a quoted
  substring of the standing text and the grounds; the quote is the anchor, so
  the exemption stops holding the moment that text changes, and an excused
  survivor is still printed with its grounds. There is no value meaning
  *check nothing*.
