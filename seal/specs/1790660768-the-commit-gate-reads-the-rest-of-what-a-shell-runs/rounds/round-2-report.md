# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — round 2 report

| Field | Value |
|---|---|
| Round | 2, a verifying round over round 1's fix range `3b8522c3..cd4a65d7` |
| Target SHA | `1b444773` |
| Base compared against | `86256492`, and `3b8522c3` (round 1's target, the same hooks as `befe53cd`) |
| Ran by | specseal:warden on claude-opus-5-5 |

Every row below was re-derived in `git clone --no-local` clones at
`1b444773`, `3b8522c3` and `86256492`, with a fourth clone carrying the fixes
proposed here. Round 1's verdict cells, which hold the fix pass's account,
were read as claims and each was checked against the code and by execution.

## What this round found, in the order one causes the next

**All nine of round 1's verdicts are closed.** The invariant holds at the
head over every corpus this round rebuilt: 9,408 W1 commands in four session
kinds lose 0 of the base's stops and add 0, and 28,527 recorded commands keep
every target the base found. The depth bound answers at 10,000 headers in the
time the base takes. The worktree guard and the consent writer match
`86256492` on round 1's shapes again.

Two new members of the class were found, both silent at `86256492` as well.

- **Yellow 1 answers the orchestrator's question 4.** `2>/dev/null cd w &&
  git switch -c nb` is silent in the guard because the walk never lands a
  `cd` whose words hold a redirection. That covers a redirection after the
  operand (`cd W 2>/dev/null`), in front of the `cd`, or glued to either. The
  same cause makes the commit gate silent on `cd u2 >/dev/null && git
  commit` from a directory that is not opted in. It is silent too under
  `[no-review]` over a parity arm. bash 3.2.57 and zsh 5.9 commit in every
  one of those shapes. The consent writer files the creation under the wrong
  clone for the same reason.
- **Yellow 2 is a second replacement of the base's directory**, in the walk's
  unplaced flag, which round 1's red 1 did not reach. It breaks the
  invariant only on commands that commit nothing, such as `: '[no-review]';
  nice 2>/x/git commit -m git`. It still makes the policy's "can only have
  gained stops" and ledger row E7's "nothing the base stops reads silent"
  false as written.

One paperwork correction (white 3) and one cost note (white 4) are below.

## Findings from execution

### 🟡 1 — a `cd` with a redirection among its words is not landed, so the guard, the consent writer and two session kinds of the commit gate judge the wrong tree

- **Where.** `hooks/cmdline.py#walk_directories`, where `moved` is built from
  `_cd_target(tokens)` alone. `_cd_target` counts `2>/dev/null` in `cd W
  2>/dev/null` as a second operand and answers `unknown`. For `2>/dev/null cd
  W` it sees no `cd`, because the first word is the redirection. The walk
  then leaves the shell unresolved in the first case and where it was in the
  second.
- **The orchestrator's question, answered.**
  - *Is it a defect?* Yes. bash runs `git switch -c nb` in the dirty `w`, and
    `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it*
    says the tree judged is the one the command acts on, "the tracked-changes
    row included". The guard judged the clean session tree and said nothing.
  - *Is it in this item's class?* The redirection half is. The shell takes
    the redirection off and the reader did not, which is #674's class. The
    commit gate misses real commits for the same reason, and those misses are
    this item's by the rule round 1 applied to its yellows 3 to 6. Six other
    spellings keep the guard silent for a different reason and are not this
    item's. They are `builtin cd w`, `command cd w`, `time cd w`, `pushd w`,
    `noglob cd w` and `cd "$W"`. The guard reads an unresolved directory as
    the session's own and judges only the first directory of a segment, as
    §*Which tree* states on purpose. They are deferred below.
  - *The minimal fix.* The walk reads the `cd` again with its redirections
    taken off (`unglued`, then `_without_redirections`, on the glued group
    where the splitter cut one). The landing is added **in front of** the
    answer the walk already had, and never replaces it. The commit gate
    judges every directory, so it only gains stops. The guard and the consent
    writer take the first directory they can name, so they take the one the
    shell went to.
- **Executed through `main()` at `86256492`, `3b8522c3` and the head.**
  - From a directory that is not opted in and holds an opted-in `u2`, `cd u2
    <r> && git commit -m x` is silent at all three for 8 of the 9 spellings
    tried: `2>/dev/null`, `>/dev/null`, `2> /dev/null`, `</dev/null`, `2>&1`,
    `>/dev/null 2>&1`, `>|f` and `-P 2>/dev/null`. `cd u2 && git commit`
    asks at all three.
  - In a declared session with a parity arm, `: '[no-review]'; cd sub <r> &&
    git commit -m x` is silent at all three for 5 of the 9, while `cd sub &&
    git commit` asks.
  - With the fix, all 38 of these tail shapes stop, against 20 at the head.
- **The guard and the consent writer**, from a clean session `S` holding a
  dirty nested clone `w`, at all three SHAs:
  - `cd w 2>/dev/null && git switch -c nb`, `2>/dev/null cd w && …` and
    `cd>/dev/null w && …` are silent. With the fix each asks, and the reason
    names the dirty file.
  - `creation_directory` files `2>/dev/null cd w && git worktree add ../wt`
    under `S`. With the fix it files it under `S/w`, where the creation ran.
  - `2>&1 cd w && …` stays silent with the fix. The walk reads the
    splitter's `&` there as a background job and keeps the unmoved shell
    first, so it belongs with the deferred six.
- **Real shells.** bash 3.2.57 and zsh 5.9 committed in `U` for all 8 shapes
  given: `cd U 2>/dev/null`, `>/dev/null`, `2> /dev/null`, `</dev/null`,
  `>/dev/null 2>&1`, `cd U>/dev/null`, `cd -P U 2>/dev/null` and `pushd U
  >/dev/null`, each followed by `&& git commit`.
- **What the fix costs.**
  - The W1 corpus loses 0 of the base's or the head's stops. It adds 8, each
    `: '[no-review]'; cd sub <r> && git commit`, which bash commits in the
    session's own repository.
  - The 28,527 recorded commands read exactly as at the head.
  - A chain of 10,000 `cd>/dev/null x;` segments now takes 14.8 s where the
    head took 0.7 s. It now lands, and a chain of plain `cd x;` already took
    8.5 s at the head and at the base.
  - The guard judges `w` where the base judged `S` for those three switches.
    `S` was the fallback for a directory the walk could not read, and the
    switch never runs there.
- **Seen red.** The 9 cases below fail against the head's hooks and pass with
  the fix. A mutant that appends the landing behind the existing answer
  instead of in front turns the guard case red and leaves the other 8 green.

### 🟡 2 — the walk's second reading replaces the base's directory where only it unplaces

- **Where.** `hooks/cmdline.py#walk_directories`, `if command_word(tokens)[1]
  or command_word(tokens, redirections=True)[1]:`, which turns every
  directory of the segment into `Unresolved`. This came in before round 1
  (`86256492..befe53cd`), and round 1's red 1 fixed the `understood` half of
  the same pattern only.
- **What.** Where the first reading already found `git` (a redirection-shaped
  word whose last component is `git`, behind a runner), the base judged that
  commit in the resolved directory. The second reading, past the
  redirection, lands behind the runner and unplaces, and the replacement is
  waived whole by `[no-review]`.
- **Executed through `main()`.** In a declared session with a parity arm, `:
  '[no-review]'; nice 2>/x/git commit -m git` and `: '[no-review]'; env
  </x/git commit -m git` ask at `86256492`. They are silent at `3b8522c3` and
  at the head, and ask with the fix.
- **Why it is a yellow and not a white.** Neither command commits: bash runs
  `commit`. But three written claims are false at the head because of it.
  They are the policy sentence "Every reader asks what it asked before first
  and adds what the new reading finds", ledger row E7's lead "nothing the
  base stops reads silent", and the changelog fragment's "The change only
  adds stops". The fix makes all three true. A smith may instead answer with
  grounds and narrow the three sentences to commands that commit.
- **The fix, and the pinned case it had to respect.** Replacing only where
  the first reading found no `git` keeps `2>/dev/null nice -n 5 git commit`
  unresolved alone. `REDIRECTED_UNPLACED` pins that shape, and the first
  version of this fix turned it red, so the fix below is the second version.
  Its case is red at the head and green with it.

## Paperwork and cost

### ⬜ 3 — a re-read note in `seal/ledger.md` says a commit is counted only where a shell reads `git`, and a quoted `>` breaks that

The row *Only a segment whose command word is `git` with the `commit`
subcommand is counted…* carries round 1's fix-pass note: "a commit is still
counted only where the command word is `git` as a shell reads it". shlex
drops the quotes before `unglued` cuts, so `"git>x" commit -m x` and
`git">"/dev/null commit -m x` read as commits at the head. The shell runs
`git>x` there, and bash and zsh did not commit. It is a stop, in the
direction the item accepts. The correction is the note naming the quoted
`>` as a case the view reads and the shell does not.

### ⬜ 4 — every body the gate reads is now split twice, so a flat chain of host words costs about 1.8 times the base

`hooks/commit-review-gate.py#_reads_a_commit` asks `split_segments` and then
`merged_segments`, which splits the same text again. It also reads the
`unglued` views. Profiled on `git -C /x commit -m x; ` followed by 600 `sh -c`
words, `split_segments_with_separators` runs 364,203 times at the head
against 182,102 at the base, and the call takes 13.7 s against 8.1 s. The
chain is quadratic at both: 8.7 s against 15.9 s at 1,000 words.

Extrapolated and not executed: the base would cross the harness's 600 s hook
limit near 8,300 words and the head near 6,150, and a timed-out hook is
silence. So between those lengths a commit the base stops would read silent.
Nobody writes such a command, and the base itself goes silent a little
further out. It is recorded so the depth work has the figure. Splitting
once with separators and deriving both views from the one result would
halve the splits.

## Round 1's nine verdicts

| Round 1 | Claim in its verdict cell | What this round found |
|---|---|---|
| red 1 | W1's refusal is added beside the base's directory, and the moved shell, the parked failure and the name environment read the as-written answer | Holds. The walk code reads that way. The W1 corpus below loses 0 and adds 0 against `86256492`. Head's test modules against `3b8522c3`'s hooks fail the 10 waiver prefixes, the 4 not-opted-in shapes and the parked case. The guard and `creation_directory` match the base on round 1's shapes |
| red 2 | the two header readings are loops bounded at 32, answering in the stopping direction | Holds. `_is_the_program` and `_segment_names_an_unknown_command` loop to `HEADERS_READ`. Through `main()`, 3 header kinds × 2 forms at 400, 1,200, 3,000 and 10,000 all stop at the head, silent at `3b8522c3` from 1,200, and take 0.5–12.6 s at 10,000 against the base's 0.5–12.8 s. Fifteen other chains at 5,000 raise nothing at the base, the head or the fix |
| yellow 3 | the walk asks the glued group | Holds. `2>&1 cd U`, `>&2`, `<&0`, `>&-`, `>|f`, `&>` and `2>&1 2>&1 cd U` add an unresolved directory beside, and bash and zsh commit in `U` for each |
| yellow 4 | `unglued` and the `merged_view` change read a glued operator | Holds for all 12 glued shapes bash commits. It also adds two stops no shell commits, `"git>x" commit` and `git">"/dev/null commit` (white 3) |
| yellow 5 | zsh's runners and short `for` are read, and `for d in git commit` stays silent | Holds. zsh commits for every commit shape, and the two pinned controls read no commit at any SHA while neither shell commits. Four new stops commit nothing: `for i (1) echo git commit`, `noglob echo git commit`, `repeat 1 echo git commit` (the stand-in `git` behind a runner) and `foreach i (1) git commit`, which zsh refuses without `end` |
| yellow 6 | the string is found past options and `--` behind a redirection | Holds for all 11 shapes bash commits. The replaced call to `_string_at` asked nothing the loop does not ask. One new stop commits nothing: `bash -c 2>/dev/null --norc "$CMD"`, which bash refuses |
| white 7 | `evidence-check` refuses nothing | Holds. `--strict` exits 0 with 3,026 ok and 0 refused |
| white 8 | the five records say added beside | Holds for the spec, I2, I10, E7 and the policy. The changelog fragment's "only adds stops" is true again once yellow 2 lands |
| white 9 | I5 records the 3 recorded commands | Holds. The same 3 commands, in 28,527, are the only difference between `86256492` and `3b8522c3` |

## The five things the orchestrator asked about

1. **The invariant, rebuilt.**
   - *The W1 corpus.* 12 redirection spellings, 14 words and 5 placements
     give 784 segments. Each was run with 3 separators in 4 session kinds:
     `[no-review]` over a parity arm, a directory not opted in then `cd u2`,
     a directory not opted in then `git -C "$SB"`, and an opted-in
     undeclared control. That is 9,408 commands through `main()` at each
     tree. The head stops exactly where `86256492` stops, with 0 lost and 0
     added. `3b8522c3` lost 1,646 of them: 726, 704, 216 and 0 by kind. The
     head's additions over `3b8522c3` are exactly those 1,646. Each is a
     commit the command runs if the prefix does not move it elsewhere. Some
     of the K2 ones are the base's own false stops, where `cd sub` would have
     made `cd u2` fail.
   - *The depths* are in the red 2 row above.
   - *The recorded commands.* 28,527 distinct pairs of command and directory
     come from all 525 of this repository's transcripts. Every target
     `86256492` or `3b8522c3` found is found at the head, and nothing raised.
     The head differs from `3b8522c3` on 3 commands. All 3 are round 1's own
     fix-pass patches, `python3 -` heredocs whose Python strings hold `for i
     (1) git commit`, so they are false stops in the class the base already
     reads, a heredoc body fed to an interpreter.
   - *The other direction on built shapes.* Of 69 shapes near the new
     readers, bash or zsh commits in 50, and the head reads a commit in every
     one of those 50. Of the 45 the head newly reads over `3b8522c3`, 7 are
     commands no shell commits (yellows 4 to 6 above). All are stops.
2. **The new readers against bash 3.2.57 and zsh 5.9.** Both pinned controls
   read no commit at all three SHAs, and neither shell commits. The near
   shapes are in the yellows 3 to 6 rows above.
3. **The guard and the consent writer.** 21 shapes from a clean `S` with a
   dirty nested `w` give the same answers at the head and at `86256492`,
   decision and consent directory alike. `3b8522c3` differs on exactly
   round 1's five (`2>/dev/null cd .; cd w`, the `source` and `eval` forms,
   and two creations filed under `S`).
