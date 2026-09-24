# 1790260567-the-broad-gate-hands-cmd-a-forward-slash — review round 2 report

Verifying round. Target SHA `9f493c56`; target diff `29678169..371206af`
(round 1's fixes), plus the merge of `release/v0.15.3` at `974c64a0` and the
ledger repair at `9f493c56`. Worked in a `git clone --no-local` at
`9f493c56`; nothing was written in the worktree except this file.

## What round 1's verdicts come to

- **Round 1's 🟡 1 (the keyring login) is closed.** `tests/conftest.py` now
  sets `GH_TOKEN` and `GH_ENTERPRISE_TOKEN` to `NOT_A_GH_TOKEN` and removes
  the other two, so `gh`'s first lookup succeeds before it can reach
  `hosts.yml` or the keyring. The claim that `ActiveToken` takes an env
  token before the keyring is the fix pass's reading of upstream `gh`; I
  did not re-read upstream, and this machine keeps no keyring login, so the
  keyring half stays `read`. What I executed: with the conftest block cut
  out of the clone, both cases in
  `tests/test_the_suite_runs_with_gh_logged_out.py` went red. The
  behavioural one read `exit 0, 40 characters, not printed`, which is this
  machine's real login. With the block in place, both passed. Q2 and the
  spec's A6 row now say what the code does (read).
- **Round 1's 🟡 2 (a built-in's switch) is closed for the built-ins, and
  not for the class.** The five new cases went red with `CMD_BUILTINS`
  emptied: `rd\s\q`, `@dir\b`, `CD\D`, `echo\`, and `rd\s\q` after `&&`
  (executed). That list is the fix. But the class the finding belongs to
  is *a switch written straight against a command name*, and the fix
  enumerated only `cmd.exe`'s own commands. That is 🟡 1 below.
- **Round 1's ⬜ 3 is closed.** The template states the rule and gives
  examples, and the test refuses the old count (read; the case passed).
- **Round 1's ⬜ 4 is closed.** `c88b007f` writes each of the two first
  readings' dates into a note on its row (read from the diff).
- **Round 1's ⬜ 5 is closed for `spec.md` and `plan.md`** (read at
  `spec.md:157`). It is not closed for the third place it named, the
  pull request body. That body has no A7 answer at all, and it is also
  stale about #510. That is ⬜ 3 below.
- **Round 1's two ❓ rows stay ❓.** Neither can be answered without
  `cmd.exe`. The pull request's `windows-latest` leg was still pending
  when this round looked.

## 🟡 1 — A switch written against any program other than a built-in is still turned into a path

`skills/verify/scripts/broad_gate.py:1298` (`CMD_BUILTINS`), applied at
`:1434`.

This repository's own premise, in the module comment above
`handed_to_shell`, is that `cmd.exe` reads a `/` in a command name as the
start of a switch. That is why `bin/test` runs a command called `bin`. The
premise does not stop at built-ins. `xcopy/e/i src dst`, `findstr/s`,
`timeout/t 5` and `ipconfig/all` all run today as the program with its
switch. The scan hands them over as `xcopy\e\i`, `findstr\s`,
`timeout\t` and `ipconfig\all` (executed through
`handed_to_shell(..., windows=True)`). `cmd.exe` then looks for a path
that does not exist, so a Broad gate row that runs today stops running.

This is the shape of round 1's 🟡 2 with one name moved, and it matters
for the same reason. `spec.md:157` still says `cmd.exe` "has no reading in
which a `/` inside a command name is part of the name" and names only the
built-ins as the exception. The template names the built-in switch as the
only switch left as written. So a person who writes `xcopy/e` into the
row has no warning in any document, and the only signal is the stderr
line after the fact. What I ran is the rewrite. What `cmd.exe` then does
with `xcopy\e\i` is read from the module's own premise. The Windows leg
answers it.

No list closes this, because the scan cannot tell a program name from a
directory name by its spelling. There are two ways to close it:

- **Name the gap (fenced below).** This makes the template, the docstring,
  the spec's failure direction and the changelog say it, and pins the
  current output with a test case. The workaround a reader needs is one
  blank: `xcopy /e` reads the same to `cmd.exe` and is not rewritten.
- **A behavioural alternative.** Only rewrite a name's `/`s where the text
  before its first `/` is a directory under the root the row runs in
  (`bin`, `.`, `..`). This would also make `CMD_BUILTINS` unnecessary. It
  would also need `root` threaded into `handed_to_shell`, and every A1
  case would need a directory to stand on. That costs more than this round
  should commission, so the fence below is the first option.

## ⬜ 2 — The merge took one character out of two notes, and the repair did not put it back

`seal/releases/0.12.0.md:109` and `seal/releases/0.5.0.md:107`. This is a
correction to the run's own records, so it is not counted in `Needs a fix`.

At `974c64a0`, each of these rows' merge notes was carried in with a cell
separator. `9f493c56` removed the stray `| `, but the `|` it had taken
came out of an escaped pipe in an earlier note on the same row. So the
0.12.0 note now reads "the paragraph names `\ ` only as a separator"
where our side read `\|`. The 0.5.0 note reads "one `\ Item \| Value \|`
header" where it read `\| Item`. Both sentences are now false about the
template. `correction-check` cannot see this because no marker was
dropped. `evidence-check` cannot see it because a note is not hashed.

Everything else about the merge holds (executed with a word-level
comparison of all 98 ledger rows that either side edited, against each
parent and the merge base):

- **The notes are a union.** Every word of every note from either side is
  in the merged row, apart from these two characters.
  `correction-check --range` over each parent's side of the merge reports
  nothing dropped.
- **Every row re-stamped at the merge carries a note.** Only one anchor
  hash is new to both parents: 0.5.0 S8's `templates/config.md` unit,
  which both sides edited. That row carries the merge's `Re-read
  2026-09-25 … re-stamped after the merge` note. Every other anchor takes
  the hash of the side that edited its unit.
- **One date cell is older than the row's own merge note.** In 0.15.1 P3,
  the `Checked` cell took the release side's `2026-09-24` while the merge
  note beside it records a 2026-09-25 re-read. No date is lost, because
  the note carries it. So this is an observation, not a row.
- **The anchors resolve.** `evidence-check` at `9f493c56` reports 2220 ok,
  0 drifted, 0 broken.

## ⬜ 3 — The pull request body says the opposite of #510's fix and carries no A7 answer

This is the body of PR #595, not a file in the tree.

- **It says `tests/conftest.py` "removes the GitHub token variables".**
  Removing them is exactly what round 1's 🟡 1 showed to be not enough,
  and the fix sets two of them instead.
- **It says the first word after a redirection is a command name.** The
  code, the template and the case `>out.txt bin/test` all say it is left
  as written.
- **It has no A7 answer.** `spec.md` A7 asks for the failure direction,
  the test seen red and the prompt budget per fix. None of them is in the
  body, and neither is the built-in exception round 1's ⬜ 5 asked for.

A squash merge makes this body the commit body on the release branch. The
orchestrator owns it before the pull request is marked ready.

## The new units, judged as code

- **`CMD_BUILTINS`** is correct for what it lists. The names are the ones
  `cmd.exe` builds in. A leading `@` is stripped, case is ignored, and
  `in_name = False` keeps `rd/s/q`'s second switch as written. A name
  opened by `"` or `^` leaves `start` stale, but the stale slice always
  spans a separator or begins with `"`/`^`, so it can never equal a
  built-in (read, and `^rd/s/q` and `"rd"/s/q` were executed: both are
  rewritten, and neither is a realistic row). A directory named like a
  built-in (`path/to/tool`) is now left as written, which is what
  `cmd.exe` did before this branch, so it is not worse. What the list
  does not cover is 🟡 1.
