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
    a share of a non-positive span is not a number anybody can read.

    **#300 narrowed what a negative span means, and one arm below flipped
    with it.** The span ends at the last call to END, so it goes negative
    only when EVERY call ended before the first call began — not merely when
    the last call to begin did. A transcript holding one call that ran for
    two hours is no longer read as negative, which is the shape the third arm
    now pins."""
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
    assert "no call ended after the first call began" in proc.stdout, proc.stdout
    # The zero-span sentence must NOT be the one a negative span gets.
    assert "every call shares one timestamp" not in proc.stdout, proc.stdout
    assert re.search(r"^  command\s+\S+\s+—$", proc.stdout, re.M), proc.stdout
    # And no idle figure, which is what a negative denominator makes of the
    # `idle > span * 0.1` threshold: the comparison is against a negative
    # number, so it is true, and the line printed sixty-five minutes of idle
    # beside a span of minus thirty.
    assert "idle" not in proc.stdout, proc.stdout

    # The sentence has to hold for EVERY negative span, not for the one shape
    # it was written against — and after #300 this shape is not one of them.
    # The span ends at the last call to END, so a call running 10:00 to 12:00
    # gives a run of two hours however early the OTHER call's result was
    # written. Under the old rule the span was `calls[-1]["end"]` over a list
    # sorted by start, so this transcript read minus sixty minutes for a run
    # that plainly lasted two, and the sentence below was the true statement
    # about a number that should never have been negative.
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
    # 120 minutes, and neither non-positive sentence: call `a` really did run
    # from 10:00 to 12:00, and that is the run's wall clock whatever order
    # the results were written in.
    assert re.search(r"^span\s+120\.0m", third.stdout, re.M), third.stdout
    assert "no call ended after the first call began" not in third.stdout, third.stdout
    assert "every call shares one timestamp" not in third.stdout, third.stdout

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
    assert "no call ended after the first call began" not in other.stdout, other.stdout


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


# --- #202: a streamed message is counted at its completed row ---------------


def test_a_streamed_message_is_counted_at_its_largest_row(tmp_path):
    """A streamed assistant message reaches the transcript as several rows
    sharing one `message.id`, and its `output_tokens` grows across them.

    Keeping the first row summed however much had been emitted when that row
    was written. Measured over the 180 transcripts on the machine that found
    it: 9,098 of 13,425 messages are split, and the reported `output` was
    4,976,637 where the completed rows give 8,683,844. One warden segment
    read as **62 output tokens across 20 turns** against a real 34,441.

    A single-row fixture cannot tell the two behaviours apart, which is why
    every case written before this one passes under either.

    `cache_write` and `cache_read` are asserted alongside because they are the
    control: they are fixed when the request is made and repeat unchanged on
    every row, so the maximum is the same number the first row gave. A change
    that started summing per row rather than per message would move all three
    together, and this case would still be green if it watched `output`
    alone."""
    rows = [
        at("2026-08-24T10:00:00Z", [use("s", "pytest -q")], "stream", partial)
        for partial in (
            {
                "output_tokens": 3,
                "cache_creation_input_tokens": 90,
                "cache_read_input_tokens": 7,
            },
            {
                "output_tokens": 400,
                "cache_creation_input_tokens": 90,
                "cache_read_input_tokens": 7,
            },
            {
                "output_tokens": 1234,
                "cache_creation_input_tokens": 90,
                "cache_read_input_tokens": 7,
            },
        )
    ]
    rows.append(
        at("2026-08-24T10:00:05Z", [{"type": "tool_result", "tool_use_id": "s"}])
    )
    path = tmp_path / "streamed.jsonl"
    path.write_text("\n".join(rows) + "\n")

    data = json.loads(run(["--json", str(path)]).stdout)
    tokens = data["tokens"]
    assert tokens["turns"] == 1, tokens
    assert tokens["output"] == 1234, tokens
    assert (tokens["cache_write"], tokens["cache_read"]) == (90, 7), tokens


def test_a_message_whose_rows_arrive_out_of_order_keeps_the_completed_count(tmp_path):
    """The reason the fix takes the maximum rather than the last row.

    The two agree on every one of the 13,425 messages measured, with 0 rows
    out of order, so last-row-wins would have been green everywhere it was
    checked. It would also have rested on an ordering the transcript format
    does not promise — and this is the transcript that separates them."""
    rows = [
        at("2026-08-24T10:00:00Z", [use("o", "pytest -q")], "reordered", usage)
        for usage in ({"output_tokens": 900}, {"output_tokens": 12})
    ]
    rows.append(
        at("2026-08-24T10:00:05Z", [{"type": "tool_result", "tool_use_id": "o"}])
    )
    path = tmp_path / "reordered.jsonl"
    path.write_text("\n".join(rows) + "\n")

    tokens = json.loads(run(["--json", str(path)]).stdout)["tokens"]
    assert (tokens["turns"], tokens["output"]) == (1, 900), tokens


def test_a_split_message_is_still_one_turn_and_not_one_per_row(tmp_path):
    """The half of the dedup that was right and had to stay right.

    A harness writes one message as one row per content block and repeats the
    usage on each. Taking the maximum per field must not become a sum per row:
    three rows of one message are one turn, and `cache_read` — which repeats
    unchanged — must read 500 rather than 1,500."""
    rows = [
        at(
            "2026-08-24T10:00:00Z",
            [use(f"b{n}", "pytest -q")],
            "one",
            {
                "output_tokens": 10,
                "cache_read_input_tokens": 500,
            },
        )
        for n in range(3)
    ]
    rows += [
        at("2026-08-24T10:00:05Z", [{"type": "tool_result", "tool_use_id": f"b{n}"}])
        for n in range(3)
    ]
    path = tmp_path / "split.jsonl"
    path.write_text("\n".join(rows) + "\n")

    tokens = json.loads(run(["--json", str(path)]).stdout)["tokens"]
    assert (tokens["turns"], tokens["output"], tokens["cache_read"]) == (1, 10, 500), (
        tokens
    )


def test_load_returns_input_counts_only(tmp_path):
    """`load`'s per-turn tuple used to carry a third element, this message's
    `output_tokens`, and nothing in the file read it.

    It is removed rather than repaired: `output_tokens` is the one field that
    grows across a split message's rows, so what sat there was the first
    partial count — the same defect as #202, waiting for its first reader.
    The input-side fields are fixed when the request is made and repeat
    unchanged, which is why they can be taken from the first row.

    Pinned on the shape rather than on the length alone, so a tuple that
    regrows a third element under a different meaning still fails."""
    module = load_script()
    rows = [
        at(
            "2026-08-24T10:00:00Z",
            [use("l", "pytest -q")],
            "m",
            {
                "input_tokens": 11,
                "cache_read_input_tokens": 4,
                "output_tokens": 999,
            },
        ),
        at("2026-08-24T10:00:05Z", [{"type": "tool_result", "tool_use_id": "l"}]),
    ]
    path = tmp_path / "load.jsonl"
    path.write_text("\n".join(rows) + "\n")

    _calls, turns = module.load(str(path))
    assert len(turns) == 1, turns
    assert len(turns[0]) == 2, turns
    assert turns[0][1] == 15, turns


# --- #200: the family names the runner a repository actually uses -----------


def test_a_runner_named_by_path_is_a_test_run(tmp_path):
    """A project that ships `bin/test` has said what its test command is, in
    the filesystem, and the five names the family knew did not include it.

    Measured over the 180 transcripts on the machine that found it: of the
    `./bin/test` calls, 266 were charged to `other` — the row nobody reads
    because it is the row everything falls into — and the rest landed in four
    different families depending on what else shared the command line.

    The negative arm is the same size as the positive one on purpose. A
    pattern widened until the row is never empty is a row that means nothing,
    so a directory called `testdata`, a `git log` mentioning the word, and a
    lint run that shares a line with none of them must all stay out."""
    module = load_script()
    for command in (
        "./bin/test",
        "bin/test -q",
        "scripts/test",
        "scripts/test.sh --fast",
        "./test.sh",
        "make test",
        "npm test",
        "npm run test",
        "pnpm run test -- --watch=false",
        "./gradlew test",
        "just test",
        "tox -e py312",
        "nox -s tests",
        "rspec spec/models",
        "phpunit --testsuite unit",
        "dotnet test",
        "bun test",
        "deno test -A",
        "uv run --with pytest pytest tests/ -q",
    ):
        assert module.family(command) == "test", command

    for command in (
        "bin/testdata --list",
        "git log --oneline -- test",
        "uvx ruff check .",
        "./bin/evidence-check",
        "python3 .github/scripts/rider_check.py",
        "cat tests/test_session_cost.py",
    ):
        assert module.family(command) != "test", command


def test_a_runner_named_inside_a_heredoc_is_not_a_run_of_it(tmp_path):
    """The other half of #200's *wrong in both directions*, in the same
    reading: the one call the family did charge to `test` was a `cat > …`
    heredoc whose body contains the word `pytest`.

    `load` flattens a call's whitespace, so a command that writes a document
    arrives at the classifier as one line with the whole document in it.
    Cutting at the heredoc operator answers it for every family at once and
    needs no list of the words a document might contain.

    The last two are the bound. A `<<` followed by a lowercase unquoted word
    is more often a quoted comparison than a heredoc, so it is left alone:
    charging a real run to `other` is the error this whole change exists to
    remove, and a lowercase heredoc delimiter classified the way it is today
    is the smaller of the two."""
    module = load_script()
    for command in (
        "cat > x.py <<'EOF' import pytest EOF",
        "cat > x.py <<EOF import pytest EOF",
        'cat > q.sql <<-"SQL" select 1 from pytest SQL',
        "python3 - <<'PY' subprocess.run(['pytest']) PY",
    ):
        assert module.family(command) == "other", command

    assert module.family("echo 'a << b' && pytest -q") == "test"
    assert module.family("cat > x <<eof pytest eof") == "test"


def test_the_report_names_the_command_the_table_could_not(tmp_path):
    """`other` leading the table means the rows above it describe a minority
    of the run, and nothing on the page said so — which is how #200 was
    published for four releases.

    Both arms, because a line that always prints is furniture: it appears when
    `other` leads and is absent when a named family does."""
    # Built so that two wrong answers are visible rather than merely
    # possible. `./bin/lint-docs` is the FIRST unnamed command, so an entry
    # taken in arrival order names it; `./bin/report` is the largest SINGLE
    # command, so an entry that does not group two pipes of one command names
    # that instead. Only grouping by `strip_pipe` and then taking the largest
    # answers `./bin/deploy --wait`.
    lines = []
    lines += call("a", 0, 5, "./bin/lint-docs")
    lines += call("b", 10, 70, "./bin/deploy --wait | tail -3")
    lines += call("c", 80, 140, "./bin/deploy --wait | head -1")
    lines += call("d", 150, 250, "./bin/report --long")
    # Larger than every unnamed command and charged to a family that HAS a
    # meaning, so an entry collected over the whole table rather than over
    # `other` alone names this and the case says so. `other` still leads by
    # total seconds, which is what the line is conditioned on.
    lines += call("e", 260, 460, "./bin/test --slow")
    lines += call("f", 470, 475, "pytest -q")
    unnamed_leads = tmp_path / "unnamed.jsonl"
    unnamed_leads.write_text("\n".join(lines) + "\n")

    out = run([str(unnamed_leads)]).stdout
    assert "`other` is the largest family and names nothing" in out, out
    named_line = next(
        line for line in out.splitlines() if "Slowest command charged there" in line
    )
    # Grouped by `strip_pipe`, so two runs of one command behind different
    # pipes are one entry and the pipe is not part of what a family would
    # have to learn. The `slowest` block below prints the pipe and is not
    # what this asserts on.
    assert named_line.endswith(": ./bin/deploy --wait"), named_line
    assert re.search(r"^  other\s+4 calls", out, re.M), out
    assert re.search(r"^  test\s+2 calls", out, re.M), out

    named = []
    named += call("d", 0, 120, "./bin/test -q")
    named += call("e", 130, 135, "./bin/deploy")
    test_leads = tmp_path / "named.jsonl"
    test_leads.write_text("\n".join(named) + "\n")

    other = run([str(test_leads)]).stdout
    assert "names nothing" not in other, other
    assert re.search(r"^  test\s+1 calls", other, re.M), other


# --- #145: the orchestrator's row is a spawn cycle, not the whole session ---
#
# Every segment of a chain has a transcript of its own, so its row is the
# whole file. The orchestrator's holds every spawn cycle of the run INSIDE it,
# so until `--spawns` the whole file was the only row it had — which is why
# #51's observation 1 has bands for three segment kinds and none for this one.
#
# A spawn cycle is not a segment. The cases below are `--spawns`', over bands
# inside one transcript; the per-segment cases at the end of this file are
# `--segments`', over the transcripts of the agents a run spawned.


def spawn(uid, start, end, subagent_type, description="a spawn"):
    """One `Agent` call and its result arriving.

    The `prompt` is present and ignored on purpose: `load` writes a call with
    no `command` field as a JSON dump of its whole input, so this is the
    shape that makes `command` a flattened prompt rather than a command line.
    Two cases below rest on that."""
    return [
        turn(
            start,
            {
                "type": "tool_use",
                "id": uid,
                "name": "Agent",
                "input": {
                    "subagent_type": subagent_type,
                    "description": description,
                    "prompt": "run pytest tests/ -q and report",
                },
            },
        ),
        turn(end, {"type": "tool_result", "tool_use_id": uid}),
    ]


@pytest.fixture
def orchestrator(tmp_path):
    """One run with two spawns, laid out so every row has something in it.

    head    two calls, one 5s gap
    cycle 1 the first spawn alone — 600s delegated
    cycle 2 two checks and a 1200s spawn; 7s and 9s gaps, 4s of command time
    tail    one call after the last spawn's result

    Cycle 2 is where the delegated-interval case can discriminate: it holds
    three calls, so it has real model gaps that a leaked 1200s would swamp
    and that dropping the spawn from the walk would shorten."""
    lines = []
    lines += call("a", 0, 10, "git status --short")
    lines += call("b", 15, 18, "cat seal/specs/x/plan.md")
    lines += spawn("A", 25, 625, "specseal:smith", "Build phase 1")
    lines += call("c", 640, 643, "git log --oneline -5")
    lines += call("d", 650, 651, "cat seal/specs/x/spec.md")
    lines += spawn("B", 660, 1860, "specseal:warden", "Review round 1")
    lines += call("e", 1870, 1880, "./bin/test tests/test_x.py -q")
    path = tmp_path / "orchestrator.jsonl"
    path.write_text("\n".join(lines) + "\n")
    return path


def spawns_of(path, args=()):
    return json.loads(run(["--json", *args, str(path)]).stdout)["spawns"]


def test_two_spawns_are_two_cycles_each_naming_what_it_spawned(orchestrator):
    """The acceptance row: two `Agent` calls, two cycles, each named."""
    spawns = spawns_of(orchestrator)
    assert spawns["found"] == 2, spawns
    cycles = [row for row in spawns["rows"] if row["kind"] == "cycle"]
    assert [row["cycle"] for row in cycles] == [1, 2], cycles
    assert [row["subagent_type"] for row in cycles] == [
        "specseal:smith",
        "specseal:warden",
    ], cycles
    assert [row["description"] for row in cycles] == [
        "Build phase 1",
        "Review round 1",
    ], cycles


def test_the_framing_and_the_closing_work_are_each_their_own_row(orchestrator):
    """`spec.md`: the work outside any cycle is reported rather than dropped.

    The head is the two framing calls before the first spawn went out and the
    tail is the one call after the last spawn's result — the closing work,
    which is the half a slice quietly drops when it stops at the last one."""
    rows = spawns_of(orchestrator)["rows"]
    kinds = [row["kind"] for row in rows]
    assert kinds == ["head", "cycle", "cycle", "tail"], kinds
    head, tail = rows[0], rows[-1]
    assert head["numbers"]["calls"] == 2, head
    assert head["numbers"]["command_s"] == 13, head  # 10 + 3
    assert tail["numbers"]["calls"] == 1, tail
    assert tail["numbers"]["command_s"] == 10, tail


def test_every_call_lands_in_exactly_one_row(orchestrator):
    """The property the whole table rests on, asserted as a sum.

    A slice that drops the run's closing work, or one that charges a call
    that outlived the cut its row ends at to both rows either side of it,
    both pass every other case here and fail this one."""
    data = json.loads(run(["--json", str(orchestrator)]).stdout)
    rows = data["spawns"]["rows"]
    counted = sum(row["numbers"]["calls"] for row in rows if row["numbers"])
    assert counted == data["calls"] == 7, (counted, data["calls"])


def test_a_row_with_no_call_keeps_its_place_in_the_partition(tmp_path):
    """A run whose first act is a spawn has an empty head, and that is a
    reading rather than a gap. Dropping the row would make the rows stop
    partitioning the run, which is the property above."""
    lines = spawn("A", 0, 60, "specseal:smith") + call("a", 70, 75, "git status")
    path = tmp_path / "no-head.jsonl"
    path.write_text("\n".join(lines) + "\n")
    rows = spawns_of(path)["rows"]
    assert [row["kind"] for row in rows] == ["head", "cycle", "tail"], rows
    assert rows[0]["numbers"] is None, rows[0]
    out = run(["--spawns", str(path)]).stdout
    assert "no call in this window" in out, out


def batch_spawn(uid, second, subagent_type, message_id="batch"):
    """One block of a message that spawned two agents at once.

    The two blocks carry different row stamps on purpose: a harness writes
    one message as one row per content block, and `load` takes each block's
    start from its own row. That is what lets the spawn sent FIRST be the one
    that reports LAST, which is the only shape where report order and send
    order disagree.

    The prompt is identical in both, and it names `pytest`: two spawns in one
    window carrying the same prompt are what a repeat group reads as a check
    re-run for a result already in hand."""
    return message(
        second,
        [
            {
                "type": "tool_use",
                "id": uid,
                "name": "Agent",
                "input": {
                    "subagent_type": subagent_type,
                    "prompt": "run pytest tests/ -q and report",
                },
            }
        ],
        message_id=message_id,
    )


def test_a_batch_of_two_spawns_is_bounded_by_when_each_report_arrived(tmp_path):
    """Two agents spawned in one turn, and the first one sent reports last.

    A cycle is bounded by its REPORT, so cycle 1 is the window ending at the
    first report — whichever spawn that was. Ordering the spawns by when they
    went out instead swaps both names, which is what the name assertion
    catches; nothing else in this module can tell the two orderings apart,
    because everywhere else a spawn reports in the order it was sent.

    Both calls sit in cycle 1, which is where the orchestrator actually made
    them, and cycle 2's window holds nothing at all."""
    lines = [
        batch_spawn("A", 0, "specseal:warden"),
        batch_spawn("B", 10, "specseal:scribe"),
        result(300, "B"),
        result(900, "A"),
    ]
    path = tmp_path / "batch.jsonl"
    path.write_text("\n".join(lines) + "\n")
    rows = spawns_of(path)["rows"]
    cycles = [row for row in rows if row["kind"] == "cycle"]
    assert [row["subagent_type"] for row in cycles] == [
        "specseal:scribe",
        "specseal:warden",
    ], cycles
    assert cycles[0]["numbers"]["calls"] == 2, cycles[0]
    assert cycles[1]["numbers"] is None, cycles[1]
    # Two delegated calls in ONE window, with one prompt between them. Left in
    # the repeat groups they read as 290 seconds of work re-run for a result
    # already produced, on a run where nothing was re-run.
    assert cycles[0]["numbers"]["repeat_same_work_s"] == 0, cycles[0]["numbers"]