4. **`2>/dev/null cd w && git switch -c nb`** is this round's yellow 1.
5. **The ledger.**
   - I2, I10, I11, I12, I5 and E7, E10 and E13 of 1790644505 each read true
     at the head, apart from E7's lead, which is yellow 2.
   - The re-pointed row in `seal/releases/0.4.0.md`, anchored on `elif
     as_written:`, is true, and its case passes in the modules run below.
   - `evidence-check --strict`, `correction-check --range
     origin/release/v0.16.0...HEAD` and `survivor-check` over the same range
     all exit 0, and they agree: 0 drifted, 0 refused, no merge commit, no
     removed wording standing.
   - *The interpreter floor.* The only hit for `strict=`, `pairwise` or
     `.UTC` under `hooks/` is `hooks/root-migrate.py:439`. It was there at
     `86256492`, and `tests/test_a_script_says_which_interpreter_it_needs.py`
     names it as deferred to #226. The four hooks this item reads parse under
     macOS's `/usr/bin/python3` 3.9.6, and the gate ran there on four new
     shapes. The fix below adds none of the three.

## Regression tests to plant

Each was seen red against the head's hooks (9 failed) and green with the fix
(9 passed):

- `tests/test_no_shape_the_base_stops_reads_silent.py`:
  - yellow 1: seven `cd` spellings with a redirection among their words, from
    a directory that is not opted in and under `[no-review]` over a parity
    arm;
  - yellow 2: two commands the base's reading placed, under `[no-review]`.
