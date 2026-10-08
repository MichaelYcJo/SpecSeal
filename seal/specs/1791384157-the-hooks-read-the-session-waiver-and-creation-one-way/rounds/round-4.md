# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — review round 4

| Field | Value |
|---|---|
| Target SHA | df73a69c0186a26a986af054e3cd333c49a2de8e |
| Written late | no |
| Ran by | specseal:warden on Opus 5.5 |
| PR | 881 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are written and no round has opened them |
| Fix range | `fba9fff061158a98e6f0678ceccfefb371295ecb..08f34e459874f3c03832238af22f24911dda7348`, 3 commits |
| Contract changes | none |
| New units | _BRACE_IN_WORD (depth 1); test_a_brace_segment_composes_its_c_values_as_git_does (depth 1); test_what_the_shell_does_not_expand_stays_silent (depth 1); test_a_brace_in_a_command_that_will_not_split_stops (depth 1) |
| Fix of a fix | no |
| Needs a fix | yes — 🟡 1 (the `-C` union misses the tree git runs in), 🟡 2 (`_BRACE` refuses a signed sequence and a brace after an escaped `$`), 🟡 3 (§A and its pin say no stopped pair is git) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 4, the redesign's first finding round after the reframe of round 3. Its target is 13e47f6e..df73a69c, phases 7 to 10: the over-stop measurement, the can-fail lease case, the brace rule on every word, and the records. Rounds 1 to 3 were inherited, and round 3's six deferred findings were the agenda. The spawn named five things to judge. First, whether _BRACE matches what bash expands and leaves alone what it must not stop. Second, whether any brace bash expands is still read past. Third, whether the -C union can miss the tree git runs in. Fourth, whether the 31-pair over-stop is measured by phase 1's method. Fifth, whether the NAME NOT IN TREE markers in round records are fair. Probes were to run in a scratch repository, never the session's checkout. It also ran the eight guard modules once. Facts arrived labelled. Read: the reframe's rule and P1 built on its default. Read from the smith: the 31-pair count, M5, 29 reds, four mutations and the module runs.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The `-C` union misses the tree git runs in: a git segment whose brace stands before its `-C` (`git {,} -C W switch feature/x`), and `-C` values git composes (`{git,} -C .. -C W switch feature/x`) | `hooks/worktree-guard.py:2485` | **fixed** `731c3c17` | fixed at 731c3c17; executed: both silent with the session's tree clean and `W` ACTIVE; bash hands git `-C W …` and `-C .. -C W …`; the brace-free `git -C .. -C W switch feature/x` denies naming `W`; the fix makes all three new parameters deny, 400 passed |
| 🟡 2 | `_BRACE` refuses a signed sequence endpoint (`git rebase main{+1..2}`) and a brace after an escaped `$` (`\${a,b}`), both expanded by bash | `hooks/worktree-guard.py:2007` | **fixed** `731c3c17` | fixed at 731c3c17; executed: bash 3.2.57 prints `1 2 3` for `{+1..3}` and `$a $b` for `\${a,b}`; `git rebase main{+1..2}` silent in an ACTIVE tree at the target; the fix stops both, 33 corpus pairs before and after |
| 🟡 3 | §A says every pair the rule stops is a command that is not git; one is a git segment, `git add <dir>/{plan,questions}.md` | `docs/worktree-guard-spec.md:106` | **fixed** `731c3c17` | fixed at 731c3c17; executed: phase 7's method through the guard's own functions: 33 of 32,641, one git; the hooks at `a8f86f44` stop that pair alone; self-check 19 of 19 and 0 of 6; the pin at `tests/test_guard_resolves_the_tree_it_judges.py:855` holds the false sentence |
| ⬜ 4 | An unquoted brace in a command the splitter cannot close (ANSI-C `$'\''`) is read only for a bare `git`: `{g..g}it switch feature/x` there is silent | `hooks/worktree-guard.py:2409` | **fixed** `731c3c17` | fixed at 731c3c17; executed: silent in an ACTIVE tree, bash runs `git switch feature/x`; `{git,}` in its place denies; the brace-free `g""it` twin is silent at `5623d728` too, so the class is deferred and only the brace line is proposed |
| ⬜ 5 | The false git share is copied into ledger row S22, the changelog fragment, `questions.md` M2, M4, P1 and phase 7 | `seal/ledger/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way.md:86` | answered | corrected at 46d8181c: ledger rows S11b and S22, `changelog.md`, `questions.md` M2, M4 and P1, phases 7 and 10 and `overview.md` carry 34 of 32,715 with its one git pair; a correction of the run's paperwork, following 🟡 3 |
| ⬜ 6 | Three `NAME NOT IN TREE` insertions split a sentence; the markers themselves are a fair use | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-2-report.md:85` | answered | corrected at 46d8181c: each of the three markers stands at the end of the sentence it split, on the line that names the removed unit; a correction of the run's paperwork; also `:91` and `plan.md:112`; 30 marker lines counted in the range |
| 🟢 | round 3's yellow 1 is closed — a brace behind a runner's operand, a redirection or a glued `(` stops | `tests/test_worktree_guard.py:1937` | confirmed | executed: each denies in an ACTIVE tree and is silent in a clean one, through `main()` and `_segment_finding` |
| 🟢 | round 3's yellow 2 is closed — empty and runner alternatives stop | `tests/test_worktree_guard.py:1945` | confirmed | executed: the four spellings deny in an ACTIVE tree |
| 🟢 | round 3's yellow 3 is closed — a brace after an `&` cut stops | `tests/test_worktree_guard.py:1949` | confirmed | executed: denies; every segment now carries the brace test, so the cut needs no reader of its own |
| 🟢 | round 3's white 4 is closed — the lease case can fail | `tests/test_lease_liveness.py:402` | confirmed | executed: `[None-None]` and `[-]` fail with the lease writer at `e0c5a191`, 6 pass at the target |
| 🟢 | round 3's white 5 is answered — an assignment brace stops, a named cost | `docs/worktree-guard-spec.md:102` | confirmed | executed: bash and zsh print `{a,b}` for an assignment; no recorded pair stops on one |
| 🟢 | round 3's white 6 is closed for the method — `phases/phase-7.md` writes it down | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/phases/phase-7.md:38` | confirmed | read: the six steps match phase 1's; the git split it reports is 🟡 3 |
| 🟢 | round 3's question on assignment-word expansion is answered | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/phases/phase-7.md:32` | confirmed | executed: M5 re-run under bash 3.2.57 and zsh, both `{a,b}` |
| 🟢 | rounds 1–2's closures stand — their brace spellings are in the reframed case | `tests/test_worktree_guard.py:1924` | confirmed | executed: round 1's and round 2's six spellings stop; the units they were fixed in left the tree and nothing reads their names |
| ❓ | Whether a hook process sees `CLAUDE_PID` and `CLAUDE_CODE_SESSION_ID` (round 1's and round 2's questions) | `hooks/hooksession.py:68` | ❓ out of verified scope | not reopened: the range does not touch it; the repository owner answers it, as `overview.md` names |

## Paste-ready fixes

```python
def _finding_trees(finding, tokens, wheres, cwd):
    """Every directory an unrecognised shape's verdict is about.

    `_finding_tree`'s one, and for a brace segment also every tree its `-C
    <dir>` word pairs name: each pair alone and the pairs composed in order,
    as git composes them, onto the directory the segment is placed in.
    `{git,} -C W switch x`, `{env,} git -C W switch x` and `git {,} -C W
    switch x` are judged in the session's tree AND in `W`, and `{git,} -C ..
    -C W switch x` in `../W`, because which word bash makes the command or
    the subcommand of is the thing the guard does not read, in a segment the
    frozen reading reads as git or not (the reframe of work item 1791384157,
    In 5, S20; round 4, yellow 1). More trees is the stopping direction. The
    pair is two plain words, `-C` and the word after it, the way
    `cmdline_base.parse_git` reads a git segment's `-C`; a glued `-C<dir>` is
    read by neither. A `-C` a brace hides (`{git,} {-C,} W switch x`) is not
    read, the named limit a string handed to a shell already has."""
    trees = [_finding_tree(tokens, wheres, cwd)]
    if tokens is None or getattr(finding, "kind", None) != "brace":
        return trees
    here, _target = worktree_consent.place(tokens, wheres, cwd)
    chdirs = []
    for at, word in enumerate(tokens[:-1]):
        if word == "-C":
            chdirs.append(tokens[at + 1])
            trees.append(apply_chdir(here, [tokens[at + 1]]))
            trees.append(apply_chdir(here, chdirs))
    return trees
```
```python
# tests/test_worktree_guard.py, added to the parameters of
# test_a_brace_command_word_is_judged_in_the_tree_its_c_names:
        # Round 4, yellow 1: a git segment whose brace stands before its
        # `-C`, which the frozen reading takes for the subcommand, and `-C`s
        # git composes. Red at `df73a69c`.
        "git {{,}} -C {w} switch feature/x",
        "git {{--no-pager,}} -C {w} switch feature/x",
        "{{git,}} -C .. -C W switch feature/x",
```
```markdown
docs/worktree-guard-spec.md, the paragraph at line 90, replaced:

A brace segment is judged in the tree the walk places it in and in every
tree a `-C <dir>` word pair among its words names, each pair alone and the
pairs composed in order as git composes them, from the placed directory. So
`{git,} -C W switch x` and `git {,} -C W switch x` stop where either the
session's tree or `W` matters: which word bash makes the command or the
subcommand of is what the guard does not read, and more trees is the
stopping direction. A `git -C` value or a `cd` operand holding a brace is
read as one word, so that segment is placed in a directory that does not
exist and falls back to the session's own tree, as §*Which tree* says.
```
```python
# A brace expansion bash and zsh perform before the command runs (#856):
# `{a,b}` with no whitespace inside, and a sequence `{1..3}`, `{+1..3}`,
# `{a..c}`, `{1..9..2}`, never after a `$`, where the braces are a parameter
# expansion. `{a}`, `{}` and `@{-1}` expand to nothing else and do not match.
_SEQUENCE = (
    r"[-+]?\d+\.\.[-+]?\d+(?:\.\.[-+]?\d+)?"
    r"|[A-Za-z]\.\.[A-Za-z](?:\.\.[-+]?\d+)?"
)
_BRACE = re.compile(r"(?<!\$)\{(?:[^{}\s]*,[^{}\s]*|" + _SEQUENCE + r")\}")
# The same test on a word the frozen splitter made. Its quotes and escapes
# are gone, so whitespace inside it was quoted (`{"a b",c}`) and a `$`
# before its brace may have been escaped (`\${a,b}` is `$a $b` to bash).
# Read only where `_BRACE` found an unquoted brace in the command's text
# (round 4 of work item 1791384157, yellow 2).
_BRACE_IN_WORD = re.compile(r"\{(?:[^{}]*,[^{}]*|" + _SEQUENCE + r")\}")
```
```python
# in _git_finding and in _segment_finding, the word test:
    if braced and any(_BRACE_IN_WORD.search(t) for t in tokens):
```
```python
# tests/test_worktree_guard.py, added to the parameters of
# test_a_brace_in_any_word_is_the_brace_shape:
        # Round 4, yellow 2: a signed sequence and a brace after an escaped
        # `$`, both expanded by bash (`git rebase main1 main2`, `$a $b`).
        # Red at `df73a69c`.
        "git rebase main{+1..2}",
        "echo {1..+3}",
        "echo \\${a,b}",
```
```markdown
docs/worktree-guard-spec.md, lines 106-110, the sentence replaced:

Of 32,641 distinct command and directory pairs recorded by 2026-10-08, the
rule stops 33: 32 a command that is not git, and one a git segment, `git add`
of a path holding `{plan,questions}`, which the owner's rule (c) stopped
before the rule was widened; none is an assignment word and none a quoted
brace beside an unquoted one, counted tree-blind by the method
`phases/phase-7.md` of work item 1791384157 writes down.

docs/worktree-guard-spec.md, lines 170-172:

shape adds 33 of 32,641 pairs recorded by 2026-10-08, one of them a git
segment and the rest a brace in an argument of a command that is not git, as
the brace paragraph above says.
```
```python
# tests/test_guard_resolves_the_tree_it_judges.py, in
# test_the_guard_policy_names_the_brace_shape_and_its_costs, replacing
# "the rule stops 31, every one a command that is not git":
        "the rule stops 33: 32 a command that is not git, and one a git segment",
    ):
        assert sentence in text, sentence
    for gone in (
        "the command-word rule stops none",
        "the segment is judged in the tree the `-C` after the brace word names",
        "every one a command that is not git",
    ):
        assert gone not in text, gone
```
```python
# in _command_findings, the untokenizable arm: a brace counts too, read off
# the raw text, because the quoting the splitter could not close is the
# quoting `_unquoted_brace` reads (round 4 of work item 1791384157, white 4).
    if not clean and (_holds_git(text) or _BRACE.search(text)):
        found.append(Finding("untokenizable", " ".join(text.split())))
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` on the eight guard modules the spawn named, in the clone at the target | exit 0, 435 passed |
| a deleted probe through `main()` at the target, 24 commands in an ACTIVE tree and again in a clean one | 9 deny in the ACTIVE tree (`{git,}`, an `if` body, a pipe, `<( )`, a backtick body, `x=1; {g..g}it`, `bash -c '{git,} …'`, and the two `$'\''` lines spelled with `{git,}` or `git`); 15 silent, each listed in the findings or the Deferred table; every one silent in the clean tree |
| the same probe, 20 commands that must not stop and 5 that should, dirty tree | 20 silent as listed under 🟡 2; `echo {a,b}` and `cat <<< {a,b}` ask; `echo \${a,b}`, `echo {+1..3}`, `echo {1..3..+1}` silent |
| the same probe, 10 commands, session's tree clean and `W` ACTIVE | deny naming `W`: `{git,} -C W`, `{git,} -C ~/W`, `cd W && {git,} …`, `git -C W {switch,} …`, `git -C .. -C W …`; silent: `git {,} -C W …`, `git {--no-pager,} -C W …`, `{git,} -C .. -C W …`, and both `--git-dir`/`--work-tree` forms |
| every probe command under bash 3.2.57 and zsh, a fake `git` first on `PATH`, cwd a scratch directory | bash hands the fake git `switch feature/x` (or its `-C` form) for every silent read-past above; zsh runs none of the brace forms that build the command word, hands git two empty words before `-C W …` for `git {,} -C W …`, and runs `$( ) git …` as bash does |
| a second probe at `5623d728` and `a8f86f44`, the hooks taken by `git archive` | identical at both: `$( ) git switch feature/x`, `$(echo git) switch feature/x`, `bash <<< 'git switch feature/x'`, both `$'\''` lines, `git rebase main{+1..2}`, `git {,} -C W …` and the `--git-dir` form silent; `git -C .. -C W …` denies naming `W` |
| bash 3.2.57 on sequence and escape spellings | `{1..+3}` and `{+1..+3}` give `1 2 3`, `{-1..+1}` gives `-1 0 1`, `\${a,b}` gives `$a $b`, `x\${,}` gives `x$ x$`; `{+1..3..2}`, `{1..3..+1}` and `{1..5..2}` stay literal |
| the paste-ready fixes for 🟡 1 and 🟡 2 applied in the clone; `tests/test_worktree_guard.py`, `tests/test_guard_resolves_the_tree_it_judges.py`, `tests/test_the_guard_asks_once_per_session.py` | exit 0, 400 passed |
| the six new parameters with the target's `hooks/worktree-guard.py` | 6 failed, 16 passed: each new parameter red |
| corpus re-measure by phase 7's method through the guard's own functions, self-check first | at the target: 33 of 32,606 pairs, 1 a git segment, 0 assignment, 0 quoted-beside, self-check 19 of 19 and 0 of 6; with the fixes: 33, the same split; at `a8f86f44`: 1 pair, the git one; a later run: 33 of 32,641 |
| `tests/test_lease_liveness.py -k "no_session_id or exported_for_another"` with `hooks/session-lease.py` at `e0c5a191`, then at the target | 2 failed (`[None-None]`, `[-]`), 4 passed; then 6 passed |
| `gh pr checks 881` at `df73a69c` | exit 8: lint, ledger, release, both grammar jobs, ubuntu, all four Windows groups and macOS group 1 pass; macOS groups 2 and 3 pending at hand-over |
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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A command substitution that leaves no word before `git` (`$( ) git switch feature/x`) or builds it (`$(echo git) switch feature/x`) is silent in an ACTIVE tree, at `5623d728` and at the target; bash and zsh run `git switch feature/x`. `{$( ),} git …` is the same hole with a brace around it | a new issue, not opened by this round | the repository owner, who decides whether the guard reads a command word a substitution makes |
| A here-string or heredoc handed to a shell (`bash <<< 'git switch feature/x'`) is not read, with or without a brace, at `5623d728` and at the target | a new issue, not opened by this round | the repository owner |
| An untokenizable command is read only for a bare `git` (P4 (a) of work item 1791270162): `g""it` behind ANSI-C `$'\''` is silent at `5623d728` and at the target | a new issue, not opened by this round; ⬜ 4 takes only the brace line | the repository owner, whose answer P4 (a) was |
| `git --git-dir=W/.git --work-tree=W switch feature/x` is judged in the session's tree, at `5623d728` and at the target | a new issue, not opened by this round | the repository owner |
