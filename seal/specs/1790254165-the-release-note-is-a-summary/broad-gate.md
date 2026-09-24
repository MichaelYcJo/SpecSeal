# 1790254165-the-release-note-is-a-summary — broad gate

<!-- The `Broad gate` cell, for a work item that ran no review
rounds. Where rounds ran the same cell lives on the last
`rounds/round-N.md`; this file is the other home, and it holds that
row and nothing else.

Written by `round-record seal`, which picks the home from what
exists, and read by `chain_check.py` at the pull request. The cell
records the commit the run happened at and the base it was compared
against, so an edit after the run spends it — which is the whole of
what a broad-gate cell asserts, and none of it depends on a round
having run. One entry per run, newest first: a run at a new commit,
or at this one against another base, is written in front and the
earlier one stays behind it as `earlier run`; a run the newest entry
already records — the same commit against the same base — replaces
it. The reader takes the first SHA as the run. -->

| Field | Value |
|---|---|
| Broad gate | 07988c2c against 580ef6bc |
