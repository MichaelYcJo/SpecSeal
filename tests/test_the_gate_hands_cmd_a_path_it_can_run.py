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


# Every directory a row in this module starts a command name in. A name is
# rewritten only where it starts in a directory that exists where the row
# runs (#596), so each case says where that is rather than leaning on
# whatever pytest's working directory happens to hold.
DIRECTORIES = ("bin", "tools", "x")


@pytest.fixture
def tree(tmp_path):
    root = tmp_path / "tree"
    for name in DIRECTORIES:
        (root / name).mkdir(parents=True)
    return str(root)


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
    tree, windows, comspec, expected
):
    """A1. Windows and a `COMSPEC` naming `cmd.exe` get `bin\\test`; POSIX,
    and a Windows `COMSPEC` naming any other shell, get the row as written.
    Keyed on the shell rather than `os.name`, because a POSIX shell in
    `COMSPEC` runs `bin/test` as written."""
    gate = gate_module()
    got = gate.handed_to_shell(ROW, windows=windows, comspec=comspec, root=tree)
    assert got == expected, f"windows={windows} comspec={comspec!r}: {got!r}"


def test_an_unset_comspec_on_windows_is_cmd_exe(tree, monkeypatch):
    """A1, the default. `subprocess` falls back to `cmd.exe` where `COMSPEC`
    is unset, so the rewrite must too — read from the environment when the
    argument is not given."""
    monkeypatch.delenv("COMSPEC", raising=False)
    gate = gate_module()
    assert gate.handed_to_shell(ROW, windows=True, root=tree) == HANDED


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
        # A `/` written against one of `cmd.exe`'s own commands is that
        # command's switch, which runs as written today.
        ("rd/s/q build && bin/test", r"rd/s/q build && bin\test"),
        ("@dir/b tests & bin/test", r"@dir/b tests & bin\test"),
        ("CD/D x && bin/test", r"CD/D x && bin\test"),
        ("echo/ && bin/test", r"echo/ && bin\test"),
        # The same after a separator: the built-in is the name that began there.
        ("bin/test && rd/s/q out", r"bin\test && rd/s/q out"),
        # A block that opens after `if`, `else` or `for … in` is not in
        # command position, which the template names as left as written.
        ("if exist x (bin/a) else (bin/b)", "if exist x (bin/a) else (bin/b)"),
        ("for %i in (x/y) do tools/x %i", "for %i in (x/y) do tools/x %i"),
        # Positions `templates/config.md` names as not rewritten, pinned so
        # the gap stays the one it states.
        ("call bin/test", "call bin/test"),
        (">out.txt bin/test", ">out.txt bin/test"),
        # The redirection's target is not a command name, blank or not.
        ("> out/log.txt bin/test", "> out/log.txt bin/test"),
    ],
)
def test_only_the_command_names_have_their_slash_turned(tree, row, expected):
    """A2. Arguments, quoted arguments, `%VAR%`, `^&`, `2>&1`, blocks and
    every operator reach `cmd.exe` as written; only `/` inside a command
    name changes. And the rewrite moves no character: the only difference
    anywhere is `/` → `\\`, position for position. Driven from a root in
    which every name here starts in a directory (`DIRECTORIES`), so each
    row is handed over exactly as it was before #596."""
    gate = gate_module()
    got = gate.handed_to_shell(row, windows=True, comspec=CMD, root=tree)
    assert got == expected, f"{row!r} was handed as {got!r}"
    only_slashes_turned(row, got)


def only_slashes_turned(row, got):
    """A3. Every character but `/` → `\\` stays where it was."""
    assert len(got) == len(row)
    moved = [(a, b) for a, b in zip(row, got, strict=True) if a != b]
    assert all(pair == ("/", "\\") for pair in moved), moved


