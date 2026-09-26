# an automation run creates its worktrees without asking — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Answered from the tree — do not reopen

The spawn prompt and the milestone left these open, and the repository
settled each. The grounds are in `spec.md` and in `plan.md`'s Alternatives
table.

- **What the guard reads as consent**: the `AskUserQuestion` answer in this
  session's own transcript. Grounds: it is the only candidate both present at
  the measured moment and written by the harness rather than the model
  (`spec.md` §*What counts as consent the model cannot forge*).
- **Whether a committed `routing.md` counts**: no, not even as a fallback. The
  model writes every byte of it, and in both measured runs it did not exist
  yet when the guard asked.
- **Whether #8's Agent path gets its own rule**: yes. `docs/worktree-guard-spec.md`
  §*Premise* counts work streams, and an isolated agent is a second stream by
  construction. The rule changes what is measured and keeps #237's
  one-confirmation floor.
- **How the `automation` label is recognised despite decorations**: by its
  leading phrase, measured against all 10 routing answers on disk (10 of 10).
- **The two riders on the edited code**: both are resolved and deleted
  (`spec.md` §Scope).

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Should a `per axis` answer with the first box (*run end to end without stopping to ask*) ticked also count as consent? The tree says it is the same promise; what the tree cannot settle is how to recognise it, because in 4 of 4 measured per-axis answers the box label had been reworded or translated, so a rule matching the prescribed label would never fire, and a looser rule would match prose | a person | (a) not counted: per-axis runs keep today's one prompt per session. (b) counted, matched on the prescribed label only, plus a sentence in `skills/implement/orchestration.md` requiring question 2's labels verbatim, which the orchestrator would then have to follow. (c) counted on a loose match: accepts labels nobody prescribed | **(a)**. The build does not read question 2 at all. Nothing gets worse for a per-axis run | ⬜ |
| Q2 | `CLAUDE.md` and `templates/claude-md-block.md` (copied into every install) say *Worktrees only for concurrent sessions*. After this work an isolated Agent in a one-session tree is judged concurrent. Should the line say *concurrent work streams — a parallel subagent counts*? | a person | (a) leave both untouched: the line points at the hook, and the hook's authority, `docs/worktree-guard-spec.md` §*Premise*, already says streams. (b) reword both in this work: every install's CLAUDE.md changes at the next update | **(a)**. The build edits neither file | ⬜ |
| Q3 | A switch written after a creation in the same command is never judged (`main`'s walk skips it once the creation has set the verdict), so with consent present `git worktree add … && git switch x` goes silent even over another session's ACTIVE tree. This has held for every session with a consent record since #257; this work extends it to the first creation of an automation session | the work | Not built here: its fix belongs to the walk, not to what counts as consent, and the milestone says this release adds no mechanism. The orchestrator files it as an issue before the pull request, and the PR body names it | Out of scope; filed by the orchestrator as #620 | ✅ |
| Q4 | Does a subagent's PreToolUse payload carry the parent's `transcript_path` or its own `subagents/…` path? | a measurement | Either answer lands on spec rule 1's second form (the glob on `<session_id>.jsonl`), so the design does not depend on it. It decides only which form is taken, and is worth one line in the phase-2 record if the build meets it | Rule 1 as written | ⬜ |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. Only this kind blocks the build, and neither row here does:
  each has a default the build proceeds on.
- **a measurement** — a probe, a command or a count settles it.
- **the work** — unknowable or unowned at framing time; the phase that meets
  it decides, or, as with Q3, the orchestrator files it.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
