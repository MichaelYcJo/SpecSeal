- **`seal` and `payload-meter` copied without their siblings exit 2 with a
  sentence (issue #610).** `seal` imports two files from the plugin's
  `hooks/` directory, and `payload-meter --calibrate` loads
  `session_cost.py` from beside it. Copied on their own, both died with a
  Python traceback at exit 1, which reads as a finding rather than a broken
  copy. Each now names the missing file's path and what it is for, and
  exits 2, the code 0.15.4 gave the other shipped scripts for the same
  case. `seal`'s documented exit codes gain the 2. A caller testing for a
  non-zero exit is unaffected.
- **The settle skill names both headings a kept directory can appear under
  (issue #611).** Once `--released-at` has moved past the commit your
  branch started from, `settle` lists a directory whose closure has not
  reached the base under *kept: the closure has not reached <base>*. The
  skill named only the other wording, *kept until the closure reaches
  <base>*. Both are named now, and the report's summary line is held by a
  case.
- **`unverified-check --baseline` says where its comparison lands in CI
  (issue #612).** It reads `git merge-base <ref> HEAD`. On a branch
  checkout, such as a local run or the broad gate's, that is where the
  branch started. In CI it is the tip of the base branch, because a pull
  request is checked out already merged into the base. The command's help,
  its docstrings, both hygiene workflows, the verify skill, both READMEs
  and both editions of `docs/one-root-by-lifetime` said only the first and
  placed it in CI. Two of them said CI never compares at the tip, which was
  false. What the check refuses is unchanged.
- **The survivor sweep states which corrected ledger rows it leaves silent
  (issue #615).** Its docstrings and `docs/review-chain-spec.md` described
  the two rules that keep a corrected row measured as alternatives. That
  called rows silent that the sweep reports. They now say a row goes silent
  only when both fail: its id does not name it, and no live row cites what
  it kept. About 35% of this repository's ledger rows carry no id, measured
  at this branch. A case now holds the id rule's direction: a row corrected
  and split into two rows under its id stays measured.
- **The broad gate's `cmd.exe` expansion says what it models (issue
  #616).** Before it decides whether a command name starts in a directory,
  the gate expands a plain `%VAR%`. It takes an environment variable named
  `CD` over the directory it would compute, as `cmd.exe` does. It leaves a
  substring or substitution such as `%VAR:~0,2%` as written. Its docstrings
  and `templates/config.md` §*Broad gate* claimed to expand the way
  `cmd.exe` does, which covered neither. They now name the plain form, the
  `CD` precedence and the substring limit, and cases hold all three.
