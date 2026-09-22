# 1790039346-settle-reads-a-marker-inside-a-commented-out-draft — round 6 report

Target SHA `1eb0ef0767a49b8d7ca0942b6178226f0334788e`, the tip of
`fix/489-settle-reads-a-marker-inside-a-commented-out-draft`, base
`origin/release/v0.13.0` at `3cdfd8ad`, draft pull request 490. Fix range
`2aade426c39c27b6be7689183432052ec18d12b3..16a56bc871edff394f430dc8caa37670e1639007`,
three commits. Reviewed in a `git clone --no-local` at that SHA; nothing was
written in the working tree but this file.

## What this round was asked, and what it opened

The verifying round. Round 5's record reads `Fixes checked by: nobody`, and
closing that is the job — judge the two-reading rule as code, judge the
surviving boundary list, read the rewritten oracle as an independent
implementation, enumerate the eight new units against the mutations that
should redden them, and re-derive the corpus figures and the marker audit.

It opened five things. One of them removes a work item's directory at exit 0,
and it is round 1's class reached through a door no round has looked at: not
the span rule, not the block rule, but what the scan calls a fence.

**The design the fix pass landed is sound.** Computing both readings and
parking on disagreement does end the class the five rounds were circling: I
could not break the AND from the span side, and the mutation set below shows
every part of it is load-bearing and pinned. What is broken is one character
class in the regular expression the scan asks first, and the case family
written to catch exactly this cannot see it.

## The findings, in causal order

### 1. A fence delimiter indented four spaces is read as a delimiter, and one of them deletes a work item's directory

`skills/verify/scripts/unverified_check.py:110` — `FENCE_RE`.

```python
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
```

CommonMark 4.5: *the opening code fence may be indented up to three spaces*.
Four or more spaces is an indented code block, or, inside an open paragraph, a
lazy continuation line. `^\s*` accepts any indentation, so `_liveness` opens
and closes a fenced block on a line that is not a fence delimiter at all.

The consequence is not that some lines are parked. It is that **one
unbalanced phantom delimiter inverts the fence state for the rest of the
file**: every real delimiter after it toggles the wrong way, so the *content*
of a real fenced block reads live and its delimiters read as content. A fold
marker quoted inside a fenced example is then a fold record.

That quotation is the documented shape, not an invented one. The module's own
constant comment at `skills/verify/scripts/unverified_check.py:78-86` says
`skills/settle/SKILL.md` §2 shows the marker inside a fenced block with a real
released work item id, and that a session copying that example into the policy
it is writing hands `settle --retire` a real directory to delete. The only
extra ingredient is one four-space-indented fence delimiter anywhere above it
in the same top-level `docs/` file.

Executed at this SHA, on a throwaway git repository built by the probe:

~~~~
docs/policy.md
--------------
A fence opens with

    ```python

and closes with a run at least as long.

```markdown
<!-- specs/1700000042-quoted -->
```
~~~~

`folded_items` returns `{'1700000042-quoted'}`. `settle --retire` exits 0,
prints `removed seal/specs/1700000042-quoted/`, and the directory is gone.
That is round 1's outcome, round 2's outcome and round 5's outcome, for the
fourth distinct cause.

A second shape reaches the same place without any real fence — a phantom
opener, a draft opener, a phantom closer, a marker:

| line | reader | CommonMark |
|---|---|---|
| `    ``` ` | fence opens | indented code block (4.5) |
| a comment opener | inside a fence, not read | HTML block type 2 opens (4.6) |
| ` ``` ` | fence closes | comment content |
| `<!-- specs/1700000042-quoted -->` | **live** | the line that closes the comment — parked |

`comment_scan`, the module's own reader, answers *began inside* for that last
line. `live_lines` answers live.

**No instance in the tree today.** No top-level `docs/` file carries a
four-space-indented fence delimiter, and bounding the pattern moves zero lines
in every `.md` file in the repository — measured below. So this is a class
with no instance, which is exactly the state round 1's class was in before a
session copied the skill's example.

### 2. The oracle is still the reader's own rule, and it goes red when the reader is corrected

`tests/test_unverified_rows_close.py:1599` — `block_ends_at`, and
`tests/test_unverified_rows_close.py:1641` — `fence_of`, inside
`a_reading_from_the_commonmark_rules`.

Round 5's finding 2 was that the oracle's block rule was `live_lines`'s own,
so the fuzz could not report finding 1's class and would go red when the scan
was corrected. The fix pass rewrote the oracle and its docstring states:

> Nothing here is named after, or copied from, a choice `live_lines` made […]
> This list is richer than the reader's on purpose: the reader may park a line
> this reading calls live, and may never do the reverse.

Both halves are false, and the second is false in the direction that matters.

- `block_ends_at` and `_paragraph_ends_at` disagree on **0** of 40,000
  generated lines built from every shape the two rules test for, and on **0**
  lines of every `.md` file in the repository. The ordered-list clause is
  identical source text in both functions.
- `fence_of` strips the line before measuring, so like `FENCE_RE` it accepts
  any indentation. That is the one rule finding 1 turns on.

So on both of finding 1's documents the oracle returns the scan's verdicts
line for line and `test_the_scan_never_reads_live_what_the_format_parks`
reports zero unsafe lines — on a document that deletes a directory.

And the trap round 5 named is still armed. With `FENCE_RE` bounded to three
spaces — the fix for finding 1, and nothing else changed — the shipped oracle
reports the **corrected** reader as unsafe on 1 line of the first document and
6 lines of the second. Fixing finding 1 alone turns this case red. The two are
one fix.

A corrected oracle does report finding 1: line 4 of the first document, lines
7 and 8 of the second, against the shipped reader; zero against the bounded
one. That is §15 satisfied — the case is seen red before it is planted.

The generator cannot reach the shape either.
`documents_with_several_spans_on_a_line`'s token list carries `` ``` `` and a
single space but nothing that produces four columns of indentation, so the
fuzz over 2,000 documents reports 0 unsafe for all four combinations of
reader and oracle. The shape has to arrive as a parametrized row, or the
generator needs an indentation token.

### 3. The docstring keeps the justification the fix pass says its own fuzz disproved

`skills/verify/scripts/unverified_check.py:310` — `_paragraph_ends_at`.

> **Being incomplete here is safe, and that is the whole difference from the
> rule round 5 removed.** […] A stop that is missing lets `_partner_ahead`
> reach further, which makes the crossing reading believe in a span the format
> would not, which parks a line.

The fix pass reported to the orchestrator that this reasoning is wrong and
that its own fuzz disproved it — reaching further changes which runs pair with
which, and consuming a partner early can make a later line live. The
correction went into the ledger. It did not go into the sentence the next
editor reads, and that sentence is stated without qualification.

Reproduced, executed at this SHA:

| document | shipped rule | with the missing setext stop added | CommonMark |
|---|---|---|---|
| ``["text `", "===", "text `", "plain prose", "text `"]`` | lines 3 and 4 **live** | lines 3 and 4 parked | lines 3 and 4 parked |

`===` under a paragraph line is a setext heading underline (CommonMark 4.3)
and ends the paragraph. The shipped rule misses it, so the run on line 0
consumes the partner the run on line 2 needed, and two lines the format parks
read live. Incompleteness moved the answer toward live, which is the direction
that removes a directory.

The rule this repository applies to itself is §14 — a fix that changes what a
person sees documents it. Here what a person reads is the version the fix pass
already knows is false.

### 4. The block rule stops where markdown does not, and that is the unsafe direction

`skills/verify/scripts/unverified_check.py:325-340` — `_paragraph_ends_at`.

Finding 3 is about a missing stop. This is the other direction, which the
docstring does not name at all: a stop the rule has and markdown does not.
An over-stop shortens `_partner_ahead`'s reach, so the crossing reading misses
a span the format has, and the AND goes live.

| line | the rule says | CommonMark |
|---|---|---|
| `3. an item` | the block ends | an ordered list interrupts a paragraph only when it starts with 1 (5.3) — paragraph text |
| `#hello` | the block ends | a heading needs a space or end of line after the hashes (4.2) — paragraph text |
| `####### seven` | the block ends | seven hashes is not a heading (4.2) — paragraph text |
| `12345678901. x` | the block ends | at most nine digits (5.2) — paragraph text |
| `    ``` ` | the block ends | finding 1 |

The first two are not hypothetical here. Over every `.md` file in the
repository, the shipped rule and a corrected one disagree on **944 lines**,
and the overwhelming majority are prose lines beginning with an issue
reference — `#341, #353).**`, `#424's work item are corrected […]`. This
repository writes that line shape constantly.

What the correction costs is small and measured: liveness changes on **6
lines across 4 files**, every one of them under `seal/specs/`, and none in
`docs/` or in `seal/ledger.md` or `seal/ledger/`. Nothing reads those files
through `live_lines`.

The `|` stop stays. It is a deliberate over-stop with a measurement behind it
— the docstring's own account of the three work items that lose coordinates
without it — and removing it moves the corpus.

### 5. The corpus case collapses 94 marker occurrences into 83 keys, last one wins

`tests/test_unverified_rows_close.py:1824` —
`test_the_three_named_markers_are_live_in_this_repositorys_ledger`.

```python
    live = {
        line.strip(): state
        for line, state in uc.live_lines(lines)
        ...
    }
```

