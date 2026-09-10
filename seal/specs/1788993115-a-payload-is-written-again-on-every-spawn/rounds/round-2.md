# 1788993115-a-payload-is-written-again-on-every-spawn — review round 2

| Field | Value |
|---|---|
| Target SHA | 179a9a8 |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 329 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 12, the case above, unless answered with grounds |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of #292 is the verifying round: its target is the diff of round 1's fixes, `f5cdd45..b4a9a1d` (eight commits), not the branch, and its job is the answers — for each of the nine `fixed` verdicts in `rounds/round-1.md`, is it actually closed. Re-derive each closure rather than taking it: run the case the fix pass says it saw red, mutate the fix the way the round-1 record's grounds describe, and say plainly which reproduces. One surface is new rather than fixed and is judged as code, *is this correct*: the seventeen entries in round 1's `New units` row — `_spawn_of`, `_carried`, `heading_starts`, `FENCE`, `bare`, `ending_of`, the copied floor guard (`FLOOR`, `FLOOR_TEXT`, `BELOW_FLOOR`, `below_floor`, `_refusal`) and the six new cases — none of which any round has read. Two shapes to try there: `_spawn_of`'s fallback to `from` when `tokens` marks a measurement (what does a baseline written by 0.9.5's meter, with neither `spawn` nor `tokens`, do); and `heading_starts`'s fence tracking against a fence opened with `~~~` or an indented fence. The `Contract changes` row names `_baseline_name → render` and two records; open the reach. Facts handed over as executed by the orchestrator at `b4a9a1d`: 148 passed over seven touched modules; `--calibrate <transcript> --baseline payload-after.json --agent smith` keeps 2.87 and labels the total estimated with a zero delta; `--sections --agent warden` lists no fenced heading; `survivor-check f5cdd45..b4a9a1d`, `rider_check`, `claude_block --check` exit 0; ruff clean. Left to verify: every red the fix pass claims, and the seventeen new units. A finding located in a record (`rounds/`, `overview.md`, the JSON) is a correction — ⬜ with the coordinate — and stays out of `Needs a fix`. Runner: `bin/test tests/<module> -q` in a `uv` venv of the clone.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | a lent ratio entry drops the spawn it was measured from | `skills/verify/scripts/payload_meter.py:457-470`, `:573-590`, `:601-605` | answered | closed at `c75915b` — executed: real transcript against `payload-after.json` keeps 2.87, total `estimated`, delta +0/+0; against `payload-before.json` reproduces the committed after-file; the new case red at `f5cdd45` and red with the `spawn`-first read or `_carried` dropped |
| 🟡 2 | `--sections` splits at headings inside fences | `skills/verify/scripts/payload_meter.py:192-205` | answered | closed at `2dadb10` — executed: `--sections --agent warden` lists no fenced heading; case red at `f5cdd45` and with the toggle dropped |
| 🟡 3 | an inline `skills:` list reads as no skills | `skills/verify/scripts/payload_meter.py:169-180` | answered | closed at `2853caa` — executed: case red at `f5cdd45` and with the inline branch disabled |
| 🟡 4 | `--baseline-agent` refuses its own spelling | `skills/verify/scripts/payload_meter.py:392`, `:514` | answered | closed at `312a151` — executed: case red at `f5cdd45` and with `short_name` dropped in `calibration_of`; read: dropping it in `measure` fails the `baseline_agent == "probe"` assertion |
| 🟡 5 | the real-tree case passes over no agents | `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:237-238` | answered | closed at `63ae1a5` — executed: `agents_in` is `{}` on a root with no `agents/` and on one holding only `.txt`, so the assertion fires on both |
| 🟡 6 | `--write` rewrites every line ending | `.github/scripts/claude_block.py:110-128`, `:147`, `:190-195` | answered | closed at `8561bda` — executed: case red at `f5cdd45` and red with each of the three parts dropped alone |
| 🟡 7 | tracebacks under the wrapper's 3.9 | `skills/verify/scripts/payload_meter.py:83-110` | answered | closed at `a42a060` — executed: `/usr/bin/python3` 3.9.6 exits 2 with the sentence and no traceback; case red at `f5cdd45` and with the exit dropped; floor module 12 passed |
| ⬜ 8 | the delta heading did not name the file | `skills/verify/scripts/payload_meter.py:529-530`, `:815-819` | answered | closed at `c75915b` — executed: both file names render; `{}` and `""` fall back to `the baseline` |
| ⬜ 9 | *six rows* is five over six anchors | `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/overview.md:19-21` | answered | corrected at `b4a9a1d`; count carried from round 1 |
| ⬜ 10 | docstring named `CLAUDE.md` as the installer's source | `hooks/mode-gate.py:16-19` | answered | closed at `b4a9a1d` — read: `install.sh:48` reads the template |
| 🟡 12 | `_spawn_of`'s `from`-and-`tokens` arm — the one `payload-before.json` depends on — is pinned by no case; with it deleted the meter module stays green and the before-file re-derives 2.49 B/token, +982 tokens, total `measured` | `skills/verify/scripts/payload_meter.py:468-469`; `tests/test_the_payload_meter_says_what_it_measured.py:645-690` | **fixed** `dd539af` | fixed at dd539af — no new case; `test_a_lent_ratio_keeps_the_spawn_it_was_measured_from` gains a block that strips `spawn` from the derived entry before lending it and asserts the ratio kept, `tokens` absent, `spawn` and `over_bytes` restored, total estimated; executed — arm deleted: 22 passed; real transcript against `payload-before.json`: 2.49 with `tokens`, total 43,013 `measured (agent-ad1be2f4984b727e5.jsonl)`, delta −13,462 B / +982; the proposed case 1 passed at HEAD, 1 failed under the deletion |
| ⬜ 13 | the fence toggle does not know which fence it is in: a `##` inside ```` ``` ```` nested in ```` ```` ````, or between `~~~` inside a backtick fence, counts as a section, in the meter and in the check's copy of `FENCE` | `skills/verify/scripts/payload_meter.py:124`, `:198-205`; `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:48`, `:63-78` | **fixed** `0bf34f6` | fixed at 0bf34f6 — a fence closes only on a fence of the same character at least as long, in `payload_meter.py#heading_starts` and in the check's `marked_headings`; the two existing fence cases gain the nested shapes, no unit added; executed on six shapes — `~~~`, four-space and list-item fences correct; the three nested shapes wrong in both modules; the corpus holds no four-backtick and no `~~~` line, so no number in the tree is wrong today |
| ⬜ 14 | `Contract changes` lists two records as reach; the one call site is `render` at `payload_meter.py:783`, the records are prose and fenced code | `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/rounds/round-1.md:10` | answered | corrected at 108c33f — `rounds/round-1.md:10` reads `_baseline_name → render`; the two record paths were prose and fenced code |
| ⬜ 15 | `frontmatter` reads a trailing `#` comment or a flow list broken over two lines into the skill name | `skills/verify/scripts/payload_meter.py:169-180` | answered | each of the four `frontmatter` edge shapes surfaces as a `missing — named by skills:, not in the tree` row rather than silently, and no `agents/*.md` in the tree writes a comment or a broken flow list |
| ⬜ 16 | the floor module's pattern cannot see `itertools.pairwise` or `int \| float`, so it neither demands nor records the meter's guard | `tests/test_a_script_says_which_interpreter_it_needs.py:466-480` | answered | the floor module's pattern names `zip(…strict=` and `.UTC` only and its own comment names the blind spot; the meter's guard is pinned by its own case, and a pattern change is mechanism a fix pass may not add |
| ❓ 11 | whether `general-purpose`'s built-in prompt sits inside the harness constant | `skills/verify/scripts/payload_meter.py:35-42` | deferred questions.md Q4 | already deferred in round 1; not re-opened |

