# Round 2 — the verifying round of `fix/262-310-a-case-pins-what-it-actually-measures`

| Field | Value |
|---|---|
| Target SHA | `7052392` |
| Diff reviewed | `d07ccbb..33be6ca` — round 1's eight fix commits and nothing else |
| Base | `release/v0.9.5`, draft PR #311 |
| Reviewed in | a `git clone --no-local` at the target, in this session's scratchpad directory. Nothing was written in the working tree but this file |
| Rounds inherited | `rounds/round-1.md`, fourteen verdict rows, for coordinates |
| Kind | verifying round: the answers to round 1's verdicts, plus the seventeen units nobody has reviewed |

## What carried and what I re-derived

Round 1's coordinates carried and saved the expensive half: which line each
finding sits on, which commit claims it, and which record states which number.
No verdict carried. Every one of the ten was opened at the commit it names and
judged against the code as it stands at `33be6ca`.

Two things round 1 got wrong were not inherited as fact, on the orchestrator's
instruction and on my own re-measurement. Its `evidence_check` probe row
records exit 0 and then exit 2, and the 2 was that report's own footprint. Its
finding 6 arithmetic predicted `28 killed · 1 survived`, and the real number is
`29 killed · 0 survived`, because the one inversion survivor was itself one of
the three arms the refusal removes.

## Round 1's ten, answered

**Findings 1 and 2 — the `timeout` and `OSError` paths. The arithmetic stays
honest and two printed lines stop being true.**

The arithmetic is honest, and I attacked it three ways. An arm whose every
operator timed out gets no entry in `by_operator`, so it cannot reach `killed`
or `survived`; it lands in `refused` with the bound in its reason. An arm where
one operator timed out and the other was measured keeps a `Verdict`, and the
timed-out operator is excluded from that operator's `asked` denominator and
named in the *pairs not asked* section. The sole-type refusal composes with
both: an arm refused by `mutate` for `invert` and timed out for `remove` prints
one row carrying both reasons, joined. No pair reaches a denominator it was not
measured for, and no pair goes unnamed.

What is no longer true is what the report says about those arms. Two lines are
now false on the paths this fix created, and finding 15 below is that.

**Finding 3 — `_lines`. The widened claim holds, and against the tokenizer
rather than against eleven fixtures.**

The eleven fixtures pass, in both directions, and they are not what settles it.
`ast` splits its own lines through a private helper of the same shape, and
`skills/verify/scripts/arm_check.py:529`'s `_lines` agrees with that helper
exactly: on all 130 `.py` files in the tree and on 61,516 synthetic strings
built from every terminator and every separator in three- and four-way
combinations, the only difference is a trailing empty element that the helper
appends and `str.splitlines(keepends=True)` also omits. `_splice` indexes only
lines a span reaches, so that element is unreachable. The eight separators
`str.splitlines` adds are exactly the eight `NOT_LINE_ENDS` names, and
`_LINE_END` keeps exactly the three the tokenizer counts.

One case the fixtures do not cover works anyway: a form feed inside the arm's
own indentation, where the tokenizer resets its column counter. Both arms
splice and both parse. Executed.

**Finding 4 — the third needle. It pins the claim, and the demonstration the
fix pass said it lacked is available.**

The fix pass lowered all three positive needles and reported the third as
lowered by class rather than shown red, because showing it would need the
paragraph rewritten. It does not. Capitalising the clause's first letter inside
the collapsed body is the same edit `In practice, ` produces, and it is one
character: with it, all three cased needles go False and all three lowered
needles stay True. Executed against the real document, restored from held bytes
and hash-compared.

So the third assertion pins the claim rather than the clause's position, and
lowering it cannot make a wrong document pass — the lowering only widens what
passes, and nothing in the paragraph distinguishes on case. It neither
over-pins nor under-pins beyond what it did before: `calls running at once` is
a four-word fragment that names the cause without carrying the direction, and
the direction is carried by the negative needle at
`tests/test_a_segment_feeds_the_flow_log.py:592` and by the whole-clause needle
above it. That under-pinning pre-dates this fix and is not something the fix
introduced.

