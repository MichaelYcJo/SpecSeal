#!/usr/bin/env python3
"""payload_meter — what each agent's startup payload is made of, and what it
costs in tokens.

Every spawn of an agent this plugin defines pays for the same prefix again:
the definition under `agents/`, every `SKILL.md` its `skills:` list injects,
and the two `CLAUDE.md` files the harness adds (the repository's and
`~/.claude/CLAUDE.md`). The prefix is cached for five minutes, and no two
spawns of one agent in a review chain fall inside five minutes of each other
(#292, `spec.md` §Measured before the first edit) — so in a chain it is
written on every spawn. This reads the tree and says what that prefix is.

  bytes, chars    counted from the files.
  tokens          NEVER counted. A token figure is `measured (<transcript>)`
                  where it came from a subagent transcript's first `usage`
                  block, or `estimated (<ratio> B/token, from <origin>)`
                  where it came from a bytes-per-token ratio. A bare number
                  is refused by the module's own tests, because the six
                  calibration spawns put three agents at 2.7, 3.2 and 3.4
                  bytes per token — one ratio does not fit all of them.

Usage:
  payload_meter.py                          one table per agent, estimates
  payload_meter.py --sections               each file split at ## / ### headings
  payload_meter.py --json                   the same as data
  payload_meter.py --calibrate <main.jsonl> measured prefixes and per-agent
                                            ratios from the spawns that
                                            transcript made
  payload_meter.py --baseline <run.json>    the delta against an earlier run;
                                            its ratios are lent to this one
  payload_meter.py --root DIR --agent NAME  a different tree, a subset

Calibration reads the main transcript's `Agent` calls for `subagent_type`,
the matching tool result for `agentId: <id>`, and
`<session>/subagents/agent-<id>.jsonl`'s first assistant `usage` — whose
`input_tokens + cache_creation_input_tokens + cache_read_input_tokens` is the
whole prefix that spawn paid for. The baseline agent (`general-purpose` by
default, no plugin skill) is subtracted, because the harness's own system
prompt, tool schemas and the `CLAUDE.md` pair are in every prefix; what is
left is the agent's own files, and dividing their bytes by it is the ratio.
A transcript that never spawned the baseline agent is refused rather than
subtracted from by zero.

Two things the ratio has to know about the machine it was measured on. A
skill name resolves to `~/.claude/skills/<name>/SKILL.md` when the user has
one, shadowing the plugin's — measured here for `writing-style`, 25,834 B
against the tree's 19,762 B — so the row reports the tree's file, notes the
shadow, and the calibration divides by the bytes the spawn actually read.
And a spawn's first message carries its prompt as well as the payload, so
of several spawns of one agent the SMALLEST prefix is taken and the count
is reported.
"""

import argparse
import datetime as dt
import importlib.util
import itertools
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# The ratio an estimate rests on when nothing measured one: no `--calibrate`
# and no `--baseline` carrying ratios. Between the three measured agents
# (2.71, 3.16, 3.44 over tree bytes; 2.87, 3.41, 3.44 over the bytes the
# spawns read), and labelled `assumed` on every figure it produces.
ASSUMED_RATIO = 3.2

BASELINE_AGENT = "general-purpose"

HEADING = re.compile(r"^#{2,3} ", re.MULTILINE)
AGENT_ID = re.compile(r"\bagentId:\s*([0-9a-f]+)")


