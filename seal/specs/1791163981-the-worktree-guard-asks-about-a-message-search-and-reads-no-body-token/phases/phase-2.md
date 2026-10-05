# 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | cc7344ca |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#790, built as `plan.md` J: keep `is_ref`'s `<name>^{commit}` lookup first
and OR onto it resolve-then-peel, the `<a>...<b>` rule with exactly one merge
base, and the remote-tracking guess over every remote (P1's default). A
fixture with a real git and the A2, A3 and A5 cases; the generated A4
comparison with the base; §*Which tree*'s first paragraph and §*Known limits*
amended, and the pin moved, in the same commit as the code; the stale comment
above the `KINDS` rows rewritten with round 2's paste-ready words. Every new
case seen red at `a3aa139a` before it is committed.

## What this phase found

**The lookup is three helpers and one OR.** `hooks/worktree-guard.py#_commit_named`
asks `<name>^{commit}` first, exactly as `a3aa139a`'s `is_ref` did, and only
where that fails resolves the name alone and peels the object name it gives.
`#_one_merge_base` splits at the first `...`, reads an empty side as `HEAD`,
resolves each side through `_commit_named` and asks `git merge-base --all` for
exactly one line. `#is_ref` runs the first, then the second only for a name
holding `...`. `#tracked_in_any_remote` lists `refs/remotes/` once and finds a
ref ending in `/<name>`; `classify` ORs it beside the base's `origin/<name>`
lookup, and the `)` peel reads through all three.

**The guess is wider than `spec.md` §*Scope* In 2's words, in the louder
direction.** In 2 says `refs/remotes/<remote>/<name>` in any remote. The build
reads any remote-tracking ref that ends in `/<name>`, which also takes a name
that is the tail of a longer remote branch (`x` beside `origin/feature/x`).
Reading the remote names would cost a second call and read git config, which
the guard does not; a remote whose own name holds a `/` is covered without it.
Every extra shape is one git refuses, so it costs a prompt on a command that
would not have run. §*Known limits* names it beside the `--detach` and
two-remote shapes M1 found, and `overview.md` records the divergence.

**A2's second clause does not hold for the guess, and the frame anticipated
it.** A2 says a form git refuses keeps the base's verdict. Under `checkout
--detach <name>` git takes no guess and refuses, and the build reads a switch
for a name only `upstream` holds, where the base read none. `spec.md` §*Out*
("a name git refuses but the guard resolves") and In 2 accept that direction,
so `test_a_name_git_refuses_keeps_the_bases_silence` holds A2 for the C1 and
C2 forms and the guess's refused shapes are named in §*Known limits* instead.

**Red at `a3aa139a`, executed.** With the cases written and `hooks/` as it
stood at `a3aa139a` (the worktree's first two commits touch only this
directory), 27 of the 75 selected cases failed: 22 of
`test_every_name_git_moves_the_tree_on_is_read_as_a_switch` (both message
searches and every merge-base form under all four carriers, the guess from
`upstream` under its two), the three `test_a_subshell_checkout_resolves_a_name_git_resolves`
cases, `test_a_message_search_over_a_dirty_tree_is_asked` (silent where it now
asks) and `test_nothing_the_base_read_as_a_switch_goes_quiet`, whose red at
the base is only that `tracked_in_any_remote` did not exist yet; its real red
is the mutation below. The pin `test_the_guard_policy_says_what_it_reads_past_the_base`
was red with `a3aa139a`'s `docs/worktree-guard-spec.md` put back and green
with the amended one.

**Every new unit was broken once, and a case went red for all but one.**
Executed with `bin/mutation-check` over the new cases, one break at a time:

| Break | Cases that went red |
|---|---|
| no resolve-then-peel (`named = None`) | 10, the message searches |
| no base step, resolve-then-peel alone (`plan.md` C) | `test_nothing_the_base_read_as_a_switch_goes_quiet` (`checkout ^main` goes quiet) |
| the object name used without the peel | 2, a blob and a tree |
| one or more merge bases instead of exactly one | 1, the criss-cross |
| an empty side not read as `HEAD` | 8 |
| no merge-base rule | 13 |
| the guess finds nothing | 3 |
| `classify` skips the guess | 2 |
| the `)` peel skips the guess | 1 |
| `_verified` ignores the exit code | 3: `git rev-parse --verify --quiet` prints for `<a>..<b>` and `<rev>^@` and still fails |
| `_one_merge_base` without its `None in sides` test | **survived** |

The survivor is an equivalent break: without the test, a side that names
nothing hands `None` to `subprocess.run`, which raises before any process
starts, and the `except` answers no. The test stays because it says what the
code means rather than leaning on an exception. Two conditions that could not
change an answer were taken out of `tracked_in_any_remote` instead
(`cc7344ca`): its exit-code test (a failed listing prints nothing) and a
length bound (no ref ends in a bare `/`, and a name whose remote part is
empty is a ref the lookup before it already found).

**The touched modules pass.** Executed at `7c0ae048`:
`tests/test_guard_resolves_the_tree_it_judges.py`, `tests/test_worktree_guard.py`,
`tests/test_the_frozen_reading_never_grows.py` and
`tests/test_one_word_one_meaning.py`, 493 passed; `uvx ruff check` and `uvx
ruff format --check` clean on both touched Python files. The new cases were
run again at `cc7344ca` by the mutation runs' baselines. `hooks/cmdline_base.py`
is untouched.

**W2, the policy's words for #790**, written here: §*Which tree*'s first
paragraph now says two rules are read past the base and states the second
clause by clause against `_commit_named`, `_one_merge_base` and
`tracked_in_any_remote`; §*Known limits* gains the bullet on names git refuses
that are still read as a branch. Both are pinned by
`test_the_guard_policy_says_what_it_reads_past_the_base`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the comment above the `KINDS` rows saying a `--` takes every name out of a checkout | replaced in place by round 2's words: a `--` with a word after it does |
| `is_ref`'s single-call body | `_commit_named`, whose first step is that call unchanged |
