# 1791270165-the-windows-test-leg-is-measured-and-cut — phase 4

| Field | Value |
|---|---|
| Phase | 4 (4a and 4b) |
| Commit | 83801eac (4a; the sampler landed at 597cc5f7, its cover case was tightened here) · ba8a93d8 (4b; the cuts are fddc5cfa and 19413602) |
| Ran by | smith on Opus 5.5 (4a), and a second smith on Opus 5.5 on another machine (4b) |

## What this phase was asked

4a, local only: a covering sampler over `_placed(verb)` in
`tests/test_guard_resolves_the_tree_it_judges.py` with S5's coverage
contract asserted by a structural case; the twins case and
`test_no_constructed_switch_is_silent` walking the sample; the red against
`94d7b2e0`'s reading shown; Q4 measured by a `test_tmp_*` probe, deleted;
D1 of `seal/releases/0.18.2.md` re-read into this item's fragment. 4b is
not started.

4b, asked of a second smith on another machine once phase 1's tables were
in: from the Windows table, cut the other cases it names, each cut keeping
its case's claim and Q5 answered case by case here, every new or rewritten
case seen red (§15), and released rows whose anchors move re-read into the
fragment.

## What this phase found

**The sample.** `_sample(verbs)` keeps every
`(operator, position, glued, target spaced)` placement the product holds at
least once, the verb that carries each taken in rotation, and for every verb
its first shape with a redirection after the subcommand holding no `&` or
`|` and its first with one that does. It is a cover, not a draw: sorted
keys and list order only. Twins: 870 shapes of the product's 20,832.
`_placed` now yields `spaced_target` as a fifth value so the placement can
be read off a shape; `_shapes` and the two cases were its only readers in
the repository.

**What left.** Each verb is no longer read at every placement, only at the
placements it carries in the rotation and its two per-cut shapes. A defect
that one verb shows at one placement alone, and no other verb shows there,
can now pass. What stays: every placement is read for some verb, every verb
is read on both sides of a cut, and the per-verb readings in
`test_classify_reads_no_switch_in_a_twin` are untouched. The rewrite or
retirement of the case is #826's, by the owner's comment.

**Seen red (§15), each through `bin/mutation-check`, `executed` 2026-10-06:**

| Break | Cases run | Verdict |
|---|---|---|
| `_sample`'s placement loop: `chosen.add((holder, first[holder][key]))` → `pass` | `-k sample_covers` | `red` — both parameters fail on `missing` (1.6 s) |
| `hooks/worktree-guard.py#read_switch_words`: the `--` return counts any `-b…` after it as creating, `94d7b2e0`'s reading | `-k no_twin_is_asked` | `red` — 28 shapes wrong, `git checkout -- -b y <<<word` among them (6.2 s) |

Both files were restored by the tool from its own copy, and
`git status --short` showed only the intended test edit after each.

**Every unit added, broken one at a time before hand-over.** The first pass
over the helpers found three that nothing watched: `_after_the_subcommand`
(`at > 2` alone), `_placement` (the target-spaced axis dropped) and an
ordering helper, each `SURVIVED`. The cover case measured coverage through
the same `_placement` the sampler used, so a dropped axis vanished from both
sides at once. The fix: the cover case reads the placement off each tuple
directly and states `_after_the_subcommand`'s boundary values, and the
ordering helper is gone, since order decided nothing a case reads
(`sorted(chosen)` keeps the sample deterministic). Re-run with
`-k 'sample_covers or no_twin_is_asked or no_constructed_switch'`:

| Break | Verdict |
|---|---|
| `_after_the_subcommand` → `return at > 2` | `red` (6.1 s) |
| `_placement` → `return op, at, glued, True` | `red` (5.1 s) |
| `_sample`'s placement loop → `pass` | `red` (3.8 s) |

The module after that edit: `426 passed in 18.53s`, exit 0; ruff check and
format exit 0. The two rewritten cases' anchors did not move again, so the
`Re-read · D1` row still holds.

**Q4, `executed` 2026-10-06.** A probe (`tests/test_tmp_twins_spawns.py`,
run once with `-p no:xdist`, deleted in the same command) subclassed
`subprocess.Popen` with a counter. The sampled twins case started **194
processes over 870 shapes**; the first three verbs' 1,268 shapes of the
full product started **0**. So the case is not wholly CPU-bound: some verbs
reach a lookup `is_ref`'s patch does not cover, at roughly one spawn in
four shapes across the sample. Which lookup was not recorded. At the
issue's 60 ms a spawn on Windows, the sample's 194 cost about 12 s there,
against roughly 4,600 for the whole product if the ratio holds. Sampling
alone was kept, Q4's default; growing the fixture is for 4b if the Windows
table still names the case.

