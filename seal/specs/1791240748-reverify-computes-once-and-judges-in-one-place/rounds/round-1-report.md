# Round 1 report — `--reverify` computes once and judges in one place

| Field | Value |
|---|---|
| Work item | 1791240748-reverify-computes-once-and-judges-in-one-place |
| Round | 1 |
| Target SHA | `ca46718589d5f06cd2525056c52736a40f5f5e80` |
| Base | `origin/release/v0.19.0` at `e6d5a055` |
| Ran by | specseal:warden on Opus 5.5 |
| Where it ran | a `git clone --no-local` of the branch at the target SHA, in the session scratchpad; the base script from a `git archive` of `e6d5a055` beside it |

## How the findings relate

The spec's six demands hold for code coordinates, and the differential the
build recorded holds when re-run. Four 🟡 sit at two places the rewrite
added, plus a third place it left out.

```
the fixed-point loop (on_a_cycle, the bound)
  ├─ 🟡 1  a row downstream of a cycle is left and named "does not settle"
  └─ 🟡 2  a pass that reaches its bound re-judges a whole file per round
one judge (#809's class)
  └─ 🟡 3  a citation is still read by two readers, and they disagree
the record (MOVES → pact changes)
  ├─ 🟡 4  a coordinate in another checkout is recorded as a BROKEN pact change
  └─ ⬜ 5  the record's row order follows the `--ledger` order
the paperwork
  └─ ⬜ 6  two `Re-read ·` rows vouch for sentences that describe walks
```

Findings 1 and 2 share one fix site, and 2's fence builds on 1's. Each 🟡
has a paste-ready fix and a case below. I applied all four fixes together in
the clone, and 832 cases of the eight touched modules passed. Each new case
failed at the target SHA.

## Findings

### 🟡 1 — A row downstream of a two-row cycle is left as "does not settle" when the cycle's members move on alternate rounds

`skills/evidence-check/scripts/evidence_check.py:3293`. `on_a_cycle` builds
its naming graph only over the keys whose verdict changed in the last round
before the bound (`moving`).

Take a cycle that one stale row starts: A quotes B's line and holds, B quotes
A's line at a stale hash. Only B moves in round 1. After that, A and B move on
alternate rounds, so one round's `moving` never holds both. The graph then
finds no cycle, and the fallback `or moving` pins every key moving in that
round. That set includes a row D that only names B and would have settled.

Which key is pinned depends on whether the bound is odd or even. The bound is
`len(dynamic) + 2`, so adding one coordinate that names an unrelated line of
another written ledger flips the result:

- With three dynamic coordinates, B is left and named, and D stays OK. This
  is correct.
- With four, A is left and named. D is also left at its old hash and named
  `does not settle`, the run exits 1, and `--strict` exits 2. One run could
  have re-stamped D, because B settles once A is left.

This breaks three statements:

- spec D1: *reaching it names the rows that still move and nothing else*;
- the docstring of `on_a_cycle`: *A coordinate downstream of such a cycle is
  not on it, and settles once the cycle is left where it stands*;
- this item's own `Corrected ·` row for E3
  (`seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:23`):
  *the rest are recomputed*.

The existing case `test_a_row_naming_one_that_never_settles_is_restamped`
covers only a self-quoting row, which moves every round. The two-row case
`test_of_two_rows_quoting_each_other_only_the_one_still_moved_is_named` also
misses it, because there both rows start stale and move together.

The fix reads the naming over every coordinate still judged and keeps
`moving` as the start set. In the clone, the case below failed at the target
SHA for the four-coordinate tree and passed with the fix for all three trees.
`tests/test_a_released_row_is_read_again_in_a_fragment.py` stayed at 449
passed.

### 🟡 2 — A row that never settles makes the run re-judge its whole file once per coordinate

`skills/evidence-check/scripts/evidence_check.py:3554`. The overview hands
this to the reviewer under *Not verified*: *the time a pass takes when it
reaches its bound*. I measured it.

A pass runs `len(dynamic) + 2` rounds before anything is pinned. A
self-quoting row changes its file every round, so every coordinate naming
that file is judged again in every round. That means rounds × coordinates
judgments, and each one parses a file whose size grows with the row count:

| Release rows, each with a fragment citation | No cycle | One self-quoting row added |
|---|---|---|
| 150 | 0.6 s | 11.7 s |
| 300 | 2.4 s | 93.6 s |
| 300, with the fence below | 2.7 s | 3.3 s |

