# Round 1 — the gate reads an example and names rows nobody wrote

Target SHA `cbe45e94b027dc4d40598575b029ca2b53145e64`, base `release/v0.12.1`,
draft pull request #445. No earlier round; nothing inherited.

Read in a `git clone --no-local` of the repository at the target SHA. Nothing
was written in the working tree except this report.

## The headline

The two tickets are closed as framed. Both classes were re-derived rather than
inherited, and both hold: #430's four sites each ask what was written below
the line they speak about, and #429's fence rule reaches all three walks.

**What the fence rule opened is a fourth walk nobody re-checked — the one that
WRITES.** `skills/implement/scripts/seal.py#table_span` now skips fenced
lines, so for a file whose live table sits under a fence nobody closed, it
finds no table at all and `with_row` appends its new table at the end of the
file — inside that fence. `seal mode` then prints that it wrote the row, and
the row it wrote is invisible to every reader. It does not converge: the
command can be run forever and the mode stays undeclared.

`spec.md` A4 pins the writer against a fenced example sitting **above a live
table**, which is the shape where a live table survives the filter. The shape
where none survives is A5's, and A5 is asserted against `broad-gate` only.

## Stage 1 — spec compliance

Judged against `spec.md` §*User scenarios & acceptance* A1–A11 and §*Data &
interfaces*. Everything below is **executed** unless it says *read*.

- **A1, A2, A3, A6, A8, A9, A10 hold.** Each has a case, and the three named
  modules are green in a clean clone at the target SHA: `176 passed, 3
  skipped`, exit code read directly, 0.
- **A4 holds for the shape it states and does not generalise.** The writer and
  the reader agree about which row is the row whenever a live table survives
  the fence filter. Finding 1 is the shape where none does.
- **A5 holds to the letter and fails the sentence behind it.** The gate exits
  2, nothing runs, and the refusal names the fenced `| Broad gate |` line
  rather than calling it absent — all asserted. What the refusal then tells
  the person to do is wrong (finding 2).
- **A7 holds.** CRLF and LF agree. The divergence the two spellings of a line
  genuinely have is measured in the ⬜ row below and moves no answer.
- **A11 holds, re-derived.** Over this repository's own `seal/config.md`:
  `declared_mode` is `('mode', 'shared')`, `refusal` is `([], [], None)`, and
  `config_rows` returns the `Broad gate` value byte-identical to the row as
  written.
- **§*Data & interfaces*, the wording contract, is followed and the contract
  itself over-claims.** Three of the four sentences say *nothing was written
  below it* while the code asks what ROWS were written below it. Finding 3.

**§*Out, each with why* — each exclusion judged, not inherited.**

| Exclusion | Verdict |
|---|---|
| The `else` arm of `missing_row` | **Holds.** Read: the arm is reachable only with `mine` refused BELOW the stopper, so the clause *this one included* always names the quoted line. It never speaks about an empty set |
| `config_rows`'s stop rule | **Holds.** Both halves still operate on what survives the filter — measured: a second `\| Item \| Value \|` header written below a fenced block still ends the table |
| `seal/parity.md`'s table | **Holds.** Read: `hooks/optin.py#parity_config` and `skills/evidence-check/scripts/evidence_check.py` both test the file's existence and nothing parses it |
| Four-space indented code blocks | **Holds.** A decision in force, unchanged |
| The other markdown-table readers | **Holds as a boundary, and the boundary is drawn one reader short of measured.** `evidence_check.py` was measured to share the class and is filed as #444; `round_record.py` and `chain_check.py` were not driven, and `seal/follow-up.md` says so. Already deferred — see §Deferred |

## Stage 2 — findings

### 1 🔴 `seal mode` reports a row it wrote and the row does not exist — and it never converges

`skills/implement/scripts/seal.py:1419` (`table_span`), `:1456`
(`with_row`), `:1484` (`write_row`), `:1880` (`mode_report`).

