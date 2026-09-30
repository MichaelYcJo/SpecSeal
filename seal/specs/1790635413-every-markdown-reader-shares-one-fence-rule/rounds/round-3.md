# 1790635413-every-markdown-reader-shares-one-fence-rule — review round 3

| Field | Value |
|---|---|
| Target SHA | b02d763ad65614ed173663dc8d1d5de4af9b3727 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #663 |
| Broad gate | 8b3f98f0 against f09f654e |
| Fixes checked by | no fixes to check |
| Fix range | `4edc5de6e230bf549c7e21f76052c5f910f68136..bd42959e4ac3dcc51d94920caa25b8c00a39ca55`, 3 commits |
| Contract changes | none |
| New units | unfenced (depth 1) |
| Needs a fix | yes — 🟡 1 (an unclosed comment switches off every fence below it in both hooks, so an example row answers for the routing table and an example table becomes the config table), 🟡 2 (an opener in prose makes the rider check read a quoted rider and lose the real one) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, verifying and the run's last: round 2 closed on its one reopening, so this record ends the run whatever it finds. Target round 2's fix diff `c7338c43..1729cf0f` at HEAD `b02d763a`, with the fixes' new units (`walk`, `hidden`, `comment_after`, `BACKTICKS` and five cases; NAME NOT IN TREE, all reverted after this round) as a finding surface, the reversal of round 1's 🟡 3 reading to be judged, and a missed declaration or a newly read commented-out row in either hook named as where a defect would leave the root.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | An HTML comment nobody closed switches off every fence below it, so a fenced example row answers for the routing table and an example table becomes the config table, with its `Broad gate` command | `hooks/config.py:183`, `hooks/routing.py:175` | deferred #667 | #667 — The run is capped. At the owner's decision, the readers this finding sits in (`hooks/config.py`, `hooks/routing.py`) were reverted to `release/v0.16.0` in `4edc5de6..4588df33`, so the shape reads as the base reads it. #667 redoes them from a clean frame (work item 1790645290); Executed: base reads the live answer on both shapes, HEAD reads the example. Inside units round 2's fixes created. The oracle shares the gap, so the parity case cannot see it |
| 🟡 2 | An opener written in prose, outside a code span, makes the rider check read a quoted rider and lose the real one, which is round 2's finding 1 from a trigger its fix cannot reach | `.github/scripts/rider_check.py:246` | deferred #667 | #667 — The same revert, for `.github/scripts/rider_check.py`; Executed: `68bcb224` reads the real rider; `c7338c43` and HEAD read the quoted one. Latent: 0 of 472 files. The fix reverses the `lone` assertion `a7581653` pinned, which is the owner's call |
| ⬜ 3 | A stray opener that a later fenced example closes hides the live table from both hooks | `hooks/config.py#walk` | deferred #667 | #667 — The loud half of the same comment-state reading, in the reverted readers; Executed: base reads it, HEAD reads none. Loud, and `_liveness`'s literal reading has the same limit |
| 🟢 | round 2's finding 1 is closed — a comment opener quoted in a code span no longer hides the rider check's fences | `.github/scripts/rider_check.py#fenced_lines` | confirmed | Executed: red with `c7338c43`'s script, green at HEAD. This round's finding 2 is the class member it could not reach (NAME NOT IN TREE: the unit was removed or reverted after this was written) |
| 🟢 | round 2's finding 2 is closed — a fence line in a comment above the table hides no declaration, and a row in a closed comment below it answers for nothing | `hooks/routing.py#hidden` | confirmed | Executed: both shapes red at the base, green at HEAD; 0 of 25 declarations differ (NAME NOT IN TREE: the unit was removed or reverted after this was written) |
| 🟢 | round 2's finding 3 is closed — a commented-out exemption excuses nothing | `skills/code-review/scripts/survivor_check.py#read_exemptions` | confirmed | Executed: red at the base, green at HEAD |
| 🟢 | round 2's ❓ on the config reader's fence-before-comment order is closed — answered into finding 2's fix | `hooks/config.py#walk` | confirmed | Executed: `test_a_fence_line_inside_a_comment_hides_no_table` (NAME NOT IN TREE, reverted after this round) red at the base, green at HEAD; 0 of 493 files differ under `config_rows` |
| 🟢 | The reversal of round 1's finding 3 reading is sound, and the pin case and the three sentences state it | `tests/test_the_mode_question_is_asked_once.py#test_delimiters_quoted_in_code_spans_hide_nothing` | confirmed | Read: it is `_liveness`'s literal reading and the rendered page. Executed: the pin case red at the base. The unclosed-comment sentence is this round's finding 1 to extend (NAME NOT IN TREE: the unit was removed or reverted after this was written) |
| 🟢 | round 2's question on the ledger is answered — the fragment's rows and the re-read notes the fix pass wrote into `seal/releases/*.md` hold | `seal/ledger/1790635413-every-markdown-reader-shares-one-fence-rule.md` | confirmed | Executed: `bin/evidence-check .` at `b02d763a`, exit 0; the fragment 72 ok, every ledger file 0 drifted and 0 broken, and 0 refused among the work item's names, this report included |
| ❓ | The new cases on the Windows and Linux legs | `tests/test_routing_is_recorded.py` | ❓ out of verified scope | Only macOS ran here. CI's test matrix at the pull request answers it |

