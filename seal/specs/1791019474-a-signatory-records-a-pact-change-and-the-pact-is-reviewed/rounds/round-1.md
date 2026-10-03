# 1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed — review round 1

| Field | Value |
|---|---|
| Target SHA | 319102043938f207fcf7ac6ae585b8cf0f5cc56d |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 749 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1 (an owed pact change that cannot be recorded is lost, the ledger re-stamped first), 🟡 2 (a second run records again), 🟡 3 (a true historical `amended` refused at exit 2), 🟡 4 (three one-mark typos silent), 🟡 5 (the walker reads tables cmark-gfm does not render) |
| Loses a record or crashes | yes — 🔴 1: a pact change owed by a drifted row citing a clause is never recorded on five paths, one of them at exit 0, and the re-stamp removes the drift that would record it later |

- [ ] Pass

## What this round was asked

Round 1 targets `31910204`, the build `2b1dcb1f..` with a merge of #742. It was asked to check #647 C and D and #735's deferrals against the frame, then quality. Named for close checking:
- the table walker against cmark-gfm with an independent generator;
- whether a clause-citing DRIFTED or BROKEN row can go unrecorded or be recorded twice, or land in the wrong work item;
- the pact review's content-hash taking, `amended` refusal and the status words;
- 🟡 19's grammar;
- Windows paths and encoding;
- the ledger re-reads and corrections.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | An owed pact change that cannot be recorded is lost: the ledger is re-stamped before the record is attempted, so the four `LEFT` paths (no work item, vendored copy, record unreadable, record unparseable) and the silent one (a `Pact` row or config that will not read, exit 0) erase the drift, and the printed remedy finds nothing to record | `skills/evidence-check/scripts/evidence_check.py:4728` | open | executed: no-work-item then `--into` records nothing (exit 0); vendored then plugin the same; empty record; unparseable `Pact` row and non-UTF-8 config exit 0 with no record. Fix run in the clone: left-then-into records one row |
| 🟡 2 | A second run records a change again: a BROKEN coordinate beside a moved one, and any coordinate or label holding `\|`, on every run, each changing the hash a pact review took | `skills/evidence-check/scripts/evidence_check.py:3576` | open | executed: two rows after two runs; three rows after three runs with `\|`. Fix run in the clone: one row |
| 🟡 3 | An `amended` pact review, true at the hash it took, is refused at exit 2 once the record grows, and stays refused after a new `holds` review takes the grown record | `skills/evidence-check/scripts/pact_check.py:823` | open | executed with the build's fixture: exit 2. Fix run in the clone: no refusal |
| 🟡 4 | `.`, `-` or `_` in place of the `/` (and before it) passes silently, inside the grammar's own "one mark" | `skills/evidence-check/scripts/pact_check.py:611` | open | executed over 21 shapes: the four of round 3 refused, these silent. Fix run in the clone: exit 2 |
| 🟡 5 | The walker reads tables cmark-gfm does not render: a line above the header `absorbs_a_header` misjudges, and an HTML block of kinds 1–5 left open above a blank line | `hooks/config.py:1044` | open | executed: 300,000 random documents, 315 disagreements; with the fix, 15, all a fence inside an HTML block |
| ⬜ 6 | A cell is split at a pipe after two backslashes, where cmark-gfm does not split; a three-cell row reads as four, silently | `hooks/config.py:893` | open | executed against cmarkgfm |
| ⬜ 7 | A pact review row naming a dropped signatory is refused at exit 2 for good, and no document says so | `skills/evidence-check/scripts/pact_check.py:688` | open | read |
| ⬜ 8 | A pact review takes a whole record: a mixed record can only be taken as `holds`, and rows that are not this pact's re-open its taken rows | `skills/evidence-check/scripts/pact_check.py:823` | open | read; the code follows `spec.md` item 9 |
| ⬜ 9 | `Re-read · P1-1` says the claim holds while *"the suite's test-only parser"* is now one of two | `seal/ledger/1791019474-a-signatory-records-a-pact-change-and-the-pact-is-reviewed.md` | open | read; a correction to the run's paperwork, not counted in `Needs a fix` |
| 🟢 | Round 3 of #735's 🟡 19 four shapes are refused at exit 2 and round 2's mentions stay exit 0 | `skills/evidence-check/scripts/pact_check.py:210` | confirmed | executed |
| 🟢 | Tab before a row, header or delimiter: the walker follows cmark-gfm 2025.10.22; a row of another width is refused loud, the recorded divergence | `hooks/config.py:993` | confirmed | executed against cmarkgfm |
| 🟢 | `NOT TAKEN` exit 1, `NOTED` exit 0, `REFUSED` and `UNREADABLE` exit 2; `amended` over an unmoved clause refused; a grown record reads `NOT TAKEN` again with both hashes | `skills/evidence-check/scripts/pact_check.py:726` | confirmed | executed: probes and the module |
| 🟢 | Every added file read and write names its encoding; every printed path goes through `shown` or `built_name`; `cmarkgfm` installs from a wheel on CI's three legs | `skills/evidence-check/scripts/pact_check.py:116` | confirmed | executed (AST scan); read (CI run at `31910204`, three pytest legs green) |
| ❓ | The full suite, the repository-wide lint and the typecheck | the tree at `31910204` | ❓ out of verified scope | the broad gate is the sealer's, once the rounds settle; the smith handed it over labelled `unverified`, and that label is honest |

