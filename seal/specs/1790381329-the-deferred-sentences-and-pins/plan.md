# Implementation Plan: the deferred sentences and pins (#610, #611, #612, #613, #615, #616)

<!-- seal/specs/1790381329-the-deferred-sentences-and-pins/plan.md — HOW, in phases. This is the Design Gate's
artifact: where the work alters observable behaviour, approval of this plan is
the gate. -->

Approved 2026-09-26 by the orchestrating session, under the owner's `automation` answer, when `smith` was spawned.

## Summary

Six deferred items, one branch, one phase each, in an order that puts the one
behaviour change first and the prose after it. Each item is fixed as a class
rather than at the coordinate its issue quotes, and each carries a pin built
on the finding's own example. `spec.md` holds the scope, the enumerated places
and the acceptance rows; this file holds the order and the method.

## Technical context

**Every paste-ready text was checked against the tree this frame read
(2c869ebc).** All six still apply, with these differences, which the builder
uses instead of the issue:

| Issue | What changed since the round |
|---|---|
| #610 | nothing. `seal.py` still loads through `sys.path.insert` + `import` at module top; `payload_meter.py#_session_cost` still loads by path with no file check |
| #611 | nothing. The skill's sentence, `BASE` and the target case are as the round quoted them |
| #612 | the issue lists seven places; the tree has eleven, plus two test docstrings (spec.md's #612 table). `docs/one-root-by-lifetime.md` and its Korean edition are false, not only incomplete: *never the base branch's moving tip* |
| #613 | the issue says two ledger rows anchor on `fix_surface`; seven do, all `@dd0a5d68`, across `seal/releases/0.4.0.md`, `0.8.0.md` and `0.15.0.md` |
| #615 | the spec sentence moved from line 926 to 932; the paste-ready bounds still match. The count the round measured (280 of 800) is re-taken at the build tip |
| #616 | the paste-ready case applies. Two twins the issue did not name: `as_cmd_expands` says *`CD` and `__CD__` are in no environment*, which the new case makes false, and `templates/config.md` §*Broad gate* claims the same equality with `cmd.exe`, pinned verbatim by the reader case |

**The method 0.15.4 paid for, and why it is written into every phase.** All
five 0.15.4 items spent their one reopening because a one-phrasing grep missed
a twin. So every sentence-class phase starts by repeating the frame's
enumeration at the build tip, by meaning, in English and Korean, over
`docs/ skills/ templates/ agents/ hooks/ .github/ README.md README.ko.md
CONTRIBUTING.md` — not only over the files spec.md lists, because the tree can
have moved and the frame can have missed one. Each phase's record says which
phrasings were searched and what each hit was judged to be. A hit judged not a
twin is listed with its grounds, the way spec.md's *Out of scope* does.

**The pin is the finding's own example.** `%CD%` for #616, not a generic
variable; the split `R1` row for #615; the exact false sentence for #612;
the two scripts themselves for #610. Each new case is seen red before it is
committed (contract §15): against the unfixed code, or with the sentence it
pins deleted, and the phase record says which.

**Failure scenario of the chosen approach, six months out.** A seventh
phrasing of one of these sentences, written after this branch, reintroduces
the error, and nothing but the positive assertions here would notice. The
pins cover the files that exist today; `survivor-check` covers some of the
rest by wording similarity, and #613 is the measured case where it could not
(the wording differed enough to fall under its floor).

## Alternatives considered

