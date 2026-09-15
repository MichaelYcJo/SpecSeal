<!-- seal/specs/1789445605-the-broad-gate-row-runs-unchecked-and-is-never-asked-for/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A `Broad gate` row written the way every command in every document here is
  written — wrapped in backticks — could earn the stamp over a suite that
  failed.** In a shell, backticks are command substitution: the checks run
  first, their exit status is thrown away, and whatever they *printed* is then
  executed as a command. Measured on the same content: unbackticked it exits
  1, backticked it exits **0**, with the failure still on the screen. The gate
  read that 0, wrote the cell and drew the seal. It now looks at the row
  before handing it to a shell and refuses three forms outright — the whole
  command wrapped in backticks, the whole command wrapped in `$(…)`, and a
  trailing `&`, which backgrounds the line so the shell answers 0 before any
  check has finished. Exit 2, nothing run, and nothing repaired: the message
  names the form, quotes the row as written and shows it as meant, because a
  value silently fixed leaves the file still wrong and teaches the next person
  that the way they wrote it was right. Everything else a shell command line
  can hold stays legal — the row is an arbitrary command line by design — and
  `templates/config.md` now lists what is refused and what is not, each with
  its reason. **An `&` that is not the last character stays legal**, with what
  it costs written beside it: the check before it is backgrounded and may
  still be running when the gate stamps, and telling that `&` from a `2>&1` or
  one inside quotes needs a shell parser the row is designed not to have.
  (#402)
- **A pipe in that row silently loses every row written below it.** This is
  not new and it is now written down. A cell of the config table ends at the
  first `|`, escaped or not, so a `Broad gate` row containing a pipe stops
  being a row — and the reader stops there, so a `Record language` or
  `Commit and pull request language` line underneath it is invisible and
  falls back to its default with nothing reported anywhere. The gate reports
  the row as *absent*, which is true and is not the cause. The template says
  so beside the promise that a pipe is legal, and first setup now refuses to
  propose a candidate carrying one — which matters because the first place it
  looks for candidates is the CI workflow, where a pipe into `tee` is
  ordinary. (#402)
- **The one value only a person can write was the one thing nothing ever asked
  for.** There is no default for the `Broad gate` row, on purpose: what the
  seal covers is exactly the command a person chose. But no question ever
  reached a person — it arrived as the gate's refusal, after the review rounds
  had settled, which is the last moment available and the one where whoever is
  there has every reason to answer it themselves. That is what happened: a
  session met the refusal, ran four candidate commands, picked one, wrote the
  row and mentioned it afterwards. First setup now asks for it in the same
  question it already asks the mode in, so the prompt budget is unchanged. It
  asks as a **proposal** rather than a blank — candidates read off the
  repository's own CI workflow, its `bin/` runners, its package manifest and
  its `Makefile`, each offered with the file it came from, and nothing
  guessed — with a decline that says what declining costs. (#401)
- **How to choose that value is written down now, in one place.** The row has
  never had a criterion. Three rules: a check that is red repository-wide for
  reasons unrelated to any branch does not belong in it; a command that
  *fixes* the tree is not a gate command, because a gate that changes the
  answer while reading it can only come back green; and the suite runner comes
  first, because the base comparison re-runs what stands before the first
  `&&`. Only the third was written anywhere, and it was written in two places
  — it is folded into the one owner rather than copied into a third. (#401)
- **A session that meets the refusal is now told to bring it to a person.**
  The absent-row message used to open *write the repository's own broad
  command into it* and print the row to type, which asked the one party that
  may not write it. It says whose the row is and names `/specseal:config`,
  and the sealer and the review orchestrator both say the refusal goes back to
  a person and the pull request stays a draft until it is answered. (#401)
