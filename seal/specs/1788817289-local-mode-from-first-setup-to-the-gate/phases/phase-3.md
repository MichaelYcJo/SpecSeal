# 1788817289-local-mode-from-first-setup-to-the-gate — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `0d0ea84`, `e580e40` |
| Ran by | specseal:smith on claude-opus-5[1m] |

## What this phase was asked

Build the half of #151 that OBSERVES the missed question: a `PreToolUse` gate
that sees `seal/` present with no recorded mode and asks once. The design was
settled before the work started — the gate and the preset pointer together,
and not `seal/config.md` as the opt-in signal.

## What this phase found

**Two designs were tried and both were abandoned for reasons `plan.md` had
weighed wrongly.** They are recorded here because the rejected reasoning is
what the next reader will re-run.

`plan.md` rejected a third arm of `commit-review-gate.py` on the grounds that
the arm renderer builds a waiver form from every arm's marker. That objection
is a five-line change and it undercounted the prompt budget: three arms render
into ONE deny, so a third arm costs zero additional interruptions wherever the
review arm already fires. It was tried second and abandoned on a different
ground, which is the one that actually holds — that file's cases pin
`"BOTH questions in ONE call"`, a two-arm sentence, and compare a whole prompt
against a released version, so a third arm rewrites pinned text in a
1600-line suite this work item has no business rewriting.

A separate gate was then blocked by an import: `commit_invocations` and
`commit_targets` live in `commit-review-gate.py`, not in `hooks/cmdline.py`.
Reaching them by loading that module from disk is the exact anti-pattern that
file's own docstring records having been fixed, and moving the whole cluster
into `cmdline.py` is a refactor of a 1000-line gate inside a bug fix.

**Which is what argued the trigger down from a commit to any Bash call, and
that is a better answer rather than a consolation.** The mode question needs
no command-line reading at all: its subject is the workspace the session is
sitting in, and `git -C <elsewhere>` does not move that. The count of
interruptions is identical, because the budget is per session; where the
question LANDS is not — `skills/implement/SKILL.md` §1 costs a question by
when it arrives, and the first Bash call is the batch a session collects
before it starts. Two cases were rewritten to say so, and the one that had
asserted a non-commit is silent now asserts the opposite.

**The bootstrap has to record the answer or the gate asks the person it just
asked.** `skills/implement/SKILL.md` §Bootstrap said in as many words *do not
write that config row here*; leaving it would have produced a double-ask on
the one path where the question WAS put to somebody. That sentence is gone,
and phase 4 carries the replacement. It is also #151's second Done-when: the
answer has to be observable afterwards.

**A third copy of the config-table parser exists and is out of scope.**
`tests/test_the_pull_request_language_is_the_repositorys.py#items` reimplements
the loop rather than calling it, which is why the header gate had no coverage
anywhere in the tree until this phase wrote a case from a surviving mutation.
Named in the handover.

**Both surviving mutations were real gaps, not equivalent mutants.** Taking
`cwd` for the repository root left the gate silent for every session sitting
in a subdirectory — most of them — and that silence reads exactly like a
repository whose row is already written.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal.py`'s `CONFIG`, `ROW_ITEM`, `LOCAL`/`SHARED`/`MODES`, the three table regexes, `config_path`, `config_rows` and `declared` | `hooks/config.py`, with `seal.py` re-exporting each name; `tests/test_the_mode_question_is_asked_once.py#test_the_command_and_the_gate_read_one_parser` asserts by `__code__.co_filename` that one implementation is left |
| `tests/test_dispatch.py`'s assumption that an opted-in repository is silent for `ls` | the same case, with the mode recorded — otherwise it would assert that a gate stays quiet about the state it was added to name |
