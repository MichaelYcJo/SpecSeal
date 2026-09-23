# Round 1 — report

Work item `1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row`,
PR #537 (draft), branch
`design/138-241-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row`
at target SHA `7604e522ade45a51dbbb89589b85905e56b7040c`, base `release/v0.15.0`
at `cbb58091fddb9a02e3136156d7963dcd66798d1b`. Reviewed in a `git clone
--no-local` of the repository at the target SHA; the clone and the one probe
script are deleted, and nothing was written outside this file. Every claim
below is labelled **executed**, **read** or **unverified**. Coordinates are
this round's own — no earlier round exists for this work item.

## Stage 1 — the build follows the two decisions of `spec.md`

**#138, decided as option 1, is built at both ends and the count walk no
longer stops at a bare `yes` (executed and read).** `chain_check.py#says_reopened`
is the one reader: it answers `True` for `yes — <what>`, `False` for `no`
with or without a reason, `None` for a bare `yes`, an empty cell and a word
outside the vocabulary (read, `skills/code-review/scripts/chain_check.py:2392-2419`).
Its three callers are `run_reopened` (:3147), `stopping_floor`'s own-row read
(:3262) and `round_record.py#floor_and_fixes` (:1931); a grep for `== FLOOR_YES`
over both scripts finds only the floor row's own read (:3367) and the wording
read that tells a bare `yes` from *neither answer* (:3271), so no local
comparison of the `Needs a fix` cell is left (executed grep). The refusal on
the record that carries it uses the floor row's words, *says `yes` and does
not say what*, and sits under `needs_excused` — `NEEDS_FROM` grandfathers the
row whole — with no cutoff of its own (read, :3256-3309). The seven new cases
in the floor-and-depth module and the two in the generator suite fail under
the phase files' mutations: I re-ran M1, M2, M3, M4, M5, M6, M7, M8, M10 and
M12 from restored bytes in the clone and every one was killed by the cases the
phase tables name, with M3 killed by the walk case alone, which is what says
that case pins the walk and not the record's own row (executed; the probes
table has the failing case per mutation).

**The writer refuses both labels (executed).** `round_record.py#terminal_value`
refuses `yes` with no reason after the join, in `written_late_cell`'s shape
(read, `skills/code-review/scripts/round_record.py:1359-1374`); M5 removed the
branch and both parametrised cases of
`test_a_bare_yes_on_either_terminal_line_is_refused_at_the_writer` went red.
The printed bound reads the cell through `chain.says_reopened(...) is True`
(read, :1929-1932); M6 restored the inline comparison and
`test_a_bare_yes_on_a_later_record_is_no_reopening_here_either` alone went
red. The frame's coordinate was one function off — the inline read lived in
`floor_and_fixes`, not `bound_line` — and `overview.md` records that; the diff
confirms `bound_line` is byte-identical (read).

**#241: no third answer, and the seven sentences are rewritten and pinned
(executed and read).** The diff touches no `hooks/routing.py`, no
`REVIEW_ANSWERS`, no `CLAUDE.md` block (read, `git diff --stat`). The
declaration table's `straight to the PR` row now names the sealer's
`broad-gate.md`, and its three qualifications — a draft is excused the file,
an earlier work item is excused and prints, the declaration is printed either
way — match `direct_seal` line for line: `strict` false returns nothing,
`began < DIRECT_GATE_FROM` returns a notice, and `main` prints the declared
line before calling it (read, `chain_check.py:3910-3935`, `:4218-4230`;
`DIRECT_GATE_FROM = 1789518345` at :780). The gate prompt's option 1,
rendered, carries `broad-gate.md`, `USER'S answer` and both spellings and no
`requires nothing`; M10 restored the old sentence and only
`test_the_first_option_says_what_the_direct_answer_owes` went red, which is
the one carrier a whole-file substring cannot read (executed). The standing
phrase *the sealer's `broad-gate.md`* occurs once in the specification, once
in the checker's docstring, once in the template, once in the routing test
and twice in `skills/implement/orchestration.md` (executed count), which is
what phase 3 recorded, so each pin is live for one sentence.

**The ledger (executed and read).** `bin/evidence-check --strict` exits 0 at
the target SHA: 1565 ok, 0 drifted, 0 broken, 128 names read from this work
item's records, 0 refused. `git diff` over `seal/ledger.md` shows seventeen
rows re-stamped, each carrying a dated *Re-read 2026-09-23* (or *-24*) note
naming this work item and what moved, and one row removed — F8. The
*Review arm* heading row carries two notes, one per issue, which is why the
prompt counts eighteen re-reads over seventeen rows. B1–B3 in the fragment
cite units the tree carries, and B1's claim that three readers go through
`says_reopened` is the grep above. Q1 holds: no `Needs a fix` cell under
`seal/specs/*/rounds/` or `tests/` reads `yes` alone (executed grep, exit 1).

