# 1790745049 — review round 2 report (verifying)

Target SHA `6a2a87d7`, base `542f920b`, reference `86256492`. Round 1's fix
range `d1e2b9d3..052c6fe8`, plus the two record commits after it. Reviewed in a
`git clone --no-local` at the target SHA. Ran by `specseal:warden`.

## In one view

The frozen reader does what the fix pass says it does. Below its rider it is
`86256492`'s `hooks/cmdline.py` byte for byte, the guard and the consent writer
reach nothing else, and over 10,598 commands of my own the guard's decision,
reason text, judged tree, every segment's directories (POSIX and Windows
tokenizing), recognised kinds and the consent directory equal `86256492`'s with
0 differences. The gate is unchanged, both readers load in one process without
touching each other, and the cost is inside 2 ms. Round 1's five verdicts are
closed.

One thing does not hold, and it is the sentence that states the plan for the
frozen copy:

1. **The policy names `0.17.0`, and a tree-wide case refuses it** (🔴 1). The fix
   pass wrote it at `c5bb0222`; the suite is red on this branch.
2. Four smaller sentences read wrong or less than they should (⬜ 2 to ⬜ 5): a
   cross-reference to the wrong section in the same paragraph, `foreach` missing
   from the listed cost, and test docstrings that still say the guard imports
   `cmdline.py`.

## 🔴 1 — The policy names the next release, so the release-hygiene case fails

`docs/worktree-guard-spec.md:585` reads *"#692, the 0.17.0 redesign, decides
the guard's reading again"*. `docs/` is one of the loaded roots, and
`tests/test_release_hygiene.py::test_no_loaded_file_names_a_version_at_or_above_the_running_one`
refuses any version at or above the running `0.15.7`:

```text
E   docs/worktree-guard-spec.md:585 names 0.17.0
FAILED tests/test_release_hygiene.py::test_no_loaded_file_names_a_version_at_or_above_the_running_one
1 failed, 406 passed
```

Executed at the target. The line came in with `c5bb0222`, inside round 1's fix
range; `git grep 0.17.0` over the loaded roots finds nothing at `542f920b` or at
`d1e2b9d3` and one line at `052c6fe8`. So the branch cannot pass the broad gate,
and the pull request's check fails on it, whichever of the two runs first.

The class (§12): every loaded file naming a version at or above the running
one. The case enumerates it and names this line alone. `hooks/cmdline_base.py:12`
names `0.17.0` too, but `hooks/` is not a loaded root and the rider is deleted by
#692 itself, so it is left out.

## ⬜ 2 — The same paragraph points the reader at the wrong section

`docs/worktree-guard-spec.md:582` sends the reader to *"§A's command-word
groups"*. §A is the branch-switch decision matrix. The two groups (read as git,
and not read as git) are in §*Creation consent*, the paragraph at lines 256–285
that this branch also edited. Read. The fix goes in the same edit as 🔴 1.

## ⬜ 3 — `foreach` is part of the cost and no list names it

The records list the zsh words the guard no longer reads past as `noglob`,
`nocorrect`, `repeat N` and `for i (…)`: `docs/worktree-guard-spec.md:280` and
`:581`, the changelog's line 24, M2, and spec S5. `hooks/cmdline.py:1563` reads
`foreach` as well, and the guard at `542f920b` read it.

Executed: `cd w && foreach i (1) git worktree add ../wt k; end` was `deny`,
judged in the session's tree, at `542f920b`, and is `silent` at `86256492` and
here. The behaviour is the base's, so nothing needs to change in code. Only the
list is short, which is the same shape as round 1's 🟡 2 ("the recognition list
names one shape of five"). The changelog's first sentence, *what #674 taught the
commit gate to read is not read here*, stays true.

A second corpus of 237 commands, the header, subshell, string and runner shapes
#674 added, measured the whole cost against `542f920b`: 30 commands differ, and
every one is a redirection in front of a `cd` or a git (`watch` included), a
zsh prefix, or `foreach`. No glued subshell, compound header, case arm, function
body or coprocess changed the guard's answer.

