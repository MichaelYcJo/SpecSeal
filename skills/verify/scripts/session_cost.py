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
  session_cost.py --spawns <transcript>  one row per spawn cycle, not one per run
  session_cost.py --segments <transcript>  one row per segment this run spawned
  session_cost.py --json <transcript>    the same numbers, machine-readable

Transcripts live under ~/.claude/projects/<path-with-slashes-as-dashes>/,
with subagent runs in <session-id>/subagents/. `--latest` searches both.

**Why `--spawns` exists, in one sentence.** Every segment of a chain has a
transcript of its own, so its row is the whole file; the orchestrator's holds
every spawn cycle of the run inside it, so the whole file was the only row it
ever had — three segment kinds have bands and this one had none (#145).

**Why `--segments` exists, in one sentence.** An agent's own wall clock is in
no column of any row `--spawns` prints: on this harness the `Agent` result is
written when the spawn is ACCEPTED, so `delegated` reads seconds while the
agent runs for a median of about 1,000 (#350). That number is in the segment's
own transcript, and this is the reader that opens it.

**A spawn cycle is not a segment**, which is the one thing to keep straight
between the two modes. `--spawns` slices THIS transcript into bands over the
orchestrator's own minutes; `--segments` opens the OTHER transcripts, one row
per agent this run spawned. `skills/verify/SKILL.md` §*Measure the segment*
owns that distinction and `tests/test_one_word_one_meaning.py` holds it.
"""

import argparse
import bisect
import datetime as dt
import itertools
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
#
# **A repository's own runner is named by PATH, and that is what the first
# five names missed (#200).** A project that ships `bin/test` has said what
# its test command is, in the filesystem, and every call of it was charged to
# `other` — the row nobody reads because it is the row everything falls into.
# Measured over the 180 transcripts on the machine that found it: of the
# `./bin/test` calls, 266 landed in `other`, and the ones that did NOT landed
# in four different families depending on what else shared the command line.
# The one call the `test` family did charge was a heredoc whose body contains
# the word `pytest`.
#
# What is added here is only the shapes that mean the same thing in any
# repository: a script named `test` invoked by path, and the runners a
# language's own convention names. What CANNOT be added is a runner with a
# name nobody outside that repository can guess — `bin/check`, `./run-suite` —
# and that residual is why `report` prints the slowest command it could not
# name rather than leaving the reader a `test` row that is quietly empty.
FAMILIES = [
    (
        "test",
        re.compile(
            r"\b(pytest|jest|vitest|go test|cargo test|mvn test|tox|nox|rspec"
            r"|phpunit|dotnet test|bun test|deno test)\b"
            r"|(^|[\s./\\])(bin|scripts)[/\\]test\b"
            r"|\btest\.(sh|bash|bat|cmd|ps1)\b"
            r"|(^|[\s./\\])(make|just|task|npm|yarn|pnpm|gradlew?)\s+(run\s+)?test\b"
        ),
    ),
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


# A heredoc body is data the command was handed, not a command that ran. The
# delimiter has to be QUOTED or written in the upper case every convention
# uses -- `<<EOF`, `<<'PY'`, `<<-"SQL"` -- because a bare `<<` followed by a
# lowercase word is more often a quoted comparison than a heredoc, and cutting
# there would charge a real run to `other`, which is the error this whole
# change exists to remove. A heredoc with a lowercase unquoted delimiter is
# left classified the way it is today: a smaller error than the one the
# looser pattern would introduce, and the direction every funnel in this file
# takes.
HEREDOC = re.compile(r"""<<-?\s*(?:'[^']*'|"[^"]*"|[A-Z_][A-Z0-9_]*)""")


def family(command):
    """The family of the command that RAN, with any heredoc body removed.

    `load` flattens a call's whitespace, so a `cat > file <<'EOF' … EOF`
    writing a document arrives here as one line with the whole document in it,
    and any runner named inside gets the call. That is the second half of
    #200's *wrong in both directions*: the family missed every real
    `./bin/test` run and charged one file write to `test`, in the same
    reading. Cutting at the heredoc operator answers it for every family at
    once and needs no list of the words a document might contain."""
    opener = HEREDOC.search(command)
    if opener:
        command = command[: opener.start()]
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


# The tools whose duration is somebody else's work, where the harness charges
# that work to the call at all.
#
# **On the harness measured here it does not, and that is worth knowing before
# reading `delegated_s`.** An `Agent` call's own tool_use-to-tool_result
# interval is 1.5-3.7 seconds across 67 spawns of three runs, and each
# subagent's transcript OPENS at its spawn's result stamp -- 61 of those 67
# within one second, the six misses being subagents of subagents, which have
# no call in the main transcript at all. So the result is written when the
# spawn is ACCEPTED, the agent then runs for a median of about 1,000 seconds,
# and that interval is in NO column of any row. It is the gap between the
# cycle that spawned and the next row's first call: `analyse` starts a
# window's `span_s` at that first call (`span` below) and never counts the gap
# before it (the model walk's `turn_key is not None` guard), whether the wait
# is above the 900-second ceiling or below it. Measured over the same three
# runs, the interval between one row's last call and the next row's first is
# 12-31% of each run's wall clock, and the wait is 98% of that.
#
# The exclusion below is therefore right and nearly free here, and it is the
# whole answer on a harness that writes the result at completion. What it is
# NOT is the removal of the double count #145 set out to remove -- that one is
# in no column of any row, between two of them, and moving it into
# `delegated_s` is a decision about what that column measures rather than a
# defect in what it measures now. `questions.md` Q4.
#
# **A name, and `plan.md` chose disclosure over a second signal.** A spawn's
# `input` also carries `subagent_type`, so a harness renaming the tool could
# be survived by matching on that field instead. `plan.md`'s failure scenario
# answers the rename the other way on purpose: the mode names the count it
# found and refuses to print a table when it found none, rather than
# defending a shape nobody has seen change. A defence against a rename that
# has not happened is a defence nothing can test; a count of zero beside the
# transcript path is a reading somebody can act on.
DELEGATING = ("Agent",)

# How far a segment transcript's OPENING stamp may sit from a spawn's result
# stamp and still be read as that spawn's segment.
#
# The measurement the block above carries was taken over 67 spawns of three
# runs of the 0.9.x line, 61 of them within one second. Re-measured for this
# mode over the 43 runs on the machine that built it, with the one-to-one
# rule `join_segments` actually uses: 296 of 349 segment transcripts are
# named at 1.0s and 301 at 2.0s. So widening to two seconds buys five
# segments of 349 and doubles the window a batch of two spawns can match the
# wrong one in, and the remainder it does not buy is structural -- those 43
# runs hold 349 segment transcripts against 305 `Agent` calls, so 44 of them
# have no call in the parent to be named by at ANY tolerance.
#
# Which is why the report prints this number and the count on each side that
# went unmatched, rather than treating the join as a fact. A tolerance is a
# reading about a harness, and the harness is not this file's.
JOIN_TOLERANCE_S = 1.0


def spawn_labels(payload):
    """What a delegating call says it spawned, as strings.

    Read at the block rather than out of the call's `command`. `load` writes
    a call carrying no `command` field as a JSON dump of its whole input and
    then collapses the result's whitespace, so recovering `subagent_type`
    from that string means re-parsing JSON whose string values have already
    been rewritten. Here the two fields are still the values the harness
    wrote.

    A field that is not a non-empty string reads as absent, the floor
    `tool_name` takes one function down: a label this file cannot print is a
    label that was never there, and the cycle still gets its row. The row is
    what the reading needs; the name on it is what makes the row easy to
    read."""
    labels = {}
    for field in ("subagent_type", "description"):
        value = payload.get(field)
        if isinstance(value, str) and value:
            labels[field] = value
    return labels


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
                        spawn_labels(payload),
                    )
                elif block.get("type") == "tool_result":
                    result_id = block.get("tool_use_id")
                    started = (
                        pending.pop(result_id, None)
                        if isinstance(result_id, str)
                        else None
                    )
                    if started:
                        began, tool, text, turn, spawn = started
                        start, end = parse_time(began), parse_time(stamp)
                        if start and end:
                            calls.append(
                                {
                                    "start": start,
                                    "end": end,
                                    "tool": tool,
                                    "command": text,
                                    "turn": turn,
                                    # Empty for every call that delegated
                                    # nothing, which is almost all of them.
                                    # `spawn_cycles` reads it only for the
                                    # calls `DELEGATING` names.
                                    "spawn": spawn,
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


def analyse(calls, turns, delegated=()):
    """The numbers for one call list. `delegated` names the tools whose own
    duration is somebody else's work.

    **Called without `delegated`, every number below is what it was before
    `--spawns` existed**, and that is deliberate rather than incidental.
    Changing what the plain reading prints would make every reading this
    repository has already published incomparable with the next one, with
    nothing on the page saying so — which is what #200 and #202 were, and
    what `plan.md`'s *no existing output changes shape* is protecting.

    **`span_s` is the one exception and it is a measured one, not a licence.**
    Its rule moved at #300, from the end of the last call to BEGIN to the end
    of the last call to END, because the old one could return a window
    shorter than a single call inside it. The comment at the arithmetic
    carries the measurement that says no published figure moves;
    `skills/verify/SKILL.md` carries it where a person taking a reading meets
    it. Every other number here is untouched, `command_s` and `model_s`
    included.

    So `delegated_s` is 0.0 for the whole-run call, and it means exactly
    *how much of this window's command time was removed because it ran
    somewhere else* — nothing was, so it is zero. It is NOT a claim that the
    run delegated nothing: the `Agent` row of `by_family` is where that
    question is answered, and a cycle row is where the removal happens.

    What a delegated call goes on counting toward, because the orchestrator
    really did make it: `calls`, `tools_per_turn`, the turn walk that bounds
    the model gaps, and its own `by_family` row. What it is kept out of:
    `command_s`, `slowest`, and the repeat groups. A prompt is not a check,
    so a prompt re-sent is not a check re-run, and a twenty-minute wait at
    the top of `slowest` tells a reader something they already know."""
    if not calls:
        return None
    # The last call to END, and not the last to BEGIN. `load` sorts by start,
    # so `calls[-1]` is whichever call went out last, and a long-lived one --
    # a background command, a suite spanning the whole window -- ends after
    # it. Reading that element's end gave a window shorter than a single call
    # the window holds: 995s against a `Bash` call of 1000s, while
    # `command_s` counted that call in full, so the share was taken against a
    # whole that did not contain its own part.
    #
    # This is the one number in this function whose RULE changed after the
    # readings above it were published (#300). Measured before it was changed:
    # over the 169 transcripts on the machine it was measured on, one span
    # moves, by 0.006s, and no printed figure moves at all -- `minutes` is one
    # decimal and `share` is whole percent. So nothing already posted needs a
    # marking line, and a transcript with a genuinely long-lived call is where
    # the two rules would part.
    span = (max(c["end"] for c in calls) - calls[0]["start"]).total_seconds()
    command_time = delegated_time = 0.0
    for call in calls:
        seconds = (call["end"] - call["start"]).total_seconds()
        if call["tool"] in delegated:
            delegated_time += seconds
        else:
            command_time += seconds

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
    unnamed = defaultdict(float)
    for call in calls:
        key = family(call["command"]) if call["tool"] == "Bash" else call["tool"]
        seconds = (call["end"] - call["start"]).total_seconds()
        by_family[key][0] += 1
        by_family[key][1] += seconds
        if key == "other":
            unnamed[strip_pipe(call["command"])] += seconds

    exact, stripped = defaultdict(list), defaultdict(list)
    for call in calls:
        seconds = (call["end"] - call["start"]).total_seconds()
        if call["tool"] in delegated:
            # A spawn's `command` is the JSON dump of its whole input, prompt
            # included, so `family` reads a prompt as a command line -- a
            # prompt naming `pytest` outside a heredoc classifies as a test
            # run, and two spawns carrying the same prompt would then read as
            # a check re-run for a result already in hand. Kept out here
            # rather than everywhere, because the whole-run reading passes no
            # `delegated` and must go on printing what it printed before.
            continue
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
                if c["tool"] not in delegated
            ),
            key=lambda d: -d["seconds"],
        )[:8],
        # The command time this window did not spend: a call whose work ran
        # in another transcript, removed from `command_s` above and reported
        # here instead. Zero whenever `delegated` is empty, which is every
        # whole-run reading -- see the docstring for why that is not the
        # claim that nothing was delegated.
        "delegated_s": delegated_time,
        "repeat_exact_s": wasted(exact),
        "repeat_same_work_s": wasted(stripped),
        # The command that cost the most of what the table could not name.
        # `other` is the family with no meaning of its own, so a runner these
        # patterns do not know disappears into it and the `test` row goes on
        # reading as *no test run happened* — which is what #200 was, silently,
        # in every reading this repository published. Naming the command turns
        # that into something the next reader can act on: it is the exact
        # string a family would have to learn. Grouped by `strip_pipe` so the
        # same work behind two different pipes is one entry, the way the
        # repeats lines already count it.
        "unnamed": (max(unnamed.items(), key=lambda kv: kv[1])[0] if unnamed else ""),
        "context_growth": token_thirds(turns),
    }


