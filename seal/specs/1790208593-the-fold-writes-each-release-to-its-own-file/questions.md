# 1790208593-the-fold-writes-each-release-to-its-own-file — questions for the planner

<!-- seal/specs/1790208593-the-fold-writes-each-release-to-its-own-file/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

## Judgments the ticket left open that the tree answered

Listed so nobody reopens them; the grounds are in `spec.md` §*Judgments the
tree answered*, one number each.

1. The checker's anchor rules do not change; its glob does. The item stays
   in 0.15.1 (1).
2. The ticket's claim that this shape removes the conflict class is not what
   the cited merge shows: seven of seven hunks were same-row conflicts. The
   build proceeds by default with the claim corrected (2, and Q1).
3. The release files are `seal/releases/<X.Y.Z>.md`, a sibling of
   `seal/ledger/`, which the ticket left to the frame (3).
4. A release file is the ledger section byte for byte, first line
   `## X.Y.Z — <date>` (4).
5. The 37 existing sections move at the release-preparation commit of the
   release that ships this work, not in this branch (5).
6. `--check` refuses any release heading left in `seal/ledger.md`, naming
   `--split`; C's doubled-version reader survives inside `--split` and over
   each release file (6).
7. `--split` refuses an existing target; a join is the fold's (7).
8. The one row anchored into `seal/ledger.md` is rewritten by the split,
   hash unchanged (8).
9. The narrowing notice stays one skipped ledger per line (9).
10. This branch re-stamps `seal/ledger.md` in its pre-split shape and merges
    the release branch in hunk by hunk (10).

## The residue

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | The ticket asks for this shape because it *removes the conflict class rather than a hunk of it*. Executed at the frame: the merge it cites, `0be23b80`, re-derived with `git merge-tree` — seven conflict blocks in `seal/ledger.md`, and in all seven both sides had edited the same rows (1, 3, 2, 2, 3, 5 and 1 shared first cells). Three branches each ran `--reverify` over units they had changed, and `--reverify` re-stamps every row citing a drifted unit, so the same rows were re-hashed three ways. A row that lives in `seal/releases/0.12.2.md` is still one row two branches re-hash differently: the seven hunks would have conflicted in four smaller files. What the split does buy is measured in `spec.md` §Scope: `seal/ledger.md` goes from 2,736 lines to about 100 and stops growing, a re-stamp's diff and a conflict's hunks land in a 9–308-line file, and a release creates a file instead of appending to the largest record in the tree. What would remove the class — a branch recording its re-verifications somewhere other than the shared row, folded at the release — changes where a hash is read from, which is the checker's baseline rule and the 0.16.0 design the ticket reserves. **Does not block this build**: the five phases are the same whichever answer comes, and the changelog entry states the corrected claim either way | a person — the repository owner | **build as framed** — #547 closes with this pull request on the corrected claim, and the overlay is a new ticket for 0.16.0 beside #159 and #526 if wanted · **stop D** — the branch is handed back with its frame and no build, and the overlay ticket carries the conflict problem · **build, and file the overlay ticket now** — the same build; the orchestrator opens the 0.16.0 ticket with this row's measurement as its body | build as framed | ⬜ |
| Q2 | `fold_ledger.py#append` is unused once the fold writes the release file (a new file is `section()`'s block; a join is `insert`). Is it removed, with the §0.4.0 row that cites `#append@e091419b` beside three live anchors narrowed — its dead anchor dropped, the way `settle` names a row that keeps a live anchor — or kept as a helper nothing calls? | the work — phase 2 decides it and `phases/phase-2.md` records it | remove, narrow the row · keep | remove; a helper nothing calls is a sentence the next reader has to disprove | ⬜ |
| Q3 | C's `doubled_versions(text)` reads a ledger for a version headed twice. D needs three readings of `## \d+\.\d+\.\d+` lines: any such line in `seal/ledger.md` (refused by `--check`, and the input of `--split`), a doubled one in `seal/ledger.md` (refused by `--split`), and exactly one matching the file name in each release file. One helper returning `[(version, [lines])]` serves all three; `doubled_versions` is that helper filtered. Does the name stay for C's cases, or does D rename it and re-point them? | the work — phase 2 decides it and records it | keep `doubled_versions` beside a new `version_headings` · one reader, C's cases re-pointed | one reader, `version_headings`, with `doubled_versions` kept as the one-line filter C's cases and `tests/test_release_hygiene.py` already name | ⬜ | (NAME NOT IN TREE until the phase adds it)
| Q4 | Does `survivor-check --range origin/release/v0.15.1...HEAD` report anything as a survivor of wording this branch removed? Candidates the frame can foresee: C's sentence in `docs/release-checklist.md` §2 (*joins the section `seal/ledger.md` already heads*) reworded here while C's own spec quotes it (a record, out of the pool); the module docstring's *The section is appended* paragraph; the two deliberately duplicated ledger paragraphs in `CLAUDE.md` and `CONTRIBUTING.md`, which this branch edits together (a report there is right only if one is missed). This branch moves no ledger row, so the flood the frame rejected in `plan.md` §Alternatives does not arise | a measurement — one run at the verify phase | assume none; a `survivors.md` row with the quote and the grounds for anything reported | ⬜ |
| Q5 | After the default glob widens, a `--ledger` run over this repository names every skipped ledger, one per line — `seal/ledger.md`, the fragments, and after the real split 37 release files. How long is the notice on the narrowed `--reverify` form `skills/code-review/orchestration.md`'s table prescribes, and does the rule *named, not counted* still read as the right one at that length? Measured, not decided: the rule stands unless the number says otherwise, and changing it is `test_every_skipped_ledger_is_named_not_counted`'s and the skill's | a measurement — one run at the verify phase over this tree (2 names today) and one line in the phase record extrapolating to 39; the real figure is the release session's after the split | the notice stays one name per line; the count goes in the memo | ⬜ |
| Q6 | At the release that runs `--split` on the real tree: does `test_the_bound_covers_every_candidate_marker_site_the_corpus_carries` stay green (8 markers stand in the standing area today, executed at the frame), does `evidence-check --strict .` report the same set before and after (the rehearsal S14 says yes on a copy at HEAD), and does `correction-check` over the next release branch's merges stay silent across the moved rows (the cross-path limit `spec.md` §Out states)? All three are one run each at the release-preparation step; none is knowable from this branch beyond the rehearsal | a measurement — the session running the release tail, at `docs/release-checklist.md` §3 | the rehearsal's answer holds on the real tree; a difference is a finding at the release pull request, not a reason to hold this branch | ⬜ |

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
