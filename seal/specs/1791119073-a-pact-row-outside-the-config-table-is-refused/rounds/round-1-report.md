# Round 1 review report — 1791119073-a-pact-row-outside-the-config-table-is-refused

- Target: PR #784 (draft), branch `fix/759-a-pact-row-outside-the-config-table-is-refused`, SHA 0e8fa373, base `release/v0.18.2` at 94d7b2e0
- Ran by: specseal:warden on claude-opus-5-5
- Where: a `git clone --no-local` of the worktree, checked out at 0e8fa373, under the round's scratch directory. Nothing was written in the worktree but this file.
- Earlier rounds: none. This is round 1, so nothing is carried.

## Summary

The build does what `spec.md` asks for every way the spec enumerated (W1–W11). I checked that by execution, on both line cuts and for all eight splitlines-only characters at eight positions in a row. The refusal does not fire on the shipped template, this repository's own config, a closed fence, a closed comment, a list-marked line, an empty value, or a repository with no `Pact` value. The vendored copy carries the same pattern, and it is blind on every input where the plugin refuses.

Two shapes in the same class are still read as the default with no refusal. In both, GFM renders a `Pact notify | always` row inside the live table, and `--reverify` still loses the pact change. Neither the spec's W-list nor the shape `PACT_ROW_SHAPE` reaches them:

1. **A table row with no leading pipe.** GFM tables do not require one, and a line directly under the table continues it.
2. **A format character such as U+200B inside the item.** It is invisible when rendered, and it is not `\s`.

Both are gaps in the grammar the two readers share, so the vendored copy misses them too. Neither is a regression: the base also read both as the default. But the record the work item exists to save is still lost in those shapes.

## Spec compliance (stage 1)

**The class, W1–W11, executed.** I seeded every new reader case and writer case against the base `hooks/config.py` and `skills/evidence-check/scripts/evidence_check.py` in the clone. 42 failed. The 18 that passed are the guards (S6, S7, S8, S12 and the S6 writer), which hold at the base by design. This confirms the §15 claim in `phases/phase-1.md` and the ledger's N1–N3 for the cases I ran. I did not re-run `mutation-check`.

**Both cuts, executed.** A probe in the scratch directory (test_tmp_stray_probe.py, deleted) placed each of U+000B, U+000C, U+001C, U+001D, U+001E, U+0085, U+2028 and U+2029 at eight positions of a `Pact notify | always` row under a `Pact` row. The positions were line start, after each pipe, inside the item, before each pipe and inside the value. 56 combinations refused with `notify` None. The 8 with the character after the closing pipe read `always`, because the reader takes the row whole and the trailing piece is empty. Neither outcome is silent. NBSP and U+3000 inside the item refuse. After the item they read `always`, because `config_rows` strips the cell.

**Where it must not fire, executed.** No refusal for:

- `templates/config.md`
- `seal/config.md`
- a closed fence
- a closed comment
- a comment line cut by U+2028
- `- | Pact notify | always |`
- a stray notify with no `Pact` anywhere, which returns `([], None, [])`

Two more lines are refused although GFM renders no row for them: a pact row in a four-space indented code block, and one on a list item's continuation line. That is ⬜ 3.

**The vendored copy, executed and read.** `NOTIFY_ROW_SHAPE` and `PACT_ROW_SHAPE` have the same pattern and flags, and S14 holds them equal. `record_pact_changes` now matches the shape over `splitlines()` plus `gfm_lines()`. That is the union of the cuts the plugin's `stray_pact_rows` reads. The probe recomputed the vendored `named` set on every input above, and it was blind on every input where the plugin refuses. It is also blind on the fence and comment inputs the plugin exempts, which is the cautious direction §Out accepts. One case runs the other way: the plugin is more cautious than the copy, and loudly. That is ⬜ 4.

**The three callers, executed.** S9 (writer `LEFT`, exit 1, ledger byte-identical, no `seal/pact-changes/`), S10 (`pact-check` `REFUSED`, exit 2) and S11 (`chain-check` notice, exit unchanged) were red at the base and pass at the head. The orchestrator's narrow run covers them at the head. My base run covers them red.

**The refusal sentence (overview Divergence), read.** The spec handed the wording to the builder ("The builder chooses the final text, and S16 pins it"). The built text drops the dash and semicolon, adds the third cause and shows non-space whitespace as `<U+XXXX>`. Each of those changes has grounds in `phases/phase-1.md`, and each of the three callers pins the sentence whole. I accept the divergence. One residual wording note is ⬜ 5.

**Commit fa4ddfe1, executed.** `git show --name-only fa4ddfe1` lists exactly four files: the ledger fragment, `changelog.md`, `phases/phase-4.md` and `plan.md`. The smith's account matches. The single `cd … && git add && git commit` call breaks contract §17's shape ("in a command of its own"). That is a process note, and nothing extra landed.

**Documents, read.** The `docs/the-pact.md` paragraph and the `templates/config.md` sentence say what the code does, and S16 pins each of them. Their claim that a row "the table's reader does not reach is refused" is broader than the code under 🟡 1 and 🟡 2. If the fixes land, the claim holds as written.

