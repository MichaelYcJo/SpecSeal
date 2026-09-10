# Round 2 — the ten are closed, and the fixes brought four of their own

The verifying round, at the diff of round 1's fixes `7575a1a..c045b2e`, in a
`git clone --no-local` of the repository at the branch head `a46e642`. Round
1's coordinates were carried; none of its verdicts were.

Every one of the ten `fixed` verdicts was re-derived rather than read: the fix
was reverted the way round 1's grounds describe, the case beside it was run,
and the assertion it failed on is recorded. All ten go red without the fix and
green with it. That answer is unqualified.

## What this round found, in the order one thing causes the next

**The repair for 🔴 1 widened the branch and mis-aimed the sentence beside
it.** The gate now reads every non-zero exit from `seal`, which is right, and
then tells the reader to sort the two states apart by looking for a
`round-record:` line above the message. Both states print one. In the very
fixture the branch ships for this path, the reader is told *no cell was
written* directly under a line that says `sealed`.

**The repair for 🔴 2 is the right row, read one word narrower than the row's
vocabulary.** `Fixes checked by` answers *has this run ended*, and that is the
correct third answer — a capped run still seals, verified. But the refusal
fires on `nobody` alone, so every other value the row must not hold — a name,
`pending`, an empty cell — walks past all six refusals and the cell is
written. The chain check `seal` runs after the write refuses on that same row.

Those two are the same shape as each other and as the branch's own subject: a
guard placed correctly and closed on the instance rather than the class.

**The two new units nobody had reviewed carry the same shape a third time.**
`SUMMARY_WORDS` dropped `warnings` from the list and left `errors` in it, so a
linter's count still lands on the suite row; and it now returns nothing for a
run in which every test was skipped, which the panel prints as `suite exit 0`.
`quote` can be replaced by `return path` with all 54 cases in its module still
green.

The record corrections round 1 listed were made. Two of the rows that were
corrected are wrong again, in the same way and for the same reason.

---

## 🟡 11 — the gate tells the reader no cell was written, under a line saying `sealed`

`skills/verify/scripts/broad_gate.py:570-583`.

The message the repair prints is:

> A `round-record:` line above is a refusal and no cell was written; anything
> else is the chain check `seal` runs after the write

Both endings of `seal` print a `round-record:` line. A refusal reaches stdout
as `round-record: <why>` (`skills/code-review/scripts/round_record.py:3110`);
a successful write reaches it as `round-record: sealed <path> — …`
(`round_record.py:3046`). `run` merges the child's two streams into the text
the gate writes out (`broad_gate.py:271`), so the reader sees one line either
way and the pointer does not point at anything.

Executed, driving `gate` with the branch's own stub from
`test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed` — the four lines a
reader sees, in order:

```
round-record: sealed round-2.md — `Broad gate` | abc123 against base
broad-gate: `Broad gate` says: …
broad-gate: outputs kept under …
broad-gate: every check passed and `round_record.py seal` exited 1, so nothing
is sealed. A `round-record:` line above is a refusal and no cell was written; …
```

The reader who follows that sentence concludes the record is untouched. The
cell is on disk.

**On the question the round was asked** — the two states are not
distinguishable from an exit code alone, and the widened branch does not claim
they are. Exit 1 can only come from after the write, because that is
`chain_check.main`'s `1 if errors else 0` (`chain_check.py:3438`). Exit 2 comes
from both sides: a `Refused` raised before the write, and `chain_check.main`'s
four `return 2` sites (`chain_check.py:3175`, `:3184`, `:3192`, `:3197`) after
it. So the code sorts one case and leaves the other ambiguous, and the printed
line is the whole of what a reader has for the ambiguous half. What it says is
wrong. The discriminator that works is the word `sealed`.

Two smaller things ride on the same lines. The code comment now reads *"it
returns whatever `chain_check` returned — 1 for errors — from AFTER it"*, which
drops the second exit round 1's own paste-ready text named. And the ledger
fragment records the false claim as verified behavior, which is a correction
below.

