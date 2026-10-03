# 1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed — review round 2

| Field | Value |
|---|---|
| Target SHA | ed1476aaf59754b57ba53963378f0f0b15501692 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 749 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 10 (the restore removes a ledger file it could not read), 🟡 11 (a SIGTERM or SIGHUP between the re-stamp and the record erases the drift unrecorded), 🟡 12 (a change re-landed after its revert is not recorded), 🟡 13 (under an intended `always`, a declaration that will not read is silent at exit 0), 🟡 14 (a coordinate the re-read leaves records nothing at exit 0), 🟡 15 (the walker reads tables cmark-gfm does not render in two unstated shapes) |
| Loses a record or crashes | yes — 🔴 10 removes a whole ledger file; 🟡 11, 🟡 12 and 🟡 13 each re-stamp the ledger with the owed pact change never recorded, so the drift that would record it is gone |

- [ ] Pass

## What this round was asked

Round 2 is a verifying round. It targets `ed1476aa` over round 1's fix range `594e1007..fc5d8e61`, the release merge `2b25dc86` (#743, #744, #745) and the close commit. It was asked:
- whether each of round 1's fixes holds;
- whether the transaction that closed 🔴 1 can still lose an owed pact change or restore what it should not;
- whether 🟡 2's idempotence holds across repeated and interleaved runs;
- whether the walker and the oracle fix agree with cmark-gfm under an independent generator;
- whether the merge left #740's narrowing, this item's transaction and #736's row L4 all true.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 10 | The restore removes a ledger file the snapshot could not read (`snapshot` reads `OSError` as absent), and an unreadable `--into` is overwritten first (older, #736) | `skills/evidence-check/scripts/evidence_check.py:3519` | open | executed: an unreadable sibling fragment and an unreadable `--into` are both gone after a run that could not record; fix run in the clone: both kept, `--into` refused at exit 2 |
| 🟡 11 | A SIGTERM or SIGHUP between the re-stamp and the record erases the drift with nothing recorded; the policy says a run that dies is put back | `skills/evidence-check/scripts/evidence_check.py:4858` | open | executed: SIGTERM at the record step, status -15, ledger re-stamped, the next run records nothing; the window is `released_drift`, 9.83 s on this repository; fix run in the clone: status 143, ledger intact, next run records one row |
| 🟡 12 | A change re-landed after its revert is re-stamped and not recorded: the key is ever-recorded, not last-recorded | `skills/evidence-check/scripts/evidence_check.py:3699` | open | executed: A→B, B→A, A→B gives two rows, ledger at B; fix run in the clone: three rows, every idempotence case green |
| 🟡 13 | Under an intended `always`, a `Pact` row or `Pact notify` that will not read is silent at exit 0, the ledger re-stamped | `skills/evidence-check/scripts/evidence_check.py:3635` | open | executed: both shapes exit 0 with no record and no line; fix run in the clone: exit 1, ledger intact |
| 🟡 14 | A coordinate the re-read leaves (statement gone, file deleted under a minor anchor, no one place under the freeze) records nothing at exit 0, while a major-only BROKEN is recorded | `skills/evidence-check/scripts/evidence_check.py:3050` | open | executed: both cases exit 0 with no record; fix run in the clone: one `BROKEN` row each, a second run adds nothing |
| 🟡 15 | The walker reads tables cmark-gfm does not render in two unstated shapes, and the docstring's list-item limit names a shape it now refuses | `hooks/config.py:1020` | open | executed: 70 of 300,000 per seed at the target; fix run in the clone: 0 of 600,000, two pinned ids invert (named in the fix) |
| 🟢 | round 1's blocking finding is closed — an owed change that cannot be recorded re-stamps nothing on the five paths it named | `skills/evidence-check/scripts/evidence_check.py:4851` | confirmed | executed: 11 cases red with `restore` and the refusal disabled; each path prints `LEFT … nothing was re-stamped`, exits 1, ledger byte for byte. The `always` arm of its silent path is 🟡 13 |
| 🟢 | round 1's yellow 2 is closed — a second identical run adds nothing, per coordinate and in the reader's form | `skills/evidence-check/scripts/evidence_check.py:3699` | confirmed | executed: 5 cases red reversed; this repository's three `\|` coordinates, six runs over two edits, no duplicate. 🟡 12 is the reland the same key suppresses |
| 🟢 | round 1's yellow 3 is closed — `amended` is judged at the record's current hash only | `skills/evidence-check/scripts/pact_check.py:848` | confirmed | executed: its case red reversed |
| 🟢 | round 1's yellow 4 is closed — `.`, `-`, `_` for or before the slash are refused | `skills/evidence-check/scripts/pact_check.py:240` | confirmed | executed: 7 cases red reversed |
| 🟢 | round 1's yellow 5 is closed for the two mechanisms it measured — a line directly above, an open kind 1–5 block | `hooks/config.py:1021` | confirmed | executed: 6 cases red reversed; round 2's generator finds neither mechanism in 300,000. What remains is 🟡 15 |
| 🟢 | round 1's white 6 is closed — a pipe after an even backslash run is refused | `hooks/config.py:906` | confirmed | executed: 2 cases red reversed |
| 🟢 | round 1's white 7 is closed — a review row naming a dropped signatory stays refused, and the policy says so | `docs/the-pact.md` | confirmed | read; its case green in the module |
| 🟢 | round 1's white 8 is closed — a pact review takes a whole record, stated | `docs/the-pact.md` | confirmed | read |
| 🟢 | round 1's white 9 is answered — the `Re-read · P1-1` row carries its `Corrected` note | `seal/ledger/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed.md` | answered | read |
| 🟢 | the merge keeps #740's narrowing and this item's transaction; L4 holds of the merged code | `skills/evidence-check/scripts/evidence_check.py:3278` | confirmed | executed: #743's grid with the five pact modules, 1028 passed; `correction-check` exit 0; `evidence-check --strict` 0 drifted, 0 broken. L4 read |
| 🟢 | the oracle's switch to the raw-HTML-omitted render hides no table | `tests/gfm_table_oracle.py` | confirmed | executed: table counts equal across both renders, and round 2's regex reading equals `rows_under`, in every one of 600,000 documents |
| ❓ | The full suite, the repository-wide lint and the typecheck | the tree at `ed1476aa` | ❓ out of verified scope | the broad gate is the sealer's, once the rounds settle; nothing here ran it, and the `unverified` label it carries is honest |

