# 1788749195-the-record-drops-the-fix-and-a-pipe-truncates-the-row — routing

<!-- seal/specs/<unix-epoch-seconds>-<slug>/routing.md — the answer given before the
first edit, in the batch the `implement` skill collects (§1). -->

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Implementation | smith |
| Branch | fix/187-189-the-record-drops-the-fix-and-a-pipe-truncates-the-row |

Answered 2026-09-07 by the owner, before the first edit — the same batch that
answered 0.9.0's first work item, carried forward for the release.

## Why this way

Both tickets change what `round_record.py` writes into a file the next segment
opens instead of the report, and #187 names three candidate shapes without
choosing between them. Which shape a record takes is a judgement a reviewer has
to make rather than a formatter, and the branch immediately before this one is
the evidence: it hit #187 five times and worked around it by hand every time.