def test_the_subagents_own_interval_is_not_charged_to_the_orchestrator(orchestrator):
    """The acceptance row, on cycle 2's fabricated 1200s spawn.

    Three implementations are separated here. Charging the delegated interval
    to the orchestrator gives a model time of 1266s or a command time of
    1204s. Dropping the spawn call out of the list handed to the analysis
    gives a model time of 7s, because the gap either side of it collapses
    into one. What is right is the third: the call stays in the walk that
    bounds the gaps and its duration leaves the command time."""
    cycles = [row for row in spawns_of(orchestrator)["rows"] if row["kind"] == "cycle"]
    second = cycles[1]["numbers"]
    assert second["delegated_s"] == 1200, second
    assert second["command_s"] == 4, second  # 3 + 1, the two checks
    assert second["model_s"] == 16, second  # 7s and 9s, neither swallowed
    assert second["calls"] == 3, second  # the spawn is still a call it made


def test_a_delegated_call_is_kept_out_of_the_slowest_and_the_repeats(orchestrator):
    """A prompt is not a check.

    A spawn's `command` is the JSON dump of its input, so the prompt arrives
    at the classifier as a command line — the fixture's prompt names `pytest`
    on purpose. Left in, two spawns carrying the same prompt read as a check
    re-run for a result already in hand, and a twenty-minute wait sits at the
    top of `slowest` telling the reader what they already knew."""
    cycles = [row for row in spawns_of(orchestrator)["rows"] if row["kind"] == "cycle"]
    second = cycles[1]["numbers"]
    assert second["repeat_same_work_s"] == 0, second
    assert all("subagent_type" not in row["command"] for row in second["slowest"]), (
        second["slowest"]
    )
    assert max(row["seconds"] for row in second["slowest"]) == 3, second["slowest"]


