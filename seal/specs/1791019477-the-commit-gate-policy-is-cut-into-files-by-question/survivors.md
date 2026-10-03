# Survivors — the commit gate's policy is cut into files by question

`survivor-check --range 2b1dcb1f...HEAD`, run by the builder before the
hand-back, reported one place. It is a record of a moment, and what it says
was true at that moment. Round 1's fix pass added the second row: the
sentence it corrected in `docs/the-record-layout.md` also stands in work item
1790993138's frame, which records the decision as it was made.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790815613-a-gate-decides-at-the-moment-of-the-action-not-from-the-text/overview.md` | because the owner decided on 2026-10-02 that restructuring `docs/` is MichaelYcJo/SpecSeal#715's | work item 1790815613's closing memo, recording why the freeze was written on 2026-10-02. This range lifted that freeze and corrected the present-tense statements of it (the config row, `docs/the-evidence-ledger.md`, the fold pin's docstring); the memo records the decision as it was made, and `spec.md` §*Scope* leaves every other work item's records untouched |
| `seal/specs/1790993138-every-record-has-one-home-and-a-released-ledger-file-never-changes/spec.md` | The `Over the ceiling` row goes away in the same change | work item 1790993138's frame, recording F1 as #715 decided it; #727 kept the row at `none` (D8) and corrected the present-tense statement in `docs/the-record-layout.md`, and `spec.md` §*Scope* leaves every other work item's records untouched |