## Paste-ready fixes

```python
# A file `snapshot` found there and could not read: `restore` leaves it alone,
# because a file it never read is one it cannot put back, and reading it as
# absent removed it (round 2 of #647 C and D, red 10).
UNREAD = object()


def snapshot(paths):
    """{path: its bytes; None where nothing is there; `UNREAD` where a file is
    there and will not read} for each of PATHS."""
    out = {}
    for path in paths:
        if not os.path.lexists(path):
            out[path] = None
            continue
        try:
            with open(path, "rb") as handle:
                out[path] = handle.read()
        except OSError:
            out[path] = UNREAD
    return out
```
```python
    for path, data in before.items():
        if data is UNREAD:
            continue
        if data is None:
```
```python
        if into and before[into] is UNREAD:
            sys.stderr.write(
                f"evidence_check: `--into {args.into}` is there and will not "
                "read, and the run would write over it — nothing was written\n"
            )
            return 2
```
```python
UNREADABLE = pytest.mark.skipif(
    os.name == "nt" or (hasattr(os, "geteuid") and os.geteuid() == 0),
    reason="a mode of 0 stops no read on Windows or as root",
)


@UNREADABLE
def test_a_ledger_that_will_not_read_is_not_removed_by_the_restore(repo):
    """The snapshot read an unreadable ledger as absent, and the restore
    removed it (round 2, red 10)."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")])
    other = cite(
        repo,
        [row("X1", "", "src/orders.py#evict@00000000")],
        where="seal/ledger/1790000000-other.md",
    )
    os.chmod(other, 0)
    try:
        move_serialize(repo)
        code, out = run(repo, "--checked", "2026-09-04")
        assert code == 1 and UNDONE in out, out
        assert os.path.lexists(other), out
    finally:
        if os.path.lexists(other):
            os.chmod(other, 0o644)


@UNREADABLE
def test_an_into_that_will_not_read_is_refused_before_anything_is_written(repo):
    """`reverify_into` wrote its rows over an `--into` it could not read."""
    frag = cite(repo, ["| F9 · kept | `src/orders.py#evict@00000000` | read | 2026-10-01 | |\n"])
    os.chmod(frag, 0)
    try:
        move_serialize(repo)
        code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
        assert code == 2 and "will not read" in out, out
    finally:
        os.chmod(frag, 0o644)
    assert "F9 · kept" in frag.read_text(encoding="utf-8")
