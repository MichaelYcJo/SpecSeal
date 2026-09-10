# Round 2 — a payload is written again on every spawn (#292)

The verifying round. Target: the diff of round 1's fixes, `f5cdd45..b4a9a1d`
(eight commits), not the branch. Reviewed in a `git clone --no-local` at
`179a9a8`, the commit on top of `b4a9a1d` that closes round 1, so
`rounds/round-1.md` was in the clone; `bin/test` built the clone's `.venv`
on first call. Round 1's coordinates were carried; every verdict below is
this round's own.

## How the answers hang together

Nine `fixed` verdicts, and all nine are closed: each new case goes red with
its script reverted to `f5cdd45`, and each fix goes red under the mutation
round 1's grounds describe — ten mutations, ten reds, with one exception.
That exception is the one finding this round opens. `_spawn_of` has two
arms, and only the first is pinned: delete the second — the one that reads a
derived entry's spawn out of `from` when `tokens` marks it a measurement —
and every planted case stays green while the committed
`payload-before.json`, which is exactly that shape, puts round 1's 2.49
B/token and `measured` back on the smith row. The fix is right; nothing
holds it there. Everything else this round was asked — the seventeen new
units, the two shapes named in the prompt, the `Contract changes` reach —
held or is a correction to a record, and is written up as such.

## The nine closures, re-derived

Every row is executed. *Reverted* means the whole script at `f5cdd45` with
the new case run against it; *mutated* means one edit to the fix at HEAD,
the pinned case run, the file restored from git afterwards. The tree was
clean after every restore.

| # | Fix | Reverted | Mutated as the grounds describe | Closed? |
|---|---|---|---|---|
| 1 | every ratio entry carries `spawn` and `over_bytes`; `_spawn_of` reads `spawn` first | red | drop the `spawn`-first read → red; drop `_carried` in the plain lent branch → red | yes — real transcript against `payload-after.json`: 2.87 kept, total `estimated`, delta +0 B / +0 tokens; against `payload-before.json`: the committed after-file reproduced, −13,462 B / −4,691 tokens, smith entry carrying `spawn` and `over_bytes` 104,261 |
| 2 | `heading_starts` tracks fences | red | drop the fence toggle → red | yes — `--sections --agent warden` lists `Where you work`, `Role`, `Report` and nothing from the fenced template |
| 3 | `frontmatter` reads an inline list | red | disable the inline branch → red | yes |
| 4 | `short_name` in `calibration_of` and `measure` | red | drop it in `calibration_of` → red; dropping it in `measure` alone fails the `baseline_agent == "probe"` assertion by reading | yes |
| 5 | the real-tree case asserts `agents_in(ROOT)` first | — | `agents_in` on a root with no `agents/` and on one holding only a `.txt` → `{}` both, so the new assertion fires on both shapes round 1 found | yes |
| 6 | `newline=""`, `bare`, `ending_of` in `claude_block.py` | red | drop the `bare` compare → red; drop `ending_of` in `write` → red; drop `newline=""` on read → red | yes — each of the three parts is load-bearing for the one case |
| 7 | the floor guard copied from `round_record.py` | red | drop the `raise SystemExit(2)` block → red | yes — `/usr/bin/python3` (3.9.6) on `--sections --agent scribe`: exit 2, the sentence names 3.12 and 3.9.6, no traceback; `tests/test_a_script_says_which_interpreter_it_needs.py` 12 passed |
| 8 | `measure` records `baseline`, `render` reads it | (folded into 1) | — | yes — `## Delta against payload-before.json` and `... payload-after.json` both rendered; `_baseline_name` on `{}`, `{"baseline": ""}` → `the baseline` |
| 10 | `hooks/mode-gate.py` docstring names the template | read | — | yes — `install.sh:48` reads `templates/claude-md-block.md`; the repository `CLAUDE.md` is the generated copy the docstring says it is |

Finding 9 (`overview.md`, five rows over six anchors) is a record
correction; the sentence at `overview.md:19-21` now reads that way. Carried
from round 1's count rather than re-counted.

## The seventeen new units, judged as code

**`_spawn_of` — one arm pinned, one not (🟡 12).** The first arm returns
`spawn`. The second returns `from` when `tokens` says the entry is a
measurement. The committed `payload-before.json` has neither `spawn` nor a
lent suffix — three derived entries with `from` and `tokens` — so the second
arm is what lets the same-spawn rule recognise the before-file at all. With
that arm deleted (executed): the whole meter module, 22 passed; the real
transcript against `payload-before.json`, smith at 2.49 B/token with a
`tokens` key, total 43,013 `measured (agent-ad1be2f4984b727e5.jsonl) …`,
delta −13,462 B / **+982** tokens. That is round 1's finding 1, on the file
this branch commits as its before-number. The new case
`test_a_lent_ratio_keeps_the_spawn_it_was_measured_from` cannot see it
because its `before` is written by the fixed meter and carries `spawn`. A
case that strips `spawn` from the derived entry before lending it is under
*Paste-ready fixes*; shown green at HEAD and red under the same mutation
(`assert 0.01 == 0.02`).

**The prompt's shape — a baseline with neither `spawn` nor `tokens`.**
Executed on the three shapes: a derived entry without `spawn` → its `from`;
a pre-`c75915b` lent-same-spawn entry (`from` names the file, `over_bytes`,
no `tokens`, no `spawn`) → `None`, and `_same_spawn_over_other_bytes` on it
with differing bytes → `None`, so the run re-derives. Round 1's finding 1
therefore still reproduces against a JSON written by the meter between
`3523022` and `c75915b` with a lent-same-spawn row. No committed file has
that shape — the after-file was regenerated — and no released meter wrote
one (the meter ships first in 0.10.0), so this is recorded as a probe result
and not as a finding.

**`_carried`.** Correct: returns `spawn` when `_spawn_of` finds one and
`over_bytes` when it is an `int`, nothing else. On a plain-lent entry with
neither it returns `{}` and the lent row is written as before.

**`heading_starts`, `FENCE` — right for the shapes the prompt named, wrong
one level down (⬜ 13).** Executed: a `~~~` fence, a fence indented four
spaces, and a fence inside a list item each hide the heading between them.
The toggle does not know which fence it is in, so a heading inside a
three-backtick block that is itself inside a four-backtick block, or a `## `
line between `~~~` inside a backtick fence (and the reverse), is counted as
a section. `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:48`
holds the same regex and `marked_headings` gives the same answer on the
four-backtick shape. The corpus the meter and the check read has no
four-backtick line and no `~~~` line (executed, `grep` over `agents/`,
`skills/`, `CLAUDE.md`, the template); the only indented fences are two
list-item pairs at `skills/implement/orchestration.md:80-82` and
`skills/evidence-ci/SKILL.md:55-57`, both tracked correctly. So the number
is right for every file in the tree today, and a fix is offered rather than
required.

**`bare`, `ending_of`.** Correct for the file shapes here: `bare("a\r\r\n")`
→ `a`; `ending_of` is CRLF when any line is and LF for an empty list. A
target mixing endings gets its block written in CRLF, which is a choice, not
a defect. `templates/claude-md-block.md` and `CLAUDE.md` hold no CR and no
other `splitlines` boundary character (executed), and `.gitattributes` pins
`eol=lf`, so the CRLF path is the `autocrlf` checkout the docstring names.

**The floor guard (`FLOOR`, `FLOOR_TEXT`, `BELOW_FLOOR`, `below_floor`,
`_refusal`).** A faithful copy of `round_record.py:170-198` with the program
name changed; it sits after five stdlib imports and before `HERE`, and the
3.9 run proves nothing above it needs 3.10. One thing to know, not to fix
(⬜ 16): `tests/test_a_script_says_which_interpreter_it_needs.py:466` finds
above-floor scripts by a pattern that matches `zip(…strict=` and `.UTC`
only, so the meter's `itertools.pairwise` and `int | float` are invisible to
it — the module neither demands the guard nor can list the meter under
`CLASSIFIED` (its `gone` assertion refuses a row the pattern does not find).
The meter's guard is inventoried by its own case and nowhere else.

**The six cases.** Each went red against its script at `f5cdd45` (five in
the meter module, one in the block module). `test_a_floor_above_this_interpreter_refuses_before_anything_is_read`
asserts its substitution matched and that the missing root is never named,
which is the right pair. `test_the_baseline_agent_may_be_named_with_its_namespace`
pins both halves of fix 4. `test_write_keeps_the_targets_line_endings` flips
the last byte of `## Tooling` (`g` → `h`), so the flip stays ASCII. The gap
is the one named under 🟡 12.

**`frontmatter` edges (⬜ 15).** Executed: `skills: []` → `[]`; `skills: #
none yet` → one skill named `# none yet`; `- a  # first` → `a  # first`; a
flow list broken over two lines → `['[a']`. Every one surfaces as a
`missing — named by skills:, not in the tree` row rather than silently, and
no agent definition in the tree writes a comment or a broken flow list
(`agents/*.md` all use the indented block form). Noted, not owed.

## The `Contract changes` reach (⬜ 14)

`_baseline_name → round-1-report.md, round-1.md, render`. Opened: the one
call site is `render`, `skills/verify/scripts/payload_meter.py:783`. The two
record paths are text — `rounds/round-1.md:99` is the paste-ready fence
that carried the new body, `rounds/round-1-report.md:253` and `:430` are the
prose that named the old one and the fence that proposed the new. The row
reads as three callers and has one; a correction to the record's
`rounds/round-1.md:10`, out of `Needs a fix`.

## Read, not executed

- `payload-after.json`'s `spawns` went 6 → 7 for smith and 1 → 2 for
  warden because the transcript it was regenerated from now holds the
  round-1 warden and the fix-pass smith. The smallest prefix is still the
  calibration spawn in both rows, and the numbers the changelog and the
  pull request carry did not move — the real run above reproduces them.
- The delta basis against `payload-before.json` reads *summed over the
  files — the earlier total was measured and this one is estimated*; that
  is the sentence the round-1 record wanted and it is what renders.

## Regression tests to plant

