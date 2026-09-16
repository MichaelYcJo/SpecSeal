# Implementation Plan: a piped broad gate row takes every config row below it (#415)

<!-- seal/specs/1789598366-a-piped-broad-gate-row-takes-every-config-row-below-it/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-17 by the repository owner, when `smith` was spawned.

## Summary

Teach the one reader of `seal/config.md`'s table the escape markdown already
defines for a pipe in a cell, and give the caller that refuses a row a way to
say *this line will not parse* instead of *this row is absent*.

The two are not alternatives, although #415 lists them as two of three
options. The escape closes the spelling a person can be told to write; the
message closes the spelling a person actually types. Landing only the first
leaves the wrong-cause refusal standing for the common case, and landing only
the second leaves a form the criterion calls legal permanently unwritable.

## Technical context

**The one line that causes all of it** is `hooks/config.py:48`:

```python
CONFIG_ROW = re.compile(r"^\|\s*(?P<item>[^|]+?)\s*\|\s*(?P<value>[^|]*?)\s*\|\s*$")
```

A cell is *anything but a pipe*, so the first pipe inside a value ends the
cell, the line stops matching, and `config_rows` — whose rule is that any
line which is not a row ends the table — stops reading there.

**What the escape-aware cell looks like.** A cell becomes *any run of
characters that are neither a pipe nor a backslash, or a backslash followed by
anything*, and the captured text has each `\x` reduced to `x` before it is
stripped. The item cell takes the same treatment, because the pattern
describes a cell rather than a column.

**Who reads this table.** Four production readers and one test-local copy,
enumerated in `spec.md` §*The class, enumerated by construction*. Two of them
are worth naming again here:

- `hooks/mode-gate.py#undeclared` is a `PreToolUse` hook. **A wrong refusal
  there stops the session**, and there is nobody at the keyboard in the runs
  this plugin is built for. It is the caller a wrong refusal costs most, and
  the plan keeps it silent on purpose: nothing added in phase 2 is reachable
  from it.
- `skills/implement/scripts/seal.py#table_span` is the *writer's* loop, and
  it stops on exactly the same rule. When the reader and the writer disagree
  about which line is the `Mode` row, `with_row` inserts a second one — the
  file goes two rows deep, and that loop's own comment says no command can
  bring such a file back into agreement.

