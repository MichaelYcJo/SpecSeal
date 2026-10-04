# 1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection — review round 2

| Field | Value |
|---|---|
| Target SHA | 675ef92a14cd97d2b638449c83b6410a0ffa7646 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #788 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `64747288749a758ce8565b67a5cb841dc44c5914..7adcc033cc92ffb6af6bb966dd263849f1c0a7dd`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | no |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of #764/#738 (PR #788), the verifying round, at 675ef92a: open round 1's fixes (range 58d4b7a5..cd684fb2) and judge whether each closes its finding with no regression — the bare trailing `--` read as a switch in both readers and the generator's `--` axis with its `_git_switches` truth rule against real git; A7's reverse binding and its skip; the policy, Known-limits, ledger claims and two survivors rows.

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
| ⬜ 3 | a test comment still says a `--` takes every name out of a checkout, two lines above the row that says it does not | `tests/test_guard_resolves_the_tree_it_judges.py:1377` | deferred #790 | #790 — A stale test comment with no behaviour depending on it; #790 changes the same module, so its checklist carries the reviewer's paste-ready wording rather than this run spending its one reopening on a comment; Read; no behaviour depends on it |
| ⬜ 4 | `Corrected · G1`'s evidence cell does not record that the fix pass's new `KINDS` row and pin assertion were seen red (correction) | `seal/ledger/1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection.md:7` | answered | A correction to a record: `Corrected · G1`'s evidence cell now records the red the fix pass and round 2 saw against `a7ab2a4e` (7adcc033).; Read; the claim holds (executed: both red at a7ab2a4e); paperwork, so out of `Needs a fix` |

## Paste-ready fixes

```python
    # §*Which tree*'s words: a `--` with a word after it takes every name out
    # of a checkout, and `-B` is a switch with or without one (round 3 of
    # #737).
```
```text
**Executed** 2026-10-04 by round 1's fix pass and again by round 2: the pin's
rewritten sentence and its Known-limits assertion red with `a7ab2a4e`'s
policy text, and the `KINDS` row for a bare `--` red with `a7ab2a4e`'s guard;
green at `675ef92a`.
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/worktree-guard.py:1022`, `hooks/worktree-guard.py:561`, `docs/worktree-guard-spec.md:644` | round 1's 🔴 1 — fixed |
| round-1 | `tests/test_guard_resolves_the_tree_it_judges.py:1685` | round 1's ⬜ 2 — fixed |
| round-1 | `hooks/cmdline_base.py` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree-guard.py:394` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree-guard.py:568` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree-guard.py:1018` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree-guard.py:466` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_guard_resolves_the_tree_it_judges.py` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `git checkout :/<message>` detaches HEAD to the newest commit whose message matches, and `classify` reads no switch, because `is_ref` appends `^{commit}` and the `:/` search then takes it as part of the pattern; silent at 94d7b2e0 too and independent of `--` | not this work item's class; a candidate for a new issue against the worktree guard | the orchestrator of release 0.18.2, who files it or drops it |
