- **The review chain's specification is three documents, and each fits under
  the ceiling (issue #526).** `docs/review-chain-spec.md` was 2,246 lines, the
  one document over the 1,000-line ceiling, so no fold could place a rule in
  it. It keeps the review run: the cycle, the bound with the floor, `Needs a
  fix` and the reopening under it, the two records, and the survivor sweep.
  `docs/commit-review-gate-spec.md` takes the hooks and the routing
  declaration, and `docs/round-record-spec.md` takes the round record's rows
  as the pull-request check reads them, with the generator. Every section
  moved whole, and every fold marker with it. Each document opens by naming
  the other two, 22 shipped citations name the file that now holds their
  section, and both READMEs link the gate document. The ceiling's listing
  is empty. A test that forbids a sentence in the specification now forbids
  it in all three documents. The split's own two other items are issues of
  their own: the `Enforced by:` retrofit of older folds (#565), and the shape
  and ceiling checks as plugin commands (#566).
- **A branch that edits cited code re-stamps the row where it stands, and
  that is not an append (issue #488).** The rule that a branch writes
  fragments and never the shared ledger named one exception, a removal. The
  case that arrives most is an edit, which drifts the row, and the only
  correct act was a write two documents forbade. The evidence-ledger policy
  and `CONTRIBUTING.md` now say a removal or an edit is kept true in the file
  the row is in: a claim that still holds is re-stamped, and one the edit made
  false is corrected in place first. That is keeping an existing claim true
  rather than appending, and adding a claim is what goes in the fragment.
- **Of a conflicted ledger row, only the notes are a union (issue #509).**
  Each side's `Re-read` and `Corrected` notes record a reading somebody did,
  so both stay. The anchor's hash belongs to the side that edited the
  anchored unit, and to neither where both did, and a union that keeps a
  stale hash names content that exists nowhere, which `correction-check`
  cannot see. The
  evidence-ledger policy and `CONTRIBUTING.md` say so and say to run
  `evidence-check` after the resolution, and the release checklist's squash
  step names where the rule lives.
- **No shipped file names a concrete release branch outside a sentence of
  history (issue #466).** The pin covered the four files the convention was
  first written on. It now reads every file the hygiene rule reads, with
  three history sentences allowed by name, and `correction-check`'s usage
  line spells `release/vX.Y.Z` rather than an example branch.
- **Three statements about statements are corrected (issue #474).** Two
  ledger rows name the four cases their widened claims rest on. The shipped
  verify skill names SpecSeal where it described SpecSeal's own CI as *this
  repository*, which every installation read as its own. And #423's finding
  4 is called what it was, a narrow reader that named both directions, in
  the gate-steps module and the ledger row that called it *half a pin*.
- **The smith's waiver example says it is the last way past the gate
  (issue #55).** The implementer's definition showed `[no-review]` as the one
  way past the commit gate. It now says the token records something untrue
  of a probe, and that contract §8, which every agent receives, names the two
  shapes to reach for first.
- **`arm-check`'s documentation says what its timeout does not reach (issue
  #316).** The bound is on how long each command is waited for, 900 seconds
  per operator and twice that per arm, and only the command's own process is
  killed. The wrapper form the section prescribes leaves a timed-out suite
  running, so a module whose suite can approach the bound names the pytest
  command directly.
- **The two comments above `kept_broad_gate`'s calls, and the sealer's seal
  sentence, say the newest entry of a same comparison is replaced (issue
  #556).** `round_record.py close` and `seal` each carried a comment saying a
  run the cell already holds is always kept behind the new entry, and
  `agents/sealer.md` said every earlier run is. The call they describe
  replaces the newest entry where it is the same commit against the same
  base, which is the ordinary case of a sealer re-run over an unchanged
  checkout. Both comments now name that replace (`same_run`), and the sealer
  says every earlier comparison is kept. Comments and one definition
  sentence; no behaviour moved.
- **The release checklist's ledger count reads the same before and after the
  split, in zsh as in bash (issue #561).** Step 2 now takes the table-line
  count and the strict checker's exit before `--split`. §3 compares against
  them with one `find` command naming no glob. The old after-command globbed
  the fragment directory the fold had just emptied, and zsh printed `0`.
- **A pipe inside a ledger cell no longer splits the row (issue #562).**
  Twenty-two rows had more cells than their table's header, from a shell pipe
  quoted in a note, which moved the `Checked` column a reader opens. Each is
  escaped with its text otherwise unchanged, and the hygiene module refuses
  such a row in the shared ledger, every release file and every fragment.
- **Confirmed, and nothing to write (issue #268).** The three statements its
  round corrected stand corrected, and a search of the shipped tree finds
  none of them standing.
- **#222 is #559's.** The paragraph saying `depth_two`'s candidates are the
  finding's own file, and why that keeps contract §15 satisfiable, is the
  outside contribution's (#559). This item wrote one too and withdrew it.
- **#331 is deferred.** The census and the tree-wide contradiction check are
  a new instrument, left for the milestone after this one.