**Finding 6 — applied, and every record states the same number.**

Re-measured in the clone, independently of the orchestrator's own run:
`hooks/review-history-guard.py — 32 arms`, `invert 29 asked · 29 killed · 0
survived`, `remove 32 asked · 20 killed · 12 survived`, combined `32 arms
mutated · 31 killed · 1 watched by no case`, three pairs named as not asked
(`is_closed:143`, `gh_segments:173`, `main:189`), exit 0, and the clone clean
afterwards.

Every record the orchestrator named states that number and no other. I swept
the tree for the numbers rather than reading only those six places:
`skills/verify/SKILL.md:82`, `skills/verify/scripts/arm_check.py:595`,
`tests/test_arm_check.py:1142`, the ledger fragment's fourth and ninth rows,
`changelog.md:17`, `phases/phase-3.md:47` and `phases/phase-4.md:30` all agree.
`tests/test_arm_check.py:1184` quotes `1 of 32` in the past tense, as what the
section used to print, which is correct.

The sweep found one record that was missed, and finding 19 below is that.

**Findings 7 and 8 — the printed output. The static list cannot lie, and it
also cannot tell you whether it applied.**

The static list cannot claim as excluded a type the walk visits, and the
mechanism is stronger than the case that pins it. `_node_arms` returns nothing
for any shape absent from `ARM_SHAPES`, so absence from that table is
sufficient. `test_every_declared_exclusion_is_classified_as_a_non_arm` asserts
that absence and membership in `NOT_ARM_NAMES` for each of the three, and
constructing a module whose only branching is each type in turn gives an empty
arm list every time. Executed.

What the static list gives up is worth naming, and it is a documented choice
rather than a defect. The two `echo` lines at
`skills/verify/scripts/arm_check.py:903` print on every report, including a
module holding none of the three, so they name the rule and never say whether
this module's total was narrowed by it. Finding 7 asked for the exclusions to
be visible where the total is printed, and they are. A reader who wants to know
whether it mattered here still has to walk the tree.

Finding 8 is closed at both call sites. `every` is taken before `--only`
narrows anything in either branch, and the case drives it red from both.

**Findings 5, 9 and 10 — the corrections.**

Finding 5's remedy is a dated column header, a sentence calling the third
column a measurement, an instruction to re-take it, and a case reading both
sentences out of the lowered whole-file text. The numbers themselves are still
hand-taken prose, which is what the disclosure is for. Closed.

Finding 9's correction to `overview.md` moved the ledger count from 4 to 9,
which is right, and moved the case count from 26 to a number that is still
wrong. Finding 18 below is that.

Finding 10's correction now names `dict(os.environ)` as what narrows the path,
and the narrowed path it names — a `--tests` command that sets
`PYTHONPYCACHEPREFIX` itself — is the only one left. Closed.

## The seventeen new units

Nine data and helper units and eight cases, none of them reviewed before now.

`_LINE_END`, `_lines`, `NOT_LINE_ENDS` and `DECLARED_EXCLUSIONS` are covered
above and are correct. `SPLICE_FIXTURES` is built by comprehension and then
appended to three times, and `ids=[f[0] for f in SPLICE_FIXTURES]` is evaluated
after all three, so the eleven ids match the eleven fixtures.
`_TWO_ARM_SOURCE`, `_PLAIN`, `TWO_SCOPES` and `DECLARED` are fixture sources
with no surprises: the `{prelude}` placeholder is the template's only brace, and
`DECLARED` does hold exactly the one countable arm its comment claims.

The eight cases pin what they say they pin, and I checked each against the
mutation aimed at it rather than against its own docstring.

