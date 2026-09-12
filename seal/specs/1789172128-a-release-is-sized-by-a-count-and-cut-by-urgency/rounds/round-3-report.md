# round 3 — the reopening's verifying round

Target: the diff of round 2's fixes, `405fe9d..3673e46`. Reviewed at `3673e46`,
in a `git clone --no-local` of this repository checked out there. Base
`origin/release/v0.11.1` = `7e17f5e`. `round-2.md`'s `New units` reads `none`,
so every surface here is a verification surface and nothing below is a first
review of new code.

**Six of round 2's seven verdicts are closed and the seventh stands answered.**
What I opened is one defect in tracked code and five corrections, and they line
up in one causal chain: the revert that the owner's answer required was taken on
the two cases and their constant, and four artifacts that described the
pre-revert tree were not brought with it — the module's own comment, ledger row
R1, `overview.md`'s memo row and `seal/follow-up.md`'s new row. The sixth is
separate and it is the loudest: a name a record uses no longer exists in the
tree, so the ledger gate refuses, and refuses on the pull request.

## 🟡 1 · the revert took the two cases and left the comment that introduces them

`tests/test_a_release_is_sized_by_a_criterion.py:259-270`. The module now ends
with a section rule and a paragraph, and nothing after it:

> `# --- the sweep's reach, pinned rather than left to the green answer ---`
> … *The two cases below are what stands between the reach and a later edit
> that trims it as unused.* … *Kept as data rather than as prose, so the
> sentences round 1 measured escaping are the ones asserted.*

There are no cases below and no data below. `wc -l` is 270 and the last
function ends at `:258`.

**Why it matters rather than reading badly.** The comment makes the exact claim
round 2's finding 2 was opened to deny — that the sweep's reach is pinned — and
it makes it in the file a maintainer opens when deciding whether an unused
regex alternative can go. Measured in the clone at `3673e46`: dropping the
pattern's three noun alternatives, dropping `CLAUDE.md` from `SCANNED`, and
dropping `hits()`'s joined-line branch each leave the module **green at 7
passed**. So the reach ships unpinned, which `rounds/round-3-fixes.md` states
plainly — and the module states the opposite.

This is the one thing I found in tracked code, and it is what `Needs a fix`
answers `yes` to. The paste-ready fix rewrites the block to say what the tree
is; deleting it whole is the other correct answer.

## ⬜ 2 · a record names a constant the revert removed, and the ledger gate refuses

`seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/rounds/round-3-fixes.md:49`
names the reverted constant in prose without the exemption marker on the line,
so `bin/evidence-check .` **exits 2**, not 1.

Measured, exit code read directly: **exit 2** at `3673e46` with one
`NOT-IN-TREE` refusal, and **exit 2** at `9e37d7a` with two — `round-3-asked.md:47`
repeats the same name on its own line. The ledger arm itself is clean:
**1145 ok · 0 drifted · 0 broken**, and the records arm's one drift at
`spec.md:159` is the one round 1 decided stays.

**This is a gate, and it is wired to the pull request.**
`.github/workflows/test.yml:85-91` runs the checker in the `ledger` job and
`exit`s on any code at or above 2, so PR #364's `ledger` job fails at both
SHAs. The same line-18 row of `round-3-fixes.md` already carries the marker
twice for the two reverted case names, so the convention was known to the pass
and applied once out of twice.

Reported as a correction because the location is under `seal/specs/`, per
`docs/review-chain-spec.md` §*The last round verifies*. It does not move
`Needs a fix`. It does have to be applied before the sealer is spawned: a broad
gate run over a tree whose `ledger` job is red is a spent run.

**The round's own paragraph claims exit 1 here.** That claim is false at
`3673e46`; I read exit 2 directly, no pipe. Recorded under §5 rather than as a
finding of its own.

## ⬜ 3 · ledger row R1 says the reach is pinned, and its own Notes cell says it is not

`seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`,
row R1. The `Verified behavior` cell reads *Round 2 found the sweep's own reach
unpinned and **it is pinned now**: … so two cases were added and each was seen
red under exactly its own mutation*. Neither half holds at `3673e46`: the cases
are not in the tree, and I measured all three widenings reverting green.

