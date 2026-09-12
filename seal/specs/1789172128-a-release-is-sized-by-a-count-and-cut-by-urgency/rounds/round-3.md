# 1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency — review round 3

| Field | Value |
|---|---|
| Target SHA | 3673e46 |
| Ran by | specseal:warden on Opus 5 |
| PR | #364 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — finding 1. The module's trailing comment block claims the sweep's reach is pinned by two cases that the revert removed, and all three widenings revert with the module green. Findings 2 to 6 are corrections under `seal/specs/`, `seal/ledger/` and `seal/follow-up.md` and do not count, though finding 2 turns the pull request's `ledger` job red and has to be applied before the sealer is spawned. |
| Loses a record or crashes | no. |

- [x] Pass

## What this round was asked

# round 3 — the reopening's verifying round, and the last record of this run

| | |
|---|---|
| Target | the **diff of round 2's fixes**, `405fe9d..3673e46` — not the branch |
| Review at | `3673e46` |
| Base of the branch | `origin/release/v0.11.1` = `7e17f5e` |
| Draft pull request | #364 |
| Ran by | specseal:warden on Opus 5 |
| Previous record | `rounds/round-2.md`, closed — 5 fixed, 0 answered, 2 deferred |

## This is the last record, and it is decided before you start

Round 1 met the floor. Round 2 was its verifying round and reopened the run on
four findings, which is the **one** reopening the chain allows. So this record
ends the run whatever it finds: anything it opens becomes an issue with the
verdict `deferred #N`, this record's `Fixes checked by` reads `no fixes to
check`, and the pull request is labelled `chain: capped`.

That changes nothing about what you should report. Report what you find.

## The job

**The answers, not new findings** — for each of round 2's seven verdicts, is it
actually closed. `rounds/round-2.md` holds the verdict table,
`rounds/round-3-fixes.md` what the pass says it did, `rounds/round-2-report.md`
the reasoning behind the verdicts.

**`round-2.md`'s `New units` reads `none`**, derived from the fix range rather
than typed, so this round has **no finding surface** and every surface in the
diff is a verification surface.

## The one thing in this diff that is not an ordinary fix

**Round 2's finding 2 was fixed, then un-fixed, on the owner's answer.** The
sequence matters and the record carries it:

1. The pass added two cases and refused a third at depth 2. Each of the two was
   measured red under exactly its own mutation and the only failure.
2. `round_record.py close` refused **all three** at exit 2. `depth_two` keys on
   the **finding's `Location`**, and finding 2's named `hits()` — created by
   round 1's fixes — so every unit the range added in that file was refused,
   including two that pin `STATES_A_SIZE` and `SCANNED`, both created by build
   phase 4 and depth 1 by what they pin.
3. The repository owner's answer was to **take the gate's exit** rather than
   route around it (a non-`fixed` verdict skips the check) or widen it.
4. So the two cases and `NOUN_FORMS` were reverted (NAME NOT IN TREE), two now-dead coordinates
   left ledger row R1, and the work went to **#366**.

**What to judge here.** That the revert is clean and complete — the three
widenings the cases would have pinned are still in the tree and the module is
7 passed; that R1's claim is still true on the five coordinates that remain and
that removing two was the right treatment rather than re-pointing; and that
`rounds/round-3-fixes.md` states the cost rather than absorbing it. **What is
not yours to reopen is the owner's answer**, or whether `depth_two` should be
finer — that question is #366's.

## What else the fix pass says it did, to be checked rather than inherited

- **Finding 1, written once from three coordinates** rather than adjusted a
  third time. `docs/issues-and-milestones.md:150-158` now says `size: now` comes
  off when the release reaches `main` and the issue closes, and that
  `merged: X.Y.Z` goes on earlier **inside that same release** at the squash.
  This clause was wrong in the build and wrong again in round 1's fix, so read
  it against `:208`, `:210-211` and `docs/branch-and-release.md:256-258` and say
  whether it is finally true of both mechanisms.
- **Finding 3's disclosure.** Every `survivor-check exit 0` this work item
  recorded as *every survivor excused* excused nothing — the check exits 0 with
  **and without** `--exempt`, the identical line. Corrected in `overview.md`,
  `phases/phase-5.md`, `rounds/round-2-fixes.md` and `survivors.md`'s header,
  with the four rows kept because they become correct when **#365** lands. One
  sentence of *another* work item's ledger row, `seal/ledger/1789108681-…md`'s
  S10, was qualified without touching its claim. Judge that reach.
- **Finding 4** — `:31-32` now says the self-exclusion is *by basename rather
  than by path*, and R1 was corrected with it.

## Executed by the orchestrating session at `3673e46`

Exit codes read directly, no pipe. Re-derive rather than inherit:

- Eight modules one per call — the module **7**, wrap 23, release-hygiene 32,
  one-word-one-meaning 13, no-real-identifiers 2, row-points-by-content 102,
  record-states-the-tree 58, rider-reaches-its-file 29 → **exit 0 each**.
- `uvx ruff check` and `uvx ruff format --check` on the module → **exit 0** each,
  after a reformat the revert made necessary.
- Both reverted cases mutated before the revert: each red for its own mutation
  and no other; module restored green, tree clean.
- `bin/evidence-check .` → **exit 1**; ledger arm **1145 ok · 0 drifted · 0
  broken**, records arm one drift at `spec.md:159` which round 1 decided stays.
  It read **exit 2 with 2 broken** before R1's dead coordinates came out, and
  the records arm refused `round-3-fixes.md` until finding 2's row stopped
  naming units the tree no longer has.
- `bin/survivor-check --range 7e17f5e..HEAD` with and without `--exempt` →
  exit 0, identical output. **That is finding 3, not evidence.**

## Settled, and not yours to reopen

The four owner answers — Q1 (c), and **a finding proposing an edit to
`tests/test_release_hygiene.py` is out of scope**; Q2 (b); Q3 (a), **no tracker
write of any kind**; Q4 (a). Round 1's two judgments. `hits()`'s one-boundary
assumption, answered with grounds. And the owner's answer on the depth refusal.

## Still unverified

**The broad gate is the `sealer`'s. Do not run it.** No `bin/broad-gate`, no
whole-suite run, no repository-wide `ruff`. It comes due when this record closes.

## The two lines the run ends on

- `Needs a fix: no`, or `yes` and what does. A 🟡 answered with grounds is `no`;
  a finding under `seal/specs/` is a correction and does not count.
- `Loses a record or crashes: no`, or `yes` and what does.

## Where the report goes

`rounds/round-3-report.md`, in the working tree, uncommitted. Do not commit it
and do not touch the tracker.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 the revert removed the two cases and left the comment block that introduces them, so the module's last words claim the sweep's reach is pinned when all three widenings revert green | `tests/test_a_release_is_sized_by_a_criterion.py:259-270` | answered | **Corrected at `01a0437`, and `answered` rather than `fixed` deliberately.** Two reasons, and the first is the substantive one: this was **my own revert left unfinished**, not a defect a fix pass was commissioned for. The owner's answer on round 2's finding 2 was to take the depth gate's exit; I reverted the two cases and `NOUN_FORMS` and left the comment block that introduced them, so the module's last word was *the two cases below are what stands between the reach and a later edit* with nothing below — the module asserting exactly what round 2's finding 2 had disproved. Completing an ordered revert is the same act finished, not a new one. The second reason is mechanical and would not on its own justify the word: `landing_values` keeps `Fixes checked by` at `nobody` if any verdict is a fix word, and `nobody` beside a ticked `Pass` on a run's last record fails the pull request. The block now states the truth — the three widenings ship unpinned, a later edit trimming any of them as unused is caught by nothing here, and **#366** holds the drafted cases and the measurement. Module 7 passed, `uvx ruff check` and `uvx ruff format --check` exit 0 |  <!-- NAME NOT IN TREE -->
| 2 | ⬜ a record names the reverted constant without the line's exemption marker, so `bin/evidence-check .` exits 2 and PR #364's `ledger` job fails | `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/rounds/round-3-fixes.md:49`, and `rounds/round-3-asked.md:47` at `9e37d7a`; the gate at `.github/workflows/test.yml:85-91` | answered | **`bin/evidence-check .` was exit 2, and this session had reported exit 1.** Corrected at `01a0437`; located in this work item's own records, so a correction. The cause was mine and is worth the sentence: two later edits of mine — the units paragraph in `rounds/round-3-fixes.md` and round 3's own paragraph — named the reverted `NOUN_FORMS` in prose with no marker, **after** my last check had passed. Verified, then edited, then reported the stale reading, which is the shape the repository's own rule about a spent gate describes. Both lines now carry `NAME NOT IN TREE`, a marker `round-3-fixes.md:18` already carried twice, so the convention was known and the omission was not ignorance. The records arm now reads **0 refused**; `evidence-check` exits 1 on the single drift round 1 decided stays, which `.github/workflows/test.yml:85-91` treats as a warning. **Round 3 was right that this had to be applied before the sealer** — a broad run taken over a tree whose `ledger` job is red is a run that was spent rather than banked |
| 3 | ⬜ R1's `Verified behavior` says the sweep's reach *is pinned now* and that two cases were added; both are false at this tip, and the row's own `Notes` cell says so | `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`, row R1 | answered | Ledger row **R1 contradicted itself** at `01a0437`: `Verified behavior` said the sweep's reach *is pinned now* and `Notes` said the pinning went to #366. The cell now says the reach is still unpinned, that two cases were added, measured red under exactly their own mutation, and then reverted on the owner's answer, and that the pinning is #366. Round 3 counted this as the **third** time this row has carried a sentence the tree contradicts, which is the fact worth carrying rather than the correction |
| 4 | ⬜ five places say the four `survivors.md` rows are armed again when #365 lands; with #365's own drafted fix applied the check still reports nothing, because a second silencing path is open | `seal/specs/1789172128-…/survivors.md` header, `phases/phase-5.md`, `overview.md`'s `## Not verified`, `rounds/round-2-fixes.md`, and `seal/ledger/1789108681-…md` row S10 | answered | **The claim that #365 rearms the exemptions was a prediction, and round 3 measured it false.** It applied #365's own drafted fix — the `rounds/` filter in `corrected` — and the four `survivors.md` rows still came back unused, because `seal/specs/*/survivors.md` has to be excluded on the ADDED side too, a second silencing path `seal/follow-up.md` already holds as its own row. So the rows need **two** changes, not one. Corrected at `01a0437` in all four places that stated it as fact: `phases/phase-5.md`, `overview.md`, `rounds/round-2-fixes.md`, and `seal/ledger/1789108681-…md`'s S10 — the last being a row in **another** work item's fragment, touched to leave it true rather than to change its claim, which rests on a grep and is unaffected. The same measurement closed round 2's finding 5 positively: with both paths shut, `changelog.md:22` prints under `exempt` with its grounds, so the re-anchored quotation works |
| 5 | ⬜ two records say reverting `hits()`'s joined-line branch leaves the module green at 9 passed; it is 7, and one of the two carries no scope for the number | `seal/follow-up.md`, the `hits()` row; `seal/specs/1789172128-…/overview.md`'s `## Not verified` | answered | Two records said the module is **9 passed**; it is 7 after the revert. Corrected at `01a0437` in `seal/follow-up.md` and `overview.md` |
| 6 | ⬜ `**#366**.**This row replaces` renders as one word, the sentence boundary lost | `seal/ledger/1789172128-…md`, row R1, `Notes` | answered | `**#366**.**This row replaces` rendered as one word for want of a space. Corrected at `01a0437` |

