# 1788993115-a-payload-is-written-again-on-every-spawn — review round 1

| Field | Value |
|---|---|
| Target SHA | 3523022 |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 329 |
| Broad gate | not yet |
| Fixes checked by | round-2 |
| Contract changes | _baseline_name → render |
| New units | bare (depth 1); ending_of (depth 1); FLOOR (depth 1); FLOOR_TEXT (depth 1); BELOW_FLOOR (depth 1); below_floor (depth 1); _refusal (depth 1); FENCE (depth 1); heading_starts (depth 1); _spawn_of (depth 1); _carried (depth 1); test_write_keeps_the_targets_line_endings (depth 1); test_a_lent_ratio_keeps_the_spawn_it_was_measured_from (depth 1); test_sections_do_not_split_at_a_heading_inside_a_fence (depth 1); test_an_inline_skills_list_is_read (depth 1); test_the_baseline_agent_may_be_named_with_its_namespace (depth 1); test_a_floor_above_this_interpreter_refuses_before_anything_is_read (depth 1) |
| Needs a fix | yes — 🔴 1 (the chained baseline re-derives a ratio over bytes the spawn never read and labels the total measured), and 🟡 2–7 unless answered with grounds |
| Loses a record or crashes | no — finding 7 is a traceback below the repository's stated interpreter floor, on a command that writes no record, and its sibling carries the same exposure deferred to #226; nothing leaves the root |
<!-- New units: seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/payload-after.json read by the diff-line heuristic and not by the AST -->

- [x] Pass

## What this round was asked

