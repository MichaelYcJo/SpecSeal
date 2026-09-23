# 1790174138-the-report-the-record-and-the-cells-disagree-on-one-format — review round 3

| Field | Value |
|---|---|
| Target SHA | 8b04523a831b9268f1ff39c980b5f64137a6e285 |
| Written late | no |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | 541 |
| Broad gate | not yet |
| Fixes checked by | no fixes to check |
| Fix range | none |
| Contract changes | none |
| New units | none |
| Needs a fix | no — ⬜ 1 is prose beside behaviour the template, the sealer and the code agree on, deferred to a ticket the owner files; the two corrections are paperwork |
| Loses a record or crashes | no — nothing found writes outside `seal/specs/` or raises; the one erasure round 2 opened is closed, and a same-run re-seal replaces an entry with the same bytes |

- [x] Pass

## What this round was asked

Round 3 of the review record's shape, the verifying round at round 2's fix and the round that ends the run: the range `43afbc1e..db292bfb` on `fix/503-the-report-the-record-and-the-cells-disagree-on-one-format`, two commits, plus the record commits that closed round 2, against the branch's base `0b8dc4b2`. It asked whether 🟡 1 is closed as the record says — `same_run` keys the replace on commit AND base, `kept_broad_gate` replaces only on `same_run`, the same-commit-other-base case was red at `43afbc1e` and is green, the reshaped same-base case still pins the replace, and the template sentence and A9 say what the code does — and whether ⬜ 2's new stands phrase is absent at the base and present at the target, ⬜ 3's docstring is true of both callers, and the two paperwork corrections (A11 in the fragment, round 1's 🟡 2 grounds cell at `e101abac`) state what `GATE_CARRIERS` pins. It also asked whether the three mutations reproduce and whether the fix range touched anything the finding did not name. The reopening is spent: this record ends the run whatever it finds, and anything it opens goes to a ticket, not a fix pass.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| ⬜ 1 | the `broad-gate.md` comment says a run taken again leaves the earlier one behind it, and the docstring says the count of entries is the count of runs; under `same_run` a same-run re-seal replaces and is two runs in one entry; no test reads the written comment | `skills/code-review/scripts/round_record.py:4278-4280`, `:363-365` | deferred to #542, filed from this record by the orchestrator | read — the comment against the replace at `:380-381` and the template's clause; executed — the grep over `tests/` hits one docstring and nothing that reads the file; round 2's regression row for the comment was not planted |
| ⬜ | A9's last clause says the count of entries is the count of runs; a same-run re-seal is two runs and one entry, so the count is of distinct comparisons | `seal/ledger/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format.md:20` | answered — corrected at d1f9ea1f | read — the clause against `kept_broad_gate:380-381`; the previous text said *runs at distinct commits* |
| ⬜ | the `seal/ledger.md` row anchored on the template's field table was re-hashed at `21b8d61e` and `db292bfb` with no re-read note, while S5 carries one per move; the claim holds | `seal/ledger.md:88` | answered — corrected at d1f9ea1f | executed — the anchor `@22992524` → `@35e76377` → `@4286fbab`, last note 2026-09-10; read — the template's `Needs a fix` row is untouched on the branch |
| 🟢 | round 2's 🟡 1 — `same_run` keys the replace on commit AND base, `kept_broad_gate` replaces only on `same_run`, the another-base case is red under the SHA-alone rule and green at the target, the same-base case pins the replace, and the template and A9 say what the code does | `skills/code-review/scripts/round_record.py:376-402`; `tests/test_the_seal_is_taken_once_by_the_sealer.py:2555-2594`; `templates/sdd-round.md:39`; the fragment's `:20` | verified | executed — m1 red at the another-base case alone with the cell holding one entry, m2 red at the same-base case alone, m3 red at four re-seal cases including the direct home; read — the helper and the two sentences |
| 🟢 | round 2's ⬜ 2 — the verify skill's stands phrase is absent at `0b8dc4b2` and present once at the target, and removing it turns the stands half red | `tests/test_the_broad_gate_cell_keeps_every_run.py:57-61`; `skills/verify/SKILL.md:456` | verified | executed — 0 at the base, 1 at the target; m4 red at `test_every_carrier_says_the_cell_holds_one_entry_per_run` |
| 🟢 | round 2's ⬜ 3 — the docstring is true of both callers: `seal` refuses a flag with no SHA-shaped word or one that does not resolve, `close` writes its flag as typed | `skills/code-review/scripts/round_record.py:371-375`, `:3956-3960`, `:4484-4493` | verified | read — `close`'s body consults `SHA_RE` nowhere and `resolves_to` only for the fix table's commits |
| 🟢 | the two paperwork corrections — A11 in the fragment and round 1's 🟡 2 grounds at `e101abac` — state what `GATE_CARRIERS` pins: eight documents, the `broad-gate.md` comment unpinned | the fragment's `:22`; `rounds/round-1.md:36` | confirmed | read — eight tuples in `GATE_CARRIERS`; each cell's *ninth carrier* names a different thing and each is true in its count |
| 🟢 | the fix range touched nothing the findings did not name: six files, every hunk one of 🟡 1, ⬜ 2, ⬜ 3, the paperwork row or a re-anchor moved by the template's row; the range is two commits as the record states | `git diff --stat 43afbc1e..db292bfb`; `rounds/round-2.md` | verified | read — every hunk mapped; executed — `git rev-list --count` 2; `evidence-check --strict` exit 0, 1624 ok |
| 🟢 | the new units as code — `same_run` and the another-base case — are correct; `zip(strict=True)` sits behind a length guard within the Python 3.12 floor | `skills/code-review/scripts/round_record.py:386-402`; `tests/test_the_seal_is_taken_once_by_the_sealer.py:2580-2594` | verified | executed — the three modules and m1–m3; read — the punctuation edge yields a duplicate and never an erasure |
| 🟢 | round 2's record at `8b04523a` states the fix as it landed — 🟡 1, ⬜ 2 and ⬜ 3 fixed at `fb960e6c`, the paperwork row answered at `e101abac`, the fix range two commits, two new units at depth 1 | `rounds/round-2.md:11-16`, `:28-31` | verified | read — against the fix range's diff; executed — the commit count |
| 🟢 | round 1's and round 2's 🟢 rows stand; the rows resting on `kept_broad_gate` and the carrier module were re-derived by the modules and mutations above | `rounds/round-1.md`; `rounds/round-2.md` | confirmed | executed — the seal, close and carrier modules at the target; read — the other rows cover code the fix range did not touch |
| ❓ | the broad gate — the full suite, tree-wide `ruff check` and `ruff format --check`, `evidence-check --strict` over the tree the sealer stands on, taken once now that the rounds have settled | the last record's `Broad gate` cell | ❓ out of verified scope | contract §2 assigns the run to the sealer; this round leaves nothing open, so the sealer's spawn is due; this round's `evidence-check` and per-file ruff are probes over the clone, not the gate |

