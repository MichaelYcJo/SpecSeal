# 1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 723dffd2 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Take one branch of `plan.md` §*What phase 4 builds* per candidate, mechanically
from phase 3's counts, under the owner's rule of 2026-10-03: zero builds the
ask, one or more removes the candidate and names the limit in
`docs/worktree-guard-spec.md` §*Known limits* with the count, the corpus and
the date. Keep `hooks/cmdline_base.py` byte-identical. Measure the median of
fifteen `dispatch.py pre-bash` calls on a plain `git switch` before and after.

## What this phase found

**The branches taken.** Count A was 9, so candidate A, `unplaced_switch`, and
its two helpers were deleted with their unit cases, and §*Known limits* gained
a bullet with the count, the corpus and the date. A case pins #686's seven
shapes silent over a dirty `w` under a clean session. Count C was 0, so
candidate C is wired.

**Where C is wired.** `main` gained one inner function, `quiet`, that every
silent exit after the walk now calls: the no-verdict exit, the no-repository
exit, the exit after a creation's own verdict, and the clean single-stream
exit. It asks `wider_only_kinds`, and `ask_what_only_the_wider_reading_finds`
puts what comes back to the person: consent first for a creation (D10), then
one `ask` naming the kinds, in both languages. No row that speaks was touched,
so `WIDER_FIRST` still denies.

**Two planned lines turned out dead, and were dropped rather than kept.** The
plan had `quiet` discard a kind the frozen loop found. `classify` finds a
subset of what `switch_kind` reads from the same frozen segments, so
`wider_only_kinds` has already left that kind out, and the discards could
never change an answer. The `-c`/`-C` test in `switch_kind` went the same
way, after phase 2's break of it survived.

**The import is guarded.** Phase 2's unguarded import made a broken
`hooks/cmdline.py` take the whole guard down beside the commit gate, the one
red case of that phase's run. Wiring C needs the import, so it now sits in a
`try`, and where it fails `wider_only_kinds` finds nothing. The guard keeps
its ACTIVE deny on a broken reader, and the commit gate's own failure still
names the module. `test_a_broken_shared_module_names_every_gate_that_imports_it[cmdline]`,
red at `d367791a`, passes unchanged, and
`test_a_broken_wider_reader_costs_only_the_question` pins the guard's half.

**Two base-answer cases changed, with a note in each.**
`test_a_segment_only_the_reading_past_redirections_finds_is_not_git_to_the_guard`
went from `silent` to `ask`, with `top` still None, so no tree is judged.
`test_a_zsh_prefixed_git_is_not_git_to_the_guard_or_the_consent_writer`'s
switch half went from `silent` to `ask`, and its consent-writer half still
files nothing.

**README.** Both worktree-guard rows were re-read. They promise that a
creation is not asked after `automation`, and consent first keeps that true,
so neither changed.

**Timing, executed.** Fifteen `dispatch.py pre-bash` calls on
`git switch feature/x` in a scratch repository, after one warm-up call each.
The median was 251.2 ms with `233f0455`'s `hooks/` and 241.3 ms with this
branch's. The difference is inside the noise; the branch is not slower.

**Every new case seen red, executed** with `mutation-check` on the committed
tree, one break at a time. The last silent exit made to ask turned the seven
`UNPLACED` pins red. The question skipped in `quiet`, or skipped at the
no-verdict exit alone, turned the `WIDER_ONLY` cases and both changed
base-answer cases red. Consent not read turned the consent case red, and so
did renaming either kind, changing either language's join, and dropping the
broken-reader guard, each in its own case. All nine breaks were red.

**The narrow run.** The 13 modules that read `hooks/worktree-guard.py`, with
every module that reads `docs/`, 65 in all: 3756 passed, 74 skipped, none
failed. `hooks/cmdline_base.py` has no diff against `233f0455`, and
`tests/test_the_frozen_reading_never_grows.py` passed in that run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `unplaced_switch`, `_wider_walk` and `_places` (NAME NOT IN TREE), with their unit cases | `docs/worktree-guard-spec.md` §*Known limits*, the bullet naming the fallback and the count; `phases/phase-3.md` holds the count |
