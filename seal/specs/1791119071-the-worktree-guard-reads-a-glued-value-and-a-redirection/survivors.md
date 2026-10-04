# Survivors — the worktree guard reads a glued value and a redirection

Phase 2 rewrote `_bare_words`'s docstring in `hooks/worktree-guard.py`: the
reduction it describes moved from `hooks/cmdline.py`'s `unglued` and
`_without_redirections` to the guard's own `handed_words`, so the sentence
about what `unglued` leaves on a word went with it. The place below describes
`unglued` itself, which is unchanged.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/plan.md` | `unglued` cuts at the first `<` or `>` and leaves an `&` on the word before it. | a released work item's plan describing `hooks/cmdline.py#unglued`, which this branch did not touch and which still cuts that way; the guard no longer calls it, and the removed docstring sentence was about the guard's use, not about `unglued` |
