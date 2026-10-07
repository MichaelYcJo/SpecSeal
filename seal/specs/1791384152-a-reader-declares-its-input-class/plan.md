# Implementation Plan: a reader declares its input class (#835)

<!-- seal/specs/1791384152-a-reader-declares-its-input-class/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved <date> by <who>, when `smith` was spawned.

## Summary

Three phases, landed in order, each one commit or a few. Phase 1 is the
registry check and the census it starts from, and it changes no reader.
Phase 2 is the `## Removes` section: the template, the records arm that reads
it, the config row, and the per-phase table it retires. Phase 3 is the
document that states both rules and the fragments. The whole item builds
**after every other 0.21.0 chain has squashed and before #834's build**, for
the reasons under *Operational impact*.

## Technical context

Existing code this builds on, as read on 2026-10-08 at this frame's tree:

- `skills/evidence-check/scripts/evidence_check.py#py_spans` (:442) —
  `{qualified name: [(start, end)]}` for defs, classes and constants, memoised
  per text; `#content_hash` (:438) — the eight-hex hash over a span. The
  census hashes with these two, imported by path the way
  `tests/test_a_document_has_room_for_the_next_fold.py#_load` loads
  `fold_check.py`.
- `evidence_check.py#claim_lines` (:5025) — which record lines are claims
  (fences and HTML comments are not); `#file_claims` (:5460) — the name
  half (`stated_names`, `stated_coordinates`, `coordinate_misses`) and the
  stamp half (`check_text`) over one record; `#check_records` (:5528) —
  every live work item's records plus `seal/follow-up.md`;
  `#coordinate_misses` (:5238) — a `path#name` whose path resolves is read
  by token of that file, which is why a removed unit named in a live record
  is a miss today. `#resolve_unit` (:614) — the ledger's own resolution,
  used for the absence judgment. `#frozen_from` (:3872) — the
  `Ledger frozen from` reader; `Removes from` copies its shape.
- `tests/test_every_file_the_plugin_reads_or_writes_names_its_encoding.py`
  — `ALLOWED` (:115) with grounds per entry, `OPENERS` (:246) as K1,
  `judge` (:393) resolving a module call through the file's imports,
  `test_the_failure_names_the_site_and_the_repair` (:634). The registry
  check copies the shape and the import resolution for `subprocess` and
  `shlex`; attribute-name matching for methods is the encoding test's
  `Path.open` approach, with the same honesty about what a static walk
  cannot follow.
- `tests/test_every_reader_ends_a_line_where_gfm_does.py#splitlines_calls`
  (:719) and `#_walk` (:734) — a census of calls keyed `(path, unit)` over
  `hooks`, `skills`, `.github/scripts`; `OUT_OF_CLASS` held closed by
  `test_every_splitlines_call_left_is_named_with_its_reason` (:754). The
  registry walker is this walk with K1 in place of one attribute and the
  unit cut at the top level.
- `skills/verify/scripts/unverified_check.py#parse_section` (:698) and
  `#check_text` (:824) — the shape a machine-read markdown section has here:
  a fixed header, `none — <why>` as the alternative, the placeholder refused.
  The `## Removes` reader in the records arm copies the shape, not the code.
