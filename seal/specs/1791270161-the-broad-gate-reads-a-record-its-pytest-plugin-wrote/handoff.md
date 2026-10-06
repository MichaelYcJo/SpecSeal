# 1791270161 — handoff

Written 2026-10-06 by the orchestrating session (Opus 5.5) when the 0.20.0 run moved to another machine. Read this first, then `overview.md` §*Where phase 1 stopped, and what is next*.

## Where it stands

- Framed by `framer` on Fable 5.1 (ea5b1bfe). Phase 1 was built by `smith` on Opus 5.5 (27365f10, 74c2ab7c). The recorder module and its eight cases (S1–S5) are in; `broad_gate.py` is unchanged and nothing loads the recorder yet.
- Q-M1 and Q-M2 are answered (the smith's measurement): `-p` through `PYTEST_ADDOPTS` loads the recorder on pytest 7.4.4, 8.0.2, 8.1.2 and 9.1.1. Under `-n 2` the controller alone writes the record. A failed collection arrives once per worker, so the reader treats a file's lines as a set. pytest reports the rootdir already resolved, so `realpath` on both sides is required.
- The branch is pushed so the other machine can fetch it. No pull request is open.

## A divergence phase 2 must handle

The recorder holds no three-part pytest or xdist version, so Q-W2's default ("move the `9.1.1` and `3.8.0` release-hygiene exemptions to the recorder's comment") no longer fits. Decide it in phase 2. `overview.md` records the divergence.

## Next

1. Phase 2 by `plan.md`: `recording_env`, `read_record`, the HEAD run recording with the `FAILED`-line fallback, `compare_at_base` rewritten to one base run and the five-row table, the Scope 7 retirements. In the same commit: rule 3, the **New?** bullet and their pins. Re-read the roughly sixty end-to-end cases into `phases/phase-2.md`. The framer estimated 2–4 hours of smith wall time for phases 2–4.
2. Phases 3 (ledger and changelog fragments) and 4 (regression corpus).
3. Routing is `automation`: the draft pull request, the `warden` rounds (Opus 5.5), `broad-gate --preflight`, the sealer, then ready. The pull request goes into `release/v0.20.0` (squash) and closes #825, #807, #813, #816 and #818.

Q1 (owner) is unanswered; its default (a), strict `new?`, is what gets built.
