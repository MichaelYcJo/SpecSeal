# Round 5 — the scan judged as code, and the oracle judged as an oracle

<!-- Annotated 2026-09-22, round 5's fix pass. The lines below marked `NAME NOT IN TREE` name units that pass removed: `is_block_boundary` and its lookahead, which decided where a paragraph ended and whose incompleteness removed a work item's directory, and the fuzz oracle and case `a_character_level_reading` and `test_the_scan_agrees_with_a_character_level_reading`, replaced by a reading written from the specification and a case asserting the safety direction rather than full agreement. Every one was in the tree when this record was written and the marker says so rather than rewriting it. NAME NOT IN TREE -->

Target SHA `62f58ea574427af58b4a34bec6c15f744099673d`. Branch
`fix/489-settle-reads-a-marker-inside-a-commented-out-draft`, base
`origin/release/v0.13.0` at `3cdfd8ad`, pull request 490. Read in a
`git clone --no-local` at that SHA; the two affected modules were green there
before anything was touched, 182 passed at exit 0, read with `echo $?` and not
through a pipe.

The cap governs and this is the fifth round. What follows is therefore handed
over rather than commissioned.

## The shape of it

The fifth formulation is a real improvement and it has the same defect as the
four before it, one level down.

`live_lines` no longer guesses at the comment state — the three mutually
dependent passes are gone, and the comment half of the scan agrees with
`comment_scan` on 40,000 generated documents that carry no backticks at all.
What replaced the guess is a **lookahead**: an unmatched backtick run opens a
multi-line code span when an equal-width partner waits before the next *block
boundary*. That lookahead introduced a new dependency — on markdown's block
structure — and `is_block_boundary` models three block starts out of the set (NAME NOT IN TREE)
markdown has.

The one it does not model is the one this module is about. A line beginning
with a comment opener starts an HTML block, so the paragraph above it has
ended and a backtick run in that paragraph cannot reach down to quote it. The
scan lets it reach. The opener is read as text inside a span, the comment
never opens, and the marker on the next line reads live.

So the chain's whole history repeats: a marker inside a commented-out draft
read as a fold record, and `settle --retire` removing a work item's directory
at exit 0 with nothing having absorbed it. Executed on a throwaway git
repository at this SHA.

And the case written to catch exactly this cannot: the oracle's boundary list
is `live_lines`'s own boundary list, so both readings make the same mistake.
Correcting the scan alone turns the fuzz case red — which is the
demonstration, not a side effect.

---

## Findings

### 1 · 🔴 A code span reaches across a line that starts its own block, and the comment opener on that line is swallowed

`skills/verify/scripts/unverified_check.py#is_block_boundary`, and the
lookahead `closes_before_the_block_ends` inside `live_lines` that calls it. (NAME NOT IN TREE)

`is_block_boundary` answers *blank line · table row · fence delimiter*. Five (NAME NOT IN TREE)
other line shapes end a paragraph in CommonMark, and every one of them lets
the lookahead reach past a line it may not reach past. Where that line
carries a comment opener, the opener is read as quoted text, the comment
never opens, and a marker below it reads live.

Executed, five shapes, each one line of prose carrying a stray backtick above
a commented-out draft whose first line also carries one:

| the line between the run and its partner | scan says the marker is | `comment_scan` says the line began |
|---|---|---|
| the draft opener itself | **live** | inside a comment |
| `## A heading` | **live** | inside a comment |
| `- a bullet` | **live** | inside a comment |
| `> quoted` | **live** | inside a comment |
| `---` | **live** | inside a comment |

Two readers in the same file disagree, which is the ground round 4 used for
the finding one level up. The scan is the one that deletes.

End to end on a throwaway git repository at this SHA: `folded_items` returns
`{'1700000042-quoted'}`, `settle --retire` exits 0, prints
`removed seal/specs/1700000042-quoted/`, and the directory is gone. The
control — the same document with no backtick on the draft's first line —
refuses at exit 1 *nothing to retire* and keeps the directory. The heading
shape was run end to end too, with the same exit 0 and the same deletion.

