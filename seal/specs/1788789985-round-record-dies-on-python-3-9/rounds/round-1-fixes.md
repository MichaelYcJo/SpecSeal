# Round 1 — fixes · `1788789985-round-record-dies-on-python-3-9` (#226, PR #235)

Fix range `2b8a50a..fb45bc1`, five commits. Every paste-ready fix in
`round-1-report.md` was re-run against the tree as it stood rather than
trusted: the reviewer verified them at `804f14b` and two of them no longer
held.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `1e24566` |
| 2 | fixed | `cedc58e` |
| 3 | fixed | `ed7f577` |
| 4 | fixed | `00bc9b0` |
| 5 | fixed | `fb45bc1` |
| 6 | fixed | `fb45bc1` |
| 7 | fixed | `00bc9b0` |

## Where I did not take the paste-ready fix

**Finding 1 — the zip half of the pattern was left alone.** The report
replaced the whole of `ABOVE_THE_FLOOR`, including a balanced-paren rewrite of
the `zip` half. Measured over the same tree, that rewrite is a **regression**:
`zip\([^()]*(?:\([^()]*\)[^()]*)*strict=` is blind to `zip(xs, f(g(y)),
strict=True)`, which the shipped `zip\(.*strict=` catches, because `.` already
crosses any depth of nesting on one line. The rewrite's only gain is a
multi-line call, and nothing in the tree writes one. So only the UTC half
moved, to `\b\w+\.UTC\b`, and `re.S` went with the rewrite — the surviving
pattern has no `.` that needs it.

Both spellings find the same six files. That was checked, not assumed.

**Finding 2 — the row had a second defect, and it was already failing.** The
report says *"Nothing in the tree parses this file, so nothing catches it"*.
That is wrong: `tests/test_a_rider_reaches_its_file.py` parses it, and
`test_no_schedulable_row_carries_a_coordinate` **was red on this branch**
before I touched anything. The row carried five `file.py:NNN` coordinates,
which that case forbids — anything tied to a coordinate is a `# RIDER:` at the
line. The report's fix would have added a sixth coordinate to a row that may
carry none.

So the row lost its coordinates as well as its blank line. Nothing is lost by
that: `spec.md`'s enumeration table holds the file and line of each member,
and the row's first sentence already points there.

**Finding 4 — fixed rather than answered.** The round offered grounds and I
did not take them. The paragraph is a line **this diff authored** (`86e140f`
had "2 the input was unusable and nothing was written"), so it is in scope,
and I enumerated the exit sites from the module's own AST rather than
guessing at exhaustiveness: `SystemExit(2)` at the guard, `SystemExit(str)` in
`load`, `sys.exit(main())` at the bottom. Three, and the corrected paragraph
names all three.

Measuring it turned up something the finding did not have. `load`'s docstring
said *exit 2*, and the truth is worse than *exit 1*: `spec_from_file_location`
returns a spec for any path ending in `.py` whether the file exists or not, so
a missing `chain_check.py` never reaches the `SystemExit` sentence at all — it
reaches `exec_module` and raises `FileNotFoundError`. A bare traceback, exit 1.
That is the shape #226 exists to remove, one file over, and the `SystemExit`
branch is unreachable from this call site. Documented at the coordinate as a
`# RIDER:` with what closing it would take, because it is coordinate-tied and
this repository sends those to the line rather than to a list.

**Finding 5 — the coordinates name units now, not lines.** The report gave the
line numbers as of `804f14b`. My own fixes then moved them 32 lines further,
which is the finding arriving a second time inside its own fix. `spec.md` now
cites `round_record.py#swallowed`, `#inherited_rows` and `#signature`, which
is the rule `seal/ledger.md` already lives by: a coordinate names content, not
a position.

## What I ran

Every exit code below was read with `; echo $?`, never through a pipe.

