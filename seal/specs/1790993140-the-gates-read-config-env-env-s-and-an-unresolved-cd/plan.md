# Implementation Plan: the gates read `--config-env`, `env -S`, and an unresolved `cd`

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-03 by the repository owner, whose `automation` answer covers this item, when `smith` was spawned.

## Summary

Phase 1 teaches the commit gate's reader the two #716 spellings and their
class. Phases 2 to 4 handle the guard: two candidate rules are built as pure
functions and left unwired, a deleted probe counts how often each would have
fired over the recorded runs, and the count decides, by the owner's rule of
2026-10-03, whether each rule is wired in or removed and named as a known
limit. Phase 5 writes the records. Both outcomes of each count are written
out below, so the builder knows what to build for either number and nobody is
asked mid-run.

## Technical context

**The commit gate's reader** (`hooks/cmdline.py`, read at `233f0455`):

- `_git_options` steps over git's global options to find the subcommand. Its
  `takes_value` set is `-C`, `-c`, `--git-dir`, `--work-tree`, `--namespace`,
  `--exec-path`. `--config-env` is missing, so `git --config-env k=v commit`
  reads `k=v` as the subcommand. `parse_git` and `_expanded` share this scan.
- `reparsed_texts`, the `env`/`genv` arm, returns `env -S`'s string as a
  command of its own. That is right for `env -S 'git commit'` and wrong for
  `env -S '-i git commit'`, because `env` splits the string into its OWN
  arguments: the command that runs is `env -i git commit`. `command_strings`
  delegates its `env` arm here.
- `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`
  pins `reparsed_texts(["env","-S","a b"]) == ["a b"]` in `TEXTS`. Adding the
  env reading changes that output, so the pin changes with a note; the base
  text stays in the list.

**The guard** (`hooks/worktree-guard.py`, read at `233f0455`):

- `main` walks the command through `walk_command`, which is
  `cmdline_base.walk_directories` over the frozen splitter. It keeps the first
  switch-kind segment and the first creation, and for each takes the first
  directory that classifies. `judgeable` turns an `Unresolved` directory into
  the session's own (`here = cwd if isinstance(where, cmdline.Unresolved)`).
- The switch ladder: ACTIVE deny, idle choice, unusable choice, the creation
  judged, the tracked-changes ask, then `sys.exit(0)` on a clean single
  stream. Before it, `if not top` exits silently when the judged directory is
  in no repository.
- Read in `hooks/cmdline_base.py#understood` and `#walk_directories`: `builtin
  cd w`, `command cd w`, `time cd w` and `pushd w` are refused by
  `understood`, so the walk carries `Unresolved(CONSTRUCT)`; `cd "$W"` with
  `W` unset is `Unresolved(VALUE)` from `_land`. `noglob cd w` is a command
  whose word is `noglob`, which `understood` accepts, so the frozen walk
  confidently says nothing moved; `2>&1 cd w` is split at `&` into a segment
  whose word is `1`, the same confident answer. `hooks/cmdline.py`'s walk
  reads both of those as moving (its `noglob` arm, and #674's redirection
  reading). These are readings, not runs; phase 2's red cases are what check
  them (`questions.md` M2).
- `tests/test_guard_resolves_the_tree_it_judges.py` holds the base's answers,
  including the four silence pins #689 wrote for shapes the wider reading
  sees and the frozen one does not.

