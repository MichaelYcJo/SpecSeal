# 1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row — review round 1

| Field | Value |
|---|---|
| Target SHA | 646b3f07f71354c65c152e6161383593fd18aefd |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 208 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1 and 🟡 2 in `row_cells`, 🟡 3 in `swallowed`, 🟡 4's gate answers, and the blind cases 🟡 5, 🟡 6, 🟡 7 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1, spawned against `646b3f0` with the draft pull request open and nothing
to inherit.

**The prompt stated the bound rather than a round number**, which is the first
time in this repository a spawn prompt has: *after a record whose `Loses a
record or crashes` row reads `no`, at most one later record may close on a fix,
and the record that reads its fixes ends the run whatever it finds.* It said so
because the chain immediately before this one read the cap of five as a budget,
ran three rounds past the bound, and had 37.9 minutes of work reverted when the
broad gate refused its records — issue #207, whose repair is that the record
say this itself.

It carried the orchestrator's own re-execution at `646b3f0` against a fixture
report rather than the build's word, and the build's strongest fact with an
instruction attached: **125 committed records swept for row width, 8 over-wide,
all 8 with the pipe inside a backticked code span**, two of which refuse the
obvious fold-into-the-last-column repair. *Re-run that sweep yourself* — an
aggregate is not a coordinate.

Five axes: every case the diff adds, against what it guards, because the branch
before this one produced nine instances of a case that cannot observe what its
own guard removes; the two readings of a row at their boundary, looking for the
input where they disagree and the wrong one wins; the empty arm, asking whether
a reader can tell an observation from a claim; what an escaped pipe does to
`chain_check` and `evidence_check` downstream; and the four document pins,
asking which of deletion, emptying and renaming each survives.

The second axis is where the 🔴 came from, one text over from where the prompt
pointed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 a `\|` inside an HTML comment inside a cell loses a column of the record; two such comments produce a row `chain_check` refuses | `skills/code-review/scripts/round_record.py:571` | open | executed both sides: base exit 0 with 5 cells, HEAD 4 cells with Grounds gone and no error, and 3 cells with `3 cells, and the Verdict column is number 4`. The orchestrator reproduced a third shape independently — 5 cells at header width with every column shifted and the Location standing in the Verdict cell |
| 2 | 🟡 the fallback drops the code-span reading, so a row with a span pipe and a bare pipe lands the Location in the verdict cell at exactly header width | `skills/code-review/scripts/round_record.py:378` | open | executed; the placement `plan.md` names as its reason for refusing the fold, reached by the fix. The repair is verified as a no-op on all 125 committed records |
| 3 | 🟡 a report that omits the OPTIONAL `## Paste-ready fixes` while a fence quotes it is refused at exit 2, where the base wrote the record | `skills/code-review/scripts/round_record.py:679` | open | executed both sides. Falsifies `seal/ledger.md:1185` F3, whose own Notes name this scenario as the thing the guard must never do, and whose `Checked` cell was moved to 2026-09-07 on this branch without being narrowed the way F1 was |
| 4 | 🟡 three of the four `What a change to a gate must carry` answers are false, and the changelog fragment ships one of them to users | `seal/specs/1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row/changelog.md:41` | open | executed against the base copies of the five changed files: 16 new cases red not 15, six for the fixes section not five, two cases green on both sides and neither docstring says so, and one arm does block more |
| 5 | 🟡 `close`'s `row_cells` change is observed by no case | `skills/code-review/scripts/round_record.py:1757` | open | executed: reverting both sites to `reader.split_row` leaves 111 passed. The two cases added for it exercise other paths, and seven bare-pipe Verdicts rows stand in this repository's committed records today |
| 6 | 🟡 the empty-arm sentence is asserted against itself, and three documents quote it verbatim | `skills/code-review/scripts/round_record.py:157` | open | executed: rewording `NO_PASTE_READY` to `none was needed` leaves 111 passed. Both cases read the constant on both sides of their comparison |
| 7 | 🟡 three of the four document pins pass on presence anywhere, and one assertion's own failure message claims the opposite | `tests/test_the_record_is_generated.py:1589` | open | executed: `agents/warden.md`, `templates/sdd-round.md` and `docs/review-handoff-protocol.md` each mutated green; `skills/code-review/SKILL.md` red |
| 8 | 🟡 a pasted fix carrying `close(` makes `is_closed` true, silencing the pre-merge reminder for a record with live deferred rows | `hooks/review-history-guard.py:72` | open | executed on both readings. Pre-existing in kind — a probes fence could already do it — and the new section makes it every record, in a run whose fixes are fixes to this vocabulary |
| 9 | ⬜ *reads no other prose* is false — the generator reads the two terminal lines from prose | `agents/warden.md:279` | open | read; the same section names those lines four paragraphs later, so what a reviewer takes from the page is unchanged. The branch exists to make that paragraph true |
| 10 | ❓ no record in this repository has ever carried a `\|`, so the rendering the whole #189 arm is about has never been observed | out of verified scope | open | GFM's tables extension specifies `\|` inside a code span rendering as a pipe; the branch's cases assert the parse, never the render. One look at a rendered record settles it — the orchestrator's |

