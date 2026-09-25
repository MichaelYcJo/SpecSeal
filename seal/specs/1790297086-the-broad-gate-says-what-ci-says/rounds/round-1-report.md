# 1790297086-the-broad-gate-says-what-ci-says — review round 1 report

First round. Target SHA `8f5ae44f`, reviewed against `origin/release/v0.15.4`
(`7b557144`); build range `cf5428b1..8f5ae44f` on top of the frame `6e93c352`.
Read in a `git clone --no-local` at `8f5ae44f` under the session scratchpad
(`<scratchpad>/item-d/round-1/clone`). Nothing was written in the worktree
except this file. No earlier `round-N.md` exists, so the implementer's
account (`overview.md`, the phase records, the ledger notes) was the only
other voice, and every claim of it used below was checked against the code.

## Summary

The four slices meet the spec on the axes it names. The directory predicate
is asked where the row runs, and that holds for `compare_at_base` as well.
The workflow reader is one rule and is driven. The guard at `main` is keyed
and pinned the way S3 says, and #499's case asserts on names rather than on a
bare word. The two ledger corrections are sound.

Three things need a fix, and the first two are about CI rather than about the
design.

- **🔴 1. CI's `release` job is already red at the target SHA.** The
  survivor step reports three sentences the branch removed that still stand
  elsewhere, and nothing records them.
- **🔴 2. The C1 case pins the skip line with `/` in the workflow's path.**
  The gate builds that path with `os.path.join`, so on `windows-latest` the
  line reads `.github\workflows\hygiene.yml` and the exact-line assertion
  should fail. That leg was still running when this report was written.
- **🟡 3. A command name rooted in `%VAR%` stopped being rewritten.** 0.15.3
  handed `%CD%/bin/test` over as `%CD%\bin\test`, and this branch hands it
  over as written. The spec names two bounds, and this is a third one that
  nobody named.

The rest are ⬜: a code comment and a ledger claim that the new guard made
imprecise, the guard's spelling-keyed edges, a gap in the comment rule, a
line the sealer is not told to relay, and an `@` inconsistency.

## Spec compliance

- **S1 / #596 (read and executed).** `handed_to_shell` builds the predicate
  from `run`'s `root` (`broad_gate.py:1304-1307`). `compare_at_base` calls
  `run("suite-at-base", runner, scratch, …)`, so a name there is judged
  against the scratch worktree (A5 holds). Every caller of both changed
  functions was enumerated with `grep` over the tree. Two are shipped code
  (`run` → `handed_to_shell` → the scan), and the rest are cases, all of
  which pass `root`. The shapes the prompt named behave as S1 says, executed
  against both `7b557144` and `8f5ae44f`. A quoted name, a caret-opened name
  and an `@`-opened name are judged on the part with those characters
  removed. An empty part (`/abs/x`, `""/x`) counts as the root and is still
  rewritten. A `..` part is a directory wherever the row runs. `C:/tools/x`
  is judged only on real Windows, where `os.path.join(root, "C:")` is `C:`.
  One shape regressed (🟡 3), and `@@` is inconsistent (⬜ 9).
- **S2 / #482, #462, #463 (read and executed).** The six enumerated sites use
  the reader. `workflow_steps` over the real `hygiene.yml` yields the same 13
  named `release` steps as `broad_gate.py#job_steps`. `code_line` handles a
  `#` inside `"…"` and `'…'`, a `#` after a URL (`https://example.com/#x`
  kept), and a tab before a comment. It gets a backslash-escaped quote and a
  quoted string spanning lines wrong (⬜ 7). `keyed_under_env` rejects
  `with:` and `run: |`. `base_spellings` returns `""` for `--baseline ""`,
  and `--baseline ''` fails the spelling check by name as well.
