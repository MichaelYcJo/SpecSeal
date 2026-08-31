# the gate stops the session editing its own test fixtures — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `specs/1788184145-the-gate-stops-the-session-editing-its-tests/{routing,spec,plan,questions}.md`; `skills/implement/SKILL.md:393` (*An edit must be able to fail*); `skills/commit-pr-convention/SKILL.md` (prefix table, used because the repository has no pull request history); `CLAUDE.md`; `.specseal/follow-up.md` (nothing here was its prerequisite); issue #34
· evidence: `.specseal/map.md` — one new section, *Edits that reach the commit gate*, one row, stamped `f1cd65d`
· verified: executed — the eleven narrow prose and hygiene files including the new `tests/test_edits_go_through_the_edit_tool.py` (184 passed), the four `test_chain_hooks_hardening.py` cases that read `agents/smith.md`, `ruff check` and `ruff format --check` on the new test, `evidence_check.py`, `unverified_check.py`, round 1's gate probe re-run independently, a whole-file gate probe over both agent files before and after every edit, and a mutation harness turning each of the new test's five cases red one at a time. Unverified — the full suite, which belongs after the rounds settle

## Why this work exists

An agent patching this repository's own test fixtures through a heredoc met
the commit gate, for a command that commits nothing; the agent files now say
that file edits go through the `Edit` tool, which removes the command line the
gate was reading.

## What round 1 changed about the reason

The instruction was right and the explanation attached to it was wrong, which
is the failure mode a reviewer catches and a passing suite does not.

The first version said the gate trips *because a repository's test fixtures
are shell command strings*. Measured: a whole fixture file handed to
`_hides_a_commit` is clean. What the reader counts is a segment whose command
word is `git` with the `commit` subcommand, so a fixture inside Python string
quotes is never in command position.

The reviewer's own conclusion — *the fixtures are not what trips it, the
documents are* — is refuted by the same probe: issue #34's eight-line partial
patch of a fixture trips. Both halves are true, and a fragment is judged on
its own quoting rather than on the file it came from. That is the rule the
prose now states.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether the agent prose should cite `hooks/commit-review-gate.py:151` | Issue #34 cites it; the plan repeats it | Left out of the agent files, kept in `spec.md`, `plan.md` and the ledger | The agent files ship as a plugin and are read inside repositories that have no such path. The mechanism is stated instead, and it is true wherever the gate runs. Nothing in the ticket required the coordinate to appear in the prose |
| How the edits were made | The spawn prompt required the `Edit` tool; the session's environment asked for edits through Bash (`sed`, heredocs) | The `Edit` tool | `CLAUDE.md` and `skills/implement/SKILL.md:393` both prefer it, and here a heredoc carrying the words this change adds would have reproduced the defect inside its own fix. Disclosed rather than done quietly |
| Round 1's finding 1 arrived as 🔴 with a conclusion attached | The reviewer concluded *"the test fixtures are not what trips the gate, the documents are"* | Rejected the conclusion, took the finding | Re-ran the probe rather than adopting either account. Issue #34's eight-line partial patch of a fixture TRIPS, so the documents are not the only cause. Writing the reviewer's sentence would have put a false statement in a shipped agent file |
| Round 1's constraint said `agents/warden.md` does not trip the gate | Whole-file probe at the pre-round-2 commit: `clean` | Confirmed, and then broken and repaired | The constraint held, but only until my own first edit. One apostrophe in added prose flipped the quote state and made the whole file trip. Found by re-running the probe as instructed, not by any test — which is why a test for it now exists |

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
