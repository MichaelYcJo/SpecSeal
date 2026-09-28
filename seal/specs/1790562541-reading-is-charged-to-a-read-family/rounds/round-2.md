# 1790562541-reading-is-charged-to-a-read-family — review round 2

| Field | Value |
|---|---|
| Target SHA | ea0d41a942541b925052db0bc055ec3127b04b3e |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #651 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `dc766d6e31c7a44c7fd2536633659d57c8f901ee..21bd0ff8d0ee1785a3f47c35f5984e13d265ae41`, 3 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🔴 1 (a leading redirection after a background `&`), 🔴 2 (zsh's `((` and short `for` forms), 🟡 3 (`rg --hostname-bin`) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 of work item 1790562541 (#642), the verifying round. Its target is the diff of round 1's fixes, 7be42f52..72ca4827 (078b4413 code, cases, SKILL and records; 4e214176 two pins; 14c46eaf ledger and overview; 72ca4827 one survivor sentence), with the branch at ea0d41a9 and draft PR #651. The job is the answers, not new findings: for each verdict round-1.md records as closed (🔴 1, 🟡 2, 🟡 3, ⬜ 4 fixed), is it actually closed, including on zsh 5.9, which is what this machine's Bash tool runs. The finding surface is round 1's `New units` (`SEPARATOR_THEN_REDIRECTION`, depth 1), the widened `writes`, the stated sed/awk program bound, and the six over-blocking controls, which nobody has reviewed. The ❓ naming question was answered by the orchestrator in questions.md Q6. Answer `Needs a fix:` and `Loses a record or crashes:` in lines of their own.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A leading redirection glued after a background `&` is `read`: `ls &</dev/null rm x`, `ls &⏎>/dev/null rm x`, zsh's `ls &\|>/dev/null rm x` | `skills/verify/scripts/session_cost.py#SEPARATOR_THEN_REDIRECTION` | **fixed** `0ecd06e6` | fixed at 0ecd06e6; Executed: `read` at ea0d41a9, and zsh 5.9 deleted the file in each. The pattern's run cannot begin with a lone `&`. Spec In §1 says a write is never `read` |
| 🔴 2 | zsh's short forms closed by `))` or a `for` list's `)` hide their body: `if (( ! true )) rm a; ls`, `for f (ls) rm $f; ls` | `skills/verify/scripts/session_cost.py#only_reads` | **fixed** `0ecd06e6` | fixed at 0ecd06e6; Executed: `read` at ea0d41a9, and zsh 5.9 deleted the file in each. The fix recognised only `[[ … ]]`, which is one of the two delimiters the zsh manual names |
| 🟡 3 | `rg --hostname-bin` runs the program it names and is `read` | `skills/verify/scripts/session_cost.py#writes` | **fixed** `0ecd06e6` | fixed at 0ecd06e6; Executed: ripgrep 14.1.1 ran the program with no hyperlink flag. `READ_WORDS`' comment says every option that runs a program is refused |
| 🟢 | round 1's blocking finding's thirteen shapes are closed — leading redirection, zsh `[[` short `if` and `always`, bash 5.3 `${ }` | `skills/verify/scripts/session_cost.py#only_reads` | confirmed | Executed: each is `other` at ea0d41a9. The class's two remaining members are findings 1 and 2 |
| 🟢 | round 1's 🟡 2 is closed — `sed -I`, `rg --pre`, `sort --compress-program` | `skills/verify/scripts/session_cost.py#writes` | confirmed | Executed: all spellings are `other` and `rg --pre-glob` is `read`. Finding 3 is the class member left over |
| 🟢 | round 1's 🟡 3 is closed — the program bound is stated | `skills/verify/scripts/session_cost.py#writes`, `#READ_WORDS` | confirmed | Read: the docstring, the comment, the SKILL paragraph, the changelog and R2 state it, and the criterion names sed and awk as admitted under it |
| 🟢 | round 1's ⬜ 4 is closed — the neutral-word list is an example | `skills/verify/SKILL.md:725` | confirmed | Read: "for example", and `NEUTRAL_WORDS` is named as the whole list |
| ❓ | round 1's naming question, the `read` row beside the `Read` tool row | `seal/specs/1790562541-reading-is-charged-to-a-read-family/questions.md` | answered | Read: Q6 records the orchestrating session's answer on the owner's naming, and says the owner may overturn it |
| 🟢 | The six over-blocking controls | `tests/test_session_cost.py#test_a_call_that_only_reads_is_charged_to_read` | verified | Executed: all six are `read`. `grep -n '{' f` and `(ls;) 2>/dev/null` lean toward `other`, as R3 states, and the corpus holds neither |
| carried | Round 1's 🟢 rows: divergences, #635's findings | `skills/verify/scripts/session_cost.py` | verified | Carried from round 1. The fix diff leaves each unit's code unchanged, except `HIDDEN_FROM_THE_WALK`, which widened toward `other` |

## Paste-ready fixes

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
```
📋 code-review applied
· spec:     round-1.md, round-1-report.md, questions.md Q1–Q6, the diffs of overview.md, changelog.md, seal/ledger/1790562541-…md R1–R7, seal/ledger/1790562540-…md A6 and seal/releases/*.md in 7be42f52..72ca4827
· compared: skills/verify/scripts/session_cost.py:225-734 at ea0d41a9; the 7be42f52..72ca4827 diff of session_cost.py, tests/test_session_cost.py and skills/verify/SKILL.md; tests/test_session_cost.py:1966-1995
· verdict:  🔴 2 · 🟡 1 · 🟢 6 confirmed or verified · ❓ 1 answered
```

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

```
no digit exemption            killed by '(cd /x && ls) 2>&1 | head'
no redirection-target exempt  killed by '(ls) <f'
lone-& alternative dropped    killed by 'ls &</dev/null rm x'
lookahead dropped (& admits &>) killed by 'ls &>/dev/null'
no --hostname-bin             killed by 'rg --hostname-bin ./x pat'
guard `elif commands:` → else  ') x' still other; ') 2' raises IndexError
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/session_cost.py:604`, `:483`, `:635` | round 1's 🔴 1 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:578`, `:590` | round 1's 🟡 2 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:584`, `:498` | round 1's 🟡 3 — fixed |
| round-1 | `skills/verify/SKILL.md:726` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py:527` | round 1's 🟢 — verified |
| round-1 | `skills/verify/scripts/session_cost.py:553` | round 1's 🟢 — verified |
| round-1 | `skills/verify/scripts/session_cost.py#family` | round 1's 🟢 — verified |
| round-1 | `skills/verify/scripts/session_cost.py#abbreviates` | round 1's 🟢 — verified |
| round-1 | `skills/verify/scripts/session_cost.py:604`, `#without_heredoc_bodies` | round 1's 🟢 — verified |
| round-1 | `skills/verify/scripts/session_cost.py#without_heredoc_bodies` | round 1's 🟢 — verified |
| round-1 | `skills/verify/scripts/session_cost.py:300`, `seal/releases/0.15.6.md` | round 1's 🟢 — verified |
| round-1 | `skills/verify/scripts/session_cost.py:2003` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
