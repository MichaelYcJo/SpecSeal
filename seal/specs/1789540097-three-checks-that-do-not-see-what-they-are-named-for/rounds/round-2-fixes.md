## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 6 | fixed | `64f36eee` — a hard-wrapped spelling joins the tuple the case already walks, which is the shape every file the sweep reads actually has. Re-measured after the fix pass stalled: dropping the flattening from `batch_instructions` is **1 failed, 50 passed** where round 2 measured exit 0, 51 passed |
| 7 | answered | `64f36eee` for the half that closes, and grounds for the half that does not. The sweep now reports what it read — the definition names and their sizes — and asserts both, so the read and the loop are held: truncating the read to ten bytes is **1 failed** and emptying the loop's iterable is **1 failed**, each where round 2 measured exit 0. What stays open is the **call**: `batch_instructions("")` passes something other than what was read, and observing that needs a walk driven by a planted definition file. That is mechanism a fix pass may not add, and `CONTRIBUTING.md` asks a separate argument for a change to what the suite guards. Recorded in `overview.md` §*Not verified* with an answerer |
