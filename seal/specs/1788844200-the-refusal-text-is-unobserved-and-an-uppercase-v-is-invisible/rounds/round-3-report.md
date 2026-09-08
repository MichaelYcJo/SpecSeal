# Review round 3 — the five corrections round 2 offered, and what the fix pass created

A verifying round. Target `3f919cc`; the fix range judged is `5544df8..ad6f81a`,
which is four files — the case docstring in `tests/test_release_hygiene.py` and
correction text in `overview.md`, `plan.md` and `spec.md`. `3f919cc` itself only
closes round 2's record.

All five of round 2's ⬜ corrections are answered, and four of them are answered
as correct. **The fifth is answered as correct at the coordinate round 2 named
and not at the class**: the sentence about the join's receiver was fixed in the
docstring, and the identical wrong sentence still stands in two ledger rows, one
of them the shared `seal/ledger.md`. That is the one thing in this round worth
the closing commit's attention.

Nothing opened here needs a fix in the sense the run's terminal condition asks
about. Every new finding is a correction — five in record locations, one in a
docstring — and none of them changes what the code does or what the module
reports. The run is also at its bound: `docs/review-chain-spec.md`
§*The reopening — one, and then the run is capped* allows one fix-closing
record after a record that met the floor, `round-2.md` is that record, so this
one ends the run whatever it finds and its open items become `deferred #N`
candidates rather than fixes to commission.

## The five answers

### ⑥ The docstring's account of the syntax tree is true, and the count and coverage stand

Derived from the parsed call rather than taken from the report. In
`refusal`'s returned expression the join's `func.value` is `Constant('\n  ')`
and `args` is `[Name('offenders')]`. The string is the receiver; `offenders`
is the only argument. So the docstring's corrected sentence at
`tests/test_release_hygiene.py:337-339` — *the `"\n  "` the join is called ON
— the receiver, not an argument* — is right, and the sentence it replaced was
wrong.

The second half is right too. A bare `ast.walk` of the expression returns 22
nodes, and the `Constant('\n  ')` receiver is among them exactly once. Under
the normalisation the docstring states before the count — flatten the `+`
chain, expand the `JoinedStr`, treat a `Call` as one atom — the expression has
**6** leaves, matching the six the docstring enumerates. Counting only the
value-carrying terminals of the bare walk (`Constant` and `Name`) gives 7,
which is round 2's figure and reproduces the old wrong count. So the docstring
is correct that the count of six holds only under the stated rule, and correct
that the bare walk does return the receiver.

Coverage stands as well: the six leaves are all read whole, and the three
separator mutations each turn the case red (see ⑧).

One residue, carried as finding 10 below: the rule the sentence leans on is
stated in two clauses, and the clause that actually excludes the receiver —
a `Call` counting as one atom — is only demonstrated by the enumerated list
rather than stated. A reader applying the two stated clauses literally gets
seven, which is the count the paragraph exists to correct.

### ⑦ The figure is right; the price beside it was not measured

Both insertions round 2 named, measured here one at a time, `__pycache__`
cleared between each and the file restored from bytes read before the first
write:

- a sentence added at the end of the timer paragraph — **32 passed, exit 0**
- a line added between the refused lines and the routes — **32 passed, exit 0**

So the docstring's *leaves this module at 32 passed (round 2)* is confirmed by
independent measurement.

The claim beside it — *pinning that nothing was added means rebuilding
`refusal` in the test* — is literally true and its cost is not what it reads.
The six pieces the case already asserts **tile the printed text exactly**:
concatenated in order they reproduce all 1186 characters (`tile == text`,
True). So the pin is one assertion built from literals the case already
carries, adding none. Measured: with that assertion added and nothing else
changed the module is 32 passed exit 0; with it added and either insertion
applied it is 1 failed / 31 passed.

