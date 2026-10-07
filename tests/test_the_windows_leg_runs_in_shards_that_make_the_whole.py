"""The sharded legs run in shards whose union is the whole suite (#841, #864).

The Windows leg runs in four shards (#841) and the macOS leg in three
(#864); ubuntu runs as one job. The file keeps the name it was given when
Windows was the only sharded leg, because the sentence is still true and a
released ledger row anchors its three cases by this path.

`pytest-split` divides the suite by each case's duration, read from the
committed `.test_durations`, and every shard runs the group its matrix entry
names. One file divides both legs, because every leg collects the same
cases. What decides whether a leg's union is the suite is the matrix itself:
a group named twice runs twice and a group named by no entry runs nowhere,
and nothing on the runner says so -- each shard passes. So the matrix is
read here, through `tests/test_ci_gives_the_checks_what_they_need.py#
pytest_matrix`, the suite's one reading of it: every entry of a sharded
system is a shard of that system's count `K` in `SHARDED`, its groups are
exactly 1 to `K` once each, every other entry carries no split, and the
pytest line hands the split to pytest.

The durations file is read too. A file missing from the tree only unbalances
the shards (`pytest-split` then divides by count), but one that does not
parse stops every shard at collection.
"""

import json
import os
import re

from test_ci_gives_the_checks_what_they_need import jobs, pytest_matrix, read

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DURATIONS = os.path.join(ROOT, ".test_durations")

SPLIT = re.compile(r"--splits (\d+) --group (\d+)")

# Each sharded operating system and its count of shards. A system not named
# here runs the whole suite as one job and carries no split.
SHARDED = {"windows-latest": 4, "macos-latest": 3}


def test_every_group_of_each_sharded_leg_runs_exactly_once():
    entries = pytest_matrix(read("test.yml"))
    for system, k in SHARDED.items():
        legs = [e for e in entries if e.get("os") == system]
        found = [SPLIT.fullmatch(e.get("split", "")) for e in legs]
        assert legs and all(found), f"a {system} leg that is not a shard: {legs}"
        counts = {int(m.group(1)) for m in found}
        assert counts == {k}, (
            f"the {system} shards say {sorted(counts)} shards, and the leg has {k}"
        )
        groups = sorted(int(m.group(2)) for m in found)
        assert groups == list(range(1, k + 1)), (
            f"{system} groups {groups} of {k}: a group named twice runs twice, "
            "and one named by no entry runs nowhere"
        )
    others = [e for e in entries if e.get("os") not in SHARDED]
    assert others and not any("split" in e for e in others), others


def test_the_pytest_line_hands_the_split_to_pytest():
    runs = [
        ln.strip()
        for ln in jobs(read("test.yml"))["pytest"].splitlines()
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