## Paste-ready fixes

```python
    return _walk(lines, None)


def _walk(lines, literal_from):
    """`walk`, with no comment delimiter read from line LITERAL_FROM on.

    **A comment that never closes hides nothing, and it switches off no
    fence either.** Read comment-first, every line below an opener nobody
    closed begins inside a comment, so no fence opens there and a fenced
    example row below it read as a row: the routing reader took it as the
    answer and this one took an example table as the table (#584 round 3).
    So a walk that ends inside a comment is walked again with that opener's
    line and everything below it read by the fence rule alone. Nothing below
    it can close a comment -- no closer follows an opener that never closed
    -- so the second walk hides no line the first did not, and it ends
    outside.
    """
    shown, commented, run_of = [], set(), []
    opener, opened_at, comment, began = None, None, False, None
    for index, raw in enumerate(lines):
        line = raw.rstrip("\r\n")
        found = FENCE.match(line)
        run = found.group("run") if found else ""
        info = found.group("info") if found else ""
        if opener is not None:
            if run[:1] == opener[0] and len(run) >= opener[1] and not info.strip():
                opener, opened_at = None, None
            continue
        if comment:
            run_of.append(index)
        else:
            commented.update(run_of)
            run_of = []
            if run and not (run[0] == "`" and "`" in info):
                opener, opened_at = (run[0], len(run)), index
                continue
            began = index
        shown.append((index, line))
        if literal_from is None or index < literal_from:
            comment = comment_after(line, comment)
    if comment:
        return _walk(lines, began)
    commented.update(run_of)
    return shown, opened_at, commented
```
```python
    return _hidden(lines, None)


def _hidden(lines, literal_from):
    """`hidden`, with no comment delimiter read from line LITERAL_FROM on --
    `hooks/config.py#_walk`'s rule: a comment that never closes switches off
    no fence below it, so the walk that ends inside one is walked again with
    that opener's line read as text (#584 round 3)."""
    fenced_at, commented, run_of = set(), set(), []
    opener, comment, began = None, False, None
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
        else:
            commented.update(run_of)
            run_of = []
            if run and not (run[0] == "`" and "`" in info):
                opener = (run[0], len(run))
                fenced_at.add(index)
                continue
            began = index
        if literal_from is None or index < literal_from:
            comment = comment_after(line, comment)
    if comment:
        return _hidden(lines, began)
    commented.update(run_of)
    return fenced_at, commented
```
```python
    if opener is None and not live[len(lines)]:
        # A comment that never closes switches off no fence below it (#584
        # round 3): the lines under its opener's line are fenced by
        # `fence_spans` alone.
        began = max(n for n in range(len(lines)) if live[n])
        for first, last in uc.fence_spans(lines[began + 1 :]):
            end = len(lines) - began - 1 if last is None else last + 1
            fenced.update(range(began + 1 + first, began + 1 + end))
