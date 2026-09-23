# 1790138190-settle-leaves-twelve-directories-with-no-way-out — overview

<!-- The closing memo (implement skill, step 4). Only what the diff cannot
show goes here, and each part is written when it happens. -->

📋 implement applied
· spec:     `spec.md` G1–G8, S1–S8, O1–O9, A1–A13 and §*Which of D1's two answers*; `plan.md` phases 1–7 and §*Alternatives*; `questions.md` Q1–Q6 and its settled list; #517's two owner comments; #511's body; `docs/the-evidence-ledger.md` §*The fold, and what tells it from a deletion*; `skills/settle/SKILL.md` whole; `docs/review-chain-spec.md` §*The declaration, and where the check went instead* and §*Two records, and what each of them says*; `docs/release-checklist.md` §2b; `docs/one-root-by-lifetime.md` and `.ko.md` §*Decided when `settle` was built*; `CLAUDE.md` §*A row whose anchor a change removes is REMOVED*
· evidence: `seal/ledger/1790138190-settle-leaves-twelve-directories-with-no-way-out.md` — thirteen rows (G4, G3 ×2, D3 ×2, S3, G5 ×4, G7, G8, D1); `seal/ledger.md` — the #33 row REMOVED, two rows corrected (S4 of `1790027178`, the retired-declaration row of `1790076070`), and the rows on every unit this branch edited re-read and re-verified, each named in its phase record
· verified: executed — each phase's slice, every new case seen red first, mutations over every unit added, A9 and A10 on scratch clones, and phase 7's four closing commands (`phases/phase-7.md`); read — the spec chain, the three CI readers' arms, the G8 floors; unverified — the rows below

## Why this work exists

After two folds `settle` reported nothing left to fold while `seal/specs/`
still held twelve released directories; this gives each kind of directory a
way out and makes an empty `seal/specs/` a green state.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Phase 3's report headings | `plan.md` phase 3: *`./bin/settle` on this branch lists the ten released spec-less directories under the new heading with `1788177600` and `1788395377` named as kept* / the report prints two headings, *retired by the rule* (eight) and *kept by the rule* (two, with their four rows) | the two headings | the plan's own sentence already separates the two as listed and kept; one heading holding both would print a directory `--retire` removes beside one it refuses, which is the confusion `survey`'s docstring records round 1 fixing for the marker arm (*skipped and named* rather than *waiting to be retired*) |
| A10's reader expectation | `spec.md` A10: *a scratch clone with every directory under `seal/specs/` removed and committed · When … `unverified_check.py --baseline <parent> seal/specs/` … run · Then each exits 0* / against that removal's own parent all three CI readers exit 1, at `3103415` and at `be1579e` alike, because the removal takes four directories the rule cannot retire (three hold a `spec.md` with no marker, one has open rows) | the readers' refusal; the settled state is measured on *the next pull request*, based on the emptied commit, where every reader exits 0 | a hand removal of directories that state a rule or hold an open row is the deletion G5's readers exist to refuse, and G6 accepts only what `settle --retire` removes. The spec's own A15 already reads the fold's pull request as a retirement *at the fold's merge-base*, which a probe cannot build without first folding the three specs (O3) |
| Where the evidence-todo rule lives | `plan.md` names only the predicate as landing in `unverified_check.py` / the rule `settle.py#open_rows` held moved there too, as `todo_open_rows`, and `settle` delegates | moved | the predicate reads `evidence-todo.md`, and a second copy of the rule is the drift `plan.md` §*What breaks in six months* is written against |
| What the #511 guard reads | `spec.md` G3: the guard reads through `unverified_check.py#live_lines` / round 1's finding 1 measured `evidence_check.py#check_text` reading every line of three addresses, so a fenced row's directory was removed and then reported BROKEN | every line of every ledger `evidence_check.py#default_patterns` names | G3's purpose is that no retirement leaves a row BROKEN, and the checker decides what BROKEN is; `live_lines`' bias toward *not live* keeps a directory for the marker reader and removed one here |
| One pull request or two for the post-release fold | `spec.md` A14: *the seven memo rows closed or re-homed · When `settle` and then `settle --retire` run* on one branch / round 1's finding 2 measured both CI readers refusing that removal at the merge base, where the rows are still open | the closures merge in a pull request of their own, before the one that retires | the CI readers ask the rule of the merge base by design (`retired_by_rule`'s docstring), and a closure merged first also keeps its ✅ in the release branch's history, where a squash of close-and-remove would leave nothing |
| An approved plan's cell names a case that no longer exists | `plan.md` phase 6 names `test_the_skill_carries_the_survivors_row_a_fold_branch_owes` / `evidence-check --strict` refuses a record naming something the tree lacks | the line carries `NAME NOT IN TREE` rather than being rewritten | the plan is the approved contract, and the checker's own token is the sanctioned way for a record to name what the tree no longer has |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck on this branch — only the phases' narrow slices ran here, and a coverage probe of the 44 modules naming `seal/specs` on an emptied clone | the `sealer`, in its single run after the review rounds settle (`agent-contract` §2) |
| The new cases on Windows — the guard, the predicate and the readers are path arithmetic over `/`-joined paths, and nothing here ran on the Windows leg | `.github/workflows/test.yml`'s Windows leg, at this branch's pull request |
| A14 and A15: the post-release fold reaching an empty `seal/specs/` with the suite, `evidence-check --strict` and the pull request's CI green, no `survivors.md` and no `routing.md` in it | the repository owner, who runs that fold after the release that ships this |
| `chain_check.py`'s rule arm under a real `pull_request` event payload — every run here was local, judged as a ready pull request with no payload | the CI run on this branch's pull request, and then on the fold's |

