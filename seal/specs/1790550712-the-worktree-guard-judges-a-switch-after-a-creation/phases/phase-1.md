# 1790550712-the-worktree-guard-judges-a-switch-after-a-creation — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | e5af3c1 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

#620. The walk change in `hooks/worktree-guard.py#main`, so a command carrying
a switch and a creation goes to the switch ladder whichever is written first.
Copies 1–6 of `plan.md` §*Enumerated copies*. The §A pointer and the
§*Creation consent* edits in `docs/worktree-guard-spec.md`, and decision 5's
*Known limits* line. Cases S1, S1b, S2, S3, S6 and the S5 extension of the
writer-record sweep, each seen red at the base. S4 as a case or as an executed
before/after table. Q5 answered when S2 first ran.

## What this phase found

**The frame holds.** Every row of `spec.md` decision 2's table matched what the
cases measured, including the one row that changes a count: with no consent,
in the idle and detection-unusable states, the create-first spelling now
answers `deny, deny, ask` over three attempts where the base answered
`deny, ask, ask`. The first deny is the switch's choice, the second is the
creation's own choice budget, and the switch-first spelling already answered
the same. `plan.md`'s prompt budget says *without consent the counts equal
today's switch-then-create counts*, and that is what was measured.

**Q5: byte for byte.** S2 compares the reason text of both spellings in every
tree state, consent state and attempt, and they are identical. `fmt_snippet`
and `fmt_sessions` read nothing the order can change. The case asserts the
whole reason.

**S4, executed as a before/after table rather than a case.** A `test_tmp_*`
probe loaded the base guard (`git archive afcb3f7 hooks`, in the session's
scratch directory) beside this branch's, and ran 20 commands × 5 tree states ×
2 consent states × 3 attempts, each on its own session id: 600 cells. 28
differ, and every one of them is a creation followed by a switch.

| Commands | Cells that differ |
|---|---|
| `git worktree add ../wt f`, `… && cd ../wt`, `git status && git worktree add ../wt f`, `git worktree add ../wt f && git status`, `… # [worktree-ok]`, two creations in one clone | 0 |
| `git switch feature/x`, `git checkout feature/x`, `… && git status`, `… # [shared-tree-ok]`, `git checkout -- f.txt` | 0 |
| four switch-first shapes (`&&`, `;`, `checkout`, a second switch after) | 0 |
| `git worktree add ../x -b x && git -C ../x switch y` | 0 |
| `git worktree add ../wt f && git switch feature/x`, its `;` and `checkout` forms, and `… && cd ../x && git switch y` | 28 — ACTIVE `ask`/`silent` → `deny`; idle and unusable `deny, ask, ask`/`silent` → `deny, deny, ask`/`deny, ask, ask`; dirty with consent `silent` → `ask` |

No cell moved toward `allow` or `silent`. The probe was deleted after it ran.

**Seen red.** The five new cases were run before `main` was edited: all five
failed (S1 and S1b `silent`, S2 and S3 with the create-first spelling weaker
in the ACTIVE, idle, unusable and dirty-with-consent cells, S6's `cd` half
`ask`). The S5 extension was green at the base, which is correct: the
writer-record property was never broken for create-first, because the
creation ladder ran there. Its three rows are what fails if the walk forgets
the creation once it has found the switch (mutation M2 below).

**Mutations**, each from the committed bytes, restored from a copy and never
from `HEAD`, run over `tests/test_the_guard_asks_once_per_session.py`,
`tests/test_worktree_guard.py` and `tests/test_guard_resolves_the_tree_it_judges.py`:

| Mutation | Red |
|---|---|
| M1′ — the base defect exactly: a switch segment is skipped once a creation was found | the five new cases, and nothing else |
| M2 — a switch found after a creation clears `creation_at` | S5 (`test_the_guard_is_never_silent_where_the_writer_records`), S2, S3, S6's `-C` half |
| M3 — the tree judged is the creation's even when a switch exists | S6 alone |
| M4 — the skip removed, so every segment is classified and the last of each kind wins | nothing |

M4 survives, and it is left surviving on purpose. The skip decides between the
first and the last segment of one kind, which differs only when a command
switches in two trees or creates in two clones. Those are #630's shapes
(`questions.md` Q1), and a case pinning either order there would pin a defect
this work defers. The skip's other job is cost: it stops `classify` from
running `git rev-parse` for every later `checkout`.

**Two copies the enumeration did not list.**

- `hooks/worktree-guard.py#judge_creation`'s docstring ended *The switch
  ladder keeps every verdict it has; only its ONE silent exit falls through to
  here*. That was false before this work: since round 2 of work item
  1788817291 the creation is also judged from both choice rows' `ask`
  (`before_ask`) and above the tracked-changes row. Corrected with the walk
  sentence beside it.
- The module docstring of `hooks/worktree-guard.py` mirrors
  `docs/worktree-guard-spec.md` §A and §B. It gained the same pointer §A
  gained, so the two stay copies of each other.

**Copy 6 moves to phase 4.** `seal/releases/0.15.5.md` A4 is a ledger row
whose anchor this phase drifted. Phase 4 re-reads every drifted row in one
pass, which is the implement skill's *draft as you go, write in one pass*, so
it is re-stamped there with the others rather than here.

**Where `Enforced by:` went.** §*Creation consent* is one folded statement and
`fold-check` allows it one `Enforced by:` line, so S1, S2 and S3 were appended
to the existing line rather than given a new one.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The present-tense claims that the walk classifies the first segment (four copies) | past tense in the same places, plus the #620 paragraph in `docs/worktree-guard-spec.md` §*Creation consent* |
| `judge_creation`'s *only its ONE silent exit falls through to here* | its corrected sentence in the same docstring |