@pytest.mark.parametrize(
    "row, expected",
    [
        # A program with a switch written against it: no directory carries
        # the program's name, so the name and its switch reach `cmd.exe`.
        ("nothere/x -q", "nothere/x -q"),
        ('"nothere/run tests" -q', '"nothere/run tests" -q'),
        ("^nothere/x", "^nothere/x"),
        ("@nothere/x", "@nothere/x"),
        # Every leading `@` is dropped, as the built-in check drops them
        # (round 1, ⬜ 9).
        ("@@bin/test", r"@@bin\test"),
        # The same shapes, starting in a directory that exists.
        ("^bin/x", r"^bin\x"),
        ('@"tools/run tests"', r'@"tools\run tests"'),
        ('"bin"/x', r'"bin"\x'),
        # `.` and `..` are directories wherever the row runs.
        ("./bin/test", r".\bin\test"),
        ("../x/y", r"..\x\y"),
        # An empty part is the drive's root, which always exists.
        ("/abs/x -q", r"\abs\x -q"),
        # One decision per name: every later `/` goes the way the first did.
        ("bin/nothere/x", r"bin\nothere\x"),
        ("nothere/bin/x", "nothere/bin/x"),
        # Each name after a separator is judged on its own.
        ("bin/test && nothere/x a/b", r"bin\test && nothere/x a/b"),
        ("nothere/x & bin/test", r"nothere/x & bin\test"),
        ("(nothere/a && bin/b)", r"(nothere/a && bin\b)"),
        # A quoted or escaped name after a separator starts where it stands,
        # not where the name before it did.
        ('nothere/x && "bin/run tests"', r'nothere/x && "bin\run tests"'),
        ("bin/test && ^nothere/x", r"bin\test && ^nothere/x"),
    ],
)
def test_a_name_that_starts_in_no_directory_is_handed_over_as_written(
    tree, row, expected
):
    """#596, the other side of A2's table. A command name whose part before
    its first `/` names no directory where the row runs is handed over as
    written, and one that does is rewritten, whatever opened it."""
    gate = gate_module()
    got = gate.handed_to_shell(row, windows=True, comspec=CMD, root=tree)
    assert got == expected, f"{row!r} was handed as {got!r}"
    only_slashes_turned(row, got)


def test_a_name_rooted_in_a_variable_is_judged_where_the_variable_points(
    tree, monkeypatch
):
    """#596, round 1's 🟡 3. `cmd.exe` expands `%VAR%` before it reads a
    command name, so the part is expanded before it is asked whether it is a
    directory. 0.15.3 rewrote `%CD%/bin/test`, and a literal `%CD%` directory
    never exists, so without the expansion that row stopped running."""
    gate = gate_module()
    monkeypatch.setenv("SPECSEAL_PROBE_TREE", tree)
    monkeypatch.delenv("SPECSEAL_PROBE_NOWHERE", raising=False)
    for row, expected in (
        ("%SPECSEAL_PROBE_TREE%/bin/test -q", r"%SPECSEAL_PROBE_TREE%\bin\test -q"),
        ("%SPECSEAL_PROBE_NOWHERE%/bin/x", "%SPECSEAL_PROBE_NOWHERE%/bin/x"),
        ("xcopy/e/i a b", "xcopy/e/i a b"),
    ):
        got = gate.handed_to_shell(row, windows=True, comspec=CMD, root=tree)
        assert got == expected, got
        only_slashes_turned(row, got)


@pytest.mark.parametrize(
    "row, asked",
    [
        ("bin/test -q", ["bin"]),
        ('"tools/run tests" -q', ["tools"]),
        ("^bin/x", ["bin"]),
        ("@bin/test", ["bin"]),
        ('@"a b"/c', ["a b"]),
        ("./bin/x", ["."]),
        # One question per name, at its first `/`.
        ("a/b/c && d/e", ["a", "d"]),
        # An empty part is answered without asking.
        ("/abs/x", []),
        # A built-in is asked about first, and is never a directory.
        ("rd/s/q x && y/z", ["y"]),
        # Only command names are asked about.
        ("echo a/b", []),
    ],
)
@pytest.mark.parametrize("answer", [True, False])
def test_the_scan_asks_about_a_name_and_reads_nothing_itself(row, asked, answer):
    """A4. The scan takes the directory question as an argument and does no
    I/O: a predicate here answers from no filesystem at all, and records
    what it was asked — the part before a name's first `/`, with `"`, `^`
    and a leading `@` removed. Both answers are driven, and the answer is
    what decides."""
    gate = gate_module()
    heard = []

    def is_directory(part):
        heard.append(part)
        return answer

    got = gate.command_names_backslashed(row, is_directory)
    assert heard == asked, heard
    only_slashes_turned(row, got)
    if asked:
        # Every asked name's `/` follows the answer.
        assert ("\\" in got) is answer, got


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


