# Round 2 — the verifying round over round 1's fixes

Target SHA `09a734bae3aa5f13eba93c46a210a78e3195776e`, base `release/v0.12.1`,
draft pull request #445. Fix range `1f60a3c..48efed7`, seven commits.

Read and run in a `git clone --no-local` of the repository at the target SHA.
Nothing was written in the working tree except this report, and every probe
file and the clone itself are gone.

Round 1's coordinates were carried, not its verdicts. Its three findings were
re-derived against the code as it now stands, and each is closed.

## The headline

**All three of round 1's findings are closed, and the fix for the first one
carries a defect of its own.** `write_row`'s new guard refuses a write whose
row would not read back, which is right. The message it prints names one
cause — a fenced code block that is never closed — and the guard fires for a
second cause the fix pass did not enumerate: a `config.md` whose last line
carries no line ending. For such a file `seal mode` can never declare the
mode, and the sentence it prints about the person's file is false.

That is `agent-contract` §12 exactly: the finding named the coordinate, the
fix was written for the coordinate, and the class has two members.

Three smaller findings sit in the same two functions, all of them sentences a
person acts on. Nothing here loses a record and nothing raises.

## Stage 1 — the three claims the fix pass made

Everything below is **executed** unless it says *read*.

**Finding 1 (🔴) is closed.** Over both fenced fixtures the write is refused,
the file is byte-identical afterwards, and `declared_mode` still answers
`('none', '')`. The claim about the third fixture holds as well, and I checked
it the way the docstring asks to be checked rather than by reading it: with
the guard widened to refuse whenever a run of three backticks is anywhere in the text, the case goes red at its third
fixture's assertion, `tests/test_the_mode_question_is_asked_once.py:633`, with
*the refusal reaches a file whose fence is closed and whose live table is
right there*. A refusal wide enough to swallow A4's shape does turn the case
red.

**Finding 2 (🟡) is closed, and the other direction is pinned.** With
`fence_left_open` wired to `return True`, `test_a_broad_gate_line_only_
inside_a_fence_is_named_and_not_called_absent` goes red at `assert "Move the
row into" in said`. The condition is what the case pins, not the presence of a
string. Finding 2 of this round is about which files that condition answers
`True` for.

**Finding 3 (🟡) is closed at all four sites**, and the enumeration is
complete for the four arms the spec names. The four sentences say *no row was
written*, which is what `below` supports, and the two that predicted one edit
would finish the file now say the stopping place moves down. Finding 4 of this
round is about a fifth arm of the same function that the count of four does
not reach.

**The ⬜ about the re-stamped ledger rows: the fix pass's ten is right and
round 1's nine was wrong.** Measured rather than read. Twenty rows in
`seal/ledger.md` carry a 2026-09-18 `Checked` date at the target SHA and eight
of them carried it at the base, so twelve were re-stamped in this branch. Of
those twelve, two already named a 2026-09-18 reading in their prose before
`89b36d2` and ten did not. All twelve name one now.

**The replacement paragraph in `overview.md` §*Not done* is correct.** A plain
`git clone --no-local` of this repository carries 48 tags including both
`fixture/*` tags, with `remote.origin.tagOpt` unset — which is the probe this
report ran in, so the fact is the tool's own behaviour and not a quotation.
The mechanism the paragraph now names is the right one: `git fetch` follows
only tags reachable from what it downloaded, so a clone made before those two
tags were pushed stays without them.

**The survivor exemption at `097bbdc` is sound** — *read*. The standing quote
is the same idiom in `refused_broad_row`, a unit answering one question,
*which refused line is this gate's row*. `missing_row` replaced its copy
because it now needs two tails from the same walk, and `refused_broad_row`
needs neither. Rewriting it would be a change made to quiet a report. One
thing the grounds do not mention and a reader might want: that unit has no
production caller in the tree, only two assertions in
`tests/test_the_seal_is_taken_once_by_the_sealer.py`. That predates this
branch and does not weaken the exemption.

**`agent-contract` §14 holds per commit** — each of the three fix commits
carries its code change and the case that pins it in the same commit.

