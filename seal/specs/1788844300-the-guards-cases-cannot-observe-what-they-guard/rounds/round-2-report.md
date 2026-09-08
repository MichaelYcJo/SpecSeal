# 1788844300-the-guards-cases-cannot-observe-what-they-guard — round 2 report

Target `600a9fc7f1bc5aa3733e9dd2ec966cac8cd9da8b` · fix range `9b1efa2..d7dce3d`
· PR #260 · reviewed in a `git clone --no-local` at the target SHA. Verifying
round: the question is whether round 1's eight verdicts are actually closed,
and whether the three units the fixes created hold.

## The shape of what this round found

Every one of round 1's eight verdicts closes. I re-ran round 1's own three tie
scenarios and its arm tally, mutated each of the three new units, and read the
re-verified ledger row against the case it anchors. All of it holds.

What does not hold is one sentence beside the fix, and everything below follows
from it:

```
① round 1 found twelve unwatched arms in the guard's other two functions
       |  so the fix pass had to choose which to close today
② it kept `gh_segments`' `except ValueError` on the ground that it is the
   ONLY survivor whose failure stops a session's Bash call
       |  but
③ two more arms of the same function stop a session too, on commands as
   ordinary as one ending in a newline, and neither has a case
       |  so
④ three carriers — a ledger row, the overview, and issue #262 — describe the
   deferred eleven as arms that "misfile a reminder rather than stopping
   anything", which is false of two of them
```

The code is sound. What is wrong is the claim about what was left behind, and
one of the three places carrying it is a ledger row.

## 🟡 1 — two more arms of the same function stop a session, and both went into the deferred eleven

`hooks/review-history-guard.py:176`, and `:181` one line further down.

`gh_segments` walks a command's segments with two index guards:

```python
        while i < len(toks) and (
            ("=" in toks[i] and not toks[i].startswith("-"))
            or os.path.basename(toks[i]) in WRAPPERS
        ):
            i += 1
        if i < len(toks) and os.path.basename(toks[i]) == "gh":
```

**[executed]** Deleting either `i < len(toks)` leaves this module at 33 passed,
exit 0 — no case in the file watches either. Fed a real `PostToolUse` payload,
the hook then exits 1 with `IndexError: list index out of range`, out of the
hook and into the session's Bash call. The commands that do it are ordinary:

| Command fed to the hook | Shipped | `while` guard deleted | `if` guard deleted |
|---|---|---|---|
| `gh pr view 1 --json comments` with a trailing newline | exit 0 | exit 1, `IndexError` | exit 1, `IndexError` |
| `echo hi;` | exit 0 | exit 1, `IndexError` | exit 1, `IndexError` |
| `FOO=bar` | exit 0 | exit 1, `IndexError` | exit 1, `IndexError` |
| `make build \| tee out.log` with a trailing newline | exit 0 | exit 1, `IndexError` | exit 1, `IndexError` |

`SEG_RE` splits on `\n` as well as on `|`, so any multi-line Bash command
leaves a trailing empty segment whose token list is empty. That is the input,
and it is not exotic — it is most of what a session runs.

**Why it matters, and it is not that the code is broken.** The code is fine:
both guards are in place. What follows from this is that the ground for
deferring eleven arms is false. Three carriers say so:

- `seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md`
  T4, Notes: *This is the one whose failure STOPS a session rather than
  misfiling a reminder*. A ledger row is this repository's record of a verified
  fact, and this one is not.
- `overview.md:78`: *the only one whose failure stops a session's Bash call*,
  and `:80`: *The other eleven misfile a reminder rather than stopping
  anything*.
- Issue #262 carries both sentences, and #262 is the ticket that decides when
  the remaining arms get watched. A reader deciding its priority from that body
  believes nothing left in it can stop a session.

Contract §12 is the rule the fix pass applied to `is_closed` and did not apply
here. The finding named an instance; the cause is *an arm of `gh_segments`
whose removal raises out of the hook*, and there are three instances. One case
covers all three, and it is below — this is not the eleven-hand-written-cases
shape #262 declines, because these three share one input class and one
assertion.

**[executed]** the case below is green as shipped at 38 passed, and red on each
of the three arms in turn, with the parameters splitting by arm: `except
ValueError` fails the two quoted-pipe parameters, each `i < len(toks)` fails the
three empty-segment ones.

