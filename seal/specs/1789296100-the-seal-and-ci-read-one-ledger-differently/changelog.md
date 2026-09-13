<!-- seal/specs/1789296100-the-seal-and-ci-read-one-ledger-differently/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A ledger run that comes back exit 1 now says that the run which decides
  would refuse the tree.** Three readers ran `evidence_check.py` over one tree
  and graded it differently, and nothing said so. `evidence-check` — the
  command every document names — takes drift as exit 1; CI's `ledger` job runs
  the same script and renders that as a warning the job passes; `broad-gate`
  runs it with `--strict`, where drift is exit 2 and the branch comes back
  `NOT SEALED`. So a session could run the documented command, read exit 1,
  and have no way to learn that the deciding reader was looking at the same
  tree as a refusal — and running the documented command more often never
  found it, because the documented command is not the one that decides. The
  lenient run now prints which reading it took and what `broad-gate` would say
  instead. **Exit 0 and exit 2 print nothing new**, because every reader grades
  those alike, and a line that prints on every run is a line people learn to
  skip. The three readers stay as they are: a branch mid-flight drifts
  legitimately, the gate runs once at the end over a tree nobody is still
  editing, and the disagreement was the design — not saying so was the defect.
  (#354)
- **The line's condition is the run's own answer, not a second copy of the
  grading rule.** The four `return` statements that ended `evidence_check.py`'s
  `main` are now one `exit_code()` function, and the print fires on `code == 1`.
  A predicate written beside a rule is a predicate that can drift from it; this
  one cannot. No exit code moves in any reader, no flag is added, and the
  `evidence-check` wrapper pair is untouched — the CI step reads the exit code
  and never the text, so the sentence reaches the job log with the step
  unchanged.
- **Five documents stopped describing one reader of three.** The
  `evidence-check` skill gains a table holding all three readers side by side;
  both READMEs' ledger paragraphs, `CONTRIBUTING.md`'s check list and the
  `ledger` job's own comment each name `broad-gate` and `--strict` beside the
  exit code they describe. A case holds the printed sentence against
  `broad_gate.py`'s ledger call site, against the wrapper's pass-through and
  against `seal_stamp`, so the claim the line makes about another file cannot
  go stale in silence.
