# Round 3 — the verifying round that ends the run

Target: `fc204d34..dad4dcd1`, round 2's fix range. HEAD is `dad4dcd1` on
`fix/404-405-406-407-408-414-the-record-chain-disagrees-with-itself-in-five-places`
and has not moved. Pull request 416, draft. Everything below was measured in a
`git clone --no-local` of this repository at that SHA, in a `uv` virtual
environment made inside the clone; the working checkout was read and never
written.

## How the four answers and the two findings relate

Round 2's four verdicts are all closed, and the two things this round opened
both sit one step behind them.

```
① 🟡 1 — the fold is held by a case that goes through `flat`      closed
② ⬜ 2 — the fold's comment states the guarantee that holds       closed
③ ⬜ 3 ⬜ 4 — the second arm's sentence says what it can check     closed
        ↓ and one step behind ①②
🟡 1 (new)  the case beside the new one still claims a wider set than it holds
        ↓ and one step behind the records that describe ③
⬜ 2 (new)  `spec.md` A8's *Then* is false of the ship, with nothing admitting it
⬜ 3 (new)  the new divergence row's takeaway rule reaches one of its three
```

## Round 2's 🟡 1 is closed, and all three assertions are load-bearing

Both mutations round 2 measured at 17 passed are now dead, and each is killed
by a different assertion of
`test_flat_is_what_folds_the_seam_and_it_folds_python_only`.

| Mutation | Whole module | Which assertion kills it |
|---|---|---|
| `flat` back to the plain flatten | exit 1 | the first — delete it and the mutation passes |
| the `.endswith(".py")` guard dropped | exit 1 | the third — delete it and the mutation passes |
| the pinned seam in `round_record.py` rewrapped into one literal | exit 1 | the second — delete it and the case goes green while asserting nothing |

The third row is the one worth stating, because round 2's own grounds do not
claim it. The second assertion is not load-bearing against either of the two
mutations, and deleting it changes neither. What it holds is the fixture: with
`round_record.py:4083` rewrapped so the phrase sits in one literal, the case
passes with the second assertion removed and fails with it in place. That is
the decay this branch has now met three times, pinned.

The docstring's quoted fixture text is accurate. `round_record.py:4083-4084`
reads `… cannot see. The "` / `"sealer's mark names a commit …`, which is the
seam the first assertion crosses.

## Round 2's ⬜ 2, ⬜ 3 and ⬜ 4 are closed

The narrower claim about the fold is true of the mechanism. `LITERAL_SEAM`'s
`\1` backreference requires the same quote character on both sides, so a
same-quote seam folds and a mixed-quote seam does not — measured on
`'"the " "seal is taken"'` against `'"the " \'seal is taken\''`. The corrected
`seal/ledger.md:2203` clause, which now says SAME quote character, states what
the code does.

The second arm's sentence holds for every row the selection routes to it.
`open_blocking` selects on `BLOCKING in "".join(seen)` and splits on
`BLOCKING in seen[0]`, and `BLOCKING` is one character, so a join cannot invent
a marker across a cell boundary. Three shapes were driven through the real
selection with the real reader — the marker in Grounds only, the marker in the
Finding cell quoting nothing, and the marker in two cells — and all three are
told they carry a blocking marker, which is true of each. `unrecognised` is
gone from the message, and the case that pins its absence is independently
load-bearing: restoring only that clause and leaving the marker clause alone
turns `test_an_unrecognised_verdict_is_refused_by_its_own_name` and
`test_a_row_reading_open_is_not_told_its_word_is_unrecognised` red and nothing
else.

## Q6 quotes what ships, and the two ledger corrections were read

`questions.md` Q6's block quote matches `open_row_reason`'s second-arm return
character for character. The one difference is markup on a placeholder: Q6
writes `` `<the # cell>` `` in backticks and the message interpolates the cell
bare. Q6 backticks `` `<word>` `` the same way and the code does backtick that
one, so the two placeholders are spelled alike in Q6 and differently in the
code. Nothing a reader acts on.

Both ledger corrections changed content rather than only a hash, which is what
round 2's ⬜ 7 asked for. The shared row's new clause is true, measured above.
The fragment's rows gained the two round-2 narrowings and one new anchor.
`bin/evidence-check --strict .` reads exit 0 in the clone — 1277 ok, 0 drifted,
0 broken, records arm 0 refused.

## 🟡 1 — the case that asserts the fold's safety does not grow with the sweeps it names

