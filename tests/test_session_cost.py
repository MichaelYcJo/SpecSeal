"""session_cost: the numbers the seal's `cost` row asks for.

The report exists because nobody can produce these from inside a session. The
fixture below is a hand-built transcript with known answers, so a change to
the parser that quietly stops finding repeats or tool calls fails here.
"""

import datetime as dt
import importlib.util
import json
import os
import re
import subprocess
import sys

import pytest

SCRIPT = os.path.join(
    os.path.dirname(__file__), "..", "skills", "verify", "scripts", "session_cost.py"
)


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
# Round 1's findings 1 and 2. `parse_time`'s docstring states the file's rule
# for the whole file — "one odd row must not end the report" — and two readers
# broke it in the same way: a value taken out of a transcript was used as a
# dict key or an arithmetic operand without anything checking what it was.
# Both readers are pinned here, because a raise in either kills the same
# report.


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
