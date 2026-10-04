# Round 2 report — the worktree guard reads a glued value and a redirection

| Field | Value |
|---|---|
| Work item | 1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection |
| Round | 2 (verifying) |
| Target SHA | 675ef92a |
| Fix range opened | 58d4b7a5..cd684fb2 (e3c5101b, 0a2e0fd0, cd684fb2) |
| Base | `release/v0.18.2` at 94d7b2e0 |
| Pull request | #788 (draft), issues #764 and #738 |
| Ran by | specseal:warden on claude-opus-5-5 |

Worked in a `git clone --no-local` of the worktree, checked out at 675ef92a,
under this round's scratch directory. Nothing was written in the worktree but
this file. git 2.54.0 (Apple Git-157), bash 3.2.57. The clone, its virtual
environment, every probe module and every scratch repository were deleted
before handover.

## Summary

Both of round 1's findings are closed, and the fixes opened nothing that
needs a fix.

- 🔴 1 is closed. git and the readers agree on every one of the 225 commands
  `_dashed` builds, and `_git_switches` is right on all 225. I also ran 53
  further `--` and `--end-of-options` placements that the axis does not
  build. Where git switches, the guard asks every one of them that a `--`
  decides.
- ⬜ 2 is closed. The reverse check sees every entry of the table on git
  2.54.0, and skipping an option git does not list is safe.

The corpus claim still holds after the fix. Over the same 25,741 recorded
pairs, the frozen reading at 675ef92a reads the same kinds as at a7ab2a4e,
and candidate C fires on none of them.

Two ⬜ notes remain. A test comment still states the rule the fix retired,
and `Corrected · G1`'s evidence cell does not record the fix pass's red. One
pre-existing silent shape was found while checking the axis: `git checkout
:/<message>`, a detach. It does not depend on `--`, it was silent at 94d7b2e0
too, and it goes under Deferred.

## What the account claimed, and what I found

| Claim (where) | Found |
|---|---|
| A bare trailing `--` is no restore in `classify` and `switch_kind`, and a `--` followed by a path stays one (e3c5101b, round-1.md) | **Executed**: 225 commands under bash in fresh scratch repositories, HEAD compared before and after, with both readers on the same command. No command git switches on is silent. Read: `hooks/worktree-guard.py:563` and `:1024` test `after` for truth, and `:1034` asks the path test only where no `--` was seen |
| `_git_switches` agrees with all 225 real git 2.54.0 commands (`tests/test_guard_resolves_the_tree_it_judges.py:1549` docstring) | **Executed**: 0 disagreements over the 225 |
| Every remaining mismatch with git is in the loud direction (prompt) | **Executed**: over the 225, 94 commands are asked where git does not switch, and git refused every one of them (exit 128). Over 53 extra placements, see Stage 1. The one quiet mismatch is `:/<message>`, which does not depend on `--` |
| D1: 4,512 of the 49,804 switching shapes were silent at a7ab2a4e once `--` is an axis, and none is silent with the fix (ledger fragment) | **Executed**: 49,804 shapes. 4,512 are silent with a7ab2a4e's guard: 3,384 with a bare `--` after the words and 1,128 with `--end-of-options` and a bare `--`. 0 are silent with 675ef92a's guard |
| D1: over the 25,741 recorded pairs, the build reads no switch the base did not and drops none | **Executed again after the fix** (it was measured at a7ab2a4e): the same 25,741 pairs re-extracted from this machine's transcripts. The tree-blind frozen reading gives the same kinds per segment at a7ab2a4e and at 675ef92a in every pair, and candidate C fires on 0 at 675ef92a. 488 pairs hold both `checkout` and `--` |
| D2: the reverse binding is red with `--guess` doctored to take a value | **Executed**: red for `--guess` on both subcommands, and also for `-q`, `-2`, `--recurse-submodules` (checkout) and `--track` (switch) doctored the same way |
| The policy sentence, the Known-limits sentence and `switch_kind`'s docstring say what `switch_kind` reads | **Read** clause by clause against `switch_kind`. **Executed**: the pin is red with a7ab2a4e's `docs/worktree-guard-spec.md` in place, and the Known-limits example `git checkout feature/x -- <&1 README.md` is judged a switch by the frozen loop, as written |
| The new cases were seen red (§15) | **Executed**: with a7ab2a4e's guard in place the module fails 11 tests: the new `KINDS` row, 8 rows of `test_classify_reads_a_switch_wherever_its_dashes_stand`, `test_a_bare_dashdash_names_the_branch_where_a_file_has_its_name` and `test_no_constructed_switch_is_silent`. At 675ef92a it gives 312 passed |
| The two new survivors.md rows quote the surviving text with grounds | **Executed**: `bin/survivor-check --range 58d4b7a5..cd684fb2` names exactly those two places, and with `--exempt` on this item's `survivors.md` it excuses both and exits 0. Read: each quote is in the file it names |

