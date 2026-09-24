"""The broad gate hands `cmd.exe` a command name it can run (#448).

`broad_gate.run(..., shell=True)` hands the `Broad gate` row to `%COMSPEC%`,
and on Windows that is `cmd.exe`, which reads a `/` inside a command NAME as
the start of a switch. `bin/test -q && …` ran a command called `bin` with the
argument `/test`, the shell said "not recognized" and exited 1, and the
failure form reported the suite as failing. `bin/test.cmd` exists so that
`cmd.exe` can call the runner, and it is reached as `bin\\test`.

Every Windows half below is driven from any machine with the platform passed
in as an argument (`windows`, `comspec`), because a defence that rests on the
machine a case happens to run on is not verified (`agent-contract` §13). The
one claim no argument can stand in for — that `cmd.exe` really resolves
`bin\\probe` to `bin\\probe.cmd` — is `test_the_row_runs_on_the_real_platform`,
and only CI's `windows-latest` leg executes its `cmd.exe` path.
"""

import ast
import importlib.util
import os
import stat
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GATE = os.path.join(ROOT, "skills", "verify", "scripts", "broad_gate.py")

CMD = r"C:\Windows\System32\cmd.exe"
ROW = "bin/test -q && uvx ruff check . && uvx ruff format --check ."
HANDED = r"bin\test -q && uvx ruff check . && uvx ruff format --check ."


