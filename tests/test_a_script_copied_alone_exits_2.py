"""A shipped script copied without its sibling exits 2, with a sentence (#590, #610).

Six shipped scripts load a sibling, in one of two shapes. Five import it by
file path: `fold_check.py`, `settle.py`, `round_record.py`, `chain_check.py`
and `payload_meter.py`. One, `seal.py`, puts `hooks/` on `sys.path` with
`sys.path.insert` and then runs a plain `import`, which a search for the
first shape does not find. In the first four 1 means a finding or a refusal
the command made about the tree, and in `payload_meter.py` it means an input
that could not be measured; 2 means the input or the tree was unusable and
nothing was read or written. A sibling that is not beside the command is the
second kind: nothing about the tree has been read yet.

Before #590 three of the four said 1 for it. `fold_check.py` and
`settle.py` raised `SystemExit(<sentence>)`, and a string argument exits 1;
`round_record.py` did not check at all, so `spec_from_file_location` handed
back a spec for the absent path and `exec_module` died with a
`FileNotFoundError` traceback. `chain_check.py` already said 2, because its
`main` catches the load, and it is here so the class stays one shape.

The invocation per script is the smallest one that reaches its loader
(`seal/specs/1790297085-settle-retires-a-directory-main-has-not-seen-closed/
questions.md` Q1): `round_record.py` loads at import, `settle.py` and
`fold_check.py` load `hooks/optin.py` before they read the root, and
`chain_check.py` loads its readers after argument parsing, so it needs its
one required flag.

The two #610 added (`seal/specs/1790381329-the-deferred-sentences-and-pins/
questions.md` Q4): `seal.py` loads at import, so any invocation argparse
accepts reaches it -- `mode --check`, and not an empty one, because
argparse's own usage error is also exit 2 and would pass for the wrong
reason. `payload_meter.py` loads `session_cost.py` only under `--calibrate`,
and `measure` calls the loader before it opens the transcript, so the
transcript named need not exist.
"""

import os
import subprocess
import sys

import pytest

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

# (script, arguments after the copy's path, a phrase naming what the missing
# file is for, a phrase that must NOT appear), for the six scripts in both
# loader shapes: by file path, and `sys.path.insert` + `import`. The last
# column is #590's second half for `settle.py`: its loader used to give every
# file the fold record's purpose, which is false of `hooks/optin.py`.
CASES = [
    (
        "skills/settle/scripts/fold_check.py",
        ["--root", "{root}"],
        "it is what finds the repository's seal/ root",
        "fold's markers",
    ),
    (
        "skills/settle/scripts/settle.py",
        ["--root", "{root}"],
        "it is what finds the repository's seal/ root",
        "fold record",
    ),
    (
        "skills/code-review/scripts/round_record.py",
        [],
        "it is the checker this command writes records for",
        None,
    ),
    (
        "skills/code-review/scripts/chain_check.py",
        ["--baseline", "HEAD", "--root", "{root}"],
        "the shared reader",
        None,
    ),
    (
        "skills/implement/scripts/seal.py",
        ["mode", "--check"],
        "it is what finds the repository's seal/ root",
        None,
    ),
    (
        "skills/verify/scripts/payload_meter.py",
        ["--root", "{root}", "--calibrate", "{root}/main.jsonl"],
        "it is what reads a transcript's spawns",
        None,
    ),
]


def names_path(path, text):
    """Whether `text` names `path`, as written or as an `OSError` spells it.

    `str(OSError)` quotes the filename with `repr`, which doubles every
    backslash, so on Windows the path a refusal quotes from one is not the
    path as written. `chain_check.py` quotes one; the three loaders #590
    fixed write the path themselves."""
    return path in text or repr(path)[1:-1] in text


def test_the_path_is_found_as_a_windows_oserror_spells_it():
    """CI's windows-latest leg on PR #605: `chain_check.py` quotes the
    `OSError`, whose filename is repr-escaped on Windows, so every backslash
    of the path arrives doubled and the plain path is not a substring. Shown
    here with a Windows-shaped path, since a POSIX path has no separator for
    the escape to double."""
    path = "C:\\Users\\x\\alone"
    oserror = FileNotFoundError(2, "No such file or directory", path + "\\..\\r.py")
    text = f"chain-check: the shared reader would not load ({oserror})"
    assert path not in text, "the fixture no longer has the Windows shape"
    assert names_path(path, text), text
    assert names_path(path, f"cannot read {path}\\..\\r.py, and it is ...")
    assert not names_path(path, "cannot read C:\\Users\\y\\alone"), (
        "matched another path"
    )


@pytest.mark.parametrize(
    "script, args, purpose, absent", CASES, ids=[c[0].rsplit("/", 1)[1] for c in CASES]
)
def test_a_script_copied_alone_exits_2_and_names_what_it_misses(
    tmp_path, script, args, purpose, absent
):
    name = script.rsplit("/", 1)[1]
    alone = tmp_path / "alone"
    alone.mkdir()
    copy = alone / name
    with open(os.path.join(ROOT, *script.split("/")), encoding="utf-8") as f:
        copy.write_text(f.read(), encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    done = subprocess.run(
        [sys.executable, str(copy), *(a.format(root=repo) for a in args)],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        cwd=str(repo),
    )
    assert done.returncode == 2, (done.returncode, done.stderr)
    assert "Traceback" not in done.stderr, done.stderr
    assert names_path(str(alone), done.stderr), (
        f"the refusal does not name the missing path: {done.stderr}"
    )
    assert purpose in done.stderr, (
        f"the refusal does not say what the missing file is for: {done.stderr}"
    )
    if absent:
        assert absent not in done.stderr, done.stderr
