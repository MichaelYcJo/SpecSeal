# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — round 1 report

| Field | Value |
|---|---|
| Round | 1 (complete; replaces the partial report posted on #680) |
| Target SHA | `befe53cd` |
| Base compared against | `86256492` |
| Ran by | specseal:warden on claude-opus-5-5 |

Every row below was re-derived in a `git clone --no-local` at `befe53cd`,
with a second clone at `86256492`. The partial report on #680 was read as a
claim. Each of its six findings holds, and each was re-run here with a new
probe. Its fix for red 2 does not hold as written, and three of its four
yellow fixes needed changes before they passed the pinned controls.

## What this round found, in the order one causes the next

**The invariant does not hold at `befe53cd`.** The spec's invariant is that
no command `86256492` stops reads silent at the head. Two causes break it.

- **Red 1.** W1's refusal replaces the directory the base judged with an
  unresolved one. It should add the unresolved directory beside it. An
  unresolved target is waived whole by `[no-review]`, and a session that is not
  opted in reads it as silence. The same replacement reaches the worktree guard
  and the consent writer, which map an unresolved directory to the session's
  own.
- **Red 2.** The header readings recurse once per header. At about 1,000
  nested headers a `RecursionError` passes `_hides_a_commit`'s catch and
  reaches `main`. `main` then drops every commit it had found.

Four more members of #674's class read as no commit at both SHAs, while bash
3.2.57 or zsh 5.9 commits (yellows 3 to 6). They are not regressions. The
owner's standing rule makes them this item's to fix.

The fixes below were applied together in a scratch clone and run. The
results:

- the 50 new cases are red at `befe53cd` and green with the fixes;
- the W1 corpus loses 0 of 8,640 commands, where the head loses 4,125;
- 27,935 recorded commands read the same as at the head, apart from 3 probe
  commands of this round;
- the 15 reader modules pass (1,149).

## Findings from execution

### 🔴 1 — W1 replaces the directory the base judged, so 4,125 corpus commands the base stops read silent

- **Where.** `hooks/cmdline.py#walk_directories`, the `if not known:` block
  and the `failed` and `env` branches under it, together with the new first
  line of `hooks/cmdline.py#understood`.
- **What.** `spec.md` decision 1 says `understood` "is ANDed with its base
  answer, because False is its stopping direction". False is the stopping
  direction only in an opted-in session with no waiver. Elsewhere the walk
  turns it into `Unresolved(CONSTRUCT)` in place of the base's directory, and
  two paths in `hooks/commit-review-gate.py#main` read that as silence:
  - `if unreadable and optin.opted_in(cwd) and not has_marker(command,
    "[no-review]")` waives every unresolved target under `[no-review]`, so
    the parity arm the base judged in the session's directory is never
    reached;
  - from a session that is not opted in, an unresolved target is silence. A
    later relative `cd`, or a name bound before the refused segment
    (`git -C "$SB"`), stays unresolved behind it, where the base resolved it.
- **Executed through `main()` at both SHAs**, fixtures built by the probe:
  - In a declared repository with `seal/parity.md` and a staged `a.py`,
    `: '[no-review]'; <prefix> git commit -m x` went from deny to silent for
    16 of 18 prefixes. Among them: `2>/dev/null cd sub &&`, `>/dev/null pushd
    sub &&`, `>/dev/null source /dev/null;`, `2>/dev/null eval true;`,
    `2>/dev/null $CMD;`, `<<<x cd sub &&`, `<f cd sub &&`, `time 2>/dev/null
    cd sub &&`, `2>/dev/null popd;` and `2>/dev/null builtin cd sub &&`.
  - From a plain directory that is not opted in and holds an opted-in `u2`,
    9 of 9 went from deny to silent. One is `>/dev/null source /dev/null; cd
    u2 && git commit -m x`. Another is `2>/dev/null cd .; cd u2 && …`.
  - Through a bound name, 10 of 10 went silent. One is `SB=<u2>; 2>/dev/null
    source /dev/null; git -C "$SB" commit -m x`. The rest are the same with
    `[no-review]` in the parity session.
  - **The corpus.** 12 redirection spellings × 12 words × 5 placements × 3
    separators give 2,160 segments. Each was run in four session kinds, 8,640
    commands at each SHA:

    | Session kind | Base stops | Head stops | Lost at head | Lost with the fix |
    |---|---|---|---|---|
    | `[no-review]` over a parity arm | 1,815 | 330 | 1,485 | 0 |
    | not opted in, then `cd u2` | 1,815 | 330 | 1,485 | 0 |
    | not opted in, then `git -C "$SB"` | 1,980 | 825 | 1,155 | 0 |
    | opted-in undeclared, the control | 2,160 | 2,160 | 0 | 0 |

- **The guard and the consent writer.** The same replacement reaches both,
  and the spec's §*What the worktree guard sees* says it cannot ("That is the
  directory the base's walk already gave, so neither moves"). Executed from a
  clean session `S` holding a dirty nested repository `w`:
  - `hooks/worktree-guard.py` answers `ask` at `86256492` and silence at
    `befe53cd`, for four shapes such as `2>/dev/null cd .; cd w && git switch
    -c nb`. The switch lands in the dirty tree without the question the base
    asked.
  - `hooks/worktree_consent.py#creation_directory` returns `S/w` at
    `86256492` and `S` at `befe53cd` for `2>/dev/null cd .; cd w && git
    worktree add ../wt`. The consent record lands in the session's clone
    instead of the one the creation ran in.
- **Real shells.** bash 3.2.57 committed in the session's repository for
  `: '[no-review]'; 2>/dev/null cd sub && git commit`. It committed in `u2`
  for the `source` and the `cd .` shapes.
- **The fix, checked by a mutant.** The walk keeps the base's answer beside the
  refusal: `moved`, the parked failures and the three `env` branches all read
  the as-written answer. A mutant that leaves the `env` branches on `known`
  turns the 10 bound-name cases silent again, so all three parts are needed.
  #674's second acceptance box is this invariant.

### 🔴 2 — the header readings recurse with no bound, and 1,200 nested headers drop the commits already found

- **Where.** `hooks/cmdline.py#_is_the_program` and
  `hooks/cmdline.py#_segment_names_an_unknown_command`, which each call
  themselves on `tokens[h:]` once per header.
- **What.** `NESTING_READ` bounds `_hides_a_commit` alone.
  `_segment_invocations` asks `_string_hides_a_commit` at the top level,
  outside that catch. So the error reaches `main`'s `except RecursionError`,
  which sets `invocations = []`. The fallback then judges only the session's
  own directory.
- **Executed through `main()`** from a declared session with an undeclared
  `U`. Five shapes were run at 400, 1,200 and 3,000 levels, for example `cd
  U && git commit -m x; sh -c '<"f() { " ×N> true'` and `git -C U commit -m
  x; <"case a in a) " ×N> watch -g x`. All deny at `86256492` at every
  depth. At `befe53cd` all deny at 400 and all are silent at 1,200 and 3,000.
  `commit_invocations` raises `RecursionError` at 1,200.
- **Real shell.** bash 3.2.57 committed in `U` for both `sh -c` shapes with
  1,200 nested, properly closed headers.
- **The partial's fix does not hold as written.** Its loops without a bound
  are correct but quadratic. `commit_invocations` then took 46.8 s on 10,000
  `case` headers and 31.5 s on 10,000 `f() {`, where `86256492` took 4.5 s and
  0.9 s. The same class the depth bound was built against comes back. The fix
  below bounds the loop at 32, the number `NESTING_READ` uses, and answers in
  the stopping direction past it. With it: 0.16 s at 1,200 and 5.0 s at
  10,000.

### 🟡 3 — a `cd` behind a redirection the splitter cut is not read by the walk

- **Where.** `hooks/cmdline.py#walk_directories`, which never reads
  `merged_view`.
- **What.** `2>&1 cd U && git commit -m x` arrives as `2>`, then `&`, then `1
  cd U`. The walk sees a background job and a program named `1`, and does not
  move.
- **Executed.** From a declared session with an undeclared `U`, 8 of 9 shapes
  are silent at both SHAs: `2>&1 cd U &&`, `>&2 cd U &&`, `>|f cd U &&`, `<&0
  cd U &&`, `>&- cd U &&`, `2>&1 pushd U &&`, `2>&1 cd U;`, and `>&2 source
  /dev/null; git commit`. `&>/dev/null cd U` already denies at head.
- **Real shells.** bash committed in `U` for all six forms it was given. zsh
  committed for `2>&1` and `>|f`.

### 🟡 4 — a redirection glued to the end of a word hides the program, the subcommand or a `cd`

- **Where.** `_REDIRECTION` matches only at the start of a word, and so does
  every reader built on it.
- **Executed.** These 13 are silent at both SHAs from an undeclared session:
  `git>/dev/null commit`, `git commit>/dev/null`, `eval>/dev/null "$X"`,
  `sh>/dev/null -c "$CMD"`, `nice>/dev/null git commit`,
  `command>/dev/null …`, `env>/dev/null …`, `watch>/dev/null -g "$CMD"`,
  `(git>/dev/null commit)`, `git 2>/dev/null commit>/dev/null`,
  `sudo>/dev/null …`, `git<&0 commit` and `git>&2 commit`. The last two are
  also cut at `&`. From a declared session, `cd>/dev/null U && git commit` and
  `pushd>/dev/null U && …` are silent at both SHAs.
- **Real shells.** bash committed for all 12 shapes it was given, in `U` for
  the `cd` and `pushd` ones. zsh committed for `git>/dev/null commit`, `git
  commit>/dev/null` and `cd>/dev/null U`.
- **The partial's sketch needed two changes.** Its `unglued` also cut a
  quoted string holding a space. That turned the pinned control `sh -c 'case
  a in a) {fd}>f echo hi;; esac'` into a stop. And `merged_view` did not glue
  an operator that ends a word, so `git>&2 commit` was still missed. The fix
  below reads the cut tokens as a view beside the segment, like
  `merged_view`. It adds only a kind the segment did not find, and it cuts no
  word that holds whitespace.

### 🟡 5 — zsh's `noglob`, `nocorrect`, `repeat N` and the short `for` loop hide the program or a `cd`

- **Executed.** From an undeclared session, these 7 are silent at both SHAs:
  `noglob git commit`, `nocorrect git commit`, `repeat 1 git commit`, `for i
  (1) git commit`, `repeat 1 { git commit }`, `for i (1) { git commit }` and
  `repeat 2 eval "$X"`. From a declared session, `noglob cd U && git commit`,
  `nocorrect cd U &&`, `repeat 1 cd U &&` and `noglob cd U;` are silent.
- **Real shell.** zsh 5.9 committed for all seven commit shapes. The Bash
  tool's shell on this machine is zsh.
- **Two shapes are out.** `if true { … }` is a parse error in zsh 5.9, and
  `- git commit` cannot be run through `zsh -c`. Neither is claimed.
- **The partial's sketch needed a change.** Adding `for` to `UNPLACED` turned
  the pinned control `for d in git commit; do :; done` into a stop. The fix
  below reads only the parenthesised short form.

### 🟡 6 — a shell's string is not found past `--` or an option behind a redirection

- **Where.** `hooks/cmdline.py#command_strings`, the shells' branch, together
  with `_string_at`, which stops at the first word that is not a redirection.
- **Executed.** Silent at both SHAs: `bash -c 2>/dev/null -- "$CMD"`, `bash -c
  2>&1 -- "$CMD"`, `bash -c 2>/dev/null -e "$CMD"`, `sh -c 2>/dev/null +x
  "$CMD"` and `bash -c 2>/dev/null -O extglob "$CMD"`.
- **Real shells.** bash 3.2.57 committed for all five, and zsh did for the
  first. `su -c 2>/dev/null -- …` and `env -S 2>/dev/null -- …` are not
  members: `-c` and `-S` take the next word as their value, so `--` is the
  string there.

## Paperwork

### ⬜ 7 — `evidence-check` exits 2 at the head on two names the tree does not carry

The lenient `bin/evidence-check .` refuses two names at `befe53cd`, and CI's
`test.yml` runs the same command:

- `questions.md:43` names `mcp_tool` in the Q1 answer (NAME NOT IN TREE), added by `befe53cd`;
- `phases/phase-6.md:167` names the helper phase 6 removed (NAME NOT IN TREE), added by `d6fe34c0`.

Phase 6 records a lenient exit 0 at `5c721568`, before either line existed.
The correction is the marker the checker names, on each line.

### ⬜ 8 — five records state W1 as a replacement, or say that nothing was lost

Each of these is false at `befe53cd` by 🔴 1:

- `spec.md` §*What the worktree guard sees*: "so neither moves";
- ledger row I2: "leaves the walk's directory unresolved";
- ledger row I10's lead clause: "nothing `86256492` stops reads silent at
  #674's head". The corpus figures after it are true for the corpus they
  name.
- the changelog fragment: "The change only adds stops";
- the policy sentence "`understood` only adds a refusal" in
  `docs/commit-review-gate-spec.md`. This one is a policy document, so its
  correction is inside 🔴 1's paste-ready fix.

The four under `seal/` are corrected once 🔴 1 lands, with I2 re-read against
the fixed walk.

### ⬜ 9 — the P4 reading's cost, measured over every recorded transcript

The recorded run covered 27,935 distinct pairs of command and directory from
all 511 transcripts of this repository. At `befe53cd`, 3 of them gain a stop
over `86256492`. Each is `find … -name '*.md' -exec cat {} +` inside a `bash
-c`, `zsh -c` or function-body string, and none commits. Through `main()` in
a declared repository, `bash -c "find . -name '*.md' | wc -l"` is silent at
`86256492` and denies at `befe53cd`.

This is `spec.md`'s class (b), and ledger row I5 accepts it by name, glob
included. The policy's "Over 6,033 commands recorded in the milestone's runs,
none changed its verdict" is true for the three sessions it names. It is
recorded here so the budget has its wider figure, and it needs no fix.

## Round-level checks the partial did not cover

- **Tests seen red.** Target's two changed test modules were run against
  `86256492`'s `hooks/`:
  - 201 of the 315 new cases fail there;
  - the 114 that pass are controls and pins on a base answer. Their names are
    *meets no new stop*, *is silent*, *the base's own stop*, *not found twice*
    and *whose target is named git*. The phase records say mutants saw those
    red, which this round read and did not re-run.
  - All 50 cases this round plants fail at `befe53cd`, and the 525 existing
    ones pass beside them.
- **The depth bound.** Through `main()` from an undeclared session, a commit
  beside 4,000 `$(`, 6,000 `$(` and 4,000 `<(` denies in 26.5 s, 47.8 s and
  24.2 s at `86256492`. At `befe53cd` it takes 3.5 s, 6.0 s and 3.2 s, and
  the same with the fixes. An earlier run under a load average of 50 to 80
  took four to eight times as long at both SHAs, and is not used.
- **The guard's spec.** Its three examples were run through
  `cmdline.adds_a_worktree`, and they read as the sentence says at
  `befe53cd`. The first two are creations, and `git 2>&1 worktree add` is
  not. The switch half is 🔴 1.
- **The implementer notice.** `hooks/implementer-notice.py#commits` gains P5
  through `parse_git` and not P6. Its docstring says it chases less on
  purpose, because a miss costs a reminder. That is consistent, and nothing is
  owed there.
- **The ledger and changelog fragments** were read against the code, with the
  corrections above. `evidence-check` reports 0 drifted and 2 refused (⬜ 7).
  `tests/test_no_real_identifiers.py` passes.

## Regression tests to plant

Every one of them was seen red at `befe53cd` and green with the fixes, as
50 failed and 525 passed against 575 passed:

- `tests/test_no_shape_the_base_stops_reads_silent.py`:
  - 🔴 1: eight W1 prefixes under `[no-review]` over a parity arm;
  - 🔴 1: four shapes from a session that is not opted in, a bound name among
    them;
  - 🔴 2: three header kinds at 1,200 levels, each beside a commit in `u`.
- `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`:
  - 🟡 5: three rows in its wrapper table, `noglob`, `nocorrect` and
    `repeat`, which the every-wrapper pin requires;
  - 🟡 4 to 🟡 6: 18 shapes read as no commit at both SHAs;
  - 🟡 3 to 🟡 5: 11 `cd` shapes the walk did not see, through `main()`.

The code for each group is in the fenced blocks under the matching finding
below.

## Facts for the evidence ledger

- **I2, rewritten.** A refusal reached past a redirection, zsh's precommand
  words, a glued operator or a cut one adds `Unresolved(CONSTRUCT)` beside
  the directory the walk read without it. The name environment keeps its
  as-written answer. Its anchors are `walk_directories`, `understood`,
  `_unreadable_past_leading_redirections` and `_past_leading_redirections`,
  and the W1 tests above.
- **A new row for the header bound.** `_is_the_program` and
  `_segment_names_an_unknown_command` read 32 headers and then answer in the
  stopping direction. The anchors are the constant and the two readers
  (NAME NOT IN TREE until the fix lands).
- **I10's lead clause.** It is corrected to the corpus it measured, and this
  round's 8,640-command W1 corpus is added beside it.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | W1's refusal replaces the directory the base judged instead of adding one beside it, so a `[no-review]` over a parity arm, a session that is not opted in, the worktree guard's dirty-tree question and the consent record each lose what the base had | `hooks/cmdline.py#walk_directories`, `hooks/cmdline.py#understood` | open | Executed through `main()`: 4,125 of 8,640 corpus commands the base stops are silent at head, and 0 with the fix. The guard is silent where the base asked on 4 switches, and the consent directory moves from `S/w` to `S`. bash commits. The `env` half was shown needed by a mutant |
| 🔴 2 | The header readings recurse once per header, so 1,200 nested headers raise past `_hides_a_commit` into `main`, which drops the commits found | `hooks/cmdline.py#_is_the_program`, `hooks/cmdline.py#_segment_names_an_unknown_command` | open | Executed through `main()`: five shapes deny at base and are silent at head at 1,200 and 3,000 levels. The partial's unbounded loop is quadratic, 46.8 s on 10,000. The bounded loop takes 5.0 s |
| 🟡 3 | A `cd` behind a redirection the splitter cut is not read by the walk | `hooks/cmdline.py#walk_directories` | open | 8 shapes silent at both SHAs from a declared session. bash and zsh commit in `U` |
| 🟡 4 | A redirection glued to the end of a word hides the program, the subcommand or a `cd` | `hooks/cmdline.py#_REDIRECTION` | open | 15 shapes silent at both SHAs. bash commits all 12 it was given, and zsh 3 |
| 🟡 5 | zsh's `noglob`, `nocorrect`, `repeat N` and `for i (…) cmd` hide the program or a `cd` | `hooks/cmdline.py#RUNNERS` | open | 11 shapes silent at both SHAs. zsh 5.9 commits all seven commit shapes |
| 🟡 6 | A shell's string is not found past `--` or an option behind a redirection after `-c` | `hooks/cmdline.py#command_strings` | open | 5 shapes silent at both SHAs. bash commits all five |
| ⬜ 7 | `evidence-check` exits 2 at head on two refused names in this item's records | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/questions.md:43` | open | Executed at `befe53cd`: 2 refused, lenient exit 2. The second is `phases/phase-6.md:167`. A correction to the run's paperwork, and it turns CI's `test.yml` red |
| ⬜ 8 | Five records state W1 as a replacement or say nothing was lost | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/spec.md` | open | False at head by 🔴 1. Also ledger rows I2 and I10 and the changelog fragment. The policy sentence is corrected inside 🔴 1's fix |
| ⬜ 9 | The P4 reading adds a stop on `find` with a quoted glob or `{}` inside a shell string: 3 of 27,935 recorded commands | `hooks/cmdline.py#_behind_a_runner` | open | Executed over all 511 transcripts. It is `spec.md` class (b), accepted by ledger row I5. Recorded for the budget, and no fix is asked |
| 🟢 | #674's shapes are asked at head, and the new cases were seen red | `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py` | confirmed | 201 of 315 new cases fail against `86256492`'s hooks. The other 114 are controls and base-answer pins |
| 🟢 | The depth bound answers in seconds where the base took up to 48 s | `hooks/commit-review-gate.py#NESTING_READ` | confirmed | Through `main()`: 3.2–6.0 s at head against 24.2–47.8 s at base, all deny |
| 🟢 | The guard spec's three worktree examples read as written | `docs/worktree-guard-spec.md` | confirmed | Executed through `cmdline.adds_a_worktree` at both SHAs |
| ❓ | The mutants the phase records name for the 114 controls and pins | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/phases/phase-6.md` | ❓ out of verified scope | Read and not re-run. The smith's records answer for them |
| ❓ | The cases on Windows | `tests/test_no_shape_the_base_stops_reads_silent.py` | ❓ out of verified scope | CI's `windows-latest` leg at the pull request answers it |

## Executed probes

| What was run | Result |
|---|---|
| Target's two changed test modules at `befe53cd` | 525 passed |
| The same modules against `86256492`'s `hooks/` | 201 of the 315 new cases failed, and the 114 that passed are controls and base-answer pins |
| The targeted cases through `main()` at base, head and the fix: red 1 in three session kinds, red 2 at three depths, the yellows, and 7 controls | 🔴 1: 35 base stops silent at head, all restored. 🔴 2: 10 lost at 1,200 and 3,000, all restored. Yellows: 44 of 50 silent at both SHAs are stops with the fix. Controls unchanged |
| The W1 corpus through `main()`: 8,640 commands at base, head, the red fixes alone, and all fixes | Lost at head: 4,125. Lost with either fix set: 0. Added by all fixes over base: 0. Raised: 0 |
| Real bash 3.2.57 and zsh 5.9, one fresh pair of repositories per shape, 44 shapes | Every shape claimed in 🔴 1 to 🟡 6 committed. `if true { }` and `- git commit` in zsh, and `env -S` on macOS, did not, and are not claimed |
| Header nesting through `commit_invocations`, 400 to 10,000 levels, at base, head, the unbounded loop and the bounded fix | Head raises `RecursionError` from 1,200. The unbounded loop takes 46.8 s at 10,000. The bounded loop takes 5.0 s, against 4.5 s at base |
| The worktree guard and `creation_directory` on W1 shapes, at base, head and both fix clones | Head is silent on 4 switches the base asked about, and files 2 creations under `S` instead of `S/w`. Both fix clones match base |
| A mutant of the fix with the three `env` branches back on `known` | The 10 bound-name cases turn silent |
| 27,935 recorded commands from 511 transcripts through `commit_invocations` at base, head, the red fixes and all fixes | Head differs from base on 3, and the red fixes match head. All fixes add 3 more, each this round's own probe patch with a zsh loop in a heredoc body, the class the base already stops. 0 raised |
| 15 reader modules, which load the reader, both gates, the consent writer or the notice | Head: 1,099 passed. Red fixes: 1,099 passed. All fixes with the planted cases: 1,149 passed |
| The planted cases against `befe53cd`'s hooks | 50 failed and 525 passed |
| `tests/test_docs_line_wrap.py`, `tests/test_one_word_one_meaning.py` and `tests/test_no_real_identifiers.py`, with the policy edit | 58 passed |
| `ruff check` and `ruff format --check` on the four files the fix touches | Clean |
| `bin/evidence-check .` at head | 0 drifted and 2 refused, exit 2 (⬜ 7) |
| `bin/evidence-check .` with the fixes | 18 anchors drifted in the rows of I1 to I7 and the older fragments, all in units the fix edits. The fix's re-read owes them |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It belongs to the sealer, once the rounds settle, and it is not due while this round leaves findings open |

## Paste-ready fixes

Each block applies to `befe53cd` and was run as one set. Together the blocks
give the numbers above. 🔴 1 and 🔴 2 hold on their own as well, and were run
that way.

### 🔴 1 — add W1's refusal beside the base's directory

```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ def understood(tokens):
-def understood(tokens):
+def understood(tokens, redirections=True):
@@
-    if _unreadable_past_leading_redirections(tokens):
+    if redirections and _unreadable_past_leading_redirections(tokens):
         return False
@@ def walk_directories(items, cwd):
-        known = understood(tokens)
+        known = understood(tokens)
+        # W1 (#674) refuses a segment `86256492` accepted. The refusal is ADDED
+        # beside the base's reading and never replaces it: an unresolved target
+        # is waived whole by `[no-review]` and is silence from a session that
+        # is not opted in, so replacing a directory the base judged lost stops.
+        as_written = known or understood(tokens, redirections=False)
         if not known:
-            moved = [
+            refused = [
                 (Unresolved(str(here), Unresolved.CONSTRUCT), prev)
                 for here, prev in moved
             ]
+            moved = _dedup(moved + refused) if as_written else refused
@@
         if any(sep in ("||", ";") for sep, _ in items[index + 1 :]):
+            refused = [
+                (Unresolved(str(h), Unresolved.CONSTRUCT), p) for h, p in running
+            ]
             failed = (
-                running
-                if known
-                else [(Unresolved(str(h), Unresolved.CONSTRUCT), p) for h, p in running]
+                running if known else list(running) + refused if as_written else refused
             )
@@
-        elif joined in ("&&", "||") and known:
+        elif joined in ("&&", "||") and as_written:
@@
-        elif known and joined not in SUBSHELL and following not in SUBSHELL:
+        elif as_written and joined not in SUBSHELL and following not in SUBSHELL:
@@
-        elif known:
+        elif as_written:
             # A pipeline stage or a background job -- what is left once the
--- a/docs/commit-review-gate-spec.md
+++ b/docs/commit-review-gate-spec.md
@@ So each place a program word stands is read past what the shell takes off it:
   judged where the shell is, as the same commit without it is. A `cd`, a
-  relocator, a reserved word or an expanding word reached past one leaves the
-  directory unresolved, the answer a `cd` behind a prefix already had.
+  relocator, a reserved word or an expanding word reached past one adds an
+  unresolved directory beside the one the walk read without it, and never
+  replaces it: `[no-review]` waives an unresolved target whole, and a session
+  that is not opted in reads one as silence, so a replaced directory is a
+  stop lost. The same holds for zsh's `noglob`, `nocorrect` and `repeat N`,
+  for a redirection glued to a word's end (`cd>/dev/null W`), and for one the
+  splitter cut (`2>&1 cd W`).
@@
 The reading can only have gained stops by this. Every reader asks what it
-asked before first and adds what the new reading finds, `understood` only
-adds a refusal, and a generated corpus of 11,393 commands across these
-positions found none silent where the release base stopped. The one answer
+asked before first and adds what the new reading finds, `understood`'s
+refusal is added beside the directory the walk read before, and a generated
+corpus of 11,393 commands across these positions found none silent where the
+release base stopped. The one answer
```

```python
# tests/test_no_shape_the_base_stops_reads_silent.py, appended
W1_PREFIXES = [
    "2>/dev/null cd sub &&",
    ">/dev/null pushd sub &&",
    ">/dev/null source /dev/null;",
    "2>/dev/null eval true;",
    "2>/dev/null $CMD;",
    "<<<x cd sub &&",
    "X=1 2>/dev/null cd sub &&",
    "time 2>/dev/null cd sub &&",
]


@pytest.mark.parametrize("prefix", W1_PREFIXES)
def test_w1_keeps_the_directory_the_base_judged_under_a_waiver(
    monkeypatch, capsys, projects, tmp_path, prefix
):
    """Round 1 of 1790660768, red 1. W1's refusal REPLACED the directory the
    base judged with an unresolved one, and `[no-review]` waives an
    unresolved target whole -- so the parity arm the base judged in the
    session's directory went silent, while bash commits there."""
    session = make_repo(tmp_path / "session", declared=True)
    (session / "sub").mkdir(exist_ok=True)
    (session / "seal" / "parity.md").write_text("# parity\n")
    (session / "a.py").write_text("x = 1\n")
    subprocess.run(["git", "-C", str(session), "add", "a.py"], check=True)
    command = f": '[no-review]'; {prefix} {BODY}"
    for which, got in with_and_without_the_press(
        monkeypatch, capsys, projects, command, session
    ).items():
        assert "silent" not in got, (command, which, got)


@pytest.mark.parametrize(
    "shape",
    [
        ">/dev/null source /dev/null; cd u2 && {body}",
        "2>/dev/null eval true; cd u2 && {body}",
        "2>/dev/null cd .; cd u2 && {body}",
        'SB={u2}; 2>/dev/null source /dev/null; git -C "$SB" commit -m x',
    ],
)
def test_w1_keeps_the_directory_the_base_judged_outside_an_opted_in_session(
    monkeypatch, capsys, tmp_path, shape
):
    """Round 1 of 1790660768, red 1. From a directory that is not opted in, an
    unresolved target is silence, and a later relative `cd`, or a name bound
    before the refused segment, stays unresolved behind it. The base resolved
    `u2`, which is opted in, and bash commits there."""
    plain = tmp_path / "plain"
    plain.mkdir()
    u2 = make_repo(plain / "u2")
    command = shape.format(body=BODY, u2=q(u2))
    got = decisions(monkeypatch, capsys, command, plain, "s")
    assert "silent" not in got, (command, got)
```

### 🔴 2 — bound the header readings as a loop

```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ # What `header_end` answers for a header whose spelling it does not place.
 UNPLACEABLE = -1
 
+# How many compound headers, one inside the next, `_is_the_program` and
+# `names_an_unknown_command` read before the segment counts as one whose
+# program they cannot place -- the stopping direction, as `UNPLACEABLE` is
+# (round 1 of 1790660768, red 2). Unbounded, each header was one level of
+# recursion, and a thousand of them raised `RecursionError` past
+# `_hides_a_commit`'s catch into `main`, which dropped every commit found. A
+# loop without a bound rescans the rest of the segment per header: 47 s on
+# 10,000. The commit gate's `NESTING_READ` is the same number for bodies.
+HEADERS_READ = 32
+
@@ def _is_the_program(tokens, k):
-    for t in tokens[:k]:
-        if os.path.basename(t) in RUNNERS:
+    for _level in range(HEADERS_READ):
+        for t in tokens[:k]:
+            if os.path.basename(t) in RUNNERS:
+                return True
+            if not (
+                ("=" in t and not t.startswith("-"))
+                or t in LIST_OPENERS
+                or t in ("!", "(")
+            ):
+                break
+        else:
             return True
-        if not (
-            ("=" in t and not t.startswith("-")) or t in LIST_OPENERS or t in ("!", "(")
-        ):
-            break
-    else:
-        return True
-    if _is_the_program_past_redirections(tokens, k):
-        return True
-    h = header_end(tokens)
-    if h == UNPLACEABLE:
-        return True
-    if h is not None and 0 < h <= k:
-        return _is_the_program(tokens[h:], k - h)
-    return False
+        if _is_the_program_past_redirections(tokens, k):
+            return True
+        h = header_end(tokens)
+        if h == UNPLACEABLE:
+            return True
+        if h is None or not 0 < h <= k:
+            return False
+        tokens, k = tokens[h:], k - h
+    return True
@@ def _segment_names_an_unknown_command(toks, nested=False):
-    if not nested and _expands(command_word(toks)[0]):
-        return True
-    if _expands(command_word(toks, redirections=True)[0]):
-        return True
-    if any(_expands([t]) for t in _without_redirections(_behind_a_runner(toks))):
-        return True
-    h = header_end(toks)
-    if h == UNPLACEABLE:
-        return any(_expands([t]) for t in _without_redirections(toks[1:]))
-    return (
-        bool(h)
-        and h < len(toks)
-        and _segment_names_an_unknown_command(toks[h:], nested=True)
-    )
+    for _level in range(HEADERS_READ):
+        if not nested and _expands(command_word(toks)[0]):
+            return True
+        if _expands(command_word(toks, redirections=True)[0]):
+            return True
+        if any(_expands([t]) for t in _without_redirections(_behind_a_runner(toks))):
+            return True
+        h = header_end(toks)
+        if h == UNPLACEABLE:
+            return any(_expands([t]) for t in _without_redirections(toks[1:]))
+        if not h or h >= len(toks):
+            return False
+        toks, nested = toks[h:], True
+    return True
--- a/docs/commit-review-gate-spec.md
+++ b/docs/commit-review-gate-spec.md
@@
   from the program, a later word that expands counts. None of these three counts
-  a redirection's target.
+  a redirection's target. Past 32 headers, one inside the next
+  (`HEADERS_READ`), the program counts as one the reader does not place.
```

```python
# tests/test_no_shape_the_base_stops_reads_silent.py, appended
@pytest.mark.parametrize("header", ["case a in a) ", "f() { ", "coproc "])
def test_a_deep_header_nesting_keeps_the_commits_found(
    monkeypatch, capsys, projects, tmp_path, header
):
    """Round 1 of 1790660768, red 2. The header readings recursed once per
    header, so 1,200 of them raised `RecursionError` past `_hides_a_commit`
    into `main`, which dropped the commit already found in `u`."""
    session = make_repo(tmp_path / "session", declared=True)
    u = make_repo(tmp_path / "u")
    for command in (
        f"cd {q(u)} && {BODY}; sh -c '" + header * 1200 + "true'",
        f"git -C {q(u)} commit -m x; " + header * 1200 + "watch -g x",
    ):
        for which, got in with_and_without_the_press(
            monkeypatch, capsys, projects, command, session
        ).items():
            assert "silent" not in got, (command[:60], which, got)
```

### 🟡 3 — the walk asks a cut redirection's group beside its part

```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ def walk_directories(items, cwd):
     states, parked, walked, env = [(cwd, None)], [], [], {}
     stack, defined = [], set()
+    # A `cd` behind a redirection the splitter cut (`2>&1 cd W`) arrives as a
+    # part whose first word is the descriptor (yellow 3); its group, glued back,
+    # is asked beside it.
+    glued = {parts[-1]: toks for parts, toks in merged_view(items)}
@@
-        known = understood(tokens)
+        known = understood(tokens) and (index not in glued or understood(glued[index]))
```

### 🟡 4 — read a redirection glued to a word's end as a view beside the segment

```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ def redirection_width(tokens, i):
     return j - i
 
 
+def unglued(tokens):
+    """TOKENS with a redirection glued to the END of a word cut into its own
+    word, or None where no word carries one (round 1 of 1790660768, yellow 4).
+
+    `_REDIRECTION` matches at the start of a word, and a shell ends a word at
+    `<` and `>` wherever they stand: `git>/dev/null commit` runs `git commit`,
+    and `commit>/dev/null` is the subcommand `commit`. A descriptor in front
+    (`2>f`) and bash 4.1's `{fd}>f` are the operator's own and stay whole. It
+    is read as a view BESIDE the segment, the way `merged_view` is, so every
+    answer the segment gave stands and the view only adds.
+    """
+    out, cut = [], False
+    for t in tokens:
+        k = min((t.find(c) for c in "<>" if c in t), default=-1)
+        if (
+            k > 0
+            and not t[:k].isdigit()
+            and not (t[0] == "{" and t[k - 1] == "}")
+            # A word holding a space was quoted, and is an argument's.
+            and not any(c.isspace() for c in t)
+        ):
+            out += [t[:k], t[k:]]
+            cut = True
+        else:
+            out.append(t)
+    return out if cut else None
+
+
@@ def merged_view(items):
             parts, toks = groups[-1]
-            m = _REDIRECTION.match(toks[-1])
-            if m and m.end() == len(toks[-1]):
+            # The operator may be glued to the end of a word (`git>&2`,
+            # yellow 4), so the last piece `unglued` cuts is the one asked.
+            last = (unglued(toks[-1:]) or toks[-1:])[-1]
+            m = _REDIRECTION.match(last)
+            if m and m.end() == len(last):
@@ def names_an_unknown_command(text):
     # The segments the splitter cut inside a redirection are asked again,
-    # glued back (#674, `merged_view`): `2>&1 $CMD` runs `$CMD`.
+    # glued back (#674, `merged_view`): `2>&1 $CMD` runs `$CMD`. A redirection
+    # glued to a word's end is cut off and asked again too (`unglued`).
+    views = [*segments, *merged_segments(text)]
     return any(
         _segment_names_an_unknown_command(toks)
-        for toks in [*segments, *merged_segments(text)]
+        for toks in [*views, *filter(None, map(unglued, views))]
     )
@@ def _unreadable_past_leading_redirections(tokens):
-    rest, passed = _past_leading_redirections(tokens)
-    if not passed:
+    cut = unglued(tokens)
+    rest, passed = _past_leading_redirections(cut or tokens)
+    if not passed and cut is None:
         return False
--- a/hooks/commit-review-gate.py
+++ b/hooks/commit-review-gate.py
@@ from cmdline import (
     substitution_bodies,
+    unglued,
     walk_directories,
 )
@@ def _reads_a_commit(text):
-    for toks in [*segments, *merged_segments(stripped)]:
+    views = [*segments, *merged_segments(stripped)]
+    for toks in [*views, *filter(None, map(unglued, views))]:
@@ def commit_invocations(command, cwd=None):
     for parts, toks in merged_view(items):
         seen = set().union(*(kinds[p] for p in parts))
-        for kind, invs in _segment_invocations(toks, walked[parts[-1]][1]).items():
-            if kind not in seen:
-                found += invs
+        for view in filter(None, (toks, unglued(toks))):
+            for kind, invs in _segment_invocations(view, walked[parts[-1]][1]).items():
+                if kind not in seen:
+                    found += invs
+                    seen.add(kind)
+
+    # A redirection glued to a word's end (`git>/dev/null commit`, round 1 of
+    # 1790660768, yellow 4) is cut off and the segment read again beside
+    # itself, adding only a kind the segment did not find.
+    for (toks, bases), seen in zip(walked, kinds, strict=True):
+        cut = unglued(toks)
+        if cut is not None:
+            for kind, invs in _segment_invocations(cut, bases).items():
+                if kind not in seen:
+                    found += invs
```

### 🟡 5 — zsh's precommand words and short loop

```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ RUNNERS = frozenset(
         "script",
+        # zsh (round 1 of 1790660768, yellow 5): precommand modifiers, and
+        # `repeat N`, whose count is an operand the stand-in reads past.
+        "noglob",
+        "nocorrect",
+        "repeat",
     }
 )
@@ def command_word(tokens, stand_in="git", redirections=False):
     if i < len(toks) and (
         toks[i] in UNPLACED
+        # zsh's short loop, `for i (1 2) git commit` (yellow 5): the word list
+        # in parentheses, and the command straight after it. `for d in git
+        # commit` has no parenthesis there and stays a word list.
+        or (
+            toks[i] in ("for", "foreach")
+            and i + 2 < len(toks)
+            and toks[i + 2].startswith("(")
+        )
         or toks[i].endswith(")")
@@ def _past_leading_redirections(tokens):
         tok = toks[i]
+        # zsh's precommand modifiers and `repeat N` run the command in this
+        # shell, and the base read them as the command word (yellow 5).
+        if tok in ("noglob", "nocorrect") or (tok == "repeat" and i + 1 < len(toks)):
+            passed, i = True, i + (2 if tok == "repeat" else 1)
+            continue
         if (
```

```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py,
# three rows in WRAPPED after "nice" -- the every-wrapper pin requires them
    "noglob": (f"noglob {C}", HERE),
    "nocorrect": (f"nocorrect {C}", HERE),
    "repeat": (f"repeat 1 {C}", UNRESOLVED),
```

### 🟡 6 — a shell's string past `--` and the options behind a redirection

```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ def command_strings(tokens):
             flag = next(j for j, t in enumerate(rest) if _hands_a_string(word, t))
-            tail, skip = rest[flag + 1 :], False
-            for at, t in enumerate(tail):
+            # A redirection is asked and read past, and the scan goes on past
+            # the options and `--` behind it (yellow 6): `bash -c 2>/dev/null
+            # -- "$CMD"` runs `$CMD`.
+            tail, skip, at = rest[flag + 1 :], False, 0
+            while at < len(tail):
+                t, width = tail[at], redirection_width(tail, at)
                 if skip:
                     skip = False
+                elif width:
+                    out.append(t)
+                    at += width
+                    continue
                 elif t in VALUED:
                     skip = True
                 elif t != "--" and not t.startswith(("-", "+")):
-                    out += _string_at(tail, at)
+                    out.append(t)
                     break
+                at += 1
```

### 🟡 3 to 🟡 6 — the cases, appended to the wrapper module

```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py, appended
# Round 1 of 1790660768, yellows 3-6: shapes a real shell commits that read as
# no commit at both `86256492` and `befe53cd`. Each was run in bash 3.2.57 or
# zsh 5.9 and made a commit.
STILL_UNREAD = {
    # yellow 4: a redirection glued to the END of a word.
    "git>/dev/null": "git>/dev/null commit -m x",
    "commit>/dev/null": "git commit>/dev/null -m x",
    "git>&2, cut at &": "git>&2 commit -m x",
    "git<&0, cut at &": "git<&0 commit -m x",
    "(git>/dev/null": "(git>/dev/null commit -m x)",
    "nice>/dev/null": "nice>/dev/null git commit -m x",
    "env>/dev/null": "env>/dev/null git commit -m x",
    "eval>/dev/null": 'eval>/dev/null "$X"',
    "sh>/dev/null -c": 'sh>/dev/null -c "$CMD"',
    # yellow 5: zsh.
    "for i (1)": "for i (1) git commit -m x",
    "for i (1) { }": "for i (1) { git commit -m x }",
    "repeat 1 { }": "repeat 1 { git commit -m x }",
    "repeat 2 eval": 'repeat 2 eval "$X"',
    # yellow 6: the string past `--` and options behind a redirection.
    "bash -c 2>/dev/null --": 'bash -c 2>/dev/null -- "$CMD"',
    "bash -c 2>&1 --": 'bash -c 2>&1 -- "$CMD"',
    "bash -c 2>/dev/null -e": 'bash -c 2>/dev/null -e "$CMD"',
    "sh -c 2>/dev/null +x": 'sh -c 2>/dev/null +x "$CMD"',
    "bash -c 2>/dev/null -O extglob": 'bash -c 2>/dev/null -O extglob "$CMD"',
}


@pytest.mark.parametrize("name", sorted(STILL_UNREAD))
def test_a_shape_both_shas_read_as_no_commit_is_read(name, tmp_path):
    """Seen red at `befe53cd`, where each returned nothing."""
    assert found(STILL_UNREAD[name], tmp_path), name


# yellows 3-5 in the walk: a `cd` the shell runs that the walk read as
# staying put. From a declared session, the commit lands in U, which declares
# nothing, and each read silent at both SHAs.
UNSEEN_CD = [
    "2>&1 cd {u} && git commit -m x",
    ">&2 cd {u} && git commit -m x",
    ">|f cd {u} && git commit -m x",
    "<&0 cd {u} && git commit -m x",
    ">&- cd {u} && git commit -m x",
    "2>&1 pushd {u} && git commit -m x",
    "cd>/dev/null {u} && git commit -m x",
    "pushd>/dev/null {u} && git commit -m x",
    "noglob cd {u} && git commit -m x",
    "nocorrect cd {u} && git commit -m x",
    "repeat 1 cd {u} && git commit -m x",
]


@pytest.mark.parametrize("shape", UNSEEN_CD)
def test_a_cd_the_walk_did_not_see_stops(monkeypatch, capsys, shape, tmp_path):
    """Seen red at `befe53cd`, where each was silent."""
    session = make_repo(tmp_path / "session", declared=True)
    u = make_repo(tmp_path / "u")
    command = shape.format(u=u)
    assert say(monkeypatch, capsys, command, session) != "silent", command
```

## What the partial report claimed, checked

| The partial claimed | Found here |
|---|---|
| 🔴 1: 14 commands go from ask to silent | Holds, and is wider: 35 targeted shapes, 4,125 of 8,640 corpus commands, and the guard and the consent writer too |
| 🔴 1's fix holds | Holds, and its `env` half is needed. A mutant without it turns 10 cases silent |
| 🔴 2: 3 commands lost at 1,200 levels | Holds for 5 shapes at 1,200 and 3,000 |
| 🔴 2's fix, unbounded loops | Correct but quadratic: 46.8 s on 10,000 headers. It is replaced by the bounded loop |
| 🟡 3 to 🟡 6 are silent at both SHAs, and a real shell commits | Holds for every shape the partial named. `su -c … --` and `env -S … --` are not members |
| 🟡 4 and 🟡 5 sketches, not run | Each needed a change before it passed the pinned controls, as written under each finding |
| Acceptance 3: 0 verdict changes over 6,240 recorded pairs | Over 27,935 pairs, the head changes 3 (⬜ 9) |

## Coverage

This round covered:

- every finding of the partial report, each re-executed here;
- the new tests against the base (seen red);
- the depth bound's timing through `main()`;
- the worktree guard and the consent writer;
- the implementer notice (read);
- the policy text in both specs;
- the ledger fragment, the re-read rows and the changelog fragment;
- the invariant, over three corpora: the planted invariant module, this
  round's 8,640-command W1 corpus, and 27,935 recorded commands.

What it did not cover:

- **The smith's 11,393-command corpus.** It was a deleted probe and was not
  rebuilt. This round's corpora test the three session kinds that corpus did
  not model.
- **The mutants for the controls and pins.** They were read and not re-run.
- **Windows.** CI's `windows-latest` leg answers it.

Needs a fix: yes — 🔴 1 (W1 replaces the directory the base judged, in the commit gate, the guard and the consent writer), 🔴 2 (the header readings recurse with no bound and drop the commits found), 🟡 3 (a `cd` behind a cut redirection), 🟡 4 (a redirection glued to a word's end), 🟡 5 (zsh's precommand words and short loop), 🟡 6 (a shell's string past `--` or an option behind a redirection)
Loses a record or crashes: yes — 🔴 1: at `befe53cd` the consent writer files a worktree creation made in a nested clone under the session's own clone, so the creation's own clone gets no record and the session's clone gets one nobody gave. 🔴 2 raises `RecursionError` out of the reader; `main` catches it and drops the commits found

The broad gate is not due yet: this round leaves six findings open.

## Proof block

Files opened this round, in the clone at `befe53cd` unless named otherwise:

- the diff `86256492..befe53cd` of `hooks/cmdline.py` and
  `hooks/commit-review-gate.py`, whole;
- `hooks/cmdline.py`:
  - `walk_directories`, whole;
  - `command_word`, `command_strings`, `strip_subshell`, `_cd_target` and
    `understood`'s head;
  - the `RELOCATORS`, `PREFIXES`, `LIST_OPENERS`, `UNPLACED` and `RUNNERS`
    blocks;
- `hooks/commit-review-gate.py`: `main`, `_reads_a_commit`,
  `_string_hides_a_commit` and `commit_invocations`;
- `hooks/worktree-guard.py`: the module docstring, `walk_command`, the
  directory mapping before `segment_cwd`, `segment_cwd` and `classify`;
- `hooks/worktree_consent.py#creation_directory`;
- `hooks/implementer-notice.py#commits`;
- `hooks/optin.py`: `opted_in` and `parity_config`;
- `bin/test`;
- `tests/conftest.py`: `load_hook_module`, `run_hook`, `declare_routing` and
  the transcript fixture;
- `tests/test_no_shape_the_base_stops_reads_silent.py`, whole;
- `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`:
  its helpers, `WRAPPED`, the wrapper pin and `CONTROLS`;
- this work item's `spec.md`, `overview.md`, `phases/phase-6.md` and
  `changelog.md`, whole;
- this work item's ledger fragment, whole;
- `questions.md:43`;
- `docs/commit-review-gate-spec.md`, lines 317–396;
- the `docs/worktree-guard-spec.md` diff;
- `.github/workflows/test.yml:101`;
- the partial report on #680;
- the round-2 report of `1790655302`, for its shape.
