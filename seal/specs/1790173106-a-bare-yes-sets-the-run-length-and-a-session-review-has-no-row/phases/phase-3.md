# 1790173106-a-bare-yes-sets-the-run-length-and-a-session-review-has-no-row — phase 3

| Field | Value |
|---|---|
| Phase | 3 |
| Commit | 4cd5a561 |
| Ran by | specseal:smith on claude-fable-5-1 |

## What this phase was asked

#241. The seven sentences rewritten (spec items 7–9): the declaration table
row, the checker docstring, the orchestration table and its closing paragraph,
the gate prompt's option 1, the `test_routing_is_recorded.py` docstring and
`templates/sdd-routing.md`'s comment; the paragraph beside the declaration
table saying why two answers; `docs/release-checklist.md` §4's sentence. Case
A8 as a *gone / stands* pinning test, seen red by restoring one old sentence;
A9 and A10 green. Ledger rows on the moved headings re-read; the
`changelog.md` fragment for #241; `overview.md` closed. Q2 and Q3 answered.

## What this phase found

**The frame holds, with two homes it left open now chosen.** Every one of
the seven coordinates was opened at `7ba529c4` and carried the sentence the
spec's table quotes. `spec.md` item 10 names the pinning case's SHAPE and no
file, and `plan.md` says *the new case*: it went to a module of its own,
`tests/test_the_direct_answer_owes_the_sealers_record.py`, because a pin over
a file cannot live in that file (the *gone* phrase would be in it as a
literal), and the gate's option went to `tests/test_routing_is_recorded.py`
through the rendered prompt, because that option is a Python literal split
across lines that a whole-file substring cannot read. Q2's paragraph landed
where its default said, directly under the declaration table.

**Nine cases seen red at `7ba529c4` before any sentence moved** (executed):

```
FAILED …_sealers_record.py::test_each_carrier_says_what_the_direct_answer_requires[parts0..4]
FAILED …_sealers_record.py::test_the_routing_sections_closing_paragraph_names_the_seal_not_the_token
FAILED …_sealers_record.py::test_the_specification_says_why_two_answers_and_not_three
FAILED …_sealers_record.py::test_the_release_checklist_names_the_waiver_as_the_no_work_item_answer
FAILED tests/test_routing_is_recorded.py::test_the_first_option_says_what_the_direct_answer_owes
9 failed, 41 deselected
```

After the edits: the pinning module with `tests/test_routing_is_recorded.py`,
`tests/test_waiver_decided_at_start.py`, `tests/test_docs_line_wrap.py` and
`tests/test_one_word_one_meaning.py` — 128 passed; the direct-arm and
docstring cases of `tests/test_chain_check_at_the_pull_request.py` and the
floor-and-depth module — 23 passed; fifteen modules that read the edited
documents and the gate prompt (`test_chain_hooks.py`,
`test_chain_hooks_hardening.py`, `test_a_section_marked_for_one_role_…`,
`test_the_rules_have_one_owner.py`, `test_review_axes.py`,
`test_no_real_identifiers.py`, `test_broad_gate_rule.py` and eight more) —
615 passed, 7 skipped, 1 failed on `overview.md` not yet existing, green once
it was written; `test_no_loaded_file_names_a_version_at_or_above_the_running_one`
— 1 passed. All executed.

**Mutations, one old sentence restored at a time, restored from kept bytes
after `4cd5a561`** (executed; `git status` clean after each):

| Mutation | Killed by |
|---|---|
| M7 the orchestration table's direct row says *nothing required* again | the carrier pin for that file |
| M8 the specification's row says *nothing required; the declaration is printed* again | the carrier pin for the spec |
| M9 the closing paragraph says *by the token in every command* again | the closing-paragraph case |
| M10 the gate's option says *CI requires nothing for it* again | the rendered-prompt case in `test_routing_is_recorded.py` |
| M11 the template's comment loses *the sealer's `broad-gate.md`* | the carrier pin for the template |
| M12 the specification loses *Two answers, and not three* | the two-answers case |
| M13 the checklist stops naming the `no work item` answer | the checklist case |

**The pin phrase is live for one sentence per file, checked by count.** *the
sealer's `broad-gate.md`* occurs once in the spec, once in the checker's
docstring (the code names the file through `BROAD_GATE_FILE`), once in the
template, twice in `skills/implement/orchestration.md` (the table row and
the closing paragraph, which has a case of its own) and twice in
`tests/test_routing_is_recorded.py` — so that file is pinned on the
corrected docstring's own words, *requires the sealer's `broad-gate.md` of it
and no reviewer's record*, rather than on the bare phrase the new case's
docstring also carries.

**Eight ledger rows drifted and were re-read**: six anchored on
`hooks/commit-review-gate.py#judge` or the orchestration skill's `##
Orchestrator: how the work is routed` region, the *Review arm* heading row a
second time, and one row anchored on `seal/ledger.md`'s own `### 1788331011`
region — which holds the review-arm row this work item annotated, so it took
two `--reverify` passes to settle (the row it hashes was being re-stamped in
the first). `evidence-check --strict`: 1565 ok, 0 drifted, 0 refused.

**`survivor-check --range 659b4229..HEAD` reported six places**, five sharing
words with the removed F8 and one sharing `run_reopened`'s old body shape
with `written_late_reason`; each is a sentence that is still true or a
deliberate leaving, recorded in `survivors.md` with its quote and grounds.

**Q3, executed** (`chain_check.py#runner_problem`): `the session on Python
3.12` → `None`, `the session on claude-example` → `None`, `the session` →
refused for naming one thing. The vocabulary admits a session as the runner;
only the chain's other rows refuse the state.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the sentence *`straight to the PR` requires nothing* in its seven spellings — *nothing required; the declaration is printed* (spec, checker), *nothing required* (orchestration table), *by the token in every command* (orchestration paragraph), *the one CI requires nothing for* (gate option 1), *requires nothing of it at the pull request* (routing test docstring) | nowhere: each was false since `DIRECT_GATE_FROM`, and the pinning module refuses its return in the six files a substring can read, `tests/test_routing_is_recorded.py` in the seventh |
