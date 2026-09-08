# 1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible — review round 3

| Field | Value |
|---|---|
| Target SHA | 3f919cc |
| Ran by | warden on claude-opus-5 |
| PR | 259 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

A verifying round, spawned after round 2's corrections were committed and
targeted at the diff of those corrections: `5544df8..ad6f81a`, plus `3f919cc`,
which only closes round 2's record. Its job was stated as round 2's five ⬜
answers rather than new findings, with one surface exempt — what the fix pass
itself created. The cap's last round, and it was told so.

Five checks, in the order the prompt set them.

1. **⑥ the docstring's account of the syntax tree.** It had called the join's
   `"\n  "` an argument; it now says the receiver, and that a bare `ast.walk`
   of the expression does return it so the count of six holds only under the
   flattening rule stated before it. The round was asked to verify against the
   parsed call — what `func.value` and `args` actually are, and what a bare
   walk returns — and to judge whether the count and coverage still stand.
2. **⑦ the third survivor class.** The docstring now records that nothing here
   pins that nothing was ADDED, with the figure 32 passed. The round was asked
   to measure both insertions itself, and to judge whether the claim that
   pinning it means rebuilding `refusal` in the test is true or whether a
   cheaper pin was foreclosed — held to that docstring's own standing rule that
   a limit nobody measured must not be written there again.
3. **⑧ the two correction blocks' declared reach.** Each now says how far it
   reaches and both leave the superseded vocabulary standing below, on the
   ground that every acceptance row is still satisfied. The round was asked to
   verify that premise by mutation rather than by reading.
4. **⑨ `overview.md`'s rationale about a second reader**, against the two cases
   and their docstrings.
5. **⑩ whether `answered` was the right verdict** for round 1's `Fixes checked
   by` cell, or whether something was left unwritten.

Carried as not the round's to close: the two ledger anchors this branch
deliberately left drifted, which the orchestrator re-verifies at the closing
commit — the round was asked to measure the drift and say whether the units are
ones somebody has actually re-read, because a whole-file re-stamp stamps rows
nobody opened. Also `docs/flow.md`'s box, and the broad gate under contract §2.

The round was told that `tests/test_release_hygiene.py` refuses a loaded
document naming the version now running, so any version written into a record
had to be the illustrative one that test's own message points at.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 2's ⬜ 6 — the docstring's account of the join's receiver, and whether six is still the count | `tests/test_release_hygiene.py:337-339` | answered | **Executed**: in the parsed call `func.value` is `Constant('\n  ')` and `args` is `[Name('offenders')]`, so the corrected sentence is true where the one it replaced was false. Bare `ast.walk` returns 22 nodes and the receiver `Constant` is among them once; under the stated normalisation the expression has 6 leaves, and counting the bare walk's value-carrying terminals gives 7 — round 2's figure, and the old wrong count. The count and the coverage both stand |
| 2 | Round 2's ⬜ 7 — the third survivor class and its figure | `tests/test_release_hygiene.py:362-366` | answered | **Executed**: both insertions re-measured independently, `__pycache__` cleared between and the file restored from bytes — a sentence added at the end of the timer paragraph, 32 passed exit 0; a line added between the refused lines and the routes, 32 passed exit 0. The figure is confirmed. The price named beside it was not measured, which is finding 7 |
| 3 | Round 2's ⬜ 8 — the two correction blocks' declared reach, and whether the rows below are really satisfied | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/spec.md:38-40` · `plan.md:49-53` | answered | **Executed**: all three separator mutations caught, one at a time — the `"\n  "` closing element 3 deleted, the join receiver emptied, `"\n\n"` narrowed — 1 failed / 31 passed each. So `spec.md:63` and `:60` are satisfied and the ground holds. **Read**: every phrase both blocks quote is verbatim in the row it names — `plan.md:27` and `:67`, `spec.md:60` and `:63` |
| 4 | Round 2's ⬜ 9 — `overview.md`'s rationale about a second reader | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/overview.md:21` | answered | **Read**: the routes leaf is read by both cases and for different jobs — `assert routes in refusal(...)` reads it as content, `assert f"\n\n{what_to_write_instead()}" in text` reads it with the blank line attaching it. **Executed**: at the branch point `bcf48b8` the element case does not exist and the module's only assertion over `refusal`'s output is `routes in refusal(...)`, so the five counted as new were read by nothing. The third cell of the same row now contradicts the fourth — finding 8 |
| 5 | Round 2's ⬜ 10 — round 1's `Fixes checked by` cell | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/rounds/round-1.md:9` | answered | **Read**: the cell reads `round-2` at the target. `round_record.py`'s `reach_back` sets round N-1's cell when `new` writes round N and touches nothing else, which is the mechanism round 2's grounds named. Nothing was left unwritten; `answered` is the right verdict. The class moved one record over — finding 9 |
| 6 | ⬜ The ⑥ correction was made at the coordinate and not at the class — two ledger rows still call the join's receiver an argument that is never a leaf, one of them in the shared file | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16` · `seal/ledger.md:1356` | deferred #267 | #267 |
| 7 | ⬜ The third-survivor paragraph names a price nobody measured, in the docstring whose standing rule forbids exactly that | `tests/test_release_hygiene.py:366` | deferred #267 | #267 |
| 8 | ⬜ `overview.md`'s row still locates the sixth element in the case above, in the cell beside the one that now says both cases read it | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/overview.md:21` | deferred #267 | #267 |
| 9 | ⬜ `round-2.md`'s `Fixes checked by` reason is stale at the commit that closed the record — round 2's own ⬜ 10, one record over | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/rounds/round-2.md:9` | deferred #267 | #267 |
| 10 | ⬜ The rule the receiver sentence leans on does not state the clause that does the work | `tests/test_release_hygiene.py:323-326` · `:339` | deferred #267 | #267 |
| 11 | ⬜ The third survivor class reached the docstring and not the two ledger rows, and `plan.md`'s superseded *seven assertions* is the built case's assert count | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16` · `seal/ledger.md:1356` · `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/plan.md:67` | deferred #267 | #267 |

