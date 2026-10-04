# Round 4 report — 1791076833-the-reverify-writer-records-before-it-restamps

Target `c4494a40f585642a672dd27d59afe840a668db34`, base `release/v0.18.1` at
`e141980a`. This is the verifying round the round cap allows, and the run's
last. Its target is round 3's fix range, `ab8a4ecf..ec801b76`: `13300a7a`
(the code, the case and the `Enforced by:` line) and `ec801b76` (ledger rows
C1 and W9 re-hashed). `c4494a40` closes `round-3.md` and touches nothing
else. Everything below was read and run in a `git clone --no-local` at the
target, under this session's scratchpad.

## What the account claimed, and what I found

The round's paragraph claimed two things. The first is that round 3's yellow
1 is fixed by reading `seal/config.md` with `strict=True` in the vendored
branch. The diff confirms it: one argument at
`skills/evidence-check/scripts/evidence_check.py:3737`, four comment lines
above it, and one new parametrize row on the existing
`test_a_vendored_copy_whose_config_will_not_read_leaves_the_row`. The second
is that the fix added no unit. The diff holds no new `def` or class, and the
test function existed at `a5e359d3`, so that holds too.

The comment says the copy now reads the file "as `declared_pacts` reads it".
I opened `hooks/config.py:805`. `declared_pacts` checks `os.path.lexists`,
opens with `encoding="utf-8"` and the default strict errors, and answers
None on `OSError` or `ValueError`. The vendored branch checks
`os.path.lexists`, then calls `read(declaration, strict=True)`, which opens
with `errors="strict"` and answers None on the same two exceptions
(`skills/evidence-check/scripts/evidence_check.py:1065`). The two opens are
the same, so the claim in the comment is true.

### Round 3's yellow 1 is closed

Executed: with the one argument reverted in the clone, the new row
`test_a_vendored_copy_whose_config_will_not_read_leaves_the_row[it is not
UTF-8]` fails and the 13 other vendored cases pass. Restored, it passes. So
the case is red against the defect it was written for.

The fix cannot open a new disagreement in the direction that loses a record.
Read: a strict read can only turn a text into None, and in the vendored
branch None only sets `blind`, which leaves rows. So no shape the vendored
copy left before is re-stamped now. Round 3's enumeration of the remaining
disagreements (its last 🟢) therefore still holds, and I carried it rather
than re-running P1-P16.

