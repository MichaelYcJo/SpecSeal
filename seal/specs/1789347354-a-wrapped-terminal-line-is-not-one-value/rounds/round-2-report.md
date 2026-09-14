# 1789347354-a-wrapped-terminal-line-is-not-one-value — review round 2 report

Round 2 is the verifying round. Its target is the diff of round 1's fixes —
`5a2ee45..933c3e0`, three commits, HEAD `933c3e0` — and not the branch. Round 1
reviewed `7f47eed`; everything before `5a2ee45` is inherited rather than
re-derived.

Six verdicts came in closed. Five of the six are actually closed, and the sixth
— 🟡 5 — is closed at the coordinate it named and open one alternative over in
the same constant. That is the one finding this round opens, and the sentence
the fix pass wrote into the ledger fragment asserts the opposite of it.

Everything below was read or executed in a `git clone --no-local` of the
repository at `933c3e0`, with its own virtual environment. Nothing was written
in the working tree except this report.

## The fix that stopped at the coordinate instead of the class

Round 1's 🟡 5 said that `survivor_check.py#BLOCK`'s whole-line alternative
`[-*_=]{3,}\s*$` was pinned by nothing, and its argument was not about that
alternative in particular. The argument was that phase 4 retyped the whole
constant, which is the cheapest moment its alternatives will ever have to be
pinned. That argument covers every alternative of the constant equally.

The fix pass pinned one of them. Mutated to match nothing, each of the
constant's five alternatives does this to
`tests/test_a_corrected_sentence_survives_elsewhere.py`:

| Alternative killed | The module |
|---|---|
| `[-*+](?=\s)` | 53 passed |
| `\#{1,6}(?=\s\|$)` | 53 passed |
| `>` | 53 passed |
| `\d+[.)](?=\s)` | 53 passed |
| `[-*_=]{3,}\s*$` | **4 failed**, 49 passed |

Four of the five can be deleted outright and the suite says nothing. Round 1's
🟡 5 is one of five instances of one cause, and one instance was closed —
which is what contract §12 names by name.

**The `\d+[.)](?=\s)` alternative is the one worth taking**, and it is worth
taking for a reason the other three do not share. Killing the bullet or the
heading alternative widens the pattern in the direction this whole work item
argues for — more prose joins, nothing is truncated — and it is caught from
the other side by
`test_a_sentence_wrapped_onto_an_issue_number_is_one_sentence`, which goes red
when either lookahead is dropped. Killing `\d+[.)](?=\s)` is caught by nothing
in either direction: a genuine `1) …` list item merges into the sentence above
it, an n-gram crosses a boundary that is real, and the module scores a
survivor that is two sentences. That is the same consequence the constant's own
comment gives as its reason for existing.

**One half of it cannot be pinned by this module, and the paste-ready says so.**
`END` ends a sentence at `.` before whitespace, so an arm written `1.` is green
whatever `BLOCK` does — which is exactly why round 1's own paste-ready for 🟡 5
was green against the defect it named. Measured: with `\d+[.)](?=\s)` mutated
to match nothing, `1)` and `12)` join across the boundary and `1.` and `3.` do
not. The case takes the two arms that can die and leaves the `.` half to the
comment.

## Then the ledger fragment says the class is closed

Row 2 of `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md`
carries this, under **Executed**:

> Every alternative of the constant is now mutated separately and each kills
> only its own arms

The table above is that sentence executed, and it is false under both readings
of *mutated*. Killing the alternative outright: four of five kill nothing.
Dropping only the lookahead, which is the narrower reading phase 4 used:
`\d+[.)](?=\s)` still kills nothing, while the bullet and heading lookaheads
each turn one arm of
`test_a_sentence_wrapped_onto_an_issue_number_is_one_sentence` red.

This row folds into `seal/ledger.md` at the release. It is the third wrong
claim in this one row — 117 over ten new cases, then 118 over eleven, and now
this — and the first two were numbers a reader could check at a glance. This
one reads as a closed class.

Either resolution makes it true: plant the case and the sentence stands, or
narrow the sentence to the two arms and the one alternative that were actually
measured. The paste-ready blocks below carry both, because the choice is the
smith's.