## Stage 1 — does each fix close its finding

**🔴 1 — closed.** I checked the axis by construction, against what git's
`checkout` does with argv once options are parsed. A `--` as the first word
is a restore of the words after it (or nothing). A `--` as the second word,
with nothing after it, names the first word as a commit and switches. With a
pathspec after it, the first word is a source tree, which makes a restore. A
`--` at a later position is refused (`only one reference expected, N
given`). A `--` taken as an option's value is refused for every value-taking
option in the table. `switch` consumes its first `--`, so it switches only
where exactly one name is left.

The readers now follow this. A word after the first `--` returns no switch
(restore or refusal). A bare `--` leaves the name before it as the switch
target. With two or more names before it, git refuses and the reader still
reads the first name, which is loud. So the switching direction is complete
for any placement. The generator does not need every placement as long as
the readers follow that argument, and the 53 extra placements below confirm
it on real git.

| Placement asked about (prompt) | Shape run under bash | git | Guard |
|---|---|---|---|
| `--` between two names | `checkout feature/x README.md --` | refused | asked (loud) |
| `--` twice | `checkout -- feature/x --`, `checkout feature/x -- --`, `checkout - -- --`, `checkout feature/x -- -- README.md`, `switch -- --`, `switch -- feature/x --` | refused or restore | silent for `checkout`, asked for `switch` (loud) |
| `--` after a creation option's value | `checkout -b y --`, `checkout -b y feature/x --`, `checkout --orphan y --`, `switch -c y --` | switches | asked |
| `--` taken as a creation option's value | `checkout -b -- feature/x`, `checkout --orphan --`, `checkout -b y -- feature/x` | refused | asked (loud) |
| `--end-of-options` alone or with a bare `--` | `checkout --end-of-options`, `checkout --end-of-options --`, `checkout --end-of-options -- feature/x` | nothing or restore | silent |
| `--end-of-options` after the name | `checkout feature/x --end-of-options`, `checkout feature/x --end-of-options --` | switches | asked |
| pathspec `.` or `:/` | `checkout feature/x -- .`, `checkout feature/x -- :/`, `checkout -- .`, `checkout -- :/` | restore | silent |
| `.` or a file name before a bare `--` | `checkout . --`, `checkout README.md --` | refused (`invalid reference`) | silent |
| a commit or `@{-1}` before a bare `--` | `checkout feature/x~0 --`, `checkout @{-1} --` | switches | asked |
| a branch and a file of one name | `checkout README.md --` with branch `README.md` | switches | asked (the new case pins it) |

**⬜ 2 — closed, and the skip is safe.** A deleted probe module matched every
line of `git checkout -h` and `git switch -h` with `USAGE`. Every key of
`SWITCH_OPTIONS` is in `listed`, nothing listed is missing from the table,
and every `VALUE` flag agrees. So on git 2.54.0 the reverse check covers the
whole table and skips nothing. On an older git, an option the table holds
and git lacks is one git refuses, so the command moves nothing whatever the
guard reads. I also looked for a case where a table larger than git's own
option set turns a prefix ambiguous for the table but unique for git onto a
value-taking option. That would read the value as a name and go quiet. I
found no such prefix among either subcommand's options (`--c`, `--o`, `--i`,
`--forc` are ambiguous or resolve the same in both). It is the static-table
limit §*Known limits* already names.

