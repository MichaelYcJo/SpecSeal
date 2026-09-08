"""session_cost: the numbers the seal's `cost` row asks for.

The report exists because nobody can produce these from inside a session. The
fixture below is a hand-built transcript with known answers, so a change to
the parser that quietly stops finding repeats or tool calls fails here.
"""

import datetime as dt
import importlib.util
import json
import math
import os
import re
import subprocess
import sys

import pytest

SCRIPT = os.path.join(
    os.path.dirname(__file__), "..", "skills", "verify", "scripts", "session_cost.py"
)


# An integer literal with no float of its own. `json.loads` builds an
# arbitrary-precision `int` from any integer literal in a transcript, and
# `float(HUGE_INT)` raises `OverflowError` rather than returning an infinity.
HUGE_INT = int("9" * 401)

# A float near the top of the double range. Each one is finite and passes
# `count`; two of them add to an infinity, and two integers of this size each
# have a float where their sum does not.
TOP_FLOAT = 1.5e308


def stamp_at(second):
    """`second` is an offset from a fixed clock; the clock does the carrying."""
    stamp = dt.datetime(2026, 8, 24, 10, 0, 0, tzinfo=dt.UTC) + dt.timedelta(
        seconds=second
    )
    return stamp.isoformat().replace("+00:00", "Z")


def message(second, blocks, message_id=None, uuid=None, tokens=1000):
    """One transcript row.

    A row without `message_id` and `uuid` is its own turn — the shape of a
    transcript from a harness that stamps neither, and the degradation the
    parser must take toward the 1.00 floor rather than an inflated ratio."""
    row = {
        "timestamp": stamp_at(second),
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


def test_the_message_id_outranks_the_row_uuid_when_both_are_present(tmp_path):
    """Real rows carry both keys: a per-row uuid and, on a split message, a
    shared message id. Keyed uuid-first, the split message below is one turn
    per row — that mutant reads 1.0 here while every other case stays green,
    because no other fixture carries both keys at once."""
    data = batch_data(
        tmp_path,
        [
            message(0, [use("a", "ls src")], message_id="m1", uuid="u1"),
            result(5, "a"),
            message(6, [use("b", "ls tests")], message_id="m1", uuid="u2"),
            result(9, "b"),
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


# --- the token line ---------------------------------------------------------
#
# `message()` above writes `usage` with `input_tokens` alone, so every fixture
# built from it sums to zero output and zero cache. That is deliberate: the
# cases above cannot move when the token line lands. The helpers below write a
# full `usage` block, which is the shape a real assistant row carries.


def spend(
    second,
    output=0,
    cache_write=0,
    cache_read=0,
    message_id=None,
    uuid=None,
    blocks=None,
):
    """One assistant row carrying a full `usage` block.

    `blocks` defaults to a text block, so the row is a turn the token line
    counts and a turn `tools_per_turn` does not — the two counters this module
    holds apart."""
    row = {
        "timestamp": stamp_at(second),
        "message": {
            "content": blocks
            if blocks is not None
            else [{"type": "text", "text": "."}],
            "usage": {
                "input_tokens": 0,
                "output_tokens": output,
                "cache_creation_input_tokens": cache_write,
                "cache_read_input_tokens": cache_read,
            },
        },
    }
    if message_id:
        row["message"]["id"] = message_id
    if uuid:
        row["uuid"] = uuid
    return json.dumps(row)


def plain_result(second, uid):
    """A tool_result row as a harness writes one: no `usage` block, because it
    is not an assistant message. `result()` above carries one, which is a
    fixture artifact — the token line must not count such a row as a turn."""
    return json.dumps(
        {
            "timestamp": stamp_at(second),
            "message": {"content": [{"type": "tool_result", "tool_use_id": uid}]},
        }
    )


def write_run(tmp_path, main_lines, subagents=None):
    """A run on disk: `main.jsonl` with its segments under `main/subagents/`.

    That is the layout `newest` already walks — a run's subagent transcripts
    live in the directory named after the main transcript's own basename."""
    path = tmp_path / "main.jsonl"
    path.write_text("\n".join(main_lines) + "\n")
    for name, lines in (subagents or {}).items():
        target = tmp_path / "main" / "subagents" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(lines) + "\n")
    return path


def tokens_of(path):
    proc = run(["--json", str(path)])
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)["tokens"]


def worked(second, uid, command="pytest -q", **usage):
    """A call and its result: the one tool call every fixture here needs, so
    the report does not exit with `no tool calls`."""
    return [
        spend(second, message_id=f"call-{uid}", blocks=[use(uid, command)], **usage),
        plain_result(second + 1, uid),
    ]


def test_the_token_line_sums_the_run_not_just_the_transcript_it_was_given(tmp_path):
    """#161's run summed `usage` over its transcript AND its subagents with a
    script written for that one occasion. A number covering only the main
    transcript is not comparable with one that covered a whole run, so the sum
    is over both and no flag turns it off."""
    path = write_run(
        tmp_path,
        worked(0, "a", output=10, cache_write=100, cache_read=1000),
        {
            "one.jsonl": [
                spend(0, output=3, cache_write=30, cache_read=300, message_id="s1")
            ]
        },
    )
    assert tokens_of(path) == {
        "transcripts": 2,
        "turns": 2,
        "output": 13,
        "cache_write": 130,
        "cache_read": 1300,
    }


def test_each_column_is_its_own_usage_field(tmp_path):
    """Three rows, each spending in one field only. A read that puts
    `cache_read_input_tokens` where the cache-write column goes — the two
    names differ by one word in the transcript — passes any fixture whose
    fields move together."""
    path = write_run(
        tmp_path,
        [
            *worked(0, "a", output=7),
            spend(2, cache_write=50, message_id="m2"),
            spend(3, cache_read=900, message_id="m3"),
        ],
    )
    totals = tokens_of(path)
    assert (totals["output"], totals["cache_write"], totals["cache_read"]) == (
        7,
        50,
        900,
    )


def test_a_split_messages_usage_counts_once(tmp_path):
    """A harness writes one assistant message as one row per content block and
    repeats the usage on every row. `load` dedups against that trap for
    `context_growth`; the token line meets the same one, and a per-row sum
    would double a run's headline number."""
    path = write_run(
        tmp_path,
        [
            spend(
                0,
                output=10,
                cache_read=100,
                message_id="m1",
                blocks=[use("a", "pytest -q")],
            ),
            spend(
                1,
                output=10,
                cache_read=100,
                message_id="m1",
                blocks=[use("b", "ruff check .")],
            ),
            plain_result(5, "a"),
            plain_result(6, "b"),
        ],
    )
    totals = tokens_of(path)
    assert (totals["turns"], totals["output"], totals["cache_read"]) == (1, 10, 100)


def test_a_segment_measured_alone_reports_one_transcript(tmp_path):
    """A subagent's own transcript has no `subagents/` directory beside it.
    That is the ordinary case rather than a failure, and the count says so."""
    path = write_run(tmp_path, worked(0, "a", output=5))
    assert tokens_of(path)["transcripts"] == 1


def test_a_segment_of_a_segment_is_still_part_of_the_run(tmp_path):
    """The subagents directory is walked rather than listed, so a harness that
    nests one segment's transcripts under another still has its spend counted
    in the run's total."""
    path = write_run(
        tmp_path,
        worked(0, "a", output=1),
        {"inner/deep.jsonl": [spend(0, output=40, message_id="s1")]},
    )
    totals = tokens_of(path)
    assert (totals["transcripts"], totals["output"]) == (2, 41)


def test_the_token_turns_and_tools_per_turn_count_different_things(tmp_path):
    """`tools_per_turn`'s denominator counts messages carrying a tool call,
    and the per-segment bars in `docs/review-handoff-protocol.md` are
    calibrated against that ratio. The token line's turn count is assistant
    messages carrying `usage` — a turn that only thought is still a turn the
    run paid for. This fixture separates them: two turns sent a call, a third
    only spoke."""
    path = write_run(
        tmp_path,
        [
            *worked(0, "a", output=1),
            *worked(10, "b", command="ruff check .", output=1),
            spend(20, output=1, message_id="m3"),
        ],
    )
    data = json.loads(run(["--json", str(path)]).stdout)
    assert data["tokens"]["turns"] == 3
    assert data["tools_per_turn"] == 1.0


def load_script():
    """The script as a module, so a case can call one function directly.

    Every other case here drives the CLI, because that is what a person runs.
    One path cannot be reached that way: `subagent_transcripts` walks for
    FILES, so a name that is not a readable file never becomes a path the CLI
    hands on. Mutation-testing found that — the `except OSError` guard could
    be removed with the whole slice still green."""
    spec = importlib.util.spec_from_file_location("session_cost", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_a_transcript_that_cannot_be_opened_is_skipped_rather_than_raised(tmp_path):
    """A segment deleted between the walk and the open, or one whose
    permissions the walk could not see. Both totals shrink — one fewer
    transcript, and that segment's spend missing — and nothing raises."""
    good = tmp_path / "good.jsonl"
    good.write_text(spend(0, output=9, message_id="s1") + "\n")
    totals = load_script().token_totals([str(tmp_path / "gone.jsonl"), str(good)])
    assert (totals["transcripts"], totals["turns"], totals["output"]) == (1, 1, 9)


def test_a_junk_segment_shrinks_the_numbers_rather_than_stopping_the_report(tmp_path):
    """Three things sit under `subagents/` here: a readable transcript, one
    whose lines are not JSON, and a name that is a directory rather than a
    file. The report degrades to a smaller number the way a malformed line
    does, and the transcript count is what makes the gap visible to the
    person who spawned the segments."""
    path = write_run(
        tmp_path,
        worked(0, "a", output=5),
        {
            "good.jsonl": [spend(0, output=2, message_id="s1")],
            "junk.jsonl": ["not json"],
        },
    )
    (tmp_path / "main" / "subagents" / "gone.jsonl").mkdir()
    proc = run(["--json", str(path)])
    assert proc.returncode == 0, proc.stderr
    totals = json.loads(proc.stdout)["tokens"]
    assert (totals["transcripts"], totals["output"]) == (3, 7)


def test_the_printed_token_line_names_the_transcripts_it_covered(tmp_path):
    """Contract §14: the line is text a person reads and acts on, so a case
    pins its wording. The transcript count is the load-bearing half — every
    way this can go wrong prints a SMALLER number rather than failing, and
    only the person who spawned the segments can tell that `1 transcript` is
    wrong for a run that spawned six."""
    path = write_run(
        tmp_path,
        worked(0, "a", output=1000, cache_write=5000, cache_read=9000),
        {
            "one.jsonl": [spend(0, output=234, cache_write=678, message_id="s1")],
            "two.jsonl": [spend(0, cache_read=12, message_id="s2")],
        },
    )
    out = run([str(path)]).stdout
    assert re.search(r"^tokens\s+3 transcripts, 3 turns$", out, re.M), out
    assert re.search(r"^  output\s+1,234$", out, re.M), out
    assert re.search(r"^  cache write\s+5,678$", out, re.M), out
    assert re.search(r"^  cache read\s+9,012$", out, re.M), out


def test_the_token_line_says_one_transcript_rather_than_1_transcripts(tmp_path):
    """A count a person reads: `1 transcript`, not `1 transcripts`."""
    path = write_run(tmp_path, worked(0, "a", output=5))
    out = run([str(path)]).stdout
    assert re.search(r"^tokens\s+1 transcript, 1 turn$", out, re.M), out


# --- one odd row must not end the report ------------------------------------
#
# Round 1's findings 1 and 2, and round 2's finding 1. `parse_time`'s
# docstring states the file's rule for the whole file — "one odd row must not
# end the report" — and every reader below broke it the same way: a value
# taken out of a transcript was used as a dict key, an arithmetic operand or
# a format target without anything checking what it was. All of them are
# pinned here, because a raise in any one kills the same report.
#
# The class was closed twice, and the second time it was enumerated rather
# than eyeballed. Round 1 fixed six members and left a seventh one line away;
# round 2's fix pass took every field the readers read — the list from
# `grep '\.get(' session_cost.py`, not from memory — crossed it with every
# type JSON can carry and with the field being absent, and ran all 288
# variants. The seventh was the only survivor, and it had two crash sites
# rather than the one the finding named.


def odd(second, usage=None, message_id=None, blocks=None, message=None):
    """One row built field by field, so a case can write a shape the helpers
    above cannot: a `usage` value that is not a number, an id that is not a
    key, a `message` that is not an object at all."""
    if message is None:
        message = {
            "content": blocks
            if blocks is not None
            else [{"type": "text", "text": "."}],
            "usage": {} if usage is None else usage,
        }
        if message_id is not None:
            message["id"] = message_id
    return json.dumps({"timestamp": stamp_at(second), "message": message})


def test_a_transcript_with_usage_and_no_tool_call_still_reports_its_tokens(tmp_path):
    """Finding 1. The token line was computed after `analyse`'s guard, so a
    transcript carrying `usage` and no PAIRED tool call exited with `no tool
    calls in this transcript` and printed nothing — not the time lines it
    cannot produce, and not the tokens it can. That transcript is a segment
    that read and thought, which is exactly what the run-level table's
    per-kind token row is summed over."""
    path = tmp_path / "quiet.jsonl"
    path.write_text(odd(0, {"output_tokens": 7, "cache_read_input_tokens": 70}) + "\n")
    proc = run([str(path)])
    assert proc.returncode == 0, proc.stderr
    assert "no paired tool call in this transcript" in proc.stdout, proc.stdout
    assert re.search(r"^tokens\s+1 transcript, 1 turn$", proc.stdout, re.M), proc.stdout
    assert re.search(r"^  output\s+7$", proc.stdout, re.M), proc.stdout
    assert re.search(r"^  cache read\s+70$", proc.stdout, re.M), proc.stdout
    assert json.loads(run(["--json", str(path)]).stdout)["tokens"]["output"] == 7


def test_a_usage_value_that_is_not_a_number_contributes_zero(tmp_path):
    """Finding 2, first half. A harness writing `output_tokens` as the string
    `"12"` raised `TypeError: unsupported operand type(s) for +=` out of
    `token_totals`, and a `null` where an int was expected is the same shape.
    A value this file cannot add is a value it does not have — which is the
    direction `token_totals`' docstring promises."""
    path = write_run(
        tmp_path,
        [
            *worked(0, "a", output=5),
            odd(
                2,
                {
                    "output_tokens": "12",
                    "cache_write_input_tokens": None,
                    "cache_read_input_tokens": True,
                },
                message_id="m2",
            ),
        ],
    )
    totals = tokens_of(path)
    assert (totals["turns"], totals["output"], totals["cache_read"]) == (2, 5, 0)


def test_a_message_id_that_is_not_a_key_does_not_end_the_report(tmp_path):
    """Finding 2, second half, and the same defect in `load`. An id written as
    a list is not hashable, and both readers put it straight into a `set`:
    `load` raised before `token_totals` was ever reached, so one odd row lost
    the whole report rather than its own numbers. The row keys by its own
    position instead, which is the floor `load`'s docstring already names.

    The odd row carries a tool call, because that is what reaches `load`'s
    own set lookup — a row that only spoke short-circuits on `carries_call`
    and would have exercised one reader of the two."""
    path = write_run(
        tmp_path,
        [
            *worked(0, "a", output=5),
            odd(
                2,
                {"output_tokens": 3},
                message_id=["m2"],
                blocks=[use("b", "ruff check .")],
            ),
            plain_result(3, "b"),
        ],
    )
    data = json.loads(run(["--json", str(path)]).stdout)
    assert data["calls"] == 2
    assert (data["tokens"]["turns"], data["tokens"]["output"]) == (2, 8)


def test_a_tool_call_whose_id_is_not_a_key_loses_its_pairing_only(tmp_path):
    """The same class one level down: `load` indexes `pending` by the
    `tool_use` block's own id, and by the `tool_result`'s `tool_use_id`. A
    list in either raised. The unpairable call cannot be timed, so it is not
    a call — and the rest of the transcript still reports."""
    path = write_run(
        tmp_path,
        [
            *worked(0, "a", output=5),
            odd(
                10,
                {"output_tokens": 1},
                message_id="m3",
                blocks=[{"type": "tool_use", "id": ["b"], "name": "Bash", "input": {}}],
            ),
            odd(
                11,
                message_id="m4",
                blocks=[{"type": "tool_result", "tool_use_id": ["b"]}],
            ),
        ],
    )
    data = json.loads(run(["--json", str(path)]).stdout)
    assert data["calls"] == 1
    assert data["tokens"]["output"] == 6


def test_a_row_that_is_not_the_shape_the_readers_assume_is_dropped(tmp_path):
    """`message` as a string and a top-level row that is not an object at
    all. `token_totals` checked both with `isinstance`; `load` checked
    neither and raised `AttributeError` on `.get`. One reader's guard is not
    the other's."""
    path = write_run(
        tmp_path,
        [
            *worked(0, "a", output=5),
            json.dumps({"timestamp": stamp_at(2), "message": "hello"}),
            json.dumps(["not", "a", "row"]),
            json.dumps({"timestamp": stamp_at(3), "message": {"content": "text"}}),
        ],
    )
    data = json.loads(run(["--json", str(path)]).stdout)
    assert data["calls"] == 1
    assert (data["tokens"]["turns"], data["tokens"]["output"]) == (1, 5)


def test_a_tool_name_that_is_not_a_name_does_not_end_the_report(tmp_path):
    """Round 2's finding 1 — the seventh member of the class, three lines
    below the `call_id` the same pass guarded. `load` stored
    `block.get("name", "?")` with no type check, and TWO readers consume it.

    Which reader dies depends on the shape, which is why a guard at the
    reported crash site would have left the other standing. A list or an
    object is unhashable and ends `analyse`, where the name is a `by_family`
    key — before `main` has printed anything, the token block included,
    which is the outcome round 1's finding 1 was raised to end. A `null`
    name hashes fine, passes `analyse`, and raises `unsupported format
    string passed to NoneType.__format__` in `report`'s `by family` block
    instead: the span and token lines are already on screen, so it reads as
    a report that worked and then stopped.

    Both are fixed at the source, so the name is a string before either
    reader sees it. The call is charged to `?` rather than to its family —
    smaller, in the direction `count` and `message_key` already take — and
    `?` is the floor `load` had already written for a block carrying no
    `name` at all, so a name this file cannot use reads as a name that was
    never there."""
    for uid, name in (("b", ["Bash"]), ("c", {"n": 1}), ("d", None)):
        directory = tmp_path / f"name-{uid}"
        directory.mkdir()
        path = write_run(
            directory,
            [
                *worked(0, "a", output=5),
                spend(
                    10,
                    output=3,
                    message_id=f"m-{uid}",
                    blocks=[
                        {
                            "type": "tool_use",
                            "id": uid,
                            "name": name,
                            "input": {"command": "ruff check ."},
                        }
                    ],
                ),
                plain_result(11, uid),
            ],
        )
        proc = run([str(path)])
        assert proc.returncode == 0, f"{name!r}: {proc.stderr}"
        # `analyse`'s `by_family` key — where a list and an object ended it.
        assert re.search(r"^  \?\s+1 calls", proc.stdout, re.M), (
            f"{name!r}: {proc.stdout}"
        )
        # `report`'s `:<12` format — where a `null` ended it, with these two
        # lines already printed above the `by family` block it died in.
        assert re.search(r"^span\s", proc.stdout, re.M), f"{name!r}: {proc.stdout}"
        assert re.search(r"^tokens\s+1 transcript, 2 turns$", proc.stdout, re.M), (
            f"{name!r}: {proc.stdout}"
        )
        data = json.loads(run(["--json", str(path)]).stdout)
        assert (data["calls"], data["by_family"]["?"]["calls"]) == (2, 1)


def test_the_report_tells_its_two_turn_counts_apart(tmp_path):
    """Finding 5. The printed report carried the word `turns` in two meanings
    over two scopes with nothing between them: the token line's count is every
    assistant message across the whole run, and `tools_per_turn`'s denominator
    is the messages of THIS transcript that sent a call. A reader divided one
    into the other — 1.08 tools per turn printed beside 659 turns and 211
    calls, which divides to 0.32.

    So each count now says what it counts and over what. The numbers are
    unchanged; what changes is that they can no longer be read as one."""
    path = write_run(
        tmp_path,
        [
            *worked(0, "a", output=1),
            *worked(10, "b", command="ruff check .", output=1),
            odd(20, {"output_tokens": 1}, message_id="m3"),
        ],
        {"one.jsonl": [odd(0, {"output_tokens": 1}, message_id="s1")]},
    )
    out = run([str(path)]).stdout
    assert re.search(r"^tokens\s+2 transcripts, 4 turns$", out, re.M), out
    assert "a turn is any assistant message, in every transcript counted" in out, out
    assert "2 calls over 2 turns that sent one, in this transcript alone" in out, out


def at(stamp, blocks, message_id=None, usage=None):
    """One row with its timestamp written out rather than taken off the clock.

    `stamp_at` carries a fixed zone-aware clock, so a case built from it can
    never write the two shapes below: two rows sharing one instant, and a
    stamp carrying no zone at all. This harness produces neither — 299 real
    transcripts held 0 calls with `start == end` and 94,514 of 94,514
    timestamps zone-aware — so the cases build them by hand."""
    message = {"content": blocks}
    if usage is not None:
        message["usage"] = usage
    if message_id:
        message["id"] = message_id
    return json.dumps({"timestamp": stamp, "message": message})


def paired(uid, start, end, command="pytest -q"):
    """A call and its result at two stamps given verbatim."""
    return [
        at(start, [use(uid, command)], f"call-{uid}", {"output_tokens": 1}),
        at(end, [{"type": "tool_result", "tool_use_id": uid}]),
    ]


def test_a_span_of_zero_prints_what_it_can_rather_than_dividing_by_it(tmp_path):
    """A transcript whose only paired call begins and ends on one timestamp
    has `span_s == 0.0`, and three lines of `report` divide by it.

    The span line printed and then `ZeroDivisionError` took the rest — the
    token block and the family table included. That is the same shape a
    `null` tool name produced one axis over: a report that worked and then
    stopped, which reads as a report rather than as a crash.

    What replaces the percentage is a dash and one line saying why, not a
    number. A share of a span of zero is not 0% and not 100%; it does not
    exist, and the times themselves are what was measured."""
    path = tmp_path / "zero.jsonl"
    path.write_text(
        "\n".join(paired("a", "2026-08-24T10:00:00Z", "2026-08-24T10:00:00Z")) + "\n"
    )

    proc = run([str(path)])
    assert proc.returncode == 0, proc.stderr
    assert re.search(r"^span\s+0\.0m\s+\(1 tool calls\)$", proc.stdout, re.M), (
        proc.stdout
    )
    assert (
        "every call shares one timestamp, so there is no span to take a share of"
        in proc.stdout
    ), proc.stdout
    # No percentage invented for a denominator of zero.
    assert re.search(r"^  command\s+0\.0m\s+—$", proc.stdout, re.M), proc.stdout
    assert re.search(r"^  model\s+0\.0m\s+—\s+mean gap 0\.0s$", proc.stdout, re.M), (
        proc.stdout
    )
    # The two blocks the crash used to take with it, both below the span line.
    assert re.search(r"^tokens\s+1 transcript, 1 turn$", proc.stdout, re.M), proc.stdout
    assert re.search(r"^  test\s+1 calls", proc.stdout, re.M), proc.stdout

    # `--json` never reached `report`, so it survived a zero span already;
    # this arm is what keeps the guard from being moved into `analyse`.
    machine = run(["--json", str(path)])
    assert machine.returncode == 0, machine.stderr
    assert json.loads(machine.stdout)["span_s"] == 0.0


def test_a_naive_stamp_does_not_end_the_report(tmp_path):
    """`parse_time` is the one place a string becomes a `datetime`, so it is
    where a stamp carrying no zone is given one: UTC, the assumption the same
    line already makes when it rewrites a trailing `Z`.

    Mixing a naive stamp with an aware one raised `TypeError` with stdout
    empty on the report and on `--json` alike, and it raised from two
    different sites depending on how many calls the transcript held. One
    call dies on a SUBTRACTION in `analyse`, where the span is taken. Two
    die earlier, on a COMPARISON in `load`'s sort, before `analyse` is
    called at all — so a guard written at the reported crash site would have
    left the other standing.

    The third shape is why the naive row is normalised rather than dropped
    the way an unparseable one is: a transcript whose stamps are ALL naive
    keeps reporting numbers that are internally consistent, where dropping
    would have left it reporting nothing."""
    shapes = (
        # One call, aware start and naive end — the subtraction in `analyse`.
        (
            "mixed-pair",
            paired("a", "2026-08-24T10:00:00Z", "2026-08-24T10:00:10"),
            10.0,
            10.0,
        ),
        # Two calls, one pair of each — the comparison in `load`'s sort.
        (
            "mixed-calls",
            [
                *paired("a", "2026-08-24T10:00:00Z", "2026-08-24T10:00:10Z"),
                *paired(
                    "b", "2026-08-24T10:00:20", "2026-08-24T10:00:25", "ruff check ."
                ),
            ],
            25.0,
            15.0,
        ),
        # Every stamp naive — the shape that would report nothing if the row
        # were dropped instead of normalised.
        (
            "all-naive",
            paired("a", "2026-08-24T10:00:00", "2026-08-24T10:00:10"),
            10.0,
            10.0,
        ),
    )
    for name, lines, span, command_s in shapes:
        path = tmp_path / f"{name}.jsonl"
        path.write_text("\n".join(lines) + "\n")

        proc = run([str(path)])
        assert proc.returncode == 0, f"{name}: {proc.stderr}"
        assert re.search(r"^span\s", proc.stdout, re.M), f"{name}: {proc.stdout}"
        assert re.search(r"^tokens\s", proc.stdout, re.M), f"{name}: {proc.stdout}"

        # #175 records the naive case as exiting 1 with stdout EMPTY on both,
        # so both arms are asserted rather than the printed one alone.
        machine = run(["--json", str(path)])
        assert machine.returncode == 0, f"{name}: {machine.stderr}"
        data = json.loads(machine.stdout)
        assert (data["span_s"], data["command_s"]) == (span, command_s), (
            f"{name}: {data}"
        )


def turn_at(index, usage, uid):
    """One tool-call turn with its `usage` written out.

    `token_thirds` needs three turns carrying a non-zero input count before
    it computes anything, so a case about a non-finite input has to build
    three rather than reuse the one-call fixtures above.

    The stamps come off `stamp_at`, the module's own clock, rather than from
    interpolating `index` into a fixed prefix. The prefix version built
    `10:010:00` at index 10, which `datetime.fromisoformat` refuses — so
    `parse_time` returned None, `load` dropped the row, and the case went on
    asserting exit 0 while measuring one turn fewer than it said."""
    return [
        at(stamp_at(index * 60), [use(uid, "pytest -q")], f"m{uid}", usage),
        at(
            stamp_at(index * 60 + 30),
            [{"type": "tool_result", "tool_use_id": uid}],
        ),
    ]


def test_a_nan_token_count_does_not_end_the_report(tmp_path):
    """`json.loads` accepts the bare tokens `NaN`, `Infinity` and
    `-Infinity`, and all three are `float`, so a type check alone passes
    them through.

    `token_thirds` rounds a mean, and `round()` raises on a non-finite
    float — `ValueError` for a `NaN`, `OverflowError` for an infinity. The
    report ended with exit 1 and stdout EMPTY, on the report and on `--json`
    alike, which is worse than either shape #175 was opened for.

    Every usage field except `output_tokens` reaches that `round`, through
    `load`'s `input_tokens + cache_read_input_tokens` pair. `output_tokens`
    is the one field that does not, and it is the field the residual was
    first measured on — which is how a crash was recorded as printing `nan`
    at exit 0. So the fields are asserted apart rather than together."""
    shapes = (
        ("input-nan", 0, {"input_tokens": float("nan"), "output_tokens": 1}),
        ("input-inf", 0, {"input_tokens": float("inf"), "output_tokens": 1}),
        (
            "cache-read-nan",
            1,
            {
                "input_tokens": 10,
                "output_tokens": 1,
                "cache_read_input_tokens": float("nan"),
            },
        ),
        ("output-nan", 2, {"input_tokens": 10, "output_tokens": float("nan")}),
        # An integer with no float of its own. `json.loads` builds one from
        # any integer literal, and the finiteness question converts before it
        # answers — so asking it raises `OverflowError` instead of answering,
        # inside the very funnel that exists to keep such a value out.
        ("output-huge-int", 0, {"input_tokens": 10, "output_tokens": HUGE_INT}),
        ("input-huge-int", 0, {"input_tokens": HUGE_INT, "output_tokens": 1}),
    )
    for name, odd, usage in shapes:
        lines = []
        for n in range(3):
            plain = {"input_tokens": 10, "output_tokens": 1}
            lines += turn_at(n, usage if n == odd else plain, f"c{n}")
        path = tmp_path / f"{name}.jsonl"
        # `json.dumps` writes bare `NaN` and `Infinity`, which is exactly the
        # shape a harness produces and `json.loads` accepts back.
        path.write_text("\n".join(lines) + "\n")

        proc = run([str(path)])
        assert proc.returncode == 0, f"{name}: {proc.stderr}"
        assert re.search(r"^tokens\s", proc.stdout, re.M), f"{name}: {proc.stdout}"

        machine = run(["--json", str(path)])
        assert machine.returncode == 0, f"{name}: {machine.stderr}"
        data = json.loads(machine.stdout)
        # Charged 0, the direction every funnel in the file already takes —
        # never carried through as `nan`, which prints and compares wrongly.
        assert all(isinstance(v, int) for v in data["context_growth"]), (
            f"{name}: {data['context_growth']}"
        )
        for field in ("output", "cache_read", "cache_write"):
            # An integer of any size is accepted without converting it, and a
            # float has to be finite. Neither arm converts, because both
            # `int(...)` and `math.isfinite(...)` RAISE on a value that got
            # through — the huge-int arms above would then read as a test
            # error rather than as the defect this case pins.
            value = data["tokens"][field]
            assert not isinstance(value, float) or math.isfinite(value), (
                f"{name}: {data['tokens']}"
            )


def test_a_sum_of_entered_values_does_not_end_the_report(tmp_path):
    """`count` answers for each value that ENTERS. Nothing answered for what
    the arithmetic then MADE of two of them.

    `load` adds `input_tokens` to `cache_read_input_tokens` per turn, and
    `token_thirds` sums a slice of those and divides. Two counts that each
    pass the finiteness question can add to one that does not — and the
    rounding at the end then raised `OverflowError` with stdout empty, on
    the report and on `--json` alike.

    Three arms, because the sum overflows by three different routes:
    two floats whose sum is an infinity; two integers that each have a float
    where the sum does not; and one such field on enough turns that a single
    third of the list sums past the range on its own, which no per-turn
    guard could see.

    This is a separate case from the one above on purpose. That one is about
    the values a transcript carries, and this one is about what the file
    computes from two of them — the distinction three review rounds spent
    themselves on."""
    shapes = (
        # Each field finite, their per-turn sum an infinity.
        (
            "two-floats",
            3,
            {
                "input_tokens": TOP_FLOAT,
                "cache_read_input_tokens": TOP_FLOAT,
                "output_tokens": 1,
            },
            (0,),
        ),
        # Each int HAS a float; their sum does not. `count` passes both.
        (
            "two-ints",
            3,
            {
                "input_tokens": int(TOP_FLOAT),
                "cache_read_input_tokens": int(TOP_FLOAT),
                "output_tokens": 1,
            },
            (0,),
        ),
        # One field, on two of six turns, so one third of the list holds two
        # of them and the SLICE sum overflows with every turn finite.
        ("summed-third", 6, {"input_tokens": TOP_FLOAT, "output_tokens": 1}, (0, 1)),
    )
    for name, count_of_turns, odd_usage, odd_indices in shapes:
        lines = []
        for n in range(count_of_turns):
            plain = {"input_tokens": 10, "output_tokens": 1}
            lines += turn_at(n, odd_usage if n in odd_indices else plain, f"c{n}")
        path = tmp_path / f"{name}.jsonl"
        path.write_text("\n".join(lines) + "\n")

        proc = run([str(path)])
        assert proc.returncode == 0, f"{name}: {proc.stderr}"
        assert re.search(r"^tokens\s", proc.stdout, re.M), f"{name}: {proc.stdout}"

        machine = run(["--json", str(path)])
        assert machine.returncode == 0, f"{name}: {machine.stderr}"
        data = json.loads(machine.stdout)
        # A mean the file could not compute is charged 0, never carried out
        # as an infinity for a reader to mistake for a measurement.
        for value in data["context_growth"]:
            assert isinstance(value, int), f"{name}: {data['context_growth']}"


def test_a_negative_span_says_what_it_actually_saw(tmp_path):
    """A span of zero and a negative span are not the same reading, and one
    sentence claimed the first for both.

    `report` printed *every call shares one timestamp* under any span that is
    not positive. For a transcript whose last result predates the first call
    — a harness writing a result before the call it answers — that sentence
    is false about a file the reader cannot see, which is the failure mode a
    sentence under a dash exists to prevent.

    The share itself is unchanged: neither shape gets a percentage, because
    a share of a non-positive span is not a number anybody can read."""
    lines = [
        at("2026-08-24T10:00:00Z", [use("a", "pytest -q")], "ma", {"output_tokens": 1}),
        at("2026-08-24T09:00:00Z", [{"type": "tool_result", "tool_use_id": "a"}]),
        at(
            "2026-08-24T10:05:00Z",
            [use("b", "ruff check .")],
            "mb",
            {"output_tokens": 1},
        ),
        at("2026-08-24T09:30:00Z", [{"type": "tool_result", "tool_use_id": "b"}]),
    ]
    path = tmp_path / "negative.jsonl"
    path.write_text("\n".join(lines) + "\n")

    proc = run([str(path)])
    assert proc.returncode == 0, proc.stderr
    assert re.search(r"^span\s+-\d", proc.stdout, re.M), proc.stdout
    assert "the last call to begin ended before the first call began" in proc.stdout, (
        proc.stdout
    )
    # The zero-span sentence must NOT be the one a negative span gets.
    assert "every call shares one timestamp" not in proc.stdout, proc.stdout
    assert re.search(r"^  command\s+\S+\s+—$", proc.stdout, re.M), proc.stdout
    # And no idle figure, which is what a negative denominator makes of the
    # `idle > span * 0.1` threshold: the comparison is against a negative
    # number, so it is true, and the line printed sixty-five minutes of idle
    # beside a span of minus thirty.
    assert "idle" not in proc.stdout, proc.stdout

    # The sentence has to hold for EVERY negative span, not for the one shape
    # it was written against. The span is taken from the last call to BEGIN,
    # because `load` sorts by start — so the last RESULT can arrive hours
    # after the first call and the span still be negative.
    later = [
        at("2026-08-24T10:00:00Z", [use("a", "pytest -q")], "ma", {"output_tokens": 1}),
        at("2026-08-24T12:00:00Z", [{"type": "tool_result", "tool_use_id": "a"}]),
        at(
            "2026-08-24T10:05:00Z",
            [use("b", "ruff check .")],
            "mb",
            {"output_tokens": 1},
        ),
        at("2026-08-24T09:00:00Z", [{"type": "tool_result", "tool_use_id": "b"}]),
    ]
    out_of_order = tmp_path / "out-of-order.jsonl"
    out_of_order.write_text("\n".join(later) + "\n")
    third = run([str(out_of_order)])
    assert third.returncode == 0, third.stderr
    assert re.search(r"^span\s+-\d", third.stdout, re.M), third.stdout
    # The last result here arrived at 12:00, two hours AFTER the first call
    # began, so a sentence about the last result would be false.
    assert "the last call to begin ended before the first call began" in third.stdout, (
        third.stdout
    )
    assert "idle" not in third.stdout, third.stdout

    # A negative span makes every duration derived from it negative, and the
    # lines that INTERPRET a duration must not fire on one. `repeats` is
    # printed on a truthiness test, which minus sixty minutes satisfies — so
    # the report claimed an hour of work re-run for a result already in hand,
    # on a transcript where nothing was re-run at all. The `nothing obvious`
    # line below is suppressed by the same value, for the same reason.
    repeated = [
        at("2026-08-24T10:00:00Z", [use("a", "pytest -q")], "ma", {"output_tokens": 1}),
        at("2026-08-24T09:00:00Z", [{"type": "tool_result", "tool_use_id": "a"}]),
        at("2026-08-24T10:05:00Z", [use("b", "pytest -q")], "mb", {"output_tokens": 1}),
        at("2026-08-24T09:30:00Z", [{"type": "tool_result", "tool_use_id": "b"}]),
    ]
    repeats = tmp_path / "repeats.jsonl"
    repeats.write_text("\n".join(repeated) + "\n")
    fourth = run([str(repeats)])
    assert fourth.returncode == 0, fourth.stderr
    assert re.search(r"^span\s+-\d", fourth.stdout, re.M), fourth.stdout
    assert "repeats" not in fourth.stdout, fourth.stdout

    # The same negative duration must not SUPPRESS a line either. The
    # `nothing obvious` line is gated on there being no repeat time, and a
    # negative repeat time reads as falsey — so the report went silent on a
    # transcript it had nothing to say about, which is the same defect as
    # the repeats line one gate over. Two calls in ONE message put tools per
    # turn above the threshold that line also needs.
    batched = [
        at(
            "2026-08-24T10:00:00Z",
            [use("x", "pytest -q"), use("y", "pytest -q")],
            "mx",
            {"output_tokens": 1},
        ),
        at("2026-08-24T09:00:00Z", [{"type": "tool_result", "tool_use_id": "x"}]),
        at("2026-08-24T09:30:00Z", [{"type": "tool_result", "tool_use_id": "y"}]),
    ]
    suppressed = tmp_path / "suppressed.jsonl"
    suppressed.write_text("\n".join(batched) + "\n")
    fifth = run([str(suppressed)])
    assert fifth.returncode == 0, fifth.stderr
    assert re.search(r"^span\s+-\d", fifth.stdout, re.M), fifth.stdout
    assert "repeats" not in fifth.stdout, fifth.stdout
    assert "nothing obvious" in fifth.stdout, fifth.stdout

    # And a span of exactly zero keeps the sentence written for it.
    zero = tmp_path / "zero.jsonl"
    zero.write_text(
        "\n".join(paired("a", "2026-08-24T10:00:00Z", "2026-08-24T10:00:00Z")) + "\n"
    )
    other = run([str(zero)])
    assert other.returncode == 0, other.stderr
    assert "every call shares one timestamp" in other.stdout, other.stdout
    assert "the last call to begin" not in other.stdout, other.stdout


# --- #193: a third the file could not compute is not a baseline -------------


def test_a_charged_third_is_not_a_baseline_the_context_line_multiplies(tmp_path):
    """`token_thirds` charges 0 for a mean it cannot compute, and the context
    line took that 0 for a measurement.

    The threshold is a multiple of the FIRST third, so any positive last third
    clears a threshold of zero. A transcript whose first third overflowed and
    whose last third is ordinary printed `0 -> 10 input tokens; later calls
    cost more than the same call would have earlier` — the input had collapsed
    by 307 orders of magnitude and the line said it grew.

    Which direction the reader was told depended on which third overflowed,
    which is why both are here: with the charged third LAST the line is
    suppressed, and that arm was already correct and must stay so.

    Exit 0 throughout. This is the wrong-number direction rather than the
    ended-report one, which is why nothing above it caught it."""
    for name, odd_index in (("first-third", 0), ("last-third", 5)):
        lines = []
        for n in range(6):
            usage = (
                {"input_tokens": TOP_FLOAT, "cache_read_input_tokens": TOP_FLOAT}
                if n == odd_index
                else {"input_tokens": 10}
            )
            lines += turn_at(n, {**usage, "output_tokens": 1}, f"b{n}")
        path = tmp_path / f"{name}.jsonl"
        path.write_text("\n".join(lines) + "\n")

        proc = run([str(path)])
        assert proc.returncode == 0, f"{name}: {proc.stderr}"
        assert "context" not in proc.stdout, f"{name}: {proc.stdout}"

        machine = run(["--json", str(path)])
        assert machine.returncode == 0, f"{name}: {machine.stderr}"
        growth = json.loads(machine.stdout)["context_growth"]
        assert growth[0 if odd_index == 0 else 2] == 0, f"{name}: {growth}"


def test_the_context_line_still_prints_where_the_baseline_is_real(tmp_path):
    """The conjunct above must not have bought its silence by silencing the
    line. A first third of ten and a last third of a hundred is the growth the
    line exists to report, and it is asserted with the numbers in it."""
    lines = []
    for n in range(6):
        lines += turn_at(n, {"input_tokens": 10 if n < 3 else 100}, f"g{n}")
    path = tmp_path / "real-growth.jsonl"
    path.write_text("\n".join(lines) + "\n")

    proc = run([str(path)])
    assert proc.returncode == 0, proc.stderr
    assert "10 → 100 input tokens" in proc.stdout, proc.stdout


def test_a_negative_input_count_is_dropped_and_a_zero_is_dropped_with_it(tmp_path):
    """`token_thirds`' input filter was a truthiness test on a signed number,
    so it dropped a zero and KEPT a negative.

    Six turns whose first three carry minus ten give a growth of [-10, 0, 10]
    and print the context line off a baseline no harness can mean. The fix is
    the same inversion round 3's three statements had.

    The zero arm is here to pin the half that did NOT change: `count` answers
    0 both for a field a harness never wrote and for one it wrote as 0, so the
    file cannot tell a turn that spent nothing from a turn nobody measured,
    and both go on being dropped. Six turns carrying zero leave fewer than
    three inputs, so there is no growth at all."""
    negatives = []
    for n in range(6):
        negatives += turn_at(n, {"input_tokens": -10 if n < 3 else 10}, f"n{n}")
    path = tmp_path / "negative.jsonl"
    path.write_text("\n".join(negatives) + "\n")

    proc = run(["--json", str(path)])
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["context_growth"] == [10, 10, 10], proc.stdout
    printed = run([str(path)])
    assert "context" not in printed.stdout, printed.stdout

    zeros = []
    for n in range(6):
        zeros += turn_at(n, {"input_tokens": 0}, f"z{n}")
    path = tmp_path / "zero-input.jsonl"
    path.write_text("\n".join(zeros) + "\n")

    machine = run(["--json", str(path)])
    assert machine.returncode == 0, machine.stderr
    assert json.loads(machine.stdout)["context_growth"] == [], machine.stdout
