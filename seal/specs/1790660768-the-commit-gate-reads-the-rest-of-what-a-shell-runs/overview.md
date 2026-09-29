# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here, and each part is written when it happens rather
than reconstructed at the end. Facts that must outlive this work item go to the
evidence ledger, not here. -->

## Why this work exists

A commit written behind a redirection, inside a `case` arm, a function body or
a coprocess, in a subshell glued to its `(`, or in a string a host runs past a
redirection, read as no commit at `86256492` and bash landed it; the gate now
reads each of them, and every command it stopped there it still stops.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| `parse_git`'s subcommand for `git 2>/dev/null commit` | `spec.md` decision 1: "A reader that found something at base … returns that same answer." At `86256492` `parse_git` returned a git invocation whose subcommand was `2>/dev/null` | Where the first scan lands on a redirection for the subcommand, the scan past redirections replaces it, when that scan finds a subcommand at all | Read: no consumer acts on a redirection as a subcommand. The guard's `classify` acts on `worktree`, `switch` and `checkout`, the gate and `hooks/implementer-notice.py#commits` on `commit`, and `hooks/worktree_consent.py` only after `adds_a_worktree`. So the answer that is replaced was never one any reader used, and every answer a reader used is kept. Phase 1 |

## Not verified

| Item | Who must answer |
|---|---|
| The cases on Windows | CI's `windows-latest` leg, at the pull request |
| bash 4.1's `{fd}>` before a program word commits: read, not run. This machine has bash 3.2.57, which has no `{fd}>`, and zsh 5.9 answers a leading `{fd}>` with a parse error (executed, phase 1). zsh's `>!` and `>>!` in front of `git commit` did commit (executed, phase 1) | the orchestrator, where a bash 4.1 or later is at hand; until then the gate stops the shape, which costs a stop on a command zsh would refuse to parse |
| The whole suite, the repository-wide lint and the typecheck | The sealer, once, after the review rounds settle |

## Not done

Nothing yet.

## Fed back into the spec

None yet.
