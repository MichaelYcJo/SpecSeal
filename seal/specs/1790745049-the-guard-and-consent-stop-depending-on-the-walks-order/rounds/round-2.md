# 1790745049-the-guard-and-consent-stop-depending-on-the-walks-order — review round 2

| Field | Value |
|---|---|
| Target SHA | 6a2a87d738fb5469e7f69254bc460a94e7cb365f |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 691 |
| Broad gate | not yet |
| Fixes checked by | round-3 |
| Fix range | `00ed11bede7e416b5dee56de688831bfecf948b2..9f5261c53cf866ac056289d9b184e23db229d02f`, 3 commits |
| Contract changes | test_a_broken_shared_module_names_every_gate_that_imports_it → round-2-report.md, round-2.md |
| New units | none |
| Needs a fix | yes — 🔴 1, `docs/worktree-guard-spec.md:585` names `0.17.0` and the release-hygiene case fails |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 2 is verifying. It targets `6a2a87d7` over round 1's fix range `d1e2b9d3..052c6fe8`, which replaced `base_directories` with plan alternative B: the worktree guard and the consent writer read a frozen, byte-identical copy of `86256492:hooks/cmdline.py` (`hooks/cmdline_base.py`), and the gate files stay byte-identical to `542f920b`. The round was asked seven things:
1. Whether the copy is byte-identical below its rider.
2. Whether every symbol both consumers use comes from it, including through `dispatch.py`'s loading.
3. Whether the two consumers equal `86256492` at the decision level.
4. Whether the gate is unchanged.
5. Whether round 1's five verdicts are closed, records included.
6. Whether the changed failing-gate cases still prove what they proved.
7. What loading two readers costs.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The policy names `0.17.0`, so the loaded-file version case fails and the suite is red | `docs/worktree-guard-spec.md:585` | **fixed** `53d30647` | fixed at 53d30647; Executed: 1 failed, 406 passed in the hygiene module; written at `c5bb0222` in round 1's fix range |
| ⬜ 2 | The cost paragraph cites §A for the command-word groups, which are in §Creation consent | `docs/worktree-guard-spec.md:582` | answered | corrected at 53d30647; Read |
| ⬜ 3 | `foreach` is part of the guard's cost and no list names it | `docs/worktree-guard-spec.md:581` | answered | corrected at 53d30647; Executed: `deny` at `542f920b`, `silent` at `86256492` and here |
| ⬜ 4 | The shared-module case breaks both readers at once, so the per-module "no gate that does not import it" is no longer pinned, and its first sentence is false | `tests/test_a_gate_that_fails_says_so.py:302` | **fixed** `53d30647` | fixed at 53d30647; Executed: each reader broken alone names exactly its two importers |
| ⬜ 5 | Three test modules and one docstring still say the guard imports `cmdline` | `tests/test_what_the_reader_understands.py:791` | answered | corrected at 53d30647; Read; no assertion depends on it |
| 🟢 | round 1's blocking finding is closed — a segment only #674 reads as git no longer takes the first slot | `hooks/worktree-guard.py#walk_command` | confirmed | Executed: 0 differences against `86256492` over 10,598 commands, `WIDER_FIRST` and its consent twin included |
| 🟢 | round 1's 🟡 2 is closed — zsh-prefixed segments get the base's answer | `hooks/cmdline_base.py#walk_directories` | confirmed | Executed: the same corpus, all four prefixes as heads and tails |
| 🟢 | round 1's ⬜ 3 is closed — the policy says the whole command is read the base's way, which the import makes true | `docs/worktree-guard-spec.md:560` | confirmed | Read, and the differential |
| 🟢 | round 1's ⬜ 4 is closed — the changelog opens the cost as a cost | `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/changelog.md:20` | confirmed | Read |
| 🟢 | round 1's ⬜ 5 is closed — M3 is withdrawn with a dated correction | `seal/ledger/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order.md` | confirmed | Read |
| 🟢 | The frozen copy equals `86256492:hooks/cmdline.py` below its rider | `hooks/cmdline_base.py` | confirmed | Executed, byte comparison |
| 🟢 | Both readers load in one process without cross-talk | `hooks/dispatch.py#run_gate` | confirmed | Executed: module identities and 10,361 guard answers in one process |
| 🟢 | The commit gate is unchanged against `542f920b` | `hooks/commit-review-gate.py` | confirmed | Executed: empty diff, 0 of 10,361 gate outputs differ |
| 🟢 | The records name the frozen reader: M1–M4, S3/S5–S7, both policies, I's and E's corrections | `seal/ledger/` | confirmed | Read; `evidence-check` 0 drifted, 0 broken, 0 refused |
| 🟢 | Two readers cost under 2 ms per hook call | `hooks/worktree-guard.py` | confirmed | Executed, interleaved medians |
| ❓ | The guard's Windows backslash doubling on a Windows machine | `hooks/worktree-guard.py#_tokenize_with_separators` | ❓ out of verified scope | Carried from round 1. On macOS the `windows=True` walk equals `86256492`'s for every command, but `ntpath` and a real Windows shell were not run; the repository owner answers it on a Windows machine |