## Paste-ready fixes

```
The old count split the third `JoinedStr` part into a paragraph and a closing separator, and promoted the `"\n  "` the join is called ON — the receiver, `func.value`, where `args` holds `offenders` alone — to an element of its own. A bare `ast.walk` does return that string, so it is a leaf of the tree and not of the expression: the flattening rule is what puts it inside the join rather than beside it, which is why the count of six is stated after that rule and not before (review round 3).
```
```
Seven was reached by splitting that third part into a paragraph and the separator closing it, and by promoting the `"\n  "` the join is called ON — the receiver, `func.value`, where `args` holds `offenders` alone — to an element of its own. A bare `ast.walk` does return that string; the flattening rule stated before the count is what puts it inside the join rather than beside it (review round 3).
```
```python
    A third class is unmeasured by design: nothing here pins that nothing was
    ADDED. A sentence inserted at the end of the timer paragraph, or a line
    inserted before the routes, leaves this module at 32 passed (round 2).
    Every element is read whole, so nothing can go missing. The pin is
    available and it is measured, not absent: the six pieces asserted below
    tile the text exactly, so `assert text == ` their concatenation costs one
    assertion and no literal this case does not already carry — 32 passed
    unmutated, and 1 failed on either insertion (round 3). It is declined
    because that concatenation IS `refusal` rebuilt in the test, which
    `plan.md` weighed and rejected. Declined on a measurement, not on a limit.
```
```
five elements newly read in the new case, and the sixth read by both
```
```python
    So the elements are the leaves `ast.parse` gives for the returned
    expression, under three normalisations stated here because the count
    depends on them: the `+` chain flattens, a `JoinedStr` expands to its
    parts, and a `Call` counts as one atom — receiver and arguments inside it.
    The chain flattens to four operands, and the first is one f-string — a
    single `JoinedStr` of three parts. Six leaves:
```
```
**A third class is outside that set by construction**: nothing pins that nothing was ADDED. A sentence inserted at the end of the timer paragraph, or a line inserted before the routes, leaves the module at 32 passed (round 2, re-measured round 3). The pin is one assertion over the concatenation of the pieces the case already reads — measured green unmutated and red on either insertion in round 3 — and it is declined because that concatenation is `refusal` rebuilt in the test, which `plan.md` rejected.
```

## Executed probes