## Not done

Deliberately left, per `spec.md` §*Out*: nothing is retired on this branch
(O2) — the eight clean spec-less directories wait for the post-release
fold, and so do the three specs to fold and the seven open memo rows G1
names (O3); the prose citations of `1788184145`'s `rounds/round-3.md` stay
until the fold that removes it, which `settle`'s new citation listing hands
them to (O4); the fold's route (O1, `questions.md` Q1); #518 and #519 (O7).
No floor literal was lowered (O8).

**One finding outside scope, left for the repository owner to file as an
issue** (this agent posts nothing): a committed `survivors.md` silences the
survivors it quotes by subtraction rather than by exemption. Over this
branch's range the sweep reported fifteen places before `survivors.md` was
committed and seven after, with `--exempt` and without it, because
`survivor_check.py#wanted` subtracts the quotes as wording the range wrote —
#365's shape through `survivors.md` rather than `rounds/`. Closing it is new
mechanism in the sweep, which a branch framed for `settle` does not carry
(`phases/phase-7.md`).

## Fed back into the spec

Inferred during implementation — planners may overturn each:

- **A reader's retirement is the whole directory.** Each CI reader asks the
  predicate only when the directory is gone at `HEAD` (or at the range's
  right end); a memo, a declaration or an edited file removed from a
  spec-less directory that stays is still a deletion. `spec.md` did not say
  which, and the conservative reading blocks more (G6's cheaper direction).
- **An unreadable `## Not verified` section counts as open** for the rule
  arm, and the directory is kept naming it, by the rule `check_text` is
  written to: a count that cannot be read is not a count of nothing.
- **The survivor sweep can never report a verbatim copy.** A run scores at
  most 1.0 against the 1.6 floor, so a survivor is a restatement; the
  fixtures here are built that way, and a fold's standing prose is that
  shape by design.
- **"Wrote no `spec.md`" is asked of history** (`wrote_a_spec`, round 1's
  finding 3): any commit reachable from the ref that touched the directory's
  `spec.md` makes it a directory that stated a rule, so a spec deleted by an
  earlier merged pull request needs a fold's marker. A shallow clone cut
  short of the deletion reads as before; the CI checkout fetches everything.
- **`tree_at` is public on `unverified_check.py`** so the survivor sweep can
  ask whether a directory is gone without a new path-listing call site of its
  own.
