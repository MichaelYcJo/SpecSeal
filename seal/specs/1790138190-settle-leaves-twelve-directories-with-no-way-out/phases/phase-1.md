# 1790138190-settle-leaves-twelve-directories-with-no-way-out — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | 62a7c6b |
| Ran by | unknown — the spawn prompt named the agent (`smith`) and not the model, and the value is the spawning session's to give |

## What this phase was asked

#511's guard. Open `overview.md`, which the frame's own `spec.md` had turned
`tests/test_chain_hooks_hardening.py#test_every_spec_directory_that_reached_the_ladder_has_an_overview`
red. `settle` names every live ledger row — `seal/ledger.md` whole, the rows
above the first marker included, and every `seal/ledger/*.md` — whose anchor
lies under a released work item's directory; `settle --retire` keeps each
candidate such a row anchors into, removes the rest, exits 1, and prints per
row REMOVED or narrow (`spec.md` G3). `skills/settle/SKILL.md` §4 and
`docs/the-evidence-ledger.md`'s *nothing refuses the removal first*
paragraph say so in the same commit. Verified by A1–A3 in
`tests/test_settle_reads_before_it_removes.py`, each seen red against the
unfixed `retire`; `./bin/settle` naming the `seal/ledger.md` row against
`1788184145` and nothing else; the settle module and
`tests/test_docs_line_wrap.py`.

## What this phase found

**The overview test was red before this phase, as the frame said** —
executed at `3dfd16a`: `1 failed`. Green once `overview.md` exists.

**Six cases, five seen red against the unfixed `retire`** — executed at
`3dfd16a` with the cases added and `settle.py` untouched: `5 failed, 64
passed`. The sixth, *a quoted anchor is not a row*, is a control that passes
with no guard at all (nothing is held, so the directory goes either way); it
earns its red from the liveness mutation below. The document pin
`test_the_documents_say_the_retirement_keeps_an_anchored_directory` was seen
red with the two document edits stashed (`1 failed`), then green with them
back.

**Eight mutations, each red alone** — executed after committing `62a7c6b`,
each restored from saved bytes and `tests/__pycache__` cleared between them:
fragments not read · liveness ignored · rows above the first marker skipped ·
`retire` ignoring the anchored set · the verdict always REMOVED · the report
omitting the anchored list · the first cell blanked · the live-anchor count
zeroed. `git status` clean afterwards.

**`./bin/settle` on this branch, exit 0** (executed, read directly): one
anchored row, `seal/ledger.md:78  The last round's fixes are read by nobody
…`, `into 1788184145-the-gate-stops-the-session-editing-its-tests`, verdict
REMOVED — and nothing else. `12 ungrouped · 0 skipped · 2 unreleased`.

**The guard is its own read, not `coordinates`.** `coordinates` attributes a
row to the section that holds it, which is a grouping question; the guard's
question is only whether an anchor's path lies under `seal/specs/<id>/`,
whoever wrote the row. Both read through `unverified_check.py#live_lines`
and `COORDINATE_RE`, so there is still one liveness rule and one coordinate
shape. An anchor anywhere on a live line counts, the Notes cell included,
because `evidence_check.py` reads `ANCHOR_RE` over the whole text and would
report such an anchor broken just the same.

**`retire` computes the anchored set from its own candidates**, not from
`survey["anchored"]`, for the reason its docstring already gives about
`open_items`: a list made for the report is not a guard on a destructive act.

**The rewritten `docs/the-evidence-ledger.md` paragraph still sits under the
`1790076070` marker.** No marker for this work item was added: a marker is
the fold's record, and this work item has not been folded — writing one would
hand the next `settle --retire` this directory with its spec unabsorbed.

**Slice** (executed): `tests/test_settle_reads_before_it_removes.py`,
`tests/test_docs_line_wrap.py`, `tests/test_chain_hooks_hardening.py` —
`152 passed`. `ruff check` and `ruff format --check` on the two changed
`.py` files: clean.

**One ledger row drifted and was re-read**: `seal/ledger.md` S4 of
`1790027178`, anchored at `settle.py#retire`. The claim — a removal only
where `docs/` records the fold, and a held item refused — still holds; a
dated *Re-read* note says what widened, and `evidence-check --reverify`
moved `5e3f09fa -> acdd5286`. `evidence-check --strict .` exit 0 after.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `docs/the-evidence-ledger.md`'s *A retirement breaks every ledger row … and nothing refuses the removal first* and *(#511 is the missing refusal)* — overturned by #511's guard | the same paragraph, rewritten to say the retirement refuses first |
| the same paragraph's *a fold branch greps the ledger for its directories before it retires anything* — the grep is the command's now | `skills/settle/SKILL.md` §4, *A directory a ledger row anchors into is kept too* |
