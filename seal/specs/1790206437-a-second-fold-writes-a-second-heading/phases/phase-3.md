# 1790206437-a-second-fold-writes-a-second-heading — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 171feacf |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

The two sentences and the class (#542): the two paste-ready blocks from
`seal/specs/1790174138-…/rounds/round-3-report.md` §Paste-ready fixes,
verbatim, into `round_record.py`'s `new_broad_gate_file` and
`kept_broad_gate`; the written-file case in the seal module red on both
halves; the two further carriers `spec.md` S11b names
(`docs/review-handoff-protocol.md:171`, `skills/code-review/orchestration.md:528`)
read against `templates/sdd-round.md:39` and reworded where they state the
replaced rule, judgment per carrier here; A9 re-read with a dated note; A11
corrected in place (Q3's default).

## What this phase found

**The frame holds, and one of its lists disagrees with itself.** `spec.md`
§Data & interfaces lists `skills/code-review/orchestration.md` under
*Unchanged on purpose*, while S11b and judgment 10 send this phase to
reword that file's sealer paragraph where it states the replaced rule. The
spawn prompt repeats S11b, so S11b won: the paragraph is reworded, and the
unchanged list is wrong by one file. Recorded in `overview.md` as a
divergence.

**The two blocks landed verbatim.** The comment's last sentence is the
report's five lines byte for byte; the docstring's count sentence is the
report's three, and the two lines after it were re-wrapped so no line
passes 88 columns (`ruff check` exit 0). `kept_broad_gate`'s body is
unchanged.

**Judgment per carrier (S11b, §12):**

- `docs/review-handoff-protocol.md`'s `Broad gate` row said *a run taken
  again after a pre-existing failure or a late fix leaves both on the
  record*. False for a re-run at the same commit against the same base,
  which `same_run` replaces. Reworded in one clause: *a run taken again at
  a new commit after a pre-existing failure or a late fix leaves both on the
  record, while a run the newest entry already records — the same commit
  against the same base — replaces that entry*. The stands phrase
  `earlier run` survives; the gone phrase `GATE_CARRIERS` pins for this file
  is still absent.
- `skills/code-review/orchestration.md`'s sealer paragraph said the new
  entry goes *in front of any run the cell already held, which stays behind
  it as `earlier run`*. Same falsehood, same one-clause repair: *unless that
  run is the same commit against the same base, which the new entry
  replaces*. The paragraph below it (*a run the cell already holds is kept
  behind the new entry by either writer*) states the same rule for
  `close --broad-gate` and got the same clause — one cause, two instances
  in one file, both closed. `test_the_writers_are_named_as_one_path`'s
  phrase *through the same newest-first path* survives.
- The other carriers `GATE_CARRIERS` pins (`agents/sealer.md`,
  `agents/warden.md`, `docs/review-chain-spec.md`, `skills/code-review/SKILL.md`,
  `skills/verify/SKILL.md`, `templates/sdd-round.md`) were re-grepped at this
  tree for *taken again*, *stays behind*, *earlier one stays*, *count of
  runs* and *count of entries*: no hit outside `round_record.py` and the
  two files above (four hits in `session_cost.py`, `payload_meter.py` and
  the agent contract are other senses of *taken against* and *stays
  behind*). The class is closed at five carriers, as judgment 10 counted.

**Q3 decided: in place.** A11's clause *is a code comment no test pins*
reads *was a code comment no test pinned* with a `Corrected 2026-09-24`
note naming S10's case; its anchors are untouched. A9 carries a
`Re-read 2026-09-24` note and its `kept_broad_gate` stamp moved
(`c2a4e86c → 43a33862`) by `evidence-check --reverify`. Two further rows
whose anchors this phase moved were found by the same run, and each got a
note: A5 (§0.15.0) on `new_broad_gate_file@42eea32e → 86221033`, and the
`1790101577` seam row on `orchestration.md#"# code-review — the
orchestrator's half"@d1260907 → ca84bf79`. Neither claim moved.
`correction-check --range origin/release/v0.15.1...HEAD`: exit 0 (no merge
commit in the range, so nothing to drop).

**Red first, executed.** S10's stands half at `20ede02c` against the
unedited generator: 1 failed, exit 1 (*the written comment does not state
the same-run replace*). The gone half by mutation after the edit, restored
from kept bytes: the old sentence restored in place — 1 failed (stands
half); the old sentence written after the new one, lowercase — 1 failed
(gone half, *still states the rule `same_run` replaced*). A first mutation
restored the old sentence with a capital *A* and the case passed: the
absence check is case-sensitive, as the `GATE_CARRIERS` pairs are, and the
mutation was corrected rather than the case widened.

**Green, executed.** `bin/test tests/test_the_seal_is_taken_once_by_the_sealer.py
tests/test_the_broad_gate_cell_keeps_every_run.py -q`: 130 passed in
101.72 s, exit 0. `bin/test tests/test_the_fixes_close_the_record.py -k
broad_gate -q`: 1 passed, exit 0. `tests/test_docs_line_wrap.py` and
`tests/test_a_merge_cannot_silently_drop_a_correction.py`: 81 passed, exit
0. `uvx ruff check` and `uvx ruff format --check` over `round_record.py` and
the seal module: exit 0 each. `evidence-check --strict .`: `1662 ok · 0
drifted · 0 broken`, exit 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sentence *a run taken again is written in front, and the earlier one stays behind it* from the comment every `broad-gate.md` is written with, and *the count of runs* from `kept_broad_gate`'s docstring | nowhere — the rule they stated was replaced by `same_run` in 0.15.0; the eleven `broad-gate.md` files already committed keep the old sentence as records of the runs that wrote them (`plan.md` §Operational impact) |
