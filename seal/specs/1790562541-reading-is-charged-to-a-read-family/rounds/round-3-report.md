# 1790562541-reading-is-charged-to-a-read-family — review round 3 report

Target: the fix range `dc766d6e..21bd0ff8` (0ecd06e6, 6454f532, 21bd0ff8), with the branch at 56894d9d. This is the verifying round after the one reopening, so the run ends at this record. Every probe ran in a `git clone --no-local` at 56894d9d under this round's scratch directory, which was deleted afterwards.

## Summary

Round 2's three findings are closed for every shape they named, on zsh 5.9 and on bash 3.2. Both departures from round 2's paste-ready text hold on behaviour. The regex reduction is exactly equivalent. The dropped reset is not the equivalent mutant the ledger calls it, but the one input that tells them apart moves toward `other`, which is the safe side.

The same two classes still have one member each. The cause is shared: a `)` glued to the operator after it.

1. A closing `)` glued in front of a separator and a leading redirection hides the next command. `(ls);>/dev/null rm x` and five other spellings are `read`, and bash and zsh both delete `x`. This is round 2's 🔴 1 class, and `(ls)&</dev/null rm x` is literally its lone-`&` shape with a `)` in front.
2. zsh's short-form `))` or `)` glued to a redirection hides the body. `if (( ! true ))>/dev/null rm a; ls` is `read`, and zsh deletes `a`. This is round 2's 🔴 2 class. The `closed` state is set only on an operator token with no `<` or `>` in it, so `))>` never sets it.

One added line in the redirection arm fixes both. It was run: the module stays green, every new row is red at 56894d9d, and the corpus moves by 0 calls.

## What round 2 asked, answered

### Round 2's 🔴 1: a leading redirection after a lone background `&`

Executed. `ls &</dev/null rm x`, `ls &⏎>/dev/null rm x` and `ls &|>/dev/null rm x` are `other` at 56894d9d. `ls & ls` and `ls &>/dev/null` stay `read`. The shapes the finding named are closed.

The class is not closed. The pattern is applied with `.match`, so the glued token must *begin* with a separator. `(ls)&</dev/null rm x` produces the token `)&<`, which begins with `)`, and it is `read`. That is finding 1 below.

### Round 2's 🔴 2: zsh's `(( ))` and short `for` forms

Executed. `if (( ! true )) rm a; ls`, its `2>/dev/null` spelling and `for f (ls) rm $f; ls` are `other`. `(ls) <f`, `(cd /x && ls) 2>&1 | head` and `(ls) | head -5` stay `read`. `") 2"` is `other` and reaches the guard its comment names.

The class is not closed. `closed = token.endswith(")")` runs only in the arm for operators with no `<` or `>`. The tokeniser glues `))>` into one token, which goes to the redirection arm, so `closed` is never set. The word after the target then rides as an argument of `true`. That is finding 2 below.

### Round 2's 🟡 3: `rg --hostname-bin`

Executed. `rg --hostname-bin ./x pat f`, `rg --hostname-bin=./x pat f` and a bare `rg --hostname-bin` are `other`. `rg --hostn=./x pat f` is `read`, and that is correct: ripgrep 14.1.1 refuses the abbreviation (`unrecognized flag --hostn`, exit 2) and runs nothing. So the exact-word arm matches ripgrep's parser, unlike the GNU-style `abbreviates` arms beside it. Closed.

### Departure 1: the regex reduced to `&(?!>)`

Executed. I compared `(?:[;|\n(]|&(?!>))+&?[<>]` against round 2's `(?:[;|\n(]|&&|&(?![>&]))+&?[<>]` with `.match` on every string over `;`, `|`, newline, `(`, `&`, `<`, `>`, `)` and `x`, up to length 7. That is 5,380,839 strings, and 0 differ. The lone-`&` alternative covers `&&` by matching twice, and at the second `&` of `&&>` the trailing `&?` takes over. The departure holds.

### Departure 2: no reset of `closed` on a command word

Executed. It holds on behaviour, but the stated ground is wrong. Commit 6454f532 says *a command word can follow a closing ) only after an operator that clears the state*. Ledger R3 says the reset was *an equivalent mutant no case could turn red*.

An operator token that ends in `)` and also holds a separator puts the next word in command position without clearing `closed`. The examples are `()`, `;)`, `&)` and `|)`. I restored the reset in memory and compared:

