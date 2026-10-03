# Round 2 report — work item 1790993140 (#716, #678's guard half, #686)

| Field | Value |
|---|---|
| Round | 2, verifying |
| Target SHA | `f1629706` |
| Fix range | `25e5b01a..2f4e9933` (ten commits), then round 1's close commit `f1629706` |
| Earlier rounds | `rounds/round-1.md`, `rounds/round-1-report.md` |
| Ran by | specseal:warden on claude-opus-5-5 |

This round reads round 1's fixes, not the branch. Round 1's record and report
were read for coordinates; every verdict below was re-derived at `f1629706`.
The fix pass's account (the commit messages, the ledger notes, the comments in
the code) was read whole and treated as claims.

## Summary

All seven of round 1's findings are closed as round 1 named them. Two of the
fixes opened new defects, and each is in the class the fix was aimed at:

1. **Candidate C's per-view comparison (round 1's finding 3) made three shapes
   that asked go silent** (🟡 8). It compares a cut or glued view with the
   frozen parser. The frozen walk never reads those views, so
   `git switch>/dev/null x` is no switch to the frozen loop, yet its cut view
   reads as one to the frozen parser, and the kind is subtracted. At round 1's
   target the guard asked about it.
2. **Env's own-options state (round 1's finding 2) ends too early in two
   ways** (🟡 9, 🟡 10). An abbreviated long option that takes a value
   (`--un FOO`) and a redirection among env's options (`env 2>/dev/null -iS`)
   each end it. A commit-carrying cluster behind either is found by nothing.
3. **The same state ends too late at `--`** (⬜ 11): `env -- -iS '…'` denies
   in a declared repository, where the base was silent.

The fixes for all four were applied together in the round's clone. They pass
the four narrow modules, and the new cases fail against `f1629706`. The fix
for 🟡 8 fires on 0 of the 27,351 recorded pairs, the same as the built code
and round 1's target, so the owner's rule still holds for it.

One paperwork correction remains: `overview.md`'s divergence row about the
discards describes the code before the fix (⬜ 12).

## Round 1's fixes, each at its commit

- **Finding 1, `5d2a58f7` and `a8dfb388` — confirmed.** `command_strings`
  passes `env_words=False`, so it asks the expansion question of the split
  string alone. `_env_words` quotes every word but the string back into one.
  Executed: the six no-commit controls the fix added are silent in a declared
  repository (narrow run). Executed through `commit_invocations`:
  `env -S '-i' "$CMD"` is silent at `f1629706`. It is silent at `233f0455`
  too, and so is `env -i "$CMD"`, so the fix took back no stop the base made.
- **Finding 2, `ea53c0a3` — confirmed for the shapes it named.** The six
  `HANDED` shapes are found. The class is still open (🟡 9, 🟡 10, ⬜ 11).
- **Finding 3, `139bf5e6` and `cdc05d99` — confirmed.** Both restore shapes
  ask at `f1629706`. Executed: both fail against round 1's target's guard
  (2 failed, 4 passed). The four other new cases pass against the old guard
  too, which is expected. They pin the subtraction against an over-correction:
  without the per-view part a restore adds a question, and without `judged` a
  judged kind is asked again (read). The per-view comparison itself is what
  🟡 8 is about.
- **Finding 4 — still deferred to #734.** The fix range does not touch
  `ask_what_only_the_wider_reading_finds` (read). Already deferred in round 1.
- **Finding 5, `1bbc534b` — confirmed.** Executed: the new case passes, and
  fails once the line reads `except Exception:` alone.
- **Finding 6, `b32aa5ce` — confirmed.** W10's correction is round 1's fence
  verbatim (read).
- **Finding 7, `b59030bd` — confirmed.** M1's 2026-10-03 correction is
  round 1's fence verbatim (read). It was written in place over this work
  item's own unreleased correction, and the `Corrected` marker stands.

The prompt asked for confirmation rows that read `verified`. That word is in
no vocabulary: `skills/code-review/scripts/round_record.py` (the comment at
line 2283) reads it as OPEN. So the rows below read `confirmed`, as
`agents/warden.md` shows for a carried closure, with a bare marker and no
severity glyph in the row.

