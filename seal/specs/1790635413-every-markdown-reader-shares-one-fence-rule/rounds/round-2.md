# 1790635413-every-markdown-reader-shares-one-fence-rule — review round 2

| Field | Value |
|---|---|
| Target SHA | 628e37ef520831b0200191af8a215fb85525ee98 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #663 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `c7338c43a149c39c71d954aad76a72435759f658..1729cf0f79ae3377600f3953fb801f0b3bac9dad`, 8 commits |
| Contract changes | commented → commented_row_at |
| New units | BACKTICKS (depth 1); comment_after (depth 1); walk (depth 1); hidden (depth 1); test_a_row_inside_a_closed_comment_excuses_nothing (depth 1); test_a_comment_opener_quoted_in_a_code_span_hides_no_rider (depth 1); test_a_comment_hides_no_table_and_answers_for_none (depth 1); test_delimiters_quoted_in_code_spans_hide_nothing (depth 1); test_a_fence_line_inside_a_comment_hides_no_table (depth 1) |
| Needs a fix | yes — 🟡 1 (the rider check loses a rider after a comment opener quoted in a code span), 🟡 2 (the routing reader misses a declaration under a comment holding a fence line, and reads a commented-out row as the answer), 🟡 3 (a commented-out exemption excuses a survivor) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2, two jobs. Verifying: round 1's fixes, `1d3eb8a5..a06f23b2`. Finding: phase 8 (#658, added at the owner's request) and phase 9 (round 1's two deferred yellows), reviewed by nobody before, at HEAD `628e37ef`. The routing reader on the commit gate's path, and a release-time refusal that could fire on a fragment that is fine, were named as where a defect would leave the root.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The rider check's comment scan reads a comment opener quoted in a code span as an opener, so a rider quoted in a fence below is read and the real rider after it is lost | `.github/scripts/rider_check.py:240` | **fixed** `17aaf200` | fixed at 17aaf200 — `a7581653`: a comment delimiter inside a code span that closes on its line is text to the rider check; Executed: HEAD returns the quoted block (6, 7) and misses the real one at (12, 13), which `68bcb224` reads. None in today's tree. Inside a unit round 1's fixes rewrote |
| 🟡 2 | The routing reader opens a fence on a line inside an HTML comment, so a declaration with such a note above its table is now none; and a row parked in a closed comment below the table still answers for it | `hooks/routing.py:118` | **fixed** `6576a83f` | fixed at 6576a83f — `a7581653`: `hooks/routing.py#hidden` decides comments before fences and reads code spans, held with the config reader to one parity oracle built from shared functions. The round's ❓ on `hooks/config.py#fence_map` was answered into this fix by the orchestrator: `config.py` has one walk, `walk`, on the same rule, which reverses round 1's 🟡 3 reading (a delimiter quoted in a code span no longer hides a table); the three sentences and the pin case say so; Executed: the base parses the first shape and HEAD returns None; the second reads straight to the PR. With the fix both read the chain and 0 of 25 declarations differ |
| 🟡 3 | The exemption reader takes a row inside a closed HTML comment as an exemption, so a withdrawn row excuses a survivor | `skills/code-review/scripts/survivor_check.py:1774` | **fixed** `83a951a1` | fixed at 83a951a1 — `read_exemptions` reads through `readable`, so a commented-out exemption excuses nothing; Executed: the commented row is read. With `readable` it is not, and 0 of 15 files differ |
| 🟢 | round 1's finding 1 is closed — the gather refuses a fragment that leaves a fence or a comment open, before any write | `.github/scripts/gather_changelog.py#leaves_open` | confirmed | Built in phase 9. Executed: the cases red at `a06f23b2`, green at HEAD, the dry run over this tree 0 |
| 🟢 | round 1's finding 2 is closed — the fold refuses the same, before any write | `.github/scripts/fold_ledger.py#leaves_open` | confirmed | Built in phase 9. Executed: the cases red at `a06f23b2`, green at HEAD, the dry run over this tree 0 |
| 🟢 | round 1's finding 3 is closed — the shipped sentences state the code-span shape and a case pins them | `hooks/config.py#commented` | confirmed | Executed: the module is green with the pin case; read: the three sentences and the changelog fragment |
| 🟢 | round 1's finding 4 is closed for its shape — a fence line inside a rider's body hides no rider | `.github/scripts/rider_check.py#fenced_lines` | confirmed | Executed: the case fails with `68bcb224`'s script and passes at HEAD. 🟡 1 is the new instance in the same rewrite |
| 🟢 | round 1's cleanup 5 is closed — the fence walk runs once per call | `hooks/config.py#table_lines` | confirmed | Read. The other caller walks for itself, as before |
| 🟢 | Phase 8 changes no committed declaration or exemption file | `seal/specs/*/routing.md`, `seal/specs/*/survivors.md` | confirmed | Executed: 25 of 25, 15 of 15 |
| ❓ | `hooks/config.py#fence_map` also opens a fence on a line inside an HTML comment, so a config table below such a note is hidden. It did at `551c7967` too | `hooks/config.py#fence_map` | ❓ out of verified scope | Executed: `config_rows` returns nothing at the base and at HEAD. Not this round's diff and not a regression. It is the class member of 🟡 2 in a reader phase 6 ratified against its oracle. The orchestrating session answers whether it joins 🟡 2's fix in this branch or goes to its own issue |
| ❓ | The ledger fragment's rows, and the re-read notes phases 8 and 9 wrote into `seal/releases/*.md`, were not run through `evidence-check` | `seal/ledger/1790635413-every-markdown-reader-shares-one-fence-rule.md` | ❓ out of verified scope | A plugin check the broad gate runs. The sealer answers it |
| ❓ | The new cases on the Windows and Linux legs | `tests/test_routing_is_recorded.py` | ❓ out of verified scope | Only macOS ran here. CI's test matrix at the pull request answers it |

## Paste-ready fixes

```python
        pos = 0
        while True:
            if comment:
                at = line.find(_reader.CLOSER, pos)
                if at == -1:
                    break
                pos, comment = at + len(_reader.CLOSER), False
                continue
            at = line.find(_reader.OPENER, pos)
            if at == -1:
                break
            run = _reader.BACKTICKS.search(line, pos, at)
            if run is not None:
                width = run.end() - run.start()
                closer = next(
                    (
                        m
                        for m in _reader.BACKTICKS.finditer(line, run.end())
                        if m.end() - m.start() == width
                    ),
                    None,
                )
                pos = run.end() if closer is None else closer.end()
                continue
            pos, comment = at + len(_reader.OPENER), True
    return fenced
```
```text
    A comment delimiter inside a code span that closes on its own line is
    text, as `_liveness` reads it: prose quoting the opener in backticks
    opened a "comment" that made the next fenced example no fence, read the
    rider quoted in it, and turned its closing fence line into an opener
    that hid every rider below (#584 round 2, finding 1).
```
```python
def test_a_comment_opener_quoted_in_a_code_span_hides_no_rider():
    """#584 round 2, finding 1. `fenced_lines` read a comment opener inside a
    code span as an opener, so the fence below it was not a fence, the rider
    quoted in it was read, and its closing delimiter opened a fence that
    swallowed the real rider below."""
    opener = "<" + "!--"
    text = (
        "# doc\n\nA rider opens with `" + opener + "` and a marker.\n\n"
        f"```markdown\n{HTML_MARK} quoted\nVerified 2026-01-01 against q@abcdef12. -->\n```\n\n"
        f"prose\n\n{HTML_MARK} real\nVerified 2026-01-01 against r@abcdef12. -->\n"
    )
    assert riders.comment_blocks(text.splitlines(), "doc.md") == [(12, 13)]
```
```python
    An unclosed block runs to the end because everything here fails toward
    *no declaration*: the rows it swallows are not an answer, and the gate goes
    back to asking.

    **A delimiter line opens a fence only where it begins outside every HTML
    comment** -- inside a comment nothing is markdown, as
    `unverified_check.py#_liveness` and `.github/scripts/rider_check.py#fenced_lines`
    read it -- so a ``` line in a note above the table hides no table (#584
    round 2, finding 2). `hidden` is the walk; this is its fence half, and on
    a file with no comment it is the shared rule's answer."""
    return hidden(lines)[0]


COMMENT_OPENER, COMMENT_CLOSER = "<" + "!--", "-->"
BACKTICKS = re.compile(r"`+")


def comment_after(line, comment):
    """Whether LINE ends inside an HTML comment, given whether it began in
    one. A comment delimiter inside a code span that closes on its own line
    is text, so prose quoting the opener opens nothing."""
    pos = 0
    while True:
        if comment:
            at = line.find(COMMENT_CLOSER, pos)
            if at == -1:
                return True
            pos, comment = at + len(COMMENT_CLOSER), False
            continue
        at = line.find(COMMENT_OPENER, pos)
        if at == -1:
            return False
        run = BACKTICKS.search(line, pos, at)
        if run is not None:
            width = run.end() - run.start()
            closer = next(
                (
                    m
                    for m in BACKTICKS.finditer(line, run.end())
                    if m.end() - m.start() == width
                ),
                None,
            )
            pos = run.end() if closer is None else closer.end()
            continue
        pos, comment = at + len(COMMENT_OPENER), True


def hidden(lines):
    """(fenced, commented): the indices of LINES inside a fenced block, and
    those that begin inside an HTML comment that closes (#584 round 2).

    A commented-out row is not an answer, and `parse` keeps the LAST row of a
    label, so one parked below the table answered for it. A comment that
    never closes hides nothing, as `hooks/config.py#commented` has it."""
    fenced_at, commented, run_of, opener, comment = set(), set(), [], None, False
    for index, raw in enumerate(lines):
        line = raw.rstrip("\r\n")
        found = FENCE.match(line)
        run = found.group("run") if found else ""
        info = found.group("info") if found else ""
        if opener is not None:
            fenced_at.add(index)
            if run[:1] == opener[0] and len(run) >= opener[1] and not info.strip():
                opener = None
            continue
        if comment:
            run_of.append(index)
        elif run and not (run[0] == "`" and "`" in info):
            opener = (run[0], len(run))
            fenced_at.add(index)
            continue
        comment = comment_after(line, comment)
        if not comment and run_of:
            commented.update(run_of)
            run_of = []
    return fenced_at, commented
```
```python
    skipped = set().union(*hidden(lines))
    for index, line in enumerate(lines):
        if index in skipped:
```
```text
    A row inside an HTML comment that closes is a withdrawn answer on the
    same terms. `hidden` is the rule.
```
```text
with a comment half that opens no fence inside a comment and hides a line
inside a comment that closes, held on comment-free shapes by
```
```python
def test_a_comment_hides_no_table_and_answers_for_none():
    """#584 round 2, finding 2. A fence line inside an HTML comment above the
    table opened a fence that hid the whole declaration, and a row parked in
    a closed comment below the table answered for it, because `parse` keeps
    the last row of a label."""
    opener = "<" + "!--"
    above = opener + " a note, with an example:\n```\nan example\n-->\n\n"
    parsed = routing.parse(above + two_axis_text())
    assert parsed is not None and parsed["review"] == CHAIN, parsed
    below = f"\n{opener} the answer before:\n| Review | {DIRECT} |\n-->\n"
    assert routing.parse(two_axis_text() + below)["review"] == CHAIN
```
```python
    rule = reader()
    rows, ranges = [], []
    for path in paths:
```
```python
        for line in rule.readable(text):
```
```text
    **A row inside a fenced code block or an HTML comment is not an
    exemption** (#658; #584 round 2, finding 3). A `survivors.md` that shows
    its own format quotes a row, and one somebody withdrew comments it out;
    the reader took either as a judgment and excused a survivor with it.
    Excusing is the silent direction, so a fence or a comment nobody closed
    hides every row below it too: `unverified_check.py#readable` is the rule,
    and a file whose only rows are hidden holds no row and is refused as one.
```
```python
def test_a_row_inside_a_closed_comment_excuses_nothing(tmp_path):
    """#584 round 2, finding 3. A row somebody commented out is withdrawn,
    and the reader still took it as an exemption and excused a survivor."""
    reader = module()
    table = tmp_path / "survivors.md"
    table.write_text(
        "| Path | Quote | Grounds |\n|---|---|---|\n"
        "| `a.md` | a real sentence | real grounds |\n\n"
        + "<" + "!-- withdrawn:\n"
        "| `b.md` | a withdrawn sentence | nobody stands behind this |\n-->\n",
        encoding="utf-8",
    )
    rows, _ranges = reader.read_exemptions([str(table)])
    assert [where for where, _q, _g in rows] == ["a.md"], rows
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the nine touched modules (`test_routing_is_recorded`, `test_unverified_rows_close`, `test_a_corrected_sentence_survives_elsewhere`, `test_docs_line_wrap`, `test_handoff_outlives_the_merge`, `test_the_changelog_is_gathered_at_release`, `test_the_ledger_fragments_fold_at_release`, `test_a_rider_reaches_its_file`, `test_the_mode_question_is_asked_once`), at `628e37ef` | 680 passed, exit 0 |
| `comment_blocks` on a file with an opener quoted in a code span, a fenced rider example, then a real rider: `68bcb224` against HEAD | `(12, 13)` against `(6, 7)` |
| `comment_blocks` over every markdown file under the rider roots and `docs/`: `68bcb224` against HEAD, then HEAD against HEAD with 🟡 1's fix | 64 files, 0 differ; 64 files, 0 differ |
| `routing.parse` over every `routing.md`: `551c7967` against HEAD, then HEAD against HEAD with 🟡 2's fix | 25 files, 0 differ; 25 files, 0 differ |
| `routing.parse` with a ``` line inside a comment above the table: base, HEAD | a declaration; None |
| `routing.parse` with a `Review` row in a closed comment below the table, at HEAD | review read as straight to the PR |
| `read_exemptions` over every `survivors.md`: `7c47eec8^` against HEAD, then HEAD against HEAD with 🟡 3's fix | 15 files, 0 differ; 15 files, 0 differ |
| `read_exemptions` with a live row and a commented row, at HEAD | both rows read |
| `config_rows` with a ``` line inside a comment above the table: base, HEAD | nothing; nothing |
| `leaves_open`, the gather's and the fold's, over four closing shapes and three reader-limit shapes | not refused; refused |
| `gather_changelog.py --version 0.16.0 --dry-run` and `fold_ledger.py --version 0.16.0 --dry-run` in the clone | exit 0; exit 0 |
| Phase 9's cases with both scripts from `a06f23b2` | 8 failed, 1 passed |
| Phase 8's routing case with `hooks/routing.py` from `7c47eec8^` | 1 failed |
| Round 1's rider case with `rider_check.py` from `68bcb224` | 1 failed |
| The three cases below planted in their destination modules: at HEAD, then with the three fixes applied, with the rider, routing, survivor, parity and waiver modules | 3 failed; 463 passed, exit 0 |
| The full suite, lint, format and typecheck | not yet — the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/gather_changelog.py:102` | round 1's 🟡 1 — deferred |
| round-1 | `.github/scripts/fold_ledger.py:216` | round 1's 🟡 2 — deferred |
| round-1 | `hooks/config.py:232` | round 1's 🟡 3 — fixed |
| round-1 | `.github/scripts/rider_check.py:210` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/config.py:281` | round 1's ⬜ 5 — fixed |
| round-1 | `CHANGELOG.md`, `seal/ledger.md`, `seal/releases/*.md` | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/rider_check.py:226` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1790635413-every-markdown-reader-shares-one-fence-rule.md` | round 1's ❓ — out of verified scope |
| round-1 | `tests/test_a_script_copied_alone_exits_2.py` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