@pytest.mark.parametrize(
    "row, handed",
    [
        ("xcopy/e/i a b && bin/test", r"xcopy/e/i a b && bin\test"),
        ("findstr/s x *.py", "findstr/s x *.py"),
        ("timeout/t 5 && bin/test", r"timeout/t 5 && bin\test"),
        ("ipconfig/all", "ipconfig/all"),
        # The blank the template also names, which was never rewritten.
        ("xcopy /e /i a b && bin/test", r"xcopy /e /i a b && bin\test"),
    ],
)
def test_a_switch_against_another_program_reaches_cmd_exe_as_written(tree, row, handed):
    """A1, #596. A `/` written straight after a program that is not one of
    `CMD_BUILTINS` is that program's switch: no directory carries the
    program's name where the row runs, so `xcopy/e/i` reaches `cmd.exe` as
    written, and the `bin/test` after it is still rewritten. Before #596
    this case pinned the opposite, `xcopy\\e\\i`, as a documented bound."""
    gate = gate_module()
    got = gate.handed_to_shell(row, windows=True, comspec=CMD, root=tree)
    assert got == handed, got
    only_slashes_turned(row, got)


def test_the_template_says_which_positions_are_rewritten():
    """A2, the reader's half (§14). `templates/config.md` §*Broad gate* is
    where a person writing the row learns what `cmd.exe` is handed, and it
    states the rule and names the positions the scan leaves as written —
    the gap the cases above pin is only a gap nobody is surprised by while
    it is written down. It must not read as a complete count of them."""
    path = os.path.join(ROOT, "templates", "config.md")
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    section = text.split("## Broad gate", 1)[1].split("\n## ", 1)[0]
    prose = " ".join(section.split())
    for needle in (
        "the gate hands it the row with `/` written `\\` inside a command name "
        "that starts in a directory, and nowhere else",
        "It starts in a directory where the part before its first `/`, with its "
        "quotes and carets removed and every leading `@` dropped, names a "
        "directory that exists where the row runs",
        # Round 1's 🟡 3, where the person typing the row reads it.
        "A `%VAR%` in that part is expanded from the gate's own environment first",
        "`bin/test` then runs as `bin\\test`",
        "a path after `call`, `start` or `if`, or after `else`, `for … do` and "
        "`cmd /c`",
        "the definition above is the rule, and these are examples of it "
        "rather than the whole list",
        "a `/` written straight after one of `cmd.exe`'s own commands, which "
        "is that command's switch (`rd/s/q build`)",
        "a command name after a redirection that opens its command "
        "(`>out.txt bin/test`)",
        "the gate prints one line saying what `cmd.exe` was handed",
        # #596, written where the person typing the row reads it.
        "A `/` written straight after any other program's name reaches "
        "`cmd.exe` as written too",
        "`xcopy/e/i` stays `xcopy/e/i`",
        "A blank before the switch (`xcopy /e`) works as well",
        # And its two bounds, named rather than claimed away.
        "A directory an earlier command in the row makes, or one a `cd` "
        "earlier in the row enters, is not seen",
        "a directory at the root named like a program the row calls with a "
        "glued switch (an `xcopy/` directory) makes `xcopy/e` read as a path",
    ):
        assert needle in prose, f"templates/config.md §Broad gate lacks: {needle}"
    assert "Two positions are not rewritten" not in prose, (
        "the template still counts the positions it leaves as written"
    )
    assert "#596" not in prose, "the template still names #596 as open"


# --- A3: what ran is on record ------------------------------------------------


class _Ran:
    """A stand-in for `subprocess.run` that records what it was handed."""

    def __init__(self):
        self.handed = []

    def __call__(self, args, **kwargs):
        self.handed.append((args, kwargs.get("shell")))
        return subprocess.CompletedProcess(args, 0, "1 passed in 0.01s\n", "")