def spawn_cuts(calls):
    """The spawns in result order, and the times the run is cut at.

    Ordered by when each spawn call's RESULT arrived rather than by when the
    call went out, because that is what bounds a cycle. Two agents spawned in
    one batch have their results land at different times, and the second
    one's cycle is the window that ends at its result — its own call sits
    inside the first one's cycle, which is where the orchestrator actually
    made it.

    A result arriving is a transcript fact; what it MEANS is the harness's.
    `DELEGATING` above carries the measurement: on the harness measured
    there, it means the spawn was accepted rather than the report having
    arrived.

    The cuts are run through a running maximum so they never go backwards. A
    harness writing a result before the call it answers gives that call a
    negative duration, and non-monotone cuts would overlap windows whose
    whole job is to partition. `share`'s non-positive span is the same shape
    one reader over, answered the same way: the numbers stay internally
    consistent instead of the slice inverting."""
    found = sorted(
        (c for c in calls if c["tool"] in DELEGATING),
        key=lambda c: (c["end"], c["start"]),
    )
    if not found:
        return [], []
    cuts = [min(c["start"] for c in found)]
    for spawn in found:
        cuts.append(max(cuts[-1], spawn["end"]))
    return found, cuts


def in_windows(cuts, items, when):
    """`items` in the `len(cuts) + 1` windows those cuts define.

    Assignment is by ONE instant per item — a call's start, a turn's stamp —
    which is what makes the windows a partition: every item has exactly one
    of those and every instant falls in exactly one window. Assigning a call
    by overlap would put one that outlived the cut its row ends at in two
    rows, and a sum over the rows would then come out larger than the run."""
    windows = [[] for _ in range(len(cuts) + 1)]
    for item in items:
        windows[bisect.bisect_right(cuts, when(item))].append(item)
    return windows


