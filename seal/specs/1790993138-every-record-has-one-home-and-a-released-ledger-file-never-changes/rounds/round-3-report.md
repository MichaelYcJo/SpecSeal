# Round 3 report — #715, every record has one home and a released ledger file never changes

Ran by: `specseal:warden on claude-opus-5-5`.
Target: `089a5c77` on `feat/715-every-record-has-one-home-and-a-released-ledger-file-never-changes`, PR #736.
Fix range `4f0aacc8..c9fe12fd`, 8 commits, then round 2's close commit `089a5c77`.
A verifying round, and the run's last: its target is the fix diff, not the
branch. Probes ran in a `git clone --no-local` of the worktree at `089a5c77`,
in this round's scratch directory. The worktree's HEAD was never moved, and
nothing in it was written except this file. One read-side act touched the
worktree's repository: `git fetch origin`, which moved remote-tracking refs
only.

## Summary

All six round 2 findings are closed at their commits, and each of the five
cases the fix pass planted was seen red against `4f0aacc8`'s
`evidence_check.py`, each on its own assertion (executed).

The pipe-led rule `literal_statements` gained moves nothing in this tree
(executed). That holds for the 77 anchors that carry a minor claim, for the
`citation_for` output of all 1,146 anchored ledger rows, and for every call
a whole `--strict` run makes.

One new 🟡, in the code and sentences round 2's fix pass wrote for 🟡 12:

- **🟡 16.** A narrowed `--reverify` answers only for families whose *root*
  sits in a file it read. Narrowed to a released file that holds a folded
  `Re-read ·` member, it writes nothing and exits 0, with and without the
  freeze. `--strict` narrowed to the same file reports that member DRIFTED.
  The home and ledger row L4 both say the run names such a row.

One ⬜: a row whose `Checked` cell holds `2026-13-45` is described as
"the reading of no date" (⬜ 17).

The endgame re-runs to the same numbers as round 2:

- the three siblings merge with 0 conflicts;
- the second lander re-stamps 8 hashes on 7 rows;
- after the fold, all four fragments sit in `seal/releases/0.18.0.md`, and
  `--strict` reads 3,996 ok, 0 drifted, exit 0.

## Stage 1 — each round 2 fix at its commit

The fix pass's account (`round-2.md`'s verdicts, the commit messages, the
`survivors.md` rows) was read and checked against the code. Each line below
says what the code does.

- **🟡 10, `c5829e6e`.** Every carrier now says coordinates are judged one
  at a time, and none promises that an unread pair is never accepted:
  - the home, `docs/the-evidence-ledger.md:111-117`;
  - the changelog entry, `changelog.md:15-24`;
  - the comment above `CITING_VERBS`;
  - the comment in the emission loop of `family_view`;
  - spec D3 and `plan.md`.

  The changelog also gains the double-correction sentence. The three
  `survivors.md` rows quote sentences that are true of the rule (read). The
  text-reading modules over those files pass: survivors, docs line wrap, one
  word one meaning, no real identifiers, 214 cases (executed).
- **🟡 11, `9abe7a00`.** `corrected_by`'s lists drop every key in
  `superseded`. `root_of` stops at a row whose verb is not `Re-read`, so a
  third `Corrected ·` row citing C2 is filed under C2 rather than under R.
  The filter then leaves R with C1 alone, and the notice goes (read).
  `test_a_folded_double_correction_is_cleared_by_retiring_one` is red at
  `4f0aacc8`, `assert 2 == 0`, and green at HEAD (executed).
- **🟡 12, `a2c03e94`.** `released_drift` now owes a re-read for the first
  released member of a family whose coordinate holds no newest reading,
  whether that member grades DRIFTED or is OK and outranked. A new branch in
  `main` makes a no-freeze `--reverify` print `LEFT` for each owed row and
  exit 1. Both cases are red at `4f0aacc8` and green at HEAD (executed):
  - the freeze case,
    `test_a_narrowed_into_re_reads_a_family_a_fragment_outranks`, fails on
    `0 citing rows written`;
  - the no-freeze case,
    `test_an_unfrozen_narrowed_reverify_names_a_family_it_could_not_clear`,
    fails on `assert 0 == 1`.

  Closed for a narrowing to the file that holds the family's root. A
  narrowing to a released file that holds another member is 🟡 16.
