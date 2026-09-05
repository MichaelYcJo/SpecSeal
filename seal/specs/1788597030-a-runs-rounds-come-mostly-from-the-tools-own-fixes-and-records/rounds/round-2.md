# 1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records — review round 2

| Field | Value |
|---|---|
| Target SHA | a2d0494 |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | #168 — https://github.com/MichaelYcJo/SpecSeal/pull/168 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🟡 10, 🟡 11 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

The verifying round at `git diff c24344f..a2d0494` — **8 commits**, seven
fixes and the record's closing commit, given as a count the round re-took.

Round 1's nine verdicts as the agenda — is each actually closed at its
coordinate — and `round-1.md`'s `Contract changes` (two units, their reach)
and `New units` (nineteen entries) as the finding surface, judged as code.
Five things in order: each closed verdict at its coordinate, with the
Windows leg's run on `a2d0494` as 🔴 1's platform half and one `resolve_path`
case the fix pass did not list; the four generator units and three test
helpers narrowly, mutation included; the two contract changes' reach by
search; one coordinate the fix pass surfaced and nobody had judged — the
committed `round-1.md` reads *Fix below (A)* through *(G)* and carries no
fenced block, because `new` copies the three tables and nothing else; and
`chain_check` on the real tree at HEAD, every line for this item.

The rules named: rule 1 (a record-located finding is ⬜, not counted), rule 3
(🟡 is a defect the release would ship), the reopening is one, and the report
shape whose three tables this record copies.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The Windows leg is red: `occurrences` keys by `os.path.relpath` and the two cases compare `/`-joined paths | `tests/test_the_rules_have_one_owner.py#occurrences` | answered | executed — `gh pr checks 168` at a2d0494: windows pass 4m59s (run 33964679997), macos, ubuntu, ledger and lint pass; read — `.replace(os.sep, "/")` on the key at `:330`, and `test_the_occurrence_keys_are_slash_joined_whatever_the_separator` monkeypatches `os.sep` so the case is red against a key built from `relpath` alone |
| 🟡 2 | A record-located correction closed as `fixed <sha>` commissions a reader rule 1 says it does not owe | `docs/review-chain-spec.md#"##### The last round verifies"` and `agents/smith.md` fix-table paragraph | answered | read — the spec at `:162-165` states *closes `answered — corrected at <sha>`, never `fixed`* and `agents/smith.md:129-132` names the spec as the owner; executed — `test_a_correction_closed_answered_lands_on_no_fixes_to_check` lands the cell on `no fixes to check` and the READY check exits 0, one of 114 passed |
| 🟡 3 | `close` applies a fix-table row for a finding the reviewer already closed; the carriers disagree on whether such a row is owed | `skills/code-review/scripts/round_record.py#close` | answered | read — `close:1252-1264` refuses a row whose number is outside `open_now`, naming the finding and its verdict, before any write; the carriers agree on *one row per OPEN finding* (`agents/smith.md:124`, `skills/implement/SKILL.md:731`, `skills/code-review/SKILL.md:245`); executed — `test_a_row_for_a_finding_the_reviewer_closed_is_refused`, the `withdrawn` cell untouched |
| 🟡 4 | The depth-2 refusal is escaped by Location forms real records use; the same resolution over-refuses a same-named unit in another file | `skills/code-review/scripts/round_record.py#location_units` and `#depth_two` | answered | executed — nine parametrized forms refused, the basename resolves to `pkg/inner.py`, the same-named unit in another file closes at depth 1; `resolve_path` probed: `a/mod.py` against `xa/mod.py` plus `a/mod.py` resolves exact, against `xa/mod.py` alone resolves to None, `mod.py` against both resolves to None, so the `/`-prefixed `endswith` never crosses a directory boundary. One member of the class remains, the form this record's own finding 4 uses — 🟡 11 |
| 🟡 5 | Markdown goes through the diff-line heuristic and every record the range touches is named as read for definitions | `skills/code-review/scripts/round_record.py#measure` | answered | read — `measure:932` skips `PROSE_SUFFIXES` before any `show`; executed — `test_prose_is_neither_ast_nor_heuristic` over four suffixes; `HEURISTIC_RE` on `class: Foo`, `  class: Foo`, `def: yes`, `class = 'x'` matches nothing, so a `.yml` or `.toml` line beginning `class:` adds no entry. No prose reaches `measure` now; every non-Python non-prose file — `.toml`, `.yml`, `.sh`, `.json`, `LICENSE`, `.gif` — still reaches the heuristic and is named in the comment (⬜ 13 for the binary) |
| 🟡 6 | `reach_back` overwrites `no fixes to check` with `round-N` | `skills/code-review/scripts/round_record.py#reach_back` | answered | read — `reach_back:509-514` returns the line and writes nothing for `no fixes to check`; `nobody — …` still falls through to the write at `:522-527`; executed — `test_a_previous_record_that_commissioned_no_fixes_keeps_its_cell` (record byte-identical, the output names the value) and `test_the_previous_record_gets_its_checker_cell_and_nothing_else` (nobody to round-2), both in the 114 |
| ⬜ 7 | `New units` lists a name twice when two files add the same name | `skills/code-review/scripts/round_record.py#close` | answered | read — `dict.fromkeys` over the names at `close:1296`, and `depth_two` still walks `added` with its paths; executed — `test_the_same_name_added_in_two_files_is_one_entry` |
| ⬜ 8 | The `release` leg is red from the draft's opening until round 1's record commits, and no carrier says so | `skills/code-review/SKILL.md#"## Orchestrator: the pull request opens before round 1, and a phase is re-run"` | answered | read — the sentence at `skills/code-review/SKILL.md:586-589`, pinned by `test_the_release_leg_is_red_until_round_ones_record_commits`; executed — the leg at a2d0494 is red again, for `Pass` beside `nobody` on round-1.md after `close`, a second window the sentence does not name (⬜ 12) |
| ⬜ 9 | Ledger corrections: F1 counts three where four are excused; R4's Notes name the orchestrator; drifted rows owe a `Re-read` clause | `seal/ledger.md` F1 and R4 rows | answered | read — F1 reads *four different things*; R4's Notes carry no *orchestrator* sentence; 28 rows carry `Re-read 2026-09-05 in work item 1788597030's round 1 fix pass`, and the three opened (`main` moved by `--worktree` alone; `read_record`'s working-tree branch returns None like the HEAD read; `deferred` added to the section's list) each name what moved under the anchor; executed — `evidence_check.py .` unscoped in the clone: 569 ok, 3 drifted, 0 broken; on an export of `origin/release/v0.8.1`: 535 ok, the same 3 drifted, 0 broken |
| 🟡 10 | The record points at fixes it does not carry: `new` copies the probes table and drops the fenced blocks under it, so round-1.md reads *Fix below (A)* through *(G)* in seven Grounds cells and carries none, and the fix pass rebuilt each from a description | `skills/code-review/scripts/round_record.py#build` (`table_of` copies rows alone) | open | executed — `new` over a report with a fenced block under its probes table writes a record whose probes section holds the table alone (red at a2d0494); with `fenced_after` below the block lands between the table and `## Inherited coordinates`, the check exits 0, 74 passed across the generator's two suites, ruff clean; read — `templates/sdd-round.md:239-242` and `docs/review-chain-spec.md:1097-1100` say the row owes the block in the record, and `:1121-1125` says it stays in the report unless put in a row, which a block cannot be. Fix in one sentence: copy the fenced blocks under `## Executed probes` and nothing else of the section, from `build`, depth 1 |
| 🟡 11 | A Location of the form `path#a` and `#b` reads `a` alone: the fragment after *and* names no unit, so a fix answering a finding inside `b` that adds a unit in that file closes at depth 1 — the form round-1.md's own finding 4 uses | `skills/code-review/scripts/round_record.py#location_units` | open | executed — `two_rounds` with Location `mod.py#other` and `#helper`, fix adding `helper_guard`: closed with `helper_guard (depth 1)` at a2d0494, refused as depth 2 with `FRAGMENT_RE` below; on this record's cells the fragment reads `depth_two` and reads nothing from a heading anchor `#"##### …"`. Fix in one sentence: a fragment regex bound to the last path the cell resolved |
| ⬜ 12 | The ⬜ 8 sentence names one red window and the leg has two: it is red again from `close` ticking `Pass` until the verifying round's record commits | `skills/code-review/SKILL.md#"## Orchestrator: the pull request opens before round 1, and a phase is re-run"` | open — ⬜, not counted | executed — release leg at a2d0494 (run 33964679994): *judged as a draft pull request*, then `Pass` beside `nobody` on round-1.md, exit 1. One sentence below |
| ⬜ 13 | A binary the range touches is named in the heuristic comment as read for definitions | `skills/code-review/scripts/round_record.py#measure` | open — ⬜, not counted | executed — `measure` over the commit adding `assets/demo.gif` returns `heuristic` naming the gif, no entry, no crash; the comment then says the gif was read by the diff-line heuristic |
| ⬜ 14 | S8's anchor `templates/config.md#"# Repository config"` drifts on the base and this branch edited under it (the `deferred` word) with no `Re-read` on the row | `seal/ledger.md:517` | open — rule 1, not counted | executed — DRIFTED on both trees; read — the branch's diff of `templates/config.md` is the three-line exclusion-list edit R4's Notes describe |

## Executed probes

