# Round 2 report — #715, every record has one home and a released ledger file never changes

Ran by: `specseal:warden on claude-opus-5-5`.
Target: `30369bde` on `feat/715-every-record-has-one-home-and-a-released-ledger-file-never-changes`, PR #736. Fix range
`f50f5f05..b726c91b`, 13 commits, then round 1's close commit `30369bde`.
A verifying round: its target is the fix diff, not the branch. Probes ran in a
`git clone --no-local` of the worktree at `30369bde`, in this round's scratch
directory. The worktree's HEAD was never moved, and nothing in it was written
except this file.

## Summary

All nine round 1 findings are closed at their commits, and every case the fix
pass planted was seen red against the pre-fix code (executed). M2 still holds:
1,083 rows, 0 misreads (executed). Folding this release's fragments into
`seal/releases/0.18.0.md` changes no verdict, alone or with the three siblings
merged (executed).

Three new 🟡 findings sit in the units the fixes created. Each is a case where
the newest-date rule or the double-correction notice says something the tool
cannot then act on:

- the home and the changelog say the rule never accepts a pair of hashes no
  reading saw together, and S6, the rule's own target case, accepts exactly
  such a pair (🟡 10);
- once two corrections of one row have folded, the notice is permanent, and a
  third correction retiring one of them does not clear it (🟡 11);
- `--reverify` narrowed with `--ledger` to a released file, as the home tells
  a person to do, reports nothing owed while the family reads DRIFTED (🟡 12).

Three ⬜: a `Checked` cell holding a date the calendar does not have outranks
every later reading (⬜ 13); the whole-cell fallback's comment states a
property the match does not test (⬜ 14); the test module's docstring still
states the plain union (⬜ 15).

## The orchestrator's decision on round 1's 🟡 2, against the code

The decision was built as decided (read and executed). Per coordinate,
`family_view` takes the newest date among the members that record that
coordinate, accepts only those readings, and keeps a tie as a union
(`skills/evidence-check/scripts/evidence_check.py:2428-2482`). How the edges
fall, each read in `checked` and the emission loop:

- **A missing date** reads as `""`, which sorts below every date. A released
  row with no date loses to any dated reading, and a family with no dates is
  the old union. The corpus has none: 1,146 anchored ledger rows, 0 without a
  date, 0 invalid, 0 later than today (executed scan).
- **A malformed date** that still matches `CHECKED_RE`, such as `2026-13-45`,
  is compared as a string and outranks every real date (⬜ 13, executed).
- **A family whose newest reading is a `Corrected ·` row.** Dates play no part
  in superseding: a `Corrected ·` row supersedes R's family whatever the
  dates, and starts a family of its own, where the same rule applies. That is
  D3 as round 1 read it, unchanged by the fix.
- **`released_drift` follows the family.** It now skips a coordinate only
  where `view.held` is non-empty, which is the same answer `family_view`
  emits. One assumption in its new comment fails under `--ledger` (🟡 12).

Against S6, S7 and the fold, executed:

- `tests/test_two_branches_re_read_one_released_row.py` passes at HEAD. With
  the tie removed (only the first newest reading kept), the tie case goes red
  and S6 and S7 stay green: S6 and S7 never exercise the tie, because their
  two branches re-read different coordinates (S6) or both miss (S7).
- `fold_ledger.py --version 0.18.0` at HEAD moves the fragment into
  `seal/releases/0.18.0.md` with its dates as written, and `--strict` reads
  3,786 ok, 0 drifted, before and after.
- With #647, #718 and #716 merged, the second lander's repair applied, and all
  four fragments folded: 3,991 ok, 0 drifted, exit 0.

## The sibling merges, re-run

Executed, each sibling merged into `30369bde` with git's own merge:

| Merged | Conflicts | `--strict` drifted | `correction-check` |
|---|---|---|---|
| #647 | 0 | 6 | exit 0, exempt (1790993137) |
| #718 | 0 | 3 | exit 0, exempt (1790993139) |
| #716 | 0 | 0 | exit 0, exempt (1790993140) |
| all three | 0 | 9 | exit 0, all three exempt |

The counts are round 1's, so the newest-date rule added no drift to the merge.
No finding reads `matches only the reading of`: #647 re-stamps released rows
in place dated 2026-10-03, which ties with this branch's re-reads.

