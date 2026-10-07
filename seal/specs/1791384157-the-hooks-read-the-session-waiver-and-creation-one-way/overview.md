# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — overview

📋 implement applied
· spec:     (filled when the work item closes)
· evidence: (filled when the work item closes)
· verified: (filled when the work item closes)

## Why this work exists

Four facts every gate depends on were read in more than one place and the
readings disagreed (#868), and a brace expansion switched a branch silently
where another session was working (#856); each fact now has one reader that
refuses what it does not recognise.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The one token reader on a command that does not split (phase 1, built in phase 5) | `spec.md` In 3: "read in the command as written AND in `without_bodies`, nothing where the command does not split". `spec.md` S9: "`[worktree-ok]` in a comment, in parentheses and beside a body is read as today". The code reads the bare words the split produced before it failed | S9's reading: the words read before the split fails | Measured in phase 1: four of the six recorded commands In 3's sentence moves are the guard's documented comment form with an apostrophe later in the comment (`# [shared-tree-ok] the release's own tree`), which bash runs and the base guard read. The partial read takes no word inside an unclosed quote, so S7 holds, and over 32,431 pairs it reads no token the base's reads did not. It refuses one recorded pair instead of six |
| What leaves the reading when `CLAUDECODE` leaves `steps_around_hooks` (phase 4) | `spec.md` S6: "`CLAUDECODE= git commit -m x` is plain (`is_plain`) and stands aside where git decides"; `plan.md` *Operational impact* says the same of `env -u CLAUDECODE git commit -m x`. The code: `is_plain` refuses any assignment in a program's place and any program outside its list (`env`) before it asks `steps_around_hooks`, so both stay judged by the reading | The code, unchanged; the cases pin both as not plain (`NO_LONGER_PLAIN`), and the case that flips to plain is `git commit -m CLAUDECODE` | Executed at the base and at the head: `tokens.is_plain("CLAUDECODE= git commit -m x")` is False at both. The verdict is the more cautious one, and it is the one 0.16.0 gave; nothing asked for it to change |

## Not verified

| Item | Who must answer |
|---|---|
| Whether a hook process the harness spawns sees `CLAUDE_PID` (`questions.md` M1, the hook half); the Bash-child half was executed in phase 1 | the repository owner |

## Not done

Nothing yet.

## Fed back into the spec

None yet.
