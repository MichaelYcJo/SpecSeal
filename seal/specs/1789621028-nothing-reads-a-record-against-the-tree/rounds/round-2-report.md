# Round 2 — the verifying round, on round 1's fixes

Round 2 of #344, #426 and #427 at `6522c19f`, on
`fix/344-426-427-nothing-reads-a-record-against-the-tree`, against
`release/v0.12.1` at `56945007`. The target is the fix diff
`b38bd920..bf693bc1`, six commits, plus the closing commit that wrote
`rounds/round-1.md`. Reviewed in a `git clone --no-local` at the target SHA;
every mutation below was reverted there and the clone ends byte-clean.
Nothing was written in the working checkout but this file.

## How the findings relate

All ten of round 1's verdicts hold. What this round opens is in the two
**test** files the fix pass touched, and both are the same shape — an
assertion that is wrong about what it is measuring.

```
① round 1's ten verdicts          — opened one by one, all ten stand
      ↓ but the fix pass rewrote one case and wrote one new one
② the rewritten case turns red the moment this branch merges   🔴 1
      ↓ and the new case's last assertion compares a file to itself
③ `close` can write the record and the case still passes        🟡 2
      ↓ and the corrected corpus figures did not reach every cell
④–⑧ corrections, five of them in records                        ⬜
```

The two findings are independent of each other and of the ten closures. Both
live in code the fix pass added or rewrote, which is the surface
`round-1.md`'s `New units` row and the verifying round's own rule point at.

---

## The ten closures, opened one by one

### The seven `fixed`

**🟡 2 — `close` refuses a record with no row, and now names the repair.
Closed, and the closure holds.** Reverting the `try`/`except` in
`skills/code-review/scripts/round_record.py` back to the bare
`raw[field_index(reader, lines, chain.FIX_RANGE)] = fix_range` reddens the
new case. **executed**, exit 1:

```
E   AssertionError: round-record: the record has 0 `| Fix range | … |` rows and needs one
E   assert 'no `| Fix range | … |` row' in 'round-record: the record has 0 `| Fix range | … |` rows and needs one\n'
tests/test_the_fixes_close_the_record.py:2528: AssertionError
```

Restored, exit 0. The case pins the four things the repair owes — the row
that is missing, the row to add, where it goes, and that no cell was written —
and it pins the old message's bare count being gone.

**The argument for leaving the behaviour alone is sound.** `close` replaces a
row rather than inserting one because a record's field order is the
template's, and a `close` that inserted would place the row by whatever it
happened to find. Grandfathering the generator would mean writing a row into
a record whose author never saw the field. **read** —
`docs/review-chain-spec.md` §*The fix range* now carries *The grandfathering
is the checker's and not the generator's*, and the changelog fragment splits
*What changes for a caller* into the pull request's half and the generator's.
Both documents now say which side grandfathers. That is what round 1 asked
for.

**🟡 3 — the corpus count now names its command. Closed, and I reproduced the
command myself rather than the number.** **executed**, the command
`docs/review-chain-spec.md` §*The fix range* states, run at both tree states
in the clone:

| | files | stating a range | ending `HEAD` | distinct forms |
|---|---|---|---|---|
| at `56945007` | 39 | 15 | **5** | 12 |
| at `6522c19f` | 39 | 15 | **4** | 12 |

Every figure the document, the changelog fragment and ledger row R8 state
reproduces, and the moving figure moves for the reason the document gives —
the work pinned one of the five. The document says so in its own words, under
*That the same command gives 5 and then 4 is the point, not a caveat*, so it
does not read as a contradiction.

The constant comment in `skills/code-review/scripts/chain_check.py` no longer
carries the method-less count; it points at the document instead. That was
the one instance living in shipped code and it is gone. **read**.

Where the propagation stopped short is ⬜ 4 below.

**⬜ 4 — the two comment blocks are apart, and each sits above its own call.
Closed.** **read** — `chain_check.py` `main` now reads *It IS grandfathered,
behind `RANGE_FROM`* above the `fix_range` call and *it has NO cutoff* above
`doubled_grounds`. A reader checking either property from the call site now
gets it right. The wrong cross-reference inside that comment is ⬜ 6 below.