## 🟡 12 — a `Fixes checked by` nobody can read reaches the write

`skills/code-review/scripts/round_record.py:3000-3010`.

The refusal asks `chain.nobody_reason(...) is not None`, which is true for
`nobody` and its reasons and false for everything else, including everything
else the row must not hold. The docstring three screens up says *"Three
refusals, each before the write"*.

Executed, `round_record.py seal` on a record whose findings closed on a fix,
with the row set four ways:

| `Fixes checked by` | exit | cell written |
|---|---|---|
| `nobody — the fixes are not yet written` | 2 | no |
| `Nobody` | 2 | no |
| `the smith` | 1 | **yes** |
| `pending` | 1 | **yes** |
| *(empty)* | 1 | **yes** |

In each of the last three the run printed `round-record: sealed …` and then
the chain check it runs after the write refused on that exact row —
*"`Fixes checked by` is `the smith`, which is none of the three values"*. So
the subcommand writes a cell onto a record its own check will not accept, which
is the state 🔴 2 exists to prevent, reached through the value it does not read.

`reach_back` in the same file already refuses this and says why: *"a cell
nobody can read is not one to overwrite silently"* (`round_record.py:1362`).
The three-value vocabulary is `chain.CHECKER_RE`, `chain.NO_FIXES` and
`nobody` (`chain_check.py:434`, `:409`, `:410`).

Reachability, stated plainly: through `broad-gate --record` the gate's own
chain check runs before `seal` and fails on this record first, so the gate
never reaches the write. What is reachable is `round_record.py seal` invoked
directly, which is how the orchestrator and every case in the suite call it.

**On the rest of the question the round was asked.** The state the third
refusal now refuses is the window a finished run does not reach: a verifying
round's record lands on `no fixes to check`, because `landing_values` returns
that whenever no verdict is open and none closed on a fix word
(`round_record.py:1275-1279`), and a verifying round's verdicts are `answered`.
A capped run still seals — verified by reverting the refusal and watching
`test_the_capped_run_still_seals_beside_the_third_refusal` stay green while
`test_seal_refuses_while_the_fixes_have_been_read_by_nobody` goes red. The
fourth state none of the three rows sees is the one in the table above.

## 🟡 13 — the class the suite row belongs to is closed on one word of three

`skills/verify/scripts/broad_gate.py:386-395`.

`SUMMARY_WORDS` is `("passed", "failed", "error")`, and the membership test is
substring containment over the matched counts. Two things follow, both
executed:

```
suite_counts("1 passed in 1s\nFound 2 errors.\n")  -> '2 errors'
suite_counts("3 skipped in 0.10s\n")               -> None
```

The first is round 1's 🟡 5 with a different linter. `warnings` left the list
and `errors` stayed in it, and `Found 2 errors.` is what `ruff` and `mypy`
print — matched by `COUNTS_RE` and admitted by `SUMMARY_WORDS`. It needs a row
whose linter prints a count and still exits 0, which is what `--exit-zero` is
for; it is narrower than the shape round 1 measured and it is the same defect.

The second is new and needs nothing unusual. A suite in which every test was
skipped exits 0, matches no summary word, and comes back `None`, which the
panel renders as `suite exit 0` (`broad_gate.py:417`). The seal's most trusted
row then says nothing at all about a run in which nothing executed — which is
`verify`'s counterfeit, on the artifact this branch built to refuse it.

The word list is the wrong discriminator. pytest's summary is the counts
followed by the wall clock; a linter's line is not. Proposed and executed
against nine shapes, including all three the current one gets wrong.

## 🟡 14 — `quote` has no case behind either branch, and the branch it exists for is wrong

`skills/verify/scripts/broad_gate.py:313-322`.

Executed: replacing the whole body with `return path` leaves
`tests/test_the_seal_is_taken_once_by_the_sealer.py` at 54 passed. Nothing in
the suite distinguishes the unit from doing nothing, on any platform.

