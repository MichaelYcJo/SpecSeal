# 1791384157-the-hooks-read-the-session-waiver-and-creation-one-way — round 5 report

Written by specseal:warden on Opus 5.5. Target SHA
`b9a4bcffd0ecc859ba86a6329974bcb9631097e5`, PR 881. This is a verifying
round. Its target is round 4's fix diff `fba9fff0..08f34e45` (731c3c17 code,
46d8181c records, 08f34e45 comment and survivors), with be9f243a and
b9a4bcff.

## What this round was asked

The spawn asked for three judgments and one check. First, whether the brace
test now stops on every shape round 4 found and keeps every must-not-stop
form silent. Second, whether the `-C` composition is right for absolute paths
and for `-C ''`. Third, whether the 34-pair measurement's method is written
down well enough to re-run. The check was to run the eight guard modules
once. Round 4's `New units` were a finding surface.

The account arrived labelled. The orchestrator's direction to the fix pass
was read: err toward stopping, with no exceptions for signs or an escaped
`$`. The smith's account was read: one kept exception (a `$` directly before
`{`), 13 silent forms pinned, the `-C` union composed, the untokenizable line
read for a brace, 34 of 32,715 with one git pair, six mutations red, 773
passed. Each claim below is checked against the code. Probes ran in a
`git clone --no-local` of the worktree at the target, under the session's
scratchpad, and nothing was written in the worktree but this report.

## How the answers relate

