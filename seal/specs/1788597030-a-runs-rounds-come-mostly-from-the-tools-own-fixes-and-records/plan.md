# Implementation Plan: a run's rounds come mostly from the tool's own fixes and records

<!-- seal/specs/1788597030-…/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

## Summary

The last branch (#153 + #150) ran fifteen rounds and 22 h 47 min for two features' worth of review. Counted from its 70 commits, with gaps over two hours cut to two: **12.8 h sat in front of `docs` commits, 3.6 h in front of `fix` commits**. Half its 65 findings were located in records; a fix pass touched one or two code files and five to twelve record files; fifty of sixty-one later findings sat in a file the preceding fix pass wrote. The loop's gain was at or above one, and the cap had an exception every verifying round used.

The fix is a loop with gain below one, in the order of how much gain each removes: **a fix owes code and a test, and the record is generated** (the 12.8 h and the 33 record-located findings); a verifying round that finds a record defect corrects it and owes no round; a fix pass adds no mechanism; 🟡 has a threshold; the reopening is one. It alters what a gate refuses, what a script writes, and what three agents are told — the top rung — so this plan comes first.

## Technical context

- `skills/code-review/scripts/chain_check.py` — `read_record:703` reads `git show HEAD:<rel>`, which is why a check before the record commit sees nothing; `CLOSED_WORDS:325` / `FIX_WORDS:331` are the verdict vocabulary; `stopping_floor:2348` walks `later` and stops at the first record that `run_reopened:2298` or `wrote_fixes:2317`, and every reopening record is itself a floor record, so the walk restarts and the chain is unbounded by construction; `depth_problems:1672` and `DEPTH_RE` are the `New units` grammar; `fix_surface:1718` and `checked_by:1375` are the reach-back refusals; six cutoff constants `*_FROM:387-527` are the grandfathering shape; `main:2662` takes `--baseline` and `--root`.
- `skills/verify/scripts/unverified_check.py` — the shared reader `chain_check` loads (`READER:307`): `table_rows`, `visible`, `readable`. The generator loads the same two modules the same way and defines no string they hold.
- `templates/sdd-round.md` — nine field rows and four sections; the comments are the documentation and are not copied into a generated record.
- `agents/warden.md` §Report (`:209`) — free-form findings plus two lines. The tables move in here.
- `agents/smith.md:114` — a phase record at every phase's close; on the last branch phases 5–17 were fix passes. `:174` — the depth rule the generator enforces.
- `skills/code-review/SKILL.md:184-340` — the verifying round, the floor, the *Unless* paragraph at `:262`; `:339-497` the four reach-backs; `:549` the findings format.
- `docs/review-chain-spec.md:32-145` — the bound, the floor, the verifying round; `:1005` *What the record carries*. The count rule has eight carriers (`grep -rn "at most one more"` finds four; `stopping_floor`'s docstring and message, the protocol `:314`, the template `:154`).
- `tests/conftest.py` — `repo`, `declare_routing:214`, `rounds_dir:245` build the fixture repositories every checker test uses; the generator's tests use the same.
- 53 of 72 test files read prose. A rule this work changes is pinned somewhere; the pin is re-pointed to the new sentence, never deleted.

**What breaks in six months.** The warden's report headers and the generator's parser are two carriers of one shape, and they drift. Mitigation, built in phase 1: the generator's headers are `chain_check`'s constants (`VERDICTS`, `VERDICT_COLUMN`), and a test pins `agents/warden.md` §Report against them. Second: the generator becomes the place a session hides prose — a `--grounds` flag, a `--note`. Mitigation: it takes files and structured values only, and a case feeds it a comma inside a unit name and sees it refused.

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| Rules only, no generator | 15 → 3 rounds, and 50 min of record-writing per round stays: 2.5 h of the 3 h budget in records | Rejected — Q1 |
| The verifying round as a probe re-execution script | Needs a runnable probe list, which is a new parsed field; the moratorium refuses it, and its value is unmeasured while the generator's is 12.8 h | Deferred to 0.8.2, measured first |
| A `PreToolUse` hook that runs `chain_check` on every record write | A new gate for a check the generator can run itself in three seconds; #158 measured what a gate costs in auto mode | Rejected — the generator runs it |
| A new `Needs a fix` value for a capped run | Changes a row the reviewer owns and every carrier that reads it | Rejected — A4, a verdict word |
| Remove the reopening exception entirely | Round 7's floor bug and three Windows defects ship as issues on the last branch | Rejected — Q2, bounded to one |
| The generator reads the warden's free-form report | No deterministic parse; the orchestrator re-reads the report and types the table, which is the prose this work removes | Rejected — the report carries the tables |

## Phases

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | `round_record.py new` — the record from a warden report and the round paragraph, every field derived, the previous record's `Fixes checked by` set, `Pass` ticked when nothing is open, `chain_check --worktree` run before return; `agents/warden.md` §Report carries the three tables in the record's headers; `chain_check.py --worktree` | a case per field derivation on a fixture repository; the two-record reach-back read back; a comma in a cell refused; the warden headers pinned to the generator's constants; `--worktree` seen red in both directions before the flag exists | `aa5864b` |
| 2 | `round_record.py close` — the smith's fix table applied to verdict cells, `Contract changes` and `New units` from the AST diff over the fix range, depth per entry, **depth 2 refused before any cell is written**; `agents/smith.md` and `implement` §5 hand over a fix table and write no phase record for a fix pass | the surface cases against a real diff, both cells read back; the depth-2 refusal seen red; the non-Python heuristic on one fixture file; the two agent sentences pinned | `d53021d` |
| 3 | `chain_check.py`: `deferred <home>` closes, bare `deferred` stays open; the reopening bound behind `REOPEN_FROM`, refusing the second fix-closing record after a floor record and printing for earlier items; `docs/review-chain-spec.md` gains the subsection beside the eight | each refusal seen red at a named fixture; the two-record run kept green; the cutoff case at the boundary second; this repository's own records under the new arm | |
| 4 | The rules in their carriers, one owner each: record-located findings owe no round; no mechanism from a fix pass; 🟡 threshold and ⬜; the reopening is one, stated in the spec and linked from the other seven carriers; a fix pass owes code and a test; the draft pull request before round 1; a compacted session hands over; the moratorium; the orchestrator re-runs a closed phase's suite and lint before spawning the next (rule 9, in `docs/review-handoff-protocol.md` §*While the implementer runs* as a new subsection and one sentence in `code-review`'s orchestrator section). `templates/sdd-round.md` says a record is generated | every changed sentence pinned, each pin seen red with the sentence stashed; the count-rule carrier pin re-pointed; the doc suites | |
| 5 | The fragments and the memo — `changelog.md`, `seal/ledger/<id>.md` rows for the generator, the bound and the vocabulary; `overview.md` closed; the draft pull request opened | `evidence-check .` unscoped, `fold_ledger --check`, `unverified-check`, `chain_check --worktree` on this item | |

Phase 1 before everything: this branch's round 1 record is the generator's first fixture (A3), so the writer exists before the first round. Phase 3's subsection in the same phase as its refusal, the ordering this repository has learned four times. Phase 4 last among the rule edits because its pins are what the earlier phases' tests would otherwise be written against twice.

**This branch's own chain runs under phase 4's rules before phase 4 ships**, in the spawn prompt of every round, because a rule change binds sessions after the release and the rounds in front of it are not protected by it.

## Operational impact

- **No migration, no environment variable, no dependency.** `gh` is consulted for the `PR` cell and its absence reads `not yet opened`.
- **A new script ships** under `skills/code-review/scripts/`; the version moves at the release, as the hygiene workflow requires.
- **A verdict word is added**, `deferred <home>`; every existing record keeps its meaning, since an unknown word was open before and a bare `deferred` is open still.
- **A refusal is added**, bounded by work-item id — the shape six cutoffs take. **Failure direction: blocks more.** A run that reopens twice is refused where it used to pass; the trade is the one Q2 chose, stated with what it lets through: a defect found by the second reopening ships as an issue rather than as a round.
- **`--worktree` is local only.** CI keeps reading `HEAD`, because a working tree that differs from HEAD is what CI never sees and the more permissive direction is the wrong one there (`read_record`'s docstring).
- **Prompt budget: zero.**