**The disclosure that reached this round was half right, and the half that is
wrong changes the answer.** The Windows branch is not unexercisable: CI's
matrix runs `windows-latest` on every push (`.github/workflows/test.yml:37`),
and `compare_at_base` is driven there by two cases. What the branch lacks is
not a platform, it is an assertion — the code runs on the leg it was written
for and nothing asks what it produced.

So the answer to *should a unit that cannot be exercised on the platform the
branch was built on ship* is that this one is exercised on the platform it was
written for, and the thing to ship beside it is a case that does not depend on
which platform is running. A function that reads `os.name` internally can only
be driven by the machine; a function handed the platform can be driven by a
parameter, and then a reviewer on macOS can see the Windows branch red.

The branch is also wrong. Executed:

```
quote('tests/a b.py')   nt -> '"tests/a b.py"'
quote('tests/x&y.py')   nt -> 'tests/x&y.py'
```

`subprocess.list2cmdline` builds the argv quoting `CreateProcess` reads, and
Python's own documentation says it is not `cmd.exe` quoting. `run(...,
shell=True)` on Windows goes through `cmd.exe`, where an unquoted `&` ends the
command. The docstring claims the string is *"quoted for the shell `run(…,
shell=True)` will hand it to"*, and for every `cmd.exe` metacharacter that is
false. Read, not executed — there is no Windows here.

---

## Corrections — records and messages, out of `Needs a fix`

| Where | What |
|---|---|
| `seal/ledger/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it.md:37`, row S6 | The row now claims *"every `raise Refused` in it is enumerated here"* and enumerates five. `seal` has six: the fix added the `Fixes checked by` refusal and the enumeration still omits *"round-N.md has N `Pass` boxes and needs one"*. Round 1 raised this row for counting three over five; the correction raised the claim from *refusing while …* to *every*, which turns an incomplete list into a false one |
| the same file:43, row S12 | Verified behavior states *"the gate's message tells the two apart by whether a `round-record:` line stands above it"*. Both states print one — 🟡 11 above, executed. The row records as verified the thing that is wrong |
| `skills/verify/scripts/seal_stamp.py:164-170` | `check_scale(float("nan"))` returns *"scale nan is under the floor of 0.75; below it the lily is not legible"*. NaN is not under the floor; it is not on the line at all. The new case asserts only `is not None`, so the sentence a person reads is unpinned |
| `tests/test_one_word_one_meaning.py:255-262` | The span exclusion is now written twice, once for `SEAL_OWNER` and once for `SEAL_VOCABULARY`, in four identical lines. A list of `(file, span)` pairs walked once would carry a third without a third copy |
| the same file:259-261 | `rest.partition(" ## ")[2]` returns `""` when the named section is the last `##` in its file, which silently drops everything from that heading to the end of the file out of the sweep. Bounded today — `## Naming` is lines 441 to 479 of 601 — and it now has two users, so nothing announces the day it stops being bounded |

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | a `seal` exit that is not 2 prints the disc and returns 0 | `skills/verify/scripts/broad_gate.py:565-583` | answered | executed — reverting `1f5d0c4` on the fix head returns exit 0 where 2 is asserted; `test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed` fails on `assert 0 == 2`. Closed. The sentence the repair added is 🟡 11 below |
| 🔴 2 | `Pass` is checked in the window before the verifying round, and `seal` writes there | `skills/code-review/scripts/round_record.py:2989-3010` | answered | executed — with the refusal block removed, `seal` writes the cell and exits 1; `test_seal_refuses_while_the_fixes_have_been_read_by_nobody` fails on `assert 1 == 2` while `test_the_capped_run_still_seals_beside_the_third_refusal` stays green. The row is the right one and a capped run still seals. The value it does not read is 🟡 12 below |
| 🟡 3 | the panel asserts `lint  clean` whether or not a linter ran | `skills/verify/scripts/broad_gate.py:415-425` | answered | executed — reverting `04a672f` fails `test_the_panel_reports_the_rows_exit_code_and_asserts_no_linter` and `test_a_green_tree_is_sealed_with_every_check_run_in_order` on the `row exit 0` search |
| 🟡 4 | one failing file absent at base labels every other one `new` | `skills/verify/scripts/broad_gate.py:331-380` | answered | executed — with `compare_at_base` back to one run over every failing file, `tests/test_two.py` comes back `new` where `failing on base too` is asserted; the base-shared case beside it stays green |
| 🟡 5 | a linter's warning count displaces pytest's counts on the seal | `skills/verify/scripts/broad_gate.py:386-395` | answered | executed — reverting `4b9ffb7` fails on `assert '2 warnings' == '768 passed, 1 skipped'`. Closed for `warnings`; 🟡 13 below is the same class for `errors` and for a skipped-only run |
| 🟡 6 | the disc is not reproducible below scale 1.0 | `skills/verify/scripts/seal_stamp.py:188-202` | answered | executed — reverting `18b8e8f` fails `test_the_disc_draws_the_same_bytes_in_every_process` at all three scales across five hash seeds |
| 🟡 7 | the runner behind `bin/test` still names the orchestrator | `.github/scripts/run_tests.py:42-45` | answered | executed — reverting `29eeae7` fails `test_the_runner_behind_the_wrapper_says_the_same_thing` on the missing `is the sealer's, run once after` |
| 🟡 8 | the third refusal in the corrected function tells the reader to run it by hand | `skills/code-review/scripts/chain_check.py:2992-2999` | answered | executed — reverting `6bd1681` fails the new arm of `test_a_broad_gate_spent_before_the_round_it_was_meant_to_seal_fails` on `'sealer' in out` |
| 🟡 9 | the gate never prints the row's command it sealed over | `skills/verify/scripts/broad_gate.py:525-531` | answered | executed — reverting `3dcfcdd` fails `test_the_gate_names_the_row_it_sealed_over` on the missing `` `Broad gate` says: `` |
| 🟡 10 | a fourth referent of `seal`, in a file the sweep's list omits | `docs/one-root-by-lifetime.md:135`, `tests/test_one_word_one_meaning.py:166-182` | answered | executed — reverting `bce4ece` fails `test_no_instructing_document_leaves_an_instance_anonymous` on the ledger sentence; the fixed line sits outside the `## Naming` span the new exclusion removes, so the case reaches it |
| 🟡 11 | the gate tells the reader no cell was written, under a line saying `sealed` | `skills/verify/scripts/broad_gate.py:570-583` | open | executed — driving `gate` with the branch's own stub prints `round-record: sealed …` and then a message calling a `round-record:` line a refusal with no cell written |
| 🟡 12 | a `Fixes checked by` nobody can read reaches the write | `skills/code-review/scripts/round_record.py:3000-3010` | open | executed — `the smith`, `pending` and an empty cell each exit 1 with the cell written and the post-write chain check refusing that row; `nobody` and `Nobody` exit 2 with nothing written |
| 🟡 13 | a linter's error count still lands on the suite row, and an all-skipped run reports `exit 0` | `skills/verify/scripts/broad_gate.py:386-395` | open | executed — `suite_counts("1 passed in 1s\nFound 2 errors.\n")` is `'2 errors'`; `suite_counts("3 skipped in 0.10s\n")` is `None`, which the panel renders `exit 0` |
| 🟡 14 | `quote` has no case behind either branch, and the Windows branch does not quote for `cmd.exe` | `skills/verify/scripts/broad_gate.py:313-322` | open | executed — the body replaced by `return path` leaves 54 passed; `quote("tests/x&y.py")` under `os.name == "nt"` returns the path unescaped. The `cmd.exe` half is read, not executed |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_one_word_one_meaning.py tests/test_the_suite_has_a_command_that_is_cheap_twice.py -q` at `a46e642` | 123 passed in 25.00s |
| Nine fixes reverse-applied one at a time with `git apply -R --3way` of their own commit, restricted to the source file, each followed by its case | every one red, on the assertion named in its verdict row above; tree reset between |
| 🔴 2 reverted by hand (the refusal block removed from `seal`) | `test_seal_refuses_while_the_fixes_have_been_read_by_nobody` red on `assert 1 == 2`, the cell written and the post-write chain check reporting `Pass` beside `nobody`; the capped-run case green |
| 🟡 4 reverted by hand (`compare_at_base` back to one run over every failing file) | `test_a_failing_file_the_base_lacks_does_not_cost_the_others_their_verdict` red — `tests/test_two.py  new` where `failing on base too` is asserted; `test_a_failure_the_base_shares_is_labelled_failing_on_base_too` green |
| `round_record.py seal` on a fixed-but-unread record with `Fixes checked by` set to `nobody`, `Nobody`, `the smith`, `pending` and empty | exit 2 / 2 / 1 / 1 / 1; cell written on the last three, each printing `round-record: sealed …` then the chain check refusing that row |
| `broad_gate.gate` with `seal_record` stubbed to return `(1, "round-record: sealed …")` | exit 2, no disc, and the message printed directly under the `sealed` line |
| `quote()` body replaced with `return path`, then `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q` | 54 passed |
| `quote` under `os.name` forced to `"posix"` and `"nt"` over three paths | `'tests/a b.py'` → `"tests/a b.py"` on nt; `'tests/x&y.py'` → `tests/x&y.py` on nt, unescaped |
| `suite_counts` over nine outputs, current and proposed | current: `'2 errors'` for a ruff line, `None` for `3 skipped in 0.10s`. Proposed (`COUNTS_RE` plus a wall-clock tail): `'1 passed'`, `'3 skipped'`, and `None` for `2 warnings emitted` |
| `check_scale` over `nan`, `inf`, `-1.0`, `0.5`, `1.5` | all refused; `nan` refused with the below-the-floor sentence |
| `evidence-check --strict .` unscoped, in the clone at `a46e642` | `total: 1099 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `raise Refused` sites inside `seal`, counted and listed | six; the ledger row S6 enumerates five |

