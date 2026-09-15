# 1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for — survivors

<!-- What `survivor-check` reported over this work item's range and why each
report is not a defect. Two row shapes live here; this file uses the range
shape (#297), anchored on the range AND on this work item's directory. -->

`bin/survivor-check --range a99298b6..HEAD --root .` at `33661fb0` examined
1001 files against 40 sentences the range removed, and reported **88 places**:
85 in `seal/ledger.md` and three in other work items' closed records
(`1788993115-a-payload-is-written-again-on-every-spawn/spec.md` and its
`phases/phase-2.md`, `1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red/plan.md`).

**Every one of them traces to one deleted ledger row, and none is a defect.**
This branch removed S14 of work item 1788354065 from `seal/ledger.md`, because
its claim — the bootstrap *asks the mode question … and then the parity
question, and nothing else* — went with the code when phase 4 made it ask a
third. `CONTRIBUTING.md` §*House rules* says a claim that went with the code is
removed rather than re-pointed, so the row went and the new claim is in this
work item's own ledger fragment.

That row's Notes cell carried the boilerplate every row restated by work item
1788993115 (#292) carries — *Restated 2026-09-10 by work item 1788993115
(#292), which moved the Bootstrap section to `skills/implement/…*. Its
neighbours at `seal/ledger.md:1885-1891` carry the same sentence about their
own claims, which are still true and were re-read and `--reverify`'d on
2026-09-15. The three reports outside the ledger are closed records of other
work items, which are not this branch's to edit.

**What the check found where it would have mattered is nothing.** No file under
`skills/`, `templates/`, `agents/`, `tests/` or `docs/` is reported. The three
removals that carry meaning — rule 3's second copy in `skills/config/SKILL.md`,
`templates/config.md` §*Broad gate*'s closing paragraph, and
`broad_gate.missing_row`'s *write the repository's own broad command into it* —
survive nowhere in the tree.

| Range | Grounds |
|---|---|
| `origin/release/v0.12.0...HEAD` | The range removes one `seal/ledger.md` row whose claim went with the code (S14 of 1788354065, *and nothing else*). Every one of the 88 reports is that row's shared Notes boilerplate standing in neighbouring rows whose own claims are still true and were re-verified on 2026-09-15, or in another work item's closed record. Per-place rows do not scale here and none of the 88 is a repair: the three removals that carry meaning survive nowhere, and no file under `skills/`, `templates/`, `agents/`, `tests/` or `docs/` is reported at all |

## Round 1's fix pass — `96c88c9f..HEAD`

Nine places, and the cause is one rewritten paragraph. The fix pass removed
*a refusal that names what to write* from `broad_gate.missing_row` and from
`templates/config.md` (round 1's 🟡 4), and the true sentences around it share
that vocabulary — **`broad-gate` names the row and exits 2 with nothing run**
is still exactly what the gate does, and is what three of these say. None of
the nine is a stale claim.

| Path | Quote | Grounds |
|---|---|---|
| `templates/config.md` | `broad-gate` names the row and exits 2 with nothing run, because a seal taken over a command nobody chose seals nothing | Still true, and it is not the removed claim. What was removed is that the message names WHAT TO WRITE; this names the row, which the message still does |
| `templates/config.md` | **An absent row is a refusal, not a default.** `broad-gate` names this row and exits 2 with nothing run | The opening of the very paragraph this pass rewrote. Its first two sentences were correct and stayed; the sentence after them is what changed |
| `skills/config/SKILL.md` | **The `Broad gate` row has no default at all**: absent, `broad-gate` names the row and exits 2 with nothing run | Same sentence, same reason. Step 1's job is to show the row as absent and say what happens, which is unchanged |
| `tests/test_first_setup_asks_once.py` | `Orchestrator: Parity setup` states the rule for the original — *never guess* | A docstring matched on prose similarity to the bootstrap paragraph this pass edited. It describes the parity setup, not the refusal |
| `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` | The row is the one value only a person can write and nobody had written down how to choose it | A docstring about #401's second half, matched on shared vocabulary. Still true |
| `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` | A rule with no reason is one the next reader drops when it is inconvenient | The same, one case down |
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/spec.md` | **A missing `Broad gate` row is a refusal, not a default**: the sealer says which row to write and exits 2 | Another work item's CLOSED record, and a record is the past. It was true at the SHA it describes; rewriting it would make it describe a tree it never saw |
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/overview.md` | `templates/config.md` and the config skill both now say to put the runner first | The same, and the claim it states is now carried forward correctly in `seal/ledger.md`, which this pass corrected |
| `seal/specs/1789002694-two-agents-are-forbidden-the-seal-and-nobody-is-assigned-it/phases/phase-2.md` | `templates/config.md` and the config skill say to put the runner first for this reason | The same. Its live counterpart in `seal/ledger.md` was corrected rather than this record |
