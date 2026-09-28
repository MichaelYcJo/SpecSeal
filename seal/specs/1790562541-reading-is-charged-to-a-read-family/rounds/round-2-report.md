# 1790562541-reading-is-charged-to-a-read-family — review round 2 report

Round 2 is the verifying round. Its target is the diff of round 1's fixes,
7be42f52..72ca4827 (078b4413 code, cases, SKILL and records; 4e214176 two
pins; 14c46eaf ledger and overview; 72ca4827 one survivor sentence), with the
branch at ea0d41a9 and draft PR #651. It answers each closed verdict of
`round-1.md` and judges as code what nobody has reviewed: the new unit
`SEPARATOR_THEN_REDIRECTION`, the widened `writes`, the stated sed/awk
program bound and the six over-blocking controls. Probes ran in a scratch
clone at ea0d41a9, in zsh 5.9 (the shell the Bash tool runs here) and in
bash 3.2.

## How the findings relate

Every shape round 1 named is now `other`, and each fix does what its commit
says. What remains is three members of round 1's own classes that the fix
did not reach:

- Round 1's 🔴 1 (a command hidden from the walk) has two members left.
  They sit at two depths, so they are written as two findings:
  - finding 1 is a leading redirection after a background `&`. It is inside
    the new unit `SEPARATOR_THEN_REDIRECTION` (depth 1).
  - finding 2 is zsh's short forms closed by `))` or by a `for` list's `)`.
    It is inside `only_reads`, which existed before the fix (depth 0).
- Round 1's 🟡 2 (an option that runs a program) has one member left,
  `rg --hostname-bin` (finding 3, in `writes`).

Each of the three is a line that runs `rm` or a named program, and
`session-cost` charges it to `read`. Spec In §1 says a write is never
`read`, and round 1 graded that consequence 🔴.

## Findings

### 🔴 1 — A leading redirection after a background `&` is still `read`

`skills/verify/scripts/session_cost.py:566`, `SEPARATOR_THEN_REDIRECTION`.

The pattern requires the glued separator run to begin with `;`, `|`, a
newline, `(` or `&&`. A single background `&` never starts one, so a
redirection glued to it passes the check. `started` is still true from the
command before it, so the redirection is taken as that command's, and the
command after it rides along as an argument. Executed at ea0d41a9:

| Line | family | zsh 5.9 | bash 3.2 |
|---|---|---|---|
| `ls &</dev/null rm x` | `read` | deleted `x` | deleted `x` |
| `ls &⏎>/dev/null rm x` | `read` | deleted `x` | deleted `x` |
| `ls &⏎</dev/null rm x` | `read` | not run | not run |
| `ls &\|>/dev/null rm x` | `read` | deleted `x` | syntax error, nothing ran |

The spaced form `ls & >/dev/null rm x` is `other`, and so are `|&>`, `||>`,
`;&>` and `⏎&>`. Only the glued `&` escapes.

The fix lets a lone `&` begin the run when it is not the `&` of `&>` or of
`&&`: `&(?![>&])`. That keeps `ls &>/dev/null` `read`, and it is the one
control this unit needs. The unit's comment and `runs_git`'s docstring say
that a leading redirection keeps the line out. At ea0d41a9 that is not true
of these lines, and it becomes true with the fix.

### 🔴 2 — zsh's short forms closed by `))` or by a `for` list's `)` still hide a command

`skills/verify/scripts/session_cost.py:646-678`, `only_reads`.

The fix recognises zsh's short `if` by a `[[` with words after its `]]`.
The zsh manual gives `(( … ))` as the other delimiter for the same short
forms, and zsh also has a short `for name (words) cmd`. In both, the word
after the closing `)` is the body. The walk reads it as an argument of the
last command, and that command is the first word inside the parentheses.
When that word is a read or neutral word, the line is `read`. Executed at
ea0d41a9:

| Line | family | zsh 5.9 | bash 3.2 |
|---|---|---|---|
| `if (( ! true )) rm a; ls` | `read` | deleted the file | syntax error |
| `while (( ! true )) rm a; ls` | `read` | not run | not run |
| `for f (ls) rm $f; ls` | `read` | deleted the file | syntax error |
| `if (( ! true )) 2>/dev/null rm a; ls` | `read` | deleted the file | syntax error |

