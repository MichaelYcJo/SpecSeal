# Feature Specification: the commit gate stops asking about commits that are not there (#662, #665)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | Between two designs that catch the same defect, the one that stops to ask a person is the more expensive. The owner pressed `automation`, and that preset promises that nothing stops to ask again. Four permission prompts in one run broke that promise |
| The spawn prompt's constraint, from the owner | No command shape may read silent where `release/v0.16.0`'s gate judges it. A false silent is a real commit nobody judged, and that is worse than a prompt. This outranks the acceptance boxes written into #662 and #665, and it is why neither issue's first box is built as written |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The build owes four things: a test seen red, a stated failure direction, a prompt budget and platform honesty. §*What a change to a gate must carry* below states the direction and the budget, so the pull request inherits them rather than inventing them |
| `docs/commit-review-gate-spec.md` §*commit-review-gate*, the decision table and the paragraph under it | A `deny` addresses the **model** and hands the turn back. An `ask` addresses the **user** with two buttons the model never sees. That split is the whole lever this frame pulls |
| `docs/commit-review-gate-spec.md` §*Why a deny, and why only once* | The gate fires one deny per session per repository and asks every time after that. The paragraph calls the `ask` "also the answer for an environment with nobody to ask". In an automation run that sentence is false, and this work amends it for that case alone |
| `docs/commit-review-gate-spec.md` §*Which repository, and what happens when it cannot be read*, the paragraphs *A failure branch waits for the operator that runs it* and *Two operators consume one, not one* | `;` and a newline run the next command whether or not the `cd` before them worked. So `cd W && x` followed by a newline and `git commit` reaches the session's own directory whenever the `cd` fails. That is #662's shape, and the reading is correct |
| `skills/agent-contract/SKILL.md` §9 and `seal/ledger.md` §*Edits that reach the commit gate*, first row | The gate reads a heredoc body as shell on purpose (legacy #75), and a file edit goes through the `Edit` tool so that no command line reaches the reader at all. That is #665's shape, and the reading is deliberate |
| `docs/worktree-guard-spec.md` §*Creation consent* and `hooks/worktree_consent.py#automation_answered` | The tree already reads the person's `automation` press from the harness-written transcript, and one gate already answers differently because of it. The same reader serves here, with the same standing: the model writes the question and never which option was pressed |
| `skills/agent-contract/SKILL.md` §13 | The transcript's shape is a harness fact. Every way of not finding the press lands on today's behaviour, never on silence |
| `skills/agent-contract/SKILL.md` preamble | A rule kept only in whoever last wrote a spawn prompt goes missing without a trace. The written half of this work goes into the contract, not into a spawn-prompt habit |

## What was measured before this frame

All of this is **read**: the transcripts of this release's run, and the code at
`3911a8cf`. The transcripts were read with a throwaway scanner that ran no
repository code and has been deleted. The executed confirmations are rows in
`questions.md`.

### Where the four prompts came from

Session `ab2760f5-ebe2-4d22-80a0-dc951c2921de`, the milestone-49 run. The
orchestrator's working directory is the main checkout, on `release/v0.16.0`,
which no declaration names. Each `ask` below is the commit gate's
`hook_success` stdout carrying `"permissionDecision": "ask"` (NAME NOT IN TREE: a transcript entry's type).

| When (UTC) | Who | Tool use | Command shape | The stop |
|---|---|---|---|---|
| 2026-09-28 23:39:12 | D's smith (`subagents/agent-aad05d6b045f15f09.jsonl`) | `toolu_01EUoEQqbPzSmjBCvQ8JG6k3` (NAME NOT IN TREE: a transcript id) | `cd <W> && python3 - <<'EOF'` (a Python edit of `changelog.md`) `EOF`, then `git add … && git commit …` on the next line | review arm, naming the main checkout |
| 23:42:24 | D's smith | `toolu_01QC6Go1smDn7UMzs9UBi8Pb` (NAME NOT IN TREE: a transcript id) | `cd <W> && grep -c … ; git add … && git commit …`, with no heredoc at all | review arm, naming the main checkout |
| 23:42:48 | the orchestrator (main transcript) | `toolu_017FSVs2ETf3NqWGCgWe7DPx` (NAME NOT IN TREE: a transcript id) | `cat > <scratch>/issue-newline-cd.md <<'EOF'`. The issue draft quoted a heredoc whose own `EOF` line ended the outer one early, so `git add … && git commit -q -m "…"` became a real command line | review arm, naming the main checkout |
| 23:57:48 | D's smith | `toolu_01Jkofbs4FBjv7C4Lop7LsFz` (NAME NOT IN TREE: a transcript id) | `cd <W> && python3 - <<'EOF'`, a Python patch of `hooks/cmdline.py` whose body holds a `for` loop and test strings carrying `git commit` | `UNREADABLE_CONSTRUCT` |

The person's own message at 23:58:07 quotes the last of these back to the
session.

**Why each was an `ask` and not a `deny`.** At 22:59:41 the orchestrator's own
loop, `for w in …; do IFS=: read d id n <<< "$w"; git -C $d commit …`, met
the construct deny in the main checkout. `already_asked` keys its marker on
the repository's git directory and the session id alone
(`hooks/commit-review-gate.py#already_asked`). A subagent's payload carries its
parent's session id: the guard spec states it, and work item `1790635415`'s
framer measured it on 2026-09-29. So one deny spent the budget for every later
stop in the main checkout, from every agent in the run, and each of those
stops went to the person.

The same loop-variable deny appears in each of the three milestone runs on
disk: `8cadfa28…` at 2026-09-27 23:12:11, `30ac0e06…` at 2026-09-28
02:29:48, and `ab2760f5…` above. Each is the orchestrator committing
`routing.md` for several work items through a loop over `$wt`, `$1` or `$d`.

### What the four have in common

- **Three of the four started `cd <W> &&`, because an agent's shell starts in
  the session's directory at every call.** The harness resets an agent
  thread's working directory between Bash calls. That is why a subagent's
  command reaches its worktree through a `cd`, and why a commit after a `;` or
  a newline has a branch that runs in the main checkout.
- **Three of the four wrote a file through a heredoc.** Two were the smith's
  edits, and contract §9 already says an edit goes through the `Edit` tool, so
  no command line reaches the reader. The smith that broke it had §9 at
  startup, because the installed 0.15.7 contract carries it. The third was the
  orchestrator writing a new file, which is the `Write` tool's job for the same
  reason.
- **In none of them was the gate's reading wrong.** The first two commits
  really do run in the main checkout whenever the `cd` fails. The third is a
  real command line. The fourth is a body the gate reads as shell by design.

### #662's premise, corrected

#662's title says the gate forgets a `cd` at a newline. It does not. It carries
the `cd`'s **failure branch** past the newline, which is what a shell does, so
the commit is judged in both the worktree and the session's own directory. The
23:42:24 row reproduces the stop with a `;` and no newline at all. Round 2 of
work item `1790635415` confirmed the reading of
`hooks/cmdline.py#walk_directories` independently.

### What narrowing the reading cost, the last time it was tried

Work item `1790635415` narrowed the reader two ways. It trusted an existing
`cd` target not to fail, and it read a heredoc body fed to a known interpreter
as data. Its round 2 executed five shapes that the release branch denied and
the narrowed gate read silent: a program flag after the `<<`, a bundled `-Bc`,
`perl <<'EOF' -e …`, and a `$(…)` or `${…;…}` moving the boundary. It found
two more with an earlier segment moving or locking the `cd` target. Its
round 3 found three more behind a `#` glued to the delimiter, which `shlex`
reads as a comment, and three behind an assignment prefix whose `$(…)` moves
the target. In each of those, a real bash ran the commit. Each fix narrowed
further than its proof, and the owner stopped the loop.
(`seal/specs/1790635415-a-gate-that-fails-to-load-says-so/rounds/round-2-report.md`
and `round-3-report.md` on `fix/28-a-gate-that-fails-to-load-says-so`.)

## The decision this frame makes

**The gate's reading does not change. What changes is who a stop is put to,
in a session whose person pressed `automation`.**

**Corrected 2026-09-29 by phase 4 (#669).** The reading changes in one place,
and only toward more stops: phase 1 found that the base reads no commit
behind a reserved word on the same line (`for …; do git commit`, `if …; then
git commit`), the owner's standing rule put the fix on this branch, and
`hooks/cmdline.py#command_word` now reads past such a word, with the segment's
directory unresolved. Every segment it reaches is one where the base found no
command, so no command the base judged reads differently and none reads
silent. `plan.md` phase 4 and `phases/phase-4.md` hold the change and the
argument; the sentences below that call `hooks/cmdline.py` untouched are true
of phases 1–3 and not of the branch.

**Corrected again 2026-09-29 by phase 5 (#670).** Phase 4 found a second
class of the same kind: a commit behind a wrapper the reader did not know
(`exec`, `nice`, `timeout`, `xargs`), inside a string handed to a shell, or
inside a command substitution. Phase 5 reads all three, again only toward
more stops, and this time the gate's own `commit_invocations` and
`_hides_a_commit` change beside `hooks/cmdline.py`: each gains an invocation
for a string or a substitution that holds a commit, and loses none it had.
`phases/phase-5.md` holds the enumeration and the argument.

In such a session, every stop the commit gate makes is a `deny`, addressed to
the model, and never an `ask`. Its reason names the ways on that need nobody.
Everywhere else, the decision is byte-identical to `release/v0.16.0`.

Three properties make this safe by construction, not by a proof about shell
commands:

1. **The set of silent commands cannot move.** The change sits only where a
   stop has already been decided: the choice between `deny` and `ask` in
   `hooks/commit-review-gate.py#main`, and the reason text. Every path that
   returns silence runs before that choice. So does every function that
   decides whether the gate speaks: `hooks/cmdline.py` whole,
   `commit_invocations`, `commit_targets`, `judge` and `names_a_directory`.
   The diff leaves all of them untouched, and a reviewer can check that with
   `git diff` alone. (Corrected 2026-09-29: except `hooks/cmdline.py`'s
   `command_word`, `parse_git` and `walk_directories`, changed by phase 4 for
   #669 in the stricter direction only; the three gate functions and
   `names_a_directory` are still untouched. Corrected again by phase 5, #670:
   `commit_invocations` now also adds invocations for a shell string and a
   substitution, and `hooks/cmdline.py` gains the readers for them and the
   enumerated wrappers; `commit_targets`, `judge` and `names_a_directory` are
   still untouched.)
2. **`deny` is never more permissive than `ask`.** An `ask` lets the commit
   through when a person clicks. A `deny` never does. Where the base asked, the
   head refuses.
3. **Misreading the press only costs turns.** The press is read by the guard's
   existing reader, which every uncertain shape answers `False`, and `False` is
   today's behaviour. A press read where none was meant turns a person's
   button into a model's refusal. Neither way reads a commit silent.

And one written half, so that the refusal fires less often: a new contract
§17 says an agent commits with `git -C <absolute path>` written out, in a
command of its own. Any `cd` before the commit is joined by `&&` alone, and
edits stay with §9.

## Scope

**In:**

1. **The automation reading.** `hooks/commit-review-gate.py` asks
   `worktree_consent.automation_answered(<root of the payload's cwd>,
   session_id, transcript_path)`, and only after a stop has been decided. The
   press is read against the **session's own repository**, not the target. For
   an unreadable target there is no target to read it against, and the
   question it answers is whether anybody is at the keyboard, which is a fact
   about the session. The standing to speak comes from the same place
   (`optin.opted_in(cwd)`).
2. **Deny, always, under the press.** This covers both decision sites in
   `main`: the unreadable-target stop and the resolved-target stop. It covers
   both arms, review and parity. A session with no `session_id` keeps `ask`,
   because there is no transcript to read.
3. **The automation reason.** It replaces the first-time `question_reason` and
   `unreadable_reason` text, and the later `ask_reason`, under the press. It
   says, in this order:
   - This session's person pressed `automation`, so the gate puts no question
     to them. The model does not put one either, and the text does not mention
     `AskUserQuestion`.
   - The ways on, none of which needs a person:
     1. Re-issue the commit so its repository is readable:
        `git -C <absolute path> commit …` in a command of its own, or a `cd`
        joined to the commit by `&&` alone. A `;` or a new line after a `cd`
        also reaches the directory the shell started in, because a failed
        `cd` leaves it there.
     2. A file edit goes through the `Edit` tool, and a new file through
        `Write`. Neither leaves a command line to read.
     3. The waiver in front, `: '[no-review]'; git commit …`, only for a commit
        that belongs to no work item (`skills/implement/SKILL.md` §1: a waiver
        is one command's, and it is the implementer's).
     4. Otherwise, the commit is written down and handed back rather than
        retried.
   - Re-issuing the same command unchanged meets the same refusal.
4. **`docs/commit-review-gate-spec.md`.** The decision table gains the
   automation row. §*Why a deny, and why only once* gains a paragraph that
   reverses its "environment with nobody to ask" sentence for automation
   sessions, with the reasons above. A paragraph records #662 and #665 as
   readings that stay, citing `1790635415`'s rounds. `Enforced by:` lines
   name the new cases.
5. **Contract §17**, `skills/agent-contract/SKILL.md`, next number, at the
   end: *A commit names its repository in the command that makes it*. It
   carries two reasons. First, an agent's shell starts in the session's
   directory at every call, so `cd <W> && …; git commit` has a branch that
   commits there. Second, a loop variable is not a path the gate can read. It
   points at §8 for probes and §9 for edits rather than restating them
   (`tests/test_a_moved_rule_leaves_its_definition.py` refuses a copied
   section).
6. **`skills/implement/orchestration.md`, §*Write the file in a command of its
   own*.** One sentence: commit each work item's `routing.md` in its own
   command with the path written out, citing §17. The loop was measured in
   three runs out of three.
7. **Records.** A ledger fragment, a changelog fragment, and the ledger rows
   the edits drift, re-read. `plan.md` phase 3 lists them.

**Out, each with its reason:**

- **Any change to what the gate reads.** That means `hooks/cmdline.py`,
  `commit_invocations`, `_hides_a_commit` and the heredoc rule. The owner's
  constraint forbids a new silent, and work item `1790635415` measured what
  narrowing costs. (Corrected 2026-09-29: a change that only WIDENS what the
  gate reads came in as phase 4, #669, and a second as phase 5, #670;
  narrowing stays out.)
- **A reading proven by the shell's own parser** (`bash -n`, or printing a
  wrapped function back). It would settle tokenisation, which is where the `#`
  and `$(…)` holes came from. It would not settle the semantic holes: whether a
  `cd` fails is the filesystem at run time, and what an interpreter does with
  stdin is its own command line. `plan.md`'s Alternatives table has the rest.
- **Attended sessions.** Deny once per session per repository, then ask, is
  unchanged. Nothing measured this release argues against it, and it is the
  owner's documented design.
- **A `per axis` answer with its *run end to end* box ticked, and the
  `Automation` row of `routing.md`.** Neither is read, for the reasons
  `docs/worktree-guard-spec.md` §*Creation consent* gives: in every measured
  instance the box label had been reworded, and a `routing.md` is model-written.
  Stated consequence: such a run still meets asks from this gate, as it does
  from the guard.
- **Other gates that ask** (`mode-gate.py`, `review-skill-gate.py`, the
  worktree guard's switch direction). None prompted in the measured run.
- **#665's first acceptance box as written**, *reads silent where its directory
  is declared*. Silence there is the reading change the constraint forbids. S4
  replaces it with a deny under the press.
- **Posting to #662 and #665.** Rewriting their boxes and linking this frame is
  the orchestrator's act. An agent posts nothing (contract §6).
- **Discriminating by `agent_id`.** A subagent in an `Automation: no` run may
  legitimately stop to ask, and one of the four measured prompts was the
  orchestrator's own.

## User scenarios & acceptance *(mandatory)*

"Under the press" means a session transcript holding a harness-written
`automation` answer to the routing question that `automation_answered`
accepts, built by the fixture `tests/test_the_guard_asks_once_per_session.py`
already uses. No case reads a real transcript.

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | A resolved stop, after the budget is spent | Given an opted-in session repository with no declaration, and this session's marker already written. Under the press, `git commit -m x` there → `deny` with the automation reason. The same holds for a parity-arm stop | Through `main()`. Seen red at `3911a8cf`, which returns `ask` |
| S2 | A resolved stop, the first time | The same, with no marker → `deny`, and the reason does not contain `AskUserQuestion` | Seen red at `3911a8cf`, whose `question_reason` instructs `AskUserQuestion` |
| S3 | An unreadable stop, every time | Under the press, `bash <<'EOF'` with `git commit -m x` in the body, and a commit inside a `for` loop over a variable, each issued twice → `deny` both times | Seen red at `3911a8cf`, whose second answer is `ask` |
| S4 | The four measured shapes, rebuilt in temporary repositories | The session directory is opted in and undeclared, and W is declared. (a) `cd W && python3 - <<'EOF'`, body `print(1)`, `EOF`, then `git add f && git commit -m x` on the next line. (b) `cd W && true ; git add f && git commit -m x`. (c) `cd W && python3 - <<'EOF'` whose body carries a `for` loop and a string holding `; git commit -m x`. (d) `cat > f <<'EOF'` whose body holds a bare `EOF` line followed by `git commit -m x`. Under the press: `deny`, twice each. Without it: base behaviour, deny then `ask`. Silent in neither | Through `main()`. Under the press, seen red at `3911a8cf` on the second issue |
| S5 | What the automation reason says | It names `git -C <absolute path> commit`, `&&` alone after a `cd`, the `Edit` and `Write` tools, the waiver last and only for a commit belonging to no work item, handing back otherwise, and that an unchanged re-issue meets the same refusal. It does not name `AskUserQuestion` | Pinned text (contract §14). Seen red by deleting each sentence in turn |
| S6 | Without the press, nothing changes | For these, the output is byte-identical to `3911a8cf`'s: no transcript; a `per axis` press; an `Other` answer starting `automation -`; an `isSidechain: true` entry; a press whose `cwd` is another clone; no `session_id`; an unreadable transcript file | Each asserted against the base decision and reason. The existing suites for this gate pass with no existing case edited |
| S7 | The silent set does not move | (a) `git diff release/v0.16.0 -- hooks/cmdline.py` is empty (corrected 2026-09-29: it holds phase 4's #669 change, `command_word` and the two lines of `parse_git` and `walk_directories` that call it, and phase 5's #670 readers, `RUNNERS`, `reparsed_texts`, `names_an_unknown_command` and `substitution_bodies`, all of which only add stops), and in `hooks/commit-review-gate.py` the functions named in property 1 are unchanged. (b) A corpus of every shape `1790635415`'s rounds 2 and 3 measured as a false silent, rebuilt from their fences, plus #662's reverse direction (`cd <undeclared U> ; git commit -m x` from a declared session directory). Each stops with and without the press, and none is silent | (a) is read at review. (b) is a case, seen red by a mutation that returns silence on the automation branch (contract §15) |
| S8 | Declared targets stay silent under the press | `cd W && git commit -m x` and `git -C W commit -m x`, from an undeclared session directory, with W declared → silent, as at base | Through `main()`. It passes at base too, and is seen red by a mutation that denies before the declaration is read |
| S9 | The written half | Contract §17 exists, is the last section, and carries both reasons, pointing at §8 and §9 without restating them. `orchestration.md`'s paragraph cites §17 | `tests/test_a_moved_rule_leaves_its_definition.py` passes. A case pins §17's two reasons as the tree pins §9's pair (`tests/test_edits_go_through_the_edit_tool.py`) |
| S10 | The policy says what the code does | `docs/commit-review-gate-spec.md` carries the automation row, the amended paragraph and the #662/#665 paragraph, each with an `Enforced by:` line naming S1–S4 and S7's cases | Read at review. The rider and survivor checks pass |

## Data & interfaces

- **Payload fields read**, already present on every `PreToolUse` call:
  `session_id`, `transcript_path` and `cwd`. There is no new field.
- **The reader.** `hooks/worktree_consent.py#automation_answered`, unchanged.
  Whether it is imported in place or moved to a module both gates import is
  `questions.md` Q3. The ledger rows A1–A3 in `seal/releases/0.15.5.md` and W3
  in `seal/releases/0.15.6.md` anchor it.
- **When it is paid.** Only on a stop. The silent paths never read a
  transcript. The docstring records 0.09 s on a 17.3 MB transcript, measured
  by `1790381327`'s round 1.
- **The decision sites.** The two `decide(...)` calls in
  `hooks/commit-review-gate.py#main`. The reason builders are
  `question_reason`, `ask_reason` and `unreadable_reason`, and one new builder
  for the automation text.

## What a change to a gate must carry

- **Failure direction: it blocks more, never allows more.** Under the press,
  every stop that asked now refuses. A wrong refusal costs the model a turn and
  a re-issue. A wrong allow would be a commit nobody judged, which the owner
  ranked worse than a prompt. A misread press only moves a stop between its two
  refusing forms.
- **Prompt budget.**
  - *Automation session:* zero questions to a person from this gate. Base: one
    model-addressed deny per repository per session, then one person prompt
    per stop. Measured: four person prompts in one session.
  - *Attended session:* unchanged, one deny and then an ask per stop.
  - *What an unattended stop costs now:* one model turn per refused command,
    and more if the model re-issues it unchanged. Only the reason's text bounds
    that, and `questions.md` Q2 measures it.
- **Why nothing cheaper reaches the same guarantee.** A narrower reading was
  tried and measured to fail. A written rule alone was measured to fail too: §9
  was in force and broken. Allowing under the press is a false silent. The
  refusal the agent handles itself is exactly the cheaper instrument
  `CONTRIBUTING.md` names.
- **An outage is excluded, not merely unlikely.** A refusal on *every*
  invocation needs a commit that has no readable form. `git -C <absolute path>
  commit` in a command of its own is readable for every repository the gate
  can name. For one it cannot name, the text's last way on is to hand back,
  which ends the run at its destination rather than stalling it at minute
  thirty.
- **Platform honesty.** The transcript reader is the guard's, and so is its
  platform coverage. Nothing here adds process inspection. Windows is answered
  by CI's `windows-latest` leg for the cases, and the transcript location there
  is the guard's existing unknown.

## Open questions → questions.md

No row needs a person. `questions.md` lists the judgments the tickets left open
that the tree answered, then two measurements and two rows for the work.

Framed 2026-09-29 by framer, before the build.
