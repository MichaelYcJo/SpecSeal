# Round 1 report — warden

| Field | Value |
|---|---|
| Work item | 1790835050-the-delegated-note-compares-what-it-prints (#701, draft PR #711) |
| Target SHA | 7d96a67bd7b3e3981464977f8214694e2184274b |
| Base | `release/v0.17.0` at `e83db346` |
| Diff | `e83db346..7d96a67b`, six commits: routing, frame, fix and case, phase 1 record, records, phase 2 record |
| Clone | a `git clone --no-local` under the session scratchpad, `<scratchpad>/1790835050/round-1/clone`, removed at the end of the round |
| Ran by | specseal:warden on Opus 5.5 |

This is the first round, so there is no earlier record to inherit. I read
the frame (`spec.md`, `plan.md`, `questions.md`), both phase records,
`overview.md`, the changelog fragment, the ledger fragment and the seven
re-stamped rows as claims. Each claim below was checked against the code or
by execution, and the label on each says which.

**Stage 1, spec compliance: the work does what the frame asks.** S1, S2, S3,
S4, S5 and S7 hold by execution. S6 holds by reading. No 🔴 and no 🟡 were
opened. Two ⬜ remain. One is a pre-existing defect in the function this
work touched, and the other is a gap in the framer's guidance that made the
build edit the frame.

## 1. The decision against what the column prints

The comparison is `round(delegated_max / 60, 1) < 1.0` at
`skills/verify/scripts/session_cost.py:2225`. The column prints the same
value through `minutes` (`:1970`), which is `f"{seconds / 60:.1f}m"`, at
`:2257`. `delegated_max` is the largest of the values the column prints, and
formatting is monotone. So the note is absent exactly when the column's
largest cell reads `1.0m` or more, provided `round(x, 1)` and `.1f` agree on
every double.

**They agree on every interpreter I could run (executed).** I compared
`round(x / 60, 1)` with `float(f"{x / 60:.1f}")` and the note decision with
the printed cell on six interpreters: CPython 3.9.6, 3.11.13, 3.12.9, 3.12.12,
3.13.9 and 3.14.4, all on macOS aarch64. The inputs were 200,000 consecutive
doubles each way from 57.0 (`math.nextafter`), a 0.0001-step sweep from 0 to
13 s, one million uniform values in 0–600 s, and the exact ties `60 × (k/10 +
0.05)`. Every interpreter returned zero disagreements. 57.0 gives `0.9` on
both functions and the next double above it, `57.00000000000001`, gives `1.0`
on both. So the band is (57.0, 60) at double resolution, as the frame, the
code comment and D1 say.

The suite's CI legs run 3.12 on Ubuntu, macOS and Windows
(`.github/workflows/test.yml:39-41`). The build measured 3.13.9 and 3.14.4
only, so 3.12 is the interpreter `questions.md` Q1 was actually about. This
round closes it on macOS. The Ubuntu and Windows legs are the pull request's
CI run, as `overview.md` §*Not verified* already says. From reading: both
functions go through CPython's own correctly rounded dtoa (mode 3), and that
code does not depend on the platform's C library, so I expect no leg to
differ.

**At every boundary, through the real script (executed).** I rendered the
`--spawns` page at the target and at the base for single spawns paired in
56.9, 57.0, 57.001, 59.6, 59.99 and 60.0 s:

| Paired in | Cell | Note at the target | Note at the base |
|---|---|---|---|
| 56.9 s, 57.0 s | `0.9m` | printed | printed |
| 57.001 s, 59.6 s, 59.99 s | `1.0m` | absent | printed, contradicting the cell |
| 60.0 s | `1.0m` | absent | absent |

No value left a note beside a `1.0m` cell at the target. A two-spawn run
with the 59.6 s spawn in the second cycle also prints no note. A transcript
stamp of 57.00000000000001 s serialises to 57.0, so the page shows `0.9m`
and the note there, which is consistent.

The note's seconds figure is `.0f` and is at most `57s` once the decision
follows the column. Next to `0.9m` it does not contradict the cell, because
`0.9m` is rounded. The frame's *Out* list reasons the same way.

## 2. The class sweep

I re-derived the sweep rather than inheriting it. An `ast` walk of every
`<`, `>`, `<=`, `>=` comparison in `session_cost.py` at the target returns 33
sites (executed). Each one is either in `spec.md` §*The class, swept* at its
base line number, or among the length and count sites `phases/phase-1.md`
names (`:412`, `:592`, `:1157`, `:1425-1426`, `:2402`, `:2899`, `:3207`, base
numbering), or a loop bound (`:261`, `:324`). None is a value compared
against a threshold that the page prints rounded, apart from the four the
sweep names.

**Leaving `:2115` (`tools_per_turn <= 1.0`) is justified (read).** The ratio
is `len(calls) / max(len(turns), 1)` (`:1171`). A turn that sent a call sent
at least one, so the ratio is never below 1.0 when there are calls. The
*one at a time* sentence is therefore chosen only at exactly 1.0, where it
is true. Every ratio in (1.0, 1.005) prints `1.00` with *most turns send a
single call*, and that is true of the data and does not contradict `1.00`.
Rounding the comparison would print *one at a time* over a run where one
turn sent two calls.

**The sweep beyond this module (read).** Contract §12 asks for the class,
and the ticket bounded it to this module. I also grepped the other shipped
scripts for a rounded print beside a threshold. `hooks/worktree-guard.py`'s
`_age` prints `.0f` minutes. Its idle branch states `IDLE_MIN+ minutes` and
lists only sessions whose every signal is at least `IDLE_MIN`, so every age
it prints is at least the number it states. The active branch does not print
the threshold. `survivor_check.py` prints a score `.2f` and drops any score
under its floor without printing the floor. `mutation_check.py` prints an
elapsed time and compares nothing against it. No sibling instance turned up.

## 3. The case

`test_the_delegated_note_follows_the_minute_the_column_prints`
(`tests/test_session_cost.py:2661`) and its helper `delegated_cells`
(`:2638`).

- **Red on the defect (executed).** With the base `session_cost.py` checked
  out in the clone, the case fails with exit 1 at `assert "never reaches a
  minute" not in out` (`:2681`). The cell assertion above it passes. After
  the restore the clone was clean.
- **Green at the target (executed).** It passes with the module's other
  delegated cases (4 passed), and inside the full module together with the
  int-guard module (192 passed).
- **Near-misses.** The 57.0 s half asserts both `0.9m` and *57s at most*, so
  it is red under any comparison that drops the note at the floor. It also
  goes red if `minutes` changes precision, because the cell would read
  `0.95m`. I did not re-run the build's seven mutations. The table in §1 is
  my own execution of the decision at both edges.
- **Could it pass for the wrong reason?** Not on these fixtures. The helper
  reads exactly the 11-wide right-aligned slice under `delegated`, skips the
  empty head row and the `—` tail cell, and compares the whole list. A
  missing header raises `StopIteration` and fails the case. A page-wide
  search would have matched the `span` cell's `1.0m`, so reading by column
  is the right choice. **There is one limit, measured:** a row label longer
  than 30 characters shifts that row's cells right. The helper then reads
  the `model` cell (`0.0m`) where the `delegated` cell is `1.0m`. The
  fixtures use `specseal:smith`, so the case is sound, but the helper's
  docstring claims more than holds. The cause is finding ⬜ 1.

## 4. The records

- **`evidence-check .`, unscoped (executed).** Exit 0, `3312 ok · 0 drifted ·
  0 broken`. The records arm reports `5 work items read · 0 refused`.
  `--strict` also exits 0. `correction-check --range e83db346...7d96a67b`
  exits 0 (no merge commit). `ruff check` and `ruff format --check` over the
  two touched code files exit 0.
- **The seven re-stamped rows (read).** I paired each removed line with its
  added line. In all seven, the only changes are the hash `15595f59` →
  `cd336642`, a `· 2026-10-01` on the `Checked` cell where it was not
  already that date (rows 16 and 45 already were), and one appended `Re-read
  2026-10-01 by work item 1790835050 (#701)` sentence. No claim cell
  changed, and none needed to. Each note names the part of `report_spawns`
  its claim rests on, and I checked that the part is untouched at
  `:2156-2339`. Row 13 of `seal/releases/0.9.5.md` keeps its older sentence
  *the `delegated_max < 60` block … untouched*. The note appended after it
  says that sentence no longer describes the block. That keeps the history
  of notes intact, and the claim itself is still true. Row 50 of
  `seal/releases/0.11.3.md` says the edit changes an existing `--spawns`
  reading but not through anything the `--segments` mode adds. That is
  accurate, and the claim holds.
- **The build's edit of the frame (executed and read).** Commit `8fb65924`
  changed one line of `spec.md` (`:32`) and one of `plan.md` (`:61`). Each
  went from a stamp of `report_spawns` under the bare file name at hash
  `15595f59` to the full path with no stamp, plus the words *at hash
  `15595f59` when framed*. I restored the
  framed `spec.md` in the clone and re-ran `evidence-check .`: exit 2,
  `BROKEN … spec.md:32 session_cost.py#report_spawns file not found`. So the
  edit was forced: without it, S5 cannot be met.
  The edit changes no scope item, acceptance row, grounding clause or
  verdict. The anchor argument in `agents/framer.md` §*Why the frame is not
  the builder's to draw* is that a builder bends the contract toward what it
  built, and this edit bends nothing. It is also disclosed in
  `phases/phase-2.md` and in `overview.md`'s divergence table. My judgment is
  that it is acceptable. The real gap is upstream: the framer stamped a unit
  its own work was going to drift, and nothing told it not to (⬜ 2).

### ⬜ 1 — a cycle label longer than its column shifts the whole row (pre-existing)

`skills/verify/scripts/session_cost.py:2145` (`cycle_label`), printed at
`:2248`, `:2253` and `:2339` with `<30` and never cut. A label such as
`cycle 1  vercel:performance-optimizer` (37 characters) pushes every cell
of its row seven columns right of its header. Executed: the probe page put
`1.0m` under `command`, and `delegated_cells` read `0.0m`. Any
`subagent_type` over 21 characters overflows. `segment_label` cuts to
`LABEL_WIDTH` (`:2345`), and its docstring says *the way every other label
here is cut*, but `cycle_label` is the label it does not cut. This predates
the branch, and the diff does not touch those lines. I record it rather than
open it, because a test helper in the diff relies on the alignment.

### ⬜ 2 — the framer is not told that a stamp of a unit its work drifts will be refused

`agents/framer.md` says nothing about writing a `path#unit@hash` stamp in
`spec.md` or `plan.md` for a unit the work will edit. Once the work item's
ledger fragment exists, the records arm reads those lines as live anchors.
The stamp then fails: as BROKEN under a bare file name, which is what
happened here, or as drifted under a full path once the build moves the
hash. Either way the builder has to edit the frame. That is the act the
framer/smith split exists to avoid, and every future work item that edits a
unit the ledger anchors will repeat it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | the note's decision agrees with the printed cell at every boundary, on six interpreters | `skills/verify/scripts/session_cost.py:2225` | confirmed | executed: zero disagreements between `round(x / 60, 1)` and `.1f` over about 1.4M values on 3.9, 3.11, 3.12 (two builds), 3.13 and 3.14; the page at 56.9, 57.0, 57.001, 59.6, 59.99 and 60.0 s never puts the note beside `1.0m`; the band is (57.0, 60) |
| 🟢 | the class sweep is complete, and leaving `:2115` is justified | `skills/verify/scripts/session_cost.py:2115` | confirmed | executed: an `ast` walk found 33 ordering comparisons, all accounted for; read: the ratio is never below 1.0, so *one at a time* is printed only at exactly 1.0 |
| 🟢 | the case is red on the defect and reads the right cell on its fixtures | `tests/test_session_cost.py:2661` | confirmed | executed: red at the base module (exit 1 at `:2681`), green at the target (4 and 192 passed) |
| 🟢 | the records hold: seven rows re-stamped with dated notes, and the frame edit was forced and neutral | `seal/releases/0.9.5.md:13` | confirmed | executed: `evidence-check .` exit 0 unscoped and `--strict`; the framed `spec.md` restored gives exit 2 at `spec.md:32`; read: no claim cell changed |
| ⬜ 1 | `cycle_label` is padded to 30 but never cut, so a long `subagent_type` shifts every cell of its row | `skills/verify/scripts/session_cost.py:2145` | open | executed: `cycle 1  vercel:performance-optimizer` put `1.0m` under `command`; predates the branch; fix it here or defer it as an issue, the smith's call |
| ⬜ 2 | the framer's definition does not warn against stamping a unit its own work will drift | `agents/framer.md:94` | open | executed: the framed `spec.md:32` stamp makes `evidence-check` exit 2 once the fragment exists; process guidance, not this branch's code |

## Executed probes

| What was run | Result |
|---|---|
| the module's delegated cases with the repository's test runner, `-k delegated`, at the target | 4 passed, exit 0 |
| the new case with the base `session_cost.py` checked out in the clone | 1 failed at `tests/test_session_cost.py:2681`, exit 1; restored, tree clean |
| the session-cost and int-guard test modules at the target | 192 passed, exit 0 |
| `evidence_check.py .` and `--strict .`, unscoped, at the target | exit 0 both; 3312 ok · 0 drifted · 0 broken; records 5 read · 0 refused |
| `evidence_check.py .` with the framed `spec.md` restored | exit 2; BROKEN at `spec.md:32`, the bare-file stamp |
| `correction_check.py --range e83db346...7d96a67b` | exit 0, no merge commit |
| ruff check and format check over the two touched code files | exit 0 both |
| round-versus-format agreement on six CPython builds | zero disagreements |
| the `--spawns` page at six durations, at the target and the base, plus a two-spawn run and a long label | as tabled in §1 and ⬜ 1 |
| the broad gate: full suite, repository-wide lint, typecheck | not yet — the sealer's, after the rounds settle |

## Paste-ready fixes

### ⬜ 1

```python
def cycle_label(row):
    """A slice's name in the printed table, cut to the column it is padded to.

    A cycle with no `subagent_type` still gets a name. The label is how a
    reader tells one row from the next, so `cycle 3  ?` is worth more than a
    row that reads as a blank. Cut from the right, as `segment_label` cuts a
    named agent: a label wider than `LABEL_WIDTH` pushes every cell of its
    row out from under its header."""
    if row["kind"] == "cycle":
        return f"cycle {row['cycle']}  {row['subagent_type'] or '?'}"[:LABEL_WIDTH]
    return row["kind"]
```

The three `:<30` paddings in `report_spawns` would then read
`:<{LABEL_WIDTH}`. A case with a 28-character `subagent_type` would assert
that `delegated_cells` reads the `delegated` cell.

### ⬜ 2

```markdown
**Name a unit your work will edit without a stamp.** Once the work item's
ledger fragment exists, `evidence-check`'s records arm reads every
`path#unit@hash` in `spec.md` and `plan.md` as a live anchor, and the build
moves that hash. Write the full path and give the hash in words — *at hash
`<hash>` when framed* — so the builder never has to edit your frame to pass
the check.
```

Needs a fix: no
Loses a record or crashes: no

Nothing this round opened needs a fix. The two ⬜ rows still read `open`,
so the record's `Pass` box stays unchecked until a fix pass answers or
defers each one. Once that happens, the broad gate comes due, and the next
step is spawning the sealer. Executed: `round_record.py new` over this
report in the clone wrote `Needs a fix | no` and `Loses a record or crashes |
no`, and left `Pass` unchecked.

## Proof block

Files opened, all at `7d96a67b` in the clone unless marked:
`skills/verify/scripts/session_cost.py` (`:1960-1980`, `:2010-2065`,
`:2090-2156`, `:2156-2345`, `:2380-2402`);
`tests/test_session_cost.py` (`:60-115`, `:2175-2240`, the diff hunk at
`:2638-2695`); the work item's `spec.md`, `plan.md`, `questions.md`,
`overview.md`, `changelog.md`, `phases/phase-1.md`, `phases/phase-2.md`;
`seal/ledger/1790835050-the-delegated-note-compares-what-it-prints.md`; the
diff of `seal/releases/0.9.5.md` and `seal/releases/0.11.3.md`;
`agents/smith.md` (`:38-66`); `agents/framer.md` (`:25-40`, `:100-115`);
`skills/evidence-check/scripts/evidence_check.py` (`:3137-3255`);
`skills/code-review/scripts/chain_check.py` (`:3925-3960`);
`skills/code-review/scripts/round_record.py` (`:2550-2575`);
`hooks/worktree-guard.py` (`:1268-1320`, `:1820-1840`, `:2245-2260`);
`.github/workflows/test.yml` (`:39-60`, `:125-140`); `bin/test`;
`seal/specs/1790815612-the-reading-segments-batch-again-and-the-opening-lives-in-a-file/rounds/round-3.md`
(row 🟡 10) and `round-3-report.md` (head).
