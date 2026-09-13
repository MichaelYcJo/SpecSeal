# 1789296300-a-segments-own-wall-clock-is-in-no-column — review round 2

| Field | Value |
|---|---|
| Target SHA | 79563aebf3f3b5c4abac7151193a6eab5b2de7e1 |
| Ran by | warden on claude-opus-5 |
| PR | 380 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | no |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

The verifying round: round 1's fixes were written by a fix pass and read by nobody, and this round fills round 1's `Fixes checked by` cell. Scope was the diff of the fixes, `d146bd7..79563ae`, ten commits, judged against round 1's findings. Round 1's verdicts are inherited.

The reviewer was told the honest outcome is often "nothing" and that reaching for something to say is the failure mode here. It was pointed at the one place a fix was added to cover a hole nobody had seen — finding 4's `position == 0` change, which the reviewer's own drafted cases did not separate — and at the exemption, the §6 count, the median's new address, and the seven moved `Checked` cells.

**The round opened nothing needing a fix**, and it re-derived rather than accepted:

- **The `position == 0` case genuinely separates.** Reverting the line to `index == 0` fails exactly one case, and it is the one the fix pass wrote. Round 1's two drafted cases stayed green, exactly as the fix pass reported.
- **The `spawn_cycles` exemption is right, and stronger than its stated grounds** — carrying the `segment_slices` fix across turns five cases red, not one.
- **The §6 count reproduces**: 13 of 43 runs print the line, 12 name an agent this plugin spawns, and the call breakdown matches at 40 / 4 / 1.
- **The median reproduces** at 720.1 s over 384 named rows and 664.7 s over 436, mean 1,018 — three rows apart from the fix pass's 716/664, which is the population growth the document itself states. All three sites carry their measurement's address now.
- **No other live claim kept the old number.** The three remaining `1,000` sites are #145's and untouched by this branch.
- Finding 6's home was checked against the code: all six `evidence-todo.md` in the tree are closed, so opening one row there would be the single row blocking 0.11.3's release fold. `seal/follow-up.md` is right.

**Three ⬜ recorded and deliberately not fixed.** The proof block says 104 for `tests/test_session_cost.py` where the module is 105 — finding 8 recurring inside its own fix, because `f63db1c` wrote 104 and `4af3441` added a case two commits later; the `seal/follow-up.md` median row omits `tests/test_session_cost.py:2066` from the list of reach points that is the owner's only list; and `survivor-check` now reports this range clean with or without `--exempt`, because the quoted text is a sentence the range itself wrote and so drops out of the corpus, which means the exemption record cannot be re-verified by the command.