- `tests/test_guard_resolves_the_tree_it_judges.py`:
  - yellow 1: three switches into a dirty nested clone, and the consent
    directory of a creation there.

The code is in the fenced blocks below.

## Facts for the evidence ledger

- **A new row for yellow 1.** A `cd` whose words hold a redirection lands
  where the redirection is read past, in front of the answer the walk read
  with it. It is anchored on `hooks/cmdline.py#walk_directories` and the two
  test cases named above (NAME NOT IN TREE until the fix lands).
- **E10, re-read.** The walk's unplaced flag replaces the directory only
  where the first reading unplaces, and adds beside where only the second
  does and the first found `git`.
- **I2 and I12** drift with `walk_directories` and are re-read against both
  changes. I2's claim still holds, and I12's "the walk asks a cut
  redirection's glued group" now also lands its `cd`.
- **The `seal/ledger.md` row in white 3** takes the correction there.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a `cd` with a redirection among its words (`cd W 2>/dev/null`, `2>/dev/null cd W`, `cd W>/dev/null`) is never landed, so the worktree guard skips the tracked-changes question for a switch into a dirty clone, the consent writer files the creation under the session's clone, and the commit gate is silent from a directory not opted in and under `[no-review]` over a parity arm | `hooks/cmdline.py#walk_directories` | open | Executed through `main()`: silent at `86256492`, `3b8522c3` and the head on 8 of 9 tails from a directory not opted in and 5 of 9 under the waiver. The guard is silent on 3 switches, and bash 3.2.57 and zsh 5.9 commit in all 8 shapes given. With the fix, 38 of 38 stop and the guard asks. The corpus loses 0 and adds 8 real commits. 9 cases are red at the head and green with the fix |
| 🟡 2 | the walk's reading past redirections replaces the directory the base judged wherever it alone unplaces the segment, so a command the base stopped reads silent under `[no-review]` | `hooks/cmdline.py#walk_directories` | open | Executed: `nice 2>/x/git commit -m git` and `env </x/git commit -m git` under `[no-review]` over a parity arm ask at `86256492`, are silent at `3b8522c3` and the head, and ask with the fix. Neither commits, but the policy sentence, E7's lead and the changelog's "only adds stops" are false as written |
| ⬜ 3 | round 1's fix-pass note says a commit is counted only where a shell reads `git`, and a quoted `>` reads as one the shell does not run | `seal/ledger.md` | open | Executed: `"git>x" commit -m x` and `git">"/dev/null commit -m x` read as commits at the head, while bash and zsh commit neither. A correction to the note |
| ⬜ 4 | every body read is split twice and cut again, so a flat chain of host words costs about 1.8 times the base | `hooks/commit-review-gate.py#_reads_a_commit` | open | Executed: 600 `sh -c` words take 13.7 s against 8.1 s, and 1,000 take 15.9 s against 8.7 s, quadratic at both. The 600 s window between about 6,150 and 8,300 words is extrapolated, not run |
| 🟢 | round 1's blocking finding 1 is closed — W1's refusal is added beside the base's directory in the gate, the guard and the consent writer | `hooks/cmdline.py#walk_directories` | confirmed | Executed: 9,408 W1 commands in four session kinds lose 0 and add 0 against `86256492`, where `3b8522c3` lost 1,646. 15 of head's cases red at `3b8522c3`'s hooks. The guard and `creation_directory` match the base on 21 shapes |
| 🟢 | round 1's blocking finding 2 is closed — the header readings stop at 32 and keep the commits found | `hooks/cmdline.py#_is_the_program` | confirmed | Executed: 24 depth cases through `main()` stop at the head at every depth, silent at `3b8522c3` from 1,200, 0.5–12.6 s at 10,000 against 0.5–12.8 s. 6 cases red at `3b8522c3` |
| 🟢 | round 1's yellow 3 is closed — a `cd` behind a cut redirection adds an unresolved directory | `hooks/cmdline.py#walk_directories` | confirmed | Executed: 7 cut shapes add it, bash and zsh commit in `U`. 11 walk cases red at `3b8522c3` |
| 🟢 | round 1's yellow 4 is closed — a glued operator is read | `hooks/cmdline.py#unglued` | confirmed | Executed: all 12 glued shapes bash commits read, and 21 no-commit cases red at `3b8522c3`. Two extra stops that commit nothing are white 3 |
| 🟢 | round 1's yellow 5 is closed — zsh's precommand words and short loop are read | `hooks/cmdline.py#RUNNERS` | confirmed | Executed under zsh 5.9. `for d in git commit` reads nothing and commits nothing. Four new stops commit nothing and are the stand-in's accepted class |
| 🟢 | round 1's yellow 6 is closed — a shell's string is found past options and `--` | `hooks/cmdline.py#command_strings` | confirmed | Executed: 11 shapes bash commits all read. `--norc` behind `-c` is a stop bash refuses to run |
| 🟢 | round 1's white 7 is closed — the checker refuses nothing | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/questions.md` | confirmed | Executed: `evidence-check . --strict` exit 0, 3,026 ok, 0 refused |
| 🟢 | round 1's white 8 is closed — the records say added beside | `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/spec.md` | confirmed | Read against the code at the head. The changelog's "only adds stops" waits on yellow 2 |
| 🟢 | round 1's white 9 is closed — I5 carries the recorded figure | `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md` | confirmed | Executed over 28,527 recorded commands: the same 3 are the only difference between `86256492` and `3b8522c3` |
| ❓ | the 18 mutants round 1's fix pass names for its changed branches | `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md` | ❓ out of verified scope | Read, not re-run. The fix pass's records answer for them |
| ❓ | the cases on Windows | `tests/test_no_shape_the_base_stops_reads_silent.py` | ❓ out of verified scope | CI's `windows-latest` leg at the pull request answers it |

