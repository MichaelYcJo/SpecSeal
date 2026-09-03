# 1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in — routing

<!-- seal/specs/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in/routing.md — the answer
given before the first edit, in the batch the `implement` skill collects
(§1). Committed, because the check happens at the pull request and CI sees
only what is in the tree.

The rows are read by machines and their vocabulary is fixed. Anything else in
this file is for people. -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | feat/the-tree-that-must-stay-clean-has-no-way-to-opt-in |

Answered 2026-09-02 by the repository owner, before the first edit.

## Why this way

Ticket #80, first in 0.5.0's list in `docs/flow.md` because the rest of the
release stands on it: a repository that must not carry the plugin's files in
its tree gets local mode under `.git/seal/`, and the once-per-repository
moment where the `implement` skill creates the root asks one question, shared
or local. It changes where every hook finds the root, so it goes through the
chain; the pull request lands on `release/v0.5.0` and is squash-merged there
when CI is green — the owner approved that endgame before sleeping, with the
defaults of `questions.md` taken and the owner-only decisions recorded there.
The smith is spawned once per phase of `plan.md`, and the first spawn writes
the spec, plan and questions alone and stops, so the frame is read before
anything is built.
