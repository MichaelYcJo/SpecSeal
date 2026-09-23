# Round 2 report — survivors.md silences what it quotes

Target SHA `84c6c5ffde5bfd6969e620c2d3358d8bd773f483`, base `cbb58091fddb9a02e3136156d7963dcd66798d1b` (the release branch), the verifying round at round 1's fixes: the range `e7dacbf896662667530ab07c72f7b6f6caffac13..09292fa8988915727a527e7bd3cec934e817f7b4` (`d3e544d6` the test, `09292fa8` the paperwork) plus `84c6c5ff`, the commit that closed round 1's record. Reviewed in a `git clone --no-local` of the worktree at the target SHA, in the session's scratch directory; nothing was written in the worktree except this file. Reviewer: `specseal:warden`. Round 1's record and report were read first, for coordinates; its 🟢 verdicts are carried where the fix range left what they cover untouched, and re-derived where it did not.

Every claim below is labelled **executed** (I ran it, in the clone, exit code read directly), **read** (I opened the code or the record), or **unverified** (nobody in this round ran it, and the answerer is named).

## The verdict in one paragraph

Round 1's 🟡 1 is closed as the record says. `test_a_phase_record_standing_in_the_pool_is_not_a_survivor` is parametrised over a 4-file and a 33-file pool, the module runs 70 green in a fresh clone, and with the `phases/` arm of `records_a_past_state` removed the two arms go red for their own reason — the small pool on the exit code with nothing named, the large pool on the `named` assertion with the phase record reported beside `guide.md`, both carriers at 1.60 — and go green again with the bytes restored. Two of the three paperwork corrections state what the tree holds; the third, the mutation count written as *6 and 6 over the whole module*, was written after the parametrisation and measured before it: on the module as committed the `corpus` reversion turns seven cases red, because the pool case is now two arms and both are among them. That is a ⬜ correction to a ledger fragment and a phase record, the same shape as round 1's ⬜ b, and it is out of `Needs a fix`. The fix range touched five files, every one of them the test module or a record this work item owns, and the record commit touched `round-1.md` alone. Nothing found leaves the root or crashes, so nothing here consumes the cap.

## Round 1's 🟡 1 — is it closed

**The case as committed** (read, `tests/test_a_corrected_sentence_survives_elsewhere.py`, the diff of `d3e544d6` and the function at the tip). The fixture is the round-1 paste-ready fix with one docstring sentence added at the end; `pytest` is imported at the module's head, the `fillers` parameter drives a loop adding `filler-<n>.md` files whose prose shares nothing with the quoted phrases, and both assertion messages name the pool size. The three assertions are the ones the paste-ready fix carried, in the same order: `code == 1`, `"guide.md" in named`, `named == ["guide.md"]`.

**Module green** (executed): `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q -p no:cacheprovider` in the clone, exit 0, `70 passed in 19.43s`. The runner built the clone's own `.venv`, which is the repository's tooling and not a leaving of mine.

**Both arms red under the arm-off mutation** (executed, one Python probe file in the scratch directory, run once and deleted). The line `return inside == ["survivors.md"] or (len(inside) > 1 and inside[0] == "phases")` in `records_a_past_state` replaced by `return inside == ["survivors.md"]`, bytecode caches cleared, `-k standing_in_the_pool` run with the clone's venv:

| Arm | Assertion that failed | The report |
|---|---|---|
| `[0]`, a pool of 4 | `code == 1` — `guide.md's copy went unreported on a pool of 4; exit 0` | `no removed wording is still standing` |
| `[29]`, a pool of 33 | `named == ["guide.md"]` — `the report names ['guide.md', 'seal/specs/1700000000-a-claim-stands-in-two-places/phases/phase-3.md'] on a pool of 33` | both places standing at `2 phrase(s), 1.60` |

`2 failed, 68 deselected`. Bytes restored and compared equal by SHA-256, the same selection run again: `2 passed, 68 deselected`. `git status` in the clone empty afterwards and `HEAD` at the target SHA before and after each run. That is the direction the frame named for S6 — a record reported beside the real survivor — with a red behind it for the first time, and by the assertion that refuses it rather than by the one before it.

**What the fix handed over, checked**: the hand-back's `2 failed` with those two messages, `2 passed` restored, and `70 passed` all reproduce. The orchestrator's re-run at `09292fa8` (module 70, `evidence-check --strict`, tree-wide ruff, CI-form sweep) is a claim I did not take as evidence; the module and the checkers are re-executed below, and tree-wide ruff is the sealer's.

## The three paperwork corrections — do they state what the tree holds

