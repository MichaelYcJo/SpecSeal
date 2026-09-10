# Round 1 — the sealer, its command, and its one cell

Reviewed at `610eb7d`, base `release/v0.10.0`, in a `git clone --no-local` of
the repository at that commit. There is no earlier round, so nothing was
inherited and every verdict below was derived here.

## What this round found, in the order one thing causes the next

The branch's premise is that a rule forbidding two agents an act and assigning
it to nobody is a rule assigned to whoever remembers. The design that answers
it is sound and the command works. Three things go wrong along the one path
the design cares about, and they are not independent.

**The gate can declare a seal over a check it just failed.** That is the first
finding, and it is the one the rest sit under: `broad-gate --record` reads only
one of the exit codes `round_record.py seal` can return.

**The row the branch chose as "the rounds have settled" is checked one round
early.** This is the branch's own mid-work change, from `Needs a fix` to
`Pass`, and it is the question the prompt asked directly. `Pass` answers *is a
finding open*; it does not answer *has the run ended*. The two part in a window
`skills/code-review/orchestration.md` names on its own page and calls red.

**Two instances of the class the branch swept were left standing**, and one of
them is inside the very function the branch corrected. The sweep's own record
says the class was enumerated; it was enumerated one short in two places.

The stamp module is the strongest part of the branch. Its one defect is that
the drawing is not reproducible below full scale.

---

## 🔴 1 — a seal exit that is not 2 prints the disc and returns 0

`skills/verify/scripts/broad_gate.py:504-516`.

```python
    if item is not None:
        code, text = seal_record(item, tree, args.base, root, args.base, keep)
        sys.stdout.write(text)
        if code == 2:
            ...
            return 2
    shape = args.shape or console_wants_letters
    rows = panel(tree, base, checks, item)
    sys.stdout.write("\n" + "\n".join(stamp.stamp(rows, args.scale, shape)) + "\n\n")
    return 0
```

`round_record.py seal` ends with `return run_check(root, ...)`, and
`run_check` returns `chain.main(...)`, which is `return 1 if errors else 0`
(`skills/code-review/scripts/chain_check.py:3436`). So `seal` returns **1**
whenever the chain check it runs after the write reports an error. The branch
above reads only `2`. Exit 1 falls through, the disc prints, and the command
returns 0 — while its own last check said the record is broken.

Why it matters, and why it is reachable: the module's docstring at `:47-50`
states the opposite contract — *"With `--record`, success is the checks green
AND the cell written"*. `seal_stamp.not_sealed`'s docstring states the
principle the code breaks — *"a picture that says sealed beside a word that
says not is read picture first"*. And the path is the one `seal`'s own
docstring describes as measured: CI found three Windows failures after the gate
had run, so the gate was re-taken at a later commit. At that point the pull
request is READY, `run_check` consults `gh`, judges as ready rather than draft,
and enables arms the gate's own draft-forced chain run at `:477-483` excused.
The sealer then reports *sealed, exit 0*, because reporting the exit code is
exactly what its definition tells it to do.

The same three lines carry a second, smaller falsehood. Exit 2 from `seal` has
two causes: a `Refused` raised **before** the write, and a chain check
returning 2 **after** it (`chain_check.py:3173`, `:3182`, `:3190`). The message
the gate prints for both says *"the record refused the cell, so nothing is
sealed"*. Measured on a fixture below: the cell was written and the exit was 2.

## 🔴 2 — `Pass` is checked before the verifying round, and `seal` writes there

`skills/code-review/scripts/round_record.py:2960-2971`.

The prompt asks whether `Pass` answers the question the cell needs answered,
and whether a state exists where `Pass` is checked and the run has not ended.
It does not, and one does.

`close` writes the box from the verdict table alone — `raw[boxes[0]] = f"- [{'
' if still_open else 'x'}] Pass"` at `:2851` — so the box is ticked the moment
a fix table applies. `close` does not touch `Fixes checked by` unless the value
is `no fixes to check`, so a record whose findings closed on a **fix** keeps
`nobody — the fixes are not yet written`. The verifying round is still owed.

