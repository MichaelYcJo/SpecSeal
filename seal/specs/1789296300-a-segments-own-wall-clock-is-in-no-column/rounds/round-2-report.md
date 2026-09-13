# 1789296300-a-segments-own-wall-clock-is-in-no-column — review round 2 (report)

Target SHA `79563aebf3f3b5c4abac7151193a6eab5b2de7e1`, ten commits,
`d146bd7..79563ae`. The verifying round: round 1's fixes were written by a fix
pass and read by nobody, and this round is the reading. No agent was spawned
(contract §6). The broad gate was not run and is not this round's (§2).

**Round 1's fixes hold.** All eight fixes reproduce, the ninth finding's
deferral is correctly routed, and the three claims this round was told to
open rather than accept each re-measure to the stated numbers. Nothing needs
a fix. Three corrections are recorded below, all of them the run's own
paperwork.

## What was checked by running it, and what it settled

**The `position == 0` case does separate, and it is the only case that does.**
Mutating `segment_slices`' `if position == 0` back to `if index == 0` in a
scratch clone leaves the module at 1 failed, 104 passed, and the one failure
is `test_a_file_whose_first_window_is_empty_still_carries_its_tokens` — the
case the fix pass wrote after finding the hole. The two cases the reviewer
drafted stay green under that mutation, exactly as the fix pass reported. The
hole was real and the case closes it.

**The `spawn_cycles` exemption is right, and it is stronger than its own
grounds claim.** Carrying `segment_slices`' drop-the-call-less-window filter
into `spawn_cycles` turns five cases red, not one:
`test_a_row_with_no_call_keeps_its_place_in_the_partition` as the exemption
says, plus four more that rest on the same partition
(`test_a_batch_of_two_spawns_is_bounded_by_when_each_report_arrived`,
`test_an_unparseable_turn_stamp_does_not_end_the_slicing`,
`test_two_prompts_that_differ_after_a_pipe_are_not_a_check_re_run`,
`test_a_spawn_that_names_no_subagent_type_still_gets_a_row`). The two loops
are a true resemblance and a false equivalence, and the row says so.

**The §6 count reproduces exactly.** Re-measured independently over every run
with a `subagents/` directory on this machine: 43 runs, 13 carry the line, 12
of those name an agent this plugin spawns, and the `Agent` calls inside
segments are 40 by `specseal:warden`, 4 by `specseal:smith` and 1 by
`claude-preset:code-reviewer`. Exit 0 on all 43. The aggregate in
`changelog.md`, `overview.md` and the ledger fragment's evidence cell is the
number the tree produces.

**The median reproduces, and the figure now has an address.** Measured with
the mode over every segment row of the same 43 runs: named rows n=384, median
720.1 s, mean 1,018.5; all rows n=436, median 664.7 s, mean 1,019.8. The fix
pass read 716/381 and 664/433 — three rows more exist today, which is the
growth its own docstring warns about, and the ~700 it published is what the
population reads. Every one of the three places now carries either the
measurement or a pointer to `measure_segments`, which carries it. The figure
no longer travels alone.

**The new breach line renders correctly on the run it was written for.** Run
against the thirteenth run — the one whose segment spawned through
`claude-preset:code-reviewer` — the sentence prints at 74 to 78 columns
directly under the §6 paragraph and directly above the reconciliation. §14 is
satisfied: the changed text is pinned by
`test_the_breach_line_says_which_agents_the_section_binds`, and its absence
half by `test_a_clean_run_prints_no_such_line`.

## What was checked by reading it

**Finding 9's rule is sound, and the tree bears it out.** The rule the fix
pass substituted for the block's file-kind contrast is that what decides the
treatment is what the divergence IS. Checked both halves. The absent name is
absent everywhere a reader could follow it: `segment_rows` — NAME NOT IN TREE
— survives only inside the divergence row that quotes it and two phase
records that mark it, while `plan.md:100` now names `measure_segments()`. The
nested-transcript picture stands in both files, and the four line numbers the
row cites for each (`spec.md` :11, :111, :132, :155 and `plan.md` :20, :41,
:100, :103) each carry it. The block's own rule would have broken on
`plan.md`; this one does not break anywhere.

**Finding 6's routing is verified against the code.**
`.github/scripts/fold_ledger.py` refuses the release fold while any
`seal/specs/*/evidence-todo.md` has an open row, exit 1, writing nothing.
Evaluated `open_rows` against all six such files in the tree today: zero open
rows. So a row added there for the re-anchoring chore would be the only open
row in the tree and would be the thing that stops 0.11.3. The routing to
`seal/follow-up.md` is correct, and the row there names an answerer.

**No other live claim kept the old median.** Three places still say *a median
of about 1,000 seconds* — `session_cost.py:246` in `DELEGATING`'s comment,
`session_cost.py:693` in `spawn_cycles`' docstring, and
`tests/test_session_cost.py:2066` in a case docstring. All three are #145's,
dated 2026-09-09, untouched by this branch. The one live ledger claim,
`seal/ledger.md:1827`'s *Subagent spans median about 1,000s*, still carries
its `Checked` date of 2026-09-09 — it was not among the seven re-stamped
rows, so nothing was re-certified as read while false. The survivor the fix
pass found and corrected, the ledger fragment's seventh row, is the only live
claim that had kept the number.

