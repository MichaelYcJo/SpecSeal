# 1791180640-a-base-run-that-collects-only-its-files-is-the-only-measure — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Decided from the tree, so nobody reopens them.** The owner's decision left
"how to know a run collected nothing but its handed files" open, and the
spawn left five more judgments open. The tree and measurement answered each:

- **The mechanism** is one whole-row collection pass per file the base
  fails, `--collect-only` carried in `PYTEST_ADDOPTS`, read for one trailer
  and a listing of that file alone (`spec.md` §*The class*, `plan.md`
  Alternatives E). The report-field candidate lost because `file` is where a
  test is defined (Alternatives B). Exit and collection counts alone lost
  because they cannot show whose a failure is (Alternatives C, H).
- **The JUnit report stays**, read for counts only. It is the only thing
  that shows which prefix reached a pytest that took the gate's arguments,
  and its outcome does not depend on what a test prints (M10, M11) or on a
  wrapper's exit code (Alternatives C).
- **The multi-runner count survives inside the proof pass.** It counts
  pytest sessions under collection, where no test runs and so no inner run
  can print. That closes #807's two members and round 2's own `--junitxml`
  member without the first build's per-prefix collection pass
  (Alternatives D).
- **From the first build** this work keeps the report's append, its
  stale-path removal, its absolute path, the no-runner settle rule, its
  inner-run and dropper cases, and every probe layout as the regression
  corpus. It drops placement, the tree listing, the collection pass over
  prefixes, and the `UNPLACED` and NOTHING_TOGETHER reasons.
- **This repository's own row** is measured. `bin/test -q <file>` collects
  that file alone at the repository root (M13), so a file the base fails
  reads `failing on base too`.
- **The READMEs and the two agent definitions are not edited.** Each says
  `new?` means no run at the base measured the file, which stays true when
  measuring means collecting only that file (`spec.md` Scope 9).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | In a row that runs pytest more than once, where the base PASSES a failing file under the runner the gate reaches first, should the file read `new?` rather than `new`? Not answerable from the tree: the owner's decision of 2026-10-05 governs the permissive word only, and #789's own checkbox ("every candidate `new?`") predates it. The choice is which strict word a person sees, at a price in machine time, so it is a product call | a person — the repository owner | (a) **`new`, as at a3aa139a.** The proof pass runs only where the base fails a file, so a two-runner row's `new` can come from the wrong runner; it blocks, and the loop or the person then finds the file passes. (b) **`new?` for every failing file of such a row.** Costs one whole-row collection pass per comparison, on a passing base too, and states the row as unmeasured | (a): the frame builds (a), and (b) is a separate change if chosen | ⬜ |
| Q2 | Do Linux (`/bin/sh` as dash) and Windows (`cmd.exe`) give M1–M13's shapes: `PYTEST_ADDOPTS` reaching a runner inside `sh -c`, the inserted quoted file, the rest of a row after a `cmd.exe` cut, and the trailer and listing lines? The frame ran on macOS only | a measurement — CI's three-platform test job over phase 1's cases | — | the same as macOS; a red case on either platform is phase work, not a question | ⬜ |
| Q3 | Does any layout of the regression corpus give `failing on base too` where a3aa139a did not, other than S3–S5's named shapes? `spec.md` §*The class* argues none can, by construction; the layouts are what checks the argument | a measurement — phase 2's corpus run | — | none; a layout that does is fixed inside this work before phase 2 closes | ⬜ |
| Q4 | The two new reasons' constant names and exact wording, and which 0.18.2 cases move to FILES_ROW against asserting the beyond reason | the work — phase 1, which pins each reason whole and lists each case in `phases/phase-1.md` | — | meaning fixed by `spec.md` Scope 5 and S16; wording and names are phase 1's | ⬜ |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip. Measured: six probes at about three seconds each answered a row that
  had been written into the human batch, and they showed the ticket's own
  instruction was wrong.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked. Sorting
the rows this way is also what keeps the batch short enough to answer in one
sitting: two of the three kinds never needed a person at all.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
