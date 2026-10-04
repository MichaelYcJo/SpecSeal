# Round 3 report — 1791076833-the-reverify-writer-records-before-it-restamps

Target `bfb7d0b7d8e270cb6a8381bdfb289ceff831ac37`, base `release/v0.18.1` at
`e141980a`. This is the verifying round for round 2's fixes, over the range
`aa4546f0..a94914a0`. It was read in a `git clone --no-local` at the target,
and every probe ran there.

## What the account claimed, and what I found

The round's paragraph claimed three things. The first is that round 2's fix
changed only the body of `NOTIFY_ROW_SHAPE` and the vendored branch inside
`record_pact_changes`, and added no unit. The diff confirms it: it holds no
new `def` or class, and its cases are new parametrize rows on existing test
functions. The second is that the shape now matches a `Pact` or `Pact
notify` row with a value, line by line as `str.splitlines` cuts the file,
with `\s`, and is blind only where both rows are present. The code at
`skills/evidence-check/scripts/evidence_check.py:3650` and `:3734-3740` does
that. The third is that each round-2 verdict is closed. Round 2's two yellows
and two whites are closed, and each closure is below with its grounds.

The paragraph asked what the plugin's reader and the vendored copy still
disagree on. I enumerated that class by construction rather than by example.
For a moved row citing no clause, I listed each state `pact_declaration`
and `declared_pacts` can reach, and asked what the vendored branch does in
each. I then ran sixteen config files through both copies (probe P1-P16).
The disagreements fall into two directions.

- **The vendored copy leaves a row the plugin re-stamps.** This happens with
  a notify row inside a fence or an HTML comment (P5, P6), a byte-order mark
  ahead of the table (P15, P16), and the case and spacing variants the reader
  does not accept. This is the documented safe direction: the copy "leaves
  too much rather than too little".
- **The vendored copy re-stamps a row the plugin leaves.** This happens in
  four shapes. In two of them (P1, a doubled notify row with both values
  empty; P2, a doubled `Pact` row whose first value is empty, with no notify
  row) no row carries a value that could be `always`, so no reading of the
  file owes a record. The plugin leaves the row only because a doubled row
  is a refusal. The other two (P3 and P4) are 🟡 1 below.

Every shape where the plugin records under `always` was left by the vendored
copy, which is round 2's yellow 1 closed: U+0085, U+001E, U+2029, a lone CR,
tab-only cell spacing and an upper-case `ALWAYS` (P7-P9, P12-P14).

### 🟡 1 — the vendored copy reads `seal/config.md` leniently, so a config that is not UTF-8 never counts as "will not read"

`skills/evidence-check/scripts/evidence_check.py:3734`:

```python
said = read(declaration) if os.path.lexists(declaration) else ""
```

`read` without `strict` opens the file with `errors="replace"`, so it
returns `None` only when the file cannot be opened at all. The plugin's
branch reads the same file through `hooks/config.py#declared_pacts`, which
opens it strictly and answers `None` for a byte that is not UTF-8. That
`None` is the plugin's "will not read", and its writer then leaves every
moved row as `may be always` (`test_a_pact_row_that_will_not_read_leaves_the_row`,
id `a config that is not UTF-8`).

