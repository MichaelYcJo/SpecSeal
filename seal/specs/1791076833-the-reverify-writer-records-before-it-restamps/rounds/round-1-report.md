# 1791076833-the-reverify-writer-records-before-it-restamps — review round 1 report

Target `7517df8b` on `feat/647-the-reverify-writer-records-before-it-restamps`,
base `release/v0.18.1` at `e141980a`, PR #756. Reviewed in a `--no-local`
clone at the target; nothing was written in the smith's worktree except this
file.

## What this round was asked

The first review of the carried #647 C and D code and of the record-first
writer. Spec compliance first: Decision 1, W1–W10 (the write order and what
is on disk when the process dies at each step, the unreadable ledger,
idempotence, the cases where nothing can be recorded, `always` with an
unreadable declaration, left coordinates, honest `wrote` lines, strict reads
of files the run rewrites, a named `LEFT` instead of a traceback), and K1/K2.
Quality second. Enumerate failure points by construction, every write step
crossed with every way it can fail, and execute what is claimed. The prompt
also asked that PR #749's round 1 and round 2 findings (blocking 1 and 10,
yellow 2–5 and 11–15) be checked against the carried code, not inherited.

## Summary

The record-first order holds. Killed after each of the four writes a run
makes, and killed inside each of them, the next run leaves a tree identical
to one clean run's, byte for byte, with nothing recorded twice (ten cells,
executed). W8, W9 and W10 do what the spec says, and their six new cases are
red against the carried writer. K1 and K2 hold. Every PR #749 finding the
prompt named is closed by the code here: each fix taken back out turns its
own cases red, and round 2's independent walker generator finds no
disagreement with cmark-gfm in 600,000 documents.

Two findings remain, and they are one class: **a `Pact notify` value the
writer did not actually read is treated as read.** W6 says a moved row citing
no clause is unknown "unless the notify value was read and is not `always`",
and `docs/the-pact.md` says such a row is left wherever the declaration leaves
`always` possible. Two shapes leave it possible and are not left:

1. a copy of the checker with no `hooks/` beside it (🟡 1);
2. a `Pact notify` row written twice (🟡 2).

In both, a row citing no clause under an intended `always` is re-stamped at
exit 0 with nothing recorded, so the drift that would record the change is
gone. The class was enumerated by construction over every way
`record_pact_changes` reaches its `blind` decision. An unreadable config.md
and an invalid value are left correctly. A missing config.md and an absent
`Pact notify` row are correctly not blind. A doubled `Pact` row is left
correctly. The two shapes above are the remaining members.

Two paperwork corrections are not counted in `Needs a fix`. One of them, ⬜ 4,
turns `tests/test_no_real_identifiers.py` red at the target. That module was
not among the modules run on the branch, and the pull request's CI will fail
on it.

## Findings

### 🟡 1 — a vendored copy under `Pact notify | always` re-stamps a row citing no clause and records nothing

`skills/evidence-check/scripts/evidence_check.py:3717`.
`record_pact_changes` returns early when `plugin_module` finds no `hooks/`. It
names only the rows carrying a pact anchor (`citing = [e for e in entries if
e[3]]`) and returns 0 when there are none. A copy that has no `hooks/` reads
no `Pact notify` value either, so it cannot know that a row citing no clause
is not owed.

Executed: a signatory with `Pact | git@example.com:org/orders-api.git` and
`Pact notify | always`, and a fragment row citing no clause whose code moved.
The copy under `tools/` was run with `--reverify --into`. It exited 0, re-stamped the
row, wrote no record and printed `1 row re-verified`. The plugin's own copy,
run next, found nothing moved and recorded nothing. The pact change is lost
for good.

Why it matters: the spec's W5 lists "this copy has no `hooks/`" as a cause
that re-stamps nothing where a change is owed, and W6 makes the row unknown
here. `docs/the-pact.md:134` says that where the copy has no `hooks/` "the run
writes no ledger file at all", and `docs/the-pact.md:300` says it "re-stamps
nothing". Both are false for a row citing no clause under `always`.

