# Round 2 review — the verifying round over round 1's fixes (#415)

Target SHA `906c78b375e68793115f16fa007d9da2685fa744`, fix range
`c4e9c58b..af5b756c`, branch
`fix/415-a-piped-broad-gate-row-takes-every-config-row-below-it`, base
`release/v0.12.0`, pull request 428. Reviewed in a `git clone --no-local` at
that commit, in this session's scratchpad; nothing was written in the working
checkout except this file, and the clone was deleted afterwards.

Round 1's four verdicts are inherited, not re-derived. What this round did was
open the fixes themselves and the units they added.

## How this round's one finding relates to round 1's four

```
round 1 🟡 1 — the refusal stated the cost of a refused line FLAT
round 1 🟡 3 — a `Broad gate` row below a refused line was called ABSENT
        ↓ both were closed by one new unit, `hooks/config.py#refusal`
that unit answers about the FIRST refused line
        ↓ but both callers are asking about the TABLE
① a SECOND refused line further down makes both of the new sentences
  false again — one in each direction:
     · the row is in the file and the gate says it is absent   (🟡 3's shape)
     · the rows below were lost and the refusal says they were read (🟡 1's)
```

Round 1's 🟡 2 and 🟡 4 are answers rather than concessions. I tried to break
both by measurement and could not; §*What I verified and did not open* has the
numbers.

---

## 🟡 1. The refusal answers about one line, and a second bad line is what decides

`hooks/config.py:152` — `refusal` returns `(line, ended, below)` for the
**first** line it will not take as a row. `ended` says whether *that* line
ended the table, and `below` is read from the lines under *that* line, stepping
over any further refused line. `skills/verify/scripts/broad_gate.py:328`
chooses its cost sentence from `ended`, and `:352` gates the hidden-row branch
on `ended` as well.

`config_rows` stops at the **last** refused line it meets before the first one
that follows a found row. When two lines in one table will not parse, those are
different lines, and every sentence the gate prints is about the wrong one.

**Executed**, both shapes, in the clone at the target SHA.

The `Broad gate` row is in the file and the gate calls it absent:

```
| Item | Value |
|---|---|
| Notes | see C:\docs\|
| Mode | shared |
| Other | see C:\x\|
| Broad gate | bin/test -q |
```

| | What is true | What the gate says |
|---|---|---|
| `config_rows` | `[('Mode', 'shared')]` — the row never arrived | |
| `refusal` | `('| Notes | see C:\docs\|', False, [('Broad gate', 'bin/test -q')])` | |
| the message | the row is on line 6 | *has no `Broad gate` row* |

`hides_this_row` is given a list that **does** hold the row, and the branch
never runs because `ended` is `False` — it describes the `Notes` line, which
was the table's first row and ended nothing. This is round 1's 🟡 3 with one
more line in the file.

And the refusal tells a person rows arrived that did not:

```
| Item | Value |
|---|---|
| Broad gate | bin/test -q | tee out.txt |
| Mode | shared |
| Notes | see C:\docs\|
| Record language | Korean |
```

The message reads *The rows below it were read: nothing had parsed above this
line, so the table had not begun and the stop rule needs a row before it can
stop.* `config_rows` returns `[('Mode', 'shared')]`. `Record language` did not
arrive and silently falls back to English. Round 1's 🟡 1 was a person sent to
reformat rows that were read; this is the same person told to leave alone rows
that were lost, which is the more expensive direction because nothing sends
them back.

**Why it matters and who reaches it.** Both shapes need two lines the reader
refuses in one table. That is the population round 1's 🟡 3 was accepted on —
its own fixture is a Windows path ending in a separator, which stopped being a
row in phase 1 without anybody typing a pipe — with one more such line. A
person keeping two path-valued rows in `seal/config.md` is in it.

**The class, and what closes it.** `agent-contract` §12 asks for the class, and
the class is *a sentence about the table computed from one line of it*. The fix
below makes the walk carry both lines: `stopper` is the line that actually
ended the table, and `below` is the rows that actually failed to arrive. Then
the cost sentence has three cases rather than two, and the hidden-row branch
asks about the rows instead of about `ended`.

**Executed against the proposal.** With the patch applied in the clone, the
first file above says *has a `Broad gate` row and the reader never reached it*
and quotes `| Other | see C:\x\|`; the second says the rows directly below were
read, then names the line that lost the rest. `bin/test` over
`tests/test_the_seal_is_taken_once_by_the_sealer.py` and
`tests/test_the_mode_question_is_asked_once.py` stayed at exit 0, 143 passed.
Every file was restored from bytes afterwards.

---

## ⬜ The changelog states that repair without the condition it has

`seal/specs/1789598366-…/changelog.md:49` — *a row sitting BELOW a line the
reader refused is named as unreachable instead of absent.* Executed: for the
first file above it is not, and that file ships into the released notes as a
closed item. This is the same shape round 1's 🟡 1 found in the refusal
sentence, now in the bullet a release-notes reader meets. It is one sentence
behind finding 1 and is corrected with it.

## ⬜ Seven re-anchored ledger rows say nothing about who read them

`seal/ledger.md`, and `seal/specs/1789598366-…/overview.md:37`.

**Executed count** over `0995f62f..906c78b3`: thirteen rows of `seal/ledger.md`
had their content changed by this branch, and ten of those were re-stamped
again inside the fix range — hash only, no prose, no date. Six of the thirteen
carry a `Re-read 2026-09-17 by work item 1789598366 (#415)` note. **Seven carry
none**, and all seven anchor on
`skills/implement/orchestration.md#"## Orchestrator: Bootstrap — create what's
missing"`, whose hash this branch moved twice.

The `Date` column of all ten still reads 2026-09-10 or 2026-09-11, so the row
now carries a hash of content that did not exist on the date the row says it
was checked. The branch's own convention, followed in phases 1 to 4, is to keep
the date and append a *Re-read* sentence; the fix range re-stamped and appended
nothing.

`overview.md:37` is the row that discloses this to the owner, and it says *the
four claims re-read in `seal/ledger.md`* and *Each row carries a note saying
what was read and on what date*. The count is thirteen re-anchored and six
noted, and seven rows carry no note. `bin/evidence-check --strict .` is exit 0
either way — it checks the hash, not whether a person read the claim — so
nothing else will catch this.

This is the run's paperwork rather than the tool, so it is a correction and not
a fix to commission.

## ⬜ The limitation case names one of the four records that must change with it

`tests/test_the_mode_question_is_asked_once.py:332` —
`test_seal_mode_still_writes_a_second_mode_row_for_a_bare_pipe` pins a limit,
so its red direction is the limit being closed, and its whole value is the list
it hands the person who reddens it. Its messages name
`overview.md` §*Not done* and otherwise say *the records that disclose it*.
Round 1's 🟡 4 was that three of four disclosure sites read wrong; the case
names one of the four. The other three are `changelog.md:35`,
`spec.md` §*What this repair cannot see* and `templates/config.md`.

## ⬜ `refusal` gives up where `config_rows` keeps reading

`hooks/config.py:204`. A prose line **above** the table's first row ends the
walk and returns `None`, where `config_rows` steps past it and keeps reading —
so a refused row written under that prose is reported as an absent row. The old
`refused_row` did the same thing, so this predates the branch and is not a
regression; it is named because it is the same unit and the same class as
finding 1.

---

## What I verified and did not open

Each of these was executed in the clone at the target SHA, with every mutated
file restored from bytes the mutation script held and `tests/__pycache__`
cleared between runs.

**Round 1 🟡 2 is an answer.** Two measurements, and both say nothing became
unwritable.

- **Nothing lost a spelling.** I enumerated every `(item, value)` pair the
  pre-branch pattern could produce over the alphabet `a \ | space tab` up to
  eight characters — 17,297 pairs — spelled each one back as `| item | value |`
  and read it with the new pattern. **All 17,297 come back byte for byte**, and
  `unescaped` alters none of them.
- **The tree-wide comparison reproduces exactly.** 1,461 tracked files, 1,460
  readable, line by line with both patterns: **84 lines read differently, 83 in
  the widening direction and one the other way**, and the one is
  `rounds/round-1-report.md:135`, the fixture quoting this very shape. The fix
  pass's load-bearing measurement stands.

**Round 1 🟡 4 is an answer, and the worse claim is true.** Executed:
`write_row` over a bare-piped config leaves the file two `Mode` rows deep, and
the next `seal mode local` sets the first row to `local` and leaves the
person's own row reading `shared`. `config_rows` then returns `local` and the
file states two modes. The four disclosure sites agree with that and with each
other — `changelog.md:35`, `overview.md` §*Not done*, `spec.md` §*What this
repair cannot see*, `templates/config.md`. A release-notes reader meets *This
is closed for the escaped spelling only* and *a file that is already two rows
deep is repaired by nothing* in the same bullet as the repair.

**Where it was recorded is the right place.** §*Not verified* is counted by
`bin/unverified-check` and is for what nobody ran; this was run, so a row there
could never close. `seal/follow-up.md` sends anything tied to a coordinate to a
`# RIDER:`, and this is tied to `seal.py#table_span`. §*Not done* is what is
left.

**Finding 1's case is red on the CONDITION, both ways.** Restored from bytes:
the cost chooser wired to `True` — the sentence the build shipped — reddens
`test_what_a_refused_line_cost_is_read_off_the_file_and_not_stated_flat` on its
first-row half, and the two sentences swapped redden the same case on its
second-row half. A case asserting only that the conditional sentence exists
would survive the second. Both halves are in one case, as the fix record
claims.

**Finding 3's new branch is guarded.** The branch widened to fire on every
other-item refusal reddens
`test_a_refused_row_of_some_other_item_is_not_read_as_this_one`, and made
unreachable it reddens the new case. Executed separately: a file whose refused
line names another item and which has no `Broad gate` row anywhere still
reaches the absent-row refusal.

**Both new widenings are pinned.** `CELL` put back to `[^|]` reddens
`test_a_backslash_against_a_pipe_is_the_one_shape_the_escape_narrows`; a greedy
last cell reddens `test_seal_mode_still_writes_a_second_mode_row_for_a_bare_pipe`,
which is the inverted direction — it goes red the day the bare spelling is
closed.

**Round 1's ⬜ 5 is closed on both halves.** Executed: a refused line in a
second table now comes back as `None` rather than as this table's, and an
indented refused line is returned with its indentation, which is what the
rewritten docstring describes.

**The class generalises past the shapes the cases use.** Executed: a
three-column row — `| a | b | c |`, the round 1 🟡 6 shape — hiding a
`Broad gate` row below it reaches the new *never reached it* branch, so the
branch is about unparseable lines rather than about pipes.

Carried from round 1 rather than re-derived: its four verdicts, and that the
two ledger claims of the previous work item were REMOVED rather than
re-pointed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | `refusal` answers about the first refused line while both callers ask about the table, so a second refused line makes the absent-row message and the cost sentence false again | `hooks/config.py:152` | open | Executed: with two refused lines the `Broad gate` row on line 6 is reported ABSENT, and in the mirror shape the refusal says the rows below were read while `Record language` was lost. `hides_this_row` is handed a list holding the row and the branch is gated on `ended`, which describes a different line |
| ⬜ | the changelog states the round 1 🟡 3 repair without the condition it has | `seal/specs/1789598366-…/changelog.md:49` | correction | Executed: for the two-refused-line file the row is reported absent, not named unreachable |
| ⬜ | seven of the thirteen re-anchored `seal/ledger.md` rows carry no note saying who read them, and the record that discloses the re-reads says four and says each carries one | `seal/ledger.md`, `seal/specs/1789598366-…/overview.md:37` | correction | Executed: thirteen rows changed over `0995f62f..906c78b3`, ten re-stamped again inside the fix range, six carry a `Re-read 2026-09-17 … (#415)` note, dates still 2026-09-10/11. `bin/evidence-check --strict .` exit 0 either way |
| ⬜ | the bare-spelling limitation case names one of the four records that must change when the limit is closed | `tests/test_the_mode_question_is_asked_once.py:332` | correction | Read: the messages name `overview.md` §*Not done* and otherwise say *the records that disclose it*; the other three are `changelog.md:35`, `spec.md` §*What this repair cannot see*, `templates/config.md` |
| ⬜ | `refusal` gives up at a prose line above the table's first row where `config_rows` keeps reading | `hooks/config.py:204` | correction | Executed: a refused row under such a prose line is reported as an absent row. The old `refused_row` did the same, so it predates the branch |
| 🟢 | round 1 🟡 1 is closed — the cost sentence is read off the file and the case is red on the condition in both directions | `skills/verify/scripts/broad_gate.py:328` | confirmed | Executed: chooser wired to `True` reddens the first-row half, the two sentences swapped redden the second-row half |
| 🟢 | round 1 🟡 2 is an answer — no value lost a spelling, and the tree-wide measurement reproduces | `hooks/config.py:70` | confirmed | Executed: 17,297 old-reachable pairs all come back byte for byte from `| item | value |`; 1,460 files, 84 lines differing, 83 widening, one narrowing and it is the report's own fixture |
| 🟢 | round 1 🟡 3 is closed for the member it named, and the guard on the new branch is real | `skills/verify/scripts/broad_gate.py:352` | confirmed | Executed: the branch widened to every other-item refusal reddens `test_a_refused_row_of_some_other_item_is_not_read_as_this_one`; a file with no such row anywhere still reaches the absent-row refusal |
| 🟢 | round 1 🟡 4 is an answer — the four disclosure sites agree with the code and with each other, and the worse claim is true | `seal/specs/1789598366-…/overview.md` §*Not done* | confirmed | Executed: `seal mode local` over a two-deep file sets the first row and leaves the second, so the file states two modes and `config_rows` takes the first |
| 🟢 | both new widenings are pinned, the second in the inverted direction | `tests/test_the_mode_question_is_asked_once.py:230`, `:332` | confirmed | Executed: `CELL` reverted reddens the first; a greedy last cell reddens the second |
| 🟢 | round 1's ⬜ correction is closed on both halves | `hooks/config.py:152` | confirmed | Executed: a refused line in a second table comes back `None`; an indented refused line is returned with its indentation |
| 🟢 | the new branch is about unparseable lines rather than about pipes | `skills/verify/scripts/broad_gate.py:352` | confirmed | Executed: a three-column row hiding a `Broad gate` row reaches the *never reached it* branch |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the six modules this branch touches, at the target SHA, in the clone | exit 0 · 343 passed |
| the cost chooser wired to `True` — the sentence the build shipped | exit 1 · `test_what_a_refused_line_cost_is_read_off_the_file_and_not_stated_flat`, first-row half |
| the two cost sentences swapped | exit 1 · the same case, second-row half |
| the hidden-row branch widened to every other-item refusal | exit 1 · `test_a_refused_row_of_some_other_item_is_not_read_as_this_one` |
| the hidden-row branch made unreachable | exit 1 · `test_a_broad_gate_row_below_a_refused_line_is_not_reported_absent` |
| `CELL` back to `[^|]`, the pattern that predates the escape | exit 1 · 3 failed, including `test_a_backslash_against_a_pipe_is_the_one_shape_the_escape_narrows` |
| a greedy last cell, so the bare pipe parses | exit 1 · 4 failed, including `test_seal_mode_still_writes_a_second_mode_row_for_a_bare_pipe` |
| each of the six restored from bytes, `tests/__pycache__` cleared | exit 0 each |
| reachability: every `(item, value)` the old pattern produced, respelled `\| item \| value \|` and read by the new one | 17,297 pairs, 0 unreachable, 0 altered by `unescaped` |
| tree-wide line-by-line comparison, old pattern against new, over every tracked file | 1,461 tracked · 1,460 read · 84 lines differ · 83 widen · 1 narrows, at `rounds/round-1-report.md:135` |
| `write_row` over a bare-piped config, then `seal mode local` over the two-deep result | first row `local`, the person's own row still `shared`, `config_rows` returns `local` |
| `missing_row` over ten config shapes — piped first, piped second, other-item refusal hiding the row, no row anywhere, refusal first, two refusals, blank line, second table, indented, three-column | eight correct; the two-refusal shape reports ABSENT while the row is in the file |
| `refusal` and `missing_row` over the two two-refused-line shapes | the row called absent; and *the rows below it were read* while one was lost |
| the proposed repair applied in the clone, then the two test modules and the two shapes re-run | exit 0 · 143 passed; both messages correct; every file restored from bytes |
| `bin/survivor-check` over `c4e9c58b..af5b756c`, `c4e9c58b..HEAD` and `0995f62f..HEAD`, each with and without `--exempt` | exit 0 in all six · *no removed wording is still standing* in all six |
| `bin/evidence-check --strict .` | exit 0 |
| `bin/unverified-check seal/specs/` | exit 0 |
| The full suite, the repository-wide lint, the typecheck | **not yet** — the sealer's one broad run, after the rounds settle (`agent-contract` §2) |

All probe files lived outside the clone, in this session's scratchpad. The
clone was checked clean with `git status --porcelain` and then deleted.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `survivors.md` silences nothing at any range, including the one CI runs | `seal/follow-up.md`, the `#371` / `#308` row | already deferred — the repository owner. Measured here: `0995f62f..HEAD` reports zero survivors with the file, without `--exempt`, and at every narrower range too. The fix record says this of its two new rows; it is true of all twenty-one, and the cause is the one that row names — the quote joins the range's own added text before `--exempt` is consulted |
| A file already two `Mode` rows deep is repaired by nothing | `overview.md` §*Not done* | already deferred there by round 1's fix pass — the repository owner |
| A pull-request arm reporting a malformed `seal/config.md` | `spec.md` §Out, by name | already deferred in the frame |

## Paste-ready fixes

### Finding 1 — `hooks/config.py#refusal`, the walk and its contract

```python
def refusal(text):
    """Everything a caller with somebody to tell needs about the first line a
    person wrote as a row of this table and this reader will not take as one.

      line     the refused line as written, with its own indentation, or None
      ended    whether that line is the one that ENDED the table
      below    the rows written under the STOPPING line that never arrived
      stopper  the refused line that ended the table, or None

    **`ended` is a condition and not a decoration.** `config_rows` breaks on
    a line it cannot parse only once it has FOUND a row; with nothing found
    yet it steps past that line and keeps reading, so every row below still
    arrives. A refusal that says those rows were lost sends a person to
    reformat rows that were read correctly -- a true sentence about the wrong
    file, which is the shape #415 was opened about (round 1 🟡 1).

    **`stopper` is why `ended` is not enough.** The first refused line and
    the line that ended the table are the same line only when there is one
    of them. With two, `ended` is False while rows below are gone, and the
    row this gate is refusing over can be sitting under the SECOND one --
    reported absent, which is 🟡 3's shape with one more line in the file.
    So `below` is read from the stopping line and every sentence a caller
    builds is about the line it names (#415 round 2 🟡 1).

    **It reports and it refuses nothing.** Nothing here raises, and no caller
    becomes able to deny by importing it: it answers a question two callers
    that already talk to a person want to ask, which is *why did that row not
    arrive*. `hooks/mode-gate.py` deliberately does not ask it -- a
    `PreToolUse` hook that refuses wrongly stops a session with nobody able
    to get past it, and everything in this module fails toward silence.

    A line is one of these only when it begins with a pipe once its
    indentation is stripped, which is how a person spells a row -- an
    indented row is still a row somebody wrote. A blank line or a paragraph
    of prose ends the table by the rule `config_rows` has always had, so it
    is the table's end and not a refusal. So does a second header or a stray
    separator once a row has been found, and the walk stops there too rather
    than reaching into whatever table comes next.

    Before this existed the two states were indistinguishable to a caller:
    `broad_gate` reported a piped `Broad gate` row as ABSENT, which is a true
    sentence about a cause that is not the real one (#415).
    """
    seen_header, found, ended = False, False, False
    refused, stopper, below = None, None, []
    for line in text.splitlines():
        if not seen_header:
            if CONFIG_HEADER.match(line):
                seen_header = True
            continue
        if CONFIG_HEADER.match(line) or CONFIG_SEPARATOR.match(line.strip()):
            if found:
                break
            continue
        match = CONFIG_ROW.match(line)
        if match:
            if stopper is None:
                found = True
            else:
                below.append(
                    (
                        unescaped(match.group("item").strip()),
                        unescaped(match.group("value").strip()),
                    )
                )
            continue
        if not line.lstrip().startswith("|"):
            break
        if refused is None:
            refused, ended = line, found
        if found and stopper is None:
            stopper = line
    return refused, ended, below, stopper
```

`rows_under` has no caller left after this and comes out with it; its
tolerant-reading paragraph is the second one above. `refused_row` is unchanged
— `refusal(text)[0]` still answers it.

### Finding 1 — `skills/verify/scripts/broad_gate.py#refusal` and `#refused_broad_row`

```python
    config = load(CONFIG_READER, "specseal_config_for_broad_gate")
    text = config_text(home)
    if text is None:
        return None, False, [], None
    return config.refusal(text)
```

```python
    line, _ended, _below, _stopper = refusal(home)
    return line if line is not None and names_this_row(line) else None
```

### Finding 1 — `skills/verify/scripts/broad_gate.py#missing_row`, the cost sentence

```python
    line, ended, below, stopper = refusal(home)
    if line is not None and names_this_row(line):
        if not below:
            cost = (
                ". The rows below it were read: nothing had parsed above "
                "this line, so the table had not begun and the stop rule "
                "needs a row before it can stop"
            )
        elif ended:
            cost = (
                " — and every row written BELOW that line is lost with it, "
                "each falling back to its default with nothing said anywhere"
            )
        else:
            cost = (
                ". The rows directly below it were read — nothing had parsed "
                "above this line, and the stop rule needs a row before it "
                "can stop. The reader stopped lower down, at\n"
                f"    {stopper.strip()}\n"
                "so every row under THAT line is lost, each falling back to "
                "its default with nothing said anywhere"
            )
```

### Finding 1 — `skills/verify/scripts/broad_gate.py#missing_row`, the hidden-row branch

```python
    if stopper is not None and hides_this_row(below):
        return (
            f"broad-gate: {os.path.join(home, CONFIG)} has a `{ROW}` row and "
            "the reader never reached it. This line above it does not parse "
            "as a row of that table, and the reader stops reading there:\n"
            f"    {stopper.strip()}\n"
            f"So the `{ROW}` row written BELOW it is invisible, and there is "
            "no command to seal over. Every other row under that line is "
            "gone the same way, each falling back to its default.\n"
            "A cell of that table ends at a `|`. A value that needs one is "
            "written with markdown's own escape, `\\|`, which the reader "
            "reduces to a plain pipe before any shell sees it. "
            "`templates/config.md` §*What is refused, and what stays allowed* "
            "is where the row says so, and `/specseal:config` is the door to "
            "the file. Nothing ran."
        )
```

### Finding 1 — the case, in `tests/test_the_seal_is_taken_once_by_the_sealer.py`

```python
def test_a_second_refused_line_is_what_decides_what_a_first_one_cost(tmp_path):
    """Round 2's 🟡 1 of #415. `refusal` used to answer about the FIRST line
    it would not take as a row, and both of the sentences the gate builds are
    about the table: which rows failed to arrive, and whether this gate's row
    is one of them. Those are the same line only while there is one bad line.

    **Both directions are here, because the unit is wrong in both.** With the
    `Broad gate` row itself refused first, a later bad line loses rows the
    refusal then calls read — and nothing sends that person back. With some
    other item refused first, the gate's own row sits under the SECOND bad
    line and was reported absent, which is round 1 🟡 3 with one more line in
    the file.
    """
    hidden = refusal_over(
        tmp_path,
        "hidden_under_the_second",
        "| Item | Value |\n|---|---|\n"
        "| Notes | see C:\\docs\\|\n"
        "| Mode | shared |\n"
        "| Other | see C:\\x\\|\n"
        f"| {ROW} | bin/test -q |\n",
    )
    assert f"has no `{ROW}` row" not in hidden, (
        f"the row is in the file, under the SECOND line the reader refused:\n{hidden}"
    )
    assert "never reached it" in hidden, hidden
    assert "see C:\\x\\" in hidden, (
        "the refusal quotes the first bad line rather than the one that "
        f"actually stopped the reader:\n{hidden}"
    )

    lost = refusal_over(
        tmp_path,
        "lost_under_the_second",
        "| Item | Value |\n|---|---|\n"
        f"| {ROW} | bin/test -q | tee out.txt |\n"
        "| Mode | shared |\n"
        "| Notes | see C:\\docs\\|\n"
        "| Record language | Korean |\n",
    )
    assert KEPT not in lost, (
        "`Record language` did not arrive, and the refusal tells the person "
        f"every row below was read:\n{lost}"
    )
    assert "The reader stopped lower down" in lost, lost
    assert "see C:\\docs\\" in lost, lost
```

### Finding 1 — `changelog.md`, the fourth bullet's closing sentence

```
    A row that genuinely is not there gets the absent-row refusal exactly as
    before, and a row sitting BELOW a line the reader refused is named as
    unreachable instead of absent — read off the line that actually stopped
    the reader, so a second unparseable line above it does not send the
    message back to the wrong cause.
```

---

Needs a fix: yes — finding 1

Loses a record or crashes: no

## Proof block

Files opened: `hooks/config.py`, `skills/verify/scripts/broad_gate.py`,
`skills/implement/scripts/seal.py` (`table_span`/`with_row`/`write_row`),
`skills/config/SKILL.md`, `skills/implement/orchestration.md`,
`skills/code-review/scripts/survivor_check.py`, `templates/config.md`,
`bin/test`, `bin/survivor-check`, `.github/scripts/run_tests.py`,
`.github/workflows/hygiene.yml`,
`tests/test_the_mode_question_is_asked_once.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py`,
`tests/test_the_settings_have_a_front_door.py`,
`tests/test_first_setup_asks_once.py`, `seal/config.md`, `seal/ledger.md`,
`seal/ledger/1789598366-…md`, `seal/follow-up.md`,
`seal/specs/1789598366-…/{spec,plan,questions,routing,overview,changelog,survivors}.md`,
`seal/specs/1789598366-…/rounds/{round-1,round-1-report,round-1-fixes}.md`,
`~/.claude/skills/writing-style/SKILL.md`.

Commands run: listed in §*Executed probes*, all in a `git clone --no-local` at
`906c78b3`, exit codes read directly and never through a pipe.
