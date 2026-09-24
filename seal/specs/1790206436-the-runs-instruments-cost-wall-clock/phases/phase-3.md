# 1790206436-the-runs-instruments-cost-wall-clock — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 8a234674 |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

Two agents alive at once cannot share a scratch name (#544): `agents/warden.md`
§*Where you work* names `<scratchpad>/<work-item-id>/round-<n>/clone` and
puts the round's probes and captures under
`<scratchpad>/<work-item-id>/round-<n>/`; `agents/sealer.md` §*The command*
names the capture file with the work item id and says to quote the gate's
`outputs kept under` line; `skills/verify/SKILL.md`'s `/tmp/run.txt`
example carries the work item id. New module
`tests/test_a_parallel_agent_names_its_scratch_after_the_work_item.py`, red
at the base first. Verified by the new module red then green, the four prose
pins over both definitions and the skill, and `ruff` over the new test.

## What this phase found

**Red first, at `5d51b319`, against the unedited documents**: the module was
written before the three sentences and run in this tree — `3 failed in
0.66s`, one per case, each for the absence it pins. Green after the edits,
`3 passed`, exit 0. This is §15's second form — the sentence the case pins
absent — and it doubles as the mutation for a unit that is a sentence.

**W2, this phase's part — the exact sentences within 88 columns.** The
warden's is a second paragraph inside the first bullet of §*Where you work*,
so the clone rule and its directory read as one item; it names the
directory, the round home, and why (the shared scratchpad, the three
measured collisions, and §7's *every one of them is gone*). The sealer's
joins the *Your stdout is a pipe* paragraph, since that paragraph is about
what the sealer does with the gate's output; the file is
`<scratchpad>/<work-item-id>/broad-gate.log`, and the `outputs kept under
broad-gate-<random>/` line is quoted because it is the one name per run the
gate itself makes. The skill's example binds `out=<scratchpad>/<work-item-id>/run.txt`
once and reuses it on both lines, and the sentence beneath says why the name
is not `/tmp/run.txt`.

**Every module that reads any of the three documents was run as one batch**
(43 modules, found by grep over `tests/` for `warden.md`, `sealer.md`,
`skills/verify/SKILL.md`): `1 failed, 2071 passed, 7 skipped in 128.32s`.
The one failure is
`tests/test_chain_hooks_hardening.py#test_every_spec_directory_that_reached_the_ladder_has_an_overview`,
red because this work item has no `overview.md` yet — phase 4 writes it and
the case is re-run there. The five prose pins (`test_docs_line_wrap.py`,
`test_one_word_one_meaning.py`, `test_a_moved_rule_leaves_its_definition.py`,
`test_the_rules_have_one_owner.py`, `test_no_real_identifiers.py`) were also
run alone: `280 passed`, exit 0.

**One thing the tree does not read.** `zsh` does not word-split an unquoted
`$var`, so the first attempt to hand the grep's list to `bin/test` collected
nothing (exit 5) and `${=mods}` was the form that ran; noted because the
next session batching modules from a grep will meet it.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `/tmp/run.txt` from `skills/verify/SKILL.md`'s capture example | the same example, redirecting to `<scratchpad>/<work-item-id>/run.txt`; the new module's third case keeps the old name out |
