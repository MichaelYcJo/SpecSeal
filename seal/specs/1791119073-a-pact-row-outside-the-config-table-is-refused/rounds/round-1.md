# 1791119073-a-pact-row-outside-the-config-table-is-refused — review round 1

| Field | Value |
|---|---|
| Target SHA | 0e8fa3730cd63d9523a9f1764dcd874a0a9bc079 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #784 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a pact row with no leading pipe) and 🟡 2 (a format character in the item), both still read as the default with no refusal |
| Loses a record or crashes | yes — under 🟡 1 and 🟡 2, `evidence-check --reverify` re-stamps a moved row citing no clause under `always` and records no pact change. Executed for 🟡 1 through the writer, and for 🟡 2 at the reader. Both losses predate this branch, and the branch does not close them. |

- [ ] Pass

## What this round was asked

Round 1 of #759 (PR #784), at 0e8fa373 against `release/v0.18.2` (94d7b2e0): spec compliance first, then quality. Judge whether `stray_pact_rows` finds every pact-shaped line the table walk did not read as a pact row (W1–W11 enumerated from `config_rows`' code, on both line cuts, with Unicode spaces and `splitlines`-only breaks); whether the refusal fires where it must not (template, fences, comments, list lines, this repository's config, no `Pact` value); the vendored copy against the plugin's shape; the three callers end to end; the refusal sentence's divergence from the frame; and commit fa4ddfe1's file list.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A pact row with no leading pipe, directly under the table, is a GFM row of the live table and is read as the default with no refusal; `--reverify` re-stamps a moved row citing no clause unrecorded | `hooks/config.py:657` | open | executed: cmark-gfm renders the row; `pact_declaration` returns the default notify and no refusal; the writer probe re-stamped at exit 0 with no `seal/pact-changes/`; the vendored shape misses it too |
| 🟡 2 | A Unicode format character (U+200B, U+2060, U+FEFF, U+00AD) in or around the item spells it another way that neither grammar sees, and the row is read as the default | `hooks/config.py:906` | open | executed: twelve inputs returned the default notify with no refusal, and the vendored copy was not blind for any of them |
| ⬜ 3 | A pact row in a four-space indented code block, or on a list item's continuation line, is refused though GFM renders no row | `hooks/config.py:888` | open | executed; spec Scope 2 chose "any indentation" and the template states it, so nothing is commissioned |
| ⬜ 4 | A stray `Pact` with no `Pact notify` row anywhere leaves a row citing no clause, saying notify "may be `always`" | `hooks/config.py:851` | open | executed: exit 1 and LEFT; nothing can be `always` there, the vendored copy re-stamps, and no record is lost |
| ⬜ 5 | The refusal sentence's three causes do not name W8, where the row's own shape ended the table | `hooks/config.py:911` | open | read; the remedy shows the right shape, and the divergence itself is within the spec's latitude |
| 🟢 | The new reader, writer, pact-check, chain-check and vendored cases are red at the base | `tests/test_a_signatory_declares_its_pact.py` | confirmed | executed: 42 failed against the base `hooks/config.py` and `evidence_check.py`; the 18 that passed are the guards S6, S7, S8 and S12 |
| 🟢 | Commit fa4ddfe1 carries exactly the four intended files | `seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/plan.md` | confirmed | executed: `git show --name-only` lists the ledger fragment, `changelog.md`, `phases/phase-4.md` and `plan.md`; the one-call shape breaks contract §17 and nothing else landed |
| 🟢 | Both cuts and all eight splitlines-only characters, with none silent; the refusal is silent on the template, this repository's config, a fence, a comment, a list-marked line, an empty value and a repository with no pact | `hooks/config.py:858` | confirmed | executed: 64 positions and 8 guard inputs |
| 🟢 | The vendored copy has the same pattern on both cuts and is blind wherever the plugin refuses | `skills/evidence-check/scripts/evidence_check.py:3836` | confirmed | executed: probe over every input above |

## Paste-ready fixes

```python
# at the imports
import unicodedata

# replacing PACT_ROW_SHAPE and the comment's last line
# An empty value is the default, so it is not shaped as a row here. The
# leading pipe is optional because GFM's is: a line directly under the table
# with none is still a row of it. A line is read through `shape_line` first.
PACT_ROW_SHAPE = re.compile(r"[\s>]*\|?\s*(Pact(?:\s*notify)?)\s*\|\s*[^\s|]", re.I)


def shape_line(line):
    """LINE as `PACT_ROW_SHAPE` reads it: every format character (Unicode
    category Cf -- U+200B, U+2060, U+FEFF, U+00AD and the rest) removed,
    because GFM renders none of them and a person reads the row without
    them. `evidence_check.py#shape_line` is its copy."""
    return "".join(ch for ch in line if unicodedata.category(ch) != "Cf")
```
```python
# stray_pact_rows: both matches
        match = PACT_ROW_SHAPE.match(shape_line(line))
# ...
        match = PACT_ROW_SHAPE.match(shape_line(line))