- `test_a_command_that_never_returns_is_recorded_as_unmeasured` asserts both
  arms refused and the bound quoted in each reason. It cannot flake: the
  command sleeps 30 seconds against a 0.3-second bound, so interpreter startup
  cannot beat it either way.
- `test_a_spawn_failure_keeps_the_verdicts_already_measured` asserts four
  attempted commands, the first arm's two verdicts surviving, and the errno
  reaching the report. It patches `subprocess.run` on the module object rather
  than through `monkeypatch`, which is the idiom already used at
  `tests/test_arm_check.py:848`, and it restores in a `finally` before it
  asserts.
- `test_a_separator_the_tokenizer_ignores_does_not_move_a_spliced_arm` pins the
  class at its only site, and the ledger row's *exactly the tokenizer's set*
  is the claim I verified above rather than the claim the fixtures make.
- `test_the_declared_exclusions_are_named_where_the_total_is_printed` asserts
  `1 arms`, the disclosure sentence, each of the three names, and `NOT_ARMS`.
  Its `"1 arms" in text` is a loose substring — it would also match `31 arms` —
  but the fixture has one arm, so it pins what it says here.
- `test_every_declared_exclusion_is_classified_as_a_non_arm` is the structural
  pin, and it is sufficient rather than merely suggestive, for the reason given
  above.
- `test_a_filtered_run_does_not_state_its_count_as_the_modules_total` covers
  both `--only` branches and the unfiltered line, and asserts the absence of a
  denominator in the third.
- `test_the_skill_calls_its_survivor_counts_a_measurement_and_not_a_property`
  pins the disclaimer rather than the numbers, which is the right choice for
  exactly the reason its own docstring gives.
- `test_a_sole_type_handler_is_measured_by_one_operator_and_not_by_both` pins
  both spellings of *one type left*, keeps a two-type handler measured by both
  operators, and asserts the un-asked pair reaches the report.

## The two contract changes

`run_arms` gains `timeout: float | None = 900.0`, keyword-only. Thirteen
existing call sites in `tests/test_arm_check.py` omit it and inherit the
900-second bound; `main` always passes it explicitly. Nothing outside the
module and its tests calls `run_arms`, so the reach is the tests plus one
caller, and the 81 that pass confirm the four existing behaviours are unchanged.

`_report` gains `of_total=None`, keyword-only. Five call sites read it: four
pre-existing ones in `tests/test_arm_check.py` (lines 480, 555, 1149, 1368) and
one added by this diff at line 623, all omitting it, plus the two in `main`
that pass it. `None` means *print no denominator*, which is the pre-fix line and
the right value for a caller that has no module total to state.

That default is fail-open: a `main` call site that loses `of_total` silently
reverts to the header finding 8 fixed. It is guarded — the case drives both
call sites red on a dropped argument — so the fail-open default is a documented
trade rather than an unwatched one. `900.0` appears twice as a literal, at
`skills/verify/scripts/arm_check.py:773` and `:997`, and nothing keeps the two
in step; neither is wrong today because `main` always passes its own.

## What this round opened

### 🟡 15 — a mutated arm is reported as *enumerated and not mutated*, and the summary counts it as never mutated

`skills/verify/scripts/arm_check.py:961`, with `:913` and the loop echo at
`:864`.

Before this fix, an arm reached `refused` only when `mutate` had no mutation
for any operator, so nothing had been written to disk and *enumerated and not
mutated* was true. The timeout and `OSError` paths now put a mutation on disk,
run the command, restore, and then route the arm to the same list. Executed on
a two-arm fixture: with every pair timing out, and separately with a command
that cannot be spawned at all, the report prints

```
0 arms mutated · 0 killed · 0 watched by no case

2 arms refused — enumerated and not mutated:
```

after four mutations were written to the file and restored. Both lines are
false. The first also reads as a clean sweep to anyone skimming — zero
survivors out of zero arms — which is the shape of misreading this whole work
item exists to close, and the exit code is 0.

