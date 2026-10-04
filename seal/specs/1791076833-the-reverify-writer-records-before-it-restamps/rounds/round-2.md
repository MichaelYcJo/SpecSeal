# 1791076833-the-reverify-writer-records-before-it-restamps — review round 2

| Field | Value |
|---|---|
| Target SHA | bc30a10d23e0cf3cc9099b0b61accddf4f66f516 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #756 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `aa4546f0a6f8a4bc77ad774ad4f786a007c967a1..a94914a00d9ed4a59f634da5e837d8257793e9ed`, 2 commits |
| Contract changes | test_a_vendored_copy_with_no_notify_row_restamps_a_row_citing_no_clause → round-1-report.md, round-1.md; test_s3_a_notify_value_outside_the_vocabulary_is_exit_2 → pytest only |
| New units | none |
| Needs a fix | yes — 🟡 1 (the vendored copy misses a `Pact notify` row the plugin reads, beside a Unicode space or after U+2028), 🟡 2 (the vendored copy refuses every moved row in a repository holding no pact whose config carries an empty or orphaned `Pact notify` row) |
| Loses a record or crashes | yes — 🟡 1 re-stamps a moved row whose pact change `always` owes with nothing recorded, so the drift that would record it is gone |

- [x] Pass

## What this round was asked

