"""The released-row cases hold where the locale's encoding is not UTF-8.

The `windows-latest` runner's default encoding is cp1252. A file written or
read without `encoding=` uses it, and a citing row's verb is `Re-read · `, so
the middle dot went out as the one byte 0xB7 and came back as U+FFFD: 26
cases failed there and nowhere else. The commit advisor, run on its own,
printed the same byte, and the case reading it as UTF-8 got nothing.

A Latin-1 locale encodes the middle dot the same way, so this reproduces the
runner on any machine that has one. Where the machine has none, Python falls
back to UTF-8 and nothing here could fail, so the case says so and skips
rather than passing for the wrong reason.
"""

import os
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULE = os.path.join("tests", "test_a_released_row_is_read_again_in_a_fragment.py")
LATIN_1 = "en_US.ISO8859-1"
# A fixture written with a middle dot and read back by the checker, the
# citation the writer builds, `--into` writing a fragment, and the commit
# advisor run on its own.
CASES = (
    "test_a_re_read_clears_a_drifted_released_row",
    "test_the_citation_written_for_a_row_names_that_row_alone",
    "test_into_writes_one_citing_row_per_drifted_row_and_no_released_byte",
    "test_the_commit_advisor_names_into_where_the_ledger_is_frozen",
)


def latin_1_env():
    env = dict(os.environ, LC_ALL=LATIN_1, LANG=LATIN_1, PYTHONUTF8="0")
    env.pop("PYTHONIOENCODING", None)
    return env


def test_the_ledger_cases_pass_where_the_default_encoding_is_latin_1():
    env = latin_1_env()
    probe = subprocess.run(
        [sys.executable, "-c", "import locale; print(locale.getencoding())"],
        env=env,
        capture_output=True,
        encoding="utf-8",
    )
    if "utf" in probe.stdout.lower() or probe.returncode != 0:
        pytest.skip(f"this machine gives no non-UTF-8 default under {LATIN_1}")
    out = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            MODULE,
            "-q",
            "-p",
            "no:xdist",
            "-p",
            "no:cacheprovider",
            "-k",
            " or ".join(CASES),
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    assert out.returncode == 0, out.stdout[-3000:] + out.stderr[-2000:]
    assert f"{len(CASES)} passed" in out.stdout, out.stdout[-2000:]