`table_span` now reads through `hooks/config.py#unfenced`. For a `config.md`
whose live table is swallowed by a fence nobody closed, that walk sees no
header, so it returns `(-1, -1)`. `with_row` falls to its third case and
appends `| Item | Value |`, a separator and the row at the **end of the
file** — which, under an unclosed fence, is inside that fence. `write_row`
returns `""`, and `mode_report` treats an empty return as the write having
taken: it prints the success sentence and sets `kind, value` to `"mode"` and
the folder's answer without re-reading.

Executed against the target SHA, on `spec.md` A5's own fixture:

```
run 1: write_row='' declared_mode=('none', '')
run 2: write_row='' declared_mode=('none', '')
run 3: write_row='' declared_mode=('none', '')
file grew from 9 to 21 lines
```

and end to end, three consecutive `seal mode` invocations in a fixture
repository, each exit 0, each printing:

```
no `Mode` row was declared, so one was written from where the folder is: `| Mode | shared |` in seal/config.md
  folder: shared seal/
  row:    shared seal/config.md

They agree.
```

After the third, `declared_mode` is still `('none', '')` and the file carries
three duplicate tables.

**It is a regression this branch introduces, measured in both directions.**
The same fixture at `release/v0.12.1`:

```
run 1: write_row='' declared_mode=('mode', 'shared')   file 9 -> 9 lines
```

At base the fenced table was visible to the writer, so the row it rewrote was
read back. The fence rule takes the visibility away from the writer and
leaves the append at end-of-file untouched.

**Why it matters beyond one file.** `hooks/mode-gate.py` is a `PreToolUse`
hook whose own docstring states the budget: *Two prompts per session per
repository and no more … Zero once the row exists, which `seal mode` writes.*
For this shape the row never comes to exist, so it is two prompts every
session, forever, on a session that may have nobody at the keyboard — the
outage `CLAUDE.md` §*The goal a design is chosen against* is written against.
`plan.md` §*Operational impact* claims *two prompts, once, and then silence*
for a repository whose `Mode` row sits inside a fence, and `phases/phase-2.md`
repeats it. Both are false for the unclosed case.

Two fixtures reach it and neither is contrived: a live table under an unclosed
fence, and a file whose only table is a fenced example the fence never closes.

### 2 🟡 The refusal quotes a person's live row back at them and names the wrong cause

`skills/verify/scripts/broad_gate.py:546-560` (the `fenced_row` branch of
`missing_row`), `:339` (`fenced_row`).

Executed on A5's fixture — a `config.md` with `` ```markdown `` above the live
table and no closing run:

```
broad-gate: <root>/seal/config.md has a `Broad gate` line and this is it, written inside a code fence:
    | Broad gate | bin/test -q |
...
Move the row into the `| Item | Value |` table that stands outside every fence, or add that table if the file has none.
```

The quoted line is the person's live row. It is already in an
`| Item | Value |` table, and that table is not inside any fence the person
wrote — a fence three lines above it was opened and never closed. The message
tells them to move a row that is where it belongs, and never says the word
*unclosed*. Following it exactly changes nothing.

This is the shape #415, #429 and #430 were all opened about: a true sentence
about a cause that is not the real one. `templates/config.md` already states
the fact the message is missing — *A fence that is never closed runs to the
end of the file, so everything under it — the live table included — reads as
undeclared: `broad-gate` exits 2 with a message* — but the message does not
carry it.

The information is one line from the code. `unfenced` already knows it: the
loop ends with `opener` not `None`. It is thrown away at the `yield`.

### 3 🟡 *nothing was written below it* is answered from rows, so it is false whenever another malformed line is below

`skills/verify/scripts/broad_gate.py:457-462` (site 1), `:470-475` (site 2);
the wording is fixed by `spec.md` §*Data & interfaces*.

`refusal` returns every refused line, and `below` holds only the **rows**
under the stopping line. The three repaired sentences ask about rows and
then speak about what was *written*. Executed, site 1 — a table whose only
two lines are both unparseable:

```
| Item | Value |
|---|---|
| Broad gate | bin/test -q | tee out.txt |
| Record language | a | b |
```

```
... Nothing else was lost with it, because nothing was written below it: nothing had parsed above this line either ...
```

A line was written below it, and `refusal` returned it — the second element of
`refused`.

Site 2 is the same and costs more, because the arm's closing clause is a
prediction:

