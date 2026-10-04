# Implementation Plan: a waiver inside a here-document body is data

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-04 by the orchestrator under the owner's `automation` routing, when `smith` was spawned.

## Summary

Both consent reads of the commit gate stop reading here-document bodies.
`has_marker` is the PreToolUse reading and `tokens.given` is the carrier to
the git hook. Both read the command through one new function in
`hooks/tokens.py`. That function takes the bodies out with the two readers the
gate already has: `one_heredoc.reduce` where it matches, else
`cmdline.drop_heredoc_bodies`. Comments stay in. A token counts only where the
base read also finds it, so the change can only turn a silent pass into a
stop. The cases come first and are shown red. The policy sentences and the
code comments change in the same commit as the fix.

## Technical context

- `hooks/commit-review-gate.py#has_marker` runs `split_segments` over the raw
  command and falls back to `marker in command` when the split is not clean.
  It is called from `judge` (the `waived` set) and from `main` (the
  unreadable-target branch). Both call sites keep calling it unchanged.
- `hooks/tokens.py#given` runs `shlex` (`words`) over the raw command and
  reads nothing when the split fails. `hooks/answer-write.py#main` is its only
  caller.
- `hooks/one_heredoc.py#reduce` returns the command without its body for the
  one shape, and `None` otherwise. Clause D leaves no `<<` in the reduced
  text, so running `drop_heredoc_bodies` over it changes nothing. That means
  the composition can be written as one expression.
- `hooks/cmdline.py#drop_heredoc_bodies` keeps comments ("quotes and comments
  respected": a `<<` inside a comment opens nothing, and the comment text is
  copied through). The documented trailing-comment form therefore survives.
  This was read in `_heredoc_split`. That the documented forms survive is
  still a measurement, `questions.md` Q3.