- **S3 / #473 (read and executed).** `skipped_at_main` strips one `origin/`
  and compares against `main`, and it asks only whether the `release` job
  carries the step's name (⬜ 6 on what that condition leaves). C3's regex
  stops matching once the guard is mutated, and it does not read an echo
  that falls through to a later `exit 0` as a skip. I ran it over both.
  Nothing downstream reads the two `checks` entries: the panel reads only
  suite, ledger and chain, and no other script names `survivors.txt` or
  `corrections.txt` in the kept output.
- **S4 / #499 (read).** The needles are `` `release` ``, the workflow path
  and every `PARTITION` step name. None of them can occur in a path by
  accident.
- **The corrections (read).** `seal/releases/0.15.3.md` A2 was corrected in
  place. Its claim gained the directory condition, the dead anchor on the
  renamed bound case is gone, and a dated **Corrected** note follows round 2's
  note. `seal/releases/0.12.2.md` G4 carries a **Corrected** note, and its
  claim still holds: `test_a_merge_that_dropped_a_correction_is_not_sealed`
  calls `run_gate` with the default `base="base"`. The note that stays behind
  on A2 is one of 🔴 1's three survivors.

## Findings

### 🔴 1 — CI's `release` job is red at `8f5ae44f`, and the three survivors have no row

**Executed, and read from CI.** The PR's `hygiene` run 36084469701 has head
SHA `8f5ae44f`, and its step *wording this branch removed is not still
standing elsewhere* failed. I ran the same check locally over
`7b557144...HEAD` and it reports the same three places at exit 1:

- `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md:169`: *telling a program from a directory is #596.*
- the same file, `:167`: *A switch written with a blank before it (`xcopy /e`) is left as written, and the template says so;*
- `seal/releases/0.15.3.md:60`, round 2's note on A2: *… and #596 holds the behaviour fix.*

**Why it matters.** The PR cannot merge while this step is red. The sealer's
survivor arm asks the same question against `release/v0.15.4` and would
refuse the seal for the same reason. `set -e` also stopped the job at this
step, so none of the later steps ran at CI: corrections, milestone, mode, the
CLAUDE.md block and the READMEs. I ran the correction check locally, and it
exits 0: *no merge commit in 7b55714..8f5ae44*.

**The fix.** All three are past states. The first two are a shipped work
item's design record, and the third is a note that a later **Corrected** note
on the same row supersedes. Nothing needs rewording, so each gets a
`survivors.md` row. I tried the rows below in the clone: the check then exits
0 and prints the three places as `exempt`.

This is round 1 and not the verifying round, so the rule that sends a
paperwork finding to a ⬜ does not apply. The red step also blocks the merge,
whatever file the fix lands in.

### 🔴 2 — C1 pins the skip line with `/`, and the gate prints the platform's separator

`tests/test_the_gate_names_every_step_ci_runs.py:885` spells the path inside
`SKIPPED_LINE` as `.github/workflows/hygiene.yml`, and `:961` asserts
`SKIPPED_LINE in result.stderr.splitlines()`. `broad_gate.py:1875` builds the
line from `WORKFLOW = os.path.join(".github", "workflows", "hygiene.yml")`,
and on Windows that path is `.github\workflows\hygiene.yml` (executed:
`ntpath.join` returns exactly that). The fixture's row is
`sys.executable -c pass`, and the module's other gate runs reach the checks on
`windows-latest`, so this case should reach the assertion there and fail.

**Read, not executed on Windows.** The `windows-latest` leg was still in
progress at `8f5ae44f` when this report was written. That leg is what
answers it. The module's older cases never pin the path. They look for
`answers every one of` (`:611`) or read `gate.WORKFLOW` (`:728`).

### 🟡 3 — A command name rooted in `%VAR%` is no longer rewritten

**Executed.** In a root holding `bin/`:

| Row | `7b557144` | `8f5ae44f` |
|---|---|---|
| `%CD%/bin/test -q` | `%CD%\bin\test -q` | `%CD%/bin/test -q` |
| `%VIRTUAL_ENV%/Scripts/python -m pytest` | `%VIRTUAL_ENV%\Scripts\python -m pytest` | as written |

