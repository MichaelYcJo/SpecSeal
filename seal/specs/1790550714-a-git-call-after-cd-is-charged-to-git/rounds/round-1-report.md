# Review round 1 — `fix/377-a-git-call-after-cd-is-charged-to-git`

Target SHA `a2e7facc9998afbd9f351a7e53a59d8491d909aa`, base
`origin/release/v0.15.6` (`2037cf0`). Reviewed in a `git clone --no-local`
at the target under this round's scratchpad directory, since deleted. This
is a first round: the work item has no `round-N.md`, so there are no earlier
coordinates to carry and no earlier verdicts to answer.

How the findings relate:

```
#377: a git call is charged to git by command word, not by position
  ├ the rule, its fallback, the heredoc body cut and the ran wiring   (sound: 20 mutants, all killed)
  ├ ① a separator inside $( … ) or <( … ) puts the next word back
  │    in command position                                           (🟡, four sentences state the opposite)
  ├ ② a separator inside a # comment does the same                  (🟡, worse than 2037cf0's rule)
  └ what the new reading exposes in shapes nobody wrote
       ③ a here-string <<< "…" is cut as a heredoc                   (⬜, older than this branch)
       ④ an unrecognised heredoc's body lines are now command lines  (⬜)
       ⑤ git.exe, git-lfs, case arms, a leading redirection         (⬜)
```

Every shape below was measured against both rules: 2037cf0's (`^\s*(git|gh)\b`
on the flattened text, cut at the heredoc operator) and the tip's. Over the
358 transcripts under `~/.claude/projects/*SpecSeal*/` today (23,553 Bash
calls), findings 1 and 2 together move one call, so the published figures
stand. The findings are about sentences that state a rule the code does not
keep, and one direction where the new rule answers worse than the old.

## Spec compliance

The spec's S1 to S12 are each held by a case, and I checked the ones that
are code by mutation rather than by reading the phase records.

- **S1–S5, S8 hold and each case is the one that holds its property**
  (executed). I ran 20 mutants of `session_cost.py` one at a time against
  the #377 cases and the two older heredoc and `other`-note cases. Every
  mutant turned at least one case red, and each arm of the fallback case
  is killed by its own mutant. The list is under *Executed probes*.
- **S6 holds, and the fallback never answers worse than 2037cf0 through the
  fallback itself** (executed). Of about 95 shapes, the only ones where the
  tip says `other` and 2037cf0 says `git` are `git.exe` and `git-lfs` at
  the start of a line. That comes from the basename rule, not from the
  fallback (finding 5). Over the corpus, the 10 calls that leave `git` all
  go to `test`, which is the `FAMILIES` order the spec keeps.
- **S7 and Q2 hold** (read, then executed through `--json` by the existing
  case). `analyse` is called at four sites, in `measure_cycles`,
  `segment_slices` (twice) and `main`. Each one is handed `load`'s list or
  a slice of it, so every call dict carries `ran`. Nothing in
  `tests/` or `skills/` builds a call dict by hand.
- **`payload_meter.py` is untouched by the change** (read). It loads
  `session_cost.py` for `DELEGATING`, `spawn_labels`, `count` and
  `subagent_transcripts`, and none of the four changed.
- **S11 holds** (read). `unnamed`, both repeats groupings and `slowest` read
  the flattened `command`, and only the two `family` calls read `ran`.
- **S12 holds** (executed). `bin/evidence-check --strict`, unscoped, exits
  0: 2,480 ok, 0 drifted, 0 broken, 0 malformed.
- **0.9.4 S2's correction is exact** (read). The corrected clause says the
  body is removed up to its closing line and the operator cut applies only
  where no closing line follows, which is what the `family` docstring and
  the heredoc function's own docstring say the code does. The note keeps
  the lowercase-delimiter bound and states it unchanged, which is true of
  the pattern. What that bound now costs is finding 4.

The handoff's claim that the 2037cf0 fallback is *never worse* (ledger N2)
matches what I measured. Its claim that N4's `#` handling costs *one line*
reads as a family count; I measured 8 of the tip's 23 refusals as comments
holding an apostrophe, and none of the 8 changes family (executed, see
finding 2). The two readings agree if *costs* means a changed family.

