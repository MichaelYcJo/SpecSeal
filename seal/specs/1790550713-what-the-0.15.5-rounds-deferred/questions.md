# what the 0.15.5 rounds deferred — questions for the planner

<!-- seal/specs/1790550713-what-the-0.15.5-rounds-deferred/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**No row needs a person, and none blocks the build.** The owner pressed
`automation` (`routing.md`), and every row below has a default the build
proceeds on.

**Judgments the issues left open that the tree answered.** Listed so nobody
reopens them. The grounds are in `spec.md` and in `plan.md`'s Alternatives
table.

- #626: `CHANGELOG.md` §0.15.5 and the gathered fragment of 1790381328 are
  not rewritten, although the issue lists the fragment as a copy to fix.
  `docs/review-chain-spec.md` says a released entry is not rewritten. This
  work's fragment carries the correction.
- #626: 1790381328's `spec.md` IS corrected in place, because `settle` folds
  a released spec into `docs/` and `survivor-check` reads it as live prose.
- #626: round 3's paste-ready bullet is amended, not pasted: "no `@` before
  its `#`" is false of `@alice#299@abcdef12`, which is named.
- #626: the pins owed are five, not three. `docs/a.md#1장@abcdef12` and
  `src/a.py#handler @abcdef12` are rule examples with no case either. A
  completeness case holds the docstring's rules section to the dicts.
- #625: the assertion after the first `close` stays `in (0, 1)`. The draft
  exit is already pinned by
  `test_pass_is_ticked_when_nothing_is_open_and_the_gate_is_the_flag`.
- #625: round 2's paste-ready comment is amended: the pair prints only
  under `fixed`.
- #625: the class has two instances, the issue's and the "Not `code == 0`:"
  comment in `test_a_fix_commit_carries_no_empty_code_span`. Every other
  sentence about the pair was read and holds (`spec.md` lists them).
- #625: five ragged lines, not three. `round_record.py#landing_values` and
  `unverified_check.py#main`'s `--baseline` help were left by the same
  range.
- The spawn prompt said 1790381329's directory holds only `changelog.md`.
  It holds the whole work item, and `rounds/round-2-report.md` is read from
  the tree, not from git history.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | What does a ledger run print for `docs/a.md#1장@abcdef12` and `src/a.py#handler @abcdef12`, each in a code span beside a good anchor? `TAKEN_UP`'s case asserts `f"MALFORMED {shape}  "` in stdout | a measurement | one run of the existing case with the two shapes added. The tree cannot answer it by reading: what `malformed_rows` prints for a span that holds a space and two words is its "text as written", and nothing read here shows that text for these two shapes | where the output is `MALFORMED <shape>  `, both go in `TAKEN_UP` under a key naming what keeps them named. Otherwise they go in a sibling dict whose case asserts `ec.refused_coordinate(shape) is True` and the docstring presence, and the completeness case reads that dict too | ✅ answered 2026-09-28 by phase 1's run, executed: both print `MALFORMED <shape>  ` at exit 1, so both are in `TAKEN_UP`, whose case is renamed `test_what_the_rules_still_name_is_named_and_says_so` (`phases/phase-1.md`) |
| Q2 | Is `@alice#299@abcdef12` named? Rule 3's new wording has to be true of it | a measurement | a call to `refused_coordinate`. Reading already says yes: `GLUED_MARKS_RE` is searched and `#299@` matches | the bullet says the `@` must come after its `#`, not that an `@` before it makes the text silent | ✅ answered 2026-09-28 by the framer's probe at `72cd90f`: `refused_coordinate("@alice#299@abcdef12")` is True, and `@alice#299` and `@types/node#1` are False. The builder executes it again and records it in `phases/phase-1.md` (S2) |
| Q3 | Which ledger rows drift, and does each claim still hold? | the work | only `evidence-check` after the edits names them for certain. `spec.md` §*Data & interfaces* lists the fourteen expected from the units cited | re-read each against the edit, `--reverify`, and a dated `Re-read` note in the release file, with the claim corrected first where the edit made it false. S8–S12's Notes ("`changelog.md`", "one or two examples of each") are the likeliest to need a sentence | ✅ answered 2026-09-28 by the build, executed: 14 rows cite a unit the work edited, one more than listed in `0.11.4.md` (the sixth re-wrap) and `0.15.4.md`'s S1 not among them, plus `0.13.1.md`'s row hashing the `0.4.0` section. S8–S12's Notes were corrected in place; every other claim holds and took a dated `Re-read` note (`phases/phase-1.md`, `phases/phase-2.md`) |
| Q4 | Do this branch's re-stamps in `seal/releases/*.md` conflict with chain A's or C's at the squash? | the work | unknowable at framing time: A and C re-stamp what their own `evidence-check` names. `0.15.5.md` and `0.9.3.md` are the files this branch touches that the other chains may also touch | B squashes second (A, B, C). If a file conflicts, merge the release branch in (never rebase), resolve ledger files hunk by hunk (`docs/the-evidence-ledger.md` §*A correction a merge dropped*), run `evidence-check`, and re-run only the narrow cases the resolved files touch | ⬜ |

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
  framer, which would spend the interruption the framing phase exists to spend
  once.

**The framer opens rows and does not own their answers.** A row is a question
put to somebody else, so opening one costs little and closes nothing — and the
`Status` column is ticked by whoever answered, never by whoever asked.

Answered rows feed back into docs/ (policy clause or open-questions section)
before this directory's work merges.
