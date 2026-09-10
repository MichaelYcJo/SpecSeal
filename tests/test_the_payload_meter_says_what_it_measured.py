"""payload_meter: what each agent's startup payload is made of, and what it
costs in tokens — with every token figure carrying its basis.

#292. The meter reads the tree (an agent's definition, each `SKILL.md` its
`skills:` list injects, the two `CLAUDE.md` files the harness adds) and
reports bytes, characters and tokens. Bytes and characters are counted;
tokens are never — they are either MEASURED from a transcript, by
`--calibrate`, or ESTIMATED from a bytes-per-token ratio, and the label on
each figure says which. A bare token number is the defect this module
exists to refuse, because the six calibration spawns in `spec.md` showed
bytes tracking tokens at 2.7 to 3.4 per token across three agents.

The fixtures are a hand-built tree with known sizes and a hand-built
transcript pair (main + `subagents/`) with hand-written `usage` blocks, so a
change that quietly stops subtracting the baseline, or starts printing a
number with no basis, fails here.
"""

import importlib.util
import json
import os
import re
import subprocess
import sys

import pytest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT = os.path.join(ROOT, "skills", "verify", "scripts", "payload_meter.py")
BIN = os.path.join(ROOT, "bin")

# One multibyte character per file so bytes and characters differ, and the
# case that checks them cannot pass by reading one column twice.
ACCENT = "é"


def _load():
    spec = importlib.util.spec_from_file_location("payload_meter_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def meter():
    return _load()


# --- fixtures ----------------------------------------------------------------


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)


def a_tree(tmp_path, skills=("alpha", "beta"), extra_agent=False):
    """A plugin tree: one agent whose `skills:` names two skills, the two
    skill files, and the repository `CLAUDE.md`; plus a home with the user
    `CLAUDE.md`. Every file carries one accent so bytes ≠ chars."""
    root = tmp_path / "plugin"
    home = tmp_path / "home"
    listed = "".join(f"  - {name}\n" for name in skills)
    write(
        str(root / "agents" / "probe.md"),
        f"---\nname: probe\ndescription: a probe\nskills:\n{listed}---\n"
        f"# probe\n\nbody {ACCENT}\n",
    )
    if extra_agent:
        write(
            str(root / "agents" / "other.md"),
            f"---\nname: other\nskills:\n  - alpha\n---\n# other {ACCENT}\n",
        )
    write(
        str(root / "skills" / "alpha" / "SKILL.md"),
        f"---\nname: alpha\n---\n# alpha\n\nintro {ACCENT}\n\n## First\n\none\n\n"
        f"### Nested\n\ntwo\n\n## Second\n\nthree\n",
    )
    write(str(root / "skills" / "beta" / "SKILL.md"), f"# beta\n\nplain {ACCENT}\n")
    write(str(root / "CLAUDE.md"), f"## Repo rules {ACCENT}\n")
    write(str(home / ".claude" / "CLAUDE.md"), f"## User rules {ACCENT}\n")
    return root, home


def size_of(path):
    with open(path, "rb") as handle:
        raw = handle.read()
    return len(raw), len(raw.decode("utf-8"))


def stamp(second):
    return f"2026-09-10T10:00:{second:02d}.000Z"


def spawn_rows(spawns):
    """Main-transcript rows for a list of (subagent_type, agent_id): one
    `tool_use` block naming the type and one `tool_result` carrying the
    `agentId:` line the harness writes."""
    rows = []
    for number, (kind, agent_id) in enumerate(spawns):
        call_id = f"toolu_{number}"
        rows.append(
            {
                "timestamp": stamp(number * 2),
                "message": {
                    "id": f"msg_{number}",
                    "role": "assistant",
                    "content": [
                        {
                            "type": "tool_use",
                            "id": call_id,
                            "name": "Agent",
                            "input": {"subagent_type": kind, "prompt": "reply ready"},
                        }
                    ],
                    "usage": {"input_tokens": 1},
                },
            }
        )
        text = (
            "Async agent launched successfully.\n"
            f"agentId: {agent_id} (internal ID - do not mention to user.)\n"
        )
        rows.append(
            {
                "timestamp": stamp(number * 2 + 1),
                "message": {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": call_id,
                            "content": [{"type": "text", "text": text}],
                        }
                    ],
                },
            }
        )
    return rows


