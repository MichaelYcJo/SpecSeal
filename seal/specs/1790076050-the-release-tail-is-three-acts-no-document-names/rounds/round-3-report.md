# 1790076050-the-release-tail-is-three-acts-no-document-names — review round 3

The last record of this run. Target SHA `a32d6d77bc837afc0c279e8ab70a0cfdf1517b85`;
the surface read is
`cbd90ff8d0812437e696c85eced51553a5b17de4..1f1305b8bc9f0a68b4e9df7a8f34af8b33c83315`,
two commits. Round 2's `New units` and `Contract changes` both read none, so
there was no unreviewed finding surface and the job was the answers. Rounds 1
and 2's verdicts are inherited, not re-derived.

All three of round 2's findings are closed, and the wider class the fix pass
took on is real: the five forbidden verbs were substring searches for the same
reason the `edit` gate was, and removing the folded reader from the case
entirely is the right depth. Two things need a fix, and both are claims about
what the new reader holds rather than the reader itself. The run's one
reopening is spent, so both are deferred with the owner named.

## What round 2's fixes actually did — the five claims, judged

**Claim 1 — the class was wider than the finding, and the new case reddens on
both escapes.** Executed, six probes in a `git clone --no-local` at the target
SHA, each with the script restored afterwards:

| Probe | Case exit |
|---|---|
| the tree unmodified | `1 passed` |
| `--add-assignee "someone"` added to the one `edit` argv | `1 failed` |
| a `gh issue reopen` argv spread across lines with a comment between two of its words | `1 failed` |
| a plainly spelled `gh issue reopen` (the control) | `1 failed` |
| the one `issue edit` argv removed | `1 failed` |

The fourth row is what the old folded reader could not see and the reason the
class was wider than the coordinate. The fifth is the `== 1` change shown red:
under `<= 1` a script that stopped spending the label passed, and it does not
now. Both escapes the round named are closed.

**Claim 2 — the sibling row was changed, and it is the same class.** The
answerer of the `console.to_utf8()` row moved from *whoever owns
`hooks/console.py`'s convention* to *the repository owner*. The file's header
states one rule with two arms — **Every row names a person, with no condition
attached** — and round 2's finding was the second arm. A role is the first
arm of the same sentence, so `agent-contract` §12 is what the pass followed
rather than scope it took. Executed: all 19 answerer cells in the file now
read *the repository owner*.

One consequence is worth a reader knowing and is not a defect. Round 2's
record still names *whoever owns `hooks/console.py`'s convention* in its
`## Deferred` table, so the record and the file now name different answerers
for the same item. The record is a record of a moment and the file is the live
home, which is the convention this work item's own `survivors.md` states.

**Claim 3 — the guard cannot be discussed in the file it guards, and the
measurement is right.** Read at
`tests/test_a_rider_reaches_its_file.py:132-133`: the guard iterates the rows
of the section and asserts the forbidden two-word phrase is not in
`" ".join(row)`. The whole row is joined and searched, so it does not tell an
answerer cell from prose in the same row, and a row describing the guard by
quoting its literal reds against a row whose answerer is unconditional. The
new row's own description of it — *asserts that one two-word phrase does not
appear anywhere in a row* — is accurate.

**Claim 4 — the nine occurrences, and the placement.** Executed over the
whole tree: nine occurrences of the old name, in seven files. Six are marked
and all six carry the marker on the name's own line, which is the line it
exempts; the three unmarked are round records. Enumeration and placement both
hold.

