# 1788844300-the-guards-cases-cannot-observe-what-they-guard — review round 3

| Field | Value |
|---|---|
| Target SHA | a495e4f |
| Ran by | warden on claude-opus-5 |
| PR | 260 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

A verifying round, spawned after round 2's fixes were committed and targeted at
the diff of those fixes: `7c77397..54d614a`, plus `a495e4f`, which only closes
round 2's record. Its job was stated as round 2's answers rather than new
findings, with one surface exempt — what round 2's fixes themselves created.
The cap's last round, and it was told so.

Five checks, in the order the prompt set them.

1. **Does the planted case close the class it claims?** Round 2's paste-ready
   fix was a parametrized case over `gh_segments`' three session-stopping arms.
   The round was asked to verify by mutation that it goes red on each arm in
   turn, that the parameters split by arm the way its docstring claims, and
   that each input actually reaches the arm rather than standing beside it —
   the shape a sibling branch found. With the `.pyc` warning attached: bytecode
   keys on source mtime in whole seconds plus size, so mutations of equal
   length inside one second reuse the earlier bytecode.
2. **Are the three carriers of the false ground now true?** Round 2 found the
   sentence *`except ValueError` is the only survivor whose failure stops a
   session* in the ledger fragment's T4, in `overview.md` and in issue #262's
   body. Each was to be judged against the tree as it now stands, including
   whether the arithmetic is self-consistent — the counts had moved and more
   than one denominator was in play.
3. **Is T5 a claim the evidence supports?** The fix pass added a ledger row for
   the new case and stamped it with a `--reverify` that touched one row. Its
   anchors, its figures and its Notes were to be measured rather than read,
   including its claim that four of `gh_segments`' six branch decisions are now
   red and two still green.
4. **The two smaller corrections** — T4's count moved thirteen to twelve, and
   `seal/ledger.md` R5's `Checked` column moved to the 8th. For R5, whether the
   date is the date somebody actually re-read the code.
5. **One declared deviation.** The new case's docstring was made a raw string
   so the `\n` it names reads as `\n` rather than being interpreted. Nothing
   else in the reviewer's paste was changed. The round was asked to judge it.

Carried as not the round's to close: the records-arm refusals against round 1's
own report and record, which the orchestrator takes at the closing commit as an
annotation and never as a rewrite of what a reviewer concluded; `docs/flow.md`'s
box for this branch; and the broad gate, which is the orchestrator's under
contract §2.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | ⬜ T4's Notes say twelve watched by nothing, three closed here, and eleven remaining — twelve minus three is nine, and the base measures thirteen | `seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md:6` | deferred #264 | #264 |
| 2 | ⬜ issue #262's arm table sums to ten where its title, its prose and `overview.md` say nine, because the row's arm count and its unwatched count come from different enumerations | issue #262, the arm table | deferred #264 | #264 |
| 3 | ⬜ the branch closed four of `gh_segments`' decisions, not three — `basename(…) == "gh"` too — and both prose carriers subtract three from the deferred list | issue #262 · `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md:77` | deferred #264 | #264 |
| 4 | ⬜ the `FOO=bar` parameter is called an empty-segment one in the case's docstring and twice in T5, and its coverage of the guards runs through an arm #262 leaves open | `tests/test_chain_hooks.py:330` · `seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md:7` | deferred #264 | #264 |
| 5 | ⬜ `overview.md`'s closing memo still says T1–T3, 30 passed, and four arms of which two raise | `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md:14` | deferred #264 | #264 |
| 6 | round 2's 🟡 1 — `except ValueError` was not the only survivor whose failure stops a session | `hooks/review-history-guard.py:176` | answered | executed: the case is planted and red on each of the three arms in turn — `except ValueError` fails the two quoted-pipe parameters, either `i < len(toks)` fails the other three, each leaving 35 green; every parameter's input reaches its arm, traced through `SEG_RE` and `shlex`; the hook exits 1 with `IndexError` on three ordinary payloads with either guard removed. Residuals are findings 1–4 |
| 7 | round 2's ⬜ 2 — T4's count, thirteen where the other carriers give twelve | `seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md:6` | answered | the edit landed; measured, it moved the wrong way and left the row's other number untouched. Carried forward as finding 1 |
| 8 | round 2's ⬜ 3 — R5's `Checked` column against a 2026-09-08 re-verification | `seal/ledger.md:1385` | answered | read: the cell reads `2026-09-08`, and round 2 re-read the anchored case that day and recorded that its claim holds under `504b6136`. The date is a date somebody read the code, not a date typed to satisfy the column |