Why the shipped reading is not the defensible one, three ways. CommonMark
decides block structure before inline structure, and an HTML block, a
heading, a list item, a block quote and a thematic break all interrupt a
paragraph — so the span cannot reach in the first place. The module's own
comment reader says the marker line began inside a comment. And where two
readings are arguable, `blank_fences`'s neighbours and `settle.py`'s module
docstring both name the direction this module may not be wrong in, which is
the one that removes a directory.

No instance in the tree today: over `seal/ledger.md`, every `seal/ledger/*.md`
fragment and every top-level `docs/` document — eleven files — the corrected
reading and the shipped one differ on **0 lines**, and the corpus figures are
unchanged at 903 not-live lines, 102 live marker occurrences, 85 unique ids,
and the three named markers live at `seal/ledger.md` lines 767, 992 and 1619.

The fix below is not the boundary list widened in place, and the first
attempt at that was wrong in a way worth recording. `is_block_boundary` is (NAME NOT IN TREE)
asked two different questions — *may a span start on this line* for the start
line, and *has the block above ended* for every line after it. A list item or
a heading ends the paragraph above it and still holds a paragraph of its own,
so refusing a span that STARTS on one reads two real documents in this
repository differently: `docs/worktree-guard-spec.md` and
`docs/release-checklist.md` each wrap a genuine multi-line code span out of a
list item, and four lines changed answer. Applied only to the lines after the
start, the corrected reading leaves all eleven corpus files byte-identical.

The new case was seen red: against the shipped reader it fails on the first
shape, `assert True is False`. With the fix and the oracle corrected, both
modules run 183 passed at exit 0.

### 2 · 🟡 The oracle is not independent in the one respect the case exists to test

`tests/test_unverified_rows_close.py#a_character_level_reading`.

The docstring says it is "written from the format rules rather than from
`live_lines`". In the part that decides finding 1 it is written from
`live_lines`: its `ends_the_block` is that boundary list, name for name — (NAME NOT IN TREE)
blank, table row, fence — and the boundary list is a choice `live_lines`
made, not a rule any format states. Everything downstream of that choice is
shared, so the two readings cannot disagree about it.

Executed. The shipped generator does build finding 1's neighbourhood — a line
beginning with a comment opener directly under a line holding a backtick, in
**10,763 of 40,000** generated documents — and the fuzz reports **0
disagreements** over the same 40,000. The agreement is real and it measures
the span pairing, the precedence rules and the fence rules. It cannot measure
the boundary list, because both sides hold the same copy.

The sharp demonstration is the other direction: correct `is_block_boundary` (NAME NOT IN TREE)
alone and the fuzz case goes red, 1 failed of 182, on documents where the
scan is now right and the oracle is now wrong. A case that reddens when its
subject is corrected is a case pinning the subject's model rather than the
format.

So the round 4 record's reading of this is right about the generator and
wrong about the oracle. The generator was the half two rounds got wrong and
the fix pass fixed it. The oracle is the half still open.

What this does not say: the oracle is worthless. It caught real disagreements
while it was being built, by the fix pass's own account, and its precedence
and pairing halves are genuinely derived. The defect is scoped to the
boundary list.

### 3 · 🟡 `comment_scan`'s stated reason for existing is false, half its output has no reader, and 24 record lines depend on the false sentence

`skills/verify/scripts/unverified_check.py#comment_scan`.

The docstring says "two readers of this file want two different things out of
the same walk", and names the pair. One of that pair was deleted in this
range. `strip_comments` is now the only caller in the repository, and it
discards the first element of every tuple the generator yields — so the
`began` half is computed for nobody and the sentence justifying it names a
unit the tree no longer has as a unit. The case beside it was renamed to say
exactly this, which is how visible the mismatch is.

The part that is not cosmetic: that sentence is the only place outside
`seal/specs/` and `seal/ledger/` where the removed name still appears, so it
is what keeps the name in `evidence-check`'s comparison corpus. Executed —
reword the sentence so it drops the name, and the records arm goes from `0
refused` to **24 NOT-IN-TREE refusals at exit 2**, across both live work
items. The record bookkeeping this branch did is complete only while a stale
docstring stands.

The fix below keeps the name and makes the sentence true, which costs
nothing. Dropping `began` is the larger call and is named in *Decisions left
open* rather than pasted.

A row is anchored on this unit, so the edit drifts it; `evidence-check
--reverify` recomputes the hash.

### ⬜ 4 · The corrected anchor list in `spec.md` omits a row the fragment anchors

`seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`
§*Data & interfaces*.

The line now reads *anchored on `live_lines`, `is_block_boundary`, (NAME NOT IN TREE)
`folded_items`, `coordinates`, `main` and the cases*. The fragment also
anchors a row on `OPENER`, which is a constant and not a case, so the
corrected list is one short. Everything else in it is true: all five named
anchors are in the fragment, and the rest of the fragment's rows are cases.

Under `seal/specs/`, so a correction to the run's paperwork and outside
`Needs a fix`.

### ⬜ 5 · A6's note is invisible in every rendered view of the spec

Same file, the acceptance table.

Keeping A6 as the frame wrote it is the right call — the repository's own
rule is that an item is closed by marking it and never by deleting it, and
the note says plainly what replaced the criterion. What the note does not do
is reach a reader. It is an HTML comment at the end of a table row, so GitHub,
any markdown preview and any rendered copy of the spec show A6 as a live
acceptance criterion with nothing beside it. The one document a sealer checks
the build against reads, when rendered, as though the build owes an
acceptance it cannot satisfy.

The cheap repair is to say it in the cell, where it renders, and leave the
comment carrying only what the checker needs.

Also under `seal/specs/`, so outside `Needs a fix`.

---

## What I confirmed rather than opened

**The marker audit is right, re-derived rather than carried.** Reading the
files `evidence-check`'s records arm actually reads — 18 per live work item,
reports included — the markers on this work item's records silence 11
distinct compound names, and exactly **nine** of them are names the tree
carries: `FOLD_MARKER`, `blank_fences`, `comment_scan`, `folded_items`,
`live_lines`, `opens_outside_a_comment`, `strip_comments`,
`test_strip_comments_reads_through_the_one_comment_scanner` and
`test_the_scan_agrees_with_a_character_level_reading`. Every one is still (NAME NOT IN TREE)
read on at least one unmarked claim line, so nothing lost its check. And the
direction that matters is clean in both work items: **0** names the tree
lacks appear on an unmarked claim line. The count of nine is the fix pass's
and it is correct.

Sampling which of the silenced lines took a marker and which took a
correction: the marked lines I read are past-state narration — a round record
saying what a removed pass did, a phase file describing a build step that has
since been replaced — and marking rather than rewriting is what keeps the
record true at its own `Target SHA`. The two corrected as live claims are the
right two: a present-tense sentence about what the reader does now is not
past-state and a marker on it would preserve a falsehood.

**The comment half of the scan is sound.** Over 40,000 generated documents
carrying comment delimiters, markers, table rows, headings and bullets but no
backticks and no fences — where markdown cannot change the answer —
`live_lines` and `comment_scan` agree on every line of every document: **0
disagreements**. The divergence finding 1 reports is exactly and only the
span's reach.

