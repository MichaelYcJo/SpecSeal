# 1790550714-a-git-call-after-cd-is-charged-to-git — review round 1

| Field | Value |
|---|---|
| Target SHA | a2e7facc9998afbd9f351a7e53a59d8491d909aa |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 635 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `3d49670e13cde1a1764c925d9aaa69d16f646f6c..fdc6fb883a7b381f80ea9098753f6a3983abd56e`, 3 commits |
| Contract changes | none |
| New units | COMMENT_AFTER (depth 1); without_comments (depth 1); test_a_separator_inside_a_substitution_does_not_reach_the_line (depth 1); test_a_comment_runs_nothing_whatever_it_holds (depth 1) |
| Needs a fix | yes — findings 1 and 2: a separator inside a substitution or a comment is read as the line's, against the rule four sentences state |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1 of the build, at the branch's tip after the smith's three phases. The round was asked to enumerate every command shape where `git`/`gh` is or is not a command word, including separators, substitutions, comments, heredoc bodies and terminators, and wrappers. It was asked to check that the tokenizer's fallback is never worse than the base, that every consumer reads `ran`, and that every sentence about the families and the heredoc cut is true. It was also asked to mutate each new case and to run `evidence-check --strict` unscoped.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a separator inside `$( … )`, `<( … )` or `>( … )` puts the next word in command position, against the rule four sentences state | `skills/verify/scripts/session_cost.py:270` | **fixed** `bbedf36a5520498eba1612df6b12d28440cc9489` | fixed at bbedf36a5520498eba1612df6b12d28440cc9489 — the code moved to the sentences: `spec.md` §*Decided from the tree* states "A command substitution is not a command position", and the four sentences carry it. `command_words` tracks nesting from `$(`, `$((`, `<(` and `>(` and returns to the line only after the outermost `)`. Backticks cannot be tracked once the tokenizer strips quotes (the reviewer measured 11 real `git` calls turning `other`), so the backtick half of `command_words`' and `runs_git`'s docstrings, the changelog and ledger N1 is narrowed. The divergence is recorded in `overview.md`; executed: 3 shapes read `git` at the tip and `other` at 2037cf0; the fix moves 1 of 23,553 corpus calls |
| 🟡 2 | a separator inside a `#` comment puts the next word in command position, where 2037cf0 answered `other` | `skills/verify/scripts/session_cost.py:265` | **fixed** `bbedf36a5520498eba1612df6b12d28440cc9489` | fixed at bbedf36a5520498eba1612df6b12d28440cc9489 — and 73af600801b46b2c3aff80207d2af08f6fe39bf8 — `without_comments` strips a comment by bash's rule before the tokenizer: a `#` outside quotes that starts a word, keeping the newline that ends it. 73af600 adds the shape that reaches the escape branch. Ledger N4 and `overview.md` §Not done are corrected; executed: 2 shapes worse than 2037cf0; 0 corpus calls; the fix cuts refusals 23 → 15 with no family change |
| ⬜ 3 | a here-string `<<< "…"` is cut as a heredoc, dropping the rest of the line | `skills/verify/scripts/session_cost.py:193` | answered | `spec.md` In §4 fixes the `HEREDOC` pattern and its lowercase-delimiter bound; the answer is 2037cf0's, and 0 of the 43 corpus calls carrying `<<<` move. The here-string limit is now stated in the `HEREDOC` comment at bbedf36; executed: same answer as 2037cf0; 43 corpus calls, none moves |
| ⬜ 4 | a heredoc with a lowercase or escaped delimiter now has its body lines read as commands | `skills/verify/scripts/session_cost.py:184` | answered | The same clause fixes the lowercase bound; 0 corpus calls move for this reason. The reviewer's sentence is now in the `HEREDOC` comment at bbedf36: a body under a delimiter the pattern does not know is read as command lines; executed: 2 shapes worse than 2037cf0; no corpus call moves on this account |
| ⬜ 5 | `git.exe`, `git-lfs`, a case arm, a function body after `function f`, a leading redirection and an array assignment read against their bash meaning | `skills/verify/scripts/session_cost.py:282` | answered | `spec.md` In §1 makes the basename exactly `git` or `gh`; a case arm, `function f {`, a leading redirection and an array assignment are grammar the walk does not model, and the corpus holds 0 of them. `runs_git`'s docstring states them as a fourth bound at bbedf36; executed as shapes; none in the corpus |
| 🟢 | every #377 case is the one that holds its property | `tests/test_session_cost.py:1572` | confirmed | executed: 20 mutants, each killed by at least one case |
| 🟢 | the fallback never answers worse than 2037cf0's anchored rule | `skills/verify/scripts/session_cost.py:282` | confirmed | executed: about 95 shapes and the corpus; the only regressions are finding 5's basename shapes |
| 🟢 | both family sites read `ran`, and every call dict reaches `analyse` through `load` | `skills/verify/scripts/session_cost.py:722` | confirmed | read: four callers, each a slice of `load`'s list; executed through the `--json` case |
| 🟢 | 0.9.4 S2's correction states what the code does | `seal/releases/0.9.4.md:32` | confirmed | read against the `family` docstring and the heredoc function |
| 🟢 | the ledger has no drifted or broken row | `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md` | confirmed | executed: `bin/evidence-check --strict` unscoped, exit 0, 2,480 ok |
| ❓ | how the 0.15.5 run's own segment readings move | `questions.md` Q1 | ❓ out of verified scope | the transcripts are on another machine; the owner answers it, as `overview.md` already records |

