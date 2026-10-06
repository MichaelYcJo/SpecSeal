# 1791270165-the-windows-test-leg-is-measured-and-cut — phase 4

| Field | Value |
|---|---|
| Phase | 4 (4a written; 4b waits on phase 1's Windows table) |
| Commit | 83801eac (4a; the sampler landed at 597cc5f7, its cover case was tightened here) |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

4a, local only: a covering sampler over `_placed(verb)` in
`tests/test_guard_resolves_the_tree_it_judges.py` with S5's coverage
contract asserted by a structural case; the twins case and
`test_no_constructed_switch_is_silent` walking the sample; the red against
`94d7b2e0`'s reading shown; Q4 measured by a `test_tmp_*` probe, deleted;
D1 of `seal/releases/0.18.2.md` re-read into this item's fragment. 4b is
not started.

## What this phase found

**The sample.** `_sample(verbs)` keeps every
`(operator, position, glued, target spaced)` placement the product holds at
least once, the verb that carries each taken in rotation, and for every verb
its first shape with a redirection after the subcommand holding no `&` or
`|` and its first with one that does. It is a cover, not a draw: sorted
keys and list order only. Twins: 870 shapes of the product's 20,832.
`_placed` now yields `spaced_target` as a fifth value so the placement can
be read off a shape; `_shapes` and the two cases were its only readers in
the repository.

**What left.** Each verb is no longer read at every placement, only at the
placements it carries in the rotation and its two per-cut shapes. A defect
that one verb shows at one placement alone, and no other verb shows there,
can now pass. What stays: every placement is read for some verb, every verb
is read on both sides of a cut, and the per-verb readings in
`test_classify_reads_no_switch_in_a_twin` are untouched. The rewrite or
retirement of the case is #826's, by the owner's comment.

**Seen red (§15), each through `bin/mutation-check`, `executed` 2026-10-06:**

| Break | Cases run | Verdict |
|---|---|---|
| `_sample`'s placement loop: `chosen.add((holder, first[holder][key]))` → `pass` | `-k sample_covers` | `red` — both parameters fail on `missing` (1.6 s) |
| `hooks/worktree-guard.py#read_switch_words`: the `--` return counts any `-b…` after it as creating, `94d7b2e0`'s reading | `-k no_twin_is_asked` | `red` — 28 shapes wrong, `git checkout -- -b y <<<word` among them (6.2 s) |

Both files were restored by the tool from its own copy, and
`git status --short` showed only the intended test edit after each.

**Every unit added, broken one at a time before hand-over.** The first pass
over the helpers found three that nothing watched: `_after_the_subcommand`
(`at > 2` alone), `_placement` (the target-spaced axis dropped) and an
ordering helper, each `SURVIVED`. The cover case measured coverage through
the same `_placement` the sampler used, so a dropped axis vanished from both
sides at once. The fix: the cover case reads the placement off each tuple
directly and states `_after_the_subcommand`'s boundary values, and the
ordering helper is gone, since order decided nothing a case reads
(`sorted(chosen)` keeps the sample deterministic). Re-run with
`-k 'sample_covers or no_twin_is_asked or no_constructed_switch'`:

| Break | Verdict |
|---|---|
| `_after_the_subcommand` → `return at > 2` | `red` (6.1 s) |
| `_placement` → `return op, at, glued, True` | `red` (5.1 s) |
| `_sample`'s placement loop → `pass` | `red` (3.8 s) |

The module after that edit: `426 passed in 18.53s`, exit 0; ruff check and
format exit 0. The two rewritten cases' anchors did not move again, so the
`Re-read · D1` row still holds.

**Q4, `executed` 2026-10-06.** A probe (`tests/test_tmp_twins_spawns.py`,
run once with `-p no:xdist`, deleted in the same command) subclassed
`subprocess.Popen` with a counter. The sampled twins case started **194
processes over 870 shapes**; the first three verbs' 1,268 shapes of the
full product started **0**. So the case is not wholly CPU-bound: some verbs
reach a lookup `is_ref`'s patch does not cover, at roughly one spawn in
four shapes across the sample. Which lookup was not recorded. At the
issue's 60 ms a spawn on Windows, the sample's 194 cost about 12 s there,
against roughly 4,600 for the whole product if the ratio holds. Sampling
alone was kept, Q4's default; growing the fixture is for 4b if the Windows
table still names the case.

**Timing, `executed` 2026-10-06 on the smith's machine.** The three cases
with `-p no:xdist`: twins 2.85 s, switches 0.18 s, the cover case 0.14 s
together. `bin/test tests/test_guard_resolves_the_tree_it_judges.py -q`:
`426 passed in 17.74s`, exit 0. `ruff check` and `ruff format --check` on
the file: exit 0 each.

**The ledger.** `evidence-check .` reported two DRIFTED coordinates, the two
rewritten cases, both cited by D1 of 0.18.2 alone. `evidence-check
--reverify --into seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md
--checked 2026-10-06` wrote one `Re-read · D1` row; no released file
changed.

**`evidence-check --strict .` exits 2, and the cause is in the frame.**
`spec.md`'s Grounding row (line 14) quotes D1's anchor with its released
hash, `…#test_no_twin_is_asked_unless_an_operator_cuts_the_segment@3e34189e`,
and the checker reads that quotation as a coordinate. Any rewrite of the
case drifts it, so plan 4a's `evidence-check --strict .` exit 0 cannot hold
as the frame stands. `spec.md` is the framer's, and this phase did not edit
it. `overview.md` names who answers.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The twins and switch cases' walk over every shape of `_placed` | `_sample`'s cover, held by `test_the_sample_covers_every_placement_and_every_verb`; the full walk is #826's to rewrite or retire |