(the filter clause is elided so this quotation carries no unclosed comment
opener; it selects the lines beginning with the marker's opener)

`seal/ledger.md` carries 94 live marker occurrences on 83 distinct marker
lines: **11 marker lines appear twice**, at 1215/1218, 1259/1262, 1333/1336,
1370/1373, 1398/1401, 1434/1437, 1526/1529, 1590/1593, 1629/1632, 1777/1780
and 1797/1800. The dictionary keeps the last state of each, so a regression
that parks the first of a pair is invisible to the case, and `len(live) >= 80`
is a floor on keys rather than on occurrences.

The docstring calls this *the corpus floor*. A floor that eleven occurrences
can slip under is one the next formulation will be measured against and pass.

## Corrections under `seal/specs/`, outside `Needs a fix`

- **`spec.md` G3 now grounds the gate change on finding 2's false claim.** The
  line was corrected in `16a56bc8` to name
  `test_the_scan_never_reads_live_what_the_format_parks` and to say it *holds
  it against a reading derived from the format rather than from the scan*. The
  case is the right one to name; the ground is not true of the reading in the
  tree.
- **`spec.md` A6's note contradicts G3 four rows above it.** The note says
  *the acceptance that stands in its place is the agreement with an
  independently written character-level reading*. G3 now says agreement would
  forbid the design and the case asserts the safety direction instead. One of
  the two sentences has to go.
- **`overview.md` §*Not verified* row 2 names a watcher that cannot watch.**
  The row is otherwise the best thing in the fix pass's paperwork: it names
  the exact risk — *that `_paragraph_ends_at` names enough of markdown's block
  starts for the crossing reading to pair the way the format does* — and then
  closes with *and the safety fuzz is what now watches it*. Finding 2 is that
  it does not.
- **`overview.md` §*Not verified* row 3 is stale.** It says the records arm
  exits 2 on two shorthand coordinates at `spec.md:30`. Executed at this SHA:
  `bin/evidence-check --strict .` exits 0, `510 names read · 0 refused · 0
  drifted · 0 external`, ledgers `1439 ok · 0 drifted · 0 broken`. Line 30 of
  `spec.md` today is the dry-run row. A §*Not verified* row describing a
  failure that no longer exists sends the sealer to repair a repair.

## What I confirmed rather than re-litigated

- **Round 5's ⬜ 4 — the anchor list — is fixed.** `spec.md` §*Data &
  interfaces* now names `live_lines`, `folded_items`, `coordinates`, `main`,
  `OPENER`, the three helpers and the cases; the fragment carries exactly
  `_liveness`, `_paragraph_ends_at`, `_partner_ahead`, `live_lines`,
  `folded_items`, `coordinates`, `main` twice, `OPENER` and 15 cases. Read
  against the fragment's anchor column.
- **Round 5's ⬜ 5 — A6 — is fixed.** The row's first cell now carries
  **RETIRED** in the rendered table, which is what the finding asked for. The
  note's stale half is recorded above as a separate correction.
- **The corpus figures, re-derived independently.** `seal/ledger.md` at this
  SHA: 2,430 lines, **761 not-live**, **94 live marker occurrences**, **83
  unique ids**, and the three named markers live at 767, 992 and 1619. The fix
  pass's attribution of the discrepancy is right: the eleven-file corpus —
  eight `docs/*.md`, `seal/ledger.md` and two `seal/ledger/*.md` fragments —
  gives **903** not-live, which is round 5's 903 with the wrong label. Round
  5's 102 / 85 reproduces on neither set: the eleven files give 94 / 83, the
  same as the ledger alone, because every marker in the corpus lives in the
  ledger.
- **The marker audit, re-derived rather than carried.** Over both live work
  items and every `.md` file `record_files` reads: **no compound name the tree
  lacks appears on an unmarked claim line**, in either. For this work item, 17
  distinct compound names are silenced by a marker, 9 of them are names the
  tree carries and 8 are not — the 8 being the units this range removed. One
  in-tree silenced name, `check_records`, is read on no unmarked claim line in
  this work item; that is marker noise rather than a hole, since the gate's
  refusal direction is the absent name and there are none. `bin/evidence-check
  --strict .` at exit 0 agrees.
- **Every one of the eight new units has a mutation that reddens it**, derived
  independently rather than taken from the fix pass's count. Each row below
  was executed against both affected modules in the clone; baseline 191
  passed, exit 0.

| mutation | what goes red |
|---|---|
| `_liveness`: drop the literal reading | `test_every_shape_five_review_rounds_named[a span reaching past a draft opener]` |
| `_liveness`: drop the crossing reading | `test_the_scan_never_reads_live_what_the_format_parks`, `test_every_shape_five_review_rounds_named[a marker inside a multi-line code span]` |
| `_paragraph_ends_at`: never stop | the fuzz, `test_the_three_named_markers_are_live_in_this_repositorys_ledger`, `test_the_rule_over_this_repositorys_ledger_loses_no_section`, `test_no_section_of_this_repositorys_ledger_loses_a_coordinate` |
| `_paragraph_ends_at`: drop the table-row stop | the fuzz, two parked-draft cases, `test_no_section_of_this_repositorys_ledger_loses_a_coordinate` |
| `_partner_ahead`: always answer yes | 9 cases across both modules |
| `_partner_ahead`: ignore run width | the fuzz alone |

  The last row is the thin one: the width rule in `_partner_ahead` has exactly
  one guard, and it is the case finding 2 says cannot report finding 1's
  class. Recorded as ⬜ rather than as a finding, because the guard does hold
  for that mutation.
- **The AND holds from the span side.** I could not break it on a run whose
  partner is the first run of the next paragraph, three runs on one line, a
  run inside a fence reaching across it, a line that is a single backtick, a
  run opened on the file's last line, or a marker on the same line as an
  unclosed run. The reason is structural and worth writing down: a fold marker
  line begins with a comment opener at column 0, which in CommonMark always
  begins an HTML block (4.6, condition 2) and so always ends the paragraph
  above it. A marker line can therefore never sit inside a multi-line code
  span, and the span reading's errors on it are all in the parking direction.
  The deletion door is the fence state, which is finding 1.

## Which of the fix pass's claims rest on its own execution alone

The charge was to say this, because `overview.md` §*Not verified* is supposed
to carry exactly it and this is the last round.

- **It carries the general statement well** and names the specific risk
  correctly. What it gets wrong is the watcher, recorded above.
- **Claims now confirmed by a second party** — this round: the corpus figures
  and the 903 attribution; the marker audit; the mutation coverage of the
  eight new units; `evidence-check` at exit 0. The orchestrator separately
  confirmed the seven shapes and the three named markers.
- **Claims that still rest on the fix pass's own execution** — the docstring's
  measurement that bounding the crossing reading by a blank line alone keeps
  94 markers and 83 ids while parking 17 further lines and costing three work
  items their coordinates; the claim that the table-row stop makes every
  section match the previous reader *coordinate for coordinate*; the fuzz
  counts in round 5's record (10,763 of 40,000, 0 disagreements). None is load
  bearing for a verdict here, and the mutation row for the table-row stop
  gives the second one independent support.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 `FENCE_RE` accepts any indentation, so a four-space-indented delimiter opens a phantom fence, inverts the fence state for the rest of the file, and a marker quoted inside a real fenced example reads live — `settle --retire` removes the work item's directory at exit 0 | `skills/verify/scripts/unverified_check.py#FENCE_RE` | open | Executed at this SHA. CommonMark 4.5 bounds the indent to three spaces. Two shapes: a real fenced example after one phantom opener, and a phantom pair straddling a draft opener. End to end on a throwaway git repository — `folded_items` returns `{'1700000042-quoted'}`, `settle --retire` exits 0, prints `removed seal/specs/1700000042-quoted/`, directory gone. `comment_scan` answers *began inside* on the second shape's marker line. No instance in the tree: no top-level `docs/` file carries an indented delimiter, and the fix moves 0 lines in every `.md` file in the repository, with both modules at 191 passed exit 0 |
| 2 | 🟡 The oracle's block rule and fence rule are the reader's own, so the fuzz cannot report finding 1's class and goes red when the reader is corrected — round 5's finding 2, not closed | `tests/test_unverified_rows_close.py#a_reading_from_the_commonmark_rules` | open | Executed. `block_ends_at` and `_paragraph_ends_at` disagree on 0 of 40,000 generated lines and 0 lines of every `.md` in the tree; the ordered-list clause is identical source text; `fence_of` strips the line, so it accepts any indentation exactly as `FENCE_RE` does. On both of finding 1's documents the oracle returns the scan's verdicts line for line and the case reports 0 unsafe. With `FENCE_RE` bounded and nothing else changed, the shipped oracle reports the corrected reader unsafe on 1 and 6 lines. A corrected oracle reports finding 1 — 1 line and 2 lines against the shipped reader, 0 against the bounded one. The generator has no indentation token, so the shape must arrive as a parametrized row |
| 3 | 🟡 `_paragraph_ends_at`'s docstring states the justification the fix pass says its own fuzz disproved, without qualification, as the design's whole safety argument | `skills/verify/scripts/unverified_check.py#_paragraph_ends_at` | open | Executed. With the setext underline stop missing — CommonMark 4.3 — the document `["text \`", "===", "text \`", "plain prose", "text \`"]` reads lines 3 and 4 live; with the stop added it parks them, and the format parks them. Incompleteness moved the answer toward live. The correction reached the ledger and not the sentence the next editor reads |
| 4 | 🟡 `_paragraph_ends_at` stops where markdown does not — an ordered marker not starting with 1, `#` with no space, seven hashes, more than nine digits — and an over-stop shortens the crossing reading's reach, which is the direction that goes live | `skills/verify/scripts/unverified_check.py#_paragraph_ends_at` | open | Executed. CommonMark 5.3, 4.2 and 5.2. The shipped rule and a corrected one disagree on 944 lines of the repository's own `.md` files, most of them prose beginning with an issue reference. The correction changes liveness on 6 lines across 4 files, all under `seal/specs/`, none in `docs/`, `seal/ledger.md` or `seal/ledger/`. The `|` stop is left alone — it is a measured over-stop and removing it moves the corpus |
| 5 | 🟡 The corpus floor case keys a dictionary on the marker line, so 94 occurrences collapse to 83 and only the last state of each survives | `tests/test_unverified_rows_close.py#test_the_three_named_markers_are_live_in_this_repositorys_ledger` | open | Executed. `seal/ledger.md` carries 11 marker lines twice — 1215/1218, 1259/1262, 1333/1336, 1370/1373, 1398/1401, 1434/1437, 1526/1529, 1590/1593, 1629/1632, 1777/1780, 1797/1800 — so a regression parking the first of a pair is invisible, and `len(live) >= 80` is a floor on keys rather than occurrences |
| ⬜ 6 | `spec.md` G3 grounds the gate change on the oracle being derived from the format rather than from the scan, which finding 2 disproves | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` §*Goals* G3 | open | Read against the tree. The case it names is the right one; the ground is not true of the reading in the tree. Under `seal/specs/`, so outside `Needs a fix` |
| ⬜ 7 | `spec.md` A6's note says the replacement acceptance asserts agreement, and G3 four rows above says agreement would forbid the design | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`, the acceptance table | open | Read. The **RETIRED** correction itself is right and renders; the note's last sentence was carried forward from round 4 and is now stale. Under `seal/specs/`, so outside `Needs a fix` |
| ⬜ 8 | `overview.md` §*Not verified* names the incomplete-block-list risk correctly and then names the safety fuzz as what watches it | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/overview.md` §*Not verified* | open | Read, against finding 2. The row is otherwise the right disclosure and is the reason this round could aim at the right thing. Under `seal/specs/`, so outside `Needs a fix` |
| ⬜ 9 | `overview.md` §*Not verified* row 3 describes an exit 2 from the records arm that no longer happens, and names a `spec.md:30` that now holds a different row | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/overview.md` §*Not verified* | open | Executed at this SHA: `bin/evidence-check --strict .` exit 0, `510 names read · 0 refused · 0 drifted · 0 external`, ledgers `1439 ok · 0 drifted · 0 broken`. Under `seal/specs/`, so outside `Needs a fix` |
| ⬜ | The width rule in `_partner_ahead` has exactly one guard, and it is the fuzz case finding 2 is about | `skills/verify/scripts/unverified_check.py#_partner_ahead` | confirmed | Executed. Ignoring run width reddens `test_the_scan_never_reads_live_what_the_format_parks` and nothing else, 1 failed of 191. The guard does hold for that mutation; named so that fixing finding 2 does not lose it |
| 🟢 confirmation | Round 5's ⬜ 4 — the anchor list — is fixed and now matches the fragment | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md` §*Data & interfaces* | confirmed | Read against the fragment's anchor column: `_liveness`, `_paragraph_ends_at`, `_partner_ahead`, `live_lines`, `folded_items`, `coordinates`, `main` twice, `OPENER` and 15 cases |
| 🟢 confirmation | Round 5's ⬜ 5 — A6 — is fixed and the retirement renders | `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`, the acceptance table | confirmed | Read. **RETIRED** is in the first cell, so a rendered view no longer shows a live acceptance criterion with its note invisible |
| 🟢 confirmation | The corpus figures are 761 / 94 / 83 for `seal/ledger.md`, the three named markers are live at 767, 992 and 1619, and 903 is the eleven-file total | `seal/ledger.md` | confirmed | Re-derived by execution at this SHA rather than carried. The eleven-file corpus gives 903 / 94 / 83; round 5's 102 / 85 reproduces on neither set |
| 🟢 confirmation | The marker audit holds: no compound name the tree lacks reaches an unmarked claim line, in either live work item | `seal/specs/` | confirmed | Re-derived over every `.md` file `record_files` reads, through `claim_lines` and `compound` rather than by eye. 17 names silenced here, 9 in the tree, 8 absent; `check_records` is silenced and read on no unmarked line in this work item, which is noise rather than a hole. `bin/evidence-check --strict .` at exit 0 agrees |
| 🟢 confirmation | Every one of the eight new units has a mutation that reddens it, and the two-reading AND is load-bearing on both sides | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Executed, six mutations against both modules in a clone at this SHA; baseline 191 passed exit 0, read with `echo $?` and not through a pipe. The mapping is in the table above |
| 🟢 confirmation | The AND cannot be broken from the span side on the shapes this round was asked to try | `skills/verify/scripts/unverified_check.py#live_lines` | confirmed | Read and executed. A partner in the next paragraph, three runs on a line, a run reaching across a fence, a lone backtick line, a run on the last line, a marker beside an unclosed run — each answers the way the docstring's table says. The structural reason is that a marker line opens an HTML block in CommonMark 4.6 and so always ends the paragraph above it |
| ❓ out of verified scope | Whether the repository's full suite, the repository-wide lint and the typecheck pass at this SHA | the repository | not run | §2 gives the broad gate to the sealer and this definition hands me none of the three. The orchestrator reports five modules at 406 passed exit 0, `evidence_check.py --strict .` at exit 0 and `survivor-check` at exit 0, all at this SHA; I re-ran `bin/evidence-check --strict .` and the two affected modules and nothing else. The caller answers it |

## Executed probes

| What was run | Result |
|---|---|
| the two affected modules in a pristine clone at the target SHA | 191 passed, exit 0, read with `echo $?` and not through a pipe |
| the indented-delimiter document through `live_lines` and `comment_scan` | `live_lines` reads the marker live; `comment_scan` answers *began inside* |
| the same document through `folded_items` and `settle --retire` on a throwaway git repository | `{'1700000042-quoted'}`, exit 0, `removed seal/specs/1700000042-quoted/`, directory deleted |
| the real-fenced-example shape — one phantom opener above a genuine fenced block holding a marker | the marker reads live |
| `_paragraph_ends_at` against the oracle's `block_ends_at`, 40,000 generated lines and every `.md` file in the tree | 0 disagreements in both |
| both of finding 1's documents through the scan and the shipped oracle | the oracle returns the scan's verdicts line for line; 0 unsafe lines reported |
| `FENCE_RE` bounded to three spaces, shipped oracle, the same two documents | the oracle reports the corrected reader unsafe on 1 and 6 lines |
| a corrected oracle against the shipped reader, the same two documents | reports the marker line and its neighbours — 1 line and 2 lines |
| a corrected oracle against the bounded reader, the same two documents | 0 unsafe |
| the shipped fuzz generator with each pairing of reader and oracle, 2,000 documents | 0 unsafe in all four; the generator builds no indentation |
| `FENCE_RE` bounded to three spaces, over every `.md` file in the repository | 0 lines change; the eleven-file corpus stays at 903 / 94 / 83 |
| `FENCE_RE` bounded to three spaces, against both modules | 191 passed, exit 0 |
| the setext-underline document with and without the missing stop | shipped rule reads lines 3 and 4 live; with the stop, parked — incompleteness moved the answer toward live |
| the block rule corrected for the four over-stops, over every `.md` file in the repository | the rules disagree on 944 lines; liveness changes on 6 lines in 4 files, all under `seal/specs/` |
| six mutations of `_liveness`, `_paragraph_ends_at` and `_partner_ahead` against both modules | every one red; the mapping is in the confirmations above |
| `seal/ledger.md` through `live_lines` | 2,430 lines, 761 not-live, 94 live marker occurrences, 83 unique ids, the three named markers at 767, 992, 1619, and 11 marker lines appearing twice |
| the eleven-file corpus through `live_lines` | 903 not-live, 94 occurrences, 83 ids |
| the marker audit re-derived through `record_files`, `claim_lines` and `compound` over both live work items | 0 absent names on an unmarked claim line; 17 silenced here, 9 in the tree, 8 absent |
| `bin/evidence-check --strict .` at this SHA | exit 0 — `510 names read · 0 refused · 0 drifted · 0 external`; ledgers `1439 ok · 0 drifted · 0 broken` |
| the broad gate — the repository's full suite, the repository-wide lint, the typecheck | **not yet** — not run by this round and not this round's to run. The sealer takes it |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A stamp on a round report is tracked as a live claim, so a coordinate is rewritten across five files and a record can state a value that did not exist at its own `Target SHA` | `seal/follow-up.md`, not this branch — already deferred in round 3 and confirmed in rounds 4 and 5 | the orchestrator |

## Paste-ready fixes

Finding 1 — `skills/verify/scripts/unverified_check.py`, replacing the
`FENCE_RE` assignment and its comment. `blank_fences` keeps its own copy and
is deliberately not moved: the constant's comment already says that copy
serves the other gates and this scan may not move it.

```python
# A run of backticks, and a fence opener. `live_lines` needs both as it
# scans; `blank_fences` keeps its own copy of the fence pattern because it
# serves the other gates and this scan may not move it.
#
# **Three spaces, not `\s*`.** CommonMark 4.5 bounds an opening fence to three
# spaces of indentation; four is an indented code block, or a lazy
# continuation line inside an open paragraph. Reading one as a delimiter does
# not merely park lines — it INVERTS the fence state for the rest of the file,
# so a real fenced block's content reads live and its delimiters read as
# content, and a fold marker quoted inside a fenced example becomes a fold
# record. The constant above names `skills/settle/SKILL.md` §2 as the document
# that shows the marker inside a fence with a real released id, which is the
# quotation this would read (round 6, finding 1; executed on a throwaway git
# repository, `settle --retire` at exit 0 with the directory removed).
# Measured 2026-09-22: bounding it moves 0 lines in every `.md` file in this
# repository and the eleven-file corpus stays at 903 not-live, 94 marker
# occurrences and 83 ids.
BACKTICKS = re.compile(r"`+")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
```

Finding 2 — `tests/test_unverified_rows_close.py`, inside
`a_reading_from_the_commonmark_rules`: replace `block_ends_at` and `fence_of`,
and correct the docstring's fourth bullet. `str.startswith("")` is
unconditionally true, so the old `#` guard's second conjunct was dead and the
clause was the reader's `s.startswith("#")` exactly.

```python
    def block_ends_at(line):
        indent = len(line) - len(line.lstrip(" "))
        s = line.strip()
        if not s:
            return True
        if s.startswith("|") or s.startswith(">"):
            return True
        if indent <= 3 and s.startswith("#"):
            # CommonMark 4.2: one to six hashes, then a space, a tab or the
            # end of the line. The guard this replaces read
            # `s.lstrip("#").startswith((" ", ""))`, and `str.startswith("")`
            # is true of every string, so it asserted nothing.
            n = len(s) - len(s.lstrip("#"))
            if 1 <= n <= 6 and (len(s) == n or s[n] in " \t"):
                return True
        if indent <= 3 and len(s) >= 3 and s[0] in "`~" and s[:3] == s[0] * 3:
            return True
        if len(s) >= 3 and s[0] in "*-_" and set(s.replace(" ", "")) == {s[0]}:
            return True
        if s[:2] in ("- ", "* ", "+ "):
            return True
        head = s.split(".", 1)[0]
        return head.isdigit() and s[len(head) : len(head) + 2] == ". "

    def fence_of(line):
        # CommonMark 4.5 bounds an opening fence to three spaces. Stripping
        # the line first was the one rule this reading still took from
        # `live_lines`, and while it did, this case agreed with the scan on
        # the shape that removed a directory (round 6, finding 2).
        if len(line) - len(line.lstrip(" ")) > 3:
            return None
        s = line.strip()
        if len(s) < 3 or s[0] not in "`~":
            return None
        n = runs(s, 0) if s[0] == "`" else len(s) - len(s.lstrip("~"))
        return s[0] * n if n >= 3 else None
```

```python
    - **Where a block ends** (CommonMark 4.1, 4.2, 4.3, 4.5, 4.8, 5.1, 5.2 and
      GFM 4.10): a blank line, a thematic break, an ATX heading, a fence
      delimiter, a block quote marker, a list item marker, or a table row.
      **A richer list is a WEAKER case, not a safer one**, and the sentence
      here used to claim the opposite. Every extra stop shortens
      `partner_in_this_block`, which makes this reading see fewer spans, which
      makes it call MORE lines live — and the only violation this case can
      report is the scan live where this reading parks. So each rule is the
      format's rule and no other, and the two indentation bounds above are
      where that stopped being true (round 6, finding 2).
```

And one parametrized row for `test_every_shape_five_review_rounds_named`, which
is where the shape has to arrive: the generator carries no indentation token,
so the fuzz cannot build it.

```python
        # Round 6. A fence delimiter indented four spaces is an indented code
        # block, not a delimiter. One of them inverts the fence state for the
        # rest of the file, and the marker quoted inside the real fenced
        # example below becomes a fold record — `settle --retire` removing the
        # work item's directory at exit 0 with nothing having absorbed it.
        (
            "a marker in a fenced example under an indented delimiter",
            "A fence opens with\n\n    ```python\n\nand closes with a run at "
            "least as long.\n\n```markdown\n<!-- specs/s-8 -->\n```\n",
            set(),
        ),
```

Finding 3 — `skills/verify/scripts/unverified_check.py`, replacing the third
paragraph of `_paragraph_ends_at`'s docstring.

```python
    **Being incomplete here is CHEAP, not safe, and the difference is a line
    the format parks.** This bounds one half of a disagreement rather than
    the answer, and a missing stop USUALLY only lets `_partner_ahead` reach
    further, which makes the crossing reading believe in a span the format
    would not, which parks a line — a fold reported as a deletion, at exit 1,
    which a person sees. Usually, not always: reaching further also changes
    which runs pair with which, and a run that consumes a partner early
    leaves a later run with none, so a later line goes live rather than
    parked. Measured 2026-09-22 with the setext underline (CommonMark 4.3)
    missing, which it still is: `["text `", "===", "text `", "plain prose",
    "text `"]` reads its last two lines live and the format parks them. The
    rule round 5 removed decided the answer by itself, so its missing stops
    removed a directory; this one only leans, but it leans in both
    directions. Add a stop when the format has one.
```

Finding 4 — `skills/verify/scripts/unverified_check.py`, the body of
`_paragraph_ends_at`. The `|` stop is deliberately kept: it is an over-stop
with the measurement in the docstring above it, and removing it moves the
corpus.

```python
    s = line.strip()
    if not s:
        return True
    # `|` is a deliberate over-stop — GFM parses a table row's cells
    # independently and the measurement above is what it buys. `>` is the
    # format's own rule (CommonMark 5.1).
    if s.startswith(("|", ">")):
        return True
    # CommonMark 4.2: one to six hashes, then a space, a tab or end of line.
    # `s.startswith("#")` alone stops on `#hello` and on `####### seven`,
    # which are paragraph text — and on the issue references this repository
    # writes constantly, 944 lines of them (round 6, finding 4).
    if s.startswith("#"):
        n = len(s) - len(s.lstrip("#"))
        if 1 <= n <= 6 and (len(s) == n or s[n] in " \t"):
            return True
    if FENCE_RE.match(line):
        return True
    if s[0] in "*-_" and len(s) >= 3 and set(s.replace(" ", "")) == {s[0]}:
        return True
    if s[:2] in ("- ", "* ", "+ "):
        return True
    # CommonMark 5.3: an ordered list interrupts a paragraph only when it
    # starts with 1. `3. an item` inside a paragraph is paragraph text, and
    # stopping there shortens the crossing reading's reach, which is the
    # direction that goes live.
    return s[:2] in ("1.", "1)") and len(s) > 2 and s[2] in " \t"
```

Finding 5 — `tests/test_unverified_rows_close.py`, the body of
`test_the_three_named_markers_are_live_in_this_repositorys_ledger`.

```python
    ledger = os.path.join(ROOT, "seal", "ledger.md")
    with open(ledger, encoding="utf-8") as f:
        lines = f.read().split("\n")
    # Every OCCURRENCE, not a dictionary keyed on the line. This file carries
    # eleven marker lines twice, so keying on the text kept the last state of
    # each and a regression parking the first of a pair was invisible to the
    # floor below (round 6, finding 5).
    occurrences = [
        (n, line.strip(), state)
        for n, (line, state) in enumerate(uc.live_lines(lines), 1)
        if line.startswith(uc.OPENER + " specs/")
    ]
    parked = [(n, line) for n, line, state in occurrences if not state]
    assert not parked, parked
    for want in (
        "1788472135-the-run-outlives-its-last-finding",
        "1788613827-a-runs-report-carries-one-comparison-table",
        "1788844127-the-reviewers-report-reaches-the-record-retyped",
    ):
        assert any(f"specs/{want} " in line for _, line, _ in occurrences), want
    assert len(occurrences) >= 90, len(occurrences)
    assert len({line for _, line, _ in occurrences}) >= 80, len(occurrences)
```

Needs a fix: yes — findings 1 to 5. The run is capped, so each is a a fix on this branch candidate for the orchestrator to file rather than a fix to commission on this branch; findings 1 and 2 are one fix, because bounding `FENCE_RE` alone turns the fuzz case red.
Loses a record or crashes: yes — finding 1, a work item's whole SDD set removed at exit 0 with nothing having absorbed it, executed on a throwaway git repository at the target SHA.

## Proof block

Executed at `1eb0ef0767a49b8d7ca0942b6178226f0334788e` in a
`git clone --no-local` of the repository, exit codes read directly and never
through a pipe. One probe file, `test_tmp_*`, one mutation script and two
measurement scripts; all four deleted and the clone removed before this
report was handed over. Nothing was written, committed, pushed or posted
anywhere but this file.

Files opened:

- `skills/verify/scripts/unverified_check.py`
- `skills/settle/scripts/settle.py`
- `skills/evidence-check/scripts/evidence_check.py`
- `tests/test_unverified_rows_close.py`
- `tests/test_settle_reads_before_it_removes.py`
- `seal/ledger.md`
- `seal/ledger/1790039346-settle-reads-a-marker-inside-a-commented-out-draft.md`
- `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/spec.md`
- `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/overview.md`
- `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-5.md`
- `seal/specs/1790039346-settle-reads-a-marker-inside-a-commented-out-draft/rounds/round-5-report.md`
- `CONTRIBUTING.md`, `CLAUDE.md`
- `docs/*.md` — scanned for an indented delimiter, not read in full