**Timing, `executed` 2026-10-06 on the smith's machine.** The three cases
with `-p no:xdist`: twins 2.85 s, switches 0.18 s, the cover case 0.14 s
together. `bin/test tests/test_guard_resolves_the_tree_it_judges.py -q`:
`426 passed in 17.74s`, exit 0. `ruff check` and `ruff format --check` on
the file: exit 0 each.

**The ledger.** `evidence-check .` reported two DRIFTED coordinates, the two
rewritten cases, both cited by D1 of 0.18.2 alone. `evidence-check
--reverify --into seal/ledger/1791270165-the-windows-test-leg-is-measured-and-cut.md
--checked 2026-10-06` wrote one `Re-read · D1` row; no released file
changed.

**`evidence-check --strict .` exits 2, and the cause is in the frame.**
`spec.md`'s Grounding row (line 14) quotes D1's anchor with its released
hash, `…#test_no_twin_is_asked_unless_an_operator_cuts_the_segment@3e34189e`,
and the checker reads that quotation as a coordinate. Any rewrite of the
case drifts it, so plan 4a's `evidence-check --strict .` exit 0 cannot hold
as the frame stands. `spec.md` is the framer's, and this phase did not edit
it. `overview.md` names who answers. (The framer reworded it at a321fbcb,
and `--strict` exits 0 since phase 1's close.)

## 4b — what building it found

**What 4b can buy is bounded, and the bound is phase 1's.** The Windows top
50 of run 37429940700 hold 652 s of call time, 9 to 12% of the leg's worker
time (`phases/phase-1.md`). If every case in the table went to zero, the
leg would lose about 2.7 of its 30 minutes on four workers. So 4b cuts
repetition where a cut keeps the claim, and the shards of phase 3 carry the
leg.

**Every cut is the same move: a prefix several cases repeat is built once
and copied.** A case's claim is about what happens after the prefix, so
running the prefix once keeps the claim and drops only the repetition. Under
xdist a session or module fixture is built once per worker that needs it,
not once per suite, so on four workers the saving is smaller than the serial
figures below.

### Q5, case by case

Round 1's 🟡 3 later replaced `_stopped_runs` (a cache built inside the first asking case's call) with two session fixtures, `_stopped_untouched` and `_stopped_touched`, which `a_stopped_run` requests in setup. The rows below name the unit as 4b built it. · NAME NOT IN TREE

| Cases | Windows figure, run 37429940700 | Cut | What the case still holds | What left |
|---|---|---|---|---|
| `test_a_fix_of_a_fix_is_counted.py`: `test_a_record_after_an_unreframed_second_is_refused`, `test_a_reframe_naming_another_round_does_not_permit_the_record`, `test_the_depth_restarts_at_a_stop`, `test_a_reframed_record_is_written_and_starts_the_count_at_no[False]` and `[True]` | 16.9, 15.5, 20.9, 16.4, 16.5 s (86.2 s) | `_stopped_runs` builds each stopped run (touched or not) once through `stopped`, as before; `a_stopped_run` copies it into the case's directory | each case's own step after the stop: the frame written, `new` or `close` run, and the record read. The stop's own assertions (round 3 reads `second`, each `close` below exit 2) run once, at the build | the three-round stop rebuilt five times · NAME NOT IN TREE |
| the same module: the 35 cases of `test_a_location_that_lands_in_no_written_unit_reads_no` and `test_a_location_carrying_its_py_path_still_lands` | 8.97 s for the one in the table, the parameter ending `; see #w`; the other 34 sit under the table's 8.15 s floor, so their figure is inferred, not read | `_named_and_fixed_once` builds the named files, the declaration, round 1 and its closed fix once; `named_and_fixed` copies it. `two_rounds` became `round_one_fixed` plus round 2, so the other cases read as before | round 2's record, generated per case from that case's `Location`, which is the whole claim | two generator runs and five commits per case |
| `test_the_seal_is_taken_once_by_the_sealer.py`: `test_a_repository_shipping_no_gate_runs_the_invoked_copy`, `test_a_recorded_seal_on_a_pipe_signals_and_draws_nothing`, `test_the_values_file_holds_this_runs_panel`, `test_a_recorded_seal_says_the_cell_is_written_and_not_committed`, `test_the_gate_with_record_seals_the_item_and_counts_its_rounds`, `test_the_panel_reports_the_rows_exit_code_and_asserts_no_linter` | 12.4, 11.7, 11.7, 11.9, 12.2, 12.0 s (71.8 s) | `a_sealed_run`, module-scoped: one settled item sealed through `--record` with session `s-1`, under a directory whose name holds a space, as the pipe case's own run was | every assertion each case made, read off the one run's stdout, stderr, values file and tree; the real gate and the real pytest row, so `suite 1 passed` is still pytest's own count | five identical gate runs; the space in the path, once the pipe case's alone, is now under all six, which none of the other five reads |