Two probe files were written under `tests/`, both named `test_tmp_round2_probe.py`,
run and deleted. NAME NOT IN TREE. `git status` in the clone is clean and
`git worktree list` holds one entry.

## Paste-ready fixes

**🟡 11** — `skills/verify/scripts/broad_gate.py`, replacing the body of the
`if code != 0:` branch:

```python
        if code != 0:
            # `seal` exits 2 on a refusal raised BEFORE the write, and it
            # returns whatever `chain_check` returned from AFTER it -- 1 for
            # errors, 2 for a check that could not run. Only the first means
            # no cell was written, and neither of them is a seal.
            #
            # The exit code cannot tell the two apart, because both sides can
            # be 2, and NEITHER can the presence of a `round-record:` line:
            # a refusal prints `round-record: <why>` and a write prints
            # `round-record: sealed <path> -- …`, and `run` merges both of
            # the child's streams into the text above. The word is `sealed`.
            wrote = any(
                line.startswith("round-record: sealed") for line in text.splitlines()
            )
            sys.stderr.write(
                f"broad-gate: every check passed and `round_record.py seal` "
                f"exited {code}, so nothing is sealed. "
                + (
                    "The `round-record: sealed` line above says the cell WAS "
                    "written, and what stands under it is the chain check "
                    "`seal` runs after the write -- the cell is now on a "
                    "record that check still fails"
                    if wrote
                    else "The `round-record:` line above is a refusal raised "
                    "before the write, and no cell was written"
                )
                + "\n"
            )
            return 2
```

