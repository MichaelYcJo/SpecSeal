# 1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote — review round 2

| Field | Value |
|---|---|
| Target SHA | 09a734bae3aa5f13eba93c46a210a78e3195776e |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5[1m] |
| PR | 445 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `20eade5e1002bb5eb5636830779fb51362296b94..5a1f47e74add1661eef218181ae4477a0adca6cd`, 7 commits |
| Contract changes | fenced_row → round-2-report.md, round-2.md, pytest; fence_left_open → round-1-report.md, round-1.md, round-2-report.md, round-2.md, missing_row |
| New units | fence_map (depth 1); fenced_row_at (depth 1); test_a_file_whose_last_line_has_no_ending_gets_its_row_on_a_line (depth 1); test_the_arm_whose_repair_costs_a_row_says_there_is_more_to_write (depth 1); test_a_fence_opened_below_the_row_is_not_the_fence_above_it (depth 1); test_two_refused_lines_of_one_character_do_not_collide (depth 1) |
| Needs a fix | yes — finding 1, `seal mode` refusing forever over a fence the file does not have; finding 2, the fenced-row refusal naming a fence that is not above the row; finding 3, the tail chosen by string identity; finding 4, the arm whose repair costs a row and says nothing. |
| Loses a record or crashes | no — nothing raises and nothing leaves the root, and finding 1 is the one place a record was lost at the base rather than at the target SHA. |

- [x] Pass

## What this round was asked

The verifying round over round 1's fixes. Round 1's three findings closed `fixed` over `1f60a3c..48efed7`, and the units that closed them — `hooks/config.py#fence_map`, `skills/verify/scripts/broad_gate.py#fence_left_open`, two test functions and two constants, all depth 1 — are read by nobody but this round. That is what the round was pointed at: this repository has measured three consecutive rounds each finding their finding inside the previous round's fixes, across four rounds of #82.

The round was asked to open round 1's record and report first and to inherit coordinates rather than verdicts, and to treat each of the fix pass's four claims as a claim: that finding 1's case carries A4's closed-fence shape as a third fixture so a refusal wide enough to swallow it turns the case red rather than passing quietly; that finding 2 is pinned in both directions; that finding 3's class was four sites rather than the two the finding named, and that site 3's suffix is worded for its own subject; and that the re-stamped ledger rows number ten rather than the nine round 1 counted.

It was also asked to judge two things the orchestrator had already executed and said so — that finding 1 is closed over a two-run fixture, and that `survivor-check` over the fix range exits 0 with one survivor excused at `097bbdc` — and to judge the exemption itself, which is a judgment and not a measurement. And to judge the replacement `overview.md` §*Not done* paragraph the orchestrator wrote after round 1 found the first one named the wrong command.

The `#` column's shape was stated because round 1's report left ten cells empty and `round_record.py new` refused the whole table: a number for every row that commissions a fix, the severity glyph alone for every row that commissions none.