The `Notes` cell of the same row says the opposite and says it correctly — the
two coordinates were removed, *what went with those two is the pinning of the
sweep's REACH, which is #366*. So the row contradicts itself, and a reader who
stops at `Verified behavior` leaves with the answer the run spent two rounds
disproving.

`fold_ledger.py` moves this fragment into `seal/ledger.md` at the release,
where nobody re-runs it. This is the **third** statement in this one row that
did not match the tree — round 2's findings 4 and 5 were the first two — which
is why it is worth a paragraph rather than a line.

## ⬜ 4 · the disclosure's central promise is false: #365 alone does not re-arm the four rows

`seal/specs/1789172128-…/survivors.md` (header),
`seal/specs/1789172128-…/phases/phase-5.md`,
`seal/specs/1789172128-…/overview.md` (`## Not verified`),
`seal/specs/1789172128-…/rounds/round-2-fixes.md`, and
`seal/ledger/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships.md`
row S10.

The reach of the correction is right — I looked for every place this work item
offers a `survivor-check` exit 0 as evidence and the pass reached all of them.
What each of those places then asserts is that the four rows *are armed again
when #365 lands*, and that is a prediction stated as a fact.

**Measured.** With finding 3's own drafted fix applied to `corrected` — the
`rounds/` filter, which is the whole of #365 — the check at `3673e46` reports
**no survivors, exit 0, with and without `--exempt`**. The rows still excuse
nothing. They come back only when `seal/specs/*/survivors.md` is ALSO left out
of the added side, which is the *second* silencing path `seal/follow-up.md`
already carries a row for, and that is a different item from #365. So the
sentence a reader acts on — repair the checker and the judgments are live again
— names one of the two repairs it needs.

The same probe settles round 2's finding 5 in the fix's favour, which is worth
saying in the same breath: with both paths closed, `changelog.md:22` is printed
under `exempt` with its grounds. The re-anchored quote does exempt the
candidate. What fails is the claim about when.

One more thing that probe showed and nobody has a row for: with both paths
closed, two of the places reported as still carrying removed wording are
`survivors.md`'s own quote cells, `:24` and `:26`. An exemption file that
reports itself is a shape #365's fix will meet on its first run.

## ⬜ 5 · two records say the module is green at 9 passed; it is 7

`seal/follow-up.md`, the new `hits()` row, and
`seal/specs/1789172128-…/overview.md`'s new `## Not verified` row. Both say
reverting `hits()`'s joined-line branch leaves the module *green at 9 passed*.
Measured: it leaves it green at **7 passed**, because the two cases the count
included are the ones the revert removed.

The follow-up row scopes its number — *measured in round 2's fix pass* — so it
reads as history and costs a reader one reconciliation. The `overview.md` row
carries no scope at all and reads as the state of the tree. The claim both make
is true; only the number is of a tree that no longer exists.

## ⬜ 6 · two bold runs with no space between them in R1's Notes

`seal/ledger/1789172128-…md`, row R1: `…which is **#366**.**This row replaces
S3 of …**`. Rendered, that is `#366.This row replaces`, with the sentence
boundary gone. One space.

## Round 2's seven verdicts — the answers

Re-derived rather than inherited. The coordinates came from `round-2.md`; the
verdicts did not.

