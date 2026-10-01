"""The bare words of a command, read for consent tokens and for the words that
step around git's hooks, and nothing else (#692).

`questions.md` P3, answer (a), keeps the old waiver and answer spellings --
`: '[no-review]'; git commit …` -- working beside the git-native
`git -c specseal.waive=review` form. A shell drops those words before git
runs, so a git hook never sees them; this reads them out of the command and
`hooks/answers.py` hands them to the hook.

It is the one text read the redesign keeps, and its failure direction is why
it may: a token it cannot read costs one refusal naming the git-native
spelling, and a token it reads has exactly the standing tokens always had --
`docs/worktree-guard-spec.md` §*Choice sites* calls it an audit trail, not an
authorization. `steps_around_hooks` fails the same way round: a word it reads
that meant nothing costs one judgment by the reading git's hooks replace.
Nothing here names a directory or decides where an action lands.

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


def _empties_the_environment(word, after):
    if word.strip("(").rsplit("/", 1)[-1] != "env":
        return False
    return after in ("-", "--ignore-environment") or (
        after.startswith("-") and not after.startswith("--") and "i" in after
    )


def steps_around_hooks(command):
    """True when `command` carries a word that can keep this plugin's git hooks
    from judging it, so the PreToolUse reading must not stand aside for it
    (round 1 of #692, 🟡 2 and 🟡 8; `questions.md` P6's commit half).

    Three kinds, each living in the one command where the installer, which
    runs before it, cannot see them: `core.hooksPath` in any spelling (`-c`,
    `--config-env`, `git config`, a `GIT_CONFIG_*` value), any `GIT_CONFIG*`
    assignment, and `env` emptying the environment, which leaves the stub no
    session variable. A command that does not split is read as one of them.
    The direction is the refusal's: a word read here that meant nothing costs
    the reading's judgment of one command, which is 0.16.0's.
    """
    split = words(command)
    if not split:
        return bool((command or "").strip())
    for i, word in enumerate(split):
        if "hookspath" in word.lower():
            return True
        if word.lstrip("(").startswith("GIT_CONFIG") and "=" in word:
            return True
        after = split[i + 1] if i + 1 < len(split) else ""
        if _empties_the_environment(word, after):
            return True
    return False
