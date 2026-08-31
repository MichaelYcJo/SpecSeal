# the gate stops the session editing its own test fixtures — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `specs/1788184145-the-gate-stops-the-session-editing-its-tests/{routing,spec,plan,questions}.md`; `skills/implement/SKILL.md:393` (*An edit must be able to fail*); `skills/commit-pr-convention/SKILL.md` (prefix table, used because the repository has no pull request history); `CLAUDE.md`; `.specseal/follow-up.md` (nothing here was its prerequisite); issue #34
· evidence: `.specseal/map.md` — one new section, *Edits that reach the commit gate*, one row, stamped `f1cd65d`
· verified: executed — `tests/test_docs_line_wrap.py`, `test_the_set_a_work_item_always_has.py`, `test_one_word_one_meaning.py`, `test_broad_gate_rule.py`, `test_handoff_outlives_the_merge.py`, `test_waiver_decided_at_start.py`, `test_unverified_rows_close.py`, `test_release_hygiene.py`, `test_no_real_identifiers.py`, `test_ledger_stamps_resolve.py`, and the four `test_chain_hooks_hardening.py` cases that read `agents/smith.md`. Read, not run — `hooks/commit-review-gate.py:151`

## Why this work exists

An agent patching this repository's own test fixtures through a heredoc met
the commit gate, for a command that commits nothing; the agent files now say
that file edits go through the `Edit` tool, which removes the command line the
gate was reading.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether the agent prose should cite `hooks/commit-review-gate.py:151` | Issue #34 cites it; the plan repeats it | Left out of the agent files, kept in `spec.md`, `plan.md` and the ledger | The agent files ship as a plugin and are read inside repositories that have no such path. The mechanism is stated instead, and it is true wherever the gate runs. Nothing in the ticket required the coordinate to appear in the prose |
| How the edits were made | The spawn prompt required the `Edit` tool; the session's environment asked for edits through Bash (`sed`, heredocs) | The `Edit` tool | `CLAUDE.md` and `skills/implement/SKILL.md:393` both prefer it, and here a heredoc carrying the words this change adds would have reproduced the defect inside its own fix. Disclosed rather than done quietly |

## Not verified

| Item | Who must answer |
|---|---|
| The full test suite at this branch's HEAD. The narrow scope ran the cases that read the two agent files and the changelog; the broad gate runs once, after the review rounds settle | the review orchestrator |
| That an agent following the new instruction actually stops meeting the prompt. The change is prose a session reads, so nothing in the suite can execute it | the repository owner, at the next session that edits `tests/test_gate_judges_the_repo_it_commits_to.py` or `tests/test_what_the_reader_understands.py` |

## Not done

Option B of issue #34 — teaching the gate to skip a heredoc body that is being
written to a file rather than run — was left, deliberately. It reopens what
legacy #75 closed, so it needs a decision rather than a change made to quiet a
prompt. It is Q1 in `questions.md` with the trade named and the repository
owner as its answerer, and it is the ticket's second checkbox, which stays
unticked.

The reach of option A was not widened either. A person editing these fixtures
by hand through a heredoc still meets the prompt; that is the known limit of
this approach and it is what Q1 would settle.

## Fed back into the spec

None. The change states an existing rule in a second place and adds the reason
the rule did not carry; no new clause was inferred.
