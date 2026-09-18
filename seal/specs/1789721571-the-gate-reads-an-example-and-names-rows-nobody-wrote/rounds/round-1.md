# 1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote — review round 1

| Field | Value |
|---|---|
| Target SHA | cbe45e94b027dc4d40598575b029ca2b53145e64 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 445 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — finding 1, `seal mode` writing a row no walk reads and reporting it as written; finding 2, the fenced-row refusal naming a cause that is not the real one; finding 3, the three cost sentences answering about lines from a count of rows. |
| Loses a record or crashes | no — nothing leaves the root and nothing raises; finding 1 only appends to a person's `config.md` and never removes from it. |

- [ ] Pass

## What this round was asked

Round 1 of the whole branch, with no round before it and nothing inherited. The reviewer was asked to judge spec compliance before quality against the frame the framer wrote and two `smith` segments built to, and to **re-derive both enumerations rather than inherit them** — #429's class is *a walk of a markdown table with no fence state in front of it*, #430's is *a sentence about what lies below a line, computed without asking what is there*. It was asked to judge whether each of `spec.md` §*Out, each with why*'s exclusions holds, not whether it would have drawn them.

Six shapes were named to try to break: the fence rule against CommonMark, the three walks answering identically across two ways of splitting lines, the two reads behind one refusal, `config_rows`'s stop rule surviving a filter in front of it, the writer's index space after `table_span` started skipping lines, and `fenced_row` as the complement of `unfenced`.

Two corrections were handed over so they would not be re-found: the fixture-tag failure phase 1 reported as a repository defect, which was this clone missing two tags that were on `origin`; and a false fact in phase 2's own spawn prompt about `seal/config.md` carrying no backticks, which the build caught and recorded as a divergence.

The broad gate was explicitly out of the round's hands (`agent-contract` §2), and the round wrote no record and no `plan.md` row.

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

## Paste-ready fixes

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
```python
    assert "never closed" in out.stderr, (
        f"the refusal names no cause the person can act on:\n{out.stderr}"
    )
```
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
| `unfenced`, `config_rows` and `table_span` over `\x0b \x0c \x1c \x1d \x1e \x85 |
| `config_rows` over this repository's `seal/config.md`, over `templates/config.md`, and over the `## Broad gate` block pasted above and below a live table | `('mode', 'shared')` and the row's own command; the live rows in both paste positions |
| `hooks/config.py` and `broad_gate.py` load counting on one refusal | `config.md` read twice, `hooks/config.py` executed twice on the site-1 path |
| Broad gate — the full suite, the repository-wide lint and the typecheck | not yet. It is the sealer's, once, after the rounds settle (`agent-contract` §2), and it has not come due while finding 1 is open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `round_record.py` and `chain_check.py` were not driven against a fenced example table; `evidence_check.py` was, and shares the class | already deferred in this branch — `seal/follow-up.md`, ticket #444 | the repository owner |
| The full suite, the repository-wide lint and the typecheck | the broad gate, after the rounds settle | the sealer |
