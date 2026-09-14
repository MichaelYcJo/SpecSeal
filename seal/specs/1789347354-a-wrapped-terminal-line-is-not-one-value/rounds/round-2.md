# 1789347354-a-wrapped-terminal-line-is-not-one-value — review round 2

| Field | Value |
|---|---|
| Target SHA | 933c3e0 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 392 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Contract changes | none |
| New units | test_an_ordered_list_item_ends_the_segment (depth 1) |
| Needs a fix | yes — 🟡 1. Four of the five alternatives of `survivor_check.py#BLOCK` are pinned by nothing, and `\d+[.)](?=\s)` is the one whose loss nothing catches in either direction. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The verifying round. Target is the diff of round 1's fixes, `5a2ee45..933c3e0`, three commits, and not the branch — everything before `5a2ee45` had been reviewed by round 1. Round 1's record was committed and its six verdicts inherited; the job was the answers rather than new findings.

Two surfaces in that diff were named exempt from that rule and handed over as finding surfaces, because a unit the fixes created has been reviewed by nobody.

- `test_the_two_spellings_differ_only_by_the_fence_openers` asserts **string equality** of the two patterns after stripping one alternative, where round 1's finding had asked for a case *asserting the two spellings accept and reject the same shapes* — a behavioural claim. The round was asked whether string equality is that pin or a narrower one, and what it does when the two spellings become equivalent but differently written.
- `test_a_whole_line_of_one_marker_ends_the_segment` pins an alternative that predates the branch, and round 1's own paste-ready version of it was **green against the defect it named** — the line above the rule ended in a period and `END` had already cut the sentence there. The fix pass found that and rewrote it. The round was asked to check the rewrite dies under the mutation it claims, and to look for the same trap elsewhere in what landed.

Three acts of the fix pass were handed over as facts rather than left to rediscover: 🟡 4 widened past the reporter's prescription to a third copy in the same file on contract §12 grounds, taking the exception list from four carriers to two; 🟡 5's rewrite as described above; and `survivor-check` reporting two survivors in `phases/phase-4.md` which the pass **excused rather than corrected**, on the grounds that a phase record states what that phase concluded at its own commit. The round was asked to judge the exemption, which is the one place this branch chose an exemption over a correction.

One number in this work item had already been wrong twice — the record module's case count, reported as 117 over ten new cases where the tree held 118 over eleven, corrected to 118 and then to 119. The round was told to count it itself, because the ledger row folds into `seal/ledger.md` at the release and a wrong count outlives the branch.

The round was also told that round 1's verdict table had carried six confirmation rows the reviewer left unnumbered, that `new` accepted them and `close` refused the table, that they were renumbered by hand on a generated file, and that this is #321's defect with its second measured occurrence recorded there — and asked only to check the renumbering altered no row's content.

**One statement in the spawn prompt was wrong and the round corrected it**: round 1 was described as closing zero deferred, which is the fix table's count. The record's own Deferred section carries three rows — two closed in `overview.md` and one sent to #391.

What the orchestrator had already executed at `5671c44`, handed over so the round would not repeat it: four modules — `test_the_record_is_generated.py`, `test_a_corrected_sentence_survives_elsewhere.py`, `test_the_rules_have_one_owner.py`, `test_docs_line_wrap.py` — 243 passed, exit 0; `survivor-check --range 5a2ee45..5671c44 --exempt …` exit 0; and the two-spellings case read at its coordinates.

