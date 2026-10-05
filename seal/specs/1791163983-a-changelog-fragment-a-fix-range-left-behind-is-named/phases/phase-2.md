# 1791163983-a-changelog-fragment-a-fix-range-left-behind-is-named — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 8b83fbcf |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 2: the three links to `docs/the-record-layout.md` §*A commit
after the build brings its changelog fragment along* — `agents/smith.md`'s
paragraph *A fix pass is not a phase, and its record is the round record*,
`skills/implement/SKILL.md` §5, and `skills/code-review/orchestration.md`
§*Orchestrator: a fix pass resumes the implementer*, the last naming the
orchestrator's own two commits — and a `RULES` row in
`tests/test_the_rules_have_one_owner.py` (S9). Each link names the section
and does not restate the rule.

## What this phase found

**The links are short and pass the pasted-passage ratchet** (Q4).
`tests/test_no_passage_is_pasted_into_a_second_file.py` passed with the three
links in and no `BASELINE` entry; each link shares at most *changes what the
work item ships* with the owner's sentence.

**Red, per pin.** The owner's sentence and each of the three links were broken
one at a time with `mutation-check`; rule 15's cases went red each time.

**`agents/smith.md` carries a RIDER whose stamp names `## Phases`**, and the
link sits in that section, so the stamp drifted
(`tests/test_a_rider_reaches_its_file.py`). The rider was read and its three
measurements re-taken at HEAD and with the edit — the waiver line alone in a
here-document body gives one commit invocation, the line with everything above
it gives one, and `_hides_a_commit` is true for the file — unchanged from its
2026-09-22 reading. Its instruction stands and was followed (the example is
untouched), so the stamp was re-stamped with `rider_check.py --reverify --only
agents/smith.md`.

**The new sentences avoid the word `seal`** in all three carriers, so
`tests/test_one_word_one_meaning.py` has nothing new to judge.

**Every module naming one of the three carriers or the owner** — 58 modules,
listed by `grep` before the edits — was run once at this boundary: green but
for the rider (above, now re-stamped) and
`tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`,
which phase 3's `overview.md` answers.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
