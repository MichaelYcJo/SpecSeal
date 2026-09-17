# Round 3 review — the last record of the run (#415)

Target SHA `6b49dedb4d0d937ec90aae61c2b9f3e398df6896`, fix range
`5137e934..c61bed39`, branch
`fix/415-a-piped-broad-gate-row-takes-every-config-row-below-it`, base
`release/v0.12.0`, pull request 428. Reviewed in a `git clone --no-local` at
that commit, in this session's scratchpad; nothing was written in the working
checkout except this file, and the clone was deleted afterwards.

Rounds 1 and 2's verdicts are inherited, not re-derived. The run is capped —
round 2 spent the one reopening the chain allows — so everything this round
opened leaves as a deferred issue rather than as a fix to commission. That is
why `Needs a fix` reads `no` below a table holding two 🟡: the cap decides the
answer, not the absence of findings.

## How this round's findings relate to the class

```
the class round 2 named — a sentence about the table computed from ONE line of it
        ↓ round 2's fix pass closed five members by keying every sentence on `stopper`
① the chooser now asks ONLY about `stopper` and never about `below`
   · the `Broad gate` row written LAST in its table loses nothing
   · the refusal says every row below it is lost
   · this is the shape `seal/config.md` in THIS repository has
        ↓ and one member the fix could not reach, because it is not this branch's
② `config_rows` takes the FIRST `| Item | Value |` header in the file,
   so a fenced example table above the real one is the table the gate reads
```

The two are independent. ① is the repair's own remaining edge; ② predates the
branch and is named because a round that found it and said nothing leaves it
for nobody.

---

## 🟡 1. The plainest file of all is told rows were lost when none were

`skills/verify/scripts/broad_gate.py:363` — the `elif mine is stopper:` branch
prints *— and every row written BELOW that line is lost with it, each falling
back to its default with nothing said anywhere*, and it never asks `below`
whether anything is there.

**Executed**, in the clone at the target SHA, over this file:

```
| Item | Value |
|---|---|
| Mode | shared |
| Broad gate | bin/test -q | tee out.txt |
```

| | What is true | What the gate says |
|---|---|---|
| `refusal` | `below` is `[]` — nothing is written under that line | |
| the message | one line has to change | *every row written BELOW that line is lost with it* |

**Why this shape and not another.** `seal/config.md` in this repository is two
rows, `Mode` then `Broad gate`, and `Broad gate` is the last of them.
`templates/config.md`'s own table ends the same way. So the file a person is
likeliest to be holding when they first type a bare pipe is exactly the file
this sentence is false-by-implication about, and what they do next is read a
two-row table looking for rows that were never written.

**It is the class, in the direction the fix pass did not turn it.** Round 2's
fix record rejected the reviewer's chooser with the sentence *`below` being
empty and the table not having begun are different facts, and reading one as
the other is the class the fix is for.* That is right. The repair then keyed
every branch on `stopper` alone, so `below` being empty is now read as *every
row below is lost* — the same conflation, mirrored.

**Both cases that pin the sentence pin it where it is vacuous.** Executed:
`tests/test_the_seal_is_taken_once_by_the_sealer.py:1162` asserts `LOST` over
the file above, and `:1198` asserts `LOST` over a file whose refused
`Broad gate` line is also last in its table. Neither fixture has a row below
the stopping line, so nothing in the suite reads the sentence against a file
it is informative about.

**The measured population.** Fifteen config shapes were run through `refusal`
and `missing_row`; three of them reach this branch with `below` empty — the
row last in a two-row table, last in a four-row table, and the same indented.
A fourth shape has a real row below it and the sentence is correct there.

The fix is one branch and two fixture edits; it is under §*Paste-ready fixes*.

---

## 🟡 2. A fenced example table above the real one is the table the gate reads

`hooks/config.py:105` — `config_rows` begins at the **first**
`| Item | Value |` header in the file and never looks for another. A
`seal/config.md` that documents its own format with a fenced example above the
live table hands the gate the example.

**Executed:**

````
Example:

```markdown
| Item | Value |
|---|---|
| Broad gate | EXAMPLE |
```

| Item | Value |
|---|---|
| Broad gate | bin/test -q | tee out.txt |
| Mode | shared |
````

`broad_command` returns `'EXAMPLE'`. The real row, the refused line and
`missing_row` are never consulted, because as far as the gate is concerned the
row was found.

**Why it matters and who reaches it.** A fence is invisible to this reader, so
the failure is silent in both directions: the person sees a documented example
and a live row, and the sealer runs the example. Where the example is a
plausible command rather than a placeholder — `bin/test -q`, say, next to a
live row that also lints — the gate comes back green over a narrower command
than the repository chose, and the seal covers that.

