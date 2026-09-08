# 1788826000-a-stamp-names-content-not-a-commit — phase 6

| Field | Value |
|---|---|
| Phase | 6 |
| Commit | `c381371` |
| Ran by | `smith on unknown — the spawn prompt named the agent and not the model` |

## What this phase was asked

Make the documents say what the code now enforces: `seal/follow-up.md`'s
statement of the convention, and `templates/sdd-round.md`'s answer for
`Target SHA`. Pin both.

## What this phase found

**A third document was falsified by this change and nothing pointed at it.**
`tests/test_ci_gives_the_checks_what_they_need.py#test_every_job_that_runs_pytest_has_the_whole_history`
required `fetch-depth: 0` and its failure message said, in as many words, that
*the rider stamps are what keeps this needed* — because the ledger's stamp
test had already gone when the anchors moved to content. Removing the rider
ancestry check removed the last reason the message named, leaving a live
requirement explained by a mechanism that no longer exists.

Measured before rewriting it: no pytest case resolves a `Target SHA` against
this repository's ancestry, and the one live dependency is
`tests/test_the_reopening_is_one.py#test_the_whole_check_names_no_earlier_items_record`
— it resolves `origin/release/v0.8.1` and **skips** when it cannot, which is
the same silencing shape the removed shallow-clone assertion was written
against. Observed in this phase's own run: that case reports `s`, because the
remote ref is not fetched locally. The message now names it.

**This is §12 arriving through a document rather than through code.** The
class is *a text that explains a requirement by naming a mechanism this change
removes*, and the rider test's own docstring, `seal/follow-up.md`'s cost
paragraph and this CI message were the three instances. All three were found
by asking what cited the old form, not by fixing where the failure pointed.

**Where the `Target SHA` pin lives was a decision, not a default.** It sits in
the rider test rather than beside the other round-record cases because the
ticket asked for one answer covering both mechanisms so they could not drift
into different rules — and a pin split across two files is exactly how they
would.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| `seal/follow-up.md`'s sentence *Each therefore carries the date and SHA it was verified at* | replaced in the same paragraph by the content form, and refused by `test_the_header_states_the_stamp_form_riders_actually_carry` so it cannot come back |
| the CI message's claim that the rider stamps are what needs full history | rewritten to name `test_the_whole_check_names_no_earlier_items_record`, the live dependency measured in this phase |
