# Survivors — a here-document body is data to the commit gate

`survivor-check --range 636ebdb5..HEAD`, run by the builder before the
hand-back at `2d223ab4`, reported two places. It is a record of a moment, and
what it says was true at that moment. Each place is correct as it stands.

| Path | Quote | Grounds |
|---|---|---|
| `hooks/cmdline_base.py` | `"""(stripped, bodies) -- `drop_heredoc_bodies` and `heredoc_bodies` share one pass."""` | the frozen copy of `86256492`'s reader, which no work item edits (`tests/test_the_frozen_reading_never_grows.py`, and `spec.md` §*Scope*). Its `_heredoc_split` still returns `(stripped, bodies)`; the docstring this range changed is `hooks/cmdline.py`'s, whose function now returns records |
| `seal/specs/1791076831-a-here-document-body-is-data-to-the-commit-gate/spec.md` | ("whether the command commits at all is asked of every body separately, as shell, on purpose") and gives the decision to the owner | this work item's own frame, quoting the policy sentence it set out to change, so the quotation is the frame's record of what stood before. The policy itself now carries the owner's answer |