## The ledger

- **K3 and K5** are corrected in place, and each describes `f1629706`'s code
  (read). Both drift with this round's fixes. K5's corrected clause,
  *a view the frozen parser reads as the same kind*, is the rule 🟡 8 changes.
- **W10 and M1** are covered above.
- **The re-reads hold against the fixes** (read row by row). E14 says
  "`env -S` in three spellings", and its re-read note says "and more"; the
  claim stays true as a lower bound. E16 and I5 count seven new `env`
  controls, and the diff adds seven. I6 and I12 name only the env arm as
  changed, and that matches the diff. A4, A5, W1, W2, W4, W7, W9, W10 and the
  `seal/releases/0.9.1.md` row cite `main`. Only `quiet` changed there, and no
  row that speaks moved.
- **Executed:** `bin/evidence-check --ledger` on the fragment and the four
  release files reports 0 drifted and 0 broken in each.
- **`survivors.md`'s one row holds.** Executed: `bin/survivor-check --range
  25e5b01a..f1629706` names exactly one place, M1's original claim at
  `seal/releases/0.16.0.md:247`. With the work item's `survivors.md` as
  `--exempt`, it passes. The standing text is the claim the two `Corrected`
  notes after it are about, which is the correct-in-place rule.

## 🟡 8 — a redirection glued to the subcommand went from asked to silent

`hooks/worktree-guard.py:356` (`wider_only_kinds`).

**What is wrong.** The fix compares each wider view with the frozen parser
reading the same tokens. That is right for a raw segment, because the frozen
walk reads those same words. It is wrong for the two kinds of view the frozen
walk never reads: a merged group and a cut word (`unglued`). In
`git switch>/dev/null x`, the frozen walk reads the subcommand
`switch>/dev/null`, which is no switch. The cut view, `git switch >/dev/null
x`, is a switch to the frozen parser too. So the kind is subtracted, and
nothing in the frozen reading ever judged it.

**Executed.** Bash runs each shape: in a scratch repository,
`git switch>/dev/null fx` switched, `git worktree add>/dev/null …` added a
worktree, and `git checkout>/dev/null -b y` created and checked out `y`.
Through `main()`, over a dirty `w` under a clean session:

| Command | Round 1's target (`07a3dc7f`'s guard) | `f1629706` |
|---|---|---|
| `cd w && git switch>/dev/null feature/x` | ask | **silent** |
| `cd w && git checkout>/dev/null -b y` | ask | **silent** |
| `cd w && git worktree add>/dev/null ../wt-z b` | ask | **silent** |
| `cd w && git>/dev/null switch feature/x` | ask | ask |

**Why it matters.** `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it* says a switch
or creation only the commit gate's reading finds "is put to the person instead
of passing silently". Each shape above is found only by that reading, and
each was put to the person before the fix. This is the question the guard
asks. The only stop the guard puts on these shapes is gone, and a switch over
a tree another session is active in runs unasked.

**Fix.** Compare each view with the frozen parser's reading of the raw
segments it was made from. A raw segment is its own source, so the restore
case of round 1's finding 3 stays silent. A merged group's sources are its
parts, and a cut view's source is the segment it was cut from. Fenced below.

**Executed:** over D1's corpus (27,551 uses, 27,351 pairs), the fixed C fires
on 0, as do the built C and round 1's target's C. None raised, and no pair
answers differently across the three. A 43-shape set of the hidden classes
(redirections before and after `git`, cut and glued, zsh prefixes, spaced
options, runners, groups) gives the same answer under the fix as at
`f1629706`. The two exceptions are a restore before a hidden switch and a
second hidden creation, which now ask when nothing was judged. A glued
restore (`cd w && git checkout README.md>/dev/null`) stays silent.

## 🟡 9 — an abbreviated long option's value ends env's own options

`hooks/cmdline.py:1768` (`_env_takes_next`, `ENV_VALUED_LONG`). · NAME NOT IN TREE