## Executed probes

| What was run | Result |
|---|---|
| The W1 corpus through `main()`: 9,408 commands (784 segments × 3 separators × 4 session kinds) at `86256492`, `3b8522c3`, the head and the fix | Head against base: 0 lost, 0 added. `3b8522c3`: 1,646 lost. Fix against base and head: 0 lost, 8 added, all real commits. Raised: 0 anywhere |
| 28,527 recorded commands from 525 transcripts through `commit_invocations` at the four trees | Every base and `3b8522c3` target is found at the head and with the fix. Head against `3b8522c3`: 3 differ, round 1's own heredoc patches. Fix against head: 0 differ. Raised: 0 |
| Header nesting through `main()`: 3 kinds × 2 forms at 400, 1,200, 3,000 and 10,000, at `86256492`, `3b8522c3` and the head | Head stops at all 24. `3b8522c3` is silent at 18. At 10,000 the head takes 0.5–12.6 s and the base 0.5–12.8 s |
| 15 other chains at 5,000 through `commit_invocations` at base, head and fix | Nothing raised. The fix makes 5,000 `cd>/dev/null x;` take 4.0 s against 0.3 s |
| A chain of `sh -c` words at 500 and 1,000 at base and head, and a profile at 600 | 2.2 s and 8.7 s at the base, 4.0 s and 15.9 s at the head, twice the splits (white 4) |
| 69 shapes near the new readers through `commit_invocations` at three SHAs, and each in bash 3.2.57 and zsh 5.9 against fresh repositories | A shell commits in 50, and the head reads all 50. The two controls read nothing, and no shell commits. 7 new stops commit nothing |
| 38 `cd` tail shapes through `main()` in three session kinds at the four trees | Silent at base, `3b8522c3` and head on 18, and all 38 stop with the fix |
| 8 `cd` tail shapes in bash 3.2.57 and zsh 5.9 | Both shells commit in `U` for all 8 |
| The worktree guard and `creation_directory` on 21 shapes from a clean `S` with a dirty nested `w`, at the four trees | Head equals base on all 21. `3b8522c3` differs on round 1's 5. The fix differs from the head on 4: three switches ask and one creation is filed under `S/w` |
| `: '[no-review]'` over a parity arm with 4 commands whose `git` word is a redirection target, at the four trees | 2 ask at the base, are silent at `3b8522c3` and the head, and ask with the fix |
| The two changed test modules of the head against `3b8522c3`'s hooks | 59 failed and 525 passed: the 10 waiver prefixes, 4 not-opted-in shapes, the parked case, 6 header cases, 21 no-commit shapes, 11 walk shapes and 3 wrapper rows × 2 |
| 13 reader modules at the head, and at the fix with the 9 planted cases | 1,141 passed at the head. 1,150 passed with the fix, after the first version of yellow 2's fix turned `REDIRECTED_UNPLACED` red |
| The 9 planted cases against the head's hooks, and a mutant appending the landing behind the answer | 9 failed at the head. The mutant fails the guard case only |
| `ruff check` and `ruff format --check` on the fix's three files. `tests/test_docs_line_wrap.py`, `tests/test_one_word_one_meaning.py` and `tests/test_no_real_identifiers.py` with its doc edits | Clean. 58 passed |
| `bin/evidence-check . --strict`, `bin/correction-check --range origin/release/v0.16.0...HEAD` and `bin/survivor-check` over the same range, at the head | Each exit 0: 3,026 ok and 0 refused, no merge commit, 43 removed sentences with none standing |
| The four hooks this item reads, parsed and the gate run under `/usr/bin/python3` 3.9.6, at the head and with the fix | They parse, and the gate answers. No `strict=`, `pairwise` or `.UTC` in the fix |
| The broad gate: the full suite, the repository-wide lint and the typecheck | not yet. It belongs to the sealer, once the rounds settle, and it is not due while this round leaves yellows 1 and 2 open |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The worktree guard reads an unresolved directory as the session's own and judges only a segment's first directory. So a switch into a dirty clone is silent at `86256492` and the head after `builtin cd w`, `command cd w`, `time cd w`, `pushd w`, `noglob cd w`, `cd "$W"` with `W` unset, and `2>&1 cd w`, where the walk reads the splitter's `&` as a background job. §*Which tree* states the fallback on purpose, and changing it is a guard design choice | #686, in no milestone: it waits on the owner's decision | the orchestrator, who files it, and the owner, who decides whether the guard asks on an unresolved directory |