| What was run | Result |
|---|---|
| `./bin/test tests/test_release_hygiene.py -q` at the target in a fresh `git clone --no-local` | 32 passed, exit 0 |
| `ast.parse` of `refusal`'s returned expression — the flattened `+` chain, the `JoinedStr` parts, the join's receiver-versus-argument split, and a bare `ast.walk` | 4 operands; operand 1 is one `JoinedStr` of 3 parts; **6 leaves** under flatten-`+`/expand-`JoinedStr`/`Call`-as-atom; bare `ast.walk` returns 22 nodes, 11 childless, and the receiver `Constant('\n  ')` once; **7** value-carrying terminals (`Constant` + `Name`), which is round 2's figure; `func.value` is `Constant('\n  ')` and `args` is `[Name('offenders')]` |
| Whether the six substrings the case asserts tile the printed text — each located, then concatenated in order and compared | every piece present at a known offset; **`tile == text` True**, all 1186 characters |
| 9 mutations, each on its own, every `__pycache__` under the clone removed between, the file restored from the bytes read before the first write, and the baseline re-run and byte-compared at the end | baseline 32 passed exit 0; **a sentence added at the end of the timer paragraph 32 passed**; **a line added between the refused lines and the routes 32 passed**; the `"\n  "` closing element 3 deleted 1 failed / 31 passed; the join receiver emptied 1 failed / 31 passed; `"\n\n"` narrowed 1 failed / 31 passed; **the tiling pin alone 32 passed**; **the pin plus either insertion 1 failed / 31 passed**; file restored byte-identical and 32 passed exit 0 after |
| `assert` statements counted by AST in the two cases at the target | 7 in the element case for its 6 elements; 6 in the routes case |
| The module at the branch point `bcf48b8`, read for any assertion over `refusal`'s output | the element case does not exist; the only such assertion is `routes in refusal("0.8.3", …)` at line 275 — the five elements counted as new were read by nothing |
| `evidence_check.py --strict --ledger seal/ledger/1788844200-…-v-is-invisible.md .` | 5 ok · 1 drifted · 0 broken · 0 external · **0 old-format**, exit 2 — `#test_the_refusal_prints_every_piece_it_builds`, content changed at 312-425. `--reverify` NOT run |
| `evidence_check.py --strict --ledger seal/ledger.md .` | 898 ok · 1 drifted · 0 broken · 0 external · **0 old-format**, exit 2 — `#test_the_message_has_a_route_for_every_token_the_check_refuses`, content changed at 259-309. `--reverify` NOT run |
| Every phrase the two correction blocks quote, grepped against the rows they name | all verbatim — `plan.md:27` *four pieces joined by three separators*, `plan.md:67` *#203 as seven assertions*, `spec.md:60` *builds its four pieces*, `spec.md:63` *any one of the three separators* |
| `git diff --stat 5544df8 ad6f81a` and the full diff, plus `git diff --stat ad6f81a 3f919cc` | 4 files in the fix range, 28 insertions / 7 deletions, no executable line changed; the closing commit touches `round-2.md` only, 8 insertions / 8 deletions |
| `uvx ruff check` and `uvx ruff format --check` on `tests/test_release_hygiene.py` | exit 0 and exit 0 |
| `git rev-parse HEAD` and `git status --porcelain` in the clone, before and after the mutation run | `3f919cc` both times, working tree clean |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_release_hygiene.py:350-358` | round 1's 1 — fixed |
| round-1 | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16` · `seal/ledger.md:1356` · `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/changelog.md:19` · `tests/test_release_hygiene.py:311` | round 1's 2 — answered |
| round-1 | `tests/test_release_hygiene.py:333-334` | round 1's 3 — answered |
| round-1 | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:18` | round 1's 4 — answered |
| round-1 | `tests/test_release_hygiene.py:339` | round 1's 5 — fixed |
| round-1 | `tests/test_release_hygiene.py#refusal` | round 1's 6 — answered |
| round-1 | `tests/test_release_hygiene.py#VERSION_TOKEN` | round 1's 7 — answered |
| round-1 | `docs/flow.md:101` | round 1's 8 — answered |
| round-1 | `tests/test_release_hygiene.py:544-556` | round 1's 9 — answered |
| round-1 | `docs/issues-and-milestones.md:66-71` · `docs/flow.md:30` | round 1's 10 — answered |
| round-1 | `seal/ledger.md:1136` · `:1355` · `:1356` | round 1's 11 — answered |
| round-2 | `tests/test_release_hygiene.py#test_the_refusal_prints_every_piece_it_builds` | round 2's 1 — answered |
| round-2 | `seal/ledger.md:1356` · `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16` · `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/changelog.md` · `tests/test_release_hygiene.py:311` | round 2's 2 — answered |
| round-2 | `tests/test_release_hygiene.py:363` | round 2's 5 — answered |
| round-2 | `tests/test_release_hygiene.py:337-338` | round 2's 6 — fixed |
| round-2 | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/spec.md:30` · `plan.md:45` | round 2's 8 — fixed |
| round-2 | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/overview.md:21` | round 2's 9 — fixed |
| round-2 | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/rounds/round-1.md:9` | round 2's 10 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Findings 6 through 11, as the run is capped | `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* makes this the record that ends the run, so each becomes a `deferred #N` candidate rather than a fix to commission | the review orchestrator. Finding 6 is the one I would still take in the closing commit if the cap reading is wrong: a false statement about the syntax tree standing in the shared `seal/ledger.md` |
| `round_record.py` writes `Fixes checked by`'s reason once at `new` and `close` never refreshes it, so every record carries `the fixes are not yet written` between its own close and the next round's `new` | nowhere yet — offered for `seal/follow-up.md`. It is the tool behaviour behind finding 9 and behind round 2's own ⬜ 10, which is the same class in two consecutive records | the repository owner. Not this branch's to change — the fix is in the plugin's own script, and this work item is scoped to prose and one regex |
| Whether to plant the case pinning the check's own `assert not offenders, refusal(running, offenders)` | `seal/specs/1788844200-…/questions.md` Q2, with the decision in `overview.md` §Not done | the review orchestrator — already deferred by round 1's fix pass with the answerer named, not re-opened here |
| Whether a case should pin the two documents that name the check agreeing | `questions.md` Q1 and ledger row S4 | the review orchestrator, or the repository owner it asks — already deferred, not re-opened |
| The early-return implementation round 1's arrangements were measured against is reconstructed from a docstring rather than the historical bytes | `seal/specs/1788844200-…/overview.md` §Not verified | the review orchestrator, if the reverted branch's intermediate commits can be fetched. Unchanged this round |
| `CONTRIBUTING.md` §House rules does not name the case of correcting a false note in a `seal/ledger.md` row that has not drifted | nowhere yet — offered for `seal/follow-up.md` by round 1 | the repository owner. Finding 6 is a second instance of the same silence: R3 has not drifted and carries a false sentence |
