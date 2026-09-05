# Implementation Plan: a check reports clean while something is missing

## Summary

Two tickets, one shape. **A check reports clean, something is missing, and the missing thing leaves no trace.**

#153: `evidence-check --ledger '<fragment>'` reads that fragment and nothing else. `1788491830`'s three review rounds and two fix passes all ran it and all reported ok; the broad gate then ran the unscoped form and found **fifteen drifted rows and one broken claim**, one of which the branch itself had made false. The narrowing was adopted for a correct reason — keeping `--reverify` off a row whose claim is false and belongs to somebody else — and carried into reading, where it blinds.

#150: `templates/sdd-round.md` says a round record is written *right after it posts*, and nothing observes it. Measured twice in this release, four minutes and two minutes late, and both times the reviewer's drafted text lived only in a report and the next segment rebuilt it. **A record written late looks finished**, because by then the verdicts read `fixed at <sha>`.

Both alter what a skill instructs and what a gate refuses — the top rung — so this plan comes first.

## Technical context

- `docs/review-handoff-protocol.md:385` — *"the runner incantation"*, in the list of what the handoff carries as coordinates rather than prose. It does not distinguish a command's forms.
- `skills/evidence-check/scripts/evidence_check.py:1379` — `--ledger`, `action="append"`. The narrowing is a list, so the tool knows exactly what it was given and can say what it therefore skipped.
- `skills/code-review/scripts/chain_check.py` — every piece #150 needs already exists: `SHA_RE:517` pulls SHAs out of cells, `is_ancestor:937` walks, `verdict_of:1135` and `FIX_WORDS:327` read verdicts, `round_records:693` lists, `item_began:1300` grandfathers. What is missing is the question.
- The four cutoffs and their subsections in `docs/review-chain-spec.md` — `:651`, `:681`, `:717`, `:749` and the `Ran by` one at `:779`. A fifth follows the same shape, and round 2 of the last work item found that copying a neighbouring table row is how a false claim travels.
- `seal/ledger.md`'s observation 5 in #51, and `docs/flow.md`'s note that a change to `templates/`, `agents/` or `skills/` binds no session until the release ships.