- **`NOT_A_GH_TOKEN`** breaks no test the other chains added. The only
  shipped code that reads a token variable is
  `.github/scripts/release_completeness_check.py` and its siblings. They
  reach it through `gh` and never branch on `os.environ` (read). The
  modules that reach `gh` — `tests/test_release_hygiene.py`,
  `tests/test_the_record_is_generated.py` (whose `pull_request_cell` path
  meets a scratch repository with no remote, so `gh` fails before any
  token is sent) and `tests/test_the_closer_carries_on_past_a_refusal.py`
  — all passed with it in place (executed). The cost it adds is that a
  stray `gh` call now makes one network round trip and gets a 401,
  instead of failing locally. That is what the comment says it chose.
- **`test_the_token_gh_would_send_is_not_a_login`** can go red. It did,
  with the block removed. It never prints the token. It stays green on a
  machine without `gh` by skipping, which its docstring states.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A `/` written straight after any program other than a built-in (`xcopy/e/i`, `findstr/s`, `timeout/t`) is still rewritten into a path, so a row that runs today stops running; `spec.md:157` and the template name the built-ins as the only switch left as written | `skills/verify/scripts/broad_gate.py:1298` | open | executed: `handed_to_shell` with `windows=True` gives `xcopy\e\i`, `findstr\s`, `timeout\t`, `ipconfig\all`; what `cmd.exe` does with them is read from the module's own premise, and the `windows-latest` leg answers it |
