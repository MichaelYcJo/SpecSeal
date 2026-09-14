# 1789347354-a-wrapped-terminal-line-is-not-one-value — review round 3

| Field | Value |
|---|---|
| Target SHA | dd4431f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 392 |
| Broad gate | ed18657 against origin/release/v0.11.4 |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 1 and 🟡 2, both in the new case's comment block and the mutation space it describes. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The last round of the run, and told so at the spawn as a fact about the chain rather than a hope about its findings: round 1 met the floor and round 2 closed on a fix, so the one reopening was spent and this record ends the run whatever it found. The round was told what that costs — anything it opened would end the run `capped`, with every still-open finding becoming an issue reading `deferred #N` — and told to weigh it by writing each finding so somebody else could act on it without its author, not by lowering the bar.

Target is the diff of round 2's fixes, `0bd1f48..dd4431f`, three commits. Rounds 1 and 2 had reviewed everything before `0bd1f48`. Round 2's record was committed and its five verdicts inherited; the job was the answers rather than new findings.

The exempt surface, handed over as a finding surface because a unit the fixes created has been reviewed by nobody: `test_an_ordered_list_item_ends_the_segment`. The fix pass had measured five ordered-list shapes in memory before writing it and kept only the two that can die, recording that `1.` and `3.` are useless because `END` cuts at the period first and that `1)x` is prose under both spellings. The round was asked whether the two arms it keeps are the right two, and whether the comment explaining the three it dropped is true.

Four acts of the fix pass were handed over as facts rather than left to rediscover: ledger row 2 rewritten from a false class claim to five per-alternative measurements; `bin/evidence-check .` having exited 2 over a backticked `_CEILING` naming nothing in the tree, repaired on the memo line by unfolding the constant and in the reviewer's own prose by the `NAME NOT IN TREE` marker; ⬜ 4 answered rather than fixed because amending a commit subject would orphan a SHA a record names and a squash discards every subject anyway; and the memo's uncounted *twenty-seven mutations* replaced by what was actually mutated.

What the orchestrator had already executed at `dd4431f`, handed over so the round would not repeat it: four modules — `test_a_corrected_sentence_survives_elsewhere.py`, `test_the_record_is_generated.py`, `test_the_rules_have_one_owner.py`, `test_docs_line_wrap.py` — 245 passed, exit 0; `bin/evidence-check .` exit 0; `survivor-check --range 0bd1f48..4558feb --exempt …` exit 0; and the mutation confirming the new pin dies, 2 failed and 53 passed.

