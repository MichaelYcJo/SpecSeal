# 1790815610 — review round 2 report (verifying round)

Ran by: specseal:warden on claude-opus-5-5.
Target SHA: `8b8149b3af8f216e3a3121ee9d0c7ecb8dbc4d21`. Diff verified: round 1's
fix range `d6ce226a..2d47fbbd` (four commits), in a `git clone --no-local` at
the target. `3b9691d4` and `8b8149b3` are paperwork after the range; they were
read through `evidence-check`, not reviewed line by line.

## What this round found, in order of cause

Round 1's fixes do close all eight of its verdicts. Every probe round 1 ran
was run again. Each now gives the verdict its finding asked for. Two
problems sit in what those fixes added, and both are in `mutation_run`:

1. The baseline run that closes 🔴 1 has its own bound, and no case pins
   it (🟡 10). Most hangs do not depend on the break, so they now hit the
   baseline first.
2. The `except BaseException` arm that closes 🟡 2 also fires when the
   break was never written (🟡 9). A target that is read-only before the
   command starts reads `not restored`, and the line tells the person to
   restore from their commit. The file still holds its original bytes.

Four ⬜ follow. Two are documents that still describe one run per call. One
is the wording of the baseline's own verdict lines. One is a pair of
paperwork corrections.

### Round 1's verdicts: each is closed, and how this round knows

- **🔴 1 — a failure without the break read `red`. Closed.** Executed: I re-ran
  round 1's three probes against a file no case imports. They were a `-k` that
  selects nothing, a module path that does not exist, and a planted test file
  whose one case fails. Each printed `no baseline: …`, exit 2, and the file
  still read `VALUE = 1`. Mutating the baseline's red check, its propagation of
  a non-verdict, and the removal before the baseline each turned a case red
  (M7, M10 below). The fix pass named the same mutations, and they hold.
- **🟡 2 — a restore whose write raised escaped `NotRestored`. Closed.**
  Executed: cases that `chmod` the target read-only once it holds the mutant
  printed `not restored: … PermissionError …`, exit 2, with no traceback. The
  mutant stays on disk, because the write back cannot land, and the line says
  so. The interrupt half that round 1 flagged by reading was executed in
  process: I substituted a `restore` that wrote three bytes and then raised
  `KeyboardInterrupt`. The result was `not restored: … raised KeyboardInterrupt`,
  exit 2, and the file read `VAL`, so the line was true. A real SIGINT landing
  at that instant was not executed. Dropping the arm (M3) turned
  `test_a_restore_whose_write_raises_is_not_restored_and_exits_two` red. The
  class is not closed: 🟡 9 is the same arm firing when the break was never
  written.
- **🟡 3 — an unnamed exception exited 1. Closed.** Executed: a missing path
  and a directory each printed `could not run: FileNotFoundError` or
  `IsADirectoryError`, exit 2, with no traceback. M8 (the arm dropped) was red.
- **🟡 4 — the wait was on the pipe. Closed.** Executed: cases that exit 1 at
  once on the mutant and leave a same-group child holding the output read
  `red` in 0.2 s under `--timeout 3`, and the child was gone afterwards. With
  the child in a session of its own, the verdict was still `red` in 0.4 s and
  the escaped child was still alive. That is the documented limit, and I ended
  the child myself. M5 (no group kill after a normal exit) was red.
- **🟡 5 — the `not restored` word and the replaced decode were unpinned.
  Closed.** Executed: renaming `NOT_RESTORED` (M11), `errors="strict"` on the
  sink (M4), and dropping the elapsed time from the verdict line (M12) each
  turned a case red.
- **⬜ 6 — Q1 misdescribed the smith's example. Closed.** Read:
  `questions.md` Q1 carries a `Corrected 2026-10-01` note. The example at
  `agents/smith.md:268-270` names no `-p no:xdist`, and the prose at
  `:280-282` does.
- **⬜ 7 — relative `PYTHONPYCACHEPREFIX` with `--cwd`. Answered, and the
  answer holds.** Read: the defect is in `arm_check.py`'s
  `clear_bytecode_cache`, which this branch does not edit. `overview.md`
  §*Not verified* records it.
- **⬜ 8 — the verdict "names the exception". Closed.** Read: the SKILL
  section and the docstring now say the verdict names the bound's limit and
  cannot tell whether a process escaped.

### The bound through `bin/test`, re-run because the wait changed