## Stage 2 — the new units, judged as code

`_dashed`, `_git_switches`, `DASHED`, `DASHED_SWITCHES`, `DASHED_TWINS` and
the two new tests are correct where I checked them (executed, above).
`test_classify_reads_a_switch_wherever_its_dashes_stand` leaves out the
"as written" placements, which the older tests already hold.
`test_no_twin_is_asked_unless_an_operator_cuts_the_segment` takes
`DASHED_TWINS`, the non-creating `checkout`s git switches nothing on, and
they stay silent at every position without `&` or `|`. A creation or a
`switch` that git refuses is left out of the twin set on purpose, and asked,
which is the loud direction. `_git_switches` is a hand-written model and is
not run against git in CI. Its 225 agreements were re-measured here, and a
later git that changes `--` handling would not turn it red. That holds for
every generator in the module, so I raise no finding for it.

The fix newly asks two restore spellings that a7ab2a4e and 94d7b2e0 left
silent: `git checkout -p feature/x --` and `git checkout
--pathspec-from-file=list feature/x --` (executed: git restores and switches
nothing). Their spellings without `--` are asked at the base. `spec.md`'s Out
list keeps that ask on purpose (*A ref after `-p`/`--patch` or
`--pathspec-from-file`*, under §*Unknowns resolve conservatively*), so the
fix extends a decision already taken, in the loud direction.

## ⬜ 3 — a test comment still says a `--` takes every name out of a checkout

`tests/test_guard_resolves_the_tree_it_judges.py:1377`.

The comment above the `KINDS` rows reads *"§*Which tree*'s words: a `--`
takes every name out of a checkout"*. Since e3c5101b, §*Which tree* says the
opposite of that for a bare `--`, and the row added two lines below
(`checkout a name and a bare --` → `switch`) contradicts it. Nothing reads
the comment and no behaviour is wrong, so it is ⬜. `bin/survivor-check`
cannot see it because the wording differs from the sentence the range
removed.

## ⬜ 4 — `Corrected · G1`'s evidence does not record the fix pass's red (correction)

`seal/ledger/1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection.md:7`.

The row's claim and its anchors moved with the fix: the claim now names the
bare `--`, and `KINDS` and the pin carry new hashes. Its evidence cell still
describes only phase 2's run (18 `KINDS` rows, 451 passed). It does not say
that the new `KINDS` row and the pin's second assertion were seen red. D1's
row gained a *Corrected* clause for the same fix, and G1's did not. The
claim holds: both were red against a7ab2a4e (executed, above). This is
paperwork, so it is a correction and stays out of `Needs a fix`.

## Regression tests to plant

None. The fix pass's cases cover the class, and I saw them red at a7ab2a4e.

## Facts for the evidence ledger

- git 2.54.0: `git checkout <name> --end-of-options --` and `git checkout
  --end-of-options - --` switch, `git checkout --end-of-options -- <path>`
  restores, and `git checkout -b y -- <name>` is refused (`is not a commit
  and a branch 'y' cannot be created from it`). Executed.
- D1's corpus clause holds at 675ef92a: over the 25,741 pairs, the frozen
  reading's kinds are those of a7ab2a4e, pair for pair, and candidate C fires
  on 0. Executed in round 2.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | round 1's blocking finding is closed — `git checkout <name> --` is read as a switch by `classify` and `switch_kind`, and a `--` followed by a path stays a restore | `hooks/worktree-guard.py:1024`, `hooks/worktree-guard.py:563` | confirmed | Executed: 225 `_dashed` commands under bash with git 2.54.0, none git switches on is silent; 4,512 of 49,804 generated shapes silent with a7ab2a4e's guard, 0 with 675ef92a's; 53 extra `--` placements, none silent through a `--`; the new cases red at a7ab2a4e (11 failed), the module green at 675ef92a (312 passed) |
