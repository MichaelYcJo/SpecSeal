# 1790550714-a-git-call-after-cd-is-charged-to-git — review round 2

| Field | Value |
|---|---|
| Target SHA | ee72397b0401c91974d66cc578df81f2dd261c45 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 635 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — findings 1, 2, 3 and 4: a quoted parenthesis and a `);(` token break the substitution rule four sentences state, a comment on a continuation line reaches the line again, and the here-string comment names the wrong extent of the cut |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

The verifying round, at the diff of round 1's fixes (3d49670..fdc6fb8). It was asked whether each round-1 verdict is closed as a class, and whether the four new units are correct. The shapes it was given to break were nesting, arithmetic, process substitution and parentheses in quotes or comments inside a substitution; `#` in every quoting form, `${#var}`, `$#` and `\#`; and the one corpus call that moved. It was also asked to check every copy of the narrowed backtick sentence and of the comment rule.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | round 1's finding 1 is not closed as a class: a quoted or escaped `(`, `)` or separator reaches the walk as a bare operator, so a quoted `)` ends a substitution early and a quoted `(` keeps it open to the end of the command | `skills/verify/scripts/session_cost.py:331` | open | executed: `x=$(printf ')'; cd a; git log)` reads `git` (2037cf0 `other`); `n=$(grep -c '(' f)⏎git commit -m x` reads `other` (a2e7fac `git`); `echo ';' git x` reads `git` since phase 1. 0 corpus calls. The patched copy passes 116 cases |
| 🟡 2 | a token that closes a substitution and opens a subshell (`);(`, `)&&(`, `)\|(`) keeps the substitution open, so the subshell's `git` is dropped | `skills/verify/scripts/session_cost.py:331` | open | executed: three shapes read `other` at the target and `git` at a2e7fac; bash parses `echo $(pwd)\|(git c)` as a pipe into a subshell. 0 corpus calls |
| 🟡 3 | round 1's finding 2 is not closed as a class: after `\⏎`, `without_comments` sees no word start, so a comment that opens a continuation line is read as words | `skills/verify/scripts/session_cost.py:273` | open | executed: `ls \⏎# x; git push` reads `git`, where 2037cf0 read `other` and bash reads a comment. The same edit moves 1 corpus call `other` → `git`, a `git -C` after `&& \⏎` |
| 🟡 4 | the `HEREDOC` comment says a here-string cuts the rest of its line; it cuts the rest of the command, every later line included | `skills/verify/scripts/session_cost.py:199` | open | executed: `cat <<< "$x"⏎git push` reads `other`, and the text left is `cat <`. The bound is accepted; the sentence is not true |
| ⬜ 5 | seven of `COMMENT_AFTER`'s nine characters are pinned by no case | `tests/test_session_cost.py:1735` | open | executed: `COMMENT_AFTER` reduced to a space and a newline, 116 passed |
| ⬜ 6 | `without_comments` starts a comment after a substitution's `)` inside a word, and inside quotes nested in `"$( … )"` | `skills/verify/scripts/session_cost.py:258` | open | executed: `echo $(ls)#x; git s` and `x="$(git log --format="%h # %s")"; git push` read `other` at the target and at 2037cf0, `git` at a2e7fac |
| ⬜ 7 | a heredoc operator inside a comment still cuts the lines after it, because bodies are cut before comments are removed | `skills/verify/scripts/session_cost.py:402` | open | executed: `ls # see <<EOF⏎git push` reads `other` at all three copies |
| ⬜ 8 | the changelog fragment's line 12 is 107 characters, where the rest wraps near 76 | `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/changelog.md:12` | open | read; a correction, not counted in `Needs a fix` |
| 🟢 | round 1's finding 3 is answered — the here-string bound is the spec's and moves no call | `skills/verify/scripts/session_cost.py:202` | confirmed | executed: 0 corpus calls move; the sentence stating it is finding 4 |
| 🟢 | round 1's finding 4 is answered — an unrecognised heredoc's body lines are command lines, as the comment now says | `skills/verify/scripts/session_cost.py:194` | confirmed | executed: `cat <<eof⏎git push⏎eof` and `cat <<\EOF⏎git push⏎EOF` read `git` |
| 🟢 | round 1's finding 5 is answered — the fourth bound states each shape's answer | `skills/verify/scripts/session_cost.py:361` | confirmed | executed: seven shapes answer as the docstring says; the corpus count is carried from round 1 |
| 🟢 | the one corpus call round 1's fixes move goes the way the spec says | `skills/verify/scripts/session_cost.py:326` | confirmed | executed: `B=$(git merge-base … \|\| git rev-parse …)`, every `git` inside the substitution, `git` → `other` |
| 🟢 | refusals fall by the same eight | `skills/verify/scripts/session_cost.py:313` | confirmed | executed: 24 → 16 over 23,629 calls and 359 transcripts, against the fix pass's 23 → 15 over 358 |
| 🟢 | the backtick narrowing and the comment rule read alike in every copy | `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md:12` | confirmed | read: both docstrings, the changelog, N1, N2, N4, N6, `overview.md`; `SKILL.md` names neither. The `$( … )` sentence in them is finding 1's |
| 🟢 | the ledger has no drifted or broken row | `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md` | confirmed | executed: `bin/evidence-check --strict` unscoped at the target, exit 0 |

## Paste-ready fixes

