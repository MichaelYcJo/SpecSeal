# Round 3 — a payload is written again on every spawn (#292)

The verifying round after the run's one reopening. Target: the diff of round
2's fixes, `3486ce4..108c33f` (three commits), not the branch. Reviewed in a
`git clone --no-local` at `d096e62`, the commit that closes round 2, so both
closed records were in the clone; `bin/test` built the clone's `.venv` on
first call. Round 1's and round 2's coordinates were carried; every verdict
below is this round's own. The reopening is spent, so nothing here is a fix
to commission — one ⬜ is opened and it owes no issue.

## How the answers hang together

Both `fixed` verdicts are closed and each fix is load-bearing on its own: the
extended case goes red the moment the fix is taken back, at the assertion its
docstring points at, and it goes red on the round-1 shapes as well when the
fence tracking is removed altogether, so extending the cases made nothing
earlier vacuous. The three `answered` rows hold — each ground was opened
rather than taken. The one thing this round found is one level below finding
13: the new rule closes a fence on a same-character fence at least as long
even when that line carries an info string, which CommonMark reads as content.
No file the meter or the check reads has that shape, so it is a note.

## The two `fixed` verdicts, re-derived

Every row is executed. *Mutated* means one edit to the fix at HEAD made from a
Python script outside the clone, the pycache directories under
`skills/verify/scripts/` and `tests/` cleared, the named module run, both
files restored from git afterwards. `git status --porcelain` was clean after
the last restore.