The vendored copy instead reads the text with U+FFFD in place of the bad
byte. Where that byte sits in the item cell of a row, the row stops matching
`NOTIFY_ROW_SHAPE`. Executed, probe P4: `| Pact notify\xff | always |` under
a valid `Pact` row. The plugin exits 1 and leaves the row with "`Pact
notify` may be `always`". The vendored copy exits 0 and re-stamps the row,
with nothing recorded.

Why it matters: the plugin's own rule (round 2 of PR #749, yellow 13) is
that a declaration that will not read cannot rule `always` out. Once the
person removes the byte, the row reads `always`, and the change the vendored
copy re-stamped was owed a record. The drift that would have made the next
plugin run record it is gone. This is the class round 1's yellow 1 and round
2's yellow 1 were about: the vendored copy re-stamps where the plugin would
not. Three texts already promise the other behaviour. The code comment above
the line, `docs/the-pact.md:302` and `skills/evidence-check/SKILL.md:337`
all say the copy leaves the row where the config "will not read", and the
plugin's own vocabulary counts a file that is not UTF-8 as one that will not
read. Ledger row C1 says the same. So today all four are false for such a
file, and the fix makes them true without changing a word of them.

P3 is the same cause with no notify row: a bad byte in the `Mode` cell. The
vendored copy re-stamps at exit 0, and the plugin leaves the row at exit 1.
Round 2 executed this as its probe E and opened no finding for it. On its own
it loses nothing, because no row could mean `always`. It is still the same
disagreement, and the same one-line fix closes it.

Depth: the line came in at `a5e359d3`, round 1's fix, in the vendored branch
round 2 called its new unit (depth 1). Round 2's fix rewrote the comment and
the two document sentences around it and left the read as it was. The fix
adds no unit: one argument, plus one parametrize row on the existing
`test_a_vendored_copy_whose_config_will_not_read_leaves_the_row`.

Executed in the clone, then reverted: with the fix, both P3 and P4 match the
plugin (exit 1, the row left). The new row fails without the code change and
passes with it. The four pact modules pass (188). `ruff check` and `ruff
format --check` are clean on both files. The pinned document sentences need
no edit.

### ⬜ 2 — the vendored-copy paragraph's `Enforced by:` line omits the case that enforces "or will not read"

`docs/the-pact.md:308` lists three cases for the paragraph at `:296-307`.
The paragraph's "or will not read" half is held by
`test_a_vendored_copy_whose_config_will_not_read_leaves_the_row`, which the
line does not name. No behaviour is wrong. A reader following the line to
see what holds the sentence finds nothing for that half, and 🟡 1's new row
lands in that case. The paste-ready line is below.

### What was checked and found closed

- **Round 2's yellow 1.** Executed: the three new rows of
  `test_a_vendored_copy_under_a_notify_row_leaves_a_row_citing_no_clause`
  (U+00A0, U+3000, U+2028) fail against `aa4546f0`'s `evidence_check.py` and
  pass at the target. Probe P7-P9 and P12-P14 extend the class to every
  other `str.splitlines` boundary and `\s` character the reader accepts, and
  the vendored copy leaves each one. Read: the reader's `CONFIG_ROW` needs
  `^\|` and a two-cell row on a `str.splitlines` line. `str.strip` and
  Python's `\s` are the same set, and the shape's `[^\s|]` accepts the first
  character of any value that strips to non-empty, so the reader takes no
  row with a value that the shape misses.
- **Round 2's yellow 2.** Executed: the two new rows of
  `test_a_vendored_copy_with_no_notify_row_restamps_a_row_citing_no_clause`
  fail against `aa4546f0`'s script and pass at the target.
  `templates/config.md`'s empty rows and a notify row with no `Pact` row
  are re-stamped at exit 0, as the plugin re-stamps them.
- **Round 2's white 3.** Executed: with `9d2c1579`'s `hooks/config.py`
  (the doubled row read as its first value) the two new rows,
  `test_s3_a_notify_value_outside_the_vocabulary_is_exit_2[written twice]`
  and the CI print module's `notify written twice`, fail, and at the target
  they pass. The `READ` line's "will not parse" comes from
  `skills/evidence-check/scripts/pact_check.py:658`.
- **Round 2's white 4.** Read: ledger row C1 now states the shape as the
  code has it. Its "or will not read" clause is false for a config that is
  not UTF-8 until 🟡 1 is fixed. After the fix it is true as written, so no
  second correction is owed. Executed: `bin/evidence-check --ledger` over the
  fragment at the target, exit 0, 234 ok, 0 drifted, 0 broken.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The vendored copy reads `seal/config.md` leniently, so a byte that is not UTF-8 becomes U+FFFD. That never makes the file "will not read", and it can hide a `Pact notify` row. Under `\| Pact notify\xff \| always \|` the plugin leaves the moved row citing no clause (exit 1) and the vendored copy re-stamps it unrecorded (exit 0). The code comment, `docs/the-pact.md:302`, `skills/evidence-check/SKILL.md:337` and ledger row C1 all promise the row is left | `skills/evidence-check/scripts/evidence_check.py:3734` | open | executed: probe P4, plugin exit 1 and left, vendored exit 0 and re-stamped; P3 (bad byte in `Mode`, no notify row) disagrees the same way; read: `read` defaults to `errors="replace"`, `hooks/config.py#declared_pacts` reads strictly; with `strict=True` both match the plugin and the new row is red without it; line from `a5e359d3`, round 1's fix, depth 1; no unit added |
