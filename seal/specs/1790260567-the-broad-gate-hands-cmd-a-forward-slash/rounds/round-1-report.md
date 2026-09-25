# Round 1 report — 1790260567-the-broad-gate-hands-cmd-a-forward-slash

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | 7dab2a17 |
| Base | c52e8350 (the fork point) |
| Reviewed by | specseal:warden, in a `git clone --no-local` at the target SHA |
| Contract | `spec.md` and `plan.md` (frame 6e1690c5); issues #448 and #510 |

This is a first round. No `rounds/round-*.md` existed, so nothing was carried
from an earlier round. The ledger coordinates this work touched were checked
by `evidence-check`, not carried.

## Summary

Two fixes need changes. Both are defects in what the work claims to close,
not in how it is written.

1. **#510 is closed only for a `gh` that keeps its login in `hosts.yml`.**
   `gh` stores its login in the OS keyring by default. On such a machine,
   emptying `GH_CONFIG_DIR` does not hide the token: `gh` falls back to the
   keyring's active-account slot for the host. The case meant to catch that
   is `gh auth status`, which is the one command that does not take that
   fallback, so it stays green while `gh api` stays logged in. Q2 asked this
   exact question, and it was ticked on a probe of a `hosts.yml` login.
2. **The #448 rewrite breaks a row that runs on `cmd.exe` today.** A `/`
   written straight after one of `cmd.exe`'s own commands is that command's
   switch (`rd/s/q build`, `dir/b`, `cd/d`). The scan reads it as a command
   name and hands `rd\s\q build` over. The spec's failure direction
   ("allows more") and the plan's "no row that works today changes
   behaviour" are false for this shape.

Two notes do not need a fix: the template's list of positions that are not
rewritten is shorter than the set of such positions, and two ledger rows lost
their first `Checked` date with no note carrying it.

The implementer's account, checked:

- *"It covers the line's first word and the first word after `&&`, `||`,
  `&`, `|`, `(`, and a redirection."* The code does the opposite for a
  redirection. `command_names_backslashed` ends command position at `<` or
  `>` (`skills/verify/scripts/broad_gate.py:1365`), and the template and the case `(">out.txt bin/test", …)`
  both say a name after a redirection is not rewritten. The code and the
  documents agree with each other; the hand-back is what is wrong. No
  finding.
- *"`^` escapes are left alone."* Confirmed by reading the `^` branch and by
  the cases `bin/test ^& not/a/command` and `^a b/c`, which passed.
- *"Both command lines go to the kept file, and one stderr line is added."*
  Confirmed: `run` writes `$ <row>` then `cmd.exe was handed: <line>`, and
  the A3 case pins both and the stderr line verbatim. It passed.
- *"`failure_lines` adds a no-summary line."* Confirmed. The only caller,
  `gate`, calls it for failed checks alone, so a passing `suite` never gets
  the line.
- *"The Q2 probe showed that `gh auth status` exits 1 under that state on
  this machine."* Re-measured and true on this machine. It does not answer
  Q2, which is finding 1.
- *"Check that nothing was lost from those rows' notes."* Nothing was lost
  from any Notes cell: a cell-by-cell comparison of all 13 re-read rows shows
  only insertions in Notes. Two first dates left the `Checked` cells and no
  note carries them (⬜ 4).

## Findings from reading and from execution

### 🟡 1 — On a machine whose `gh` login is in the keyring, the suite still reaches a logged-in `gh`, and the case built to notice cannot

`tests/conftest.py:324-334` empties `GH_CONFIG_DIR` and pops the four token
variables. The block's comment says `gh` finds its login in two places. It
finds it in three.

What `gh` does, **read** from the `cli/cli` repository's
`internal/config/config.go` on its default branch (not this machine's
binary):

- `ActiveToken(host)` reads the token variables and the config file first.
  When both are empty it asks `ActiveUser(host)`, which fails with no
  `hosts.yml`, and then falls back to `TokenFromKeyring(host)`. That is
  `keyring.Get("gh:" + host, "")`, the host's active-account slot.