Round 2 of work item `1791076833-the-reverify-writer-records-before-it-restamps` (#647 steps C and D, PR #756), target `bc30a10d`. It is the verifying round for round 1's fixes, range `9d2c1579..013363e8`. Open those fixes first. For 🟡1, a vendored copy under a `Pact notify` row now leaves an uncited moved row; `NOTIFY_ROW_SHAPE` is deliberately broader than the plugin's reader. For 🟡2, `hooks/config.py#pact_declaration` now refuses a doubled `Pact notify` row with `notify=None`, so the writer, `pact-check` and `chain-check` all change. Then judge the seven new units (all depth 1) and the corrected record rows (T1/T2, C1, the 0.18.0 P1 re-read). One shape of the same class is out of scope and filed as #759: a notify row after the table ends. Report anything else you find, at the depth it sits.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The vendored copy's `NOTIFY_ROW_SHAPE` misses a `Pact notify \| always` row the plugin reads: a U+00A0 or U+3000 space beside a pipe, or the row after a U+2028 line separator. The vendored copy re-stamps a moved row citing no clause at exit 0 with nothing recorded, where the plugin records it | `skills/evidence-check/scripts/evidence_check.py:3645` | **fixed** `e4d29aac` | fixed at e4d29aac; executed in temporary signatories: plugin exit 0 and recorded, vendored exit 0, re-stamped and not recorded, for all three; the plugin's `config_rows` uses `\s` and `str.splitlines`, the shape `[ \t]` and `^` under `re.M`; round 1's yellow 1's class, in the new unit (depth 1) |
| 🟡 2 | `NOTIFY_ROW_SHAPE` matches a `Pact notify` row with no value, and one with no `Pact` row, so the vendored `--reverify` leaves every moved row citing no clause in a repository that holds no pact, including one carrying `templates/config.md`'s own table, at exit 1, and sends the person to "where the signatory is checked out" | `skills/evidence-check/scripts/evidence_check.py:3645` | **fixed** `e4d29aac` | fixed at e4d29aac; executed: `\| Pact \|  \|` with `\| Pact notify \|  \|`, and a notify row with no `Pact` row: plugin exit 0 and re-stamped, vendored at `bc30a10d` exit 1 and nothing re-stamped, vendored at `9d2c1579` exit 0 and re-stamped; `templates/config.md:38-39` ships both empty rows; the new unit (depth 1) |
| ⬜ 3 | A doubled `Pact notify` row is now `notify=None`, which `chain-check` prints as "a value that will not parse" and `pact-check`'s `READ` line as "will not parse"; neither print is pinned | `skills/code-review/scripts/chain_check.py:4048` | **fixed** `e4d29aac` | fixed at e4d29aac — parametrize rows on the existing `test_s3_a_notify_value_outside_the_vocabulary_is_exit_2` and `test_a_row_that_will_not_parse_is_a_notice_and_never_a_failure` pin the doubled row's `pact-check` and `chain-check` output; read: `skills/evidence-check/scripts/pact_check.py:658` is the second site; the refusal sentence printed beside each is right and `pact-check` exits 2 on it, so no behaviour is wrong; §14 asks for a pin; no test drives either reader with a doubled row |
| ⬜ 4 | Ledger row `C1` says the vendored copy names each moved row "where `seal/config.md` holds a `Pact notify` row or will not read"; for the U+00A0 row the plugin reads, it does not, and the sentence changes with 🟡 1 and 🟡 2's fix | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:5` | answered | corrected at `a94914a0`: ledger row C1's claim now says the vendored copy is blind only where both `Pact` and `Pact notify` carry a value, matched per `str.splitlines` line with Python's `\s`; read against probe C; a correction to the run's paperwork, not counted in `Needs a fix` |
| 🟢 | round 1's yellow 1 is closed for the shape it named: a vendored copy under a plain `\| Pact notify \| always \|` row leaves a moved row citing no clause, records nothing and exits 1 | `skills/evidence-check/scripts/evidence_check.py:3729` | confirmed | executed: with `9d2c1579`'s `evidence_check.py` and `hooks/config.py` restored, `test_a_vendored_copy_under_a_notify_row_leaves_a_row_citing_no_clause` (both) and `test_a_vendored_copy_whose_config_will_not_read_leaves_the_row` fail, and pass at the target; the other shapes of the class are this round's 🟡 1 |
| 🟢 | round 1's yellow 2 is closed: a doubled `Pact notify` row has no value, and the plugin's writer leaves a moved row citing no clause under it whatever the first row says | `hooks/config.py:786` | confirmed | executed: `test_a_notify_row_written_twice_has_no_value` (3) and `test_a_notify_row_written_twice_leaves_a_row_citing_no_clause` (2) fail on the pre-fix code and pass at the target; read: a doubled `Pact` row and an out-of-vocabulary value reach the same `refused and unknown` arm |
| 🟢 | round 1's white 3 is closed: claim rows `T1` and `T2` are relabelled, each with a note naming where `W1` and `W2` still stand | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:1` | confirmed | read rows 1 and 2; executed: `bin/evidence-check --ledger` over the fragment, exit 0, 232 ok |
| 🟢 | round 1's white 4 is closed: `plan.md` names the old worktree by its directory name | `seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/plan.md:24` | confirmed | executed: `tests/test_no_real_identifiers.py` passes at the target, in the 211-case run |
| 🟢 | The seven new units are correct apart from `NOTIFY_ROW_SHAPE`, and their cases were red before the fix | `tests/test_a_signatory_records_a_pact_change.py:1356` | confirmed | executed: 8 of the 10 new parametrisations fail against `9d2c1579`'s code; the 2 that pass are `test_a_vendored_copy_with_no_notify_row_restamps_a_row_citing_no_clause`, which pins carried behaviour; read: `_vendored` copies the script alone, so `plugin_module` answers None as for a real vendored copy |
| 🟢 | The re-read of the 0.18.0 row `P1` holds: a doubled `Pact notify` row is a refusal with no value, which is stricter than and consistent with "never read as absent" | `seal/ledger/1791076833-the-reverify-writer-records-before-it-restamps.md:65` | confirmed | read against `seal/releases/0.18.0.md:6` and `pact_declaration` at the target |
| carried | Round 1's ten confirmations (PR #749's closures, W8-W10, K1 and K2) | `skills/evidence-check/scripts/evidence_check.py:4992` | confirmed | carried from round 1; the fix range touches none of their code except the vendored branch, whose citing-row arm is unchanged and still pinned by `test_a_vendored_copy_says_it_recorded_nothing`; executed: the six modules that hold them, 211 passed |
| ❓ | The full suite, the repository-wide lint and the typecheck | the tree at `bc30a10d` | ❓ out of verified scope | the broad gate is the sealer's, after the rounds settle; the `unverified` label it carries is honest |