Round 1 of #292 at `3523022`, the whole branch `perf/292-a-payload-is-written-again-on-every-spawn` against `release/v0.10.0` (43 files, +4,512 / −334), draft pull request #329. The change claims `spec.md` S1–S8. Three classes to enumerate for this change: a section addressed to one role sitting in another role's payload (the corpus the new check reads, and whether the cut in `spec.md` §Scope item 3 left an implementer's sentence in `orchestration.md` or an orchestrator's in `SKILL.md`); a token figure whose basis does not say where it came from (the meter's rule that every figure is `measured` or `estimated (<ratio>, from <agent>)` — look for a path that prints a bare number, and for a ratio derived over bytes a spawn did not read); and a case that lost its ability to fail when it was re-pointed (21 cases across 8 modules now read `orchestration.md`, some by concatenating two files — a `not in` over a concatenation is the shape to try). In this order: `skills/verify/scripts/payload_meter.py`, and first its two phase-4 units `_same_spawn_over_other_bytes` and `delta_against`, which nobody has reviewed, then `--calibrate`'s pairing of an `Agent` tool_use to `subagents/agent-<id>.jsonl` through the tool_result text, the baseline subtraction, the `~/.claude/skills` shadow detection, and Windows paths since CI runs windows-latest; `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` — can it pass vacuously on an empty glob, does it read fences as prose, does it read `###` as well as `##`; the split itself — the merged waiver paragraph in `SKILL.md`, the rider's answer in `orchestration.md` (the PARITY arm, a migration repository), and every `§1`/`(§1)` cross-reference in either file; the 21 re-pointed cases; `.github/scripts/claude_block.py` with the hygiene step and `install.sh` against a target holding a stale block; the eight rows in `seal/ledger/1788993115-….md` at their new coordinate and the six rows re-verified in `seal/ledger.md`; and last the numbers in `changelog.md` and the pull request body against `payload-before.json` and `payload-after.json`. Facts handed over as executed: the six calibration spawns in `spec.md` §Measured (prefix totals 39,488 · 46,056 · 46,056 · 64,190 · 75,783 · 75,783); the re-verification at `3523022` — 430 passed over the touched modules, `evidence-check .` 1,059 ok · 0 drifted · 0 broken, `survivor-check`, `rider_check`, `claude_block --check` and `unverified-check` all exit 0, ruff clean. Left to verify: everything the smith's four phase records claim was seen red, and whether `general-purpose`'s own prompt is small enough to sit inside the harness constant (phase 1's open item). Runner: `bin/test tests/<module> -q` in a `uv` venv of the clone.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | a lent ratio entry drops the spawn it was measured from, so a second `--calibrate` against the after-number re-derives the ratio over bytes the spawn never read and labels the total measured | `skills/verify/scripts/payload_meter.py:382-392`, `:465`, `:491`; `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/payload-after.json` | **fixed** `c75915b` | fixed at c75915b — every ratio entry carries `spawn` and `over_bytes`; `_spawn_of` reads `spawn` first; `payload-after.json` regenerated from the same transcript, −13,462 B / −4,691 tokens unchanged; executed — `--calibrate <transcript> --baseline payload-after.json --agent smith`: 2.49 B/token, +5,381 tokens over 0 bytes, `measured (agent-ad1be2f4984b727e5.jsonl)` on the total |
| 🟡 2 | `--sections` splits at headings inside code fences; the check in the same branch reads a fence as a quotation | `skills/verify/scripts/payload_meter.py:137-160` | **fixed** `2dadb10` | fixed at 2dadb10 — `heading_starts` tracks fences the way the check does; executed — `--sections --agent warden` lists `## Verdicts`, `## Executed probes`, `## Deferred`, `## Paste-ready fixes` from the fenced template in `agents/warden.md` |
| 🟡 3 | an inline `skills:` list reads as no skills, silently, in the meter and in the check that shares its parser | `skills/verify/scripts/payload_meter.py:110-128` | **fixed** `2853caa` | fixed at 2853caa — `frontmatter` reads an inline list, a bare comma list and an unindented block list; executed — `skills: [a, b]` → `[]`, `skills: a, b` → `[]` |
| 🟡 4 | `--baseline-agent` compares the raw name against short names, refusing the spelling the refusal itself prints | `skills/verify/scripts/payload_meter.py:313-351` | **fixed** `312a151` | fixed at 312a151 — `short_name` applied in `calibration_of` and in `measure`; executed — `specseal:scribe` refused, `scribe` accepted, on the real transcript |
| 🟡 5 | the real-tree case passes over a tree with no `agents/*.md` | `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:230-234` | **fixed** `63ae1a5` | fixed at 63ae1a5 — the real-tree case asserts `agents_in(ROOT)` is non-empty first; executed — `findings()` returns `[]` for a root with no `agents/` and for one with no `.md` in it |
| 🟡 6 | `--write` rewrites every line ending of the target, outside the block included, and the case that says otherwise compares through universal newlines | `.github/scripts/claude_block.py:103-108`, `:165-175`; `tests/test_the_claude_md_block_has_one_source.py:152` | **fixed** `8561bda` | fixed at 8561bda — lines read with `newline=""`, blocks compared without endings, `--write` keeps the target's ending; executed — CRLF copy of `CLAUDE.md`: 153 CRLF lines before `--write`, 0 after; bytes after the end marker changed |
| 🟡 7 | under the `python3` the wrapper invokes (3.9 on macOS), `--sections` and `--baseline` end in a traceback rather than the floor sentence its sibling script copied | `bin/payload-meter:13`, `skills/verify/scripts/payload_meter.py:143`, `:376` | **fixed** `a42a060` | fixed at a42a060 — the interpreter floor guard copied from `round_record.py`, so a 3.9 `python3` gets the sentence and exit 2; executed — `/usr/bin/python3` 3.9.6: plain run exit 0, `--sections` AttributeError, `--baseline` TypeError |
| ⬜ 8 | the after-run's delta heading reads *against the baseline* rather than naming the file, because only a `(lent)` suffix is recognised | `skills/verify/scripts/payload_meter.py:702-706` | **fixed** `c75915b` | fixed at c75915b — `measure` records the baseline file and `render` names it for every entry shape; executed — render of `--calibrate` + `--baseline payload-before.json`; folded into fix 1 |
| ⬜ 9 | *six rows left in `seal/ledger.md`* is five rows over six anchors | `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/overview.md:19` | answered | corrected at b4a9a1d — `overview.md` reads five rows over six anchors, the README row carrying two |
| ⬜ 10 | the docstring still says `install.sh` copies the block out of `CLAUDE.md` | `hooks/mode-gate.py:16-17` | **fixed** `b4a9a1d` | fixed at b4a9a1d — `hooks/mode-gate.py`'s docstring names `templates/claude-md-block.md`; read — `install.sh:48` reads `templates/claude-md-block.md` since `d6305b4` |
| ❓ 11 | whether `general-purpose`'s built-in prompt sits inside the harness constant | `skills/verify/scripts/payload_meter.py:35-42` (the docstring's rule) | deferred questions.md Q4 | questions.md Q4 |

## Paste-ready fixes

