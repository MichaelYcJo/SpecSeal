# Round 1 report — reading is charged to a `read` family (#642)

Target: `fix/642-reading-is-charged-to-a-read-family` at 0ba42634, against
origin/release/v0.15.7 (d71265b9). First round; no earlier round exists, so
nothing is carried.

## How the findings relate

Stage 1 holds: the five divergences stand, #635's four findings are in, and
the owner's answer is mechanical. Stage 2 found one cause with three faces,
all in `only_reads` and `writes`:

```
the rule charges a line `read` when every command it SEES only reads
  ├─ 1  a command the walk never puts in command position is not seen
  │      (bash leading redirection, zsh short forms and `always`, bash 5.3 `${ …; }`)
  ├─ 2  an option that makes a read word write or run is not refused
  │      (`sed -I`, `rg --pre`, `sort --compress-program`)
  └─ 3  a program that writes or runs is not seen, and the bound says less than it is
         (`sed` e/W, `awk` system()/pipes)
```

Each is a write or a run charged to `read`, which the spec's grounding row
from #200 names the worse error. None moves a call in this machine's corpus
today (0 of 24,303), so the published figures stand; what is wrong is the
rule and the sentences that describe it.

## Stage 1 — spec compliance

**The five divergences each hold (read, and executed where noted).**

- `case`/`esac` out of the neutral words. `case $x in a) rm f;; esac; ls`
  is `other` and pinned. Keeping them would have been exactly finding 1's
  shape. Holds.
- Hidden forms by text match. `"$(ls)"` reaches the walk as `$_ls_`, so the
  walk alone cannot see it; the match errs toward `other`
  (`grep -r '<<' docs` is `other`, executed). Command words still come from
  the one walk. Holds.
- `read` judged on the recorded text. `without_heredoc_bodies` cuts a
  here-string's `<<<`, and the here-string arm pins the choice. Holds.
- GNU long-option prefixes. `abbreviates` requires three characters, so
  `--` stays the end of options. Holds, and it is where finding 2's class
  begins: the build widened the spelling of the options it knew and did
  not ask which other options write or run.
