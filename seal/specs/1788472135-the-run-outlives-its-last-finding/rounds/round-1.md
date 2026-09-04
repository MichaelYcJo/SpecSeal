# 1788472135-the-run-outlives-its-last-finding — review round 1

| Field | Value |
|---|---|
| Target SHA | c0325b5ad90689548070bad7030d8bb6b79abb74 |
| PR | not yet opened |
| Broad gate | not yet |
| Fixes checked by | nobody — this round's fixes are not yet written; the round that reads them sets this cell |
| Contract changes | `floor_answer` renamed to `yes_or_no` and widened to read both the floor row and `Needs a fix` → `stopping_floor`, `run_reopened`; `stopping_floor` took a count of later records and now takes the records themselves, in round order → `main`; `depth_problems` returns four lists where it returned three → `fix_surface`; `says_none` accepts a trailing `;` → `fix_surface` (both row arms) |
| New units | `run_reopened` (depth 1); `NEEDS` (depth 1); `NEEDS_FROM` (depth 1); `SUBSECTIONS` (depth 1); `NO_CHECK_READS` (depth 1); `COMMA_LIMIT` (depth 1) |
| Needs a fix | yes — 🔴 1 the floor refuses the sequence its own documents require; 🔴 2 `docs/review-handoff-protocol.md` carries neither new rule; 🔴 3 `evidence-check --strict` exits 2, and that is the release-preparation step |
| Loses a record or crashes | no |

- [ ] Pass

<!-- The eighteen test functions this round's fixes planted are deliberately
not in `New units`. The three constants above are data a later change can
silently put out of step; a per-case function is shown whole by the diff, and
listing eighteen of them would bury the six units the verifying round has to
actually open. The implementer proposed this and the orchestrator accepted it.
Every entry is depth 1: round 1's findings were all inside what phases 1-3
wrote, and none inside a unit the fix pass itself created. -->

## What this round was asked

The whole branch against `release/v0.8.0`, with eight named surfaces to attack
in order — the order being what would cost most if it were wrong, and the list
existing because #81's round 1 was the cheapest round on record for having one.

1. The floor and the verifying round contradicting each other: construct the run
   where a round meets the floor, its fixes close a 🟡, and the one permitted
   verifying round then opens something. Is there a legal next move?
2. How later records are counted — filename sort against `round-10.md`, or
   `Target SHA` order on a branch that moved.
3. `DEPTH_RE` against hostile unit names: a name containing `(depth 2)`, digits
   (`sha256_of`), `(Depth 1)`, `( depth  1 )`, `(depth 01)`, two markers.
4. `says_none` against the depth walk, and the short-circuit order that decides
   all of it.
5. The two cutoffs at the same second, and a work-item directory with no
   timestamp prefix.
6. A malformed row on an old record — absence grandfathered, malformation not.
7. This branch's own records are the first held to both rules. If a real record
   cannot be written honestly, that is a 🔴 at the cheapest possible moment.
8. What the ledger fragment claims, including the two rows left DRIFTED on
   purpose.

The runner was handed over rather than left to be found — `.venv/bin/pytest`,
with the four other checkers and their argument shapes — because #51's
observation 4 measures one lost round trip per round to an invocation nobody
handed over, and this session had already lost three finding it.