Reaching it takes an arithmetic expression or a word list whose first word
is one of the thirty read and neutral words. The corpus holds none,
because the differential below moves no call. The consequence is still the
one 🔴 1 was graded for, in the shell the harness runs.

The fix works on the walk and not on text. bash refuses a word after a
closing `)`, and zsh runs it. So after an operator ending in `)`, any
argument word keeps the line out. Two kinds of word are exempt: a
descriptor number (`(cd /x && ls) 2>&1`) and a redirection's target
(`(ls) <f`). Each exemption has a control, and the mutant that drops it is
killed.

One pin moves with the fix. `") x"` pinned the `elif commands:` guard, and
under the fix the new branch returns before that guard is reached. `") 2"`
reaches the guard, and it raises `IndexError` without the guard (executed),
so the pin should become that case.

### 🟡 3 — `rg --hostname-bin` runs its program and is `read`

`skills/verify/scripts/session_cost.py:620`, `writes`.

`READ_WORDS`' comment now states the criterion: every option that makes a
word write a file or run a program is one `writes` refuses. ripgrep has two
options that take a command, `--pre` and `--hostname-bin`, and the fix
refuses only `--pre`. Executed with ripgrep 14.1.1: `rg --hostname-bin=./hb
pat f` ran `./hb` with no hyperlink flag, with `--hyperlink-format=default`,
and with `--color=always`. The family of that call is `read`.

The other twelve read words were checked for an option that runs a
program, by reading their man pages on this machine. Only `sort
--compress-program` and `find`'s actions turned up, and both are already
refused. The fix adds `--hostname-bin` in both spellings beside `--pre`.

## Answers to round 1's verdicts

- **🔴 1, its thirteen shapes: confirmed closed.** Each is `other` at
  ea0d41a9 (executed), and so are `${|` and `${⏎`. The class is not closed:
  findings 1 and 2 are its two remaining members.
- **🟡 2: confirmed closed for the three named options.** `sed -I` (also
  `-nI`), `rg --pre` in both spellings and `sort --compress-program` (also
  its prefix `--compress-prog`) are `other` (executed). `rg --pre-glob`
  stays `read`. Finding 3 is the class member left over.
- **🟡 3: confirmed closed.** The bound is stated in `writes`' docstring,
  in `READ_WORDS`' comment, in the SKILL paragraph and in the changelog
  fragment. The admission criterion no longer contradicts sed and awk being
  admitted, because the comment names them as admitted under the bound.
  R2's note no longer calls two program writes the whole bound (72ca4827).
- **⬜ 4: confirmed closed.** The SKILL list now opens with "for example"
  and names `NEUTRAL_WORDS` as the whole list (read).
- **Round 1's ❓ (the `read` row beside the `Read` tool row): answered.**
  `questions.md` Q6 records the orchestrating session's answer. It rests on
  the owner's pre-edit answer, which named the family `read`, and it
  records that the owner may overturn it. No change was asked of the code.
- **Round 1's 🟢 rows are carried.** The fix diff leaves `NEUTRAL_WORDS`,
  `abbreviates`, `family`, `without_heredoc_bodies` and `runs_git`'s code
  unchanged. It widens `HIDDEN_FROM_THE_WALK` in the direction of `other`
  and still matches on text.

## Checked against the account

- *Claimed* in the unit's comment, `runs_git`'s docstring and the R3
  correction: a leading redirection keeps the line out. *Found* at
  `session_cost.py:566` that one glued after a background `&` does not
  (finding 1).
- *Claimed* in the changelog fragment and R3: zsh's short `if` forms keep
  out. *Found* only the `[[` form is recognised. The `((` form and the
  short `for` are `read` (finding 2).
- *Claimed* in `READ_WORDS`' comment: every option that runs a program is
  refused. *Found* that `rg --hostname-bin` is not (finding 3).
- *Claimed* by the caller: five shapes are `other` and three are `read` at
  72ca4827. *Found* the same at ea0d41a9. The rg line was run as `rg --pre
  ./x pat`, not with the caller's argument.
- *Claimed*: the six new read controls hold. *Found* that all six are
  `read`. Two further shapes lean toward `other`, which R3 states:
  `grep -n '{' f` (a quoted brace is a bare `{` to the walk) and
  `(ls;) 2>/dev/null` (the `;)` token resets `started`). Neither occurs in
  the corpus.
- *Carried, not re-run*: `bin/test` over the other two modules (the caller
  reports 203 over three), `evidence_check.py --strict`, `round_record.py
  close`, the 18 shapes red at 0ba42634, the 18 mutants and 2 survivors,
  and the fix pass's corpus movement of 1 call of 24,333. The survivors'
  pins are in 4e214176 (read), and `") x"` stops pinning its guard under
  finding 2's fix.

## What this round did not verify

- bash 5.3's `${ cmd; }` was not run, because this machine has bash 3.2 and
  zsh 5.9 only. The pattern errs toward `other`. Anyone with bash 5.3 can
  answer it.
- The full suite, repository-wide lint and typecheck: not yet. They are
  the sealer's, once the rounds settle, and they are not due while this
  report opens findings.

## Regression tests to plant

All go in `tests/test_session_cost.py`, and the fences under *Paste-ready
fixes* carry the exact lines.

- `test_what_the_walk_cannot_see_is_not_read`: three shapes for finding 1
  and three for finding 2. The stray-paren pin gains `") 2"`.
- `test_a_write_is_never_read`: two spellings of `rg --hostname-bin`.
- `test_a_call_that_only_reads_is_charged_to_read`: `ls & ls`, `(ls) <f` and
  `(cd /x && ls) 2>&1 | head`.

They were seen red as follows. The planted module against ea0d41a9's code
failed in two functions (2 failed, 138 passed, exit 1), and the probe showed
each planted other-shape `read` at ea0d41a9. Five mutants of the proposed
fix are each killed by a planted case.

## Facts for the evidence ledger

- R2: add `rg --hostname-bin` beside `rg --pre`. Executed 2026-09-28 with
  ripgrep 14.1.1: the program ran with no hyperlink flag.
- R3: a leading redirection glued after a background `&` (`&<`, `&⏎>`,
  zsh's `&|>`) and a word after a closing `)` other than a descriptor
  number or a redirection's target (zsh's `if (( … )) cmd` and
  `for f (…) cmd`) are `other`. Executed 2026-09-28: zsh 5.9 deleted the
  file in `ls &</dev/null rm x`, `ls &⏎>/dev/null rm x`, `ls &|>/dev/null
  rm x`, `if (( ! true )) rm x; ls` and `for f (ls) rm x; ls`, and bash 3.2
  in the first two.
- The changelog fragment's list of zsh short forms and `runs_git`'s
  docstring change with finding 2's fix.
- With the paste-ready fixes applied in the clone, `evidence_check.py
  --strict` names five anchors as drifted: `only_reads`, `writes` and the
  three case functions above. Those are the rows R1–R3 cite, and each needs
  a re-read. The report itself raised no name that is not in the tree.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A leading redirection glued after a background `&` is `read`: `ls &</dev/null rm x`, `ls &⏎>/dev/null rm x`, zsh's `ls &\|>/dev/null rm x` | `skills/verify/scripts/session_cost.py#SEPARATOR_THEN_REDIRECTION` | open | Executed: `read` at ea0d41a9, and zsh 5.9 deleted the file in each. The pattern's run cannot begin with a lone `&`. Spec In §1 says a write is never `read` |