**What breaks in six months.** The refusal reads a commit relationship, and commit relationships change under a rebase — a record's adding commit is rewritten and its new parent may descend from the fix. `plan.md`'s own Status column carries the same caveat for the same reason and tolerates it because nothing measures from it; this refusal does measure. The mitigation to weigh in phase 3: read the record's **first** commit on the branch rather than in the repository's whole history, or accept that a rebase can turn a passing record failing and say so in the message.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Guidance alone for #153 | It binds a session that reads it. The orchestrator that sprang this trap wrote the guidance | Rejected — questions.md Q1; the tool announces too |
| Narrow `--ledger` so it cannot be the only argument | Breaks the one use that is correct — a fragment's own `--reverify` — and that use is why the flag exists | Rejected |
| Move #153 to the pull-request job alone | It already runs there and would have caught this. But a round that learns at the pull request learns after its fixes are written, and the handoff is where a round learns anything | Rejected — the job stays as it is; the guidance is what changes |
| Refuse a record whose **last** commit descends from the fix | A correct record is written with `open` cells and updated when the fixes land, so its last commit legitimately descends. That refusal fails every well-written record | Rejected — the **adding** commit is the distinguishing one |
| Check that a record carries what it says it verified | Named in #150's own comment as *state whether it is checkable before assuming it is*. A probe row naming a proposed fix with no fix in the file may or may not be machine-readable | **Phase 4's question, answered either way rather than assumed** |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `docs/review-handoff-protocol.md` and `skills/code-review/SKILL.md` name the two forms and what each is for — the unscoped read that says what a branch broke, the scoped write that keeps `--reverify` off somebody else's row | cases pinning both sentences, seen red with the prose stashed | `a942058` |
| 2 | `evidence_check.py` says which ledgers it did not read when `--ledger` narrowed it | a case on the output, seen red before the line exists | `93c8b89` |
| 3 | `chain_check.py` refuses a round record whose **adding** commit descends from a commit its own verdicts name as the fix, behind a fifth cutoff; `docs/review-chain-spec.md` gains the subsection | each refusal seen red at a named SHA; a case for the well-written record that must keep passing; the rebase caveat settled and written into the message or the spec | `55ae839` |
| 4 | Whether *the record carries what it says it verified* is checkable — **answered either way**, in the spec if it is not; the fragments | `evidence-check .` **unscoped**, `fold_ledger --check`, `unverified-check` | `9485fec` |
| 5 | Round 1's four 🟡 — the eight re-stamped ledger rows re-read and dated, the refusal's reach stated where the SHA is written, `added_on_branch` reading the LATEST add, and the skipped set folded by inode rather than by a spelling of the path | three cases seen red at `148bd10`; nineteen mutations across both checkers; `evidence-check .` **unscoped** | `b87ba49` |
| 6 | Round 2's five 🟡 and the sixth it handed back — the fix surface the ordering rule made provisional is now refused once a later round has opened the fixes; the zero-inode silence closed; and every remaining description of the old add-index corrected | two cases seen red at `47e6ebf`; thirteen mutations, none surviving; the branch's own two records run against the new arm | `c528161` |
| 7 | Round 3's eight 🟡 as four classes and two singletons — the declared limit widened to what actually escapes, the arm's key stated where a reader meets the refusal, the terminal `Fixes checked by` value put in the spec's table, and every re-stamped ledger row carrying what its re-read found | eighteen mutations across every decision this branch argues in prose, nine surviving and five of them closed here; nine cases written or widened and every one seen red; **575 cases green** across the seventeen suites that read the two checkers or the documents this phase edited, run at the committed tree rather than before it | `e94c3de` |
| 8 | Round 4's 🔴 and six 🟡 as four classes — the malformed cell that makes the branch red, all four recorded limits re-derived, the escape limit pinned in every copy that exists, and one rule for a record cell corrected in place | every parsed cell of all four records run through every checker that reads one; fourteen mutations, fourteen dead; four cases written or widened and every one seen red; `evidence_check.py .` **unscoped** still one drifted row — S8 alone, the row deferred to the owner | `73ee5a1` |
| 9 | Round 5's 🔴 1 and 🟡 2 as the repository owner answered them — the correction-trace rule phase 8 built is reverted whole, because it keys on a git history the release squash destroys, and issue #159 carries round 4's 🟡 7 instead | the release squash reproduced in a `--no-local` clone from `origin/release/v0.8.0` — five records at 1 commit each, six suites **152 passed**; `chain_check --baseline origin/release/v0.8.0` down to `round-5.md`'s honest mid-run pair; `evidence_check.py .` **unscoped** still one drifted row, S8 alone; `unverified-check` exit 0 | `cd7998e` |
| 10 | Round 7's 🔴 1 and three 🟡, written by the orchestrator on the owner's instruction rather than by a smith — the floor's count stops at a record whose verdicts closed on a fix as well as at one that reopened, because `Needs a fix` is the reviewer's answer and the verdict column is the fix surface's, and the two came apart when round 6's 🟡 were fixed over its `no`; the three reach-backs round 6 owed; the fragment paragraph naming R6 among the six | one case seen red against the old walk with the floor's own sentence, and this repository's own records red the moment `round-7.md` exists — `test_this_repositorys_own_round_records_pass_the_per_record_checks` red at `9bf9584`, green at `9efd314`; a direct pin on `wrote_fixes`; every earlier floor case green, three quiet rounds still refused; **309 passed** across the floor, surface, checker and document suites; ruff clean; `chain_check` down to `round-7.md`'s honest pair; the three documents that state the bound carrying the second stop | `9efd314` |
| 11 | Round 8's 🔴 and two 🟡, the orchestrator's again — the count rule's other three copies (the normative protocol and both `chain_check.py` docstrings) now name both stops, a case was written to pin all five carriers (round 9 found it live for the protocol alone, and phase 12 narrowed it to that), and `round-7.md`'s reach names `main` where it said `check_round` | the carrier case seen red on the protocol before the copies were corrected, then green; the prose, handoff, line-wrap and one-word suites **84 passed**; ruff clean on the two changed Python files; `chain_check` down to `round-8.md`'s honest pair with `round-7.md`'s `nobody` gone; the module AST-identical with docstrings stripped, so `Contract changes` is `none`; the three `stopping_floor` anchors re-read and re-stamped from a one-row scratch ledger, `evidence_check.py .` **unscoped** back to one drifted row, S8 alone | `cd4fec2` |
| 12 | Round 9's two 🔴 and four 🟡, the orchestrator's, as the owner shaped them — the carrier pin narrowed to the protocol, the one carrier where it was live, with a guard against an emptied tuple; the refusal message (the eighth copy of the count rule, the one a person reads) naming both stops and refusing the false way out; the spec's exits row and the skill's own paragraph, the seventh and eighth copies; and three records' claims about the pin corrected in place with the belief kept | the message case seen red against the old refusal, then green; the narrowed pin green with a non-empty guard; the floor, prose, doc and handoff suites **167 passed**; ruff clean on the three changed Python files; `chain_check` down to `round-9.md`'s honest pair; `stopping_floor` the one changed unit by AST, so `Contract changes` names its returned message; the five anchors it moved re-read and re-stamped from a scratch ledger, `evidence_check.py .` **unscoped** back to S8 alone; R12 lists the eight carriers by coordinate | `35def0f` |

Phase 1 before 2 and 3, and phase 3's spec subsection in the same phase as its
refusal — the two orderings this repository has now learned four times between
them.

**This branch's own chain runs under phase 1's rule before phase 1 ships**: every round is handed the unscoped read, because a guidance change binds sessions after the release and the rounds in front of it are not protected by it.

## Operational impact

- **No migration, no environment variable, no dependency.**
- **A round record written late fails a pull request**, bounded by work-item id — the shape five cutoffs now take.
- **A narrowed `evidence-check` gains a line of output.** Nothing parses that output; the pull-request job reads the exit code and the totals line.
- **Failure direction: blocks more**, for the same trade as the four before it — with two exceptions this branch's rounds forced, each named where it lives. The pending fix-surface arm takes **allow** for a reason it cannot read (phase 6, `overview.md`'s divergence table), and the floor's count now stops at a record that wrote fixes as well as at one that reopened (phase 10), which is **allow** by one record in one sequence. Both are the cheaper mistake for the same reason: the other direction refused an honest record, and a checker satisfiable only by a false record is this work item's own subject.
- **Prompt budget: zero.**
