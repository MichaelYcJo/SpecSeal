# Implementation Plan: the commit gate reads the rest of what a shell runs (#674)

<!-- seal/specs/<unix-epoch-seconds>-<slug>/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-29 by the orchestrating session, when `smith` was spawned.

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

The commit gate reads the rest of #670's class. That covers a program word
behind a redirection, whether the redirection was cut by the splitter or not,
and a program word inside a `case` arm, a function body or a coprocess. It
covers a word glued to `(`, and the string a host runs when a redirection
stands after its flag. It adds the hosts among `RUNNERS` that `1790644505`'s
enumeration did not mark. And it bounds how deep one body is read inside
another.

Every changed unit keeps the base's answer and adds to it (`spec.md` decision
1). That is how the invariant holds by construction and not by a proof about
shell commands. The base is `86256492`.

## Technical context

The units, each read at `86256492`:

- `hooks/cmdline.py`:
  - `command_word` reads past assignments, runners, `!` and list openers, and
    stands in the first `git` or `eval` inside `UNPLACED`, a pattern or a
    definition.
  - `_git_options` stops at the first word that does not start with `-`.
  - `understood` refuses a `cd` behind a prefix (`return at == 0`).
  - `split_segments_with_separators` runs `shlex` with
    `punctuation_chars=";|&"`.
  - `reparsed_texts` and `command_strings` compare `os.path.basename(tok)` on
    raw tokens.
  - `_is_the_program` accepts assignments, list openers, `!`, `(` and a
    runner.
  - `names_an_unknown_command` asks `command_word(toks)[0]`.
- `hooks/commit-review-gate.py`:
  - `_hides_a_commit` catches `RecursionError`.
  - `_reads_a_commit` splits with `split_segments`, so the separators are
    lost.
  - `commit_invocations` walks `split_segments_with_separators`' items.
  - `_string_hides_a_commit` ORs `reparsed_texts` and `command_strings`.
- The guard reads `parse_git` and `walk_directories`
  (`hooks/worktree-guard.py#walk_command`, `#segment_cwd`, `#classify`), and
  so does the consent writer (`hooks/worktree_consent.py`). Both map an
  `Unresolved` directory to `cwd`.

**What breaks in six months if this is built as chosen.** The merged view is
a second reading of the same tokens. The splitter could one day be taught
about `>&` for a reason of its own. The view would then find nothing to glue
and go quiet, and the cases planted for P6 are what would say so. The
positional header reading is a small grammar, and a header spelling nobody
listed falls to the stand-in. That is a stop in front of a person, which is
the direction this repository accepts. The first report of such a stop is
the signal to add the spelling, never to remove the fallback.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| **A. Round 3's paste-ready fixes as written** | Four gaps, each read at `86256492`:<br>(1) the `REDIRECTION` pattern does not fullmatch a spaced `<<`, so `<< EOF watch …` is missed;<br>(2) the `watch` filter drops a bare `2>` and keeps `/dev/null`, so `watch -g 2> /dev/null "$CMD"` joins to `/dev/null $CMD`;<br>(3) `su`, `runuser`, `script` and `env -S` keep taking a redirection for the string;<br>(4) nothing reads a redirection in front of `git` or `eval`, so `2>/dev/null git commit -m x` stays silent.<br>Its stand-in for `watch` in headers also stops `grep -n watch *.py` inside a function body | Its rows and its depth-bound code are adopted. The design is not |
| **B. Teach the splitter `>&`, `&>`, `<&` and `>\|`** | Every segmentation in both gates and in the walk moves. `cd W 2>&1 && git commit -m x` is read today as a `cd` in a backgrounded segment, so the commit is judged in the session directory as well. Read correctly, it is judged in `W` alone, and a declared `W` then reads silent where the base stopped. The guard and the consent writer move with it | Rejected. It breaks the invariant in the shapes it corrects |
| **C. A second, redirection-aware tokenizer for the string readers** | Two models of one question drift apart, which is the failure `hooks/cmdline.py`'s docstring and `_heredoc_split`'s comment record, measured | Rejected |
| **D. One position reader, each unit a superset of its base answer, a merged view for the cut operators, a named depth bound** | The positional header grammar can miss a spelling. A miss falls to the stand-in, which is a stop and never a silence, and the base is silent on every P7–P9 `watch` anyway. So a miss is never below the base | **Chosen** |
| **E. The stand-in everywhere: any `watch` in a segment holding a header counts** | `f() { grep -n watch *.py; }; f` stops in an attended session. That is the cost round 1 of `1790644505` ruled a defect for `grep watch` at the top level | Rejected for headers the reader can place, and kept as the fallback where it cannot |
| **F. Keep P4 inside a string as the base reads it** (the word right after the runner) | `sh -c 'nice -n 5 $CMD'` stays silent. That contradicts "where the reader cannot be certain, it stops" and the #670 sentence the spec keeps | Rejected. The stand-in counts a later word that expands, as the base already does for `watch` behind a runner. Its cost is (b), counted by Q2 |
| **G. A bound on the bytes read instead of the depth** | It also bounds a wide, shallow command, which has no measured cost today. A depth bound answers the one shape measured slow, and a count of calls pins it | Rejected. Depth, 32 |
| **H. A lower depth bound, 16** | It halves the pathological time, with no measurement behind the number. 32 has round 3's 1.8 s and 3.3 s | Rejected. Phase 5 records the time at 32. A value below it needs its own measurement |
| **I. A timeout in `hooks/hooks.json`** | A harness that kills the hook produces no output, and no output is silence | Rejected |
| **J. Read `parallel`'s template for expansion** | Placing its command word means parsing its options, which take values, and its `:::` or `::::` inputs | Rejected. `parallel` is read for a commit only |