`skills/code-review/orchestration.md:436-438` names that exact window:

> It is red once more from `close` ticking `Pass` until the verifying round's
> record commits, for the reason the check prints — `Pass` beside `nobody` on
> the last record — and that window is expected.

Twenty-eight lines later the same file says the sealer is spawned once the
rounds have settled, and `skills/verify/SKILL.md:285`, `agents/sealer.md:76`,
`agents/smith.md:190` and `agents/warden.md:57` all define that as the `Pass`
box being checked. So one file tells the orchestrator that the state is red and
tells it to spawn the sealer into it.

Measured, on the module's own fixtures: round 1 opened a finding, the fix
landed, `close` applied a table closing it `fixed`, no round 2 was generated.

```
Pass line          : ['- [x] Pass']
Needs a fix        : yes — 🔴 1
Fixes checked by   : nobody — the fixes are not yet written
records on disk    : ['round-1.md']
Broad gate after   : de1af3e against base
```

`seal` wrote the cell. What it costs is the run: the verifying round then
generates `round-2.md`, whose `Broad gate` reads `not yet`, and `chain_check`
reads the **last** record. The gate was spent, not banked — the rule
`CLAUDE.md` §*Verification Scope* states, broken by the row chosen to enforce
it.

The repair is not to put `Needs a fix` back. The row that answers *has the run
ended* is `Fixes checked by`, one line below `Pass`: it reads `nobody — …`
exactly inside this window, `no fixes to check` on a capped run — which is the
case the phase-5 change exists to admit — and a later `round-N` afterwards. It
is machine-read, it is the row `chain_check.checked_by` already refuses on, and
it costs the capped run nothing.

## 🟡 3 — the panel prints `lint  clean` whether or not a linter ran

`skills/verify/scripts/broad_gate.py:373`. The row is a literal:

```python
        ("lint", "clean"),
```

The `Broad gate` row is one shell command line and the gate cannot tell which
part of it is a linter — `templates/config.md:191` says so itself. A repository
whose row is only a test runner gets a seal asserting a check that never ran,
and the seal is the artifact a reader trusts precisely because it is drawn on
success alone.

## 🟡 4 — one failing file that the base does not carry makes every other one read `new`

`skills/verify/scripts/broad_gate.py:315-338`. The docstring claims the
verdicts are *"measured — never inferred"*.

Measured: pytest handed a path that does not exist exits 4 with `no tests ran`
and prints no `FAILED` line at all.

```
exit 4
no tests ran in 0.00s
failing_files() sees: []
```

`compare_at_base` passes every failing file to one run at the base. This
branch adds `tests/test_the_seal_is_taken_once_by_the_sealer.py`, which does
not exist at `release/v0.10.0` — so if the gate ever failed on this branch with
that file among the failures, every other failing file, including ones failing
on base too, would come back labelled `new`. The smith is told at
`agents/smith.md:287` to act on that word.

## 🟡 5 — a linter's warning count displaces pytest's counts on the seal

`skills/verify/scripts/broad_gate.py:344-349`. `suite_counts` walks the lines
backwards and returns the first `COUNTS_RE` match, and the row's linter output
stands after pytest's summary.

```
suite_counts("768 passed in 30s\nwarning: 2 warnings emitted\n") -> '2 warnings'
```

The panel's `suite` row is what a reader takes as how many tests ran.

## 🟡 6 — the same scale draws differently from one process to the next

`skills/verify/scripts/seal_stamp.py:186`.

```python
            row.append(max(set(ink), key=ink.count) if ink else ".")
```

`set` of strings iterates in an order that moves with `PYTHONHASHSEED`, so a
tie between two chart colours resolves differently per process. Measured over
five seeds at `--scale 0.75`: two distinct renderings.