## Paste-ready fixes

```python
def snapshot(paths):
    """{path: its bytes, or None where it is absent} for each of PATHS."""
    out = {}
    for path in paths:
        try:
            with open(path, "rb") as handle:
                out[path] = handle.read()
        except OSError:
            out[path] = None
    return out


def restore(before):
    """Put each file BEFORE holds back as it was, byte for byte, through a
    rename beside the real file as `write_atomic` does; remove one that was
    absent and now exists."""
    for path, data in before.items():
        if data is None:
            if os.path.isfile(path):
                os.remove(path)
            continue
        target = os.path.realpath(path)
        fd, tmp = tempfile.mkstemp(
            dir=os.path.dirname(target) or ".", prefix=os.path.basename(target) + "."
        )
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
        try:
            os.chmod(tmp, stat.S_IMODE(os.stat(target).st_mode))
        except OSError:
            pass
        os.replace(tmp, target)
```
```python
        # What the re-read moved, for the pact changes it owes (#647, C).
        moves = []
        # Every file this run may write, as it stands: put back where a pact
        # change is owed and cannot be recorded, because the re-stamp is what
        # clears the drift, and a re-stamp without its record loses the
        # trigger for good -- the next run finds nothing moved.
        before = snapshot(ledgers + ([into] if into else []))
        if into is None and cutoff is None:
            ...
            recorded = record_pact_changes(moves, root, into, args.checked)
            if recorded:
                restore(before)
            return max(code, 1 if owed else 0, recorded)
        ...
        recorded = record_pact_changes(moves, root, into, args.checked)
        if recorded:
            restore(before)
        return max(code, written, recorded)
```
```python
    declared = config.declared_pacts(seal_home(root))
    refused = (
        ["seal/config.md could not be read"] if declared is None else declared[2]
    )
    if refused and any(e[3] for e in entries):
        for where, _row, _parts, _anchors in (e for e in entries if e[3]):
            print(
                f"  LEFT  {where}  cites a pact clause, and the `Pact` rows will "
                f"not read: {refused[0]} — no pact change was recorded and "
                "nothing was re-stamped; fix the row and run it again"
            )
        return 1
    declared = declared or ([], None, [])
    pacts, notify = declared[0], declared[1] or config.NOTIFY_DEFAULT
```
```python
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
```
```python
def test_a_change_left_is_recorded_by_the_remedy_it_names(repo):
    """The run that cannot name a work item re-stamps nothing, so the drift
    is still there for the run its LEFT line names (round 1, red 1)."""
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    new = move_serialize(repo)
    code, out = run(repo, "--checked", "2026-09-04")
    assert code == 1 and "nothing was re-stamped" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 0, out
    assert record_rows(repo) == [
        f"| {CLAUSE} | seal/ledger/{ITEM}.md · O1 | `src/orders.py#serialize@{old}` "
        f"→ `@{new}` | 2026-09-04 |"
    ], out