**The fence half holds on every shape I could build.** A fence opened inside
a comment is not a fence; a comment opened inside a fence is not a comment; a
`~~~` fence is not closed by a ``` one; a four-backtick run is not closed by
three then one; a span opened on the last line of the file, and an unclosed
fence, comment or span at end of file, all end without reaching for anything.
The precedence pair — fence first, then whichever of a comment opener and a
backtick run comes first in the text — holds on each.

**A genuine multi-line span inside a table cell is correctly refused.** GFM
parses cells independently, so a backtick run on a table row has no partner
to reach for, and the scan opens no span there. Sound as shipped.

**The carried ⬜ about stamps is confirmed, not reopened.**
`git merge-base --is-ancestor 281308c7 7f2d6f1c` exits 1 at this SHA, so the
hash `round-2.md` carries beside its own `Target SHA` first existed later. Its
home is `seal/follow-up.md` and not this branch, which is where round 3 sent
it and round 4 confirmed it.

**The blank-line span reset in `live_lines` never fires.** The lookahead
refuses to open a span whose partner sits past a boundary, and a blank line is
one, so a span cannot be open when a blank line arrives. Instrumented and run
over 60,000 generated documents and every `.md` file in the tree: not reached
once. It is a safety net for a state the contract above it already rules out —
and the oracle's equivalent line resets on any boundary rather than on a blank
line, so if it ever did fire the two would disagree. Harmless either way.

**`FENCE_RE` reads a line whose info string carries backticks as a fence
opener, where CommonMark reads a paragraph.** The consequence is that the
lines below are parked, which is the cheap direction — a fold record unread is
a directory kept and a deletion reported at exit 1, which a person sees.
`blank_fences` has read it the same way since before this branch, and moving
one without the other is the shape `live_lines`'s own docstring forbids. Noted
so the next reader does not meet it as a surprise.

---

## Regression tests to plant

`tests/test_unverified_rows_close.py`, beside
`test_the_scan_agrees_with_a_character_level_reading` — the case under (NAME NOT IN TREE)
*Paste-ready fixes*, shown red against the shipped reader before the fix.

`tests/test_settle_reads_before_it_removes.py` wants the end-to-end half that
the unit case does not carry: the same document through `settle --retire` on a
throwaway repository, asserting exit 1 and the directory still present. Round
3's and round 4's equivalents are already in that module and this one belongs
beside them.

## Facts for the evidence ledger

- `live_lines`'s comment state and `comment_scan`'s agree line for line over
  40,000 generated documents carrying no backticks and no fences — measured
  2026-09-22. The claim is that the comment half is not a second guess; what
  it does not cover is the span's reach, which is finding 1.
- Correcting the span's reach leaves all eleven corpus files byte-identical —
  903 not-live lines, 102 live marker occurrences, 85 unique ids — so the
  corpus does not choose between the two readings and cannot be used to.
- The records arm's corpus holds one removed unit's name through a single
  docstring sentence; removing it refuses 24 record lines at exit 2. The claim
  worth anchoring is that the arm's corpus is prose-wide, which
  `tree_names` states and this measures.

---

## Decisions left open

**Whether `comment_scan` keeps its `began` half.** One caller, which discards
it. Dropping it collapses the generator into `strip_comments` and removes the
last trace of the pair; keeping it costs a tuple nobody unpacks and leaves a
second reader cheap to add. Finding 3's paste-ready fix does neither — it
makes the sentence true and leaves the shape alone, because deleting a unit
is what put 24 record lines one docstring away from refusing.

**Whether the boundary list should exist at all.** Finding 1's fix widens it.
The alternative is to stop opening multi-line spans entirely: an unmatched
backtick run is then literal, every comment opener is real, and the failure
direction is parking lines rather than deleting a directory. It would remove
the lookahead, the boundary list and this whole class in one edit. I did not
measure what it costs the corpus, and the fix below is the one I verified.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 The span lookahead is bounded by three block starts and markdown has more, so a comment opener at the start of the next line is swallowed as quoted text — a marker inside a parked draft reads live and `settle --retire` removes the work item's directory at exit 0 | `skills/verify/scripts/unverified_check.py#is_block_boundary` | open | Executed at this SHA. Five interrupting shapes — the draft opener itself, an ATX heading, a list item, a block quote, a thematic break — each read the marker live where the module's own `comment_scan` answers *began inside*. End to end on a throwaway git repository: `folded_items` returns the quoted id, `settle --retire` exits 0 and prints `removed seal/specs/1700000042-quoted/` with the directory deleted; the backtick-free control refuses at exit 1 and keeps it; the heading shape deletes too. Corpus unmoved and no instance today — 0 lines of eleven files differ, 903 not-live, 102 marker occurrences, 85 ids, the three named markers live at 767, 992 and 1619. The paste-ready fix applies the wider set only to lines AFTER the start line, because a list item ends the paragraph above it and still holds one of its own; applied to the start line it reads `docs/worktree-guard-spec.md` and `docs/release-checklist.md` differently on four lines. With it and the oracle corrected, both modules run 183 passed exit 0, and the new case is red against the shipped reader |
| 2 | 🟡 The character-level oracle is not independent where it counts: its `ends_the_block` is `live_lines`'s own boundary list, so the fuzz cannot report finding 1's class and goes red when the scan is corrected | `tests/test_unverified_rows_close.py#a_character_level_reading` | open | Executed. The shipped generator builds finding 1's neighbourhood in 10,763 of 40,000 documents and the fuzz reports 0 disagreements over the same 40,000 — the agreement is real for pairing, precedence and fences, and vacuous for the boundary list. Correcting `is_block_boundary` alone reddens this case and nothing else, 1 failed of 182, on documents where the scan is now right. The round 4 record's reading is right about the generator and open about the oracle (NAME NOT IN TREE) |
| 3 | 🟡 `comment_scan`'s docstring justifies the generator by a pair that no longer exists, `began` has no reader, and that false sentence is the only thing keeping a removed unit's name in `evidence-check`'s corpus | `skills/verify/scripts/unverified_check.py#comment_scan` | open | Read and executed. `strip_comments` is the only caller in the repository and discards the first element of every tuple; the case beside it was renamed to say the pair is gone. Reword the sentence so it drops the name and the records arm goes from `0 refused` to 24 NOT-IN-TREE refusals at exit 2 across both live work items. The paste-ready fix keeps the name and makes the sentence true; a row is anchored on the unit, so the edit drifts it and `evidence-check --reverify` recomputes |
| ⬜ 4 | The corrected anchor list names five anchors and the fragment carries six — the row anchored on `OPENER` is a constant, not a case | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` §*Data & interfaces* | open | Read against the fragment's anchor column. All five named anchors are there and every remaining row is a case except the one on `OPENER`. The correction itself was the right call — the old list named a unit this range removed, and a present-tense claim that has gone false is corrected rather than marked. Under `seal/specs/`, so outside `Needs a fix` |
| ⬜ 5 | A6's note is an HTML comment at the end of a table row, so every rendered view shows a live acceptance criterion with nothing beside it | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`, the acceptance table | open | Read. Keeping the row as the frame wrote it is right and matches the repository's own rule about marking rather than deleting; what the note does not do is reach a reader of the rendered spec, which is the document a sealer checks the build against. Saying it in the cell renders; the comment then carries only what the checker needs. Under `seal/specs/`, so outside `Needs a fix` |
| ⬜ | The blank-line span reset in `live_lines` is unreachable, and the oracle's equivalent resets on a different condition | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Instrumented and executed over 60,000 generated documents and every `.md` file in the tree: never reached. The lookahead refuses a span whose partner sits past a boundary and a blank line is one, so the state it guards cannot arise. Harmless; named so the next reader does not take it for a live rule |
| ⬜ | `FENCE_RE` reads a line whose info string carries backticks as a fence opener where CommonMark reads a paragraph | `skills/verify/scripts/unverified_check.py` | confirmed | Read. The consequence is that lines below are parked — a fold record unread, a directory kept, a deletion reported at exit 1, which a person sees. `blank_fences` has read it this way since before this branch and `live_lines`'s docstring forbids moving one without the other |
| ⬜ | A stamp on a round report is tracked as a live claim, so a record states a value that did not exist at its own `Target SHA` | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-2.md` | confirmed | Confirmed as asked rather than reopened. Executed at this SHA: `git merge-base --is-ancestor 281308c7 7f2d6f1c` exits 1. Its home is `seal/follow-up.md` and not this branch |
| 🟢 confirmation | The marker audit is right — nine silenced names are in the tree, every one still covered, and no record line claims a removed unit without a marker | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/` | confirmed | Re-derived rather than carried, over the 18 files per work item the records arm actually reads. Markers silence 11 distinct compound names here and exactly nine are names the tree carries; each is still read on at least one unmarked claim line, the smallest cover being one. Zero names the tree lacks appear on an unmarked claim line, in either live work item |
| 🟢 confirmation | The comment half of the scan is not a second guess — it agrees with `comment_scan` wherever markdown cannot change the answer | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Executed: 40,000 generated documents carrying comment delimiters, markers, table rows, headings and bullets and no backticks or fences — 0 documents where the two readings differ on any line |
| 🟢 confirmation | The fence half and the precedence pair hold on every shape I could build | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Executed, ten shapes: a fence opened inside a comment, a comment opened inside a fence, a `~~~` fence not closed by a ``` one, four backticks not closed by three then one, a run at the start of a line decided as a fence, a span opened on the last line, and an unclosed fence, comment or span at end of file. Each answers the way the docstring's table says |
| 🟢 confirmation | A multi-line span inside a table cell is correctly refused | `skills/verify/scripts/unverified_check.py#is_block_boundary` | confirmed | Read and executed. GFM parses a row's cells independently, so a backtick run on a table row reaches for nothing, and the start-line arm of the boundary test is what enforces it. This is the one question the start-line arm is right about |
| 🟢 confirmation | The `settle.py` half of the range is docstring only, and the docstring is true | `skills/settle/scripts/settle.py#coordinates` | confirmed | Read the whole diff for that file across the range: 26 lines, all prose. It names one scan carrying three states, which is what the code does, and hands the reasoning to `live_lines`'s own docstring rather than keeping a second copy |
| 🟢 confirmation | Both modules are green at this SHA before anything is touched | the two affected modules | confirmed | Executed in a clone at the target SHA: 182 passed, exit 0, read with `echo $?` and not through a pipe |
| ❓ out of verified scope | Whether the repository's full suite, the repository-wide lint and the typecheck pass at this SHA | the repository | not run | §2 gives the broad gate to the sealer and this definition hands me none of the three. The orchestrator reports five modules at 397 passed exit 0, `evidence_check.py --strict .` at exit 0 with 0 refused, 0 drifted and 0 broken, and `survivor-check` at exit 0, all at this SHA; this round did not re-run them and does not certify them. The caller answers it |