def test_a_rewritten_row_is_kept_and_said_beside_the_row_as_written(
    tree, tmp_path, monkeypatch, capsys
):
    """A3. The shell is handed `bin\\test`; the kept file's first line is the
    row as written and its second is what `cmd.exe` was handed; and one
    stderr line, pinned verbatim here (§14), says the same before the run.
    `run` asks about the directory where the row runs, its own `root`."""
    gate = gate_module()
    ran = _Ran()
    monkeypatch.setattr(gate.subprocess, "run", ran)
    check = gate.run(
        "suite",
        ROW,
        tree,
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
        "of a switch, so a command name that starts in a directory has its `/` "
        f"handed to it as `\\`: {HANDED}\n"
    )
    assert check.code == 0


def test_run_judges_the_directory_where_the_row_runs(tmp_path, monkeypatch):
    """A5. The same row, run from a root with no `bin/`, is handed over as
    written: `run` passes its own `root` on, and the directory is asked
    there and not in the caller's working directory."""
    gate = gate_module()
    ran = _Ran()
    monkeypatch.setattr(gate.subprocess, "run", ran)
    bare = tmp_path / "bare"
    bare.mkdir()
    gate.run(
        "suite", ROW, str(bare), str(tmp_path), shell=True, windows=True, comspec=CMD
    )
    assert ran.handed == [(ROW, True)], ran.handed


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
    under = "cmd" if runs_under_cmd_exe(gate, repo) else "sh"
    assert f"probe ran under {under}" in check.text, kept
    assert f"probe ran under {under}" in kept, kept


def runs_under_cmd_exe(gate, repo):
    """Whether this machine's shell is `cmd.exe`, read from what the gate
    would hand it. `repo` holds `bin/`, so the probe's answer does not rest
    on what pytest's working directory happens to hold (#596)."""
    return gate.handed_to_shell("bin/probe", root=str(repo)) != "bin/probe"


def test_a_switch_against_a_program_runs_on_the_real_platform(tmp_path):
    """A6, #596. `where/q cmd` — a program that ships with Windows and is not
    one of `CMD_BUILTINS`, with a switch written straight against it —
    run through `run(..., shell=True)` from a root with no `where`
    directory, exits 0: `/q` prints nothing and `where` finds `cmd`. Only
    CI's `windows-latest` leg executes it; elsewhere the shell is not
    `cmd.exe` and the row means nothing there (`questions.md` M1)."""
    gate = gate_module()
    repo = tmp_path / "repo"
    (repo / "bin").mkdir(parents=True)
    if not runs_under_cmd_exe(gate, repo):
        pytest.skip("the shell here is not cmd.exe")
    keep = tmp_path / "keep"
    keep.mkdir()
    row = "where/q cmd"
    assert gate.handed_to_shell(row, root=str(repo)) == row
    check = gate.run("suite", row, str(repo), str(keep), shell=True)
    kept = (keep / "suite.txt").read_text(encoding="utf-8")
    assert check.code == 0, kept


# --- A5: a failing row with no test result says so ----------------------------

# Pinned verbatim, because a person reads it on the failure form and decides
# from it whether to open the kept file (`agent-contract` §14).
NO_SUMMARY = (
    "no pytest summary in this output, so this exit code is not a count of "
    "failing tests: the row may have stopped before any test ran"
)


@pytest.mark.parametrize(
    "name, text, said",
    [
        # #448's case: the shell never reached the suite. The wording is
        # the machine's own language, which is why the line does not read it.
        (
            "suite",
            "'bin' is not recognized as an internal or external command,\n",
            True,
        ),
        ("suite", "", True),
        # A summary is a count, and the count is what the form shows instead.
        ("suite", "F\n1 failed in 0.01s\n", False),
        ("suite", "E\n1 error in 0.02s\n", False),
        # Any other check's output was never a pytest run.
        ("ledger", "BROKEN a#b@c\n", False),
    ],
)
def test_a_failing_suite_with_no_summary_says_it_is_not_a_count(name, text, said):
    """A5. The line is keyed on what is missing, pytest's summary with its
    wall clock, and not on an exit code: `cmd.exe` exits 1 for a command it
    cannot find, which is pytest's own 1."""
    gate = gate_module()
    lines = gate.failure_lines(gate.Check(name, 1, text, "/x/out.txt"))
    assert (NO_SUMMARY in lines) is said, lines
    assert lines[0] == "exit 1", lines
    assert lines[-1] == "full output: /x/out.txt", lines
    if name == "suite" and not said:
        assert gate.suite_counts(text) in lines, lines
