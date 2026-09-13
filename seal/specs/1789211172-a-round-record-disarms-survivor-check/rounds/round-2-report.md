# Round 2 report — a round record disarms survivor-check

| Field | Value |
|---|---|
| Work item | `1789211172-a-round-record-disarms-survivor-check` |
| Issue · PR | #365 · #372 (draft) |
| Branch | `fix/365-a-round-record-disarms-survivor-check` |
| Target SHA | `fb64d06` |
| Base | `release/v0.11.2` at `bc5248c` |
| Round | 2 — the verifying round; diff under review `b9caadb..fb64d06` |

HEAD was still `fb64d06` and the working tree clean when this report was
finished.

Reviewed in a `git clone --no-local` of the repository checked out at the
target SHA, inside this session's scratchpad. Every mutation was applied in
the clone and the file restored; the clone reported a clean tree at `fb64d06`
before it was deleted. Nothing was written in the working checkout except this
file.

## The verdict in one paragraph

**Nothing needs a fix.** All seven of round 1's findings are closed on my own
grounds, the six-mutation claim holds and is stronger than it was recorded —
I took ten red shapes, six of which neither side had tried — and the smith's
two judgment calls, refusing my paste-ready fix and writing no `survivors.md`,
are both correct. I measured the refusal rather than reading it, and the
survivor call is right for a reason its own record does not state. The one
thing I opened is a limitation of the new unit that a person meets only after
a deliberate edit, with the failure message warning them at that moment: it is
⬜ and it does not hold the gate.

## Findings

### ⬜ 8 · after the classify act, a second **unfiltered** site in a declared scope passes

`tests/test_a_corrected_sentence_survives_elsewhere.py:723` (the count
assertion) with `:671` (`_mentions`).

The case now has two classify acts and they demand different things. A path
list in a scope nothing has declared forces the person into one of the three
buckets, and each bucket then asserts something — `_mentions` for the filtered
ones, the grounds for the named exception. A **second** path list in a scope
that is already declared forces only an integer: bump `PATH_LIST_CALLS`.

That second act asserts nothing about the new site, because `_mentions` asks
whether the predicate appears anywhere in the function and either call
satisfies it.

**Executed**, three mutations of `corrected` with the module and the case both
restored byte-identical:

| Mutation | Case |
|---|---|
| a second **unfiltered** path list, count left at 1 | **red** — `{'corrected': 2}` against `{'corrected': 1}` |
| the same second **unfiltered** path list, count bumped to 2 | **green** |
| a second **filtered** path list, count bumped to 2 | **green** |

The middle row is the gap: the module now derives two path lists inside
`corrected` and only one of them applies the predicate, and the case is green.

**Why this is ⬜ and not 🟡.** The release ships nothing defective — the case
as it stands is strictly tighter than the one round 1 reviewed, and reaching
the gap takes a deliberate edit to the declaration. The message the person
meets at that edit already says it: *the grounds recorded above are about the
call this case counted rather than about the one just added*. That is
disclosure at the moment of the act, which is the difference between a
documented limit and a silent hole. It is worth a row so the next reader does
not re-find it.

## What I checked and found sound

### Finding 1's fix — ten red shapes, four of them the ones left for me

The claim was six mutations, six red. I took four of the six directly, and six
shapes neither the smith nor the orchestrating session had tried. All ten are
red, each with the module restored byte-identical and the restoration checked
by hash:

| Shape | Case | Whose |
|---|---|---|
| the filter removed from `corrected` | red | the smith's, re-taken here |
| a fourth unfiltered path-list function | red | the smith's, re-taken here |
| two path lists in **one outer call's arguments** | red — `{'corrected': 2}` | the smith's, re-taken here |
| a second unfiltered caller of `tracked` | red — names both callers | the smith's, re-taken here |
| an **async** path-list function | red | new — and it is finding 5's fix paying off |
| a path list in a **nested function** inside `corrected` | red — the inner scope is named | new |
| a path list in a **method of a class** | red | new |
| a direct `subprocess.run` path list at module scope | red — reports `<module>` | new |
| a module-scope path list **inside an `if` block** | red | new |
| a module-scope path list **inside a comprehension** | red | new |