Doubling the rows multiplied the time by eight, so a ledger of a thousand rows
would look like a hung process. The answer the run gives is correct; only the
time is the defect.

The base did not pay this. A self-quoting row is not a citation, so
`cited_first` walked its file once. The cost is new with the bound. NAME NOT IN TREE

The fix pins a key early, from the second round of a pass. It pins a key only
when the round rewrote that key's own row again and the key sits on a naming
cycle whose rows a re-stamp rewrites:

- **Why the rule is sound.** A key that moved changes its row. That change
  moves the next key on the cycle, and so on back to the first key, unless a
  row on the cycle is left whole for want of a date cell. Those rows are kept
  out of the graph.
- **Measured.** Counting `judge` calls on a 40-row tree gave 1,846 at the
  target SHA and 165 with the fix. The three modules that drive `reverify` hardest
  (the fragment module, the pact-change module and the row-points module)
  passed 800 of 800 cases.

### 🟡 3 — A citation is still read by two readers, and the two commands describe it differently

`skills/evidence-check/scripts/evidence_check.py:3509` and `:3534`. In
`--strict`, a citing row's citation is read by the family reader, `cited_row`
(`check_ledger` blanks the row from `check_text`). In `--reverify` the same
citation is a `Spot` that `judge` reads. The two readers disagree in two
shapes, both executed:

| Tree | `--strict` | `--reverify` |
|---|---|---|
| the citation's literal is on two lines of its section | BROKEN, *the literal is on 2 lines of its section, so it names no one row — lengthen it* | *the anchored statement is gone from … (3-6) — re-verify — left*, exit 0 |
| the citation's section heading is there twice | BROKEN, *the section it names is there 2 times* | nothing; `0 rows re-verified`, exit 0 |

The base behaves the same way, so the instance is old. This item still owns
it, for three reasons:

- spec §12's class table says *one coordinate judged by two implementations*
  is closed in full (*all: D2, D3*), and does not list this instance;
- #809's comment is exactly *the two commands describe one row
  differently*;
- this item's new `Corrected ·` row for `seal/releases/0.4.0.md:59`
  (`seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:41`)
  claims *`--reverify` … never contradicts the check's verdict, and never
  answers a flagged row with silence*. The second shape falsifies both
  halves.

The fix lets the family reader overrule `judge` for a citation it refuses, so
the `left` line carries the sentence `--strict` printed. Where the family
reader says OK or DRIFTED, nothing changes. Both shapes failed at the target
SHA and passed with the fix.

### 🟡 4 — A coordinate in another checkout, or one escaping the repository, is now recorded as a BROKEN pact change

`skills/evidence-check/scripts/evidence_check.py:3182`. `plan_ledger` hands
MOVES `(recorded, None)` for every coordinate it leaves, and
`record_pact_changes` writes each such part as BROKEN. The base wrote no part
for a coordinate it could not place: `walked(...)` then `continue`, with
nothing pending.

I ran a signatory tree with a `Pact` row, a `seal/parity.md` and a row citing
a pact clause beside one coordinate, through both scripts:

| Coordinate, at a made-up hash | `--strict` | base record | branch record |
|---|---|---|---|
| `legacy/src/x.py#f` (no such checkout given) | EXTERNAL | no row | one row, the coordinate `BROKEN` |
| `../outside.py#f` | BROKEN, *path escapes the repository* | no row | one row, the coordinate `BROKEN` |

The record is permanent and never edited by hand, and a pact review at the
pact's repository takes each row of it. `docs/the-pact.md` §*A signatory
records a pact change* defines the record's BROKEN as *where the re-read
leaves it because no one place holds it — its unit, its file or its quoted
statement gone*. A checkout the run was not given is none of those. Spec D5's
*`(recorded, None)` for each the run leaves* is broader than the policy
document, and the policy document outranks it.

The differential could not see this: no tree in the corpus puts such a
coordinate on a row citing a pact clause. The S7 case checks only that each
part matches what the file holds.

The fix gives no part to an EXTERNAL coordinate or one whose path escapes.
Both shapes failed at the target SHA and passed with the fix, and the
pact-change module passed in full.

