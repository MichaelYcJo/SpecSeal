# Round 2 report — 1790550712-the-worktree-guard-judges-a-switch-after-a-creation

| Field | Value |
|---|---|
| Round | 2 (verifying) |
| Target SHA | fe24f07e64353516a56888799e022587ec17159b |
| Target | the fix range `537ee120df98a2346d99b2db53b6d2d08dd2d15e..b8c2adcf55ab53a1e82956dd29cc13a194bba99b` (16125e7, b8c2adc), not the branch |
| Base | origin/release/v0.15.6; the comparison side for row 3 is 537ee12 |
| Reviewed by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` at the target under the session scratchpad, with 537ee12's `hooks/worktree-guard.py` beside it for comparison; all removed |

## Summary

Round 1's finding 1 is closed for the decision and for the listing. Row 3
now asks about the tree the switch acts on, from every shape I ran it
through, and no deny moved. The case the fix added turns red when either
argument goes back to `cwd`.

The fix did not close it as a class, though. Row 3 produces two things
besides the decision: a force-staged check and a set of cleanup commands.
Both work with paths that `git status --porcelain` gives relative to the
tree's root. The fix moved both of them to the switch's directory, which is
neither the root nor the place the commands run from.

- 🟡 1: the cleanup commands still run wherever the shell is standing. For a
  `-C` or `cd` switch into another repository they now act on the session's
  own tree, although the note above them describes the other tree.
  Executed.
- 🟡 2: when the switch goes through a subdirectory, the force-staged check
  now asks about the wrong path. The base named the file and the target
  does not. This is a regression introduced by the fix. Executed.

Round 1's finding 2 is closed for the two words it named. The replacement
sentence explains their placement with a mechanism that execution shows is
false, and a third word the sentence does not name falls in the group it
predicts wrongly (⬜ 3). The new ledger row W9 cites figures from a probe that
is not in the tree, which is the defect this work item corrected in a
`0.9.1` row (⬜ 4).

The `main` stamp re-stamp in `plan.md` is not a `plan.md` row. With the old
stamp, `evidence-check --strict` exits 2 (🟢).

## Findings

### 🟡 1 — The cleanup commands in the phantom note act on the shell's tree, not the tree the note describes

`hooks/worktree-guard.py:2329` now computes the phantom list from `eff_cwd`.
`:2334` still prints `git restore --staged <path>`, and `:2338` still prints
`git restore <path>`, with no `-C`. Before the fix, the note and its
commands both concerned `cwd`. After the fix, the note describes the
switch's tree and the commands act wherever the shell stands.

**Executed.** The session tree A and a clone B each had `ign.txt`
force-staged. For `git -C <B> switch feature/x` from A, the target asks and
prints `git restore --staged ign.txt`. When that line ran in A, the session's
directory, it unstaged A's `ign.txt`, and B's stayed staged. From a
directory that is not a repository, the same line fails.

This matters because the note says *These commands clean the tree*. A model
that follows the note changes the index of a tree nobody asked about. The
`git restore <path>` advice is worse: it overwrites the working copy of
that path in whichever tree the shell is in. No case pins either line.
Every path in the listing comes from porcelain and is relative to the
tree's root, so naming the root with `-C` makes the command correct from
every shell position. The subdirectory case below is one of those
positions.

### 🟡 2 — Reached through a subdirectory, the force-staged check asks about the wrong path

`hooks/worktree-guard.py:2329` passes `eff_cwd` to `phantom_entries`, and
that function runs `git check-ignore -q --no-index <path>` there. Porcelain
v1 gives paths relative to the root, and `check-ignore` reads a path relative
to the directory it runs in. When `eff_cwd` is a subdirectory, the check
asks about `sub/ign.txt` instead of `ign.txt`.

**Executed**, with `/ign.txt` in `.gitignore` and `ign.txt` force-staged at
the root. A subdirectory run of porcelain printed `A  ign.txt`, relative to
the root.

| Command, session at the root | 537ee12 | fe24f07 |
|---|---|---|
| `git switch feature/x` | named | named |
| `cd <A>/sub && git switch feature/x` | named | **not named** |
| `git -C <A>/sub switch feature/x` | named | **not named** |
| `git switch feature/x`, session in `sub` | not named | not named |

The fix caused rows 2 and 3. At the base, a session sitting in a
subdirectory already missed the path, and the same one-word fix closes that
too: `top` is the root of the tree `eff_cwd` is in, and it is already
computed above the row. An unanchored pattern such as `ign.txt` hides the
defect, because it also matches `sub/ign.txt`. That is the pattern the new
case uses, and it is why the case passes. The ask itself still fires in
every row. What goes missing is the note and the commands that clean up the
path.

### ⬜ 3 — The replacement text states the wrong reason, and `$HOME/git` falls into the group it predicts wrongly

`docs/worktree-guard-spec.md:258-262` defines the silent group as *an
expansion the lexer leaves unexpanded (`$GIT`, `gi*`, a command
substitution)*. It then says `~/git` and `*/git` *are paths once expanded*.
The test comment at `tests/test_the_guard_asks_once_per_session.py:389`
says the same thing in stronger terms: they *expand to paths before
`parse_git` reads them*.

**Executed.** The lexer hands back `~/git`, `*/git` and `$HOME/git` without
expanding them, exactly as it does `$GIT`. `parse_git` reads all three as git
because `hooks/cmdline.py:1830` compares `os.path.basename(tokens[i])`, and
the unexpanded word's last component is already `git`. Without a record, all
three deny, while `$GIT`, `gi*` and `$(which git)` are silent.

So the rule as written puts all three in the silent group, and the next
sentence moves two of them out for a reason that is not what happens.
`$HOME/git` is named nowhere, and a reader following the rule predicts
silence where the guard denies. The error is on the cautious side, since a
wrong deny costs a prompt. The members the case pins are placed correctly,
which is why this is ⬜. Round 1's finding 2 is therefore closed for its two
instances and not for its class.

### ⬜ 4 — W9 cites figures from a probe that is not in the tree

`seal/ledger/1790550712-the-worktree-guard-judges-a-switch-after-a-creation.md`
W9 states *a 3,168-cell comparison against `537ee12`: 141 cells silent → ask,
45 ask → silent*. No committed file produces those numbers. This work item
corrected the 0.9.1 row *Whatever the writer would record for …* for exactly
this: counts *from a probe whose shapes were never in the tree*, replaced by
the committed case that reproduces the property.

I reproduced the property on a grid of my own. I did not reproduce the
counts (see the probes). W9's claim that the force-staged check reads *the
tree the switch acts on* also has to follow 🟡 2's fix, which makes it read
the tree's root. A paperwork correction: it stays out of `Needs a fix`.

## Answers to what the prompt asked

- **Other `cwd` reads in the switch ladder.** Read, lines 2051 to 2370.
  `sessions_in_tree`, `fmt_snippet`, the steer text and the choice sites all
  read `top`, which comes from `eff_cwd`. `judge_creation` takes `cwd` only as
  the directory to parse the command from, and it takes the creation's own
  repository as `top`. That is correct and unchanged. What remains is the
  pair above: the note's commands (🟡 1) and the directory used for the
  root-relative paths (🟡 2). The listing prints porcelain's root-relative
  paths and does not say which tree they belong to. 🟡 1's fix adds that as
  a side effect.
- **What `eff_cwd` is per shape.** Executed, with the session at A and
  `sessions_in_tree` recording the `top` it was given:
  - `cd <B> && git switch`: B.
  - `git -C <t> -C B switch`: B, because each `-C` is joined to the one
    before it.
  - `cd <t> && git -C B switch`: B, the relative `-C` resolved from the `cd`.
  - `git -C <nonrepo> switch`: none. Silent at `if not top`, because git
    refuses the command itself.
  - `cd <nonrepo> ; git switch` and `cd /no/such/dir ; git switch`: A, the
    fallback.
  - `cd <A>/sub` and `-C <A>/sub`: `top` A, `eff_cwd` `A/sub`. This is the
    shape behind 🟡 2.
  - A creation-only command never reaches row 3, which exits at
    `reason == "worktree-add"`. Where there is a creation and a switch,
    `eff_cwd` is the switch's directory, not the creation's.
  - `git worktree add <new> … && git -C <new> switch`: `eff_cwd` is `<new>`,
    which does not exist yet. The creation is judged, it denies, and row 3 is
    not reached.
  - `… && cd <new> && git switch`: falls back to A, which is W7.
- **Direction.** Executed on 168 cells: three session directories (A, A/sub,
  outside), four dirty states of A and B, and 14 shapes, including
  `checkout`, both creation orders and `[shared-tree-ok]`. 32 cells moved
  silent → ask, 12 moved ask → silent, and nothing else moved. No deny
  moved. Every ask → silent cell is A dirty and B clean, with a switch into B
  from A or A/sub. Every silent → ask cell has a dirty target. None of the
  cells is a dirty target going quiet. The 141 and 45 are not reproduced (⬜
  4).
- **The spec's sentences.** In §*Which tree*, *every row of §A — the
  tracked-changes row included* is true for the decision and the listing:
  executed, and pinned by the new case, which the section does not cite.
  It is not true for the row's own commands (🟡 1). The `~/git` and `*/git`
  text is covered in ⬜ 3.
- **The `plan.md` stamp.** The rule at `skills/implement/SKILL.md:553`
  forbids a *`plan.md` row*. Its reason is that `round_record.py close` makes
  the round record the fix pass's record, and its neighbour at `:440` makes
  the Phases table the task list. The fix pass added no row to the Phases
  table and no progress. It moved an existing coordinate in the anchor table
  (`plan.md:231`) and added a two-line paragraph (`plan.md:251`) saying why.
  Executed: with the old stamp put back, `bin/evidence-check . --strict`
  exits 2 on `DRIFTED plan.md:231`. The other reading of the rule would
  leave the checker red. Keeping an existing coordinate true is not writing
  a row, which is the same line CLAUDE.md draws for the ledger.

## Regression tests to plant

Both go in `tests/test_guard_resolves_the_tree_it_judges.py`. The fences
under 🟡 1 and 🟡 2 below hold them.

- 🟡 1: three new asserts in the existing case, after its two assertions
  about the force-staged path. With the target's code they fail, because the
  printed command is the one with no `-C`. The fix pass should show that red
  before applying the fix.
- 🟡 2: a new case with three cells and an anchored pattern. Probe 2 showed
  the target naming nothing in all three shapes, so all three are expected
  red before the fix. Probe 2 is an equivalent of the case and not the case
  itself. The fix pass should show the case red before applying the fix.

## Facts for the evidence ledger

- W9 needs correcting once 🟡 2 is fixed: the force-staged check reads the
  root of the switch's tree. The 3,168 / 141 / 45 figures should be replaced
  by the committed case (⬜ 4).
- 🟡 1's fix is a new claim: the commands in the note name the tree's root
  with `-C`. It should go in a new row in the fragment, with 🟡 1's case as
  its evidence.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The phantom note's `git restore` commands carry no `-C`, so after the fix they act on the shell's tree while the note describes the switch's tree | `hooks/worktree-guard.py:2334` | open | Executed: for `git -C <B> switch` from A, the printed hint run in A unstaged A's `ign.txt` and left B's staged. Before the fix, the note and its commands concerned the same directory. No case pins either line |
| 🟡 2 | Reached through a subdirectory, the force-staged check runs `check-ignore` in that subdirectory with root-relative paths and misses the path | `hooks/worktree-guard.py:2329` | open | Executed: with an anchored `/ign.txt`, `cd <A>/sub && git switch` and `git -C <A>/sub switch` from the root named it at 537ee12 and do not at fe24f07. The session-in-`sub` shape misses it at both, and the same fix closes it |
| ⬜ 3 | The replacement text puts `~/git` and `*/git` in the first group because they are *paths once expanded*. The lexer expands neither, `parse_git` compares the unexpanded basename, and `$HOME/git` falls in the group the rule predicts wrongly | `docs/worktree-guard-spec.md:258` | open | Executed: all three tokens come back unexpanded, and `parse_git` reads each as git, so each denies without a record. The test comment at `tests/test_the_guard_asks_once_per_session.py:389` states the same false mechanism |
| ⬜ 4 | W9 cites 3,168 / 141 / 45 from a probe that is not in the tree, and its force-staged clause has to follow finding 2's fix | `seal/ledger/1790550712-the-worktree-guard-judges-a-switch-after-a-creation.md:11` | open | The same defect this work item corrected in the 0.9.1 row *Whatever the writer would record for …*. The direction property is reproduced on my own 168 cells and the counts are not. A paperwork correction |
| 🟢 | round 1's finding 1 is closed for the decision and the listing — row 3 asks about the tree the switch acts on | `hooks/worktree-guard.py:2325` | confirmed | Executed: 12 shapes and 168 cells. No deny moved, and every ask → silent cell is a dirty session tree switching into a clean target. M16 (listing back to `cwd`) turned the new case alone red across the four guard modules; M17 (force-staged check back to `cwd`) turned the new case red. The class is not closed; see findings 1 and 2 |
| 🟢 | round 1's finding 2 is closed for the two words it named — `~/git` and `*/git` sit in the no-record deny group | `tests/test_the_guard_asks_once_per_session.py:397` | confirmed | Executed: both deny without a record, and the case pins both. The stated mechanism is ⬜ 3 |
| 🟢 | The new unit `test_the_dirty_tree_row_reads_the_tree_the_switch_is_in` is sound for what it covers | `tests/test_guard_resolves_the_tree_it_judges.py:513` | confirmed | Read and executed: the fourth cell restores the session tree to the template's `f.txt` content, so it is clean there, and each of the four cells differs at 537ee12 in my sweep. It has no subdirectory cell and no anchored pattern, which is why finding 2 passes it |
| 🟢 | The fix pass's `plan.md` edit re-stamps an existing anchor and writes no row | `seal/specs/1790550712-the-worktree-guard-judges-a-switch-after-a-creation/plan.md:231` | confirmed | Executed: with the old stamp, `evidence-check --strict` exits 2 (`DRIFTED plan.md:231`). The rule at `skills/implement/SKILL.md:553` concerns rows, and the Phases table is untouched |

## Paste-ready fixes

### 🟡 1

```python
        if phantoms:
            why = "\n".join(f"    {p} — {r}" for p, r in phantoms)
            # Porcelain names each path from the tree's root, and the shell
            # may stand anywhere: in another repository for `git -C <repo>
            # switch`, or in a subdirectory. Naming the root is what makes the
            # command act on the tree this note describes.
            at = shlex.quote(top)
            fixes = "\n".join(
                f"    git -C {at} restore --staged {shlex.quote(p)}" for p, _ in phantoms
            )
            note = tr(
                f"\nIndex-only residue invisible in the working tree:\n{why}\n"
                f"These commands clean the tree (run `git -C {at} restore <path>` "
                f"first to keep index-only content):\n{fixes}\n",
                f"\n이 중 워크트리에서는 보이지 않는 index 잔재:\n{why}\n"
                f"아래 명령으로 정리하면 트리가 clean이 됩니다 "
                f"(index에만 존재하는 내용을 살리려면 `git -C {at} restore <path>` "
                f"를 먼저 실행):\n{fixes}\n",
            )