- `activateUser` fills that empty-username slot at every login that uses
  the keyring, which is `gh auth login`'s default storage.
- `Hosts()` for `gh auth status` comes from `KnownHosts()`, the config file
  and the variables. It never reads the keyring.

So on a keyring machine with the block in place, `gh auth status` says
"not logged into any GitHub hosts" and exits 1, and `gh api …` still sends
the keyring token. That second path is the one #510 is about: the scripts
this suite drives call `gh api` and `gh pr`/`gh issue`, never
`gh auth status`.

Why it matters:

- `CONTRIBUTING.md` §*Running the checks* now tells contributors the suite
  runs logged out "on your machine as on CI". On the default `gh` setup
  that is false, and the #510 class (a case that passes locally and fails
  on CI) stays open there.
- `test_gh_reports_no_login_under_the_suites_environment` · NAME NOT IN TREE
  (`tests/test_the_suite_runs_with_gh_logged_out.py:69`) asks
  `gh auth status`. That is the one command that is blind to this path, so
  it stays green on exactly the machines where the scrub fails.
- `plan.md` names this risk ("a future `gh` could read its keyring token
  without looking at `GH_CONFIG_DIR`") and assigns the behavioural case to
  catch it. Today's `gh` already does this, and the case cannot catch it.
- `questions.md` Q2 asked "does a `gh` that is authenticated through the OS
  keyring report *not logged in*?" It is ticked ✅ on a probe of a login
  kept in `hosts.yml`, which the phase record states itself. The question's
  premise was never measured, and its fallback (setting `gh`'s host
  variable to a neutral host) was not written on the strength of that
  tick. The fallback would also not be enough: a command given
  `-R owner/repo` resolves its host from the repository, not from that
  variable.

**Executed** on this machine, where `gh` 2.100.0 keeps its login in
`hosts.yml`: under an empty `GH_CONFIG_DIR` with the token variables unset,
`gh auth status` exited 1 and `gh auth token` exited 1. So the block works
here. The keyring path cannot be executed on this machine without writing
to the user's keychain, which this round does not do. It is labelled
`read`, and the fix below adds a case that a keyring machine turns red.

The fix sets the two variables `gh` reads first to a value no server
accepts, so `ActiveToken` never reaches the keyring. It also asks
`gh auth token` instead of `gh auth status`. `gh auth token` takes the
same `ActiveToken` path as every API call and needs no network, and the
assertion never prints the token. What this changes:

- **Kept:** a stray `gh` fails on every machine.
- **Changed:** locally it fails with a 401 after one network round trip.
  On CI it fails with "gh auth login" before any network call. Both are
  failures, and the messages differ.
- **The alternative, if the smith prefers it:** put a `gh` stub that exits 4
  at the front of `PATH`. That removes the network trip. It also changes
  what `which("gh")` answers in the 28 modules that go through
  `round_record.py`, which is a wider change.

A structural case keeps red on any machine when the new lines are removed.
On this machine the behavioural case can be seen red only by pointing
`GH_TOKEN` at a value other than the placeholder. On a keyring machine it
goes red against today's block. The smith says in the handover which of
these it showed.

### 🟡 2 — The rewrite turns a built-in command's switch into a path, so `rd/s/q build` stops running as written

`command_names_backslashed` (`skills/verify/scripts/broad_gate.py:1375`)
rewrites every `/` inside a word in command position. For one of
`cmd.exe`'s own commands, a `/` written straight after the name is that
command's switch, and `cmd.exe` reads it that way today. Old DOS rows are
written like this: `dir/b`, `rd/s/q`, `del/q`, `cd/d`.

**Executed** here with `windows=True` and `comspec` set to a `cmd.exe`
path:

| Row | Handed to `cmd.exe` |
|---|---|
| `rd/s/q build && bin/test` | `rd\s\q build && bin\test` |
| `del/q build.log & bin/test -q` | `del\q build.log & bin\test -q` |
| `dir/b tests && bin/test` | `dir\b tests && bin\test` |
| `cd/d C:/w && bin/test` | `cd\d C:/w && bin\test` |
| `echo/ && bin/test` | `echo\ && bin\test` |

What `cmd.exe` then does is **read, not executed**, because this machine
has no `cmd.exe`. It has two possible readings, and the row breaks under
both. If a `\` does not end a built-in's name, `rd\s\q` is an unknown
command and the row fails "not recognized", the #448 symptom moved to the
first command. If it does end it, as `cd\` for `cd \` suggests, `rd` is
handed the path `\s\q build` instead of `/s /q`. That is a different act.
For `del\q build.log` it deletes a file at the drive root before
`build.log`.

Why it matters: the spec's failure direction says the rewrite "allows
more" and that "`cmd.exe` has no reading in which a `/` inside a command
name is part of the name". `plan.md` says "no row that works today changes
behaviour". For a built-in the `/` is not part of the name, but after the
rewrite the `\` is. So the rewrite can deny a row that runs today, or
change what it does, and nothing on the failure form says the gate did it.
The stderr line does say what was handed, but it gives the reason as
"cmd.exe reads a `/` in a command name as the start of a switch", which is
exactly the reading the rewrite just overrode.

The fix leaves a `/` as written when the name before it is one of
`cmd.exe`'s internal commands. The CI `windows-latest` leg is what can
execute the result. The fenced case below runs the transform on every leg,
so it can be seen red on macOS by deleting the new branch.

### ⬜ 3 — The template names two positions that are not rewritten, and there are more

`templates/config.md:201` says "Two positions are not rewritten": a path
after `call`, `start` or `if`, and a name after an opening redirection.
The scan also leaves as written `for … do tools/x`, `cmd /c tools/lint`
(pinned as unchanged in `test_only_the_command_names_have_their_slash_turned`
but not named in the template), and a name after `else`. Once 🟡 2 is
fixed, a built-in's switch joins the list. The positive definition just
above ("the word at the start of the line, or the first word after `&&`,
`||`, `&`, `|` or a `(` that opens a block") already excludes all of
them, so a reader who follows it is not misled. Only the "Two" sentence
reads as a complete list. Suggested wording is in the fence for 🟡 2,
which has to touch that sentence anyway.

### ⬜ 4 — Two ledger rows lost the date of their first reading

The 13 re-read rows were compared cell by cell. **No Notes cell lost
anything**; every change there is an insertion of the new `Re-read
2026-09-25` note. Five `Checked` cells held several dates and now hold
`2026-09-25`. Three of those five keep every removed date as a `Re-read`
marker in their notes. Two do not:

- `seal/releases/0.10.0.md` S1 (line 62) dropped `2026-09-10`. That is the
  row's original reading, which no note names.
- `seal/releases/0.12.2.md` R7 (line 14) dropped `2026-09-21`. Same shape.

`templates/ledger.md` defines the column as "the date somebody read the
code", so one date is a defensible reading. Git history keeps the old
value, and no tool reads it. It is recorded so the reduction is a decision
and not an accident.

### ⬜ 5 — Correction: the failure-direction sentences in the work item's paperwork

`spec.md:150-154` ("allows more … `cmd.exe` has no reading in which a `/`
inside a command name is part of the name") and `plan.md:132` ("no row
that works today changes behaviour") are false until 🟡 2 is fixed. After
the fix they hold only with "except a built-in's switch, which is left as
written" added. The PR body's failure-direction answer (A7) inherits the
same sentence.

## The classes, enumerated (§12)

- **Every `cmd.exe` line shape where a command word could still carry `/`,
  or an argument could be rewritten.** Still carrying `/`, as documented
  and left alone: after `call`/`start`/`if`, after an opening redirection.
  Still carrying `/`, not in the template's list: after `for … do`, after
  `cmd /c`, after `else` (⬜ 3). An argument or switch rewritten: a `/`
  written against a built-in (🟡 2). One more rewrite with an uncertain
  reading: `a=b/c` becomes `a=b\c`. `cmd.exe` may end a name at `=`, `,` or
  `;`, which would make `b/c` an argument. No realistic `Broad gate` row
  has that shape, and whether `cmd.exe` splits there is for the Windows leg
  to answer. It is recorded in `❓` below rather than as a finding. Quoted
  stretches, `^`-escapes, `%VAR%`, `2>&1`, `(…)` blocks and every operator
  were read against the scan and pass the parametrised cases.
- **Every place that runs the `Broad gate` row with `shell=True`.** A grep
  of `skills/`, `hooks/`, `.github/` and `bin/` finds one `subprocess.run`
  with `shell=`, in `run`. It has two callers, `gate` (line 2041) and
  `compare_at_base` (line 1488). The AST case holds that count.
  Confirmed.
- **Every test path that could still reach an authenticated `gh` or another
  credentialed call.** Token variables and `hosts.yml` are closed. The OS
  keyring is open (🟡 1). The phase record's grep for `env=` built from
  nothing is carried as its own `read` claim and was not re-derived beyond
  checking that no test reads `GH_TOKEN` from the environment as a
  precondition: `test_a_release_cannot_ship_an_untrue_milestone.py` names
  it only in workflow text. A `git` credential helper that runs through
  `gh` for an HTTPS remote is out of scope per `spec.md`, which reads no
  test as naming a network remote.
- **Every document that states how the gate runs the row.**
  `templates/config.md` §*Broad gate* (edited), `agents/sealer.md`'s
  failure-form bullet (edited, for the no-summary line), and the
  docstrings of `run`, `handed_to_shell`, `command_names_backslashed` and
  `quote`. `docs/the-broad-gate.md` and `skills/verify/SKILL.md` do not say
  which shell runs the row. The two `README` mentions of `cmd.exe` are
  about `hooks/hooks.json`, not the row. The changelog fragment repeats
  the template's "the two that are not".

## Regression tests to plant

- `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`: the built-in
  cases in the fence for 🟡 2, inside the existing parametrisation of
  `test_only_the_command_names_have_their_slash_turned`.
- `tests/test_the_suite_runs_with_gh_logged_out.py`: the `gh auth token`
  case in the fence for 🟡 1, replacing the `gh auth status` case, and the
  structural case's new expectation.

## Facts for the evidence ledger

- The A6 row in `seal/ledger/1790260567-the-broad-gate-hands-cmd-a-forward-slash.md`
  says the block makes "`gh auth status` under that environment report no
  login". That is true and is not the property #510 needs. After 🟡 1 the
  row should state that `gh`'s active token under the suite's environment is
  the placeholder, and cite the new case.
- For the A2 row, after 🟡 2: a `/` directly after a `cmd.exe` internal
  command is handed as written.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | On a machine whose `gh` login is in the OS keyring (the default), an empty `GH_CONFIG_DIR` does not hide it: `ActiveToken` falls back to the keyring's active-account slot. The behavioural case asks `gh auth status`, the one command that does not take that fallback, and Q2 was ticked on a `hosts.yml` probe | `tests/conftest.py:324` | open | read from the upstream `gh` source; executed here only for the `hosts.yml` half (`auth status` 1, `auth token` 1) |
| 🟡 2 | A `/` written against a `cmd.exe` built-in (`rd/s/q`, `dir/b`, `del/q`, `cd/d`) is that command's switch, and the scan hands it over as `\`, which breaks or changes a row that runs today | `skills/verify/scripts/broad_gate.py:1375` | open | rewrite output executed on macOS with the platform passed in; what `cmd.exe` does with it is read, and the Windows leg is the answerer |
| ⬜ 3 | The template says two positions are not rewritten; `for … do`, `cmd /c` and `else` are also left as written | `templates/config.md:201` | open | read; the positive definition beside it is correct |
| ⬜ 4 | Two re-stamped rows lost their first `Checked` date, and no note carries it; no Notes cell lost anything | `seal/releases/0.10.0.md:62` | open | executed: a cell-by-cell comparison of all 13 rows; also `seal/releases/0.12.2.md:14` |
| ⬜ 5 | Correction: the failure-direction sentences are false for a built-in's switch until 🟡 2 is fixed | `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md:150` | open | read; also `plan.md:132`, and the PR body's A7 answer |
| 🟢 | The rewrite is applied at the one shell site, and both `shell=True` callers reach it | `skills/verify/scripts/broad_gate.py:1204` | confirmed | read, and the AST case passed |
| 🟢 | The kept file and stderr say what `cmd.exe` was handed; an argv check and a row with nothing to rewrite add nothing | `skills/verify/scripts/broad_gate.py:1236` | confirmed | executed: the A3 cases passed |
| 🟢 | A failing `suite` with no pytest summary gets the no-summary line, and one with a summary gets the count | `skills/verify/scripts/broad_gate.py:1922` | confirmed | executed: unit cases and the end-to-end gate case passed |
| 🟢 | Every edited ledger anchor resolves with no drift | `seal/releases/0.10.0.md` | confirmed | executed: `evidence-check` over the tree, 2078 ok, 0 drifted, 0 broken |
| ❓ | Whether `cmd.exe` ends a command name at `=`, `,` or `;`, which would make the scan rewrite an argument in `a=b/c` | `skills/verify/scripts/broad_gate.py:1375` | ❓ out of verified scope | no `cmd.exe` here; the CI `windows-latest` leg or a person on Windows answers it, and no realistic row has the shape |
| ❓ | Whether `cmd.exe` resolves `bin\probe` to `bin\probe.cmd` (Q1, A4) | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` | ❓ out of verified scope | executed only through `sh` here; the CI `windows-latest` leg answers it at the pull request |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`, `tests/test_the_suite_runs_with_gh_logged_out.py` and the new end-to-end case in `tests/test_the_seal_is_taken_once_by_the_sealer.py`, in the clone | exit 0, 49 passed |
| `evidence-check` over the clone at 7dab2a17 | exit 0; 2078 ok, 0 drifted, 0 broken |
| `gh auth status` and `gh auth token` with `GH_CONFIG_DIR` empty and the token variables unset, on this machine (`gh` 2.100.0, login in `hosts.yml`) | exit 1 and exit 1; the scratch directory stayed empty |
| `handed_to_shell` with `windows=True` and a `cmd.exe` `COMSPEC` over eight rows with built-ins, `for … do`, `cmd /c` and `a=b/c` | built-in switches rewritten (`rd\s\q`, `del\q`, `dir\b`, `cd\d`, `echo\`); `for … do` and `cmd /c` left as written; `a=b\c` |
| A cell-by-cell comparison of the 13 changed rows in `seal/releases/` | Notes cells: insertions only. `Checked`: five multi-date cells reduced; two first dates carried by no note |
| The full suite, lint and typecheck (the broad gate) | not yet — nobody has run it on this branch, and it is the sealer's |

## Paste-ready fixes

### 🟡 1 — `tests/conftest.py`, the `gh` block

```python
# The suite runs with `gh` logged out, on every machine (#510). CI's pytest job
# has no token, so a case that falls through its stubs onto a live `gh` fails
# there -- and passed on every developer's machine and under the broad gate,
# because `gh` is logged in on both. Nothing local could see that class; CI
# found it after the branch was sealed.
#
# `gh` looks for its login in three places, in this order: a token variable,
# `hosts.yml` under its config directory, and the OS keyring. It reads the
# keyring even where no `hosts.yml` exists: `ActiveToken` falls back to the
# host's active-account slot, which `gh auth login` fills by default. Emptying
# the config directory hides only the second place. So the two variables `gh`
# reads first are SET, to a value no server accepts, and `gh` never reaches
# the keyring. A stray call then fails with a 401 here and with "gh auth
# login" on CI -- a failure in both places, which is the point.
# A case that needs `gh` stubs it.
GH_CREDENTIALS = (
    "GH_TOKEN",
    "GITHUB_TOKEN",
    "GH_ENTERPRISE_TOKEN",
    "GITHUB_ENTERPRISE_TOKEN",
)
# Not a credential: what `gh` finds in place of one.
NOT_A_GH_TOKEN = "specseal-suite-runs-with-gh-logged-out"
_EMPTY_GH_CONFIG = tempfile.mkdtemp(prefix="specseal-empty-gh-config-")
os.environ["GH_CONFIG_DIR"] = _EMPTY_GH_CONFIG
atexit.register(shutil.rmtree, _EMPTY_GH_CONFIG, True)
for _name in GH_CREDENTIALS:
    os.environ.pop(_name, None)
os.environ["GH_TOKEN"] = NOT_A_GH_TOKEN
os.environ["GH_ENTERPRISE_TOKEN"] = NOT_A_GH_TOKEN
```

```python
# tests/test_the_suite_runs_with_gh_logged_out.py

# Pinned verbatim: the conftest's placeholder, which is not a credential.
NOT_A_GH_TOKEN = "specseal-suite-runs-with-gh-logged-out"

PROBE = f"""
import json, os, runpy
runpy.run_path({CONFTEST!r})
home = os.environ.get("GH_CONFIG_DIR")
print(json.dumps({{
    "tokens": {{n: os.environ[n] for n in {TOKENS!r} if n in os.environ}},
    "home": home,
    "empty": bool(home) and os.path.isdir(home) and not os.listdir(home),
}}))
"""

# in test_the_conftest_takes_every_gh_login_away, replacing the tokens assert:
    assert seen["tokens"] == {
        "GH_TOKEN": NOT_A_GH_TOKEN,
        "GH_ENTERPRISE_TOKEN": NOT_A_GH_TOKEN,
    }, f"the suite's token variables: {sorted(seen['tokens'])}"


def test_the_token_gh_would_send_is_not_a_login():
    """A6, behavioural. `gh auth token` takes the same path as every API
    call -- the variables, then `hosts.yml`, then the keyring's active slot --
    and needs no network. `gh auth status` does not read the keyring without
    a `hosts.yml`, so it reported no login on a machine where `gh api` was
    still logged in. Red on a keyring machine against a block that only
    empties `GH_CONFIG_DIR`. The token is never printed."""
    gh = shutil.which("gh")
    if gh is None:
        pytest.skip("gh is not on PATH, so nothing here can reach one")
    r = subprocess.run(
        [gh, "auth", "token"],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        timeout=60,
        env={**os.environ, "GH_PROMPT_DISABLED": "1"},
    )
    token = r.stdout.strip()
    assert r.returncode != 0 or token == NOT_A_GH_TOKEN, (
        "`gh auth token` found a login under the suite's environment "
        f"(exit {r.returncode}, {len(token)} characters, not printed), so a "
        "case that reaches a live `gh` passes here and fails on CI"
    )
```

`CONTRIBUTING.md` §*Running the checks*, the paragraph's second sentence:

```markdown
CI's pytest job has no token, so `tests/conftest.py` makes the same true
locally when it is imported: it points `GH_CONFIG_DIR` at an empty directory,
removes `GITHUB_TOKEN` and `GITHUB_ENTERPRISE_TOKEN`, and sets `GH_TOKEN` and
`GH_ENTERPRISE_TOKEN` to a value no server accepts — because without a token
variable, `gh` reads the login it keeps in your OS keyring.
```

### 🟡 2 — `skills/verify/scripts/broad_gate.py`, `command_names_backslashed`

```python
# `cmd.exe`'s own commands. Written straight against one of them, a `/` is
# that command's switch -- `rd/s/q`, `dir/b`, `cd/d` -- and `cmd.exe` runs the
# row as written. Turned into `\` it stops being a switch, so it is left.
CMD_BUILTINS = frozenset(
    "assoc break call cd chdir cls color copy date del dir echo endlocal "
    "erase exit for ftype goto if md mkdir mklink move path pause popd "
    "prompt pushd rd rem ren rename rmdir set setlocal shift start time "
    "title type ver verify vol".split()
)


# inside command_names_backslashed: track where the name began
    out = []
    at_command = True  # the next word read is a command name
    in_name = False  # inside that command name now
    quoted = False
    start = 0  # where the current command name began
    i, n = 0, len(command)
    while i < n:
        c = command[i]
        if quoted:
            if c == '"':
                quoted = False
            elif c == "/" and in_name:
                c = "\\"
            out.append(c)
            i += 1
            continue
        if c == '"':
            quoted = True
            if at_command:
                at_command, in_name, start = False, True, i
            out.append(c)
            i += 1
            continue
        if c == "^":
            if at_command:
                at_command, in_name, start = False, True, i
            out.append(command[i : i + 2])
            i += 2
            continue
        if c in "&|":
            at_command, in_name = True, False
        elif c in "<>":
            at_command, in_name = False, False
        elif c in " \t(":
            in_name = False
        else:
            if at_command:
                at_command, in_name, start = False, True, i
            if c == "/" and in_name:
                if command[start:i].lstrip("@").lower() in CMD_BUILTINS:
                    # A built-in's switch, written against it: as written.
                    in_name = False
                else:
                    c = "\\"
        out.append(c)
        i += 1
    return "".join(out)
```

```python
# tests/test_the_gate_hands_cmd_a_path_it_can_run.py, added to the
# parametrisation of test_only_the_command_names_have_their_slash_turned:
        # A `/` written against one of `cmd.exe`'s own commands is that
        # command's switch, which runs as written today.
        ("rd/s/q build && bin/test", r"rd/s/q build && bin\test"),
        ("@dir/b tests & bin/test", r"@dir/b tests & bin\test"),
        ("CD/D x && bin/test", r"CD/D x && bin\test"),
        ("echo/ && bin/test", r"echo/ && bin\test"),
```

`templates/config.md` §*Broad gate*, replacing the "Two positions" sentence.
The needles `test_the_template_says_which_positions_are_rewritten` reads are
kept word for word:

```markdown
Some positions are not rewritten, and `cmd.exe` reads them exactly as
before: a path after `call`, `start` or `if`, or after `for … do` and
`cmd /c`; a command name after a redirection that opens its command
(`>out.txt bin/test`); and a `/` written straight after one of `cmd.exe`'s
own commands, which is that command's switch (`rd/s/q build`).
```

Needs a fix: yes — 🟡 1 (the keyring login escapes the suite's scrub, and the case built to catch it cannot) and 🟡 2 (a built-in's switch is rewritten into a path)
Loses a record or crashes: no

## Proof block

Files opened at 7dab2a17 in the clone:

- `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md`, `plan.md`, `questions.md`, `changelog.md`, `phases/phase-3.md`
- `skills/verify/scripts/broad_gate.py` (the diff; `run`, `handed_to_shell`, `command_names_backslashed`, `failure_lines`, `refused_broad_row` and the neighbouring fence readers, `gate`'s failure loop)
- `tests/conftest.py` (the diff), `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`, `tests/test_the_suite_runs_with_gh_logged_out.py`, the diff of `tests/test_the_seal_is_taken_once_by_the_sealer.py`
- `tests/test_a_release_cannot_ship_an_untrue_milestone.py` (lines 480–570), `tests/test_release_hygiene.py` (lines 1620–1650)
- `templates/config.md`, `CONTRIBUTING.md`, `agents/sealer.md` (the diffs), `templates/ledger.md` (lines 44–75)
- `skills/evidence-check/scripts/evidence_check.py` (`reverify`)
- The diffs of `seal/releases/0.10.0.md`, `0.12.0.md`, `0.12.2.md`, `0.15.1.md`, `0.5.0.md`, `0.8.2.md` and `seal/ledger/1790260567-the-broad-gate-hands-cmd-a-forward-slash.md`
- Outside the tree, read: the `cli/cli` repository's `internal/config/config.go` (`ActiveToken`, `TokenFromKeyring`, `activateUser`, `Hosts`)
