# 1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd — review round 3

| Field | Value |
|---|---|
| Target SHA | a575739f01c20c1dcc03a6610471e7c5bce842b7 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 733 |
| Broad gate | 215c82b8 against 233f0455 |
| Fixes checked by | no fixes to check |
| Fix range | `97f6cee08c1234591d754f7cd23b3cf5ff3754bf..97f6cee08c1234591d754f7cd23b3cf5ff3754bf`, 0 commits |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 13 (a redirection word read as a branch name makes `git checkout . &>/dev/null` ask "switches a branch", silent at the base and at `f1629706`) and 🟡 14 (`ENV_OPTIONS` misses BSD's `-` and GNU 9.12's `--env0-from`, so a commit behind `env -i-S` or `env --S` is found by nothing); 🟡 15 is a silence the base shipped too, which I judge answerable with grounds and deferrable |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 is a verifying round and the run's last, since round 2 closed on fixes and spent the one reopening. It targets `a575739f` over round 2's fix range `e74efba8..40214e98`. It was asked:
- whether round 2's fixes hold;
- whether the units that pass created are correct: `ENV_OPTIONS` against both synopses, candidate C's comparison against each view's source segments, and the claimed equivalent mutant;
- whether any non-commit `env` line silent at base now stops, or a stopped shape goes silent;
- whether the ledger corrections hold.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 13 | 🟡 8's fix compares a cut or merged view with segments that lack its redirection word, which `switch_kind` reads as a branch name, so `git checkout . &>/dev/null` and other non-switch shapes ask "switches a branch" | `hooks/worktree-guard.py:364` | deferred #737 | #737 — The run is capped at the reopening bound, which commissions nothing. #737 is in this release's milestone, because the base never asked this question and 0.18.0 should not ship it; it carries the report's fence; executed: six shapes silent at `233f0455` and `f1629706`, ask at `a575739f`; bash runs each without switching; the fence passes the two modules and fires on 0 of 27,351 pairs |
| 🟡 14 | `ENV_OPTIONS` misses BSD's `-` letter and GNU 9.12's `--env0-from`, so `env -i-S`, `env --S` and `env --env0-from f -iS` hide a commit from every reading | `hooks/cmdline.py:1783` | deferred #737 | #737 — The same reason and the same issue; both fences touch the guard's and the reader's code together; executed: macOS `env -i-S`, `-v-S` and `--S` run the string, and five shapes are found by nothing at three commits; read: GNU's and FreeBSD's sources |
| 🟡 15 | a checkout whose name carries a redirection (`git checkout feature/x>/dev/null`, `git checkout 2>/dev/null feature/x`) switches unasked, because `classify` looks the redirection up as part of the name and C reads the name tree-blind | `hooks/worktree-guard.py:364` | deferred #738 | #738 — A silence the base shipped (233f0455 through a575739f); the backlog issue carries the fence and its cost; executed: bash switches; silent through `main()` at `233f0455`, `07a3dc7f`, `f1629706` and `a575739f`; not a regression; a tree-blind fence asks on a glued restore too |
| ⬜ 16 | the merged-group mutant the build calls equivalent is not: it silences `git switch &>/dev/null feature/x`, and no case pins an `&>` before the name | `hooks/worktree-guard.py:361` | deferred #737 | #737 — The two cases that pin the merged-group comparison ride with 🟡 13's fence; executed at function level: 32 of 854 shapes differ, the mutant silent on each; the code is right |
| ⬜ 17 | K3's corrected clause and E14's round 2 note say the table holds every option of both synopses | `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` K3 | answered | corrected at `97f6cee0`; read; paperwork correction, outside `Needs a fix`; drifts with 🟡 14's fix |
| 🟢 | round 2's finding 8 is closed for the shapes it named — a redirection glued to the subcommand is asked again | `hooks/worktree-guard.py:364` | confirmed | executed: the three glued shapes ask at `a575739f` and are silent at `f1629706`; the comparison it introduced is this round's finding 13 |
| 🟢 | round 2's finding 9 is closed — an abbreviated long option's value no longer ends env's own options | `hooks/cmdline.py:1813` | confirmed | executed: `env --un FOO -iS` is found at `a575739f`, by nothing at `f1629706`; the abbreviation cases pass; GNU env read, not run |
| 🟢 | round 2's finding 10 is closed — a redirection among env's options is read past | `hooks/cmdline.py:1742` | confirmed | executed: `env -u FOO 2>/dev/null -iS 'git commit -m x'` is found and denied at `a575739f`, found by nothing at `f1629706` |
| 🟢 | round 2's finding 11 is closed — `--` ends env's options | `hooks/cmdline.py:1749` | confirmed | executed: `env -- -iS 'git commit -m y'` is silent in a declared repository at `a575739f` and `233f0455`, a deny at `f1629706` |
| 🟢 | round 2's finding 12 is closed — `overview.md`'s two rows describe the code | `seal/specs/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd/overview.md` | answered | read: round 2's fence in substance; the env row's "one table" claim drifts with finding 14 |
| 🟢 | round 1's finding 4 stays deferred — the fix range does not touch the consent read | `hooks/worktree-guard.py:373` | deferred #734 | already deferred in round 1; read: no diff to `ask_what_only_the_wider_reading_finds` in `e74efba8..a575739f` |
| 🟢 | the ledger rows round 2's fixes drifted hold — K3 and K5 corrected, E14, I6, E16 and I5 re-read, two `survivors.md` rows | `seal/releases/0.16.0.md`, `seal/specs/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd/survivors.md` | confirmed | executed: evidence-check 0 drifted, 0 broken on five ledger files; survivor-check names two places and passes with the exemption; read: each row against the diff, apart from finding 17 |