The last three matter because `MODULE_SCOPE` could easily have been written to
catch only a top-level assignment. It is not: the walk descends through
statement bodies and comprehensions alike, so a list built at import time is
found wherever it is built.

The async row is the one place two of round 1's findings meet. Before finding
5's fix, an async path-list function was found by `_derives_a_path_list` and
then raised *is no longer a function in this module* from `_function` — red in
the safe direction with a message blaming a deletion. It now reports the real
message.

### Brittleness — two false-red candidates, and only one of them is new

`plan.md` names *an ordinary refactor turns it red for no defect* as this
case's own failure scenario, so I ran four refactors that add no defect:

| Refactor | Case |
|---|---|
| rename a local variable in `corrected` | green |
| the same call reflowed across lines | green |
| git arguments hoisted into a tuple, then splatted | **red** |
| a second but already-**filtered** path list in `corrected` | **red** |

The third is a genuine false red and it is **inherited, not introduced.** I ran
it against the pre-fix case at `b9caadb` as well and it is red there too: both
shapes read the path-listing words out of the call's own constants, so hoisting
the arguments into a tuple takes the site out of the walk's sight and
`corrected` vanishes from the list entirely. This diff did not make it worse
and did not make it better. It is recorded here so the next round does not
spend a probe re-finding it.

The fourth is the one behavior change in the false-red direction — green
before the fix, red after — and I judge it a correct tightening rather than a
false red. `_mentions` cannot tell which of two sites carries the filter, so a
second site genuinely cannot be verified as filtered by this case, and
demanding classification is the right direction. It is also the doorway to
finding 8 above.

### The smith declined my paste-ready fix, and the refusal is correct

This is a claim about round 1's own proposed remedy, so I measured both shapes
against the same mutated tree rather than reading the argument.

On a mutation putting two path lists in one outer call's arguments inside
`corrected`:

| Shape | Result |
|---|---|
| round 1's paste-ready fix, which reads the whole call subtree | `{'corrected': 1}` — **passes** |
| the shipped `_path_list_words`, which stops at a nested call | `{'corrected': 2}` — **fails** |

Both agree on the unmutated module, so the correction costs nothing and buys
the nested case. The smith's account of why is accurate: reading the constants
of a whole subtree sees the outer call once and collapses the two sites, which
is round 1's finding one level down. **The paste-ready fix I relayed was
wrong and the smith was right to correct rather than paste it.**

### The five ⬜ corrections

All applied on their merits, all read.

- **Finding 3.** The memo's executed line now names the one repository-wide
  `ruff check`, that §2 reserves it and §3 asks it be named, and that the run
  is spent rather than banked.
- **Finding 4.** `phases/phase-5.md`'s removal table gains the second row,
  with the grounds and with the limit stated — the eleven-to-one measurement
  is of the added side alone, so the wider half's evidence lives on #371.
- **Finding 5.** Both helpers now match async, and the async mutation above is
  it paying off.
- **Finding 6, which I was asked to judge.** Keeping the conjunct as a second
  assertion is right. `grounds` comes from `NAMED_EXCEPTION` in the test file
  and `body` comes from the module, so the two fail for opposite reasons and
  one message could only ever blame one party. The first is not dead weight:
  it fires when somebody rewords the recorded grounds away from `foreign`,
  and without it the case would go on checking the module against an argument
  that had been rewritten above it. The messages say which party each blames.
- **Finding 7.** I read the docstring paragraph the case pins. It says the
  exclusion holds *out of the **pool** that is searched and out of the
  **range** that is measured -- both sides of the range's path list, not its
  added side alone*. So the paragraph's *both sides* is the two sides of the
  path list, and the corrected message names that pair. Right pair, fixed.

### The two things the fix pass found on its own

Both check out, and both carried a claim I opened rather than took.

**The follow-up clause.** The row now says #371 is the RANGE half and #308 the
CORPUS half, that landing either alone leaves the row silenced by the other
path, and that this pass had no scope to touch either ticket. The reasoning is
sound on the mechanism as the module stands.