Executed: `mutation-check --timeout 8` over `bin/test` running two 40 s
cases, under `-n auto` and under `-p no:xdist`. Both read `timed out after
8s … before the mutation was written`, exit 2, after 8–9 s. `pgrep` found
nothing afterwards, and the target was unchanged. The hang now lands in the
baseline, which is 🟡 10's point. The group kill reaches xdist workers there
too.

### 🟡 9 — a target that was read-only from the start reads `not restored` over its original bytes

`skills/verify/scripts/mutation_check.py:337-350`. The mutant's write at
`:331` raises `PermissionError` before a byte lands. The `finally` then calls
`restore`, whose own write raises the same error. The new `except
BaseException` arm turns that into `NotRestored`. Executed: a target that was
`chmod 400` before the command ran printed `not restored: … was not restored:
writing it back raised PermissionError … Restore it from your own commit
before anything else reads it.`, exit 2. The file still read `VALUE = 1\n`.

Why it matters: `not restored` is the one verdict that tells a person to act
on the file. `agents/smith.md` §Boundaries says what that act costs when it is
taken from HEAD over uncommitted work: a round's work was wiped mid-loop.
Here the instruction comes with nothing to restore. The exit code is right,
since nothing was measured. The verdict word and the instruction are wrong.

The fix is the one fact the `finally` lacks: whether the file differs from
the bytes read at the start. Compare first, and restore only when it
differs. Then the write's own `PermissionError` reaches `main`'s new
`except Exception` arm and reads `could not run: PermissionError …`, exit 2.
That is true. Every other restore path is unchanged. A truncating write that
failed halfway hashes differently, so it is still restored, and a file the
cases deleted reads as differing, so it is still written back. Executed in
the clone: the case below was red at the target. With the fix applied, the
module passed (38 passed, the two new cases included). The patch was then
reverted.

### 🟡 10 — the baseline's bound is pinned by no case

`skills/verify/scripts/mutation_check.py:319`. Executed: replacing the
baseline's `timeout=timeout` with `timeout=None` SURVIVED against the whole
module (M1). Every fixture that reaches the bound passes at once against the
original, so the bound they reach is always the mutated run's. That includes
STARTS_A_CHILD and its escaped variant, which round 1's fixes rewrote to do
that. L7 claims *a baseline that times out or cannot start says it was the
baseline*, and its anchors pin only the cannot-start half.

Why it matters: a hang that does not depend on the break used to happen in
the mutated run. It now happens in the baseline, before anything is written.
That makes the baseline's bound the one most hangs meet, and it is the bound
this work item exists for: the 32-minute hang. Without a case, a later edit
can drop that bound silently. Executed in the clone: the case below passed at
the target. Under M1 it was red twice, on the missing `before the mutation
was written` and on 31 s elapsed. That is how §15 was shown for it.

### ⬜ 11 — two step lists still describe one run per call

`agents/smith.md:271-276` and `bin/mutation-check:11-15` each list the
command's steps as *refuses …, writes the break, removes …, runs the cases
under a bound (300 s …), restores …*. Neither names the run against the file
as it is. Neither says the bound applies to each of two runs, so a call can
take twice the bound. `skills/verify/SKILL.md` and the docstring were updated,
and these two were not. §12 counts four members in this class, and two are
closed. The behaviour and the verdict list (*a run that measured nothing*)
stay right, so this is ⬜ under the findings format. L4 says
`agents/smith.md` is untouched and its claim holds, and the claim it pins
does hold. What it pins is not the step list.

### ⬜ 12 — the baseline's own verdict lines

Three lines describe the baseline. Each is either worded loosely or not fully
pinned:
- `no baseline` drops the baseline's exit code. The `before` detail it
  replaces carries it, at `:320-326`. pytest's 5 and 4 are what tell a
  mistyped `-k` from a failing case. The sentence *Nothing was written* is
  pinned by no case (M9 SURVIVED). The cases do check the file, but not the
  sentence.
- A Ctrl-C during the baseline prints `interrupted: … was restored from the
  bytes read before the write` (`:418-427`), and no write had happened.
  Executed in process: P7b. The file was intact, so what the person is told
  to believe is true, but the sentence describes an event that did not occur.
- A baseline timeout reads *…unless it put itself in a session of its own,
  before the mutation was written*. The suffix (`:328`) attaches to the escape
  clause rather than to the verdict.

### ⬜ 13 — correction: `questions.md` Q5 still states the per-call figures

`seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md:42`
answers Q5 with *0.84 s through the command … 0.47 s with `-p no:xdist`* and
no note. L5 carries the `Corrected` note: *each call now runs the cases twice,
about twice the 0.47 s, by reading and not re-timed*. Q5 does not. Executed
this round, on L5's own setup (`arm_check.py`'s `clear_bytecode_cache`
broken, `tests/test_arm_check.py -q -k "cache or restore" -p no:xdist`, five
runs after a warm-up): `mutation-check` took 0.96–1.07 s, mean 1.01 s. One
bare `bin/test` run of the same cases took 0.41–0.47 s. So L5's *about twice*
holds, and the figure can be stated as measured. `phases/phase-4.md` is a
dated record of what was timed then, and I leave it as it is. This is
paperwork, outside `Needs a fix`.

### ⬜ 14 — correction: the ledger fragment's header does not list L7

`seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md:1-8`
describes the rows as L1–L6, and L7 sits between L5 and L6. This is
paperwork, outside `Needs a fix`.

### The three things the prompt also asked

- **The interrupt during the restore write.** It is handled, and the result is
  above under 🟡 2: `not restored`, exit 2, and the partial file is reported
  truthfully.
- **`evidence-check .`, unscoped.** Executed at the target: exit 0, total 3195
  ok · 0 drifted · 0 broken · 0 overflow. The records arm read 1 work item
  with 0 drifted and 0 refused.
