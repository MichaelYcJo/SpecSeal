# 1788936260-a-case-pins-what-it-actually-measures — review round 3 (report)

| Field | Value |
|---|---|
| Target SHA | 0cfc5e6 |
| Diff reviewed | `0c93614..984d585` — round 2's fixes and nothing else |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 311 |
| Broad gate | **not yet, and it is now due** — the rounds settle at this record. `unverified`, answered by the review orchestrator (contract §2) |
| Fixes checked by | this round; the run is capped here |
| Contract changes | none — I wrote no code |
| New units | none — I wrote no code |

Round 2's three fixed verdicts are closed and its two answered ones hold.
Four things this round opens, and by the run's cap each is an issue rather
than a fix pass. None of them stops the merge.

## What this round found, in causal order

### The guard round 2 installed refuses the wrong class, and two values it lets past end the run in a traceback

Round 2's finding 17 asked for `--timeout -1` to be refused, and it is:
exit 2, the reason on stderr, the module untouched. What the guard tests is
`args.timeout < 0`, and the class is not *negative* — it is *not a usable
number of seconds*. `type=float` accepts three values that are not one, and
the guard catches one of them.

`nan` and `inf` are not negative, so both reach `subprocess.run`. The
selector then computes `math.ceil(timeout * 1e3)`, which raises `ValueError`
for `nan` and `OverflowError` for `inf`. The arm loop catches
`subprocess.TimeoutExpired` and `OSError` and neither of these is either, so
both escape `run_arms`, `_report` is never reached, and the tool exits 1 with
a traceback. That is the shape round 1 recorded as its floor breach, arriving
through a value the guard was written to close a sibling of.

`inf` is the reachable half. The help says `0` removes the bound; a reader
who did not reach the help types the word that means the same thing
everywhere else. Executed through the command line at the target, exit codes
read directly:

| Value | Exit | What a person sees |
|---|---|---|
| `-1` | 2 | the refusal, and the module untouched |
| `0` | 0 | unbounded, both arms measured |
| `1e-9` | 0 | `0 arms measured`, both arms in the no-verdict list — honest |
| `nan` | **1** | `ValueError: cannot convert float NaN to integer` |
| `inf` | **1** | `OverflowError: cannot convert float infinity to integer` |
| `1e400` | **1** | the same `OverflowError` — it parses to `inf` |

Nothing is lost on that path. The outer `finally` in `run_arms` restores the
module, and `git status --porcelain` in the clone was empty after every
value. The cost is a traceback where round 2 installed a usage error, and one
retype.

The small-positive decision the fix pass defended holds, and `1e-9` above is
the measurement: the run reports `0 arms measured · 0 killed · 0 watched by
no case` and puts both arms in the no-verdict list with the bound quoted.
That output is honest, which is what makes refusing it unnecessary. It is
also why the refusal message's stated reason does not distinguish the values
it refuses from the ones it accepts — *the run prints a survivor count of
zero it never measured* is equally true of `1e-9`. The reason that does
distinguish them is in the comment, not in the message, and the fix below
puts it in both.

### The no-verdict header sends the reader to the reasons, and no reason answers

This is the half of round 2's finding 15 that did not land. The header now
reads:

```
2 arms with no verdict from any operator — the reason beside each says
whether it was ever mutated:
```

The distinction was moved out of the label and into the reason. The reason
strings were not changed, so nothing beside any arm says it. Executed on all
three doors at the target, and these are the reasons printed verbatim:

| Door | Was the mutation written? | The reason a person reads |
|---|---|---|
| every pair times out | **yes** — written, run, restored | `TimeoutExpired: the command did not return within 0.3s, so this arm was not measured` |
| the command cannot be spawned | **yes** — written and restored | `FileNotFoundError: [Errno 2] No such file or directory: '…'` |
| a bare `except:` | **no** — `mutate` raises first | `NoMutationDefined: h:4: a bare \`except:\` catches everything, …` |

None of the three says whether the arm was mutated. The timeout reason says
*not measured*, which is the other question. The spawn failure says nothing
at all. The refusal says nothing at all. A reader who takes the header at its
word and looks at the reason has to already know that `NoMutationDefined` and
`SyntaxError` are raised before the write and that `TimeoutExpired` and the
errnos are raised after it — which is the knowledge the header exists to
spare them.

The mixed row makes the promise ill-formed rather than merely unkept. On the
timed-out door one arm printed both doors at once, joined:

```
g:10  ExceptHandler  ValueError
    invert: NoMutationDefined: g:10: this handler has one type left, … |
    remove: TimeoutExpired: the command did not return within 0.3s, …
```

For that arm the honest answer to *was it ever mutated* is *by one operator*,
and there is no wording in the report that conveys it.