@pytest.mark.parametrize(
    "config_bytes",
    [
        b"| Item | Value |\n|---|---|\n| Pact | orders api |\n",
        b"| Item | Value |\n|---|---|\n| Pact | git@example.com:org/orders-api.git |\n"
        b"| Note | caf\xe9 |\n",
    ],
    ids=["a Pact row that will not parse", "a config that is not UTF-8"],
)
def test_a_pact_row_that_will_not_read_leaves_the_row(repo, config_bytes):
    (repo / "seal" / "config.md").write_bytes(config_bytes)
    old = unit_hash(repo, "src/orders.py", "serialize")
    rows = [row("O1", f"`{CLAUSE}`, ", f"src/orders.py#serialize@{old}")]
    ledger = cite(repo, rows)
    move_serialize(repo)
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    assert code == 1 and "the `Pact` rows will not read" in out, out
    assert ledger.read_text(encoding="utf-8") == "".join(rows), out
```
```python
# One coordinate of a record's `Code` cell, as `record_pact_changes` writes
# it: moved to a new hash, or BROKEN.
CODE_PART = re.compile(
    r"`(?P<coord>[^`]*)@(?P<old>[0-9a-f]{6,12})`"
    r"(?: → `@(?P<new>[0-9a-f]{6,12})`| BROKEN)"
)
```
```python
        parts = list(dict.fromkeys(coords))
        where = f"{built_name(ledger, root)}:{number}"
        row = f"{built_name(ledger, root)} · {label or number}".replace("|", "\\|")
        entries.append((where, row, parts, list(PACT_ANCHOR_RE.finditer(line))))
```
```python
    # Held per coordinate and compared as the reader reads a cell (`\|` a
    # pipe), so a row is not recorded again because one of its coordinates
    # was recorded with another, or because its text holds an escaped pipe.
    held = {
        (clause, row, *part.group("coord", "old", "new"))
        for _l, clause, row, code, _c in rows
        for part in CODE_PART.finditer(code)
    }
    date = checked or datetime.date.today().isoformat()
    new = []
    for where, clause, row, parts in owed:
        key = (config.unescaped(clause), config.unescaped(row))
        fresh = [
            (coord, old, nw)
            for coord, old, nw in parts
            if (*key, config.unescaped(coord), old, nw) not in held
        ]
        if not fresh:
            continue
        held.update((*key, config.unescaped(c), o, n) for c, o, n in fresh)
        code = ", ".join(
            f"`{coord}@{old}` → `@{nw}`" if nw else f"`{coord}@{old}` BROKEN"
            for coord, old, nw in fresh
        )
        new.append((where, f"| {clause} | {row} | {code} | {date} |"))
```
```python
def test_a_broken_coordinate_beside_a_moved_one_is_recorded_once(repo):
    s = unit_hash(repo, "src/orders.py", "serialize")
    e = unit_hash(repo, "src/orders.py", "evict")
    cite(repo, [
        f"| O1 · x | `{CLAUSE}`, `src/orders.py#serialize@{s}`, "
        f"`src/orders.py#evict@{e}` | read | 2026-10-01 | |\n"
    ])
    src = SOURCE.replace("'id': order.id", "'id': order.id, 'tax': 0")
    (repo / "src" / "orders.py").write_text(
        src.split("\n\n\ndef evict")[0] + "\n", encoding="utf-8"
    )
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    first = (repo / RECORD).read_text(encoding="utf-8")
    code, out = run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    assert (repo / RECORD).read_text(encoding="utf-8") == first, out


def test_a_coordinate_holding_an_escaped_pipe_is_recorded_once(repo):
    doc = repo / "docs" / "x.md"
    doc.parent.mkdir()
    doc.write_text("# T\n\n## A | B\n\ntext one\n", encoding="utf-8")
    h = unit_hash(repo, "docs/x.md", '"## A \\| B"')
    cite(repo, [
        f"| O1 \\| x · y | `{CLAUSE}`, `docs/x.md#\"## A \\| B\"@{h}` "
        "| read | 2026-10-01 | |\n"
    ])
    doc.write_text("# T\n", encoding="utf-8")
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-04")
    run(repo, "--into", FRAGMENT, "--checked", "2026-09-05")
    assert len(record_rows(repo)) == 1
```
```python
        for review in reviewed:
            # Judged against the record it takes, and only that one: a review
            # at an older hash took rows this record has since added to, and
            # re-judging its verdict against them refuses one that was true.
            if review[5] != config.VERDICT_AMENDED or review[4] != digest:
                continue