**What breaks in six months, for the chosen approach.** The guard now loads
the commit gate's wider reader as a second opinion. If a later change to
`hooks/cmdline.py` widens what it calls a switch or a move, candidate A or C
fires on commands it did not fire on when phase 3 counted, and a run that
measured zero stops starts stopping. Nothing re-counts automatically. The
mitigation is that the reason text names the readable spelling, so the agent
can rewrite and retry, and that `tests/test_guard_resolves_the_tree_it_judges.py`
pins controls (`cd w && git switch`, `git -C w switch`, a plain `git switch`)
that must stay silent on a clean tree.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **#716 env -S: read `env <string> <rest>` beside the string as a command** | A string with no commit costs nothing; one with a commit is found either way. The only new stops are commands that hold `env -S` and a commit | **Chosen.** It adds a reading and keeps the base one, so the gate only blocks more |
| #716 env -S: replace the string reading with the env reading | Drops an answer the base gave, against the rule every #670/#674 reader kept: ask what the base asked first, then add | Rejected |
| #716 env -S: name it a known limit | A commit the reader could find at no cost to commands that commit nothing stays unjudged | Rejected |
| **#716 `--config-env`: add it to `takes_value`, with the class measured** | None found: the glued form already reads, and the spaced one is the same option | **Chosen** |
| #716 `--config-env`: stop on any command naming `--config-env` | Round 3 of #692 showed the stand-aside is not the gap for y05; a word-based stop would also stop `git --config-env k=v status` | Rejected |
| **#686 signal: the frozen walk's `Unresolved`, or the two walks disagreeing about the judged segment** | Fires on every construct either walk cannot follow before a switch: loops, `eval`, subshells. That is the honest class, and phase 3 counts it | **Chosen.** It reuses the enumeration #674 already built for `noglob` and redirections instead of writing a new one |
| #686 signal: the frozen walk's `Unresolved` alone | Misses `noglob cd w` and `2>&1 cd w`, two of the issue's seven shapes, because the frozen walk is confident about both | Rejected |
| #686 signal: scan each segment for a `cd`, `pushd` or `popd` word the walk did not move on | A new list of words, which is the enumeration every round of #692 found short | Rejected |
| #686 signal: teach the frozen walk | P4 and P6 pin its bytes, and S11 tests them | Not open |
| **#686 response: `ask`, only where the base would be silent** (the clean single-stream exit and the no-repository exit) | Every base deny and choice is kept, so nothing is allowed that was refused. Its cost is a stop wherever it fires, which is what phase 3 counts | **Chosen** |
| #686 response: judge the tree the wider walk gives | That is the ordering #689 measured and took back: the wider reading choosing the guard's tree met commands bash never ran the switch in | Rejected |
| #686 response: deny once, then ask (the `choose` pattern) | The owner's rule says the guard asks. `choose` exists for two named ways on; here there is one question, whether to proceed | Rejected |
| **#678: ask where only the wider reading finds a switch or a creation, consent first for a creation** | Fires on every recorded command that hides a switch or creation behind a redirection, a zsh prefix or a spaced `--config-env` | **Chosen.** The frozen reading keeps its slot (WIDER_FIRST stays a deny), so this only turns a silence into a question |
| #678: judge the wider reading's segment through the ladder | Needs the wider segment matched to a frozen directory, the ordering trap again, and its count would depend on tree state no transcript records | Rejected |
| **Measure the built function** (build unwired in phase 2, import it from the probe in phase 3) | None found: what is counted is what is wired | **Chosen** |
| Measure with the probe's own copy of the rule, build after | The copy and the build drift, and the count no longer describes the code | Rejected |
| Count one number across both #686 and #678 | One shape's stops would refuse the other shape, though the owner's rule is about each | Rejected; `questions.md` D2 |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#716 in the commit gate's reader.** M1 first: enumerate git's global options that take a separate value by running each on the installed git in a scratch repository named `g-716-*` under the session scratchpad, deleted after. `--config-env` and every other missing member go into `hooks/cmdline.py#_git_options`. The `env -S` arm of `reparsed_texts` adds `env <string> <rest>` beside the string. The `TEXTS` pin changes with a note. The `env -S` clause of `docs/commit-review-gate-spec.md`'s #670 paragraph is reworded in place to say the split string is also read as `env`'s own words, with no new line and no new marker | S1–S5 red at `233f0455` and green after; a mutant that drops the base `env -S` text is killed; the existing cases of the two touched test modules pass; `wc -l docs/commit-review-gate-spec.md` ≤ 1047 and `fold-check` reports the same 18 markers | bfdb9b18 |
| 2 | **The two guard candidates, built and left unwired.** Candidate A and candidate C as pure functions in `hooks/worktree-guard.py` (`spec.md` §*Data & interfaces*). The guard imports `hooks/cmdline.py` under a separate name. Unit cases: A is true for each of #686's seven shapes before `git switch feature/x`, and false for `cd w && git switch`, `git -C w switch`, a plain `git switch`, and `cd /no/such/dir ; git switch x`. C finds a creation in `cd w && git 2>&1 worktree add ../wt b` and `git --config-env k=v worktree add ../wt b`, a switch in `cd w && 2>/dev/null nice -n 5 git switch feature/x`, `git --config-env k=v switch x` and the `ZSH_PREFIXED` shapes, and nothing for `WIDER_FIRST`'s commands (the frozen reading already finds their switch) or for a plain `git switch` | every unit case seen red against a stub that returns the opposite; M2 answered in the phase record (which shapes reach A through `Unresolved` and which through the disagreement); `main` is unchanged, so `tests/test_guard_resolves_the_tree_it_judges.py` passes untouched | d367791a |
| 3 | **The count.** A probe named `test_tmp_*` reads the corpus `questions.md` D1 fixes, deduplicates (command, directory) pairs, and calls phase 2's two functions on each. It records: transcripts read (main and subagent), pairs, pairs holding a frozen switch, pairs holding a frozen creation, **count A**, **count C**, and every pair that fired, with paths rewritten to `/Users/x/` (`tests/test_no_real_identifiers.py`). Before trusting a zero it runs the same functions on #686's seven shapes and S9a's shapes inside the probe and shows each fires. Run it with `run_in_background: true`. It is deleted afterwards, with every scratch file it made | `phases/phase-3.md` holds both counts, the denominators and the fired list; the decision for each candidate is written there as the rule's output, in one line | c7f84438 |
| 4 | **The branch, one per candidate, taken mechanically from phase 3.** See *What phase 4 builds* below | the cases named there; `tests/test_the_frozen_reading_never_grows.py` passes unchanged (S10) | 723dffd2 |
| 5 | **Records.** The ledger fragment for this work's claims. Every existing row `evidence-check` names as drifted, re-read in the file it is in and re-stamped with `--checked`, corrected first where an edit made it false. The changelog fragment `seal/specs/1790993140-…/changelog.md`, naming #716, #678 and #686. `overview.md`, with the guard-strings shape in *Not done*. The lines for the pull request: the test seen red, the failure direction, the prompt budget (phase 3's counts) and platform honesty | `bin/evidence-check` exit 0; `rider_check.py`; the record and document checks this work touches; `survivor-check --range 233f0455..HEAD` | |