**The five points work item A inherits (read against the landed code)** hold:
three readable values per terminal line with the bare `yes` refused at both
ends; one reader with `bound_line` reading through it; `Review` unchanged at
two answers and `Ran by` untouched; `direct_seal` reading through
`broad_gate`; and the seven sentences pinned as gone/stands pairs.

## Stage 2 — what the reading and the probes found

### 🟡 1 — `seal/ledger.md`'s F4 note points at F8, which this branch removed from that file, and the hygiene workflow refuses the branch for it

`seal/ledger.md:785`, in the comment under
`### 1788472135-the-run-outlives-its-last-finding`, reads *its claim is
carried forward by F8 — which says more than F4 did, because the reason for
the rename is part of the claim now*, and `seal/ledger.md:777` lists F8 among
the rows of that section. Commit `e852f49c` removed F8 from this file and
re-founded the claim as the fragment's B2 (read). So a reader following F4's
note finds nothing, and the sentence is now false in the file that carries it.

It also fails at the pull request. `.github/workflows/hygiene.yml:250-255`
runs `survivor_check.py --range origin/<base>...HEAD` with every
`seal/specs/*/survivors.md` as an exemption. I ran that exact form at the
target SHA and it exits 1 on `seal/ledger.md:784`, sharing *the rename is
part* and *of the claim* with the removed F8 row (score 1.77) — executed. The
smith's range `659b4229..HEAD` starts after the frame commit and does not
surface it (executed: exit 0 with the exemption file, one survivor, exempt),
which is why the hand-back could report six survivors all excused.

The fix is a correction, not an exemption: the sentence is false, so it is
rewritten with a dated `Corrected` marker in the shape `correction_check.py`
reads, pointing at the fragment. The comment sits in no anchored region — the
only `seal/ledger.md` anchors are the `### 1788331011` and `### 1788398967`
headings — so no hash moves. I committed the paste-ready fix below in the
clone from Python and the CI form exits 0 (*every survivor is excused by a
row above (1)*), `correction-check --range cbb58091...HEAD` exits 0,
`evidence-check --strict` stays at 1565 ok, and `test_docs_line_wrap.py`,
`test_a_merge_cannot_silently_drop_a_correction.py` and
`test_no_real_identifiers.py` pass with the edit in the tree (86 passed) —
executed, then reset. One fact for the fix pass: `survivor-check` reads the
files at HEAD, not the working tree, so the fix is only checkable after it is
committed.

### ⬜ 2 — `overview.md` counts ten mutations where the phase files table thirteen

`seal/specs/1790173106-…/overview.md:12` says *the ten mutations in
`phases/`*; `phases/phase-1.md`, `phase-2.md` and `phase-3.md` table M1–M13
(read). Paperwork under `seal/specs/`, reported as a correction and kept out
of `Needs a fix`.

### ⬜ 3 — `survivors.md` excuses six reports and the range now produces one

`seal/specs/1790173106-…/survivors.md:3` says the check reported six places at
`4cd5a561`. At `7604e522` the same range, `659b4229..HEAD`, reports one —
`chain_check.py:2960`, `written_late_reason`'s body — and the other five rows
excuse nothing (executed). Harmless today; the file's own rule is that a quote
is the anchor, and five anchors now anchor nothing. Paperwork, a correction.

### ⬜ 4 — the writer's refusal for the floor line explains the other row

`skills/code-review/scripts/round_record.py:1365-1374`: the message raised for
`Loses a record or crashes: yes` says *`Needs a fix` is the cell the floor's
count of later records restarts at, so a bare `yes` there bought a round* —
true, but about the other label. The behaviour and the fact are right; only
the sentence a person reads is one row off. `Needs a fix` never counts it.

### Regression tests to plant

None beyond what the branch plants. 🟡 1's check is the hygiene workflow's
own step, and the paste-ready fix is verified against it above.

### Facts for the evidence ledger