**The second lander's re-stamp count is 7 rows, not 9.** Round 1 counted the
9 findings. In the all-three merge, `--reverify --into <this fragment>
--checked 2026-10-03` re-stamped 8 hashes on 7 rows, wrote 0 citing rows and
left 0, after which the ledger reads 0 drifted:

- 6 rows of this work item's fragment: 12, 18, 29, 30, 45 and 60. Row 29
  carries two of the hashes, its citation and `templates/config.md`.
- 1 row of #718's fragment, row 23, on `docs/branch-and-release.md`.
- The ninth finding is released R in `seal/releases/0.5.0.md`, in row 29's
  family. It clears when row 29 is re-stamped.

**One interaction round 1 did not report.** In the #647 merge, `--strict`
still exits 2 after the ledger is clean. The records arm refuses 4 names,
because #647's `phases/phase-3.md` and `rounds/round-1-report.md` name
`fold_ledger.py#SELF_ANCHOR_RE`, a unit this branch's build removed (NAME NOT IN TREE)
in `63d75120`. After the fold the arm reads no work item, so the refusal is gone, but the
sealer of whichever of #647 and #715 lands second meets it before the fold.
This is outside the fix range and is not a finding of this branch's code. It
goes to the orchestrator's handoff (§*Deferred*).

## Stage 1 — each round 1 fix at its commit

The fix pass's account (`round-1.md`'s verdicts and the commit messages) was
read and checked against the code; each line below is what the code does.

- **🔴 1, `d971ba27`.** `reverify_into` slices `m.string`, the line the match
  was made on (`evidence_check.py:3267-3270`). Both loops of `released_drift`
  take `m` from `ANCHOR_RE.finditer` over one member's line, so `m.string` is
  always that line. The case is red at `f50f5f05` (executed).
- **🟡 2, `c7ec3c23`, `1f8f001a`, `752a50a3`.** As above. The removed arm of
  `released_drift` (`752a50a3`) was the `any(status == "OK")` skip, now
  `view.held`.
- **🟡 3, `01082c4f`.** The LEFT text, `FROZEN_REPAIR` and the home all say the
  correction carries every coordinate the claim still rests on. Pinned by
  `test_a_moved_released_row_is_told_its_correction_carries_every_coordinate`,
  red at `f50f5f05` (executed).
- **🟡 4, `c730be61`.** Built as round 1's paste. The notice is right while
  both rows are fragments. Once both have folded, nothing clears it (🟡 11).
- **🟡 5, `fe6b06f6`.** `CITATION` is tried before `ANCHOR`. M2 re-run: all
  1,083 citations read back through `corrections()`, and all 12 `Corrected ·`
  rows in the tree are keyed on the citation the checker reads (executed).
- **🟡 6, `5604b390`.** Row 25 is a `Corrected ·` row whose claim holds against
  `check_text` (per-file `seen`) and `family_view` (per-row `seen` only). No
  other row cites the 0.4.0 row, so no `Re-read ·` row is left inside a
  superseded family (read).
- **🟡 7, `f4b1d18e`.** The §3 row names `--into` with a fold fragment and the
  second fold that joins it. A fragment with no `seal/specs/` directory folds
  (L7), and an added release file passes the freeze (read).
- **⬜ 8, `2f01c24b`.** Qualified in the home and in spec §*Grounding* (read).
- **⬜ 9, `c4b06aae`.** The fallback names R1 in round 1's shape. Its comment
  claims more than the match tests (⬜ 14).

The ledger, read: row 25 as above. L1, L3, L4 and L5 now state the fixed
behaviour, and each claim matches the code it cites. The three re-stamped
rows still hold. R5 (0.12.1) is about `tracked_text_files`, and P3 (0.15.1) is
about §3's suite line, `bin/test -q`; neither is touched by the §3 drift row.
C2 (0.16.0) is about the overflow rule, which §*A row is a content anchor*
still states at its line 46. The `survivors.md` row keeps the overview's ✅
question, and its grounds are right. `--strict` at HEAD: 3,786 ok, 0 drifted
(executed).

## Stage 2 — the units the fixes created

### 🟡 10 — the home and the changelog say no unread pair is ever accepted, and S6 accepts one