The implementer's executed and unverified lists were handed over so the round
would check rather than repeat them.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | A run whose verifying round produces fixes has no record set that passes. Round N answers `no`, round N+1 verifies and closes something with a fix, those fixes need round N+2 — and `later` for round N is then 2 | `skills/code-review/scripts/chain_check.py:1731` | open | `word == FLOOR_NO and later > 1` read directly at `:1731`; `test_a_second_record_after_the_floor_fails:350` pins exit 1 for exactly that sequence. `skills/code-review/SKILL.md:294`, unchanged by this branch, says a verifying round that opens something IS a finding round — and a finding round's fixes need a reader. This branch's own run is the first instance: this record answers `no` and `Needs a fix: yes` |
| 🔴 2 | `docs/review-handoff-protocol.md` — which `templates/sdd-round.md:7` names as the file that carries the format — learned neither rule | `docs/review-handoff-protocol.md:110-124`, `:117`, `:285`, `:476-501` | open | `grep -c "Loses a record or crashes"` → **0**, verified. `:117`'s `New units` row names neither the depth nor the `;` separator. `:285` says both fix-surface rows are grandfathered by one key, which `DEPTH_FROM` made false. Title still `draft 0.9`. `tests/test_the_fixes_name_their_surface.py:473` enforces this class for the previous two rows and nothing extends it |
| 🔴 3 | `evidence-check --strict` exits 2 on this tree, and `docs/release-checklist.md` runs that command at release preparation | `seal/ledger.md:543`, `:517` | open | Executed: `--strict` → exit 2, plain → exit 1, `467 ok · 2 drifted`. `release/v0.8.0` reports `451 ok · 0 drifted`, so both are this branch's drift. The checklist prescribes `--reverify`, which is the one act the implementer correctly refused for a claim that is false — `:543` says *eleven fields* and the list is twelve |
| 🟡 4 | `skills/code-review/SKILL.md` gives two answers about `New units` and omits the floor from its own field enumeration | `skills/code-review/SKILL.md:167`, `:393` | open | `:393` is the table a session opens to fill the cell and names no depth; `:167` enumerates the record's contents and stops at `Needs a fix`. Phase 1 corrected exactly this class for `Needs a fix` in three files |
| 🟡 5 | The entry walk splits on `;` alone and takes the first depth marker, so a comma-separated list and a doubled marker both pass | `skills/code-review/scripts/chain_check.py:1447` | open | Four cells executed; the comma form is the spelling `New units` used **before** this branch, which `tests/test_the_fixes_name_their_surface.py:310` had to be migrated off in this diff. `plan.md:132` declares the failure direction *blocks more*; these two paths allow |
| 🟡 6 | `none;` is refused, and following the refusal's own instruction produces `none (depth 1)`, which the checker reads as *no units* | `skills/code-review/scripts/chain_check.py:1393`, `:1547` | open | Executed both cells. `says_none` rstrips `.` and not `;`, and short-circuits before the depth walk |
| 🟡 7 | A work item with no timestamp prefix is excused all four refusals permanently, and three of the four never say so | `docs/review-chain-spec.md`, `chain_check.py:1200` | open | Three cases executed on a no-prefix directory. The behaviour follows `item_began`'s recorded reasoning and is not disputed; the checker's public contract is where it comes apart |
| 🟡 8 | The module docstring — the checker's own inventory of what it refuses — gained neither rule | `skills/code-review/scripts/chain_check.py:2-242` | open | The `New units` block still names no depth; `Loses a record or crashes` first appears at `:377` as a constant |
| 🟡 9 | Deleting the shipped `## 0.7.0` section rides a feature branch, against two precedents that gave it its own | `docs/flow.md`, commit `b5166af` | answered | The precedents are real (`818f119`, `ef7937e`). The grounds for doing it here are in the commit body: `release/*` takes no direct push, so the change needs a branch and a pull request, and no other branch of this release was open. The risk named — that dropping this pull request drops the deletion — is accepted rather than unseen |

## Executed probes

| What was run | Result |
|---|---|
| `evidence_check.py --strict .` | **exit 2**, `467 ok · 2 drifted` — 🔴 3 confirmed |
| `evidence_check.py .` | exit 1, same totals |
| `grep -c "Loses a record or crashes" docs/review-handoff-protocol.md` | **0** — 🔴 2 confirmed |
| `sed -n` at `chain_check.py:1731` | `if word == FLOOR_NO and later > 1:` → error unless excused — 🔴 1's mechanism |
| `sed -n` at `tests/…floor_and_the_depth.py:350` | `assert code == 1` for three records, two answering `no` — the behaviour is pinned |
| `grep -rn "Needs a fix"` over `chain_check.py`, `hooks/`, `bin/`, `.github/scripts/` | **zero hits** — the row that says a run reopened is read by nothing, which is what decides 🔴 1's repair |
| `pytest tests/test_docs_line_wrap.py` | 18 passed |

The reviewer's own runs are in its report and are not restated here: 154 cases
green at the target, 23 of 34 red at `1b4d5a4`, 50 probe cases, both ledger
modes, `fold_ledger --dry-run`, `unverified-check`, `chain_check --baseline
main`. It worked in a `git clone --no-local` and its probe file was deleted.

## Inherited coordinates

Round 1 — nothing to inherit. What this round was handed instead is in *What
this round was asked*: the implementer's own phase records, which carry what
each phase found and where it diverged from the plan.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `seal/ledger.md:517` (*S8*) is corrected or removed. Its claim is false — `templates/config.md:23`'s first row is `Commit and pull request language` — but the claim predates this branch and belongs to a released section | `overview.md` §Not verified, and half of 🔴 3 | the repository owner |
| Whether a `(depth 1)` on a unit that is really second-level is honest. No check can see it | `overview.md` §Not verified | the verifying round reading the `New units` surface |
| The full suite, repository-wide lint, and typecheck | `overview.md` §Not verified | the orchestrator's single broad run, after the rounds settle |
| That the reviewer spawned two general-purpose agents and the shared working tree was switched off the branch under review, against `agent-contract` §6 | an issue of its own, opened by the orchestrator | the repository owner — it is a defect in the chain, not in this branch |
