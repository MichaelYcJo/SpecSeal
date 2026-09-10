# Round 1 — a payload is written again on every spawn (#292)

Target SHA `3523022`, branch `perf/292-a-payload-is-written-again-on-every-spawn`,
base `release/v0.10.0`, draft pull request #329. Reviewed in a `git clone
--no-local` at the target; the repository's own runner (`bin/test`) built the
clone's `.venv` on first call. No earlier round.

## How the findings hang together

The meter's whole claim is *every token figure carries a basis*, and the
branch's own phase 4 found the one way that claim broke — a spawn's measured
tokens divided by bytes it never read — and fixed it for one hop. Finding 1
is that same defect one hop later, on the path #120 is told to take. Findings
2 to 4 are three more places the meter reads something silently as a smaller
thing than it is (a fenced heading as a section, an inline `skills:` list as
no list, a namespaced baseline name as an unspawned agent). Findings 5 to 7
are the check and the block script: one can pass over nothing, one rewrites
what it says it never touches, one crashes below the floor its sibling in the
same branch guards against. Everything else the round was asked — the split,
the 21 re-pointed cases, the eight ledger rows, the numbers — held under
execution and is recorded as such below.

## Stage 1 — the spec, S1 to S8

| Scenario | Held? | How |
|---|---|---|
| S1 composition | yes | read — `composition`, `render`; executed — the module's 17 cases, 43 passed with the other two new modules |
| S2 measured beside estimated | **partly** | executed — the refusal on a transcript naming no baseline agent holds (`calibration_of:351`); executed — the chained baseline re-derives a ratio over bytes the spawn did not read and labels the total `measured` (finding 1); executed — the refusal also fires on the baseline agent's own namespaced spelling (finding 4) |
| S3 before and after | yes, as the memo records it | executed — `--calibrate` + `--baseline payload-before.json` in the clone reproduces `payload-after.json`: smith −13,462 B, −4,691 tokens summed over the files; the S3 sum clause is recorded as a divergence in `overview.md` with grounds I re-derived (32,522 + 16,545 = 49,067 against 46,249; the excess is the header, the pointer section and one reworded bullet) |
| S4 the check can fail | yes, with a hole | executed — `findings()` on `git archive fc50702` names exactly the three marked headings for `smith`; `4e9c31c` and `471cd69` are clean; executed — a tree with no `agents/*.md` passes the real-tree case (finding 5) |
| S5 the split | yes | read — `orchestration.md:1-274` against the spec's cut by paragraph; details below |
| S6 the re-pointed cases | yes | executed — seven mutations planting a forbidden sentence back into `SKILL.md` (and one into `orchestration.md`), each case red, 64 passed on the restored tree |
| S7 one source for the block | yes, with one platform hole | executed — `install.sh` against a scratch target holding a stale block between user text above and below; block byte-identical to the template, both sides kept, `.bak` written; `claude_block.py --check` exit 0; executed — `--write` on a CRLF target rewrites every line ending (finding 6) |
| S8 nothing asks anyone | yes | read — no `AskUserQuestion`, no `input(` in the three new files; the check pins the second |

## Findings from execution

### 1. The lent ratio drops the spawn it was measured from, so #120's first `--calibrate` re-derives 2.49 B/token and calls it measured — 🔴

`skills/verify/scripts/payload_meter.py:382-392` (`_same_spawn_over_other_bytes`)
recognises the earlier run only when the baseline's ratio entry has
`from` equal to the spawn file. Phase 4 wrote that entry for the derived case
alone. The lent-same-spawn branch at `:465` writes `from` as the sentence
`payload-before.json (lent — the same spawn, over other bytes)`, and the plain
lent branch at `:491` writes neither the spawn nor `over_bytes`. So the
spawn's identity survives exactly one hop.

Executed in the clone, with the real calibration transcript and the committed
`payload-after.json` as the baseline — the shape #120 is told to run, since
its before-number is this work item's after-number:

```
ratios.smith: {"bytes_per_token": 2.49, "from": "agent-ad1be2f4984b727e5.jsonl",
               "tokens": 36295, "over_bytes": 90534}
smith total:  43,013 tokens, basis "measured (agent-ad1be2f4984b727e5.jsonl) …"
delta total:  {"bytes": 0, "tokens": +5381}
delta skills/implement/SKILL.md: {"bytes": 0, "tokens": +1729}
render:       "Ratio 2.49 B/token: 90,534 bytes the spawn read over 36,295 tokens"
```

That is the defect `6ddfa69` fixed, reproduced one hop later: +5,381 tokens
with zero bytes changed, a row saying the spawn read bytes it never read, and a
total labelled `measured`. The class is *every entry shape a baseline can
carry*: derived (carries the spawn), lent-same-spawn (loses it), lent (loses
it and the byte count). The fix carries `spawn` and `over_bytes` through all
three and reads `spawn` first. The committed `payload-after.json` has to be
regenerated after the fix, from the same transcript and `payload-before.json`,
so that it carries the spawn; the orchestrator holds that transcript.

Found by reading; reproduced by execution. Paste-ready fix below.

### 2. `--sections` splits at headings inside code fences, while the check one file over reads a fence as a quotation — 🟡

`payload_meter.py:137-160` (`sections_of`) finds `HEADING` matches over the
whole text. `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:63-77`
(`marked_headings`) tracks fences and skips them, and its docstring says why:
a skill quotes headings as examples, and an example is not a section.
Executed, `--sections --agent warden` on the real tree:

```
agents/warden.md: ['(before the first heading)', '## Where you work', '## Role',
                   '## Report', '## Verdicts', '## Executed probes', '## Deferred',
                   '## Paste-ready fixes']
```

The last four are the fenced report template inside `## Report`. #120 reads
`--sections` to decide what to trim, so a phantom section with a real byte
count is a number that sends a reader to cut a fenced example. Paste-ready fix
below shares the fence rule.

### 3. An inline `skills:` list reads as no skills, silently — 🟡

`payload_meter.py:110-128` (`frontmatter`) reads a block sequence only.
Executed:

```
'skills:'  + '  - a' '  - b'  -> ['a', 'b']
'skills: [a, b]'               -> []
'skills: a, b'                 -> []
```

A flow sequence is valid YAML for the same field. The meter then reports the
definition as its whole payload, and the check — which reads the list through
the same parser — has nothing to check. Q6 (a) ships the meter for users' own
definitions, which is where the other spelling arrives. Paste-ready fix below
reads the inline form.

### 4. `--baseline-agent` refuses the spelling its own refusal prints — 🟡

`payload_meter.py:313-351`: `seen` is keyed by `short_name(kind)` and the
refusal lists `subagent_type` values; `baseline_agent` is compared raw.
Executed on the real transcript:

```
--baseline-agent specseal:scribe -> REFUSED: … never spawned the baseline agent
                                    `specseal:scribe` … it spawned …, specseal:scribe, …
--baseline-agent scribe          -> ok, baseline 46,056
```

Paste-ready fix below normalises the name once.

### 5. The real-tree check passes over a tree with no agents — 🟡

`tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:230-234`
asserts `findings(ROOT) == []`. `findings` derives its agents from
`agents_in`, which returns `{}` for a missing `agents/` or one with no `.md`.
Executed: both shapes return `[]`, so the case is green over nothing. On this
tree `agents_in` names the three; the property `CONTRIBUTING.md` asks of a
gate is that it can fail, and this one cannot fail in the shape a deleted
directory gives it. Paste-ready fix below asserts what was read.

### 6. `claude_block.py --write` rewrites every line ending of the target, outside the block included — 🟡

`.github/scripts/claude_block.py:103-108` reads with newline translation and
`:173` writes with it, so the bytes written are the platform's ending for every
line, not the target's. Executed on macOS with a CRLF copy of `CLAUDE.md` (a
Windows checkout with `autocrlf=true`):

```
--check on the CRLF copy: exit 0
--write after a one-byte flip: exit 0 | CRLF lines before: 153, after: 0
bytes outside the block changed: True
```

The docstring and `tests/test_the_claude_md_block_has_one_source.py:152`
(`test_write_restores_the_copy_and_touches_nothing_outside_the_markers`) say
the region alone is touched; the case compares through universal newlines, so
it cannot see this. On Windows the same code turns an LF file into CRLF. A
contributor on that platform who runs the one command the check's message
names gets a whole-file diff. Paste-ready fix below keeps the target's ending.

### 7. Under the interpreter `bin/payload-meter` invokes, `--sections` and `--baseline` end in a traceback — 🟡

`bin/payload-meter:13` runs `python3`, which on macOS is the 3.9.6 shim.
`payload_meter.py:143` uses `itertools.pairwise` and `:376` `int | float`, both
3.10. Executed with `/usr/bin/python3`:

```
payload-meter --agent scribe             -> exit 0
payload-meter --agent scribe --sections  -> AttributeError: module 'itertools' has no attribute 'pairwise'
payload-meter --agent scribe --baseline  -> TypeError: unsupported operand type(s) for |
```

`claude_block.py` in this same branch copied `round_record.py`'s floor guard
for exactly this. `tests/test_a_script_says_which_interpreter_it_needs.py`
passes over the meter because its patterns do not name these two constructs.
The sibling `session_cost.py` carries the same exposure, deferred to #226 —
grounds a smith can answer with, or the two-line spelling below removes the
crash without a guard.

## Findings from reading

### The split — `spec.md` §Scope item 3, checked by paragraph

- **Out of `SKILL.md`, in full:** Bootstrap and Parity setup — moved, text
  unchanged except the bullet phase 4 reworded (`orchestration.md:43-45`),
  which names `skills/implement/SKILL.md` §2 where it said *below*. Correct:
  the feedback rule is §2 of the other file.
- **Out of §1, the span:** from *How this work is routed is one of them* up to
  *Once the batch is answered* — moved (`orchestration.md:151-273`). The
  axis table, the checkbox table, the two `routing.md` commands, the four
  combinations, the wake/quiet table, the `straight to the PR` sentence, the
  branch table, the gather sentence and the standing-waiver paragraph are all
  there and nowhere in `SKILL.md`.
- **Stays, merged:** the waiver paragraph, `SKILL.md` §1 *A waiver is one
  command's, and it is the implementer's* — carries `[no-review]`, *one
  command* against *a work item*, the no-declaration behaviour, the front-of-
  command form and `[no-parity]`, and names `orchestration.md` instead of a
  table the reader cannot see. `test_the_skill_keeps_the_token_as_a_per_command_waiver`
  still reads it there, green.
- **The rider:** answered at `orchestration.md:221-228` — *never wakes the
  PARITY arm* and *costs nothing even in a migration repository*; the
  `# RIDER:` is gone and `rider_check.py` exits 0 (executed).
- **Nothing an implementer acts on left, nothing orchestrator-only stayed:**
  `grep` over `SKILL.md` for `AskUserQuestion`, `multiSelect`, `spawn`,
  `routing.md`, `orchestrat` finds the pointer section, the file-set tree,
  the merged waiver paragraph, the two §2 pointers and the records table —
  each a reference, none a procedure. The one-batch rule, the two sharpeners
  and the yes/no tell stay in §1 as the spec says. One judgment call the spec
  made and I note rather than contest: the gather sentence (*basing on `main`
  means running the gather*) is advice to whoever writes the changelog entry,
  and `agents/smith.md:80-83` carries the same rule for the smith, so nothing
  the smith needs left its payload.
- **Cross-references:** no `§1` remains in either file. `SKILL.md:282-283`
  and `:288-290` name `orchestration.md` for the declaration and the
  wake/quiet table. Outside the skill, every `§1` reference (`CLAUDE.md:35`,
  `CONTRIBUTING.md:84`, `hooks/mode-gate.py:37`, `templates/sdd-routing.md:4`,
  `docs/review-chain-spec.md:484,513`, three test docstrings) points at the
  one-batch rule or the yes/no tell, which stayed. `hooks/mode-gate.py:16-17`
  still says the preset block in `CLAUDE.md` is what `install.sh` copies —
  since phase 3 it copies the template. Prose in a docstring; ⬜.

### The 21 re-pointed cases

Read against the diff of the eight modules. Every absence assertion that
used to read `SKILL.md` alone now reads both halves
(`both_halves()` in `test_first_setup_asks_once.py`; the two-file loops in
`test_waiver_decided_at_start.py` and `test_one_word_one_meaning.py`), and
`test_the_release_target_is_asked_before_the_work_starts` reads the two
concatenated because it pins a moved sentence and a staying one. Executed:
planting *nowhere else*, the old *no marker at all* row, *two axes*, the
*Do not write that config row* sentence and `.git/seal/` back into
`SKILL.md` each turned its case red; `.git/seal/` planted in
`orchestration.md` did too; 64 passed on the restored tree. Not vacuous.

### The eight ledger rows and the five re-verified

Each of the eight claims in `seal/ledger/1788993115-….md` was read against
`orchestration.md:26-132`: S14 (three lines, opt-in, mode then parity, nothing
else — `:114-127`), S4/S12 (one question, two options, shared first, the
common-dir spelling, either place not asked — `:65-93,129-132`), Q7 (0.3.x
told, not asked — `:54-63`), S5/🟡4 (the one-line version read — `:76-82`),
🟡1/🟡4/r3 1 (the file names `templates/ledger.md`, `templates/hygiene.yml`,
`templates/parity.md`), r3 4 (clause tables arrive empty — `:33`), S7
(`/specseal:config` as the way back — `:124-127`), S11/S12 (the block's
sentence precedes the write instruction, and the bootstrap runs `seal mode` —
`:101`). All hold. Executed: `bin/evidence-check .` in the clone, 1,059 ok ·
0 drifted · 0 broken · 0 refused. The rows re-verified in `seal/ledger.md`
are five rows over six anchors — the README row carries two — where
`overview.md:19` says *six rows*; ⬜ paperwork.

### The numbers

`changelog.md` and the pull request body against the two JSON files: 46,249 −
32,522 = 13,727 B; 16,115 − 11,332 = 4,783 tokens; the pair 10,482 − 10,217 =
265 B and 3,652 − 3,560 = 92; 13,727 − 265 = 13,462 B and 4,783 − 92 = 4,691;
114,650 − 13,462 = 101,188 B. The three ratios 2.87 / 3.41 / 3.44 are
104,261 / 36,295, 84,181 / 24,702 and 22,598 / 6,568. The spec's six prefix
totals match `payload-before.json`'s calibration block (baseline 39,488;
smith 75,783 over 3 spawns, warden 64,190 over 1, scribe 46,056 over 2). All
consistent. The delta heading in the after-run's own render reads `## Delta
against the baseline` rather than naming `payload-before.json`, because
`_baseline_name` (`payload_meter.py:702-706`) looks for a `(lent)` suffix the
same-spawn entry does not carry; ⬜, folded into fix 1.

### Windows paths

Read: every key and display path goes through `.replace(os.sep, "/")`
(`agents_in`, `composition`), the check builds `rel` with forward slashes,
`delta_against` keys on the display path, `by_id` on basenames, and the
committed JSON carries `root: "."` and transcript basenames only. No `os.sep`
reaches a key. Not executed on Windows.

### The shadow

Read, and confirmed by my own spawn: `writing-style` arrived in this
session's context with the base directory `/Users/x/.claude/skills/writing-style`,
the user's copy, while `agent-contract` arrived from the plugin cache. The
meter's rule (`composition`, `~/.claude/skills/<name>/SKILL.md` shadows the
tree's) matches what the harness did here.

### Phase 1's open item — ❓ out of verified scope

Whether `general-purpose`'s built-in prompt is small enough to sit inside the
harness constant the meter subtracts. Settling it takes a spawn, which
contract §6 keeps out of my hands. What can be read: the scribe's 6,568-token
delta over 22,598 B (3.44 B/token) is consistent with English prose only if
that prompt is small, and says nothing about how small. Answerer: Q4's probe
in the next session, as `overview.md` already names.

## Regression tests to plant

- `tests/test_the_payload_meter_says_what_it_measured.py` —
  `test_a_lent_ratio_keeps_the_spawn_it_was_measured_from` (NAME NOT IN TREE):
  calibrate → before; change the tree; calibrate + baseline=before → after;
  calibrate + baseline=after → the ratio is still the kept one, `tokens` is
  absent, the note is present. Red on `3523022`.
- same file — `test_sections_do_not_split_at_a_heading_inside_a_fence` (NAME NOT IN TREE):
  a fixture skill with a fenced `## Example`; `--sections` lists no such
  section and the pieces still sum to the file.
- same file — `test_an_inline_skills_list_is_read` (NAME NOT IN TREE): a
  definition with `skills: [alpha, beta]` measures both files.
- same file — `test_the_baseline_agent_may_be_named_with_its_namespace` (NAME NOT IN TREE):
  `calibration_of(transcript, "plugin:probe")` succeeds.
- `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` — the
  real-tree case asserts `agents_in(ROOT)` is non-empty before asserting the
  findings are; a planted case `findings()` on an empty root is reported as
  such rather than as clean, if the fix goes into `findings`.
- `tests/test_the_claude_md_block_has_one_source.py` —
  `test_write_keeps_the_targets_line_endings` (NAME NOT IN TREE): a CRLF
  target, `--check` exit 0, `--write` after a flip, CRLF count unchanged and
  the bytes after the end marker identical.

## Facts for the evidence ledger

- `payload_meter.py#_same_spawn_over_other_bytes` recognises the earlier run
  by the spawn file alone; a baseline written by a lent run carries no spawn
  file (executed: 2.49 B/token, +5,381 tokens over 0 bytes, on the second hop).
- `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py#findings`
  at `fc50702` names the three marked headings for `smith`; at `4e9c31c` and
  `471cd69` it names nothing (executed from `git archive` trees).
- `install.sh` against a target holding a stale block between user text keeps
  both sides and replaces the block with the template's bytes (executed).
- `bin/evidence-check .` at `3523022`: 1,059 ok · 0 drifted · 0 broken
  (executed, my own run, agreeing with the orchestrator's).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | a lent ratio entry drops the spawn it was measured from, so a second `--calibrate` against the after-number re-derives the ratio over bytes the spawn never read and labels the total measured | `skills/verify/scripts/payload_meter.py:382-392`, `:465`, `:491`; `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/payload-after.json` | open | executed — `--calibrate <transcript> --baseline payload-after.json --agent smith`: 2.49 B/token, +5,381 tokens over 0 bytes, `measured (agent-ad1be2f4984b727e5.jsonl)` on the total |
| 🟡 2 | `--sections` splits at headings inside code fences; the check in the same branch reads a fence as a quotation | `skills/verify/scripts/payload_meter.py:137-160` | open | executed — `--sections --agent warden` lists `## Verdicts`, `## Executed probes`, `## Deferred`, `## Paste-ready fixes` from the fenced template in `agents/warden.md` |
| 🟡 3 | an inline `skills:` list reads as no skills, silently, in the meter and in the check that shares its parser | `skills/verify/scripts/payload_meter.py:110-128` | open | executed — `skills: [a, b]` → `[]`, `skills: a, b` → `[]` |
| 🟡 4 | `--baseline-agent` compares the raw name against short names, refusing the spelling the refusal itself prints | `skills/verify/scripts/payload_meter.py:313-351` | open | executed — `specseal:scribe` refused, `scribe` accepted, on the real transcript |
| 🟡 5 | the real-tree case passes over a tree with no `agents/*.md` | `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:230-234` | open | executed — `findings()` returns `[]` for a root with no `agents/` and for one with no `.md` in it |
| 🟡 6 | `--write` rewrites every line ending of the target, outside the block included, and the case that says otherwise compares through universal newlines | `.github/scripts/claude_block.py:103-108`, `:165-175`; `tests/test_the_claude_md_block_has_one_source.py:152` | open | executed — CRLF copy of `CLAUDE.md`: 153 CRLF lines before `--write`, 0 after; bytes after the end marker changed |
| 🟡 7 | under the `python3` the wrapper invokes (3.9 on macOS), `--sections` and `--baseline` end in a traceback rather than the floor sentence its sibling script copied | `bin/payload-meter:13`, `skills/verify/scripts/payload_meter.py:143`, `:376` | open | executed — `/usr/bin/python3` 3.9.6: plain run exit 0, `--sections` AttributeError, `--baseline` TypeError |
| ⬜ 8 | the after-run's delta heading reads *against the baseline* rather than naming the file, because only a `(lent)` suffix is recognised | `skills/verify/scripts/payload_meter.py:702-706` | open | executed — render of `--calibrate` + `--baseline payload-before.json`; folded into fix 1 |
| ⬜ 9 | *six rows left in `seal/ledger.md`* is five rows over six anchors | `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/overview.md:19` | open | read — the `seal/ledger.md` diff rehashes five rows; the README row carries two anchors |
| ⬜ 10 | the docstring still says `install.sh` copies the block out of `CLAUDE.md` | `hooks/mode-gate.py:16-17` | open | read — `install.sh:48` reads `templates/claude-md-block.md` since `d6305b4` |
| ❓ 11 | whether `general-purpose`'s built-in prompt sits inside the harness constant | `skills/verify/scripts/payload_meter.py:35-42` (the docstring's rule) | open | out of verified scope — needs a spawn, which contract §6 forbids this agent; answerer: Q4's probe in the next session |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| without `--baseline` the meter cannot tell a stale transcript from a fresh one | `questions.md` Q8, already there | the repository owner |
| the exact token count of one file, and the size of `general-purpose`'s built-in prompt | `questions.md` Q4, already there | the next session started in this repository, with the three probe definitions |
| `session_cost.py` runs under 3.9 with no floor guard, the same exposure as finding 7 | `seal/follow-up.md` (#226), already there | the owner of #226 |

## Paste-ready fixes

🔴 1 — `skills/verify/scripts/payload_meter.py`, replace `_same_spawn_over_other_bytes` and carry `spawn` in all three ratio entries:

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

And for ⬜ 8 in the same pass — record the baseline's name once and read it:

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

(with `out["baseline"] = out_baseline` set where `out` is built, when a
baseline was given.) Then regenerate `payload-after.json` from the same
transcript and `payload-before.json`, so the committed file carries `spawn`.

🟡 2 — `skills/verify/scripts/payload_meter.py`, `sections_of` reads fences the way the check does:

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

(the rest of `sections_of` unchanged; `HEADING` loses `re.MULTILINE`, which a
per-line match no longer needs.)

🟡 3 — `skills/verify/scripts/payload_meter.py`, `frontmatter` reads the inline form:

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

🟡 4 — `skills/verify/scripts/payload_meter.py`, `calibration_of` normalises the name it is given:

```python
def calibration_of(transcript, baseline_agent):
    """Measured prefixes per agent from one main transcript's spawns.

    Several spawns of one agent take the SMALLEST prefix: a first message
    holds the payload plus the spawn prompt, and the prompt only adds.
    `baseline_agent` may be spelled with or without its namespace."""
    baseline_agent = short_name(baseline_agent)
    helpers = _session_cost()
```

and in `measure`, before `out` is built: `baseline_agent = short_name(baseline_agent)`.

🟡 5 — `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`, the real-tree case asserts what it read:

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

🟡 6 — `.github/scripts/claude_block.py`, keep the target's own line ending:

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

(`quote()` keeps `rstrip("\n")`; make it `rstrip("\r\n")` so a CRLF line is
quoted without its carriage return. The docstring's *no branch for a prefix*
reasoning is unchanged.)

🟡 7 — `skills/verify/scripts/payload_meter.py`, the two constructs spelled for the interpreter the wrapper reaches:

```python
    for begin, end in zip(bounds, bounds[1:]):
```

```python
    if isinstance(entry, dict) and isinstance(
        entry.get("bytes_per_token"), (int, float)
    ):
```

(or the floor guard `claude_block.py:38-70` carries, copied after the
imports, if the answer is that the meter is a 3.12 tool — then `bin/payload-meter`
should say so the way that guard does rather than through a traceback.)

Needs a fix: yes — 🔴 1 (the chained baseline re-derives a ratio over bytes the spawn never read and labels the total measured), and 🟡 2–7 unless answered with grounds
Loses a record or crashes: no — finding 7 is a traceback below the repository's stated interpreter floor, on a command that writes no record, and its sibling carries the same exposure deferred to #226; nothing leaves the root

## Proof block — files opened

- `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/`: `spec.md`, `plan.md`, `questions.md`, `overview.md`, `routing.md`, `survivors.md`, `changelog.md`, `payload-before.json`, `payload-after.json`, `phases/phase-1.md` … `phase-4.md`
- `seal/ledger/1788993115-a-payload-is-written-again-on-every-spawn.md`; the diff of `seal/ledger.md`
- `skills/verify/scripts/payload_meter.py` (all), `skills/verify/scripts/session_cost.py` (`spawn_labels`, `subagent_transcripts`, `count`, `DELEGATING`)
- `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py`, `tests/test_the_payload_meter_says_what_it_measured.py`, `tests/test_the_claude_md_block_has_one_source.py` (all three in full); the diffs of `tests/test_chain_hooks_hardening.py`, `tests/test_docs_line_wrap.py`, `tests/test_first_setup_asks_once.py`, `tests/test_one_word_one_meaning.py`, `tests/test_release_hygiene.py`, `tests/test_review_axes.py`, `tests/test_the_mode_question_is_asked_once.py`, `tests/test_the_settings_have_a_front_door.py`, `tests/test_waiver_decided_at_start.py`; `tests/test_the_set_a_work_item_always_has.py:40-110`; `tests/test_a_script_says_which_interpreter_it_needs.py` (its `CLASSIFIED` region)
- `skills/implement/orchestration.md` (all), the diff of `skills/implement/SKILL.md` and its §1 as it stands; `skills/code-review/SKILL.md` was not re-read
- `.github/scripts/claude_block.py` (all); the diffs of `.github/workflows/hygiene.yml`, `install.sh` (and `install.sh:1-40,60-140`), `templates/claude-md-block.md`, `CLAUDE.md`, `README.md`, `README.ko.md`, `hooks/mode-gate.py`, `docs/flow.md`, `skills/preset-setup/SKILL.md`, `skills/update/SKILL.md`, `bin/payload-meter`, `bin/payload-meter.cmd`; `bin/session-cost`; `templates/sdd-routing.md`; `agents/scribe.md`, `agents/smith.md`, `agents/warden.md` (frontmatter)
- the session's main transcript under `~/.claude/projects/` (the `agentId:` lines and one subagent's first `usage` block, read-only)
- pull request #329's body, via `gh`