**What is wrong.** `_env_takes_next` knows `--unset`, `--chdir` and `--argv0` · NAME NOT IN TREE
by their full names alone. GNU's getopt takes every unambiguous prefix of a
long option. `_env_split_at`'s docstring says so for `--split-string`, from · NAME NOT IN TREE
`--s`. `--un FOO` is therefore not read as taking a value, `FOO` reads as the
program, and the own-options state ends before the cluster.

**Executed** through `commit_invocations`: each is found by nothing at
`f1629706` and at `233f0455`:

- `env --un FOO -iS 'git commit -m x'`
- `env --ch /tmp -iS 'git commit -m x'`
- `env --ar x -iS 'git commit -m x'`
- `env --un FOO --split 'git commit -m x'`

**Read, not run:** GNU env accepts these prefixes. There is no GNU coreutils
on this machine, and macOS `env` has no long options. The claim rests on the
same getopt rule the fix already relies on for `--split`. The answerer is the
fix pass, if it can reach a Linux machine.

**Why it matters.** Contract §12. Round 1's finding 2 was this class: a
spelling of env's options its getopt accepts that the reader does not parse.
With `-i` in the cluster, the git hook stub sees no session either
(`spec.md`'s table, y09). So the command-reading gate is the only reader, and
a commit runs that no gate judges.

**Fix.** Read a long option that takes a value in every prefix, as
`_env_split_at` reads `--split-string`. No other long option of GNU `env` · NAME NOT IN TREE
starts with `u`, `c` or `a`. Fenced below.

## 🟡 10 — a redirection among env's options ends them

`hooks/cmdline.py:1739` (the env arm of `reparsed_texts`).

**What is wrong.** The arm ends the own-options state at the first word that
does not start with `-`. A redirection is such a word, but it belongs to the
shell, and env never sees it.

**Executed.** macOS `env 2>/dev/null -iS 'echo ran-behind-redirection'`
printed the line (exit 0). Each of these is found by nothing at `f1629706`
and at `233f0455`:

- `env 2>/dev/null -iS 'git commit -m x'`
- `env -u FOO 2>/dev/null -iS 'git commit -m x'`
- `env -u 2>/dev/null FOO -iS 'git commit -m x'`
- `env >/dev/null --split 'git commit -m x'`
- `env -i 2>&1 -vS 'git commit -m x'`

`env -iS 2>/dev/null 'git commit -m x'` is found, because `_string_at` reads
past a redirection after the option. Round 1 checked redirections around the
base spellings, which are read anywhere. Nothing checked them before a
cluster.

**Why it matters.** The same as 🟡 9. It is a separate finding because its
fix is in `reparsed_texts`, which existed before round 1, while 🟡 9's fix is
in a unit round 1's fixes created.

**Fix.** Step over a redirection, with a spaced target, while among env's own
options, using `redirection_width` as `command_strings` does. A value still
pending stays pending across it. Fenced below.

## ⬜ 11 — `--` does not end env's options, so a no-commit line now stops

`hooks/cmdline.py:1739`. `env -- -iS 'git commit -m y'` runs a program named
`-iS`, because `--` ends env's options. The arm keeps reading options past
`--` and takes `-iS` for a cluster. Executed: this command is a deny in a
declared repository at `f1629706` and silent at `233f0455`. It is the one
shape found where a fix turned a silent `env` line holding no commit into a
stop. No real program is called `-iS`, so this is ⬜, and it is fixed by one
condition. Fenced below.

## ⬜ 12 — `overview.md`'s divergence row describes the code before the fix

`seal/specs/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd/overview.md:27`.
The row says "no discard; `wider_only_kinds` already leaves out every kind the
frozen segments hold". Its grounds say "a discard could never change an
answer". Since `139bf5e6`, `quiet` hands the judged kinds over and
`wider_only_kinds` subtracts them. Round 1 showed that the old subtraction
could change an answer. Round 1's report also asked for a row naming the
`env -S` class; there is none. This is paperwork under `seal/specs/`, so it is
outside `Needs a fix`. A replacement row is fenced below.

## Regression tests to plant

All are fenced under *Paste-ready fixes*, and each was seen to fail against
`f1629706` (contract §15):

- `tests/test_guard_resolves_the_tree_it_judges.py`, `WIDER_ONLY`: the three
  glued shapes. They run through `test_candidate_c_finds_what_only_the_wider_reading_finds`
  and `test_what_only_the_wider_reading_finds_is_put_to_the_person`; 6 failed
  at `f1629706`.
- `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`,
  `HANDED`: three abbreviation shapes and four redirection shapes. `CONTROLS`:
  the `--` shape. 16 failed at `f1629706`, across
  `test_the_gate_stops_it`,
  `test_a_commit_in_a_string_or_a_substitution_is_read_as_unreadable`,
  `test_a_declared_repository_meets_no_new_stop` and
  `test_the_controls_read_no_hidden_commit`.

## Facts for the evidence ledger

- K5's clause *a view the frozen parser reads as the same kind* becomes,
  after 🟡 8's fix, *a view whose kind the frozen parser reads from one of the
  segments it was made from*. Its anchor on `wider_only_kinds` drifts.
- K3 drifts with 🟡 9, 🟡 10 and ⬜ 11. It should say that env's own options
  are read past a redirection and past an abbreviated long option's value, and
  that they end at `--`.
- Over D1's corpus, candidate C with 🟡 8's fix fires on 0 of 27,351 pairs,
  as the built C does. Executed 2026-10-03, round 2. It is a re-run of K5's
  measurement and needs no new anchor.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 8 | candidate C compares a cut or glued view with the frozen parser, which never reads such a view, so a redirection glued to the subcommand (`git switch>/dev/null x`) went from asked to silent | `hooks/worktree-guard.py:356` | open | executed: three glued shapes ask at round 1's target and are silent at `f1629706`, and bash runs each; the fix fires on 0 of 27,351 corpus pairs |
| 🟡 9 | an abbreviated long option that takes a value (`--un`, `--ch`, `--ar`) ends env's own options at its value, so `env --un FOO -iS 'git commit -m x'` is found by nothing | `hooks/cmdline.py:1768` | open | executed: four shapes found by nothing at `f1629706` and `233f0455`; read, not run on GNU env: getopt takes unambiguous prefixes, as `_env_split_at`'s docstring says | · NAME NOT IN TREE
| 🟡 10 | a redirection among env's options ends them, so `env 2>/dev/null -iS 'git commit -m x'` is found by nothing | `hooks/cmdline.py:1739` | open | executed: macOS `env` runs the string behind the redirection; five shapes found by nothing at `f1629706` and `233f0455` |
| ⬜ 11 | `--` does not end env's options, so `env -- -iS 'git commit -m y'` denies in a declared repository | `hooks/cmdline.py:1739` | open | executed: deny at `f1629706`, silent at `233f0455`; no real program is called `-iS` |
| ⬜ 12 | `overview.md`'s `quiet`'s-discards row describes the subtraction before the fix, and no row names the `env -S` class | `seal/specs/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd/overview.md:27` | open | read; paperwork correction, outside `Needs a fix` |
| 🟢 | round 1's finding 1 is closed — env's own words are not asked the expansion question, and are quoted back into one word each | `hooks/cmdline.py:1950` | confirmed | executed: the six added no-commit controls are silent in a declared repository; `env -S '-i' "$CMD"` is silent at `f1629706` as at `233f0455` and as `env -i "$CMD"` |
| 🟢 | round 1's finding 2 is closed for the shapes it named — a cluster ending in `S` and a `--split-string` prefix are read among env's own options | `hooks/cmdline.py:1736` | confirmed | executed: the six added `HANDED` shapes are found; the class is not closed, which is this round's findings 9, 10 and 11 |
| 🟢 | round 1's finding 3 is closed — a restore before a hidden switch no longer silences the question | `hooks/worktree-guard.py:2260` | confirmed | executed: both restore cases ask, and both fail against round 1's target's guard; the built C fires on 0 of 27,351 pairs, re-counted; the comparison it introduced is this round's finding 8 |
| 🟢 | round 1's finding 4 stays deferred — the fix range does not touch the consent read | `hooks/worktree-guard.py:361` | deferred #734 | already deferred in round 1; read: `ask_what_only_the_wider_reading_finds` has no diff in `25e5b01a..2f4e9933` |
| 🟢 | round 1's finding 5 is closed — the guarded import catches a module body that exits | `hooks/worktree-guard.py:145` | confirmed | executed: the new case passes, and fails with `except Exception:` alone |
| 🟢 | round 1's finding 6 is closed — W10 names the third command that names no tree | `seal/releases/0.15.6.md` W10 | confirmed | read: round 1's fence verbatim; executed: evidence-check reports 0 drifted, 0 broken |
| 🟢 | round 1's finding 7 is closed — M1's correction is narrowed | `seal/releases/0.16.0.md` M1 | confirmed | read: round 1's fence verbatim; executed: survivor-check names M1's original claim alone, and the one `survivors.md` row excuses it |
| 🟢 | the re-reads of E14, E16, I5, I6, I12 and of the rows citing `main` hold against the fixes, and K3 and K5 describe `f1629706` | `seal/releases/0.16.0.md`, `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` | confirmed | read row by row; executed: evidence-check on the five ledger files, 0 drifted, 0 broken |

## Executed probes

| What was run | Result |
|---|---|
| Narrow run at `f1629706`: the guard, wrapper, frozen-reading and gate-fails modules | 740 passed |
| Candidate C at round 1's target (`25e5b01a`'s hooks) and at `f1629706`, over 43 shapes of the hidden classes | one shape differs at the function: `git switch>/dev/null x` (switch, then nothing) |
| `main()` over four glued shapes, round 1's target and `f1629706`, dirty `w` under a clean session | three ask, then silent; `git>/dev/null switch` asks at both |
| Bash in a scratch repository: `git switch>/dev/null`, `git worktree add>/dev/null`, `git checkout>/dev/null -b` | each ran: the branch switched, a worktree was added, `y` was created |
| Corpus re-count over D1's cut: round 1's target's C, the built C, and the C with 🟡 8's fix | 27,551 uses, 27,351 pairs; each fires on 0; none raised; no pair differs across the three |
| `env` shapes through `commit_invocations` at `233f0455`, `f1629706` and with the fences | clusters behind an abbreviated value and behind a redirection: found by nothing at both commits, found with the fences; `env -- -iS`: found at `f1629706` only |
| macOS `env 2>/dev/null -iS 'echo …'` | ran the string, exit 0 |
| Round 1's restore cases with `25e5b01a`'s guard; the exiting-module case with `except Exception:` alone | 2 failed and 4 passed; 1 failed |
| The four fences applied in the round's clone, then the four narrow modules | 762 passed; ruff check and format clean on the four files |
| The new cases against `f1629706`'s code | guard module 6 failed; wrapper module 16 failed |
| `bin/evidence-check --ledger` on the fragment and four release files | 0 drifted, 0 broken in each |
| `bin/survivor-check --range 25e5b01a..f1629706`, with and without `survivors.md` | passes with it; without, one place, M1's original claim |
| Broad gate (full suite, repository-wide lint, typecheck) | not yet: the sealer's, after the rounds settle |

