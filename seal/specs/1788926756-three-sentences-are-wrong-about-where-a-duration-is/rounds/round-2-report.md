# 1788926756-three-sentences-are-wrong-about-where-a-duration-is — round 2 report

The verifying round of a pass that was almost entirely prose. Eleven verdicts
from round 1, six fix commits, no unit added, and one gate that is green for a
reason the pass itself named as a defect.

**All eleven of round 1's verdicts are closed.** Three sentences were fixed in
the tool, eight records were corrected, and I re-derived every one against the
code rather than against the fix table. The pass's own §12 sweep found three
instances round 1 had not named, and all three are corrected.

**What this round opens is one thing, and it is not in the arithmetic.** The
pass diagnosed the survivor-check defect correctly as a defect and then
diagnosed its *mechanism* wrong, and the repair it names — one line in
`corpus` — moves the score by 0.001 and leaves the survivor hidden. Separately,
the reason given for shipping the corrected disclosure sentence unpinned does
not hold: the depth-2 exit it cites cannot apply on this branch, and pinning it
is one function in a module that already reads the exact paragraph.

---

## The survivor is hidden by a different mechanism than the one recorded, and the named repair does not move it

`survivors.md` and `overview.md` §*Not verified* both state the cause as
document frequency:

> The mechanism is document frequency. `weights` is `log2(F / df) / log2(F)`,
> so a phrase's weight falls as more files carry it, and `corpus` excludes a
> work item's `rounds/` records from the pool but not its `survivors.md`.

**The measurement is right and the diagnosis is not.** I reproduced the score
drop exactly — 1.63 at `9d9e717`, 0.76 at `6a22d56` — and then took the two
candidate mechanisms apart one at a time:

| What was changed, one at a time | Score of both candidates | Pool |
|---|---|---|
| nothing (as shipped at `6a22d56`) | **0.758** | 764 |
| every `survivors.md` dropped from `corpus` — *the repair the tree names* | **0.757** | 760 |
| the `written` subtraction in `wanted` disabled | **1.829** | 764 |
| both | 1.853 | 760 |

The proposed one-line change to `corpus` moves the number by a thousandth and
leaves the candidate 0.84 under the floor. The whole effect is `wanted`
(`skills/code-review/scripts/survivor_check.py:517-522`), which subtracts the
n-grams the range **added** from the n-grams it looks for. `corrected`'s own
docstring says why that subtraction exists — *a phrase the fix kept is not a
phrase the fix corrected* — and an exemption quote is by construction the
survivor's own wording, so writing the row does not dilute the phrase's weight,
it deletes the phrase from the search set.

**The reported phrases are the signature, and they are visible in the output.**
At `9d9e717` the shared run is *from the last* together with *span is taken
from*, at 1.63. At `6a22d56` those two phrases are not reported at all and a
different, weaker one — *the last result* — comes back at 0.76. A reweighting
keeps the phrase and lowers its number; this drops the phrase.

**Why it matters beyond the wording.** #308 will be repaired where the tree
points, in `corpus`, the measurement will not change, and the survivor will
stay hidden — with an issue closed over it. The correct surface is the diff
side: `corrected` has to skip a `survivors.md` the same way `corpus` skips a
`rounds/` record, and `records_a_past_round` is the predicate that already
exists to be widened.

Everything else the pass wrote about this is confirmed. `survivor-check` at
`b411e77` with every `seal/specs/*/survivors.md` handed to it exits 0 and
prints *no removed wording is still standing* — no `exempt` line, so the two
excused survivors are absent rather than listed, and the file's own header
guarantee ("an excused survivor is still printed with its grounds") does not
hold. The deferral is also right: this is a change to a gate's behaviour that
CI reads, and a fix pass declining it is correct. What is wrong is the
mechanism and the repair beside it.

**Is shipping the branch acceptable this way?** Yes, on one condition. The
green is not a false green about the branch's own work — both hidden survivors
are shipped release notes that must not be edited, and #307 already owns that
class. What is unacceptable is shipping the wrong repair inside #308, because
that is an issue that will be closed without fixing anything. Correct the two
paragraphs and #308's body, and the branch can go.

## The disclosure sentence is unpinned on grounds that do not exist

`overview.md` §*Not verified* says:

> Pinning it means adding a unit to pin a unit this branch created, which
> `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins
> it* refuses at depth 2 — so it takes that section's exit rather than being
> built here.

Three things are wrong with that, and the first two are checkable.

- **Round 1's record names no parent unit.** `round-1.md:11` reads
  `| New units | none |`. `depth_two` in `round_record.py` builds its parent
  set from every earlier record's `New units` row and returns immediately when
  that set is empty, so the mechanised refusal cannot fire on this branch at
  all. I confirmed the row is honest by AST comparison over the fix range:
  `session_cost.py` and `test_session_cost.py` each added and removed no
  top-level unit.
- **The thing to be pinned is not a unit.** It is a prose paragraph in
  `skills/verify/SKILL.md`. `New units` is derived from a Python AST comparison
  of top-level defs, classes and module-level constants, so a Markdown
  paragraph can never be the parent the section refuses under.
- **The section's own two cases put this at depth 1, and §14 requires it.**
  *A fix pass may add a unit; that unit's fix may not.* A case pinning round
  1's own fix is the first of those, not the second — and the reason the
  section gives for allowing depth 1 is that the unit is read by the round
  that follows, which is this round. `skills/agent-contract/SKILL.md` §14 is
  not optional about it: *a fix that changes what a person sees documents it
  and pins it, in the same commit.*

**The cost of the missing pin is measurable and small.** The paragraph sits
inside the section `tests/test_a_segment_feeds_the_flow_log.py` already loads
and whitespace-collapses through `section_body()` — I confirmed all three of
its new clauses are reachable there and that the old wording is absent. So this
is one function in an existing module with an existing reader, not new
mechanism. Executed both ways: green at `b411e77` (exit 0), red against the
pre-fix `skills/verify/SKILL.md` at `2479859` (exit 1, naming the clause it
lost).

**One gap in the ratified document, which is not this branch's to close.**
`orchestration.md` names two cases — a finding in code that predates the run
(depth 1) and a finding inside a unit an earlier round's *fixes* created (depth
2). A finding inside something the branch's own *implementation* pass wrote is
neither, and that is what round 1's finding 1 was. Both the mechanised check
and the section's stated reasoning resolve it toward allowed, so the answer is
not in doubt — but the section says it by omission. It belongs in `follow-up.md`
or an issue, not here.

## The three refusals to edit an approved document are all correct

Findings 5, 10 and 9 each declined to edit a ratified document and recorded the
divergence instead. All three took the route `skills/implement/SKILL.md:682`
names — *where spec and implementation diverged, both sides quoted, which side
won, and the grounds* — and `templates/sdd-overview.md:24` is the table they go
in. I checked each against the tree rather than against the pass's account.

- **Finding 5.** `plan.md:20-24` still reads *fires strictly less often
  afterwards*, and `overview.md`'s divergence table now carries the executed
  counterexample with both sides quoted. `phases/phase-2.md` carried the same
  conflation in its own words and was corrected there. Correct: editing an
  approved plan to match what was built makes the contract follow the work.
- **Finding 10.** `plan.md:12` and the two `1788700685` lines are left in the
  present tense; `spec.md`'s evidence row is the one that got a marker. The
  distinction holds and I checked it: `plan.md` §Technical context is uniformly
  pre-change, so nothing in it mixes states, while `spec.md`'s table has two
  rows phase 1 rewrote to post-change values sitting beside one that was not —
  and that row now says which state it is.
- **Finding 9.** `seal/ledger.md`'s F5 note no longer asserts the absence is
  whole. It says *the absence this row names is no longer whole and the row
  cannot be re-stamped as though it were*, names `(#272)` by section rather
  than by line, and hands the narrow-or-widen decision to `questions.md` Q4
  with the owner. `evidence-check` exits 0 at 1041 ok · 0 drifted.

## The §12 sweep's three instances are corrected, and it missed a fourth

The three the pass found are all closed, and I re-derived each:

- `spec.md:61` now says the row read *a one-second overlap* and names #145's
  round-3 fixture as the shape that number belongs to.
- The changelog fragment now reads *Nothing this repository has published
  moves, and elsewhere on the machine three printed figures do* — the flat
  claim is gone from the surface a reader outside the work item meets.
- Row 11's Verified cell now carries 1000s and -987s and says it was
  re-measured for #300, from 995s and -992s.

**A fourth instance of the same class is still standing, in the same sentence
round 1's finding 11 corrected.** `overview.md`'s `verified:` line reads *the
two modules the skill change touches (105 passed with the first)*. Executed:
`test_session_cost.py` is 69 and `test_a_segment_feeds_the_flow_log.py` is 27,
so the pair is **96**, and it was 96 at `80cc7ce` where the line was written as
well. No module reading `skills/verify/SKILL.md` has the 36 cases that would
make 105 — the only module in the tree that collects 36 is
`test_the_reopening_is_one.py`, which the skill change does not touch. Round 1
found the wrong number in this line, the fix pass corrected the 69 beside it,
and the second number in the same clause was never re-run.

## And the record's two terminal rows are cut off mid-clause

`round-1.md:12-13` read:

> `| Needs a fix | yes — findings 1 and 7 ship reader-facing sentences that are |`
> `| Loses a record or crashes | no — every defect is a sentence, the arithmetic is |`

Both stop where my round-1 report wrapped the line. What is lost from the first
is the whole substance — *false about the code beside them, and findings 3, 4,
5, 8 and 9 are records asserting things the code and the arithmetic contradict*
— so the record states a terminal condition whose reason is a fragment.

The record is paperwork and corrects in the closing commit. What is behind it
is not: `round_record.py new` takes what stands after the colon on one physical
line and writes it with no complaint when the value continues on the next. That
is a silent truncation of the two fields the run's own bound is read from. It is
pre-existing, outside this branch's diff, and belongs in an issue rather than in
a fix pass here — but the reporting convention that produced it is mine and the
next report will hit it again, so the field wants either a one-line value or a
generator that folds the continuation.

## The broad gate

**Not yet, and now due.** No full-suite, repository-wide lint or typecheck run
has happened on this branch; the last reading is the base's 2,973 passed at
`78d2c12`. `ruff` is not installed in the working checkout, so nothing on this
branch has been linted at all. Both are the orchestrator's, once. Nothing in
this round's findings changes code, so the gate can run as soon as the two
prose corrections and the pinning case land.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | Round 1's 1 — the span disclosure sent a reader looking for a background command | `skills/verify/SKILL.md:429-438` | answered | closed. The paragraph now names batching as the ordinary way in and says 100% of the machine's overlap is intra-turn. Re-derived: the clause is reachable through `section_body()` and the old wording *something running in the background* is absent from the section. **But it is pinned by nothing — see finding 12** |
| 2 | Round 1's 2 — Q3's trigger fired on the wrong threshold and its cost column carried no number | `questions.md` §Q3 | answered | closed. Q3 keeps its three answers, gains the fourth-row trigger correction, and its option table now carries 58 of 169 and 23 of 169 with the largest move. The decision stays the owner's and is in `overview.md` §*Not verified* |
| 3 | Round 1's 3 — *no printed figure moves* was flat in two documents and false machine-wide | `spec.md:76`, `questions.md` Q1, ledger fragment row 4, this item's changelog fragment | answered | closed on all four. Read: `spec.md`'s row, Q1 and fragment row 4 all now say THIS PROJECT's transcripts and name the three moves elsewhere; the changelog fragment reads *Nothing this repository has published moves, and elsewhere on the machine three printed figures do* |
| 4 | Round 1's 4 — three documents merged the three-second fixture with #145's one-second one | ledger fragment row 5, `test_session_cost.py` docstring, `spec.md:61`, #145 `questions.md` | answered | closed. The case docstring now separates the two shapes and says what the fixture pins is the cut rather than the magnitude; `spec.md:61` names the substitution it made. Executed: `bin/test tests/test_session_cost.py -q` is 69 passed, exit 0 |
| 5 | Round 1's 5 — *the refusal fires strictly less often* is false | `plan.md:20-24`, `phases/phase-2.md:44-49` | answered | closed correctly, and the refusal to edit `plan.md` is right. `phases/phase-2.md` is corrected in its own words; the counterexample is in `overview.md`'s divergence table with both sides quoted, which is the route `skills/implement/SKILL.md:682` names |
| 6 | Round 1's 6 — four unprinted sentences named a spawn's result as the cause | `in_windows`, `report_spawns`, two `test_session_cost.py` docstrings | answered | closed. Executed grep over the module, the script and the skill: the only remaining occurrences of *outlived a spawn's result* are the two negative assertions at `test_session_cost.py:2159` and `:2248`, which is what should remain |
| 7 | Round 1's 7 — #145's ungathered fragment shipped the old cause beside the correction | `seal/specs/1788908215-*/changelog.md:59-66` | answered | closed. The fragment now reads *where a call outlives the cut its row ends at* and *the report prints the two sums and refuses the figure instead* |
| 8 | Round 1's 8 — row 8 quoted the deleted expression, row 11 opened with a stale pair | `seal/ledger/1788908215-*.md` rows 8 and 11 | answered | closed, including the second stale pair the report had not named. Row 11's Verified cell now carries 1000s and -987s and says it was re-measured for #300 from 995s and -992s |
| 9 | Round 1's 9 — F5's note narrowed an absence that is not there | `seal/ledger.md:873` | answered | closed. The note asserts the absence is not whole rather than asserting it is, names `(#272)` by section, and hands the decision to `questions.md` Q4. Executed: `evidence-check` exits 0 at 1041 ok · 0 drifted |
| 10 | Round 1's 10 — the dead expression restated in the present tense in four documents | `spec.md:75`, `plan.md:12`, `1788700685` `plan.md:16` and `overview.md:19` | answered | closed correctly. Read both: `plan.md` §Technical context is uniformly pre-change so nothing in it mixes states, and `spec.md`'s row sits in a table two of whose rows phase 1 rewrote — which is the one that needed the marker and now has it |
| 11 | Round 1's 11 — the proof line said 68 passed against a module that passes 69 | `overview.md` §verified | answered | the 69 is corrected and executed. **The second number in the same clause was not swept — see finding 14** |
| 12 | **The corrected disclosure sentence ships unpinned, and the depth-2 exit given for it cannot apply.** `round-1.md:11`'s `New units` row reads `none`, so `depth_two` returns before testing anything; the parent named is a Markdown paragraph, which `New units` can never hold; and `agent-contract` §14 requires a fix that changes what a person sees to pin it in the same commit | `skills/verify/SKILL.md:429-438`, `tests/test_a_segment_feeds_the_flow_log.py`, grounds at `overview.md` §*Not verified* | open | 🟡. Executed: AST comparison over `2479859..addd8ca` adds and removes no top-level unit in either Python file, so the `none` in that row is honest and the parent set is empty. The pin is one function in a module that already loads the section — green at `b411e77` exit 0, red against `2479859`'s `SKILL.md` exit 1 |
| 13 | **The mechanism recorded for the hidden survivor is the wrong one, and the repair named beside it moves the score by 0.001.** Both files say document frequency and name a one-line change to `corpus`; the whole effect is the added-n-gram subtraction in `wanted` | `seal/specs/1788926756-*/survivors.md`, `overview.md` §*Not verified* | open | ⬜ correction — both locations are under `seal/specs/`, so `Needs a fix` does not count it. Executed, one change at a time: `corpus` without every `survivors.md` gives 0.757 against 0.758 as shipped; `wanted` without the `written` subtraction gives 1.829. The reported phrase changes from *span is taken from* to *the last result*, which is deletion from the search set and not reweighting. #308's body needs the same correction |
| 14 | **`overview.md`'s `verified:` line says 105 passed for the two modules the skill change touches; the pair is 96.** The same clause round 1's finding 11 corrected, one number over | `overview.md` §verified | open | ⬜ correction. Executed: 69 and 27 through `bin/test`, 96 together, and 96 at `80cc7ce` where the line was written. No module reading `skills/verify/SKILL.md` collects 36; the only 36 in the tree is `test_the_reopening_is_one.py` |
| 15 | **`round-1.md`'s two terminal rows stop mid-clause**, so the record states a bound whose reason is a fragment | `rounds/round-1.md:12-13` | open | ⬜ correction. Read both files: the report's values wrap across two physical lines at `round-1-report.md:528` and `:532`, and the record carries only the first |
| 16 | **`round_record.py new` truncates a wrapped `Needs a fix` or `Loses a record or crashes` value silently**, which is how finding 15 happened | `skills/code-review/scripts/round_record.py` | open | 🟡, pre-existing and outside this branch's fix range. Not a fix for this branch's pass — it belongs in an issue with finding 12's documentation gap. Read, not executed against the generator |
| 17 | The prompt's *51 assertions in that module* is 49 | `tests/test_a_segment_feeds_the_flow_log.py` | withdrawn | ⬜, and nothing to correct: the number appears in no tracked file, only in the spawn prompt. Executed: 49 `Assert` nodes over 27 test functions by AST, and `grep -c` agrees |

## Executed probes

| What was run | Result |
|---|---|
| `survivor-check --range 78d2c12..b411e77` with every `seal/specs/*/survivors.md` handed to it, as CI does | exit 0, *no removed wording is still standing* — and **no `exempt` line**, so both excused survivors are absent rather than printed with their grounds |
| `examine` on the two shipped-release-note candidates at four commits | 1.63 at `9d9e717`; 0.76 at `6a22d56`, `addd8ca` and `b411e77`. The floor is 1.6 |
| the two candidate mechanisms, one at a time | `corpus` minus every `survivors.md`: 0.758 → 0.757, pool 764 → 760. `wanted` minus the `written` subtraction: 0.758 → **1.829**. Both: 1.853 |
| `bin/test tests/test_session_cost.py -q` at `b411e77` | 69 passed, exit 0 |
| `bin/test` on both modules the skill change touches, at `b411e77` and at `80cc7ce` | 96 passed both times, exit 0 — against `overview.md`'s 105 |
| whole-suite collection, `--collect-only` — collection, never a run | 90 modules, 2,998 cases. The only module collecting 36 is `test_the_reopening_is_one.py` |
| the proposed pinning case for the disclosure paragraph | green at `b411e77` exit 0; red against `2479859`'s `skills/verify/SKILL.md` exit 1, naming the clause it lost |
| AST unit comparison over `2479859..addd8ca` | `session_cost.py` and `test_session_cost.py` each add and remove no top-level def, class or module-level constant — the `none` in round 1's `New units` and `Contract changes` rows is honest |
| `bin/evidence-check` | exit 0 — total 1041 ok · 0 drifted · 0 broken · 0 external · 0 old-format |
| `bin/unverified-check` | exit 0 — 205 open · 46 closed · 0 unreadable, and it prints the wrong mechanism from finding 13 on every run |
| grep for the removed cause across the script, the module and the skill | the only remaining *outlived a spawn's result* are the two negative assertions at `test_session_cost.py:2159` and `:2248` |
| the row shape behind the pass's own measurement correction | confirmed. `session_cost.py:707-747` builds a row as `{**labels, "window": …, "turns": …}` with the count under `numbers["calls"]`, so `row.get("calls")` is `None` for every row and the first sweep was measuring nothing |

```
# In a `git clone --no-local` of the repository at b411e77, from the clone
# root, with a `uv` venv because pytest is not installed for the system
# interpreter. The probe was named test_tmp_pin.py, run once, and deleted;
# the clone tree is clean and nothing was written in the working checkout.

uv venv .venv && uv pip install --python .venv/bin/python pytest
./bin/test tests/test_session_cost.py tests/test_a_segment_feeds_the_flow_log.py -q ; echo $?
./bin/evidence-check ; echo $?
./bin/unverified-check ; echo $?

python3 skills/code-review/scripts/survivor_check.py --range 78d2c12..b411e77 \
  $(for f in seal/specs/*/survivors.md; do printf -- "--exempt %s " "$f"; done) ; echo $?

# The mechanism isolation, in outline: import survivor_check as a module, then
# run its own pipeline four times over the range 78d2c12..6a22d56 --
#   gone, written = corrected(root, A, B)      # `written = set()` for arm 3
#   keep = wanted(gone, written)
#   pool = corpus(root, B)                     # `survivors.md` filtered for arm 2
#   where, files = carriers(pool, keep)
#   score(gone, keep, where, weights(len(pool), files), 0.01)
# and read the two shipped-release-note rows out of the result.
```

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| What the report should print where `command` exceeds 100% of the span | `questions.md` Q3, already deferred by round 1 — named here so it is not re-litigated | the owner |
| Whether F5's clause narrows to its three literals or the case widens to the shape | `questions.md` Q4, already deferred by round 1 | the owner |
| Whether the disclosure belongs in the report's own output as well | `questions.md` §*Open, and it is small*, already deferred by round 1 | the owner |
| `orchestration.md` names no case for a finding inside something the branch's own implementation pass wrote — finding 12's third bullet | an issue, with finding 16 | the orchestrator |
| `round_record.py new` silently truncating a wrapped terminal-condition value — finding 16 | an issue | the orchestrator |
| The full suite, the repository-wide lint and the typecheck; `ruff` is not installed in the working checkout | `agent-contract` §2 — the orchestrator's, once, and now due | the orchestrator |
| Windows | #103's standing gap, already deferred by round 1 | nobody has run it |

## Paste-ready fixes

For finding 12 — the pinning case. It goes at the end of
`tests/test_a_segment_feeds_the_flow_log.py`, beside the other cases that read
the same section:

```
def test_the_section_names_batching_as_the_way_a_share_passes_one_hundred():
    """A share over 100% is a true reading, and WHY it happens is the half a
    person acts on. The paragraph used to send that reader looking for a
    background command; measured over one machine's transcripts, 100% of the
    overlap above a second is calls batched into one assistant message and
    none of it crosses a turn. Nothing else in the tree reads this clause, so
    without this case an edit can put the rarer cause back as the ordinary
    one and no check says anything."""
    body = section_body()
    assert "calls running at once" in body, (
        "the paragraph must name concurrent calls as what puts a share over "
        "100%, not something running in the background"
    )
    assert "batched into one message" in body, (
        "batching is the ordinary way a share passes 100% and the paragraph "
        "has to say so — a reader sent to look for a background command "
        "finds nothing and reads the share as broken arithmetic"
    )
    assert "crossed a turn" in body, (
        "the measured claim is that none of the overlap crosses a turn; "
        "without it the paragraph asserts a cause it does not bound"
    )
    assert "something running in the background" not in body, (
        "the old wording named the rarer cause as the ordinary one"
    )
```

For finding 13 — the two paragraphs in `survivors.md`. Replace the diagnosis
sentence:

```
**Writing the two rows below did not excuse those survivors — it hid them,
and that is a defect in the checker rather than in the rows.** Executed:
`examine` scores both candidates at **1.626** at `9d9e717`, above the 1.6
floor, and **0.758** at `6a22d56`, the commit that changed this file and
nothing else. The mechanism is the added-n-gram subtraction, not document
frequency. `corrected` returns the n-grams the range WROTE alongside the
sentences it removed, and `wanted` subtracts them from what the run looks
for at all — because a phrase the fix kept is not a phrase the fix
corrected. An exemption quote is by definition the survivor's own wording,
so writing the row puts those phrases on the written side and deletes them
from the search set. The reported phrase changes rather than weakening:
*span is taken from* at 1.626 before the row, a different and weaker *the
last result* at 0.758 after it. Dropping every `survivors.md` from `corpus`
moves the same candidates from 0.758 to 0.757, so document frequency is
worth a thousandth here and is not the cause.
```

and the repair named after it:

```
**It is not fixed here, and the surface is the diff side rather than the
corpus.** `corrected` has to skip a `survivors.md` the way `corpus` already
skips a `rounds/` record, which is `records_a_past_round` widened to a
second shape — a change to a gate CI reads, which is mechanism a fix pass
may not add (`skills/code-review/orchestration.md` §*A fix pass adds the
unit that pins it*). It is handed to the orchestrator as an issue, separate
from #307. Excluding `survivors.md` from `corpus` is the repair this note
first named and it does not work: measured, it moves the score by 0.001.
```

For finding 14 — `overview.md`'s `verified:` line. The clause reads *the two
modules the skill change touches (105 passed with the first)*:

```
            the two modules the skill change touches (96 passed with the
            first — `tests/test_session_cost.py` 69 and
            `tests/test_a_segment_feeds_the_flow_log.py` 27),
```

For finding 15 — `round-1.md`'s two rows, restored to what the report's values
actually say:

```
| Needs a fix | yes — findings 1 and 7 ship reader-facing sentences that are false about the code beside them, and findings 3, 4, 5, 8 and 9 are records asserting things the code and the arithmetic contradict |
| Loses a record or crashes | no — every defect is a sentence, the arithmetic is correct on every axis swept, and nothing leaves the root or raises |
```

For finding 16 — one line in the report convention, which is the cheaper half.
Both terminal lines are written unwrapped, however long, so the generator's
one-physical-line read is always the whole value. The generator side wants an
issue rather than an edit from this branch.

---

Needs a fix: yes — finding 12, one case pinning the corrected disclosure clause at `skills/verify/SKILL.md:429-438`; §14 requires it and the depth-2 exit cited for declining it cannot apply, because `round-1.md`'s `New units` is `none` and the parent named is prose rather than a unit
Loses a record or crashes: no — every finding this round is a sentence or a missing case, `evidence-check` and `unverified-check` both exit 0, and nothing leaves the root or raises

## Proof

Opened, in a `git clone --no-local` at `b411e77` unless noted:

- `skills/code-review/scripts/survivor_check.py` — the module docstring's
  §*What is excluded*, `records_a_past_round`, `corpus`, `corrected`, `wanted`,
  `carriers`, `weights`, `weigh`, `runs`, `score`, `examine`,
  `read_exemptions`, `FLOOR`
- `skills/code-review/scripts/round_record.py` — the module docstring's field
  list, `units_named_earlier`, `location_units`, `depth_two`, `resolve_path`,
  `tracked_at`
- `skills/code-review/orchestration.md` — §*A fix pass adds the unit that pins
  it*, §*Then say who checked them, in the record*, §*And name the fix surface,
  in the same record*
- `docs/review-chain-spec.md` — §*The last round verifies, and what it verifies
  is a diff*, §*The depth in `New units`*
- `skills/verify/SKILL.md:429-441` — the span paragraph and the refusal
  paragraph under it, at `b411e77` and at `2479859`
- `skills/verify/scripts/session_cost.py` — `in_windows`, `report_spawns`, the
  row construction at 707-747, `analyse`'s span expression
- `tests/test_session_cost.py` — the two changed docstrings, the two negative
  assertions at 2159 and 2248, `test_a_head_call_outlives_the_cut_without_outliving_a_spawns_result`
- `tests/test_a_segment_feeds_the_flow_log.py` — the module header, `read`,
  `section_body`, `SECTION_HEADING`, and every assertion in it
- `skills/implement/SKILL.md:71`, `:118`, `:680-690` — the overview memo's four
  sections
- `templates/sdd-overview.md` — §*Where spec and implementation diverged*,
  §*Not verified*
- `seal/specs/1788926756-three-sentences-are-wrong-about-where-a-duration-is/`
  — `overview.md`, `spec.md`, `plan.md`, `questions.md`, `changelog.md`,
  `survivors.md`, `phases/phase-2.md`, `rounds/round-1.md`,
  `rounds/round-1-report.md`
- `seal/ledger.md:865-880` — F1 through F6, and F5's note in full
- `seal/ledger/1788926756-three-sentences-are-wrong-about-where-a-duration-is.md`
  — rows 4 and 5
- `seal/ledger/1788908215-the-orchestrator-is-measured-by-the-whole-session.md`
  — rows 8 and 11
- `seal/specs/1788908215-the-orchestrator-is-measured-by-the-whole-session/changelog.md:55-72`
- `bin/survivor-check`, `bin/test`
- the full diff of `2479859..addd8ca`, all fourteen files
