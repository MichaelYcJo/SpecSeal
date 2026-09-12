# round 2 — the verifying round's paragraph

| | |
|---|---|
| Target | the **diff of round 1's fixes**, `a0f0e9a..941dab5` — not the branch |
| Review at | `941dab5` |
| Base of the branch | `origin/release/v0.11.1` = `7e17f5e` |
| Draft pull request | #364 |
| Ran by | specseal:warden on Opus 5 |
| Previous record | `rounds/round-1.md`, closed — 8 fixed, 0 answered, 0 deferred |

## The job, and the one surface that is not verification

**The answers, not new findings** — for each of round 1's nine verdicts, is it
actually closed. `rounds/round-1.md` holds the verdict table,
`rounds/round-2-fixes.md` holds what the fix pass says it did, and
`rounds/round-1-report.md` holds the reasoning the verdicts came from.

**One exception, and it is a finding surface.** `round-1.md`'s `New units` row
reads **`hits (depth 1)`**, derived from the fix diff by `round_record.py
close` rather than typed. `hits()` in
`tests/test_a_release_is_sized_by_a_criterion.py:117-134` is a unit the fixes
created, so nobody has reviewed it: it is *is this correct*, not *did this
close something*. It is also the whole of finding 2's answer, which makes it
the round's centre.

Read it against what it has to do. A hand-wrapped document splits a sentence
across exactly one line boundary, so `hits()` searches each line and each line
joined to the next with the wrap collapsed — and skips the joined check where
the next line matches alone, so a wrapped sentence is reported once at the line
it starts on. Ask what the one-boundary assumption costs: `test_docs_line_wrap`
caps the width, and a sentence long enough to span **two** boundaries is the
shape this cannot see. Whether that matters is a judgment; make it rather than
assume it.

## What the fix pass says it did, to be checked rather than inherited

- **Finding 1 answered with a sentence about two moments, not a corrected
  moment.** `docs/issues-and-milestones.md:148-155` now anchors the label's
  removal on *the moment `main` moves and the issue closes* and then says
  **Not when `merged: X.Y.Z` goes on**, naming the section that puts that a
  release earlier. Judge whether the new sentence is true of both mechanisms,
  and whether a reader lands on the right moment.
- **Finding 3 widened `STATES_A_SIZE` and disclosed a misfire at the
  coordinate** — `\bis\s+the\s+size\b` can match a sentence about the size of
  anything, and the constant says so and says nothing in the scanned set
  matches it today outside the two excluded files. **That second clause is a
  measurement with a shelf life**; re-derive it rather than trust it.
- **Finding 5 corrected a false execution claim in a ledger row.** R1 said
  `git grep -n "is the size"` exits 1; it exits 0. Check that what the row now
  says reproduces, and that `phases/phase-2.md` keeping its `1` with a clause
  naming the commit from which it stops being true is the right treatment for a
  phase record.
- **Finding 7 marked #351's `changelog.md:22` rather than excusing it**, and
  `survivors.md`'s row now quotes the marking clause so the exemption dies if
  the marking changes. Judge both halves, and whether the released section now
  reads correctly in work-item id order.
- **Finding 9 added `CLAUDE.md` to `SCANNED`.** 170 files, no offender claimed.

## Executed by the orchestrating session at `941dab5`

Exit codes read directly, no pipe. Re-derive rather than inherit:

- Eight modules, one per call — the new module 7, `test_docs_line_wrap` 23,
  `test_release_hygiene` 32, `test_one_word_one_meaning` 13,
  `test_no_real_identifiers` 2, `test_a_row_points_by_content` 102,
  `test_a_record_states_what_the_tree_has` 58,
  `test_the_set_a_work_item_always_has` 16 → **exit 0 each**.
- `uvx ruff check` and `uvx ruff format --check` on the module → **exit 0** each.
- `STATES_A_SIZE` exercised directly: all three noun forms that escaped before
  — `A release's size is three or four work items.`, `Three or four work items
  is the size of a release.`, `The size of a release is three work items.` —
  are now **caught**, and so is the replaced sentence.
- `hits()` exercised directly: a sentence wrapped across two lines is `[]` to a
  plain line scan and `[1]` to `hits()`; a whole-line statement reports once;
  two adjacent matching lines produce no double report. **This session's first
  attempt was wrong** — `hits()` takes a list of lines, and passing a string
  iterates characters and answers `[]`. Worth knowing before you call it.
- `git grep -c "is the size"` over the set R1 names → four hits, all inside the
  new module.
- `bin/survivor-check --range 7e17f5e..HEAD --exempt <survivors.md>` → **exit 0**.
- `bin/evidence-check .` → **exit 1**, ledger arm **1144 ok · 0 drifted · 0
  broken**, records arm one drift at `spec.md:159`.
- The finding-1 sentence read against `:209-210` and
  `docs/branch-and-release.md:251-258`.

## Settled, and not yours to reopen

**The four owner answers.** Q1 (c) — the releases are cited as prose, the
checker's off-by-one is #363, and **a finding proposing an edit to
`tests/test_release_hygiene.py` is out of scope**. Q2 (b) — the prefix form;
the spelling is settled when the owner creates the label, so a better one is a
note. Q3 (a) — **this work item writes nothing to the tracker.** Q4 (a) —
milestone descriptions are out of scope.

**Round 1's own two judgments.** #351's `changelog.md:22` gets a marking clause
rather than an exemption; and `spec.md:159`'s records-arm drift **stays**,
because S3 was removed rather than re-pointed, so re-stamping would leave a row
that no longer exists quoting current content. Judge whether the fixes did what
those decisions asked, not whether the decisions were right.

## Still unverified, and it stays that way

**The broad gate is the `sealer`'s. Do not run it.** No `bin/broad-gate`, no
whole-suite run, no repository-wide `ruff`. It comes due when this round closes.

## The form the commands take in this checkout

`ruff` is not installed — `uvx ruff check` / `uvx ruff format --check`. Read
exit codes directly, never through a pipe (`cmd > /tmp/x 2>&1; echo $?`); this
shell is `zsh`. `bin/test`, narrow, one module per call. `evidence_check.py .`
**unscoped for reading** — the `--ledger` narrowing is for a `--reverify` write
and blinds a read.

## The line the run ends on

Answer each in a line of its own — `Needs a fix: no`, or `yes` and what does;
and `Loses a record or crashes: no`, or `yes` and what does. A 🟡 answered with
grounds is `no`, and a finding located under `seal/specs/` is a correction that
does not count. **The reopening is one**: if this round opens something, its own
fixes get one more verifying round and a second is refused, after which the run
ends `capped`.