The probe files, the copies of earlier hooks, the scratch repositories and
the round's clone were deleted before hand-over.

## Paste-ready fixes

### 🟡 8 — compare a view with the segments it was made from

```python
# hooks/worktree-guard.py, wider_only_kinds
# Docstring: replace "and a view the frozen parser reads as the same kind is
# not hidden from it, so neither is reported" with "and a view's kind is hidden
# only where the frozen parser reads it from none of the segments the view was
# made from, so neither is reported".
    text = wide.drop_heredoc_bodies(wide.drop_comments(command))
    items, _clean = wide.split_segments_with_separators(text)
    segments = [tokens for _sep, tokens in items]
    # Each view beside the segments it was made from. The frozen walk reads
    # those segments as written, never a glued group or a cut word, so a kind
    # is hidden unless the frozen parser reads it from one of the view's own
    # segments: `git checkout README.md` is a restore to `classify` and must
    # not silence a switch behind a redirection after it, and `git
    # switch>/dev/null x` is no switch to the frozen parser, although its cut
    # view is (round 2 of 1790993140).
    sourced = [(tokens, [tokens]) for tokens in segments]
    sourced += [
        (tokens, [segments[i] for i in parts])
        for parts, tokens in wide.merged_view(items)
    ]
    wider = set()
    for view, sources in sourced:
        frozen = {switch_kind(parse_git(tokens)) for tokens in sources}
        for tokens in filter(None, (view, wide.unglued(view))):
            kind = switch_kind(wide.parse_git(tokens))
            if kind and kind not in frozen:
                wider.add(kind)
    return wider - set(judged)