**It predates this branch and this branch could not have closed it.** The walk
in `config_rows` is unchanged over `0995f62f..HEAD`; only `CELL` moved.
`spec.md` §*What this repair cannot see* scopes out *a row above the header, a
row after a blank line, a row in a second table* — this is the inverse of the
third and is named in no record. It is reported here because the run ends and
nobody else is looking.

---

## ⬜ The four records the limitation case names can be pinned after all

`tests/test_the_mode_question_is_asked_once.py:358`. Round 2's fix record says
correction 3 *cannot be shown red and is not claimed to be: a message's text is
not what pytest reads*, and that *there is no way to pin that short of
asserting the message about itself.*

The first half is true and the second is too strong. What rots about a list of
four records is not its completeness but its coordinates: a record renamed or a
section retitled leaves the case handing a stale list to whoever reddens it.
That half pins cheaply — resolve the four paths and assert each exists, and
build the message from the same list, so the list and the assertion cannot
drift apart. The red direction is a record moving, which is a different
direction from the limitation closing, and both are worth having.

This is the run's paperwork rather than the tool, so it is a correction.

## ⬜ Two identical refused lines are quoted twice, once as *lower down*

`skills/verify/scripts/broad_gate.py:363`. Executed: a file with the same
unparseable `Broad gate` line written twice, a parsed row between them, gets
*this is it* over the line and then *The reader stopped LOWER DOWN, at* over
byte-identical text. Every fact in the message is correct — there really are
two such lines — but the person reads the same line twice and cannot tell them
apart. Cosmetic, and named so it is on the record rather than rediscovered.

---

## What I verified and did not open

Each of these was executed in the clone at the target SHA, with every mutated
file restored from the bytes the mutation script held and every
`__pycache__` cleared between runs. Exit codes were read directly.

**The two new cases are red on WHICH line a sentence describes.** All three of
the fix record's claims reproduce exactly, and each reddens *both* new cases:

- the reviewer's own chooser — `if not below` taken first — reddens both on the
  **one-bad-line half**, at `:1162` and `:1198`, each on the `LOST` assertion;
- the chooser collapsed back to two cases reddens both on the **two-bad-line
  half**, at `:1146` on *The reader stopped LOWER DOWN* and `:1211` on *never
  even reached it*;
- both units restored to `5137e934`, the commit before the fix, reddens both on
  *has no `Broad gate` row* (§15).

A case asserting only that a conditional sentence exists cannot be red under
the first two on opposite halves. These are.

**Four further mutations, each red on its own case.** The hidden-row branch
gated on the first refused line being the stopper; `refused_broad_row` asking
only the first refused line; the walk giving up at prose above the table's
first row; every refused line reported as reached. Restored after each: exit 0,
145 passed.

**The class holds at nine shapes the fix pass did not build.** Executed through
`refusal`, `missing_row`, `refused_broad_row` and `broad_command`, with an
instrumented copy of `config_rows` as the truth oracle:

| Shape | The gate's sentence |
|---|---|
| the header restated as a three-column row, the row below it | correct — *never reached it*, and the stopping line is quoted |
| a three-column row as the stopper, the row below it | correct |
| the `Broad gate` row refused and good, both in one table | correct — the good row is read and no refusal is built |
| CRLF line endings throughout | correct — `splitlines` drops the carriage return and every sentence is the same as for the LF file |
| an indented refused line last in its table | correct in every respect but ① above |
| a refused line, then a blank line, then the row | *has no `Broad gate` row* — scoped out by `spec.md`, see below |
| a refused line, then prose, then the row | the same |
| a refused line, then prose, then a row that parses | the same |
| a refused line, then a second header, then the row | the same, and here it is correct — that is a second table |

**The blank-line and prose shapes are scoped out, and the scope is honest.**
`spec.md` §*What this repair cannot see* says *every other way a row goes
missing is unchanged — a row above the header, a row after a blank line, a row
in a second table*. Measured: `below` stops at the first blank or prose line
under the stopping line, so `hides_this_row` answers `False` and the absent-row
refusal fires. That is not an under-report — `config_rows` would break at the
same line even with the stopping line repaired, so `below` is exactly what the
stopping line cost, which is what its docstring claims. The row really is
outside the table by the reader's own rule.