```
distinct renderings across 5 seeds: 2
  A: '    oolm......GGGGGWGGG......mlOo     |  tree     c46fd2d …'
  B: '    oolm......GGGGGWWGG......mlOo     |  tree     c46fd2d …'
```

The module's own opening argument is that four hand-typed discs were lopsided
and *"a circle that is calculated cannot be off centre"*. A calculated circle
that is not reproducible gives that argument back at every scale but 1.0, and
any case that ever pins bytes below 1.0 will flake.

## 🟡 7 — `.github/scripts/run_tests.py` still says the run is the orchestrator's

`.github/scripts/run_tests.py:42-44`.

> The full suite takes about five minutes and is the orchestrator's, run once
> after the review rounds settle: `skills/agent-contract/SKILL.md` forbids it
> to smith and warden, which is why naming one module is the ordinary use.

`bin/test:23-26` is a five-line wrapper whose only act is
`exec python3 "$here/../.github/scripts/run_tests.py"`, and it was converted to
*the sealer's* in this branch. The sentence it wraps was not. The changelog
fragment claims *"the runner's own comment … All of them now say the sealer's"*
— true of the wrapper, false of the runner. Nothing pins this docstring:
`tests/test_the_suite_has_a_command_that_is_cheap_twice.py:152-157` asserts the
wording on `bin/test`, and the negative pin at
`tests/test_the_seal_is_taken_once_by_the_sealer.py:900` is applied to the two
agent definitions only.

This is the §12 class the prompt named, and it is its most literal instance:
one command, two files, two owners.

## 🟡 8 — the third refusal in the corrected function still says to run it by hand

`skills/code-review/scripts/chain_check.py:2988-2997`.

> "A broad run with an edit after it was spent, not banked. **Run it again now
> that the rounds have settled and write the new SHA into the cell**"

`chain_check.broad_gate` prints three fatal refusals. Two were re-pointed to
the sealer's spawn in this branch; the premature-SHA one, in the same function
and reached by the same reader at the same moment, names no agent and no
command. `seal/ledger/1789002694-…md`'s S9 records the class as *"`chain_check.py`'s
two refusals"*, and `survivors.md` §Phase 4 records the enumeration as
complete. It was one short, in the one function the branch opened.

## 🟡 9 — the gate never prints the command it sealed over

`skills/verify/scripts/broad_gate.py:469` runs the row's command; `run` writes
`$ <command>` into the kept output file at `:270` and nothing reaches stdout.

`agents/sealer.md:139-142` tells the sealer to *"quote the row's command and
let the reader judge it"*, and `agents/sealer.md:132` tells it to
*"name the command before you run it"* — `verify`'s first condition. The
sealer opens no repository file by its own rule, and the gate's output does not
carry the row, so the one thing the Seal Test asks for first is the one thing
the report cannot honestly contain.

## 🟡 10 — a fourth referent of `seal`, outside the sweep's file list

`docs/one-root-by-lifetime.md:135`.

> `seal/ledger*` is the seal itself: the binding of spec to code that breaks on
> drift.

`skills/verify/SKILL.md:158` states the new rule as *every reference to an
INSTANCE names whose*, and lists what may stay bare: the Seal Test, a seal
block, a counterfeit seal, SpecSeal itself. The evidence ledger is none of
those, and this is an instructing document. `tests/test_one_word_one_meaning.py:151-166`
sweeps a hand-written list of twelve files and `docs/one-root-by-lifetime.md`
is not on it — which is the same shape as finding 7 and 8: the class was closed
where somebody looked.

---

## Corrections — records, out of `Needs a fix`