| Line | without the reset (branch) | with the reset | What the shells do |
|---|---|---|---|
| `ls () cat f` | `other` | `read` | zsh defines a function `ls` and runs nothing (exit 0); bash refuses (exit 2) |
| `(ls;) cat f` | `other` | `read` | both shells refuse |
| `(ls) \| head -5`, `for f (ls) rm $f; ls` | unchanged | unchanged | |

So one line zsh accepts turns the mutant red. The branch's answer, `other`, is the right one for a line that reads nothing, and no write escapes either way. The departure stands. Only the sentence in R3 is false, which is ⬜ 3.

## Findings

### 🔴 1: a `)` glued before a separator and a redirection hides the next command

`skills/verify/scripts/session_cost.py#SEPARATOR_THEN_REDIRECTION`, used by `only_reads`'s redirection arm (`.match(token)`).

Executed at 56894d9d:

| Line | `family` | bash 3.2 | zsh 5.9 |
|---|---|---|---|
| `(ls);>/dev/null rm x` | `read` | deleted `x` | deleted `x` |
| `(ls)&&>/dev/null rm x` | `read` | deleted `x` | deleted `x` |
| `(ls)\|>/dev/null rm x` | `read` | deleted `x` | deleted `x` |
| `(ls)&</dev/null rm x` | `read` | deleted `x` | deleted `x` |
| `(ls)⏎>/dev/null rm x` | `read` | deleted `x` | deleted `x` |
| `(ls);</dev/null rm x` | `read` | deleted `x` | deleted `x` |

Why it matters: spec In §1 says a write is never `read`, and here `rm` is charged to reading in both shells. The token is `);>`, `)&<` and so on. `.match` anchors at the token's start, and `)` is not in the class, so the walk takes the token for a redirection of the subshell. The target is dropped, and `rm x` becomes arguments of `ls`.

Two fixes close this, and either is enough:

- the `closed` line from 🔴 2, because the `rm` after the target is a word after a closing `)`. The mutant table shows every row stays `other` with `.match` kept;
- `.search` in place of `.match`, which finds the separator inside the token. This one is the pattern's own fix, and it does not depend on a word following the target.

With both applied, `.search` becomes an equivalent mutant that no row turns red. A fix pass that drops parts no case can kill will drop it, as it dropped the `&&` alternative. Both are fenced below. Which one the fix keeps is the fixer's choice.

Depth: `SEPARATOR_THEN_REDIRECTION` is round 1's `New units` row (depth 1), and round 2's fixes changed it.

### 🔴 2: zsh's short form, closed by a `)` glued to a redirection, hides its body

`skills/verify/scripts/session_cost.py#only_reads`, the `closed` state that round 2's fixes added.

Executed at 56894d9d:

| Line | `family` | zsh 5.9 | bash 3.2 |
|---|---|---|---|
| `if (( ! true ))>/dev/null rm a; ls` | `read` | deleted `a` | refused, exit 2 |
| `if (( ! true ))</dev/null rm a; ls` | `read` | deleted `a` | refused, exit 2 |
| `if (( ! true ))&>/dev/null rm a; ls` | `read` | deleted `a` | refused, exit 2 |
| `for f (ls)>/dev/null rm $f; ls` | `read` | ran `rm ls` | refused, exit 2 |
| `for f (ls)</dev/null rm $f; ls` | `read` | deleted a file named `ls` | not run |
| `for f (ls)2>/dev/null rm $f; ls` | `other` | exit 0; `rm`'s error went to `/dev/null`, so its run was not observed | refused, exit 2 |

Why it matters: this is the harness's shell on this machine, and round 2 pinned the spaced spelling `if (( ! true )) 2>/dev/null rm a; ls` for this reason. The glued spelling is the same line to zsh. `closed` is assigned only in the arm for operators without `<` or `>`, so `))>`, `)<` and `))&>` never set it. The `2>` spelling is caught only because the tokeniser splits `)` from the digit.

Depth: `only_reads` is not in either record's `New units`, and the `closed` state is round 2's fix inside it. The finding is written apart from 🔴 1 for that reason, although one line fixes both.

### ⬜ 3: ledger R3 calls the dropped reset an equivalent mutant

`seal/ledger/1790562541-reading-is-charged-to-a-read-family.md`, R3, round 2's correction note: *the command-word reset of the closing-paren state dropped, each an equivalent mutant no case could turn red*.

The regex half is true (departure 1). The reset half is false: `ls () cat f` is `other` without the reset and `read` with it, and zsh accepts the line. Suggested wording: the reset was dropped because the one line that tells them apart, zsh's `name () cmd` function definition, runs nothing, and `other` is the right family for it. This is the run's paperwork, so it is outside `Needs a fix`.

