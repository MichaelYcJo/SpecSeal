# 1790076050-the-release-tail-is-three-acts-no-document-names — phase 4

| Field | Value |
|---|---|
| Phase | 4 |
| Commit | `cdfcc40b` |
| Ran by | smith on claude-opus-5[1m] |

## What this phase was asked

`size: now` exists and stops existing on the issue it is spent on.
`.github/scripts/tracker_labels.py` with `--check`/`--apply`, a step in
`close-issues-on-release.yml`, the removal inside
`close_issues_on_release.py#main`, and `docs/issues-and-milestones.md`
gaining where the judgment is made, what removes a spent label and that no
sweep is owed — with the one pinned sentence reworded and
`tests/test_a_release_is_sized_by_a_criterion.py`'s literal moved in the same
commit. A case for A9, A10, A11, A12; the existing case carries A13.

## What this phase found

### The spec named one pinned sentence that would move. There were two.

`spec.md` §*Judgments* 10 anticipated
`test_a_release_is_sized_by_a_criterion.py#test_the_label_is_two_states_and_nothing_reads_it` — NAME NOT IN TREE
(renamed by round 1's finding 4 to
`test_the_label_is_two_states_and_nothing_schedules_from_it`),
whose literal `**Nothing reads this label**` becomes false the moment
something reads it. It moved as planned.

The second was not anticipated and was found by running the suite:
`tests/test_release_hygiene.py#test_the_script_only_ever_closes` asserts that
`close_issues_on_release.py` never gains `"gh", "issue", "<verb>"` for six
verbs, **`edit` among them**. A11 is precisely an `issue edit`, so that case
was red the moment the removal landed.

It was not treated as an obstacle and not quieted. **The property the case
protects was never the verb** — its own message says so: *only ever closes is
what makes a re-run and a force-push safe to reason about*. Both new acts are
idempotent, the close by skipping an issue already closed and the removal by
happening only after a read says the label is there, so the property holds
and the assertion had been spelled in terms of a proxy for it. The case now
allows one `issue edit`, requires it to carry `--remove-label`,
refuses `--add-label` outright — adding a label is the sibling's act at the
squash, and a second writer is how two scripts come to disagree about the
current answer — and keeps the other five verbs forbidden. The script's own
docstring made the same *the only write is a close* claim and moved with it,
in this commit (`agent-contract` §14).

### Four ledger anchors drifted across four rows, and one row was removed

The handoff said five rows anchor the edited heading; phase 1 measured three
(G5, S4, R2). Phase 4's edits drifted three anchors, reaching those three
rows plus a fourth the handoff did not mention.

| Row | Anchor that drifted | Judgment |
|---|---|---|
| G5 | the document heading | **re-verified** — the claim is the flow-log title format's home. Still in this section at lines 96 and 112, and `grep -c 'chore: flow measurement' skills/verify/SKILL.md` still returns 0. The edit is one hunk from line 145 on, below both |
| S4 | the document heading | **re-verified** — the claim is that two documents state the version rule, not three. The sentence is at line 100 with its below-the-running half at 103; the new paragraphs state no version boundary |
| S3 | `label_merged_on_release_branch.py#issue_labels` | **re-verified** — the claim is that re-running the signal writes nothing twice, by construction. The unit is now a one-line delegation to the same logic on the same `_issue_api`; `main`'s `if label in carried` guard is untouched and the case it names was re-run green |
| **R2** | the heading **and** the sized-by-a-criterion case | **REMOVED** — see below |

**R2 is the case the handoff described and the only one that arose.** Its
claim ended *and **nothing reads it***, which this phase makes false.

**No document carries an arm for it, and this record used to say one did.**
Round 1's finding 5 is that correction. The section with the arms is
`CONTRIBUTING.md` §*House rules*, not §*Running the checks*, which is the
pytest-and-ruff section and says nothing about a row beyond naming a command.
And §*House rules* does not reach this case either — both of its arms are
conditioned on the cited code changing:

