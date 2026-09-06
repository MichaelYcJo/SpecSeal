# 1788661274-the-roll-names-the-next-version-by-guessing — review round 1

| Field | Value |
|---|---|
| Target SHA | 2ca226b |
| Ran by | specseal:warden on claude-opus-5 |
| PR | 178 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | close_issue → main, ledger.md, pytest; test_one_open_issue_after_the_retry_succeeds → no call site found |
| New units | TITLE_PREFIX (depth 1); test_a_title_the_roll_did_not_write_names_no_version (depth 1); test_the_close_comment_names_the_version_this_release_shipped (depth 1); test_the_tracker_doc_states_the_whole_prefix_the_roll_requires (depth 1) |
| Needs a fix | yes |
| Loses a record or crashes | no |

- [x] Pass

## What this round was asked

Round 1, the finding round, against `2ca226b` with base `cc0a2c6`. Eight things
to attack, in order: the condition's correctness at the boundary (a re-run, a
revert, a version moving backwards, two releases in one push, a tag with no
version move); `rolled_from`'s parse against six malformed titles, with the note
that phase 1 had already had two mutations survive there and the instruction to
find the third; whether *always roll* on an unreadable title is the safe
direction or produces a log that churns; whether `next_version` truly has no
caller left anywhere rather than in `seal/` alone; whether the two printed lines
distinguish *correctly quiet* from *the condition is broken*; the `spec.md`
divergence and whether leaving the spec unedited is the right record; the six
re-stamped ledger rows including one in a merged work item's fragment; and what
would fail against real GitHub, since every case fakes `subprocess.run`.

The unscoped ledger read was named as the form to run, with this branch offered
as the demonstration: the handoff to its own last phase predicted one drifted
row and the unscoped read found eight.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | `rolled_from` matches `TITLE_MARKER` anywhere in the title, so a title the roll never wrote can answer *not due* and stall the log with the workflow green | `.github/scripts/roll_flow_measurement_issue.py#rolled_from` | **fixed** `93f034b` | fixed at 93f034b — `` — `TITLE_PREFIX` holds the whole of what `log_title` writes and `rolled_from` matches it with `startswith`, so the reader is exactly as wide as the writer. **The class was enumerated by decomposing the artefact rather than by listing titles**: `log_title` composes three segments — what precedes the marker, the marker, the version — and every writer/reader gap must live in one of them because there is nowhere else in the string. G2 had enumerated the third segment and both its members and never looked at the first, which is why a class it called closed had another member. `startswith(TITLE_PREFIX)` closes all three at once. Outside this module the class has no instance: `rolled_from` is the only reader of a composed title in the repository and `log_title` its only writer; executed: `rolled_from("docs: explain flow measurement — after 0.8.2")` → `"0.8.2"`, `roll_is_due(…, "0.8.2")` → `False`. The writer prefixes `chore: `, the reader does not check it. G2's class has a third instance the row does not enumerate, and it falls in the one direction the design says must be unreachable. Fix executed, 55 passed |
| 🟡 2 | `close_issue`'s posted comment still says the new log opens *for the version this release ships next*, which is the convention this change removed | `.github/scripts/roll_flow_measurement_issue.py#close_issue` | **fixed** `93f034b` | fixed at 93f034b — `` — `close_issue` takes the shipped version and derives its successor's title from `log_title`, so the comment cannot silently restate the removed convention. Pinned by `test_the_close_comment_names_the_version_this_release_shipped`, which had no counterpart before; `issue_body` was rewritten for the same reason and pinned; this class-mate was not touched and no case reads the `--comment` argument. Shipped person-facing text naming the wrong version relative to the title a reader will see |
| ⬜ 3 | `.strip()` in `rolled_from` is unpinned — the mutation removing it survives all 55 cases, before and after finding 1's fix | `.github/scripts/roll_flow_measurement_issue.py#rolled_from` | **fixed** `93f034b` | fixed at 93f034b — `` — the missing `.strip()` case, pinned inside `test_rolled_from_reads_only_the_title_the_roll_itself_writes`; executed mutation run. The behavioural cost is one roll that was not owed, which is the chosen safe direction, so this is the missing case rather than a shipped defect. Phase 1 killed two mutations here; this is the third |
| ⬜ 4 | The `if not marker: return None` guard is unreachable in effect — `partition` already yields `''` for an absent separator | `.github/scripts/roll_flow_measurement_issue.py#rolled_from` | **fixed** `93f034b` | fixed at 93f034b — `` — finding 1's fix makes the guard real: deleting it now fails `test_a_title_the_roll_did_not_write_names_no_version`. No case was written for the old unreachable form; executed: deleting the guard leaves 55 passed. Finding 1's fix makes it a real guard |
| ⬜ 5 | `partition` vs `rpartition` is unpinned; a title carrying the marker twice | `.github/scripts/roll_flow_measurement_issue.py#rolled_from` | answered | finding 1's fix removes `partition` entirely, so `partition` against `rpartition` has no subject left. The marker-twice title is covered instead by an assertion that the answer is not a shippable version |
| ⬜ 6 | The `nothing due:` line names its conclusion and never the title it parsed, which is the one input to the decision | `.github/scripts/roll_flow_measurement_issue.py#main` | **fixed** `93f034b` | fixed at 93f034b — `` — the `nothing due:` line names the log's title, so a coincidental match is visible in a workflow log; both lines meet the *tell them apart* requirement. Naming the title makes finding 1's shape visible in a workflow log |
| ⬜ 7 | The tracker document's rule — *a title with no `after` in it* — is looser than the marker the code requires | `docs/issues-and-milestones.md#"### `flow-measurement` is a label that is not an index"` | **fixed** `93f034b` | fixed at 93f034b — `` — `docs/issues-and-milestones.md` states the whole prefix the code requires rather than *a title with no `after` in it*; `flow measurement — after ` is the whole marker; a hand-written title with `after` and a hyphen also answers `None`. This is where a person copies a recovery title from |
| ⬜ 8 | A test replaces `time.sleep` on the real stdlib module with no restore, so later `monkeypatch` restores to the leaked lambda | `tests/test_a_release_rolls_the_flow_measurement_issue.py` | **fixed** `93f034b` | fixed at 93f034b — `` — fixed here rather than deferred: one function, already changed by this diff, and the fix is a `monkeypatch.setattr` in place of a bare assignment. Demonstrated by measurement: `time.sleep` is a leaked lambda after the module runs at `253ac8c` and the built-in after the fix; read at `cc0a2c6`: pre-existing, both lines. In scope because this diff changed the enclosing function |
| ⬜ 9 | `spec.md` quotes the owner's half 2 without *"name the NEXT version by the same arithmetic the release actually used"* — the clause the build went against | `seal/specs/1788661274-the-roll-names-the-next-version-by-guessing/spec.md` | answered | corrected at `6a56361` — `spec.md` now quotes the owner's half 2 whole, including *name the NEXT version by the same arithmetic the release actually used*, and records that the work item went the other way with the issue's own delegation as grounds |
| ⬜ 10 | Equality reads a version moving backwards as due, reopening the duplicate-title symptom #155 reports | `.github/scripts/roll_flow_measurement_issue.py#roll_is_due` | answered | ordering is rejected in ledger row G1 on grounds I checked and agree with: it is what would leave an old `0.9.0` title never due once `0.9.0` ships. Cost is one roll that was not owed |
| ⬜ 11 | `next_version` has no remaining caller anywhere — workflow, docs, tests, scripts | `.github/scripts/roll_flow_measurement_issue.py` | answered | confirmed first-hand by `grep -rn next_version` over the tree, not `seal/` alone: only records |
| ⬜ 12 | The six re-stamped ledger rows, and touching a merged work item's fragment | `seal/ledger.md` | answered | every coordinate opened at `2ca226b`; each claim rests on a unit that did not drift. Re-stamping the merged fragment's row was necessary — that anchor is the skill section this branch edited |
| ⬜ 13 | The `spec.md` acceptance-scenario divergence, handed to the review chain | `seal/specs/1788661274-the-roll-names-the-next-version-by-guessing/overview.md` | answered | accepted. The built behaviour is right, and leaving the spec unedited with both texts recorded is the correct way to keep the delegated decision visible |