## Paste-ready fixes

```python
    position, previous, nested = True, "", 0
    for token in lexer:
        if token and set(token) <= set(PUNCTUATION):
            opens = token.startswith("(") and previous.endswith("$")
            if nested or opens or token[:2] in ("<(", ">("):
                # `$( … )`, `$(( … ))`, `<( … )` and `>( … )`: no word inside
                # is a command word, and only what follows the `)` that
                # closes the outermost one reaches the line.
                nested = max(0, nested + token.count("(") - token.count(")"))
                token = "" if nested else token[token.rfind(")") + 1 :]
            chars = set(token)
            position = not (chars & REDIRECTION) and bool(chars & SEPARATOR)
        elif position:
```
```text
N1: … A word inside quotes, inside `$( … )` or `<( … )`, or behind a wrapper
is not a command word, and neither is a backtick substitution's first word. …

changelog: … A word inside quotes, inside `$( … )` or behind a wrapper such
as `timeout` is not a command word, so `grep -rn git`, `cat .git/config` and
`echo 'a; git b'` stay out. …
```
```python
# A `#` that begins a word, outside quotes, starts a comment that runs to
# the end of its line. It is bash's rule and not the tokeniser's, which
# starts one inside a word and swallows the newline that ends it.
COMMENT_AFTER = frozenset(" \t\n;&|()")


def without_comments(command):
    """The command with every shell comment removed, its newline kept.

    So `# cd x && git push` loses its `&&` and its `git`, while `a#b`,
    `${#x}` and `echo '#'` keep their `#`. A comment holding an apostrophe
    no longer reaches the tokeniser, so it no longer refuses the line."""
    out, quote, at, boundary = [], None, 0, True
    while at < len(command):
        char = command[at]
        if char == "\\" and quote != "'":
            out.append(command[at : at + 2])
            at += 2
            boundary = False
            continue
        if quote:
            if char == quote:
                quote = None
        elif char in "'\"":
            quote = char
        elif char == "#" and boundary:
            end = command.find("\n", at)
            at = len(command) if end == -1 else end
            continue
        out.append(char)
        at += 1
        boundary = quote is None and char in COMMENT_AFTER
    return "".join(out)
```
```python
    lexer = shlex.shlex(
        without_comments(command), posix=True, punctuation_chars=PUNCTUATION
    )
    # A newline is a separator here, not whitespace. `without_comments` has
    # already removed every comment, so `#` is an ordinary character to the
    # tokeniser, whose own comment handling would swallow the newline that
    # ends a comment and the command on the next line with it.
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
```
```text
`#` is an ordinary character to the tokeniser instead, and comments are
removed before it by bash's rule (a `#` that begins a word, outside quotes),
so a comment holding a separator or an apostrophe reaches neither the
command words nor the refusal.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_session_cost.py -q -p no:xdist -k <the #377 cases, the heredoc case, the other-note case, both comparability cases>` at the target | 12 passed |
| 20 mutants, one at a time, against the same selection: empty reserved words, no assignment skip, no `$(` branch, newline as whitespace, the tokeniser's comments restored, no redirection guard, exact name instead of basename, fallback `False`, fallback exception escaping, fallback judging the whole line, no `<<-` tabs, cut to end, operator line dropped, search restarted at 0, each `analyse` site reading `command`, `load` storing the flat text in `ran`, `git` checked first, the fallback pattern unanchored, `(` removed from the separators | each killed; restored byte for byte |
| about 95 command shapes through 2037cf0's rule and the tip's `family`, with the tip's command words printed | findings 1, 2, 4 and 5; every shape in the prompt's list otherwise answers as the docstrings say |
| every Bash call in the 358 transcripts through the tip and through 2037cf0's rule | 3,765 calls move to `git`; 10 leave `git`, all to `test` |
| findings 1 and 2's fixes applied in the clone, then `bin/test tests/test_session_cost.py -q` | 114 passed |
| the same fixes over every Bash call in the corpus | 1 call moves (`git` → `other`); refusals 23 → 15; reverted |
| a backtick arm added to finding 1's fix, over the corpus | 11 real `git` runs turned `other`; dropped from the fix |
| calls holding `<<<`, with the here-string neutralised | 43 calls, 0 move |
| `bin/evidence-check --strict`, unscoped, at the target | exit 0; 2,480 ok, 0 drifted, 0 broken, 0 malformed |
| the full suite, repository-wide lint and typecheck (the broad gate) | not yet run by anyone. It is the sealer's, after the rounds settle; this round is not the last, since it leaves two findings open |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| how the 0.15.5 run's segment readings move (Q1) | `overview.md` §*Not verified* | the owner, on the machine that holds the 0.15.5 transcripts |