The round was required to number every row of its verdict table including confirmations, because the unnumbered shape had already cost this work item one hand-edit on a generated file. The broad gate was withheld by name as the sealer's single act after this round settles.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The comment says killing the bullet or heading alternative widens the pattern and is caught; killing either narrows it and turns nothing red | `tests/test_a_corrected_sentence_survives_elsewhere.py:353-356` | deferred #393 | #393 |
| 🟡 2 | Two mutations of the alternative round 2 pinned are still caught by nothing, and the comment's grounds for leaving each are wrong | `tests/test_a_corrected_sentence_survives_elsewhere.py:358-363`, `skills/code-review/scripts/survivor_check.py:385` | deferred #393 | #393 |
| ⬜ 3 | Ledger row 2's headline **Three of the constant's five alternatives are pinned and two are not** is false under both readings of *pinned* | `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md:13` | answered | Corrected at 16bef1e. Located in `seal/ledger/`, so a correction rather than a fix to commission. The headline now says which of the five are pinned depends on the direction of the mutation, gives both readings, and points at #393 for the remainder. The five per-alternative measurements under it were checked row by row against the tree by round 3 and are all true |
| ⬜ 4 | `overview.md` §*Not verified* counts a lookahead among the five alternatives and repeats 🟡 1's wrong direction | `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/overview.md:33` | answered | Corrected at 16bef1e. Located in `seal/specs/`. The row now names the three alternatives unpinned against being killed outright and the one unpinned against losing its lookahead, and states the direction finding rather than repeating its opposite |
| ⬜ 5 | The memo's *every alternative of both constants … with its lookahead dropped* claims more than ledger rows 1 and 2 record | `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/overview.md:6` | answered | Corrected at 16bef1e. Located in `seal/specs/`. The memo's claim is narrowed to what was measured: each alternative killed outright, and, where it has one, with its lookahead dropped |
| ⬜ 6 | Round 2's committed report had a word substituted, not only a marker added | `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/rounds/round-2-report.md:104` | answered | Nothing in the tree is wrong. Round 2's committed report is as the reviewer left it except for the exemption marker `agents/warden.md` requires; what was inaccurate was the fix pass's description of that edit as keeping every word, which lives in a hand-back message rather than in a file. Recorded here so the next reader of that report knows a comma and a `which` moved with the marker |
| ⬜ 7 | `round-2.md`'s `Fixes checked by` still reads *nobody — the fixes are not yet written* in the commit that applied them | `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/rounds/round-2.md:10` | answered | Closed by `round-record new` writing this record: `round-2.md`'s `Fixes checked by` now reads `round-3`. It was the expected state of a cell that only the next round can fill, not a defect |
| ⬜ 8 | Ledger row 2's five per-alternative measurements | `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md:13` | answered | Executed — all five re-measured at `dd4431f` and all five true, including the `[-*_]{3,}` narrowing turning the `===` arm alone red and the ordered-list lookahead turning nothing red. Only the headline count over them is wrong, which is ⬜ 3 |
| ⬜ 9 | Round 2's 🟡 1, fixed at `074e6bb` — the ordered-list alternative is pinned | `tests/test_a_corrected_sentence_survives_elsewhere.py:364-380` | answered | Executed — the alternative replaced by a never-matching pattern: 2 failed, 53 passed, both arms of the new case and nothing else. The two arms kept are the two of the five tried that discriminate |
| ⬜ 10 | Contract §15 — the new unit was seen red before it was planted | `tests/test_a_corrected_sentence_survives_elsewhere.py:365` | answered | Executed — independently reproduced, not inherited: killing the alternative takes the module from 55 passed to 2 failed, 53 passed, and the two failures are this case's own arms |
| ⬜ 11 | Round 2's ⬜ 4, answered rather than fixed — `5671c44`'s subject is not amended | `seal/specs/1789347354-…/rounds/round-2.md:47` | answered | Read — `round-2.md`'s verdict row 4 names `5671c44` as its location, so an amend orphans a SHA a committed record points at. `CLAUDE.md` §*the merge method is fixed per direction* squashes a feature branch into its release branch, so no subject survives. The grounds hold |
| ⬜ 12 | The range the hand-over ran `survivor-check` over stopped one commit short of the target | `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value` | answered | Executed — re-run over the full `0bd1f48..dd4431f`, including the record commit the narrower range excluded: exit 0, 965 files examined against 4 removed sentences, no removed wording still standing. No gap |
| ⬜ 13 | The hand-over names the memo's replaced total as *twenty-seven mutations*; the tree removed `eighteen mutations` | `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/overview.md:6` | answered | Read — `git show 4558feb` removes the word `eighteen`. Contract §5: nothing rests on either figure now, so this is a correction to the account and not to the tree |

## Paste-ready fixes

```python
# The ordered-list alternative, the second of the constant's five that nothing
# pins — same constant, same retyping, same argument as round 1's 🟡 5. It is
# the one worth taking for a reason the bullet and heading alternatives do not
# share, and the reason is about the DIRECTION of the mutation rather than
# about the alternative. What
# `test_a_sentence_wrapped_onto_an_issue_number_is_one_sentence` catches for
# those two is their lookahead being dropped, which widens the pattern until
# `#120` at the head of a line is a heading again. Killing either alternative
# outright narrows the pattern instead, and nothing catches that: measured at
# `dd4431f`, 55 passed either way. Killing this one is caught from neither
# direction until the arms below exist.
#
# `END` ends a sentence at `.` before whitespace, so an arm written `1.` is
# green under the merge assertion whatever `BLOCK` does — measured, and it is
# the same trap that made round 1's first attempt at the whole-line case
# useless. That bounds the assertion, not the alternative: the `.` half is
# reachable one assertion over, on whether the marker joins the sentence above
# it, and `1)x` reaches the lookahead from the other side. Both are pinned
# below.
```
```python
# The `.` half of `[.)]`. The merge assertion above cannot see it, because
# `END` has already cut the sentence at the period — but the block boundary
# still decides whether the marker is the last word of the paragraph above it,
# and that it can see. Narrowed to `[)]` the module was 55 green before this
# case; the two arms below turn red.
@pytest.mark.parametrize("opener", ["1.", "3."])
def test_an_ordered_list_marker_stays_out_of_the_sentence_above(opener):
    """A list marker is not the last word of the paragraph above it.

    `END` splits `1.` off as a segment of its own either way, so nothing about
    the merge changes — what changes is which segment the number belongs to,
    and with the alternative gone it is swallowed by the claim above."""
    reader = module()
    text = f"the claim above the item\n{opener} an unrelated claim below it"
    keys = [sentence.key for sentence in reader.sentences("docs/probe.md", text)]
    assert not any(k.endswith("above the item " + opener[:-1]) for k in keys), (
        f"{opener!r} was not read as a list item, so its number joined the "
        f"sentence above it and scores as part of that claim: {keys!r}"
    )


