# Implementation Plan: `settle` reads a marker inside a commented-out draft, and the opt-out arm accepts a directory as the marker

<!-- Annotated 2026-09-22, round 5's fix pass. The lines below marked `NAME NOT IN TREE` name units that pass removed: `is_block_boundary` and its lookahead, which decided where a paragraph ended and whose incompleteness removed a work item's directory, and the fuzz oracle and case `a_character_level_reading` and `test_the_scan_agrees_with_a_character_level_reading`, replaced by a reading written from the specification and a case asserting the safety direction rather than full agreement. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

<!-- Annotated 2026-09-22, round 4's fix pass. The lines below marked `NAME NOT IN TREE` name units this branch later removed: `blank_code_spans` and `opens_outside_a_comment`, deleted when one stateful scan replaced the three passes behind `live_lines`, and `test_one_comment_scanner_serves_both_readers`, renamed to `test_strip_comments_reads_through_the_one_comment_scanner` once that scan left `comment_scan` a single reader. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

<!-- seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-22 by the orchestrating session, when `smith` was spawned.
The owner pressed `automation` in the routing batch before the first edit, which
routes this gate through the session rather than stopping the run for it; the
owner has not read this plan. `questions.md` carries no row a person has to
answer.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval. The owner
pressed `automation` in the routing batch, which routes this gate through the
session rather than stopping the run for it — say so here the way the parent
plan did. -->

## Summary

Round 3 of #458's chain found that the rule *a line stops being live two
ways* had been given to `folded_items` in full and to `coordinates` by half,
and that the obvious way to carry the other half over — asking
`opens_outside_a_comment` of `seal/ledger.md` — loses three real section
markers, because ledger anchors quote comment openers inside backticks. This
work gives the rule **one owner**: a helper in the shipped reader that blanks
fences, then inline code spans, then asks the comment state, and every reader
of the fold record and the ledger sections goes through it. Beside it, three
small things the same round opened: the opt-out arm reads the marker with the
accessor `hooks/optin.py` rejected by name, the fragments loop is pinned by
nothing, and the single-scan pin pins agreement rather than a single scan.

**The shape that decides everything else:** the span pass sits *in front of*
`opens_outside_a_comment`, not inside `comment_scan`. `comment_scan` serves
`strip_comments`, whose exact output `seal/ledger.md:80` pins and round 3
measured over 1,435 files; teaching the scanner about backticks would change
what every record reader gets for a comment opener inside a code span. The
two fold readers need the span rule and nothing else does, so the pass is a
sibling of `blank_fences`, and the composition is a function of its own that
both callers name.

## Technical context

What this builds on, with coordinates at `3cdfd8ad`:

- `skills/verify/scripts/unverified_check.py#comment_scan` (`:151`),
  `#strip_comments` (`:182`), `#opens_outside_a_comment` (`:191`),
  `#blank_fences` (`:207`), `#readable` (`:231`), `#FOLD_MARKER` and its
  comment (`:71-102`), `#folded_items` (`:651`, the read at `:709-713`, and
  the comment at `:702-708` saying why it uses `enumerate` and not a paired
  walk). The helper goes beside `blank_fences`; `folded_items` switches to it.
- `skills/settle/scripts/settle.py#coordinates` (`:288`): `live =
  load(READER, ...).blank_fences` at `:314`; the ledger loop `:319-329`, which
  matches `MARKER_LINE_RE` and resets on `## `; the fragments loop
  `:330-336`. The docstring at `:301-312` names round 2's finding 5 and
  misattributes the fence rule's second copy to #487.
- `skills/settle/scripts/settle.py#main`: `optin.home_at(root)` at `:606`,
  `optin.git_common_dir(root)` at `:613`, `os.path.exists` at `:614`.
- `hooks/optin.py#home_at` (`:167`, `common` parameter documented at
  `:178-185`, `isfile` at `:200`), `#git_common_dir` (`:99`, the `.git`
  directory fast path at `:113-115`, so on a main worktree the second call
  costs no process and the case counts calls, not processes), `#SCRATCH`
  (`:46`).
