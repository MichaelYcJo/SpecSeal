# 1791270165 — handoff

Written 2026-10-07 by the orchestrating session (Opus 5.5) at the end of the second machine's segment of the 0.20.0 run. It replaces the 2026-10-06 handoff. Read this first.

## Where it stands

- **Built, reviewed and sealed.** Phases 1, 3, 4a, 4b and 5 are closed (phase 2 dropped by the owner's Q10 (b)). Review ran three rounds, one reopening, `chain: capped`; round 3's one 🟡 was deferred to #847 and then fixed on this branch at bc2d8b82. The release branch (with #831, 275a7ce0) is merged in at 73c765c9.
- **Sealed at bc2d8b82 against 275a7ce0** (12967 passed, 87 skipped, every arm exit 0); the cell is committed at 52f5fe18 and pushed.
- Draft PR #845 into `release/v0.20.0`, labelled `chain: capped`, body updated (Closes #841, #847). Its checks at 52f5fe18 were still running when this session stopped (lint, ledger, arm-check, ubuntu and two Windows shards had passed).
- Result: the Windows leg's slowest shard is 10–10.6 min (was 33–36 on this branch, 37–40 on 0.19.0's PRs); macOS, 12–21 min, is now the longest leg. Every leg has a timeout (15 / 35 / 20 per shard) and every case a 90 s ceiling (`SPECSEAL_CASE_CEILING_S` raises it on a busy machine).

## Next

1. `gh pr checks 845`: read **every** workflow, not only `test` (`hygiene` was red for three pushes on this branch and nobody looked). All green at 52f5fe18 → `gh pr ready 845`, wait for the re-run, then squash-merge into `release/v0.20.0`. The owner pre-approved squash merges of green, sealed PRs into the release branch (not main, not tags). Subject: the PR title plus ` (#845)`.
2. That merge unblocks #826 phase 3 (its W4).