| Case | Destination | Pins |
|---|---|---|
| `test_a_baseline_written_before_spawn_existed_still_names_its_spawn` (NAME NOT IN TREE) | `tests/test_the_payload_meter_says_what_it_measured.py`, after `test_a_lent_ratio_keeps_the_spawn_it_was_measured_from` | `_spawn_of`'s `from`-and-`tokens` arm, the one `payload-before.json` needs |

## Facts for the evidence ledger

- `skills/verify/scripts/payload_meter.py#_spawn_of` — a ratio entry names
  its spawn in `spawn`, or in `from` only where `tokens` marks it a
  measurement; a lent entry's `from` is never read as a spawn.
- `skills/verify/scripts/payload_meter.py#heading_starts` — a `##`/`###`
  line inside a fence opened by ```` ``` ```` or `~~~` at any indentation
  is not a section.
- `.github/scripts/claude_block.py#write` — the block takes the target's
  line ending, and a target already carrying the block under either ending
  is left unwritten.

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
| 🟡 12 | `_spawn_of`'s `from`-and-`tokens` arm — the one `payload-before.json` depends on — is pinned by no case; with it deleted the meter module stays green and the before-file re-derives 2.49 B/token, +982 tokens, total `measured` | `skills/verify/scripts/payload_meter.py:468-469`; `tests/test_the_payload_meter_says_what_it_measured.py:645-690` | open | executed — arm deleted: 22 passed; real transcript against `payload-before.json`: 2.49 with `tokens`, total 43,013 `measured (agent-ad1be2f4984b727e5.jsonl)`, delta −13,462 B / +982; the proposed case 1 passed at HEAD, 1 failed under the deletion |
| ⬜ 13 | the fence toggle does not know which fence it is in: a `##` inside ```` ``` ```` nested in ```` ```` ````, or between `~~~` inside a backtick fence, counts as a section, in the meter and in the check's copy of `FENCE` | `skills/verify/scripts/payload_meter.py:124`, `:198-205`; `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:48`, `:63-78` | open | executed on six shapes — `~~~`, four-space and list-item fences correct; the three nested shapes wrong in both modules; the corpus holds no four-backtick and no `~~~` line, so no number in the tree is wrong today |
| ⬜ 14 | `Contract changes` lists two records as reach; the one call site is `render` at `payload_meter.py:783`, the records are prose and fenced code | `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/rounds/round-1.md:10` | open | read — `grep` over the tree; correction to the record, out of `Needs a fix` |
| ⬜ 15 | `frontmatter` reads a trailing `#` comment or a flow list broken over two lines into the skill name | `skills/verify/scripts/payload_meter.py:169-180` | open | executed on four shapes; each surfaces as a `missing` row, not silently; no `agents/*.md` writes either |
| ⬜ 16 | the floor module's pattern cannot see `itertools.pairwise` or `int \| float`, so it neither demands nor records the meter's guard | `tests/test_a_script_says_which_interpreter_it_needs.py:466-480` | open | read; the module's own comment names the blind spot; the meter's guard is pinned by its own case |
| ❓ 11 | whether `general-purpose`'s built-in prompt sits inside the harness constant | `skills/verify/scripts/payload_meter.py:35-42` | deferred questions.md Q4 | already deferred in round 1; not re-opened |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the size of `general-purpose`'s built-in prompt | `questions.md` Q4, already there | the next session started in this repository |

## Paste-ready fixes

🟡 12 — after `test_a_lent_ratio_keeps_the_spawn_it_was_measured_from` in
`tests/test_the_payload_meter_says_what_it_measured.py`; green at HEAD, red
with `_spawn_of`'s second arm deleted:

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

⬜ 13 — offered, not owed; the same edit belongs in the check's copy at
`tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:48-78`
(§12, one class in two files):

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

Needs a fix: yes — 🟡 12, the case above, unless answered with grounds
Loses a record or crashes: no

## Proof block — files opened

- `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/rounds/round-1.md`, `round-1-report.md`, `round-1-fixes.md`, `round-2-asked.md`, `spec.md`, `payload-before.json`, `payload-after.json` (via the diff), `overview.md` (via the diff)
- `git diff f5cdd45..b4a9a1d`, whole
- `skills/verify/scripts/payload_meter.py` — lines 70-125, 145-225, 300-330, 380-470, 500-640, 800-840
- `.github/scripts/claude_block.py` — lines 85-215
- `skills/code-review/scripts/round_record.py` — lines 168-198
- `bin/payload-meter`, `install.sh` (grep), `.gitattributes`
- `tests/test_the_payload_meter_says_what_it_measured.py` — the new cases, `_before_and_a_changed_tree`, the helper index
- `tests/test_the_claude_md_block_has_one_source.py` — the new case (via the diff)
- `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` — lines 43-90, 230-238
- `tests/test_a_script_says_which_interpreter_it_needs.py` — lines 455-525 and the `def`/`FLOOR` index
- `skills/implement/orchestration.md` — lines 76-84
- `agents/scribe.md`, `agents/smith.md`, `agents/warden.md` — the `skills:` blocks
- `hooks/mode-gate.py` — lines 13-21 (via the diff)
