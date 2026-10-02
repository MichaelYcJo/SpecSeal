# 1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text — review round 3

| Field | Value |
|---|---|
| Target SHA | 4fe82d29439ef0eb53b572f7014795359352a194 |
| Written late | no |
| Ran by | specseal:warden on claude-opus-5-5 |
| PR | 705 |
| Broad gate | not yet |
| Fixes checked by | round-4 |
| Fix range | `b34b5401225b3196c9ab4e7dca5bcb848c0acc6b..a4692a0b9e086248c0054b2b661edd840ad0ef5a`, 6 commits |
| Contract changes | none |
| New units | PLAIN_PROGRAMS (depth 1); PLAIN_GIT (depth 1); PLAIN_CONFIG (depth 1); is_plain (depth 1); test_concluding_a_conflicted_merge_is_judged (depth 1); STILL_PLAIN (depth 1); NO_LONGER_PLAIN (depth 1); test_each_other_condition_of_the_rule_makes_a_command_not_plain (depth 1); test_a_negative_that_is_plain_stays_plain (depth 1); test_a_negative_outside_the_allowlist_is_not_plain (depth 1); PLAIN_AND_NOT (depth 1); test_a_plain_agent_commit_stands_aside_and_one_word_more_is_judged (depth 1) |
| Needs a fix | yes — 🟡 1 (the words inside a string a shell parses again) and 🟡 2 (an emptied environment behind another `env` option, and `exec -c`). |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3 is a verifying round at `4fe82d29`. Its diff is round 2's fix range `b6d5bdb2..75577dc0`, plus the release merge `8b4c6545`, which no round had read. It was asked, for each of round 2's five `fixed` verdicts, whether the finding and its class are closed, re-running probes n01–n08. It was asked to probe both directions of the exact-name comparison: each new spelling denied, and an ordinary command that only mentions a name left silent. It was also asked to look for further spellings of the same class.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A session name, a config key, `HOME` or a `GIT_CONFIG*` assignment inside a string a shell parses again (`sh -c`, `bash -c`, `eval`, a quoted `$( … )`, `env -S`) is one word to the reader, and the commit lands unjudged; 0.16.0 stopped each | `hooks/tokens.py#steps_around_hooks` | **fixed** `7e8269c4` | fixed at 7e8269c4 — owner-directed change of mechanism (questions.md P7, 2026-10-02): the reading stands aside only for a positively defined plain command; executed x10, x11, x15, x17, y01, y02, y03, y08, y10: landed, target silent, 0.16.0 deny; patched, all nine deny; class of round 2's 🟡 1 and 🟡 2 |
| 🟡 2 | `env -v -i`, `env -u FOO -i`, `env -vuNAME` and `exec -c` empty the environment past a reader that looks only at the word after `env`; 0.16.0 stopped each | `hooks/tokens.py#_empties_the_environment` | **fixed** `7e8269c4` | fixed at 7e8269c4 — the same rule as 🟡 1 (P7); executed x08, x09, x12, x16, y07, z08: landed, target silent, 0.16.0 deny; patched, all six deny; class of round 1's 🟡 8 |
| ⬜ 3 | `git --config-env core.hooksPath=VAR commit` with a space, and `env -S '-i git commit'`, are commits neither reading places | `hooks/cmdline.py#_git_options` | deferred #716 | #716 — Predates the branch: 0.16.0's reading misses both spellings too (y05, y09); executed y05, y09: landed, both readings silent; 0.16.0's gap as much as the target's; a new issue is the candidate home, and the owner answers it |
| ⬜ 4 | The conflicted-merge sentence round 2's ⬜ 5 added has no case among the paragraph's `Enforced by:` line | `docs/commit-review-gate-spec.md` §*A commit git makes for its own rebase, cherry-pick or revert* | **fixed** `7e8269c4` | fixed at 7e8269c4; read: the six named cases conclude no merge; executed n07 refused, so the sentence is true |
| 🟢 | round 2's finding 1 is closed for its instances — `NAME=`, `env -u`, `env -uNAME`, `unset`, and `export -n`, `declare +x`, `typeset +x` through the bare name | `hooks/tokens.py#steps_around_hooks` | confirmed | executed n01–n03, x01–x03, z01: landed with git alone, target deny; the class is this round's 🟡 1 and 🟡 2 |
| 🟢 | round 2's finding 2 is closed for its instances — `include.path`, `includeIf` with a dotted condition, `HOME=`, `XDG_CONFIG_HOME=`; the `chmod -x` limit is written and true | `hooks/tokens.py#steps_around_hooks`, `docs/commit-review-gate-spec.md` | confirmed | executed n04, n05, x04, x05, x07, x07d, x18, x20, y04 deny; n06 landed with the target silent, as written; the class is this round's 🟡 1 |
| 🟢 | round 2's finding 3 is closed — the old spelling's limit states the match as `hooks/answers.py#given` makes it | `docs/commit-review-gate-spec.md`, `hooks/answers.py#_squash` | confirmed | read: escapes and every non-alphanumeric dropped, then a substring of the ancestors' argv |
| 🟢 | round 2's finding 4 is closed — both latency sentences count the `post-commit` interpreter | `docs/commit-review-gate-spec.md`, `hooks/githooks.py#_NARROW` | confirmed | read: the `post-commit` entry is empty |
| 🟢 | round 2's finding 5 is closed — the policy says a conflicted merge's conclusion is judged and a clean merge is not | `docs/commit-review-gate-spec.md` | confirmed | executed n07, n08 refused; n09 landed unjudged; the pin is this round's ⬜ 4 |
| 🟢 | the words a command only mentions stay silent | `hooks/tokens.py#steps_around_hooks` | confirmed | executed m01–m06: `steps_around_hooks` false, target silent, the stub refused each; m07 `-m CLAUDECODE` is read, and costs a judgment the stub made the same way |
| 🟢 | the release merge `8b4c6545` changed nothing this branch's hooks do or say | `skills/verify/` | confirmed | executed: no file under `hooks/`, `docs/`, `agents/` or the agent contract in its delta; read: no hook imports `skills/verify/scripts/` |
| 🟢 | the ledger holds unscoped at the target | `seal/` | confirmed | executed: `bin/evidence-check .` exit 0; 3,492 ok, 0 drifted, 0 broken |
| 🟢 | the module the fixes touched passes at the target | `tests/test_the_commit_gate_decides_at_the_commit.py` | confirmed | executed: 216 passed, 62 skipped, exit 0 |
| ❓ | Whether a `systemMessage` from the installer reaches the model or only the person | `hooks/hook-install.py#main` | ❓ out of verified scope | carried from rounds 1 and 2; nothing here ran the harness's renderer; the orchestrator answers it |
| ❓ | Whether a command the person types with `!` is "a person's own commit" under P2 — it carries `CLAUDECODE` and is judged | `hooks/githooks.py#_P2` | ❓ out of verified scope | carried from rounds 1 and 2; the owner answers it |
| ❓ | M4's version floor and M5 | `overview.md` §*Not verified* | ❓ out of verified scope | carried; this round ran real shells under a real `claude` ancestor, not the harness's own Bash calls; the orchestrator answers it |

