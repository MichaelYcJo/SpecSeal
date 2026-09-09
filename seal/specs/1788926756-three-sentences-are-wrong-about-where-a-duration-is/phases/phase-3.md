# 1788926756-three-sentences-are-wrong-about-where-a-duration-is — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `80cc7ce` · `62347dc` — the second carries the survivor sweep's own correction, which is this phase's verification step |
| Ran by | specseal:smith on unknown — the spawn prompt named no model, and the template forbids a segment sourcing that value from its own idea of what it is |

## What this phase was asked

The span's own disclosure in `skills/verify/SKILL.md` beside where a reader
meets it, the changelog and ledger fragments, and the ledger rows the edits to
`#analyse` and `#report_spawns` drift — the handoff named six, two at
`#analyse` in `seal/ledger.md` and four at `#report_spawns` in #145's
fragment. Verified by the modules the skill change touches, `evidence-check`,
and §12's survivor sweep over the whole fix range.

## What this phase found

**It is fourteen rows over seven anchors, not six over two.** The handoff
counted #145's fragment correctly and stopped there. What `evidence-check`
actually reported:

| File | Anchors drifted | Rows |
|---|---|---|
| `seal/ledger.md` | `#analyse`, `#report`, `SKILL.md#"## Measure the segment…"` | 7 — `:101`, `:873`, `:1037`, `:1141`, `:1335`, `:1818`, `:1821` |
| `seal/ledger/1788908215-…​.md` | `#analyse`, `#report_spawns`, the same section, `#test_a_call_that_outlives_a_cut…` | 7 — rows 5 to 11 |

Two anchors nobody named do the extra work. `#report` drifted because the
negative-span sentence lives there, and the skill's own section drifted
because the disclosure and item 1's clause are both inside it — and three
`seal/ledger.md` rows cite that section for claims about labels, the
run-level table and the title format, none of which this work item touches.

**Every one of the fourteen claims holds.** Each was re-read against the code
as it stands rather than re-stamped on the strength of the anchor having
moved for a reason I knew about. `--reverify` rewrote 17 stamps, then 5 more
for the section after this phase's own edit to it; the two stale `Checked`
dates (`:101` at 2026-09-01, `:1335` at 2026-09-06) moved with them.
`evidence-check` reads 1041 ok · 0 drifted · 0 broken, exit 0.

**Three sentences in another work item's fragment were corrected in place
rather than left standing beside a correction.** `CLAUDE.md`'s *keep an
existing row true* exception is the grounds, and it is the only reason to
touch a file that belongs to another work item. They said the span reads the
last call to begin, that the difference carries both errors, and that Q5 is
open with the owner as its answerer. The first two are what this work item
changed; the third is what it answers.

**§12's sweep found one real survivor and it was in the answer's own source
page.** #145's `questions.md` Q5 still read *it is not fixed here* and still
gave the grounds phase 2 removed. Leaving that would have left the question
this work item answers contradicting the answer, in the file a reader goes to
for the reasoning. It now opens with the answer, the date and where it landed,
keeps its option table as the thing the answer was chosen against, and records
that its first option's third column named only half of the 101%. The other
two reports are this work item's own spec and questions rows, both still true,
excused in `survivors.md` with a quote as the anchor. Re-run with `--exempt`:
763 files against 85 removed sentences, no removed wording standing, exit 0.

**One defect found and not touched, because it is another work item's row.**
`seal/follow-up.md`'s last schedulable row is about `chain_check.py`'s
unparseable `Broad gate` refusal, and its grounds read *a `# RIDER:` at the
coordinate is refused because four ledger rows anchor at `#report_spawns` and
two at `#analyse`*. Those are `session_cost.py`'s anchors and that row's
coordinate is in `chain_check.py`, so the grounds appear to have been carried
over from #145. It also undercounts: there are four rows at `#analyse` across
the two ledger files, not two. It belongs to work item
`1788912166-…`, whose round 2 wrote it, and correcting another item's
follow-up row on grounds I am inferring needs a person — handed over rather
than edited.

**What the shipped skill was kept clear of.** `seal/ledger.md:873` holds that
the shipped skill names no tracker state existing in this repository alone,
and its case is the only one in its module reading for an absence. The
disclosure cites `#300` once, matching the single issue citation the file
already carries, and names no label, issue title or measurement figure — the
numbers are in the ledger fragment and the changelog, where they belong.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| #145's `questions.md` Q5 as an OPEN question — *it is not fixed here*, and the option table as a live decision | The same section, rewritten to open with the answer and its date. The table is kept rather than deleted, because it is what the answer was chosen against and `overview.md`'s divergence section reads it |
| The clause *the difference there carries this error as well as the rows' overlap*, in Q5 and in #145's ledger fragment row 11 | Both corrected in place to the subinterval grounds. The conclusion — the figure is not the overlap — is unchanged and now rests on something still true |
| The claim that a `# RIDER:` inside `analyse` is what `seal/follow-up.md`'s rule would put there, tied to an unanswered Q5 | #145's fragment row 11, whose note now records that Q5 was answered and by whom. No rider was planted: seven ledger rows anchor inside the two functions, and `questions.md` Q3 plus the module comments hold the facts instead |
| `plan.md`'s phase-3 cell naming *the six ledger rows* | The same cell, corrected to fourteen over seven anchors with the reason the count was low. `phase-3.md`'s table above is the enumeration |
