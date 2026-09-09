# 1788936260-a-case-pins-what-it-actually-measures — review round 2

| Field | Value |
|---|---|
| Target SHA | 7052392 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 311 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Contract changes | none |
| New units | NO_VERDICT_COMMANDS (depth 1); test_the_report_does_not_call_a_mutated_arm_unmutated (depth 1); test_the_help_says_the_bound_reaches_the_command_and_not_its_children (depth 1); test_a_negative_bound_is_refused_rather_than_measured (depth 1); test_a_pair_whose_command_ran_and_answered_nothing_is_not_called_unasked (depth 1) |
| Needs a fix | yes — findings 15, 16 and 17. Two printed lines that are false on the paths this fix pass created (`skills/verify/scripts/arm_check.py:913` and `:961`), a docstring and a help text claiming a bound the code does not deliver for the documented `--tests` form (`:786` and `:995`), and a negative `--timeout` that prints a survivor count of zero it never measured (`:995`). Findings 18 and 19 are record corrections under `seal/specs/` and count here for nothing. |
| Loses a record or crashes | no — `git status --porcelain` was empty in the clone after 61 mutations of the real module and every probe, including the all-timed-out path, the unspawnable-command path and the orphaned-grandchild probe. `subprocess.run` reaps the child before raising `TimeoutExpired`, so the `finally` restore runs with no live reader of the mutated file. The `OSError` path now returns a report instead of raising, which is what round 1 recorded as the floor breach and it is closed. |

- [x] Pass

## What this round was asked

Round 2, the **verifying** round of
`fix/262-310-a-case-pins-what-it-actually-measures`. Target `7052392`; the
diff to review is `d07ccbb..33be6ca`, round 1's fixes and nothing else. Round
1's record and report are committed and inherited.

**The job is the answers, not new findings.** For each of round 1's ten
verdicts, is it actually closed. Eight read `**fixed** <sha>` and two
`answered`; open the commit each names and judge the fix, not the claim that
it landed.

**One surface in that diff is exempt from that rule and is a finding surface
instead**: `New units`, seventeen entries, every one at depth 1 —
`_LINE_END`, `_lines`, `NOT_LINE_ENDS`, `SPLICE_FIXTURES`, `_PLAIN`,
`DECLARED_EXCLUSIONS`, `DECLARED`, `TWO_SCOPES`, `_TWO_ARM_SOURCE` and eight
cases. Nobody has reviewed those. Treat them as *is this correct*, and the
eight cases as *does this pin what it says it pins* — round 1's own finding 4
was a case asserting something true that was not the claim, and the fix pass
reported four of the checker's cases first passing against the mutation aimed
at them.

**Two contract changes, and their reach is the regression class issue #57
measured.** `run_arms` gains a `timeout` keyword and `_report` an `of_total`
keyword. Both have defaults, so the four existing `_report` call sites are
claimed unchanged — verify that, and verify the default's value is the right
one rather than merely present.

**Five things this round was told to attack in the fixes specifically.**