## The three things the fix pass did on its own judgement

**🟡 4's widening is right, and it leaves a durability gap the module it edited
already knows how to close.** The reporter's paste-ready touched
`agents/warden.md` alone; the fix pass also took the copy in
`terminal_value`'s docstring, on contract §12 grounds. Counted at `933c3e0`,
the three-shape list — an HTML tag, `**bold**`, an indented run of prose —
now lives in `docs/review-handoff-protocol.md:308` and
`skills/code-review/scripts/round_record.py:1247`, and nowhere else. Four to
two, and the two left are one per implementation: the protocol states the
rule, the constant's comment documents the code beside it. That is a different
thing from four carriers of one sentence, and the widening was the correct
call.

What did not come with it is the half of round 1's finding that was written in
its grounds rather than in its paste-ready — *no case compares any two*. Still
true. `tests/test_the_rules_have_one_owner.py` pins the warden's half of the
split and nothing counts the list's carriers, where the same module already
owns the idiom for it: `occurrences(...)` against a `_CEILING` constant, which
is how `AT_MOST_ONE_MORE_CEILING` holds a different sentence to its two
carriers. The list can grow back to four with nothing red.

**🟡 5's rewrite dies under the mutation it claims.** With `[-*_=]{3,}\s*$`
mutated to match nothing, all four arms of
`test_a_whole_line_of_one_marker_ends_the_segment` go red and the module goes
4 failed / 49 passed — where round 1's own paste-ready form stayed 49 green.
The rewrite earns it by dropping the full stop above the rule, and the comment
in the case says why. It also discriminates rather than failing as a block:
narrowing the class to `[-*_]{3,}` kills the `===` arm and leaves the other
three passing.

**The survivors call is sound.** `survivor-check` over the full fix range
`5a2ee45..933c3e0` — not only the range the orchestrator ran, which stopped at
`5671c44` — examined 965 files against 25 removed sentences and exits 0 with
both survivors excused. Both are halves of one sentence in
`phases/phase-4.md`, both anchored on a quote that dies the moment either half
is edited, and the grounds are the right ones: a phase record asserts a past
state, and `spec.md` §*Scope* refuses to rewrite past-state records for the
same reason. The correction is where a reader acts on it, and all three places
check out — ledger row 2 carries it, `overview.md` §*Not verified* closes the
row with a ✅ and what closed it, and the fix table is in the hand-back. This
is the one place the branch chose an exemption over a correction and it chose
correctly.

The commit that wrote it is titled *phase 4's record keeps what phase 4
concluded, and says where the correction lives*. The record says nothing of
the kind: `5671c44` adds `survivors.md` and touches no other file, and
`phases/phase-4.md` is byte-identical across the whole fix range. The half of
the subject after the comma describes `survivors.md`, not the record.

## What the count actually is

119. `tests/test_the_record_is_generated.py` at `933c3e0` runs 119 passed,
exit 0 — counted by running it, not by reading the row. `overview.md` says
*107 at the base, 118 after, 119 with round 1's pin* and the ledger row says
*107 → 118 green, and 119 once round 1's fix pass added the pin below*. Both
are right.

## The renumbering altered no content

Rows 7 through 12 of round 1's verdict table changed in exactly one place
each: the `#` cell went from `—` to `⬜ 7` … `⬜ 12`. Finding, Location,
Verdict and Grounds are byte-identical across `933c3e0`'s diff for all six
rows. The hand-edit did what #321 forced it to do and nothing else.

One thing the renumbering could not repair, and it is `close`'s shape rather
than the editor's. Finding 4's Grounds cell now reads *fixed at 0293739; Read
— `docs/review-handoff-protocol.md:305`, `round_record.py:1243` and `:1296`
carry the same list; grep finds no case pinning them together*. Two of those
three carriers were emptied by the very commit the cell names. A reader of the
record is told the pre-fix state under a **fixed** verdict, because `close`
prepends to the grounds rather than replacing them. Recorded here so it is not
rediscovered; it belongs with #321 rather than with this branch.

## One correction to the handover