| # | Mutation | Module | Red at | Closed? |
|---|---|---|---|---|
| 12 | `_spawn_of`'s `from`-and-`tokens` arm deleted | `tests/test_the_payload_meter_says_what_it_measured.py` | 1 failed, 21 passed — `test_a_lent_ratio_keeps_the_spawn_it_was_measured_from` at `:714`, `assert ratio["bytes_per_token"] == kept["bytes_per_token"]`; the ratio came back re-derived, `0.01` with `tokens: 10002` and `from: agent-bbbb2.jsonl` | yes — the new block is what fails, and for the docstring's reason: the old shape went unrecognised and the run re-derived |
| 13 | `heading_starts` back to the single toggle, new regex kept | the same module | 1 failed, 21 passed — `test_sections_do_not_split_at_a_heading_inside_a_fence` at `:741`; `## Inner example` and `## Tilde inside backticks` counted as sections | yes — both nested shapes the docstring names |
| 13 | `heading_starts` keeps the new rule, `FENCE` back to ```` (```|~~~) ```` | the same module | 1 failed — `:741`; `## Inner example` counted | yes — the regex is load-bearing on its own: a four-backtick opener read as three lets the inner ``` close it |
| 13 | `heading_starts` with no fence tracking at all | the same module | 1 failed — `:741`; `## Example`, `### Nested example`, `## Tilde example`, `## Inner example`, … counted | yes — the round-1 shapes still pin the case; nothing earlier in it went vacuous |
| 13 | `marked_headings` back to the single toggle, new regex kept | `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` | 1 failed, 8 passed — `test_a_marker_quoted_inside_a_code_fence_is_not_a_section` at `:200`, `assert findings(root) == []`; one finding naming the fenced marker | yes |
| 13 | `marked_headings` keeps the new rule, `FENCE` back to the old regex | the same module | 1 failed — `:200` | yes — same reason as the meter's |
| 13 | `marked_headings` with no fence tracking at all | the same module | 1 failed — `:200` | yes — the round-1 shape still pins it |

Round 1's 🟡 2 rested on `heading_starts`, which `0bf34f6` rewrote; the
third row above is that verdict re-derived, and it still holds. Nothing else
in the fix diff touches what round 2's other answers rested on, so those
stand as round 2 recorded them.

## The three `answered` rows, grounds opened

**14 — read.** `rounds/round-1.md:10` reads `_baseline_name → render` at
`108c33f`. `grep` over the tree's `.py` finds one call site,
`skills/verify/scripts/payload_meter.py:793`, and the definition at `:825`.
Holds.

**15 — executed.** `frontmatter` and `composition` on the four edge shapes,
each on a tree holding one real skill `a`: `skills: []` → no skill rows;
`skills: # none yet` → one row `skills/# none yet/SKILL.md` marked
`missing`; `- a  # first` → `skills/a  # first/SKILL.md` marked `missing`;
a flow list broken over two lines → `skills/[a/SKILL.md` marked `missing`.
Each renders as `missing — named by `skills:`, not in the tree`. The three
`agents/*.md` use the indented block form with no comment. Holds.

**16 — read.** `tests/test_a_script_says_which_interpreter_it_needs.py:466`
is `zip\(.*strict=|\b\w+\.UTC\b`, and the comment above it names the blind
spot as measured. The meter's `itertools.pairwise` (`:225`) and `int | float`
(`:462`) match neither arm. Holds.

## What this round opened

**⬜ 17 — a closing fence with an info string closes the block; CommonMark
reads it as content.** `payload_meter.py:207-212` and the check's copy at
`tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:71-77`
close on same character and length alone. CommonMark's closing fence may be
followed only by spaces, so on the shape ```` ``` ```` / ```` ```python ```` /
`## H` / ```` ``` ```` / `## Real` the meter lists `## H` and CommonMark
lists `## Real` (executed on that text). Executed over the 31 files the
meter and the check read — `agents/*.md`, every `.md` under `skills/`,
`CLAUDE.md`, `templates/claude-md-block.md` — against a copy of
`heading_starts` that also requires an empty tail: zero files differ. The
shape needs a document that nested a fence without widening the outer one,
which no file here does, so no number in the tree is wrong and the release
ships no defect on it. Recorded so the next person who widens the fence rule
knows the third condition; not owed an issue, and `Needs a fix` does not
count it.

## Read, not executed

- The extended `test_a_lent_ratio_keeps_the_spawn_it_was_measured_from`
  deep-copies `before` before stripping `spawn`, so `kept` — a reference into
  `before` — still carries the value the later assertions compare against.
- `heading_starts` never reads `fence[0]` while `fence` is `None`: the first
  branch takes every opener while no fence is open, so the second branch's
  `opened` is only truthy with a fence set. The check's copy has the same
  order.
- `round-2.md`'s `Fixes checked by` row still reads `nobody — the fixes are
  not yet written`; `round_record.py:49` sets the previous record's row to
  `round-N` when this round's record is written, so that is the flow and not
  a correction.

## Regression tests to plant

None. The two extended cases pin both fixes, shown above.

## Facts for the evidence ledger

- `skills/verify/scripts/payload_meter.py#heading_starts` — a fence closes
  only on a fence of the same character at least as long; a `##`/`###` line
  inside a ```` ``` ```` block nested in a ```` ```` ```` block, or between
  `~~~` inside a ```` ``` ```` block, is not a section.
- `skills/verify/scripts/payload_meter.py#_spawn_of` — a derived entry with
  `from` and `tokens` and no `spawn` names its spawn in `from`, so a baseline
  written before `spawn` existed is recognised as the same spawn.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 12 | `_spawn_of`'s `from`-and-`tokens` arm was pinned by no case | `skills/verify/scripts/payload_meter.py:479-480`; `tests/test_the_payload_meter_says_what_it_measured.py:700-718` | answered | closed at `dd539af` — executed: arm deleted, 1 failed / 21 passed, red at `:714` on `bytes_per_token`, the ratio re-derived to `0.01` with `tokens: 10002`; the docstring's reason |
| ⬜ 13 | the fence toggle did not know which fence it was in, in the meter and in the check | `skills/verify/scripts/payload_meter.py:125`, `:202-215`; `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:48`, `:63-85` | answered | closed at `0bf34f6` — executed: old toggle → meter case red at `:741` (`## Inner example`, `## Tilde inside backticks` counted), check case red at `:200`; old regex alone → red in both; no tracking at all → red in both on the round-1 shapes too |
| ⬜ 14 | `Contract changes` listed two records as reach | `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/rounds/round-1.md:10` | answered | read — the row reads `_baseline_name → render` at `108c33f`; one call site, `payload_meter.py:793` |
| ⬜ 15 | `frontmatter` reads a trailing `#` comment or a broken flow list into the skill name | `skills/verify/scripts/payload_meter.py:169-181` | answered | executed — the four shapes each render a `missing — named by skills:, not in the tree` row; the three `agents/*.md` use the indented block form |
| ⬜ 16 | the floor module's pattern cannot see `itertools.pairwise` or `int \| float` | `tests/test_a_script_says_which_interpreter_it_needs.py:466` | answered | read — the pattern is `zip\(.*strict=\|\b\w+\.UTC\b`, its comment names the blind spot; the meter's guard is pinned by `test_a_floor_above_this_interpreter_refuses_before_anything_is_read` |
| 🟡 2 (round 1) | `--sections` splits at headings inside fences | `skills/verify/scripts/payload_meter.py:193-215` | answered | re-derived because `0bf34f6` rewrote the unit it rested on — executed: fence tracking removed, the case is red on the round-1 shapes |
| ⬜ 17 | a closing fence carrying an info string closes the block, where CommonMark reads it as content, in the meter and in the check | `skills/verify/scripts/payload_meter.py:207-212`; `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:71-77` | open | executed — synthetic shape diverges; the 31 files the meter and check read: zero diverge; no defect ships, no issue owed |
| ❓ 11 | whether `general-purpose`'s built-in prompt sits inside the harness constant | `skills/verify/scripts/payload_meter.py:35-42` | deferred questions.md Q4 | already deferred in round 1; not re-opened |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_payload_meter_says_what_it_measured.py tests/test_a_section_marked_for_one_role_reaches_only_that_role.py -q` in the clone at `d096e62` | 31 passed |
| `_spawn_of`'s `from`-and-`tokens` arm deleted, pycache cleared, the meter module | 1 failed, 21 passed — `:714`, `bytes_per_token` re-derived to `0.01`, `tokens: 10002` |
| `heading_starts` back to the single toggle, the meter module | 1 failed — `:741`, `## Inner example` and `## Tilde inside backticks` counted |
| `heading_starts` with the old `FENCE` regex, the meter module | 1 failed — `:741`, `## Inner example` counted |
| `heading_starts` with no fence tracking, the meter module | 1 failed — `:741`, every fenced heading counted |
| `marked_headings` back to the single toggle, the check module | 1 failed, 8 passed — `:200` |
| `marked_headings` with the old `FENCE` regex, the check module | 1 failed — `:200` |
| `marked_headings` with no fence tracking, the check module | 1 failed — `:200` |
| `git checkout --` on both files after each mutation; `git status --porcelain` | clean each time |
| `frontmatter` and `composition` on `skills: []`, `skills: # none yet`, `- a  # first`, a two-line flow list | `[]`, `['# none yet']`, `['a  # first']`, `['[a']`; each non-empty one a `missing` row |
| `heading_starts` against a copy requiring an empty tail on the closer, over `agents/*.md`, `skills/**/*.md`, `CLAUDE.md`, `templates/claude-md-block.md` | 31 files, 0 diverge |
| the same pair on ```` ``` ```` / ```` ```python ```` / `## H` / ```` ``` ```` / `## Real` | meter `['## H']`, CommonMark copy `['## Real']` |
| `grep _baseline_name` over the tree's `.py` | `payload_meter.py:793` (call), `:825` (def) |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the size of `general-purpose`'s built-in prompt | `questions.md` Q4, already there | the next session started in this repository |

Needs a fix: no
Loses a record or crashes: no

The run ends on this answer: both `fixed` verdicts are closed, the three
`answered` rows hold, and the one thing opened is a ⬜. The broad gate is
`not yet` in both closed records and has now come due.

## Proof block — files opened

- `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/rounds/round-2.md`, `round-2-report.md`, `round-2-fixes.md`, `round-1.md` (lines 1-113)
- `git diff 3486ce4..108c33f`, whole
- `skills/verify/scripts/payload_meter.py`, whole
- `tests/test_the_payload_meter_says_what_it_measured.py` — the `def` index and lines 560-760
- `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py` — lines 40-110, 180-215
- `tests/test_a_script_says_which_interpreter_it_needs.py` — lines 455-490
- `agents/scribe.md`, `agents/smith.md`, `agents/warden.md` — the `skills:` blocks
- `skills/code-review/scripts/round_record.py` — the `Fixes checked by` lines (grep)
- `docs/review-chain-spec.md` — the reopening lines (grep)
- `skills/code-review/SKILL.md` — the findings-format lines (grep)
- `bin/test`
