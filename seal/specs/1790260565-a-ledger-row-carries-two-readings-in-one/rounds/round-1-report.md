# Round 1 report — a ledger row carries two readings in one

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | 59012e5d |
| Base | `origin/release/v0.15.3` = c52e8350 |
| Contract | `spec.md` and `plan.md` at frame 04ad1e6c |
| Reviewed by | specseal:warden on Opus 5.5 |
| Where | a `git clone --no-local` of the worktree, checked out at 59012e5d |

## Summary

The branch does what it claims, and nothing I found needs a fix. The three
rows now hold one reading each, and no dated marker was lost in the join. The
width case now counts rows that sit under no header. The new needles and the
new exception sentence each go red when their text is removed. Three ⬜ items
remain, and each is about how strong a case is, not about a wrong fact or
wrong behaviour:

1. The halves rule's first half, *only the notes are a union*, is still held
   by no needle. #568's repair rests on that sentence.
2. The new unit case's comment says it catches a corpus case that stops
   passing the width. Reverting the corpus case's call back to
   `overwide_rows` leaves every case green.
3. The row shapes `overwide_rows` still does not count. None of them is in
   the tree today.

One more ⬜ is a correction to this work item's paperwork. The plan's
approval line has a second sentence on the same line, so the chain check
cannot read it and reports it absent (⬜ 4).

## What the account claimed, and what I found

| Claimed | Found | How |
|---|---|---|
| No shipped script changed | True. The diff touches `docs/`, `seal/` and `tests/` only. None of the #444 chain's readers (`evidence_check.py`, `unverified_check.py`, `settle.py`, `fold_ledger.py`) is touched | read: `git diff --stat c52e8350...59012e5d` |
| S4 and G5 were one merge's two sides, and the join is a union | True for both. In each row the deleted second opening equals the first pair's opening byte for byte: 1284 shared characters in G5 and 652 in S4, each running into the first marker where the two sides differ (`Re-read 2026-09-06`/`-22` against `Re-read 2026-09-23`). The new Notes cell is the first side's whole text, then a period, then the second side's text after the shared opening | executed: a probe split each row on its escaped separators at c52e8350 and compared the two sides with the row at 59012e5d |
| No marker lost | True for every row the branch changed: S4, G5, the eleven-modules row, C2, D1, E1, E2 and R4. Each one lost nothing and gained only this work item's own notes | executed: `correction_check.markers` on each row before and after, the rows matched by key or by anchor set |
| S4's claim was false after #363 and is corrected in place | True. `docs/issues-and-milestones.md:129-131` says *at or above the running one and not yet tagged*, and *a version below the running one, or one this repository has tagged, is history*. The corrected claim says the same. The count of two documents still holds: only `docs/issues-and-milestones.md` and `docs/release-checklist.md` under `docs`, `skills`, `agents`, `CONTRIBUTING.md` and `README.md` carry *at or above the running* | read, plus `git grep -l` |
| The eleven-modules row had seven cells at `31937b9f`, so its Notes cell was split in three rather than two, as the frame said | True: seven pipes, no closing pipe, seven cells. The policy paragraph and C2 are right, and the spec and plan are wrong. `overview.md` records this as a divergence | executed |
| Only two rows carried a second date-and-notes pair | True at `31937b9f` and at c52e8350, and there are none at 59012e5d. A row counts here when more than one cell is a bare date after splitting on every pipe, escaped or not. The scan covered `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md` | executed |
| A fourth row (`0.11.5.md:28`) was left alone as a single reading | Agreed. Its `\|` sits outside a code span only because the quoted assertion carries backticks inside a single-backtick span. The escape keeps it one cell, and the row has one Checked date | executed (the instrument) and read |
| The unit case was seen red against the header-only `overwide_rows` | Reproduced: `assert [] == [(1, 5, 6)]` | executed: I reset the width in `overwide_rows` to `None` in the clone, then restored it |
| The phase-4 case was seen red against the old paragraph | Reproduced: *the spec's exception does not name the direction chain_check.py's other refusals take* | executed: I restored the base `docs/round-record-spec.md` in the clone, then restored the target version |
| Each new clause goes red when deleted from each carrier | Held by construction. Each new needle occurs exactly once in `CLAUDE.md` and in `CONTRIBUTING.md`. In the policy document, `` `Corrected <date>` note `` occurs twice, and the separate third-outcome assertion covers that, because its needle occurs once | executed: a whitespace-collapsed count of each needle in each carrier |
| 25 released rows were uncounted and are now counted | True. There are 767 body rows over the shared file and the release files, 25 of them under no header (5 in `0.15.0.md`, 20 in `0.15.1.md`). Counting the fragment's own 2 rows gives 769 and 27. All are five cells wide, and `ledger_overwide` names no row anywhere | executed |
| `survivors.md` exempts what the sweep reported | True. `bin/survivor-check --range c52e8350...59012e5d --exempt …/survivors.md` exits 0: *every survivor is excused by a row above (14)* | executed |
| The date switch at phase 2 | Consistent. Every note from phase 2 on is dated 2026-09-25, and each re-read row's Checked cell matches its newest note | read |