`handed_to_shell` asks `os.path.isdir(os.path.join(root, "%CD%"))`, and that
literal directory never exists. `cmd.exe` expands `%CD%` before it reads the
name, so the name it reads is `C:\…/bin/test`. That is the shape #448's
premise says it reads as a switch. A row that ran under 0.15.3 stops
running, and neither the template nor the scan's docstring names it. The
two bounds they do name are about where the directory is judged (an earlier
command, a `cd`). This one is about what the part is spelled with.

**The fix.** Expand the part from the gate's environment before asking.
`ntpath` is already imported, and its `expandvars` reads `%VAR%` on every
platform, so a case can drive it from macOS. I ran the predicate below:
`%TREE%/bin/test` gives `%TREE%\bin\test`, `%NOPE%/bin/x` stays as written,
and `xcopy/e/i` stays as written. The template needs one sentence and its
case one needle (§14).

### ⬜ 4 — `gate`'s comment says everything below takes `base.commit`

`broad_gate.py:2175`: *Everything below asks `base.commit`, which is the
commit CI will compare against.* `skipped_at_main(base.given, workflow)` sits
below it and asks the caller's spelling, and it has to: the workflow's guard
compares a branch name. The comment should name that exception.

### ⬜ 5 — `seal/releases/0.12.2.md` R2's claim still says every consumer takes the commit

R2's claim is *Every consumer of the base inside one gate run takes the
resolved COMMIT*. This branch gave it a **Re-read** note, which says *every
check it runs still takes `base.commit`*. That is narrower than the claim,
and the claim itself was not touched. CLAUDE.md's rule for an edit that makes
a claim false asks for a correction in place. The finding is about the
run's paperwork: a correction, not a fix.

### ⬜ 6 — The skip is keyed on a spelling, not on the step's own guard

**Executed.** `refs/heads/main`, `refs/remotes/origin/main` and
`upstream/main` all return `[]`, so those spellings run two arms that CI
skips. The second condition asks whether the `release` job carries the
step's name, not whether that step carries the guard. Outside SpecSeal it
holds for no repository today: the shipped `templates/hygiene.yml` names its
job `hygiene`. Neither edge is live either. `agents/sealer.md` tells the
sealer to pass the plain branch name, and running an arm CI skips is the
direction that over-asks. The skip line itself says what CI says.

### ⬜ 7 — The comment rule tracks quotes per line and ignores `\"`