- **⬜ 13, `e2a808b7`.** `calendar_date` keeps only dates
  `datetime.date.fromisoformat` accepts, so a date the calendar does not have
  reads as `""`, the oldest. Its case is red at `4f0aacc8`, `assert 2 == 0`,
  and green at HEAD (executed). How the message then names that row is ⬜ 17.
- **⬜ 14, `ba837122`.** The fix went further than round 2's paste, which
  changed only the comment. `literal_statements` now keeps, among several
  hits of a literal that opens with `| `, the one line that begins with it.
  It is the one resolver behind `cited_row`, `minor_region` and
  `--reverify`, so the citation writer and its readers still agree (read).
  The case is red at `4f0aacc8`, `assert None is not None`, and green at
  HEAD (executed). The tree probe is below, under *Stage 2*.
- **⬜ 15, `43354f87`.** S1 in the test module's docstring states the
  newest-reading rule with ties (read).

The ledger, read: `22ff64ec` rewrites L1, L3 and L4 and re-stamps the rows
whose `main` and `family_view` hashes moved.

- L1 and L3 state what the code does.
- L4's added clause about a narrowed `--ledger` run is false in the case
  🟡 16 measures.

`--strict` at HEAD reads 3,791 ok, 0 drifted, exit 0 (executed).

Round 1's nine findings were confirmed by round 2 and are carried, not
re-derived. The exception is where round 2's fixes touched them: round 1's
🟡 4 through 🟡 11, round 1's ⬜ 9 through ⬜ 14, and round 1's 🟡 2 through
🟡 10's sentences. Each of those is answered above.

## Stage 2 — the units the pass created

### The pipe-led literal moves no citation, no M2 row and no minor anchor

Executed: a probe ran the old and the new `literal_statements` side by side
over the tree at HEAD.

| Read | Count | Where the two rules disagree |
|---|---|---|
| anchors in tracked text files | 4,487 | — |
| anchors carrying a minor claim | 77, 1 of them pipe-led | `classify` differs on 0 |
| anchored ledger rows given to `citation_for` | 1,146 | output differs on 0 |
| `literal_statements` calls in a whole `--strict` run, `cited_row` included | every call | 0 calls disagree |

The `--strict` run under the probe read 3,791 ok, 0 drifted, exit 0.

`correction_check.py` keys a `Corrected ·` row by the citation text, not by
resolving it, so the new rule cannot split the two checkers (read,
`corrections`).

One property, read: the rule changes an answer only where the old rule had
two or more hits. The old rule widened that case to the unit and said
DRIFTED. A minor anchor stamped while ambiguous would therefore read
differently now. The tree has none, as the 0 above shows.

### 🟡 16 — a narrowed `--reverify` answers only for families rooted in a file it read

Coordinates:

- the filter in `released_drift`, `skills/evidence-check/scripts/evidence_check.py:3214-3216`:
  `if top[0] not in wanted: continue`;
- its docstring, `skills/evidence-check/scripts/evidence_check.py:3184-3192`;
- the home, `docs/the-evidence-ledger.md:157-160`;
- ledger row L4,
  `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md:4`.

The family below is executed, with code at h1:

- R sits in `seal/releases/0.1.0.md`: h1, dated 2026-01-01.
- C is a folded `Re-read ·` of R in `seal/releases/0.2.0.md`: h1, dated
  2026-02-01.
- F is a fragment `Re-read ·` of R: h2, dated 2026-03-01.

| Run | Exit | What it says |
|---|---|---|
| `--strict .` | 2 | 3 drifted: F, R and C. C reads "matches only the reading of 2026-02-01; the newest reading … holds other content" |
| `--strict --ledger seal/releases/0.2.0.md .` | 2 | C DRIFTED, in the file it read |
| under the freeze, `--reverify --into … --checked 2026-04-01 --ledger seal/releases/0.2.0.md .` | 0 | `0 citing rows written · 0 released rows left`; `--strict` still exits 2 |
| without the freeze, `--reverify --ledger seal/releases/0.2.0.md .` | 0 | no `LEFT` line; `--strict` still exits 2 |
| without the freeze, `--reverify --ledger seal/releases/0.1.0.md .` | 1 | `LEFT seal/releases/0.1.0.md:5 … still DRIFTED`: the root's file works |