**The failure scenario of the chosen approach, in six months.** Somebody
writes a `Broad gate` row with a pipe, does not know about `\|` because
nobody reads a template before typing a row, and meets the new refusal. The
refusal names the line and quotes it — so the failure is loud — but it is
still a failure, and the complaint returns as *why do I have to escape a pipe
in a field you called a shell command line*. The answer the repository will
have to give is that the field is a markdown cell, which is why that question
is put to a person now rather than settled here (`questions.md` Q1).

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **Make the last cell greedy** — `(?P<value>.*?)` — so an **unescaped** pipe lands in the value | `\| a \| b \| c \|` becomes the row `('a', 'b \| c')`. A three-column table written under this one is then absorbed as rows of it instead of ending it, and `templates/config.md` ships three-column tables. It also reverses round 1 🟡 6 of the loop's own history, recorded in `tests/test_the_pull_request_language_is_the_repositorys.py#items` | **rejected.** It buys the naive spelling at the price of the rule that says where the table stops |
| **Skip the unparseable line and keep reading** — the fourth option #415 does not name | The stop rule exists so that prose and a second table are not read as more of this one. Skipping puts that back, and does it *silently* — a reader that quietly discards a line a person wrote is the same defect this work exists to remove, one line further along | **rejected.** A silence is not repaired by a second silence |
| **Name the cause and nothing else** — #415's option 2 alone | The escaped spelling stays unwritable, so a form `templates/config.md` §*Choosing a value — the criterion* calls legal has no spelling at all. And the `Mode` row hidden below such a line still vanishes silently, because `hooks/mode-gate.py` gets no message by design — so `seal mode` can still write a second `Mode` row | **rejected as the whole answer, adopted as half of it.** It is phase 2 |
| **Teach the escape and nothing else** — #415's option 1 alone | A person typing a shell command line writes `\|` bare. The row still does not parse, and `broad-gate` still says *has no `Broad gate` row* — the wrong-cause message #415 was opened about, surviving for the spelling people actually use | **rejected as the whole answer, adopted as half of it.** It is phase 1 |
| **Refuse a pipe in `broad_gate.py#not_as_written`** | The criterion already decided a pipe is legal, and the defect is in the table reader. A refusal here would restrict what a broad command may be, which `spec.md` §Out forbids and #415 lists under *Not this* | **rejected** |
| **Put the refusal in `hooks/config.py`** | It is the shared reader for four callers and one is a `PreToolUse` hook. A refusal there is a refusal about every row, in a module whose docstring says everything in it fails toward *nothing is declared*. `plan.md` of work item `1789445605` rejected the same move for the same reason | **rejected.** The new reader is pure: it reports, and only the two callers that already talk to a person consult it |
| **Nothing** — #415's option 3 | `templates/config.md` carries the measurement beside the promise, which is honest. But it leaves the writer able to put a second `Mode` row into a person's file, and a document that says *this does not work* is not a repair | **rejected** |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **A cell carries an escaped pipe, and the reader and the writer still agree.** `CONFIG_ROW`'s two cells become escape-aware; `config_rows` reduces an escaped pipe to one literal pipe in the value it returns. `table_span` inherits it through the alias. Also the three measurements `questions.md` M1–M3 ask for, recorded in `phases/phase-1.md` with their populations | `bin/test tests/test_the_mode_question_is_asked_once.py tests/test_the_seal_is_taken_once_by_the_sealer.py -q; echo $?` — exit code read directly, never through a pipe (§1). **Red-first mutation: revert `CONFIG_ROW`'s value cell to `[^\|]*?`.** The new case reads a four-row table whose SECOND row is a `Broad gate` row written with `\|` and whose third and fourth are `Mode` and `Record language`, and it must go red on **the number of rows returned** — a case that only checks the `Broad gate` value would still pass if the rows below were dropped, and dropping them is the defect. A second case counts `Mode` rows in the file `seal mode shared` writes over a config whose `Mode` row sits below that piped row, and goes red under the same revert | ed090be1 |
| 2 | **An unparseable line is named instead of being read as the end of the table.** `hooks/config.py` gains a pure reader returning the first line refused after the header; `broad_gate.py#missing_row` uses it and says the line will not parse, quoting it, where its first cell is `Broad gate`. `hooks/mode-gate.py` is not touched, and a case pins that it still denies nothing | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py -q; echo $?`. **Red-first mutation: delete the new branch in `missing_row`.** The fixture is a config whose `Broad gate` row carries a bare, UNESCAPED pipe — after phase 1 that is the shape that still will not parse, so the case has a subject. It asserts both halves of §14: the new sentence is present AND *has no `Broad gate` row* is absent. A separate case keeps the genuinely-absent config on the old sentence, so the branch cannot have swallowed it | d87da322 |
| 3 | **The fourth copy of the loop is closed.** `tests/test_the_pull_request_language_is_the_repositorys.py#items` goes, and its callers read through `hooks/config.py#config_rows` | `bin/test tests/test_the_pull_request_language_is_the_repositorys.py -q; echo $?`. **Red-first mutation: point the import at a local reimplementation again.** The identity assertion is `__code__.co_filename`, the way `tests/test_the_mode_question_is_asked_once.py#test_the_command_and_the_gate_read_one_parser` already asserts it for `seal.py` — a module loaded under a name of its own is a different module object with the same code, so an import check alone would not see the copy return | |
| 4 | **The documents and the records that promise the old behaviour.** `templates/config.md` §*What is refused, and what stays allowed* — the pipe row now says how a pipe IS written; `skills/config/SKILL.md`; the changelog fragment; the ledger fragment, where the falsified claim is removed and rewritten | `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_settings_have_a_front_door.py -q; echo $?`, then `bin/evidence-check --strict .; echo $?`. **Red-first mutation: restore the template's old pipe sentence.** The two cases in `tests/test_the_seal_is_taken_once_by_the_sealer.py` that today assert *cannot reach this row at all* and *takes every row below it* must be rewritten in this phase, and the rename of the case whose NAME states the old behaviour lands in the same commit as the fragment edit — a record naming a unit the tree lacks takes even the non-strict `evidence-check` to exit 2 | |

**Phase 1 before phase 2, and the order is load-bearing.** Phase 2's case
needs a line that still will not parse after the escape is taught, and that
is the unescaped pipe. Written the other way round, phase 2's fixture would
be an escaped pipe, phase 1 would then make it parse, and the case would go
green for a reason nobody intended — the shape
`seal/specs/1789455558-the-record-chain-disagrees-with-itself-in-five-places/overview.md`
records as *the thing seen red was not the thing shipped*.

**Every case here calls the unit the production path calls.** That
overview's first rule — *pin the function the production path calls, never
the helper beside it* — is why phase 1's case reads `config_rows` and
`broad_command` rather than applying `CONFIG_ROW` itself, and why phase 3
asserts by `__code__.co_filename`.

**Every fixture here is malformed on purpose.** The overview's second rule —
*check that a case's own assertion can fire before a fixture's guard does* —
bites hard in this work item, because the subject of every case is a config
file that does not parse. A fixture helper that builds a well-formed table
and asserts it reads back would swallow the whole subject. Build the fixture
text literally, and show each case red before it is planted (§15).

## Operational impact

| Item | What a reader must not miss |
|---|---|
| **Two ledger claims go false** | Both are in `seal/ledger/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for.md`, a fragment of this same unreleased cycle, not in `seal/ledger.md`. The row is REMOVED where it stands and the new claim written into this work item's own fragment — `CLAUDE.md` §*a change writes fragments*. Nothing is re-pointed |
| **Two test units carry the old behaviour in their names** | Renaming them and editing the fragment that cites them is **one commit**. `evidence-check`'s records arm refuses a record naming a unit the tree lacks, and a refused record takes even the non-strict run to exit 2 |
| **No migration, no new dependency, no new environment variable** | The change is one regex, one pure function, one branch and one sentence |
| **No compatibility break for a repository whose config parses today** | A widened cell pattern can only make more lines into rows, never fewer. A6 is the acceptance scenario that asks for the measurement rather than the argument, and a file whose reading moves is a divergence row in `overview.md` |
| **Anchors this branch drifts** | `hooks/config.py#config_rows` is cited by `seal/ledger.md` and by the fragment above, so drift is expected. Re-read each claim and re-stamp; do not sweep anchors whose claims are untouched |
