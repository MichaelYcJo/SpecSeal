# 1791384158-the-broad-gate-reads-its-counts-from-the-recorder — overview

📋 implement applied
· spec:     this item's `routing.md`, `handoff.md`, `spec.md`, `plan.md`, `questions.md`; `templates/config.md` §*Broad gate* rule 3; `skills/verify/SKILL.md` §*The broad gate — after the rounds, then compare against the base*, the **New?** bullet; `docs/the-broad-gate.md` §*Where the stamp is drawn*; `agents/sealer.md` §*The command*; `docs/release-checklist.md` §6; `docs/the-record-layout.md` §*A change writes fragments, never a shared file*; `docs/the-evidence-ledger.md` (the `evidence-check --help` text of it); the released rows `evidence-check` named, each read before its re-read or correction
· evidence: `seal/ledger/1791384158-the-broad-gate-reads-its-counts-from-the-recorder.md` — K1–K17 for this work's own claims; 23 `Corrected ·` rows for released rows this work made false; 78 `Re-read ·` rows from `evidence-check --reverify --into … --checked 2026-10-08`
· verified: executed — Q-M1 on pytest 6.1, 7.0 and 9.1 and on 9.1 with xdist 3.8; every new and re-aimed case red at 5623d728's code (or, for the byte-for-byte case, under a mutant) and green after; the touched modules whole at each phase boundary; 70-odd `bin/mutation-check` runs; `DRY_RUN=1 release_seal.py` over a local record; `bin/evidence-check --strict .`; read — the window of Scope 5, which needs the owner's plugin update; the full suite, which is the sealer's

## Why this work exists

