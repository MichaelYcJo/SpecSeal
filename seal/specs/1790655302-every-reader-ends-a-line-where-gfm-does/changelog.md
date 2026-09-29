### Changed

- **Two gates excuse less, and one may refuse once at this upgrade** (#664).
  Where a document holds a U+2028, U+2029, NEL, form feed, VT or `\x1c`–`\x1e`
  in the middle of a line, a fold marker or a gathered-changelog marker
  standing after it is no longer read as a line of its own, because no
  renderer shows it as one.
  - `unverified-check --baseline` no longer counts such a marker in `docs/`
    as a fold, so a work item directory it used to excuse is reported as
    removed.
  - `survivor-check` no longer counts such a marker in `CHANGELOG.md` as a
    gathered fragment, so the fragment is back in the sweep.
  - `fold-check` no longer counts such a marker in a document listed under
    `Over the ceiling`. The frozen count or digest can then disagree once,
    and the refusal prints the digest to write into `seal/config.md`.
- **Line numbers in refusals and annotations below one of those characters
  now match `grep -n`, git and GitHub** (#664). This covers `round-record`,
  `unverified-check`, `survivor-check`, `fold-check`'s shape check and
  `gather_changelog.py`'s section check. Above the first such character, and
  in a document holding none, every number is the same as before.

### Fixed

- **Every reader of markdown or record text ends a line where GFM does**
  (#664). The eight characters above used to end a line for these readers
  and for no renderer. Each reader now reads `unverified_check.py#gfm_lines`,
  one splitter, and two readers of one text split it alike.
  - `round-record new` copies a character a report quotes into the record as
    it stood, where it used to write a line break in its place. `close` reads
    a fix row holding one as one row rather than cutting its grounds.
  - `gather_changelog.py --version` appends into an existing section below
    such a character, where it used to put the new entries above the
    section's heading, and writes the character back rather than a line
    break.
  - `correction-check` names a dropped `Corrected` or `Re-read` note that
    stood after such a character in a ledger row. It used to belong to no
    row, so the loss was silent.
  - `chain-check` does not read a framer's mark or a plan's approval that
    stands after such a character on a line of prose.
  - `payload-meter --sections` and the pull-request issue-claims check start
    no section or segment after one mid-line. `round-record close` measures a
    unit added below a form feed in a non-Python file and finds a call after
    a U+2028.
- **`claude_block.py --write` copies a template line holding such a
  character whole** (#664). It used to cut the line and give each piece a
  line end, so the repository's copy of the block gained a line break that
  `install.sh`'s copy does not have. The script now ends a line at LF alone,
  as `install.sh`'s `awk` does.
- **The rider check reads no rider whose marker line follows one of the
  eight characters mid-line** (#664). Such a rider was read and never cut
  from the region its stamp hashes, so its own stamp was hashed and
  `--reverify` could not make it read ok. A rider on a line of its own is
  read as before. `rider_check.py` now loads `hooks/blocks.py` for a
  Python file that carries a marker, as it already did for markdown.
  `--migrate` infers a rider's anchor on the line numbers `ast` gives, so a
  form feed inside a string above the rider no longer points it at the
  wrong unit.
- **The worktree guard reads a transcript record that carries a raw U+2028
  inside a string** (#664). The record used to split into two halves that
  each failed to parse, so the blocking prompt named an earlier message of
  the conversation it protects.