| # | Round 2's finding | Recorded | My answer |
|---|---|---|---|
| 1 | the label's two moments | fixed `95b3d83` | **closed.** Read at `3673e46` against `docs/issues-and-milestones.md:208` (the section title), `:210-213` (*for the length of a release*) and `docs/branch-and-release.md:256-258`. The new clause puts the removal at *the release reaches `main` and the issue closes* and `merged: X.Y.Z` *earlier inside that same release, at the squash onto the release branch*. Both are true of the mechanisms: `label_merged_on_release_branch.py` fires on a push to `release/*`, which for a feature branch is the squash this repository's merge table fixes; `close_issues_on_release.py` fires on a push to `main`. The third attempt is true of both, and it names the other label's mechanism rather than its distance |
| 2 | nothing distinguishes the fixed module from the defective one | deferred #366 | **closed as deferred, with the revert incomplete.** The code half is right: the three widenings are in the tree, the module runs 7 passed, and I measured each of the three reverting green — so *ships unpinned* is the honest state and `round-3-fixes.md` states the cost rather than absorbing it. What the revert left is finding 1 above, the comment that introduces cases that are gone. The owner's answer on the depth refusal is not reopened |
| 3 | `corrected` misses the `rounds/` exclusion | deferred #365 | **closed as deferred; the disclosure reaches every site and its central claim is false** — finding 4 above. #365 is filed and the four rows are kept, which is the right treatment; what is wrong is *armed again when #365 lands* |
| 4 | *by path* where the code excludes by basename | fixed `95b3d83` | **closed.** `tracked()` at `:138-150` filters on `os.path.basename(rel) != SELF`, and the docstring at `:31-33` and R1 both now say basename. The claim *a copy of it anywhere in the scanned set is excluded with it* follows from that filter |
| 5 | the survivors file excuses nothing, and the quote would not match | fixed `34beebb` | **closed, on a measurement.** With both silencing paths closed, `exempted` answers with grounds for `changelog.md:22` and the check prints it under `exempt` — the re-anchoring onto the surviving sentence works. The finding's second location, `round-1.md`'s probe row, needed nothing and got nothing: at round 1's target one survivor WAS reported and the row excused it, so *16 removed sentences, 1 survivor, excused by a row* is true at its own SHA. Round 2's claim that both records stated a check that found nothing was right about `survivors.md`'s header and not about that row |
| 6 | R1 cites the sweep unit but not the helper | fixed `34beebb` | **closed.** `hits@d323992a` is in R1's `Code grounds`, and the ledger arm reads 1145 ok · 0 drifted · 0 broken at `3673e46` — executed |
| 7 | `hits()`'s one-boundary assumption | answered | **stands, not reopened.** The residual is disclosed in `seal/follow-up.md` and `overview.md`'s memo, which is what an answered finding owes |

## Not mine, and left alone

The four owner answers (Q1 (c) and no edit to `tests/test_release_hygiene.py`;
Q2 (b); Q3 (a) and no tracker write; Q4 (a)), round 1's two judgments,
`hits()`'s one-boundary assumption, and the owner's answer to take the depth
gate's exit. Whether `depth_two` should key on something finer is #366's
question and I did not form one.

## ❓ out of verified scope

The broad gate — the full suite, the repository-wide lint, the typecheck. Not
run here; `agent-contract` §2 assigns it to the sealer, once, after the rounds
settle. **Answered by: the sealer, spawned by the orchestrating session.** It
comes due when this record closes, and finding 2 has to be applied first or the
`ledger` job is red under it.

