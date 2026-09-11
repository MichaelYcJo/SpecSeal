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

## Phase 4 / 4b — the fourth axis, and the mark it leaves

`survivor-check --range e82403f..d950e8b` examines 846 files against the
eighty-five sentences the range removed and reports six places. One was a live
claim of this phase's own and was corrected rather than exempted; the five
below are records, and each records something that was true of a past release
or a past work item.

**What the range removed, and what the five still carry.** The notice used to
speak for one axis, so every sentence describing it said `smith` and `the mark`
in the singular. Phase 4b widened the code and rewrote those sentences in
`README.md`, `docs/review-chain-spec.md` and this work item's own test module.
What the checker then finds standing is the singular wording in places whose
job is to say what shipped at the time — which is the same reading phase 3's
row gives its one place, one level over: the sentence survives where its job is
to record, not to instruct.

The corrected one, for the record rather than as an exemption:
`tests/test_the_implementer_is_recorded.py`'s module docstring still described
the silence as *nothing is said when the mark stands*, which with two axes is a
claim about the wrong grain. It now reads *about an axis whose mark stands*.

| Path | Quote | Grounds |
|---|---|---|
| `CHANGELOG.md` | "a reminder in the `post-bash` group prints one line naming the declaration where it answers `smith`" | **A released section.** It says what 0.7.0 shipped, and 0.7.0 shipped a notice that spoke for one axis. Editing it would make the changelog claim that release did something it did not do, which is the one thing a changelog may not say |
| `seal/specs/1788310269-the-implementer-leaves-a-mark/changelog.md` | "a reminder in the `post-bash` group prints one line naming the declaration where it answers `smith`" | **The fragment the released section above was gathered from**, and a record of the same fact for the same reason. `gather_changelog.py` moves a fragment's text verbatim, so a fragment that disagreed with the section built from it would be a record of nothing |
| `seal/specs/1788310269-the-implementer-leaves-a-mark/spec.md` | "`smith-helper` is there because a substring test would read it as the agent" | **A past work item's frame**, describing the case list as that work item shipped it. The live copy is the test's own docstring, which this phase widened — `framer-helper` sits beside `smith-helper` there now, and the spec of a work item that closed in 0.7.0 does not follow it |
| `seal/ledger.md` | "where the declaration for this branch answers `smith` and no mark stands, one line names `seal/specs/<item>/routing.md`" | **A live ledger claim that is narrower than the code and still true of it.** Every word holds for the axis it names; what it does not state is the `Planning` half, which is this work item's own claim and goes in its fragment rather than being appended here. The row's Notes now carry the 2026-09-11 re-read saying exactly that, so a reader meeting the narrow clause finds the reason beside it |
| `seal/ledger.md` | "Rows for the work item that gave the routing declaration's third axis its reader: a mark written when `smith` is spawned" | **A section heading naming which work item the rows below belong to.** It is a label on a past work item, not a claim about the tree, and the work item it labels is the one that gave the THIRD axis its reader. The fourth axis's rows go under this work item's own heading |

**What would make these exemptions stop holding.** The quote is the anchor in
each. The four records stop being records the moment their sentence is read as
a live instruction — a changelog section rewritten as current behaviour, a past
spec cited as the rule. The ledger row stops holding the moment its clause is
false rather than narrow: if the notice ever stops saying that line for a
declaration answering `smith`, the row is a survivor and the report is a
finding.

Anchored on this range as well as on these quotes, the same way the rows above
are, and with the same caveat phase 3's row records: that anchoring says what
these rows are FOR, and the checker itself matches a `| Path | Quote | Grounds |`
row on its path and its quote alone.