## Stage 2 — what this round found

### 🔴 1 — a `config.md` whose last line has no ending can never have its mode declared, and the refusal blames a fence the file does not have

`skills/implement/scripts/seal.py#with_row`, `#write_row`.

**Executed.** `with_row`'s second arm inserts the new row at `end`, the index
just past the first table's last row. Where that row is the file's last line
and carries no ending of its own, the inserted row is concatenated onto it:

```
in   '| Item | Value |\n|---|---|\n| Record language | Korean |'
out  '| Item | Value |\n|---|---|\n| Record language | Korean || Mode | shared |\n'
```

`config_rows` of that text is `[]` — one line of four cells, and both rows are
gone. The third arm already guards against this, terminating the last line
before it appends; the second arm does not.

At `release/v0.12.1` this shape was silent data loss: `write_row` returned
`""`, the file was written with the two rows merged, the `Record language` row
stopped being read, and `declared_mode` still answered `('none', '')`. **The
new guard stops the write, which is the improvement.** What it then says is:

> `<root>/seal/config.md` has a fenced code block that is never closed, and
> everything under it -- the table this command would have written the `Mode`
> row into -- is inside it, where no walk of that table reads it. Nothing was
> written. Close the fence and run this command again.

There is no fence in that file. `fence_map(text.splitlines())[1]` is `None`.
The person is told to close a fence that does not exist, and no act of theirs
makes `seal mode` write the row: the refusal repeats on every run, and the
mode gate asks again every session. That is the symptom round 1 opened its 🔴
about, reached by the second member of the same class.

Thirteen shapes were driven through `write_row`. Three trip the guard: a
backtick fence never closed, a tilde fence never closed, and this one. The
first two name their cause correctly.

The repair is two acts. The root cause is `with_row`'s insert arm, and with
that fixed this shape writes and reads back like any other. The message is the
second: it should name the cause it checked rather than one it inferred, so
that the next member of the class is not misdescribed either.

### 🟡 2 — an unclosed fence anywhere in the file is reported as the fence above the quoted row

`skills/verify/scripts/broad_gate.py#fence_left_open`, `#missing_row`.

**Executed.** `fence_left_open` asks whether the file has an opener that never
closes. It does not ask where that opener is. The refusal it chooses says *A
fenced code block **above it** is never closed*, so a file whose `Broad gate`
row sits in a closed example block and which opens a second block lower down
gets the wrong sentence and the wrong act:

````
# Repository config

An example of the format:

```markdown
| Item | Value |
|---|---|
| Broad gate | EXAMPLE |
```

And a block somebody opened and never closed:

```markdown
| Item | Value |
````

The gate prints *A fenced code block above it is never closed, so it runs to
the end of the file and takes the whole table with it. Close that fence — the
row itself may already be where it belongs.* The row is not where it belongs:
it is in an example block that closes correctly, and closing the later fence
changes nothing about it. The same file with the trailing block removed prints
*Move the row into the `| Item | Value |` table that stands outside every
fence*, which is the sentence this person needed.

This is the shape round 1's finding 2 was opened about, reached from the other
side. `fence_map` already returns the opener's index, so the position is one
comparison away.

### 🟡 3 — the tail below the stopping line is chosen by string identity, and one-character lines collide

`skills/verify/scripts/broad_gate.py#missing_row`.

**Executed.** The new loop finds the stopping line with `line is stopper` and
does not stop at the first match, so `after_stopper` is taken from the last
line that satisfies it. CPython hands back one shared object for every
one-character string, so two refused lines that are both `|` are the same
object:

```
| Item | Value |
|---|---|
| Mode | shared |
|
|
| Broad gate | bin/test -q |
```

`refusal` returns `[('|', True), ('|', False)]` and `stopper is refused[1][0]`
is `True` as well as `stopper is refused[0][0]`. The refusal then prints *No
other row was written under that line, so nothing else was lost with it.* and
stops — the clause *There are more lines below it this reader will not take as
rows either* is dropped, although one is. The same file with the second line
written `| x` instead of `|` prints the clause.