```
```python
def test_an_amended_review_at_an_older_hash_is_not_judged_again(world):
    """An `amended` that was true at the hash it took stays true after the
    record grows with a row citing the amended clause (round 1, yellow 3)."""
    _anchor, first = record(world, cites=V1)
    _anchor, now = record(world, cites=V2, label="O2", step=2)
    review(
        world,
        (SIGNATORY_URL, f"{ITEM}@{first}", "amended"),
        (SIGNATORY_URL, f"{ITEM}@{now}", "holds"),
    )
    code, out = run(world)
    assert "REFUSED" not in out, out
    assert "2 pact changes read, 2 taken" in out, out
```
```python
def near_miss(said, name):
    """True where SAID is NAME and one more mark the name class holds -- a
    `.`, `-` or `_` -- standing where an anchor's `/` went missing, as in
    `pact:orders-api."## A"@1a2b3c4d`: the name pattern takes the mark
    in, so without this the token names another pact and nobody reads it."""
    said = said.lower()
    return len(said) == len(name) + 1 and said.startswith(name) and said[-1] in "._-"
```
```python
            graded = [
                m.span()
                for m in checker.PACT_ANCHOR_RE.finditer(view)
                if not near_miss(m.group("name"), name)
            ]
            for near in PACT_MENTION_RE.finditer(view):
                inside = any(s <= near.start() < e for s, e in graded)
                said = near.group("name")
                if not (said.lower() == name or near_miss(said, name)) or inside:
                    continue
```
```python
@pytest.mark.parametrize(
    "shape",
    [
        "pact:orders-api.{loc}@{h}",
        "pact:orders-api-{loc}@{h}",
        "pact:orders-api_{loc}@{h}",
        "pact:orders-api.@{h}",
        "pact:orders-api-/{loc}@{h}",
    ],
    ids=["a dot", "a hyphen", "an underscore", "a dot, no heading path", "a mark before the slash"],
)
def test_a_mark_the_name_holds_is_not_a_second_name(world, shape):
    """`.`, `-` and `_` are marks the grammar's "one mark" covers and the
    name pattern also takes in (round 1, yellow 4)."""
    anchor = shape.format(loc=LOCATOR, h=clause(V2))
    write(world["web"], "seal/ledger/1790000000-x.md", ledger_row(anchor))
    code, out = run(world)
    assert code == 2, out
    assert "does not parse" in out, out
```
```python
def raw_html_open(lines):
    """True where an HTML block of CommonMark 4.6's kinds 1-5 -- the kinds no
    blank line ends -- is still open after LINES, so everything under it is
    the block's raw text and GFM renders no table there."""
    end = None
    for line in lines:
        if end is not None:
            if end.search(line):
                end = None
            continue
        if blocks.columns(line) >= 4:
            continue
        content = line.lstrip(" ")
        number, closer = html_start(content)
        if number is not None and number <= 5 and not closer.search(content, 1):
            end = closer
    return end is not None
```
```python
    above = shown[at - 1] if at > 0 else None
    if above is not None and above[0] == head_index - 1 and above[1].strip():
        return [], [
            f"has a `| {name} |` header directly under `{above[1].strip()}`, "
            "and GFM renders a table under a line only in some of the shapes "
            "that line can take — leave a blank line above the header"
        ]
    if raw_html_open([line for _i, line in shown[:at]]):
        return [], [
            f"has a `| {name} |` header inside an HTML block opened above it "
            "and never closed, so GFM renders no table there — close the block"
        ]
```
```python
@pytest.mark.parametrize("which", sorted(HEADERS))
def test_a_line_directly_above_the_header_is_refused(which):
    """Whether cmark-gfm renders a table under a line depends on the block
    state above it, which the walker does not track, so any non-blank line
    directly above a header is refused with the blank-line remedy
    (round 1, yellow 5)."""
    header = HEADERS[which]
    for kind, lines in KINDS.items():
        if not any(line.strip() for line in lines):
            continue
        text = document(header, lines, "before the header", "")
        rows, refusals = config.gfm_table(text, header)
        assert refusals and "blank line above the header" in refusals[0], kind


