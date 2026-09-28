# Implementation Plan: the sealer's stamp reaches the person it is drawn for

<!-- seal/specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for/plan.md
— HOW, in phases. This is the Design Gate's artifact: where the work alters
observable behaviour, approval of this plan is the gate. -->

Approved 2026-09-28 by the orchestrating session, under the owner's `automation` answer, when `smith` was spawned.

## Summary

The gate stops drawing where nobody can see it. On a sealed, recorded, piped
run it writes the panel's rows to a session-keyed file under the git common
dir and prints one `SEALED … <path>` line. A `Stop` hook in the main session
draws each undrawn file once, as a JSON `systemMessage`, after the turn's
final text. Probe D showed that surface rendering unfolded and in colour on
the owner's screen. A person running the gate in a real terminal still sees
it drawn there, once.

## Technical context

What this builds on (content anchors, read 2026-09-28):

- `skills/verify/scripts/broad_gate.py#gate`: the draw is its last act,
  `sys.stdout.write(... stamp.stamp(rows, args.scale, shape) ...)`, reached
  only after every check passed and, with `--record`, after `seal_record`
  returned 0. **That is exactly the point where the values file is written.**
  The trigger condition (exit 0 and the cell written) is therefore the code
  path itself, not a reading of it.
- `broad_gate.py#panel`: it already builds the rows. The file serialises its
  return value, and nothing else computes them.
- `broad_gate.py#main` and its `__main__`: `pick_shape(sys.stdout)` is asked
  before the streams are reconfigured. The terminal decision (draw here or
  signal) has to be taken from that same early answer, because after the
  reconfigure every stream answers `utf-8`. So `console_wants_letters`
  becomes, or is joined by, the answer to *is stdout a terminal at all*.
  `pick_shape` today folds "not a tty" and "not UTF-8" into one boolean, and
  the build must split them: a cp949 **terminal** still draws, as letters.
- `skills/verify/scripts/seal_stamp.py#stamp`, `#check_scale` and `#main`:
  the reader, `--from`, and `DEFAULT_SCALE` go here. `stamp()` enforces the
  scale floor itself, so a file carrying a bad scale is refused by the
  function that draws.
- `hooks/dispatch.py#GROUPS`, `#merge` and `#main`: a `stop` group, one
  gate. `merge` passes a single JSON object through unchanged (the
  `jsons[0]` path), so `systemMessage` survives the dispatcher. `main`'s
  `event_name` defaults non-`pre-` groups to `PostToolUse`. That is read only
  on the decision path, which this hook never takes, but the build should
  make it say `Stop` for the new group rather than leave a false name in it.
- `hooks/implementer-notice.py`: the shape the new hook copies (payload
  read, opt-in check via `optin`, silent on every failure) and the stance it
  cites.
- `hooks/console.py#to_utf8`: called in the hook's `__main__`, as every
  gate does.

**The failure scenario of the chosen approach, which is what breaks in six
months:**

1. **`CLAUDE_CODE_SESSION_ID` goes away or changes meaning.** The variable
   is undocumented, and it was measured in one version (2.1.283). The files
   then land under `none/`, the hook draws nothing, and the only symptom is
   a missing stamp. **Mitigation built in:** the `SEALED` line says whether a
   session was found, so a sealer's report shows the break on the first run
   after it. Q2 records the remaining measurement.
2. **The early-draw window.** The gate writes the file a few seconds before
   the sealer finishes its report. A main-session turn that happens to end
   inside those seconds draws the stamp before the orchestrator has written
   anything about it. It is still last on that turn's screen, but it is not
   under the result text it belongs to. It is rare, since a background
   sealer's completion is what normally starts the turn that ends with the
   draw. **Deferred remedy, not built:** a `SubagentStop` hook that *arms*
   the sealer's files, with `Stop` drawing only armed ones. It is not built
   because nobody has observed the window, and because whether `SubagentStop`
   carries the parent's `session_id` is one more unmeasured fact.
3. **The hook costs every turn.** `Stop` fires at the end of every
   main-session turn in every opted-in repository: one Python start, about
   92 ms bare (`hooks/dispatch.py` docstring), plus a directory listing.
   The `post-bash` group already pays that after every Bash call, which is
   far more often, so the precedent accepts it. The hook returns before any
   git call when the session's directory does not exist.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| The gate keeps drawing in the sealer (today) | It arrives behind `ctrl+o`, and the 0.15.6 stopgap drew it twice, colourless and cut (issue, 2026-09-28) | Rejected by the owner |
