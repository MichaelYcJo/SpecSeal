# 1789081272-the-writer-of-the-contract-is-not-its-executor — survivor exemptions

## Phase 2 — the move out of the design gate

`survivor-check --range 02c5b90..5571996` examines 843 files against the
seventeen sentences the range removed and reports one place. It is a
coincidence of ordinary Python, scoring 1.89 on three shared phrases — two of
them the same fragment counted twice — and it is not a copy of anything this
phase corrected.

The removal that produced it is `test_the_design_gate_belongs_to_the_smith`,
whose body opened `agents/smith.md` and looped `for name in
("confidence-check", "feature-planner")`. What the check found standing is a
different loop over a different directory, in a module about the root
migration.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_root_migrates_itself.py` | `for name in sorted(os.listdir(os.path.join(ROOT, "hooks"))):` | **About which hooks still read `.specseal/`**, which is S15 of another work item and has nothing to do with who calls the two utility skills. The shared phrases the check names are `8 read assert` — the `encoding="utf-8"` read followed by an assertion, twice — and `for name in`, which is every walk over a sorted list of file names. The claim this phase corrected was *the design gate belongs to the smith*; nothing resembling it appears in this file |

**What would make this exemption stop holding.** The quote is the anchor. If
that loop ever comes to read `agents/*.md` or to assert which agent calls a
skill, it is the same subject and the report is a finding rather than a
coincidence.

The exemption is anchored on this range as well as on this quote. A different
range re-runs the check from scratch, and a row written for
`02c5b90..5571996` does not answer for it.

**Over the phase's whole range the report is gone, and the row is kept
anyway.** `survivor-check --range 02c5b90..dfe9d6f` examines 844 files against
twenty-four removed sentences and reports nothing standing: the phase's later
commits changed what the range removed, and the 1.89 that put this pairing
over the floor did not survive the recount. The row stays because it records a
judgment somebody made and can check — deleting it would leave the phase
record naming a survivor with nothing behind it — and because it costs
nothing: an exemption that matches no candidate silences nothing.

## Phase 3 — the report splits on who can answer the row

`survivor-check --range fe823dc..de0291b` examines 845 files against the five
sentences the range removed and reports one place. The report is correct and
the standing text is correct too, which is the whole of this row: the sentence
survives in a cell whose job is to record what the default WAS.

The removal is `agents/framer.md`'s old report rule — *the path and the count,
never the rows' text*, resting on §5. Q2 of this work item's own
`questions.md` proposed that rule as its default, and the owner refined it on
2026-09-11. Q1 is the precedent for what happens next: the `Default until
answered` cell keeps the default it stood on, and the `Status` cell records
the answer against it.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/questions.md` | "It is the shape agents/sealer.md's report already has, and §5 says an aggregate is not a coordinate" | **It is the Default column of the row that was answered**, and this file's shape requires it to stand: a row whose default is edited to match its answer no longer records that an answer was given against anything. Q1 above it does the same thing with the same two cells. The live claim — what a framer actually reports — moved with the removal, and `agents/framer.md` carries it in the answered form |

**What would make this exemption stop holding.** The quote is the anchor, and
it is quoted from the Default cell. If that sentence ever appears anywhere it
is read as a live instruction — the `Status` cell, the framer's definition,
the template — it is a survivor rather than a record, and the report is a
finding.

Anchored on this range as well as on this quote, the same way the phase 2 row
is. A different range re-runs the check from scratch and this row does not
answer for it.

**Over the phase's whole range it is the same one place.**
`survivor-check --range fe823dc..fe7430a` examines 846 files against nine
removed sentences and reports this row and nothing else. Recorded because the
range-anchoring above is a statement about what this row is FOR, not about
what the checker enforces: a `| Path | Quote | Grounds |` row is matched on
its path and its quote, and only a `| Range | Grounds |` row is scoped to a
range by the checker itself.