```python
def _same_spawn_over_other_bytes(baseline_data, name, spawn_file, seen_bytes):
    """The bytes the baseline's ratio was measured over, when this run's
    smallest spawn for `name` is that very spawn and the tree's bytes differ
    from them — or None when the two agree or the baseline knows nothing.
    `spawn` is read first: a lent entry's `from` names the file it was lent
    from, and the spawn behind it has to survive every hop."""
    entry = ((baseline_data or {}).get("ratios") or {}).get(name)
    if not isinstance(entry, dict):
        return None
    if (entry.get("spawn") or entry.get("from")) != spawn_file:
        return None
    over = entry.get("over_bytes")
    if isinstance(over, int) and over != seen_bytes:
        return over
    return None
```
```python
                if lent is not None:
                    ratio, origin = lent, f"{name} in {base_name}"
                    out["ratios"][name] = {
                        "bytes_per_token": ratio,
                        "from": f"{base_name} (lent — the same spawn, over other bytes)",
                        "spawn": entry["from"],
                        "over_bytes": read_over,
                        "shadowed": shadowed,
                    }
            elif delta > 0:
                ratio = round(seen_bytes / delta, 2)
                origin = name
                out["ratios"][name] = {
                    "bytes_per_token": ratio,
                    "from": entry["from"],
                    "spawn": entry["from"],
                    "tokens": delta,
                    "over_bytes": seen_bytes,
                    "shadowed": shadowed,
                }
```
```python
        if ratio is None:
            lent = _ratio_from_baseline(baseline_data, name)
            if lent is not None:
                ratio = lent
                origin = f"{name} in {os.path.basename(baseline)}"
                carried = (baseline_data.get("ratios") or {}).get(name) or {}
                out["ratios"][name] = {
                    "bytes_per_token": ratio,
                    "from": f"{os.path.basename(baseline)} (lent)",
                    **{k: carried[k] for k in ("spawn", "over_bytes") if k in carried},
                }
```
```python
    if baseline:
        with open(baseline, encoding="utf-8") as handle:
            baseline_data = json.load(handle)
        out_baseline = os.path.basename(baseline)
```
```python
def _baseline_name(data):
    return data.get("baseline") or "the baseline"
```
```python
FENCE = re.compile(r"^\s*(```|~~~)")


def heading_starts(text):
    """Offsets of every `##` / `###` heading outside a code fence. A skill
    quotes headings as examples, and an example is not a section — the same
    rule `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`
    applies before it reads a marker."""
    starts, offset, fenced = [], 0, False
    for line in text.splitlines(keepends=True):
        if FENCE.match(line):
            fenced = not fenced
        elif not fenced and HEADING.match(line):
            starts.append(offset)
        offset += len(line)
    return starts


def sections_of(text):
    """The file split at its `##` / `###` headings, each piece's own size.
    The pieces sum to the file: every byte belongs to exactly one."""
    starts = heading_starts(text)
    bounds = [0, *starts, len(text)]
```
```python
    for line in block.splitlines():
        if re.match(r"^name:\s*\S", line):
            name = line.split(":", 1)[1].strip()
            in_skills = False
        elif re.match(r"^skills:\s*\S", line):
            # `skills: [a, b]` and `skills: a, b` — one line, read as a list
            # rather than as no list at all.
            inline = line.split(":", 1)[1].strip()
            if inline.startswith("[") and inline.endswith("]"):
                inline = inline[1:-1]
            skills.extend(
                s.strip().strip("'\"") for s in inline.split(",") if s.strip()
            )
            in_skills = False
        elif re.match(r"^skills:\s*$", line):
            in_skills = True
        elif in_skills and re.match(r"^\s*-\s*\S", line):
            skills.append(line.split("-", 1)[1].strip())
        elif re.match(r"^\S", line):
            in_skills = False
```
```python
def calibration_of(transcript, baseline_agent):
    """Measured prefixes per agent from one main transcript's spawns.

    Several spawns of one agent take the SMALLEST prefix: a first message
    holds the payload plus the spawn prompt, and the prompt only adds.
    `baseline_agent` may be spelled with or without its namespace."""
    baseline_agent = short_name(baseline_agent)
    helpers = _session_cost()
```
```python
def test_no_agent_preloads_a_section_marked_for_the_orchestrator():
    """Red between the commit that marked `implement`'s three sections and
    the one that moved them (`phases/phase-2.md` names both). The agents are
    asserted first: a tree with no `agents/*.md` has nothing to check, and a
    check over nothing is green over nothing."""
    agents = _meter().agents_in(ROOT)
    assert agents, "no agents/*.md was read — the check would pass over nothing"
    found = findings(ROOT)
    assert found == [], "\n".join(found)
```
```python
def read_lines(path, what):
    try:
        with open(path, encoding="utf-8", newline="") as f:
            return f.read().splitlines(keepends=True)
    except OSError as exc:
        raise NoBlock(f"cannot read the {what} at {shown(path)}: {exc}") from exc