### What phase 4 builds

**Candidate A (#686), count A = 0 → the guard asks.**

1. In `main`, keep the frozen walk, the first slot, `judgeable` and every row
   as they are. Compute candidate A for the switch segment the loop chose.
2. Where A is true, replace exactly two silent exits with an `ask`: the
   `if not top` exit when a switch (not only a creation) was found, and the
   final `sys.exit(0)` of the clean single-stream row. Rows 1, 1-b, 2 and 3
   are untouched, so an ACTIVE deny, a choice and the tracked-changes ask
   still decide first.
3. The reason, in both languages through `tr`: the guard could not tell which
   tree this switch runs in, names the part of the command it could not
   follow where it can, says it judged the session's own tree, and names
   `git -C <dir> switch …`, or the `cd` as a plain command of its own, as a
   spelling it reads.
4. Cases: the seven shapes over a dirty nested `w` under a clean session ask
   (red at `233f0455`: silent); the reason pinned in English and Korean;
   `test_a_cd_the_guard_cannot_read_leaves_it_judging_its_own_tree` stays
   `deny`; `test_a_cd_behind_a_redirection_leaves_the_guard_on_the_tree_the_base_judged`
   changes from `silent` to `ask` for its switch commands, with a note naming
   this work item, and its consent half stays as it is; the controls stay
   silent.
5. Policy: `docs/worktree-guard-spec.md` §*Which tree*'s two fallback bullets
   say the guard still judges the session's tree first and now asks where it
   would have let a switch it could not place pass silently. The sentence
   saying the guard reads "never through `hooks/cmdline.py`" says it reads
   that module as a second opinion that never chooses the tree. The comment
   above the guard's `import cmdline_base` says the same. An `Enforced by:`
   line names the new cases.

**Candidate A (#686), count A ≥ 1 → the fallback stays.**

1. Delete candidate A and its unit cases. `main` is unchanged.
2. `docs/worktree-guard-spec.md` §*Known limits* gains one bullet: where the
   guard cannot resolve the tree a switch acts on, it judges the session's own
   tree; the seven shapes as examples; **the count, the corpus and the date**
   from `phases/phase-3.md`; and that the owner's rule of 2026-10-03 kept the
   fallback because asking would have added that many stops.
3. A case pins the seven shapes silent on a clean session tree over a dirty
   `w`, so the bullet stays true; its `Enforced by:` line names it.

**Candidate C (#678), count C = 0 → the guard asks.**

1. In `main`, after the frozen loop, compute candidate C. For each kind the
   frozen loop did NOT find:
   - a switch found by C → `ask`, with a reason saying the switch is written
     in a shape the guard reads as text it does not follow, and naming the
     plain spelling;
   - a creation found by C → read consent first, exactly as
     `guard_worktree_creation` does: under consent stay silent, as at the
     base; otherwise `ask`, with the same kind of reason.
   The frozen findings keep their slots and their verdicts.
2. The consent writer is not touched: a creation it does not see mints no
   consent, which is the safe direction.
3. Cases: S9a's shapes ask (red at `233f0455`: silent); under consent the
   creation shapes stay silent; `WIDER_FIRST` still denies;
   `test_a_segment_only_the_reading_past_redirections_finds_is_not_git_to_the_guard`
   and the switch half of `test_a_zsh_prefixed_git_is_not_git_to_the_guard_or_the_consent_writer`
   change from `silent` to `ask` with a note, and that case's consent-writer
   half stays `""`.
4. Policy: the command-word groups paragraph of §*Creation consent* and the
   cost paragraph of §*Which tree* say these shapes are now put to the person,
   consent first for a creation. An `Enforced by:` line names the cases.
   `README.md` and `README.ko.md` are re-read: their worktree-guard row
   promises a creation is not asked under `automation`, and consent-first
   keeps that true, so neither should change. If the builder finds otherwise,
   both move together.

**Candidate C (#678), count C ≥ 1 → refused.**

1. Delete candidate C and its unit cases.
2. `docs/worktree-guard-spec.md` §*Known limits* gains one bullet: a switch
   or creation only the commit gate's wider reading finds is silent to the
   guard; the shapes; **the count, the corpus and the date**; refused under
   the owner's rule of 2026-10-03.
3. Pin `cd w && git 2>&1 worktree add ../wt b` and `git --config-env k=v
   switch x` silent beside the existing silence pins, and name them in the
   bullet's `Enforced by:`.

**In every branch** the guard import of `hooks/cmdline.py` stays only if a
candidate was wired; with both refused it is removed with them.

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

- **No migration, no new environment variable, no new dependency.**
- **The guard loads `hooks/cmdline.py`** where a candidate is wired. In a
  grouped `dispatch.py pre-bash` call the commit gate has usually loaded it
  already, so `sys.modules` makes it one load. Phase 4 measures the median of
  fifteen `dispatch.py pre-bash` calls on a plain `git switch` before and
  after, the way `hooks/cmdline_base.py`'s docstring measured the import
  recursion, and records both figures.
- **Failure direction, for the pull request.** Phase 1 only adds commits found,
  so the commit gate blocks more and never less. Phase 4 only turns a silence
  into an ask, or changes nothing, so the guard blocks more and never less.
- **Prompt budget, for the pull request.** Phase 1: a stop on a command that
  holds a spaced `--config-env` or an `env -S` before a commit, which the base
  stopped nowhere. Phase 4: phase 3's counts, zero for whatever was wired.
- **Platform.** String reading only, no process inspection. `env -S` is GNU
  coreutils 8.30+ and macOS `env`; `--config-env` is git 2.31+. M1 runs on the
  installed git (2.54.0 on the framing machine, read from `git --version`);
  CI's legs run the cases on Linux and Windows.