That makes the sentence a price named without being measured, in the docstring
whose own standing rule two paragraphs down is that a limit nobody measured
must not be written there again. It is the first of the four instances in this
function's history that is *true* — the pin genuinely is a reconstruction, and
`plan.md` rejected reconstruction — so declining it is defensible. What is
missing is the measurement that makes it a decision rather than a limit. The
correction is one clause, and it is finding 7 with a paste-ready fix.

### ⑧ The premise holds — all three separators are caught, so the rows below are satisfied

Each of the three separators mutated on its own:

| The separator | Mutation | Result |
|---|---|---|
| the `"\n  "` closing element 3 | deleted | 1 failed / 31 passed |
| the join's receiver `"\n  "` | emptied | 1 failed / 31 passed |
| `"\n\n"` | narrowed to `"\n"` | 1 failed / 31 passed |

`spec.md:63`'s acceptance row — *any one of the three separators is deleted /
Then a case goes red, one per separator* — is therefore satisfied, and so is
`:60`'s row on the offender join (carried from round 1 and round 2, both of
which reddened it). The ground the two correction blocks rest on is sound: the
vocabulary below them is superseded and the criteria are still met, so leaving
accepted rows in the words they were accepted in is the right call.

Both blocks' quotations check out against the text they reach. `plan.md:51-53`
quotes *four pieces joined by three separators*, which is `plan.md:27` verbatim,
and *#203 as seven assertions*, which is `plan.md:67` verbatim. `spec.md:39`
quotes *builds its four pieces* and *any one of the three separators*, which are
`spec.md:60` and `:63` verbatim.

One coincidence the blocks do not remark on, carried as finding 11: the built
case has exactly **seven** `assert` statements for its six elements, because the
timer paragraph is read by two contiguous halves. So `plan.md:67`'s *seven
assertions*, which the block above calls the superseded reading, happens to
describe the case that was built. A number that is right for the wrong reason is
how *seven* looked derived the first three times.

### ⑨ The rationale is true against both cases

Verified against the two cases and their docstrings rather than against the
cell. `test_the_message_has_a_route_for_every_token_the_check_refuses` ends on
`assert routes in refusal(...)`, which reads the routes as content of the
printed text. `test_the_refusal_prints_every_piece_it_builds` ends on
`assert f"\n\n{what_to_write_instead()}" in text`, which reads the routes
together with the blank line that attaches them to the block above. Two
different jobs on the same leaf, which is what the new cell claims.

*The five counted as new are the five nothing read before* is true too, and
measured against the branch point rather than read. At `bcf48b8` the element
case does not exist, and the only assertion anywhere in the module that reads
`refusal`'s output is `assert routes in refusal("0.8.3", …)` at line 275. No
assertion there read the opening constant, the interpolated version, the timer
paragraph, the joined refused lines or the blank line. Five, and nothing read
them.

The same table row's third cell was left as it stood, and it now contradicts
the cell beside it — finding 8.

### ⑩ `answered` is right, and nothing was left unwritten

`round-1.md:9` at the target reads `| Fixes checked by | round-2 |`. The
reach-back that `round_record.py new` performs when it writes round 2 set it,
which is exactly the mechanism round 2's grounds named. `reach_back`'s
docstring confirms the write is the only thing it touches. So the stale reason
is gone, the cell holds a true fact about which round read those fixes, and
there is nothing a fix could have added. `answered` is the right verdict.

The class, however, moved rather than closed — finding 9.

## What the fix pass created

### The ⑥ correction stopped at the coordinate round 2 named

Round 2's ⬜ 6 was that the docstring called the join's receiver *an argument*
and *never a leaf*. The docstring was corrected. The same two sentences stand
uncorrected in two ledger rows:

- `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16`, the S2 row's Notes column: *promoted the join's `"\n  "` argument — an argument to an operand, never a leaf — to an element of its own*
- `seal/ledger.md:1356`, R3's Notes column: *promoting the join's `"\n  "` argument — an argument to an operand, never a leaf — to an element of its own*