`docs/the-evidence-ledger.md:111-112`,
`seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/changelog.md:20-21`,
`skills/evidence-check/scripts/evidence_check.py:2004-2005`.

The home says the cost "is the price of never accepting a pair of hashes no
reading saw together". The changelog says such a pair "is never accepted", and
the code comment says the same. The rule is per coordinate, so that holds only
when one row recorded every coordinate. Executed:

1. R records `handler@h1` and `other@o1`.
2. Branch A edits `handler` and re-reads it as h2. Branch B edits `other` and
   re-reads it as o2, on another day.
3. After the merge the code is at (h2, o2), and `--strict` exits 0, 6 OK.

Nobody read (h2, o2) together. That is S6, the case the rule was built to
pass, and the halves rule's own premise: each side vouches for the unit it
edited. A same-day tie does the same with both coordinates on both rows:
readings (h2, o1) and (h1, o2), code at (h2, o2), exit 0.

Why it matters: round 1's 🟡 2 was this same paragraph stating a cost the code
does not have. The fix moved the false sentence from the cost to the
guarantee, and the changelog carries it into the release notes. What the rule
buys is narrower: a coordinate is held to its newest reading, so a revert to
content a newer reading superseded is caught.

The changelog entry also says nothing of the double-correction notice, a new
DRIFTED a person will see. The fix below adds one sentence for it.

### 🟡 11 — once two corrections of one row have folded, the notice is permanent

`skills/evidence-check/scripts/evidence_check.py:2400-2418`,
`docs/the-evidence-ledger.md:118-122`.

The home's repair is "one row merging the two", and that row is written in a
fragment before the fold. CI's ledger job is lenient, so two sibling branches
that each correct one row can both land and fold, and nothing red stands in
the way. After that, both correcting rows sit in a frozen file. Executed:

1. R in `0.1.0.md`; C1 and C2, both correcting R, in `0.2.0.md`.
2. `--strict` exits 2, each correcting row named DRIFTED, "corrected by 2 rows".
3. A fragment row C3, `Corrected ·` citing C2, retires it. `--strict` still
   exits 2 with the same two lines, and `--reverify --into` writes nothing and
   exits 0.

`corrected_by` counts every row whose parent's root is R, including one that
a later correction superseded, so there is no row a person can write that
clears it. The repository's `--strict` then stays red for every later sealer.
With the fix below, applied in the clone, step 3 exits 0 with 5 ok, and the
four ledger modules pass (186 cases).

### 🟡 12 — a narrowed `--reverify` names nothing while the family reads DRIFTED

`skills/evidence-check/scripts/evidence_check.py:3190-3207` (`released_drift`).

The new comment says an older released reading that matches "names nothing a
re-read must cover", because "a newest reading in a fragment was re-stamped in
place before this view was read". The re-stamp runs over `writable`, which is
the fragments among `ledgers`. The home tells a person to narrow the write
with `--ledger` to the files read. A person who re-read released R passes the
release file, and then no fragment is re-stamped. Executed, under the freeze:

1. R records `handler@h1` on 2026-01-01. A fragment re-read records h2 on
   2026-02-01. The code goes back to h1.
2. `--strict` exits 2: the fragment reading is DRIFTED, and R "matches only
   the reading of 2026-01-01".
3. `--reverify --into … --checked 2026-03-01 --ledger seal/releases/0.1.0.md .`
   prints `0 citing rows written · 0 released rows left` and exits 0. Plain
   `--reverify --ledger …` does the same.
4. `--strict` still exits 2.

Before the fix pass this family read OK, so the silence is new with the rule.
With the fix below, step 3 writes one row and step 4 exits 0 (executed in the
clone). Unnarrowed, nothing changes: after the in-place re-stamp the
fragment's newest reading holds, and `view.held` skips the coordinate before
the new line is reached.

### ⬜ 13 — a `Checked` date the calendar does not have outranks every later reading

`skills/evidence-check/scripts/evidence_check.py:2428-2435` (`checked`).

A date cell used to decide nothing, so nothing validated it. Now it orders
readings, and `checked` compares the `CHECKED_RE` match as a string. Executed:
a released row dated `2026-13-45`, its unit edited, `--into --checked
2026-03-01` prints `1 citing row written · 0 left`, and `--strict` still
reports DRIFTED, naming the newest reading as 2026-13-45. The corpus holds no
such date, and the message names the bad date, so a person can see it. It
matters for a fragment that folds with a typo. With the fix below, the same
run reads 0 drifted (executed in the clone).