| What was run | Result |
|---|---|
| `git clone --no-local` at a2d0494, `uv venv`, `pytest` on `test_the_fixes_close_the_record.py`, `test_the_record_is_generated.py`, `test_the_rules_have_one_owner.py` | 114 passed; `uvx ruff check` on the generator and the three test files exit 0 |
| `git log --oneline c24344f..a2d0494` | 8 commits, seven fixes and the record's closing commit, the count re-taken |
| `gh pr checks 168`, `gh pr view 168 --json headRefOid,isDraft` | headRefOid a2d0494, draft; release fail 9s, windows pass 4m59s, macos pass, ubuntu pass, ledger pass, lint pass |
| `gh run view 33964679994 --log-failed` (the release leg) | `judged as a draft pull request`, then `Pass` is checked beside `Fixes checked by: nobody — the fixes are not yet written` on round-1.md, exit 1 |
| `chain_check.py --baseline origin/release/v0.8.1` on the real tree at HEAD a2d0494, HEAD read | exit 1: `judged as a ready pull request (no pull-request event payload)`; the item is `through the review chain — 1 round record(s), last is round-1.md`; `round-1.md:0  Pass is checked beside Fixes checked by: nobody — …` with the way-out sentence naming the verifying round |
| the same with `--worktree` | exit 1, the same three lines after `reading the working tree (--worktree)` |
| `evidence_check.py .` unscoped in the clone, and on a `git archive` export of `origin/release/v0.8.1` | clone: 569 ok, 3 drifted (`hooks/dispatch.py#run_gate`, `.github/scripts/fold_ledger.py#demote`, `templates/config.md#"# Repository config"`), 0 broken; base: 535 ok, the same 3 drifted, 0 broken |
| `grep -o 'Re-read 2026-09-05 in …'` over `seal/ledger.md` | 28 rows name work item 1788597030's round 1 fix pass; the other four are the last item's |
| `resolve_path` on `a/mod.py`, `mod.py`, `./a/mod.py`, `inner.py`, `chain_check.py`, `b/mod.py` against a tracked set holding `a/mod.py`, `xa/mod.py`, `pkg/inner.py`, `mod.py`; `a/mod.py` against `xa/mod.py` alone; `mod.py` against `xa/mod.py` and `a/mod.py` | exact, exact, `a/mod.py`, `pkg/inner.py`, `skills/code-review/scripts/chain_check.py`, None; None; None |
| `location_units` on six Location cells of round-1.md against `HEAD`'s tree | the `path#unit` cells resolve to their full path; `path#a` and `#b` yields `a` alone; the heading-anchor and ledger cells yield nothing; `helper()` yields `helper` with no file |
| `HEURISTIC_RE` on `+class: Foo`, `+  class: Foo`, `+class = 'x'`, `+function_name = 1`, `+def x`, `+fn main() {`, `+[def]`, `+def: yes` | matches `x` and `main` only |
| `measure` over the commit adding `assets/demo.gif` | `changed` and `added` empty, `heuristic` names the gif, no exception |
| `grep` for `reach_back`, `location_units`, `depth_two(`, `PROSE_SUFFIXES`, `HEURISTIC_RE`, `tracked_at`, `resolve_path`, `BARE_IDENTIFIER_RE` over `skills tests agents docs templates` | one caller each: `new:678` and `depth_two:1176`; no test calls either directly |
| `test_tmp_round2_probe.py` in the clone: a report with a fenced block under the probes table through `new`; `two_rounds` with Location `mod.py#other` and `#helper` through `close` | at a2d0494: 2 failed — the record's probes section holds the table alone; `close` closed with `helper_guard (depth 1)`. With the diff below applied in the clone: 2 passed; the two generator suites 74 passed; `ruff check` and `ruff format --check` exit 0; `FRAGMENT_RE` on the real cells reads `depth_two` after `location_units` and nothing from `#"##### …"`, `#168`; clone reverted, probe deleted, `git status` clean |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|
| round-1 | `tests/test_the_rules_have_one_owner.py#occurrences` | round 1's 🔴 1 — fixed |
| round-1 | `docs/review-chain-spec.md#"##### The last round verifies"` and `agents/smith.md` fix-table paragraph | round 1's 🟡 2 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#close` | round 1's 🟡 3 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#location_units` and `#depth_two` | round 1's 🟡 4 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#measure` | round 1's 🟡 5 — fixed |
| round-1 | `skills/code-review/scripts/round_record.py#reach_back` | round 1's 🟡 6 — fixed |
| round-1 | `skills/code-review/SKILL.md#"## Orchestrator: the pull request opens before round 1, and a phase is re-run"` | round 1's ⬜ 8 — fixed |
| round-1 | `seal/ledger.md` F1 and R4 rows | round 1's ⬜ 9 — fixed |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| The full suite, repository-wide lint and typecheck (`Broad gate` stays `not yet`; this round opens fixes, so the gate is not yet due) | the broad gate, once after the rounds settle (§2) | the orchestrator |
| ⬜ 14 — S8's anchor drifts on the base and the branch edited under it | the three base drifts are re-stamped where base drifts are, at the release-preparation commit; the branch's own edit under S8 is named there | the release preparer |
| ⬜ 13 — a binary named in the heuristic comment | fixed in passing in the same fix pass or not at all (rule 3) | the fix pass, optional |
| `fenced_after`'s unclosed-fence refusal has no case here — the probe covered the closed block only | a case seen red in the fix pass that plants it (§15) | the fix pass |
| A5 and the spec paragraph at `:1121-1125` say the block stays in the report | corrected in the closing commit beside the fix (rule 1) | the fix pass |