`released_drift` builds `wanted` from the released files in LEDGERS. It then
skips every family whose root is not in that set, so C was read and its
family is never asked about.

Why it matters:

- **It is round 2's 🟡 12 one file over.** A narrowed `--reverify` names
  nothing owed, exits 0, and the same narrowing under `--strict` reads the
  family DRIFTED.
- **The case is common after a fold.** The fold moves `Re-read ·` rows into
  release files. A person who re-read the rows of `seal/releases/0.18.0.md`
  and narrows the write to that file, as the home tells them to, is in this
  case.
- **Two sentences the fix pass wrote state the opposite.** The home says the
  run "names each released row it read whose family's newest reading sits in
  a file it did not write". L4 says the same, and adds that under the freeze
  "a narrowed `--into` writes the re-read an outranked released reading
  owes". C is such a row in both.

With the fix below, applied in the clone:

- the freeze run prints `1 citing row written`, and `--strict` exits 0;
- the no-freeze run prints the `LEFT` line for the family's root;
- the four ledger modules pass, 146 cases.

Unnarrowed runs do not change. There every released file is in `wanted`, so
every family's root already is.

The docstring is stale for a second reason. It still says a family is owed
where "a released member's reading drifted", and since `a2c03e94` an
outranked OK reading counts too. The fix below rewrites it.

### The smith's reading of 🟡 12: where it holds and where it does not

The question was whether "never exits 0 while `--strict` still reads the
family DRIFTED" may be narrowed to families with a member in a file the run
read.

**Narrowing to a file that holds no member is coherent.** Executed: with
`--ledger seal/ledger/<an unrelated fragment>.md`, `--reverify` exits 0
with and without the freeze. The narrowing notice names
`seal/releases/0.1.0.md`, the fragment and `0.2.0.md` as not read. The
same narrowing under `--strict` also exits 0, with 0 drifted reported,
because a narrowing chooses what is reported (`main`, the comment above
`ledger_families`). So the property holds once it is stated per
narrowing: a narrowed `--reverify` never exits 0 while a narrowed
`--strict` over the same files reads a row DRIFTED. A run that read
nothing in the family says nothing about it. It names the files it skipped,
exactly as `--strict --ledger` and the pre-existing `--reverify --ledger`
do.

**What the smith built is narrower than that reading.** The code keys on the
root's file, not on any member's file, so it fails the smith's own
statement in the 🟡 16 case. That is the real hole. The reading is right;
the build stops one step short of it.

### The units checked and found to hold

- **The superseded filter in `corrected_by`.** A retiring row must be a
  `Corrected ·` whose citation resolves. A `Re-read ·` row citing C2 joins
  C2's family and retires nothing. A correction whose citation does not
  resolve has no parent, so it retires nothing (read).
- **`released_drift` counting an outranked released reading.** It reaches
  that line only where `view.held` is empty, and that is exactly where
  `family_view` emits DRIFTED. BROKEN is a property of the coordinate's major
  anchor, the same for every reading, so breaking at the first released
  member loses nothing (read).
- **`calendar_date`.** `CHECKED_RE` already restricts the shape, and
  `fromisoformat` refuses `2026-02-30` and `2026-13-45`. If every reading
  of a coordinate is undated or invalid, they tie as `""`, which is the old
  union (read).
- **The no-freeze branch, run without narrowing.** Executed on the 🟡 16
  family with `--checked`: exit 0, no `LEFT`, `--strict` 5 ok, 0 drifted.

### ⬜ 17 — an invalid `Checked` date is named "no date"

`skills/evidence-check/scripts/evidence_check.py:2488` (`family_view`, the
emission loop).

Executed: R dated `2026-13-45`, a fragment re-read dated 2026-02-01, and
the code reverted to R's hash. `--strict` reads "matches only the reading of
no date; the newest reading … 2026-02-01". The row carries a date. It is
one the calendar does not have, and the line should say that, because the
person's repair is to fix the typo. The verdict is right, so this is ⬜.

## The release endgame, re-run

Executed. The siblings were fetched from the worktree's remote-tracking refs
(#735 at `5c193b42`, #731 at `32f4caef`, #733 at `c198bce0`, each based on
`233f0455`). Each was merged into `089a5c77` with git's own merge.
`correction-check` ran with `--range 233f0455...HEAD`.