**⬜ 5 — the template row closes its pipe. Closed.** **read**, and
**executed**: reverting the pipe reddens nothing across the three modules
that read this template — 181 passed, exit 0. That is disclosure rather than
a demand, and it is in ⬜ 8 below with ⬜ 8's twin.

**⬜ 6 — the pinned command no longer claims a number it does not produce.
Closed on the substance, and the repair broke the sentence.** The prose now
attributes the sixteen to the branch's life rather than to one run, which is
the claim round 1 said was false. The wording is ⬜ 5 below.

**⬜ 7 — the divergence row exists. Closed.** **read** —
`overview.md` §*Where spec and implementation diverged* now carries a row for
the `seal/ledger.md` re-stamp, and it says the right thing: the exclusion's
grounds were about removal, a drifted row takes the tree to NOT SEALED under
`--strict`, so leaving them was not available and the scope line anticipated
the wrong verb.

**⬜ 8 — `close`'s count guard reads the command the way `chain_check` reads
it. Closed.** **read** — `counted is None or not counted.strip().isdigit()`
now matches `fix_range` forty lines away. **executed**: reverting the
`isdigit()` half reddens nothing — 102 passed, exit 0. See ⬜ 8 below.

### The two `answered`

**⬜ 9 — the git cost. The answer holds; one figure in it has gone stale.**
The reasoning is right and it is the reasoning that matters: memoizing
`resolves_to` changes a function five arms share, which is mechanism a fix
pass may not build, and the cost becomes measurable the moment it becomes
real. I accept it.

The figure beside it does not survive its own record. **executed** — walking
every `round-N.md` in the tree through `fix_range` with `chain_check`'s git
helper instrumented: 230 records, 0 errors, 229 notices, and **1** call, not
0:

```
git calls made by fix_range: 1 in 0.120s
    ('rev-list', '--count', 'b38bd92…..bf693bc1…')
```

The call is `round-1.md`'s own, and the grounds cell saying *0 git calls* was
written into the record that made it false. That is ⬜ 7 below.

**⬜ 10 — the two surviving `..HEAD` fix tables. The answer holds.** **read** —
`spec.md` §Out does exclude records of any work item other than 1789034970's,
`RANGE_FROM` does excuse them, and recording the survival rather than fixing
it is the right handling for a branch that was not asked to touch them. I
accept it. The branch then wrote a new moving range of its own, which is ⬜ 3.

### The one `deferred`

**🟡 1 → #436. Verified.** **executed** — the issue exists, is `OPEN`, and is
titled *fix: chain-check never names a Fix range still saying the fixes are
not yet written*. Its body carries the orchestrator's own execution of the
planted record, points at round 1's record for the paste-ready arm, names the
cutoff question as a judgment for whoever builds it, and lists what not to
build. It says what the row claims it says.

---

## 🔴 1 — the rewritten case turns red the moment this branch merges

`tests/test_chain_check_at_the_pull_request.py:2843`, the
`assert printed == len(records) - len(carrying)` line of
`test_the_records_in_this_repository_are_not_failed_by_the_new_row`.

The subtraction says: every record that carries the row produces **zero**
notices. Nothing guarantees that, and the module under test documents the
opposite as normal. `fix_range` returns a notice for a record whose range
ends this repository cannot see, and its own docstring calls that *the
ordinary state of a merged record and not a fault in it*, because a feature
branch squashes into its release branch and the squash keeps none of the
branch's own commits.

`round-1.md` is the only record carrying the row, and its ends are
`b38bd920…` and `bf693bc1…` — two commits of this feature branch. They
resolve today because the branch exists. They stop resolving once #435
squash-merges and the branch is deleted, which is the merge method the
repository rule fixes for this direction. `.github/workflows/test.yml` checks
out at `fetch-depth: 0`, which fetches branches and tags and not
`refs/pull/*` — `hygiene.yml` says so in its own comment — so a merged
`release/v0.12.1` has no path to those objects.

**executed** — the squash simulated in the clone by pointing the record's
range at two commits this repository does not hold, everything else
untouched:

