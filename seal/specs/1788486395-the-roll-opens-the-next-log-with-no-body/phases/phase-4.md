# 1788486395-the-roll-opens-the-next-log-with-no-body — phase 4

<!-- seal/specs/1788486395-the-roll-opens-the-next-log-with-no-body/phases/phase-4.md
— what this phase of the build did, written by the implementer when the phase
closes. -->

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | 5e76246 |

## What this phase was asked

- Create the `flow-baseline` label in this repository and apply it to `#51`.
- The changelog fragment, written for whoever reads `CHANGELOG.md` in six
  months rather than for a reviewer of this diff.
- The ledger fragment, content anchors, `path#major@hash`, computed with
  `evidence-check`. Judge which claims are worth a row; where the honest answer
  is "no row", write that judgment into `overview.md`.
- `overview.md`, opened at the first unverified item.

## What this phase found

**The search-index lag `#109` recorded reproduced on the first read, which is
what makes the whole mechanism executed rather than read.**
`gh issue edit 51 --add-label flow-baseline` returned 0, and the very next
`gh issue list --label flow-baseline --state open --json number,title`
returned `[]` while `gh issue view 51 --json labels` in the same breath showed
the label applied. A second list, one tool round-trip later, returned
`[{"number":51,...}]`. That is the exact behaviour this script's docstring
documents for `flow-measurement`, observed for `flow-baseline` on the day it
was created. **What it means for `find_baseline_issue`:** a lag there costs
the body's ledger clause, not the release, which is already the designed
failure — but it is a real path, not a theoretical one, and nothing retries it.

**`evidence-check --reverify` does take a selector, just not the one the spawn
prompt looked for.** `--ledger GLOB` bypasses ledger discovery entirely, so
`bin/evidence-check --ledger seal/ledger/1788486395-*.md --reverify .` stamped
this work item's twelve anchors and opened no other file. `seal/ledger.md`'s S8
row still carries `45edf260`, checked by grep after the run. The hand-repair
the prompt braced for was not needed and is not a step anyone has to take.

**`seal/ledger.md`'s one DRIFTED row is S8, which is already deferred.** The
check reports `templates/config.md#"# Repository config"` as content-changed;
opening it, that is `seal/ledger.md:517`, hash `45edf260`, and work item
1788472135's overview already carries it with the repository owner named — the
claim is false, and re-stamping it is not the repair. `git diff 9f22d67` is
empty for both `templates/config.md` and `seal/ledger.md`, so nothing here
touched it, and the `--ledger` scoping above is what kept this branch's
`--reverify` off it. It is closed in this work item's *Not verified* rather
than left open, because what it needed was opening rather than answering.

**One thing that deferral says is no longer true.** Its text reads
*"`evidence-check --reverify` takes no row selector: one run on this tree
re-stamps this false claim along with everything else"*, and it was written
before anyone tried `--ledger`. The selector is per-ledger rather than per-row,
which is enough — a work item's rows live in a file of their own, so nobody
has to restore S8 by hand to stamp their own. The sentence belongs to another
work item's committed record and was left alone; it is named here and in the
handover instead.

**Neither release-time gathering command is due on this branch, and both were
run to see so.** `gather_changelog.py --check` exits 1 naming two ungathered
fragments — this work item's and 1788472135's — which is the correct state for
a branch merging into `release/v0.8.0`; the hygiene workflow runs that check on
pull requests into `main`, where the gather is what answers it.
`fold_ledger.py --version 0.8.0 --dry-run` exits 0 and prints this fragment
under a 0.8.0 heading, so the fold has nothing to trip on.

**Five rows, and the judgment for the other side is in `overview.md`.** The
four in the roll script are each a narrow reading a later tidy-up would widen
in good faith. F5 is the odd one: it is the only case in
`tests/test_a_segment_feeds_the_flow_log.py` that reads for an **absence**, so
it is the only one a section could satisfy while also saying something it must
not. Phase 1's prose itself gets no row — twelve cases already read it sentence
by sentence, and a coordinate per sentence would be an inventory of the diff.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/flow.md`'s `#110 + #117` tick — carried into `5e76246` by a `git add -A`, declared nowhere, and taken back out by round 1's fix pass | PR #144, which the orchestrator opened for exactly that one-character change on `docs/the-flow-ticks-110-and-117` before this work item started. Two open pull requests carrying it is a conflict waiting at whichever merges second. `git diff f187b39 -- docs/flow.md` is now empty, so this branch touches the file not at all |