```
```python
    # a comment that never closes switches off no fence below it (#584
    # round 3): the fenced row is still fenced
    ["a note " + "<" + "!--" + " never closed", "| a |", "```", "| b |", "```", "| c |"],
```
```python
def test_an_unclosed_comment_switches_off_no_fence():
    """#584 round 3, finding 1. Read comment-first, every line under an
    opener nobody closed began inside a comment, so no fence opened there,
    and a fenced example row below the table answered for it."""
    opener = "<" + "!--"
    text = (
        two_axis_text()
        + f"\nA note: {opener} nobody closed this.\n\n"
        + f"```markdown\n| Review | {DIRECT} |\n```\n"
    )
    assert routing.parse(text)["review"] == CHAIN
```
```python
def test_an_unclosed_comment_switches_off_no_fence(config):
    """#584 round 3, finding 1. Read comment-first, every line under an
    opener nobody closed began inside a comment, so no fence opened there,
    and an example table above the live one became THE table: its `Mode`
    and its `Broad gate` command were read."""
    opener = "<" + "!--"
    text = (
        f"# c\n\nwrite {opener} to start a note.\n\n"
        "```\n| Item | Value |\n|---|---|\n| Mode | local |\n| Broad gate | true |\n```\n\n"
        "| Item | Value |\n|---|---|\n| Mode | shared |\n| Broad gate | bin/test |\n"
    )
    assert config.config_rows(text) == [("Mode", "shared"), ("Broad gate", "bin/test")]
    assert config.fence_map(text.splitlines())[1] is None