# The lookahead, and the one shape that reaches it. `1)x` is prose while
# `(?=\s)` stands and a list item once it is dropped, so the assertion runs
# the other way round from every case above it: this arm holds the pattern
# NARROW, where the others hold it wide.
def test_an_ordered_list_marker_needs_the_space_after_it():
    """`1)x` is prose, so the wrap above it is not a block boundary.

    Without the lookahead a hard-wrapped sentence whose second line opens
    `1)x` splits at a boundary that is not there — the same false split the
    bare `[-*+>#]` class cost this module, one alternative over."""
    reader = module()
    text = "the claim above the item\n1)x an unrelated claim below it"
    keys = [sentence.key for sentence in reader.sentences("docs/probe.md", text)]
    assert any("above the item" in k and "below it" in k for k in keys), (
        "`1)x` was read as a list item, so a hard-wrapped sentence split at a "
        f"boundary that is not there and no n-gram crosses it: {keys!r}"
    )
```
```
**Two of the constant's five alternatives are pinned against outright deletion and three are not**, measured 2026-09-14 by mutating each in turn — killed, and where it carries a lookahead, with the lookahead dropped — and the row says which rather than claiming the class: killing `[-*_=]{3,}\s*$` turns four arms red and narrowing it to `[-*_]{3,}` turns the `===` arm alone red; killing `\d+[.)](?=\s)` turns two arms red, though **dropping that alternative's lookahead turns nothing red, and neither does narrowing `[.)]` to `[)]`**; the bullet and heading alternatives are pinned only through their lookaheads, each dropping to one red arm of `test_a_sentence_wrapped_onto_an_issue_number_is_one_sentence`, and killing either outright turns nothing red; and **`>`, which carries no lookahead, is pinned by nothing**
```
```
Round 2's 🟡 1 is why the ordered-list alternative was the second taken and `>` was not — dropping the bullet or heading lookahead widens the pattern in the direction this work item argues for and is caught from the other side, where killing this one is caught from neither and merges a real list item into the sentence above it. Killing the bullet or heading alternative outright is caught by nothing either, which is the mutation this row used to describe as covered
```
```
| Three mutations of `survivor_check.py#BLOCK` are caught by nothing — `>` killed, the lookahead on `\d+[.)]` dropped, and `[.)]` narrowed to `[)]`; killing the bullet or heading alternative outright narrows the pattern and is caught by nothing either | the repository owner, as a ticket against `survivor_check.py` — round 3 is this work item's last round. Round 3's 🟡 2 carries a measured arm for each of the two that sit on the alternative this branch pinned |
```
```
· verified: executed — the four modules below, the record module before and after; each of `survivor_check.py#BLOCK`'s five alternatives mutated in turn, killed and, where it carries a lookahead, with the lookahead dropped, and seven of `round_record.py#BLOCK_START`'s ten likewise, and every sentence this work pins stashed in turn — the results are per-alternative in ledger rows 1 and 2 rather than as a total here, because a count is the third thing this work item got wrong about its own measurements, `bin/evidence-check .`, `--strict`, and the Q5 measurement over 337 terminal rows. Read — the frame, the round-4 report, `seal/ledger.md` R7 and the `issue_claims_check.py` rows. Unverified — the full suite, repository-wide lint and typecheck, which are the sealer's
```
```
| Fixes checked by | round-3 |
```

## Executed probes

| What was run | Result |
|---|---|
| `pytest tests/test_a_corrected_sentence_survives_elsewhere.py` at `dd4431f`, in a `--no-local` clone | 55 passed, exit 0 |
| Ten mutations of `survivor_check.py#BLOCK`, one per run, each on the same module | the table below |
| `[.)]` narrowed to `[)]`, a mutation neither round had taken | 55 passed, exit 0 — half the character class is caught by nothing |
| Candidate arm for the `.` half, on the sentence key rather than the merge | green at `dd4431f`, red under the `[)]` narrowing and under the outright kill |
| Candidate arm for the lookahead — `1)x` asserted to stay one segment | green at `dd4431f`, red with `(?=\s)` dropped |
| `bin/evidence-check .` at `dd4431f` | exit 0 |
| `bin/survivor-check --range 0bd1f48..dd4431f` — the full target range | exit 0, no removed wording still standing |
| The full suite, repository-wide `ruff check` and `ruff format --check` | not yet — the sealer's, after this round settles, per `skills/agent-contract/SKILL.md` §2. This report leaves nothing for a fix pass in the tool, so the spawn is due once ⬜ 3–⬜ 7 are answered |