```

```python
        # In test_the_dirty_tree_row_reads_the_tree_the_switch_is_in, inside the
        # loop, after `assert "gitignored path force-staged" in reason, reason`
        # (add `import shlex` at the top of the module):
        hint = [l.strip() for l in reason.splitlines() if "restore --staged" in l]
        assert hint and hint[0].startswith("git -C "), hint
        assert os.path.samefile(shlex.split(hint[0])[2], repo), hint
```

### 🟡 2

```python
        phantoms = phantom_entries(entries, top)
```

```python
def test_the_force_staged_check_reads_from_the_root_of_the_tree(
    monkeypatch, capsys, repo
):
    """Round 2 of work item 1790550712, finding 2. `git status --porcelain`
    names paths from the root of the tree, and `git check-ignore` reads a path
    from where it runs. Reached through a subdirectory, the check asked about
    `sub/ign.txt`, and an anchored pattern named nothing."""
    (repo / "sub").mkdir()
    (repo / ".gitignore").write_text("/ign.txt\n")
    (repo / "ign.txt").write_text("x\n")
    subprocess.run(
        ["git", "-C", str(repo), "add", "-f", "ign.txt"],
        check=True,
        capture_output=True,
    )
    for command, cwd in (
        (f"cd {repo / 'sub'} && git switch feature/x", repo),
        (f"git -C {repo / 'sub'} switch feature/x", repo),
        ("git switch feature/x", repo / "sub"),
    ):
        decision, reason, _ = run(monkeypatch, capsys, command, cwd)
        assert decision == "ask", (command, decision, reason)
        assert "gitignored path force-staged" in reason, (command, reason)
