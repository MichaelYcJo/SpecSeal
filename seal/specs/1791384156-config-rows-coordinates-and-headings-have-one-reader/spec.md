# Feature Specification: config rows, the ledger coordinate and a markdown heading each have one reader (#867)

<!-- seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended* | a doubled row or an unreadable file is answered by a refusal in a command and by silence in a hook, never by a question |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | every phase that changes what a gate answers states its direction, its prompt budget (zero throughout), a test seen red, and the platform the unreadable-file fixtures hold on |
| `docs/the-evidence-ledger.md` §*A row is a content anchor, and it names no commit* | the coordinate is `path#major@hash`, the major level a unit or a heading path; this is the format whose one grammar is `evidence_check.py#ANCHOR_RE` |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment* | the released rows the heading fix moves are re-read as `Re-read ·` rows and re-pointed as `Corrected ·` rows in this work item's fragment, never edited in place |
| `docs/the-pact.md` §*A `Pact notify` value outside the vocabulary, or a row written twice, has no value at all* | the precedent for the duplicate answer: a row written twice is refused, and its first row is not the answer |
| `docs/the-broad-gate.md` §*A fenced example in a config file is not a config row* | every walk of the `\| Item \| Value \|` table shares one fence rule; the reader and the writer must agree about which line is the row |
| `docs/one-root-by-lifetime.md` §*A cell may carry an escaped pipe, and one line that will not parse is named rather than treated as the end of the table* | the reader and the writer share the constant that describes a row, because their disagreement is what writes a duplicate row into a person's file |
| `templates/config.md` §*The ledger freeze* | the shape a refusal of a config row already takes — both commands exit 2 naming the row, nothing is written |
| #834 `spec.md` §*What the table found besides*, and `inventory/4-ledger-settle-seal.md` §*Observations* (branch `chore/834-every-reader-and-record-is-inventoried`) | the counts this frame rests on: two answers to a duplicate row, four to an unreadable file, five coordinate grammars, four heading rules |

## Scope

**In — three of the issue's six formats, each read by one reader with one
answer to a duplicate and one to an unreadable file.**

1. **`seal/config.md` rows.** `hooks/config.py` is the reader. A row written
   twice has no value and is refused with a sentence naming the item and the
   count. A file that is absent declares nothing; a file that is there and
   cannot be read is refused with a sentence naming the path. Every caller
   reads through the reader and acts on a refusal by its own kind: a hook
   that may not stop (`hooks/mode-gate.py`, `hooks/evidence-advisor.py`)
   reads it as nothing declared and says nothing; a command a person runs
   (`evidence-check`, `correction-check`, `fold-check`, `broad-gate`,
   `seal mode`, `pact-check`) prints it and exits 2 with nothing judged. The
   vendored checker carries a twin of the reader, held equal by a case. The
   same duplicate rule reaches `hooks/routing.py#parse`: a label written
   twice has no value, so a strict label doubled is not a declaration and the
   gate asks, and an optional one doubled is unanswered.
2. **The ledger coordinate.** `evidence_check.py#ANCHOR_RE` is the one
   grammar. `correction_check.py` and `settle.py` reach it by loading the
   checker, as they already load `unverified_check.py` and `hooks/config.py`;
   `.github/scripts/rider_check.py` builds its stamp from the checker's
   locator and hash pieces. Three regexes leave the tree.
3. **A markdown heading.** CommonMark 4.2's ATX heading — at most three
   spaces, one to six `#`, then a space, a tab or the end of the line — read
   on the lines a renderer shows. `skills/verify/scripts/unverified_check.py#heading_level`
   is the one spelling; the checker, the fold check, the chain check, the
   survivor sweep, the payload meter and the unverified-record check read it
   there, and the checker's vendored copy carries a twin held equal. The
   checker computes a `.md` region over its own quoted-line rule, so a `## B`
   inside a closed fence opens no section. `tests/commonmark_oracle.py` holds
   the rule to markdown-it.

**Out, with the ground for each.**

