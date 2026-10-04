# 1791119070-a-waiver-inside-a-here-document-body-is-data — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 9f3bb358 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The behaviour, its words and its pins, in one commit. First the cases: S1,
S2, S3, S5 and S6 in `tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py`,
and S4's rows in `tests/test_the_old_spellings_reach_the_hook.py`, each shown
red against the base hooks (S3 green there). Then one shared body-stripping
function in `hooks/tokens.py` (`one_heredoc.reduce` where it matches, else
`cmdline.drop_heredoc_bodies`), read by `commit-review-gate.py#has_marker` and
`tokens.py#given` and ANDed with each one's base read, so the change can only
turn a silent pass into a stop. No new tokenizer. The four comments, the two
policy sentences, and the `Enforced by:` lines naming the new cases. The
worktree guard's `has_token` stays out (Q1, answered (b), filed as #780), and
`hooks/worktree-guard.py` is sibling D's. Records name the mechanism and the
code coordinate, never a command string that gets past the gate.

## What this phase found

**The frame holds, with one part that nothing can observe.** Every coordinate
the plan named was where it said: `has_marker`'s two call sites, `given`'s
one caller, the three comments, and the two policy sentences. The part that
does not hold as a measurable claim is the `reduce` half of
`tokens.py#without_bodies`. Over the generated corpus
`tests/test_one_heredoc_shape_agrees_with_the_shell.py#corpus` and
`#program_corpus`, 756 admitted one-shape strings each with the token added
on a body line, `drop_heredoc_bodies` alone never kept a body token
(executed, a pure-function probe, deleted). Hand-built near-misses on the
terminator line (a trailing space, a tab, a quoted copy, a comment after it)
agreed too. So the mutation that bypasses `reduce` stays green (M2 below),
and no case can be written that tells the two apart today. The branch stays
because the frame chose it and the orchestrator kept the frame. It keeps the
consent reads reading the text the commit reading reads for that shape, and it
holds if the splitter's boundaries move. The overview's divergence section
carries this.

**How red was shown (§15).** The cases were written and run before either hook
was edited, so the run read the base hooks as they stood at `94d7b2e0`.
Seven failed, each with the expected verdict: S1, the three S2 openers and S5
were `silent` where the tokenless command got `deny`, and `given`'s two body
rows returned the token where `()` was expected. S3's four forms, the S6 case
and the other `given` rows were green there, as they must be. The two
`NEWLY_READ` strings in S6 cannot be red at the base, because the base read is
the left side of the AND; they were shown red by mutation (M3, M5).

**Mutations, one at a time, through `bin/mutation-check`.**

| # | Break | Result |
|---|---|---|
| M1 | `without_bodies` returns the text without `drop_heredoc_bodies` | red, 5 cases |
| M2 | `without_bodies` skips `reduce` | survived, see above |
| M3 | `given` reads only `without_bodies`, no AND | red, the `NEWLY_READ` row and S6 |
| M4 | `given` reads only the raw command | red, both body rows |
| M5 | `has_marker` reads only `without_bodies`, no AND | red, S6 |
| M6 | `has_marker`'s second read is the raw command | red, 5 cases |
| M7 | `without_bodies` drops its empty-command guard | survived first; red once the `None` row was added at `9f3bb358` |

**Q2, measured: no existing case relied on a token inside a body.** The eight
modules the plan lists ran after the fix: 720 passed, 77 skipped, 1 failed.
The failure is
`tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`,
naming this work item, which has a `spec.md` and no `overview.md` until phase 2.

**Q3, measured: every documented form is kept.** S3's four forms (the no-op in
front, a trailing comment after the terminator, a trailing comment on the
program's suffix, a comment with an apostrophe) are silent, and all of
`tests/test_the_waiver_can_be_typed.py` passed beside the two host modules,
314 in all.

**Q4, decided by the work.** The function is `tokens.without_bodies`, and
`has_marker` reaches it through the `tokens` module the gate already imports.
The base scan moved into `_reads_marker`, so `has_marker` is the AND of two
calls.

**A module the plan did not name.** `answer-write.py` now imports `cmdline`,
through `given`. `tests/test_a_gate_that_fails_says_so.py#test_a_broken_shared_module_names_every_gate_that_imports_it`
counts the gates a broken `cmdline.py` names, and it went red with one more.
The expected list now names `answer-write.py`. A broken `cmdline.py` now
skips that gate, and a skipped answer writer carries no token to the git
hook, which refuses and names the git-native spelling. That is the closed
direction.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The sentence in `docs/commit-review-gate-spec.md` that the scan for a waiver token sees the command as written | replaced in the same paragraph by what the scan now reads |
| `main`'s comment naming #773 as the open half | replaced in the same comment by what the consent reads now do |
