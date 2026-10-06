"""The Windows leg runs in shards whose union is the whole suite (#841).

`pytest-split` divides the suite by each case's duration, read from the
committed `.test_durations`, and every shard runs the group its matrix entry
names. What decides whether the union is the suite is the matrix itself: a
group named twice runs twice and a group named by no entry runs nowhere, and
nothing on the runner says so -- each shard passes. So the matrix is read
here: every Windows entry is a shard, all of one count `K`, the groups are
exactly 1 to `K`, the other legs carry no split, and the pytest line hands
the split to pytest.

The durations file is read too. A file missing from the tree only unbalances
the shards (`pytest-split` then divides by count), but one that does not
parse stops every shard at collection.
"""

import json
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKFLOW = os.path.join(ROOT, ".github", "workflows", "test.yml")
DURATIONS = os.path.join(ROOT, ".test_durations")

SPLIT = re.compile(r'split: "--splits (\d+) --group (\d+)"')


def pytest_job():
    with open(WORKFLOW, encoding="utf-8") as handle:
        text = handle.read()
    return text[text.index("  pytest:") : text.index("  ledger:")]


def matrix_entries(job):
    """The `include:` entries, one flow mapping a line; comments are not."""
    return [ln.strip() for ln in job.splitlines() if ln.strip().startswith("- { os:")]


def test_every_group_of_the_windows_split_runs_exactly_once():
    entries = matrix_entries(pytest_job())
    windows = [e for e in entries if "windows-latest" in e]
    found = [SPLIT.search(e) for e in windows]
    assert windows and all(found), f"a Windows leg that is not a shard: {windows}"
    counts = {int(m.group(1)) for m in found}
    assert len(counts) == 1, f"the shards disagree on how many there are: {counts}"
    (k,) = counts
    groups = sorted(int(m.group(2)) for m in found)
    assert groups == list(range(1, k + 1)), (
        f"groups {groups} of {k}: a group named twice runs twice, and one named "
        "by no entry runs nowhere"
    )
    others = [e for e in entries if "windows-latest" not in e]
    assert others and not any("split:" in e for e in others), others


def test_the_pytest_line_hands_the_split_to_pytest():
    runs = [
        ln.strip()
        for ln in pytest_job().splitlines()
        if ln.strip().startswith("- run: pytest ")
    ]
    assert len(runs) == 1, runs
    assert runs[0].endswith("${{ matrix.split }}"), runs[0]


def test_the_durations_file_parses_and_names_cases():
    with open(DURATIONS, encoding="utf-8") as handle:
        durations = json.load(handle)
    assert durations, "the durations file is empty"
    bad = [
        node
        for node, seconds in durations.items()
        if not node.startswith("tests/")
        or "::" not in node
        or not isinstance(seconds, (int, float))
        or seconds < 0
    ]
    assert not bad, bad[:5]
