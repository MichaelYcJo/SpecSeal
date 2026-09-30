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
| `sudo -s` and `sudo -i` as string hosts | `spec.md` S5: `sudo -s 'git commit -m x'` and `sudo -i "$CMD"` → stop. `questions.md` Q4's default: "As stated" | Not hosts. S5's two `sudo` rows are not planted as stops; a pin says `sudo -s 'git commit -m x'` reads as no commit and `sudo -s git commit -m x` as one | Read, `man sudo` 1.9.17p2 on this machine, for both `-s` and `-i`: "The command and any args are concatenated, separated by spaces, after escaping each character (including white space) with a backslash (‘\’) except for alphanumerics, underscores, hyphens, and dollar signs." A quoted string arrives at the shell's `-c` as one word, so the shell never parses it as a command line, and Q4's own second option says the host is then left out. The argv form, which does commit, is the runner reading's since #670. `flock` is a host as stated: util-linux's flock(1) manual page, read online because this machine has no `flock(1)`, says `-c` passes the command "to the shell with -c". Phase 3 |
| `watch`'s join without redirections | `plan.md` phase 3: "`watch` adds its join without redirections" | Not built | Executed: after phase 1, `watch -g 2>/dev/null "$CMD"` and `watch -g 2> /dev/null "$CMD"` already deny, because `names_an_unknown_command` re-splits the joined string and reads it past its redirections, glued or spaced. A second join would ask nothing the first does not, and no case could see it: its mutant would survive by construction. Both rows are planted in `STILL_HANDED` and pass. Phase 3 |
| The directory a merged group's addition takes | `spec.md` decision 3: "An addition takes the directory of the part that holds the command word or the host" | The directories of the group's last part | Read, `hooks/cmdline.py#walk_directories`: across `&` and `\|` the walk carries the unmoved shell beside the moved one (`carried = list(running) + carried`), so the last part's directories include every earlier part's. The only part that moves the shell is a `cd`, and a `cd` part would itself be the group's command word. So the two rules answer alike on every input, and the one built first was a unit no case could fail: its mutant survived. The simpler rule is the superset. Phase 4 |
| The walk's `STATE_CAP` collapse | `spec.md` decision 1 keeps each reader's base answer and adds to it, and says nothing of the walk's cap, which collapses every directory into one unresolved one | A second thread in the walk carries the base's states, and each segment's directories are the walk's and then that thread's | Executed: the directories this item adds beside the base's counted toward the cap, so 9 `2>/dev/null cd sub;` segments, or a refused one and 16 `cd sub;`, collapsed where `86256492` did not, and under `[no-review]` the base's stop read silent. `questions.md` Q7, answered **Keep them** on 2026-09-30. Round 2's fix pass, `879df3b4` |

## Not verified

| Item | Who must answer |
|---|---|
| The cases on Windows | CI's `windows-latest` leg, at the pull request |
| The whole suite, the repository-wide lint and the typecheck | The sealer, once, after the review rounds settle |

## Answered by the orchestrator

On 2026-09-29, and so no longer open:

- **bash 4.1's `{fd}>` before a program word commits.** Executed in the `bash:4.1` (4.1.17) and `bash:5.2` (5.2.37) images: `{fd}>/tmp/log git commit` and `{fd}>&2 git commit` each made a commit in a fresh repository. The branch's `commit_invocations` at `d6fe34c0` finds the commit in both shapes and none in `{fd}>f true`. zsh's parse error on the leading form stands (phase 1), so the stop costs a command zsh would refuse and saves one bash runs.
- **Whether the harness cuts off a long `PreToolUse` hook** (`questions.md` Q1): it does at 600 s, and a timed-out hook does not block. Read from the hooks documentation. The bound only saves time.

## Not done

- **A command word that expands at the top level** — `"$CMD"`, `"$SHELL"
  -c …`, `nohup "$CMD"`, and `sudo -s $CMD` unquoted — is still not asked.
  `spec.md` §*Scope* puts it out: it is a new rule with its own prompt cost,
  not the rest of #670's class. Filed as #678.
- **`parallel`'s expansion question.** Its arguments are read for a commit
  written out. Placing its command word means parsing its options and its
  `:::` inputs, which `spec.md` §*Scope* leaves out. Filed as #678.
- **The worktree guard does not read the merged view.** `git 2>&1 worktree
  add` is not a creation to it, as at `86256492`. The frame put the view in
  the commit gate's three readers alone, and `docs/worktree-guard-spec.md`
  now says so.
- **Every body the gate reads is split twice** (round 2's ⬜ 4).
  `hooks/commit-review-gate.py#_reads_a_commit` asks `split_segments` and then
  `merged_segments`, which splits the same text again. Executed 2026-09-30
  through `commit_invocations` on `git -C /x commit -m x; ` followed by `sh
  -c` repeated 600 and 1,000 times, on archives of both trees:

  | | 600 words | 1,000 words |
  |---|---|---|
  | `86256492` | 2.33 s, 180,300 splits | 6.20 s, 500,500 splits |
  | `b9098078` | 4.14 s, 360,599 splits | 11.04 s, 1,000,999 splits |

  That is twice the splits and about 1.8 times the time, quadratic at both.
  Extrapolated from these figures and not run, the harness's 600 s hook limit
  is crossed near 9,800 words at the base and 7,400 at the head, and a
  timed-out hook is silence. Nobody writes such a command. Splitting once with
  separators and deriving both views from the one result would halve the
  splits; that is a performance pass, not this item's, and no issue is filed
  from here.

## Fed back into the spec

None. `spec.md` and `plan.md` are unchanged. The four places the build went
another way are the divergence rows above, and the policy text is in
`docs/commit-review-gate-spec.md` as the plan asked.
