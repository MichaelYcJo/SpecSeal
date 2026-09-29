# Round 3 — warden report

Target: the fix diff `c7338c43..1729cf0f`, read in a `git clone --no-local` of the orchestrator's tree at `b02d763a`. The commit on top of the range is round 2's close and touches records only. This is a verifying round and the run's last: round 2 closed on a fix, which was the one reopening.

Carried from round 2: its coordinates, and the executed baseline of 25 declarations and 15 exemption files. Not carried: any verdict. Every closure below was re-derived this round.

## What this round found, in one view

Round 2's three findings are closed, and so is its ❓ on the config reader. The new walk reads a comment before a fence, and that order is right. It is the order `_liveness` uses, and it is what closes round 2's finding 2.

The order has one consequence nobody wrote down, and two findings come from it:

1. **In the hooks (🟡 1, in the new units).** "A comment that never closes hides nothing" is still true line by line. But every line below an unclosed opener now *begins inside a comment*, so no fence opens there. A fenced example below such an opener is read as live rows. The routing reader then takes an example row as the answer, and the config reader takes an example table as the table, including its `Broad gate` command. Both read the base correctly.
2. **In the rider check (🟡 2, one depth down).** Round 2's finding 1 was a comment opener quoted in a code span. The same failure comes back when the opener is written in prose without backticks, and the code-span fix cannot reach it. Losing a real rider is the silent half. Only a rule that tells a comment starting a line from one inside a paragraph can close it, and that rule reverses one assertion the fix range pinned.

A third shape is loud, and is recorded as ⬜ 3 without a fix.

## The account, checked

