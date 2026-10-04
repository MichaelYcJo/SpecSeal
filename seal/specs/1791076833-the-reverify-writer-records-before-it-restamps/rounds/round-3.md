# 1791076833-the-reverify-writer-records-before-it-restamps — review round 3

| Field | Value |
|---|---|
| Target SHA | bfb7d0b7d8e270cb6a8381bdfb289ceff831ac37 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #756 |
| Broad gate | not yet |
| Fixes checked by | round-4 |
| Fix range | `ab8a4ecff78f2a321786843f72ca3a7c434e6e28..ec801b766ac015be2b0bd458242ebaabf78e64b1`, 2 commits |
| Contract changes | test_a_vendored_copy_whose_config_will_not_read_leaves_the_row → round-3-report.md, round-3.md |
| New units | none |
| Needs a fix | yes — 🟡 1 (the vendored copy reads `seal/config.md` leniently, so a config that is not UTF-8 is never "will not read", and a moved row the plugin leaves is re-stamped unrecorded) |
| Loses a record or crashes | yes — 🟡 1 re-stamps a moved row citing no clause where a bad byte hides a `Pact notify` row whose value is `always`; the plugin cannot rule `always` out there, and once the byte is repaired the change is owed with its drift already gone |

- [x] Pass

## What this round was asked

