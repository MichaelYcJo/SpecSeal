# 1790208643-the-spec-is-split-and-its-sentences-are-settled — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | recorded in `plan.md`'s Status cell for phase 3 — this file is part of that commit |
| Ran by | smith on Opus 5.5 |

## What this phase was asked

Resumed after #558 (D), #560 (F) and #559 (an outside contribution) squashed
and the orchestrator merged `release/v0.15.1` (`06f10aaa`) in at `4a077852`.
First: re-read the nine rows the merge drifted, with dated notes, and check
every merged row reads as one sentence after another. Take #222 out of this
item as work done here, because #559 closed it and the orchestrator removed
this item's paragraph. Finish phase 0's D half. Then phase 3 as the plan
states it, into D's text: #488 and #509 in `docs/the-evidence-ledger.md`
first, then `CONTRIBUTING.md`, then the checklist's squash step, with
`CONFLICT_SENTENCES` needles seen red with a needle removed. **`CLAUDE.md` is
not edited here.** The exact sentences it needs are below, for the
orchestrator to paste.

## What this phase found

**The merge's nine drifts** (executed, `evidence-check --strict .` at
`4a077852`: exit 2, `9 drifted`). Each one is a unit both sides edited:

- the floor section: #558 put its aside in the past tense;
- `round_record.py#depth_two`, in two files: #559's paragraph;
- `skills/code-review/orchestration.md`, both headings, and
  `agents/warden.md` §*Role*, in two files: #558 widened the paperwork
  sentence to `seal/releases/`;
- the `### 1788331011` section of `seal/ledger.md`: both sides' notes;
- `tests/test_a_record_precedes_the_fixes_it_commissions.py#test_the_declared_limit_names_what_escapes_with_the_words_unchanged`:
  #558 reads `seal/releases/` too.

Each row is re-read and noted *Re-read 2026-09-24 at the merge of
`release/v0.15.1` (#558, #559) into #526's branch, at `4a077852`: …*, with
what each side did. `--reverify` re-stamped 11 rows; then `--strict` exit 0,
`1831 ok` (`75b226a7`). Four sentences a merged row ran together, all in the
row anchored on the `### 1788331011` section, are separated with a period.
The other unpunctuated joins in the resolved hunks predate the merge.

**#222 withdrawn** (read). The four notes this branch wrote on `depth_two`
rows named *#222's paragraph*. They now say the paragraph is #559's, which
closed #222, and that this branch's was withdrawn at the merge. `spec.md`
§*Scope*'s #222 row, S15, the fragment list, `plan.md`'s phase-4 row and
`phases/phase-4.md` all say so. `changelog.md` never had a #222 entry, so
nothing is dropped there.

**Phase 0's D half** (read, `git diff 0eda669f 4a077852` over the documents
phase 0 named).

