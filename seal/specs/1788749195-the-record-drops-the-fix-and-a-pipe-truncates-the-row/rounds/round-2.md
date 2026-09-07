# 1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row — review round 2

| Field | Value |
|---|---|
| Target SHA | 5d270017e59f205f9b3d22335aa2e6535e35a131 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 208 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | test_the_guard_falls_back_to_the_raw_text_without_the_reader → no call site found |
| New units | HIDDEN_CLOSING_WORD (depth 1); test_a_closing_word_a_reader_blanks_is_not_a_closing_note (depth 1); test_a_paste_ready_fence_carrying_a_table_is_not_read_as_hidden_rows (depth 1) |
| Needs a fix | yes — 🟡 1, the hook's comment arm is pinned by no case and named by no sentence |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, the verifying round for round 1's ten findings, spawned against
`5d27001` with the fix diff `03c4d93..8078a31`.

**The prompt stated the bound rather than a round number**, as round 1's did:
round 1's floor row reads `no`, so this round is the one reopening the rule
allows — open nothing needing a fix and the run ends here; open something and
one fix pass follows, after which the record that reads it ends the run
whatever it finds.

It carried the orchestrator's own re-execution at `5d27001` on both repaired
shapes, and **the answer to round 1's ❓ 10, executed rather than reasoned**:
`gh api -X POST /markdown --mode gfm` over a table whose cell holds
`` `a \| = b` `` returns two `td` elements with the code span rendering a plain
pipe. That is the property the whole #189 arm assumes and no case had observed.

It also named one shape the orchestrator ran that is *not* repaired, and asked
the round to judge it rather than take it: a row supplying one more column than
the header under every reading is capped with the surplus in the last cell.

Four things the fix pass did beyond the patches were handed over with an
instruction attached rather than as facts — it deleted one of the reviewer's
four readings on a measurement, gathered the comment rule into one function
after finding the reviewer's per-call-site version unobservable, corrected the
sweep's own claim from *no-op on 125 records* to *no-op on 4120 rows and the 8
already-broken ones changed*, and caught itself twice mutating its own
assertions. **Re-derive each**, because a reading removed on a measurement is a
reading nothing observes if the measurement was wrong.

Five axes: every case the fix diff adds against what it guards, assuming a
third instance of the class the fix pass had already found twice inside its own
work; `Contract changes` and whether every place the changed contract reaches
was revisited; the hook's new relative-path reader and its fallback; the ledger
read unscoped; and the empty arm's trade.

The first axis is where the finding came from — the third instance was there.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 the reader's comment arm is observed by no case and named by no sentence — swapping `readable` for `blank_fences` leaves all 24 cases green, while that arm is what flips two of the 126 committed records | `hooks/review-history-guard.py:130` | **fixed** `c19766f` | fixed at c19766f — `` — and the number is corrected: **three of three** flipped records turn on the comment arm, not two, and the **fence arm flips none**. So the arm every sentence named moves no committed record and the arm nothing watched moves all of them. The case is written over the reader's passes as a parametrised class rather than over the one arm, because this is the third time the same inference — true of a required section, applied to an optional one — has produced a finding; executed: `is_closed` at base and HEAD over all 126 committed records, 3 flip and 2 on a header comment; the mutation left the module at 24 passed |
| 2 | ⬜ the changelog fragment and ledger R5 describe the fence half only, and the changelog ships to users | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/changelog.md:57` | **fixed** `c19766f` | fixed at c19766f — `` — the docstring, the changelog fragment and ledger R5 each name both arms and say which one moves real records; read; the same understatement as finding 1, in the two carriers a person meets |
| 3 | ⬜ `overview.md` still names the render question unanswered and owed to the orchestrator, where round 1's record has it answered and executed | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/overview.md:24` | **fixed** `c19766f` | fixed at c19766f — `` — `overview.md`'s render row is marked answered with what closed it rather than deleted, so the row count a check reads does not move in the same edit that verifies it; read at `5d27001`, where both files stand |
| 4 | ⬜ `chain_module` is a one-line alias for `check_module`, one call site against eight | `tests/test_the_record_is_generated.py:64` | **fixed** `c19766f` | fixed at c19766f — `` — `chain_module` deleted, its one call site on `check_module`, and the absence asserted; read |
| 5 | ✅ round 1's 🔴 1 — a comment pipe loses a column | `skills/code-review/scripts/round_record.py:398` | answered | executed: dropping `comments=True` from `raw_cells` turns 4 cases red; 0 rows in the corpus collapse below the reader's own split |
| 6 | ✅ round 1's 🟡 2 — span pipe plus bare pipe lands the Location in the Verdict cell | `skills/code-review/scripts/round_record.py:461` | answered | executed: dropping the cap turns its own case red; dropping `spans=True` turns 3 red |
| 7 | ✅ round 1's 🟡 3 — the swallow guard refused over an optional section | `skills/code-review/scripts/round_record.py:770` | answered | executed: widening back to `READ_HEADINGS` turns the new optional case red; the trade is stated in the constant, the docstring and R4 |
| 8 | ✅ round 1's 🟡 4 — three of four gate answers false | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/changelog.md:41` | answered | read; the re-measured claims match an independent sweep — 8 of 4126, the differing set identical to the over-wide set |
| 9 | ✅ round 1's 🟡 5 — `close`'s `row_cells` change observed by no case | `skills/code-review/scripts/round_record.py:1848` | answered | executed: reverting each of the two sites turns one new case red, a different one each time |
| 10 | ✅ round 1's 🟡 6 — the empty-arm sentence asserted against itself | `skills/code-review/scripts/round_record.py:157` | answered | executed: rewording `NO_PASTE_READY` now turns the new case red |
| 11 | ✅ round 1's 🟡 7 — three document pins passed on presence anywhere | `tests/test_the_record_is_generated.py:1619` | answered | executed: all three place-mutations red; the first protocol mutation was invalid and is withdrawn |
| 12 | ✅ round 1's 🟡 8 — a pasted fix read as a closing note | `hooks/review-history-guard.py:129` | answered | executed: dropping the reader consult turns 2 cases red. The fence half is pinned; the comment half is finding 1 |
| 13 | ✅ round 1's ⬜ 9 — *reads no other prose* was false | `agents/warden.md:278` | answered | executed: restoring either false spelling turns the case red, and it now asserts both |
| 14 | ✅ round 1's ❓ 10 — whether a `\|` renders as a pipe | out of verified scope | answered | carried from round 1's record, not re-derived: the orchestrator executed it against GitHub's renderer. `overview.md` is finding 3 |