**The seven ledger notes hold, and each was checked against the section rather
than against the note.** All seven rows of `seal/ledger.md` anchored on
`skills/implement/orchestration.md#"## Orchestrator: Bootstrap — create what's
missing"` now carry a `Re-read 2026-09-17 in round 2's fix pass` note. The
branch's edits to that section are **one paragraph**, reached by two commits
(`291fde2` rewrote it, `caaa4c1` put the condition into what a bare pipe
costs), and it sits inside numbered item 1, inside the second question. Each
note's grounds were opened:

| The row | What its note claims | What I found |
|---|---|---|
| S4 / S12, the mode question | both edits sit inside the second question's paragraphs | the mode question is the numbered item's first half; the edit is below it |
| Q7, the 0.3.x layout | the paragraph sits above the numbered list | it does — it is the paragraph before item 1 |
| S5, the version one-liner | in the shared option's bullet, above both edits | it is |
| the templates-in-prose row | both edits name `templates/config.md` exactly as the text did before | six mentions in the section at the base, six at HEAD, all six byte-identical |
| r3 4, the clause tables | the first bullet still says it, the fourth still says evidence rows are left empty | both do |
| S7, the way back | the closing paragraph naming `/specseal:config` sits below the list | it does |
| S11 / S12, the preset | `CLAUDE.md` is untouched by this branch | `git diff` over `0995f62f..HEAD` on that path is empty |

`overview.md:37` now says thirteen and five and names the pass that gave seven
of them their notes, which is what round 2's count said. `bin/evidence-check
--strict .` is exit 0 either way, so this was the only thing that could catch
it.

**The survivors question — both causes are real, and the first is readable
from the code.** `survivor_check.py#exempted` compares an exemption row's first
cell against the candidate's path by equality or by path-suffix, so a cell
written `path:line` can never match at any range. All twenty-one rows were
written that way and all twenty-one are bare now. The second cause reproduces:
over `5137e934..c61bed39`, `5137e934..HEAD` and `0995f62f..HEAD`, with and
without `--exempt`, all six runs are exit 0 with byte-identical output — the
five places stopped being candidates once the rows were committed, which is
#371 / #308. So the file is inert at the range the fix pass runs, for the
reason already deferred, and live at a range that predates the rows.