- D gives each release its own file, `seal/releases/<X.Y.Z>.md`. It keeps
  `seal/ledger.md` for the notation and the pre-fragment rows, and moves the
  sections folded into it before #547 exactly once, with `fold_ledger.py
  --split` at the 0.15.1 release.
- `seal/releases/` does not exist yet. So every row this item re-points or
  re-stamps is in `seal/ledger.md` or a fragment today, and the split carries
  it byte for byte.
- In the three carriers, D rewrote *seal/ledger.md* as *a ledger file*, and
  the conflict rule as *a ledger file — `seal/ledger.md`, a
  `seal/releases/<X.Y.Z>.md`, or a fragment*. D also added the
  `--split` step to the checklist's §2 and the three split readings to §3.
- **D did not write the removal-or-edit exception or the halves**, so #488
  and #509 are still owed. The frame's choice to say *the file the row is in*
  and no path holds against D's layout: the row may now be in any of three
  files.

**#488** (written). The owner, `docs/the-evidence-ledger.md` §*A row is a
content anchor*, now reads *Appended is the word, and a removal is not one —
nor is an edit*. It covers a branch that *removes or edits* cited code, says
the row is re-read and re-stamped in the file it is in, and says both are
*keeping an existing claim true, which is not appending*.
`CONTRIBUTING.md` §*House rules* already listed the two answers, and the
first one is the drift-by-edit case. It gains the sentence that both answers
are writes to the file the row is in and neither is an append. So the
*third arm* the frame asked for is a clause saying the existing two are the
exception, not a third bullet. The `seal/follow-up.md` row (Q3) is untouched.

**#509** (written). *Hunk by hunk has two halves, and only the notes are a
union* goes into the owner's §*A correction a merge dropped* and into
`CONTRIBUTING.md` beside its conflict paragraphs. The checklist's squash step
(W3's default, §0) gains one linking sentence naming the owner, because the
merge that bullet permits is where a session meets the conflict.
`CONTRIBUTING.md`'s pointer reads *carries both paragraphs and the halves
rule*, which keeps the pinned phrase.

**The pins, seen red** (executed). `CONFLICT_SENTENCES` gains four needles:
*removes or edits code an existing*, *keeping an existing claim true*, *the
side that edited the anchored unit*, and *run `evidence-check` after the
resolution*. A new case, `test_the_policy_document_owns_the_exception_and_the_halves`,
reads the four in the owner and the checklist's link.

- A probe removed each of the four from the owner, restoring from kept bytes
  and checking sha256. The case was exit 1 each time (`1 failed`) and exit 0
  after the restore.
- `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` is **red on
  purpose until the orchestrator pastes the text below**:
  `CLAUDE.md does not say: removes or edits code an existing`.
- A probe applied the paste to a scratch copy of `CLAUDE.md`, not this tree.
  All 10 needles are present, the pointer sentence is present, and the
  module name is present, so the case goes green with the paste.

Module runs: the correction, contributor, line-wrap and ceiling modules gave
`1 failed, 121 passed`, the one failure being that `CLAUDE.md` case.
`.github/scripts/claude_block.py --check` exit 0. Rows on
`CONTRIBUTING.md` §*House rules* (C8, and D's D1), on the checklist's §0
(S9), and on the owner's §*A row is a content anchor* were re-read and
noted. `--reverify` re-stamped 4 rows, then `--strict` exit 0, `1831 ok`.

**What `CLAUDE.md` needs — paste-ready, two replacements** in §*Repo rule — a
change writes fragments, never the shared file*. Each old text occurs once.

Replacement A — replace

```
**Appended is the word, and a removal is not one.** A branch that removes code
an existing ledger row cites — in `seal/ledger.md` or a
`seal/releases/<X.Y.Z>.md` — must touch that file to leave the ledger true:
the row is removed there, and the new claim is written into the branch's own
fragment. `CONTRIBUTING.md` carries the same sentence, and the two
```

with

```
**Appended is the word, and a removal is not one — nor is an edit.** A branch
that removes or edits code an existing ledger row cites — in `seal/ledger.md`
or a `seal/releases/<X.Y.Z>.md` — must touch the file the row is in to leave
the ledger true. A removal takes the row out there and writes the new claim
into the branch's own fragment; an edit drifts the row, which is re-read
against that edit and re-stamped there with a dated note. Both are keeping an
existing claim true, which is not appending. `CONTRIBUTING.md` carries the
same sentence, and the two
```

Replacement B — replace

```
cannot prevent it.

`CONTRIBUTING.md` carries both paragraphs, and
```

with

```
cannot prevent it.

**Hunk by hunk has two halves, and only the notes are a union.** A row's
`Re-read` and `Corrected` notes are both sides', because each records a
reading somebody performed; the anchor's hash belongs to exactly one side, the
side that edited the anchored unit. `correction-check` cannot see a union that
kept the other side's hash, because no marker was dropped, so run
`evidence-check` after the resolution: a drifted anchor is the tool naming
which side that was. `docs/the-evidence-ledger.md` §*A correction a merge
dropped* owns the rule.

`CONTRIBUTING.md` carries both paragraphs and the halves rule, and
```

After the paste, the row C8 anchored on that `CLAUDE.md` section drifts and is
re-read with `evidence-check --reverify .`; the claim (*both say what to do
when the shared ledger conflicts, held against each other*) holds.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| this item's #222 paragraph in `depth_two` (removed by the orchestrator at `4a077852`) | #559's paragraph, in the same docstring |
| *a removal is not one* as the whole exception, in the owner | the same paragraph, widened to an edit |
