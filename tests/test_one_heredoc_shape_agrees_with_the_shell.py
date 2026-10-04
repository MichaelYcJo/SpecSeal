"""Every string `hooks/one_heredoc.py` admits is cut where a real shell cuts it
(#739, #763; scenario S6 and Q3 of work item
`1791089603-one-heredoc-shape-the-reader-matches-exactly-is-data`).

The reader decides where a body ends with an exact line comparison and no
shell lexer. That is a claim about bash and zsh, and this module measures it
rather than trusting it: a generated corpus of in-shape commands, each a sink
that writes the body to a file, is run through each shell, directly and
through `eval` (the harness hands a command to the shell one of those two
ways). For every string the reader admits, the file the shell wrote must be
the reader's body byte for byte, and no marker a body line would create may
exist. A body line the shell took for the terminator would have run the next
line, `: > m<n>`, as a command.

The corpus is built over clause C's axes: near-terminator lines with a
trailing blank, a leading or trailing tab, a `#` tail, quotes, a doubled
delimiter, a carriage return and a backslash at the line's end; a body line
containing the delimiter; an empty body and a body of one empty line; and the
terminator at end of input with and without a newline. Every candidate is
built in shape, so the reader must admit exactly those without a banned byte,
and the case checks that first: a reader that stopped admitting would
otherwise pass here by comparing nothing.

The program arm, `python3 -`, is run too, for clauses E and F: the lines after
its terminator are the suffix the gate reads, so the shell must run those and
no line of the body. Its body holds the same near lines, each followed by a
line that creates a marker. Python refuses such a body as a syntax error
before running any of it, and the shell has already decided where the body
ended, so the markers that exist are the lines the shell ran as commands:
exactly the suffix's, in the directory its `cd` names. They are compared with
the markers the reader's reduced text names.

The strings are harmless: `cat`, `tee`, `python3` refusing a program it
cannot compile, a `cd` into a directory the case made, and `: >` to create a
marker. Nothing here commits. Each shell is found by
`conftest.shell_probe` and skipped by name where it is not one, and its
startup files are kept out by pointing `HOME` and `ZDOTDIR` at the case's own
directory.
"""

import os
import shutil
import subprocess

import pytest
from conftest import load_hook_module, shell_probe

reader = load_hook_module("one_heredoc.py", "one_heredoc_agrees")

DELIMITERS = ["EOF", "x_9"]

# (first line without the opener, the file the body lands in, relative to the
# directory the shell starts in)
HEADS = [
    ("cat > out", "out"),
    ("cat >> out", "out"),
    ("tee -a out", "out"),
    ("cd 'a b' && tee 'o u t'", os.path.join("a b", "o u t")),
]


def near_lines(d):
    """Lines a reader could mistake for the terminator, or the delimiter
    standing inside a longer line."""
    return [
        f"{d} ",
        f" {d}",
        f"\t{d}",
        f"{d}\t",
        f"{d}#x",
        f"{d} #x",
        f"'{d}'",
        f'"{d}"',
        f"{d}{d}",
        f"{d};",
        f"{d})",
        f"x{d}",
        f"{d}x",
        f"$({d})",
        f"`{d}`",
        f"<<{d}",
        f"{d}\r",
        f"{d}\\",
    ]


def bodies(d):
    """Each body as its lines. Every near line is followed by a line that
    creates a marker, so a shell that ended the body early runs it."""
    out = []
    for i, line in enumerate(near_lines(d)):
        out.append([line, f": > m{i}"])
    out.append([x for i, line in enumerate(near_lines(d)) for x in (line, f": > n{i}")])
    out += [
        [],
        [""],
        ["", "", ": > e0"],
        [f"cat > f <<'{d}'", ": > e1"],
        ["$(: > e2)", "`: > e3`", "${x:=y}", "a\\b", "!!", "é ü 漢"],
        ["   ", "\t", "#", f"# {d}"],
        [d.swapcase(), f"{d.swapcase()}x", ": > e4"],
        # Banned by clause A, so the reader admits none of these and nothing
        # compares them. They are here so that deleting a ban puts them in
        # front of the shells rather than nowhere.
        ["x\\"],
        ["x\\", ": > e5"],
        ["x\r", ": > e6"],
    ]
    return out


ENDS = ["", "\n", "\n\n"]


def corpus():
    """(command, file, body lines) for every combination."""
    rows = []
    for d in DELIMITERS:
        for head, target in HEADS:
            for lines in bodies(d):
                for end in ENDS:
                    text = "".join(line + "\n" for line in lines)
                    rows.append((f"{head} <<'{d}'\n{text}{d}{end}", target, lines))
    return rows


BANNED = ("\r", "\0", "\\\n")

MODES = {
    "directly": lambda cmd: ["-c", cmd],
    "through eval": lambda cmd: ["-c", 'eval "$1"', "sh", cmd],
}