## ⬜ 4 — The shared-module case proves the union, and its first sentence is false

`tests/test_a_gate_that_fails_says_so.py:302` opens with *"`cmdline.py` is
imported by two `pre-bash` gates and two `post-bash` gates"*. Since #689 it is
imported by one of each. The appended *Changed by #689* paragraph explains the
change but leaves that sentence standing.

What the case still proves, and what it no longer does:

- **Still proved.** Every gate that imports a broken shared reader is named,
  once, and the four names are the right four.
- **No longer proved.** *"With no gate that does not import it"* per module.
  Both readers are broken at once, so a guard that went back to importing
  `cmdline.py` would still be named and the case would stay green. The guard-tree
  module's behavioural cases do catch that regression (M1's mutants), so this is
  a lost pin and not a lost check.
- **Keeping it.** Parametrise over the two readers. I ran the three partitions
  with a deleted probe (`tests/test_tmp_s6_split.py`, NAME NOT IN TREE):
  `cmdline.py` alone names the commit gate and `implementer-notice.py`;
  `cmdline_base.py` alone names the guard and `worktree_consent.py`, and the
  commit gate still decides because its import of `worktree_consent` is guarded.

The second case, `test_a_gate_that_fails_to_load_names_every_group_that_loads_it`,
proves what it proved: the load failure it asserts is the guard's and the
consent writer's own file, now reached through `cmdline_base.py`.

## ⬜ 5 — Three test modules still say the guard imports `cmdline`

`tests/test_what_the_reader_understands.py:791` says *"the guard reaches its
reader with a plain `import cmdline`"*. The import is now
`import cmdline_base as cmdline`, and the reasoning around it still holds.
`tests/test_a_commit_behind_a_reserved_word_is_judged.py:37`,
`tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py:38` and
`tests/test_no_shape_the_base_stops_reads_silent.py:43` comment their
`import cmdline` as *"the plain name both gates import"*. Read. None of the three
compares a guard answer with `cmdline.Unresolved`, so no case passes for the
wrong reason. Only the comments are stale.

## What the prompt asked, answered

1. **The frozen copy.** The shebang plus everything below the 18 rider lines
   equals `git show 86256492:hooks/cmdline.py` byte for byte. Executed, compared
   as bytes.
2. **Every symbol from the copy.** The guard's attribute uses (`adds_a_worktree`,
   `drop_comments`, `drop_heredoc_bodies`, `parse_git`,
   `split_segments_with_separators`, `understood`, `Unresolved`,
   `walk_directories`) and the consent writer's (the same plus `apply_chdir`)
   all resolve on `cmdline_base`. Neither imports another module that imports
   `cmdline`: `console` and `optin` import nothing of the kind. Read. In one
   process loaded the way `dispatch.py` loads them, commit gate first, the guard's
   reader, its `parse_git` and `apply_chdir`, and the consent writer's reader are
   `cmdline_base`; the gate's walk is `cmdline`'s; the two `Unresolved` classes
   are distinct objects; the gate and the guard share one `worktree_consent`.
   The guard's 10,361 answers in that process equal its answers alone. Executed.
3. **Decision-level equality.** 0 differences in decision, reason, judged tree,
   each segment's directories, directories under the Windows tokenizing,
   recognised kinds and consent directory, over 10,361 commands (7,485 silent,
   2,558 denied, 318 asked at `86256492`; 2,053 with a consent directory) and 237
   more. I did not re-count the build's 43,544; mine is an independent corpus
   that carries round 1's shapes (`WIDER_FIRST`, the zsh prefixes, the round-3
   chain, `cd>/dev/null`), heredocs, CR/LF, tabs, `eval`, strings, functions,
   `case`, `coproc`, `watch`, the walk's cap and two-head products.
4. **The gate.** `git diff 542f920b -- hooks/cmdline.py hooks/commit-review-gate.py`
   is empty, and the gate's output over the same 10,361 commands (579 denied)
   equals `542f920b`'s. The gate now loads `cmdline_base.py` through
   `worktree_consent`, which M4 records. Executed.
