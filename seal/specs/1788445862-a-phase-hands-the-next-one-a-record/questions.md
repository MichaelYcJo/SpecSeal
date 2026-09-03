# a phase hands the next one a record — questions for the planner

<!-- seal/specs/1788445862-a-phase-hands-the-next-one-a-record/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

| # | Question | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|
| Q1 | Should a segment's record also name which plugin version/commit was in force when the segment ran? (#119's own "needs a second look" add-on 1) | **Build it now** — every `round-N.md`/`phase-N.md` gains a field naming the installed plugin version or commit, widening this branch's scope beyond the two named files-lists in #121/#119. **Defer** — leave it for a follow-up ticket; nothing in this branch reads or writes such a field | Defer | ⬜ deferred — see grounds |
| Q2 | Should `CONTRIBUTING.md` gain a paragraph explaining the plugin-copy-in-force / version-cache confusion? (#119's own "needs a second look" add-on 2) | **Write it now** — adds documentation prose unrelated to either template this branch touches. **Defer** — leave it for a follow-up ticket | Defer | ⬜ deferred — see grounds |

Both rows are deferred, not open: the repository owner already scoped them
out of #119 in the issue body itself — "Both 'needs a second look' add-ons at
the bottom of #119 are OUT OF SCOPE for this branch (not asked to build
now)". They are recorded here rather than silently dropped, per the same
issue's instruction to name them "for a follow-up ticket, with the reasoning
from the issue body (widens scope; is documentation on a records ticket) as
the grounds":

- **Q1's grounds** — naming a plugin version or commit per segment is a
  third kind of field this branch does not otherwise add (the phase and round
  work here is entirely about what a segment was *asked* and what it *found*,
  never about which build of the plugin ran it), and it would touch every
  record-writing site a second time for an unrelated reason. Widens scope.
- **Q2's grounds** — a `CONTRIBUTING.md` paragraph about the
  plugin-copy-in-force confusion is prose explaining a mechanism
  (`docs/experiments/2026-09-03-skill-preload-and-the-copy-in-force.md`
  already exists for that), not a template or skill change a phase/round
  record needs to exist. It is documentation on a records ticket.

Neither blocks this branch: a different answer to either would not change
anything this branch builds, which is the test `skills/implement/SKILL.md`
§1 gives for whether something belongs in this file at all versus being
raised and dropped. `seal/follow-up.md` is not the destination for these
two, because that file's own rule restricts it to items with nowhere else to
go in a repository that has a tracker — this repository does, and issue #119
already names the follow-up.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges. Neither row here needs that: deferring
is not a policy decision, it is a scope boundary already drawn by the issue
that opened this branch.
