# 1789211172-a-round-record-disarms-survivor-check — phase 5

| Field | Value |
|---|---|
| Phase | 5 |
| Commit | `aa24fbe` |
| Ran by | `specseal:smith` on `unknown` — the spawn prompt named no model, and this template reserves the value for the spawning session rather than letting a segment source it from its own idea of what it is |

## What this phase was asked

`changelog.md`; `seal/ledger/1789211172-….md` created with the new rows;
`seal/ledger.md` S3 re-read and re-verified; `seal/follow-up.md`'s
`survivors.md` row corrected where it describes `rounds/` as left out of the
corpus; `overview.md` with `## Not verified` carrying Q1's residue and the
broad gate.

## What this phase found

**A `spec.md` spelling defect that no phase before this one could have
surfaced.** The frame's §*Data & interfaces* table quoted rows S3 and S6's
anchors as `survivor_check.py#corrected@65b199e3` — the filename alone, which
does not resolve. Nothing reported it while phases 1 to 3 ran. It appeared the
moment the ledger fragment was created, at `2 refused` and exit 2, because
`evidence_check.py`'s `unread_items` reads a work item's records **only once
that work item has a fragment**: a directory with no fragment is in the set
the arm answers *not read* for.

So the defect is latent from the moment the spec is written and surfaces in
phase 5 of the build, after the frame has been approved. A framer cannot check
its own spec against that arm — there is nothing for the arm to read yet — and
the builder is the first party who can. That is the clause this work item feeds
back, and it is in `overview.md`.

**Corrected the way `8ce7f70` corrected the identical spelling in #361's
spec:** the two stamped anchors moved into a fence above the table, with the
sentence saying why. `claim_lines` states the rule — a stamp in a fence is a
quoted anchor exactly as a name in one is a quoted name — and these are
quotations of what S3 and S6 wrote rather than claims this spec makes about
the tree. S3's is the stamp this work item then moves, so fencing is also the
only spelling that stays true after the re-verify. Both rows' content is
untouched.

**A `path:line` spelling inside a ledger fragment is read as a coordinate.**
The fragment's first draft quoted the report's own output —
`…/changelog.md:22` and `rounds/round-1.md:5` — and both came back
`OLD-FORMAT … run evidence-check --migrate`. A ledger row is a content anchor
by rule, so the ledger arm reads any `path:line` in one as a row somebody
forgot to migrate. Reworded to name the file without the line. The same
spelling inside `phases/*.md` is read by the records arm, which counts names
rather than stamps, and is not refused — so the rule is the ledger fragment's,
not the work item directory's.

**`seal/ledger.md` S6 needed no edit and is deliberately left alone.**
Neither `records_a_past_round` nor `corpus` changed a byte, so the row did not
drift, and its claim — the records are outside the corpus — is still exactly
true. What it became is an understatement. The wider claim is S1 of this work
item's own fragment, which is what `CLAUDE.md` asks for: a row is not widened
in place.

**S3 drifted, was re-read, and was re-verified rather than re-pointed.** Its
claim is about what happens to a path once it is in `corrected`'s list — the
counted difference `seen[key] > counted[key]` — and the filter narrows the
list before the blobs are read. Untouched code, moved hash.
`bin/evidence-check --reverify .` named all seven rows it changed, and the
plain check then read `1149 ok · 0 drifted · 0 broken`, exit 0.

**The `survivors.md` row in `seal/follow-up.md` stays open and gains a home.**
Its stale clause compared the proposed exclusion to *the way `rounds/` is left
out of the corpus*; `rounds/` was out of the corpus and in the range until
this work item, so the fix that row proposes had no completed instance to be
modelled on when it was written. It has one now, on both sides of the list.
Q1's answer was *out*, so the row is not closed — it names **#371**, which is
where the argument and #361's round 3 two-run measurement live. Nothing in
this work item re-arms an exemption, which is acceptance row A6.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/follow-up.md`'s clause *the way `rounds/` is left out of the corpus by construction* — the comparison it makes stopped being true when phase 2 landed | Replaced in the same row by the corrected comparison, which points at #365 for the completed instance and at #371 for the open question. The row itself is not closed: Q1 answered *out* |
| `spec.md`'s two unfenced anchor quotations | Moved into a fence in the same section, with the grounds beside them. Nothing left the document |