## Executed probes

| What was run | Result |
|---|---|
| the roll's module and the flow-log module in a `git clone --no-local` at `2ca226b`, uv venv | 55 passed, exit 0 |
| `evidence_check.py .` unscoped at `2ca226b` in the clone | exit 1, 661 ok · 1 drifted · 0 broken |
| the same, at `cc0a2c6` in the clone | 642 ok · 1 drifted, the same row — the drift is pre-existing, confirmed rather than carried |
| five mutations of the script, each run against both modules | `.strip()` removed → SURVIVED · `if not marker` guard removed → SURVIVED · `partition`→`rpartition` → SURVIVED · `main`'s not-due guard removed → killed (3 failed) · `TITLE_MARKER` trailing space removed → killed (4 failed) |
| `rolled_from` called directly on eight boundary titles at `2ca226b` | the prose title → `'0.8.2'`, not due · hyphen-for-em-dash → `None` · trailing space → `'0.8.2'` · `-rc1` suffix → kept · marker twice → the whole tail · marker with nothing after → `None` · uppercase → `None` |
| finding 1's fix applied to the clone, both modules re-run | 55 passed, exit 0; the prose title then answers `None`. The `.strip()` mutation still survives on top of it |
| `gh issue list` for both labels, `gh label list`, the milestones — reads only | one open log, one open baseline, both label and milestone present |
| probe files and the clone deleted | all removed |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The full suite, the repository-wide lint, the typecheck | `overview.md` §Not verified — contract §2 keeps them out of a round | the orchestrator, at the broad gate after the rounds settle |
| The roll against real GitHub. Every case fakes `subprocess.run`; the four `gh` call sites were read against live tracker state and no failure is predicted beyond finding 2's text, but nothing was executed against it | `overview.md` §Not verified | the 0.8.2 release, which is the first live run |
