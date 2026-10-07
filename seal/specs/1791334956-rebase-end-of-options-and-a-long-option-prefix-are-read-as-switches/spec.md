# Feature Specification: rebase's --end-of-options and a long-option prefix are read as switches (#854)

<!-- seal/specs/1791334956-rebase-end-of-options-and-a-long-option-prefix-are-read-as-switches/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `docs/worktree-guard-spec.md` §A | what a listed subcommand promises: it leaves HEAD on the branch it was on. A `rebase` that names a branch is unrecognised |
| `docs/worktree-guard-spec.md` §Known limits | where a spelling the guard does not read is named rather than closed |

The frame is round 3 of work item 1791270162 (#826): `seal/specs/1791270162-the-worktree-guard-allows-a-listed-shape-and-asks-the-rest/rounds/round-3-report.md`, with its verdict table, its probes under git 2.50.1 and its *Paste-ready fixes*. That run ended capped. The owner pressed `automation` for this item.

## Scope

In:

1. **🟡 1.** `_rebase_names_a_branch` closes the class of ways git stops reading options or reads a short spelling of one:
   - `--end-of-options` ends options as `--` does;
   - git accepts any unambiguous prefix of a long option, so `--ro` is `--root`, and the guard reads it so.
   
   The case that runs each listed form under git covers the new spellings, so a wrong reading goes red. Whether another long option of `rebase` that takes or changes the branch argument has a prefix the guard misses is the work's to answer: enumerate `git rebase -h`'s long options against git.
2. **⬜ 2.** §A's sentence on the stop's reason says that a reason describing one tree calls it "this tree".
3. **⬜ 3.** §Known limits names the two spellings that fall back to the session's tree: `cd w 2>&1`, and a cut git inside an `if` body after `cd W`.

Out:

- Every other subcommand on `LEAVES_THE_TREE`. Round 3 judged them, and the binding case holds them.
- `questions.md` P5 of 1791270162. It stays as built.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 | Given an ACTIVE tree, when `git rebase --ro feature/x` runs, then the guard stops it as unrecognised | a case red at 3d78c220 |
| S2 | As S1, with `git rebase --end-of-options main -x` | a case red at 3d78c220 |
| S3 | `git rebase --rebase-merges main`, and any other listed rebase that names no branch, stays listed | a case |
| S4 | Every listed form still leaves HEAD where it was under git, and every switching form, the new ones included, moves it | the git-binding case |
| S5 | §A and §Known limits say what S1–S3 do, pinned | the policy pin cases |

## Data & interfaces

- `hooks/worktree-guard.py#_rebase_names_a_branch`: the option-end set gains `--end-of-options`, and a prefix of `--root` counts as `--root`.
- `docs/worktree-guard-spec.md` §A and §Known limits.

## Open questions → questions.md

None. The fix is the reviewer's, probed in round 3 (21 rebase and git-binding cases passed in a clone).

Framed 2026-10-07 by the session, before the build.
