# a round record disarms survivor-check — questions for the planner

<!-- seal/specs/1789211172-a-round-record-disarms-survivor-check/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does `seal/specs/*/survivors.md` join `rounds/` in the by-construction exclusion, and on which sides? An exemption row quotes the standing text by design, so once the commit adding it is inside the range that quote counts as wording the range wrote and subtracts the survivor the row was written to excuse — the same class as #365 in kind, a different mechanism. The repository reserved this twice: `seal/follow-up.md` holds the added side as its own row and says in as many words that what needs a person is whether the exclusion is right; #361's `rounds/round-3.md:221` records the corpus side as having no row at all | **a person** | **out (the default)** — #365 ships the round-record filter alone. The universal silencing path closes: every review chain posts a round record, so that one fires on every reviewed branch. The exemption path stays open, so a branch that writes a `survivors.md` still silences its own survivor through the diff, and #361's four exemption rows stay unarmed. Plan phase 4 closes as `deferred #N`. · **in** — phase 4 also leaves `seal/specs/*/survivors.md` out of `corrected`'s `paths` and out of `corpus`. Both halves, because #361's round 3 measured the added side alone at `3673e46`: exit 1, five places without `--exempt`; with `--exempt`, three exempted — including `changelog.md:22` printed with its grounds — and **two still reported, both of them `survivors.md`'s own quote cells**, which is the corpus half. Against it: `seal/follow-up.md` notes that a branch may edit prose in the same commit as its exemption file, and that a by-construction exclusion is what this module argues for over lists | **out.** Phases 1, 2, 3 and 5 run either way, so the build does not wait for this. The answer decides only whether phase 4 runs or becomes `deferred #N` | **out** — answered 2026-09-12 by the owner, before the first edit. Phase 4 closes as `deferred #371`, which carries round 3's two-run measurement and the argument against |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. The only kind of row that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument.
- **the work** — unknowable at framing time; the phase that meets it decides
  it there and records a divergence row.

## What was settled without asking, and where

Four things read as questions and are not, because reading the repository
answered them. They are recorded here so the next session does not re-open
them.

- **Which side to filter.** Both, on `paths`. Round 2 of #361 measured the
  `paths` form and the removed-sentence count stayed at 16
  (`seal/specs/1789172128-…/rounds/round-2-report.md:177-181`). A *measurement*
  that was already taken.
- **Whether `--migrate` carries the same asymmetry.** It does not.
  `evidence_check.py`'s `--migrate` resolves ledger coordinates against a
  tree and builds neither a sentence pool nor a removed-wording range, so
  there is no instance of the asymmetry to check. Settled by construction in
  `spec.md` §*The class, enumerated by construction*.
- **Whether `whole_range()`'s range at `:833` should be filtered too.** No.
  It asks whether the range belongs to the work item a declaration was
  written in, and a round record in that directory is evidence of ownership.
  Filtering there would turn a legitimate declaration into `foreign`, which
  the function's own docstring at `:802-807` names as the failure it must not
  have.
- **Whether #361's invalidated records are repaired here.** No — the repair
  already happened in the work item that found it, at `01a0437`, and a round
  record states a past state at its Target SHA. `spec.md` §*Scope*, out-item 4
  carries the coordinates.

Answered rows feed back into `docs/` — a policy clause or an open-questions
section — before this directory's work merges. Q1's answer, either way, is
owed to `seal/follow-up.md`'s `survivors.md` row: *out* leaves it standing and
corrects its stale clause, *in* closes it.
