# the changelog is one file per release (#728) — questions for the planner

<!-- seal/specs/1791076834-the-changelog-is-one-file-per-release/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**Nothing in this file blocks the build.** Nobody is asked during this run,
so every row below carries the default the build proceeds on.

## What the ticket left open and the tree answered

Listed so nobody reopens them; the grounds are in `spec.md`, and each can be
overturned by opening what was opened there.

- **A release file keeps its `## X.Y.Z — <date>` heading** (spec D1): every
  section reader finds a section by that line, and the migration can be
  proven lossless by concatenation (measured on acc3bae6).
- **The index keeps one `## ` line per release** (spec D2): 0.18.0's update
  skill, which is the one that runs the update into 0.18.1, verifies the
  install by the first `## ` line of `CHANGELOG.md`.
- **0.18.1 is gathered by the new tooling** (spec D6): this branch squashes
  before release preparation, the old gather corrupts the index on a migrated
  tree, and `publish-release.yml` runs the script at the tagged commit.
- **The shipped survivor sweep is in scope** (spec D5): it is a reader of the
  released sections the issue's list did not name, and without it the
  migration range itself reports released prose.
- **The update skill is in scope** (spec scope 6): it is the reader the
  issue's prompt calls the `plugin update` verification habit.
- **The installed plugin needs no change to carry `changelog/`**: the install
  path and the marketplace clone are copies of the whole tree (read: `ls` of
  both on 2026-10-04).
- **The migration is a throwaway script, not a flag** (plan, *Alternatives*).
- **The gather's flags, exit codes and refusals are unchanged** (spec D3).

## The residue

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Does an index entry carry only the heading and a link, or also a one-line summary of the release? | a person | **Link only**: the gather writes it from the heading it already has, and nothing composes prose. **A summary line**: needs a source — the `release: X.Y.Z — <symptoms>` line exists only in the release pull request's title, which the gather runs before — so it would be a new hand-written field per release. Different code. Why the tree could not settle it: it is what a reader of the index should see, which no document states | Link only. Decided by the framer, because the summary has no source at gather time | ⬜ decided by framer, default in force |
| Q2 | On the update into 0.18.1, 0.18.0's update skill summarises `CHANGELOG.md` and meets the index (spec D7). Accept a thinner summary for that one update, or carry the newest release's full text in the index as well? | a person | **Accept**: one release's update summary depends on the session following the index's link; no record has two homes. **Duplicate the newest section into the index**: the update into 0.18.1 summarises as before, at the cost of the newest release's text living in two files, where `docs/the-record-layout.md`'s opening paragraph gives every kind of record one home. Why the tree could not settle it: it trades one update's experience against the layout's one-home rule, and only the owner can weigh a user's experience against policy | Accept. Decided by the framer: the policy gives a record one home, and the cost lasts one update | ⬜ decided by framer, default in force |
| Q3 | Should a released `changelog/<X.Y.Z>.md` be refused by a machine rule once a newer one exists, as `Ledger frozen from` refuses a released ledger file? | a person | **No rule (this work)**: a hand edit to a released file is caught only by review. **A rule**: new mechanism in the gather or a hygiene case, which F2 does not ask for. Why the tree could not settle it: no policy freezes a released changelog section by machine, and adding a rule is a new decision, not an inference | No rule; out of this work's scope (spec *Out*) | ⬜ decided by framer, default in force |
| Q4 | `seal/follow-up.md` rows 70 and 72 cite *the released `CHANGELOG.md` §0.12.2*. This work moves that section. Rewrite the coordinate only, or leave the rows untouched? | a person | **Coordinate only**: the rows keep pointing at the sentence they mean, and their decision (Q1 of work items 1789996775 and 1789996780) stays the owner's, untouched. **Leave them**: their coordinate points at an index with no such text. Why the tree could not settle it: the rows are the owner's open questions, and editing a row somebody else must answer is a judgment about their record | Coordinate only, the decision text unchanged | ⬜ decided by framer, default in force |
| Q5 | Is the migration lossless on the tree the smith actually builds on, after `origin/release/v0.18.1` is merged in? | a measurement | The S1 probe (spec), run once after phase 0's merge. On acc3bae6 it holds: 44 headings, each preceded by exactly one blank line, `# Changelog\n\n` prefix, one trailing newline, no CR, rejoin identical | Holds, as measured on acc3bae6 | ⬜ |
| Q6 | Does a wave-1 branch of 0.18.1 add a reader or writer of `CHANGELOG.md` or of its sections? | a measurement | Phase 0's two greps on the merged tree. On acc3bae6 `origin/release/v0.18.1` is still e141980a, so nothing had squashed when this was framed | None | ⬜ |
| Q7 | The exact wording of the index's paragraph, and of each printed line that now names `changelog/X.Y.Z.md` | the work | Phase 1 and phase 4 write them, with the case that pins each (contract §14) | — | ⬜ |
| Q8 | Whether `tests/test_every_reader_ends_a_line_where_gfm_does.py`'s monkeypatch of `survivor.read_blobs` keeps its shape once `gathered_fragments` reads more than one path | the work | Phase 3 decides with the predicate's shape; the case's assertion (a marker after a U+2028 is not a live marker) must hold for both shapes | — | ⬜ |

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