- **`survivor-check`'s one exempted place.** Executed: `--range
  d6ce226a..2d47fbbd` without `--exempt` exits 1 on `plan.md:164` alone. With
  `survivors.md` it exits 0, and so does the range through the target. The
  grounds hold. Read: `plan.md:164` is the approved plan's own quote of L1.
  Rewriting it would misstate what the owner approved. What it says, *before
  the cases run and after the restore*, is still true of the mutated run,
  which is the run it describes.
- **The baseline's cost in the records.** L5's correction note is honest, and
  this round's timing agrees with it (⬜ 13). `skills/verify/SKILL.md` gives
  the bound per run and states no per-call figure. Q5 is the one record that
  still states one, and ⬜ 13 covers it. The changelog fragment gives no cost.

### Carried, not re-established

- Round 1's 🟢 class rows (`tests/__pycache__` named nowhere,
  `PYTHONDONTWRITEBYTECODE=1` in both modules, the five re-stamped release
  rows): this range does not touch them. `evidence-check` is green over them.
- Round 1's ❓ on the Windows arm stays out of scope. One new fact is read and
  not run. The CHILD arm's comment at `:219-220` cites
  `Popen.send_signal`, and on Windows `Popen.kill` is `terminate`. CPython's
  own source, read here, shows that `terminate` returns early when
  `returncode` is set. So the no-op holds, though the comment names the other
  method. On Windows, the output now goes to a temporary file handed to the
  child, and that is also unexecuted.

## Regression tests to plant

Destination: `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py`,
at the end of the module. Both bodies are in *Paste-ready fixes*. Both were run
in the clone: the bound case was green at the target and red under M1. The
read-only case was red at the target and green with the fix.

## Facts for the evidence ledger

- L7's anchors pin only the cannot-start half of *a baseline that times out
  or cannot start says it was the baseline*. Once 🟡 10's case is planted,
  add it to L7's anchors.
- L3's claim *a restore that did not land, whether its hash differs or its
  write raises* needs the qualifier that 🟡 9's fix makes true: *a restore
  attempted over bytes that differ*. A target the break never reached is
  `could not run`.
- L5 can say *measured 2026-10-01 in round 2: 1.01 s mean per call against
  0.43 s for one run* instead of *by reading and not re-timed*, if the fix
  pass chooses to.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking finding 1 is closed — a failure without the break is `no baseline`, exit 2, nothing written | `skills/verify/scripts/mutation_check.py:313-328` | confirmed | Executed: a `-k` selecting nothing, a missing module and an already failing case each printed `no baseline`, exit 2, file unchanged; M7 and M10 red |
| 🟢 | round 1's finding 2 is closed — a restore whose write raises, an interrupt inside it included, is `not restored`, exit 2 | `skills/verify/scripts/mutation_check.py:337-350` | confirmed | Executed: cases that lock the mutant gave `not restored … PermissionError`, exit 2; a substituted restore that wrote three bytes and raised `KeyboardInterrupt` gave `not restored`, exit 2, file `VAL`; M3 red. The class reaches 🟡 9 |
| 🟢 | round 1's finding 3 is closed — an unnamed exception is `could not run`, exit 2 | `skills/verify/scripts/mutation_check.py:428-438` | confirmed | Executed: a missing path and a directory each exit 2 with no traceback; M8 red |
| 🟢 | round 1's finding 4 is closed — cases that exit but leave a child on the output read at once | `skills/verify/scripts/mutation_check.py:196-267` | confirmed | Executed: `red` in 0.2 s under `--timeout 3`, child gone; escaped child: `red` in 0.4 s, child alive (the documented limit); M5 red |
| 🟢 | round 1's finding 5 is closed — the `not restored` word and the replaced decode are pinned | `skills/verify/scripts/mutation_check.py:116`, `:244` | confirmed | Executed: M11, M4 and M12 (the elapsed time) each red |
| 🟢 | round 1's note 6 is closed — Q1 names where `-p no:xdist` is written | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md` | confirmed | Read: the Q1 cell and its `Corrected` note; `agents/smith.md:268-282` |
| 🟢 | round 1's note 7 is answered — the relative-prefix defect predates the branch | `skills/verify/scripts/arm_check.py:783-789` | confirmed | Read: `overview.md` §Not verified records it; `arm_check.py` is not edited in the range |
| 🟢 | round 1's note 8 is closed — the escape sentence names a limit, not an event | `skills/verify/SKILL.md` §*`mutation-check` asks condition 2 of one unit* | confirmed | Read: the SKILL paragraph and the module docstring |
| 🟢 | The group bound still reaches pytest and its xdist workers through `bin/test`, now in the baseline | `skills/verify/scripts/mutation_check.py#run_cases` | confirmed | Executed: 8 s bound, `-n auto` and `-p no:xdist`, `pgrep` empty, target unchanged |
| 🟢 | The one survivor is exempted on sound grounds | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/plan.md:164` | confirmed | Executed: `survivor-check` exit 1 without the table, exit 0 with it; Read: the plan quotes the claim as approved, still true of the mutated run |
| 🟢 | L5 says the baseline doubles a call's cost, and the figure holds | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md` L5 | confirmed | Executed: 1.01 s mean per call against 0.43 s for one run, on L5's setup |
| 🟡 9 | A target read-only before the command starts reads `not restored` and is told to be restored from a commit, though the break never reached it | `skills/verify/scripts/mutation_check.py:337-350` | open | Executed: `chmod 400` before the run gave `not restored … PermissionError`, exit 2, file `VALUE = 1`; the proposed case red at the target, green with the fix |
| 🟡 10 | The baseline's bound is pinned by no case, and it is now the bound most hangs meet | `skills/verify/scripts/mutation_check.py:319` | open | Executed: `timeout=None` on the baseline SURVIVED the module (M1); the proposed case red under M1 |
| ⬜ 11 | The smith's step list and the wrapper's comment omit the baseline and the bound per run | `agents/smith.md:271-276`, `bin/mutation-check:11-15` | open | Read: SKILL and the docstring were updated, these two were not; behaviour and verdict list stay right |
| ⬜ 12 | The baseline's verdict lines: `no baseline` drops the exit code and its *Nothing was written* is unpinned; `interrupted` in the baseline says the file was restored; the timeout suffix lands on the escape clause | `skills/verify/scripts/mutation_check.py:320-328`, `:418-427` | open | Executed: M9 SURVIVED; Ctrl-C substituted into the baseline's wait printed *was restored from the bytes read before the write* |
| ⬜ 13 | correction: Q5 states the per-call command figures with no note that a call now runs the cases twice | `seal/specs/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout/questions.md:42` | open | Read; L5 carries the note, Q5 does not. Paperwork, outside `Needs a fix` |
| ⬜ 14 | correction: the ledger fragment's header lists L1–L6 and not L7 | `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md:1-8` | open | Read. Paperwork, outside `Needs a fix` |
| ❓ | The Windows arm: `proc.kill()`, its text, the temporary-file output, and `bin/mutation-check.cmd` | `skills/verify/scripts/mutation_check.py:218-221`, `bin/mutation-check.cmd` | ❓ out of verified scope | No Windows machine here; carried from round 1. Who answers it: the orchestrator, from the `windows-latest` leg of `.github/workflows/test.yml` on the pull request |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the work item's module, `-q -p no:xdist`, at the target | exit 0; 36 passed |
| `mutation-check` on a scratch target, `--tests "bin/test tests/test_arm_check.py -q -p no:xdist -k <a name no case has>"` | `no baseline`, exit 2, file unchanged |
| The same with a module path that does not exist | `no baseline`, exit 2, file unchanged |
| The same with a planted test file whose one case fails | `no baseline`, exit 2, file unchanged; the file was removed afterwards |
| Cases that make the target read-only once it holds the mutant | `not restored … PermissionError`, exit 2, no traceback; file `VALUE = 2` |
| A target read-only before the command starts, cases red only on the mutant | `not restored … PermissionError`, exit 2; file `VALUE = 1` (🟡 9) |
| A missing path, and a directory | `could not run: FileNotFoundError` / `IsADirectoryError`, exit 2, both |
| Cases that exit 1 on the mutant leaving a same-group child on the output, `--timeout 3` | `red`, exit 0, 0.2 s; child gone |
| The same with the child in a session of its own | `red`, exit 0, 0.4 s; child alive, ended by hand |
| Cases that sleep whatever the file holds, `--timeout 2` | `timed out after 2s … before the mutation was written`, exit 2, 2.2 s; file unchanged |
| In process: `restore` substituted by one that writes three bytes and raises `KeyboardInterrupt` | `not restored … KeyboardInterrupt`, exit 2; file `VAL` |
| In process: `KeyboardInterrupt` raised from the baseline's wait | `interrupted … was restored from the bytes read before the write`, exit 2; file unchanged; nothing had been written (⬜ 12) |
| `bin/mutation-check` on `mutation_check.py`, whole module `-x -p no:xdist`: M1 the baseline's `timeout=None` | SURVIVED (🟡 10) |
| The same: M2 the removal between the write and the mutated run | red: the baseline-cache case |
| The same: M3 the restore's `except BaseException` arm | red: the restore-raises case |
| The same: M4 `errors="strict"` on the sink | red: the non-UTF-8 case |
| The same: M5 no group kill after a normal exit | red: the child-on-the-output case |
| The same: M6 the baseline suffix dropped | red: the cannot-start case |
| The same: M7 the baseline's propagation of a non-verdict | red: the cannot-start case |
| The same: M8 `main`'s `except Exception` arm | red: the unreadable-path case |
| The same: M9 *Nothing was written* dropped from the `no baseline` detail | SURVIVED (⬜ 12) |
| The same: M10 the removal before the baseline | red: S1 |
| The same: M11 `NOT_RESTORED` renamed | red: the restore-did-not-land case |
| The same: M12 the elapsed time dropped from the verdict line | red: the red-and-exit-zero case |
| `git status --porcelain` in the clone after the mutations | empty |
| `mutation-check --timeout 8` over `bin/test` running two 40 s cases, `-n auto` and `-p no:xdist` | `timed out after 8s … before the mutation was written`, exit 2, 8–9 s; `pgrep` empty, both |
| Five `mutation-check` calls on L5's setup, `-p no:xdist`, after one warm-up, interleaved with one bare `bin/test` run each | all red; 0.96–1.07 s per call, mean 1.01 s; one run 0.41–0.47 s |
| The two proposed cases at the target | the bound case passed; the read-only case failed (`not restored`) |
| The bound case under M1 | red: suffix missing, 31.0 s |
| The module with 🟡 9's fix and both cases applied in the clone | exit 0; 38 passed; reverted afterwards |
| `bin/evidence-check .`, unscoped | exit 0; 3195 ok, 0 drifted, 0 broken; records 1 work item read, 0 drifted |
| `bin/survivor-check --range d6ce226a..2d47fbbd`, without and with `--exempt survivors.md`; and `d6ce226a..8b8149b3` with it | exit 1 on `plan.md:164` alone; exit 0; exit 0 |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet: nobody has run it on this branch. It is the sealer's once the rounds settle, and it is not due while 🟡 9 and 🟡 10 stand |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `skills/verify/scripts/arm_check.py`'s `run_arms` reads any non-zero exit as killed with no baseline: round 1's finding 1 class, in a file C2 keeps unedited (already deferred in round 1) | a new issue, beside #313 | the orchestrator, who files it when the pull request is opened |

