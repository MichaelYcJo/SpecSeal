# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — review round 5

| Field | Value |
|---|---|
| Target SHA | b9a4bcffd0ecc859ba86a6329974bcb9631097e5 |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 881 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Fix range | none — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Fix of a fix | first — 🟡 2 at hooks/worktree-guard.py#_BRACE, a unit round-4's fixes changed |
| Needs a fix | yes — 🟡 1 (a `$` before a quote hides a brace that makes `git`), 🟡 2 (whitespace inside a substitution or a parameter expansion ends the brace's word) |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Verifying round 5 of round 4's fixes: fba9fff0..08f34e45 plus the table and the close at b9a4bcff. The job was the answers to round 4's six verdicts. Round 4's new units (_BRACE_IN_WORD and three cases) were a finding surface. The spawn asked three things: whether the brace test is now biased to stop in every shape round 4 found while every must-not-stop form stays silent; whether the -C composition is right for absolute paths and -C ''; and whether the 34-pair measurement's method is written so it can be re-run. Probes were to run in a scratch repository, never the session's checkout. It also ran the eight guard modules once. Facts arrived labelled. Read: the orchestrator's direction to err toward stopping. Read from the smith: the one $ exception, 13 pinned silent forms, the composition, the 34/32,715 figure, six mutations and 773 passed.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A `$` that begins a quote (`$''`, `$'x'`, `$""`) is left before the `{` when the quote is taken out, so `$''{g..g}it switch feature/x` reads as a parameter expansion and is silent in an ACTIVE tree; bash and zsh run `git switch feature/x` | `hooks/worktree-guard.py:2046` | open | executed: bash 3.2.57 and zsh 5.9 make `$''{g..g}it` the word `git`, a fake git ran `switch feature/x`; four spellings silent in an ACTIVE tree at the target; with the fix the three proposed parameters are red at the target and green, the 13 silent forms stay silent |
| 🟡 2 | Whitespace inside `$( … )`, backticks or `${ … }` ends the brace's word for `_BRACE` and for the per-word test, so `{git,$(: x)} switch feature/x`, its backtick twin and `{git,${x:- }} switch feature/x` are silent in an ACTIVE tree; bash runs `git switch feature/x` | `hooks/worktree-guard.py:2021` | open | executed: bash prints `[git]` for all three and a fake git ran `switch feature/x`; the splitter cuts the word into `{git,$(:` and `x)}`; with the fix all three deny, three guard modules 416 passed, corpus 34 of 33,088 unchanged; also `:2212` and `:2302`; not #886, whose command word a substitution makes |
| ⬜ 3 | A reflog range (`git diff HEAD@{1}..HEAD@{0}`, `git log @{u}..@{1}`) asks in a dirty tree, and §A's silent list names `@{-1}` without saying that a range across two reflog braces stops | `docs/worktree-guard-spec.md:80` | open | executed: both `ask`, naming the brace shape; it is the stopping direction the orchestrator chose, so one clause naming the cost is all it asks |
| ⬜ 4 | The 34-pair self-check ran 21 must-stop and 15 must-not forms, but phase 7 step 6, its `Self-check` line and `questions.md` M4 name 19 and 6, the extra forms are written nowhere, and ledger S22 carries both figures | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/phases/phase-7.md:75` | open | a correction of the run's paperwork; executed: steps 1 to 5 re-run to 34 of 33,077, one git, none assignment; step 4's `_BRACE` and the guard's `_BRACE_IN_WORD` (NAME NOT IN TREE since round 5's fixes) agree on 34 and differ on the assignment column (0 against 1) |
| 🟢 | round 4's yellow 1 is closed — the `-C` union composes in order and covers a git segment whose brace stands before its `-C` | `hooks/worktree-guard.py:2488` | confirmed | executed: the four new parameters fail with the guard of `fba9fff0` and pass at the target; seven more spellings with `-C ''`, `-C ""`, absolute values first and mid-chain each deny naming `W` |
| 🟢 | round 4's yellow 2 is closed — a signed sequence and a brace after an escaped `$` stop | `hooks/worktree-guard.py:2021` | confirmed | executed: the four new parameters of the brace-shape test fail at `fba9fff0` and pass at the target; the class stays open as this round's 🟡 1 and 🟡 2 |
| 🟢 | round 4's yellow 3 is closed — §A says 34 of 32,715 with one git pair, and its pin holds the sentence | `docs/worktree-guard-spec.md:116` | confirmed | read: the sentence and its pin at `tests/test_guard_resolves_the_tree_it_judges.py:828`; executed: phase 7's steps 1 to 5 re-run to 34 with one git pair |
| 🟢 | round 4's white 4 is closed — an untokenizable line holding a brace stops | `hooks/worktree-guard.py:2430` | confirmed | executed: the new test fails at `fba9fff0` and passes at the target |
| 🟢 | round 4's white 5 is closed — the corrected count reaches every record that copied the old one | `seal/ledger/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way.md:86` | confirmed | read: a search of `docs/`, `seal/ledger/` and the work item outside its round records finds the old figure only where a record states what phase 7 first gave |
| 🟢 | round 4's white 6 is closed — each marker ends the sentence it split | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-2-report.md:85` | confirmed | read: the diff at 46d8181c; executed: the eight guard modules pass |

## Paste-ready fixes

```python
# after _BRACE_IN_WORD
# A parameter expansion with no brace inside it (`${HOME}`, `${a,}`, `${x:- }`).
_PARAMETER = re.compile(r"\$\{[^{}]*\}")


def _unquoted_brace(text) -> bool:
    ...  # docstring unchanged
    if tokens is None:
        return bool(_BRACE.search(text or ""))
    # A quoted span or an escape stands in as one character, never as nothing:
    # taken out, the `$` of `$''{g..g}it` lands before the `{` and reads as a
    # parameter expansion, which bash does not make of it.
    bare = tokens.QUOTED_SPANS.sub("q", text or "")
    # A substitution or a parameter expansion is part of the word it stands in
    # however much whitespace it holds (`{git,$(: x)}`, `{git,${x:- }}` are
    # `git` to bash), so its body stands in as one character too.
    if wide is not None:
        try:
            for body in sorted(wide.substitution_bodies(bare), key=len, reverse=True):
                bare = bare.replace(body, "q")
        except (Exception, SystemExit):
            return True
    return bool(_BRACE.search(_PARAMETER.sub("q", bare)))
```
```python
# _git_finding, and the same line in _segment_finding: the words joined, so a
# brace the frozen splitter cut at a substitution's whitespace is one match.
    if braced and _BRACE_IN_WORD.search(" ".join(tokens)):
```
```
`find`'s `{}`, `@{-1}`). An escaped `$` is not a parameter expansion, so
`\${a,b}`, which bash makes `$a $b`, stops (round 4 of work item 1791384157),
and neither is a `$` before a quote: `$''{g..g}it`, which bash and zsh make
`git`, stops. A command substitution or a parameter expansion is part of the
word it stands in, whatever whitespace it holds, so `{git,$(: x)}` and
`{git,${x:- }}`, which bash makes `git`, stop too (round 5 of work item
1791384157). A reflog range across two braces (`HEAD@{1}..HEAD@{0}`) holds
a `..` between them and stops, which bash would not expand.
A command the splitter could not close is read for such a brace in its raw
```
```python
        # Round 5, yellows 1 and 2.
        "and neither is a `$` before a quote",
        "A command substitution or a parameter expansion is part of the word it "
        "stands in",
```

## Executed probes

| What was run | Result |
|---|---|
| the eight guard modules named by the spawn, through `bin/test`, in the scratch clone at the target | exit 0, 435 passed |
| `printf '[%s]'` over thirteen spellings under bash 3.2.57 and zsh 5.9, in a scratch directory | bash: `$''{g..g}it` gives `[git]`, `{git,$(: x)}`, `` {git,`: x`} `` and `{git,${x:- }}` give `[git]`, `$'x'{a,b}` gives `[xa][xb]`, `$${a,b}` and `HEAD@{1}..HEAD@{0}` stay literal; zsh: the same, except it keeps an empty word after `git` for the three substitution forms and leaves `{+1..2}` literal |
| the same commands with a fake `git` on bash's path | `$''{g..g}it`, `{git,$(: x)}` and `{git,${x:- }}`, each followed by `switch feature/x`, printed `fake git ran: switch feature/x` |
| the guard at the target, ACTIVE tree | `$''{g..g}it switch feature/x`, `$''{g..g}it rebase main feature/x`, `$""{git,} -C . switch feature/x`, `echo $'x'{a,b}`, `{git,$(: x)} switch feature/x`, its backtick twin and `{git,${x:- }} switch feature/x` silent; `{git,} switch feature/x` deny |
| seven `-C` spellings, session tree clean and `W` ACTIVE | each deny naming `W`; the splitter keeps `''` and `""` as an empty word |
| round 4's new and widened tests with `hooks/worktree-guard.py` from `fba9fff0` | 9 failed, 29 passed: each new must-stop parameter and the untokenizable test failed |
| the same selection at the target | 38 passed |
| `_BRACE` mutated to cross whitespace and drop its `$` exception (`.*?` for each `\S*?`, no lookbehind), the silent test | 2 failed of 13 (`echo ${a,}`, the `&& echo {c, d}` form) |
| `git diff HEAD@{1}..HEAD@{0}` and `git log @{u}..@{1}`, dirty tree | `ask`, naming the brace shape |
| phase 7 steps 1 to 5, written from the record alone, guard at the target | 34 of 33,077 pairs; one git; assignment 0 with step 4's `_BRACE`, 1 with the guard's `_BRACE_IN_WORD` (NAME NOT IN TREE since round 5's fixes) |
| the paste-ready fixes for 🟡 1 and 🟡 2 applied in the clone | the six proposed parameters fail at the target and pass with the fixes; the brace-shape and silent tests 33 passed; `tests/test_worktree_guard.py`, `tests/test_guard_resolves_the_tree_it_judges.py` and `tests/test_the_guard_asks_once_per_session.py` exit 0, 416 passed; corpus 34 of 33,088 by step 4, the word test and the joined test |
| `gh pr checks 881` at `b9a4bcff` | exit 0: lint, ledger, release, both grammar jobs, ubuntu, three macOS groups and four Windows groups pass |
| `bin/evidence-check --strict`, `survivor-check`, `correction-check` | not run by this round; the smith's exit 0 is carried, and the sealer's broad gate runs them |
| the broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_worktree_guard.py:2178` | round 1's 🔴 1 — fixed |
| round-1 | `tests/test_worktree_guard.py:729` | round 1's 🔴 2 — fixed |
| round-1 | `hooks/worktree-guard.py:2270` | round 1's 🟡 3 — fixed |
| round-1 | `hooks/session-lease.py:91` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/worktree-guard.py:2007` | round 1's ⬜ 5 — answered |
| round-1 | `hooks/tokens.py:33` | round 1's ⬜ 6 — fixed |
| round-1 | `hooks/hooksession.py:68` | round 1's ❓ — out of verified scope |
| round-1 | `hooks/worktree_consent.py:419` | round 1's ❓ — out of verified scope |
| round-2 | `hooks/worktree-guard.py:2292` | round 2's 🟡 1 — fixed |
| round-2 | `hooks/worktree-guard.py:2470` | round 2's 🟡 2 — fixed |
| round-2 | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/survivors.md:24` | round 2's ⬜ 3 — answered |
| round-2 | `hooks/session-lease.py:98` | round 2's ⬜ 4 — fixed |
| round-2 | `hooks/session-lease.py:25` | round 2's ⬜ 5 — fixed |
| round-2 | `tests/test_worktree_guard.py:2199` | round 2's 🟢 — confirmed |
| round-2 | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/survivors.md` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:2282` | round 2's 🟢 — confirmed |
| round-2 | `hooks/tokens.py:45` | round 2's 🟢 — confirmed |
| round-3 | `hooks/worktree-guard.py:2320` | round 3's 🟡 1 — deferred |
| round-3 | `hooks/worktree-guard.py:2325` | round 3's 🟡 2 — deferred |
| round-3 | `hooks/worktree-guard.py:2392` | round 3's 🟡 3 — deferred |
| round-3 | `tests/test_lease_liveness.py:401` | round 3's ⬜ 4 — deferred |
| round-3 | `hooks/worktree-guard.py:2321` | round 3's ⬜ 5 — deferred |
| round-3 | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-2-fixes.md:23` | round 3's ⬜ 6 — deferred |
| round-3 | `tests/test_worktree_guard.py:1933` | round 3's 🟢 — confirmed |
| round-3 | `tests/test_worktree_guard.py:1985` | round 3's 🟢 — confirmed |
| round-3 | `hooks/session-lease.py:102` | round 3's 🟢 — confirmed |
| round-3 | `hooks/session-lease.py:27` | round 3's 🟢 — confirmed |
| round-4 | `hooks/worktree-guard.py:2485` | round 4's 🟡 1 — fixed |
| round-4 | `docs/worktree-guard-spec.md:106` | round 4's 🟡 3 — fixed |
| round-4 | `hooks/worktree-guard.py:2409` | round 4's ⬜ 4 — fixed |
| round-4 | `seal/ledger/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way.md:86` | round 4's ⬜ 5 — answered |
| round-4 | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-2-report.md:85` | round 4's ⬜ 6 — answered |
| round-4 | `tests/test_worktree_guard.py:1937` | round 4's 🟢 — confirmed |
| round-4 | `tests/test_worktree_guard.py:1945` | round 4's 🟢 — confirmed |
| round-4 | `tests/test_worktree_guard.py:1949` | round 4's 🟢 — confirmed |
| round-4 | `tests/test_lease_liveness.py:402` | round 4's 🟢 — confirmed |
| round-4 | `docs/worktree-guard-spec.md:102` | round 4's 🟢 — confirmed |
| round-4 | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/phases/phase-7.md:38` | round 4's 🟢 — confirmed |
| round-4 | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/phases/phase-7.md:32` | round 4's 🟢 — confirmed |
| round-4 | `tests/test_worktree_guard.py:1924` | round 4's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The four silent shapes round 4 found before this branch (a substitution that makes the command word, a here-string to a shell, `g""it` in an untokenizable line, `--git-dir`) | #886, already deferred in round 4 | the repository owner |
