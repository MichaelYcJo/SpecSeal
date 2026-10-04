# Round 2 report — 1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters (#729, PR #768)

Target `dc01bbb9`, the verifying round for round 1's fix range
`597d3625..2fa080e3`, against `release/v0.18.1` at `edee5ca2`. Reviewed in a
`git clone --no-local` scratch clone at the target. The worktree under review
was only read, and this file is the one write in it.

## The answer in four lines

- **All four of round 1's verdicts hold.** Each fix does what the account
  says, and each new case was shown red against round 1's target and is green
  at this one.
- **The enumeration of round 1's finding 1 left three sentences standing.**
  Two are cells of the design record's #729 section, which the fix pass
  edited in the column beside them. The third is a comment in `settle.py`.
  None is a shipped defect (⬜ 2).
- **The new unit `CITED_NAME_RE` reads every name in today's tree right**, but
  the docstring beside it claims more than it does: the listing and the
  removal disagree on five shapes, none of which the tree holds (⬜ 1).
- **Two loose ends of the new procedure text**: it names a release tag without
  saying how to find it (⬜ 3), and its 381-line figure counts more than the
  sentence says it counts (⬜ 4).

Nothing this round found needs a fix. The broad gate has come due: the
sealer's spawn is next.

## What the account claimed, and what I found

The round paragraph and the round-1 record's grounds are the account. Each
claim was opened against the code at the target.

- **Round 1, finding 1, option (b).** Claimed: the arm section gained a
  paragraph, fold step 1 now says to read a cited record at the tag, and every
  "nothing reads" sentence became "no check reads". Found: the paragraph is at
  `skills/settle/SKILL.md:116-124` and the fold-step sentence at
  `skills/settle/SKILL.md:204-206`. Both are pinned by
  `test_the_fold_reads_a_reference_into_the_process_record_at_the_tag`, which
  went red against round 1's docs. The four carriers the fix pass converted
  are pinned by `test_no_carrier_says_nothing_reads_the_process_record`, and
  the design record's #729 cell by
  `test_the_design_records_dated_section_says_no_check_reads_it`. The
  enumeration is the part that is not whole (⬜ 2).
- **Round 1, finding 2.** Claimed: `cites_a_process_record` reads the name
  through `CITED_NAME_RE` and leaves the verdict to `is_process_record`.
  Found: it does, at `skills/settle/scripts/settle.py:1351-1366`. The 176
  taken-name cases, built as eleven names times sixteen tails, gave 122 red
  against round 1's predicate. With the end-to-end case that is 123, the
  figure the ledger fragment's row L3 records. All are green at the target,
  and the 144 not-taken controls are green at both.
- **Round 1, finding 3.** Claimed: the README rows. Found: both editions'
  `settle [--retire]` row now ends with a sentence naming
  `settle --retire-process` (`README.md:288`, `README.ko.md:280`), and the
  spelling three cases split on is untouched. The new assertion in
  `test_both_cheat_sheets_carry_the_command` went red against round 1's
  READMEs in both editions.
- **Round 1, finding 4, answered.** Claimed: the trade is written into
  `survivor_check.py`'s docstring. Found: it is, at
  `skills/code-review/scripts/survivor_check.py:344-349`, and it states round
  1's measurement as round 1 recorded it. I carried round 1's execution of the
  base-against-target case rather than re-running it, because no line of
  `written_for_a_pull_request` or of its call site moved in the fix range.
- **The 381 lines in 157 files across 51 items.** Re-measured at `e141980a`
  with a `git grep` of `(rounds|phases)/` over the released items'
  `overview.md`, `questions.md`, `plan.md` and `spec.md`: 381, 157 and 51,
  exactly. What the number counts is ⬜ 4.

## Findings

### ⬜ 1 — The docstring says the listing and the removal cannot disagree about a name, and they disagree on five shapes

**Where.** `skills/settle/scripts/settle.py:1362-1363`, beside
`CITED_NAME_RE` at `:1351`.

**What is wrong.** The docstring ends: "The answer is `is_process_record`'s,
so the listing and the removal cannot disagree about a name". The two
predicates share the final call, but not the reading of the name.
`is_process_record` takes any `pr.` name that ends in `.md`, and
`CITED_NAME_RE` stops at the first character outside `[A-Za-z0-9_-]` or at a
double dot. The second argument also differs: the arm passes whether the entry
is a directory on disk, and the citation passes whether the name is on
`PROCESS_DIRS`. I ran both predicates over eight shapes in a probe:

| A citation's path | The entry on disk | Listed | Taken |
|---|---|---|---|
| `pr..md` | file `pr..md` | no | yes |
| `pr.zh+hant.md` | file `pr.zh+hant.md` | no | yes |
| `survivors.md_` (closing an italic) | file `survivors.md` | no | yes |
| `survivors.md/notes.md` | directory `survivors.md` | yes | no |
| `rounds` | file `rounds` | yes | no |
| `rounds.`, `pr.md`, an empty path | as named | agree | agree |

**Why ⬜.** The first three list too little, which is the direction round 1's
finding 2 was about. But no name of any of these shapes is in the tree. The
one pull-request file at `e141980a` is `pr.ko.md`, and no citation outside
`seal/specs/` follows a process-record name with `_` or `-`. The last two list
too much, which costs a line of output. What would ship is a claim in a
docstring, and nothing that runs depends on it. Correcting the docstring
answers the finding. Widening the pattern would trade one guessed shape for
another.

### ⬜ 2 — The enumeration for round 1's finding 1 left three sentences that say the process record serves nobody after its release

**Where.**

- `docs/one-root-by-lifetime.md:726`, the *What it corrects above* cell:
  "the process record was 525 of the 841 files … kept for nobody".
- `docs/one-root-by-lifetime.ko.md:698`, the same cell: "아무도 읽지 않는 채
  남아 있었습니다".
- `skills/settle/scripts/settle.py:1195`: "What a work item's directory holds
  for its pull request and nothing after its release".

**What is wrong.** The round paragraph asked for this check, and these three
sentences answer it. I built the class by construction, as every line the
branch adds outside this item's frame and ledger fragment that claims no
reader, plus a grep of every *process record* paragraph in the tree. The
0.4.0 body's "nothing reads it after the merge" (`docs/one-root-by-lifetime.md:168`)
is the one the fix pass left on purpose, and I left it too. The two table
cells sit in the row whose *Answer* cell the fix pass rewrote to "no check
reads it … what the SDD set still cites of it is read at the release tag".
The cell beside it still says the record was kept for nobody. The Korean cell
says it in so many words: nobody reading it. The `settle.py` comment is the
class's third spelling, "for its pull request and nothing after".

**Why ⬜.** The two table cells describe the state before #729. In the window
they describe, when no fold had run since 2026-09-24, nobody did read those
files. So the sentence can be read as true. The comment describes purpose
rather than readers. The behaviour is right and the procedure now says where
a reference resolves, so no release ships a defect if these stand. They are
listed so that the enumeration's answer is on record. Nothing pins any of the
three, and no ledger row anchors on the #729 section.

### ⬜ 3 — The procedure sends the reader to "the tag of the release that shipped the item" and does not say how to find that tag

**Where.** `skills/settle/SKILL.md:204-206` (fold step 1) and `:121-123` (the
arm section).

**What is wrong.** A work item's directory does not record which release
shipped it. The fold session has to find the tag before the example
`git show v<X.Y.Z>:<path>` works. The tag does exist: for each of the 55 items
present at `e141980a`, the first tag containing the commit that added the
directory exists, and no process-record file of any of them changed after that
tag. So the pointer is exact on today's corpus. Only the way to find it is
missing. A form with no tag also reads the latest version, which matters if a
process file is ever touched after its release: the parent of the commit that
removed the file.

**Why ⬜.** The reader can find the tag in more than one way, and each takes
one command. This is a missing convenience in a procedure, not a pointer that
fails to resolve.

### ⬜ 4 — "381 lines" counts every `rounds/` or `phases/` path, and the sentence says it counts the item's own records named by relative path

**Where.** `skills/settle/SKILL.md:116-119`.

**What is wrong.** The sentence reads: "name its own `rounds/round-N.md` and
`phases/phase-N.md` by relative path. Measured when this arm shipped, 381
lines in 157 of those files did". I reproduced 381 with the pattern
`(rounds|phases)/`. Of those lines, 50 write the path with a `specs/<id>/`
prefix, some of them into another item's directory. 331 are relative only,
and 281 of those name a `round-N` or `phase-N` file. The figure is the right
order of magnitude, and it measures the wider set.

**Why ⬜.** The figure only shows how large the problem is. No behaviour and
no instruction rests on it.

### Confirmed, each against the code

- **The fix range's narrow modules pass at the target**: the two new modules
  and `tests/test_a_process_record_drop_passes_the_readers.py`, 506 passed.
  Executed.
- **Each new case was seen red** (§15): the target's test files were run
  against round 1's `skills/`, `docs/` and READMEs. 131 failed, and every
  failure was one of the new cases. Executed.
- **The ledger fragment holds**: `evidence-check --strict` on this item's
  fragment, 114 ok, 0 drifted, 0 broken. Executed.