def subagent_rows(cache_write, cache_read, inputs=2):
    """A subagent transcript: a user row with no usage, then the first
    assistant message whose `usage` carries the whole prefix, then a later
    assistant message with a DIFFERENT usage that must not be the one read."""
    first = {
        "input_tokens": inputs,
        "cache_creation_input_tokens": cache_write,
        "cache_read_input_tokens": cache_read,
        "output_tokens": 4,
    }
    later = {
        "input_tokens": 500,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": cache_write + cache_read,
        "output_tokens": 40,
    }
    return [
        {"timestamp": stamp(0), "message": {"role": "user", "content": "hi"}},
        {
            "timestamp": stamp(1),
            "message": {
                "id": "msg_a",
                "role": "assistant",
                "content": [{"type": "text", "text": "ready"}],
                "usage": first,
            },
        },
        {
            "timestamp": stamp(2),
            "message": {
                "id": "msg_b",
                "role": "assistant",
                "content": [{"type": "text", "text": "done"}],
                "usage": later,
            },
        },
    ]


def a_transcript(tmp_path, spawns, prefixes):
    """`spawns` is a list of (subagent_type, agent_id); `prefixes` maps
    agent_id → (cache_write, cache_read). Returns the main transcript path."""
    main = tmp_path / "session-0001.jsonl"
    with open(main, "w", encoding="utf-8") as handle:
        for row in spawn_rows(spawns):
            handle.write(json.dumps(row) + "\n")
    for agent_id, (write_count, read_count) in prefixes.items():
        path = tmp_path / "session-0001" / "subagents" / f"agent-{agent_id}.jsonl"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            for row in subagent_rows(write_count, read_count):
                handle.write(json.dumps(row) + "\n")
    return str(main)


