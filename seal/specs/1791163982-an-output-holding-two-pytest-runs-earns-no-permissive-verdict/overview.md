# 1791163982-an-output-holding-two-pytest-runs-earns-no-permissive-verdict — overview

## Why this work exists

The broad gate read its words at the base off printed text that can hold a
second pytest run, and gave a permissive word from it; it now reads pytest's
own JUnit report of the one run it asked about, and a row with two runners
reads `new?`.

## Where spec and implementation diverged

| Divergence | Spec says / code did | Chosen | Grounds |
|---|---|---|---|
| A failing test placed on no appended file | `spec.md` Scope 3: "on none of them → `new?` for every file it could be, and for every file not named" / read as every file no failure names, it turned S5's `an-inner-failed-line` case from `new` to `new?`, because `SUITE_ROW` collects all of `tests` and the base's own failing `tests/test_one.py` is in the report | such a failure is a file the row collected besides the appended ones and decides nothing; a file the report names no test of reads `UNPLACED` | `spec.md` S5: every 0.18.2 word assertion is kept. The scope's protection holds: a name the reader cannot place hides the file's passing tests too, so the file reads `new?` (`phases/phase-1.md`) |
| One file named at two offsets | spec silent / the either-direction match alone gives `failing on base too` to `tests/test_two.py` where the row collects it and `other/tests/test_two.py` and only the second fails at the base | `UNPLACED` | one run has one rootdir, so two offsets are two files; constructed (`two-offsets` row) |
| The reader's inputs | `spec.md` Scope 3: "a pure function of (report text, the files appended, the run's exit code, whether the run stopped early)" / those four do not tell a candidate's run of one file from a run of the others that holds one file | a fifth argument, `alone` | rule 3's pinned limit sentence, held by `test_a_file_the_base_carries_only_at_the_root_is_not_measured_under_a_cd` |
| S6's base | `spec.md` S6: "The base fails `tests/test_two.py`" / with the base failing it, the `sh -c` row runs its own `tests` and a3aa139a read `failing on base too`, true by coincidence, so no `new` to see red | both rows built with a base that passes the file; both read `new` at a3aa139a | S6's "seen red (`new`)" is the point of the case |
| S3's branch | `spec.md` S3: S1's base under `-rN` and `-rP` / the branch's own run writes no `FAILED` line under those flags, so nothing was compared | the branch's failing test prints the two `FAILED` lines (`spec.md` Axis C) | the scenario cannot be reached otherwise |
| Two cases beyond S1–S11 | `spec.md` §*User scenarios* / a report left in a reused `--keep-output` directory settled a prefix that wrote nothing, and a relative `--keep-output` under a `cd` sent the report under the scratch worktree | the stale path is removed before each run and the path made absolute, each with a case | contract §15 and `agents/smith.md`'s mutation rule |
| A released row the writer re-read | the `--reverify --into` writer wrote a `Re-read ·` row for 0.18.1's B4 / B4 says "the two reasons are pinned whole", and there are now five | a `Corrected · B4` row in place of the re-read | the claim names a count the change made false |
| A pin in a module the spec never names | spec silent on `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py` / its `test_each_rule_is_carried_with_the_reason_it_is_a_rule` held rule 3's old reason, "until one prints pytest's summary", and went red | the pin holds "until one writes that report", absent at a3aa139a | contract §14: the rule's reason is the sentence the change rewrote |
| Three framed lines naming what the tree lacks | `spec.md` (twice) and `plan.md` name a test this work removed and `PYTEST_PLUGINS` / `evidence-check`'s records arm refused them | each line carries the checker's `NAME NOT IN TREE` marker; no word of the frame changed | the refusal's own text, the repair work item 1791119069 made too |

## Not verified

| Item | Who must answer |
|---|---|
| The full suite, lint and typecheck after the rounds | the sealer, spawned by the orchestrator |
| The cases on Windows (`cmd.exe`) and Linux: the quoted `--junitxml=<path>` through `cmd.exe`, and the `PYTEST_ADDOPTS` collection pass there | CI's three-platform test job |
| This repository's own row through a real failing broad gate (`bin/test -q` handed `--junitxml` at the base) — the probe ran `bin/test` directly, not through the gate | the sealer, at its run, only if its run fails a test |

## Not done

A file that holds no test at the base, beside another collected module of
the same name, could read `failing on base too`. Round 1 of review ran two
shapes of it (a package named like the module, and a same-named module
deeper in the tree), and its fix pass closed both: a test is placed by the
path the `xunit1` report gives it, and a positive offset only where every
test in the report shares it. One shape stays open and is named in rule 3:
pytest's rootdir below the directory the row runs pytest in, with a
same-named module a directory up that the row also collects. Where a report
carries no `file` attribute at all, the dotted fallback still cannot tell a
class from a package of the same name at offset 0; every pytest the fix pass
ran writes the attribute.

Two runners that drop the gate's arguments stay uncounted, named in rule 3
and filed as #807: one given `-p no:junitxml`, and a later one inside a part
that drops its arguments.

Measuring a two-runner row file by file (`plan.md` Alternative F) and the
runners collection alone cannot reach (`spec.md` Axis B) stay out, as the
frame left them; rule 3 names the second.

## Fed back into the spec

none — the divergences above are recorded here and in `phases/phase-1.md`;
no clause was added to `spec.md`.