```
```text
(#584): a row somebody commented out is not an answer they gave. A comment
that never closes hides nothing and switches off no fence below it, a comment
delimiter inside a code span that closes on its own line is text, and a code
fence opens only on a line that begins outside every comment — the order the
shared rule reads in. Where this gate's row stands
```
```text
and the writer alike. **A comment that is never closed hides nothing**, and
it switches off no fence below it. A
```
```text
    answer they gave, which is the direction this module fails in. A comment
    that never closes hides nothing and switches off no fence below it: an
    unclosed opener above the live table leaves every row, and every fence,
    where it was. The line that OPENS a comment begins
```
```python
        assert "switches off no fence" in text, "/".join(parts)
```
```python
        if comment:
            comment = _reader.CLOSER not in line
            continue
        stripped = line.lstrip(" ")
        if len(line) - len(stripped) <= 3 and stripped.startswith(_reader.OPENER):
            comment = _reader.CLOSER not in stripped
```
```text
    **Only an opener that begins its line starts a comment that can hold a
    fence line**, which is CommonMark's HTML block, and it runs to the first
    line holding the closer. An opener anywhere else is inline, inside a
    paragraph, and a fence line interrupts a paragraph, so it hides no fence
    — whether it sits in a code span (#584 round 2, finding 1) or in plain
    prose (#584 round 3, finding 2). Reading either as a comment made the
    next fenced example no fence, read the rider quoted in it, and turned
    its closing fence line into an opener that hid every rider below. This
    departs from `_liveness`'s literal reading on purpose: the one question
    asked here is whether a line opens a fence, and the block rule answers
    it exactly.
```
```python
    # an opener that does not begin its line is inline, and a fence line
    # interrupts the paragraph it sits in: the fence opens and runs to the
    # end, so the rider below is not read (#584 round 3, finding 2)
    lone = (
        "a lone ` then " + opener + " a note\n```\n-->\n\n"
        f"{HTML_MARK} real\nVerified 2026-01-01 against r@abcdef12. -->\n"
    )
    assert riders.comment_blocks(lone.splitlines(), "doc.md") == []
```
```python
def test_an_opener_inside_prose_hides_no_fence():
    """#584 round 3, finding 2. An opener in prose, not in a code span, began
    a "comment" that the next example's closer ended, so the example was no
    fence, the rider quoted in it was read, and its closing delimiter opened
    a fence that swallowed the real rider below. Only a line that begins with
    the opener starts a comment that can hold a fence line."""
    opener = "<" + "!--"
    text = (
        "# doc\n\nWrite " + opener + " to open a note.\n\n"
        f"```markdown\n{HTML_MARK} quoted\n"
        "Verified 2026-01-01 against q@abcdef12. -->\n```\n\n"
        f"prose\n\n{HTML_MARK} real\nVerified 2026-01-01 against r@abcdef12. -->\n"
    )
    assert riders.comment_blocks(text.splitlines(), "doc.md") == [(12, 13)]
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the five touched modules (`test_routing_is_recorded`, `test_unverified_rows_close`, `test_the_mode_question_is_asked_once`, `test_a_rider_reaches_its_file`, `test_a_corrected_sentence_survives_elsewhere`), at `b02d763a` | 491 passed, exit 0 |
| The fix range's new cases, with the four code files from `c7338c43` | 20 failed, 2 passed, exit 1 |
| `routing.parse` and `config_rows`, the two 🟡 1 shapes and the two ⬜ 3 shapes: `c7338c43` against HEAD | 🟡 1: live answer against example; ⬜ 3: live answer against none |
| `comment_blocks`, the 🟡 2 shape, at `68bcb224`, `c7338c43` and HEAD | `(12, 13)`; `(6, 7)`; `(6, 7)` |
| 30,000 random files: config walk against routing walk against `hidden_by_the_shared_rule` (NAME NOT IN TREE), at HEAD | 0 differ; 0 differ |
| `routing.parse` over every `routing.md`, and `config_rows` over every markdown file: `c7338c43` against HEAD | 25 files, 0 differ; 493 files, 0 differ |
| 🟡 1's and 🟡 2's fixes with the four cases under *Regression tests to plant*, applied in the clone: the five touched modules | 495 passed, exit 0 |
| The same four cases with HEAD's code | 5 failed (the four cases and the flipped `lone` assertion's test), exit 1 |
| With 🟡 1's fix: the random files, the declarations and the markdown files again | 0 differ; 25 of 25 same as HEAD; 493 of 493 same as HEAD |
| With 🟡 2's fix: `fenced_lines` and `comment_blocks` over every markdown file under `docs/`, `seal/` and the rider roots, against HEAD | 472 files, 0 differ |
| `bin/evidence-check .` in the clone at `b02d763a`, with this report in the work item | exit 0; 0 drifted, 0 broken, 0 refused |
| `round_record.py new` on this report, in the clone | exit 0; the record parses, and it says the run is capped |
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
| round-2 | `.github/scripts/rider_check.py:240` | round 2's 🟡 1 — fixed |
| round-2 | `hooks/routing.py:118` | round 2's 🟡 2 — fixed |
| round-2 | `skills/code-review/scripts/survivor_check.py:1774` | round 2's 🟡 3 — fixed |
| round-2 | `.github/scripts/gather_changelog.py#leaves_open` | round 2's 🟢 — confirmed |
| round-2 | `.github/scripts/fold_ledger.py#leaves_open` | round 2's 🟢 — confirmed |
| round-2 | `hooks/config.py#commented` | round 2's 🟢 — confirmed (NAME NOT IN TREE: the unit was removed or reverted after this was written) |
| round-2 | `.github/scripts/rider_check.py#fenced_lines` | round 2's 🟢 — confirmed (NAME NOT IN TREE: the unit was removed or reverted after this was written) |
| round-2 | `hooks/config.py#table_lines` | round 2's 🟢 — confirmed (NAME NOT IN TREE: the unit was removed or reverted after this was written) |
| round-2 | `seal/specs/*/routing.md`, `seal/specs/*/survivors.md` | round 2's 🟢 — confirmed |
| round-2 | `hooks/config.py#fence_map` | round 2's ❓ — out of verified scope |
| round-2 | `tests/test_routing_is_recorded.py` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