## Paste-ready fixes

```python
# skills/code-review/scripts/round_record.py:275 — signature
def split_cells(line, spans=False, limit=None, comments=False):
```
```python
# skills/code-review/scripts/round_record.py:305 — the scan gains a comment arm.
# `comments` reads a `|` between `<!--` and `-->` as text, for the same reason
# `spans` does inside a backtick run: `table_body` measured this row's width on
# `strip_comments(report)`, where that character is NOT a break, and
# `copied_row` rebuilds it from `raw`, where it is. Two texts disagreeing about
# one character is the asymmetry `NEVER_CLOSED_VERBATIM` already documents for
# fences; here it cost a column. Executed: one such comment came out of `new`
# one cell short with the last column gone, and two produced a row
# `chain_check` refuses — a record the generator wrote and its own checker
# will not read.
    out, buf, i, marker, hidden = [], [], 0, None, False
    while i < len(body):
        ch = body[i]
        if comments and not hidden and body.startswith("<!--", i):
            hidden = True
            buf.append(body[i : i + 4])
            i += 4
            continue
        if hidden:
            if body.startswith("-->", i):
                hidden = False
                buf.append(body[i : i + 3])
                i += 3
                continue
            buf.append(ch)
            i += 1
            continue
        if spans and ch == "`":
```
```python
# skills/code-review/scripts/round_record.py:366-378 — the body of `row_cells`
    if reader.split_row(line) is None:
        return None
    cells = split_cells(line, spans=True, comments=True)
    if len(cells) == width:
        return cells
    # The reader's own answer wherever it fits, so the common row is read by
    # the function every downstream check reads it by and not by a second
    # spelling of it. `comments=True` is what makes it that answer on a RAW
    # report line: this function is handed `raw[i]`, and `table_body` counted
    # the columns on the comment-stripped text.
    plain = split_cells(line, comments=True)
    if len(plain) <= width:
        return plain
    # The cap taken with the code-span reading still on, wherever THAT lands
    # on the width. A row carrying both a `|` inside a code span and a bare one
    # past it is over-wide under either reading alone, so it used to fall to
    # the plain cap — which re-splits the reviewer's code span and shifts every
    # later column left, landing the Location in the verdict cell `chain_check`
    # reads. That is the placement `plan.md` gives as its reason for refusing
    # the fold, reached by the fix instead. An unbalanced backtick run still
    # lands under the width here, so the plain cap below stays its answer.
    spanned = split_cells(line, spans=True, comments=True, limit=max(width - 1, 0))
    if len(spanned) == width:
        return spanned
    return split_cells(line, limit=max(width - 1, 0), comments=True)
