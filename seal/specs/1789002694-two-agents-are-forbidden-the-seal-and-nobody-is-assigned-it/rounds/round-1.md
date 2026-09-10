# 1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it — review round 1

| Field | Value |
|---|---|
| Target SHA | 610eb7d |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 332 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | seal_record → round-1-report.md, round-1.md, gate |
| New units | quote (depth 1); SUMMARY_WORDS (depth 1); SEAL_VOCABULARY (depth 1); SEAL_VOCABULARY_SPAN (depth 1); test_a_scale_that_is_not_a_number_is_refused_before_anything_runs (depth 1); test_the_failure_form_lines_up_the_widest_check_name (depth 1); test_the_disc_draws_the_same_bytes_in_every_process (depth 1); CHECKED_BY (depth 1); test_the_gate_names_the_row_it_sealed_over (depth 1); test_the_suite_row_reads_pytests_counts_and_not_a_linters (depth 1); test_a_failing_file_the_base_lacks_does_not_cost_the_others_their_verdict (depth 1); fixed_but_unread_item (depth 1); test_seal_refuses_while_the_fixes_have_been_read_by_nobody (depth 1); test_the_capped_run_still_seals_beside_the_third_refusal (depth 1); test_the_panel_reports_the_rows_exit_code_and_asserts_no_linter (depth 1); test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed (depth 1); test_the_runner_behind_the_wrapper_says_the_same_thing (depth 1) |
| Needs a fix | yes — 🔴 1 and 🔴 2, and 🟡 3 through 🟡 10 |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of #30 at `610eb7d`, the whole branch `feat/30-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it` against `release/v0.10.0` (48 files, +4,606 / −113), draft pull request #332. The change claims `spec.md` S1–S8. Three classes to enumerate for this change. First, an agent that judges: the sealer's whole design is that it judges nothing, so look for any path where it forms an opinion — a failure it interprets, a `new` / `failing on base too` it decides rather than reports, a check whose exit code it reads as anything but non-zero-means-not-sealed. Second, a seal taken over nothing: `verify`'s counterfeit rule applied to this work item's own product — a `Broad gate` row whose command exits 0 without reading a file, a check whose refusal is indistinguishable from its pass, a stamp printed beside numbers that did not come from the run it claims. Third, a rule stated in more than one place: this branch moved the suite's ownership through nine documents and settled what `seal` means across seven more, and §12 is the rule the branch itself found `survivor-check` cannot reach — the removed refusal was enumerated in six places and the check saw one. In this order: `skills/verify/scripts/broad_gate.py`, and first its base comparison (a scratch worktree it creates and removes, on a range it derives from a failing command's output) and its row reader; `skills/verify/scripts/seal_stamp.py`, where the disc is computed rather than drawn and the twin has to match it in both dimensions on a console that cannot render blocks; `round_record.py seal`, whose gate this branch changed from `Needs a fix` to `Pass` after finding its own two items disagreed — judge that change as code, not as a fix; `agents/sealer.md` against the three definitions beside it, and the two definitions this branch rewrote; then the seven documents that name the owner and the rule about whose seal is whose; then the ledger fragment's ten rows at their coordinates; and last the numbers in `changelog.md` and the pull request body. Facts handed over as executed by the orchestrator at `610eb7d`: ten modules 436 passed; `evidence-check .` unscoped 1,093 ok · 0 drifted · 0 broken; `survivor-check` over both the phase range and the branch range, `rider_check` exit 0; ruff clean; `broad_gate.py` refuses exit 2 with no repository and exit 2 with no row, and the refusal prints the row's form. Left to verify: everything the five phase records claim was seen red, and the capped-run repair, which phase 4 measured with a fixture and phase 5 fixed. A finding located in a record is a correction — ⬜ with the coordinate — and stays out of `Needs a fix`. Runner: `bin/test tests/<module> -q` in a `uv` venv of the clone.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | a `seal` exit that is not 2 prints the disc and returns 0 | `skills/verify/scripts/broad_gate.py:504-516` | **fixed** `1f5d0c4` | fixed at 1f5d0c4 — the gate reads every non-zero exit from `seal`, not only 2, and tells a refusal before the write from a check that failed after it; executed — `chain_check.main` returns `1 if errors else 0` at `chain_check.py:3436`; the branch reads only `2`. Fixture probe returned exit 2 with the cell already written |
| 🔴 2 | `Pass` is checked in the window before the verifying round, and `seal` writes there | `skills/code-review/scripts/round_record.py:2960-2971` | **fixed** `000ec8f` | fixed at 000ec8f — a third refusal reads `Fixes checked by`; the `Pass` refusal stays, and a capped run reading `no fixes to check` is untouched; executed — fixture: `Pass` `[x]`, `Fixes checked by` `nobody — the fixes are not yet written`, one record on disk, cell written. `skills/code-review/orchestration.md:436` calls that window red |
| 🟡 3 | the panel asserts `lint  clean` whether or not a linter ran | `skills/verify/scripts/broad_gate.py:373` | **fixed** `04a672f` | fixed at 04a672f — the panel's `lint` row states what ran rather than asserting clean; read — the row is a literal beside four rows read from output |
| 🟡 4 | one failing file absent at base labels every other one `new` | `skills/verify/scripts/broad_gate.py:315-338` | **fixed** `221b7ba` | fixed at 221b7ba — a file the base does not carry no longer makes every other one read `new`; executed — pytest exits 4 with no `FAILED` line, so `failing_files` returns `[]` |
| 🟡 5 | a linter's warning count displaces pytest's counts on the seal | `skills/verify/scripts/broad_gate.py:344-349` | **fixed** `4b9ffb7` | fixed at 4b9ffb7 — a linter's warning count no longer displaces pytest's counts; executed — `suite_counts` returned `'2 warnings'` over a combined output |
| 🟡 6 | the disc is not reproducible below scale 1.0 | `skills/verify/scripts/seal_stamp.py:186` | **fixed** `18b8e8f` | fixed at 18b8e8f — the same scale draws the same disc in every process; executed — two distinct renderings at `--scale 0.75` across five `PYTHONHASHSEED` values |
| 🟡 7 | the runner behind `bin/test` still names the orchestrator | `.github/scripts/run_tests.py:42-44` | **fixed** `29eeae7` | fixed at 29eeae7 — the runner behind `bin/test` names the sealer; read — `bin/test:23` converted, the file it execs not; no case pins the docstring |
| 🟡 8 | the third refusal in the corrected function tells the reader to run it by hand | `skills/code-review/scripts/chain_check.py:2988-2997` | **fixed** `6bd1681` | fixed at 6bd1681 — the third refusal names the spawn rather than telling the reader to run it by hand; read — three fatal refusals in `broad_gate`, two re-pointed |
| 🟡 9 | the gate never prints the row's command it sealed over | `skills/verify/scripts/broad_gate.py:469`, `agents/sealer.md:132` | **fixed** `3dcfcdd` | fixed at 3dcfcdd — the gate names the command it sealed over; read — `run` writes it to the kept file only |
| 🟡 10 | a fourth referent of `seal`, in a file the sweep's list omits | `docs/one-root-by-lifetime.md:135` | **fixed** `bce4ece` | fixed at bce4ece — a fourth referent of `seal`, and three more the hand enumeration found that the check could not; read — `tests/test_one_word_one_meaning.py:151-166` lists twelve files, not this one |

