# Review round 2 — `fix/377-a-git-call-after-cd-is-charged-to-git`

Target SHA `ee72397b0401c91974d66cc578df81f2dd261c45`, base
`origin/release/v0.15.6`. This is the verifying round. Its target is round
1's fix range, `3d49670e13cde1a1764c925d9aaa69d16f646f6c..fdc6fb883a7b381f80ea9098753f6a3983abd56e`
(bbedf36, 73af600, fdc6fb8), and not the branch. `ee72397` changes only
`round-1.md`, so the code at the target is fdc6fb8's. I reviewed in a
`git clone --no-local` at the target under this round's scratchpad
directory, since deleted, and compared three copies of `session_cost.py`:
2037cf0's (the base rule), a2e7fac's (round 1's target) and the target's.

How the findings relate:

```
round 1's fixes
  ├ finding 1's fix: a depth count over $( … ), <( … ), >( … )
  │    closes every shape round 1 named                                  (executed)
  │    ① a quoted or escaped ( ) ; reaches the count as an operator       (🟡, both directions)
  │    ② one token that closes a substitution and opens a subshell       (🟡, git lost)
  ├ finding 2's fix: without_comments, bash's word-start rule
  │    closes every shape round 1 named                                  (executed)
  │    ③ after a line continuation it sees no word start                 (🟡, worse than 2037cf0)
  │    ⑤ seven of COMMENT_AFTER's nine members are pinned by nothing    (⬜)
  │    ⑥ it starts a comment in two places bash does not                (⬜, same answer as 2037cf0)
  │    ⑦ a heredoc operator inside a comment still cuts                 (⬜, older than the fix)
  └ the answers to findings 3, 4 and 5
       ④ the here-string sentence says "its line"; the cut is to the end (🟡)
       ⑧ the changelog fragment has one unwrapped line                  (⬜, correction)
```

Every shape below was put through all three copies. Over the 359 transcripts
under `~/.claude/projects/*SpecSeal*/` today (23,629 Bash calls), none of
findings 1 to 3 moves a call at the target. So the published figures stand,
and the findings are about sentences the fix pass wrote that the code does
not keep. Two of the three answer worse than a2e7fac, and finding 3 answers
worse than 2037cf0 as well.

## Round 1's verdicts

- **Finding 1 (fixed at bbedf36): closed for the shapes it named, and not
  as a class** (executed). The four cases in the new test and the prompt's
  nesting shapes all answer as the docstring says: `$(a $(b) c; git x)`,
  `$((1+2)); git x`, `$(( (1+2) * 3 )); git s`, `<( … )` inside `$( … )`,
  and a `)` inside a comment inside a substitution. What stays open is
  findings 1 and 2 below. The count reads the tokeniser's output, and that
  output has already lost the quotes and the order the count needs.
- **Finding 2 (fixed at bbedf36 and 73af600): closed for the shapes it
  named, and not as a class** (executed). `#` inside single, double and
  ANSI-C quotes, `a#b`, `${#var}`, `$#`, `\#`, `\\#`, a `#` after `<<EOF` on
  the operator's line, a tab before `#`, `;#` and `|#` all answer as bash
  reads them. What stays open is finding 3 below, a comment on a
  continuation line.
- **Finding 3 (answered): the answer stands, and the sentence written for
  it is finding 4 below** (executed). The bound is the spec's and moves no
  call. The comment names the wrong extent of the cut.
- **Finding 4 (answered): true** (executed). `cat <<eof⏎git push⏎eof` and
  `cat <<\EOF⏎git push⏎EOF` are both `git` at the target, as the `HEREDOC`
  comment now says.
- **Finding 5 (answered): true** (executed). A `case` arm, `function f {`,
  `>out git status`, `git-lfs pull` and `git.exe status` answer `other`, and
  `x=(git s)` answers `git`, each as the fourth bound in `runs_git`'s
  docstring states. That none occurs in the corpus is carried from round 1's
  measurement and not re-established.
- **Q1 (❓, deferred in round 1)** was not re-opened. It stays where round 1
  put it, in `overview.md` §*Not verified*, for the owner.

## Findings

### 1. A quoted `(` or `)` moves the substitution count, in both directions — 🟡

`skills/verify/scripts/session_cost.py:331`. `shlex` in POSIX mode removes
quotes and backslashes before the walk sees a token. So `')'`, `"("` and
`\;` arrive as the bare tokens `)`, `(` and `;`, and
`set(token) <= set(PUNCTUATION)` reads each as an operator. The depth count
that bbedf36 added then moves on a character bash reads as part of a word.

- A quoted `)` inside a substitution closes it early, and the words after
  it are command words: `x=$(printf ')'; cd a; git log)` and
  `x=$(echo ")"; cd a; git log)` read `git`. 2037cf0 read `other`, and the
  rule says `other`.
- A quoted `(` inside a substitution leaves the count above zero until the
  command ends. Every later word is dropped, every later line included:
  `n=$(grep -c '(' f)⏎git commit -m x` and `x=$(echo '(') ; git s` read
  `other`. a2e7fac read `git`, and bash runs `git`.

The same cause is older than the fix: `echo ';' git x`, `echo "&&" git x` and
`echo \; git x` read `git` at a2e7fac and at the target, where 2037cf0 read
`other`. It stands beside the unchanged docstring sentence at `:297`, *"so a
separator or a word inside quotes is not seen"*. It is one finding, because
one edit closes both.

Why it matters. The fix pass wrote the sentence *"No word inside `$( … )` …
is a command word, however many commands the substitution holds, and only
what follows the `)` that closes the outermost one reaches the line again"*
into `command_words`' docstring, `runs_git`'s docstring, ledger N1 and the
changelog fragment. A quoted parenthesis breaks both halves of it. The
second direction also reaches past the line, because a count left open
drops every later command.

The fix belongs in the pass that still sees the quotes. `without_comments`
already tracks quoting, so it can turn a quoted or escaped operator
character into a letter before the tokeniser strips the quote. With that
applied in the clone, the eleven quoted and escaped shapes above answer as
bash does, the module's 116 cases pass, and the corpus moves by one call
(finding 3's, below). Refusals stay at 16. Tracking a backtick that is not
quoted would become possible in the same pass. This round does not ask for
that, because the narrowing is the fix pass's accepted answer.

### 2. A token that closes a substitution and opens a subshell keeps the substitution open — 🟡

`skills/verify/scripts/session_cost.py:331`. `shlex` groups adjacent
punctuation into one token, so `);(`, `)&&(` and `)|(` each arrive whole.
`nested + token.count("(") - token.count(")")` ignores order, so it reads
one close and one open as no change. The subshell that follows is then
inside the substitution, and its `git` is dropped.
`x=$(pwd);(cd a && git s)`, `echo $(date)&&(cd a; git x)` and
`echo $(pwd)|(git c)` read `other` at the target and `git` at a2e7fac. Bash
parses the last one as `echo $(pwd) | ( git c )` (executed through
`declare -f`). The fix is to walk the token one character at a time, which
also lets `)<(` close one process substitution and open the next.

### 3. A comment that opens a continuation line is read as words — 🟡

`skills/verify/scripts/session_cost.py:273`, in `without_comments`, a unit
the fix pass created. The escape arm sets `boundary = False` after every
escaped character, `\⏎` included. Bash removes a `\⏎` before it reads any
word, so the boundary that held before the backslash still holds after it.
`ls \⏎# x; git push` reads `git` at the target. Bash reads `ls` and a
comment (executed through `declare -f`), and 2037cf0 read `other`. That is
round 1's finding 2 again, a separator inside a comment reaching the line,
through the one door the new function leaves open.

Removing `\⏎` in that arm also closes a related miss that predates the
branch. The tokeniser reads `\⏎git` as the single word `⏎git`. So
`cd /x && \⏎git status` reads `other`, and one real call in the corpus has
that shape (a `git -C … worktree add` after `cd … && \`). It is the one call
the patched copy moves, from `other` to `git`.

### 4. The here-string sentence names the wrong extent of the cut — 🟡

`skills/verify/scripts/session_cost.py:199`, written at bbedf36 to answer
round 1's finding 3. The sentence is *"a here-string, `<<< "$x"`, is matched
as an operator with no closing line, so the rest of its line is cut"*. The
pattern matches from the second `<`, with `$x` as the delimiter, and no
later line equals `$x`. So the command is cut from there to its end, every
later line included. `cat <<< "$x"⏎git push` reads `other`, and
`without_heredoc_bodies` returns `cat <` for it (executed). A reader who
trusts the comment expects the next line to be read. Round 1's own summary
row said *"dropping the rest of the line"*, and the sentence inherited it.
No call moves, so only the sentence is wrong.

### 5. Seven of `COMMENT_AFTER`'s nine characters are pinned by no case — ⬜

`tests/test_session_cost.py:1735`. With `COMMENT_AFTER` reduced to a space
and a newline, all 116 cases of the module pass (executed). So
`ls;# c; git push`, `ls⇥# c; git push` and `(ls)# c; git push` could start
reading `git` again with nothing going red. The code is right today. The
lines to add are under *Regression tests to plant*. Three other mutants of
the new code each die: `>(` dropped from the openers, nothing kept after the
outermost `)`, and a comment that eats its newline. A fourth, dropping the
`max(0, …)` guard, survives, and it differs only on input bash itself
rejects.

### 6. `without_comments` starts a comment in two places bash does not — ⬜

`skills/verify/scripts/session_cost.py:258`. Both shapes read `git` at
a2e7fac and `other` at the target and at 2037cf0, so neither is worse than
the base rule.

- `)` is in `COMMENT_AFTER`, which is right after a subshell (bash reads
  `(ls)#x` as a comment) and wrong after a substitution inside a word. In
  `echo $(ls)#x; git s` bash runs `git s`.
- The quote tracking does not know that quotes nest inside `"$( … )"`. In
  `x="$(git log --format="%h # %s")"; git push`, the `#` looks unquoted
  after a space, and `; git push` is removed with it.

### 7. A heredoc operator inside a comment still cuts the lines after it — ⬜

`skills/verify/scripts/session_cost.py:402`. `family` removes heredoc bodies
before `runs_git` removes comments. So `ls # see <<EOF⏎git push` is cut at
`<<EOF`, and it reads `other` at all three copies. Bash runs `git push`.
It is older than the fix. It is worth knowing because the new case is named
`test_a_comment_runs_nothing_whatever_it_holds`, and a comment holding
`<<EOF` does change the reading. Reversing the two passes is not a
paste-ready repair: an apostrophe in a heredoc body would then open a quote
in `without_comments`.

### 8. The changelog fragment has one line of 107 characters — ⬜, correction

`seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/changelog.md:12`.
The fix pass's edit left `inside backticks is read as the line's. A line
the tokeniser refuses, on an unmatched quote, is judged by` on one line,
where the rest of the fragment wraps near 76. It is paperwork and is not
counted in `Needs a fix`.

## The new units

- `COMMENT_AFTER` — its members are right except `)` after a substitution
  (finding 6), and most of them are unpinned (finding 5).
- `without_comments` — right for every shape the prompt listed except the
  continuation line (finding 3) and the two in finding 6.
- `test_a_separator_inside_a_substitution_does_not_reach_the_line` — every
  line holds at the target (executed, 2 passed). It is the case that kills
  two of the four nesting mutants above. It pins no quoted parenthesis and
  no `);(`.
- `test_a_comment_runs_nothing_whatever_it_holds` — every line holds, and
  the escaped-quote line kills the escape mutant the fix pass named. It pins
  only a space and the start of the command as word starts (finding 5).

## Every copy of the two sentences

All read (the ledger rows through `evidence-check`, which also executed).

- The backtick narrowing reads the same in `command_words`' docstring,
  `runs_git`'s docstring, the changelog fragment, ledger N1 and
  `overview.md`'s divergence row. Each is true at the target:
  ``echo `cd a; git x` `` reads `git`, and ``echo ` git x` `` does not.
- The comment rule reads the same in the `without_comments` docstring,
  `command_words`' docstring, the changelog fragment, ledger N4 and
  `overview.md`. It is true except for finding 3's shape, which N4's *"so
  nothing inside one is a separator or a command word"* covers.
- `skills/verify/SKILL.md` names neither backticks nor comments. Its *"never
  a word inside quotes or inside `$( … )`"* is false in finding 1's shapes,
  and so is the `$( … )` sentence in N1, the changelog and both docstrings.
  One fix repairs all of them without rewording.
- N2's *"15 with comments removed first, the eight gone having refused on a
  comment's apostrophe"* and N6's *"one call … from `git` to `other`"* hold.
  Today's corpus has one transcript more, and it gives 24 → 16, the same
  eight, and the same one call.

## The one call that moved, and the refusals

Executed over 23,629 Bash calls in 359 transcripts. a2e7fac → target moves
exactly one call, `git` → `other`: `D=…; cd "$D"; B=$(git merge-base
origin/main HEAD 2>/dev/null || git rev-parse …); echo …`. Both `git`s are
inside the substitution, and the second follows `||` inside it, which is
round 1's finding 1 itself. The spec's *"A command substitution is not a
command position"* makes `other` the intended answer. Refusals are 24 at
a2e7fac and 16 at the target. The fix pass measured 23 → 15 over 358
transcripts, and the one transcript added since holds one more refused line
at both.

## Regression tests to plant

`tests/test_session_cost.py`. Each line below was red at the target and
green on the patched copy (executed, eleven lines red at the target).

- In `test_a_separator_inside_a_substitution_does_not_reach_the_line`, not
  `git`: `"x=$(printf ')'; cd a; git log)"`, `'x=$(echo ")"; cd a; git log)'`.
  `git`: `"x=$(echo '(') ; git s"`, `"n=$(grep -c '(' f)\ngit commit -m x"`,
  `"x=$(pwd);(cd a && git s)"`, `"echo $(date)&&(cd a; git x)"`,
  `"echo $(pwd)|(git c)"`.
- In `test_git_named_anywhere_but_a_command_word_is_not_git`:
  `"echo ';' git x"`, `'echo "&&" git x'`, `"echo \\; git x"`.
- In `test_a_comment_runs_nothing_whatever_it_holds`, not `git`:
  `"ls \\\n# x; git push"`, and for finding 5, which pass today and pin the
  set: `"ls;# c; git push"`, `"ls\t# c; git push"`, `"(ls)# c; git push"`.
  `git`: `"cd /x && \\\ngit status"`.

## Facts for the ledger

Once findings 1 to 3 are fixed, N1 and N4 need a corrected note and a re-stamp
for `command_words` and `without_comments`, and N6 should gain the corpus
figure the fix produces. On today's corpus that is one call, `other` → `git`.
Nothing this round verified is missing from the ledger as it stands.

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

## Paste-ready fixes

### Finding 1 — a quoted or escaped operator character becomes a letter

In `without_comments`, replacing the escape arm and the quote branch. This
block includes finding 3's line, so apply one or the other.

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

### Finding 2 — walk the operator token one character at a time

In `command_words`, replacing lines 326–332.

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

### Finding 3 — a line continuation keeps the boundary before it

In `without_comments`, the escape arm alone, if finding 1's block is not
taken.

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

### Finding 4 — the here-string sentence

Replacing the last two sentences of the `HEREDOC` comment, lines 197–201.

```python
# body arguments of the first line. And a here-string, `<<< "$x"`, is matched
# from its second `<` as an operator whose delimiter is `$x`; no later line is
# that, so the command is cut from there to its end, every later line with
# it, as it was before #377. Round 1 of #377's review found neither moving a
# call in 358 transcripts, and the pattern is left as 0.9.4 stated it.
```

Needs a fix: yes — findings 1, 2, 3 and 4: a quoted parenthesis and a `);(` token break the substitution rule four sentences state, a comment on a continuation line reaches the line again, and the here-string comment names the wrong extent of the cut
Loses a record or crashes: no

## Proof block

Files opened at the target in the clone: `skills/verify/scripts/session_cost.py`
(lines 98–125, 170–420, 564–680, 712–725, 2218–2245),
`tests/test_session_cost.py` (1617–1660 and the fix diff's two cases),
`skills/verify/SKILL.md` (684–705),
`seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md` (N1–N6
through the fix diff), and in the same work item `rounds/round-1.md`,
`changelog.md`, `overview.md`, `spec.md` (30–40, 160–170), `questions.md`
(14–22) and `plan.md` (60–68). Also `bin/test` (head) and
`rounds/round-1-report.md` (head). The fix range was read as a whole diff:
`3d49670e..fdc6fb88`.