**Q5's other cut, a cheaper `Broad gate` row (`plan.md` Alternatives K),
was not taken anywhere.** No case was read for whether its claim is about
pytest's output, so Q5's default stands: each keeps the real runner.

### Left alone, with the Windows figure and the grounds

| Cases | Windows figure | Why left |
|---|---|---|
| the twelve other sealer cases in the table (`test_a_run_whose_report_names_no_failure_and_exits_otherwise_is_not_measured[tests-none-failing]`, `test_values_that_cannot_be_written_leave_the_seal_standing`, `test_the_pull_request_the_record_names_reaches_the_values_file`, `test_a_run_with_no_session_says_so_and_names_the_hand_command`, `test_the_gate_reads_the_real_seals_two_endings_apart`, `test_a_settled_item_preflights_green_and_names_the_record_it_asked`, `test_a_seal_exit_that_is_not_two_leaves_the_tree_unsealed`, `test_a_runners_event_payload_judges_the_fixture_and_fails_its_gate`, `test_a_fixed_at_verdict_in_a_verifying_round_fails_the_preflight`, `test_a_first_runner_without_the_gates_environment_costs_the_word`, `test_the_generated_unread_fixes_fail_the_preflight_at_seal`, `test_a_capped_run_is_sealed_with_its_deferral_on_the_stamp`) | 8.2 to 14.8 s (129.7 s) | each prepares a state of its own before its gate run (a file in the values directory's place, a pull request on the record, no session, a capped run …), so no two share a run. The remaining lever is Alternatives K, case by case, which nobody has read for them (`overview.md` Not done) |
| `test_the_second_landing_in_a_run_reads_second_and_prints_the_stop`, `test_a_quiet_record_between_the_two_does_not_restart_the_count` | 12.4, 17.4 s | each is the only case on its path: the first reads what round 3's `new` prints, which is the last step of the prefix the stopped template holds, and the second runs four rounds no other case runs |
| `tests/test_no_shape_the_base_stops_reads_silent.py::test_no_shape_the_base_stops_reads_silent`, `tests/test_the_guard_asks_once_per_session.py::test_the_guard_is_never_silent_where_the_writer_records` (the plan's "two guard cases at 31 s and 38 s locally") | 36.4, 23.3 s | neither repeats anything. The first walks a corpus of measured leaking rows, each a distinct finding of an earlier round, and issues each twice per session because a first stop and a later one are answered differently; the second walks states, directories and commands whose combinations round 2 of its work item found a defect in. A smaller corpus drops claims. The guard's premise is #826's, which reads these figures (`spec.md` Scope 1) |
| `tests/test_guard_resolves_the_tree_it_judges.py::test_nothing_the_base_read_as_a_switch_goes_quiet`, and the modules the frame did not name (`test_a_record_precedes_the_fixes_it_commissions.py` 48.8 s over 4 cases, `test_the_commit_gate_decides_at_the_commit.py` 45.4 s over 4, `test_the_fixes_close_the_record.py` 37.6 s over 3, seven modules with one or two cases) | see `phases/phase-1.md` | outside 4b's list in `plan.md`. They are on the table for phase 5's per-case ceiling to name, and the guard case for #826 |

### Seen red (§15) and every added unit broken, `executed` 2026-10-06

Each through `bin/mutation-check`, `-p no:xdist`, on the second smith's
machine. The rewritten cases first, against the code they pin:

| Break | Cases run | Verdict |
|---|---|---|
| `round_record.py#reframed_after` returns `True` | the unreframed and the wrong-round reframe cases | `red`, both fail |
| the same returns `False` | the depth-restart case and both reframed cases | `red`, all three fail |
| `round_record.py#landings` reads with `paths_only=False` | the 25 lands-nowhere location cases | `red`, 5 fail |
| `landings` lands nothing (`if False:`) | the 10 py-path location cases | `red`, all 10 fail |
| `broad_gate.py#uncommitted_line` returns `None` | the cell-written case | `red` |
| the session sentence printed with two spaces | the pipe case | `red` |
| the `rounds` row counts one more round | the values-file and record-seals cases | `red`, both fail |
| the ledger row reads `okay` for `ok` | the panel-rows case | `red` |
| the stderr line reads `gates` for `gate` | the shipping-no-gate case | `red` |

Then each unit this phase added:

| Unit and break | Verdict |
|---|---|
| `_stopped_runs`: `stopped(d, touched)` built untouched | `red`: `[True]` fails on the new assertion that only the touched copy carries `return 1000` · NAME NOT IN TREE |
| `a_stopped_run`: copies the untouched template whatever is asked | `red`, the same assertion |
| `_stopped_runs`: `if touched not in built:` → `if True:` | `SURVIVED`, and it should: the cache changes what the build costs and nothing a case reads. A dropped cache shows as time in the `--durations` table · NAME NOT IN TREE |
| `a_sealed_run`: built with no space in the path | `red`, the pipe case |
| `a_sealed_run`: built under session `s-2` | `red`, the pipe and values-file cases |
| `_named_and_fixed_once`: `round_one_fixed(d)` → `declared(d)` | `red`, all 10 py-path cases |
| `named_and_fixed`: hands the template itself to every case | `red`, 9 of 10 (round 2's record already exists from the first) |
| `_named_and_fixed_once`: `with_named_files(d)` → `pass` | `SURVIVED`. Moved, not added: since the reframe after round 3 only a `.py` path lands, so the named files decide no case's outcome. Whether the files should stay in the cases is the module's owner's to judge; it changes no claim this phase made (`read`) |

`git status --short` showed nothing but this item's records after each run.

### Timing, `executed` 2026-10-06, serial (`-p no:xdist`) on the second smith's machine

The machine ran other sessions' suites at the same time, so one figure can
move by a factor of four from one run to the next (the record-seals case
took 32.6 s before). The before column ran the cases from the commit before
each cut, copied to a `test_tmp_*` file, run once and deleted (§7).

| Cases | Before | After |
|---|---|---|
| the five stopped cases | 43.9 s | 21.8 s, both templates' builds included |
| the six sealed-run cases | 93.0 s | about 7 s: the shared run's 6.5 s setup, each case under 0.3 s |
| the 35 location cases | 223.8 s | 90.7 s, the template's build included |

The narrow runs after the cuts: `bin/test tests/test_a_fix_of_a_fix_is_counted.py
tests/test_the_seal_is_taken_once_by_the_sealer.py -q` gave `525 passed in
350.66s` after the first two cuts, and `bin/test tests/test_a_fix_of_a_fix_is_counted.py
-q` gave `58 passed in 80.82s` after the third; exit 0 each, read directly.
`ruff check` and `ruff format --check` exit 0 on both files.

**What the Windows leg gains is phase 3's to read.** The draft pull
request's first run is the leg after 4b, and its table says what these cuts
bought there.

### The ledger

`evidence-check .` reported twelve DRIFTED coordinates, all the rewritten
cases. Each released row citing one was read against its case before the
re-read: G2 of 0.15.1, N1 and N5 of 0.15.7, N3, N5 and P1 of 0.17.0, and
A1, A2, A4 and A8 of 0.19.0. Each claims what the gate or the generator
does, and each case still asserts it, shown by the reds above.
`evidence-check --reverify --into seal/ledger/1791270165-….md --checked
2026-10-06` wrote ten citing rows and left no released row. `evidence-check
--strict .` exit 0, read directly.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| The twins and switch cases' walk over every shape of `_placed` | `_sample`'s cover, held by `test_the_sample_covers_every_placement_and_every_verb`; the full walk is #826's to rewrite or retire |
| 4b: the stop rebuilt by five cases, round 1 and its fix rebuilt by 35, and one sealed gate run made six times | `_stopped_runs` and `_named_and_fixed_once` in `tests/test_a_fix_of_a_fix_is_counted.py`, `a_sealed_run` in `tests/test_the_seal_is_taken_once_by_the_sealer.py`; each case's own step still runs per case · NAME NOT IN TREE |
| 4b: the pipe case's own move of its repository under a spaced directory | `a_sealed_run`, which is built there |
