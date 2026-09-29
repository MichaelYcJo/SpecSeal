# 1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs — phase 3

<!-- seal/specs/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs/phases/phase-3.md -->

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 14dc9fdb |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

Build `plan.md`'s phase 3: strings past redirections, and the hosts
`1790644505` did not mark (`spec.md` §*The class, enumerated*, the string
table). The shells' picker, the `su`/`runuser`/`script` picker and the `env
-S` picker ask a redirection after the flag and read past it, with a spaced
target taken together with its operator. `watch` adds its join without
redirections. `sudo -s`/`-i` with a command and `flock -c`/`--command` become
hosts, with their value-taking options from `man sudo` and `man flock` (Q4).
`parallel` is read for a commit. S4 and S5's host rows are seen red at
`86256492`, the round-1 controls stay silent, and
`test_every_enumerated_wrapper_has_a_shape` still passes.

## What this phase found

**One helper for all four pickers.** `_string_at(words, j)` returns the word
at `j`, which is the word the base asked. Where that word is a redirection, it
also returns the words past it, up to the first that is not one. A spaced
target goes with its operator and is not asked. The shells' first-operand
loop, the `su`/`runuser`/`script`/`flock` picker and `env -S`'s picker in
`reparsed_texts` all call it. `command_strings`'s `env` branch goes through
`reparsed_texts` and gets it too. So every picker asks what it asked at
`86256492`, plus what the shell really runs.

**Q4, answered from the manuals.**

- *`flock`: as stated.* util-linux's flock(1): "Pass a single command,
  without arguments, to the shell with -c." Its options that take a value are
  `-E`/`--conflict-exit-code`, `-w`/`--wait`/`--timeout`, `--start` and
  `--length`. None of them sits between `-c` and its command, and the picker
  takes the word after the flag, so none needs a skip. This machine has
  `flock(2)` and no `flock(1)`, so the page was read at
  `man7.org/linux/man-pages/man1/flock.1.html`.
- *`sudo -s` and `sudo -i`: not as stated.* `man sudo` 1.9.17p2 on this
  machine says the command and its args are concatenated "after escaping each
  character (including white space) with a backslash … except for
  alphanumerics, underscores, hyphens, and dollar signs". A quoted string
  therefore reaches the shell's `-c` as one word, and the shell runs no
  command line out of it. `sudo` stays out of `STRING_HOSTS`, and a pin
  records why. The argv form `sudo -s git commit -m x` does commit, and
  `sudo` the runner has read that since #670 (executed: the pin's second
  assertion). The manual was read, and sudo was not run: running it needs
  credentials this session does not have.

The `$`-exception leaves one shape: a single-quoted `'$CMD'` expanded by the
target user's shell. That shape is a command word expanding at the top level,
which `spec.md` §*Scope* puts out of this work.

**`watch`'s second join was not built.** Phase 1 already made
`names_an_unknown_command` read past a redirection when it re-splits
`watch`'s join, so both of S4's `watch` rows deny without it. `overview.md`
has the divergence.

**`parallel` shares `watch`'s branch in `reparsed_texts`.** Every word that
is not an option is read for a commit. It stays out of `command_strings`
(`spec.md` §*Scope*, Out).

**Seen red.** 24 cases failed at `f614f89c` against phase 2's reader, which
has no string reading past a redirection and no `flock` or `parallel` host.
Phase 2's reader stops a superset of `86256492`'s, so every one of the 24 is
red there too. The two `watch` rows and the `sudo` pin passed there, as the
divergence and the decision say they should.

**Mutants.** Each ran alone under `PYTHONDONTWRITEBYTECODE=1` and was
restored from saved bytes. The tree was clean afterwards.

| # | Branch mutated | Killed by |
|---|---|---|
| 1 | `_string_at` stops at the first word | `env -S 2>/dev/null` |
| 2 | `_string_at` asks a spaced target too | `bash -c 2> /dev/null $CMD` |
| 3 | the shells' picker takes the first operand only | `bash -c 2>/dev/null $CMD` |
| 4 | the `su` picker takes the next word only | `su -c 2>/dev/null $CMD root` |
| 5 | `env -S` takes the next word only | `env -S 2>/dev/null` |
| 6 | no `flock` host | `flock -c` |
| 7 | `flock --command` is no flag | `flock --command` |
| 8 | no `parallel` | `parallel :::` |
| 9 | `sudo` as a host | `TEXTS[behind a runner]` and the `sudo` pin |

**Verification.** Executed at `14dc9fdb`: the 26 modules, 1392 passed and 1
skipped, exit 0. The frame's 42 shapes through `main()` at `86256492` and
here: every S4 row and the `flock` and `parallel` rows moved from silent to
deny, and the two `sudo` rows stayed silent, as Q4's answer says they should.
None moved from deny to silent. `test_every_enumerated_wrapper_has_a_shape`
passed.

**Lines for the pull request, `CONTRIBUTING.md` §*What a change to a gate
must carry*.**

- *A test seen red.* 24 cases at `f614f89c`, and every changed branch has a
  mutant a case kills.
- *Failure direction.* Each picker returns the word it returned at
  `86256492` and adds the words past a redirection. `flock` and `parallel`
  add readings. Nothing is taken away.
- *Prompt budget.* On commands that commit nothing, one new stop. A `flock`
  argv form whose own program takes a `-c` and an expanding operand after it,
  such as `flock /tmp/l gcc -c "$SRC"`, now reads as a host string. That is
  the cost `su` already carried. Phase 6 counts it with the rest.
- *Platform honesty.* String reading only. `flock` and `parallel` are not
  installed here, and `sudo` was read, not run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
