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

## What round 2 changed about the reason, again

Round 1 corrected *which* segments count. Round 2 found the corrected sentence
still described one branch of two, which is the more dangerous shape: a rule
that is right as far as it goes invites a reader to apply it and stop.

A segment the reader cannot expand counts as well. An `eval` whose argument
holds a variable or a command substitution stops the session with **no `git`
anywhere in the body**, because nothing can tell what it reduces to without
running the shell. So a session following round 1's text would search its
patch for a commit, find none, proceed, and meet the prompt anyway — the
failure this work item exists to remove, arriving through the fix for it.

Both files now state the two branches separately, and each is pinned.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Whether the agent prose should cite `hooks/commit-review-gate.py:151` | Issue #34 cites it; the plan repeats it | Left out of the agent files, kept in `spec.md`, `plan.md` and the ledger | The agent files ship as a plugin and are read inside repositories that have no such path. The mechanism is stated instead, and it is true wherever the gate runs. Nothing in the ticket required the coordinate to appear in the prose |
| How the edits were made | The spawn prompt required the `Edit` tool; the session's environment asked for edits through Bash (`sed`, heredocs) | The `Edit` tool | `CLAUDE.md` and `skills/implement/SKILL.md:393` both prefer it, and here a heredoc carrying the words this change adds would have reproduced the defect inside its own fix. Disclosed rather than done quietly |
| Round 1's finding 1 arrived as 🔴 with a conclusion attached | The reviewer concluded *"the test fixtures are not what trips the gate, the documents are"* | Rejected the conclusion, took the finding | Re-ran the probe rather than adopting either account. Issue #34's eight-line partial patch of a fixture TRIPS, so the documents are not the only cause. Writing the reviewer's sentence would have put a false statement in a shipped agent file |
| Round 2 handed over replacement paragraphs the reviewer had already applied and measured | Reviewer's text, verified at 76 columns and zero added apostrophes | Rewrote them, keeping the claim | Taking measured text unread would make the wording the reviewer's and the responsibility mine. Rewriting cost one real defect and caught it: my version dropped `command position` from `agents/warden.md`, and round 1's own test failed at the baseline run before any mutation. The test planted last round paid for itself this round |
| Q2 was a decision, and the session was told to run unattended | Round 2 named it a trade needing a person | Wrote `questions.md` Q2 with three options; raised no prompt | The standing instruction is that a decision needing a person becomes a row. A waiver example is only useful shown verbatim, so making the line stop tripping may cost the example its job — not a call a session should make to quiet its own tooling |
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

`agents/smith.md` still trips the gate at its own waiver example, and that was
left rather than fixed. Breaking the example to quiet the line would cost the
example its job — a waiver a reader has to retype by hand is a waiver typed
wrong. The fact is recorded three ways so it cannot go missing: a rider at the
coordinate, `questions.md` Q2 with the options priced, and a ledger row.

## Fed back into the spec

None. The change states an existing rule in a second place and adds the reason
the rule did not carry; no new clause was inferred.
