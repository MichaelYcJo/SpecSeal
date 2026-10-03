# 1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd — review round 2

| Field | Value |
|---|---|
| Target SHA | f1629706ae29452923d4a9304ff8ffefc88f2897 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 733 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `e74efba8dd0d72fc071a281eac9b2b562142d5f3..40214e980dd3a99339e20396cd5b933576645e4a`, 6 commits |
| Contract changes | none |
| New units | ENV_STRING (depth 1); ENV_OPTIONS (depth 1); _ENV_SHORT (depth 1); _ENV_LONG (depth 1); _env_long (depth 1); _env_option (depth 1); ENV_SPELLINGS (depth 1); ENV_GRAMMAR (depth 1); test_every_row_of_the_env_grammar_has_a_case (depth 1); test_a_cluster_behind_env_s_own_options_is_read (depth 1); test_the_split_string_after_the_options_is_read_past_a_redirection (depth 1); test_an_ambiguous_prefix_names_no_long_option (depth 1) |
| Needs a fix | yes — 🟡 8 (a redirection glued to the subcommand went from asked to silent in the guard), 🟡 9 (an abbreviated long option's value ends env's own options), 🟡 10 (a redirection among env's options ends them) |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is a verifying round. It targets `f1629706` over round 1's fix range `25e5b01a..2f4e9933`. It was asked:
- whether each of round 1's fixes holds;
- whether the units the fix pass created are correct: the `env` option walk (`_env_split_at`, `_env_takes_next`, `ENV_VALUED`, `ENV_VALUED_LONG`), the quoted re-join, `command_strings`' `env_words=False`, candidate C's per-view subtraction, and the `SystemExit` guard; · NAME NOT IN TREE
- whether 🟡 3's per-view version still fires on zero recorded pairs;
- whether any fix silenced a stopped shape or stopped a silent non-commit line;
- whether the ledger corrections and re-reads hold.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 8 | candidate C compares a cut or glued view with the frozen parser, which never reads such a view, so a redirection glued to the subcommand (`git switch>/dev/null x`) went from asked to silent | `hooks/worktree-guard.py:356` | **fixed** `07b67ac3` | fixed at 07b67ac3; executed: three glued shapes ask at round 1's target and are silent at `f1629706`, and bash runs each; the fix fires on 0 of 27,351 corpus pairs |
| 🟡 9 | an abbreviated long option that takes a value (`--un`, `--ch`, `--ar`) ends env's own options at its value, so `env --un FOO -iS 'git commit -m x'` is found by nothing | `hooks/cmdline.py:1768` | **fixed** `49f27f09` | fixed at 49f27f09 — `043f3153`; executed: four shapes found by nothing at `f1629706` and `233f0455`; read, not run on GNU env: getopt takes unambiguous prefixes, as `_env_split_at`'s docstring says | · NAME NOT IN TREE
| 🟡 10 | a redirection among env's options ends them, so `env 2>/dev/null -iS 'git commit -m x'` is found by nothing | `hooks/cmdline.py:1739` | **fixed** `49f27f09` | fixed at 49f27f09; executed: macOS `env` runs the string behind the redirection; five shapes found by nothing at `f1629706` and `233f0455` |
| ⬜ 11 | `--` does not end env's options, so `env -- -iS 'git commit -m y'` denies in a declared repository | `hooks/cmdline.py:1739` | **fixed** `49f27f09` | fixed at 49f27f09; executed: deny at `f1629706`, silent at `233f0455`; no real program is called `-iS` |
| ⬜ 12 | `overview.md`'s `quiet`'s-discards row describes the subtraction before the fix, and no row names the `env -S` class | `seal/specs/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd/overview.md:27` | answered | corrected at `aa3bbf21`; read; paperwork correction, outside `Needs a fix` |
| 🟢 | round 1's finding 1 is closed — env's own words are not asked the expansion question, and are quoted back into one word each | `hooks/cmdline.py:1950` | confirmed | executed: the six added no-commit controls are silent in a declared repository; `env -S '-i' "$CMD"` is silent at `f1629706` as at `233f0455` and as `env -i "$CMD"` |
| 🟢 | round 1's finding 2 is closed for the shapes it named — a cluster ending in `S` and a `--split-string` prefix are read among env's own options | `hooks/cmdline.py:1736` | confirmed | executed: the six added `HANDED` shapes are found; the class is not closed, which is this round's findings 9, 10 and 11 |
| 🟢 | round 1's finding 3 is closed — a restore before a hidden switch no longer silences the question | `hooks/worktree-guard.py:2260` | confirmed | executed: both restore cases ask, and both fail against round 1's target's guard; the built C fires on 0 of 27,351 pairs, re-counted; the comparison it introduced is this round's finding 8 |
| 🟢 | round 1's finding 4 stays deferred — the fix range does not touch the consent read | `hooks/worktree-guard.py:361` | deferred #734 | already deferred in round 1; read: `ask_what_only_the_wider_reading_finds` has no diff in `25e5b01a..2f4e9933` |
| 🟢 | round 1's finding 5 is closed — the guarded import catches a module body that exits | `hooks/worktree-guard.py:145` | confirmed | executed: the new case passes, and fails with `except Exception:` alone |
| 🟢 | round 1's finding 6 is closed — W10 names the third command that names no tree | `seal/releases/0.15.6.md` W10 | confirmed | read: round 1's fence verbatim; executed: evidence-check reports 0 drifted, 0 broken |
| 🟢 | round 1's finding 7 is closed — M1's correction is narrowed | `seal/releases/0.16.0.md` M1 | confirmed | read: round 1's fence verbatim; executed: survivor-check names M1's original claim alone, and the one `survivors.md` row excuses it |
| 🟢 | the re-reads of E14, E16, I5, I6, I12 and of the rows citing `main` hold against the fixes, and K3 and K5 describe `f1629706` | `seal/releases/0.16.0.md`, `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` | confirmed | read row by row; executed: evidence-check on the five ledger files, 0 drifted, 0 broken |

## Paste-ready fixes

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
```markdown
| `quiet`'s discards | Plan §*What phase 4 builds*, C step 1: "For each kind the frozen loop did NOT find". Code: `quiet` hands the kinds the loop judged to `wider_only_kinds`, which subtracts them, and a view counts as hidden only where the frozen parser reads its kind from none of the segments it was made from | the loop's verdicts | `classify` judges fewer kinds than `switch_kind` reads from the same words, so subtracting the words' kinds let a restore silence a hidden switch (round 1, yellow 3); comparing a cut view with the frozen parser silenced a glued subcommand (round 2, yellow 8) |
| `env -S`'s spellings | Spec §*Scope* 1: "every spelling of `env`'s split string". Code: `-S`, `-S<s>`, `--split-string[=<s>]` anywhere, and among env's own options a cluster ending in `S` and every prefix of `--split-string`; env's own options are read past a redirection and an abbreviated long option's value, and end at `--` | getopt's spellings | round 1, yellow 2, and round 2, yellows 9 and 10: macOS `env` runs `-iS` and a cluster behind a redirection; GNU's getopt takes unambiguous prefixes |
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/cmdline.py:1740` | round 1's 🟡 1 — fixed |
| round-1 | `hooks/cmdline.py:1726` | round 1's 🟡 2 — fixed |
| round-1 | `hooks/worktree-guard.py:336` | round 1's 🟡 3 — fixed |
| round-1 | `hooks/worktree-guard.py:359` | round 1's ⬜ 4 — deferred |
| round-1 | `hooks/worktree-guard.py:143` | round 1's ⬜ 5 — fixed |
| round-1 | `seal/releases/0.15.6.md:17` | round 1's ⬜ 6 — answered |
| round-1 | `seal/releases/0.16.0.md:247` | round 1's ⬜ 7 — answered |
| round-1 | `phases/phase-3.md` | round 1's 🟢 — confirmed |
| round-1 | `questions.md` D1 | round 1's 🟢 — confirmed |
| round-1 | `233f0455..07a3dc7f` | round 1's 🟢 — confirmed |
| round-1 | `docs/worktree-guard-spec.md` | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree-guard.py` main | round 1's 🟢 — confirmed |
| round-1 | `hooks/worktree-guard.py:141` | round 1's 🟢 — confirmed |
| round-1 | `hooks/cmdline.py` | round 1's 🟢 — confirmed |
| round-1 | `docs/commit-review-gate-spec.md` | round 1's 🟢 — confirmed |
| round-1 | `seal/releases/0.16.0.md` | round 1's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain
