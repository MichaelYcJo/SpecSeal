# 1790562541-reading-is-charged-to-a-read-family — review round 3

| Field | Value |
|---|---|
| Target SHA | 56894d9db81b9d4e2622c58ff9bc69c77590c089 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | #651 |
| Broad gate | a4351ff1 against a9a74c46 |
| Fixes checked by | no fixes to check |
| Fix range | `510621d114d39d20d0f3715823c1d82c29736708..1863aafdbd32f784506527bcbb7b5afa0a3aca18`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🔴 1 (a `)` glued before a separator and a leading redirection), 🔴 2 (zsh's short form closed by a `)` glued to a redirection) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 of work item 1790562541 (#642), the verifying round and the run's last: round 2 reopened the run and its fixes closed on a fix, which spent the one reopening, so the run ends at this record whatever it finds. Its target is the diff of round 2's fixes, dc766d6e..21bd0ff8 (0ecd06e6 the fixes and planted rows, 6454f532 two equivalent parts removed and one control added, 21bd0ff8 the ledger), with the branch at the closed record's commit and draft PR #651. The job is the answers: are round 2's 🔴 1 (a leading redirection after a lone background `&`), 🔴 2 (zsh's `(( ))` and short `for` forms) and 🟡 3 (`rg --hostname-bin`) actually closed, on zsh 5.9 as well as bash, and do the fix's two departures from the reviewer's paste-ready text (a reduced regex, and no reset on a command word) hold. Anything still open takes the filing ladder. Answer `Needs a fix:` and `Loses a record or crashes:` in lines of their own.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A `)` glued before a separator and a leading redirection hides the next command: `(ls);>/dev/null rm x`, `(ls)&</dev/null rm x`, `(ls)⏎>/dev/null rm x`, and three more are `read` | `skills/verify/scripts/session_cost.py#SEPARATOR_THEN_REDIRECTION` | deferred #652 | #652 — this record ends the run on the reopening bound; the one-line fix and planted rows are carried there, 0 corpus calls affected; Executed at 56894d9d: all six are `read`, and bash 3.2 and zsh 5.9 deleted the file in each. `.match` needs the token to begin with a separator, and `);>` begins with `)`. Spec In §1 says a write is never `read`. The class is round 2's finding 1 |
| 🔴 2 | zsh's short form closed by a `)` glued to a redirection hides its body: `if (( ! true ))>/dev/null rm a; ls`, `for f (ls)</dev/null rm $f; ls` are `read` | `skills/verify/scripts/session_cost.py#only_reads` | deferred #652 | #652 — the same `closed` line closes it; carried with 🔴 1; Executed at 56894d9d: five spellings are `read`, and zsh 5.9 ran `rm` in each. `closed` is set only by an operator with no `<` or `>`, and `))>` is one token. The class is round 2's finding 2 |
| ⬜ 3 | Ledger R3's note calls the dropped command-word reset an equivalent mutant no case could turn red | `seal/ledger/1790562541-reading-is-charged-to-a-read-family.md` R3 | answered | a correction to a record under seal/ledger/: R3 corrected in place at 1863aafd; Executed: `ls () cat f` is `other` without the reset and `read` with it, and zsh 5.9 accepts it (a function definition, exit 0). A correction to the run's paperwork, outside `Needs a fix` |
| 🟢 | round 2's blocking finding 1 is closed for the three shapes it named — `&<`, `&⏎>`, zsh's `&\|>` | `skills/verify/scripts/session_cost.py#SEPARATOR_THEN_REDIRECTION` | confirmed | Executed: all three are `other` at 56894d9d, and `ls & ls` and `ls &>/dev/null` stay `read`. The `)`-prefixed member of the class is finding 1 |
| 🟢 | round 2's blocking finding 2 is closed for the shapes it named — `if (( … )) cmd`, its `2>` spelling, `for f (…) cmd` | `skills/verify/scripts/session_cost.py#only_reads` | confirmed | Executed: all three are `other`, and the three new controls are `read`. `") 2"` reaches the guard. The glued-redirection member of the class is finding 2 |
| 🟢 | round 2's finding 3 is closed — `rg --hostname-bin` | `skills/verify/scripts/session_cost.py#writes` | confirmed | Executed: both spellings and the bare flag are `other`. ripgrep 14.1.1 refuses `--hostn`, so the exact-word arm matches ripgrep's parser |
| 🟢 | The fix's reduced regex, `&(?!>)` alone | `skills/verify/scripts/session_cost.py#SEPARATOR_THEN_REDIRECTION` | confirmed | Executed: 0 of 5,380,839 strings differ from round 2's pattern under `.match` |
| 🟢 | The fix's dropped reset of `closed` on a command word | `skills/verify/scripts/session_cost.py#only_reads` | confirmed | Executed: only `ls () cat f` and the refused `(ls;) cat f` differ, both toward `other`, and zsh runs nothing for the first. The stated ground is finding 3 |
| carried | Round 1's closures and round 2's 🟢 rows | `skills/verify/scripts/session_cost.py` | confirmed | Carried from round 2. The fix range leaves those units unchanged apart from the parts re-derived above |

## Paste-ready fixes

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
```python
# skills/verify/scripts/session_cost.py, only_reads, the redirection arm
                    if not started or SEPARATOR_THEN_REDIRECTION.search(token):
                        return False
# and the unit's comment gains: "Searched rather than matched, because a `)`
# closing a subshell can come first: `);>`, `)&<`."
```
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
```
📋 code-review applied
· spec:     round-2.md, round-2-report.md (verdicts and paste-ready fixes), the dc766d6e..56894d9d diffs of changelog.md, overview.md and seal/releases/0.15.6.md, ledger R3's round 2 note, docs/review-chain-spec.md §The cap bounds rounds, §The reopening and §Where a leftover goes
· compared: skills/verify/scripts/session_cost.py:280-739 at 56894d9d; the dc766d6e..21bd0ff8 diff of session_cost.py and tests/test_session_cost.py; 6454f532 on its own; tests/test_session_cost.py:1852-2001
· verdict:  🔴 2 · ⬜ 1 · 🟢 5 confirmed · carried 1
```

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
| round-2 | `skills/verify/scripts/session_cost.py#SEPARATOR_THEN_REDIRECTION` | round 2's 🔴 1 — fixed |
| round-2 | `skills/verify/scripts/session_cost.py#only_reads` | round 2's 🔴 2 — fixed |
| round-2 | `skills/verify/scripts/session_cost.py#writes` | round 2's 🟡 3 — fixed |
| round-2 | `skills/verify/scripts/session_cost.py#writes`, `#READ_WORDS` | round 2's 🟢 — confirmed |
| round-2 | `skills/verify/SKILL.md:725` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1790562541-reading-is-charged-to-a-read-family/questions.md` | round 2's ❓ — answered |
| round-2 | `tests/test_session_cost.py#test_a_call_that_only_reads_is_charged_to_read` | round 2's 🟢 — verified |
| round-2 | `skills/verify/scripts/session_cost.py` | round 2's carried — verified |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🔴 1: a `)` glued before a separator and a redirection hides the next command | Rung 1 fits on ownership, since the unit is round 1's `New units` row. This record ends the run, though, and may not close on a fix (§*The reopening*). The orchestrator chooses between rung 2, a comment on #642 while it is open, and rung 3, #642's remainder issue | the repository owner, as #642's owner: release 0.15.7 item B ships a `read` family that both shells' `rm` reaches through this shape |
| 🔴 2: zsh's short form closed by a `)` glued to a redirection | the same choice as finding 1, and the same fix line closes both | the repository owner, as #642's owner, for the same reason on zsh, the shell the harness runs here |
| ⬜ 3: ledger R3's note calls the reset an equivalent mutant | the ledger fragment's R3, corrected in place when findings 1 and 2 are fixed, or by the orchestrator before the pull request | the orchestrating session, which writes the ledger corrections for this work item |