def test_the_shapes_round_1_measured_are_refused():
    u = "https://example.com/org/a"
    opener = "<" + "!-- old list, being retired"
    for text in (
        f"| Name |\n|---|\n| x |\n| Signatory |\n|---|\n| {u} |\n",
        f"Intro\n-\n2. second\n| Signatory |\n|---|\n| {u} |\n",
        f"1) one\n<a>\n___\n>\n| Signatory |\n|---|\n| {u} |\n",
        f"# Pact\n\n{opener}\n\n| Signatory |\n|---|\n| {u} |\n",
        f"<pre>\nexample\n\n| Signatory |\n|---|\n| {u} |\n",
    ):
        assert oracle.rows_under(text, ("Signatory",)) is None, text
        rows, refusals = config.gfm_table(text, ("Signatory",))
        assert refusals, text
```
```python
        "has a `| Signatory |` header directly under `- a note`, and GFM "
        "renders a table under a line only in some of the shapes that line "
        "can take — leave a blank line above the header",
```
```python
# A pipe after an even run of backslashes: `CELL` splits there and cmark-gfm
# does not (its cell scanner reads `\|` as an escaped pipe wherever it stands).
EVEN_ESCAPED_PIPE = re.compile(r"(?<!\\)(?:\\\\)+\|")


def table_cells(line):
    """..."""
    match = TABLE_ROW.match(line)
    if not match or EVEN_ESCAPED_PIPE.search(line):
        return None
    ...
```
```markdown
A pact review row names a signatory by the URL the pact lists, so taking a
signatory out of the `Signatory` table refuses every pact review row that
names it, at exit 2: take those rows out with the signatory, in the same
change.
```
```markdown
A pact review takes a whole record, one verdict for every row in it. A
record citing a clause the pact amended beside one it kept is taken as
`holds`, the amendment written in the pact itself; and a row that is not
this pact's -- a `—` row, or one citing another pact -- still changes the
record's hash, so a record this pact took reads `NOT TAKEN` again when one
is added.
```
```markdown
**Corrected 2026-10-03 by work item 1791019474:** the claim says *"the suite's test-only parser"*; since W2 `cmarkgfm` is a second test-only package beside it, pinned in `CMARKGFM`. Every operative part of the claim -- the pin, both build strategies, the adopted-environment step, the failure sentence, CI's and `CONTRIBUTING.md`'s strings -- still holds for markdown-it-py.
```

## Executed probes

| What was run | Result |
|---|---|
| The five pact modules (`test_one_table_walker_reads_what_gfm_renders`, `test_a_pact_review_takes_a_pact_change`, `test_a_signatory_records_a_pact_change`, `test_pact_check`, `test_a_signatory_declares_its_pact`) at `31910204` | 777 passed |
| An independent random-document generator, walker against `cmarkgfm`, 20,000 then 300,000 documents | 219 then 315 tables read that cmark-gfm does not render (two mechanisms, 🟡 5); body side: only ⬜ 6 |
| Targeted walker shapes through `gfm_table` and `pact_signatories` | unclosed comment and `<pre>` above, table above, setext `-` read with no refusal; a pipe after two backslashes splits; tab, width, NBSP refused |
| Writer sequences in temporary signatories (no work item then `--into`; vendored then plugin; BROKEN beside a move, twice; `\|` coordinate and label, three runs; unparseable `Pact` row; non-UTF-8 config; empty record) | 🔴 1 and 🟡 2 reproduced as described |
| `amended` at v1, record grown with a v2 row, a new `holds` review | exit 2, 🟡 3 |
| 21 anchor shapes through `PACT_MENTION_RE` and `PACT_ANCHOR_RE` as `pact-check` filters them | 🟡 4 table |
| The paste-ready fixes for 🔴 1, 🟡 2, 🟡 3, 🟡 4 and 🟡 5 applied together in the clone, the probes and the five modules re-run, then the clone reverted | probes inverted (each defect gone); 771 passed, 6 failed — exactly the six cases that pin the old behaviour, each named in the fixes below |
| An AST scan of every added line for file I/O without `encoding=` | none |
| The broad gate: the full suite, the repository-wide lint, the typecheck | not yet — not run here; it is the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A fence `unfenced` hides that cmark-gfm reads inside an HTML block (15 documents of 300,000 after 🟡 5's fix) | 🟡 5's docstring sentence names it as a limit; `unfenced` is shared with `config_rows` and older than this work item | the orchestrator, who decides whether it earns an issue |
