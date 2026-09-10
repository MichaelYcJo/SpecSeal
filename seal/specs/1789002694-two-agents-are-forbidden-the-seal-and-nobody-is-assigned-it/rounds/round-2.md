# 1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it — review round 2

| Field | Value |
|---|---|
| Target SHA | a46e642 |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 332 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | quote → main, round-1-report.md, round-1.md, round-2-asked.md, round-2-report.md, round-2.md, quote, compare_at_base, pytest |
| New units | SCALE_NOT_A_NUMBER (depth 1); SEAL_EXCLUDED (depth 1); test_a_path_is_quoted_for_the_shell_of_either_platform (depth 1); set_checked_by (depth 1); test_seal_refuses_a_fixes_checked_by_that_is_outside_the_vocabulary (depth 1); test_the_refusal_names_the_three_values_the_row_holds (depth 1) |
| Needs a fix | yes — 🟡 11, 🟡 12, 🟡 13 and 🟡 14 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of #30 is the verifying round, at the diff of round 1's fixes, `7575a1a..c045b2e` (twelve commits), not the branch. Its job is the answers: for each of the ten `fixed` verdicts in `rounds/round-1.md`, is it actually closed — re-derive by reverting the fix the way round 1's grounds describe and saying which case goes red, rather than by reading the diff. Two of them need more than that. 🔴 1's repair widened what the gate reads from `seal`'s exit codes, and the question is whether the two states it now tells apart — a refusal raised before the write and a check that failed after it — are actually distinguishable from the exit code alone. 🔴 2 added a third refusal reading `Fixes checked by`, which is this branch's THIRD answer to the question of which row is the trigger: `Needs a fix` was built and phase 4 measured it wrong for a capped run, `Pass` replaced it in phase 5 and round 1 found it fires a round early, and this is the third — so judge it as code, ask what state it now refuses that a finished run reaches, and confirm a capped run still seals. The other surface is new rather than fixed: the units round 1's record names under `New units`, which nobody has reviewed — `quote`, `SUMMARY_WORDS`, `SEAL_VOCABULARY`, `SEAL_VOCABULARY_SPAN` and the cases beside them. The fix pass disclosed that `quote()` has nothing behind it on macOS: deleting its body left all cases green, because the Windows branch is unreachable there. That is `docs/flow.md`'s #103 class, and the question for this round is whether a unit that cannot be exercised on the platform the branch was built on should ship with a case that says so. This round is NOT bounded by the reopening rule yet — the run has spent no reopening — so anything it opens is a fix to commission in the ordinary way. Facts handed over as executed by the orchestrator at the fix head: eight modules 261 passed; `evidence-check .` unscoped 1,099 ok · 0 drifted · 0 broken; `survivor-check` over the branch range exit 0; ruff clean; the gate's exit branch reads `code != 0` and the record carries three refusals among fifty-six. Left to verify: every red the fix pass claims, and the four new units. A finding located in a record is a correction — ⬜ with the coordinate — and stays out of `Needs a fix`. Runner: `bin/test tests/<module> -q` in a `uv` venv of the clone. <!-- NAME NOT IN TREE: round 2's own finding is what removed these. `SUMMARY_WORDS` became `SUMMARY_TAIL` (🟡 13) and `SEAL_VOCABULARY` / `SEAL_VOCABULARY_SPAN` became the `SEAL_EXCLUDED` pairs (a round 2 correction). The names are kept as the round read them. -->

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
| 🟡 11 | the gate tells the reader no cell was written, under a line saying `sealed` | `skills/verify/scripts/broad_gate.py:570-583` | **fixed** `5a20202` | fixed at 5a20202 — the two states are told apart by a discriminator the message carries, not by the exit code, and the refusal names which side it is on; executed — driving `gate` with the branch's own stub prints `round-record: sealed …` and then a message calling a `round-record:` line a refusal with no cell written |
| 🟡 12 | a `Fixes checked by` nobody can read reaches the write | `skills/code-review/scripts/round_record.py:3000-3010` | **fixed** `0cbd6ad` | fixed at 0cbd6ad — the third refusal reads the row's whole vocabulary rather than `nobody` alone, and names all three values in its message; executed — `the smith`, `pending` and an empty cell each exit 1 with the cell written and the post-write chain check refusing that row; `nobody` and `Nobody` exit 2 with nothing written |
| 🟡 13 | a linter's error count still lands on the suite row, and an all-skipped run reports `exit 0` | `skills/verify/scripts/broad_gate.py:386-395` | **fixed** `bd08f52` | fixed at bd08f52 — the suite row is read on an axis that is not a word list, so a linter's error count and an all-skipped run both stop landing on it; executed — `suite_counts("1 passed in 1s\nFound 2 errors.\n")` is `'2 errors'`; `suite_counts("3 skipped in 0.10s\n")` is `None`, which the panel renders `exit 0` |
| 🟡 14 | `quote` has no case behind either branch, and the Windows branch does not quote for `cmd.exe` | `skills/verify/scripts/broad_gate.py:313-322` | **fixed** `67cdbda` | fixed at 67cdbda — the unit takes the platform as an argument so a case can turn it red on any machine, the quoting is `cmd.exe`'s rather than `CreateProcess`'s, and the residual it does not close is named in the docstring; executed — the body replaced by `return path` leaves 54 passed; `quote("tests/x&y.py")` under `os.name == "nt"` returns the path unescaped. The `cmd.exe` half is read, not executed |

## Paste-ready fixes

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
```python
    # The stub's text is a `round-record: sealed …` line, which is what the
    # real subcommand prints when the cell WAS written. The message has to
    # read it that way round, or the reader is told the record is untouched
    # while the cell stands on it.
    assert "exited 1" in out.err, out.err
    assert "the cell WAS written" in out.err, out.err
    assert "no cell was written" not in out.err, out.err
```
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
```python
    # The class, not the instance. `warnings` was the word round 1 measured;
    # `errors` is the same defect one linter over, and a skipped-only run is
    # the shape that came back with no counts at all.
    assert gate.suite_counts("1 passed in 1s\nFound 2 errors.\n") == "1 passed"
    assert gate.suite_counts("3 skipped in 0.10s\n") == "3 skipped"
    assert gate.suite_counts("768 passed in 63.21s (0:01:03)\n") == "768 passed"
```
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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/broad_gate.py:504-516` | round 1's 🔴 1 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2960-2971` | round 1's 🔴 2 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:373` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:315-338` | round 1's 🟡 4 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:344-349` | round 1's 🟡 5 — fixed |
| round-1 | `skills/verify/scripts/seal_stamp.py:186` | round 1's 🟡 6 — fixed |
| round-1 | `.github/scripts/run_tests.py:42-44` | round 1's 🟡 7 — fixed |
| round-1 | `skills/code-review/scripts/chain_check.py:2988-2997` | round 1's 🟡 8 — fixed |
| round-1 | `skills/verify/scripts/broad_gate.py:469`, `agents/sealer.md:132` | round 1's 🟡 9 — fixed |
| round-1 | `docs/one-root-by-lifetime.md:135` | round 1's 🟡 10 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
