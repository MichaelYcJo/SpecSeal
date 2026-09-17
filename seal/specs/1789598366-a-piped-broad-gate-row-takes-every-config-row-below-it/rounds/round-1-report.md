# Round 1 review — a piped broad gate row takes every config row below it (#415)

Target SHA `028f71ad8c588d8b3f08b94104fabd79ce4015a1`, branch
`fix/415-a-piped-broad-gate-row-takes-every-config-row-below-it`, base
`release/v0.12.0`. Reviewed in a `git clone --no-local` at that commit;
nothing was written in the working checkout except this file.

## How the four findings hang together

The branch does what it says. Every red-first mutation the plan names goes
red when it is restored from bytes, and I ran all five myself. What it does
not do is carry one measurement all the way to the person.

```
the reader learns `\|`
        ↓
① the refusal it feeds states the cost of a refused line WITHOUT the
  condition the branch itself measured — false when that line is the
  table's first row
        ↓ the same regex change, in the other direction
② a cell whose value ends in a backslash stopped being a row. `plan.md`
  says a widened pattern can only make MORE lines into rows
        ↓ ① and ② land in the same place
③ a `Broad gate` row that is in the file, below a line the reader
  refused, is still reported as ABSENT — the wrong-cause message #415
  was opened about, one item over
        ↓ and separately
④ for a BARE pipe, `seal mode` still writes a second `Mode` row. The
  changelog reads as if that were closed
```

Findings from reading and findings from execution are labelled apart below,
and every claim I make about behaviour was executed.

---

## 🟡 1. The refusal tells a person rows were lost that were not

`skills/verify/scripts/broad_gate.py:283` — the new branch in `missing_row`:

```
Nothing read it, so there is no command to seal over — and every row written
BELOW that line is lost with it, each falling back to its default with
nothing said anywhere.
```

That sentence is unconditional. The branch measured that it holds only under
a condition, and wrote the condition into five places — `templates/config.md`
line 224 (*where a row above it already parsed*),
`seal/specs/1789598366-…/overview.md` §*Fed back into the spec*,
`seal/specs/1789598366-…/changelog.md`'s closing paragraph, the first row's
Notes cell in `seal/ledger/1789598366-…md`, and the comment above
`PIPED_TABLE` at `tests/test_the_mode_question_is_asked_once.py:154`. The one
place it is missing is the sentence a person actually reads.

**Executed.** A config whose piped `Broad gate` line is the table's **first**
row:

```
| Item | Value |
|---|---|
| Broad gate | bin/test -q | tee out.txt |
| Mode | shared |
| Record language | English |
```

`config_rows` returns `[('Mode', 'shared'), ('Record language', 'English')]`
— the rows below it **arrived**. `broad_command` returns `None`, so
`missing_row` fires and tells the person those two rows are lost and are
falling back to defaults. They are not. The person goes and reformats a
`Mode` row that was read correctly.

The cause is that `refused_row` at `hooks/config.py:156` does not track what
`config_rows` tracks. `config_rows` breaks on an unparseable line only once
`found` is non-empty; `refused_row` has no `found` at all, so it names a line
that did not end the table.

Two more documents carry the same unconditional sentence, and one case pins
it there:

| Where | Line |
|---|---|
| `skills/config/SKILL.md:89` | *every row below it in the file is lost with it* |
| `skills/implement/orchestration.md:159` | *every row written below it in the file is lost with it* |
| `tests/test_first_setup_asks_once.py:222` | asserts that sentence is present |
| `seal/ledger/1789598366-…md`, row 3 | *says every row below it is lost too* |

The ledger fragment states the narrowing in row 1 and restates the
unconditional claim in row 3, so the fragment disagrees with itself.

---

## 🟡 2. The escape narrows what parses, and `plan.md` says that cannot happen

`hooks/config.py:70` — `CELL = r"(?:[^|\\]|\\.)"`. A backslash must now be
followed by a character inside the cell, so a value whose last character is a
backslash, with no space before the closing pipe, no longer matches.

**Executed**, old pattern against new on the same lines:

| Line | Before this branch | After |
|---|---|---|
| `| Broad gate | C:\Users\x\tools\|` | `('Broad gate', 'C:\Users\x\tools\')` | no row |
| `| Broad gate | C:\Users\x\tools\ |` | unchanged | unchanged |

`plan.md` §*Operational impact* states the opposite as a fact — *A widened
cell pattern can only make more lines into rows, never fewer* — and
`questions.md` M3 states it again in its options cell. M3's measurement is
sound and its population is named (1,449 tracked files, ten with a readable
table); what is wrong is the generalisation from that population to a
property of the pattern. `spec.md` §*What this repair cannot see* does not
name this shape either.

The behaviour itself is arguably the price of the escape and may be kept. The
claim that there is no compatibility break cannot be.

---

## 🟡 3. A `Broad gate` row below a refused line is still reported absent

`skills/verify/scripts/broad_gate.py:265` — `refused_broad_row` returns the
refused line only when its own first cell is `Broad gate`. Where the refused
line names some other item, the gate falls back to the absent-row refusal.

That is correct when there is no `Broad gate` row. It is the #415 defect
again when the row is sitting below the refused line.

**Executed**, and it is finding 2 that makes it reachable without anybody
typing a pipe:

```
| Item | Value |
|---|---|
| Mode | shared |
| Notes | see C:\docs\|
| Broad gate | bin/test -q |
```

| | Before this branch | After |
|---|---|---|
| `config_rows` | all three rows | `[('Mode', 'shared')]` |
| `broad-gate` says | runs the command | *has no `Broad gate` row* |

A config that worked now refuses, and the refusal names a cause that is not
the real one — which is the sentence `spec.md` opens with as the thing being
repaired. `agent-contract` §12 asks for the class, and the class here is *a
`Broad gate` row the reader could not reach*; the branch closed the member
where the refused line is itself the `Broad gate` line.

`tests/test_the_seal_is_taken_once_by_the_sealer.py:952` pins the narrow
behaviour with a fixture that has **no** `Broad gate` row at all, so it
cannot see the case where one exists below the refused line.

Neither `spec.md` §*What this repair cannot see* nor `overview.md` §*Not
done* names this shape.

---

## 🟡 4. `seal mode` still writes a second `Mode` row, and the records read as if it did not

**Executed.** `write_row` over a config whose `Broad gate` row carries a
**bare** pipe, with `Mode` below it:

```
| Record language | English |
| Mode | shared |              ← inserted by the command
| Broad gate | bin/test -q | tee out.txt |
| Mode | shared |              ← the person's own row
```

`declared` answered `('none', '')` and the file came back two `Mode` rows
deep — bit for bit the outcome `questions.md` M1 measured and the ledger
calls *the worst outcome in this work item*. Phase 1 closes it for the
escaped spelling only, and the branch says elsewhere that the bare spelling
is the one somebody reaches for first.

`templates/config.md:224` is honest about this — it says `seal mode` writes a
second row. Three disclosure sites stop one sentence short:

| Where | What it says | What it does not say |
|---|---|---|
| `changelog.md:20-25` | *`seal mode` **was** writing a second `Mode` row … Measured, and now pinned* | that it still does, for a bare pipe |
| `changelog.md:43-46` | *still invisible to the mode gate, which still simply asks the question again* | what answering that question then does to the file |
| `overview.md` §*Not done* | the same sentence | the same |
| `spec.md` §*What this repair cannot see* | the same sentence | the same |

A reader of the released changelog closes it believing the duplication is
gone. And nothing in the branch — not `overview.md` §*Not verified*, not
`seal/follow-up.md` — records that a file already two rows deep is repaired
by nothing, which `skills/implement/scripts/seal.py:1437` says in its own
comment.

---

## ⬜ 5. Two corrections in `refused_row`

`hooks/config.py:156`.

- The scan steps past a second `| Item | Value |` header and a stray
  separator unconditionally, where `config_rows` **breaks** at both once a
  row has been found. **Executed**: over a file whose second table holds the
  refused line, `config_rows` returns `[('Mode', 'shared')]` and
  `refused_row` returns `| Broad gate | a | b |` from the table below. The
  docstring's *the scan stops there rather than reaching into whatever table
  comes next* reads wider than the code delivers. Reachability is low — a
  blank line between the two tables ends the scan correctly — and the fix
  proposed for finding 1 closes it as a side effect.
