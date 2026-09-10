# 1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it — survivor exemptions

## Phase 3

`survivor-check --range 52f6bd3..HEAD` reports three places. Two were real
survivors of the same correction and are fixed in the range —
`skills/code-review/scripts/chain_check.py`'s two failure messages told a
reader to take the broad run by hand and to write the cell with
`round_record.py close --broad-gate`, which is what this phase moved to a
sealer spawn. They are corrected and pinned, so they are not exempted here.

The third is not a stale copy of a corrected claim. It states a different
fact, in a sentence the correction did not touch.

| Path | Quote | Grounds |
|---|---|---|
| `README.md:71` | At the gate, the run is read against the base commit: a failure that predates the work is named as a follow-up rather than chased, and nothing edits between that seal and the PR. | **Still true, and about a different subject.** What the range removed is `agents/smith.md`'s instruction to the implementer — *when the broad gate returns a failure, first ask whether it fails on the base commit as well* — which named an act the smith no longer performs, because `broad-gate` now re-runs the failing files at the base itself and hands back `new` or `failing on base too`. The check matched two phrases the two sentences share, *"a failure that predates the"* and *"the work is"*, scoring 1.60. The README sentence names no actor: it says the comparison happens at the gate and what a base failure is treated as, and both are exactly what the gate does now. Correcting it would remove a true statement about the design in order to erase a coincidence of wording |

**What would make this exemption stop holding.** The quote is the anchor. If
that sentence comes to name WHO takes the comparison — the smith, the
orchestrator, or a session reading the report — it is asserting the act this
range moved to the sealer, and it becomes a genuine survivor.

## Phase 4

`survivor-check --range 6f09a3f..HEAD` reports four places, and the corrected
sentence behind three of them is one this phase wrote: `seal/ledger.md`'s G2
row said *`close --broad-gate` is the only thing that changes the value*,
which #30 made false by adding `seal`.

**Two of the four were corrected rather than exempted**, and they are the two
that are alive: `skills/code-review/scripts/chain_check.py`'s gate docstring
and the inline comment a hundred lines below it both enumerated the writers of
the `Broad gate` cell and both stopped at one. Phase 3 left them, reading the
sentence as reasoning that survives `seal` joining `close`; the word in it is
*only*, and the conclusion it carries — *so a cell this arm cannot parse there
is a cell somebody chose* — rests on the enumeration being complete. An
enumeration one short is the defect, which is the same class phase 3 corrected
in the docstring of the case that pins that arm.

The three below are records of what was true when they were written. None of
them describes the tree as it stands, and correcting one would rewrite what a
past release shipped or what a past phase decided.

