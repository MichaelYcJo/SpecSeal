# Round 3 report — a gate decides at the moment of the action (#692)

| Field | Value |
|---|---|
| Round | 3, verifying |
| Target SHA | `4fe82d29439ef0eb53b572f7014795359352a194` |
| Diff verified | round 2's fix range `b6d5bdb2..75577dc0` (five fixes and a ledger re-stamp), and the release merge `8b4c6545` (`origin/release/v0.17.0` at `5180b89e`), which no round had read |
| Ran by | specseal:warden on claude-opus-5-5 |
| Where | a `git clone --no-local` at the target under this round's scratch directory; real git 2.50.1 (Apple Git-155), bash and zsh, through the clone's own stubs in scratch repositories only; every one removed at hand-over |

## How the answers relate, in one picture

```
round 2's five fixes ── every instance re-run, every one closed
   │
   ├─ 🟡 1 the session variables, compared as whole words
   │     → NAME=, env -u, env -uNAME, unset, export -n, declare +x, typeset +x: denied
   │
   ├─ 🟡 2 a config file that can carry core.hooksPath
   │     → include.path, includeIf (a dotted condition too), HOME=, XDG_CONFIG_HOME=: denied
   │     → chmod -x lands, and the written limit now says so
   │
   ├─ but a word compared whole is one word of the OUTER command
   │     → 🟡 1  the same words inside a string a shell parses again (sh -c, eval, "$( … )") land
   │
   ├─ and the env reading looks only at the word right after env
   │     → 🟡 2  env -v -i, env -u FOO -i, env -vuNAME, env -S'-u NAME', exec -c land
   │
   ├─ ⬜ 3, 4, 5 the three sentences are true where a reader meets them
   │     → ⬜ 4  nothing pins the conflicted-merge sentence
   │
   └─ ⬜ 3  two spellings neither reading places a commit in, 0.16.0's as much as the target's
```

## Round 2's answers

### 🟡 1 — the session variables: closed for every spelling of one word, not for the class

Executed, in a stubbed clone with no lease, under bash: n01 `CLAUDECODE= CLAUDE_CODE_SESSION_ID= git commit`, n02 `env -u … -u …`, n03 `unset …`, and this round's x01 `export -n`, x02 `declare +x`, x03 `env -uCLAUDECODE -uCLAUDE_CODE_SESSION_ID`, plus z01 `typeset +x` under zsh. Each lands with git alone, and the target's `dispatch.py pre-bash` answers `deny` for each. The installed 0.16.0 reading stops each too.

The word-whole comparison is why `export -n`, `declare +x` and `typeset +x` are caught although no line names them: a bare `CLAUDECODE` word is enough. That holds only for words of the command as typed, which is this round's 🟡 1.

### 🟡 2 — a config file: closed for its instances, and the `chmod -x` limit is true

Executed: n04 `git -c include.path=<file>`, n05 `HOME=<dir>`, x07 an `includeIf.gitdir:` key, x07d the same key with a dot in the condition's path, x18 `INCLUDE.PATH` in capitals, x20 `git config include.path`, y04 `--config-env=include.path=…`, x04 `GIT_CONFIG_GLOBAL=`, x05 GIT_CONFIG_SYSTEM=. Each lands with git alone and is denied by the target. x19 `XDG_CONFIG_HOME=` is denied and, carrying no hooks path in its file here, was refused by the stub as well.

n06, `chmod -x` on both stubs, lands and the target's reading is silent, which `docs/commit-review-gate-spec.md` now states in the limit beside the removed stub. The sentence is true where a reader meets it.

### ⬜ 3, ⬜ 4, ⬜ 5 — the three sentences are true

- ⬜ 3 (read): `hooks/answers.py#_squash` drops each `\NNN` escape and then every character that is not an ASCII letter or digit, and `hooks/answers.py#given` tests `carried in _squash(a)` over the ancestors' argv. The new sentence says exactly that.
- ⬜ 4 (read): the `post-commit` entry in `hooks/githooks.py#_NARROW` is empty, so a judged commit that lands starts a third interpreter, and so does a person's commit while a lease file stands. Both sentences now count three.
- ⬜ 5 (executed): n07 `git merge --continue` and n08 `git commit --no-edit`, each concluding a conflicted merge in an undeclared clone, are refused by the stub. 0.16.0's reading is silent on n07. n09, a merge with no conflict, lands unjudged, which the new last sentence states. Nothing pins the paragraph's new sentence, which is this round's ⬜ 4.