The fix leaves every moved row where the signatory's config.md has a
`Pact notify` row, or will not read. A copy with no `hooks/` can see that the
row exists but cannot read its value. Where config.md has no such row, the
default records only citing rows, and the copy still re-stamps the rest. Both
new cases are fenced below. Executed in the clone: the first is red without
the fix and green with it, the counter-case is green either way, and four
modules give 184 passed.

### 🟡 2 — a `Pact notify` row written twice reads its first value as known

`skills/evidence-check/scripts/evidence_check.py:3737`.
`blind` is `declared[1] in (None, NOTIFY_ALWAYS)`. `pact_declaration` refuses
a doubled `Pact notify` row but still returns the first row's value
(`hooks/config.py:783` to `:796`). With `never` or `when the pact is touched`
written first and `always` second, `blind` is false. A row citing no clause
is then neither in `unknown` nor owed.

Executed, for both first values: exit 0, the row re-stamped, no record, and
no line naming the refusal. The run is silent about the doubled row
altogether. `pact-check` at the pact's repository will refuse the signatory's
config, but the change itself is never recorded.

Why it matters: `docs/the-pact.md:133` to `:135` says the run writes no ledger
file for "`Pact` rows that will not read (for a moved row citing no clause,
wherever they leave `always` possible)". A doubled row leaves `always`
possible. This is the shape PR #749's yellow 13 did not name. Its two named
shapes, an invalid value and an unparseable `Pact` row with `always`, are
left correctly at the target.

The fix is in the writer and not in `pact_declaration`. That function is
shared with `chain_check.py` and `pact_check.py`, and both already treat any
refusal as a refusal, so changing what it returns would move their output.
Here the writer treats a refused `Pact notify` row as having no value.
Executed in the clone: both parametrisations red without the fix and green
with it.

### ⬜ 3 — two ledger claim rows share labels with the spec's contract clauses

`seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:1`
and `:2`. The carried rows `W1 ·` (the table walker) and `W2 ·` (`cmarkgfm`)
sit beside the new rows `W8 ·`, `W9 ·` and `W10 ·`, which are the spec's
writer-contract clauses. A reader following "W1" from the spec's §*The
writer's contract* to the ledger lands on the walker claim. That is a
correction to the run's paperwork, not a defect in the tool, and it is not
counted in `Needs a fix`. Relabelling the two carried rows, for example to
`T1 ·` and `T2 ·`, before anything cites them removes the collision.

### ⬜ 4 — this item's `plan.md` writes a real user path, and the identifier check is red at the target

`seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/plan.md:24`.
The line names the worktree that holds PR #749's branch by its absolute path,
under a real home directory. `tests/test_no_real_identifiers.py` fails at the
target with this report absent (`test_only_fixture_user_paths`, executed). The
line came in with the frame commit `20f2207c`. That module is not one of the
12 changed modules the orchestrator ran, so nothing on the branch has run it.
It will fail the pull request's pytest job on all three platforms.

It sits under `seal/specs/`, so it is a correction to the run's paperwork and
is not counted in `Needs a fix`. It is still the one thing here CI will
refuse. Write the path relative to the worktrees directory, or as
`/Users/x/…`, as `CLAUDE.md` §*Repo rule — no real identifiers in examples
or fixtures* says.

## What was checked and closed

### PR #749's findings, against the carried code

Each fix was taken back out of the clone and its module run, then the file
was restored:

| Fix taken out | Cases red |
|---|---|
| plan applied before the record (blocking 1, blocking 10, yellow 11) | 17 cases, among them the five paths blocking 1 named, the vendored, record and `Pact`-row cases, both kill cases and the unreadable-sibling case |
| raw comparison instead of the reader's (yellow 2) | 3 |
| ever-recorded instead of the record's last word (yellow 12) | 2 |
| `blind` forced false (yellow 13) | the two `always` parametrisations |
| no move appended for a coordinate the re-read leaves (yellow 14) | 3 |
| `amended` judged at any hash (yellow 3) | 1 |
| no near miss (yellow 4) | 7 |
| the three walker refusals off (yellow 5, yellow 15) | 474 |
| even-backslash pipe splits (white 6) | 2 |