5. **Round 1's five verdicts.** Closed; see the verdict table.
6. **The failing-gate cases.** ⬜ 4.
7. **Cost.** Interleaved, twelve runs each, median, the guard alone:
   `ls` 31.9 / 30.9 ms, `cd w && git switch` 508.9 / 511.3 ms, `git worktree add`
   480.9 / 476.8 ms (`542f920b` / target). `dispatch.py pre-bash` differs by 0.1
   to 1.7 ms, and the commit gate alone by 0.1 to 0.6 ms. A first, sequential
   pass read 18 ms for the base sets against 31 ms for the target. The
   interleaved rerun did not reproduce that gap, so it is discarded as an artifact
   of ordering.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The policy names `0.17.0`, so the loaded-file version case fails and the suite is red | `docs/worktree-guard-spec.md:585` | open | Executed: 1 failed, 406 passed in the hygiene module; written at `c5bb0222` in round 1's fix range |
| ⬜ 2 | The cost paragraph cites §A for the command-word groups, which are in §Creation consent | `docs/worktree-guard-spec.md:582` | open | Read |
| ⬜ 3 | `foreach` is part of the guard's cost and no list names it | `docs/worktree-guard-spec.md:581` | open | Executed: `deny` at `542f920b`, `silent` at `86256492` and here |
| ⬜ 4 | The shared-module case breaks both readers at once, so the per-module "no gate that does not import it" is no longer pinned, and its first sentence is false | `tests/test_a_gate_that_fails_says_so.py:302` | open | Executed: each reader broken alone names exactly its two importers |
| ⬜ 5 | Three test modules and one docstring still say the guard imports `cmdline` | `tests/test_what_the_reader_understands.py:791` | open | Read; no assertion depends on it |
| 🟢 | round 1's blocking finding is closed — a segment only #674 reads as git no longer takes the first slot | `hooks/worktree-guard.py#walk_command` | confirmed | Executed: 0 differences against `86256492` over 10,598 commands, `WIDER_FIRST` and its consent twin included |
| 🟢 | round 1's 🟡 2 is closed — zsh-prefixed segments get the base's answer | `hooks/cmdline_base.py#walk_directories` | confirmed | Executed: the same corpus, all four prefixes as heads and tails |
| 🟢 | round 1's ⬜ 3 is closed — the policy says the whole command is read the base's way, which the import makes true | `docs/worktree-guard-spec.md:560` | confirmed | Read, and the differential |
| 🟢 | round 1's ⬜ 4 is closed — the changelog opens the cost as a cost | `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/changelog.md:20` | confirmed | Read |
| 🟢 | round 1's ⬜ 5 is closed — M3 is withdrawn with a dated correction | `seal/ledger/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order.md` | confirmed | Read |
| 🟢 | The frozen copy equals `86256492:hooks/cmdline.py` below its rider | `hooks/cmdline_base.py` | confirmed | Executed, byte comparison |
| 🟢 | Both readers load in one process without cross-talk | `hooks/dispatch.py#run_gate` | confirmed | Executed: module identities and 10,361 guard answers in one process |
| 🟢 | The commit gate is unchanged against `542f920b` | `hooks/commit-review-gate.py` | confirmed | Executed: empty diff, 0 of 10,361 gate outputs differ |
| 🟢 | The records name the frozen reader: M1–M4, S3/S5–S7, both policies, I's and E's corrections | `seal/ledger/` | confirmed | Read; `evidence-check` 0 drifted, 0 broken, 0 refused |
| 🟢 | Two readers cost under 2 ms per hook call | `hooks/worktree-guard.py` | confirmed | Executed, interleaved medians |
| ❓ | The guard's Windows backslash doubling on a Windows machine | `hooks/worktree-guard.py#_tokenize_with_separators` | ❓ out of verified scope | Carried from round 1. On macOS the `windows=True` walk equals `86256492`'s for every command, but `ntpath` and a real Windows shell were not run; the repository owner answers it on a Windows machine |

## Paste-ready fixes

🔴 1 and ⬜ 2 together, `docs/worktree-guard-spec.md` lines 581–586 (⬜ 3's
`foreach` is folded in on the first line):