Carried from rounds 1 and 2 rather than re-derived: their verdicts, that the
two ledger claims of the previous work item were REMOVED rather than
re-pointed, and round 2's reachability and tree-wide pattern measurements.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | the cost sentence asks only the stopping line and never the rows, so a `Broad gate` line written last in its table is told every row below it was lost when none was written | `skills/verify/scripts/broad_gate.py:363` | deferred #430 | Executed: over a two-row file ending in the refused line, `below` is `[]` and the message says every row below is lost. Both cases pinning that sentence use files with nothing below it. The run is capped, so this leaves as an issue rather than as a fix |
| 2 | `config_rows` reads the first `\| Item \| Value \|` header in the file, so a fenced example table above the live one is the table the gate runs | `hooks/config.py:105` | deferred #429 | Executed: `broad_command` returns the fenced example's value and the live row is never reached. Predates the branch — the walk is unchanged over `0995f62f..HEAD` — and is named in no record |
| ⬜ | the fix record's claim that the limitation case's list of four records cannot be pinned is too strong | `tests/test_the_mode_question_is_asked_once.py:358` | correction | Read: the completeness of the list cannot be pinned, but its coordinates can — resolve the four paths, assert each exists, build the message from the same list |
| ⬜ | two byte-identical refused lines are quoted as *this is it* and as *stopped LOWER DOWN* | `skills/verify/scripts/broad_gate.py:363` | correction | Executed: every fact in the message is correct and the reader cannot tell the two quotations apart |
| ⬜ | a `Broad gate` row below a blank line or prose under the stopping line is reported absent | `hooks/config.py:152` | deferred `spec.md` §*What this repair cannot see* | Executed over four shapes. `below` is exactly what the stopping line cost, so this is the reader's own rule rather than an under-report; `spec.md` names *a row after a blank line* by name |
| 🟢 | round 2's 🟡 1 is closed on all five members the fix pass enumerated | `hooks/config.py:152`, `skills/verify/scripts/broad_gate.py:351` | confirmed | Executed: all fifteen shapes reach the sentence naming the line their own facts are about, but for finding 1 |
| 🟢 | the two new cases are red on WHICH line the sentence describes, not on a sentence existing | `tests/test_the_seal_is_taken_once_by_the_sealer.py:1094`, `:1170` | confirmed | Executed: the reviewer's chooser reddens both on the one-bad-line half, the collapse reddens both on the two-bad-line half, and `5137e934` reddens both on the absent-row message |
| 🟢 | §15 holds for both new cases | `tests/test_the_seal_is_taken_once_by_the_sealer.py:1094`, `:1170` | confirmed | Executed: both units restored to the commit before the fix redden both cases |
| 🟢 | all seven re-anchored ledger rows carry a note whose grounds hold against the section | `seal/ledger.md`, `skills/implement/orchestration.md` §*Orchestrator: Bootstrap* | confirmed | Read the section and executed the diffs: one paragraph edited by two commits, inside numbered item 1; every claim each note makes about where it sits is true |
| 🟢 | `overview.md`'s disclosure agrees with the count | `seal/specs/1789598366-…/overview.md:37` | confirmed | Read: thirteen in `seal/ledger.md` and five in the previous work item's fragment, seven of the thirteen noted in round 2's fix pass |
| 🟢 | the survivor exemptions were inert for two independent causes, as the fix record says | `skills/code-review/scripts/survivor_check.py:891` | confirmed | Read `exempted` — a `path:line` cell matches neither by equality nor by suffix. Executed: six runs over three ranges, with and without `--exempt`, all exit 0 with identical output |
| 🟢 | CRLF, indentation and three-column stoppers are all read correctly | `hooks/config.py:152` | confirmed | Executed: the CRLF file's sentences are identical to the LF file's; an indented refused line comes back with its indentation; a three-column stopper reaches the *never reached it* branch |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_seal_is_taken_once_by_the_sealer.py` and `tests/test_the_mode_question_is_asked_once.py`, at the target SHA, in the clone | exit 0 · 145 passed |
| fifteen config shapes through `refusal`, `missing_row`, `refused_broad_row` and `broad_command`, against an instrumented copy of `config_rows` as the truth oracle | fourteen correct; the `Broad gate` line last in its table is told every row below it was lost |
| a fenced `\| Item \| Value \|` table written above the live one | `broad_command` returned the fenced example's value; the live row was never reached |
| the cost chooser keyed on `below` — the round 2 reviewer's own proposal | exit 1 · both new cases, on the one-bad-line half |
| the cost chooser collapsed back to two cases | exit 1 · both new cases, on the two-bad-line half |
| the hidden-row branch gated on the first refused line being the stopper | exit 1 · `test_a_second_refused_line_is_what_decides_what_a_first_one_cost` |
| `refused_broad_row` asking only the first refused line | exit 1 · `test_the_gate_reads_every_refused_line_and_not_only_the_first` |
| the walk giving up at prose above the table's first row | exit 1 · the same case |
| every refused line reported as reached | exit 1 · the same case |
| `hooks/config.py` and `skills/verify/scripts/broad_gate.py` restored to `5137e934`, the commit before the fix | exit 1 · both new cases, on *has no `Broad gate` row* |
| each of the two restored from bytes, every `__pycache__` cleared between runs | exit 0 · 145 passed each |
| `git diff` of `skills/implement/orchestration.md` over `0995f62f..HEAD`, and per commit | one paragraph, two commits; six `templates/config.md` mentions at the base and six at HEAD, unchanged |
| `git diff --stat` of `CLAUDE.md` over `0995f62f..HEAD` | empty — untouched, as the S11 note claims |
| `bin/survivor-check` over `5137e934..c61bed39`, `5137e934..HEAD` and `0995f62f..HEAD`, each with and without `--exempt` | exit 0 in all six · identical output with and without the file |
| `bin/evidence-check --strict .` | exit 0 · 0 refused · 0 drifted |
| `bin/unverified-check seal/specs/` | exit 0 |
| The full suite, the repository-wide lint, the typecheck | **not yet** — the sealer's one broad run, which this round's close is what makes due (`agent-contract` §2) |

Every probe file lived outside the clone, in this session's scratchpad. The
clone was checked clean with `git status --porcelain` after the last restore
and then deleted.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the cost sentence says rows below were lost where none were written | a new issue — the run is capped (`docs/review-chain-spec.md` §*The reopening*) | the repository owner. The paste-ready fix below is one branch and two fixture edits |
| a fenced example table above the live one is the table the gate reads | a new issue | the repository owner. Predates this branch; `spec.md` §*What this repair cannot see* names the neighbouring shapes and not this one |
| a `Broad gate` row below a blank line or prose is reported absent | `spec.md` §*What this repair cannot see* | already deferred there — the repository owner |
| `survivors.md` silences nothing at the range the fix pass runs | `seal/follow-up.md`, the `#371` / `#308` row | already deferred in round 2 — the repository owner. Re-measured here over three ranges, six runs |
| a file already two `Mode` rows deep is repaired by nothing | `overview.md` §*Not done* | already deferred by round 1's fix pass — the repository owner |
| a pull-request arm reporting a malformed `seal/config.md` | `spec.md` §Out, by name | already deferred in the frame |

## Paste-ready fixes

### Finding 1 — `skills/verify/scripts/broad_gate.py#missing_row`, the stopping-line branch

```python
        elif mine is stopper and below:
            cost = (
                " — and every row written BELOW that line is lost with it, "
                "each falling back to its default with nothing said anywhere"
            )
        elif mine is stopper:
            cost = (
                " — and nothing was written below it, so nothing else was "
                "lost with it: this one line is the whole of what changes"
            )
```

### Finding 1 — the docstring paragraph that states the count

```
    **It is read off the line that actually stopped the reader, which is
    not always the line being quoted.** A file with two lines the reader
    will not take has four shapes, and each gets its own sentence: nothing
    stopped the reader at all; this line stopped it; this line was read and
    something LOWER DOWN stopped it, so the rows under that line are the
    lost ones; or the reader had already stopped ABOVE this line and never
    met it. Chosen from a flat `ended` these collapsed into two, and both of
    the two were false about the two-line file — the rows below were lost
    while the refusal said they were read (#415 round 2 🟡 1).

    **The stopping line is asked what it took, not only that it stopped.**
    A row written LAST in its table stops the reader and loses nothing,
    because nothing is written under it — which is the shape this
    repository's own `seal/config.md` has, and the shape a person is most
    likely to be holding the first time they type a bare pipe. Reading an
    empty `below` as a loss is the same conflation as reading it as *the
    table had not begun*, mirrored, so the branch asks both (#415 round 3).
```

### Finding 1 — the two fixtures, in `tests/test_the_seal_is_taken_once_by_the_sealer.py`

```python
ALONE = "nothing was written below it, so nothing else was lost"
```

```python
    last = refusal_over(
        tmp_path,
        "refused_and_last",
        "| Item | Value |\n|---|---|\n"
        "| Mode | shared |\n"
        f"| {ROW} | bin/test -q | tee out.txt |\n",
    )
    assert ALONE in last, (
        "a `Mode` row parsed above this line and the line is what stopped "
        "the reader, so the cost is the rows below it — and none are "
        f"written. The refusal says rows were lost:\n{last}"
    )
    assert LOST not in last, last
    assert KEPT not in last, (
        "the table had begun: a `Mode` row is one line above this one.\n"
        f"{last}"
    )

    took = refusal_over(
        tmp_path,
        "refused_and_took",
        "| Item | Value |\n|---|---|\n"
        "| Mode | shared |\n"
        f"| {ROW} | bin/test -q | tee out.txt |\n"
        "| Record language | Korean |\n",
    )
    assert LOST in took, (
        "`Record language` is written under the stopping line and did not "
        f"arrive, and the refusal does not say so:\n{took}"
    )
    assert ALONE not in took, took
```

```python
    second = refusal_over(
        tmp_path,
        "refused_second",
        "| Item | Value |\n|---|---|\n"
        "| Notes | see C:\\x\\|\n"
        "| Mode | shared |\n"
        f"| {ROW} | bin/test -q | tee out |\n"
        "| Record language | Korean |\n",
    )
    assert f"has no `{ROW}` row" not in second, (
        f"the row is in the file and it is the SECOND refused line:\n{second}"
    )
    assert "bin/test -q | tee out" in second, second
    assert LOST in second, second
```

Needs a fix: no

Loses a record or crashes: no

## Proof block

Files opened: `hooks/config.py`, `skills/verify/scripts/broad_gate.py`,
`skills/implement/orchestration.md` §*Orchestrator: Bootstrap*,
`skills/code-review/scripts/survivor_check.py`, `templates/config.md`,
`seal/config.md`, `seal/ledger.md`, `bin/test`, `bin/survivor-check`,
`.github/scripts/run_tests.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py`,
`tests/test_the_mode_question_is_asked_once.py`,
`seal/specs/1789598366-…/{spec,plan,questions,overview,changelog,survivors,routing}.md`,
`seal/specs/1789598366-…/rounds/{round-1,round-1-fixes,round-2,round-2-report,round-2-fixes}.md`,
`seal/ledger/1789598366-…md`, `~/.claude/skills/writing-style/SKILL.md`.

Commands run: listed in §*Executed probes*, all in a `git clone --no-local` at
`6b49dedb`, exit codes read directly and never through a pipe.