```

```python
# tests/test_guard_resolves_the_tree_it_judges.py, WIDER_ONLY, after
# "--config-env, a switch"
    # Round 2 of 1790993140: a redirection glued to the subcommand's end.
    # bash runs each (executed); the frozen parser reads `switch>/dev/null`
    # as no subcommand, and only the cut view reads the kind. Silent at
    # `f1629706`, where the cut view was compared with the frozen parser.
    "a redirection glued to switch": (
        "cd w && git switch>/dev/null feature/x",
        "switch",
    ),
    "a redirection glued to checkout": (
        "cd w && git checkout>/dev/null -b y",
        "switch",
    ),
    "a redirection glued to add": (
        "cd w && git worktree add>/dev/null ../wt b",
        "creation",
    ),
```

### 🟡 9 — a long option that takes a value, in every prefix

```python
# hooks/cmdline.py
ENV_VALUED_LONG = ("--unset", "--chdir", "--argv0")


def _env_takes_next(t):
    """True where T is one of `env`'s options whose value is the next word.

    A long one in every prefix GNU's getopt takes, as `_env_split_at` reads
    `--split-string`'s: `--un`, `--ch`, `--ar`. No other long option of GNU
    `env` starts with `u`, `c` or `a` (round 2 of 1790993140).
    """
    if t.startswith("--"):
        return len(t) > 2 and any(name.startswith(t) for name in ENV_VALUED_LONG)
    middle = t[1:-1]
    return (
        len(t) > 1
        and t[-1] in ENV_VALUED
        and all(c.isalnum() and c not in ENV_VALUED for c in middle)
    )
