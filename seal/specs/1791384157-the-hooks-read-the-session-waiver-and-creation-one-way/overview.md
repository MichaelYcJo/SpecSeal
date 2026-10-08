# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — overview

📋 implement applied
· spec:     `spec.md` In 1–6 and S1–S24 with the reframe after round 3, `plan.md` phases 1–10 and Alternatives, `questions.md` (#856 = (c), P1, M1–M5, W1–W4); `docs/worktree-guard-spec.md` §A, §*Creation consent*, §*Which tree*, §*Known limits*; `docs/the-commit-gate-inside-git.md` §*The commit gate inside git*; `docs/commit-review-gate-spec.md` §*commit-review-gate (PreToolUse, Bash)*; `docs/the-review-and-parity-arms.md` §*Parity arm*; agent contract §12, §13, §15
· evidence: `seal/ledger/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way.md`: rows for S1–S24 and the round fixes (S3a, S5a, S11a, S11b, S13a), 7 `Corrected ·` rows (W7, G3, W1, W3, W4, T1, M1) and 51 `Re-read ·` rows written by `evidence-check --reverify --into`
· verified: executed — the corpus probes of phases 1 and 7, M5 under bash and zsh, every new case red before its code or its mutation, `bin/mutation-check` on each new unit, the modules each phase names, the 45 modules touching a changed hook, the eight suite-wide guard modules, `bin/evidence-check . --strict` and `bin/correction-check`; read — the Windows branches, and whether a hook process sees `CLAUDE_PID`; not run — the full suite, which is the sealer's

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
| The brace stop's text (phase 9) | `spec.md` In 5, reframed: the plain spelling "is the text `_described` already carries". That text said the shell turns a brace into other words "before git reads them", which is false of `cat {a,b}` | Reworded, in both languages: "before the command runs, so this guard cannot tell which command that is"; the two text pins follow | §14: a person reads the stop and acts on it, and the reframe made it reach commands that are not git |
| S18's red at `a8f86f44` (phase 9) | `spec.md` S18: "red at a8f86f44 by construction (each silent there)" | Nine of ten parameters red there; `A={{a,b},c} ls` already stopped | The removed command-word reading read every word up to the command word, and an assignment stands before it, so a nested brace there was already a stop. The case pins it as a stop at the head either way |
| Records naming the removed units (phase 9) | The reframe removed `_brace_command_at`, `_brace_spells_git` and `_ONE_BRACE` (NAME NOT IN TREE); 30 lines of `spec.md`, `plan.md` and the round 2 and round 3 records named them | Each such line carries `NAME NOT IN TREE` beside the name; no other word of those records changed | `bin/evidence-check --strict` refuses a record naming a unit the tree lacks, and the marker is the remedy it names |

## Not verified

| Item | Who must answer |
|---|---|
| Whether a hook process the harness spawns sees `CLAUDE_PID` (`questions.md` M1, the hook half); the Bash-child half was executed in phase 1 | the repository owner |
| Windows: the consent writer reading through the backslash-doubling adapter, the lease route and the stub without `CLAUDECODE`, and the S10 cases, which skip there because the `git` shim is a POSIX script; all read, none run on Windows | the repository owner, through the CI Windows leg at the pull request |
| The full suite, lint and typecheck over the whole tree | the sealer, spawned by the orchestrator after the review rounds |

## Not done

- `spec.md` S6's `CLAUDECODE= git commit -m x` standing aside: not built,
  because `is_plain` refuses the assignment first (divergence row above).
- `seal/releases/0.20.0.md` R1 takes a `Re-read ·` row rather than the
  `Corrected ·` row `spec.md` S14 named: R1's claim already says `--root` is
  read "off the words once their redirections are off". The phrase S14 meant
  was the docstring's, which phase 3 corrected.
- No PreToolUse refusal text changed to name `git -c
  specseal.waive=review` (divergence row above).

## Fed back into the spec

Inferred during implementation, for a planner to overturn:

- The one consent-token reader reads the bare words before a split fails
  and none after it (`hooks/tokens.py#given`, In 3 amended by phase 1's
  measurement).
- The frozen body fallback is an argument to `tokens.given`, handed by the
  guard, so `hooks/tokens.py` stays outside the frozen reader's importers.
- A `git diff HEAD` on a branch with no commit is a failure the parity arm
  asks about, like any other (In 4).
- A non-git brace segment's union of trees carries one finding and several
  trees (`_finding_trees`); a glued `-C<dir>` is not read, as the frozen
  reader does not read it for a git segment (`questions.md` W3).
- `questions.md` P1 is built on its default, **yes**, under `Automation |
  yes`; the owner's answer is still open, and a *no* reopens the frame.