```
```python
        # A signal no `except` sees -- SIGTERM from a timeout, SIGHUP from a
        # closed terminal -- killed the run between the re-stamp and the
        # record, and the drift was gone (round 2 of #647 C and D, yellow
        # 11). Raised here as SystemExit, the `except` below puts the ledger
        # back. A SIGKILL or a power cut stays out of reach of any handler.
        def interrupted(signum, _frame):
            raise SystemExit(128 + signum)

        for name in ("SIGTERM", "SIGHUP"):
            if hasattr(signal, name):
                signal.signal(getattr(signal, name), interrupted)
```
```python
        # A run stopped part way -- an exception, an interrupt, SIGTERM or
        # SIGHUP -- is no different: what it wrote is put back, so no
        # re-stamp outlives the record it owed.
```
```markdown
`Pact` rows that will not read, a copy of the checker with no `hooks/`, or a
run stopped part way by an exception, an interrupt, SIGTERM or SIGHUP. A
SIGKILL or a power cut between the re-stamp and the record is out of reach
of any handler and still loses the drift.
```
```markdown
`Pact` rows will not read, or where the run is stopped by an exception, an
interrupt, SIGTERM or SIGHUP (a SIGKILL or a power cut is out of reach) —
```
```python
@pytest.mark.skipif(os.name == "nt", reason="SIGTERM ends a Windows process before any handler")
def test_a_sigterm_between_the_restamp_and_the_record_puts_the_ledger_back(repo, tmp_path):
    """A signal `except` does not see erased the drift unrecorded (round 2,
    yellow 11)."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    wrapper = tmp_path / "killed.py"
    wrapper.write_text(
        "import importlib.util, os, signal, sys\n"
        f"spec = importlib.util.spec_from_file_location('ec', {SCRIPT!r})\n"
        "ec = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(ec)\n"
        "ec.record_pact_changes = lambda *a: os.kill(os.getpid(), signal.SIGTERM)\n"
        f"sys.argv = ['evidence_check.py', '--reverify', '--into', {FRAGMENT!r}, "
        f"'--checked', '2026-09-04', {str(repo)!r}]\n"
        "sys.exit(ec.main())\n",
        encoding="utf-8",
    )
    done = subprocess.run(
        [sys.executable, str(wrapper)], cwd=str(repo), capture_output=True, encoding="utf-8"
    )
    assert done.returncode != 0, done.stdout + done.stderr
    assert ledger.read_text(encoding="utf-8") == "".join(rows)
```
```python
    # The last thing recorded for each coordinate of each clause and row, in
    # the form the record's reader reads a cell in (`\\|` a pipe). A
    # coordinate is recorded again only where what it did now is not what it
    # was last recorded doing: a second identical run adds nothing, and a
    # change re-landed after its revert is recorded (round 2 of #647 C and
    # D, yellow 12).
    last = {}
    for _l, clause, row, code, _c in rows:
        for part in CODE_PART.finditer(code):
            last[(clause, row, part.group("coord"))] = part.group("old", "new")
    date = checked or datetime.date.today().isoformat()
    new = []
    for where, clause, row, parts in owed:
        key = (config.unescaped(clause), config.unescaped(row))
        fresh = [
            (coord, old, nw)
            for coord, old, nw in parts
            if last.get((*key, config.unescaped(coord))) != (old, nw)
        ]
        if not fresh:
            continue
        last.update(((*key, config.unescaped(c)), (o, n)) for c, o, n in fresh)
```
```markdown
A coordinate whose last recorded row for the same clause and ledger row says
the same move or the same `BROKEN` is not recorded again, compared as the
record's reader reads a cell, so a second identical run leaves the record
byte for byte as it was and its content hash with it; a change that comes
back after its revert is recorded, because the record's last word for it was
the revert.
```
```python
def test_a_change_relanded_after_its_revert_is_recorded(repo):
    """A→B, B→A, A→B: the third is a change the pact's repository has not
    seen since the revert (round 2, yellow 12)."""
    a = unit_hash(repo, "src/orders.py", "serialize")
    cite(repo, [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{a}")])
    b = move_serialize(repo)
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    (repo / "src" / "orders.py").write_text(SOURCE, encoding="utf-8")
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-06")
    assert code == 0, out
    rows = record_rows(repo)
    assert len(rows) == 3, rows
    assert rows[-1].endswith(
        f"`src/orders.py#serialize@{a}` → `@{b}` | 2026-09-06 |"
    ), rows
```
```python
    # A row citing a pact is owed under any `Pact notify`; a row citing none
    # is owed under `always`, and a declaration that will not read cannot
    # say it is not `always` (round 2 of #647 C and D, yellow 13).
    blind = declared is None or declared[1] in (None, config.NOTIFY_ALWAYS)
    unread = [e for e in entries if e[3] or blind]
    if refused and unread:
        # Silent before: a row that will not read reads as no pact declared,
        # and the drift went unrecorded at exit 0.
        for where, _row, _parts, anchors in unread:
            why = (
                "cites a pact clause"
                if anchors
                else "moved, and `Pact notify` may be `always`"
            )
            print(
                f"  LEFT  {where}  {why}, and the `Pact` rows will not read: "
                f"{refused[0]} — {NOT_RESTAMPED}; fix the row and run it again"
            )
        return 1
```
```python
@pytest.mark.parametrize(
    "rows",
    [
        (("Pact", PACT_URL), ("Pact notify", "allways")),
        (("Pact", "orders api"), ("Pact notify", "always")),
    ],
    ids=["a Pact notify that will not read", "a Pact row that will not read, always"],
)
def test_under_always_a_declaration_that_will_not_read_leaves_the_row(repo, rows):
    """A row citing no clause is owed under `always`, and a refused
    declaration cannot say `always` was not meant (round 2, yellow 13)."""
    (repo / "seal" / "config.md").write_text(
        config_text(("Mode", "shared"), *rows), encoding="utf-8"
    )
    old = unit_hash(repo, "src/orders.py", "serialize")
    ledger_rows = [row("O1", "", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, ledger_rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1 and "`Pact notify` may be `always`" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(ledger_rows), out
```
```python
            if body is None:
                print(f"  {left_as}  the file could not be read — left")
                pending.append((m.start(), left_as, m.group("hash"), None))
                continue
```
```python
                    print(
                        f"  {left_as}  the anchored statement is gone from "
                        f"{locator} — the check calls this DRIFTED; left"
                    )
                    pending.append((m.start(), left_as, m.group("hash"), None))
                    continue
```
```python
            if new is None:
                left.append((where, f"{coord} — no one place to hash, so not re-read"))
                if moves is not None:
                    moves.append((path, key[1], coord, m.group("hash"), None))
                continue
```
```markdown
coordinate from its recorded hash to its current one, or `BROKEN` where the
re-read leaves it because no one place holds it -- its unit, its file or its
quoted statement gone)
```
```python
@pytest.mark.parametrize("how", ["the anchored statement is gone", "the file is gone"])
def test_a_coordinate_the_reread_leaves_is_recorded(repo, how):
    """Recorded as a major-only BROKEN is; it was left at exit 0 with
    nothing recorded (round 2, yellow 14)."""
    text = (repo / "src" / "orders.py").read_text(encoding="utf-8")
    places, _ = ec.resolve_unit("src/orders.py", "serialize", text)
    a, b = ec.minor_region("src/orders.py", text, places[0], '"return"')[0]
    h = ec.content_hash(ec.gfm_lines(text)[a - 1 : b])
    coord = f'src/orders.py#serialize>"return"@{h}'
    cite(repo, [row("O1", f"`{CLAUSE}`, ", coord)])
    if how == "the file is gone":
        (repo / "src" / "orders.py").unlink()
    else:
        (repo / "src" / "orders.py").write_text(
            SOURCE.replace("    return {'id': order.id}", "    pass"), encoding="utf-8"
        )
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/ledger/{ITEM}.md · O1 | `{coord}` BROKEN | 2026-09-04 |"
    ], out
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    assert len(record_rows(repo)) == 1
```
```python
def a_list_above(lines):
    """True where a list item stands in LINES since the last heading or
    thematic break at the start of a line, so an indented header under it can
    be more of that item: a blank line does not end a list item, and the
    header's indent decides (round 2 of #647 C and D, yellow 15)."""
    seen = False
    for line in lines:
        if blocks.columns(line) >= 4:
            continue
        content = line.lstrip(" ")
        if line[:1] != " " and (ATX_HEADING.match(line) or THEMATIC_BREAK.match(line)):
            seen = False
        elif LIST_ITEM.match(content):
            seen = True
    return seen