### ⬜ 14 — the whole-cell fallback's comment says no other cell begins a line, and the match does not test where a cell begins

`skills/evidence-check/scripts/evidence_check.py:2186-2193` (`unique_literal`).

`literal_statements` matches a substring after collapsing whitespace. So
`| R1 · handler adds one |` is found on R2's line when R2 has a cell exactly
equal to R1's first cell, and `citation_for` returns None (executed). Round
1's shape (`see R1 · …`) is covered. Anchoring the match at the line start
would not help on its own, because `cited_row` resolves through the same
substring search, so the fix is the comment.

### ⬜ 15 — the test module's docstring still states the plain union

`tests/test_a_released_row_is_read_again_in_a_fragment.py:16`. S1 reads "a
coordinate is OK when any reading in R's family recorded what it holds". Every
other carrier of the rule was updated (the search covered the docs, the
script's help and comments, the spec, the changelog and the ledger).

## Regression tests to plant

Each case below was seen red at `30369bde` by the probe named in §*Executed
probes*, and green with its fix applied in the clone.

```text
tests/test_a_released_row_is_read_again_in_a_fragment.py
  1. two folded corrections of one row, one retired by a third correction,    (🟡 11)
     read clean
  2. --reverify --into narrowed to the released file writes the re-read a     (🟡 12)
     family drifted by a fragment's newer reading owes
  3. a Checked cell that is not a calendar date does not outrank a re-read    (⬜ 13)
```

## Facts for the evidence ledger

- The newest-date rule is per coordinate. Readings of different units written
  by different rows combine into a pair no reading recorded, and the checker
  reads it OK (executed, P1).
- Folding this release's fragments changes no verdict: 3,786 ok, 0 drifted
  before and after at `30369bde`; 3,991 ok, 0 drifted with the three siblings
  merged and the second lander's re-stamp applied (executed).
- The second lander re-stamps 7 rows, 8 hashes: 6 in this work item's
  fragment, 1 in #718's (executed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking finding is closed — `--into` slices the line the match was made on | `skills/evidence-check/scripts/evidence_check.py:3267` | confirmed | closed at `d971ba27`; executed: its case red at `f50f5f05`, green at HEAD |
| 🟢 | round 1's finding 2 is closed — only the newest-dated readings of a coordinate count, ties a union, as the orchestrator decided | `skills/evidence-check/scripts/evidence_check.py:2428` | confirmed | closed at `c7ec3c23`, `1f8f001a`, `752a50a3`; executed: P1 red at `f50f5f05`; the tie case red with the tie removed |
| 🟢 | round 1's finding 3 is closed — the repair says the correction carries every coordinate | `skills/evidence-check/scripts/evidence_check.py:3285` | confirmed | closed at `01082c4f`; executed: its case red at `f50f5f05` |
| 🟢 | round 1's finding 4 is closed — two corrections of one fragment-stage row are named | `skills/evidence-check/scripts/evidence_check.py:2400` | confirmed | closed at `c730be61`; executed: red at `f50f5f05`; the folded case is new finding 11 |
| 🟢 | round 1's finding 5 is closed — a closing-pipe citation is keyed by the citation | `skills/evidence-check/scripts/correction_check.py:579` | confirmed | closed at `fe6b06f6`; executed: both cases red at `f50f5f05`; M2 1,083 rows, 0 misread; 12 of 12 tree rows keyed right |
| 🟢 | round 1's finding 6 is closed — row 25 is a `Corrected ·` row whose claim holds | `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md:25` | confirmed | answered at `5604b390`; read against `check_text` and `family_view`; no other row cites the 0.4.0 row |
| 🟢 | round 1's finding 7 is closed — the §3 drift row names `--into` and the second fold | `docs/release-checklist.md:199` | confirmed | closed at `f4b1d18e`; executed: its case red at `f50f5f05`; read against `fold_ledger.py` and the freeze |
| 🟢 | round 1's finding 8 is closed — REMOVED-not-re-pointed is qualified for the freeze | `docs/the-evidence-ledger.md:37` | confirmed | closed at `2f01c24b`; read |
| 🟢 | round 1's finding 9 is closed — the whole-cell fallback names R1 in round 1's shape | `skills/evidence-check/scripts/evidence_check.py:2186` | confirmed | closed at `c4b06aae`; executed: its case red at `f50f5f05`; the comment is new finding 14 |
| 🟡 10 | the home, the changelog and the code comment say no pair of hashes nobody read together is accepted; S6 and a same-day tie accept one | `docs/the-evidence-ledger.md:111`, `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/changelog.md:20`, `skills/evidence-check/scripts/evidence_check.py:2004` | open | executed: (h2, o2) from two rows reads 6 OK, exit 0; the tie reads 8 OK, exit 0 |
| 🟡 11 | once two corrections of one row have folded, the notice cannot be cleared: a third correction retiring one leaves both named | `skills/evidence-check/scripts/evidence_check.py:2404` | open | executed: exit 2 before and after the retiring row; exit 0 with the fix in the clone |
| 🟡 12 | `--reverify` narrowed with `--ledger` to a released file reports nothing owed while the family reads DRIFTED | `skills/evidence-check/scripts/evidence_check.py:3195` | open | executed: `0 written · 0 left`, exit 0, strict exit 2 after; with the fix 1 written, strict exit 0 |
| ⬜ 13 | a `Checked` date the calendar does not have outranks every later reading | `skills/evidence-check/scripts/evidence_check.py:2435` | open | executed: `2026-13-45` outranks the `--into` row it reported written |
| ⬜ 14 | the whole-cell fallback's comment claims a line-start property the substring match does not test | `skills/evidence-check/scripts/evidence_check.py:2186` | open | executed: R2 with a cell equal to R1's first cell, `citation_for` → None |
| ⬜ 15 | the test module's docstring still states the plain union | `tests/test_a_released_row_is_read_again_in_a_fragment.py:16` | open | read |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the three touched ledger modules at HEAD | 183 passed |
| `bin/test` on the S6/S7 module, the docs line-wrap module and the one-home module at HEAD | 42 passed |
| the same three touched modules with the four source files at `f50f5f05` | 9 failed (every case the fix pass planted), 174 passed |
| the tie removed from `family_view` (first newest reading only) | the tie case red; S6 and S7 green |
| `evidence_check.py --strict .` at HEAD | 3,786 ok, 0 drifted, exit 0 |
| M2 at HEAD: `citation_for` → fragment row → `ANCHOR_RE` → `cited_row`, and `corrections()` | 1,083 rows, 0 without a citation, 0 wrong rows, 0 misread, 0 fallback of either kind |
| `corrections()` against `ANCHOR_RE` on every `Corrected ·` row in the tree | 12 of 12 keyed on the citation |
| date scan of every anchored ledger row | 1,146 rows: 0 without a date, 0 invalid, 0 after 2026-10-03 |
| sibling merges (#647, #718, #716, all three) into `30369bde`, then `--strict` and `correction-check --range` | 0 conflicts; drifted 6, 3, 0, 9; correction-check exit 0, each exempt |
| the second lander's repair in the all-three merge: `--reverify --into <this fragment> --checked 2026-10-03` | 8 hashes on 7 rows re-stamped, 0 written, 0 left; ledger 0 drifted; records arm 4 refused (#647's records name a removed unit) |
| `fold_ledger.py --version 0.18.0` at HEAD, then `--strict` | 3,786 ok, 0 drifted |
| the same fold over the all-three merge with the repair applied | 4 fragments folded; 3,991 ok, 0 drifted, exit 0 |
| P1: two rows each re-reading one unit; then a same-day tie (🟡 10) | exit 0, 6 OK; exit 0, 8 OK |
| P2: two corrections folded, then a third retiring one (🟡 11) | exit 2, exit 2; `--into` 0 written, exit 0; with the fix: exit 2, exit 0 |
| P3: a fragment's newer reading, code reverted, `--reverify` narrowed to the release file (🟡 12) | strict exit 2; `0 written · 0 left`, exit 0; strict exit 2; with the fix: 1 written, strict exit 0 |
| P4: a released row dated `2026-13-45` (⬜ 13) | `--into` 1 written, strict exit 2; with the fix: exit 0 |
| P5: R2 with a cell equal to R1's first cell (⬜ 14) | `citation_for` → None |
| the four ledger modules with the fixes for 11, 12 and 13 applied in the clone | 186 passed |
| the broad gate (full suite, repository lint, typecheck) | not yet — the sealer's, once the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the second lander re-stamps 7 rows (6 of this fragment, 1 of #718's) and clears #647's 4 records-arm refusals of a unit this branch removed | the handoff to whichever of #647, #718 and #715 lands second | the orchestrator of the 0.18.0 run |