| ⬜ 2 | The vendored-copy paragraph's `Enforced by:` line names no case for its "or will not read" half | `docs/the-pact.md:308` | open | read: `test_a_vendored_copy_whose_config_will_not_read_leaves_the_row` holds that half and is not listed; no behaviour wrong |
| 🟢 | round 2's yellow 1 is closed — the vendored copy leaves a moved row citing no clause beside U+00A0 or U+3000, or after U+2028, where the plugin records it | `skills/evidence-check/scripts/evidence_check.py:3650` | confirmed | executed: the three new rows fail against `aa4546f0`'s script and pass at the target; probe P7-P9, P12-P14 (U+0085, U+001E, lone CR, U+2029, tabs, `ALWAYS`): plugin records, vendored leaves; read: the reader takes no row with a value the shape misses |
| 🟢 | round 2's yellow 2 is closed — the template's empty rows and a notify row with no `Pact` row are re-stamped at exit 0 by the vendored copy, as by the plugin | `skills/evidence-check/scripts/evidence_check.py:3740` | confirmed | executed: the two new rows fail against `aa4546f0`'s script and pass at the target |
| 🟢 | round 2's white 3 is closed — a doubled `Pact notify` row's `pact-check` `READ` line and the CI print are pinned | `tests/test_pact_check.py:273` | confirmed | executed: both new rows fail with `9d2c1579`'s `hooks/config.py` and pass at the target |
| 🟢 | round 2's white 4 is closed — ledger row C1 says what the shape finds | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:5` | confirmed | read against the code at the target; its "or will not read" half becomes true with yellow 1's fix, so no second correction is owed; executed: `bin/evidence-check --ledger` exit 0, 234 ok |
| 🟢 | The disagreements left after yellow 1 cannot lose a record: the vendored copy leaves where the plugin re-stamps (fence, comment, byte-order mark), or re-stamps only where no row carries a value that could be `always` (doubled empty notify rows, a doubled `Pact` row with the first empty and no notify row) | `skills/evidence-check/scripts/evidence_check.py:3740` | confirmed | executed: probe P1, P2, P5, P6, P15, P16; read: the plugin leaves P1 and P2 because a doubled row is a refusal, not because `always` is possible |
| carried | Round 1's and round 2's earlier confirmations (PR #749's closures, W8-W10, K1, K2, the seven round-1 units, T1/T2, the 0.18.0 P1 re-read) | `skills/evidence-check/scripts/evidence_check.py:4992` | confirmed | carried from round 2; the fix range touches only the vendored branch and its comment; executed: the four pact modules and the identifier module, 192 passed |
| ❓ | The full suite, the repository-wide lint and the typecheck | the tree at `bfb7d0b7` | ❓ out of verified scope | the broad gate is the sealer's, after the rounds settle; the `unverified` label it carries is honest |

## Paste-ready fixes

### 🟡 1

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

### ⬜ 2

```markdown
docs/the-pact.md:308, replacing the line:

Enforced by: tests/test_a_signatory_records_a_pact_change.py::test_a_vendored_copy_says_it_recorded_nothing, tests/test_a_signatory_records_a_pact_change.py::test_a_vendored_copy_under_a_notify_row_leaves_a_row_citing_no_clause, tests/test_a_signatory_records_a_pact_change.py::test_a_vendored_copy_with_no_notify_row_restamps_a_row_citing_no_clause, tests/test_a_signatory_records_a_pact_change.py::test_a_vendored_copy_whose_config_will_not_read_leaves_the_row
```

## Regression tests to plant

- `tests/test_a_signatory_records_a_pact_change.py`: the `it is not UTF-8`
  row of `test_a_vendored_copy_whose_config_will_not_read_leaves_the_row`
  (above). I saw it red against the target's script and green with the fix.

## Facts for the evidence ledger

- C1's `record_pact_changes` coordinate drifts with 🟡 1's fix. The claim's
  "or will not read" half becomes true as written, so the re-read needs no
  change of wording.

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

### Probe P1-P16

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1 (the vendored copy reads `seal/config.md` leniently, so a config that is not UTF-8 is never "will not read", and a moved row the plugin leaves is re-stamped unrecorded)
Loses a record or crashes: yes — 🟡 1 re-stamps a moved row citing no clause where a bad byte hides a `Pact notify` row whose value is `always`; the plugin cannot rule `always` out there, and once the byte is repaired the change is owed with its drift already gone

## Proof block

Files opened this round, all at the target unless named:
`seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/rounds/round-2.md`,
`skills/evidence-check/scripts/evidence_check.py` (lines 1065-1100,
3600-3900), `hooks/config.py` (lines 60-130, 170-460, 600-830),
`docs/the-pact.md` (lines 140-165, 295-312, the `Enforced by:` lines),
`skills/evidence-check/SKILL.md` (lines 320-345),
`tests/test_a_signatory_records_a_pact_change.py` (lines 1-110, 455-500,
777-781, 1382-1504), `bin/test`, the round-2 fix diff `aa4546f0..a94914a0`
over `skills`, `hooks`, `tests`, `docs` and `seal/`, and the round's paragraph
handed to me by the orchestrator.

The probe file, the scratch outputs and the clone were made under the
session scratchpad. The probe file was deleted after its run, and the clone
was reset to the target.