**The seven `Checked` cells each carry a dated re-read note.** All seven moved
to 2026-09-13 and nothing else in any of the seven rows changed; every one
already held a `**Re-read 2026-09-13 for #350**` note in its Notes cell, so
the column was contradicting a reading that had happened rather than
recording one that had not.

**The five new units judged as code, not as fixes.** All five pin units that
came from a build phase — `segment_slices`, `measure_segments`,
`report_breaches` — so all five are depth 1 and none is the depth-2 shape the
fix-pass rule refuses. Read each for what it asserts rather than for whether
it passes; no defect found. One thing was checked and is not a finding: a file
whose window 0 is now dropped reports `1/1` and so falls out of `slices > 1`,
which is what feeds the *segments the coordinator restarted* sentence. That
sentence explains the `N/of` markers and a collapsed file prints none, so it
stays honest. Nothing else is lost with the dropped window — `analyse` returns
null for a call-less window either way, and the token figure is the whole
file's.

## The corrections

**⬜ 1 — the proof block is stale again, one lower.** `overview.md:10` records
`bin/test tests/test_session_cost.py -q` at 104; the module reads **105** at
the reviewed HEAD. This is finding 8 recurring inside its own fix: `f63db1c`
wrote 104, and `4af3441` — two commits later in the same pass — added the
fifth case. The same shape the finding named, one commit apart.

**⬜ 2 — the follow-up row's enumeration of the median is one place short.**
`seal/follow-up.md`'s new second row tells the owner where #145's figure
reached: *the shipped script twice*, the `seal/ledger.md` row, and #145's own
records. `tests/test_session_cost.py:2066` states the same 1,000-second
median in a case docstring and is in none of those three categories. That row
is the only list the owner will have.

**⬜ 3 — the survivor record cannot be re-derived by running the documented
command.** `survivors.md`'s header names
`survivor-check --range <a>..<b> --exempt <this file>`, and its own text says
an exemption stops holding as soon as the quoted text changes. Measured: at
`216df9d` the check reports `session_cost.py:713` at score 2.00 **with no
`--exempt` at all**; at `d0a455e`, whose only change is the one survivors.md
line that made the quote contiguous, it reports *no removed wording is still
standing* — again with no `--exempt`. The quote is wording the range itself
wrote, and `survivor_check.py#corrected` subtracts what the range wrote from
what it searches for. `#records_a_past_round` excludes files under
`rounds/`, and `survivors.md` does not sit there. So the exemption silences
the report whether or not the reviewer passes it, and a reader cannot run the
command to see what was exempted. The effect is confined to ranges containing
the quoting commit — a later branch's range does not carry it — which is why
this is a correction and not a fix to commission. It is also not this
branch's code: `survivor_check.py` is untouched here, and thirteen other work
items already carry a `survivors.md`.

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

Every probe ran in a `git clone --no-local` of the branch inside the session
scratchpad, or read-only over the run transcripts. The clone, its virtual
environment and both probe scripts were deleted; the worktree under review was
never written to except for this report.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Finding 6 — re-anchoring the seven `seal/ledger.md` rows one altitude down | `seal/follow-up.md`, written at `f63db1c` | the repository owner. Verified this round: the `evidence-todo.md` route would make the release fold refuse, and every one of the six such files in the tree is closed today |
| The ledger half of #145's median — `seal/ledger.md:1827` still reads *Subagent spans median about 1,000s* | `seal/follow-up.md`, written at `216df9d` | the repository owner. Its `Checked` cell is still 2026-09-09, so nothing was re-certified while false |
| The §6 line becoming an exit code rather than a line | `overview.md` §Not done | a later work item, choosing against the 13 readings that now exist |
| `survivor-check` has no cheat-sheet row in either README | `overview.md` §Not done | the repository owner |

## Paste-ready fixes

⬜ 1 — `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/overview.md:10`, the module count only:

```
`bin/test tests/test_session_cost.py -q` (105 after round 1's fix pass; 100 at the handoff, which the proof block recorded as 98)
```

Needs a fix: no

Loses a record or crashes: no

## Proof block

Opened: `seal/specs/1789296300-a-segments-own-wall-clock-is-in-no-column/`
— `rounds/round-1.md`, `overview.md`, `changelog.md`, `spec.md`, `plan.md`,
`survivors.md`; `seal/ledger.md`,
`seal/ledger/1789296300-a-segments-own-wall-clock-is-in-no-column.md`,
`seal/follow-up.md`; `skills/verify/scripts/session_cost.py`,
`tests/test_session_cost.py`,
`skills/code-review/scripts/survivor_check.py`,
`.github/scripts/fold_ledger.py`, `bin/test`, `tests/test_docs_line_wrap.py`,
`CLAUDE.md`.

verified: **executed** — the eleven probe rows above, every one in a scratch
clone at `79563ae` or read-only over this machine's run transcripts. **read** —
finding 9's rule against `spec.md`, `plan.md` and the phase records; finding
7's measured comment; the five new units; the seven `Checked` cells and their
Notes. **unverified** — the full suite, the repository-wide lint and the
typecheck, which contract §2 makes one act with one owner; answerer: the
sealer, spawned next.