The `operator/arm pairs with no verdict` section has the same gap and no
disclosure clause at all — a pair listed there was mutated when the reason is
`TimeoutExpired` and was not when it is `SyntaxError`, and its header does
not raise the question.

The four labels themselves are right, and every path I could construct
reaches the correct one: the per-arm `no verdict` line, `N arms measured`,
`N operator/arm pairs with no verdict` and `N arms with no verdict from any
operator`. What is missing is the content the fourth label now points at.

### The document that prescribes the hazardous command says nothing about the bound

Round 2's finding 16 corrected the claim in three places — `run_arms`'
docstring, the `--timeout` help, and the changelog fragment — and all three
now agree, verified by reading. `skills/verify/SKILL.md` is the fourth
carrier and the only one a user reads before typing anything, and it is the
place the wrapper form is prescribed:

```
arm-check hooks/review-history-guard.py --tests "bin/test tests/test_chain_hooks.py -q"
```

That is exactly the form finding 16 measured: `bin/test` execs
`.github/scripts/run_tests.py`, which runs pytest through `subprocess.run`,
so the bound reaches one process above the suite. The skill never mentions
`--timeout`, the 900-second default, or that a timed-out pair leaves a whole
suite running. `arm-check` appears in five files in the tree and this is the
only document among them.

Whether the bound *should* reach a process group is #313 and stays there.
Telling the reader what it does not reach is the half round 2 recorded as
owed either way, and it did not reach the document.

### `Verdict`'s docstring still defines both fields as the never-tried case

`skills/verify/scripts/arm_check.py:674` and `:679`, untouched by this diff:

> the distinction between *no case watches this* and *this was never tried*
> is the whole reason `refused` exists.
>
> … an arm ANOTHER operator could be applied to is not refused as a whole,
> and its **un-asked** operator was invisible until this field existed

Both sentences are what round 2's finding 15 corrected one function over.
`refused` now exists for two distinctions, so *the whole reason* is false,
and `not_applicable` now holds pairs that were asked and answered nothing, so
*un-asked operator* is the reading the report was corrected away from. This
is the docstring that defines what `by_operator` and `not_applicable` mean,
so it is where the next maintainer learns the wrong thing.

`survivor_check.py` did not report it — the sentences it matched on were
longer — and `survivors.md` does not excuse it. The class was enumerated
across the printed output and stopped at the module boundary of `_report`.
The comment at `:846`, *so it goes where the un-asked pairs go*, is the same
instance inside `run_arms` and the fix below takes both.

### Three corrections under the work item's own records

**The report says *so it is not refused* and prints no label a reader can
find.** `arm_check.py:977`. The `refused` list's header became *arms with no
verdict from any operator*, and the word `refused` now appears nowhere in the
output — so a reader told an arm *is not refused* has no category to place it
outside of. The sentence is still true internally; it points at a name the
report stopped printing.

**`survivors.md`'s fifth grounds cell credits the exempted case with an
assertion it does not make.** `survivors.md:50` says of
`test_an_operator_that_could_not_be_asked_of_an_arm_is_named`: *The section
header it reads is asserted through `operator/arm pairs with no verdict`*.
That case never calls `_report`; it asserts on `refused[0]`'s reason string.
The case that asserts the header, and that asserts the header does not say
*not asked*, is
`test_a_partly_skipped_operator_is_reported_without_refusing_the_arm` — which
the cell calls *a sibling case* doing only the second half. The exemption
itself is sound: the quote is the case's name, its arm is a match pattern
with no mutation for either operator, and nothing is written on that path.
What is wrong is the sentence a future reader would use to re-test the
exemption.

The other four exemptions hold, checked one at a time against the code each
describes. All five sit on the door where `mutate` raises before the write —
`mutate`'s own docstring; the bare-`except:` case;
`phase-3.md`'s *either*, whose two clauses are the match pattern and the bare
`except:`; and `phase-3.md`'s `gh_segments:176` passage, whose `remove`
mutation was a `SyntaxError`. `mutate` calls `ast.parse` on the mutated
source before returning, so a `SyntaxError` is raised before anything is
written — which is what makes *could not be asked* exact for that one.

**The recount says which number is which, and carries no date and no
command.** `overview.md:6` and `handoff.md:92`, both now *47 cases … 58
collected counting the two parametrized ones' arms, counted after round 2's
fixes*. I measured 47 `^def test_` and 58 collected at the target, and the
arithmetic is consistent: 47 functions, one parametrized eleven ways and one
two ways, gives 47 + 10 + 1 = 58.

Read as a class rather than as a number, the sentence closes the failure mode
that produced both earlier errors. Both were the two numbers conflated — 26
against 35, then 51 against 53 — and the sentence now states the relationship
between them, so the next reader can check one against the other instead of
guessing which was meant.