## Paste-ready fixes

```python
def test_a_baseline_written_before_spawn_existed_still_names_its_spawn(
    meter, tmp_path
):
    """`payload-before.json` was written before a ratio entry carried
    `spawn`: a derived entry names its spawn in `from` and marks itself a
    measurement with `tokens`. `_spawn_of` reads that shape too, and nothing
    pinned it — with that arm deleted every case here stayed green while the
    committed before-file re-derived 2.49 B/token over bytes its spawn never
    read, +982 tokens, and called the total measured (#292 round 2)."""
    root, home, transcript, before, before_path = _before_and_a_changed_tree(
        meter, tmp_path
    )
    kept = dict(before["ratios"]["probe"])
    assert "tokens" in kept and kept["from"] == "agent-bbbb2.jsonl"
    del before["ratios"]["probe"]["spawn"]
    with open(before_path, "w", encoding="utf-8") as handle:
        json.dump(before, handle)
    after = meter.measure(
        str(root), str(home), calibrate=transcript, baseline=before_path
    )
    ratio = after["ratios"]["probe"]
    assert ratio["bytes_per_token"] == kept["bytes_per_token"], ratio
    assert "tokens" not in ratio, "the old shape went unrecognised; re-derived"
    assert ratio["spawn"] == "agent-bbbb2.jsonl"
    assert ratio["over_bytes"] == kept["over_bytes"]
    assert after["agents"]["probe"]["total"]["basis"].startswith("estimated (")
```
```python
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


def heading_starts(text):
    """Offsets of every `##` / `###` heading outside a code fence. A fence
    closes only on a fence of the same character at least as long — the
    rule that keeps a ``` inside a ```` block, or a ~~~ inside a ``` block,
    from ending the outer one."""
    starts, offset, fence = [], 0, None
    for line in text.splitlines(keepends=True):
        opened = FENCE.match(line)
        if fence is None and opened:
            fence = opened.group(1)
        elif fence is not None and opened and opened.group(1)[0] == fence[0] and len(opened.group(1)) >= len(fence):
            fence = None
        elif fence is None and HEADING.match(line):
            starts.append(offset)
        offset += len(line)
    return starts
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_payload_meter_says_what_it_measured.py tests/test_the_claude_md_block_has_one_source.py tests/test_a_section_marked_for_one_role_reaches_only_that_role.py -q` in the clone | 49 passed |
| `.venv/bin/python -m pytest tests/test_a_script_says_which_interpreter_it_needs.py -q` | 12 passed |
| `/usr/bin/python3` (3.9.6) `skills/verify/scripts/payload_meter.py --sections --agent scribe` | exit 2; stderr names 3.12 and 3.9.6 and the interpreter path; no traceback |
| meter `--calibrate <the session's main transcript> --baseline payload-before.json --agent smith --json` | smith 2.87 `(lent — the same spawn, over other bytes)` with `spawn` `agent-ad1be2f4984b727e5.jsonl` and `over_bytes` 104,261; total 35,258 estimated; delta −13,462 B / −4,691 tokens; `baseline` = `payload-before.json` |
| the same against `payload-after.json` | 2.87 kept; total estimated; delta +0 B / +0 tokens; `baseline` = `payload-after.json` |
| meter `--sections --agent warden --json` | `agents/warden.md` sections: before-the-first-heading, `## Where you work`, `## Role`, `## Report` |
| `payload_meter.py` at `f5cdd45`, the five new meter cases | 5 failed |
| `claude_block.py` at `f5cdd45`, `test_write_keeps_the_targets_line_endings` | 1 failed |
| ten single-edit mutations at HEAD, each restored from git: `spawn`-first read dropped · `_carried` dropped · `from`+`tokens` arm dropped · fence toggle dropped · inline branch disabled · `short_name` dropped in `calibration_of` · guard exit dropped · `bare` compare dropped · `ending_of` dropped · `newline=""` dropped | 1 failed each, except the `from`+`tokens` arm: 22 passed over the whole meter module |
| the `from`+`tokens` arm dropped, real transcript against `payload-before.json` | smith 2.49 with `tokens`; total 43,013 `measured (…)`; delta −13,462 B / +982 tokens |
| the proposed case, a probe file run once and deleted, at HEAD and under the same deletion | 1 passed; 1 failed at `assert 0.01 == 0.02` |
| `heading_starts` on seven shapes; `marked_headings` on the four-backtick shape | `~~~`, four-space, list-item, unclosed: correct; four-backtick outer, `~~~` inside backticks, backticks inside `~~~`: inner heading counted, in both modules |
| `_spawn_of` / `_carried` on a derived entry without `spawn`, a pre-fix lent-same-spawn entry, a plain lent entry, `None`, a string | `from` / `None` / `None` / `None` / `None`; `_same_spawn_over_other_bytes` on the pre-fix lent shape with differing bytes → `None` |
| `frontmatter` on `[]`, `# none yet`, `- a  # first`, a two-line flow list | `[]`, `['# none yet']`, `['a  # first']`, `['[a']` |
| `agents_in` and `findings` on a root with no `agents/` and one holding only `n.txt` | `{}` / `[]` both |
| `grep` for ```` ```` ````, `~~~`, and fences indented four or more spaces over `agents/`, `skills/`, `CLAUDE.md`, `templates/claude-md-block.md` | none · none · two paired list-item fences |
| `grep _baseline_name` over the tree | one call site, `payload_meter.py:783`; the rest is record text |
| `git status --porcelain` after every restore | clean |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/payload_meter.py:382-392`, `:465`, `:491`; `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/payload-after.json` | round 1's 🔴 1 — fixed |
| round-1 | `skills/verify/scripts/payload_meter.py:137-160` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/payload_meter.py:110-128` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/scripts/payload_meter.py:313-351` | round 1's 🟡 4 — fixed |
| round-1 | `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:230-234` | round 1's 🟡 5 — fixed |
| round-1 | `.github/scripts/claude_block.py:103-108`, `:165-175`; `tests/test_the_claude_md_block_has_one_source.py:152` | round 1's 🟡 6 — fixed |
| round-1 | `bin/payload-meter:13`, `skills/verify/scripts/payload_meter.py:143`, `:376` | round 1's 🟡 7 — fixed |
| round-1 | `skills/verify/scripts/payload_meter.py:702-706` | round 1's ⬜ 8 — fixed |
| round-1 | `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/overview.md:19` | round 1's ⬜ 9 — answered |
| round-1 | `hooks/mode-gate.py:16-17` | round 1's ⬜ 10 — fixed |
| round-1 | `skills/verify/scripts/payload_meter.py:35-42` (the docstring's rule) | round 1's ❓ 11 — deferred |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the size of `general-purpose`'s built-in prompt | `questions.md` Q4, already there | the next session started in this repository |