## ⬜ 2 — the ledger row says thirteen where the issue and round 1 both say twelve

`seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md:6`.

T4's Notes read *`gh_segments` five arms and `main` nineteen, and thirteen of
those were watched by nothing*, then *The remaining eleven arms are deferred to
#262*. Thirteen minus the one closed here is twelve, not eleven.

**[read]** #262's own table gives four unwatched in `gh_segments` and eight in
`main` — twelve — and round 1's finding 1 says *twelve arms of the file's other
two functions are unwatched*. Twelve minus one is eleven, and the rest of T4
and all of #262 are written against eleven. The stray number is `thirteen`,
which is round 1's count of RED mutations rather than of unwatched arms.

This is a correction, not a fix: the location is a ledger fragment.

## ⬜ 3 — the row was re-verified on the 8th and still says it was read on the 7th

`seal/ledger.md:1385`.

**[read]** R5's anchor is now
`test_the_guard_falls_back_to_the_raw_text_without_the_reader@504b6136`, written
at `d7dce3d`, and its `Checked` column still reads `2026-09-07`. Round 1's own
paste-ready fix for that finding asked for both halves — *and R5's Checked
column 2026-09-07 -> 2026-09-08*. `--reverify` rewrites the hash cell and
nothing else, so the date half is the writer's, and it did not happen.

`CLAUDE.md` says the `Checked` column holds the date somebody read the code and
that re-verifying is re-reading followed by `--reverify`. As it stands the row
says its claim was last read against content that has since changed, which is
the one thing the column exists to answer.

This is a correction, not a fix: the location is `seal/ledger.md`.

## The eight verdicts, answered

### Round 1's 🟡 1 — closed

**[executed]** Deleting `except ValueError` from `gh_segments` fails
`test_an_unbalanced_quote_in_a_piped_gh_command_does_not_stop_the_session`
alone, 32 green. The case's input reaches the arm rather than standing beside
it: `SEG_RE` splits `gh pr view 1 --json comments | jq '.c[] | .b'` into three
segments, two of which raise `No closing quotation` from `shlex`, and the
second command leaves one such segment. The 🟡 above is about the sentence
beside this fix, not about the fix.

### Round 1's 🟡 2 — closed, and round 1's own control now fails

**[executed]** All three of round 1's scenarios, re-run at the target:

| Mutation of the reader | Round 1 measured | This round measures |
|---|---|---|
| a third blanking pass added as a module function | RED, both parameters | RED, 2 failed / 31 passed |
| the same blanking written inline as a substitution | **GREEN, 30 passed, exit 0** | **RED, 2 failed / 31 passed** — refused by name, `['sub']` |
| a reader pass renamed | RED, with advice that does not work | RED, with advice that does (below) |

The refusal message names the offending call and both repairs: give the pass a
name on the reader module, or teach the derivation the shape you used.

**[executed]** Deleting the refusal from `reader_blanking_passes` fails
`test_a_blanking_pass_written_as_a_sub_is_refused_rather_than_unseen` alone, 32
green.

### Round 1's ⬜ 3 — closed, with the correction above

**[read]** The anchor moved to `504b6136` and the claim under it still holds. I
read the anchored case rather than trusting the hash: it still points `READER`
away from the real reader, still asserts `reader()` returns None rather than
raising, still asserts the raw-text fallback on both a fenced record and a
missing one, and now carries one parameter per reachable arm — four, which is
what R5's own corrected sentence claims. The docstring edit that moved the hash
is round 1's ⬜ 5 being answered, and it does not contradict anything R5 says.
The residual is the `Checked` date, ⬜ 3 above.

### Round 1's ⬜ 4 — closed, figures confirmed

**[executed]** I re-ran the whole tally against the module as it stood at
`c3c22c2`, in a worktree at that commit. Baseline 27 passed, exit 0. Mutating
`reader`'s five arms one at a time, caches cleared and spaced:

| Arm deleted | Result |
|---|---|
| `spec is None` | RED — 1 failed, 26 passed |
| `spec.loader is None` | green — 27 passed |
| `except OSError` | RED — 1 failed, 26 passed |
| `except ImportError` | green — 27 passed |
| `except SyntaxError` | green — 27 passed |

Two red, three green, and the named members match the corrected cell exactly.
The correction is right.