```
| Item | Value |
|---|---|
| Mode | shared |
| Broad gate | bin/test -q | tee out.txt |
| Record language | a | b |
```

```
... and nothing was written below it, so nothing else was lost with it: this one line is the whole of what changes.
```

*This one line is the whole of what changes* is false here. Fix the quoted
line and the reader walks on to `| Record language | a | b |`, which becomes
the new stopping line. The person is told one edit finishes the file, and it
does not.

#430's class is *a sentence about what lies below a line, computed without
asking what is there*. The repair narrowed *what is there* to *what parsed as
a row*, which closes the shape the tickets named and leaves this one.

### ⬜ `overview.md` §*Not done* states a mechanism the tree disproves

`seal/specs/1789721571-…/overview.md` §*Not done*, the paragraph committed at
`35a9638`.

> **A fresh clone starts in the state this one was in**, because `git clone`
> fetches tags reachable from the fetched branches, and these two are not

`git clone` copies **every** tag by default; it is `git fetch`, and
`git clone --no-tags`, that fetch only reachable ones. Executed: a plain
`git clone --no-local` of this repository at the target SHA carries both
`fixture/*` tags, `remote.origin.tagOpt` is unset, and
`bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` is `55
passed`, exit code read directly, 0.

The rest of the paragraph is right and the correction was worth making — the
tags are on `origin`, the module is green, nothing in the repository was
wrong. Only the sentence about what a fresh clone gets is false, and it is the
sentence written for the next reader.

### ⬜ Nine `seal/ledger.md` rows carry a `Checked` date no record backs

`seal/ledger.md`, twelve rows changed in this range.

All twelve had `Checked` moved to `2026-09-18`. Three record a 2026-09-18
re-read (two say *Re-read 2026-09-18 for #430*, one carries the date in its
evidence cell). The other nine name 2026-09-17 or earlier as their last
re-read and say nothing about this one. Neither `phases/phase-1.md` nor
`phases/phase-2.md` mentions the ledger re-verification at all.

Updating the hashes is right — the anchored content moved, and the alternative
is DRIFTED rows. `CLAUDE.md` says the `Checked` column holds the date somebody
read the code, so nine rows now claim a reading that no record in this branch
states was taken.

### ⬜ `unfenced` strips two of the eight terminators `splitlines` splits on

`hooks/config.py:119` (`unfenced`), the `rstrip` at `:179`.

`config_rows` and `refusal` pass `text.splitlines()`; `table_span` passes
`text.splitlines(keepends=True)`. `rstrip("\r\n")` removes CR and LF, and
`str.splitlines` also breaks on `\x0b \x0c \x1c \x1d \x1e \x85  
 ` — so for those eight the two walks are handed different text for the
same line.

Executed over all eight, in a row position and in a fence-delimiter position:
**no answer moves.** Every retained terminator is absorbed by `CONFIG_ROW`'s
trailing `\s*` or by `str.strip()` in the closing-fence test, and
`config_rows`, `table_span` and the quoted refusal line agree in every case.

Reported because the docstring's safety argument is scoped to LF and CRLF,
which is accurate, while the pattern it rests on is wider — a future narrowing
of `CELL` or of the closing-fence test would break the agreement silently, and
A7 would not see it.

### ⬜ One refusal re-executes the reader once per helper

`skills/verify/scripts/broad_gate.py:185` (`load`), `:254`, `:268`, `:339`.

`refusal`, `rows_read` and `fenced_row` each call `load(CONFIG_READER, …)` and
`config_text(home)` of their own, and `load` runs `exec_module` every time —
recompiling five regexes per call. Measured on one refusal: `config.md` read
twice and `hooks/config.py` executed twice on the site-1 path, three times
where the fenced branch is reached. `phases/phase-1.md` already names this
(*each call re-reads `config.md` and re-imports `hooks/config.py` by path*).
It is a refusal path that ends the run, so nothing is hot; noted because the
repeated read is also what makes the two answers able to disagree, which is
what `354c09d` had to pin as a case.

### ⬜ The table-spanning consequence is the only extra one I could find

