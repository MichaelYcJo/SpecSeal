# Round 3 report — 1790815615, the seal names what it sealed and counts only the steps that run

A verifying round, and the last one: round 2 used the run's one reopening,
so this round ends the run whatever it finds. Target SHA
`111ef570a47de827c08b75d3ffc4b409ee1989a5`. The diff verified is round 2's
fix range `0cbadb8e6c16e409a68ab14494b93dac6c187198..4744a1c045ba7e02c6190c56aee6a89cc915b0eb`,
five commits; `111ef570` only closes round 2's record. The work was done in
a `git clone --no-local` at the target, never in the worktree.

## What round 2's account claimed, and what the code does

Round 2 recorded 🟡 1, 🟡 2 and ⬜ 5 as `fixed`, and ⬜ 3 and ⬜ 4 as
`answered`. Each was checked against the code at the target.

- **🟡 1 (slash-joined words read as a path home) is closed for its
  instance.** Executed: `CI/CD`, `and/or` and `stdout/stderr` stay words,
  and the issue after them is the home. All four round-2 cells are right,
  and reverting `HOME_TOKEN` makes five of the new parametrized cases fail,
  so the cases were seen red. **The class is not closed**, though. The same
  commit widened the bare-name arm from `.md` to any extension, so a dotted
  name that is not a file now reads as a home. That is 🟡 1 below.
- **🟡 2 (a path home loses its underscores) is closed for underscores
  inside a word.** Executed: `tests/test_the_gate_names_every_step_ci_runs.py`
  keeps its name, and reverting the marks line makes the two new cases fail.
  **The class is not closed** for an underscore at the edge of a path
  segment. That is 🟡 2 below.
- **⬜ 3 is answered.** Read: `seal_stamp.not_sealed` writes the names on
  its first line only (`skills/verify/scripts/seal_stamp.py:472`); the
  per-check lines carry the check's name and output (`:479`), and the
  preflight replaces exactly line 0 (`skills/verify/scripts/broad_gate.py:2915`).
  The corrected `overview.md` sentence says that. Executed: `survivor-check`
  over the fix range flags the P3 ledger note as a survivor of the removed
  sentence, and the new `survivors.md` row excuses it (exit 0 with
  `--exempt`).
- **⬜ 4 is answered.** Read: 0.15.1 N3, 0.15.4 A5 and C4, and 0.15.7 N9
  each carry a note for the merge into this work item, and the earlier
  notes are still there. Executed: `evidence-check .` reports 0 drifted and
  0 broken.
- **⬜ 5 is fixed.** Read: the `gate_copy` docstring (`broad_gate.py:451`)
  and the comment above `INVOKED_AS_VAR` (`:3015`) now name both reasons.
  The claim was checked against the installed 0.16.0 copy, which redirects
  (its `redirect_line`) and never sets `SPECSEAL_BROAD_GATE_INVOKED_AS`.

### The smith's departure: no lookbehind

The report's paste-ready fix started the path arm with `(?<![\w/.-])`. The
smith left it out, on the grounds that it misses `./seal/follow-up.md`.
**The grounds are correct** (executed). With the lookbehind put back,
`deferred see ./seal/follow-up.md` fails, and it is the only one of the 24
home cases that does. Every possible start inside `./seal/follow-up.md`
comes after `/`, `.` or `-`, so the lookbehind refuses all of them, and the
cell falls back to its words. The lookbehind also bought nothing. It limits
where a match may begin, while 🟡 1 below is about where a match ends.
Without it, a match can only begin partway into a token after a character
the first class excludes (`.`, `/`, `:`), and that is the start of the path
anyway.

## Findings

Both findings sit in lines this run's own fix commits wrote: `HOME_TOKEN`
at `fa03671d`, the marks line at `90e5e27`. Each is one depth.

### 🟡 1 — a dotted name before an issue is read as a file home, and hides the issue

`skills/verify/scripts/broad_gate.py:2404`. The new `HOME_TOKEN` takes any
token whose last part has an extension, with no slash required. Python
attribute names match that shape, and this repository's prose is full of
them. Executed at the target:

| Cell | Home printed | Should be |
|---|---|---|
| `deferred — chain_check.verdict_of's reading is #703's` | `chain_check.verdict_of` | `#703` |
| `deferred — seal_stamp.not_sealed's head is #704's` | `seal_stamp.not_sealed` | `#704` |
| `deferred — args.preflight goes to #705` | `args.preflight` | `#705` |
| `deferred — re.sub is #706's` | `re.sub` | `#706` |
| `deferred — the Node.js port is #702's` | `Node.js` | `#702` |

At `0cbadb8e`, before the fix, every one of these read the issue. The bare
arm took `.md` only, and the old `EMPHASIS` took the underscores out of the
first two anyway. So this is round 2's 🟡 1 class: something the cell does
not name as a home is printed as the home, and the real home is hidden. The
widening came from round 2's own paste-ready regex, which the smith copied.
The 73 deferred rows in the tree all still read right. Like round 2's
🟡 1, this misreads the next deferral written in prose, not any record that
exists today.