| Merged | Conflicts | `--strict` | Records arm | `correction-check` |
|---|---|---|---|---|
| #735 (#647) | 0 | 3,878 ok, 6 drifted, exit 2 | 4 refused | exit 0, read under the old rule (1790993137, 1790993138) |
| #731 (#718) | 0 | 3,878 ok, 3 drifted, exit 2 | 0 refused | exit 0, read under the old rule (1790993138, 1790993139) |
| #733 (#716) | 0 | 3,813 ok, 0 drifted, exit 0 | 0 refused | exit 0, read under the old rule (1790993138, 1790993140) |
| all three | 0 | 3,987 ok, 9 drifted, exit 2 | 4 refused | exit 0, all four ids below the cutoff 1790993141 |

On the all-three merge, the ledger and pact modules pass, 458 cases. They
are the four ledger modules, `test_evidence_check.py`, the three pact
modules, the GFM line-reader module and the one-home module (executed).

**The second lander's re-stamp.** The command was `--reverify --into
seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md
--checked 2026-10-03 .` on the all-three merge. It exited 0 with `8 rows
re-verified`, `0 citing rows written · 0 released rows left`, and dated 7
rows. The exact rows, each hash old → new:

| Fragment row | Coordinate | Hash |
|---|---|---|
| 1790993138:12, `Re-read · P2-1 · The checker, …` | citation into `seal/releases/0.15.3.md`, "P2-1 · The checker," | `795c63e3` → `795d127a` |
| 1790993138:18, `Re-read · H1 · every split …` | citation into `seal/releases/0.16.0.md`, "H1 · every split" | `c7650aa1` → `098baf93` |
| 1790993138:29, `Re-read · S8 · templates/config.md …` | citation into `seal/releases/0.5.0.md`, "S8 ·" | `58bed345` → `564aa3ba` |
| 1790993138:29, the same row | `templates/config.md#"# Repository config"` | `ea2dbeae` → `9b19d671` |
| 1790993138:30, `Re-read · Every place a ledger path …` | citation into `seal/releases/0.8.3.md`, "Every place a ledger" | `e22ad330` → `0a90be02` |
| 1790993138:45, `Re-read · P3 · no loaded document …` | citation into `seal/releases/0.15.1.md`, "P3 · no loaded document" | `c9b35739` → `d6e6b23a` |
| 1790993138:60, `Re-read · P1c · the two documents …` | citation into `seal/releases/0.15.0.md`, "P1c · the two documents" | `b2c32774` → `776971f4` |
| 1790993139:23, `W4 · docs/branch-and-release.md's release-tail bullet …` | `docs/branch-and-release.md#"## Cutting a release"` | `6a2d58f1` → `c29d15f1` |

The ninth drifted finding is released S8 in `seal/releases/0.5.0.md`, on
`templates/config.md`. It is in row 29's family and clears with row 29.

Six of the eight hashes are citations. #647 is cut below the cutoff, so it
edits those released rows in place, legally. Each citation is a row a
person re-reads before the re-stamp is committed, which is what `--checked`
says (unverified: whether each cited row's claim still holds after #647's
edit; the second lander answers it).

**The final ledger state.**

| After | `--strict` | Records arm |
|---|---|---|
| the re-stamp | 3,996 ok, 0 drifted; exit 2 | 4 work items read, 4 refused |
| `fold_ledger.py --version 0.18.0`, staged | 3,996 ok, 0 drifted; exit 0 | 0 work items read, 51 unread, 0 refused |

The fold moved four fragments into a new `seal/releases/0.18.0.md` under
`## 0.18.0 — 2026-10-03`, one `###` section per work item (1790993137,
1790993138, 1790993139, 1790993140), and removed each fragment.
`fold_ledger.py --check` then exits 0.

**The records-arm refusal.** #735's records name
`fold_ledger.py#SELF_ANCHOR_RE` (NAME NOT IN TREE) at four lines:

- `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/phases/phase-3.md:36` and `:43`;
- `seal/specs/1790993137-a-signatory-declares-its-pact-and-pact-check-reads-it/rounds/round-1-report.md:24` and `:27`.

