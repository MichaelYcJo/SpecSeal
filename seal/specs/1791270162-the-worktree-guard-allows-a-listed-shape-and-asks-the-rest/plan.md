# Implementation Plan: the worktree guard allows a listed shape and asks the rest

<!-- seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. Framed by `specseal:framer` on Fable 5.1. -->

Approved 2026-10-06 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval. The
routing answer is the owner's `automation` press of 2026-10-06 (`routing.md`),
so the shape the last two frames used is `Approved <date> by the repository
owner, whose `automation` answer covers this item, when `smith` was spawned.` -->

## Summary

Turn the worktree guard's switch arm around. Today it predicts from a
command's text whether the command switches a branch, through four readings
grown on a frozen one, and asks about what it predicts. After this work it
recognises three shapes from the frozen reading's own words — a listed git
command, a `git switch`, and everything else — and, only in a tree where a
switch would matter, stops on everything else: a `deny` to the model where
the person pressed `automation`, an `ask` otherwise. The readings that did
not converge (candidate C, the option table, the name lookups and guesses)
leave the tree with the cases that pinned them, and every released ledger
row that cited one gets a `Corrected ·` row. The first phase measures the
cost over the recorded runs before anything is built, and `spec.md` In 7
says which half of that measurement belongs to #841.

## Technical context