```
```python
# skills/code-review/scripts/round_record.py:162 — after READ_HEADINGS
# `PASTE_READY` is the first member whose section is OPTIONAL: `agents/warden.md`
# §Report tells a round that opened nothing needing a fix to leave the heading
# out. The swallow guard's premise — hidden AND absent means swallowed — holds
# only where the report must carry the section, so only these three reach it.
# `seal/ledger.md` F3: what is refused is a report LOSING a section, never a
# fence MENTIONING one, and its own Notes name the case this reopened.
REQUIRED_HEADINGS = tuple(h for h, _ in REPORT_TABLES)  # NAME NOT IN TREE
```
```python
# skills/code-review/scripts/round_record.py:679
    for heading in REQUIRED_HEADINGS:  # NAME NOT IN TREE
        if heading in text and not reader.sections(lines, heading):
            raise Refused(SWALLOWED.format(name=heading))
```
```python
# tests/test_the_fixes_close_the_record.py — append
def test_a_raw_pipe_the_record_already_carries_survives_close(repo):
    """The row `close` re-serialises may carry a BARE `|`: every record
    written before #189 escaped nothing, and a record is a file a person
    edits. `reader.split_row` splits it into a sixth cell, so the grounds stop
    at the pipe and the row outgrows its header. Seven such rows stand in this
    repository's own committed records. The existing pair cannot see this: one
    goes through `fix_table`, the other through an already-escaped pipe both
    readings agree about."""
    declared(repo)
    code, out, _ = generate(repo, report_text=report(verdicts=THREE))
    assert code == 0, out
    path = repo / ROUNDS / "round-1.md"
    grounds = "the augmented assignment reads a |= b"
    text = path.read_text(encoding="utf-8")
    assert "| open | executed |" in text
    path.write_text(
        text.replace("| open | executed |", f"| open | {grounds} |", 1),
        encoding="utf-8",
    )
    a = commit(repo, "round 1")
    write(repo, "mod.py", MOD_CHANGED)
    b = commit(repo, "fix")
    code, out, record = close(
        repo,
        1,
        fix_table(
            f"| 1 | fixed | {b[:7]} |\n",
            "| 2 | answered | the rest is never passed |\n",
            "| 3 | deferred #12 | #12 |\n",
        ),
        f"{a}..{b}",
    )
    assert code in (0, 1), out
    one, _two, _three = verdict_cells(record)
    assert len(one) == 5, record
    assert one[4] == f"fixed at {b[:7]}; {grounds}"
```
```python
# tests/test_the_record_is_generated.py — append beside the empty-arm cases
def test_the_empty_arms_sentence_is_the_generators_constant():
    """One constant, four carriers. The two empty-arm cases read
    `NO_PASTE_READY` out of the module on both sides of their assertion, so
    they hold whatever it says — and three documents quote it word for word.
    `seal/ledger/1788749195-...` R2 calls it a load-bearing wording rather
    than a default string; this is what makes that true."""
    sentence = generator_module().NO_PASTE_READY
    for parts in (
        ("agents", "warden.md"),
        ("templates", "sdd-round.md"),
        ("docs", "review-handoff-protocol.md"),
    ):
        flat = " ".join(read(*parts).split())
        assert sentence in flat, parts
```
```python
# tests/test_the_record_is_generated.py:1589 — the body of
# test_the_reviewer_is_told_where_the_paste_ready_fixes_go
    generator = generator_module()
    heading = generator.PASTE_READY
    # 1. warden.md: inside the fenced block that IS the reviewer's output
    #    contract, not standing anywhere below `## Report` — which is the last
    #    section of the file, so the old slice was its whole tail.
    body = read("agents", "warden.md")
    section = body[body.index("\n## Report\n") :]
    blocks = re.findall(r"\n```[^\n]*\n(.*?\n)```\n", section, re.S)
    assert any(f"\n{heading}\n" in f"\n{block}" for block in blocks), (
        "the heading has to stand in a fenced block of the reviewer's output "
        "contract, not only in the prose around it"
    )
    skill = read("skills", "code-review", "SKILL.md")
    findings = skill[skill.index("\n## Findings format\n") :]
    assert f"`{heading}`" in findings, (
        "the findings format is where a reviewer reads what a paste-ready fix "
        "is; it has to say where the fix goes"
    )
    # 2. sdd-round.md: in the record's own section order, which `build` writes
    #    — a section moved to the end of the template describes a record
    #    nobody gets.
    order = re.findall(r"(?m)^##\s.*$", read("templates", "sdd-round.md"))
    assert order.index(heading) == order.index(generator.VERDICTS) + 1, order
    assert order.index(generator.PROBES) == order.index(heading) + 1, order
    # 3. review-handoff-protocol.md: a row of the field table, which is the
    #    table of what a record carries — not the prose below it.
    proto = read("docs", "review-handoff-protocol.md")
    table = proto[proto.index("\n| Field | Required | Content |\n") :]
    assert f"| {heading.lstrip('# ')} |" in table[: table.index("\n#### ")], table
