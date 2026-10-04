# 1791119069-a-cd-rows-failing-path-is-measured-under-its-own-directory — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | 7d65dfe9 |
| Ran by | specseal:smith on claude-opus-5-5 |

## What this phase was asked

The resume after the re-frame (d22b105b, re-approved at 186d9c7b), approach H.
The root check only nominates candidates: failing files the base's root tree
lacks. Each candidate is confirmed by a run of the row's prefixes at the base
on that file alone. A pytest summary gives the measured verdict. A lone
`no tests ran in <t>s` line with exit 4 or 5 gives `new`. Anything else gives
`new?`, with `NO_RUNNER`'s parenthesis and its pin changed in the same commit.
The runs are kept as `suite-at-base-<k>-<n>.txt`. Rule 3 states the cost and
the two limits in sentences that are pinned. Cases S1, S1x, S2, S3, S4 and S5,
each seen red first at 94d7b2e0 where it can be.

## What this phase found

- **Seen red at 94d7b2e0 first**, with the gate and `templates/config.md`
  byte-identical to that commit and only the cases added. 17 failed:
  - S1 and S1x read `new`;
  - S2, plain and xdist, read `new?` for both files;
  - S3 kept only `suite-at-base-1.txt`;
  - S4 read `new`;
  - the nine S5 rows failed on the missing reader;
  - the rule-3 pin and the `NO_RUNNER` whole-text pin failed on their text.

  After the fix, the three modules the change touches gave 475 passed and
  1 skipped. Those modules are this one,
  `tests/test_the_gate_hands_cmd_a_path_it_can_run.py` and
  `tests/test_the_broad_gate_row_is_asked_for_and_runs_as_written.py`.
- **The frame's Scope 4 did not hold as written, and the case held
  instead.** Scope 4 said every run "is a `run(...)` call written in
  `compare_at_base`'s own body, so `test_the_one_shell_site_is_run_and_it_applies_the_rewrite`
  holds unchanged". With a second loop for the candidates, that case went
  red: `['compare_at_base', 'compare_at_base', 'gate']`. It counts calls,
  not the functions they sit in. The case was left unchanged. The body now
  builds one list of groups: every other file as one group, then one group
  per candidate. One loop runs them through the prefixes, so `run` is
  called from one place.
- **The kept-file name is the group's suffix, and so is the guard.** The
  nothing-collected reading is applied only to a group of one. A run of
  several files that collects nothing does not say which file the base
  lacks. That is the un-nominated direction, the last row of `spec.md`'s
  class table, and there it must stay `new?`. No scenario in `spec.md`
  covered the guard. So a case was added beyond S1–S7:
  `test_a_file_the_base_carries_only_at_the_root_is_not_measured_under_a_cd`.
  It is green at 94d7b2e0 too, because the old code also gave that shape
  `new?`. The mutation that drops the guard turns it red.
- **The order of the words is now the branch's.** At 94d7b2e0
  `compare_at_base` returned the absent files first. It now returns
  `{f: verdicts[f] for f in files}`, the order the branch's `FAILED` lines
  first named them. S3 was parametrised plain and xdist so that its plain
  half can pin this; under xdist the `FAILED` order is the order the
  workers finished in. Mutating the return to `verdicts` turns S3[plain]
  red.
- **Two sentences outside the frame's edit list were made false, and were
  corrected (contract §12):**
  - `skills/verify/SKILL.md`'s **New?** bullet told a reader to open
    `suite-at-base-<k>.txt`, which a candidate's run is not kept as. It now
    reads `suite-at-base-*.txt`. The spec said that file is not edited, on
    the grounds that the words' meanings do not change. Those grounds still
    hold; the file name is what changed. `overview.md` records it.
  - The docstring of `test_a_file_named_below_a_cd_is_run_at_the_base_and_not_called_new`
    said the file "is run there with the others". It is now run alone. Its
    assertions are unchanged.
- **Rule 3 does not use the word "nominated".** The third sentence says a
  file "is not run alone", which a row's author can read without this
  module's vocabulary. The code's comment and docstring keep "candidate".
- **Every unit was mutated, one at a time, through `mutation-check`, and
  each came back `red`** (exit 0, the tree restored and clean afterwards).
  The cases were run with `-p no:xdist` for the runner; the xdist fixtures
  start their own pytest.

  | Break | Cases that went red |
  |---|---|
  | `NOTHING_COLLECTED_RE` without `$` | S5, the trailing-words row |
  | without `^` | S5, the `echo:` row |
  | without the leading `=*` | S5, run 7's ruled row |
  | `collected_nothing` without the exit condition | S5, exit 0 and exit 1 rows |
  | `NOTHING_COLLECTED_EXITS = (4,)` | S5, runs 2 and 7 |
  | `NOTHING_COLLECTED_EXITS = (5,)` | S5, run 1 |
  | the guard `alone and` dropped | the added limit case |
  | nothing collected gives `NO_RUNNER` instead of `new` | S2 ×2, S3 ×2, the base-lacks case |
  | the suffix `-{n}` spelled `_{n}` | S1 ×2, S3 ×2 |
  | the candidate test inverted (`is not None`) | 8 of 9 cases selected |
  | the return in the order the runs went | S3[plain] |
  | `NO_RUNNER`'s parenthesis changed | its whole-text pin |
  | each of rule 3's three sentences deleted | the rule-3 pin, each time |

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the branch-root half of the split, `os.path.isfile(os.path.join(root, f))`, and the round-1 🟡 2 comment that justified it | `compare_at_base`'s docstring, the paragraph *A file the base's tree lacks at the root is run alone, and that run decides it*; `templates/config.md` rule 3 |
| the docstring sentence "A file the base does not carry cannot fail there, so it reads `new` without a run" and the paragraph *The absent ones are separated before the run rather than after it* | the same paragraph, which keeps round 1's 🟡 4 reason |
| `NO_RUNNER`'s parenthesis naming one kept form | `NO_RUNNER`, naming both; its pin in `tests/test_the_seal_is_taken_once_by_the_sealer.py` |
