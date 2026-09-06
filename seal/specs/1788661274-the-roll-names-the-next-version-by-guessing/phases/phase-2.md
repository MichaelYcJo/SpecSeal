# 1788661274-the-roll-names-the-next-version-by-guessing — phase 2

<!-- seal/specs/1788661274-the-roll-names-the-next-version-by-guessing/phases/phase-2.md -->

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | `7d25e28` |
| Ran by | |

## What this phase was asked

Carry phase 1's convention to the two documents a person reads, verifying
each sentence against the file first — a sentence that is already right is
not to be touched.

1. `skills/verify/SKILL.md` §*Measure the segment, and feed the flow log*:
   correct *"accumulates for one version and is discarded when that version
   ships"*, which describes the wrong boundary now. **Nothing
   repository-specific**, because `seal/ledger.md`'s F5 row binds this file —
   the shipped skill may name `flow-measurement` and `flow-baseline` and no
   tracker state that exists here alone. So the title format does not go
   here.
2. `docs/issues-and-milestones.md` §*`flow-measurement` is a label that is
   not an index*: add the missing condition to *"closes the current one and
   opens the next when a release reaches `main`"* — a push to `main`, and
   only where a new version has shipped. And carry the title format here,
   since the skill may not have it: what a title means now, and what the
   older ones mean, since closed logs are not retitled.
3. Read the script's module docstring, already rewritten by phase 1, before
   writing either document, so the three say one thing rather than three.

Bounded to those two documents and the cases that pin them. #172 and #51 are
GitHub state and are not this branch's to touch, and `plan.md` §Alternatives
is settled — the verdicts are read, not re-opened.

## What this phase found

**One of the two sentences was wrong and the other was incomplete, and the
difference decided where each edit went.** The skill's sentence stated a
boundary that no longer exists: under phase 1's convention the version a log
is named after has already shipped when the log opens, so *discarded when
that version ships* points a reader at an end that has already passed. The
tracker document's sentence was not false — the roll does close the current
log and open the next when a release reaches `main` — it just never said
that a push which shipped nothing does neither. So the skill needed its
sentence replaced and the document needed a clause added, and the case for
each is shaped accordingly: the skill's case refuses the old phrase by name,
the document's case refuses the old *unconditional* form and requires both
the trigger and the condition.

**The wrap and the marker are what keep the two ends of the skill's sentence
from being one.** `test_the_section_says_what_separates_the_two_logs`
already asserted the word `discarded`, so the replacement had to keep it —
it does, and the new case adds the two ends it was missing (`opens at a
release`, `until the next version ships`). Both cases read
`section_body()`, which collapses whitespace, so neither breaks when the
paragraph re-wraps.

**The document's cases read the script's constant rather than a literal, and
that is the drift this phase was actually guarding against.**
`test_the_tracker_doc_states_the_title_the_roll_writes` asserts
`TITLE_MARKER` appears in the section, and then feeds every backticked
`chore: …` example in the section through `rolled_from`, requiring at least
one the script can read back. An example the roll would answer `None` for is
an older-convention title being held up as the current one, which is the
confusion the section exists to end — and it is what a well-meaning edit
produces, since the older form is what the tracker still shows.

**Nothing in the skill turned out to need the class-mate edits.** Two
neighbouring sentences say *one of them is deleted at every release* and
*schedules it for deletion at the next release*, and both are still true:
every release ships a new version, so every release rolls. The class the
grep enumerated — the boundary stated as one version's life — has exactly
one member in shipped prose, and one more in `phases/phase-1.md`, which is a
record quoting the sentence it asked phase 2 to fix and stays as written.

**One sentence I wrote had to be taken back out before it shipped.** The
document's new clause first read *"the workflow fires on every push to the
default branch, so most of those pushes roll nothing and say so"*. That is
an aggregate nobody has measured, and it is probably false here: the
repository's own rule sends nothing to `main` except a release merge, so
most pushes to `main` do roll. It now names the two cases that genuinely
roll nothing — a re-run of the job, and a merge that shipped nothing —
which is what the workflow trigger actually implies.

**What phase 3 has to carry.** The closing set: a ledger fragment (nothing
from phase 1 or phase 2 has reached the ledger yet — the condition, the
direction of the unreadable title, the writer/reader constant, and now the
two documents that state the convention to a reader); a changelog fragment;
`overview.md`, whose §Where spec and implementation diverged is
`phases/phase-1.md`'s `spec.md` divergence with both texts, and whose §Not
verified must carry the suite as `unverified` with the orchestrator as its
answerer; and `docs/flow.md`'s #155 box. F5's own row in `seal/ledger.md`
carries a `Checked` date and a re-read history: this phase re-read that
section and left the absence intact, which is a re-verification phase 3
should record rather than a new row.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The skill's *"accumulates for one version and is discarded when that version ships"* | Replaced in place by the two ends that are true now, and pinned by `test_the_rolling_logs_life_is_bounded_by_two_releases`, which refuses the old phrase by name |
| The tracker document's *"opens the next when a release reaches `main`"*, as an unconditional statement | Replaced in place by the trigger and the condition together, and pinned by `test_the_tracker_doc_states_the_condition_the_roll_carries`, which refuses the unconditional form by name |
