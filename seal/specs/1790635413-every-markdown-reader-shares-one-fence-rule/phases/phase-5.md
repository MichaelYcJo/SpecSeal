# 1790635413-every-markdown-reader-shares-one-fence-rule — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | ee193db3 |
| Ran by | unknown — the spawn prompt did not name the agent and model, and the segment does not source that value from itself |

## What this phase was asked

`plan.md` phase 5: `payload_meter.py#heading_starts` and
`tests/test_a_section_marked_for_one_role_reaches_only_that_role.py#headings`
on `fence_opener` / `fence_closes`; `payload_meter.py#FENCE` and the test's
`FENCE` retire; the meter's missing reader exits 2 with a sentence. Verified
by S12 and S18's row for this script, with Q2 answered before the fix.

## What this phase found

- **Q2, measured before the fix.** A probe compared the meter's old
  `heading_starts` with a walk over `fence_spans` across all 482 tracked
  `.md` files. One file differs: `skills/evidence-check/SKILL.md`, whose
  line 443 (a prose line opening with a four-backtick code span) opened a
  fence under the old rule and hid `## Known limits`, `## Migrating a
  pre-anchor ledger` and `## CI`. None of the three is marked
  `Orchestrator:`, so the role check's verdict does not move. The two
  five-space fences the frame named change no heading, because no heading
  stands between them. The probe was deleted after the run.
- **S12 has two shapes in each reader.** The frame named the backtick-info
  shape. The four-space shape is the other difference between the old rule
  (`^\s*`) and the shared one, and it is red in both readers too.
- **The meter's loader is lazy, and `measure` calls it first.** The existing
  S18 row for `--calibrate` runs a copy that lacks both `session_cost.py`
  and `unverified_check.py`. A load at import would have answered that row
  with the wrong purpose. So the fence rule loads only under `--sections`,
  and `measure` asks for it before it reads the root, which is how the new
  S18 row reaches it in a directory with no `agents/`. The new row also
  asserts its sentence does not name the transcript sibling.
- **The meter's exit-code paragraph** now lists the missing fence rule under
  `--sections` as a 2.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `payload_meter.py#FENCE` | `unverified_check.py#fence_opener` / `#fence_closes`, which `heading_starts` asks through `_fence_rule` |
| the role test's `FENCE` | the same pair, loaded as `RULE` |
| `payload_meter.py#FENCE` in `fence_opener`'s list of readers that keep their own rule | the same docstring's list of readers that ask it, with the role test's `headings` |