The fix is to require a slash for any extension, and keep the bare arm at
`.md`, as it was before round 2. Executed in the clone: with the fix, all
24 home cases pass. The five cells above read their issue, and the 73 tree
rows read as before. The cost is that a bare non-`.md` file such as
`round_record.py` reads as words (`to round_record.py`) instead of a file,
which is what happened before the fix. The work item's ledger fragment row
N9 says *a path whose last part carries an extension*, so it needs a
`Corrected` note.

### 🟡 2 — an underscore at the edge of a path segment is still taken off

`skills/verify/scripts/broad_gate.py:2431`. The narrower marks pattern
removes an underscore that has no word character on one side. That is true
of the underscore right after `/`, and of a dunder name next to a `.`. The
marks are also stripped inside a code span, where Markdown treats nothing as
emphasis. Executed at the target (fixture paths, which the tree does not
carry — NAME NOT IN TREE):

```
deferred to src/pkg/_internal/io.py      ->  src/pkg/internal/io.py
deferred to `src/pkg/_internal/io.py`    ->  src/pkg/internal/io.py
deferred to pkg/__init__.py              ->  pkg/init.py
deferred to `skills/x/__init__.py`       ->  skills/x/init.py
```

This is round 2's 🟡 2 class, closed only for the interior instance. The
docstring is honest about the rule (*an underscore only at a word's edge*).
But the work item's ledger row N9 says *its underscores kept*, and that is
false for these names. The gate ships to every installation, and Python
repositories name packages this way. No tracked file in this repository
starts a segment with `_` (executed: `git ls-files`, 0 such paths), so no
record misprints today.

The fix keeps a code span literal. Outside a span, an underscore counts as
a mark only where no word character, `/` or `.` touches it. Executed in the
clone with 🟡 1's fix applied too: all 24 home cases pass, the three cells
whose segment is under a directory read whole, `__deferred__ #664` and
`_phase 9_` still lose their marks, and the 73 tree rows read as before.
A bare dunder name outside a span, such as a lone `__init__.py`
(NAME NOT IN TREE), still loses its leading pair. Markdown itself renders
that as bold, and with 🟡 1's fix it is not a file home anyway.

## Regression tests to plant

Both go into `tests/test_the_seal_is_taken_once_by_the_sealer.py`, in
`test_a_deferrals_home_is_read_whole`'s parameters. All six cells were seen
failing at the target (executed, as quoted above), so they are red before
the fix and green after it.

## Facts for the evidence ledger

- The work item's fragment row N9 needs a `Corrected` note once 🟡 1 and
  🟡 2 are fixed: the file arm is *a path whose last part carries an
  extension, or a bare `.md` name*, and *its underscores kept* then holds
  everywhere except a lone dunder name outside a code span.

## Where the run stands

This round ends the run. Both findings are in lines this run's fixes wrote,
and the cap rule says such a finding is the branch's to fix, whatever round
found it. The orchestrator applies that test. Once both are closed, the
sealer's spawn comes due. The full suite has not run.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a dotted name that is not a file (`chain_check.verdict_of`, `re.sub`, `Node.js`) placed before an issue is printed as the home and hides the issue; the bare-name arm was widened from `.md` to any extension | `skills/verify/scripts/broad_gate.py:2404` | open | executed at the target over five cells, all wrong, all right at `0cbadb8e`; round 2's 🟡 1 class, opened by `fa03671d`; the fix is executed green over 24 cases and 73 tree rows |
| 🟡 2 | an underscore at the edge of a path segment is still taken off, inside a code span too, so a package's private directory or a dunder module name prints without its underscores | `skills/verify/scripts/broad_gate.py:2431` | open | executed at the target over four cells, all wrong; round 2's 🟡 2 class, closed only for the interior instance at `90e5e27`; ledger N9 says *its underscores kept* |
| 🟢 | round 2's 🟡 1 finding is closed for its instance — slash-joined words stay words | `skills/verify/scripts/broad_gate.py:2404` | confirmed | executed: four round-2 cells right; reverting `HOME_TOKEN` fails five new cases; the class goes on as 🟡 1 |
| 🟢 | round 2's 🟡 2 finding is closed for its instance — an interior underscore is kept | `skills/verify/scripts/broad_gate.py:2431` | confirmed | executed: reverting the marks line fails the two new cases; the class goes on as 🟡 2 |
| 🟢 | round 2's ⬜ 3 is closed — the overview says the names ride only the head line the preflight replaces | `seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/overview.md:39` | confirmed | read at `seal_stamp.py:472` and `broad_gate.py:2915`; `survivor-check` over the range exits 0 with the work item's `survivors.md` |
| 🟢 | round 2's ⬜ 4 is closed — the four rows re-hashed at the merge carry a merge note | `seal/releases/0.15.4.md` | confirmed | read: 0.15.1 N3, 0.15.4 A5 and C4, 0.15.7 N9, earlier notes kept; `evidence-check .` 0 drifted |
| 🟢 | round 2's ⬜ 5 is closed — both places name an installed copy older than #666 | `skills/verify/scripts/broad_gate.py:3015` | confirmed | read, and the installed 0.16.0 copy read: it redirects and sets no invoked-path variable |
| 🟢 | the smith's departure from the paste-ready lookbehind is right | `skills/verify/scripts/broad_gate.py:2404` | confirmed | executed: with the lookbehind, `deferred see ./seal/follow-up.md` fails, 1 of 24; the lookbehind limits where a match starts, never where it ends |

## Paste-ready fixes

### 🟡 1

```python
# What a home looks like inside a deferral's prose: an issue, or a file —
# a path whose last part carries an extension, or a bare `.md` name. A bare
# dotted name is not a file, so `chain_check.verdict_of`, `re.sub` and
# `Node.js` stay words and an issue after them is still found (round 3 of
# #666), as `CI/CD`, `and/or` and `stdout/stderr` do (round 2).
HOME_TOKEN = re.compile(
    r"#\d+|[\w-][\w.-]*(?:/[\w.-]+)+\.[A-Za-z]\w+\b|[\w-][\w.-]*\.md\b"
)
```

```python
        # A dotted name is not a file, and an issue after it is the home
        # (round 3's 🟡 1).
        ("deferred — chain_check.verdict_of's reading is #703's", "#703"),
        ("deferred — the Node.js port is #702's", "#702"),
        ("deferred — `round_record.py`'s owner, see #709", "#709"),
```

### 🟡 2

```python
    marks = "".join(
        part if i % 2 else re.sub(r"\*+|(?<![\w/.])_+|_+(?![\w/.])", "", part)
        for i, part in enumerate(cell.split("`"))
    )
