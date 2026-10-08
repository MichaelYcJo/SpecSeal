# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — round 4 report

Target SHA `df73a69c0186a26a986af054e3cd333c49a2de8e` (executed: `git rev-parse
HEAD` in a scratch clone made with `git clone --no-local` and checked out
detached there). Range `13e47f6e..df73a69c`, 7 commits: the redesign's
first finding round. Reviewed by specseal:warden on Opus 5.5.

## What this round was asked

The redesign of the brace rule after round 3 stopped on a second fix of a
fix: phases 7–10, built on `spec.md` In 5, In 6, Out and S17–S24. Round 3's
six findings were deferred to the frame and are the redesign's agenda. The
spawn asked five things: whether `_BRACE` matches what bash expands and what
it must leave alone; whether any brace bash expands is still read past
(rounds 1–3's shapes, `$'…'` quoting, here-strings); whether the `-C` union
can miss the tree git runs in; whether the 31-pair over-stop was measured by
phase 1's method; and whether the `NAME NOT IN TREE` markers in round records
are a fair use of the exemption. It also ran the eight guard modules once
and read `gh pr checks 881`.

Facts arrived labelled. Read: the reframe's rule, and P1 built on its
default under `Automation | yes`, unanswered by the owner. Read from the
smith: 31 of 32,498 pairs, all non-git; M5; 29 cases red at `a8f86f44`; four
mutations; 30 marker lines; 562 and 435 passed; three checks exit 0. Each is
checked below or labelled as carried.

## How the findings relate

```
the reframe: an unquoted brace in any word stops; nothing reads where it stands
  ├─ 🟡 2  the brace's own definition is narrower than bash's  (a git word read past)
  ├─ 🟡 1  the tree a brace segment is judged in misses where git runs
  ├─ 🟡 3  the measured price, which P1 asks the owner to accept, misstates its git share
  │     └─ ⬜ 5  the same figure in the paperwork copies
  ├─ ⬜ 4  a brace in a command the splitter cannot close is read only for a bare `git`
  └─ ⬜ 6  three marker insertions split a sentence (the markers themselves are fair)
```

Round 3's agenda is answered: every one of its 19 spellings stops, the lease
case can fail, the assignment cost is measured, and the figure has a method.
The new findings sit in the pieces the reframe still has to get right on its
own: the definition of a brace, the trees, and the price.

## 🟡 1 — the `-C` union misses the tree git runs in

`hooks/worktree-guard.py:2485` (`hooks/worktree-guard.py#_finding_trees`).

The union is applied only where `parse_git` reads the segment as no git, and
each `-C` pair is composed alone onto the placed directory. git does
neither. Two spellings follow from that, and each is silent with the
session's tree clean and `W` ACTIVE, while bash runs `git -C W switch
feature/x` or `git -C .. -C W switch feature/x`:

- `git {,} -C W switch feature/x` and `git {--no-pager,} -C W switch
  feature/x`. The frozen reading takes the brace word for the subcommand, so
  it never sees the `-C` after it, and the segment is judged only in the
  session's tree. The reframe's principle, that the guard does not read where
  a brace stands, is exactly what this exclusion breaks: it reads the brace
  as standing in the subcommand slot.
- `{git,} -C .. -C W switch feature/x`. The union holds `..` and `./W`, and
  git runs in `../W`. The same words without the brace, `git -C .. -C W
  switch feature/x`, deny and name `W`, because `apply_chdir` composes every
  `-C` in order.

Executed: both silent at the target through `main()`; under bash 3.2.57 a
fake `git` first on `PATH` received `-C W switch feature/x` and `-C .. -C W
switch feature/x`. The first shape was silent at `5623d728` and `a8f86f44`
too, so round 2's `-C` read never covered it; the unit it now lives in is
the redesign's. `docs/worktree-guard-spec.md:90` says a brace segment read as
git "is placed as every git segment is", which is the sentence that has to
change with the code.

Why it matters: the union exists so that which word bash makes the command
of does not decide the tree. In both spellings the tree git switches is one
the guard never looks up, in the one state, ACTIVE, where §A denies.

Fix: apply the union to every brace finding and add each running
composition of the `-C` values. Applied in the clone, the three guard modules
pass (400) and the three new parameters are red against the target's hook.

## 🟡 2 — `_BRACE` refuses two brace expansions bash performs

`hooks/worktree-guard.py:2007`.

The reframe moves every judgment onto one definition, so that definition has
to be at least as wide as bash's. Two spellings bash expands do not match:

- **A signed sequence endpoint.** bash 3.2.57 expands `{+1..3}`, `{1..+3}`
  and `{-1..+1}` (executed: `1 2 3`, `1 2 3`, `-1 0 1`), and the pattern
  accepts only `-?`. So `git rebase main{+1..2}`, which bash hands git as
  `git rebase main1 main2` and which switches to `main2`, is listed and
  silent in an ACTIVE tree. The command's text is not braced either, so the
  stop is lost at both tests.
- **A brace after an escaped `$`.** `echo \${a,b}` prints `$a $b` under bash
  and zsh. The text test reads it as unquoted (`QUOTED_SPANS` takes `\$` out),
  but the frozen splitter has taken the backslash off the word, so the word
  is `${a,b}` and the `(?<!\$)` lookbehind refuses it.

A third gap is the same mismatch in another form: a word whose alternative
holds whitespace the shell quoted (`{"a b",c}`) reaches the word test with
the quotes gone, and `[^{}\s]` refuses it. No spelling built from it was
found that makes `git`, so it is named here and not counted.

What `_BRACE` leaves alone is right. Executed, dirty tree, each silent:
`echo ${HOME}`, `echo {}`, `echo {a}`, `echo a{b}c`, `find . -name x -exec
echo {} \;`, `awk '{print}' f.txt`, a JSON argument in single quotes, `jq '{a:
.b, c: .d}' x.json`, `printf '%s' "${a,}"`, `echo "${x:-{a,b}}"`, `git log -g
@{1}`, `git log --format='{%h,%s}'`, `echo $'{a,b}'`, `echo ${a,b}`, and a
commit message heredoc holding `{a,b}`. `$${a,b}` is not expanded by bash and
not matched. `{1..3..+1}` is not expanded by bash 3.2 and not matched.

Fix: allow a sign on every sequence number, and test the frozen words with a
pattern that drops the lookbehind and the whitespace exclusion, read only
where the text test already found an unquoted brace. The over-stop it adds is
a `${x,}` word in a command that already holds an unquoted brace. Executed
over the corpus with the fix: 33 pairs stopped, the same 33 as without it.

## 🟡 3 — §A says no stopped pair is git, and one is

`docs/worktree-guard-spec.md:106` and `:171`, pinned by
`tests/test_guard_resolves_the_tree_it_judges.py:855`.

§A says the rule stops 31 of 32,498 pairs, "every one a command that is not
git". Re-measured by the method `phases/phase-7.md` writes down, through the
guard's own `_segment_finding` and `_command_findings` at the target: 33 of
32,641 pairs, and one of them stops in a git segment, `git add
seal/specs/<id>/{plan,questions}.md`, from a 2026-09-23 transcript. The hooks
at `a8f86f44` stop exactly that one pair through `_git_finding`, so it is the
owner-confirmed rule (c) that stops it, before any reframe. Phase 1's M2,
zero git pairs over 32,431, misses it the same way. The self-check passed in
every run: 19 of 19 round 1–3 spellings stop, 0 of 6 quoted forms do. No
assignment word and no quoted brace beside an unquoted one is among the 33.

The method as written and the figure disagree, and the deleted probe that
produced the figure cannot be re-read, so which step diverged is not
established. The count's size is close; what is wrong is the claim that no
git command pays. That claim is the one P1 puts in front of the owner, who
has not answered yet.

Fix: write the git share, and the pin that holds the sentence.

## ⬜ 4 — a brace in a command the splitter cannot close is read only for a bare `git`

`hooks/worktree-guard.py:2409`.

`: $'\'' && {g..g}it switch feature/x && : "'"` is silent in an ACTIVE tree,
and bash runs `git switch feature/x`. ANSI-C quoting makes the plain-quote
readers disagree with bash (`hooks/tokens.py` names this disagreement): the
splitter cannot close the command, and `QUOTED_SPANS` reads the brace as
quoted, so `_unquoted_brace` is false. The untokenizable arm then asks only
`_holds_git`, and `{g..g}it` holds no bare `git`. The same command with
`{git,}` denies, through that arm.

The class is older than this branch. `g""it` in place of the brace is silent
at the target and at `5623d728`, so the arm reads every git spelling that
avoids the bare word as nothing. That part goes to the Deferred table. The
brace part is the reframe's own claim, and one line keeps it: an
untokenizable command holding a brace pattern anywhere stops, in the
stopping direction a broken reader already takes.

## ⬜ 5 and ⬜ 6 — corrections to the run's paperwork

⬜ 5. The false git share is copied into ledger row S22
(`seal/ledger/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way.md:86`),
the changelog fragment (`changelog.md:55`), `questions.md` M2, M4 and P1, and
`phases/phase-7.md:23`. Each follows 🟡 3's corrected sentence.

⬜ 6. The 30 marker lines are a fair use. `skills/code-review/SKILL.md`
names this exact use, a record deliberately calling a name gone, and every
added marker sits beside a removed unit's name without changing a claim
(executed: 30 added lines carry the marker across `spec.md`, `plan.md` and
the round 2–3 records). Three insertions, though, landed mid-sentence where
a line broke. At `rounds/round-2-report.md:85` the marker stands between a
removed unit's name and the line number that belongs to it; at `:91` it
stands between "so the" and "segment is no git"; at `plan.md:112-113` it
interrupts a parenthesis. Moving each marker to the end of its sentence
keeps the exemption and the sentence.

## Round 3's agenda

- **Yellows 1–3 are closed.** Every one of the 19 spellings rounds 1–3 found
  stops in an ACTIVE tree and is silent in a clean single-stream tree
  (executed at the target, through `main()` for the round 3 forms and
  through `_segment_finding` for all 19). The rule reads no position, so the
  next spelling of the same kind needs no fix: `x=1; {g..g}it`, an `if` body,
  a pipe, `<( )` and a backtick body each deny.
- **White 4 is closed.** `[None-None]` and `[-]` fail with
  `hooks/session-lease.py` at `e0c5a191` and pass at the target (executed).
- **White 5 is answered by design.** An assignment brace stops, a named
  cost; bash 3.2.57 and zsh each print `{a,b}` for `A={a,b}; printf %s
  "$A"` (executed), so the cost is a stop on a word the shell leaves alone,
  as In 5 says.
- **White 6 is closed for the method.** The method is written down, and it
  matches phase 1's: the same corpus, the judgment text, substitution bodies,
  `QUOTED_SPANS`, the self-check first. Its git split is 🟡 3.
- **Round 3's question** on assignment-word expansion is answered by M5.

## What was asked, answered

| Question | Answer |
|---|---|
| Does `_BRACE` match bash? | No in two forms (🟡 2); everything listed above as left alone is left alone |
| Is any brace still read past? | Rounds 1–3's shapes: none. `$'…'`: one, behind the untokenizable arm (⬜ 4). Here-strings: `bash <<< '{git,} switch feature/x'` is silent, and so is `bash <<< 'git switch feature/x'` with no brace, at `5623d728` too, so a here-string handed to a shell is unread whatever it holds (Deferred). `cat <<< {a,b}` stops although bash does not expand a here-string word, which is cost 3's direction |
| Can the `-C` union miss? | Yes, two ways (🟡 1). `-C ~/W` and `cd W && {git,} …` are read |
| Was 31 measured by phase 1's method? | The method is phase 1's; the git split it reports is not what the method gives (🟡 3) |
| Are the markers fair? | Yes; three insertions split a sentence (⬜ 6) |

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | The `-C` union misses the tree git runs in: a git segment whose brace stands before its `-C` (`git {,} -C W switch feature/x`), and `-C` values git composes (`{git,} -C .. -C W switch feature/x`) | `hooks/worktree-guard.py:2485` | open | executed: both silent with the session's tree clean and `W` ACTIVE; bash hands git `-C W …` and `-C .. -C W …`; the brace-free `git -C .. -C W switch feature/x` denies naming `W`; the fix makes all three new parameters deny, 400 passed |
| 🟡 2 | `_BRACE` refuses a signed sequence endpoint (`git rebase main{+1..2}`) and a brace after an escaped `$` (`\${a,b}`), both expanded by bash | `hooks/worktree-guard.py:2007` | open | executed: bash 3.2.57 prints `1 2 3` for `{+1..3}` and `$a $b` for `\${a,b}`; `git rebase main{+1..2}` silent in an ACTIVE tree at the target; the fix stops both, 33 corpus pairs before and after |
| 🟡 3 | §A says every pair the rule stops is a command that is not git; one is a git segment, `git add <dir>/{plan,questions}.md` | `docs/worktree-guard-spec.md:106` | open | executed: phase 7's method through the guard's own functions: 33 of 32,641, one git; the hooks at `a8f86f44` stop that pair alone; self-check 19 of 19 and 0 of 6; the pin at `tests/test_guard_resolves_the_tree_it_judges.py:855` holds the false sentence |
| ⬜ 4 | An unquoted brace in a command the splitter cannot close (ANSI-C `$'\''`) is read only for a bare `git`: `{g..g}it switch feature/x` there is silent | `hooks/worktree-guard.py:2409` | open | executed: silent in an ACTIVE tree, bash runs `git switch feature/x`; `{git,}` in its place denies; the brace-free `g""it` twin is silent at `5623d728` too, so the class is deferred and only the brace line is proposed |
| ⬜ 5 | The false git share is copied into ledger row S22, the changelog fragment, `questions.md` M2, M4, P1 and phase 7 | `seal/ledger/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way.md:86` | open | a correction of the run's paperwork, following 🟡 3 |
| ⬜ 6 | Three `NAME NOT IN TREE` insertions split a sentence; the markers themselves are a fair use | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-2-report.md:85` | open | a correction of the run's paperwork; also `:91` and `plan.md:112`; 30 marker lines counted in the range |
| 🟢 | round 3's yellow 1 is closed — a brace behind a runner's operand, a redirection or a glued `(` stops | `tests/test_worktree_guard.py:1937` | confirmed | executed: each denies in an ACTIVE tree and is silent in a clean one, through `main()` and `_segment_finding` |
| 🟢 | round 3's yellow 2 is closed — empty and runner alternatives stop | `tests/test_worktree_guard.py:1945` | confirmed | executed: the four spellings deny in an ACTIVE tree |
| 🟢 | round 3's yellow 3 is closed — a brace after an `&` cut stops | `tests/test_worktree_guard.py:1949` | confirmed | executed: denies; every segment now carries the brace test, so the cut needs no reader of its own |
| 🟢 | round 3's white 4 is closed — the lease case can fail | `tests/test_lease_liveness.py:402` | confirmed | executed: `[None-None]` and `[-]` fail with the lease writer at `e0c5a191`, 6 pass at the target |
| 🟢 | round 3's white 5 is answered — an assignment brace stops, a named cost | `docs/worktree-guard-spec.md:102` | confirmed | executed: bash and zsh print `{a,b}` for an assignment; no recorded pair stops on one |
| 🟢 | round 3's white 6 is closed for the method — `phases/phase-7.md` writes it down | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/phases/phase-7.md:38` | confirmed | read: the six steps match phase 1's; the git split it reports is 🟡 3 |
| 🟢 | round 3's question on assignment-word expansion is answered | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/phases/phase-7.md:32` | confirmed | executed: M5 re-run under bash 3.2.57 and zsh, both `{a,b}` |
| 🟢 | rounds 1–2's closures stand — their brace spellings are in the reframed case | `tests/test_worktree_guard.py:1924` | confirmed | executed: round 1's and round 2's six spellings stop; the units they were fixed in left the tree and nothing reads their names |
| ❓ | Whether a hook process sees `CLAUDE_PID` and `CLAUDE_CODE_SESSION_ID` (round 1's and round 2's questions) | `hooks/hooksession.py:68` | ❓ out of verified scope | not reopened: the range does not touch it; the repository owner answers it, as `overview.md` names |

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

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| A command substitution that leaves no word before `git` (`$( ) git switch feature/x`) or builds it (`$(echo git) switch feature/x`) is silent in an ACTIVE tree, at `5623d728` and at the target; bash and zsh run `git switch feature/x`. `{$( ),} git …` is the same hole with a brace around it | a new issue, not opened by this round | the repository owner, who decides whether the guard reads a command word a substitution makes |
| A here-string or heredoc handed to a shell (`bash <<< 'git switch feature/x'`) is not read, with or without a brace, at `5623d728` and at the target | a new issue, not opened by this round | the repository owner |
| An untokenizable command is read only for a bare `git` (P4 (a) of work item 1791270162): `g""it` behind ANSI-C `$'\''` is silent at `5623d728` and at the target | a new issue, not opened by this round; ⬜ 4 takes only the brace line | the repository owner, whose answer P4 (a) was |
| `git --git-dir=W/.git --work-tree=W switch feature/x` is judged in the session's tree, at `5623d728` and at the target | a new issue, not opened by this round | the repository owner |