R3's clause will also need a correction when 🔴 1 and 🔴 2 are fixed. It says *a word after a closing `)` that is neither a descriptor number nor a redirection's target* is `other`. At 56894d9d that is false whenever the `)` is glued to the redirection.

## Regression tests to plant

Destination `tests/test_session_cost.py`. Each row goes inside an existing case, following the depth rule the fix pass used.

- `test_what_the_walk_cannot_see_is_not_read`, the other-list: `(ls);>/dev/null rm x`, `(ls)&</dev/null rm x`, `(ls)⏎>/dev/null rm x`, `if (( ! true ))>/dev/null rm a; ls`, `for f (ls)</dev/null rm $f; ls`. Seen red: each is `read` at 56894d9d's code, measured one row at a time. The module run with the rows and the old code stopped at the first, 1 failed, exit 1.
- `test_a_call_that_only_reads_is_charged_to_read`: `(ls)>/dev/null` and `(cd /x && ls)2>&1 | head`, the glued spellings of two existing controls. They are `read` under the fix and under every mutant tried. No mutant this round turned them red, so the fix pass still owes that (§15). One mutant that should turn them red: return `other` for every redirection token beginning with `)`.

## Facts for the evidence ledger

- R3's clause, once fixed: a `)` glued to a redirection (`))>`, `)<`, `))&>`) closes the short form's test or list the same way a bare `)` does, and a `)` glued in front of a separator and a redirection (`);>`, `)&<`, `)⏎>`) is a leading redirection. The rows above are the grounds.
- R3's note: the regex reduction is equivalent over 5,380,839 strings, measured. The reset is not equivalent, and `ls () cat f` is the witness (⬜ 3).
- ripgrep 14.1.1 refuses an abbreviated long flag (`--hostn`, exit 2). The exact-word `rg` arm in `writes` is grounded by that refusal, and `abbreviates` does not apply to `rg`.

## Carried, not re-derived

- Round 1's closures and round 2's 🟢 rows (the six controls, the program bound, the neutral-word wording, the Q6 answer) are carried. The fix range touches `writes` only in the `rg` arm, and `only_reads` only in the `closed` state and the pattern, both of which were re-derived above.
- The caller's executed facts that I did not re-run: `bin/test` over three session-cost modules (203 passed), `evidence_check.py --strict` (exit 0), and `close` (exit 0, New units none). The fix pass's read facts are carried as the fix pass's claims: 12 mutants killed, 0 of 24,409 calls moved, and eight shapes red at ea0d41a9.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A `)` glued before a separator and a leading redirection hides the next command: `(ls);>/dev/null rm x`, `(ls)&</dev/null rm x`, `(ls)⏎>/dev/null rm x`, and three more are `read` | `skills/verify/scripts/session_cost.py#SEPARATOR_THEN_REDIRECTION` | open | Executed at 56894d9d: all six are `read`, and bash 3.2 and zsh 5.9 deleted the file in each. `.match` needs the token to begin with a separator, and `);>` begins with `)`. Spec In §1 says a write is never `read`. The class is round 2's finding 1 |
| 🔴 2 | zsh's short form closed by a `)` glued to a redirection hides its body: `if (( ! true ))>/dev/null rm a; ls`, `for f (ls)</dev/null rm $f; ls` are `read` | `skills/verify/scripts/session_cost.py#only_reads` | open | Executed at 56894d9d: five spellings are `read`, and zsh 5.9 ran `rm` in each. `closed` is set only by an operator with no `<` or `>`, and `))>` is one token. The class is round 2's finding 2 |
| ⬜ 3 | Ledger R3's note calls the dropped command-word reset an equivalent mutant no case could turn red | `seal/ledger/1790562541-reading-is-charged-to-a-read-family.md` R3 | open | Executed: `ls () cat f` is `other` without the reset and `read` with it, and zsh 5.9 accepts it (a function definition, exit 0). A correction to the run's paperwork, outside `Needs a fix` |
| 🟢 | round 2's blocking finding 1 is closed for the three shapes it named — `&<`, `&⏎>`, zsh's `&\|>` | `skills/verify/scripts/session_cost.py#SEPARATOR_THEN_REDIRECTION` | confirmed | Executed: all three are `other` at 56894d9d, and `ls & ls` and `ls &>/dev/null` stay `read`. The `)`-prefixed member of the class is finding 1 |
| 🟢 | round 2's blocking finding 2 is closed for the shapes it named — `if (( … )) cmd`, its `2>` spelling, `for f (…) cmd` | `skills/verify/scripts/session_cost.py#only_reads` | confirmed | Executed: all three are `other`, and the three new controls are `read`. `") 2"` reaches the guard. The glued-redirection member of the class is finding 2 |
| 🟢 | round 2's finding 3 is closed — `rg --hostname-bin` | `skills/verify/scripts/session_cost.py#writes` | confirmed | Executed: both spellings and the bare flag are `other`. ripgrep 14.1.1 refuses `--hostn`, so the exact-word arm matches ripgrep's parser |
| 🟢 | The fix's reduced regex, `&(?!>)` alone | `skills/verify/scripts/session_cost.py#SEPARATOR_THEN_REDIRECTION` | confirmed | Executed: 0 of 5,380,839 strings differ from round 2's pattern under `.match` |
| 🟢 | The fix's dropped reset of `closed` on a command word | `skills/verify/scripts/session_cost.py#only_reads` | confirmed | Executed: only `ls () cat f` and the refused `(ls;) cat f` differ, both toward `other`, and zsh runs nothing for the first. The stated ground is finding 3 |
| carried | Round 1's closures and round 2's 🟢 rows | `skills/verify/scripts/session_cost.py` | confirmed | Carried from round 2. The fix range leaves those units unchanged apart from the parts re-derived above |

