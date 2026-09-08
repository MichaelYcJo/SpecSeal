# 1788844300-the-guards-cases-cannot-observe-what-they-guard — review round 2

| Field | Value |
|---|---|
| Target SHA | 600a9fc7f1bc5aa3733e9dd2ec966cac8cd9da8b |
| Ran by | warden on claude-opus-5 |
| PR | 260 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — finding 1, the ground that sent two more session-stopping arms into the deferred eleven, carried by a ledger row, `overview.md` and issue #262 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

A verifying round, spawned after round 1's fixes were committed and targeted at
the diff of those fixes: `9b1efa2..d7dce3d`. Its job was stated as the answers
rather than new findings, with one surface exempt — what the fixes themselves
created.

Six checks, in the order the prompt set them.

1. **One arm pinned and eleven sent to an issue — judge the split.** Round 1
   named twelve unwatched arms. The fix pass pinned the one whose failure stops
   a session and deferred the rest to #262, on the grounds that eleven
   hand-written cases close today's list and not the class, which is the same
   failure #210 is about one level down. The round was asked whether the one
   kept is the right one and whether #262's scope is the class rather than a
   longer list.
2. **The tie, re-running round 1's own probe** — a third pass as a module
   function, the same blanking written inline as a substitution (round 1
   measured 30 passed exit 0 there), and a rename.
3. **The tie's failure message**, read as somebody who has just renamed a pass,
   asking whether it now names a repair that works.
4. **The three new units**, checked for the shape a sibling branch found: a
   case whose input never reaches the thing it claims to pin.
5. **Two `answered` rows**, and whether the corrected mutation tally holds
   against the module as it stood at that commit.
6. **The one row the orchestrator closed itself** — the drifted ledger anchor,
   re-verified at `d7dce3d` to `504b6136`, which is the value the fix pass had
   independently computed after the permission classifier blocked `--reverify`
   twice. The round was asked to verify the row's claim still holds under its
   new hash, because a re-verification that stamps a claim which has stopped
   being true is worse than a drifted row.

Carried as not the round's to close: the records-arm refusals against round 1's
own report and record, which the orchestrator takes at the closing commit. The
round was asked to say so if its own report widened the class.

Facts carried as executed by the orchestrator: the module at 30 passed exit 0
and ruff clean at round 1's target; at `d7dce3d` the unscoped total 909 ok ·
0 drifted · 0 broken, with the exit 2 coming entirely from the records arm.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 `except ValueError` is not the only survivor whose failure stops a session — two `gh_segments` index guards do too, on a command ending in a newline, and both sit in the deferred eleven that three carriers call arms which "misfile a reminder rather than stopping anything" | `hooks/review-history-guard.py:176` | open | executed: deleting either `i < len(toks)` leaves this module at 33 passed, exit 0, and makes the hook exit 1 with `IndexError` on four ordinary payloads including a plain multi-line command. Contract §12 — one input class, one case; the parametrized case below is green at 38 passed and red on each of the three arms in turn |
| 2 | ⬜ T4 says thirteen arms watched by nothing where #262's own table and round 1 both give twelve, and thirteen minus the one closed here is not the eleven the rest of the row is written against | `seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md:6` | open | read: #262's table is 4 plus 8; round 1's finding 1 says twelve. `thirteen` is round 1's count of red mutations, not of unwatched arms. A ledger fragment, so a correction rather than a fix |
| 3 | ⬜ R5's anchor was re-verified 2026-09-08 and its `Checked` column still reads 2026-09-07, which round 1's own paste-ready fix asked to move | `seal/ledger.md:1385` | open | read: `--reverify` rewrites the hash cell alone, so the date is the writer's half and it was not written. `CLAUDE.md` makes that column the date somebody read the code. A ledger location, so a correction rather than a fix |
| 4 | round 1's 🟡 1 — `gh_segments`' `except ValueError` | `hooks/review-history-guard.py:173` | answered | executed: deleting the arm fails the new case alone, 32 green, and `shlex` raises `No closing quotation` on the segments the case feeds — the input reaches the arm |
| 5 | round 1's 🟡 2 — the tie could not see a pass written as a substitution | `tests/test_chain_hooks.py:515` | answered | executed: round 1's own control is now red. The same blanking written inline gave 30 passed exit 0 for round 1 and gives 2 failed / 31 passed here, refused by name; deleting the refusal fails the new case alone |
| 6 | round 1's ⬜ 3 — R5's drifted anchor | `seal/ledger.md:1385` | answered | read: the anchored case still removes the guarantee, still asserts the raw-text fallback rather than a raise, and now carries one parameter per reachable arm — four, which is what the corrected sentence claims. The claim holds under `504b6136`. Residual is finding 3 |
| 7 | round 1's ⬜ 4 — the corrected mutation tally | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/rounds/round-3.md:71` | answered | executed at `c3c22c2`, 27 passed baseline: 2 red — `spec is None`, `except OSError` — and 3 green — `spec.loader is None`, `ImportError`, `SyntaxError`. The corrected figures and the named members are right |
| 8 | round 1's ⬜ 5 — the loader sweep stated universally | `tests/test_chain_hooks.py:417` | answered | read: the docstring now gives the loop-`else` reason as the argument and the 21 inputs as corroboration, names the suffix list as per-platform and points at contract §13; `overview.md` carries both halves |
| 9 | round 1's ⬜ 6 — the tie's message prescribed the wrong repair for a rename | `tests/test_chain_hooks.py:563` | answered | executed: after a rename, re-keying the entry as the message now says gives 33 passed exit 0, while adding a key leaves 3 failed. Cutting the rename half back out fails the new case alone |
| 10 | round 1's ⬜ 7 — SHAs a clone cannot open | `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md:43` | answered | executed: `c7fe663` and `6de1bca` are not valid object names in a fresh clone; `341be0b`, `70c272c`, `701d109` resolve, and following the file's history gives exactly those three |
| 11 | round 1's ⬜ 8 — the deferred arm counts for the reader's own passes | `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md:54` | answered | unchanged and still deferred; the module has its own test file and this round did not widen into it |