## Quality

### 1. 🟡 A separator inside `$( … )` or `<( … )` puts the next word back in command position

`skills/verify/scripts/session_cost.py:270`, in `command_words`.

**What is wrong.** The `$(` branch sets the position to false for the
opening parenthesis only. The next separator inside the substitution sets
it back to true, so the word after it is yielded as a command word.

| Command | 2037cf0 | tip |
|---|---|---|
| `x=$(cd /y && git log -1)` | `other` | `git` |
| `diff <(cd a; git show) b` | `other` | `git` |
| `echo x \| tee >(cd a; git hash-object --stdin)` | `other` | `git` |
| `` echo `cd x; git s` `` | `other` | `git` |
| `echo "$(cd a; git show)"` | `other` | `other` |

**Why it matters.** Four places state the opposite as the rule:

- the `runs_git` docstring (line 293): *a command substitution is not a
  command position*;
- `skills/verify/SKILL.md:695`: *never a word inside quotes or inside
  `$( … )`*;
- the changelog fragment, line 8: *a word inside a command substitution …
  is not a command word*;
- ledger N1: *a word inside `$( … )`, `` ` `` or `<( … )` … is not a command
  word*.

The last row of the table is the other half. The docstring rejects counting
only unquoted substitutions because the family would then depend on quoting
nobody can see in the table. That is what the tip does whenever the
substitution holds a separator.

The measured size is small: one call in 23,553 moves when the fix below is
applied (executed). So the published figures stand, and what is wrong is a
rule stated in four places that the code keeps only for single-command
substitutions.

**The fix** tracks nesting from the `$(`, `<(` or `>(` that opens a
substitution, keeps every word inside out of command position, and lets only
what follows the outermost closing `)` reach the line. Applied in the clone,
`tests/test_session_cost.py` gave 114 passed, and over the corpus it moved
exactly the one call above (both executed, then reverted).

Backticks are not in the fix. A backtick token cannot be told from a quoted
one after `shlex` strips the quotes, and my attempt to track them turned 11
real `git` runs to `other` (every one of them a `grep -c '```'`). So the fix
narrows the backtick half of the sentence instead, in N1 and in the
changelog.

### 2. 🟡 A separator inside a `#` comment does the same, and there the tip answers worse than 2037cf0

`skills/verify/scripts/session_cost.py:265`, `lexer.commenters = ""`.

**What is wrong.** Turning the tokeniser's comment handling off keeps the
newline that ends a comment, which is why it was done. It also makes every
separator inside a comment a real separator.

| Command | 2037cf0 | tip |
|---|---|---|
| `# cd x && git push⏎ls` | `other` | `git` |
| `ls  # then; git push` | `other` | `git` |
| `# don't forget⏎git add a` | `other` | `other` (refused, then the pattern) |

**Why it matters.** The first two are the one direction the prompt asked
about: a line that runs no `git` is charged to `git`, where 2037cf0 said
`other`. The corpus holds none of them today (executed), so this is a shape
and not a published figure. The prompt's own list names *a comment line
`# git …`*, and the case that pins it (`# stage the record⏎git add a`) holds
no separator, which is why it passes.

**The fix** removes comments before the tokeniser sees the line. It follows
bash's rule: a `#` that begins a word, outside quotes. `a#b`, `${#x}`, `$#`
and `echo '#'` keep their `#` (executed). As a side effect, a comment holding
an apostrophe no longer reaches the tokeniser. Over the corpus, refusals go
from 23 to 15 and no call changes family (executed). The comment above
`lexer.commenters` and N4's note need one sentence each, fenced below.

### 3. ⬜ A here-string `<<< "…"` is cut as a heredoc

`skills/verify/scripts/session_cost.py:193`, `HEREDOC`.

`read a b <<< "$x"; git log` reads `other`. The pattern finds `<< "$x"`
inside `<<<`, finds no closing line, and cuts to the end, which drops the
`git log` on the same line. This pattern is unchanged by the branch, and
2037cf0 answers the same. It belongs to the class the branch repairs (a
command after a heredoc operator), which is why it is here. Over the
corpus, 43 calls hold `<<<` and none changes family when it is neutralised
(executed). A `(?<!<)` in front of the pattern and a `(?!<)` after the `<<`
would close it, if the smith takes it.

### 4. ⬜ A heredoc the pattern does not recognise now has its body read as command lines

`skills/verify/scripts/session_cost.py:184`.

`cat <<eof⏎git push⏎eof` and `cat <<\EOF⏎git push⏎EOF` read `git` at the
tip and `other` at 2037cf0. Flattening used to make the body's words
arguments of the first line. With the newlines kept, each body line is a
command line. The comment at line 184 is still true (*left classified as if
it were not one*), but the error it calls smaller is now a different error.
None of the corpus's multi-line calls with a lowercase or escaped delimiter
moves on this account (executed). A sentence saying so beside line 184 would
let the next reader find it.

### 5. ⬜ Shapes that now read against their bash meaning, none in the corpus

All executed as single shapes, and none moves a call in the corpus:

- `git.exe status` and `git-lfs pull` at the start of a line were `git` and
  are `other`. The basename must equal `git` or `gh`.
- `case x in a) git s;; esac` and `function f { git s; }` are `other`,
  because a case arm's `)` and a `{` after a function name do not put the
  next word in command position.
- `>out git status` and `cd x && 2>/dev/null git s` are `other`, because a
  leading redirection is read as a command word's place.
- `x=(git s)`, an array assignment, is `git`.

The wrapper bound (`env`, `sudo`, `command`, `exec`, `nohup`, `xargs`) is
stated in the `runs_git` docstring and behaves as stated.

## Regression tests to plant

Destination `tests/test_session_cost.py`, beside the #377 cases. The first
three shapes of the first case and the first three of the second answer
wrongly at the target SHA and correctly with the fixes applied (executed as
`family` calls on both modules; the cases themselves were not planted).

```python
def test_a_separator_inside_a_substitution_does_not_reach_the_line():
    """A command substitution is not a command position, and neither is any
    word inside one: a separator inside `$( … )` or `<( … )` separates the
    substitution's commands, not the line's. What follows the closing `)`
    is the line's again."""
    module = load_script()
    for command in (
        "x=$(cd /y && git log -1)",
        "diff <(cd a; git show) b",
        "echo x | tee >(cd a; git hash-object --stdin)",
    ):
        assert module.family(command) != "git", command
    for command in ("echo $(git a); git b", "echo $(( 1 + 2 )); git s"):
        assert module.family(command) == "git", command


def test_a_comment_runs_nothing_whatever_it_holds():
    """A `#` that begins a word starts a comment to the end of its line, so a
    separator inside one separates nothing. A `#` inside a word or inside
    quotes starts no comment, and a comment's apostrophe is not a quote."""
    module = load_script()
    for command in ("# cd x && git push\nls", "ls  # then; git push"):
        assert module.family(command) != "git", command
    for command in (
        "# don't forget\ngit add a",
        "echo '#'; git s",
        "echo a#b; git s",
        "echo ${#x}; git s",
    ):
        assert module.family(command) == "git", command
```

## Facts for the evidence ledger

- Over the 358 transcripts under `~/.claude/projects/*SpecSeal*/` on
  2026-09-28 (23,553 Bash calls), findings 1 and 2's fixes together move one
  call, from `git` to `other`. The tokeniser refuses 23 lines at the tip and
  15 with comments removed. None of the 8 refusals a comment caused changes
  family. This bears on N4's note (executed).
- N1's sentence *a word inside `$( … )`, `` ` `` or `<( … )` … is not a
  command word* is false at the target SHA for a substitution holding a
  separator. It becomes true for `$(`, `<(` and `>(` with finding 1's fix
  and stays false for backticks (executed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a separator inside `$( … )`, `<( … )` or `>( … )` puts the next word in command position, against the rule four sentences state | `skills/verify/scripts/session_cost.py:270` | open | executed: 3 shapes read `git` at the tip and `other` at 2037cf0; the fix moves 1 of 23,553 corpus calls |
| 🟡 2 | a separator inside a `#` comment puts the next word in command position, where 2037cf0 answered `other` | `skills/verify/scripts/session_cost.py:265` | open | executed: 2 shapes worse than 2037cf0; 0 corpus calls; the fix cuts refusals 23 → 15 with no family change |
| ⬜ 3 | a here-string `<<< "…"` is cut as a heredoc, dropping the rest of the line | `skills/verify/scripts/session_cost.py:193` | open | executed: same answer as 2037cf0; 43 corpus calls, none moves |
| ⬜ 4 | a heredoc with a lowercase or escaped delimiter now has its body lines read as commands | `skills/verify/scripts/session_cost.py:184` | open | executed: 2 shapes worse than 2037cf0; no corpus call moves on this account |
| ⬜ 5 | `git.exe`, `git-lfs`, a case arm, a function body after `function f`, a leading redirection and an array assignment read against their bash meaning | `skills/verify/scripts/session_cost.py:282` | open | executed as shapes; none in the corpus |
| 🟢 | every #377 case is the one that holds its property | `tests/test_session_cost.py:1572` | confirmed | executed: 20 mutants, each killed by at least one case |
| 🟢 | the fallback never answers worse than 2037cf0's anchored rule | `skills/verify/scripts/session_cost.py:282` | confirmed | executed: about 95 shapes and the corpus; the only regressions are finding 5's basename shapes |
| 🟢 | both family sites read `ran`, and every call dict reaches `analyse` through `load` | `skills/verify/scripts/session_cost.py:722` | confirmed | read: four callers, each a slice of `load`'s list; executed through the `--json` case |
| 🟢 | 0.9.4 S2's correction states what the code does | `seal/releases/0.9.4.md:32` | confirmed | read against the `family` docstring and the heredoc function |
| 🟢 | the ledger has no drifted or broken row | `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md` | confirmed | executed: `bin/evidence-check --strict` unscoped, exit 0, 2,480 ok |
| ❓ | how the 0.15.5 run's own segment readings move | `questions.md` Q1 | ❓ out of verified scope | the transcripts are on another machine; the owner answers it, as `overview.md` already records |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| how the 0.15.5 run's segment readings move (Q1) | `overview.md` §*Not verified* | the owner, on the machine that holds the 0.15.5 transcripts |

## Paste-ready fixes

### 1

In `command_words`, replace the loop head and the punctuation branch:

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

The backtick half of the rule, in ledger N1's clause and in the changelog
fragment's first bullet, narrowed to what the code keeps:

```text
N1: … A word inside quotes, inside `$( … )` or `<( … )`, or behind a wrapper
is not a command word, and neither is a backtick substitution's first word. …

changelog: … A word inside quotes, inside `$( … )` or behind a wrapper such
as `timeout` is not a command word, so `grep -rn git`, `cat .git/config` and
`echo 'a; git b'` stay out. …
```

### 2

Above `command_words`:

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

In `command_words`, the lexer and the comment above `lexer.commenters`:

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

Ledger N4's note, its last sentence:

```text
`#` is an ordinary character to the tokeniser instead, and comments are
removed before it by bash's rule (a `#` that begins a word, outside quotes),
so a comment holding a separator or an apostrophe reaches neither the
command words nor the refusal.
```

Needs a fix: yes — findings 1 and 2: a separator inside a substitution or a
comment is read as the line's, against the rule four sentences state

Loses a record or crashes: no

## Proof block

Files opened in this round, at the target SHA in the clone unless named:

- `skills/verify/scripts/session_cost.py` (the diff; lines 100–330, 495–580, 632–775 and 2149–2175; `payload_meter.py`'s use of it)
- `skills/verify/scripts/payload_meter.py` (lines 134–160, 375–445)
- `skills/verify/SKILL.md` (lines 640–706)
- `tests/test_session_cost.py` (the diff; `load_script`, `call`)
- `docs/measuring-a-run.md` (lines 55–95)
- `README.md`, `README.ko.md` (the `session-cost` rows)
- `seal/releases/0.9.4.md` (the diff)
- `seal/ledger/1790550714-a-git-call-after-cd-is-charged-to-git.md`
- `seal/specs/1790550714-a-git-call-after-cd-is-charged-to-git/spec.md`, `questions.md`, `changelog.md`
- `bin/test`