and, in `tests/test_the_seal_is_taken_once_by_the_sealer.py`, at the end of
`test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed`, replacing
`assert "exited 1" in out.err`:

```python
    # The stub's text is a `round-record: sealed …` line, which is what the
    # real subcommand prints when the cell WAS written. The message has to
    # read it that way round, or the reader is told the record is untouched
    # while the cell stands on it.
    assert "exited 1" in out.err, out.err
    assert "the cell WAS written" in out.err, out.err
    assert "no cell was written" not in out.err, out.err
```

**🟡 12** — `skills/code-review/scripts/round_record.py`, replacing the
condition and the refusal added for 🔴 2 (the comment above it stands):

```python
    checker = reader.visible(chain.field(rows, chain.CHECKED_BY) or "").strip()
    plain = checker.strip("`").rstrip(".").lower()
    # Every value that is NOT a later round and NOT `no fixes to check` is
    # refused, rather than `nobody` alone. The row has a three-word
    # vocabulary and the other two thirds of what it can hold -- a name, a
    # word outside the vocabulary, an empty cell -- used to reach the write,
    # and the chain check `seal` runs AFTER the write refuses on this same
    # row. `reach_back` two hundred lines up already refuses an unreadable
    # cell rather than acting on it, for the reason it states there.
    if not chain.CHECKER_RE.match(plain.removesuffix(".md")) and plain != chain.NO_FIXES:
        raise Refused(
            f"round-{n}.md's `{chain.CHECKED_BY}` reads `{checker}`, so the "
            "fixes that closed its findings have been read by no LATER round. "
            f"The row holds one of three values: `round-N`, `{chain.NO_FIXES}`, "
            f"or `{chain.NOBODY} {DASH} <why>`. `Pass` was ticked by `close` "
            "when the fix table applied, which is one row earlier than the run "
            "ending. Spawn the verifying round first; its record is the one "
            "this cell belongs on; no cell was written"
        )