## Findings from reading

### ⬜ 1 — the halves rule's union clause is held by no needle

`tests/test_a_merge_cannot_silently_drop_a_correction.py:711` (`CONFLICT_SENTENCES`)

I enumerated the class this round was asked for: every sentence stating the
edit and conflict rules that the needles do not hold. After #569's three
needles went in, these clauses still carry no needle:

- **The halves rule's first half.** The bold sentence *Hunk by hunk has two
  halves, and only the notes are a union* stands at `CLAUDE.md:169`,
  `CONTRIBUTING.md:258` and `docs/the-evidence-ledger.md:150`, and so does
  *A row's `Re-read <date>` and `Corrected <date>` notes are both sides'*.
  The #509 needles hold only the hash half. This is the clause #568's own
  repair rests on: the spec's Grounding cites it, and so does every new note
  on S4 and G5. It is in all three carriers exactly once, so a needle for it
  goes in green.
- **The edit rule's other two outcomes.** These are *re-read and re-stamped
  there with a dated note* (the claim holds) and *remove the row and write
  the new claim into the fragment* (the claim went with the code). The
  guides word them differently: `CLAUDE.md` has a sentence and
  `CONTRIBUTING.md` a bulleted list. So no shared needle exists without a
  rewording, and each would need a needle for its own carrier.
- **The arguments behind them.** These are *Taking a side reverted three
  corrections* and *`correction-check` cannot see a union that kept a stale
  hash*. Both are the kind of text the module's comment says it pins
  (*the INSTRUCTION and the argument behind it*).

Why it is ⬜ and not 🟡: every one of these sentences is true today, and
nothing ships wrong. What stays open is that deleting one fails no case. That
is the class #569's ⬜ 1 was filed under, at the same severity.

### ⬜ 2 — the unit case's comment claims it catches a regression it does not

`tests/test_release_hygiene.py:1296`

The comment reads *What the corpus case calls, so a width it stopped passing
goes red here*. `overview.md` puts it more strongly: *Through the helper the
unit case goes red on the same mutation*. The unit case goes red only when
the width is dropped **inside** `ledger_overwide`. The natural regression
edits the call site instead: someone changes
`tests/test_release_hygiene.py:1325` back to `overwide_rows(...)`, and then
no case goes red. I executed that mutation, and all three cases selected by
`-k "test_a_row_under_no_header or test_no_ledger_row_splits or pipe"`
stayed green. The corpus is five cells wide everywhere, so it cannot notice
that its rows under no header went uncounted again.

Nothing ships wrong: the corpus case does call `ledger_overwide` today. The
defect is a sentence that overstates what the case holds.

### ⬜ 3 — shapes `overwide_rows` still does not count

`tests/test_release_hygiene.py:1255`