Blocking 10 is closed by construction as well. The only file removal left in
`evidence_check.py` is `write_atomic`'s cleanup of its own temporary sibling
(`evidence_check.py:1169`). A non-UTF-8 `--into` is refused at exit 2 and
left byte for byte (executed). Yellow 11 is closed by the order itself, as the
kill matrix below shows: no step re-stamps before the record.

### The writer's contract

- **W1, W2**: by construction. A run with three fragments, one of them the
  `--into` that also takes a `Re-read ·` row, and a released row makes four
  writes: the record, then three ledgers. Killed after each write, and killed
  inside each one with a half-written temporary sibling left behind, the next
  run's tree equals a clean run's in every file. The record was never
  appended twice. A leftover `<name>.md.<random>` is read by nothing.
- **W3**: an unreadable sibling fragment is named and kept (carried case,
  red under the apply-first mutation). A non-decoding fragment is
  `ledger unreadable` and left byte for byte (phase 2 case).
- **W4**: second run byte-identical, reland recorded, piped coordinates once
  (mutations above).
- **W5**: no work item, executed in place. The output carries the `LEFT` line
  and `PACT_CHANGE_UNDONE` and no hash line, `re-verified` or `dated` line.
  The other causes are covered by the carried cases red under the apply-first
  mutation.
- **W6**: closed for an unreadable config.md, an invalid value, a missing
  config.md and an absent row. Not closed for the two shapes in 🟡 1 and 🟡 2.
- **W7**: three exits record `BROKEN` (yellow 14's mutation).
- **W8, W9, W10**: the six phase-2 cases for them fail against
  `evidence_check.py` at `2d2387fd` (the carry commit) and pass at the target.
  The four phase-2 cases that pass there pin carried behaviour (W1, W2, W6's
  missing-file arm). Read: `told_now` holds every write-claiming line, and
  `landed_at` filters by the planned keys that landed. `apply_plan` catches
  only `OSError`, which is every failure `write_atomic` and `makedirs` raise
  for a text the run decoded strictly or leniently.
- **The output order**: W8 moves every `--reverify` run's hash lines below its
  `LEFT` lines, pact or not. No document carries an example of the old order.
  The 17 unchanged modules that drive `--reverify` pass at the target (1046
  passed).

### K1, K2 and Decision 1

`git diff b4c9deb2 2d2387fd` over the 30 carry-set paths changes 31 lines.
Each is a marker rename or a citation of PR #749's round. The one line that
names neither is the second half of a citation wrapped across two lines in
`hooks/config.py`. That matches the overview's count of 19 against the frame's
17. Every later change to a carry-set path is in the three phase-2 commits.
One path outside the carry set changed, `tests/test_gates_do_not_fail_open.py`:
its stub of `read` takes `strict`, which W9's new signature requires.
`git grep 1791019474` at the target outside this item's own records matches
nothing.

## Regression tests to plant

Destination `tests/test_a_signatory_records_a_pact_change.py`, three cases,
fenced under 🟡 1 and 🟡 2 below. Each was seen red against the target and
green with its fix (§15). `docs/the-pact.md`'s two sentences change with
🟡 1's fix, so the sentence pin (§14) moves with them. It is the
parametrised case `test_the_documents_say_what_the_writer_does`, or a new row
beside `test_a_vendored_copy_says_it_recorded_nothing` in `Enforced by`.

## Facts for the evidence ledger

- The record-first order survives a kill after, or inside, every one of a
  run's writes, and the next run's tree equals one clean run's (executed,
  ten cells). This could back the claim row `C1 ·` with a case that walks
  the write count rather than one cell.