```
AssertionError: 230 notices over 229 records with no row: a record that
predates the row has to print, not go quiet
assert 230 == (230 - 1)
tests/test_chain_check_at_the_pull_request.py:2843: AssertionError
```

Exit 1. Restored, exit 0.

**What it costs.** The suite goes red on `release/v0.12.1` at the first run
after this branch merges, on a branch nobody is working on, with a message
that names the wrong cause — it reports a record *going quiet* when the
record did exactly what the checker's docstring says a merged record does.
This repository has the same shape in its own history:
`tests/test_a_rider_reaches_its_file.py` went red after a merge and a patch
release exists to fix one line of it.

**The case's own comment describes the right rule and the arithmetic does not
implement it.** The comment says *a record WITHOUT the row is printed and
never failed, and the two groups account for every record*. Counting notices
only over the records with no row says exactly that, and says nothing about
what a record with the row prints.

## 🟡 2 — the new case's last assertion compares the file to itself

`tests/test_the_fixes_close_the_record.py:2537`, the
`assert record == path.read_text(encoding="utf-8"), "the refusal wrote
anyway"` line of
`test_a_record_with_no_fix_range_row_is_told_which_row_to_add`.

`record` is what the module's `close` helper returns, and that helper reads
the record **after** the subprocess. The assertion then reads the same path a
second time and compares the two. Both are post-run reads of one file, so the
comparison is between a value and itself and cannot fail however much `close`
wrote.

**executed** — `close` altered to overwrite every `round-*.md` under the work
item with `CLOBBERED BY THE PROBE` before raising, and the case run against
it:

```
=== case run with `close` clobbering the record -> exit 0
    1 passed in 0.86s
=== restored -> exit 0
```

The record was destroyed and the assertion whose message is *the refusal
wrote anyway* said nothing.

**What it costs.** `close` refusing without writing is the half of this
behaviour that keeps a refusal repairable — round 1's own finding turned on
*nothing reaches disk, which is right*. The new case is the only thing in the
tree that claims to pin it on this path, and it pins nothing. A later change
that made `close` write before refusing would ship green.

The fix is one variable: keep the bytes the test itself wrote before the run
and compare against those. The test already computes them.

## ⬜ 3 — the new exemption file states a moving range

`seal/specs/1789621028-nothing-reads-a-record-against-the-tree/survivors.md:3`
— the heading `## Round 1's fix pass — ` followed by the range
`b38bd920..HEAD`.

This is the class the work item is named after, in a file the fix pass
created. The file makes a reproducible claim under that heading — *the range
is exit 0 and one row is used* — and the second end of the range it names
moves with every commit.

**executed**, both readings in the clone: `--range b38bd920..bf693bc1` and
`--range b38bd920..HEAD` each exit 0 with `every survivor is excused by a row
above (1)`, and each names `spec.md:46` as the one row used. So the claim is
true today under either reading, and under the second it stops being a claim
anybody can re-run once the tip moves.

The sibling file the same fix pass repaired, `1789034970-…/survivors.md`, was
pinned to `d35c874...ce0f9fe` for exactly this reason. The convention was
established and then not followed one file over.

## ⬜ 4 — the retired spellings figure survives in the two cells beside the ones that were corrected

`seal/ledger/1789621028-nothing-reads-a-record-against-the-tree.md:10`, R8's
`Notes` cell; and
`seal/specs/1789621028-nothing-reads-a-record-against-the-tree/overview.md:26`
and `:59`.

The corrected figure under the named command is **12 distinct sentence
forms**. R8's `Verified behavior` cell now says 12. Its `Notes` cell, in the
same row, still argues *15 files in 8 spellings refuses the parser more
firmly than 11 in eleven did*. `overview.md`'s divergence row does the same
thing across two cells of one row: `Chosen` says 12, `Grounds` says 8. And
`overview.md:59` states, in plain prose with no correction beside it, *the
grounds are the 8 spellings measured across 15 files*.

The three records that hold the figure as a record of a moment —
`phases/phase-3.md`, `phases/phase-4.md`, and `spec.md` through the exemption
— each carry the correction the repository's convention asks for. These three
do not, and two of them are cells of the very rows the fix pass edited for
this finding.