## Paste-ready fixes

```python
    if item is not None:
        code, text = seal_record(item, tree, args.base, root, args.base, keep)
        sys.stdout.write(text)
        if code != 0:
            # `seal` exits 2 on a refusal raised BEFORE the write, and it
            # returns whatever `chain_check` returned -- 1 for errors, 2 for a
            # check that could not run -- from AFTER it. Only the first of
            # those means no cell was written, and neither of them is a seal.
            sys.stderr.write(
                f"broad-gate: every check passed and `round_record.py seal` "
                f"exited {code}, so nothing is sealed. A `round-record:` line "
                "above is a refusal and no cell was written; anything else is "
                "the chain check `seal` runs after the write, and the cell may "
                "be written over a record that check still fails\n"
            )
            return 2
```
```python
    # `Pass` says nothing in the verdict table is open. It does NOT say the
    # run ended: `close` ticks the box the moment a fix table applies, and the
    # verifying round that reads those fixes has not run yet.
    # `skills/code-review/orchestration.md` §*Orchestrator: the pull request
    # opens before round 1* calls that window red and it is the window a seal
    # is spent in -- the verifying round's record becomes the last one, its
    # cell reads `not yet`, and the run has to be taken again.
    # A capped run reads `no fixes to check` here, so this costs it nothing.
    checker = reader.visible(chain.field(rows, chain.CHECKED_BY) or "").strip()
    if chain.nobody_reason(checker.strip("`").rstrip(".").lower()) is not None:
        raise Refused(
            f"round-{n}.md's `{chain.CHECKED_BY}` reads `{checker}`, so the "
            "fixes that closed its findings were opened by nobody and the "
            "verifying round is still owed. `Pass` was ticked by `close` when "
            "the fix table applied, which is one row earlier than the run "
            "ending. Spawn the verifying round first; its record is the one "
            "this cell belongs on. No cell was written"
        )
```
```python
        # NOT `("lint", "clean")`. The row is one shell command line and
        # nothing in it says which part is a linter, so `clean` over a row
        # with no linter in it is the seal asserting a check that never ran.
        # What the gate actually measured is the row's exit code.
        ("row", f"exit {checks[SUITE].code}"),
```
```python
    try:
        # A file the base does not carry makes pytest exit 4 with `no tests
        # ran` and print no FAILED line, so passing it alongside the others
        # loses the measurement for ALL of them. Asked of the base tree first.
        absent = [f for f in files if git(scratch, "cat-file", "-e", f"HEAD:{f}") is None]
        present = [f for f in files if f not in absent]
        verdicts = {f: NEW for f in absent}
        if present:
            runner = (
                f"{first_command(command)} "
                f"{' '.join(shlex.quote(f) for f in present)}"
            )
            check = run("suite-at-base", runner, scratch, keep, shell=True)
            at_base = set(failing_files(check.text))
            verdicts.update({f: (ON_BASE if f in at_base else NEW) for f in present})
        return verdicts
    finally:
        subprocess.run(
            ["git", "-C", root, "worktree", "remove", "--force", scratch],
            capture_output=True,
        )
```
```python
# pytest's summary always names one of these; a linter's `2 warnings emitted`
# matches COUNTS_RE too and stands AFTER pytest in a row joined with `&&`, so
# a backwards walk that takes the first match takes the linter's number.
SUMMARY_WORDS = ("passed", "failed", "error")


def suite_counts(text):
    for line in reversed(text.splitlines()):
        m = COUNTS_RE.search(line)
        if m and any(word in m.group(1) for word in SUMMARY_WORDS):
            return m.group(1)
    return None
```
```python
            # `max(set(ink), ...)` iterated a set of strings, whose order
            # moves with PYTHONHASHSEED, so a tie between two chart colours
            # drew differently from one process to the next. Highest count,
            # then earliest in the chart -- both stable.
            row.append(
                max(dict.fromkeys(ink), key=lambda c: (ink.count(c), -ink.index(c)))
                if ink
                else "."
            )
```
```python
The full suite takes about five minutes and is the sealer's, run once after
the review rounds settle: `skills/agent-contract/SKILL.md` forbids it to smith
and warden, and `agents/sealer.md` is the agent it is assigned to, which is
why naming one module is the ordinary use.
```
```python
def test_the_runner_behind_the_wrapper_says_the_same_thing():
    """`bin/test` is five lines and one `exec` into this file. #30 re-pointed
    the wrapper's comment from `orchestrator` to `sealer` and left the module
    it runs saying the other thing, which is one command with two owners."""
    runner = read("..", ".github", "scripts", "run_tests.py")
    assert "is the sealer's, run once after" in runner
    assert "is the orchestrator's" not in runner
```
```python
                        "— went through no broad gate at all. A broad run "
                        "with an edit after it was spent, not banked. Spawn "
                        "the `sealer` again now that the rounds have settled: "
                        "`broad-gate --base <base> --record <item>` re-takes "
                        "the run at the tree as it stands and writes the new "
                        "SHA into this cell"
```
```python
    # The first of the four conditions is to name the command before running
    # it, and the row is the only part of this run the gate did not choose.
    # `agents/sealer.md` asks the sealer to quote it, and the sealer opens no
    # repository file -- so it has to arrive here.
    sys.stderr.write(f"broad-gate: `{ROW}` says: {command}\n")
    checks[SUITE] = run(SUITE, command, root, keep, shell=True)
```
```markdown
**What the names say.** `seal/specs/<id>/` holds the spec and its process
record. `seal/ledger*` is the binding of spec to code that breaks on drift —
what the product name seals, rather than one of the seals an agent takes
(`skills/verify/SKILL.md` §*Every agent seals what it verified, and one of
them is final*).
```
```python
    ("docs", "one-root-by-lifetime.md"),
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q` | 42 passed in 13.90s; 35 test functions in the file |
| `bin/test tests/test_broad_gate_rule.py -q` | exit 0 |
| `git worktree add --detach <mkdtemp path> HEAD~1`, then `worktree remove --force` | exit 0 both ways; the directory `mkdtemp` created is accepted because it is empty, and `remove` deletes it. Same-commit-as-HEAD detached add: exit 0. A removal that does not happen leaves a `prunable` entry and the next `add` still succeeds — this axis is clean |
| `stamp(SAMPLE_ROWS, 0.75, True)` under `PYTHONHASHSEED` 0, 1, 2, 12345, 99999 | 2 distinct renderings out of 5 |
| `build()` and `stamp()` at scales 1.0, 0.9, 0.8, 0.75 | twin and block form equal in rows and in visible width at every scale (22/84, 20/81, 18/76, 17/74); `h` even at all four |
| `colour_row` over every row at scale 1.0 | 43 cells, at most 40 colour sequences in a row — under the cell count, and by three |
| `check_scale(nan)` then `stamp(..., nan, ...)` | `None`, then `ValueError: cannot convert float NaN to integer` |
| `pytest -q test_a.py test_missing.py` with `test_missing.py` absent | exit 4, `no tests ran`, `failing_files()` → `[]` |
| `suite_counts("768 passed in 30s\nwarning: 2 warnings emitted\n")` | `'2 warnings'` |
| Fixture from the module's own helpers: round 1 opened, fix landed, `close` applied a `fixed` table, no round 2; then `round_record.py seal` | `Pass` `[x]`, `Needs a fix` `yes — 🔴 1`, `Fixes checked by` `nobody — the fixes are not yet written`, one record on disk. Cell written: `de1af3e against base`. Exit 2, from the chain check that runs after the write |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A ledger coordinate whose hash is not eight hex characters is skipped in silence | `seal/specs/1789002694-…/questions.md` Q8 | the repository owner — already deferred by the branch, named here so it is not re-litigated |
| `payload-meter --agent sealer` | #292, pull request #329 | #292 — already deferred by the branch |
