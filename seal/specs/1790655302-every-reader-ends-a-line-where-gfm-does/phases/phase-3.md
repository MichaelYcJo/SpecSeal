# 1790655302-every-reader-ends-a-line-where-gfm-does — phase 3

<!-- seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | c7042fa4 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 3: the independent readers.
`correction_check.py#rows`; `chain_check.py#frame_mark` and `#frame`;
`payload_meter.py#heading_starts` with ends kept;
`issue_claims_check.py#segments` with ends kept, loading the reader the way
`gather_changelog.py#load_reader` does; `round_record.py#measure` and
`#call_sites`; and `claude_block.py#read_lines`, which moves to LF alone with
ends kept, `awk`'s cut (questions.md D6). Answer questions.md Q3. Verified
by S9–S15 red at base, each reader's module, and S20 for `correction-check`,
`chain-check`, `payload_meter` and `claude_block.py --check`.

## What this phase found

- **Q3 is answered red.** At `2e392d46`, `claude_block.py --write` wrote a
  template line holding `alpha` U+2028 `beta` into the target as two lines.
  The move is a defect fix with a pinned case, not agreement with `awk`
  alone.
- **`read_lines` has an arm no existing case read.** A last line with no
  line end is kept by the new split's second arm. Dropping that arm stayed
  green across `tests/test_the_claude_md_block_has_one_source.py` and the
  new case, because every fixture ended in LF. S15's target now ends with
  no line end, and the dropped arm is red.
- **`frame_mark` needed the reader passed in.** It took only the text. Its
  one caller, `frame`, already had the reader, so the signature became
  `frame_mark(reader, text)`. S10 at base therefore stops on the old
  signature. The base answer was read off the base function directly: it
  returned `('2026-01-01', 'framer')` for the mark after a U+2028.
- **S11 is tested through `frame` with `read_record` replaced.** The
  approval line is read inside `frame` from git at HEAD, so the case hands
  it the two files through `read_record` and a stand-in for the routing
  module's two constants, rather than building a repository.
- **`issue_claims_check.py` now loads the shared reader at import**, by
  path, the way `gather_changelog.py` does. It is a CI script of this
  repository, so a reader that moves stops it with a traceback at the pull
  request, which is the loud direction.
- **S20.** `correction-check` and `chain-check` printed the same bytes
  before and after. `claude_block.py --check` printed the same line.
  `payload_meter.py --sections` printed the same 293 lines at `2e392d46`
  (run from the base archive) and here.
- **Ledger.** 7 rows drifted and each claim held. G7–G10 are this phase's
  rows.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
