# a changelog fragment a fix range left behind is named (#797) — questions for the planner

<!-- seal/specs/<unix-epoch-seconds>-<slug>/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Nothing here blocks the build.** The judgments #797 left open were answered
from the tree, and their grounds are in `spec.md` and `plan.md`'s
*Alternatives considered*, where a reviewer can overturn them by opening what
was opened:

- **Notice or refusal** — notice. `spec.md` §*The measurement*: a refusal
  would have stopped 24 of 42 branch tips, at least 9 of them honest.
- **Where the check lives** — `chain_check`, the one reader `close`, `seal`
  and CI all run. `spec.md` §*Scope* says why neither `close` nor
  `broad-gate --preflight`.
- **How each range is found** — post-build is round 1's `Target SHA` to HEAD,
  first-parent and non-merge; a fix range is the record's `Fix range` row;
  after the last round is what no row holds past the last range's end; an
  integration's merge is skipped and the item's own commits after it count.
- **Whether `agents/` and `skills/*/SKILL.md` count** — yes, by
  `skills/implement/SKILL.md` §3, and by construction: every path outside the
  `seal/` root and outside a `tests` directory counts.
- **Where the rule lives** — one section of `docs/the-record-layout.md`, with
  the three carriers linking to it.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | The per-item reading in `spec.md` judges five released fragments likely lagging — `1790635412` and `1790635414` (0.16.0), `1790993137`, `1790993138` and `1790993140` (0.18.0). Are their released `changelog/<X.Y.Z>.md` sections corrected? The tree cannot answer it because amending a released record is the owner's open decision already: `seal/follow-up.md`'s two rows on `changelog/0.12.2.md` wait on the same choice, and this item's build is the same either way | a person — the repository owner | (a) leave the released sections as they are, and the five stay named here and in `spec.md`; (b) a later branch based on `main` amends them, after somebody reads each against its diff — the reading here is from commit subjects only | (a). The build does not touch `changelog/` | ⬜ open; default (a) taken by the orchestrator under the owner's `automation` routing, and the build touched no `changelog/<X.Y.Z>.md`. The owner is told at the pull request |
| Q2 | The 14 fix ranges and 5 work items `spec.md` labels *unclear*, and the split of the rest — honest or lagging, read against each full diff rather than from commit subjects | a measurement — reading each range's diff against the fragment as it shipped | a finer split changes the counts and not the decision: even the smallest honest share (21 of 66 ranges, 9 of 24 items) argues against a refusal | the counts stand as labelled *read* | ⬜ open; the default stands — no range was re-read against its diff in this build, and the decision does not move on it |
| Q3 | The notice's exact wording, how many commits it names before it summarises the rest, and the new test module's name | the work — phase 1 meets it | any spelling that names the commit, its round or *after the last round*, its behaviour paths, the fragment's path and the owning section, and that says nothing is owed where the fragment still says what ships | phase 1 decides and pins it (contract §14) | ✅ decided 2026-10-05 in phase 1: one notice per work item naming every late commit, up to three paths each, three attributions; `tests/test_a_fragment_left_behind_is_named.py` pins it (`phases/phase-1.md`) |
| Q4 | Whether the three link sentences share 25 consecutive words with the owning section, which `tests/test_no_passage_is_pasted_into_a_second_file.py` would refuse | a measurement — that module, run in phase 2 | rewording a link until the module passes; never a `BASELINE` entry | links written short, naming the section | ✅ measured 2026-10-05 in phase 2: `tests/test_no_passage_is_pasted_into_a_second_file.py` passed with the three links in and no `BASELINE` entry (`phases/phase-2.md`) |

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
