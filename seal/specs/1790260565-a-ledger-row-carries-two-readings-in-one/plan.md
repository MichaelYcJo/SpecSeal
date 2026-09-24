# Implementation Plan: a ledger row carries two readings in one, and the rules' cases

<!-- seal/specs/1790260565-a-ledger-row-carries-two-readings-in-one/plan.md — HOW, in phases. -->

Approved <date> by <who>, when `smith` was spawned.

## Summary

The work has four slices, one per defect. Each ends green and committed.
Phase 1 repairs three ledger rows by judgment. Phase 2 makes the width case
count the rows it only claimed to read. Phase 3 plants the needles #569's
reviewer already ran. Phase 4 makes one document name the same rule its
code names. No shipped script changes. Every edit to a
`seal/releases/*.md` file keeps an existing claim true in the file the claim
stands in. The two new claims go to
`seal/ledger/1790260565-a-ledger-row-carries-two-readings-in-one.md`, and
each phase adds its line to `seal/specs/1790260565-…/changelog.md`.

## Technical context

- **The three rows (phase 1).** `seal/releases/0.9.2.md` S4,
  `seal/releases/0.8.2.md` G5, and `seal/releases/0.9.3.md` "The eleven
  modules that pin the path…". Find them by content, never by line.
  - In S4 and G5, the text after the first escaped separator is a date, and
    the text after the second is a Notes cell that **repeats the first Notes
    cell's opening word for word** and then carries later markers:
    - S4: 2026-09-23 merge re-read; `Corrected 2026-09-24` (#363);
      `Re-read 2026-09-24` (#198).
    - G5: 2026-09-23; four `Re-read 2026-09-24` notes (#174, #363, #198,
      #547).
  - No marker appears in both halves (read 2026-09-24).
  - The eleven-modules row has one date. Its two escaped separators split
    Notes text only.
- **`overwide_rows` (phase 2)** is at
  `tests/test_release_hygiene.py#overwide_rows`. Its header comes only from
  a `|` line followed by a table rule. Any non-`|` line resets it to
  `None`, and a row under `None` is skipped. The corpus case
  `#test_no_ledger_row_splits_into_more_cells_than_its_header` reads
  `ledger_files()` plus `seal/ledger/*.md`. The width to fall back on is in
  `templates/ledger.md`, in the header line that begins `| Clause |`, which
  has five cells.
  Every header on a ledger-row table in the tree has five cells:
  - 130 are `| Clause | … | Checked | Notes |`;
  - 15 are `| Claim | … | Date | Notes |`;
  - the only other two headers belong to the notation's `| Item | Value |`
    table and to one `| Decision | Content | Grounds |` table, and both
    keep their own header.
- **The needles (phase 3)** are
  `tests/test_a_merge_cannot_silently_drop_a_correction.py#CONFLICT_SENTENCES`
  and `#OWNED_SENTENCES`, and the owner's case
  `#test_the_policy_document_owns_the_exception_and_the_halves`. #569's body
  holds the reviewer's block verbatim, green at #567's target.
  Why the owner needs its own assertion: the owner's halves paragraph says
  `` `Corrected <date>` notes ``, which contains the shared needle
  `` `Corrected <date>` note ``. So the shared needle alone stays green with
  the edit arm's clause deleted from the owner.
- **The exception sentence (phase 4)** is `docs/round-record-spec.md`
  §*The fix surface — `Contract changes` and `New units`*, the paragraph
  that begins "**Its direction is `allow`". The code's statement is
  `skills/code-review/scripts/chain_check.py#says_not_yet`, docstring,
  second paragraph. The existing case for the behaviour is
  `tests/test_a_record_precedes_the_fixes_it_commissions.py#test_a_reason_the_checker_does_not_recognise_passes`.

**Rows this branch will drift.** Candidates were found by grep over the
anchors. `evidence-check` is the authority, and the list is not:

- phase 2: C2 (`0.15.1.md`, three anchors in `test_release_hygiene.py`), and
  D1 and E1 (`0.15.1.md`, on `docs/the-evidence-ledger.md`'s
  "## A row is a content anchor, and it names no commit");
- phase 3: E1 and E2 (`0.15.1.md`, `CONFLICT_SENTENCES` and the owner's
  case);
- phase 4: R4 (`0.9.1.md`, on round-record-spec §*The fix surface*).

**Hazard for every phase: `--reverify` re-stamps every drifted row in the
file it is given** (`seal/follow-up.md` row 72). Run the lenient
`bin/evidence-check --ledger <file> .` first. Reverify a file only when every
row it reports drifted is one this phase re-read. Otherwise write the new
hash by hand from the tool's report. G5's own notes record that precedent:
"Stamped by hand from a copy".

**`CLAUDE.md`: judged, nothing in it becomes false.**
- "A ledger fragment needs no header of its own. Every row in it carries its
  own anchor and hash, so there is nothing for a header to declare." Phase 2
  keeps fragments headerless and supplies the width from the template, so
  the fragment still needs no header.
- The *hunk by hunk* and *Appended is the word* paragraphs already carry
  every needle phase 3 adds.
- No paste-ready text is owed.

**Parallel chain.** `1790260566-a-row-inside-a-fence-reads-as-live` edits
the readers in `evidence_check.py`, `unverified_check.py`, `settle.py` and
`fold_ledger.py`. This plan touches none of them. The only shared ground is
fence handling, and `overwide_rows` keeps its own toggle (spec, *Out*).
Functions this branch edits:
- `tests/test_release_hygiene.py#overwide_rows` and
  `#test_no_ledger_row_splits_into_more_cells_than_its_header`;
- `tests/test_a_merge_cannot_silently_drop_a_correction.py#CONFLICT_SENTENCES`,
  `#OWNED_SENTENCES` and
  `#test_the_policy_document_owns_the_exception_and_the_halves`.

**What breaks in six months.** A new ledger-row shape with a sixth column.
The width is then read from the template, so the template is the one place
to change. A fragment carrying a table that is not a ledger row, with no
header, would be counted against five cells. The refusal names the line,
and that fragment would need a header, which is the right answer for a
table that is not ledger rows.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #568: keep the newer pair, drop the older | The older pair's `Re-read` markers leave a row that still stands. That is the loss `correction_check` exists to name, done by hand on a normal commit, where no check looks | rejected |
| #568: leave both pairs escaped | The row states two Checked dates, and a reader cannot tell which one the anchor's hash was taken at. That is the issue as filed | rejected |
| #568: the union by the halves rule. One Checked date (the re-read's), the shared opening once, then every marker of both sides in date order, then this work's `Re-read` note | The merged Notes cell is long, and it already was. The builder can collapse the duplicated opening wrongly, and A1's marker comparison is what catches that | **chosen** |
| #501: require every fragment to carry a header | Contradicts `CLAUDE.md` ("needs no header") and the fragment template. It needs an owner's edit, and 25 released rows would need a header inserted | rejected |
| #501: exempt headerless rows and correct the policy and C2 to say so | A headerless row renders in GitHub as a paragraph rather than a table, so no cell is dropped from sight. But the column shift the policy names still reaches every reader that keys on cells (`correction_check`'s first-cell row key, `settle.py#first_cell`). The policy's own argument for reading fragments ("blind exactly while the rows are being written") rules this out | rejected |
| #501: count a headerless row against the template's ledger-row width | A fragment table that is not ledger rows is counted against five cells. That is loud and names the line | **chosen** |
| #501: add the count to the shipped `evidence_check.py` | A new refusal in consumer repositories' builds, in a file the parallel chain is editing | out → `questions.md` Q1 |
| #569 ⬜ 2: point the document at `docs/review-chain-spec.md` more precisely | That section's `blocks more` is the reopening's failure direction, which is a different rule. More precision still points at the wrong rule | rejected |
| #569 ⬜ 2: reword the code's docstring to match the document | The code names the right rule, and the ledger row R7 (`0.8.0.md`) states it the code's way | rejected |
| #569 ⬜ 2: the reviewer's sentence in the document, plus a case holding document and docstring to one referent | none found | **chosen** |

## Phases

Vertical slices. Each ends committed, with its narrow run green. The broad
gate is `sealer`'s, not a phase's (`agent-contract` §2).

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#568.** S4 and G5 each hold one reading. The Checked date is this phase's re-read date. Notes hold the shared opening once, then every marker of both halves in date order, then `Re-read <date> by work item 1790260565 (#568)`: the two pairs were one merge's two sides, joined as a union by the halves rule, and the claim was re-read against its anchors. If the re-read finds a claim false (for S4, whether the claim cell must carry the tagged half its `Corrected 2026-09-24` note describes), the claim is corrected in place with a `Corrected <date>` note instead. The eleven-modules row's two escaped separators become sentence boundaries, and its Notes wording is otherwise unchanged, `Re-verified 2026-09-16` included. It gains the same `Re-read` note. Hashes are re-stamped by the hazard rule in *Technical context*. | (1) The phase-1 instrument, which searches for `\|` outside code spans in every table row of `seal/ledger.md` and `seal/releases/*.md`, returns nothing. (2) A throwaway `test_tmp_*` probe compares each row's marker multiset before and after, using `correction_check.py`'s own marker reader, and finds none lost. Delete the probe (§7). (3) `bin/evidence-check --ledger` over the three files, lenient: none of the three rows drifted. (4) `bin/test tests/test_release_hygiene.py -k "ledger or pipe"` | |
| 2 | **#501.** `overwide_rows` counts a row that has no header above it against a width supplied by its caller. The corpus case supplies the ledger-row width read from `templates/ledger.md`. A new unit case gives a headerless six-cell row and expects it named against five. The corpus case's docstring states what it now counts, with the instrument and the date. `docs/the-evidence-ledger.md`'s escaped-pipe paragraph takes the text below. C2 (`0.15.1.md`) gets a `Corrected <date>` note: its "every fragment" was true of reading and false of counting until this phase, and "Three of the 22 were a second date-and-notes pair" is corrected to two plus one split Notes cell. The fragment gains one row for the headerless count. D1, E1 and C2 are re-read wherever their anchors drift. | (1) The new unit case is **seen red** against the current `overwide_rows` (it returns `[]`) before the fix is written (§15). (2) `bin/test tests/test_release_hygiene.py`, where the corpus case is green with the 25 headerless released rows now counted. (3) `bin/test tests/test_a_folded_statement_names_what_enforces_it.py tests/test_a_document_has_room_for_the_next_fold.py`, where the `Enforced by:` line still resolves and the document is under its ceiling. (4) Lenient `bin/evidence-check --ledger seal/releases/0.15.1.md --ledger seal/ledger/1790260565-a-ledger-row-carries-two-readings-in-one.md .` | |
| 3 | **#569 ⬜ 1.** #569's paste-ready block goes in as the reviewer wrote it: three needles added, `OWNED_SENTENCES = CONFLICT_SENTENCES[-7:]`, the comment above the needles rewritten so it no longer says "the checker says which after the fact", and the owner's third-outcome assertion ("the edit made false is corrected there first"). E1 and E2 (`0.15.1.md`) each gain `Re-read <date> by work item 1790260565 (#569)`: the clauses round 1's fix pass added are now held by `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` and the owner's case, each seen red, so the Result's *Executed* now covers them. Their hashes are re-stamped. No document changes. | (1) Green at the start: `bin/test tests/test_a_merge_cannot_silently_drop_a_correction.py`. (2) **Seen red**, once per clause per carrier. Delete the clause and watch the right case go red. For `CONTRIBUTING.md` and `docs/the-evidence-ledger.md`, restore from kept bytes. For `CLAUDE.md`, use a scratch copy the probe points `ROOT` at, **never an in-place edit of the owner's file**. The phase record lists each deletion and the case it turned red. (3) Lenient `bin/evidence-check --ledger seal/releases/0.15.1.md .` | |
| 4 | **#569 ⬜ 2.** `docs/round-record-spec.md`'s paragraph opens with the reviewer's sentence: "**Its direction is `allow` for a reason the checker does not recognise, and that is a deliberate exception to the direction every other refusal in `chain_check.py` takes, which treats what it cannot read as failing.**" The rest of the paragraph is unchanged. A new case in `tests/test_a_record_precedes_the_fixes_it_commissions.py` asserts two things: the paragraph names `chain_check.py`'s direction and not `docs/review-chain-spec.md` §*The reopening*, and `says_not_yet.__doc__` still says every other refusal treats what it cannot read as failing. The fragment gains one row for this claim. R4 (`0.9.1.md`) is re-read if its anchor drifts. The changelog fragment is complete. | (1) The new case is **seen red** against the current document before the sentence changes. (2) `bin/test tests/test_a_record_precedes_the_fixes_it_commissions.py tests/test_the_reopening_is_one.py`. (3) Lenient `bin/evidence-check --ledger seal/releases/0.9.1.md --ledger seal/ledger/1790260565-a-ledger-row-carries-two-readings-in-one.md .` | |

### Phase 2's policy text, paste-ready

It replaces the paragraph under 1790208643's marker that begins "**A `|`
inside a ledger cell is escaped". The marker line and the `Enforced by:`
line stay exactly as they are.

```
**A `|` inside a ledger cell is escaped, and a row with more cells than its
table's header fails.** An unescaped pipe splits the row, and the text after it
lands in the next column, so a claim runs into its grounds and a date into its
notes. At `31937b9f`, 22 rows stood split that way: two of them carried a
second date-and-notes pair in one Notes cell, and one a Notes cell split in
two (#562; #568 joined each into one reading). A row under no header is
counted against the five columns `templates/ledger.md` declares for a ledger
row, because a fragment has no header by rule and the fold copies it into its
release file as it stands — without that width, every fragment row was read
and none was counted (#501). The case reads the shared file, every release
file and every fragment.
```

The builder may re-wrap the lines. The needles the case pins are the
sentences, not the line breaks.

## Operational impact

None for a deployer. No script, hook, skill or agent definition changes, and
the plugin version does not move. Inside this repository, the width case now
counts fragment rows. A branch that writes a headerless fragment row with a
stray `|` is refused on its own pull request rather than at the release that
folds it.