| Path | Quote | Grounds |
|---|---|---|
| `CHANGELOG.md` | above the cutoff `round_record.py new` writes the row on every record and `close --broad-gate` is the only thing that changes the value, so such a cell is a choice | **True of the release it describes.** `seal` did not exist in 0.9.5 — #30 adds it in 0.10.0 — so the entry is an accurate account of what that release shipped. A changelog entry is dated by the section it sits in, and editing a shipped section to match a later release makes it a description of the present rather than a record of a release |
| `seal/specs/1788912166-red-for-following-the-documents-green-for-ignoring-one/changelog.md` | above the cutoff `round_record.py new` writes the row on every record and `close --broad-gate` is the only thing that changes the value, so such a cell is a choice | **The same sentence, in the fragment that produced it.** `gather_changelog.py` copies a fragment into the released section and leaves the fragment behind, so this is the source of the row above and shipped with it in 0.9.5. Correcting it would put the fragment and the section it was gathered into out of step, which is the one thing a reader comparing them checks |
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/phases/phase-3.md` | Renaming it removes an anchor rather than drifting one, and a removed anchor is BROKEN where a changed body is DRIFTED — so the rename belongs to the phase that touches the ledger, beside the row it forces | **This work item's own record of the handover, and it is what phase 4 carried out.** The corrected text is the docstring of the case phase 3 chose not to rename; phase 4 renamed it and the docstring now says why the old name stood. The record says why phase 3 deferred the rename, which is a statement about a decision rather than about the tree, and it stays true whatever the case is called. The line carries `NAME NOT IN TREE` for the same reason |

**What would make these three stop holding.** Each quote is its own anchor. If
a CHANGELOG section is ever rewritten to describe the tree as it stands rather
than the release it shipped, the first two stop being history and become
present-tense claims; and if `phases/phase-3.md` comes to assert what the case
is called TODAY rather than what phase 3 read and deferred, the third does.

### Over the whole branch — what CI reads

The phase ranges above each end at 0. `survivor-check --range
origin/release/v0.10.0...HEAD`, which is the spelling the pull-request check
uses, reports four more, and all four share one cause.

**What this branch removed from `chain_check.py` is an INSTRUCTION**: *write
the SHA the one full-suite run happened at and the base it was compared
against (`round_record.py close --broad-gate …`)*, replaced by the sealer's
spawn. **What the four places below share with it is the cell's VALUE
FORMAT** — *the SHA the one full-suite run happened at and the base it was
compared against* — which the correction kept word for word, because the
format did not change and nothing about it was ever the orchestrator's act.
Correcting them would edit four true descriptions of a cell in order to erase
a wording the correction itself preserved.

| Path | Quote | Grounds |
|---|---|---|
| `templates/sdd-round.md` | `not yet`, or the SHA the one full-suite run happened at and the base it was compared against. | **This is the row this branch edited, and the edit is one sentence further along.** The quoted half describes what the cell may hold; the sentence added immediately after it names `round_record.py seal`, the sealer's route through `broad-gate --record <item>`, and `close --broad-gate` for the one pass where fixes and the gate land together. A reader who reaches the quoted words reaches the new sentence in the same breath |
| `seal/specs/1788912166-red-for-following-the-documents-green-for-ignoring-one/spec.md` | The `Broad gate` cell — `not yet`, or the SHA the one full-suite run happened at and the base it was compared against | **A shipped work item's specification of the cell's value, and #30 did not change that value.** #295 gave the cell a reader; #30 gives it a writer with a name. Neither moved what goes in it |
| `tests/test_chain_check_at_the_pull_request.py` | The cell was written on every record and read by nothing, so a work item could open a ready pull request having never run the one full-suite pass | **The docstring says why that arm exists, and it is a statement about the state before #295.** The shared phrases are *full suite pass* and *run the one* — the thing both sentences name, rather than the act one of them moved. The same case gained an assertion in this range that the refusal names the `sealer`, so the file is corrected where the correction was owed |
| `skills/code-review/SKILL.md` | target commit SHA (mandatory — branches move between rounds), verdict table with the grounds behind each verdict, **executed probe results** | **A list of what a reviewer's report carries, which names no broad run at all.** The overlap is on `SHA` and on words any sentence about a commit uses; nothing in the line is about who takes the gate |

**What would make these four stop holding.** Each quote is its own anchor. Any
of them coming to say who WRITES the cell, or who takes the run, is asserting
the act this branch moved to the sealer, and becomes a genuine survivor — the
template's row is the one to watch, because it is the one that already names a
writer one sentence later and could easily come to name the wrong one.

## Phase 5

`survivor-check --range 0eae75b..HEAD` reports seven places. **One was
corrected rather than exempted** — `skills/verify/scripts/broad_gate.py`'s
docstring listed the three refusals `round_record.py seal` used to have, and
this phase left it two. Enumerating that class by hand found four more the
checker could not see, because they share no wording with the lines the range
removed: `agents/sealer.md` twice, the seal module's own docstring, and this
work item's changelog fragment. All five are corrected in the range.

The six below are not stale copies of a corrected claim. Every one of them
overlaps the deleted code on **identifier n-grams** — `chain.FLOOR_NO`,
`chain.FLOOR_YES`, `chain.yes_or_no`, `chain.field(rows, chain.NEEDS)`, and
assertions on another checker's `Needs a fix` output — and each is a
different reader of that row, doing a job this phase did not touch.

**The one worth stating rather than dismissing is the floor bound.** It still
reads `Needs a fix`, on purpose: it asks whether the run REOPENED, which is
the reviewer's own answer and stays the reviewer's. `seal` asked a different
question of the same row — has the run ended — and that is the question the
`Pass` box answers from the verdict table. Two readers of one row, asking two
things, is the state this phase arrived at deliberately.

| Path | Quote | Grounds |
|---|---|---|
| `skills/code-review/scripts/round_record.py` | What stands after the colon in the report's `<label>: …` line. | **The reader that puts the reviewer's line INTO the record.** `new` copies `Needs a fix` from the report; nothing about which row `seal` refuses on reaches it. The overlap is `chain.FLOOR_NO` and `chain.FLOOR_YES`, the vocabulary constants both functions name |
| `skills/code-review/scripts/round_record.py` | seen = [] for _k, path in earlier: try: with open(path, encoding="utf-8") as handle: | **The floor bound's walk over earlier records**, which reads `Needs a fix` to find the first later record saying the run reopened. That is the question above, and it is not the one `seal` stopped asking |
| `tests/test_the_pull_request_language_is_the_repositorys.py` | chain = _checker( "chain_check", "skills", "code-review", "scripts", "chain_check.py" ) | **A loader for two checker modules.** The overlap is the module and constant names, in a file about which language a pull request is written in |
| `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` | Before round 1 the row was read by no check at all — `grep -rn "Needs a fix"` over the checkers returned nothing | **The record of when that row first got a reader**, which is the floor bound. The shared phrases are `out assert needs` and `a fix in out` — the shape of an assertion on a checker's output, not a claim about the seal |
| `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` | declared(repo, OLD_ITEM, lambda sha: record(sha, needs=value)) code, out = run(repo) | **The floor bound's own cases**, asserting `chain_check`'s message rather than `seal`'s. `seal` is not in this module |
| `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` | began = check_module().NEEDS_FROM | **The grandfathering cutoff for the same row**, which is about which work items the floor bound applies to at all |

**A seventh appeared once the ledger row was corrected**, because correcting
S6 put its old sentence into the range's removed set.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/phases/phase-2.md` | a third subparser setting the LAST record's `Broad gate` cell alone, refusing while `Needs a fix` reads `yes`, while `Pass` is unchecked | **This work item's own record of what phase 2 built, and it built three refusals.** A phase record states what that phase was asked and what building it found; it is dated by the phase it sits in, the way a shipped changelog section is dated by its release. Correcting it would make phase 2's record describe a decision phase 5 took, and the reader comparing the two phases would lose the fact that the third refusal existed and was removed — which is what `phases/phase-5.md` exists to say |

