# 1791270164 — handoff

Written 2026-10-06 by the orchestrating session (Opus 5.5) when the 0.20.0 run moved to another machine. Read this first, then `overview.md` §*Where the run stopped*.

## Where it stands

- `framer` on Fable 5.1 framed this item (fce42e0d) after the owner reopened the emblem mid-frame. `smith` on Opus 5.5 started phase 1 and left it **unfinished and not green**, committed as `wip` (de5f8fcb) so the work survives the move.
- The vector source, the cell-centre sampler and `build(scale, r0_cells=…)` are in. `EMBLEM_D` holds an INTERIM ring.
- `bin/test` over the two phase-1 modules with `-x` exited 1: 1 failed, 487 passed. The failure is `test_several_files_come_out_as_one_message_oldest_first`. The smith suspects the 0.90 disc narrowed from (40, 40) to (39, 40) and the hook now picks a different rung. That is unconfirmed.
- The branch is pushed so the other machine can fetch it. No pull request is open.

## Q1 — the emblem — is the owner's, and it is still open

The owner withdrew the lily: it reads badly at 0.90 and has no tie to the project. They asked for a mark that means SpecSeal and for a smaller disc pressed inside the sheet's lower right corner, "like a real seal". The candidates were rendered on the old machine from vector at terminal resolution:

- § (section sign). It reads as `$` or S at 20 px and below.
- A serif S monogram. It is legible to 20 px.
- A check mark. It is legible even at 16 px.
- A document page. It turns to stripes at 16 px.

Each was drawn at 20 and 16 px, with a plain disc or with a wax edge plus a raised inner rim.

The orchestrator recommended C or B at 20 px with the wax edge and rim; at 16 px, drop the rim. The renders were in the old machine's session scratchpad and did not travel. The owner's answer supplies the `EMBLEM_D` path and the disc size (`r0_cells`). The pull request is not opened with the interim ring.

## Next

1. Read which rung `admitted` picks for the two blocks. Then decide whether the failing case's expected rungs change or `R0_CELLS` does.
2. Re-run the two modules without `-x`, then see each new case red (`bin/mutation-check`).
3. Finish S8's documentation sweep: the module docstring still says fleur-de-lis and 29x32 chart, and the `SCALE_FLOOR`, `DEFAULT_SCALE` and `KEY` comments and the *lily* case names remain. Then write `phases/phase-1.md` and fill `plan.md`'s Status.
4. Phases 2–4 by `plan.md`: the disc moves inside the sheet, the PNG is drawn as an image, and the emblem and records follow. The framer estimated 2–3 hours of smith wall time.
5. Routing is `automation`: the draft pull request, the `warden` rounds (Opus 5.5), `broad-gate --preflight`, the sealer, then ready. The pull request goes into `release/v0.20.0` (squash) and closes #832.