## Paste-ready fixes

```python
# hooks/worktree-guard.py, wider_only_kinds: the loop over `sourced`
    wider = set()
    for view, sources in sourced:
        frozen = {switch_kind(parse_git(tokens)) for tokens in sources}
        # The view as the program reads it: a cut or merged view carries a
        # redirection word its segments do not, and `switch_kind` reads any
        # word as a name, so `git checkout . &>/dev/null` read as a switch
        # (round 3 of 1790993140).
        kind = switch_kind(wide.parse_git(_bare_words(view)))
        if kind and kind not in frozen:
            wider.add(kind)
    return wider - set(judged)


def _bare_words(tokens):
    """TOKENS with a redirection glued to a word's end cut off, and every
    redirection taken out: the words the program is handed."""
    cut = wide.unglued(tokens) or list(tokens)
    # `unglued` cuts `.&>f` at `>`, and bash ends the word at `&>`.
    cut = [
        t[:-1]
        if t.endswith("&") and i + 1 < len(cut) and cut[i + 1].startswith(">")
        else t
        for i, t in enumerate(cut)
    ]
    return wide._without_redirections([t for t in cut if t])
```
```python
# hooks/worktree-guard.py, wider_only_kinds' docstring: replace "The wider
# reading is its splitter's segments, `merged_view`'s groups and the words a
# redirection glued to a word's end, each read by its `parse_git`" with:
    The wider reading is its splitter's segments and `merged_view`'s groups,
    each read by its `parse_git` with every redirection taken off, a glued
    one cut first, so a redirection word is never read as a branch name
```
```python
# tests/test_guard_resolves_the_tree_it_judges.py, WIDER_ONLY, after
# "a redirection glued to add"
    # Round 3 of 1790993140: bash runs each; the splitter cuts `&>` at `&`,
    # and only the merged view holds the switch. The mutant comparing the
    # merged view with itself is silent on both.
    "&> between switch and its name": (
        "cd w && git switch &>/dev/null feature/x",
        "switch",
    ),
    "&> between checkout and its name": (
        "cd w && git checkout &>/dev/null feature/x",
        "switch",
    ),
    # A redirection between `worktree` and `add`: silent at `a575739f`.
    "a redirection between worktree and add": (
        "cd w && git worktree 2>/dev/null add ../wt b",
        "creation",
    ),
```
```python
# tests/test_guard_resolves_the_tree_it_judges.py, before
# test_a_restore_the_frozen_parser_reads_is_not_hidden_from_it
@pytest.mark.parametrize(
    "command",
    [
        "cd w && git checkout . &>/dev/null",
        "cd w && git checkout .&>/dev/null",
        "cd w && git checkout -q &>/dev/null",
        "cd w && git switch --detach &>/dev/null",
        "cd w && git switch --detach>/dev/null",
        "cd w && git checkout>/dev/null .",
    ],
)
def test_a_redirection_word_is_not_read_as_a_branch_name(
    monkeypatch, capsys, repo, tmp_path, command
):
    """Round 3 of 1790993140. A cut or merged view carries the redirection
    word its segment does not, and `switch_kind` reads any word as a name.
    Each asked at `a575739f`, and was silent at `f1629706`."""
    session, _other = _a_dirty_w_under_a_clean_session(repo, tmp_path)
    decision, reason, _ = run(monkeypatch, capsys, command, session)
    assert decision == "silent", (command, decision, reason)
```
```python
# hooks/cmdline.py, ENV_OPTIONS: after the --list-signal-handling row
    (None, "--env0-from", "required"),
```
```python
# hooks/cmdline.py, after ENV_OPTIONS: replace the _ENV_SHORT line
_ENV_SHORT = {short: value for short, _long, value in ENV_OPTIONS if short}
# BSD's getopt has `-` among its letters, as `-i`: `env -i-S '…'` and `env
# --S '…'` run the string on macOS (executed, round 3 of 1790993140).
_ENV_SHORT["-"] = None
```
```python
# hooks/cmdline.py, the comment above ENV_OPTIONS: replace the sentence on a
# lone `-` with
# What the table does not need a row for: a lone `-`, which GNU takes as `-i`
# and the end of the options, and BSD as `-i` among them; the walk reads it as
# one of env's own options, which costs a stop only where GNU's program is
# named like an option. And `--`, which ends them. BSD's `-` inside a word is
# `_ENV_SHORT`'s, below the table.
```
```python
# hooks/cmdline.py, _env_option: replace the long-name arm
    if t.startswith("--"):
        name, eq, attached = t.partition("=")
        long = _env_long(name, own)
        if long is not None or not own or t == "--":
            value = _ENV_LONG.get(long)
            if value == ENV_STRING:
                return (("here", attached) if eq else ("next", None)), False
            return None, own and value == "required" and not eq
        # No GNU long name: BSD's getopt reads the word as a cluster whose
        # first letter is `-`, so `--S` is `-i -S` there.
