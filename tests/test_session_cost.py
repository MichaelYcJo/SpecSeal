"""session_cost: the numbers the seal's `cost` row asks for.

The report exists because nobody can produce these from inside a session. The
fixture below is a hand-built transcript with known answers, so a change to
the parser that quietly stops finding repeats or tool calls fails here.
"""

import datetime as dt
import json
import os
import subprocess
import sys

import pytest

SCRIPT = os.path.join(
    os.path.dirname(__file__), "..", "skills", "verify", "scripts", "session_cost.py"
)


def turn(second, block):
    """`second` is an offset; the clock does the carrying."""
    stamp = dt.datetime(2026, 8, 24, 10, 0, 0, tzinfo=dt.UTC) + dt.timedelta(
        seconds=second
    )
    return json.dumps(
        {
            "timestamp": stamp.isoformat().replace("+00:00", "Z"),
            "message": {"content": [block], "usage": {"input_tokens": 1000}},
        }
    )


def call(uid, start, end, command):
    return [
        turn(
            start,
            {
                "type": "tool_use",
                "id": uid,
                "name": "Bash",
                "input": {"command": command},
            },
        ),
        turn(end, {"type": "tool_result", "tool_use_id": uid}),
    ]


@pytest.fixture
def transcript(tmp_path):
    lines = []
    # 10s of tests, then the same scope again with a different pipe (8s), then
    # a 2s git call. Model gaps: 5s and 5s.
    lines += call("a", 0, 10, "pytest tests/unit -q | tail -5")
    lines += call("b", 15, 23, "pytest tests/unit -q | grep FAILED")
    lines += call("c", 28, 30, "git status --short")
    path = tmp_path / "t.jsonl"
    path.write_text("\n".join(lines) + "\n")
    return path


def run(args):
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )


def test_it_separates_command_time_from_model_time(transcript):
    data = json.loads(run(["--json", str(transcript)]).stdout)
    assert data["calls"] == 3
    assert data["command_s"] == 20  # 10 + 8 + 2
    assert data["model_s"] == 10  # two 5s gaps


def test_a_rerun_that_only_changes_the_pipe_counts_as_a_repeat(transcript):
    """The whole point: 8 seconds spent viewing a result already produced."""
    data = json.loads(run(["--json", str(transcript)]).stdout)
    assert data["repeat_same_work_s"] == 8
    assert data["repeat_exact_s"] == 0  # the commands differ after the pipe


def test_the_family_split_charges_a_compound_command_to_its_test(tmp_path):
    lines = call("a", 0, 60, "ruff check . && pytest tests -q")
    path = tmp_path / "c.jsonl"
    path.write_text("\n".join(lines) + "\n")
    data = json.loads(run(["--json", str(path)]).stdout)
    assert data["by_family"]["test"]["seconds"] == 60


def test_the_report_names_batching_when_every_turn_sent_one_call(transcript):
    out = run([str(transcript)]).stdout
    assert "batching" in out and "1.00 tools per turn" in out


def test_a_malformed_line_does_not_stop_the_read(tmp_path):
    path = tmp_path / "b.jsonl"
    path.write_text("not json\n" + "\n".join(call("a", 0, 5, "pytest -q")) + "\n")
    assert run(["--json", str(path)]).returncode == 0


def test_an_unparseable_timestamp_drops_its_row_not_the_report(tmp_path):
    bad = json.dumps(
        {
            "timestamp": "yesterday",
            "message": {
                "content": [
                    {
                        "type": "tool_use",
                        "id": "z",
                        "name": "Bash",
                        "input": {"command": "ls"},
                    }
                ]
            },
        }
    )
    worse = json.dumps(
        {
            "timestamp": "yesterday",
            "message": {"content": [{"type": "tool_result", "tool_use_id": "z"}]},
        }
    )
    path = tmp_path / "ts.jsonl"
    path.write_text("\n".join([bad, worse, *call("a", 0, 5, "pytest -q")]) + "\n")
    r = run(["--json", str(path)])
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["calls"] == 1


def test_a_transcript_with_no_tool_calls_says_so(tmp_path):
    path = tmp_path / "e.jsonl"
    path.write_text("{}\n")
    r = run([str(path)])
    assert r.returncode != 0 and "no tool calls" in r.stderr
