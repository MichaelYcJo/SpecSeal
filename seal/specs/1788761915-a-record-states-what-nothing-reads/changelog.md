- **`evidence-check` now reads what a record says about the tree, and refuses
  a record of a work item that has not shipped when it names a unit nothing
  outside the records carries (issue #190).** A ledger row is a claim about
  the tree that something reads; a `spec.md`, a `plan.md`, an `overview.md`,
  a round record or a phase record states the same kind of thing and nothing
  read it. One work item closed that class three times in three rounds and it
  came back each time, because every closing grepped for the carriers instead
  of building a reader.

  **The boundary is a file the release already removes.** A work item whose
  `seal/ledger/<id>.md` fragment still exists has not shipped, and the fold
  deletes that fragment at the release — so *this record is still the file
  the next segment opens* needs no state of its own. The 129 occurrences in
  work items that have shipped are history and are never opened: a plan from
  0.4.0 proposing a helper that was built under another name is a correct
  record of what was decided then, and a check that refuses history is a
  different mistake.

  **A backticked name is read as a claim only when it carries an
  underscore**, and that narrowing was forced by measuring. Of the 55 distinct
  names in this repository's records that appear nowhere else, the 19 without
  an underscore are a shell command, six stdlib names, an errno, an
  environment variable, a lint code, a probe value, five words of ordinary
  prose in backticks, and three verdict words a checker used to emit — not one
  a claim about a unit, where all 36 compound names are. Without it the first
  record mentioning `str.rpartition` would be asked to mark it as absent,
  which is noise attached to a name that is real.

  **The escape hatch is the marker reviewers already write.** A line carrying
  `NAME NOT IN TREE` is not read at all, in either of the marker's two
  meanings: a name a paste-ready fix is proposing, and a name a record is
  deliberately calling gone. It exempts the line and not the name, so the same
  name still has to exist everywhere else it is claimed — and the exemption
  stays with the person who knows the name is absent instead of becoming a
  list inside the checker that whoever is annoyed by a refusal can widen.

  **A `path#unit@hash` a record wrote down is resolved by the ledger's own
  reader**, so a stamp in a record and a row in a ledger cannot drift apart
  into two rules. Two things deliberately do not carry across: a verdict
  table's `Location` column is `path:line` by design, so a record is never
  told to run the coordinate migrator, and drift in a record reports rather
  than fails — a live work item's branch is editing the very units its records
  stamp, and a check that is always red gets ignored. An `EXTERNAL`
  coordinate is exit 0 in a record exactly as it is in a ledger, so a
  migration repository does not fail for the state its parity config exists
  to allow.

  **A quotation is not a claim.** A fenced line and an HTML comment are not
  read: `## Paste-ready fixes` is code the tree does not have yet, which is
  what a paste-ready fix is, and marking one up would change the fix somebody
  pastes.

  **The run says how many work items it did not read.** A work item that has
  not written its ledger fragment yet is skipped, and `0 names read` with exit
  0 used to say the same thing for *every record is clean* and *no record was
  opened*. The summary now opens with `N work items read · M unread`.

  One hole is known and left: an untracked or `.gitignore`d file still counts
  as part of the tree, so a scratch note holding a name can silence a refusal
  locally. Closing it means asking git what it carries, and this checker calls
  git for nothing outside `--migrate`. CI reads a clean checkout, where the
  file is not there, so CI is the stricter reader. (#190)

- **`round_record.py new` says what bound the next round is under, as it
  writes the record (issue #207).** The review chain bounds a run one step
  earlier than the cap: after a record whose floor row reads `no`, at most one
  later record may close on a fix, and the record that reads its fixes ends
  the run whatever it finds. That was enforced only at the broad gate — after
  every round of the run had already been spawned — so a session deciding
  whether to spawn again had nothing but the cap, which is a number a prompt
  can carry and is wrong. One work item ran three rounds past the bound with
  both documents open, wrote *"round N of a cap of five"* into every spawn
  prompt it sent, and reverted 37.9 minutes of agent time.

  `new` already opens the previous record to set its `Fixes checked by`, and
  the floor row is a row of the same table, so the answer costs a read it was
  already paying for. It prints nothing where no earlier record met the floor
  — including round 1, because a sentence invented for a state that has none
  is worse than silence — `one reopening remains` where none has closed on a
  fix since, and `this record ends the run` where one has, carrying the same
  four-cell exit the refusal at the gate names.

  **It reads both of the walks the gate runs, because a quiet run is bounded
  by only one of them.** Floor `no`, then two rounds that neither reopened the
  run nor closed on a fix: nothing has closed on a fix, and the gate still
  refuses the third record. Reading one walk printed `one reopening remains`
  at round 2 and invited exactly the round that would be refused. It is also
  silent for a work item old enough that the gate grandfathers it, guarded
  separately for each walk, because a work item can be past one cutoff and not
  the other — one bound really enforced, the other only noticed.

  The floor record it names is the **earliest** whose row reads `no`. Keyed to
  the latest it restarts at every record it stops at and bounds nothing, which
  is the failure the count itself was rebuilt for. (#207)