| 🟢 | round 1's ⬜ 2 is closed — A7 binds the table both ways, and skipping an option git does not list is safe | `tests/test_guard_resolves_the_tree_it_judges.py:1817` | confirmed | Executed: on git 2.54.0 every table key is listed and matched, so the skip skips nothing; doctoring `--guess`, `-q`, `-2`, `--recurse-submodules` and `--track` to take a value turns it red; an option an older git lacks is one git refuses |
| 🟢 | `_git_switches` decides what git does for every `_dashed` placement | `tests/test_guard_resolves_the_tree_it_judges.py:1549` | confirmed | Executed: 0 disagreements with git 2.54.0 over the 225 commands |
| 🟢 | every remaining mismatch a `--` decides is loud | `hooks/worktree-guard.py:1024` | confirmed | Executed: 94 asked commands over the 225 are all refused by git; the extra placements asked where git does nothing are refusals, `checkout HEAD --`, and the `-p`/`--pathspec-from-file` restores that `spec.md`'s Out list keeps asked |
| 🟢 | the corpus clause still holds after the fix: no recorded pair changes kind, and C fires on none | `docs/worktree-guard-spec.md:741` | confirmed | Executed: the same 25,741 pairs, a7ab2a4e against 675ef92a tree-blind, 0 differ; `wider_only_kinds` at 675ef92a fires on 0 |
| 🟢 | the policy sentence, the Known-limits sentence and `switch_kind`'s docstring agree with `switch_kind` | `docs/worktree-guard-spec.md:644`, `docs/worktree-guard-spec.md:753` | confirmed | Read clause by clause; Executed: the pin red with a7ab2a4e's policy, and the Known-limits example judged a switch by the frozen loop |
| 🟢 | the two new survivors.md rows quote the surviving text with grounds | `seal/specs/1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection/survivors.md` | confirmed | Executed: `bin/survivor-check` over the fix range names exactly those two and excuses both |
| ⬜ 3 | a test comment still says a `--` takes every name out of a checkout, two lines above the row that says it does not | `tests/test_guard_resolves_the_tree_it_judges.py:1377` | open | Read; no behaviour depends on it |
| ⬜ 4 | `Corrected · G1`'s evidence cell does not record that the fix pass's new `KINDS` row and pin assertion were seen red (correction) | `seal/ledger/1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection.md:7` | open | Read; the claim holds (executed: both red at a7ab2a4e); paperwork, so out of `Needs a fix` |

## Executed probes

| What was run | Result |
|---|---|
| A deleted probe module: each of the 225 `DASHED` commands under bash with git 2.54.0, one fresh scratch repository each (`main`, `feature/x` one commit ahead, `README.md`, `feature/x` as the previous branch), HEAD's symbolic ref and commit compared before and after, beside `_git_switches`, the frozen loop's `classify` and candidate C | `_git_switches` wrong on 0; silent on a switch 0; asked where git does not switch 94, all exit 128 |
| The same module over 53 further placements (the table in Stage 1 and more) | none silent through a `--`; `checkout :/second` and `checkout :/second --` detach while both readers are silent, the same at 94d7b2e0; `checkout --detach --` detaches at HEAD and moves no file, silent as `checkout --detach` is at the base |
| A deleted count over `DASHED_SWITCHES` through `_shapes`, `is_ref` a lookup over the repository's refs, with 675ef92a's and a7ab2a4e's guard | 49,804 shapes; 0 silent at 675ef92a; 4,512 at a7ab2a4e (3,384 bare `--` after, 1,128 `--end-of-options` and a bare `--`) |
| `bin/test tests/test_guard_resolves_the_tree_it_judges.py -q` with a7ab2a4e's guard in place, then at 675ef92a | 11 failed, 301 passed; then 312 passed |
| The policy pins with a7ab2a4e's `docs/worktree-guard-spec.md` in place | `test_the_guard_policy_says_a_hidden_file_checkout_is_asked` failed, 2 passed |
| `test_the_option_table_binds_the_installed_git` with one table entry doctored to take a value, six entries | 6 of 6 red, each naming the entry; and a parse of both `-h` outputs: every table key listed, every value flag equal |
| A deleted replay of this machine's transcripts before 2026-10-03T11:06:22+09:00, tree-blind, a7ab2a4e's against 675ef92a's `switch_kind` per frozen segment, then `wider_only_kinds` at 675ef92a | 25,741 pairs; 0 differ; C fires on 0 |
| The Known-limits example and six neighbours through the frozen loop and C | `feature/x -- <&1 README.md` judged a switch, as the sentence says; `-- 2>/dev/null README.md` silent; `-->/dev/null`, `-- >/dev/null`, a subshell and a `;` after the `--` all asked |
| `bin/survivor-check --range 58d4b7a5..cd684fb2`, without and with `--exempt` | 2 places, the two rows' quotes; with the exemption, exit 0 |
| `bin/evidence-check --ledger` on this item's ledger fragment | 38 ok, 0 drifted, 0 broken |
| `git checkout README.md --` in a scratch repository with a branch and a file both named `README.md` | switches to the branch, exit 0 |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet run, at any SHA; it is the sealer's, once the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `git checkout :/<message>` detaches HEAD to the newest commit whose message matches, and `classify` reads no switch, because `is_ref` appends `^{commit}` and the `:/` search then takes it as part of the pattern; silent at 94d7b2e0 too and independent of `--` | not this work item's class; a candidate for a new issue against the worktree guard | the orchestrator of release 0.18.2, who files it or drops it |