## Paste-ready fixes

### 🟡 10

`docs/the-evidence-ledger.md`, replacing the two sentences from "The cost is a
re-read" to the end of the paragraph:

```markdown
against it. The cost is a re-read, never a question. What it buys is that a
coordinate is held to its newest reading, so a revert to content a newer
reading superseded is caught. Coordinates are still judged one at a time, as
the halves rule judges units: two branches re-reading different units of one
row leave a pair no single reading recorded, and it reads OK, because each
side read the unit it edited. A same-day pair of readings from two branches is
a union, so a revert to either reads OK.
```

`seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/changelog.md`,
the entry's middle:

```markdown
  of them recorded what the code holds now, and DRIFTED when none did. Two
  branches that edited the same unit still leave the row DRIFTED, and code
  reverted to a hash only a superseded reading recorded reads DRIFTED too.
  A `Corrected ·` row supersedes the row it cites, and a released row
  corrected by two or more rows names each of them DRIFTED until one claim
  is kept.
```

`skills/evidence-check/scripts/evidence_check.py`, the comment above
`CITING_VERBS`:

```python
# neither matches and the row is DRIFTED. The cost: content back at a hash
# only an older reading recorded reads DRIFTED, a partial revert and a whole
# one alike, and costs a re-read, never a question. Coordinates are still
# judged one at a time, so readings of two units on two rows combine into a
# pair neither row recorded (round 1, 🟡 2; round 2, 🟡 10). A `Corrected ·` row supersedes
```

