# Round 2 report — 1790815615, the seal names what it sealed and counts only the steps that run

A verifying round. Target SHA `39ef351cc9e778604f83d7d6c97e6a8101f81f74`;
the diff verified is round 1's fix range
`613b93896123490b8eaf893d716bacf46659c0b4..bf44693446255098ef5fb459f69172e4db8fdcf9`
(four commits), plus the merge `613b9389` itself, which nobody had reviewed.
Read and run in a `git clone --no-local` of the branch at the target, with
`origin/release/v0.17.0` pointed at `a340221b`, the merge's second parent
and the remote's head. Nothing was written in the worktree but this file.

Carried from round 1, not re-established: the coordinates of the five
findings, the six-module list, and the two real records whose homes were
cut. Every verdict below is this round's.

How the findings relate:

```
round 1's 🟡 2: a home was read as the first word
   └─ fixed: an issue or a path anywhere in the cell is the home
        ├─ 🟡 1  but `HOME_TOKEN`'s path arm takes any two words joined by a slash
        │        (`CI/CD`, `and/or`), and one placed before an issue hides the issue
        └─ 🟡 2  and a path home is read after `EMPHASIS`, which drops every `_`,
                 so an underscored path prints as a file that does not exist
the merge 613b9389
   └─ holds: every note of both sides stands, hashes are right, #638's preflight intact
        ├─ ⬜ 3  `overview.md` says the names reach a failed preflight's per-check lines; they do not
        └─ ⬜ 4  four heading rows re-hashed at the merge carry no note of it
round 1's 🟡 4: the gate row's third case
   └─ fixed in the three documents and the changelog
        └─ ⬜ 5  two code comments next to it still give two of the three cases
```

## Round 1's verdicts, answered

### 🟡 1 — the counts and the homes continue beneath their label: closed

`wrapped` (`skills/verify/scripts/broad_gate.py:266`) breaks the list
before a piece that does not fit, keeps the comma at the end of the row it
leaves, and holds back one column for that comma on every piece except the
last. Re-run over the tree (executed): `1790645290` now draws
`4 deferred -> #673,` / `#664`, and `1790297085` draws
`4 deferred -> #611,` / `#612, #610`. Every home is shown and no row is
wider than 23 columns. The class is closed. The suite's counts take the
same path, and `5181 passed, 10 skipped, 2 xfailed, 3 warnings` draws on
three rows of 12, 22 and 10 columns. `beside` in `seal_stamp.py` centres a
panel of any height against the disc (read), so the extra rows draw
correctly.

### 🟡 2 — a home is no longer the first word: closed for the tree, and two misreads remain in the same class

The tree's four rows now read right (executed): `#97`, and
`phase 9 of this branch` twice. The fourth row,
`deferred — they are true statements about the past, …` (`1788395377`,
round 1), names no home. It now prints its whole clause, which `fit` elides
on the panel. That is the designed fallback, and that record is not a last
record. The typed shapes read right as well: `deferred to #664` and
`deferred → #664` give `#664`, `deferred → later` gives `later`, and the
returned home is ASCII.

The fix opened two new misreads in the same class, a home printed that is
not the home. They are 🟡 1 and 🟡 2 below.

### 🟡 3 — the coverage base is pinned: closed

`unanswered` and `coverage_line` now require `given`. Two mutations were
executed:

- Dropping the argument from the gate's call raises `TypeError` and fails
  `test_the_stamp_says_how_many_steps_the_seal_did_not_answer`.
- Passing `None` explicitly fails only
  `test_a_release_pull_request_is_sealed_as_ci_would_judge_it` (1 failed,
  303 passed), so the new assertion there is not vacuous.

The merged call is `coverage_line(workflow, base.given) if workflow and not
args.preflight else None`, which keeps both sides' halves.

### 🟡 4 and ⬜ 5 — the gate row's third case: closed in the four places named

`agents/sealer.md`, `docs/the-broad-gate.md`, the section comment above
`GATE_REL` and the changelog fragment each state all three cases (read in
the diff). `test_the_documents_say_where_the_panel_now_carries_each_name`
pins all four (green, executed). Two neighbouring code comments still give
two of the three cases. That is ⬜ 5.

## New findings

### 🟡 1 — `HOME_TOKEN`'s path arm reads any two words joined by a slash as a path

