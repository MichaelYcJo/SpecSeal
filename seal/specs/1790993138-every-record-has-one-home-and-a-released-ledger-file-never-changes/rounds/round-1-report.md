# Round 1 report — #715, every record has one home and a released ledger file never changes

Ran by: `specseal:warden on claude-opus-5-5`.
Target: `626bdeb6` on `feat/715-every-record-has-one-home-and-a-released-ledger-file-never-changes`.
Base: `233f0455` (`origin/release/v0.18.0`). Diff: `233f0455..626bdeb6`, 29 commits on the branch
(26 build commits plus framing and routing).
First round; no earlier round record exists. Probes ran in a `git clone --no-local` of the
worktree at the target SHA, in this round's scratch directory, and the worktree's HEAD was never moved.

## Summary

One defect writes wrong data into the ledger. `--reverify --into` builds each
re-read coordinate by slicing the family root's line with a match taken from
another member's line. Once any `Re-read ·` row has been folded into a release
file, which the 0.18.0 release does with this branch's 42 rows, the command
writes a bare hash where a coordinate belongs and reports the row as written (🔴 1).

Four findings are about the family reading itself. Each makes a false claim
read OK, or lets a lost correction go unreported:

- the per-coordinate union accepts a pair of hashes no reading ever saw together (🟡 2);
- a `Corrected ·` row that re-points one moved coordinate stops every other coordinate of the row from being checked (🟡 3);
- two branches correcting one released row leave two contradictory claims, both OK and nothing named (🟡 4);
- `correction-check` keys a `Corrected ·` row whose citation holds `\|` on the wrong coordinate, so the row's loss at a merge is never reported (🟡 5).

Two findings are about the branch's own paperwork and its carriers. A re-read
the branch wrote vouches for a claim the branch made false (🟡 6). The release
checklist tells the next release preparation to run a command the freeze now
refuses (🟡 7). Two ⬜ are wording and an unreachable corner (8, 9).

What held, executed:

- S12: zero files under `seal/releases/` changed, and `seal/ledger.md` has one hunk, in its header above the first table.
- M2 holds end to end. All 1,083 released rows get a citation that resolves to their own line through the fragment-row parse, and `correction-check` reads every one of those citations back.
- The three sibling branches merge with this one without a textual conflict, and `correction-check` exempts each with its one line.
- The shipped scripts compile under Python 3.9.6, and `evidence_check.py` and `correction_check.py` run there.

## Stage 1 — spec compliance

The implementer's account was read in full (`overview.md`, `phases/`, the
changelog fragment, the commit messages, the spawn prompt). Each claim below
was checked against the code.

- **D2/W1, the citation literal.** Claimed: 0 of 1,083 coordinate-bearing
  released rows fail. Executed: every row's `citation_for` output was put
  into a `Corrected ·` fragment row, parsed back by `ANCHOR_RE`, resolved by
  `cited_row` and read by `correction_check.py#corrections`. Result: 1,083 rows,
  0 without a citation, 0 resolving to another line, 0 `correction-check`
  misreads. The closing-pipe fallback is used by 0 corpus rows, and 215 literals
  are under 8 characters (`S8 ·`, `F2 ·`). A citation cannot land on the wrong
  row by construction: the literal is unique in its section at write time, the
  section heading must be unique in its file, and the file is frozen. One shape
  is still mishandled downstream, the `\|` fallback (🟡 5). One row shape gets no
  citation at all (⬜ 9).
- **D3, the family verdict.** Probed (§*Executed probes*). The union is the
  halves rule computed at a merge, as S6/S7 show. It is wider than the rule it
  replaces in time, though. The old in-place re-stamp kept one hash per unit.
  The union keeps every hash anyone ever recorded and mixes them across units
  (🟡 2). The stated failure direction names the single-unit revert, and its
  grounds sentence ("somebody read the claim against that content") is false
  for the mixed case.
- **A released row whose anchor moved.** It is sound that a `Re-read ·` row
  cannot clear a coordinate whose spelling changed: the family is keyed on the
  spelling. The `Corrected ·` repair has a cost nothing names, though. The
  correction supersedes the whole row, so it silences every coordinate the
  correction leaves out (🟡 3). The repair text the tool prints, "re-points or
  retires it", invites exactly that partial row.
- **D5, the freeze.** Read `correction_check.py#frozen_changes`, and executed
  against all three siblings. Each sibling was merged into this branch's tip,
  standing in for the release branch after this lands, and `correction-check
  --range <tip>...<merge>` ran on each. All three exit 0 with `every work item
  this range adds (17909931NN) is below Ledger frozen from 1790993141`. The key
  is the added `routing.md`, so a sibling stays exempt after merging the release
  branch in. CI's `origin/release/vX.Y.Z...HEAD` spelling was read rather than
  executed: `BASE_VERSION` matches it.