**The `Ran by` row** (executed and read). `overview.md` §*Not verified* row 2 now opens with ✅ and its answerer cell reads *filled by the orchestrating session at `bc38c8f3`; round 1's ⬜ a, closed in the round-1 fix pass*. `bin/unverified-check --baseline cbb58091… seal/specs/` exits 0 and reads this memo as `2 open · 1 closed`, so the checker counts the row as closed rather than as a third open row. The two rows still open are the broad gate (the sealer) and the effect on already-open branches (the orchestrating session), each with its answerer.

**The memo's red-run count** (read). `overview.md` line 12 now reads *eleven red runs over ten cases seen red first (6 + 4 + 1 across the phase records, the docstring case counted once per extension) and both arms of the parametrised pool case red in the round-1 fix pass*. The phase records give six at `531cc723` (S1, S2, S3, S4, S9, S10), four at `c1311c53` (the added, edited and pool phase-record cases, and S9 again for its second paragraph), one at `95956de8` (S7's deeper arm): eleven runs, and the distinct set is ten because S9 is the one name in both lists. *70 after round 1's fix* is the executed count above. *8 mutations red* is read: the two arms, the collapsed class, the two call-site reversions, the `OWNER_DIR` tail and the two docstring openers.

**E3 re-read, and the phase-2 record** (read against the executed output). Ledger row E3's evidence cell gained *Re-read 2026-09-24 in round 1's fix pass (finding 1)* followed by the two arms' outcomes — `[0]` red at exit 0 with nothing standing, `[29]` red on the `named` assertion with the record beside `guide.md` at 1.60, green restored, `2 passed` — and its anchor for the case was re-stamped to `@e64fda0b`, which `bin/evidence-check --strict .` accepts (exit 0, 1569 ok, 0 drifted, 0 broken). `phases/phase-2.md`'s bullet for the pool case carries the same two messages verbatim, and both match what the probe printed, message for message and score for score. The marker on E3 is spelled verb-then-date, which is the shape `correction_check.py` reads.

**The mutation counts — the one that does not hold at the tip** (executed). Ledger row E1 and `phases/phase-4.md` §*Mutations* were corrected from *3 and 5* to *6 and 6 over the whole module*, with a parenthesis saying the earlier figures *were the counts under the `-k` selections the mutation script ran*. Round 1 measured 6 and 6 at `bc38c8f3`, over the 69-case module. The correction was written at `09292fa8`, one commit after `d3e544d6` turned the pool case into two arms, and on the module as committed the counts are:

| Mutation | Red | Cases |
|---|---|---|
| `corpus` back on `records_a_past_round` | **7** | S1, S2, S3, the added phase-record case, the pool case's `[0]` **and** `[29]`, the path-list case |
| `corrected` back on `records_a_past_round` | 6 | S1, S3, S4, the added and edited phase-record cases, the path-list case |

So *6 and 6 over the whole module* names a module that no longer exists at the tip; a reader who re-runs the `corpus` reversion finds seven, for the reason the fix itself created. Round 1's ⬜ b was this same shape one commit earlier. The parenthesis about `-k` selections is the smith's account of the phase-4 run and nothing in the tree reproduces which selection produced 3 and 5; the corrected figures do not rest on it, so it is recorded here as read and left where it is. ⬜ below, with the sentence to write.

## The fix range's reach

**Read**, `git diff --name-only` over the fix range: `seal/ledger/1790174139-survivors-md-silences-what-it-quotes.md` (rows E1 and E3), `overview.md`, `phases/phase-2.md`, `phases/phase-4.md` under the work item's directory, and `tests/test_a_corrected_sentence_survives_elsewhere.py`. The record commit `84c6c5ff` changes `rounds/round-1.md` alone: the four cells that said *the fixes are not yet written* now name the range, the fix commit and the contract change, the `Pass` box is ticked, and 🟡 1's verdict reads `fixed d3e544d6`. The ledger fragment is the one file outside `seal/specs/<id>/`, and it is this work item's own. `skills/code-review/scripts/survivor_check.py` is untouched since `8dc9390` and its bytes at the target SHA equal the worktree's; no unit was added.