This branch removed that unit at `63d75120`, together with `--split`. #647's
code does not use it: in #647's tree the name sits only in
`fold_ledger.py` and those records. The consequences:

- `--strict` exits 2 on any tree that carries both branches before the fold,
  even with the ledger at 0 drifted;
- after the fold the arm reads no work item, so the refusal is gone;
- whichever sealer runs between the second landing and the release
  preparation meets it.

The cheapest repair sits with #647: write `NAME NOT IN TREE` on those four
lines in its own records. If #715 lands first, #647 does it on its own
branch. If #647 lands first, #715's second-lander commit has to edit
another work item's records instead. This is not a defect of this branch's
code (§*Deferred*).

## Regression tests to plant

```text
tests/test_a_released_row_is_read_again_in_a_fragment.py
  1. a narrowed --reverify --into answers for a family whose folded member   (🟡 16)
     sits in the file it read, though its root does not
  2. the same family without the freeze: the narrowed --reverify exits 1     (🟡 16)
     naming the family's root
```

Case 1 was seen red at `089a5c77` by the probe in §*Executed probes*
(`0 citing rows written`, exit 0), and green with the fix in the clone.

## Facts for the evidence ledger

- The pipe-led rule in `literal_statements` moves no anchor in this tree: 77
  claim anchors, 1,146 citations, 0 disagreeing calls in a whole `--strict`
  run (executed, at `089a5c77`).