`skills/verify/scripts/broad_gate.py:2400`: `[\w.-]+(?:/[\w.-]+)+` matches
`CI/CD`, `and/or`, `read/write` and `stdout/stderr`. Because the search
returns the leftmost match, such a word also hides a real home later in
the cell. Executed at the target:

| Cell | Printed | The home |
|---|---|---|
| `deferred — the stdout/stderr split is #700's` | `stdout/stderr` | `#700` |
| `deferred — read/write order is in seal/follow-up.md` | `read/write` | `seal/follow-up.md` |
| `deferred to whoever owns CI/CD next` | `CI/CD` | the words |
| `deferred to the owner and/or the framer` | `and/or` | the words |

Why it matters: this is round 1's 🟡 2 class, a stamp naming as the home
something the cell does not name as one. This repository's prose uses
slash-joined words often, so the next deferral written in prose can hit
it. Requiring the path's last part to carry an extension fixes all four
rows. All twelve parametrized cases still pass with that change (executed,
and the sealer module is green with it: 216 passed). One misread is left
and not asked for: the words fallback splits `e.g. to the next release` at
`e.g`, because `HOME_END` treats `. ` as a sentence end.

### 🟡 2 — a path home is read after `EMPHASIS`, which removes every underscore

`skills/verify/scripts/broad_gate.py:2423` reads the home off
`chain.EMPHASIS.sub("", cell)`. `EMPHASIS` is `[*_`]+`, which suits
`verdict_of` asking for a word, but it also deletes the `_` inside a file
name. Executed at the target:
`deferred tests/test_the_gate_names_every_step_ci_runs.py` prints
`tests/testthegatenameseverystepciruns.py`, and
``deferred to `broad_gate.py`'s owner`` prints `broadgate.py`.

Why it matters: the fix's docstring now says a path anywhere is the home,
and every test module and script in this repository is named with
underscores. The stamp would name a file that does not exist. The line
predates the fix, so it sits at depth 0, apart from 🟡 1. The fix
promoted paths to first-class homes, which is why this round opened it.
Taking out only code spans, asterisks and `_` at a word's edge keeps the
name (executed together with 🟡 1's change: the probe's cells read right
and the sealer module is green).

### ⬜ 3 — `overview.md` says the names reach a failed preflight's per-check lines

`overview.md:39` (§Not done) says: *"At the merge, the names went onto the
per-check lines below a failed preflight's head (`not_sealed(…, branch,
base.ref)`)"*. `not_sealed` puts the names only on its first line
(executed: `NOT SEALED   feat/666-x @ aaaaaaaa against
origin/release/v0.17.0 @ bbbbbbbb`, then `''`, then `  suite    1
failed`). The preflight replaces exactly that line, so the names never
reach a preflight's output. #638's ledger fragment says it correctly:
*"the per-check lines carry over"*. This is paperwork, so it is a
correction: the sentence should say the names are passed and discarded
with the head.

### ⬜ 4 — four release rows the merge re-hashed carry no note of it

The merge re-hashed two headings both sides edited: `skills/verify/SKILL.md`
§*The broad gate — after the rounds…* (`d7dd805d`) and
`skills/code-review/orchestration.md` §*Orchestrator: the pull request
opens…* (`be3b595b`). The hashes are right, since `evidence-check` at
`613b9389` reports 0 drifted. #638's fragment rows over the same headings
gained an *at the merge* re-read. The release rows did not:
`seal/releases/0.15.1.md` N3, `seal/releases/0.15.4.md` A5 and C4, and
`seal/releases/0.15.7.md` N9. Each still carries both sides' notes, and
together those cover both edits. What is missing is the dated line saying
somebody read the merged section. All twelve rows anchored on `gate` or
`main` carry one.

### ⬜ 5 — two code comments give the gate row's condition without the older-copy case

`skills/verify/scripts/broad_gate.py:3006` (*"Absent, the running copy was
invoked directly."*, above `INVOKED_AS_VAR`) and the `gate_copy` docstring
at `:450` (*"`installed` is None — the tree's copy invoked directly"*) give
one reason for the missing path. There is a second: an installed copy older
than #666 redirects without setting the variable. This is the rest of
round 1's 🟡 4 class. Both are comments and the behaviour is right, so it is
⬜.

## The merge, checked against both parents

Executed: a three-way probe over the nine `seal/releases/*.md` files that
both `6b421616` and `a340221b` edited.

- **Rows.** Each file has the same row count at the base, on both sides and
  at the merge (24, 39, 27, 47, 39, 32, 24, 107, 22). No row is duplicated
  and none is lost. The duplicate lines the probe flagged are the
  pre-existing repeated table headers.
- **Notes.** Every `Re-read` and `Corrected` note from either side is
  present at the merge. That includes 0.15.7 N2's
  `Corrected 2026-10-01 by work item 1790815611 (#638)` and the sentence it
  added to the Claim, *"A green `--preflight` run draws and writes nothing
  too…"*, which the smith restored. The probe's two "lost" reports were
  sentence-split artefacts and were read by hand.
- **Hashes.** Every anchor that one side edited carries that side's hash.
  The anchors both sides edited carry a third hash: `broad_gate.py#gate`
  (`51ce700f`), `#main` (`ccbdc94b`), and the two headings of ⬜ 4. That is
  the hash of neither side, which is the rule. `evidence-check .` at
  `613b9389` reports `total: 3233 ok · 0 drifted · 0 broken`, so each of
  those hashes is the merged unit's.
- **Code.** The combined diff shows three hunks where the merge differs
  from both parents, all in `gate`. The `--record` refusal still stands
  before `item` is taken. The coverage call keeps the base and the
  preflight's `None`. A failed preflight replaces `not_sealed`'s head with
  `preflight_line(PREFLIGHT_FAILED, …)`, and a green one returns before the
  record and stamp. `PREFLIGHT_PASSED`, `PREFLIGHT_FAILED`, `PREFLIGHT_TAIL`
  and `preflight_line` are unchanged from `a340221b`. Eleven `preflight`
  cases pass, including
  `test_a_fixed_at_verdict_in_a_verifying_round_fails_the_preflight`, which
  asserts the head `PREFLIGHT FAILED`, and
  `test_a_preflight_with_record_is_refused_and_writes_no_cell`.
- **`correction-check --range origin/release/v0.17.0...HEAD`** exits 0:
  *examined 1 merge commit(s) in a340221..39ef351 — no correction marker
  was dropped at a merge*.

## What holds

- `wrapped`, over the real records and over edge lists (executed). A first
  piece wider than the frame goes to `fit` alone. A row that would fill
  the frame exactly is broken one piece early, so its comma is not cut.
- The ASCII rule in `deferred_home`. It does what its docstring says: a
  Korean home `다음 릴리스` prints `?? ???`. That loses the home for a
  repository whose `Record language` is not English. But `fit` and `letter`
  measure with `len()`, and a terminal draws a Hangul syllable two columns
  wide, so an unfolded home would break the frame. The fold is the bound
  the panel already has, and this round does not count it as a defect.
- `evidence-check .` unscoped and `--strict .` at the target exit 0,
  `total: 3237 ok · 0 drifted · 0 broken`.

## Regression tests to plant

- `tests/test_the_seal_is_taken_once_by_the_sealer.py`,
  `test_a_deferrals_home_is_read_whole`: the slash and underscore cells in
  the fixes below. The slash cells were seen red at the target and green
  with the fix (probe, executed). The `broad_gate.py` cell was seen red at
  the target and green with 🟡 2's fix. The test-module cell was executed
  red at the target only.

## Facts for the evidence ledger

None new.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `HOME_TOKEN`'s path arm reads words joined by a slash (`CI/CD`, `and/or`, `stdout/stderr`) as a path, and one placed before an issue hides the issue: `deferred — the stdout/stderr split is #700's` prints `stdout/stderr` | `skills/verify/scripts/broad_gate.py:2400` | open | executed at the target over four cells; requiring an extension fixes all four, and the twelve parametrized cases and the sealer module stay green (216 passed) |
| 🟡 2 | a path home is read after `EMPHASIS`, which removes every `_`, so `tests/test_the_gate_names_every_step_ci_runs.py` prints as `tests/testthegatenameseverystepciruns.py` | `skills/verify/scripts/broad_gate.py:2423` | open | executed at the target; this line predates the fix (depth 0), and the fix made a path a first-class home; the paste-ready marks keep the name, sealer module green with it |
| ⬜ 3 | `overview.md` §Not done says the names reach a failed preflight's per-check lines; `not_sealed` puts them on the head only, and the preflight replaces the head | `seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/overview.md:39` | open | `not_sealed` executed with names: only line 0 carries them; paperwork, a correction |
| ⬜ 4 | four release rows re-hashed at the merge over the two headings both sides edited carry no *at the merge* note, where #638's fragment rows over the same headings do | `seal/releases/0.15.4.md` | open | rows 0.15.1 N3, 0.15.4 A5 and C4, 0.15.7 N9; hashes right (`evidence-check` at `613b9389`, 0 drifted); both sides' notes present; paperwork, a correction |
| ⬜ 5 | two comments give one reason for an absent invoked path, the direct run, and leave out an installed copy older than #666 | `skills/verify/scripts/broad_gate.py:3006` | open | read; also the `gate_copy` docstring at `:450`; the rest of round 1's 🟡 4 class; behaviour right |
| 🟢 | round 1's 🟡 1 is closed — a list of counts or homes continues beneath its label | `skills/verify/scripts/broad_gate.py:266` | confirmed | executed: `1790645290` and `1790297085` show every home, every row 23 columns or fewer; `beside` draws any height |
| 🟢 | round 1's 🟡 2 is closed for the tree's four rows and the typed shapes | `skills/verify/scripts/broad_gate.py:2405` | confirmed | executed over every deferred row of every `round-N.md` and over `to #664`, `→ #664`, `→ later`: right home, ASCII; the two remaining misreads are 🟡 1 and 🟡 2 |
| 🟢 | round 1's 🟡 3 is closed — the base cannot be dropped silently | `skills/verify/scripts/broad_gate.py:2829` | confirmed | mutations executed: argument dropped raises `TypeError` and fails a case; `None` fails `test_a_release_pull_request_is_sealed_as_ci_would_judge_it` |
| 🟢 | round 1's 🟡 4 and ⬜ 5 are closed in the four places named | `docs/the-broad-gate.md:106` | confirmed | read in the diff; the documents case pins all four, green (executed) |
| 🟢 | the merge keeps every note of both sides, a right hash on every row, no row duplicated or lost | `seal/releases/0.15.7.md` | confirmed | three-way probe over nine files executed; `evidence-check .` at `613b9389` 0 drifted; `correction-check` exit 0 |
| 🟢 | #638's preflight survives the merge: head unchanged, `--record` refused first, no coverage line, early return | `skills/verify/scripts/broad_gate.py:2793` | confirmed | combined diff read; eleven `preflight` cases green (executed) |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the sealer, CI-steps, range, stamp and broad-gate-rule modules, in the clone | exit 0, 351 passed |
| `bin/evidence-check .` unscoped, then `--strict .`, at the target | both exit 0; `total: 3237 ok · 0 drifted · 0 broken` |
| `bin/evidence-check .` unscoped at the merge `613b9389` | exit 0; `total: 3233 ok · 0 drifted · 0 broken` |
| `bin/correction-check --range origin/release/v0.17.0...HEAD`, `origin/release/v0.17.0` at `a340221b` | exit 0; one merge examined, no marker dropped |
| a one-off three-way probe over the nine release files both parents edited: rows, notes, hashes, one-sided cells | rows equal; every note present; one-sided hashes from the editing side; both-edited hashes are the merge's own |
| a one-off probe: `rounds_rows` for `1790645290` and `1790297085`, `deferred_home` over every deferred row of the tree and fifteen typed cells, `wrapped` over six lists, `not_sealed` with names | every home shown; tree rows right; slash, underscore and later-issue cells as reported; names on line 0 only |
| the gate's coverage call with the argument dropped, then the three gate modules (`-x`) | exit 1, `TypeError`, `test_the_stamp_says_how_many_steps_the_seal_did_not_answer` fails |
| the gate's coverage call given `None`, then the three gate modules | exit 1, 1 failed (`test_a_release_pull_request_is_sealed_as_ci_would_judge_it`), 303 passed |
| 🟡 1's and 🟡 2's fixes applied in the clone, the probe re-run, then the sealer module | probe: 17 of 18 cells right, `e.g.` the one left; sealer module exit 0, 216 passed; file restored with `git checkout` |
| the eleven `preflight` cases across the sealer and broad-gate-rule modules | 11 passed |
| the full suite, repository lint and typecheck (the broad gate) | not yet: not run by this round; it is the sealer's once the rounds settle |

## Paste-ready fixes

### 🟡 1 — a path is a file name, not any two words with a slash

In `skills/verify/scripts/broad_gate.py`, replacing the `HOME_TOKEN` line
and its comment:

```python
# What a home looks like inside a deferral's prose: an issue, or a file — a
# path whose last part carries an extension, so `CI/CD`, `and/or` and
# `stdout/stderr` stay words and an issue after them is still found (round 2
# of #666).
HOME_TOKEN = re.compile(r"#\d+|(?<![\w/.-])[\w-][\w.-]*(?:/[\w.-]+)*\.[A-Za-z]\w+\b")
```

In `tests/test_the_seal_is_taken_once_by_the_sealer.py`, added to the
parameters of `test_a_deferrals_home_is_read_whole`:

```python
        # Words joined by a slash are words, not a path (round 2 of #666).
        ("deferred — the stdout/stderr split is #700's", "#700"),
        ("deferred to whoever owns CI/CD next", "to whoever owns CI/CD next"),
        ("deferred — read/write order is in seal/follow-up.md", "seal/follow-up.md"),
```

### 🟡 2 — read the home without removing the underscores in a file name

In `skills/verify/scripts/broad_gate.py`, under `HOME_END`:

```python
# The marks a home is read without: code spans, asterisks, and an underscore
# at a word's edge. Not `chain_check.EMPHASIS`, which removes every `_` and
# so prints `tests/test_x.py` as `tests/testx.py` (round 2 of #666).
HOME_MARKS = re.compile(r"`|\*+|(?<!\w)_+|_+(?!\w)")
```

In `deferred_home`, between the `startswith` check and `rest`:

```python
    s = chain.MARKER.sub("", HOME_MARKS.sub("", cell).strip())
    rest = s[len(chain.DEFERRED) :].strip(chain.SEPARATORS)
```

Added to the same parameters:

```python
        # A file name keeps its underscores (round 2 of #666).
        (
            "deferred `tests/test_the_gate_names_every_step_ci_runs.py`",
            "tests/test_the_gate_names_every_step_ci_runs.py",
        ),
        (
            "deferred to `skills/verify/scripts/broad_gate.py`'s owner",
            "skills/verify/scripts/broad_gate.py",
        ),
```

Needs a fix: yes — 🟡 1 (a slash-joined word read as a path home), 🟡 2 (a
path home loses its underscores)
Loses a record or crashes: no

The broad gate has not come due: this round leaves two findings that need a
fix.

## Proof block

Files opened, all at the target in the clone unless a revision is named:
`seal/specs/1790815615-the-seal-names-what-it-sealed-and-counts-only-the-steps-that-run/rounds/round-1.md`,
`…/rounds/round-1-report.md`, `…/overview.md` (line 39 and the fix-range
diff), `…/changelog.md` (the fix-range diff);
`skills/verify/scripts/broad_gate.py` (the fix-range diff, `wrapped`,
`HOME_TOKEN`, `HOME_END`, `deferred_home`, `rounds_rows`, the panel's
workflow rows, `gate_copy`, `copy_origin`, `INVOKED_AS_VAR`,
`PREFLIGHT_PASSED`, `PREFLIGHT_FAILED`, `PREFLIGHT_TAIL`, `preflight_line`, and the merge's combined diff);
`skills/verify/scripts/seal_stamp.py` (`not_sealed`, `letter`, `beside`,
`stamp`); `skills/code-review/scripts/chain_check.py` (`EMPHASIS`,
`MARKER`, `SEPARATORS`, `DEFERRED`, `NO_HOME`); `agents/sealer.md` and
`docs/the-broad-gate.md` (the fix-range diff);
`tests/test_the_gate_names_every_step_ci_runs.py` and
`tests/test_the_seal_is_taken_once_by_the_sealer.py` (the fix-range diff,
and the preflight case's assertions);
`seal/releases/0.15.7.md` N2 and N3, and `seal/releases/0.15.1.md` N3,
`seal/releases/0.15.4.md` A5 and C4, `seal/releases/0.15.7.md` N9 at
`6b421616`, `a340221b` and `613b9389`;
`seal/ledger/1790815611-the-record-arms-run-before-the-sealer-is-spawned.md`
(word diff `a340221b..613b9389`); `bin/test`.