- **What the siblings meet anyway (executed, not a finding).** `evidence-check
  --strict` on the merged trees exits 2:
  - with #647 merged: 4 citations into release files #647 re-stamps in place
    drift, plus 2 family drifts on `templates/config.md`, which both branches edit;
  - with #718 merged: 2 citation drifts plus 1 family drift on `docs/branch-and-release.md`;
  - with #716 merged: 0;
  - with all three merged: 9.

  This is spec §*How a branch cut before this one stays valid*'s "one
  interaction that remains". CI's ledger job is lenient, so CI stays green, but
  the sealer's `--strict` run comes back NOT SEALED for whichever branch lands
  second. The repair is a re-read and an in-place re-stamp of this work item's
  fragment rows, in the second lander's branch. The orchestrator should hand
  that to the second lander by name.
- **D6, the fold and `settle`.** Read. `--split` is gone from code, help,
  `CONTRIBUTING.md` and the release checklist. The older-version refusal
  compares against `release_files`, which sorts by `version_key`. On whether
  `settle` can retire a directory something still cites: its superseded skip
  asks the checker's own `family_view` over every ledger the checker reads, and
  skips exactly the rows the checker stops grading, R and its re-reads. The
  `Corrected ·` row itself stays checked, so a correcting row's own coordinate
  into the directory still keeps it. Consistent. The one escape is a dropped
  correction (`correction-check`'s arm, 🟡 5 for one citation shape).
- **One home per rule.** Every rule removed from `CLAUDE.md` and
  `CONTRIBUTING.md` was searched for in its home: the coordinate shape, no line
  number or SHA, no git except `--migrate`, DRIFTED-never-BROKEN, REMOVED not
  re-pointed, `--checked`, hunk by hunk, never ours/theirs, the halves, the
  fragment table, no header, the `## ` line in a changelog fragment, the
  evidence-todo refusal, the fold `--check` on PRs into `main`, and two commands
  in one commit. Each is stated in `docs/the-evidence-ledger.md`,
  `docs/the-record-layout.md` or `docs/release-checklist.md`. No carrier lost a
  rule only it stated. W3 holds: `agents/smith.md` defers to the repository's
  convention. Two carriers keep a sentence the freeze made wrong: the release
  checklist's §3 table row (🟡 7) and the home's own REMOVED sentence (⬜ 8).
- **The branch's own ledger work.** Claimed in the spawn prompt: "42 `Re-read ·`
  and 18 `Corrected ·` rows cover 63 released rows". The fragment holds 42
  `Re-read ·`, 11 `Corrected ·` and 10 new rows, and they cite 53 distinct
  released rows, one citation each. No record of the work item states 18 or 63;
  the figure was the prompt's. Sampled hard: rows 11–35, 43–55 and 60–63 were
  read against their claims, and the `Corrected ·` rows 36–42 and 56–59. Row 25
  re-reads a claim this branch made false (🟡 6). The rest that were opened hold,
  including row 30: `built_name` calls `display_name`, so "every place … calls
  `display_name`" still holds.
- **S13.** `docs/the-record-layout.md` has every row the scenario names, the D7
  cut and F1–F4 marked as not built. It is 196 lines and 12 KB, and
  `tests/test_docs_line_wrap.py` passes (executed).
- **Python floor.** Compiling with py_compile under `/usr/bin/python3` 3.9.6 passes for
  `evidence_check.py`, `correction_check.py`, `settle.py`, `evidence-advisor.py`,
  `fold_ledger.py` and `survivor_check.py` (executed).
  `evidence_check.py --strict .` and `correction_check.py --range` run to
  completion under 3.9.6. The 8 DRIFTED rows 3.9 reports, all on
  `tests/test_the_root_migrates_itself.py`, are the same at the base under 3.9
  and 0 under 3.12, so they come from `ast`'s spans on 3.9, not from this branch.
  The new code uses `functools.cache` (3.9) and nothing newer.

## Stage 2 — quality

### 🔴 1 — `--into` writes a bare hash for a coordinate a folded re-read carries, and reports it written

`skills/evidence-check/scripts/evidence_check.py:3198-3199`, in `reverify_into`.

`released_drift` files each drifted coordinate under the family's root (`top`),
but the match `m` it keeps comes from whichever released member graded DRIFTED
first. At `:3131` that is any member of the family, in `str(file_identity)`
order. `reverify_into` then slices `lines[key[1] - 1]`, the root's own line,
at `m`'s offsets. When `m` came from another member, the slice is a fragment
of an unrelated cell.

Executed: released R in `0.1.0.md` cites `handler`. A folded `Re-read ·` row in
`0.2.0.md` cites R and adds `other`. Editing `other` and running `--reverify
--into … --checked …` exits 0 and prints `1 citing row written · 0 released
rows left`. Where the row should carry the fixture's coordinate for `other`
at its new hash, it carries the bare hash `` `90309471` ``, and the next
`--strict` still reports `other` DRIFTED.

Why it matters: `--into` is the only documented repair for a drifted released
row. From the 0.18.0 release on, the fold puts this branch's 42 `Re-read ·`
rows into a release file, so every family they belong to has a released member
other than its root. A coordinate shared by R and that member is sliced
correctly or not depending on inode order. A coordinate only the member carries
is always wrong.

The fix slices the line the match was made on, `m.string`, which is right for
both loops in `released_drift`. Executed with the fix: the row carries the whole
coordinate for `other` at that hash, and `--strict` exits 0. The two touched
modules pass, 101 cases.

### 🟡 2 — the union accepts a pair of hashes no reading recorded together, and the stated cost says otherwise

`skills/evidence-check/scripts/evidence_check.py:2402` (`held` per coordinate),
`docs/the-evidence-ledger.md:102-104`, spec D3's *Failure direction*.

A code coordinate is OK when any member recorded its current hash, and each
coordinate is judged alone. Executed:

1. R records `handler@h1` and `other@o1` for "handler's increment matches other's factor".
2. Both units change, and a `Re-read ·` row records `h2` and `o2`.
3. `handler` alone is reverted to `h1`.

Result: `--strict` exits 0, 5 OK. The pair `(h1, o2)` was never read, and the
claim is false there.

Under the rule this replaces, the in-place re-stamp had moved R to `(h2, o2)`,
and the revert reads DRIFTED. The home's sentence, "content that returns to a
hash an earlier reading recorded reads OK again, because somebody read the
claim against that content", covers the single-unit revert only. A partial
revert, meaning one unit back at an old reading while another sits at a newer
one, is the realistic case: `git revert` of a commit that touched one of a
claim's units. Every re-read adds a hash that stays valid until a correction
cuts the family, so the accepted set only grows.

The union per coordinate is what S6 needs, because `--into` writes only the
drifted coordinates of a row. So the minimum fix is to state the cost truly and
pin it. A narrower rule exists if the owner wants one: per coordinate, accept
only the readings with the newest `Checked` date, ties kept as a union. It
passes S6 and S7, since a same-day parallel pair is a tie, and it reads P1's
revert as DRIFTED. Spec D3 rejected "the newest re-read" for whole rows; this
is per coordinate with ties, which D3's grounds do not reach. Whether to take
it is the repository owner's decision.

### 🟡 3 — a `Corrected ·` row that re-points one moved coordinate stops the row's other coordinates from being checked

`skills/evidence-check/scripts/evidence_check.py:3217` (the LEFT text),
`docs/the-evidence-ledger.md:119-121`, `hooks/evidence-advisor.py` (`FROZEN_REPAIR`).

Executed:

1. R records `handler@h1` and `other@o1`.
2. `handler` is renamed. `--into` correctly leaves it, saying `a re-read cannot clear it, so a Corrected · row in your own fragment re-points or retires it`.
3. A `Corrected ·` row citing R with `handle2@<now>` alone gives `--strict` 0.
4. Then `other` is edited, and `--strict` still exits 0.

R's `other` is never read again, because the correction supersedes R's whole
family. The design is right that a correction ends R's claim. Nothing says,
though, that the correcting row must carry the coordinates the claim still
rests on. The tool's own repair text names only the moved coordinate, and the
home's "a `Corrected ·` row re-points it" reads the same way. A pure move
(rename, file move) is the commonest BROKEN, and each one repaired this way
silently drops the rest of the row's grounds.

### 🟡 4 — two branches correcting one released row leave two contradictory claims, both OK

`skills/evidence-check/scripts/evidence_check.py:2374-2378` (`superseded`).

Executed: R "handler adds one". Fragment A has `Corrected · handler adds two`
and fragment B has `Corrected · handler adds three`, both citing R and both
with `handler` at its current hash. `--strict` exits 0, 4 OK, nothing named.

Under the old rule the two in-place corrections met on R's line, and a person
read both hunks. Now each correction starts its own family, and nothing
reports a released row superseded twice. Two parallel branches that each find
one row false is exactly the case the conflict used to surface. It is the same
situation as D3's two parallel re-reads, but for claims, where a union is not
an answer. `correction-check` does not see it either: neither row was dropped.
Spec D3 is silent on more than one correction of one row.

The fix names the case so a person reads the two together. Which row stays is
then a claim judgment. The repair path needs one decision. The second lander
cannot cite the first lander's correction, because a citation into a fragment
is refused until the fold, so the repair is to merge the two claims into one
row. That edits another work item's fragment, which `docs/the-evidence-ledger.md`
already allows for stacked branches (hunk by hunk).

### 🟡 5 — `correction-check` reads a closing-pipe citation as the next coordinate, so dropping that `Corrected ·` row is never reported

`skills/evidence-check/scripts/correction_check.py:426` (`ANCHOR`), `:583` (`corrections`).

`citation_for` writes the literal `"<cell tail> \|"` when every prefix of the
first cell also stands on another line, and it escapes any `|` in a heading the
same way. `ANCHOR`'s locator class `[^`@|]*?` cannot cross the `|`, so the first
match on such a row is its first code coordinate. Executed: the citation
`seal/releases/0.1.0.md#"### …">"R1 · it adds \|"@…` makes `corrections()`
return `{'src/service.py#handler': …}`.

`dropped_corrections` then takes `src/service.py` as the cited file, finds it in
no ledger listing, and skips the row (`:352-354`, read). A merge that drops such
a row is not reported, and two such rows sharing a first code coordinate also
collide in `setdefault`.

No corpus row needs the fallback today (M2 re-run). But it is a shape the
build writes and pins (`test_the_citation_written_for_a_row_names_that_row_alone`),
and the arm exists precisely so a dropped correction does not bring a false
claim back.

Executed with the fix below: the key becomes the citation, and all 1,083 corpus
citations still read back. The two touched modules pass.

### 🟡 6 — row 25 of the branch's fragment re-reads a claim the branch made false

`seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md:25`,
citing `seal/releases/0.4.0.md` "The checker de-duplicates on `(coordinate, hash)`
within one file, so a fold moves its total by exactly the rows two files cited
identically".

The row was written by `--into` and carries its boilerplate, "the cited row's
claim holds". It no longer does. `check_ledger` blanks every row in a family
before `check_text`'s per-file `seen` runs, and `family_view` emits per row, so
a `(coordinate, hash)` that a family row shares with another row of its file is
counted twice.

Executed: one release file with two rows citing one `(coordinate, hash)` prints
`1 ok`. Add a fragment re-reading one of them, and the same file prints `2 ok`.
The 0.18.0 fold puts 53 citing rows into a release file, so the total stops
being the count the claim describes. The row should be a `Corrected ·` row.

§12, the class: the other re-reads of rows about `check_text` or `check_ledger`
behaviour were read. Rows 12, 14, 22 and 30 still hold: fences are skipped
through `ledger_table_rows`, OVERFLOW still comes from `overflow_rows`, an
unreadable ledger is still reported by `check_ledger`, and `built_name` goes
through `display_name`.

### 🟡 7 — the release checklist tells the next release preparation to run `--reverify --checked`, which the freeze now refuses

`docs/release-checklist.md:199`, §3's table, row `evidence-check --strict`.

The row says drift from the preparation's own edits is fixed with
"`--reverify --checked <date>` … narrowed with `--ledger` … in the same
commit". In this repository `--reverify` now writes no released file. It exits
1 naming each row and the `--into` form. A fragment written then must also be
folded, or `fold_ledger.py --check` refuses the release pull request into
`main` with `ledger fragments that never folded`.

The 0.18.0 preparation is the first reader of this row under the freeze. The
carrier instrument the spec names (`git grep -l -- '--reverify'`) does find
this file, but phase 6 changed §2 and left this row in §3.

### ⬜ 8 — the home says a removed anchor's row is REMOVED, and two sections later says a released row is never removed and a `Corrected ·` row re-points it

`docs/the-evidence-ledger.md:37-38` against `:89-91` and `:119-121`.

§*A row is a content anchor* still states "A row whose anchor a change removes
is `REMOVED`, not re-pointed" with no qualification. Under the freeze a released
row is neither removed nor left: a `Corrected ·` row retires it, or re-points a
moved one. The behaviour is right and the sentence is unqualified. Spec
§*Grounding* also says this work "keeps" REMOVED-not-re-pointed, while the
overview's divergence table shows the build re-points via `Corrected ·`.

### ⬜ 9 — a row whose first cell also closes another cell of its section gets no citation, so it can be neither re-read nor corrected

`skills/evidence-check/scripts/evidence_check.py:2160-2180` (`unique_literal`).

Executed: R1 `| R1 · handler adds one | … |` and R2 `| R2 · other doubles | … | see
R1 · handler adds one |`. `citation_for` returns None for R1. Every prefix
stands on R2's line, and so does the closing-pipe tail. `--into` would leave R1
with "no citation names this row alone", and no repair exists. No corpus row
has this shape (M2: 0 of 1,083), and a frozen file cannot grow one, but a
future release file can. A last fallback anchored on the row's leading pipe
names it. That fix was not executed.

## Regression tests to plant

Each case below was seen red against `626bdeb6` by the probe named in
§*Executed probes*. Cases 1 and 5 also went green with the fix applied in the
scratch clone.

```text
tests/test_a_released_row_is_read_again_in_a_fragment.py
  1. --into re-reads a coordinate that only a folded Re-read row carries        (🔴 1)
  2. a partial revert reads as the home states it: OK under the union as it     (🟡 2)
     stands, or DRIFTED if the owner takes the newest-per-coordinate rule
  3. --into's LEFT line for a moved released row says the correction carries    (🟡 3)
     every coordinate the claim rests on (pins the sentence, contract §14)
  4. a released row corrected by two Corrected · rows is named on both           (🟡 4)
tests/test_a_merge_cannot_silently_drop_a_correction.py
  5. corrections() keys a closing-pipe citation by the citation, and a merge     (🟡 5)
     dropping that row is reported
```

## Facts for the evidence ledger

- The family union is per coordinate. A row citing two units reads OK at a pair
  of hashes that no member recorded together (executed, probe P1).
- With W1's rule, all 1,083 coordinate-bearing released rows at `626bdeb6` get a
  citation that resolves to their own line through a fragment row's parse, and
  `correction_check.py#corrections` reads each back. The closing-pipe fallback is
  used by none (executed, M2 re-run).
- The three 0.18.0 siblings merge with this branch without a textual conflict.
  `correction-check` exempts each by its added `routing.md` id. `evidence-check
  --strict` on the merged trees reports 6, 3 and 0 drifted, and 9 with all
  three merged (executed).
- The shipped scripts this branch touches compile under Python 3.9.6, and
  `evidence_check.py` and `correction_check.py` run there. 3.9 reports 8 DRIFTED
  rows on `tests/test_the_root_migrates_itself.py` at the base as well, and
  3.12 reports 0 (executed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `--into` slices the family root's line with a match from another member, writes a bare hash for the coordinate and reports the row written | `skills/evidence-check/scripts/evidence_check.py:3198` | open | executed: the row carried `` `90309471` `` for `src/service.py#other`, exit 0, drift still reported; fixed in the scratch clone with `m.string` |
| 🟡 2 | the per-coordinate union reads OK a pair of hashes no reading recorded together, and the home's stated cost says somebody read it | `skills/evidence-check/scripts/evidence_check.py:2402`, `docs/the-evidence-ledger.md:102` | open | executed: R at (h1,o1), re-read at (h2,o2), revert to (h1,o2) reads 5 OK, exit 0; the replaced in-place rule reads DRIFTED |
| 🟡 3 | a `Corrected ·` row re-pointing one moved coordinate silences the row's other coordinates, and the repair text invites that row | `skills/evidence-check/scripts/evidence_check.py:3217`, `docs/the-evidence-ledger.md:121` | open | executed: after the partial correction an edit to `other` reads exit 0 |
| 🟡 4 | two `Corrected ·` rows correcting one released row both read OK and nothing names them | `skills/evidence-check/scripts/evidence_check.py:2374` | open | executed: contradictory corrections, exit 0, 4 OK; spec D3 is silent on it |
| 🟡 5 | `correction-check` keys a closing-pipe citation on the next coordinate, so its dropped row is never reported | `skills/evidence-check/scripts/correction_check.py:583` | open | executed: key `src/service.py#handler`; `dropped_corrections` then skips it (read); fixed in the scratch clone |
| 🟡 6 | the fragment's row 25 re-reads the per-file dedup claim, which family rows no longer obey | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md:25` | open | executed: one file goes from 1 ok to 2 ok for one `(coordinate, hash)` once a row is in a family |
| 🟡 7 | the release checklist's §3 drift row prescribes plain `--reverify --checked`, which writes no released file under the freeze | `docs/release-checklist.md:199` | open | read; the 0.18.0 preparation is its first reader |
| ⬜ 8 | the home's REMOVED-not-re-pointed sentence is unqualified beside the freeze's never-removed, re-pointed-by-correction rule | `docs/the-evidence-ledger.md:37` | open | read |
| ⬜ 9 | a row whose first cell also ends another cell of its section gets no citation | `skills/evidence-check/scripts/evidence_check.py:2160` | open | executed: `citation_for` returns None; 0 corpus rows have the shape |

## Executed probes

| What was run | Result |
|---|---|
| S12: `git diff --name-only 233f0455...HEAD -- seal/releases`; hunks in `seal/ledger.md` | 0 files; 1 hunk, in the header above the first table |
| the new and changed modules in the clone: `bin/test` on the five ledger test modules | 179 passed |
| `tests/test_docs_line_wrap.py` | 35 passed |
| `evidence_check.py .` at HEAD under 3.12 / `--strict` under 3.9.6 / at the base under both | HEAD 3.12: 3776 ok, 0 drifted. HEAD 3.9: 8 drifted. Base 3.12: 0 drifted. Base 3.9: the same 8 drifted |
| py_compile of six shipped scripts under 3.9.6; `correction_check.py --range 233f0455...HEAD` under 3.9.6 | all 0; exit 0 with the exempt line for 1790993138 |
| sibling merges (#647, #718, #716, all three) into the tip, then `evidence-check --strict` and `correction-check --range <tip>...<merge>` | 0 conflicts; correction-check exit 0 with the exempt line for each; strict drift 6, 3, 0, 9 |
| M2 end to end: `citation_for` → fragment row → `ANCHOR_RE` → `cited_row`, and `corrections()` | 1,083 rows, 0 without a citation, 0 wrong rows, 0 misread; 0 fallback; 215 literals under 8 chars |
| P1: joint revert (🟡 2) | exit 0, 5 OK at a pair nobody read |
| P2: moved anchor and partial correction (🟡 3) | BROKEN, then LEFT by `--into`, then exit 0 after the correction, then exit 0 after `other` changed |
| P3: `Corrected ·` row with no marker | MALFORMED, exit 1 lenient and 2 strict; it still supersedes |
| P4: two contradicting corrections (🟡 4) | exit 0, 4 OK |
| P5: first cell repeated in another row's last cell (⬜ 9) | `citation_for` → None |
| P6: `--into` with a folded re-read member (🔴 1) | wrote `` `90309471` ``, exit 0; with the `m.string` fix: wrote the full coordinate, then strict exit 0 |
| pipe citation through `corrections()` (🟡 5) | key `src/service.py#handler`; with the `CITATION` fix: the citation |
| dedup (🟡 6) | release file 1 ok → 2 ok once one row is in a family |
| the two touched modules with both fixes applied in the clone | 101 passed |
| `fold_ledger.py --check` at HEAD | exit 1, naming only this branch's unfolded fragment: expected on a feature branch |
| the broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, once the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the newest-dated-per-coordinate rule as a replacement for the plain union (🟡 2's second option) | spec D3, as a question beside the stated cost | the repository owner |
| who re-stamps this fragment's 9 citing rows when #647 and #718 land before or after this branch | the orchestrator's handoff to the second lander | the orchestrator of the 0.18.0 run |

## Paste-ready fixes

### 🔴 1

```python
# skills/evidence-check/scripts/evidence_check.py, reverify_into
    for key in sorted(drifted, key=lambda k: (view.files[k[0]][0], k[1])):
        path, body, _, table = view.files[key[0]]
        # ... unchanged down to the stamping loop ...
        stamped = []
        for coord, m in drifted[key].items():
            new = current_hash(m, root, maps, default_repo)
            if new is None:
                left.append((where, f"{coord} — no one place to hash, so not re-read"))
                continue
            # M may come from any released member of the family, not from
            # KEY's own line (`released_drift`): slice the line it was matched on.
            stamped.append(spanned(m.string[m.start() : m.start("hash")] + new))
```

```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py
def test_into_re_reads_a_coordinate_a_folded_re_read_carries(repo):
    """The drifted coordinate sits on a folded `Re-read ·` row, not on the
    family's root: the row `--into` writes names it whole (warden round 1)."""
    handler = unit_hash(repo, "src/service.py", "handler")
    other = unit_hash(repo, "src/service.py", "other")
    (row,) = released(
        repo, [f"| R1 · handler adds one | `src/service.py#handler@{handler}` | read | 2026-01-01 | |"]
    )
    folded = (
        f"| Re-read · R1 · handler adds one | `{citation(row, 'R1 · handler adds one')}`, "
        f"`src/service.py#other@{other}` | read | 2026-02-01 | Re-read 2026-02-01 by work item 2 |"
    )
    released(repo, [folded], version="0.2.0", section="### 2000000001-a-later-item")
    (repo / "seal" / "config.md").write_text(
        "| Item | Value |\n|---|---|\n| Ledger frozen from | 0 |\n"
    )
    (repo / "src" / "service.py").write_text(SERVICE.replace("x * 2", "x * 7"))
    r = run(
        ["--reverify", "--into", "seal/ledger/3000000001-y.md", "--checked", "2026-03-01", "."],
        repo,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    written = (repo / "seal" / "ledger" / "3000000001-y.md").read_text()
    assert f"`src/service.py#other@{unit_hash(repo, 'src/service.py', 'other')}`" in written
    assert run(["--strict", "."], repo).returncode == 0
```

### 🟡 2

`docs/the-evidence-ledger.md` §*A released row is read again in the branch's
fragment*: this replaces the sentence that begins "Its one cost is stated".

```markdown
neither matches. Its cost is stated in two parts. Content that returns to a
hash an earlier reading recorded reads OK again, because somebody read the
claim against that content. And the union is per coordinate, not per
reading: a row citing two units is OK when each unit matches some reading,
though no reading may have seen that pair together. A partial revert lands
there — one unit back at an old reading, the other at a newer one — and a
claim about how the two units fit can be false while it reads OK. The in-place
re-stamp this replaced kept one hash per unit and read that state DRIFTED.
```

(Spec D3's *Failure direction* bullet and the comment above `CITING_VERBS` take
the same second sentence. The case in §*Regression tests to plant* item 2 pins it.)

### 🟡 3

```python
# skills/evidence-check/scripts/evidence_check.py, reverify_into
    for at, coord, detail in broken:
        left.append(
            (
                at,
                f"{coord} BROKEN — {detail}; a re-read cannot clear it, so a "
                "`Corrected ·` row in your own fragment re-points or retires it — "
                "and carries every other coordinate the claim still rests on, "
                "because the correction supersedes the whole row and a "
                "coordinate it leaves out is not checked again",
            )
        )
```

`docs/the-evidence-ledger.md`, the end of the `--into` paragraph:

```markdown
row whose anchor moved is not cleared by a re-read, because the family is
keyed on the coordinate, and a `Corrected ·` row re-points it. That row
supersedes the whole released row, so it carries every coordinate the claim
still rests on, the moved one at its new place: a coordinate it leaves out is
not checked again.
```

### 🟡 4

```python
# skills/evidence-check/scripts/evidence_check.py, family_view, after `superseded = {...}`
    # A released row corrected by more than one row carries two claims and
    # nothing reconciles them: the conflict two in-place corrections used to
    # meet on is gone, so the checker names the pair instead (warden round 1).
    corrected_by = {}
    for key in parent:
        if verb_of(key) == "Corrected" and root_of(parent[key]) != key:
            corrected_by.setdefault(root_of(parent[key]), []).append(key)
    for top, keys in corrected_by.items():
        if len(keys) < 2:
            continue
        keys.sort(key=lambda k: (str(k[0]), k[1]))
        names = ", ".join(where(k) for k in keys)
        for key in keys:
            emit(
                key,
                (
                    "DRIFTED",
                    coordinate_of(citations[key]),
                    f"the row it cites is corrected by {len(keys)} rows ({names}) "
                    "— read them together and keep one claim",
                ),
            )
```

### 🟡 5

```python
# skills/evidence-check/scripts/correction_check.py, beside CORRECTED_ROW
# A citation's locator is quoted, and a quoted segment may hold `\|` -- the
# closing-pipe literal `citation_for` writes, or a heading with a pipe in it.
# `ANCHOR` stops at any `|`, so it is tried second.
CITATION = re.compile(
    r'([^\s`|]+\.[A-Za-z0-9]+#"(?:[^"\\]|\\.)*"(?:>"(?:[^"\\]|\\.)*")?)@[0-9a-f]{6,}'
)


def corrections(text):
    """`{citation: row}` for every `Corrected ·` row of `text`."""
    found = {}
    for row in rows(text):
        if not row.key.startswith(CORRECTED_ROW):
            continue
        cited = CITATION.search(row.raw) or ANCHOR.search(row.raw)
        if cited:
            found.setdefault(cited.group(1).strip(), row)
    return found
```

### 🟡 6

```markdown
| Corrected · `check_text` de-duplicates on `(coordinate, hash)` within one file for the rows no family reads; a row that cites a released row, or is cited by one, is graded per row by `family_view`, which does not de-duplicate, so once citing rows fold a fold moves the `ok` total by more than the rows two files cited identically | `seal/releases/0.4.0.md#"#### The fold is a move, marked and ordered">"The checker de-duplicates"@1e14ea36`, `skills/evidence-check/scripts/evidence_check.py#check_text@c4b73b1a`, `skills/evidence-check/scripts/evidence_check.py#family_view@59d80192` | **Executed** <date>: one release file with two rows citing one `(coordinate, hash)` prints `1 ok`, and `2 ok` once a fragment re-reads one of them | <date> | Corrected <date> by work item 1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes: the family reader grades a cited row outside `check_text`'s per-file `seen` |
```

(It replaces line 25 of the fragment. A `Re-read ·` and a `Corrected ·` row
citing one released row would leave the `Re-read ·` row inside a superseded
family, unread.)

### 🟡 7

```markdown
| `evidence-check --strict` | rows anchored on units the preparation edited read as drifted. Where `seal/config.md` declares `Ledger frozen from`, as this repository does, re-read every row citing them, write the re-reads with `--reverify --into seal/ledger/<unix-seconds>-fold.md --checked <date>`, and fold that fragment with a second `fold_ledger.py --version X.Y.Z` in the same commit, which joins the release's file; plain `--reverify` writes no released file and exits 1 naming each row. Without the row, `--reverify --checked <date>` narrowed with `--ledger` to the files read, in the same commit. The total can drop across a fold: two fragments citing one coordinate identically fold into one row, and the unique-anchor count is what stays equal |
```

### ⬜ 8

```markdown
removes. **A row whose anchor a change removes is `REMOVED`, not re-pointed**
— its claim went with the code, and the new claim is a new row. Under the
freeze a released row is never removed: a `Corrected ·` row retires it, or
re-points a moved one (§*A released row is read again in the branch's
fragment*).
```

### ⬜ 9

```python
# skills/evidence-check/scripts/evidence_check.py, unique_literal, before `return None`
# (not executed in round 1)
    # The cell whole, with the row's leading pipe: no other cell begins a line.
    whole = "| " + " ".join(cell.split()) + " |"
    if not LITERAL_STOP_RE.search(whole[2:-2]):
        hits = literal_statements(lines, region, whole)
        if len(hits) == 1 and hits[0][0] == number:
            return whole
```

Needs a fix: yes — 🔴 1 (`--into` writes a broken coordinate), 🟡 2–7 (the union's stated cost, the partial correction, the double correction, the pipe citation in `correction-check`, fragment row 25, the release checklist's §3 row)

Loses a record or crashes: yes — 🔴 1 writes a re-read row whose coordinate is a bare hash and reports it written, so the reading it was asked to record is lost; 🟡 5 lets a dropped `Corrected ·` row pass `correction-check` unreported

## Proof block

Opened in this round, at `626bdeb6` unless marked:

- `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/`: `spec.md`, `questions.md`, `overview.md`, `phases/phase-4.md` (lines 40–60), `phases/phase-6.md` (lines 30–75)
- `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md` (all 63 rows listed; rows 25, 36–42 and 56–59 read in full)
- `seal/releases/0.8.3.md:13`, `seal/releases/0.14.0.md:36`, `seal/releases/0.4.0.md:199`
- `skills/evidence-check/scripts/evidence_check.py`: the full diff, plus `literal_statements`, `minor_region`, `recorded_here`, `ledger_table_rows`, `row_label`, `exit_code`, `file_identity`, `display_name`, `built_name`
- `skills/evidence-check/scripts/correction_check.py`: the full diff, plus `parse_range`, `examine`, `ANCHOR`
- `.github/scripts/fold_ledger.py`: the full diff, plus `release_files`
- `skills/settle/scripts/settle.py`: the full diff, `anchored_rows`, the floor guard
- `hooks/evidence-advisor.py`, `skills/code-review/scripts/survivor_check.py`, `skills/verify/scripts/unverified_check.py`, `seal/config.md`, `seal/ledger.md`: diffs
- `CLAUDE.md`, `CONTRIBUTING.md`: diffs, and `CONTRIBUTING.md:100-175`
- `docs/the-evidence-ledger.md:14-45, 60-175, 178-235, 290-420`; `docs/the-record-layout.md` whole; `docs/release-checklist.md:185-205`, its diff
- `skills/evidence-check/SKILL.md`, `skills/settle/SKILL.md`, `templates/config.md`: diffs; `skills/code-review/orchestration.md:470-495`; `skills/implement/SKILL.md:260-275`; `agents/smith.md:134-135`
- `tests/test_a_released_row_is_read_again_in_a_fragment.py:1-140` and its case list
- `.github/workflows/hygiene.yml`: the correction-check step
