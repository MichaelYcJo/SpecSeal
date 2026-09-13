# 1789296100-the-seal-and-ci-read-one-ledger-differently — phase 1

| Field | Value |
|---|---|
| Phase | 1 |
| Commit | `eb0189d` |
| Ran by | unknown — the spawn prompt named no model, and the value is the spawning session's to fill |

## What this phase was asked

Write `tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py` before
anything is fixed: the behavioural case (S1–S3 — a drifted fixture run lenient,
run strict, a clean tree, a BROKEN anchor, an OLD-FORMAT row) and the
structural case (S4–S5 — `broad_gate.py`'s ledger call site carries `--strict`,
`bin/evidence-check` holds no default of its own, and the documents name the
strict reader beside the lenient one). Both seen red, and this record says how
each was seen failing.

## What this phase found

**Red, and what it looked like.** `bin/test tests/test_the_lenient_run_says_what_the_broad_gate_will_say.py -q`
against the unfixed tree: **8 failed, 5 passed**.

| Case | How it failed |
|---|---|
| `test_a_drifted_tree_is_told_what_the_gate_would_say` (S1) | the fixture reached exit 1 and `1 drifted`, and the run ended at `0 work items read · … · 0 external`. The sentence was not in stdout |
| `test_the_line_is_the_last_thing_an_exit_1_run_prints` | same run, `endswith` false — the records arm's counts were the last line |
| `test_the_grading_is_one_function_and_the_line_reads_its_answer` | `AttributeError: module 'specseal_evidence_check' has no attribute 'exit_code'` — the grading was four `return` statements inline in `main`, with no unit to call |
| `test_the_checker_states_the_sentence_once` · `test_the_sentence_is_one_line` · `test_the_notice_borrows_the_word_the_failing_gate_prints` · `test_the_gate_still_passes_the_flag_the_notice_names` | `AttributeError: … has no attribute 'LENIENT_NOTICE'` |
| `test_no_document_describes_the_lenient_reader_alone` (S5) | `these describe one reader alone: ['skills/evidence-check/SKILL.md', 'README.md', 'README.ko.md', 'CONTRIBUTING.md', '.github/workflows/test.yml']` — all five |

**The five that passed are the silence cases, and they passed for no reason.**
S2 and S3 assert that the sentence is *absent* at exit 0 and exit 2. Nothing
prints it yet, so they pass against a checker that does nothing — which is
exactly the counterfeit `agent-contract` §15 is about, one polarity over.
An absence case cannot be shown red by the unfixed tree; it is shown red by a
tree that prints the sentence unconditionally. **Phase 2 owes that mutation**:
make the print unconditional, watch S2 and S3 go red, restore, and record it.

**The line's condition is a function, not a predicate beside one.** `plan.md`
asked for *this run is about to return 1* rather than a second spelling of the
grading. That needs the four `return` statements at
`evidence_check.py:2471-2478` extracted into `exit_code(totals, refused,
drifted, strict)`, so the print reads the answer instead of recomputing it.
The case asserts the extracted unit directly, across the whole grading table
including both records-arm counts, so phase 2's extraction is pinned as a
refactor that changed no grading.

**The structural case reads a call, not a line.** `ledger_call_site()` walks
from `checks[LEDGER]` until the parentheses balance rather than reading
`broad_gate.py:570` by number, so a reformatting that wraps the call does not
read as a missing flag. `spec.md` and `plan.md` both cite the line number;
the case does not, and that is deliberate — a line number is the coordinate
this repository's own ledger rule refuses.

**S5's rule is per-block, not per-file.** `README.md:43` and `README.ko.md:41`
already name `broad-gate` in the sealer's row of the agent table, three hundred
lines from anything about drift. A file-level `in` would have passed both
READMEs on text that has nothing to do with the ledger. The case splits each
file on blank lines and asks for one block carrying `--strict` and `broad-gate`
together, which is what *named beside* means.

**The sentence is asserted as one literal in two files.** `NOTICE` here and
`LENIENT_NOTICE` in the checker, compared for equality. `test_the_sentence_is_one_line`
is beside it because a sentence wrapped across two source lines survives
neither a grep nor a substring assertion — a regression this repository has
already shipped once.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| none | none |
