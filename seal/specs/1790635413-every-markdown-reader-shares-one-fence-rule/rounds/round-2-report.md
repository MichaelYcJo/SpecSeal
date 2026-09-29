# Round 2 — warden report

Target: branch `fix/584-every-markdown-reader-shares-one-fence-rule` at `628e37ef`, against `release/v0.16.0` at `551c7967`. Two jobs, kept apart:

- **Verifying** round 1's fixes, `1d3eb8a5..a06f23b2`, and the `New units` and `Contract changes` its record names.
- **Finding** in phases 8 (`7c47eec8^..2641ba87`) and 9 (`028eee43..628e37ef`), which nobody had reviewed.

Carried from round 1: its coordinates and the executed baseline of 140/140 changelog markers and 125/125 ledger markers. Not carried: any verdict. Every closure below was re-derived this round.

## What this round found, in one view

Round 1's five findings are closed. Phase 9 closes 1 and 2, and does it on the reader's own rule. The three new findings are one class, which the fix for round 1's finding 4 named and fixed in one reader: **a walk that decides fences needs to know whether a line begins inside an HTML comment, and a comment walk needs to know a code span.**

1. Round 1's fix gave the rider check a comment state with no code spans. So a comment opener quoted in a code span now hides the fence below it, and the real rider after that is lost (🟡 1). This is inside a unit round 1's fixes rewrote.
2. Phase 8 copied the config reader's fence rule into the routing reader, and that rule decides a fence before the comment. So a fence line inside a comment above the table now hides a declaration that read at the base. The same reader still takes a row parked in a closed comment below the table as the answer (🟡 2). This is on the commit gate's path.
3. Phase 8's exemption reader skips fences but not closed comments, so a commented-out exemption still excuses a survivor (🟡 3).

The config reader has the same fence-before-comment order, and has had it since before this branch. That is a question, not a finding here (❓ below).

## The account, checked

| Claimed | Found |
|---|---|
| Phase 8: no committed `routing.md` or `survivors.md` reads differently | Confirmed by execution. 25 of 25 declarations parse the same at `551c7967` and HEAD, and 15 of 15 exemption files read the same at `7c47eec8^` and HEAD |
| Phase 8: the routing case was red before the fix | Confirmed by execution: with `hooks/routing.py` from `7c47eec8^`, the case fails |
| Phase 8: `fenced` is held to the shared rule over the same shapes as the config copy | True, and the parity module is green. None of the shapes holds a comment, which is where 🟡 2 sits |
| Phase 9: eight cases red at `a06f23b2`, a ninth that passes before and after | Confirmed by execution, exactly: 8 failed, 1 passed |
| Phase 9: this tree is not refused | Confirmed by execution: the gather and the fold both exit 0 under `--dry-run --version 0.16.0` |
| Phase 9: `leaves_open` asks the exact shape each script writes | True by reading. The gather's `section` writes the marker, the body and a blank line, then the next marker. The fold writes `demote` of `own_marker_dropped`'s output rather than the text itself. The two lines those drop, the `# <id>` title and the fragment's own marker, cannot change whether a fence or a comment is open |
| Round 1's fix: "inside a comment nothing is markdown, so a ``` line in a rider's own body opens nothing" | True for that shape. But the scan that decides "inside a comment" reads a comment opener inside a code span as an opener. See 🟡 1 |

## 🟡 1 — a comment opener quoted in a code span makes the rider check read a quoted rider and lose the real one

`.github/scripts/rider_check.py:240`, the comment scan inside `fenced_lines`, which `comment_blocks` asks of every markdown file.

Round 1's fix added a comment state so that a fence line inside a rider's body opens nothing. The scan looks for `&lt;!--` and `-->` with `str.find` and does not know a code span. This repository's prose quotes the opener in backticks all the time. When it does, the scan believes a comment is open from that point on.

Executed on a file with that prose line, then a fenced example quoting a rider, then a real rider:

- At `68bcb224` the reader returns `(12, 13)`, the real rider, and nothing else. That is right.
- At HEAD it returns `(6, 7)`, the quoted rider. The fence line above the example was not a fence, because the scan thought it sat inside a comment.
- The quoted rider's own closing delimiter then ended the "comment". The example's closing fence line was read as an opener, and that fence ran to the end of the file and hid the real rider.

So one prose line produces both failures phase 3 and round 1 each closed: a quoted rider read as a rider, and a real rider never resolved. No file in today's tree has this shape (executed: 0 of 64 files under the rider roots differ between `68bcb224` and HEAD), so the finding is latent, as round 1's finding 4 was.