- Three guards dropped as equivalent mutants. The phase-2 record names two
  and the overview a third. (a) An operator right after a redirection fails
  the target test anyway. (b) A redirection with no target is a syntax
  error: `cat f >` is `read`, and bash and zsh both refuse it before running
  anything, so nothing is mischarged. (c) Round 3's `end < len(command)`:
  a join on the last line ends the walk unclosed, which is what a failed
  comparison does, and no delimiter the pattern admits ends in `\`. All
  three hold.

**#635's four findings are in.** Finding 1's join is pinned, and I asked
the shells directly: zsh 5.9, bash 3.2 and sh all print `body EOF` for
`cat <<EOF⏎body \⏎EOF⏎echo …⏎EOF` (executed). That closes the overview's
*Not verified* row for this machine. It matters more than the row says: the
harness here runs zsh, not bash (`$ZSH_VERSION` is 5.9 in a Bash call,
executed). Finding 2's two examples read `git` as the new docstrings say
(executed). Findings 3 and 4 carry dated `Corrected` notes (read).

**The owner's answer is mechanical.** Any `<<` keeps a line out, and the
`python3 -` arm stays `other` (read, pinned).

## Stage 2 — quality

### 🔴 1 — A command the walk never reaches is charged to reading

`skills/verify/scripts/session_cost.py:604` (`only_reads`), with the claim
at `:483`.

The rule collects each command's arguments and appends every word after a
command word to that command (`:635`). A word the walk does not put in
command position is therefore read as the previous command's argument, and
the line is judged by the command before it. Three shapes reach that:

| Shape | Example, charged `read` at 0ba42634 | How it was established |
|---|---|---|
| bash leading redirection after a separator, or first in a subshell or line | `ls; >/dev/null rm -rf x`, `ls && >/dev/null rm -rf x`, `ls;>/dev/null rm -rf x`, `</dev/null rm x; ls`, `(>/dev/null rm x); ls`, `cat f⏎</dev/null python3 build.py` | executed, the rule |
| zsh short forms and `always` blocks | `if [[ -f a ]] rm a; ls`, `if [[ -f a ]] { rm a }; ls`, `{ ls; } always { rm a; }` | executed: zsh 5.9 deleted the file in each, and the rule says `read` |
| bash 5.3 `${ cmd; }` | `cat ${ rm x; }` | the rule executed; bash 5.3's behaviour read, not run (no 5.3 here) |

Why it matters. The spec's In §1 says a call is `read` when every command
it runs only reads, and its grounding row says a write is never `read`.
The build's own docstring at `:483` claims *`only_reads` walks the same words
and meets the same four bounds, each turned toward `other`*. The
leading-redirection bound is the third of `runs_git`'s four, and it is
turned toward `read`. The pinned case `<f cat` passes only because nothing
precedes it; put any read word first and the hidden command disappears.

The zsh shapes are not exotic here: the harness on the machine #642
measured runs zsh, so the walk models a grammar that is not the one
executing the calls.

The fix keeps each shape out rather than modelling it, which is the
direction the file already takes. A redirection before a command's first
word, and an operator token that glues a separator to one, keeps the line
out; so does a `[[` with words after its `]]`, a bare `{` or `}` argument,
and `${` followed by a space or `|`. The new pattern it adds for the glued
token is `LEADING_SEPARATOR` (NAME NOT IN TREE). Executed in a scratch
clone: the probe shapes all go to `other`; `(cd /x && ls) 2>/dev/null`,
`{ ls; } 2>/dev/null`, `ls &>/dev/null`, `cat ${f:-x}` and
`[[ -f x ]] && cat x` stay `read`; `bin/test tests/test_session_cost.py` is
140 passed with exit 0; ruff check and format exit 0; and over 24,303 corpus
calls no call changes family.

### 🟡 2 — Three options that make a read word write or run are not refused

`skills/verify/scripts/session_cost.py:578` (`writes`), `:590`.

- `sed -I` is the BSD and macOS in-place edit. On darwin, `sed -I ''
  s/a/b/ f` rewrote the file (executed). `writes` tests `"i" in word`, which
  is case-sensitive, so `sed -I '' s/a/b/ f` and `sed -I.bak s/a/b/ f` are
  `read`. This machine is darwin.
- `rg --pre CMD` runs `CMD` on every file it searches. `rg --pre ./x.sh
  pat` is `read` (executed, the rule).
- `sort --compress-program=PROG` runs `PROG`. `sort
  --compress-program=sh f` is `read` (executed, the rule).

Why it matters. `READ_WORDS`' comment (`:498`) admits a word only when *the
option that makes it write a file is one `writes` refuses*. These three are
such options, and #642's §12 note was that the spelling of an option is a
class. The fix adds them to `writes`. It moves no corpus call (executed).

### 🟡 3 — A program that writes or runs is `read`, and the stated bound is narrower than the gap

`skills/verify/scripts/session_cost.py:584` (`writes`' docstring) and
`:498` (`READ_WORDS`' comment); the ledger fragment's R2 note says the same.

The docstring names two bounds, `sed`'s `w` and `awk`'s `print > "f"`. Six
more shapes are `read` at 0ba42634 (executed, the rule):
`sed -n '1e touch y' f`, `sed 's/.*/rm -rf x/e' f`,
`sed 's/x/y/w out' f`, `awk 'BEGIN{system("rm -rf x")}'`,
`awk '{print | "sh"}' f` and `awk '{print > "out"}' f`.

Why it matters. A reader who meets `awk 'BEGIN{system(...)}'` in a `read`
row finds a docstring listing two writes and nothing that runs. The
admission criterion is also contradicted by two of its own words. `sed` and
`awk` can write through their programs, so neither has standard output as
its only output. Nothing records that they were admitted under a bound, so
the next word is judged by a criterion the list itself breaks. Reading the
program is an unbounded enumeration, so the fix states the limit rather than
chasing it, per `code-review`'s *Verdicts that close too early*.

### ⬜ 4 — The published neutral-word list is short, and three of its words are not loop words

`skills/verify/SKILL.md:726` says *a word that touches no file (`cd`,
`echo`, `test` and the loop words)*. The changelog fragment (`:16`) gives
a longer list. Both omit `pwd`, `pushd`, `popd`, `true`, `:`, `[[` and `}`,
and `fi`, `}` and `[[` are not loop words. The behaviour is right and a
reader can still act on the sentence, so this is a note. Writing *for
example* before the list, or naming `NEUTRAL_WORDS`, would make it true.

### ❓ — The `read` row prints beside the `Read` tool's row

The meter's `by family` block keys a non-Bash call by its tool name, so a
reading now carries both `read` (Bash calls that read) and `Read` (the
`Read` tool). On a real transcript the block printed `read 29 calls` and,
eleven rows below, `Read 1 calls` (executed). `--json`'s `by_family` holds
both keys. The frame weighed the name against the `verify` label `read` and
not against this row. The name is the owner's decision (`questions.md`),
so this is a question for the owner and not a finding.

## Regression tests to plant

All in `tests/test_session_cost.py`. Every shape in the first two rows was
`read` at 0ba42634 by this round's probe, so each is red against the
branch.

| Case | Add |
|---|---|
| `test_what_the_walk_cannot_see_is_not_read` | `ls; >/dev/null rm -rf x`, `ls && >/dev/null rm -rf x`, `ls;>/dev/null rm -rf x`, `ls&&>/dev/null rm x`, `</dev/null rm x; ls`, `(>/dev/null rm x); ls`, `ls; >&2 rm x`, `cat f\n</dev/null python3 build.py`, `if [[ -f a ]] rm a; ls`, `if [[ -f a ]] { rm a }; ls`, `{ ls; } always { rm a; }`, `{ ls } always { rm b }`, `cat ${ rm x; }` |
| `test_a_write_is_never_read` | `sed -I '' s/a/b/ f`, `sed -I.bak s/a/b/ f`, `rg --pre ./x.sh pat`, `rg --pre=sh pat`, `sort --compress-program=sh f` |
| `test_a_call_that_only_reads_is_charged_to_read` (controls, so the fix cannot over-reach) | `(cd /x && ls) 2>/dev/null`, `{ ls; } 2>/dev/null`, `(ls)>/dev/null`, `ls &>/dev/null`, `cat ${f:-x}`, `[[ -f x ]] && cat x` |

The controls pass before and after. Each is seen red through a mutant that
returns `other` on every redirection, which the smith runs.

## Facts for the evidence ledger

- The Bash tool on this machine runs zsh 5.9, not bash. Executed:
  `$ZSH_VERSION` printed 5.9 inside a Bash call. The heredoc join R5 rests
  on holds in zsh 5.9, bash 3.2 and sh (executed). This belongs in R5's note.
- R3's clause lists what is hidden from the walk. Once finding 1 lands it
  gains a leading redirection, zsh's short forms and `always` blocks, and
  `${ …; }`.
- R2's note gains finding 2's options and finding 3's full bound.
- `runs_git`'s docstring carries finding 1's corrected sentence. Every
  0.15.6 row anchored on `runs_git` drifts, and `evidence-check` names them.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A command the walk never puts in command position is read as the previous command's argument, so a line that runs `rm` or `python3` is `read`: bash leading redirection, zsh short `if`/`always` forms, bash 5.3 `${ cmd; }`; the `runs_git` docstring claims all four bounds turn toward `other` | `skills/verify/scripts/session_cost.py:604`, `:483`, `:635` | open | Executed: 13 shapes are `read` at 0ba42634, and zsh 5.9 deleted the file in each zsh shape. Spec In §1 and the grounding from #200 say a write is never `read`. The paste-ready fix passes the module (140) and moves 0 of 24,303 corpus calls |
| 🟡 2 | `writes` does not refuse `sed -I` (BSD/macOS in-place), `rg --pre` or `sort --compress-program`, so each is `read` | `skills/verify/scripts/session_cost.py:578`, `:590` | open | Executed: darwin `sed -I ''` rewrote a file; the rule returns `read` for all five spellings. `READ_WORDS`' criterion requires such options to be refused |
| 🟡 3 | `sed` `e`/`W`/`s///e` and `awk` `system()`/`print \|`/`getline` are `read`, the `writes` docstring states only `w` and `print >`, and sed and awk are admitted against the criterion `READ_WORDS`' comment states | `skills/verify/scripts/session_cost.py:584`, `:498` | open | Executed: six program shapes are `read`. Unbounded domain, so the fix states the bound rather than parsing programs |
| ⬜ 4 | The published neutral-word list reads as complete and calls `fi`, `}` and `[[` loop words | `skills/verify/SKILL.md:726` | open | Read. Behaviour is right; the sentence is imprecise |
| 🟢 | Divergence: `case`/`esac` out of the neutral words | `skills/verify/scripts/session_cost.py:527` | verified | Read and pinned; keeping them would be finding 1's shape |
| 🟢 | Divergence: hidden forms found by text match | `skills/verify/scripts/session_cost.py:553` | verified | Read; errs toward `other`, executed on a quoted `<<` |
| 🟢 | Divergence: `read` judged on the recorded text | `skills/verify/scripts/session_cost.py#family` | verified | Read; the here-string arm pins it |
| 🟢 | Divergence: GNU long-option prefixes | `skills/verify/scripts/session_cost.py#abbreviates` | verified | Read; `--` stays the end of options. Finding 2 is the class beside it, not a defect in it |
| 🟢 | Divergence: three guards dropped as equivalent mutants; `cat f >` is `read` | `skills/verify/scripts/session_cost.py:604`, `#without_heredoc_bodies` | verified | Read. A target-less redirection is refused by bash and zsh before anything runs; the join guard's removal cannot close a body |
| 🟢 | #635 finding 1: the heredoc body join | `skills/verify/scripts/session_cost.py#without_heredoc_bodies` | verified | Executed in zsh 5.9, bash 3.2 and sh: the continued line closes nothing |
| 🟢 | #635 findings 2–4: bound directions, the #377 overview and N2 corrected | `skills/verify/scripts/session_cost.py:300`, `seal/releases/0.15.6.md` | verified | Executed: both examples read `git`; the dated notes read |
| ❓ | The `read` family row prints beside the `Read` tool row in one table and one `by_family` object | `skills/verify/scripts/session_cost.py:2003` | ❓ out of verified scope | Executed on a real transcript; whether to keep the name is the owner's decision, which the frame did not weigh against this row. The owner answers it |

## Executed probes

| What was run | Result |
|---|---|
| Class probe, 66 shapes through `family` at 0ba42634, in a scratch clone | 13 hidden-command shapes, 5 option shapes and 6 program shapes are `read`; every redirection spelling into a file, `tee`, `xargs`, `eval`, functions, aliases, `trap`, `exec`, `command`, `&`, subshell and brace-group redirections, here-strings and pipes into `sh` are `other` |
| zsh 5.9 running `if [[ -f a ]] { rm a }; ls`, `if [[ -f b ]] rm b; ls`, `{ ls; } always { rm a; }`, `{ ls } always { rm b }` | each deleted its file, exit 0 |
| darwin `sed -I '' s/a/b/ f` | exit 0, the file rewritten to `b` |
| heredoc join `cat <<EOF⏎body \⏎EOF⏎echo …⏎EOF` in zsh 5.9, bash 3.2, sh | each printed `body EOF` and the next line |
| which shell a Bash call runs | `ZSH_VERSION=5.9`, process `/bin/zsh` |
| corpus family counts at 0ba42634, 375 transcripts, 24,271 Bash calls | git 6,476 · read 7,825 · other 6,010 · test 3,452 · lint/type 456 · build 52; consistent with the smith's 7,819 over 374 |
| corpus differential, branch rule against the paste-ready fixes, 24,303 calls | 0 calls change family |
| `bin/test tests/test_session_cost.py` with the paste-ready fixes applied in the clone | 140 passed, exit 0 |
| ruff check and ruff format --check on the patched `session_cost.py` | exit 0, exit 0 |
| `session_cost.py` at 0ba42634 on a real transcript | `by family` printed `read 29 calls` and `Read 1 calls` as separate rows |
| #635's examples `x="$(echo "; git log")"` and `echo $(ls)#'⏎git push'` | both `git`, as the docstrings now say |
| `bin/test` over the branch's own modules at 0ba42634 | not run by this round; the caller's 260 passed is carried as the caller's, not re-run |
| full suite, repository-wide lint and typecheck | not yet; the sealer's, once the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

## Unverified

| Item | Who answers it |
|---|---|
| bash 5.3's `${ cmd; }` running `cmd` (no bash 5.3 on this machine; read from its manual) | the smith, on a machine with bash 5.3, or by accepting the conservative pattern as it stands |
| the heredoc join in a Linux bash | the smith, if a Linux reading matters; POSIX states the same join |

## Paste-ready fixes

### Finding 1 — keep a hidden command out

```python
# session_cost.py, beside HIDDEN_FROM_THE_WALK
# What the walk cannot see into: a heredoc or here-string operator, a command
# or arithmetic substitution, a backtick, a process substitution, and bash
# 5.3's `${ … }` and `${| … }`, which run their commands in the current
# shell. Matched on the text anywhere, a quoted or commented one included,
# because the side that errs is `other`.
HIDDEN_FROM_THE_WALK = re.compile(r"<<|\$\(|`|<\(|>\(|\$\{[\s|]")

# An operator token that ends one command and opens a redirection before the
# next one's first word, glued by the tokeniser: `;>`, `&&>`, `|<`, `(>`.
# `&>` alone is not one, because bash reads it as a redirection of its own.
LEADING_SEPARATOR = re.compile(r"(?:[;|\n(]|&&)+&?[<>]")  # NAME NOT IN TREE
```

```python
# only_reads, the walk and the judgement
    commands, redirect, started = [], None, False
    try:
        for kind, token in shell_words(command):
            if redirect is not None:
                harmless = token == "/dev/null" or (
                    redirect.endswith(">&") and (token.isdigit() or token == "-")
                )
                if not harmless:
                    return False
                redirect = None
            elif kind == "command":
                commands.append([token])
                started = True
            elif kind == "operator":
                if set(token) & REDIRECTION:
                    # A redirection before a command's first word keeps that
                    # word out of command position (`runs_git`'s third
                    # bound), so what the command runs is never seen:
                    # `ls; >/dev/null rm -rf x`. Here the bound keeps the
                    # line out, as the other three do.
                    if not started or LEADING_SEPARATOR.match(token):  # NAME NOT IN TREE
                        return False
                    redirect = token if ">" in token else None
                else:
                    started = not (set(token) & SEPARATOR)
            elif commands:
                commands[-1].append(token)
    except ValueError:
        return False
    reads = False
    for word, *arguments in commands:
        name = word.replace("\\", "/").rsplit("/", 1)[-1]
        if (name == "[[" and "]]" in arguments[:-1]) or {"{", "}"} & set(arguments):
            # zsh runs what follows `]]` as the body of a short `if` or
            # `while` (`if [[ -f a ]] rm a`), a brace group after one, and
            # an `always` block after a closing `}` (`{ ls } always { rm
            # a }`). The walk models bash and reads each as arguments, so the
            # command in it is never seen, and the line keeps out.
            return False
        if name in READ_WORDS and not writes(name, arguments):
            reads = True
        elif name not in NEUTRAL_WORDS:
            return False
    return reads
```

```text
runs_git's docstring, replacing its last paragraph:

    `only_reads` walks the same words and meets the same bounds, each
    turned toward `other` because a write charged to reading is the worse
    error (#642): a substitution keeps the line out rather than being read
    past, a wrapper is not a neutral word, a `case` is not one either
    because its arms' commands are never in command position, a leading
    redirection keeps the line out because the command after it is never
    seen, and a refused line is `other` with no pattern to fall back to.
    The harness runs the user's shell, zsh on the machine #642 measured,
    and zsh's short `if [[ … ]] cmd` and `always` blocks hide a command
    the same way, so `only_reads` keeps those out as well.
```

Precondition: none beyond the module's own; the fix reads no file and calls
no process.

### Finding 2 — the options that write or run

```python
    for word in arguments:
        short = word.startswith("-") and not word.startswith("--")
        if name == "sed" and (
            (short and ("i" in word or "I" in word)) or abbreviates(word, "--in-place")
        ):
            return True
        if name == "sort" and (
            (short and "o" in word)
            or abbreviates(word, "--output")
            or abbreviates(word, "--compress-program")
        ):
            return True
        if name == "rg" and (word == "--pre" or word.startswith("--pre=")):
            return True
        if name == "find" and word in FIND_WRITES:
            return True
        if name == "awk" and (word.startswith("-i") or abbreviates(word, "--include")):
            return True
    return False
```

`rg` parses long options with no abbreviation, so `--pre` is matched exactly.

### Finding 3 — state the bound the programs leave

```python
def writes(name, arguments):
    """Whether a read word's arguments make it write a file.

    `sed -i` in every spelling (`-i.bak`, `-ni`, `--in-place`, `--in`), and
    the BSD and macOS `-I`, with a single-dash word read wholesale, so
    `sed -es/a/i/ f` counts too; `sort`'s `-o` and `--output`, and its
    `--compress-program`, which runs the program it names; `rg --pre`, which
    runs its command on every file; `find`'s `FIND_WRITES`; and
    `awk -i inplace` or `--include`.

    What sits inside a quoted program is a bound, because the walk cannot
    read it, and it is a bound in both directions it can fail: a `sed`
    script's `w` and `W` commands and `w` flag write a file, its `e` command
    and `e` flag run one, and an `awk` program's `print > "f"`, `print |
    "cmd"`, `"cmd" | getline` and `system()` write or run. Each is `read`."""
```

```python
# The words that make a line `read` (#642), by basename. A word is admitted
# when its only output is standard output, or when every option that makes
# it write a file or run a program is one `writes` refuses. `sed` and `awk`
# are admitted under a stated bound: their programs can write and run, the
# walk cannot read a quoted program, and `writes` says which commands do.
# These thirteen are the list #642 measured, so its numbers can be set beside
# the ticket's; the next word is added by that criterion, with a count behind
# it, and `tee`, which writes the files it is given, never can be.
```

Needs a fix: yes — 🔴 1 (a hidden command is charged to `read`), 🟡 2 (three options that write or run), 🟡 3 (the program bound is unstated and contradicts the admission criterion)
Loses a record or crashes: no

```
📋 code-review applied
· spec:     seal/specs/1790562541-reading-is-charged-to-a-read-family/spec.md In §1–§4, Scope, Decided, S1–S13; overview.md; questions.md Q1–Q5; survivors.md; phases/phase-2.md; changelog.md; seal/ledger/1790562541-reading-is-charged-to-a-read-family.md R1–R7; seal/releases/0.15.6.md N1–N3 diff
· compared: skills/verify/scripts/session_cost.py:116-143, 200-495, 498-680, 983-1010, 1060-1146, 2003-2020, 2583-2597; skills/verify/SKILL.md:700-736; tests/test_session_cost.py diff (1571-1665, 1708-1729, 1825-2010, 3051-3066); skills/code-review/scripts/round_record.py:420-440
· verdict:  🔴 1 · 🟡 2 · 🟢 7 · ❓ 1
```
