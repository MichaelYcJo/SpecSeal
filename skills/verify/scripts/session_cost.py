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


def parse_time(value):
    """None for a stamp that will not parse — one odd row must not end the
    report, the same way one unparseable line does not."""
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None


def family(command):
    for name, pattern in FAMILIES:
        if pattern.search(command):
            return name
    return "other"


def load(path):
    """Tool calls paired with their results, plus per-turn token counts.

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
            stamp = row.get("timestamp")
            message = row.get("message") or {}
            content = message.get("content")
            if not stamp or not isinstance(content, list):
                continue
            usage = message.get("usage") or {}
            turn_key = message.get("id") or row.get("uuid") or f"row-{number}"
            carries_call = False
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    text = (block.get("input") or {}).get("command", "")
                    if not text:
                        text = json.dumps(block.get("input") or {}, ensure_ascii=False)
                    pending[block.get("id")] = (
                        stamp,
                        block.get("name", "?"),
                        " ".join(text.split()),
                        turn_key,
                    )
                    carries_call = True
                elif block.get("type") == "tool_result":
                    started = pending.pop(block.get("tool_use_id"), None)
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
            if carries_call and turn_key not in counted:
                counted.add(turn_key)
                turns.append(
                    (
                        stamp,
                        usage.get("input_tokens", 0)
                        + usage.get("cache_read_input_tokens", 0),
                        usage.get("output_tokens", 0),
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
    inputs = [t[1] for t in turns if t[1]]
    if len(inputs) < 3:
        return []
    third = len(inputs) // 3
    return [
        round(sum(part) / len(part))
        for part in (inputs[:third], inputs[third : 2 * third], inputs[2 * third :])
        if part
    ]


def minutes(seconds):
    return f"{seconds / 60:.1f}m"


def report(data):
    print(f"span          {minutes(data['span_s'])}   ({data['calls']} tool calls)")
    print(
        f"  command     {minutes(data['command_s'])}"
        f"   {data['command_s'] / data['span_s'] * 100:.0f}%"
    )
    print(
        f"  model       {minutes(data['model_s'])}"
        f"   {data['model_s'] / data['span_s'] * 100:.0f}%"
        f"   mean gap {data['gap_mean_s']:.1f}s"
    )
    idle = data["span_s"] - data["command_s"] - data["model_s"]
    if idle > data["span_s"] * 0.1:
        print(
            f"  idle        {minutes(idle)}"
            f"   {idle / data['span_s'] * 100:.0f}%"
            f"   waiting on a person, or on a gap this file cannot see"
        )

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
    if same:
        print(
            f"  repeats            {minutes(same)}  a check re-run for a result "
            f"already produced"
            + (f" ({minutes(exact)} of it identical)" if exact else "")
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
            f"{shape}, and each turn costs "
            f"{data['gap_mean_s']:.0f}s of model time on top of the command"
        )
    growth = data["context_growth"]
    if len(growth) == 3 and growth[2] > growth[0] * 1.5:
        print(
            f"  context            {growth[0]:,} → {growth[2]:,} input tokens; "
            f"later calls cost more than the same call would have earlier"
        )
    if not same and data["tools_per_turn"] >= 1.2:
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
    data = analyse(calls, turns)
    if not data:
        sys.exit("no tool calls in this transcript")
    if args.json:
        print(json.dumps(data, indent=2))
    else:
        report(data)
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