The orchestrator left all three alone on the arithmetic this release already paid for once: on the sibling branch for #354, fixing a ⬜ that the verifying round had deliberately kept off its fix list is what made that round close on a fix and ended the run at round 3. None of the three changes what any check reads, and the third is a property of `survivor_check`'s corpus rather than of this branch.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | 🟡 round 1's finding 1 — `unnamed` summed over slices rather than transcripts | `skills/verify/scripts/session_cost.py#measure_segments` | **answered** | Holds. Mutated the line back to `sum(1 for row in rows if not row["named"])` in a scratch clone: 1 failed, 104 passed, and the one failure is `test_an_unnamed_file_that_was_resumed_is_counted_once`. The case separates the two readings and nothing else in the module does; Executed |
| 2 | 🟡 round 1's finding 2 — the published median is the mean, carried into three new places | `skills/verify/scripts/session_cost.py` :39–40 and `#measure_segments`; `…/changelog.md` | **answered** | Holds, and the figure has an address. Re-measured with the mode over every segment row of the 43 runs: named n=384 median 720.1 s mean 1,018.5; all rows n=436 median 664.7 s mean 1,019.8. The fix pass's 716/381 and 664/433 differ by the three rows the population has grown, which its own docstring predicts. The corrected block that round 1 drafted without an address now carries one in `changelog.md`, and the module docstring points at `measure_segments`, which carries the measurement; Executed |
| 3 | 🟡 round 1's finding 3 — the §6 line cited the contract at agents it does not bind | `skills/verify/scripts/session_cost.py#report_breaches` | **answered** | Holds. Re-measured independently over the 43 runs: 13 carry the line, 12 name an agent this plugin spawns, 40 `Agent` calls by `specseal:warden`, 4 by `specseal:smith`, 1 by `claude-preset:code-reviewer`; exit 0 on all 43. Rendered the report on the thirteenth run itself — the sentence prints at 74–78 columns in the right place. Pinned by `test_the_breach_line_says_which_agents_the_section_binds` and its absence twin; Executed |
| 4 | 🟡 round 1's finding 4 — an empty window printed as a slice the agent never worked | `skills/verify/scripts/session_cost.py#segment_slices` | **answered** | Holds, and the arm round 1 did not catch is closed. Mutating `position == 0` back to `index == 0` fails exactly one case, `test_a_file_whose_first_window_is_empty_still_carries_its_tokens`, which is the case `4af3441` added for that hole; the two drafted cases stay green under it, as the fix pass reported. Judged a fix rather than an answered row on the grounds that zero occurrences still harms a count a reader trusts without opening the file — the call it made is sound, and the shape is one this repository's own workflow produces. No reading is lost with the dropped window: `analyse` returns null for a call-less window either way; Executed and Read |
| 5 | ⬜ round 1's finding 5 — seven `seal/ledger.md` `Checked` cells left stale | `seal/ledger.md` | **answered** | Holds. All seven moved to 2026-09-13, each already carrying a `**Re-read 2026-09-13 for #350**` note in its Notes cell, and nothing but the date changed in any of the seven rows. `evidence_check.py .` reads 1158 ok · 0 drifted · 0 broken; Executed |
| 6 | ⬜ round 1's finding 6 — the seven rows anchored a heading path too high | `seal/ledger.md` | **answered** | Correctly routed. `fold_ledger.py` refuses the release fold while any `seal/specs/*/evidence-todo.md` has an open row; evaluated `open_rows` over all six such files in the tree and every one is closed, so a row added there would be the only open row and would be what stops 0.11.3. `seal/follow-up.md` carries both sides and names the repository owner; Executed and Read |
| 7 | ⬜ round 1's finding 7 — every segment transcript read five times on a `--json` run | `skills/verify/scripts/session_cost.py#segment_slices`, `#main` | **answered** | Holds. The comment states its own measurement (257ms/698ms/926ms against `analyse`'s 28–36ms) and says the gating is what it shares with `spawns` while the cost is not, which is the reading round 1 asked for. The gating is unchanged and the question it leaves open is named as `--json`'s rather than this line's; Read |
| 8 | ⬜ round 1's finding 8 — the proof block recorded a stale module count | `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/overview.md` | **open** | Recurred inside its own fix. `overview.md:10` records 104; the module reads **105** at the reviewed HEAD. `f63db1c` wrote 104 and `4af3441` added the fifth case two commits later. Correction ⬜ 1 above; Executed |
| 9 | ⬜ round 1's finding 9 — the divergence table did not say which convention applied | `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/overview.md` | **answered** | The substituted rule is sound and the tree bears it out. `segment_rows` — NAME NOT IN TREE — survives only in the row quoting it and two marked phase records, and `plan.md:100` names `measure_segments()`; the nested-transcript picture stands in both files at every one of the eight lines the row cites. The block's own file-kind rule would have broken on `plan.md`; this one breaks nowhere; Read |
| 10 | ⬜ the follow-up row enumerating where #145's median reached omits `tests/test_session_cost.py:2066` | `seal/follow-up.md` | **open** | The row names the shipped script twice, the `seal/ledger.md` row and #145's own records. The case docstring at :2066 states the same 1,000-second median and is none of those. That row is the only list the owner gets. Correction ⬜ 2; Read |
| 11 | ⬜ `survivor-check` over the fix range reports clean with or without `--exempt`, so the exemption record cannot be re-derived | `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/survivors.md`, `skills/code-review/scripts/survivor_check.py#corrected` | **open** | At `216df9d` the check reports `session_cost.py:713` at 2.00 with no `--exempt`; at `d0a455e`, whose only change is the one survivors.md line, it reports nothing standing, again with no `--exempt`. The quote is wording the range wrote, and the range's written n-grams are subtracted from what is searched for; `#records_a_past_round` excludes `rounds/` and not `survivors.md`. Confined to ranges holding the quoting commit, and `survivor_check.py` is untouched by this branch. Correction ⬜ 3; Executed |
| 12 | ⬜ a file whose window 0 is dropped now prints `1/1` and falls out of the *segments the coordinator restarted* count | `skills/verify/scripts/session_cost.py#segment_slices`, `#report_segments` | **withdrawn** | Opened as a possible silent second reading and it is not one. That sentence explains the `N/of` markers, and a collapsed file prints none, so the line stays true. Nothing else moves: `widest_idle_gap` was never computed across a window boundary, and the dropped window's row carried a null `numbers` before the fix as well; Read |