`tests/test_one_word_one_meaning.py:415` —
`test_folding_the_seam_cannot_hide_an_instance_it_would_have_found`.

The case builds `swept` as four sources: the literal `"the seal"`, a spread of
`SEAL_BARE_IS_THE_CONCEPT`, and two literals copied from
`test_no_shipped_document_calls_a_spawn_cycle_a_segment`. Only the spread is a
live reference. Its docstring says the property *holds for a set that grows,
where three examples hold only for themselves*, and the module comment at
line 46 says the case asserts it *over the whole phrase set rather than over
examples*.

Measured, two ways, each leaving the case green:

- a third spelling carrying a foldable seam added to the segment sweep, which
  reads `session_cost.py` and `test_session_cost.py`, both folded members
- `chain_check.py` added to `SEAL_SWEPT`, a new folded member whose phrases
  nothing then checks

**Why it is safe today, and why that reason is the finding.** `flat` folds only
when the last path part ends `.py`, so a phrase searched in a markdown file
cannot be cut at all. Exactly four folded members exist across both sweeps —
`seal_stamp.py` and `round_record.py` in `SEAL_SWEPT`, `session_cost.py` and
`test_session_cost.py` in `SEGMENT_SWEPT` — and `swept` is every phrase searched
in them. Of the 33 phrases this module searches for through `flat`, the other 26
are read out of markdown and are out of the fold's reach.

That reason is stated nowhere in the case, so the seven entries read as a longer
list of examples rather than as a closed set, and the next person adding a `.py`
member has nothing telling them to extend it. This is round 2's ⬜ 2 one notch
narrower: the claim moved from false about the mechanism to wider than the
check, and the check still cannot fail for the case that matters.

## ⬜ 2 — `spec.md` A8's *Then* is false of the ship, and nothing admits it

`seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/spec.md:85`
and the same file's line 101.

A8 reads *then it refuses the row with a message that names the verdict word as
outside the vocabulary*. Round 1's 🟡 1 removed that phrase from the message
because it was false about `open`, and
`test_an_unrecognised_verdict_is_refused_by_its_own_name` now asserts
`"outside the vocabulary" not in line`. So the acceptance scenario states the
opposite of what a shipped case pins. Line 101's *What a person sees* row
carries the same sentence in its *After* column.

A8's own title, *an unrecognised verdict is still refused, by its own name*, is
stale for the second reason as well: round 2's ⬜ 4 removed *unrecognised
verdict* from the message.

This is round 1's ⬜ 3 again — an acceptance scenario whose *Then* is false with
nothing admitting it. That round was answered with a divergence row for A5, and
A7 has one too. A8 has none, and the string `A8` occurs exactly once in the
whole work item, in `spec.md` itself.

## ⬜ 3 — the new divergence row's takeaway rule reaches one of the three instances it names

`seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/overview.md:37`.

The row is true where it generalises and loose where it instructs.

- **True.** *The shape is not a bad case — each was seen red against something —
  it is that the thing seen red was not the thing shipped.* That covers all
  three.
- **Reaches one of three.** *What a later reader should take from it: pin the
  function the production path calls, never the helper beside it.* That is the
  fold exactly. It is not round 1's ⬜ 4, whose cause the round recorded as *the
  case-level positive assertion duplicates the fixture guard added in the same
  commit, so it cannot fire* — no helper, no production path, and the rule as
  written would have passed it. Nor is it #406 itself, which was a deleted
  output assertion rather than a case pinning a neighbour.
- **Counts the subject among the repairs.** The heading says *A repair … was
  itself held by nothing, three times*, while the cell's own body says *the work
  item's own subject arriving in its own repairs, twice more* and then lists
  #406 first. Two repairs and the subject, summed to three in the heading.

## ⬜ — `drop the marker` is singular, and a row can carry two

`skills/code-review/scripts/chain_check.py#open_row_reason`. With a 🔴 in two
cells other than the `#` cell, the remedy names one marker and dropping one
leaves the row refused; the reader drops the second on the next run. The old
sentence said *drop the quote* with the same singular, so this range did not
introduce it, and the refusal is self-correcting on a second pass. Reported and
left alone.

## What was not judged

