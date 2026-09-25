# Feature Specification: the broad gate says what CI says

<!-- seal/specs/1790297086-the-broad-gate-says-what-ci-says/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Six tickets with one subject. In each one, the broad gate or a case that reads
the workflow the gate mirrors says something different from what CI says:

- **#596.** On `cmd.exe` the gate rewrites a switch written straight after a
  program into a path, so `xcopy/e/i` stops running.
- **#473.** The gate runs two arms on a `main` base, and the workflow skips
  them there.
- **#499.** A case reads the word it forbids out of paths it did not produce.
- **#462, #463, #482.** Cases that read `.github/workflows/hygiene.yml` as text
  count a commented-out flag, count any `BASE:` line, raise `TypeError` on an
  empty value, or slice the file on a token a comment may contain.

This is a patch release (milestone 46, `release: 0.15.4`, item D). The work
fixes instruments and adds no gate. Every refusal it touches enforces a rule a
document already states, and the one arm this work removes from a run is an
arm CI also skips.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/the-broad-gate.md` §*What the gate runs, and how the list is kept true* ("Every step CI runs is either mirrored by a named arm or excluded with a written reason") and the same file's #475 paragraph ("CI runs the checkout's scripts, and the gate exists to say what CI will say") | #473's guard is owed. A mirrored arm that asks where its step does not ask is a second reading of one question. |
| `skills/verify/SKILL.md` §*What the count does not say* ("#473 is the work item about that class, opened with the one live instance") | This paragraph names the instance this work closes, so its sentence has to change with the code. |
| `templates/config.md` §*Broad gate* ("The value must run as the command it reads as"; the paragraph *Which shell runs the row, and what it is handed*) | #596's fix makes the criterion true for `xcopy/e`. The template owns the statement of which positions are rewritten, so it changes in the same commit (contract §14). |
| `broad_gate.py#workflow_text` docstring and `spec.md` A7 of `1789985781-the-gates-arm-list-is-maintained-by-hand` ("the plugin ships to repositories that have no such workflow, and for them nothing about the run changes") | #473's guard applies only where the gated repository carries the steps it mirrors. Without the workflow, every arm runs exactly as before. |
| `CLAUDE.md` *Repo rule — a change writes fragments, never the shared file*, and the paragraph after it on editing code a row cites | New claims go in `seal/ledger/1790297086-the-broad-gate-says-what-ci-says.md`. The 0.15.3 row A2 in `seal/releases/0.15.3.md` becomes false under #596. It gets corrected in place with a `Corrected <date>` note, and it loses only its dead anchor (`docs/the-evidence-ledger.md` §`settle` paragraph: "a row that keeps a live anchor beside the dead one loses only the dead one"). |
| `CLAUDE.md` *Repo rule — no real identifiers in examples or fixtures* | Fixture workflows and paths use neutral values. |
| `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it* (cited by #482) | That rule is why #482 was left to a ticket. Changing a case's reader is build work, and it belongs here in a phase, not in a fix pass. |

## Scope

### In

**S1 — #596: a `/` in a command name is rewritten only where the name starts in a directory.**
`skills/verify/scripts/broad_gate.py#command_names_backslashed` keeps its
position scan and makes one more decision at the first `/` of a command
name. That `/` is not a built-in's switch (`CMD_BUILTINS` is still asked
first, unchanged), so the scan looks at the part of the name before it. That
part is the name's characters from its start up to the `/`, with `"` and `^`
removed and one leading `@` dropped. The `/` and every later `/` in the same
name are rewritten to `\` **only where that part names a directory that
exists**. Otherwise every `/` in the name is handed over as written. An empty
part is a name that begins with `/`, and it counts as a directory: the
drive's root always exists, and this keeps today's output for that shape.

- **The scan stays pure.** It takes the directory question as an argument, a
  predicate `is_directory(part)`, and does no I/O itself. `handed_to_shell`
  gains a `root` argument and builds the predicate as
  `os.path.isdir(os.path.join(root, part))`. When `root` is None it uses the
  current directory, which is where `subprocess.run` with `cwd=None` would run
  the row. `run` passes its own `root`. That covers both shell callers:
  `gate`, and `compare_at_base`, whose `root` is its scratch worktree.
  `test_the_one_shell_site_is_run_and_it_applies_the_rewrite` still holds
  that there is one shell site.
- **Judged against the directory the row starts in.** Two bounds are named in
  the scan's docstring and in the template, not claimed away:
  - A directory made by an earlier command in the same row, or entered by a
    `cd` earlier in the row, is not seen. That name is handed over as written,
    which is what happened before #448, and it is no worse than the row
    itself.
  - A directory at the root named like a program (a `xcopy/` directory) makes
    `xcopy/e` read as a path. `cmd.exe` is itself ambiguous for that tree.
- **What a person reads changes, so it is documented and pinned in the same
  commit (contract §14).**
  - `handed_line` says "each command name's `/`", which becomes false for a
    row like `xcopy/e && bin/test`. It is reworded to say that only a name
    starting in a directory is rewritten, and the case that reads the line
    pins the new text.
  - `templates/config.md` §*Broad gate*: the sentences "A `/` written
    straight after any other program's name is read as part of a path and
    rewritten … Telling the two apart is #596" are replaced by the directory
    rule, the two bounds above, and the note that a blank before a switch
    (`xcopy /e`) still works.
  - `test_the_template_says_which_positions_are_rewritten` pins the new
    sentences, and its `#596` needle goes.