**Three more appeared once `overview.md` closed its three Not-done
paragraphs**, for the same reason the seventh did: replacing a sentence puts
the old one into the range's removed set, and a record that said the same
thing is then reported.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/phases/phase-4.md` | A capped run has no path to a sealed pull request, and it was measured rather than read. | **Phase 4's own finding, and it was true when phase 4 measured it.** The sentence names what that phase established with a fixture, and phase 5 is what repaired it. A phase record is dated by the phase it sits in; rewriting this one would erase the measurement that bought the repair, which is the one thing `phases/phase-5.md` points back at |
| `docs/flow.md` | A run that reaches the reopening bound turns every finding still open into an issue, which is right | **A statement about the review chain, in the paragraph that sizes a release**, and it is still true — the cap's behaviour did not change. What phase 5 changed is whether a record in that state can be sealed. The overlap is the two phrases both sentences need to describe the same bound |
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/phases/phase-4.md` | the warden's opening stops calling its review mark a seal, and its link sentence is what says which seal is which | **Phase 4's hand-over to phase 5, describing work phase 5 then did.** It is a record of what was asked, which is exactly what `## Five items carried to phase 5` is for, and `phases/phase-5.md`'s own `## What this phase was asked` is the other half of the pair a reader compares |

**What would make these ten stop holding.** Each quote is its own anchor. Any
of them coming to say that `Needs a fix` decides whether the BROAD GATE may
run — rather than whether the run reopened, or what the reviewer wrote — is
asserting the condition this phase removed, and becomes a genuine survivor.
The two `round_record.py` rows are the ones to watch, because they sit in the
file the removal happened in.

## Round 2's fix pass

`survivor-check --range cd7ea2f..HEAD` reports one place. It is not a stale
copy of a corrected claim — it is the function the correction was modelled on,
using the same helper for the opposite question.

| Path | Quote | Grounds |
|---|---|---|
| `skills/code-review/scripts/round_record.py` | A record that says which round read its | **`reach_back`'s own reading of the same cell, and it is where 🟡 12's fix came from.** What the range removed is `seal`'s `nobody_reason(...) is not None`, which refused only `nobody`; what stands here is `nobody_reason(...) is None`, which refuses everything OUTSIDE the vocabulary — the complement, and the correct one. The round-2 report cites this function by name as the precedent: *`reach_back` already refuses this and says why*. The overlap is the helper's name and the `raise Refused` that follows it, which is what any two readers of one cell share |

**What would make this exemption stop holding.** The quote is the anchor. If
`reach_back` comes to refuse only `nobody` — the reading `seal` shipped and
round 2 reopened — it is the same defect in the other subcommand, and it is a
finding rather than an exemption.

## CI's Windows leg

`survivor-check --range cd7ea2f..HEAD` reports two places once the gate
case's `skipif(os.name == "nt")` is removed. Both are other Windows skips and
neither is the defect that removal fixed.

**The first shares the reason string word for word and is still a different
case**, which is why it was opened rather than exempted by shape.

| Path | Quote | Grounds |
|---|---|---|
| `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` | A copy of `bin/` taken on its own | **The class is already answered here, deliberately, by the case directly below it.** This one copies `bin/test` alone into a temporary directory WITHOUT its twin and executes it, so its subject is what `sh` prints when the runner is missing — there is no twin in that copy to reach for. `test_both_wrappers_say_the_same_thing_when_the_runner_is_missing` covers the `.cmd` sentence by READING both files and says so in its own docstring: *on the one platform the `.cmd` twin runs, nothing reads its sentence*. What this branch removed is a skip that stepped around a twin that WAS there; this skip steps around nothing |
| `tests/test_the_printed_ledger_name_is_the_file_that_was_read.py` | Win32 folds `..` before the filesystem | **Platform semantics, not a wrapper.** The skip is about how Win32 resolves a path through a symlink, which has no twin to run instead. The overlap is the decorator's own words — `pytest mark skipif os`, `name nt reason` — which any two Windows skips share |

**What would make these two stop holding.** Each quote is its own anchor. If
the first ever copies the `.cmd` twin into that directory, it has a file
Windows can execute and the skip becomes the one this branch removed. If the
second comes to name a wrapper rather than path resolution, the same.