None new. B1–B3 in the fragment already carry what this round verified, and
🟡 1 is a correction to prose, which takes a `Corrected <date>` marker rather
than a row.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `seal/ledger.md`'s F4 note says F8 carries its claim forward; this branch removed F8 from that file, so the note is false and the hygiene workflow's `survivor_check.py --range origin/<base>...HEAD` exits 1 on it at the pull request | `seal/ledger.md:777`, `seal/ledger.md:785` | open | executed: CI form exit 1 at `7604e522` on `seal/ledger.md:784`; exit 0 with the paste-ready correction committed in the clone; the smith's range `659b4229..HEAD` does not surface it |
| ⬜ | `overview.md` says ten mutations; the phase files table thirteen (M1–M13) | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/overview.md:12` | not a defect | read; paperwork correction under `seal/specs/`, kept out of `Needs a fix` |
| ⬜ | `survivors.md` excuses six reports; at the target SHA the same range produces one (`chain_check.py:2960`), so five rows anchor nothing | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/survivors.md:3` | not a defect | executed: `survivor-check --range 659b4229..HEAD` reports one place |
| ⬜ | `terminal_value`'s refusal for the floor line explains `Needs a fix`'s count, one row off | `skills/code-review/scripts/round_record.py:1365` | not a defect | read; the behaviour and the fact are right, the sentence is one row off |
| 🟢 | one reader for the reopening question, three callers, no local `== FLOOR_YES` left on the `Needs a fix` cell | `skills/code-review/scripts/chain_check.py:2392`, `:3147`, `:3262`; `skills/code-review/scripts/round_record.py:1931` | not a defect | read and executed grep; M1 and M3 killed |
| 🟢 | a bare `yes` refused at the reader in the floor row's words under `NEEDS_FROM`'s grandfathering, and it stops the count of nothing | `skills/code-review/scripts/chain_check.py:3256-3309` | not a defect | executed: A1, A2, A3 green; M1, M2, M3 killed |
| 🟢 | `round_record.py new` refuses a bare `yes` on either terminal line, and the printed bound reads through the gate's reader | `skills/code-review/scripts/round_record.py:1359`, `:1931` | not a defect | executed: M5 killed both parametrised cases, M6 killed the bound case alone |
| 🟢 | the three #138 carriers and the seven #241 places say what stands and no longer say what is gone; the gate's option pinned through the rendered prompt | `tests/test_the_direct_answer_owes_the_sealers_record.py`, `tests/test_routing_is_recorded.py:255`, `tests/test_the_record_is_held_to_the_floor_and_the_depth.py:1297` | not a defect | executed: M4, M7, M8, M10, M12 killed; the standing phrase occurs once per file, twice in the orchestration skill |
| 🟢 | the declaration table row's three excusals match `direct_seal`; no third `Review` answer, no change to `hooks/routing.py` | `docs/review-chain-spec.md:743`, `skills/code-review/scripts/chain_check.py:3910-3935` | not a defect | read against the code and the diff stat |
| 🟢 | F8 removed and re-founded as B2; seventeen rows re-read with dated notes; `evidence-check --strict` green; Q1 is zero | `seal/ledger.md`, `seal/ledger/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row.md` | not a defect | executed: 1565 ok · 0 drifted · 0 broken; grep for a bare `yes` cell finds none |
| 🟢 | the five points work item A inherits remain true of the landed code | `seal/specs/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row/plan.md:89-109` | not a defect | read |
| ❓ | the broad gate — full suite, repository-wide lint, typecheck | — | out of verified scope | the sealer's, after the rounds settle; the prompt labelled it unverified and ordered no run |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over twelve modules in the clone at `7604e522`: the floor-and-depth module, `test_the_record_is_generated.py`, `test_a_record_precedes_the_fixes_it_commissions.py`, `test_the_direct_answer_owes_the_sealers_record.py`, `test_routing_is_recorded.py`, `test_waiver_decided_at_start.py`, `test_docs_line_wrap.py`, `test_one_word_one_meaning.py`, `test_chain_check_at_the_pull_request.py`, `test_the_run_stops_at_the_last_finding.py`, `test_a_record_says_why_it_was_written_late.py`, `test_no_real_identifiers.py` | `540 passed in 225.90s`. The status of that call was read through `\| tail`, so the summary line is the evidence and the status is not; the mutation probe's baselines over the same modules returned 0 directly |
| mutation probe, one file `test_tmp_mutations.py` (NAME NOT IN TREE: deleted after the run), each mutation applied by an exact single-match substitution, the module run through the clone's venv with the exit code read directly, the file restored from git and `git status` clean after each | M1 — 4 failed (`…fails_after_the_cutoff`, `…prints_before_the_cutoff`, `…does_not_stop_the_count`, `test_says_reopened_is_the_one_reader_of_the_reopening_question`); M2 — 3 failed (the three walk and row cases); M3 — 1 failed (`…does_not_stop_the_count` alone); M4 — 1 failed (`test_each_carrier_says_a_bare_yes_is_refused[parts1]`); M5 — 2 failed (both labels); M6 — 1 failed (`…is_no_reopening_here_either`); M7 — 1 failed (`…requires[parts2]`); M8 — 1 failed (`…requires[parts0]`); M10 — 1 failed (`test_the_first_option_says_what_the_direct_answer_owes`); M12 — 1 failed (`…why_two_answers_and_not_three`). All killed |
| `bin/evidence-check --strict` at `7604e522` | exit 0; `total: 1565 ok · 0 drifted · 0 broken · 0 external · 0 old-format`; records: 1 work item read, 128 names read, 0 refused |
| `bin/survivor-check --range 659b4229..HEAD --exempt seal/specs/1790173106-…/survivors.md` (the smith's range) | exit 0; one survivor, `chain_check.py:2960`, exempt; *every survivor is excused by a row above (1)* |
| `python3 skills/code-review/scripts/survivor_check.py --range cbb58091...HEAD` with every `seal/specs/*/survivors.md` (the hygiene workflow's form) | exit 1; `seal/ledger.md:784` shares *the rename is part* / *of the claim* with removed F8, score 1.77 — 🟡 1 |
| the same form at a probe commit carrying the paste-ready fix for 🟡 1, committed from Python in the clone and reset afterwards | exit 0; `correction-check --range cbb58091...HEAD` exit 0; `evidence-check --strict` 1565 ok; `test_docs_line_wrap.py`, `test_a_merge_cannot_silently_drop_a_correction.py`, `test_no_real_identifiers.py` — 86 passed with the edit in the tree |
| Q1: `grep -rn -E '^\| *Needs a fix *\| *\**yes\**\.? *\|' seal/specs/*/rounds/*.md tests/` | no match (exit 1); no live cell reads `yes` alone |
| `uvx ruff check` and `uvx ruff format --check` over the seven changed `.py` files | `All checks passed!`; `7 files already formatted` |
| the broad gate — full suite, repository-wide `ruff`, typecheck | not yet |

## Paste-ready fixes

🟡 1 — `seal/ledger.md`, the comment under `### 1788472135-the-run-outlives-its-last-finding`. Two edits; both verified against the hygiene form at a probe commit.

```
seal/ledger.md:777 — replace
only mutation or a review round found (F3, F6, F8, F9, F10, F11). F12 is the
with
only mutation or a review round found (F3, F6, F9, F10, F11, and F8 until
#138 removed it — see the F4 note below). F12 is the
```

```
seal/ledger.md:784-786 — replace
is REMOVED rather than re-pointed and its claim is carried forward by F8 —
which says more than F4 did, because the reason for the rename is part of the
claim now. -->
with
is REMOVED rather than re-pointed. **Corrected 2026-09-24 by work item
1790173106 (#138)**: F8 carried F4's claim forward, and F8 has left this file
too — its bare-`yes` reading went with the code — so the claim now lives in
`seal/ledger/1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row.md`
B2, which the fold moves under this file's `### 1790173106` heading. -->
```

Needs a fix: yes — 🟡 1, the F4 note in `seal/ledger.md` that still names the removed F8 and turns the hygiene workflow's survivor-check step red at the pull request
Loses a record or crashes: no

## Proof block — files opened

Executed in the clone at `7604e522`: the twelve modules above through `bin/test`, the mutation probe, `bin/evidence-check --strict`, `bin/survivor-check` in both ranges, `bin/correction-check`, `uvx ruff`, the Q1 grep. Read: `seal/specs/1790173106-…/{spec,plan,questions,overview,routing,changelog,survivors}.md`, `phases/phase-{1,2,3}.md`, `seal/ledger/1790173106-….md`, the full branch diff against the base, `skills/code-review/scripts/chain_check.py` (`yes_or_no`, `says_reopened`, `stopping_floor`, `run_reopened`, `written_late_reason`, `direct_seal`, `closed_with_a_fix`, the `routing.DIRECT` branch of `main`, the constants), `skills/code-review/scripts/round_record.py` (`terminal_value`, `floor_and_fixes`, `bound_line`, `written_late_cell`), `seal/ledger.md` (the diff, the F4 comment, the anchors on the file), `tests/test_the_record_is_held_to_the_floor_and_the_depth.py` and `tests/test_the_record_is_generated.py` (fixtures and the new cases), `tests/test_routing_is_recorded.py` (fixtures and the new case), `tests/test_the_direct_answer_owes_the_sealers_record.py`, `docs/review-chain-spec.md` (§Review arm, §`Needs a fix`), `skills/implement/orchestration.md` (the four-combinations table, the routing section's closing paragraph, the order inside a ticket), `skills/code-review/orchestration.md` (the sealer's spawn), `agents/sealer.md` (the direct route), `docs/review-handoff-protocol.md` (the `Needs a fix` field), `.github/workflows/hygiene.yml` (the survivor-check step), `skills/evidence-check/scripts/correction_check.py` (the marker rule), `bin/test`. Unverified: the broad gate, the sealer's.
