# the encoding walker judges a class opener and a shadowing local (#762) — questions for the planner

<!-- seal/specs/1791119068-the-encoding-walker-judges-a-class-opener-and-a-shadowing-local/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row here needs a person.** The judgments #762 left open were answered
from the tree, and `spec.md` §*Decisions* holds each with its grounds, so
nobody reopens them:

- D1 — 🟡 1 is closed for its class by separating method rows from function
  rows, not by excepting the one key round 3's paste-ready fix excepts.
- D2 — 🟡 2 is closed by removing the bare-name excuse, not by narrowing it to
  `os` and `webbrowser` (K2; round 2's reviewer had already called the
  resulting over-report acceptable).
- D3 — ⬜ 3 is in scope as a docstring sentence; tracing `/` and `.joinpath`
  is out.
- D4 — a local shadowing an imported module's name in a narrower scope is
  stated in *What no row can hold*, not traced.
- D5 — #741's released `spec.md` is not edited; this work item's K1 row
  supersedes its line 86 at the fold.
- D6 — round 3's paste-ready fixes are re-derived and every new case is seen
  red first.
- ⬜ 4 is widened from round 3's three `dbm` names to the class enumerated by
  construction (spec §*The classes*, C3).

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| M1 | Does the tree hold a bare unimported receiver whose `.open()` the bare-name excuse was keeping green? The framer's grep found none (read, not executed); why the tree could not settle it: only the repository case, run once `owner`'s bare-name branch is removed, executes the claim over every tracked `.py` | a measurement | none found: D2 stands. One found: the build keeps round 3's two-name branch (`os`, `webbrowser`) instead, records the divergence in `overview.md`, and the review judges it | D2 — delete the branch; phase 2's run of the repository case answers it | ⬜ |
| M2 | Which standard-library modules carry a module-level `open` on 3.12, the suite's floor? Why the tree could not settle it: the framer ran the construction on 3.13.5 and checked presence on 3.14.3; `aifc` and `sunau` exist on 3.12 alone and `dbm.gnu` was absent from both local builds | a measurement | the 3.12 run matches C3: add the eight names. It shows another: add it with its grounds and say so in `phase-2.md`. It shows one of the eight opens locale text: leave it out and say so | add the eight C3 names | ⬜ |
| W1 | The exact shape of the split in D1 — a second table keyed by receiver class, or positions passed into `judge_opener` — and how S3's test names the table it reads. Why the tree could not settle it: either shape satisfies D1 and S3, and which reads better is visible only once the code is open | the work | either; the constraint is that the kinds `zipfile.Path.open()` and `<expr>.open()` do not change and that S3 is red against the base's `OPENERS` | the builder's choice, recorded in `phase-1.md` | ✅ decided by phase 1: a second table, `OPEN_METHODS`, keyed by what `owner` resolves the receiver to and read by the `.open` branch alone; S3's test reads every table `judge` tests `target in` from `judge`'s own source, red at the base naming `OPENERS['zipfile.Path.open']` (`phases/phase-1.md`) |

**`Who can answer` takes one of three values and nothing else.** They were one
shape on the page before this, and #84's second comment measured all three
inside a single run's four rows.

- **a person** — what the product should be, or a value somebody has to be
  accountable for. This is the file's stated purpose, and the only kind of row
  that blocks the build.
- **a measurement** — a probe, a command or a count settles it, so asking a
  person is the wrong instrument and queueing it behind one wastes a round
  trip.
- **the work** — unknowable at framing time. The phase that meets it decides
  it there and records a divergence row; it does not travel back to the
  framer.

**The framer opens rows and does not own their answers.** The `Status` column
is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
