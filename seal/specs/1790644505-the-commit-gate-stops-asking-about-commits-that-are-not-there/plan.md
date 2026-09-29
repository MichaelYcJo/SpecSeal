# Implementation Plan: the commit gate stops asking about commits that are not there (#662, #665)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-29 by the orchestrating session, when `smith` was spawned. The approval ratifies the reversal the frame names: under an `automation` press, `docs/commit-review-gate-spec.md`'s `ask` for an environment with nobody to ask becomes a `deny` addressed to the model. The owner had said, in this run, that an automation run stopping for the person to choose is the failure to avoid, which is what the reversal answers.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. A later session, a reviewer and CI all read the tree, and a plan
with nobody's name on it is indistinguishable from one nobody approved.

Where the session builds the work itself, `<who>` is still a person and the
moment is still the first edit rather than a spawn — say so in place of the
clause about `smith`, and keep the shape.

That shape is `templates/sdd-routing.md`'s, whose `Answered <date> by <who>,
before the first edit.` line records the other batch the same way: the verb,
the date, who, and the moment it was given. The two are pinned against each
other, so neither spelling can drift into a second convention for one kind of
fact. -->

## Summary

In a session whose person pressed `automation`, the commit gate refuses every
command it stops (`deny`, addressed to the model) instead of asking the person
after the first refusal. The reason names the ways on that need nobody. What
the gate reads is untouched, so no command becomes silent. A new contract
section tells agents the commit shape the gate reads without a stop, so the
refusal fires less often.

**Read this before approving.** The plan reverses one sentence of
`docs/commit-review-gate-spec.md` §*Why a deny, and why only once* for
automation sessions: "Every attempt after the first meets the plain `ask` —
which is also the answer for an environment with nobody to ask". Approving this
plan is where that reversal is ratified. `spec.md` §*The decision this frame
makes* holds the grounds.

## Technical context

What this builds on, by content anchor:

- `hooks/commit-review-gate.py#main`: the two `decide(...)` sites. The
  unreadable branch decides `"deny" if first else "ask"`, where `first` is
  `bool(session) and not already_asked(cwd, here, session)`. The resolved
  branch does the same through `already_asked(target, git_dir, session)`.
  Everything above those two lines decides whether the gate speaks at all, and
  none of it changes.
- `hooks/commit-review-gate.py#already_asked`: one marker per git directory
  per session. Every agent in a run shares the parent's session id, so the
  first stop in a repository spends the budget for the whole run. That is how
  the measured run's four stops each became a person prompt (`spec.md`
  §*Why each was an `ask` and not a `deny`*).
- `hooks/commit-review-gate.py#question_reason`, `#ask_reason` and
  `#unreadable_reason`: the three texts the automation reason stands in for.
  `question_reason` and the unreadable first-time text instruct the model to
  put the choice up with `AskUserQuestion`. A subagent has no such tool, and in
  an automation run the main session must not use it.
- `hooks/worktree_consent.py#automation_answered`: the press reader, with
  four conditions and fail-closed on every shape. It is called here with the
  root of the payload's `cwd`, which is the clone the press was given in: every
  measured press has the main checkout as its `cwd`.
- `docs/commit-review-gate-spec.md` §*commit-review-gate*'s decision table,
  §*Why a deny, and why only once*, and §*Which repository, and what happens
  when it cannot be read*.
- `skills/agent-contract/SKILL.md` §8, which covers `git -C` for probes, and
  §9, which covers edits through `Edit`. §17 is new and sits at the end
  (§*How the sections are numbered*).
- `skills/implement/orchestration.md` §*Write the file in a command of its
  own*: where the orchestrator's routing commits are described.

**What breaks in six months.**

- *The harness renames `toolUseResult` or `answers`.* The reader returns
  `False`, and automation runs meet asks again. That is visible, not silent,
  and the guard breaks the same way at the same moment. `seal/releases/0.15.5.md`
  row A2 already names this risk for the guard.