| Where | What |
|---|---|
| `seal/ledger/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it.md:4` | The header says *"Nine rows"*; the table holds eleven (S1–S11). S10 and S11 arrived in `4cdc858` and the count did not move. The enumeration in the same paragraph stops at S8 |
| the same file, row S6 | Enumerates three refusals. `round_record.py#seal`'s own docstring says *"Two refusals"*, `agents/sealer.md:97` says *"refuses outright on two things"*, and the function has five `raise Refused` sites. The row's own Notes say a row enumerating three over a function with two would pass silently; that is the state it is now in. The case pinning the third, `test_seal_refuses_a_cell_with_no_sha_in_it`, is not among the row's coordinates |
| the same file, row S11 | *"the same table that holds the other ten"* — `RULES` in `tests/test_the_rules_have_one_owner.py` holds ten entries **including** this one, and that module's docstring says nine plus *"A tenth rule joined from #30"*. It is the other nine |
| the same file, row S11 | *"each carry a sentence naming that section rather than restating the rule"* — `agents/warden.md:24-26` restates the owner's sentence verbatim before linking. `test_every_link_names_the_owner` asserts only that the link is present, so nothing catches it |
| `seal/specs/1789002694-…/changelog.md:96-107` | *"It stood in nine places"*, then a nine-item list, then *"Two of the places were not documents at all but the failure messages the chain check prints"*. Those two are not in the list of nine, so it is eleven — or the second sentence should read *two more places* |
| pull request #332 body, Verified table | *"The work item's own module \| 26 cases"*. The module holds 35 test functions and collects 42 |
| pull request #332 body, Decisions left | *"measured by hand at 20,044 B"*. That was phase 3's reading of a 6,279 B definition; `agents/sealer.md` is 7,111 B at this head, so the payload is 20,876 B. Still the smallest of the four |
| `skills/verify/scripts/broad_gate.py:323-328` | When `git worktree add` fails, the function returns without removing the directory `tempfile.mkdtemp` created |
| `skills/verify/scripts/broad_gate.py:330` | `shlex.quote` builds POSIX quoting for a command line executed under `cmd.exe` on Windows. Unreachable while pytest node ids carry no spaces, and wrong the moment one does |
| `skills/verify/scripts/broad_gate.py:400-420` | `seal_record` takes `base_ref` and `base`, and its one caller passes `args.base` to both |
| `skills/verify/scripts/seal_stamp.py:365` | `not_sealed` pads the check name to 8; `survivors` is 9, so that one check's first line sits in the wrong column |
| `skills/verify/scripts/seal_stamp.py:157-163` | `check_scale` compares with `<` and `>`, so `--scale nan` passes. `broad_gate.main` catches `Refused` alone, so every check runs, the cell is written, and `stamp` then raises `ValueError: cannot convert float NaN to integer`. `not (SCALE_FLOOR <= scale <= SCALE_CEILING)` closes it |

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | a `seal` exit that is not 2 prints the disc and returns 0 | `skills/verify/scripts/broad_gate.py:504-516` | open | executed — `chain_check.main` returns `1 if errors else 0` at `chain_check.py:3436`; the branch reads only `2`. Fixture probe returned exit 2 with the cell already written |
| 🔴 2 | `Pass` is checked in the window before the verifying round, and `seal` writes there | `skills/code-review/scripts/round_record.py:2960-2971` | open | executed — fixture: `Pass` `[x]`, `Fixes checked by` `nobody — the fixes are not yet written`, one record on disk, cell written. `skills/code-review/orchestration.md:436` calls that window red |
| 🟡 3 | the panel asserts `lint  clean` whether or not a linter ran | `skills/verify/scripts/broad_gate.py:373` | open | read — the row is a literal beside four rows read from output |
| 🟡 4 | one failing file absent at base labels every other one `new` | `skills/verify/scripts/broad_gate.py:315-338` | open | executed — pytest exits 4 with no `FAILED` line, so `failing_files` returns `[]` |
| 🟡 5 | a linter's warning count displaces pytest's counts on the seal | `skills/verify/scripts/broad_gate.py:344-349` | open | executed — `suite_counts` returned `'2 warnings'` over a combined output |
| 🟡 6 | the disc is not reproducible below scale 1.0 | `skills/verify/scripts/seal_stamp.py:186` | open | executed — two distinct renderings at `--scale 0.75` across five `PYTHONHASHSEED` values |
| 🟡 7 | the runner behind `bin/test` still names the orchestrator | `.github/scripts/run_tests.py:42-44` | open | read — `bin/test:23` converted, the file it execs not; no case pins the docstring |
| 🟡 8 | the third refusal in the corrected function tells the reader to run it by hand | `skills/code-review/scripts/chain_check.py:2988-2997` | open | read — three fatal refusals in `broad_gate`, two re-pointed |
| 🟡 9 | the gate never prints the row's command it sealed over | `skills/verify/scripts/broad_gate.py:469`, `agents/sealer.md:132` | open | read — `run` writes it to the kept file only |
| 🟡 10 | a fourth referent of `seal`, in a file the sweep's list omits | `docs/one-root-by-lifetime.md:135` | open | read — `tests/test_one_word_one_meaning.py:151-166` lists twelve files, not this one |

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