## Paste-ready fixes

```python
# hooks/tokens.py: replaces _empties_the_environment, and adds the helper below it
def _empties_the_environment(split, i):
    """`env` given `-i`, `-` or `--ignore-environment` anywhere among its
    options, or `exec -c` (bash and zsh), each of which runs the command with
    an empty environment (round 1 of #692, 🟡 8; round 3, an option before
    the `-i`, and `exec -c`)."""
    base = split[i].strip("(").rsplit("/", 1)[-1]
    rest = split[i + 1 :]
    if base == "exec":
        return any(
            w.startswith("-") and not w.startswith("--") and "c" in w for w in rest[:3]
        )
    if base != "env":
        return False
    j = 0
    while j < len(rest):
        w, value = rest[j], None
        j += 1
        if w in ("-", "--ignore-environment"):
            return True
        if w == "--" or not w.startswith("-"):
            return False
        if w.startswith("--"):
            name, eq, value = w.partition("=")
            if not eq and name in ("--unset", "--chdir", "--split-string"):
                value, j = (rest[j] if j < len(rest) else ""), j + 1
            if name == "--split-string" and _empties_the_environment(
                ("env", *words(value)), 0
            ):
                return True
            continue
        flags = w[1:]
        for k, f in enumerate(flags):
            if f == "i":
                return True
            if f in "uPSC":
                # A valued flag takes the rest of its word, or the next word.
                value = flags[k + 1 :]
                if not value:
                    value, j = (rest[j] if j < len(rest) else ""), j + 1
                # `-S` splits its value into more of env's own arguments.
                if f == "S" and _empties_the_environment(("env", *words(value)), 0):
                    return True
                break
    return False


def _strings_a_shell_runs(command, split):
    """The strings inside `command` a shell parses again: what `sh -c` and the
    other hosts `cmdline.reparsed_texts` names are handed, `eval`'s
    arguments, and every `$( … )` body (round 3 of #692)."""
    from cmdline import reparsed_texts, substitution_bodies

    bare = [w.strip("()") for w in split]
    texts = list(reparsed_texts(bare))
    texts += [" ".join(bare[k + 1 :]) for k, w in enumerate(bare) if w == "eval"]
    texts += substitution_bodies(command)
    return [t for t in texts if t.strip() and t != command]
```
```python
# hooks/tokens.py, steps_around_hooks: the head of the loop, replaced
    split = words(command)
    if not split:
        return bool((command or "").strip())
    # A string a shell parses again is a command of its own, and every word
    # below is read there too (round 3 of #692, executed).
    if any(steps_around_hooks(t) for t in _strings_a_shell_runs(command, split)):
        return True
    for i, word in enumerate(split):
        if "hookspath" in word.lower():
            return True
        if word.lstrip("(").startswith("GIT_CONFIG") and "=" in word:
            return True
        if _empties_the_environment(split, i):
            return True
```
```python
# hooks/tokens.py, steps_around_hooks: the -u arm, replaced
        elif name.startswith("-") and not name.startswith("--") and "u" in name:
            # `-uNAME`, and `-vuNAME` with a flag before it (round 3).
            session = name[name.index("u") + 1 :]
```
```python
# tests/test_the_commit_gate_decides_at_the_commit.py, STEPS_AROUND: add
    # Round 3's 🟡 1: a string a shell parses again is read word by word too.
    "sh -c unsetting a session variable": "sh -c 'unset CLAUDECODE; git commit -m x'",
    "include.path behind cd in bash -c": (
        "bash -c 'cd . && git -c include.path=/x/cfg commit -m x'"
    ),
    "GIT_CONFIG behind cd in sh -c": (
        "sh -c 'cd . && GIT_CONFIG_GLOBAL=/x/g git commit -m x'"
    ),
    "HOME in a quoted substitution": 'echo "$(cd . && HOME=/x/h git commit -m x)"',
    "eval of a literal string": "eval 'unset CLAUDECODE; git commit -m x'",
    # Round 3's 🟡 2: the environment emptied with another option first.
    "env -v -i": "env -v -i git commit -m x",
    "env -u then -i": "env -u FOO -i git commit -m x",
    "env -u glued behind a flag": "env -vuCLAUDECODE git commit -m x",
    "env -S splitting a -u": "env -S'-u CLAUDECODE' git commit -m x",
    "exec -c": "(exec -c git commit -m x)",
```
```python
# tests/test_the_commit_gate_decides_at_the_commit.py,
# test_only_those_words_make_the_reading_judge_a_git_decided_clone: add
        # A string a shell runs keeps its message whole (round 3 of #692).
        "bash -c 'git commit -m \"mentions CLAUDECODE today\"'",
        'echo "$(git rev-parse HEAD)"; git commit -m x',
        # An option that empties nothing (round 3 of #692, 🟡 2).
        "exec git commit -m x",
        "env -v git commit -m x",
        "env -u FOO git commit -m x",
```
```markdown
[docs/commit-review-gate-spec.md, the stand-aside paragraph -- the list becomes]
`core.hooksPath` in any spelling (`-c`, `--config-env`, `git config`), a config
file that can carry it (`include.path`, `includeIf`, `HOME=`,
`XDG_CONFIG_HOME=`), any `GIT_CONFIG*` assignment, the environment emptied
(`env -i` wherever it stands among `env`'s options, `exec -c`), a word naming
`CLAUDECODE` or `CLAUDE_CODE_SESSION_ID` whole (`NAME=`, `env -u`, `unset`,
which leave the stub no session), and a command that does not split. Each is
read inside a string a shell parses again as well -- `sh -c`'s, `eval`'s, a
`$( … )` body, `env -S`'s -- because a word compared whole is one word of the
command, and that string is one word of it (round 3 of #692, executed).

[skills/agent-contract/SKILL.md §9 -- the parenthesis becomes]
words can keep the hooks from running (`core.hooksPath` or a config file
that can carry it, `GIT_CONFIG*`, `env -i` or `exec -c`, a session variable
unset or emptied, in the command or in a string it hands a shell).
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_commit_gate_decides_at_the_commit.py -q` in the round's clone, at the target | 216 passed, 62 skipped, exit 0 |
| `bin/evidence-check .`, unscoped, in the clone at the target | exit 0; 3,492 ok, 0 drifted, 0 broken |
| `git diff --name-only 75577dc0 8b4c6545` on `hooks`, `docs`, `agents`, `skills`, and `git diff --stat 8b4c6545 4fe82d29` | only `skills/verify/` in the merge's delta; `rounds/round-2.md` alone after it |
| one temporary probe script: a fresh scratch world per case, stubs installed by the clone's `hooks/hook-install.py`, the command run through real bash or zsh with the session variables set and no lease (did HEAD move?), then handed to the target's `dispatch.py pre-bash` and the installed 0.16.0 `commit-review-gate.py`; cases c00, n01–n09, x01–x21, x07d, y01–y10, m01–m07, z01, z08 | as reported per finding. c00, a plain commit, was refused by the stub. 0.16.0 answered `ask` rather than `deny` wherever the target's reading had refused the same command first in that world; both are stops |
| the paste-ready `hooks/tokens.py` changes patched into the clone, the x, y, m and z groups re-run, and 66 selected cases of `tests/test_the_commit_gate_decides_at_the_commit.py` and `tests/test_the_old_spellings_reach_the_hook.py` | every 🟡 1 and 🟡 2 case deny; m01–m06 unchanged; y05 and y09 still silent in both readings; 66 passed, exit 0; the patch reverted and the clone's status clean at the target |
| The broad gate: full suite, repository-wide lint, typecheck | not yet — none of the three was run here; it is the sealer's, and it comes due once 🟡 1 and 🟡 2 are answered |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `hooks/creationgate.py:118-126`, `:161-169`, `:271-281` | round 1's 🔴 1 — fixed |
| round-1 | `hooks/commit-review-gate.py:1344-1347`, `docs/commit-review-gate-spec.md:144-161` | round 1's 🟡 2 — fixed |
| round-1 | `hooks/hook-install.py:116-122`, `hooks/githooks.py:237-241` | round 1's 🟡 3 — fixed |
| round-1 | `hooks/worktree-guard.py:1629`, `docs/worktree-guard-spec.md:386` | round 1's 🟡 4 — fixed |
| round-1 | `hooks/creationgate.py:109-115`, `:271-277` | round 1's 🟡 5 — fixed |
| round-1 | `hooks/creationgate.py:125`, `:155-156` | round 1's 🟡 6 — fixed |
| round-1 | `hooks/commitgate.py:179-199`, `hooks/githooks.py:37-42`, `docs/commit-review-gate-spec.md:106-118` | round 1's 🟡 7 — fixed |
| round-1 | `hooks/hooksession.py:102-111`, `hooks/githooks.py:109-118` | round 1's 🟡 8 — fixed |
| round-1 | `hooks/answers.py:76-109`, `hooks/answer-write.py:28` | round 1's 🟡 9 — fixed |
| round-1 | `hooks/commitgate.py:77-79`, `:107-118` | round 1's 🟡 10 — fixed |
| round-1 | `hooks/githooks.py:109-118`, `docs/commit-review-gate-spec.md:156-159` | round 1's 🟡 11 — fixed |
| round-1 | `skills/agent-contract/SKILL.md:241`, `:345` | round 1's ⬜ 12 — fixed |
| round-1 | `hooks/hook-install.py:145-181` | round 1's ⬜ 13 — fixed |
| round-1 | `hooks/cmdline_base.py`, `hooks/worktree-guard.py:1629` | round 1's 🟢 — confirmed |
| round-1 | `seal/` | round 1's 🟢 — confirmed |
| round-1 | `hooks/commitgate.py:129-199` | round 1's 🟢 — confirmed |
| round-1 | `hooks/hooksession.py:102-111` | round 1's 🟢 — confirmed |
| round-1 | `hooks/hook-install.py:184-195` | round 1's ❓ — out of verified scope |
| round-1 | `hooks/githooks.py:109-118` | round 1's ❓ — out of verified scope |
| round-1 | `overview.md` §*Not verified* | round 1's ❓ — out of verified scope |
| round-2 | `hooks/tokens.py:55-87` | round 2's 🟡 1 — fixed |
| round-2 | `hooks/tokens.py:63-87`, `docs/commit-review-gate-spec.md:189-194` | round 2's 🟡 2 — fixed |
| round-2 | `docs/commit-review-gate-spec.md:216-217`, `hooks/answers.py:147-181` | round 2's ⬜ 3 — fixed |
| round-2 | `docs/commit-review-gate-spec.md:218-226` | round 2's ⬜ 4 — fixed |
| round-2 | `docs/commit-review-gate-spec.md:112-143` | round 2's ⬜ 5 — fixed |
| round-2 | `hooks/worktree-guard.py`, `docs/worktree-guard-spec.md:376-398` | round 2's 🟢 — confirmed |
| round-2 | `hooks/tokens.py#steps_around_hooks`, `docs/commit-review-gate-spec.md:189-194` | round 2's 🟢 — confirmed |
| round-2 | `hooks/hook-install.py#write_stubs`, `hooks/githooks.py#decides` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py` | round 2's 🟢 — confirmed |
| round-2 | `hooks/worktree-guard.py`, `hooks/worktree_consent.py` | round 2's 🟢 — confirmed |
| round-2 | `hooks/commitgate.py#_sequencer_commit` | round 2's 🟢 — confirmed |
| round-2 | `hooks/tokens.py#steps_around_hooks` | round 2's 🟢 — confirmed |
| round-2 | `hooks/answers.py#given`, `hooks/hooksession.py#call_args` | round 2's 🟢 — confirmed |
| round-2 | `hooks/commitgate.py#_key` | round 2's 🟢 — confirmed |
| round-2 | `hooks/githooks.py:117-126` | round 2's 🟢 — confirmed |
| round-2 | `skills/agent-contract/SKILL.md:241-251`, `:349-357` | round 2's 🟢 — confirmed |
| round-2 | `docs/commit-review-gate-spec.md:228-233` | round 2's 🟢 — confirmed |
| round-2 | `hooks/cmdline_base.py:1-22` | round 2's 🟢 — confirmed |
| round-2 | `tests/` | round 2's 🟢 — confirmed |
| round-2 | `hooks/hook-install.py#main` | round 2's ❓ — out of verified scope |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