## Executed probes

| What was run | Result |
|---|---|
| `family` at 56894d9d on round 2's shapes, the controls, and the `rg` spellings, in the scratch clone | Round 2's eight shapes: `other`. `rg --hostn=./x pat f`: `read`. Controls `ls & ls`, `ls &>/dev/null`, `(ls) <f`, `(cd /x && ls) 2>&1 \| head`, `(ls) \| head -5`, `ls -la`, `cd /x && sed -n 1,5p f`: `read`. `") 2"` and `") x"`: `other` |
| ripgrep 14.1.1, `--hostn=./hb --hyperlink-format=default pat f` | `unrecognized flag --hostn`, exit 2, and the program did not run |
| Regex equivalence, branch pattern against round 2's paste-ready one, under `.match` | 5,380,839 strings over nine characters up to length 7: 0 differ |
| `family` at 56894d9d on 14 candidate lines | 11 `read` (the six in finding 1, and `))>`, `))<`, `))&>`, `for f (ls)>`, `(ls)>/dev/null rm x`). `for f (ls)2>/dev/null rm $f; ls`, `ls () cat f` and `(ls;) cat f` are `other` |
| zsh 5.9 and bash 3.2, `-c` on each candidate, with files `x`, `a` and `f` present | Finding 1's six: both shells deleted `x`. `))>`, `))<`, `))&>`: zsh deleted `a`, bash exit 2. `for f (ls)>`: zsh ran `rm` (its error names `ls`), bash exit 2. `for f (ls)2>`: zsh exit 0 with the error sent to `/dev/null`, bash exit 2. `for f (ls)</dev/null …` with a file named `ls`: zsh deleted it. `(ls)>/dev/null rm x` and `(ls;) cat f`: parse error in both. `ls () cat f`: zsh exit 0, bash exit 2. `{ ls; }>/dev/null rm x`, `{ ls; } rm x`: parse error in both, so they are not escapes |
| The reset of `closed` restored in memory | `ls () cat f` and `(ls;) cat f` turn `read`. `(ls) \| head -5` and `for f (ls) rm $f; ls` are unchanged |
| `bin/test tests/test_session_cost.py` at 56894d9d, unmodified | 140 passed, exit 0 |
| The same with both proposed fixes (the `closed` line and `.search`) and the planted rows | 140 passed, exit 0 |
| The same with the planted rows against 56894d9d's code | 1 failed (`(ls);>/dev/null rm x`, the first row), 139 passed, exit 1. Each row is `read` there when run on its own |
| The same with the `closed` line alone and the planted rows | 140 passed, exit 0 |
| `uvx ruff check` and `uvx ruff format --check` on the two files with the `closed` line alone | exit 0, exit 0. The `.search` variant was not linted |
| Mutants of the proposed fix | see the fence |
| Corpus differential, 56894d9d against both fixes, over this machine's top-level transcripts | 124 transcripts, 16,476 Bash calls: 0 change family. A subset of the fix pass's 24,409 calls, which were read and not re-run |
| `bin/test` over the branch's other two modules, `evidence_check.py --strict`, `round_record.py close` | not run by this round; the caller's results are carried as the caller's |
| Full suite, repository-wide lint and typecheck | not yet; the sealer's, once the rounds settle |