What it does not carry is a date or the command that takes it. Round 1's
finding 5 closed the same class in `skills/verify/SKILL.md` with a dated
column header, a disclaimer naming the number a measurement, and a case
pinning both sentences; here there is none of the three. *After round 2's
fixes* is locatable through `rounds/round-2.md`, which is better than a bare
number and weaker than a date — and it is weaker than what round 2's own
paste-ready text proposed, which anchored the count to `33be6ca`. So: the
class is narrowed, not closed, and a third wrong value would now be
detectable rather than invisible.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 15 | The timeout and `OSError` paths route a mutated arm into a list the report called *enumerated and not mutated* | `skills/verify/scripts/arm_check.py:993` | answered | Closed at `b9a1af7` for the labels. Executed: all four labels print correctly on all three doors, and the per-arm line reads `no verdict`. The header's own promise about the reasons is not kept — finding 21 |
| 16 | The bound bounds the wait and not the work, and a per-command bound was called a per-arm one | `skills/verify/scripts/arm_check.py:788` | answered | Closed at `22fc414`. Read: the docstring, the `--timeout` help and `changelog.md:40` all now say *the wait, not the work*, *only the command's own process*, and *two operators, so twice the bound*. The fourth carrier, the document that prescribes the wrapper form, says nothing — finding 22 |
| 17 | `--timeout` accepted a negative and a whole run then reported a survivor count of zero at exit 0 | `skills/verify/scripts/arm_check.py:1040` | answered | Closed at `4243149` for the negative. Executed: `-1` exits 2 with the reason on stderr and the module untouched; `-inf` exits 2 from argparse's own option parsing. The guard tests `< 0` rather than the class — finding 20 |
| 18 | `overview.md` stated a collected-case count the tree did not have | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:6` | answered | Corrected at `984d585`. Executed: 47 `^def test_` and 58 collected at the target, and the two numbers' stated relationship is arithmetically consistent. The class is narrowed rather than closed — finding 26 |
| 19 | `handoff.md` stated the pre-fix `invert` number in the present tense with no dated note | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/handoff.md:86` | answered | Corrected at `984d585`. Read: the addendum is dated 2026-09-09, names the relabelled first line, and says why the argument the paragraph makes is unchanged. It carries the recount, which is finding 26's second coordinate |
| 20 | 🟡 `--timeout nan` and `--timeout inf` are accepted, escape the arm loop as `ValueError` and `OverflowError`, and end the run in a traceback at exit 1 | `skills/verify/scripts/arm_check.py:1040` | open | Executed through the command line at `0cfc5e6`, exit codes read directly: `nan` and `inf` and `1e400` each exit 1 with the selector's traceback; `-1` exits 2. `type=float` accepts three non-real values and `< 0` catches one. Module restored and the clone clean on every value. Round 2's finding 17's class, enumerated as *negative* instead of *not a usable number of seconds* |
| 21 | 🟡 The no-verdict header says *the reason beside each says whether it was ever mutated*, and none of the three reason strings says it | `skills/verify/scripts/arm_check.py:993` | open | Executed on all three doors: the timeout reason says *not measured*, the `OSError` reason and the `NoMutationDefined` reason say nothing about the write. §14 — the fix moved the distinction into the reason and did not change any reason. The mixed row prints both doors joined under a singular claim, and the `operator/arm pairs` header has the same gap with no clause at all |
| 22 | 🟡 `skills/verify/SKILL.md` prescribes the `--tests "bin/test …"` form and never mentions `--timeout`, the 900-second default, or what the bound does not reach | `skills/verify/SKILL.md:68` | open | Read: `arm-check` appears in five files and this is the only document; `grep -n timeout` over the skill returns nothing in that section. Finding 16's class, fourth carrier — the three that state the claim were corrected and the one that prescribes the command was not. #313 owns whether the bound should reach a process group; this is the disclosure round 2 recorded as owed either way |
| 23 | 🟡 `Verdict`'s docstring still calls *this was never tried* the whole reason `refused` exists and calls `not_applicable`'s contents the *un-asked* operator | `skills/verify/scripts/arm_check.py:674` | open | Read: untouched by this diff, and both sentences are what finding 15 corrected in `_report`. `refused` now holds two outcomes and `not_applicable` holds asked-and-unanswered pairs. `survivor_check.py` did not report it and `survivors.md` does not excuse it — §12, the class stopped at `_report`'s boundary. `run_arms`' comment at `:846` is the same instance |
| 24 | ⬜ The report tells a reader an arm *is not refused* and prints no label called refused anywhere | `skills/verify/scripts/arm_check.py:977` | open | Read: `refused` survives as a variable name and as this one clause; every printed label became *no verdict*. The sentence stays true internally and points the reader at a category the output no longer has |
| 25 | ⬜ `survivors.md`'s fifth grounds cell credits the exempted case with a section-header assertion it does not make | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/survivors.md:50` | open | Executed and read: `test_an_operator_that_could_not_be_asked_of_an_arm_is_named` never calls `_report` and asserts on `refused[0]`'s reason; the header and the *not asked* absence are both asserted by `test_a_partly_skipped_operator_is_reported_without_refusing_the_arm`. The exemption holds — the door is the one where nothing is written — and the grounds sentence a future reader would re-test it with does not |
| 26 | ⬜ The recount carries no date and no command, and its anchor is a phrase rather than the SHA round 2's own fix text proposed | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:6` | open | Executed: 47 and 58 are correct at the target and their stated relationship checks out. The class that produced both earlier errors — the two numbers conflated — is closed by the sentence now saying which is which. What is absent is a date, the command, and any case; round 2's paste-ready text said *collected at `33be6ca`* and the applied text says *after round 2's fixes* |
| 27 | 🟢 Every path reaches the right one of the four labels | `skills/verify/scripts/arm_check.py:933` | answered | Executed: the all-timed-out door, the unspawnable door, the never-mutated door and the mixed one-measured-one-timed-out arm. Per-arm `no verdict`, `N arms measured`, `N operator/arm pairs with no verdict`, `N arms with no verdict from any operator`. `refused` arms never reach the pairs list, so nothing is counted twice, and the arm total equals measured plus no-verdict on every door |
| 28 | 🟢 The deliberate non-refusal of a small positive bound is honest output | `skills/verify/scripts/arm_check.py:1040` | answered | Executed: `--timeout 1e-9` gives exit 0, `0 arms measured · 0 killed · 0 watched by no case`, both arms in the no-verdict list with the bound quoted in each reason. Nothing reads as a clean sweep, which is what makes the asymmetry with the refused values defensible on grounds and not only on judgement |
| 29 | 🟢 The docstring, the help and the changelog fragment say the same thing | `skills/verify/scripts/arm_check.py:788` | answered | Read all three side by side: the wait rather than the work, the direct child only, two operators so twice the bound. The asymmetry in pinning is sound — the help is output and `test_the_help_says_the_bound_reaches_the_command_and_not_its_children` pins it whole-clause and whitespace-collapsed, where a docstring is not a rendered line and §14 does not reach it. The changelog fragment adds *a negative is refused*, which neither of the other two carries; that is a gap in the help's favour rather than a disagreement |
| 30 | 🟢 All five survivor exemptions sit on the door where nothing is written | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/survivors.md:44` | answered | Read each quote against its code: `mutate`'s docstring, whose raise precedes the write; the bare-`except:` case, both of whose arms `mutate` refuses; `phase-3.md`'s *either*, resolved by the two clauses before it; `phase-3.md`'s `gh_segments:176`, whose `remove` mutation was a `SyntaxError`, and `mutate` calls `ast.parse` before returning so nothing was written; and the fifth case's arm, a match pattern with no mutation for either operator. *Never tried* and *could not be asked* are exact in all five. One grounds cell misdescribes a case — finding 25 |
| 31 | 🟢 The four new units are correct, and the patching style follows the file's own precedent | `tests/test_arm_check.py:1035` | answered | Executed: 86 passed, exit 0, on `tests/test_arm_check.py` and `tests/test_a_segment_feeds_the_flow_log.py` in a clone at the target. `NO_VERDICT_COMMANDS` drives both mutated doors and its case asserts the module's hash is back before it reads the report, which is the premise. Read: the global `ARM.subprocess.run` assignment with a `finally` restore is the file's existing convention at two other cases, so the new one adds no hazard the file did not already carry |
| 32 | 🟢 `Contract changes: none` is true | `skills/verify/scripts/arm_check.py:773` | answered | Read: `run_arms`, `_report` and `main` all keep their signatures; the diff touches `run_arms`' docstring, one comment and one echo string inside its body, four echo strings and three comments inside `_report`, and the help text plus a new guard inside `main`. The only new module-level unit is `NO_VERDICT_COMMANDS` in the test file. A body is not a unit added, and the claim survives that reading |
| 33 | 🟢 This branch falsifies no ledger row elsewhere, and no removed wording still stands unexcused | `seal/ledger.md` | answered | Executed in the clone at the target, exit code read directly: `evidence_check.py .` unscoped, exit 0, `total: 1063 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, `652 names read · 0 refused`. Carried, not re-derived: the orchestrator's `survivor-check` clean on `0c93614..984d585` with the five excused on the pre-`survivors.md` range |

## Paste-ready fixes

### Finding 20 — refuse the class, not the sign

```python
import argparse
import ast
import hashlib
import math
import os
```

```python
    if not math.isfinite(args.timeout) or args.timeout < 0:
        # `0` removes the bound, and `-1` is how several tools spell the same
        # intention. Passed through, `subprocess.run` raises `TimeoutExpired`
        # before the command starts, so every pair of every arm is recorded
        # as unmeasured and the run prints a perfect score for a measurement
        # nobody took.
        #
        # `nan` and `inf` are the same class, and `type=float` accepts both.
        # Neither is negative, so a `< 0` test lets them through, and
        # `selectors` then computes `math.ceil(timeout * 1e3)` and raises
        # `ValueError` for `nan`, `OverflowError` for `inf` -- neither of
        # which the arm loop catches, so the run dies with a traceback at
        # exit 1 and `_report` is never reached. `inf` is also what a reader
        # who did not get as far as the help types to mean what `0` means
        # here. The class is *not a usable number of seconds*, never
        # *negative*.
        #
        # A tiny positive is NOT refused, and that is the line: `0.001`
        # produces `0 arms measured` with the bound quoted beside every arm,
        # which is honest output. These three produce a perfect score or a
        # traceback.
        parser.error(
            "--timeout takes a finite, non-negative number of seconds, and 0 "
            "removes the bound. A negative value times every command out "
            "before it starts, so every arm is recorded as unmeasured and the "
            "run prints a survivor count of zero it never measured; `nan` and "
            "`inf` are accepted by `float` and reach the selector, which ends "
            "the run in a traceback."
        )
```