- Round 2 of PR #749's generator at the target: seed 11 gives 30,188 agree and
  269,812 refused; seed 23 gives 29,798 agree and 270,202 refused; no
  disagreement and no oracle mismatch in either.

## Not verified

| Item | Who answers it |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once the rounds settle. The smith handed it over labelled `unverified`, and that label is honest |
| The W10 and `--into` step-3 cases on Windows and as root | the repository owner, as the overview already states. Not re-judged here |
| Lint of the paste-ready fixes | the smith, at the fix pass; they were run, not linted |
| The suite's other modules that read every tracked file's text, beyond `tests/test_no_real_identifiers.py` and the two the branch changed | the sealer, in the broad gate |

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A copy with no `hooks/`, under `Pact notify \| always`, re-stamps a moved row citing no clause at exit 0 and records nothing; the plugin's copy then finds nothing to record | `skills/evidence-check/scripts/evidence_check.py:3717` | open | executed in a temporary signatory; contradicts spec W5 and W6 and `docs/the-pact.md:134` and `:300`; fix run in the clone: red then green, 184 passed |
| 🟡 2 | A `Pact notify` row written twice is read as its first value, so with `never` or the default first and `always` second a moved row citing no clause is re-stamped at exit 0, unrecorded and unannounced | `skills/evidence-check/scripts/evidence_check.py:3737` | open | executed for both first values; contradicts spec W6 and `docs/the-pact.md:133`; fix run in the clone: red then green |
| ⬜ 3 | Ledger claim rows `W1 ·` and `W2 ·` (walker, `cmarkgfm`) share labels with the spec's writer-contract clauses W1 and W2, beside rows `W8 ·` to `W10 ·`, which are those clauses | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:1` | open | read; a correction to the run's paperwork, not counted in `Needs a fix` |
| ⬜ 4 | This item's `plan.md` names a worktree by an absolute path under a real home directory, so `tests/test_no_real_identifiers.py` fails at the target | `seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/plan.md:24` | open | executed: `test_only_fixture_user_paths` fails at `7517df8b`; came in with `20f2207c`; a correction to the run's paperwork, not counted in `Needs a fix`, and the pull request's pytest job will fail on it |
| 🟢 | PR #749 round 1's blocking finding 1 is closed: an owed change that cannot be recorded re-stamps nothing on the five paths it named | `skills/evidence-check/scripts/evidence_check.py:4992` | confirmed | executed: 17 cases red with the plan applied before the record; in place with no work item, no claim line and the ledger kept. The vendored path's `always` arm is this round's yellow 1 |
| 🟢 | PR #749 round 2's blocking finding 10 is closed: no step removes a ledger, and an `--into` that will not read is refused before anything is written | `skills/evidence-check/scripts/evidence_check.py:4962` | confirmed | read: the only removal is `write_atomic`'s temporary file; executed: the sibling case red under the apply-first mutation, a non-UTF-8 `--into` exit 2 and byte for byte |
| 🟢 | PR #749 round 2's yellow 11 is closed: no window between a re-stamp and its record remains | `skills/evidence-check/scripts/evidence_check.py:4992` | confirmed | executed: the kill matrix, ten cells, each next run equal to a clean run |
| 🟢 | PR #749 round 1's yellow 2 is closed: a second identical run adds nothing, compared as the reader reads a cell | `skills/evidence-check/scripts/evidence_check.py:3821` | confirmed | executed: 3 cases red with the raw comparison |
| 🟢 | PR #749 round 2's yellow 12 is closed: a change re-landed after its revert is recorded | `skills/evidence-check/scripts/evidence_check.py:3813` | confirmed | executed: 2 cases red with the ever-recorded key |
| 🟢 | PR #749 round 2's yellow 13 is closed for the two shapes it named: an invalid `Pact notify` value, and an unparseable `Pact` row under `always` | `skills/evidence-check/scripts/evidence_check.py:3737` | confirmed | executed: both parametrisations red with `blind` forced false. The doubled-row shape is this round's yellow 2 |
| 🟢 | PR #749 round 2's yellow 14 is closed: a coordinate the re-read leaves is recorded `BROKEN` at all three exits | `skills/evidence-check/scripts/evidence_check.py:3133` | confirmed | executed: 3 cases red with the moves removed |
| 🟢 | PR #749 round 1's yellow 3 is closed: `amended` is judged at the record's current hash only | `skills/evidence-check/scripts/pact_check.py:848` | confirmed | executed: 1 case red |
| 🟢 | PR #749 round 1's yellow 4 is closed: `.`, `-` or `_` for or before the slash is refused | `skills/evidence-check/scripts/pact_check.py:240` | confirmed | executed: 7 cases red |
| 🟢 | PR #749 round 1's yellow 5 and round 2's yellow 15 are closed: the walker refuses what cmark-gfm does not render | `hooks/config.py:1050` | confirmed | executed: 474 cases red with the three refusals off; round 2's generator, 600,000 documents over seeds 11 and 23, no disagreement |
| 🟢 | PR #749 round 1's white 6 is closed: a pipe after an even backslash run is refused | `hooks/config.py:907` | confirmed | executed: 2 cases red |
| 🟢 | W8, W9 and W10 hold: no write claim before the write lands, strict reads of what the run writes, and a named `LEFT` line instead of a traceback | `skills/evidence-check/scripts/evidence_check.py:1097` | confirmed | executed: the six phase-2 cases fail against the carry commit's writer and pass at the target |
| 🟢 | K1 and K2 hold: the carry diff is marker renames and citations alone, and the tree names no work item it does not hold | `docs/the-pact.md` | confirmed | executed: `git diff b4c9deb2 2d2387fd` over the carry set, 31 lines, each a marker or a citation; `git grep 1791019474` outside this item's records, nothing |
| ❓ | The full suite, the repository-wide lint and the typecheck | the tree at `7517df8b` | ❓ out of verified scope | the broad gate is the sealer's, after the rounds settle; the smith's `unverified` label is honest |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the writer module, the two pact-check modules and `tests/test_gates_do_not_fail_open.py` at the target | 145 passed |
| `bin/test` over the 17 unchanged modules that drive `--reverify` | 1046 passed |
| `bin/test` over the 12 changed test modules | 1236 passed |
| Round probes in a temporary signatory: a vendored copy under `always`; a doubled `Pact notify`; three record header spellings; in place with no work item; a non-UTF-8 `--into` | 🟡 1 and 🟡 2 reproduced; the header spellings append under the header with no traceback; no claim line without a write; `--into` refused at exit 2, byte for byte |
| Kill matrix: a kill after each write and a kill inside each write (temporary sibling half-written), then a normal run, compared file by file with one clean run | all ten cells equal to the clean run; the record never appended twice |
| The same matrix with `--checked` older than the rows' own dates | a second `Re-read ·` row on any re-run; the same at `e141980a` and `b4c9deb2` with no pact; #746's stale `--checked`, deferred below |
| The six W8–W10 cases against `evidence_check.py` from `2d2387fd` | 6 failed, 4 passed (the four pin carried behaviour) |
| Nine mutations, each fix of PR #749's rounds taken back out, its module run, the file restored | every mutation red, counts in the table above |
| Round 2 of PR #749's generator, 300,000 documents, seeds 11 and 23 | 0 disagreements, 0 oracle mismatches |
| The paste-ready fixes below, applied in the clone with their cases, then reverted | new cases 3 red without the code fix, 4 green with it; the writer, `test_pact_check.py`, the review module and the declaration module 184 passed |
| `bin/evidence-check --ledger` over this item's fragment | exit 0; 223 ok, 0 drifted, 0 broken; records arm 0 refused, 0 drifted |
| `tests/test_no_real_identifiers.py` at the target | 1 failed, 4 passed: `test_only_fixture_user_paths` on this item's `plan.md:24` (⬜ 4) |
| This report, copied into the clone and marked for adding (not committed), through the records arm and the identifier check, then removed | records arm 0 refused, 0 drifted; the identifier check names `plan.md:24` alone, nothing in this report |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — not run here; it is the sealer's, after the rounds settle |