## The merge `8b4c6545`

The merge changes no file under `hooks/`, `docs/` or `agents/`, and not `skills/agent-contract/SKILL.md` (executed: `git diff --name-only 75577dc0 8b4c6545` on those paths lists only `skills/verify/`). No hook imports `skills/verify/scripts/`: the three hook files naming that directory name it in comments (read). So the merge changed nothing this branch's hooks do or say. The commit after it, `4fe82d29`, touches `rounds/round-2.md` alone (executed).

`bin/evidence-check .`, unscoped in the clone, exits 0 with 3,492 ok, 0 drifted and 0 broken (executed), which covers the `seal/releases/0.15.1.md` resolution.

## New findings

### 🟡 1 — The same words inside a string a shell parses again still land unjudged

`hooks/tokens.py#steps_around_hooks` reads the shlex words of the command as typed. A string that `sh -c`, `bash -c` or `eval` runs, or a double-quoted `$( … )` body, is one word there. Round 2's fixes compare a session name, a config key and `HOME` as whole words, so none of them matches inside that string. Round 1's `GIT_CONFIG*` test is a prefix test, so it misses the assignment as soon as another word comes first inside the string.

Executed, each in a stubbed clone with no lease:

| # | Command | git | target reading | 0.16.0 reading |
|---|---|---|---|---|
| x10 | `sh -c 'unset CLAUDECODE CLAUDE_CODE_SESSION_ID; git commit -q -m x'` | landed | silent | deny |
| y08 | the same inside `( … )` | landed | silent | deny |
| x17 | `bash -c 'export -n CLAUDECODE CLAUDE_CODE_SESSION_ID; git commit -q -m x'` | landed | silent | deny |
| y03 | `eval 'unset CLAUDECODE CLAUDE_CODE_SESSION_ID; git commit -q -m x'` | landed | silent | deny |
| x11 | `sh -c 'cd . && git -c include.path=<file> commit -q -m x'` | landed | silent | deny |
| x15 | `sh -c 'cd . && HOME=<dir> git commit -q -m x'` | landed | silent | deny |
| y01 | `sh -c 'cd . && GIT_CONFIG_GLOBAL=<file> git commit -q -m x'` | landed | silent | deny |
| y02 | `echo "$(cd . && HOME=<dir> git commit -q -m x)"` | landed | silent | deny |
| y10 | `env -S'-u CLAUDECODE -u CLAUDE_CODE_SESSION_ID' git commit -q -m x` | landed | silent | deny |

Why it matters: each is a commit 0.16.0 stopped that this branch lets land with no written limit. That is the bar round 2's 🟡 1 and 🟡 2 were raised at. The reader already knows these strings: `hooks/cmdline.py#reparsed_texts` and `hooks/cmdline.py#substitution_bodies` are what the commit gate itself uses to find a commit inside them. `steps_around_hooks` never asks them.

The fix reads every such string as a command of its own. With it patched into the clone, all nine answered `deny` (executed). Five negatives stayed false, among them `bash -c 'git commit -m "mentions CLAUDECODE today"'`, `sh -c 'git commit -m "read include.path"'` and `echo "$(git rev-parse HEAD)"; git commit -m x` (executed). The patch was then reverted.

### 🟡 2 — An emptied environment still lands when another option comes first

`hooks/tokens.py#_empties_the_environment` reads only the one word after `env`. The `-u` arm round 2 added reads only a word that starts with `-u`. And `exec -c`, which bash and zsh both use to run a command with an empty environment, is named nowhere.

Executed, each in a stubbed clone with no lease:

| # | Command | git | target reading | 0.16.0 reading |
|---|---|---|---|---|
| x09 | `env -v -i git commit -q -m x` | landed | silent | deny |
| x16 | `env -u FOO -i git commit -q -m x` | landed | silent | deny |
| x12 | `env -vuCLAUDECODE` and the same for the other name, then `git commit -q -m x` | landed | silent | deny |
| x08 | `(exec -c git commit -q -m x)` under bash | landed | silent | deny |
| z08 | the same under zsh, the harness's shell | landed | silent | deny |
| y07 | `bash -c 'exec -c git commit -q -m x'` | landed | silent | deny |

Why it matters: these are round 1's 🟡 8, `env -i`, with one more word in front. The owner's P6 reason, that a token misread costs one refusal, covers them the same way. macOS's `env` accepts `-vuNAME` and rejects `--unset=NAME` (executed), so the spelling that works on this platform is the one the arm misses.

The fix walks all of `env`'s options instead of the first, counts `exec -c`, and reads a `-u` glued behind another flag. With it patched in, all six answered `deny`, along with y10 above. `exec git commit`, `env -v git commit`, `env -u FOO git commit`, `env -P /usr/bin git commit` and `env -S 'FOO=1 git commit'` stayed false (executed). The 66 selected cases of the two touched modules passed with the patch in (executed), and the patch was then reverted.

### ⬜ 3 — Two spellings neither reading places a commit in

`git --config-env core.hooksPath=VAR commit` with a space (y05), and `env -S '-i git commit'` (y09), land unjudged. Both readings are silent, 0.16.0's as well as the target's (executed). For y05 the cause is that `hooks/cmdline.py#_git_options` does not list `--config-env` in `takes_value`, so the reader takes `core.hooksPath=VAR` for the subcommand (read). `steps_around_hooks` already returns true for y05, so the stand-aside is not the gap; the reader's git parser is.

This is not a stop the branch dropped, so it is ⬜. It is reported because the policy's list says `core.hooksPath` in any spelling keeps the reading, and a reader of that sentence would take the separated form to be judged. A new issue against the command reader is the candidate home; the owner answers it.

### ⬜ 4 — Nothing pins the conflicted-merge sentence

The sentence round 2's ⬜ 5 added to `docs/commit-review-gate-spec.md` §*A commit git makes for its own rebase, cherry-pick or revert* is true (n07, n08, n09 above). The paragraph's `Enforced by:` line names six cases, and none of them concludes a merge (read). An edit that one day counts `MERGE_HEAD` as a sequencer state would turn n07 silent with every listed case still green. A case to plant is under *Regression tests to plant*.

## Regression tests to plant

- `tests/test_the_commit_gate_decides_at_the_commit.py`, `STEPS_AROUND`: the ten entries in the paste-ready block for 🟡 1 and 🟡 2. Each was seen red by this round: the target's `pre-bash` answered `silent` on the command each entry abbreviates (x08–x12, x15–x17, y01–y03, y07, y08, y10, z08; executed), and the case asserts `deny`.
- The same file, `test_only_those_words_make_the_reading_judge_a_git_decided_clone`: the five negatives in the same block, each executed false with the fix in.
- The same file, for ⬜ 4: a case that conflicts a merge in `world.u`, resolves it, runs `git merge --continue` under the session, and asserts HEAD did not move. n07 is that case by hand.

## Facts for the evidence ledger