| What was run | Result |
|---|---|
| `bin/test tests/test_a_script_says_which_interpreter_it_needs.py -q` after the finding 1 edits | `11 passed`, exit **0** |
| Mutation: the UTC half reverted to `datetime\.UTC`, the `CLASSIFIED` row kept | exit **1** — `['skills/verify/scripts/session_cost.py'] no longer carry the construct they were classified for` |
| Mutation: the `CLASSIFIED` row removed, the widened half kept | exit **1** — `['skills/verify/scripts/session_cost.py'] use a construct newer than python 3.12 and are not classified` |
| Mutation: `_EARLY = os.path.abspath(__file__)` inserted above `FLOOR`, widened AST case | exit **1** — `module level calls abspath() at line 150, above the guard at line 183`. The shipped case was green against the same mutation |
| Mutation: the `§` put back into `BELOW_FLOOR` | exit **1** — `the refusal carries ['§'], which prints as an escape under an ASCII stderr` |
| `PYTHONIOENCODING=ascii /usr/bin/python3 skills/code-review/scripts/round_record.py new --help` (3.9.6) | exit **2**, the whole three-line refusal in ASCII, no escape |
| The real script with `chain_check.py` deleted, at 3.14.4 | exit **1**, `FileNotFoundError` traceback — the docstring's `exit 2` disproved |
| `bin/test tests/test_a_rider_reaches_its_file.py -q` before the finding 2 fix | exit **1** — the coordinate case |
| The same after it | exit **0** |
| `bin/test` over the four modules `round_record.py` backs (`test_the_record_is_generated`, `test_the_fixes_close_the_record`, `test_the_fixes_name_their_surface`, `test_the_rules_have_one_owner`) | `232 passed`, exit **0** |
| `bin/test tests/test_a_script_says_which_interpreter_it_needs.py tests/test_a_rider_reaches_its_file.py -q` at the end | `20 passed`, exit **0** |
| `uvx ruff check` and `uvx ruff format --check`, the two changed `.py` only | exit **0** and exit **0** |
| `bin/evidence-check --reverify` | exit **0**, 6 anchors re-verified; then `bin/evidence-check` anchors: `777 ok · 0 drifted · 0 broken` |

Every mutation ran from bytes I had saved in the same script and was restored
from those bytes, never from `HEAD`; each one reports `restored
byte-identical: True`. `tests/__pycache__` was cleared between mutations.

## Re-enumeration of my own diff

The orchestrator asked whether the widened pattern has a blind spot one
construct over, the way both of its predecessors did. **It does, and there are
two.** Probed against the pattern as committed:

| Construct | Seen? |
|---|---|
| `zip(xs, f(g(y)), strict=True)` — two levels of nesting, one line | **matched** (and lost by the paste-ready rewrite, which is why it was declined) |
| A `zip(` whose `strict=` is on a later line | **blind** |
| `from datetime import UTC`, then bare `UTC` | **blind** |
| `import datetime as dt`, then `dt.UTC` | matched — this is finding 1 |

Neither blind spot exists in the tree today: the committed pattern and my AST
re-derivation return the same six files. Both are named in the pattern's own
comment, in `spec.md` §*The class, enumerated by construction*, and in the
ledger fragment's R3.

**They were not fixed, and that is the judgment rather than an oversight.**
Three text spellings have now been tried and each was blind one construct
over — the first to a nested parenthesis, the second to an import alias, the
proposed third to a deeper nesting. That is the 3+ Fix Rule's signal: the
architecture is talking, and what it says is that a text pattern cannot
enumerate a syntactic class. The close is the AST walk R3 already names, and
an AST walk is mechanism — a fix pass does not add one. It needs a person.

**A second blind spot, in finding 3's own fix.** The widened AST case sees
every module-level statement that *calls* something. It cannot see a
module-level statement that does work without a call, and it deliberately
skips `Import`; an `ImportFrom` placed above the guard would execute a module
and go unseen for the same reason `Import` does. That exemption is the guard
block's stated design — it sits after the imports on purpose — so this is the
check matching the design rather than missing something, but it is the edge a
next round should not have to rediscover.

## What is open, and who answers it

| Item | Who must answer |
|---|---|
| **`tests/test_a_record_states_what_the_tree_has.py::test_this_repositorys_own_records_state_nothing_the_tree_lacks` fails**, on three lines of round 1's own records: `rounds/round-1.md:23`, `rounds/round-1-report.md:38`, `rounds/round-1-asked.md:5`, each naming `py_compile`. Proven to predate this fix pass — those three files are byte-identical between `2b8a50a` and `fb45bc1`, and `py_compile` appears nowhere outside `seal/` at either commit. Not corrected here because a round record is written by the session that verified it, and a fix pass overwriting a reviewer's prose is what `close` refuses rows for. The remedy the checker names is one edit: `NAME NOT IN TREE` on each of the three lines | the orchestrator |
| The full suite, the repository-wide `ruff check` and the typecheck — `unverified`. `skills/agent-contract/SKILL.md` §2 reserves the broad gate. What was run is the table above: seven modules, narrowly | the orchestrator |
| Closing the pattern's two remaining blind spots with an AST walk, per the re-enumeration above. Mechanism, so not a fix pass's to add | the repository owner |
| Giving `load` a sentence instead of a `FileNotFoundError` traceback when the sibling checker is missing. Carried as a `# RIDER:` at the function, stamped `2026-09-08 at cedc58e` | whoever next opens `round_record.py#load` |

Nothing in the prompt asked for a check §2 excludes, so there is no declined
instruction to name.