The fix reads the backtick run first, as `unverified_check.py#_liveness` does in its literal reading. It adds no second rule, only a code span that closes on its own line. With it, the case reads `(12, 13)`, round 1's case still passes, and 0 of 64 files differ from HEAD.

## 🟡 2 — the routing reader now misses a declaration with a fence line inside a comment above it, and still reads a commented-out row

`hooks/routing.py:118` (`fenced`) and `:147` (`table_rows`), which `parse` reads for the commit gate and `chain_check.py` reads at the pull request.

Phase 8 copied `hooks/config.py#fence_map`'s rule, and that rule decides a fence before it looks at comments. The shared rule does the opposite: `_liveness` opens a fence only on a line that begins outside every comment, and round 1's fix moved the rider check to that order for exactly this reason. Two shapes, both executed on `parse`:

- **A declaration that read at the base is now none.** Take a note in an HTML comment above the table that holds a ``` line. At `551c7967`, `parse` returns the declaration. At HEAD it returns `None`, because the ``` line inside the comment opened a fence that ran to the end of the file. The file renders with its table showing. The commit gate goes back to asking on a work item that answered, and in an automation run that is a stop in the middle of the run. The refusal also points at a missing declaration rather than at the fence, which is the wrong-cause shape #429 was opened about.
- **A row parked in a closed comment still answers.** `parse` keeps the last row of each label. So a `| Review | straight to the PR |` row inside a closed comment below the table turns a declared review chain into *straight to the PR*. That is the silent shape #658 closed for fences. Phase 6 gave the config reader a comment half for the same reason, and `fence_opener`'s docstring records routing's copy as having "no comment half" without giving a reason. This half predates the branch. It is in this finding because the one walk that fixes the first shape also fixes this one.

The fix gives `fenced` a comment state, with the same code-span reading as 🟡 1, and hides a line that begins inside a comment that closes, as `hooks/config.py#commented` does. An unclosed comment still hides nothing. `fenced` keeps its name and its answer on every comment-free shape, so the parity case stays green. Executed with the fix: both shapes read the declared chain, 0 of 25 declarations differ from HEAD, and the routing, parity and waiver modules are green. (NAME NOT IN TREE: the unit was removed or reverted after this was written)

## 🟡 3 — a commented-out exemption still excuses a survivor

`skills/code-review/scripts/survivor_check.py:1774` (`read_exemptions`).

Phase 8's own grounds apply here: "excusing is the silent direction". A `survivors.md` row that somebody withdrew by commenting it out is read as an exemption. Executed: a file with a live `a.md` row and a commented `b.md` row returns both.

`unverified_check.py#readable` is the shared answer, fences and comments together, and it already serves the review-record gates. An unclosed comment blanks to the end there, which here is the loud direction: fewer exemptions, or the empty-file refusal. With it, the case reads `a.md` alone and 0 of 15 exemption files differ from HEAD. The fix also loads the reader once per call rather than once per file. `hygiene.yml` hands every `survivors.md` in the tree to one run, so today that is fifteen loads of a 1,670-line module where one would do.

## Round 1's findings, each re-derived

- **Finding 1 and finding 2**, the release scripts writing markers their own readers cannot see, are closed by phase 9. The refusal comes before anything is written or printed, with or without `--dry-run`, and asks `live_lines` itself. The cases were red at `a06f23b2` (executed). Shapes that close are not refused (executed): an opener in a code span, a comment closed on its own line, a closed fence, and a table row quoting the opener.
- **The refusal fires only where the reader would misread.** Three shapes are refused although they render fine: an opener in a four-space code block, a bare opener after a lone backtick in the same paragraph, and a fence in a list whose closer is indented past three spaces (executed). In each, `live_markers` would also fail to see the next marker, so the refusal prevents the doubled entry rather than blocking a correct gather. These are `live_lines`' documented limits. The 140 historical entries hold none of them.
- **Finding 3** is closed as a statement. The docstring, `docs/the-broad-gate.md`, `templates/config.md` and the changelog fragment all state the code-span shape. The new case pins both the reading and the absence of the old sentence (executed, green). `spec.md` still carries the old sentence at line 115, and that is fine because it is not shipped and retires at settle.
- **Finding 4** is closed for its shape. The case fails with `68bcb224`'s `rider_check.py` and passes at HEAD (executed). The rewrite that closed it is where 🟡 1 sits.
- **Cleanup 5** is closed (read). `table_lines` computes `fence_map` once and hands it to `commented`. The other caller, `broad_gate.py#commented_row_at`, passes nothing and walks for itself, which is unchanged. (NAME NOT IN TREE: the unit was removed or reverted after this was written)
- **The new units** are correct as code: the rider case, `QUOTED_DELIMITERS` (NAME NOT IN TREE, reverted after round 3), and the code-span pin case. The one-line variant in the pin case closes its comment on the same line, so the stray closer below reads as text, as intended.