- `skills/implement/scripts/seal.py#no_root` (`:663`) — the third reader of
  the marker, already `isfile`; the class is complete with `settle.py`.
- `tests/test_settle_reads_before_it_removes.py`: the `tree` fixture (`:88`)
  builds a repository with a ledger, three released items and one unreleased;
  `LEDGER` (`:36`) is the ledger text to extend; `run` (`:131`) drives
  `survey`/`report`/`retire` in-process; `test_a_fenced_marker_in_the_ledger_opens_no_section`
  (`:679`) is the shape A2, A3 and A5 sit beside;
  `test_an_opted_out_repository_is_told_which_state_it_is_in` (`:706`) and
  `test_a_repository_with_no_root_at_either_place_says_so` (`:589`) are the
  shapes A1 sits between; `test_a_missing_sibling_reader_is_a_sentence_and_not_a_traceback`
  (`:342`) shows `settle.load` is the seam A7's stand-in goes through.
- `tests/test_unverified_rows_close.py`: `uc` is the module loaded by path
  (`:24-32`); `test_one_comment_scanner_serves_both_readers` (`:1482`); (NAME NOT IN TREE)
  `test_readable_would_erase_every_fold_record` (`:1509`); the comment-shape
  family (`:1458-1479`) and the fence-shape family (`:1358-1376`) are what a
  changed `folded_items` must keep green.
- `tests/test_chain_hooks.py#reader_blanking_passes` (`:570`) and
  `#HIDDEN_CLOSING_WORD` (`:624`): the tie that derives the parametrisation
  from `readable`'s source. Untouched as long as `readable` is untouched.
- `tests/test_a_script_says_which_interpreter_it_needs.py#ABOVE_THE_FLOOR`
  (`:467`): `zip\(.*strict=` is refused by text in an unguarded script, and
  `unverified_check.py` is unguarded.
- `tests/test_optin_home.py#test_a_directory_of_that_name_is_not_the_marker`
  (`:318`): the case A1 mirrors one module over.
- Round 3's report, `seal/specs/1790027178-…/rounds/round-3-report.md`
  §*Paste-ready fixes*: the four patches. Findings 1, 3 and 4 are taken as
  written. Finding 2's is departed from in two ways said below.

**Two departures from round 3's paste-ready finding-2 patch, and why.**

1. The patch puts the span pass in `coordinates` only and leaves
   `folded_items` on its two-call form. `docs/` carries the same shape today —
   three lines quoting `<!-- specs/<id> -->` inside backticks — closed on
   their own line, so nothing is misread yet; an author writing `` `<!--` ``
   alone in a `docs/` sentence parks every marker below it. One helper both
   readers name is the whole point of the ticket's *carry it back*.
2. The patch's regex, `` `+[^`]*`+ ``, closes a backtick string at the next
   backtick string of *any* length. Measured over `seal/ledger.md`: it and
   the CommonMark equal-length rule agree on every liveness answer today
   (94/94 markers, 761 not-live lines) and blank 60 lines differently. The
   difference is a double-backtick span holding a single backtick, which the
   loose regex closes early. The equal-length rule is chosen because it is
   the spelled-out rule a reader can check against the specification, and
   the cost is a few more lines than a `re.sub`. Either passes A3 and A4; the
   Alternatives table carries the loose one.

**What breaks in six months, for the chosen approach.** The rule is
single-line: a code span that crosses a line break — legal in CommonMark,
impossible in a table row — with a comment opener inside it is not blanked,
and the opener parks the lines below it until a `-->`. That is the naive
rule's failure on a shape this repository has never carried, and the
docstring says so in one sentence so the next reader meets the limit as a
limit rather than as a surprise. The failure direction is the safe one: fewer
lines read as live, which is a fold record unread and a deletion reported,
never a directory removed with nothing absorbing it.