## Paste-ready fixes

### 🟡 9 — compare before restoring

In `skills/verify/scripts/mutation_check.py`, above `mutation_run`:

```python
def _sha_on_disk(path: str) -> str | None:
    """The sha256 of what `path` holds now, or None when it cannot be read."""
    try:
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None
```

And the head of `mutation_run`'s `finally`, the two `except` arms below it unchanged:

```python
    finally:
        try:
            # A write that never reached the file -- it was read-only before
            # the command started -- leaves nothing to put back, and a restore
            # tried anyway raises the same error and reads `not restored`
            # over a file that holds its original bytes (round 2, 🟡 9).
            if _sha_on_disk(path) != original_sha:
                restore(path, original, original_sha)
        except RuntimeError as exc:
```

The case, at the end of `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py`:

```python
@pytest.mark.skipif(
    os.name != "nt" and os.geteuid() == 0, reason="root writes a read-only file"
)
def test_a_target_that_cannot_be_written_is_not_called_unrestored(tmp_path, capsys):
    """Round 2, 🟡 9. A target that is read-only before the command starts
    never takes the break and holds its original bytes, so `not restored`
    there tells a person to restore a file nothing changed."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    os.chmod(target, 0o444)
    try:
        code, out = run(
            [
                target,
                "--replace",
                "VALUE = 1",
                "VALUE = 2",
                "--tests",
                red_on(tmp_path, target, "VALUE = 2"),
            ],
            capsys,
        )
    finally:
        os.chmod(target, 0o644)
    assert code == 2, out
    assert out.startswith("could not run:"), out
    assert "PermissionError" in out, f"the cause is not named: {out}"
    assert target.read_text(encoding="utf-8") == "VALUE = 1\n"
```

