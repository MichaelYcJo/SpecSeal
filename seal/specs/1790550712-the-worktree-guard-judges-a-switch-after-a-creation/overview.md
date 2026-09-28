# 1790550712-the-worktree-guard-judges-a-switch-after-a-creation — overview

📋 implement applied
· spec:     `spec.md` (decisions 1–9, S1–S12), `plan.md` (every section), `questions.md` Q1–Q5, and `routing.md` of this work item; `docs/worktree-guard-spec.md` §A, §*Creation consent* whole, §*What exactly is read*, §*Choice sites*, §*Which tree, when the command walks to it*, §*Known limits*; round 2 of work item 1790381327 §*Paste-ready fixes*; round 3 of work item 1788817291 (from history at `f51e634^`) whole; `CLAUDE.md` *a change writes fragments*; `skills/evidence-check/SKILL.md` §*The records arm*
· evidence: W1–W8 in `seal/ledger/1790550712-the-worktree-guard-judges-a-switch-after-a-creation.md`; twelve rows re-read and re-stamped in `seal/releases/0.15.5.md` (A1, A3, A4, A5), `seal/releases/0.9.1.md` (six rows) and `seal/releases/0.9.4.md` (S3, S4); 0.15.5 A1 and A4 and two 0.9.1 rows corrected in place
· verified: executed — the narrow guard modules and the modules that read the edited files, every seen-red run and the fifteen mutations `phases/phase-1.md` to `phase-3.md` list, the 600-cell before/after probe, the 58-word command-word probe, the heredoc probe, the Q4 transcript count, and `evidence-check --strict` (exit 0); read — `README.md` and `README.ko.md` worktree-guard rows, the released `CHANGELOG.md`; unverified — the full suite, lint and typecheck (below)

## Why this work exists

With consent present, `git worktree add ../x -b x && git switch y` took a
branch out from under an ACTIVE session, because the guard never read a switch
written after a creation. Now the order decides nothing. Alongside, two guard
messages stop claiming a count nobody took, the consent reader refuses an
unmeasured transcript shape, and the policy document states its two command
classes by the cases that hold them rather than by figures nobody can re-run.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| S10's verdict groups | `spec.md` S10: "a committed case pinning at least one member of each group (`allow` · `ask` · silent)" / there is no `ask` group; the case pins `allow` and silent with a record, `deny` and silent without | code | Executed, phase 3: with a record, 58 command words gave 20 `allow` and 38 silent. Round 3 of 1788817291 measured its `ask` cells at `3287c78`, before #257 made a consented compound silent |
| `only_creates_a_worktree` is edited | `plan.md`: "`only_creates_a_worktree@78d05862` is not edited … its anchor does not drift", and its docstring is "read and found true" / the docstring said *Falling to `ask` there*, which is false, and was corrected | code | The same measurement. `plan.md` carries a builder's note under the table |
| S4 | `spec.md` S4: "new case, or the builder's executed before/after table" / an executed table | the table | `phases/phase-1.md`: 600 cells against the base, 28 moved, all of them create-then-switch and all stricter. A case would have pinned base verdicts that other cases already pin |
| §*Known limits*' heredoc line | `plan.md`: deleted on a silent measurement / deleted, and a case added | code | A deleted limit with nothing behind it is a claim nobody can re-run. `test_a_git_command_inside_a_heredoc_body_is_not_judged`, seen red by M15 |
| Where the S10 case is cited | `spec.md` S10: "the paragraph cites it on an `Enforced by:` line" / appended to §*Creation consent*'s single `Enforced by:` line, and named in the paragraph's prose | code | `tests/test_a_folded_statement_names_what_enforces_it.py`: a folded statement has exactly one `Enforced by:` line |
| Copy 6 (`seal/releases/0.15.5.md` A4) | `plan.md` phase 1 / phase 4 | phase 4 | `skills/implement/SKILL.md` §2, *draft as you go, write in one pass*: every drifted row was re-read in one pass |
| `plan.md`'s anchor stamps | framed at the base's hashes / re-stamped to the state their rows were re-read against | code | `evidence-check --strict` grades a drifted stamp in a live record like a drifted ledger row (exit 2), and `plan.md` phase 4's own Verified-by requires exit 0 |
| Two copies the enumeration did not list | `plan.md` §*Enumerated copies*, 19 items / also `judge_creation`'s *only its ONE silent exit falls through to here* (false since round 2 of 1788817291), the module docstring's §A mirror, `test_a_path_qualified_git_carries_no_allow`'s docstring, and the §*Creation consent* prompt-budget sentence *Before consent … still costs one prompt each time* | code | Found by the S12 sweep run by construction, including *falls to `ask`* and *costs … a prompt*. Each is listed in its phase record |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |
| Whether the create-then-switch shape occurs in anyone else's sessions. Q4 counted 0 of 44 creation commands over this machine's 728 transcripts only | nobody can measure another person's history from this repository; the PR body states the count as this machine's |
| The switch arm against a live concurrent session rather than a patched `sessions_in_tree` | #24, already open |
| The new cases on Windows. None of them uses a backslash spelling, which is the one shape `test_a_path_qualified_git_carries_no_allow` already branches on | the CI matrix's Windows leg |

## Not done

**#630**, the two other instances of the walk's cause: a switch in a second
tree and a creation in a second clone are still judged on the first of each
kind. `questions.md` Q1 took its default, defer, and mutation M4 in
`phases/phase-1.md` survives for exactly that reason: the walk's skip decides
first-versus-last only in #630's shapes, and pinning either order there would
pin a defect this work defers.

**`skills/evidence-check/SKILL.md` §*The records arm* and the code disagree on
record drift.** The skill says *`DRIFTED` in a record does not fail the run*;
`evidence_check.py#exit_code` returns 2 under `--strict` for record drift, the
same as ledger drift, and the comment beside the count says drift is graded
the way ledger drift is. Met in phase 4, where this work item's own `plan.md`
stamps made the strict check exit 2. It is outside this work item's files, so
it is handed to the orchestrator to place.

## Fed back into the spec

`docs/worktree-guard-spec.md` gained, *inferred during implementation* and
open to the planners: the §A pointer (a command that also creates is judged by
the switch table whichever comes first); the #620 paragraph in §*Creation
consent*; the property paragraph's restriction to *a session with no consent*,
with the reason; and the §*Known limits* line for a switch into the worktree
the same command creates.
