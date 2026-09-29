# Feature Specification: a gate that fails to load says so

<!-- seal/specs/1790635415-a-gate-that-fails-to-load-says-so/spec.md — WHAT
this work delivers and how we'll know. The policy documents in docs/ outrank
this file; cite them, don't restate. -->

Issue #28, milestone 49 (0.16.0), item D. The owner answered the design
question before the first edit (relayed in the spawn prompt, recorded in
`routing.md` §*Why this way*): **fail open, but say so.** The tool call still
proceeds, the other gates in the group still decide, and the failure is
reported once, naming the gate. Not deny, not ask. This frame decides where it
is said, what "once" is keyed on, where that state lives, and which failures
count.

**The decision, in one paragraph.** `dispatch.py` keeps swallowing a gate that
raises, so every group decides exactly as it does today, byte for byte. What
changes is that the swallow leaves a record: a gate that fails — to load, or
inside `main()` — writes one pending record under the git common dir, keyed by
session and gate. The `stop` group, at the end of the main session's turn,
says every pending record once as a JSON `systemMessage`, the surface
`hooks/sealer-stamp.py` already draws on, and marks each one said. A gate
that stays broken for the rest of the session is not said again.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/commit-review-gate-spec.md` §*Registration — gates run in groups, not one process each* | The ratified rule: "a gate that raises is skipped and the rest of the group still decides — a crashing gate must not block a tool call." Kept whole. This work adds the sentence that it is said, and that section is where it goes |
| `CONTRIBUTING.md` §*House rules*, the bullet *Hooks are Python invoked as `python3 <script>`, with `py -3 <script>` behind it* | "The fallback is safe because `dispatch.py` exits 0 for every decision it makes." A non-zero exit is therefore not available as the way to say it: `||` would start a second interpreter on a consumed stdin |
| `CONTRIBUTING.md` §*House rules*, the bullet *Hooks stay local and quiet* | "No writing outside the repo being worked on, and failure must never block a tool call." The record lives under the repository's git common dir, not in the user's home, and the call is never blocked |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a stated failure direction, a prompt budget, platform honesty. Each is answered below (§*What a change to a gate must carry, answered*) |
| `CLAUDE.md` §*The goal a design is chosen against* | The report is a line, never a question. It adds no prompt and stops nothing, so an unattended run stays unattended |
| `skills/agent-contract/SKILL.md` §12 | The defect is a class: every way a gate's failure reads as silence. §*Scope* enumerates it |
| `skills/agent-contract/SKILL.md` §14 | The report is text a person reads. Its wording is pinned by a case in the same commit that adds it |
| `hooks/implementer.py` module docstring (the stance) and `hooks/sealer-stamp.py` §*Only the main session's `Stop`* | Precedent for a record under the git dir keyed by session, and for a `Stop` draw that is skipped for a payload carrying `agent_id` |
| `CLAUDE.md` §*a change writes fragments, never the shared file* | The changelog entry and the new ledger rows go in this work item's fragments. Rows in `seal/releases/*.md` that this work drifts are re-read in place |

## What was measured before the frame, and by whom

| Fact | Label | Where |
|---|---|---|
| `run_gate` catches `Exception` around both the import (`exec_module`) and `main()`, and returns `""` for either. `SystemExit` is caught around `main()` only, so a `SystemExit` raised at import escapes `run_gate` and ends the whole group | read | `hooks/dispatch.py#run_gate` |
| With `hooks/cmdline.py` broken, `pre-bash` and `pre-agent` both exit 0 with no output | executed 2026-09-02 by an earlier session | the RIDER inside `run_gate` |
| A broken or missing `implementer-mark.py` leaves the worktree guard's `pre-agent` verdict byte-identical | executed 2026-09-02 | `seal/releases/0.4.0.md`, the row citing `dispatch.py#run_gate`; `tests/test_the_implementer_is_recorded.py#test_a_broken_mark_gate_leaves_the_worktree_guards_verdict_alone` |
| `console.py` is imported by all fifteen gates, and `optin.py` by every gate except `session-lease` and `lint-python`. `cmdline.py` is imported by `commit-review-gate`, `worktree-guard`, `implementer-notice` and `worktree_consent`, and `routing.py` by four gates. So a break in `console.py` silences every group at once, `stop` and `session-start` included, and a break in `optin.py` silences thirteen gates | read | the `import` lines of each file in `hooks/` |
| A `Stop` hook's JSON `systemMessage` renders unfolded, after the turn's final text, with line 1 styled as a dim label | executed 2026-09-28, seen on the owner's screen (probe D) | `seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/spec.md` §*What was measured* |
| A `Stop` hook's `systemMessage` does not enter the model's context | executed 2026-09-28 over the session transcript | the same work item's `questions.md` Q1 |
| `SubagentStop` carries the parent's `session_id` and differs from `Stop` by `agent_id` alone | executed 2026-09-28 | the same work item's `questions.md` Q2 |
| A **subagent's** tool-event payload carries the **parent's** `session_id`: this framer's own Bash calls moved the mtime of `<common-dir>/specseal-leases/ab2760f5-…`, the main session's id, to the second of each call, three calls in a row (`session-lease.py` writes that file from `post-bash`) | executed 2026-09-29 by this framer | `stat -f %m` before and after, in this session |
| A dispatcher that cannot start (its file missing) is already said by the harness: the transcript holds a `hook_non_blocking_error` attachment (a harness attachment type, NAME NOT IN TREE), "Hook script appears to be missing … Treating as non-blocking" | read, 2026-09-29, from `~/.claude/projects/…/30ac0e06-….jsonl` (Claude Code 2.1.283) | the transcript survey in this session |
| The hooks reference names `systemMessage` as a field common to every event, "Warning message shown to the user", and says the action proceeds when the JSON carries no decision | read through a summarising fetch of code.claude.com/docs/en/hooks, 2026-09-29. The same fetch said PostToolUse plain stdout goes to the debug log only, while 27 transcript records show `post-bash` plain stdout stored as a hook attachment's `content`. So the fetch is not authority on stdout, and this frame does not rely on plain stdout anywhere | fetch in this session; transcript survey |

## Scope

**In.**

1. **A failure leaves a record.** In `hooks/dispatch.py`, a gate that fails
   during the call is recorded, and the group's stdout is left exactly as it is
   today. Three things count as a failure. Every one of them reads as silence
   today:
   - an exception while loading the file: a missing file, a `SyntaxError`, an
     `ImportError` from a shared module, or any other `Exception` from
     `exec_module`;
   - a **`SystemExit` while loading**. Today it escapes `run_gate` and takes
     every other gate in the group down with it, which breaks the isolation
     property rather than only hiding a failure. `hooks/sealer-stamp.py#load_stamp`
     already catches `(Exception, SystemExit)` around the same call, for
     `seal_stamp.py`'s own interpreter floor;
   - an `Exception` raised by `main()`. `tests/test_gates_do_not_fail_open.py`
     records two measured instances that reached the catch this way (the
     Windows `relpath` raise and the undecodable `routing.md`).

   A `SystemExit` raised by `main()` is **not** a failure. `worktree-guard.py`
   finishes with `sys.exit(0)` at eight sites in `main()` and one in
   `respond()`, so the catch keeps today's `pass`.

2. **The record.** It is a small JSON file at
   `<git-common-dir>/specseal-gate-failure/<session-id>/<gate>.pending`, created
   exclusively, so two concurrent hook processes write it once. It holds the
   group, whether the failure was at load or at run, the exception's class
   name, and the first line of its message. It is written only when all of
   the following hold:
   - the payload parses and carries a `session_id`. The id and the gate name
     are `basename`d before they become path parts, as
     `worktree-guard.py#already_asked` does for the same measured path escape;
   - the payload's `cwd` resolves to a git common dir;
   - the repository is opted in, asked of `optin.opted_in`. **Where `optin.py`
     itself cannot be imported, the answer is "cannot tell", and the record is
     written.** A broken `optin.py` silences thirteen of the fifteen gates,
     so it is the last state that may go unsaid;
   - no `<gate>.reported` exists beside it.

   The report path imports no module under `hooks/` except that guarded
   `optin` lookup. It must not depend on the module whose failure it reports.

3. **The draw.** The `stop` group, after its own gates have run, reads the
   pending records of the payload's `session_id`. Each one it can read is
   claimed by renaming it to `<gate>.reported` and is then said. The
   renaming happens before anything is printed, which is
   `skills/verify/scripts/seal_stamp.py#claim`'s shape. A record for a gate
   of the `stop` group itself is written first and said in the same
   invocation. The payload's `cwd` is resolved to its common dir by walking up
   to the `.git` entry, as `hooks/sealer-stamp.py#toplevel` does, so a turn
   end in a main checkout starts no process when nothing is pending. Nothing is
   drawn for a payload carrying `agent_id`, for another session's records, or
   in a repository not opted in.

4. **What is said.** It is one JSON object, `{"systemMessage": …}`:
   - **line 1** is a label that names what this is and how many gates it
     covers, because the harness shows it as `Stop says: <line 1>`;
   - **one line per gate**, oldest record first, by the `at` pair each record
     carries rather than by the file's time, which records written in one
     call can share (*corrected after Windows CI*, see §*Data &
     interfaces*). Each line names the gate
     file, load or run, where it failed, and the exception's class and first
     line. A load failure names every group that loads the gate's file, and a
     run failure the group it was seen in (*inferred in round 1's fix pass*,
     🟡 1). It says that the calls went ahead and that the other gates in the
     group
     still decided;
   - **the closing sentence** says that this is said once per session and
     that nothing was blocked.

   Where the `stop` group's own output is a `systemMessage` (the sealer's
   stamp), the report goes **before** it, in the same message. The stamp stays
   the last thing on the screen, which #400 decided. Where the group printed
   nothing, the report is the whole output.

5. **Every group is covered by the same path.** `pre-bash`, `pre-agent`,
   `pre-skill`, `post-bash`, `post-agent`, `post-edit` and `session-start`
   record a failure, and `stop` both records and draws. `GROUPS` and `EVENTS`
   are not changed.

6. **The words this makes false are corrected in this work item.**
   - the RIDER inside `run_gate` is resolved and removed. The comment that
     replaces it says what the catch now does;
   - `hooks/dispatch.py`'s module docstring gains that a failure is said;
   - `hooks/implementer.py`'s module docstring has a sentence saying a gate that
     quietly stops running would turn the notice off "and nobody would learn
     that it had". That sentence becomes false and is corrected;
   - `docs/commit-review-gate-spec.md` §*Registration* gains the paragraph
     and an `Enforced by:` line;
   - both READMEs change together (house rule): one sentence in the
     introduction to *The gates* / *게이트*.

7. **The ledger.** New rows go in `seal/ledger/1790635415-a-gate-that-fails-to-load-says-so.md`.
   Two existing rows drift, because this work edits the unit they cite, and
   each is re-read in place with a dated note:
   - `seal/releases/0.4.0.md`, the row citing `hooks/dispatch.py#run_gate`.
     Its claim ("byte-identical") stays true under this design;
   - `seal/releases/0.15.7.md` N8, the row citing `hooks/dispatch.py#main`.

**Out.**

- **Failing closed**, whether deny or ask. The owner rejected it on
  2026-09-29, and `CONTRIBUTING.md` independently calls a deny that fires on
  every invocation in some environment an outage.
- **Telling the model.** The report goes to the person. `plan.md`'s
  Alternatives table has the grounds.
- **Saying it inside the failing call.** Also in the Alternatives table.
- **`merge()`'s existing drops.** Two cases exist. Plain texts vanish when
  another gate in the same group prints JSON, and a second gate's
  `systemMessage` vanishes when the first JSON carries none. Neither is this
  class: in both the gate *ran* and its output is lost in merging. And no
  group emits either combination today (read: every `post-bash` gate prints
  plain text, and every `session-start` gate prints a `systemMessage`). This
  work's own draw does not pass through `merge()`. It is added after the
  merge, so neither drop can reach it.
- **The dispatcher failing to start.** A missing or unparseable `dispatch.py`
  or a missing interpreter is already said by the harness as a non-blocking
  hook error (measured above).
- **A gate's timeout**, which is the harness's.
- **A `SystemExit` from `main()` with a non-zero code.** No gate raises one
  (read: every `sys.exit` in `hooks/` is `sys.exit(0)`), and changing its
  meaning is a separate decision.
- **`hooks/config.py`.** Work item B (#584) may change it in parallel. Nothing
  here needs it.
- **Issues #26 and #27.** #26 is already closed (0.3.0 shipped the mark gate,
  with the isolation measured). This work removes the precondition #27 names
  and builds nothing of #27.

## User scenarios & acceptance *(mandatory)*

`record` below means the `.pending` file of item 2. `A broken gate` is a copy
of `hooks/` in which one gate's file is replaced by `def broken(:\n`, the
shape `test_a_broken_mark_gate_leaves_the_worktree_guards_verdict_alone`
already uses. Every case drives `dispatch.py` as a subprocess, which is what
production spawns.

| # | Scenario | Given / When / Then | Verifiable how |
|---|---|---|---|
| S1 | **A broken gate is not silent** (the issue's third box) | Given an opted-in repository and a copy of `hooks/` with `commit-review-gate.py` broken, when `pre-bash` runs `git commit -m x` for session X and then `stop` runs for X, then the `stop` output is one JSON object whose `systemMessage` names `commit-review-gate.py`, `pre-bash`, load, and `SyntaxError` | a dispatch case; **seen red against the current `dispatch.py`**, where `stop` prints nothing |
| S2 | The group decides as before | Given S1's broken copy, the `pre-bash` stdout is byte-identical to the same call with `commit-review-gate.py` removed from the copy | same case |
| S3 | It is said once | Given S1 has drawn, when `pre-bash` fails again for X and `stop` runs again for X, then the second `stop` prints nothing and no new `.pending` exists | same case, second round |
| S4 | Per session | Given S3, when the same happens for session Y, then Y's `stop` says it | same case |
| S5 | A failure inside `main()` | Given a gate whose `main()` raises `RuntimeError("boom")` after import succeeds, then the record says run, not load, and names `RuntimeError: boom` | a dispatch case with a planted gate in a copied `hooks/` |
| S6 | A shared module breaks several gates | Given `cmdline.py` broken, when `pre-bash` and `post-bash` each run once for X, then `stop` names `commit-review-gate.py` and `worktree-guard.py`, which are the `pre-bash` gates importing it, and `implementer-notice.py` and `worktree_consent.py` from `post-bash`, one line each, and no gate that does not import `cmdline.py` | dispatch case |
| S6b | The module the opt-in question needs is the broken one | Given `optin.py` broken in an opted-in repository, when `pre-bash` runs and then `stop` runs for X, then `stop` names all three `pre-bash` gates (`worktree-guard.py` reaches `optin.py` through `worktree_consent.py`) and `sealer-stamp.py`, which fails in the `stop` group itself and is said in the same invocation, one line each | dispatch case |
| S7 | `SystemExit` at load is isolated | Given a gate whose module body calls `sys.exit(0)` placed before `commit-review-gate.py` in a group, when the group runs a commit in an opted-in repository, then the commit gate's deny is still printed, dispatch exits 0, and the planted gate is recorded as a load failure | an in-process case in the shape of `test_dispatch.py#test_a_crashing_gate_does_not_take_the_group_down`; **seen red against the current `dispatch.py`**, where the group prints nothing |
| S8 | Not opted in | Given a repository without `seal/` and a broken gate, when a group and then `stop` run, then no `specseal-gate-failure` directory exists and `stop` prints nothing | dispatch case |
| S9 | Beside the stamp | Given a pending values file for X (the sealer-stamp fixture) and a pending failure record for X, when `stop` runs, then one `systemMessage` carries the report first and the whole stamp last, with the stamp's label line and block unchanged | a case in or beside `tests/test_the_stamp_reaches_the_person_it_is_drawn_for.py` |
| S10 | A subagent's failure reaches the main session | Given a `post-bash` payload for X carrying `agent_id`, which fails a gate, when a `Stop` for X without `agent_id` runs, then it is said. A `Stop`-shaped payload carrying `agent_id` draws nothing and leaves the record pending | dispatch case |
| S11 | The isolation property stands | `tests/test_dispatch.py#test_a_crashing_gate_does_not_take_the_group_down` and `tests/test_the_implementer_is_recorded.py#test_a_broken_mark_gate_leaves_the_worktree_guards_verdict_alone` pass **unchanged** | the two existing cases |
| S12 | It never decides | No output this work adds carries `permissionDecision` or `decision`, and `dispatch.py` exits 0 in every case above | asserted in S1, S7 and S9 |
| S13 | Nowhere to write | Given a payload with no `session_id`, or a git common dir that cannot be written, then nothing is recorded, nothing raises, and the group's stdout is unchanged | dispatch case; the unwritable half built by making `specseal-gate-failure` a file rather than by `chmod`, because the CI job runs as root (`test_gates_do_not_fail_open.py` records why) |
| S14 | The words are pinned | The label line and the per-gate line are asserted as text (contract §14). `docs/commit-review-gate-spec.md` §*Registration* names the case that enforces it | the S1 case asserts the text; a doc-pin assertion in the style the repository already uses |

## Data & interfaces

**The record.** `<git-common-dir>/specseal-gate-failure/<session-id>/<gate>.pending`,
then `<gate>.reported` once said. `<gate>` is the file name as `GROUPS` spells
it, for example `commit-review-gate.py`. The body is JSON with five keys:
`group`, `phase` (`load` or `run`), `error` (the class name), `message`
(the first line of `str(exc)`, capped at a length the work chooses) and
`at`, `[the writer's clock in nanoseconds, the gate's place among that
call's failures]`, which is what the report is ordered by. `at` was added
after Windows CI said two records in name order: a file's time can be equal
for records one call writes, on NTFS at 100 ns and on any file system that
sets it at a coarser tick. A record with no `at`, or one that is not two
integers, is ordered by its file's time, and name order breaks a tie
(*inferred during implementation*). The
body is data a newer or older plugin may write, so a body the drawer cannot
read still yields a line naming the gate from the file name alone. Unlike a
stamp, the gate's name is the whole of the report's value, and it is
readable without the body.

**The output.** `{"systemMessage": "<label>\n<one line per gate>\n<closing sentence>"}`,
with the stamp's own `systemMessage` appended after a blank line where one
exists. The exact words belong to the work and are pinned by S1 and S14.

**Interpreter.** The report path runs under whatever `python3` the harness
finds, 3.9 on a stock macOS (`hooks/sealer-stamp.py`'s docstring), so it uses
nothing newer. It must not import `seal_stamp.py`, whose floor is 3.12. Its
claim is a plain `os.replace`.

**Cost.** The path through `dispatch.py` when nothing fails does no new work
in any group but `stop`. At `stop` it does a walk up from `cwd` and one
directory check, and it starts no process in a main checkout. On the failure
path it pays for resolving the common dir and asking `optin.opted_in`, once
per failing gate per call. The work measures the `stop` delta and records it
in its phase record.

## What a change to a gate must carry, answered

- **Test seen red:** S1 and S7, against the current `dispatch.py`.
- **Failure direction:** unchanged. Every call a gate's failure allowed
  before, it still allows. The work adds a line at the end of the turn. Where
  the record cannot be written, the result is today's silence, and the
  frame accepts that. A read-only git dir already disables every marker in
  this plugin.
- **Prompt budget:** zero. A `systemMessage` asks nothing. At most one line
  per broken gate per session per clone, and none at all in a healthy
  install.
- **Platform honesty:** `os.replace` and exclusive create behave the same
  on Windows. The path parts are `basename`d on both. No process inspection is
  involved. The Windows render of a `Stop` `systemMessage` is unmeasured,
  which is the same open row #400 carries (its `questions.md` Q4).

## What cannot be checked, stated

- **A healthy install says nothing, and so does a broken install whose
  records could not be written.** Those two states produce the same screen.
  That is the residue of fail-open, now narrowed from every failure to an
  unwritable git dir.
- **A session that ends its turns in a different clone** from the one a
  failure was recorded in does not see that record. This is the grain that
  `implementer-notice.py` already states: once per repository per session.
- **Whether a person reads the line.** This is the same as for every
  `systemMessage` this plugin prints.

## Open questions → questions.md

Anything a planner must answer lives in questions.md, not inline — unanswered
questions buried in prose read as decided.

<!-- The line below is the framer's mark, and it is the only evidence in the
     TREE that the framing happened — the existing framer mark lives in the
     repository's git dir, and a git dir does not travel, so CI cannot see it.
     Fill in the date and `<who>`; `<who>` takes the two values the `Planning`
     row of `routing.md` takes, `framer` or `the session`, and a mark that
     disagrees with that row is refused at the pull request rather than
     guessed at.
     The shape — verb, date, who, the moment — is the one `routing.md` and
     `plan.md` already end with, which is what keeps three feet-lines from
     becoming three conventions. -->

Framed 2026-09-29 by framer, before the build.