### Kill matrix

```python
# Fixture: the freeze, a released row R1 citing the clause, and three
# fragments (the --into one among them) each with a citing row; the code
# under all four moved. Four writes: the record, then the three ledgers.
# For k in 1..5 and mid in (False, True): write_atomic is wrapped to die
# (os._exit(137)) after its k-th call, or, with mid, inside its k-th call
# after writing half of a temporary sibling. Then a normal --reverify --into
# --checked runs, and every file under seal/ is compared with one clean run.
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A second `--reverify --into` with a `--checked` older than the released row's own date appends a second identical `Re-read ·` row, because the new row is not the family's newest reading; the same at `e141980a` with no pact | #746, a stale `--checked` under `--into`, which the spec keeps out of this item | #746's work item, in this release |
| `--migrate` reads a ledger leniently and writes it back (`evidence_check.py:2725` and `:2845`), so a byte that is not UTF-8 becomes U+FFFD. This is W9's class outside `--reverify`, in code this branch does not touch | a new issue | the orchestrator, who files it |

## Paste-ready fixes

### 🟡 1 — the vendored copy reads whether a `Pact notify` row is there

```python
# beside NOT_RESTAMPED in skills/evidence-check/scripts/evidence_check.py
# A `Pact notify` row as a copy with no `hooks/` can see one: its item cell,
# whatever the value says, because that copy cannot read the value.
NOTIFY_ROW_RE = re.compile(r"^[ \t]{0,3}\|[ \t]*Pact notify[ \t]*\|", re.M | re.I)
```

```python
    config = plugin_module(CONFIG_READER, "specseal_config_for_pact_changes")
    if config is None:
        # A copy with no `hooks/` reads no `Pact notify` value either, so
        # where the signatory's config.md has a `Pact notify` row, or will not
        # read, a moved row citing no clause may be owed under `always`, and
        # this copy cannot rule it out (the writer's contract, W5 and W6).
        declaration = os.path.join(seal_home(root), "config.md")
        said = read(declaration) if os.path.lexists(declaration) else ""
        blind = said is None or bool(NOTIFY_ROW_RE.search(said))
        unknown = [e for e in entries if e[3] or blind]
        for where, _row, _parts, anchors in unknown:
            why = (
                "cites a pact clause"
                if anchors
                else "moved, and `Pact notify` may be `always`"
            )
            print(
                f"  LEFT  {where}  {why}, and this copy of evidence_check.py "
                "has no hooks/ beside it to read the `Pact` row with — "
                f"{NOT_RESTAMPED}; run the plugin's `evidence-check --reverify` "
                "where the signatory is checked out"
            )
        return 1 if unknown else 0
