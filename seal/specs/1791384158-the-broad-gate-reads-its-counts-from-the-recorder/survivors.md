# Survivors — the broad gate reads its counts from the recorder

`survivor-check --range d6a443fd..ae9027d1` named 22 places that still carry
wording this build removed. Each was read at ae9027d1, and none is a sentence
this work owes a correction in place:

- **Released ledger files never change** (`seal/config.md` declares `Ledger
  frozen from`). Every released row below that this work made false is
  superseded by a `Corrected ·` row in this item's fragment; the others are
  history inside a family whose newest reading that fragment now holds.
- **Another work item's records are a record of what was true then**, and no
  build rewrites them.
- **Three places share only a phrase** with a docstring this work removed,
  the `summary_counts` one about a unit at depth 2, and say something else
  that still holds.

| Path | Quote | Grounds |
|---|---|---|
| `seal/releases/0.10.0.md` | This row lost a coordinate rather than re-pointing one | released, frozen; S14 is superseded by this fragment's `Corrected · S14` |
| `seal/releases/0.10.0.md` | It closes the finding on the instance and not the class | released, frozen; the same S14 row |
| `seal/releases/0.17.0.md` | The COUNT of blocks is bounded: `admitted` carries as many of the oldest pending blocks | released, frozen; 0.17.0's B2 is superseded by 0.20.0's `Corrected · B2`, which this fragment's `Corrected · B2` supersedes |
| `seal/releases/0.20.0.md` | `admitted` carries as many of the oldest pending blocks as fit `MESSAGE_BUDGET` together with their disc at the ladder's one rung | released, frozen; superseded by this fragment's `Corrected · B2` |
| `seal/releases/0.18.0.md` | C2 · `suite_counts` reads pytest's JUnit file | released, frozen; superseded by this fragment's `Corrected · C2` |
| `seal/releases/0.20.0.md` | `DEFAULT_SCALE` is 0.90, `--scale` defaults to it | released, frozen; a re-read of 0.15.7's N5, which this fragment's `Corrected · N5` supersedes |
| `seal/releases/0.15.7.md` | Everything else this row lists holds: `drawings` still draws each file whole at its own scale | released, frozen; 0.15.7's N7 family, superseded by 0.20.0's `Corrected · N7` and this fragment's `Corrected · N7` |
| `seal/releases/0.20.0.md` | with #832's sentences that the ladder is one rung, 0.90 | released, frozen; superseded by this fragment's `Corrected · D2` |
| `seal/releases/0.20.0.md` | `SCALE_LADDER` is `(0.90,)` since #832 | released, frozen; superseded by this fragment's `Corrected · B1` |
| `seal/releases/0.15.7.md` | with no `--scale` the scale is `seal_stamp.DEFAULT_SCALE`, 0.90 | released, frozen; superseded by this fragment's `Corrected · N5` |
| `seal/releases/0.20.0.md` | or its `end` line shows an exit other than 0, 1 and 5, as a `KeyboardInterrupt` | released, frozen; superseded by this fragment's `Corrected · U3` |
| `seal/specs/1791384158-the-broad-gate-reads-its-counts-from-the-recorder/spec.md` | Describes the ladder as *its file's own scale, then 0.90, the one rung with a disc since #832*. | this item's frame, quoting the sentence it asked to be corrected; `docs/the-broad-gate.md` was corrected |
| `seal/specs/1790260567-the-broad-gate-hands-cmd-a-forward-slash/plan.md` | Phase 2 reads what is actually missing, the summary | another work item's plan, a record of its own build |
| `seal/specs/1791270164-the-release-seal-is-drawn-in-curves/spec.md` | `scale` None leaves the disc off and the block begins at column 0 | another work item's frame, a record of its own build |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/overview.md` | as many as fit with the disc, oldest first, each at the highest rung it can take | another work item's overview, a record of its own build |
| `seal/specs/1790913304-the-seal-stamp-is-a-letter-with-the-seal-on-its-corner/questions.md` | **As many as fit with the disc, oldest first, each at the highest rung it can take | the owner's answer of 2026-10-02, a record; the rule it states holds over the two rungs left |
| `seal/specs/1791076833-the-reverify-writer-records-before-it-restamps/spec.md` | `round_record close` then refused round 2 at depth 2 | another work item's frame; shares the depth-2 phrase only |
| `skills/code-review/orchestration.md` | A fix answering a finding *inside* a unit an earlier round's fixes created may not add another to pin it | shares the depth-2 phrase with the removed `summary_counts` docstring; still true |
| `skills/code-review/scripts/round_record.py` | A unit at depth 2 is refused before any of that is written | the same phrase; still true |
| `agents/smith.md` | The depth is measured rather than declared | the same phrase; still true |
| `skills/verify/scripts/broad_gate.py` | **A row is refused four ways, and all four are exit 2 with nothing run** | shares "is the counterfeit `verify` names" with a retired scale case's docstring; still true |
| `.test_durations` | -m pytest -q -p no:cacheprovider tests-a | the test runner's timing data, keyed by test ids; not prose |
