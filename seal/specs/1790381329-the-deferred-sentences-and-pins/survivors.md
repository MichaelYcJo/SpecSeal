# 1790381329-the-deferred-sentences-and-pins — survivors

`survivor-check --range origin/release/v0.15.5...HEAD`, run at `ed9635af`
after the build's seven phases, reported two places. Both were read and
neither is a sentence this work item made false.

| Path | Quote | Grounds |
|---|---|---|
| `docs/release-checklist.md` | `unverified_check` resolves its baseline to `git merge-base <the base ref> HEAD`, so a work item squashed into the release branch after a sibling forked is not that sibling's removal | Step 0 of the release checklist. It shares two phrases with the `--baseline` help sentence phase 3 rewrote (#612), which placed the fork point in CI. This one places nothing: a sibling squashed after the branch was cut is not its removal on a branch checkout, where the merge base is the fork point, or at CI's merge ref, where HEAD holds the squash too. `spec.md` §*Out of scope* read it the same way, and `test_the_documents_state_the_merge_base_footing` holds it to the merge base and not to the tip |
| `seal/specs/1790381329-the-deferred-sentences-and-pins/spec.md` | *A `%VAR%` in that part is expanded first, as `cmd.exe` expands it before it reads the name* | The frame's #616 table, column *What it says now*: a quote of `templates/config.md` as it stood when the frame read the tree, beside the column saying what it must say. Phase 6 made the change that column asks for. The spec is the contract this work item was built against, and a quote of the state it changed is not an instruction |
