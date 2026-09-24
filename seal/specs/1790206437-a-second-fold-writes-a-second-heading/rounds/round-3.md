# 1790206437-a-second-fold-writes-a-second-heading — review round 3

| Field | Value |
|---|---|
| Target SHA | 74a93fea352de078ad7540a994d0367ee60a3d21 |
| Written late | no |
| Ran by | warden on Opus 5.5 |
| PR | 552 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | `74a93fea352de078ad7540a994d0367ee60a3d21..013a5278afcf878e868e0fc1c7b1a0a2cecd1670`, 1 commit |
| Contract changes | none |
| New units | none |
| Needs a fix | yes — 🟡 9, the two `round_record.py` comments that state the pre-`same_run` rule; deferred to #556 because the run is capped |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 3, the last round of the run — round 2 opened a 🟡 and spent the one reopening — reviewed at 74a93fea: round 2's fix range `9da6a303..fd6a8fd3`, one commit of docstrings and prose. It asked whether the thirty-one-minute gap now stands in every carrier, re-measured; whether every rewritten same-run sentence names the newest entry as `same_run(entries[0], value)` does, with one more class grep across `agents/`, `docs/`, `skills/` and `templates/` for a carrier that still says any held run is replaced or always kept; and whether the orchestrator's corrections to #553 and PR #552's body hold. Anything it opened needing a fix goes to a named home rather than onto this branch.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 9 | two comments above the `kept_broad_gate` call say a held run is kept, with no same-run replace — #542's class in #542's file, which phase 3's grep terms did not match | `skills/code-review/scripts/round_record.py:3955-3956`, `:4516-4519` (and `agents/sealer.md:189`, weaker) | deferred #556 | read — `kept_broad_gate` drops `entries[0]` on `same_run`; `:3955-3956` is word for word the `orchestration.md` sentence phase 3 judged *same falsehood* and reworded; phase 3's grep terms (`phases/phase-3.md`) do not match *is kept behind*; the enclosing units `close` and `seal` predate the work item, so the cap defers it; a new issue the orchestrator files |
| ⬜ 10 | #553's correcting comment gives the target's twenty pairs as *at 9f846733* | issue #553, the comment of 2026-09-24T00:53:35Z | answered | corrected outside the tree by the orchestrator: #553's correcting comment no longer lists the tip's pair lines under *at 9f846733*; it points at the issue body, which lists them at 9f846733 and names the two-line shift; executed — pairs recounted at 9f846733 and 74a93fea; the comment's update time equals its creation time; the body is correct; the orchestrator's, outside the tree, out of `Needs a fix` |
| 🟢 | round 2's 🟡 5 is closed — every in-tree carrier states the measured thirty-one minutes, with `bee7ae99` as the preparation commit | `tests/test_release_hygiene.py:1117-1123`, `tests/test_the_ledger_fragments_fold_at_release.py:314-318`, fragment row F3, `spec.md:16-22`, `questions.md:13-15` | verified | executed — `git log -1 --date=iso-strict` and `TZ=UTC` on both commits (02:04:21 and 02:35:35 +0900; 17:04:21 and 17:35:35 UTC on 2026-09-08); `4ac9bf35` the child of `bee7ae99`; both headings `2026-09-08`; no *day after*, *next day* or similar on this subject in the tree outside the round records |
| 🟢 | round 2's ⬜ 6 is closed — the five rewordings name the newest entry as the one a same comparison replaces | `agents/sealer.md:139-143`, `docs/review-chain-spec.md:341-346`, `skills/code-review/scripts/chain_check.py:3662-3669`, `skills/code-review/orchestration.md:527-529`, `:536-539` | verified | read against `kept_broad_gate` and `same_run(entries[0], value)`; the handoff-protocol row, the template row, the written comment and the docstring were already precise; executed — `survivor-check` over the fix range, 24 removed sentences, none standing; the narrow modules green |
| 🟢 | round 2's ⬜ 7 is answered — #553's title and body say twenty and list 9f846733's pairs | issue #553 | answered | executed — `gh issue view 553`; the twenty pairs recounted at 9f846733 match the body; the comment's leftover is ⬜ 10 |
| 🟢 | round 2's ⬜ 8 is answered — the pull request body says the doubled-version arm is silent and `--check` exits 1 on the unfolded fragment, and gives thirty-one minutes | pull request #552 body | answered | executed — `gh pr view 552`; `fold_ledger.py --check --root .` exits 1 naming only this branch's fragment |
| 🟢 | the ten ledger rows re-stamped with dated or narrowed notes; the ledger resolves | `seal/ledger.md` G2, S9, R1, C4, A5, the seam row, the `no fixes to check` row, the needs-no-second-reader row; the fragment's F1, F3 | verified | executed — `evidence-check --strict .` `1686 ok · 0 drifted · 0 broken`; `correction-check` exit 0; read — each changed segment against the sentence it describes |
| 🟢 | round 1's four findings stay closed — the count clause round 1's 🟡 1 fixed survives the rewrite of the same docstrings | `tests/test_release_hygiene.py:1117-1123`, `tests/test_the_ledger_fragments_fold_at_release.py:314-315`, F3 | verified | read — seventeen sections and eighteen tags still stated; the range touches no other round-1 surface |
| ❓ | the broad gate — the full suite, the repository-wide lint and the format check over the settled branch | the sealer's `broad-gate` run | ❓ out of verified scope | `agent-contract` §2 keeps it from this round; the sealer answers it, and its spawn comes due once this round's record is closed with 🟡 9 deferred |

