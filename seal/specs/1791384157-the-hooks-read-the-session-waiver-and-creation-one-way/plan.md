# Implementation Plan: the hooks read the session, the waiver and a creation one way (#868, #856)

<!-- seal/specs/1791384157-the-hooks-read-the-session-waiver-and-creation-one-way/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-10-08 by the repository owner, when `smith` was spawned.

<!-- The line above is the record that the gate happened. Fill it in at the
spawn: reading this plan and spawning the builder IS the approval, so nothing
extra is being asked for here — only that the approval stop living in a
transcript. -->

## Summary

Four facts every gate depends on are read in more than one place, and the
readings disagree (#868): where a creation lands, which process is the
session, whether a waiver token was typed, and what a failed git call means.
Each gets one reader the hooks import, chosen so the reader refuses what it
does not recognise, and each copy that disagreed leaves the tree. #856's
brace expansion is answered from §A of `docs/worktree-guard-spec.md` as #826
wrote it: a word bash expands before git reads it is a shape the guard does
not recognise, so it stops where the tree matters, like every other such
shape, and is neither predicted nor named a limit.

`spec.md` In 1–6 is the contract; this file is the order the work arrives in
and why each design was chosen over its alternative.

## Technical context

Coordinates at 5623d728 (`seal/specs/1791382684-…/inventory/1-hooks-shell.md`
and `2-hooks-rest.md` are the inventory's; the line numbers below were read
again by the framer on 2026-10-07).

**Placement (In 1).** `hooks/worktree-guard.py:2998` takes `wheres[0]`;
`judgeable` (wg:596-636) falls back twice; `_tokenize_with_separators`
(wg:232-276) doubles backslashes on Windows. `hooks/worktree_consent.py:419-453`
(`creation_directory`) walks the same `cmdline_base.walk_directories` and
takes the first entry that is not `Unresolved`, with no doubling. The frozen
walk's `wheres` is the failure branch first, then the skipped live shells
(`hooks/cmdline_base.py:1950-2020`), which is why `wheres[0]` is the
directory bash runs a `||` segment in. `tests/test_the_frozen_reading_never_grows.py#test_only_the_two_fallback_arms_read_it`
pins which modules import `cmdline_base`; the one placement function goes
into `worktree_consent.py`, an importer already, so that case is untouched.
The guard already imports `worktree_consent` (wg:188).

**Session (In 2).** `hooks/hooksession.py:40-65` (`claude_ancestor`, basename
test, depth 20), `:81-102` (`call_args`, the same test), `:139-148`
(`session`, `CLAUDE_CODE_SESSION_ID` only). `hooks/session-lease.py:57-85`
(`owner_pid`, substring test, depth 15). `hooks/worktree-guard.py:1213-1229`
(`sessions_in_tree`, basename test over `ps -axo`). `hooks/githooks.py:117-125`
(`_P2`, two variable names). `hooks/tokens.py:117-128` (`steps_around_hooks`,
the same two names). Measured by the framer in a Bash child on 2026-10-07:
`CLAUDE_PID` is exported and equals the `claude` ancestor's pid; the `claude` — NAME NOT IN TREE
process's own environment could not be read with `ps -E`, so whether a hook
process sees the variable is `questions.md` M1.

**Waiver (In 3).** `hooks/tokens.py:44-88` (`words`, `without_bodies`,
`_bare`, `given`); `hooks/commit-review-gate.py:657-697` (`has_marker`,
`_reads_marker` with the substring fallback at :695), callers at :1122 and
:1418; `hooks/worktree-guard.py:381-440` (`has_token`), `:442-459`
(`_without_bodies`, the frozen fallback), callers at :1974 and :3119;
`hooks/answer-write.py:29` reads `tokens.given`. The substring fallback's
own argument (crg:663-665) was made when the PreToolUse reading was the only
gate; since #692 the refusal names `git -c specseal.waive=review`
(`docs/the-commit-gate-inside-git.md` §*The arms*), and `hooks/tokens.py`'s
docstring already records the choice to refuse (*an unbalanced quote reads
nothing*).

**Failed git (In 4).** `hooks/gate.py:65-79` (`git`, `""` on failure),
`:93-95` (`touches_code`), `:98-131` (`arms_missing`, `paths()` asked only
for the parity arm); `hooks/commit-review-gate.py:571-583` (`git`, the copy),
`:598-636` (`changed_paths`); `hooks/commitgate.py:71` (`config --get-all`),
`:224-229` (`pre_commit`), `:241` (`symbolic-ref -q`), `:258-266`
(`_paths_between`). A hook that raises is a non-zero exit with a traceback,
and a PreToolUse gate that raises reaches `hooks/dispatch.py:134-170` as a
pending failure record and the call goes ahead, so the failure has to be an
answer the caller handles, not an exception.

**Brace (In 5).** `hooks/worktree-guard.py:2261-2292` (`_git_finding`),
`:2158-2184` (`_plain_words`), `:2226-2258` (`_rebase_names_a_branch`, the
docstring phrase at :2246), `:2571-2718` (`_described`, one branch per
finding kind in both languages), `:284-296` (`_judgment_text`). The quoted
spans of the judgment text are removable with the regex
`hooks/tokens.py:216` already uses. #856's round-1 report
(`seal/specs/1791334956-…/rounds/round-1-report.md`) holds the executed
table: both brace rebases moved HEAD under git 2.50.1 and were silent in an
ACTIVE tree at 71e4b3a3 and at the base. The stop-cost method is
`seal/specs/1791270162-…/phases/phase-1.md` §*Method*: every Bash `tool_use`
in every `*.jsonl` under `~/.claude/projects/*SpecSeal*/`, distinct
(command, cwd) pairs, each walked by the frozen reading, tree-blind, with a
self-check on the spec's own shapes before any zero is trusted.

**The failure scenario of the chosen approach.** In six months a fifth hook
needs the session or a creation's directory and writes its own walk beside
the one reader, because nothing in the tree stops a new copy. What catches
it is #835's registry: every reader this work adds or removes is a row of
#834's table with its input class, and this plan names each (below) so that
frame can read them. The brace rule is itself a text read, a guess about
quoting from a regex; what bounds it is that every answer it gives is a stop
or silence-as-today, never an allow the base refused, and
`test_no_listed_form_moves_head_under_git` keeps the listed forms honest
under git.

**Input class of every reader this work adds or changes**, in #834's words:

| Reader | Reads | Class | Unknown |
|---|---|---|---|
| the one placement function (`worktree_consent`) | the frozen walk's `wheres` and the segment's `-C` | guess | refused to the session's own tree |
| `hooksession.is_claude`, `claude_ancestor` | `ps -o ppid=,comm=` — NAME NOT IN TREE | guess | passed (no `claude` is no session, a person's own commit) |
| `hooksession.claude_pid` | env `CLAUDE_PID`, else the walk — NAME NOT IN TREE | observed, then guess | as above |
| `githooks._P2`, `tokens.steps_around_hooks` | the one session variable name | owned | — |
| `tokens.given` (now the only token reader) | bare words of the command and of `without_bodies` | guess | refused (no split, no token) |
| `gate.git` (now the only runner) | git's exit code and stdout | observed | refused (`None`, and the parity arm asks) |
| `_git_finding`'s `brace` arm | the frozen words and the judgment text's unquoted spans | guess | refused (a stop where the tree matters) |

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #856 (a): expand braces in the guard, so `{main,feature/x}` becomes two words before the shape is read | a shell-prediction rule in the one family that did not converge after its redesign (#834 part 8: 6 issues, 4 reopenings, two filed after #850). The next spelling — `$'…'`, `{a..z..2}`, a brace glued across a quote, zsh's brace-class option — reopens it, and each expansion the guard performs is one more place its words are not the frozen reading's | rejected |
| #856 (b): name brace expansion a known limit | the two measured commands switch HEAD and are silent in an ACTIVE tree, which is the Premise's own failure; the Known-limits bullets name shapes that fall back to a tree the guard still judges, not shapes it lets through where the tree matters | rejected |
| #856 (c): a word holding an unquoted brace expansion in a git segment is unrecognised | §A's rule applied to one more thing the frozen reading cannot read; costs a stop where the tree matters, with a plain spelling the model can rewrite under the press; a quoted brace beside an unquoted one in another segment over-stops (named) | **chosen** |
| In 1: unify placement on the writer's rule (first resolved entry) | wrong for `cd X \|\| …`, where the resolved entry is the branch bash skipped, and for `cd <missing> ; …`, where it names a directory that holds nothing; measured by the framer's probe | rejected |
| In 1: unify on the guard's rule, in `worktree_consent.py` | the guard's answer is the base's on the three pinned chains (probe) and bash's on the two that disagreed; no new importer of `cmdline_base` | **chosen** |
| In 1: a new module `hooks/placement.py` | a new file, and a new importer of the frozen reader that `test_only_the_two_fallback_arms_read_it` would have to learn | rejected |
| In 2: align the predicate only, keep three walks | three readers of one fact, each guessing; the registry would list three rows for one question | rejected |
| In 2: one reader, `CLAUDE_PID` first, the walk under it | an observed value where the harness exports it; where it does not, today's walk; §13 is why the walk stays | **chosen** |
| In 2: keep `$CLAUDECODE` in the stub and in `steps_around_hooks` | not wrong, but two names for one fact in two places, and the second exists only because of the first. With it gone the verdict is unchanged in every state: variable set → judged through the environment; unset, lease standing → judged through the lease (the stub starts Python for a lease); unset, no lease → not judged, which Python answered the same way after starting | rejected |
| In 3: keep `has_marker`'s substring fallback | a waiver read where the command did not split, which is reading loosely in the one direction that waives with nobody asked; the argument for it predates the git-native spelling the refusal now names | rejected |
| In 3: three readers through one `tokens.given` | one splitter, one body rule, one parenthesis rule; the only behaviour change is on a command that does not split, where the refusal already names the way on | **chosen** |
| In 4: `gate.git` raises on failure | in a git hook, a traceback and a refused commit with no reason text; in a PreToolUse gate, a pending failure record and the call goes ahead (`dispatch.py:161-170`), which is silence | rejected |
| In 4: `gate.git` answers `None` on failure, `""` on an empty answer, and the parity path reader turns `None` into *asks* | each caller says at its own line which exit is an ordinary *no*; the parity arm asks where it was silent; nothing else changes | **chosen** |

## Phases

Vertical slices — each phase ends with something runnable and verified.
Every new case is seen red at 5623d728 first (§15), and each phase record
says how. No phase runs the broad gate; the sealer does (§2).

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **Measure before building; nothing in the tree but the record.** A deleted `test_tmp_*` probe by the method of 1791270162's phase 1 over the recorded corpus, tree-blind: M2, pairs holding a git segment with an unquoted brace expansion, by subcommand (In 5's new stop class, an upper bound); M3, pairs that do not split and carry a waiver token as a substring (In 3's cost); and the self-check on S11's and S12's shapes before any zero is trusted. M1 answered where it can be (`questions.md`). `phases/phase-1.md` with the tables, user paths rewritten to `/Users/x/`; the probe, its result files and every scratch directory gone (§7) | the record's tables; the self-check line; `ls` of the scratchpad showing no `test_tmp_*` of this phase | 84535260 |
| 2 | **One placement (In 1).** The adapter and the placement function in `hooks/worktree_consent.py`; `creation_directory`, the guard's `judgeable` and `_tokenize_with_separators` through them; S1–S3 planted red at 5623d728 first; the `Creation consent` sentence of `docs/worktree-guard-spec.md` with its pin | `uv run --frozen pytest -q -p no:cacheprovider tests/test_guard_resolves_the_tree_it_judges.py tests/test_the_guard_asks_once_per_session.py tests/test_the_frozen_reading_never_grows.py`, exit code read directly (§1); the red run of each new case in `phases/phase-2.md` | e1cca725 |
| 3 | **The brace shape (In 5).** `_git_finding`'s `brace` arm reading the frozen words and the judgment text's unquoted spans; `_described`'s text in both languages; S11–S13 red first; `_rebase_names_a_branch`'s docstring; §A's brace sentence, its two costs and phase 1's M2 figure in the failure-direction paragraph, §*Known limits*' hidden-spelling bullet, each with its `Enforced by:` line | `uv run --frozen pytest -q -p no:cacheprovider tests/test_worktree_guard.py tests/test_guard_resolves_the_tree_it_judges.py` and the policy-pin module for the guard spec; the git-binding case executed under bash | b5ceec40 |
| 4 | **One session reader (In 2).** `hooksession.is_claude`, `claude_pid`, `SESSION_VARIABLE`; `session-lease.py#owner_pid` and `sessions_in_tree` through them; `_P2` formatted from the one name; `steps_around_hooks` reading it; S4–S6 red first, the `CLAUDECODE` fixtures of `test_the_commit_gate_decides_at_the_commit.py` rewritten to the one name with one flipped to plain; `docs/the-commit-gate-inside-git.md` §*A commit with no Claude session* and the stand-aside paragraph's word list, pinned — NAME NOT IN TREE | `uv run --frozen pytest -q -p no:cacheprovider tests/test_lease_liveness.py tests/test_the_commit_gate_decides_at_the_commit.py tests/test_the_hooks_are_installed_where_git_runs_them.py tests/test_worktree_guard.py`; `test_s9_*` green; the stub text asserted free of `CLAUDECODE` | 8f056802 |
| 5 | **One waiver reader and one runner (In 3, In 4).** `tokens.without_bodies` with the frozen fallback; `has_marker` and `has_token` through `tokens.given`, `_reads_marker`, the guard's `carries` and `_without_bodies` gone; `gate.git` answering `None`, `crg.git` gone, each caller's ordinary-*no* line explicit, the three path readers handing `None` through and `touches_code(None)` True; S7–S10 red first, S8's property case over the three corpora; the consent-read paragraph of `docs/commit-review-gate-spec.md`, §*The arms* of `docs/the-commit-gate-inside-git.md` and §*Parity arm* of `docs/the-review-and-parity-arms.md`, pinned | `uv run --frozen pytest -q -p no:cacheprovider tests/test_the_old_spellings_reach_the_hook.py tests/test_one_heredoc_shape_is_data_to_the_commit_gate.py tests/test_gate_judges_the_repo_it_commits_to.py tests/test_chain_hooks_hardening.py tests/test_the_commit_gate_decides_at_the_commit.py tests/test_guard_resolves_the_tree_it_judges.py tests/test_a_gate_that_fails_says_so.py`; `uvx ruff check hooks/` for the dead imports | 077c0bc6 |
| 6 | **The fragments and the closures.** `seal/ledger/1791384157-….md` with a row per scenario and the `Re-read ·`/`Corrected ·` rows for G3, G6 (0.17.0), W1 (0.18.2), T1 (0.18.3), F3 and R1 (0.20.0), written in one pass; `changelog.md` naming #868 and #856 and carrying phase 1's two figures; `overview.md` with the divergences, the `Not verified` table (Windows, read not run — the repository owner) and what was fed back; `plan.md`'s Status column closed | `bin/evidence-check . --strict`, `bin/correction-check` where the fragment carries corrections, and the five text-hygiene modules the framer ran, exit codes read directly | |

This table is also where the work records how far it got. There is no separate
task list: a list of tasks is mutable progress, and a stale one asserts a state
that is not true, which is the failure the evidence ledger exists to prevent.

**Status is empty, or the commit that closed the phase.** A tick is refused,
and so is `done`: both can be typed without anything having happened, and both
assert a present state that nobody can check. A commit hash asserts a past one
— someone can open it — which is the same trick that lets a round record live
beside the contract rather than in tool state.

Fill it in as each phase closes, not at the end. A phase reconstructed
afterwards is reconstructed from the diff, which is where it already was.

What a phase discovers while it is being built, and needs the next phase to
know, does not fit in this table's cells. Write it to
`seal/specs/<work-item-id>/phases/phase-N.md`, from `templates/sdd-phase.md`,
when the phase closes.

One caveat, so nobody builds on it: where feature branches squash, these
commits stop resolving at the merge, and a rebase during the work does the
same thing earlier and more quietly. Re-read the column after any rebase.

## Seams with the 0.21.0 siblings

None of the brief's siblings names a unit this plan changes
(`hooks/worktree-guard.py`, `worktree_consent.py`, `hooksession.py`,
`session-lease.py`, `githooks.py`, `tokens.py`, `gate.py`,
`commit-review-gate.py`, `commitgate.py`, and the four policy documents of
S15). #835's registry reads #834's table, and the table rows for the readers
above change with phases 2–5: the input-class table in *Technical context*
is what that frame reads. #867 reads `seal/config.md` and the coordinate
grammar, which phase 6's fragment uses as every fragment does.

## Operational impact

- The stub's bytes change (one variable name), so `hooks/hook-install.py`
  rewrites every opted-in clone's three stubs at the next session or Bash
  call, silently, as it does for a plugin move.
- `CLAUDECODE= git commit -m x` and `env -u CLAUDECODE git commit -m x` are
  plain and stand aside where git decides; `CLAUDE_CODE_SESSION_ID=` forms
  are judged by the reading as today.
- A command that does not split and carries `[no-review]` or `[no-parity]`
  as a substring meets the refusal; the way on is
  `git -c specseal.waive=review`, which the refusal names.
- In a repository declaring `seal/parity.md`, a commit whose `git diff`
  fails meets the parity question where it met silence.
- The guard's stop gains one kind, `brace`, with its own text in both
  languages; under the press it is a `deny` with the plain spelling.
- A lease may record a pid for a session whose process is not named
  `claude`, where the harness exports `CLAUDE_PID` to its hooks (M1).
- No migration, no new dependency, no new environment variable the plugin
  sets.
