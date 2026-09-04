# 1788472135-the-run-outlives-its-last-finding — phase 4

<!-- seal/specs/1788472135-the-run-outlives-its-last-finding/phases/phase-4.md — what
this phase of the build did, written by the implementer when the phase closes. -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 2b547e2 |

## What this phase was asked

Build phase 4, the last one: two fragments and the closing of the memo.

- `changelog.md`, written for whoever reads `CHANGELOG.md` six months from now
  rather than for a reviewer of this diff, since
  `.github/scripts/gather_changelog.py` concatenates it at the release with no
  branch context around it. The two issue numbers are #110 and #117, and what
  changed for a reader is that a review run has a floor as well as a ceiling
  and a fix pass has a bound on what it may create, both enforced at the pull
  request for work items begun on or after `1788472135`.
- `seal/ledger/1788472135-the-run-outlives-its-last-finding.md`. Phase 3's
  record names the anchorable units; **judge which claims are worth a row
  rather than writing one per function**, and where the honest answer is "no
  row", write that judgment down rather than padding the fragment — #109 did
  exactly this and recorded it. Hashes come from `evidence-check`, not from a
  hand.
- The memo: close what phase 4 closes, leave the rest open with an answerer
  named, and fill the `📋 implement applied` block's `evidence:` and
  `verified:` lines. Three items were named to leave open: the broad gate,
  whether a real `round-N.md` satisfies the two new rows, and a `(depth 1)`
  that is really second-level.

Verification the phase owes: `fold_ledger.py --check`, `evidence-check` over
the new rows, and `bin/unverified-check` green. The single broad run is
explicitly still not this segment's.

## What this phase found

**The branch left ten drifted anchors in `seal/ledger.md`, and nothing in the
phase's own checklist would have found them.** `fold_ledger.py --check` and
`bin/unverified-check` were both green before this phase wrote anything;
`evidence-check .` was not. Ten rows written by four earlier work items cite
regions this branch edited — `chain_check.py`'s `main` and `fix_surface`, the
constants block, `templates/sdd-round.md`'s field table,
`skills/code-review/SKILL.md`'s verifying-round section,
`docs/review-chain-spec.md`'s review arm, `templates/config.md` twice,
`tests/test_the_pull_request_language_is_the_repositorys.py`'s
`ROUND_RECORD_FIELDS`, and `agents/smith.md`'s `## Phases`. A tree built from
the branch's base commit `10b0017` reports **451 ok, 0 drifted**, so all ten
are this branch's. Drift is CI's warning rather than its failing exit
(`.github/workflows/test.yml`'s ledger job exits only at 2), which is why
three phases could pass their own checks without meeting it.

Fifteen rows cite those ten anchors. Each anchor's diff was read before
anything was re-dated, and each claim still holds: `checked_by` is still
per-record (`main` gained `enumerate` and a `stopping_floor` call, nothing
else), `fix_surface`'s reach walk and separator refusal are untouched under
the new depth walk, `templates/config.md`'s change is four additions inside
one bullet, and `agents/smith.md`'s mutation-testing rule — the whole subject
of row L5 — is where it was.

**Two rows were left DRIFTED on purpose, and that is a decision rather than an
omission.** Re-verifying rewrites a row's hash, which asserts that somebody
read the region and the claim holds. Two claims do not.

| The row | What is wrong | What was done |
|---|---|---|
| *r3 3 / r4 2* under `## 0.5.0` — *`templates/sdd-round.md` still carries the eleven fields `ROUND_RECORD_FIELDS` expects of it* | this branch made the list twelve | left standing, hash restored to `53859758`; **F7 of this work item's fragment carries the corrected claim** |
| *S8* under `## 0.5.0` — *`templates/config.md` is one `\| Item \| Value \|` table whose first row is `Pull request language` → `English`* | its own work item renamed that row to `Commit and pull request language`, before this branch existed | left standing, hash restored to `45edf260`; named in the memo with an answerer |

The first was **not** deferred to an issue, which the repository's own rule
forbids for a defect a branch caused: the true claim is written now, in this
branch's own fragment, which is where `CLAUDE.md` says a work item's claims
go. What was declined is rewriting another work item's row in a released
section — that row's two other sentences are a dated census *of eleven
entries* and would become false if the number were changed under them. So the
count moves in the new row and the old row keeps pointing at itself through
the checker's own word for *re-read me*.

**Seven rows, and the judgment about the rest is in the fragment rather than
here.** Phase 3 named twelve anchorable units. Six earned rows — the two
grandfatherings that are not one (F1), the two cutoffs that are deliberately
separate and a case that pins them together anyway (F2), and four narrow
readings that only mutation found (F3, F4, F6) or that exist because a
derivation reads constants rather than literals (F5). `listed` earned none: it
joins names for a message and nothing about it is a claim. Neither did the
prose in the six documents, because
`tests/test_the_run_stops_at_the_last_finding.py` and
`tests/test_a_fix_pass_may_add_a_unit.py` already assert every sentence in the
file it belongs in — the judgment the sibling work item 1788445862 made, for
the same reason. Both judgments are written into the fragment's own header
comment, where a reader who opens the fragment meets them.

**`fold_ledger.py --check` is red on this branch and that is the correct
state.** It reports the fragment as never folded, which is what an in-flight
work item looks like; `.github/workflows/hygiene.yml:87` skips the step unless
the base branch is `main`, and this branch targets `release/v0.8.0`. What
proves the fragment is the shape the release gathers is
`fold_ledger.py --version 0.8.0 --dry-run`, which moves all seven rows, writes
nothing, and exits 0. `gather_changelog.py --check` is red for the same reason
and skipped by the same condition.

**One instruction in the task was inverted, in the same direction phase 1's
was.** It named `fold_ledger.py --check` as the check to get green; the check
that goes green is `bin/unverified-check`, and `--check` on either release
script is red by design until the release. The evidence the instruction wanted
exists, in the dry run.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | — |
