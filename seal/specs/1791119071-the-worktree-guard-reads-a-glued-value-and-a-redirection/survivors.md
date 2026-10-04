# Survivors — the worktree guard reads a glued value and a redirection

Phase 2 rewrote `_bare_words`'s docstring in `hooks/worktree-guard.py`: the
reduction it describes moved from `hooks/cmdline.py`'s `unglued` and
`_without_redirections` to the guard's own `handed_words`, so the sentence
about what `unglued` leaves on a word went with it. The place below describes
`unglued` itself, which is unchanged.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1791019475-a-restore-is-asked-no-switch-question-and-env-options-are-whole/plan.md` | `unglued` cuts at the first `<` or `>` and leaves an `&` on the word before it. | a released work item's plan describing `hooks/cmdline.py#unglued`, which this branch did not touch and which still cuts that way; the guard no longer calls it, and the removed docstring sentence was about the guard's use, not about `unglued` |
| `seal/releases/0.18.1.md` | a `checkout` with no `--` among its words that names `-` or a word other than | G1 as it shipped in 0.18.1, which is frozen; this item's fragment supersedes it with `Corrected · G1`, which carries the sentence round 1's fix pass wrote |
| `seal/specs/1791119071-the-worktree-guard-reads-a-glued-value-and-a-redirection/spec.md` | the sentence "Each side is read by its words alone: a `switch` naming a word or `-`, a `checkout` carrying `-b` or `-B`, a `checkout` | the frame quoting #750's sentence as the one this work item rewrites; it is the starting state, and the frame is not this pass's to edit |