- macOS's `/usr/bin/env` reads `--unset=NAME` as `-u nset=NAME` and fails with EINVAL, and accepts a glued `-vuNAME` (round 3 of #692, executed).
- Under bash and under zsh, `exec -c git commit` runs git with an empty environment, and with no lease file its commit lands past the stubs unjudged (round 3 of #692, executed).
- Git 2.50.1 accepts `--config-env <name>=<var>` with a space, and a `core.hooksPath` given that way is applied to the commit (round 3 of #692, y05, executed).

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | A session name, a config key, `HOME` or a `GIT_CONFIG*` assignment inside a string a shell parses again (`sh -c`, `bash -c`, `eval`, a quoted `$( … )`, `env -S`) is one word to the reader, and the commit lands unjudged; 0.16.0 stopped each | `hooks/tokens.py#steps_around_hooks` | open | executed x10, x11, x15, x17, y01, y02, y03, y08, y10: landed, target silent, 0.16.0 deny; patched, all nine deny; class of round 2's 🟡 1 and 🟡 2 |
| 🟡 2 | `env -v -i`, `env -u FOO -i`, `env -vuNAME` and `exec -c` empty the environment past a reader that looks only at the word after `env`; 0.16.0 stopped each | `hooks/tokens.py#_empties_the_environment` | open | executed x08, x09, x12, x16, y07, z08: landed, target silent, 0.16.0 deny; patched, all six deny; class of round 1's 🟡 8 |
| ⬜ 3 | `git --config-env core.hooksPath=VAR commit` with a space, and `env -S '-i git commit'`, are commits neither reading places | `hooks/cmdline.py#_git_options` | open | executed y05, y09: landed, both readings silent; 0.16.0's gap as much as the target's; a new issue is the candidate home, and the owner answers it |
| ⬜ 4 | The conflicted-merge sentence round 2's ⬜ 5 added has no case among the paragraph's `Enforced by:` line | `docs/commit-review-gate-spec.md` §*A commit git makes for its own rebase, cherry-pick or revert* | open | read: the six named cases conclude no merge; executed n07 refused, so the sentence is true |
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

### 🟡 1 and 🟡 2

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

The docstring of `steps_around_hooks` names the kinds in the same order, and takes the same two additions.

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_commit_gate_decides_at_the_commit.py -q` in the round's clone, at the target | 216 passed, 62 skipped, exit 0 |
| `bin/evidence-check .`, unscoped, in the clone at the target | exit 0; 3,492 ok, 0 drifted, 0 broken |
| `git diff --name-only 75577dc0 8b4c6545` on `hooks`, `docs`, `agents`, `skills`, and `git diff --stat 8b4c6545 4fe82d29` | only `skills/verify/` in the merge's delta; `rounds/round-2.md` alone after it |
| one temporary probe script: a fresh scratch world per case, stubs installed by the clone's `hooks/hook-install.py`, the command run through real bash or zsh with the session variables set and no lease (did HEAD move?), then handed to the target's `dispatch.py pre-bash` and the installed 0.16.0 `commit-review-gate.py`; cases c00, n01–n09, x01–x21, x07d, y01–y10, m01–m07, z01, z08 | as reported per finding. c00, a plain commit, was refused by the stub. 0.16.0 answered `ask` rather than `deny` wherever the target's reading had refused the same command first in that world; both are stops |
| the paste-ready `hooks/tokens.py` changes patched into the clone, the x, y, m and z groups re-run, and 66 selected cases of `tests/test_the_commit_gate_decides_at_the_commit.py` and `tests/test_the_old_spellings_reach_the_hook.py` | every 🟡 1 and 🟡 2 case deny; m01–m06 unchanged; y05 and y09 still silent in both readings; 66 passed, exit 0; the patch reverted and the clone's status clean at the target |
| The broad gate: full suite, repository-wide lint, typecheck | not yet — none of the three was run here; it is the sealer's, and it comes due once 🟡 1 and 🟡 2 are answered |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

Needs a fix: yes — 🟡 1 (the words inside a string a shell parses again) and 🟡 2 (an emptied environment behind another `env` option, and `exec -c`).
Loses a record or crashes: no

## Proof block

Files opened this round: `hooks/tokens.py`, `hooks/githooks.py` (the stub text and `_NARROW`), `hooks/answers.py` (`_squash`, `given`), `hooks/commit-review-gate.py` (the stand-aside block), `hooks/cmdline_base.py` and `hooks/cmdline.py` (`reparsed_texts`, `command_strings`, `_git_options`), `hooks/dispatch.py` (the `pre-bash` group), `tests/conftest.py` (the installer fixtures), `tests/test_the_commit_gate_decides_at_the_commit.py` (the fixture world, `pre_bash`, `STEPS_AROUND`, the negatives), `docs/commit-review-gate-spec.md` (the sequencer, stand-aside, limits and latency passages), and the diffs of `b6d5bdb2..75577dc0` and `75577dc0..4fe82d29`. Round 2's record and report were read for coordinates; every verdict above is this round's own.