`9e37d7a`, which adds `round-3-asked.md`, is outside the target range. I read
its evidence-check consequence only, because finding 2's fix has to cover both
files.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 the revert removed the two cases and left the comment block that introduces them, so the module's last words claim the sweep's reach is pinned when all three widenings revert green | `tests/test_a_release_is_sized_by_a_criterion.py:259-270` | open | **executed** — the three widenings mutated one at a time in a clone at `3673e46`, module green at 7 passed each, tree restored clean; module ends at 270 with its last function at `:258` |
| 2 | ⬜ a record names the reverted constant without the line's exemption marker, so `bin/evidence-check .` exits 2 and PR #364's `ledger` job fails | `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/rounds/round-3-fixes.md:49`, and `rounds/round-3-asked.md:47` at `9e37d7a`; the gate at `.github/workflows/test.yml:85-91` | open | **executed** — exit read directly: 2 at `3673e46` (1 refused), 2 at `9e37d7a` (2 refused); ledger arm 1145 ok · 0 drifted · 0 broken both times |
| 3 | ⬜ R1's `Verified behavior` says the sweep's reach *is pinned now* and that two cases were added; both are false at this tip, and the row's own `Notes` cell says so | `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`, row R1 | open | **executed** — the same three mutations; **read** — the two cells against each other, and `fold_ledger.py` moves the fragment into `seal/ledger.md` at the release |
| 4 | ⬜ five places say the four `survivors.md` rows are armed again when #365 lands; with #365's own drafted fix applied the check still reports nothing, because a second silencing path is open | `seal/specs/1789172128-…/survivors.md` header, `phases/phase-5.md`, `overview.md`'s `## Not verified`, `rounds/round-2-fixes.md`, and `seal/ledger/1789108681-…md` row S10 | open | **executed** — `corrected`'s `rounds/` filter applied in a clone: exit 0, no survivors, with and without `--exempt`; with `survivors.md` also out of the added side, exit 1, three exempted and two reported, `changelog.md:22` printed under `exempt` with its grounds |
| 5 | ⬜ two records say reverting `hits()`'s joined-line branch leaves the module green at 9 passed; it is 7, and one of the two carries no scope for the number | `seal/follow-up.md`, the `hits()` row; `seal/specs/1789172128-…/overview.md`'s `## Not verified` | open | **executed** — mutation 3 of the probe, green at 7 passed |
| 6 | ⬜ `**#366**.**This row replaces` renders as one word, the sentence boundary lost | `seal/ledger/1789172128-…md`, row R1, `Notes` | open | **read** — two adjacent bold runs with no separating space |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_release_is_sized_by_a_criterion.py -q`, in a clone at `3673e46` | exit 0 · 7 passed |
| probe · the three widenings mutated one at a time, module re-run after each, file restored | exit 0 · 7 passed each — the pattern's three noun alternatives, `CLAUDE.md` in `SCANNED`, and `hits()`'s joined-line branch all revert with the module green; `git status --porcelain` empty after |
| `bin/evidence-check .` at `3673e46` | **exit 2** · ledger arm 1145 ok · 0 drifted · 0 broken; records arm 1 DRIFTED at `spec.md:159` and **1 NOT-IN-TREE** at `rounds/round-3-fixes.md:49` |
| `bin/evidence-check .` at `9e37d7a` | **exit 2** · same ledger arm · **2 NOT-IN-TREE**, adding `rounds/round-3-asked.md:47` |
| `bin/survivor-check --range 7e17f5e..3673e46`, with and without `--exempt` | exit 0 each, identical *no removed wording is still standing* — the disclosure reproduces |
| probe · #365's drafted fix applied to `corrected` (the `rounds/` filter), then the range re-run | exit 0 · no survivors, with and without `--exempt` — the four rows are NOT re-armed by #365 alone |
| probe · that filter plus `seal/specs/*/survivors.md` out of the added side | exit 1 · without `--exempt` 5 places; with `--exempt` 3 exempted — `changelog.md:22` among them, printed with its grounds — and 2 still reported, both of them `survivors.md`'s own quote cells at `:24` and `:26` |
| read · `docs/issues-and-milestones.md:148-158` against `:208`, `:210-213` and `docs/branch-and-release.md:256-258` | the third attempt is true of both mechanisms |
| read · `tracked()` at `:138-150` | `os.path.basename(rel) != SELF` — the docstring's *by basename* claim holds |
| read · `.github/workflows/test.yml:85-91` | the `ledger` job `exit`s on any evidence-check code at or above 2, so finding 2 is red on the pull request |
| Broad gate — the full suite, the repository-wide lint, the typecheck | **not yet**, and not run here. It is the sealer's. It comes due when this record closes, after finding 2 is applied |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the version checker's off-by-one | **#363**, by Q1 | the repository owner. Already deferred; not re-opened here |
| `release: 0.11.1`'s milestone description | the tracker, by Q4 | the repository owner. Already deferred; not re-opened here |
| whether `size: now` is the spelling the owner creates | `overview.md`'s `## Not verified` | the repository owner, after this merges. Already deferred |
| pinning the sweep's reach, and a `Location` that spans two depths | **#366** | the repository owner. Already deferred by round 2's fix pass; finding 1 above is what the revert left behind, not a re-opening of it |
| `corrected`'s missing `rounds/` exclusion | **#365** | the repository owner. Already deferred and filed. What finding 4 adds is that #365 alone does not re-arm this work item's rows |
| leaving `seal/specs/*/survivors.md` out of the added side, and an exemption file that reports its own quote cells | `seal/follow-up.md` already carries the first half; the second half has no row | the repository owner. This run is capped, so finding 4's residue is a `deferred #N` candidate rather than a fix to commission |