- **The four markdown-table grammars in `hooks/` and the chain check**
  (`hooks/routing.py#table_rows`, `hooks/config.py#indexed_config_rows`,
  `hooks/config.py#gfm_table`, `skills/code-review/scripts/chain_check.py#table_rows`).
  Each reads a different file with a different failure direction — the gate
  asks, the hook stays silent, the checker refuses — and the one family with
  issues since 0.18.0 (pact markdown: #759, #794, #830, #831, #844; four
  reopenings) is `gfm_table`'s callers and the signer compatibility reader,
  which converged for the `Pact` row (#793) and is open at #844 in a test's
  own paragraph rule, not in a table reader. Moving `config_rows` onto
  `gfm_table` would refuse a config whose header has a non-blank line above
  it (`tests/test_one_table_walker_reads_what_gfm_renders.py::test_a_line_directly_above_the_header_is_refused`),
  which turns a `Broad gate` row into no row and stops the sealer: an
  outage-class change that needs its own migration and prompt-budget
  argument. **Filed** — `plan.md` §*Operational impact* carries the issue
  text. `chain_check.py#table_rows` is #866's seam.
- **Whether a line is live** (`evidence_check.py#quoted_lines`,
  `unverified_check.py#live_lines`, `evidence_check.py#claim_lines`,
  `settle.py#anchored_rows`, `unverified_check.py#readable`,
  `hooks/config.py#hidden_lines`, `rider_check.py#quoted_lines`): seven
  rules with four failure directions, each argued in its docstring for its
  reader's consequence. Measured over the released ledgers (2026-10-07,
  probe, read-only): `quoted_lines` and `live_lines` skip the same rows on
  every file (none), and `readable` blanks 46 rows across eight release
  files that the checker reads on purpose (#444: a commented-out row is a
  claim somebody parked). No issue since 0.18.0 is in this family. **Filed**
  — `plan.md` §*Operational impact* carries the issue text.
- **The fold's own `## X.Y.Z` section line** (`settle.py#coordinates` at
  `startswith("## ")`, `.github/scripts/fold_ledger.py`,
  `.github/scripts/gather_changelog.py`): these read the line their own
  writer writes, `fold_ledger.py#section` and the changelog gatherer, an
  owned format rather than a markdown heading. They stay.
- **The paragraph-termination block starts** (`round_record.py#BLOCK_START`,
  `.github/scripts/issue_claims_check.py#BLOCK_START`,
  `survivor_check.py` line 583, `unverified_check.py#_paragraph_ends_at`):
  the question *where does a hand-wrapped paragraph end*, carried by three
  script roots that cannot import one another and pinned pairwise
  (`tests/test_the_record_is_generated.py::test_the_two_spellings_differ_only_by_the_fence_openers`).
  The ATX half of `_paragraph_ends_at` asks the one rule after this work;
  the rest stays.
- **`evidence_check.py#heading_slugs` and `GITHUB_HEADING_RE`**: a reader of
  GitHub's anchor set — ATX, setext, a heading behind a container, markup
  stripped — which answers *which `#slug` links resolve*, not *where does a
  section end*. It stays as it is.
- **`hooks/config.py#ATX_HEADING`** inside `gfm_table`'s table-end rule: the
  same ATX rule inside the walker that cmark-gfm already holds. It stays.

## Judgments the tree answered

Each of these was open in the issue and is decided here from the tree; the
grounds are the clause or the measurement named, and `questions.md` lists
them so nobody reopens one.

1. **The one answer to a duplicate row is a refusal, not first-wins and not
   last-wins.** `hooks/config.py#pact_declaration` already refuses a doubled
   `Pact notify` with *the first row is not the answer* (round 1 of PR #756,
   yellow 2), `docs/the-pact.md` ratified it, and a silent choice between two
   rows is a sentence nobody reads. Measured: this repository's own config
   and all 86 committed `routing.md` declarations hold no doubled label, so
   the rule costs no existing file.
2. **An absent file and an unreadable file are two states, and only the
   second is refused.** `hooks/config.py#declared_pacts` and
   `hooks/mode-gate.py#unreadable` (NAME NOT IN TREE since phase 1) each tell the two apart already, in
   opposite directions, for the reason each docstring gives: a gate that
   refuses wrongly is an outage, a command that reads a written row as
   absent is the silence the pact reader exists to end. Today the freeze arm
   of `evidence_check.py#frozen_from` and `correction_check.py#cutoff_at`
   turns OFF on an unreadable file, so `--reverify` re-stamps a released row
   in place and a pull request editing a frozen file passes — the permissive
   direction on the one row whose loss cannot be recovered.
3. **The coordinate grammar is `ANCHOR_RE`, and the copies disagree with it
   today.** Measured over 8,218 coordinates in the released ledgers: two
   rows (`bin/test`, `bin/round-record`, paths with no `.ext`) have no
   identity for `correction-check`, so a merge dropping their correction is
   silence; nine strings that are MALFORMED examples quoted in `0.15.5.md`
   (`docs/a.md#1장@abcdef12`, a space before the `@`) are identities for it
   and no coordinate for the checker; 47 rows are keyed on a fragment of
   their first cell because `correction_check.py` splits on a raw `|` while
   every other reader honours `\|`; `settle.py#COORDINATE_RE` and
   `ANCHOR_RE` match the same 8,218 spans, so no segment moves.