## Paste-ready fixes

### ⬜ 3

`tests/test_guard_resolves_the_tree_it_judges.py`, the comment above
`"checkout a name before --"`:

```python
    # §*Which tree*'s words: a `--` with a word after it takes every name out
    # of a checkout, and `-B` is a switch with or without one (round 3 of
    # #737).
```

### ⬜ 4

`Corrected · G1`'s evidence cell, appended after its **Read** sentence:

```text
**Executed** 2026-10-04 by round 1's fix pass and again by round 2: the pin's
rewritten sentence and its Known-limits assertion red with `a7ab2a4e`'s
policy text, and the `KINDS` row for a bare `--` red with `a7ab2a4e`'s guard;
green at `675ef92a`.
```

Needs a fix: no

Loses a record or crashes: no

Nothing in this round is open beyond the two ⬜ notes, so the broad gate has
come due. What comes due is the sealer's spawn, once the orchestrator has
recorded this round.

## Proof block

Files opened (at 675ef92a in the clone unless noted):

- `hooks/worktree-guard.py` (`SWITCH_OPTIONS`, `_long_option`, `read_switch_words`, `switch_kind`, `wider_only_kinds`, `_bare_words`, `is_ref`, `classify`)
- `tests/test_guard_resolves_the_tree_it_judges.py` (the fix range's diff; `_redirections`, `RESTORES`, `_placed`, `_shapes`, `KINDS`, `CREATING`, `CREATIONS`, `SWITCHES`, `TWINS`, `_dashed`, `_git_switches`, `DASHED_TWINS`, `_read_apart`, the new tests, `USAGE`, `test_the_option_table_binds_the_installed_git`)
- `tests/conftest.py` (`load_hook_module`, `repo`)
- `docs/worktree-guard-spec.md` (the fix range's diff; §*Which tree*'s #678 paragraph; §*Known limits*' static-table and `&`-cut bullets)
- `seal/ledger/1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection.md` (the fix range's diff)
- this item's `rounds/round-1.md`, `rounds/round-1-report.md`, `survivors.md`, `spec.md` (Out list and acceptance table), `phases/phase-1.md` and `phases/phase-3.md` (the corpus paragraphs)
- `bin/test`, `bin/survivor-check` and `bin/evidence-check` (their headers)
- `hooks/worktree-guard.py` and `docs/worktree-guard-spec.md` at a7ab2a4e, and `hooks/worktree-guard.py` at 94d7b2e0, each put in place in the clone for the comparisons and restored

Carried from round 1, not re-derived: the six 🟢 verdicts round 1 recorded
(the frozen files unchanged, the table being git 2.54.0's, the C-position
property over the older twins, the restore twins' silence, the `--no-`
removal, the four survivor cases). The fix range touches none of the files or
units those verdicts rest on, except `classify` and `switch_kind`. For those
two, the twin and restore sweeps above re-ran the property.