Nothing decided rests on it: 12 forms refuses the parser at least as firmly
as 8 did. What it costs is that the ledger row written to close *a number
quoted without its method* quotes a number without its method in its own
second cell.

## ⬜ 5 — the reworded sentence no longer joins its own tail

`seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/survivors.md:5`.

Round 1's ⬜ 6 asked for the number the pinned range produces to be stated in
the prose. The repair instead moved the sixteen off the command and onto the
branch's life, which answers the substance. It reworded only the first half of
the sentence, and the second half was written to continue the first.

**executed** — the file with HTML comments stripped, which is how a reader
sees it:

```
Sixteen places were reported across this branch's life by
`survivor-check --range d35c874...ce0f9fe`

across this branch — fifteen at the head it was first run against, and a
sixteenth once the note explaining a removed ledger row landed, …
```

*across this branch's life* and *across this branch* now say the same thing
twice with the command between them, and the tail begins as a fragment.
Before the edit the head read *`survivor-check --range d35c874...ce0f9fe`
reports sixteen places* and the tail completed it.

## ⬜ 6 — a comment in shipped code cites the wrong finding

`skills/code-review/scripts/chain_check.py:4271`, inside the `fix_range`
comment block: *so the two comments are kept apart on purpose (round 1's 8)*.

The comment separation is round 1's ⬜ **4**. Round 1's ⬜ 8 is the
`isdigit()` guard, and `round_record.py:3797` cites it correctly as *(round
1's 8)* in the other file. So the tree now has two comments citing the same
finding for two unrelated repairs, and a reader following this one lands on a
guard in a file that has nothing to do with comment placement.

Every other citation in these two modules carries the severity marker —
*round 1's 🟡 1*, *round 1's 🔴 2* — or the word *finding*. This one carries a
bare number, which is what made the collision possible.

## ⬜ 7 — an `answered` grounds cell states a figure its own record falsified

`seal/specs/1789621028-nothing-reads-a-record-against-the-tree/rounds/round-1.md:37`,
⬜ 9's `Grounds` cell: *the arm run over all 230 records in this tree makes 0
git calls in 0.057 s*.

The measurement was true when it was taken and stopped being true when
`round-1.md` was written with a real range in it. **executed**, above: 1 call.
The same commit that wrote this sentence is the commit that made it false,
which is this work item's own class one more time, in one of its own cells.

The answer it supports is unaffected — 1 call is as good as 0 for the
argument that memoizing is not owed yet.

## ⬜ 8 — two of the seven closures are pinned by nothing

`templates/sdd-round.md`, the `| Fix range |` row's closing pipe; and
`skills/code-review/scripts/round_record.py`, `close`, the `isdigit()` half of
the count guard.

**executed** — each reverted alone:

| Reverted | Ran | Result |
|---|---|---|
| the template's closing pipe | the three modules that read this template | 181 passed, exit 0 |
| the `isdigit()` half of the guard | `tests/test_the_fixes_close_the_record.py` | 102 passed, exit 0 |

Both are cleanups round 1 recorded as breaking nothing, so this is disclosure
rather than a demand. It is worth one line because the `isdigit()` half is a
new refusal path rather than a cosmetic change — it is unreachable in
practice, since `git rev-list --count` answers a digit or fails, and an
unreachable refusal with no case is a thing the next reader cannot tell from a
reachable one.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The rewritten repository-wide case asserts that a record carrying the row prints no notice, which the checker's own docstring calls the ordinary state of a merged record — so the case turns red on `release/v0.12.1` at the first run after this branch squash-merges | `tests/test_chain_check_at_the_pull_request.py:2843` · `test_the_records_in_this_repository_are_not_failed_by_the_new_row`, the `printed == len(records) - len(carrying)` assertion | open | Executed: the record's ends pointed at commits this repository does not hold, everything else untouched — exit 1, `230 notices over 229 records with no row`, `assert 230 == (230 - 1)`; restored exit 0. `fix_range` answers unresolvable ends with a NOTICE, `.github/workflows/test.yml` checks out at `fetch-depth: 0` which never fetches `refs/pull/*`, and the repository rule squashes a feature branch into its release branch |
| 🟡 2 | The new case's `the refusal wrote anyway` assertion compares two post-run reads of one file, so it cannot fail | `tests/test_the_fixes_close_the_record.py:2537` · `test_a_record_with_no_fix_range_row_is_told_which_row_to_add` | open | Executed: `close` altered to overwrite every `round-*.md` under the work item before raising — the case still passed, exit 0, and the assertion whose message is `the refusal wrote anyway` said nothing. The helper reads the record after the subprocess and the test reads the same path again |
| ⬜ 3 | The exemption file this fix pass created states its range as `b38bd920..HEAD`, a moving end, in the work item that exists to refuse them — while the sibling file the same pass repaired was pinned | `seal/specs/1789621028-…/survivors.md:3` | open | Executed: both `..bf693bc1` and `..HEAD` exit 0 with one row used, so the stated result is true today and re-runnable under only one of them |
| ⬜ 4 | The retired `8 spellings` figure survives in R8's `Notes` cell and in two places in `overview.md`, two of them cells of the very rows the fix pass corrected to `12` | `seal/ledger/1789621028-…md:10` · R8 `Notes`; `seal/specs/1789621028-…/overview.md:26` and `:59` | open | Read: R8's `Verified behavior` says 12 distinct sentence forms and its `Notes` argues from 8; `overview.md`'s divergence row says 12 in `Chosen` and 8 in `Grounds`. The three records of a moment that hold the old figure all carry a correction beside it; these do not |
| ⬜ 5 | Round 1's ⬜ 6 repair reworded the first half of a sentence and left the second half, which was written to continue it | `seal/specs/1789034970-…/survivors.md:5` | open | Executed, the file with HTML comments stripped: `across this branch's life by <command>` is followed by `across this branch — fifteen at the head…`, so the phrase is doubled and the tail begins as a fragment |
| ⬜ 6 | A comment in shipped code cites `round 1's 8` for what is round 1's ⬜ 4, while `round_record.py` cites the same number correctly for ⬜ 8 | `skills/code-review/scripts/chain_check.py:4271` · the `fix_range` comment block in `main` | open | Read: the separation of the two comment blocks is ⬜ 4; ⬜ 8 is the `isdigit()` guard at `round_record.py:3797`, which cites `(round 1's 8)` correctly. Every other citation in these two modules carries the severity marker or the word `finding` |
| ⬜ 7 | ⬜ 9's `answered` grounds state `0 git calls`, and the commit that wrote the sentence is the commit that made it false | `seal/specs/1789621028-…/rounds/round-1.md:37` · ⬜ 9's `Grounds` cell | open | Executed: `fix_range` over all 230 records with the git helper instrumented makes **1** call, `rev-list --count` for `round-1.md`'s own range, in 0.120 s. The answer it supports is unaffected |
| ⬜ 8 | Two of the seven closures — the template's closing pipe and the `isdigit()` half of `close`'s count guard — are pinned by no case | `templates/sdd-round.md` · the `\| Fix range \|` row; `skills/code-review/scripts/round_record.py` · `close` | open | Executed, each reverted alone: the pipe gives 181 passed exit 0 over the three modules reading the template, the guard gives 102 passed exit 0 over `tests/test_the_fixes_close_the_record.py`. Both are cleanups round 1 recorded as breaking nothing; the guard is a new refusal path rather than a cosmetic change |
| 🟢 9 | 🟡 1 of round 1 — the pending `Fix range` no arm reads back | `skills/code-review/scripts/chain_check.py` · `fix_range`, the `says_none` early return | deferred #436 | Executed: issue #436 exists and is `OPEN`, titled `fix: chain-check never names a Fix range still saying the fixes are not yet written`. Its body carries the orchestrator's execution, points at round 1's record for the paste-ready arm, names the cutoff question as the builder's judgment, and lists what not to build. The row's claim holds |
| 🟢 10 | 🟡 2 of round 1 — `close`'s refusal names no repair | `skills/code-review/scripts/round_record.py` · `close` | fixed | Executed: the `try`/`except` reverted to the bare `field_index` write reddens the new case at exit 1, `assert 'no \| Fix range \| … \| row' in 'round-record: the record has 0 … rows and needs one'`; restored exit 0. Read: the behaviour argument holds, and `docs/review-chain-spec.md` §*The grandfathering is the checker's and not the generator's* and the changelog's split `What changes for a caller` now say which side grandfathers |
| 🟢 11 | 🟡 3 of round 1 — a corpus count with no command | `docs/review-chain-spec.md` · §*The fix range* | fixed | Executed: the document's own command run in the clone gives 39 / 15 / 5 / 12 at `56945007` and 39 / 15 / 4 / 12 at `6522c19f`, matching the document, the changelog fragment and R8 exactly. The document states the moving figure as the point rather than as a caveat. The constant comment in `chain_check.py` no longer carries the method-less count. Where the propagation stopped short is ⬜ 4 above |
| ⬜ 12 | ⬜ 4 of round 1 — stacked comment blocks | `skills/code-review/scripts/chain_check.py` · `main` | fixed | Read: each block now sits above its own call and states that arm's cutoff correctly. The citation inside it is ⬜ 6 above |
| ⬜ 13 | ⬜ 5 of round 1 — the template's missing pipe | `templates/sdd-round.md` | fixed | Read: the row closes. Executed: nothing pins it — ⬜ 8 above |
| ⬜ 14 | ⬜ 6 of round 1 — a pinned command beside a number it does not produce | `seal/specs/1789034970-…/survivors.md` | fixed | Read: the sixteen is now attributed to the branch's life rather than to one run of the pinned command, which answers the substance. The wording it left behind is ⬜ 5 above |
| 🟢 15 | ⬜ 7 of round 1 — the ledger re-stamp had no divergence row | `seal/specs/1789621028-…/overview.md` · §*Where spec and implementation diverged* | fixed | Read: the row exists and states the right thing — the exclusion's grounds were about removal, and a drifted row takes the tree to NOT SEALED under `--strict`, so leaving them was not available |
| ⬜ 16 | ⬜ 8 of round 1 — half a guard the neighbouring module writes in full | `skills/code-review/scripts/round_record.py` · `close` | fixed | Read: `counted is None or not counted.strip().isdigit()` now matches `fix_range`. Executed: nothing pins it — ⬜ 8 above |
| ⬜ 17 | ⬜ 9 of round 1 — the arm's git cost | `skills/code-review/scripts/chain_check.py` · `fix_range` and `resolves_to` | answered | The reasoning is accepted: memoizing a function five arms share is mechanism a fix pass may not build, and the cost becomes measurable when it becomes real. Executed: the figure beside it is stale — 1 call, not 0, which is ⬜ 7 above and does not change the answer |
| ⬜ 18 | ⬜ 10 of round 1 — two surviving `..HEAD` fix tables | `seal/specs/1789598366-…/rounds/round-1-fixes.md` and `round-2-fixes.md` | answered | Accepted. Read: `spec.md` §Out does exclude records of other work items, `RANGE_FROM` does excuse them, and recording the survival is the right handling for a branch that was not asked to touch them. The branch then wrote a new moving range of its own, which is ⬜ 3 above |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_fixes_close_the_record.py tests/test_chain_check_at_the_pull_request.py -q` in the clone at `6522c19f` | 229 passed, exit 0 — the baseline every mutation below was taken against |
| `close`'s `try`/`except` reverted to the bare `field_index` write, then restored | exit 1 mutated, exit 0 restored — the new case reddens on the exact old message |
| the record's range ends pointed at commits this repository does not hold, then restored | exit 1, `230 notices over 229 records with no row`, `assert 230 == (230 - 1)`; exit 0 restored — 🔴 1 |
| `RANGE_FROM` moved to `1`, then restored | exit 1 on `assert not failed`, naming five records of work items begun before the cutoff — ledger R6's own claim, reproduced |
| `close` altered to overwrite every `round-*.md` before raising, then restored | **exit 0, 1 passed** — the `the refusal wrote anyway` assertion never fires — 🟡 2 |
| the `isdigit()` half of `close`'s count guard reverted, then restored | 102 passed, exit 0 — nothing pins it |
| the template's closing pipe reverted, then restored | 181 passed, exit 0 over the three modules that read the template — nothing pins it |
| the command `docs/review-chain-spec.md` §*The fix range* states, at `56945007` and at `6522c19f` | 39 / 15 / **5** / 12 and 39 / 15 / **4** / 12 — every shipped figure reproduces |
| `fix_range` over all 230 `round-N.md` files with `chain_check`'s git helper instrumented | 0 errors, 229 notices, **1** git call in 0.120 s |
| `bin/survivor-check --range b38bd920..bf693bc1 --exempt <this item's survivors.md>` | exit 0, 1068 files against 31 removed sentences, one exemption row used, `every survivor is excused by a row above (1)` |
| `bin/survivor-check --range b38bd920..HEAD --exempt <the same>` — the range the file literally states | exit 0, same result at `6522c19` |
| `bin/evidence-check` in the clone | exit 0, **1340 ok**, 0 drifted, 0 broken |
| `gh issue view 436` | `OPEN`, and the body says what `round-1.md`'s deferred row claims |
| The full suite, the repository-wide lint and the typecheck | **not yet** — `agent-contract` §2 leaves all three to the sealer and this round ran none of them. They are not due yet either: 🔴 1 and 🟡 2 are open, so a fix pass and one further verifying round come first |

Every mutation was applied alone, reverted in a `finally`, and every
substitution asserted it matched. The clone ends with an empty
`git status --porcelain`. Exit codes were read from `returncode` and never
through a pipe.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether a record's `Location` cell should become a content anchor | `questions.md` Q1 of this work item | the repository owner |
| Whether `chain_check.fix_range` behaves correctly on a record read after a real squash rather than in a fixture | `overview.md` §Not verified | the repository owner, at the first release that merges a work item carrying the row |

Both are carried forward from round 1 unchanged. The second is worth reading
beside 🔴 1: the deferral is about the **checker** after a squash, and 🔴 1 is
about the **case**. The checker does the right thing — it prints. The case is
what fails.

## Paste-ready fixes

🔴 1 — `tests/test_chain_check_at_the_pull_request.py`. Count the notices only
over the group the claim is about, so a notice from a record that carries the
row cannot break the arithmetic. Replace the loop and the closing assertions:

```python
    assert len(records) > 200, f"the walk found {len(records)} records"
    failed, printed_without_a_row, carrying = [], 0, []
    for rel in sorted(records):
        errors, notices = check.fix_range(reader, ROOT, rel)
        failed.extend(errors)
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            carries = f"| {check.FIX_RANGE} |" in f.read()
        if carries:
            carrying.append(rel)
        else:
            printed_without_a_row += len(notices)
    assert not failed, f"records the new row would fail: {failed[:5]}"
    # The population, split the way the tree is actually split. Until this
    # work item's own round 1 there was no record carrying the row at all and
    # this read `printed == len(records)`; the first record to carry one made
    # that false, which is the case being right rather than the tree being
    # wrong. What has to hold is that a record WITHOUT the row is printed and
    # never failed, and that the two groups account for every record -- a walk
    # that quietly read nothing would report no failures too.
    #
    # The notices are counted over that group ALONE, never as a subtraction
    # from the whole. A record that HAS the row prints whenever its ends stop
    # resolving, which `fix_range`'s own docstring calls "the ordinary state
    # of a merged record and not a fault in it" -- and the squash that merges
    # this branch makes it the state of the one record carrying the row. A
    # subtraction asserts that such a record prints nothing, which is the
    # opposite of what this module documents (round 2's 1).
    assert carrying, "no record in this tree carries the row, so nothing is read"
    assert printed_without_a_row == len(records) - len(carrying), (
        f"{printed_without_a_row} notices over {len(records) - len(carrying)} "
        "records with no row: a record that predates the row has to print, "
        "not go quiet"
    )
```

🟡 2 — `tests/test_the_fixes_close_the_record.py`. Keep the bytes the test
wrote before the run and compare against those. First, name them where the
test already computes them:

```python
    stripped = text.replace(row + "\n", "")
    path.write_text(stripped, encoding="utf-8")
```

Then compare the returned record against those bytes rather than against a
second read of the same file:

```python
    # The bytes from BEFORE the run, never a second read of the file the run
    # may have written. `close` in this module returns the record it read
    # AFTER the subprocess, so comparing that against another read of the
    # same path compares the file to itself and passes however much `close`
    # wrote -- shown by making `close` clobber every record before raising
    # and watching this line stay green (round 2's 2).
    assert record == stripped, "the refusal wrote anyway"
```

⬜ 3 — `seal/specs/1789621028-nothing-reads-a-record-against-the-tree/survivors.md`,
the heading. Pin the end the way the sibling file was pinned:

```markdown
## Round 1's fix pass — `b38bd920..bf693bc1`
```

⬜ 4 — `seal/ledger/1789621028-nothing-reads-a-record-against-the-tree.md`, R8's
`Notes` cell, and
`seal/specs/1789621028-nothing-reads-a-record-against-the-tree/overview.md`
lines 26 and 59. In all three, the argument reads the same way with the
corrected figure:

```markdown
None of them changes a decision — 15 files in 12 sentence forms refuses the
parser more firmly than 11 in eleven did — and what matters is that the
measured figures are what shipped into the specification, with the command
that produces them named beside them.
```

⬜ 5 — `seal/specs/1789034970-the-contract-is-settled-against-the-agents-that-exist/survivors.md`.
Let the head and the tail be one sentence again:

```markdown
Sixteen places were reported across this branch's life by
`survivor-check --range d35c874...ce0f9fe`
```

becomes

```markdown
`survivor-check --range d35c874...ce0f9fe` reports two places today. Sixteen
were reported across this branch's life
```

⬜ 6 — `skills/code-review/scripts/chain_check.py`, the `fix_range` comment
block in `main`:

```python
            # (round 1's ⬜ 4). Whether an arm has a cutoff is the load-bearing
```

⬜ 7 — `seal/specs/1789621028-nothing-reads-a-record-against-the-tree/rounds/round-1.md`,
⬜ 9's `Grounds` cell. The record is not rewritten; the correction goes beside
it, the way this work item corrected its own phase records:

```markdown
the arm run over all 230 records in this tree makes 0 git calls in 0.057 s
<!-- Round 2, 2026-09-17: 1 call, not 0 — `rev-list --count` for this
record's own range, which this record is what introduced. Executed with
`chain_check`'s git helper instrumented, 0.120 s over the same 230 records.
The answer is unaffected: 1 is as good as 0 for the argument that memoizing
is not owed yet. -->
```

⬜ 8 — no fix is proposed. Both are cleanups round 1 recorded as breaking
nothing, and the disclosure is the point.

Needs a fix: yes — 🔴 1, the rewritten case that reddens on the release branch
once this branch squash-merges; and 🟡 2, the new case's assertion that cannot
fail

Loses a record or crashes: no

## Proof block

Files opened: `skills/code-review/scripts/chain_check.py`,
`skills/code-review/scripts/round_record.py`, `docs/review-chain-spec.md`,
`templates/sdd-round.md`, `bin/test`, `CLAUDE.md`, `seal/config.md`,
`seal/ledger/1789621028-nothing-reads-a-record-against-the-tree.md`,
`seal/specs/1789621028-…/{overview,changelog,survivors}.md` and its
`phases/{phase-3,phase-4}.md` and `rounds/{round-1,round-1-report}.md`,
`seal/specs/1789034970-…/survivors.md`,
`tests/test_chain_check_at_the_pull_request.py`,
`tests/test_the_fixes_close_the_record.py`,
`.github/workflows/{test,hygiene}.yml`, `.github/scripts/run_tests.py`,
`~/.claude/skills/writing-style/SKILL.md`.

Commands run: listed in §*Executed probes*, all inside a `git clone
--no-local` at `6522c19f`. Every mutation was reverted in a `finally` and the
clone was verified byte-clean afterwards. The two probe drivers lived outside
the clone, in this session's scratchpad, and were deleted with it; no probe
file was ever written inside the clone.
