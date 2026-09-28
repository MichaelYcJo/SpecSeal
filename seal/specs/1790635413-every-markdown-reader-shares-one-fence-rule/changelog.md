- **A row inside an HTML comment in `seal/config.md` is no longer read
  (issue #584).** The config reader had no comment state, so a `Broad gate`
  row somebody commented out above the live one was the only row the gate
  got, and a whole old table parked inside a comment was read as the table.
  Every reader and the `seal mode` writer now skip a line that begins inside
  a comment that closes; a comment that never closes hides nothing, so no
  file that reads today stops reading. **This can change what a repository
  declares**: a `Broad gate` or `Mode` row that stands only inside a closed
  comment stops being read, and `broad-gate` then refuses naming the row as
  *written inside an HTML comment*, or the mode question comes back once.
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
  - The rider check no longer reads a rider quoted inside a fenced example
    in a markdown file, which it reported as BROKEN at exit 2.
  - `correction-check` skips a ledger row inside a fenced example that
    closes, as `evidence-check` does, and still watches a row under a fence
    that never closes.
  - `payload-meter --sections` no longer loses the headings after a prose
    line that opens with a four-backtick code span; in this repository that
    brings back three sections of `skills/evidence-check/SKILL.md`.
- **A copy of `correction_check.py` or `payload_meter.py` taken without
  `unverified_check.py` exits 2 with a sentence naming the missing file
  (issue #584).** `payload_meter.py` needs it only under `--sections`.