Both statements are false by the same measurement that vindicated the docstring:
the string is the receiver, `offenders` is the only argument, and a bare
`ast.walk` returns the string. The second of the two sits in the shared file,
which is where a reader outside this work item will meet the claim first —
and the fragment's own header paragraph states the reason this branch edits
that file at all, *because a claim corrected only in a fragment leaves the
false one standing where a reader will find it first*. Here the direction is
reversed and the sentence applies unchanged.

This is a correction rather than something needing a fix, because both
locations are ledger rows. It is still the round's main result: the class was
not enumerated, and the durable record carries the sentence the code no longer
does.

### The third survivor class reached the docstring and not the ledger

The docstring now records the insertion class. Ledger fragment S2 and
`seal/ledger.md` R3 both still say *the two survivors are measured, and neither
is a limit*, scoped to *thirteen mutations*. Nothing there is false — the
survivor list is stated relative to the set that was run, which is the
discipline this row was corrected into three times. What is absent is the third
class, which the docstring now names and the ledger does not, and this row's
history is exactly that of a survivor list read as complete. Finding 11.

### Nothing else in the range

The four files in `5544df8..ad6f81a` are the docstring and three correction
texts. No executable line changed: the module's assertions, `refusal`,
`VERSION_TOKEN` and the `[vV]?` widening are untouched in the range. `ruff
check` and `ruff format --check` on the one changed `.py` file are exit 0 and
exit 0. The module is 32 passed exit 0 at the target, in a fresh
`git clone --no-local`, and 32 passed exit 0 again after every mutation was
reverted, with the file byte-identical to the bytes read before the first
write.

`3f919cc` changed `round-2.md` only: `Contract changes` and `New units` lost
their `— the fixes are not yet written` suffixes, `Pass` was ticked, and the
five ⬜ verdicts moved from `open` to `**fixed** ad6f81a` (⑩ to `answered`).
`Fixes checked by` was not refreshed, which is finding 9.

## Carried, not closed

- **The two drifted ledger anchors.** Measured, `--reverify` **not** run.
  Scoped on the fragment: 5 ok · 1 drifted · 0 broken · 0 old-format, exit 2 —
  `tests/test_release_hygiene.py#test_the_refusal_prints_every_piece_it_builds`,
  content changed at 312-425. Scoped on `seal/ledger.md`: 898 ok · 1 drifted ·
  0 broken · 0 old-format, exit 2 —
  `tests/test_release_hygiene.py#test_the_message_has_a_route_for_every_token_the_check_refuses`,
  content changed at 259-309. **Both units have been re-read whole in this
  round**: the first is the case whose docstring and assertions I enumerated
  leaf by leaf and mutated nine times, the second I read in full at 259-309 to
  settle ⑨ and its routes assertion. A re-stamp of those two rows is a re-stamp
  of units somebody opened. Every other row in both files is `ok`, so no
  whole-file re-stamp is needed and none should be taken — 898 of the 899 rows
  in the shared file were not re-read by anybody this round.
- **`docs/flow.md`'s box for this branch** — the orchestrator's.
- **The broad gate.** Not run, and named so it is not read as passing: the full
  suite, unscoped `evidence-check`, repository-wide `ruff check` and
  `ruff format --check`, the typecheck, `unverified_check.py` and
  `chain_check.py`. Contract §2 holds them for the orchestrator, once, after the
  rounds settle. Nothing opened here needs a fix, so the broad run is the next
  step. What I did run is scoped: the one module, `evidence-check` with
  `--ledger` twice, and `ruff` on the one changed file.
- **`chain_check.py` was not run** either, which matters for one reason worth
  saying: round 2's own probe table records it at exit 1 against the state that
  round resolved, and the reopening bound above is a rule I read rather than a
  check I executed. The orchestrator's run at the broad gate is what confirms
  the cap reading.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 2's ⬜ 6 — the docstring's account of the join's receiver, and whether six is still the count | `tests/test_release_hygiene.py:337-339` | answered | **Executed**: in the parsed call `func.value` is `Constant('\n  ')` and `args` is `[Name('offenders')]`, so the corrected sentence is true where the one it replaced was false. Bare `ast.walk` returns 22 nodes and the receiver `Constant` is among them once; under the stated normalisation the expression has 6 leaves, and counting the bare walk's value-carrying terminals gives 7 — round 2's figure, and the old wrong count. The count and the coverage both stand |