## Paste-ready fixes

### 🟡 1 and 🟡 2 — the walk

```diff
--- a/hooks/cmdline.py
+++ b/hooks/cmdline.py
@@ def walk_directories(items, cwd):
         # Asked as written and read past its redirections (#674), and either
         # one unplaces: `2>/dev/null nice -n 5 git commit` stands behind a
         # runner's options that the first reading never reached.
-        if command_word(tokens)[1] or command_word(tokens, redirections=True)[1]:
+        unplaced = tuple(
+            w if isinstance(w, Unresolved) else Unresolved(str(w), Unresolved.CONSTRUCT)
+            for w in wheres
+        )
+        first, first_unplaced = command_word(tokens)
+        if first_unplaced:
             # A command behind a reserved word that begins a list, or inside a
             # construct whose command word is not found by position (#669).
             # Written across lines it would follow a segment `understood`
             # refuses, and that is the directory it gets here too.
-            wheres = tuple(
-                w
-                if isinstance(w, Unresolved)
-                else Unresolved(str(w), Unresolved.CONSTRUCT)
-                for w in wheres
+            wheres = unplaced
+        elif command_word(tokens, redirections=True)[1]:
+            # Only the second reading unplaces. Where the first already found
+            # `git`, that is the commit `86256492` judged in WHERES, and the
+            # unresolved directory is added beside it rather than in its
+            # place (round 2 of 1790660768): `nice 2>/x/git commit -m git`
+            # stopped on the parity arm at the base, and `[no-review]` waived
+            # the replacement whole.
+            placed = bool(first) and os.path.basename(first[0]) == "git"
+            wheres = (
+                _directories([(w, None) for w in wheres + unplaced])
+                if placed
+                else unplaced
             )
         walked.append((tokens, wheres))
 
@@ def walk_directories(items, cwd):
             (here if target is None else _land(here, prev, target), here)
             for here, prev in running
         ]
+        # A redirection among a `cd`'s words -- after its operand (`cd W
+        # 2>/dev/null`), glued to one (`cd W>/dev/null`), in front of it, or
+        # cut by the splitter (`2>&1 cd W`) -- is the shell's, and the `cd`
+        # still lands in W (round 2 of 1790660768). Read as an operand it
+        # made the target unknown, and read as the program it left the shell
+        # where it was: silence from a session that is not opted in, and
+        # under `[no-review]` over a parity arm, where `cd W` stops. The
+        # landing read past it is ADDED in front of that answer and never
+        # replaces it, so the commit gate judges both, and the worktree guard
+        # and the consent writer, which take the first directory they can
+        # name, take the one the shell went to.
+        view = _expanded(glued[index], env) if index in glued else tokens
+        past = _cd_target(_without_redirections(unglued(view) or view))
+        if past is not None and past != target:
+            moved = _dedup(
+                [(_land(here, prev, past), here) for here, prev in running] + moved
+            )
 
         # A construct the reader does not understand leaves the shell