```

### ⬜ 3

```markdown
like any other. One it does not read as git — a command word whose last path
component, as written and before the shell expands anything, is not `git`
(`$GIT`, `gi*`, a command substitution, a different case, a trailing slash),
or a wrapper it does not read past such as `nice` — is not a git invocation to
this guard, and it says nothing. `parse_git` expands nothing and compares that
last component, so `~/git`, `*/git` and `$HOME/git` belong to the first group.
```

```python
    # `parse_git` compares the command word's last path component as written,
    # before any expansion, so `~/git`, `*/git` and `$HOME/git` sit here and
    # not with `$GIT` below (round 1 finding 2, round 2 finding 3).
    ("none", "deny"): (
        "git",
        "/usr/bin/git",
        "sudo git",
        "VAR=1 git",
        "~/git",
        "*/git",
        "$HOME/git",
    ),
```

### ⬜ 4

```markdown
Reverting either argument to `cwd` (M16 the listing, M17 the force-staged check) turned this case red. What moved against `537ee12` is what the case's four cells hold: a dirty target reached from elsewhere now asks and names its own changes, a clean target switched from a dirty shell tree is now silent, and no deny moved
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on `tests/test_guard_resolves_the_tree_it_judges.py` and `tests/test_the_guard_asks_once_per_session.py`, at the target | 99 passed, exit 0 |
| M16, the listing back to `tracked_changes(cwd)`, over the four guard modules | exit 1; 1 failed (the new case), 201 passed, 1 skipped |
| M17, the force-staged check back to `phantom_entries(entries, cwd)`, on the new case alone | exit 1, at the force-staged assertion; not run over the other modules |
| `bin/evidence-check . --strict` at the target | exit 0, 0 drifted |
| The same, with `plan.md:231` put back to `main@cf55137d` | exit 2, `DRIFTED plan.md:231` |
| The tree judged for each of 12 shapes, session at A | as listed under *What `eff_cwd` is per shape* |
| Direction sweep, 537ee12 against fe24f07, 168 cells | 32 silent → ask, 12 ask → silent, nothing else moved; every ask → silent is A dirty, B clean, switch into B |
| The phantom hint for `git -C <B> switch` from A, run in A | A's `ign.txt` unstaged, B's still staged |
| Anchored `/ign.txt`, four subdirectory shapes, at both SHAs | named at 537ee12 for `cd sub` and `-C sub`; named at neither for a session in `sub`; not named at fe24f07 in any of the three |
| Lexer and verdict for six command words, no record | `~/git`, `*/git` and `$HOME/git` unexpanded, read as git, and deny; `$GIT`, `gi*` and `$(which git)` silent |
| The full suite, repository-wide lint and typecheck (the broad gate) | not yet: no run exists, and it belongs to the sealer after the rounds settle. It is not due, because this round leaves findings 1 and 2 open |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1 (the phantom note's commands act on the shell's tree) and 🟡 2 (the force-staged check misses paths when the switch goes through a subdirectory, a regression from the fix)
Loses a record or crashes: no

## Proof

Files opened at fe24f07: `hooks/worktree-guard.py` (ELSEWHERE, `judgeable`, `segment_cwd`, `tracked_changes`, `phantom_entries`, `repo_paths`, `main` from 2040 to the end), `hooks/cmdline.py` (`parse_git`, `adds_a_worktree`, `apply_chdir`), `docs/worktree-guard-spec.md` (§A, §*Creation consent* 255-265, §*Which tree*, §*Known limits*), `tests/test_guard_resolves_the_tree_it_judges.py` (the harness and the new case), `tests/test_the_guard_asks_once_per_session.py` (`COMMAND_WORD_GROUPS` and its case), `tests/conftest.py` (the repo template, the language pin), `skills/implement/SKILL.md` (540-560), the work item's `rounds/round-1.md` and `plan.md`, and the full diff of the fix range, including the ledger fragment and `seal/releases/0.15.5.md` and `0.9.1.md`.