- **Cases.**
  - `test_a_switch_against_another_program_is_rewritten_the_documented_bound_not_the_goal`
    inverts, which its own docstring predicted. It gets a name that says the
    new behaviour: `xcopy/e/i`, `findstr/s`, `timeout/t` and `ipconfig/all`
    are handed over as written where no such directory exists.
  - The A2 table (`test_only_the_command_names_have_their_slash_turned`)
    keeps its rows and expected outputs. It is driven with a predicate or root
    in which every prefix it names (`bin`, `tools`, `x`, …) is a directory.
  - A new table drives the other side: the same shapes with the prefix
    absent, a quoted name, a `^`-opened name, `@`, `.` and `..`, an empty
    prefix, and a name after a separator.
  - The calls to `handed_to_shell` in that module that pass no root pass
    one explicitly: `test_only_cmd_exe_on_windows_is_handed_the_backslashed_row`,
    `test_an_unset_comspec_on_windows_is_cmd_exe`, and the platform probe in
    `test_the_row_runs_on_the_real_platform`, which passes its fixture
    repository. None of them may lean on pytest's working directory
    happening to hold `bin/`.
- **Executed on Windows where Windows exists.** A real-platform case beside
  `test_the_row_runs_on_the_real_platform` runs a row with a non-built-in
  program and a switch written against it through `run(..., shell=True)` on
  the `windows-latest` leg, and asserts exit 0. `where/q cmd` is the default.
  `where.exe` ships with Windows, `/q` prints nothing, and it exits 0 when
  `cmd` is found. The case is skipped where the shell is not `cmd.exe`.
  `questions.md` M1 records that this premise is the ticket's, not a run here.

**S2 — one reader for the workflow's text, in `tests/conftest.py`, for #482, #462 and #463.**
The suite already shares helpers through `from conftest import …`: 53
modules do (counted 2026-09-25), and `tests/` has no other helper module. The shared reader goes
there. It reads text and is driven over fixtures. It is a test helper, not a
gate, and nothing in it refuses anything. It holds:

- **The comment rule, one owner.** A line whose first non-blank character is
  `#` is not code. Neither is a trailing comment: from a `#` that follows a
  blank and stands outside `"…"` and `'…'` to the end of the line. YAML ends
  a plain scalar there, and inside a `run:` block the shell ignores the rest
  of the line there, so both layers agree that it does not run.
  - Measured 2026-09-25: no non-comment line in `.github/workflows/*.yml`
    carries a trailing comment today (`grep` over every workflow). The wider
    rule therefore changes no current reading.
  - `tests/test_ci_gives_the_checks_what_they_need.py#strip_comments` is the
    whole-line half of the same rule. It becomes a use of the shared one, so
    the suite has one comment rule and not two.
