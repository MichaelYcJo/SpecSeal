# 1788472135-the-run-outlives-its-last-finding — phase 2

<!-- seal/specs/1788472135-the-run-outlives-its-last-finding/phases/phase-2.md — what
this phase of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 1b4d5a4 |

## What this phase was asked

Build phase 2 only: state #117's bound — *a fix pass may add a unit; that
unit's fix may not* — **with its exit written first.** A refused unit has
somewhere to go, a deferral with a named answerer or an issue, which is
already what #110 says to do with what a stopped round found. That sentence
lands first, in the same section, so nobody meets a refusal with no exit.
`plan.md` calls the order the point rather than convenience; keep it.

Three files:

- `skills/code-review/SKILL.md`, beside phase 1's floor, because the reader
  meeting the floor is the reader who needs to know what a fix may still add.
- `agents/smith.md:145-160`, what a fix pass may add, in the file the smith
  actually reads. The cap and the verifying round are stated there; what a fix
  pass may create is stated nowhere.
- `templates/sdd-round.md`, the existing `New units` row. The entry shape is
  `unit (depth N)`, `;`-separated, and `none` stays an answer with or without a
  reason. Show the form in the comment so a session can copy it. Do **not** add
  a separate depth row: `plan.md`'s Alternatives table records why one number
  per round cannot be true, since a single fix pass can answer both an
  original-code finding and a finding inside an earlier pin.

The measurement to carry: across four rounds of #82, round 1's fixes added
`configured_language` and a templates check and round 2 found the defect
reproduced in both; round 2 added `mirror_to_refuse` and a widened glob and
round 3 found the glob out of step with its corpus; round 3 added
`as_language_name`, `ROUND_RECORD_FIELDS` and a `git ls-files` helper and round
4 found a subprocess without `check=True` and a list hand-copied from the file
it checks.

Same segment constraints as phase 1: `chain_check.py` untouched, no fragments,
narrow verification only.

## What this phase found

**The exit's position is checkable, and checking presence alone would have
been vacuous.** `test_the_exit_is_stated_before_the_rule` compares the two
offsets rather than asserting two substrings exist. It has to read a **slice**
of each file: `skills/code-review/SKILL.md` now carries the exit sentence
twice on purpose — once under the floor, once under the bound — so a
whole-file ordering check is answered by the floor's copy and would pass on a
depth section that named no exit at all. Each slice is bounded by text that was
in the file before this rule landed (`### Then say who checked` in the skill,
`the way out is the verifying round above` and `What is unresolved at that` in
the smith), so the window is defined by the document rather than by the
sentence under test.

**Pinning the slicer was the missing case, and mutation is what surfaced it.**
Degrading `section()` to return the whole file left the ordering case green and
saying nothing. `test_the_section_slice_is_narrower_than_the_file` closes it,
including the count assertion that the skill carries the exit sentence at least
twice — if either section starts borrowing the other's exit, one of the two
refuses with nothing to point at.

**One absence case passed on an empty read.** With `read()` mutated to return
`""`, `test_needs_a_fix_no_longer_claims_to_be_the_only_ending` stayed green:
an absence is trivially satisfied by a file that was never opened.
`skills/verify/SKILL.md`'s own rule is that an absence claim is only as good as
the search behind it, so each of the three files now asserts the sentence that
**replaced** the old one beside the old one's absence. The same mutation now
takes all nine cases in that module red rather than eight.

**Three spellings of one sentence reached three files on the first draft** — a
semicolon in one, a lower-cased clause in another. The rule is now verbatim in
all three, and `test_all_three_files_state_the_rule` is what keeps it that way.
A rule a reader has to recognise across paraphrases is a rule phase 3 cannot
find at all.

**What phase 3 parses, stated exactly.** The row as the template now carries
it:

```
| New units | <`none`, or the top-level definitions and constants this round's fixes added, each with the depth it was added at — `unit (depth N)`, entries separated by `;`. The verifying round's finding surface> |
```

The three cell values the template shows filled in, which are what a record
author copies:

```
| New units | configured_language (depth 1); mirror_to_refuse (depth 1) |
| New units | none |
| New units | none — the fixes are not yet written |
```

So the accepted entry is `<unit name> (depth <N>)`, one space before the
parenthesis, entries separated by `; `. `says_none` keeps its tolerance
unchanged: `none` alone, and `none — <reason>`, are both answers. The refusals
phase 3 owes are an entry with no depth at all — the present-and-malformed case
`fix_surface` already declines to grandfather — and a depth of 2 or above, whose
failure message has to name the two places the unit goes instead.

**`templates/config.md` grew twice this branch, and phase 3 may owe it a
third.** `Loses a record or crashes` went on the *what no row governs* list in
phase 1; `depth` went on it here, because a record author writing in another
language would otherwise translate the marker a checker is about to read. When
phase 3 adds a module constant that `chain_check.py` matches literally,
`test_the_exclusion_list_holds_every_string_a_checker_matches` derives its
expectation from that constant and will demand it on the same list.

**A check on this branch is still red for a reason that is not this phase's,**
unchanged from phase 1:
`tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`
fails while this work item's directory has no `overview.md`. It fails
identically on a tree built from the branch's base commit. The closing memo is
written when implementation ends, after phase 4.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | — |
