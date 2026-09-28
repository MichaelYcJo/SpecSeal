# 1790562541-reading-is-charged-to-a-read-family — review round 1

| Field | Value |
|---|---|
| Target SHA | 0ba4263447ccb168ed4a263eae083c8d528b7484 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #651 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1 (a hidden command is charged to `read`), 🟡 2 (three options that write or run), 🟡 3 (the program bound is unstated and contradicts the admission criterion) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 of work item 1790562541 (#642), a first round against the whole branch `fix/642-reading-is-charged-to-a-read-family` at 0ba42634, base origin/release/v0.15.7 (d71265b9, which carries #637), draft PR #651. Judge spec compliance against spec.md first (In §1–§4, the owner's read-only answer, #635's four findings), including the five places the build diverged from the spec (case/esac out of the neutral words, hidden forms by text match, `read` judged on the recorded text, GNU long-option prefixes, three guards removed as equivalent mutants so `cat f >` now reads as `read`) and whether each holds. Then quality. The class to enumerate: every shape of a Bash line that WRITES, deletes or runs something while every command word on it is a read or neutral word (redirections in every spelling, in-place flags, `-exec`, `tee`, `xargs`, subshells, functions, aliases, `eval`, a here-string, a pipe into a writer), each of which must stay out of `read`, and every place a published sentence or test states which families exist. Probe on real command lines, not only fixtures.

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

## Paste-ready fixes

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
```
📋 code-review applied
· spec:     seal/specs/1790562541-reading-is-charged-to-a-read-family/spec.md In §1–§4, Scope, Decided, S1–S13; overview.md; questions.md Q1–Q5; survivors.md; phases/phase-2.md; changelog.md; seal/ledger/1790562541-reading-is-charged-to-a-read-family.md R1–R7; seal/releases/0.15.6.md N1–N3 diff
· compared: skills/verify/scripts/session_cost.py:116-143, 200-495, 498-680, 983-1010, 1060-1146, 2003-2020, 2583-2597; skills/verify/SKILL.md:700-736; tests/test_session_cost.py diff (1571-1665, 1708-1729, 1825-2010, 3051-3066); skills/code-review/scripts/round_record.py:420-440
· verdict:  🔴 1 · 🟡 2 · 🟢 7 · ❓ 1
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
