# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | e1cca725 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

One placement (`spec.md` In 1): the tokenizing adapter and the placement
function in `hooks/worktree_consent.py`; `creation_directory`, the guard's
`judgeable` and `_tokenize_with_separators` through them; S1–S3 planted red
at `5623d728` first; the `Creation consent` sentence of
`docs/worktree-guard-spec.md` with its pin.

## What this phase found

**The guard's `judgeable` is gone rather than kept as a wrapper.** The
placement takes the walk's `wheres` for the segment and picks the first
itself, so the guard's `main` stores `wheres` for each unrecognised shape and
hands them to `_finding_tree`, and `worktree_consent.place` is the one place
`wheres[0]` is read. `segment_cwd` moved with it, and the guard binds both
names (`_tokenize_with_separators`, `segment_cwd`) to the consent module's
functions, so the cases that call them through the guard are unchanged.

**The placement's repository test is `optin.repo_root` now, not the guard's
`repo_paths`.** Both run `git rev-parse --show-toplevel` under a five-second
bound and answer empty where the directory is missing or holds no
repository, so the answer is the same; what changed is that a case patching
`wg.repo_paths` no longer sees the placement's lookup. One case does patch
it, `test_each_tree_is_placed_once_however_many_shapes_it_holds`, and it
counts the stop's lookups, which the placement never made for that command
(its segments run in the session's own directory). It passes unchanged.

**How each case was seen red.** S1's two cases and S3's two new chains, red
against the base hooks (the hooks of `84535260` are the base's): the writer
answered `{other}` and `{missing}`. S3's three pinned chains were green at
the base, as `spec.md` S3 says. `test_the_consent_writer_composes_the_creations_own_dash_c`
pins what already held: `bin/mutation-check` returning the shell's directory
instead of the `-C` target SURVIVED every case of the module until it was
planted, and is red with it. The policy pin, red against the base's text.

**Mutations, through `bin/mutation-check`:** `place` taking the first
resolved entry, red; `place` without its no-repository fallback, red; the
`-C` target swapped for the shell's directory, red. Defaulting
`split_with_separators`' `windows` to False SURVIVED, and it is an equivalent
mutant on this machine: `os.name` is not `nt` here, and every Windows case
passes `windows=True` explicitly.

**The rider moved with its unit.** `_tokenize_with_separators`' RIDER (a
single-quoted UNC path loses the repository) is on
`split_with_separators` now, says the writer reads through the same adapter,
and is re-stamped by `.github/scripts/rider_check.py --reverify`: 20 ok, 0
drifted.

**The released rows are re-read once, in phase 6.** `evidence-check` after
this phase reports 30 released rows drifted, nearly all on
`hooks/worktree-guard.py#main`, which phases 3 and 5 change again, and one
broken row on the removed `judgeable`. Re-reading them now would date a
reading the next two phases undo, so phase 6 writes the `Re-read ·` and
`Corrected ·` rows in one pass.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `hooks/worktree-guard.py#judgeable` and its docstring | `hooks/worktree_consent.py#place`, the docstring with it; a `Corrected ·` row in phase 6 for the released row citing it |
| `hooks/worktree-guard.py#_tokenize_with_separators`' body and its rider | `hooks/worktree_consent.py#split_with_separators`; the guard keeps the name bound to it |
| `hooks/worktree-guard.py#segment_cwd`'s body | `hooks/worktree_consent.py#segment_cwd`; the guard keeps the name bound to it |
| `hooks/worktree_consent.py#creation_directory`'s placement loop (the first resolved entry) | `hooks/worktree_consent.py#place` |