| 🔴 2 | zsh's short forms closed by `))` or a `for` list's `)` hide their body: `if (( ! true )) rm a; ls`, `for f (ls) rm $f; ls` | `skills/verify/scripts/session_cost.py#only_reads` | open | Executed: `read` at ea0d41a9, and zsh 5.9 deleted the file in each. The fix recognised only `[[ … ]]`, which is one of the two delimiters the zsh manual names |
| 🟡 3 | `rg --hostname-bin` runs the program it names and is `read` | `skills/verify/scripts/session_cost.py#writes` | open | Executed: ripgrep 14.1.1 ran the program with no hyperlink flag. `READ_WORDS`' comment says every option that runs a program is refused |
| 🟢 | round 1's blocking finding's thirteen shapes are closed — leading redirection, zsh `[[` short `if` and `always`, bash 5.3 `${ }` | `skills/verify/scripts/session_cost.py#only_reads` | confirmed | Executed: each is `other` at ea0d41a9. The class's two remaining members are findings 1 and 2 |
| 🟢 | round 1's 🟡 2 is closed — `sed -I`, `rg --pre`, `sort --compress-program` | `skills/verify/scripts/session_cost.py#writes` | confirmed | Executed: all spellings are `other` and `rg --pre-glob` is `read`. Finding 3 is the class member left over |
| 🟢 | round 1's 🟡 3 is closed — the program bound is stated | `skills/verify/scripts/session_cost.py#writes`, `#READ_WORDS` | confirmed | Read: the docstring, the comment, the SKILL paragraph, the changelog and R2 state it, and the criterion names sed and awk as admitted under it |
| 🟢 | round 1's ⬜ 4 is closed — the neutral-word list is an example | `skills/verify/SKILL.md:725` | confirmed | Read: "for example", and `NEUTRAL_WORDS` is named as the whole list |
| ❓ | round 1's naming question, the `read` row beside the `Read` tool row | `seal/specs/1790562541-reading-is-charged-to-a-read-family/questions.md` | answered | Read: Q6 records the orchestrating session's answer on the owner's naming, and says the owner may overturn it |
| 🟢 | The six over-blocking controls | `tests/test_session_cost.py#test_a_call_that_only_reads_is_charged_to_read` | verified | Executed: all six are `read`. `grep -n '{' f` and `(ls;) 2>/dev/null` lean toward `other`, as R3 states, and the corpus holds neither |
| carried | Round 1's 🟢 rows: divergences, #635's findings | `skills/verify/scripts/session_cost.py` | verified | Carried from round 1. The fix diff leaves each unit's code unchanged, except `HIDDEN_FROM_THE_WALK`, which widened toward `other` |

## Executed probes

