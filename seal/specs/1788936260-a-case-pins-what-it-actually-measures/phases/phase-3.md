# 1788936260-a-case-pins-what-it-actually-measures — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `8d53ca4` |
| Ran by | unknown — the spawn prompt carried no `Ran by` value, and this row is the spawning session's rather than the segment's own; the orchestrator fills it |

## What this phase was asked

The mutation and the report: each arm mutated, the command run, the unkilled
arms named with function, arm and line; the module restored and
hash-verified after each. Verified by a fixture with one watched and one
unwatched arm.

The restore condition came with the phase and with a reason: four fix passes
ran this enumeration by hand in one day, and the one that skipped the hash
check recorded a mutation as killed while never having applied it, because
the pattern missed by two spaces of indentation. Never `git checkout`.

## What this phase found

**The survivor count is a property of the mutation operator, and the first
run made that unmissable.** Built with inversion alone — `not (arm)` — the
checker reported **1** survivor out of 32 arms. #262 reports **nine**
unwatched arms. Those two numbers do not disagree; they answer different
questions, and putting the 1 beside the ticket's 9 would have read as a
refutation of the ticket by a checker measuring something else. That is
precisely the class of error this work item exists about.

Reading #262 again, every sentence in its table is about **taking something
out**: *"removing either opt-in half makes a globally installed plugin nag
unrelated repositories"*, *"removing `not segs` makes the stray and
unreadable notices fire on every Bash call"*. Its nine is a **removal** count.
`plan.md` names all three kill mechanisms — *"a test inverted, a guard
removed, an except handler made unreachable"* — and only two were built.

So there are two operators, and the report keeps them apart:

| Operator | Asks | Result on the real module, as this phase measured it |
|---|---|---|
| `invert` | would a case notice this test being **backwards** | 32 asked · 31 killed · **1 survived** |
| `remove` | would a case notice this arm being **absent** | 32 asked · 20 killed · **12 survived** |

**Round 1's fix moved the top row and the argument above it got sharper.**
Finding 6: for a handler with one type left, `invert` and `remove` produce the
same text, so `invert` is refused for those three arms and the pair is named
in the report. Re-measured 2026-09-09 after the fix: `invert` 29 asked · 29
killed · **0 survived**, `remove` unchanged, combined unchanged at 31 killed ·
1 watched by no case. The single inversion survivor was `main:189`, which is
one of the three — so a checker built with inversion alone would now print
**0** beside the ticket's nine rather than 1.

An arm counts watched when **any** operator is noticed, because the question
*does any case depend on this arm* is answered by one yes. The per-operator
rows sit beside that total and the report says in words which row the
ticket's table compares with — a reader who compares 9 with the combined
count is comparing two different measurements.

**12 against the ticket's 9, and the gap is the ticket's own argument.** The
file changed twice after that measurement (`341be0b`, `1dedd1e`) and four of
the thirteen it started from were closed on #209 · #210's branch. The number
is not corrected in the ticket (`questions.md` assumption 3); it is recorded
here beside the run that produced it.

**Removing an arm cannot be spliced inside the arm.** Dropping a member of
`a and b` has to rewrite `a and b`, so an `Arm` grew a second span — the
group — and the text that group reads without it. Two places where the naive
form is a `SyntaxError` rather than a mutation, and both are in the real
module:

- **An except tuple spans its own parentheses.** The remainder replaces them
  too, and `except OSError, ValueError:` has not been Python since 2. `reader`
  is exactly that shape (`except (OSError, ImportError, SyntaxError)`), so
  unwrapped, all three of its handler arms would have come back refused.
- **A wrapped boolean test spans its own brackets.** `gh_segments`'s `while`
  test is `i < len(toks) and (\n … \n)`; dropping the index guard leaves a
  two-line expression with nothing bracketing it. **This one was found by the
  run, not by reading** — see below.

**An operator that could not be asked of an arm was invisible, and only the
report's own arithmetic gave it away.** The first two-operator run printed
`remove 31 asked` against 32 arms. Nothing said which arm was missing or why:
the arm was not `refused`, because `invert` had measured it, so its un-asked
operator fell out of that operator's denominator silently. That is the
skip-versus-refuse failure this whole module refuses, one level in — in the
code that reports the refusals. A `Verdict` now carries `not_applicable` with
the reason, and the report names every operator/arm pair it could not ask.
The arm was `gh_segments:176`, and the parenthesising fix above means the
current run asks all 32.

**Round 2 widened that list and relabelled it, so the report's words are no
longer these.** Round 1's timeout and `OSError` fixes put a second outcome
into it — a pair whose command WAS asked and answered nothing — so *not
asked* became false of the section as a whole and *enumerated and not mutated*
became false of the arms. Since round 2's finding 15 the report reads *N
operator/arm pairs with no verdict*, *N arms with no verdict from any
operator* and *N arms measured*, and the reason beside each arm is what says
whether it was ever mutated. Everything this phase says above is about the
pair that could not be asked, which is still that.

**A third way for a verdict to be measured against the wrong module, which
no hash catches.** Building the fixture, the arm that no case reaches came
back `killed`, with a traceback pointing at an assertion the unmutated module
satisfies. The bytes on disk were correct at every moment; the interpreter
never read them.

CPython validates a `.pyc` against the source's mtime and **size**, and two
mutations of one arm shape are routinely the same size — `not (host ==
"example.com")` and `not (flag)` both add exactly six characters. Written
inside one mtime tick, arm two loads arm one's bytecode. `restore`'s hash
compare cannot see it, because it compares the file and the file was right.