```
```python
    head_index = shown[at][0]
    # The line as written, hidden or not: a line `unfenced` hides directly
    # above the header is a line GFM may read the header into -- a fence
    # inside an HTML block of kinds 6-7, or a list item the fence-only
    # reading hid (round 2 of #647 C and D, yellow 15).
    above = text.splitlines()[head_index - 1] if head_index > 0 else ""
    if shown[at][1][:1] == " " and a_list_above([ln for _i, ln in shown[:at]]):
        return [], [
            f"has a `| {name} |` header indented under a list item, which GFM "
            "reads as more of that item where the indent reaches its text — "
            "write the header at the start of its line"
        ]
    if above.strip():
        return [], [
            f"has a `| {name} |` header directly under `{above.strip()}`, "
            "and GFM renders a table under a line only in some of the shapes "
            "that line can take — leave a blank line above the header"
        ]
```
```python
    **A header with a line directly above it is refused**, with the
    blank-line remedy, whether or not `unfenced` hides that line, because
    whether GFM renders a table there depends on block state no reader here
    tracks -- a paragraph, a list item's lazy paragraph, a table above, a
    setext underline, an HTML block, a fence inside one -- and the first
    walker, which mirrored those rules line by line, read tables GFM does
    not render (round 1 of #647 C and D, yellow 5; round 2, yellow 15). So
    is a header indented under a list item, which a blank line does not end
    (`a_list_above`), and a header under an HTML block of kinds 1-5 left
    open above it (`raw_html_open`), which no blank line ends. **What this
    cannot see** is block state none of those three lines carries; round 2's
    generator found none over 600,000 documents.
```
```python
@pytest.mark.parametrize(
    "text",
    [
        "- x\n\n  | Signatory |\n|---|\n| {u} |\n",
        "1) one\n\n   | Signatory |\n|---|\n| {u} |\n",
        "{c} open\n```\n-->\n- note\n| Signatory |\n|---|\n| {u} |\n",
        "<div>\n```\nx\n```\n| Signatory |\n|---|\n| {u} |\n",
    ],
    ids=[
        "a header indented into a bullet item",
        "a header indented into an ordered item",
        "a list item hidden under a comment holding a fence",
        "a fence inside a kind-6 block directly above",
    ],
)
def test_the_shapes_round_2_measured_are_refused(text):
    text = text.format(u="https://example.com/org/a", c="<" + "!--")
    assert oracle.rows_under(text, ("Signatory",)) is None, text
    rows, refusals = config.gfm_table(text, ("Signatory",))
    assert refusals, text


@pytest.mark.parametrize(
    "above",
    ["text\n```\nx\n```\n", "text\n" + "<" + "!-- c -->\n"],
    ids=["a closed fence directly above", "a closed comment directly above"],
)
def test_a_hidden_line_directly_above_the_header_is_refused(above):
    """GFM renders these; the walker refuses with the blank-line remedy,
    because the same hidden line is what hides a header GFM does not render."""
    text = f"# Pact\n\n{above}| Signatory |\n|---|\n| https://example.com/org/a |\n"
    rows, refusals = config.gfm_table(text, ("Signatory",))
    assert refusals and "blank line above the header" in refusals[0], refusals
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_one_table_walker_reads_what_gfm_renders.py`, `tests/test_a_pact_review_takes_a_pact_change.py`, `tests/test_a_signatory_records_a_pact_change.py`, `tests/test_pact_check.py`, `tests/test_a_signatory_declares_its_pact.py`, `tests/test_a_released_row_is_read_again_in_a_fragment.py` at `ed1476aa` | 1028 passed |
| Each fix's code hunk reversed on HEAD, its module run, then restored: `881e6005`, `06264ade`, `ba5ebee3`, `2e550f45`, `26d4ef53`; for `26a3199b` (which does not reverse cleanly) `restore` made a no-op and the `Pact`-row refusal disabled | 1, 7, 2, 6, 5 and 11 cases red, each exactly the fix's own cases |
| `bin/correction-check --range origin/release/v0.18.0...HEAD` | exit 0; 2 merge commits, no marker dropped, no released ledger file changed |
| `bin/evidence-check --strict .` | exit 0; 4272 ok, 0 drifted, 0 broken; records arm 0 refused, 0 drifted |
| `chain_check.py --baseline origin/release/v0.18.0 --root .` | exit 0; names `Broad gate` `not yet` and `Pass` beside `Fixes checked by: nobody`, both expected |
| Writer probes in temporary signatories: an unreadable sibling fragment; an unreadable `--into` under the freeze; SIGTERM at the record step; A→B, B→A, A→B; `always` with a bad `Pact notify` and a bad `Pact` row; a piped label; this repository's three `\|` coordinates over six runs; a statement gone and a file deleted under a minor anchor | 🔴 10, 🟡 11, 🟡 12, 🟡 13, 🟡 14 reproduced as described; the piped label and the six runs record nothing twice |
| `released_drift` timed over this repository's 46 ledger files | 9.83 s, the window 🟡 11 measures |
| Round 2's generator (fenced below), 300,000 documents, seeds 11 and 23, at `ed1476aa` | 70 and 70 tables read where none renders: kind 6–7 fence 49 and 58, indented header under a list item 19 and 12, a hidden line above 2 and 0; oracle checks 0 and 0 |
| The fixes for 🔴 10, 🟡 11, 🟡 12, 🟡 13 and 🟡 14 applied together in the clone, then reverted | every probe inverted; writer module, #743's grid and the probes 251 passed; `test_pact_check.py` and `test_a_pact_review_takes_a_pact_change.py` 109 passed |
| The fix for 🟡 15 applied in the clone, then reverted | generator 0 of 300,000 for each seed; the five pact modules 818 passed, 2 failed (the two ids the fix names) |
| An AST scan of every file I/O call added in the fix range for a missing `encoding=` | none |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — not run here; it is the sealer's, after the rounds settle |

```python
# Round 2's generator: walker against cmark-gfm, independent of the build's
# corpus. Run from a clone with the suite's venv:
#   .venv/bin/python gen.py <clone> <documents> <seed>
import collections, html, importlib.util, os, random, re, sys

CLONE, N, SEED = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sys.path[:0] = [os.path.join(CLONE, "hooks"), os.path.join(CLONE, "tests")]
spec = importlib.util.spec_from_file_location("cfg", os.path.join(CLONE, "hooks", "config.py"))
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)
import cmarkgfm  # noqa: E402
from cmarkgfm.cmark import Options  # noqa: E402
import gfm_table_oracle as build_oracle  # noqa: E402