```
```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py,
# HANDED, after "env -vS behind a cut redirection"
    # Round 3 of 1790993140: BSD's getopt reads `-` as `-i`, inside a cluster
    # and as the first letter of a word no GNU long name matches; macOS `env`
    # runs each string (executed). Each found nothing at `a575739f`.
    "env -i-S": f"env -i-S '{C}'",
    "env --S": f"env --S '{C}'",
    "env --S behind an option's value": f"env -u FOO --S '{C}'",
    # GNU coreutils 9.12's `--env0-from` takes a value (read, not run).
    "env -iS behind --env0-from's value": f"env --env0-from f -iS '{C}'",
```
```python
# tests/test_a_commit_behind_a_wrapper_or_in_a_substitution_is_judged.py,
# ENV_SPELLINGS, after "--argv0"
    "--env0-from": "--env0-from f",
```
```python
# hooks/worktree-guard.py, wider_only_kinds: replace 🟡 13's three lines
# from `kind = …` with
        parsed = wide.parse_git(_bare_words(view))
        kind = switch_kind(parsed)
        if kind and (kind not in frozen or _names_anew(parsed, sources)):
            wider.add(kind)


def _names_anew(parsed, sources):
    """True where a checkout's name, its redirection taken off, is a word no
    source segment's checkout names: `classify` looked `feature>/dev/null`
    up as a ref, and only the bare `feature` is one. Tree-blind, so a glued
    restore (`git checkout README.md>/dev/null`) is asked too."""
    if not parsed or parsed[0] != "checkout":
        return False
    names = [a for a in parsed[1] if not a.startswith("-")]
    if not names or names[0] == ".":
        return False
    for tokens in sources:
        theirs = parse_git(tokens)
        if theirs and theirs[0] == "checkout":
            words = [a for a in theirs[1] if not a.startswith("-")]
            if words[:1] == names[:1]:
                return False
    return True
