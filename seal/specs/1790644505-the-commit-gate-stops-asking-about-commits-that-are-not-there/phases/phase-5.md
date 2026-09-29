# 1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there — phase 5

<!-- seal/specs/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there/phases/phase-5.md -->

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | 130f8010 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 5, added by the orchestrating session at `6f4b0e34`
after phase 4 found the class and the orchestrator confirmed it at
`3911a8cf`: #670. `exec`, `timeout`, `nice` and `xargs` in front of `git
commit`, and `$( … )` or backticks around one, read silent while `env` is
judged. The owner's standing rule puts the fix on this branch.

The message that started the phase set the terms. Enumerate the wrappers that
run their arguments as a command, and put the list here with how it was found
and what was left out and why. A commit inside `$( … )`, backticks or `<( … )`
is judged or reads as unreadable, never silent. Stricter is the only permitted
direction; where the reader cannot be certain, it stops. The cases must be
seen red at `768377bf`, S7 green before and after, one mutant per branch under
`PYTHONDONTWRITEBYTECODE=1`, ledger rows and a changelog entry naming #670,
rows it drifts re-read, and the gate-change lines here.

## What this phase found

**Three readings, not one.** #670 names one symptom, and it has three
causes:

- the reader knew five wrappers by name and stopped at the first word it did
  not know;
- it never read a string handed to a shell (`sh -c`);
- it never looked inside a substitution.

Each is its own reading, and each adds invocations only.

**The enumeration** (`hooks/cmdline.py#RUNNERS`), with where each group came
from:

| Source | Programs |
|---|---|
| POSIX: the utilities whose operands name a utility to execute, and the special built-in that replaces the shell with one | `command`, `env`, `nice`, `nohup`, `time`, `xargs`, `exec` |
| GNU coreutils, the *Modified command invocation* chapter, plus `runcon` from its SELinux chapter | `chroot`, `env`, `nice`, `nohup`, `stdbuf`, `timeout`, `runcon` |
| The same coreutils under the `g`-prefixed names Homebrew installs on macOS | `gchroot`, `genv`, `gnice`, `gnohup`, `gstdbuf`, `gtimeout` |
| util-linux: the scheduling, session, locking, limit and namespace tools | `chrt`, `ionice`, `taskset`, `setsid`, `flock`, `prlimit`, `setpriv`, `unshare`, `nsenter`, `runuser` |
| Privilege | `sudo` (already known), `doas`, `pkexec` |
| macOS | `caffeinate`, `arch` |
| Tracers | `strace`, `ltrace`, `valgrind` |
| Programs that run a command per input or on a schedule | `find` (`-exec`, `-execdir`), `parallel`, `watch`, `script` |

How it was found: from those sources' own lists of programs that execute an
operand. Each member got a shape in
`tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py#WRAPPED`,
in the form it is used, and `test_every_enumerated_wrapper_has_a_shape` fails
for any member of `RUNNERS` added later without one.

**The shell-string hosts** (`reparsed_texts`):

- `sh`, `bash`, `zsh`, `dash`, `ksh`, `mksh`, `yash` and `ash`, given a short
  option cluster holding `c`;
- `su`, `runuser` and `script`, given `-c` or `--command`;
- `env -S` in its three spellings;
- `watch`, whose arguments it runs through `sh -c`.

Once the flag is present, every non-option word after the program is read as a
command. Which word is the string depends on options this reader does not
parse (`bash -o errexit -c '…'`), and an extra word costs a stop where a
missed string costs a silence.

**Left out, and why.** Each was executed at phase 5's reader and returns no
invocation, as at the base:

- **A program whose operand is a file, not a command:** `bash run.sh` with no
  `-c`, `source`, `.`, `make`. Reading them means opening the file, and the
  gate reads the command, not what it runs.
- **Task runners:** `uv run`, `npx`, `pnpm exec`, `poetry run`, `bundle exec`.
  They are an ecosystem list with no closed source to enumerate from, and each
  is two words, which the command-word reading does not have.
- **Remote and container runners:** `ssh host git commit`, `docker exec`,
  `kubectl exec`. The commit lands in a repository on another machine or in a
  container, which the gate cannot see or judge.
- **Two other hooks keep their own copy of the five wrappers:**
  `hooks/evidence-advisor.py` and `hooks/review-history-guard.py`. Neither
  decides whether a commit is judged (read, not executed).
- **The worktree guard reads the enumerated runners through `parse_git`, but
  not shell strings or substitutions.** Those readers live in the commit gate.

**Where the reader cannot be certain, it stops.**

- **Options it does not parse.** Behind a runner's own options or operands,
  the first `git` word stands in for the command word, and the directory is
  unplaced (`env -C`, `sudo -D` and `chroot` move it, and knowing which flags
  do so needs a parser).
