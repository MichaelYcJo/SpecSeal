# 1788993115-a-payload-is-written-again-on-every-spawn — review round 3

| Field | Value |
|---|---|
| Target SHA | d096e62 |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 329 |
| Broad gate | 75fc6d1 against 401ccc4 |
| Fixes checked by | no fixes to check |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of #292 is the verifying round after the one reopening the run allows, at the diff of round 2's fixes, `3486ce4..108c33f` (three commits: a pin extended into an existing case, the nested-fence rule in both `heading_starts` and the check's `marked_headings`, and a one-cell correction to `rounds/round-1.md`). Its job is the answers: for the two `fixed` verdicts in `rounds/round-2.md` (12 and 13), is each actually closed — re-derive by deleting `_spawn_of`'s `from`-and-`tokens` arm and by restoring the old fence toggle in each module, and say which case goes red; and for the three `answered` rows (14, 15, 16), do the grounds hold. `New units` reads `none`, so there is no unreviewed unit surface this time; the extended cases are the changed surface, and the question for each is whether it still fails for the reason its docstring gives. This round is bounded by `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped*: it reports anything it opens as a `deferred #N` candidate rather than as a fix to commission, and `Needs a fix: no` is what ends the run. Facts handed over as executed by the orchestrator at `108c33f`: 116 passed over five modules; `survivor-check 3486ce4..108c33f`, `rider_check` exit 0; ruff clean on the three Python files. Runner: `bin/test tests/<module> -q` in a `uv` venv of the clone.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 12 | `_spawn_of`'s `from`-and-`tokens` arm was pinned by no case | `skills/verify/scripts/payload_meter.py:479-480`; `tests/test_the_payload_meter_says_what_it_measured.py:700-718` | answered | closed at `dd539af` — executed: arm deleted, 1 failed / 21 passed, red at `:714` on `bytes_per_token`, the ratio re-derived to `0.01` with `tokens: 10002`; the docstring's reason |
| ⬜ 13 | the fence toggle did not know which fence it was in, in the meter and in the check | `skills/verify/scripts/payload_meter.py:125`, `:202-215`; `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:48`, `:63-85` | answered | closed at `0bf34f6` — executed: old toggle → meter case red at `:741` (`## Inner example`, `## Tilde inside backticks` counted), check case red at `:200`; old regex alone → red in both; no tracking at all → red in both on the round-1 shapes too |
| ⬜ 14 | `Contract changes` listed two records as reach | `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/rounds/round-1.md:10` | answered | read — the row reads `_baseline_name → render` at `108c33f`; one call site, `payload_meter.py:793` |
| ⬜ 15 | `frontmatter` reads a trailing `#` comment or a broken flow list into the skill name | `skills/verify/scripts/payload_meter.py:169-181` | answered | executed — the four shapes each render a `missing — named by skills:, not in the tree` row; the three `agents/*.md` use the indented block form |
| ⬜ 16 | the floor module's pattern cannot see `itertools.pairwise` or `int \| float` | `tests/test_a_script_says_which_interpreter_it_needs.py:466` | answered | read — the pattern is `zip\(.*strict=\|\b\w+\.UTC\b`, its comment names the blind spot; the meter's guard is pinned by `test_a_floor_above_this_interpreter_refuses_before_anything_is_read` |
| 🟡 2 | `--sections` splits at headings inside fences | `skills/verify/scripts/payload_meter.py:193-215` | answered | re-derived because `0bf34f6` rewrote the unit it rested on — executed: fence tracking removed, the case is red on the round-1 shapes |
| ⬜ 17 | a closing fence carrying an info string closes the block, where CommonMark reads it as content, in the meter and in the check | `skills/verify/scripts/payload_meter.py:207-212`; `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:71-77` | answered | a closing fence carrying an info string is read as a closer where CommonMark reads it as content; executed over the 31 files the meter and the check read, zero diverge, so no number in the tree is wrong and no defect ships — recorded as the third condition the next widening of the fence rule has to carry, and owed no issue |
| ❓ 11 | whether `general-purpose`'s built-in prompt sits inside the harness constant | `skills/verify/scripts/payload_meter.py:35-42` | deferred questions.md Q4 | already deferred in round 1; not re-opened |

## Paste-ready fixes

no paste-ready fix in the report

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
| round-2 | `skills/verify/scripts/payload_meter.py:457-470`, `:573-590`, `:601-605` | round 2's 🔴 1 — answered |
| round-2 | `skills/verify/scripts/payload_meter.py:192-205` | round 2's 🟡 2 — answered |
| round-2 | `skills/verify/scripts/payload_meter.py:169-180` | round 2's 🟡 3 — answered |
| round-2 | `skills/verify/scripts/payload_meter.py:392`, `:514` | round 2's 🟡 4 — answered |
| round-2 | `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:237-238` | round 2's 🟡 5 — answered |
| round-2 | `.github/scripts/claude_block.py:110-128`, `:147`, `:190-195` | round 2's 🟡 6 — answered |
| round-2 | `skills/verify/scripts/payload_meter.py:83-110` | round 2's 🟡 7 — answered |
| round-2 | `skills/verify/scripts/payload_meter.py:529-530`, `:815-819` | round 2's ⬜ 8 — answered |
| round-2 | `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/overview.md:19-21` | round 2's ⬜ 9 — answered |
| round-2 | `hooks/mode-gate.py:16-19` | round 2's ⬜ 10 — answered |
| round-2 | `skills/verify/scripts/payload_meter.py:468-469`; `tests/test_the_payload_meter_says_what_it_measured.py:645-690` | round 2's 🟡 12 — fixed |
| round-2 | `skills/verify/scripts/payload_meter.py:124`, `:198-205`; `tests/test_a_section_marked_for_one_role_reaches_only_that_role.py:48`, `:63-78` | round 2's ⬜ 13 — fixed |
| round-2 | `seal/specs/1788993115-a-payload-is-written-again-on-every-spawn/rounds/round-1.md:10` | round 2's ⬜ 14 — answered |
| round-2 | `tests/test_a_script_says_which_interpreter_it_needs.py:466-480` | round 2's ⬜ 16 — answered |
| round-2 | `skills/verify/scripts/payload_meter.py:35-42` | round 2's ❓ 11 — deferred |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| the size of `general-purpose`'s built-in prompt | `questions.md` Q4, already there | the next session started in this repository |