def test_the_reader_admits_every_in_shape_string_without_a_banned_byte():
    """The corpus is what the shell half compares, so it must not shrink: every
    candidate is in shape, and only clause A's bytes keep one out."""
    rows = corpus()
    admitted = [c for c, _, _ in rows if reader.reduce(c) is not None]
    expected = [c for c, _, _ in rows if not any(b in c for b in BANNED)]
    assert admitted == expected
    assert len(admitted) > 500, len(admitted)


def run_one(shell, mode, command, target, home):
    work = home / "w"
    if work.exists():
        shutil.rmtree(work)
    (work / "a b").mkdir(parents=True)
    env = {
        k: v for k, v in os.environ.items() if k not in ("BASH_ENV", "ENV", "CDPATH")
    }
    env.update(HOME=str(home), ZDOTDIR=str(home))
    done = subprocess.run(
        [shell, *MODES[mode](command)],
        cwd=work,
        env=env,
        capture_output=True,
        timeout=30,
    )
    path = work / target
    wrote = path.read_bytes() if path.is_file() else None
    markers = sorted(
        os.path.relpath(os.path.join(root, name), work)
        for root, _, names in os.walk(work)
        for name in names
        if os.path.join(root, name) != str(path)
    )
    return done.returncode, wrote, markers


@pytest.mark.parametrize("mode", sorted(MODES))
@pytest.mark.parametrize("shell", ["bash", "zsh"])
def test_the_shell_cuts_every_admitted_body_where_the_reader_does(
    shell, mode, tmp_path
):
    why = shell_probe(shell)
    if why is not None:
        pytest.skip(f"{shell}: {why}")
    disagreements = []
    compared = 0
    for command, target, _lines in corpus():
        found = reader._match(command)
        if found is None:
            continue
        compared += 1
        code, wrote, markers = run_one(shell, mode, command, target, tmp_path)
        expected = found[1].encode("utf-8")
        if code != 0 or wrote != expected or markers:
            disagreements.append(
                f"{command!r}: exit {code}, wrote {wrote!r}, "
                f"reader {expected!r}, other files {markers}"
            )
    assert compared > 500, compared
    assert not disagreements, (
        f"{len(disagreements)} of {compared} admitted strings cut differently "
        f"by {shell} {mode}:\n" + "\n".join(disagreements[:20])
    )


# (first line without the opener, the directory the suffix runs in, relative
# to the directory the shell starts in)
PROGRAM_HEADS = [
    ("python3 -", "."),
    ("python3 - 'q a' x.md", "."),
    ("cd 'a b' && python3 -", "a b"),
]

SUFFIXES = [": > s", ": > s\n: > t\n"]


def program_corpus():
    """(command, directory the suffix runs in) for every admitted
    combination: one near line and its marker per body, and one body of all
    of them."""
    rows = []
    for d in DELIMITERS:
        near = near_lines(d)
        bodies_ = [[line, f": > m{i}"] for i, line in enumerate(near)]
        bodies_.append([x for i, line in enumerate(near) for x in (line, f": > n{i}")])
        for head, where in PROGRAM_HEADS:
            for lines in bodies_:
                for suffix in SUFFIXES:
                    text = "".join(line + "\n" for line in lines)
                    command = f"{head} <<'{d}'\n{text}{d}\n{suffix}"
                    if reader.reduce(command) is not None:
                        rows.append((command, where))
    return rows


def suffix_markers(reduced, where):
    """The marker files the reduced text's own lines create, read the way
    its suffix is written: one `: > NAME` per line, after the first."""
    names = []
    for line in reduced.split("\n")[1:]:
        if line.startswith(": > "):
            names.append(os.path.normpath(os.path.join(where, line[4:])))
    return sorted(names)


def test_the_program_corpus_is_admitted_and_its_suffix_kept():
    rows = program_corpus()
    assert len(rows) > 150, len(rows)
    for command, where in rows:
        reduced = reader.reduce(command)
        assert suffix_markers(reduced, where), command


@pytest.mark.parametrize("mode", sorted(MODES))
@pytest.mark.parametrize("shell", ["bash", "zsh"])
def test_the_shell_runs_a_programs_suffix_and_no_line_of_its_body(
    shell, mode, tmp_path
):
    """Clauses E and F, measured: after `python3 -`'s terminator the shell
    runs exactly the lines the reduced text keeps, and none of the body."""
    why = shell_probe(shell)
    if why is not None:
        pytest.skip(f"{shell}: {why}")
    if shutil.which("python3") is None:
        pytest.skip("python3 is not on PATH here, so the program arm cannot run")
    disagreements = []
    rows = program_corpus()
    for command, where in rows:
        expected = suffix_markers(reader.reduce(command), where)
        _code, _wrote, markers = run_one(shell, mode, command, "", tmp_path)
        if markers != expected:
            disagreements.append(f"{command!r}: ran {markers}, reader {expected}")
    assert not disagreements, (
        f"{len(disagreements)} of {len(rows)} program strings ran differently "
        f"in {shell} {mode}:\n" + "\n".join(disagreements[:20])
    )