The seal's suite counts were read off text a test could print into, two stops passed a half-run base as finished, and a dial on the stamp turned nothing; now the counts and the stops are what the row's own pytest recorded, and the dial is gone.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| When `suite_counts` is None | `spec.md` Data & interfaces: "None where `record.sessions` is 0 or `record.unread` is not 0" / also None where no report was counted | the third condition | A session that ran nothing has no count to print; the panel then reads `exit <n>`, as it did for pytest's `no tests ran` |
| How often a collection counts | spec silent / a `collect` line counts once per session per node and outcome | once | `read_record` already reads a file's lines as a set because xdist can hand the controller one failed collect report per worker; counting each would print `2 errors` for one broken module |
| A teststatus answer with no word | `spec.md` §*The input class*: "written as given, `""` included" / a hook that raises, an empty answer, or a first element that is not a string writes `None` | `None` | "It never raises out of a hook" (the recorder's docstring); `None` counts under no category in the gate, as the input-class table says of a non-string |
| `failure_lines`' signature | `spec.md`: it gains the unread line and the counts / it takes the head `RunRecord` as `record` from phase 2, replacing its `unplaced` and `unended` integers | `record` | A third integer would have been replaced by the record in phase 3 anyway; no caller used the old keywords |
| How `panel` is handed the run's record | `spec.md`: "the head record is read once … and handed to `failure_lines` and to `panel`" / `panel(..., run=)`, a new keyword after `record` | `run` | `panel`'s `record` is the work item's round record, which `rounds_rows` reads and #866 changes; the seam (`plan.md` §*Seams*) keeps that call untouched |
| What the **New?** bullet says | `spec.md` §*What this frame removes*: the bullet takes rule 3's new clause / it also gains one sentence on a base record with a line that did not parse, and one clause on such lines at `HEAD` | both | Contract §14: `UNREAD_AT_BASE` is a new `new?` reason a reader is handed, and the bullet is where a reader is told what each reason means. Rule 3 was left without it: a damaged record is not a row the gate cannot measure. The bullet's wording differs from rule 3's because `tests/test_no_passage_is_pasted_into_a_second_file.py` refused a 31-word run they shared |
| R3's reading of xdist under `-x` | `spec.md` R3: "the stop flag is `DSession.shouldstop`, … so the exit-code net keeps it" / measured: the controller's own `Session` sets `shouldfail` from the reports xdist forwards | measured | Q-M1 (`phases/phase-1.md`); the exit net still keeps it as well. `RAN_TO_ITS_END`'s comment says what was measured |
| `pytest.exit()` in an xdist worker | spec silent / measured: exit 3 on the controller, no hook called | named in `RAN_TO_ITS_END`'s comment | The exit net refuses 3, so nothing passes; the comment names it so nobody expects `stopped` to carry it |
| The byte-for-byte fixture's form | `questions.md` Q-W3: "the byte-for-byte fixture captured at 5623d728" / six SHA-256 prefixes, pinned in the case | hashes | A sixteen-digit hash fails on any byte, and the block form is kilobytes of colour codes (`phases/phase-5.md`) |
| The values file's `scale` | `spec.md` Scope 5: "`signal` writes no `scale`" / `signal` writes the constant `SCALE_FOR_OLDER_HOOKS`, 0.9, through 0.21's cycle | the constant | Round 1's 🟡 3, option A, the orchestrator's decision: the gate a session runs is the tree's copy while the hook and `seal-stamp` are the installed plugin's, and 0.20.0's refuse a file without a numeric `scale`, which left every seal of the cycle undrawn and the `--from` recovery refused too. Read by nothing in the tree; its comment names the release that removes it |
| Q-M2's run | `questions.md` Q-M2: "this repository's own suite run once through `bin/test -q`" / four modules, and S5's tree on every run | narrowed | A full-suite run is the sealer's (contract §2), and the spawn prompt forbade it too; see *Not verified* |
| Two released rows kept as re-reads | `spec.md` S15 lists "0.20.0 … corrections … where they say *at every scale* or name the ladder's rung" / 0.20.0's `Corrected · N5` and `Corrected · P1` say the `suite` row is "`✓` and pytest's counts" | `Re-read ·` | The counts are still pytest's own categories, now read off the record; neither row names a scale, a summary line or the text reader |

`docs/release-checklist.md` §6 after the merge of `origin/release/v0.21.0`
(452d891d): #858 rewrote the plugin directory's box and the paragraph above
the commands, and this work rewrote the release note box's by-hand route; the
two edits touch different boxes and state no conflicting fact, so both stand
as merged. The ledger rows citing §6 — K14 and the re-reads of S9, P1c and W4
— were read against the merged section and re-stamped.

## Not verified

| Item | Who must answer |
|---|---|
| Q-M2 over the whole suite: `suite_counts(record)` against pytest's printed line for this repository's full run | the sealer's broad gate, once, after the rounds: its panel's `suite` row against the line in `suite.txt` |
| The full suite, the repository-wide lint and the typecheck | the sealer, once, after the review rounds settle |
| ✅ The one window of Scope 5: in this repository, a values file the tree's gate writes before the owner updates the plugin is refused by the installed 0.20.0 hook and left pending; drawn after the update, or at once with `seal-stamp --from` | closed by round 1's fix, 6ea5686e: the gate writes `"scale": 0.9` through 0.21's cycle, and the installed 0.20.0 `seal_stamp.py --from` drew a values file written that way, exit 0, executed 2026-10-08 |
| The `seal` job's suite step with the recorder loaded, on a real tag: the directory made, the key handed on, `SUITE_RECORDS` and `SUITE_KEY` read | the next release's `seal` job, read by the owner in its log |
| The gate's new end-to-end cases (S7, S8, S14) on Linux and Windows | CI's three-platform `pytest` job, at the pull request |

## Not done

- **A run at `HEAD` that pytest stopped with exit 0 still seals.** `pytest.exit(returncode=0)` in a test, or a plugin's stop that exits 0, leaves the suite arm green, and the gate seals over a run that did not finish; `UNENDED_HERE` is printed only on the failure form. Closing it changes when the gate seals, which no scope item of this work names. Filed as #883 (round 1's 🟡 6).
- A test with no file of its own counted under no category, so the counts could be short of pytest's own line; round 1's 🟡 2 made it this branch's to fix, and the counts are now refused on the panel and the release seal where `unplaced` is not 0 (#884).
- One over-strictness is named in `RAN_TO_ITS_END`'s comment rather than closed (round 1's ⬜ 4): a session whose `-x` or `--maxfail` limit fell on its last test ran every test and still reads unended, because pytest sets `shouldfail` either way.
- **`deferred_home`'s docstring** says it writes a pattern inline "as `suite_counts` writes its clock", and `suite_counts` no longer has one. The unit is #866's (`plan.md` §*Seams*), so the sentence was left for that branch to drop.

## Fed back into the spec

- `suite_counts` is None where no report was counted — *inferred during implementation*.
- A collection counts once per session — *inferred during implementation*.
- The **New?** bullet names a base record holding a line that did not parse — *inferred during implementation*, from contract §14.