### 🟡 11

```python
# skills/evidence-check/scripts/evidence_check.py, family_view
    for keys in corrected_by.values():
        # A correcting row a later `Corrected ·` row supersedes is no longer
        # a claim: that later row is the repair once both have folded, where
        # neither can be edited (round 2, 🟡 11).
        keys = [k for k in keys if k not in superseded]
        if len(keys) < 2:
            continue
```

```markdown
read them together and keep one claim. The second branch cannot cite the
first one's row before the fold, so the repair is one row merging the two.
Once both have folded, a `Corrected ·` row citing one of them retires it.
```

```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py
def test_a_folded_double_correction_is_cleared_by_retiring_one(repo):
    """Both corrections folded, so neither can be edited: a third
    `Corrected ·` row citing one of them retires it, and the notice goes
    (round 2, 🟡 11)."""
    h = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"],
    )
    cite = citation(r, "R1 · handler adds one")
    sec = "### 2000000001-a-later-item"
    c1, c2 = (
        f"| Corrected · handler adds {n} | `{cite}`, `src/service.py#handler@{h}` "
        "| read | 2026-02-01 | Corrected 2026-02-01 |"
        for n in ("two", "three")
    )
    released(repo, [c1, c2], version="0.2.0", section=sec)
    frozen(repo, "0")
    assert run(["--strict", "."], repo).returncode == 2
    retire = citation(c2, "Corrected · handler adds three", version="0.2.0", section=sec)
    fragment(
        repo,
        [
            f"| Corrected · handler adds two, as the other row says | `{retire}`, "
            f"`src/service.py#handler@{h}` | read | 2026-03-01 | Corrected 2026-03-01 |"
        ],
        name="3000000001-y",
    )
    out = run(["--strict", "."], repo)
    assert out.returncode == 0, out.stdout
```

### 🟡 12

```python
# skills/evidence-check/scripts/evidence_check.py, released_drift
            for key, m, status, detail in graded:
                if ledger_kind(root, view.files[key[0]][0]) != "released":
                    continue
                if status == "BROKEN":
                    broken.append((where(key), coord, detail))
                    break
                # DRIFTED, or OK and outranked by a newer reading holding
                # other content: the family owes a re-read either way. That
                # newer reading may sit in a fragment LEDGERS left out, which
                # nothing re-stamped (round 2, 🟡 12).
                drifted.setdefault(top, {}).setdefault(coord, m)
                break