## Paste-ready fixes

```
seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md — T4,
findings 1 and 3 together. Two edits to the Notes cell.

The base, which the five-way enumeration in the same sentence gives as 5 + 8:

-  gives `gh_segments` five arms and `main` nineteen, and twelve of those
-  were watched by nothing.
+  gives `gh_segments` five arms and `main` nineteen, and thirteen of those
+  were watched by nothing — every one of `gh_segments`' own, measured with
+  this branch's two `gh` cases deselected.

and the remainder, four of the thirteen having been closed here:

-  The remaining eleven arms are deferred to #262 rather than pinned one by
-  one
+  The remaining nine arms are deferred to #262 rather than pinned one by
+  one
```
```
seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md — T5,
finding 4. Two edits: the Executed cell, then the Notes.

-  deleting either `i < len(toks)` fails the three empty-segment ones, each
-  leaving 35 green
+  deleting either `i < len(toks)` fails the other three, each leaving 35
+  green — two of them leave a segment whose token list is empty, and
+  `FOO=bar` leaves one token the env-assignment prefix arm consumes, so `i`
+  reaches `len(toks)` either way

-  The case closed `basename(…) == "gh"` as a by-product — the two parameters
-  expecting `[]` watch it — which leaves `gh_segments` with two unwatched
-  arms, and those stay with #262
+  The case closed `basename(…) == "gh"` as a by-product — `echo hi;` watches
+  it, and `FOO=bar` does not, because the prefix arm has already left
+  `i == len(toks)` and the widened test is False either way — which leaves
+  `gh_segments` with one unwatched arm under round 1's five-way enumeration,
+  two under the six-way split this cell uses, and it stays with #262
```
```python
# tests/test_chain_hooks.py:328-331 — finding 4, the docstring's second
# paragraph. `FOO=bar` is one token, not an empty segment, and it is worth
# saying which arm carries it there.

    The parameters are grouped by arm, so a mutation says which one went:
    the two quoted-pipe commands are the `except ValueError` arm, and the
    other three are the index guards. Two of those leave a segment whose
    token list is empty; `FOO=bar` leaves one token, which the
    env-assignment prefix arm consumes, so `i` reaches `len(toks)` by the
    other route. Contract §12 — the finding named one instance and the cause
    produces three.
```
```
Issue #262 — findings 2 and 3. The table row, and two sentences.

The row, so that its unwatched count uses the same enumeration as its arm
count (the whole prefix-skip loop taken as one boolean member is green, at
38 passed exit 0):

-  | `gh_segments` | 5 | 2 |
+  | `gh_segments` | 5 | 1 |

The count of what the branch closed, which is four decisions of which three
stop a session:

-  Three of the fourteen are closed on the branch for #209 · #210, all in
-  `gh_segments` and all under one parametrized case: `except ValueError` and
-  the two `i < len(toks)` index guards.
+  Four of the fourteen are closed on the branch for #209 · #210, all in
+  `gh_segments` and all under one parametrized case: `except ValueError`,
+  the two `i < len(toks)` index guards, and `basename(…) == "gh"` as a
+  by-product. The first three are the ones whose failure stops a session's
+  Bash call rather than misfiling a reminder.

and the paragraph under `What is left`, so that two in `gh_segments` is not
subtracted from a table that gives one:

-  Nine arms. Two of them are in `gh_segments` — the env-assignment prefix arm
-  and the `WRAPPERS` arm, both measured green again at round 3 with every
-  other arm of that function now red — and the rest are in `main`.
+  Nine arms. One of them is in `gh_segments` — the prefix-skip loop, whose
+  env-assignment half and `WRAPPERS` half were both measured green again at
+  round 3 with every other decision of that function now red — and the other
+  eight are in `main`.
```
```
seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md
— finding 3, the `Not done` paragraph at :77. One sentence, to match #262.

-  Three of the fourteen
-  survivors are fixed here, all in `gh_segments` and all under one parametrized
-  case: `except ValueError`, and the two `i < len(toks)` index guards. Those are
-  the three whose failure stops a session's Bash call rather than misfiling a
-  reminder
+  Four of the fourteen
+  survivors are fixed here, all in `gh_segments` and all under one parametrized
+  case: `except ValueError`, the two `i < len(toks)` index guards, and
+  `basename(…) == "gh"` as a by-product. The first three are the ones whose
+  failure stops a session's Bash call rather than misfiling a reminder
```
```
seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md
— finding 5, the closing memo, IF the orchestrator reads a memo as maintained.
Three lines, at :14, :17 and :35.

-  · evidence: `seal/ledger/1788844300-…` T1, T2, T3 — added
+  · evidence: `seal/ledger/1788844300-…` T1, T2, T3 — added; T4 and T5 added
+              by round 1's and round 2's fix passes

-  · verified: EXECUTED — `bin/test tests/test_chain_hooks.py -q`, 30 passed at
-              `57e9603`
+  · verified: EXECUTED — `bin/test tests/test_chain_hooks.py -q`, 30 passed at
+              `57e9603`, and 38 passed at the reviewed head

-  Four arms of the pre-merge guard could have been deleted without a single case
-  going red, and two of them would have raised out of a `PostToolUse` hook into
-  somebody's Bash call
+  Seven arms of the pre-merge guard could have been deleted without a single
+  case going red — four found by the implementation pass and three more by the
+  review rounds — and five of them would have raised out of a `PostToolUse`
+  hook into somebody's Bash call
```

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_chain_hooks.py -q` in a `--no-local` clone at `a495e4f` | exit 0 — 38 passed |
| `gh_segments`' six branch decisions mutated one at a time, `__pycache__` cleared and the hook's mtime stamped a minute apart between each | 4 red — `except ValueError` (3 failed), each `i < len(toks)` (3 failed), `basename(…) == "gh"` (1 failed) — and 2 green at 38 passed, the env-assignment prefix arm and the `WRAPPERS` arm |
| the same six with the new parametrized case deselected | `except ValueError` alone red, failing round 1's case; **`while` guard, `if` guard and `== "gh"` all green at 33 passed** |
| the same six, plus the whole prefix-skip loop as one arm, with BOTH `gh` cases deselected | **all eight mutations green at 32 passed, exit 0** — before this branch, no case watched any decision of `gh_segments` |
| the whole prefix-skip loop removed as one arm, at the shipped tree | 38 passed, exit 0 — one unwatched arm under round 1's five-way enumeration |
| `SEG_RE.split` and `shlex.split` traced over each of the case's five parameters | the two quoted-pipe commands raise `No closing quotation` on 2 of 3 and 1 of 2 segments; `…comments\n` and `echo hi;` each leave a segment whose token list is `[]`; **`FOO=bar` leaves `['FOO=bar']`** and reaches the guards only after the env-assignment prefix arm advances `i` to 1 |
| the hook fed real `PostToolUse` payloads for five commands, as shipped and with each `i < len(toks)` removed in turn | exit 0 on all five as shipped; exit 1 with `IndexError: list index out of range` on `gh pr view 1 --json comments\n`, `echo hi;` and `FOO=bar` with either guard removed |
| `./bin/evidence-check --strict --ledger seal/ledger/1788844300-….md .` | fragment **11 ok · 0 drifted · 0 broken** — T5's two anchors resolve; exit 2 from the records arm alone, 4 refused · 1 drifted, the set carried as not this round's |
| `uvx ruff check` and `uvx ruff format --check` on `tests/test_chain_hooks.py` | exit 0 both — all checks passed, 1 file already formatted |
| `git rev-parse HEAD` and `git status --porcelain` before and after every mutation batch | `a495e4f38e59fc059a627890b00a65a4d4b2f201` throughout, working tree clean after each restore |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/review-history-guard.py:173` | round 1's 1 — fixed |
| round-1 | `tests/test_chain_hooks.py:515` | round 1's 2 — fixed |
| round-1 | `seal/ledger.md:1385` | round 1's 3 — fixed |
| round-1 | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/rounds/round-3.md:71` | round 1's 4 — answered |
| round-1 | `tests/test_chain_hooks.py:417` | round 1's 5 — fixed |
| round-1 | `tests/test_chain_hooks.py:563` | round 1's 6 — fixed |
| round-1 | `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md:43` | round 1's 7 — answered |
| round-1 | `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md:54` | round 1's 8 — answered |
| round-2 | `hooks/review-history-guard.py:176` | round 2's 1 — fixed |
| round-2 | `seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md:6` | round 2's 2 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the remaining unwatched arms of `main`, and the durable close that derives arms from source and mutates them | issue #262, already deferred by the branch | the orchestrator, or the work item #262 opens |
| whether `blank_fences` and `strip_comments` have unwatched arms of their own | `overview.md:54`, already deferred by the branch | the review orchestrator, or a follow-up work item |
| whether a work item's closing memo is swept after review fixes or stands as a snapshot of the implementation pass | finding 5 states both readings | the review orchestrator |