```
```python
# hooks/review-history-guard.py — beside the other module constants
READER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "skills", "verify", "scripts", "unverified_check.py",
)


def _reader():  # NAME NOT IN TREE
    """The one reader, or None when this copy of the plugin has no `skills/`."""
    import importlib.util

    try:
        spec = importlib.util.spec_from_file_location("specseal_reader", READER)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except (OSError, ImportError):
        return None


def is_closed(records):
    """True when some round record says the rows were drained.

    Read through the shared reader, so a closing WORD inside a fenced block is
    not a closing note. `## Paste-ready fixes` puts the reviewer's code into
    every record, and `closed` is a word this repository's own fixes carry —
    matched on the raw text, one pasted `def close(...)` silences the reminder
    for a record that drained nothing.
    """
    if not records:
        return True  # nothing to close
    reader = _reader()  # NAME NOT IN TREE
    for path in records:
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            return True  # unreadable: say nothing rather than nag wrongly
        if reader is not None:
            text = "\n".join(reader.readable(text))
        if CLOSED_RE.search(text):
            return True
    return False
```

## Executed probes

| What was run | Result |
|---|---|
| the over-wide sweep re-run independently over every committed round record | 125 records, 8 over-wide rows, all 8 with the pipe inside a code span; 7 recover their column under the span reading, the 8th has unbalanced backticks. The probes row's pipe is in column 0 and round 9's is in Finding — the branch's two counterexamples confirmed |
| `./bin/evidence-check .` unscoped at `646b3f0` | exit 0 — 735 ok, 0 drifted, 0 broken, 0 external, 0 old-format |
| `./bin/test tests/test_the_record_is_generated.py tests/test_the_fixes_close_the_record.py -q` | 111 passed |
| the same two modules with the five changed files at `origin/release/v0.9.0` | 20 failed, 91 passed — 16 new cases plus 4 re-parametrised runs of a pre-existing case |
| `./bin/test` on `test_docs_line_wrap`, `test_review_axes`, `test_the_rules_have_one_owner`, `test_a_moved_rule_leaves_its_definition` | 168 passed |
| `./bin/test` on `test_a_record_precedes_the_fixes_it_commissions`, `test_the_last_rounds_fixes_are_checked`, `test_chain_check_at_the_pull_request`, `test_the_record_is_held_to_the_floor_and_the_depth` | 237 passed |
| `new` end to end on a scratch repository, base and HEAD, for a cell carrying one HTML comment and two | finding 1, both arms |
| `new` end to end, base and HEAD, for a report omitting the paste-ready heading while a probes fence quotes it | finding 3, exit 0 against exit 2 |
| mutations: escape no-op, span reading dropped, cap dropped, sketches dropped, `NO_PASTE_READY` reworded, `close` reverted, warden.md fence block emptied | 9 red, 2 red, 4 red, 4 red, green, green, green |
| the combined fix for findings 1 and 2, applied in a clone | 111 passed, no-op on all 125 committed records, `split_cells(line) == reader.split_row(line)` holds, all six shapes correct |
| the swallow-guard fix with the parametrisation narrowed | 110 passed, and the refused report writes its record with the quoted heading still carried inside the probes fence |
| `is_closed` on a record with a live Deferred row, with and without `def close(args):` in the paste-ready block | True, then False |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
