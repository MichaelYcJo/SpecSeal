# A/B — the 0.1.0 checker against the redesign, seven scenarios

Run by the review orchestrator, independently of the implementer. The old
checker is `708e348:skills/evidence-check/scripts/evidence_check.py` — the one
0.1.0 users hold. The new checker was measured twice: at `338badc` and again
after round 4's fixes at `38802bc`; the verdicts below are from the second run.
Hashes in new-scheme fixtures were written by the checker's own `--reverify`,
so the harness cannot disagree with the implementation.

Each scenario has a ground truth: should a person be told to re-read the claim
(REPORT), or not (QUIET) — and does the stored pointer still lead a reader to
the right place afterwards.

| Scenario | Truth | 0.1.0 (line + stamp) | Redesign (anchor + hash) |
|---|---|---|---|
| S1 unrelated edit above the citation | QUIET | quiet, **but the coordinate silently lies** — line 9 now holds different code | **quiet, pointer intact** |
| S2 the cited code changes | REPORT | DRIFTED | DRIFTED |
| S3 squash merge of the verifying branch | QUIET | **test failure** — the stamp orphaned, the PR #49 incident | **quiet** |
| S4 stale on arrival (B changes the code, squashes first) | REPORT | DRIFTED — same word as the noise below | **DRIFTED — a hash mismatch, the only thing the word means now** |
| S5 the cited symbol renamed | REPORT | **silent miss** — the cited line was untouched, the claim now names a function that no longer exists | **BROKEN, loud, with the destination**: `locator not found — identical content at #total_price (renamed?)` |
| S6 whitespace-only reformat | QUIET | DRIFTED noise | DRIFTED — a chosen limit, see below |
| S6b an indent change that CHANGES meaning | REPORT | DRIFTED (indistinguishable from S6) | DRIFTED |
| S7 a row verified a minute ago, stamped at base per the old rule | QUIET | DRIFTED — drift at birth, the #50 case | **quiet** |

**Score against ground truth: 0.1.0 3/7 · redesign 6/7.**

## The one miss is a measured choice, not a defect

S6 and S6b cannot be told apart without a parser. Normalising indentation out
of the hash would silence S6 — and silently pass S6b, where a statement moved
out of its loop. The design keeps indentation in the hash: fail-noisy on a
reformat, correct on a meaning change. The remedy after a deliberate reformat
is one command, `evidence-check --reverify .`, which re-hashes every
resolvable row.

## What the numbers do not show

- The 0.1.0 scheme's DRIFTED meant four different things (S2, S4, S6, S7 —
  two real, two noise) spelled identically. A signal indistinguishable from
  noise is what taught people to bump the header instead of reading rows.
  The redesign's DRIFTED means one thing: the content changed.
- On this branch's own history, before the redesign, 12 of 23 commits touched
  `.specseal/` — half the branch was ledger bookkeeping. The stamp/baseline
  machinery those commits maintained no longer exists.
- Checker wall clock, median of five: 356 ms → 114 ms (later ~130 ms with the
  old-format detection), running no git at all.

## Where the harness lives

The scenario scripts ran from a session scratchpad and are not part of the
tree; this file is the durable record. Rebuilding them is mechanical: each
scenario is a three-commit fixture repository, the old half writes a
`path:line` row with a `date `sha`` stamp, the new half writes a
`path#anchor@00000000` row and lets `--reverify` fill the hash. S3 includes
the reachability test the 0.1.0 scheme shipped
(`tests/test_ledger_stamps_resolve.py`, since removed), because that test was
part of the mechanism being compared.
