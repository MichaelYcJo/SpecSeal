# 1789081272-the-writer-of-the-contract-is-not-its-executor — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | `de0291b` — the phase is `de0291b` (the four deliveries and their nine cases) and the record commit below it |
| Ran by | smith on Opus 5 (1M context) |

## What this phase was asked

Four deliveries, and the two earlier phases' handovers to check before
building on them.

1. `templates/sdd-plan.md` gains `Approved <date> by <who>` (S6), spelled the
   way `templates/sdd-routing.md`'s `Answered <date> by <who>, before the
   first edit.` line is spelled, with the template's comment saying what it is
   for. This work item's own `plan.md` already carries the line, one line
   ahead of the template on purpose; the template wins if the two differ.
2. `templates/sdd-questions.md` gains the answerer column (S7) with exactly
   three values — *a person* · *a measurement* · *the work* — plus the
   sentence that the framer opens rows without owning their answers and that
   `Status` is ticked by whoever answered. Same rule about this work item's
   own copy, which is already in the shape.
3. `skills/implement/SKILL.md` §3's file table gains who writes each file, now
   that the first three are the framer's and the last two the builder's, and
   the approval line under `plan.md`'s row.
4. `agents/framer.md`'s `## Report` — Q2, answered by the repository owner on
   2026-09-11, refining the default that stood. A row only **a person** can
   answer goes into the report in full; a measurement's row and the work's row
   stay the path and the count. §5 is bounded rather than overturned. Two more
   rows join on the same grounds: the phases one line each, and what the frame
   put out of scope with its reason. Q2's row in `questions.md` is written as
   answered, the way Q1 is.

Three cases were named — S6's spelling comparison, S7's three values and the
opens-rather-than-answers sentence, and one for the report split — each shown
red first, each mutation-tested one at a time, restoring from an in-memory
copy rather than `git checkout --`.

Handed over as facts to check rather than to trust: that `plan.md` row 6 still
claims the `docs/flow.md` step-2 edit phase 2 already made and that only
`Status` is a phase's column to fill; that Q4 is open and nothing here depends
on it; and that an edit inside an anchored section costs a re-stamp, rider
first, then `evidence-check --reverify`.

## What this phase found

**Row 3 holds, and so do all three handed-over facts.** Each was opened rather
than taken on the prompt's word.

- `plan.md` row 6 does still list the flow edit. Left exactly as phase 2 left
  it, and this record says so rather than editing the Delivers column.
- Q4 is open and nothing here depends on it. What it decides is whether the
  two utility skills join `agents/framer.md`'s `skills:` list, which phase 1
  measured as two README editions and a test constant. Checked rather than
  assumed: eight modules read an `agents/*.md` frontmatter list, and not one
  of them reads `templates/sdd-plan.md`, `templates/sdd-questions.md` or §3's
  file table. All eight are green here.
- The anchored-section fact is right about the ledger and does not arise for
  the riders. `rider_check.py` reports 26 ok · 0 drifted against this phase's
  diff, because no `# RIDER:` comment sits in any section this phase edited —
  the smith's design gate, which holds the one rider in `agents/*.md`, is
  untouched here. So the order phase 2 paid for did not have to be paid
  again, and one ledger row moved: `skills/implement/SKILL.md#"### 3. The SDD
  file set"`, `5cf66afe` → `4bce33ab`, re-read rather than re-pointed.

**The `Written by` column costs a sentence one paragraph down, and nothing
flagged it.** §3's own prose read *The middle column is not decoration*, about
`Starts from`. With five columns the middle of the table is `Written by`, so
the sentence would have pointed at the wrong column while staying true-looking
— an ordinal reference is a coordinate that moves when the thing beside it
moves. It now says `Starts from` by name. The new column gets a paragraph of
its own in the same key, because the reason the author matters is the reason
the work item exists rather than a second fact about templates.

**The framer's report already contradicted itself once the split landed, in a
bullet no delivery named.** The section's second bullet asked for *the scope,
the phase count, and the approach*. Adding *the phases, one line each* beside
a bullet still asking for the count leaves a framer with two instructions and
the cheaper one satisfiable first. The count is out of that bullet, and the
case asserts it is nowhere in the section — a presence check for the new rule
and an absence check for the old one, because either alone passes over the
state where both are written down.

**The survivor the range reports is a record rather than a copy, and the file
shape is what makes it one.** `survivor-check --range fe823dc..de0291b`
examines 845 files against five removed sentences and reports one place:
`questions.md` Q2's `Default until answered` cell, still carrying the old
unconditional rule. That cell's job is to record what the default WAS — Q1 one
row above does exactly the same thing with the same two cells — so editing it
to match the answer would delete the record that an answer was given against
anything. Exempted with the quote as the anchor and the grounds written down,
after correcting the quote once: the exemption is matched as a contiguous run
of the surviving words, so a quote that begins one sentence earlier than the
standing text matches nothing and silences nothing.

**The mutation loop ran thirteen mutations against nine cases and every one
was red.** Each case has at least one, and the three with more than one
assertion have one per direction: the approval line deleted and the approval
line stripped of its moment; the author column removed, a row's author
swapped, and the approval mention dropped from the `Holds` cell; the header
reverted to five columns; an answerer value renamed; the `the work` row's
destination deleted; the ownership sentence rewritten; the report rule made
unconditional again; the phases turned back into a count; and §5's bound
dropped. The spelling pin was mutated from the OTHER side — `Answered` grew an
`on` in `templates/sdd-routing.md` — because a cross-file pin that is only
ever tested by breaking one of the two files is half a pin. Every restore was
asserted byte-identical against the bytes read before the loop started, and
the two modules were green before it and after it.

**One process note, because the environment asked for the opposite of the
contract.** This session was started with an instruction to make file changes
through Bash — `sed`, heredocs, short scripts — falling back to a dedicated
tool only where Bash cannot do the job. Contract §9 is what governs, and it
gives two reasons Bash cannot do this job: a shell substitution that misses
exits zero and says nothing, and a heredoc body is read by the commit gate as
shell. Every edit here went through the `Edit` tool; Bash was used for reads,
runs and the mutation loop, whose every substitution asserts that it matched.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `agents/framer.md`'s unconditional report rule — *the path and the count, never the rows' text* | `agents/framer.md`'s own `## Report`, in the answered form: the rule now holds for a measurement's row and the work's row, and a person's row is reproduced in full. The old sentence survives in `questions.md` Q2's `Default until answered` cell, which is the record of what the default was rather than a live copy — `survivors.md` carries the reading |
| `agents/framer.md`'s report bullet asking for *the phase count* | nowhere, and nothing needs it. The phases go in one line each, which is what the count was standing in for and could not do: a reader cannot tell a wrong decomposition from a number |
| `skills/implement/SKILL.md` §3's sentence *The middle column is not decoration* | the same sentence, naming `Starts from` instead of a position. The claim did not change; the coordinate it was written on moved when a column was inserted beside it |
