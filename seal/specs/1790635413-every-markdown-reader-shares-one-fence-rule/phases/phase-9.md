# 1790635413-every-markdown-reader-shares-one-fence-rule — phase 9

| Field | Value |
|---|---|
| Phase | 9 |
| Commit | 028eee43 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

`plan.md` phase 9, which the orchestrating session added once `questions.md`
Q5 was answered (a). Round 1's 🟡 1 and 🟡 2: `gather_changelog.py` and
`fold_ledger.py` write a fragment verbatim, so a fenced block or an HTML
comment the fragment leaves open puts every later marker on a line their own
`live_markers` cannot see. The builder chooses between refusing such a
fragment before anything is written and closing what it left open. Either
way, the failure must be loud before a write, never a doubled entry after
one. The phase must also:

- show the report's two drafted shapes red at `a06f23b2`;
- run `bin/test` over the gather, fold and live-marker modules;
- kill one mutant per changed unit;
- say how the failure reaches a person at release time, because
  `.github/scripts/` is release automation.

## What this phase found

- **Refuse, not close. Grounds:**
  - A fold is a move whose promise is byte for byte, and a gathered entry is
    prose that ships in the release note. Closing a block would ship text
    nobody wrote.
  - Closing would also have to guess where the block was meant to end: at
    the fragment's end, or somewhere earlier.
  - One of the two drafted shapes is a bare comment opener in prose. That
    opener was never meant to open anything, so the right repair is the
    author's.
  - The refusal needs no second rule. `leaves_open` asks `live_lines` of the
    exact shape each script writes: the body, a blank line, then a marker.
- **Both refusals stand where the scripts' other refusals stand.** They come
  before anything is written or printed, with or without `--dry-run`, and
  name each fragment.
  - The gather's sits beside the #586 refusal, after it, and reads only the
    fragments this run would gather. A fragment already in the file cannot
    be un-shipped.
  - The fold's sits after the open-row guard and the empty-fragments exit,
    and reads every fragment. A second fold for the version appends below
    everything, so even the last fragment of a release can hide a later
    marker.
- **How the failure reaches a person at release time.** Release preparation
  runs `gather_changelog.py --version X.Y.Z` and
  `fold_ledger.py --version X.Y.Z` in one commit (`docs/branch-and-release.md`).
  - Each refusal exits 1, prints the fragment's path, says to close the block
    in a pull request into the release branch and run again, and ends
    `Nothing was written` / `nothing folded: … untouched`.
  - The person preparing the release sees that on the step's own output,
    before any file changes. The tree is exactly as it was, so the repair
    is one pull request and a re-run.
  - If the step is skipped or its exit ignored, the fragment stays
    ungathered or unfolded. The hygiene workflow's `--check`, which runs on
    the release pull request into `main`, then names it and fails the pull
    request.
  - Nothing catches the fragment at its own pull request. That is the same
    gap #586's refusal has (its `questions.md` Q3), and it is not built here.
- **Seen red at `a06f23b2`.** The scripts are unchanged from `a06f23b2` to
  `7da62911`. Eight cases failed there, each exiting 0 where 1 is asserted:
  - four for the gather: fence or comment, with or without `--dry-run`;
  - four for the fold: the same four combinations.

  A ninth case, a fragment that closes both a fence and a comment, passed
  there. It passes after the fix too, so the refusal cannot pass by refusing
  everything.
- **Mutants, each alone and each killed:**

  | Mutant | Red |
  |---|---|
  | The gather's `leaves_open` inverted | 27 |
  | The gather's refusal skipped under `--dry-run` | 2 |
  | The fold's refusal skipped under `--dry-run` | 2 |
  | The fold's `leaves_open` asking fences only (`fence_spans`) instead of `live_lines` | 2, the comment shapes |

  After each, the file was restored from the commit.
- **This tree is not refused.** `gather_changelog.py --version 0.16.0
  --dry-run` and `fold_ledger.py --version 0.16.0 --dry-run` both exit 0 over
  this branch. That covers its own changelog and ledger fragments, whose
  prose quotes fences inside code spans.
- **One slip, recovered.** Fourteen re-read notes failed to land at first,
  because their Edit calls came before the files were read, and a
  `--reverify` ran between the failure and the retry. So the drifted rows
  were re-stamped once before their notes existed. The notes were then
  written and the rows re-stamped again. The final tree carries each note
  beside its hash, and `evidence-check --strict` reads 2704 ok, 0 drifted.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `demote`'s sentence that a block which never closes "runs to the end, as it did" | the same docstring, which now says `main` refuses such a fragment before it reaches `demote`; `seal/ledger/…` F1 is corrected to match |