## Executed probes

| What was run | Result |
|---|---|
| the two affected modules in a pristine clone at the target SHA | 182 passed, exit 0, read with `echo $?` and not through a pipe |
| ten adversarial shapes through the scan — fences inside comments, comments inside fences, mixed fence characters, unequal backtick runs, spans at end of file, a span in a table cell | nine answer as the docstring's table says; the tenth is finding 1 |
| five paragraph-interrupting shapes through the scan, each against `comment_scan` | the marker reads live in all five where `comment_scan` answers *began inside* |
| finding 1's document through `folded_items` and `settle --retire` on a throwaway git repository | `{'1700000042-quoted'}`, exit 0, `removed seal/specs/1700000042-quoted/`, directory deleted |
| the backtick-free control and, separately, the heading shape, through the same command | control exits 1 *nothing to retire* and keeps the directory; the heading shape exits 0 and deletes |
| the shipped fuzz generator, asked how often it builds finding 1's neighbourhood | 10,763 of 40,000 documents |
| the scan against the shipped oracle over 40,000 documents of that generator | 0 disagreements |
| `is_block_boundary` corrected, the oracle left alone, against the two modules | 1 failed of 182 — the fuzz case alone (NAME NOT IN TREE) |
| both corrected, against the two modules, with the new case added | 183 passed, exit 0 |
| the corrected reading against the shipped one over eleven corpus files | 0 lines differ; 903 not-live, 102 live marker occurrences, 85 unique ids, the three named markers live at `seal/ledger.md` 767, 992 and 1619 |
| the first, wider correction — the boundary applied to the start line too — over the same corpus | 4 lines differ in `docs/worktree-guard-spec.md` and `docs/release-checklist.md`, each a genuine wrapped span in a list item; this is why the shipped fix bounds only the lines after the start |
| the new case against the shipped reader | red, `assert True is False` on the first shape |
| `live_lines` against `comment_scan` over 40,000 documents with no backticks and no fences | 0 documents differ on any line |
| the blank-line span reset, instrumented, over 60,000 generated documents and every `.md` file in the tree | never reached |
| the marker audit re-derived over the files the records arm reads | 11 names silenced here, 9 of them in the tree, every one covered elsewhere, 0 uncovered; the other live work item: 10 silenced, 7 in the tree, 4 uncovered and correctly so |
| the removed unit's name dropped from the one docstring that still carries it, then `evidence-check --strict .` | exit 2, 24 NOT-IN-TREE refusals across both live work items, against `0 refused` before |
| `evidence-check --strict .` in the pristine clone | exit 0, `0 refused · 0 drifted · 0 external` in the records arm |
| `git merge-base --is-ancestor 281308c7 7f2d6f1c` | exit 1 — the round 2 record's stamp postdates its own `Target SHA` |
| the broad gate — the repository's full suite, the repository-wide lint, the typecheck | **not yet** — not run by this round and not this round's to run. The sealer takes it |