`tests/conftest.py#code_line` reads `run: echo "a \" # b"` as
`run: echo "a \"`, and it drops a `# …` line that sits inside a
double-quoted string spanning lines of a `run: |` block. Both mistakes drop
code. The docstring claims the rule only ever errs toward reading a comment
as code. No workflow line has either shape today (the spec's measurement).

### ⬜ 8 — `agents/sealer.md` does not tell the sealer to relay the skip line

The sealer quotes the stderr lines its definition names: the moved-base
line (`:71`) and the gate line. On a release pull request the skip line is
the only trace that two arms did not run, because the panel has no row for
either. Nothing tells the sealer to carry it into the report the
orchestrator reads. S3 says this line is *what a person sees*.

### ⬜ 9 — The directory part drops one `@`, and the built-in check drops all of them

**Executed.** `@@bin/test` asks about `@bin` and is handed over as written,
while `@@dir/b` is read as a built-in through `lstrip("@")`
(`broad_gate.py:1491`). One scan normalises one name two ways. Which of the
two `cmd.exe` does is not measured here.

## Regression tests to plant

- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`: a row rooted in an
  environment variable that names the tree, rewritten, and one naming nothing,
  as written (🟡 3's fence).
- `tests/test_the_gate_names_every_step_ci_runs.py`: nothing new. 🔴 2's fix
  makes the existing C1 case portable.

## Facts for the evidence ledger

- The `release` job's survivor step at `8f5ae44f` reports exactly three
  places, and with 🔴 1's rows it exits 0 (executed locally over
  `7b557144...HEAD`).
- `workflow_steps` and `job_steps` agree on the real workflow's 13 `release`
  steps (executed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | CI's `release` job is red at the target: the survivor step reports three removed sentences still standing, and no `survivors.md` row covers them | `seal/releases/0.15.3.md:60` | open | executed: CI run 36084469701 at `8f5ae44f` failed that step; `survivor_check.py --range 7b557144...HEAD` exit 1 with the same three; with the fenced rows it exits 0 |
| 🔴 2 | C1 pins the skip line with `/`, but the gate builds the path with `os.path.join`, so the exact-line assertion should fail on `windows-latest` | `tests/test_the_gate_names_every_step_ci_runs.py:885` | open | read, plus executed `ntpath.join` giving `.github\workflows\hygiene.yml`; the Windows leg was in progress at the target and answers it |
| 🟡 3 | A command name rooted in `%VAR%` (`%CD%/bin/test`) was rewritten in 0.15.3 and is now handed over as written; no bound names it | `skills/verify/scripts/broad_gate.py:1306` | open | executed against `7b557144` and `8f5ae44f` in a root holding `bin/`; the fenced predicate tried and gives `%TREE%\bin\test` |
| ⬜ 4 | `gate`'s comment says everything below takes `base.commit`, and the new guard takes `base.given` | `skills/verify/scripts/broad_gate.py:2175` | open | read |
| ⬜ 5 | R2's claim (*every consumer takes the resolved COMMIT*) got a Re-read note, not a correction, though the guard now consumes the given spelling | `seal/releases/0.12.2.md` | open | read; a correction to the run's paperwork |
| ⬜ 6 | The skip is keyed on a spelling (`refs/heads/main`, `upstream/main` run both arms) and on the step's name rather than its guard | `skills/verify/scripts/broad_gate.py:1841` | open | executed over eight spellings; no live instance: the sealer passes the plain name and the shipped template has no `release` job |
| ⬜ 7 | The comment rule tracks quotes per line and ignores `\"`, so it can drop code, which its docstring says it never does | `tests/conftest.py:48` | open | executed over six lines and a spanning string; no workflow line has either shape |
| ⬜ 8 | `agents/sealer.md` names the stderr lines to relay and not the skip line, the only trace that two arms did not run | `agents/sealer.md:71` | open | read |
| ⬜ 9 | The directory part drops one `@`, and the built-in check drops all of them | `skills/verify/scripts/broad_gate.py:1491` | open | executed: `@@bin/test` handed over as written |
| 🟢 | #596's predicate is asked where the row runs, `compare_at_base` included | `skills/verify/scripts/broad_gate.py:1220` | confirmed | read: `run` passes `root`, `compare_at_base` passes `scratch`; every caller of both changed functions enumerated by grep |
| 🟢 | The 0.15.3 A2 correction: claim amended, dead anchor dropped, dated Corrected note | `seal/releases/0.15.3.md:60` | confirmed | read; `evidence_check.py --strict` 2269 ok · 0 drifted · 0 broken (executed) |
| 🟢 | The 0.12.2 G4 correction: the note is true and the claim still holds | `seal/releases/0.12.2.md:39` | confirmed | read: the G4 case runs `run_gate` with the default `base="base"` |
| 🟢 | C3 is total and goes red when a guard moves | `tests/test_the_gate_names_every_step_ci_runs.py` | confirmed | executed: the regex matches the real guard, not a mutated one, and not an echo that falls through |
| ❓ | M1: whether `cmd.exe` runs `where/q cmd` as a program plus its switch | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` | ❓ out of verified scope | macOS here; the `windows-latest` leg at the pull request answers it, and the orchestrator reads that leg |

## Executed probes

| What was run | Result |
|---|---|
| `handed_to_shell` at `7b557144` and `8f5ae44f`, `windows=True`, a root holding `bin/` and `tools/`, over nine rows (`%CD%/…`, `%VIRTUAL_ENV%/…`, `"@bin/test"`, `@@bin/test`, `""/x`, `^@bin/x`, `bin/test`, `.venv/…`, `C:/tools/x`) | `%CD%` and `%VIRTUAL_ENV%` rewritten before and not after; `@@bin/test`, `"@bin/test"` and `^@bin/x` no longer rewritten; `""/x` and `bin/test` unchanged; `.venv/…` not rewritten where absent (the named bound) |
| `skipped_at_main` over the real workflow with eight spellings | `main` and `origin/main` skip both arms; `refs/heads/main`, `refs/remotes/origin/main`, `upstream/main`, `MAIN`, ` main` and `origin/main/` skip none |
| `code_line` over six lines, and `code_lines` over a quoted string spanning lines of a `run: \|` block | the `\"` line cut at the `#` inside the string; the spanning string's `#` line dropped; URL, apostrophe, `''` and tab lines as the docstring says |
| `workflow_steps` against `job_steps` on the real `hygiene.yml` | 13 and 13, same order |
| C3's regex over the real survivors step, the same step with its guard mutated, and a guard whose `exit 0` follows `fi` | match, no match, no match |
| `ntpath.join(".github", "workflows", "hygiene.yml")` | `.github\workflows\hygiene.yml` |
| `survivor_check.py --range 7b557144...HEAD` in the clone, without and with 🔴 1's rows | exit 1, three places; exit 0, three `exempt` |
| `correction_check.py --range 7b557144...HEAD` | exit 0, no merge commit in the range |
| `evidence_check.py --strict .` | exit 0, 2269 ok · 0 drifted · 0 broken |
| 🟡 3's predicate over five rows with `TREE` naming a directory holding `bin/` | `%TREE%\bin\test`; `%NOPE%/bin/x` as written; `xcopy/e/i` as written |
| `bin/test tests/test_a_workflow_is_read_the_one_way.py tests/test_the_gate_names_every_step_ci_runs.py -k …` (the new reader, #473 and #499 cases) | 30 passed on macOS |
| The probe module, run once through `bin/test` and then deleted | 3 passed (it printed, it asserted nothing) |
| The broad gate (full suite, lint, typecheck through `broad-gate`) | not yet — the sealer's, once the rounds settle; nothing here ran it |
| CI at `8f5ae44f` (read, not run here) | `release` failure at the survivor step; lint, ledger, ubuntu and macOS pytest success; `windows-latest` still in progress |

## Paste-ready fixes

### 🔴 1

```markdown
# 1790297086-the-broad-gate-says-what-ci-says — survivors

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md` | telling a program from a directory is #596 | The spec of the work item that shipped #448 in 0.15.3, recording what its round 2 decided and deferred to #596. It is a past state, and this work item is what closed #596; the design record keeps what was true when it was written |
| `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md` | A switch written with a blank before it (`xcopy /e`) is left as written, and the template says so | Same record, same grounds. The sentence is still true of the scan: a blank before a switch is never rewritten |
| `seal/releases/0.15.3.md` | and #596 holds the behaviour fix | Round 2's dated **Corrected** note on row A2, kept as the history of the claim. The **Corrected 2026-09-25 by work item 1790297086 (#596)** note after it on the same row says that it stopped being true and what replaced it |
```

Written to `seal/specs/1790297086-the-broad-gate-says-what-ci-says/survivors.md`.

### 🔴 2

```python
# tests/test_the_gate_names_every_step_ci_runs.py — the path as the gate
# builds it, so the pin holds on every leg of the matrix.
SKIPPED_LINE = (
    f"broad-gate: the base is `main`, and {gate.WORKFLOW} skips "
    "the steps the `survivors` and `corrections` arms mirror on a pull request "
    "into `main`, so this run does not run them either"
)
```

### 🟡 3

```python
# skills/verify/scripts/broad_gate.py, handed_to_shell — cmd.exe expands
# %VAR% before it reads the name, so the part is expanded the same way before
# it is asked. `ntpath` reads %VAR% on every platform, so a case drives it.
    here = os.curdir if root is None else root
    return command_names_backslashed(
        command,
        lambda part: os.path.isdir(os.path.join(here, ntpath.expandvars(part))),
    )
```

```python
# tests/test_the_gate_hands_cmd_a_path_it_can_run.py
def test_a_name_rooted_in_a_variable_is_judged_where_the_variable_points(
    tree, monkeypatch
):
    """#596. `cmd.exe` expands `%VAR%` before it reads a command name, so the
    part is expanded before it is asked whether it is a directory."""
    gate = gate_module()
    monkeypatch.setenv("SPECSEAL_PROBE_TREE", tree)
    monkeypatch.delenv("SPECSEAL_PROBE_NOWHERE", raising=False)
    for row, expected in (
        ("%SPECSEAL_PROBE_TREE%/bin/test -q", r"%SPECSEAL_PROBE_TREE%\bin\test -q"),
        ("%SPECSEAL_PROBE_NOWHERE%/bin/x", "%SPECSEAL_PROBE_NOWHERE%/bin/x"),
    ):
        got = gate.handed_to_shell(row, windows=True, comspec=CMD, root=tree)
        assert got == expected, got
        only_slashes_turned(row, got)
```

```text
templates/config.md §Broad gate, after "…names a directory that exists where
the row runs;" — add:

A `%VAR%` in that part is expanded from the gate's own environment first, as
`cmd.exe` expands it before it reads the name.

and the matching needle in test_the_template_says_which_positions_are_rewritten:

    "A `%VAR%` in that part is expanded from the gate's own environment first",
```

Needs a fix: yes — 🔴 1 (the survivor step is red at CI), 🔴 2 (C1's pinned
line on `windows-latest`), 🟡 3 (a `%VAR%`-rooted command name regressed)
Loses a record or crashes: no

## Proof block

Files opened this round, all at `8f5ae44f` unless marked:

- `seal/specs/1790297086-the-broad-gate-says-what-ci-says/`: `spec.md`, `questions.md`, `plan.md`, `overview.md`, `phases/phase-1.md` to `phase-4.md`, `changelog.md`
- `skills/verify/scripts/broad_gate.py`: `Base`, `resolve_base`, `run`, `handed_line`, `handed_to_shell`, `command_names_backslashed`, `compare_at_base`, `job_steps`, `PARTITION`, `SKIPPED_AT_MAIN`, `skipped_at_main`, `skipped_line`, `gate`, and the same file at `7b557144`
- `skills/verify/SKILL.md` §*What the count does not say* (diff), `templates/config.md` §*Broad gate* (diff), `templates/hygiene.yml` (head and step names)
- `tests/conftest.py` (the reader), `tests/test_a_workflow_is_read_the_one_way.py`, `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`, `tests/test_the_gate_names_every_step_ci_runs.py`, `tests/test_the_gate_asks_the_range_ci_will_ask.py` (`base_spellings`, `keyed_under_env`, the regexes, the one-read case), `tests/test_a_merge_cannot_silently_drop_a_correction.py`, `tests/test_a_body_naming_two_issues_claims_one.py`, `tests/test_ci_gives_the_checks_what_they_need.py`, `tests/test_the_changelog_is_gathered_at_release.py`, `tests/test_the_ledger_fragments_fold_at_release.py` (diffs)
- `.github/workflows/hygiene.yml` (guards and step names), `.github/workflows/test.yml` (matrix)
- `agents/sealer.md` (the base and the lines it relays)
- `seal/releases/0.15.3.md` rows A1 and A2, `seal/releases/0.12.2.md` rows G4 and R2, `seal/ledger/1790297086-the-broad-gate-says-what-ci-says.md` row S1
- `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md:160-172` and its `survivors.md`
- `skills/code-review/scripts/survivor_check.py` (the survivors-file rules)
- CI: PR 607's check rollup and the failing `hygiene` run's log at `8f5ae44f`
