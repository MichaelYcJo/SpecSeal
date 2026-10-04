# 1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection — review round 1

| Field | Value |
|---|---|
| Target SHA | a7ab2a4eaf32ab7ef85572ec84a56276a618f122 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #788 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `58d4b7a599a9eb8258b6e28d6ee4cb75b697d973..cd684fb2737f1f1e152347eb4f2cf5adef306107`, 3 commits |
| Contract changes | none |
| New units | _dashed (depth 1); _git_switches (depth 1); DASHED (depth 1); DASHED_SWITCHES (depth 1); DASHED_TWINS (depth 1); test_classify_reads_a_switch_wherever_its_dashes_stand (depth 1); test_a_bare_dashdash_names_the_branch_where_a_file_has_its_name (depth 1) |
| Needs a fix | yes — 🔴 1, `git checkout <name> --` read as a restore by `classify` and `switch_kind`, and 48 placements the base asked now silent |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of #764/#738 (PR #788), at a7ab2a4e against `release/v0.18.2` (94d7b2e0): spec compliance first, then quality, in the guard's new word reader, `classify`, `switch_kind` and `_bare_words`. Judge whether the reader reads `checkout`/`switch` words as git's option parser receives them after bash strips redirections, enumerated over carrier word × spelling × redirection placement against real git; whether a restore twin stays silent and the newly-asked shapes are all C positions; that the frozen files are unchanged; the Known-limits additions and counts; and the removed `--no-` rule and the four closed mutation survivors.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | `git checkout <name> --` with nothing after the `--` switches, and `classify` and `switch_kind` read any `--` as a restore; the build newly silences 48 generated shapes the base asked (`-->/dev/null` and its kin) | `hooks/worktree-guard.py:1022`, `hooks/worktree-guard.py:561`, `docs/worktree-guard-spec.md:644` | **fixed** `e3c5101b031663dc670c84a83d85e74bf4dd0cbf` | fixed at e3c5101b031663dc670c84a83d85e74bf4dd0cbf; Executed under bash with git 2.54.0: six trailing-`--` spellings switch while both readers read no kind; the `_placed` sweep counts 460 of 492 silent at the build against 442 and 436 at the base; the fix below turns the four proposed cases from red at a7ab2a4e to green |
| ⬜ 2 | A7 binds the table one way only: a `VALUE` entry git no longer lists as mandatory stays green and eats a name | `tests/test_guard_resolves_the_tree_it_judges.py:1685` | **fixed** `e3c5101b031663dc670c84a83d85e74bf4dd0cbf` | fixed at e3c5101b031663dc670c84a83d85e74bf4dd0cbf; Read; every `VALUE` entry matches git 2.54.0 today (executed), so nothing ships wrong |
| 🟢 | `hooks/cmdline_base.py`, S11 and `hooks/cmdline.py` are unchanged | `hooks/cmdline_base.py` | confirmed | Executed: the diff over the four frozen-side files is empty |
| 🟢 | The option table is git 2.54.0's, hidden options included | `hooks/worktree-guard.py:394` | confirmed | Executed: `--git-completion-helper-all` lists exactly the 22 and 15 long names, and `-h` lists the short letters and value markers |
| 🟢 | Every newly asked no-switch shape stands at a C position | `hooks/worktree-guard.py:568` | confirmed | Executed over the module's 12,092 twin placements: 268 newly asked, none after the subcommand without `&` or a pipe; the 230 figure is the smith's set and is carried |
| 🟢 | A restore twin with a redirection after the subcommand stays silent in `classify` | `hooks/worktree-guard.py:1018` | confirmed | Executed: the sweep and the three `main()` restore cases |
| 🟢 | Dropping the `--no-` rule changes no answer | `hooks/worktree-guard.py:466` | confirmed | Executed: no long name begins with `no-`; `switch -c y --no-create feature/x` switches and is read as a switch |
| 🟢 | The four survivors each have a case that pins the mutated unit | `tests/test_guard_resolves_the_tree_it_judges.py` | confirmed | Read: each case asserts the value its mutant changes; `bin/mutation-check` not re-run |

## Paste-ready fixes

