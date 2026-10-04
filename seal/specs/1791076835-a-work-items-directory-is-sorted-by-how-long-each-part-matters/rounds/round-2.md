# 1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters — review round 2

| Field | Value |
|---|---|
| Target SHA | dc01bbb95876534dcb8cf79462862e7802a6555f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #768 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `dc01bbb95876534dcb8cf79462862e7802a6555f..a14deb6b2a125e62572ce85a34eae7f40f66a5dc`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item `1791076835-a-work-items-directory-is-sorted-by-how-long-each-part-matters` (#729, PR #768). This is the verifying round for round 1's fixes, `597d3625..2fa080e3`.

Open each fix and judge whether its round-1 verdict is closed:

- 🟡1 took option (b). The arm section gained a paragraph saying the SDD set that stays still points into what left. Fold step 1 now says to read a cited record at the release tag. Every "nothing reads" sentence became "no check reads".
- 🟡2: `cites_a_process_record` reads the name in front of the path through `CITED_NAME_RE`, and it leaves the verdict to `is_process_record`.
- 🟡3: the README rows.
- ⬜4 was answered, with the trade written into `survivor_check.py`'s docstring.

The new units are a finding surface: `CITED_NAME_RE` and six test functions. The class 🟡1 named was enumerated by the fix pass. Check that enumeration for a "nothing reads" sentence it left standing, outside the frame and the dated 0.4.0 design body, which it left on purpose.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | The docstring says the citation listing and the removal cannot disagree about a name; they disagree on five shapes, three listing too little, none in the tree | `skills/settle/scripts/settle.py:1362` | answered | no change. The five name shapes on which the listing and the deletion part never occur in the tree: the reviewer counted none. Where they would part, the listing names more or less than is deleted, and nothing is lost. The docstring's claim covers the names the tree holds, and the 176-name construction case pins them. Narrowing the predicate now would commission a change no round reads, after a verifying round that opened nothing; executed: both predicates over eight shapes in a scratch probe, five disagree; read: the tree's one pull-request file is pr.ko.md and no citation follows a process name with an underscore or a dash |
| ⬜ 2 | The enumeration for round 1's finding 1 left three sentences saying the process record serves nobody after its release: the design record's corrects cell in both editions, and a comment in settle.py | `docs/one-root-by-lifetime.md:726` | answered | no change. `docs/one-root-by-lifetime.md:726` and its Korean twin's `:698` sit in the dated 0.4.0 design body, which round 1 left on purpose as a record of what was decided then. `settle.py:1195`'s "for its pull request and nothing after its release" states what the record is for, not who reads it; read and grepped by construction; the Korean edition is `docs/one-root-by-lifetime.ko.md:698` and the comment is `skills/settle/scripts/settle.py:1195`; the 0.4.0 body at line 168 was left on purpose; no case pins and no ledger row anchors any of the three |
| ⬜ 3 | The procedure names the release tag a cited record resolves at without saying how to find it | `skills/settle/SKILL.md:204` | answered | no change. `git show v<X.Y.Z>:<path>` is the documented route, and the reviewer measured that all 55 released items have their tag, with no cited file changed since. The parent-of-deletion route is an alternative, not a correction; executed: 55 of 55 items have a tag holding their process record unchanged; read: no step says how to find it |
| ⬜ 4 | The 381-line figure counts every rounds or phases path, while the sentence says it counts the item's own records named by relative path | `skills/settle/SKILL.md:119` | answered | no change. The 381 lines count every staying line that points into the process record. 331 of them are relative paths and 281 name a round or phase. The sentence's "point into what left" holds for all 381; executed: 381 reproduced with the wider pattern; 331 relative only, 281 naming a round or phase file |
| 🟢 | round 1's finding 1 is closed — the arm section and fold step 1 say where a reference from the SDD set resolves, and the four carriers say no check reads it | `skills/settle/SKILL.md:116` | confirmed | executed: the fold-step, carrier and dated-section cases red against round 1's docs and green at the target; the residue of the class is this round's ⬜ 2, which needs no fix |
| 🟢 | round 1's finding 2 is closed — a citation ending in punctuation, a line number or an anchor, or naming rounds with no slash, is listed | `skills/settle/scripts/settle.py:1354` | confirmed | executed: 123 red against round 1's predicate, all green at the target; controls green at both |
| 🟢 | round 1's finding 3 is closed — both README cheat-sheet rows name the process arm | `README.md:288` | confirmed | executed: the new assertion red against round 1's READMEs in both editions, green at the target; `README.ko.md:280` read |
| 🟢 | round 1's finding 4 is answered — the trade is written where the filter lives | `skills/code-review/scripts/survivor_check.py:344` | confirmed | read; round 1's base-against-target execution carried, since nothing it ran moved in the fix range |
| 🟢 | The fix range's three narrow modules pass at the target | `tests/test_settle_retires_the_process_record.py` | confirmed | executed: 506 passed |

## Paste-ready fixes

```python
    `PROCESS_DIRS` names the directory, with a slash after it or none. The
    answer is `is_process_record`'s for every name `CITED_NAME_RE` reads
    whole. A `pr.*.md` whose middle holds a character outside that pattern,
    or a name closed by an italic `_`, is read short and not listed, and a
    directory spelled like a file on `PROCESS_FILES` is listed although the
    arm keeps it; the tree holds none of these. An empty name is on neither
    list."""
```
```markdown
and on 2026-10-04 the process record was 525 of the 841 files under `seal/specs/` and 67% of the bytes, kept with no check reading it
```
```markdown
2026-10-04 에는 `seal/specs/` 아래 파일 841 개 가운데 525 개, 바이트로는 67% 가 어느 검사도 읽지 않는 채 남아 있었습니다
```
```python
# What a work item's directory holds for its pull request, and no check reads
# after its release: the round records and the reviewer's reports, the phase
```
```markdown
Where a released item's SDD set cites one of its own round or phase records,
`settle --retire-process` may already have taken it. Read it as it stood
before the removal: `git show "$(git log -1 --format=%h --diff-filter=D -- <path>)^:<path>"`.
That needs no release tag, and it is the last version the tree held.
```
```markdown
`rounds/round-N.md` and `phases/phase-N.md` by relative path. Measured when
this arm shipped, 381 lines in 157 of those files named a `rounds/` or
`phases/` path, 331 of them by a relative one, across 51 items. The
```

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

```
   2 tests/test_settle_reads_before_it_removes.py::test_both_cheat_sheets_carry_the_command
 122 tests/test_settle_retires_the_process_record.py::test_a_citation_into_a_taken_file_is_read_whatever_follows_it
   1 tests/test_settle_retires_the_process_record.py::test_a_citation_written_as_prose_is_listed
   4 tests/test_settle_retires_the_process_record.py::test_no_carrier_says_nothing_reads_the_process_record
   1 tests/test_settle_retires_the_process_record.py::test_the_design_records_dated_section_says_no_check_reads_it
   1 tests/test_settle_retires_the_process_record.py::test_the_fold_reads_a_reference_into_the_process_record_at_the_tag
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/settle/SKILL.md:110` | round 1's 🟡 1 — fixed |
| round-1 | `skills/settle/scripts/settle.py:1347` | round 1's 🟡 2 — fixed |
| round-1 | `README.md:288` | round 1's 🟡 3 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:1452` | round 1's ⬜ 4 — answered |
| round-1 | `skills/settle/scripts/settle.py:1381` | round 1's 🟢 — confirmed |
| round-1 | `tests/conftest.py` | round 1's 🟢 — confirmed |
| round-1 | `skills/code-review/scripts/survivor_check.py:928` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