## Paste-ready fixes

Finding 1, the constant. Goes below `FENCE_RE`:

```python
# A line that starts a leaf block of its own. The paragraph above it has
# ended, so a backtick run in that paragraph cannot reach past it for a
# partner. `is_block_boundary` answers a DIFFERENT question — may a span
# start on this line — and the two are kept apart because a list item or a
# heading ends the paragraph above it and still holds a paragraph of its own:
# refusing a span that starts on one reads `docs/worktree-guard-spec.md` and
# `docs/release-checklist.md` differently, four lines, each a genuine wrapped
# span inside a bullet.
#
# The first alternative is the one that costs a directory. A line beginning
# `<!` opens an HTML block, so the comment opener on it is a real opener and
# not text quoted by a span reaching down from the line above. Read as
# quoted, the comment never opens and the marker below it reads live —
# `settle --retire` removing a work item's directory at exit 0 with nothing
# having absorbed it (round 5, finding 1; executed on a throwaway git
# repository, five interrupting shapes, every one of them deleting).
INTERRUPTS = re.compile(
    r"^ {0,3}(#{1,6}([ \t]|$)|>|[-*+][ \t]|\d{1,9}[.)][ \t]|<[!?]"
    r"|([-*_])[ \t]*(\3[ \t]*){2,}$)"
)
```

