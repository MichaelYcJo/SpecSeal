# 1789996780-the-census-and-the-tie-that-nothing-holds — questions for the planner

<!-- seal/specs/1789996780-the-census-and-the-tie-that-nothing-holds/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

## What the tree answered, so nobody reopens it

The three tickets left several judgments open. The tree answered these, and
the grounds are in `spec.md` and in `plan.md`'s Alternatives table where a
reviewer can open them. They are listed because a reader cannot tell a
judgment that was decided from one that was never met.

- **Which corpus every figure in the module is stated over, and how a reader
  is told.** `seal/ledger.md` alone, stated at **one site** — the census note
  beside `MARKER` — with no other comment or docstring in the module
  restating a digit. Every figure in that note carries three clauses: the
  corpus, the instrument, and the moment it was taken. Six sites stating one
  number is the defect #470 reports; correcting six copies would leave six
  copies to drift, which is the shape that has now failed three times.
- **Why that corpus, since #470's stated reason is false.** #470 prescribes
  `seal/ledger.md` as *a corpus a branch cannot move*. It has moved twice:
  `a8bf2a86`, the 0.12.2 release, folded 44 rows from the three
  `seal/ledger/*.md` fragments into it and deleted them — row C1 did not
  exist in that file before that commit — and **this branch moves it again**
  when it corrects C1, because a `Corrected <date>` marker is itself a
  marker. So the corpus is kept and the grounds are replaced: it is chosen
  as the file a release folds the fragments INTO and the one that survives a
  release, and the note says it moves. Shipping *a branch cannot move it*
  would hand the next reader a guarantee the same commit breaks.
- **Whether the three-file figures are corrected or removed.** Removed. That
  corpus does not exist at this SHA, so there is no true version of the
  sentence to write.
- **Whether #469's census case may read the real ledger files.** Yes. The
  defect #470 reports is a **number** over a corpus that moves; a case that
  asserts a **property** over the same corpus does not have it — the corpus
  growing is exactly when the case should speak. So the case reads the real
  files, through the module's own `LEDGER` and `FRAGMENTS` constants rather
  than a hard-coded list, and asserts no count at all. A hard-coded list goes
  blind at a fold, which has already happened once.
- **What the census case does when the corpus grows a longer run.** It goes
  **red**, naming the file, the row, the run length and the spelling, so the
  bound is raised deliberately with the case re-driven. A warning or a skip
  is a green that means nothing, which is the hole the issue exists to close.
  The false refusal on a legitimate new spelling is the accepted cost, and
  the message is what makes it one line of work rather than an investigation.
- **Whether the six tracked files stating 404 are corrected in place, and
  with what marker.** In place, and the marker is decided by the file class.
  SDD records take the `<!-- CORRECTED <date> by work item 1789996780
  (#<issue>). … -->` marker that work item 1789996775 fixed one hour earlier,
  **adopted verbatim** including the uppercase verb and its reasoning: a
  hand-grep for the ledger's sentence-case `Corrected <date>` must not return
  an SDD record, and that grep is the only way the #424 incident was ever
  caught. `seal/ledger.md` row C1 takes the ledger's own sentence-case
  marker, because `correction-check` reads that file and that spelling. Code
  and test comments are corrected with no marker at all — git history is the
  audit trail for code, and a marker there would answer the wrong grep.
- **Which records are in and which are out.** `spec.md`, `plan.md`,
  `overview.md`, `changelog.md` and a ledger row state a present fact, so a
  false one is corrected. `rounds/round-N.md`, `rounds/round-N-report.md` and
  `phases/phase-N.md` assert a past state at a named SHA and are the audit
  trail every correction cites, so they are left alone. Work item 1789996775
  settled this and the same reasoning applies unchanged.
- **Which sites the class actually has.** Enumerated by construction over the
  tracked tree, never from round 3's list of six. Two of the six have moved
  under the list: the ledger fragment was folded into `seal/ledger.md` as row
  C1, and the changelog fragment was gathered into `CHANGELOG.md` §0.12.2 —
  a seventh site the list does not name, and the one a reader outside the
  work item actually reads. Q1 is what that seventh site turns into.