| 2 | Round 2's ⬜ 7 — the third survivor class and its figure | `tests/test_release_hygiene.py:362-366` | answered | **Executed**: both insertions re-measured independently, `__pycache__` cleared between and the file restored from bytes — a sentence added at the end of the timer paragraph, 32 passed exit 0; a line added between the refused lines and the routes, 32 passed exit 0. The figure is confirmed. The price named beside it was not measured, which is finding 7 |
| 3 | Round 2's ⬜ 8 — the two correction blocks' declared reach, and whether the rows below are really satisfied | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/spec.md:38-40` · `plan.md:49-53` | answered | **Executed**: all three separator mutations caught, one at a time — the `"\n  "` closing element 3 deleted, the join receiver emptied, `"\n\n"` narrowed — 1 failed / 31 passed each. So `spec.md:63` and `:60` are satisfied and the ground holds. **Read**: every phrase both blocks quote is verbatim in the row it names — `plan.md:27` and `:67`, `spec.md:60` and `:63` |
| 4 | Round 2's ⬜ 9 — `overview.md`'s rationale about a second reader | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/overview.md:21` | answered | **Read**: the routes leaf is read by both cases and for different jobs — `assert routes in refusal(...)` reads it as content, `assert f"\n\n{what_to_write_instead()}" in text` reads it with the blank line attaching it. **Executed**: at the branch point `bcf48b8` the element case does not exist and the module's only assertion over `refusal`'s output is `routes in refusal(...)`, so the five counted as new were read by nothing. The third cell of the same row now contradicts the fourth — finding 8 |
| 5 | Round 2's ⬜ 10 — round 1's `Fixes checked by` cell | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/rounds/round-1.md:9` | answered | **Read**: the cell reads `round-2` at the target. `round_record.py`'s `reach_back` sets round N-1's cell when `new` writes round N and touches nothing else, which is the mechanism round 2's grounds named. Nothing was left unwritten; `answered` is the right verdict. The class moved one record over — finding 9 |
| 6 | ⬜ The ⑥ correction was made at the coordinate and not at the class — two ledger rows still call the join's receiver an argument that is never a leaf, one of them in the shared file | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16` · `seal/ledger.md:1356` | open | **Executed**: the same AST measurement that vindicated the docstring falsifies both rows — the string is the receiver, `offenders` is the only argument, and a bare `ast.walk` returns the string. **Read**: the fragment's own header states that a claim corrected only in a fragment leaves the false one standing where a reader finds it first; the direction here is reversed and the sentence applies unchanged. A correction, not a fix — both locations are ledger rows. Round 2's ⬜ 6 named one location, and its own proof block records both these rows as opened, so the wording was in front of that round; its grep looked for the count words rather than for *argument*, which is how it passed |
| 7 | ⬜ The third-survivor paragraph names a price nobody measured, in the docstring whose standing rule forbids exactly that | `tests/test_release_hygiene.py:366` | open | **Executed**: the six pieces the case already asserts tile the printed text exactly — concatenated in order they reproduce all 1186 characters, `tile == text` True. With that one assertion added and nothing else changed, 32 passed exit 0; with it added and either insertion applied, 1 failed / 31 passed. So the pin adds no literal the case does not already carry. The sentence is true — the pin is a reconstruction, which `plan.md` rejected — and the measurement that makes it a decision rather than a limit is absent. Fourth instance of the class in this function's history, and the first that is true. Round 2 stated the price as a read — *pinning the whole text is rebuilding `refusal` inside the test* — with no probe behind it |
| 8 | ⬜ `overview.md`'s row still locates the sixth element in the case above, in the cell beside the one that now says both cases read it | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/overview.md:21` | open | **Read**: the `Chosen` cell reads *five elements in the new case, the sixth in the case above it* while the `Grounds` cell beside it now reads *the routes piece is read by both cases, and deliberately*. The new case does assert the routes, so the sixth is in both and the third cell is the superseded statement round 2's ⬜ 9 named. Only the fourth cell was rewritten |
| 9 | ⬜ `round-2.md`'s `Fixes checked by` reason is stale at the commit that closed the record — round 2's own ⬜ 10, one record over | `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/rounds/round-2.md:9` | open | **Read**: the cell reads `nobody — the fixes are not yet written` while four verdicts in the same file read `**fixed** ad6f81a`. `3f919cc` refreshed `Contract changes` and `New units` and left this one. By `round_record.py`'s own design `close` leaves the cell for the next `new` to set, so the value is what the ordering rule requires and only the reason is false — and `new` of this round overwrites it with `round-3`. Self-resolving at this record; the tool behaviour that writes a reason once and never refreshes it is the durable item, deferred below |
| 10 | ⬜ The rule the receiver sentence leans on does not state the clause that does the work | `tests/test_release_hygiene.py:323-326` · `:339` | open | **Read**: *Under the rule above* points at a paragraph stating two normalisations — flatten the `+` chain, expand the `JoinedStr`. The clause that puts the receiver inside element 4 is that a `Call` counts as one atom, which the enumerated list demonstrates (items 4 and 6 are calls) and no sentence states. **Executed**: applying only the two stated clauses yields seven leaves, which is the count the paragraph exists to correct |
| 11 | ⬜ The third survivor class reached the docstring and not the two ledger rows, and `plan.md`'s superseded *seven assertions* is the built case's assert count | `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16` · `seal/ledger.md:1356` · `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/plan.md:67` | open | **Read**: both ledger rows still say *the two survivors are measured, and neither is a limit*, scoped to thirteen mutations. Nothing false — the list is stated relative to the set run — but the class the docstring now names is absent from the durable record, and this row's history is a survivor list read as complete. **Executed**: the built case has 7 `assert` statements for its 6 elements, so `plan.md:67`'s *seven assertions*, which the block above calls superseded, describes what was built |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Findings 6 through 11, as the run is capped | `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* makes this the record that ends the run, so each becomes a `deferred #N` candidate rather than a fix to commission | the review orchestrator. Finding 6 is the one I would still take in the closing commit if the cap reading is wrong: a false statement about the syntax tree standing in the shared `seal/ledger.md` |
| `round_record.py` writes `Fixes checked by`'s reason once at `new` and `close` never refreshes it, so every record carries `the fixes are not yet written` between its own close and the next round's `new` | nowhere yet — offered for `seal/follow-up.md`. It is the tool behaviour behind finding 9 and behind round 2's own ⬜ 10, which is the same class in two consecutive records | the repository owner. Not this branch's to change — the fix is in the plugin's own script, and this work item is scoped to prose and one regex |
| Whether to plant the case pinning the check's own `assert not offenders, refusal(running, offenders)` | `seal/specs/1788844200-…/questions.md` Q2, with the decision in `overview.md` §Not done | the review orchestrator — already deferred by round 1's fix pass with the answerer named, not re-opened here |
| Whether a case should pin the two documents that name the check agreeing | `questions.md` Q1 and ledger row S4 | the review orchestrator, or the repository owner it asks — already deferred, not re-opened |
| The early-return implementation round 1's arrangements were measured against is reconstructed from a docstring rather than the historical bytes | `seal/specs/1788844200-…/overview.md` §Not verified | the review orchestrator, if the reverted branch's intermediate commits can be fetched. Unchanged this round |
| `CONTRIBUTING.md` §House rules does not name the case of correcting a false note in a `seal/ledger.md` row that has not drifted | nowhere yet — offered for `seal/follow-up.md` by round 1 | the repository owner. Finding 6 is a second instance of the same silence: R3 has not drifted and carries a false sentence |

