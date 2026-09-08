#!/usr/bin/env python3
"""session_cost — where a session's minutes actually went.

The `cost` row in the seal block asks for a number nobody can produce from
inside the session: how long the checks took, and how much of the wall clock
was spent waiting on the model between them. The transcript already holds
both. This reads it.

What it separates, because each has a different fix:

  command time   the tool actually running. Fix: make the command cheaper —
                 a parallel runner, a narrower scope.
  model time     the gap between one result arriving and the next call going
                 out. Fix: fewer calls — batch independent reads and runs.
  repeats        the same command, or the same command with a different pipe.
                 A second run to see the output differently returns nothing.
  tokens         what the run spent — output, cache write, cache read — summed
                 over this transcript AND every segment under its
                 `<session-id>/subagents/`. The row of a run's comparison
                 table nobody can produce by hand.

Usage:
  session_cost.py <transcript.jsonl>     one transcript
  session_cost.py --latest [DIR]         newest transcript for a repo (default: cwd)
  session_cost.py --json <transcript>    the same numbers, machine-readable

Transcripts live under ~/.claude/projects/<path-with-slashes-as-dashes>/,
with subagent runs in <session-id>/subagents/. `--latest` searches both.
"""

import argparse
import datetime as dt
import json
import math
import os
import re
import sys
from collections import defaultdict

HOME = os.path.expanduser("~")
PROJECTS = os.path.join(HOME, ".claude", "projects")

# Command families, in priority order — the first match wins, so a compound
# `ruff … && pytest …` is charged to the test run that dominates it.
FAMILIES = [
    ("test", re.compile(r"\b(pytest|jest|vitest|go test|cargo test|mvn test)\b")),
    ("lint/type", re.compile(r"\b(ruff|mypy|eslint|tsc|flake8|black|lint-imports)\b")),
    ("build", re.compile(r"\b(make|cargo build|npm run build|tsc -b|docker build)\b")),
    ("git", re.compile(r"^\s*(git|gh)\b")),
]

# The token fields `token_totals` sums, and the `usage` key each is read from.
FIELDS = (
    ("output", "output_tokens"),
    ("cache_write", "cache_creation_input_tokens"),
    ("cache_read", "cache_read_input_tokens"),
)


def parse_time(value):
    """None for a stamp that will not parse — one odd row must not end the
    report, the same way one unparseable line does not.

    **A stamp carrying no zone is read as UTC.** That is the assumption the
    line below already makes when it rewrites a trailing `Z`, stated here
    because it is now load-bearing. Every `datetime` in this file comes
    through here, and the readers do two things with one that a naive value
    beside an aware one forbids: they subtract it from another, in six
    places, and they order it against another, in `load`'s sort and
    `analyse`'s `max`. Either raises `TypeError` — the sort before anything
    has printed, on the report and on `--json` alike, which is `count`'s
    failure one axis over.

    Dropping the naive row instead, the way an unparseable one is dropped,
    would leave a transcript whose stamps are ALL naive reporting nothing,
    where today it reports numbers that are internally consistent. What the
    assumption costs is an absolute time read out of a harness writing local
    naive stamps. Nothing here prints one: every number this file produces
    is a difference between two stamps, and a difference is right whenever
    the two share a zone.

    **Where the two do NOT share a zone, the difference is wrong by that
    harness's offset — and it is now wrong at exit 0, where it used to
    raise.** That is the mixed transcript this normalisation was written
    for, so the cost is not a corner of the assumption but its main case: a
    naive local stamp read as UTC and subtracted from an aware one is off by
    the writer's offset from UTC, which at UTC+9 turns a ten-second span
    into minus nine hours. The trade is `plan.md`'s accepted alternative —
    a number that is wrong under a stated assumption beats a report that
    ends — and it is stated here because a silent wrong number is the one
    outcome nobody can see."""
    try:
        stamp = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
    return stamp if stamp.tzinfo is not None else stamp.replace(tzinfo=dt.UTC)


def family(command):
    for name, pattern in FAMILIES:
        if pattern.search(command):
            return name
    return "other"


def count(value):
    """A `usage` field as a number, or 0 when it is not one.

    `parse_time` above states this file's rule — one odd row must not end the
    report — and the two readers below broke it the same way, by using a value
    taken out of a transcript as an arithmetic operand or as a dict key with
    nothing checking what it was. A harness writing a token count as the
    string `"12"`, or as `null`, raised `TypeError` out of a report that had
    already read the rest of the file.

    `bool` is excluded on purpose: `True + 1` is 2, so a flag landing in a
    token column would be a wrong number rather than a missing one.

    **A non-finite value is excluded for the stronger reason: it ends the
    report.** `json.loads` accepts the bare tokens `NaN`, `Infinity` and
    `-Infinity` by default and all three are `float`, so the type check
    below passes them. What happens next depends on which field carried
    one, and only one of the two outcomes is the wrong-number failure
    `bool` is excluded for. `token_totals`' sums print `nan` and exit 0.
    But `token_thirds` rounds a mean, and `round()` raises on a non-finite
    float — `ValueError` for a `NaN`, `OverflowError` for an infinity —
    which ends the report with stdout EMPTY, on the report and on `--json`
    alike.

    Every usage field except `output_tokens` reaches that `round`, through
    the `input_tokens + cache_read_input_tokens` pair `load` builds. That
    exception is why this was first recorded as harmless: `output_tokens`
    was the field it was measured on, and it is the one field where the
    crash does not happen."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return 0
    try:
        finite = math.isfinite(value)
    except OverflowError:
        # An `int` too large to have a float of its own. `json.loads` builds
        # an arbitrary-precision `int` from any integer literal, and
        # `math.isfinite` converts to float before it answers — so ASKING the
        # question raises, inside the funnel that exists to keep such a value
        # out. Returning 0 answers it the way every other arm here does, and
        # it also keeps the value away from `token_thirds`' division, which
        # raises on the same int for the same reason one frame later.
        return 0
    return value if finite else 0


def message_key(message, row, number):
    """A key for one assistant message that is always hashable.

    A harness writing `message.id` as a list makes it unusable as a key, and
    both readers put it straight into a `set`. The row's own uuid is the next
    answer and the row's position is the floor — the same three-step fallback
    `load` already documented, with the type check the code assumed."""
    for candidate in (message.get("id"), row.get("uuid")):
        if isinstance(candidate, str) and candidate:
            return candidate
    return f"row-{number}"


def tool_name(value):
    """A `tool_use` block's `name` as a string, or `?` when it is not one.

    Two readers consume this one field and each dies on a different shape,
    which is why the check is here rather than at either of them. `analyse`
    keys `by_family` by it, so a list or an object raises `TypeError:
    unhashable type` before anything has printed — the token block included,
    which is the outcome `main`'s own note below says was fixed. `report`
    prints it under a `:<12` format spec, so a `null` hashes fine, passes
    `analyse`, and raises in the `by family` block instead, with the span and
    token lines already on screen.

    `?` is the floor `load` had already written for a block carrying no
    `name`, so a name this file cannot use reads as a name that was never
    there. The call is charged to `?` rather than to its family, which is the
    same direction `count` and `message_key` take: a smaller answer rather
    than none at all."""
    return value if isinstance(value, str) and value else "?"


def load(path):
    """Tool calls paired with their results, plus per-turn INPUT counts.

    A turn is one assistant MESSAGE that carries at least one tool_use,
    keyed by the message id — a harness writes one message as one row per
    content block, every row carrying the same id — with the row's uuid and
    then the row itself as fallbacks. Counting per tool_use block instead
    pinned tools-per-turn at ~1.00 structurally: five runs of two agent
    types measured exactly 1.00, and a day's conclusions were drawn from a
    meter that could not read anything else. A transcript with none of the
    three keys degrades to one turn per row — the old floor, never an
    inflated ratio."""
    pending, calls, turns = {}, [], []
    counted = set()
    with open(path, encoding="utf-8", errors="replace") as handle:
        for number, line in enumerate(handle):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if not isinstance(row, dict):
                continue
            stamp = row.get("timestamp")
            message = row.get("message")
            if not isinstance(message, dict):
                continue
            content = message.get("content")
            if not stamp or not isinstance(content, list):
                continue
            usage = message.get("usage")
            if not isinstance(usage, dict):
                usage = {}
            turn_key = message_key(message, row, number)
            carries_call = False
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    carries_call = True
                    call_id = block.get("id")
                    if not isinstance(call_id, str):
                        # Unpairable: `pending` is keyed by it, and a call
                        # with no result has no duration to charge anywhere.
                        continue
                    payload = block.get("input")
                    if not isinstance(payload, dict):
                        payload = {}
                    text = payload.get("command", "")
                    if not isinstance(text, str) or not text:
                        text = json.dumps(payload, ensure_ascii=False)
                    pending[call_id] = (
                        stamp,
                        tool_name(block.get("name")),
                        " ".join(text.split()),
                        turn_key,
                    )
                elif block.get("type") == "tool_result":
                    result_id = block.get("tool_use_id")
                    started = (
                        pending.pop(result_id, None)
                        if isinstance(result_id, str)
                        else None
                    )
                    if started:
                        began, tool, text, turn = started
                        start, end = parse_time(began), parse_time(stamp)
                        if start and end:
                            calls.append(
                                {
                                    "start": start,
                                    "end": end,
                                    "tool": tool,
                                    "command": text,
                                    "turn": turn,
                                }
                            )
            # Once per message, not once per block: a split message's later
            # rows repeat its usage, and a multi-call row would count its
            # tokens once per call.
            #
            # **Input-side fields only, and the first row is the right one for
            # them.** `input_tokens` and `cache_read_input_tokens` are fixed
            # when the request is made, so every row of a split message
            # repeats them unchanged -- measured identical first-row and
            # last-row over 13,425 messages, which is why #202's defect in
            # `token_totals` does not reach this reader.
            #
            # The tuple used to carry a third element, this message's
            # `output_tokens`, and NOTHING read it: `token_thirds` takes
            # `t[1]`, `analyse` takes `len(turns)`, and no other index appears
            # in this file. It is removed rather than repaired because
            # `output_tokens` is the one field that does grow across rows, so
            # what sat there was the first partial count -- a wrong number
            # waiting for its first reader, which is exactly how #202 was
            # written into `token_totals`. A consumer that needs it should
            # take the maximum across the message's rows, the way
            # `token_totals` now does.
            if carries_call and turn_key not in counted:
                counted.add(turn_key)
                turns.append(
                    (
                        stamp,
                        count(usage.get("input_tokens"))
                        + count(usage.get("cache_read_input_tokens")),
                    )
                )
    calls.sort(key=lambda c: c["start"])
    return calls, turns


def strip_pipe(command):
    """The command without its output plumbing.

    Two runs that differ only after the pipe produced the same work twice."""
    return re.split(r"\s*\|\s*(?!\|)", command)[0].strip()


def analyse(calls, turns):
    if not calls:
        return None
    span = (calls[-1]["end"] - calls[0]["start"]).total_seconds()
    command_time = sum((c["end"] - c["start"]).total_seconds() for c in calls)

    # Model time: the last result of one TURN to the first call of the next.
    # Two calls issued together are one turn — the wait between the first
    # result and the second call's row is the batch executing, not the model
    # thinking — and the gap after a batch runs from its last result, not
    # from whichever call sorts last by start.
    model_time, gaps = 0.0, []
    turn_key = turn_end = None
    for call in calls:
        if turn_key == call["turn"]:
            turn_end = max(turn_end, call["end"])
            continue
        if turn_key is not None:
            gap = (call["start"] - turn_end).total_seconds()
            if 0 <= gap < 900:
                model_time += gap
                gaps.append(gap)
        turn_key, turn_end = call["turn"], call["end"]

    by_family = defaultdict(lambda: [0, 0.0])
    for call in calls:
        key = family(call["command"]) if call["tool"] == "Bash" else call["tool"]
        by_family[key][0] += 1
        by_family[key][1] += (call["end"] - call["start"]).total_seconds()

    exact, stripped = defaultdict(list), defaultdict(list)
    for call in calls:
        seconds = (call["end"] - call["start"]).total_seconds()
        if family(call["command"]) not in ("test", "lint/type", "build"):
            continue
        exact[call["command"]].append(seconds)
        stripped[strip_pipe(call["command"])].append(seconds)

    def wasted(groups):
        # Every run after the first produced a result already in hand.
        return sum(sum(sorted(v)[:-1]) for v in groups.values() if len(v) > 1)

    return {
        "span_s": span,
        "command_s": command_time,
        "model_s": model_time,
        "calls": len(calls),
        # `call_turns` is `tools_per_turn`'s own denominator, returned so the
        # printed report can name it. It is NOT the token line's turn count:
        # that one is every assistant message carrying `usage`, over the whole
        # run, where this one is the messages of THIS transcript that sent a
        # call. Printing the two without saying so let a reader divide one
        # into the other — 1.08 tools per turn beside 659 turns and 211 calls.
        "call_turns": len(turns),
        "tools_per_turn": len(calls) / max(len(turns), 1),
        "gap_mean_s": (sum(gaps) / len(gaps)) if gaps else 0.0,
        "by_family": {
            k: {"calls": v[0], "seconds": v[1]} for k, v in by_family.items()
        },
        "slowest": sorted(
            (
                {
                    "seconds": (c["end"] - c["start"]).total_seconds(),
                    "command": c["command"][:110],
                }
                for c in calls
            ),
            key=lambda d: -d["seconds"],
        )[:8],
        "repeat_exact_s": wasted(exact),
        "repeat_same_work_s": wasted(stripped),
        "context_growth": token_thirds(turns),
    }


def token_thirds(turns):
    """The mean input count over each third of the run, as whole numbers.

    **`count` answers for each value that enters; this answers for the sum.**
    Two counts it accepted as finite can add to one that is not, and this is
    the one site in the file that converts a derived number to an `int`. Both
    routes were measured ending the report with stdout empty, on the report
    and on `--json` alike: two floats near the top of the range summing to an
    infinity, which `round` refuses; and two integers that each have a float
    where their sum does not, which the division refuses. A single third can
    also sum past the range on its own, so no per-turn guard reaches it.

    A mean the file cannot compute is charged 0, the direction every funnel
    here takes — never carried out as an infinity, which a reader would take
    for a measurement.

    **The rule this site is one member of, and where it is enforced (#192).**
    Every site in this module that converts a number to an `int` carries a
    guard: a finiteness test on the same operand in the enclosing
    conditional, or a `try` catching both `OverflowError` and `ValueError`.
    The class is not a list anybody maintains —
    `tests/test_a_derived_number_reaching_an_int_carries_a_guard.py`
    enumerates the sites from this file's own syntax tree and decides
    membership by invoking Python's integer-conversion protocol on an
    operand, so a conversion written under any name at all is a member. Add
    an unguarded one and that check names it with its unit.

    **Two shapes the rule does not reach, so nobody has to rediscover them.**
    A **subscript** bound converts through `__index__` and is excluded,
    because telling a derived bound from `len(inputs) // 3` needs provenance
    the walk does not have. And the true **division** two lines up is not a
    conversion at all: `sum(part) / len(part)` raises `OverflowError` on two
    integers that each have a float where their sum does not, which is why
    the `try` around it is doing work the finiteness test below cannot do.
    Both are `questions.md` Q1 and Q2 of work item
    `1788873620-two-in-range-values-make-one-that-is-not`."""
    # Strictly positive, not truthy. A truthiness test on a SIGNED number
    # drops a zero and KEEPS A NEGATIVE, and the negative is the half that
    # was wrong: six turns whose first three carry minus ten input tokens gave
    # a growth of [-10, 0, 10] and printed the context line off a baseline no
    # harness can mean. Zero goes on being dropped and that is not a
    # regression -- `count` answers 0 both for a field a harness never wrote
    # and for one it wrote as 0, so this file cannot tell a turn that spent
    # nothing from a turn nobody measured, and a mean is the wrong place to
    # guess. What changes is only that a count below zero leaves with it
    # (#193).
    inputs = [t[1] for t in turns if t[1] > 0]
    if len(inputs) < 3:
        return []
    third = len(inputs) // 3
    means = []
    for part in (inputs[:third], inputs[third : 2 * third], inputs[2 * third :]):
        if not part:
            continue
        try:
            mean = sum(part) / len(part)
        except OverflowError:
            # An integer sum with no float of its own. The question cannot be
            # asked, which is the same answer the funnels above give.
            mean = math.inf
        means.append(round(mean) if math.isfinite(mean) else 0)
    return means


def subagent_transcripts(path):
    """Every `*.jsonl` under the `<session-id>/subagents/` directory beside
    this transcript.

    A run's segments are written to a directory named after the main
    transcript's own basename, which is the layout `newest` already walks.
    The directory is WALKED rather than listed, so a harness that nests one
    segment's transcripts under another still has that spend counted.

    A missing directory is the ordinary case — a segment measured on its own
    has no subagents beside it — and it returns nothing rather than raising."""
    base = os.path.basename(path)
    session = base[: -len(".jsonl")] if base.endswith(".jsonl") else base
    root = os.path.join(os.path.dirname(os.path.abspath(path)), session, "subagents")
    if not os.path.isdir(root):
        return []
    found = []
    for directory, _dirs, files in os.walk(root):
        found += [os.path.join(directory, f) for f in files if f.endswith(".jsonl")]
    return sorted(found)


def token_totals(paths):
    """Summed `usage` over every transcript given, and how many were read.

    A TURN here is an assistant message carrying a `usage` block, whether or
    not it carries a tool call. That is NOT `tools_per_turn`'s denominator,
    which counts only messages carrying a tool_use: the per-segment bars in
    `docs/review-handoff-protocol.md` are calibrated against that ratio, and
    widening it would move a published threshold without saying so. Two
    counters, on purpose — a turn that only thought spent tokens the run paid
    for, and a turn that sent no call is not a turn the batching advisory can
    read anything into.

    A message's usage counts ONCE however many rows it is split across, at
    the LARGEST count each field reached: a harness writes one message as one
    row per content block and repeats the usage on each, which is the same
    trap `load` dedups against for `context_growth`. Per-row summing would
    double a run's headline number, and keeping the first row understated
    `output` by whatever had not been streamed yet — the block comment on the
    loop carries the measurement (#202).

    No way this degrades ENDS the report, and almost every one of them makes
    the totals smaller: a transcript that cannot be opened is skipped, a line
    that will not parse is dropped, a harness that stops writing one of the
    fields contributes zero, and a value that is not a number counts as none.
    One shape goes the other way — a split message whose rows carry neither a
    usable `message.id` nor a usable `uuid` is keyed by row position, so its
    usage counts once per row instead of once. Nothing in this file can tell
    that shape from a run that really sent that many messages.

    Which is why both counts are returned and printed. `transcripts` covers
    the files the walk OPENED, not the files that contributed — a segment that
    opened and yielded nothing is counted here and is invisible in the totals —
    so a line covering one file for a run that spawned six is visibly wrong to
    the person who spawned them, and `turns` is where a run's messages being
    counted twice would show. They are the only reader who can tell either."""
    totals = {
        "transcripts": 0,
        "turns": 0,
        "output": 0,
        "cache_write": 0,
        "cache_read": 0,
    }
    for path in paths:
        seen = {}
        try:
            with open(path, encoding="utf-8", errors="replace") as handle:
                for number, line in enumerate(handle):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        row = json.loads(line)
                    except ValueError:
                        continue
                    if not isinstance(row, dict):
                        continue
                    message = row.get("message")
                    if not isinstance(message, dict):
                        continue
                    usage = message.get("usage")
                    if not isinstance(usage, dict):
                        continue
                    key = message_key(message, row, number)
                    if key not in seen:
                        totals["turns"] += 1
                    # The LARGEST count each field reaches, not the first row
                    # carrying it. A streamed assistant message is written as
                    # several rows sharing one `message.id`, and its
                    # `output_tokens` GROWS across them -- the last row carries
                    # the completed count. Keeping the first summed however
                    # much had been emitted when that row was written, so a
                    # warden round that produced a full findings report read
                    # as 62 output tokens across 20 turns, three tokens a
                    # turn. Measured over the 180 transcripts on the machine
                    # that found it: 9,098 of 13,425 messages are split, and
                    # the reported total was 4,976,637 against a real
                    # 8,683,844.
                    #
                    # **The error is not a scale factor**, which is why no
                    # reader could correct for it: it is however much of each
                    # message had been written when its first row landed. Two
                    # segments the same day were out by 3.2x and 556x.
                    #
                    # Maximum rather than last-row-wins, though the two agree
                    # on every one of those 13,425 messages and 0 rows arrive
                    # out of order. `output_tokens` grows within a message, so
                    # the largest IS the completed count under any row order,
                    # where last-row-wins is only right under one the format
                    # does not promise. The cost is one dict per field instead
                    # of a set, and it buys a claim that does not rest on
                    # something unmeasured.
                    #
                    # The dedup itself was right and stays: a harness writes
                    # one message as one row per content block and repeats the
                    # usage on each, so per-row summing would multiply a run's
                    # headline number. Only which row wins changed.
                    seen[key] = {
                        field: max(
                            seen.get(key, {}).get(field, 0), count(usage.get(source))
                        )
                        for field, source in FIELDS
                    }
        except OSError:
            # A segment this run cannot open is a segment the line does not
            # cover; the transcript count is what makes the gap visible.
            continue
        for row_totals in seen.values():
            for field, _source in FIELDS:
                totals[field] += row_totals[field]
        totals["transcripts"] += 1
    return totals


def minutes(seconds):
    return f"{seconds / 60:.1f}m"


def plural(number, word):
    """`1 transcript`, `3 transcripts` — the line is read by a person.

    Named `plural` rather than `counted` because both `load` and
    `token_totals` hold a local set called `counted`, and a module function
    those two shadow is a name that reads wrong wherever it is used."""
    return f"{number:,} {word}" + ("" if number == 1 else "s")


def report_tokens(tokens):
    """The token block, printed either under the time lines or on its own.

    On its own when a transcript carries `usage` and no paired tool call: a
    segment that read and thought has no span to report and still spent what
    the run's token row is summed over. The block was inside `report`, which
    `main` reached only after `analyse` had returned something."""
    print(
        f"tokens        {plural(tokens['transcripts'], 'transcript')}, "
        f"{plural(tokens['turns'], 'turn')}"
    )
    print("              a turn is any assistant message, in every transcript counted")
    print(f"  output      {tokens['output']:>15,}")
    print(f"  cache write {tokens['cache_write']:>15,}")
    print(f"  cache read  {tokens['cache_read']:>15,}")


def share(part, whole):
    """`part` as a percentage of `whole`, or `—` when there is no share to take.

    A transcript whose only paired call begins and ends on one timestamp has
    a span of zero, and the three lines below divide by it. Printing the span
    line and then raising `ZeroDivisionError` is the shape `tool_name` was
    written to end: a report that worked and then stopped, with the token
    block and the family table lost behind the crash.

    The guard is on the whole span being POSITIVE, not on it being non-zero.
    Zero is the shape that was measured; a negative span — a harness writing
    a result before the call it answers — is the same undefined division with
    a sign on it, and a percentage of it would be a number nobody can read.
    Neither gets one invented. What the reader sees is the times themselves,
    which are what was actually measured."""
    return f"{part / whole * 100:.0f}%" if whole > 0 else "—"


def report(data):
    print(f"span          {minutes(data['span_s'])}   ({data['calls']} tool calls)")
    if data["span_s"] == 0:
        print(
            "              every call shares one timestamp, so there is no "
            "span to take a share of"
        )
    elif data["span_s"] < 0:
        # Two shapes, two sentences. `share` decides what a non-positive span
        # MEANS for a percentage, and one dash covers both; what it cannot do
        # is say which shape the reader is looking at, because it is handed
        # the numbers and not the transcript.
        print(
            "              the last call to begin ended before the first "
            "call began, so the span is negative and there is no share to "
            "take of it"
        )
    print(
        f"  command     {minutes(data['command_s'])}"
        f"   {share(data['command_s'], data['span_s'])}"
    )
    print(
        f"  model       {minutes(data['model_s'])}"
        f"   {share(data['model_s'], data['span_s'])}"
        f"   mean gap {data['gap_mean_s']:.1f}s"
    )
    idle = data["span_s"] - data["command_s"] - data["model_s"]
    # The span has to be positive before a tenth of it is a threshold. At a
    # negative span the threshold is negative too, so the comparison is true
    # and the line printed sixty-five minutes of idle beside a span of minus
    # thirty. At a span of zero `0 > 0` is false on its own, which is why
    # this conjunct was dropped once and why dropping it was wrong.
    if data["span_s"] > 0 and idle > data["span_s"] * 0.1:
        print(
            f"  idle        {minutes(idle)}"
            f"   {share(idle, data['span_s'])}"
            f"   waiting on a person, or on a gap this file cannot see"
        )

    print()
    report_tokens(data["tokens"])

    print("\nby family")
    for name, row in sorted(
        data["by_family"].items(), key=lambda kv: -kv[1]["seconds"]
    ):
        print(f"  {name:<12}{row['calls']:>4} calls  {minutes(row['seconds']):>7}")

    print("\nslowest")
    for row in data["slowest"]:
        print(f"  {row['seconds']:6.0f}s  {row['command'][:88]}")

    print("\nwhere the time could go instead")
    exact, same = data["repeat_exact_s"], data["repeat_same_work_s"]
    # Compared against zero rather than tested for truth. These are durations,
    # so a negative span makes them negative, and a negative number is truthy
    # — the report claimed an hour of work re-run for a result already in
    # hand on a transcript where nothing was re-run. The same value read as
    # falsey would have suppressed the `nothing obvious` line below.
    if same > 0:
        print(
            f"  repeats            {minutes(same)}  a check re-run for a result "
            f"already produced"
            + (f" ({minutes(exact)} of it identical)" if exact > 0 else "")
        )
    if data["tools_per_turn"] < 1.2:
        # Above 1 the one-at-a-time claim is one the number no longer
        # supports — and under per-block counting it never could rise to
        # contradict it, which is how the claim printed on five straight runs.
        shape = (
            "independent calls are going out one at a time"
            if data["tools_per_turn"] <= 1.0
            else "most turns send a single call"
        )
        print(
            f"  batching           {data['tools_per_turn']:.2f} tools per turn — "
            f"{data['calls']:,} calls over "
            f"{plural(data['call_turns'], 'turn')} that sent one, in this "
            f"transcript alone; {shape}, and each turn costs "
            f"{data['gap_mean_s']:.0f}s of model time on top of the command"
        )
    growth = data["context_growth"]
    # `growth[0]` is 0 either because the file could not compute that third --
    # `token_thirds` charges 0 for a mean outside the range -- or because the
    # third really was zero, which `token_thirds`' own input filter already
    # excludes. Neither is a baseline a multiple can be taken of, and without
    # this conjunct any positive last third clears a threshold of zero: a
    # transcript whose FIRST third overflowed printed `0 -> 10 input tokens;
    # later calls cost more`, where the input had collapsed by 307 orders of
    # magnitude. With the charged third LAST the line is suppressed instead,
    # so which direction the reader was told depended on which third
    # overflowed. Same shape as the positive-span conjunct in `share` (#193).
    if len(growth) == 3 and growth[0] > 0 and growth[2] > growth[0] * 1.5:
        print(
            f"  context            {growth[0]:,} → {growth[2]:,} input tokens; "
            f"later calls cost more than the same call would have earlier"
        )
    if same <= 0 and data["tools_per_turn"] >= 1.2:
        print("  nothing obvious — the command time is the command's own cost")


def newest(directory):
    # `~/.claude/projects` encodes a cwd by replacing every non-alphanumeric
    # character, not just the separator. Replacing `os.sep` alone is right on
    # POSIX by coincidence and wrong on Windows, where a drive letter keeps its
    # colon: `C:\GitHub\SpecSeal` became `C:-GitHub-SpecSeal` and the real
    # directory is `C--GitHub-SpecSeal`, so `session-cost --latest .` reported
    # "no transcript found" for a directory that is right there. Measured.
    # `hooks/worktree-guard.py` `project_slug` states the same rule; the two
    # trees do not import each other, so this names it rather than sharing it.
    slug = re.sub(r"[^A-Za-z0-9-]", "-", os.path.abspath(directory))
    root = os.path.join(PROJECTS, slug)
    if not os.path.isdir(root):
        return None
    found = []
    for base, _dirs, files in os.walk(root):
        found += [os.path.join(base, f) for f in files if f.endswith(".jsonl")]
    return max(found, key=os.path.getmtime) if found else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript", nargs="?")
    parser.add_argument("--latest", nargs="?", const=".", metavar="DIR")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = args.transcript
    if args.latest:
        path = newest(args.latest)
        if not path:
            sys.exit(f"no transcript found for {os.path.abspath(args.latest)}")
        if not args.json:
            print(f"# {path}\n")
    if not path:
        parser.error("give a transcript path or --latest")

    calls, turns = load(path)
    timings = analyse(calls, turns)
    # The whole run, not the transcript that was named: a token count covering
    # one segment is not comparable with one that covered a run, and #170 asks
    # for the row to be one command rather than one command per transcript.
    #
    # Summed BEFORE the no-tool-calls guard, not after it. A transcript with
    # `usage` and no paired tool call has no span to report and did spend
    # tokens, and exiting there printed neither — while a segment that read
    # and thought is exactly what the run-level table's per-kind token row is
    # summed over.
    tokens = token_totals([path, *subagent_transcripts(path)])
    if timings is None and not tokens["turns"]:
        sys.exit("no tool calls in this transcript")
    data = {**(timings or {}), "tokens": tokens}
    if args.json:
        print(json.dumps(data, indent=2))
    elif timings:
        report(data)
    else:
        print(
            "no paired tool call in this transcript, so there is no time to "
            "report — what it spent is below\n"
        )
        report_tokens(tokens)
    return 0


if __name__ == "__main__":
    # A console that cannot encode what this prints kills it with stdout
    # empty, which is how a hook says "nothing to see here". `hooks/console.py`
    # owns the reasoning and the three decisions behind these lines.
    for _name, _errors in (
        ("stdin", "replace"),
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main())
