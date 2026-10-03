# 1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | d367791a |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build candidate A (#686) and candidate C (#678's guard half) as pure functions
in `hooks/worktree-guard.py`, and leave both unwired, so phase 3's probe
imports the code that would be wired. The guard imports `hooks/cmdline.py`
under a name that does not shadow `cmdline_base as cmdline`. A must be true for
#686's seven shapes before `git switch feature/x`, and false for
`cd w && git switch`, `git -C w switch`, a plain `git switch` and
`cd /no/such/dir ; git switch x`. C must find a creation in
`cd w && git 2>&1 worktree add ../wt b` and `git --config-env k=v worktree add
../wt b`, and a switch in `cd w && 2>/dev/null nice -n 5 git switch feature/x`,
`git --config-env k=v switch x` and the `ZSH_PREFIXED` shapes. It must find
nothing for `WIDER_FIRST` or a plain `git switch`. Answer M2.

## What this phase found

Phase 4 removed candidate A and its two helpers, so three names below are
gone from the tree; each line naming one says so.

**Four functions, not two.** `unplaced_switch` (A, NAME NOT IN TREE) and
`wider_only_kinds` (C) both need a kind read from the words alone, since a
transcript carries no tree for `classify` to ask. So `switch_kind` reads a
`parse_git` result as `"switch"`, `"creation"` or None. It counts every
`checkout` that names something, which is `questions.md` D3's upper bound.
`_wider_walk` (NAME NOT IN TREE) is `hooks/cmdline.py`'s walk over its own
splitter, and `_places` (NAME NOT IN TREE) makes two walks' directories
comparable across the two modules' `Unresolved` classes.

**A takes `chosen`**, the segment `main` would judge. Without it, the first
segment `switch_kind` calls a switch stands in, and that is what the probe
counts. **W1** is answered as the frame defaulted: the judged segment is
matched to the wider walk's segment with the same words (the nth such, where
the frozen walk has n before it), and no match answers True.

**C reads the views the commit gate reads**: its splitter's segments,
`merged_segments`, and `unglued` of each, through `hooks/cmdline.py`'s
`parse_git`. It subtracts the kinds the frozen walk's segments hold, so a kind
the frozen reading found keeps its slot (`WIDER_FIRST`).

**M2, executed** with a scratch directory holding `w`:

| Shape | Frozen walk | Reaches A through |
|---|---|---|
| `builtin cd w`, `command cd w`, `time cd w`, `pushd w` | `Unresolved(CONSTRUCT)` | the frozen `Unresolved` |
| `cd "$W"` | `Unresolved(VALUE)` | the frozen `Unresolved` |
| `noglob cd w` | the session's own directory, confidently | the disagreement: the wider walk adds an `Unresolved` |
| `2>&1 cd w` | the session's own directory, confidently | the disagreement: the wider walk adds `w` |

Five and two, as the frame read it.

**The import costs the guard its independence from a broken
`hooks/cmdline.py`.** The 13 modules that read `hooks/worktree-guard.py` gave
764 passed, 1 skipped and 1 failed, and the failure is that fact:
`test_a_broken_shared_module_names_every_gate_that_imports_it[cmdline]` now
sees the guard fail to load beside the commit gate and `implementer-notice.py`.
Phase 4 decides what the import becomes, because it depends on which
candidate is wired.

**Red against a stub that returns the opposite, executed** with
`mutation-check`, one break at a time. `return False` and `return True` at the
head of A, and `return set()` and `return {"switch", "creation"}` at the head
of C, each turned the cases red. So did each inner unit: A's `Unresolved`
test removed, its disagreement ignored, its no-twin answer flipped, and
`chosen` ignored; C's glued views, its merged views and its subtraction
dropped; and four of `switch_kind`'s five branches. The fifth, `-c`/`-C` in a
`git switch`, SURVIVED, because `-c` always takes a name and the name is a
positional the next test already counts. It is removed in phase 4 rather than
pinned by an invented case. A pin for `-b` before `--`, in `classify`'s order,
was added in `df0d1b6c` before the breaks ran, because reading the cases
showed no case could reach that branch otherwise; with it, the break was red.

`main` is unchanged. `tests/test_guard_resolves_the_tree_it_judges.py` passed
whole (149 passed beside the frozen-reader and overview modules).

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
