# Implementation Plan: config rows, the ledger coordinate and a markdown heading each have one reader (#867)

<!-- seal/specs/1791384156-config-rows-coordinates-and-headings-have-one-reader/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-08 by the repository owner, when `smith` was spawned.

## Summary

Three formats the repository owns are each read by several copies that
answer differently (#834, part 4). This work leaves each with one reader and
one answer: `hooks/config.py` for `seal/config.md` rows, with a doubled row
refused and an unreadable file told apart from an absent one;
`evidence_check.py#ANCHOR_RE` for the ledger coordinate, reached by import
from `correction_check.py`, `settle.py` and `rider_check.py`; and
`unverified_check.py#heading_level` for a markdown heading, CommonMark's ATX
rule on shown lines, held to markdown-it through `tests/commonmark_oracle.py`.
Six phases: the hooks, the commands, the grammar, the heading rule, the
checker's regions and the released rows they move, then the record. Two
formats the issue lists are filed rather than built, with the grounds in
`spec.md` §*Scope* and the issue texts in §*Operational impact* below.

## Technical context

Coordinates are at 5623d728 (0.20.0 as shipped), which this branch is cut
from; the inventory's row ids are part 4's.

**The config reader and its callers.** `hooks/config.py#indexed_config_rows`
(line 345) is the one walk and `config_rows` (306) its projection; both read
through `unfenced` (235), which reads `hooks/blocks.py`'s walk.
`declared_mode` (490) and `reference_roots` (549) open the file themselves,
take the first matching row, and fold an unreadable file into *none*;
`declared_pacts` (994) returns None for an unreadable file, on purpose, and
`pact_declaration` (819) refuses a doubled `Pact` or `Pact notify` row.
`hooks/mode-gate.py#unreadable` (156; NAME NOT IN TREE since phase 1) opens the file a second time to tell
unreadable from none. Outside `hooks/`: `evidence_check.py#frozen_from`
(3872) takes the last row and turns the freeze off on an unreadable file
(E47); `correction_check.py#cutoff_at` (929) the same (C17);
`fold_check.py#config_rows` (491) reads an unreadable file as no row at
exit 0 (F11) and `row_value` (509) takes the first (F12);
`seal.py#table_span` (1430) writes the first, saying the reader reads the
first (X16); `broad_gate.py#broad_command` (798) takes the first and reads
an unreadable file as no row; `evidence_check.py#record_pact_changes`
(4616) refuses an unreadable file; `pact_check.py` (585) exits 2
`UNREADABLE`. The vendored twin `evidence_check.py#vendored_config_rows`
(3830) knows no fence or comment and is held equal by no case.

**The coordinate grammar.** `evidence_check.py#ANCHOR_RE` (146) with
`ANCHOR_PATH` and `ANCHOR_NAME` (144–145), `RECORD_COORD_RE` (4962) built
from the same pieces. `correction_check.py#ANCHOR` (427) requires `.ext`
before the `#` and takes `@hex{6,}`; `CITATION` (580) is a second spelling
for a quoted locator; `Row.__init__` (446) splits cells on a raw `|`.
`settle.py#COORDINATE_RE` (196) is a narrowed copy.
`rider_check.py#NEW_STAMP` (156) is the locator and hash alternatives minus
the path. `correction_check.py` loads `unverified_check.py` (`load_reader`,
239) and `hooks/config.py` (`load_config`, 268) by path; `settle.py` loads
the checker (`CHECKER`, 174) in `anchored_rows` (619); `rider_check.py`
loads it in `load_checker` (164).

**The heading rule.** `evidence_check.py#heading_level` (517) is
`^#{1,6}\s` on raw lines; `heading_path` (567), `text_regions` (522),
`file_units`' `.md` arm (928), `citation_for` (2424), `content_matches`
(1024) and `resolve_unit` (652) read it, over `gfm_lines(text)` rather than
`gfm_lines(unquoted(text))`; `pact_check.py#clause_hash` (430) inherits it.
`unverified_check.py#_paragraph_ends_at` (551–561) already spells
CommonMark 4.2 inline and `headings` (693) reads `startswith("#")`;
`chain_check.py#heading_level` (1238) the same with a depth;
`survivor_check.py#ledger_rows` (1163) the same; `fold_check.py#HEADING`
(139) is the CommonMark rule; `payload_meter.py#heading_starts` reads its
own `HEADING`. `judge` (1669) hashes the region's lines as written, so a
region computed on blanked lines hashes the same bytes.

**The oracles.** `tests/commonmark_oracle.py` reads markdown-it 4.2.0
(`run_tests.py#MARKDOWN_IT`) and answers which lines a renderer hides; its
imports are pinned. `tests/gfm_table_oracle.py` reads cmark-gfm 2025.10.22
and holds `gfm_table`. Neither holds a heading rule today.

**What breaks in six months.** The twin in the vendored checker drifts from
the plugin's reader on a shape the equality case's table does not hold.
That is the failure every twin here already carries, and what bounds it is
that the table is the config template's own shapes plus the refusals this
work adds, not an example list. The second: #836 extends the coordinate's
locator to a test node id in `ANCHOR_RE`'s pieces and a reader that took a
piece by name keeps reading the old one — which is why every reader reaches
the compiled pattern and the stamp alone takes the pieces, under a case.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Make every config reader last-wins (or every one first-wins) | A person edits the row they see and the other one answers; the writer appends a third; no sentence ever reaches anybody, which is the silent choice #756's round 1 refused for `Pact notify` | rejected — a doubled row is refused |
| An unreadable config reads as nothing declared everywhere, the hooks' rule | The freeze turns off on a decode error: `--reverify` re-stamps released rows in place and `correction-check` passes a pull request that edits a frozen file (E47, C17 today) | rejected for commands |
| An unreadable config is refused everywhere, the pact reader's rule | `hooks/mode-gate.py` denies every Bash call in a cp949 console, the outage `CONTRIBUTING.md` names; `mode-gate.py#unreadable`'s docstring measured the case | rejected for hooks; refused in commands, silent in hooks |
| Copy `ANCHOR_RE` byte for byte into each reader and hold the copies equal by cases | The next locator form (#836's) lands in one and reddens three files; a copy held by a case is what the inventory counts as the shape that reopens | rejected — import |
| Keep `^#{1,6}\s` on raw lines and teach it fences alone | 246 fenced lines stop being headings, and `#84's` at column 0 and `#######` stay headings in the record readers; two rules again | rejected — one CommonMark rule, shown lines |
| Read setext headings too | The 35 setext headings in the tree are all a front-matter line under its `---`, which GitHub renders as a table; reading them makes every `SKILL.md`'s second line a heading | rejected, measured; the oracle case names the limit |
| Put the heading rule in `hooks/blocks.py` | No hook reads a heading, and every consumer already loads `unverified_check.py`; a second shared reader for one function | rejected |
| Move `config_rows` onto `gfm_table` | A header with a non-blank line above it is refused, so a `Broad gate` row becomes no row and the sealer stops; needs a migration and a prompt-budget argument of its own | filed (§*Operational impact*) |
| Unify the seven live-line rules | Four failure directions each argued for its reader's consequence; 0 issues since 0.18.0; a redesign of `claim_lines`' comment state is its own frame | filed (§*Operational impact*) |

## Phases

Vertical slices — each phase ends with something runnable and verified. A
case is planted only after it has been seen red (`agent-contract` §15), and
each phase that changes a gate's answer states the direction and the prompt
budget in its phase record (`CONTRIBUTING.md` §*What a change to a gate must
carry*); the budget is zero in every phase.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `hooks/config.py` reads the file once and tells absent from unreadable, and answers one item with a value, nothing, or a refusal naming a doubled item; `declared_mode`, `reference_roots`, `declared_pacts`, `pact_declaration` read through it (the pact reader's own doubled-row sentences become the generic one's); `hooks/mode-gate.py#unreadable` (NAME NOT IN TREE since phase 1) removed; `hooks/routing.py#parse` reads a doubled strict label as no declaration and a doubled optional one as unanswered. Direction: hooks say nothing on a refusal, the gate asks on a doubled strict label (0 of 86 declarations today) | S1's hook half, S5; red first in `tests/test_the_mode_question_is_asked_once.py`, `tests/test_a_reference_root_is_read_and_never_taken.py`, `tests/test_a_signer_declares_its_pact.py`, `tests/test_routing_is_recorded.py`; `tests/test_the_hooks_hide_what_a_renderer_hides.py` and `tests/test_one_table_walker_reads_what_gfm_renders.py` unchanged and green | 456aa0af |
| 2 | Every command reads config through phase 1 and refuses at exit 2 naming the row or the path: `evidence_check.py#frozen_from` (with `vendored_config_rows` and a twin of the value rule, held equal by S4's shape table), `correction_check.py#cutoff_at`, `fold_check.py#config_rows` (and `row_value` removed), `broad_gate.py#broad_command`, `seal.py#table_span`/`with_row` refusing two `Mode` rows naming both lines, `pact_check.py` unchanged. `templates/config.md` and `skills/evidence-check/SKILL.md` say what a doubled row and an unreadable file do. Direction: refuse more, in commands only | S1's command half, S2, S3, S4; one case per command, the unreadable fixtures a directory and a non-UTF-8 file; `tests/test_the_mode_question_is_asked_once.py::test_seal_mode_still_writes_a_second_mode_row_for_a_bare_pipe` re-read: the reader still sees one row of that file, so the case stands with its sentence corrected | bad39695 |
| 3 | One coordinate grammar: `ANCHOR_RE`'s locator and hash pieces exported by name; `correction_check.py` loads the checker and reads `ANCHOR_RE` for `Row.anchors` and `corrections`, `reader.split_row` for `Row.key`, `ANCHOR` and `CITATION` removed; `settle.py` reads `checker.ANCHOR_RE` in `coordinates` and `anchored_rows`, `COORDINATE_RE` removed; `rider_check.py` builds its stamp from the checker's pieces at `load_checker`. Direction: `correction-check` gains an identity for two released rows and loses nine MALFORMED-shaped ones; nothing else moves | S6, S7, S12's first grep; red first in `tests/test_a_merge_cannot_silently_drop_a_correction.py`, `tests/test_settle_reads_before_it_removes.py`, `tests/test_a_rider_reaches_its_file.py` | 776f6370 |
| 4 | The heading rule: `unverified_check.py#heading_level` lifted out of `_paragraph_ends_at`; `headings`, `chain_check.py#heading_level`, `survivor_check.py#ledger_rows`, `fold_check.py#HEADING` (NAME NOT IN TREE since phase 4), `payload_meter.py#heading_starts` read it; `tests/commonmark_oracle.py` answers the ATX heading lines from `heading_open` tokens; a property case holds the rule over the frame's shapes, a seeded corpus and every tracked `.md`, and asserts every setext heading in the tree is a front-matter line. Direction: a record's section runs past a `#NNN`-led line to its real end — more rows inside `## Verdicts`, `## Not verified` and a fold statement, the stricter direction; 0 such lines in the round records at v0.18.3 and v0.19.0 | S9, S10; red first in the modules holding `section_end`'s cases, `tests/test_unverified_rows_close.py`, `tests/test_a_folded_statement_names_what_enforces_it.py` and the new property case | d515308a |
| 5 | The checker reads headings by the rule on shown lines: a `heading_rule` switch beside `fence_rule` with a vendored twin held equal; `heading_path`, `text_regions`, `file_units`, `citation_for`, `content_matches`, `resolve_unit` compute `.md` regions over `gfm_lines(unquoted(text))`; `pact_check.py#clause_hash` inherits. Then the released rows: `evidence-check --strict .` names each drifted or broken heading-path row (measured at most 28 citations), `--reverify --into seal/ledger/<this id>.md --checked <date>` writes the `Re-read ·` rows, and the rows citing `agents/warden.md`'s fenced `## Verdicts` and `## Paste-ready fixes` get `Corrected ·` rows re-pointed to `## Report`, each read by the smith. Direction: a region ends where the renderer's section ends; a row anchored on a quoted heading is BROKEN and re-pointed | S8, S11, S12's second grep; red first in `tests/test_a_row_points_by_content.py` (the #834 E15 probe as a case, `   ## B`, `#84's`), the twin's equality case; `evidence-check --strict .` and `correction-check --range` exit 0 on the branch after the fragment is written | 3327c81e |
| 6 | The record: `changelog.md`, `overview.md` (§*Not verified* with the rows phase 5 wrote), ledger fragment rows for the new units, `tests/test_a_record_states_what_the_tree_has.py` green over this directory (the `NAME NOT IN TREE` lines in `spec.md` drop their marker once the names exist), the two issue texts in §*Operational impact* handed to the session to file, any rider on a moved unit answered or re-stamped | the five hygiene modules the brief names plus every module a phase touched; the broad gate is the sealer's | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Seams with the sibling frames of 0.21.0

- **#836** (a ledger row's claim is the test that enforces it): touches
  `evidence_check.py`'s reverify and family units and
  `docs/the-evidence-ledger.md`. This work touches the grammar constants
  (phase 3) and the `.md` region readers (phase 5), none of which #836
  names. If #836 adds a locator form, it adds it to `ANCHOR_RE`'s pieces
  once and every reader inherits it; either order lands, and the rebase is
  on constants. Phase 5's `Re-read ·` and `Corrected ·` rows are written
  under the rule the tree has; if #836 changes what a re-read is before
  phase 5 runs, phase 5 writes what #836's rule asks instead.
- **#870** (a unit the extractor cannot bound is refused): touches
  `generic_units` and the generic arms of `file_units` and `resolve_unit`.
  Phase 5 touches the `.md` arms of the same two functions. Disjoint hunks
  in shared functions: whichever lands second rebases on the other.
- **#866** (a round-record cell has one reader): touches `chain_check.py`
  and `round_record.py` cell readers. Phase 4 touches
  `chain_check.py#heading_level` alone, which no cell reader is.
- **#835** (a reader declares its input class): the registry reads #834's
  table. The units this work adds — the config value rule, the heading
  rule, the twins — are rows of that registry where it has landed before
  phase 6; phase 6 adds them there, classed `owned` (the config table, the
  coordinate) and `observed` (the heading rule, held to markdown-it).

## Operational impact

- **What a user sees change.** `evidence-check`, `correction-check`,
  `fold-check`, `broad-gate`, `seal mode` and `pact-check` exit 2 on a
  doubled config row or a `seal/config.md` that is there and cannot be read,
  naming it. The commit gate asks on a `routing.md` whose strict label is
  written twice. The checker's `.md` regions end where a renderer's section
  ends, so a user's released heading-path rows may drift once, repaired by
  their own `--reverify` (or `--reverify --into` under a freeze).
  `correction-check`'s row identities change for a path with no `.ext` and
  for a quoted MALFORMED example.
- **The vendored checker.** `tools/evidence_check.py` picks up the twins at
  the next `/specseal:evidence-ci`, as every change to the checker does.
- **No new dependency.** markdown-it is already the suite's; the hooks and
  the scripts stay standard library.
- **Two issues to file** (the session's act, not the build's; both into
  milestone `release: 0.21.0` or its successor as the owner decides):
  1. *fix: `seal/config.md`'s `| Item | Value |` table is read by its own
     grammar, not by the walker cmark-gfm holds* — `hooks/config.py#config_rows`
     is an owned grammar held by hand cases; `gfm_table` is held to
     cmark-gfm over an enumerated corpus. Moving the config table onto the
     walker refuses a header with a non-blank line above it, which turns a
     `Broad gate` row into no row and stops the sealer. What to decide: the
     migration for installed configs and the prompt budget of a refusal that
     reaches a hook. Grounds: #834 part 2 rows 95, 108; #867's frame.
  2. *fix: whether a ledger or record line is live has seven rules with four
     failure directions* — `quoted_lines`, `live_lines`, `claim_lines`,
     `anchored_rows`, `readable`, `hidden_lines`, the rider's `quoted_lines`.
     Measured 2026-10-07: the first two agree on every released row;
     `readable` blanks 46 rows in eight release files the checker reads on
     purpose. What to decide: per reader, which consequence its direction
     protects and whether one rule with a stated bias can carry all seven;
     `claim_lines`' deferred positional scanner is part of it. Grounds: #834
     part 4 §*Observations*; #867's frame.