## Paste-ready fixes

```python
# tests/test_chain_hooks.py — append beside the other three guard cases
def test_a_closing_word_inside_an_html_comment_is_not_a_closing_note(tmp_path):
    """The reader's OTHER arm, which nothing observed until this case.

    `readable` is `blank_fences(strip_comments(...))`, and it is
    `strip_comments` that does half the work in production: over this
    repository's 126 committed records the repair flips three from closed to
    not-closed, and in two of them the only closing word stands in the
    record's own header comment, which `blank_fences` alone keeps. Measured
    by swapping `readable` for `blank_fences` — all 24 cases of this module
    stayed green, so the arm that flips two real records rested on nothing.

    A record's header comment narrates the round. `It closed all five` is a
    sentence about findings, not a statement that the Deferred rows were
    drained, and the three records it silenced all have live rows."""
    guard = load_hook_module("review-history-guard.py", "guard_reads_comments")
    record = tmp_path / "round-1.md"
    record.write_text(
        "# round 1\n\n"
        "<!-- The verifying round for round 2's fixes. It closed all five. -->\n\n"
        "| Target SHA | abc |\n\n"
        "## Deferred\n\n"
        "| Finding | Where it went | Who answers it |\n|---|---|---|\n"
        "| the windows leg | nowhere yet | nobody |\n",
        encoding="utf-8",
    )
    assert guard.is_closed([str(record)]) is False
```
```python
# hooks/review-history-guard.py:108 — the first sentence of `is_closed`'s
# docstring names one of the reader's two arms, and the other is what flips
# two of this repository's own committed records.
    Read through the shared reader, so a closing word counts only where a
    reader would read it: not inside a fenced block, and not inside an HTML
    comment. Both arms are load-bearing — `blank_fences` is what a pasted
    fix needs, and `strip_comments` is what a record's header comment needs,
    which is where two of this repository's 126 committed records carry
    their only closing word. `## Paste-ready fixes` puts the reviewer's own
```

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_the_record_is_generated.py tests/test_the_fixes_close_the_record.py tests/test_chain_hooks.py -q` | 143 passed |
| `./bin/evidence-check .` unscoped at `5d27001` | exit 0 — 743 ok, 0 drifted, 0 broken, 0 external, 0 old-format |
| the four-reading shape against the three-reading one, over 4126 committed body rows and 2560 constructed rows | 0 disagreements; the removal is also provable — the span break set is a subset of the plain one |
| the branch sweep: re-serialisation against the verbatim line of `origin/release/v0.9.0`, over 4126 rows | differs on 8; the differing set is exactly the over-wide set |
| rows where `raw_cells` collapses below `reader.split_row` | 0 of 4126 |
| nine code mutations — `raw_cells` comments, reading 2's spans, reading 2's cap, `REQUIRED_HEADINGS`, both `close` sites, the reader consult, `NO_PASTE_READY`, `warden.md`'s prose | all red, each on its own case |
| four document-pin mutations — the heading out of `warden.md`'s fenced contract, the section to the end of `sdd-round.md`, the protocol row below the `####` boundary, the row deleted | all red |
| two fallback mutations — `reader()` never falls back, an unreadable record nags | both red on the fallback case |
| `readable` swapped for `blank_fences` in the hook | **green — 24 passed.** Finding 1 |
| `is_closed` at base and HEAD over all 126 committed round records | 3 flip closed to not-closed; all 3 have live `Deferred` rows |
| `new` end to end over six HTML-comment shapes | 3 write a record, all at header width; 2 refused naming the unclosed comment; 1 refused naming the row, writing nothing |
| `reader()` pointed at a non-Python file and at a directory | returns None both times, no raise |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:571` | round 1's 1 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:378` | round 1's 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:679` | round 1's 3 — fixed |
| round-1 | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/changelog.md:41` | round 1's 4 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1757` | round 1's 5 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:157` | round 1's 6 — fixed |
| round-1 | `tests/test_the_record_is_generated.py:1589` | round 1's 7 — fixed |
| round-1 | `hooks/review-history-guard.py:72` | round 1's 8 — fixed |
| round-1 | `agents/warden.md:279` | round 1's 9 — fixed |
| round-1 | out of verified scope | round 1's 10 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