## Paste-ready fixes

```text
redirection or behind zsh's `noglob`, `nocorrect`, `repeat N`, `for i (…)` or
`foreach i (…)` is not git to this guard, so it says nothing there
(§*Creation consent*'s command-word groups). Round 2 of work item 1790660768
made the guard read the first and #674 the second, and #689 took both back as
the accepted cost. The commit gate still reads both. #692, the redesign of how
the gates learn where a command acts, decides the guard's reading again, and
deletes the frozen copy.
```
```text
zsh's `noglob`, `nocorrect`, `repeat N`, `for i (…)` or `foreach i (…)`
```
```python
@pytest.mark.parametrize(
    "broken, named",
    [
        ({"cmdline.py": BROKEN}, ["commit-review-gate.py", "implementer-notice.py"]),
        ({"cmdline_base.py": BROKEN}, ["worktree-guard.py", "worktree_consent.py"]),
        (
            {"cmdline.py": BROKEN, "cmdline_base.py": BROKEN},
            [
                "commit-review-gate.py",
                "worktree-guard.py",
                "implementer-notice.py",
                "worktree_consent.py",
            ],
        ),
    ],
    ids=["cmdline", "cmdline_base", "both"],
)
def test_a_broken_shared_module_names_every_gate_that_imports_it(
    repo, tmp_path, broken, named
):
    """S6. A broken shared reader names every gate that imports it, once, and
    no gate that does not. `cmdline.py` is imported by the commit gate and
    `implementer-notice.py`; since #689 `cmdline_base.py`, the reader frozen at
    `86256492`, is imported by the worktree guard and `worktree_consent.py`. The
    commit gate's own import of `worktree_consent` is guarded, so a broken
    `cmdline_base.py` does not name it. The `post-bash` call is not a commit: a
    copy of `hooks/` has no `skills/` beside it, so `evidence-advisor.py` would
    fail at run on a commit for want of its checker, which is the fixture and
    not the reader."""
    opted_in(repo)
    hooks = hooks_copy(tmp_path, broken)
    dispatch(hooks, "pre-bash", bash(repo, "s-x"))
    dispatch(
        hooks,
        "post-bash",
        bash(repo, "s-x", command="ls", hook_event_name="PostToolUse"),
    )
    for path in (repo / ".git" / RECORDS / "s-x").iterdir():
        os.utime(path, ns=(10**18, 10**18))
    lines = said(stop(hooks, repo, "s-x"))
    assert lines[0] == f"SpecSeal: {len(named)} gates failed and were skipped", lines
    assert gates_said(lines) == named, lines
    assert lines[-1] == CLOSING
```
```python
import cmdline  # noqa: E402  -- the plain name the commit gate imports
```
```text
    `wg.cmdline` rather than the `reader` above: the guard reaches its reader
    with a plain `import cmdline_base as cmdline`, which goes through
    `sys.modules`, while
```

