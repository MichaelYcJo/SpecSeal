# the deferred sentences and pins — questions for the planner

<!-- seal/specs/1790381329-the-deferred-sentences-and-pins/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row needs a person, and none blocks the build.** Every row below has a
default the build proceeds on.

**Judgments the issues left open that the tree answered.** Listed so nobody
reopens them; the grounds are in `spec.md` and `plan.md`'s Alternatives table.

- #610: exit 2 for both scripts. `payload_meter.py` already uses 2 for its
  other "nothing ran" case, and #590's CHANGELOG entry fixes the class.
  `seal.py`'s docstring promise of *no third* code is rewritten, not kept.
- #610: the class under `skills/` is exactly the issue's two scripts,
  enumerated by construction (three loader shapes, bare sibling imports
  included). `hooks/`, `.github/scripts/` and `evidence_check.py` are out,
  each with its grounds.
- #612: the statement is *both places*, not *the base's tip*; eleven places
  and two test docstrings, not seven; `docs/one-root-by-lifetime.md` and its
  Korean edition are false, not only incomplete.
- #613: seven ledger rows drift, not two. No new case for a docstring.
  `docs/round-record-spec.md` line 96 and `docs/review-handoff-protocol.md`
  line 274 are not twins.
- #615: S4 is not pinned as silent.
- #616: `as_cmd_expands`'s *`CD` and `__CD__` are in no environment* and
  `templates/config.md` §*Broad gate* are twins and are corrected; the
  config sentence's pinned needle changes with it.
- Every item gets a pin on the finding's own example except #613 (a
  docstring, outside contract §14's list).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | How many anchored ledger rows carry no id `ROW_ID` reads, at the build tip? The round counted 280 of 800 (35.0%) at its tip; the tree says *about 37%* and *298 of about 800* | a measurement | one probe (`test_tmp_*`, deleted after, contract §7): import `survivor_check.ROW_ID` and the ledger checker's `ANCHOR_RE` the way `survivor_check.py#evidence` loads it, read `seal/ledger.md`, `seal/releases/*.md` and `seal/ledger/*.md` through `unverified_check.py#live_lines`, count live table rows with at least one anchor, and those `ROW_ID` does not match. The tree cannot answer it because the count moves with every release fold | the measured figure goes into all three #615 statements, with the tip it was taken at in phase 5's record. If the probe's total differs from the round's 800 by more than the rows folded since, the phase record says so and the figure is still the probe's | ⬜ |
| Q2 | Where does `cmd.exe` resume scanning after an undefined `%NAME%` — and does `as_cmd_expands` agree? | a measurement | only a run of `cmd.exe` answers it, and this work item runs on macOS. The tree cannot answer it: the round read it from memory and executed nothing on Windows. A Windows-only case would first run at the pull request, unattended | not modelled and not claimed: the docstring says so, and `overview.md` `## Not verified` carries the row with its answerer, *a Windows run of `cmd.exe` — whoever next changes the broad gate's cmd.exe path* (#616's own *Who acts*) | ⬜ |
| Q3 | Do C's `seal/releases/*.md` re-stamps conflict with B's at the squash? (B's frame, 6fc5532c, leaves both READMEs unedited, so the README pair is not a surface any more) | the work | unknowable at framing time: which rows B's phase 3 re-stamps is what B's `evidence-check` names after its own edits | C squashes last. If a file conflicts, merge the release branch in (never rebase), resolve ledger files hunk by hunk, run `evidence-check`, and re-run only the narrow cases the resolved files touch | ⬜ |
| Q4 | Which invocation of `payload_meter.py` is the smallest that reaches `_session_cost` without failing earlier (argparse, the tree walk, a missing transcript)? | the work | `main` calls `measure`, which reaches `calibration_of` only with `--calibrate`; whether `measure` reads the transcript or the agents first is the next line to read, and the phase that writes the row reads it | `--calibrate <an existing empty file>` plus whatever `--root` keeps `measure` from failing first; the row's comment names why, as the other rows' invocations are explained in the module docstring | ⬜ |