def run(args, home, cwd=None):
    env = dict(os.environ, HOME=str(home), USERPROFILE=str(home))
    return subprocess.run(
        [sys.executable, SCRIPT, *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=cwd or ROOT,
    )


def rows_of(table_text):
    """The data rows of every markdown table in a report, split into cells."""
    out = []
    for line in table_text.splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            out.append(cells)
    return out


# --- S1: the meter reports composition ---------------------------------------


def test_the_composition_table_counts_bytes_and_chars_per_file_and_in_total(
    meter, tmp_path
):
    root, home = a_tree(tmp_path)
    data = meter.measure(str(root), str(home))
    assert list(data["agents"]) == ["probe"]
    files = data["agents"]["probe"]["files"]
    paths = [f["path"] for f in files]
    assert paths == [
        "agents/probe.md",
        "skills/alpha/SKILL.md",
        "skills/beta/SKILL.md",
        "CLAUDE.md",
        "~/.claude/CLAUDE.md",
    ], paths
    on_disk = [
        root / "agents" / "probe.md",
        root / "skills" / "alpha" / "SKILL.md",
        root / "skills" / "beta" / "SKILL.md",
        root / "CLAUDE.md",
        home / ".claude" / "CLAUDE.md",
    ]
    for row, path in zip(files, on_disk, strict=True):
        raw, chars = size_of(path)
        assert (row["bytes"], row["chars"]) == (raw, chars), row["path"]
        assert row["bytes"] > row["chars"], f"{row['path']} carries no multibyte char"
    total = data["agents"]["probe"]["total"]
    assert total["bytes"] == sum(f["bytes"] for f in files)
    assert total["chars"] == sum(f["chars"] for f in files)


def test_the_claude_md_pair_is_marked_as_the_harness_share(meter, tmp_path):
    """The two `CLAUDE.md` files sit in EVERY agent's prefix, the baseline
    agent's included, so a calibrated delta never covers them. The row says
    so, and the pair is reported as the agent's own line in the text."""
    root, home = a_tree(tmp_path)
    data = meter.measure(str(root), str(home))
    files = data["agents"]["probe"]["files"]
    harness = [f["path"] for f in files if f.get("share") == "harness"]
    own = [f["path"] for f in files if f.get("share") == "agent"]
    assert harness == ["CLAUDE.md", "~/.claude/CLAUDE.md"]
    assert own == ["agents/probe.md", "skills/alpha/SKILL.md", "skills/beta/SKILL.md"]
    text = meter.render(data)
    assert "CLAUDE.md pair" in text


def test_sections_split_each_file_at_its_headings_and_sum_to_the_file(meter, tmp_path):
    root, home = a_tree(tmp_path)
    data = meter.measure(str(root), str(home), sections=True)
    alpha = next(
        f
        for f in data["agents"]["probe"]["files"]
        if f["path"] == "skills/alpha/SKILL.md"
    )
    names = [s["heading"] for s in alpha["sections"]]
    assert names == [
        "(before the first heading)",
        "## First",
        "### Nested",
        "## Second",
    ]
    assert sum(s["bytes"] for s in alpha["sections"]) == alpha["bytes"]
    assert sum(s["chars"] for s in alpha["sections"]) == alpha["chars"]
    text = meter.render(data)
    assert "### Nested" in text
    without = meter.measure(str(root), str(home))
    assert "sections" not in without["agents"]["probe"]["files"][1]


def test_json_carries_the_same_numbers_as_the_text_and_no_machine_path(tmp_path):
    root, home = a_tree(tmp_path)
    as_json = run(["--root", str(root), "--json"], home, cwd=str(tmp_path))
    assert as_json.returncode == 0, as_json.stderr
    data = json.loads(as_json.stdout)
    as_text = run(["--root", str(root)], home, cwd=str(tmp_path))
    assert as_text.returncode == 0, as_text.stderr
    for row in data["agents"]["probe"]["files"]:
        assert f"{row['bytes']:,}" in as_text.stdout, row["path"]
    assert str(home) not in as_json.stdout
    assert str(tmp_path) not in as_json.stdout, "an absolute path reached the JSON"
    assert data["root"] == "plugin"
    assert "measured_at" in data


def test_a_skill_the_list_names_and_the_tree_lacks_is_a_row_not_a_crash(
    meter, tmp_path
):
    root, home = a_tree(tmp_path, skills=("alpha", "ghost"))
    data = meter.measure(str(root), str(home))
    ghost = next(f for f in data["agents"]["probe"]["files"] if "ghost" in f["path"])
    assert ghost["bytes"] == 0
    assert ghost.get("missing") is True
    assert "missing" in meter.render(data)


# --- every token figure carries a basis ---------------------------------------


def test_without_calibration_every_token_figure_reads_estimated_and_names_its_origin(
    meter, tmp_path
):
    root, home = a_tree(tmp_path)
    data = meter.measure(str(root), str(home))
    probe = data["agents"]["probe"]
    for row in [*probe["files"], probe["total"]]:
        assert row["basis"].startswith("estimated ("), row
        assert "B/token" in row["basis"], row
        assert "assumed" in row["basis"], (
            "no ratio was measured, so the label has to say the figure rests on "
            f"an assumption: {row['basis']}"
        )
        assert row["tokens"] == round(row["bytes"] / meter.ASSUMED_RATIO), row
    text = meter.render(data)
    for cells in rows_of(text):
        if cells and cells[0] in ("File", "Section"):
            continue
        if len(cells) >= 5 and re.fullmatch(r"[\d,]+", cells[3]):
            assert cells[4].startswith(("estimated", "measured")), cells


# --- S2: measured beside estimated -------------------------------------------


def test_calibrate_subtracts_the_baseline_and_derives_one_ratio_per_agent(
    meter, tmp_path
):
    root, home = a_tree(tmp_path)
    own = sum(
        size_of(p)[0]
        for p in (
            root / "agents" / "probe.md",
            root / "skills" / "alpha" / "SKILL.md",
            root / "skills" / "beta" / "SKILL.md",
        )
    )
    transcript = a_transcript(
        tmp_path,
        [("general-purpose", "aaaa1"), ("plugin:probe", "bbbb2")],
        {"aaaa1": (20000, 10000), "bbbb2": (30002, 10000)},
    )
    data = meter.measure(str(root), str(home), calibrate=transcript)
    # 2 input + 30002 + 10000 = 40004 against 2 + 20000 + 10000 = 30002.
    delta = 40004 - 30002
    probe = data["agents"]["probe"]
    assert probe["prefix"] == {
        "measured": 40004,
        "baseline": 30002,
        "baseline_agent": "general-purpose",
        "from": "agent-bbbb2.jsonl",
        "spawns": 1,
        "subagent_type": "plugin:probe",
    }
    ratio = data["ratios"]["probe"]
    assert ratio["from"] == "agent-bbbb2.jsonl"
    assert ratio["bytes_per_token"] == round(own / delta, 2)
    assert ratio["over_bytes"] == own
    assert ratio["tokens"] == delta
    assert probe["total"]["basis"].startswith("measured (agent-bbbb2.jsonl)")
    assert "estimated" in probe["total"]["basis"], (
        "the CLAUDE.md pair is inside the baseline, so its share is an estimate "
        "even on a calibrated row and the total's basis has to say so"
    )
    pair = [f for f in probe["files"] if f["share"] == "harness"]
    own_rows = [f for f in probe["files"] if f["share"] == "agent"]
    assert probe["total"]["tokens"] == delta + sum(f["tokens"] for f in pair)
    for row in own_rows + pair:
        assert (
            row["basis"]
            == f"estimated ({ratio['bytes_per_token']} B/token, from probe)"
        )
        assert row["tokens"] == round(row["bytes"] / ratio["bytes_per_token"])
    assert data["calibrated_from"] == "session-0001.jsonl"


def test_a_transcript_that_never_spawned_the_baseline_agent_refuses(meter, tmp_path):
    """Subtracting zero would print a measured total that is the whole
    harness prefix, labelled as the agent's own. The refusal names what it
    wanted and what it saw."""
    root, home = a_tree(tmp_path)
    transcript = a_transcript(
        tmp_path, [("plugin:probe", "bbbb2")], {"bbbb2": (30002, 10000)}
    )
    with pytest.raises(meter.CalibrationError) as caught:
        meter.measure(str(root), str(home), calibrate=transcript)
    message = str(caught.value)
    assert "general-purpose" in message
    assert "plugin:probe" in message
    result = run(
        ["--root", str(root), "--calibrate", transcript], home, cwd=str(tmp_path)
    )
    assert result.returncode == 1
    assert "general-purpose" in result.stderr
    assert "measured" not in result.stdout


def test_two_spawns_of_one_agent_take_the_smallest_prefix_and_say_how_many(
    meter, tmp_path
):
    """A spawn's first message carries the payload PLUS its prompt, so the
    smallest prefix seen is the closest to the bare payload; the six
    calibration spawns were told `reply with one word` for this reason."""
    root, home = a_tree(tmp_path)
    transcript = a_transcript(
        tmp_path,
        [
            ("general-purpose", "aaaa1"),
            ("plugin:probe", "bbbb2"),
            ("plugin:probe", "cccc3"),
        ],
        {"aaaa1": (20000, 10000), "bbbb2": (30002, 10000), "cccc3": (0, 35000)},
    )
    data = meter.measure(str(root), str(home), calibrate=transcript)
    prefix = data["agents"]["probe"]["prefix"]
    assert prefix["spawns"] == 2
    assert prefix["measured"] == 35002
    assert prefix["from"] == "agent-cccc3.jsonl"


def test_a_spawn_whose_result_carries_no_agent_id_is_reported_not_counted(
    meter, tmp_path
):
    """The three `tmp-probe-*` spawns in the calibration session failed with
    `Agent type not found` and no agentId; a meter that died on them would
    never have read the six that worked."""
    root, home = a_tree(tmp_path)
    transcript = a_transcript(
        tmp_path,
        [("general-purpose", "aaaa1"), ("plugin:probe", "bbbb2")],
        {"aaaa1": (20000, 10000), "bbbb2": (30002, 10000)},
    )
    with open(transcript, "a", encoding="utf-8") as handle:
        rows = spawn_rows([("tmp-probe", "zzzz9")])
        rows[1]["message"]["content"][0]["content"] = [
            {"type": "text", "text": "Agent type 'tmp-probe' not found."}
        ]
        for row in rows:
            handle.write(json.dumps(row) + "\n")
    data = meter.measure(str(root), str(home), calibrate=transcript)
    assert data["agents"]["probe"]["prefix"]["measured"] == 40004
    assert data["calibration"]["unread"] == [
        {"subagent_type": "tmp-probe", "why": "no agentId in the tool result"}
    ]


def test_a_user_level_skill_shadows_the_trees_and_the_ratio_says_so(meter, tmp_path):
    """Measured on the machine that wrote this: `agents/smith.md` lists
    `writing-style`, the harness resolved the bare name to
    `~/.claude/skills/writing-style/SKILL.md` (25,834 B) rather than the
    plugin's (19,762 B), and adding the difference is what brought the
    warden's ratio to the scribe's. The row reports the tree's file, notes
    the shadow, and the calibration divides by the bytes the spawn READ."""
    root, home = a_tree(tmp_path)
    shadow = home / ".claude" / "skills" / "alpha" / "SKILL.md"
    write(str(shadow), "# alpha, the user's own\n" + "x" * 500 + "\n")
    data = meter.measure(str(root), str(home))
    alpha = data["agents"]["probe"]["files"][1]
    assert alpha["path"] == "skills/alpha/SKILL.md"
    assert alpha["bytes"] == size_of(root / "skills" / "alpha" / "SKILL.md")[0]
    assert alpha["shadow"] == {
        "path": "~/.claude/skills/alpha/SKILL.md",
        "bytes": size_of(shadow)[0],
    }
    assert "shadowed" in meter.render(data)
    transcript = a_transcript(
        tmp_path,
        [("general-purpose", "aaaa1"), ("plugin:probe", "bbbb2")],
        {"aaaa1": (20000, 10000), "bbbb2": (30002, 10000)},
    )
    calibrated = meter.measure(str(root), str(home), calibrate=transcript)
    ratio = calibrated["ratios"]["probe"]
    seen = (
        size_of(root / "agents" / "probe.md")[0]
        + size_of(shadow)[0]
        + size_of(root / "skills" / "beta" / "SKILL.md")[0]
    )
    assert ratio["over_bytes"] == seen
    assert ratio["shadowed"] == ["skills/alpha/SKILL.md"]


# --- S3: before and after ------------------------------------------------------


def test_a_baseline_json_lends_its_ratios_and_the_delta_names_what_moved(
    meter, tmp_path
):
    root, home = a_tree(tmp_path)
    transcript = a_transcript(
        tmp_path,
        [("general-purpose", "aaaa1"), ("plugin:probe", "bbbb2")],
        {"aaaa1": (20000, 10000), "bbbb2": (30002, 10000)},
    )
    before = meter.measure(str(root), str(home), calibrate=transcript)
    before_path = tmp_path / "before.json"
    with open(before_path, "w", encoding="utf-8") as handle:
        json.dump(before, handle)
    # Then the tree changes: alpha loses a section, a new skill appears.
    write(str(root / "skills" / "alpha" / "SKILL.md"), "# alpha\n\nintro\n")
    write(
        str(root / "agents" / "probe.md"),
        "---\nname: probe\nskills:\n  - alpha\n  - beta\n  - gamma\n---\n# probe\n",
    )
    write(str(root / "skills" / "gamma" / "SKILL.md"), "# gamma\n\nnew\n")
    after = meter.measure(str(root), str(home), baseline=str(before_path))
    ratio = before["ratios"]["probe"]["bytes_per_token"]
    alpha = after["agents"]["probe"]["files"][1]
    assert alpha["basis"] == (f"estimated ({ratio} B/token, from probe in before.json)")
    assert alpha["tokens"] == round(alpha["bytes"] / ratio)
    delta = after["delta"]["probe"]
    alpha_before = before["agents"]["probe"]["files"][1]
    assert delta["files"]["skills/alpha/SKILL.md"] == {
        "bytes": alpha["bytes"] - alpha_before["bytes"],
        "tokens": alpha["tokens"] - alpha_before["tokens"],
        "basis": alpha["basis"],
    }
    assert delta["added"] == ["skills/gamma/SKILL.md"]
    assert delta["removed"] == []
    assert delta["total"]["bytes"] == (
        after["agents"]["probe"]["total"]["bytes"]
        - before["agents"]["probe"]["total"]["bytes"]
    )
    text = meter.render(after)
    assert "## Delta against before.json" in text
    assert "skills/gamma/SKILL.md" in text and "added" in text


def _before_and_a_changed_tree(meter, tmp_path):
    """A calibrated run, then the tree changes and NO new spawn is taken —
    the shape #292's own after-number had: the transcript's smallest probe
    spawn read `alpha` as it stood before the cut."""
    root, home = a_tree(tmp_path)
    transcript = a_transcript(
        tmp_path,
        [("general-purpose", "aaaa1"), ("plugin:probe", "bbbb2")],
        {"aaaa1": (20000, 10000), "bbbb2": (30002, 10000)},
    )
    before = meter.measure(str(root), str(home), calibrate=transcript)
    before_path = tmp_path / "before.json"
    with open(before_path, "w", encoding="utf-8") as handle:
        json.dump(before, handle)
    write(str(root / "skills" / "alpha" / "SKILL.md"), "# alpha\n\nintro\n")
    return root, home, transcript, before, str(before_path)


def test_calibrating_the_same_spawn_over_a_changed_tree_keeps_the_ratio_it_read(
    meter, tmp_path
):
    """The measured token count belongs to the bytes that spawn READ. Divided
    by the bytes the tree holds now it is a ratio nobody measured, and the
    first after-run of #292 printed exactly that: smith at 2.49 B/token
    against the 2.87 its spawn paid, and +979 tokens on a file whose bytes
    had not moved. When the baseline names the same spawn over other bytes,
    the baseline's ratio is kept, the row says so, and nothing in the run
    claims to be measured."""
    root, home, transcript, before, before_path = _before_and_a_changed_tree(
        meter, tmp_path
    )
    after = meter.measure(
        str(root), str(home), calibrate=transcript, baseline=before_path
    )
    kept = before["ratios"]["probe"]
    ratio = after["ratios"]["probe"]
    assert ratio["bytes_per_token"] == kept["bytes_per_token"]
    assert "tokens" not in ratio, "a lent ratio has no measurement of its own"
    assert ratio["over_bytes"] == kept["over_bytes"]
    assert "before.json" in ratio["from"] and "same spawn" in ratio["from"]
    probe = after["agents"]["probe"]
    note = probe["prefix"]["note"]
    assert "agent-bbbb2.jsonl" in note and "before.json" in note
    assert f"{kept['over_bytes']:,}" in note, "the bytes the spawn read are named"
    assert "take a spawn after the change" in note
    assert probe["total"]["basis"].startswith("estimated ("), probe["total"]
    assert probe["total"]["tokens"] == sum(f["tokens"] for f in probe["files"])
    alpha = probe["files"][1]
    assert alpha["path"] == "skills/alpha/SKILL.md"
    assert alpha["tokens"] == round(alpha["bytes"] / kept["bytes_per_token"])
    assert alpha["basis"] == (
        f"estimated ({kept['bytes_per_token']} B/token, from probe in before.json)"
    )
    text = meter.render(after)
    assert note in text
    assert "bytes the spawn read over" not in text.split("## probe")[1], (
        "the ratio line would claim the spawn read this tree's bytes"
    )


def test_a_delta_between_a_measured_total_and_an_estimated_one_sums_the_files(
    meter, tmp_path
):
    """Subtracting an estimated total from a measured one reports the gap
    between two bases as if it were a change in the tree: -6,773 tokens on
    #292's after-run, where the files summed to -4,691. Where the two totals
    rest on different bases the token delta is the sum over the files and
    the basis says so; bytes are exact either way and are still subtracted."""
    root, home, _transcript, before, before_path = _before_and_a_changed_tree(
        meter, tmp_path
    )
    write(str(root / "skills" / "gamma" / "SKILL.md"), "# gamma\n\nnew\n")
    write(
        str(root / "agents" / "probe.md"),
        "---\nname: probe\nskills:\n  - alpha\n  - gamma\n---\n# probe\n",
    )
    after = meter.measure(str(root), str(home), baseline=before_path)
    delta = after["delta"]["probe"]
    assert delta["added"] == ["skills/gamma/SKILL.md"]
    assert delta["removed"] == ["skills/beta/SKILL.md"]
    now = {f["path"]: f for f in after["agents"]["probe"]["files"]}
    then = {f["path"]: f for f in before["agents"]["probe"]["files"]}
    summed = (
        sum(d["tokens"] for d in delta["files"].values())
        + now["skills/gamma/SKILL.md"]["tokens"]
        - then["skills/beta/SKILL.md"]["tokens"]
    )
    assert delta["total"]["tokens"] == summed
    assert delta["total"]["bytes"] == (
        after["agents"]["probe"]["total"]["bytes"]
        - before["agents"]["probe"]["total"]["bytes"]
    )
    assert "summed over the files" in delta["total"]["basis"]
    assert "measured" in delta["total"]["basis"]
    assert "estimated" in delta["total"]["basis"]
    assert "summed over the files" in meter.render(after)


def test_a_lent_ratio_keeps_the_spawn_it_was_measured_from(meter, tmp_path):
    """Round 1, finding 1. The after-run of #292 is #120's before-run, and a
    lent entry that names only the file it was lent from loses the spawn
    behind it: one hop later the meter re-derived 2.49 B/token over bytes
    the spawn never read, +5,381 tokens over 0 bytes, and called the total
    measured. `spawn` and `over_bytes` ride every entry shape a baseline can
    carry, and the same-spawn rule reads `spawn` first."""
    root, home, transcript, before, before_path = _before_and_a_changed_tree(
        meter, tmp_path
    )
    kept = before["ratios"]["probe"]
    assert kept["spawn"] == "agent-bbbb2.jsonl", "the derived entry names its spawn"
    after = meter.measure(
        str(root), str(home), calibrate=transcript, baseline=before_path
    )
    assert after["ratios"]["probe"]["spawn"] == "agent-bbbb2.jsonl"
    assert after["ratios"]["probe"]["over_bytes"] == kept["over_bytes"]
    after_path = tmp_path / "after.json"
    with open(after_path, "w", encoding="utf-8") as handle:
        json.dump(after, handle)
    again = meter.measure(
        str(root), str(home), calibrate=transcript, baseline=str(after_path)
    )
    ratio = again["ratios"]["probe"]
    assert ratio["bytes_per_token"] == kept["bytes_per_token"], ratio
    assert "tokens" not in ratio, "a second hop re-derived a measurement"
    assert ratio["spawn"] == "agent-bbbb2.jsonl"
    probe = again["agents"]["probe"]
    assert "note" in probe["prefix"], probe["prefix"]
    assert probe["total"]["basis"].startswith("estimated ("), probe["total"]
    delta = again["delta"]["probe"]
    assert delta["total"] == {
        "bytes": 0,
        "tokens": 0,
        "basis": delta["total"]["basis"],
    }, delta["total"]
    # The plain lent shape carries the same two facts, so a third hop that
    # starts from a run with no --calibrate still knows the spawn.
    plain = meter.measure(str(root), str(home), baseline=before_path)
    assert plain["ratios"]["probe"]["spawn"] == "agent-bbbb2.jsonl"
    assert plain["ratios"]["probe"]["over_bytes"] == kept["over_bytes"]
    # Finding 8, folded in: the delta heading names the file it was taken
    # against, whichever entry shape the ratio has.
    assert after["baseline"] == "before.json"
    assert "## Delta against before.json" in meter.render(after)
    assert "## Delta against after.json" in meter.render(again)


def test_sections_do_not_split_at_a_heading_inside_a_fence(meter, tmp_path):
    """Round 1, finding 2. A skill quotes headings as examples inside a
    fence, and `--sections` listed four of `agents/warden.md`'s fenced
    template headings as sections with real byte counts — a number that
    sends #120 to cut an example. The check one file over already reads a
    fence as a quotation; the meter reads it the same way, and the pieces
    still sum to the file."""
    text = (
        "# alpha\n\nintro\n\n## First\n\nreal\n\n```markdown\n## Example\n"
        "### Nested example\n```\n\n~~~\n## Tilde example\n~~~\n\n## Second\n\nlast\n"
    )
    pieces = meter.sections_of(text)
    assert [p["heading"] for p in pieces] == [
        "(before the first heading)",
        "## First",
        "## Second",
    ], [p["heading"] for p in pieces]
    assert sum(p["bytes"] for p in pieces) == len(text.encode("utf-8"))
    assert sum(p["chars"] for p in pieces) == len(text)


def test_the_delta_lists_an_agent_the_baseline_has_and_the_tree_lost(meter, tmp_path):
    root, home = a_tree(tmp_path, extra_agent=True)
    before = meter.measure(str(root), str(home))
    before_path = tmp_path / "before.json"
    with open(before_path, "w", encoding="utf-8") as handle:
        json.dump(before, handle)
    os.remove(root / "agents" / "other.md")
    after = meter.measure(str(root), str(home), baseline=str(before_path))
    assert after["delta"]["other"] == {"removed_agent": True}
    assert "other" in meter.render(after)


# --- the wrapper pair ----------------------------------------------------------


def test_both_wrappers_ship_and_point_at_the_meter():
    """`bin/` is on the Bash tool's PATH while the plugin is enabled, and
    cmd.exe resolves the `.cmd` twin through PATHEXT.
    `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` pins the
    pairing for every entry; this pins that the pair runs THIS script."""
    posix = os.path.join(BIN, "payload-meter")
    windows = os.path.join(BIN, "payload-meter.cmd")
    assert os.path.isfile(posix), "bin/payload-meter missing"
    assert os.path.isfile(windows), "bin/payload-meter.cmd missing"
    with open(posix, encoding="utf-8") as handle:
        assert "skills/verify/scripts/payload_meter.py" in handle.read()
    with open(windows, encoding="utf-8") as handle:
        text = handle.read()
    assert "skills\\verify\\scripts\\payload_meter.py" in text
    assert "py -3" in text and "python " in text


def test_the_real_tree_runs_and_names_every_shipped_agent(tmp_path):
    """The meter's default root is the plugin root resolved from its own
    location, so it works from the version cache and from a clone."""
    home = tmp_path / "home"
    write(str(home / ".claude" / "CLAUDE.md"), "## user\n")
    result = run(["--json"], home)
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    shipped = sorted(n[: -len(".md")] for n in os.listdir(os.path.join(ROOT, "agents")))
    assert sorted(data["agents"]) == shipped
    for name, agent in data["agents"].items():
        assert agent["files"][0]["path"] == f"agents/{name}.md"
        assert not any(f.get("missing") for f in agent["files"]), name