> - the claim still holds and you have re-read it — run `evidence-check --reverify .`
> - the claim went with the code — **remove the row and write the new claim into your own fragment.**
>
> So a claim leaves `seal/ledger.md` when the code it was about does.

R2's code went nowhere. Both anchors still resolve and `evidence-check`
agrees. What happened is a third thing the two arms do not name: **a claim
falsified by code this branch ADDED.** `CLAUDE.md`'s copy of the rule is the
same two arms, so the tree is silent on it from both sides.

**The act taken is still the right one**, which is why the removal stands.
`--reverify` would leave a false claim standing under a fresh hash, and a
stamp asserts that somebody read the claim and found it true — so the arm
that looks closest is the one that writes a lie. Removing the row and
rewriting the claim is what the second arm would say if its condition were
*the claim went false* rather than *the code went away*.

What is owed is the gap, not a different act, and it is a policy change a fix
pass may not make: it is now a row of `seal/follow-up.md` with the repository
owner named, at the next change to `CONTRIBUTING.md` §*House rules*.

T1 of `seal/ledger/1790076050-the-release-tail-is-three-acts-no-document-names.md`
carries the claim forward, corrected, against five coordinates.

R2's own Notes had already named the gap this phase closes: *nothing pins the
label against the tracker — a label that is never created, or created under a
different spelling, leaves the document describing something absent, and no
check can see that.* That is still true of the tracker's live state, and T2
closes it from the side a check can reach: the declaration and the document
are held together in the tree, and the workflow carries the declaration to
the tracker.

`seal/ledger.md` moved by 3 insertions and 4 deletions in total — three
re-read notes and R2's line. The unscoped read afterwards: **1452 ok, 0
drifted, 0 broken**, up from 1440. **Corrected in round 1's fix pass**: this
said `R2's two anchors out, the fragment's fourteen in`, and both figures were
wrong in ways that cancel. `seal/ledger.md` alone goes 1440 → 1439, so **one**
anchor left it — R2's document anchor is byte-identical to S4's and the checker
counts a file's coordinates once — and the fragment carried **13**, not 14.
1439 + 13 is 1452 either way, which is why the arithmetic never complained.
The fragment carries 14 as of round 1's fix pass, which added
`close_issues_on_release.py#spend_label` to T1, so the corpus reads 1453.

### A YAML step is anchored by its whole `- name:` line

The fragment's first spelling of the workflow anchor quoted the step's name
text alone and came back with *no place — the check calls this row BROKEN*.
Every existing workflow anchor in `seal/ledger.md` quotes the full line,
`- name: …` included. Corrected before the stamp; no BROKEN row was ever
committed.

### `gh label list` reproduces #450 today

**Read 2026-09-22**: the live tracker has no label matching `size` at all,
which reproduces the ticket's 2026-09-20 measurement. The colour was taken
from `chain: capped` rather than from the topic labels — a divergence from
`spec.md` §*Judgments* 11, recorded in `overview.md` with grounds.

### How each case was shown red (§15)

Seventeen mutations across four files, each removing one behaviour, sentence
or step, with every file restored from a byte copy kept outside the tree.
`57 passed` before and after.

