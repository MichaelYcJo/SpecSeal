<!-- seal/specs/1789100139-the-file-said-to-delete-it-when-the-last-box-was-ticked/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **`docs/flow.md` is deleted, and this entry is the record of what it
  carried.** It was the third file every branch appended to, after
  `CHANGELOG.md` and `seal/ledger.md`. Those two were cured with per-work-item
  fragments because checkers read them; nothing read this one, so it is cured
  by deletion. No marker is left behind in any file it was removed from — the
  removal is recorded here, in one place, rather than as a trail of notes
  saying a file used to exist. Its 120 lines went four ways:

  - **The order a ticket runs in is now `skills/implement/orchestration.md`
    §*Orchestrator: the order inside a ticket*.** This is the one a person
    has to know: whoever opened `docs/flow.md` each morning for the three
    numbered steps reads them there. It is the first section of that file,
    ahead of the three it already had, because those three are steps inside
    the sequence — step 1 is *write `routing.md` before the first edit*,
    which the routing section then details. Nothing about the sequence
    changed: the draft pull request still opens between the smith and the
    warden rounds, and step 2 still names the framer. The two cases that
    pinned those claims moved with the section rather than being deleted.
  - **The sizing rule is now `docs/issues-and-milestones.md`** — *a release
    is sized in work items rather than in ticket numbers, and three or four
    is the size*, in the paragraph that already says what a `release:`
    milestone holds, with the measurement behind it. It is the only standing
    rule the file carried, and exactly one document states it now. **That
    wording is what this work moved and not what the document says today**:
    the entry below replaces it in this same release with a criterion, and
    names the count as a ceiling.
  - **The 18 checkbox rows and the grounds for their order are on the
    tracker.** Each scheduled release milestone's description states the
    release's purpose and why its issues sit in that order, and a ticket
    whose position had grounds that were in no ticket body gained a comment
    carrying them. Scheduling an issue is one act again — the milestone —
    where it used to be the milestone *and* a line in this file.
  - **The clause naming the file is gone from the 0.4.0 design record**,
    `docs/one-root-by-lifetime.md` §*Order* and its Korean edition. The rest
    of the sentence stands and no version number was added to either, which
    is what marking the path as removed would have cost: both editions are
    in `RECORDS_OF_A_MOMENT` precisely to exempt version tokens.

  Two rules end with the file rather than moving: *a branch writes this file
  for the rows its own work created*, and *a shipped version's section is
  deleted, not kept*. Both were about maintaining it.

  `docs/release-checklist.md` loses four steps, including the one explaining
  how to resolve the conflict this file caused on adjacent lines. The
  quadratic cost that conflict was measured at is still recorded, one bullet
  up, without naming the file. Six live citations were repaired: two in
  `skills/code-review/scripts/survivor_check.py`, one in
  `skills/verify/scripts/broad_gate.py`, one in
  `tests/test_a_corrected_sentence_survives_elsewhere.py`, and in
  `tests/test_release_hygiene.py` the `RECORDS_OF_A_MOMENT` entry with its
  docstring argument and one fixture path. Dropping that entry was measured
  first: seven offending lines remained and all seven were in the file being
  deleted. (#351)