`phases/phase-2.md` records that a table can now span a fenced block. I looked
for a second consequence of filtering in front of the walk and found none:
measured, a second `| Item | Value |` header below a fenced block still ends
the table, prose below a fenced block still ends it, and the block
`/specseal:config` copies out of `templates/config.md` gives the live rows
whether it is pasted above or below the live table. The exposure is narrow —
pipe lines written directly under a fenced block with no prose and no second
header between them — and the recorded direction (*more of a person's live
table is read*) holds for it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 `seal mode` writes the `Mode` row inside an unclosed fence, reports success, and never converges — two prompts every session, forever, and the file grows a table a run | `skills/implement/scripts/seal.py#table_span`, `#with_row`, `#mode_report` | open | Executed at the target SHA and at `release/v0.12.1`: three runs give `declared_mode == ('none', '')` and 9 → 21 lines at HEAD, `('mode', 'shared')` and 9 → 9 lines at base. A regression this branch introduces. `plan.md` §*Operational impact* and `phases/phase-2.md` both assert *and then silence* for this shape |
| 2 | 🟡 The fenced-row refusal quotes a person's live row back as *written inside a code fence* and tells them to move it into a table it is already in, never naming the unclosed fence | `skills/verify/scripts/broad_gate.py#missing_row`, `#fenced_row` | open | Executed on A5's own fixture. Following the instruction exactly changes nothing. `templates/config.md` states the missing fact; the message does not carry it. `unfenced` already computes it and discards it at the yield |
| 3 | 🟡 *nothing was written below it* and *this one line is the whole of what changes* are answered from rows, so both are false when another unparseable line sits below the quoted one | `skills/verify/scripts/broad_gate.py#missing_row`, `spec.md` §*Data & interfaces* | open | Executed at site 1 and site 2. `refusal` returns the line in `refused` and the sentence says nothing was written. At site 2 the reader stops at the next malformed line, so one edit does not finish the file |
| ⬜ | `overview.md` §*Not done* says a fresh clone loses the fixture tags because `git clone` fetches only reachable tags; it copies every tag by default | `seal/specs/1789721571-…/overview.md` §*Not done* | correction | Executed: a `git clone --no-local` at the target SHA carries both `fixture/*` tags and the module is `55 passed`, exit 0. The rest of the corrected paragraph matches the tree |
| ⬜ | Nine of the twelve `seal/ledger.md` rows re-stamped in this range carry a 2026-09-18 `Checked` date that no record states was read | `seal/ledger.md` | correction | Three rows record the re-read; nine name 2026-09-17 or earlier as their last. Neither phase record mentions the re-verification |
| ⬜ | `unfenced`'s `rstrip("\r\n")` leaves six of the eight terminators `splitlines` breaks on, so the two spellings of a line differ in text | `hooks/config.py#unfenced` | answered | Executed over all eight in two positions: no answer moves. The docstring's LF/CRLF scoping is accurate; the latent width is what is reported |
| ⬜ | One refusal re-executes `hooks/config.py` and re-reads `config.md` once per helper | `skills/verify/scripts/broad_gate.py#load` | answered | Measured: two of each on the site-1 path, three where the fenced branch is reached. Already named in `phases/phase-1.md` |
| ⬜ | The table-spanning consequence is the only additional one I could find | `hooks/config.py#unfenced`, `#config_rows` | answered | Measured: the second-header stop, the prose stop, and the copied block above and below the live table all behave as before |
| 🟢 | A11 — this repository's own answers are unmoved | `seal/config.md` | confirmed | Executed: `('mode', 'shared')`, `([], [], None)`, and the `Broad gate` value byte-identical to the row |
| 🟢 | The `else` arm of `missing_row` is correctly out of scope | `skills/verify/scripts/broad_gate.py#missing_row` | confirmed | Read: reachable only with the quoted line refused below the stopper, so *this one included* always names it |
| 🟢 | `seal/parity.md`'s table is correctly out of scope | `hooks/optin.py#parity_config` | confirmed | Read: existence test only, in both readers |
| 🟢 | `config_rows`'s stop rule is unchanged on what survives the filter | `hooks/config.py#config_rows` | confirmed | Executed: a second header below a fenced block still ends the table |
| 🟢 | The three named modules are green at the target SHA in a clean clone | `tests/` | confirmed | `176 passed, 3 skipped`, exit code read directly, 0 |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_mode_question_is_asked_once.py tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py -q` in a clean clone at `cbe45e9` | `176 passed, 3 skipped`; exit code read directly, 0 |
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q` in the same clone, no tags fetched by hand | `55 passed`; exit code read directly, 0 |
| `write_row` three times over A5's fixture and over a fenced-only table, at `cbe45e9` | `declared_mode` stays `('none', '')` all three times; files grow 9 → 21 and 6 → 18 lines |
| The same two fixtures against `hooks/config.py` and `seal.py` taken from `release/v0.12.1` | `('mode', 'shared')` after run 1 both times; files 9 → 9 and 6 → 7 lines |
| `seal.py mode` three times, as a subprocess, in a committed fixture repository holding A5's `config.md` | exit 0 each time, each printing *one was written from where the folder is* and *They agree*; `declared_mode` still `('none', '')`, three duplicate tables in the file |
| `missing_row` over site 1 and site 2 fixtures carrying a second unparseable line | both print *nothing was written below it*; `refusal` returned that line in `refused` |
| `missing_row` over A5's fixture and over a fenced example beside a live table with no `Broad gate` row | both print the fenced-row refusal and *Move the row into the `\| Item \| Value \|` table that stands outside every fence* |
| `unfenced`, `config_rows` and `table_span` over `\x0b \x0c \x1c \x1d \x1e \x85    ` in a row position and a fence-delimiter position | the two spellings of a line differ in text in all eight; no answer moves in any |
| `config_rows` over this repository's `seal/config.md`, over `templates/config.md`, and over the `## Broad gate` block pasted above and below a live table | `('mode', 'shared')` and the row's own command; the live rows in both paste positions |
| `hooks/config.py` and `broad_gate.py` load counting on one refusal | `config.md` read twice, `hooks/config.py` executed twice on the site-1 path |
| Broad gate — the full suite, the repository-wide lint and the typecheck | not yet. It is the sealer's, once, after the rounds settle (`agent-contract` §2), and it has not come due while finding 1 is open |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `round_record.py` and `chain_check.py` were not driven against a fenced example table; `evidence_check.py` was, and shares the class | already deferred in this branch — `seal/follow-up.md`, ticket #444 | the repository owner |
| The full suite, the repository-wide lint and the typecheck | the broad gate, after the rounds settle | the sealer |

