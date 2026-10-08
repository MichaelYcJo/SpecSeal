# Survivors — the hooks read the session, the waiver and a creation one way

`survivor-check --range origin/release/v0.21.0...HEAD` named 12 places at
`1680ea76`, and each was read in round 1. One stated a retired reading in the
present tense, the docstring of
`test_consent_is_not_read_out_of_a_command_that_did_not_parse`, and was
corrected at `89bca43f`. The 11 left are of two kinds:

- **Another work item's record.** Work item 1791163981's `spec.md` (lines
  175 and 178) records what that item framed, when `has_token` carried its
  own `_without_bodies`.
- **History told as history, or a unit that still holds.** The docstrings of
  `has_token` and of cases in `tests/test_the_waiver_can_be_typed.py`,
  `tests/test_guard_resolves_the_tree_it_judges.py` and
  `tests/test_worktree_guard.py` say what a reading did before #868 in the
  past tense; `base_marker` in
  `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py` states the
  base on purpose; and `main()` still reaches `segment_cwd`, through
  `worktree_consent.place`.

| Range | Grounds |
|---|---|
| `origin/release/v0.21.0...HEAD` | the removed readings' sentences stand in work item 1791163981's record and in docstrings that tell a reading's history as history or describe a unit that still holds; each was read in round 1, and the one stating a retired reading in the present tense was corrected |
