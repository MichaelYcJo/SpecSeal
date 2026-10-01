# arm-check reads a run that measured nothing as a kill — questions for the planner

<!-- seal/specs/1790823441-arm-check-reads-a-run-that-measured-nothing-as-a-kill/questions.md
— decisions only a human can make, extracted so nothing ships on a silent
assumption. Before adding a row, check the inheritance rule: if policy is
silent but existing behavior answers it, inherit and record — only genuinely
NEW rules belong here. -->

**No row here blocks the build.** The ticket and the spawn left the
judgments below open, and the tree answered each of them. They are listed so
nobody reopens them, each with where its grounds are, so a reviewer can
overturn one by opening the same place. What survived judging is the table
after it: one assumption written down for a person, two measurements, and
two decisions the work makes where it meets them.

## Judgments the tree answered

| # | Judgment | Answer | Grounds |
|---|---|---|---|
| J1 | Does `arm-check`'s refusal take the sibling's verdict word and exit, or its own? | `no baseline`, exit 2. The word is the sibling's because the fact is the same (the cases are not green against the unmutated file, nothing was written); the exit is `arm-check`'s own existing code for a run refused before measuring | `arm_check.py#main`'s `--timeout` guard exits 2 through `parser.error`, pinned by `test_a_negative_bound_is_refused_rather_than_measured`; `tests/test_one_word_one_meaning.py`'s rule against a second spelling for one fact; `plan.md` §Alternatives F and G |
| J2 | Does *report-only, exit 0 either way* forbid the exit 2? | No. That sentence is about a **survivor** — the SKILL section says the open decision is *whether an unwatched arm should fail a run* — and a refusal before any mutation is not a survivor. `test_the_checker_is_report_only_and_exits_zero_over_the_real_module` keeps pinning exit 0 for a measured run with a survivor | `skills/verify/SKILL.md` §arm-check, last paragraph; `tests/test_arm_check.py:1024-1047`; spec S7 |
| J3 | Are a baseline timeout and a baseline spawn failure `no baseline` too, or their own verdicts as in `mutation-check` (`timed out … before the mutation was written`)? | `no baseline`, with the cause in the reason. `arm-check` has no run-level verdict vocabulary — a timeout and an `OSError` are per-pair *reasons* in its report — so one refusal naming the cause is the shape its output already has | `arm_check.py#run_arms:900-915` (the two `except` arms write reasons, not verdicts); `plan.md` §Alternatives H |
| J4 | Once per call or once per arm? | Once per `run_arms` call with `--tests`, before any write, `--only` or not, module with no arms or not | `plan.md` §Alternatives C and L: the module is unchanged between arms, and *runs once per `--tests` call* is one sentence to state |
| J5 | Raise, or return a third value? | Raise `NoBaseline`, carrying the cause and the command's output | `plan.md` §Alternatives E: a third return value a caller ignores is the defect one level up; every existing caller unpacks two |
| J6 | Is the baseline bounded, and by what? | By the same `timeout` as an operator's run, and S4 pins it | #641's round 2 🟡 10 found the sibling's baseline bound unpinned and SURVIVED a mutation to `None`; the help text already says what the bound reaches (#313) and gains that it covers the baseline |
| J7 | Is the command's output printed on `no baseline`? | Yes, after the verdict line — it is the one run whose cause a person has to read to act (pytest's *no tests ran*, *file not found*). A kill's and a survival's output stay unprinted | #641's round 2 ⬜ 12: `no baseline` there dropped the exit code and the sentence *Nothing was written* was pinned by no case; both are in the verdict line here and both are pinned (S1, §14) |
| J8 | Where is a relative prefix resolved? | Against the cases' working directory, `run_arms`'s `cwd`, passed to `clear_bytecode_cache(path, cwd=…)`. `None` keeps today's behaviour for a caller that passes nothing | spec M1: CPython 3.14.4's `cache_from_source` joins `sys.pycache_prefix` as given, so a relative prefix is the importing process's cwd plus the prefix; spec M2: today's join never sees `cwd`; `plan.md` §Alternatives I, J, K |
| J9 | Is `main` catching every other exception (the sibling's 🟡 3) in scope? | No | In `mutation-check` exit 1 is `SURVIVED`'s code, so a traceback read as a verdict; in `arm-check` exit 1 is no documented verdict (0 measured, 2 refused), so it does not. spec §Scope, out |
| J10 | Are #312, #313, #314, #687 in scope? | No; the ticket keeps them out and the tree agrees each is a different class in the same file | spec §Scope, out, one line each |
| J11 | Which existing cases change, and are any retired? | Five are rewritten keeping every assertion (spec M5, §Scope 5); none is retired; the report-only pin and the kill/survive pin are untouched | `tests/test_arm_check.py` read at the lines spec M5 names; the per-arm timeout, spawn failure and failed-restore paths all still exist after the baseline |
| J12 | Is `arm-check` a gate under `CONTRIBUTING.md` §*What a change to a gate must carry*? | No, inherited from work item `1790690762`'s `spec.md`; the failure direction (refuses more) and the prompt budget (zero) are stated anyway in spec §*Failure direction* | that spec's Grounding row; `skills/verify/SKILL.md` §arm-check |
| J13 | Changelog heading | `### Fixed` | A command printed `killed` for arms no case ran against; nothing refuses a measured run afterwards |
| J14 | Does `docs/the-broad-gate.md`'s arm-check statement need an edit? | No. Its claim (arms enumerated, mutated, survivors reported) and its `Enforced by:` case are unchanged and green | `docs/the-broad-gate.md` §*A check that cannot fail is not a check*; spec S6 |

## The residue

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | When #641's branch and this one are both on `release/v0.17.0`, `mutation_check.py`'s three `clear_bytecode_cache(path)` calls (its `mutation_run`, lines 318, 335, 351 at `53659481`) should pass `cwd=cwd` to get the relative-prefix fix, which closes that item's own ⬜ 7. Which branch carries the one-line change? **Not blocking**: either answer leaves this item's code as planned, because the new parameter defaults to today's behaviour (S11) | a person — the repository owner, as the orchestrator of both branches | *The branch that lands second* adds the three keywords in its merge-resolution commit, with its narrow module run. *A follow-up commit on `release/v0.17.0`* after both squash, with the same run. *Leave it*: `mutation-check`'s mirror stays the process's cwd and #641's ⬜ 7 stays open in its `overview.md` | the branch that lands second carries it, and says so in its hand-back. Written here so the merge does not forget a file this tree does not hold | ⬜ |
| Q2 | Does the documented form `--tests "bin/test tests/test_chain_hooks.py -q -k <a name no case has>"` reach `no baseline` with `exit 5` in the reason — that is, does `bin/test`'s runner (`.github/scripts/run_tests.py`) propagate pytest's exit code unchanged? S1–S3 model the three shapes with `sys.exit(N)` probes, which is all the CI grammar legs can run; this is the same fact through the wrapper a person actually types | a measurement — one command by the build in phase 1, or by the reviewer | Propagated: the reason names `exit 5` and the printed output shows pytest's *no tests ran*. Not propagated (the runner rewrites the code): the baseline still refuses on a non-zero exit, and the reason names the runner's code; the hand-back says so and the SKILL sentence does not promise pytest's number | the baseline reads any non-zero exit as not green, so nothing in the code depends on the answer; it decides only how the SKILL sentence words the example | ✅ measured 2026-10-01 in phase 1: `bin/arm-check hooks/review-history-guard.py --tests "bin/test tests/test_chain_hooks.py -q -k specseal_no_case_has_this_name"` printed `no baseline: exit 5. …` with pytest's `no tests ran in 0.71s` below it and exited 2, the guard's sha256 unchanged. The runner propagates the code. The SKILL sentence says *exit non-zero* and names no number, so it promises nothing either answer breaks (`phases/phase-1.md`) |
| Q3 | The baseline's cost on the real module: `arm-check hooks/review-history-guard.py --tests "bin/test tests/test_chain_hooks.py -q"` before and after, wall clock, for the ledger row R1's notes. The framer runs nothing | a measurement — the build, at phase 3, on the machine it reports | One run added to 61: the figure is roughly one sixty-second of the run plus the runner's start-up. The row says the number, the date and the machine, and does not call it small | the row carries the two timings or says they were not taken and why | ⬜ |
| Q4 | The exact wording of the verdict line beyond the three pinned pieces (`no baseline:`, the cause as the command gave it, *Nothing was written and no arm was measured.*), whether a green baseline prints a line of its own, and whether the captured output is printed whole or tailed | the work — phase 1 decides and its phase record says what was chosen | Whole output: a long suite's output scrolls, but nothing a person needs is cut. Tailed: shorter, and the line that names the cause may be above the cut. A green-baseline line: one more line per run that says the run was green, which the report's `arms measured` line already implies | whole output; no line on a green baseline | ✅ decided in phase 1 as the default: the whole output, stdout then stderr, printed after the verdict line; no line on a passing first run. The line reads `no baseline: <cause>. --tests has to pass against <module> as it is before anything is mutated, because a failure under a mutation says nothing about the mutation. Nothing was written and no arm was measured.` (`phases/phase-1.md`) |
| Q5 | The shape of the probe that is green against the unmutated module and hangs only on a mutated one, for the two rewritten timeout cases (spec §Scope 5): compare the module's text to a copy the case wrote, or import it and sleep on a changed return value | the work — phase 1 decides; the probe's docstring says why that shape | Text comparison: hangs on every mutation of either arm, including `remove` of the unwatched arm, which an import-based probe would not notice. Import-based: closer to a real suite, but `remove` of `flag` leaves `classify("example.com", …)` unchanged, so one pair would not hang and the case would stop pinning *every pair times out* | text comparison against a copy under `tmp_path` | ✅ decided in phase 1 as the default: `HANGS_ON_A_MUTATION` compares the module's bytes with a copy and sleeps on any difference, run with `-S`, under `HANG_BOUND = 1.0` rather than the old 0.3 because the passing first run has to finish inside it (`phases/phase-1.md`, `overview.md`) |

**`Who can answer` takes one of three values and nothing else.**

- **a person** — what the product should be, or a value somebody has to be
  accountable for. The only kind of row that blocks the build, and Q1 is
  written so that it does not: the assumption is on the row, and a different
  answer changes a file this tree does not hold.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument. Q2 and Q3.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records the choice in its phase record. Q4 and Q5.

**The framer opens rows and does not own their answers.** The `Status`
column is ticked by whoever answered, never by whoever asked. Answered rows
feed back into the phase records or the ledger notes before this
directory's work merges.