```

```markdown
`hooks/` beside it cannot read the `Pact` row; it names each row citing a
pact, and each other row whose code moved where `seal/config.md` has a `Pact
notify` row it cannot read, says it recorded nothing, and re-stamps nothing,
so the plugin's own checker records the change where the signatory is
checked out.
```

```python
def test_a_vendored_copy_under_a_notify_row_leaves_a_row_citing_no_clause(
    repo, tmp_path
):
    """A copy with no `hooks/` cannot read `Pact notify`, so under a
    `Pact notify` row a moved row citing no clause is left, not re-stamped
    (round 1, yellow 1)."""
    (repo / "seal" / "config.md").write_text(
        config_text(("Mode", "shared"), ("Pact", PACT_URL), ("Pact notify", "always")),
        encoding="utf-8",
    )
    vendored = tmp_path / "tools" / "evidence_check.py"
    vendored.parent.mkdir()
    vendored.write_text(open(SCRIPT, encoding="utf-8").read(), encoding="utf-8")
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O2", "", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    done = subprocess.run(
        [sys.executable, str(vendored), "--reverify", "--into", FRAGMENT,
         "--checked", "2026-09-04", str(repo)],
        cwd=str(repo), capture_output=True, encoding="utf-8", errors="replace",
    )
    out = done.stdout + done.stderr
    assert done.returncode == 1, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
    assert "moved, and `Pact notify` may be `always`, and this copy of" in out, out