## Paste-ready fixes

```
`bin/test tests/test_session_cost.py -q` (105 after round 1's fix pass; 100 at the handoff, which the proof block recorded as 98)
```

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_session_cost.py -q` at the target SHA, in a `git clone --no-local` of the branch | **105 passed**, exit 0 |
| Probe — `position == 0` mutated back to `index == 0` in the clone, restored from a byte copy | **1 failed, 104 passed**, exit 1. The single failure is `test_a_file_whose_first_window_is_empty_still_carries_its_tokens`; the two drafted cases stay green. The case separates the two readings and it is the only one that does |
| Probe — `segment_slices`' call-less-window filter carried into `spawn_cycles`, restored from a byte copy | **5 failed, 100 passed**, exit 1, including `test_a_row_with_no_call_keeps_its_place_in_the_partition`. The exemption holds and is stronger than its grounds claim |
| Probe — `unnamed` mutated back to a sum over rows, restored from a byte copy | **1 failed, 104 passed**, exit 1, `test_an_unnamed_file_that_was_resumed_is_counted_once`. The module restores to 105 passed, exit 0, and the file matches the kept bytes |
| Probe — `--segments` and `--segments --json` over every run with a `subagents/` directory on this machine | 43 runs, exit 0 on every one. **13 carry a §6 line; 12 of those name an agent this plugin spawns.** `Agent` calls inside segments: 40 `specseal:warden`, 4 `specseal:smith`, 1 `claude-preset:code-reviewer` |
| Probe — the median, re-measured with the mode over every segment row of the same 43 runs | named rows n=384 **median 720.1 s** mean 1,018.5; all rows n=436 median 664.7 s mean 1,019.8 |
| Probe — the new breach line rendered against the thirteenth run | Prints at 74–78 columns between the §6 paragraph and the reconciliation, naming `claude-preset:code-reviewer` |
| `survivor_check.py --range d146bd7..79563ae --exempt …/survivors.md` | 914 files, 27 removed sentences, **nothing standing**, exit 0. The same command without `--exempt` also reports nothing standing — see finding 11 |
| `survivor_check.py --range d146bd7..216df9d`, no `--exempt` | **1 place** still carrying removed wording: `session_cost.py:713` at score 2.00. `d0a455e` changes one line of `survivors.md` and nothing else, and after it the same range reports clean |
| `evidence_check.py .` in the clone | **1158 ok · 0 drifted · 0 broken · 0 external · 0 old-format**, exit 0; records arm 84 names read · 0 refused |
| Probe — `fold_ledger.py#open_rows` over all six `seal/specs/*/evidence-todo.md` in the tree | **0 open rows** across all six, so an added open row would be the only one and would stop the release fold |
| The broad gate — the full suite, the repository-wide lint, the typecheck | **not yet.** Contract §2 makes it one act with one owner and this round is not it. Answerer: the sealer, spawned after the rounds settle |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/scripts/session_cost.py#measure_segments` | round 1's 1 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py` :39–40 and `#measure_segments`; `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/changelog.md:10` | round 1's 2 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py#report_breaches` | round 1's 3 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py#segment_slices` | round 1's 4 — fixed |
| round-1 | `seal/ledger.md` | round 1's 5 — fixed |
| round-1 | `skills/verify/scripts/session_cost.py#segment_slices`, `#main` | round 1's 7 — fixed |
| round-1 | `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/overview.md` | round 1's 8 — fixed |
| round-1 | `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/overview.md`, `spec.md` :132 | round 1's 9 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Finding 6 — re-anchoring the seven `seal/ledger.md` rows one altitude down | `seal/follow-up.md`, written at `f63db1c` | the repository owner. Verified this round: the `evidence-todo.md` route would make the release fold refuse, and every one of the six such files in the tree is closed today |
| The ledger half of #145's median — `seal/ledger.md:1827` still reads *Subagent spans median about 1,000s* | `seal/follow-up.md`, written at `216df9d` | the repository owner. Its `Checked` cell is still 2026-09-09, so nothing was re-certified while false |
| The §6 line becoming an exit code rather than a line | `overview.md` §Not done | a later work item, choosing against the 13 readings that now exist |
| `survivor-check` has no cheat-sheet row in either README | `overview.md` §Not done | the repository owner |