The prompt that spawned this round says round 1 closed *zero deferred*. Round
1's record carries three Deferred rows — the `file_units` fence defect, #309's
two `close` defects routed to #391, and whether `survivor-check` over this
branch's range reports anything. Two of the three are now closed in
`overview.md` §*Not verified*, which is why they are not re-litigated here.
Contract §5: the aggregate was checked rather than taken.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | 🟡 5 closed one of five unpinned alternatives of one constant; `\d+[.)](?=\s)` is the one whose loss nothing catches in either direction | `skills/code-review/scripts/survivor_check.py:384`, `tests/test_a_corrected_sentence_survives_elsewhere.py` | open | Executed — each of the five alternatives mutated to match nothing in turn: only `[-*_=]{3,}\s*$` turns the module red (4 failed, 49 passed); the other four leave 53 passed. Contract §12: the finding named an instance and the cause is the whole retyped constant |
| ⬜ 2 | Ledger row 2's **Executed** sentence *every alternative of the constant is now mutated separately and each kills only its own arms* is false under both readings of *mutated* | `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md` row 2 | open | Executed — alternative killed: 4 of 5 leave 53 passed. Lookahead dropped: `\d+[.)](?=\s)` leaves 53 passed, the bullet and heading lookaheads each turn one arm red. A correction by location, and the row folds into `seal/ledger.md` at the release |
| ⬜ 3 | 🟡 4's widening is correct and leaves the finding's second half open — the list is in two carriers and no case counts them, where the module that took the fix already owns the idiom | `docs/review-handoff-protocol.md:308`, `skills/code-review/scripts/round_record.py:1247`, `tests/test_the_rules_have_one_owner.py` | open | Executed — grep at `933c3e0` finds the three-shape list in exactly those two places, four before. Read — `AT_MOST_ONE_MORE_CEILING` is the same module's existing occurrence-ceiling idiom, unused here. Answerable with grounds: two carriers one per implementation is not the four-carrier state |
| ⬜ 4 | `5671c44`'s subject says phase 4's record *says where the correction lives*; the record was not touched | `5671c44` commit subject | open | Read — the commit adds `survivors.md` and nothing else; `phases/phase-4.md` is byte-identical across `5a2ee45..933c3e0`. The clause describes `survivors.md` |
| ⬜ 5 | `close` prepends to a grounds cell, so finding 4's record now states the pre-fix carrier count under a **fixed** verdict | `seal/specs/1789347354-…/rounds/round-1.md` verdict row 4 | open | Read — the cell names `:1296` as carrying the list; `0293739` emptied it. Belongs with #321, not with this branch |
| ⬜ 6 | 🟡 5's rewrite dies under the mutation it claims, and discriminates per shape | `tests/test_a_corrected_sentence_survives_elsewhere.py:328` | answered | Executed — the alternative mutated to match nothing: 4 failed, 49 passed, where round 1's paste-ready form stayed 49 green. Narrowed to `[-*_]{3,}`: the `===` arm alone goes red |
| ⬜ 7 | The equality pin is stronger than the claim `plan.md` named, not narrower, and its cost is a false red on a rewrite that changes nothing | `tests/test_the_record_is_generated.py:539` | answered | Executed — an alternative added to the model alone turns it red, which is 🟡 1's defect closed. `[-*+]` rewritten `[*+-]`, the same character class, also turns it red: 1 failed, 118 passed. The failure names both patterns, so a cosmetic red explains itself |
| ⬜ 8 | The record module's case count | `tests/test_the_record_is_generated.py` | answered | Executed — 119 passed, exit 0 at `933c3e0`. `overview.md` and ledger row 2 both say 119 |
| ⬜ 9 | The survivors exemption over a correction | `seal/specs/1789347354-…/survivors.md` | answered | Executed — `survivor-check --range 5a2ee45..933c3e0` with the exemption file: 965 files, 25 removed sentences, both survivors excused, exit 0. Read — the grounds match `spec.md` §*Scope*, the anchors are quotes, and all three present-tense carriers of the correction check out |
| ⬜ 10 | The six renumbered rows altered no content | `seal/specs/1789347354-…/rounds/round-1.md` | answered | Read — the diff changes the `#` cell of each of the six and no other character |
| ⬜ 11 | The `-` underline caveat added by 🟡 6's fix is true, and is stated in two prose carriers with no case behind it | `docs/review-handoff-protocol.md:304`, `skills/code-review/scripts/round_record.py:1240` | answered | Executed — `--` matches neither the model's nor the generator's pattern; `=` and `==` match both. The claim holds today; a later narrowing of `=+` would falsify both copies with nothing red |
| ⬜ 12 | The ledger anchors survive the fix range | `seal/ledger.md`, `seal/ledger/1789347354-…md` | answered | Executed — `evidence_check.py .` at `933c3e0`: 1191 ok · 0 drifted · 0 broken, records arm 0 refused · 0 drifted, exit 0 |
| ⬜ 13 | Round 1 deferred three rows, not zero | `seal/specs/1789347354-…/rounds/round-1.md` §*Deferred* | answered | Read — three rows; two are closed in `overview.md` §*Not verified* and the third is routed to #391. Contract §5, the prompt's aggregate checked rather than taken |