```text
redirection or behind zsh's `noglob`, `nocorrect`, `repeat N`, `for i (…)` or
`foreach i (…)` is not git to this guard, so it says nothing there
(§*Creation consent*'s command-word groups). Round 2 of work item 1790660768
made the guard read the first and #674 the second, and #689 took both back as
the accepted cost. The commit gate still reads both. #692, the redesign of how
the gates learn where a command acts, decides the guard's reading again, and
deletes the frozen copy.
```

⬜ 3, the other lists. `docs/worktree-guard-spec.md:280`, the changelog's
line 24, M2 and spec S5 each change the same phrase:

```text
zsh's `noglob`, `nocorrect`, `repeat N`, `for i (…)` or `foreach i (…)`
```

⬜ 4, `tests/test_a_gate_that_fails_says_so.py`. The per-module lists are the
executed partition. The count line for two gates was not run and follows the
four-gate wording:

```python
@pytest.mark.parametrize(
    "broken, named",
    [
        ({"cmdline.py": BROKEN}, ["commit-review-gate.py", "implementer-notice.py"]),
        ({"cmdline_base.py": BROKEN}, ["worktree-guard.py", "worktree_consent.py"]),
        (
            {"cmdline.py": BROKEN, "cmdline_base.py": BROKEN},
            [
                "commit-review-gate.py",
                "worktree-guard.py",
                "implementer-notice.py",
                "worktree_consent.py",
            ],
        ),
    ],
    ids=["cmdline", "cmdline_base", "both"],
)
def test_a_broken_shared_module_names_every_gate_that_imports_it(
    repo, tmp_path, broken, named
):
    """S6. A broken shared reader names every gate that imports it, once, and
    no gate that does not. `cmdline.py` is imported by the commit gate and
    `implementer-notice.py`; since #689 `cmdline_base.py`, the reader frozen at
    `86256492`, is imported by the worktree guard and `worktree_consent.py`. The
    commit gate's own import of `worktree_consent` is guarded, so a broken
    `cmdline_base.py` does not name it. The `post-bash` call is not a commit: a
    copy of `hooks/` has no `skills/` beside it, so `evidence-advisor.py` would
    fail at run on a commit for want of its checker, which is the fixture and
    not the reader."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, broken)
    dispatch(hooks, "pre-bash", bash(repo, "s-x"))
    dispatch(
        hooks,
        "post-bash",
        bash(repo, "s-x", command="ls", hook_event_name="PostToolUse"),
    )
    for path in (repo / ".git" / RECORDS / "s-x").iterdir():
        os.utime(path, ns=(10**18, 10**18))
    lines = said(stop(hooks, repo, "s-x"))
    assert lines[0] == f"SpecSeal: {len(named)} gates failed and were skipped", lines
    assert gates_said(lines) == named, lines
    assert lines[-1] == CLOSING
```

⬜ 5, the comment in the three modules and the docstring sentence:

```python
import cmdline  # noqa: E402  -- the plain name the commit gate imports
```

```text
    `wg.cmdline` rather than the `reader` above: the guard reaches its reader
    with a plain `import cmdline_base as cmdline`, which goes through
    `sys.modules`, while
```

## Executed probes

