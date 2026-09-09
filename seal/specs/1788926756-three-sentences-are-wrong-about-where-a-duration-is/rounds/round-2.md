# 1788926756-three-sentences-are-wrong-about-where-a-duration-is — review round 2

| Field | Value |
|---|---|
| Target SHA | b411e77 |
| Ran by | specseal:warden on claude-opus-5 |
| PR | #306 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — finding 12, one case pinning the corrected disclosure clause at `skills/verify/SKILL.md:429-438`; §14 requires it and the depth-2 exit cited for declining it cannot apply, because `round-1.md`'s `New units` is `none` and the parent named is prose rather than a unit |
| Loses a record or crashes | no — every finding this round is a sentence or a missing case, `evidence-check` and `unverified-check` both exit 0, and nothing leaves the root or raises |

- [ ] Pass

## What this round was asked

The verifying round of a pass that was almost entirely prose, on a branch
whose green survivor check was green for a reason that is itself a defect. It
was asked three things: whether the depth-2 exit was taken correctly and
whether an unpinned disclosure sentence may ship, whether three refusals to
edit an approved document were right, and whether the branch may ship while
#308 stands.

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

## Paste-ready fixes

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
```
            the two modules the skill change touches (96 passed with the
            first — `tests/test_session_cost.py` 69 and
            `tests/test_a_segment_feeds_the_flow_log.py` 27),
```
```
| Needs a fix | yes — findings 1 and 7 ship reader-facing sentences that are false about the code beside them, and findings 3, 4, 5, 8 and 9 are records asserting things the code and the arithmetic contradict |
| Loses a record or crashes | no — every defect is a sentence, the arithmetic is correct on every axis swept, and nothing leaves the root or raises |
```

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

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `skills/verify/SKILL.md:429-433` | round 1's 1 — fixed |
| round-1 | `questions.md` §Q3 | round 1's 2 — answered |
| round-1 | `spec.md:76`, `questions.md` Q1, `seal/ledger/1788926756-*.md` row 4 | round 1's 3 — answered |
| round-1 | `seal/ledger/1788926756-*.md` row 5, `tests/test_session_cost.py` head-cut docstring, #145 `questions.md:100` | round 1's 4 — fixed |
| round-1 | `plan.md:20-24`, `phases/phase-2.md:44-49` | round 1's 5 — answered |
| round-1 | `#in_windows`, `#report_spawns`, two `tests/test_session_cost.py` docstrings | round 1's 6 — fixed |
| round-1 | `seal/specs/1788908215-*/changelog.md:59-66` | round 1's 7 — answered |
| round-1 | `seal/ledger/1788908215-*.md` rows 8 and 11 | round 1's 8 — answered |
| round-1 | `seal/ledger.md:873` | round 1's 9 — answered |
| round-1 | `spec.md:75`, `plan.md:12`, `seal/specs/1788700685-*/plan.md:16` and `overview.md:19` | round 1's 10 — answered |
| round-1 | `overview.md` §verified | round 1's 11 — answered |

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
