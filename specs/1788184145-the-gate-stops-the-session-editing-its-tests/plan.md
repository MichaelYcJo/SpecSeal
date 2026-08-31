# Implementation Plan: the gate stops the session editing its own test fixtures

<!-- specs/1788184145-the-gate-stops-the-session-editing-its-tests/plan.md — HOW, in
phases. This is the Design Gate's artifact: where the work alters observable
behaviour, approval of this plan is the gate. -->

## Approval

**Approval was given in advance**, by the repository owner, on 2026-08-31, for
option A as scoped below. The session that implements it does not stop for a
go, and anything that would otherwise be raised is written into
`questions.md` or `.specseal/follow-up.md` instead.

This work sits on the top rung — it alters an agent's instructions, which is
text a spawned session reads and acts on — so `spec.md` and this file are owed
whether or not anyone is waiting to approve them.

## Summary

An agent editing this repository's own test fixtures through a
`python3 - <<'PYEOF'` heredoc meets the commit gate. The gate reads a heredoc
body as shell on purpose, because a commit hidden in one used to walk past it.

**What it counts is narrower than the first draft of this plan said**, and
round 1 measured it: a segment whose command word is `git` with the `commit`
subcommand. A fixture sitting inside Python string quotes is never in command
position, so a whole fixture file handed to the reader is clean. What trips it
is a *fragment* whose own quoting leaves a commit in command position — issue
#34's eight-line reproduction — or a document line showing a waiver example
verbatim. Either way the gate finds a commit, cannot say which repository it
lands in, and asks, for a command that commits nothing.

The fix is to remove the Bash command line rather than to change the gate:
state in `agents/smith.md` and `agents/warden.md` that file edits go through
the `Edit` tool, naming both reasons that point the same way.

## Technical context

- `hooks/commit-review-gate.py:151` — `_hides_a_commit` recurses into heredoc
  bodies. Added by `4ba28fe` for legacy #75. This is the behaviour that makes
  a patch-by-heredoc look like a commit, and it is correct.
- `skills/implement/SKILL.md:393` — *"An edit must be able to fail."* The
  source of reason 1. The agent files must not restate the skill at length;
  they add what it does not carry, which is reason 2.
- `agents/smith.md:79` — phase 3 already says half of it. Reason 1 is there;
  reason 2 is missing. Extend at that coordinate rather than adding a second
  paragraph elsewhere, or the file says the same thing twice.
- `agents/warden.md` — says nothing about this. `grep -n -i 'edit tool|`Edit`|
  sed -i|heredoc'` returned zero lines. It needs the whole statement.

**Failure scenario in six months.** The instruction reaches agents and not
people, so a maintainer editing the gate's tests by hand through a heredoc
meets the same prompt. That is the known and accepted limit of option A, and
it is what Q1 exists to revisit.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A — say it in the agent files** | Reaches agents only; a person editing by hand still meets the prompt | **Taken.** Small, needs no change to a gate, and removes the path for the agents that actually hit it |
| **B — the gate skips a heredoc body being written to a file** | The reader would have to decide what a body is FOR, a judgment it makes nowhere else, and legacy #75 exists because a body that looks inert can run | Out of scope. Becomes Q1 rather than a change made to quiet a prompt |
| **C — leave it** | The measured cost is a stopped session in an unattended run, and approving records a waiver for a command that never commits | Rejected |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `agents/smith.md` phase 3 names both reasons | `test_docs_line_wrap`, `test_the_set_a_work_item_always_has`, `test_broad_gate_rule`, `test_waiver_decided_at_start`, `test_one_word_one_meaning`, `test_chain_hooks_hardening` | `a15ef3b` |
| 2 | `agents/warden.md` carries the whole statement, beside its probe rules | the same set, plus `test_handoff_outlives_the_merge` | `a15ef3b` |
| 3 | the `## Unreleased` changelog entry, the ledger row and the closing memo. (`questions.md` Q1 was written with the rest of the SDD set, before implementing) | `test_release_hygiene`, `test_ledger_stamps_resolve`, `evidence_check.py`, `unverified_check.py`, `test_chain_hooks_hardening::test_plugin_version_is_in_changelog` | `f805088` — `questions.md` Q1 at `13ab33a` |
| 4 | Round 1's findings: the corrected mechanism in both agent files, the reader-repository claim removed, and `tests/test_edits_go_through_the_edit_tool.py` planted | the narrow suite, plus a mutation harness showing each of the five cases go red | `8b6c6ff` |

Phases 1 and 2 are one vertical slice each — a file whose readers are sessions,
so what makes it runnable is the prose tests that read it.

Phase 4 was not planned. It exists because round 1 found phases 1 and 2
shipping a correct instruction with a wrong reason attached, which is a defect
the tests could not have caught because phase 3 planted none.

## Operational impact

None. No migration, no new environment variable, no new dependency, no
compatibility break. `.claude-plugin/plugin.json` stays at `0.0.1`; the pull
request lands on `release/v0.0.2`, so the entry goes under `## Unreleased`.