```

### 🟡 1 and 🟡 2 — the policy documents

```diff
--- a/docs/commit-review-gate-spec.md
+++ b/docs/commit-review-gate-spec.md
@@ So each place a program word stands is read past what the shell takes off it:
   for a redirection glued to a word's end (`cd>/dev/null W`), and for one the
-  splitter cut (`2>&1 cd W`).
+  splitter cut (`2>&1 cd W`). A redirection after a `cd`'s operand, or glued
+  to one (`cd W 2>/dev/null`, `cd W>/dev/null`), is the shell's as well. The
+  landing read past any of these is added in front of the directory the walk
+  read with it: the gate judges both, and the worktree guard and the consent
+  writer, which take the first directory they can name, take W.
@@ The reading can only have gained stops by this.
 asked before first and adds what the new reading finds, `understood`'s
-refusal is added beside the directory the walk read before, and a generated
+refusal is added beside the directory the walk read before, the walk's
+reading past redirections unplaces a segment beside its directory and never
+in place of it, and a generated
 corpus of 11,393 commands across these positions found none silent where the
--- a/docs/worktree-guard-spec.md
+++ b/docs/worktree-guard-spec.md
@@ ### Which tree, when the command walks to it
 was while the commands do not. Both are read the same way the commit gate
-reads them (`commit-review-gate-spec.md` §Which repository).
+reads them (`commit-review-gate-spec.md` §Which repository). A redirection
+among the `cd`'s words (`cd W 2>/dev/null`, `2>/dev/null cd W`, `cd>/dev/null
+W`) moves it too, since round 2 of work item 1790660768; until then the switch
+was judged in the session's own tree while it ran in W.
```