A related shape is left to the smith. A ledger coordinate that does not
settle also hands MOVES a BROKEN part (`:3148`), and the same definition
does not cover it either. The fence leaves that branch as it is; the smith
can answer it with grounds or extend the guard.

### ⬜ 5 — The pact-change record's row order follows the order of `--ledger`

`skills/evidence-check/scripts/evidence_check.py:3599`. MOVES is extended
ledger by ledger in the order LEDGERS names them, and `record_pact_changes`
writes rows in that order.

- **Executed:** in `test_a_citation_restamp_is_not_a_pact_change`, the base
  and the branch wrote the record's two rows in opposite order.
- **Read:** with several `--ledger` arguments, the order of the arguments
  decides the order of the rows.

S4 says *any permutation of `--ledger` arguments writes the same bytes to
every file*, and the record is a file the run writes. No row's meaning
changes and the dedup reads per key, so the behaviour is right and only the
sentence overclaims. Neither the S4 case nor the S7 case builds a pact tree.

### ⬜ 6 — Two `Re-read ·` rows vouch for released sentences that describe walks

`seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:21`
re-reads E1 (`seal/releases/0.18.2.md`), whose claim ends *one move per
coordinate however many walks re-stamp it (#791)*. Line `:32` re-reads A4
(`seal/releases/0.18.3.md`), which says the run left a coordinate *by its own
last walk*.

Neither sentence is false after the rewrite, but both describe a mechanism
that no longer exists. Phase 3 rewrote the pact document's version of E1's
sentence for exactly that reason. A `Corrected ·` row, or a note in the
`Re-read ·` row, would keep the next reader from going to look for a walk.
This finding sits under `seal/ledger/`, so it is a correction and is out of
`Needs a fix`.

## What was checked and holds

- **One judge for code coordinates.** These callers all reach `judge`:
  `check_text` through `classify`, the family grade at `:2615`,
  `released_drift` at `:3897`, `reverify`'s static and dynamic verdicts at
  `:3509` and `:3534`, and `reverify_into` at `:4135` and `:4161`. No other
  caller reads a place with `resolve_unit` (read).
  `bin/evidence-check --strict .` at the target exits 0 (executed).
- **Code judged once from disk, ledger lines judged against the plan, one
  write.** Read in `reverify`: the static memo, `judged_against` swapping
  PLANNED per round, and one `put` per ledger after the loop. Executed through
  the differential's S2 and S4 cells.
- **#806 closed.** In S2 and six S4 orderings, the base exited 1 with B's
  coordinate left, and the branch exited 0 with it re-stamped (executed).
- **#809's cell C8 closed for code coordinates.** In three trees, the base
  recorded BROKEN or *no one place to hash*, and the branch re-stamped and
  recorded the move (executed). The citation instance is 🟡 3.
- **A row that never settles.** It is named on a `LEFT` line and the run
  exits 1, as S6 says (executed). The cases that misfire are 🟡 1 and 🟡 2.
- **The differential's classes.** Re-run over the nine modules that call
  `--reverify` through the script: 562 calls, 446 identical and 116
  different. 72 differ in `left` words only, and each new line is the check's
  sentence. 27 differ in order only, with the same exit, the same written
  bytes and the same set of lines. The build recorded 112 differences; the
  extra four come from cases planted after its probe ran (the re-point
  section case, the two cycle cases, one more words case). The 27 order-only
  differences were each read: hash lines and the dated list in file order
  instead of walk order. No behaviour hides there.
- **Probe 3.** Re-run at `1f4d6cfc` with both scripts in two archive copies.
  The two fragments are byte-identical at 46 rows, and the stdout is the same
  set of lines. Two `LEFT` lines for `seal/releases/0.18.2.md:90` changed
  position, where the phase record names `0.18.1.md:417`. It is the same
  copy-dependent inode order either way.
- **The narrowed run's reader.** `moved_and_left_out` reads every ledger
  coordinate of a left-out file against the plan and against the disk, names
  only OK→DRIFTED, and holds its line until the named file lands (read). S9
  is executed in the differential.
- **The eight `Corrected ·` rows.** Each was read against the released claim
  it replaces and against the code. Six hold. E3's row (`:23`) is false only
  through 🟡 1, and the 0.4.0 row (`:41`) only through 🟡 3. Both become
  true with those fixes. The choice of `0.18.1:417` over `0.18.0:24` is
  right: 417 already supersedes L4.
- **The 38 `Re-read ·` rows.** I sampled eight: E1, C1, A4, A6, W8, and three
  0.4.0 rows. All eight claims hold; two carry walk wording (⬜ 6).

## The account, claim by claim

| The account says | What I found |
|---|---|
| `overview.md`: D6 probe 2 found 112 `--reverify` differences, 0 unexplained | 116 at the target, every one classified; the extra four come from cases planted after the probe |
| `overview.md`: *within a round a verdict is reused where the file its coordinate names did not change, except a BROKEN one* | Holds; reuse is per target file, which is also why 🟡 2 re-judges a whole file per round |
| `phases/phase-2.md`: *at the bound only the coordinates on a cycle are left and the rest recomputed* | False for a cycle whose members move on alternate rounds (🟡 1) |
| `phases/phase-4.md`: probe 3's one position difference is the `LEFT` line for `0.18.1.md:417` | In my copies it was the two lines for `0.18.2.md:90`; the cause is the same inode order |
| `overview.md`, *Not verified*: the time a pass takes at its bound, answered by the reviewer | Measured (🟡 2) |
| spec §12: *one coordinate judged by two implementations*, all instances closed | The citation reader is an instance not listed (🟡 3) |

## Regression tests to plant

- `tests/test_a_released_row_is_read_again_in_a_fragment.py`: the downstream
  row of an alternating cycle (🟡 1), the judge-call count beside a row that
  never settles (🟡 2), and the citation the family reader refuses (🟡 3).
  The three cases are in the fences below.
- `tests/test_a_signatory_records_a_pact_change.py`: the coordinate no
  checkout places, which records no pact change (🟡 4).

Each failed at the target SHA in the clone. Each passed with its fix, and
with all four fixes applied together.

## Facts for the evidence ledger

None that this round verified and the fragment lacks. The measurement in
🟡 2 belongs in the fix's own row once the fix lands.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A row downstream of a cycle whose members move on alternate rounds is left and named does not settle; the result flips with an unrelated coordinate | `skills/evidence-check/scripts/evidence_check.py:3293` | open | Executed: the four-coordinate tree left D drifted with exit 1; spec D1, the docstring of on_a_cycle and the E3 Corrected row say a downstream row settles |
| 🟡 2 | A pass that reaches its bound re-judges every coordinate of the cycling file once per dynamic coordinate | `skills/evidence-check/scripts/evidence_check.py:3554` | open | Executed: 300 rows took 93.6 s with one self-quoting row and 2.4 s without; 3.3 s with the fix; 1,846 judge calls fell to 165 |
| 🟡 3 | A citation is read by the family reader in --strict and by judge in --reverify; they disagree on a duplicated literal and a duplicated section | `skills/evidence-check/scripts/evidence_check.py:3509` | open | Executed: BROKEN in --strict against a DRIFTED sentence or silence in --reverify; spec §12 claims the class closed; the 0.4.0 Corrected row at the fragment's line 41 is false |
| 🟡 4 | An EXTERNAL coordinate, or one escaping the repository, is recorded as a BROKEN pact change | `skills/evidence-check/scripts/evidence_check.py:3182` | open | Executed: the base recorded nothing and the branch records BROKEN; docs/the-pact.md defines BROKEN as unit, file or quoted statement gone |
| ⬜ 5 | The pact-change record's row order follows the --ledger order, which S4's sentence about every file does not allow | `skills/evidence-check/scripts/evidence_check.py:3599` | open | Executed in one tree (rows swapped against the base); read for the permutation; no row's meaning changes |
| ⬜ 6 | Two Re-read rows vouch for released sentences written in terms of walks (E1, A4) | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:21` | open | Records correction; the claims hold, the vocabulary names a removed mechanism |
| 🟢 | One judge reads every code coordinate for --strict, --reverify and --into | `skills/evidence-check/scripts/evidence_check.py:1669` | confirmed | Read: every caller found; executed: --strict . exits 0 at the target |
| 🟢 | #806 is closed: one run re-stamps a coordinate naming a line it moves, in any ledger order | `skills/evidence-check/scripts/evidence_check.py:3549` | confirmed | Executed: S2 and six S4 orderings, base exit 1, branch exit 0 |
| 🟢 | #809's cell C8 is closed for code coordinates, in place and under --into | `skills/evidence-check/scripts/evidence_check.py:1827` | confirmed | Executed: three trees, the move recorded where the base recorded BROKEN |
| 🟢 | A row that never settles is named on a LEFT line and the run exits 1 | `skills/evidence-check/scripts/evidence_check.py:3653` | confirmed | Executed in the differential and in the cycle probe |
| 🟢 | The differential's classes are what they are called, the 27 order-only differences included | `seal/specs/1791240748-reverify-computes-once-and-judges-in-one-place/phases/phase-2.md:80` | confirmed | Executed: re-run, 116 differences; the 4 beyond 112 come from later cases |
| 🟢 | Probe 3: both scripts write byte-identical fragments over this repository | `seal/specs/1791240748-reverify-computes-once-and-judges-in-one-place/phases/phase-4.md:21` | confirmed | Executed at 1f4d6cfc; 46 rows each; the same set of stdout lines |
| 🟢 | The eight Corrected choices match the claims they correct, apart from the two findings name | `seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md:19` | confirmed | Read: six hold; E3 at line 23 and 0.4.0 at line 41 turn true with the fixes for 1 and 3 |

## Executed probes

| What was run | Result |
|---|---|
| A two-row cycle started by one stale row, with a row D naming B, with 0, 1 and 2 unrelated coordinates naming a written ledger | At the target, the tree with one unrelated coordinate left D and named it does not settle, exit 1, --strict 2; with the fix for 🟡 1, all three trees named one row and re-stamped D |
| A release file of 150 and of 300 rows, each cited from a fragment, with and without one self-quoting row, unfrozen --reverify --checked | 0.6 s and 11.7 s; 2.4 s and 93.6 s; with the fix for 🟡 2, 2.7 s and 3.3 s |
| judge calls counted in-process, 40 rows and one self-quoting row | 1,846 at the target; 165 with the fix |
| Differential: every --reverify call of the script in nine modules, base script first in the same tree, tree restored, then the branch | 562 calls: 446 identical, 72 left words, 27 order only, 17 named cells (C8 3, #806 7, S6 family 3, S8 1, D4 1, re-point section 1, record row order 1) |
| A pact-citing row with an EXTERNAL coordinate and with an escaping one, through both scripts | Base: no record row; branch: one BROKEN row each |
| A fragment citation whose literal is on two lines, and whose section heading is there twice, through both scripts | --strict BROKEN both; --reverify says a DRIFTED sentence, or nothing, at exit 0, on both scripts |
| D6 probe 3 at 1f4d6cfc in two archive copies, base and branch scripts | Both exit 1; fragments byte-identical, 46 rows; the same set of stdout lines |
| bin/evidence-check --strict . at the target | exit 0 |
| All four fixes applied in the clone, the eight modules that drive --reverify plus the four new cases | 832 passed; each new case failed at the target SHA |
| Broad gate — the full suite, the repository-wide lint and the typecheck | not yet; the sealer's, after the rounds settle |

Needs a fix: yes — 🟡 1 (downstream row left on an alternating cycle), 🟡 2 (a pass at its bound costs rounds × coordinates), 🟡 3 (a citation read by two readers), 🟡 4 (EXTERNAL and escaping coordinates recorded as BROKEN pact changes)

Loses a record or crashes: no

## Paste-ready fixes

### 🟡 1 — `on_a_cycle` reads the naming over every coordinate still judged

Replace `on_a_cycle` in `skills/evidence-check/scripts/evidence_check.py`
(the `among` parameter is what 🟡 2's loop passes):

```python
def on_a_cycle(moving, spots, verdicts, among=None):
    """The keys of MOVING whose coordinate reaches itself (S6).

    MOVING is the coordinates whose verdict changed on the last round the
    bound allowed; SPOTS maps a key to its `Spot`, VERDICTS to the verdict
    that round gave it. A coordinate names the rows its verdict's region
    spans in its target file, and one whose naming leads back to its own row
    -- a row quoting its own line, or rows quoting each other -- has no
    hash the run can write that the write does not move again. A coordinate
    downstream of such a cycle is not on it, and settles once the cycle is
    left where it stands. AMONG, where given, is the keys the naming may
    pass through."""
    # The naming is read over every coordinate still judged, not over MOVING
    # alone: the members of a cycle one stale row starts move on alternate
    # rounds, so no single round's MOVING holds the whole cycle.
    live = [
        key
        for key in (spots if among is None else among)
        if verdicts.get(key) is not None
    ]
    names = {}
    for key in live:
        region = verdicts[key].region
        names[key] = [
            other
            for other in live
            if region is not None
            and spots[other].home == spots[key].target
            and region[0] <= spots[other].number <= region[1]
        ]
    found = set()
    for key in moving:
        if key not in names:
            continue
        stack, seen = list(names[key]), set()
        while stack:
            other = stack.pop()
            if other == key:
                found.add(key)
                break
            if other not in seen:
                seen.add(other)
                stack.extend(names[other])
    return found
```

The case, in `tests/test_a_released_row_is_read_again_in_a_fragment.py`:

```python
@pytest.mark.parametrize("unrelated", [0, 1, 2], ids=["none", "one", "two"])
def test_a_row_downstream_of_a_cycle_one_stale_row_starts_is_restamped(
    repo, unrelated
):
    """A quotes B's line and holds it; B quotes A's at a stale hash; D names
    B's line. Only B moves in the first round, so A and B move on alternate
    rounds and no one round's moving set holds both. One of A and B is left
    and named, and D, on no cycle, is re-stamped, however many unrelated
    coordinates name a written ledger. Red at ca467185 with one."""

    def names(label):
        return f'{R_FILE}#"{SECTION}">"\\| {label}"'

    b = f"| B · quotes A | `{names('A · quotes')}@0000beef` | read | 2026-01-01 | |"
    a = f"| A · quotes B | `{names('B · quotes')}@{line_hash(b)}` | read | 2026-01-01 | |"
    d = f"| D · names B | `{names('B · quotes')}@{line_hash(b)}` | read | 2026-01-01 | |"
    released(repo, [a, b, d])
    o = unit_hash(repo, "src/service.py", "other")
    rows = []
    for i in range(unrelated):
        z = f"| Z{i} · plain | `src/service.py#other@{o}` | read | 2026-01-01 | |"
        rows += [
            z,
            f'| E{i} · names Z | `seal/releases/0.2.0.md#"{SECTION}">"\\| Z{i} · '
            f'plain"@{line_hash(z)}` | read | 2026-01-01 | |',
        ]
    if rows:
        released(repo, rows, version="0.2.0")
    fix = run(["--reverify", "--checked", "2026-03-01", "."], repo)
    named = [line for line in fix.stdout.splitlines() if "does not settle" in line]
    assert len(named) == 1 and "D · names B" not in named[0], fix.stdout
    check = run(["--strict", "."], repo)
    drifted = [line for line in check.stdout.splitlines() if "DRIFTED" in line]
    assert len(drifted) == 1, check.stdout
```

### 🟡 2 — pin a coordinate on a cycle the round it rewrites its own row again

In `reverify`, replace the block from `texts = {ledger.home: ledger.text …}`
through `pinned |= on_a_cycle(moving, by_key, verdicts) or moving`
(depends on 🟡 1's `among`):

```python
    def rewrites(key):
        """Whether a re-stamp of KEY rewrites its row: not where `--checked`
        leaves the row whole for want of a date cell."""
        spot = by_key[key]
        header, cells = parsed[spot.key[0]].rows.get(spot.number, (None, []))
        return checked is None or (
            bool(cells) and date_column(header, cells) is not None
        )

    propagating = {key for key in by_key if rewrites(key)}
    texts = {ledger.home: ledger.text for ledger in parsed}
    pinned, earlier, changed = set(), {}, set(texts)
    while True:
        # Each pass is bounded, and a pass that reaches its bound leaves the
        # coordinates still moving on a cycle (`on_a_cycle`) and runs again
        # over the rest. A key once left stays left, so the passes end.
        moving, settled, looping = set(), False, set()
        for step in range(len(dynamic) - len(pinned) + 2):
            verdicts = judged_against(
                texts, [key for key in by_key if key not in pinned], earlier, changed
            )
            verdicts.update((key, None) for key in pinned)
            plans = planned(verdicts)
            following = {
                home: plans[home].text if plans[home].text is not None else original
                for home, original in ((ledger.home, ledger.text) for ledger in parsed)
            }
            moving = {
                key for key, found in verdicts.items() if found != earlier.get(key)
            }
            changed = {home for home in texts if following[home] != texts[home]}
            before, earlier, texts = texts, verdicts, following
            if not changed:
                settled = True
                break
            if step:
                # From a pass's second round on, a coordinate whose own row
                # this round rewrote again, on a cycle of rows each re-stamp
                # rewrites, cannot settle: waiting for the bound only judges
                # every coordinate of its file once per coordinate the run
                # carries.
                old = {home: gfm_lines(before[home]) for home in changed}
                new = {home: gfm_lines(texts[home]) for home in changed}
                rewrote = {
                    key
                    for key in (moving & propagating) - pinned
                    if by_key[key].home in changed
                    and old[by_key[key].home][by_key[key].number - 1]
                    != new[by_key[key].home][by_key[key].number - 1]
                }
                looping = on_a_cycle(rewrote, by_key, verdicts, propagating)
                if looping:
                    break
        if settled:
            break
        pinned |= looping or on_a_cycle(moving, by_key, verdicts) or moving
```

The case, in `tests/test_a_released_row_is_read_again_in_a_fragment.py`:

```python
def test_a_row_that_never_settles_costs_no_round_per_coordinate(repo, monkeypatch):
    """S6 beside forty citations of its file. The run leaves the self-quoting
    row once a round rewrites it again on its own cycle, rather than judging
    every citation of the file once per coordinate the run carries. Red at
    ca467185, which called judge 1,846 times here; 165 with the fix."""
    n = 40
    h = unit_hash(repo, "src/service.py", "handler")
    rows = [
        f"| R{i:02d} · handler adds one | `src/service.py#handler@{h}` | read "
        "| 2026-01-01 | |"
        for i in range(n)
    ]
    rows.append(
        f'| X · quotes itself | `{R_FILE}#"{SECTION}">"\\| X · quotes"@0000beef` '
        "| read | 2026-01-01 | |"
    )
    released(repo, rows)
    fragment(
        repo,
        [
            f"| Re-read · R{i:02d} | `{citation(rows[i], f'R{i:02d} · handler adds one')}`, "
            f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
            for i in range(n)
        ],
    )
    edit_handler(repo)
    calls = []
    real = ec.judge
    monkeypatch.setattr(ec, "judge", lambda *a: calls.append(a) or real(*a))
    paths = sorted(str(p) for p in (repo / "seal").rglob("*.md"))
    ec.reverify(paths, str(repo), {}, None, "2026-03-01")
    assert len(calls) < 10 * n, len(calls)
```

### 🟡 3 — a citation the family reader refuses takes that reader's verdict

In `reverify`, add this helper after the loop that builds `parsed`, and call
it at the two places that call `judge` on a spot:

```python
    def verdict_of(spot):
        """`judge`'s verdict for SPOT, except that a citation the family
        reader refuses takes that reader's status and sentence, the ones
        `--strict` prints for it: one citation, one reading (#809's class)."""
        verdict = judge(spot.m, root, maps, default_repo, scan_cache)
        if not spot.citation:
            return verdict
        files = {}

        def load(path):
            ident = file_identity(path)
            if ident not in files:
                body = read(path)
                files[ident] = (
                    None
                    if body is None
                    else (
                        path,
                        body,
                        gfm_lines(unquoted(body)),
                        {n: (h, c) for n, h, c in ledger_table_rows(body)},
                    )
                )
            return ident, files[ident]

        _header, cells = parsed[spot.key[0]].rows.get(spot.number, (None, []))
        status, detail, _ = cited_row(
            spot.m, citing_verb(cells), root, maps, default_repo, load
        )
        if status in ("OK", "DRIFTED"):
            return verdict
        return verdict._replace(status=status, detail=detail, now=None, dest=None)
```

```diff
-            index = (coordinate_of(spot.m), spot.m.group("hash"))
+            index = (coordinate_of(spot.m), spot.m.group("hash"), spot.citation)
             if index not in memo:
-                memo[index] = judge(spot.m, root, maps, default_repo, scan_cache)
+                memo[index] = verdict_of(spot)
@@ judged_against
-                    found[key] = judge(
-                        by_key[key].m, root, maps, default_repo, scan_cache
-                    )
+                    found[key] = verdict_of(by_key[key])
```

The case, in `tests/test_a_released_row_is_read_again_in_a_fragment.py`:

```python
@pytest.mark.parametrize("shape", ["literal twice", "section twice"])
def test_reverify_names_a_citation_in_the_family_readers_words(repo, shape):
    """A citation `--strict` reads BROKEN through the family reader -- its
    literal on two lines of its section, or its section there twice -- is
    named by `--reverify` with that sentence. Red at ca467185, which said
    the anchored statement is gone, or nothing, at exit 0."""
    h = unit_hash(repo, "src/service.py", "handler")
    r1 = f"| R1 · handler adds one | `src/service.py#handler@{h}` | read | 2026-01-01 | |"
    released(repo, [r1])
    fragment(
        repo,
        [
            f"| Re-read · R1 | `{citation(r1, 'R1 · handler adds one')}`, "
            f"`src/service.py#handler@{h}` | read | 2026-02-01 | Re-read 2026-02-01 |"
        ],
    )
    path = repo / R_FILE
    body = path.read_text(encoding="utf-8")
    if shape == "literal twice":
        body += r1.replace("2026-01-01", "2026-01-02") + "\n"
    else:
        body += (
            f"\n{SECTION}\n\n"
            "| R2 · other | `src/service.py#other@00000000` | read | 2026-01-01 | |\n"
        )
    path.write_text(body, encoding="utf-8")
    check = run(["--strict", "."], repo)
    (said,) = [
        line
        for line in check.stdout.splitlines()
        if "BROKEN" in line and "0.1.0.md#" in line
    ]
    detail = said.split('"R1 · handler adds one"', 1)[1].strip()
    fix = run(
        [
            "--reverify",
            "--checked",
            "2026-03-01",
            "--ledger",
            "seal/ledger/2000000001-a-later-item.md",
            ".",
        ],
        repo,
    )
    assert f'"R1 · handler adds one"  {detail} — left' in fix.stdout, fix.stdout
```

### 🟡 4 — a coordinate no checkout places hands MOVES nothing

In `plan_ledger`, the general leaving:

```diff
         left.append((spot, verdict.detail))
+        if verdict.status == "EXTERNAL" or spot.target is None:
+            # Another checkout this run was not given, or a path out of the
+            # repository: no unit, file or quoted statement is known gone,
+            # which is all the pact's BROKEN says, so MOVES gets no part.
+            continue
         pending.append((spot, None))
     dated, undated, undatable = [], [], []
```

The case, in `tests/test_a_signatory_records_a_pact_change.py`:

```python
@pytest.mark.parametrize(
    "coord", ["legacy/src/x.py#f@0000beef", "../outside.py#f@0000beef"]
)
def test_a_coordinate_no_checkout_places_records_no_pact_change(repo, coord):
    """A row citing a clause beside a coordinate in another checkout the run
    was not given, or one escaping the repository: the run names it `left`
    and records nothing, because nothing is known gone. Red at ca467185,
    which recorded it BROKEN; e6d5a055 recorded nothing."""
    (repo / "seal" / "parity.md").write_text(
        "| Item | Value |\n|---|---|\n", encoding="utf-8"
    )
    cite(repo, [row("O1", f"`{CLAUSE}`, ", coord)])
    _code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert f"  {coord.rsplit('@', 1)[0]}  " in out, out
    assert record_rows(repo) == [], out
```

## Proof block

```
📋 code-review applied (warden, round 1)
· read:     spec.md, routing.md, questions.md, overview.md, survivors.md,
            phases/phase-1.md … phase-4.md, changelog.md;
            seal/ledger/1791240748-reverify-computes-once-and-judges-in-one-place.md (lines 11-41);
            skills/evidence-check/scripts/evidence_check.py (1055-1135, 1191-1262, 1568-1834,
            2209-2336, 3040-3679, 3740-4250, 4387-4612, 5676-5866) at the target;
            the base script at e6d5a055 (3330-3640);
            tests/test_a_released_row_is_read_again_in_a_fragment.py (1-125, 3860-4312);
            tests/test_a_signatory_records_a_pact_change.py (1-140); docs/the-pact.md (140-220);
            the docs/ diff; seal/releases 0.4.0:59, 0.18.0:24, 0.18.1:417, 0.18.2:86/87/90,
            0.18.3:6/8/10, and the E1, C1, A4, A6, W8 and three 0.4.0 rows
· executed: the probes in the table above, in a scratch clone at ca467185; bin/evidence-check --strict .
· unverified: the broad gate — the sealer, after the rounds settle
```