- The docstring says *A line is one of these only when it BEGINS with a
  pipe*; the code tests `line.lstrip().startswith("|")`, so an indented line
  counts. **Executed**: `  | Broad gate | x | y |` is returned and matched.
  The behaviour is the better one; the sentence describes a stricter rule
  than the code has.

---

## What I verified and did not open

Each of these was executed in the clone, at the target SHA, restoring every
mutated file from bytes.

- **Phase 1's named mutation goes red on the count, not the value.** With
  `CONFIG_ROW`'s value cell reverted to `[^|]*?`, the assertion that fires
  first is `assert len(rows) == 4` and it reports *the table has four rows
  and 1 came back*. The ordering the case claims for itself is real.
- **Phase 2's mutation.** The new branch made unreachable →
  `test_an_unescaped_pipe_is_named_as_a_line_that_will_not_parse` fails.
- **Phase 2's A5 guard.** `test_the_absent_row_refusal_sends_the_question_to_a_person`
  builds its config with `row=False` and no unparseable line, so the new
  branch cannot fire for it — the old message cannot have been swallowed.
  Read, then confirmed by the mutation below.
- **The first-cell reading dropped** → `test_a_refused_row_of_some_other_item_is_not_read_as_this_one`
  fails, naming the line it wrongly accepted.
- **Phase 3's identity assertion distinguishes a copy.** I replaced `items`
  with a byte-faithful reimplementation compiled in the test file itself —
  same escape, same stop rules, same results — and
  `test_this_file_loads_the_one_reader_and_not_a_copy_of_it` failed on
  `__code__.co_filename`. An import check would have passed.
- **The Windows constraint.** With `unescaped` widened to
  `re.sub(r"\\(.)", r"\1", cell)`,
  `test_a_windows_path_survives_the_reader_exactly_as_written` fails. Q1's
  binding constraint is pinned.
- **Phase 4's named mutation.** The template's old pipe sentence restored →
  `test_the_allowed_list_says_how_a_pipe_is_written` fails.
- **The two ledger claims were REMOVED, not re-pointed.** The old fragment's
  header count went 8 → 7, the pipe row is gone from it, and the new claim is
  a row of this work item's own fragment. The other rows in that fragment
  were re-stamped only.