## Paste-ready fixes

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
```markdown
**Round 2 found the sweep's own reach unpinned and it still is**: each of round 1's three widenings — the pattern's three noun alternatives, `CLAUDE.md` in `SCANNED`, and `hits()`'s joined-line branch — reverts with the module green, re-derived at 7 passed on 2026-09-12. Two cases were written for the first two and reverted when `round_record.py close` refused them at depth 2; a case for `hits()` is depth 2 by construction, since round 1's fix pass created it. So the reach is anchored here and pinned by nothing, which is **#366**, with a row in `seal/follow-up.md` for the `hits()` half.
```
```markdown
which is **#366**. **This row replaces S3 of `seal/ledger/1789100139-…md`**,
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `docs/issues-and-milestones.md:147-148`, against `:201` and `:209-210` and `docs/branch-and-release.md:257-258` | round 1's 1 — fixed |
| round-1 | `tests/test_a_release_is_sized_by_a_criterion.py:184-193`, docstring at `:13` | round 1's 2 — fixed |
| round-1 | `tests/test_a_release_is_sized_by_a_criterion.py:63-67` | round 1's 3 — fixed |
| round-1 | `docs/issues-and-milestones.md:135-139`, against `:77` and `:129-131` | round 1's 4 — fixed |
| round-1 | `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md`, row R1 | round 1's 5 — fixed |
| round-1 | `seal/specs/.../phases/phase-4.md`, `seal/specs/.../questions.md` Q8 | round 1's 6 — fixed |
| round-1 | `seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md:22` | round 1's 7 — fixed |
| round-1 | `seal/specs/.../spec.md:159` | round 1's 8 — answered |
| round-1 | `tests/test_a_release_is_sized_by_a_criterion.py:47-56` | round 1's 9 — fixed |
| round-2 | `docs/issues-and-milestones.md:152-155`, against `:208` and `:210-211` and `docs/branch-and-release.md:256-258` | round 2's 1 — fixed |
| round-2 | `tests/test_a_release_is_sized_by_a_criterion.py`, the pattern at `:90-97`, `hits()` at `:117-134`, `SCANNED` at `:55-68` | round 2's 2 — deferred |
| round-2 | `skills/code-review/scripts/survivor_check.py`, `corrected` — the `paths` list built from `diff --name-only`; docstring at `:65` and `:70-79` | round 2's 3 — deferred |
| round-2 | `tests/test_a_release_is_sized_by_a_criterion.py:31`, against `:146`; and `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md` row R1 | round 2's 4 — fixed |
| round-2 | `seal/specs/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency/survivors.md`, and `rounds/round-1.md`'s probe row | round 2's 5 — fixed |
| round-2 | `seal/ledger/1789172128-a-release-is-sized-by-a-count-and-cut-by-urgency.md` row R1, `Code grounds` | round 2's 6 — fixed |
| round-2 | `tests/test_a_release_is_sized_by_a_criterion.py:117-134` | round 2's 7 — answered |
| round-2 | `docs/issues-and-milestones.md:141`, `:152` | round 2's 8 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the version checker's off-by-one | **#363**, by Q1 | the repository owner. Already deferred; not re-opened here |
| `release: 0.11.1`'s milestone description | the tracker, by Q4 | the repository owner. Already deferred; not re-opened here |
| whether `size: now` is the spelling the owner creates | `overview.md`'s `## Not verified` | the repository owner, after this merges. Already deferred |
| pinning the sweep's reach, and a `Location` that spans two depths | **#366** | the repository owner. Already deferred by round 2's fix pass; finding 1 above is what the revert left behind, not a re-opening of it |
| `corrected`'s missing `rounds/` exclusion | **#365** | the repository owner. Already deferred and filed. What finding 4 adds is that #365 alone does not re-arm this work item's rows |
| leaving `seal/specs/*/survivors.md` out of the added side, and an exemption file that reports its own quote cells | `seal/follow-up.md` already carries the first half; the second half has no row | the repository owner. This run is capped, so finding 4's residue is a `deferred #N` candidate rather than a fix to commission |