```

and, in `tests/test_the_seal_is_taken_once_by_the_sealer.py`, beside
`test_seal_refuses_while_the_fixes_have_been_read_by_nobody`:

```python
@pytest.mark.parametrize("value", ["the smith", "pending", ""])
def test_seal_refuses_a_fixes_checked_by_that_is_outside_the_vocabulary(repo, value):
    """Round 2's 🟡 12. The refusal added for round 1's 🔴 2 read `nobody` and
    the row holds three values, so the other two thirds of what it can carry
    reached the write: the cell was written, `round-record: sealed …` was
    printed, and the chain check `seal` runs AFTER the write then refused on
    that very row. `reach_back` refuses an unreadable cell rather than acting
    on it, and this is the same cell one subcommand over."""
    path = fixed_but_unread_item(repo)
    text = path.read_text(encoding="utf-8")
    path.write_text(
        "\n".join(
            f"| {CHECKED_BY} | {value} |"
            if line.startswith(f"| {CHECKED_BY} |")
            else line
            for line in text.splitlines()
        )
        + "\n",
        encoding="utf-8",
    )
    before = read_bytes(path)
    code, out = run_seal(repo, f"{short(repo, 'HEAD')} against base")
    assert code == 2, out
    assert "no cell was written" in out, out
    assert read_bytes(path) == before, "the record was written under a refusal"
```

**🟡 13** — `skills/verify/scripts/broad_gate.py`, replacing `SUMMARY_WORDS`
and `suite_counts`:

```python
# pytest's summary line is the counts followed by the wall clock -- `768
# passed, 1 skipped in 12.34s`, decorated or not. Matching on the WORDS
# closed round 1's 🟡 5 on its instance and not on its class: `warnings` left
# the list and `errors` stayed in it, so `Found 2 errors.` from a linter run
# with `--exit-zero` still lands on the suite row; and a run where every test
# was SKIPPED matched no word at all and came back None, which the panel
# prints as `exit 0` -- the seal's most trusted row saying nothing about a
# run in which nothing executed. The wall clock is what pytest's summary has
# and a linter's line does not.
SUMMARY_TAIL = re.compile(r"\bin \d+(?:\.\d+)?s\b")


def suite_counts(text):
    for line in reversed(text.splitlines()):
        m = COUNTS_RE.search(line)
        if m and SUMMARY_TAIL.search(line[m.end() :]):
            return m.group(1)
    return None
```

and, in `test_the_suite_row_reads_pytests_counts_and_not_a_linters`, after the
existing assertions:

```python
    # The class, not the instance. `warnings` was the word round 1 measured;
    # `errors` is the same defect one linter over, and a skipped-only run is
    # the shape that came back with no counts at all.
    assert gate.suite_counts("1 passed in 1s\nFound 2 errors.\n") == "1 passed"
    assert gate.suite_counts("3 skipped in 0.10s\n") == "3 skipped"
    assert gate.suite_counts("768 passed in 63.21s (0:01:03)\n") == "768 passed"
