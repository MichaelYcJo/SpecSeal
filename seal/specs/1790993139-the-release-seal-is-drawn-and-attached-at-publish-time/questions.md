# 1790993139-the-release-seal-is-drawn-and-attached-at-publish-time — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**This run is unattended, and nobody is left to ask** (`routing.md`:
`Automation` yes, `Answer pressed` automation). Each row a person would
otherwise answer is **decided by the frame**: the answer is written in, the
build proceeds on it, and the owner can overturn it by opening what the
grounds name. Nothing in this file blocks the build.

**What the tickets left open and the tree answered.** These are not rows,
and nobody needs to reopen them:

- **Where the seal goes in the note.** It replaces the `### 📊 At a glance`
  table, and the fallback keeps the table as it is today. Owner, #718's first
  comment.
- **The success-path shape.** Heading kept, image with alt text, one line of
  counts beneath. This is 0.17.0's hand edit, read with `gh release view
  v0.17.0`.
- **The drawing.** `compose` → `block` → one rectangle per cell, 14 × 28 px,
  font size 22, bold on line 1, at `DEFAULT_SCALE`. Owner, #718's last
  comment, and the hand-drawn script.
- **Who may import Pillow.** Nothing under `hooks/` or `skills/`.
  `CONTRIBUTING.md` §*Running the checks*: *the gates themselves are
  stdlib-only*.
- **Whether a new `.github/scripts/` file is held to the floor.** It is:
  `tests/test_a_script_says_which_interpreter_it_needs.py#shipped_python`
  excludes only `tests/` and `seal/`.
- **The label column.** It is fixed at eight by `seal_stamp.letter`'s
  `{label:<8}`, so the owner's *`deferred` set the column* holds only because
  `deferred` is exactly eight characters. A fixed label set of eight or fewer
  pins it.
- **Whether `settle --retire` can remove this release's round records before
  the tag.** It cannot. `docs/release-checklist.md` §2b retires released work
  items, in a separate later pull request.
- **The plugin's longest exception class name.** `NoMutationDefined`, 17
  characters, not the 28 #722 and round 3 state.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | #718's body says nothing at publish time reads a file in the tree. Do the chain rows read the round records at the tag anyway? | a person | **(a) Read them**, through `hooks/routing.py#item_dir` and `#rounds` and `chain_check.py#verdict_table` and `#verdict_of`. That reproduces 0.17.0's 27 rounds exactly, and #715 moving the records turns the rows into `not read`, never a wrong number. **(b) The pull requests' bodies**, as #718's table says. Measured on 0.17.0's eleven pull requests: no `specs/` marker, and the `## Review chain` sections are prose no template or checker holds. **(c) Capped alone** loses what *What it says* lists | **(a).** The ticket's reason for keeping out of the tree was `seal/releases/` (#715), which this does not read. The owner's own last comment names the round records as where the 0.17.0 counts came from | decided by frame |
| Q2 | Where does the suite count come from? | a person | **(a) A run at the tag in the `seal` job, counted from `--junitxml`**: the tag's own tree, at the cost of minutes of runner time after the note is out. **(b) A JUnit artifact uploaded by `test.yml`**: a race with the `push: main` run, and a tree that is not the tag's. **(c) A CI log**: the owner called it not a stable API | **(a).** A seal is drawn only when that run passed | decided by frame |
| Q3 | Where does the PNG dependency live, and at which version? | a person | **(a) Test-and-release only, `pillow==12.3.0` pinned once in `run_tests.py#PACKAGES`**, as `markdown-it-py` is (#667), so the pixel pin runs the same way locally and on CI. **(b) Workflow only**, with the pin skipped locally. **(c) A stdlib PNG with a hand-made font** | **(a).** 12.3.0 is PyPI's newest on 2026-10-03, requires Python ≥ 3.10, and ships cp312 wheels for all three CI platforms | decided by frame |
| Q4 | Does the seal run on a release the run did not create (a re-run, a re-pushed tag)? | a person | **(a) No**: `publish_release_note.py` writes `created`, and the `seal` job runs only on `true`. **(b) Yes, if the generated glance table is still there** | **(a).** It is the same line as *It never republishes*. A seal can still be drawn by hand with `DRY_RUN=1` and `gh release upload` | decided by frame |
| Q5 | When the suite fails at the tag, what does the release get? | a person | **(a) Today's note, a green job, and a `::warning::` naming the failure.** **(b) A red job**, which #718's fallback rule and the first goal both refuse for a release that has already shipped. **(c) A NOT SEALED drawing**, which is the gate's form for a branch, not a release's | **(a)** | decided by frame |
| Q6 | What happens to a value wider than the panel's value column (23)? | a person | **(a) It moves to a continuation row**, for example `S skipped` under `P passed`. **(b) A shorter wording** that changes the 0.17.0 look for every release | **(a).** Only the suite row can overflow: `7003 passed, 66 skipped` is exactly 23 | decided by frame |
| Q7 | #722: what is the cap, and where is it applied? | a person | **(a) `NAME_CAP` = 40 UTF-16 units, at write in `record` and again at read in `describe`, which also re-caps `message`.** Two gates come to about 951 by arithmetic, and the smith measures it. **(b) At write only**, which leaves a record from an older plugin unbounded (`read_record`'s docstring). **(c) Count it into the reserve**, which cannot bound a foreign name | **(a).** No marker is added to a cut name, matching how `first_line` cuts text | decided by frame |
| Q8 | What does a chain row show when its source cannot be read? | a person | **(a) The value `not read`, with the row kept.** **(b) The row dropped**, which reads as *none*. **(c) The whole seal falls back** | **(a).** The suite and the two counts are the seal's claim, and only their absence falls back (S2) | decided by frame |
| Q9 | Does every browser draw an image served as `application/octet-stream` from the release-download URL? | a measurement | Open 0.18.0's release page in Chrome, Firefox and Safari once. Read so far: the final `200` carries no `nosniff` (measured 2026-10-03 on 0.17.0's asset), Fetch's `nosniff` blocking covers script and style only, and an `<img>` ignores `content-disposition` | The URL is kept. The counts line and the alt text carry every number if it does not draw | ⬜ |
| Q10 | The deferred rule gives 12 distinct issues on 0.17.0's tree; the owner's hand count was 13. Which issue is the 13th, and does the rule miss a verdict shape? | a measurement | Phase 3 lists the twelve (`#313 #701 #704 #706 #708 #709 #710 #712 #713 #716 #720 #721`) against 0.17.0's round records and the PR bodies' deferred lists, and records the difference in `phases/phase-3.md` | The rule stands as specified (S10). A verdict shape it misses is fixed in phase 3 and pinned | ⬜ |
| Q11 | Which font does `ubuntu-latest` give `font()`: DejaVu Sans Mono, or Pillow's bundled default? | the work | Phase 2's pixel case prints the font it used on CI's ubuntu leg. The first live run at the tag logs it again | The chain falls through to `ImageFont.load_default(size=22)`. The pin samples colours away from the glyphs, so it holds for any font | ⬜ |

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