## Paste-ready fixes

**Finding 1** — `skills/implement/scripts/seal.py#write_row`. The write is not
the claim; being read back is. Check before touching the file, so a refusal
leaves nothing behind.

```python
    new = (
        NEW_CONFIG.format(item=ROW_ITEM, value=value)
        if text is None
        else with_row(text, value)
    )
    # **The row is not written until it reads back.** `table_span` skips
    # fenced lines, so a file whose table is swallowed by a fence nobody
    # closed has no table this walk can see -- and `with_row` then appends
    # one at the END of the file, which is inside that fence. The write
    # succeeds, `declared_mode` still answers "none", and `seal mode` reports
    # a row that no walk reads: the mode gate asks again next session and the
    # file grows by a table a run. Checked here rather than after the write,
    # so a refusal leaves the person's file exactly as it was (#429).
    if not any(item == ROW_ITEM for item, _value in config_rows(new)):
        return (
            f"{path} has a fenced code block that is never closed, and "
            "everything under it -- the table this command would have "
            f"written the `{ROW_ITEM}` row into -- is inside it, where no "
            "walk of that table reads it. Nothing was written. Close the "
            "fence and run this command again."
        )
    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(new)
    except (OSError, ValueError) as exc:
        return f"{path} could not be written: {exc}"
    return ""
```

`mode_report` already prints a non-empty return as *the `Mode` row could not
be written: …* and falls back to the folder, so no caller changes. The case to
plant, in `tests/test_the_mode_question_is_asked_once.py`, seen red by
reverting this hunk:

```python
def test_a_row_that_would_land_inside_an_unclosed_fence_is_refused(tmp_path):
    """The writer's claim is that the row reads back. A fence nobody closed
    runs to the end of the file, so an append lands inside it -- and
    `seal mode` used to report a row it wrote that `declared_mode` could not
    see, every session, growing the file by a table each time."""
    home = tmp_path / "seal"
    home.mkdir()
    before = (
        "# Repository config\n\nAn example of the format:\n\n```markdown\n"
        "| Item | Value |\n|---|---|\n| Mode | shared |\n"
    )
    write_config(home, before)
    failed = seal.write_row(str(home), "shared")
    assert "never closed" in failed, failed
    assert (home / "config.md").read_text(encoding="utf-8") == before, (
        "a refused write touched the file"
    )
```

**Finding 2** — keep one fence rule and stop discarding what it already knows.
`hooks/config.py`: fold the walk into a classifier that keeps the state it
ends in, and make the generator a view of it.

```python
def fence_map(lines):
    """([(index, line)] outside every fenced block, the index of an opener
    that was never closed or None) — the one fence rule, computed once.

    `unfenced` below is the generator form all three walks read the file
    through; this is the same walk with the state it ENDS in kept. A fence
    that runs to the end of the file is the one thing about a fence a caller
    with somebody to tell has to be able to say: `broad-gate` quoting a live
    `| Broad gate |` row back as *written inside a code fence* and telling
    the person to move it is a true sentence about a cause that is not the
    real one, which is the failure #429 was opened about arriving one shape
    over. A second fence rule written for that question is the split this
    module exists to prevent.
    """
    shown, opener, opened_at = [], None, None
    for index, raw in enumerate(lines):
        line = raw.rstrip("\r\n")
        fence = FENCE.match(line)
        run = fence.group("run") if fence else ""
        info = fence.group("info") if fence else ""
        if opener is None:
            if run and not (run[0] == "`" and "`" in info):
                opener, opened_at = (run[0], len(run)), index
                continue
            shown.append((index, line))
            continue
        if run[:1] == opener[0] and len(run) >= opener[1] and not info.strip():
            opener, opened_at = None, None
    return shown, opened_at


def unfenced(lines):
    """<the existing docstring, unchanged>"""
    yield from fence_map(lines)[0]
```

`skills/verify/scripts/broad_gate.py`, beside `fenced_row`:

```python
def fence_left_open(home):
    """Whether a fenced code block in the root's config is never closed.

    Read off the one fence rule, not a second one. It is the difference
    between a row somebody pasted into an example block and a row that is in
    the live table with a fence opened above it — and the two need different
    sentences, because the second person has nothing to move.
    """
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    text = config_text(home)
    if text is None:
        return False
    return config.fence_map(text.splitlines())[1] is not None
```

and in `missing_row`'s fenced branch, replace the *Move the row* sentence with
one that reads the file:

```python
        where = (
            "A fenced code block above it is never closed, so it runs to the "
            "end of the file and takes the whole table with it. Close that "
            "fence — the row itself may already be where it belongs."
            if fence_left_open(home)
            else "Move the row into the `| Item | Value |` table that stands "
            "outside every fence, or add that table if the file has none."
        )
        return (
            f"broad-gate: {os.path.join(home, CONFIG)} has a `{ROW}` line and "
            "this is it, written inside a code fence:\n"
            f"    {fenced.strip()}\n"
            "A table inside a code fence is an example of the format and not "
            "this repository's own answer, so no walk of that table reads it "
            "— not this gate's reader, not the mode gate's, and not "
            "`seal mode`'s writer. The row is not absent: it is written where "
            f"nothing reads it, and there is no command to seal over.\n{where}\n"
            "`templates/config.md` §*What is refused, and what stays allowed* "
            "is where the rule says so, and `/specseal:config` is the door to "
            "the file. Nothing ran."
        )
```

`tests/test_the_seal_is_taken_once_by_the_sealer.py::test_an_unclosed_fence_hides_the_live_table_and_the_gate_says_which_line`
gains the assertion, which is what makes it red today:

```python
    assert "never closed" in out.stderr, (
        f"the refusal names no cause the person can act on:\n{out.stderr}"
    )
```

**Finding 3** — say what the code asks. Three string edits in
`skills/verify/scripts/broad_gate.py#missing_row`, and site 2's prediction
conditioned on the lines rather than the rows.