def spawn_cycles(calls, turns):
    """The run sliced at its spawn cycles, every call in exactly one slice.

    A spawn is an `Agent` `tool_use` block. Cycle *N* ends when spawn *N*'s
    result arrives and begins where the row before it ended, so the slices
    are, in order:

      head      before the first spawn went out — the run's framing
      cycle 1   the first spawn going out, until its result arrives
      cycle N   spawn N-1's result arriving, until spawn N's arrives
      tail      after the last spawn's result — the run's closing work

    **Cycle 1 is not the same shape as the others and a reader has to know
    it.** Cycles 2..N each carry the window in which the orchestrator
    verified the previous report and framed the next prompt. Cycle 1 carries
    neither: the run's own start is a boundary a script can take, and the
    head row is where that work goes. The head printed beside cycle 1 is what
    keeps the two readable together.

    **What no boundary here can separate**, said here rather than found
    later: between spawn N-1's result arriving and spawn N going out, the
    orchestrator waits on that agent, verifies the report it eventually
    hands over, and frames the next prompt — and no transcript field marks
    where any of those ends. The whole window is charged to cycle N. That is
    why a cycle row is read as a band and not as an attribution, and it is
    the one thing the per-act split (#145's second candidate) would answer.

    **The waiting is NOT in that band on the harness measured in
    `DELEGATING`, and a reader has to know where it went.** A subagent runs
    for a median of about 1,000 seconds there while the orchestrator issues
    nothing, and that whole interval falls between two rows: it precedes the
    next row's first call, where `span_s` begins and where the model walk
    starts counting. So a cycle's `model_s` is the orchestrator's own gaps
    and not the wait, the rows partition the run's CALLS rather than its
    time, and 12-31% of a measured run's wall clock is in no row at all.

    The turns are sliced by the same cuts, because `analyse` reads that list
    for its own denominator: handed the whole run's, a window's calls would
    be divided by the run's turns. A turn's stamp is the timestamp of the
    message that sent its calls, so it lands where its calls do."""
    found, cuts = spawn_cuts(calls)
    if not found:
        return []
    call_windows = in_windows(cuts, calls, lambda c: c["start"])
    stamped = [(parse_time(stamp), value) for stamp, value in turns]
    turn_windows = in_windows(
        cuts,
        # A stamp that will not parse has no window to fall in. It is dropped
        # from the denominator rather than charged to a guess, which is the
        # direction `parse_time` already takes for a call.
        [t for t in stamped if t[0] is not None],
        lambda t: t[0],
    )
    rows = []
    for index in range(len(cuts) + 1):
        if index == 0:
            labels = {
                "kind": "head",
                "cycle": 0,
                "subagent_type": "",
                "description": "",
            }
        elif index == len(cuts):
            labels = {
                "kind": "tail",
                "cycle": len(found) + 1,
                "subagent_type": "",
                "description": "",
            }
        else:
            spawn = found[index - 1].get("spawn") or {}
            labels = {
                "kind": "cycle",
                "cycle": index,
                "subagent_type": spawn.get("subagent_type", ""),
                "description": spawn.get("description", ""),
            }
        rows.append(
            {**labels, "window": call_windows[index], "turns": turn_windows[index]}
        )
    return rows


def measure_cycles(calls, turns):
    """Every slice's own numbers, from the same `analyse` the whole run uses.

    `found` is the count of spawns, and it is returned even when it is zero
    because a caller that reads only `rows` cannot tell *this run delegated
    nothing* from *this file no longer recognises a spawn*. `plan.md`'s
    failure scenario in six months is the second one, and #200 is what the
    first reading of an empty table costs.

    `delegated=DELEGATING` is the whole difference between a cycle row and
    the whole-run row: whatever interval an `Agent` call spans is work that
    ran in another transcript, and charging it here too would count it
    twice. How much of that work the interval actually covers is the
    harness's answer rather than this file's, and `DELEGATING` carries the
    measurement for the one measured here.

    A slice with no calls keeps its row with `numbers` at null. A head of
    nothing is a real reading — the run's first act was a spawn — and
    dropping the row would stop the rows partitioning the run, which is the
    one property the sum over them rests on.

    The numbers are NESTED under `numbers` rather than spread beside the
    labels, because `analyse` already returns a key called `calls` and a row
    naming its own call count would have to shadow it. Nesting also lets a
    case assert that a cycle's keys are the whole run's keys, which is what
    keeps a second meter from being hand-rolled here."""
    rows = []
    for row in spawn_cycles(calls, turns):
        rows.append(
            {
                "kind": row["kind"],
                "cycle": row["cycle"],
                "subagent_type": row["subagent_type"],
                "description": row["description"],
                "numbers": analyse(row["window"], row["turns"], DELEGATING),
            }
        )
    return {"found": len(spawn_cuts(calls)[0]), "rows": rows}


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


def opening_stamp(path):
    """A transcript's first parseable `timestamp`, or None.

    **The one thing this file could not already read.** `load` returns PAIRED
    tool calls only, so a transcript's opening row is in nothing any other
    reader here produces — and the opening is exactly what the join needs,
    because the measurement above `DELEGATING` was taken against it: a
    subagent's transcript OPENS at its spawn's result stamp.

    Joining on the segment's first tool CALL instead would be late by however
    long the agent read and thought before calling anything — #265 measured
    about 110,000 characters of payload arriving before an agent's first call
    — so the tolerance would have to widen from a second to minutes, and a
    window that wide matches the wrong spawn in a batch of two.

    Stops at the first usable stamp rather than reading the file. A file that
    cannot be opened, holds no parseable line, or carries no stamp at all
    returns None and is named by nobody: the same direction `tool_name` and
    `count` take one reader over, a smaller answer rather than none."""
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if not isinstance(row, dict):
                    continue
                when = parse_time(row.get("timestamp"))
                if when:
                    return when
    except OSError:
        return None
    return None