| Mutation | Case that went red |
|---|---|
| the description stops being the document's own sentence | `test_a_missing_label_is_created_with_the_documents_own_sentence` |
| the description drops when the label stops being current | the same case |
| the create runs without a read saying the name is absent | `test_reconciling_an_already_complete_tracker_writes_nothing` |
| `--check` acts instead of only reporting | `test_check_reports_and_writes_nothing` |
| the specifying document is dropped from the declaration | `test_every_declared_label_says_which_document_specifies_it` |
| the reconcile step is removed from the workflow | `test_the_workflow_runs_the_apply_arm_and_needs_no_new_permission` |
| the spent label is never removed | three A11 cases |
| **the removal moves before the close** | `test_the_close_comes_first_so_a_failed_label_write_cannot_cost_it` |
| a failing label write stops the run instead of reporting | `test_the_issue_closes_even_when_the_label_write_fails` |
| the label is removed without reading whether it is there | `test_an_issue_without_the_label_gets_no_label_call` |
| the sibling copies the reader back | `test_the_label_reader_has_one_source` |
| the document drops when the judgment is made | `test_the_document_answers_what_it_left_open[when …]` |
| the document drops what removes a spent label | the same case, `[what …]` |
| the document drops the no-sweep rule | the same case, `[no …]` |
| the no-sweep rule keeps its verdict and loses its reason | `test_the_no_sweep_rule_carries_its_reason` |
| **the sentence reverts to `Nothing reads this label`** | `test_the_label_is_two_states_and_nothing_reads_it` (NAME NOT IN TREE — renamed by round 1's finding 4 to `…_and_nothing_schedules_from_it`) |
| the sentence stops naming the workflow that reads it | the same case |

**The first run of all seventeen reported NOTHING red**, and that was the
mutation harness rather than seventeen worthless cases: three module names
were passed as one string and became a single pytest path argument that
matched no file, so every run collected nothing and printed no FAILED line.
The tell was the restored run printing no count either. The harness now
raises when a run produces no count line, because a mutation run that did not
happen and a mutation nothing catches look identical in the output — which is
`skills/verify`'s *a check that cannot fail is a counterfeit* arriving one
level up, inside the thing that was checking the checks.

### Two other reds, and only one of them was this phase's

Running the neighbouring modules produced a second failure,
`test_the_gate_names_every_step_ci_runs.py#test_a_repository_with_no_hygiene_workflow_is_sealed_exactly_as_before`.
**It is not this branch's**, and it was measured rather than argued: the case
asserts `"release" not in result.stderr.replace(str(repo), "")`, which strips
the fixture repository's path but not the interpreter's — and this worktree's
own path is `…/wt-release-tail/.venv/bin/python`. A throwaway worktree of
**the same commit** at a path with no `release` in it runs the case green.
The probe worktree was removed and `git worktree list` confirms nothing was
left behind (§7).

So the case is sensitive to the path a checkout sits at, and any worktree
named for a release branch fails it. Nothing here changes it — it is outside
this work item's scope and belongs to whoever owns that module — and it is in
`overview.md`'s `## Not verified` with the sealer named, because the broad
gate runs from wherever the sealer is standing.

### What a gate change owes (`CONTRIBUTING.md`)

- **Test seen red**: the seventeen above.
- **Failure direction**: the reconcile step fails only if `gh` itself fails;
  a missing label is created and a complete tracker is a no-op, so there is
  no red for the *state* of the tracker. The label removal never fails the
  job at all, which is the asymmetry T1 records. A gate that failed a pull
  request for a missing label was rejected, with grounds in `plan.md`.
- **Prompt budget: zero.** Both run on GitHub after a push to `main`, in a
  job that already exists, with nobody at a keyboard.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/ledger.md`'s R2, whose claim ended *and nothing reads it* | T1 of `seal/ledger/1790076050-the-release-tail-is-three-acts-no-document-names.md`, corrected and against five coordinates |
| the sentence `**Nothing reads this label**` from `docs/issues-and-milestones.md` | replaced in place by `**Nothing schedules from this label**` plus the paragraph naming the one workflow that reads it; `test_the_label_is_two_states_and_nothing_reads_it` (NAME NOT IN TREE — renamed by round 1's finding 4 to `…_and_nothing_schedules_from_it`) pins both halves |
| the blanket ban on `gh issue edit` in `tests/test_release_hygiene.py` | the same case, restated: one `issue edit`, carrying `--remove-label`, never `--add-label`, and the other five verbs still forbidden. **This phase wrote `at most one`, and review round 2 changed it to EXACTLY one** — `<= 1` passes at zero, which is what let the whole parsed block be skipped by a re-spelled argv; the reason is at `tests/test_release_hygiene.py#test_the_script_closes_and_takes_off_one_named_label_and_nothing_else` |
| `label_merged_on_release_branch.py#issue_labels`'s own unpacking of `closer._issue_api` | `close_issues_on_release.py#issue_labels`, the module that owns that read; the sibling delegates and `seal/ledger.md`'s S3 was re-read against the move |