- **ruff check and ruff format --check on the four changed Python files**:
  clean. Executed. This is a lint of the changed files, not the repository-wide
  lint.

## Regression tests to plant

None is owed: nothing this round found needs a fix. If ⬜ 1 is answered by the
docstring, no case changes. If it is answered by changing the pattern, the
first three rows of ⬜ 1's table belong in
`tests/test_settle_retires_the_process_record.py` beside the taken-file cases,
shown red first.

## Facts for the evidence ledger

- Executed 2026-10-04 at `dc01bbb9`: the round-1 fix cases, run against round
  1's code and documents, failed 131 times, as 122 predicate cases, the
  end-to-end prose case, four carrier cases, the dated-section case, the
  fold-step case and both README editions. All passed at the target.
- Measured 2026-10-04 at `e141980a`: 55 work item directories, each with a
  release tag that contains its first commit, and no process-record file
  changed between that tag and `e141980a`.
- Measured 2026-10-04 at `e141980a`: of the 381 SDD-set lines naming a
  `rounds/` or `phases/` path, 331 are relative only, and 281 of those name a
  `round-N` or `phase-N` file.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The docstring says the citation listing and the removal cannot disagree about a name; they disagree on five shapes, three listing too little, none in the tree | `skills/settle/scripts/settle.py:1362` | open | executed: both predicates over eight shapes in a scratch probe, five disagree; read: the tree's one pull-request file is pr.ko.md and no citation follows a process name with an underscore or a dash |
| ⬜ 2 | The enumeration for round 1's finding 1 left three sentences saying the process record serves nobody after its release: the design record's corrects cell in both editions, and a comment in settle.py | `docs/one-root-by-lifetime.md:726` | open | read and grepped by construction; the Korean edition is `docs/one-root-by-lifetime.ko.md:698` and the comment is `skills/settle/scripts/settle.py:1195`; the 0.4.0 body at line 168 was left on purpose; no case pins and no ledger row anchors any of the three |
| ⬜ 3 | The procedure names the release tag a cited record resolves at without saying how to find it | `skills/settle/SKILL.md:204` | open | executed: 55 of 55 items have a tag holding their process record unchanged; read: no step says how to find it |
| ⬜ 4 | The 381-line figure counts every rounds or phases path, while the sentence says it counts the item's own records named by relative path | `skills/settle/SKILL.md:119` | open | executed: 381 reproduced with the wider pattern; 331 relative only, 281 naming a round or phase file |
| 🟢 | round 1's finding 1 is closed — the arm section and fold step 1 say where a reference from the SDD set resolves, and the four carriers say no check reads it | `skills/settle/SKILL.md:116` | confirmed | executed: the fold-step, carrier and dated-section cases red against round 1's docs and green at the target; the residue of the class is this round's ⬜ 2, which needs no fix |
| 🟢 | round 1's finding 2 is closed — a citation ending in punctuation, a line number or an anchor, or naming rounds with no slash, is listed | `skills/settle/scripts/settle.py:1354` | confirmed | executed: 123 red against round 1's predicate, all green at the target; controls green at both |
| 🟢 | round 1's finding 3 is closed — both README cheat-sheet rows name the process arm | `README.md:288` | confirmed | executed: the new assertion red against round 1's READMEs in both editions, green at the target; `README.ko.md:280` read |
| 🟢 | round 1's finding 4 is answered — the trade is written where the filter lives | `skills/code-review/scripts/survivor_check.py:344` | confirmed | read; round 1's base-against-target execution carried, since nothing it ran moved in the fix range |
| 🟢 | The fix range's three narrow modules pass at the target | `tests/test_settle_retires_the_process_record.py` | confirmed | executed: 506 passed |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the two new modules and the drop-readers module at `dc01bbb9` | 506 passed |
| The target's two test modules against round 1's `skills/`, `docs/` and READMEs | 131 failed, all of them new cases; restored to the target afterwards |
| The citation predicate and the arm's predicate over eight shapes, in a one-run probe file, since deleted | five disagree, three agree |
| `bin/evidence-check --strict --ledger` on this item's fragment | exit 0, 114 ok, 0 drifted, 0 broken |
| ruff check and ruff format --check on the four changed Python files | exit 0, clean and already formatted |
| `git grep` for a rounds or phases path over released SDD files at `e141980a` | 381 lines, 157 files, 51 items; 331 relative only |
| First release tag per item at `e141980a`, and any process-record change after it | 55 of 55 tagged, 0 changed |
| The full suite, lint and typecheck (the broad gate) | not yet; it is the sealer's, and with nothing open it has come due |

### The red run against round 1