Both probe files were named `test_tmp_probe.py` and `tests/test_tmp_probe_pass.py`,
run once in the clone and deleted; `git status` is clean and `git worktree list`
holds one entry. NAME NOT IN TREE

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A ledger coordinate whose hash is not eight hex characters is skipped in silence | `seal/specs/1789002694-…/questions.md` Q8 | the repository owner — already deferred by the branch, named here so it is not re-litigated |
| `payload-meter --agent sealer` | #292, pull request #329 | #292 — already deferred by the branch |

## Paste-ready fixes

**🔴 1** — `skills/verify/scripts/broad_gate.py`, replacing the `if code == 2:`
block:

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

**🔴 2** — `skills/code-review/scripts/round_record.py`, in `seal`, immediately
after the `Pass` refusal and before `named = chain.SHA_RE.findall(...)`:

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

**🟡 3** — `skills/verify/scripts/broad_gate.py`, in `panel`, replacing the
`("lint", "clean")` row:

```python
        # NOT `("lint", "clean")`. The row is one shell command line and
        # nothing in it says which part is a linter, so `clean` over a row
        # with no linter in it is the seal asserting a check that never ran.
        # What the gate actually measured is the row's exit code.
        ("row", f"exit {checks[SUITE].code}"),
```

**🟡 4** — `skills/verify/scripts/broad_gate.py`, the body of `compare_at_base`
inside the `try:`:

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

**🟡 5** — `skills/verify/scripts/broad_gate.py`, beside `COUNTS_RE` and
replacing `suite_counts`:

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

**🟡 6** — `skills/verify/scripts/seal_stamp.py`, in `shrink`, replacing the
`row.append(...)` line:

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

**🟡 7** — `.github/scripts/run_tests.py`, the docstring paragraph at `:42`:

```python
The full suite takes about five minutes and is the sealer's, run once after
the review rounds settle: `skills/agent-contract/SKILL.md` forbids it to smith
and warden, and `agents/sealer.md` is the agent it is assigned to, which is
why naming one module is the ordinary use.
```

and, in `tests/test_the_suite_has_a_command_that_is_cheap_twice.py`, beside the
case that pins the wrapper:

```python
def test_the_runner_behind_the_wrapper_says_the_same_thing():
    """`bin/test` is five lines and one `exec` into this file. #30 re-pointed
    the wrapper's comment from `orchestrator` to `sealer` and left the module
    it runs saying the other thing, which is one command with two owners."""
    runner = read("..", ".github", "scripts", "run_tests.py")
    assert "is the sealer's, run once after" in runner
    assert "is the orchestrator's" not in runner
```

**🟡 8** — `skills/code-review/scripts/chain_check.py`, the premature-SHA
message at `:2987-2997`, last two clauses:

```python
                        "— went through no broad gate at all. A broad run "
                        "with an edit after it was spent, not banked. Spawn "
                        "the `sealer` again now that the rounds have settled: "
                        "`broad-gate --base <base> --record <item>` re-takes "
                        "the run at the tree as it stands and writes the new "
                        "SHA into this cell"
```

**🟡 9** — `skills/verify/scripts/broad_gate.py`, immediately before the row's
command runs at `:469`:

