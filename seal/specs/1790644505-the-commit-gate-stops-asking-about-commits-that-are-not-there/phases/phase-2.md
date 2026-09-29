# 1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there — phase 2

<!-- seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 36e3d994 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 2, the written half. Contract §17, *A commit names its
repository in the command that makes it*, as the next number and the last
section, carrying two reasons — an agent's shell starts in the session's
directory at every call, and a loop variable is not a path the gate can read —
and pointing at §8 and §9 rather than restating them. One sentence in
`skills/implement/orchestration.md` §*Write the file in a command of its own*
citing it. A new case pinning §17's two reasons, seen red with each deleted.

## What this phase found

**The section registry had to grow with the section.**
`tests/test_the_agent_contract_holds_the_universal_rules.py` refuses a section
with no pin (`test_every_pinned_section_exists_and_nothing_is_unpinned`), so
§17 took a row in its `PINS`: the shape sentence, *join it to the commit with
`&&` and nothing else*. That is the one existing test file this phase edits,
and the edit is the registry's own extension, not a changed case.

**§17 does not trip the gate it is about.** `_hides_a_commit` over the whole
contract stays False with §17 in it, and a case in the new module holds that,
beside `tests/test_edits_go_through_the_edit_tool.py`'s own.

**No copy of §8 or §9.** `tests/test_a_moved_rule_leaves_its_definition.py`
passed with §17 in place, so no 15-word run of it appears in an agent
definition, and the new module refuses the two phrases a restatement of §8 or
§9 would carry.

**Seen red.** Each of these deletions turned the named case red, one at a
time, and the text was restored and checked equal to the commit after each:

| Deleted | Red |
|---|---|
| the first reason, where the shell starts | `test_the_first_reason_is_where_the_shell_starts` |
| the second reason, what the gate can read | `test_the_second_reason_is_what_the_gate_can_read` |
| the pairing sentence | `test_the_rule_pairs_its_two_reasons` |
| the shape sentence | `test_the_rule_is_the_last_section_and_names_the_shape`, and the registry's §17 pin twice |
| the orchestration sentence | `test_the_orchestrator_commits_its_routing_files_the_same_way` |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
