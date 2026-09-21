# 1789996775-the-gate-states-what-its-own-fixes-disproved — overview

<!-- The closing memo (implement skill, step 4). Not a summary of the work:
`git diff --stat` holds the file list and the diff holds the detail. Only what
the diff cannot show goes here. -->

📋 implement applied
· spec:     `seal/specs/1789996775-…/spec.md` A1–A8 and §*The correction
            marker*; `plan.md` four phases and §*Alternatives considered*;
            `questions.md` Q1–Q4; `CLAUDE.md` §*A change writes fragments,
            never the shared file*; `CONTRIBUTING.md` §*House rules*;
            `skills/agent-contract/SKILL.md` §§1, 2, 4, 8, 9, 12, 14, 15;
            `seal/specs/1789956662-…/rounds/round-2-report.md` findings 10,
            13, 14 and `round-3-report.md` finding 15 with its paste-ready
            fixes
· evidence: `seal/ledger/1789996775-the-gate-states-what-its-own-fixes-disproved.md`
            W1, W2, W3 — new. `seal/ledger.md` R4 of work item 1789956662
            corrected and re-read, R5 re-read, and G6 of work item 1789985781
            re-read for the shared `panel` anchor
· verified: executed — the ref-format probe over five spellings, the two new
            cases seen red then green, one mutation of `a_runner_could_hold`,
            three test modules, `evidence-check` and `--reverify`,
            `survivor-check`, `correction-check`, `unverified-check`, and
            `ruff check` / `ruff format --check` over the two touched source
            files. Read — the three comment sites of A6, the four record
            sites of A4 and A5, and the three ledger rows read by hand before
            `--reverify`. Unverified — the full suite, the repository-wide
            lint and the typecheck, which are the `sealer`'s one broad run

## Why this work exists

Three sets of statements that #423's own fixes disproved were still standing
where a reader meets them, so the gate's docstrings, its test module and the
shipped work item's records each asserted something that work item had
measured to be false.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the A5 marker sits for a statement inside a markdown table | `spec.md` §*The correction marker*: *A5's marker sits immediately after the statement it is about* | The marker for the `seal_stamp.py#letter` row sits after the whole table, and its first sentence says so and names the row | A `<!-- -->` line between two table rows splits the table in every renderer, so *immediately after* would cost the three rows below it their table. The marker's two deliberate properties — the uppercase verb and naming the work item and the issue — are untouched |
| The wording of the marker's grounds clause for the three A4 sites | The template's slot reads *It is false because …* | *It is not false, and that is the point* — the grounds are that the statement carried no evidence label and no answerer | The three A4 statements are true. What A4 adds is the label, and a marker asserting the sentence was false would be a second false statement in the same record. The slot's job is the grounds with the coordinate, which it still carries |
| A third ledger row was marked where A7 names two | `spec.md` A7: *`seal/ledger.md`'s R4 and R5 of work item 1789956662 are re-read and re-stamped* | G6 of work item 1789985781 carries a `Re-read` note too | `--reverify` re-stamped three rows, not two: the lenient report names `panel` once and R5 and G6 both cite it. Leaving G6 re-stamped with no note is precisely the silence `seal/follow-up.md`'s open row measured, and the shared ledger's own S12 row already carries the `Re-stamped by the same --reverify run` sentence as precedent (`agent-contract` §12) |
| This work item's own `spec.md` §*Data & interfaces* carried two stale stamps | The framer wrote the two coordinates with a bare filename and the pre-change hashes, f312f19b and e2c844e8 | Both re-stamped to the post-change hashes, with the old hash named beside each, and the paths written in full | `evidence-check`'s records arm read both as BROKEN at exit 2 once A2 and A3 landed — *file not found — same name at skills/verify/scripts/broad_gate.py (content differs)*. The frame is this work item's live contract rather than a shipped record, so no A5 marker is owed; the old hash is kept in the cell so the drift is readable |
| A6's grep criterion returns two lines rather than none | `spec.md` A6: *`grep -n "byte-identical\|exactly as it did\|reading as it did"` over the module returns nothing that still claims the module was untouched* | Left as it is, and recorded here | The two hits are the corrections themselves — *all but ONE assertion … reading as it did* and *It is NOT byte-identical*. The criterion is about surviving claims, not about the tokens, and rewording the replacements to empty the grep would mean departing from round 3's paste-ready text for the checker's benefit |

## What the broad gate found, and the one commit after it

The sealer's first run came back **NOT SEALED, exit 1**, one arm of seven red:
`tests/test_release_hygiene.py::test_no_loaded_file_names_a_version_at_or_above_the_running_one`,
labelled `new` by the gate because the same file passes at the base. The
offending line is `skills/verify/scripts/broad_gate.py:399 names 2.54.0` —
the git build A1's docstring states its measurement was taken on.

**It is git's version and not this plugin's**, so no release of SpecSeal
makes it wrong, and the test has a mechanism for exactly that:
`VERSIONS_OF_ANOTHER_PRODUCT`, keyed on `(file, token)` so an exemption stays
a fact about one comment rather than a hole the number can walk through
anywhere. `skills/implement/scripts/seal.py`'s git `2.50.1` is already in it,
declared for the same reason in the same words — *an exit code read off an
unnamed git is not a measurement*. This branch adds the second git entry and
says in the cell that the pair is what makes the class visible.

Two things about this, said plainly because the commit lands after the review
rounds closed:

- **The red was seen before the fix**, and by the gate rather than by the
  session that wrote it: the failure output is quoted in full above. That is
  `CONTRIBUTING.md` §*What a change to a gate must carry*'s first bullet in
  its strongest form.
- **It ships unreviewed.** Round 1 had already answered `Needs a fix: no` and
  closed, and this is a gate refusal rather than a round finding, so no
  reader opened it. It is one dictionary entry and its reason; what a reader
  would weigh is whether the entry is right or whether A1's docstring should
  have named the git build some other way. The entry follows the precedent
  the file already carries.

**The gate was then spent a second time.** The first run's eleven-and-a-half
minute suite is not recoverable — `uvx ruff check` and `uvx ruff format
--check` never ran in it either, because the repository's `Broad gate` row is
one `&&` chain and `bin/test` short-circuited it.

## Not verified

| Item | Who must answer |
|---|---|
| **Q1 — whether `CHANGELOG.md` §0.12.2 should carry the evidence label this work adds to the three work-item records.** Built to its default: the released section is left alone, so a reader of `CHANGELOG.md` meets the baseline half unlabelled while `changelog.md`, `plan.md` and `overview.md` of work item 1789956662 carry the label. `gather_changelog.py#ungathered` decides by marker and never by content, so the corrected fragment is never re-gathered and the two copies simply diverge with nothing able to see it. `questions.md` Q1 holds both readings of policy and the row stays ⬜ | **the repository owner.** `CONTRIBUTING.md` §*House rules* says one branch edits that file and it is the one based on `main`; `CLAUDE.md` says appended is the word and a removal is not one. Accountability for a released record is the owner's, and `seal/follow-up.md` carries the item so a later release branch can take it |
| ✅ the full suite, the repository-wide lint and the typecheck | **The `sealer`'s second run answered it.** `broad-gate --base release/v0.12.3 --record …` at `6af8406c` against `8531c858`: **SEALED, exit 0**, seven arms. The repository's `&&` chain ran to its end this time — `3955 passed, 9 skipped` in 11m49s, then `All checks passed!` and `154 files already formatted` — and the ledger, corrections, survivors, chain and mode arms each exited 0. `rounds/round-1.md`'s `Broad gate` cell carries the SHA pair. The first run is the section above |
| whether the baseline half of the direction claim — *a baseline carried forward drops the rows the base's own newer commits added* — is worth a case of its own. This work labels it `read, not executed` in three records and does not measure it | the repository owner, who is named as its answerer at all three sites |
| the two new cases and the `@{-1}` fixture on Windows and Linux. `git switch` and `check-ref-format` are git behaviour rather than OS behaviour, and the exit codes were read on macOS with git 2.54.0 alone | CI's matrix, at this branch's pull request |

## Not done

**The two em-dash clauses round 2's finding 10 noticed in `moved_line`'s
second filling.** `spec.md` §*Explicitly out* rules them out and the wording
A2 chose happens to leave one clause where there were two in the new third
branch, which is A2's own text rather than a second change. The `reads`
branch round 1's finding 2 wrote is untouched and still carries both.

**The round records and phase records of work item 1789956662.**
`spec.md` §*Explicitly out* and `questions.md` §*What the tree answered* both
say why: they assert a past state at a named SHA, they are the audit trail
every correction here cites, and round 3's finding 15 already excused
`phases/phase-1.md`'s superseded reading on the record.

**A3 of work item 1789956662's `spec.md` is untouched**, which is #465's own
*Not this*. The spec was right and the three comments drifted from it.

**Two `survivors.md` rows were written, and the file is why the check is
now silent.** Phase 3's first removal was too wide, `survivor-check` over
the range reported two standing places at 1.90 and 1.67 against a floor of
1.6, and both were excused with a quote and grounds rather than reworded.
Measured afterwards at `9948b8af`: the same command reports nothing, with
`--exempt` and without it. Removing `survivors.md` in a probe commit brings
both places back. The file's own quotes raise the document frequency of the
phrases it excuses, which is the arithmetic
`skills/code-review/scripts/survivor_check.py` documents for a work item's
`rounds/` records and excludes them for — so the two rows are silenced
rather than printed under `exempt` with their grounds, and a reader of the
step learns nothing. The tool question is tracked as #308; the rows and
their grounds stand as written.

<!-- CORRECTED 2026-09-21 by work item 1789996775 (round 1, finding 1). What
stood here: "No `survivors.md` row was written, because `survivor-check`
reported no surviving wording over this branch's range. Q4 is answered by the
measurement rather than by an exemption." It is false because `survivors.md`
landed at `95503f60`, the commit after the one that wrote this paragraph, and
`questions.md` Q4, `phases/phase-2.md` and `phases/phase-3.md` all record the
two rows. Corrected in place with the round and the finding named, never
deleted silently: a record of a past state that quietly becomes true is a
record nobody can audit. -->

## Fed back into the spec

**Inferred during implementation, and a planner may overturn it:**
`names_a_branch` and `a_runner_could_hold` are two questions about one input,
and neither is the other's duplicate. `origin/HEAD` is the one spelling
`check-ref-format` accepts on the whole name that no `--base` ever reaches,
because `names_a_branch` refuses `HEAD` a step earlier — so removing either
guard reopens a defect the other does not catch. The ledger's W2 row carries
this and `spec.md` A2 did not state it.
