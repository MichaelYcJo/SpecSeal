# Open questions — 1788844127-the-reviewers-report-reaches-the-record-retyped

The routing batch was answered before this work item was spawned, and the
design direction came with it. Nothing here blocked the build; each row was
decided in writing and continued, per `skills/implement/SKILL.md` §1.

| # | Question | What was assumed, and why | Who must answer |
|---|---|---|---|
| Q1 | Which checkout does the reviewer write `round-<n>-report.md` in — the clone it reviews from, or the repository under review? The handoff said *"under the work item"* and did not name the tree, and `agents/warden.md:29-34` says the reviewer works in a clone *"and only there"* | **Assumed: the repository under review**, with a named exception added to `agents/warden.md`. The clone's lifetime is written down nowhere, so a path into it is a file the next segment may not be able to open — the ticket's own failure shape. `plan.md` §*Alternatives considered* carries both readings and what each costs | the orchestrator |
| Q2 | `--asked` has the same defect as `--report` had: it is a required path to a file that exists as prose in a spawn prompt, and the orchestrator types it out. The tests already name `round-N-asked.md` as a convention, and no shipped document does | **Assumed out of scope**, because the ticket is about the report and the round paragraph is the orchestrator's own text rather than another agent's — retyping your own prompt loses nothing. Worth an issue rather than a widening here | the orchestrator |
| Q3 | `round-N-asked.md` and `round-N-fixes.md` are named in `tests/test_the_reopening_is_one.py:428`, `tests/test_chain_check_at_the_pull_request.py:1294` and `CHANGELOG.md`, and in **no** shipped document — not `agents/`, not `skills/`, not `docs/`, not `templates/`. Executed: `grep -rn 'asked\.md\|fixes\.md' agents/ skills/ docs/ templates/ CONTRIBUTING.md` returns nothing. So this change documents the report's name while its two siblings stay conventions that live only in test comments | **Assumed out of scope.** Naming them is a documentation pass over files this ticket does not otherwise touch | the orchestrator |