The round was required to number every row of its verdict table including confirmations, because the unnumbered shape had cost this work item a hand-edit on a generated file an hour earlier. The broad gate was withheld by name as the sealer's single act after the rounds settle.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | 🟡 5 closed one of five unpinned alternatives of one constant; `\d+[.)](?=\s)` is the one whose loss nothing catches in either direction | `skills/code-review/scripts/survivor_check.py:384`, `tests/test_a_corrected_sentence_survives_elsewhere.py` | **fixed** `074e6bb` | fixed at 074e6bb; Executed — each of the five alternatives mutated to match nothing in turn: only `[-*_=]{3,}\s*$` turns the module red (4 failed, 49 passed); the other four leave 53 passed. Contract §12: the finding named an instance and the cause is the whole retyped constant |
| ⬜ 2 | Ledger row 2's **Executed** sentence *every alternative of the constant is now mutated separately and each kills only its own arms* is false under both readings of *mutated* | `seal/ledger/1789347354-a-wrapped-terminal-line-is-not-one-value.md` row 2 | **fixed** `074e6bb` | fixed at 074e6bb; Executed — alternative killed: 4 of 5 leave 53 passed. Lookahead dropped: `\d+[.)](?=\s)` leaves 53 passed, the bullet and heading lookaheads each turn one arm red. A correction by location, and the row folds into `seal/ledger.md` at the release |
| ⬜ 3 | 🟡 4's widening is correct and leaves the finding's second half open — the list is in two carriers and no case counts them, where the module that took the fix already owns the idiom | `docs/review-handoff-protocol.md:308`, `skills/code-review/scripts/round_record.py:1247`, `tests/test_the_rules_have_one_owner.py` | answered | The state round 1's finding named — four carriers with nothing comparing them — is gone. The two that remain are one per implementation: the protocol states the rule for a second implementation, and the constant's comment documents the code beside it, which is the ordinary owner-plus-code relationship this repository has everywhere rather than the eight-carrier state `test_the_rules_have_one_owner.py` exists for. The residual risk is real and closing it is a walk, which `agents/smith.md` names among the mechanism a fix pass may not add — and round 3 is this work item's last round, so a walk written now ships unread. Recorded in `overview.md` §*Not verified* with the repository owner named, as a ticket against that module |
| ⬜ 4 | `5671c44`'s subject says phase 4's record *says where the correction lives*; the record was not touched | `5671c44` commit subject | answered | Amending `5671c44`'s subject is the wrong repair twice over. That commit is inside the range round 2 reviewed and round 2's record names it, so rewriting it orphans a SHA a record points at; and a feature branch squashes into its release branch, so no commit subject on this branch survives the merge at all. Nothing durable is bought |
| ⬜ 5 | `close` prepends to a grounds cell, so finding 4's record now states the pre-fix carrier count under a **fixed** verdict | `seal/specs/1789347354-…/rounds/round-1.md` verdict row 4 | deferred #391 | #391 |
| ⬜ 6 | 🟡 5's rewrite dies under the mutation it claims, and discriminates per shape | `tests/test_a_corrected_sentence_survives_elsewhere.py:328` | answered | Executed — the alternative mutated to match nothing: 4 failed, 49 passed, where round 1's paste-ready form stayed 49 green. Narrowed to `[-*_]{3,}`: the `===` arm alone goes red |
| ⬜ 7 | The equality pin is stronger than the claim `plan.md` named, not narrower, and its cost is a false red on a rewrite that changes nothing | `tests/test_the_record_is_generated.py:539` | answered | Executed — an alternative added to the model alone turns it red, which is 🟡 1's defect closed. `[-*+]` rewritten `[*+-]`, the same character class, also turns it red: 1 failed, 118 passed. The failure names both patterns, so a cosmetic red explains itself |
| ⬜ 8 | The record module's case count | `tests/test_the_record_is_generated.py` | answered | Executed — 119 passed, exit 0 at `933c3e0`. `overview.md` and ledger row 2 both say 119 |
| ⬜ 9 | The survivors exemption over a correction | `seal/specs/1789347354-…/survivors.md` | answered | Executed — `survivor-check --range 5a2ee45..933c3e0` with the exemption file: 965 files, 25 removed sentences, both survivors excused, exit 0. Read — the grounds match `spec.md` §*Scope*, the anchors are quotes, and all three present-tense carriers of the correction check out |
| ⬜ 10 | The six renumbered rows altered no content | `seal/specs/1789347354-…/rounds/round-1.md` | answered | Read — the diff changes the `#` cell of each of the six and no other character |
| ⬜ 11 | The `-` underline caveat added by 🟡 6's fix is true, and is stated in two prose carriers with no case behind it | `docs/review-handoff-protocol.md:304`, `skills/code-review/scripts/round_record.py:1240` | answered | Executed — `--` matches neither the model's nor the generator's pattern; `=` and `==` match both. The claim holds today; a later narrowing of `=+` would falsify both copies with nothing red |
| ⬜ 12 | The ledger anchors survive the fix range | `seal/ledger.md`, `seal/ledger/1789347354-…md` | answered | Executed — `evidence_check.py .` at `933c3e0`: 1191 ok · 0 drifted · 0 broken, records arm 0 refused · 0 drifted, exit 0 |
| ⬜ 13 | Round 1 deferred three rows, not zero | `seal/specs/1789347354-…/rounds/round-1.md` §*Deferred* | answered | Read — three rows; two are closed in `overview.md` §*Not verified* and the third is routed to #391. Contract §5, the prompt's aggregate checked rather than taken |

## Paste-ready fixes

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
```
The whole-line alternative is mutated to match nothing and all four of its
arms go red; the bullet and heading lookaheads each turn one arm of
`test_a_sentence_wrapped_onto_an_issue_number_is_one_sentence` red when
dropped. The `>` and `\d+[.)]` alternatives are pinned by nothing and are
handed over.
```
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
```
docs: the two survivors of the fix range are excused, and the grounds are a quote (#339)
```

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `evidence_check.py#file_units` reads a `##` line inside a fenced block as a heading; three of thirty-six anchored markdown files affected, `seal/ledger.md` R7 under-covered by 81 lines | `overview.md` §*Not verified*, and it is a change to a gate | the repository owner — carried from round 1 unchanged, and this round did not reopen it |
| #309's two `close` defects, and `close` prepending to a stale grounds cell (⬜ 5 above) | #391, in the `release: 0.11.4` milestone | the third work item of this release |