## Paste-ready fixes

```python
# tests/test_chain_hooks.py — finding 1, a sibling of the case the fix pass
# added, beside it. One input class, one assertion, three arms.
#
# Executed in a clone at 600a9fc: 38 passed exit 0 as shipped. Deleting
# `except ValueError` fails the two quoted-pipe parameters; deleting either
# `i < len(toks)` fails the three empty-segment ones; each leaves the rest of
# the module green.


@pytest.mark.parametrize(
    "command,expected",
    [
        ("gh pr view 1 --json comments | jq '.c[] | .b'", ["gh pr view 1 --json comments"]),
        ("gh pr merge 1 --squash | tee it's-done.log", ["gh pr merge 1 --squash"]),
        ("gh pr view 1 --json comments\n", ["gh pr view 1 --json comments"]),
        ("echo hi;", []),
        ("FOO=bar", []),
    ],
)
def test_no_segment_of_a_bash_command_raises_out_of_gh_segments(command, expected):
    """`gh_segments`' THREE arms whose failure stops a session, not one.

    Round 2's 🟡 1. The fix pass closed `except ValueError` on the ground
    that it was the only survivor of round 1's enumeration whose failure
    leaves the hook — and the two `i < len(toks)` guards do the same, for a
    different input. `SEG_RE` splits on `\n` as well as on `|`, so ANY
    multi-line Bash command leaves a trailing empty segment whose token list
    is empty; both guards are what keeps `toks[i]` off it. Deleting either
    left this module at 33 passed, exit 0, while the hook fed a real
    PostToolUse payload exited 1 with `IndexError: list index out of range`
    — out of a hook and into the session's Bash call, the one thing this
    file's own docstring says must never happen.

    The parameters are grouped by arm, so a mutation says which one went:
    the two quoted-pipe commands are the `except ValueError` arm, and the
    three that reduce to an empty token list are the index guards. Contract
    §12 — the finding named one instance and the cause produces three."""
    guard = load_hook_module("review-history-guard.py", "guard_every_segment")
    assert guard.gh_segments(command) == expected
```
```
seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md — T4,
finding 1 and finding 2 together. Two edits to the Notes cell.

The count:

-  gives `gh_segments` five arms and `main` nineteen, and thirteen of those
-  were watched by nothing.
+  gives `gh_segments` five arms and `main` nineteen, and twelve of those
+  were watched by nothing.

and the ground:

-  This is the one whose failure STOPS a session rather than misfiling a
-  reminder, which is the floor `hooks/review-history-guard.py`'s own
-  docstring sets
+  This is one of THREE arms of `gh_segments` whose failure stops a session
+  rather than misfiling a reminder, which is the floor
+  `hooks/review-history-guard.py`'s own docstring sets. The other two are
+  the index guards `i < len(toks)` in the `while` and in the `if`: `SEG_RE`
+  splits on a newline, so any multi-line command leaves an empty segment
+  and an empty token list, and without either guard the hook exits 1 with
+  `IndexError` on an ordinary command. All three are covered by one
+  parametrized case rather than three
```
```
seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md
— finding 1, the `Not done` paragraph at :74. Two sentences.

-  One of the fourteen survivors is fixed here — `gh_segments`'
-  `except ValueError`, the only one whose failure stops a session's Bash call
-  — and two are behaviour-preserving.
-  The other eleven misfile a reminder rather than stopping anything, and
-  writing a case for each closes today's list and not the class.
+  Three of the fourteen survivors are fixed here, all in `gh_segments` and
+  all under one parametrized case: `except ValueError`, and the two
+  `i < len(toks)` index guards. Those are the three whose failure stops a
+  session's Bash call rather than misfiling a reminder — the index guards
+  because `SEG_RE` splits on a newline, so any multi-line command leaves an
+  empty token list for `toks[i]` to fall off. Two more survivors are
+  behaviour-preserving. The nine that remain misfile a reminder rather than
+  stopping anything, and writing a case for each closes today's list and
+  not the class.
```
```
Issue #262 — finding 1. The body's two false sentences, and its table.

-  One of the fourteen is closed on the branch for #209 · #210: `gh_segments`'
-  `except ValueError`, the only one whose failure stops a session's Bash call
-  rather than misfiling a reminder.
+  Three of the fourteen are closed on the branch for #209 · #210, all in
+  `gh_segments` and all under one parametrized case: `except ValueError` and
+  the two `i < len(toks)` index guards. Those are the three whose failure
+  stops a session's Bash call rather than misfiling a reminder. `SEG_RE`
+  splits on a newline, so any multi-line command leaves a segment with an
+  empty token list, and without either guard the hook exits 1 with
+  `IndexError` on an ordinary command.

-  | `gh_segments` | 5 | 4 |
+  | `gh_segments` | 5 | 2 |

-  Eleven arms.
+  Nine arms, all of them in `main`.

and the closing count `The other eleven` becomes `The other nine`.
```
```
seal/ledger.md:1385 — finding 3. R5's Checked column only; the anchor cell is
already right.

-  | 2026-09-07 |
+  | 2026-09-08 |

That is the fourth cell of the row, between the Executed cell ending
"— all red" and the Notes cell beginning "**The section is what made".
```

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_chain_hooks.py -q` in a `--no-local` clone at `600a9fc` | exit 0 — 33 passed |
| a third blanking pass added to `readable` as a module function, then the module run | RED — 2 failed, 31 passed |
| the identical blanking written inline as a substitution inside `readable`, then the module run | **RED — 2 failed, 31 passed**, `AssertionError: readable makes an attribute call this derivation cannot see: ['sub']`. Round 1 measured 30 passed exit 0 for the same mutation |
| a reader pass renamed, nothing else changed | RED — 2 failed, 31 passed, message naming both causes |
| the same rename, then the entry re-keyed as the message prescribes | **exit 0 — 33 passed** |
| the same rename, then a third key ADDED as the old message prescribed | RED — 3 failed, 31 passed |
| `except ValueError` deleted from `gh_segments`, module run | RED — `test_an_unbalanced_quote_in_a_piped_gh_command_does_not_stop_the_session` alone, 32 passed |
| the attribute-call refusal deleted from `reader_blanking_passes`, module run | RED — `test_a_blanking_pass_written_as_a_sub_is_refused_rather_than_unseen` alone, 32 passed |
| the rename half cut out of the tie's message, module run | RED — `test_the_ties_message_answers_a_rename_as_well_as_an_addition` alone, 32 passed |
| `shlex.split` over the segments `SEG_RE` gives for the two commands the new gh case feeds | 2 of 3 segments raise `No closing quotation` in the first, 1 of 2 in the second — the input reaches the arm |
| `gh_segments`' four remaining arms mutated one at a time, module run | all four green — 33 passed, exit 0; no case in the file watches any of them |
| the hook fed real `PostToolUse` payloads with each `i < len(toks)` deleted in turn | exit 1, `IndexError: list index out of range` on all four commands, including `gh pr view 1 --json comments` with a trailing newline and `echo hi;`; exit 0 on all four as shipped |
| the proposed parametrized case planted, then each of `gh_segments`' three crash arms deleted in turn | 38 passed exit 0 shipped; `except ValueError` fails the two quoted-pipe parameters, each `i < len(toks)` fails the three empty-segment ones |
| `reader`'s five arms mutated one at a time at `c3c22c2`, 27 passed baseline, in a worktree at that commit | 2 red — `spec is None`, `except OSError` — 3 green — `spec.loader is None`, `ImportError`, `SyntaxError` |
| `git cat-file -t` on the five SHAs `overview.md`'s divergence row has carried | `c7fe663`, `6de1bca` — `Not a valid object name`; `341be0b`, `70c272c`, `701d109` — commits |
| `git log --follow` over the other work item's round-3 record | exactly `341be0b`, `70c272c`, `701d109` and the correcting commit |
| `uvx ruff check` and `uvx ruff format --check` on `tests/test_chain_hooks.py` at `600a9fc` | exit 0 both |
| `git rev-parse HEAD` in the clone before and after every mutation batch | `600a9fc` throughout; working tree clean after each restore |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the remaining unwatched arms of `main`, and the durable close that derives arms from source and mutates them | issue #262, already deferred by the branch | the orchestrator, or the work item #262 opens |
| whether `blank_fences` and `strip_comments` have unwatched arms of their own | `overview.md:54`, already deferred by the branch | the review orchestrator, or a follow-up work item |
