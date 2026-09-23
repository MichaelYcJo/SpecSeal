# folded statements pile into one spec (#520) — questions for the planner

<!-- seal/specs/1790154761-folded-statements-pile-into-one-spec/questions.md —
decisions only a human can make, extracted so nothing ships on a silent
assumption. The run is `automation`: nobody is asked, so every row says why
the tree could not settle it, and every default continues. -->

## What the ticket left open and the tree answered — do not reopen

| Settled | Answer | Where the grounds are |
|---|---|---|
| Split the chain spec now? | no. It is deferred with a home, and a ceiling holds the pile in the meantime | `spec.md` §*What was measured…*: the 1,430-line section and the 47-file surface, 12 of those files in PR #525. `plan.md` §*Alternatives* row 1 |
| State where a fold puts a chain rule | yes: one subject, one document, and a document over the ceiling takes no new statement | `spec.md` §Scope item 3. The owner of the rule is `skills/settle/SKILL.md` §2 |
| Does a standing statement get a fixed shape? | yes: a bold rule sentence, its grounds, and one `Enforced by:` line | `spec.md` §Scope item 2 |
| Can a check read the shape? | yes, for new folds. It reads presence, count and that each target resolves. It cannot read truth or contradiction, and the spec says so | `spec.md` §Scope item 2, and §*Out* row 4 |
| Pair the editions or retire the Korean one? | pair them | `CONTRIBUTING.md` §*Both READMEs move together*, the docstring of `test_both_editions_took_the_same_decisions`, five test modules that pin the Korean text, and PR #525 extending both editions by hand. `plan.md` §*Alternatives* row 6 |
| How are the existing 101 statements exempted? | by work-item id, `< 1790154761`. There is no list | `plan.md` §*Alternatives* row 4 |

## Rows

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Should `docs/one-root-by-lifetime.ko.md` exist at all? | a person. Why the tree cannot settle it: whether a design record is kept in Korean is a product choice about who reads `docs/`. The tree shows the owner has kept it, which answers *what to do by default* and not *what the owner wants* | **keep and pair** (the default): phase 1 as planned. **Retire**: delete the file, drop the language link in the English header, edit the five modules that pin it, and the pairing test then reads no pair (its read-at-least-one floor must be removed with it, not lowered) | keep and pair | ⬜ |
| Q2 | Is `LINE_CEILING = 1000` the right value? | a person. Why the tree cannot settle it: it is a limit folders are bound by, so it has to be a value somebody is accountable for (`skills/implement/SKILL.md` §3). The tree gives the grounds and not the value: the next-largest document is 839 lines, so 1,000 binds only the chain spec. Any value from 840 to 2,158 builds the same code today | a lower value binds `docs/review-handoff-protocol.md` sooner. A value of 2,000 is one Read tool window, and it lets every other document more than double | 1000 | ⬜ |
| Q3 | Which issue number is the over-list entry's home? | the work. The orchestrator files the split issue (rung 3, `backlog: docs drift`) before phase 3, with three items: the split along the chain spec's own headings, with the `commit-review-gate` section divided on its `###` headings; the `Enforced by:` retrofit of the 101 statements; and the plugin-level command for the two checks. Phase 3 writes the number into `OVER_CEILING` and the prose | none. The number is written, and phase 3 does not start without it | the number the orchestrator hands phase 3 | ⬜ |
| Q4 | May a record of a moment (`tests/test_no_document_names_the_old_roots.py#DESIGN_RECORD`) take a fold? The first fold wrote an undated standing section into `docs/one-root-by-lifetime.md`, while the settle test's docstring says such a record takes a later decision only as a dated section | a person. Why the tree cannot settle it: the two readings are both in the tree, and nothing here builds differently under either, because phase 1 pairs the editions whichever way this goes | **yes** (the status quo): nothing moves. **No**: a later work item moves the section into a living document, and settle §2 names design records as closed to folds | yes — status quo, and no build change here | ⬜ |
| Q5 | Where exactly do the Korean edition's 5 non-section markers go when a Korean paragraph does not match the English one sentence for sentence? | the work. Phase 1 meets it. The check pairs by heading position, not by paragraph, so any placement under the right heading passes, and the translator puts each one on the matching statement | — | above the Korean paragraph that carries the same statement | ⬜ |

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

None of the three person rows blocks the build. Each has a default that
continues, and a different answer to Q1 or Q2 changes one phase's content
without changing the order of the phases.