def bare(line):
    """The line without its ending, which is what two copies are compared
    on: a CRLF checkout carries the same block as an LF one."""
    return line.rstrip("\r\n")


def ending_of(lines):
    return "\r\n" if any(line.endswith("\r\n") for line in lines) else "\n"


def first_difference(wanted, found):
    for i in range(min(len(wanted), len(found))):
        if bare(wanted[i]) != bare(found[i]):
            return i, wanted[i], found[i]
    return None
```
```python
def write(template_path, target_path, out):
    wanted = block(read_lines(template_path, "template"))
    target = read_lines(target_path, "target")
    first, last = region(target)
    template, copy = shown(template_path), shown(target_path)
    wanted = [bare(line) + ending_of(target) for line in wanted]
    if target[first : last + 1] == wanted:
        out.write(f"{NAME}: {copy} already carries the block; nothing written\n")
        return 0
    with open(target_path, "w", encoding="utf-8", newline="") as f:
        f.write("".join(target[:first] + wanted + target[last + 1 :]))
    out.write(f"{NAME}: wrote the block from {template} into {copy}\n")
    return 0
```
```python
    for begin, end in zip(bounds, bounds[1:]):
```
```python
    if isinstance(entry, dict) and isinstance(
        entry.get("bytes_per_token"), (int, float)
    ):
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_section_marked_for_one_role_reaches_only_that_role.py tests/test_the_payload_meter_says_what_it_measured.py tests/test_the_claude_md_block_has_one_source.py -q` | 43 passed |
| `bin/test tests/test_a_script_says_which_interpreter_it_needs.py -q` | 12 passed — the meter is neither guarded nor classified there |
| `bin/evidence-check .` in the clone at `3523022` | exit 0; 1,059 ok · 0 drifted · 0 broken · 0 refused |
| `python3 .github/scripts/rider_check.py`; `python3 .github/scripts/claude_block.py --check` | both exit 0 |
| `bash install.sh <scratch>/CLAUDE.md` where the file held user text, a stale block (`## Tooling (old)`, one rule removed), user text | exit 0; block byte-identical to the template; text above and below kept; `CLAUDE.md.bak` written |
| meter `measure(root=clone, calibrate=<the session's main transcript>, baseline=payload-after.json, agents=smith)` | ratio 2.49 from `agent-ad1be2f4984b727e5.jsonl`, total basis `measured (…)`, delta +5,381 tokens over 0 bytes (finding 1) |
| the same with `baseline=payload-before.json` | reproduces `payload-after.json`: smith lent 2.87, total 35,258 estimated, delta −13,462 B / −4,691 tokens; heading `## Delta against the baseline` (⬜ 8) |
| `calibration_of(transcript, "specseal:scribe")` / `("scribe")` | refused / accepted (finding 4) |
| `findings()` on a root with no `agents/`, and on one with `agents/notes.txt` only | `[]` both (finding 5) |
| `measure(root=clone, agents=warden, sections=True)` | `agents/warden.md` sections include the four fenced headings (finding 2) |
| `frontmatter()` on four `skills:` spellings | block list read; `[a, b]`, `a, b` and an unindented block list read as `[]` (finding 3) |
| `findings()` on `git archive` trees of `fc50702`, `4e9c31c`, `471cd69` | 3 findings naming `smith` and `skills/implement/SKILL.md` / 0 / 0 — phase 2's red-on-the-real-tree claim holds |
| `claude_block.py --check` then `--write` on a CRLF copy of `CLAUDE.md` with one byte flipped | check exit 0; write exit 0, 153 CRLF lines → 0, bytes outside the block changed (finding 6) |
| seven mutations: *nowhere else*, the old `no marker at all` row, *two axes*, *Do **not** write that config row here*, `` `.git/seal/` `` planted into `skills/implement/SKILL.md`; `` `.git/seal/` `` into `orchestration.md`; each case run alone | 1 failed each; 64 passed over the three modules on the restored tree |
| `/usr/bin/python3` (3.9.6) `payload_meter.py --agent scribe` / `--sections` / `--baseline payload-before.json` | exit 0 / AttributeError / TypeError (finding 7) |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| without `--baseline` the meter cannot tell a stale transcript from a fresh one | `questions.md` Q8, already there | the repository owner |
| the exact token count of one file, and the size of `general-purpose`'s built-in prompt | `questions.md` Q4, already there | the next session started in this repository, with the three probe definitions |
| `session_cost.py` runs under 3.9 with no floor guard, the same exposure as finding 7 | `seal/follow-up.md` (#226), already there | the owner of #226 |