## Paste-ready fixes

```python
# skills/evidence-check/scripts/evidence_check.py, replacing NOTIFY_ROW_SHAPE
# and its comment
# Anything shaped like a `Pact` or a `Pact notify` row with a value, for a
# copy with no `hooks/` to read either with: any case, any indentation,
# quoted or fenced or not, matched line by line as `str.splitlines` cuts a
# file and with `\s` as Python reads it, because those are the plugin
# reader's own rules (round 2 of PR #756, yellow 1). An empty value is the
# default, and a notify row with no `Pact` value is ignored, so neither can
# mean `always` (yellow 2).
NOTIFY_ROW_SHAPE = re.compile(r"[\s>]*\|\s*(Pact(?:\s+notify)?)\s*\|\s*[^\s|]", re.I)
```
```python
    # in record_pact_changes, the vendored branch, replacing the comment and
    # the `blind = ...` line
    if config is None:
        # This copy reads no `Pact notify` value either, so where the config
        # holds a `Pact` row and a `Pact notify` row that both carry a value,
        # or will not read, a moved row citing no clause may be owed under
        # `always` and is left with the rows citing one (round 1 of PR #756,
        # yellow 1). The shape is looser than the plugin's reader, so it
        # leaves too much rather than too little; without both rows nothing
        # can mean `always` (round 2, yellow 2).
        declaration = os.path.join(seal_home(root), "config.md")
        said = read(declaration) if os.path.lexists(declaration) else ""
        named = {
            " ".join(m.group(1).lower().split())
            for m in map(NOTIFY_ROW_SHAPE.match, (said or "").splitlines())
            if m
        }
        blind = said is None or named == {"pact", "pact notify"}
```
```python
# tests/test_a_signatory_records_a_pact_change.py, appended
# --- round 2 of PR #756: the vendored copy's shape against the plugin's reader

CONFIG_HEAD = "| Item | Value |\n|---|---|\n| Mode | shared |\n"


@pytest.mark.parametrize(
    "tail",
    [
        f"| Pact | {PACT_URL} |\n| Pact notify | always |\n",
        f"| Pact | {PACT_URL} |\n| Pact notify　| always |\n",
        f"| Pact | {PACT_URL} | | Pact notify | always |\n",
    ],
    ids=["a no-break space", "an ideographic space", "a line separator"],
)
def test_a_vendored_copy_leaves_every_notify_row_the_plugin_reads(repo, tmp_path, tail):
    """The plugin's reader takes `\\s` and `str.splitlines` as Python reads
    them, so each of these is `Pact notify | always` to it; the vendored
    copy leaves the row too, or the change is re-stamped unrecorded (round 2
    of PR #756, yellow 1)."""
    (repo / "seal" / "config.md").write_text(CONFIG_HEAD + tail, encoding="utf-8")
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O2", "", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    code, out = _vendored(repo, tmp_path)
    assert code == 1 and "may be `always`" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out


@pytest.mark.parametrize(
    "tail",
    ["| Pact |  |\n| Pact notify |  |\n", "| Pact notify | always |\n"],
    ids=["the template's empty rows", "a notify row with no Pact row"],
)
def test_a_vendored_copy_holding_no_pact_restamps_a_row_citing_no_clause(
    repo, tmp_path, tail
):
    """With no `Pact` value, or no `Pact notify` value, nothing is owed and
    nothing can mean `always`, so the vendored copy re-stamps as the plugin
    does (round 2 of PR #756, yellow 2)."""
    (repo / "seal" / "config.md").write_text(CONFIG_HEAD + tail, encoding="utf-8")
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger = cite(repo, [row("O2", "", f"src/orders.py#serialize@{old}")])
    new = move_serialize(repo)
    code, out = _vendored(repo, tmp_path)
    assert code == 0, out
    assert f"@{new}" in ledger.read_text(encoding="utf-8"), out
```
```markdown
docs/the-pact.md, the vendored-copy sentence (and add the two new cases to
its `Enforced by:` line):

`hooks/` beside it cannot read the `Pact` row; it names each row citing a
pact, and each other moved row where `seal/config.md` holds a `Pact` row and
a `Pact notify` row that both carry a value, or will not read, says it
recorded nothing, and re-stamps nothing, so the plugin's own checker records
the change where the signatory is checked out.

skills/evidence-check/SKILL.md, the same sentence:

pact on a `LEFT` line, and each other moved row where `seal/config.md` holds
a `Pact` row and a `Pact notify` row that both carry a value, or will not
read, records nothing, and exits 1. A `Pact notify` row written twice has no
value, so it cannot rule `always` out either.
```
```python
# tests/test_a_signatory_records_a_pact_change.py,
# test_the_documents_say_what_the_writer_does: the two pinned sentences
        (
            "docs/the-pact.md",
            "and each other moved row where `seal/config.md` holds a `Pact` row and "
            "a `Pact notify` row that both carry a value, or will not read, says it "
            "recorded nothing, and re-stamps nothing",
        ),
        (
            "skills/evidence-check/SKILL.md",
            "and each other moved row where `seal/config.md` holds a `Pact` row and "
            "a `Pact notify` row that both carry a value, or will not read, records "
            "nothing, and exits 1. A `Pact notify` row written twice has no value",
        ),
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the writer module, the declaration module, `test_pact_check.py`, the CI print module, the pact review module, `tests/test_gates_do_not_fail_open.py` and `tests/test_no_real_identifiers.py` at the target | 211 passed |
| Round 1's ten new parametrisations against `9d2c1579`'s `evidence_check.py` and `hooks/config.py`, then restored | 8 failed, 2 passed (the 2 pin carried behaviour) |
| Probe A-F: a moved row citing no clause, run through the plugin's copy at the target, a vendored copy at the target and a vendored copy of `9d2c1579`'s script | A, the template's empty rows, and B, a notify row with no `Pact` row: plugin 0 and re-stamped, vendored 1 and left, old vendored 0 and re-stamped. C, U+00A0; C2, U+3000; D, U+2028: plugin 0 and recorded, vendored 0, re-stamped and not recorded. E, a byte that is not UTF-8 and no notify row: plugin 1 and left, vendored 0 and re-stamped. F, a plain `always` row: plugin 0 and recorded, vendored 1 and left |
| The paste-ready fixes below, applied in the clone with their cases, then reverted | the 5 new parametrisations failed at the target and passed with the fix; probe A-D then matched the plugin on what is left and what is re-stamped; the six modules, 184 passed; ruff check and format clean on the two Python files |
| `bin/evidence-check --ledger` over this item's fragment at the target | exit 0; 232 ok, 0 drifted, 0 broken; records arm 0 refused, 0 drifted |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — not run here; it is the sealer's, after the rounds settle |

```python
# Probe A-F. For each config.md, a temporary signatory: src/orders.py, a
# ledger row citing no clause at serialize's hash, then serialize edited.
# Run `--reverify --into <fragment> --checked 2026-09-04` three ways: the
# plugin's script in the clone, the same script copied alone into tools/
# (no hooks/, no SKILL.md beside it), and 9d2c1579's script copied alone.
# Report exit, whether the ledger row was re-stamped, whether
# seal/pact-changes/ was written, and the first LEFT line.
A  = "| Pact |  |\n| Pact notify |  |\n"                    # templates/config.md
B  = "| Pact notify | always |\n"                           # no Pact row
C  = f"| Pact | {URL} |\n| Pact notify | always |\n"
C2 = f"| Pact | {URL} |\n| Pact notify　| always |\n"
D  = f"| Pact | {URL} | | Pact notify | always |\n"
E  = Mode cell "shar\xffed", a Pact row, no notify row
F  = f"| Pact | {URL} |\n| Pact notify | always |\n"
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