The broad gate was out of the round's hands (`agent-contract` §2), and the round wrote no record and no `plan.md` row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 A `config.md` whose last line has no ending is corrupted by `with_row`, caught by the new guard, and refused with a sentence naming a fence the file does not have — `seal mode` can never declare the mode for it | `skills/implement/scripts/seal.py#with_row`, `#write_row` | **fixed** `7c56e05` | fixed at 7c56e05; Executed over thirteen shapes: three trip the guard and one of them has no fence, `fence_map(...)[1]` is `None`. At `release/v0.12.1` the same file is written with its two rows merged into one and `declared_mode` stays `('none', '')` — the guard stops the loss and misnames the cause |
| 2 | 🟡 `fence_left_open` answers about the whole file, so a row inside a CLOSED example block is told a fence above it is open whenever any fence lower down is | `skills/verify/scripts/broad_gate.py#fence_left_open`, `#missing_row` | **fixed** `15d4f38` | fixed at 15d4f38; Executed over a config with a closed example block and a second block opened below it: *A fenced code block above it is never closed … Close that fence*. The same file without the trailing block prints *Move the row into*, which is the act this person needs. `fence_map` already returns the opener's index |
| 3 | 🟡 `after_stopper` is chosen by `line is stopper` over a list that is not stopped at the first match, so two refused lines that are both `\|` collide and the clause about the lines below is dropped | `skills/verify/scripts/broad_gate.py#missing_row` | **fixed** `1b23880` | fixed at 1b23880; Executed: `refusal` returns `[('\|', True), ('\|', False)]` and the stopper is identical to both, CPython sharing one object per one-character string. The refusal omits *There are more lines below it this reader will not take as rows either*; the same file with `\| x` as the second line prints it |
| 4 | 🟡 The `rows_read` arm of site 1 is the only one where following the refusal loses a row that reads today, and it is the one arm with no clause about what lies below | `skills/verify/scripts/broad_gate.py#missing_row` | **fixed** `538293c` | fixed at 538293c; Executed: `config_rows` returns `[('Mode', 'shared')]` before the instructed edit and `[('Broad gate', 'bin/test -q \| tee out.txt')]` after it — the `Mode` row is lost to the stop rule the edit switches on. The three sibling arms carry the *moves the stopping place down* clause; this one holds `after_mine` and says nothing |
| ⬜ | `spec.md` §*Data & interfaces* still gives the superseded wording as the contract, and §*Where spec and implementation diverged* does not carry the divergence its own escape hatch asks for | `seal/specs/1789721571-…/spec.md` §*Data & interfaces* | correction | Read: the section quotes *nothing was written below it* as site 2's contract and the case asserts that exact string is absent. The reasoning is in §*Fed back into the spec*, which `templates/sdd-overview.md` defines as clauses this work ADDED |
| ⬜ | The ledger fragment carries no row for `write_row`'s refusal, `fence_map` or `fence_left_open`, and R7 claims a behaviour the fix made conditional | `seal/ledger/1789721571-…md` | correction | Read: seven rows, none added by the fix range. R7's anchor is `fenced_row`, untouched by the fix, so `evidence-check` keeps passing over the narrowed claim |
| ⬜ | The new case's third fixture rebuilds the fixture `test_the_writer_and_the_reader_agree_about_which_row_is_the_row` already uses | `tests/test_the_mode_question_is_asked_once.py:633`, `:553` | correction | Executed: the widened-guard mutation turns both red. Deliberate and documented; noted so a change to `FENCED_ABOVE` is known to reach two cases |
| 🟢 | Round 1's finding 1 is closed, and the third fixture is a real canary | `skills/implement/scripts/seal.py#write_row`, `tests/test_the_mode_question_is_asked_once.py` | confirmed | Executed: the guard widened to refuse whenever a run of three backticks is anywhere in the text turns the case red at its third fixture, and the two fenced fixtures refuse with the file byte-identical and `('none', '')` unmoved |
| 🟢 | Round 1's finding 2 is closed and both directions are pinned | `skills/verify/scripts/broad_gate.py#fence_left_open`, `tests/test_the_seal_is_taken_once_by_the_sealer.py` | confirmed | Executed: `fence_left_open` wired to `return True` turns `test_a_broad_gate_line_only_inside_a_fence_is_named_and_not_called_absent` red at `assert "Move the row into" in said` |
| 🟢 | Round 1's finding 3 is closed at all four sites, and site 3's suffix speaks about its own subject | `skills/verify/scripts/broad_gate.py#missing_row` | confirmed | Read at all four arms: site 3's tail reads *There are more lines below THAT one*, chosen off `after_stopper`, which is the stopping line — the subject the person must fix there. The two touched modules are green |
| 🟢 | The ⬜ about re-stamped ledger rows: ten, not nine, and all twelve now record the reading | `seal/ledger.md` | confirmed | Executed: 20 rows at the target SHA carry 2026-09-18 and 8 did at the base, so twelve were re-stamped; two named the reading before `89b36d2` and ten did not; zero of the twelve are silent now |
| 🟢 | `overview.md` §*Not done*'s replacement paragraph is correct | `seal/specs/1789721571-…/overview.md` §*Not done* | confirmed | Executed: this round's own clone carries 48 tags including both `fixture/*` tags with `remote.origin.tagOpt` unset. The mechanism the paragraph now names — tag following on `git fetch` — is the one that produces the state |
| 🟢 | The survivor exemption at `097bbdc` is sound | `seal/specs/1789721571-…/survivors.md` | confirmed | Read: the standing quote is the same idiom in `refused_broad_row`, which answers one question and needs neither tail. Its only callers in the tree are two assertions, which predates this branch |
| 🟢 | Each fix commit carries the case that pins it | `2ad0a56`, `94f5a1d`, `87fc32c` | confirmed | Executed: every one of the three changes a module and its test file in the same commit |
| ❓ | The full suite, the repository-wide lint and the typecheck | `tests/`, the repository's `Broad gate` row | out of verified scope | `agent-contract` §2 and this round's prompt both place the broad gate with the sealer, after the rounds settle. Two modules were run narrow and nothing broad was |

## Paste-ready fixes

```python
    if end >= 0:
        # **The line above the insertion point may carry no ending.** Where
        # the first table's last row is the file's last line and the file
        # ends without a newline, the inserted row is concatenated onto it:
        # `| Record language | Korean || Mode | shared |` is one line of four
        # cells, no walk of that table reads either row, and the guard below
        # then refuses over a fence the file does not have. The third arm has
        # terminated the last line all along; this one has to as well. At
        # `release/v0.12.1` this shape was written silently and cost the row
        # that was already there (#429, round 2).
        if end == len(lines) and lines and not lines[-1].endswith(("\n", "\r")):
            lines[-1] += ending
        lines.insert(end, row + ending)
        return "".join(lines)
```
```python
fence_map = repo_config.fence_map
```
```python
    if not any(item == ROW_ITEM for item, _value in config_rows(new)):
        # **The message names the cause it CHECKED, never one it inferred.**
        # This guard is about the row not reading back, and an unclosed fence
        # is one way for that to happen rather than the only one — a file
        # whose last line carries no ending reached it too, and telling that
        # person to close a fence is the wrong-cause shape this work item is
        # about (#429, round 2).
        if fence_map(new.splitlines())[1] is not None:
            return (
                f"{path} has a fenced code block that is never closed, and "
                "everything under it -- the table this command would have "
                f"written the `{ROW_ITEM}` row into -- is inside it, where no "
                "walk of that table reads it. Nothing was written. Close the "
                "fence and run this command again."
            )
        return (
            f"{path} would not read the `{ROW_ITEM}` row back after this "
            "write, so the row would land where no walk of that table reads "
            "it. Nothing was written and your file is exactly as it was. "
            "This is a defect in this command rather than in your file: "
            "please report it with the file's first lines."
        )
```
```python
def fenced_row_at(home):
    """(index, line) for this gate's row written inside a code fence, or
    (None, None). `fenced_row` below is that answer's line alone, and its
    docstring is where this one's reasoning lives.

    The INDEX is what lets the refusal say *a fence above it*: an opener left
    unclosed lower down the file is not this row's cause, and the person whose
    row is in a block that closes correctly still has to move it
    (#429, round 2).
    """
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    text = config_text(home)
    if text is None:
        return None, None
    lines = text.splitlines()
    shown = {index for index, _line in config.unfenced(lines)}
    return next(
        (
            (index, line)
            for index, line in enumerate(lines)
            if index not in shown and names_this_row(line)
        ),
        (None, None),
    )


def fenced_row(home):
    """<the existing docstring, unchanged>"""
    return fenced_row_at(home)[1]


def fence_left_open(home, above=None):
    """Whether a fenced code block ABOVE the line at index ABOVE is never
    closed — or anywhere in the file, where ABOVE is None.

    <the existing docstring's three paragraphs, unchanged>

    **Above, because that is what the sentence says.** A file whose row sits
    in an example block that closes and which opens a second block further
    down answered True here, and the person was told to close a fence that
    has nothing to do with their row while the act they needed — move it —
    was the sentence they did not get (#429, round 2).
    """
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    text = config_text(home)
    if text is None:
        return False
    opened_at = config.fence_map(text.splitlines())[1]
    if opened_at is None:
        return False
    return above is None or opened_at < above
```
```python
    at, fenced = fenced_row_at(home)
    if fenced is not None:
        # Two causes, two acts, and the person in the second case has nothing
        # to move: their row is in the live table and a fence opened ABOVE it
        # was never closed, so it runs to the end of the file and takes the
        # whole table with it. Told to move the row they would follow the
        # instruction exactly and change nothing (#429, round 1). The fence
        # has to be above the row: one opened below it leaves the row inside
        # a block that closes, where moving it is still the act
        # (#429, round 2).
        where = (
            "A fenced code block above it is never closed, so it runs to the "
            "end of the file and takes the whole table with it. Close that "
            "fence — the row itself may already be where it belongs."
            if fence_left_open(home, at)
            else "Move the row into the `| Item | Value |` table that stands "
            "outside every fence, or add that table if the file has none."
        )
```
```python
    mine, reached, after_mine, after_stopper = None, False, [], []
    for position, (line, got) in enumerate(refused):
        if mine is None and names_this_row(line):
            mine, reached = line, got
            after_mine = [text for text, _got in refused[position + 1 :]]
            break
    if stopper is not None:
        # **The stopper's POSITION, not its identity.** `refused` holds line
        # text, and CPython hands back one shared object for every
        # one-character string — so two refused lines that are both `|` are
        # the same object, `line is stopper` matched both, and the tail came
        # from the last of them with the clause about the lines below
        # silently dropped. Every entry appended before the stopper carries
        # `got` True and the stopper's is the last of those, which is a fact
        # about how `refusal` fills the list rather than about the text
        # (#430, round 2).
        last_reached = max(
            position for position, (_line, got) in enumerate(refused) if got
        )
        after_stopper = [text for text, _got in refused[last_reached + 1 :]]
```
```python
            if rows_read(home):
                cost = (
                    ". The rows below it were read: nothing had parsed above "
                    "this line, so the table had not begun and the stop rule "
                    "needs a row before it can stop"
                ) + (
                    ""
                    if not after_mine
                    else ". Fixing this line is what lets the stop rule stop, "
                    "and the next line below it this reader will not take as "
                    "a row is where it will — so the rows under THAT line, "
                    "which arrive today, go with the repair. There is more "
                    "than one line to write here"
                )
                # The one arm where doing what this message asks makes the
                # file worse, and it was the one arm with nothing to say
                # about what lies below. Measured over a file whose quoted
                # line, a second malformed line and a `Mode` row stand in
                # that order: the reader returns the `Mode` row today and
                # loses it once the quoted line parses (#430, round 2).
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_mode_question_is_asked_once.py tests/test_the_seal_is_taken_once_by_the_sealer.py -q` in a clean clone at `09a734b` | `160 passed, 3 skipped`; exit code read directly, 0 |
| `fence_left_open` mutated to `return True`, then `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q -k "only_inside_a_fence or unclosed_fence_hides"` | exit 1 · `1 failed, 1 passed` at `assert "Move the row into" in said` |
| The `write_row` guard mutated to refuse whenever a run of three backticks is anywhere in the text, then `bin/test tests/test_the_mode_question_is_asked_once.py -q -k "unclosed_fence_is_refused or writer_and_the_reader_agree"` | exit 1 · red at `:633`, *the refusal reaches a file whose fence is closed and whose live table is right there*, and at `:557` |
| `write_row` over thirteen `config.md` shapes, each compared against `fence_map(...)[1]` | three refuse; two have an unclosed fence and the third has no fence at all — the file whose last line carries no ending |
| `with_row` over that file at the target SHA and at `origin/release/v0.12.1` | identical output both times, the last row and the new row merged into one line, `config_rows` of it `[]`. At the base `write_row` returns `""` and writes it; at the target SHA the guard refuses and the file is untouched |
| `missing_row` over a config with a closed example block and a second block opened below it, and over the same file without that block | *Close that fence* for the first, *Move the row into* for the second; `fence_left_open` is `True` for both |
| `missing_row` over a config with two refused lines that are both `\|`, and over the same file with `\| x` as the second | the clause about further lines is dropped for the first and printed for the second; `stopper` is identical to both entries of `refused` |
| `missing_row` and `config_rows` over a site-1 file with a second malformed line and a `\| Mode \| shared \|` row below both | the refusal says the rows below were read and says nothing more; `config_rows` is `[('Mode', 'shared')]` before the instructed edit and loses that row after it |
| The twelve `seal/ledger.md` rows this branch re-stamped, each checked for a 2026-09-18 reading in its prose at `1f60a3c` and at `09a734b` | two named one before `89b36d2`, ten did not; all twelve name one now |
| `git tag` in a plain `git clone --no-local` of this repository | 48 tags, both `fixture/*` tags present, `remote.origin.tagOpt` unset |
| Broad gate — the full suite, the repository-wide lint and the typecheck | not yet. It is the sealer's, once, after the rounds settle (`agent-contract` §2), and this round leaves findings open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/implement/scripts/seal.py#table_span`, `#with_row`, `#mode_report` | round 1's 1 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py#missing_row`, `#fenced_row` | round 1's 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py#missing_row`, `spec.md` §*Data & interfaces* | round 1's 3 — fixed |
| round-1 | `seal/specs/1789721571-…/overview.md` §*Not done* | round 1's ⬜ — correction |
| round-1 | `seal/ledger.md` | round 1's ⬜ — correction |
| round-1 | `hooks/config.py#unfenced` | round 1's ⬜ — answered |
| round-1 | `skills/verify/scripts/broad_gate.py#load` | round 1's ⬜ — answered |
| round-1 | `hooks/config.py#unfenced`, `#config_rows` | round 1's ⬜ — answered |
| round-1 | `seal/config.md` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/broad_gate.py#missing_row` | round 1's 🟢 — confirmed |
| round-1 | `hooks/optin.py#parity_config` | round 1's 🟢 — confirmed |
| round-1 | `hooks/config.py#config_rows` | round 1's 🟢 — confirmed |
| round-1 | `tests/` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `round_record.py` and `chain_check.py` were not driven against a fenced example table | already deferred in this branch — `seal/follow-up.md`, ticket #444 | the repository owner |
| One refusal loads `hooks/config.py` and reads `config.md` once per helper, and `fence_left_open` adds another pair on the fenced path | already answered in round 1 and named in `phases/phase-1.md` | the repository owner |
| The full suite, the repository-wide lint and the typecheck | the broad gate, after the rounds settle | the sealer |