The row label still reads *six mutations, one per arm* over a five-arm tally,
which is the shape round 1 objected to. It no longer asserts the contradiction,
though — the cell now says the six were the round's own set and did not include
`ImportError`, and states the true per-arm figures separately. That is the
honest form, and I am not reopening it.

### Round 1's ⬜ 5 — closed

**[read]** The docstring now gives the durable reason — the loader is assigned
inside the supported-suffix loop and None is returned from that loop's `else`,
so the state is unreachable for any location string — and marks the sweep as
corroboration, naming the per-platform suffix list and pointing at contract §13.
`overview.md`'s *Not done* paragraph carries the same two halves. This is the
repair round 1 asked for.

### Round 1's ⬜ 6 — closed, and the prescribed repair works

**[executed]** I read the message as a renamer and then did what it says.

| After renaming a reader pass | Result |
|---|---|
| do nothing | RED, 2 failed |
| re-key the existing entry, as the message now prescribes | **GREEN, 33 passed, exit 0** |
| add a third key, which is all the old message offered | RED, 3 failed |

The message names both causes and the repair each one takes, and the repair it
gives a renamer is the one that works.

**[executed]** Cutting the rename half back out of the message fails
`test_the_ties_message_answers_a_rename_as_well_as_an_addition` alone, 32 green.

### Round 1's ⬜ 7 — closed

**[executed]** `c7fe663` and `6de1bca` are `Not a valid object name` in a fresh
clone; `341be0b`, `70c272c` and `701d109` all resolve. Following the file's
history gives exactly those three versions plus the correcting commit itself, so
the row now names every version a clone can open and no more.

### Round 1's ⬜ 8 — unchanged

Named as already deferred, and it stays there.

## The three new units — the exempt surface

All three were seen red on their own mutation, each failing alone with the other
32 green, and none is a case whose input stops short of what it claims to pin.

| Unit | Mutation | Result |
|---|---|---|
| `test_an_unbalanced_quote_in_a_piped_gh_command_does_not_stop_the_session` | `except ValueError` deleted | RED alone — and `shlex` does raise on the segments the case feeds |
| `test_a_blanking_pass_written_as_a_sub_is_refused_rather_than_unseen` | the attribute-call refusal deleted | RED alone — the fake reader is a real module and reaches the derivation |
| `test_the_ties_message_answers_a_rename_as_well_as_an_addition` | the rename half of the tie's message removed | RED alone — and the behaviour it stands for is executed above, not only asserted |

The third pins a message by reading the source of the function that carries it,
which is contract §14's shape rather than a behavioural assertion. It is worth
saying that its guarantee is textual: it would pass if the two words moved into
that function's docstring. The behaviour behind the words is executed in ⬜ 6
above, so nothing rests on the text alone.

## What I did not run

`evidence-check` unscoped, the full suite, repository-wide lint and the
typecheck are the orchestrator's under contract §2 and were not run here. The
`--reverify` the prompt withheld was not run either; I verified the row by
reading the case its anchor names.

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the remaining unwatched arms of `main`, and the durable close that derives arms from source and mutates them | issue #262, already deferred by the branch | the orchestrator, or the work item #262 opens |
| whether `blank_fences` and `strip_comments` have unwatched arms of their own | `overview.md:54`, already deferred by the branch | the review orchestrator, or a follow-up work item |

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

Needs a fix: yes — finding 1, the ground that sent two more session-stopping arms into the deferred eleven, carried by a ledger row, `overview.md` and issue #262
Loses a record or crashes: no

## Proof

Files opened in a `git clone --no-local` at `600a9fc`, plus a worktree at
`c3c22c2`:

- `tests/test_chain_hooks.py`
- `hooks/review-history-guard.py`
- `skills/verify/scripts/unverified_check.py`
- `skills/evidence-check/scripts/evidence_check.py`
- `bin/test`
- `seal/ledger.md`
- `seal/ledger/1788844300-the-guards-cases-cannot-observe-what-they-guard.md`
- `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/overview.md`
- `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/changelog.md`
- `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/rounds/round-1.md`
- `seal/specs/1788844300-the-guards-cases-cannot-observe-what-they-guard/rounds/round-1-report.md`
- `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/rounds/round-3.md`
- issue #262, read with `gh issue view`