| `PostToolUse` hook on the **sealer's** Bash call | Tool events fire inside subagents (docs, read), so it renders in the sealer's folded output, and it fires before any text follows | Rejected |
| `PostToolUse` hook on a main-session Bash call (the orchestrator runs `seal-stamp --from`) | It renders (probe A), but it fires before the text that follows the call, which breaks *the seal is last*, and it depends on the orchestrator's act | Rejected |
| The orchestrator's own Bash call prints the stamp | It folds at a few lines, and about 10.9 KB of block form enters the orchestrator's context (measured with `wc -c`, relayed) | Rejected. `seal-stamp --from` stays as the by-hand path (S11), not the route |
| `Stop` hook, plain stdout (probe C) | Unneeded now that D is settled. The docs also say plain stdout from most events goes to the debug log | Rejected |
| **`Stop` hook, JSON `systemMessage` (probe D), session-keyed values file under the git common dir** | The three scenarios in §Technical context | **Chosen.** Probe D renders unfolded, in colour, after the final text. The trigger is the gate's own code path. The session key stops a concurrent session in another worktree of the same clone from drawing, and taking this run's stamp |
| Values file in the gate's temp `broad-gate-<random>/`, found by scanning the transcript for the `SEALED` line | The drawing then depends on the sealer relaying one line, which is a session's act (the issue: *never to a session's reading*). The docs also say the transcript is written asynchronously and may lag | Rejected |
| Values file in the work item directory, committed | It edits the tree after the seal (`skills/verify/SKILL.md`: *nothing edits between the broad seal and the PR*), and it puts transient drawn/undrawn state into a durable record | Rejected |
| Key the pending files by the repository alone, with no session | Any main session of the clone draws the stamp, including a concurrent one working on another item | Rejected while the env var holds. It is the fallback if Q2 comes back unequal |
| A piped run without `--record` keeps printing the twin | The body's Done-when says drawing a stamp requires exit 0 **and** the written cell, and that no other path draws one | Rejected. S9 prints one line and draws nothing |
| A hand-run in a real terminal also only signals | A person at their own terminal would see no stamp. The 2026-09-15 rows (*a hand-run prints exactly once*; form chosen against the terminal) are stated to still stand, and the path is unreachable from a tool call (`/dev/tty` measurement) | Rejected. S10 draws once, and only over a written cell (corrected 2026-09-28: a terminal run without `--record` signals, per #400's Done-when; `overview.md`'s divergence row) |
| Delete the file after drawing | It gives the same at-most-once, but the run's values are gone and `--from` has nothing left to reproduce | Rejected in favour of a rename to `.drawn.json` |

## Phases

Vertical slices. Each phase carries the documents its behaviour change makes
false, so the tree never states a surface that is not there.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **The gate signals; the file can be drawn by hand.** `seal_stamp.DEFAULT_SCALE = 0.90` with its reason and the 0.75 candidate; both CLIs default to it. The values reader and `--from` with claim-before-draw. In `broad_gate.gate`: stdout a terminal draws once over a written cell (the form chosen as today; corrected 2026-09-28, see `overview.md`'s divergence row); stdout not a terminal draws nothing, and on a recorded seal writes the file and prints the `SEALED` line (S14 and S15 wording included). `pick_shape`'s two answers are split so the terminal question is asked before the reconfigure. Existing gate cases that read panel rows off a pipe move to reading the values file (Q5 names where). Documents: `broad_gate.py` and `seal_stamp.py` docstrings, `bin/seal-stamp`'s usage comment, and `agents/sealer.md` §*The command* (the exit-0 bullet, and the *arrives as letters* paragraph now saying the gate prints one `SEALED` line, that the stamp is drawn in the session that spawned the sealer after its text, and that the sealer draws nothing, neither with `seal-stamp` nor from the file) | New cases for S1, S2, S7–S15. The four gate test files named in Q5, run narrowly. Every new case seen red once (contract §15): S1 against today's gate, which draws on a pipe; the rest with their assertion's subject reverted | cde753c2 |
| 2 | **The hook draws, and the rule is written where it is read.** `hooks/sealer-stamp.py`: `Stop` only; silent when the payload has `agent_id`, when `hook_event_name` is not `Stop`, when not opted in, or when the session directory is absent; each undrawn file for `session_id`, oldest first, renamed and then drawn; one `systemMessage` with the label line first. `dispatch.py`'s `stop` group and `hooks.json`'s `Stop` entry. Documents: `skills/code-review/orchestration.md`'s closing rule (the stamp is drawn for you at the end of your turn; put the result text first; never draw one, neither with `seal-stamp` nor by relaying the sealer's log, which 0.15.6 did; on a red run relay the `NOT SEALED` lines and nothing is drawn); `skills/verify/SKILL.md`'s **Form** bullet; `docs/the-broad-gate.md`'s new paragraph, with `<!-- specs/1790562543-the-stamp-reaches-the-person-it-is-drawn-for -->`, an `Enforced by:` line naming the hook cases, and a separate `Enforced by: nothing — …` sentence for what the screen shows. Then the ledger fragment `seal/ledger/1790562543-the-stamp-reaches-the-person-it-is-drawn-for.md`, the drifted rows re-read where they live (spec.md §Data & interfaces), and the changelog fragment | Hook cases S3–S6 through `dispatch.py stop`. `tests/test_dispatch.py`, the `hooks.json` cases in `tests/test_chain_hooks_hardening.py`, `tests/test_console_is_not_utf8.py`. Document-pin cases S16, each seen red with its sentence deleted. `tests/test_docs_line_wrap.py` and `tests/test_one_word_one_meaning.py`. `evidence-check` narrowed to this item's fragment | d0f9f125 |

**Two phases, not three.** The documents are split by the behaviour that
makes them false. `sealer.md` becomes false the moment the gate stops
drawing on a pipe, so it rides Phase 1. The orchestrator's rule is true only
once a hook draws, so it rides Phase 2.

**Between the phases the tree draws nothing for a sealer's run.** Phase 1
alone is a state where the stamp exists only as a file. That is acceptable
on a feature branch, which squashes. It is also why the two phases ship in
one pull request and are never released apart.

**S17 is not a phase.** It is read by the owner on the first real sealer run
after this merges, and the overview's `## Not verified` table carries it
with that answerer.

## Operational impact

- **A new hook event.** `Stop` is registered in `hooks/hooks.json`. Every
  opted-in session runs one Python process at each turn's end.
- **New files outside the tree.** `<git-common-dir>/specseal-stamp/<session>/`
  collects one small JSON file per sealed piped run, renamed `.drawn.json`
  once drawn. Nothing prunes them.
- **A piped `broad-gate` no longer prints the letter twin.** Anything
  scripted against the disc on stdout, such as the 0.15.6 stopgap of
  re-printing a sealer's log, gets one `SEALED` line instead.
- **The default scale moves from 1.0 to 0.90** for `seal-stamp` and
  `broad-gate`. `--scale` still overrides it.
- No new dependency and no migration. The cell format is unchanged.
