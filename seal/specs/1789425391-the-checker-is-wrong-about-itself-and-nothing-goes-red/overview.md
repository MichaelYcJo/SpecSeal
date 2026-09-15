# 1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red — overview

📋 implement applied
· spec:     `CLAUDE.md` (§*The goal a design is chosen against*, §*a change writes fragments, never the shared file*, §*A ledger coordinate names content, never a position*, §*no real identifiers*), `skills/agent-contract/SKILL.md` §§1, 2, 5, 6, 7, 8, 9, 12, 14, 15, `skills/implement/SKILL.md` §§1–4, `docs/review-chain-spec.md` (§*A verdict row that commissions nothing*, §*The depth in `New units`*, §*What the record carries*, §*The reopening*), `docs/review-handoff-protocol.md` §*The `Fixes checked by` field*, `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it*, `templates/sdd-round.md` (§*New units*, §*Inherited coordinates*), and this work item's `spec.md`, `plan.md`, `questions.md`, `routing.md`
· evidence: nine rows in `seal/ledger/1789425391-the-checker-is-wrong-about-itself-and-nothing-goes-red.md`, the fragment's first write; eight `seal/ledger.md` rows re-read and re-stamped (F12, R1, R2, R6, S6, S10, S12, S13, and the review-arm heading row), none appended to
· verified: executed — the six phases' narrow modules at each boundary, and 27 mutations across the six phases, each killed. Read — nothing claimed as passing that was not run. Unverified — the broad gate, which is the sealer's

## Why this work exists

Six tickets that every one came out of a review round exercising the review
chain's own checker, and every one is that checker saying something false while
the suite stays green; after this, each of those states turns a case red.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| The corpus size | `plan.md` §Summary and `spec.md` S16 say *this repository's own 176 records* | **211 of 212 parse**, measured at `dd6af99` | 176 was round 4's count at `151792e`, in a clone of a branch that had not met `release/v0.11.4`. The merge brought 35 more records in. `plan.md` §*#331's trap* is the clause that forbids carrying a figure across, and it applies to its own document's figure |
| `SUMMARY_WORDS` | `spec.md` S11 builds a case on *the measured #30 shape (🟡 13 at `:386-395` inside `SUMMARY_WORDS`)* | The shape, with underscore-free parent units; the name annotated `NAME NOT IN TREE` | `git log -S` over `broad_gate.py` on every branch finds the name in no merged commit — it lived between #30's round-1 and round-2 fixes and the squash discarded both. `COUNTS_RE` reads the summary line today. What S11 is about is the SHAPE — two findings in one file, each inside a different earlier unit — and that is what the cases build |
| The `close` half of S2 | Round 4 verified a numbered short row through `close` by probe and left it a probe | A case | `spec.md` S2 says *cases on both subcommands*, and `plan.md` phase 2 says `new` **and** `close`. A probe re-run proves nothing about the next change |
| The positive control's strength | `plan.md` phase 1: *both `failures.extend(errors)` replaced with `pass` must turn a case red* | A fixture that turns it red when **either** is stubbed | The fixture costs nothing more — one record with an empty `New units` row and an empty floor row — and the weaker acceptance leaves each half individually unpinned |

## Not verified

| Item | Who must answer |
|---|---|
| The broad gate — the full suite, the repository-wide lint, the typecheck. None of the three was run: `skills/agent-contract/SKILL.md` §2 assigns all three to `agents/sealer.md`, once, after the rounds settle | `agents/sealer.md`, spawned by the orchestrator after the review rounds settle |
| Whether the depth-2 walk should reach a parent unit whose name carries an underscore. `units_named_earlier` runs each `New units` entry through `chain.EMPHASIS` (`[*_`]+`) applied to the whole entry, so `only_tested` is read back as `onlytested` while `added` names come from the AST unstripped — the walk therefore reaches no snake_case parent, which is most Python units. Measured 2026-09-15 while building #333's cases; recorded as a stamped `# RIDER:` at the coordinate with the repair named. Outside this work item's six tickets, and widening what the rule refuses is a change to a gate | the repository owner |
| Whether the `New units` / `Contract changes` pair reading *none — the fixes are not yet written* beside a sealed `no fixes to check` should be refused. Q1, answered **(a) leave it open** by the owner before the build | the repository owner, in 0.12.0 beside #174 |

## Not done

**Q1's cost, which is the sentence the answer was bought with.**
`docs/review-chain-spec.md` §*What the record carries* records, as an open
problem, that `no fixes to check` beside a fix-surface row still reading
*none — the fixes are not yet written* is *the one place the pair is not merely
unrefused but wrong*: a round that commissioned no fixes will never have any.
Phase 4 makes `no fixes to check` the only value `seal` will write a `Broad
gate` cell beside — so **every sealed record is now a member of that population
rather than an edge of it**, and the next reader meets the spec's open note over
a wider set than it was written about. The owner answered (a) before the build,
the scope line in `spec.md` is what it rests on, and this paragraph is the whole
of what the answer costs.

**The five tickets the owner moved to `release: 0.12.0`** — #344, #174, #159,
#149 and #331 — are untouched. #331's discipline is applied (`plan.md`
§*#331's trap*) and its sweep is not built.

**Round 4's ⬜ 5 is taken as the sentence rather than the list.** The short-row
guard still raises on the first offending row where `id_refusal` beside it names
every one. The grounds were re-checked here — the guard was already immediate
before the verdict arm and only its condition widened, and zero of the 2,044
committed verdict rows are short — and the comment now says which it is, why,
and what the repair is if anybody opens the function again.

**Round 4's ⬜ 6 was moot.** The three-word line `test, and the` came from a
rewrap of a paragraph `1ff0a6c` reverted, so the tree never carried it.

## Fed back into the spec

**`docs/review-chain-spec.md` §*A verdict row that commissions nothing*** — that
the record is read in two cells; that the open verdict ends on a space, a comma
or nothing and is NOT `chain.SEPARATORS`; and that the ruling *the verdict word
cannot do this job* argues against a vocabulary test rather than against reading
the cell. Inferred during implementation from round 4's measurements, and pinned
by two cases because `survivor-check` is structurally blind to an overturned
claim left standing.

**`docs/review-chain-spec.md` §*The depth in `New units`*** — that the
generator's refusal names the finding whose fix commit added the unit, and that
where the range cannot resolve one it still refuses and says the attribution is
file-level. Inferred during implementation; a planner may overturn the second
half, and `plan.md` §*The two judgments* holds the argument.

**`templates/sdd-round.md` §*Inherited coordinates*** — that the `Why` cell is
filled twice and the second time is `close --round N-1`'s, with its two refusals
and its silence. Inferred during implementation.