| What was run | Result |
|---|---|
| The frozen copy against `git show 86256492:hooks/cmdline.py`, as bytes | Equal below the 18 rider lines |
| `git diff 542f920b..6a2a87d7 -- hooks/cmdline.py hooks/commit-review-gate.py` | Empty |
| Differential over 10,361 generated commands, each hook set in its own process on a fresh copy of one fixture, the guard's `main()` with `sessions_in_tree` reporting a session active in `w` alone, a new session id per command | Target against `86256492`: 0 differences in decision, reason, judged tree, walk, Windows-mode walk, kinds and consent directory; no exceptions on either side |
| The same commands with the commit gate loaded first in the guard's process, as `dispatch.py` does | Guard answers equal the guard alone; module identities as in item 2; gate output equal to `542f920b`'s for all 10,361 (579 denied) |
| A second corpus of 237 header, subshell, string and runner shapes at `86256492`, `542f920b` and the target | Target against `86256492`: 0 differences. Against `542f920b`: 30 decision or tree differences, all of them redirection, zsh prefix or `foreach` |
| A deleted probe breaking `cmdline.py`, `cmdline_base.py` and both, through `dispatch.py` and the stop report | Commit gate and `implementer-notice.py`; guard and `worktree_consent.py`; all four |
| `bin/test` on the guard-tree, failing-gate, reader-understands, rider, no-real-identifiers and no-shape modules | 305 passed, exit 0 |
| `bin/test` on the eleven other modules that load the guard or the consent writer, `tests/test_dispatch.py` included | 1107 passed, 1 skipped, exit 0 |
| `bin/test` on eight tree-scanning modules the new file and text joined (hygiene, interpreter, release watch, old roots, survivors, one word, rule owners, merge corrections) | 1 failed, 406 passed, exit 1: 🔴 1 |
| `bin/evidence-check`; `bin/correction-check --range 542f920b...HEAD` | 0 drifted, 0 broken, 0 refused, exit 0; no merge commit in the range, exit 0 |
| Hook time, interleaved, twelve runs each after one warm-up, three hook sets | Differences of 0.1 to 1.7 ms; see item 7 |
| Broad gate: full suite, repository-wide lint and typecheck | not yet — nothing has run it on this branch; it comes due with the sealer's spawn once 🔴 1 is fixed and a round passes |

```text
session/        git init, no commits (clean)
session/w/      copy of a one-commit repository with branch feature/x; f.txt modified; seal/ present
session/clean/  the same copy, unmodified
O/              the same copy, outside the session
nosuch          never created
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the guard should read zsh-prefixed and redirected segments rather than leave them to the user's settings | already deferred in round 1 to #692, the owner's redesign of how the gates learn where a command acts | the repository owner |

## Regression tests to plant

- ⬜ 4's parametrised case, in `tests/test_a_gate_that_fails_says_so.py`. It
  replaces the current S6. Seen red: none of the three rows was run as a case.
  The partition itself was executed through the deleted probe, and reverting the
  guard's import to `cmdline` would be the red to show.

## Facts for the evidence ledger

- The guard and the consent writer's answers equal `86256492`'s over an
  independent 10,598-command corpus, POSIX and Windows walks included (M1's
  claim, measured again, not by the build's script).
- At `542f920b` the guard read past `foreach`, and here it does not (M2's list).

## How this round was scoped

Verifying round: the target was the fix range and the two record commits after
it. `hooks/cmdline_base.py`, the round's new unit, was judged as code. I ran no
full suite, lint or typecheck (§2). The test modules I ran are those that load
the changed files and those that scan every loaded file, which the new
paragraph joined; that is how 🔴 1 surfaced before the broad gate.

Needs a fix: yes — 🔴 1, `docs/worktree-guard-spec.md:585` names `0.17.0` and the release-hygiene case fails

Loses a record or crashes: no

## Proof block

Opened: `hooks/cmdline_base.py`, `hooks/cmdline.py` (symbols, line 1563),
`hooks/worktree-guard.py` (imports, `walk_command`, `classify`, `main`, the
choice record), `hooks/worktree_consent.py` (imports, `creation_directory`),
`hooks/commit-review-gate.py` (imports, `main`, the press reader),
`hooks/dispatch.py` (`GROUPS`, `run_gate`), `docs/worktree-guard-spec.md`,
`docs/commit-review-gate-spec.md` (diff), `tests/test_a_gate_that_fails_says_so.py`,
`tests/test_guard_resolves_the_tree_it_judges.py`,
`tests/test_what_the_reader_understands.py`, `tests/test_release_hygiene.py`,
`tests/test_no_shape_the_base_stops_reads_silent.py`, the work item's
`overview.md`, `spec.md`, `survivors.md`, `changelog.md`, `rounds/round-1.md`,
its ledger fragment, and the diffs of 1790660768's and 1790644505's fragments and
changelogs and 1790635415's fragment.
