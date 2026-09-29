- **Every markdown reader the release and the checks ship shares one fence
  rule (issue #584).** CommonMark's: at most three spaces of indentation, a
  backtick opener whose info string holds no backtick, and a close only on a
  run of the same character at least as long with nothing after it.
  - The ledger fold copies a fenced `#` line as text, closing a fence by
    that rule rather than on any line starting with the opener's three
    characters, and a fenced `## X.Y.Z` heads nothing for `--check` or for a
    second fold.
  - A folded or gathered marker counts only on a live line, for the ledger
    fold, its `--check`, and `gather_changelog.py --check`: one quoted in a
    fenced example, a commented-out draft or a code span is not a fold or a
    gathered entry. The changelog check used to read a marker quoted anywhere,
    even inline in prose.
  - Because of that, `gather_changelog.py --version` and
    `fold_ledger.py --version` now refuse, with or without `--dry-run` and
    before writing anything, a fragment that opens a fenced block or an HTML
    comment and never closes it, naming the fragment. Written as it was, such
    a fragment hid every marker below it: the gather's `--check` then asked
    for a second gather that wrote the entry twice, and the fold's `--check`
    passed with a wrong count. Close the block in the fragment and run the
    step again.
  - `correction-check` skips a ledger row inside a fenced example that
    closes, as `evidence-check` does, and still watches a row under a fence
    that never closes.
  - `payload-meter --sections` no longer loses the headings after a prose
    line that opens with a four-backtick code span; in this repository that
    brings back three sections of `skills/evidence-check/SKILL.md`.
- **A copy of `correction_check.py` or `payload_meter.py` taken without
  `unverified_check.py` exits 2 with a sentence naming the missing file
  (issue #584).** `payload_meter.py` needs it only under `--sections`.
- **A survivor exemption quoted inside a fenced example or an HTML comment
  is no longer read as one (issue #658, the exemption half).**
  `survivor-check --exempt` takes no exemption from a fenced example or a
  commented-out row, and a fence or a comment that is never closed hides the
  rows below it, because an exemption excuses a survivor. A quote in
  `survivors.md` can therefore not hold a comment opener. No `survivors.md`
  in this repository reads differently.
