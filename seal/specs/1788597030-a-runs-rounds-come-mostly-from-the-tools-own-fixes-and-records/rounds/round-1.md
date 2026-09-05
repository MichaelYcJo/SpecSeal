# 1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records — review round 1

| Field | Value |
|---|---|
| Target SHA | f86e977 |
| Ran by | specseal:warden on claude-fable-5-1 |
| PR | #168 — https://github.com/MichaelYcJo/SpecSeal/pull/168 |
| Broad gate | not yet |
| Fixes checked by | nobody — the fixes are not yet written |
| Contract changes | none — the fixes are not yet written |
| New units | none — the fixes are not yet written |
| Needs a fix | yes — 🔴 1, 🟡 2, 🟡 3, 🟡 4, 🟡 5, 🟡 6 |
| Loses a record or crashes | no |

- [ ] Pass

## What this round was asked

Round 1 at `git diff origin/release/v0.8.1..f86e977` — **25 commits**, given
as a count the round re-takes. The branch is the machine #161 asked for, so
the target is the machine on its own first use, in this order:

1. `round_record.py new` against a report in the shape `agents/warden.md`
   §Report now prescribes — in a `--no-local` clone of this branch, with a
   report the round writes itself: does the record it produces pass
   `chain_check` as a first record, and does a second `new` set the first
   record's `Fixes checked by`.
2. `round_record.py close` over this branch's own ranges — `132494f..2b55606`
   (phase 2) and `f37b64c..ec2dfb5` (phase 4a, docs only): does `New units`
   name what `git diff` shows added and nothing else, does `Contract changes`
   name `chain_check.main`'s new flag with its reach, and does a docs-only
   range read `none`.
3. The depth-2 refusal — every `Location` form the spec names (`path#unit`,
   `path#unit@hash`, `path:line`, a backticked identifier) against a record
   whose `New units` names the parent; and the form that escapes it, if one
   does.
4. The reopening walk against the last item's fifteen records
   (`seal/specs/1788501054-…/rounds/`), which begin before `REOPEN_FROM`: it
   must print, never fail; and against a three-record fixture on or after the
   cutoff: the second fix-closing record refused by file.
5. `verdict_of` on `deferred` — the spellings the normaliser folds and the
   ones it does not; whether a bare `**deferred**` is open.
6. `--worktree` from a linked worktree, and with an untracked `round-N.md`.
7. The nine rules across their owners and links: any two carriers that
   disagree, and any sentence the *Unless* removal left stranded (`grep` for
   *third case*, *runs away*, *cannot loop*, *Unless th*).
8. The sixteen drifted `seal/ledger.md` rows (`evidence_check.py .`
   unscoped): for each, is the claim still true of the content under the
   anchor now. A table in the report — row, still true or not, what changed —
   so the fix pass re-stamps each with a `Re-read` clause; a false claim is a
   finding.
9. The draft pull request's platform legs (`gh pr checks`): report each leg's
   state; a red Windows leg is a finding with the log's coordinate.
10. `overview.md`'s three divergences: judged on their grounds.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🔴 1 | The Windows leg is red: `occurrences` keys by `os.path.relpath` and the two cases compare `/`-joined paths | `tests/test_the_rules_have_one_owner.py#occurrences` | open | executed — PR #168 run 33962446559 job 101296562555, `2 failed, 2211 passed`, both failures in this file; green on macOS and ubuntu. Fix below (A) |
| 🟡 2 | A record-located correction closed as `fixed <sha>` commissions a reader rule 1 says it does not owe | `docs/review-chain-spec.md#"##### The last round verifies"` and `agents/smith.md` fix-table paragraph | open | executed — P4c: `fixed` leaves `nobody — the fixes are not yet written` beside a checked `Pass` and a READY check exits 1; `answered`/`deferred #N` land on `no fixes to check` and exit 0. Fix below (B) |
| 🟡 3 | `close` applies a fix-table row for a finding the reviewer already closed, overwriting the reviewer's verdict; the carriers disagree on whether such a row is owed | `skills/code-review/scripts/round_record.py#close` | open | read — `:1187-1233` applies every row in `fixes`; `agents/smith.md` and `skills/implement/SKILL.md` §5 say one row per finding, the skill says per open finding. Fix below (C) |
| 🟡 4 | The depth-2 refusal is escaped by Location forms real records use — a basename `path#unit`, `./path#unit`, a backticked `name()`, a bare name, `path::unit` — and writes depth 1 for a depth-2 unit; the same resolution over-refuses a same-named unit in another file | `skills/code-review/scripts/round_record.py#location_units` and `#depth_two` | open | executed — P3: the spec's four forms refused with exit 2 and no cell written; the five above closed with `helper_guard (depth 1)`; the last item's records carry `` `chain_check.py#fix_surface` ``. Fix below (D) |
| 🟡 5 | Markdown goes through the diff-line heuristic: a prose line beginning `class`/`def`/`function` becomes a `New units` entry, and every record and doc the range touches is named as read for definitions | `skills/code-review/scripts/round_record.py#measure` | open | comment executed (P2a, P2b name five and six `.md` files); phantom read — 13 such lines exist in the tree (`docs/review-handoff-protocol.md:274`, the last item's `rounds/round-7.md:117`), none in this branch's diff. Fix below (E) |
| 🟡 6 | `reach_back` overwrites `no fixes to check` with `round-N`, so a record that commissioned no fixes says a later round read them | `skills/code-review/scripts/round_record.py#reach_back` | open | executed — P4d: a round 1 of only `withdrawn` verdicts read `no fixes to check`; `new --round 2` set it to `round-2` and the check said nothing. Fix below (F) |
| ⬜ 7 | `New units` lists a name twice when two files add the same name | `skills/code-review/scripts/round_record.py#close` | open | executed — P2a: `fix_table (depth 1)` and `close (depth 1)` twice over `132494f..2b55606`; behaviour right, reads badly. Dedupe at `:1214` |
| ⬜ 8 | The `release` leg is red from the draft's opening until round 1's record commits, and no carrier says so | `skills/code-review/SKILL.md#"## Orchestrator: the pull request opens before round 1, and a phase is re-run"` | open | executed — PR #168 `release` leg: judged as a draft, then `rounds/ holds no round-N.md`, exit 1. One sentence below (G) |
| ⬜ 9 | Ledger corrections: F1 counts three excused things where the reopening arm makes four; R4's Notes still say the orchestrator writes the round record; nineteen drifted rows owe a `Re-read` clause | `seal/ledger.md` F1 and R4 rows | open | read — the table above; a correction under rule 1, not counted |

## Executed probes

| What was run | Result |
|---|---|
| `round_record.py new --round 1 --target f86e977` in the `--no-local` clone, warden-shaped report with a 🟡 and a ⬜ row | exit 0; every field row derived; `chain_check --worktree` with a draft payload exit 0, without a payload exit 1 (judged ready); committed record passes the HEAD read with a draft payload |
| `round_record.py close --round 1 --range 132494f..2b55606`, table `fixed d2b51df` and `answered` | exit 1 from the check (`Pass` beside `nobody`, the documented verifying-round exit); `Contract changes` none; `New units` 76 entries equal to an independent AST diff of the range's `.py` files; five `.md` files named in the heuristic comment |
| `round_record.py new --round 2` after the close | exit 0; round-1's `Fixes checked by` set to `round-2`; two inherited coordinates carried with their verdict words; `--pr` copied verbatim |
| `round_record.py close --round 2 --range f37b64c..ec2dfb5`, `fixed d3e2862` | 28 `New units` from `tests/test_the_rules_have_one_owner.py`, not `none`: the range is not docs-only; `Contract changes` none |
| `measure()` over `4cfb1ef^..4cfb1ef`, `0946350..132494f`, `2b55606..f37b64c` | docs-only commit measures to `none`; phase 1 adds `WORKTREE` and `worktree_files` with no contract change (`main`'s signature unchanged); phase 3 adds the five `chain_check` constants |
| Depth-2 fixtures, ten Location forms, `round-1.md` naming `helper (depth 1)`, range adding `helper_guard` | refused with exit 2 and the record unchanged: `mod.py#helper`, `mod.py#helper@deadbeef`, `mod.py:5`, `` `helper` ``, prose around `mod.py#helper`; closed with `helper_guard (depth 1)`: nested basename, `./mod.py#helper`, `` `helper()` ``, bare `helper`, `mod.py::helper` |
| `stopping_floor` on the last item's fifteen records, real repository, HEAD read | 0 errors, 12 notices, each naming the second fix-closing record and ending in prints instead of failing |
| Three-record fixtures at `1788597030-…` and `1788597029-…`, rounds 2 and 3 closing on a fix after a floor record | at the cutoff: error naming `round-3.md` after `round-2.md` with the `capped` exit; a second before: the same message as a notice |
| A ⬜ correction row closed as `fixed`, `answered`, `deferred #170` after a floor record, READY payload | `fixed`: cell stays `nobody`, `Pass` ticked, exit 1; `answered` and `deferred`: `no fixes to check`, exit 0 |
| `new --round 2` over a round-1 whose cell read `no fixes to check` | the cell became `round-2`; the check printed nothing about it |
| `verdict_of` on 24 `deferred` spellings | ten closed, six `deferred (no home)`, four unreadable and open (`deferred: #170`, `deferred(#170)`, `deferred#170`, `defered #170`); none a fix word |
| `git worktree add` at `f86e977`, `new` inside it, `chain_check --worktree --root <wt>` and without the flag | `new` exit 0 writing an untracked record; with the flag exit 0; without it exit 1 `holds no round-N.md` |
| `.venv/bin/python -m pytest` on the four new test files plus `test_the_run_stops_at_the_last_finding.py`, `test_the_last_rounds_fixes_are_checked.py`, `test_the_record_is_held_to_the_floor_and_the_depth.py` | 286 passed, exit 0 |
| pytest on the 13 pin modules of the drifted ledger rows | 341 passed, exit 0 |
| `uvx ruff check` on the six changed Python files and `ruff format --check` on the two scripts | exit 0 both |
| `evidence_check.py .` unscoped, READ form | exit 1, `553 ok · 19 drifted · 0 broken`; the table above |
| `chain_check.py --baseline origin/release/v0.8.1` on the real tree, with and without `--worktree` | exit 1 both: no round record yet, judged as ready outside a workflow |
| `gh pr view --json number,url,isDraft` in the real repository, read-only | `{"isDraft":true,"number":168,"url":"https://github.com/MichaelYcJo/SpecSeal/pull/168"}` — the shape `pull_request_cell` parses |
| `gh pr checks 168`, `gh run view --log-failed` on the Windows job | release fail, windows fail (two `occurrences` cases), ledger, lint, macos, ubuntu pass |

## Inherited coordinates

| From | Coordinate | Why it is still worth opening |
|---|---|---|

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `templates/sdd-round.md`'s severity comment under the verdicts table reads without ⬜ | `overview.md` §Not done — left ⬜ by phase 4a, fixed in passing or not at all | nobody |
| The full suite, repository-wide lint and typecheck | the broad gate, once after the rounds settle (§2) | the orchestrator |
| Whether the orchestrator re-ran each phase's suite before the next (rule 9's claim about this branch) | nothing in the tree records it; `overview.md` says the same | the orchestrator |
| A machine without `gh` tells the check draft for every local `new`, the quiet direction `pull_request_state`'s docstring names | a limit to record in `run_check`'s docstring; CI re-judges from the real payload | the fix pass, one sentence |
