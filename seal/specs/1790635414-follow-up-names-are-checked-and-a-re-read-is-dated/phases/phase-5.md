# 1790635414-follow-up-names-are-checked-and-a-re-read-is-dated — phase 5

<!-- seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/phases/phase-5.md -->

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 3dd2cbfd |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 5, #664, added at the owner's request, with the
issue's comment correcting its body: a markdown anchor is not shifted, and a
character at a line end or on a blank line moves no hash. Every hash-side
and anchor-span split in `evidence_check.py` moves to the line ends `ast` and
GFM use, through `gfm_lines`, whose docstring A's run left with two false
sentences. Then enumerate the class outside the checker and record what each
reader does: `correction_check.py#rows`, `round_record.py`'s report copy,
`survivor_check`, `fold_check`, `hooks/config.py`, `gather_changelog`. The
spawn narrowed the moves: B (#584) is rewriting fence and comment readers and
D (#28) `hooks/dispatch.py` and `hooks/cmdline.py`, so only readers in files
neither touches move here, and the rest are named for a follow-up once B
squashes. Verified by the form-feed case seen red at `56e53c90`, the tree
check moving no row's hash, one mutant per changed call site, and the
checker's and each moved reader's modules.

## What this phase found

- **Eleven call sites in the checker, all moved.** `resolve_unit`,
  `minor_region`, `recorded_here`, `file_units`, `content_matches`,
  `check_text` (twice), `migrate` (the cited file and the stamped one) and
  `reverify` (the heal and the re-stamp). No `str.splitlines` call is left in
  the file.
- **The class inside the checker is wider than #664 says, and the comment's
  correction is true of numbering only.** A markdown anchor is numbered and
  sliced on one list of lines, so it is not shifted; but a line-end
  character before `## ` made a heading GFM never sees, which ended the
  section there, and one before column-0 text ended a generic unit's block.
  Both let an edit pass; both cases are red at `56e53c90` on the real
  assertion (exit 0 where `DRIFTED` was owed), beside #664's `.py` case.
- **The first red run of the markdown case proved nothing.** Its fixture
  wrote into a `docs/` the `repo` fixture does not create, so it failed at
  both commits with `FileNotFoundError`. Caught on the green side, where it
  still failed; the helper now makes the parent, and the case was re-run
  red at the base for the right reason.
- **Four cases pin a partial move, not the old defect.** The rename heal in
  Python and a generic file, and `--migrate` with and without its stamp,
  pass at `56e53c90`, which was wrong consistently on one list of lines.
  They exist so that one call site moved back is caught, and the mutant run
  shows each one doing that.
- **One mutant per call site, eleven, every one red.** A scratch probe put
  each site back on `str.splitlines`, one at a time, in a copy of `HEAD`
  extracted with `git archive`, and ran the #664 cases against it through
  the same probe plugin: `resolve_unit` 4 red, `minor_region` 1,
  `recorded_here` 1, `file_units` 1, `content_matches` 2, the unsure hash 1,
  `check_text`'s hash 8, `migrate`'s lines 2, its stamped lines 1, the heal
  2, `reverify`'s hash 6. The copy was restored and compared afterwards.
- **The switch moved no row's hash in this tree** (executed): no tracked file
  holds any of the eight characters, and the ledger arm's full output is
  byte-identical under the base checker and this one over the same tree.
  The sixteen rows that drifted were this phase's edits to the units they
  cite, and were re-read and re-stamped with `--checked` in the phase's
  ledger commit, with the seven more rows phase 4 had already dated.
- **`gfm_lines`' docstring now says what is true after the move**: which
  anchors went wrong and how, what the switch moves (a region holding such a
  character mid-line, and a `.py` unit below one), what it does not (a
  character at a line end or on a blank line, which `normalise` drops), and
  that nothing here moved. The two sentences A's round 3 found false are
  gone with the paragraph they stood in.
- **#664's tooling observation, seen once in this run.** An `Edit` whose new
  text carried a `２` escape wrote the fullwidth character itself, and
  the linter refused the file. The cases build every such character from its
  code point for that reason.

**The class outside the checker, enumerated by `git grep` for
`.splitlines(` over every shipped `.py`**, sorted by what each call reads
and who may move it now:

| Reader | What it splits | Disposition |
|---|---|---|
| `skills/settle/scripts/fold_check.py#ceiling_problems` | a `docs/*.md` document, to count its lines | **moved** here, to a copy of the rule held equal to the checker's by a case; the eight characters no longer put a document at the ceiling over it |
| `skills/settle/scripts/fold_check.py#markers`, `#marker_digest`, `#numbered_statements` | a document, for fold markers and statement boundaries | **left, coupled**: they count what the fold itself reads, and the fold reads through the shared reader, which splits with `splitlines`. Moved alone they would disagree with the fold about a marker |
| `skills/code-review/scripts/round_record.py` — the report copy in `build`, and every `raw, lines = text.splitlines(), reader.readable(text)` pair (`open_hider`, `hiders_close`, `swallowed`, `inherited_rows`, `reach_forward`, `reach_back`, `fix_table`, `close`, `seal`) | a round report or record | **left, coupled**: `raw` is zipped index by index with `reader.readable(text)`, which is `unverified_check.py`'s and splits with `splitlines`; moving `raw` alone misaligns the pair on exactly the input #664 is about. They move with `readable` |
| `skills/verify/scripts/unverified_check.py` — `readable`, the `live_lines` callers, `folded_items` | every record and ledger the shared reader serves | **B's file**. This is where one splitter for every script belongs, and where the two coupled rows above are unblocked |
| `skills/evidence-check/scripts/correction_check.py#rows` | a ledger file at each side of a merge | **B's file** |
| `.github/scripts/gather_changelog.py` (6 calls) | changelog fragments and `CHANGELOG.md` | **B's file** |
| `skills/code-review/scripts/survivor_check.py` (5 calls) | records and ledger rows before and after a range | **B's file** |
| `hooks/config.py` (3 calls) | `seal/config.md` | **B's file** |
| `.github/scripts/rider_check.py#region_lines` | a rider's file, sliced at the lines `checker.resolve_unit` returned | **coupled to the checker, and missed by this phase**: `resolve_unit` numbers on `gfm_lines` since this phase, and the slice stayed on `splitlines`, so a region below a mid-line U+2028 was one line early and an edit to its last line passed. Round 1 of this work item found it (🟡 4); its fix pass moved the one line, the file being B's otherwise. *Row added 2026-09-29 by that fix pass (⬜ 6)* |
| `rider_check.py` (its other calls), `broad_gate.py`, `payload_meter.py`, `seal.py`, `hooks/routing.py` | riders, reports, records, `routing.md` | **B's files** (`hooks/routing.py` and `seal.py` D's too); not named by #664 |
| `hooks/ledger-migrate.py`, `hooks/root-migrate.py` | ledger and root files at session start | **D's files**; not named by #664 |
| `.github/scripts/claude_block.py`, `skills/code-review/scripts/chain_check.py#frame_mark` and `#frame`, `skills/verify/scripts/deferral_check.py#read_events`, `.github/scripts/issue_claims_check.py#segments`, `hooks/worktree-guard.py#last_user_snippet`, `round_record.py#measure`'s diff lines | `CLAUDE.md` against `install.sh`'s `awk` cut (which ends lines at LF alone), `spec.md` and `plan.md`, an events log, an issue's text, a transcript's JSON lines (JSON permits a raw U+2028 inside a string, so a split breaks a record's parse), and the changed lines of a fix range | **not moved, not named by #664**: members by the same cause, each owed its own red case, and one splitter in the shared reader is the move that serves them all |
| git and subprocess output — `close_issues_on_release`, `release_completeness_check`, `commit-review-gate`, `version-check`, `worktree-guard`'s status and listing reads, `chain_check`'s listings, `settle.py`, `session_cost`, `round_record`'s path and log listings — plus two constants and `run_tests#venv_version` | lines git or a tool prints, a docstring, `pyvenv.cfg` | **out of the class**: paths, subjects and config keys, not a document's lines |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `str.splitlines` on the hash side of `evidence_check.py`, eleven calls | `gfm_lines`, at every one |
| `gfm_lines`' paragraph calling the hash side a known defect, with #664's two false sentences in it | the rewritten docstring, which says what the switch moved and what it did not |
| `str.splitlines` in `fold_check.py#ceiling_problems`' count | `fold_check.py#gfm_lines` |