## Findings

### 🟡 1 — A pact row with no leading pipe continues the live table in GFM, and is still read as the default

`hooks/config.py:657` (`PACT_ROW_SHAPE`), twinned at `skills/evidence-check/scripts/evidence_check.py:3748` (`NOTIFY_ROW_SHAPE`).

**What is wrong.** The shape requires a `|` before the item. GFM table rows do not. The leading and trailing pipes are optional, and a non-blank line directly below a table that starts no other block is another row of that table.

**Executed, with the cmark-gfm in the worktree's virtualenv.** These two inputs render a three-row tbody whose last row is `Pact notify` / `always`:

```
| Item | Value |
|---|---|
| Mode | shared |
| Pact | git@example.com:org/orders-api.git |
Pact notify | always |
```

The second is the same table ending in `Pact notify | always`, with no pipe at either end.

**Executed, at the head.** `pact_declaration` returns `notify == "when the pact is touched"` and no refusal for both inputs. `CONFIG_ROW` needs `^\|`, so the walk passes the line by (W8's arm), and the shape cannot match it. Under the writer (`tests/` probe test_tmp_759_probe.py, deleted), a moved ledger row citing no clause was re-stamped at exit 0, and `seal/pact-changes/` was not created. That is the exact loss #759 was opened about, under `always`. The vendored copy is not blind there either, so it re-stamps too.

**Why it matters.** A person reading the rendered `seal/config.md` sees `Pact notify | always` inside the table. The release then says such a row is refused and never read as the default, and it is read as the default.

**Fix.** Make the leading pipe optional in both shapes. The pin keeps the two equal. With the probe's pattern swapped in, both inputs refuse, and the template, this repository's config, S8 and an in-table `always` read as before.

### 🟡 2 — A format character inside the item spells it another way that neither grammar sees

The same two lines as 🟡 1, plus `hooks/config.py:888`, `:900` and `:906`, and the `named` set in `record_pact_changes`.

**What is wrong.** U+200B, U+2060, U+FEFF and U+00AD are Unicode category Cf. They are not `\s`, and GFM renders them as nothing. In `| Pact<U+200B>notify | always |`, inside the table under a `Pact` row, cmark-gfm renders an item that reads `Pact​notify` (executed). `config_rows` takes the row under the item `Pact​notify`, which is not `PACT_NOTIFY_ROW`, so it is not in `taken`. The shape's `\s+` cannot cross the Cf character, so the line is not shaped either.

**Executed.** The probe tried each of the four characters between the words, after the item and at line start. All twelve returned the default notify with no refusal, and the vendored `named` set was not blind for any of them.

**Why it matters.** W9, "another spelling", is in scope, and the docs promise that a row "with its item spelled another way" is refused. A Cf character pasted from a web page or a word processor is that spelling, and it is invisible in the rendered table. The likelihood is lower than 🟡 1, and the loss is the same.

**Fix.** Remove Cf characters before the shape reads a line, in both readers. Let the space between `Pact` and `notify` be empty, so `Pa<U+200B>ct notify` and `Pact<U+200B>notify` both normalise to a notify row. Name the item by its letters alone. Show Cf characters as code points in the refusal, because otherwise the sentence quotes a line that looks correct. Executed with the probe's patched shape: all of `Pa<U+200B>ct notify`, `Pact<U+200B>notify`, `Pact notify<U+FEFF>`, `Pact<U+00AD>notify` and `Pa<U+200B>ct | URL` refuse, and the guards above read as before.

### ⬜ 3 — An indented code block and a list item's continuation line are refused, though GFM renders no row there

`hooks/config.py:888`. The spec chose "any indentation" (Scope 2), and `templates/config.md` says an indented row is refused, so this is a recorded decision and not a defect. It is still the one place where #429's rule ("a pact row there is an example") is applied to fences and comments and not to a four-space indented code block, which GFM renders as `<pre><code>` (executed). The refusal's cautious direction loses nothing. Its cost is a `pact-check` exit 2 and a `--reverify` exit 1 in a repository that keeps an indented example in its config. No fix is commissioned.

### ⬜ 4 — A stray `Pact` line with no `Pact notify` row anywhere leaves a row citing no clause, with "may be `always`"

`hooks/config.py:851`, in `pact_declaration`: any stray refusal sets `notify` to None. Executed: config with `Mode` in the table and `| Pact | URL |` below a blank line, and a moved row citing no clause. The result is a `LEFT` line saying "moved, and `Pact notify` may be `always`", at exit 1. No notify row exists, so nothing can mean `always`, and the vendored copy re-stamps the same row at exit 0. The plugin is the stricter of the two, so no record is lost, and the person fixes the stray row in any case. The clause "may be `always`" is not true of this file. Spec Scope 1 says a stray sets `notify` None without distinguishing this case.

### ⬜ 5 — The refusal sentence's causes do not name W8, where the row's own shape ended the table

`hooks/config.py#stray_refusal`. For `| Pact notify | always` written as the table's last row with no closing pipe, the sentence offers three causes: "stands outside the … table, spells the item another way, or holds a character that cuts the line". A person looking at the file sees it inside the table. The remedy, `| Pact notify | … |`, does show the right shape, so the person can act. An optional fourth cause, "or is not written as a two-cell row", would cover the indented, block-quoted, third-cell, no-closing-pipe and escaped-pipe shapes. The sentence is pinned in five places, so the cost of a change is known.

## Quality (stage 2)

- **Altitude, read.** The design compares positions rather than listing the ways a table ends, and `config_rows` became a projection of one indexed walk. That is the right depth. A new arm of the walk cannot slip past the detector. Only a new shape of row can, which is what 🟡 1 and 🟡 2 are.
- **Efficiency, read.** `pact_declaration` now runs the fence and comment walk twice, once in `indexed_config_rows` and once in `stray_pact_rows`, through `unfenced`. The file is small and the readers are not on a hot path, so I recorded nothing.
- **Census, read.** `stray_pact_rows` holds two `.splitlines(` calls and the census entry says `(2, F)`. The `config_rows` entry moved to `indexed_config_rows` with its single call.

## Regression tests to plant

- `tests/test_a_signatory_declares_its_pact.py`: add to `STRAY_WAYS` the rows for no leading pipe and no pipe at either end, directly under the table (🟡 1). Add to S3 the rows for `Pact<U+200B>notify`, `Pact notify<U+FEFF>` and `Pact<U+00AD>notify`, with the shown text carrying `<U+200B>` and so on (🟡 2). Add the "no leading pipe, no `Pact` anywhere" input to S6.
- `tests/test_a_signatory_records_a_pact_change.py`: a writer case with `Pact notify | always |` directly under the table that is left at exit 1. Seen red at 0e8fa373: re-stamped at exit 0. Also a vendored case for the same input and for `Pact<U+200B>notify`.
- The S14 pin compares pattern and flags. A Cf normaliser written into each reader would be a second grammar that S14 cannot see. One case should feed the same lines to both readers and compare the items they find.

## Facts for the evidence ledger

- N1's claim ("refuses every line shaped as a `Pact` or `Pact notify` row with a value") is true of the shape and narrower than the docs' claim. After 🟡 1 and 🟡 2 the anchors on `PACT_ROW_SHAPE`, `stray_pact_rows` and `_shaped_item` move, and N3's anchor on `record_pact_changes` moves too.
- Executed 2026-10-04: cmark-gfm renders `Pact notify | always |` and `Pact notify | always`, directly under a two-column table, as a row of that table.

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

## Paste-ready fixes

### 🟡 1 and 🟡 2 — the shape, in `hooks/config.py`

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

### 🟡 1 and 🟡 2 — the twin, in `skills/evidence-check/scripts/evidence_check.py`

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

### 🟡 1 and 🟡 2 — the cases, in `tests/test_a_signatory_declares_its_pact.py`

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

### 🟡 1 — the writer case, in `tests/test_a_signatory_records_a_pact_change.py`

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A misplaced `Ledger frozen from` row is read as no freeze (`spec.md` §Out, overview "Not done") | the orchestrator, as a candidate to file | the orchestrator of this run |

Needs a fix: yes — 🟡 1 (a pact row with no leading pipe) and 🟡 2 (a format character in the item), both still read as the default with no refusal

Loses a record or crashes: yes — under 🟡 1 and 🟡 2, `evidence-check --reverify` re-stamps a moved row citing no clause under `always` and records no pact change. Executed for 🟡 1 through the writer, and for 🟡 2 at the reader. Both losses predate this branch, and the branch does not close them.

The broad gate has not come due: this round leaves 🟡 1 and 🟡 2 open, so the sealer's spawn waits for the round that closes them.

## Proof block

Files opened in this round, all at 0e8fa373 in the clone unless noted:

- `seal/specs/1791119073-a-pact-row-outside-the-config-table-is-refused/spec.md`, `overview.md`, `questions.md`, `changelog.md` and `routing.md` (head); `seal/ledger/1791119073-a-pact-row-outside-the-config-table-is-refused.md`
- `hooks/config.py`: lines 60–122, 140–380 and 640–660, and the diff of `pact_declaration`, `stray_pact_rows`, `_shaped_item` and `stray_refusal`
- `hooks/blocks.py`: `gfm_lines` and `walk_text`
- `skills/evidence-check/scripts/evidence_check.py`: `gfm_lines`, lines 3730–3900 (`NOTIFY_ROW_SHAPE` and `record_pact_changes`) and the imports
- `templates/config.md`: lines 1–45 and 376–425; `seal/config.md`, through the probe and grep
- the test diff of `tests/test_a_signatory_declares_its_pact.py`, `tests/test_a_signatory_records_a_pact_change.py`, `tests/test_pact_check.py`, `tests/test_a_signatorys_ci_prints_its_pact.py` and `tests/test_every_reader_ends_a_line_where_gfm_does.py`
- the diff of `docs/the-pact.md`; `bin/test`
- `git show --name-only fa4ddfe1`

Every probe file was deleted, and the clone and its round directory were removed before handover.