- *A model meets the refusal and re-issues the same command.* Only the
  reason's text stands between that and a loop of turns. `questions.md` Q2 is
  the count that says whether it happens.
- *A model reaches for `[no-review]` where a person used to click Approve.*
  The waiver stays visible in the command, which a click never was. The reason
  offers it last, and only for a commit that belongs to no work item.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. Narrow the reading**, as work item `1790635415` did: trust an existing `cd` target not to fail, and read a heredoc body fed to a known interpreter as data | Measured: round 2's report tables eight commands and round 3's six that read silent where `release/v0.16.0` judged them, and a real bash ran the body or landed the commit for every one it ran (`rounds/round-2-report.md` and `rounds/round-3-report.md` on `fix/28-a-gate-that-fails-to-load-says-so`, the rows marked `silent`). The rule the owner approved in #665 was stated correctly and implemented narrower than it at every round | Rejected. It breaks the constraint, and the class has shown no end |
| **B. Narrow by construction**: have the shell's own parser report the structure (`bash -n`, or wrap the command in a function and print it back), then decide on that | It settles tokenisation, where the `#` delimiter and the `$(…)` boundary holes came from. It does not settle semantics. Whether a `cd` fails is the filesystem when the command runs, and an earlier segment or an assignment prefix changes it (round 2's `mv`/`chmod`, round 3's `X=$(mv …)`). What an interpreter does with stdin is its own command line: a flag after the `<<`, a bundled `-Bc`, a script argument. The parser would also have to be the right one: the Bash tool runs the user's shell, which on the owner's machine is zsh with the harness's snapshot of aliases, so `python3` need not be `python3`. And it adds a process to every Bash call in a hook group that `docs/commit-review-gate-spec.md` §*Registration* keeps in one interpreter | Rejected. What is left after it is the hand-written allowlist that A already measured |
| **C. Allow under the press**, following the guard's precedent (the press counts as consent) | The guard's allow is consent to create a worktree. Here the stop names a repository no declaration covers, or one the gate could not read at all, and the unreadable branch runs before any declaration is consulted. An allow there is precisely the false silent: a real commit, into a repository nobody declared, judged by nobody | Rejected. It breaks the constraint |
| **D. Deny, always, under the press** | A model that cannot find a readable form re-issues and is refused again, turn after turn. A model may type `[no-review]` where a person would have clicked. A press read wrongly turns a person's button into a refusal | **Chosen.** No command becomes silent, and the person is never asked. Each failure costs turns, bounded by the reason's text and measured by Q2 |
| **E. The agent side alone**: a contract rule on commit shape, and §9 as it stands | §9 was in force and broken, since two of the four measured prompts followed heredoc edits. The `cd … ; git commit` shape is in no document for real work, only for probes (§8). A written rule alone left the measured run prompted, and "proven mechanisms beat written rules" is this project's stated preference | Kept as the second half of D, not on its own |
| **F. Change nothing, and record why** | The owner was prompted four times in one run whose preset promised no question. The promise stays broken | Rejected |
| **G. Deny always, in every session** | It reverses the once-per-session design for attended sessions too. Nothing this release measured argues against that design, and there a person is present to answer the `ask` | Rejected. Out of scope |
| **H. Deny always for a subagent's call** (the payload carries `agent_id`) | A subagent in an `Automation: no` run may legitimately stop to ask. And one of the four measured prompts was the orchestrator's own, which has no `agent_id` | Rejected. Automation is the discriminator, and the caller is not |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The gate. `main` reads the press, only after a stop is decided, through `worktree_consent.automation_answered` against the root of the payload's `cwd`. Under the press both decision sites return `deny` with the automation reason, for both arms. A new reason builder holds `spec.md` §*Scope* item 3's text. `hooks/cmdline.py` and every function named in `spec.md` property 1 stay byte-identical. `docs/commit-review-gate-spec.md`: the automation row, the amended §*Why a deny, and why only once*, the #662/#665 paragraph, and `Enforced by:` lines | S1–S4 through `main()`, each seen red at `3911a8cf`. S5, seen red by deleting each sentence. S6 against base output. S7 (a) read in the diff, and S7 (b) seen red by a mutation that returns silence under the press. S8 seen red by a mutation that denies before the declaration is read. `questions.md` Q1, taken once outside the suite. The modules for this gate, and the guard's `tests/test_the_guard_asks_once_per_session.py`, which must pass untouched | 9ee5b9b1 |
| 2 | The written half. Contract §17, *A commit names its repository in the command that makes it*, at the end, pointing at §8 and §9. One sentence in `skills/implement/orchestration.md` §*Write the file in a command of its own* citing it | S9. `tests/test_a_moved_rule_leaves_its_definition.py`, `tests/test_one_word_one_meaning.py`, and a new case pinning §17's two reasons, seen red with each reason deleted | 36e3d994 |
| 3 | Records. The ledger fragment `seal/ledger/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there.md` gets new rows for S1–S4, S7 and §17. The changelog fragment `seal/specs/1790644505-…/changelog.md` is written. Rows the edits drift are re-read in place, and `docs/commit-review-gate-spec.md`'s headings are cited by `seal/releases/0.15.1.md` S2 and `seal/releases/0.4.0.md`. If Q3 moves the reader, rows A1–A3 of `seal/releases/0.15.5.md` and W3 of `seal/releases/0.15.6.md` are REMOVED there and re-claimed in the fragment (`CLAUDE.md` §*a change writes fragments*) | `evidence-check` on the fragment and each file touched. `rider_check.py`. The survivor sweep over the corrected sentences | 2e205343 |
| 4 | **A commit after `do`, `then`, `else` or `elif` is judged (#669).** Added 2026-09-29 by the orchestrating session at the owner's standing request: phase 1's builder found, and the orchestrator confirmed by executing it at `3911a8cf`, that the commit gate reads no commit in `for x in a; do git commit -m x; done`, `while …; do git commit …; done` or `if true; then git commit …; fi`. The gate reads the segment's first word, a reserved word, and finds no command, so a real commit goes unjudged. The reading gets **stricter**: after a reserved word that begins a command list (`do`, `then`, `else`, `elif`, `!`, `{`, `(`), the next word is read as the command word. This is the one change to `hooks/cmdline.py` in this work item. Its direction is the only one the invariant permits: S7 still holds, since nothing the base judges reads silent. Where it cannot be certain, it stops rather than reading silent. | (1) Each shape in #669, and the `else`/`elif`/`{ …; }`/`( … )`/`!` neighbours, is judged, **seen red** at `ade83e4e`. (2) S7 green before and after. (3) `bin/test` over the gate, reader and guard modules. (4) One mutant per changed branch, killed. | 8c552f50 |

What a phase finds that the next one needs goes in
`phases/phase-N.md`, from `templates/sdd-phase.md`, when it closes. This plan
does not try to predict it.

## Operational impact

- **No migration, no new environment variable, no new dependency.**
- **A behaviour change a person will notice.** In a session whose person
  pressed `automation`, the commit gate no longer shows a permission prompt.
  A stop comes back to the model as a refusal, and the run goes on or hands
  back at its end.
- **Unchanged for everyone else.** An attended session, or a `per axis` run
  with its *run end to end* box ticked, still meets one refusal and then a
  prompt per stop. The second is a stated consequence (`spec.md` §*Scope*,
  Out), not an oversight.
- **For the pull request body.** It carries the failure direction and the
  prompt budget from `spec.md` §*What a change to a gate must carry*. It also
  says that #662's and #665's first acceptance boxes were replaced, not built
  (`CONTRIBUTING.md` §*What a change to a gate must carry*).