- `hooks/worktree-guard.py` (3,152 lines). `main` at 2687–3145: the walk over
  `walk_command` (280–309) keeps the first switch and the first creation,
  classifies each segment with `classify` (1216–1308, `base_only` first,
  then the #790 lookups), and falls to `quiet()` (2827–2835), which asks
  candidate C's question through `wider_only_kinds` (586–639) and
  `ask_what_only_the_wider_reading_finds` (658–700). The ladder is 2867–3144
  and does not change. `judgeable` (970–1009) and `segment_cwd` name the
  tree a segment acts on and do not change. `tracked_changes` (2015) and
  `sessions_in_tree` (1874) are the tree-state readers the new
  `tree_matters` composes; today they run only after a switch is found,
  and after this work only after an unrecognised shape or a switch is found,
  so a listed shape costs no spawn where today a `checkout` costs
  `git rev-parse` through `is_ref`.
- The option reading to remove: `_REDIRECTION` (322), `_redirection_width`
  (328), `handed_words` (349), `_Options` (396), `SWITCH_OPTIONS` (410),
  `_long_option` (482), `read_switch_words` (501), `switch_kind` (545). The
  lookups to remove: `_verified` (1026), `_commit_named` (1044),
  `_OBJECT_NAME`/`_object_named` (1069–1072), `_one_merge_base` (1095),
  `is_ref` (1117), `tracked_in_any_remote` (1134), `_refs` (1157),
  `_fetched_as` (1176), `_the_bases_lookup` (1311), `_no_guess` (1317).
- The press reader: `hooks/worktree_consent.py#automation_answered`
  (274–378), wrapped exactly as `hooks/commit-review-gate.py#automation_pressed`
  (862–886) wraps it: no session, no reader, any exception → False. The
  record reader `granted`/`consent` is NOT the press (`spec.md` In 3, S7).
- The shell-string readers to reuse from `hooks/cmdline.py`:
  `command_strings` (1981), `reparsed_texts` (1701), `substitution_bodies`
  (2214), `drop_heredoc_bodies` (330). Where the module fails to load, the
  text test of `spec.md` In 1 stands in (W3).
- The construction model: `hooks/tokens.py#PLAIN_GIT` (170) and the counted
  comment above `PLAIN_PROGRAMS` (156–166).
- The corpus method: `v0.18.0:seal/specs/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd/phases/phase-3.md`
  and `v0.18.2:seal/specs/1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection/phases/phase-1.md`
  (read with `git show`): every `*.jsonl` under the repository's project
  directories, every Bash `tool_use`, distinct (command, cwd) pairs, the two
  cuts, a deleted `test_tmp_*` probe that loads the hooks under test and the
  base's hooks from `git archive`, and a self-check that the probe fires on
  the shapes it is meant to before a zero is trusted.
- Tests that cite the guard: 13 files (`grep -l "worktree-guard.py" tests/`,
  executed). The ones this work rewrites or retires cases in:
  `tests/test_guard_resolves_the_tree_it_judges.py` (90 cases, 2,633 lines;
  the generators at 1515–1635, the 165 s case at 1734, the tables at
  2006–2069, the 24.9 s case at 2140), `tests/test_worktree_guard.py` (52
  cases; the ladder, which gains S1–S9), `tests/test_the_guard_asks_once_per_session.py`
  (75 cases; `write_transcript` and `ask_entries` are the press fixtures;
  `test_the_guard_is_never_silent_where_the_writer_records` at 622 stays).
  `tests/test_the_frozen_reading_never_grows.py` must stay green untouched.
- Released rows to correct: `grep -c "worktree-guard.py#<sym>@"` over
  `seal/ledger.md` and `seal/releases/*.md`, executed 2026-10-06 — the
  counts are in `spec.md` In 6. D1 of `seal/releases/0.18.2.md`
  §1791119071 also cites `test_no_twin_is_asked_unless_an_operator_cuts_the_segment`.
- **The failure scenario of the chosen approach, in six months.** A git
  subcommand nobody here runs — `git stash` in a repository that never
  recorded one, `git submodule update` — meets the stop in a plugin user's
  dirty tree. Under the press it costs the model one deny and a retry that
  cannot be rewritten (the command IS the plain spelling), so the model has
  to put it to the person after all; without the press it is one `ask` per
  such command until a release adds the row. That is the cost `questions.md`
  P1 puts to the owner, and the Operational impact section names it. The
  mitigation inside this design is that the stop's text names the list, so
  the row to add is one grep away.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| A. Keep the prediction and add the fifth reading (#732's string reading, #734's clone) | The class #826 names: each reading meets spellings, orderings and DWIM guesses the last one missed, and the guard grew from 2,616 to 3,152 lines across four of them without converging | rejected — the ticket's own argument, and the owner reopened P4 for it |
| B. The allow-list consulted in every tree state, so an unrecognised shape asks even in a clean single-stream tree | `git checkout README.md` in a clean tree with nobody else there asks a person about a tree nothing can harm; on Windows and in a session without the press that is a prompt on most restores. A deny that fires on every invocation in some environment is an outage (§*Unknowns resolve conservatively*) | rejected — `CLAUDE.md`'s first goal: it catches no defect B's row 5 silence misses |
| C. The allow-list only where the tree matters, the stop always an `ask` | An `automation` run stops at the first `git checkout <branch>` in a dirty tree although the model could have rewritten it as `git switch` and met today's rows. #678's question already has this shape and already stops runs | rejected — `docs/commit-review-gate-spec.md` §*Why a deny, and why only once* settled the press's shape for the commit gate; the same reader is on disk |
| **D. The allow-list only where the tree matters; an unrecognised shape is a `deny` to the model under the press and an `ask` otherwise; `git switch` keeps the ladder** | A subcommand missing from the list stops an honest command until a release lists it (the six-months scenario above). A hidden creation in a clean single-stream tree is silent, as at 0.16.0 | **chosen** — zero new person-stops under the press by construction, the readings go, and the two costs are named limits with a row each |
| E. Treat `git checkout <name>` as a switch for the ladder rather than as unrecognised | `git checkout README.md` in a dirty tree asks the person *the changes will follow you* — a false ask the rewrite to `git checkout -- README.md` or `git restore` would have avoided, and the person, not the model, pays it | rejected — D's deny lets the model disambiguate for free; the ladder keeps `git switch` alone |
| F. Seed the list from `git --list-cmds=main,others` on git 2.54.0 minus the branch-movers (P1 (b)) | A mover left out of the subtraction (`stash branch`, `symbolic-ref`, a later git's new verb) reads silent, and nobody measured the list; this is the deny-list the ticket argues against, one level down | not decided here — `questions.md` P1, the owner's; (a) is the default and the ticket's text |
| G. Keep candidate C beside the allow-list for the clean single-stream state, so a hidden switch still asks there | Keeps the reader whose findings did not converge (#737, #745, two rounds of ordering) to protect a state in which there is nothing to protect | rejected — row 5 says nothing of a plain switch there; a hidden one deserves no more |
| H. Delete the 165 s case outright and leave D1 of 0.18.2 as it stands | A released row would cite a case that does not exist, and `evidence-check` reads BROKEN at the next release | refused — `docs/the-evidence-ledger.md`: a `Corrected ·` row, and #841 sequenced first (`spec.md` In 7) |

## Phases

Vertical slices — each phase ends with something runnable and verified.
**On the 45-minute question, plainly: phase 1 fits in about 45 minutes of a
smith's wall time and is the piece the owner asked for first; phases 2–4
together do not.** The guard is 3,152 lines, one test module alone holds 90
cases of which about a third leave, the policy document is 814 lines with
`Enforced by:` lines a checker reads, and about 35 released ledger citations
each owe a `Corrected ·` row. The estimate for 2–4 is three to five hours of
smith wall time, spawned as separate phases; the routing says this session
hands off after the framer and smith segments, so phase 1 is what this
session's smith can close, and `handoff.md` names phases 2–4 as next.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **Measure before building; nothing in the tree but the record.** A deleted `test_tmp_*` probe over every `~/.claude/projects/*SpecSeal*/**/*.jsonl` on the maintainer's machine, each directory named with its transcript count; both cuts of `spec.md` In 7; per cut: pairs, pairs holding a git segment the frozen reading yields, a frequency table of git subcommands (the input to `LEAVES_THE_TREE`, M1), the tree-blind stop count by shape class of In 1 (M2), the pairs stopped that today's guard does not stop and the pairs today's guard stops that the build does not (M2), and every stopped shape with no plain rewrite (M3). The probe self-checks on S3's shapes before any zero is trusted. The `--durations` figures are READ from #841's body, not run (M4). `phases/phase-1.md` from `templates/sdd-phase.md`; `questions.md` M1–M3 answered; P1's default recorded as taken under the press if unanswered | the record's tables with the paths rewritten to `/Users/x/`; the probe, its result files and every scratch directory gone (§7); the self-check line in the record | 1d28e9a9 |
| 2 | **The shape and the stop.** `LEAVES_THE_TREE` with phase 1's counts; `shape_of`; `tree_matters` composing `sessions_in_tree` and `tracked_changes` once (W2); `stop_unrecognised` with the one reason text in both languages (W1) and the press read wrapped as the commit gate wraps it; the shell-string and body reading of In 1 through `hooks/cmdline.py` with the fail-closed text test where it does not load (W3); `main`'s walk keeps the first switch, the first creation and the first unrecognised shape with its tree, and takes the stop before the ladder where the tree matters; candidate C's call sites in `quiet()` replaced. Cases S1, S3–S9 planted red at `a9d7b0e5` first (`agent-contract` §15), then green. `classify` and the readings are still defined but unreached by `main` | `uv run pytest tests/test_worktree_guard.py tests/test_the_guard_asks_once_per_session.py tests/test_a_creation_is_judged_before_git_runs.py -q`, read exit code directly (§1); the red run of each new case recorded in `phases/phase-2.md` | |
| 3 | **The removal and the retirement.** After rebasing over #841's sampled case (W4): delete every symbol in `spec.md` In 4; retire the cases of In 6 whose subject is gone, the sampled 165 s case included, and the `KINDS`/`WIDER_ONLY`/`MOVES`/`GUESSED`/`REFUSED` tables with their fixtures; `test_guard_resolves_the_tree_it_judges.py` keeps the walk, tree, token and `judgeable` cases; S10 and S11 planted; `seal/ledger/1791270162-….md` gains a `Corrected ·` row per released row citing a removed symbol, D1 of 0.18.2 §1791119071 among them, in one write at the phase's close; `--durations` of the rewritten module recorded after (M4) | `uv run pytest tests/test_guard_resolves_the_tree_it_judges.py tests/test_the_frozen_reading_never_grows.py -q --durations=10`; `uvx ruff check hooks/worktree-guard.py` for the dead imports; `evidence-check` on the fragment | |
| 4 | **The policy, the fragments and the closures.** `docs/worktree-guard-spec.md` as `spec.md` In 6 says: §A names the shapes and the stop's two readers and failure direction, §*Which tree* keeps the frozen-reading paragraphs and loses the two rules read past the base and candidate C, §*Known limits* loses four bullets and gains three; S12's policy pins rewritten; `changelog.md` naming #732 and #734 as closed and carrying phase 1's numbers; the ledger rows for S1–S14; `overview.md` with the divergences, the `Not verified` table (Windows, read not executed, answerer the repository owner) and what was fed back; the prompt budget paragraph for the pull request body | `uv run pytest tests/test_a_folded_statement_names_what_enforces_it.py tests/test_docs_line_wrap.py tests/test_the_guard_policy*.py -q` (the policy pins' module, whatever its name after phase 3); `evidence-check` and `correction-check` on the fragments | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it, and it has two halves. Where feature
branches squash, these commits stop resolving at the merge — and **a rebase
during the work does the same thing earlier and far more quietly**, because the
orphaned object still answers `git cat-file` in the worktree that wrote it.
The quiet half is the one that bites: this column was wrong on its own first
use, nine SHAs deep, and only a reviewer opening them found it. **Re-read the
column after any rebase**, or it names commits that resolve in one clone and
nowhere else. That is tolerable because nothing measures from this column.
The evidence ledger had the same problem and no such tolerance. It no longer
has it at all: a ledger row names a symbol and a content hash, so there is no
commit in it for a rebase to orphan.

## Operational impact

- No migration, no new dependency, no new hook, no change to
  `hooks/hooks.json` or to any environment variable.
- **A behaviour change plugin users meet.** In a tree another session holds,
  one whose detection is unusable (every Windows session), or one with
  tracked changes, a git command the guard does not recognise now stops:
  an `ask` naming the plain spelling, or a `deny` to the model where the
  person pressed `automation`. Today only a predicted switch stops there.
  The list is measured from this repository's recorded runs (`questions.md`
  P1), so a subcommand this repository never ran is asked about in another
  repository's dirty tree until a release adds its row. The release notes
  say this in one sentence and name the list's location.
- **What stops asking.** `git checkout README.md`, `git checkout ':/text'`
  and `2>/dev/null git switch x` in a clean single-stream tree no longer
  ask; `git checkout <branch>` in a dirty tree is denied to the model and
  retried as `git switch`, which asks as before. The 165 s and 24.9 s cases
  leave the suite with their subject (#841's record carries the durations).
- `hooks/cmdline_base.py` is byte-identical before and after;
  `tests/test_the_frozen_reading_never_grows.py` is the check.