Why it matters beyond the wording: a command that stops being spawnable partway
through is the reachable case the fix was written for, and the operator reading
that report has to be able to tell *nothing measured this* from *this was never
touched*. The refused section names each reason, so the information is present;
the two headline lines contradict it.

Contract §14 asks for a pin in the same commit. The phrase is pinned, at
`tests/test_arm_check.py:489`, but only through
`test_a_refused_arm_is_counted_and_named_in_the_report`, whose arm has no
mutation for either operator — the one path where the phrase is true. No case
reads the report on either new path.

The paste-ready fix below changes the two labels and adds nothing to any
signature. The fuller fix for the same cause is to stop merging two outcomes
into one list: `run_arms` would record whether a mutation was ever applied for
an arm and return that beside the reason, which changes the shape of `refused`
and reaches thirteen call sites. Either closes the false line; the second is
the one that keeps *not mutated* sayable.

### 🟡 16 — the bound bounds the wait, not the command, for exactly the `--tests` form the skill tells you to type

`skills/verify/scripts/arm_check.py:786` (the docstring) and `:995` (the help
text).

`run_arms`'s docstring says *`timeout` bounds ONE arm's command* and
`--timeout`'s help says *seconds one arm's command may take*. On a timeout,
`subprocess.run` sends `SIGKILL` to the direct child and to nothing below it.
`bin/test` is `exec python3 .github/scripts/run_tests.py`, and that script runs
pytest through `subprocess.run` at `.github/scripts/run_tests.py:297` — so the
documented command, `--tests "bin/test tests/test_chain_hooks.py -q"`, puts the
suite one process below the one the bound reaches.

Executed with a wrapper whose grandchild sleeps 20 seconds against a 1-second
bound: `run_arms` returned in 2.0 seconds, the module was restored, and the
grandchild was still running afterwards. The probe killed it.

The load-bearing half of the bound survives this: the module is restored
promptly, which is what the docstring's own reasoning is about. What does not
survive is the claim. The orphan keeps running unbounded, competing with every
arm after it, and on the documented command that is a full test suite per
timed-out pair. Nothing in the report says a process was left behind.

Two more words in the same two places are off by a factor of two: the bound is
per operator-command, not per arm, so an arm can consume twice it — measured
above, 2.0 seconds against a 1-second bound for one arm.

The paste-ready fix corrects both claims and says what is not killed. The
fuller fix is a process group — `Popen` with `start_new_session=True` (NAME NOT
IN TREE — a `subprocess` keyword my proposed fix would use) and `os.killpg` on
timeout — which changes the process model, behaves differently on Windows, and
is the kind of mechanism round 1 sent to #312 rather than building in a fix
pass. Naming it as an issue is a reasonable answer; leaving the docstring as it
stands is not.

### 🟡 17 — `--timeout -1` measures nothing and prints a perfect score

`skills/verify/scripts/arm_check.py:995`.

`type=float` accepts a negative, and `args.timeout or None` passes it straight
through. `subprocess.run` raises `TimeoutExpired` before the command starts, so
every pair of every arm is recorded as unmeasured. Executed through `main`:
exit 0, `0 arms mutated · 0 killed · 0 watched by no case`, and thirty-two
reasons reading *the command did not return within -1.0s*.

`0` is documented as removing the bound, and `-1` is how several tools spell
the same intention. A person who types it gets the best possible result out of
a run that measured nothing. The refused section discloses it, and the two
headline lines do not — which is finding 15's cause reached through a second
door, and why the two are worth fixing together.

The guard is four lines and refuses at parse time.

### ⬜ 18 — `overview.md`'s case count is wrong again, in the line that corrected it

`seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:6`.

The line reads *43 cases in `tests/test_arm_check.py`, 51 counting the
parametrized one's arms*. Executed: `grep -c '^def test_'` gives 43, and pytest
collects 53. The 51 is 42 plus the nine separator fixtures — the count was
taken before `c37e909` added the CRLF and lone-CR fixtures, which took
`SPLICE_FIXTURES` from nine entries to eleven.

