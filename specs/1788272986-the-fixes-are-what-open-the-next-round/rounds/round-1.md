# 1788272986-the-fixes-are-what-open-the-next-round — review round 1

| Field | Value |
|---|---|
| Target SHA | e5e0c48 |
| PR | none yet |
| Broad gate | e2a5af6 vs origin/release/v0.3.0 (delta to e5e0c48 is one docs-only commit touching two Status cells of this item's plan.md; judged non-invalidating — no ledger anchor points there, and the seven plan-reading test files pass at HEAD, 310 passed) |
| Fixes checked by | nobody — round 1's fixes are not yet written; the verifying round sets this when it reads them |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 1 (a separator-only cell passes both fix-surface rows; one-guard fix supplied). 🟡 3 closes as a recorded limit + pin, 🟡 4 as a one-sentence prose ground; neither blocks on its own |

- [ ] Pass

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 0 | Stage 1: all eight #57 checklist items implemented; out-of-scope respected | `skills/code-review/scripts/chain_check.py:1321`, `skills/code-review/SKILL.md:59` | pass | every item read at its coordinate and both exit directions of every new refusal executed (probes below), except the two gaps reported as 🟡 1 / 🟡 3. Smith's assumptions Q1–Q3 judged sound |
| 🟡 1 | A cell of only separators (`\| ; \|`) passes both `Contract changes` and `New units` — `value.split(";")` yields empty entries, all skipped, no error; not `none`, not empty | `skills/code-review/scripts/chain_check.py:1392` | open | probe: exit 0 on a post-cutoff item, both rows; the empty-cell refusal one screen up says "a row that says nothing answers nothing" and `;` says exactly nothing. Orchestrator re-read the loop and confirms |
| 🟡 2 | Does `tests/test_gates_do_not_fail_open.py` need to cover the new refusals? | `skills/code-review/scripts/chain_check.py:400` | answered | uncoverable through that file's class: it pins the locale-decode → None → silent-allow path in hooks, and `chain_check.py`'s `git()` pins `encoding="utf-8", errors="replace"`, so the state is unconstructible here. Fact goes to the ledger (evidence-todo) |
| 🟡 3 | An ASCII arrow inside a backticked unit name (`` `operator->` ``) reads as the reach separator, so a unit listed without reach passes | `skills/code-review/scripts/chain_check.py:1396` | open | probe: exit 0. Parsing code spans to fix it would be the unbounded-domain enumeration the diff's own rule 6 refuses — closes as a RECORDED LIMIT (docstring sentence naming `→` as the spelling that avoids it) + pin per rule 8, not as a parser |
| 🟡 4 | The axes prose groups Security with Concurrency as not-settled-by-one-request-read but grounds only concurrency's exemption | `skills/code-review/SKILL.md:61` | open | the security paragraph explains table membership, not why one-path reading fails; a future prose tightening reads "the same way" as licensing a revert. One-sentence ground supplied in the report |

## Executed probes

| What was run | Result |
|---|---|
| `\| Contract changes \| ; \|` on a post-cutoff item (scratch repo) | exit 0 → 🟡 1 |
| `\| New units \| ; \|` | exit 0 → 🟡 1 |
| `\| Contract changes \| — \|` | exit 1, names the entry |
| `` `operator->` `` listed without reach | exit 0 → 🟡 3 |
| `None` (capitalised) | exit 0 — tolerant in the intended direction |
| garbage record, no tables | exit 1 — fails closed |
| targeted suites: test_the_fixes_name_their_surface + test_review_axes + test_the_last_rounds_fixes_are_checked + test_chain_check_at_the_pull_request + test_gates_do_not_fail_open + test_docs_line_wrap | 175 passed |
| seven plan.md-reading test files (broad-gate delta check) | 310 passed |
| `ruff check` on the four changed .py files | clean |
| `evidence_check.py --strict .` | 65 ok — the 7 new fragment rows resolve |
| `unverified_check.py --baseline origin/release/v0.3.0` | 18 open, none about this diff's claims |
| `gather_changelog.py --check` | lists this branch's own fragment — normal feature-branch state |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|

nothing to drain — all four findings are handed to the fixing session (smith, resumed), none deferred out of this work item.