```python
    if sub == "checkout":
        creating, names, after = read_switch_words(sub, args)
        if creating:
            return "create+switch"
        if after:
            return None  # explicit path restore: a pathspec follows `--`
        if "-" in names:
            return "switch"  # previous branch
        if not names:
            return None
        first = names[0]
        # `git checkout <name> --`, nothing after the `--`, names a commit and
        # switches to it: the `--` only says the name is no file.
        if after is None and (
            first == "."
            or os.path.exists(os.path.join(cwd or ".", first))
            or os.path.exists(first)
        ):
            return None  # restoring a file/dir, not switching branch
```
```python
    if creates:
        return "switch"
    if after:
        return None
    if any(n != "." for n in names):
        return "switch"
    return None
```
```text
    branch, in `classify`'s order: one carrying a creating option counts,
    with or without a name; then one with a word after its `--` does not,
    whatever stands before it; then one naming `-` or a word other than `.`
    does, a `--` with nothing after it included.
```
```text
Each side is read by its words alone, as git is handed them: a `switch`
naming a word or `-` or carrying a creating option, a `checkout` carrying a
creating option (`-b`, `-B` or `--orphan`, in any spelling git's option
parser accepts), a `checkout` that names `-` or a word other than `.` and
has no `--` among its words or nothing after its `--`, or a `worktree add`;
an option's value is not a name, and a redirection is no word.
```
```text
A cut after a `--` leaves the frozen reading a `--` with nothing after it, so
`git checkout feature/x -- <&1 README.md`, a restore, is judged a switch to
`feature/x` too.
```
```python
    "checkout a name before --": (["git", "checkout", "x", "--", "f"], None),
    "checkout a name and a bare --": (["git", "checkout", "x", "--"], "switch"),
```
```python
    "switch -- feature/x",
    # A `--` with nothing after it only says the name before it is no file.
    "checkout feature/x --",
    "checkout - --",
```

## Executed probes

| What was run | Result |
|---|---|
| 38 `git checkout` and `git switch` commands under bash 3.2.57 with git 2.54.0, one fresh scratch repository each (branches `main` and `feature/x`, a committed `README.md`, a previous branch), HEAD compared before and after; the build's and the base's `classify` per frozen segment plus `wider_only_kinds` on the same command | Six trailing-`--` spellings switch while both readers read nothing; `checkout feature/x -->/dev/null` switches, the base asks and the build does not; every other switching spelling is asked by the build; `-h`, `-2`, `--quiet=1`, `--c` and `--no-c` are refused by git and asked by the build |
| `git checkout --git-completion-helper-all`, `git switch --git-completion-helper-all`, `git checkout -h`, `git switch -h` against `SWITCH_OPTIONS` | 22 and 15 long names, the table's exactly; no hidden option; value markers match |
| Pattern equality of the guard's `_REDIRECTION` and `hooks/cmdline.py`'s | equal |
| `git diff 94d7b2e0 a7ab2a4e` over `hooks/cmdline_base.py`, `hooks/cmdline.py`, `hooks/worktree_consent.py`, `tests/test_the_frozen_reading_never_grows.py` | empty |
| A deleted probe module through `bin/test`: the module's `TWINS` and `RESTORES` through `_placed`, base guard against build guard, `is_ref` a lookup over the repository's refs; then the trailing-`--` verbs through `_placed` | 12,092 twin placements, 268 newly asked, 0 outside C positions; `checkout feature/x --` 442 silent at base, 460 at build; `checkout - --` 436 and 460; `checkout --conflict=merge feature/x --` 546 and 564 |
| The same, with 🔴 1's fix applied in the clone | trailing-`--` verbs 0 silent of 492, 492 and 596; newly asked twins 294, 0 outside C positions |
| `bin/test tests/test_guard_resolves_the_tree_it_judges.py -q` in the clone with 🔴 1's fix and its cases | 246 passed |
| The same module with the cases and a7ab2a4e's guard | 4 failed (the KINDS row, two `classify` rows, the generated A4 case), 242 passed |
| The broad gate (full suite, repository-wide lint, typecheck) | not yet run, at any SHA; the sealer's, once the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