Round 1's finding 9 was this line stating 26 against 35. The correction fixed
the ledger half and left the same class in the other half. `81 passed` across
the two modules is 53 plus 28, so the collected number is the one the run
already agrees with.

### ⬜ 19 — `handoff.md` states the pre-fix number in the present tense, and it is the only snapshot record with no dated note

`seal/specs/1788936260-a-case-pins-what-it-actually-measures/handoff.md:71`.

Three records hold the pre-fix operator comparison. `phases/phase-3.md` and
`phases/phase-4.md` each keep their table and carry a dated addendum saying the
`invert` row moved, which is the right treatment and is what the fix pass did.
`handoff.md` carries neither: line 71 reads *`invert` alone gives **1**
survivor* in the present tense, line 79 pastes the pre-fix run block, and line
60 says *35 cases in `tests/test_arm_check.py`*. The paragraph it sits in tells
the reviewer to open that finding first.

Whether a handoff is frozen the way a round record is, or gets an addendum the
way a phase record does, is the orchestrator's call rather than mine. What is
not defensible is the two treatments sitting side by side in one work item with
nothing saying which applies.

## The generator question the orchestrator asked

I agree it is a defect in the generator. `round_record.py`'s `new` copies the
verdict table verbatim through `copied_row`, and the only reader that validates
a `#` cell is `finding_number`, called from `verdict_rows` at
`skills/code-review/scripts/round_record.py:2581` on the `close` path — so
`new` writes a record that its own sibling subcommand refuses, and the refusal
arrives at the fix pass, which has to hand-edit a generated file, instead of at
the round that could still correct the report. The reviewer's report is where
the `—` came from, and `agents/warden.md`'s verdict-table template does not say
the `#` must be a bare integer either, so the format document is a second
surface worth naming in the issue.

## The suite

Unverified, and the orchestrator answers it: the full suite, the
repository-wide lint and the typecheck. Contract §2 — the broad gate is the
orchestrator's, run once after the rounds settle. `ruff` is not installed in
the clone's virtual environment. Nine narrow modules and one full re-measurement
of the real module were run here and are labelled in the probes table.

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
| 🟡 15 | The timeout and `OSError` paths route a mutated arm into a list the report calls *enumerated and not mutated*, and the summary counts it as never mutated | `skills/verify/scripts/arm_check.py:961` | open | Executed: every pair timed out, and separately a command that cannot be spawned, both print `0 arms mutated · 0 killed · 0 watched by no case` and `2 arms refused — enumerated and not mutated` after four mutations were written and restored. §14 — the phrase is pinned at `tests/test_arm_check.py:489`, on the one path where it is true |
| 🟡 16 | The bound bounds the wait and not the command: a wrapper's grandchild outlives it, for exactly the `--tests` form `skills/verify/SKILL.md` documents | `skills/verify/scripts/arm_check.py:786` | open | Executed: a 1-second bound against a wrapper whose grandchild sleeps 20 seconds returned in 2.0s with the grandchild still running. `bin/test` `exec`s `run_tests.py`, which runs pytest through `subprocess.run` at `.github/scripts/run_tests.py:297`. The same two places also call a per-command bound a per-arm one — 2.0s for one arm against a 1-second bound |
| 🟡 17 | `--timeout` accepts a negative, and a whole run then reports a survivor count of zero at exit 0 | `skills/verify/scripts/arm_check.py:995` | open | Executed through `main`: `--timeout -1` gives exit 0, `0 arms mutated · 0 killed · 0 watched by no case`, and every pair refused with *did not return within -1.0s*. `0` is documented as removing the bound; `-1` is how the same intention is spelled elsewhere and measures nothing |
| ⬜ 18 | `overview.md` says 51 collected cases against 53, in the line that corrected round 1's finding 9 | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/overview.md:6` | open | Executed: 43 `^def test_`, 53 collected by pytest, `81 passed` across the two modules being 53 plus 28. The 51 is 42 plus nine separator fixtures, taken before `c37e909` made `SPLICE_FIXTURES` eleven |
| ⬜ 19 | `handoff.md` states the pre-fix `invert` number in the present tense and is the only snapshot record with no dated note | `seal/specs/1788936260-a-case-pins-what-it-actually-measures/handoff.md:71` | open | Read: line 71 *`invert` alone gives 1 survivor*, line 79 the pre-fix run block, line 60 *35 cases*, in the paragraph that tells the reviewer to open that finding first. Both phase records carry a dated addendum for the same number; whether a handoff is frozen or annotated is the orchestrator's call |

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

