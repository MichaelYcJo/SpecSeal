# Feature Specification: past the cap, the guard keeps the tree the base judged

<!-- seal/specs/1790729827-past-the-cap-the-guard-keeps-the-tree-the-base-judged/spec.md
— WHAT this work delivers and how we'll know. The policy documents in docs/
outrank this file; cite them, don't restate. -->

Milestone 49 (0.16.0), item M: #689, the findings round 3 of work item I
(`1790660768`, #674) left when its run ended capped. The branch is cut from
`release/v0.16.0` at `542f920b`, which carries item I. No framer ran. The
session planned it and handed `smith` the frame in its spawn prompt, and
`smith` wrote this file and `plan.md` from that prompt after its first fix
commit (`81dfcbb1`), not before it. The mark at the foot is the checker's fixed
wording; `overview.md` §*Where spec and implementation diverged* records the
order the files were really written in.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/commit-review-gate-spec.md` §*Which repository, and what happens when it cannot be read* > *A `cd` the gate cannot read*, the `STATE_CAP` paragraph | the walk carries the base's states in a thread of their own; whose directories come first is what the worktree guard and the consent writer read |
| `docs/worktree-guard-spec.md` §*Which tree, when the command walks to it* | the tree judged is the one the command acts on; an unreadable destination falls back to the session's own directory |
| `docs/worktree-guard-spec.md` §*Unknowns resolve conservatively* | a wrong deny costs a prompt, a wrong allow breaks another session's tree |
| `CLAUDE.md` §*Repo rule — a change writes fragments, never the shared file* | the ledger rows and the changelog entry go in this item's fragments; the drifted rows of other fragments are re-read where they live |

## Scope

In:

- **🟡 1.** The order of each segment's directories in
  `hooks/cmdline.py#walk_directories`, so that past `STATE_CAP` a directory on
  the branch a `||` skips no longer leads the base thread's, and the class the
  same cause produces (§12): every way a walk whose first directory is
  unresolved still names a readable one behind it.
- **⬜ 2.** I15's exception list in
  `seal/ledger/1790660768-the-commit-gate-reads-the-rest-of-what-a-shell-runs.md`.
- **⬜ 3** and **⬜ 4**, each fixed or refused with grounds in `overview.md`.
- The two policy sentences above, the rows the change drifts, and this item's
  ledger and changelog fragments.

Out:

- How the guard treats an unresolved directory, and how the consent writer
  treats a segment whose readable directories all sit behind unresolved ones.
  That is #686's question, and `overview.md` §*Not done* records what this
  work measured of it.
- The splitter's tokens. ⬜ 3 would need quote-aware tokens, which every
  reader shares.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 — round 3's case | Given a clean session repository with a dirty nested `w`, when `cd w; ` + 9 × `2>/dev/null cd nosuch; ` + `cd <missing> \|\| git switch feature/x` is judged, then the guard asks and names `f.txt`, and the creation twin is filed under `w` | `tests/test_guard_resolves_the_tree_it_judges.py#test_a_skipped_cd_past_the_walks_cap_keeps_the_tree_the_base_judged`, red at `542f920b` |
| S2 — every regain behind an unresolved first | Given the same chain, when the `cd` the `\|\|` skips is spelled behind a redirection the splitter cut, with one after its operand, with one in front, or into a repository, then the guard and the consent writer answer as `86256492` | `…#test_every_skipped_branch_past_the_walks_cap_keeps_the_tree_the_base_judged`, each red at `542f920b` |
| S3 — every capping prefix | Given `cd w &&` in front of the nine, or eight failing `cd`s, then the same | `…#test_a_skipped_cd_past_the_cap_keeps_the_base_tree_whatever_capped_the_walk`, each red at `542f920b` |
| S4 — the same cause with no cap | Given `cd w; 2>/dev/null cd nosuch \|\| (cd O) <op> git worktree add ../wt` for `&&`, `;` and `\|\|`, then the creation is filed under `w`, as `86256492` filed it and where bash creates it | `…#test_a_subshell_behind_a_failing_cd_keeps_the_directory_the_base_named`, each red at `542f920b` |
| S5 — what the fix keeps | Given the capped chain followed by `2>/dev/null cd O && git switch`, then the guard judges `O`, where bash switches | `…#test_past_the_walks_cap_a_cd_landed_past_a_redirection_still_leads`, red at `86256492` and against round 3's proposed fix |
| S6 — the gate's text | Given 9 × `2>/dev/null cd nosuch; ` + `cd <nowhere> \|\| git commit`, then the deny lists `<nowhere>` first | `tests/test_no_shape_the_base_stops_reads_silent.py#test_past_the_cap_the_deny_names_the_directory_the_base_named_first`, red at `542f920b` |
| S7 — the gate's verdicts | Given a generated corpus through the gate's `main()` in three session kinds, then no stop `86256492` made is silent, and no decision differs from `542f920b`'s | probe, recorded in `phases/phase-1.md` |

## Data & interfaces

None. `walk_directories` returns the same set of directories per segment; only
their order moves.

## Open questions → questions.md

None. The one choice this work made between two readings of the spawn's
invariant is recorded with its grounds in `plan.md` §*Alternatives
considered*.

Framed 2026-09-30 by the session, before the build.
