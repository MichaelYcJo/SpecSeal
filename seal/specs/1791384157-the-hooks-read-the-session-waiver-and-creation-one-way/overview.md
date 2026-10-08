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
| Where the frozen body fallback lives (phase 5) | `spec.md` In 3: "`tokens.without_bodies` takes the fallback the guard's `_without_bodies` carried". The code: `tokens.given(command, fallback)` takes the body reader as an argument, and the guard hands it `cmdline_base.drop_heredoc_bodies` | An argument to `given` | `tests/test_the_frozen_reading_never_grows.py#test_only_the_two_fallback_arms_read_it` pins the importers of `hooks/cmdline_base.py` to the guard and the consent writer; `tokens.py` importing it would add a third. `given` rather than `without_bodies`, because the T1 cases replace `tokens.without_bodies` with one that raises, and the fallback has to catch that too |
| What S7's refusal names (phase 5) | `spec.md` In 3 and S7: "the refusal names `git -c specseal.waive=review`". The PreToolUse reading's refusal for the review arm names the waiver typed in front, `: '[no-review]'; git commit …`; the git-native spelling is the git hooks' refusal | The text unchanged; S7 pins the review arm and the `: '[no-review]'` way on | The form it names splits, so the one reader reads it, and no text a person reads had to change for this. The git hooks' refusal already names `git -c specseal.waive=review` |
| The comment form with an apostrophe before the token (phase 5) | `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py` pinned `{commit}  # don't [no-review]` as a documented form that waives. In 3's reader reads nothing from the apostrophe on | Refused; the case is rewritten to pin the refusal and the waiver typed in front | The apostrophe opens a quote to a reader that reads comments; no recorded run held this form (`phases/phase-1.md`). The apostrophe-after form is pinned as waiving instead |
| A commit whose `git diff HEAD` has no `HEAD` (phase 5) | `spec.md` In 4 names the failures it means: a non-zero exit, an `OSError`, a timeout. On an unborn branch, `-a` or a pathspec makes `changed_paths` run `git diff HEAD`, which exits non-zero | The parity arm asks there | It is a diff git could not take, which is the rule; it costs one question in a repository declaring `seal/parity.md`, on its first commit, where the base said nothing |
| `Enforced by:` beside §*Parity arm* (phase 5) | `spec.md` S15: each policy sentence "with its `Enforced by:` line" | No line in `docs/the-review-and-parity-arms.md`; the paragraph names the module of its three cases, and the pin holds the sentence | The section carries no statement marker, so `tests/test_docs_line_wrap.py` reads a line of paths there as prose over the 88-column limit |

## Not verified

| Item | Who must answer |
|---|---|
| Whether a hook process the harness spawns sees `CLAUDE_PID` (`questions.md` M1, the hook half); the Bash-child half was executed in phase 1 | the repository owner |

## Not done

Nothing yet.

## Fed back into the spec

None yet.