**The restored `## Not verified` row.** `skills/implement/SKILL.md` §4 says in
as many words that *an item is closed by marking it, never by deleting it*, so
the grounds are right. The restoration's claim is that `dc1e93a` wrote
`specseal:smith on claude-opus-5` into all four phase records; I opened all
four and all four carry it. The row is a ✅ naming what closed it, and
`unverified-check` reads the memo as 5 open · 1 closed, where round 1 saw
5 open · 0 closed.

The blind-spot claim is the one I would not take on prose, because it is a
claim about what a gate cannot see. It holds: the memo does not exist at
`bc5248c`, so there is no earlier row count to compare against, and
`unverified-check --baseline bc5248c` exits 0 with the row deleted or restored
alike.

### The ledger

S2 was widened from *every function* to *every place … counted by call site,
module scope included*, and that is what the code now does — the `<module>`
rows in the mutation table above are the measurement. The widening was
re-verified rather than re-pointed, and that is the correct act: the anchor
names `test_every_path_list_this_module_derives_from_git_is_filtered_or_named`,
which still exists, so `CLAUDE.md`'s *a row whose anchor a change removes is
REMOVED* does not apply. Nothing was re-pointed that should have been removed.

S2's quoted red message still matches what the module produces — I reproduced
it verbatim on the fourth-function mutation. S3's second anchor was re-verified
for finding 7's message edit. `bin/evidence-check .` exits 0 at `fb64d06`:
1149 ok, 0 drifted, 0 broken, `0 refused` — the same totals round 1 read at
`dc1e93a`, with the two hashes moved.

### The survivor step — checked myself, and the call is right

I ran both ranges rather than reading the smith's account of them, and both
numbers reproduce exactly.

| Range | Result |
|---|---|
| `bc5248c...fb64d06` — what the gate runs | **exit 0** · 902 files · 6 removed sentences · no removed wording still standing |
| `b9caadb..fb64d06` — the fix pass's own | **exit 1** · 902 files · 14 removed sentences · **5 places** |

All five name the same corrected coordinate: the old `_derives_a_path_list`
body. The shared wording is generic Python `ast` idiom — *walk node if not
isinstance*, *ast constant and isinstance*, *setdefault node name* — standing
in `test_the_record_is_generated.py`, `test_a_row_points_by_content.py` twice,
`round_record.py`, and in this module's own `_callers_of`.

**The deeper reason the gate is silent, which the record does not state.** The
old body did not exist at `bc5248c`. This branch wrote it and then rewrote it,
so over the range the gate measures it was never removed wording at all — that
is why a range of 6 removed sentences finds nothing while a sub-range of 14
finds five. The five places are an artifact of a sub-range whose start point is
a commit on this branch, not a survivor of anything the release base held.