### 🟡 1 — the changelog fragment

```diff
--- a/seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/changelog.md
+++ b/seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/changelog.md
@@
   cut (`2>&1 cd W`), and a shell's string past `--` or an option after a
   redirection (`bash -c 2>/dev/null -- "$CMD"`). bash or zsh committed for
-  each.
+  each. A `cd` with a redirection after its operand (`cd W 2>/dev/null && git
+  commit`) now lands in W too. It was silent from a directory that is not
+  opted in and under `[no-review]`, and the worktree guard judged the
+  session's own tree for a switch made in W.
```

### 🟡 1 and 🟡 2 — the cases

```python
# tests/test_no_shape_the_base_stops_reads_silent.py, appended
CD_BEHIND_A_REDIRECTION = [
    "cd {d} 2>/dev/null",
    "cd {d} >/dev/null",
    "cd {d} 2> /dev/null",
    "cd {d} </dev/null",
    "cd {d} >/dev/null 2>&1",
    "cd -P {d} 2>/dev/null",
    "cd {d}>/dev/null",
]


@pytest.mark.parametrize("cd", CD_BEHIND_A_REDIRECTION)
def test_a_cd_with_a_redirection_among_its_words_lands(
    monkeypatch, capsys, projects, tmp_path, cd
):
    """Round 2 of 1790660768. A redirection after a `cd`'s operand is the
    shell's, and the `cd` still lands; the walk read it as a second operand
    and left the target unresolved. An unresolved target is silence from a
    session that is not opted in and is waived whole by `[no-review]`, so
    both commands were silent at `86256492` and at #674's head, where `cd D
    && git commit` stops. bash 3.2.57 and zsh 5.9 commit in D."""
    plain = tmp_path / "plain"
    plain.mkdir()
    make_repo(plain / "u2")
    command = f"{cd.format(d='u2')} && {BODY}"
    got = decisions(monkeypatch, capsys, command, plain, "s")
    assert "silent" not in got, (command, got)
    session = make_repo(tmp_path / "session", declared=True)
    (session / "sub").mkdir()
    (session / "seal" / "parity.md").write_text("# parity\n")
    (session / "a.py").write_text("x = 1\n")
    subprocess.run(["git", "-C", str(session), "add", "a.py"], check=True)
    command = f": '[no-review]'; {cd.format(d='sub')} && {BODY}"
    for which, got in with_and_without_the_press(
        monkeypatch, capsys, projects, command, session
    ).items():
        assert "silent" not in got, (command, which, got)


def test_a_second_reading_that_unplaces_keeps_the_base_directory(
    monkeypatch, capsys, projects, tmp_path
):
    """Round 2 of 1790660768. The walk's reading past redirections REPLACED
    the directory the base judged with an unresolved one wherever it alone
    unplaced the segment, and `[no-review]` waived that whole: `nice
    2>/x/git commit -m git`, a commit to the base's reading, stopped on the
    parity arm at `86256492` and was silent at #674's head."""
    session = make_repo(tmp_path / "session", declared=True)
    (session / "seal" / "parity.md").write_text("# parity\n")
    (session / "a.py").write_text("x = 1\n")
    subprocess.run(["git", "-C", str(session), "add", "a.py"], check=True)
    for shape in ("nice 2>/x/git commit -m git", "env </x/git commit -m git"):
        command = f": '[no-review]'; {shape}"
        for which, got in with_and_without_the_press(
            monkeypatch, capsys, projects, command, session
        ).items():
            assert "silent" not in got, (command, which, got)
```

