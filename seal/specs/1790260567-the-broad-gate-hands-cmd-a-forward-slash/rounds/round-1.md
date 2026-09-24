# 1790260567-the-broad-gate-hands-cmd-a-forward-slash — review round 1

| Field | Value |
|---|---|
| Target SHA | 7dab2a17612a51b6ea28ec0c1f7a31530f85ba64 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 595 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `29678169a0fc5bf5e57e6dedb9af23dc13ed9f93..371206af7e8355846f9394978f82d97dbff7a7c9`, 7 commits |
| Contract changes | none |
| New units | CMD_BUILTINS (depth 1); NOT_A_GH_TOKEN (depth 1); test_the_token_gh_would_send_is_not_a_login (depth 1) |
| Needs a fix | yes — 🟡 1 (the keyring login escapes the suite's scrub, and the case built to catch it cannot) and 🟡 2 (a built-in's switch is rewritten into a path) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of work item 1790260567 reviews the build at 7dab2a17 against spec.md and plan.md (frame 6e1690c5): the cmd.exe command-name rewrite and the no-summary line (#448), and the suite running with gh logged out (#510). The classes are every cmd.exe line shape where a command word could still carry a slash or an argument be rewritten, every place that runs the Broad gate row with shell=True, every test path that could still reach an authenticated gh, and every document stating how the gate runs the row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | On a machine whose `gh` login is in the OS keyring (the default), an empty `GH_CONFIG_DIR` does not hide it: `ActiveToken` falls back to the keyring's active-account slot. The behavioural case asks `gh auth status`, the one command that does not take that fallback, and Q2 was ticked on a `hosts.yml` probe | `tests/conftest.py:324` | **fixed** `554536af` | fixed at 554536af — 1ae6b42f, 371206af; read from the upstream `gh` source; executed here only for the `hosts.yml` half (`auth status` 1, `auth token` 1) |
| 🟡 2 | A `/` written against a `cmd.exe` built-in (`rd/s/q`, `dir/b`, `del/q`, `cd/d`) is that command's switch, and the scan hands it over as `\`, which breaks or changes a row that runs today | `skills/verify/scripts/broad_gate.py:1375` | **fixed** `660d8e09` | fixed at 660d8e09 — edfb96af; rewrite output executed on macOS with the platform passed in; what `cmd.exe` does with it is read, and the Windows leg is the answerer |
| ⬜ 3 | The template says two positions are not rewritten; `for … do`, `cmd /c` and `else` are also left as written | `templates/config.md:201` | **fixed** `660d8e09` | fixed at 660d8e09; read; the positive definition beside it is correct |
| ⬜ 4 | Two re-stamped rows lost their first `Checked` date, and no note carries it; no Notes cell lost anything | `seal/releases/0.10.0.md:62` | answered | a record correction, corrected at c88b007f; executed: a cell-by-cell comparison of all 13 rows; also `seal/releases/0.12.2.md:14` |
| ⬜ 5 | Correction: the failure-direction sentences are false for a built-in's switch until 🟡 2 is fixed | `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/spec.md:150` | answered | a record correction, corrected at 69158f60; read; also `plan.md:132`, and the PR body's A7 answer |
| 🟢 | The rewrite is applied at the one shell site, and both `shell=True` callers reach it | `skills/verify/scripts/broad_gate.py:1204` | confirmed | read, and the AST case passed |
| 🟢 | The kept file and stderr say what `cmd.exe` was handed; an argv check and a row with nothing to rewrite add nothing | `skills/verify/scripts/broad_gate.py:1236` | confirmed | executed: the A3 cases passed |
| 🟢 | A failing `suite` with no pytest summary gets the no-summary line, and one with a summary gets the count | `skills/verify/scripts/broad_gate.py:1922` | confirmed | executed: unit cases and the end-to-end gate case passed |
| 🟢 | Every edited ledger anchor resolves with no drift | `seal/releases/0.10.0.md` | confirmed | executed: `evidence-check` over the tree, 2078 ok, 0 drifted, 0 broken |
| ❓ | Whether `cmd.exe` ends a command name at `=`, `,` or `;`, which would make the scan rewrite an argument in `a=b/c` | `skills/verify/scripts/broad_gate.py:1375` | ❓ out of verified scope | no `cmd.exe` here; the CI `windows-latest` leg or a person on Windows answers it, and no realistic row has the shape |
| ❓ | Whether `cmd.exe` resolves `bin\probe` to `bin\probe.cmd` (Q1, A4) | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` | ❓ out of verified scope | executed only through `sh` here; the CI `windows-latest` leg answers it at the pull request |

## Paste-ready fixes

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
```markdown
CI's pytest job has no token, so `tests/conftest.py` makes the same true
locally when it is imported: it points `GH_CONFIG_DIR` at an empty directory,
removes `GITHUB_TOKEN` and `GITHUB_ENTERPRISE_TOKEN`, and sets `GH_TOKEN` and
`GH_ENTERPRISE_TOKEN` to a value no server accepts — because without a token
variable, `gh` reads the login it keeps in your OS keyring.
```
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
```markdown
Some positions are not rewritten, and `cmd.exe` reads them exactly as
before: a path after `call`, `start` or `if`, or after `for … do` and
`cmd /c`; a command name after a redirection that opens its command
(`>out.txt bin/test`); and a `/` written straight after one of `cmd.exe`'s
own commands, which is that command's switch (`rd/s/q build`).
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`, `tests/test_the_suite_runs_with_gh_logged_out.py` and the new end-to-end case in `tests/test_the_seal_is_taken_once_by_the_sealer.py`, in the clone | exit 0, 49 passed |
| `evidence-check` over the clone at 7dab2a17 | exit 0; 2078 ok, 0 drifted, 0 broken |
| `gh auth status` and `gh auth token` with `GH_CONFIG_DIR` empty and the token variables unset, on this machine (`gh` 2.100.0, login in `hosts.yml`) | exit 1 and exit 1; the scratch directory stayed empty |
| `handed_to_shell` with `windows=True` and a `cmd.exe` `COMSPEC` over eight rows with built-ins, `for … do`, `cmd /c` and `a=b/c` | built-in switches rewritten (`rd\s\q`, `del\q`, `dir\b`, `cd\d`, `echo\`); `for … do` and `cmd /c` left as written; `a=b\c` |
| A cell-by-cell comparison of the 13 changed rows in `seal/releases/` | Notes cells: insertions only. `Checked`: five multi-date cells reduced; two first dates carried by no note |
| The full suite, lint and typecheck (the broad gate) | not yet — nobody has run it on this branch, and it is the sealer's |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
