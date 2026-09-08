- **A pull request body naming two issues claims one, and nothing said so
  (issue #167).** PR #162's body wrote a closing keyword followed by two
  numbers in one sentence. At the 0.8.0 release the first was closed and the
  second stayed open, and somebody closed it by hand afterwards.

  Nothing malfunctioned. A closing keyword claims the one number that follows
  it — GitHub reads it that way, and `close_issues_on_release.py` says so in a
  comment two lines above its own regex. The answer was written down in the
  one file whose author needs it least at the moment the prose is written: the
  session writing a pull request body is not reading the release closer.

  **So the repair is a check that reports, not a wider regex.** Widening
  `CLOSING` would make this repository close issues GitHub does not, and the
  two would then disagree about what a body means — worse than the loss it
  repairs.

  `.github/scripts/issue_claims_check.py` runs first in the `hygiene`
  workflow, on every pull request. It prints every issue number the body
  claims, every one it merely mentions, and a warning for any sentence that
  claims one number and names another beside it. **It never fails a pull
  request**: a check that goes red on prose stops a release for a false
  positive, and one measured occurrence does not buy that. Its only non-zero
  exit is a step handed no body at all, which is a misconfigured workflow
  rather than a body.

  **What a sentence is, since the whole check turns on it.** A segment ends at
  `.!?;` before whitespace, at a blank line, or at the start of a new markdown
  block — and **not** at a single newline, because every body here is
  hard-wrapped and the defect arrives split across two lines. Fenced blocks
  and code spans are blanked character for character, so a body quoting the
  failing shape as an example reports nothing, and the warning can still quote
  the sentence as the author wrote it. `e.g.` ends a segment too, which can
  only split two numbers apart: the check under-reports rather than inventing
  a warning.

  `docs/issues-and-milestones.md` gains the rule in prose, beside the section
  that already says a missing `Closes #N` costs an issue that stays open
  forever.
