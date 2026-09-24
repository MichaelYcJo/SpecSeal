# Survivors — the spec is split and its sentences are settled

`bin/survivor-check --range origin/release/v0.15.1...HEAD`, run at phase 6
(`4b25160c`), reported two places carrying the exception sentence #488 widened.
`skills/evidence-check/SKILL.md` §*`correction-check`* was a fourth carrier of
the rule, and it is corrected in the same phase. The one below is
`CLAUDE.md`, which this work item's implementer does not edit: the
orchestrator pastes `phases/phase-3.md`'s replacement A. Once the paste lands,
the quote no longer stands and this exemption stops holding, which is the
intended end of it.

| Path | Quote | Grounds |
|---|---|---|
| `CLAUDE.md` | A branch that removes code an existing ledger row cites — in `seal/ledger.md` or a `seal/releases/<X.Y.Z>.md` — must touch that file to leave the ledger true | `CLAUDE.md` is the repository owner's file, and an agent message cannot authorize an agent to edit it. The orchestrator makes the edit from the paste-ready text in `phases/phase-3.md`, and `tests/test_a_merge_cannot_silently_drop_a_correction.py#test_a8_both_rule_documents_say_what_to_do_at_the_conflict` is red on `CLAUDE.md` until it does, so the exemption cannot outlive a forgotten paste unnoticed |