| Occurrence | State |
|---|---|
| `overview.md:26` | marked, same line (round 1) |
| `phases/phase-4.md:154` | marked, same line (round 1) |
| `phases/phase-4.md:201` | marked, same line (round 1) |
| `rounds/round-2-report.md:169` | marked, same line (round 2's report) |
| `spec.md:201` | marked, same line — this fix range |
| `phases/phase-4.md:25` | marked, same line — this fix range |
| `rounds/round-1-report.md:146` | unmarked, a round record |
| `1789172128-…/rounds/round-1.md:56` | unmarked, another work item's record |
| `1789172128-…/rounds/round-1-asked.md:38` | unmarked, another work item's record |

**One part of the handoff's reasoning for it is not supported by the tree.**
The claim that the fix was needed *because the markers written in round 1 sat
on the following line and exempted nothing* does not hold: at `cbd90ff8` all
three of round 1's markers were already on the name's own line, and this fix
range did not move any of them. What the fix range did is mark the two
`path#name` occurrences that carried no marker at all, which is the act round
2's ⬜ asked for. The act is right; only the stated reason for it is wrong,
and it appears in no tracked file.

**Claim 5 — the exemption and its grounds.** Read: the two survivors are the
folded reader in `tests/test_a_release_cannot_ship_an_untrue_milestone.py` and
`tests/test_a_merged_ticket_says_so_on_the_tracker.py`, about two scripts this
range does not touch. *Only the forbidden half is weak* holds as reasoning —
the positive assertions in the second file fail when a spelling moves, which
is the safe direction, and the forbidden loops in both files pass when it
moves. The judgment that a fix pass may not rewrite two unrelated modules'
checks is this repository's own, and the class is disclosed rather than
silently exempted. Executed: `read_exemptions` parses line by line and skips
blank lines and comment lines, so the inserted block costs the file no
exemption row.

What is wrong is not the exemption. It is the sentence the same row uses to
argue it, which is finding 1 below.

**The claim about the checker, verified.** The fix pass reports inventing
`test_the_signal_only_ever_creates_and_adds` (NAME NOT IN TREE) while writing
a `seal/follow-up.md` row, catching it by grep, and notes that
`evidence-check` would not have caught it either. The conclusion is right and
the reason is wrong, which is finding 2.

## Findings

### 🟡 1. The new reader is described as escape-proof in two tracked files, and it is not

`tests/test_release_hygiene.py:1054-1060` and `seal/follow-up.md:83`

The case's docstring names three things a fold does not survive and then says
the reader was replaced:

> a fold normalises whitespace and nothing else, so a comment between two
> words of the argv, **or a value moved into a constant**, defeats it just as
> the line breaks did. … The reader is `ast` now and the fold is gone.

The new `seal/follow-up.md` row makes the same pairing, naming *a comment
between two of those words, a value moved into a constant, or the words being
spelled through a variable*, and then *that instance is repaired — … parses
with `ast` now and searches nothing*.

**Executed.** The `ast` reader closes the first escape and neither of the
other two:

| The script gains a `gh issue reopen`, spelled as | Case exit |
|---|---|
| a plain argv (the control) | `1 failed` |
| an argv with a comment between two of its words | `1 failed` |
| an argv whose first word is a module constant | **`1 passed`** |
| an argv whose verb is a module constant | **`1 passed`** |

`issue_argvs` compares `words(argv)[:3]` against three string literals, and
`words` keeps only `ast.Constant` strings. A name in any of the first three
positions is dropped, the prefix shifts, and the verb is never matched. That
is the same blindness one layer further out: the reader is stronger than the
fold on whitespace and exactly as blind on a value that is not a literal.

Why it matters, and why it is not only prose. The `seal/follow-up.md` row
asks the repository owner to decide **whether the two remaining cases are
converted**, and states the cost as *an `ast` reader in each* against *two
negative claims resting on a reader now known not to hold them*. Converting
them on that premise buys less than the row says it buys, because the reader
they would be converted to has an open escape of its own. The decision the
owner is being asked to make is stated against a benefit that was not
measured.

### 🟡 2. `seal/follow-up.md` is in no name checker's corpus, and the recorded reason names a different gap

`skills/evidence-check/scripts/evidence_check.py:1919`

The fix pass's reason for why `evidence-check` would not have caught its
invented name is that *a `path#name` inside a `seal/follow-up.md` row is read
as a coordinate rather than as a name*. Half of that is true and it is not the
half that applies to that file.

**Executed**, four injections into a clone at the target SHA, each removed
afterwards, `evidence-check` run over the repository each time:

| Injected | Result |
|---|---|
| a bare invented name, in `seal/follow-up.md` prose | exit 0 · 114 names read · **0 refused** |
| the same name as `path#name`, in `seal/follow-up.md` prose | exit 0 · 114 names read · **0 refused** |
| a bare invented name, in this work item's `spec.md` | **exit 2** · 115 names read · **1 refused** |
| the same name as `path#name`, in this work item's `spec.md` | exit 0 · 114 names read · **0 refused** |

Two separate gaps, and the record names only the second:

- **`seal/follow-up.md` is read by nothing.** Row three is the control and it
  refuses, so the checker does catch an invented bare name — inside a live
  work item. Rows one and two show the file itself is outside that corpus:
  the records arm reads `seal/specs/<id>/` for ids that have a ledger
  fragment, and `seal/follow-up.md` is neither. The form of the name is
  irrelevant there; a bare name passes too.
- **`path#name` inside a live work item is read as a coordinate.** Row four
  is the gap round 2's record described, and it is real. `RECORD_NAME_RE`
  requires the whole backticked span to be an identifier, so a slash or a `#`
  takes the token out of the corpus.

Why it matters: `seal/follow-up.md` is a long-lived tracked file whose rows
are mostly unit names, addressed to a person who is expected to act on them
later. Every name in it is unchecked, and the only thing that caught the
invented one was a fix pass grepping by hand before it committed. The next
one will be written by somebody who does not.

### ⬜ 3. `survivors.md` says *the four below* and three rows follow it

`seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/survivors.md:41`

Round 1's comment opens *Round 1's fix pass adds the four below*, and its four
rows sat contiguously beneath it at `cbd90ff8`. This fix range inserted its own
comment and two rows **between the third and the fourth**, so a reader counting
four rows down from round 1's comment lands on two of round 2's. Round 1's
fourth row is now separated from its own comment by round 2's whole block.

It costs the check nothing — `read_exemptions` reads rows one line at a time
and the orphaned row is still parsed — so this is prose accuracy only. It is
also the class this work item keeps re-finding: a count about a corpus, stated
where the corpus can move underneath it. Appending the new block after round
1's fourth row would have left both comments true.

A correction to this run's own paperwork, so `Needs a fix` does not count it.

### ⬜ 4. Two lines of `phase-4.md` still say the case allows *at most one* `issue edit`

`seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:43`
and `:202`

Both read *at most one `issue edit`*, describing what the restated case
checks. This fix range changed that to exactly one, deliberately, and gave the
reason in a comment at `tests/test_release_hygiene.py:1128`. The phase record
is a record of a moment and was accurate when written; what makes these two
worth naming is that they are the phase record's statement of what the case
checks **now**, and a reader opening the coordinate to check the claim finds a
stronger assertion than the record describes.

A correction to this run's own paperwork, so `Needs a fix` does not count it.

### ⬜ 5. The close assertion no longer pins what the script closes

`tests/test_release_hygiene.py:1116-1119`

The removed line asserted `'"gh", "issue", "close", str(issue),' in folded` —
that the script still closes, and that the fourth word of that argv is the
issue number. The new `len(closes) == 1` is stronger on the count, which the
old form did not check at all, and drops the argument. A close rewritten to
act on something other than `issue` passes.

The trade is almost certainly right and is the same trade the `edit` argv
makes, where the flags are read and the operand is not. What is missing is
that nothing records it, in a case whose whole subject this round and the last
two have been what an assertion is and is not bound to.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the case docstring and the new `seal/follow-up.md` row both say the `ast` reader closes *a value moved into a constant*, and it does not — the row asks the owner to convert two more cases on that premise | `tests/test_release_hygiene.py:1054-1060` | deferred `seal/follow-up.md` | Executed in a clone at `a32d6d77`: a `gh issue reopen` argv whose first word, or whose verb, is a module constant leaves the case at `1 passed`; the same argv spelled plainly, or with a comment between its words, reds it. `words` keeps only `ast.Constant` strings, so a name in the first three positions shifts the prefix. The cap is spent, so this is a deferral rather than a commissioned fix |
| 🟡 2 | `seal/follow-up.md` is outside the records corpus, so a bare invented name in it passes too — and the recorded reason, `path#name` read as a coordinate, is a second and separate gap that applies inside a live work item | `skills/evidence-check/scripts/evidence_check.py:1919` | deferred to an issue | Executed, four injections in a clone at `a32d6d77`: bare and `path#name` in `seal/follow-up.md` both exit 0 with 0 refused; bare in this work item's `spec.md` exits 2 with 1 refused; `path#name` in the same file exits 0. The records arm reads `seal/specs/<id>/` for ids with a ledger fragment, and `RECORD_NAME_RE` requires the whole backticked span to be an identifier |
| ⬜ | `survivors.md`'s round 1 comment says *the four below* and this range inserted two rows before round 1's fourth | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/survivors.md:41` | answered | ⬜ — this run's own paperwork, prose accuracy only. Executed: `read_exemptions` parses row by row and skips blanks and comments, so no exemption row is lost and `survivor-check` is unaffected |
| ⬜ | `phase-4.md:43` and `:202` say the case allows *at most one* `issue edit` while it now requires exactly one | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:43` | answered | ⬜ — this run's own paperwork. Read: the change to exactly one is deliberate and reasoned at `tests/test_release_hygiene.py:1128`; the record is the coordinate a reader opens to check what the case does |
| ⬜ | the close assertion drops the `str(issue)` operand the folded form pinned, and nothing records the trade | `tests/test_release_hygiene.py:1116-1119` | answered | ⬜ — `len(closes) == 1` is stronger on the count, which the old form did not check at all, and the operand is the same thing the `edit` argv already leaves unread. Only the disclosure is missing |
| 🟢 | the new case reddens on both escapes the round named — `--add-assignee` on the `edit` argv, and a re-spelled `gh issue reopen` | `tests/test_release_hygiene.py:1116-1136` | confirmed | Executed in a clone at `a32d6d77`: `--add-assignee` gives `1 failed`; a `gh issue reopen` argv spread across lines with a comment between two of its words gives `1 failed`, where the folded reader counted zero. The plain spelling is the control and also reds |
| 🟢 | `edit` is exactly one rather than at most one, and the change is shown red | `tests/test_release_hygiene.py:1127-1134` | confirmed | Executed: with the one `issue edit` argv replaced by a `gh api` call the case gives `1 failed`. Under `<= 1` that state passed, which is what let the whole parse be skipped |
| 🟢 | the sibling answerer change is the same rule's other arm, not scope the pass took | `seal/follow-up.md:81` | confirmed | Read: the header states one sentence with two arms — names a person, and no condition attached. A role is the first arm. Executed: all 19 answerer cells now read *the repository owner* |
| 🟢 | the guard joins the whole row and searches it, so it cannot be discussed in the file it guards | `tests/test_a_rider_reaches_its_file.py:132-133` | confirmed | Read: the assertion is over `" ".join(row)` for every row of the section, with no cell distinction, so a row quoting the literal while describing it reds although its answerer is unconditional. The new row's description of the guard is accurate |
| 🟢 | the nine occurrences of the renamed case, and the marker on the name's own line | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/spec.md:201` | confirmed | Executed over the whole tree: nine occurrences in seven files; six marked, every marker on the name's own line, which is the line `evidence-check` exempts; the three unmarked are round records. The handoff's reason — that round 1's markers sat on the following line — is not supported: all three were already on the name's line at `cbd90ff8` and this range did not move them |
| 🟢 | the corrected `console.to_utf8()` census | `seal/follow-up.md:81` | confirmed | Executed independently at `a32d6d77`: 13 `.py` files under `.github/scripts/`, 13 carrying a `__main__`, 6 calling `to_utf8()` and 7 not. Exactly the row's figures, and the seven non-callers are the ones `overview.md` now names |
| 🟢 | the 103-column line is re-wrapped, paragraph and all | `docs/branch-and-release.md:100-104` | confirmed | Executed: the re-wrapped lines run 75, 76, 76, 75, 8. The one line still over 88 in that paragraph is 91 and is a single unbreakable path, unchanged by this range |
| 🟢 | the two survivors' exemption and its grounds | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/survivors.md:59-60` | confirmed | Read: both cited cases exist and both still carry the folded forbidden-verb loop; the positive assertions are in the direction a fold cannot silently pass. Executed: `read_exemptions` skips blanks and comments, so the inserted block costs no row. The grounds argue the act correctly; finding 1 is about a different sentence in the same row |
| ⬜ | round 1's `## Paste-ready fixes` cell reading *no paste-ready fix in the report* — already filed as #505 | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/rounds/round-1.md:63` | answered | ⬜ — carried from round 2 unchanged. A defect in the record generator, not in this branch, and nothing in this range touches it |
| ❓ | the broad gate — the full suite, the repository-wide lint and the typecheck | `skills/verify/scripts/broad_gate.py` | out of verified scope | `agent-contract` §2 and `agents/warden.md` hand it to the sealer. The prompt withheld it, so nothing was declined. Answerer: the `sealer`, in its single run |

## Paste-ready fixes

Both are for the answerer named in the `## Deferred` table below, not for a
fourth round. The run's one reopening is spent.

### 🟡 1 — `tests/test_release_hygiene.py`, the docstring paragraph at `:1054-1060`

```
    The arguments go one per line, so `issue reopen` cannot occur as a literal
    and a forbidden-substring list over the raw text forbids nothing. Folding
    the source first was the answer to that for a long time, and it is not
    enough: a fold normalises whitespace and nothing else, so a comment
    between two words of the argv defeats it just as the line breaks did. Two
    review rounds of #450 each found that from a different side. The reader is
    `ast` now and the fold is gone.

    **What the parse does NOT close, measured rather than assumed.** The three
    words are compared against string literals, so an argv whose command, verb
    or subcommand is a module constant or a variable is not matched and walks
    past the forbidden list — measured at round 3, exit 0 on both spellings.
    Reading a name back to its value is a constant-folder, which is mechanism
    with its own argument to make; the gap is a row of `seal/follow-up.md`
    with the owner named.
```

### 🟡 1 — `seal/follow-up.md:83`, the two sentences that state what converting buys

Replace *That instance is repaired — … parses with `ast` now and searches
nothing —* with the measured form, and restate the decision the row asks for:

```
That instance is repaired in the whitespace direction only: `tests/test_release_hygiene.py#test_the_script_closes_and_takes_off_one_named_label_and_nothing_else` parses with `ast` and searches nothing, which closes the comment-between-the-words escape and leaves the other two open — measured at round 3, where a `gh issue reopen` argv whose first word, or whose verb, is a module constant passed the parsed case at exit 0.
```

and, in the same row's closing question:

```
**What needs a person is whether the two remaining cases are converted, and to WHAT** — an `ast` reader in each closes one of the three escapes named above and not the other two, so converting them buys less than a reader of this row would assume, and a reader that folds constants back to their values is a second decision on top of it.
```

### 🟡 2 — an issue body, for the gap no row carries

```
title: a tracked file full of unit names is read by no name checker, and `path#name` is invisible inside the ones that are

Two gaps, measured at a32d6d77 by four injections into a clone, each removed
afterwards:

1. `seal/follow-up.md` is outside the records corpus. The records arm reads
   `seal/specs/<id>/` for ids that have a ledger fragment; that file is
   neither, so a bare invented unit name in it exits 0 with 0 refused. The
   same name in a live work item's `spec.md` exits 2 with 1 refused, which is
   the control. Every unit name in the repository's schedulable-items file is
   unchecked, and the rows are addressed to a person expected to act on them
   later.

2. `path#name` is not read as a name inside a work item either. RECORD_NAME_RE
   requires the whole backticked span to be an identifier, so a slash or a `#`
   takes the token out of the corpus. Measured: the same invented name written
   as `path#name` in a live `spec.md` exits 0 with 0 refused.

Found because round 2's fix pass invented a case name while writing a
`seal/follow-up.md` row and caught it by grepping before it committed. Nothing
would have caught it otherwise.
```

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the worktree at `a32d6d77`; every probe below ran there, the script or document was restored after each, and the clone and its environment were removed afterwards | the worktree was written to once, for this report |
| the hygiene case at `a32d6d77`, unmodified | `1 passed` — the baseline every probe below is read against |
| probe: `--add-assignee "someone"` added to the one `gh issue edit` argv | `1 failed` — the first escape the round named is closed |
| probe: a `gh issue reopen` argv spread across lines with one comment between two of its words | `1 failed` — the second escape is closed; this is what the folded reader counted as zero |
| probe: a plainly spelled `gh issue reopen` argv (the control) | `1 failed` |
| probe: the one `gh issue edit` argv replaced by a `gh api` call | `1 failed` — `== 1` shown red where `<= 1` passed |
| probe: a `gh issue reopen` argv whose first word is a module constant | **`1 passed`** — finding 1 |
| probe: a `gh issue reopen` argv whose verb is a module constant | **`1 passed`** — finding 1 |
| probe: a bare invented unit name injected into `seal/follow-up.md` prose, then `evidence-check` over the repository | exit 0 · 114 names read · **0 refused** — finding 2 |
| probe: the same name as `path#name` in `seal/follow-up.md` prose | exit 0 · 114 names read · 0 refused |
| probe: a bare invented unit name in this work item's `spec.md` (the control) | **exit 2** · 115 names read · **1 refused** |
| probe: the same name as `path#name` in this work item's `spec.md` | exit 0 · 114 names read · 0 refused — the gap round 2's record described |
| `evidence_check.py .` in the clone at `a32d6d77` | `total: 1453 ok · 0 drifted · 0 broken`; the fragment `14 ok`; `1 work item read · 99 unread · 114 names read · 0 refused`. Exit 0, read directly. Every figure the fix pass reported, exact |
| independent count of `.py` files under `.github/scripts/`, of those carrying a `__main__`, and of those calling `to_utf8()` | 13 / 13 / 6, so 7 non-callers. The corrected row's figures, re-derived rather than read |
| enumeration of the renamed case's old name over the whole tree, with each occurrence's marker placement | 9 occurrences in 7 files; 6 marked, all 6 on the name's own line; 3 unmarked and all 3 round records |
| `uvx ruff check` and `ruff format --check` over `tests/test_release_hygiene.py` in the clone | exit 0 and exit 0, read directly |
| measured line widths of the re-wrapped paragraph in `docs/branch-and-release.md` | 75 · 76 · 76 · 75 · 8. The one line over 88 in that paragraph is a 91-column unbreakable path this range did not touch |
| the eight modules and the repository-wide lint the orchestrating session ran; the 88 passed over the hygiene, rider and wrap modules; `survivor-check` over this fix range | not re-run — `agent-contract` §3, the handoff carries them |
| the 357 passed over fourteen modules, `ruff` 0/0, and `deferral-check`, `correction-check` and `unverified-check` the fix pass reports | not re-run — the handoff carries them, and §2 does not put them in this round's hands |
| the broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** It is the sealer's single run, after the rounds settle, and this round did not take it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round 2, finding 1 | `tests/test_release_hygiene.py:1116-1136` | the restated case; opening it is how both escapes were re-measured and how finding 1 was found one layer out |
| round 2, findings 2 and 3 | `seal/follow-up.md:81-83` | the two corrected rows and the two new ones; re-reading them is what produced findings 1 and 2 |
| round 2, ⬜ | `seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/phases/phase-4.md:25` | the unmarked `path#name`; now marked, and the coordinate that led to the checker probes |
| round 1, finding 4 | `tests/test_a_release_is_sized_by_a_criterion.py#test_the_label_is_two_states_and_nothing_schedules_from_it` | the renamed case, carried forward as the name every occurrence is checked against |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The `ast` reader closes the whitespace escape and not a value moved into a constant or a verb spelled through a variable, while a case docstring and a `seal/follow-up.md` row both say it is repaired — and that row asks the owner to convert two more cases on that premise. Measured at round 3, exit 0 on both open spellings | a correction to `seal/follow-up.md:83` and to the docstring at `tests/test_release_hygiene.py:1054`, with the paste-ready forms above | the repository owner |
| `seal/follow-up.md` is outside `evidence-check`'s records corpus, so no name in it is checked at all, and `path#name` is invisible to the name reader inside the work items that ARE read. Two gaps, both measured; nothing in the tree records either | an issue against `skills/evidence-check/scripts/evidence_check.py`, with the paste-ready body above | the repository owner |
| The guard that stops an answerer from being a condition tests one spelling while the rule is a shape — **already deferred** by round 2, written into `seal/follow-up.md:82` by its fix pass. Not re-litigated; verified as written and its second measurement confirmed | `seal/follow-up.md` | the repository owner |
| Whether `console.to_utf8()` is owed by every `.github/scripts/` entry point — **already deferred** by round 1, to `seal/follow-up.md:81`. Its figures are now correct and re-derived; nothing about the question moved | `seal/follow-up.md` | the repository owner |
| The arm neither `CONTRIBUTING.md` §*House rules* nor `CLAUDE.md` carries — **already deferred** by round 1, to `seal/follow-up.md:80`. Round 2 fixed that row's answerer; the question in it is untouched | `seal/follow-up.md` | the repository owner |
| Whether the two remaining folded forbidden-verb readers are converted — **already deferred** by this fix range, to `seal/follow-up.md:83`. Finding 1 is about how that row states the benefit, not about the question | `seal/follow-up.md` | the repository owner |
| `round-1.md`'s `## Paste-ready fixes` cell — **already filed as #505**, in the record generator rather than in this work | issue #505 | whoever owns `skills/code-review/scripts/round_record.py` |

Needs a fix: yes — findings 1 and 2, and neither is in what round 2 asked to
have repaired. Finding 1 is two tracked files saying the new reader closes an
escape it leaves open, in a row that asks the owner to convert two more cases
on that basis. Finding 2 is a checker gap the run met by accident and recorded
with the wrong cause. The run's one reopening is spent, so both are deferred
with the repository owner named and neither commissions a fourth round.

Loses a record or crashes: no — nothing found leaves the root, nothing
crashes, and no path this release exercises is affected. Finding 1 is a claim
about a check that is stronger than the check; finding 2 is a checker that
reads less than a record says it reads. Both are silence where a warning was
assumed, and neither writes or drops anything.

## Proof block

**Executed** — the probes in the table above, each in a `git clone --no-local`
of the worktree at `a32d6d77`, with the modified file restored after every
probe and the clone removed afterwards. The worktree itself was written to
once, for this report.

**Read, not executed** — round 1's and round 2's verdicts, inherited rather
than re-derived; the eight modules and the repository-wide lint the
orchestrating session ran before round 1; the 88 passed and `survivor-check`
it ran over this fix range; the 357 passed over fourteen modules and the three
checks the fix pass reports.

**Unverified** — the broad gate: the full suite, the repository-wide lint and
the typecheck over the whole tree. Answerer: the `sealer`, in its single run.
The tag-triggered workflow's actual run on the forge and the reconcile step's
live write to the tracker are not runnable by any agent and answer to the
repository owner.

Files opened: `tests/test_release_hygiene.py`,
`tests/test_a_rider_reaches_its_file.py`,
`tests/test_a_merged_ticket_says_so_on_the_tracker.py`,
`tests/test_a_release_cannot_ship_an_untrue_milestone.py`,
`.github/scripts/close_issues_on_release.py`, `.github/scripts/run_tests.py`,
`bin/test`, `docs/branch-and-release.md`, `seal/follow-up.md`,
`skills/evidence-check/scripts/evidence_check.py`,
`skills/code-review/scripts/survivor_check.py`, and this work item's
`overview.md`, `spec.md`, `survivors.md`, `phases/phase-4.md`,
`rounds/round-2.md`, `rounds/round-2-report.md`.
