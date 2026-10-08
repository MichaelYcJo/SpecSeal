## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `23f22eb4` — the value stays `1791384163`, right for the release the owner scoped on 2026-10-08 (the eleven framed items plus #834's build, all below it); `NOTES_FROM`'s comment, the owner file's sentence, the test's constant and the ledger's N2 now say what it assumes — no item of that release framed after the batch — and that whoever frames one moves the cutoff past its own id in the same change. The far-future value was not taken: it would switch the rule off for every item framed after the release ships, which is the case the rule is for |
| 2 | answered | corrected at `23f22eb4` — the changelog fragment names the eleven items framed with this one as before the cutoff, and says a later one moves it |
| 3 | answered | cleared by round-2.md being the last record, as the finding says: at `b0e52bb2`, executed, `chain_check.py --baseline origin/release/v0.21.0` names nothing on round-1.md, judged ready or draft (draft exit 0); no edit taken |