## Phases

Vertical slices. Each phase ends with its rows planted, seen red at
`86256492` and green after. `tests/test_no_shape_the_base_stops_reads_silent.py`
passes before and after, and one mutant per changed branch is killed under
`PYTHONDONTWRITEBYTECODE=1`. `bin/test` runs the modules that load the gate,
`hooks/cmdline.py`, the guard or the consent writer. The broad gate is the
sealer's, once, after the rounds settle.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **A program word behind a redirection or glued to `(`** (`spec.md` P5, P10, W1). One recognizer for every redirection form in P5 and P6, glued and spaced. `command_word` reads past leading redirections, for `git`, `eval` and the string's command word. `_git_options` reads past a redirection before the subcommand. `understood` refuses a `cd`, a relocator, a reserved word or an expanding word reached past a leading redirection, the rule it already has for a prefix. `_is_the_program` reads past redirections and a glued `(`. Host words glued to `(` are recognized in `reparsed_texts` and `command_strings`. Each unit keeps its base answer where that answer found something | S1, S2 and S5's `(sh`/`(watch` rows, each red at `86256492`. S8's P5 and P10 rewrites of the controls stay silent. The guard's modules pass. A case pinning a redirected git as unread moves group, and the phase record says so. `2>/x/git commit` still stops, the edge in decision 1 | a94e22bc |
| 2 | **Compound headers, and P4 inside a string** (`spec.md` P7–P9, P4). The positional reading of a `case` arm (first and later arms, `(P)`, `P )`), a function definition in the six spellings, `coproc` with and without a NAME. It is used for `watch` and for the string's command word, with the stand-in only where a header cannot be placed. Inside a string, a later word that expands counts behind a runner's options | S3, red at `86256492`. S8's P7–P9 rewrites of the controls stay silent, and each is seen red by a mutant that uses the stand-in for a placeable header. Q3's spellings are recorded as read by position or by the fallback | 7d488ee6 |
| 3 | **Strings past redirections, and the hosts `1790644505` did not mark** (`spec.md` §*The class, enumerated*, the string table). The shells', the `su`/`runuser`/`script` and the `env -S` pickers ask a redirection after the flag and read past it, a spaced target with its operator. `watch` adds its join without redirections. `sudo -s`/`-i` with a command and `flock -c`/`--command` become hosts, with their value-taking options from `man sudo` and `man flock` (Q4). `parallel` is read for a commit | S4 and S5's host rows, red at `86256492`. The round-1 controls stay silent. `test_every_enumerated_wrapper_has_a_shape` still passes | 14dc9fdb |
| 4 | **The merged view for the operators the splitter cut** (`spec.md` P6, decision 3). It glues a segment ending in a bare operator to the next across `&` or `\|`, and an `&` before a segment that begins with `>`, folding chains. `commit_invocations`, `_reads_a_commit` and `names_an_unknown_command` read it beside the original segments. It adds only what neither part found, with the directory of the part holding the command word or host | S6, red at `86256492`. S6's control: `commit_invocations` on `git commit -m x 2>&1 \| tail -1` equals its base list. The round-1 controls followed by `2>&1` stay silent | |
| 5 | **The depth bound** (`spec.md` decision 4). `NESTING_READ = 32` in `hooks/commit-review-gate.py`. `_hides_a_commit` answers True past it, and the `RecursionError` catch stays | S9. The call count is a case, red at `86256492`. The time for 4000 and 6000 nested `<(`, `$(` and backticks beside a commit, at `86256492` and after, is recorded in the phase record and the PR body. The §13 run with a lowered recursion limit, once, in a subprocess, is recorded too | |
| 6 | **Proof and records.** The differential corpus of S7 (b), and Q2's prompt budget. The #670 paragraph of `docs/commit-review-gate-spec.md`: the positions, the redirection rule, the merged view, the hosts, the bound, and its `Enforced by:` line. `docs/worktree-guard-spec.md`, if it names a word a redirection now reaches. The ledger fragment `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md`. The rows Q5 names, re-read in the files they are in with a dated note, and corrected where an edit made them false. The changelog fragment `seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/changelog.md`, naming #674 | S7 (b): zero rows silent at head where `86256492` stops, with the corpus size and the new-stop count on its non-commit half. Q2's counts. `evidence-check` exit 0 on every file touched. `rider_check.py`. The survivor sweep over the corrected sentences | |

What a phase finds that the next one needs goes in `phases/phase-N.md`, from
`templates/sdd-phase.md`, when it closes. This plan does not try to predict
it.

## Operational impact

- **No migration, no new environment variable, no new dependency.**
- **A behaviour change a person may notice.** Commands that run a commit, a
  shell string or `watch` from any of P4–P10 and W1 now meet the gate. In an
  attended session that is one refusal and then a prompt per re-issue. Under
  the `automation` press it is a refusal. Commands that commit nothing meet it
  only in (a)–(e) of `spec.md` §*How the controls stay unasked*.
- **The worktree guard** classifies a git behind a redirection, which it did
  not see before (`spec.md` §*What the worktree guard sees*).
- **For the pull request body.** It carries the failure direction and the
  prompt budget from `spec.md` §*What a change to a gate must carry*, Q2's
  counts, phase 5's times, and the three boxes of #674 answered.