```

```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py,
# HANDED, after "env -iS behind an option's value"
    # Round 2 of 1790993140: GNU's getopt takes a prefix of a long option
    # that takes a value too, so its value is still env's own word. Each
    # found nothing at `f1629706`.
    "env -iS behind --un's value": f"env --un FOO -iS '{C}'",
    "env -iS behind --ch's value": f"env --ch /tmp -iS '{C}'",
    "env --split behind --ar's value": f"env --ar x --split '{C}'",
```

### 🟡 10 — step over a redirection among env's options

```python
# hooks/cmdline.py, the env arm of reparsed_texts
            own, value, skip = True, False, 0
            for j, t in enumerate(rest):
                if skip:
                    skip -= 1
                    continue
                # A redirection among env's options is the shell's, and env
                # never sees it: `env 2>/dev/null -iS '…'` runs the string
                # (round 2 of 1790993140).
                width = redirection_width(rest, j) if own else 0
                if width:
                    skip = width - 1
                    continue
                at = _env_split_at(t, own and not value)
                # (the rest of the loop as it stands, with white 11's line)
```

```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py,
# HANDED, after yellow 9's three
    # Round 2 of 1790993140: a redirection among env's options is the
    # shell's, and env still reads the cluster after it (executed on macOS
    # `env`). Each found nothing at `f1629706`.
    "env -iS behind a redirection": f"env 2>/dev/null -iS '{C}'",
    "env -iS behind a redirection after a value": f"env -u FOO 2>/dev/null -iS '{C}'",
    "env -iS behind a redirection before a value": f"env -u 2>/dev/null FOO -iS '{C}'",
    "env -vS behind a cut redirection": f"env -i 2>&1 -vS '{C}'",