```

**🟡 14** — `skills/verify/scripts/broad_gate.py`, replacing `quote`:

```python
def quote(path, windows=None):
    """One path, quoted for the shell `run(..., shell=True)` hands it to.

    `windows` is the platform, defaulting to this one, so BOTH branches can
    be driven from a case on either machine. Reading `os.name` inside the
    body left the branch that exists for Windows unreachable from the machine
    this was written on, and the whole unit could be replaced by `return
    path` with 54 cases still green -- which is `docs/flow.md` #103's class
    made out of the fix for it.

    On Windows `run(..., shell=True)` goes through `cmd.exe`, and
    `subprocess.list2cmdline` builds the argv quoting `CreateProcess` reads,
    which Python's own documentation says is NOT `cmd.exe` quoting: it wraps
    a path holding a space and leaves `& | ^ < > ( )` for the shell to act
    on. Double quotes carry both -- inside them `cmd.exe` treats none of
    those as syntax -- and a `"` cannot appear in a Windows path at all.
    """
    if windows is None:
        windows = os.name == "nt"
    return f'"{path}"' if windows else shlex.quote(path)
```

and, in `tests/test_the_seal_is_taken_once_by_the_sealer.py`:

```python
@pytest.mark.parametrize(
    "path, posix, windows",
    [
        ("tests/test_one.py", "tests/test_one.py", '"tests/test_one.py"'),
        ("tests/a b.py", "'tests/a b.py'", '"tests/a b.py"'),
        ("tests/x&y.py", "'tests/x&y.py'", '"tests/x&y.py"'),
    ],
)
def test_a_path_is_quoted_for_the_shell_of_either_platform(path, posix, windows):
    """Round 2's 🟡 14. The unit took the platform from `os.name`, so the half
    written for Windows could not be driven from the machine the branch was
    written on and no case asserted the other half either -- the body could
    be replaced by `return path` with every case green.

    `&` is the one that matters: `subprocess.list2cmdline` quotes a space and
    leaves a `cmd.exe` metacharacter bare, and `run(..., shell=True)` on
    Windows goes through `cmd.exe`."""
    gate = gate_module()
    assert gate.quote(path, windows=False) == posix
    assert gate.quote(path, windows=True) == windows
```

Needs a fix: yes — 🟡 11, 🟡 12, 🟡 13 and 🟡 14
Loses a record or crashes: no

## Proof block

Read: `rounds/round-1.md`, `rounds/round-1-report.md`, `rounds/round-1-fixes.md`,
`rounds/round-2-asked.md`; `git diff 7575a1a..c045b2e` in full;
`skills/verify/scripts/broad_gate.py`, `skills/verify/scripts/seal_stamp.py`,
`skills/code-review/scripts/round_record.py`,
`skills/code-review/scripts/chain_check.py`,
`tests/test_the_seal_is_taken_once_by_the_sealer.py`,
`tests/test_one_word_one_meaning.py`,
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py`,
`tests/test_chain_check_at_the_pull_request.py`, `bin/test`, `bin/seal`,
`bin/broad-gate`, `.github/workflows/test.yml`, `docs/one-root-by-lifetime.md`,
`seal/ledger/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it.md`,
`seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/changelog.md`,
`seal/config.md`.

Executed: the twelve runs in the probes table above, all in a
`git clone --no-local` at `a46e642` with a `uv` venv, `pytest 9.1.1` on Python
3.13.9, macOS.

Unverified, and who answers it: the full suite, the repository-wide lint and
the typecheck were not run — `skills/agent-contract/SKILL.md` §2 reserves them
for the sealer, and this work item is what gives that run an owner. The
`cmd.exe` half of 🟡 14 was read and not executed; CI's `windows-latest` leg
answers it. `survivor-check` over the branch range and `ruff` were handed over
as executed by the orchestrator and were not re-run here.
