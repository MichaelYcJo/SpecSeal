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

- The worktree guard (`hooks/worktree-guard.py#walk_command`) and the consent
  writer (`hooks/worktree_consent.py#creation_directory`) read the directories
  `86256492`'s walk named, from the base thread `walk_directories` already
  carries, through a new `cmdline.base_directories`. They never read the
  walk's own directories.
- The policy sentences in both specs, I's ledger rows and changelog fragment
  that describe the guard or the consent writer reading the walk.
- Existing cases that pin I's walk-first behaviour for the guard or the consent
  writer, changed to the base's behaviour with a note.

Out:

- The commit gate. It keeps I's reading, both threads in one tuple, in the
  order it has at `542f920b`, because that order is the order its deny names
  targets in.
- Which segments the guard reads as git (`parse_git`). #674 widened that for
  the guard too (`2>/dev/null git worktree add`), and it stays.
- The redesign of how the gates learn where a command acts (0.17.0).

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 the round-3 chain | Given a clean session holding a dirty `w`, when the command is `cd w; ` + 9 × `2>/dev/null cd nosuch; ` + `cd <missing> \|\| git switch feature/x`, then the guard asks about `w`, and the same chain ending in `git worktree add ../wt` is filed under `w` | `test_the_guard_judges_the_tree_the_base_judged_whatever_the_walk_leads` and `test_the_consent_writer_files_where_the_base_filed_whatever_the_walk_leads` in `tests/test_guard_resolves_the_tree_it_judges.py`; red at `542f920b` |
| S2 PR #690's residuals | `cd w; 2>/dev/null cd <missing>; git switch` and `cd w; cd>/dev/null <missing> && 2>/dev/null cd <O>` + newline + `git switch`: the guard asks about `w`, consent files under `w` | the same two cases; red at `542f920b` |
| S3 base equality | Over a generated corpus, every segment's directories as the guard reads them, the guard's judged tree and consent's filed directory equal `86256492`'s hooks | a background script over `git archive 86256492`, recorded in `overview.md` |
| S4 the gate unchanged | Over a gate corpus, no decision and no reason text changes against `542f920b` | a background script, recorded in `overview.md` |
| S5 the accepted cost | `cd w 2>/dev/null && git switch feature/x` and its two siblings leave the guard on the session's own tree, silent as at `86256492`, and consent files under the session's clone; the commit gate still judges `w` | I13's guard case, changed; the gate's I13 cases unchanged |
| S6 a segment only #674 reads as git | `cd w && 2>/dev/null nice -n 5 git switch feature/x` is judged in `w`, the base thread's as-written directory, not where the second reading unplaces it | `tests/test_guard_resolves_the_tree_it_judges.py`; red at `542f920b` |

## Data & interfaces

`cmdline.base_directories(items, cwd)` has `walk_directories`' signature and
return shape, `[(tokens, wheres)]`. Its `wheres` is the base thread's distinct
directories for the segment, unplaced where the as-written reading of the
command word unplaces it, which is the flag `86256492` read.

## Open questions → questions.md

None. The owner decided the scope on 2026-09-30 (`routing.md`).

Framed 2026-09-30 by the session, before the build.
