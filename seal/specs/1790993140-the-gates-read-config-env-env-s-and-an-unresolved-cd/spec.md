# Feature Specification: the gates read `--config-env`, `env -S`, and an unresolved `cd`

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Three issues, one reader family. #716 is two commits the commit gate's text
reading does not find. #678's guard half and #686 are two places where the
worktree guard's frozen reading is silent while bash acts somewhere it did
not look. The guard half of both is decided by a count, under the owner's
rule of 2026-10-03, and this frame writes both outcomes so the count settles
what is built without anybody being asked again.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against* | A design that stops to ask costs more than one that does not, and the difference is argued. Here it is argued by a count over the recorded runs, not by opinion |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | The pull request states a test seen red, the failure direction, the prompt budget and platform honesty. Phase 3's counts are the prompt budget for the guard half |
| `docs/commit-review-gate-spec.md` §*The commit gate inside git*, the stand-aside paragraph, and `hooks/tokens.py#is_plain` | Where this plugin's git hooks run, the PreToolUse reading stands aside only for a command whose shape is known plain (#692, `questions.md` P7). Neither #716 shape is plain, so the text reading is what judges them |
| `docs/commit-review-gate-spec.md`, the #670 paragraph (`env -S` among the strings read as a command) | The `env -S` sentence there is the one #716 makes incomplete. The file is listed under `Over the ceiling` in `seal/config.md` until #715, so any change there replaces words in place: no new fold marker and no net growth in lines |
| `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it* | The guard judges the first segment of each kind and the first directory in it that classifies, read through `hooks/cmdline_base.py`. Two kinds of destination fall back to the session's own directory. This is the sentence #686 changes or names as a limit |
| `docs/worktree-guard-spec.md` §*Creation consent*, the command-word groups paragraph | A git behind a redirection (`git 2>&1 worktree add`) is not git to the guard. This is the sentence #678's guard half changes or names as a limit |
| `docs/worktree-guard-spec.md` §*Unknowns resolve conservatively* | A wrong deny costs a prompt and a wrong allow can break another session's tree, but a deny on every invocation is an outage. The ask designed here only replaces a silence |
| `seal/specs/1790815613-…/questions.md` P4 and P6 | The owner kept the switch and creation arms on the frozen `86256492` reader, byte-pinned, with no rule added to it. `tests/test_the_frozen_reading_never_grows.py` is the pin. Nothing here edits `hooks/cmdline_base.py` |
| `seal/specs/1790745049-…/spec.md` S5–S7 (#689) | A segment only the wider reading reads as git must never take the guard's first slot, and the wider reading never chooses the guard's tree. Every addition here keeps both |
| `seal/specs/1790660768-…/questions.md` Q2 and `phases/phase-6.md` | The method of the count: every Bash command in the recorded transcripts, main and subagent, as distinct (command, directory) pairs, read by the readers in a deleted probe, and the verdicts that change are counted |

## Scope

**In.**

1. **#716, the commit gate's reader.** `git --config-env <name>=<var> commit`
   with a space after the option, and `env -S '<env's own words> git commit'`,
   are found as commits by `hooks/cmdline.py`. The class is enumerated, not
   only the coordinate: every git global option that takes its value as a
   separate word, and every spelling of `env`'s split string (`-S <s>`,
   `-S<s>`, `--split-string <s>`, `--split-string=<s>`, and `genv`).
2. **#716, which reading each shape reaches.** Stated in the table below and
   in the phase record. It is not a choice; it is what the code does.
3. **#686, the switch arm.** A candidate rule: where the tree a switch acts on
   cannot be resolved, the guard asks instead of going silent on the session's
   own tree. It is built in phase 2, measured in phase 3, and wired or removed
   in phase 4 by the count.
4. **#678, the guard half.** A candidate rule: a switch or a creation that only
   the commit gate's wider reading finds (`git 2>&1 worktree add`,
   `2>/dev/null git switch x`, a zsh-prefixed git, and `git --config-env k=v
   switch x` once item 1 lands) is put to the person instead of passing
   unread. It goes through the same three phases as item 3.
5. **The policy text, the pins and the records** for whichever way each count
   falls: `docs/worktree-guard-spec.md`, the in-place reword in
   `docs/commit-review-gate-spec.md`, the ledger fragment, the changelog
   fragment, and the base-answer cases each built rule changes.

**Out, each with its reason.**

- **Editing `hooks/cmdline_base.py`.** P4 and P6 pin its bytes and S11 tests
  them. Every guard-side addition lives in `hooks/worktree-guard.py`.
- **The creation arm's unresolved directory** (an unresolved `cd` before
  `git worktree add`). Without consent every Bash creation row already stops
  (ask, choice or deny, `docs/worktree-guard-spec.md` §B), so an ask there adds
  nothing. With consent the row allows, and consent is the owner's
  `automation` press, which `README.md`'s worktree-guard row promises will not
  ask. #686's own comment of 2026-09-30 measured the cost of the creation case
  as "one extra ask later, never a silent pass".
