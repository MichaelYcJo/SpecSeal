# 1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row — review round 3

| Field | Value |
|---|---|
| Target SHA | b1673a3f796fe7f9c7e8d8ad3c741dd92caaa783 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 208 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, spawned against `b1673a3` with the fix diff `f434c9c..c19766f`, and
told in its first paragraph that **this record ends the run**: round 1 met the
floor, round 2 was the one reopening `docs/review-chain-spec.md` allows, and the
record that reads its fixes ends the run whatever it finds. So the prompt asked
it not to open a thread it could not finish reading, and to give issue-shaped
grounds for anything it did open, because that is where those were going.

It carried two facts to test rather than take. The fix pass had **corrected
round 2's own number** — three of three flipped records turn on the comment arm,
not two, and the fence arm flips none — and it had **found two more instances of
the run's dominant class after being told to assume a fourth**, one of them not a
sleeping branch: widening `swallowed`'s row loop back to `READ_HEADINGS` makes a
paste-ready fix containing a markdown table read as hidden rows and be refused,
and this repository's paste-ready fixes contain tables.

Six axes: the three new units against what they guard; the parametrised case
asked whether a third reader pass actually fails it or is silently uncovered;
the `Contract changes` row; the three sentence carriers checked against the tree
rather than read, because this branch had already produced two false figures in
records; `overview.md`'s render row marked answered rather than deleted, and the
argument for that; and the ledger read unscoped.

It was asked whether there was a seventh instance of the class. There was, in
the function the previous fix pass had parametrized in order to enumerate its
arms.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 `reader()` has ~~four~~ FIVE failure paths and the enumeration pinned two; ~~`SyntaxError` is a live arm no case watches~~ **`SyntaxError` and `ImportError` are two live arms no case watches**, and R5 wrote the count down as two | `hooks/review-history-guard.py:101` | deferred #209 | #209 — **corrected 2026-09-08 by work item 1788844300 at `b8471fb`, which enumerated the arms out of the function's own source rather than reading them: `except (OSError, ImportError, SyntaxError)` has three members, so the function has five arms and four of them are reachable. Both unwatched arms have a parameter now** |
| 2 | ⬜ `HIDDEN_CLOSING_WORD` is a class over two literals, not over the reader's passes | `tests/test_chain_hooks.py:434` | deferred #210 | #210 |
| 3 | ⬜ the `REQUIRED_HEADINGS` correction reached F3 and R3 and missed F1 and `overview.md` | `seal/ledger.md:1183` | answered | corrected at `b73bdd3` — `seal/ledger.md` F1's parenthetical and its re-read sentence now name `REQUIRED_HEADINGS`, and `overview.md`'s R3 bullet reads as corrected by R4. A finding located in a record is a correction and owes no fix pass |
| 4 | ⬜ two carriers say all three flipped records hide the word in a header comment; one is a body comment seventeen lines in | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/changelog.md:68` | answered | corrected at `b73bdd3` — the changelog fragment and ledger R5 now say an HTML comment the round wrote to narrate itself, two of them the header comment and the third a note beside the field table |
| 5 | ⬜ round 2's finding 4 grounds claim an assertion of `chain_module`'s absence that does not exist | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/rounds/round-2.md:62` | answered | corrected at `b73bdd3` — `rounds/round-2.md`'s grounds cell no longer claims an assertion nothing makes, and says what is true instead. NAME NOT IN TREE: the name this row is about is gone, and the cell it corrected carries the same marker |
| 6 | ❓ `Contract changes` reads `no call site found` for a pytest test function, where `pytest only` is the value that exists for it | out of verified scope | deferred #211 | #211 |
| 7 | ✅ round 2's 🟡 1 — the comment arm observed by no case | `hooks/review-history-guard.py:130` | answered | executed: swapping `readable` for `blank_fences` turns 1 red, for `strip_comments` turns 3 red. 127 records, 3 flip, 3 of 3 on the comment arm, 0 on the fence arm, all 3 with live Deferred rows |
| 8 | ✅ round 2's ⬜ 2 — the carriers described the fence half only | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/changelog.md:57` | answered | read: all three carriers now name both arms and say which one moves real records |
| 9 | ✅ round 2's ⬜ 3 — `overview.md`'s render row | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/overview.md:24` | answered | executed: the mark is `unverified_check.CLOSED`, so the row counts closed and the total is unchanged — `3 open · 1 closed`, exit 0 |
| 10 | ✅ round 2's ⬜ 4 — `chain_module` a one-line alias | `tests/test_the_record_is_generated.py:64` | answered | executed: the name is gone — NAME NOT IN TREE — and `check_module()` has nine call sites, 147 passed |

## Paste-ready fixes

no paste-ready fix in the report

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_chain_hooks.py tests/test_the_record_is_generated.py tests/test_the_fixes_close_the_record.py -q` in a `--no-local` clone at `b1673a3` | exit 0 — 147 passed |
| `./bin/evidence-check .` unscoped at `b1673a3` | exit 0 — 743 ok · 0 drifted · 0 broken · 0 external · 0 old-format |
| `is_closed` over all 127 committed round records under four readings — raw, fence-only, comment-only, `readable` | 110 closed raw, 107 closed readable; 3 flip; 0 under the fence arm alone, 3 under the comment arm alone; all 3 carry live Deferred rows |
| six mutations, one per arm | ~~4 red, 2 green — `spec.loader is None` and `SyntaxError`~~ **corrected 2026-09-08 by work item 1788844300 at `b8471fb`: the six did not include `ImportError`, which the round counted as one of two members of the except tuple rather than three. Re-executed against this module as it stood at `c3c22c2`, `reader`'s five arms give 2 red — `spec is None`, `except OSError` — and 3 green — `spec.loader is None`, `ImportError`, `SyntaxError`; deleting `ImportError` leaves 27 passed, exit 0, the same reading `SyntaxError` gives. That is also why the count below says four arms where the function has five** |
| a third blanking pass added to `readable`, then the module run | green — 27 passed; a closing word inside an inline code span reads as hidden |
| `reader()` at a `.py` file containing `def (`, with and without `SyntaxError` in the tuple | `None`, then raised `SyntaxError: invalid syntax` |
| `spec_from_file_location` against a directory, a `.txt`, an extensionless file, a missing `.py` | spec None for the first three; a loader for the missing path |
| `./bin/unverified-check` on the work item's `overview.md` | exit 0 — 3 open · 1 closed |
| `grep -rn chain_module` over the tree | 2 hits, both inside the round records |
| `git log -S` on F1's and F3's correction text | F1 at `ca799b7`; F3 corrected at `b466cde`; `overview.md`'s R3 bullet at `e8adc2a` |

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
| round-2 | `hooks/review-history-guard.py:130` | round 2's 1 — fixed |
| round-2 | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/changelog.md:57` | round 2's 2 — fixed |
| round-2 | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/overview.md:24` | round 2's 3 — fixed |
| round-2 | `tests/test_the_record_is_generated.py:64` | round 2's 4 — fixed |
| round-2 | `skills/code-review/scripts/round_record.py:398` | round 2's 5 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:461` | round 2's 6 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:770` | round 2's 7 — answered |
| round-2 | `skills/code-review/scripts/round_record.py:1848` | round 2's 9 — answered |
| round-2 | `tests/test_the_record_is_generated.py:1619` | round 2's 11 — answered |
| round-2 | `hooks/review-history-guard.py:129` | round 2's 12 — answered |
| round-2 | `agents/warden.md:278` | round 2's 13 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the `Contract changes` row for a pytest test function | #211 | the session that takes it |