| What was run | Result |
|---|---|
| Class probe through `family` at ea0d41a9, 64 lines, in a scratch clone | Round 1's shapes plus `${\|`, `${⏎`, `sed -nI` and `--compress-prog`: 21 of 21 `other`. Background-`&` shapes: 4 `read`. zsh `((` and short-`for` shapes: 5 `read`. `rg --hostname-bin`: `read`. Controls: 18 of 22 `read`, five of the six planted ones among them. Of the four others, `while read …` has no read word and `ls & wait` has `wait`, both rightly `other`; `grep -n '{' f` and `(ls;) 2>/dev/null` lean toward `other`. The sixth planted control, `cat ${f:-x}`, is `read` when run on its own |
| zsh 5.9 and bash 3.2, `-c` on six escaping lines, each with a file `x` present | zsh deleted `x` in all six. bash deleted it in the two `&` lines and refused the other four with exit 2 |
| ripgrep 14.1.1, `--hostname-bin=./hb` alone, with `--hyperlink-format=default`, and with `--color=always` | the program ran each time, exit 0 |
| `bin/test tests/test_session_cost.py` with the paste-ready fixes and cases applied in the clone | 140 passed, exit 0 |
| The same module with the planted cases against ea0d41a9's code | 2 failed, 138 passed, exit 1 |
| `uvx ruff check` and `uvx ruff format --check` on the two patched files | exit 0, exit 0 |
| Five mutants of the proposed fix | each killed; see the fence |
| Corpus differential, ea0d41a9 against the proposed fix, 377 local transcripts, 24,379 Bash calls | 0 calls change family |
| `bin/test tests/test_no_real_identifiers.py` at ea0d41a9 | 5 passed, exit 0 |
| `bin/test` over the branch's other two modules, `evidence_check.py --strict`, `round_record.py close` | not run by this round; the caller's results are carried as the caller's |
| Full suite, repository-wide lint and typecheck | not yet; the sealer's, once the rounds settle |

### Mutants of the proposed fix

```
no digit exemption            killed by '(cd /x && ls) 2>&1 | head'
no redirection-target exempt  killed by '(ls) <f'
lone-& alternative dropped    killed by 'ls &</dev/null rm x'
lookahead dropped (& admits &>) killed by 'ls &>/dev/null'
no --hostname-bin             killed by 'rg --hostname-bin ./x pat'
guard `elif commands:` → else  ') x' still other; ') 2' raises IndexError
```

## Paste-ready fixes

### 🔴 1

```python
# skills/verify/scripts/session_cost.py, replacing the unit and its comment
# An operator token that ends one command and opens a redirection before the
# next one's first word, glued by the tokeniser: `;>`, `&&>`, `|<`, `(>`,
# `⏎<`, and after a background `&`: `&<`, `&⏎>` and zsh's `&|>`. `&>` alone
# is not one, because bash and zsh read it as a redirection of its own.
SEPARATOR_THEN_REDIRECTION = re.compile(r"(?:[;|\n(]|&&|&(?![>&]))+&?[<>]")
```

```python
# tests/test_session_cost.py, test_what_the_walk_cannot_see_is_not_read, the other-list
        "ls &</dev/null rm x",
        "ls &\n>/dev/null rm x",
        "ls &|>/dev/null rm x",
# tests/test_session_cost.py, test_a_call_that_only_reads_is_charged_to_read
        "ls & ls",
```

### 🔴 2

```python
# skills/verify/scripts/session_cost.py, only_reads, the walk
    commands, redirect, started, closed, previous = [], None, False, False, ""
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
                started, closed = True, False
            elif kind == "operator":
                if set(token) & REDIRECTION:
                    # A redirection before a command's first word keeps that
                    # word out of command position (`runs_git`'s third
                    # bound), so what the command runs is never seen:
                    # `ls; >/dev/null rm -rf x`. Here the bound keeps the
                    # line out.
                    if not started or SEPARATOR_THEN_REDIRECTION.match(token):
                        return False
                    redirect = token if ">" in token else None
                else:
                    started = not (set(token) & SEPARATOR)
                    closed = token.endswith(")")
            elif closed and not (token.isdigit() or set(previous) & REDIRECTION):
                # bash refuses a word after a closing `)`; zsh runs it as the
                # body of a short form (`if (( x )) rm a`, `for f (a b) rm
                # $f`). The walk reads it as an argument, so the command in
                # it is never seen, and the line keeps out. A descriptor
                # number and a redirection's target are not that word.
                return False
            elif commands:
                commands[-1].append(token)
            previous = token
    except ValueError:
        return False
```

```python
# skills/verify/scripts/session_cost.py, runs_git's docstring, its last sentence
    The harness runs the user's shell, zsh on the machine #642 measured,
    and zsh's short forms hide a command the same way: `if [[ … ]] cmd`,
    `if (( … )) cmd`, `for f (…) cmd` and an `always` block, so
    `only_reads` keeps those out as well."""
```

```python
# tests/test_session_cost.py, test_what_the_walk_cannot_see_is_not_read, the other-list
        "if (( ! true )) rm a; ls",
        "if (( ! true )) 2>/dev/null rm a; ls",
        "for f (ls) rm $f; ls",
# the stray-paren pin, which under this fix only `") 2"` still holds
    assert module.family(") x") == "other"
    assert module.family(") 2") == "other"
# tests/test_session_cost.py, test_a_call_that_only_reads_is_charged_to_read
        "(ls) <f",
        "(cd /x && ls) 2>&1 | head",
```

### 🟡 3

```python
# skills/verify/scripts/session_cost.py, writes, the rg arm
        if name == "rg" and (
            word in ("--pre", "--hostname-bin")
            or word.startswith(("--pre=", "--hostname-bin="))
        ):
            return True
# and in writes' docstring: `rg --pre`, which runs its command on every
# file, and `rg --hostname-bin`, which runs its program for the host name;
```

```python
# tests/test_session_cost.py, test_a_write_is_never_read
        "rg --hostname-bin ./x pat",
        "rg --hostname-bin=./x pat",
```

Needs a fix: yes — 🔴 1 (a leading redirection after a background `&`), 🔴 2 (zsh's `((` and short `for` forms), 🟡 3 (`rg --hostname-bin`)
Loses a record or crashes: no

```
📋 code-review applied
· spec:     round-1.md, round-1-report.md, questions.md Q1–Q6, the diffs of overview.md, changelog.md, seal/ledger/1790562541-…md R1–R7, seal/ledger/1790562540-…md A6 and seal/releases/*.md in 7be42f52..72ca4827
· compared: skills/verify/scripts/session_cost.py:225-734 at ea0d41a9; the 7be42f52..72ca4827 diff of session_cost.py, tests/test_session_cost.py and skills/verify/SKILL.md; tests/test_session_cost.py:1966-1995
· verdict:  🔴 2 · 🟡 1 · 🟢 6 confirmed or verified · ❓ 1 answered
```
