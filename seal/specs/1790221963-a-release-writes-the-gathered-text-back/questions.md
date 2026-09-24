# a release writes the gathered text back — questions for the planner

<!-- seal/specs/1790221963-a-release-writes-the-gathered-text-back/questions.md — decisions only a human can make,
extracted so nothing ships on a silent assumption. Before adding a row,
check the inheritance rule: if policy is silent but existing behavior
answers it, inherit and record — only genuinely NEW rules belong here. -->

**What the tickets left open and the tree answered**, listed so nobody
reopens it here. The grounds are in `spec.md` §*Judgments the tree
answered*, numbered the same way.

1. #557's paste-ready fix applies to `61f0d0d8` as written. The two files
   differ from round 3's target by one comment line outside `corrected`.
2. The held set is read at `a`, because the gatherer leaves the fragment in
   place and a gatherer that deletes it leaves nothing at `b`.
3. The key match has one known miss, a prose-first fragment fused with its
   marker line. That is §12's member, and phase 2 is conditional on Q1.
4. #555's case is P6d, not P6. After #557, P6 is protected by the guard and
   by the filter each alone, so it pins neither. It stays as the pair's case.
5. The `lost` guard stays, because P6d goes silent without it.
6. Step E (#526) needs no sentence. `docs/review-chain-spec.md` §*The
   survivor sweep* states nothing at the altitude this work changes.
7. Step A's F1, C2 and `plan.md` gate row are corrected in place, with dated
   notes. Its round records are not edited.
8. Nothing in `seal/follow-up.md` waits on this work.

No row below is a person's. The build does not wait on this file.

| # | Question | Who can answer | Options & what each implies | Default until answered | Status |
|---|---|---|---|---|---|
| Q1 | Is G4 red with phase 1's filter in place? G4 is a fragment whose body opens with a plain sentence equal to `FOUND`, gathered in `gather_changelog.py#section`'s layout (marker line, then the body with no blank line) under an H1 release. By reading, `segments` fuses the marker's words with that first sentence, the key misses the held set, and the sentence is written. Nothing has executed it | a measurement — G4 run against phase 1's tree, in phase 2 | Red: phase 2 lands the marker blank in `newly_released`, and G4 is planted. Green: the reading was wrong somewhere, and nothing is changed or planted. `phases/phase-2.md` records the exit, the `against N sentence(s)` line and which sentence key the fragment's first line produced | phase 2 runs the measurement first and does what it says | ✅ red, exit 0 with `against 2 sentence(s)`, the first line keyed `specs 1700000003 a shipped item the verdict cell …`; the blank landed at `c90821fb` (`phases/phase-2.md`) |
| Q2 | With phases 1–3 in place, what does G6 (P6) do with the guard removed alone, and with the filter removed alone? `spec.md` judgment 4 says green both times, because each protects P6 alone, and red only with both removed. That is read, not executed | a measurement — two mutations from Python in phase 3, the file restored byte-identical | Green both times: recorded in `phases/phase-3.md`, and the case's docstring says it pins the pair. Red under either: that one does pin P6 alone, judgment 4 was wrong, and the record says which | the case is planted as the pair's pin, and the mutations' results are recorded | ⬜ |
| Q3 | Which ledger anchors does the build actually drift? `spec.md` §*Data & interfaces* lists eight rows on `corrected`, F1 on `newly_released` if phase 2 lands, and C2 on `a_gathered_fragment`. Whether the docstring heading anchor `#"## What is excluded, by construction rather than by list"` (three `seal/ledger.md` rows) drifts when one sentence under it is reworded is not known. Step A measured that a paragraph added under it did not | the work — `bin/evidence-check --strict .` before `--reverify`, in phase 4 | Each row it names is re-read and re-stamped with a dated `Re-read` note, or corrected where its claim changed (F1, C2). A row the table did not predict goes in `overview.md`'s divergence table | the table in `spec.md` | ⬜ |
| Q4 | How is G4's fixture laid down? It can import `gather_changelog.py#section` by path, as `tests/test_the_changelog_is_gathered_at_release.py` loads the gatherer, so the layout follows the gatherer if it ever changes. Or it can spell the layout inline with a comment naming `section` | the work — phase 2 | Import: the case tracks the real layout, and the test module gains one dependency on release automation. Tests may take that dependency, a shipped script may not. Inline: no dependency, and the case can go stale against a changed gatherer | import `section` by path | ✅ imported by path (`gathered_section`); the named module runs the gatherer as a subprocess rather than loading it, and the import works because the gatherer puts `hooks/` on `sys.path` itself (`phases/phase-2.md`) |

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