## Paste-ready fixes

Finding 1 — `tests/test_a_release_is_sized_by_a_criterion.py`, replacing the
trailing comment block at `:259-270`:

```python
# --- the sweep's reach is NOT pinned, and that is the state it ships in ------

# **A sweep that answers *no offender* cannot pin its own reach.** No file in
# the tree carries the shapes round 1 measured escaping, so deleting the reach
# that finds them changes the sweep's answer not at all: round 2 measured each
# of round 1's three widenings -- the pattern's noun alternatives, `CLAUDE.md`
# in `SCANNED`, and `hits()`'s joined-line branch -- reverting with this module
# still green, and round 3 re-derived it at 7 passed.
#
# Two cases were written for it and reverted. `round_record.py close` refused
# them at depth 2, keying on the finding's `Location` rather than on what each
# case pins, and the gate's exit was taken rather than routed around. So the
# reach ships unpinned, deliberately: #366 carries the drafted cases, the
# measurement, and the question about a `Location` spanning two depths. Do not
# read a green run here as evidence that a widening is still needed.
```

Finding 2 — `rounds/round-3-fixes.md:49`, and `rounds/round-3-asked.md:47`
at `9e37d7a`. Append the exemption marker to each line that names the reverted
constant in prose, exactly as line 18 of the same file already does. The marker
is the four words the checker looks for, added at the end of the prose line:
`(NAME NOT IN TREE)`. It is not written inside a fence, because a fence is
already exempt and the marker would corrupt a paste-ready block.

Finding 3 — `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`,
row R1, replacing the sentence that begins *Round 2 found the sweep's own reach
unpinned*:

```markdown
**Round 2 found the sweep's own reach unpinned and it still is**: each of round 1's three widenings — the pattern's three noun alternatives, `CLAUDE.md` in `SCANNED`, and `hits()`'s joined-line branch — reverts with the module green, re-derived at 7 passed on 2026-09-12. Two cases were written for the first two and reverted when `round_record.py close` refused them at depth 2; a case for `hits()` is depth 2 by construction, since round 1's fix pass created it. So the reach is anchored here and pinned by nothing, which is **#366**, with a row in `seal/follow-up.md` for the `hits()` half.
```

Finding 5 — `seal/follow-up.md`'s `hits()` row and
`seal/specs/1789172128-…/overview.md`'s matching `## Not verified` row: replace
`green at 9 passed` with `green at 7 passed`, and in the memo row say the tip
the number is of.

Finding 6 — `seal/ledger/1789172128-…md`, row R1, `Notes`:

```markdown
which is **#366**. **This row replaces S3 of `seal/ledger/1789100139-…md`**,
```

Needs a fix: yes — finding 1. The module's trailing comment block claims the
sweep's reach is pinned by two cases that the revert removed, and all three
widenings revert with the module green. Findings 2 to 6 are corrections under
`seal/specs/`, `seal/ledger/` and `seal/follow-up.md` and do not count, though
finding 2 turns the pull request's `ledger` job red and has to be applied
before the sealer is spawned.

Loses a record or crashes: no.

## Proof block

Opened in a `git clone --no-local` of this repository at `3673e46`, and at
`9e37d7a` for finding 2's second location only:
`tests/test_a_release_is_sized_by_a_criterion.py`,
`docs/issues-and-milestones.md`, `docs/branch-and-release.md`,
`skills/code-review/scripts/survivor_check.py`,
`.github/workflows/test.yml`, `bin/test`, `seal/ledger.md`,
`seal/follow-up.md`,
`seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`,
`seal/ledger/1789108681-a-merged-ticket-looks-unstarted-until-the-release-ships.md`,
and under `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/`:
`overview.md`, `survivors.md`, `phases/phase-5.md`, `rounds/round-1.md`,
`rounds/round-2.md`, `rounds/round-2-report.md`, `rounds/round-2-fixes.md`,
`rounds/round-3-fixes.md`, `rounds/round-3-asked.md`.

Three `test_tmp_*` probe scripts were written outside the repository, run once,
and deleted; the clone is clean at `3673e46` and nothing was written in the
working checkout except this report.
