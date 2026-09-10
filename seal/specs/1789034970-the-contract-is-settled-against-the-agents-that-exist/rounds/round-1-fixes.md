# Round 1's fix pass — the contract is settled against the agents that exist

Range `e972b5f..054c58f`, eight commits, on
`docs/120-the-contract-is-settled-against-the-agents-that-exist`. Every finding
of round 1 has a row. Read by `round_record.py close`, which applies it to
`rounds/round-1.md`.

## Fixes

| # | Verdict | Commit or grounds |
|---|---|---|
| 1 | fixed | `6788894` |
| 2 | fixed | `d137aeb` |
| 3 | fixed | `d137aeb` |
| 4 | fixed | `1f2e9fc` |
| 5 | fixed | `054c58f` |
| 6 | fixed | `d5146a3` |
| 7 | fixed | `d5146a3` |
| 8 | fixed | `81669e1` |
| 9 | fixed | `d137aeb` |
| 10 | fixed | `1f2e9fc` |
| 11 | answered | The reviewer measured 10 at `d35c874` and 10 at `5aa83af`, same pair, and states it is not asking for the assertion to change. It does not change. What the finding found that the account did not is that the bound is on the MAXIMUM rather than per pair, so a second definition newly reaching 10 leaves the case silent — that is recorded as a `# RIDER:` at the assertion, stamped and checked, because a per-pair bound is a walk and a fix pass may not add mechanism (`skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it*). Corrected at `054c58f` |
| 12 | answered | Both records now read *a branch a worktree already held*, following #120's comment and the contract. A finding located in a record is a correction: corrected at `054c58f` |

## What the class re-enumeration found

The round's headline is that the branch's own enumeration missed the class it
was aimed at, so both classes were re-enumerated by construction rather than
swept for again.

**The probe rule.** `grep -rn test_tmp_` over every shipped `.md` returns
exactly two documents: `skills/agent-contract/SKILL.md` §7 itself, and
`skills/code-review/SKILL.md`'s Probes row — finding 1. Then every file that
mentions probes at all was opened: `agents/{warden,smith,sealer,scribe}.md`,
`skills/implement/SKILL.md`, `skills/code-review/orchestration.md`,
`docs/review-chain-spec.md`, `docs/review-handoff-protocol.md`,
`templates/{sdd-round,config,seal-README}.md` and `docs/flow.md`. Each either
points at §7 without restating it — `agents/scribe.md:43` is the shape — or does
not state the rule. Two statements, both now correct, one pinned for the first
time.

**Who the broad gate belongs to.** Every shipped `.md` carrying *the full suite
is*, *out of your hands* or *until the rounds settle*: `agents/smith.md:187`
and `agents/warden.md:53` say *the full suite is the sealer's* and are correct,
`skills/verify/SKILL.md`, `docs/review-handoff-protocol.md:503` and
`CONTRIBUTING.md:18` are correct, and `agents/warden.md:157` was the one wrong
statement — finding 2. Its case is asserted over the whole `agents/*.md` glob
rather than over that file.

**Old §6 vocabulary.** `grep -rn exception` over `agents/`, `skills/` and
`templates/`: `agents/warden.md:180` and `:283` are findings 9,
`skills/agent-contract/SKILL.md:160` is §6's own history paragraph and correct
as written, and every other hit is a different subject. Closed.

**Definitions that name a durable write without bounding it.** Enumerated over
the glob by the new case rather than by reading: `sealer.md` and `warden.md`
already closed theirs, `scribe.md` says it writes nothing anywhere, and
`smith.md` was the only one open — finding 4, and the case is red on that file
alone against the tree as it stood.

## Narrow runs

| Run | Exit |
|---|---|
| Finding 1's case against the skill as it stood | 1 |
| `tests/test_a_probe_that_commits_says_so.py` + wrap | 0 — 29 passed |
| Findings 2, 3, 9's cases with `agents/warden.md` stashed | 1 — 3 failed |
| Four modules after | 0 — 180 passed |
| Findings 4, 10's cases with both definitions stashed | 1 — 2 failed, 3 passed, red on `agents/smith.md` alone |
| Four modules after | 0 — 239 passed |
| Finding 7's case with the contract stashed | 1 |
| Finding 6's case with a second definition carrying the marker | 1 — *2 definitions assign the broad gate* |
| Finding 6's case with the marker reworded out of the sealer | 1 — *0 definitions* |
| Four modules after both mutants were restored | 0 — 153 passed |
| Finding 8's assertions with the template stashed | 1 |
| Two routing modules after | 0 — 41 passed |
| `bin/evidence-check .` | 0 — 1111 ok · 0 drifted · 0 broken |
| `.github/scripts/rider_check.py` | 0 — 25 ok · 0 drifted · 0 broken |
| `bin/survivor-check --range e972b5f..HEAD --exempt …` | 0 — no removed wording is still standing |
| `bin/survivor-check --range origin/release/v0.10.0...HEAD --exempt …` | 0 — three exempt, all rows already written |

## What is still `unverified`

The full suite, the repository-wide lint and the typecheck. §2 leaves the broad
gate to the definition that assigns it, which is `agents/sealer.md`'s.
Answered by **the sealer**, spawned once the rounds settle.

`bin/evidence-check`, which round 1 declined as possibly bundled into the broad
act, was run here scoped and unscoped: `skills/verify/scripts/broad_gate.py`
bundles it into the sealer's single command, and §2 names the full suite, the
repository-wide lint and the typecheck — not the plugin's own record checkers,
which every phase of this work item ran. The reading is disclosed rather than
assumed, and the orchestrator can overrule it.