Parametrise the existing case rather than adding a second one — the cause is
one, and the three values are its instances:

```python
@pytest.mark.parametrize("value", ["-1", "nan", "inf"])
def test_a_bound_that_is_not_a_number_of_seconds_is_refused(two_arms, capsys, value):
    """Round 2's finding 17 and round 3's finding 20, which are one class.

    `type=float` accepts three values that are not a number of seconds. A
    negative times every command out before it starts: every pair of every
    arm unmeasured, exit 0, and a survivor count of zero. `nan` and `inf`
    are not negative, so a `< 0` guard lets them past, and `selectors` then
    computes `math.ceil(timeout * 1e3)` and raises `ValueError` for `nan`,
    `OverflowError` for `inf` -- neither caught by the arm loop, so the run
    ends in a traceback at exit 1 with `_report` never reached. `0` is
    documented as removing the bound and `inf` is how the same intention is
    spelled elsewhere.

    A tiny positive bound is NOT refused, and that is deliberate: `0.001` is
    a legitimate thing to type against a fast command, and finding 15's
    labels are what make its output readable.

    Red how: `if args.timeout < 0` restored gives exit 1 and a traceback for
    `nan` and `inf`; the guard deleted gives exit 0 and `0 arms measured`
    for all three. Both measured through `main`. Executed."""
    module_path, tests = two_arms
    with pytest.raises(SystemExit) as exit_code:
        ARM.main([str(module_path), "--tests", shlex.join(tests), "--timeout", value])
    assert exit_code.value.code == 2, "argparse's own usage-error exit"
    printed = capsys.readouterr()
    assert "--timeout takes a finite, non-negative number of seconds" in printed.err
    assert "survivor count of zero it never measured" in printed.err, (
        "the refusal has to say what would have happened, or it reads as an "
        "arbitrary validation rule"
    )
    assert "arms measured" not in printed.out, "and nothing was run"
```

### Finding 21 — say it in the reason, since the header now promises it

Three edits inside `run_arms`' operator loop. Each keeps the exception class
name first, so `test_a_refused_arm_is_counted_and_named_in_the_report`,
`test_a_command_that_never_returns_is_recorded_as_unmeasured` and
`test_a_pair_whose_command_ran_and_answered_nothing_is_not_called_unasked`
stay green — they assert on the class name and on *did not return within
0.3s*, both of which survive.

```python
                except (NoMutationDefined, SyntaxError) as exc:
                    # `nothing was written` because the report's header now
                    # sends the reader here to learn whether the arm was
                    # mutated, and an exception class name does not tell them.
                    # `mutate` raises before the open() below, and `ast.parse`
                    # at its end is what makes a SyntaxError one of these.
                    not_applicable[operator] = (
                        f"{type(exc).__name__} (nothing was written to the "
                        f"module): {exc}"
                    )
                    continue
```

```python
                except subprocess.TimeoutExpired:
                    # A command that never returns is not a verdict. `killed`
                    # would read as *a case noticed* and `survived` as *none
                    # did*, and neither was measured -- so it goes where the
                    # pairs with no verdict go, with the bound in the reason.
                    not_applicable[operator] = (
                        f"TimeoutExpired (the mutation was written, run and "
                        f"restored): the command did not return within "
                        f"{timeout}s, so this arm was not measured"
                    )
                except OSError as exc:
                    # The command could not be spawned. Every verdict taken
                    # before this one is real, so the report has to survive to
                    # print them: raising here discards the whole run for one
                    # failed spawn, and `bin/test` builds a virtualenv on
                    # demand, so a mid-run failure is reachable.
                    not_applicable[operator] = (
                        f"{type(exc).__name__} (the mutation was written and "
                        f"restored; the command never started): {exc}"
                    )
```