Finding 1, the lookahead. Inside `closes_before_the_block_ends`: (NAME NOT IN TREE)

```python
        if is_block_boundary(lines[start_line]):
            return False
        for i in range(start_line, len(lines)):
            if i > start_line and (
                is_block_boundary(lines[i]) or INTERRUPTS.match(lines[i])
            ):
                return False
```

Finding 1, the case. In `tests/test_unverified_rows_close.py`:

```python
def test_a_span_may_not_reach_across_a_line_that_starts_its_own_block():
    """Round 5's finding. The lookahead bounded a span by three block
    starts — blank line, table row, fence — and markdown has more. A line
    beginning a comment, a heading, a list item, a block quote or a thematic
    break ends the paragraph above it, so a backtick run in that paragraph
    cannot reach past it for a partner. Where it did, the comment opener on
    that line was read as quoted text, the comment never opened, and a marker
    inside the commented-out draft read live — `settle --retire` removing the
    work item's directory at exit 0 with nothing having absorbed it.
    """
    opener, closer = "<!" + "--", "--" + ">"
    marker = f"{opener} specs/1700000042-quoted {closer}"
    draft = f"{opener} a draft with `code` in it"
    for interrupter in (None, "## A heading", "- a bullet", "> quoted", "---"):
        lines = ["prose with a stray ` backtick"]
        if interrupter is not None:
            lines.append(interrupter)
        lines += [draft, marker, "more prose"]
        live = [flag for _, flag in uc.live_lines(lines)]
        assert live[lines.index(marker)] is False, (interrupter, live)
