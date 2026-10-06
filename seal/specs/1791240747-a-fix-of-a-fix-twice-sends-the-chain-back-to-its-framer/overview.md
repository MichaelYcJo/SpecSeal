# 1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer — overview

📋 implement applied
· spec:     `spec.md`, `plan.md` (approved, `afedc96c`), `questions.md`; `docs/review-chain-spec.md` §*The review run has a bound, and an end* and §*The reopening — one, and then the run is capped*; `docs/round-record-spec.md` §*The fix range*, §*The fix surface*, §*The depth in `New units`*; `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `skills/code-review/orchestration.md` §*The cap is a ceiling* and §*A fix pass adds the unit that pins it*; `skills/implement/orchestration.md` §*which of these acts runs itself*; `templates/config.md` §*What no row governs*
· evidence: `seal/ledger/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer.md` — A1–A7 new, 54 `Re-read ·` rows, `Corrected ·` G8, R3, R4
· verified: executed — the narrow module runs each phase names, the modules touching every file changed, `mutation-check` on every unit added, the S12 replay probe, `evidence-check --strict` (exit 0), the freeze diff (empty), `survivor-check` (nothing standing); read — the claims of every released row whose anchor moved; unverified — the full suite, lint and typecheck (the sealer)

## Why this work exists

A fix pass whose fix is itself the next round's finding, twice in one run, now stops the fix passes mechanically and sends the work item back to its framer, where it used to run on until a person noticed.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| Where the unit's AST is kept | `plan.md` phase 1: "`top_units` keeps enough of each node to compare ASTs between ends" / the code adds `round_record.py#unit_dumps`, a separate reading keyed to the same names | code | `top_units`' value is a three-tuple a dozen call sites unpack; a fourth element moves all of them for a reading only `fix_pass_units` makes |
| Whether `New units` is read | `spec.md` §*The reading*: "that unit is named by round K-1's `New units`, or is present at both ends … with a different AST" / the code derives the added units from the range's two ends and does not read the row | code | `close` writes `New units` from exactly the units present at `b` and absent at `a`; the ends give the same set with the path the row lacks, so a name two files share cannot land in the wrong file. The two differ only for a hand-edited row (inferred during implementation) |
| The arm's signature | `spec.md` §Data & interfaces: "`fix_of_a_fix(reader, root, rel, earlier, later)`" / the code takes `(reader, root, rel, earlier, stopped)` | code | none of the gate table's eight rows reads the records after this one, and the resumption row needs the `second` the run began after |
| Which open rows can land | `spec.md` §*The reading*: "its verdict is open when `new` writes the record" / the code also skips a row whose `#` cell carries 🟢, ❓ or ⬜ | code | the spec's own Grounding widens the severity "to any finding that commissions a fix", and `round_record.py`'s `OWED_MARKERS` comment says those three commission nothing; the replay measured six work items stopped on ⬜ rows alone (inferred during implementation) |
| The one-owner rule's number | `plan.md` phase 3: "rule 11" / the row is rule 16 | code | 11 has belonged to *a wrapped terminal line is one value* since #340, and 12–15 followed it |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, the repository-wide lint and the typecheck over the branch | the sealer, once the review rounds settle |
| ✅ Whether 18 of 57 work items is the stop rate wanted, against the hunk grain's 10 that misses #801 (`questions.md` Q4) | decided by the orchestrator at round 1, under the `automation` answer by which the repository owner delegated the run's decisions: the function grain stays at two. The evidence is round 1's reviewer's sample — 11 stops opened, 10 real, 1 borderline, 0 false — and their replay, 26 of 64 over all four tags; the sample answered whether the stops are real, and the reviewer left the rate itself the owner's call (`questions.md` Q4; corrected by round 2's ⬜ 4) |
| ✅ The 23 records at `v0.18.1` and `v0.18.2` whose fix ranges this clone does not carry, so the replay read none of them | resolved by round 1's reviewer with `refs/pull/*/head` fetched in a scratch clone: 119 of 122 records resolve, and five more work items reach `second`, all at round 3 (`questions.md` Q1's correction) |
| A real stop end to end — the orchestrator closing on `deferred the frame`, labelling `chain: reframed`, re-spawning the framer and resuming — has run only as planted repositories | the orchestrator, at the first `second` a run writes |

## Not done

`CLAUDE.md`'s 3+ Fix Rule line and `templates/claude-md-block.md` are left as they are, as `spec.md` §Out says: a link to the new owner is a one-line follow-up for the repository owner. Nothing reads `chain: reframed`, by design. `agents/smith.md`'s 3+ Fix bullet is about the builder's own loop and is untouched.

## Fed back into the spec

None of `spec.md`'s clauses was rewritten. Two readings were added and are recorded above as inferred during implementation: added units come from the range's ends rather than the `New units` row, and a 🟢, ❓ or ⬜ row never lands. Round 1 added three more: a cell naming a file is about that file, so a backticked name beside it lands only through that path and a bare name only where one file of the range carries it; the gate holds a run's count in both directions and only a counted `second` cuts a run; and the depth walk reads the current run (`questions.md` Q5, the orchestrator's decision). `docs/review-chain-spec.md`'s reopening section gained one sentence saying a `second` ends a run too.