```python
# tests/test_guard_resolves_the_tree_it_judges.py: add `import shutil` beside
# `import shlex`, then append
def test_a_cd_behind_a_redirection_moves_the_tree_the_guard_judges(
    monkeypatch, capsys, repo, tmp_path
):
    """Round 2 of 1790660768. A redirection among a `cd`'s words is the
    shell's, and the switch runs in the tree the `cd` reached. The walk read
    it as an operand or as the program, and the guard judged the clean
    session tree instead of the dirty one the switch lands in -- silent at
    `86256492` and at #674's head. The consent writer filed the creation
    under the session's clone for the same reason."""
    session = tmp_path / "session"
    session.mkdir()
    subprocess.run(["git", "-C", str(session), "init", "-q"], check=True)
    shutil.copytree(repo, session / "w")
    (session / "w" / "f.txt").write_text("changed on purpose\n")
    for command in (
        "cd w 2>/dev/null && git switch feature/x",
        "2>/dev/null cd w && git switch feature/x",
        "cd>/dev/null w && git switch feature/x",
    ):
        decision, reason, _ = run(monkeypatch, capsys, command, session)
        assert decision == "ask", (command, decision, reason)
        assert "f.txt" in reason, (command, reason)
    acted = wg.worktree_consent.creation_directory(
        "2>/dev/null cd w && git worktree add ../wt", str(session)
    )
    assert os.path.samefile(acted, session / "w"), acted
```

Needs a fix: yes — 🟡 1 (a `cd` with a redirection among its words is never landed: the guard, the consent writer and two session kinds of the commit gate judge the wrong tree), 🟡 2 (the walk's second reading replaces the base's directory where only it unplaces)
Loses a record or crashes: yes — 🟡 1: `creation_directory` files `2>/dev/null cd w && git worktree add` and `cd w 2>/dev/null && git worktree add` under the session's own clone, so the clone the creation ran in gets no record and the session's clone gets one nobody gave. The same effect counted as yes for round 1's red 1, and here it is also present at `86256492`

## Proof block

Opened this round:

- `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/rounds/round-1.md`
  and `round-1-report.md` (lines 1–300), `spec.md` (§*What the worktree
  guard sees* and its neighbours), `changelog.md`;
- `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md`
  (I2, I5, I10, I11, I12), `seal/ledger/1790644505-the-commit-gate-stops-asking-about-commits-that-are-not-there.md`
  (E7, E10, E13), and the diffs of `seal/ledger.md` and
  `seal/releases/0.4.0.md` over `86256492..1b444773`;
- `hooks/cmdline.py`: `_REDIRECTION`, `redirection_width`, `unglued`,
  `split_segments_with_separators`, `merged_view`, `_string_at`,
  `command_word`, `HEADERS_READ`, `_is_the_program`, `command_strings`,
  `names_an_unknown_command`, `_segment_names_an_unknown_command`,
  `_without_redirections`, `understood`,
  `_unreadable_past_leading_redirections`, `_past_leading_redirections`,
  `_cd_target`, `_land`, `walk_directories`, and the `86256492..1b444773`
  diff of `parse_git` and `_git_options`;
- `hooks/commit-review-gate.py`: `_hides_a_commit` to `commit_invocations`,
  `_segment_invocations` and `main`;
- `hooks/worktree-guard.py`: `walk_command`, `judgeable`, `main` to its
  first `judge_creation`; `hooks/worktree_consent.py#creation_directory`;
- `docs/commit-review-gate-spec.md` (the #674 bullets and the paragraph
  after them) and `docs/worktree-guard-spec.md` (§*Unknowns resolve
  conservatively*, §*Which tree, when the command walks to it*);
- `tests/test_no_shape_the_base_stops_reads_silent.py`, the
  `REDIRECTED_UNPLACED` cases of
  `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`,
  and the dirty-tree and unreadable-`cd` cases of
  `tests/test_guard_resolves_the_tree_it_judges.py`;
- `CONTRIBUTING.md` (the floor paragraph) and
  `tests/test_a_script_says_which_interpreter_it_needs.py` (the floor
  pattern and its allowlist).

Every probe, clone and fixture of this round lived under the session's
scratchpad and was removed at handover. Nothing in the repository was written
but this file.