## Paste-ready fixes

Finding 15 — the two labels, and the loop echo. No signature changes.

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

And the case that pins the phrase, so it reads the path where it is true and
the paths where it is not:

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

Finding 16 — the docstring paragraph in `run_arms`.

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

And the help text:

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

Finding 17 — the guard, straight after `args = parser.parse_args(argv)`.

```python
    if args.timeout < 0:
        parser.error(
            "--timeout takes a non-negative number of seconds, and 0 removes "
            "the bound. A negative value times every command out before it "
            "starts, so every arm is recorded as unmeasured and the run "
            "prints a survivor count of zero it never measured."
        )
```

Finding 18 — the line in `overview.md`.

```markdown
· verified: executed — 43 cases in `tests/test_arm_check.py`, 53 collected counting the parametrized one's eleven arms, each seen red against a mutation of the checker; the #310 case red on all five of its arms and green unmutated; the checker's first run over `hooks/review-history-guard.py`. Read — #262's and #310's bodies, and the two commits the ticket's table predates. Unverified — the full suite, the repository-wide lint and the typecheck (contract §2: the orchestrator's, once, after the rounds), and every platform but macOS.
```

Finding 19 — an addendum under `handoff.md`'s run block, in the shape both
phase records already use.

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

Needs a fix: yes — findings 15, 16 and 17. Two printed lines that are false on the paths this fix pass created (`skills/verify/scripts/arm_check.py:913` and `:961`), a docstring and a help text claiming a bound the code does not deliver for the documented `--tests` form (`:786` and `:995`), and a negative `--timeout` that prints a survivor count of zero it never measured (`:995`). Findings 18 and 19 are record corrections under `seal/specs/` and count here for nothing.
Loses a record or crashes: no — `git status --porcelain` was empty in the clone after 61 mutations of the real module and every probe, including the all-timed-out path, the unspawnable-command path and the orphaned-grandchild probe. `subprocess.run` reaps the child before raising `TimeoutExpired`, so the `finally` restore runs with no live reader of the mutated file. The `OSError` path now returns a report instead of raising, which is what round 1 recorded as the floor breach and it is closed.

## Proof

Files opened in this round, in a clone at `7052392`:

- `skills/verify/scripts/arm_check.py`
- `skills/verify/SKILL.md`
- `tests/test_arm_check.py`
- `tests/test_a_segment_feeds_the_flow_log.py`
- `bin/test`, `bin/arm-check`
- `.github/scripts/run_tests.py`
- `skills/code-review/scripts/round_record.py`
- `skills/code-review/scripts/chain_check.py`
- `seal/ledger/1788936260-a-case-pins-what-it-actually-measures.md`
- `seal/specs/1788936260-a-case-pins-what-it-actually-measures/` — `routing.md`, `overview.md`, `handoff.md`, `changelog.md`, `survivors.md`, `phases/phase-3.md`, `phases/phase-4.md`, `rounds/round-1.md`, `rounds/round-1-report.md`

Commands are in the probes table above, each with its exit code read directly
rather than through a pipe. One probe file, `test_tmp_round2.py`, written in the
clone, run, and removed; the clone was clean afterwards.