| Approach | Failure scenario | Verdict |
|---|---|---|
| #610: keep exit 1 for `payload_meter.py`, as #590's frame did, because its 1 means "could not measure" | a lone copy exits 1, which reads as "this transcript could not be calibrated from" and sends the reader to the transcript; the script already uses 2 for the other "nothing ran" case (the interpreter floor) | rejected: 2, on the script's own convention |
| #610: keep `seal.py`'s "no third exit code" and exit 1 with a sentence | `seal.py` becomes the one shipped command outside #590's class, and the next frame that enumerates the class finds it again | rejected: 2, and the docstring's exit line is rewritten in the same commit |
| #612: say only "the base's tip" everywhere | false for the local run and the broad gate, which run on a branch checkout, where the fork point is what keeps a sibling's squash from reading as a removal | rejected: both places, with the either-way conclusion |
| #612: assert the old phrase absent in every file | the old wording has several phrasings, and a negative assertion of one passes while a second survives — the failure 0.15.4 measured | rejected as the only pin: a positive phrase per file, plus the one false sentence's absence where it stands today |
| #613: add a case pinning the docstring | a docstring is not a message, verdict or rendered line (contract §14's list), and the rule's behaviour is already pinned by the draft/ready cases | rejected: the docstring is corrected and the seven rows re-read; no new case |
| #615: pin S4, the one truly silent shape, as exit 0 | locks a known false negative in; the day someone pairs removed and added lines, the case goes red for a fix | rejected |
| #616: also probe where `cmd.exe` resumes after an undefined name, on the Windows CI leg | adds a Windows-only case whose first run is at the pull request, in an unattended run, for a question the docstring can leave open truthfully | rejected for this work item: recorded in `overview.md` `## Not verified` with its answerer (questions.md Q2) |
| Six branches, one per issue | six review chains and six squashes for six sentences | rejected by the milestone, which scheduled C as one branch |

## Phases

Commit at the end of every phase at least; commit earlier where a step stands
on its own. Each phase runs only the narrow cases it touched (the named test
file, `-k` where it is large), and `evidence-check` after its edits to find
the ledger rows it drifted. None runs the broad gate: that is the sealer's.