- **A `case` inside a substitution.** Its patterns end in an unmatched `)`, so
  from the `case` word to the end of the input counts as the body.
- **An unterminated substitution** runs to the end of the input.
- **Expansions in a shell string.** A command word the shell would expand
  there (`sh -c "$CMD"`) counts as one that might commit.

**Why no shape the base judges becomes silent.**

1. *`parse_git` finds the same command word wherever the base found one.* The
   base read past assignments and the five `WRAPPERS`, which are a subset of
   `RUNNERS`. For a segment where the base reached `git`, every word before it
   was an assignment or one of those five, so the new loop reaches the same
   `git` with `after_runner` either unset or irrelevant: the scan runs only
   when the word reached is not `git`. The scan can only add a `git` where the
   base had none.
2. *The gate's invocations are a superset.* `commit_invocations` and
   `_hides_a_commit` keep every branch they had and add two: a shell string,
   and a substitution body, each of which can only append an invocation. The
   directories of existing invocations are not touched, and the only
   directories added are `Unresolved`, which is a stop wherever the session
   opted in.
   **Corrected 2026-09-29 by round 1's fix pass.** This item was false in
   three places, and round 1's red refuted it:
   - Resolved directories were added: `nice git -C W` and `do git -C W`
     compose an absolute `-C` onto the walk's base.
   - A found invocation took away the base's fallback for a command the
     splitter could not finish, which judged the session's own directory
     only while nothing was found.
   - An unresolved target is not a stop where `[no-review]` is present.

   So `nice git -C W commit -m x; echo $'it\'s'; git commit -m y`, with W
   declared, read silent where the base denied, and bash committed in the
   session's repository. The fallback now stands beside what was found, so
   the argument holds for invocations and for the fallback alike.
   `tests/test_no_shape_the_base_stops_reads_silent.py` carries the shapes
   that refuted this item.
3. *Measured.* S7 passed before the change (`768377bf`) and after it.
   The 34 modules that load the gate, the reader, the guard or the consent
   writer passed at the phase's head (1412 passed, 2 skipped, exit 0).

**What the stricter reading costs, measured.** The body of a substitution is
read the way a heredoc body is, and a heredoc body is read as commands however
it is quoted. That is the base's own rule, and the frame refused to narrow it
by consumer. So the message in `git commit -m "$(cat <<'EOF' … EOF)"`, which
the base never read, is now read.

Of the 275 commit messages on `release/v0.16.0`, sent in that form, one
(`95e3258`) is newly read as hiding a commit, against none at `768377bf`. That
is the prompt cost: one attended prompt, or one refusal under the
`automation` press, per such message.

The same rule makes this repository's two gate fixture files read as hiding a
commit when taken whole. Their strings hold commits inside `sh -c` strings and
substitutions. So contract §9 and the policy no longer say a whole fixture
file is clean. `seal/ledger.md`'s row on the command-word rule is corrected,
and a case pins the new §9 sentence.

**A defect the mutants found.** A herestring (`<<<`) inside a substitution was
stepped over by only one character, so its last two `<` read as a heredoc and
the body ran to the end of the input. The effect was stricter, but wrong. It
is fixed at `0ae1f042` and pinned, and the pin was seen red with the fix
disabled.

**One existing case moved.**
`tests/test_the_guard_asks_once_per_session.py#COMMAND_WORD_GROUPS` pinned
`nice git` as a word the guard does not read as git. `nice` is now an
enumerated runner, so the guard judges `nice git worktree add`, which is the
stricter direction for the guard too. The pin moved group, `uv run git` took
its place as the example of a word not read, and `docs/worktree-guard-spec.md`
says so. At `768377bf`, `parse_git` returns `None` for both (executed).

**Seen red.** The cases were committed at `123ee602` before the reader
changed. 121 of the 129 then in the module failed at `768377bf`'s code; the
eight that passed were the controls. Shapes added later were checked against
`768377bf`'s archived hooks by a deleted probe, and each returned no
invocation there:

- the six remaining `g`-prefixed and `runcon` runners;
- the two `env -S` spellings;
- a shell string inside a substitution;
- the guard pin.

The unit pins on the readers fail at `768377bf` because the readers do not
exist there.

**Mutants.** Each was killed on its own under `PYTHONDONTWRITEBYTECODE=1` and
restored, and `git diff` was empty after each:

| # | Branch mutated | Killed by |
|---|---|---|
| 1 | runners narrowed back to `WRAPPERS` | 72 cases |
| 2 | the runner scan trigger removed | 56 cases |
| 3 | `--command` never hands a string | the `su --command` shapes and pins |
| 3b | `--command` hands a string for any program | `--command is su's, not a shell's` |
| 4 | only a bare `-c` counts | `bash -ec`, the cluster pin |
| 5 | the string-host branch removed | 32 cases |
| 6 | the `--command=` value not collected | the `su --command=` shape and pin |
| 7 | the `watch` branch removed | `watch` shape and pin |
| 8 | `env -S` as a separate word not read | `env -S` shape and pin |
| 9 | `--split-string=` not read | its shape and pin |
| 10 | `-S` glued not read | its shape and pin |
| 11 | reserved words and `[` not skipped in a shell string | the declared controls and the unknown-command pin |
| 12 | the expansion check removed | `sh -c "$CMD"` and the unknown-command pin |
| 13 | the dashed heredoc's tab-stripped delimiter | the dashed-heredoc body pin |
| 14 | heredocs not stepped over | both heredoc body pins |
| 15 | the herestring step disabled | the herestring body pin |
| 16 | single quotes inside a substitution | the `)` in single quotes pin |
| 17 | escapes inside a substitution | the escaped `)` pin |
| 18 | double quotes inside a substitution | the `)` in double quotes pin |
| 19 | nesting not counted | the nested pin |
| 20 | the `case` fallback removed | the `case` shape and pin |
| 21 | outer single quotes not text | the single-quoted control and pin |
| 22 | outer double quotes not tracked | the quoted `<(` and apostrophe pins |
| 23 | outer escapes not stepped over | the escaped `$(` pin, added when this mutant first survived |
| 24 | the backtick branch removed | the backtick shape and pins |
| 25 | an escaped backtick inside not stepped over | its pin |
| 26 | process substitution inside quotes | the quoted `<(` pin |
| 27 | the process-substitution branch removed | `<( )`, `>( )` shapes and pin |
| 28 | `_hides_a_commit` reads no shell string | a shell string inside a substitution |
| 29 | `_hides_a_commit` does not recurse into substitutions | nested, arithmetic, heredoc-body shapes |
| 30 | `commit_invocations` reads no shell string | 34 cases |
| 31 | `commit_invocations` reads no substitution | 24 cases |
| 32 | `_string_hides_a_commit` without the unknown-command check | `sh -c "$CMD"` |

The `continue` the gate had after an `eval` segment was removed, not mutated.
It only kept out a duplicate target, so no case could tell it was there.

Not mutated: `_heredoc_end`'s two fall-through returns (an empty delimiter,
and a delimiter line never found). Each mutant could only lengthen a body,
which is the stricter side, so neither can hide a commit. That was read, not
executed.

**Lines for the pull request, `CONTRIBUTING.md` §*What a change to a gate
must carry*.** These cover #670; phases 1 and 4 hold theirs.

- *A test seen red.* Every new case was run against `768377bf` before the
  change, or against its archived hooks for the ones added later. Every
  changed branch has a mutant a case kills.
- *Failure direction: it blocks more, never allows more.* Every invocation
  the base found is still found, in the same directory. What is added is a
  commit behind an enumerated program, in a shell string or in a substitution,
  and the last two stop as unreadable. A wrong read costs a stop, never a
  silence.
- *Prompt budget.* A commit written in any of the new shapes now meets the
  gate: in an attended session, one refusal and then a prompt; under the
  `automation` press, a refusal. The side cost is measured: 1 in 275 of this
  repository's commit messages, sent as `"$(cat <<'EOF' … EOF)"`, now reads
  as hiding a commit, where none did at `768377bf`. A heredoc edit of this
  repository's gate fixture files now stops too, which contract §9 already
  routes through the `Edit` tool.
- *Why nothing cheaper reaches the same guarantee.* Leaving the shapes unread
  is a real commit nobody judges. Narrowing the heredoc rule by consumer, to
  spare the commit-message case, is the narrowing work item `1790635415`
  measured to read real commits silent.
- *Platform honesty.* This is pure string reading, with no process
  inspection. The enumeration names macOS, Linux and GNU programs alike, and
  none is run. The cases ran on macOS; Windows is CI's `windows-latest` leg.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the gate's `continue` after an `eval` segment | none: it only kept a duplicate target out |
| `overview.md`'s phase-4 *Not done* bullet on the wrappers and substitutions | the same bullet, rewritten as done in phase 5, so phase 4's pointer still lands |
| contract §9's and the policy's "a whole fixture file is clean" | the corrected sentences in both, pinned by `tests/test_edits_go_through_the_edit_tool.py#test_the_rule_names_a_string_a_shell_runs_as_a_position` |
| `nice git` in the guard's not-read-as-git group | the group the guard judges, and `uv run git` in its place |