The position is recoverable without identity at all: every entry appended
before the stopper carries `got` `True`, and the stopper's is the last of
them.

### 🟡 4 — the one arm where following the instruction costs a row that reads today says nothing about it

`skills/verify/scripts/broad_gate.py#missing_row`, the `stopper is None` arm
with `rows_read(home)` true.

**Executed.** Round 1's finding 3 was repaired at four sentences. The same
function has a fifth arm that speaks about what lies below the quoted line,
and it is the only one where doing what the refusal asks makes the file worse.

```
| Item | Value |
|---|---|
| Broad gate | bin/test -q | tee out.txt |
| Record language | a | b |
| Mode | shared |
```

Today `config_rows` returns `[('Mode', 'shared')]` — nothing has parsed above
the quoted line, so the reader steps past both malformed lines and the `Mode`
row arrives. The refusal says *The rows below it were read: nothing had parsed
above this line, so the table had not begun and the stop rule needs a row
before it can stop*, and stops there.

Escape the pipe as the message instructs and `config_rows` returns
`[('Broad gate', 'bin/test -q | tee out.txt')]`. The quoted line now parses,
the stop rule can stop, and it stops at `| Record language | a | b |` — so the
`Mode` row that was being read is lost. The person follows the instruction
exactly and loses a declaration nothing warned them about.

The three sibling arms say *fixing this one moves the stopping place down
rather than clearing the table* when a refused line stands below. This arm has
`after_mine` in hand and says nothing.

### ⬜ the spec still states the superseded wording as the contract

`seal/specs/1789721571-…/spec.md` §*Data & interfaces* → *What the changed
sentences say*.

**Read.** That section says *The wording below is the contract* and gives site
2's as *— and nothing was written below it, so nothing else was lost with it:
this one line is the whole of what changes*. The code says *no row was
written*, and
`tests/test_the_seal_is_taken_once_by_the_sealer.py#test_a_second_unparseable_line_below_is_not_called_nothing`
asserts the spec's string is **absent** from the output. Spec and case now
contradict each other on the same sentence.

The escape hatch is in that section — *A builder who diverges records the
divergence in `overview.md` with both sides quoted* — and the fix pass wrote
the reasoning into §*Fed back into the spec* instead, which
`templates/sdd-overview.md` defines as *clauses this work added*. §*Where spec
and implementation diverged* carries three rows and none of them is this one.
Both sides are quoted somewhere, so nothing is hidden; what is missing is a
row in the table a reader checks. Either amend the four bullets or add the
row.

### ⬜ the ledger fragment does not carry what the fix range shipped

`seal/ledger/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote.md`.

**Read.** Seven claim rows, none added or re-verified by the fix range —
`89b36d2` touched two of them to re-stamp their dates. Three shipped
behaviours have no row: `write_row` refusing a row that would not read back,
`fence_map`, and `fence_left_open`. R7 claims *A `Broad gate` line that exists
only inside a code fence is quoted back **with where it has to move to***,
which the fix made conditional — half the time the refusal now says to close a
fence instead. Its anchor is `fenced_row`, which the fix did not touch, so
`evidence-check` will keep passing over a claim the code narrowed.

### ⬜ the new case's third fixture repeats a fixture two cases above it

`tests/test_the_mode_question_is_asked_once.py:633` and `:553`.