def test_a_cycle_is_divided_by_its_own_turns_and_not_the_runs(orchestrator):
    """`tools_per_turn` is the one number in the row with a denominator, and
    handing `analyse` the whole run's turn list is the way to get it wrong
    without getting anything else wrong.

    Cycle 2 sent three calls over three turns, so its ratio is 1.00. Divided
    by the run's seven turns it reads 0.43 — under every threshold the
    printed advisory has — and every other number in the row stays right,
    which is what would make it survive a reading."""
    cycles = [row for row in spawns_of(orchestrator)["rows"] if row["kind"] == "cycle"]
    second = cycles[1]["numbers"]
    assert second["call_turns"] == 3, second
    assert second["tools_per_turn"] == 1.0, second
    head = spawns_of(orchestrator)["rows"][0]["numbers"]
    assert head["call_turns"] == 2, head


def test_a_report_stamped_before_its_call_does_not_move_a_call_out_of_its_row(
    tmp_path,
):
    """The running maximum on the cuts, with the guarantee removed.

    A harness writing a result before the call it answers gives that spawn a
    negative duration, which is the one shape that can make a later cut
    earlier than the one before it. Cuts that go backwards are not a sorted
    list, so the search that assigns calls to windows answers from a binary
    search over an assumption that no longer holds — and the call at 55s,
    which belongs to the framing before any spawn, is charged to a cycle
    instead. The count still partitions, so only the assignment shows it.

    `share` and `report` already answer the non-positive span for the printed
    report. This is the same harness one reader over, and until this case the
    defence against it had never been tried."""
    lines = call("a", 55, 60, "git status --short")
    lines += [
        turn(
            100,
            {
                "type": "tool_use",
                "id": "A",
                "name": "Agent",
                "input": {"subagent_type": "specseal:smith", "prompt": "x"},
            },
        ),
        result(50, "A"),
    ]
    lines += spawn("B", 200, 300, "specseal:warden")
    path = tmp_path / "backwards.jsonl"
    path.write_text("\n".join(lines) + "\n")
    data = json.loads(run(["--json", str(path)]).stdout)
    rows = data["spawns"]["rows"]
    head = rows[0]["numbers"]
    assert head is not None and head["calls"] == 1, rows
    counted = sum(row["numbers"]["calls"] for row in rows if row["numbers"])
    assert counted == data["calls"] == 3, (counted, data["calls"])