```python
        if char == "\\" and quote != "'":
            escaped = command[at + 1 : at + 2]
            at += 2
            if escaped == "\n":
                # `\⏎` is a line continuation, which bash removes before it
                # reads a word, so the boundary before it still holds.
                continue
            # An escaped operator is part of a word, and `shlex` would strip
            # the backslash and hand the walk a bare `;`.
            neutral = escaped and escaped in PUNCTUATION
            out.append("\\" + ("_" if neutral else escaped))
            boundary = False
            continue
        if quote:
            if char == quote:
                quote = None
            elif char in PUNCTUATION:
                # A quoted operator is part of a word, and `shlex` strips the
                # quotes that would say so: `echo ';' git x` reached the walk
                # as a bare `;`, and a quoted `(` inside `$( … )` left the
                # substitution open to the end of the command.
                char = "_"
        elif char in "'\"":
```
```text
without_comments docstring, appended:
    A character the shell reads as part of a word because it is quoted or
    escaped, and that the tokeniser would return as an operator, is replaced
    by a letter here, where the quoting can still be seen.
```
```python
            # `$( … )`, `$(( … ))`, `<( … )` and `>( … )`: no word inside is
            # a command word, and only what follows the `)` that closes the
            # outermost one reaches the line. One operator token can close a
            # substitution and open a subshell (`);(`), so it is walked a
            # character at a time rather than counted.
            opens = token.startswith("(") and previous.endswith("$")
            left = []
            for at, char in enumerate(token):
                if nested:
                    nested += {"(": 1, ")": -1}.get(char, 0)
                elif char == "(" and (
                    (at == 0 and opens) or token[at - 1 : at] in ("<", ">")
                ):
                    nested = 1
                    if left and left[-1] in "<>":
                        left.pop()
                else:
                    left.append(char)
            token = "".join(left)
```
```python
        if char == "\\" and quote != "'":
            escaped = command[at + 1 : at + 2]
            at += 2
            if escaped == "\n":
                # `\⏎` is a line continuation, which bash removes before it
                # reads a word, so the boundary before it still holds.
                continue
            out.append("\\" + escaped)
            boundary = False
            continue
```
```python
# body arguments of the first line. And a here-string, `<<< "$x"`, is matched
# from its second `<` as an operator whose delimiter is `$x`; no later line is
# that, so the command is cut from there to its end, every later line with
# it, as it was before #377. Round 1 of #377's review found neither moving a
# call in 358 transcripts, and the pattern is left as 0.9.4 stated it.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_session_cost.py -q -p no:xdist -k "substitution_does_not_reach or comment_runs_nothing"` at the target | 2 passed |
| 53 command shapes through 2037cf0's, a2e7fac's and the target's `family`, with the target's command words printed | 18 differ from bash's reading: findings 1, 2, 3, 6 and 7, the `case` bound, the backtick bound and one shape bash rejects |
| the shapes that decide a comment or a subshell, through bash's own parser (`declare -f` of a function holding each) | `ls \⏎# x` is a comment; `$(ls)#x` is one word; `(ls)#x` is a comment; `x="$(… "%h # %s")"` keeps its `#`; `echo $(pwd)\|(git c)` is a pipe into a subshell |
| five mutants of the new code, one at a time, each against the whole module | `COMMENT_AFTER` reduced to a space and a newline: 116 passed (finding 5). No `max(0, …)`: 116 passed. `>(` dropped from the openers, nothing kept after the outermost `)`, a comment eating its newline: each 1 failed. Restored byte for byte |
| every Bash call in 359 transcripts under `~/.claude/projects/*SpecSeal*/`, through a2e7fac, the target and the patched copy | a2e7fac → target: 1 call, `git` → `other`. Refused: 24, 16, 16. target → patched: 1 call, `other` → `git` |
| findings 1 to 3's fixes applied in the clone, then `bin/test tests/test_session_cost.py -q -p no:xdist` | 116 passed; the file restored with `git checkout`, and the clone was clean after |
| the planted lines above, at the target and on the patched copy | 11 wrong at the target, 0 on the patched copy |
| `cat <<< "$x"⏎git push`, the finding 4 and 5 shapes, through the target | as findings 4 and 5 and the verdicts say |
| `bin/evidence-check --strict`, unscoped, at the target | exit 0; 0 drifted, 0 broken, 0 malformed in every file |
| the orchestrator's four modules giving 205 passed, and ruff clean, at the target | not re-run here: unverified by this round, and the orchestrator answers it |
| the full suite, repository-wide lint and typecheck (the broad gate) | not yet. Nobody has run it. It is the sealer's after the rounds settle, and it has not come due, because this round leaves findings 1 to 4 open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/session_cost.py:270` | round 1's 🟡 1 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:265` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:193` | round 1's ⬜ 3 — answered |
| round-1 | `skills/verify/scripts/session_cost.py:184` | round 1's ⬜ 4 — answered |
| round-1 | `skills/verify/scripts/session_cost.py:282` | round 1's ⬜ 5 — answered |
| round-1 | `tests/test_session_cost.py:1572` | round 1's 🟢 — confirmed |
| round-1 | `skills/verify/scripts/session_cost.py:722` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.9.4.md:32` | round 1's 🟢 — confirmed |
| round-1 | `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md` | round 1's 🟢 — confirmed |
| round-1 | `questions.md` Q1 | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
