"""The bare words of a command, read for consent tokens and nothing else (#692).

`questions.md` P3, answer (a), keeps the old waiver and answer spellings --
`: '[no-review]'; git commit …`, `git worktree add … # [worktree-ok]` --
working beside the git-native `git -c specseal.waive=review` form. A shell
drops those words before git runs, so a git hook never sees them; this reads
them out of the command and `hooks/answers.py` hands them to the hook.

It is the one text read the redesign keeps, and its failure direction is why
it may: a token it cannot read costs one refusal naming the git-native
spelling, and a token it reads has exactly the standing tokens always had --
`docs/worktree-guard-spec.md` §*Choice sites* calls it an audit trail, not an
authorization. Nothing here names a directory or decides where an action
lands.

The rules are the two consent reads 0.16.0 had, joined:

  * **a bare word, never a substring** -- inside a quoted message it is prose
    (`git commit -m "drop [no-review] later"`), which `has_marker` and
    `has_token` both refused to read as consent;
  * **comments are read** -- the documented form writes the token in one;
  * **a parenthesis riding on a word is not part of it** --
    `(git worktree add ../wt f [worktree-ok])` (the guard's `has_token`);
  * **an unbalanced quote reads nothing** -- the guard's choice over the
    commit gate's substring fallback, because reading loosely is the
    direction that waives without anybody asking, and here the cost of the
    other direction is one refusal.
"""

import shlex

KNOWN = ("[no-review]", "[no-parity]", "[worktree-ok]", "[shared-tree-ok]")


def words(command):
    """Every bare word of `command`, comments included; () for one that does
    not split."""
    lexer = shlex.shlex(command or "", posix=True, punctuation_chars=";&|<>")
    lexer.commenters = ""
    lexer.whitespace_split = True
    try:
        return tuple(lexer)
    except ValueError:
        return ()


def given(command):
    """The known tokens `command` carries as bare words, in `KNOWN`'s order."""
    found = {w.strip("()") for w in words(command)}
    return tuple(t for t in KNOWN if t in found)