```

### ⬜ 11 — `--` ends env's options

```python
# hooks/cmdline.py, the env arm of reparsed_texts
                elif own and (t == "--" or not t.startswith("-")):
                    # `--` ends env's options: the next word is the program.
                    own = False
```

```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py,
# CONTROLS, after "a program's own cluster ending in S"
    # Round 2 of 1790993140: `--` ends env's options, so the word after it
    # is the program `-iS`, not a cluster. A deny at `f1629706`.
    "a program after env's --": "env -- -iS 'git commit -m y'",
```

### ⬜ 12 — the divergence rows

```markdown
| `quiet`'s discards | Plan §*What phase 4 builds*, C step 1: "For each kind the frozen loop did NOT find". Code: `quiet` hands the kinds the loop judged to `wider_only_kinds`, which subtracts them, and a view counts as hidden only where the frozen parser reads its kind from none of the segments it was made from | the loop's verdicts | `classify` judges fewer kinds than `switch_kind` reads from the same words, so subtracting the words' kinds let a restore silence a hidden switch (round 1, yellow 3); comparing a cut view with the frozen parser silenced a glued subcommand (round 2, yellow 8) |
| `env -S`'s spellings | Spec §*Scope* 1: "every spelling of `env`'s split string". Code: `-S`, `-S<s>`, `--split-string[=<s>]` anywhere, and among env's own options a cluster ending in `S` and every prefix of `--split-string`; env's own options are read past a redirection and an abbreviated long option's value, and end at `--` | getopt's spellings | round 1, yellow 2, and round 2, yellows 9 and 10: macOS `env` runs `-iS` and a cluster behind a redirection; GNU's getopt takes unambiguous prefixes |
```

Needs a fix: yes — 🟡 8 (a redirection glued to the subcommand went from asked to silent in the guard), 🟡 9 (an abbreviated long option's value ends env's own options), 🟡 10 (a redirection among env's options ends them)
Loses a record or crashes: no

The broad gate has not come due: three findings need a fix first.

## Proof block

Files opened in this round:

- `hooks/worktree-guard.py` at `f1629706`: the import block, `walk_command`,
  `switch_kind`, `wider_only_kinds`, `ask_what_only_the_wider_reading_finds`,
  `main`. Also `25e5b01a`'s copy, run beside it.
- `hooks/cmdline.py` at `f1629706`: `unglued`, `split_segments`,
  `split_segments_with_separators`, `merged_view`, `merged_segments`,
  `reparsed_texts`, `ENV_VALUED`, `ENV_VALUED_LONG`, `_env_takes_next`, · NAME NOT IN TREE
  `_env_split_at`, `_env_words`, `command_strings`, `names_an_unknown_command`, · NAME NOT IN TREE
  `_without_redirections`. `hooks/cmdline_base.py`: `walk_directories`, and a
  source comparison of every function the two readers share.
- `hooks/commit-review-gate.py`: `_reads_a_commit`, `_string_hides_a_commit`,
  `commit_invocations`.
- `tests/test_guard_resolves_the_tree_it_judges.py`,
  `tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py`
  (the fix range's diff and the tables it edits), `tests/conftest.py`
  (`load_hook_module`, `repo`), `tests/test_no_real_identifiers.py`.
- `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it*; `docs/round-record-spec.md`
  §*A verdict row that commissions nothing*;
  `skills/code-review/scripts/chain_check.py` (`CLOSED_WORDS`);
  `skills/code-review/scripts/round_record.py` (the verdict-word comment).
- The fix range's diff of `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md`,
  `seal/releases/0.9.1.md`, `0.15.5.md`, `0.15.6.md` and `0.16.0.md`, and the
  full K3, K5, W10, M1, E14, E16, I5, I6 and I12 rows.
- The work item's `rounds/round-1.md`, `rounds/round-1-report.md`,
  `survivors.md`, `overview.md`, and `questions.md` (D1, D3, D7).
