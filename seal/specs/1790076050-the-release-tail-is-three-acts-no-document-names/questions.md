# the release tail is three acts no document names — questions for the planner

<!-- seal/specs/1790076050-the-release-tail-is-three-acts-no-document-names/questions.md
     Decisions only a human can make, extracted so nothing ships on a silent
     assumption. -->

**This run is `automation`: nobody will be asked anything.** So the default
below is what ships, and the row exists to record that a person can overturn
it later, not to hold the work up.

## What the tickets left open and the tree answered

These were genuinely open and are not rows, because they were settled by
reading or by measuring. `spec.md` §*Judgments this frame made* holds each
one with its grounds; this list is so nobody reopens them looking for a
question.

- Whether #386 takes a checklist line, a workflow, or a refusing check —
  the workflow, and the trigger is the tag push rather than the push to
  `main`.
- Where a release note's title comes from — the tagged commit's `release:
  X.Y.Z — <symptoms>` line, which `docs/release-checklist.md` §5 prescribes.
  **Measured, and #386's own sentence about this is wrong**: the merge
  commit's *subject* is GitHub's `Merge pull request #N from …` line and the
  title line is in the body; and the twenty-three hand-written release names
  reproduce neither the pull request titles nor the changelog headings.
- Whether this plugin is listed in the directory today — **measured
  2026-09-22: it is in neither file.** Official carries 310 entries, the
  community mirror 2,282, and no entry matches. An external entry pins
  `source.url` plus `source.sha` — **which `phases/phase-3.md` measured false
  the same afternoon and this line kept until round 1's fix pass.** 52 of
  official's 310 entries carry `source` as a plain string with no url and no
  sha at all, and 3 community entries carry a url and a ref and no sha. The
  shape holds for the external majority and is not one a reader may assume.
- Whether #450's repair is a tracker row or a machine — a machine, with the
  precedent one file over.
- Whether the open backlog gets a `size: now` sweep — no, on the section's
  own argument.
- Who removes a spent `size: now`, and when — the workflow that closes the
  issue, at the moment it closes it.
- The label's colour and description — the document's own sentence and the
  topic labels' colour family. Nothing turns on either, so it is an
  assumption written down rather than a question.

## The rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Once a plugin is listed in the directory, does an update reach it automatically from the source repository, or must something be resubmitted through the portal? | **a person** — the repository owner, who made the submission. It is not readable from anywhere public: neither directory's README says, the community mirror is read-only and syncs from a pipeline nobody outside can see, and the answer lives behind the submission form | **automatic** — the checklist box becomes a confirmation that the pinned commit caught up, checked at the next release rather than acted on · **resubmission** — the box names the portal and the act, and a stale pin is work rather than a wait | **The box works under either answer and ships as written**: it reports the pinned commit against the released one and says to resubmit through the portal when it is stale. An automatic sync makes that instruction unnecessary, never wrong | ⬜ |

**Why Q1 survived the judging.** Everything else in these three tickets was
answerable from the tree or by a measurement, and was. This one is a fact
about somebody else's system, stated nowhere public, and no probe reaches it —
the two directory files say what is listed and not how a listing is refreshed.
It is recorded rather than waited on because the two answers do not produce
different code: the command reports the same three facts either way, and only
one sentence of the checklist box would read differently.

**Nothing here blocks the build.** No row of this file has to be answered
before phase 1 starts, and none of them changes what any phase builds.