| Claimed | Found |
|---|---|
| Round 2's record: all three yellows `fixed` | Confirmed by execution. Every case the fixes added fails with the four code files from `c7338c43` and passes at HEAD (20 failed at base; 491 passed at HEAD over the five touched modules) |
| `hooks/config.py#walk` and `hooks/routing.py#hidden` are one rule, held to one oracle | Confirmed by execution, and beyond the listed shapes: 30,000 random files built from sixteen delimiter-heavy lines, 0 where config and routing differ, and 0 where config and `hidden_by_the_shared_rule` differ (NAME NOT IN TREE: the walks and the oracle were reverted after this round) |
| 0 of 25 declarations differ | Confirmed by execution against `c7338c43`. Also 0 of 493 markdown files in the tree differ under `config_rows` |
| The reversal of round 1's finding 3 reading is sound, and the three sentences and the pin case tell the truth | True for the code-span half, by reading and execution. The sentence "a comment that never closes hides nothing" is true but no longer complete. See 🟡 1 |
| "An unclosed comment still hides nothing" (round 2's report, on its fix) | True of the comment half. False of the fence half: it switches off every fence below it. See 🟡 1 |

## 🟡 1 — an HTML comment nobody closed switches off every fence below it, so an example row answers for the table

`hooks/config.py:183` (`walk`) and `hooks/routing.py:175` (`hidden`), both units round 2's fixes created. The first is read on every Bash call through `mode-gate` and by `broad-gate`; the second is read on every commit through the commit gate.

The new walk opens a fence only on a line that begins outside every comment. When an opener never closes, `comment` stays true to the end of the file. So no line below it can open a fence. The walk then keeps its older promise that an unclosed comment hides nothing, and shows every one of those lines. A fenced example below a stray opener is therefore read as live rows.

Executed at `c7338c43` and at HEAD, with one prose line holding an unclosed `&lt;!--` in each file:

| Shape | Base | HEAD |
|---|---|---|
| `routing.md`: the table, then the stray opener, then a fenced `| Review | straight to the PR |` | through the review chain | **straight to the PR** |
| `config.md`: the stray opener, then a fenced example table (`Mode local`, `Broad gate true`), then the live table (`Mode shared`, `Broad gate bin/test`) | the live table | **the example table** |

Why each one matters:

- **Routing.** `parse` keeps the last row of a label. A declared review chain reads as *straight to the PR*, which is the silent shape #658 closed for fences, now reached through a comment.
- **Config.** `config_rows` reads the first table. `declared_mode` then answers `local`, and `broad-gate` would run the example's command. With `true` in that cell, the one broad run reports green without running anything.

The oracle cannot catch this, because it is built the same way. `_liveness` calls every line after an unclosed opener not live, so `hidden_by_the_shared_rule` (NAME NOT IN TREE) opens no fence there either and then hides nothing. The two copies and the oracle agree on a rule that no single shared reader holds. `_liveness` hides that tail, and `readable` blanks it. Neither one shows it with its fences switched off.

The fix keeps the promise and extends it to fences. A walk that ends inside a comment is walked again, and from the opener's line down nothing is read as a comment delimiter. No `-->` follows an opener that never closed, so the second walk hides nothing the first did not, and it always ends outside a comment. Executed with the fix: both shapes read as at the base, config and routing agree with the extended oracle on 30,000 random files, 0 of 25 declarations and 0 of 493 markdown files differ from HEAD, and the five touched modules pass (495). The three new cases fail at HEAD.

The sentences change with it (contract §14). "A comment that never closes hides nothing" gains "and switches off no fence below it" in `docs/the-broad-gate.md` and `templates/config.md`. `test_delimiters_quoted_in_code_spans_hide_nothing` (NAME NOT IN TREE) already reads those two files and `hooks/config.py`, so it takes the new phrase as a second assertion.

## 🟡 2 — an opener written in prose makes the rider check read a quoted rider and lose the real one

`.github/scripts/rider_check.py:246`, the comment scan in `fenced_lines`. That unit was built in round 1's fixes and rewritten in round 2's, so this finding sits one depth below 🟡 1.

Round 2's finding 1 was this sequence:

1. A prose line quotes the opener in a code span, and the scan starts a comment there.
2. The next fenced example is no fence, so the rider quoted in it is read as a rider.
3. That rider's own `-->` ends the comment.
4. The example's closing fence line then opens a fence that hides the real rider below.

The fix taught the scan code spans, and that closes the backtick trigger. The same sequence runs from an opener written without backticks. Executed with `Write &lt;!-- to open a note.` as the prose line:

- At `68bcb224`, before round 1's fix: `(12, 13)`, the real rider.
- At `c7338c43` and at HEAD: `(6, 7)`, the quoted rider. The real one is lost.

No file in today's tree has the shape. Executed: 472 markdown files, and none holds an unquoted opener left open on its line. So the finding is latent, as round 2's finding 1 was.

No fix inside the literal reading can close this. A mid-line opener, a fence line and a later `-->` is exactly the shape the fix range pinned as a comment. That is the `lone` assertion in `test_a_comment_opener_quoted_in_a_code_span_hides_no_rider` (NAME NOT IN TREE), added in `a7581653`. The literal reading cannot tell that pinned case from this finding's shape.

CommonMark can tell them apart:

- An opener that begins its line, after at most three spaces, starts an HTML block. The block runs to the first line holding `-->`, and a fence line inside it opens nothing. This is round 1's finding 4, and every rider has this shape.
- An opener anywhere else is inline HTML inside a paragraph. A fence line interrupts the paragraph, so an inline opener can never hide a fence opener.

For the one question `fenced_lines` asks, whether a line opens a fence, that rule is exact rather than a guess at the block model. Executed with it:

- This case reads `(12, 13)`, and round 2's code-span case still passes, without any code-span logic.
- 0 of 472 markdown files differ from HEAD, in either `fenced_lines` or `comment_blocks`.
- The rider module passes once its `lone` assertion expects `[]`. That is the rendered truth, and the direction `comment_blocks`'s docstring already accepts for a fence nobody closed.

**The cost is a decision for the owner.** It moves the rider check off `_liveness`'s literal reading, which the unit's docstring cites, and it reverses one assertion this fix range pinned. That is why the fix is offered here and not closed here.

## ⬜ 3 — the loud half: a stray opener that a later example closes hides the live table

`hooks/config.py#walk`, `hooks/routing.py#hidden`. This is the same stray opener as 🟡 1, with a fenced example below the table that itself holds a closed comment. The example's `-->` ends the stray comment, and the example's closing fence line then opens a fence to the end of the file. Executed: the base reads the declaration and the config table, and HEAD reads `None` and `[]`. (NAME NOT IN TREE: the unit was removed or reverted after this was written)

This is the loud direction: the gate asks again, and `broad-gate` names the row as commented out. The literal reading in `_liveness` has the same limit. The line-start rule from 🟡 2 would close it for fences, but the hooks also use the comment state to hide rows. There a mid-line opener has to go on hiding a withdrawn row, so that rule cannot be copied into the hooks as it stands. Recorded, not commissioned.

## Round 2's findings, each re-derived

- **Finding 1 (rider, code span): closed for its shape.** Executed: the case fails with `c7338c43`'s script and passes at HEAD. 🟡 2 above is the same failure from a trigger the fix could not reach.
- **Finding 2 (routing, comment above and row below): closed.** Executed: both shapes of `test_a_comment_hides_no_table_and_answers_for_none` (NAME NOT IN TREE) read the chain at HEAD. At the base, the first returns `None` and the second returns *straight to the PR*.
- **Finding 3 (commented-out exemption): closed.** Executed: the case fails at the base and passes at HEAD. Read: `read_exemptions` goes through `readable`, which still counts a delimiter in a code span. That is the loud direction for an exemption, and the docstring and `20a0bfa` say so.
- **The ❓ on `hooks/config.py#fence_map`: closed into finding 2's fix.** Executed: `test_a_fence_line_inside_a_comment_hides_no_table` (NAME NOT IN TREE) fails at the base and passes at HEAD.
- **The contract change `commented` → `commented_row_at`: read.** `commented` lost its second parameter, and its one caller outside the module, `broad_gate.py#commented_row_at` (NAME NOT IN TREE), passes one argument.

## Regression tests to plant

| Destination | Case | Seen red |
|---|---|---|
| `tests/test_routing_is_recorded.py` | test_an_unclosed_comment_switches_off_no_fence, NAME NOT IN TREE | fails at HEAD, passes with 🟡 1's fix |
| `tests/test_the_mode_question_is_asked_once.py` | test_an_unclosed_comment_switches_off_no_fence, NAME NOT IN TREE | fails at HEAD, passes with 🟡 1's fix |
| `tests/test_unverified_rows_close.py` | a sixteenth `COMMENT_SHAPES` (NAME NOT IN TREE) entry, with the oracle extended | fails at HEAD (shape 15), passes with 🟡 1's fix |
| `tests/test_a_rider_reaches_its_file.py` | test_an_opener_inside_prose_hides_no_fence, NAME NOT IN TREE, and the `lone` assertion flipped | both fail at HEAD, pass with 🟡 2's fix |

## Facts for the evidence ledger

- `hooks/config.py#walk` and `hooks/routing.py#hidden` return the same hidden lines. Executed over 30,000 random files and every committed declaration, at `b02d763a`. (NAME NOT IN TREE: the unit was removed or reverted after this was written)
- No markdown file in the tree holds an HTML comment opener left open on its line outside a code span. Executed over 472 files, at `b02d763a`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | An HTML comment nobody closed switches off every fence below it, so a fenced example row answers for the routing table and an example table becomes the config table, with its `Broad gate` command | `hooks/config.py:183`, `hooks/routing.py:175` | open | Executed: base reads the live answer on both shapes, HEAD reads the example. Inside units round 2's fixes created. The oracle shares the gap, so the parity case cannot see it |
| 🟡 2 | An opener written in prose, outside a code span, makes the rider check read a quoted rider and lose the real one, which is round 2's finding 1 from a trigger its fix cannot reach | `.github/scripts/rider_check.py:246` | open | Executed: `68bcb224` reads the real rider; `c7338c43` and HEAD read the quoted one. Latent: 0 of 472 files. The fix reverses the `lone` assertion `a7581653` pinned, which is the owner's call |
| ⬜ 3 | A stray opener that a later fenced example closes hides the live table from both hooks | `hooks/config.py#walk` | open | Executed: base reads it, HEAD reads none. Loud, and `_liveness`'s literal reading has the same limit |
| 🟢 | round 2's finding 1 is closed — a comment opener quoted in a code span no longer hides the rider check's fences | `.github/scripts/rider_check.py#fenced_lines` | confirmed | Executed: red with `c7338c43`'s script, green at HEAD. This round's finding 2 is the class member it could not reach (NAME NOT IN TREE: the unit was removed or reverted after this was written) |
| 🟢 | round 2's finding 2 is closed — a fence line in a comment above the table hides no declaration, and a row in a closed comment below it answers for nothing | `hooks/routing.py#hidden` | confirmed | Executed: both shapes red at the base, green at HEAD; 0 of 25 declarations differ (NAME NOT IN TREE: the unit was removed or reverted after this was written) |
| 🟢 | round 2's finding 3 is closed — a commented-out exemption excuses nothing | `skills/code-review/scripts/survivor_check.py#read_exemptions` | confirmed | Executed: red at the base, green at HEAD |
| 🟢 | round 2's ❓ on the config reader's fence-before-comment order is closed — answered into finding 2's fix | `hooks/config.py#walk` | confirmed | Executed: `test_a_fence_line_inside_a_comment_hides_no_table` (NAME NOT IN TREE) red at the base, green at HEAD; 0 of 493 files differ under `config_rows` |
| 🟢 | The reversal of round 1's finding 3 reading is sound, and the pin case and the three sentences state it | `tests/test_the_mode_question_is_asked_once.py#test_delimiters_quoted_in_code_spans_hide_nothing` | confirmed | Read: it is `_liveness`'s literal reading and the rendered page. Executed: the pin case red at the base. The unclosed-comment sentence is this round's finding 1 to extend (NAME NOT IN TREE: the unit was removed or reverted after this was written) |
| 🟢 | round 2's question on the ledger is answered — the fragment's rows and the re-read notes the fix pass wrote into `seal/releases/*.md` hold | `seal/ledger/1790635413-every-markdown-reader-shares-one-fence-rule.md` | confirmed | Executed: `bin/evidence-check .` at `b02d763a`, exit 0; the fragment 72 ok, every ledger file 0 drifted and 0 broken, and 0 refused among the work item's names, this report included |
| ❓ | The new cases on the Windows and Linux legs | `tests/test_routing_is_recorded.py` | ❓ out of verified scope | Only macOS ran here. CI's test matrix at the pull request answers it |

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

## Paste-ready fixes

### 🟡 1 — `hooks/config.py#walk`

Replace the body of `walk` from `shown, commented, run_of = ...` to its `return`:

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

### 🟡 1 — `hooks/routing.py#hidden` (NAME NOT IN TREE: the unit was removed or reverted after this was written)

Replace the body of `hidden` from `fenced_at, commented, run_of = ...` to its `return`:

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

### 🟡 1 — the oracle and a sixteenth shape, `tests/test_unverified_rows_close.py`

In `hidden_by_the_shared_rule` (NAME NOT IN TREE), between the fence loop and `commented, run = set(), []`:

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

At the end of `COMMENT_SHAPES` (NAME NOT IN TREE):

```python
    # a comment that never closes switches off no fence below it (#584
    # round 3): the fenced row is still fenced
    ["a note " + "<" + "!--" + " never closed", "| a |", "```", "| b |", "```", "| c |"],
```

### 🟡 1 — the pin cases

`tests/test_routing_is_recorded.py`, above `test_a_row_quoted_inside_a_fence_is_not_an_answer` (NAME NOT IN TREE):

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

`tests/test_the_mode_question_is_asked_once.py`, above `test_the_writer_leaves_a_commented_row_alone` (NAME NOT IN TREE):

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

### 🟡 1 — the sentences, and the pin that reads them

`docs/the-broad-gate.md`, the sentence beginning "A comment that never closes":

```text
(#584): a row somebody commented out is not an answer they gave. A comment
that never closes hides nothing and switches off no fence below it, a comment
delimiter inside a code span that closes on its own line is text, and a code
fence opens only on a line that begins outside every comment — the order the
shared rule reads in. Where this gate's row stands
```

`templates/config.md`:

```text
and the writer alike. **A comment that is never closed hides nothing**, and
it switches off no fence below it. A
```

`hooks/config.py#commented`, the sentence on an unclosed comment: (NAME NOT IN TREE: the unit was removed or reverted after this was written)

```text
    answer they gave, which is the direction this module fails in. A comment
    that never closes hides nothing and switches off no fence below it: an
    unclosed opener above the live table leaves every row, and every fence,
    where it was. The line that OPENS a comment begins
```

`tests/test_the_mode_question_is_asked_once.py#test_delimiters_quoted_in_code_spans_hide_nothing`, in its loop: (NAME NOT IN TREE: the unit was removed or reverted after this was written)

```python
        assert "switches off no fence" in text, "/".join(parts)
```

### 🟡 2 — `.github/scripts/rider_check.py#fenced_lines` (NAME NOT IN TREE: the unit was removed or reverted after this was written)

Replace the comment scan, from `pos = 0` to the end of its `while` loop:

```python
        if comment:
            comment = _reader.CLOSER not in line
            continue
        stripped = line.lstrip(" ")
        if len(line) - len(stripped) <= 3 and stripped.startswith(_reader.OPENER):
            comment = _reader.CLOSER not in stripped
```

and the docstring paragraph that begins "A comment delimiter inside a code span":

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

### 🟡 2 — `tests/test_a_rider_reaches_its_file.py`

In `test_a_comment_opener_quoted_in_a_code_span_hides_no_rider` (NAME NOT IN TREE), the `lone` block:

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

and below that test:

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

Needs a fix: yes — 🟡 1 (an unclosed comment switches off every fence below it in both hooks, so an example row answers for the routing table and an example table becomes the config table), 🟡 2 (an opener in prose makes the rider check read a quoted rider and lose the real one)
Loses a record or crashes: no

The broad gate is not due: this report leaves two findings open. When the orchestrator settles them — fixed or filed — what comes due is the sealer's spawn.

## Proof block

Opened this round. The first line is in the orchestrator's tree; the rest are in a `git clone --no-local` of it at `b02d763a`:

- In the orchestrator's tree: `rounds/round-2.md` and `rounds/round-2-report.md`.
- The diff `c7338c43..1729cf0f` for every code, doc and test file it touches, and the work item's `changelog.md` and `survivors.md` hunks in it.
- `hooks/config.py` (`fence_map`, `comment_after`, `walk`, `commented`, `table_lines`, `config_rows`, `refusal`, `declared_mode`), `hooks/routing.py` (`fenced`, `comment_after`, `hidden`, `table_rows`, `parse`). NAME NOT IN TREE: the units round 1's and round 2's fixes added here were reverted after this round.
- `skills/verify/scripts/unverified_check.py` (`comment_scan`, `blank_fences`, `_liveness`, `_paragraph_ends_at`, `_partner_ahead`, `live_lines`, `readable`), `skills/verify/scripts/broad_gate.py` (`fenced_row_at`, `fenced_row`, `commented_row_at`, `fence_left_open`), `skills/implement/scripts/seal.py` (`table_span`, and the write guard that asks `fence_map`). NAME NOT IN TREE: `commented_row_at` was reverted after this round.
- `.github/scripts/rider_check.py` (`fenced_lines`, `comment_blocks`), `skills/code-review/scripts/survivor_check.py` (`reader`).
- `tests/test_unverified_rows_close.py` (`FENCE_SHAPES` through `test_the_comment_rule_agrees_with_the_config_reader`), and the new cases in `tests/test_routing_is_recorded.py`, `tests/test_the_mode_question_is_asked_once.py` and `tests/test_a_rider_reaches_its_file.py`. NAME NOT IN TREE: the comment cases were reverted after this round.
- `docs/the-broad-gate.md` and `templates/config.md`, the paragraphs the fix range changed.