I enumerated the class, and none of these shapes is in any ledger file at
59012e5d (executed):

- **A row indented by one to three spaces.** `overwide_rows` requires
  `line.startswith("|")`. `correction_check.rows` strips the line first
  (`skills/evidence-check/scripts/correction_check.py:360`), so the marker
  reader reads a row the width case skips.
- **A row inside a `~~~` fence or an indented fence.** The spec's *Out*
  leaves this to the #444 chain, and that is still the right owner.
- **A row ending in `\|` with no closing pipe.** The spec's *Out* covers it.
  It produces a loud refusal, not a silent pass.
- **A table whose header is itself wider than the template.** Its rows are
  measured against its own header, so a six-cell header lets six-cell rows
  pass. The rule as written (*more cells than its table's header*) allows
  this, so it is a limit of the rule, not of the fix.

I checked one more candidate and rejected it: `\\|` (an escaped backslash
before a pipe). `0.12.0.md:105` carries one inside a code span, and the case
treats it as an escape. I did not render it to confirm how GFM reads it, so
that one is **read**.

## Findings from execution

### ⬜ 4 — correction: the checker cannot see the plan's approval line

`seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/plan.md:5`

I dry-ran `round_record.py new` on this report inside the clone. Its chain
check reported *plan.md's approval line is absent*. The line is there. It
fails to match because a second sentence follows it on the same line:
`APPROVED_RE` (`skills/code-review/scripts/chain_check.py:3806`) is anchored
at `was spawned\.$`, and the line goes on with *Q1 builds on its default (a)
and is filed for the owner as #585.* The check reports this and does not
refuse the record. This is a correction to the run's paperwork, so it is not
counted under `Needs a fix`.

Every other run below exited 0, except the two mutation probes, which were
meant to go red and did.

## Regression tests to plant

- `tests/test_a_merge_cannot_silently_drop_a_correction.py`: the union
  needle below, if ⬜ 1 is taken.
- `tests/test_release_hygiene.py`: if ⬜ 2 is taken, a case that runs the
  corpus case's own iteration over a synthetic tree holding one overwide
  headerless fragment row. The alternative is to reword the comment so it
  claims only what the unit case holds.

## Facts for the evidence ledger

None owed. L1 and X1 in the fragment resolve (`bin/evidence-check`, 8 ok).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The halves rule's union clause, the edit rule's re-stamp and removal outcomes, and the two arguments behind them are held by no needle, although #569 pinned their neighbours | `tests/test_a_merge_cannot_silently_drop_a_correction.py:711` | open | Needle counts in the three carriers (executed). *only the notes are a union* is in all three exactly once, so a needle for it goes in green |
| ⬜ 2 | The unit case's comment says a corpus case that stops passing the width goes red, but reverting the call site to `overwide_rows` keeps every case green | `tests/test_release_hygiene.py:1296` | open | Executed a mutation at `tests/test_release_hygiene.py:1325`: 3 passed |
| ⬜ 3 | Shapes still uncounted: an indented row, a row in a `~~~` or indented fence, a trailing `\|`, a header wider than the template | `tests/test_release_hygiene.py:1255` | open | None is in any ledger file at 59012e5d (executed). The fence and trailing-pipe shapes are already in the spec's *Out* |
| ⬜ 4 | Correction: the plan's approval line carries a second sentence after *was spawned.*, so the approval regex misses it and the chain check reports the line absent | `seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/plan.md:5` | open | Executed a dry run of `round_record.py new` in the clone. `APPROVED_RE` at `skills/code-review/scripts/chain_check.py:3806` is anchored at the end of the line. Reported, not refused |
| 🟢 | #568 — S4 and G5 are lossless unions of one merge's two sides under one Checked date, and the eleven-modules row's Notes is joined | `seal/releases/0.9.2.md:31`, `seal/releases/0.8.2.md:145`, `seal/releases/0.9.3.md` | confirmed | Byte comparison of each side's opening, marker multisets before and after, and no two-date row left in any ledger file (executed) |
| 🟢 | S4's claim is corrected to carry the tagged half | `seal/releases/0.9.2.md:31` | confirmed | `docs/issues-and-milestones.md:129-131` (read) |
| 🟢 | #501 — a row under no header is counted against the template's five columns, and the policy paragraph and C2 say so | `tests/test_release_hygiene.py:1233` | confirmed | Unit case seen red against the header-only function and green after; corpus green over 769 rows (executed) |
| 🟢 | #569 ⬜ 1 — the three needles and the owner's third-outcome assertion pin the clauses #567's review added | `tests/test_a_merge_cannot_silently_drop_a_correction.py:711` | confirmed | Each needle occurs once per guide, and the owner has its own assertion (executed) |
| 🟢 | #569 ⬜ 2 — the spec's exception names the direction `chain_check.py` names, and a case holds both statements to it | `docs/round-record-spec.md:542` | confirmed | New case red against the base paragraph and green at target (executed) |
| 🟢 | No drifted or broken anchor anywhere in the ledger, and the survivor sweep is fully exempted | `seal/` | confirmed | `bin/evidence-check .` 2062 ok, 0 drifted. `bin/survivor-check` with the exemption file exits 0 (executed) |

## Executed probes

| What was run | Result |
|---|---|
| A probe (named with the `test_tmp_` prefix, run once, deleted) over `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md` at 59012e5d: rows with a `\|` outside a code span or an escaped date pair; `ledger_overwide` over every file; rows under no header; indented or `~~~`-fenced rows; marker multisets of every changed row before and after; the eleven-modules row at `31937b9f` | one `\|` row (`0.11.5.md:28`, a single reading); no overwide row; 769 body rows, 27 under no header; no indented or `~~~` rows; no marker lost; 7 cells at `31937b9f` |
| Rows with more than one bare date cell, splitting on every pipe, at `31937b9f`, c52e8350 and 59012e5d | 2 (G5, S4), then 2, then 0 |
| Byte comparison of the second opening against the first in G5 and S4 | shared opening identical, and the new Notes cell is the first side whole plus the second side's remainder |
| `bin/test -q tests/test_release_hygiene.py -k "ledger or pipe or header or width"` | 6 passed, exit 0 |
| `bin/test -q tests/test_a_merge_cannot_silently_drop_a_correction.py tests/test_a_record_precedes_the_fixes_it_commissions.py tests/test_a_folded_statement_names_what_enforces_it.py tests/test_a_document_has_room_for_the_next_fold.py` | 139 passed, exit 0 |
| `bin/test -q tests/test_no_real_identifiers.py tests/test_unverified_rows_close.py` | 151 passed, exit 0 |
| Mutation: base `docs/round-record-spec.md`, then the phase-4 case | red, *does not name the direction chain_check.py's other refusals take*; file restored |
| Mutation: the width reset to `None` in `overwide_rows`, then the unit case | red, `assert [] == [(1, 5, 6)]`; file restored |
| Mutation: the corpus case calls `overwide_rows` instead of `ledger_overwide` | green, 3 passed: this is ⬜ 2; file restored |
| Needle counts in `CLAUDE.md`, `CONTRIBUTING.md` and `docs/the-evidence-ledger.md`, whitespace collapsed | each new needle occurs once per guide; `` `Corrected <date>` note `` occurs twice in the owner; *only the notes are a union* occurs once in each and is not a needle |
| `bin/evidence-check --ledger` over the five touched release files and the fragment, lenient | 544 ok, 0 drifted, 0 broken |
| `bin/evidence-check .` | 2062 ok, 0 drifted, 0 broken; records 35 names read, 0 refused |
| `bin/correction-check --range c52e8350...59012e5d` | no merge commit in the range, exit 0 |
| `bin/survivor-check --range c52e8350...59012e5d --exempt seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/survivors.md` | every survivor excused (14), exit 0 |
| `round_record.py new` on this report, run as a dry run in the clone and discarded | the tables parse; `Needs a fix` and `Loses a record or crashes` both read `no`; the chain check reports the plan's approval line absent, which is ⬜ 4 |
| The broad gate: full suite, lint and format over the finished branch | not yet: it has not been run, and it is the sealer's |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The fence toggle in `overwide_rows` misses `~~~` and indented fences (part of ⬜ 3) | spec *Out*: the #444 chain's fence helper, adopted here after it lands | the orchestrator, when it sequences #444 against this branch |
| The cell count as a shipped refusal for consumer repositories | `questions.md` Q1 → #585 | the owner |

## Paste-ready fixes

### ⬜ 1 — the union needle

In `tests/test_a_merge_cannot_silently_drop_a_correction.py`, the #509 group
and the slice. The needle is already in all three carriers exactly once, so
this goes in green. To see it red, delete the bold sentence from each
carrier's scratch copy.

```python
    # #509: of a conflicted row only the notes are a union; the hash is the
    # side's that edited the unit and neither side's where both did, and the
    # row the checker names is re-read against every edit the merge carries.
    "only the notes are a union",
    "the side that edited the anchored unit",
    "to neither side where both did",
    "re-read against every edit the merged unit carries",
    "run `evidence-check` after the resolution",
)

# The owner of the two rules the needles above end with. The guides carry
# them and link here; the policy document states them first (#488, #509).
OWNED_SENTENCES = CONFLICT_SENTENCES[-8:]
```

### ⬜ 2 — a comment that claims what the case holds

In `tests/test_release_hygiene.py`, inside
`test_a_row_under_no_header_is_counted_against_the_width_it_is_given`:

```python
    # `ledger_overwide` is what the corpus case calls, so a width dropped
    # inside it goes red here. A corpus case that stops calling it does not:
    # no row in the tree is overwide, so the corpus alone stays green.
    assert ledger_overwide(fragment) == [(1, 5, 6)]
```

### ⬜ 4 — the approval line on a line of its own

In `seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/plan.md`,
replace line 5 with these two paragraphs:

```
Approved 2026-09-24 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

Q1 builds on its default (a) and is filed for the owner as #585.
```

Needs a fix: no
Loses a record or crashes: no


The gate has come due. Nothing this round opened needs a fix, so the next act
is the sealer's spawn, and the broad gate is its to run.

## Proof block

Files opened in this round, all at 59012e5d in the clone unless a revision
is named:

- `seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/`: `spec.md`, `plan.md`, `questions.md`, `overview.md`, `survivors.md`, `changelog.md`, `phases/phase-1.md`, `phases/phase-3.md`
- `seal/ledger/1790260565-a-ledger-row-carries-two-readings-in-one.md`
- `seal/releases/0.8.2.md`, `0.9.1.md`, `0.9.2.md`, `0.9.3.md`, `0.15.1.md` (the changed rows, at c52e8350 and at 59012e5d); `0.11.5.md:28`; `0.12.0.md:105`
- `seal/ledger.md` at `31937b9f` (the split rows)
- `tests/test_release_hygiene.py` (`overwide_rows`, the helpers, both cases, `ledger_files`)
- `tests/test_a_merge_cannot_silently_drop_a_correction.py:690-790`
- `tests/test_a_record_precedes_the_fixes_it_commissions.py` (the new case, via the diff)
- `docs/round-record-spec.md` and `docs/the-evidence-ledger.md` (the changed paragraphs); `docs/issues-and-milestones.md:120-140`; `docs/release-checklist.md:260-272`
- `CLAUDE.md`, `CONTRIBUTING.md` (the conflict and edit paragraphs, whitespace collapsed)
- `skills/evidence-check/scripts/correction_check.py:300-370`; `skills/code-review/scripts/chain_check.py#says_not_yet` (docstring) and `chain_check.py:3806` (`APPROVED_RE`)
- `seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/plan.md:5` (the approval line)
- `templates/ledger.md` (the `| Clause |` header line); `bin/test`
