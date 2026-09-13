- **The round-record generator can now be typed as `round-record`, and every
  shipped document that names it says where it is (issue #318).** Four agent
  segments concluded `skills/code-review/scripts/round_record.py` does not
  ship and hand-wrote the record it writes; two of those hand-written records
  had a field wrong in a way only the next round's reader caught. The script's
  own `--help` has printed `usage: round-record` since it shipped, and no file
  answered to that name.

  **The two halves of the defect needed two different repairs, and the ticket
  proposed them as alternatives.** Two of the thirty-six mentions show a
  command for somebody to type, and a `bin/` wrapper pair fixes those. The
  other thirty-four describe what the generator does — *`round_record.py new`
  writes `round-N.md`* — and a reader who meets one goes looking for a
  filename rather than typing anything. Three of the four segments in the
  incident were `warden`, whose definition never tells it to run the script
  at all, so the wrapper alone would not have reached them.

  **The ticket's own enumeration was short by six documents.** It named three;
  `round_record.py` appears in nine, and the file the four segments actually
  hand-wrote from — `templates/sdd-round.md`, seven mentions — was not among
  the three. Each of the nine now carries one reachable form, the command or
  the script's repo-relative path.

- **A shipped document that names a script it gives no way to reach now fails
  the suite.** The check enumerates `skills/*/scripts/*.py` and every `.md`
  under `agents/`, `skills/` and `templates/` rather than naming this one
  script, so the tenth document and the thirteenth script are caught the way
  `bin/` itself was not. It blocks more than it did: a document naming a
  script with no locator is now red, and the repair is one sentence written by
  the person already editing that document. The failure names the document and
  both accepted forms.

  **A script may also keep no wrapper, and then it says why.** `chain_check.py`
  is named in four shipped documents and invoked in none of them, and all
  three places that do invoke it carry its full path — so it keeps no command
  and is classified with that reason instead. The classification is not a note:
  the check asserts the property it rests on, so the moment a document shows
  `chain_check.py` being invoked, the classification goes red rather than
  standing as a sentence that has quietly stopped being true.