def test_an_unparseable_turn_stamp_does_not_end_the_slicing(tmp_path):
    """The file's own rule — one odd row must not end the report — reaching
    the one reader that orders a turn against a time.

    `parse_time` already drops the unpairable CALL on such a row, and the
    turn is appended with the stamp as written. A turn with no time has no
    window to fall in, and asking which window it falls in compares `None`
    with a `datetime`: `TypeError`, out of the slice, with stdout empty —
    which is `count`'s failure one reader over and the shape `report`'s own
    docstrings say this file refuses. Dropped from the denominator instead,
    the direction every funnel here takes."""
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
                ],
                "usage": {"input_tokens": 500},
            },
        }
    )
    lines = [bad, *spawn("A", 10, 70, "specseal:smith"), *call("a", 80, 85, "ls")]
    path = tmp_path / "odd-turn.jsonl"
    path.write_text("\n".join(lines) + "\n")
    proc = run(["--json", str(path)])
    assert proc.returncode == 0, proc.stderr
    rows = json.loads(proc.stdout)["spawns"]["rows"]
    assert [row["kind"] for row in rows] == ["head", "cycle", "tail"], rows


def test_two_prompts_that_differ_after_a_pipe_are_not_a_check_re_run(tmp_path):
    """The repeat groups, with the shape a real orchestrator's prompts have.

    A spawn's `command` is the JSON dump of its whole input, and the repeat
    groups key on that string with everything after the first `|` cut off —
    plumbing, on a command line. A spawn prompt carries markdown tables, so
    two prompts that share a sentence and then differ inside a table collapse
    into one group, and the two spawns read as 290 seconds of work re-run for
    a result already in hand. Nothing was re-run: they are two different
    agents doing two different things."""
    lines = [
        message(
            0,
            [
                {
                    "type": "tool_use",
                    "id": "A",
                    "name": "Agent",
                    "input": {
                        "subagent_type": "specseal:warden",
                        "prompt": "run pytest, then review round 1 | file | verdict | 1",
                    },
                }
            ],
            message_id="pair",
        ),
        message(
            10,
            [
                {
                    "type": "tool_use",
                    "id": "B",
                    "name": "Agent",
                    "input": {
                        "subagent_type": "specseal:warden",
                        "prompt": "run pytest, then review round 1 | file | verdict | 2",
                    },
                }
            ],
            message_id="pair",
        ),
        result(300, "B"),
        result(900, "A"),
    ]
    path = tmp_path / "pipes.jsonl"
    path.write_text("\n".join(lines) + "\n")
    first = spawns_of(path)["rows"][1]["numbers"]
    assert first["calls"] == 2, first
    assert first["repeat_same_work_s"] == 0, first
    assert first["repeat_exact_s"] == 0, first


def test_a_cycle_carries_the_same_numbers_the_whole_run_does(orchestrator):
    """The acceptance row: the cycle row's keys ARE the whole run's keys.

    What it stops is a second meter hand-rolled for cycles. The labels are
    named rather than subtracted loosely, so adding one is a decision
    somebody makes here rather than a key that appears in a published
    reading.

    `segments` is the second such decision, taken when #350 landed: it is a
    reading of the transcripts BESIDE this one, so like `tokens` and `spawns`
    it is not one of `analyse`'s keys and does not belong in a cycle row's
    numbers. The case caught it on the commit that added it, which is the
    whole reason the exclusion is a literal list."""
    data = json.loads(run(["--json", str(orchestrator)]).stdout)
    whole = set(data) - {"tokens", "spawns", "segments"}
    for row in data["spawns"]["rows"]:
        assert set(row) == {"kind", "cycle", "subagent_type", "description", "numbers"}
        if row["numbers"]:
            assert set(row["numbers"]) == whole, (row["kind"], set(row["numbers"]))
    for key in (
        "span_s",
        "command_s",
        "model_s",
        "calls",
        "tools_per_turn",
        "gap_mean_s",
    ):
        assert key in whole, key


def test_the_plain_reading_is_the_number_it_was_before_the_mode_existed(orchestrator):
    """Every reading this repository has published was taken without the
    mode, and a value that quietly moves makes those incomparable with
    nothing on the page saying so — which is what #200 and #202 were.

    So the whole-run row still charges the delegated 1800s to command time,
    and its `delegated_s` is 0.0 because nothing was removed from it. The
    `Agent` row of the family table is where the delegated time stays
    visible in that reading."""
    data = json.loads(run(["--json", str(orchestrator)]).stdout)
    assert data["command_s"] == 1827, data["command_s"]  # 600 + 1200 included
    assert data["delegated_s"] == 0.0, data["delegated_s"]
    assert data["by_family"]["Agent"] == {"calls": 2, "seconds": 1800}, data[
        "by_family"
    ]


def test_a_run_with_no_spawn_names_the_count_rather_than_printing_a_table(transcript):
    """#200's failure shape, repaid the way #200 was.

    An empty cycle table reads as *this run spawned nothing* — and a run that
    DID spawn reads exactly the same way the moment a harness stops writing a
    spawn as an `Agent` call. So the count and the transcript path are printed
    and the table is not."""
    spawns = spawns_of(transcript)
    assert spawns == {"found": 0, "rows": []}, spawns
    out = run(["--spawns", str(transcript)]).stdout
    assert "0 spawns found" in out, out
    assert str(transcript) in out, out
    assert "t/turn" not in out and "cycle 1" not in out, out


def test_the_printed_table_names_each_cycle_and_what_it_spawned(orchestrator):
    """The rendered text, because that is what a person posts to the log.

    The partition line is printed even when it agrees: the rows resting on it
    is the reason a reader gets to see it hold rather than taking the file's
    word for it."""
    out = run(["--spawns", str(orchestrator)]).stdout
    assert "2 spawns found" in out, out
    assert "cycle 1  specseal:smith" in out, out
    assert "cycle 2  specseal:warden" in out, out
    assert re.search(r"^  head\s", out, re.M), out
    assert re.search(r"^  tail\s", out, re.M), out
    assert "7 calls over the rows above, of 7 calls in the transcript" in out, out
    assert "Build phase 1" in out and "Review round 1" in out, out
    # 20.0m delegated in cycle 2, and a dash where nothing was delegated.
    assert "20.0m" in out, out
    assert "—" in out, out


def test_a_delegated_column_of_seconds_says_which_of_two_things_it_is(
    orchestrator, tmp_path
):
    """Measured on this harness: an `Agent` call pairs in 1.5-3.7 seconds
    because its result is written when the spawn is ACCEPTED, and each
    subagent's transcript opens at that same stamp — 61 of 67 spawns across
    three runs, within one second. The agent then runs for a median of about
    1,000 seconds, in NO column of any row —
    `test_the_delegated_wait_is_in_no_column_of_any_row` is where that is
    pinned.

    So a `delegated` column of near-zeroes is not the reading it looks like,
    and a reader taking it for *nothing was delegated* is #200's failure
    shape one column over. Both arms, because a line that always prints is
    furniture: absent where a spawn's own interval really does cover its run,
    present where none of them can."""
    quick = spawn("A", 0, 3, "specseal:smith") + call("a", 20, 25, "git status")
    path = tmp_path / "quick.jsonl"
    path.write_text("\n".join(quick) + "\n")
    out = run(["--spawns", str(path)]).stdout
    assert "`delegated` never reaches a minute here — 3s at most" in out, out
    # Whitespace-collapsed, so the wording is what this pins rather than
    # which column the line happens to wrap at.
    assert "result is written when the spawn is ACCEPTED" in " ".join(out.split()), out

    covered = run(["--spawns", str(orchestrator)]).stdout
    assert "never reaches a minute" not in covered, covered


