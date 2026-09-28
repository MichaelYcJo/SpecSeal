# the sealer's stamp reaches the person it is drawn for — questions for the planner

<!-- seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

**No row below needs a person, and none blocks the build.** Issue #400 left
the following judgments open. The tree answered them, and the grounds are in
`plan.md`'s Alternatives table or in `spec.md`. They are listed here so
nobody reopens them as questions:

- **Which `Stop` output shape.** It is the JSON `systemMessage`. Probe D,
  seen on the owner's screen on 2026-09-28, showed it unfolded, in colour,
  and after the final text.
- **Whether `Stop` fires at a subagent's end.** The docs (read) say
  `SubagentStop` is that event. The hook also returns silently on any payload
  carrying `agent_id`, so the answer no longer matters to correctness (S5).
- **Where the values file lives.** It goes under the git **common** dir,
  keyed by session, because the sealer's `--root` and the orchestrator's
  `cwd` are different worktrees of one clone in this very run.
- **Whether a piped run without `--record` draws.** It does not. The body's
  Done-when requires exit 0 and a written cell.
- **Whether a hand-run in a real terminal draws.** It does, once, and only
  over a written cell (corrected 2026-09-28 by the build: a terminal run
  without `--record` draws nothing, per #400's Done-when). The 2026-09-15
  rows still stand, and no tool call can reach that path.
- **Delete or keep a drawn file.** It is renamed to `.drawn.json` before
  printing, which gives at most one drawing and keeps the values.
- **The per-turn cost of a `Stop` hook** (one Python start at each turn's
  end). It is accepted on the precedent of the `post-bash` group, which pays
  the same after every Bash call.
- **Relabelling `seal-stamp`'s sample.** It is out of scope. No rule asks a
  session to draw any more, so the sample is not a cheap path to anything.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does a `Stop` hook's `systemMessage` enter the model's context on the next turn? The earlier four-variant probe observed that none of its output did. The D-only re-probe did not look, and the docs, through a summarising fetch, said both "shown to the user" and "added to Claude's context" | **a measurement**, taken after the first real draw: the session's transcript `.jsonl` was searched for the label line. One command | **Not in context:** the stamp costs the orchestrator nothing, and `docs/the-broad-gate.md` may say so. **In context:** about 11 KB per stamp lands in the one context a release cannot replace, and the paragraph says that instead. The code is the same either way | Unstated. The policy paragraph makes no claim about context cost until this is measured | ✅ Not in context. Executed 2026-09-28 by the orchestrating session over its own transcript: each draw is stored as an `attachment` of type `hook_success` whose model-facing `content` is empty and whose `stdout` holds the drawing, and no stamp text reached the model's context across three draws. Closed with overview.md's Q1 row. |
| Q2 | Does the `Stop` payload's `session_id` equal the `CLAUDE_CODE_SESSION_ID` a subagent's Bash sees? Measured so far, in this framer (a subagent, Claude Code 2.1.283): the variable is present and equals the id naming the parent's scratchpad directory. The docs' `Stop` example shows `scratchpad_dir` — a field of the harness's payload, NAME NOT IN TREE — ending in `session_id`. Nobody has compared the two directly | **a measurement**, and only the main session can take it, because only it hosts a `Stop` hook. A throwaway `Stop` hook that logs `session_id` beside a subagent's `echo $CLAUDE_CODE_SESSION_ID` settles it | **Equal:** the plan stands. **Not equal:** key the pending files by the repository alone (`plan.md` Alternatives, the fallback row). That is a one-constant change in the hook's lookup, and it accepts that a concurrent session of the same clone could draw another item's stamp | Equal. If wrong, the failure is the safe one: nothing is drawn, and the `SEALED` line still reaches the report | ✅ Equal, so the plan stands. Executed 2026-09-28 by the orchestrating session: a logging-only `Stop`/`SubagentStop` hook logged 9 events. The `Stop` payload's `session_id` was `30ac0e06-a6b6-40f6-ba38-d88db37d3321`, the value `CLAUDE_CODE_SESSION_ID` held in the main session's Bash and in a subagent's, and the main transcript's basename. Its `agent_id` was absent and its `cwd` was the main checkout, not the worktree the sealer runs in, which is why the values live under the git common dir. `SubagentStop` fired 8 times with the SAME `session_id` and with `agent_id` present, so `agent_id` is the only field that tells the two apart, and it is the guard the hook uses (S5). Relayed to smith by the orchestrator |
| Q3 | Does the early-draw window (`plan.md` §*Technical context*, scenario 2) occur in a real run? That is, a main turn ending between the gate's exit and the sealer's report, which draws the stamp above the text it belongs under | **a measurement**, on the next release run. Watch whether any stamp arrives before the orchestrator's result text | **Never seen:** nothing to build. **Seen:** add the `SubagentStop` arming hook, which first needs its own measurement of that event's `session_id` | Not built | ⬜ |
| Q4 | Does the block form render through the hook on Windows (Windows Terminal, and a cp949 console)? | **a measurement** on a Windows machine. No session here has one. The answerer is the repository owner, or whoever next runs a session on Windows | **Renders:** nothing. **Mojibake:** the hook picks the letter twin on Windows. That is a one-line change, and it gives up the colour there | Block form everywhere, carried as an overview `## Not verified` row | ⬜ |
| Q5 | Which existing gate cases read the disc or a panel row off a **piped** run, and so stop observing anything once the gate signals instead of drawing? Found by `git grep` so far: `tests/test_the_seal_is_taken_once_by_the_sealer.py`, `crown_of() in out.stdout` in the sealed-run case; `tests/test_the_gate_names_every_step_ci_runs.py`, the `not answered` row rendered from `result.stdout`. The absence assertions (`crown_of() not in out.stdout` on a red run, a refused record and a failing chain check) keep passing and **stop proving anything** | **the work**. Phase 1 meets each one when the gate changes | Each positive reading moves to the values file (a `--record` fixture) or to `panel()` directly, because a run without `--record` writes no file (S9). Each vacuous absence gains *and no values file exists*, which is S7 and S8 | Phase 1 decides case by case and records it in `phases/phase-1.md` | ✅ Decided by the work in Phase 1 (`cde753c2`): seven positive readings moved and five reachable absences gained `and no values file exists`, each named in `phases/phase-1.md` §*What this phase found* |
| Q6 | The exact wording of the `SEALED` signal line and of the hook's label line | **the work**. Fixed by the cases that pin them (contract §14) | Constrained by `spec.md` §*Data & interfaces*: it starts with `SEALED`, carries `<tree> against <base>`, and names the path; the label is not blank | As `spec.md` states | ✅ Decided by the work: the gate's line is `SEALED   <tree> against <base>` and one clause saying where the stamp will be drawn, or that nothing was recorded, no session was found, or the values could not be written (`broad_gate.py`'s `NOTHING_RECORDED`, `NO_SESSION_FOUND`, `DRAWN_AT_TURN_END`, `VALUES_UNWRITTEN`); the hook's label is `SEALED <tree> against <base> · <work item id>` (`seal_stamp.label`). Each is pinned by the cases `phases/phase-1.md` and `phases/phase-2.md` name |
| Q7 | Does the suite, run under Claude Code, leak the real `CLAUDE_CODE_SESSION_ID` into the gate's subprocesses and write values files keyed to the live session? | **the work**. The files would land in each fixture's own git dir, which the live hook never reads, so this is about determinism, not a leak into the session | The gate cases set or clear the variable explicitly, beside `env_without_a_pull_request` | Set or cleared explicitly in every new case | ✅ Decided by the work in Phase 1: `env_without_a_pull_request` and the gate module's autouse fixture clear it for every case, and a case that wants a session passes one |

**`Who can answer` takes one of three values and nothing else.**

- **a person**: what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of
  row that blocks the build.
- **a measurement**: a probe, a command or a count settles it, so asking a
  person is the wrong instrument.
- **the work**: unknowable at framing time. The phase that meets it decides
  it there and records a divergence row.

**The framer opens rows and does not own their answers.** The `Status`
column is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