**Round 1's six 🟢 verdicts, carried and one re-executed.** The predicate, the call sites, `OWNER_DIR`, the follow-up rows and the five places on #525 rest on files the fix range did not touch, so those verdicts are carried and not re-derived. The branch's own sweep is the one that could have moved — the fix range added prose to the ledger fragment, which is in the pool — so it was re-executed in the CI spelling (`hygiene.yml`'s bash array, `python3 skills/code-review/scripts/survivor_check.py` with all 14 `--exempt` files): exit 0, nine `exempt`, `every survivor is excused by a row above (9)`, 371 files, 36 removed sentences; without `--exempt`, exit 1 and the same nine standing.

**Coverage probe over the records** (executed, two modules): `bin/test tests/test_the_last_rounds_fixes_are_checked.py tests/test_no_real_identifiers.py -q`, exit 0, 77 passed — the record commit's cells and the new prose pass the checks that read them. `bin/correction-check --range cbb58091…HEAD` exits 0 with *no merge commit in the range*, which is the expected answer on a feature branch. `uvx ruff check` and `uvx ruff format --check` on the edited test file, both exit 0.

## One thing about the run rather than the branch

The first clone of this round reported `9 failed, 61 passed` on the module. Its reflog shows `HEAD` moved from the target SHA to `8ab72d81` — the tip of the `fix/536` branch, another work item's round — at 00:50:54, inside the module's run, and back at 00:51:49, by commands this session did not issue. The clone had been named without the work item id in a scratch directory that parallel rounds of one session share. The result was discarded, the clone removed, and everything above was run in a second clone named after the work item, with `HEAD` checked before and after every run. Recorded in the probes table so the number is not read as the branch's, and in the summary for the orchestrating session, since the next parallel round will meet the same directory.

## Findings

### ⬜ a — E1 and phase-4 say the `corpus` reversion turns six cases red; on the committed module it turns seven

`seal/ledger/1790174139-survivors-md-silences-what-it-quotes.md` row E1, the evidence cell's sentence *`corrected` and `corpus` each put back on `records_a_past_round`, 6 and 6 red over the whole module*; and `seal/specs/1790174139-survivors-md-silences-what-it-quotes/phases/phase-4.md` §*Mutations*, the parenthesis *(**6 and 6** over the whole module …)*. The figures are round 1's, measured on the 69-case module at `bc38c8f3`; the fix pass wrote them into the records after `d3e544d6` split the pool case into two arms, and both arms go red under the `corpus` reversion, so the whole-module count at the tip is 7 for `corpus` and 6 for `corrected`. Paperwork under `seal/ledger/` and `seal/specs/`, out of `Needs a fix`. The sentence to write, in both places: *`corrected` and `corpus` each put back on `records_a_past_round`, 6 and 7 red over the whole module at `84c6c5ff` (the path-list case among them both times, and both arms of the parametrised pool case under `corpus`; the 5 and 3 first written here were counts under `-k` selections, and the 6 and 6 that replaced them were round 1's counts on the module before the pool case was parametrised)*. A `Corrected 2026-09-24` marker in front of it is what `correction-check` reads, and E1 carries none yet.

## Regression tests to plant

None. The one case this round verified is planted and has been seen red on both arms.

## Facts for the evidence ledger

- Row E3 holds as re-read: both directions of the pool half seen red on the committed module, each by its own assertion, `[0]` at exit 0 and `[29]` on the `named` assertion at 1.60; the anchor `@e64fda0b` resolves under `--strict`.
- Row E1's mutation counts at the tip: `corpus` reversion 7 red, `corrected` reversion 6 red, over the 70-case module (⬜ a).
- The branch's own sweep in the CI spelling at `84c6c5ff`: nine `exempt`, nine standing without the file, 371 files, 36 sentences.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟢 | Round 1's 🟡 1 is closed: the pool case runs on 4 and 33 files and each arm goes red on its own assertion with the `phases/` arm removed | `tests/test_a_corrected_sentence_survives_elsewhere.py` `test_a_phase_record_standing_in_the_pool_is_not_a_survivor` | answered | Executed: module 70 passed; arm removed → `[0]` exit 0 nothing named, `[29]` names `guide.md` and the phase record at 1.60, `2 failed`; restored `2 passed`, bytes equal |
| 🟢 | The `Ran by` row is closed and read as closed; the memo's eleven-over-ten count follows from the phase records; E3's re-read and the phase-2 bullet match the executed output message for message | `overview.md` §*Not verified* row 2 and line 12; `phases/phase-2.md`; ledger row E3 | answered | Executed: `unverified-check` reads `2 open · 1 closed`, `evidence-check --strict` exit 0 with `@e64fda0b`; read: 6 + 4 + 1 over ten names, the two arm messages verbatim |
| ⬜ | E1 and phase-4 say *6 and 6 over the whole module*; on the committed module the `corpus` reversion turns 7 red, both arms of the parametrised pool case among them | `seal/ledger/1790174139-survivors-md-silences-what-it-quotes.md` E1; `phases/phase-4.md` §*Mutations* | answered | Correction; executed counts 7 and 6 over the 70-case module; the figures written were round 1's, measured before the parametrisation the same fix pass committed |
| 🟢 | The fix range touched the test module and this work item's own records and nothing else; the record commit touched `round-1.md` alone; no unit added | the fix range `e7dacbf8..09292fa8` and `84c6c5ff` | answered | Read: five paths in the range, one of them the ledger fragment outside `seal/specs/<id>/`; `survivor_check.py` byte-identical to the worktree's and untouched since `8dc9390` |
| 🟢 | Round 1's six 🟢 verdicts stand — five carried on untouched files, the branch's own sweep re-executed in the CI spelling | `skills/code-review/scripts/survivor_check.py`; the branch's own range | answered | Carried: the predicate, call sites, `OWNER_DIR`, follow-up rows and the five places rest on files outside the fix range. Executed: nine `exempt` at exit 0 with 14 `--exempt` files, nine standing at exit 1 without |
| ❓ | Tree-wide `ruff check` and `ruff format --check`, and the full suite | the repository | out of verified scope | Not run in this round on §2 grounds; the hand-back labels them the sealer's and the orchestrator says it ran ruff at `09292fa8`. The sealer answers, and this round leaves nothing open, so that spawn is due |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test tests/test_a_corrected_sentence_survives_elsewhere.py -q -p no:cacheprovider` in the clone at `84c6c5ff` | exit 0, 70 passed |
| mutation: `phases/` arm removed from `records_a_past_state`, the pool case's two arms selected by `-k` | exit 1, `2 failed`: `[0]` exit 0, `no removed wording is still standing` · `[29]` names `guide.md` and the phase record, both at 1.60 |
| the same selection with the bytes restored | exit 0, `2 passed`; SHA-256 equal to the committed bytes; `git status` empty; `HEAD` at the target before and after |
| mutation: `corpus` back on `records_a_past_round`, whole module | 7 red — S1, S2, S3, the added phase-record case, pool `[0]` and `[29]`, the path-list case |
| mutation: `corrected` back on `records_a_past_round`, whole module | 6 red — S1, S3, S4, the added and edited phase-record cases, the path-list case |
| `bin/evidence-check --strict .` | exit 0, 1569 ok, 0 drifted, 0 broken |
| `bin/unverified-check --baseline cbb58091… seal/specs/` | exit 0; this memo `2 open · 1 closed` |
| CI spelling: `python3 skills/code-review/scripts/survivor_check.py --range cbb58091…...HEAD` with the 14 `--exempt` files of `hygiene.yml`'s bash array | exit 0, 9 `exempt`, 0 standing, `every survivor is excused by a row above (9)`, 371 files, 36 removed sentences |
| the same without `--exempt` | exit 1, 9 standing |
| `bin/correction-check --range cbb58091…...HEAD` | exit 0, no merge commit in the range |
| `uvx ruff check` and `uvx ruff format --check` on the edited test file | exit 0, exit 0 |
| `bin/test tests/test_the_last_rounds_fixes_are_checked.py tests/test_no_real_identifiers.py -q` (coverage probe over the record commit and the new prose) | exit 0, 77 passed |
| the first clone, named without the work item id in the shared scratch directory | module exit 1, 9 failed 61 passed; its reflog shows `HEAD` moved to `8ab72d81` at 00:50:54 and back at 00:51:49 by commands this session did not issue; result discarded, clone removed, everything above re-run in a clone named after the work item |
| the probe's leavings | two probe files in the scratch directory deleted; both clones removed; the worktree untouched except this file |
| Broad gate — full suite, tree-wide `ruff check`, `ruff format --check` | not yet |

Needs a fix: no — ⬜ a is a correction to a ledger fragment and a phase record under `seal/`, and the rule keeps it out of this line
Loses a record or crashes: no

## Proof block

Files opened in the clone at `84c6c5ff`: `tests/test_a_corrected_sentence_survives_elsewhere.py` (the fix diff, the parametrised case, the helpers `run`, `paths_in`, `build`, `phase_record`, `_mentions`, the constants `FOUND`, `REPAIRED`, `PHASE`, the docstring case, the module-loading head), `skills/code-review/scripts/survivor_check.py` (`records_a_past_state`, `records_a_past_round`, the docstring section on exclusions, `corpus`, `corrected`, the `--exempt` argument), `.github/scripts/run_tests.py`, `bin/test`, `bin/survivor-check`, `tests/conftest.py`, `.github/workflows/hygiene.yml` (the survivor step), `skills/code-review/scripts/chain_check.py` (the closed-verdict words), `skills/code-review/scripts/round_record.py` (the headings it parses and the finding-id rule), `skills/evidence-check/scripts/correction_check.py` (the marker's shape), `seal/ledger/1790174139-survivors-md-silences-what-it-quotes.md` (the fix diff and rows E1–E5), and under `seal/specs/1790174139-survivors-md-silences-what-it-quotes/`: `rounds/round-1.md` (the record and its closing diff), `rounds/round-1-report.md`, `overview.md`, `phases/phase-1.md`, `phases/phase-2.md`, `phases/phase-3.md`, `phases/phase-4.md` (at the tip and at `e7dacbf8`). Executed: the commands in the probes table, from two Python probe files in the session's scratch directory, each run once and deleted, and the runner and checker invocations named above.