## The rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | May this branch amend the released `CHANGELOG.md` §0.12.2 section, which carries the same false figure — *404 marker occurrences on 190 rows* — at `CHANGELOG.md:121`? It is the copy a reader outside the work item meets, and `gather_changelog.py` decides by marker and never by content, so a corrected fragment is never re-gathered and the two copies simply diverge with nothing able to see it | **a person** — the repository owner. Policy points two ways: `CONTRIBUTING.md` §*House rules* says *one branch does edit `CHANGELOG.md`, and it is the one based on `main`*, and this branch is not that one; `CLAUDE.md` says *appended is the word, and a removal is not one*, which is what lets a branch touch a shared file to leave it true. Accountability for a released record is the owner's. **This is the same question work item 1789996775's Q1 asks about a different sentence in the same released section — one answer governs both** | **Amend** — both copies land in one commit and the reader-facing one stops being false, and a released section is edited by a branch `CONTRIBUTING.md` says does not edit it. **Leave** — the fragment and the work-item records are corrected, §0.12.2 keeps the false sentence, and the divergence is disclosed rather than silent | **Leave.** It is the reversible half: a false sentence in a released section can be corrected by any later release branch, and an amendment to a released record cannot be un-made without another one. `smith` builds this default, records the divergence as a row of `overview.md` §*Not verified* naming the owner, and adds a `seal/follow-up.md` item so the next release branch can carry it | ⬜ |
| Q2 | #469's own issue body carries a histogram whose `1 word` row is counted over `seal/ledger.md` alone while the `0 words` row above it is counted over the three ledger files, so the table sums to 412 and is neither corpus — round 3 measured this and wrote the replacement. Who repairs the ticket? | **a person** — the orchestrator or the repository owner. `agent-contract` §6 withholds posting from every agent, so neither `framer` nor `smith` can edit an issue body. It is named here rather than left, because a false census in the ticket that asks for a census instrument is the specific thing #469 exists to stop | **Repair the ticket** — the body states which corpus each row is, using round 3's measured replacement, re-taken at the tip. **Leave it** — the ticket keeps a figure neither corpus, and the tree is true while the request that produced it is not | **Leave the ticket to a person and make the tree true.** `smith` writes the corrected statement into this work item's own records, where it is readable, and names the ticket's error in `overview.md`. The conclusion the histogram supports — there is no run of four — is unchanged on either corpus | ⬜ |
| Q3 | Do the comment and docstring edits drift the ledger anchors that cite this module — `correction_check.py#MARKER`, `#VERBS`, `#markers`, `#examine` — given that the census note sits immediately above the `MARKER` assignment? | **a measurement** — `bin/evidence-check` at the branch tip names what drifted; asking a person what a content hash covers is the wrong instrument | If they drift, every row citing a drifted coordinate is **read by hand before** `evidence-check --reverify` runs, then re-stamped. If they do not, nothing is re-stamped | Assume `#MARKER` may drift and `#examine` does not, since `examine` is not edited. Read, not executed by this frame — `seal/follow-up.md` measured that the drift report names a coordinate once while `--reverify` re-stamps every row citing it, which writes *somebody read this* over rows nobody opened | ⬜ |
| Q4 | What are the figures — the file's marker total, the part on rows, the part in prose, and the bound comparison — at this branch's tip, **after** the C1 correction lands? | **a measurement** — the unbounded walk phase 2 establishes, re-run in phase 4. This frame states no digit on purpose: every number the tickets and the round reports hand over was taken before the 0.12.2 fold, and `agent-contract` §5 says an aggregate is not a coordinate | The measured figures are what the census note and C1 say. Restating round 3's is the third circular census in a different costume | Nothing. No digit is inherited; each is re-taken with the instrument and written with its date | ⬜ |
| Q5 | Does `survivor-check --range origin/<base>...HEAD` fire on the sentences phase 3 removes? Near-identical sentences stand in the round records and round reports of work item 1789969379, which this work deliberately leaves alone | **the work** — the phase that removes the wording is the phase that can run the check. Nothing decidable at framing time | If it fires, the answer is a `survivors.md` row with the quote and the grounds — the surviving copies are past-state records — and never a reword chosen to quiet the checker | Assume it may fire; write the row with grounds if it does | ⬜ |
| Q6 | Is `Re-read and re-stamped a third time <date>` still the longest qualifier the tree carries, and does it still sit where the module comment says it does? The claim is addressed positionally, as `seal/ledger.md:1172`, and the 0.12.2 fold added 44 rows to that file | **a measurement** — the same unbounded walk answers both halves in one run | Whatever it measures is what A9 writes, and it is written as a **content** coordinate — the row and the spelling — because `CLAUDE.md` says a coordinate names content and never a position | Assume the spelling still stands and the line number may not. Neither is restated without the run | ⬜ |

**`smith` answers Q3, Q4, Q5 and Q6, and must not answer Q1 or Q2.** Q1 is
the owner's: its two answers mean different files edited and the accountable
party for a released record is the owner — building the default is not
answering it, and the row stays ⬜ with the divergence disclosed. Q2 is a
person's for a different reason: the repair is an act `agent-contract` §6
withholds from every agent, so no agent can close it however clear the answer.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
