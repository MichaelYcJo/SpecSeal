# 1789996775-the-gate-states-what-its-own-fixes-disproved — questions for the planner

<!-- seal/specs/1789996775-the-gate-states-what-its-own-fixes-disproved/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

## What the tree answered, so nobody reopens it

The three tickets left four judgments open. Three of them the repository
answered, and the grounds are in `spec.md` and in `plan.md`'s Alternatives
table where a reviewer can open them. They are listed here because a reader
cannot tell a judgment that was decided from one that was never met.

- **May a SHIPPED work item's own records be corrected in place, and with
  what marker?** Yes, in place, with the marker `spec.md` §*The correction
  marker* fixes. The precedent is inside the very work item being corrected:
  `seal/specs/1789956662-…/phases/phase-3.md`:34 and `phases/phase-4.md`:38
  both correct a statement in place under a `<!-- CORRECTED … -->` comment,
  and phase-3 writes the reasoning down — *Corrected in place with the round
  and the finding named, never deleted silently … a record of a past state
  that quietly becomes true is a record nobody can audit.* Nothing in
  `CLAUDE.md`, `CONTRIBUTING.md` or `docs/one-root-by-lifetime.md` freezes an
  SDD record at the release. What those three do freeze is somewhere else:
  the shared ledger, whose rows carry `Corrected <date>` and `Re-read <date>`
  and which `correction-check` watches, and the released sections of
  `CHANGELOG.md`, which Q1 below is about.
- **Which records are in and which are out.** `spec.md`, `plan.md`,
  `overview.md` and `changelog.md` state a present fact about the shipped
  change, so a false one is corrected. `rounds/round-N.md`,
  `rounds/round-N-report.md` and `phases/phase-N.md` assert a PAST state at a
  named SHA — `skills/implement/SKILL.md` §*Document layout* — and they are
  the audit trail every correction cites, so they are left alone.
- **Whether `moved_line` should speak for CI at all when resolution reached a
  spelling like `@{-1}`** (#461's second half). No, and the tree decides it
  rather than taste: `seal/ledger.md`'s R4 row records as **Executed** the
  claim *it never says CI reads a ref CI does not read*, and `@{-1}` is a
  spelling where it does. Either the code becomes true or the row is narrowed,
  and the design intent is the row's own wording, so A2 makes the code true
  and A7 corrects the row for having been verified as true when it was not.

## The rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | May this branch amend the released `CHANGELOG.md` §0.12.2 section to add the evidence label A4 adds to the three work-item records? The same unlabelled sentence stands there, it is the copy a reader outside the work item actually reads, and `gather_changelog.py#ungathered` decides by MARKER and never by content — so a corrected fragment is never re-gathered and the two copies simply diverge, with nothing able to see it | **a person** — the repository owner. Policy is not silent here, it points two ways: `CONTRIBUTING.md` §*House rules* says *one branch does edit `CHANGELOG.md`, and it is the one based on `main`*, and this branch is not that one; `CLAUDE.md` says *appended is the word, and a removal is not one*, which is what lets a branch touch a shared file to leave it true. `skills/implement/SKILL.md` §1 sends a ticket that asks for what a policy clause forbids to a person rather than to a build. Accountability for a released record is the owner's | **amend** — the label lands in both copies in one commit, the reader-facing copy stops being unlabelled, and a released section is edited by a branch `CONTRIBUTING.md` says does not edit it. **Leave** — the fragment is labelled, `CHANGELOG.md` §0.12.2 keeps the unlabelled sentence, and the divergence is disclosed rather than silent | **Leave.** It is the reversible half: an unlabelled true sentence in a released section can be labelled by any later release branch, and an amendment to a released record cannot be un-made without another one. `smith` builds this default, records the divergence as a row of this work item's `overview.md` §*Not verified* naming the owner, and adds a `seal/follow-up.md` item so the next release branch can carry it | ⬜ |
| Q2 | What property does `git check-ref-format --branch` actually have, in the words A1 will state? Round 2 measured the five outcomes on git 2.54.0 and this frame did not re-run them | **a measurement** — one probe over the five spellings of round 2's finding 10 (`HEAD`, `HEAD~1`, `base@{u}`, `topic@{1}`, `@{-1}`), plus what the command PRINTS for `@{-1}`, which is the half that says whether the property is *expands `@{-N}` then checks* or merely *accepts it* | The measured property is what A1 writes. Asking a person for it is the wrong instrument | Round 2's measured table, which A1 must not restate without re-running: `@{-1}` accepted, the other four refused | ✅ **Answered 2026-09-21 by measurement, phase 1.** The property is *expands `@{-N}`, then checks what it expanded to*, and the stdout is what settles it: `@{-1}` exits 0 **and prints `base`**, while `HEAD`, `HEAD~1`, `base@{u}` and `topic@{1}` each exit 128 with *is not a valid branch name*. Re-run on git 2.54.0 in a scratch clone rather than restated. `phases/phase-1.md` and `seal/ledger/1789996775-….md` W1 carry it |
| Q3 | Which git command separates `origin/@{-1}` from `origin/base` without a pattern written in `broad_gate.py`? `git check-ref-format <full refname>` is the candidate — a full refname may not contain `@{` — and it is git's own answer rather than a hand-rolled one, which is what #461's *Not this* requires | **a measurement** — run it against the constructed runner ref for each of the five spellings, in a scratch repository, and read the exit code directly (`cmd >/dev/null 2>&1; echo $?`, never through a pipe) | If it separates them, A2's guard is that call. If it does not, `plan.md`'s Alternatives table holds the fallback: drop the runner clause entirely where the given spelling is not the one the workflow would spell, which needs no new command | The `check-ref-format` call on the full refname. Read, not executed by this frame | ✅ **Answered 2026-09-21 by measurement, phase 1.** It separates them. `git check-ref-format refs/remotes/origin/<spelling>` exits 0 for `base`, `release/v0.12.3` and a short SHA, and exits 1 for `@{-1}`, `HEAD~1`, `base@{u}` and `topic@{1}`; the bare `origin/<spelling>` label the gate actually builds separates them identically, so the guard asks git about the string that is printed. `plan.md`'s fallback was not needed. `a_runner_could_hold` is that call |
| Q4 | Does `survivor-check --range origin/release/v0.12.3...HEAD` fire on the wording A3 and A6 remove? Near-identical sentences stand in `seal/specs/1789956662-…/phases/phase-1.md` and in the three round reports, none of which this work touches | **the work** — the phase that removes the wording is the phase that can run the check. Nothing decidable at framing time | If it fires, the answer is a `survivors.md` row with the grounds — the surviving copies are a phase record and three round reports, all past-state records A5 deliberately leaves alone — and never a reword chosen to quiet the checker | Assume it may fire; write the row with grounds if it does | ✅ **Answered 2026-09-21 by the work, phases 2 and 3.** Clean at phase 2 over the range up to `b4a8f0f`. Phase 3's removals made it speak three times. One was a real defect and was corrected — the sentence A3 removed was still standing in the panel case's own docstring, and round 2's finding 13 paste-ready text, which QUALIFIES the claim rather than dropping it, is what ships. The other two are excused in `survivors.md` with a quote and grounds: both carry only the true half of the removed sentence and neither draws the inference the range corrected |

**`smith` answers Q2, Q3 and Q4 and must not answer Q1.** Q1 is a person's:
its two answers mean different files edited, and the accountable party for a
released record is the repository owner. Building the default is not
answering it — the default is the reversible half, and the row stays ⬜ with
the divergence disclosed until the owner says otherwise.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