## Paste-ready fixes

```
    # Through the same path as `seal` (round 1's 🟡 1): a run the cell
    # already holds is kept behind the new entry by either writer, and the
    # newest, where it is the same commit against the same base, is replaced
    # by either (`same_run`).
```
```
    # ONE ENTRY PER RUN, NEWEST FIRST (#174). A run the cell already holds is
    # kept behind the new one as `earlier run`, because a second broad run --
    # after a pre-existing failure, or after the last fixes landed -- used to
    # REPLACE the first and the run-level table was then filled from memory.
    # The newest entry alone is replaced, where it is the same commit against
    # the same base (`same_run`).
    # `kept_broad_gate` is the one path, shared with `close --broad-gate`.
```
```
  entry of the cell records — the newest first, and every earlier comparison
  kept behind it. A tree that moves afterwards is a tree with no seal on it.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_ledger_fragments_fold_at_release.py tests/test_release_hygiene.py tests/test_the_broad_gate_cell_keeps_every_run.py tests/test_no_real_identifiers.py tests/test_docs_line_wrap.py tests/test_one_word_one_meaning.py -q` in the clone at 74a93fea | 151 passed, exit 0 |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` | exit 0; `total: 1686 ok · 0 drifted · 0 broken · 0 external · 0 old-format` |
| `python3 skills/evidence-check/scripts/correction_check.py --range 9f846733...HEAD` | exit 0; no merge commit in the range |
| `bin/survivor-check --range 9da6a303..fd6a8fd3`, with and without `--exempt` the work item's `survivors.md` | 399 files against 24 removed sentences; no removed wording standing either way |
| `python3 .github/scripts/fold_ledger.py --check --root .` | exit 1, naming only this branch's unfolded fragment; no doubled-version report |
| `uvx ruff check` and `uvx ruff format --check` on the two test files and `chain_check.py` | all checks passed; 3 files already formatted |
| `git log -1 --date=iso-strict`, and the same under `TZ=UTC`, on `bee7ae99` and `4ac9bf35` | `2026-09-09T02:04:21+09:00` / 17:04:21 UTC 2026-09-08; `2026-09-09T02:35:35+09:00` / 17:35:35 UTC 2026-09-08 |
| `git log -S'## 0.9.3 — ' -- seal/ledger.md`; `git log bee7ae99..4ac9bf35`; the `0.9.3` heading lines at both commits | `bee7ae99`, `4ac9bf35`, `d08c671`; one commit between; line 1683 at `bee7ae99`, 1683 and 1774 at `4ac9bf35`, both dated 2026-09-08 |
| `git grep -i -E "day after\|next day\|a day later\|following day"` over the tree, round records excluded | nothing on this subject |
| `git grep` for the same-run wordings (*same commit against the same base*, *same comparison*, *taken again*, *its own entry*, *already held*, *already holds*, *every earlier run*) over `agents/`, `docs/`, `skills/`, `templates/` | the five reworded carriers name the newest; `round_record.py:3955-3956` and `:4516-4519` state no replace (🟡 9); `agents/sealer.md:189` weaker |
| the twenty doubled marker pairs located at 9f846733 and at 74a93fea | 9f846733's pairs match #553's body; from `1773/1776` on, the comment's numbers are the target's |
| `gh issue view 553 --json title,body,comments`; `gh api` on its comments | title and body say twenty; the comment's update time equals its creation time |
| `gh pr view 552 --json isDraft,baseRefName,headRefOid,body` | draft, base `release/v0.15.1`, head 74a93fea; *thirty-one minutes*; the doubled-version arm silent, `--check` exit 1 on the fragment |
| the broad gate — the full suite, the repository-wide lint and the format check | not yet |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `.github/scripts/fold_ledger.py:24` (and `tests/test_release_hygiene.py:1120`, `tests/test_the_ledger_fragments_fold_at_release.py:314`, the changelog fragment lines 6–7, fragment row F3's Notes) | round 1's 🟡 1 — fixed |
| round-1 | `seal/specs/1790206437-a-second-fold-writes-a-second-heading/overview.md` §Not done, `phases/phase-5.md` §What this phase found, pull request #552 §Found outside the item | round 1's ⬜ 2 — fixed |
| round-1 | `docs/review-chain-spec.md:342-343`, `agents/sealer.md:140-142` | round 1's ⬜ 3 — fixed |
| round-1 | pull request #552 body | round 1's ⬜ 4 — answered |
| round-1 | the four test modules the diff adds to | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/fold_ledger.py:398-411`, fragment row F2 | round 1's 🟢 — confirmed |
| round-1 | `.github/scripts/fold_ledger.py#insert` | round 1's 🟢 — confirmed |
| round-1 | the sealer's `broad-gate` run | round 1's ❓ — out of verified scope |
| round-2 | `tests/test_release_hygiene.py:1118-1119`, `tests/test_the_ledger_fragments_fold_at_release.py:317`, fragment row F3's Notes (and `spec.md:19`, `questions.md:14-15`) | round 2's 🟡 5 — fixed |
| round-2 | `agents/sealer.md:140-142`, `docs/review-chain-spec.md:343-344`, `skills/code-review/scripts/chain_check.py:3667-3668` (and `skills/code-review/orchestration.md:527-529`, `:537-539`) | round 2's ⬜ 6 — fixed |
| round-2 | issue #553 | round 2's ⬜ 7 — answered |
| round-2 | `.github/scripts/fold_ledger.py:23-26`, `tests/test_release_hygiene.py:1119-1123`, `tests/test_the_ledger_fragments_fold_at_release.py:314-315`, the changelog fragment, F3 | round 2's 🟢 — verified |
| round-2 | `overview.md` §Not done, `phases/phase-5.md` | round 2's 🟢 — verified |
| round-2 | `agents/sealer.md:139-143`, `docs/review-chain-spec.md:341-346`, `skills/code-review/scripts/chain_check.py:3662-3669` | round 2's 🟢 — verified |
| round-2 | `seal/specs/1790206437-a-second-fold-writes-a-second-heading/survivors.md` | round 2's 🟢 — verified |
| round-2 | `seal/ledger.md` G2, S9, R1, C4, A5 and two unnamed rows; the fragment's F1, F3 | round 2's 🟢 — verified |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| 🟡 9 · two comments in `round_record.py` (`close`, `seal`) say a held run is kept with no same-run replace; `agents/sealer.md:189` weaker | #556, milestone `release: 0.15.1`, taken by the document item `1790208643`; the run is capped and the units predate the work item | the orchestrator, who files it; the smith of the work item that takes it |