def _session_cost():
    """The transcript helpers, imported from the sibling script rather than
    re-derived: how a delegating call names what it spawned, and where a
    run's subagent transcripts are."""
    path = os.path.join(HERE, "session_cost.py")
    spec = importlib.util.spec_from_file_location("specseal_session_cost", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CalibrationError(Exception):
    """A transcript the meter cannot calibrate from — said, never guessed."""


# --- the tree -----------------------------------------------------------------


def plugin_root():
    """`skills/verify/scripts/` → the plugin root, wherever the copy lives."""
    return os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def frontmatter(text):
    """The `name:` and `skills:` an agent definition's frontmatter declares."""
    name, skills = None, []
    if not text.startswith("---"):
        return name, skills
    end = text.find("\n---", 3)
    block = text[3:end] if end != -1 else text[3:]
    in_skills = False
    for line in block.splitlines():
        if re.match(r"^name:\s*\S", line):
            name = line.split(":", 1)[1].strip()
            in_skills = False
        elif re.match(r"^skills:\s*$", line):
            in_skills = True
        elif in_skills and re.match(r"^\s+-\s*\S", line):
            skills.append(line.split("-", 1)[1].strip())
        elif re.match(r"^\S", line):
            in_skills = False
    return name, skills


def read(path):
    with open(path, "rb") as handle:
        raw = handle.read()
    return raw, raw.decode("utf-8", errors="replace")


def sections_of(text):
    """The file split at its `##` / `###` headings, each piece's own size.
    The pieces sum to the file: every byte belongs to exactly one."""
    starts = [m.start() for m in HEADING.finditer(text)]
    bounds = [0, *starts, len(text)]
    out = []
    for begin, end in itertools.pairwise(bounds):
        piece = text[begin:end]
        if begin == 0 and starts and starts[0] == 0:
            continue
        heading = (
            "(before the first heading)"
            if begin == 0
            else piece.split("\n", 1)[0].rstrip()
        )
        out.append(
            {
                "heading": heading,
                "bytes": len(piece.encode("utf-8")),
                "chars": len(piece),
            }
        )
    return out


def file_row(root, rel, display, share, sections):
    path = os.path.join(root, rel)
    row = {"path": display, "share": share}
    if not os.path.isfile(path):
        row.update({"bytes": 0, "chars": 0, "missing": True})
        return row
    raw, text = read(path)
    row.update({"bytes": len(raw), "chars": len(text)})
    if sections:
        row["sections"] = sections_of(text)
    return row


def composition(root, home, name, definition, sections):
    """The rows of one agent's payload, in the order the harness lays them
    out: the definition, each skill, then the harness's `CLAUDE.md` pair."""
    _name, skills = frontmatter(read(os.path.join(root, definition))[1])
    rows = [file_row(root, definition, definition, "agent", sections)]
    for skill in skills:
        rel = os.path.join("skills", skill, "SKILL.md")
        row = file_row(root, rel, rel.replace(os.sep, "/"), "agent", sections)
        shadow = os.path.join(home, ".claude", "skills", skill, "SKILL.md")
        if os.path.isfile(shadow):
            row["shadow"] = {
                "path": f"~/.claude/skills/{skill}/SKILL.md",
                "bytes": len(read(shadow)[0]),
            }
        rows.append(row)
    rows.append(file_row(root, "CLAUDE.md", "CLAUDE.md", "harness", sections))
    user = os.path.join(home, ".claude", "CLAUDE.md")
    rows.append(
        file_row(
            os.path.dirname(user),
            os.path.basename(user),
            "~/.claude/CLAUDE.md",
            "harness",
            sections,
        )
    )
    return rows


def agents_in(root, only=()):
    directory = os.path.join(root, "agents")
    found = {}
    if not os.path.isdir(directory):
        return found
    for entry in sorted(os.listdir(directory)):
        if not entry.endswith(".md"):
            continue
        rel = os.path.join("agents", entry)
        name, _skills = frontmatter(read(os.path.join(root, rel))[1])
        name = name or entry[: -len(".md")]
        if only and name not in only:
            continue
        found[name] = rel.replace(os.sep, "/")
    return found


# --- the transcript -----------------------------------------------------------


def _rows(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError:
                continue
            if isinstance(row, dict):
                yield row


def _text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            b.get("text", "")
            for b in content
            if isinstance(b, dict) and isinstance(b.get("text"), str)
        )
    return ""


def spawns_in(transcript, helpers):
    """Every `Agent` call in a main transcript, paired with the `agentId` its
    result carried. A call whose result carries none (a type the harness
    did not know, for one) is returned under `unread` with why."""
    pending, spawned, unread = {}, [], []
    for row in _rows(transcript):
        message = row.get("message")
        if not isinstance(message, dict):
            continue
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "tool_use" and block.get("name") in (
                helpers.DELEGATING
            ):
                payload = block.get("input")
                if not isinstance(payload, dict):
                    payload = {}
                call_id = block.get("id")
                if isinstance(call_id, str):
                    pending[call_id] = helpers.spawn_labels(payload)
            elif block.get("type") == "tool_result":
                labels = pending.pop(block.get("tool_use_id"), None)
                if labels is None:
                    continue
                kind = labels.get("subagent_type", "?")
                match = AGENT_ID.search(_text_of(block.get("content")))
                if match:
                    spawned.append((kind, match.group(1)))
                else:
                    unread.append(
                        {"subagent_type": kind, "why": "no agentId in the tool result"}
                    )
    return spawned, unread


def first_prefix(path, helpers):
    """The whole prefix a subagent paid for: `input_tokens` plus both cache
    columns of its FIRST assistant message. Later messages carry the
    conversation as well and are not the payload."""
    for row in _rows(path):
        message = row.get("message")
        if not isinstance(message, dict) or message.get("role") != "assistant":
            continue
        usage = message.get("usage")
        if not isinstance(usage, dict):
            continue
        return (
            helpers.count(usage.get("input_tokens"))
            + helpers.count(usage.get("cache_creation_input_tokens"))
            + helpers.count(usage.get("cache_read_input_tokens"))
        )
    return None


def short_name(subagent_type):
    """`specseal:smith` → `smith`; `general-purpose` stays as it is."""
    return subagent_type.rsplit(":", 1)[-1]


def calibration_of(transcript, baseline_agent):
    """Measured prefixes per agent from one main transcript's spawns.

    Several spawns of one agent take the SMALLEST prefix: a first message
    holds the payload plus the spawn prompt, and the prompt only adds."""
    helpers = _session_cost()
    spawned, unread = spawns_in(transcript, helpers)
    by_id = {
        os.path.basename(p)[len("agent-") : -len(".jsonl")]: p
        for p in helpers.subagent_transcripts(transcript)
        if os.path.basename(p).startswith("agent-")
    }
    seen = {}
    for kind, agent_id in spawned:
        path = by_id.get(agent_id)
        if path is None:
            unread.append(
                {"subagent_type": kind, "why": f"no subagents/agent-{agent_id}.jsonl"}
            )
            continue
        prefix = first_prefix(path, helpers)
        if prefix is None:
            unread.append(
                {
                    "subagent_type": kind,
                    "why": f"agent-{agent_id}.jsonl has no assistant usage",
                }
            )
            continue
        name = short_name(kind)
        entry = seen.setdefault(
            name,
            {"measured": prefix, "from": os.path.basename(path), "spawns": 0},
        )
        entry["spawns"] += 1
        entry.setdefault("subagent_type", kind)
        if prefix < entry["measured"]:
            entry.update({"measured": prefix, "from": os.path.basename(path)})
    if baseline_agent not in seen:
        saw = sorted(e["subagent_type"] for e in seen.values()) or ["nothing"]
        raise CalibrationError(
            f"{os.path.basename(transcript)} never spawned the baseline agent "
            f"`{baseline_agent}`, whose prefix is what every other agent's is "
            f"measured against; it spawned {', '.join(saw)}. Spawn one with "
            f"`use no tools, reply with one word`, or name another with "
            f"--baseline-agent"
        )
    return {
        "transcript": os.path.basename(transcript),
        "baseline_agent": baseline_agent,
        "baseline": seen[baseline_agent],
        "agents": {k: v for k, v in seen.items() if k != baseline_agent},
        "unread": unread,
    }


# --- the measurement ----------------------------------------------------------


def _ratio_from_baseline(baseline_data, name):
    ratios = (baseline_data or {}).get("ratios") or {}
    entry = ratios.get(name)
    if isinstance(entry, dict) and isinstance(
        entry.get("bytes_per_token"), int | float
    ):
        return entry["bytes_per_token"]
    return None


def measure(
    root,
    home,
    agents=(),
    sections=False,
    calibrate=None,
    baseline=None,
    baseline_agent=BASELINE_AGENT,
):
    """The whole reading as data. `calibrate` is a main transcript path;
    `baseline` an earlier run's JSON path, whose ratios are lent to agents
    this run did not measure and whose numbers the delta is taken against."""
    baseline_data = None
    if baseline:
        with open(baseline, encoding="utf-8") as handle:
            baseline_data = json.load(handle)
    measured = calibrate_data = None
    if calibrate:
        calibrate_data = calibration_of(calibrate, baseline_agent)
        measured = calibrate_data["agents"]
    out = {
        "measured_at": dt.date.today().isoformat(),
        "root": os.path.relpath(root),
        "ratios": {},
        "agents": {},
    }
    if calibrate_data:
        out["calibrated_from"] = calibrate_data["transcript"]
        out["calibration"] = {
            "baseline_agent": baseline_agent,
            "baseline": calibrate_data["baseline"],
            "unread": calibrate_data["unread"],
        }
    for name, definition in agents_in(root, agents).items():
        files = composition(root, home, name, definition, sections)
        own = [f for f in files if f["share"] == "agent"]
        pair = [f for f in files if f["share"] == "harness"]
        prefix = None
        ratio, origin = None, None
        if measured and name in measured:
            entry = measured[name]
            base = calibrate_data["baseline"]["measured"]
            prefix = {
                "measured": entry["measured"],
                "baseline": base,
                "baseline_agent": baseline_agent,
                "from": entry["from"],
                "spawns": entry["spawns"],
                "subagent_type": entry["subagent_type"],
            }
            delta = entry["measured"] - base
            seen_bytes = sum(f.get("shadow", {}).get("bytes", f["bytes"]) for f in own)
            shadowed = [f["path"] for f in own if "shadow" in f]
            if delta > 0:
                ratio = round(seen_bytes / delta, 2)
                origin = name
                out["ratios"][name] = {
                    "bytes_per_token": ratio,
                    "from": entry["from"],
                    "tokens": delta,
                    "over_bytes": seen_bytes,
                    "shadowed": shadowed,
                }
            else:
                prefix["note"] = (
                    f"prefix {entry['measured']:,} is not above the baseline's "
                    f"{base:,}; nothing to derive a ratio from"
                )
        if ratio is None:
            lent = _ratio_from_baseline(baseline_data, name)
            if lent is not None:
                ratio = lent
                origin = f"{name} in {os.path.basename(baseline)}"
                out["ratios"][name] = {
                    "bytes_per_token": ratio,
                    "from": f"{os.path.basename(baseline)} (lent)",
                }
        if ratio is None:
            ratio, origin = ASSUMED_RATIO, "assumed — nothing calibrated"
        basis = f"estimated ({ratio} B/token, from {origin})"
        for row in files:
            row["tokens"] = round(row["bytes"] / ratio)
            row["basis"] = basis
            for section in row.get("sections", ()):
                section["tokens"] = round(section["bytes"] / ratio)
                section["basis"] = basis
        pair_tokens = sum(f["tokens"] for f in pair)
        total = {
            "bytes": sum(f["bytes"] for f in files),
            "chars": sum(f["chars"] for f in files),
        }
        if prefix and "note" not in prefix:
            total["tokens"] = (prefix["measured"] - prefix["baseline"]) + pair_tokens
            total["basis"] = (
                f"measured ({prefix['from']}) for the agent's own files, "
                f"{prefix['measured']:,} - {prefix['baseline']:,} of "
                f"{baseline_agent}; + estimated CLAUDE.md pair"
            )
        else:
            total["tokens"] = sum(f["tokens"] for f in files)
            total["basis"] = basis
        agent = {"files": files, "total": total}
        if prefix:
            agent["prefix"] = prefix
        out["agents"][name] = agent
    if baseline_data:
        out["delta"] = delta_against(out, baseline_data)
    return out


def delta_against(now, before):
    """Per agent, per file: what changed since the earlier run. Files and
    agents that appeared or disappeared are named rather than diffed."""
    out = {}
    before_agents = before.get("agents") or {}
    for name, agent in now["agents"].items():
        old = before_agents.get(name)
        if not isinstance(old, dict):
            out[name] = {"added_agent": True}
            continue
        old_files = {f["path"]: f for f in old.get("files", []) if "path" in f}
        files, added = {}, []
        for row in agent["files"]:
            past = old_files.pop(row["path"], None)
            if past is None:
                added.append(row["path"])
                continue
            files[row["path"]] = {
                "bytes": row["bytes"] - past.get("bytes", 0),
                "tokens": row["tokens"] - past.get("tokens", 0),
                "basis": row["basis"],
            }
        old_total = old.get("total", {})
        out[name] = {
            "files": files,
            "added": added,
            "removed": sorted(old_files),
            "total": {
                "bytes": agent["total"]["bytes"] - old_total.get("bytes", 0),
                "tokens": agent["total"]["tokens"] - old_total.get("tokens", 0),
                "basis": agent["total"]["basis"],
            },
        }
    for name in before_agents:
        if name not in now["agents"]:
            out[name] = {"removed_agent": True}
    return out


# --- the report ---------------------------------------------------------------


def _n(value):
    return f"{value:,}" if isinstance(value, int) else str(value)


def _signed(value):
    return f"{value:+,}"


def render(data):
    lines = [f"# payload-meter — {data['root']} ({data['measured_at']})", ""]
    calibration = data.get("calibration")
    if calibration:
        base = calibration["baseline"]
        lines += [
            f"Calibrated from `{data['calibrated_from']}`: the baseline agent "
            f"`{calibration['baseline_agent']}` paid {_n(base['measured'])} tokens "
            f"of prefix ({base['from']}, {base['spawns']} spawn"
            f"{'s' if base['spawns'] != 1 else ''}); every measured figure below "
            f"is a spawn's prefix minus that.",
        ]
        for item in calibration.get("unread", ()):
            lines.append(f"- not read: `{item['subagent_type']}` — {item['why']}")
        lines.append("")
    for name, agent in data["agents"].items():
        prefix = agent.get("prefix")
        head = f"## {name}"
        if prefix:
            head += (
                f" — prefix {_n(prefix['measured'])} measured ({prefix['from']}"
                f", {prefix['spawns']} spawn{'s' if prefix['spawns'] != 1 else ''}"
                f", the smallest taken)"
            )
        lines += [head, ""]
        if prefix and "note" in prefix:
            lines += [prefix["note"], ""]
        ratio = data["ratios"].get(name)
        if ratio and "tokens" in ratio:
            lines += [
                f"Ratio {ratio['bytes_per_token']} B/token: {_n(ratio['over_bytes'])} "
                f"bytes the spawn read over {_n(ratio['tokens'])} tokens above the "
                f"baseline"
                + (
                    f" (shadowed on this machine: {', '.join(ratio['shadowed'])})"
                    if ratio.get("shadowed")
                    else ""
                )
                + ".",
                "",
            ]
        lines += ["| File | Bytes | Chars | Tokens | Basis |", "|---|---|---|---|---|"]
        pair = []
        for row in agent["files"]:
            if row["share"] == "harness":
                pair.append(row)
                continue
            lines.append(_file_line(row))
            for section in row.get("sections", ()):
                lines.append(
                    f"| &nbsp;&nbsp;{section['heading']} | {_n(section['bytes'])} | "
                    f"{_n(section['chars'])} | {_n(section['tokens'])} | "
                    f"{section['basis']} |"
                )
        if pair:
            names = " + ".join(f"`{p['path']}`" for p in pair)
            lines.append(
                f"| CLAUDE.md pair ({names}) | {_n(sum(p['bytes'] for p in pair))} | "
                f"{_n(sum(p['chars'] for p in pair))} | "
                f"{_n(sum(p['tokens'] for p in pair))} | {pair[0]['basis']} — inside "
                f"every agent's prefix, the baseline's included |"
            )
            for row in pair:
                if row.get("missing"):
                    lines.append(
                        f"| &nbsp;&nbsp;`{row['path']}` | 0 | 0 | 0 | missing |"
                    )
        total = agent["total"]
        lines.append(
            f"| **total** | {_n(total['bytes'])} | {_n(total['chars'])} | "
            f"{_n(total['tokens'])} | {total['basis']} |"
        )
        lines.append("")
    delta = data.get("delta")
    if delta:
        lines += [f"## Delta against {_baseline_name(data)}", ""]
        for name, change in delta.items():
            if change.get("added_agent"):
                lines.append(f"- `{name}`: added since the baseline")
                continue
            if change.get("removed_agent"):
                lines.append(f"- `{name}`: in the baseline, not in this tree")
                continue
            lines += [
                f"### {name}",
                "",
                "| File | Δ bytes | Δ tokens | Basis |",
                "|---|---|---|---|",
            ]
            for path, row in change["files"].items():
                lines.append(
                    f"| `{path}` | {_signed(row['bytes'])} | {_signed(row['tokens'])} | "
                    f"{row['basis']} |"
                )
            for path in change["added"]:
                lines.append(f"| `{path}` | added | | |")
            for path in change["removed"]:
                lines.append(f"| `{path}` | removed | | |")
            total = change["total"]
            lines.append(
                f"| **total** | {_signed(total['bytes'])} | "
                f"{_signed(total['tokens'])} | {total['basis']} |"
            )
            lines.append("")
    return "\n".join(lines)


def _baseline_name(data):
    for entry in data.get("ratios", {}).values():
        if isinstance(entry.get("from"), str) and entry["from"].endswith(" (lent)"):
            return entry["from"][: -len(" (lent)")]
    return "the baseline"


def _file_line(row):
    if row.get("missing"):
        return f"| `{row['path']}` | 0 | 0 | 0 | missing — named by `skills:`, not in the tree |"
    note = ""
    if "shadow" in row:
        note = (
            f" — shadowed on this machine by `{row['shadow']['path']}` "
            f"({_n(row['shadow']['bytes'])} B)"
        )
    return (
        f"| `{row['path']}` | {_n(row['bytes'])} | {_n(row['chars'])} | "
        f"{_n(row['tokens'])} | {row['basis']}{note} |"
    )


# --- entry --------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--root", default=plugin_root())
    parser.add_argument("--agent", action="append", default=[])
    parser.add_argument("--sections", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--baseline", metavar="FILE")
    parser.add_argument("--calibrate", metavar="TRANSCRIPT")
    parser.add_argument("--baseline-agent", default=BASELINE_AGENT)
    args = parser.parse_args()
    try:
        data = measure(
            os.path.abspath(args.root),
            os.path.expanduser("~"),
            agents=tuple(args.agent),
            sections=args.sections,
            calibrate=args.calibrate,
            baseline=args.baseline,
            baseline_agent=args.baseline_agent,
        )
    except CalibrationError as error:
        print(f"payload-meter: {error}", file=sys.stderr)
        return 1
    if not data["agents"]:
        print(f"payload-meter: no agents/*.md under {args.root}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(render(data))
    return 0


if __name__ == "__main__":
    for _name, _errors in (
        ("stdout", "replace"),
        ("stderr", "backslashreplace"),
    ):
        _stream = getattr(sys, _name, None)
        if hasattr(_stream, "reconfigure"):
            _stream.reconfigure(encoding="utf-8", errors=_errors)
    sys.exit(main())
