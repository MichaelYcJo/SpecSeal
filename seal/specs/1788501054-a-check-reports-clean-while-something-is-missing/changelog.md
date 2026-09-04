- **A ledger check scoped to one work item's fragment reported clean while the
  shared ledger went stale underneath it.** `evidence-check --ledger
  '<fragment>'` reads that fragment and nothing else, and the narrowing was
  adopted for a correct reason: it is what keeps `--reverify` off a row whose
  claim is false and belongs to somebody else. Carried into READING, it
  blinds. One work item's three review rounds and two fix passes all ran the
  scoped form and all reported ok; the unscoped read at the pull request found
  **fifteen drifted rows and one broken claim**, every one in a file the
  branch had touched, and one of them a claim the branch itself had made
  false.
  **`docs/review-handoff-protocol.md` (draft 1.2) gains a fourth handoff
  requirement**: a command with more than one form names the form, and says
  what the other one is for. Naming the form alone is not enough — a reader
  who does not know what the write's narrowing buys deletes it, and
  `--reverify` then re-stamps the false claim.
  `skills/code-review/SKILL.md` carries the two forms as a table, with the
  repair that looks obvious refused by name.
  **And the tool announces its own narrowing**, because guidance binds only a
  session that reads it and the session this trap was sprung on narrowed the
  command on its own initiative. A `--ledger` run now opens with the ledgers
  it did not read, named one per line, and how to read them. It prints before
  anything is opened — so a glob with a typo in it no longer reports `no
  evidence ledgers found`, which is the sentence a repository with no ledger
  at all gets — and a run that narrowed to exactly what the defaults would
  have opened says nothing. Nothing in a skipped ledger is read: the line is a
  report on what was skipped, not a second pass over it.
  **Two names for one file are one ledger**, matched by inode rather than by a
  spelling of the path, so a case variant on a case-insensitive filesystem, a
  hard link and a symlink all count as read. Comparing paths put a platform
  inside the answer — `os.path.normcase` folds case on Windows alone — and
  `--ledger SEAL/ledger.md` then read the ledger and listed it as unread.
  A file the run cannot identify falls back to its path rather than to a
  shared blank: an inode of 0 is not an identity (Python's own contract says
  so, and CPython's Windows `stat` leaves both fields 0 when it cannot open a
  file), and taken at face value it gave every such file ONE identity — so a
  ledger that was read swallowed every ledger that was not, and the run said
  nothing. Over-reporting is the declared direction here, and silence was its
  reverse. (#153)
- **A round record written after the fixes it commissioned looked exactly like
  one written before them.** `templates/sdd-round.md` says a record is written
  right after the round posts and nothing observed it; measured twice in one
  release, four minutes and two minutes late, and both times the reviewer's
  drafted replacement text lived only in a report and the next segment rebuilt
  it from scratch. A late record leaves no trace, because by then its verdict
  cells read `fixed at <sha>` — which is what a correct record looks like
  after its own update pass.
  **`chain_check.py` refuses a record whose ADDING commit descends from a
  commit its own verdicts name as the fix**, for work items begun on or after
  its `ORDER_FROM` — the fifth cutoff of the shape `STRICT_FROM`,
  `SURFACE_FROM`, `FLOOR_FROM`, `NEEDS_FROM` and `RUNNER_FROM` carry. It is
  the adding commit and never the last one: a correct record IS updated after
  its fixes land, so refusing on the last commit would fail every well-written
  record. Read on every record, like the four rows before it, because the last
  record is the one least likely to be late.
  **Three things it does not refuse**, each of which would otherwise fail an
  honest record: a verdict closing with `answered`, `withdrawn` or `not a
  defect`, which produces no code; a fix commit that is an ancestor of the
  record's own `Target SHA`, which the round already reviewed and therefore
  did not commission — that one is red on the second record of every well-run
  chain without it; and a record with no adding commit in `<baseline>..HEAD`,
  which arrived before the base and about which nothing is claimed.
  **Where a record was deleted and re-added, the LATER add is what counts.**
  That is the only shape producing more than one add, and it is the one that
  makes a late record look early: a stub committed on time, removed, and the
  real record written after the fixes. The version anybody reads was authored
  at the last add.
  **The reach is the commit a verdict cell carries, and that is a bound rather
  than a choice.** Measured across this repository's own records: 235 cells
  close with a fix word, 215 name a commit and 20 do not, and `| fixed |` is
  house style rather than malformed. So a record written entirely that way is
  invisible to the refusal however late it was committed.
  `templates/sdd-round.md` now asks for the commit beside the word, with the
  reason, rather than a sixth refusal being added for a spelling twenty
  existing cells already use — the reach grows as records land and nothing red
  is inherited.
  **The ordering rule made a record's fix surface start out empty, and
  `chain_check.py` now requires the second step.** Because the record is
  committed before its fixes exist, `Contract changes` and `New units` both
  begin at `none — the fixes are not yet written`, and until this landed
  nothing required anyone to come back and fill them — a record that never
  did read exactly like one whose fixes added nothing, and a verifying round
  opening it saw no finding surface at all. A row still saying *not yet
  written* on a record whose `Fixes checked by` names a later round is now
  refused: that round opened the fixes, so they exist, and the cell
  contradicts its own file two rows down. While `Fixes checked by` still says
  `nobody`, the value is the truth and nothing refuses it. Behind the same
  cutoff, so records of earlier work items print.
  This is the one place in the checker whose direction for a value it cannot
  read is **allow** rather than refuse. A rule about which English sentences
  mean *not yet* would be a rule about English, so the phrase is a constant
  the template prints and the checker matches at the START of the reason.
  **What escapes is wider than a rewording**, and three spellings carry the
  template's words unchanged: a dash outside the separator set, a doubled
  space inside the phrase, and any clause in front of it. Only the first is
  punctuation, so widening the separator set would close one of the three and
  leave the claim false about the other two — the limit is written down
  instead, with all three spelled out and a case running them.
  **And the arm keys on `Fixes checked by`**, so it reaches the session that
  filled that cell and stopped, never the one that filled nothing. `nobody`
  beside a pending row prints rather than fails, because that is the state the
  ordering rule requires; `no fixes to check` beside one prints too, and there
  the pair is not merely unrefused but wrong — a round that commissioned no
  fixes will never have any. That is the terminal record of every run, and
  whether it should be refused is a question for the repository owner.
  **What a rebase does to it is stated rather than left to be found.** The
  adding commit is read on the branch, and a rebase replays a branch's commits
  in order, so a passing record cannot be turned failing. What a rebase
  changes is the SHA a verdict cell names, which then resolves to nothing and
  makes no claim — so a rebase can turn a **failing** record passing, and that
  is the safe direction of the two.
  `docs/review-chain-spec.md` carries the subsection, and
  `skills/code-review/SKILL.md` carries the habit that clears it: commission
  the fix pass from the committed record rather than from the reviewer's
  report, which is a message in a session that ends. (#150)
- **Whether a record can be made to carry the artifact it says it verified is
  answered rather than assumed, and the answer is no.** A round record's
  executed-probes row read *"the round's proposed fixes … green, then red in
  every case"* and the record contained none of that code, so the implementer
  wrote its own replacement for the second time in one release. Writing the
  record first is necessary and not sufficient.
  `docs/review-chain-spec.md` names the three checks somebody would write and
  why each fails — a keyword match over free prose is an enumeration over an
  unbounded domain, requiring a fenced block on every record refuses the
  ordinary case, and the content cannot be in a diff at the moment the record
  is written. What remains is a declaration in `templates/sdd-round.md`: a
  probe row whose subject was a **proposed replacement** carries the
  replacement itself, in a fenced block, never a sentence about it. A command
  is reproducible from its own text; a patch is not. (#150)
