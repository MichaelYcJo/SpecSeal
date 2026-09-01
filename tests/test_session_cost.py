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


def message(second, blocks, message_id=None, uuid=None, tokens=1000):
    """One transcript row. `second` is an offset; the clock does the carrying.

    A row without `message_id` and `uuid` is its own turn — the shape of a
    transcript from a harness that stamps neither, and the degradation the
    parser must take toward the 1.00 floor rather than an inflated ratio."""
    stamp = dt.datetime(2026, 8, 24, 10, 0, 0, tzinfo=dt.UTC) + dt.timedelta(
        seconds=second
    )
    row = {
        "timestamp": stamp.isoformat().replace("+00:00", "Z"),
        "message": {"content": blocks, "usage": {"input_tokens": tokens}},
    }
    if message_id:
        row["message"]["id"] = message_id
    if uuid:
        row["uuid"] = uuid
    return json.dumps(row)


def turn(second, block):
    return message(second, [block])


def use(uid, command):
    return {
        "type": "tool_use",
        "id": uid,
        "name": "Bash",
        "input": {"command": command},
    }


def result(second, uid):
    return turn(second, {"type": "tool_result", "tool_use_id": uid})


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


def batch_data(tmp_path, lines, name="m.jsonl"):
    path = tmp_path / name
    path.write_text("\n".join(lines) + "\n")
    proc = run(["--json", str(path)])
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_two_calls_in_one_message_are_one_turn(tmp_path):
    """The meter read exactly 1.00 on five runs of two agent types because it
    could not read anything else: a turn was counted per tool_use BLOCK, so a
    message carrying two calls was two turns and len(calls)/len(turns) was
    pinned at ~1.00. A turn is the MESSAGE. This case reads 1.0 against that
    code and 2.0 against the fix."""
    data = batch_data(
        tmp_path,
        [
            message(0, [use("a", "ls src"), use("b", "ls tests")], message_id="m1"),
            result(10, "a"),
            result(18, "b"),
        ],
    )
    assert data["tools_per_turn"] == 2.0


def test_a_message_split_across_rows_is_one_turn_with_no_model_gap_inside(tmp_path):
    """A harness writes one assistant message as one row per content block,
    each row carrying the same message id. Two things must hold: the rows are
    one turn, and the wait between the first result and the second call's row
    is the batch executing, not the model thinking."""
    data = batch_data(
        tmp_path,
        [
            message(0, [use("a", "ls src")], message_id="m1"),
            result(10, "a"),
            message(12, [use("b", "ls tests")], message_id="m1"),
            result(18, "b"),
        ],
    )
    assert data["tools_per_turn"] == 2.0
    assert data["model_s"] == 0


def test_the_uuid_carries_the_turn_when_the_message_has_no_id(tmp_path):
    data = batch_data(
        tmp_path,
        [
            message(0, [use("a", "ls src")], uuid="u1"),
            result(5, "a"),
            message(6, [use("b", "ls tests")], uuid="u1"),
            result(9, "b"),
        ],
    )
    assert data["tools_per_turn"] == 2.0


def test_a_messages_tokens_count_once_however_many_calls_it_carries(tmp_path):
    """The two-call message below carried 1000 tokens into the context report
    twice, which skewed every third computed from the list."""
    data = batch_data(
        tmp_path,
        [
            message(
                0,
                [use("a", "ls src"), use("b", "ls tests")],
                message_id="m1",
                tokens=1000,
            ),
            result(1, "a"),
            result(2, "b"),
            message(10, [use("c", "ls docs")], message_id="m2", tokens=2000),
            result(11, "c"),
            message(20, [use("d", "ls hooks")], message_id="m3", tokens=3000),
            result(21, "d"),
            message(30, [use("e", "ls skills")], message_id="m4", tokens=4000),
            result(31, "e"),
        ],
    )
    assert data["context_growth"] == [1000, 2000, 3500]


def test_the_gap_after_a_batch_measures_from_its_last_result(tmp_path):
    """Two calls go out together; the slow one (x) started first and finished
    last. Model time to the next turn runs from the turn's LAST result (18s),
    not from whichever call sorts last by start (y, ending at 10s) — the
    per-call reading books 15s of thinking where 7s happened."""
    data = batch_data(
        tmp_path,
        [
            message(0, [use("x", "pytest tests/a -q")], message_id="m1"),
            message(5, [use("y", "git status --short")], message_id="m1"),
            result(10, "y"),
            result(18, "x"),
            message(25, [use("c", "git log -1")], message_id="m2"),
            result(30, "c"),
        ],
    )
    assert data["model_s"] == 7


def test_the_report_stops_claiming_one_at_a_time_above_a_ratio_of_one(tmp_path):
    """A run at 1.1 mostly sends single calls, but `independent calls are
    going out one at a time` is a claim the number no longer supports — and
    under per-block counting the ratio could never rise to contradict it."""
    lines = [
        message(0, [use("a0", "ls src"), use("a1", "ls tests")], message_id="m0"),
        result(1, "a0"),
        result(2, "a1"),
    ]
    for i in range(1, 6):
        lines += [
            message(i * 10, [use(f"b{i}", f"cat file{i}")], message_id=f"m{i}"),
            result(i * 10 + 1, f"b{i}"),
        ]
    path = tmp_path / "w.jsonl"
    path.write_text("\n".join(lines) + "\n")
    out = run([str(path)]).stdout
    assert "batching" in out
    assert "one at a time" not in out
    assert "most turns send a single call" in out


def test_a_transcript_with_no_tool_calls_says_so(tmp_path):
    path = tmp_path / "e.jsonl"
    path.write_text("{}\n")
    r = run([str(path)])
    assert r.returncode != 0 and "no tool calls" in r.stderr
