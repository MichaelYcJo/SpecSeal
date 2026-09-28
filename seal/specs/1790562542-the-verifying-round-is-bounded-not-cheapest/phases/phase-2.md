# 1790562542-the-verifying-round-is-bounded-not-cheapest — phase 2

| Field | Value |
|---|---|
| Phase | 2 |
| Commit | b2b1de06 |
| Ran by | unknown — the spawn prompt named no agent or model for this row, and the value is the spawning session's to give |

## What this phase was asked

Run `evidence-check .` on the phase-1 tree to name what drifted. Re-read
each drifted row against the edit and re-stamp it with `--reverify`,
narrowed with `--ledger` per `skills/code-review/orchestration.md` §*The
check a round runs reads everything, and only a write is narrowed*, with a
dated `Re-read 2026-09-28` note. Add this work item's own row to
`seal/ledger/1790562542-the-verifying-round-is-bounded-not-cheapest.md`.
Then run `survivor-check --range origin/release/v0.15.7..HEAD` and correct
or exempt every survivor, which answers `questions.md` Q2.

## What this phase found

**Twelve anchors drifted in eleven rows, not the plan's seven.** The plan's
list was a reading and said the executed answer wins. Seven rows are the
plan's. Four more come from the #81 correction phase 1 took on:

- `seal/releases/0.10.0.md` 🟡 1 / 🟡 4 / r3 1
- `seal/releases/0.5.0.md` r3 3 / r4 2
- `seal/releases/0.8.1.md` R9, on both its template and skill anchors

The eleventh is `seal/ledger.md`'s "The handoff before round 1 … protocol
rather than habit". It anchors the `## The handoff before round 1` H2,
which encloses the bars subsection C2 edits. The plan read only
`seal/releases/*.md` for the protocol and missed it. Every one of the
eleven claims holds after the edit, and none sits in a sentence this branch
changed. Each row carries a `Re-read 2026-09-28 by work item 1790562542
(#639), phase 2` note saying what changed inside its unit and why the
claim still holds. The `Checked` cells were left as they were, the way
earlier re-reads in these rows left them.

**The write was narrowed one file at a time.** `--reverify` ran once per
file holding one of the eleven rows, with `--ledger <file>`, and once over
the new fragment. The baseline had 0 drifted, so no row outside the eleven
could be rewritten either way. The diff confirms it: `git diff --stat` over
`seal/` shows one changed line per row, 11 in all, and only in those ten
files.

**The fragment made this work item's records live, and the records arm
then read the plan's own drift table.** `evidence-check` reads a work
item's records only once it has a ledger fragment. The baseline read none,
and the first run after the fragment read this one. Two findings came back
at exit 2:

- The plan's table quoted six anchors with the hashes they held at
  `97a30dc6`. Each is exactly a unit this branch edits, so each read as
  DRIFTED. The hashes were taken out of the table, and a sentence below it
  says why.
- `phases/phase-1.md` shortened a test name to `names_81`, which is not in
  the tree. The full name is written now, and in the fragment too.

**The new fragment's two rows narrow two coordinates to a sentence.** The
warden's `## Role` and the review skill's `## Cross-session records` are
units that drift on unrelated edits, as the re-read notes on the rows that
anchor them whole show. Each row's Notes cell says so.

**Q2 is answered (a): silent.** `survivor-check` read 454 files at
`b2b1de0` against the 20 sentences the range removed, and reported "no
removed wording is still standing". No `survivors.md` was needed. The
gone halves the test modules keep verbatim did not come back as survivors.

**Executed, exit codes read directly:**

- `bin/evidence-check .` exits 1 before the re-stamp (2501 ok, 12 drifted,
  0 broken). After the re-stamp it exits 2 on the two records findings
  above. After those corrections it exits 0: 2529 ok, 0 drifted, 0 broken,
  and the fragment's 16 anchors all ok. The records line reads "1 work item
  read … 0 refused · 0 drifted".
- `bin/survivor-check --range origin/release/v0.15.7..HEAD` exits 0. The
  `--exempt` form first exited 2, because the file it names does not exist
  until something needs exempting.
- `bin/correction-check --range origin/release/v0.15.7...HEAD` exits 0,
  with no merge commit in the range.
- `bin/test tests/test_the_verifying_round_is_bounded_not_cheapest.py tests/test_the_last_rounds_fixes_are_checked.py tests/test_the_handoff_before_round_one.py tests/test_a_segments_record_says_what_it_was_asked.py tests/test_the_ledger_fragments_fold_at_release.py tests/test_a_merge_cannot_silently_drop_a_correction.py -q` exits 0.
- `bin/unverified-check` on this work item exits 0.

## What this phase removes

| Removed item | Where it must land |
|---|---|
| the six base-state `@hash` stamps in `plan.md`'s *Ledger rows this edit drifts* table | this record, which lists the executed drift. The hashes each row now holds are in the rows themselves |
