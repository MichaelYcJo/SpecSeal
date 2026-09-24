# 1790260565-a-ledger-row-carries-two-readings-in-one — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | e79665da |
| Ran by | specseal:smith on Opus 5.5 |

## What this phase was asked

#569 ⬜ 2: the paragraph in `docs/round-record-spec.md` §*The fix surface*
that begins "Its direction is `allow`" opens with the reviewer's sentence,
and the rest of the paragraph stays as it is. A new case in
`tests/test_a_record_precedes_the_fixes_it_commissions.py` asserts that the
paragraph names `chain_check.py`'s direction and not
`docs/review-chain-spec.md` §*The reopening*, and that
`says_not_yet.__doc__` still says every other refusal treats what it cannot
read as failing. The case was to be seen red against the current document
first. The fragment gains one row, R4 (`seal/releases/0.9.1.md`) is re-read
if its anchor drifts, and the changelog fragment is completed.

## What this phase found

- **Seen red (§15)** against the paragraph as it stood: *the spec's
  exception does not name the direction chain_check.py's other refusals
  take*. It was green after the sentence changed.
- **Mutated.** The document and `chain_check.py` were restored from bytes
  read before the first write, with `tests/__pycache__` cleared between
  runs. Each of three mutations turned the case red: §*The reopening* put
  back beside the new phrase, the new referent removed, and the docstring's
  "Every other refusal here" sentence reworded. `chain_check.py` was written
  only by the probe and restored byte for byte, and the tree was clean
  after.
- **R4 drifted, as the plan predicted, and nothing else did.** Its last note
  from 1790208643's round-1 fix pass describes the sentence as it stood
  then, naming §*The reopening*. That note records a past reading, so it is
  left as written, and a `Re-read 2026-09-25` note after it says what the
  sentence names now. `--reverify` over `0.9.1.md` changed R4 alone. R7
  (`0.8.0.md`) states the exception the code's way and did not drift.
- **`survivor-check` over the whole branch reported what phase 1 left, and
  the work item now has a `survivors.md`.** Over phase 4's own range it
  reported two places: the spec and R4's older note, both quoting the old
  sentence to say what it was. Over the whole branch it also reported the
  openings phase 1 kept once in S4 and G5, and the texts they describe. It
  found twelve from `0f5f537b` and fourteen from the base, because the sweep
  splits sentences differently per range. Each has a row with a quote and
  grounds. With the file, both ranges exit 0: "every survivor is excused by
  a row above (14)". The hygiene workflow runs this sweep on a pull request
  into a release branch and fails it, so without the file the pull request
  would have been refused.
- **The one skip in these runs is not this branch's.**
  `tests/test_the_reopening_is_one.py:574` skips because
  `origin/release/v0.8.1` is not fetched in this worktree.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the spec's "the `blocks more` direction `docs/review-chain-spec.md` §*The reopening* states" | the reviewer's sentence in the same paragraph, naming the direction every other refusal in `chain_check.py` takes |
