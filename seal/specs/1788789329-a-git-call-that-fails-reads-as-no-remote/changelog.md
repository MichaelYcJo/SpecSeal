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
  reporting it. The value compared is now the value printed. (#111)