4. **A heading is CommonMark's ATX heading on shown lines, and setext
   headings are not read.** Measured over the 768 tracked `.md` files with
   markdown-it 4.2.0: 246 heading-looking lines stand inside closed fences
   and are read as headings today, in 39 files; no ATX heading is indented
   one to three spaces; the 35 setext headings markdown-it finds are all a
   front-matter line under its `---` closer (`skills/*/SKILL.md`, the eval
   graders, one issue template), which GitHub renders as a table and not as
   a heading. So setext is left out with that ground, and the oracle case
   says so the day a real one appears.
5. **The heading fix moves released rows, and that is paid under the rule
   the tree has.** Measured: 28 heading-path citations across the release
   files change region when fenced lines are blanked — `CONTRIBUTING.md`
   §*Running the checks* ends 61 lines early today at a fenced `##`; two
   `agents/warden.md` headings (`## Verdicts`, `## Paste-ready fixes`) exist
   only inside a fenced report template, so those rows go BROKEN and are
   re-pointed by a `Corrected ·` row to the heading that holds the fence.
   `docs/the-evidence-ledger.md` §*A released row is read again in the
   branch's fragment* is the procedure; #836 may change what a row's claim
   is after this, and it inherits one grammar either way.
6. **A `#NNN`-led prose line is not a heading, and the record readers stop
   treating it as one.** `chain_check.py#heading_level` and
   `unverified_check.py#headings` read `startswith("#")`, so a wrapped line
   beginning with an issue number ends a `## Verdicts` or `## Not verified`
   section early and the rows below it fall outside — the permissive
   direction. Measured: 0 such lines in the 11 round records at v0.18.3 and
   at v0.19.0, 28 in `spec.md`/`plan.md`/`overview.md` at v0.19.0, 107 in
   `docs/`, `agents/`, `skills/` and `templates/` today.
7. **The one heading reader lives in `unverified_check.py`, not in
   `hooks/blocks.py`.** No hook reads a heading; every consumer is under
   `skills/` or `.github/scripts/` and already loads the shared reader.
8. **The vendored copy keeps a twin of each rule and a case holds the twin
   equal**, the arrangement `vendored_fence_opener`, `vendored_split_row`,
   `gfm_lines` and `PACT_WORD` already have. `vendored_config_rows` has no
   such case today — the inventory's row E46 says it does, and `grep` over
   `tests/` finds no case naming it; this work adds the case.

## What this delivers — the standing statements

Each is written to be folded into `docs/` at the release; the case named
beside it is what the build plants, seen red first.

**`seal/config.md` has one reader, and a row written twice has no value.**
`hooks/config.py` answers one item with a value, with nothing, or with a
refusal that names the item and how many times it was written. A hook reads
a refusal as nothing declared and says nothing; a command prints it and
exits 2 with nothing judged, the shape a non-numeric `Ledger frozen from`
already takes. The writer, `seal mode`, refuses to write a file that holds
two `Mode` rows and names both lines, because a writer that picks one leaves
a file no command can bring into agreement.

**A `seal/config.md` that is there and cannot be read is refused; one that
is absent declares nothing.** The two states are told apart in the reader,
once, and never by a caller opening the file a second time. The freeze arm
never turns off because the file could not be read.

**A `routing.md` label written twice has no value.** A strict label doubled
makes the file no declaration, so the commit gate asks as it does for any
file that does not parse; an optional label doubled is unanswered.

**The ledger coordinate has one grammar, and every reader reaches it by
import.** `evidence_check.py#ANCHOR_RE`, with its path, locator and hash
pieces named so a reader of a part can take the part. A row's identity for
`correction-check` is its coordinates with the hash dropped, read by that
grammar through the escape-honouring cell split; a rider stamp's locator and
hash are the coordinate's minus the path.

**A markdown heading is CommonMark's ATX heading, read where a renderer
shows it, and `unverified_check.py#heading_level` is its one spelling.** A
`#` run inside a closed fence, a `#NNN` at the start of a wrapped line and a
`#######` are not headings; a heading indented up to three spaces is. The
checker's `.md` regions are computed on lines with closed fences blanked and
hashed over the lines as written, so a region's end moves and its bytes do
not. `tests/commonmark_oracle.py` answers which lines markdown-it reads as
ATX headings and the reader is held to it over the frame's shapes, a seeded
corpus and every tracked `.md` file.

