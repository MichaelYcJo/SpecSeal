# Survivors — the shipped section goes and the plan is renumbered

## Whole ranges

| Range | Grounds |
|---|---|
| `origin/release/v0.10.0...HEAD` | **This branch deletes `docs/flow.md`'s 0.9.5 section, and every sentence of it standing elsewhere is the deletion working rather than a defect.** The file's own rule is why: *"A shipped version's section is deleted, not kept — the design record, the CHANGELOG and the tickets are the durable copies."* So the 34 places reported are the durable copies the rule names — five in `CHANGELOG.md`, four in `seal/ledger.md` after the fold, the rest in the shipped work items' own `spec.md`, `plan.md`, `overview.md`, `routing.md` and `phases/`, plus one in `skills/verify/SKILL.md` which is the live disclosure the deleted row was a pointer to. **Not one of them may be corrected**: a released changelog entry and a folded ledger row are records of what a release did, and rewriting them to match today's plan destroys the thing they are kept for. This is the second occurrence — #293's range reported 153 — and it is filed as **#307**, which argues that a gathered changelog entry should leave the corpus by construction the way `rounds/` already does. The range row is #297's mechanism, shipped in 0.9.5 for exactly this branch shape. |