## Paste-ready fixes

```python
        "having run. One entry per run, newest first: a run at a new commit,\n"
        "or at this one against another base, is written in front and the\n"
        "earlier one stays behind it as `earlier run`; a run the newest entry\n"
        "already records — the same commit against the same base — replaces\n"
        "it. The reader takes the first SHA as the run. -->\n"
```
```python
    two entries for one claim would make the count of entries stop being
    the count of distinct comparisons — commit and base — which is what
    the run-level table reads off the cell.
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py tests/test_the_broad_gate_cell_keeps_every_run.py tests/test_the_fixes_close_the_record.py -q` in the clone at `8b04523a`, exit read from the file it was written to | `232 passed in 215.75s`, exit 0 |
| baseline before any mutation: the seal module `-k "re_seal or another_base"`, and the carrier module | 7 passed, 119 deselected, exit 0; 3 passed, exit 0 |
| m1 — `same_run`'s `elif x != y` arm disabled, so only SHA-shaped words are compared (the rule at `43afbc1e`) | `test_a_re_seal_at_the_same_commit_against_another_base_keeps_both` 1 failed with the cell `f302329 against origin/base`, 6 passed, exit 1 |
| m2 — the replace dropped (`entries = entries[1:]` → `pass`) | `test_a_re_seal_at_the_commit_the_cell_names_replaces_that_entry` 1 failed with the commit entered twice, 6 passed, exit 1 |
| m3 — `same_run` returns True unconditionally | 4 failed (`…keeps_the_earlier_run…`, `…replaces_that_entry`, `…keeps_both`, `test_the_direct_home_takes_the_same_shape_on_a_re_seal`), 3 passed, exit 1 |
| m4 — `skills/verify/SKILL.md:456` loses `[; earlier run: <sha> vs base <sha>]` | `test_every_carrier_says_the_cell_holds_one_entry_per_run` 1 failed naming that carrier, 2 passed, exit 1 |
| after every mutation `git checkout --` on the file; `git status --porcelain` in the clone | clean |
| `git show 0b8dc4b2:skills/verify/SKILL.md`, grep counts of `; earlier run: <sha> vs base <sha>` and of `earlier run`, then the same at the target | 0 and 1 at the base; 1 and 2 at the target |
| `python3 skills/evidence-check/scripts/evidence_check.py --strict .` in the clone, exit read directly | exit 0 — `total: 1624 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records arm 0 refused, 0 drifted |
| `uvx ruff check` and `uvx ruff format --check` over the three `.py` files the fix range edited, exits read directly | exit 0 and exit 0; `All checks passed!`, `3 files already formatted` |
| `git rev-list --count 43afbc1e..db292bfb` | 2 |
| the anchor hash of the `seal/ledger.md` row *The answer a run ends on had no field* at `0b8dc4b2`, `21b8d61e`, `43afbc1e` and the target | `@22992524`, `@35e76377`, `@35e76377`, `@4286fbab`; last note 2026-09-10 at every one |
| `grep -rn "stays behind it\|a run taken again\|earlier one stays" tests/` | one docstring, `tests/test_the_seal_is_taken_once_by_the_sealer.py:2556`; nothing reads a written `broad-gate.md` for the sentence |
| this report through `round_record.py new --round 3 --target 8b04523a… --baseline 0b8dc4b2` in the clone, then `evidence-check --strict` with the report in place; the record it wrote and its reach-back into `round-2.md` undone in the clone (the worktree's record is the orchestrator's to write) | `new` exit 0 — `Pass` ticked with ⬜ 1 read as closed on `deferred`, both terminal lines copied as values, 12 verdict rows and both fenced blocks carried, `Fixes checked by` reads `no fixes to check`, and the generator printed that this record ends the run and the run is capped; `evidence-check` exit 0, 1624 ok, 641 names read, 0 refused |
| the broad gate — full suite, tree-wide lint and format check, `evidence-check --strict` at the tree the sealer stands on | not yet |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/code-review/scripts/round_record.py:3883`, `:4067`, `templates/sdd-round.md:39`, `skills/code-review/orchestration.md:535` | round 1's 🟡 1 — fixed |
| round-1 | `agents/warden.md:320-322`; `plan.md:74-77` | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:1086-1090`, `skills/code-review/scripts/chain_check.py:1569-1583` | round 1's 🟡 3 — fixed |
| round-1 | `agents/warden.md:466` | round 1's ⬜ 4 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:2093-2102` | round 1's ⬜ 5 — fixed |
| round-1 | `docs/review-chain-spec.md:982-984`, `skills/code-review/SKILL.md:332-334` | round 1's ⬜ 6 — fixed |
| round-1 | `tests/test_the_report_standard_is_one_in_three_places.py` | round 1's ⬜ 7 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py:4441-4444` | round 1's ⬜ 8 — fixed |
| round-1 | `round_record.py:2003-2016`, `:2081-2092`; `docs/review-chain-spec.md:1517-1518` | round 1's 🟢 — verified |
| round-1 | `chain_check.py:1180-1223`, `:1529-1533`; `round_record.py:1006-1032`, `:1035-1048`, `:1219-1224`, `:2119-2125`, `:2215` | round 1's 🟢 — verified |
| round-1 | `chain_check.py:1862-1894` against `:2641-2648`; `evidence_check.py:2065-2103` | round 1's 🟢 — verified |
| round-1 | `round_record.py:4313-4319`, `:4441-4444`; `chain_check.py:3684`, `:3723`, `:4012-4021` | round 1's 🟢 — verified |
| round-1 | `agents/warden.md:423-441`, `:443-453`, `:464-471`; `tests/test_the_report_standard_is_one_in_three_places.py` | round 1's 🟢 — verified |
| round-1 | `tests/test_a_release_is_sized_by_a_criterion.py:100-142` | round 1's 🟢 — verified |
| round-1 | `overview.md:26-32` | round 1's 🟢 — verified |
| round-1 | `round_record.py:1397`, `:1973-1975`; `templates/sdd-round.md` diff; `chain_check.py:4012-4021` | round 1's 🟢 — verified |
| round-1 | `seal/specs/1790174138-…/survivors.md:17-20` | round 1's 🟢 — verified |
| round-1 | the last record's `Broad gate` cell | round 1's ❓ — out of verified scope |
| round-2 | `skills/code-review/scripts/round_record.py:376-381`, `:4259-4261`; `agents/sealer.md:141`, `:186-188`; `docs/review-chain-spec.md:341-343`; `templates/sdd-round.md:39` | round 2's 🟡 1 — fixed |
| round-2 | `tests/test_the_broad_gate_cell_keeps_every_run.py:54-58`; `skills/verify/SKILL.md:456`, and `:783` at the base | round 2's ⬜ 2 — fixed |
| round-2 | `skills/code-review/scripts/round_record.py:367-368`, `:4554` | round 2's ⬜ 3 — fixed |
| round-2 | `seal/ledger/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format.md:22`; `seal/specs/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format/rounds/round-1.md:36` | round 2's ⬜ — answered |
| round-2 | `skills/code-review/scripts/round_record.py:347-385`, `:3936-3943`, `:4499`; `templates/sdd-round.md:39`; `skills/code-review/orchestration.md:535-539` | round 2's 🟢 — verified |
| round-2 | `agents/warden.md:320-325`; `tests/test_the_broad_gate_cell_keeps_every_run.py` | round 2's 🟢 — verified |
| round-2 | `skills/code-review/scripts/round_record.py:1128-1139`; `skills/code-review/scripts/chain_check.py:1574-1580` | round 2's 🟢 — verified |
| round-2 | `agents/warden.md:466-469`; `docs/review-chain-spec.md:979-985`; `skills/code-review/SKILL.md:329-334`; `tests/test_the_report_standard_is_one_in_three_places.py:1-6` | round 2's 🟢 — verified |
| round-2 | `skills/code-review/scripts/round_record.py:2136-2153`; `floor_and_fixes` | round 2's 🟢 — verified |
| round-2 | `skills/code-review/scripts/round_record.py:376-381`; `tests/test_the_seal_is_taken_once_by_the_sealer.py:2555-2577` | round 2's 🟢 — verified |
| round-2 | `git diff --stat 83988abd..21b8d61e`, fifteen files; `seal/ledger.md`; `seal/ledger/1790174138-the-report-the-record-and-the-cells-disagree-on-one-format.md:20-21` | round 2's 🟢 — verified |
| round-2 | `skills/code-review/scripts/round_record.py:347-385`; `tests/test_the_broad_gate_cell_keeps_every_run.py` | round 2's 🟢 — verified |
| round-2 | `rounds/round-1.md` | round 2's 🟢 — confirmed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| ⬜ 1 — the `broad-gate.md` comment's *the earlier one stays behind it* and the *count of runs* sentence in the docstring and A9 predate `same_run`; no test reads the written comment | a new issue, filed from this record: the comment names the replace and its key, the docstring and A9 say distinct comparisons, and the seal module pins the written sentence (round 2's second regression row), seen red first | the repository owner |