```
   2 tests/test_settle_reads_before_it_removes.py::test_both_cheat_sheets_carry_the_command
 122 tests/test_settle_retires_the_process_record.py::test_a_citation_into_a_taken_file_is_read_whatever_follows_it
   1 tests/test_settle_retires_the_process_record.py::test_a_citation_written_as_prose_is_listed
   4 tests/test_settle_retires_the_process_record.py::test_no_carrier_says_nothing_reads_the_process_record
   1 tests/test_settle_retires_the_process_record.py::test_the_design_records_dated_section_says_no_check_reads_it
   1 tests/test_settle_retires_the_process_record.py::test_the_fold_reads_a_reference_into_the_process_record_at_the_tag
```

### ⬜ 1

```
rest='pr..md'                 entry='pr..md'         dir=False listed=False taken=True  DISAGREE
rest='pr.zh+hant.md'          entry='pr.zh+hant.md'  dir=False listed=False taken=True  DISAGREE
rest='survivors.md_'          entry='survivors.md'   dir=False listed=False taken=True  DISAGREE
rest='survivors.md/notes.md'  entry='survivors.md'   dir=True  listed=True  taken=False DISAGREE
rest='rounds'                 entry='rounds'         dir=False listed=True  taken=False DISAGREE
rest='rounds.'                entry='rounds'         dir=True  listed=True  taken=True  AGREE
rest=''                       entry=''               dir=False listed=False taken=False AGREE
rest='pr.md'                  entry='pr.md'          dir=False listed=True  taken=True  AGREE
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Paste-ready fixes

None of these is owed, since every finding is ⬜. They are here so that the
smith can take one rather than describe it.

### ⬜ 1

`skills/settle/scripts/settle.py`, the last sentences of
`cites_a_process_record`'s docstring:

```python
    `PROCESS_DIRS` names the directory, with a slash after it or none. The
    answer is `is_process_record`'s for every name `CITED_NAME_RE` reads
    whole. A `pr.*.md` whose middle holds a character outside that pattern,
    or a name closed by an italic `_`, is read short and not listed, and a
    directory spelled like a file on `PROCESS_FILES` is listed although the
    arm keeps it; the tree holds none of these. An empty name is on neither
    list."""
```

### ⬜ 2

`docs/one-root-by-lifetime.md:726`, the end of the third cell:

```markdown
and on 2026-10-04 the process record was 525 of the 841 files under `seal/specs/` and 67% of the bytes, kept with no check reading it
```

`docs/one-root-by-lifetime.ko.md:698`, the same place:

```markdown
2026-10-04 에는 `seal/specs/` 아래 파일 841 개 가운데 525 개, 바이트로는 67% 가 어느 검사도 읽지 않는 채 남아 있었습니다
```

`skills/settle/scripts/settle.py:1195`:

```python
# What a work item's directory holds for its pull request, and no check reads
# after its release: the round records and the reviewer's reports, the phase
```

### ⬜ 3

`skills/settle/SKILL.md`, fold step 1, replacing the sentence at lines 204-206:

```markdown
Where a released item's SDD set cites one of its own round or phase records,
`settle --retire-process` may already have taken it. Read it as it stood
before the removal: `git show "$(git log -1 --format=%h --diff-filter=D -- <path>)^:<path>"`.
That needs no release tag, and it is the last version the tree held.
```

### ⬜ 4

`skills/settle/SKILL.md:118-119`:

```markdown
`rounds/round-N.md` and `phases/phase-N.md` by relative path. Measured when
this arm shipped, 381 lines in 157 of those files named a `rounds/` or
`phases/` path, 331 of them by a relative one, across 51 items. The
```

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files I opened at `dc01bbb9`: the round paragraph handed to this round; this
item's `rounds/round-1.md` and `rounds/round-1-report.md`; the fix-range diff
of `skills/settle/SKILL.md`, `skills/settle/scripts/settle.py`,
`skills/code-review/scripts/survivor_check.py`, `docs/the-record-layout.md`,
`docs/release-checklist.md`, `docs/one-root-by-lifetime.md` and its Korean
edition, both READMEs, the item's `changelog.md` and `overview.md`, and both
test modules. I also read `settle.py` lines 850-935 (`CITATION_RE`,
`tracked_text`, `citations`), 1188-1345 (the process lists,
`is_process_record`, `process_plan`, `taken_by`, `process_anchored`) and
1425-1445 (the call into `citations`), and
`tests/test_settle_retires_the_process_record.py` lines 340-380 and 520-580.
Further reads: `docs/one-root-by-lifetime.md` lines 155-175 and its section
headings, `skills/settle/SKILL.md`'s headings, the branch's whole added-line
diff outside the frame and the ledger fragment, and the ledger fragment's rows
that a grep returned. `bin/test`'s header was read in the scratch clone.