| ⬜ 2 | Correction: the merge at 974c64a0 took the `\|` out of one note in each of two rows, and 9f493c56 repaired the cells but not the character, so each note now says something false about the template | `seal/releases/0.12.0.md:109` | open | executed: word-level comparison of all 98 side-edited rows against both parents; also `seal/releases/0.5.0.md:107` |
| ⬜ 3 | Correction: PR #595's body says the conftest removes the token variables, says a name after a redirection is rewritten, and carries no A7 answer | PR #595 body | open | read via `gh pr view`; the orchestrator owns the body before ready |
| 🟢 | round 1's blocking finding 1 is closed — the suite's `gh` finds a placeholder before `hosts.yml` or the keyring | `tests/conftest.py:341` | confirmed | executed: both cases red with the block cut out, green with it in; the keyring half is read, since this machine keeps no keyring login |
| 🟢 | round 1's finding 2 is closed for `cmd.exe`'s own commands — the five cases pin a built-in's switch as written | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py:114` | confirmed | executed: all five went red with `CMD_BUILTINS` emptied; the rest of the class is 🟡 1 |
| 🟢 | round 1's finding 3 is closed — the template states the rule and names examples, and a case refuses the old count | `templates/config.md:201` | confirmed | read; the case passed |
| 🟢 | round 1's finding 4 is closed — both re-stamped rows carry their first reading's date in a note | `seal/releases/0.10.0.md:62` | confirmed | read from `c88b007f`'s diff; also `seal/releases/0.12.2.md:14` |
| 🟢 | round 1's finding 5 is closed in `spec.md` and `plan.md` | `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md:157` | confirmed | read; the pull request body's half is ⬜ 3 |
| 🟢 | The merge kept both sides' notes, every row re-stamped at the merge carries a note, and no correction marker was dropped | `seal/releases/0.5.0.md:107` | verified | executed: the row comparison, `correction-check` over each side, `evidence-check` 2220 ok; the two characters are ⬜ 2 |
| 🟢 | `NOT_A_GH_TOKEN` breaks no test the other chains added | `tests/conftest.py:335` | verified | executed: the three modules that reach `gh` passed; read: no shipped code branches on a token variable |
| ❓ | Whether `cmd.exe` ends a command name at `=`, `,` or `;` (carried from round 1) | `skills/verify/scripts/broad_gate.py:1434` | ❓ out of verified scope | no `cmd.exe` here; the `windows-latest` leg or a person on Windows answers it |
| ❓ | Whether `cmd.exe` resolves `bin\probe` to `bin\probe.cmd` (Q1, A4; carried from round 1) | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` | ❓ out of verified scope | the `windows-latest` leg answers it at the pull request; it was pending when this round looked |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`, `tests/test_the_suite_runs_with_gh_logged_out.py`, `tests/test_the_record_is_generated.py`, `tests/test_release_hygiene.py` and `tests/test_the_closer_carries_on_past_a_refusal.py`, in the clone at 9f493c56 | exit 0, 245 passed |
| The two cases in `tests/test_the_suite_runs_with_gh_logged_out.py` with the conftest's `gh` block cut out of the clone (`gh` 2.100.0, login in `hosts.yml`) | exit 1, 2 failed: the structural case listed all four variables; the behavioural case found a login (exit 0, 40 characters, not printed); the clone was restored |
| `handed_to_shell` with `CMD_BUILTINS` emptied, over the five new rows | each built-in's switch was rewritten, so each case would go red |
| `handed_to_shell` with `windows=True` over 16 rows: built-ins, external programs with a switch, `^`/`"`-opened names, a directory named like a built-in | built-ins left as written; `xcopy\e\i`, `findstr\s`, `timeout\t`, `ipconfig\all`, `^rd\s\q`, `"rd"\s\q` rewritten; `path/to/tool` left |
| `evidence-check` in the clone at 9f493c56 | exit 0; 2220 ok, 0 drifted, 0 broken |
| `correction-check --range e1f1d4ec..9f493c56` and `--range 8dcd0d90..9f493c56` | exit 0 and exit 0; no correction marker dropped |
| A word-level comparison of every ledger row either side edited (98), against the merge base, both parents and 9f493c56 | two characters lost (⬜ 2); every other note word kept; one hash new to both parents, with the merge note |
| The full suite, lint and typecheck (the broad gate) | not yet — nobody has run it on this branch, and it is the sealer's |

## Paste-ready fixes

### 🟡 1

```markdown
templates/config.md, §Broad gate — replace "switch (`rd/s/q build`). Any other" with:

switch (`rd/s/q build`). A `/` written straight after any other program's
name is rewritten, because the scan cannot tell a program from a directory:
`xcopy/e` is handed over as `xcopy\e`, which `cmd.exe` cannot find. Write a
blank before the switch (`xcopy /e`), which `cmd.exe` reads the same way and
the scan leaves as written. Any other
```