```python
    refused, below, stopper = refusal(home)
    mine, reached, after = None, False, []
    for position, (line, got) in enumerate(refused):
        if names_this_row(line):
            mine, reached = line, got
            after = [text for text, _got in refused[position + 1 :]]
            break
    if mine is not None:
        if stopper is None:
            if rows_read(home):
                ...
            else:
                cost = (
                    ". No row was written below it, so nothing else was lost "
                    "with it: nothing had parsed above this line either, so "
                    "the table had not begun and the stop rule needs a row "
                    "before it can stop"
                )
        elif mine is stopper:
            if below:
                ...
            else:
                cost = (
                    " — and no row was written below it, so nothing else was "
                    "lost with it"
                ) + (
                    ": this one line is the whole of what changes"
                    if not after
                    else ". There are more lines below it this reader will "
                    "not take as rows either, so fixing this one moves the "
                    "stopping place down rather than clearing the table"
                )
```

`spec.md` §*Data & interfaces* carries the old wording as the contract, so its
site 1 and site 2 bullets move with it, and `skills/config/SKILL.md`'s
last-row sentence and `templates/config.md`'s allowed-list cell say *no row
was written below it* for the same reason. The case, in
`tests/test_the_seal_is_taken_once_by_the_sealer.py`, red today:

```python
def test_a_second_unparseable_line_below_is_not_called_nothing(tmp_path):
    """#430's class is a sentence about what lies below a line computed
    without asking what is there. Asking `below` narrows *what is there* to
    *what parsed as a row*, and a second malformed line is neither a row nor
    nothing — and it is what the reader stops at next, so *this one line is
    the whole of what changes* is a prediction the file does not keep."""
    repo = build_repo(tmp_path / "repo", row=False)
    write(
        repo,
        "seal/config.md",
        "| Item | Value |\n|---|---|\n| Mode | shared |\n"
        f"| {ROW} | bin/test -q | tee out.txt |\n"
        "| Record language | a | b |\n",
    )
    commit(repo, "two lines the reader will not take")
    said = run_gate(repo, keep=tmp_path / "out").stderr
    assert "nothing was written below it" not in said, said
    assert "this one line is the whole of what changes" not in said, said
    assert "moves the stopping place down" in said, said
```

Needs a fix: yes — finding 1, `seal mode` writing a row no walk reads and reporting it as written; finding 2, the fenced-row refusal naming a cause that is not the real one; finding 3, the three cost sentences answering about lines from a count of rows.
Loses a record or crashes: no — nothing leaves the root and nothing raises; finding 1 only appends to a person's `config.md` and never removes from it.

## Proof

Files opened at `cbe45e94b027dc4d40598575b029ca2b53145e64`:

- `hooks/config.py`, `hooks/mode-gate.py` (docstring and the ask/deny lines),
  `hooks/optin.py:215-235`
- `skills/verify/scripts/broad_gate.py`, `skills/implement/scripts/seal.py`
  (lines 1300-1620, 1870-1930), `skills/evidence-check/scripts/evidence_check.py:858-875`
- `skills/config/SKILL.md` and `templates/config.md`, as the range's diff
- `tests/test_the_seal_is_taken_once_by_the_sealer.py` (the fixture helpers and
  the new cases), `tests/test_the_mode_question_is_asked_once.py` (A4 and A7),
  `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`, as the
  range's diff
- `seal/specs/1789721571-…/spec.md`, `plan.md`, `questions.md`, `overview.md`,
  `phases/phase-2.md`, `survivors.md`, `routing.md`, `changelog.md`
- `seal/ledger/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote.md`,
  `seal/ledger.md` as the range's diff, `seal/follow-up.md` as the range's diff
- `seal/config.md`, `bin/test`, `CLAUDE.md`

Probes: four scratch scripts named `test_tmp_*`, run once in a
`git clone --no-local` of this repository, all deleted. The clone, the venv
`bin/test` built inside it, and a scratch directory holding the two base-
revision modules are removed; `git worktree list` names one worktree, the
user's own, and `git status --porcelain` in the working tree is empty. No git
worktree was created.