**Corrected 2026-09-22, round 1's finding 2.** The paragraph above reasons
about a multi-line span holding a comment OPENER, and for that shape every
word of it holds. It is not the only shape: a multi-line span holding a
MARKER is not blanked either, the marker survives and reads as a fold record
although it is a quotation, and `settle --retire` then removes that directory
at exit 0 with nothing having absorbed it. So *the failure direction is the
safe one* is true of the opener and false of the marker, and the sentence as
written covers only half the limit. The door is older than this work — the
base's reader answers the same — and closing it means carrying span state
across lines, which no phase of this plan covers. What this work owes it is
an accurate sentence, and `blank_code_spans`'s docstring carries one: (NAME NOT IN TREE)
measured the same day, six top-level `docs/` documents hold fourteen
multi-line code spans and not one holds a delimiter or a marker, so what
keeps the shape harmless here is that no instance holds one rather than that
the shape does not occur.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Apply `opens_outside_a_comment` to `seal/ledger.md` as `folded_items` does — the obvious closure | Measured at `3cdfd8ad`: three real markers lost (lines 767, 992, 1619) and 787 lines not live, because four anchors quote an unclosed `<!--` inside backticks. Two work items' segments would be wrong on the real ledger | rejected — the ticket's own measurement, reproduced |
| A `settle.py`-local span pre-pass, `folded_items` unchanged | Two readers of one rule again, which is the state round 3 found. `docs/` can carry the shape: three lines quote the opener inside backticks today, closed by luck of the convention, and one `` `<!--` `` in a sentence parks every marker below it and reports a fold as a deletion | rejected — one owner in the shipped reader |
| Teach `comment_scan` itself to skip an opener inside backticks | Changes `strip_comments`'s output for every record reader — `check_text`, `round_record.py`, `chain_check.py`, the review-history guard — where `seal/ledger.md:80` pins the exact output and round 3 measured it unchanged over 1,435 files. A behaviour change to gates that are not this ticket's subject | rejected — the pass sits in front of the scan, for the two readers that want it |
| Compose the span pass into `readable()` | `tests/test_chain_hooks.py#reader_blanking_passes` derives its parametrisation from `readable`'s source and turns red; `HIDDEN_CLOSING_WORD` then wants a third key, and #210's history says a closing word inside a span stops counting — a change to what `is_closed` says at every merge. The T2 row in `seal/ledger.md` records exactly this mutation as the tie's proof | rejected |
| Round 3's regex `` `+[^`]*`+ `` for the span pass | Closes a double-backtick span at the first single backtick inside it. Agrees with the equal-length rule on every liveness answer in today's ledger and blanks 60 lines differently; nothing is lost today, and the rule a reader can check against CommonMark is the other one | not chosen — and **no longer acceptable, corrected 2026-09-22 after round 1's finding 5**: the build planted `test_a_code_span_closes_at_a_backtick_string_of_equal_length`, and applying this regex reddens two of its five shapes. A3 and A4 do hold for both, which is what this cell measured; what it did not foresee is a case pinning the rule itself, so the permission it granted is one the suite now refuses |
| Assert `coordinates(ROOT)` yields 94 sections, as round 3's regression table suggests | 94 grows at every release fold and the case rots into a number somebody bumps; a floor over the repository's own corpus is the shape `skills/settle/SKILL.md` §3 names as the expensive one | rejected — A4 asserts set equality with the fence-only sectioning, non-empty |
| **Three passes in sequence — blank fences, blank code spans, then read the comment state.** The shape this work was built on, and what four review rounds rejected | The middle pass must answer *is this backtick run a code span* without the comment state, and the true answer depends on it: inside a comment markdown is not parsed, so backticks there are literal and a closing delimiter between them really closes the comment. The comment state in turn depends on which delimiters the span pass left standing. Two mutually dependent questions cannot be answered in sequence, so each formulation was a guess with a shape it got wrong, and each shape was found by a review round rather than by a case. **Round 1**: blanking every span took a quoted closing delimiter with it, so a draft the quotation ended stayed open and a section marker below it was lost. **Round 2**: narrowing to spans holding an opener still blanked the span whole, so a span quoting a complete comment lost its closer the same way. **Round 3**: blanking the opener occurrences instead un-parked a draft, because inside a draft the backticks are not a span at all — `settle --retire` removed a directory at exit 0. **Round 4**: stopping at the span's first closing delimiter left the two-span shape, a closer in one span and an opener in a later one, and removed a directory at exit 0 again. Three of the four moved the gate toward deleting | **rejected after round 4**, replaced by one scan carrying fence, comment and code-span state together. What made the replacement available is that the three functions are a closed island — `live_lines` has three call sites, `blank_code_spans` and `opens_outside_a_comment` had one each, inside it — so its internals could be rewritten with `strip_comments`, `comment_scan`, `blank_fences` and `readable` untouched, which is what `seal/ledger.md` and `tests/test_chain_hooks.py#reader_blanking_passes` pin. Verified: every caller derives the same answer over all eleven corpus files (NAME NOT IN TREE) |
| **One scan that decides where a block ends.** The shape round 4 built, and what round 5 rejected | The scan fixed the comment state, which rounds 1 to 4 had guessed at. It then had to answer the one thing left — whether a backtick run with no partner on its own line is a span — and that needs to know where the paragraph ends. Its `is_block_boundary` named three block starts and markdown has more, so a comment opener on the next line was swallowed as quoted text: **executed, a paragraph carrying an unclosed backtick, a draft opener, the closing backtick and a marker read live at this branch's tip and parked at `release/v0.13.0`, and `settle --retire` removed the directory at exit 0.** A guess at a block model fails for the same reason a guess at the comment state did, one level down | **rejected after round 5**, replaced by computing both readings and ANDing them. A wider boundary list would have been the sixth formulation of the same guess (NAME NOT IN TREE) |
| **Reading B unbounded — a span reaches for its partner wherever it falls**, as the re-derivation first stated it | Measured, and it does not survive the corpus: `seal/ledger.md` goes from 761 not-live lines to 1,829 and from 94 markers over 83 ids to 20 over 20, because in a table block every stray backtick finds a partner a few rows later. `settle` would report 20 sections where it reports 83 | **not chosen** — B is bounded by where the paragraph ends, below |
| **Reading B bounded by a blank line alone**, the one paragraph rule CommonMark states unconditionally | Measured: it keeps every marker and every id — 761 → 778 not-live, 94 markers, 83 ids — and still takes three work items from 12, 57 and 29 coordinates to 5, 40 and 19, because a table block carries no blank line and GFM parses a row's cells independently. `segment_of` then groups those three by what is left | **not chosen**, and `test_no_section_of_this_repositorys_ledger_loses_a_coordinate` is the case that would have caught it |
| One phase for all five findings | One warden round judges a refusal-path fix, a test-only change and a reader rule at once, and a finding in one blocks the others' close. The three sit on three different surfaces | rejected — three phases |
| Fix `os.path.exists` alone and leave `home_at(root)` resolving twice | Nothing breaks; the ⬜ stays open on the same twenty lines a phase already opens, and `hooks/optin.py:178-185` documents the parameter with the measurement that created it | rejected — same phase, one case each |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The refusal path agrees with `hooks/optin.py`.** `settle.py#main` resolves the common git directory once and hands it to `home_at(root, common)`; the opt-out arm reads the marker with `os.path.isfile`; the module docstring says the marker is a FILE where it names the opt-out. Findings 1 and 5 | A1 red against the tree (the opt-out sentence prints today), A7 red against the tree (two calls today); then `tests/test_settle_reads_before_it_removes.py` green. Ledger row for `main` and the two cases in this work item's fragment | `60d5505c` |
| 2 | **The single-scan pin pins a single scan.** `test_one_comment_scanner_serves_both_readers` keeps its two behaviour assertions and replaces the two agreement assertions with a module-level stub of `comment_scan` that both readers answer from; its docstring says what it now asks. Finding 4. No shipped file changes | A6 red by mutation — a private copy of the walk inlined into `strip_comments` passes today's case and fails the new one; then `tests/test_unverified_rows_close.py` green. Ledger row anchored on the case | `29368ff2` (NAME NOT IN TREE) |
| 3 | **A line is live by one rule, and every reader asks it.** `blank_code_spans` and `live_lines` in `unverified_check.py`; `folded_items` reads through `live_lines` and the stub in phase 2's case also covers it; `coordinates` reads both loops through `live_lines`, extracting coordinates from the fence-blanked text; the three docstrings and the `FOLD_MARKER` comment say the rule and its single-line limit, and `coordinates` stops attributing the fence rule's second copy to #487. Findings 2 and 3 | A2 red against the tree; A3 and A4 red by mutation (the span pass removed); A5 red by mutation (the fragments loop back to a whole-file `finditer`, round 3's M7); A8 executed at the tip and quoted in `overview.md`; A9 over the four modules named there; A10 read. Ledger rows for the two new units, `coordinates`, `folded_items` and the cases; S1 and S3 re-read in the parent's fragment with a dated note; `changelog.md` written | `7605feb4` (NAME NOT IN TREE) |

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`.

Phase 1 is first because it touches nothing the other two read and lets the
build meet the fixture shapes on the smallest surface. Phase 2 precedes phase
3 on purpose: the pin is the guard the rule change is built under, so the
helper phase 3 adds is asserted to come off the one scan in the same commit
that creates it, rather than a phase later.

**Per phase, what the record has to say (§15, §4).** Which case was red,
against what — the tree at `3cdfd8ad` or a named mutation applied and
restored — and the exit code read directly, `cmd >/dev/null 2>&1; echo $?`.
Run the module you touched and the modules that load the reader; the broad
gate is the sealer's and a prompt cannot widen that (§2, §3).

**What the mutation for A3 and A4 is.** The span pass removed from
`live_lines`, so the comment state is asked of the fence-blanked text alone.
A4 then reports three ids missing from the real ledger's sectioning and A3
reports the marker after the quoted opener unread — the ticket's measurement
as a red case.

What a phase discovers and the next needs goes to
`seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes. Phase 3's record carries
the dry-run line verbatim.