C = "<" + "!--"
HEADERS = {"sig": ("Signatory",), "rec": ("Clause", "Row", "Code", "Checked"),
           "rev": ("Signatory", "Change", "Verdict")}
BODY = {"sig": ["| https://example.com/o/a |", "| https://example.com/o/b |", "|x|"],
        "rec": ["| c | r | k | 2026-01-01 |", "|c|r|k|2026-01-02|"],
        "rev": ["| s | i@abcdef12 | holds |", "|s|i@abcdef12|amended|"]}
VOCAB = [
    "", "", "", "text", "more text here", "a | b", "x \\| y", "Intro",
    "# Heading", "## Two", "###### six", "#notheading",
    "===", "---", "-", "--", "***", "___", "- - -", "* * *",
    "- item", "* item", "+ item", "1. one", "2. two", "1) one", "3) three", "-", "1.", "*",
    "> quote", ">", "> | Signatory |", ">> deep",
    "    indented", "\tindented tab", "  two spaces", "   three spaces",
    "```", "```python", "~~~", "~~~~", "````",
    C + " c -->", C, "-->", C + " open", "end -->",
    "<pre>", "</pre>", "<script>", "</script>", "<style>", "</style>", "<textarea>", "</textarea>",
    "<?php", "?>", "<!DOCTYPE html>", "<!X", ">", "<![CDATA[", "]]>",
    "<div>", "</div>", "<table>", "</table>", "<p>", "<details>", "<a>", '<a href="x">',
    "<span>", "</a>", "<h1", "<br>", "<b>bold</b>",
    "[ref]: https://example.com", "[^1]: note",
    "| Name |", "|---|", "| x |", "| a | b |", "|---|---|", ":-:", "| --- |",
    "|", "||", "| |", "\\|", "\\\\|", "|\\\\| x |",
    "&#124;", "<https://example.com>", "https://example.com",
]
FENCE_START = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def my_tables(out):
    """[(header, rows)] by regex over cmark's own raw-HTML-omitted output."""
    def cells(s, tag):
        return tuple(html.unescape(re.sub(r"<[^>]*>", "", c)).strip()
                     for c in re.findall(rf"<{tag}[^>]*>(.*?)</{tag}>", s, re.S))
    found = []
    for t in re.finditer(r"<table>(.*?)</table>", out, re.S):
        head = re.search(r"<thead>(.*?)</thead>", t.group(1), re.S)
        tb = re.search(r"<tbody>(.*?)</tbody>", t.group(1), re.S)
        rows = [cells(tr, "td") for tr in re.findall(r"<tr>(.*?)</tr>", tb.group(1), re.S)] if tb else []
        found.append((cells(head.group(1), "th") if head else (), rows))
    return found


def doc(rng):
    kind = rng.choice(list(HEADERS))
    header = HEADERS[kind]
    head_line, delim = "| " + " | ".join(header) + " |", "|" + "---|" * len(header)
    pre = [rng.choice(VOCAB) for _ in range(rng.randint(0, 6))]
    body = [rng.choice(BODY[kind]) if rng.random() < 0.6 else rng.choice(VOCAB)
            for _ in range(rng.randint(0, 4))]
    v = rng.random()
    if v < 0.1:
        head_line = " " * rng.randint(1, 3) + head_line
    elif v < 0.15 and len(header) == 1:
        delim = "| :-- |"
    lines = pre + [head_line, delim] + body
    if rng.random() < 0.2:
        lines += [rng.choice(VOCAB) for _ in range(rng.randint(1, 3))]
    return header, "\n".join(lines) + "\n"


def cause(text, header):
    lines = text.split("\n")
    k = next(i for i, ln in enumerate(lines) if ln.strip() == "| " + " | ".join(header) + " |")
    html_seen = False
    for ln in lines[:k]:
        if config.blocks.columns(ln) < 4 and config.html_start(ln.lstrip(" "))[0] in (6, 7):
            html_seen = True
        if FENCE_START.match(ln) and html_seen:
            return "a fence inside an HTML block of kind 6-7"
    if lines[k].startswith(" ") and any(re.match(r"^ {0,3}([-+*]|\d+[.)])( |$)", ln) for ln in lines[:k]):
        return "an indented header under a list item"
    return "other"


rng, stats, first = random.Random(SEED), collections.Counter(), {}
for _ in range(N):
    header, text = doc(rng)
    safe = cmarkgfm.github_flavored_markdown_to_html(text, options=Options.CMARK_OPT_DEFAULT)
    unsafe = cmarkgfm.github_flavored_markdown_to_html(text, options=Options.CMARK_OPT_UNSAFE)
    if safe.count("<table>\n<thead>") != unsafe.count("<table>\n<thead>"):
        stats["oracle: a table only one render has"] += 1
    mine = next((r for h, r in my_tables(safe) if h == header), None)
    if mine != build_oracle.rows_under(text, header):
        stats["oracle: the build's reading differs from this one"] += 1
    rows, refusals = config.gfm_table(text, header)
    got = [c for _n, c in rows]
    if refusals:
        stats["refused"] += 1
    elif mine is None:
        key = f"DISAGREE, read where none renders ({'rows' if got else 'empty'}): {cause(text, header)}"
        stats[key] += 1
        first.setdefault(key, text)
    elif got != mine:
        stats["DISAGREE, rows differ"] += 1
        first.setdefault("DISAGREE, rows differ", text)
    else:
        stats["agree"] += 1
for k, v in sorted(stats.items()):
    print(f"{v:8d}  {k}")
for k, v in first.items():
    print(f"first of {k}: {v!r}")
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/evidence-check/scripts/evidence_check.py:4728` | round 1's 🔴 1 — fixed |
| round-1 | `skills/evidence-check/scripts/evidence_check.py:3576` | round 1's 🟡 2 — fixed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:823` | round 1's 🟡 3 — fixed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:611` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/config.py:1044` | round 1's 🟡 5 — fixed |
| round-1 | `hooks/config.py:893` | round 1's ⬜ 6 — fixed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:688` | round 1's ⬜ 7 — fixed |
| round-1 | `seal/ledger/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed.md` | round 1's ⬜ 9 — answered |
| round-1 | `skills/evidence-check/scripts/pact_check.py:210` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py:993` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:726` | round 1's 🟢 — confirmed |
| round-1 | `skills/evidence-check/scripts/pact_check.py:116` | round 1's 🟢 — confirmed |
| round-1 | the tree at `31910204` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