- **A step, found by its name or by what it runs.**
  - `workflow_step(text, name)` returns one step's block. The step is found by
    its `- name:` value, read the way `broad_gate.py#STEP_RE` and `#unquote`
    read it, and the block runs to the next `- name:` at the same list level
    or to the next job. Comment lines are removed from the block.
  - `step_running(text, script)` returns the one step whose code lines, with
    comments removed, name `script`. It asserts that there is exactly one. A
    comment naming the script can then never move the region.
- **The class this closes, enumerated by construction** (every slice of the
  workflow's text on a bare token, found with `grep` over the modules that
  read `hygiene.yml`, 2026-09-25):

  | Site | Slices on |
  |---|---|
  | `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_a9_the_leg_runs_the_check_and_is_allowed_to_fail` | `correction_check.py` |
  | `…#test_a9_the_leg_asks_the_range_the_pull_request_is_about` (#482's instance) | `correction_check.py` |
  | `…#test_a9_the_leg_skips_a_release_pull_request_and_says_why` | the `- name:` part holding `correction_check.py` |
  | `tests/test_a_body_naming_two_issues_claims_one.py#test_the_body_reaches_the_script_through_the_environment` | `issue_claims_check.py` |
  | `tests/test_the_changelog_is_gathered_at_release.py#test_the_check_only_runs_for_a_release` | the step's name, as a bare substring |
  | `tests/test_the_ledger_fragments_fold_at_release.py#test_the_check_only_runs_for_a_release` | the step's name, as a bare substring |

  All six move onto the shared reader, and each keeps what it asserts. The
  body-injection case keeps its second assertion
  (`workflow.split("run:")[-1]`) unchanged, because that one reads the whole
  file on purpose.
- **#462.** `tests/test_the_gate_asks_the_range_ci_will_ask.py#base_spellings`
  reads code lines only, through the shared comment rule. It counts a `BASE:`
  line only where it is a key of an `env:` mapping, meaning the nearest
  shallower code line above it is `env:`. A `BASE:` under `with:`, or inside a
  `run: |` block, is not a base.
- **#463.** `base_spellings` returns `""` for an empty quoted value, not
  `None` (`group(1) if group(1) is not None else group(2)`). The widened
  pattern stays, as #463 asks. The check the case makes on each spelling is
  lifted into a helper that takes the list. An empty spelling then fails that
  helper's assertion, naming the value, the way every other malformed
  spelling fails.
- **Driven, as #462 asks.** A fixture workflow carries a flag in a whole-line
  comment, a flag in a trailing comment, a second unrelated `BASE:` under
  `with:`, one inside a `run: |` block, and `--baseline ""`. The reader is
  asserted over it, and the helper is asserted to raise `AssertionError` on
  the empty value.

**S3 — #473: the gate skips the two arms where CI skips their steps.**
`gate` does not run the `survivors` and `corrections` arms when **both** of
these hold:

1. the base the caller gave names `main`: `base.given`, with one leading
   `origin/` removed, is `main`. That is the gate's reading of the workflow's
   `github.base_ref == "main"`, and it is keyed on what the caller said the
   pull request merges into, as `agents/sealer.md` tells the sealer to pass
   it; and
2. the gated repository's `hygiene.yml` carries that arm's step in its
   `release` job (`job_steps(workflow, RELEASE_JOB)` holds the step's name).

- **Why both conditions.** Condition 2 keeps A7. A repository with no such
  workflow is every other repository that installs the plugin, and many of
  them merge feature branches straight into `main`. For them, skipping at
  `main` would drop two arms from every run, which is the unsafe direction.
  In the repository that does carry the steps, CI skips them there, so the
  gate skipping them too changes no verdict CI would give.
- **Where it is declared.** The arms the guard covers are one constant beside
  `PARTITION`, which is where #473 says a reader looks. `main` is written
  once. `PARTITION`'s three-tuple shape does not change, because seven sites
  in `tests/test_the_gate_names_every_step_ci_runs.py` and two in
  `broad_gate.py` unpack it (counted 2026-09-25).
- **What a person sees.** One stderr line before the checks run names both
  arms, says the base is `main`, and says the workflow's steps skip there.
  The panel is unchanged, because it carries no row for either arm. The
  `workflow` row's count is unchanged too: a step both sides skip is a step
  the gate's run agrees with, not one it failed to answer. The line is pinned
  (§14).
- **The drift pin #473 asks for.** For each mirrored arm, the workflow's step
  body skips when `github.base_ref` is `"main"` exactly where the constant
  holds that arm, read through S2's `workflow_step`. Measured 2026-09-25:
  of the five mirrored steps, two carry the skip (`survivors`,
  `corrections`) and three carry none (`unverified`, `chain`, `mode`), and
  the release job has no job-level `if:`. The pin is total over the five, so
  a guard added to a third step, or dropped from one of the two, fails the
  suite.
- **`skills/verify/SKILL.md` §*What the count does not say*.** Its last
  sentence names this instance as live. It is rewritten to say that the
  instance is closed and how. The class stays named, because the pin covers a
  guard on the base and no other kind of condition.

**S4 — #499: the case asserts on what names the release job, not on the whole stream.**
`tests/test_the_gate_names_every_step_ci_runs.py#test_a_repository_with_no_hygiene_workflow_is_sealed_exactly_as_before`
stops stripping echoed paths out of stderr and then searching the rest for
the bare word `release`. It asserts instead that stderr carries none of the
things that name the release job: `` `release` `` in backticks, as
`coverage_line` spells the job, `gate.WORKFLOW`, and every step name in
`gate.PARTITION`.

- A path cannot carry any of those by accident. A gate that prints a
  coverage line for a repository with no workflow still goes red.
- **Read, not executed:** 1404b3a7 (#549, 2026-09-24) already added
  `sys.executable` and the gate's realpath to the strip list, after #499 was
  filed on 2026-09-22, so the ticket's own instance may already be green.
  The strip list is still a list of echoed paths kept by hand, and the next
  echoed path reopens it. `questions.md` M2 is the measurement.
- The red direction, shown before commit (contract §15): the gate made to
  print a coverage line whatever the workflow says fails the case.

### Out, and why

- **Other positions `cmd.exe` reads as a command** (`call bin/test`,
  `>out bin/test`, `cmd /c bin/x`). The template already names them as not
  rewritten. #596 is about a switch and not about positions.
- **`broad_gate.py#job_steps`'s trailing-comment gap**, named in its own
  docstring. It is shipped code with no current instance, and it fails loudly
  if one appears. S2's reader is the suite's, and shipped code does not import
  from `tests/`.
- **A structural case that forbids slicing the workflow on a bare token in
  any test module.** That would be a check over the suite's own source, a new
  gate in effect. The class is enumerated above by construction, and the
  handover says so.
- **`CHANGELOG.md` §0.15.3's sentence naming #596 as open.** A released
  section is history. This work's changelog fragment says what changed.
- **`seal/follow-up.md` row 80** (cases that search a script's folded
  source). It is the same family of text readers with a different subject and
  no ticket in this milestone.
- **Other kinds of workflow condition on a mirrored step**, such as a
  job-level `if:` or an event filter. None exists today (measured above), and
  S3's pin covers the base guard only. `skills/verify/SKILL.md` keeps the
  class named.
- **`docs/the-broad-gate.md`.** Ratified policy. Nothing in it becomes false:
  it states the partition rule and not the arms' conditions.

## User scenarios & acceptance *(mandatory)*

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| A1 | A switch after a program runs on `cmd.exe` | Given `windows=True`, `COMSPEC` naming `cmd.exe` and a root with no `xcopy` directory, when `handed_to_shell("xcopy/e/i a b && bin/test", …, root=…)` runs with `bin/` present, then it returns `xcopy/e/i a b && bin\test` | Parametrised case over `xcopy/e/i`, `findstr/s`, `timeout/t`, `ipconfig/all`; red against the code at the frame commit |
| A2 | A path still becomes a path | Given a root with `bin/` and `tools/`, when `bin/test`, `"tools/run tests"`, `@bin/test`, `./bin/test` and `(bin/a && bin/b)` are handed over, then each has its name's `/` written `\` as today | The existing A2 table, driven with those directories |
| A3 | Every character but `/`→`\` stays put | For every row in A1–A2, `len(handed) == len(row)` and each changed pair is `("/", "\\")` | A2's existing two assertions, applied to the new table too |
| A4 | The scan does no I/O | `command_names_backslashed` takes the directory question as an argument, and a case drives both answers with no filesystem | A case passing a predicate that records what it was asked: the part before the first `/`, with `"`, `^` and a leading `@` removed |
| A5 | The directory is the row's own working directory | `compare_at_base`'s run in its scratch worktree judges `bin` against that worktree | Read: `run` passes its `root`; the one-shell-site case still holds |
| A6 | Windows executes it | On `windows-latest`, a row with a non-built-in and a switch against it, run through `run(..., shell=True)`, exits 0 | Real-platform case, skipped off `cmd.exe`; M1 |
| A7 | The documents say the new rule | `templates/config.md` §*Broad gate* states the directory rule and both bounds; the scan's docstring and `handed_line` agree | The template case with the new needles, each shown red with its sentence cut |
| B1 | A commented flag is not a base | A fixture with `# --baseline origin/other` and `run: x --range foo  # --baseline bar` yields no `origin/other` and no `bar` | Reader case over the fixture |
| B2 | Only `env:`'s `BASE:` counts | A fixture with `BASE:` under `env:`, under `with:`, and inside `run: \|` yields exactly the `env:` one | Reader case |
| B3 | An empty base asserts | `--baseline ""` → `base_spellings` returns `[""]`, and the spelling check raises `AssertionError` naming it, not `TypeError` | Case with `pytest.raises(AssertionError)`; red against the code at the frame commit (`TypeError`) |
| B4 | A comment naming a script cannot move a region | A fixture with a comment naming `correction_check.py` above an unrelated step and the real step below → `step_running` returns the real step; the six enumerated sites use the reader | Reader case, shown red with comment stripping removed; the six cases green on the real workflow |
| B5 | One comment rule | `test_ci_gives_the_checks_what_they_need.py` uses the shared rule | Read, plus that module green |
| C1 | A release pull request is sealed as CI would judge it | Given a repository whose `hygiene.yml` carries both steps, and a branch where the correction arm would refuse, when the gate runs with `--base main`, then `corrections` and `survivors` do not run, the stderr line says why, and the gate prints its SEALED stamp | Fixture case; the same fixture with a non-`main` base is NOT SEALED (the red direction) |
| C2 | A repository with no workflow is unchanged | With no `hygiene.yml` and `--base main`, both arms run and the refusing fixture is NOT SEALED | Fixture case |
| C3 | The guard and the workflow cannot drift | For each mirrored arm, "its step skips at `main`" iff "the constant holds it" | Structural case through `workflow_step`, shown red by removing one arm from the constant |
| C4 | The verify skill says it | `skills/verify/SKILL.md` no longer calls the instance live | Read by review |
| D1 | A checkout under `release/` is not red | The no-workflow case asserts on the release job's names, not on a bare word | Case green; red when the gate prints a coverage line unconditionally; M2 run before and after |

## Data & interfaces

- `broad_gate.command_names_backslashed(command, is_directory)`: the second
  argument is new and required. It is a callable taking the name's part
  before its first `/`.
- `broad_gate.handed_to_shell(command, windows=None, comspec=None, root=None)`:
  `root` is new.
- `broad_gate.run(...)`: the signature is unchanged, and it passes `root` on.
- `broad_gate.gate`: one new stderr line where the guard fires. No new flag
  and no new exit code.
- A new module constant beside `PARTITION` holding the guarded arms. The
  name is the builder's choice.
- `tests/conftest.py`: the comment rule, `workflow_step`, `step_running`.
  The names are the builder's choice, and S2 states their behaviour.
- Ledger: rows anchored on `broad_gate.py#command_names_backslashed`,
  `#handed_to_shell`, `#handed_line`, `#run`, `#gate`, `#PARTITION`,
  `templates/config.md#"## Broad gate"` and the edited test units will drift.
  Each is re-read against this edit where it stands. `seal/releases/0.15.3.md`
  row A2 is corrected in place (its xcopy clause turns false), and its anchor
  on the renamed bound case is dropped as dead. New claims go to
  `seal/ledger/1790297086-the-broad-gate-says-what-ci-says.md`.
- Changelog: `seal/specs/1790297086-the-broad-gate-says-what-ci-says/changelog.md`.

## Open questions → questions.md

Two measurements (M1, M2) and no question for a person.
`questions.md` lists what the tickets left open and the tree decided.

Framed 2026-09-25 by framer, before the build.
