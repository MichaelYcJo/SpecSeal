# the commit gate reads the rest of what a shell runs — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row below needs a person, and none blocks the build.** The spawn prompt
set the invariant, and the ticket and the prompt left the following judgments
open. The tree answered each one, and the grounds are in `spec.md` or in
`plan.md`'s Alternatives table. They are listed here so nobody reopens them:

- **What the class is.** It is the positions a program word can stand in
  (P1–P13), every redirection form, and the four readers that ask where a
  program stands. It is not the report's shapes alone (`spec.md` §*The class,
  enumerated*). The grammar found shapes the report did not list:
  `2>/dev/null git commit -m x`, `git 2>/dev/null commit`, `2>/dev/null eval`,
  `2>/dev/null cd W`, `(sh -c …)`, the `su` and `env -S` pickers, and
  `sudo -s` and `flock -c`. All are read, not executed.
- **How round 1's controls stay unasked.** By position, never by presence.
  The stand-in is used only where a header cannot be placed, and each control
  is planted in each new position (`spec.md` §*How the controls stay unasked*,
  Alternatives E).
- **Whether to change the splitter for `2>&1`.** No. That moves every
  segmentation and breaks the invariant, so a merged view that adds only what
  neither part found is used instead (Alternatives B, C).
- **Whether a changed unit may drop a base answer.** No. Each keeps it and
  adds (`spec.md` decision 1). That covers even `2>/x/git commit`, which the
  base reads as git.
- **Whether P4 inside a string stays as the base reads it.** No. Where the
  reader cannot tell an option's value from the program, it stops
  (Alternatives F).
- **The depth bound's value.** 32, the one value with a measurement behind it
  (Alternatives G, H).
- **Whether to add a hook timeout.** No. A killed hook is silence
  (Alternatives I).
- **Whether the worktree guard changes.** It classifies a git behind a
  redirection, and W1 does not move its directories (`spec.md` §*What the
  worktree guard sees*).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does the harness cut off a `PreToolUse` command hook when `hooks/hooks.json` sets no `timeout`, and after how long? Round 3 left this open beside a 30 s answer | a measurement: the orchestrator, from the Claude Code hooks documentation or one probe hook that sleeps past a candidate limit. The tree cannot answer it, because nothing in it names the harness's default | **A limit under 30 s**: at `86256492` a deep nesting is cut off, and a cut-off hook is silence, so that shape reads silent there, and the bound is what closes it. **A limit above 30 s, or none**: the bound only saves time | The bound is built either way. Nothing in the design waits on this row | ✅ answered 2026-09-29 by the orchestrator, read from https://code.claude.com/docs/en/hooks: "Defaults: 600 for `command`, `http`, and `mcp_tool`", lowered to 30 only on `UserPromptSubmit`, `PreModelSwitch` and `PostModelSwitch`, and to 10 on `MessageDisplay`. A `PreToolUse` command hook runs up to 600 s, and "A timed-out `command` … hook doesn't block the tool call". So the second option holds: the slowest nesting at `86256492`, 62.1 s in phase 5, finishes inside the limit and denies there too, and the bound only saves time · NAME NOT IN TREE |
| Q2 | The prompt budget. Over every Bash command in the recorded milestone runs (sessions `8cadfa28…`, `30ac0e06…`, `ab2760f5…`, whose transcripts are on the owner's machine), how many move from silent at `86256492` to a stop at head, split into `spec.md`'s cost classes (a)–(e)? | a measurement: phase 6, with a read-only probe that runs both gates' readers over the commands and is deleted afterwards (contract §7). The count is what `CONTRIBUTING.md` asks the pull request to state | **Zero**: the budget is the stops on commits, strings and `watch` at the new positions, which is the fix. **Non-zero**: each command is listed in the phase record with its class. Where one comes from a header spelling the reader could place by position, that spelling is added. The fallback is never removed | Expected zero, and the pull request says so only once it is counted | ✅ measured 2026-09-29 by phase 6: zero. 6,033 distinct (command, directory) pairs from the three sessions' 102 transcripts, main and subagent, read by both gates' readers in a deleted probe; none changes its verdict, so each of (a)–(e) is zero. The probe read 495 commits and 16 unresolved targets alike at both SHAs (`phases/phase-6.md`) |
| Q3 | Which header and redirection spellings arrive from `shlex` as which tokens? For example `f(){`, `(a)`, `a )`, `<< 'EOF'`, `{fd}>f`, zsh `>!f`, and `2> >(tee log)`, whose target is two tokens | the work: phase 1 for redirections and phase 2 for headers. Each phase records every spelling as read by position or left to the stand-in | Not a choice: the rule is fixed. A spelling read by position costs nothing. A spelling left to the stand-in is a stop, and it is counted under Q2 (a) | The stand-in | ✅ answered by phases 1 and 2: every redirection spelling is read by position or by the merged view, none by a stand-in (`phases/phase-1.md`'s table); every valid header spelling is read by position, and only spellings bash refuses fall to the stand-in (`tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py#HEADERS`) |
| Q4 | `sudo -s` and `sudo -i`, `flock -c` and `--command`: do they hand the operand to a shell, and which of their options take a value? `spec.md` states it from memory of the manuals, which is nobody's finding | the work: phase 3, from `man sudo` and `man flock` on the machine it runs on. The manual is the source, and the tree holds no copy | **As stated**: they become hosts, with the shells' string rule. **Not as stated**: the host is left out, and the phase record says why | As stated | ✅ answered by phase 3 from the manuals: `flock` as stated, a host with `-c` and `--command`; `sudo -s` and `-i` not as stated, because `man sudo` escapes the command into one word before the shell's `-c`, so they are left out and a pin says why (`phases/phase-3.md`, `overview.md`) |
| Q5 | Which ledger rows do these edits drift? `spec.md` §*Data & interfaces* lists the expected ones from their anchors | the work: phase 6 runs `evidence-check` on `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md` and re-reads each drifted row in its own file (`CLAUDE.md` §*a change writes fragments*) | Not a choice | The list in `spec.md` | ✅ answered by phase 6: `evidence-check` named 16 drifted anchors. They covered the rows `spec.md` expected, four in `seal/ledger.md` (not two) plus E10, E11, E13, E14, E15, E18 and E19, and also E7, E9, E12, E16 and one row in `seal/releases/0.4.0.md`. That last one was a statement anchor inside `understood` that a refactor had moved out; `understood` was restructured to keep it in place, and the row reads ok again. The other 15 rows were re-read in their own files with dated notes, and E7 and E18 were corrected. After the re-stamp the ledger reads 0 drifted, 0 broken (`phases/phase-6.md`) |
| Q6 | Does a worktree guard case pin a redirected git, or a word glued to `(`, as a word the guard does not read? | the work: phase 1, from `tests/test_the_guard_asks_once_per_session.py#COMMAND_WORD_GROUPS` and the guard's other modules. `1790644505`'s phase 5 moved `nice git` in the same way | **A pin exists**: it moves to the group the guard judges, and `docs/worktree-guard-spec.md` says so. **None**: nothing moves | None moves until one is found | ✅ answered by phase 1: none. `COMMAND_WORD_GROUPS` names no redirected git and no word glued to `(`, and the 26 modules that load the reader passed unchanged; `docs/worktree-guard-spec.md` gains one sentence saying the guard now reads a redirected `git` (`phases/phase-1.md`) |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
