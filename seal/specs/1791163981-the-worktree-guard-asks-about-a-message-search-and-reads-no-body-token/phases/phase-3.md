# 1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 0b22544d |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#780, built as `plan.md` I: `has_token` counts a token only where the base
read of the command as written AND the same read over
`tokens.without_bodies(command)` find it, through the same `_tokenize`,
parenthesis stripping and Windows doubling, falling back to the frozen
reader's `drop_heredoc_bodies` where `tokens.without_bodies` cannot load or
raises. The A6, A7 and A8 cases and the A9 implication case. The docstrings
(`has_token`, `_judgment_text`, the module's retry-token paragraph,
`hooks/tokens.py`'s rule list), §*Choice sites*' token paragraph and both
READMEs' two token rows, pinned, in the same commit as the code. Every new
case seen red at `a3aa139a` first.

## What this phase found

**The read is one inner function run twice, joined by `and`.**
`hooks/worktree-guard.py#has_token` runs its base comparison over the
command, then over `#_without_bodies(command)`. `_without_bodies` asks
`tokens.without_bodies`, and on any exception, `SystemExit` included, falls
back to `cmdline_base.drop_heredoc_bodies`. `tokens` is imported at module
level under the same guard as `wide`, so a broken `hooks/tokens.py` costs the
token read's wider half and not the guard.

**The plan's fallback condition was narrowed during the build.** The first
version took the fallback where `wide` was None as well as where the read
raised. Breaking that test survived: `tokens.without_bodies` imports
`hooks/cmdline.py` itself when it runs, so a module that cannot load already
raises there, and the extra condition read the same failure twice
(`0b22544d`). `spec.md` A8 says the broken reader is made "the way
`test_a_broken_wider_reader_costs_only_the_question` makes it", which sets
`wide` to None and leaves `hooks/cmdline.py` loadable; after the narrowing that
would exercise nothing, so the A8 case loads the guard from a copy of
`hooks/` whose `cmdline.py` exits at load, the way
`test_a_wider_reader_that_exits_at_load_costs_only_the_question` does, and a
second variant makes `tokens.without_bodies` raise. `overview.md` records the
divergence.

**Red at `a3aa139a`, executed.** With the new cases written and the guard as
phase 2 left it (its `has_token` is `a3aa139a`'s), the four
`test_a_token_only_a_body_carries_is_not_read` cases and both
`test_a_broken_wider_reader_reads_no_body_token_and_keeps_a_typed_one` cases,
as first written, failed; the rewritten A8 case was seen red against the base
read put back, the second break in the table below. The six A7 cases and the A9 case passed, as they must, since they pin
what the base already read. The verdicts the A6 cases assert were also run
through `main()` against both copies of `hooks/` by a deleted probe:
`a3aa139a` was silent on both `[shared-tree-ok]` bodies at the cannot-tell
row and asked on both `[worktree-ok]` bodies at the single-stream row; the
build puts the choice on the first two and denies the second two. The pin
`test_the_guard_policy_and_readmes_say_a_body_token_is_not_read` was red with
`a3aa139a`'s `README.md` and `README.ko.md` put back, and red again with its
`docs/worktree-guard-spec.md` put back.

**Every new unit was broken once, and every break went red.** Executed with
`bin/mutation-check` at `0b22544d`:

| Break | Cases that went red |
|---|---|
| the body-free read alone, no AND (`plan.md` F) | 4: A9, through the two commands the splitter finishes only once the body goes |
| the base read alone (`plan.md` G) | 6: A6 and both A8 variants |
| the fallback reads the command as written | 2: A8's two body halves |
| the fallback reads nothing (`plan.md` H) | 4: A8's typed halves |
| the fallback's exception not caught | 4 |
| no parenthesis stripping | 4, `test_the_retry_token_survives_a_closing_parenthesis` among them |

`tokens is None`, the guard on the module-level import, is not broken by any
case: `hooks/tokens.py` loads in every run, and making it fail to load is a
copy of `hooks/` the A8 case already builds for `cmdline.py`. It is named here
rather than pinned.

**The touched modules pass.** Executed at `0b22544d`:
`tests/test_guard_resolves_the_tree_it_judges.py`, `tests/test_worktree_guard.py`,
`tests/test_the_guard_asks_once_per_session.py`,
`tests/test_the_old_spellings_reach_the_hook.py`,
`tests/test_lease_liveness.py` and `tests/test_worktree_guard_signals.py`,
648 passed and 1 skipped; at `f18bd16a` the same six with
`tests/test_the_frozen_reading_never_grows.py` and
`tests/test_one_word_one_meaning.py`, 670 passed and 1 skipped. `uvx ruff
check` and `uvx ruff format --check` clean on the touched Python files.

**W2, the words for #780**, written here: §*Choice sites*' *Where the token
is read from* paragraph says a token inside a here-document body is not read,
by which rule, and what happens where `hooks/cmdline.py` cannot load;
`README.md`'s two token rows and `README.ko.md`'s two rows say the same. Each
is pinned by `test_the_guard_policy_and_readmes_say_a_body_token_is_not_read`.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sentence in `_judgment_text`'s docstring saying a consent read reads the command as written | the same docstring: comments kept, and `has_token` reads it as written and without its bodies |