## Executed probes

| What was run | Result |
|---|---|
| The frozen copy against `git show 86256492:hooks/cmdline.py`, as bytes | Equal below the 18 rider lines |
| `git diff 542f920b..6a2a87d7 -- hooks/cmdline.py hooks/commit-review-gate.py` | Empty |
| Differential over 10,361 generated commands, each hook set in its own process on a fresh copy of one fixture, the guard's `main()` with `sessions_in_tree` reporting a session active in `w` alone, a new session id per command | Target against `86256492`: 0 differences in decision, reason, judged tree, walk, Windows-mode walk, kinds and consent directory; no exceptions on either side |
| The same commands with the commit gate loaded first in the guard's process, as `dispatch.py` does | Guard answers equal the guard alone; module identities as in item 2; gate output equal to `542f920b`'s for all 10,361 (579 denied) |
| A second corpus of 237 header, subshell, string and runner shapes at `86256492`, `542f920b` and the target | Target against `86256492`: 0 differences. Against `542f920b`: 30 decision or tree differences, all of them redirection, zsh prefix or `foreach` |
| A deleted probe breaking `cmdline.py`, `cmdline_base.py` and both, through `dispatch.py` and the stop report | Commit gate and `implementer-notice.py`; guard and `worktree_consent.py`; all four |
| `bin/test` on the guard-tree, failing-gate, reader-understands, rider, no-real-identifiers and no-shape modules | 305 passed, exit 0 |
| `bin/test` on the eleven other modules that load the guard or the consent writer, `tests/test_dispatch.py` included | 1107 passed, 1 skipped, exit 0 |
| `bin/test` on eight tree-scanning modules the new file and text joined (hygiene, interpreter, release watch, old roots, survivors, one word, rule owners, merge corrections) | 1 failed, 406 passed, exit 1: 🔴 1 |
| `bin/evidence-check`; `bin/correction-check --range 542f920b...HEAD` | 0 drifted, 0 broken, 0 refused, exit 0; no merge commit in the range, exit 0 |
| Hook time, interleaved, twelve runs each after one warm-up, three hook sets | Differences of 0.1 to 1.7 ms; see item 7 |
| Broad gate: full suite, repository-wide lint and typecheck | not yet — nothing has run it on this branch; it comes due with the sealer's spawn once 🔴 1 is fixed and a round passes |

```text
session/        git init, no commits (clean)
session/w/      copy of a one-commit repository with branch feature/x; f.txt modified; seal/ present
session/clean/  the same copy, unmodified
O/              the same copy, outside the session
nosuch          never created
```

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/worktree-guard.py:2086`, `hooks/worktree_consent.py:437` | round 1's 🔴 1 — fixed |
| round-1 | `hooks/cmdline.py:2617` | round 1's 🟡 2 — fixed |
| round-1 | `docs/worktree-guard-spec.md:559` | round 1's ⬜ 3 — fixed |
| round-1 | `seal/specs/1790745049-the-guard-and-consent-stop-depending-on-the-walks-order/changelog.md:20` | round 1's ⬜ 4 — answered |
| round-1 | `hooks/cmdline.py#walk_directories` | round 1's 🟢 — confirmed |
| round-1 | `hooks/` | round 1's 🟢 — confirmed |
| round-1 | `tests/test_guard_resolves_the_tree_it_judges.py` | round 1's 🟢 — confirmed |
| round-1 | `hooks/cmdline.py#base_directories` | round 1's 🟢 — confirmed · NAME NOT IN TREE |
| round-1 | `hooks/worktree-guard.py#_tokenize_with_separators` | round 1's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether the guard should read zsh-prefixed and redirected segments rather than leave them to the user's settings | already deferred in round 1 to #692, the owner's redesign of how the gates learn where a command acts | the repository owner |
