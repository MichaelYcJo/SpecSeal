# 1789347354-a-wrapped-terminal-line-is-not-one-value — review round 3 report

The verifying round, and the run's last. Target is the diff of round 2's
fixes, `0bd1f48..dd4431f`, three commits — not the branch. Round 2's five
verdicts are inherited; the job was the answers, plus the one unit the fixes
created that nobody has reviewed.

## How the findings relate

Round 2's 🟡 1 said an alternative of `survivor_check.py#BLOCK` was pinned by
nothing, and its ⬜ 2 said the ledger row describing the constant's mutation
space was false. The fix pass closed both — the alternative is pinned, and the
row now measures each alternative instead of claiming a class. Every one of
those five measurements is true; I re-ran all ten mutations and they match.

What did not come with it is the direction the mutations were taken in. The
new case's comment, the ledger row's **Notes** cell and `overview.md` all say
that *killing* the bullet or heading alternative is caught by an existing
case. Killing either turns nothing red — 55 passed both times. What that case
catches is the lookahead being dropped, which is the opposite mutation. The
ledger's own **Verified behavior** cell says so correctly, one cell to the
left of the sentence that contradicts it.

That same comment then closes two more doors that are open, and both are one
arm wide. So the findings run: a wrong direction stated three times, the two
pins that direction talked the fix pass out of writing, and then the
paperwork the two produced.

## 🟡 1 — The comment says killing the bullet or heading alternative is caught; killing either turns nothing red

`tests/test_a_corrected_sentence_survives_elsewhere.py:353-356` states the
reason this alternative was chosen over the other two:

> the one worth taking for a reason the bullet and heading alternatives do not
> share: killing either of those widens the pattern, and
> `test_a_sentence_wrapped_onto_an_issue_number_is_one_sentence` catches a
> widening from the other side.

Two things in that sentence are wrong. Killing an alternative removes matches,
so it narrows the pattern rather than widening it; dropping a lookahead is
what widens it. And killing either alternative is caught by nothing — measured
at `dd4431f`, the bullet alternative replaced by a pattern that matches nothing
leaves 55 passed, and the heading alternative likewise. Only the
lookahead-dropped mutations turn that case red, one arm each.

Why it matters: the comment is the recorded justification for leaving the
bullet and heading alternatives unpinned, and it tells the next reader they
are already covered against deletion. They are not. A later edit that deletes
either alternative ships green.

The class is the sentence rather than the line. It appears in three carriers,
and two of them then draw opposite conclusions from it:

| Carrier | What it says about killing bullet or heading |
|---|---|
| `tests/test_a_corrected_sentence_survives_elsewhere.py:354` | widens the pattern, and is caught from the other side |
| `seal/ledger/1789347354-…md` row 2, **Notes** cell | widens the pattern in the direction this work item argues for and is caught from the other side |
| `seal/ledger/1789347354-…md` row 2, **Verified behavior** cell | killing either outright turns nothing red — correct |
| `seal/specs/1789347354-…/overview.md:33` | widens the pattern **and turns nothing red** — half right |

The paste-ready below fixes the test comment. The two ledger and overview
corrections are ⬜ 4 and ⬜ 5, because their location is under `seal/`.

## 🟡 2 — Two mutations of the alternative just pinned are still caught by nothing, and each closes with one arm

The comment at `tests/test_a_corrected_sentence_survives_elsewhere.py:358-363`
gives up on both, and the grounds are measurably wrong in each case.

**The `.` half of `[.)]`.** The comment says *Only the `)` half can be pinned
here*, on the ground that `END` cuts at the period first. The premise is true
for the merge assertion the case uses, and the conclusion does not follow.
Narrowing `[.)]` to `[)]` leaves the module 55 green, so half the character
class this round's fix was written to protect is protected by nothing — and
the half is reachable one assertion over. With `[.)]` in place, the sentence
above a `1.` item reads `the claim above the item`; with `[)]`, it reads `the
claim above the item 1`, because the marker stops being a block opener and
becomes the last word of the paragraph above it. An assertion on that key goes
red under the narrowing and under the outright kill, and is green at
`dd4431f`.

**The lookahead `(?=\s)`.** The comment says `1)x` *is green … and the
lookahead that says so is pinned by nothing*, and `074e6bb`'s message lists
`1)x` among the shapes that *cannot* die. `1)x` is in fact the one shape that
reaches the lookahead: it stays one segment while `(?=\s)` stands and splits
into two once the lookahead is dropped. Asserted in the direction the shape
actually discriminates — that it stays one segment — the arm is green at
`dd4431f` and red with the lookahead dropped. `overview.md:33` hands that same
lookahead to the repository owner as a ticket on the ground that nothing pins
it; the shape that pins it was measured in the fix pass and discarded for
being green under an assertion written the other way round.

Why it matters: this is round 1's 🟡 5 and round 2's 🟡 1 a third time — a
retyped constant whose mutation space is open — and the two remaining holes in
it were each reasoned closed rather than measured closed.

## ⬜ 3 — Ledger row 2's headline count is false under both readings, which is the failure round 2's ⬜ 2 closed

`seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md:13` opens
its **Verified behavior** cell with **Three of the constant's five
alternatives are pinned and two are not**. The five measurements that follow
it in the same cell are all correct, and they do not add to three:

| Reading of *pinned* | Pinned | Not pinned |
|---|---|---|
| some mutation of it turns something red | bullet, heading, ordered, whole-line — **4** | `>` — **1** |
| killing it outright turns something red | ordered, whole-line — **2** | bullet, heading, `>` — **3** |

`074e6bb`'s message names the two it counted as unpinned: *`>` in neither
direction, and the lookahead on `\d+[.)]`*. A lookahead is not one of the five
alternatives, so that pairing cannot produce a count of five either. Under the
second reading the figures are simply transposed — two are pinned and three
are not.

Round 2's ⬜ 2 was *false under both readings*. Its fix replaced a false class
claim with a false count, which is the fourth time this work item has been
wrong about its own measurements.

The same cell also says **`>` is pinned by nothing in either direction**. `>`
carries no lookahead, so it has only one direction; the claim is true and the
phrase names a mutation that does not exist.

## ⬜ 4 — `overview.md` calls a lookahead one of five alternatives, and repeats the wrong direction

`seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/overview.md:33`
reads *Two of `survivor_check.py#BLOCK`'s five alternatives are still pinned by
nothing — `>` in either direction, and the lookahead on `\d+[.)]`*. One of the
two named is not an alternative. The row then repeats 🟡 1's wrong direction —
*killing … outright widens the pattern* — though it gets the consequence right.

The row also understates what is open: after 🟡 2, the `.` half of `[.)]` is
unpinned as well, and both it and the lookahead close with one arm each rather
than needing a ticket.

## ⬜ 5 — The memo's replacement for the count claims more than rows 1 and 2 hold

`overview.md:6` now reads *every alternative of both constants mutated in
turn, killed and with its lookahead dropped*. Checked against the rows it
defers to:

- **Row 2** covers all five alternatives of `survivor_check.py#BLOCK`. Two of
  the five — `>` and `[-*_=]{3,}\s*$` — have no lookahead to drop, so *with
  its lookahead dropped* cannot be true of them.
- **Row 1** covers `round_record.py#BLOCK_START`, which has ten alternatives.
  Its enumeration names the `#` and `[-*+]` lookaheads, the three run-of-three
  alternatives, the setext alternative, `[.)]` narrowed, and the whole-line
  anchor. It never mentions `[>|]`, ` ``` ` or `~~~` — three alternatives with
  no recorded mutation.

Replacing a count with a claim about every alternative was the right move; the
claim as written is broader than the evidence under it. The narrow true form is
in the paste-ready.

Separately, and for the hand-over rather than the tree: the round 3 prompt says
the memo's replaced total was *twenty-seven mutations*. The tree says
`eighteen mutations` at `4558feb^`. Neither figure is in the tree now, so
nothing needs fixing — but the hand-over's number is not the one that was
removed.

## ⬜ 6 — Round 2's committed report did change wording, not only marking

The hand-over states that the reviewer's prose *kept every word and took the
`NAME NOT IN TREE` marker instead*.
`seal/specs/1789347354-…/rounds/round-2-report.md:101-105` shows otherwise:

| | Round 2 wrote | `074e6bb` committed |
|---|---|---|
| joining clause | `constant, which is how` | `constant. NAME NOT IN TREE` + `That is how` |

A comma became a full stop, `which` became `That`, and a marker line was
inserted mid-sentence. The meaning is unchanged and the marker was the right
mechanism, so this is a correction to the account rather than to the file: a
reviewer's committed report is the record of what that reviewer wrote, and the
hand-over should say a word was substituted to make room for the marker.

## ⬜ 7 — `round-2.md` still says its fixes are not yet written, in the commit that applied them

`seal/specs/1789347354-…/rounds/round-2.md:10` reads
`| Fixes checked by | nobody — the fixes are not yet written |`. The same
commit, `dd4431f`, updated the two sibling cells carrying that identical
phrase — `Contract changes` and `New units` — and left this one. Round 1's
record reads `round-2` in that cell, which is the convention
`skills/code-review/scripts/round_record.py` implements when the next round
lands. Setting it to `round-3` is the orchestrator's write, not a fix pass's,
so this is here to make sure it is not left behind.

## What round 2's closures were checked against

Every inherited verdict was re-derived rather than adopted. The four the
hand-over asked about:

- **Ledger row 2's five measurements** — all five re-measured, all five true.
  The table is under `## Executed probes`.