Carried from the record chain rather than re-derived: the two stop rules'
history (#82 round 1 🟡 6 and round 2 🟡 5), which the branch moved from the
test copy into `hooks/config.py`'s docstring. I opened the moved text and
checked it matches; I did not re-derive the rounds.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | The refusal says every row below the refused line is lost, without the condition the branch measured; false when that line is the table's first row | `skills/verify/scripts/broad_gate.py:283` | open | Executed: `config_rows` returned the two rows below it while the refusal said they were lost. Same sentence in `skills/config/SKILL.md:89`, `skills/implement/orchestration.md:159`, and pinned by `tests/test_first_setup_asks_once.py:222` |
| 2 | A value ending in a backslash before the closing pipe stopped being a row; `plan.md` and `questions.md` M3 say a widened pattern can only make more lines into rows | `hooks/config.py:70` | open | Executed: old pattern read `('Broad gate', 'C:\Users\x\tools\')`, new pattern reads no row. M3's measurement is sound; the generalisation past its population is not |
| 3 | A `Broad gate` row below a refused line naming another item is still reported ABSENT — the wrong-cause message, one item over | `skills/verify/scripts/broad_gate.py:265` | open | Executed: a config that read three rows before the branch now refuses with *has no `Broad gate` row*. `agent-contract` §12; the case at line 952 uses a fixture with no such row |
| 4 | `seal mode` still writes a second `Mode` row for a bare pipe, and three of four disclosure sites read as if it were closed | `seal/specs/1789598366-…/changelog.md:20` | open | Executed: `write_row` left the file two `Mode` rows deep. `templates/config.md:224` says so; the changelog, `overview.md` §*Not done* and `spec.md` do not |
| ⬜ | `refused_row` steps past a second header where `config_rows` breaks, and its docstring describes a stricter rule than the code has | `hooks/config.py:156` | correction | Executed: a refused line from a second table came back as this table's; an indented line is accepted although the docstring says a line must begin with a pipe |
| 🟢 | Phase 1's mutation is red on the row COUNT, asserted before the value | `tests/test_the_mode_question_is_asked_once.py:189` | confirmed | Executed: *the table has four rows and 1 came back* |
| 🟢 | Phase 3's `__code__.co_filename` assertion distinguishes a faithful copy from the one reader | `tests/test_the_pull_request_language_is_the_repositorys.py:711` | confirmed | Executed: red against a byte-faithful reimplementation compiled in the test file |
| 🟢 | The Q1 constraint — exactly the two characters — is pinned | `tests/test_the_mode_question_is_asked_once.py:225` | confirmed | Executed: red under a general backslash unescape |
| 🟢 | A5: the absent-row message was not swallowed by the new branch | `tests/test_the_seal_is_taken_once_by_the_sealer.py:684` | confirmed | Read the fixture (`row=False`, no unparseable line), then executed the branch mutation |
| 🟢 | Two ledger claims REMOVED and rewritten into this work item's fragment, nothing re-pointed | `seal/ledger/1789445605-…md` | confirmed | Read: header 8 → 7, the pipe row gone, the new claim in this work item's own fragment |
| 🟢 | `hooks/mode-gate.py` is untouched and still answers the home or `""` | `hooks/mode-gate.py` | confirmed | Executed as part of the module run; the case at `tests/test_the_mode_question_is_asked_once.py:290` asserts it |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the six modules this branch touches, at the target SHA | exit 0 · 338 passed |
| Phase 1's mutation — `CONFIG_ROW`'s value cell back to `[^\|]*?` | exit 1 · 3 failed, first on the row count |
| Phase 2's mutation — the new branch in `missing_row` made unreachable | exit 1 · 1 failed |
| Phase 3's mutation — `items` replaced by a byte-faithful local copy | exit 1 · 1 failed on `__code__.co_filename` |
| Q1's mutation — `unescaped` widened to a general backslash unescape | exit 1 · 1 failed |
| Phase 4's mutation — the template's old pipe sentence restored | exit 1 · 1 failed |
| `refused_broad_row`'s first-cell reading dropped | exit 1 · 1 failed |
| Behaviour probe: a refused `Broad gate` line as the table's FIRST row | the two rows below it were returned while the refusal said they were lost |
| Behaviour probe: a value ending in a backslash, old pattern against new | a row before this branch, no row after it |
| Behaviour probe: `write_row` over a bare-piped config | the file came back two `Mode` rows deep |
| `bin/evidence-check --strict .` | exit 0 |
| The full suite, the repository-wide lint, the typecheck | **not yet** — the sealer's one broad run, after the rounds settle (`agent-contract` §2) |

All probe files and the clone were deleted before this report was handed over.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A file already two `Mode` rows deep is repaired by nothing | not recorded anywhere in this branch — finding 4 asks for the row | the repository owner |
| A pull-request arm reporting a malformed `seal/config.md` | `spec.md` §Out, by name | already deferred in the frame |

## Paste-ready fixes

### Finding 1 — `hooks/config.py`, beside `refused_row`

```python
def refused_row_ends_the_table(text):
    """Whether the line `refused_row` names is the one that ENDED the table.

    `config_rows` breaks on a line it cannot parse only once it has found a
    row; with nothing found yet it steps past that line and keeps reading,
    so every row below it still arrives. A refusal that says those rows were
    lost sends a person to reformat rows that were read correctly, which is
    the same shape #415 was opened about.

    A second header or a stray separator ends the table once a row has been
    found, so a line refused after one of those did not end anything either.
    """
    seen_header, found = False, False
    for line in text.splitlines():
        if not seen_header:
            if CONFIG_HEADER.match(line):
                seen_header = True
            continue
        if CONFIG_HEADER.match(line) or CONFIG_SEPARATOR.match(line.strip()):
            if found:
                return False
            continue
        if CONFIG_ROW.match(line):
            found = True
            continue
        if line.lstrip().startswith("|"):
            return found
        return False
    return False
```

### Finding 1 — `skills/verify/scripts/broad_gate.py#missing_row`

```python
    refused = refused_broad_row(home)
    if refused is not None:
        config = load(CONFIG_READER, "specseal_config_for_broad_gate")
        took_the_rows_below = config.refused_row_ends_the_table(
            config_text(home) or ""
        )
        cost = (
            " — and every row written BELOW that line is lost with it, each "
            "falling back to its default with nothing said anywhere"
            if took_the_rows_below
            else ". The rows below it were read: nothing had parsed above "
            "this line, and the stop rule needs a row before it can stop"
        )
        return (
            f"broad-gate: {os.path.join(home, CONFIG)} has a `{ROW}` line "
            "and this is it, written so that it does not parse as a row of "
            "that table:\n"
            f"    {refused.strip()}\n"
            f"Nothing read it, so there is no command to seal over{cost}.\n"
            "A cell of that table ends at a `|`. A value that needs one is "
            "written with markdown's own escape, `\\|`, which the reader "
            "reduces to a plain pipe before any shell sees it — so "
            f"`| {ROW} | bin/test -q \\| tee out.txt |` is the row that runs "
            "that command. `templates/config.md` §*What is refused, and what "
            "stays allowed* is where the row says so, and `/specseal:config` "
            "is the door to it. Nothing ran."
        )
```

### Finding 1 — the case, in `tests/test_the_seal_is_taken_once_by_the_sealer.py`

```python
def test_a_piped_row_that_is_the_tables_first_does_not_claim_the_rows_below(
    tmp_path,
):
    """Round 1 of #415. `config_rows` breaks on an unparseable line only once
    it has found a row, so a piped row written FIRST loses only itself. The
    refusal used to tell the person every row below it was gone — a true
    sentence about the wrong file, which is the shape this work item exists
    to end."""
    home = tmp_path / "seal"
    home.mkdir()
    (home / "config.md").write_text(
        "| Item | Value |\n|---|---|\n"
        f"| {ROW} | bin/test -q | tee out.txt |\n"
        "| Mode | shared |\n"
        "| Record language | English |\n",
        encoding="utf-8",
    )
    module = gate_module()
    said = module.missing_row(str(home))
    assert "does not parse as a row" in said, said
    assert "every row written BELOW that line is lost" not in said, (
        "the refusal claims rows were lost that the reader returned"
    )
    assert "the stop rule needs a row before it can stop" in said, said
```

### Finding 1 — the two documents

```
skills/config/SKILL.md — replace
  Written with a bare pipe the line parses as no row, `broad-gate` quotes it
  back, and every row below it in the file is lost with it.
with
  Written with a bare pipe the line parses as no row and `broad-gate` quotes
  it back. Where a row above it already parsed, every row below it is lost
  with it — the reader stops reading the table there. Written as the table's
  first row it loses only itself, because the stop rule needs a row before it
  can stop.
```

```
skills/implement/orchestration.md — replace
  and every row written below it in the file is lost with it.
with
  and, where a row above it already parsed, every row written below it is
  lost with it.
```

### Finding 2 — `spec.md` §*What this repair cannot see*, a fourth bullet

```
- **One shape that parsed before this change no longer does.** A cell whose
  value ends in a backslash immediately before the closing pipe — `| Broad
  gate | C:\Users\x\tools\|` — was a row under the old pattern and is not one
  under the new, because a backslash must now be followed by a character
  inside the cell. `plan.md` §*Operational impact* says a widened cell
  pattern can only make more lines into rows; that is true of every shape in
  the tree (M3's population, measured) and not true of the pattern. Writing
  the same value with a space before the closing pipe reads exactly as
  before.
```

### Finding 2 — the case, in `tests/test_the_mode_question_is_asked_once.py`

```python
def test_a_value_ending_in_a_backslash_is_the_one_shape_the_escape_narrows(
    config,
):
    """The escape costs one shape, and it is named rather than discovered.
    A backslash must be followed by a character inside a cell, so a value
    whose last character is a backslash with no space before the closing
    pipe stopped being a row. Written with the space it is untouched."""
    tight = "| Item | Value |\n|---|---|\n| Broad gate | C:\\Users\\x\\tools\\|\n"
    spaced = "| Item | Value |\n|---|---|\n| Broad gate | C:\\Users\\x\\tools\\ |\n"
    assert config.config_rows(tight) == [], (
        "the narrowing is deliberate; if this returns a row the pattern "
        "changed and the disclosure in `spec.md` is now wrong"
    )
    assert config.config_rows(spaced) == [
        ("Broad gate", "C:\\Users\\x\\tools\\")
    ], "a backslash that is not part of `\\|` is the value's own character"
```

### Finding 3 — `skills/verify/scripts/broad_gate.py#missing_row`, a third sentence

```python
    # Where the refused line names some OTHER item and it ended the table,
    # a `Broad gate` row below it is in the file and unreachable. Saying the
    # row is absent is the wrong-cause message this work item exists to end,
    # one item over.
    other = refused_other_row(home)
    if other is not None:
        return (
            f"broad-gate: {os.path.join(home, CONFIG)} has a line that does "
            "not parse as a row of its table, and the reader stops there:\n"
            f"    {other.strip()}\n"
            f"So a `{ROW}` row written BELOW it is invisible, and there is no "
            "command to seal over. A cell of that table ends at a `|`; a "
            "value that needs one is written `\\|`. `/specseal:config` is "
            "the door to the file. Nothing ran."
        )
```

with the companion in the same module:

```python
def refused_other_row(home):
    """The refused line that ENDED the table and names some item other than
    this gate's row, or None. A `Broad gate` row below such a line is in the
    file and unreachable, so the absent-row refusal is a true sentence about
    a cause that is not the real one."""
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    text = config_text(home)
    if text is None:
        return None
    line = config.refused_row(text)
    if line is None or not config.refused_row_ends_the_table(text):
        return None
    first = FIRST_CELL.match(line.strip())
    return None if first and first.group(1).strip() == ROW else line
```

### Finding 3 — the case, in `tests/test_the_seal_is_taken_once_by_the_sealer.py`

```python
def test_a_broad_gate_row_below_a_refused_line_is_not_reported_absent(tmp_path):
    """The class `agent-contract` §12 asks for: a `Broad gate` row the reader
    could not reach. The branch closed the member where the refused line is
    itself the `Broad gate` line; this is the member one item over, and the
    person's row is sitting in the file while the gate calls it absent."""
    home = tmp_path / "seal"
    home.mkdir()
    (home / "config.md").write_text(
        "| Item | Value |\n|---|---|\n"
        "| Mode | shared |\n"
        "| Notes | see C:\\docs\\|\n"
        f"| {ROW} | bin/test -q |\n",
        encoding="utf-8",
    )
    module = gate_module()
    said = module.missing_row(str(home))
    assert f"has no `{ROW}` row" not in said, (
        "the row is in the file, below a line the reader refused"
    )
    assert "does not parse as a row" in said, said
    assert "see C:\\docs\\" in said, "the refusal does not show the line"
```

### Finding 4 — `changelog.md`, the closing paragraph

```
  What this does not repair is written beside it: a pipe written WITHOUT the
  escape still is not a row, and what changes for that person is the message
  rather than the outcome. That includes the second `Mode` row — for a bare
  pipe `seal mode` still writes one, because the writer stops where the
  reader stops, and a file that is already two rows deep is repaired by
  nothing. A `Mode` row hidden below an unparseable line is also still
  invisible to the mode gate, which simply asks the question again. And the
  cost falls on the rows below a line that does not parse only when a row
  above it already parsed — the stop rule needs a row before it can stop.
```

### Finding 4 — `overview.md` §*Not verified*, a fifth row

```
| a `seal/config.md` already two `Mode` rows deep — no command in this plugin brings it back into agreement, and this branch adds none | the repository owner |
```

---

Needs a fix: yes — findings 1, 2, 3 and 4
Loses a record or crashes: no

## Proof block

Files opened: `hooks/config.py`, `hooks/mode-gate.py` (through the case),
`skills/verify/scripts/broad_gate.py`, `skills/config/SKILL.md`,
`skills/implement/orchestration.md`, `skills/implement/scripts/seal.py`
(`table_span`/`with_row` region), `templates/config.md`, `bin/test`,
`.github/scripts/run_tests.py`, `tests/test_the_mode_question_is_asked_once.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py`,
`tests/test_the_pull_request_language_is_the_repositorys.py`,
`tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`,
`tests/test_first_setup_asks_once.py`,
`tests/test_the_settings_have_a_front_door.py`, `seal/config.md`,
`seal/ledger/1789598366-…md`, `seal/ledger/1789445605-…md`,
`seal/specs/1789598366-…/{spec,plan,questions,routing,overview,changelog,survivors}.md`,
`~/.claude/skills/writing-style/SKILL.md`.

Commands run: listed in §*Executed probes*, all in a `git clone --no-local`
at `028f71ad`, exit codes read directly and never through a pipe.
