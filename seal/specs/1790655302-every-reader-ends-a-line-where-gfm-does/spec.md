# Feature Specification: every reader ends a line where GFM does

<!-- seal/specs/1790655302-every-reader-ends-a-line-where-gfm-does/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Milestone 49 (0.16.0), item G: the rest of #664. Work item C
(`1790635414`, PR #668) moved every hash-side and anchor-span split in
`evidence_check.py`, and `fold_check`'s line count, onto the line ends `ast`
and GFM use. It left the same class standing in readers that items B and D
were editing at the time, and in readers that go through the shared reader.
B, C and D have landed in `release/v0.16.0` at `2e392d46`, which is where this
branch was cut.

**The class.** A reader that splits markdown or record text with
`str.splitlines()` ends a line at U+2028, U+2029, NEL, form feed, VT and
`\x1c`–`\x1e` as well as at LF, CR and CRLF. GFM, `ast` and git end a line at
LF, CR and CRLF alone. So below one of those eight characters such a reader
reads lines no renderer shows: a table row cut in two, a heading or a marker
line that is not there, a line number one off the line `grep -n` and git
print, and, where the reader writes the text back, the character turned into
a real line break.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| #664's body and its two comments (the ticket) | The class and its first coordinates. The second comment lists the readers left after C, and routing names the seven this item inherits |
| `seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/phases/phase-5.md` §*What this phase found*, the table | C's enumeration of every `.splitlines(` in shipped code and each one's disposition. This frame re-enumerated from the tree (M3) and reaches the same members, plus the dispositions C left as "not named by #664" |
| `routing.md` §*Why this way* | The readers are fixed in this release rather than filed, at the owner's standing request. `hooks/config.py`, `hooks/routing.py`, `hooks/blocks.py` and `.github/scripts/rider_check.py` are work item F's (#667, PR #672) and stay untouched |
| `skills/settle/scripts/fold_check.py#gfm_lines`, its docstring | "the one reader every script shares is where a single copy belongs". This is the grounds for where the splitter lives (questions.md D1) |
| `skills/evidence-check/scripts/evidence_check.py`, the comment above `VENDORED_FENCE_RE` | `evidence-ci` puts the checker alone in a user repository's `tools/`, where the shared reader is not beside it. So the checker keeps its own copy of the splitter, held equal by a case, the arrangement its fence rule already has (questions.md D2) |
| `.github/scripts/claude_block.py`, its module docstring | "The region is cut the way `install.sh`'s `awk` cuts it". `awk` ends a record at LF alone, so this reader's rule is LF, not GFM (questions.md D6) |
| `skills/agent-contract/SKILL.md` §12, §14, §15 | The class is enumerated, not the coordinate. A line number a refusal prints changes below one of the eight characters, so it is pinned. Every new case is seen red at `2e392d46` |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | Red test, failure direction, prompt budget and platform honesty, for every gate this item touches (§*Failure direction and prompt budget* below) |
| `CLAUDE.md` §*The goal a design is chosen against* | Nothing in this item asks a person anything. The prompt budget is zero |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* and §*commit early* | New ledger rows go to `seal/ledger/1790655302-every-reader-ends-a-line-where-gfm-does.md`. A shared-file row an edit drifts is re-read and re-stamped where it stands. A row whose anchor this item removes (`fold_check.py#gfm_lines`) is removed there, and its claim rewritten in the fragment |
| `skills/implement/SKILL.md` §6, "The records themselves stay" | C's `rounds/round-1.md` already holds a line break where its report held U+2028 (M2). It is a closed record and is not rewritten |
| `CLAUDE.md` §*Repo rule — no real identifiers in examples or fixtures* | Fixtures use neutral paths. Each of the eight characters is built from its code point, never typed (C's phase 5 records why) |

## What was measured before the frame, and by whom

Taken in this framer at `f104b6d2`. No check of the repository's ran. The
scans below are read-only and wrote nothing.

| # | Fact | Label |
|---|---|---|
| M1 | Of 788 tracked text files, exactly one holds any of the eight characters: `seal/specs/1790635414-follow-up-names-are-checked-and-a-re-read-is-dated/rounds/round-1-report.md`, two U+2028, both inside fenced blocks (its lines 260 and 450 by LF). No tracked file holds a CR | executed (a Python scan over `git ls-files`) |
| M2 | That work item's `rounds/round-1.md` holds a real LF at the two places its report held U+2028 (its lines 209–210 and 252–253). This is the report-copy defect #664 names, standing in the tree | executed (`grep -n`) |
| M3 | Every `.splitlines(` in shipped code (`git grep` over `*.py`, `tests/` excluded), with its enclosing unit by `ast`. The table in §*The class, enumerated* is that list | executed |
| M4 | `readable`'s callers: `chain_check.py` (13 sites), `round_record.py`, `survivor_check.py#read_exemptions`, `hooks/review-history-guard.py#is_closed`, and `unverified_check.py`'s own `check_text`. None of them except `round_record.py` pairs `readable(text)`'s indices with a second split of the same text | read (`git grep`, each site opened) |
| M5 | `round_record.py#swallowed` zips `strip_comments(report.splitlines())` with `readable(report)` under `strict=True`. Moving `readable` alone makes that zip raise on a report holding one of the eight characters | read |
| M6 | `tests/test_chain_hooks.py#reader_blanking_passes` derives `readable`'s passes from the calls it makes BY NAME to module-level functions. A `gfm_lines(text)` call inside `readable` would count as a new pass and redden it | read |
| M7 | Work item F's branch (`origin/fix/658-667-…`, merge base `66b34a4e`) edits, beside its four files, `unverified_check.py` (the `fence_opener` docstring), `evidence_check.py` (one comment line above `VENDORED_FENCE_RE`), `broad_gate.py` and `seal.py`. F's merge base is before C, and F's `rider_check.py#region_lines` still slices `text.splitlines()` where C moved it to `checker.gfm_lines(text)` | read (`git diff`, `git show`) |
| M8 | `gather_changelog.py#insert` finds an existing section's index with `changelog_text.count("\n", …)` and indexes `changelog_text.splitlines()` with it. The two disagree below one of the eight characters | read |

## Scope

**In.** Every reader of markdown or record text in shipped code that splits
with `str.splitlines()`, outside F's files, moves to the line ends its
grammar uses. For every reader but two, that grammar is GFM. `claude_block.py`
matches `awk` and the transcript tails match JSON Lines, so both split at
LF alone.

1. **One splitter, in the shared reader.**
   `skills/verify/scripts/unverified_check.py` gains `GFM_LINE_RE` and
   `gfm_lines(text, keepends=False)`, the rule `evidence_check.py#gfm_lines`
   holds today. `readable` and `folded_items` read it.
2. **The readers coupled to it move in the same commit.** No two readers of
   one text may disagree about where its lines are.
   - `round_record.py`'s report copy and every `raw` / `readable` pair:
     `#open_hider`, `#hiders_close`, `#swallowed`, `#inherited_rows`,
     `#reach_forward`, `#reach_back`, `#build`, `#fix_table`, `#close`,
     `#seal`.
   - `fold_check.py#numbered_statements`, `#markers` and `#marker_digest`
     count what `folded_items` reads.
   - `fold_check.py#gfm_lines`, the copy, is retired. `#ceiling_problems`
     asks the reader's.
3. **The changelog readers and their partner.**
   - `gather_changelog.py`: `#live_markers`, `#leaves_open`,
     `#section_lines`, `#insert` and `#main`.
   - `survivor_check.py#gathered_fragments` reads the same markers, and its
     docstring says the two split alike on purpose.
   - `survivor_check.py#segments` (its line numbers must agree with
     `#python_prose` and `#released_lines`, which number at LF) and
     `#removed_ledger_rows` (both ends of the range).
4. **The independent markdown readers.**
   - `correction_check.py#rows`
   - `chain_check.py#frame_mark` (the foot of `spec.md`) and `#frame` (the
     `Approved` line of `plan.md`)
   - `payload_meter.py#heading_starts`
   - `issue_claims_check.py#segments`
   - `round_record.py#measure` and `#call_sites`, which split `git diff` and
     `git grep -n` output whose lines are file content, numbered by git at LF
   - `claude_block.py#read_lines`, at LF alone and keeping ends, the way
     `install.sh`'s `awk` cuts the block
5. **The transcript tails.** `hooks/worktree-guard.py#last_user_snippet` and
   `#last_active_event_epoch` split a JSON Lines tail at LF. JSON permits a
   raw U+2028 inside a string, so `splitlines` breaks one record into two
   halves that each fail to parse. Every other transcript reader in the tree
   (`worktree_consent.py`, `payload_meter.py#_rows`, `session_cost.py`)
   iterates the file, which splits at LF, so these two are the only ones
   out of line.
6. **The class is held closed by a case.** One case lists every
   `.splitlines(` call in shipped code by enclosing unit, each one marked
   out of the class with its reason. A new call fails the case until someone
   classifies it. The same case keeps every copy of the splitter equal:
   the reader's, the checker's, and `arm_check.py#_lines` with ends kept.
7. **The docstrings that describe a split** in the moved units say what is
   true after the move. That covers `gfm_lines`' two docstrings,
   `live_lines`' *What this may not touch*, `gather_changelog.py#live_markers`
   and `fold_check.py`'s retired paragraph.

**Out, and why.**

| Left | Why | What happens instead |
|---|---|---|
| `hooks/config.py#unfenced`, `#config_rows`, `#refusal`; `hooks/routing.py#table_rows`; `.github/scripts/rider_check.py` (`Rider.__init__`, `#riders_in`, `#write_block`); `hooks/blocks.py` | F's files (#667). F's design keeps each reader's lines on `splitlines` and has the walk read GFM lines, mapping each reader line to the GFM line it starts in (`hooks/blocks.py#walk_text` on F's branch) | Nothing here. The class case exempts these files by path and names F as the reason |
| `.github/scripts/rider_check.py#inferred_anchor` | F's file. It compares `splitlines` numbering against `checker.py_spans`, which is `ast`'s, so two form-feed lines above a rider pick the next function. Only `--migrate` calls it | Once F lands, `inferred_anchor` slices `checker.gfm_lines(text)`, the list `region_lines` slices since C. It is recorded in `overview.md` §*Not done*, and the milestone 49 orchestrator answers it |
| `skills/verify/scripts/broad_gate.py#fenced_row_at`, `#fence_left_open`; `skills/implement/scripts/seal.py#with_row`, `#write_row` | Their line indices are `hooks/config.py`'s walk indices, and F's PR rewrites all four functions against its own reader | F's answer stands for them |
| `fold_ledger.py#live_markers`, `#leaves_open`, `#demote`, `#insert`; `settle.py#coordinates`; `unverified_check.py#todo_open_rows`; `survivor_check.py#released_lines`, `#python_prose` | Not in the class. They split on `"\n"` text read through `open()`'s or `subprocess`'s newline translation, which already ends a line where GFM does. `fold_ledger` rewrites byte for byte and relies on the `split("\n")` / `"\n".join` round trip, which `gfm_lines` would break by dropping the trailing empty element | Left as they are, named in the class case |
| git and subprocess output whose lines are paths, refs, subjects or a tool's messages. Sites: `close_issues_on_release.py#arrived`, `release_completeness_check.py#subjects_since`, `commit-review-gate.py#collect`, `version-check.py#latest`, `root-migrate.py#dirty`, `worktree-guard.py#proc_cwd`, `#lease_owner_alive`, `#sessions_in_tree` and `#tracked_changes`, `chain_check.py#added_on_branch` and `#restored_from`, `round_record.py#head_moved`, `#worktrees_of`, `#touched` and `#tracked_at`, `seal.py#porcelain`, `#other_worktrees` and `#gitlinks_under_root`, `settle.py#released`, `session_cost.py#open_log`, `unverified_check.py#overviews_at` and `#tree_at`, `broad_gate.py#first_lines`, `#suite_counts` and `#gate` | Not a document's lines | Named in the class case |
| YAML: `broad_gate.py#job_steps`, `deferral_check.py#read_events` and `#runners_in`, `payload_meter.py#frontmatter` | Not markdown or a record. They read a workflow file or a front-matter block for event and key names, and no record reader reads that output | Named in the class case |
| `ledger-migrate.py#attempted`, `root-migrate.py#attempted`; `dispatch.py#first_line`; `run_tests.py#venv_version`; `__doc__.splitlines()[0]` in `issue_claims_check.py#main` and `rider_check.py#main`; `seal_stamp.py`'s module constant | A marker file of root paths this plugin writes, an exception message, `pyvenv.cfg`, docstrings and a constant | Named in the class case |
| C's `rounds/round-1.md`, holding LF where its report held U+2028 (M2) | A closed record asserts a past state and is kept (`skills/implement/SKILL.md` §6). The LF sits inside a quoted test in a fenced block, so no reader reads a row from it | Left. The case for scenario S1 is this instance, rebuilt in a fixture |
| `live_lines` and `readable` taking TEXT instead of lines, so no caller splits at all | It changes the signature eight callers use, and the `fold_ledger` and `settle` callers split on `"\n"` for the byte-for-byte reason above | `plan.md` §*Alternatives considered*, row E |

## The class, enumerated

This is every `.splitlines(` call in shipped code at `f104b6d2` (M3), by
enclosing unit. Docstring and comment mentions are not listed.

| Reader | Text it splits | Disposition | Phase |
|---|---|---|---|
| `skills/verify/scripts/unverified_check.py#readable` | every record, overview, report and survivors file the gates read | moved, GFM | 1 |
| `unverified_check.py#folded_items` | `docs/*.md`, for fold markers | moved, GFM | 1 |
| `skills/code-review/scripts/round_record.py#open_hider`, `#hiders_close`, `#swallowed`, `#inherited_rows`, `#reach_forward`, `#reach_back`, `#build`, `#fix_table`, `#close`, `#seal` | a report or a record, the `raw` half of a pair with `readable`, and the text written back | moved, GFM, with `readable` | 1 |
| `skills/settle/scripts/fold_check.py#numbered_statements`, `#markers`, `#marker_digest` | `docs/*.md`, counting what `folded_items` reads | moved, GFM, with `folded_items` | 1 |
| `.github/scripts/gather_changelog.py#live_markers`, `#leaves_open`, `#section_lines`, `#insert`, `#main` | `CHANGELOG.md` and a fragment, read and written back | moved, GFM | 2 |
| `skills/code-review/scripts/survivor_check.py#gathered_fragments` | `CHANGELOG.md` at a revision, the same markers `live_markers` reads | moved, GFM, with `gather_changelog` | 2 |
| `survivor_check.py#segments`, `#removed_ledger_rows` | a document's sentences with their line numbers; a ledger at each end of a range | moved, GFM | 2 |
| `skills/evidence-check/scripts/correction_check.py#rows` | a ledger file at each side of a merge | moved, GFM | 3 |
| `skills/code-review/scripts/chain_check.py#frame_mark`, `#frame` | `spec.md`'s last line, `plan.md`'s `Approved` line | moved, GFM | 3 |
| `skills/verify/scripts/payload_meter.py#heading_starts` | a skill's or agent's markdown, split into sections by offset | moved, GFM, ends kept | 3 |
| `.github/scripts/issue_claims_check.py#segments` | an issue's or pull request's body, cut by offset | moved, GFM, ends kept | 3 |
| `round_record.py#measure`, `#call_sites` | `git diff` and `git grep -n` lines, each carrying a line of file content | moved, GFM | 3 |
| `.github/scripts/claude_block.py#read_lines` | `CLAUDE.md` and the template, compared with `awk`'s cut | moved, LF alone, ends kept | 3 |
| `hooks/worktree-guard.py#last_user_snippet`, `#last_active_event_epoch` | a JSON Lines transcript tail | moved, LF alone | 4 |
| `hooks/config.py` (3), `hooks/routing.py#table_rows`, `.github/scripts/rider_check.py` (5), `broad_gate.py#fenced_row_at` and `#fence_left_open`, `seal.py#with_row` and `#write_row` | F's files, or indices into F's walk | out, F (#667) | — |
| The git, subprocess, YAML and constant sites in §*Scope* **Out** | not a document's lines | out, named in the case | 5 |

## User scenarios & acceptance *(mandatory)*

Every case below is seen red at `2e392d46` on its real assertion before it is
committed (§15), and the handover says how. "One of the eight" means each
character, built from its code point, unless the row names one.

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | A report's quoted character survives into its record | Given a round report whose fenced block holds `alpha` U+2028 `beta` on one line, when `round_record.py new` writes the record, then the record holds that line with the U+2028 in it, not a line break (M2's instance) | case, red at base |
| S2 | A fix row with a line separator in a cell is one row | Given a fix table whose `Commit or grounds` cell holds a U+2028, when `close` reads it, then the row is read with its three cells and applied | case, red at base |
| S3 | A marker GFM does not see as its own line excuses nothing | Given `docs/x.md` holding `prose` U+2028 `<!-- specs/<id> -->` on one line, when `folded_items` reads it, then `<id>` is not folded, so a removal of that directory is still counted as a removal | case, red at base |
| S4 | The ceiling and the fold agree about a marker | Given S3's document, then `fold_check.py#markers` and `#marker_digest` count no marker there, the same as `folded_items`, and `#ceiling_problems` counts its lines with the reader's `gfm_lines` | case |
| S5 | Gathering into an existing section below a separator lands there and keeps the character | Given `CHANGELOG.md` with a U+2028 in an older entry above the version's existing section, when `gather_changelog.py --version` runs, then the new entries sit at the end of that section and the U+2028 is still in the older entry | case, red at base |
| S6 | The gatherer and the sweep read one marker alike | Given a marker after a U+2028 on its line, then `gather_changelog.py#live_markers` and `survivor_check.py#gathered_fragments` both leave the fragment ungathered | case, red at base on the sweep side |
| S7 | A sentence's line number is the file's | Given a document with a form feed mid-line above a sentence, when `survivor_check.py#segments` reports it, then the number is the sentence's line by LF, the number `grep -n` prints | case, red at base |
| S8 | A ledger row holding a separator is one row at both ends | Given a ledger row with a U+2028 in its notes at `a` and `b`, when `#removed_ledger_rows` compares them, then the row is found standing | case, red at base |
| S9 | A correction after a separator is counted | Given a row whose `Corrected <date>` note sits after a U+2028, and a merge that drops the note, when `correction_check.py` reads both sides, then it names the dropped correction | case, red at base |
| S10 | The framer's mark is the last line a renderer shows | Given `spec.md` whose last line is `prose` U+2028 followed by a well-formed mark, when `chain_check.py#frame_mark` reads it, then there is no mark, because that line does not begin with one | case, red at base |
| S11 | The approval line is a line of its own | Given `plan.md` holding `prose` U+2028 `Approved 2026-01-01 by x, when smith was spawned.` on one line, when `#frame` reads it, then no approval is found | case, red at base |
| S12 | A heading after a separator is not a section | Given a skill file with a `#` after a U+2028 mid-line, when `payload_meter.py#heading_starts` splits it, then no section starts there and every offset still sums to the file's length | case, red at base |
| S13 | An issue body is cut where GitHub renders a block | Given a body with a block-start line shape after a U+2028 mid-line, when `issue_claims_check.py#segments` cuts it, then no cut is made there | case, red at base |
| S14 | A unit added below a form feed is measured | Given a non-Python file whose added line is a form feed and then `def name` on one line, when `round_record.py#measure` reads the diff, then `name` is in the added units. The same holds for `#call_sites` on a `git grep -n` line holding a U+2028 before the call | case, red at base |
| S15 | The CLAUDE.md block is cut the way `awk` cuts it | Given a template line holding a U+2028 mid-line, when `claude_block.py --write` then `--check` run, then the line is written with its U+2028 and `--check` agrees with `install.sh`'s cut | case; if the base cannot be made red, the phase says the move is for agreement with `awk` only (questions.md Q3) |
| S16 | A transcript record holding a raw separator is read | Given a JSON Lines tail whose last user record carries a raw U+2028 inside a string, when `worktree-guard.py#last_user_snippet` reads it, then the snippet is that record's, not an earlier one's. `#last_active_event_epoch` is read the same way | case, red at base |
| S17 | One splitter, and its copies agree | Over LF, CR, CRLF, each of the eight, no trailing newline and the empty string, `unverified_check.gfm_lines`, `evidence_check.gfm_lines` and `arm_check._lines` (as `gfm_lines(…, keepends=True)`) return the same lines | case (replaces `tests/test_a_document_has_room_for_the_next_fold.py`'s copy check) |
| S18 | The splitter is not a blanking pass | `tests/test_chain_hooks.py#reader_blanking_passes` still derives `readable`'s passes, does not count `gfm_lines`, and still goes red when a pass is added | case, and a mutant adding a pass seen red |
| S19 | The class stays closed | Every `.splitlines(` call in shipped code outside F's files is either absent or listed in the class case with its reason. A new call in an unlisted unit fails the case | case, red with a planted call |
| S20 | Nothing moves on this tree | Each moved reader's output over this tree is byte-identical at `2e392d46` and after its phase, apart from what M1's report changes inside its fences | executed per phase |

## Data & interfaces

- `unverified_check.py` gains `GFM_LINE_RE` and `gfm_lines(text,
  keepends=False)`, the same signature and result as
  `evidence_check.py#gfm_lines`. No existing function changes its signature.
- `fold_check.py#gfm_lines` is removed. `#ceiling_problems` asks the
  reader's, so `fold_check.py` loads the reader on every run that reads a
  document, where it loaded it before only for a document listed over the
  ceiling. A copy taken alone was already refused with exit 2 by `load`.
- No output format changes. What a person sees change is a line number in a
  refusal or annotation, and only below one of the eight characters. Such a
  number now matches `grep -n` and git.

## Failure direction and prompt budget

| Gate | Before, below one of the eight | After | Direction |
|---|---|---|---|
| `unverified-check --baseline` via `folded_items` | a marker GFM never shows excuses a directory's removal | it excuses nothing | blocks more |
| `survivor-check` via `gathered_fragments` | a marker GFM never shows excuses a fragment from the sweep | it excuses nothing | blocks more |
| `survivor-check --exempt` via `readable` (`#read_exemptions`) | a row split in two can lose its exemption | the row is read whole | allows the row it was meant to |
| `correction-check` via `#rows` | a correction after the character is invisible, so dropping it is silent | it is read | blocks more |
| `round-record` | a record rewrite turns the character into a line break, and a row cut in two is refused or misread | the character is kept, and the row is read whole | fewer false refusals, no silent rewrite |
| `chain-check` via `#frame_mark`, `#frame` | a mark or an approval no renderer shows as its own line counts | it does not count | blocks more |
| `fold-check` | a marker GFM never shows is counted into the frozen count and digest | not counted, so a consumer's listed entry may need its digest updated, which the refusal prints | blocks once, loudly |

The prompt budget is zero. No change here puts a question in front of a
person.

**Platform.** The eight characters and the regex are the same on every
platform. Text read through `open()` or `subprocess` in text mode arrives
with CR already translated, and that is also true on Windows. `read_blobs`
reads bytes and keeps a lone CR, which `gfm_lines` ends a line at, as
`splitlines` did. Only macOS runs this item's cases. Linux is CI's, and
nobody runs Windows here.

## Open questions → questions.md

No row needs a person. Three rows are for a measurement or the work, and the
judgments the tree answered are listed at the head of that file.

Framed 2026-09-29 by framer, before the build.
