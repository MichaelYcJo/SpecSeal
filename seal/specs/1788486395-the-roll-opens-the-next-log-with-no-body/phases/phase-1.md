# 1788486395-the-roll-opens-the-next-log-with-no-body — phase 1

<!-- seal/specs/1788486395-the-roll-opens-the-next-log-with-no-body/phases/phase-1.md
— what this phase of the build did, written by the implementer when the phase
closes. -->

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 97f1519 |

## What this phase was asked

Build phase 1 only, of the four-phase table in `plan.md`: the sentence, before
the mechanism. `skills/verify/SKILL.md:312-346`, and three things in it.

1. **Which reading goes where.** A segment's own numbers to the
   `flow-measurement` issue, as today. Anything that compares across versions —
   a rate against a previous version's baseline, an observation that a
   measurement answers — to the `flow-baseline` issue. The distinction is kind,
   not scope: one accumulates and is discarded, the other is maintained.
2. **How a repository declares its durable log**: an issue carrying
   `flow-baseline`. Same lookup shape as the rolling one, and the same
   invariant — exactly one open.
3. **Two zeroes, told apart.** The existing no-op for an absent label is right
   and stays. A repository whose label *has* a history and now has none open is
   the failure `roll_flow_measurement_issue.py`'s docstring names.
   `gh issue list --label flow-measurement --state all` separates them for one
   call. A session names it and does not repair it — two sessions finishing
   segments together would both read zero and both create, and the next release
   fails on two-or-more. Point at the script's docstring for the invariant
   rather than restating it.

Point at `docs/issues-and-milestones.md` for the tracker's own conventions;
do not restate them.

Two existing pins constrain the prose: `test_skill_has_no_html_comments_at_all`
and `test_the_section_states_an_absent_label_is_a_no_op`. All seven existing
cases stay green. The skill ships, so it may name only `flow-measurement` and
`flow-baseline`, and never `#51` or `log: measurement`.

## What this phase found

**A phrase-matching pin is the file's own idiom, and it forces the prose to
carry the phrase rather than the meaning.** Every case in
`tests/test_a_segment_feeds_the_flow_log.py` is a substring check, so a new
case pinning "which reading goes where" has to pick words. The first draft said
*a reading that only means something across versions*, and the case asserting
`span versions` was red against prose that says exactly the right thing. The
prose moved to *Readings that span versions* rather than the case moving to
the prose: a case that is rewritten to match whatever was written pins nothing.
**Phase 2 and 3 inherit the opposite constraint** — the script's cases assert
against `gh` argument lists, where the value under test is the string itself
and there is no such gap.

**The negative constraint needed a mutation, not a revert.**
`test_the_shipped_skill_names_no_repository_specific_tracker_state` is green
the moment it is written, so §15's *seen red first* cannot be shown by
reverting a fix — there is no fix. It was shown by breaking each of the three
things it forbids, one at a time: `log: measurement` inserted into the section
(exit 1), `#51` inserted (exit 1), and a bare `` `measurement` `` inserted
(exit 1). None survived. The probe restored the file from bytes it kept, never
from HEAD, because phase 1 was uncommitted while it ran.

**The pointer at the roll script is a path an installed repository does not
have, and it is named as such in the prose.** `.github/` stays home
(`tests/test_the_release_check_watches_what_ships.py`), so
`.github/scripts/roll_flow_measurement_issue.py` exists in this repository and
nowhere a user installs the plugin. The section carries it as *"where a
repository has one"* rather than as a bare path. Nothing was invented for this:
the same file already points at `docs/review-chain-spec.md` twice, and `docs/`
stays home by the same list. What a reader loses in an installed repository is
a pointer that resolves; what they keep is the sentence that tells them the
invariant is written down somewhere and not being restated here. **This is
worth a reviewer's eye** — the alternative is restating the invariant, which
`plan.md` and `docs/issues-and-milestones.md` both refuse.

**The overview check was red on this branch before the phase started, and this
phase closed it.**
`tests/test_chain_hooks_hardening.py::test_every_spec_directory_that_reached_the_ladder_has_an_overview`
fails for any work item holding `spec.md` or `plan.md` and no `overview.md`.
The sibling work item 1788472135 met the same red and carried it to phase 4;
this one opened the memo instead, which is what the `implement` skill asks for
anyway — the memo is opened at the first unverified item, and phase 1 already
had four.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The sentence *"if the search returns none, this whole section is a no-op"* — a single zero case covering both a repository that never measured and one whose log stopped | The same section, as the first of two bullets under *A reading of zero open is two different facts*. Every phrase `test_the_section_states_an_absent_label_is_a_no_op` reads (`no-op`, `nothing is posted`, `nothing fails`, `nothing asks`) moved with it, and that case is green |
