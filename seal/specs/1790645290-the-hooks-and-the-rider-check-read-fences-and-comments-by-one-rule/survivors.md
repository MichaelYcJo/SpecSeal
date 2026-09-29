# Survivors — the hooks and the rider check read fences and comments by one rule

The sweep after phase 5 (`survivor-check --range origin/release/v0.16.0...HEAD`,
which resolved to `66b34a4..34135c7`) reported nine places. None presents the
removed wording as the tree's state now: two are the closed work item B's own
record of where it left the routing reader and the rider check, and seven quote
the fallback test command as it stood in the moment they record.

| Path | Quote | Grounds |
|---|---|---|
| `seal/specs/1790635413-every-markdown-reader-shares-one-fence-rule/overview.md` | A new work item redoes them from a clean frame, and #658 stays open for its routing half. | work item B's closing memo, recording where B left the two readers when it closed; this work item is the one it names, and a record of that moment is not a statement about the tree now |
| `seal/specs/1790635413-every-markdown-reader-shares-one-fence-rule/overview.md` | The config reader's comment-before-fence reading, which the routing reader and the rider check had both taken on, reopened a finding in every round: | the same memo, recording why B's rounds ended as they did; still true of B |
| `.github/scripts/run_tests.py` | `CONTRIBUTING.md` already named a command -- `uvx --with pytest python3 -m pytest tests/ -q` -- so nothing was missing. | the module docstring's account of #156, which is about what the section said when that issue was opened; history, and true of that day |
| `tests/test_the_suite_has_a_command_that_is_cheap_twice.py` | that half is wrong -- `CONTRIBUTING.md` §*Running the checks* named `uvx --with pytest python3 -m pytest tests/ -q`. | the same account of #156 in the case module's docstring; history |
| `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/plan.md` | - Tests are run narrowly with `uvx --with pytest python3 -m pytest tests/<file> -q` (`CONTRIBUTING.md`). | a shipped work item's plan, recording the command its own phases ran |
| `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/plan.md` | `uvx --with pytest python3 -m pytest tests/test_a_record_precedes_the_fixes_it_commissions.py -q`. | the same plan's Verified-by cell, the command that phase ran |
| `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/plan.md` | `uvx --with pytest python3 -m pytest tests/test_chain_check_at_the_pull_request.py tests/test_a_record_precedes_the_fixes_it_commissions.py tests/test_docs_line_wrap.py tests/test_a_folded_statement_names_what_enforces_it.py -q` | the same plan's Verified-by cell |
| `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/plan.md` | `uvx --with pytest python3 -m pytest tests/test_the_last_rounds_fixes_are_checked.py tests/test_the_rules_have_one_owner.py tests/test_the_fixes_close_the_record.py tests/test_docs_line_wrap.py tests/test_a_folded_statement_names_what_enforces_it.py -q` | the same plan's Verified-by cell |
| `seal/specs/1790297083-the-release-job-goes-red-on-a-record-it-need-not-judge/plan.md` | `uvx --with pytest python3 -m pytest tests/test_a_row_points_by_content.py -q` | the same plan's Verified-by cell |