- The second lander re-stamps the same 8 hashes on 7 rows as round 2 counted.
  6 rows are in this work item's fragment and 1 is #718's row 23. After the
  fold, the ledger reads 3,996 ok, 0 drifted (executed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 2's finding 10 is closed — every carrier says coordinates are judged one at a time and none promises an unread pair is never accepted | `docs/the-evidence-ledger.md:111` | confirmed | closed at `c5829e6e`; read: the home, the changelog, both comments, D3, `plan.md`; executed: the four text-reading modules, 214 passed |
| 🟢 | round 2's finding 11 is closed — a third `Corrected ·` row retiring one of two folded corrections clears the notice | `skills/evidence-check/scripts/evidence_check.py:2419` | confirmed | closed at `9abe7a00`; executed: its case red at `4f0aacc8`, green at HEAD; read: `root_of` files the retiring row under C2 |
| 🟢 | round 2's finding 12 is closed for a narrowing to the family root's file | `skills/evidence-check/scripts/evidence_check.py:3230` | confirmed | closed at `a2c03e94`; executed: both cases red at `4f0aacc8`, green at HEAD; a narrowing to a file holding another member is new finding 16 |
| 🟢 | round 2's finding 13 is closed — a date the calendar does not have orders nothing | `skills/evidence-check/scripts/evidence_check.py:2756` | confirmed | closed at `e2a808b7`; executed: its case red at `4f0aacc8`, green at HEAD; the message is new finding 17 |
| 🟢 | round 2's finding 14 is closed — a first cell equal to another row's cell gets a citation | `skills/evidence-check/scripts/evidence_check.py:797` | confirmed | closed at `ba837122`, as a behaviour change rather than round 2's comment; executed: its case red at `4f0aacc8`; the old and new rules disagree on 0 calls over the tree |
| 🟢 | round 2's finding 15 is closed — S1 states the newest-reading rule | `tests/test_a_released_row_is_read_again_in_a_fragment.py:16` | confirmed | closed at `43354f87`; read |
| carried | round 1's nine findings are closed, as round 2 confirmed them | `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/rounds/round-2.md:32` | confirmed | carried from round 2, not re-derived; the three that round 2's fixes touched (round 1's 2, 4 and 9) are answered by the rows above |
| 🟡 16 | a narrowed `--reverify` answers only for families whose root sits in a file it read; narrowed to a release file holding a folded member, it writes nothing and exits 0 while `--strict` over the same file reads that member DRIFTED, and the home and L4 say it names that row | `skills/evidence-check/scripts/evidence_check.py:3215`, `docs/the-evidence-ledger.md:157`, `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md:4` | open | executed: freeze `--into` 0 written, exit 0; no freeze exit 0, no `LEFT`; narrowed `--strict` exit 2; with the fix, 1 written and `--strict` exit 0; in code and sentences round 2's fix pass wrote, so the branch's to fix |
| ⬜ 17 | a `Checked` cell holding a date the calendar does not have is named "the reading of no date" | `skills/evidence-check/scripts/evidence_check.py:2488` | open | executed: R dated `2026-13-45` reads "matches only the reading of no date" |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the four ledger modules, `test_evidence_check.py`, the narrowing module and the one-home module at HEAD | 251 passed |
| the five cases round 2's fix pass planted, with `evidence_check.py` at `4f0aacc8` | 5 failed, each on its own assertion |
| old against new `literal_statements` over the tree at HEAD: `classify` on 77 claim anchors, `citation_for` on 1,146 rows, a whole `--strict` run | 0 differences, 0 disagreeing calls; strict 3,791 ok, 0 drifted, exit 0 |
| `bin/test` on the survivors, docs line-wrap, one-word and no-real-identifiers modules at HEAD | 214 passed |
| 🟡 16 family (R in 0.1.0, folded C in 0.2.0, fragment F newest, code reverted): `--strict` | exit 2, 3 drifted |
| the same, `--strict --ledger seal/releases/0.2.0.md` | exit 2, C DRIFTED |
| the same, under the freeze: `--reverify --into … --checked 2026-04-01 --ledger seal/releases/0.2.0.md` | exit 0, `0 citing rows written · 0 released rows left`; strict exit 2 after |
| the same, without the freeze: `--reverify --ledger seal/releases/0.2.0.md` | exit 0, no `LEFT`; strict exit 2 after |
| the same, without the freeze: `--reverify --ledger seal/releases/0.1.0.md` | exit 1, `LEFT seal/releases/0.1.0.md:5` |
| the same, narrowed to an unrelated fragment: `--strict`, then `--reverify` with and without the freeze | strict exit 0; reverify exit 0 both, with the narrowing notice naming the three unread ledgers |
| the same, without the freeze, unnarrowed: `--reverify --checked 2026-04-01` | exit 0, no `LEFT`; strict 5 ok, 0 drifted |
| the 🟡 16 fix applied in the clone: the two member-file runs, then the four ledger modules | freeze: 1 written, strict exit 0; no freeze: `LEFT` for the root; 146 passed |
| ⬜ 17: R dated `2026-13-45`, a newer fragment re-read, code reverted | "matches only the reading of no date" |
| sibling merges (#735, #731, #733, all three) into `089a5c77`, then `--strict` and `correction-check --range 233f0455...HEAD` | 0 conflicts; drifted 6, 3, 0, 9; records arm 4, 0, 0, 4 refused; correction-check exit 0 each |
| `bin/test` on the ledger, pact, GFM line-reader and one-home modules over the all-three merge | 458 passed |
| the second lander's re-stamp on the all-three merge: `--reverify --into <this fragment> --checked 2026-10-03` | exit 0; 8 hashes on 7 rows; 0 written, 0 left; strict 3,996 ok, 0 drifted, exit 2 (records arm 4 refused) |
| `fold_ledger.py --version 0.18.0` after the re-stamp, staged, then `--strict` and `fold_ledger.py --check` | 4 fragments folded into `seal/releases/0.18.0.md`; strict 3,996 ok, 0 drifted, exit 0, 0 refused; check exit 0 |
| the broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, once the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the second lander re-stamps 8 hashes on 7 rows (6 rows of this fragment, #718's row 23), and #735's four records lines naming a unit this branch removed refuse the records arm until the fold | the handoff to whichever of #647, #718 and #715 lands second; already deferred in round 2 | the orchestrator of the 0.18.0 run |

## Paste-ready fixes

### 🟡 16

```python
# skills/evidence-check/scripts/evidence_check.py, released_drift's docstring
    """`(view, drifted, broken)` for the released files among LEDGERS.

    DRIFTED is `{row: {coordinate: match}}`, one entry per row a re-read
    owes: a released row outside every family with a drifted coordinate, and
    the root of each family that is not superseded, has a released member in
    LEDGERS, and has a coordinate none of whose newest readings holds the
    current content, where a released member's reading is drifted or is
    outranked by that newer reading. BROKEN is `[(where, coordinate,
    detail)]` for the released coordinates a re-read cannot clear, which
    take a `Corrected ·` row instead.
    """
```

```python
# skills/evidence-check/scripts/evidence_check.py, released_drift
    for top, by_coord in view.readings.items():
        # A family is the run's to answer for where any of its members sits
        # in a released file LEDGERS names, not only its root: a folded
        # re-read is a released row too (round 3, 🟡 16).
        members = {key[0] for graded in by_coord.values() for key, *_ in graded}
        if top[0] not in wanted and not members & wanted:
            continue
```

```markdown
it adds the row. Where citing rows exist anyway, a `--reverify` narrowed with
`--ledger` names, by its root row, each family a released file it read holds
a member of whose newest reading sits in a file it did not write, and exits
1, because no in-place re-stamp of the files it read can clear that family.
```

```text
L4, the clause after "without the row it re-stamps in place as before,":
and narrowed with `--ledger` it names, by its root row, each family a released file it read holds a member of whose newest reading it could not reach and exits 1; under the freeze a narrowed `--into` writes the re-read such a family owes
```

```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py
def test_a_narrowed_into_answers_for_a_family_a_folded_member_puts_in_the_file(repo):
    """The run is narrowed to the release file holding a folded re-read of R,
    not R's own file. That member reads DRIFTED under the same narrowing, so
    `--into` owes its family a re-read (round 3, 🟡 16)."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [
            f"| R1 · handler adds one | `src/service.py#handler@{h1}` | read | 2026-01-01 | |"
        ],
    )
    cite = citation(r, "R1 · handler adds one")
    released(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `src/service.py#handler@{h1}` "
            "| read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        version="0.2.0",
        section="### 1500000001-the-second-item",
    )
    edit_handler(repo)
    h2 = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{cite}`, `src/service.py#handler@{h2}` "
            "| read | 2026-03-01 | Re-read 2026-03-01 |"
        ],
        name="2000000009-z",
    )
    (repo / "src" / "service.py").write_text(SERVICE)
    narrowed = ["--ledger", "seal/releases/0.2.0.md", "."]
    assert run(["--strict", *narrowed], repo).returncode == 2
    unfrozen = run(["--reverify", *narrowed], repo)
    assert unfrozen.returncode == 1, unfrozen.stdout
    assert "LEFT  seal/releases/0.1.0.md:5" in unfrozen.stdout, unfrozen.stdout
    frozen(repo, "0")
    out = run(["--reverify", "--into", INTO, "--checked", "2026-04-01", *narrowed], repo)
    assert "1 citing row written" in out.stdout, out.stdout
    assert run(["--strict", "."], repo).returncode == 0
