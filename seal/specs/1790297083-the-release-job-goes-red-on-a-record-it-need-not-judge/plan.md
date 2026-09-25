# Implementation Plan: how chain_check reads a record (#598 instances 1 and 4, #529)

<!-- seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/plan.md -->

Approved 2026-09-25 by the orchestrating session under the owner's `automation` answer, when `smith` was spawned.

## Summary

The work has three code slices and one records slice, all in
`skills/code-review/scripts/chain_check.py` and the documents that describe
it:

1. `added_on_branch` finds the latest add across a merge and under a skewed
   clock (#529).
2. A record restored byte-for-byte from the base's history is not this pull
   request's claim, in both arms that key on the pull request's own add
   (#598 instance 1).
3. `Pass` beside `nobody` on the last record prints in a draft and fails at
   ready (#598 instance 4).
4. The ledger and changelog fragments, and every drifted row re-read.

None of them adds a refusal. Slice 1 makes an existing rule hold, and slices
2 and 3 relax a refusal where a document already says the state is not a
failure.

## Technical context

Read 2026-09-25 at `59c0caf0`:

- `chain_check.py#added_on_branch` runs `git log --diff-filter=A
  --format=%H <base>..HEAD -- <rel>` and takes the first line. Its docstring
  and `docs/review-chain-spec.md` both say the first line is the LATEST add.
  The measurement in `spec.md` Scope 1 shows two ways that fails: history
  simplification (S1) and date order (S7).
- `chain_check.py#main` decides reachability with `refs =
  target_refs(reader, root, declared) if last in touched else None`. Here
  `touched` is `changed(root, args.baseline)`, meaning `base...HEAD` by
  name-status. A directory re-added by the pull request is `A` in that diff
  whatever its content. `main` already computes `fork =
  reader.merge_base(root, args.baseline)` before the loop, and the restoration
  predicate reads from `fork`.
- `chain_check.py#written_late` asks `added_on_branch(root, base, rel)` and
  returns no claim when it is None. The restoration answer joins that exit.
- `chain_check.py#checked_by` raises the `Pass`-beside-`nobody` error under
  `last and pass_checked(lines) and began >= STRICT_FROM`. It has no `strict`
  parameter today. `main` computes `strict = state != "draft"` and passes it
  to `check_round` and `broad_gate` only.
- The `unknown` state (no payload, one that will not parse, a non-boolean
  `draft`) is judged as ready. Slice 3 inherits that and adds no path around
  it.
- `round_record.py close` runs the check with no payload, so it keeps
  reporting the refusal after ticking `Pass`. That output is what makes the
  verifying round mandatory at the keyboard, and slice 3 leaves it unchanged
  (scenario C4).
- **Work item C (#590) edits this file in parallel.** C owns `load` and the
  `try`/`except` around the two `load(...)` calls at the top of `main`. Do not
  touch either. A's edits in `main` are the `refs =` line, the item's printed
  line, and the arguments to `checked_by` and `written_late`, all further
  down the function.
- Tests are run narrowly with `uvx --with pytest python3 -m pytest
  tests/<file> -q` (`CONTRIBUTING.md`). The suite, lint and typecheck are the
  sealer's, once, after the rounds settle (contract §2).

**What breaks in six months.**

- *Slice 2.* A record restored from the base's history is taken on its
  original pull request's word about where its commits are. If a repository
  ever retires a record that was never reviewed (a record merged past a red
  check), a restore brings it back without re-asking. That is the same trust
  an untouched record already gets, so it is no new hole.
- *Slice 3.* A draft that is never marked ready never meets the refusal, and
  neither does a draft that merges without passing through ready. The first
  state reaches no branch. The second is impossible in this repository,
  because `main` and `release/*` both require a pull request and a draft
  cannot merge. In another repository the same hole already exists for the
  missing-record arm (#296) and for an unchecked `Pass`.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #529 with `--full-history` alone (#525's fix, copied) | S7: a side branch whose commits carry an older committer date than the early add lists the early add first, and `found[0]` takes it | Rejected. Measured red in framing |
| #529 with `--full-history --topo-order` | Two adds on parallel lines that are not ancestor-related get an arbitrary order. That needs two branches each adding the same path, and they would conflict at the merge unless the contents match. Nothing in this repository's flow produces it | **Chosen** |
| #529 with `--full-history --simplify-merges` | Also correct on S1 through S7, but it orders by date. It does the right thing on S7 by pruning, not by ordering | Rejected. `--topo-order` states the property the docstring relies on |
| #529 by choosing the earliest add of the current content | Contradicts `docs/review-chain-spec.md`'s *latest add* row. It is also the direction #529 calls unsafe | Rejected. That is a design change, not a patch |
| Instance 1: compare against `main` by name (the issue's wording) | Assumes the release's base is called `main`. A repository whose base has another name, or a pull request into `main` itself, gets no answer or the wrong one | Rejected |
| Instance 1: "the blob the path held LAST in the base's history" (only the version that was retired) | A restore of an earlier version of a record is refused on reachability, although that version was also added, and judged, by an earlier pull request. It also needs an ordered history walk where the chosen predicate needs one `--find-object` | Rejected. It is narrower for no documented reason |
| Instance 1: "any blob this path held in the merge base's history", by `git log --full-history --find-object=<blob> <fork> -- <rel>` | A record reverted by the pull request to an older committed version makes no reachability claim. That version's commits were claimed when it was first added | **Chosen**. Measured on #597's real records and on S4 and S5 |
| Instance 1: drop a restored `routing.md` from `declarations` | A restored item would be read for nothing, which is quieter than the documented *every requirement except reachability* | Rejected |
| Instance 4: leave it red and keep the orchestration sentence *"that window is expected"* | Six pull requests red on one chain's ordinary step. A check red for following the document beside it is a check people learn to skip (#296's grounds) | Rejected |
| Instance 4: print at every stage (drop the refusal) | Overturns the owner's answer to Q1 of `1788212517` | Rejected |
| Instance 4: move it earlier (refuse at `close`) | `close` already prints the refusal locally. Refusing there would stop the session writing the very record the verifying round needs | Rejected |
| Instance 4: print in a draft, fail at ready or unknown | A draft that never goes ready never meets it. That is the same trade #296 took for the missing record | **Chosen** |

## Phases

Each phase ends with its cases seen red first (§15: against the old code, or
with the pinned sentence deleted), then green, then committed. The
documentation for a behaviour lands in the same commit as the behaviour
(§14).

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | #529. `added_on_branch` passes `--full-history --topo-order`. Its docstring gives the two reasons (simplification, S1; date order, S7) and the measured answer that a merge is never an `A`. The `docs/review-chain-spec.md` delete and re-add row says the reading holds across a merge and a skewed clock. Cases A1 and A2, plus A3 if no existing case builds a merge | `uvx --with pytest python3 -m pytest tests/test_a_record_precedes_the_fixes_it_commissions.py -q`. A1 red against the current line and A2 red with `--full-history` alone, both shown in the phase record | 66d39e30 |
| 2 | #598 instance 1. One restoration predicate, asked by the reachability decision in `main` and by `written_late`. The restored item's printed line names the commit. Docstrings, the `docs/commit-review-gate-spec.md` row, and a new `docs/review-chain-spec.md` row in the §*When the record was written* table. The *what it costs* sentence of the delete and re-add row narrowed to a restore within the branch. Cases B1 to B4 | `uvx --with pytest python3 -m pytest tests/test_chain_check_at_the_pull_request.py tests/test_a_record_precedes_the_fixes_it_commissions.py tests/test_docs_line_wrap.py tests/test_a_folded_statement_names_what_enforces_it.py -q`. B1 and B4 red on the pre-phase code | |
| 3 | #598 instance 4. `checked_by` takes `strict`, and in a draft the last-record `Pass`-beside-`nobody` refusal becomes a notice naming the verifying round and *Ready for review*. Every other refusal in the function is unchanged. Also: the module and function docstrings, `docs/round-record-spec.md` §*`Fixes checked by`* (sentence, table row, `Enforced by:`), `docs/review-chain-spec.md` §*Two records*, and the replacement for `skills/code-review/orchestration.md`'s *"It is red once more …"* sentence with its pin in `tests/test_the_rules_have_one_owner.py`. Cases C1 to C3 | `uvx --with pytest python3 -m pytest tests/test_the_last_rounds_fixes_are_checked.py tests/test_the_rules_have_one_owner.py tests/test_the_fixes_close_the_record.py tests/test_docs_line_wrap.py tests/test_a_folded_statement_names_what_enforces_it.py -q`. C1 red on the pre-phase code, and the orchestration pin red with the new sentence deleted | |
| 4 | Records. `seal/ledger/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge.md` with one row per new claim: the two flags and why, the restoration predicate and its two callers, and the draft arm. Every row `evidence_check.py` reports DRIFTED because of phases 1 to 3 is re-read against the edit and re-stamped in its own file with a dated note, and its claim is corrected in place where the edit made it false. `seal/specs/…/changelog.md` written | `python3 skills/evidence-check/scripts/evidence_check.py` (the ledger tool, narrow) reports nothing DRIFTED or BROKEN that this branch caused. `uvx --with pytest python3 -m pytest tests/test_a_row_points_by_content.py -q` | |

Phase 4 comes last on purpose. Phases 2 and 3 both edit `main`, so
re-stamping `main`'s rows after each would stamp them twice. The rows are
drafted as each phase settles and written in one pass here, before the draft
pull request opens. So the first review round sees the ledger.

What each phase discovers, and what the next needs, goes into
`phases/phase-N.md` from `templates/sdd-phase.md` when the phase closes.

## Operational impact

- No new dependency, env var or migration. The only git features used are
  `--full-history`, `--topo-order` and `--find-object`. Each was measured on
  git 2.54.0. `--find-object` needs git 2.16 or later.
- The check's output changes in two places people read: the restored item's
  line and the draft notice. Both are pinned.
- A pull request that restores a retired work item's directory (as #597 did)
  stops going red on reachability. One that edits the restored record still
  goes red.
- A draft pull request in the window between `close` and the verifying
  round's record stops being red. Pressing *Ready for review* is where the
  refusal now lands.
- **Merge order with work item C:** A squashes first, and C merges the
  release branch in. If both branches re-stamped a `chain_check.py#main` row,
  the ledger conflict is resolved hunk by hunk (`CLAUDE.md`, the ledger
  paragraph), with `evidence_check.py` run after the resolution.