```
mutation of survivor_check.py#BLOCK          result        arms turned red
-------------------------------------------  ------------  ----------------------------
baseline (dd4431f)                            55 passed     —
bullet [-*+](?=\s) killed                     55 passed     none
bullet lookahead dropped                      1 failed, 54  wrapped_onto[**round 4**]
heading \#{1,6}(?=\s|$) killed                55 passed     none
heading lookahead dropped                     1 failed, 54  wrapped_onto[#120's]
> killed                                      55 passed     none
\d+[.)](?=\s) killed                          2 failed, 53  ordered_list[1)], [12)]
\d+[.)] lookahead dropped                     55 passed     none
[-*_=]{3,}\s*$ killed                         4 failed, 51  whole_line[---][___][***][===]
[-*_=]{3,}\s*$ narrowed to [-*_]{3,}          1 failed, 54  whole_line[===]
[.)] narrowed to [)]  (not previously taken)  55 passed     none
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:1252-1258` | round 1's 1 — fixed |
| round-1 | `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md` row 1 | round 1's 2 — fixed |
| round-1 | PR #392 §*Operational impact* | round 1's 3 — answered |
| round-1 | `agents/warden.md:409` | round 1's 4 — fixed |
| round-1 | `skills/code-review/scripts/survivor_check.py:384` | round 1's 5 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1247`, `docs/review-handoff-protocol.md:302` | round 1's 6 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#BLOCK_START` | round 1's ⬜ 7 — answered |
| round-1 | `tests/test_the_record_is_generated.py` | round 1's ⬜ 8 — answered |
| round-1 | `seal/specs/1789347354-…/spec.md:252` | round 1's ⬜ 9 — answered |
| round-1 | `skills/code-review/scripts/round_record.py`, `templates/sdd-round.md` | round 1's ⬜ 10 — answered |
| round-1 | `agents/warden.md`, `docs/review-handoff-protocol.md` | round 1's ⬜ 11 — answered |
| round-1 | `skills/code-review/scripts/survivor_check.py#BLOCK` | round 1's ⬜ 12 — answered |
| round-2 | `skills/code-review/scripts/survivor_check.py:384`, `tests/test_a_corrected_sentence_survives_elsewhere.py` | round 2's 🟡 1 — fixed |
| round-2 | `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md` row 2 | round 2's ⬜ 2 — fixed |
| round-2 | `docs/review-handoff-protocol.md:308`, `skills/code-review/scripts/round_record.py:1247`, `tests/test_the_rules_have_one_owner.py` | round 2's ⬜ 3 — answered |
| round-2 | `5671c44` commit subject | round 2's ⬜ 4 — answered |
| round-2 | `seal/specs/1789347354-…/rounds/round-1.md` verdict row 4 | round 2's ⬜ 5 — deferred |
| round-2 | `tests/test_a_corrected_sentence_survives_elsewhere.py:328` | round 2's ⬜ 6 — answered |
| round-2 | `tests/test_the_record_is_generated.py:539` | round 2's ⬜ 7 — answered |
| round-2 | `seal/specs/1789347354-…/survivors.md` | round 2's ⬜ 9 — answered |
| round-2 | `seal/specs/1789347354-…/rounds/round-1.md` | round 2's ⬜ 10 — answered |
| round-2 | `docs/review-handoff-protocol.md:304`, `skills/code-review/scripts/round_record.py:1240` | round 2's ⬜ 11 — answered |
| round-2 | `seal/ledger.md`, `seal/ledger/1789347354-…md` | round 2's ⬜ 12 — answered |
| round-2 | `seal/specs/1789347354-…/rounds/round-1.md` §*Deferred* | round 2's ⬜ 13 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Round 2's ⬜ 5 — `close` prepends to a grounds cell, so round 1's finding 4 states a pre-fix count under a **fixed** verdict | issue #391 | the repository owner |
| `evidence_check.py#file_units` reads a heading inside a fence as a heading, so three of thirty-six anchored markdown files truncate | `overview.md` §*Not verified* | the repository owner — a change to a gate under `CONTRIBUTING.md` |
| The three-shape joined-list is stated in two carriers and no case counts them | `overview.md` §*Not verified* | the repository owner, as a ticket against `tests/test_the_rules_have_one_owner.py` |