# What a harness writes into a running agent's own transcript when the
# coordinator sends it a new message. `skills/verify/SKILL.md` §*Measure the
# segment* prescribes the hand split at exactly these rows, in exactly these
# words, and until now nothing asserted it against a file.
#
# **Measured over the 350 segment transcripts on one machine before this was
# written.** 41 of them hold an idle gap at or above `analyse`'s 900-second
# ceiling, 82 such gaps in all, and the row after a gap is a `type=user` row
# carrying `isMeta` and a bare string in 61 of the 82. Of those, the ones
# beginning with the sentence below are the coordinator's; the rest are the
# harness talking to the agent about itself -- a response cut off mid-stream,
# a background-task notification -- and splitting at those would cut one
# stretch of work in half.
#
# **So the marker is the sentence and not the row shape**, and the cost is
# that a harness rewording it stops every split. That failure is loud rather
# than silent: a file that can no longer be cut falls to the floor below,
# which prints one row AND names the idle gap the span now covers. A reader
# sees a segment that worked for 37 seconds reported over two hours with a
# line saying why. The alternative -- splitting on `isMeta` alone -- fails
# the other way, cutting a working stretch in two with nothing on the page.
COORDINATOR_MESSAGE = "The coordinator sent a message while you were working:"


def resume_cuts(path):
    """The stamps at which a coordinator's new message restarted this segment.

    A resumed agent's transcript holds several stretches of work in one file,
    and read whole it reports a span covering every idle gap between them —
    a segment that worked for 37 seconds reading as two hours. The hand
    method was to split the file by eye and measure one slice; these are the
    cuts that does by hand.

    Run through a running maximum, the way `spawn_cuts` runs its own: cuts
    that go backwards would overlap the windows they exist to partition.

    A file that cannot be opened or holds no marker returns nothing, and the
    segment is one row — with `widest_idle_gap` naming what that row's span
    then covers."""
    cuts = []
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except ValueError:
                    continue
                if not isinstance(row, dict) or row.get("type") != "user":
                    continue
                if not row.get("isMeta"):
                    continue
                message = row.get("message")
                if not isinstance(message, dict):
                    continue
                content = message.get("content")
                if not isinstance(content, str):
                    continue
                if not content.lstrip().startswith(COORDINATOR_MESSAGE):
                    continue
                when = parse_time(row.get("timestamp"))
                if when:
                    cuts.append(max(when, cuts[-1]) if cuts else when)
    except OSError:
        return []
    return cuts


def widest_idle_gap(calls):
    """The longest stretch inside these calls in which the agent issued
    nothing, or 0.0 where there is none worth naming.

    Only gaps at or above `analyse`'s 900-second ceiling count, because that
    is the gap the model walk already drops: below it the wait is in
    `model_s` and a reader can see it, and at or above it the time is in the
    span and in no other column. Naming it is the floor for a file that has
    an idle gap and no marker to cut it at."""
    widest = 0.0
    for before, after in itertools.pairwise(calls):
        gap = (after["start"] - before["end"]).total_seconds()
        if gap >= 900:
            widest = max(widest, gap)
    return widest


def join_segments(openings, spawns):
    """Each segment paired with the spawn whose result it opened at, or None.

    `openings` is `[(path, opened)]` and `spawns` the `Agent` calls. A
    segment takes the nearest UNCLAIMED spawn result within
    `JOIN_TOLERANCE_S`, segments considered in opening order, and each spawn
    is claimed at most once.

    **The claim is what keeps a batch of two from naming one agent twice.**
    Two segments opening at the same instant and one spawn between them is a
    real shape — a nested transcript opens whenever its own parent spawned
    it, which can be the same second — and without the claim both rows carry
    the same name and a reader adding a column counts one segment twice.

    **A segment that matches nothing is named by nobody rather than by its
    nearest spawn.** The unnamed count is the reading: on the machine this
    was measured on, 44 of 349 segment transcripts had no `Agent` call in
    their parent at all, because a subagent of a subagent is spawned from a
    transcript the parent never sees. Naming those by proximity would put a
    confident wrong name on every one of them.

    Returns the pairs in opening order and how many spawns went unclaimed.
    Both counts are returned even when they agree, for the reason
    `report_spawns` prints its own: a join that silently matched nothing
    reads exactly like a run that spawned nothing."""
    claimed = [False] * len(spawns)
    paired = []
    for path, opened in sorted(openings, key=lambda pair: pair[1]):
        best = None
        for index, call in enumerate(spawns):
            if claimed[index]:
                continue
            distance = abs((opened - call["end"]).total_seconds())
            if distance <= JOIN_TOLERANCE_S and (best is None or distance < best[1]):
                best = (index, distance)
        if best is None:
            paired.append((path, None))
        else:
            claimed[best[0]] = True
            paired.append((path, spawns[best[0]]))
    return paired, claimed.count(False)


def segment_slices(transcript, labels):
    """One transcript's rows — one per stretch of work, not one per file.

    **One row is one segment, and a resumed agent's file holds several.** The
    coordinator sends a running agent a new message, the agent goes on in the
    same transcript, and the idle gap between the two stretches belongs to
    neither. Read whole, the file reports a span covering that gap: measured
    on this repository's own fixture, 140.1 minutes for an agent that worked
    for 37 seconds.

    **Every slice carries the file's name, because only the file's opening
    can be joined.** A resume has no `Agent` call of its own in any
    transcript — the coordinator sent a message, it did not spawn — so the
    second slice would otherwise read as a segment nobody spawned, and the
    unnamed count, which is a reading about the harness, would climb with
    every resume.

    **The token figure stays the file's and rides its first slice.**
    `token_totals` keys a streamed message by its id and keeps the largest
    count each field reached (#202); re-deriving that per slice would
    duplicate the rule, and a message whose rows straddled a boundary would
    be counted in both — #202's own failure shape rebuilt one reader over.
    So later slices carry `None` and the table prints a dash, which is a
    reader seeing there is nothing to add rather than adding a number twice.
    What that gives up is a per-slice token column, stated here rather than
    left to be found.

    **A cut is a marker and not a stretch of work, so a window with no call
    in it is not a row.** The coordinator can send one message and then
    another before the agent acts; the empty window between them would print
    as a slice the agent never worked, push every later `N/of` up by one, and
    borrow `no paired call` from the whole-transcript case below. The file
    that paired no call anywhere still owes its one row.

    Where there is no marker and an idle gap anyway, the file is one row and
    `idle_gap_s` says what that row's span covers."""
    calls, turns = load(transcript)
    cuts = resume_cuts(transcript)
    if not cuts:
        return [
            {
                **labels,
                "slice": 1,
                "slices": 1,
                "idle_gap_s": widest_idle_gap(calls),
                "spawns": sum(1 for c in calls if c["tool"] in DELEGATING),
                "numbers": analyse(calls, turns),
                "tokens": token_totals([transcript]),
            }
        ]
    call_windows = in_windows(cuts, calls, lambda c: c["start"])
    stamped = [(parse_time(stamp), value) for stamp, value in turns]
    turn_windows = in_windows(
        cuts,
        # A stamp that will not parse has no window to fall in, and is
        # dropped rather than charged to a guess — `spawn_cycles` takes the
        # same direction for the same reason.
        [t for t in stamped if t[0] is not None],
        lambda t: t[0],
    )
    # A window with no call in it is not a stretch of work. The coordinator
    # can send one message and then another before the agent acts, and the
    # empty window between them was printed as a slice the agent never worked
    # -- which also pushed every later `N/of` up by one, so the second of two
    # stretches read as `3/3`. It also re-used `no paired call`, which means a
    # whole transcript that read and thought and spent tokens, for a slice
    # that spent nothing. Reachable and not observed: zero call-less slices
    # across the 43 runs on the machine this was written on.
    #
    # The `or [0]` is the file that paired no call at all. It still owes its
    # row, for the reason `measure_segments`' docstring gives.
    kept = [i for i in range(len(cuts) + 1) if call_windows[i]] or [0]
    rows = []
    for position, index in enumerate(kept):
        window = call_windows[index]
        rows.append(
            {
                **labels,
                "slice": position + 1,
                "slices": len(kept),
                # Within a slice the gap is named too: a coordinator can send
                # a message to an agent that then idles again for its own
                # reasons, and one marker does not answer for the whole file.
                "idle_gap_s": widest_idle_gap(window),
                # Per SLICE and not per file: a resumed agent's breach
                # belongs to the stretch it happened in, and #343's line has
                # to name which agent — and which of its stretches — did it.
                "spawns": sum(1 for c in window if c["tool"] in DELEGATING),
                "numbers": analyse(window, turn_windows[index]),
                # The first KEPT slice, not window 0, which may have been
                # dropped as empty. The figure is the file's and rides one row.
                "tokens": token_totals([transcript]) if position == 0 else None,
            }
        )
    return rows