The broad gate. `agent-contract` §2 assigns the full suite, the repository-wide
lint and the typecheck to `agents/sealer.md`, once, after the rounds settle. It
has not been run, by this round or by anything before it. This report leaves
nothing open that needs the fix pass, so the sealer's spawn is what comes due —
not a run for the reading session to assemble.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | the case asserting the fold cannot hide an instance is built on a hand-copied list of seven and claims a set that grows; a seam-carrying phrase joining either sweep, or a new `.py` member joining `SEAL_SWEPT`, leaves it green | `tests/test_one_word_one_meaning.py#test_folding_the_seam_cannot_hide_an_instance_it_would_have_found` | deferred #418 | Executed, two mutations, both exit 0 where the case should be red: a third spelling carrying a seam added to the segment sweep, and `chain_check.py` added to `SEAL_SWEPT`. Read: `flat` folds only `.py` members, so the four folded members across both sweeps are the whole risk surface and `swept` covers them — 7 of the module's 33 searched phrases, the other 26 read out of markdown. The reason is in no comment, so the set reads as examples |
| ⬜ 2 | `spec.md` A8's *Then* says the message names the verdict word as outside the vocabulary; round 1's 🟡 1 removed that phrase and a shipped case asserts its absence, and no divergence row admits it | `seal/specs/1789455558-…/spec.md:85`, `:101` | open | Read: the acceptance scenario and the *What a person sees* row both carry the phrase; `test_an_unrecognised_verdict_is_refused_by_its_own_name` asserts `"outside the vocabulary" not in line`. A5 and A7 each have a divergence row for this shape (round 1's ⬜ 3); `A8` occurs once in the work item, in `spec.md`. The title is stale a second way — round 2's ⬜ 4 removed *unrecognised verdict* |
| ⬜ 3 | the new divergence row's takeaway rule — *pin the function the production path calls, never the helper beside it* — reaches the fold and not the other two instances the same row names, and the heading counts the branch's subject among the repairs | `seal/specs/1789455558-…/overview.md:37` | open | Read: round 1's ⬜ 4 is recorded as *the case-level positive assertion duplicates the fixture guard added in the same commit*, which the rule as written would pass; #406 was a deleted output assertion. The cell's body says *twice more* and lists three, while the heading says *three times* of repairs |
| ⬜ | `drop the marker` is singular and a row can carry a marker in two cells other than the `#` cell | `skills/code-review/scripts/chain_check.py#open_row_reason` | not a defect | Executed against the real selection: a row with 🔴 in the Finding and Grounds cells is refused with one remedy naming one marker. The pre-fix sentence said *drop the quote* with the same singular, so this range did not introduce it, and the second pass corrects the reader |
| 🟢 | round 2's 🟡 1 is closed: the fold is held through `flat`, and each of the three assertions is load-bearing against a different failure | `tests/test_one_word_one_meaning.py#test_flat_is_what_folds_the_seam_and_it_folds_python_only` | verified | Executed, three mutations, all exit 1 where round 2 measured exit 0: `flat` back to the plain flatten, the `.py` guard dropped, and the pinned seam rewrapped into one literal. Deleting the first assertion revives the first mutation, the third revives the second, and the second lets the rewrapped fixture pass with the case asserting nothing. Read: the docstring's quoted fixture matches `round_record.py:4083-4084` |
| 🟢 | round 2's ⬜ 2 is closed: the narrower claim is true of the mechanism, and the case can fail inside its own set | `tests/test_one_word_one_meaning.py#LITERAL_SEAM` | verified | Executed: a same-quote seam folds and a mixed-quote seam does not, so `seal/ledger.md:2203`'s corrected SAME quote character clause is true; a seam-carrying entry added to `SEAL_BARE_IS_THE_CONCEPT` turns the case red. The set's boundary is the separate finding above |
| 🟢 | round 2's ⬜ 3 is closed: the sentence describes the condition the selection tests, for every shape that reaches the arm | `skills/code-review/scripts/chain_check.py#open_row_reason`, `#open_blocking` | verified | Executed against the real selection with the real reader: the marker in Grounds only, in the Finding cell quoting nothing, and in two cells — all three reach the second arm and are told they carry a blocking marker, which is true of each. `BLOCKING` is one character, so `"".join(seen)` cannot invent one across a cell boundary. `open_blocking` is untouched in the fix range |
| 🟢 | round 2's ⬜ 4 is closed, and the case that pins the absence is independently load-bearing | `tests/test_chain_check_at_the_pull_request.py#test_an_unrecognised_verdict_is_refused_by_its_own_name` | verified | Executed: restoring only the *unrecognised verdict* clause and leaving the marker clause alone turns exactly two cases red — that one and `test_a_row_reading_open_is_not_told_its_word_is_unrecognised` — 94 of 96 still passing |
| 🟢 | Q6 quotes the sentence that ships | `seal/specs/1789455558-…/questions.md:20` | verified | Executed: `open_row_reason` called with the placeholders Q6 uses returns Q6's quoted text character for character, except that Q6 backticks the `# cell` placeholder where the message interpolates it bare. Q6 spells both placeholders alike; the code backticks only the verdict |
| 🟢 | the two ledger corrections changed a claim rather than a hash, and the ledger reads clean | `seal/ledger.md:2203`, `seal/ledger/1789455558-….md:12`, `:13` | verified | Executed: `bin/evidence-check --strict .` exit 0 read directly in the clone — 1277 ok · 0 drifted · 0 broken · 0 external, records arm 0 refused. Read: the shared row's new SAME quote character clause and the fragment's two round-2 narrowings are content edits, and the mechanism measurement above says the new clause is true |
| 🟢 | nothing outside `seal/` still pins a phrase this range removed | `tests/`, `skills/`, `hooks/` | verified | Executed: a tree-wide grep for *quotes a blocking finding*, *drop the quote*, *unrecognised verdict* and *can only create a hit* returns only the two cases asserting absence and the two comments naming the old wording in order to reject it. `survivors.md`'s three new exemptions match what the grep finds under `seal/` |
| ❓ | the broad gate — the full suite, the repository-wide lint, the typecheck | `seal/config.md` | out of verified scope | `agent-contract` §2 assigns it to `agents/sealer.md`, once, after the rounds settle. It has not run. Answered by the orchestrating session's sealer spawn, which this report makes due |

## Executed probes

| What was run | Result |
|---|---|
| `tests/test_one_word_one_meaning.py` and `tests/test_chain_check_at_the_pull_request.py` in the clone at `dad4dcd1` | 114 passed, exit 0 read directly |
| `tests/test_the_seal_is_taken_once_by_the_sealer.py` and `tests/test_the_fixes_close_the_record.py` | 153 passed, exit 0 read directly |
| `flat` reverted to the plain flatten, module re-run | **exit 1** — round 2's first mutation is dead |
| the `.endswith(".py")` guard dropped, module re-run | **exit 1** — round 2's second mutation is dead |
| each of the new case's three assertions deleted under each of those two mutations | first assertion revives mutation one, third revives mutation two, second revives neither |
| the pinned seam at `round_record.py:4083` rewrapped into one literal | **exit 1** as shipped; **exit 0** with the second assertion deleted — the fixture guard is what holds |
| `LITERAL_SEAM` on a same-quote seam and on a mixed-quote seam | folded and not folded — the corrected `seal/ledger.md` clause is true |
| a seam-carrying entry added to `SEAL_BARE_IS_THE_CONCEPT` | **exit 1** — the widened case can fail inside its own set |
| a seam-carrying spelling added to the segment sweep, and `chain_check.py` added to `SEAL_SWEPT` | **exit 0** both — coverage probe, the case does not grow with its sweeps (🟡 1) |
| every `flat(...)` read in the module walked by `ast`, and every sweep member classified by extension | 33 phrases searched, 7 in the case's set; 4 folded `.py` members across both sweeps, all covered |
| three row shapes driven through `open_blocking` and `open_row_reason` with the real reader | all three reach the second arm; the sentence is true of each; two markers get one singular remedy |
| only the *unrecognised verdict* clause restored, chain-check module re-run | **exit 1** — 2 failed, 94 passed, the two `open`-row cases |
| `open_row_reason`'s second-arm return compared byte for byte with `questions.md` Q6's block quote | identical but for the backticked `# cell` placeholder |
| `bin/evidence-check --strict .` in the clone, exit read directly | exit 0 — 1277 ok · 0 drifted · 0 broken · 0 external, records arm 0 refused |
| `git log -L` over `open_blocking` across `fc204d34..dad4dcd1` | no commits — the selection is untouched by the fix range |
| tree-wide grep for the four phrases this range removed | only absence assertions and rejecting comments outside `seal/` |
| the broad gate — the full suite, the repository-wide lint, the typecheck | **not yet** — it has not been run, by this round or by anything before it |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The eleven cells already rendered wrong by #414's cause | already deferred in round 1 to Q1's fourth work item, cut from `release/v0.12.0` | the orchestrating session, at that work item |
| The five other readers of `chain.SEPARATORS` | already deferred in round 1 to a separate work item; `phases/phase-3.md` and Q5 carry the reading | the orchestrating session |

## Paste-ready fixes

🟡 1, first half — replace the closing sentence of the module comment at
`tests/test_one_word_one_meaning.py:44-46` (the one beginning *That is what*)
with the reason the set is closed:

```python
# between, which is why `orchestrator's segments` is safe. The set that has to
# be checked is closed rather than long: `flat` folds only `.py` members, so a
# phrase searched in a markdown file is out of the fold's reach entirely, and
# `test_folding_the_seam_cannot_hide_an_instance_it_would_have_found` asserts
# the property over every phrase either sweep searches for in a folded member.
```

🟡 1, second half — in
`test_folding_the_seam_cannot_hide_an_instance_it_would_have_found`, replace the
docstring's *it holds for a set that grows, where three examples hold only for
themselves* clause and add the guard that makes the set closed. The assertion
goes immediately above the existing `for phrase in swept:` loop:

```python
    # Why seven phrases are the whole of what is at risk rather than a longer
    # list of examples: `flat` folds only `.py` members, so a phrase searched
    # in a markdown file cannot be cut at all. These four are the only folded
    # members either sweep reads, and `swept` above is every phrase searched
    # in them. A `.py` member joining a sweep turns this red, because its
    # phrases then need adding above (round 3's 🟡 1).
    assert [p for p in (*SEAL_SWEPT, *SEGMENT_SWEPT) if p[-1].endswith(".py")] == [
        ("skills", "verify", "scripts", "seal_stamp.py"),
        ("skills", "code-review", "scripts", "round_record.py"),
        ("skills", "verify", "scripts", "session_cost.py"),
        ("tests", "test_session_cost.py"),
    ], (
        "a folded member joined a sweep, so a phrase searched in it can be "
        "cut by the fold and belongs in `swept` above"
    )
```

⬜ 2 — a divergence row for `overview.md`'s table, in the shape A5 and A7
already use:

```markdown
| `spec.md` A8's *Then* is false of the shipped message, and a case asserts the opposite | A8: *it refuses the row with a message that **names the verdict word as outside the vocabulary**, names the vocabulary, and does not name 🔴*, and the *What a person sees* row repeats it | The message names neither *outside the vocabulary* nor *an unrecognised verdict*. It reads *not one of the words that close a row*, renders the words from `CLOSED_WORDS`, and names no 🔴 | A8 was written before round 1 read it. Its phrase reached `open` — the word `agents/warden.md` prescribes — so it stated a rule the file does not hold, and round 1's 🟡 1 removed it; `test_an_unrecognised_verdict_is_refused_by_its_own_name` now asserts `"outside the vocabulary" not in line`, so the scenario and the case contradict each other. Round 2's ⬜ 4 removed *unrecognised verdict* for the same reason, which leaves A8's title stale too. **What A8 still gates is met:** the row is refused, the vocabulary is named, and 🔴 is absent. Only the spelling of the verdict clause diverged, twice, each time toward a sentence the checker can actually hold (round 3's ⬜ 2) |
```

⬜ 3 — replace the takeaway sentence in `overview.md:37` and correct the count:

```markdown
What a later reader should take from it: the three have one shape and two different causes, so one rule does not close them. For the fold, pin the function the production path calls, never the helper beside it (round 2's 🟡 1). For round 1's ⬜ 4, check that the case's own assertion can fire before the fixture's guard does. The count is the branch's subject plus two repairs, not three repairs.
```

Needs a fix: yes — 🟡 1, the case asserting the fold's safety does not grow with the sweeps it names, so a folded member or a seam-carrying phrase joining either sweep goes unchecked.
Loses a record or crashes: no

## Proof

Read in the clone at `dad4dcd1`: `tests/test_one_word_one_meaning.py`,
`tests/test_chain_check_at_the_pull_request.py`,
`skills/code-review/scripts/chain_check.py`,
`skills/code-review/scripts/round_record.py`, `README.md:492`.
Read in the working checkout: `rounds/round-1.md`, `rounds/round-2.md`,
`rounds/round-2-report.md`, `rounds/round-2-fixes.md`, `spec.md`, `plan.md`,
`overview.md`, `questions.md`, `survivors.md`, `changelog.md`,
`seal/ledger.md:2203`,
`seal/ledger/1789455558-the-record-chain-disagrees-with-itself-in-five-places.md`,
and the full `fc204d34..dad4dcd1` diff.
Executed: every row of the probes table above, in the clone, in a `uv` virtual
environment made inside it. Every probe file was deleted and both trees are
clean.
Unverified: the broad gate, answered by `agents/sealer.md`.