def test_a_vendored_copy_with_no_notify_row_restamps_a_row_citing_no_clause(
    repo, tmp_path
):
    """With no `Pact notify` row the default records citing rows alone, so
    the vendored copy still re-stamps a row citing no clause."""
    vendored = tmp_path / "tools" / "evidence_check.py"
    vendored.parent.mkdir()
    vendored.write_text(open(SCRIPT, encoding="utf-8").read(), encoding="utf-8")
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger = cite(repo, [row("O2", "", f"src/orders.py#serialize@{old}")])
    new = move_serialize(repo)
    done = subprocess.run(
        [sys.executable, str(vendored), "--reverify", "--into", FRAGMENT,
         "--checked", "2026-09-04", str(repo)],
        cwd=str(repo), capture_output=True, encoding="utf-8", errors="replace",
    )
    out = done.stdout + done.stderr
    assert done.returncode == 0, out
    assert f"@{new}" in ledger.read_text(encoding="utf-8"), out
```

### 🟡 2 — a refused `Pact notify` row has no value

```python
    # A row citing a pact is owed under any `Pact notify`; a row citing none
    # is owed under `always`, and a declaration that will not read cannot say
    # it is not `always`, so such a row is unknown (round 2 of PR #749,
    # yellow 13). A `Pact notify` row refused -- written twice, say -- has no
    # value either, whatever its first row says (round 1, yellow 2).
    notify_refused = declared is not None and any(
        refusal.startswith(f"`{config.PACT_NOTIFY_ROW}") for refusal in declared[2]
    )
    blind = (
        declared is None
        or declared[1] in (None, config.NOTIFY_ALWAYS)
        or notify_refused
    )
```

```python
@pytest.mark.parametrize("first", ["never", "when the pact is touched"])
def test_a_notify_row_written_twice_leaves_a_row_citing_no_clause(repo, first):
    """A `Pact notify` row written twice is refused and has no value, so a
    moved row citing no clause is left, not re-stamped (round 1, yellow 2)."""
    (repo / "seal" / "config.md").write_text(
        config_text(
            ("Mode", "shared"),
            ("Pact", PACT_URL),
            ("Pact notify", first),
            ("Pact notify", "always"),
        ),
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O2", "", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1 and "`Pact notify` may be `always`" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
```

Needs a fix: yes — 🟡 1 (a vendored copy under `always` re-stamps a row citing no clause unrecorded), 🟡 2 (a doubled `Pact notify` row is read as its first value)
Loses a record or crashes: yes — 🟡 1 and 🟡 2 each re-stamp a moved row whose pact change `always` owes, with nothing recorded, so the drift that would record it is gone

## Proof

Files opened at the target: `skills/evidence-check/scripts/evidence_check.py`
(`read`, `put`, `apply_plan`, `told_now`, `landed_at`, `write_atomic`,
`reverify`, `released_drift`, `reverify_into`, `record_pact_changes`,
`plugin_module`, `pact_change_item`, `main`'s `--reverify` arm),
`skills/evidence-check/scripts/pact_check.py` (`read`, `pact_reviews`,
`pact_changes`), `hooks/config.py` (`declared_pacts`, `pact_declaration`,
`table_cells`, `pact_changes`), `tests/test_a_signatory_records_a_pact_change.py`,
`tests/test_gates_do_not_fail_open.py` (its diff), `docs/the-pact.md`
(§*A signatory records a pact change* to §*What this does not see*),
`skills/evidence-check/SKILL.md` (its diff), this item's `spec.md`,
`overview.md`, `survivors.md`, `changelog.md` and ledger fragment, and PR
#749's `rounds/round-1.md` and `rounds/round-2.md` at `b4c9deb2`.
