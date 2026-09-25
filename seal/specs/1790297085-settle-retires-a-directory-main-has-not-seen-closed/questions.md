# settle refuses a retirement the release's base has not seen closed — questions for the planner

<!-- seal/specs/1790297085-settle-retires-a-directory-main-has-not-seen-closed/questions.md -->

**The owner pressed `automation` for the whole milestone, so nobody answers
before the build. Every row below has a default the build proceeds on, and
none of them blocks it.**

**What the tickets left open and the tree answered — listed so nobody
reopens them:**

- **Which base `settle` compares against (#602).** `--released-at`, default
  `origin/main`, compared at the merge base of that ref and `HEAD`.
  `skills/settle/SKILL.md` §1 already defines `--released-at` as the branch
  the release merges to, and both CI readers compare at that merge base
  (`unverified_check.py#main`, `chain_check.py#main`).
  `docs/one-root-by-lifetime.md`'s decision row already says the predicate is
  asked of the merge base for `settle`, which is false today and true after
  this work. No new flag.
- **What the refusal names (#602).** The base, as `unverified_check.py#base_label`
  spells it, and every row open there, under a heading of its own. Exit 1,
  the code `settle.py`'s docstring already gives a refused retirement.
- **Whether the marker arm needs the same check (#602).** No. Both CI readers
  excuse a folded directory before asking about its rows, so a fold cannot
  turn the release pull request red this way.
- **Which exit code (#590).** 2. In each of the three scripts, 2 already
  means *the input or the tree was unusable and nothing was done*, and 1
  means a finding or a refusal. `round_record.py`'s docstring documents 1
  for this case and argues why; that paragraph is what #590 overturns.
- **Whether `chain_check.py` needs the fix (#590).** No. Measured 2026-09-25:
  copied alone, it exits 2 with a sentence, because `chain_check.py#main`
  catches the load. The ticket's `~812` coordinate is the function, and the
  process-level claim does not hold. Not editing it also removes the merge
  with work item A.
- **Which other loaders are in the class (#590).** None beyond the three.
  `spec.md` §Scope *Out* lists every by-path loader and why each is outside.
- **What counts as a `## ` line (#586).** Exactly what ends a section for the
  two release readers: `line.startswith("## ")`. A `###` line, a bare `##`
  and an indented `## ` are gathered. A `## ` inside a fence is refused,
  because neither reader knows fences.
- **Which fragments are checked (#586).** The ones this run would gather. One
  already in `CHANGELOG.md` cannot be un-shipped by refusing the release.
- **Whether `--check` or the suite also refuses (#586).** Not in this
  release: the milestone adds no gate. Carried as Q3 below.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | For each of the four scripts in the class case, what is the smallest invocation that reaches the loader when the script is copied alone? | the work | `round_record.py` loads at import, so any subcommand reaches it; `settle.py` and `fold_check.py` load `hooks/optin.py` early in `main`; `chain_check.py` needs `--baseline` before it loads. Phase 1 meets it and writes it into `phases/phase-1.md` | The framer's probe invocations in `spec.md` §*Data & interfaces* | ✅ Answered 2026-09-25 by phase 1, on the default: `round_record.py` with no arguments (it loads `chain_check.py` at import, before argument parsing); `fold_check.py --root <empty dir>` and `settle.py --root <empty dir>` (each loads `hooks/optin.py` before it reads the root); `chain_check.py --baseline HEAD --root <empty dir>` (`--baseline` is required, and the readers load right after parsing). The class case in `tests/test_a_script_copied_alone_exits_2.py` runs exactly these |
| Q2 | Does an existing case in `tests/test_settle_reads_before_it_removes.py` expect a directory to be retired while its closure sits only in the working tree? | the work | If one does, it encoded #602 as correct. Phase 2 commits the fixture's closure to the base the case names, and does not weaken the refusal to keep the case green | Commit the closure in the fixture; record the case by name in `phases/phase-2.md` | ✅ Answered 2026-09-25 by phase 2: no. None of the 111 cases that stood before it expected that; `moment()` commits every overview it writes and the fixture runs at `HEAD`, so the base holds the closure in each, and all 111 stayed green with the refusal unweakened. No fixture changed |
| Q3 | Should a later release catch a fragment carrying a `## ` line at the fragment's own pull request — through `gather_changelog.py --check` on every base, or a suite case over every `seal/specs/*/changelog.md` — rather than at release preparation? The tree cannot answer it: it is a new check, and whether the earlier catch is worth one is the owner's trade | a person | **(a)** No: release preparation stops, and the fix is one pull request into the release branch. **(b)** Yes, in 0.16.0 or later: a new check, filed as its own issue | (a) for this release. The orchestrator may file (b) as an issue; this work item builds nothing for it | ⬜ |