Round 3 of work item `1791076833-the-reverify-writer-records-before-it-restamps` (#647 steps C and D, PR #756). This is the verifying round for round 2's fixes, over the range `aa4546f0..a94914a0`. Round 2 reopened the run, so this round is the last one that can close on a fix. If it opens anything needing a fix, the run ends capped.

Round 2's fix changed only the body of `NOTIFY_ROW_SHAPE` and the vendored branch inside `record_pact_changes`. It now matches a `Pact` or `Pact notify` row that carries a value, reads cell space as `\s`, matches each `str.splitlines` line, and treats the declaration as blind only when both rows are present. It added no unit. Its cases are new parametrize rows on existing test functions.

Open each fix, and judge whether each round-2 verdict is closed. Watch for what the reader and the vendored shape still disagree on. Report what you find at the depth it sits.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The vendored copy reads `seal/config.md` leniently, so a byte that is not UTF-8 becomes U+FFFD. That never makes the file "will not read", and it can hide a `Pact notify` row. Under `\| Pact notify\xff \| always \|` the plugin leaves the moved row citing no clause (exit 1) and the vendored copy re-stamps it unrecorded (exit 0). The code comment, `docs/the-pact.md:302`, `skills/evidence-check/SKILL.md:337` and ledger row C1 all promise the row is left | `skills/evidence-check/scripts/evidence_check.py:3734` | **fixed** `13300a7a` | fixed at 13300a7a; executed: probe P4, plugin exit 1 and left, vendored exit 0 and re-stamped; P3 (bad byte in `Mode`, no notify row) disagrees the same way; read: `read` defaults to `errors="replace"`, `hooks/config.py#declared_pacts` reads strictly; with `strict=True` both match the plugin and the new row is red without it; line from `a5e359d3`, round 1's fix, depth 1; no unit added |
| ⬜ 2 | The vendored-copy paragraph's `Enforced by:` line names no case for its "or will not read" half | `docs/the-pact.md:308` | answered | corrected at `13300a7a`: `docs/the-pact.md`'s vendored paragraph's `Enforced by:` line names `test_a_vendored_copy_whose_config_will_not_read_leaves_the_row`; read: `test_a_vendored_copy_whose_config_will_not_read_leaves_the_row` holds that half and is not listed; no behaviour wrong |
| 🟢 | round 2's yellow 1 is closed — the vendored copy leaves a moved row citing no clause beside U+00A0 or U+3000, or after U+2028, where the plugin records it | `skills/evidence-check/scripts/evidence_check.py:3650` | confirmed | executed: the three new rows fail against `aa4546f0`'s script and pass at the target; probe P7-P9, P12-P14 (U+0085, U+001E, lone CR, U+2029, tabs, `ALWAYS`): plugin records, vendored leaves; read: the reader takes no row with a value the shape misses |
| 🟢 | round 2's yellow 2 is closed — the template's empty rows and a notify row with no `Pact` row are re-stamped at exit 0 by the vendored copy, as by the plugin | `skills/evidence-check/scripts/evidence_check.py:3740` | confirmed | executed: the two new rows fail against `aa4546f0`'s script and pass at the target |
| 🟢 | round 2's white 3 is closed — a doubled `Pact notify` row's `pact-check` `READ` line and the CI print are pinned | `tests/test_pact_check.py:273` | confirmed | executed: both new rows fail with `9d2c1579`'s `hooks/config.py` and pass at the target |
| 🟢 | round 2's white 4 is closed — ledger row C1 says what the shape finds | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:5` | confirmed | read against the code at the target; its "or will not read" half becomes true with yellow 1's fix, so no second correction is owed; executed: `bin/evidence-check --ledger` exit 0, 234 ok |
| 🟢 | The disagreements left after yellow 1 cannot lose a record: the vendored copy leaves where the plugin re-stamps (fence, comment, byte-order mark), or re-stamps only where no row carries a value that could be `always` (doubled empty notify rows, a doubled `Pact` row with the first empty and no notify row) | `skills/evidence-check/scripts/evidence_check.py:3740` | confirmed | executed: probe P1, P2, P5, P6, P15, P16; read: the plugin leaves P1 and P2 because a doubled row is a refusal, not because `always` is possible |
| carried | Round 1's and round 2's earlier confirmations (PR #749's closures, W8-W10, K1, K2, the seven round-1 units, T1/T2, the 0.18.0 P1 re-read) | `skills/evidence-check/scripts/evidence_check.py:4992` | confirmed | carried from round 2; the fix range touches only the vendored branch and its comment; executed: the four pact modules and the identifier module, 192 passed |
| ❓ | The full suite, the repository-wide lint and the typecheck | the tree at `bfb7d0b7` | ❓ out of verified scope | the broad gate is the sealer's, after the rounds settle; the `unverified` label it carries is honest |

## Paste-ready fixes

```python
# skills/evidence-check/scripts/evidence_check.py, record_pact_changes, the
# vendored branch: the end of the comment and the `said = ...` line
        # can mean `always` (round 2 of PR #756, yellow 2). It is read
        # strictly, as `declared_pacts` reads it: a lenient read turns a byte
        # that is not UTF-8 into U+FFFD, which can hide the row the plugin
        # refuses to rule out (round 3 of PR #756, yellow 1).
        declaration = os.path.join(seal_home(root), "config.md")
        said = read(declaration, strict=True) if os.path.lexists(declaration) else ""
```
```python
# tests/test_a_signatory_records_a_pact_change.py, replacing the decorator,
# signature, docstring and the chmod block of
# test_a_vendored_copy_whose_config_will_not_read_leaves_the_row
@pytest.mark.parametrize(
    "shape",
    [
        pytest.param("it cannot be opened", marks=UNREADABLE),
        "it is not UTF-8",
    ],
)
def test_a_vendored_copy_whose_config_will_not_read_leaves_the_row(
    repo, tmp_path, shape
):
    """A `seal/config.md` the vendored copy cannot open, or one that is not
    UTF-8, cannot rule `always` out either, so a moved row citing no clause
    is left, as the plugin's own reader leaves it (round 3 of PR #756,
    yellow 1). Read leniently, the byte below hides the notify row."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger_rows = [row("O2", "", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, ledger_rows)
    move_serialize(repo)
    config = repo / "seal" / "config.md"
    if shape == "it is not UTF-8":
        config.write_bytes(
            config_text(("Mode", "shared"), ("Pact", PACT_URL)).encode("utf-8")
            + b"| Pact notify\xff | always |\n"
        )
        code, out = _vendored(repo, tmp_path)
    else:
        os.chmod(config, 0)
        try:
            code, out = _vendored(repo, tmp_path)
        finally:
            os.chmod(config, 0o644)
    assert code == 1 and "may be `always`" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(ledger_rows), out
```
```markdown
docs/the-pact.md:308, replacing the line:

Enforced by: tests/test_a_signatory_records_a_pact_change.py::test_a_vendored_copy_says_it_recorded_nothing, tests/test_a_signatory_records_a_pact_change.py::test_a_vendored_copy_under_a_notify_row_leaves_a_row_citing_no_clause, tests/test_a_signatory_records_a_pact_change.py::test_a_vendored_copy_with_no_notify_row_restamps_a_row_citing_no_clause, tests/test_a_signatory_records_a_pact_change.py::test_a_vendored_copy_whose_config_will_not_read_leaves_the_row
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the writer module, the declaration module, `tests/test_pact_check.py`, the CI print module and `tests/test_no_real_identifiers.py` at the target | 192 passed |
| The writer module's `vendored` cases against `aa4546f0`'s `evidence_check.py`, then restored | the 5 new rows failed; the 8 others passed (they pin carried behaviour, and the documents are at the target) |
| The two white-3 rows against `9d2c1579`'s `hooks/config.py`, then restored | both failed; the 3 sibling rows passed |
| Probe P1-P16, plugin and vendored copy, for a moved row citing no clause | P7-P9, P12-P14: plugin 0 and recorded, vendored 1 and left. P5, P6, P15, P16: plugin 0 and re-stamped, vendored 1 and left. P10, P11: both 1 and left. P1, P2: plugin 1 and left, vendored 0 and re-stamped, with no value that could be `always`. P3, P4: plugin 1 and left, vendored 0 and re-stamped (yellow 1) |
| Yellow 1's fix and its row, applied in the clone, then reverted | the new row failed without the code change and passed with it; P3 and P4 then matched the plugin; the four pact modules, 188 passed; `ruff check` and `ruff format --check` clean on both files |
| `bin/evidence-check --ledger` over this item's fragment at the target | exit 0; 234 ok, 0 drifted, 0 broken; records arm 0 refused, 0 drifted |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — not run here; it is the sealer's, after the rounds settle |

```python
# One file in the clone's tests/, run once, deleted. It imports the writer
# module's helpers (repo, cite, row, move_serialize, run, _vendored). For each
# seal/config.md below it cites src/orders.py#serialize from a row citing no
# clause, moves serialize, then runs `--reverify --into <fragment> --checked`
# through the plugin's script and through `_vendored` (the script alone, no
# hooks/, no SKILL.md). It prints exit, re-stamped, recorded, first LEFT line.
# HEAD = "| Item | Value |\n|---|---|\n| Mode | shared |\n"; URL = PACT_URL
P1  = HEAD + "| Pact | URL |\n| Pact notify |  |\n| Pact notify |  |\n"
P2  = HEAD + "| Pact |  |\n| Pact | URL |\n"
P3  = b"...| Mode | shar\xffed |\n| Pact | URL |\n"
P4  = HEAD + b"| Pact | URL |\n| Pact notify\xff | always |\n"
P5  = notify `always` row inside a ``` fence below the table
P6  = notify `always` row inside an HTML comment block below the table
P7  = "| Pact | URL |" U+0085 "| Pact notify | always |"
P8  = "| Pact | URL |" U+001E "| Pact notify | always |"
P9  = every line ended by a lone CR
P10 = "| Pact notify | \\| |"
P11 = "| Pact | ; |" + "| Pact notify | always |"
P12 = "| Pact notify | ALWAYS |"
P13 = "| Pact | URL |" U+2029 "| Pact notify | always |"
P14 = tab-only cell spacing on both rows
P15 = a byte-order mark before HEAD
P16 = a byte-order mark on the header line, no Mode row
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3717` | round 1's 🟡 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3737` | round 1's 🟡 2 — fixed |
| round-1 | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:1` | round 1's ⬜ 3 — answered |
| round-1 | `seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/plan.md:24` | round 1's ⬜ 4 — answered |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:4992` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:4962` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3821` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3813` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3133` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:848` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:240` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:1050` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:907` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:1097` | round 1's 🟢 — confirmed |
| round-1 | `docs/the-pact.md` | round 1's 🟢 — confirmed |
| round-1 | the tree at `7517df8b` | round 1's ❓ — out of verified scope |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3645` | round 2's 🟡 1 — fixed |
| round-2 | `skills/code-review/scripts/chain_check.py:4048` | round 2's ⬜ 3 — fixed |
| round-2 | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:5` | round 2's ⬜ 4 — answered |
| round-2 | `skills/evidence-check/scripts/evidence_check.py:3729` | round 2's 🟢 — confirmed |
| round-2 | `hooks/config.py:786` | round 2's 🟢 — confirmed |
| round-2 | `tests/test_a_signatory_records_a_pact_change.py:1356` | round 2's 🟢 — confirmed |
| round-2 | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:65` | round 2's 🟢 — confirmed |
| round-2 | the tree at `bc30a10d` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