**Read.** `test_the_writer_and_the_reader_agree_about_which_row_is_the_row`
already builds `FENCED_ABOVE.replace("| Mode | shared |", "| Mode | local |")`
and drives `write_row` over it. The new case builds the same bytes for a
different purpose — as a canary against an over-wide refusal — and my mutation
turned both red. The duplication is deliberate and the docstring says so; it
is noted because a reader who changes `FENCED_ABOVE` now has two cases to
think about.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🔴 A `config.md` whose last line has no ending is corrupted by `with_row`, caught by the new guard, and refused with a sentence naming a fence the file does not have — `seal mode` can never declare the mode for it | `skills/implement/scripts/seal.py#with_row`, `#write_row` | open | Executed over thirteen shapes: three trip the guard and one of them has no fence, `fence_map(...)[1]` is `None`. At `release/v0.12.1` the same file is written with its two rows merged into one and `declared_mode` stays `('none', '')` — the guard stops the loss and misnames the cause |
| 2 | 🟡 `fence_left_open` answers about the whole file, so a row inside a CLOSED example block is told a fence above it is open whenever any fence lower down is | `skills/verify/scripts/broad_gate.py#fence_left_open`, `#missing_row` | open | Executed over a config with a closed example block and a second block opened below it: *A fenced code block above it is never closed … Close that fence*. The same file without the trailing block prints *Move the row into*, which is the act this person needs. `fence_map` already returns the opener's index |
| 3 | 🟡 `after_stopper` is chosen by `line is stopper` over a list that is not stopped at the first match, so two refused lines that are both `\|` collide and the clause about the lines below is dropped | `skills/verify/scripts/broad_gate.py#missing_row` | open | Executed: `refusal` returns `[('\|', True), ('\|', False)]` and the stopper is identical to both, CPython sharing one object per one-character string. The refusal omits *There are more lines below it this reader will not take as rows either*; the same file with `\| x` as the second line prints it |
| 4 | 🟡 The `rows_read` arm of site 1 is the only one where following the refusal loses a row that reads today, and it is the one arm with no clause about what lies below | `skills/verify/scripts/broad_gate.py#missing_row` | open | Executed: `config_rows` returns `[('Mode', 'shared')]` before the instructed edit and `[('Broad gate', 'bin/test -q \| tee out.txt')]` after it — the `Mode` row is lost to the stop rule the edit switches on. The three sibling arms carry the *moves the stopping place down* clause; this one holds `after_mine` and says nothing |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `round_record.py` and `chain_check.py` were not driven against a fenced example table | already deferred in this branch — `seal/follow-up.md`, ticket #444 | the repository owner |
| One refusal loads `hooks/config.py` and reads `config.md` once per helper, and `fence_left_open` adds another pair on the fenced path | already answered in round 1 and named in `phases/phase-1.md` | the repository owner |
| The full suite, the repository-wide lint and the typecheck | the broad gate, after the rounds settle | the sealer |

## Paste-ready fixes

Finding 1, the root cause — `skills/implement/scripts/seal.py#with_row`:

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

Finding 1, the message — `skills/implement/scripts/seal.py`, beside the other
aliases and in `write_row`:

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

Finding 2 — `skills/verify/scripts/broad_gate.py`, a sibling that hands back
the position and `fence_left_open` taking it (the sibling's name is new here,
NAME NOT IN TREE):

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

Finding 3 — `skills/verify/scripts/broad_gate.py#missing_row`:

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

Finding 4 — `skills/verify/scripts/broad_gate.py#missing_row`, the `rows_read`
arm:

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

Needs a fix: yes — finding 1, `seal mode` refusing forever over a fence the
file does not have; finding 2, the fenced-row refusal naming a fence that is
not above the row; finding 3, the tail chosen by string identity; finding 4,
the arm whose repair costs a row and says nothing.

Loses a record or crashes: no — nothing raises and nothing leaves the root, and finding 1 is the one place a record was lost at the base rather than at the target SHA.

## Proof block

Files opened: `hooks/config.py`, `skills/implement/scripts/seal.py`,
`skills/verify/scripts/broad_gate.py`, `bin/test`,
`tests/test_the_mode_question_is_asked_once.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py`, `seal/ledger.md`,
`seal/ledger/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote.md`,
`templates/sdd-overview.md`, and under
`seal/specs/1789721571-the-gate-reads-an-example-and-names-rows-nobody-wrote/`:
`spec.md`, `overview.md`, `changelog.md`, `survivors.md`,
`rounds/round-1.md`, `rounds/round-1-report.md`.

Probes: two `test_tmp_*` files in a `git clone --no-local` at the target SHA,
run once each and deleted with the clone.