**So writing no `survivors.md` is correct, and writing one would have been a
defect.** I read `hygiene.yml` to check the second half of the argument and it
holds: the step globs `seal/specs/*/survivors.md` and passes **every** match as
`--exempt` on **every** release-branch run, and there are already thirteen such
files in the tree. Five rows quoting generic `ast` idiom would be handed to
every future branch's run, permanently silencing that idiom for ranges that
have nothing to do with this work item. The escape is anchored on a quote so it
degrades when the quoted text changes; idiom this generic would not change, so
these rows would not degrade. That is a worse outcome than the green gate the
branch already has.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 The enumeration case measures function names, so a second unfiltered path list inside an already-declared function, or one at module scope, passes it | `tests/test_a_corrected_sentence_survives_elsewhere.py:615`, `:676` | answered | Closed at `b002b3f` on my own grounds. Executed ten red shapes, four of the smith's six re-taken here and six neither side tried — async, a nested function, a class method, and module scope reached three ways (a direct `subprocess.run`, inside an `if`, inside a comprehension). Module restored byte-identical after each, checked by hash |
| 2 | 🟡 The pull request body attributes four red mutations to the enumeration case; `phases/phase-3.md:57` records two | PR #372 body | answered | Round 1 closed it in the body, not in the tree, and no commit ever carried the claim. Nothing in this diff re-introduces it |
| 3 | ⬜ The memo's executed line omits the one repository-wide `ruff` run the smith disclosed | `seal/specs/1789211172-…/overview.md:10` | answered | Read. The line now names the run, the two contract sections, and that it is spent rather than banked |
| 4 | ⬜ Phase 5's removal table names one changed clause; the follow-up edit changed two | `phases/phase-5.md` removal table | answered | Read. The second row is present with the grounds and with the limit — the eleven-to-one figure is of the added side alone |
| 5 | ⬜ `_mentions` and `_function` accept only `FunctionDef` | `tests/test_a_corrected_sentence_survives_elsewhere.py:671`, `:773` | answered | Executed: an async path-list function is now red with the enumeration message rather than with *is no longer a function in this module* |
| 6 | ⬜ `"foreign" in grounds` is a tautology, and its failure message blames the module | `tests/test_a_corrected_sentence_survives_elsewhere.py:760` | answered | Read, and the smith's judgment is right. The conjuncts fail for opposite reasons — `grounds` is a constant in the case, `body` comes from the module — so two messages blame the correct party each. The first fires when the recorded grounds are reworded away from `foreign` |
| 7 | ⬜ The docstring case's message names the wrong pair | `tests/test_a_corrected_sentence_survives_elsewhere.py:574` | answered | Read the pinned paragraph: its *both sides* is the two sides of the range's path list. The corrected message names that pair |
| 8 | ⬜ After the classify act, a second **unfiltered** site in a declared scope passes — `_mentions` cannot tell which of two calls carries the filter | `tests/test_a_corrected_sentence_survives_elsewhere.py:723`, `:671` | open | Executed: a second unfiltered path list in `corrected` is red at count 1 and **green** once the count is bumped to 2. ⬜ rather than 🟡 — it takes a deliberate edit to reach and the assertion message discloses it at that moment |
| — | The smith's refusal of round 1's paste-ready fix | `tests/test_a_corrected_sentence_survives_elsewhere.py:628` (`_path_list_words`) | answered | Executed both shapes on the same mutated tree: the subtree-reading shape counts `corrected: 1` and passes, the shipped shape counts 2 and fails; they agree on the unmutated module. The refusal is correct |
| — | No `survivors.md` written | `.github/workflows/hygiene.yml`, the two ranges | answered | Executed both ranges: the gate's range exits 0 with nothing standing, the fix range's five places all trace to a body that did not exist at `bc5248c`. Reading `hygiene.yml`, every `seal/specs/*/survivors.md` is handed to every run, so five rows of generic `ast` idiom would silence it for every future branch |
| — | The ledger's S2 widening and S3 re-verify | `seal/ledger/1789211172-a-round-record-disarms-survivor-check.md` | answered | The widened claim is what the code does, measured. Re-verified rather than re-pointed is correct: the anchor names a unit that still exists. `evidence-check` exit 0, 1149 ok, 0 drifted, 0 broken |
| — | The restored `## Not verified` row | `seal/specs/1789211172-…/overview.md` | answered | All four phase records carry `specseal:smith` on `claude-opus-5`, so the row's claim is true. The blind-spot claim holds: the memo is absent at `bc5248c` and `unverified-check --baseline bc5248c` exits 0 either way |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` at `fb64d06` | 47 passed, exit 0 |
| Mutation: the filter removed from `corrected` | red — `corrected derives a path list and no longer applies records_a_past_round` |
| Mutation: a fourth unfiltered path-list function | red — names the four scopes against the three declared |
| Mutation: two path lists in **one outer call's arguments** inside `corrected` | red — `{'corrected': 2}` against `{'corrected': 1}` |
| Mutation: a second unfiltered caller of `tracked` | red — `tracked is reached from ['audit', 'corpus']` |
| Mutation: an **async** path-list function | red — the enumeration message, not the *no longer a function* one |
| Mutation: a path list in a **nested function** inside `corrected` | red — the inner scope is named separately |
| Mutation: a path list in a **method of a class** | red |
| Mutation: a direct `subprocess.run` path list at **module scope** | red — reports `<module>` |
| Mutation: a module-scope path list **inside an `if` block** | red — reports `<module>` |
| Mutation: a module-scope path list **inside a comprehension** | red — reports `<module>` |
| Refactor with no defect: rename a local in `corrected`; the call reflowed across lines | green, green — no false red |
| Refactor with no defect: git arguments hoisted into a tuple | **red** — and red against the pre-fix case at `b9caadb` too, so inherited rather than introduced |
| Refactor: a second but already-**filtered** path list in `corrected` | red (green before the fix) — judged a correct tightening, `_mentions` cannot tell which site filters |
| Finding 8: a second **unfiltered** path list, count bumped to 2 | **green** — the residual |
| Round 1's paste-ready shape vs the shipped `_path_list_words`, on the nested-calls mutation | `{'corrected': 1}` passes vs `{'corrected': 2}` fails; identical on the unmutated module |
| `bin/survivor-check --range bc5248c...fb64d06` — the gate's own range | **exit 0** · 902 files · 6 removed sentences · no removed wording still standing |
| `bin/survivor-check --range b9caadb..fb64d06` — the fix pass's range | exit 1 · 14 removed sentences · 5 places, all naming the old `_derives_a_path_list` body |
| `bin/evidence-check .` at `fb64d06` | exit 0 · 1149 ok · 0 drifted · 0 broken · `0 refused` |
| `bin/unverified-check` on the memo | exit 0 · 5 open · 1 closed — the restored row is the closed one |
| `bin/unverified-check --baseline bc5248c` | exit 0 — the memo is absent at the base, so the deletion was invisible to it |
| The four `phases/phase-N.md` records, read for `Ran by` | all four carry `specseal:smith` on `claude-opus-5` |
| The broad gate — the full suite, the repository-wide lint, the format check | **not yet.** Unrun and unclaimed at `fb64d06`. `agent-contract` §2 keeps it out of this round and the memo's `## Not verified` assigns it to the sealer. **It has now come due**: this round leaves nothing open, so what comes next is the sealer's spawn |