```
row                                   base   fix    m:match  m:noclosed  m:anyparen
(ls);>/dev/null rm x                  read   other  other    other       other
(ls)&</dev/null rm x                  read   other  other    other       other
(ls)\n>/dev/null rm x                 read   other  other    other       other
if (( ! true ))>/dev/null rm a; ls    read   other  other    read        other
for f (ls)</dev/null rm $f; ls        read   other  other    read        other
(ls)>/dev/null                        read   read   read     read        read
(cd /x && ls)2>&1 | head              read   read   read     read        read

m:match     .search back to .match     not killed: the closed line alone covers finding 1
m:noclosed  the closed line removed    killed by the two zsh rows
m:anyparen  ")" in token for startswith  not killed: no row separates them
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🔴 1: a `)` glued before a separator and a redirection hides the next command | Rung 1 fits on ownership, since the unit is round 1's `New units` row. This record ends the run, though, and may not close on a fix (§*The reopening*). The orchestrator chooses between rung 2, a comment on #642 while it is open, and rung 3, #642's remainder issue | the repository owner, as #642's owner: release 0.15.7 item B ships a `read` family that both shells' `rm` reaches through this shape |
| 🔴 2: zsh's short form closed by a `)` glued to a redirection | the same choice as finding 1, and the same fix line closes both | the repository owner, as #642's owner, for the same reason on zsh, the shell the harness runs here |
| ⬜ 3: ledger R3's note calls the reset an equivalent mutant | the ledger fragment's R3, corrected in place when findings 1 and 2 are fixed, or by the orchestrator before the pull request | the orchestrating session, which writes the ledger corrections for this work item |

## Paste-ready fixes

### 🔴 1 and 🔴 2: the `closed` line, which alone closes both

```python
# skills/verify/scripts/session_cost.py, only_reads, the redirection arm
                    if not started or SEPARATOR_THEN_REDIRECTION.match(token):
                        return False
                    redirect = token if ">" in token else None
                    # A `)` glued to the redirection after it closes a
                    # subshell, a short form's `(( … ))` or a `for` list as a
                    # bare `)` does (`if (( x ))>/dev/null rm a`), so the word
                    # after the target is a word after a closing `)`. That
                    # also keeps out `(ls);>/dev/null rm x`, whose token
                    # begins with `)` and so escapes the pattern above.
                    closed = closed or token.startswith(")")
```

### 🔴 1: the pattern's own fix, if the fixer keeps it as well

```python
# skills/verify/scripts/session_cost.py, only_reads, the redirection arm
                    if not started or SEPARATOR_THEN_REDIRECTION.search(token):
                        return False
# and the unit's comment gains: "Searched rather than matched, because a `)`
# closing a subshell can come first: `);>`, `)&<`."
```

### The planted rows

```python
# tests/test_session_cost.py, test_what_the_walk_cannot_see_is_not_read, the other-list
        "(ls);>/dev/null rm x",
        "(ls)&</dev/null rm x",
        "(ls)\n>/dev/null rm x",
        "if (( ! true ))>/dev/null rm a; ls",
        "for f (ls)</dev/null rm $f; ls",
# tests/test_session_cost.py, test_a_call_that_only_reads_is_charged_to_read
        "(ls)>/dev/null",
        "(cd /x && ls)2>&1 | head",
```

Needs a fix: yes — 🔴 1 (a `)` glued before a separator and a leading redirection), 🔴 2 (zsh's short form closed by a `)` glued to a redirection)
Loses a record or crashes: no

The broad gate has not come due. Two findings are open, so the sealer's spawn waits on the orchestrator's decision about their rung.

```
📋 code-review applied
· spec:     round-2.md, round-2-report.md (verdicts and paste-ready fixes), the dc766d6e..56894d9d diffs of changelog.md, overview.md and seal/releases/0.15.6.md, ledger R3's round 2 note, docs/review-chain-spec.md §The cap bounds rounds, §The reopening and §Where a leftover goes
· compared: skills/verify/scripts/session_cost.py:280-739 at 56894d9d; the dc766d6e..21bd0ff8 diff of session_cost.py and tests/test_session_cost.py; 6454f532 on its own; tests/test_session_cost.py:1852-2001
· verdict:  🔴 2 · ⬜ 1 · 🟢 5 confirmed · carried 1
```