### 🟡 10 — pin the baseline's bound

At the end of the same module:

```python
def test_a_baseline_past_the_bound_is_timed_out_and_writes_nothing(tmp_path, capsys):
    """Round 2, 🟡 10. A hang that does not depend on the break -- the common
    kind -- now happens in the baseline, before anything is written, so that
    run's bound is the one most hangs meet."""
    target = tmp_path / "target.py"
    target.write_text("VALUE = 1\n", encoding="utf-8")
    log = tmp_path / "seen.txt"
    appends = SEES_FILE.replace('"w", encoding', '"a", encoding')
    assert appends != SEES_FILE, "the fixture did not change"
    body = appends + "import time\ntime.sleep(30)\n"
    started = time.monotonic()
    code, out = run(
        [
            target,
            "--replace",
            "VALUE = 1",
            "VALUE = 2",
            "--tests",
            cases_command(probe(tmp_path, body), target, log),
            "--timeout",
            "1",
        ],
        capsys,
    )
    elapsed = time.monotonic() - started
    assert code == 2, out
    assert out.startswith("timed out after 1s"), out
    assert "before the mutation was written" in out, out
    assert elapsed < 10, f"the baseline was not bounded: {elapsed:.1f}s"
    assert target.read_text(encoding="utf-8") == "VALUE = 1\n"
    assert log.read_text(encoding="utf-8") == "VALUE = 1\n"
```

### ⬜ 11 — the smith's step list (optional)

```
   It refuses an `<old>` that does not occur exactly once, runs the cases
   against the file as it is and stops with `no baseline` if they already
   fail, writes the break, removes the mutated file's cached bytecode for
   every interpreter tag, runs the cases again, each run under a bound (300 s
   unless `--timeout` says otherwise), puts the file back from the bytes it
   read first and compares the hash, and prints `red`, `SURVIVED`, or a run
   that measured nothing.
```

Needs a fix: yes — 🟡 9 (a read-only target reads `not restored` over its original bytes) and 🟡 10 (the baseline's bound is pinned by no case)
Loses a record or crashes: no

## Proof block

Files opened this round, at the target in the clone unless noted:
- `skills/verify/scripts/mutation_check.py` (lines 60–450, and the range diff)
- `tests/test_a_mutation_clears_one_files_bytecode_and_ends_at_a_timeout.py` (the range diff, helpers, SEES_FILE, the tail)
- `skills/verify/scripts/arm_check.py` (`restore`, `clear_bytecode_cache`)
- `skills/verify/SKILL.md` (lines 125–200, and the range diff)
- `agents/smith.md` (lines 255–295, 392–402)
- `bin/mutation-check`, `bin/mutation-check.cmd`, `bin/test` (head)
- `seal/ledger/1790815610-a-mutation-clears-one-files-bytecode-and-ends-at-a-timeout.md`
- In the work item: `changelog.md`, `overview.md` (diff), `questions.md` (diff and Q5), `phases/phase-2.md` (diff), `phases/phase-4.md` (lines 22–45), `plan.md` (lines 155–170), `survivors.md`, `routing.md`, `rounds/round-1.md`
- CPython's `subprocess.Popen.terminate` source, read through `inspect`