```markdown
seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md,
Failure directions, first bullet — replace from "The rewrite only ever turns"
to "a row that ran before (round 1's 🟡 2)." with:

  The rewrite only ever turns `/` into `\` inside a command word. Where the
  word before the `/` is a directory, as in `bin/test`, that is the only
  change. Where it is a program, the `/` was that program's switch:
  `cmd.exe`'s own commands (`rd/s/q`, `dir/b`) are left as written, and any
  other program (`xcopy/e`) is rewritten and **denied** — a row that ran
  before now fails to find `xcopy\e`. The template says so and names the
  blank that avoids it. **Corrected 2026-09-25** in round 1's fix pass for
  the built-ins (round 1's 🟡 2), and in round 2's for every other program
  (round 2's 🟡 1).
```

```python
# skills/verify/scripts/broad_gate.py, command_names_backslashed's docstring,
# appended after the "Not rewritten, and named rather than claimed" paragraph:

    **Rewritten, and named rather than claimed:** a switch written straight
    against a program that is not one of `CMD_BUILTINS` (`xcopy/e`). The
    scan cannot tell a program's name from a directory's by its spelling,
    so `xcopy/e` is handed over as `xcopy\\e` and does not run. This one is
    worse than the row as written, and `templates/config.md` §*Broad gate*
    says so and names the blank that avoids it (`xcopy /e`).
```

```python
# tests/test_the_gate_hands_cmd_a_path_it_can_run.py, added to the
# parametrisation of test_only_the_command_names_have_their_slash_turned,
# after the built-in cases:
        # Any other program's switch is rewritten: the gap the template
        # names, pinned so it stays the one it states.
        ("xcopy/e/i a b && bin/test", r"xcopy\e\i a b && bin\test"),
        ("xcopy /e /i a b && bin/test", r"xcopy /e /i a b && bin\test"),

# and to the needles of test_the_template_says_which_positions_are_rewritten:
        "A `/` written straight after any other program's name is rewritten",
        "Write a blank before the switch (`xcopy /e`)",
```

```markdown
seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/changelog.md,
first bullet — after "is that command's switch and is left as written." add:

  A switch written straight against any other program, as in `xcopy/e`, is
  rewritten and stops running; write a blank before it (`xcopy /e`).
```

## Regression tests to plant

- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`: the two `xcopy`
  rows and the two template needles above. Show them red first: delete the
  new template sentence and watch the needle case fail. The `xcopy/e/i`
  row pins today's output, so it goes red only if the gap closes
  unannounced.

## Facts for the evidence ledger

- `command_names_backslashed` rewrites a `/` written straight after any
  name not in `CMD_BUILTINS`, a program's switch included (executed at
  `9f493c56`: `xcopy/e/i` gives `xcopy\e\i`).
- `tests/conftest.py` sets `GH_TOKEN` and `GH_ENTERPRISE_TOKEN` to
  `NOT_A_GH_TOKEN` at import, and with that block cut out
  `test_the_token_gh_would_send_is_not_a_login` goes red on a machine
  logged in through `hosts.yml` (executed at `9f493c56`).

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

The broad gate is not due yet: 🟡 1 is open. Once it is answered, and
⬜ 2 and ⬜ 3 are corrected, what comes due is the sealer's spawn.

Needs a fix: yes — 🟡 1 (a switch written against a program other than a built-in is still rewritten into a path, and the documents name only the built-ins)
Loses a record or crashes: no

## Proof block

Files opened: `skills/verify/scripts/broad_gate.py` (1195–1445),
`tests/conftest.py` (via the diff and the clone), `tests/test_the_suite_runs_with_gh_logged_out.py`
and `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` (via the diff),
`templates/config.md` (195–212), `CONTRIBUTING.md` (via the diff),
`skills/code-review/scripts/round_record.py` (955–1015),
`tests/test_the_record_is_generated.py` (180–200),
`tests/test_a_release_cannot_ship_an_untrue_milestone.py` (485–560),
`.github/scripts/release_completeness_check.py` (40–80), the work item's
`rounds/round-1.md`, `spec.md` (150–168), `plan.md` (58–68, 128–142),
`questions.md` (Q2, Q3), `changelog.md`, `overview.md` and
`phases/*.md` (grep), `seal/releases/0.4.0.md`, `0.5.0.md`, `0.8.2.md`,
`0.9.3.md`, `0.10.0.md`, `0.12.0.md`, `0.12.2.md`, `0.13.1.md`,
`0.15.0.md` and `0.15.1.md` at the merge base, both parents and
`9f493c56`, and PR #595's body and checks.