## Paste-ready fixes

Finding 6, `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md:16` — the S2 Notes clause:

```
The old count split the third `JoinedStr` part into a paragraph and a closing separator, and promoted the `"\n  "` the join is called ON — the receiver, `func.value`, where `args` holds `offenders` alone — to an element of its own. A bare `ast.walk` does return that string, so it is a leaf of the tree and not of the expression: the flattening rule is what puts it inside the join rather than beside it, which is why the count of six is stated after that rule and not before (review round 3).
```

Finding 6, `seal/ledger.md:1356` — the corresponding clause of R3:

```
Seven was reached by splitting that third part into a paragraph and the separator closing it, and by promoting the `"\n  "` the join is called ON — the receiver, `func.value`, where `args` holds `offenders` alone — to an element of its own. A bare `ast.walk` does return that string; the flattening rule stated before the count is what puts it inside the join rather than beside it (review round 3).
```

Finding 7, `tests/test_release_hygiene.py:362-366` — the third-survivor paragraph:

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

Finding 8, `seal/specs/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible/overview.md:21` — the third cell:

```
five elements newly read in the new case, and the sixth read by both
```

Finding 10, `tests/test_release_hygiene.py:323-326` — the rule paragraph, so it carries the clause the later sentence leans on:

```python
    So the elements are the leaves `ast.parse` gives for the returned
    expression, under three normalisations stated here because the count
    depends on them: the `+` chain flattens, a `JoinedStr` expands to its
    parts, and a `Call` counts as one atom — receiver and arguments inside it.
    The chain flattens to four operands, and the first is one f-string — a
    single `JoinedStr` of three parts. Six leaves:
```