I then ran the shapes the strict read newly reaches through both copies
(probe Q1-Q7, below). In every shape where the file will not read, the
plugin and the vendored copy both exit 1 and leave the moved row citing no
clause: a bad byte in the `Mode` cell (round 3's P3), a bad byte inside an
HTML comment holding a `Pact notify | always` row, a bad byte with no `Pact`
row at all, a directory in the file's place, and a dangling symlink. The
only disagreement left in the probe is Q7, a valid `never` row, where the
vendored copy leaves and the plugin re-stamps; that is the documented safe
direction ("leaves too much rather than too little").

### Round 3's white 2 is closed

Read: `docs/the-pact.md:308` now names
`test_a_vendored_copy_whose_config_will_not_read_leaves_the_row`, which holds
the paragraph's "or will not read" half. Executed: the module that checks a
folded statement names what enforces it passes.

### Ledger rows C1 and W9

`ec801b76` moves only the hashes of `record_pact_changes` (to `42221904`)
and of the test case (to `79e6bba3`). Executed: `bin/evidence-check
--ledger` over the item's fragment, exit 0, 234 ok, 0 drifted, 0 broken. C1's
"or will not read" now holds for a config that is not UTF-8, as round 3
said it would. W9's claim says the files the run writes are read strictly
and names three files that keep the lenient read; neither half is made false
by a strict read of a file the run does not write, so it holds as written.

### ⬜ 1 — `read`'s docstring says every file the run only reads keeps the lenient read

`skills/evidence-check/scripts/evidence_check.py:1074-1076`:

```python
    that will not decode will not read, and its caller leaves it. A file the
    run only reads -- code under a coordinate, a released ledger -- keeps the
    lenient read, because nothing is written back to it."""
```

Round 3's fix made `seal/config.md`, in the vendored branch, the first file
the run only reads and reads strictly. The sentence states a rule, not an
example list, so it is now false for that one call. The behaviour is right
and nothing ships wrong, which is why this is ⬜. A reader who trusts the
docstring and "tidies" the vendored call back to the default would reopen
round 3's yellow 1; the case at
`tests/test_a_signatory_records_a_pact_change.py:1495` would catch that, so
the risk is a wasted round, not a lost record.

### ⬜ 2 — the spec's W9 says the same, as a frame

`seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/spec.md:236`
says "A file it only reads, such as the code under a coordinate, keeps
today's lenient read." This is the frame, under `seal/specs/`, so it is a
correction to the run's paperwork and not a fix to the tool. It is reported
apart from ⬜ 1 so each finding carries one location.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 3's yellow 1 is closed — the vendored copy reads `seal/config.md` strictly, so a config that is not UTF-8 will not read and a moved row citing no clause is left, as the plugin leaves it | `skills/evidence-check/scripts/evidence_check.py:3737` | confirmed | executed: the new row red with the argument reverted (1 failed, 13 passed) and green restored; probe Q1-Q4 and Q6, plugin and vendored both exit 1 and leave; read: `declared_pacts` and `read` with `strict=True` open the file the same way and answer None on the same exceptions |
| 🟢 | round 3's white 2 is closed — the vendored paragraph's `Enforced by:` line names the case for "or will not read" | `docs/the-pact.md:308` | confirmed | read: the line names `test_a_vendored_copy_whose_config_will_not_read_leaves_the_row`; executed: the folded-statement module passes in the narrow run |
| 🟢 | The fix opens no disagreement that loses a record: a strict read can only make `said` None, and None only leaves rows | `skills/evidence-check/scripts/evidence_check.py:3743` | confirmed | read: `blind = said is None or ...`; executed: probe Q1-Q7, no shape where the vendored copy re-stamps and the plugin leaves; round 3's P1-P16 enumeration carried, not re-run |
| 🟢 | Ledger rows C1 and W9 hold at the new hashes | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:5` | confirmed | executed: `bin/evidence-check --ledger` exit 0, 234 ok, 0 drifted, 0 broken; read: C1's "or will not read" now true for a non-UTF-8 config, W9's claim untouched by a read of a file the run does not write |
| ⬜ 1 | `read`'s docstring says a file the run only reads keeps the lenient read, and since round 3's fix the vendored branch reads `seal/config.md`, which the run only reads, strictly | `skills/evidence-check/scripts/evidence_check.py:1074` | open | read: the vendored call at `:3737` passes `strict=True` for a file nothing writes; behaviour right, the sentence wrong; the unit `read` predates the rounds (phase 2), depth 0; who answers it: the orchestrator of PR #756, a comment-only edit before the seal or deferred under the ladder |
| ⬜ 2 | The spec's W9 says a file the run only reads keeps the lenient read | `seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/spec.md:236` | open | read: same sentence as ⬜ 1, in the frame; a correction to the run's paperwork, not a fix; who answers it: the orchestrator of PR #756 |
| carried | Round 1's, round 2's and round 3's earlier confirmations (PR #749's closures, W8-W10, K1, K2, the seven round-1 units, T1/T2, the 0.18.0 P1 re-read, round 2's closures) | `skills/evidence-check/scripts/evidence_check.py:4992` | confirmed | carried from round 3; the fix range touches the vendored branch's one read, its comment, one test case, one doc line and two ledger hashes; executed: the narrow modules below, 260 passed |
| ❓ | The full suite, the repository-wide lint and the typecheck | the tree at `c4494a40` | ❓ out of verified scope | the broad gate is the sealer's, after the rounds settle; the `unverified` label it carries is honest; who answers it: the sealer |

## Paste-ready fixes

```python
# skills/evidence-check/scripts/evidence_check.py, read(), replacing the
# last sentence of the docstring (lines 1074-1076)
    that will not decode will not read, and its caller leaves it. Code under
    a coordinate and a released ledger keep the lenient read, because nothing
    is written back to them. A vendored copy's `seal/config.md` is read
    strictly although nothing writes it, because there a byte the lenient
    read replaces can hide the `Pact notify` row (round 3 of PR #756,
    yellow 1)."""
```
```markdown
seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/spec.md:236,
replacing the sentence:

A file it only reads, such as the code under a coordinate, keeps today's
lenient read; a vendored copy's `seal/config.md` is the one exception, read
strictly since round 3 of PR #756.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the writer module, the declaration module, `tests/test_pact_check.py`, the CI print module, `tests/test_no_real_identifiers.py`, the folded-statement module and `tests/test_docs_line_wrap.py` at the target | 260 passed |
| The writer module's `vendored` cases with `strict=True` removed from the vendored read, then restored | 1 failed (`[it is not UTF-8]`), 13 passed; restored, all pass |
| Probe Q1-Q7, plugin and vendored copy, for a moved row citing no clause | Q1-Q4, Q6: both exit 1, row left, nothing recorded. Q7: plugin exit 0 and re-stamped, vendored exit 1 and left (the documented safe direction) |
| `ruff check` and `ruff format --check` on the two changed Python files | both exit 0 |
| `bin/evidence-check --ledger` over this item's fragment at the target | exit 0; 234 ok, 0 drifted, 0 broken; records arm 0 refused, 0 drifted |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — not run here; it is the sealer's, after the rounds settle |

```python
# One probe file in the clone's tests/, run once, deleted. It imports the
# writer module's helpers (repo, cite, row, move_serialize, run, _vendored,
# config_text). For each seal/config.md below it cites src/orders.py#serialize
# from a row citing no clause, moves serialize, then runs
# `--reverify --into <fragment> --checked` through the plugin's script and
# through `_vendored`. It prints exit, re-stamped, recorded, first LEFT line.
# HEAD = config_text(("Mode", "shared"), ("Pact", PACT_URL))
Q1 = b"| Item | Value |\n|---|---|\n| Mode | shar\xffed |\n| Pact | URL |\n"
Q2 = HEAD + an HTML comment block holding "| Pact notify | always | \xff"
Q3 = seal/config.md replaced by a directory
Q4 = seal/config.md replaced by a dangling symlink
Q6 = b"| Item | Value |\n|---|---|\n| Note | caf\xe9 |\n"   # no Pact row
Q7 = config_text(("Mode", "shared"), ("Pact", URL), ("Pact notify", "never"))
```

The broad gate has come due. This report leaves nothing needing a fix, so
what comes due is the sealer's spawn.

Needs a fix: no
Loses a record or crashes: no

## Proof block

Files opened: `skills/evidence-check/scripts/evidence_check.py` (`read`,
`NOTIFY_ROW_SHAPE`, `record_pact_changes`), `hooks/config.py`
(`pact_declaration`, `declared_pacts`),
`tests/test_a_signatory_records_a_pact_change.py` (the `vendored` cases,
`_vendored`, `test_a_pact_row_that_will_not_read_leaves_the_row`),
`docs/the-pact.md:148-160` and `:290-310`, `skills/evidence-check/SKILL.md:325-360`,
`seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/spec.md:226-238`,
`seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md`
(rows C1 and W9 in the diff), `rounds/round-3.md`, `rounds/round-3-report.md`,
`bin/test`, and the diffs `ab8a4ecf..ec801b76` and `c4494a40`.