```
```python
# tests/test_guard_resolves_the_tree_it_judges.py, WIDER_ONLY
    # Round 3 of 1790993140, yellow 15: `classify` looks the redirection up
    # as part of the name. bash switches each (executed); silent at every
    # commit from `233f0455` to `a575739f`.
    "a redirection glued to checkout's name": (
        "cd w && git checkout feature/x>/dev/null",
        "switch",
    ),
    "a redirection before checkout's name": (
        "cd w && git checkout 2>/dev/null feature/x",
        "switch",
    ),
```

## Executed probes

| What was run | Result |
|---|---|
| Narrow run at `a575739f`: the guard and wrapper modules | 768 passed |
| `main()` over three sets of guard shapes at `233f0455`, `07a3dc7f`, `f1629706` and `a575739f`, dirty `w` under a clean session | 🟡 13: six shapes silent, ask, silent, ask; 🟡 15: four shapes silent at all four; round 2's glued shapes ask at `a575739f` only |
| Candidate C as built, the merged-self mutant and `f1629706`'s rule, at function level, over 854 generated shapes | built and mutant differ on 32, the mutant silent on each; built asks where `f1629706` did not on 82 |
| Bash in a scratch repository: the checkout shapes of 🟡 13, 🟡 15 and ⬜ 16 | glued and spaced-before names switch; `checkout . &>/dev/null` restores and stays on `main` |
| macOS `env -i-S`, `env -v-S`, `env --S`, `env - -S`, `env -- -S`, `env -x` | the first four run the string; `--` makes `-S` the program (exit 127); `-x` is refused |
| 20 `env` shapes through `commit_invocations` and `main()` in a declared repository, at `233f0455`, `f1629706` and `a575739f` | five commit shapes found by nothing at all three (🟡 14); four `"$CMD"` shapes newly denied, as `env -S "$CMD"` was at the base; no stopped shape went silent |
| Corpus count over D1's cut: built C, 🟡 13's fence, 🟡 15's fence | 27,351 pairs, none raised; 0, 0 and 0 |
| 🟡 13's and 🟡 14's fences applied in the round's clone, then the two modules | 793 passed; `ruff check` clean; `ruff format` reflows two lines, already reflowed in the fences |
| The new cases against `a575739f`'s hooks | 18 failed, 775 passed |
| 🟡 15's fence on top, then the guard module | 124 passed, 1 failed: the glued restore, the trade named under 🟡 15 |
| `bin/evidence-check --ledger` on the fragment and four release files | 0 drifted, 0 broken in each |
| `bin/survivor-check --range e74efba8..a575739f`, with and without `survivors.md` | passes with it; without, two places, both round 1 yellow 3 citations |
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
| round-2 | `hooks/worktree-guard.py:356` | round 2's 🟡 8 — fixed |
| round-2 | `hooks/cmdline.py:1768` | round 2's 🟡 9 — fixed |
| round-2 | `hooks/cmdline.py:1739` | round 2's 🟡 10 — fixed |
| round-2 | `seal/specs/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd/overview.md:27` | round 2's ⬜ 12 — answered |
| round-2 | `hooks/cmdline.py:1950` | round 2's 🟢 — confirmed |
| round-2 | `hooks/cmdline.py:1736` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:2260` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py:361` | round 2's 🟢 — deferred |
| round-2 | `hooks/worktree-guard.py:145` | round 2's 🟢 — confirmed |
| round-2 | `seal/releases/0.15.6.md` W10 | round 2's 🟢 — confirmed |
| round-2 | `seal/releases/0.16.0.md` M1 | round 2's 🟢 — confirmed |
| round-2 | `seal/releases/0.16.0.md`, `seal/ledger/1790993140-the-gates-read-config-env-env-s-and-an-unresolved-cd.md` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 15, a checkout whose name carries a redirection switches unasked; a tree-aware C needs each segment's directory | proposed: a new issue beside #686 and #734, if the orchestrator does not take the fence | the orchestrator, then the owner, who decided D3's tree-blind count |
