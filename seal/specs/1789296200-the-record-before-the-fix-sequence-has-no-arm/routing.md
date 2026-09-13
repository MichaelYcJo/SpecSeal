# 1789296200-the-record-before-the-fix-sequence-has-no-arm — routing

| Axis | Answer |
|---|---|
| Review | through the review chain |
| Destination | open the pull request |
| Planning | framer |
| Implementation | smith |
| Branch | feat/345-the-record-before-the-fix-sequence-has-no-arm |

Answered 2026-09-13 by the owner, before the first edit.

## Why this way

Review was not an open axis: #345 changes a gate's verdict and when it is
delivered, so `CONTRIBUTING.md` §*What a change to a gate must carry* forces the
chain. The framer draws the frame because the issue leaves the placement open.
The owner answered implementation and destination in one batch with the other
two work items of 0.11.3.

**A coordinate in the sentence this paragraph replaced was wrong, and it is
corrected here rather than quietly dropped.** It read *`round_record.py`'s
`written_late` refusal*. `written_late` is in
`skills/code-review/scripts/chain_check.py`, and three places said otherwise —
issue #345's body, this file, and the prompt that spawned the framer. The
framer opened the coordinate instead of building on it (contract §5), which is
also why this work item touches two scripts rather than one.