Then the `operator/arm pairs` header can carry the same clause, because that
list holds both doors too:

```python
        echo(
            f"{len(skipped)} operator/arm pairs with no verdict — the arm was "
            f"answered by another operator, so the arm itself is not in the "
            f"list below, but this operator's count excludes it. The reason "
            f"beside each says whether the mutation was written:"
        )
```

And the case that pins it, which is what the header's promise has been
missing:

```python
def test_the_reason_says_whether_the_mutation_was_written(two_arms):
    """Round 3's finding 21. §14 — the header is what a person reads, and it
    points at the reasons.

    Round 2's finding 15 moved the never-mutated/nothing-measured
    distinction out of the label and into the reason beside each arm. The
    labels changed and the reasons did not, so the header promised a
    disclosure no reason made: `TimeoutExpired` said *not measured*, which
    is a different question, and the `OSError` and `NoMutationDefined`
    reasons said nothing about the write at all. A reader had to already
    know which exceptions are raised before the open() and which after it.

    Red how: drop the parenthetical from any of the three reasons and the
    door it belongs to stops answering here. Executed on all three."""
    module_path, tests = two_arms
    # Written, run, restored.
    _, refused = ARM.run_arms(
        str(module_path),
        [sys.executable, "-c", "import time; time.sleep(30)"],
        timeout=0.3,
    )
    assert all("the mutation was written" in why for _, why in refused), (
        f"{refused!r} — the header says the reason says whether the arm was "
        f"mutated, and a timed-out pair was"
    )
    _, refused = ARM.run_arms(str(module_path), ["specseal-no-such-command-xyz"])
    assert all("the mutation was written" in why for _, why in refused)

    # Nothing written: `mutate` refuses a bare `except:` before the open().
    bare = module_path.parent / "bare.py"
    bare.write_text(
        "def h(x):\n    try:\n        return x\n    except:\n        return None\n",
        encoding="utf-8",
    )
    _, refused = ARM.run_arms(str(bare), [sys.executable, "-c", "pass"])
    assert len(refused) == 1
    assert "nothing was written to the module" in refused[0][1], (
        "and the other door has to say so in the same place, or the header "
        "is answered for one outcome and not the other"
    )
```

### Finding 22 — the disclosure reaches the document that prescribes the command

Insert after `skills/verify/SKILL.md:76`, the paragraph ending *in the rest of
the tree.*:

```markdown
**The bound reaches the command and not what the command starts.** One
operator's command is waited for `--timeout` seconds, 900 by default, and `0`
removes the bound; each arm asks two operators, so an arm can take twice it.
When the wait runs out only that command's own process is killed. The second
form above puts the suite one process further down — `bin/test` execs
`.github/scripts/run_tests.py`, which runs pytest through `subprocess.run` —
so a timed-out pair leaves a whole suite running, unbounded and unreported,
competing with every arm after it. Against a module whose suite can approach
the bound, name the pytest command directly instead of the wrapper.
```

### Finding 23 — the docstring that defines the two fields

`skills/verify/scripts/arm_check.py`, `Verdict`'s docstring. The removed
wording still stands at `mutate`'s docstring and in `phase-3.md`, and
`survivors.md` already excuses both of those places, so `survivor-check`
needs no new exemption for this edit.

```python
    """One arm's result, across every operator that produced a verdict for it.

    `by_operator` maps an operator to `True` when its mutation was noticed.
    An operator that produced no verdict for this arm is absent from it
    rather than recorded as unnoticed — the distinction between *no case
    watches this* and *nothing measured this* is why `refused` exists.

    `not_applicable` is where that operator goes instead, with the reason.
    The reason carries two outcomes since the bound and the spawn failure
    reached this field: `mutate` had no mutation, so nothing was written; or
    the command timed out or could not be spawned, so the mutation WAS
    written, run and restored. It is a separate field rather than nothing,
    because an arm ANOTHER operator answered is not refused as a whole, and
    its unanswered operator was invisible until this field existed: the real
    module reported `remove 31 asked` against 32 arms and never said which
    arm was missing or why.
    """
```

And the comment inside `run_arms`, the same instance:

```python
                    # A command that never returns is not a verdict. `killed`
                    # would read as *a case noticed* and `survived` as *none
                    # did*, and neither was measured -- so it goes where the
                    # pairs with no verdict go, with the bound in the reason.
```

### Finding 24 — name the label the report actually prints

```python
        echo(
            f"{len(skipped)} operator/arm pairs with no verdict — the arm was "
            f"answered by another operator, so it is not among the arms with "
            f"no verdict from any operator, but this operator's count "
            f"excludes it:"
        )
```

Fold this into finding 21's version of the same line rather than applying
both.