## Paste-ready fixes

### 🟡 1

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

### 🟡 2

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

### 🟡 3

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

### ⬜ 4

```python
# in _command_findings, the untokenizable arm: a brace counts too, read off
# the raw text, because the quoting the splitter could not close is the
# quoting `_unquoted_brace` reads (round 4 of work item 1791384157, white 4).
    if not clean and (_holds_git(text) or _BRACE.search(text)):
        found.append(Finding("untokenizable", " ".join(text.split())))
```

Needs a fix: yes — 🟡 1 (the `-C` union misses the tree git runs in), 🟡 2 (`_BRACE` refuses a signed sequence and a brace after an escaped `$`), 🟡 3 (§A and its pin say no stopped pair is git)
Loses a record or crashes: no

The broad gate has not come due: this round leaves three findings needing a
fix, so the sealer's spawn waits for the round that verifies them.

## Proof block

Files opened in this round, at `df73a69c` unless named:

- `hooks/worktree-guard.py` (lines 1995–2489, 2940–3070, the range's diff)
- `hooks/tokens.py` (lines 36–70)
- `hooks/cmdline.py:3082`, `hooks/cmdline_base.py:2272`
- `tests/test_worktree_guard.py` (lines 1–145, 1112–1150, 1870–2175)
- `tests/test_guard_resolves_the_tree_it_judges.py` (the two brace policy pins)
- `tests/test_lease_liveness.py` (the range's diff), `tests/conftest.py:820`
- `docs/worktree-guard-spec.md` (lines 88–110, 168–173, 845–935, the range's diff)
- `docs/round-record-spec.md` (lines 295–345)
- `skills/evidence-check/SKILL.md` (lines 640–670), `skills/evidence-check/scripts/evidence_check.py` (lines 5000–5060), `skills/code-review/SKILL.md` (lines 365–385)
- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/`: `spec.md`, `questions.md`, `routing.md`, `plan.md` (the range's diff), `phases/phase-1.md` (lines 40–75), `phases/phase-7.md`, `phases/phase-9.md`, `rounds/round-1.md`, `rounds/round-2.md`, `rounds/round-3.md`, `rounds/round-2-report.md` (lines 83–93), the range's diff of every round file
- `seal/ledger/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way.md:78`, `:86`, `changelog.md` (lines 50–60)
- `bin/test`