def _shaped_item(match):
    named = "".join(match.group(1).split()).lower()
    return PACT_NOTIFY_ROW if named == "pactnotify" else PACT_ROW


# stray_refusal: show a format character as well as non-space whitespace
    shown = "".join(
        f"<U+{ord(ch):04X}>"
        if (ch.isspace() and ch != " ") or unicodedata.category(ch) == "Cf"
        else ch
        for ch in line.strip()
    )
```
```python
# at the imports
import unicodedata

NOTIFY_ROW_SHAPE = re.compile(r"[\s>]*\|?\s*(Pact(?:\s*notify)?)\s*\|\s*[^\s|]", re.I)


def shape_line(line):
    """`hooks/config.py#shape_line`, copied for a copy with no `hooks/`."""
    return "".join(ch for ch in line if unicodedata.category(ch) != "Cf")


# record_pact_changes, the vendored branch
        lines = [
            shape_line(line)
            for line in (said or "").splitlines() + gfm_lines(said or "")
        ]
        named = {
            "".join(m.group(1).lower().split())
            for m in map(NOTIFY_ROW_SHAPE.match, lines)
            if m
        }
        blind = said is None or named >= {"pact", "pactnotify"}
```
```python
# appended to STRAY_WAYS
    (
        "W8 no leading pipe, directly under the table",
        CONFIG + "Pact notify | always |\n",
        "Pact notify | always |",
    ),
    (
        "W8 no pipe at either end, directly under the table",
        CONFIG + "Pact notify | always\n",
        "Pact notify | always",
    ),


@pytest.mark.parametrize(
    "ch", ["​", "⁠", "﻿", "­"],
    ids=["U+200B", "U+2060", "U+FEFF", "U+00AD"],
)
def test_a_notify_row_spelled_with_a_format_character_is_refused(ch):
    """A format character renders as nothing, so GFM shows `Pact notify`;
    the walk takes another item, and the shape reads past it."""
    for row, shown in (
        (f"| Pact{ch}notify | always |", f"| Pact<U+{ord(ch):04X}>notify | always |"),
        (f"| Pact notify{ch} | always |", f"| Pact notify<U+{ord(ch):04X}> | always |"),
    ):
        assert config.pact_declaration(CONFIG + row + "\n")[1:] == (
            None,
            [refused_as(shown)],
        ), row


def test_the_reader_and_the_vendored_copy_read_one_line_alike():
    """S14 pins the pattern; this pins the line each reads it through."""
    path = os.path.join(
        ROOT, "skills", "evidence-check", "scripts", "evidence_check.py"
    )
    spec = importlib.util.spec_from_file_location("ec_for_the_shape_line", path)
    ec = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ec)
    for line in ("| Pa​ct notify | x |", "﻿| Pact | x |", "Pact | x"):
        assert config.shape_line(line) == ec.shape_line(line), line
```
```python
def test_a_notify_row_with_no_leading_pipe_leaves_a_row_citing_no_clause(repo):
    """GFM reads `Pact notify | always |` directly under the table as a row
    of it; the reader does not, so it is refused and the row is left."""
    (repo / "seal" / "config.md").write_text(
        config_text(("Mode", "shared"), ("Pact", PACT_URL))
        + "Pact notify | always |\n",
        encoding="utf-8",
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger_rows = [row("O1", "", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, ledger_rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1, out
    assert ledger.read_text(encoding="utf-8") == "".join(ledger_rows), out
    assert not (repo / "seal" / "pact-changes").exists(), out
```

## Executed probes

| What was run | Result |
|---|---|
| Reader matrix: 8 splitlines-only characters × 8 positions, Unicode spaces and format characters × 3 positions, no-leading-pipe rows, and the must-not inputs, through `pact_declaration` and the vendored `named` set, at 0e8fa373 | 56 refused, 8 read `always`, 0 silent among the cuts; 16 silent defaults (🟡 1 and 🟡 2); guards silent as specified; indented code and a list continuation refused (⬜ 3) |
| cmark-gfm rendering of the no-leading-pipe rows, `Pact<U+200B>notify` and the four-space indented row | the first three render as a row of the live table; the indented one renders as a code block |
| Writer: `Pact notify \| always \|` directly under the table, with a moved row citing no clause | exit 0, re-stamped, no `seal/pact-changes/` (🟡 1) |
| Writer: a stray `Pact` line with no notify row, with a moved row citing no clause | exit 1, LEFT "may be `always`" (⬜ 4) |
| The new cases of the four pact modules against the base `hooks/config.py` and `evidence_check.py` | 42 failed, 18 passed (the guards) |
| The proposed shape and Cf normaliser, patched into the reader in a probe | every 🟡 input refused; the template, this repository's config, S8, an in-table `always` and "no pact, stray notify" read as before |
| The full suite, the repository-wide lint and the typecheck | not yet; this is the sealer's run after the rounds settle, and nothing in this round substitutes for it |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A misplaced `Ledger frozen from` row is read as no freeze (`spec.md` §Out, overview "Not done") | the orchestrator, as a candidate to file | the orchestrator of this run |