```

### ⬜ 17

```python
# skills/evidence-check/scripts/evidence_check.py, family_view's emission loop
                    detail = (
                        f"matches only the reading of "
                        f"{checked(key) or 'no date the calendar has'}; "
                        f"the newest reading of this coordinate, {newest} at "
                        f"{where(last[0])}, holds other content — re-read"
                    )
```

Needs a fix: yes — 🟡 16 (a narrowed `--reverify` answers only for families rooted in a file it read; the home and L4 say otherwise)

Loses a record or crashes: no

## Proof block

Opened in this round, at `089a5c77` unless marked:

- `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/`: `rounds/round-2.md`, `rounds/round-2-report.md` in full; the fix range's diffs of `spec.md`, `plan.md`, `changelog.md`, `survivors.md`; `changelog.md:1-40`
- `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md`: the fix range's word diff; rows 1, 3, 4, 8, 36 in full
- `skills/evidence-check/scripts/evidence_check.py`: the fix range's diff; `literal_statements`, `minor_region`, `default_patterns`, `classify` (head), `ledger_kind`, `citation_for`, `family_view` from the citation loop to its return, `calendar_date`, `date_column`, `reverify` (head), `released_drift`, the `--reverify` branch of `main` and the narrowing notice above it
- `skills/evidence-check/scripts/correction_check.py:555-680`
- `docs/the-evidence-ledger.md:92-160` and the fix range's diff
- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: lines 1-175, 652-665, and the fix range's diff
- `bin/test`
- in the all-three merge: the `--strict`, re-stamp and fold outputs; `git grep SELF_ANCHOR_RE` over #647's head and `089a5c77`; `git show 63d75120 -- .github/scripts/fold_ledger.py`
