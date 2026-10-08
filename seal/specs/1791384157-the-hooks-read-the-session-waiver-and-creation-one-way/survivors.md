# Survivors — the hooks read the session, the waiver and a creation one way

`survivor-check --range origin/release/v0.21.0...HEAD` named 12 places at
`1680ea76`, and each was read in round 1. One stated a retired reading in the
present tense, the docstring of
`test_consent_is_not_read_out_of_a_command_that_did_not_parse`, and was
corrected at `89bca43f`. The 11 left are of two kinds:

- **Another work item's record.** Work item 1791163981's `spec.md` records
  what that item framed, when `has_token` carried its own `_without_bodies`.
- **History told as history, or a unit that still holds.** The docstrings of
  `has_token` and of cases in `tests/test_the_waiver_can_be_typed.py`,
  `tests/test_guard_resolves_the_tree_it_judges.py` and
  `tests/test_worktree_guard.py` say what a reading did before #868 in the
  past tense; `base_marker` states the base on purpose; and `main()` still
  reaches `segment_cwd`, through `worktree_consent.place`.

Round 2 found that the range row this file held excused the whole branch
where a row per place was writable. Each place has its own row now, anchored
on a quote from the standing text, so its exemption stops holding when that
text changes.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token/spec.md` | Where `tokens.without_bodies` cannot load or raises | another work item's record of what it framed |
| `seal/specs/1791163981-the-worktree-guard-asks-about-a-message-search-and-reads-no-body-token/spec.md` | `has_token` reads no body (#780) | another work item's record of what it framed |
| `tests/test_worktree_guard.py` | `main()` asks `segment_cwd` for the `-C` target | `main()` reaches `segment_cwd` through `worktree_consent.place`, on the segment's own tokens |
| `tests/test_the_waiver_can_be_typed.py` | The judgment read drops comments, so a command carrying an apostrophe | still true of the judgment read; the docstring tells the consent read's history as history |
| `tests/test_the_waiver_can_be_typed.py` | That answer used to be handed to the CONSENT read | history told as history |
| `tests/test_the_waiver_can_be_typed.py` | The waiver was honoured before the judgment read started dropping comments | history told as history |
| `tests/test_guard_resolves_the_tree_it_judges.py` | the rule `hooks/tokens.py#given` has kept for the commit gate since #773 | `given` is the one consent reader since #868 and still keeps that rule |
| `tests/test_guard_resolves_the_tree_it_judges.py` | holds no repository sent the guard to | history told as history |
| `tests/test_guard_resolves_the_tree_it_judges.py` | The judgment read strips a subshell opener | still true; `has_token`'s half is told in the past tense |
| `hooks/worktree-guard.py` | The commit gate learned this about | history told as history |
| `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py` | `has_marker` as it stood at `94d7b2e0` | `base_marker` states the base on purpose |