def measure_segments(path, calls):
    """One row per spawned segment of this run, read from that segment's own
    transcript rather than from the parent's columns.

    **This is the number that is in no other column.** A cycle row's
    `delegated` is the `Agent` call's own tool_use-to-tool_result interval,
    which on the measured harness is seconds because the result is written
    when the spawn is ACCEPTED; the agent then runs for a median of about
    1,000 seconds, and that interval is in none of `--spawns`' columns, in
    any row. It is in the segment's own file, and this opens it.

    A row's numbers come from `analyse` with no `delegated`, which is the
    PLAIN reading — exactly what a person running this script against that
    one transcript gets today. That is the point: the mode replaces the hand
    method named in `skills/verify/SKILL.md`, so a row has to be the same
    number that method produced, not a second meter with its own rules.

    A row's tokens cover that segment's OWN file only. The run total sums the
    whole tree, so the two are different numbers on purpose and the column is
    summable only with the parent's own row — `report_segments` says so,
    because a column that looks summable and is not is #200's failure shape
    in a new place.

    A transcript with no paired tool call keeps its row with `numbers` at
    null. A segment that read and thought and called nothing is a real
    reading and it spent tokens the run paid for, which is the same case
    `report_tokens` was split out for."""
    found = subagent_transcripts(path)
    spawns = sorted(
        (c for c in calls if c["tool"] in DELEGATING),
        key=lambda c: (c["end"], c["start"]),
    )
    beside = os.path.dirname(os.path.abspath(path))
    openings = []
    unreadable = []
    for transcript in found:
        opened = opening_stamp(transcript)
        if opened is None:
            # No stamp to join on. The row is still owed — the file is part
            # of the run — and it is named by nobody, which is what the
            # unnamed count is for.
            unreadable.append(transcript)
        else:
            openings.append((transcript, opened))
    paired, unclaimed = join_segments(openings, spawns)
    rows = []
    for transcript, spawn in [*paired, *((t, None) for t in unreadable)]:
        labels = (spawn or {}).get("spawn") or {}
        rows += segment_slices(
            transcript,
            {
                "agent": labels.get("subagent_type", "") if spawn else "",
                "description": labels.get("description", "") if spawn else "",
                "named": spawn is not None,
                "transcript": os.path.relpath(transcript, beside),
            },
        )
    return {
        "tolerance_s": JOIN_TOLERANCE_S,
        "transcripts": len(found),
        "spawns": len(spawns),
        # Over TRANSCRIPTS, never over rows. A resumed file is several rows
        # carrying one name, so counting rows makes this climb with every
        # resume -- which is the failure `segment_slices` gives every slice
        # the file's name to avoid, undone one function later. `report_breaches`
        # reconciles the §6 count against this number, so a row count makes a
        # run whose counts agree print that they do not, and sends a reader
        # looking for a child transcript that was never missing. Measured on
        # the machine this was written on: one of 43 runs already reads 3 for
        # two unnamable files. The resumed count in `report_segments`
        # de-duplicates the same way, which is what this line was missing
        # rather than a new rule.
        "unnamed": len({row["transcript"] for row in rows if not row["named"]}),
        "unclaimed": unclaimed,
        "rows": rows,
    }


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
        #
        # The sentence says what the arithmetic computes, and the arithmetic
        # moved at #300: the span is now the LAST call to end minus the first
        # to begin, so a negative one means no call ended after the first
        # call began -- every one of them, not just the last to begin. The
        # rule change also made this branch rarer on purpose. A call running
        # 10:00-12:00 beside a result written before its own call used to
        # print a negative span for a run that plainly lasted two hours.
        print(
            "              no call ended after the first call began, so the "
            "span is negative and there is no share to take of it"
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
    ranked = sorted(data["by_family"].items(), key=lambda kv: -kv[1]["seconds"])
    for name, row in ranked:
        print(f"  {name:<12}{row['calls']:>4} calls  {minutes(row['seconds']):>7}")
    # Only when `other` LEADS the table, because that is the reading a person
    # would otherwise take at face value: the family with no meaning of its
    # own holding more time than any family that has one means the rows above
    # it are describing a minority of the run. `test` reading 0 while `other`
    # leads is the shape #200 was, and it was published for four releases with
    # nothing on the page suggesting the number was not the number.
    if ranked and ranked[0][0] == "other" and data.get("unnamed"):
        print(
            "              `other` is the largest family and names nothing, so "
            "a runner\n              these patterns do not know reads as no "
            "such run at all.\n              Slowest command charged there: "
            f"{data['unnamed'][:76]}"
        )

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


def cycle_label(row):
    """A slice's name in the printed table.

    A cycle with no `subagent_type` still gets a name. The label is how a
    reader tells one row from the next, so `cycle 3  ?` is worth more than a
    row that reads as a blank."""
    if row["kind"] == "cycle":
        return f"cycle {row['cycle']}  {row['subagent_type'] or '?'}"
    return row["kind"]


def report_spawns(spawns, path, total_calls, run_span=0.0):
    """One row per spawn cycle, or the count and no table.

    `run_span` is the whole run's wall clock, and it is a parameter rather
    than a re-derivation because `main` has already computed it. With it the
    report can say how much of the run is BETWEEN the rows — which the rows
    themselves cannot show, since each one's `span` starts at its own first
    call. Zero means the caller had no reading to give, and the line is then
    not printed at all.

    **A negative is a different case and takes a different guard, and this
    docstring used to conflate them.** `run_span` cannot go negative; the
    DIFFERENCE between it and the rows' spans can, because the rows partition
    the calls and not the spans. Where it does, the figure is refused rather
    than printed — the comment at the subtraction says why, and why the
    refusal does not name the shortfall an overlap.

    **The refusal is the whole reason this prints a count.** A harness that
    renames the spawn tool, or spawns arriving through a path that writes no
    `tool_use` block, would leave this mode reporting zero cycles on a run
    that had six — and an empty table reads as *this run spawned nothing*,
    which is #200's failure shape exactly. So the count and the transcript
    path are printed and the table is not, which is the same repair #200
    took: say what was found, and do not render a shape that means something
    else when it is empty."""
    found, rows = spawns["found"], spawns["rows"]
    if not rows:
        print(f"0 spawns found in {path}\n")
        print(
            "No `Agent` tool_use block in this transcript, so there is no "
            "spawn cycle to slice it at."
        )
        print(
            "The count is printed and the table is not: an empty table reads "
            "as a run that\nspawned nothing, and a run that DID spawn reads "
            "exactly the same way the moment\na harness stops writing a spawn "
            "as an `Agent` call."
        )
        return
    print(
        f"{plural(found, 'spawn')} found, and the run slices into "
        f"{plural(len(rows), 'row')} — every call in exactly one of them"
    )
    print("  head        before the first spawn went out — the run's framing")
    print("  cycle N     spawn N-1's result arriving until spawn N's arrives")
    print("  tail        after the last spawn's result — the closing work")
    print("  delegated   the `Agent` call's own tool_use-to-tool_result span")
    print(
        "\n  A cycle row is a band over several acts and never an attribution\n"
        "  to one: inside it the orchestrator waits on the previous agent,\n"
        "  verifies the report it hands over and frames the next prompt, and\n"
        "  no transcript field marks where any of those ends."
    )
    # The measured harness writes the `Agent` result when the spawn is
    # ACCEPTED, so `delegated` reads seconds where the agent ran for twenty
    # minutes. A column of zeroes that a reader takes for *nothing was
    # delegated* is #200's failure shape one column over, so the page says
    # which of the two it is looking at rather than leaving the reader to
    # assume. It fails toward saying so: a run of genuinely quick agents gets
    # one sentence it did not need, where the silence costs a wrong reading.
    delegated_max = max(
        (row["numbers"]["delegated_s"] for row in rows if row["numbers"]), default=0.0
    )
    if delegated_max < 60:
        print(
            f"\n  `delegated` never reaches a minute here — {delegated_max:.0f}s at "
            "most — so on this\n  harness the `Agent` result is written when the "
            "spawn is ACCEPTED rather than\n  when its report arrives. The agent's "
            "own wall clock is then in NONE of the\n  columns above, in this row or "
            "any other: it is the gap between one row's\n  last call and the next "
            "row's first, and a row's `span` starts at its own\n  first call while "
            "`model` never counts the gap before it. Its own transcript\n  under "
            "`<session-id>/subagents/` is where that number is."
        )
    print(
        "\n  "
        f"{'row':<30}{'span':>8}{'command':>9}{'model':>8}"
        f"{'delegated':>11}{'calls':>7}{'t/turn':>8}{'gap':>7}"
    )
    counted = 0
    for row in rows:
        numbers = row["numbers"]
        if not numbers:
            # A real reading, not a gap in the table: an empty head means the
            # run's first act was a spawn. The row stays so the rows go on
            # partitioning the run.
            print(f"  {cycle_label(row):<30}     no call in this window")
            continue
        counted += numbers["calls"]
        delegated = numbers["delegated_s"]
        print(
            f"  {cycle_label(row):<30}"
            f"{minutes(numbers['span_s']):>8}"
            f"{minutes(numbers['command_s']):>9}"
            f"{minutes(numbers['model_s']):>8}"
            f"{(minutes(delegated) if delegated else '—'):>11}"
            f"{numbers['calls']:>7}"
            f"{numbers['tools_per_turn']:>8.2f}"
            f"{numbers['gap_mean_s']:>6.0f}s"
        )
    # Printed rather than asserted, and printed even when it agrees. The
    # partition is what the rows rest on, so a reader gets to see it hold
    # instead of taking this file's word for it.
    print(
        f"\n  {plural(counted, 'call')} over the rows above, of "
        f"{plural(total_calls, 'call')} in the transcript"
    )
    # The rows partition the CALLS. They do not partition the TIME: a row's
    # `span` starts at its own first call, so the wait after each spawn's
    # result is between two rows and in no column. Printed because it is
    # 12-31% of a measured run, and a reader adding the span column has no
    # other way to learn the total is short. `mostly` is measured: the wait
    # is 98% of the interval and the rest is each row's last call to the cut.
    #
    # And the subtraction can come out NEGATIVE, which is not an interval and
    # must not be printed as one. `in_windows` assigns a call by its START,
    # which is what makes the CALLS partition and is not enough to make the
    # spans partition: a call that outlives the cut its row ends at stays in
    # the row it began in while the next row's calls have already started,
    # so two rows' spans cover the same seconds and their sum can pass the
    # run's own span. A background `Bash` command in the head row printed `-16.5m of the
    # run's 16.6m is BETWEEN the rows — mostly the wait`, exit 0 — the class of
    # false printed line #145 exists to close, reintroduced by the fix for it.
    #
    # The refusal prints the two SUMS and not their difference. `minutes` is
    # one decimal, so an overlap under three seconds printed `by 0.0m` beside
    # a refusal and read as nothing having happened; two figures the reader
    # subtracts carry the same fact and never round one of them away.
    #
    # And it names the cut a row ENDS at, never a spawn's result.
    # `spawn_cuts` opens its cut list at the first spawn's START, so the head
    # row's cut is not a result at all: a head call can outlive its own row's
    # cut and still end before that spawn's result arrives, and naming the
    # result then names a cause the transcript does not carry.
    #
    # Neither printed figure is the rows' OVERLAP, and after #300 that holds
    # for a new reason. A row's span now ends at its own last call to END,
    # and so does the run's, so every row's interval is a SUBINTERVAL of the
    # run's. The difference is therefore the gaps between the rows minus
    # their overlap, and a negative one is the overlap net of the gaps. Where
    # the head row covers the whole run there are no gaps and the two
    # coincide -- which is exactly why naming it the overlap would be a claim
    # that holds on the pinned fixture and fails in general. Before #300 the
    # grounds were different: the span read the last call TO BEGIN's end, so
    # an outliving call shortened the RUN's span too and the difference
    # carried both errors.
    #
    # That subinterval property is also why this can no longer fire on ONE
    # row. It used to: the head row's span reached 1000s against a run of
    # 995s, so a single row passed the whole run. Now a sum past the run's
    # span requires two rows covering the same seconds.
    if run_span > 0:
        spans = sum(row["numbers"]["span_s"] for row in rows if row["numbers"])
        outside = run_span - spans
        # `>= 0` and not `> 0`: an exact cover is the partition agreeing, and
        # the tally above is printed even when it agrees for the same reason.
        # `mostly` covers the other direction too: where a small overlap is
        # netted off against larger gaps, what prints is the gaps minus the
        # overlap, so the figure is a floor on what is between the rows and
        # never an overstatement of it.
        if outside >= 0:
            print(
                f"  {minutes(outside)} of the run's {minutes(run_span)} is BETWEEN "
                f"the rows — mostly the wait\n  after each spawn's result, in no "
                "column above"
            )
        else:
            print(
                f"  the rows' spans sum to {minutes(spans)} against the run's own "
                f"{minutes(run_span)}, so\n  this run has no between-the-rows "
                "figure: a call outlived the cut\n  its row ends at, and the row "
                "it began in covers seconds the\n  next row's does too"
            )
    described = [r for r in rows if r["kind"] == "cycle" and r["description"]]
    if described:
        print("\nwhat each cycle spawned")
        for row in described:
            print(f"  {cycle_label(row):<30}{row['description'][:70]}")


# The label column of the per-segment table, named once because
# `segment_label` cuts to it and `report_segments` pads to it. Two literals
# that have to agree is a column that goes ragged the day one of them moves.
LABEL_WIDTH = 30


def segment_label(row):
    """A segment's name in the printed table.

    A named row is its agent. A row named by nobody is its transcript's path
    relative to the file it was measured beside, because that is the thing a
    reader can actually open — `cycle_label`'s `?` says a name is missing,
    and here there is somewhere to go and look instead.

    **A path too long for the column is cut from the LEFT.** A path is read
    from the right: the file name is what gets opened, and the directories
    above it are already known — they are beside the transcript that was
    named. Cutting from the right the way every other label here is cut left
    `main/subagents/inner/agent-dee`, which is the one part of the path a
    reader cannot use."""
    # A resumed file's slices all carry one agent's name, so without this a
    # reader cannot tell a segment that was resumed from two agents of the
    # same kind — and the two mean completely different things about a run.
    suffix = f"  {row['slice']}/{row['slices']}" if row["slices"] > 1 else ""
    width = LABEL_WIDTH - len(suffix)
    if row["named"]:
        return row["agent"][:width] + suffix
    transcript = row["transcript"]
    if len(transcript) <= width:
        return transcript + suffix
    return "…" + transcript[-(width - 1) :] + suffix


def report_breaches(segments):
    """#343: an `Agent` call made INSIDE a segment, named where it happened.

    `skills/agent-contract/SKILL.md` §6 withholds four acts from every agent
    whatever its own definition says, and one of them is spawning. Delivery
    is not what failed: round 1 of #120 spawned two agents and disclosed
    neither, with the rule already in that agent's payload, in a section the
    same agent was reviewing a diff of. So this is not a second place to put
    the rule — it is a place the act shows up whether or not anybody says so.

    **It notices and stops nothing, and that is the claim the evidence's
    location permits rather than a softer one chosen on taste.** The
    transcript is under the home directory of the machine that ran the agent:
    it is in no commit, reaches no CI runner, and a checker that read one
    would run exactly where a person already is. A line in a report a person
    already runs at every segment boundary is what that leaves. Making it an
    exit code is a later work item's, and it will be choosing against
    readings rather than against a guess.

    **It says who §6 reaches, because the walk cannot tell.** §6 binds the
    agents this plugin spawns. An `Agent` call in a segment's transcript is
    all this file can see, and a `subagent_type` from somewhere else — one
    whose own procedure instructs the fan-out — looks exactly the same.
    Measured over the 43 runs on the machine this was written on: 13 carry
    the line, 12 of them name an agent this plugin spawns, and the thirteenth
    names `claude-preset:code-reviewer`, which no definition here governs.
    The row is still worth printing — a spawn made inside a segment is worth
    seeing whoever made it — so the scope is stated rather than the row
    filtered, which is the same direction the two counts below take. A line
    that cries a rule at an agent the rule does not reach is one a reader
    learns to discount.

    **The two counts of one breach are printed rather than reconciled.** A
    spawn made inside a segment arrives twice — as an `Agent` call in that
    segment's own file, and as a transcript with no call in the PARENT to
    name it. Where they disagree, either a child's transcript is missing or a
    segment is unnamed for the other reason, its opening outside the
    tolerance, and nothing in this file can tell which. Saying so is worth
    more than picking one."""
    rows = segments["rows"]
    breaches = [row for row in rows if row["spawns"]]
    calls = sum(row["spawns"] for row in rows)
    unnamed = segments["unnamed"]
    if not calls and not unnamed:
        return
    if breaches:
        print("\n  §6 — an agent spawned another agent")
        for row in breaches:
            print(
                f"    {segment_label(row).strip()} made "
                f"{plural(row['spawns'], '`Agent` call')} in its own transcript"
            )
        print(
            "\n  `skills/agent-contract/SKILL.md` §6 withholds four acts from "
            "every agent\n  whatever its own definition says: post nothing, "
            "push nothing, open no pull\n  request, and spawn no agent. This "
            "line notices and stops nothing — the\n  transcript it read is on "
            "the machine that ran the agent, in no commit and on\n  no CI "
            "runner, and a report a person already runs at every segment "
            "boundary is\n  what that leaves."
        )
        print(
            "\n  §6 binds the agents this plugin spawns. A row above naming "
            "an agent from\n  somewhere else is still a spawn made inside a "
            "segment and still worth\n  seeing, but which rule it answers to "
            "is for that agent's own definition\n  to say."
        )
    print(
        f"\n  {plural(calls, '`Agent` call')} inside a segment, against "
        f"{plural(unnamed, 'segment')} the parent\n  could not name"
        + (
            ", and the two agree."
            if calls == unnamed
            else ", and the two do not agree."
        )
    )
    print(
        "  One spawn arrives twice — as a call in the spawning segment's own "
        "file, and as\n  a transcript with no `Agent` call in this one to name "
        "it. Where the counts\n  part, a child's transcript is missing or a "
        "segment is unnamed for the other\n  reason, and nothing here can tell "
        "which; both numbers print so a reader can."
    )


def report_segments(segments, path):
    """One row per spawned segment, or the count and no table.

    **This is the reading the hand method produced one transcript at a
    time.** `skills/verify/SKILL.md` §*Measure the segment* put a
    `session_cost.py` run at the end of every smith and warden segment, which
    means opening each segment's file by hand and, for a resumed one,
    splitting it by eye. The rows below are that, for every segment of a run,
    in one command.

    **A segment is one agent's own stretch of a chain, and a spawn cycle is
    not one.** `--spawns` slices THIS transcript into bands over the
    orchestrator's own minutes; this opens the OTHER transcripts, one row
    each. The two modes answer different questions and sit beside each other.

    The refusal is `report_spawns`' and it is here for the same reason: a
    harness that moves `<session-id>/subagents/`, or stops opening a segment
    at its spawn's result, would leave this printing an empty table on a run
    that spawned six — and an empty table reads as a run that spawned
    nothing, which is #200's failure shape exactly. So the count and the path
    are printed and the table is not.

    Every count prints even when they agree, which is `report_spawns`'
    partition tally one reader over: a join that silently matched nothing
    reads exactly like a run whose segments were all named."""
    rows = segments["rows"]
    if not rows:
        print(f"0 segments found beside {path}\n")
        print(
            "No transcript under this run's `<session-id>/subagents/`, so there "
            "is no segment\nto open. That is the ordinary case for a segment "
            "measured on its own rather\nthan a failure, and the exit code says "
            "so."
        )
        print(
            "\nThe count is printed and the table is not: an empty table reads "
            "as a run that\nspawned nothing, and a run that DID spawn reads "
            "exactly the same way the moment\na harness moves that directory or "
            "stops opening a segment at its spawn's result."
        )
        return
    print(
        f"{plural(segments['transcripts'], 'segment transcript')} beside this "
        f"one, {plural(segments['spawns'], 'spawn')} in it, joined within "
        f"{segments['tolerance_s']:.1f}s"
    )
    print(
        f"  {plural(segments['unnamed'], 'segment')} named by nobody, and "
        f"{plural(segments['unclaimed'], 'spawn')} that claimed none"
    )
    print(
        "\n  agent       the `subagent_type` of the spawn whose result this "
        "segment opened at\n  span        this segment's OWN wall clock — the "
        "number in no column of any\n              `--spawns` row, because "
        "that mode's `delegated` is the interval\n              until the spawn "
        "was ACCEPTED\n  tokens      output + cache write + cache read, over "
        "this segment's own file"
    )
    if segments["unnamed"]:
        print(
            "\n  A segment named by nobody carries its transcript's path "
            "instead. Either the\n  parent made no `Agent` call for it — a "
            "subagent of a subagent is spawned from\n  a transcript the parent "
            "never sees — or its opening sits outside the tolerance\n  above. "
            "The row is printed either way: a file this mode cannot name is "
            "still\n  part of the run, and dropping it would take its numbers "
            "out of the reading too."
        )
    resumed = [row for row in rows if row["slices"] > 1]
    if resumed:
        print(
            "\n  Slices marked `N/of` above come from "
            f"{plural(len(set(row['transcript'] for row in resumed)), 'segment')} "
            "the coordinator\n  restarted. It sent the agent a new message and "
            "the agent went on in the same\n  transcript, so the idle gap "
            "between two stretches belongs to neither and no\n  slice's span "
            "covers it. Every slice carries "
            "the file's name: a resume has no `Agent` call of its\n  own "
            "anywhere, so only the file's opening could be joined. The token "
            "figure is\n  the file's and rides its first slice, which is why "
            "the others print a dash."
        )
    # The floor. A file with an idle gap and no marker to cut it at is one
    # row whose span covers the wait, and that is a true reading nobody can
    # see in the columns -- `analyse`'s model walk drops any gap of 900s or
    # more, so it is in `span` and in nothing else. Named rather than left,
    # because the alternative is a segment that worked for half a minute
    # reported over two hours with nothing on the page.
    stuck = [row for row in rows if row["idle_gap_s"]]
    if stuck:
        widest = max(row["idle_gap_s"] for row in stuck)
        print(
            "\n  An idle gap with no coordinator message in it to cut at sits "
            f"inside\n  {plural(len(stuck), 'row')} above — the widest is "
            f"{minutes(widest)}. That time is inside the row's span and "
            "in no\n  other column, because the model walk drops any gap of "
            "fifteen minutes or more.\n  Read such a span as a stretch of work "
            "plus a wait, never as work."
        )
    print(
        f"\n  {'agent':<{LABEL_WIDTH}}{'span':>8}{'calls':>7}{'t/turn':>8}{'gap':>7}{'tokens':>14}"
    )
    for row in rows:
        numbers, tokens = row["numbers"], row["tokens"]
        # A dash, not a zero. A later slice of a resumed file has no token
        # figure of its own -- the file's rides its first slice -- and a zero
        # there reads as a stretch that spent nothing.
        spent = (
            f"{tokens['output'] + tokens['cache_write'] + tokens['cache_read']:,}"
            if tokens
            else "—"
        )
        if not numbers:
            # A real reading, not a gap in the table: a segment that read and
            # thought and called nothing has no span and still spent what the
            # run paid for. `report_tokens` was split out for the same shape.
            print(
                f"  {segment_label(row):<{LABEL_WIDTH}}"
                f"{'no paired call':>30}{spent:>14}"
            )
            continue
        print(
            f"  {segment_label(row):<{LABEL_WIDTH}}"
            f"{minutes(numbers['span_s']):>8}"
            f"{numbers['calls']:>7}"
            f"{numbers['tools_per_turn']:>8.2f}"
            f"{numbers['gap_mean_s']:>6.0f}s"
            f"{spent:>14}"
        )
    report_breaches(segments)
    # A column that looks summable and is not is #200's failure shape in a
    # new place, so the page says which of the two it is rather than leaving
    # the reader to find out by comparing two numbers that should have
    # agreed. `token_totals` already sums the whole tree for the run's own
    # reading, so the rows here and that total overlap completely.
    print(
        "\n  The token column covers each segment's OWN file. The run's own "
        "reading already\n  sums the whole tree, so adding this column to it "
        "is counting the same tokens\n  twice."
    )
    # #200 left this repository's own runner in the `other` family and #202
    # counted a streamed message at its first partial row, so a token figure
    # and a family row both meant something different before they were
    # repaired. Both are fixed in the code above; a reading that does not say
    # from when it is comparable is a number somebody will hold against one
    # taken before the repair.
    print(
        "\n  Comparable with readings taken since 0.9.4 and not with ones "
        "taken before it:\n  #200 charged this repository's own test runner to "
        "`other`, and #202 counted a\n  streamed message at its first partial "
        "row. Both are repaired in the numbers\n  above."
    )


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
    parser.add_argument("--spawns", action="store_true")
    parser.add_argument("--segments", action="store_true")
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
    # The orchestrator's own rows. Computed for both readings that print
    # them, because `questions.md` Q1 puts `spawns` in `--json` beside the
    # existing keys rather than behind the flag: a reading taken with
    # `--json` and no `--spawns` would otherwise be missing the one thing
    # this work item exists to produce.
    #
    # And NOT computed for the plain printed report, which does not read the
    # key. Measured on a 497-call transcript with 32 spawns: `measure_cycles`
    # is 25.5ms against `analyse`'s own 42.6ms, so computing it there is half
    # again the cost of the reading being printed, for a value nothing shows.
    # `None` reaches only `report`, which reads the keys it names.
    spawns = measure_cycles(calls, turns) if args.spawns or args.json else None
    if args.spawns and not args.json:
        # Before the token walk, which this report does not print and which
        # opens every transcript under the run. A cycle carries no token
        # count of its own: `load` gives tokens per TURN and the tokens a
        # spawn spent are in the subagent's own transcript, so a per-cycle
        # token column would be summing the wrong file.
        report_spawns(spawns, path, len(calls), timings["span_s"] if timings else 0.0)
        return 0
    # The other transcripts of this run, one row each. Computed on the same
    # terms as `spawns` — behind its own flag, and in `--json` regardless, so
    # a machine-readable reading is never missing it.
    #
    # Before the no-tool-calls guard below, the way `--spawns` is: a run whose
    # own transcript paired no call can still have spawned six segments, and
    # the six rows are a reading somebody asked for by name.
    segments = measure_segments(path, calls) if args.segments or args.json else None
    if args.segments and not args.json:
        report_segments(segments, path)
        return 0
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
    data = {
        **(timings or {}),
        "tokens": tokens,
        "spawns": spawns,
        "segments": segments,
    }
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