## Regression tests to plant

- `tests/test_a_rider_reaches_its_file.py`: a comment opener in a code span hides no rider (🟡 1).
- `tests/test_routing_is_recorded.py`: a comment above the table hides no declaration, and a commented row below it answers nothing (🟡 2).
- `tests/test_a_corrected_sentence_survives_elsewhere.py`: a row inside a closed comment excuses nothing (🟡 3).

All three are in the fix blocks below and were run in their destination modules as written. At HEAD, 3 failed. With the three fixes applied, those cases and the rider, routing, survivor, parity and waiver modules passed together: 463 passed, exit 0.

## Facts for the evidence ledger

- `rider_check.py#fenced_lines` treats a comment delimiter inside a code span that closes on its own line as text. Anchor it once 🟡 1 lands.
- `hooks/routing.py#table_rows` skips a line inside a fence and a line that begins inside an HTML comment that closes, and opens no fence on a line inside a comment. Anchor it on the routing walk once 🟡 2 lands, beside phase 8's row.
- `survivor_check.py#read_exemptions` reads through `readable`. Anchor it once 🟡 3 lands, as a re-read of phase 8's row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The rider check's comment scan reads a comment opener quoted in a code span as an opener, so a rider quoted in a fence below is read and the real rider after it is lost | `.github/scripts/rider_check.py:240` | open | Executed: HEAD returns the quoted block (6, 7) and misses the real one at (12, 13), which `68bcb224` reads. None in today's tree. Inside a unit round 1's fixes rewrote |
| 🟡 2 | The routing reader opens a fence on a line inside an HTML comment, so a declaration with such a note above its table is now none; and a row parked in a closed comment below the table still answers for it | `hooks/routing.py:118` | open | Executed: the base parses the first shape and HEAD returns None; the second reads straight to the PR. With the fix both read the chain and 0 of 25 declarations differ |
| 🟡 3 | The exemption reader takes a row inside a closed HTML comment as an exemption, so a withdrawn row excuses a survivor | `skills/code-review/scripts/survivor_check.py:1774` | open | Executed: the commented row is read. With `readable` it is not, and 0 of 15 files differ |
| 🟢 | round 1's finding 1 is closed — the gather refuses a fragment that leaves a fence or a comment open, before any write | `.github/scripts/gather_changelog.py#leaves_open` | confirmed | Built in phase 9. Executed: the cases red at `a06f23b2`, green at HEAD, the dry run over this tree 0 |
| 🟢 | round 1's finding 2 is closed — the fold refuses the same, before any write | `.github/scripts/fold_ledger.py#leaves_open` | confirmed | Built in phase 9. Executed: the cases red at `a06f23b2`, green at HEAD, the dry run over this tree 0 |
| 🟢 | round 1's finding 3 is closed — the shipped sentences state the code-span shape and a case pins them | `hooks/config.py#commented` | confirmed | Executed: the module is green with the pin case; read: the three sentences and the changelog fragment (NAME NOT IN TREE: the unit was removed or reverted after this was written) |
| 🟢 | round 1's finding 4 is closed for its shape — a fence line inside a rider's body hides no rider | `.github/scripts/rider_check.py#fenced_lines` | confirmed | Executed: the case fails with `68bcb224`'s script and passes at HEAD. 🟡 1 is the new instance in the same rewrite (NAME NOT IN TREE: the unit was removed or reverted after this was written) |
| 🟢 | round 1's cleanup 5 is closed — the fence walk runs once per call | `hooks/config.py#table_lines` | confirmed | Read. The other caller walks for itself, as before (NAME NOT IN TREE: the unit was removed or reverted after this was written) |
| 🟢 | Phase 8 changes no committed declaration or exemption file | `seal/specs/*/routing.md`, `seal/specs/*/survivors.md` | confirmed | Executed: 25 of 25, 15 of 15 |
| ❓ | `hooks/config.py#fence_map` also opens a fence on a line inside an HTML comment, so a config table below such a note is hidden. It did at `551c7967` too | `hooks/config.py#fence_map` | ❓ out of verified scope | Executed: `config_rows` returns nothing at the base and at HEAD. Not this round's diff and not a regression. It is the class member of 🟡 2 in a reader phase 6 ratified against its oracle. The orchestrating session answers whether it joins 🟡 2's fix in this branch or goes to its own issue |
| ❓ | The ledger fragment's rows, and the re-read notes phases 8 and 9 wrote into `seal/releases/*.md`, were not run through `evidence-check` | `seal/ledger/1790635413-every-markdown-reader-shares-one-fence-rule.md` | ❓ out of verified scope | A plugin check the broad gate runs. The sealer answers it |
| ❓ | The new cases on the Windows and Linux legs | `tests/test_routing_is_recorded.py` | ❓ out of verified scope | Only macOS ran here. CI's test matrix at the pull request answers it |

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