### Finding 25 — the grounds cell

`seal/specs/1788936260-a-case-pins-what-it-actually-measures/survivors.md:50`,
the fifth row's Grounds column:

```markdown
The case's arm is a match-case pattern that has no mutation for either
operator, so *could not be asked* is its subject and its name is accurate —
`mutate` raises before anything is written, and the case asserts on
`refused[0]`'s reason rather than on the report. The section header is
asserted by a different case, `test_a_partly_skipped_operator_is_reported_without_refusing_the_arm`,
which pins both `operator/arm pairs with no verdict` and the absence of *not
asked*. The two together are what keep the wider list honest.
```

### Finding 26 — the recount

`overview.md:6`, the `verified:` line's first clause:

```markdown
· verified: executed — `tests/test_arm_check.py` holds 47 `^def test_` and collects 58, the difference being two parametrized cases' arms; re-take both with `grep -c '^def test_'` and `pytest --collect-only`, because a hand-taken count in this line has been wrong twice. Measured 2026-09-09 at `984d585`. Each case seen red against a mutation of the checker; the #310 case red on all five of its arms and green unmutated; the checker's first run over `hooks/review-history-guard.py`.
```

`handoff.md:92`, the same treatment:

```markdown
likewise the pre-round-1 one: 47 `^def test_` and 58 collected, measured
2026-09-09 at `984d585` with `grep -c` and `pytest --collect-only`.
```

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the repository, checked out at `0cfc5e6`, `uv venv` inside it | clone at the target, CPython 3.13.9, pytest 9.1.1. `git status --porcelain` empty at the end of the round |
| `.venv/bin/python -m pytest tests/test_arm_check.py tests/test_a_segment_feeds_the_flow_log.py -q`, exit code read directly | `86 passed`, exit 0 — the orchestrator's figure reproduced |
| `grep -c '^def test_' tests/test_arm_check.py` and `pytest tests/test_arm_check.py -q --collect-only` | 47 and 58. 47 functions, one parametrized eleven ways and one two ways: 47 + 10 + 1 = 58 |
| `arm_check.py <fixture> --tests … --timeout V` through the command line for `V` in `nan`, `inf`, `1e400`, `-inf`, and through `main` for `-1`, `0`, `1e-9`; exit codes read directly | `nan` exit 1 `ValueError: cannot convert float NaN to integer`; `inf` and `1e400` exit 1 `OverflowError: cannot convert float infinity to integer`; `-inf` exit 2 from argparse's option parsing; `-1` exit 2 from the guard; `0` unbounded and both arms measured; `1e-9` exit 0 with `0 arms measured · 0 killed · 0 watched by no case` and both arms in the no-verdict list |
| `run_arms` with `timeout=float("nan")` directly, then the module's sha256 | `ValueError` escapes `run_arms`; the outer `finally` restored the module, hash unchanged |
| `run_arms` then `_report` on a two-arm fixture, all four doors: every pair timed out, the command unspawnable, a bare `except:`, and one operator measured with the other timed out | every label correct — per-arm `no verdict`, `0 arms measured`, `N operator/arm pairs with no verdict`, `N arms with no verdict from any operator`. Module hash back after each |
| The reason strings printed under the no-verdict header, read against the header's claim | `TimeoutExpired: the command did not return within 0.3s, so this arm was not measured`; `FileNotFoundError: [Errno 2] No such file or directory: '…'`; `NoMutationDefined: h:4: a bare \`except:\` catches everything, …`. None contains *mutated*. One arm printed both doors joined by ` \| ` under a singular claim |
| `mutate`'s raise sites against the write, read | `ast.parse` runs at the end of `mutate` and the write happens after `mutate` returns, so `NoMutationDefined` and `SyntaxError` both precede any write — which is what makes the five exemptions exact |
| `grep -rln arm-check` over the tree, and `grep -n timeout` over `skills/verify/SKILL.md` | five files name `arm-check`, one of which is a document; the skill's §2 mentions no bound |
| `.venv/bin/python skills/evidence-check/scripts/evidence_check.py .` unscoped, exit code read directly | exit 0, `total: 1063 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, `652 names read · 0 refused` |
| `git status --porcelain` in the clone after every probe, and the probe file deleted | empty |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-2 | `skills/verify/scripts/arm_check.py:961` | round 2's 15 — the labels landed, the reasons did not |
| round-2 | `skills/verify/scripts/arm_check.py:786` | round 2's 16 — three carriers corrected, a fourth found |
| round-2 | `skills/verify/scripts/arm_check.py:995` | round 2's 17 — the guard's class |
| round-2 | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:6` | round 2's 18 — the recount |
| round-2 | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/handoff.md:71` | round 2's 19 — the dated addendum |
| round-1 | `skills/verify/scripts/arm_check.py:589` | round 1's 6 — the sole-type refusal, which is why one arm shows both doors at once |
| round-1 | `skills/verify/SKILL.md:80` | round 1's 5 — the treatment finding 26 measures the recount against |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Findings 20, 21, 22 and 23 | **issues**, by the run's cap — round 2 spent the one reopening `docs/review-chain-spec.md` allows, so nothing here commissions a fix pass. 20 and 21 are one issue if the owner wants them together: both are a fix that changed the outward half of a pair and left the inward half | the repository owner |
| Findings 24, 25 and 26 | corrections. 24 rides on 21's edit to the same line; 25 and 26 are under `seal/specs/` and count toward nothing | the repository owner, or the release-preparation commit |
| A process group, so the bound reaches a wrapper's grandchildren | **#313** — already deferred in round 2's record. Finding 22 is the disclosure half and does not depend on it | the repository owner, at #313 |
| A run killed mid-arm loses uncommitted work in the module under check | **#312** — already deferred in rounds 1 and 2, and out of scope by this round's spawn prompt | the repository owner, at #312 |
| What `arm-check`'s exit code should mean | `questions.md` Q1 — already deferred, report-only today and pinned by a case. Finding 20 would give it a second non-zero exit to reason about | the repository owner |
| Whether the twelve `remove` survivors are gaps | `questions.md` Q2 — already deferred, with `phase-4.md`'s table of the twelve as the input | a later work item |
| A sweep of the tree for other cases pinning a document clause by substring | #310's inherited `Not verified` row — already deferred and out of scope by the spawn prompt | whoever builds that sweep; #310 stays open on it |
| `round_record.py new` accepting a `#` cell that `close` refuses | already deferred in round 2's record, coordinate `skills/code-review/scripts/round_record.py:2581` | the repository owner |
| The full suite, the repository-wide lint and the typecheck | contract §2 and §3: the broad gate is the orchestrator's, run once now that the rounds have settled. Handed over labelled **`unverified`**. `ruff` is absent from the clone's virtual environment; `uvx ruff check .` is the form that works | **the review orchestrator** |
| Windows and Linux | `overview.md` — already deferred. `bin/arm-check.cmd` has been run by nobody and this diff does not touch it | CI's windows and linux legs |