```python
    # The first of the four conditions is to name the command before running
    # it, and the row is the only part of this run the gate did not choose.
    # `agents/sealer.md` asks the sealer to quote it, and the sealer opens no
    # repository file -- so it has to arrive here.
    sys.stderr.write(f"broad-gate: `{ROW}` says: {command}\n")
    checks[SUITE] = run(SUITE, command, root, keep, shell=True)
```

**🟡 10** — `docs/one-root-by-lifetime.md:134-136`:

```markdown
**What the names say.** `seal/specs/<id>/` holds the spec and its process
record. `seal/ledger*` is the binding of spec to code that breaks on drift —
what the product name seals, rather than one of the seals an agent takes
(`skills/verify/SKILL.md` §*Every agent seals what it verified, and one of
them is final*).
```

and, in `tests/test_one_word_one_meaning.py`, in `SEAL_SWEPT`:

```python
    ("docs", "one-root-by-lifetime.md"),
```

---

Needs a fix: yes — 🔴 1 and 🔴 2, and 🟡 3 through 🟡 10
Loses a record or crashes: no

---

## Proof block

```
· the two new scripts read whole — skills/verify/scripts/broad_gate.py,
  skills/verify/scripts/seal_stamp.py                          [read]
· round_record.py `seal`, `close`, `where`, `landing_values`, `run_check`;
  chain_check.py `broad_gate`, `checked_by`, `pass_checked`, `nobody_reason`,
  `main`'s exit codes, `CLOSED_WORDS`/`FIX_WORDS`                [read]
· the branch diff — git diff release/v0.10.0...610eb7d --stat, and the full
  diff of round_record.py, chain_check.py, agents/smith.md, agents/warden.md,
  skills/code-review/orchestration.md, skills/verify/SKILL.md,
  docs/review-chain-spec.md, templates/config.md, templates/sdd-round.md,
  skills/config/SKILL.md, README.md, README.ko.md, CLAUDE.md, CONTRIBUTING.md,
  bin/test, docs/flow.md, docs/review-handoff-protocol.md,
  tests/test_broad_gate_rule.py, tests/test_the_rules_have_one_owner.py [read]
· the work item — spec.md, plan.md, questions.md, overview.md, routing.md,
  changelog.md, survivors.md, rounds/round-1-asked.md                 [read]
· agents/sealer.md whole; agents/*.md frontmatter                     [read]
· tests/test_the_seal_is_taken_once_by_the_sealer.py — case list, fixtures,
  helpers; tests/test_one_word_one_meaning.py's seal sweep             [read]
· bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py -q
  → 42 passed in 13.90s (exit 0)                                  [executed]
· bin/test tests/test_broad_gate_rule.py -q → exit 0              [executed]
· nine probes, one file, run once, deleted — the worktree axis, the shrink
  seeds, the twin's dimensions, the colour count, nan, the absent base file,
  suite_counts, first_command, and the fixture that writes the cell early
                                                                  [executed]
· the phase records' `seen red` claims — not re-derived; each would need the
  code or the sentence restored and the case re-run       [unverified: the
  orchestrator, or a later round with the held bytes the phases name]
· the full suite, the repository-wide lint, the typecheck  [unverified: the
  sealer, which is what this work item creates]
· broad gate: not yet — due when the last round record's `Pass` is checked,
  and finding 🔴 2 is about that row
· red proven: none — a review round plants no cases; every finding above was
  either executed against the shipped code or read at a coordinate
```

The phase records' *seen red* claims are the one axis of this round that stays
unverified rather than passing. `plan.md` says each case was shown failing
against code and documents restored from held bytes, and re-deriving that means
restoring those bytes for thirty-eight cases. Finding 🔴 2 is the one place the
question bites: the case that pins the phase-5 change,
`test_seal_writes_over_a_capped_runs_needs_a_fix`, is red against the old
refusal and green now — and it is green over the window this report says the
new row admits, because the fixture it uses never builds that window.
