# 1791270164 — handoff

Written 2026-10-07 by the orchestrating session (Opus 5.5) at the end of the second machine's segment of the 0.20.0 run. It replaces the 2026-10-06 handoff. Read this first, then `plan.md` (the reframe paragraph and Phases) and `phases/phase-2.md`.

## Where it stands

- **Phase 1 closed** at 88070eac (smith on Opus 5.5 on this machine; the red case was the interim ring shrinking the message, not the disc width).
- **The owner answered Q1 on 2026-10-06**, after judging renders in their own terminal (`! cat <file>.ans`): the mark is **§** (Georgia Bold, 820 units tall), drawn by the rendering they chose ("D": a 6×6 area average per half-block pixel in linear light, the mark in `LILY_LIGHT` with a 0.7-pixel shadow, coverage tightened by a smoothstep, grid fit (0, +0.375) × 1.04, a continuously lit rim, the disc edge blended into the parchment on the sheet and hard off it), the disc **24 cells across** at the default rung, **pressed over the sheet's lower-right corner** (#717's shape). They saw 20 cells and sextant characters break the mark. The framer folded this in at b7a13d47; every point rule and the `d` string are in `spec.md`.
- **Phase 2 closed** at 108f549c (records de0e8b18): the terminal stamp draws the owner's § on a 24-cell disc; the hook's ladder is one rung (0.90), then the sheet alone. Q3: one real-run stamp is 7,180 UTF-16 units; **two stamps no longer fit one message**, so two seals in one turn arrive one per Stop, oldest first (a divergence the frame did not expect). Q6: 0.036 s per disc. Orchestrator re-ran: lint pass, 915 passed with seven neighbouring modules.
- **The owner has not yet looked at the phase-2 stamp.** The sample was `~/Desktop/specseal-stamp-0.90.ans` on the second machine; regenerate it with `bin/seal-stamp` from a real-size values file (the hook's `full_values()` shape) and ask the owner to `! cat` it before phase 3. The owner said to get their check on visual results before proceeding.
- `bin/evidence-check --strict .` exits 2 (25 drifted, 5 broken): the released rows phases 1–2 moved, listed in `phases/phase-2.md`, owed by phase 4's fragment. `survivor-check --range a9d7b0e5...HEAD` reports **10 places**, also owed before the seal.
- Q2 (redraw 0.18.0–0.19.0 images) stays with the owner, default (a), does not block.
- HEAD de0e8b18 (pushed at this handoff). No pull request yet.

## Next

1. Show the owner the phase-2 stamp; take their word before phase 3.
2. Phases 3 (the PNG drawn as an image, same corner placement, transparent around the overhang) and 4 (records, fragment, the evidence-check and survivor debts) by `plan.md`, resuming or spawning `smith` on Opus 5.5. `git merge origin/release/v0.20.0` before the seal.
3. Routing is `automation`: draft PR at the end of the build, `warden` rounds, preflight, sealer, ready, squash into `release/v0.20.0`. Closes #832.