Finding 11, the third-survivor class for both ledger rows — appended to the survivor sentence in each:

```
**A third class is outside that set by construction**: nothing pins that nothing was ADDED. A sentence inserted at the end of the timer paragraph, or a line inserted before the routes, leaves the module at 32 passed (round 2, re-measured round 3). The pin is one assertion over the concatenation of the pieces the case already reads — measured green unmutated and red on either insertion in round 3 — and it is declined because that concatenation is `refusal` rebuilt in the test, which `plan.md` rejected.
```

## Proof

Read in the clone at `3f919cc`, and nothing was written in the primary tree:

- `tests/test_release_hygiene.py` — `refusal`, `what_to_write_instead`,
  `VERSION_TOKEN`, `ILLUSTRATIVE_VERSION`, `RECORDS_OF_A_MOMENT`,
  `RUNNING_IN_THE_FIXTURES`, and both cases whole
- `tests/test_release_hygiene.py` at `bcf48b8`, the branch point
- `seal/specs/1788844200-…/rounds/round-1.md` · `round-2.md`
- `seal/specs/1788844200-…/overview.md` · `plan.md` · `spec.md`
- `seal/ledger/1788844200-the-refusal-text-is-unobserved-and-an-uppercase-v-is-invisible.md`
- `seal/ledger.md`, the rows naming this module's units
- `seal/specs/1788844200-…/rounds/round-1-report.md` · `round-2-report.md`
- `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped*
  and the two paragraphs on the cap and the floor
- `skills/code-review/scripts/round_record.py` — the `new`/`close` field
  derivations and `reach_back`
- `bin/test`

Two things the reports settle that the records alone did not. Round 2's ⬜ 6
names one location, `tests/test_release_hygiene.py:337-338`, and its own proof
block records reading `seal/ledger.md` rows R1 and R3 in full and the fragment
whole — so the two rows in finding 6 were open in that round and the wording was
not flagged there. Its grep for surviving claims looked for the count words
(*seven*, *four pieces*, *three separators*), which is why the *argument*
sentence passed it. And round 2's own prose states the price in finding 7 as a
read — *pinning the whole text is rebuilding `refusal` inside the test* — with no
probe behind it, which is what made it worth measuring here.

Every fact above was re-derived in this round except the two named as carried in
⑧ (round 1's and round 2's offender-join mutations) and the reopening bound,
which is read from `docs/review-chain-spec.md` rather than executed.

Needs a fix: no
Loses a record or crashes: no