```

```python
        # An underscore at a segment's edge is the file's, not a mark, and
        # nothing inside a code span is a mark (round 3's 🟡 2).
        ("deferred to src/pkg/_internal/io.py", "src/pkg/_internal/io.py"),
        ("deferred to `src/pkg/_internal/io.py`", "src/pkg/_internal/io.py"),
        ("deferred to pkg/__init__.py", "pkg/__init__.py"),
```

The docstring sentence to match:

```text
The marks are taken off by a narrower pattern than `chain_check.EMPHASIS`,
which removes every `_`: nothing inside a code span is a mark, and outside
one, asterisks and an underscore that no letter, `/` or `.` touches, so
`tests/test_x.py` and `src/pkg/_internal/io.py` keep their names (round 2's
🟡 2 and round 3's 🟡 2 of #666).
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q` in the clone at the target | exit 0, 225 passed |
| a one-off probe: `deferred_home` over 31 typed cells and every deferred row of every `round-N.md` in the tree | round 2's four cells and the `./`, `../`, `to #664`, `→ #664`, `→ later` cells right; 73 tree rows right, all ASCII; the dotted-name and edge-underscore cells wrong, as reported |
| the home cases (`-k home`) with `HOME_TOKEN` reverted to `0cbadb8e`'s | exit 1, 5 failed: the four slash cells and the `./` cell |
| the home cases with the marks line reverted to `chain.EMPHASIS` | exit 1, 2 failed: the two underscore cells |
| the home cases with round 2's paste-ready lookbehind in place of the shipped regex | exit 1, 1 failed: `deferred see ./seal/follow-up.md` |
| the home cases and the typed probe with both fixes above applied | exit 0, 24 passed; 29 of 31 typed cells as expected (the other two read words, as described); 73 tree rows unchanged; file restored, `git status` clean |
| `bin/evidence-check .`, unscoped, at the target | exit 0; `total: 3237 ok · 0 drifted · 0 broken · 0 external · 0 old-format · 0 malformed · 0 overflow` |
| `bin/survivor-check --range 0cbadb8e..4744a1c0`, then again with `--exempt` set to the work item's `survivors.md` | exit 1 with one survivor (the P3 note), then exit 0, excused by the row |
| the full suite, repository lint and typecheck (the broad gate) | not yet: this round did not run them; they are the sealer's once the rounds settle |

Needs a fix: yes — 🟡 1 (a dotted name before an issue is read as the
home), 🟡 2 (an underscore at a path segment's edge is taken off)

Loses a record or crashes: no

## Proof block

Files opened this round:
`skills/verify/scripts/broad_gate.py` (the fix diff, `deferred_home`,
`HOME_TOKEN`, `rounds_rows`, the preflight head),
`skills/verify/scripts/seal_stamp.py` (`not_sealed`),
`skills/code-review/scripts/chain_check.py` (`verdict_of`, `EMPHASIS`,
`MARKER`, `SEPARATORS`), `tests/test_the_seal_is_taken_once_by_the_sealer.py`
(the home cases and the module loaders), the installed 0.16.0
`broad_gate.py` (searched for the invoked-path variable and the redirect),
`rounds/round-2.md` and `rounds/round-2-report.md` of this work item, and
the fix range's diff of `overview.md`, `survivors.md`, the 1790815611 ledger
fragment and `seal/releases/0.15.1.md`, `0.15.4.md`, `0.15.7.md`. Labels:
everything under *Executed probes* was run in the clone; the ⬜ 3, ⬜ 4 and
⬜ 5 closures are read, with the checks named beside them. Nothing was left
unverified, apart from the broad gate, which is the sealer's.