```

Finding 2, the oracle. Replaces `partner_on_a_later_line`'s boundary test and (NAME NOT IN TREE)
adds the helper beside it — written character by character because that module
imports no regex module on purpose:

```python
    def interrupts_a_paragraph(line):
        """A line that starts a leaf block of its own. The paragraph above it
        has ended, so an inline span cannot reach past it — which is what a
        comment opener at the start of the next line relies on. Derived from
        the block rules, NOT from the reader this oracle judges: the boundary
        list was the one part of this reading copied from `live_lines`, and
        while it was, this case agreed with the scan on the shape that
        removed a directory (round 5, finding 2).
        """
        if len(line) - len(line.lstrip(" ")) > 3:
            return False
        s = line.lstrip(" ")
        if not s:
            return False
        if s[0] == ">" or s[:2] in ("<!", "<?"):
            return True
        if s[0] == "#":
            n = len(s) - len(s.lstrip("#"))
            return 1 <= n <= 6 and (len(s) == n or s[n] in " \t")
        bare = s.replace(" ", "").replace("\t", "")
        if s[0] in "-*_" and len(set(bare)) == 1 and len(bare) >= 3:
            return True
        if s[0] in "-*+":
            return len(s) > 1 and s[1] in " \t"
        digits = len(s) - len(s.lstrip("0123456789"))
        return (
            1 <= digits <= 9
            and len(s) > digits + 1
            and s[digits] in ".)"
            and s[digits + 1] in " \t"
        )

    def partner_on_a_later_line(start_line, width):
        """Whether an equal-width run waits on a LATER line of the block."""
        if ends_the_block(lines[start_line]):
            return False
        for k in range(start_line + 1, len(lines)):
            if ends_the_block(lines[k]) or interrupts_a_paragraph(lines[k]):
                return False
```

Finding 3, the docstring. Replaces the second paragraph of `comment_scan`:

```python
    One scanner, because a second copy of the walk is what `check_text`'s
    docstring spent three review rounds undoing. `strip_comments` wants the
    text and is the only caller left: `opens_outside_a_comment`, which wanted
    the state the line STARTED in, went with the three-pass composition
    `live_lines` replaced, and `live_lines` carries that state itself now. The
    pair is why this yields both halves and the first half currently reaches
    nobody — the name above is kept deliberately, because it is the only
    mention outside the records, and dropping it refuses 24 record lines at
    exit 2 (round 5, finding 3).

    Why the state cannot be read off the text: a fold marker IS a comment, so
    a genuine one and one sitting inside a commented-out draft both come back
    with nothing kept.
```

Needs a fix: yes — finding 1, the span lookahead's boundary list, which reads a marker inside a commented-out draft as live and removes a work item's directory at exit 0; and finding 2, the oracle, whose boundary list is the scan's own, so the case written for this class cannot report it.
Loses a record or crashes: yes — finding 1, a work item's whole SDD set removed at exit 0 with nothing having absorbed it, executed on a throwaway git repository at the target SHA.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A stamp on a round report is tracked as a live claim, so a coordinate is rewritten across five files and a record can state a value that did not exist at its own `Target SHA` | `seal/follow-up.md`, not this branch — already deferred in round 3 and confirmed in round 4 | the orchestrator |

---

## Proof block

Files opened at `62f58ea574427af58b4a34bec6c15f744099673d`:

- `skills/verify/scripts/unverified_check.py` — the module docstring, the
  constants, `comment_scan`, `strip_comments`, `blank_fences`,
  `is_block_boundary`, `live_lines` in full, `folded_items`, `check_records`, (NAME NOT IN TREE)
  `tree_names`, `compound`, `claim_lines`, and the records arm in `main`
- `skills/settle/scripts/settle.py` — the module docstring and `coordinates`,
  and the whole of this range's diff to it
- `tests/test_unverified_rows_close.py` — `a_character_level_reading`, (NAME NOT IN TREE)
  `documents_with_several_spans_on_a_line`,
  `test_the_scan_agrees_with_a_character_level_reading`, (NAME NOT IN TREE)
  `test_the_first_delimiter_on_the_line_wins`,
  `test_strip_comments_reads_through_the_one_comment_scanner`,
  `test_readable_would_erase_every_fold_record`
- `tests/test_a_record_states_what_the_tree_has.py` — the module docstring and
  its fixtures
- `bin/test` — the runner's header
- `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-4.md`
  in full
- `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`
  — the acceptance table and §*Data & interfaces*, through the range's diff
- `seal/ledger/1790039346-settle-reads-a-marker-inside-a-commented-out-draft.md`
  — the anchor column
- `seal/ledger/1790027178-a-shipped-spec-waits-for-a-settle-that-was-never-built.md`
  — the S1 row
- `seal/ledger.md`, every `seal/ledger/*.md` and every top-level `docs/`
  document — read as a corpus by the probes rather than line by line

Not opened: the other 97 work items' records, the rest of the test suite, and
everything the broad gate would touch.