- **A string the guard is handed to a shell** (`sh -c 'git switch x'`,
  `env -S 'git switch x'`). The guard has never read strings; that is #670's
  class for the guard, a wider shape than either issue names, and it has no
  count behind it. The builder names it in `overview.md`'s *Not done*, and the
  session that spawned the build decides its filing under
  `docs/review-chain-spec.md` §*Where a leftover goes*.
- **The commit shapes of #678** (`"$CMD"`, `parallel`). #692's comment on #678
  closes them by design where the stubs are installed; a foreign-slot clone
  keeps 0.16.0's text gate, and nothing here changes it.
- **`docs/commit-review-gate-spec.md` growth.** Frozen under `Over the
  ceiling` until #715, which runs in parallel. Item 1's policy change is a
  reword of the existing `env -S` clause, nothing more.
- **`hooks/tokens.py`.** Round 3 of #692 found the stand-aside is not the gap
  for y05 (`steps_around_hooks` already returns true), and neither shape is
  plain, so the reading already judges both. Only the reader misses them.

### Which reading each #716 shape reaches

| Shape | git's hook | PreToolUse reading | Grounds |
|---|---|---|---|
| `git --config-env core.hooksPath=VAR commit -m x` | **Never.** `core.hooksPath` from VAR points git at another hooks directory, so this plugin's stub does not run, in any clone | **The only reading, in every clone.** `steps_around_hooks` matches `hookspath`, so `is_plain` is false and `git_decides` is false; the commit gate's text reading judges. Today it finds no commit, because `_git_options` takes `core.hooksPath=VAR` for the subcommand | read: `hooks/tokens.py#steps_around_hooks`, `hooks/commit-review-gate.py#main`, `hooks/cmdline.py#_git_options`; executed by round 3 of #692, y05: landed, both readings silent |
| `env -S '-i git commit -m x'` | **Not where no lease stands.** `env -i` empties the environment, so the stub sees neither session variable. Where a lease stands the stub has a session; that half is unverified and is not needed by this build | **The only reading where no lease stands, and the one that judges in every clone.** `env` is not in `PLAIN_PROGRAMS`, so `is_plain` is false. Today `reparsed_texts` returns `-i git commit` and reads it as a command whose word is `-i` | read: `hooks/tokens.py#is_plain`, `hooks/cmdline.py#reparsed_texts`; executed by round 3 of #692, y09: landed with no lease, both readings silent |
| `git --config-env k=v switch x`, `git --config-env k=v worktree add ../w b` | The guard reads text on every git (P4, P6) | **The guard's frozen reading, which does not find them** (`cmdline_base._git_options` has the same set). They reach the guard only through item 4, if it is built | read: `hooks/cmdline_base.py#_git_options` |

## User scenarios & acceptance *(mandatory)*

