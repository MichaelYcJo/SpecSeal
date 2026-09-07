- **A git call that failed used to read as a repository with no remote, and
  in `seal import` that switched off the refusal keeping another project's
  records out (issue #111).** `git()` in `skills/implement/scripts/seal.py`
  answered `""` for every failure — an `OSError`, a timeout, a non-zero exit —
  and four of its five call sites read that `""` as a fact about the
  repository. The sharpest of them decided whether the zip in hand came from
  somewhere else: an empty answer short-circuited the whole condition, so a
  git that timed out merged another project's records with no word about it.
  Nothing is destroyed — `seal import` never overwrites — but two projects'
  work items land in one root keyed by work-item id, with nothing afterwards
  to tell them apart, which is the outcome the refusal exists to prevent.

  **The unanswerable question now refuses**, which is the direction
  `gitlinks_under_root`, `porcelain` and `indexed` in the same file already
  take. The message carries git's own words, because *run it again* and *this
  machine will never answer* are the two things a person does next and only
  git's text tells them apart.

  **The escape is `--allow-unreadable-remote`, a flag of its own.** Typing
  `--allow-other-repo` is saying *I have read both URLs and they are one
  repository under two spellings*; someone whose git could not answer has read
  neither and is saying something else. Routing both past one flag would merge
  the two facts again at the only place a user acts on the distinction.

  **The manifest leaves out what git could not read**, rather than freezing
  `""` into the zip for the receiving machine to read as a fact. `remote` now
  has three states — a URL, `""` for a repository with no `origin`, and absent
  for a question that went unanswered — and a zip recording no remote refuses
  on arrival for the same reason. `head` loses its empty state entirely: `git
  rev-parse HEAD` prints a SHA whenever it succeeds, so present means a SHA
  was read. The format number does not move, because no field was renamed or
  repurposed and format 1's only reader of the two already went through
  `manifest.get`.

  **`git_asked` is one helper where there were three.** `porcelain`, `tracked`
  and `gitlinks_under_root` had each grown the same *(value, why)* shape for
  themselves; it is promoted so a caller needing the distinction does not
  write a fourth. `git()` is that helper with the distinction thrown away,
  which is the right reading for a caller with nothing to do with `why` — and
  after this change it has exactly one call site left, `other_worktrees`,
  where a failure means an advisory note does not print. Its docstring now
  says that silence is by design.

  Its `answered` parameter exists for one measured fact: `git config --get`
  exits 1 when the key is not set, so for that command alone a non-zero code
  is an answer. Measured 2026-09-07 — an unset `remote.origin.url` gives
  `(1, '', '')` and a `.git/config` git cannot parse gives `(128, '', 'fatal:
  bad config line 9 …')`. `--default ""` would have removed the special case
  and wants git 2.18, which nothing else here needs, so an old git would have
  started refusing a path that works today.

  **The ticket said four call sites were left; there were five.** It did not
  count the second `git()` inside the refusal message, which asked git again
  for the URL it had just read and printed whatever that call answered — so a
  failure between the two put a blank where the message promises this clone's
  URL. That is this ticket's own failure appearing inside the message
  reporting it. The value compared is now the value printed.

  **The receiving guard reads the manifest's `remote` for its TYPE, not its
  presence.** Review round 1 measured `null`, `42`, `[]`, `{}` and `true` all
  importing at exit 0 with both guards silent — and `null` is what any JSON
  writer produces from the `None` this change introduced, so the very state
  the export uses to say *I could not look* arrived at the guard as a key that
  was present.

  **The refusal names the machine that can fix it.** One closing line used to
  cover two failures with two different next steps. When this clone's git went
  silent, running the import again may succeed; when the ZIP is the silent
  side, the bytes say the same thing on every run there is and the export has
  to happen again on the other machine — so telling that person to re-run sent
  them into a loop that cannot end. When both sides are silent the zip
  decides, because no re-run here clears it whatever this clone's git answers
  next.

  **The export says which field it had to leave out.** It used to write a zip
  that would be refused on arrival and print nothing about it, which left the
  diagnosis on the importing machine while the one that could clear the
  failure — by running the export again — was told it had succeeded. Only the
  `remote` line carries the note about the other machine's flag, because only
  a missing `remote` is refused there. (#111)

- **Two checks of this repository's own round records stopped crashing on the
  files the review chain writes beside a record.** Both asked git for
  `seal/specs/*/rounds/round-*.md`, and git's pathspec has no way to say *and
  then a number*, so the glob also picked up `round-N-report.md`,
  `round-N-asked.md` and `round-N-fixes.md`. Ordering the result asked for a
  round number those files do not have, and two of them in one work item ended
  the check with a `TypeError` instead of a verdict — so a run that committed
  a reviewer's report beside its record turned two checks off and reported it
  as a crash. `chain_check.py` itself already drops those files on the same
  test; the two readers that did not now do. (#111)