**A vendored copy of the checker carries a twin of each rule it cannot
import, and a case holds every twin equal over a shape table.** The config
reader's twin stays blind to fences and comments, as the inventory's row E46
states, and the case's table says so by holding no fenced shape.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 a config row written twice | Given a `config.md` with two `Ledger frozen from` rows, when `evidence-check` or `correction-check --range` runs, then it exits 2 naming the row and the count, and nothing is written or judged; when `hooks/mode-gate.py` runs over the same file with two `Mode` rows, then it says nothing | cases in `tests/test_a_released_row_is_read_again_in_a_fragment.py`, `tests/test_a_merge_cannot_silently_drop_a_correction.py` and `tests/test_the_mode_question_is_asked_once.py`, each seen red against the first-wins or last-wins reading |
| S2 the writer meets two rows | Given a `config.md` with two `Mode` rows, when `seal mode shared` runs, then it refuses naming both lines and writes nothing; `seal mode --check` exits non-zero the same way | a case in `tests/test_the_mode_question_is_asked_once.py` |
| S3 an unreadable config | Given `seal/config.md` is a directory, or holds bytes that do not decode as UTF-8, when `evidence-check`, `correction-check`, `fold-check`, `broad-gate` or `pact-check` runs, then each exits 2 naming the path and nothing is judged; when `hooks/mode-gate.py` or `hooks/evidence-advisor.py` runs, then it says nothing; an absent file still reads as nothing declared everywhere | one case per command, the fixtures a directory and a non-UTF-8 file, which hold on macOS, Linux and Windows alike |
| S4 the vendored config twin | Given the shape table of config tables (a doubled row, an empty value, an escaped pipe, a stray separator, a second header, no header), when the plugin's reader and the checker's twin read each, then rows and values are equal; the table holds no fence and no comment, and the case says why | a case beside `tests/test_evidence_check.py::test_the_vendored_cell_rule_agrees_with_the_shared_one` |
| S5 a routing label written twice | Given a `routing.md` with two `Review` rows, when the commit gate reads it, then it is no declaration and the gate asks; with two `Planning` rows the declaration stands and `Planning` reads as unanswered | cases in `tests/test_routing_is_recorded.py`, seen red against the last-wins reading |
| S6 one coordinate grammar | Given the 0.8.2 release row anchored at `bin/test#"…"@hash`, when `correction-check` reads it, then the row has that coordinate as its identity; given the MALFORMED examples quoted in the 0.15.5 release file, then none is an identity; given a row whose first cell holds `\|`, then its key is the whole cell | cases in `tests/test_a_merge_cannot_silently_drop_a_correction.py`; a case that `correction_check.py`, `settle.py` and `rider_check.py` define no pattern matching `@[0-9a-f]{6` of their own |
| S7 settle's segments do not move | Given this repository's release files, when `settle`'s coordinate reader runs through the checker's grammar, then every path it attributes is the one it attributed through its own copy | a case in `tests/test_settle_reads_before_it_removes.py` over `seal/releases/*.md` (measured 0 difference over 8,218 spans) |
| S8 a fenced `##` opens no section | Given a `.md` with one real `## B` and one `## B` inside a closed fence, when the checker resolves `"## B"`, then it resolves to the one real section rather than reading as ambiguous; given `   ## B` indented three spaces, then it is a heading; given `#84's line` at column 0, then it is not | cases in `tests/test_a_row_points_by_content.py`, the first the executed probe of #834 part 4 row E15 turned into a case, seen red before the rule moves |
| S9 the record readers' sections | Given a round record whose `## Verdicts` section holds a wrapped line beginning `#120)`, when `chain-check` reads the section, then the rows below that line are inside it; the same for `## Not verified` in `unverified-check` and for `fold-check`'s statements | cases in `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` (or the module that holds `section_end`'s cases), `tests/test_unverified_rows_close.py` and `tests/test_a_folded_statement_names_what_enforces_it.py`, seen red |
| S10 the oracle holds the rule | Given the frame's shapes, a seeded generated corpus and every tracked `.md` file, when `heading_level` is asked of each line a renderer shows, then its answer equals markdown-it's ATX heading set for the document; and every setext heading markdown-it finds in the tree is a front-matter line | a property case beside `tests/test_the_hooks_hide_what_a_renderer_hides.py`, reading `tests/commonmark_oracle.py` |
| S11 the released rows are re-read, not edited | Given the heading rule moves, when `evidence-check --strict .` runs, then it names each released heading-path row that drifted or broke; after `--reverify --into seal/ledger/<this id>.md --checked <date>` and the `Corrected ·` rows for the two `agents/warden.md` headings, then the ledger arm exits 0 and `correction-check --range` is clean | executed in phase 5 and recorded in `overview.md` with the row count (expected at most 28 citations, fewer distinct rows) |
| S12 the copies are gone | Given the tree after the build, when the enumeration greps run — `@\[0-9a-f\]\{6` outside `evidence_check.py`, and `#\{1,6\}` or `startswith("#` in a reader of a markdown heading outside `unverified_check.py`, its vendored twin, the slugger and the walker — then each finds nothing | a case that runs the two greps over `hooks/`, `skills/` and `.github/scripts/` with the named exemptions, so the next copy is red on arrival |

## Data & interfaces

New or changed names; the lines naming a unit the tree does not carry yet
say so.

- `hooks/config.py`: a reader of the file that returns its text or a refusal
  that tells absent from unreadable, and a reader of one item over the rows
  that returns a value or a refusal naming a doubled item — `config_value` · NAME NOT IN TREE.
  `declared_mode`, `reference_roots`, `declared_pacts` and `pact_declaration`
  read through them; `pact_declaration`'s own doubled-row sentences become
  the generic one's.
- `hooks/mode-gate.py#unreadable` is removed; the gate asks the reader · NAME NOT IN TREE.
- `hooks/routing.py#parse`: a doubled label has no value.
- `skills/evidence-check/scripts/evidence_check.py`: the locator and hash
  pieces of `ANCHOR_RE` exported as named strings beside `ANCHOR_PATH` and
  `ANCHOR_NAME` — `ANCHOR_LOCATOR`, `ANCHOR_HASH` · NAME NOT IN TREE;
  `frozen_from` through the config reader's value rule; a twin of the value
  rule and of the heading rule beside `vendored_config_rows` —
  `vendored_config_value`, `vendored_heading_level` · NAME NOT IN TREE; a
  `heading_rule` · NAME NOT IN TREE switch beside `fence_rule` and
  `cell_rule`; `heading_path`, `text_regions` (markdown), `file_units` (`.md`),
  `citation_for`, `content_matches` and `resolve_unit` compute `.md` regions
  over `gfm_lines(unquoted(text))`; `heading_level` becomes the twin's name
  or a thin alias of the rule, never a second spelling.
- `skills/evidence-check/scripts/correction_check.py`: loads the checker by
  path beside the two it loads today; `Row.anchors` and `corrections` read
  `ANCHOR_RE`; `Row.key` reads `reader.split_row`; `ANCHOR` and `CITATION`
  are removed; `cutoff_at` through the value rule and the unreadable rule.
- `skills/settle/scripts/settle.py`: `COORDINATE_RE` removed; `coordinates`
  and `anchored_rows` read the checker's grammar.
- `skills/settle/scripts/fold_check.py`: `HEADING` and `row_value` removed;
  `config_rows` refuses an unreadable file at exit 2.
- `skills/implement/scripts/seal.py`: `table_span` and `with_row` refuse two
  `Mode` rows naming both lines.
- `skills/verify/scripts/unverified_check.py`: `heading_level(line)` — the
  one spelling, lifted out of `_paragraph_ends_at`, which calls it;
  `headings` reads it.
- `skills/verify/scripts/broad_gate.py#broad_command`: through the value
  rule; a refusal reaches the sealer's gate as exit 2 naming the row.
- `skills/verify/scripts/payload_meter.py#heading_starts`,
  `skills/code-review/scripts/chain_check.py#heading_level`,
  `skills/code-review/scripts/survivor_check.py#ledger_rows`: read the one
  rule.
- `.github/scripts/rider_check.py`: the stamp pattern is built from the
  checker's locator and hash pieces at `load_checker`.
- `tests/commonmark_oracle.py`: `heading_lines` · NAME NOT IN TREE — the
  lines markdown-it reads as ATX headings, with their level, from the
  parser's `heading_open` tokens whose markup is a `#` run; imports
  unchanged, so `tests/test_the_hooks_hide_what_a_renderer_hides.py::test_the_oracle_imports_the_parser_and_nothing_of_this_repositorys`
  keeps holding.
- `templates/config.md` and `skills/evidence-check/SKILL.md`: say what a
  doubled row and an unreadable file do, beside the non-numeric freeze row.

## Open questions → questions.md

`questions.md` holds no row a person must answer; its head lists the eight
judgments above, and its rows are two the work settles and one a measurement
already settled.

Framed 2026-10-07 by framer, before the build.