```

```python
# tests/test_a_released_row_is_read_again_in_a_fragment.py
def test_a_narrowed_into_re_reads_a_family_a_fragment_outranks(repo):
    """The newest reading sits in a fragment `--ledger` leaves out, so no
    in-place re-stamp reaches it: `--into` still owes the released row a
    re-read (round 2, 🟡 12)."""
    h1 = unit_hash(repo, "src/service.py", "handler")
    (r,) = released(
        repo,
        [f"| R1 · handler adds one | `src/service.py#handler@{h1}` | read | 2026-01-01 | |"],
    )
    edit_handler(repo)
    h2 = unit_hash(repo, "src/service.py", "handler")
    fragment(
        repo,
        [
            f"| Re-read · R1 · handler adds one | `{citation(r, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{h2}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
        name="2000000009-z",
    )
    frozen(repo, "0")
    (repo / "src" / "service.py").write_text(SERVICE)
    assert run(["--strict", "."], repo).returncode == 2
    out = run(
        ["--reverify", "--into", INTO, "--checked", "2026-03-01",
         "--ledger", "seal/releases/0.1.0.md", "."],
        repo,
    )
    assert "1 citing row written" in out.stdout, out.stdout
    assert run(["--strict", "."], repo).returncode == 0
```

### ⬜ 13

```python
# skills/evidence-check/scripts/evidence_check.py, beside date_column
def calendar_date(text):
    """Whether TEXT, a `CHECKED_RE` match, is a date the calendar has: a
    `2026-13-45` would otherwise outrank every reading after it (round 2)."""
    try:
        datetime.date.fromisoformat(text)
    except ValueError:
        return False
    return True


# family_view, checked
        found = CHECKED_RE.findall(cells[column[0]]) if column else []
        return max((d for d in found if calendar_date(d)), default="")
```

### ⬜ 14

```python
    # The cell whole, with both of its pipes: it names the row where no
    # other line holds that run, which covers a first cell that also ends
    # another row's last cell (round 1, ⬜ 9). The match is a substring, as
    # `cited_row` resolves it, so a cell exactly equal to another row's cell
    # still names no row.
```

### ⬜ 15

```text
  S1  a coordinate is OK when one of its newest readings in R's family -- the
      members recording it with the newest `Checked` date, ties together --
      recorded what it holds
```

Needs a fix: yes — 🟡 10 (the home, the changelog and a comment state a guarantee the per-coordinate rule does not give), 🟡 11 (a folded double correction cannot be cleared), 🟡 12 (a narrowed `--reverify` names nothing owed while the family reads DRIFTED)

Loses a record or crashes: no

## Proof block

Opened in this round, at `30369bde` unless marked:

- `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/`: `rounds/round-1.md`, `rounds/round-1-report.md`, and the fix range's diffs of `spec.md`, `overview.md`, `changelog.md`, `survivors.md`
- `seal/ledger/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes.md`: the fix range's word diff; rows 1–10, 25, 39, 43, 45, 57, 62 in full
- `seal/releases/0.12.1.md:26`, `seal/releases/0.15.1.md:22`, `seal/releases/0.16.0.md:22`
- `skills/evidence-check/scripts/evidence_check.py`: the fix range's diff; `literal_statements`, `unique_literal`, `citation_for`, `cited_row`, `family_view` whole, `date_column`, `checked_refusal`, `reverify` (head), `released_drift`, `reverify_into`, the `--reverify` branch of `main`, `check_ledger`, `check_text`, `classify` (head), `ANCHOR_RE`, `HEADING_SEP`
- `skills/evidence-check/scripts/correction_check.py`: the fix range's diff, `ANCHOR`, `corrections`, `dropped_corrections`
- `skills/code-review/scripts/chain_check.py`: `CLOSED_WORDS`
- `hooks/evidence-advisor.py`, `docs/release-checklist.md`, `docs/the-evidence-ledger.md`: the fix range's diffs; `docs/the-evidence-ledger.md:96-137` and §*A row is a content anchor*
- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: lines 1-140, 650-658, 921-1180; the fix range's diffs of `tests/test_a_merge_cannot_silently_drop_a_correction.py` and `tests/test_the_ledger_fragments_fold_at_release.py`
- `bin/test`