Every case below is seen red before it is planted (contract §15). "Red"
means against the unfixed code; for a pin of an unchanged base answer, red
means a mutant of the branch it pins.

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 `--config-env` spaced | Given a session in an opted-in, undeclared repository, when the command is `git --config-env core.hooksPath=VAR commit -m x`, then `commit_invocations` returns one invocation and the commit gate stops. In a declared one it is silent, as any commit there is | a case in `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`; red at `233f0455` |
| S2 `--config-env` in a stubbed clone | Given a clone carrying this plugin's git hook stubs, when the same command reaches `dispatch.py pre-bash`, then the reading judges it (no stand-aside) and stops in an undeclared directory | a case beside `STEPS_AROUND` in `tests/test_the_commit_gate_decides_at_the_commit.py`; red at `233f0455` |
| S3 the git option class | For every git global option phase 1 measures as taking its value as a separate word (`questions.md` M1), `git <option> <value> commit -m x` is found as a commit, and `git <option> <value> status` is not | one parametrized case over M1's list; each member red where it was missing from `takes_value` |
| S4 `env -S` | `env -S '-i git commit -m x'`, `env -S'-i git commit -m x'`, `env --split-string '-i git commit -m x'`, `env --split-string='-i git commit -m x'` and the `genv` spelling are each found as a commit | parametrized case; red at `233f0455` |
| S5 base answers kept | `env -S 'git commit -m x'`, `env -S 'FOO=1 git commit -m x'` and every existing `env -S` entry still read as before; `env -S 'echo hi'` and `env -S '-i true'` commit nothing; `git --config-env=k=v commit` (glued) is unchanged; `reparsed_texts(["env","-S","a b"])` keeps `"a b"` and gains the env reading | the existing cases, plus the pin at `TEXTS` (`"env -S"`, `"env -S glued"`) changed with a note saying why; a mutant that drops the base text is killed |
| S6 the count for #686 | Over the corpus `questions.md` D1 fixes, the number of distinct (command, directory) pairs where candidate A fires is recorded, with the corpus size and the number of pairs that hold a switch at all | `phases/phase-3.md`; the probe is deleted afterwards (contract §7) |
| S7a **#686 built** (count A = 0) | Given a clean session tree holding a dirty nested clone `w`, when the command is each of `builtin cd w`, `command cd w`, `time cd w`, `pushd w`, `noglob cd w`, `cd "$W"` with `W` unset, `2>&1 cd w`, then `&& git switch feature/x`, the guard asks, and its reason says it could not tell which tree the switch runs in and names `git -C <dir> switch …` as a spelling it reads. Every base deny and choice is kept: an ACTIVE session in the session's tree still denies (`test_a_cd_the_guard_cannot_read_leaves_it_judging_its_own_tree` stays `deny`). A resolved `cd w && git switch` and `git -C w switch` are unchanged | cases in `tests/test_guard_resolves_the_tree_it_judges.py`; each of the seven red at `233f0455` (silent); the reason text pinned in English and Korean (contract §14) |
| S7b **#686 refused** (count A ≥ 1) | `docs/worktree-guard-spec.md` §*Known limits* names the fallback with the count, the corpus and the date, and the seven shapes stay silent on a clean session tree | a case pinning silence for the seven shapes; the bullet's `Enforced by:` names it |
| S8 the count for #678 | Over the same corpus, the number of pairs where candidate C fires is recorded, with the number of pairs whose frozen reading finds a switch or creation | `phases/phase-3.md` |
| S9a **#678 built** (count C = 0) | `cd w && git 2>&1 worktree add ../wt b` and `git --config-env k=v worktree add ../wt b` are put to the person where no consent holds, and stay silent under consent; `cd w && 2>/dev/null nice -n 5 git switch feature/x`, `git --config-env k=v switch x` and the five `ZSH_PREFIXED` switch shapes ask. `WIDER_FIRST` still denies over the session active in `w` (the first slot is unchanged), and the consent writer files exactly where it filed | the base-answer cases that change (`test_a_segment_only_the_reading_past_redirections_finds_is_not_git_to_the_guard`, `test_a_zsh_prefixed_git_is_not_git_to_the_guard_or_the_consent_writer`) are changed with a note, not deleted; new cases red at `233f0455` |
| S9b **#678 refused** (count C ≥ 1) | `docs/worktree-guard-spec.md` §*Known limits* names the shape with the count; `git 2>&1 worktree add` and `git --config-env k=v switch x` are pinned silent beside the existing silence pins | a case; the bullet's `Enforced by:` names it |
| S10 the frozen reading | `hooks/cmdline_base.py` is byte-identical to `233f0455`, and only the guard and the consent writer import it | `tests/test_the_frozen_reading_never_grows.py` passes unchanged |
| S11 the frozen policy file | `docs/commit-review-gate-spec.md` carries the same fold markers and no more lines than at `233f0455` (1047) | `fold-check`; `wc -l` |
| S12 the records | The ledger fragment holds this work's claims; every existing row whose anchor this work edits is re-read and re-stamped in the file it is in with a dated note; the changelog fragment names #716, #678 and #686 | `bin/evidence-check` exit 0; the fragment checks |

## Data & interfaces

- `hooks/cmdline.py#_git_options`: `takes_value` gains `--config-env` and
  whatever else M1 measures. `parse_git` and `_expanded` read the same scan,
  so both learn it at once.
- `hooks/cmdline.py#reparsed_texts` (and `command_strings`, which delegates
  its `env` arm to it): for `env -S`, the split string is also returned as
  `env <string> <words after it>`, beside the string alone. The base reading is
  kept, so the change only adds.
- `hooks/worktree-guard.py` gains two pure functions, names the builder's,
  that phase 3's probe imports so the thing measured is the thing wired:
  - **candidate A**: given the command and the session directory, true when
    the switch-kind segment the guard would judge has an `Unresolved` among
    its directories in the frozen walk, or when `hooks/cmdline.py`'s walk
    gives that segment directories the frozen walk does not. It never returns
    a tree. Where the two splits cannot be matched, it answers true
    (`questions.md` W1);
  - **candidate C**: given the command and the session directory, the kinds
    (switch, creation) that `hooks/cmdline.py`'s reading finds — its splitter,
    `merged_view`, `parse_git` and `adds_a_worktree` — where the frozen
    reading finds none of that kind.
- The guard imports `hooks/cmdline.py` under a name that does not shadow its
  `cmdline_base as cmdline` binding. `test_only_the_two_fallback_arms_read_it`
  is about `cmdline_base` and is unaffected.
- Ledger: `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md`.
  Rows in `seal/releases/0.9.1.md`, `0.9.4.md`, `0.15.5.md`, `0.15.6.md` and
  `0.16.0.md` cite `hooks/worktree-guard.py` or the `cmdline.py` units this
  touches (read: a count of anchors by grep, not of rows checked); those that
  drift are re-read there.

## Open questions → questions.md

No row needs a person. The owner's rule of 2026-10-03 decides #686 and #678's
guard half from a count, and every judgment the tickets left open is decided
in `questions.md` with its grounds, so it can be overturned by opening what
was opened.

Framed 2026-10-03 by framer, before the build.