1. **The `timeout` and `OSError` paths (finding 1's first half, finding 2).**
   A `TimeoutExpired` and an `OSError` are now recorded as un-asked pairs. Does
   the arithmetic stay honest — an arm whose every operator timed out, an arm
   where one timed out and one was measured, and the interaction with the
   sole-type refusal that already produces un-asked pairs? A timeout is a
   *verdict nobody took*, and this module's own subject is that such a thing
   must be named rather than dropped.
2. **`_lines` (finding 3).** It is a new unit and the claim widened after
   round 1: the row now says the split must be *exactly* the tokenizer's set,
   both directions. Check both — the eight separators `splitlines` adds, and
   the two terminators a `\n`-only split drops. Then ask whether `_lines` and
   `ast` actually agree, rather than whether they agree on eleven fixtures.
3. **Finding 4's third needle.** The fix lowered all three positive
   assertions. The fix pass says the third, `calls running at once`, was
   lowered by class rather than demonstrated red, because demonstrating it
   would need the paragraph rewritten. Judge that gap: is the third assertion
   now pinning the claim, over-pinning, or under-pinning?
4. **Finding 6's applied answer.** `invert` now refuses a sole-type handler
   and the numbers moved to `29 asked · 29 killed · 0 survived` — not round
   1's predicted `28 killed · 1 survived`, because the one inversion survivor
   was itself one of the three refused arms. I re-measured that in a separate
   clone at `c37e909`: exit 0, three pairs named, combined `32 arms mutated ·
   31 killed · 1 watched by no case`, and the clone's tree clean afterwards.
   What is left is whether **every record that states the number now states
   the same one** — `SKILL.md`, `OPERATORS`' docstring, a case docstring, the
   ledger fragment's fourth row, the changelog fragment, and the dated notes
   the fix pass left under `phase-3.md` and `phase-4.md` instead of editing
   their measurements.
5. **Findings 7 and 8's printed output.** Both change what a person reads, so
   contract §14 asks for a pin in the same commit. The declared exclusions are
   now named statically rather than by a second walk — check that the static
   list cannot claim as excluded a node type the walk actually visits, which is
   what the fix pass says its extra case covers.

**Facts handed over as coordinates, each labelled. Executed by me** at
`c37e909` or `33be6ca`: the arm-check re-measurement above; `81 passed` on
`tests/test_arm_check.py` and `tests/test_a_segment_feeds_the_flow_log.py`;
43 `^def test_` in the former; 9 ledger data rows; `evidence_check.py .`
unscoped exit 0, `1063 ok · 0 drifted · 0 broken`; `survivor-check` exit 0 on
`d07ccbb..33be6ca` and, on the pre-`survivors.md` range `d07ccbb..5b55671`,
one report now excused. **Executed by the fix pass and not re-run by me** —
claims with coordinates, contract §5: `487 passed` across sixteen modules,
`113 passed` across the five that read the ledger, ten mutation arms each seen
red, and six document edits against the corrected #310 case.

**Two things round 1 got wrong that this round should not inherit as fact.**
Its `evidence_check` probe row records exit 0 and then exit 2 — the 2 is the
report's own footprint, a `_lines` the tree did not have yet, and `_lines`
exists now. And its finding 6 arithmetic predicted `28 killed · 1 survived`,
which is wrong for the reason in point 4.

**Out of scope.** #312 (finding 1's sidecar half, mechanism, the owner's);
`questions.md` Q1 and Q2; #310's inherited sweep. The broad gate is the
orchestrator's, once, after this round settles — contract §2.

**If this round opens nothing needing a fix, the run ends here.** If it opens
something, that is the one reopening the chain allows and the run then ends
capped.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | A hung `--tests` command is unbounded | `skills/verify/scripts/arm_check.py:822` | answered | Closed at `7b48498`. Executed: a 30s command against a 0.3s bound returns in 0.3s per pair, both arms unmeasured, the bound quoted in each reason, the module restored. The bound's own claim is narrower than it says — finding 16 |
| 2 | A `--tests` command that cannot be spawned discards every verdict measured so far | `skills/verify/scripts/arm_check.py:842` | answered | Closed at `7b48498`. Executed: a nonexistent command no longer raises out of `run_arms`; every arm reaches the report with the errno beside it, the module restored. What the report then says about those arms is finding 15 |
| 3 | `_splice` used `str.splitlines`, which splits on separators `ast` does not | `skills/verify/scripts/arm_check.py:529` | answered | Closed at `d4209bd`, re-stamped at `33be6ca`. Executed: `_lines` agrees with `ast`'s own private line splitter on 130 tree files and 61,516 synthetic strings, differing only by a trailing empty element `_splice` cannot index. Both directions of the widened claim hold, and a form feed in the arm's own indentation splices correctly too |
| 4 | #310's clause assertion was case-sensitive on its first letter | `tests/test_a_segment_feeds_the_flow_log.py:566` | answered | Closed at `facac61`. Executed: capitalising each clause's first letter in the collapsed body turns all three cased needles False and leaves all three lowered needles True — the demonstration the fix pass reported as unavailable. The third needle pins the claim; its lack of a direction pre-dates this fix and is carried by the negative needle at `:592` |
| 5 | Two undated hand-taken numbers in durable prose, with no case | `skills/verify/SKILL.md:82` | answered | Closed at `5b55671`. Read: the column header is dated, the disclaimer names the numbers a measurement and says what to do instead, and `test_the_skill_calls_its_survivor_counts_a_measurement_and_not_a_property` pins both sentences out of the lowered whole-file text. Executed: the numbers are correct at `33be6ca` |
| 6 | For a sole-type `except`, one measurement was reported as two operator rows | `skills/verify/scripts/arm_check.py:634` | answered | Closed at `5b55671`. Executed independently of the orchestrator's run: `invert 29 asked · 29 killed · 0 survived`, `remove 32 asked · 20 killed · 12 survived`, combined `32 arms mutated · 31 killed · 1 watched by no case`, three pairs named, exit 0, clone clean. Every record the orchestrator listed states that number; the sweep found one it did not list — finding 19 |
| 7 | The declared exclusions were invisible where the total is printed | `skills/verify/scripts/arm_check.py:903` | answered | Closed at `125bae0`. Executed: the static list cannot name a walked type, because `_node_arms` returns nothing for any shape absent from `ARM_SHAPES` and the case asserts that absence for all three; a module whose only branching is each type in turn gives an empty arm list. The line prints on a module holding none of the three, so it names the rule and not whether it applied — a documented trade, not a defect |
| 8 | `--only` made the header state the filtered count as the module's total | `skills/verify/scripts/arm_check.py:1013` | answered | Closed at `125bae0`. Executed: both branches take `every` before `--only` narrows anything; the filtered header reads `1 of 2 arms (--only)` and the unfiltered one carries no denominator. The `of_total=None` default is fail-open and the case drives both call sites red on a dropped argument |
| 9 | `overview.md` stated counts the tree did not have | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:5` | answered | Corrected at `5b55671`; the ledger half is right — 9 data rows, executed. The case half is still wrong, as finding 18 |
| 10 | The `PYTHONDONTWRITEBYTECODE` self-report's reasoning named too wide a path | `tests/test_arm_check.py:869` | answered | Corrected at `5b55671`. Read: `run_arms` builds the child's environment from `dict(os.environ)`, so the only remaining path is a `--tests` command that sets `PYTHONPYCACHEPREFIX` itself, which is what the docstring now names |
| 🟢 11 | Grammar totality, both directions | `skills/verify/scripts/arm_check.py:88` | answered | Re-derived rather than carried: `ARM_SHAPES` and `NOT_ARM_NAMES` are disjoint, and the walk dispatches on `ARM_SHAPES` alone, which is what makes absence from it sufficient for finding 7's disclosure. Executed: 81 passed, `test_every_ast_constructor_is_classified` among them, on CPython 3.13.9 |
| 🟢 12 | The two `bin/` wrappers are faithful transcriptions | `bin/arm-check:16` | answered | Untouched by this diff — `git diff d07ccbb..33be6ca` names neither file — so round 1's verdict has nothing to have been broken by. Read: `bin/arm-check` still `exec`s the script with arguments passed through, which is the half finding 16 depends on |
| 🟢 13 | The run leaves no mutated module and no temp file | `skills/verify/scripts/arm_check.py:867` | answered | Re-measured, not carried: `git status --porcelain` empty in the clone after 61 mutations of the real module, four probe runs including the all-timed-out and unspawnable paths, and the grandchild probe. The timeout path restores because `subprocess.run` reaps the child before raising |
| 🟢 14 | This branch falsifies no ledger row elsewhere | `seal/ledger.md` | answered | Executed: `evidence_check.py .` unscoped in the clone at `7052392`, exit code read directly, exit 0, `total: 1063 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, `0 refused`. Round 1's second reading of 2 was its own report's footprint and is not inherited |
| 🟡 15 | The timeout and `OSError` paths route a mutated arm into a list the report calls *enumerated and not mutated*, and the summary counts it as never mutated | `skills/verify/scripts/arm_check.py:961` | **fixed** `b9a1af7` | fixed at b9a1af7 — four labels, not two: the fix pass enumerated a third door, a pair whose command ran and answered nothing, which the report had been calling `not asked`; Executed: every pair timed out, and separately a command that cannot be spawned, both print `0 arms mutated · 0 killed · 0 watched by no case` and `2 arms refused — enumerated and not mutated` after four mutations were written and restored. §14 — the phrase is pinned at `tests/test_arm_check.py:489`, on the one path where it is true |
| 🟡 16 | The bound bounds the wait and not the command: a wrapper's grandchild outlives it, for exactly the `--tests` form `skills/verify/SKILL.md` documents | `skills/verify/scripts/arm_check.py:786` | **fixed** `22fc414` | fixed at 22fc414 — the claim in three places, not two; the process group is mechanism and went to #313; Executed: a 1-second bound against a wrapper whose grandchild sleeps 20 seconds returned in 2.0s with the grandchild still running. `bin/test` `exec`s `run_tests.py`, which runs pytest through `subprocess.run` at `.github/scripts/run_tests.py:297`. The same two places also call a per-command bound a per-arm one — 2.0s for one arm against a 1-second bound |
| 🟡 17 | `--timeout` accepts a negative, and a whole run then reports a survivor count of zero at exit 0 | `skills/verify/scripts/arm_check.py:995` | **fixed** `4243149` | fixed at 4243149 — refused at parse time, exit 2, the module untouched; Executed through `main`: `--timeout -1` gives exit 0, `0 arms mutated · 0 killed · 0 watched by no case`, and every pair refused with *did not return within -1.0s*. `0` is documented as removing the bound; `-1` is how the same intention is spelled elsewhere and measures nothing |
| ⬜ 18 | `overview.md` says 51 collected cases against 53, in the line that corrected round 1's finding 9 | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:6` | answered | corrected at 970e2e0 |
| ⬜ 19 | `handoff.md` states the pre-fix `invert` number in the present tense and is the only snapshot record with no dated note | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/handoff.md:71` | answered | corrected at 970e2e0 |

## Paste-ready fixes

```python
    survivors = [v for v in verdicts if not v.killed]
    echo("")
    echo(
        f"{len(verdicts)} arms measured · {len(verdicts) - len(survivors)} killed "
        f"· {len(survivors)} watched by no case"
    )
```
```python
    if refused:
        echo("")
        # NOT "not mutated": the timeout and OSError paths write the mutation,
        # run the command and restore, and land here when no operator came
        # back with a verdict. A reader has to be able to tell "nothing
        # measured this" from "this was never touched", and the reason beside
        # each arm is what says which.
        echo(f"{len(refused)} arms with no verdict from any operator:")
```
```python
                echo(f"  no verdict  {arm}")
```
```python
def test_the_report_does_not_call_a_mutated_arm_unmutated(two_arms):
    """Round 2's finding 15. §14 — the report is what a person reads.

    An arm reached `refused` only when `mutate` had no mutation for any
    operator, so nothing had been written to disk. The timeout and `OSError`
    paths write the mutation, run the command, restore, and land in the same
    list — where the header said `enumerated and not mutated` and the summary
    counted the arm as never mutated. Both were false after four mutations.

    Red how: either label restored prints `enumerated and not mutated` here.
    Executed."""
    module_path, _ = two_arms
    verdicts, refused = ARM.run_arms(
        str(module_path),
        [sys.executable, "-c", "import time; time.sleep(30)"],
        timeout=0.3,
    )
    lines = []
    found = [v.arm for v in verdicts] + [a for a, _ in refused]
    ARM._report(
        str(module_path), verdicts, refused, ARM.counts(found), lines.append
    )
    text = "\n".join(lines)
    assert "not mutated" not in text, (
        f"{text!r} — every one of these arms was mutated on disk and then "
        f"restored; what was missing is a verdict, not the mutation"
    )
    assert "no verdict from any operator" in text
    assert "arms mutated" not in text, (
        "the summary counts arms that produced a verdict, and a timed-out "
        "arm was mutated without producing one"
    )
```
```python
    `timeout` bounds how long ONE operator's command is WAITED for, and `None`
    removes the bound. An arm asks each operator in turn, so an arm can take
    twice it. While a command runs the module on disk holds the mutation and
    `capture_output` means nothing is printed, so an unbounded hang is
    indistinguishable from a slow suite — and the longer the process lives
    mutated, the more likely it is ended by something no `finally` sees.

    It bounds the WAIT and not the work: `subprocess.run` kills the direct
    child and nothing below it, and the documented `--tests "bin/test ..."`
    puts pytest one process further down (`bin/test` execs
    `.github/scripts/run_tests.py`, which runs pytest through
    `subprocess.run`). So a timed-out pair leaves that suite running, unbounded
    and unreported, competing with every arm after it. The module is restored
    either way, which is the half the paragraph above is about.
```
```python
    parser.add_argument(
        "--timeout",
        type=float,
        default=900.0,
        help=(
            "seconds ONE operator's command is waited for before the pair is "
            "recorded as unmeasured. An arm asks two operators, so it can "
            "take twice this. Only the command's own process is killed, not "
            "anything it spawned. 0 removes the bound"
        ),
    )
```
```python
    if args.timeout < 0:
        parser.error(
            "--timeout takes a non-negative number of seconds, and 0 removes "
            "the bound. A negative value times every command out before it "
            "starts, so every arm is recorded as unmeasured and the run "
            "prints a survivor count of zero it never measured."
        )
```
```markdown
· verified: executed — 43 cases in `tests/test_arm_check.py`, 53 collected counting the parametrized one's eleven arms, each seen red against a mutation of the checker; the #310 case red on all five of its arms and green unmutated; the checker's first run over `hooks/review-history-guard.py`. Read — #262's and #310's bodies, and the two commits the ticket's table predates. Unverified — the full suite, the repository-wide lint and the typecheck (contract §2: the orchestrator's, once, after the rounds), and every platform but macOS.
```
```markdown
**Round 1 moved the `invert` row and the block above is the run before it.**
Finding 6 refused `invert` for the three handlers with one type left, where the
two operators produce the same text. Re-measured 2026-09-09: `invert` 29 asked
· 29 killed · **0** survived, `remove` and the combined row unchanged. The
paragraph's *`invert` alone gives 1 survivor* is that pre-fix run; the argument
it makes is unchanged, because 0 beside the ticket's nine reads as a refutation
just as 1 did. The case count above is likewise the pre-round-1 one — 53 are
collected at `33be6ca`.
```

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` of the repository, checked out at `7052392` | clone at the target; a `uv` venv built inside it, CPython 3.13.9, pytest 9.1.1 |
| `.venv/bin/python -m pytest tests/test_arm_check.py tests/test_a_segment_feeds_the_flow_log.py -q`, exit code read directly | `81 passed`, exit 0 |
| `.venv/bin/python -m pytest tests/test_arm_check.py -q --collect-only` and the same for the flow-log module | 53 collected and 28 collected; `grep -c '^def test_'` 43 and 28. 42 + 11 parametrized arms = 53, so `overview.md`'s 51 is wrong |
| `.venv/bin/python skills/verify/scripts/arm_check.py hooks/review-history-guard.py --tests ".venv/bin/python -m pytest tests/test_chain_hooks.py -q"`, exit code read directly | exit 0. `hooks/review-history-guard.py — 32 arms`; `32 arms mutated · 31 killed · 1 watched by no case`; `invert 29 asked · 29 killed · 0 survived`; `remove 32 asked · 20 killed · 12 survived`; three pairs not asked, `is_closed:143`, `gh_segments:173`, `main:189`; survivor `main:189 ExceptHandler Exception` |
| `_lines` against `ast`'s own private line splitter, on every `.py` file in the tree and on synthetic strings | 130 files and 61,516 strings: zero differences other than a trailing empty element the reference appends, which `str.splitlines(keepends=True)` also omits and `_splice` cannot index |
| `arms` and `mutate` on a source with a form feed inside the arm's own indentation | both arms spliced and both mutations parsed, for both operators |
| `run_arms` with a 30-second command against a 0.3-second bound, then `_report` on the result | 0 verdicts, 2 refused, the bound quoted in each reason. The report printed `0 arms mutated · 0 killed · 0 watched by no case` and `2 arms refused — enumerated and not mutated` |
| `run_arms` with a command that cannot be spawned at all, then `_report` | 0 verdicts, 2 refused, `FileNotFoundError` in each reason, module restored, the same two false lines, `_report` returned 0 |
| `run_arms` with one operator's command timing out and the other measured, then `_report` | the measured operator keeps its row, the timed-out pair is named under *operator/arm pairs not asked*, and no pair reaches a denominator it was not measured for |
| The sole-type refusal and a timeout on the same arm | one refused row carrying both reasons, joined — `NoMutationDefined` for `invert` and `TimeoutExpired` for `remove` |
| `_report` on a module holding none of `Assert`, `For`, `AsyncFor` | the two disclosure lines print anyway, naming the rule and not whether it applied |
| `arms` on a module whose only branching is each declared exclusion in turn, and the two table memberships | empty arm list for all three; none in `ARM_SHAPES`, all three in `NOT_ARM_NAMES` |
| `ARM.main` with `--timeout 0` and with `--timeout -1` | `0`: unbounded, both arms measured. `-1`: exit 0, `0 arms mutated · 0 killed · 0 watched by no case`, every pair refused with *did not return within -1.0s* |
| `run_arms` at a 1-second bound against a wrapper whose grandchild sleeps 20 seconds | returned in 2.0s, module restored, grandchild still in `ps` afterwards; the probe killed it |
| The three #310 needles against the real `skills/verify/SKILL.md`, each clause capitalised in the collapsed body, document restored from held bytes and hash-compared | cased False and lowered True for all three; document hash unchanged |
| `.venv/bin/python skills/evidence-check/scripts/evidence_check.py .` unscoped, exit code read directly | exit 0, `total: 1063 ok · 0 drifted · 0 broken · 0 external · 0 old-format`, `542 names read · 0 refused` |
| `.venv/bin/python skills/code-review/scripts/survivor_check.py --range d07ccbb..33be6ca`, exit code read directly | exit 0, 781 files examined at `33be6ca` against 31 removed sentences, no removed wording still standing |
| Sweep of the tree for every statement of the operator numbers | `skills/verify/SKILL.md:82`, `arm_check.py:595`, `test_arm_check.py:1142`, the ledger fragment's rows 4 and 9, `changelog.md:17`, `phase-3.md:47`, `phase-4.md:30` all agree. `handoff.md:71` and `:79` do not — finding 19 |
| `git status --porcelain` in the clone after every probe, and the probe file removed | empty |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/arm_check.py:745` | round 1's 1 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:520` | round 1's 3 — fixed |
| round-1 | `tests/test_a_segment_feeds_the_flow_log.py:562` | round 1's 4 — fixed |
| round-1 | `skills/verify/SKILL.md:80` | round 1's 5 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:589` | round 1's 6 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:233` | round 1's 7 — fixed |
| round-1 | `skills/verify/scripts/arm_check.py:787` | round 1's 8 — fixed |
| round-1 | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:5` | round 1's 9 — answered |
| round-1 | `tests/test_arm_check.py:744` | round 1's 10 — answered |
| round-1 | `skills/verify/scripts/arm_check.py:87` | round 1's 🟢 11 — answered |
| round-1 | `bin/arm-check.cmd:7` | round 1's 🟢 12 — answered |
| round-1 | `skills/verify/scripts/arm_check.py:767` | round 1's 🟢 13 — answered |
| round-1 | `seal/ledger.md` | round 1's 🟢 14 — answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Finding 1's second half — a run killed mid-arm loses uncommitted work in the module under check | **#312**, already deferred in round 1's record with the four things it has to settle. Untouched by this diff and out of scope by the spawn prompt | the repository owner, at #312 |
| A process group for finding 16, so the bound reaches a wrapper's grandchildren | an issue, if the owner wants it. It changes the process model, differs on Windows, and is the kind of mechanism round 1 sent to #312 rather than building. The docstring correction is owed either way and is not deferred | the repository owner |
| What `arm-check`'s exit code should mean | `questions.md` Q1 — already deferred, report-only today and pinned by a case. Findings 15 and 17 make its printed output honest without touching it | the repository owner |
| Whether the twelve `remove` survivors are gaps | `questions.md` Q2 — already deferred, with `phase-4.md`'s table of the twelve as the input | a later work item |
| A sweep of the tree for other cases pinning a document clause by substring | #310's inherited `Not verified` row — already deferred and out of scope by the spawn prompt | whoever builds that sweep; #310 stays open on it |
| `round_record.py new` accepting a `#` cell that `close` refuses | an issue the orchestrator will open; the coordinate is `skills/code-review/scripts/round_record.py:2581`, and `agents/warden.md`'s verdict-table template is the second surface | the repository owner |
| The full suite, repository-wide lint and typecheck | contract §2: the broad gate is the orchestrator's, run once after the rounds settle. `ruff` is absent from the clone's virtual environment | **the review orchestrator** |
| Windows and Linux | `overview.md` — already deferred. `bin/arm-check.cmd` has been run by nobody, and this diff does not touch it | CI's windows and linux legs |