- Comments that say the consent read sees the whole command:
  `commit_invocations` (the paragraph beginning "A JUDGMENT read"), `main`
  (the paragraph beginning "Where the command is the one heredoc shape",
  whose last sentence names #773 as open), and `has_marker`'s docstring
  ("Cleanliness is measured HERE, on the command as written"). That last one
  stays true for the base half of the AND and needs a sentence for the other
  half.

**What breaks in six months.** A new consent read gets added, for example a
fifth token, and it tokenises the raw command, bodies included. Nothing ties
it to the shared function. The one defence is that the function lives in
`hooks/tokens.py`, whose module docstring is titled as the consent reads'
rules and which a new token's author opens first. Its rules list gains the
line "a here-document body reads nothing". The worktree guard's `has_token` is
that case today (Q1).

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A — take out only the one shape's body (`one_heredoc.reduce`), and read every other command as written | Every body outside the one shape stays a token source: a sink with an unquoted delimiter, a double-quoted delimiter, any other interpreter. The defect stays open for exactly the spellings the docs do not teach, and those are the ones a session writes by accident. A consent read's safe direction is reading less (#769 round 1's 🟡 1: "More text can only find more waiver tokens") | rejected |
| **B — `reduce` where it matches, else `drop_heredoc_bodies`, ANDed with the base read, one function shared by both consent reads** | `spec.md` cases 4 and 5. A waiver typed inside a shell-fed body, or after text the splitter wrongly takes for a body, is refused. Each costs one stop, and the stop says how to go on: the token in front of the Bash call's own command. The repository's fixed direction is to trade a silent pass for a stop, as `_heredoc_split`'s comments argue for the judgment read. The silent pass here is a commit into an undeclared repository that nobody reviews | **chosen** |
| C — B, but keep a body whose consumer is a shell (`cmdline.SHELLS`) | `_heredoc_split` does not track which command owns which redirect, as its docstring says. Keeping shell-fed bodies needs a reader that pairs each body with its consumer, and that is a new tokenizer over the boundaries #760 spent four review passes on. What it saves is case 4's stop, which already has a way on | rejected |
| D — make `has_marker` call `tokens.given`, so one consent read serves both | The two disagree on a command that does not split cleanly (substring fallback against reading nothing). Merging them changes which waivers are honoured on unclean commands that have no body at all. That is a decision of its own, outside #773 | rejected for this item |
| E — find the bodies with `heredoc_bodies` and delete their text from the raw command by string replacement | A body's text can also appear outside the body, so the replacement deletes the wrong run | rejected |
| F — B without the AND | Removing a body can turn a split that failed into one that succeeds. A token the base never read, for example one on the opener line inside a quote that the body closed, would then be honoured. That is a new silent pass, the one direction this work must not add | rejected |

## Phases

Vertical slices — each phase ends with something runnable and verified.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | The behaviour, its words and its pins in one commit. First, cases S1, S2, S3, S5 and S6 in `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py`, and S4's rows in `tests/test_the_old_spellings_reach_the_hook.py`, shown red against the base hooks (S3 green there, as it must be). Then the shared function in `hooks/tokens.py`, `has_marker` and `given` reading it ANDed with their base reads, the four comments, the two policy sentences, and the `Enforced by:` lines naming the new cases | The new cases red at `94d7b2e0`'s hooks and green after. The narrow set: the two host modules, `tests/test_the_waiver_can_be_typed.py`, and every module that holds both a heredoc and a waiver token. A grep at `94d7b2e0` found eight such modules: `tests/test_guard_resolves_the_tree_it_judges.py`, `tests/test_chain_hooks_hardening.py`, `tests/test_edits_go_through_the_edit_tool.py`, `tests/test_no_shape_the_base_stops_reads_silent.py`, `tests/test_worktree_guard.py`, `tests/test_an_automation_run_meets_no_commit_prompt.py`, `tests/test_gate_judges_the_repo_it_commits_to.py` and `tests/test_the_commit_gate_decides_at_the_commit.py`. The `Enforced by:` checker is also run | 9f3bb358 |
| 2 | The records. The work item's ledger rows in `seal/ledger/1791119070-a-waiver-inside-a-here-document-body-is-data.md`. The re-reads of every released row whose anchor phase 1 moved, written by `evidence-check --reverify --into` that fragment after each row has been read. The changelog fragment `changelog.md` in this directory. The closing memo `overview.md` | `evidence-check` exits 0. `tests/test_no_real_identifiers.py` and `tests/test_one_word_one_meaning.py` pass | d75638c7 |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

What a phase discovers while it is being built, and needs the next phase to
know, goes to `seal/specs/1791119070-a-waiver-inside-a-here-document-body-is-data/phases/phase-N.md`,
from `templates/sdd-phase.md`, when the phase closes.

**How red is shown (§15).** Check out `hooks/tokens.py` and
`hooks/commit-review-gate.py` at `94d7b2e0` over the phase-1 tree, run the new
cases, and restore the files. Copying the two files from `git show` output
works just as well. A `git stash` is not allowed in this run. The handover
says which cases failed and how.

**A note for whoever writes the cases.** Earlier reviewers on this gate were
stopped by a safety classifier while they built bypass strings at the shell.
Build each case's command inside the test module from named parts (the
opener, the body, the suffix) and run it through `run_hook`, never as a
Bash-tool command line. The records name each shape by the parts it is built
from.

## Operational impact

- No migration, no environment variable, no dependency, no config row.
- **A behaviour change a person can meet**: `spec.md` case 4. A waiver typed
  inside a body that a shell runs no longer waives. The changelog fragment
  says so and names the way on.
- **Released rows phase 2 has to re-read**, from a read at `94d7b2e0`.
  Editing the comment in `main` moves the `hooks/commit-review-gate.py#main`
  anchor, cited at `@553b6500` by seven re-read rows in
  `seal/releases/0.18.1.md`. Editing the comment in `commit_invocations` moves
  `hooks/commit-review-gate.py#commit_invocations`, cited at `@1cf73673` by
  `seal/ledger.md`, five rows of `seal/releases/0.16.0.md` and one of
  `seal/releases/0.18.1.md`. Changing `given` moves the
  `hooks/tokens.py#given` anchor, cited at `@e436fefe` by G6 in
  `seal/releases/0.17.0.md`.
  The two policy paragraphs may move the anchors of their own headings. `judge`
  is not edited, so its rows stay. `evidence-check` names the complete set, and
  the list above is what reading found, not that set.
- **Sibling items.** D edits `hooks/worktree-guard.py#switch_kind` and
  `classify`, which phase 2 found at `hooks/worktree-guard.py#classify` and not
  in `hooks/cmdline_base.py`, where this line first put it
  (`phases/phase-2.md`). This item edits neither file and calls only
  the live `hooks/cmdline.py`, so no tokenizer is shared between the two
  edits. If Q1 is answered "join this item", `has_token` sits in D's file and
  the two branches meet there. E rewrites the `--reverify` writer that phase 2
  uses. Its #772 needs a repository without a ledger freeze, and this
  repository has one. #774 is about pact changes. Neither should touch these
  re-reads. Even so, phase 2 reads each row it writes after the tool has
  written it.
