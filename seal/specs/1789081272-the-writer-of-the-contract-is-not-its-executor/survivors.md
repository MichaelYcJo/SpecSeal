# 1789081272-the-writer-of-the-contract-is-not-its-executor — survivor exemptions

## Phase 2 — the move out of the design gate

`survivor-check --range 02c5b90..5571996` examines 843 files against the
seventeen sentences the range removed and reports one place. It is a
coincidence of ordinary Python, scoring 1.89 on three shared phrases — two of
them the same fragment counted twice — and it is not a copy of anything this
phase corrected.

The removal that produced it is `test_the_design_gate_belongs_to_the_smith`, <!-- NAME NOT IN TREE: the case phase 2 split into two; the name is what this row read when it judged the report -->
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
| `seal/specs/1788310269-the-implementer-leaves-a-mark/overview.md` | "A work item commits many times and the implementer does not change when it does" | **A past work item's closing memo**, giving the reason the mark is keyed on the branch as that work item gave it. The live copy is `docs/review-chain-spec.md`'s paragraph, which this phase widened to *neither the framer nor the implementer*, and the ledger Notes cell that carried the same sentence, which now says *whoever does its work*. A memo written when there was one axis is not wrong about the release it closed |
| `seal/specs/1788310269-the-implementer-leaves-a-mark/plan.md` | "A work item commits many times and the implementer does not change when it does" | **The same sentence in the same past work item's plan**, and a record for the same reason. A plan states what its own phases were going to build; rewriting it to match a later release makes it a record of nothing |

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

**The range was widened twice and the report changed both times, which is why
the rows outnumber what any one run says.** Over `e82403f..d950e8b` the check
reports six places; over `e82403f..553afb1`, two; over `e82403f..1601614`,
five — three of them new, because the later commits reworded
`docs/review-chain-spec.md`'s *the implementer does not change when it does*
and that put a fresh sentence on the removed side. The ledger Notes cell
carrying it was corrected rather than exempted — it now says *whoever does its
work*, which is true of both axes and states no new claim about either — and
the two past-work-item records below it are exempted. Every row here is kept
whether or not the run at hand reports it, for the reason phase 2's row gives:
an exemption matching no candidate silences nothing, and deleting one would
leave this record naming a survivor with nothing behind it.

## Round 1 fix pass — the deferral written on the acceptance row

`survivor-check --range 1d1b6e9..029e4fe` examines 851 files against the
thirty-one sentences the range removed and reports two places, both the same
line of `plan.md` and both from the same correction.

Finding 8 struck through `spec.md`'s S10 acceptance row, which was the only
place of eight where the #350 deferral was not written. That put S10's whole
scenario on the removed side, and `plan.md` row 5 — phase 5's `Delivers`
cell — says the same thing in almost the same words, because the acceptance
row and the phase row were written from each other.

**The phase row is not a survivor, because the deferral is on it.** Its
`Status` cell reads `deferred #350`, which round 1 examined as its own
finding and withdrew: an issue number asserts a past state somebody can open,
exactly as a commit hash does. A reader meeting the promise in the `Delivers`
cell meets the deferral in the same row, which is the state finding 8 was
asking for and not the state it was correcting.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/plan.md` | "one row per segment, named by its spawn's `subagent_type`, with its own span" | **A plan row that states what its phase was going to build, with the deferral in its own `Status` cell.** Striking it through would contradict round 1's withdrawal of finding 13, which read `deferred #350` as the correct treatment for this row. What finding 8 corrected was an acceptance row carrying NO marker anywhere on it; this row carries one in the column that exists for it |
| `seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/plan.md` | "the segments it could not name counted and printed rather than dropped" | **The same cell and the same grounds**, reported a second time because the correction removed two separate sentences of S10's scenario and both have a counterpart here. A plan states what its phases were going to build; rewriting it to match the deferral makes it a record of nothing, which is the reading phase 4's rows already give a past work item's plan |

**What would make these exemptions stop holding.** The quote is the anchor in
each, and the `Status` cell is the condition. If phase 5's row ever loses
`deferred #350` — if the deferral is taken back, or the row is edited to read
as live again — the `Delivers` cell is a promise with nothing beside it and
the report is a finding rather than a coincidence of two documents written
from each other.

Anchored on this range as well as on these quotes, the same way every row
above is.

**Over the range CI reads the two reports are gone, and the rows are kept
anyway.** `survivor-check --range origin/release/v0.11.0...HEAD` examines 851
files against 144 removed sentences and reports two places, both of them
phase 4's already-exempted changelog pair. The wider range counts S10's
scenario differently, so the pairing that scored 2.00 and 1.69 over the fix
range does not survive the recount. The rows stay for the reason phase 2's
row gives: an exemption matching no candidate silences nothing, and deleting
one would leave this record naming a survivor with nothing behind it.