- **`bin/evidence-check .`** — exit 0 at `dd4431f`. The marker sits on the
  line carrying the name it exempts, and `AT_MOST_ONE_MORE_CEILING` resolves
  to `tests/test_the_rules_have_one_owner.py:439`.
- **⬜ 4 answered rather than fixed** — sound. `round-2.md:47` names `5671c44`
  as a verdict location, so amending it would orphan a SHA a committed record
  points at, and `CLAUDE.md` §*the merge method is fixed per direction*
  squashes a feature branch into its release branch, so no subject on this
  branch reaches `main`. Nothing durable is bought by the amendment.
- **The new unit's two arms** — the right two of the five tried. `1)` and
  `12)` each discriminate; `1.` and `3.` do not discriminate under this
  assertion, and `1)x` is one segment under both spellings, so under this
  assertion it would be red rather than green. The conclusion the fix pass
  drew is right for `1.` and `3.`; for `1)x` the word is wrong and the door it
  closed is 🟡 2.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The comment says killing the bullet or heading alternative widens the pattern and is caught; killing either narrows it and turns nothing red | `tests/test_a_corrected_sentence_survives_elsewhere.py:353-356` | open | Executed — bullet alternative replaced by a never-matching pattern: 55 passed, exit 0. Heading alternative likewise: 55 passed. Only the lookahead-dropped mutations turn one arm of `test_a_sentence_wrapped_onto_an_issue_number_is_one_sentence` red. The same sentence stands in ledger row 2's **Notes** cell and `overview.md:33`, and row 2's **Verified behavior** cell contradicts it |