def gate_module():
    spec = importlib.util.spec_from_file_location("specseal_broad_gate_for_cmd", GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --- A1: which shell gets the rewrite ----------------------------------------


@pytest.mark.parametrize(
    "windows, comspec, expected",
    [
        (True, CMD, HANDED),
        (True, "CMD.EXE", HANDED),
        (True, f'"{CMD}"', HANDED),
        # Unset and empty are what Python itself answers with `cmd.exe`.
        (True, "", HANDED),
        (True, r"C:\Program Files\Git\bin\bash.exe", ROW),
        (True, r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe", ROW),
        (False, CMD, ROW),
        (False, None, ROW),
    ],
)
def test_only_cmd_exe_on_windows_is_handed_the_backslashed_row(
    windows, comspec, expected
):
    """A1. Windows and a `COMSPEC` naming `cmd.exe` get `bin\\test`; POSIX,
    and a Windows `COMSPEC` naming any other shell, get the row as written.
    Keyed on the shell rather than `os.name`, because a POSIX shell in
    `COMSPEC` runs `bin/test` as written."""
    gate = gate_module()
    got = gate.handed_to_shell(ROW, windows=windows, comspec=comspec)
    assert got == expected, f"windows={windows} comspec={comspec!r}: {got!r}"


def test_an_unset_comspec_on_windows_is_cmd_exe(monkeypatch):
    """A1, the default. `subprocess` falls back to `cmd.exe` where `COMSPEC`
    is unset, so the rewrite must too — read from the environment when the
    argument is not given."""
    monkeypatch.delenv("COMSPEC", raising=False)
    gate = gate_module()
    assert gate.handed_to_shell(ROW, windows=True) == HANDED


# --- A2: only command names change ------------------------------------------


@pytest.mark.parametrize(
    "row, expected",
    [
        (ROW, HANDED),
        # `compare_at_base`'s runner: the first command, then quoted paths.
        ('bin/test "tests/x.py"', r'bin\test "tests/x.py"'),
        ("bin/test tests/a/b.py --out=dir/x", r"bin\test tests/a/b.py --out=dir/x"),
        ('"tools/run tests" -q "a/b"', r'"tools\run tests" -q "a/b"'),
        ("bin/test %OUT%/x & tools/lint", r"bin\test %OUT%/x & tools\lint"),
        ("bin/test ^& not/a/command", r"bin\test ^& not/a/command"),
        # An escaped character opens the command name it stands in, so the
        # word after the next blank is an argument and keeps its `/`: a
        # one-character name that is escaped is still the name.
        ("^a b/c", "^a b/c"),
        ('bin/test "a & b/c" && x/y', r'bin\test "a & b/c" && x\y'),
        ("(bin/a && bin/b) || bin/c", r"(bin\a && bin\b) || bin\c"),
        (
            "bin/test 2>&1 | tools/tee out/log.txt",
            r"bin\test 2>&1 | tools\tee out/log.txt",
        ),
        ("bin/test>out/log.txt", r"bin\test>out/log.txt"),
        ("bin/test<in/x.txt", r"bin\test<in/x.txt"),
        ("bin/test\tx/y", "bin\\test\tx/y"),
        ("@bin/test -q", r"@bin\test -q"),
        ("  bin/test", r"  bin\test"),
        ("echo a/b", "echo a/b"),
        ("echo (a/b)", "echo (a/b)"),
        ("echo(a/b)", "echo(a/b)"),
        ("cmd /c bin/x", "cmd /c bin/x"),
        # The two positions named as not rewritten, pinned so the gap stays
        # the one `templates/config.md` states.
        ("call bin/test", "call bin/test"),
        (">out.txt bin/test", ">out.txt bin/test"),
        # The redirection's target is not a command name, blank or not.
        ("> out/log.txt bin/test", "> out/log.txt bin/test"),
    ],
)
def test_only_the_command_names_have_their_slash_turned(row, expected):
    """A2. Arguments, quoted arguments, `%VAR%`, `^&`, `2>&1`, blocks and
    every operator reach `cmd.exe` as written; only `/` inside a command
    name changes. And the rewrite moves no character: the only difference
    anywhere is `/` → `\\`, position for position."""
    gate = gate_module()
    got = gate.handed_to_shell(row, windows=True, comspec=CMD)
    assert got == expected, f"{row!r} was handed as {got!r}"
    assert len(got) == len(row)
    moved = [(a, b) for a, b in zip(row, got, strict=True) if a != b]
    assert all(pair == ("/", "\\") for pair in moved), moved


def test_the_one_shell_site_is_run_and_it_applies_the_rewrite():
    """A2, the class by construction. `broad_gate.py` has exactly one call
    passing `shell=`, it is inside `run`, and the string it is handed is the
    one `handed_to_shell` produced. `gate`'s `SUITE` and `compare_at_base`'s
    `suite-at-base` both reach a shell through it, so a third shell site
    written anywhere else turns this red rather than going unrewritten."""
    with open(GATE, encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    sites, callers = [], []
    for fn in ast.walk(tree):
        if not isinstance(fn, ast.FunctionDef):
            continue
        for node in ast.walk(fn):
            if not isinstance(node, ast.Call) or not any(
                kw.arg == "shell" for kw in node.keywords
            ):
                continue
            func = node.func
            if (
                isinstance(func, ast.Attribute)
                and isinstance(func.value, ast.Name)
                and func.value.id == "subprocess"
            ):
                sites.append((fn.name, node))
            elif isinstance(func, ast.Name) and func.id == "run":
                callers.append(fn.name)
    names = [name for name, _ in sites]
    assert names == ["run"], f"`subprocess` calls passing `shell=` are in: {names}"
    # The two callers the spec enumerates, and a third is a change to read.
    assert sorted(callers) == ["compare_at_base", "gate"], callers
    run_fn = next(
        fn for fn in tree.body if isinstance(fn, ast.FunctionDef) and fn.name == "run"
    )
    call = sites[0][1]
    assert call.args and isinstance(call.args[0], ast.Name), ast.dump(call)
    handed = call.args[0].id
    assigned_from_rewrite = [
        node
        for node in ast.walk(run_fn)
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == handed for t in node.targets)
        and any(
            isinstance(inner, ast.Call)
            and isinstance(inner.func, ast.Name)
            and inner.func.id == "handed_to_shell"
            for inner in ast.walk(node.value)
        )
    ]
    assert assigned_from_rewrite, (
        f"`run` hands the shell `{handed}`, and nothing in `run` assigns it "
        "from `handed_to_shell`"
    )


def test_the_template_says_which_positions_are_rewritten():
    """A2, the reader's half (§14). `templates/config.md` §*Broad gate* is
    where a person writing the row learns what `cmd.exe` is handed, and it
    names the two positions the scan leaves as written — the gap the cases
    above pin is only a gap nobody is surprised by while it is written down."""
    path = os.path.join(ROOT, "templates", "config.md")
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    section = text.split("## Broad gate", 1)[1].split("\n## ", 1)[0]
    prose = " ".join(section.split())
    for needle in (
        "the gate hands it the row with `/` written `\\` inside each command "
        "name, and nowhere else",
        "`bin/test` then runs as `bin\\test`",
        "a path after `call`, `start` or `if`",
        "a command name after a redirection that opens its command "
        "(`>out.txt bin/test`)",
        "the gate prints one line saying what `cmd.exe` was handed",
    ):
        assert needle in prose, f"templates/config.md §Broad gate lacks: {needle}"


# --- A3: what ran is on record ------------------------------------------------


class _Ran:
    """A stand-in for `subprocess.run` that records what it was handed."""

    def __init__(self):
        self.handed = []

    def __call__(self, args, **kwargs):
        self.handed.append((args, kwargs.get("shell")))
        return subprocess.CompletedProcess(args, 0, "1 passed in 0.01s\n", "")


def test_a_rewritten_row_is_kept_and_said_beside_the_row_as_written(
    tmp_path, monkeypatch, capsys
):
    """A3. The shell is handed `bin\\test`; the kept file's first line is the
    row as written and its second is what `cmd.exe` was handed; and one
    stderr line, pinned verbatim here (§14), says the same before the run."""
    gate = gate_module()
    ran = _Ran()
    monkeypatch.setattr(gate.subprocess, "run", ran)
    check = gate.run(
        "suite",
        ROW,
        str(tmp_path),
        str(tmp_path),
        shell=True,
        windows=True,
        comspec=CMD,
    )
    assert ran.handed == [(HANDED, True)], ran.handed
    kept = (tmp_path / "suite.txt").read_text(encoding="utf-8").splitlines()
    assert kept[:3] == [f"$ {ROW}", f"cmd.exe was handed: {HANDED}", "exit 0"], kept
    assert capsys.readouterr().err == (
        "broad-gate: suite — cmd.exe reads a `/` in a command name as the start "
        "of a switch, so each command name's `/` is handed to it as `\\`: "
        f"{HANDED}\n"
    )
    assert check.code == 0


@pytest.mark.parametrize(
    "windows, comspec, row",
    [
        (False, None, ROW),
        (True, r"C:\Program Files\Git\bin\bash.exe", ROW),
        # Nothing to rewrite, so nothing changed, so nothing extra is said.
        (True, CMD, "uvx ruff check ."),
    ],
)
def test_a_row_handed_as_written_adds_nothing_to_the_record(
    tmp_path, monkeypatch, capsys, windows, comspec, row
):
    """A3, the other half. Where nothing was rewritten, the kept file is the
    shape it always was and nothing is printed."""
    gate = gate_module()
    ran = _Ran()
    monkeypatch.setattr(gate.subprocess, "run", ran)
    gate.run(
        "suite",
        row,
        str(tmp_path),
        str(tmp_path),
        shell=True,
        windows=windows,
        comspec=comspec,
    )
    assert ran.handed == [(row, True)], ran.handed
    kept = (tmp_path / "suite.txt").read_text(encoding="utf-8").splitlines()
    assert kept[:2] == [f"$ {row}", "exit 0"], kept
    assert capsys.readouterr().err == ""


def test_an_argv_check_is_never_rewritten(tmp_path, monkeypatch, capsys):
    """A3. The plugin's own checks are argv lists with `shell=False`, which
    reach `CreateProcess` directly and take no shell's reading; the rewrite is
    for shell strings only, whatever the platform."""
    gate = gate_module()
    ran = _Ran()
    monkeypatch.setattr(gate.subprocess, "run", ran)
    argv = [sys.executable, "tools/check.py"]
    gate.run("ledger", argv, str(tmp_path), str(tmp_path), windows=True, comspec=CMD)
    assert ran.handed == [(argv, False)], ran.handed
    assert capsys.readouterr().err == ""


# --- A4: the real platform --------------------------------------------------


def test_the_row_runs_on_the_real_platform(tmp_path):
    """A4. A fixture with the pair `bin/probe` (sh) and `bin/probe.cmd`, and
    the row `bin/probe`, run through the real shell of whatever machine this
    is. On macOS and ubuntu `sh` runs the POSIX half; only on
    `windows-latest` does `cmd.exe` run `bin\\probe` and resolve it to
    `bin\\probe.cmd`. Its red on Windows without the fix is #448's own
    measurement, not a run of this case."""
    gate = gate_module()
    repo = tmp_path / "repo"
    (repo / "bin").mkdir(parents=True)
    probe = repo / "bin" / "probe"
    probe.write_text("#!/bin/sh\necho probe ran under sh\n", encoding="utf-8")
    probe.chmod(probe.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    (repo / "bin" / "probe.cmd").write_text(
        "@echo probe ran under cmd\r\n", encoding="utf-8"
    )
    keep = tmp_path / "keep"
    keep.mkdir()
    check = gate.run("suite", "bin/probe", str(repo), str(keep), shell=True)
    kept = (keep / "suite.txt").read_text(encoding="utf-8")
    assert check.code == 0, kept
    under = "cmd" if gate.handed_to_shell("bin/probe") != "bin/probe" else "sh"
    assert f"probe ran under {under}" in check.text, kept
    assert f"probe ran under {under}" in kept, kept