Needs a fix: yes — findings 20, 21, 22 and 23. Findings 24, 25 and 26 are corrections and count toward nothing.
Loses a record or crashes: yes — `skills/verify/scripts/arm_check.py:1040`. `--timeout nan` and `--timeout inf` escape the arm loop as `ValueError` and `OverflowError`, `_report` is never reached, and the tool exits 1 with a traceback, which is the shape round 1 recorded here and round 2 closed for `OSError`. Nothing leaves the root: `run_arms`' outer `finally` restores the module on that path, the hash was verified back, and the clone's `git status --porcelain` was empty after every value. No verdict is discarded either, because the first command raises before any arm is measured.
Should not merge: no. Nothing on this branch breaks a gate, a hook or a case; 86 passed and `evidence_check.py .` is clean at the target; every no-verdict path restores the module byte for byte. The four open findings are a report-only measurement tool printing an unkept promise, a document missing a warning, a docstring one fix behind its own function, and a traceback on two values nobody types by accident except `inf`. Each is a ticket, none is a release.

## Proof block

Opened in a `git clone --no-local` of the repository at `0cfc5e6`, paths
relative to the repository root:

- `skills/verify/scripts/arm_check.py` — the whole of `run_arms`, `_report`,
  `main`'s argument block and guard, `mutate`, `Verdict`, and the `add_boolean`
  comment at `:400`
- `tests/test_arm_check.py` — the four new units and their fixture, the three
  edited cases, `test_an_operator_that_could_not_be_asked_of_an_arm_is_named`,
  `test_a_partly_skipped_operator_is_reported_without_refusing_the_arm`,
  `two_arms`, and the module header
- `skills/verify/SKILL.md` §*`arm-check` asks condition 2 of a whole module,
  one arm at a time*
- `seal/specs/1788936260-a-case-pins-what-it-actually-measures/` —
  `rounds/round-1.md`, `rounds/round-2.md`, `rounds/round-2-report.md`,
  `survivors.md`, `overview.md`, `handoff.md`, `changelog.md`,
  `phases/phase-3.md`
- `seal/ledger/1788936260-a-case-pins-what-it-actually-measures.md` — the
  three rows re-stamped by this fix pass
- `git diff 0c93614..984d585` in full, all eight files
- Not opened: `bin/arm-check`, `bin/arm-check.cmd`,
  `.github/scripts/run_tests.py`, `hooks/review-history-guard.py`,
  `phases/phase-4.md`, `plan.md`, `spec.md`, `questions.md` — none is touched
  by this diff, and round 2's verdicts on the first four are carried as
  coordinates rather than as conclusions