The repair is `clear_bytecode_cache` around every arm plus
`PYTHONDONTWRITEBYTECODE` in the subprocess. The realistic trigger is not
even the loop: **this repository's own suite imports
`hooks/review-history-guard.py`**, so `hooks/__pycache__/` holds bytecode for
it before `arm-check` is ever run.

**Reproducing it is timing-dependent, so the mechanism is what gets pinned.**
Measured both ways inside this work item — poisoned when the two writes were
adjacent, clean when they were not. A case that reproduces it would pass on a
fast machine and fail on a slow one. So the case asks the one question with a
stable answer: at the moment an arm's command runs, is there cached bytecode
for the module at all? A planted cache, a stand-in command that reports what
it *saw*, and one observation per arm.

**Four cases went green against the mutation aimed at them, and each was a
case pinning the wrong thing.** This is the phase's most useful finding,
because all four passed the suite and would have shipped:

| Case, as first written | The mutation it survived | Why |
|---|---|---|
| the exit rule is report-only | the mutating branch returns the survivor count | it called `main([GUARD])` with no `--tests`, so it only ever ran the LISTING branch |
| a stale cache cannot decide a verdict | the `clear_bytecode_cache` **call** deleted | it exercised the helper directly and never the call site |
| an arm is watched when any operator is noticed | `any` swapped for `all` | its fixture's arms were killed by BOTH operators, so the two readings agree on every arm it looked at |
| the report separates the operators | the per-operator rows merged into one total | it asserted that the words `invert` and `remove` appear, and they also appear in the paragraph explaining the difference |

All four are fixed. The exit case now runs the mutating path over a fixture
with a survivor present. The cache case observes the call site. The
any-versus-all case uses `if a and b:` against a case passing `True, True` —
the one shape where exactly one operator kills, so the two readings differ.
The report case asserts the ROWS, one per operator, each carrying its own
killed and survived counts.

**The pattern across all four is the same and it is #310's lesson.** Each
asserted something true that was not the claim: a branch that was not the one
under test, a helper instead of its call site, a fixture where the distinction
could not appear, and a word instead of a structure. A case is only as good as
the mutation it has been seen to fail against, which is why the probe reports
`GREEN — VACUOUS` rather than a pass rate.

**The third is an arm no case kills, and it is reported rather than removed —
the checker's own verdict, applied to itself.** The per-arm restore is
watched, by a new case asserting that no second arm runs its command after a
restore that did not land; that is the property only the per-arm one can have,
and it is the defect the four fix passes met. The restore at the END of the
run is the redundant half: measured, the end-state case goes red only when
**both** are deleted. It is kept for one narrow path — an exception escaping
between the write and the inner `try`, a `clear_bytecode_cache` raising on a
permissions error — where nothing else puts the module back. That reasoning
sits at the coordinate, in the code.

**The splice reads a column offset as bytes, not characters.** `col_offset`
is a UTF-8 byte offset, and this repository's modules carry non-ASCII prose
throughout. Sliced as a character index the head keeps too much and the
mutation lands mid-token, which is a `SyntaxError`, which `mutate` catches and
reports as a *refused* arm — so the arm goes unmeasured and the reason is
invisible. Pinned with `if "é" == y or x:`.

**An arm with no defined mutation is refused, not reported unwatched.** A
match pattern is not an expression, so inverting it is unavailable, and a bare
`except:` has no type to aim elsewhere. `survived` on either would read as *no
case watches this* when the truth is *this was never tried*, so the report
counts and names them separately.

## `CONTRIBUTING.md` §What a change to a gate must carry

- **A test seen red.** All **35** cases in `tests/test_arm_check.py`, against
  **36** mutations of `skills/verify/scripts/arm_check.py`, one at a time —
  every case's own targeted mutation, plus one more for each of the two
  properties served by two mechanisms. 35 targets hit, **0 vacuous**. The
  checker was restored from held bytes and sha256-compared after every
  mutation (`7b58766b4e82` throughout the final set).

  **Four cases went green against the mutation aimed at them and were
  rewritten**, and that is the evidence worth more than the count — every one
  of them passed the suite and would have shipped. They are listed below.
- **Failure direction.** The checker **allows more**: report-only, exit 0
  whether or not an arm survived, so it refuses nothing today. It is the
  cheaper direction here because the first run's number is nine-ish arms
  nobody is fixing today — a check that goes red on history people cannot fix
  is a check people learn to skip (`chain_check.py:127`'s own argument). The
  enumeration's own failure direction is the opposite and deliberate: an
  unrecognised node type **raises**, because the alternative is a shorter
  count that still reads like a total.
- **Prompt budget: zero.** No hook, no gate, no question — a command a person
  or CI runs. Stated rather than omitted.
- **Platform honesty.** An AST walk, file writes and one subprocess; no
  process inspection. Two platform-specific things are handled rather than
  assumed: `col_offset` as a byte offset, and `sys.pycache_prefix` /
  `PYTHONPYCACHEPREFIX` when cached bytecode lives outside the source
  directory. **Executed on macOS (darwin 25.5.0, CPython 3.12.11) only.** The
  Windows and Linux legs are unverified by me; the `.cmd` wrapper is
  transcribed from `bin/survivor-check.cmd` and has not been run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The inline restore-and-compare inside `run_arms`'s loop | Moved to `restore()`, a function of its own, so its failure path is reachable by a case rather than only by a real failed run |
| Nothing else | none |