## Paste-ready fixes

### 🟡 1 — `.github/scripts/rider_check.py#fenced_lines` (NAME NOT IN TREE: the unit was removed or reverted after this was written)

Replace the comment scan at the end of the loop, from `pos = 0` to the `return`:

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

Add to the docstring, after the paragraph on comments:

```text
    A comment delimiter inside a code span that closes on its own line is
    text, as `_liveness` reads it: prose quoting the opener in backticks
    opened a "comment" that made the next fenced example no fence, read the
    rider quoted in it, and turned its closing fence line into an opener
    that hid every rider below (#584 round 2, finding 1).
```

The case, in `tests/test_a_rider_reaches_its_file.py`:

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

### 🟡 2 — `hooks/routing.py`

Replace `fenced`'s body, from its last docstring paragraph on, and add the walk below it:

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

In `table_rows`, replace the two lines that compute and ask the skipped set:

```python
    skipped = set().union(*hidden(lines))
    for index, line in enumerate(lines):
        if index in skipped:
```

and the docstring's last sentence, "`fenced` is the rule.", with:

```text
    A row inside an HTML comment that closes is a withdrawn answer on the
    same terms. `hidden` is the rule.
```

In `unverified_check.py#fence_opener`'s docstring, replace "with no comment half," in the routing bullet with:

```text
with a comment half that opens no fence inside a comment and hides a line
inside a comment that closes, held on comment-free shapes by
```

The case, in `tests/test_routing_is_recorded.py`:

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

### 🟡 3 — `skills/code-review/scripts/survivor_check.py#read_exemptions`

Load the reader once, above the loop, and read through `readable`:

```python
    rule = reader()
    rows, ranges = [], []
    for path in paths:
```

```python
        for line in rule.readable(text):
```

Replace the docstring's last paragraph with:

```text
    **A row inside a fenced code block or an HTML comment is not an
    exemption** (#658; #584 round 2, finding 3). A `survivors.md` that shows
    its own format quotes a row, and one somebody withdrew comments it out;
    the reader took either as a judgment and excused a survivor with it.
    Excusing is the silent direction, so a fence or a comment nobody closed
    hides every row below it too: `unverified_check.py#readable` is the rule,
    and a file whose only rows are hidden holds no row and is refused as one.
```

The case, in `tests/test_a_corrected_sentence_survives_elsewhere.py`:

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

Needs a fix: yes — 🟡 1 (the rider check loses a rider after a comment opener quoted in a code span), 🟡 2 (the routing reader misses a declaration under a comment holding a fence line, and reads a commented-out row as the answer), 🟡 3 (a commented-out exemption excuses a survivor)
Loses a record or crashes: no

## Proof block

Opened this round, in a `git clone --no-local` at `628e37ef`, except the first line:

- In the orchestrator's tree: `rounds/round-1.md`, `rounds/round-1-report.md`, `plan.md`, `phases/phase-8.md`, `phases/phase-9.md`, and `changelog.md`; and issue #658 on GitHub.
- The diffs `1d3eb8a5..a06f23b2`, `7c47eec8^..2641ba87` and `028eee43^..628e37ef` for every code, test and doc file they touch.
- `hooks/routing.py` (`fenced`, `table_rows`, `parse`), `hooks/config.py` (`FENCE`, `fence_map`, `commented`, `table_lines`), and `templates/sdd-routing.md`.
- `skills/verify/scripts/unverified_check.py` (`comment_scan` through `readable`), `skills/verify/scripts/broad_gate.py#commented_row_at`. (NAME NOT IN TREE: the unit was removed or reverted after this was written)
- `skills/code-review/scripts/survivor_check.py` (`reader`, `hook`, `read_exemptions`), and the lines naming `routing` in `chain_check.py`, `round_record.py` and `hooks/*.py`.
- `.github/scripts/gather_changelog.py` (`live_markers` through `insert`, `main`'s refusals), `.github/scripts/fold_ledger.py` (`marker` through `demote`, `own_marker_dropped`, `section`, `main`), `.github/scripts/rider_check.py` (`load_reader`, `fenced_lines`, `comment_blocks`).
- The helper names in `tests/test_a_rider_reaches_its_file.py`, `tests/test_routing_is_recorded.py`, `tests/test_a_corrected_sentence_survives_elsewhere.py` and `tests/test_unverified_rows_close.py#fenced_by_the_shared_rule`.