Every mutation was applied in the clone and the module restored byte-identical,
verified by hash after each. The clone reported a clean tree at `fb64d06`
before it was deleted. No probe file was left in either tree.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The exemption path — a `survivors.md` row still silences its own survivor through the diff | Already deferred by this work item: Q1 answered *out*, `plan.md` phase 4 closes `deferred #371`, and the `seal/follow-up.md` row now names #308 as its corpus half | the repository owner, on #371 with #308 |
| Whether any branch in flight now reports a survivor it did not report before | Already deferred: `overview.md` `## Not verified` | the first pull request into a release branch after this merges |
| Windows | Already deferred: `overview.md` `## Not verified` | CI, or whoever next runs the check on Windows |
| Finding 8 — a second unfiltered site in a declared scope, after the count is bumped | Not deferred by this round; recorded as ⬜ so the next reader does not re-find it. No ticket asked for | the repository owner, if it is ever worth a row |

Needs a fix: no

Loses a record or crashes: no

## Proof block

Opened and read in full: `tests/test_a_corrected_sentence_survives_elsewhere.py`
(the whole changed block — `_path_list_words`, `_derives_a_path_list`,
`_mentions`, `_callers_of`, `_function`, the enumeration case and the docstring
case), `skills/code-review/scripts/survivor_check.py` (`git`, `tracked`,
`corpus`, `corrected`, `whole_range`, and the docstring section the case pins),
`.github/workflows/hygiene.yml` (the survivor step and its range),
`bin/survivor-check`, `bin/test`, `seal/follow-up.md` (the changed row),
`seal/ledger/1789211172-a-round-record-disarms-survivor-check.md`,
`skills/implement/SKILL.md` §4, and under
`seal/specs/1789211172-a-round-record-disarms-survivor-check/` —
`rounds/round-1.md`, `rounds/round-1-report.md`, `overview.md`,
`phases/phase-5.md`, and all four `phases/phase-N.md` `Ran by` rows.

Inherited from round 1 without re-deriving: the fix on `corrected` itself,
`whole_range`'s unfiltered list and its ownership argument, phase 1's red
output, and A6. Round 1 opened those and closed them, and nothing in this
diff touches them.