def test_the_delegated_wait_is_in_no_column_of_any_row(tmp_path):
    """Where the agent's wall clock actually goes, on the ACCEPTED harness.

    A window's `span_s` starts at its own first call and the model walk never
    counts the gap before that call, so the wait after a spawn's result is in
    no column of the row that follows it — under the 900s ceiling as much as
    above it. Nine pages said it was in the next row's `model` while it
    stayed under fifteen minutes; this is the case that would have caught
    that, and it is the number a reader of the band table needs."""
    lines = call("z", 0, 1, "git status --short")
    lines += spawn("A", 5, 7, "specseal:smith")
    # 300s of silence: the agent running, well under the 900s ceiling.
    lines += call("b", 307, 310, "git log --oneline -5")
    lines += call("c", 315, 317, "cat seal/specs/x/spec.md")
    path = tmp_path / "accepted.jsonl"
    path.write_text("\n".join(lines) + "\n")
    rows = spawns_of(path)["rows"]
    tail = rows[-1]["numbers"]
    assert tail["span_s"] == 10, tail  # 307 to 317, not 7 to 317
    assert tail["model_s"] == 5, tail  # 315-310 alone; the 300s is not here
    assert tail["command_s"] == 5, tail
    assert tail["delegated_s"] == 0.0, tail
    data = json.loads(run(["--json", str(path)]).stdout)
    outside = data["span_s"] - sum(
        row["numbers"]["span_s"] for row in rows if row["numbers"]
    )
    # 304 and not 300, which is why the printed line says MOSTLY the wait:
    # 300s of it is the wait after the spawn's result, and 4s is the head's
    # own last call to the cut. On the three measured runs that second part
    # is 0.6-0.8m of a 42-168m total, and here it is deliberately visible.
    assert outside == 304, outside
    out = " ".join(run(["--spawns", str(path)]).stdout.split())
    assert "in NONE of the columns above" in out, out
    assert "5.1m of the run's 5.3m is BETWEEN the rows" in out, out


def test_a_call_that_outlives_a_cut_prints_no_between_the_rows_figure(tmp_path):
    """The rows partition the CALLS, and the difference can go the other way.

    `in_windows` assigns a call by its start, which is what makes the calls
    partition and is not enough to make the spans partition: a call that
    outlives the cut its row ends at stays in the row it began in while the
    next row's calls have already started, so two rows' spans cover the same
    seconds and their sum can pass the run's own span. The line above then
    subtracts to a negative and printed `-16.5m of the run's 16.6m is
    BETWEEN the rows -- mostly the wait`: a negative interval, named as the
    delegated wait, in the one report this work item exists to make honest.

    A background `Bash` command is the ordinary way to reach it, which is
    what this transcript is."""
    lines = call("bg", 0, 1000, "npm run dev")
    lines += spawn("A", 5, 7, "specseal:smith")
    lines += call("b", 10, 12, "git status --short")
    lines += call("c", 990, 995, "git log --oneline -5")
    path = tmp_path / "outlives.jsonl"
    path.write_text("\n".join(lines) + "\n")
    rows = spawns_of(path)["rows"]
    spans = sum(row["numbers"]["span_s"] for row in rows if row["numbers"])
    data = json.loads(run(["--json", str(path)]).stdout)
    # The premise: the spans overlap, so they sum past the run's own span.
    assert spans > data["span_s"], (spans, data["span_s"])
    out = " ".join(run(["--spawns", str(path)]).stdout.split())
    # What the reader gets is the two SUMS, not their difference and not "the
    # rows overlap by 16.4m". `minutes` is one decimal, so a difference under
    # three seconds rounds to `by 0.0m` and reads as nothing having happened
    # beside a refusal; two figures the reader subtracts never round one away.
    #
    # And the difference is not the overlap. After #300 every row's interval
    # is a subinterval of the run's, so what the subtraction gives is the
    # gaps between the rows MINUS their overlap. Here the head row covers the
    # whole run, so there are no gaps and the 987s happens to equal the
    # overlap — which is why naming it the overlap would be a claim that
    # holds on this fixture and fails in general.
    assert "the rows' spans sum to 33.1m against the run's own 16.7m" in out, out
    assert "no between-the-rows figure" in out, out
    # The whole point: no negative is stated, and nothing is called the wait.
    assert "is BETWEEN the rows" not in out, out
    assert "-16.4m" not in out, out
    # The cut a row ends at, never a spawn's result: the head row's cut is
    # the first spawn's START.
    assert "outlived the cut its row ends at" in out, out
    assert "outlived a spawn's result" not in out, out


def test_the_printed_report_calls_a_cycle_row_a_band(orchestrator):
    """The row covers the wait, the verifying and the framing at once, and
    posting it as an attribution to one of those overstates it. The caveat is
    on the page rather than only in `plan.md`, because the page is what gets
    pasted into the log."""
    out = run(["--spawns", str(orchestrator)]).stdout
    assert "band over several acts and never an attribution" in out, out
    assert "spawn N-1's result arriving until spawn N's arrives" in out, out
    assert "the `Agent` call's own tool_use-to-tool_result span" in out, out


def test_a_spawn_that_names_no_subagent_type_still_gets_a_row(tmp_path):
    """A label this file cannot print is a label that was never there. The
    row is what the reading needs; the name on it is what makes it easy to
    read, and a blank label would leave a reader unable to tell one row from
    the next."""
    lines = [
        turn(0, {"type": "tool_use", "id": "A", "name": "Agent", "input": {}}),
        result(60, "A"),
    ]
    path = tmp_path / "unnamed.jsonl"
    path.write_text("\n".join(lines) + "\n")
    rows = spawns_of(path)["rows"]
    assert rows[1]["subagent_type"] == "", rows[1]
    assert "cycle 1  ?" in run(["--spawns", str(path)]).stdout


# --- #300: a window's span ends at the last call to END ---------------------


def test_a_span_covers_every_call_it_counts(tmp_path):
    """A window's span ends at the last call to END, not the last to BEGIN.

    `analyse` took the span as `calls[-1]["end"] - calls[0]["start"]` over a
    list `load` sorts by START, so a call that outlived every later call
    ended after the window it was counted in. A background command running
    0-1000s beside calls at 10-12s and 990-995s gave a span of 995s — five
    seconds shorter than the single call the window holds — and `command_s`
    counted that call in full, so the printed share was taken against a
    whole that did not contain its own part.

    The invariant this pins is the one that makes a span a span: no call it
    counted ends after it."""
    lines = call("bg", 0, 1000, "npm run dev")
    lines += call("b", 10, 12, "git status --short")
    lines += call("c", 990, 995, "git log --oneline -5")
    path = tmp_path / "outlives-the-span.jsonl"
    path.write_text("\n".join(lines) + "\n")
    data = json.loads(run(["--json", str(path)]).stdout)
    assert data["span_s"] == 1000, data["span_s"]
    # `slowest` is sorted by duration, so its head is the longest single
    # call. A span shorter than that is a window that does not contain one
    # of its own calls, which is what 995 against 1000 was.
    longest = data["slowest"][0]["seconds"]
    assert longest == 1000, data["slowest"][0]
    assert data["span_s"] >= longest, (data["span_s"], longest)
    out = run([str(path)]).stdout
    assert "span          16.7m" in out, out


def test_a_head_call_outlives_the_cut_without_outliving_a_spawns_result(tmp_path):
    """The head row's cut is the first spawn's START, not a spawn's result.

    `spawn_cuts` opens its cut list at the first spawn's start, so a head
    call can outlive its own row's cut and still end before that spawn's
    result arrives. The refusal must not name a cause this transcript does
    not carry, and it must not print a magnitude that rounds to nothing.

    The two sums are what removes the magnitude. `minutes` is one decimal, so
    a difference under three seconds printed `by 0.0m` as the grounds for
    withholding a figure: #145's round 3 measured that on a one-second
    overlap. The difference here is three seconds and printed `by 0.1m`; what
    this fixture pins is item 1, the cut rather than the result. Note that
    both sums round to 0.2m on it, so the reader's own subtraction gives 0.0m
    — the two figures stop the line ASSERTING a magnitude of zero, and they
    do not recover one."""
    lines = call("bg", 0, 8, "npm run dev")
    lines += spawn("A", 5, 9, "specseal:smith")
    lines += call("b", 6, 9, "pytest -q")
    lines += call("c", 9, 10, "git status --short")
    path = tmp_path / "head-cut.jsonl"
    path.write_text("\n".join(lines) + "\n")
    out = " ".join(run(["--spawns", str(path)]).stdout.split())
    assert "no between-the-rows figure" in out, out
    assert "outlived the cut its row ends at" in out, out
    # No call in this transcript ends after the spawn's result at 9s.
    assert "outlived a spawn's result" not in out, out
    # The two sums, so nothing rounds to `by 0.0m`.
    assert "sum to 0.2m against the run's own 0.2m" in out, out
    assert "by 0.0m" not in out, out


def test_an_exact_cover_reads_as_the_partition_agreeing(tmp_path):
    """`outside == 0` takes the between-the-rows line, not the refusal.

    The guard is `>= 0` and not `> 0`, and until now nothing pinned that
    choice: the rows summing to exactly the run's span is the partition
    agreeing, and the tally above it is printed when it agrees for the same
    reason. Under `> 0` this transcript would print a refusal — *no
    between-the-rows figure* — for a run whose rows cover it exactly, which
    is the one shape where the reader can see the arithmetic work.

    Head 0-8s, spawn 5-7s, call 10-12s: run span 12s against row spans of 8s,
    2s and 2s. The figure is 0.0m and it is a real reading."""
    lines = call("bg", 0, 8, "npm run dev")
    lines += spawn("A", 5, 7, "specseal:smith")
    lines += call("c", 10, 12, "git status --short")
    path = tmp_path / "exact-cover.jsonl"
    path.write_text("\n".join(lines) + "\n")
    rows = spawns_of(path)["rows"]
    spans = sum(row["numbers"]["span_s"] for row in rows if row["numbers"])
    data = json.loads(run(["--json", str(path)]).stdout)
    assert data["span_s"] == 12, data["span_s"]
    assert spans == 12, spans
    out = " ".join(run(["--spawns", str(path)]).stdout.split())
    assert "0.0m of the run's 0.2m is BETWEEN the rows — mostly the wait" in out, out
    assert "no between-the-rows figure" not in out, out


# --- the per-segment reading (#350) ----------------------------------------
#
# Every other mode in this file reads the transcript it was given. This one
# opens the transcripts BESIDE it — one row per spawned segment, read from
# that segment's own file — because the agent's own wall clock is in none of
# the columns any other row has. `--spawns` says so in prose and points at
# `<session-id>/subagents/`; this is the reader that goes there.


@pytest.fixture
def run_with_segments(tmp_path):
    """Two spawns and a transcript for each, opening at its own spawn's
    result stamp — the join's measured shape.

    smith  spawned at 25, accepted at 625; its file holds two calls, 625-641
    warden spawned at 660, accepted at 1860; its file holds one call

    The two segments hold different call counts on purpose: a reading taken
    from the PARENT's columns cannot tell them apart, and one taken from each
    segment's own file can."""
    main = []
    main += call("a", 0, 10, "git status --short")
    main += spawn("A", 25, 625, "specseal:smith", "Build phase 1")
    main += call("b", 640, 643, "git log --oneline -5")
    main += spawn("B", 660, 1860, "specseal:warden", "Review round 1")
    return write_run(
        tmp_path,
        main,
        {
            "agent-smith.jsonl": [
                *worked(625, "s1", "./bin/test tests/test_x.py -q", output=700),
                *worked(640, "s2", "ruff check .", cache_write=300),
            ],
            "agent-warden.jsonl": [
                *worked(1860, "w1", "cat docs/spec.md", cache_read=40)
            ],
        },
    )


def segments_of(path, args=()):
    proc = run(["--json", *args, str(path)])
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)["segments"]


def test_each_spawned_segment_is_named_by_the_spawn_it_opened_at(run_with_segments):
    """The acceptance row. Two segments, each named by the spawn whose result
    its transcript opens at, and each carrying numbers read from its own
    file rather than from the parent's columns."""
    segments = segments_of(run_with_segments)
    assert (segments["transcripts"], segments["spawns"]) == (2, 2), segments
    assert (segments["unnamed"], segments["unclaimed"]) == (0, 0), segments
    assert segments["tolerance_s"] == 1.0, segments
    assert [row["agent"] for row in segments["rows"]] == [
        "specseal:smith",
        "specseal:warden",
    ], segments["rows"]
    assert all(row["named"] for row in segments["rows"]), segments["rows"]
    # Read from each segment's own file: the smith's holds two calls over
    # 625-641, the warden's one. Neither number is in the parent transcript.
    smith, warden = segments["rows"]
    assert (smith["numbers"]["calls"], smith["numbers"]["span_s"]) == (2, 16), smith
    assert (warden["numbers"]["calls"], warden["numbers"]["span_s"]) == (1, 1), warden


def test_a_segments_tokens_are_its_own_file_and_not_the_runs(run_with_segments):
    """A column that looks summable and is not is #200's failure shape in a
    new place. Each row's tokens cover that segment's own transcript, so the
    run total — which sums the whole tree — is the larger number."""
    data = json.loads(run(["--json", str(run_with_segments)]).stdout)
    rows = data["segments"]["rows"]
    assert all("tokens" in row for row in rows), rows
    assert sum(row["tokens"]["transcripts"] for row in rows) == 2, rows
    assert data["tokens"]["transcripts"] == 3, data["tokens"]


def test_a_segment_opening_outside_the_tolerance_is_named_by_nobody(tmp_path):
    """Both directions, because a join that cannot fail names everything.

    The same fixture is built twice and only the segment's opening stamp
    moves: on the spawn's result it is named, three seconds off it is not."""

    def built(opening, name):
        main = call("a", 0, 10, "git status --short") + spawn(
            "A", 25, 625, "specseal:smith", "Build phase 1"
        )
        root = tmp_path / name
        root.mkdir()
        return write_run(root, main, {"agent-one.jsonl": worked(opening, "s1")})

    on_time = segments_of(built(625, "on-time"))
    assert on_time["unnamed"] == 0, on_time
    assert on_time["rows"][0]["agent"] == "specseal:smith", on_time["rows"]

    late = segments_of(built(628, "late"))
    assert late["unnamed"] == 1, late
    assert late["rows"][0]["named"] is False, late["rows"]
    assert late["rows"][0]["agent"] == "", late["rows"]
    # The spawn is still there and still counted — it simply claimed nothing.
    assert (late["spawns"], late["unclaimed"]) == (1, 1), late


def test_a_segment_the_parent_cannot_name_is_counted_rather_than_dropped(tmp_path):
    """A subagent of a subagent has no `Agent` call in the parent at all, so
    no stamp can name it. `spec.md`: it gets a row and the count says how
    many there were — a smaller answer rather than none, which is the
    direction `tool_name` and `count` already take."""
    main = call("a", 0, 10, "git status --short") + spawn(
        "A", 25, 625, "specseal:smith", "Build phase 1"
    )
    path = write_run(
        tmp_path,
        main,
        {
            "agent-smith.jsonl": worked(625, "s1"),
            "inner/agent-deep.jsonl": worked(700, "d1"),
        },
    )
    segments = segments_of(path)
    assert (segments["transcripts"], segments["spawns"]) == (2, 1), segments
    assert segments["unnamed"] == 1, segments
    named = [row for row in segments["rows"] if row["named"]]
    anonymous = [row for row in segments["rows"] if not row["named"]]
    assert [row["agent"] for row in named] == ["specseal:smith"], named
    assert len(anonymous) == 1, anonymous
    # Dropped rather than counted, the row would be invisible AND its numbers
    # would be missing from every reading of the run.
    assert anonymous[0]["numbers"]["calls"] == 1, anonymous


def test_one_spawn_is_claimed_by_one_segment(tmp_path):
    """Two transcripts opening at the same instant and one spawn between
    them. Without the claim, both rows carry the same agent's name and a
    reader adding the column counts one segment twice."""
    main = call("a", 0, 10, "git status --short") + spawn(
        "A", 25, 625, "specseal:smith", "Build phase 1"
    )
    path = write_run(
        tmp_path,
        main,
        {"agent-one.jsonl": worked(625, "s1"), "agent-two.jsonl": worked(625, "s2")},
    )
    segments = segments_of(path)
    assert segments["transcripts"] == 2, segments
    assert [row["named"] for row in segments["rows"]].count(True) == 1, segments["rows"]
    assert segments["unnamed"] == 1, segments
    assert segments["unclaimed"] == 0, segments


def test_a_run_with_no_segments_reads_rather_than_raising(transcript):
    """A segment measured on its own has no `subagents/` directory beside it.
    That is the ordinary case for this mode, not a failure — the reading is
    empty and the exit code is 0."""
    proc = run(["--json", str(transcript)])
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["segments"] == {
        "tolerance_s": 1.0,
        "transcripts": 0,
        "spawns": 0,
        "unnamed": 0,
        "unclaimed": 0,
        "rows": [],
    }


def segment_report(path, args=()):
    proc = run(["--segments", *args, str(path)])
    assert proc.returncode == 0, proc.stderr
    return proc.stdout


def test_the_printed_segment_table_names_each_agent_and_its_own_span(
    run_with_segments,
):
    """The rendered text, because that is what a person posts to the flow log.

    The two spans are the whole point of the mode: 16s and 1s, read from each
    segment's own file. Neither number is in any column of any `--spawns` row
    — there the same two agents read as 600s and 1200s of `delegated`, which
    is the interval until the spawn was ACCEPTED."""
    out = segment_report(run_with_segments)
    assert "specseal:smith" in out, out
    assert "specseal:warden" in out, out
    for header in ("span", "calls", "t/turn", "gap", "tokens"):
        assert header in out, (header, out)
    # 16s and 1s, printed by `minutes` at one decimal, and each segment's own
    # token spend: 700 output + 300 cache write for the smith, 40 cache read
    # for the warden. A column pinned only at zero is a column that could be
    # printing anything.
    assert re.search(
        r"^  specseal:smith\s+0\.3m\s+2\s+[\d.]+\s+\d+s\s+1,000$", out, re.M
    ), out
    assert re.search(
        r"^  specseal:warden\s+0\.0m\s+1\s+[\d.]+\s+\d+s\s+40$", out, re.M
    ), out


def test_the_segment_report_names_the_tolerance_it_joined_within(run_with_segments):
    """A join is a reading about a harness, not a fact this file asserts. The
    tolerance is on the page so a reader can tell a segment that matched
    nothing from a window that was too tight."""
    assert "1.0s" in segment_report(run_with_segments), segment_report(
        run_with_segments
    )


def test_the_segment_report_states_its_counts_even_when_they_agree(run_with_segments):
    """`report_spawns` prints its partition tally even when it agrees, and
    for the same reason: a join that silently matched nothing reads exactly
    like a run that spawned nothing. Two transcripts, two spawns, nothing
    unmatched on either side — and all four numbers print."""
    out = " ".join(segment_report(run_with_segments).split())
    assert "2 segment transcripts" in out, out
    assert "2 spawns" in out, out
    assert "0 segments named by nobody" in out, out
    assert "0 spawns that claimed none" in out, out


def test_a_segment_named_by_nobody_carries_its_transcript_instead(tmp_path):
    """A name it cannot print is a name that was never there — and a path is
    what the reader can actually open. The count says how many there were."""
    main = call("a", 0, 10, "git status --short") + spawn(
        "A", 25, 625, "specseal:smith", "Build phase 1"
    )
    path = write_run(
        tmp_path,
        main,
        {
            "agent-smith.jsonl": worked(625, "s1"),
            "inner/agent-deep.jsonl": worked(700, "d1"),
        },
    )
    out = segment_report(path)
    assert "1 segment named by nobody" in " ".join(out.split()), out
    assert "agent-deep.jsonl" in out, out
    assert "no `Agent` call" in out, out


def test_a_run_with_no_segment_names_the_count_rather_than_printing_a_table(
    transcript,
):
    """#200's failure shape, repaid the way `report_spawns` repays it: an
    empty table reads as a run that spawned nothing, and a run that DID spawn
    reads the same way the moment a harness moves the directory."""
    out = segment_report(transcript)
    assert "0 segments found" in out, out
    assert str(transcript) in out, out
    assert "t/turn" not in out, out
    assert "subagents/" in out, out


def test_the_token_column_says_it_is_not_the_runs_own(run_with_segments):
    """A column that looks summable and is not is #200's failure shape in a
    new place, so the page says which of the two it is rather than leaving a
    reader to add it to the run's own total."""
    out = " ".join(segment_report(run_with_segments).split())
    assert "own file" in out, out
    assert "counting the same tokens twice" in out, out


def test_the_reading_names_the_release_it_is_comparable_from(run_with_segments):
    """#200 and #202 both moved what a token and a family row MEAN, and both
    were fixed in 0.9.4. A reading that does not say so is a number a reader
    will compare with one taken before the repair."""
    out = " ".join(segment_report(run_with_segments).split())
    assert "0.9.4" in out, out


def test_the_mode_exits_zero_whether_it_finds_a_segment_or_not(
    run_with_segments, transcript
):
    """A measurement command that fails on a finding is a gate wearing a
    report's shape. Nothing reads this exit code today, and the orchestrator's
    own posting step would break on exactly the discovery it was posting."""
    for path in (run_with_segments, transcript):
        proc = run(["--segments", str(path)])
        assert proc.returncode == 0, (path, proc.returncode, proc.stderr)


def test_no_existing_printed_line_moves_when_the_mode_is_not_asked_for(
    run_with_segments,
):
    """`analyse`'s docstring sets the condition and #200 and #202 are what
    breaking it cost. The plain reading and `--spawns` are byte-identical to
    what they printed before this mode existed."""
    plain = run([str(run_with_segments)]).stdout
    assert "segment transcripts beside this one" not in plain, plain
    assert "named by nobody" not in plain, plain
    spawns = run(["--spawns", str(run_with_segments)]).stdout
    assert "named by nobody" not in spawns, spawns
    assert "2 spawns found" in spawns, spawns


# --- the resume slice: one row is one segment, not one file ----------------


def coordinator_message(second, text="Round 1's record is committed. Fix three."):
    """The row a harness writes when the coordinator sends a running agent a
    new message.

    `skills/verify/SKILL.md` prescribes the hand split *at the user lines
    where the coordinator sent it a new message*, and this is that line in
    the harness's own words. Measured over the 350 segment transcripts on one
    machine: 41 hold an idle gap at or above `analyse`'s 900-second ceiling,
    82 such gaps in all, and the row after a gap is a `type=user` row with
    `isMeta` set and a bare-string content far more often than anything
    else."""
    return json.dumps(
        {
            "timestamp": stamp_at(second),
            "type": "user",
            "isMeta": True,
            "message": {
                "role": "user",
                "content": (
                    "The coordinator sent a message while you were working: " + text
                ),
            },
        }
    )


@pytest.fixture
def resumed_segment(tmp_path):
    """One segment transcript holding two stretches of work separated by an
    idle gap and a coordinator message.

    slice 1  two calls, 625-641
    (idle)   8,359 seconds in which the agent issued nothing
    slice 2  two calls, 9010-9031

    The file's own span is 8,406 seconds. Read whole — which is what the mode
    does before this phase — one row covers the idle gap and reports a span
    over two hours for an agent that worked for 37 seconds."""
    main = call("a", 0, 10, "git status --short") + spawn(
        "A", 25, 625, "specseal:smith", "Build phase 1"
    )
    return write_run(
        tmp_path,
        main,
        {
            "agent-smith.jsonl": [
                *worked(625, "s1", "./bin/test tests/test_x.py -q", output=500),
                *worked(640, "s2", "ruff check ."),
                coordinator_message(9000),
                *worked(9010, "s3", "./bin/test tests/test_y.py -q"),
                *worked(9030, "s4", "git commit -m x"),
            ]
        },
    )


def test_a_resumed_segment_is_one_row_per_slice_not_one_per_file(resumed_segment):
    """The acceptance row, and the assertion the whole-file reading fails.

    Two slices, each with its own span, and their sum well under the file's
    own — because the idle gap between them belongs to neither. A mode that
    inherits the whole-file reading has not solved the problem it was built
    for."""
    segments = segments_of(resumed_segment)
    assert len(segments["rows"]) == 2, segments["rows"]
    spans = [row["numbers"]["span_s"] for row in segments["rows"]]
    assert spans == [16, 21], spans
    # The file's own span, which is what one row would have reported.
    assert sum(spans) < 8406, spans
    assert [row["slice"] for row in segments["rows"]] == [1, 2], segments["rows"]
    assert all(row["slices"] == 2 for row in segments["rows"]), segments["rows"]


def test_a_later_slice_inherits_the_name_from_the_files_first(resumed_segment):
    """Only the file's opening stamp can be joined to a spawn's result — a
    resume has no `Agent` call of its own anywhere. So the name is the file's
    and every slice carries it, rather than the second slice reading as a
    segment nobody spawned."""
    rows = segments_of(resumed_segment)["rows"]
    assert [row["agent"] for row in rows] == ["specseal:smith"] * 2, rows
    assert all(row["named"] for row in rows), rows
    assert segments_of(resumed_segment)["unnamed"] == 0, rows


def test_a_files_tokens_are_carried_by_its_first_slice_only(resumed_segment):
    """`token_totals` dedups a streamed message by its id and keeps the
    largest count each field reached (#202). Re-deriving that per slice would
    duplicate the rule, and a message whose rows straddled a slice boundary
    would be counted in both — #202's failure shape rebuilt in a new place.
    So the figure stays the file's, and every later slice prints a dash
    rather than a number a reader would add up."""
    rows = segments_of(resumed_segment)["rows"]
    assert rows[0]["tokens"]["output"] == 500, rows[0]
    assert rows[1]["tokens"] is None, rows[1]


def test_a_segment_with_no_marker_names_the_gap_it_could_not_split(tmp_path):
    """The floor `plan.md` names. Where the marker is absent and an idle gap
    above the 900-second ceiling is present, one row prints and the report
    says what that does to the span — rather than a span quietly covering a
    wait nobody can see in the columns."""
    main = call("a", 0, 10, "git status --short") + spawn(
        "A", 25, 625, "specseal:smith", "Build phase 1"
    )
    path = write_run(
        tmp_path,
        main,
        {
            "agent-smith.jsonl": [
                *worked(625, "s1", "./bin/test tests/test_x.py -q"),
                *worked(2000, "s2", "ruff check ."),
            ]
        },
    )
    rows = segments_of(path)["rows"]
    assert len(rows) == 1, rows
    assert rows[0]["slices"] == 1, rows[0]
    # 626 to 2000 — the gap `analyse`'s model walk already drops and no
    # column has ever named.
    assert rows[0]["idle_gap_s"] == 1374, rows[0]
    out = " ".join(segment_report(path).split())
    assert "no coordinator message" in out, out
    assert "22.9m" in out, out


def test_a_segment_that_was_not_resumed_reports_one_slice_and_no_gap(
    run_with_segments,
):
    """The negative half. A segment that ran straight through is one slice
    with nothing to name, and a report that says otherwise is reading a
    marker into a file that has none."""
    rows = segments_of(run_with_segments)["rows"]
    assert all(row["slices"] == 1 and row["slice"] == 1 for row in rows), rows
    assert all(row["idle_gap_s"] == 0 for row in rows), rows
    out = " ".join(segment_report(run_with_segments).split())
    assert "no coordinator message" not in out, out
    assert "resumed" not in out, out


def test_the_printed_table_says_which_slice_of_its_file_a_row_is(resumed_segment):
    """Two rows carrying one agent's name is unreadable without it — a reader
    cannot tell a resumed segment from two agents of the same kind."""
    out = segment_report(resumed_segment)
    assert "specseal:smith  1/2" in out, out
    assert "specseal:smith  2/2" in out, out
    assert "coordinator" in out, out


def test_the_two_count_sentences_agree_with_their_own_number(tmp_path, resumed_segment):
    """`1 segment was resumed` and `2 segments was resumed` — the second is
    what a first draft printed, and it is the failure
    `test_the_token_line_says_one_transcript_rather_than_1_transcripts`
    already polices one line over. Read off a real run before it was caught:
    `6 segments was resumed` and `2 rows above covers an idle gap`.

    Both sentences are built so no verb has to agree with a count, which is
    the repair rather than two branches that can drift apart. This pins each
    at one and at more than one."""
    one = " ".join(segment_report(resumed_segment).split())
    assert "come from 1 segment the coordinator restarted" in one, one

    # Two resumed files in one run, so the same sentence has to carry a
    # plural subject.
    main = (
        call("a", 0, 10, "git status --short")
        + spawn("A", 25, 625, "specseal:smith", "Build phase 1")
        + spawn("B", 700, 1200, "specseal:warden", "Review round 1")
    )
    both = write_run(
        tmp_path,
        main,
        {
            "agent-smith.jsonl": [
                *worked(625, "s1"),
                coordinator_message(9000),
                *worked(9010, "s2"),
            ],
            "agent-warden.jsonl": [
                *worked(1200, "w1"),
                coordinator_message(9500),
                *worked(9510, "w2"),
            ],
        },
    )
    many = " ".join(segment_report(both).split())
    assert "come from 2 segments the coordinator restarted" in many, many


def test_the_idle_gap_sentence_agrees_with_its_own_number(tmp_path):
    """The other half of the same class: `2 rows above covers`. The sentence
    puts the count in an object rather than a subject, so one row and two
    read the same way."""
    main = (
        call("a", 0, 10, "git status --short")
        + spawn("A", 25, 625, "specseal:smith", "Build phase 1")
        + spawn("B", 700, 1200, "specseal:warden", "Review round 1")
    )
    path = write_run(
        tmp_path,
        main,
        {
            "agent-smith.jsonl": [*worked(625, "s1"), *worked(2000, "s2")],
            "agent-warden.jsonl": [*worked(1200, "w1"), *worked(4000, "w2")],
        },
    )
    out = " ".join(segment_report(path).split())
    assert "sits inside 2 rows above" in out, out