## Executed probes

| What was run | Result |
|---|---|
| `pytest tests/test_the_record_is_generated.py` at `933c3e0` | 119 passed, exit 0 |
| `pytest tests/test_a_corrected_sentence_survives_elsewhere.py` at `933c3e0` | 53 passed, exit 0 |
| `pytest tests/test_the_rules_have_one_owner.py` at `933c3e0` | 48 passed, exit 0 |
| `survivor_check.py#BLOCK`, each of the five alternatives mutated to match nothing in turn | `[-*_=]{3,}\s*$`: 4 failed, 49 passed. Bullet, heading, `>`, `\d+[.)]`: 53 passed each — four alternatives pinned by nothing |
| The same constant, each lookahead dropped instead | Bullet and heading: 1 failed each, both arms of `test_a_sentence_wrapped_onto_an_issue_number_is_one_sentence`. `\d+[.)]`: 53 passed |
| `survivor_check.py#BLOCK` narrowed to `[-*_]{3,}\s*$` | 1 failed, 3 passed — the `===` arm alone, so the new case discriminates per shape |
| The proposed ordered-list arms, with `\d+[.)](?=\s)` mutated to match nothing in memory | `1)` and `12)` join across the boundary; `1.` and `3.` do not — `END` cuts at the full stop whatever `BLOCK` does |
| An alternative added to `.github/scripts/issue_claims_check.py#BLOCK_START` alone | `test_the_two_spellings_differ_only_by_the_fence_openers`: 1 failed — the drift 🟡 1 named is caught |
| `round_record.py#BLOCK_START`'s `[-*+]` rewritten `[*+-]`, the same class | 1 failed, 118 passed — the pin is string equality, so a behaviour-identical rewrite goes red |
| The three carriers' patterns matched against nine line shapes | The sibling differs from the other two on `=` and `==`, which its comment does not name; the `\|` and fence differences it does name |
| `survivor_check.py --range 5a2ee45..933c3e0 --exempt …/survivors.md` | 965 files, 25 removed sentences, 2 survivors, both excused, exit 0 |
| `evidence_check.py .` at `933c3e0` | 1191 ok · 0 drifted · 0 broken · 0 external · 0 old-format; records arm 2 work items read, 0 refused, 0 drifted; exit 0 |
| The broad gate — the full suite, repository-wide `ruff check`, the typecheck | Not run by this round and not yet run by anybody at this SHA. It is the sealer's single act under contract §2, and this report leaves 🟡 1 open, so it is not yet due |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `evidence_check.py#file_units` reads a `##` line inside a fenced block as a heading; three of thirty-six anchored markdown files affected, `seal/ledger.md` R7 under-covered by 81 lines | `overview.md` §*Not verified*, and it is a change to a gate | the repository owner — carried from round 1 unchanged, and this round did not reopen it |
| #309's two `close` defects, and `close` prepending to a stale grounds cell (⬜ 5 above) | #391, in the `release: 0.11.4` milestone | the third work item of this release |

## Paste-ready fixes

The case for 🟡 1, in `tests/test_a_corrected_sentence_survives_elsewhere.py`,
beside the whole-line case the fix pass planted:

```python
# The ordered-list alternative, the second of the constant's five that nothing
# pins — same constant, same retyping, same argument as round 1's 🟡 5. Only
# the `)` half can be pinned here: `END` ends a sentence at `.` before
# whitespace, so a `1.` arm is green whatever `BLOCK` does, which is what made
# round 1's first attempt at the whole-line case useless.
@pytest.mark.parametrize("opener", ["1)", "12)"])
def test_an_ordered_list_item_ends_the_segment(opener):
    """A list item is a block, so the prose above it is a sentence of its own.

    Without this alternative a claim hard-wrapped above a list and the list's
    first item land in one segment, and an n-gram crosses a boundary that is
    real — the mis-scoring direction this module's constant exists to avoid,
    rather than the truncation `round_record.py` guards."""
    reader = module()
    # No full stop above the item, on purpose: the block boundary has to be
    # the only thing that can end this sentence.
    text = f"the claim above the item\n{opener} an unrelated claim below it"
    keys = [sentence.key for sentence in reader.sentences("docs/probe.md", text)]
    assert not any("above the item" in k and "below it" in k for k in keys), (
        f"{opener!r} opens a list item and the segment ran straight through "
        f"it: {keys!r}"
    )
```

If ⬜ 2 is answered by planting that case, ledger row 2's sentence stands as
written once the arm count is right. If it is answered by narrowing the
sentence instead, this is what was actually measured:

```
The whole-line alternative is mutated to match nothing and all four of its
arms go red; the bullet and heading lookaheads each turn one arm of
`test_a_sentence_wrapped_onto_an_issue_number_is_one_sentence` red when
dropped. The `>` and `\d+[.)]` alternatives are pinned by nothing and are
handed over.
```

For ⬜ 3, the occurrence ceiling the module already has an idiom for, in
`tests/test_the_rules_have_one_owner.py`:

```python
JOINED_SHAPES = "with an HTML tag, with `**bold**`, or with an indented run of prose"
JOINED_SHAPES_CEILING = 2


def test_the_joined_shapes_are_listed_in_two_places():
    """The protocol states the narrowing for a second implementation; the
    constant's comment documents the code beside it. Round 1's 🟡 4 found the
    same list in four places with nothing counting them, and counting them is
    what keeps the fix from being undone one restatement at a time."""
    found = occurrences(JOINED_SHAPES)
    assert found.get("/".join(PROTOCOL)) == 1, found
    assert sum(found.values()) <= JOINED_SHAPES_CEILING, found
```

For ⬜ 4, the commit subject that `5671c44` should have carried — it matters
because the branch squashes and the subject becomes a line in the release
branch's history:

```
docs: the two survivors of the fix range are excused, and the grounds are a quote (#339)
```

## Proof block

Opened, at `933c3e0` unless stated:

- `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/rounds/round-1.md`
- `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/overview.md`
- `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/survivors.md`
- `seal/specs/1789347354-a-wrapped-terminal-line-is-not-one-value/phases/phase-4.md`
- `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md`
- `skills/code-review/scripts/round_record.py` — `BLOCK_START` and `terminal_value`
- `skills/code-review/scripts/survivor_check.py` — `WORD`, `BLOCK`, `END`
- `.github/scripts/issue_claims_check.py` — `BLOCK_START`
- `agents/warden.md`, `docs/review-handoff-protocol.md`
- `tests/test_the_record_is_generated.py`,
  `tests/test_a_corrected_sentence_survives_elsewhere.py`,
  `tests/test_the_rules_have_one_owner.py`
- `git diff 5a2ee45..933c3e0`, and `git show` for each of the three commits

Not opened: the branch before `5a2ee45`, which round 1 reviewed; PR #392's
body; `spec.md`, `plan.md` and `questions.md`, whose claims reached this round
through round 1's verdicts rather than directly.

Needs a fix: yes — 🟡 1. Four of the five alternatives of `survivor_check.py#BLOCK` are pinned by nothing, and `\d+[.)](?=\s)` is the one whose loss nothing catches in either direction.

Loses a record or crashes: no

Nothing found in this range drops a record or raises. 🟡 1 is a missing pin on
code that is correct today, and ⬜ 2 is a claim in a row that folds into
`seal/ledger.md` at the release — both outlive the branch, neither costs a run
its output.