## Operational impact

- **No shipped command changes shape.** No new flag, no exit code moved, no
  printed sentence rewritten. What changes is which of two existing refusals
  a directory-named marker produces, and which lines of `seal/ledger.md` and
  `docs/` two readers treat as live. On this repository both readings are
  identical before and after: `bin/settle` prints `81 work items in 37
  segments, 16 ungrouped, 0 skipped` either way, and `folded_items` returns
  the empty set either way.
- **The hygiene workflow's unverified-record step reads the changed
  `folded_items`.** **Rewritten 2026-09-22 after round 4 replaced the reader's
  structure**; what this bullet said through rounds 2 and 3 argued about the
  failure direction of a stateless pre-pass, and there is no pre-pass left to
  have one. `live_lines` is one scan carrying fence, comment and code-span
  state together, so it is the reading rather than an approximation of it,
  and the expensive-against-cheap trade goes with the guess. What replaces it
  is agreement in the direction that matters:
  `test_the_scan_never_reads_live_what_the_format_parks` holds the scan to a
  reading written from the specification, over generated documents whose
  lines carry several code spans and the block starts a span could be asked
  to reach past. Not full agreement — the scan parks a line wherever its two
  readings differ, and that is deliberate.
  On this repository's own corpus nothing moves — 761 not-live lines, 94
  marker occurrences over 83 unique ids, the three named markers live, and
  every one of the eleven corpus files yielding the same section and marker
  sets as the reader this replaced. What a person sees is unchanged:
  `folded_items` returns the empty set here and `bin/settle` prints the same
  line at exit 0. Prompt budget: zero.
- **A version bump is already owed by the release.** `skills/` ships, and
  the release branch this merges into already carries the move.
- **Fragments, never the shared files.** `CHANGELOG.md` and `seal/ledger.md`
  are not touched. The parent's fragment is touched for two re-reads, which
  `CONTRIBUTING.md` §*House rules* names as the repair for drift-by-edit.
- **`evidence-check --strict` at the sealer.** S1 and S3 in the parent's
  fragment drift by construction when `folded_items` and `coordinates` are
  edited; phase 3 re-reads them, so the sealer meets 0 drifted. A drifted row
  reaching the sealer is a phase-3 omission, not a finding.
- **No migration, no new environment variable, no new dependency, no
  interpreter construct above 3.9 in the unguarded reader.**
