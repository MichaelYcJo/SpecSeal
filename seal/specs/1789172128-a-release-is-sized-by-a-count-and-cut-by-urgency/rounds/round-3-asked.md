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
