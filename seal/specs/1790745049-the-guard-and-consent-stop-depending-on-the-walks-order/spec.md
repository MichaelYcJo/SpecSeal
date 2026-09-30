# Feature Specification: the guard and consent stop depending on the walk's order

<!-- seal/specs/<unix-epoch-seconds>-<slug>/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it* | The tree judged is the one the command acts on. This work changes how that tree is read: from the release base's reading, not the commit gate's |
| `docs/worktree-guard-spec.md` §*Unknowns resolve conservatively* | A wrong deny costs a prompt; a wrong allow breaks another session's tree. The containment keeps the base's answers, so it moves neither way against `86256492` |
| `docs/commit-review-gate-spec.md` §*A `cd` the gate cannot read* (#674's paragraphs) | The gate judges every directory, so its reading is unchanged here |
| `routing.md` §*Why this way* | The owner's decision of 2026-09-30: containment for 0.16.0, a redesign for 0.17.0 |

## Scope

In:

- The worktree guard and the consent writer read every command through
  `hooks/cmdline_base.py`, `86256492`'s `hooks/cmdline.py` copied byte for
  byte under a rider, and never through `hooks/cmdline.py`. **Corrected
  2026-09-30** by round 1's fix pass: this item said they read the directories
  of the base thread `walk_directories` carries, through a new
  `cmdline.base_directories`. That thread shared #674's `command_word` and
  `parse_git`, so a segment only the wider reading reads as git took the
  guard's first slot (round 1, red 1) and zsh-prefixed segments were unplaced
  where the base placed them (yellow 2). Plan alternative B, the frozen copy,
  replaced it.
- The policy sentences in both specs, I's ledger rows and changelog fragment
  that describe the guard or the consent writer reading the walk.
- Existing cases that pin I's walk-first behaviour for the guard or the consent
  writer, changed to the base's behaviour with a note.

Out:

- The commit gate. `hooks/cmdline.py` is `542f920b`'s, byte for byte.
- ~~Which segments the guard reads as git (`parse_git`). #674 widened that for
  the guard too (`2>/dev/null git worktree add`), and it stays.~~
  **Corrected 2026-09-30** by round 1's fix pass: the frozen copy makes the
  guard's recognition `86256492`'s too, so #674's widening no longer reaches
  the guard. That is in scope now, as part of the accepted cost (S5).
- The redesign of how the gates learn where a command acts (0.17.0).

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the round-3 chain | Given a clean session holding a dirty `w`, when the command is `cd w; ` + 9 × `2>/dev/null cd nosuch; ` + `cd <missing> \|\| git switch feature/x`, then the guard asks about `w`, and the same chain ending in `git worktree add ../wt` is filed under `w` | `test_the_guard_judges_the_tree_the_base_judged_whatever_the_walk_leads` and `test_the_consent_writer_files_where_the_base_filed_whatever_the_walk_leads` in `tests/test_guard_resolves_the_tree_it_judges.py`; red at `542f920b` |
| S2 PR #690's residuals | `cd w; 2>/dev/null cd <missing>; git switch` and `cd w; cd>/dev/null <missing> && 2>/dev/null cd <O>` + newline + `git switch`: the guard asks about `w`, consent files under `w` | the same two cases; red at `542f920b` |
| S3 base equality | Over a generated corpus, the guard's decision, the kinds it recognised, its judged tree, every segment's directories as it reads them, and consent's filed directory equal `86256492`'s hooks, for every command. **Corrected 2026-09-30** by round 1's fix pass: the row asked for equal directories and trees only, and the build's corpus carried no zsh prefix and no segment the base reads no git in, so it could not see red 1 or yellow 2 | a background script over `git archive 86256492`, recorded in `overview.md` |
| S4 the gate unchanged | Over a gate corpus, no decision and no reason text changes against `542f920b` | a background script, recorded in `overview.md` |
| S5 the accepted cost | `cd w 2>/dev/null && git switch feature/x` and its two siblings leave the guard on the session's own tree, silent as at `86256492`, and consent files under the session's clone; a git behind a redirection or zsh's `noglob`, `nocorrect`, `repeat N` or `for i (…)` is not git to the guard or the consent writer; the commit gate still reads both | I13's guard case, changed; S6's case; `test_a_zsh_prefixed_git_is_not_git_to_the_guard_or_the_consent_writer`; the gate's I13 cases unchanged |
| S6 a segment only #674 reads as git | `cd w && 2>/dev/null nice -n 5 git switch feature/x` is not git to the guard, which is silent as at `86256492`. **Corrected 2026-09-30** by round 1's fix pass: the row said it is judged in `w`, the base thread's as-written directory; that answer came from #674's `parse_git`, which the guard no longer reads | `test_a_segment_only_the_reading_past_redirections_finds_is_not_git_to_the_guard`; red at `4bc94f05` |
| S7 the first slot | A segment `86256492` read no git in, in front of one it read (`2>/dev/null git switch x; cd w && git switch x`, four more), does not take the guard's or the consent writer's first slot: the guard denies over the session active in `w`, and consent files under `w` | `test_a_segment_the_base_reads_no_git_in_does_not_take_the_first_slot` and `test_the_consent_writer_files_the_creation_the_base_filed_behind_a_wider_one`; red at `4bc94f05` |

## Data & interfaces

`hooks/cmdline_base.py` is imported as `cmdline` by `hooks/worktree-guard.py`
(with `apply_chdir` and `parse_git` from it) and by
`hooks/worktree_consent.py`. It has `86256492`'s interfaces, and nothing else
imports it. **Corrected 2026-09-30** by round 1's fix pass: this section
described `cmdline.base_directories(items, cwd)`, which is removed.

## Open questions → questions.md

None. The owner decided the scope on 2026-09-30 (`routing.md`).

Framed 2026-09-30 by the session, before the build.