```
round 4's six verdicts ............ all closed at the target (executed)
   |
   +-- yellow 2's direction: "err toward stopping"
         |
         +-- the brace test still reads two things as word facts
               that bash does not:
               (1) a quote taken out leaves its `$` before the `{`  -> 🟡 1
               (2) whitespace inside `$( )`, backticks or `${ }`
                   ends the word                                     -> 🟡 2
         +-- the bias's own cost: a reflog range stops, unnamed      -> ⬜ 3
   |
   +-- yellow 3's re-count: steps 1-5 re-run to 34 and one git;
         the self-check it ran is not the one written down           -> ⬜ 4
```

## 🟡 1. A `$` before a quote still reads as a parameter expansion

`_unquoted_brace` takes every quoted span and escape out with nothing in its
place (`hooks/worktree-guard.py:2046`). A `$` that begins an ANSI-C or a
locale quote (`$''`, `$'x'`, `$""`) is not part of the span
`tokens.QUOTED_SPANS` matches, so it stays behind and lands directly before
the next `{`. `_BRACE`'s one kept exception, `(?<!\$)`, then reads
`$''{g..g}it` as `${g..g}it`, a parameter expansion, and the command holds no
brace.

Bash 3.2.57 and zsh 5.9 both make `$''{g..g}it` the single word `git`. A
fake `git` on bash's path printed `switch feature/x` for
`$''{g..g}it switch feature/x`. The guard at the target is silent on it in a
tree another session is ACTIVE in, and on `$''{g..g}it rebase main
feature/x`, `$""{git,} -C . switch feature/x` and `echo $'x'{a,b}`
(executed).

This is round 4's yellow 2 again in a new spelling. Round 4's `\${a,b}` was
fixed because the escape takes its `$` with it; a quote that begins with `$`
leaves the `$` behind. The orchestrator's direction allowed no exception but
a real `${`, and this is not one.

The fix is to let a quoted span stand in as one character instead of none.
Its paste-ready form is under `## Paste-ready fixes`, and it was applied in
the clone. The six new parameters were red at the target and green with it.
The 13 silent forms stayed silent, and the three guard modules passed.

## 🟡 2. Whitespace inside a substitution ends the brace's word

`_BRACE` reads "the same word" as a run of non-whitespace,
`\{\S*?(?:,|\.\.)\S*?\}` (`hooks/worktree-guard.py:2021`). Bash does not end
a word at whitespace inside `$( … )`, a backtick pair or `${ … }`. So
`{git,$(: x)}`, `` {git,`: x`} `` and `{git,${x:- }}` are each one word to
bash, and bash makes `git` of each: the second alternative expands to
nothing, or to a space that word splitting removes. Bash printed `[git]` for
all three, and the fake `git` ran `switch feature/x` for the `$( )` and the
`${ }` forms. zsh keeps an empty word there, so under zsh git refuses the
command.

The guard misses them twice. The text test does not match, because the
`\S` run stops at the space. The word test (`_BRACE_IN_WORD`, at `:2212` in
`_git_finding` and `:2302` in `_segment_finding`) is asked once per word the
frozen splitter made. The splitter cuts `{git,$(: x)}` into `{git,$(:` and
`x)}`, and neither word holds a whole brace. All three spellings, with
`switch feature/x` after them, are silent in an ACTIVE tree at the target
(executed).

This is not #886. #886 holds a substitution that makes the command word.
Here the brace makes it, and `{git,${x:- }}` holds no command substitution at
all. The cause is the brace test's idea of a word, which is this work item's
rule.

The fix has two parts, and both were applied in the clone. First, the text
test stands each substitution body and each parameter expansion in as one
character. Second, the segment test reads the segment's words joined, so a
brace the splitter cut in two is still one match. With both, the three
spellings deny in an ACTIVE tree. The 13 silent forms stay silent, because
none of them holds an unquoted brace for the command-level test to find. The
corpus count did not move: 34 of 33,088 under the method, the word test and
the joined test alike.

Both 🟡 sit in units round 4's fix rewrote (`_BRACE` at `:2021`) or that
predate it (`_unquoted_brace`, `_segment_finding`, `_git_finding`). Neither
sits in a unit round 4's fixes created.

## ⬜ 3. A reflog range stops, and nothing names it

`git diff HEAD@{1}..HEAD@{0}` and `git log @{u}..@{1}` each ask in a dirty
tree, naming the brace shape (executed). Bash expands neither. The rule as
§A writes it covers them: an unquoted `{` with a `..` before a later `}` in
the same word. But §A's list of what stays silent names `@{-1}`
(`docs/worktree-guard-spec.md:80`), and a reader will take that for reflog
syntax in general.

This is the stopping direction the orchestrator chose, so the release
ships no defect. No recorded pair in the corpus is one of these. The ⬜ asks
for one clause in §A naming the cost, and nothing else.

## ⬜ 4. The 34-pair method re-runs, but its self-check is not the one written

Steps 1 to 5 of `phases/phase-7.md` re-run cleanly. A probe written from
those steps alone, with the guard at the target, counted 34 of 33,077 pairs:
one git segment, no assignment word. That matches the record. The corpus has
grown since 32,715, as the record says it will.

Step 6 and the `Self-check` line still name nineteen must-stop spellings and
six quoted forms (`phases/phase-7.md:75` and `:81`), and `questions.md` M4
says the same. The fix pass reports 21 of 21 and 0 of 15, and so do
`overview.md:29` and the ledger row S22. S22 carries both figures in one
row. The two extra must-stop spellings and nine extra must-not forms are
written down nowhere, so the self-check behind 34 cannot be re-run as it
ran.

One smaller point belongs with it. Step 4 names `_BRACE` for the word test,
and the guard asks `_BRACE_IN_WORD`. Both give 34 and one git pair. Under
the guard's own test, the zsh `${(f)…}` pair's assignment word matches, so
the assignment column reads 1 and not 0. The prose already names that pair.
The table's 0 is correct only for step 4 as written.

This is a correction to the run's paperwork, under `seal/specs/` and
`seal/ledger/`, and it is not counted in `Needs a fix`.

## Round 4's verdicts

- **Yellow 1, the `-C` union.** It is closed. The four new parameters failed
  with the `hooks/worktree-guard.py` of `fba9fff0` and pass at the target.
  Seven more spellings were probed with the session's tree clean and `W`
  ACTIVE, and each denies naming `W`. They were `-C .. -C '' -C W`, the same
  with `""`, `git {,} -C .. -C '' -C W`, an absolute first value, an
  absolute value after a relative one, `git {,} -C nowhere -C <abs W>` and
  `-C '' -C .. -C W`. The splitter keeps `''` as an empty word, and
  `apply_chdir`'s `os.path.join` leaves the directory unchanged on it and
  resets on an absolute value, as git does.
- **Yellow 2, signed sequences and `\${a,b}`.** It is closed for every
  spelling round 4 named. The four new parameters failed at `fba9fff0` and
  pass at the target. The class it belongs to is still open, as 🟡 1 and
  🟡 2 above.
- **Yellow 3, §A's false sentence.** It is closed. §A says 34 of 32,715 with
  one git pair (`docs/worktree-guard-spec.md:116`), the pin carries the new
  sentence and refuses the old one, and the re-run above reproduces the
  split.
- **White 4, the brace in an untokenizable line.** It is closed: the new
  test failed at `fba9fff0` and passes at the target.
- **White 5, the copied share.** It is closed. Outside the round records,
  the old figure survives only where a record says what phase 7 first gave.
- **White 6, the markers.** It is closed. Each of the three markers now ends
  its sentence, and the eight guard modules pass.

## Round 4's new units

- `_BRACE_IN_WORD` is right as a pattern: it crosses whitespace and takes no
  `$` exception, as its comment says. Where it is asked is the second half of
  🟡 2: once per word, after the splitter has cut a brace in two.
- `test_a_brace_segment_composes_its_c_values_as_git_does` is sound. Both
  parameters failed at `fba9fff0`.
- `test_what_the_shell_does_not_expand_stays_silent` can fail. With `_BRACE`
  mutated to cross whitespace and drop the `$` exception, two parameters
  failed: `echo ${a,}` and the `&& echo {c, d}` form. The bare `echo {a, b}`
  did not fail, because the word test silences it on its own. The test is
  still a fair pin.
- `test_a_brace_in_a_command_that_will_not_split_stops` is sound. It failed
  at `fba9fff0`.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A `$` that begins a quote (`$''`, `$'x'`, `$""`) is left before the `{` when the quote is taken out, so `$''{g..g}it switch feature/x` reads as a parameter expansion and is silent in an ACTIVE tree; bash and zsh run `git switch feature/x` | `hooks/worktree-guard.py:2046` | open | executed: bash 3.2.57 and zsh 5.9 make `$''{g..g}it` the word `git`, a fake git ran `switch feature/x`; four spellings silent in an ACTIVE tree at the target; with the fix the three proposed parameters are red at the target and green, the 13 silent forms stay silent |
| 🟡 2 | Whitespace inside `$( … )`, backticks or `${ … }` ends the brace's word for `_BRACE` and for the per-word test, so `{git,$(: x)} switch feature/x`, its backtick twin and `{git,${x:- }} switch feature/x` are silent in an ACTIVE tree; bash runs `git switch feature/x` | `hooks/worktree-guard.py:2021` | open | executed: bash prints `[git]` for all three and a fake git ran `switch feature/x`; the splitter cuts the word into `{git,$(:` and `x)}`; with the fix all three deny, three guard modules 416 passed, corpus 34 of 33,088 unchanged; also `:2212` and `:2302`; not #886, whose command word a substitution makes |
| ⬜ 3 | A reflog range (`git diff HEAD@{1}..HEAD@{0}`, `git log @{u}..@{1}`) asks in a dirty tree, and §A's silent list names `@{-1}` without saying that a range across two reflog braces stops | `docs/worktree-guard-spec.md:80` | open | executed: both `ask`, naming the brace shape; it is the stopping direction the orchestrator chose, so one clause naming the cost is all it asks |
| ⬜ 4 | The 34-pair self-check ran 21 must-stop and 15 must-not forms, but phase 7 step 6, its `Self-check` line and `questions.md` M4 name 19 and 6, the extra forms are written nowhere, and ledger S22 carries both figures | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/phases/phase-7.md:75` | open | a correction of the run's paperwork; executed: steps 1 to 5 re-run to 34 of 33,077, one git, none assignment; step 4's `_BRACE` and the guard's `_BRACE_IN_WORD` agree on 34 and differ on the assignment column (0 against 1) |
| 🟢 | round 4's yellow 1 is closed — the `-C` union composes in order and covers a git segment whose brace stands before its `-C` | `hooks/worktree-guard.py:2488` | confirmed | executed: the four new parameters fail with the guard of `fba9fff0` and pass at the target; seven more spellings with `-C ''`, `-C ""`, absolute values first and mid-chain each deny naming `W` |
| 🟢 | round 4's yellow 2 is closed — a signed sequence and a brace after an escaped `$` stop | `hooks/worktree-guard.py:2021` | confirmed | executed: the four new parameters of the brace-shape test fail at `fba9fff0` and pass at the target; the class stays open as this round's 🟡 1 and 🟡 2 |
| 🟢 | round 4's yellow 3 is closed — §A says 34 of 32,715 with one git pair, and its pin holds the sentence | `docs/worktree-guard-spec.md:116` | confirmed | read: the sentence and its pin at `tests/test_guard_resolves_the_tree_it_judges.py:828`; executed: phase 7's steps 1 to 5 re-run to 34 with one git pair |
| 🟢 | round 4's white 4 is closed — an untokenizable line holding a brace stops | `hooks/worktree-guard.py:2430` | confirmed | executed: the new test fails at `fba9fff0` and passes at the target |
| 🟢 | round 4's white 5 is closed — the corrected count reaches every record that copied the old one | `seal/ledger/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way.md:86` | confirmed | read: a search of `docs/`, `seal/ledger/` and the work item outside its round records finds the old figure only where a record states what phase 7 first gave |
| 🟢 | round 4's white 6 is closed — each marker ends the sentence it split | `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-2-report.md:85` | confirmed | read: the diff at 46d8181c; executed: the eight guard modules pass |

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
| phase 7 steps 1 to 5, written from the record alone, guard at the target | 34 of 33,077 pairs; one git; assignment 0 with step 4's `_BRACE`, 1 with the guard's `_BRACE_IN_WORD` |
| the paste-ready fixes for 🟡 1 and 🟡 2 applied in the clone | the six proposed parameters fail at the target and pass with the fixes; the brace-shape and silent tests 33 passed; `tests/test_worktree_guard.py`, `tests/test_guard_resolves_the_tree_it_judges.py` and `tests/test_the_guard_asks_once_per_session.py` exit 0, 416 passed; corpus 34 of 33,088 by step 4, the word test and the joined test |
| `gh pr checks 881` at `b9a4bcff` | exit 0: lint, ledger, release, both grammar jobs, ubuntu, three macOS groups and four Windows groups pass |
| `bin/evidence-check --strict`, `survivor-check`, `correction-check` | not run by this round; the smith's exit 0 is carried, and the sealer's broad gate runs them |
| the broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The four silent shapes round 4 found before this branch (a substitution that makes the command word, a here-string to a shell, `g""it` in an untokenizable line, `--git-dir`) | #886, already deferred in round 4 | the repository owner |

## Paste-ready fixes

### 🟡 1 and 🟡 2, `hooks/worktree-guard.py`

Applied together in the clone and verified as described above. 🟡 1 is the
`"q"` in place of `""`. 🟡 2 is the substitution and parameter stand-ins and
the joined segment test.

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

### 🟡 1 and 🟡 2, `docs/worktree-guard-spec.md` §A, lines 80 to 82

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

The last full sentence before the raw-text sentence answers ⬜ 3, and the
smith may drop it if ⬜ 3 is answered otherwise.

### 🟡 1 and 🟡 2, the pin in `tests/test_guard_resolves_the_tree_it_judges.py`

```python
        # Round 5, yellows 1 and 2.
        "and neither is a `$` before a quote",
        "A command substitution or a parameter expansion is part of the word it "
        "stands in",
```

## Regression tests to plant

- `tests/test_worktree_guard.py`, the parameter list of
  `test_a_brace_in_any_word_is_the_brace_shape`, after `'echo {"a b",c}'`.
  Each was seen red at the target and green with the fix in the clone.

```python
        # Round 5, yellow 1: a `$` before a quote is no parameter expansion
        # (`$''{g..g}it` is `git` to bash and zsh).
        "$''{g..g}it switch feature/x",
        "echo $'x'{a,b}",
        'echo $""{a,b}',
        # Round 5, yellow 2: a substitution or a parameter expansion is part
        # of the word it stands in, whatever whitespace it holds.
        "{git,$(: x)} switch feature/x",
        "{git,`: x`} switch feature/x",
        "{git,${x:- }} switch feature/x",
```

- `tests/test_worktree_guard.py`, the parameter list of
  `test_a_brace_segment_composes_its_c_values_as_git_does`, optionally:
  `"{git,} -C .. -C '' -C W switch feature/x"`. It passes at the target, so
  it pins present behaviour. It is planted only if a mutation shows it red
  first, for example skipping an empty `-C` value in the composition.

## Facts for the evidence ledger

- S11b and S22: the brace rule stops a `$''{g..g}it`, `{git,$(: x)}` and
  `{git,${x:- }}` command word once 🟡 1 and 🟡 2 are fixed. Executed in this
  round's clone: the corpus count stays 34, with one git pair, over 33,088
  pairs.
- S22: the self-check figure has to be one figure, with its forms written in
  `phases/phase-7.md` step 6 (⬜ 4).

## The broad gate

Not yet. The sealer runs it once, after the rounds settle. This round leaves
two 🟡 open, so it has not come due.

Needs a fix: yes — 🟡 1 (a `$` before a quote hides a brace that makes `git`), 🟡 2 (whitespace inside a substitution or a parameter expansion ends the brace's word)
Loses a record or crashes: no

## Proof block

Files opened by this round:

- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-4.md`
- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-4-fixes.md`
- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/rounds/round-4-report.md` (its tail through `cat`, and `:81-180`)
- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/phases/phase-7.md`
- `seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/overview.md:29`, `questions.md:74`
- `seal/ledger/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way.md:86`
- `hooks/worktree-guard.py:2000-2057`, `:2380-2519`, `:2990-3099`, and the diff `fba9fff0..08f34e45`
- `hooks/cmdline_base.py:2265-2288`, `hooks/worktree_consent.py:483-523`, `hooks/tokens.py:67-82`
- `tests/test_worktree_guard.py:1095-1135`, `:1986-2160`
- `tests/test_guard_resolves_the_tree_it_judges.py:849-868` (the diff)
- `docs/worktree-guard-spec.md:69-125` (the diff), `:72-83`
- `bin/test`
- #886's title and body, through `gh issue view`
