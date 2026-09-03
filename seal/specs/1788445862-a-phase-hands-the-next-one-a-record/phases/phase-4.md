# 1788445862-a-phase-hands-the-next-one-a-record — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 118af25 |

## What this phase was asked

Build phase 4 only, of the 4-phase table in `plan.md` — the closing phase:
write `seal/specs/1788445862-…/changelog.md`, one fragment entry per
`docs/branch-and-release.md`'s convention, summarizing what #121 and #119
shipped; write `seal/ledger/1788445862-….md`, this work item's own ledger
fragment, using the coordinate notation in `templates/ledger.md` and
`skills/implement/SKILL.md`'s ledger section, writing rows only for claims
actually worth a durable coordinate — `none — <why>` explicitly offered as a
legitimate outcome for a branch this documentation-shaped; close `overview.md`
from `templates/sdd-overview.md` (purpose line, spec/implementation
divergence judged honestly rather than assumed, what was not verified —
including the plugin-cache limitation phase 3 named as a known fact this
branch cannot observe — and what fed back into the spec); run the narrow
verification named in `plan.md`'s Phase 4 row, fresh, reading full output
rather than through a pipe; fill `plan.md`'s Phase 4 Status cell with the
commit that closes it; then write this file. No pull request, no reviewer
spawn — the orchestrator runs the review chain next.

## What this phase found

**The "none — why" option was on the table and was not taken.** This branch
is templates, agent instructions, skill wiring and two test modules — no
hook, no gate, no checker — which is exactly the shape `plan.md`'s Phase 4
row and the spawning prompt both flagged as a legitimate "none" case. Five
rows were written anyway (P1–P5 in the ledger fragment), on the judgment
that two of them are genuinely hard to cheaply re-derive once this
directory stops being actively read: the deliberate `phase-N.md` /
`phase-<N>.md` bracket-vs-bare-form split (P3), which reads as an
inconsistency to fix until the reasoning behind it is opened, and the
constant-vs-constant test pitfall phase 3 caught in itself (P5), a reusable
testing lesson with no other durable home once `phases/phase-3.md` stops
being routinely read. The comparable prior work item
`1788420761-the-settings-live-in-a-file-nobody-opens` — also a skill/template
branch with no gate — set the precedent: five to seven rows (S1–S7), each
grounding a claim its own new test module pins, not a bulk audit. This
branch's five rows follow that shape rather than defaulting to `none` on file
count alone.

**Computing the hashes by hand was not attempted.** Every row was drafted with
a placeholder hash (`00000000`), then `evidence-check --reverify`, scoped to
only this fragment (`--ledger 'seal/ledger/1788445862-….md'` — never the bare
default, which would also re-hash every row of the shared `seal/ledger.md`),
recomputed and wrote the real ones: 16 coordinates, 16 resolved. A follow-up
run of the plain check (no `--reverify`) confirmed `16 ok · 0 drifted · 0
broken` before the fragment was committed — the hash a row carries was
actually read against the file it names, not typed by hand and hoped correct.

**`seal/ledger/` did not exist in this tree before this phase.** Every prior
work item's fragment had already been folded into `seal/ledger.md` and
removed at its release (`0.4.0` through `0.6.0`); this branch is the first to
write into the directory since the last fold, so the directory itself is new
on this branch rather than merely a new file inside an existing one.

**The one real spec/plan divergence worth recording**, written into
`overview.md`'s divergence table rather than left implicit: `plan.md`'s Phase
2 row asked for `phases/phase-N.md` to be "spelled identically across all
four files phase 1 and 2 touch", and the code that shipped does not do that
— it keeps `templates/sdd-phase.md`'s own header bracketed while the other
three stay bare, which phase 2's own record already argued was the right
reading of an undercount in the plan's own wording, not a shortfall against
it. The phase 3 heading-skeleton case and the constant-vs-constant self-catch
are not divergences by the same test: the plan's Phase 3 row already
anticipated the split, and the self-catch is a correction to the test's own
construction, not to what was asked.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | — |

<!-- `seal/follow-up.md` was read in full for this check (also read at
`plan.md`'s own Technical Context, before phase 1). Its one open row — bringing
`agents/smith.md` and `agents/scribe.md` under `tests/test_docs_line_wrap.py`
together — names neither this work item nor anything this phase's diff
touches, and closing this work item does not resolve it or make it doable;
it stays open, for the repository owner, exactly as `plan.md` already
recorded before implementation began. -->
