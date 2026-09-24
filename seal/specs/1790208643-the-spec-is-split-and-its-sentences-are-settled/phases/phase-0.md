# 1790208643-the-spec-is-split-and-its-sentences-are-settled — phase 0

| Field | Value |
|---|---|
| Phase | 0 |
| Commit | 23d46e81 |
| Ran by | specseal:smith on Claude Opus 5.5 (1M context) — the agent as the spawn prompt's first line names it, the model as the commit trailer it prescribes names it |

## What this phase was asked

The A/B/C half of phase 0, from the merged base `f2e8915c`
(`origin/release/v0.15.1` at `61f0d0d8` merged in): re-read every section A
(#550), B (#549) and C (#552) rewrote that `plan.md` §Summary names — the
survivor sweep, the broad gate and sealer sections, the `Broad gate` cell and
`same_run` sentences, the depth convention, `agents/warden.md` §*Where you
work* and its two-depth sentence, `docs/release-checklist.md` §2–3 — and
re-measure the heading tree of `docs/review-chain-spec.md` (M1's inputs).
D's half (#558, not squashed at the spawn) is left for the resumed phase 3.

## What this phase found

**The four squashes are three, and D is not one of them yet** (executed:
`git log --oneline origin/release/v0.15.1 -6`): `61f0d0d8` (#550, A),
`1404b3a7` (#549, B), `6b912e66` (#552, C), then `9f846733`, the v0.15.0
merge. D's branch exists on the remote (`fix/547-the-fold-writes-each-release-to-its-own-file`)
and nothing of it is on the base. So every ledger row this branch re-points
lands in `seal/ledger.md` as it stands, and the resumed phase 3 re-reads
where D moved each one.

**What A, B and C changed in the files this item touches** (executed:
`git diff 9f846733 origin/release/v0.15.1` over `docs/review-chain-spec.md`,
`agents/`, `docs/release-checklist.md`, `docs/review-handoff-protocol.md`,
`CONTRIBUTING.md`, `skills/verify/SKILL.md`, `skills/code-review/SKILL.md`,
`skills/code-review/orchestration.md`, `round_record.py`, `chain_check.py`):

- `docs/review-chain-spec.md`: two edits, both in sections this split moves
  or keeps. The `same_run` sentence in §*The review run has a bound*'s last
  `###` (§*Where a leftover goes*, the sealer paragraph) stays in the run
  document. C's #366 sentence closes §*The depth in `New units`*'s
  *What no check can see* paragraph and moves with the section to the record
  document, unchanged.
- `agents/warden.md`: B's clone paragraph under §*Where you work*, and C's
  *Write one depth per finding* paragraph. Neither cites the spec; the one
  warden citation this split re-points is §*A verdict row that commissions
  nothing* at `:206`.
- `skills/code-review/SKILL.md`: C's *One depth per finding* paragraph cites
  `docs/review-chain-spec.md` §*The depth in `New units`*, a section that
  moves to the record document. **The frame's list of shipped citations does
  not have it** — it was written before C landed — so phase 1 re-points it
  too.
- `docs/release-checklist.md` §2 (the fold's second-run sentence) and §3 (the
  command block's `bin/test -q`), `docs/review-handoff-protocol.md`'s
  `Broad gate` row, `skills/code-review/orchestration.md`'s two sealer
  paragraphs, `agents/sealer.md`'s gate-copy and scratch paragraphs and its
  `earlier run` sentence, `round_record.py#kept_broad_gate`'s docstring and
  `new_broad_gate_file`'s comment, `chain_check.py#broad_gate`'s docstring,
  `CONTRIBUTING.md`'s `-n auto` paragraph, `skills/verify/SKILL.md`'s
  scratchpad capture: none of them cites the spec by a section this split
  moves, and none is on this branch's edit list except `agents/sealer.md`
  and `round_record.py`, which #556 edits in phase 4 against the text as C
  left it.

**The heading tree at the merged base** (executed: a heading walk that skips
fenced blocks, over `docs/review-chain-spec.md` at `f2e8915c`). 2,246 lines,
eight more than the frame measured at `9f846733` — C's sentence and A's
two-line widening of the `same_run` sentence. Spans, to the next heading at
the same level or above:

| Line | Span | Heading |
|---|---|---|
| 1 | 13 own | `#` title and opening |
| 14 | 18 | The cycle |
| 32 | 328 | The review run has a bound (own 31; its four `###` 63, 45, 87, 102) |
| 360 | 63 | Two records |
| 423 | 14 | Registration |
| 437 | 1,551 | commit-review-gate (own 36; Which repository 172 with its `####` 29; Why a deny 25) |
| 670 | 1,278 | Review arm (own 39; Where the marker goes 28) |
| 737 | 1,211 | The declaration (own 71) |
| 808–1655 | 30, 86, 20, 140, 91, 208 | `Pass`, `Fixes checked by`, finding id, verdict row, fix range, fix surface |
| 1383–1579 | 53, 28, 116 | floor, `Needs a fix`, reopening |
| 1580–1727 | 76, 72 | depth, `Ran by` |
| 1728–1947 | 128, 92 | When the record was written, What the record carries |
| 1948 | 40 | Parity arm |
| 1988–2035 | 20, 28 | review-history-guard, implementer-mark |
| 2036 | 50 | The survivor sweep (its `###` 16) |
| 2086 | 150 | The record generator (own 37; its three `###` 39, 41, 33) |
| 2236 | 12 | Non-goals |

**The tail that belongs to §The declaration is 35 lines, not 17.** It runs
from *Which declaration applies is settled by the branch it names* to
*Deleting the routing file restores today's behavior exactly* — lines
1912–1946 here — and the text the frame quotes as its first and last
sentences is exactly that run. The frame's count was wrong and its
boundaries right; the move is made by the boundaries. The paragraph above
the tail — *A moratorium for 0.8.x: no new parsed field in `round-N.md`* —
is about the record and stays with §*What the record carries*.

**M1's inputs, re-estimated from these spans**: the run document about 870
lines, the gate document about 520 (the tail's extra 18 lines go here), the
record document about 885. All three under the 1,000-line ceiling, so the
four-document fallback is not in play; phase 1 measures the real counts.

**Fold markers at the base** (executed: `unverified_check.live_lines` and
`FOLD_MARKER` over the file): 29 live marker lines, 26 distinct ids; the
multiset's digest, sorted and newline-joined, is `8f8c4d85f213eb9b`
(sha256, first 16). Phase 1's census compares against this.

**Baselines taken for phase 1** (executed, exit codes read directly):
`python3 skills/evidence-check/scripts/evidence_check.py --strict .` exit 0,
`total: 1767 ok · 0 drifted · 0 broken`; `bin/settle` exit 0, first line
`released and unfolded: 8 work items in 8 segments, 2 ungrouped, 0 skipped`.

**The ledger anchors on the document are 24, not 23.** The 23 in
`seal/ledger.md` the frame counted are there, and C's fragment
`seal/ledger/1790206437-a-second-fold-writes-a-second-heading.md` row D1
adds a fourth anchor on §*The depth in `New units`*. Phase 1 re-points it in
that fragment.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