| Phase | Delivers | Verified by | Status |
|---|---|---|---|
| 1 | **#610.** `seal.py` checks for `hooks/config.py` and `hooks/optin.py` before its `import` lines and exits 2 with one sentence per missing file, naming the path and its purpose (reuse the phrases `settle.py#load` and `fold_check.py` already use for `optin.py`: *it is what finds the repository's seal/ root*). `payload_meter.py#_session_cost` checks for `session_cost.py` and exits 2 the same way; how it reaches `main`'s exit (a raise `main` catches, or `SystemExit(2)` after the sentence) is the builder's, matching the file's existing floor refusal. `seal.py`'s exit-code line and `payload_meter.py`'s docstring name the new code. Two `CASES` rows; the test module's docstring and the `CASES` comment say six scripts and both loader shapes (`by file path` and `sys.path.insert` + `import`). Invocations: one argparse accepts, because argparse's usage error is also exit 2 | `tests/test_a_script_copied_alone_exits_2.py`, both new rows seen red first (exit 1, traceback) | 31ccd45d |
| 2 | **#611.** The round's paste-ready sentence in `skills/settle/SKILL.md` §1. The second wording asserted beside the first in `test_the_documents_say_the_closure_has_to_reach_the_base`; the round's summary-line assertion in `test_the_report_does_not_promise_what_the_retirement_refuses`. Enumerate first: both heading wordings and the summary line, English and Korean, tree-wide — the frame found the skill the only document naming a heading | `tests/test_settle_reads_before_it_removes.py -k "documents_say_the_closure or report_does_not_promise"`, each assertion seen red (second wording deleted from the skill; old summary wording in `settle.py#main`) | e4c76096 |
| 3 | **#612.** Every place in spec.md's #612 table, and any the repeated enumeration adds, rewritten to carry the statement spec.md fixes: the fork point on a branch checkout, the base's tip in CI. Both Korean editions in Korean prose written as Korean (`skills/writing-style` §영어를 옮길 때는), not translated clause by clause. The documents case extended as spec.md says, its docstring corrected. Phrasings to search at minimum: *fork point*, *forked from*, *where this branch forked*, *where you forked*, *after the fork*, *after your branch was cut*, *moving tip*, *the base revision*, *merge base* within a sentence about CI or a pull request; *갈라진 지점*, *갈라진 뒤*, *현재 끝*, *병합 기준*, *merge base* | `tests/test_unverified_rows_close.py -k merge_base_footing`, seen red before the prose; the unverified_check module's own cases (`tests/test_unverified_rows_close.py`) because its help and docstrings changed | a80180e0 |
| 4 | **#613.** The round's paste-ready lines in `chain_check.py#fix_surface`'s docstring. Enumerate first for twins of the `nobody` rule that state the check's timing without *at a ready pull request*: *beside a checked `Pass`*, *refuses it on the LAST record*, *fails beside*, *carrying `nobody`*, *carrying it*, *`Pass` 가 체크된*, *`Pass` 옆*; spec.md lists the two the frame judged not twins and why. Re-read each of the seven `@dd0a5d68` rows against the edit and re-stamp it in its release file with a dated `Re-read` note (`evidence-check --reverify`, then check the diff touched only those rows) | `evidence-check` reports no drifted row on `fix_surface`; `tests/test_chain_check_at_the_pull_request.py` still green (it holds the rule's behaviour) | de59906b |
| 5 | **#615.** Re-count first (questions.md Q1), then the round's three paste-ready texts with the measured figure in place of *280 of the 800* / *35%*. Enumerate the silent-set statement by meaning before editing: *goes silent*, *stays silent*, *silent when*, *four shapes*, *about 37%*, *298*, *falls back to its anchors*, in `skills/`, `docs/`, the survivor tests' docstrings, and `seal/specs/1790297084-*/` only to read (a closed work item's record is not rewritten). Plant `test_a_claim_split_into_two_rows_as_it_is_corrected_stays_measured` | `tests/test_a_corrected_sentence_survives_elsewhere.py -k "ledger or row or id"`; the new case seen red with `>=` changed to `==` in `removed_ledger_rows`, then restored | ae66911f |
| 6 | **#616.** The round's case appended to `test_a_name_rooted_in_a_variable_is_judged_where_the_variable_points`, and that case's docstring clause corrected. The docstring class from spec.md's #616 table: `as_cmd_expands` (the round's sentence, plus the defined-`CD`-wins correction), `handed_to_shell`'s docstring and comment, `templates/config.md` §*Broad gate* and its pinned needle. Enumerate first: *the way `cmd`*, *as `cmd.exe` expands*, *expanded the same way*, *in no environment*, *computes*, *`cmd.exe` 가 펼치*, *`cmd.exe` 처럼* | `tests/test_the_gate_hands_cmd_a_path_it_can_run.py`; the new assertion seen red with `value`'s two branches swapped; the reader case seen red with the old config sentence | 1e6cca3e |
| 7 | **Close.** The changelog fragment (one entry per issue, what a user of the plugin sees change: `seal` and `payload-meter` exit 2, the settle skill's second heading, the unverified-check documents, the survivor sweep's statement, the broad gate's documented limits). New ledger rows, if any, in `seal/ledger/1790381329-the-deferred-sentences-and-pins.md`. `overview.md` with its `## Not verified` table (Q2's row at least). A last `evidence-check` over the whole ledger to catch a drift a phase missed | `evidence-check` with 0 drifted and 0 broken; the phase records exist | |

Each phase writes `phases/phase-N.md` when it closes: what it was asked, the
phrasings it searched and what each hit was judged to be, how each new case
was seen red.

## Operational impact

- **Exit codes.** `seal` can now exit 2, where its docstring promised only 0
  and 1. A caller testing `!= 0` is unaffected; a caller testing `== 1` for
  "nothing was written" would miss a broken plugin copy, which previously
  died with 1 and a traceback. No caller in this repository tests seal's code
  (read: `README.md` says "exits non-zero").
- **No new dependency, variable or migration.**
- **Sibling branches.** B may re-stamp rows in the same `seal/releases/*.md`
  files; its frame leaves both READMEs unedited. The squash order is A, B, C, so C meets any conflict
  last and resolves it: ledger files hunk by hunk, then `evidence-check`
  (`docs/the-evidence-ledger.md` §*A correction a merge dropped*); the release
  branch merged in, never rebased onto (`docs/release-checklist.md` step 0).