| 🟡 2 | Two mutations of the alternative round 2 pinned are still caught by nothing, and the comment's grounds for leaving each are wrong | `tests/test_a_corrected_sentence_survives_elsewhere.py:358-363`, `skills/code-review/scripts/survivor_check.py:385` | open | Executed — `[.)]` narrowed to `[)]`: 55 passed; a key-level arm on the same text is green at `dd4431f` and red under that narrowing and under the outright kill. `1)x` asserted to stay one segment is green at `dd4431f` and red with `(?=\s)` dropped, so the lookahead `overview.md:33` defers to the repository owner closes with one arm |
| ⬜ 3 | Ledger row 2's headline **Three of the constant's five alternatives are pinned and two are not** is false under both readings of *pinned* | `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md:13` | open | Executed — ten mutations, one per run: 4 pinned / 1 not under *any mutation turns something red*, 2 pinned / 3 not under *killing it turns something red*. Neither is 3/2. A correction by location, and the row folds into `seal/ledger.md` at the release |
| ⬜ 4 | `overview.md` §*Not verified* counts a lookahead among the five alternatives and repeats 🟡 1's wrong direction | `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/overview.md:33` | open | Read — the constant has five alternatives and `(?=\s)` is part of one of them. Executed — killing an alternative narrows the pattern; the row's *widens* is the opposite mutation. The row also omits the `.` half, open after 🟡 2 |
| ⬜ 5 | The memo's *every alternative of both constants … with its lookahead dropped* claims more than ledger rows 1 and 2 record | `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/overview.md:6` | open | Read — two of `BLOCK`'s five alternatives carry no lookahead, and row 1's enumeration never mentions `BLOCK_START`'s `[>|]`, ` ``` ` or `~~~`. Replacing the count was right; the replacement overstates by three alternatives and two lookaheads |
| ⬜ 6 | Round 2's committed report had a word substituted, not only a marker added | `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/rounds/round-2-report.md:104` | open | Read — `constant, which is how` became `constant.` + marker + `That is how`. Meaning preserved, mechanism right; the hand-over's *kept every word* is what is false, not the file |
| ⬜ 7 | `round-2.md`'s `Fixes checked by` still reads *nobody — the fixes are not yet written* in the commit that applied them | `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/rounds/round-2.md:10` | open | Read — `dd4431f` updated the two sibling cells carrying the same phrase and left this one; round 1's record reads `round-2` there. The orchestrator's write when round 3's record lands |
| ⬜ 8 | Ledger row 2's five per-alternative measurements | `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md:13` | answered | Executed — all five re-measured at `dd4431f` and all five true, including the `[-*_]{3,}` narrowing turning the `===` arm alone red and the ordered-list lookahead turning nothing red. Only the headline count over them is wrong, which is ⬜ 3 |
| ⬜ 9 | Round 2's 🟡 1, fixed at `074e6bb` — the ordered-list alternative is pinned | `tests/test_a_corrected_sentence_survives_elsewhere.py:364-380` | answered | Executed — the alternative replaced by a never-matching pattern: 2 failed, 53 passed, both arms of the new case and nothing else. The two arms kept are the two of the five tried that discriminate |
| ⬜ 10 | Contract §15 — the new unit was seen red before it was planted | `tests/test_a_corrected_sentence_survives_elsewhere.py:365` | answered | Executed — independently reproduced, not inherited: killing the alternative takes the module from 55 passed to 2 failed, 53 passed, and the two failures are this case's own arms |
| ⬜ 11 | Round 2's ⬜ 4, answered rather than fixed — `5671c44`'s subject is not amended | `seal/specs/1789347354-…/rounds/round-2.md:47` | answered | Read — `round-2.md`'s verdict row 4 names `5671c44` as its location, so an amend orphans a SHA a committed record points at. `CLAUDE.md` §*the merge method is fixed per direction* squashes a feature branch into its release branch, so no subject survives. The grounds hold |
| ⬜ 12 | The range the hand-over ran `survivor-check` over stopped one commit short of the target | `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value` | answered | Executed — re-run over the full `0bd1f48..dd4431f`, including the record commit the narrower range excluded: exit 0, 965 files examined against 4 removed sentences, no removed wording still standing. No gap |
| ⬜ 13 | The hand-over names the memo's replaced total as *twenty-seven mutations*; the tree removed `eighteen mutations` | `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/overview.md:6` | answered | Read — `git show 4558feb` removes the word `eighteen`. Contract §5: nothing rests on either figure now, so this is a correction to the account and not to the tree |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Round 2's ⬜ 5 — `close` prepends to a grounds cell, so round 1's finding 4 states a pre-fix count under a **fixed** verdict | issue #391 | the repository owner |
| `evidence_check.py#file_units` reads a heading inside a fence as a heading, so three of thirty-six anchored markdown files truncate | `overview.md` §*Not verified* | the repository owner — a change to a gate under `CONTRIBUTING.md` |
| The three-shape joined-list is stated in two carriers and no case counts them | `overview.md` §*Not verified* | the repository owner, as a ticket against `tests/test_the_rules_have_one_owner.py` |

## Paste-ready fixes

🟡 1 — replace the comment at `tests/test_a_corrected_sentence_survives_elsewhere.py:351-363`:

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

🟡 2 — add after `test_an_ordered_list_item_ends_the_segment`, at
`tests/test_a_corrected_sentence_survives_elsewhere.py:381`:

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

⬜ 3 — replace the headline and the closing phrase of ledger row 2's
**Verified behavior** cell:

```
**Two of the constant's five alternatives are pinned against outright deletion and three are not**, measured 2026-09-14 by mutating each in turn — killed, and where it carries a lookahead, with the lookahead dropped — and the row says which rather than claiming the class: killing `[-*_=]{3,}\s*$` turns four arms red and narrowing it to `[-*_]{3,}` turns the `===` arm alone red; killing `\d+[.)](?=\s)` turns two arms red, though **dropping that alternative's lookahead turns nothing red, and neither does narrowing `[.)]` to `[)]`**; the bullet and heading alternatives are pinned only through their lookaheads, each dropping to one red arm of `test_a_sentence_wrapped_onto_an_issue_number_is_one_sentence`, and killing either outright turns nothing red; and **`>`, which carries no lookahead, is pinned by nothing**
```

⬜ 3 — and in the same row's **Notes** cell, replace the final clause:

```
Round 2's 🟡 1 is why the ordered-list alternative was the second taken and `>` was not — dropping the bullet or heading lookahead widens the pattern in the direction this work item argues for and is caught from the other side, where killing this one is caught from neither and merges a real list item into the sentence above it. Killing the bullet or heading alternative outright is caught by nothing either, which is the mutation this row used to describe as covered
```

⬜ 4 — replace `overview.md:33`:

```
| Three mutations of `survivor_check.py#BLOCK` are caught by nothing — `>` killed, the lookahead on `\d+[.)]` dropped, and `[.)]` narrowed to `[)]`; killing the bullet or heading alternative outright narrows the pattern and is caught by nothing either | the repository owner, as a ticket against `survivor_check.py` — round 3 is this work item's last round. Round 3's 🟡 2 carries a measured arm for each of the two that sit on the alternative this branch pinned |
```

⬜ 5 — replace the executed clause of `overview.md:6`:

```
· verified: executed — the four modules below, the record module before and after; each of `survivor_check.py#BLOCK`'s five alternatives mutated in turn, killed and, where it carries a lookahead, with the lookahead dropped, and seven of `round_record.py#BLOCK_START`'s ten likewise, and every sentence this work pins stashed in turn — the results are per-alternative in ledger rows 1 and 2 rather than as a total here, because a count is the third thing this work item got wrong about its own measurements, `bin/evidence-check .`, `--strict`, and the Q5 measurement over 337 terminal rows. Read — the frame, the round-4 report, `seal/ledger.md` R7 and the `issue_claims_check.py` rows. Unverified — the full suite, repository-wide lint and typecheck, which are the sealer's
```

⬜ 7 — `round-2.md:10`, the orchestrator's write when round 3's record lands:

```
| Fixes checked by | round-3 |
```

Needs a fix: yes — 🟡 1 and 🟡 2, both in the new case's comment block and the
mutation space it describes.

Loses a record or crashes: no

🟡 1 is a stated measurement taken in the opposite direction to the one
claimed, and 🟡 2 is two mutations of the alternative this round's fix pinned
that are still caught by nothing, each closing with one measured arm.
Nothing found this round leaves the root or crashes. `survivor_check.py`
scores sentences; every finding is about which mutations of its constant are
observed and about what three documents say was measured. ⬜ 3 through ⬜ 7 are
under `seal/`, so `Needs a fix` does not count them.

## Proof

Opened and read at `dd4431f`, in a `git clone --no-local` checkout:

- `skills/code-review/scripts/survivor_check.py` — `STRUCK`, `WORD`, `BLOCK`,
  `END`, `blank_struck`, `segments`, `Sentence`, `sentences`, `ngrams`
- `skills/code-review/scripts/round_record.py` — `BLOCK_START`,
  `terminal_value`, the `Fixes checked by` references
- `tests/test_a_corrected_sentence_survives_elsewhere.py` — the module
  docstring, the fixture constants, and lines 290-385
- `tests/test_the_rules_have_one_owner.py:439-466`
- `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md` rows 1
  and 2
- `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/overview.md`
- `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/rounds/round-1.md`
  header, `rounds/round-2.md`, `rounds/round-2-report.md:95-110`
- `docs/review-chain-spec.md` §*Fixes checked by*, §*The last round verifies*
- `CONTRIBUTING.md` §*running the suite*, `CLAUDE.md` §*the merge method is
  fixed per direction*, §*no real identifiers*
- `git log 0bd1f48..dd4431f`, full messages of all three commits

Probes were named `test_tmp_*`, run from the clone, and deleted with the clone
before this report was handed over.