- `templates/sdd-spec.md` (53 lines; the mark is the last line and
  `tests/test_waiver_decided_at_start.py` :721 and
  `tests/test_the_chain_goes_back_to_its_framer.py` :447 hold it there);
  `templates/sdd-phase.md` §*What this phase removes* and
  `tests/test_a_phase_hands_the_next_one_a_record.py::test_removes_section_is_a_table_with_a_none_row`
  (:234); `agents/framer.md` :94 (the writes table's `spec.md` row) and :342
  (the report's *What you put out of scope* line).
- `templates/config.md` §*The ledger freeze* (:481) — the row table
  shape (`Row | Value | Absent`) a new config row is documented in;
  `seal/config.md` (14 lines, six rows).
- `docs/the-record-layout.md` §*docs/* (:115) — the table a new document
  takes a row in; nothing pins that table (grep over `tests/` on
  2026-10-08).

**Constraints.** The check calls git for nothing (`docs/the-evidence-ledger.md`).
Every text file is opened with `encoding="utf-8"`. Each failure text a
person reads is pinned in the commit that writes it (§14). A case is seen red
before it is planted (§15). The walker's K1 is a list to extend, never an
exemption list to grow.

**Failure scenario of the chosen approach, six months on.** Two, stated so
nobody discovers them. First, the census never empties because #834's
backfill stalls: then only new and changed units ever declare, and the
population's majority stays silent under `unread`. The census only shrinks and
each touch declares one unit, so the direction is right and the speed is
#834's. Second, a `Reads:` line goes stale when a reader is redesigned from
`guess` to `owned` and the line is not moved: nothing re-reads a class, as
nothing re-reads an `Enforced by:` target. The warden reads the diff's lines;
that is the whole re-reading, and `docs/the-reader-registry.md` says so.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A table under `docs/`, the ticket's wording | the ceiling holds top-level `docs/*.md` to 1,000 lines and the inventory is 2,287; every reader change edits one shared file across eleven branches; a second copy of a judgment the docstring carries; the table's own `Class` parse read 1,381 of 1,467 rows | rejected; `questions.md` Q1 puts the ticket's wording in front of the owner, default as chosen |
| A table under `docs/readers/`, outside the ceiling's top level | the same shared file and the same second copy; it dodges `fold-check`'s letter and not the reason settle §2 states | rejected |
| A per-work-item fragment `seal/readers/<id>.md`, folded at release | a second ledger: 84 % of ledger rows since 0.18.0 are bookkeeping (part 7), and this would add 654 more with a fold of their own | rejected |
| Declaration by decorator | needs a module every hook and script imports; hooks are standalone `python3 <script>` entry points, and a docstring line needs nothing at runtime | rejected |
| Population = every top-level unit, `nothing` for the rest | 1,521 declarations, 867 of them `nothing`; the backfill touches every function in the tree | rejected; a K1 call is what makes a unit a reader |
| Test functions in the population | a pin's class is its assertion's shape, already known; 3,817 pins would each carry a line that says what the `assert` says | rejected; stated in `spec.md` §Out |
| Rule 2 as a ratchet on `Reads: guess` | the count is unknown until the census empties; a ratchet needs an exemption list, and §14 requires new pins for every message change | deferred to the owner with the count, after #834's build |
| Rule 2 read from the pull request body or from prose | the guess class the inventory counts as the shape that reopens | rejected |
| Rule 2 in `unverified-check --baseline` (existence at the base verified) | a second reader of `spec.md` beside the records arm, which would still refuse the removed names; the hygiene step name is copied into `broad_gate.py` (#869's file) and would move | rejected; the records arm reads it, and the warden opens the base |
| Rule 2 in a test of this repository only | the records arm still refuses the names, so the arm learns the section anyway; a second reader for one judgment | rejected |
| Keep the per-phase removal table beside `## Removes` | two records of one fact, the shape #834 found disagreeing with itself | rejected; the table retires |
| The census inside the test module as a constant | 654 lines in a module; #834's script rewrites it; a data file diffs and parses as one line per unit | rejected for a `.txt` beside the test |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `tests/test_a_reader_declares_its_input_class.py`: the walker (population by K1 over the five roots, top-level unit, methods and nested defs folded into it), the `Reads:` grammar reader, the census reader, planted-root cases R1–R7 and R9, the real-tree case R8; `tests/undeclared_readers.txt` taken from this tree at the phase's commit; `py_spans` and `content_hash` imported from `evidence_check.py`, `judge`-style import resolution for `subprocess`/`shlex` reused from the encoding test. No reader's body changes | the module's cases; R8 seen red twice — one census line deleted, one census hash altered — and the texts of R1–R4 pinned (§14, §15); `uvx ruff check` on the module | |
| 2 | `templates/sdd-spec.md` §*Removes* above the mark; `agents/framer.md` :94 and :342 name it; `evidence_check.py`: `claim_lines`/`file_claims` read the `## Removes` section's rows as absence claims (`STANDING` via `resolve_unit`, the names on those lines skipped by the name half, a non-coordinate cell refused), a `Removes from` reader in `frozen_from`'s shape through the one config reader the tree has, presence required at or above the cutoff; `templates/config.md` documents the row; `seal/config.md` gets `Removes from | <epoch at the write>`; `templates/sdd-phase.md` §*What this phase removes* removed with its pins in `tests/test_a_phase_hands_the_next_one_a_record.py` and every carrier `grep -rn "What this phase removes"` finds; this item's own `## Removes` row goes from `STANDING` to clean in the same phase | the arm's cases S1–S7 as planted roots in the evidence-check test module that owns the records arm; S8's pins; `bin/evidence-check .` exit 0 at the phase's last commit and exit 1 naming `STANDING` at a probe commit before the template section is removed (S9) | |
| 3 | `docs/the-reader-registry.md` (the four classes, the grammar, the population and K1, the census, `## Removes`, what neither check reads, the counts at landing as a reading); `CONTRIBUTING.md` §*What a change to a gate must carry* two bullets; `docs/the-record-layout.md` §*docs/* row; `seal/specs/<id>/changelog.md`; `seal/ledger/<id>.md` rows per scenario | `bin/fold-check` exit 0; D1–D2; the five hygiene tests the brief names; `tests/test_a_folded_statement_names_what_enforces_it.py`; `tests/test_no_passage_is_pasted_into_a_second_file.py` unchanged | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

What a phase discovers while it is being built, and needs the next phase to
know, goes to `seal/specs/<work-item-id>/phases/phase-N.md`, from
`templates/sdd-phase.md`, when the phase closes. Phase 2 of this item changes
that template; a phase record written after it carries no removal table, and
phase 1's record, written before, carries one with a `none` row.

## Seams with the other 0.21.0 chains

| Sibling | The unit both touch | What this build does |
|---|---|---|
| #867 (`seal/config.md` rows, the coordinate grammar, headings have one reader) | `evidence_check.py` config reading (`frozen_from`, `config_reader`), `RECORD_COORD_RE`/`stated_coordinates`, the heading reader `## Removes` is found by | lands after #867; `Removes from` reads through the one config reader it leaves, the Removes cell through the one coordinate reader, the heading through the one heading reader. If #867 slips, `frozen_from` is generalised to `cutoff_row(root, item)` and `frozen_from` calls it, so one reader exists either way |
| #836 (a ledger row's claim is the test that enforces it) | `evidence_check.py` — reverify and families | no shared unit; phase 2 edits `claim_lines`, `file_claims` and adds the cutoff reader only |
| #870 (a unit outside Python is refused, not guessed) | `evidence_check.py#generic_units` | not touched; `resolve_unit` is called, not changed |
| #866, #869 (`broad_gate.py`) | the hygiene step names `broad_gate.py` copies | not touched; no hygiene step is added or renamed |
| #834 (the inventory's build) | every reader file's docstrings; `tests/undeclared_readers.txt` | #834 builds after this item: it writes `Reads:` lines from the inventory's rows and removes census lines, and says in its own spec where `inventory/` ends |

## Operational impact

- **No migration, one new config row.** `Removes from` in `seal/config.md`,
  set at the build to the epoch second of the write. A consuming repository
  without the row has presence unchecked; one with a `## Removes` section in
  a live `spec.md` has its rows read as absence claims from this release on,
  which the changelog fragment says.
- **The order of landing is the cost control.** This item builds after the
  other 0.21.0 chains have squashed and before #834's build. Earlier, every
  sibling that edits a census unit would have to declare it and delete its
  census line on a branch cut before the file existed, and ten branches
  deleting neighbouring lines of one sorted file conflict at the squash.
  Later than #834 is impossible, because the backfill empties a census that
  has to exist. What 0.21.0 therefore does not get: its own reader changes
  declared at the time they were made. The brief asked each frame to state
  its readers' classes in its `spec.md`, so #834's backfill can read them
  there.
- **No new dependency, no new workflow step, no `CLAUDE.md` row.** The
  failure text of each check is the instruction, pinned; the always-on
  surface does not grow (`CONTRIBUTING.md` §*Proposing a new gate or skill*).
- **Prompt budget.** Zero. Neither check asks anything; each refuses with the
  repair in the message, at the commit (the advisor), in CI and in the broad
  gate.
- **Failure direction.** Both checks block more, never allow more: an
  undeclared or changed reader stops the branch at the suite; a named
  removal still standing stops it at `--strict`. A wrong deny costs one
  docstring line or one row; a wrong allow — a typo'd coordinate passing as
  gone — is the warden's to catch at the base, and the document says so.
- **Platform.** The walker is `ast` over UTF-8 text with paths spelled `/`
  as the ledger spells them; nothing it reads differs by platform.
