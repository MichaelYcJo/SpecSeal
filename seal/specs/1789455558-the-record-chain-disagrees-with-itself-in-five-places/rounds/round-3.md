# 1789455558-the-record-chain-disagrees-with-itself-in-five-places — review round 3

| Field | Value |
|---|---|
| Target SHA | dad4dcd1 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 416 |
| Broad gate | 27c510d4 against release/v0.12.0 |
| Fixes checked by | no fixes to check |
| Contract changes | none — no fixes to check |
| New units | none — no fixes to check |
| Needs a fix | yes — 🟡 1, the case asserting the fold's safety does not grow with the sweeps it names, so a folded member or a seam-carrying phrase joining either sweep goes unchecked. |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

The last record of the run. Round 1 met the floor and round 2 — a verifying
round that opened four findings — closed on a fix, so the one reopening is
spent and this record ends the run whatever it finds
(`docs/review-chain-spec.md` §*The reopening — one, and then the run is
capped*).

Its target is the diff of round 2's fixes, `fc204d34..dad4dcd1`, and its job is
the answers: are round 2's four verdicts actually closed. The one unit that fix
pass added — `test_flat_is_what_folds_the_seam_and_it_folds_python_only` — is
exempt from that rule and was read as a finding surface.

Three claims the fix pass made about its own work were checked rather than
trusted: that `questions.md` Q6 now quotes the sentence that ships, that the
two corrected ledger rows were re-read rather than only re-stamped, and that
the divergence row generalising this branch's own shape is true.

The round was also asked to route rather than only to report, since no round
follows it.

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

## Paste-ready fixes

```python
# between, which is why `orchestrator's segments` is safe. The set that has to
# be checked is closed rather than long: `flat` folds only `.py` members, so a
# phrase searched in a markdown file is out of the fold's reach entirely, and
# `test_folding_the_seam_cannot_hide_an_instance_it_would_have_found` asserts
# the property over every phrase either sweep searches for in a folded member.
```
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
```markdown
| `spec.md` A8's *Then* is false of the shipped message, and a case asserts the opposite | A8: *it refuses the row with a message that **names the verdict word as outside the vocabulary**, names the vocabulary, and does not name 🔴*, and the *What a person sees* row repeats it | The message names neither *outside the vocabulary* nor *an unrecognised verdict*. It reads *not one of the words that close a row*, renders the words from `CLOSED_WORDS`, and names no 🔴 | A8 was written before round 1 read it. Its phrase reached `open` — the word `agents/warden.md` prescribes — so it stated a rule the file does not hold, and round 1's 🟡 1 removed it; `test_an_unrecognised_verdict_is_refused_by_its_own_name` now asserts `"outside the vocabulary" not in line`, so the scenario and the case contradict each other. Round 2's ⬜ 4 removed *unrecognised verdict* for the same reason, which leaves A8's title stale too. **What A8 still gates is met:** the row is refused, the vocabulary is named, and 🔴 is absent. Only the spelling of the verdict clause diverged, twice, each time toward a sentence the checker can actually hold (round 3's ⬜ 2) |
```
```markdown
What a later reader should take from it: the three have one shape and two different causes, so one rule does not close them. For the fold, pin the function the production path calls, never the helper beside it (round 2's 🟡 1). For round 1's ⬜ 4, check that the case's own assertion can fire before the fixture's guard does. The count is the branch's subject plus two repairs, not three repairs.
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/chain_check.py#open_row_reason` | round 1's 🟡 1 — fixed |
| round-1 | `tests/test_one_word_one_meaning.py#test_no_instructing_document_leaves_an_instance_anonymous` | round 1's 🟡 2 — fixed |
| round-1 | `seal/specs/1789455558-…/spec.md` §A5 | round 1's ⬜ 3 — answered |
| round-1 | `tests/test_the_fixes_close_the_record.py#test_a_unit_added_by_a_fix_outside_every_earlier_unit_is_depth_one` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#fix_table` | round 1's ⬜ 5 — answered |
| round-1 | `seal/ledger.md` at `release/v0.12.0:2204`, superseded by `seal/ledger/1789455558-….md:13` | round 1's ⬜ 6 — answered |
| round-1 | `seal/ledger.md:2201` | round 1's ⬜ 7 — answered |
| round-1 | `skills/code-review/scripts/round_record.py#close`, `#inherited_rows` | round 1's 🟢 — verified |
| round-1 | `skills/code-review/scripts/round_record.py#reach_forward` | round 1's 🟢 — verified |
| round-1 | `seal/ledger.md`, `seal/ledger/1789455558-….md` | round 1's 🟢 — verified |
| round-1 | `seal/config.md` | round 1's ❓ — out of verified scope |
| round-2 | `tests/test_one_word_one_meaning.py#flat` | round 2's 🟡 1 — fixed |
| round-2 | `tests/test_one_word_one_meaning.py#LITERAL_SEAM` | round 2's ⬜ 2 — fixed |
| round-2 | `skills/code-review/scripts/chain_check.py#open_blocking`, `#open_row_reason` | round 2's 🟢 — verified |
| round-2 | `skills/code-review/scripts/round_record.py#seal`, `tests/test_one_word_one_meaning.py#test_no_instructing_document_leaves_an_instance_anonymous` | round 2's 🟢 — verified |
| round-2 | `seal/ledger.md:2203`, `seal/ledger/1789455558-the-record-chain-disagrees-with-itself-in-five-places.md:13` | round 2's 🟢 — verified |
| round-2 | `seal/ledger.md:1945`, `seal/ledger.md:2201` | round 2's 🟢 — verified |
| round-2 | `tests/test_the_fixes_close_the_record.py#one_finding_inside_one_earlier_unit` | round 2's 🟢 — verified |
| round-2 | `seal/specs/1789455558-…/overview.md`, `seal/specs/1789455558-…/changelog.md` | round 2's 🟢 — verified |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The eleven cells already rendered wrong by #414's cause | already deferred in round 1 to Q1's fourth work item, cut from `release/v0.12.0` | the orchestrating session, at that work item |
| The five other readers of `chain.SEPARATORS` | already deferred in round 1 to a separate work item; `phases/phase-3.md` and Q5 carry the reading | the orchestrating session |
