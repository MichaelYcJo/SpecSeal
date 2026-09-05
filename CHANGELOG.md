# Changelog

## 0.8.1 — 2026-09-05

<!-- specs/1788597030-a-runs-rounds-come-mostly-from-the-tools-own-fixes-and-records -->
- **A review round's record is generated from the two agents' reports rather
  than written by the orchestrator, one cell at a time.** Issue #161 counted
  the branch before this one (#153 + #150): fifteen rounds and 22 h 47 min for
  two features' worth of review. From its 70 commits, with gaps over two hours
  cut to two, **12.8 h of its 18.8 active hours sat in front of record commits
  and 3.6 h in front of fix commits**; 33 of its 65 findings were located in a
  record rather than in code, and 50 of the 61 findings after round 1 sat in a
  file the preceding fix pass had written. The loop that reviewed the tool's
  own paperwork had a gain at or above one, and that is why this release
  exists.
  `skills/code-review/scripts/round_record.py` writes `rounds/round-N.md`.
  `new` takes the warden's report and the round paragraph of the spawn prompt
  and derives every field row from something nobody typed into a cell:
  `Target SHA` from a ref that has to resolve, `PR` from `gh` or `not yet
  opened`, `Fixes checked by` and the two surface rows at their landing
  values, `Needs a fix` and `Loses a record or crashes` from what stands after
  the colon in the report's two lines, the verdict, probe and deferred tables
  copied row for row, `Inherited coordinates` from every earlier record's
  `Location` cells. It sets round N-1's `Fixes checked by` to `round-N` — the
  reach-back the orchestrator forgot five times on the last branch — ticks
  `Pass` when no verdict is open, and runs `chain_check --worktree` before it
  returns, told the pull request is a draft unless `gh` says otherwise.
  `close` takes the smith's fix table and the fix range, applies the verdicts,
  and measures `Contract changes` and `New units` from an AST comparison of
  the range's two ends — every changed signature with the enclosing unit of
  each call site, every added top-level unit with its depth. **A unit at
  depth 2 is refused at the keyboard, before any cell is written**: a `fixed`
  finding whose `Location` sits inside a unit an earlier record's `New units`
  names, in a file the range adds a unit to. The refusal names the unit, the
  finding, the record whose row names the parent, and the exit the rule
  already gives. What the orchestrator still writes by hand is one thing, the
  round paragraph of the spawn prompt, which `new` copies in verbatim.
  Every cell writer takes a structured value: a pipe or a newline anywhere,
  or a comma inside a surface name, is refused before anything touches the
  disk, and there is no `--grounds` or `--note` flag for a session to hide
  prose in. Nothing here commits; the commit is the orchestrator's, made from
  a record it has read. When every verdict closes without a fix word —
  `answered`, `withdrawn`, `not a defect`, `deferred <home>` — both
  subcommands land the record on `no fixes to check` and a bare `none`, from
  one spelling of the derivation, because a round that commissioned no fixes
  will never have any and *not yet written* is false the moment it is
  written. That is the capped run's last record, and the check accepts it.
  Seen red first: every refusal at a named fixture, the two-record reach-back
  read back, the depth-2 refusal on a fixture whose earlier record names the
  parent; 29, 47 and 6 mutations over the three phases' units, none surviving
  a second pass. Prompt budget: zero. The AST comparison reads Python; a file
  it cannot parse, or another language, is read by a diff-line heuristic and
  the cell's trailing comment names the files read that way. (#161)
- **`chain_check.py --worktree` reads the records as the working tree holds
  them, so a check run before the record commit judges the cell it is about.**
  Three 🔴 of the last branch reached CI because the check read `git show
  HEAD:<rel>` and a record edited on disk was invisible to it until committed.
  Under the flag `read_record` opens the file on disk, `changed` includes
  uncommitted and untracked paths so a record just written is judged and its
  `Target SHA` held to the branch, and the first line of the output says the
  working tree was read. **Local only**: CI keeps reading `HEAD`, because a
  working tree that differs from HEAD is what CI never sees and the more
  permissive direction is the wrong one there. Seen red in both directions
  before the flag existed — an uncommitted edit that breaks a record, and one
  that repairs it, each visible only with the flag. Failure direction: at the
  pull request nothing changes; locally it blocks more, on the record about
  to be committed, which is where a refusal costs a correction rather than a
  round. Prompt budget: zero. The path is rebuilt from `/`-split parts with
  `os.path.join`, as the rest of the checker does, and no case ran on Windows.
  (#161)
- **The floor's reopening exception is bounded to one, and a run that would
  reopen twice ends `capped`.** A verifying round that opens something is a
  finding round, its fixes need a reader, and that reader may open something
  again; every record the floor's count stopped at was itself a record that
  met the floor, so the count restarted there and nothing bounded the chain.
  #161 measured fifteen rounds through that door, with the exception used by
  every verifying round of the branch.
  `stopping_floor` now makes a second walk over the same later records, and it
  never stops: it counts every later record whose verdicts closed on a fix,
  wherever it sits, and refuses the second, naming it by file and the floor
  record it follows. The message carries the exit in one spelling
  (`CAPPED_EXIT`): every finding still open becomes an issue, its verdict
  reads `deferred #N`, the record's `Fixes checked by` reads `no fixes to
  check`, and the pull request says `chain: capped`. Keyed to `REOPEN_FROM`,
  whose value is the id of the work item that added the rule — the seventh
  cutoff of the shape `STRICT_FROM` … `ORDER_FROM` carry — so earlier work
  items print and nothing red is inherited. `docs/review-chain-spec.md`
  §*The reopening — one, and then the run is capped* owns the rule; the
  skill, the template, the protocol and the warden link to it in one sentence
  each, where four of them used to state the unbounded version.
  **The vocabulary the exit needs.** `deferred <home>` joins `CLOSED_WORDS`
  and not `FIX_WORDS`: `deferred #170` and `deferred seal/follow-up.md` close
  a finding on the issue or the file it went to and produced no code, so `no
  fixes to check` beside them is the truth and a last record whose every
  verdict reads that way may tick `Pass`. A bare `deferred` — the word with
  nothing after it, or only a separator — stays OPEN and comes back as
  `deferred (no home)`, the direction every verdict the checker cannot read
  takes: it says something was left and not where. `templates/config.md`'s
  list of strings no language row governs carries the word.
  Seen red: each refusal at a named fixture before the walk existed, the
  cutoff at the boundary second, the capped run's legal end, the bare word
  through a ready pull request; the well-written two-record run kept green,
  and this repository's own records pass under the new arm. Nine mutations
  over the walk and the vocabulary, nine killed. **Failure direction: blocks
  more.** A run that reopens twice is refused where it used to pass. What it
  lets through, stated rather than left to be found: a defect the second
  reopening would have found ships as an issue rather than as a round — the
  trade `questions.md` Q2 chose with the alternative on the table, since
  removing the exception entirely would have shipped round 7's floor bug and
  three Windows defects of the last branch as issues too. Prompt budget:
  zero. The walk reads records through the same reader as every other check,
  with no platform-dependent path in it. (#161)
- **Nine rules bind a review run, each stated by one carrier and linked from
  the others, so a run's rounds come from the code rather than from the
  tool's own fixes and records.** Where each one lives, with what it
  measures:
  1. A finding whose `Location` is a record (`seal/specs/**`,
     `seal/ledger/**`, `seal/ledger.md`) is a correction and not a round —
     what `chain_check` or `evidence_check` refuses is corrected in the
     closing commit, what they do not read is prose, and `Needs a fix` does
     not count it. Owner `docs/review-chain-spec.md` §*The last round
     verifies*, with the count: 33 of 65 findings located in records, records
     55 % of the diff.
  2. A fix pass may not add mechanism — a rule, a checker, a template
     section, a walk. A finding closable only by one is an issue and the
     verdict is `deferred #N`; the depth rule already refuses the second
     level, this is the first. Owner `skills/code-review/SKILL.md` §*A fix
     pass adds the unit that pins it*, with round 4 of the last branch as the
     measurement: a rule, a reader and two cases built to close one 🟡, at
     the cost of round 5's 🔴, issue #159 and half of round 6.
  3. 🟡 means *a defect the release would ship* — the tool does something
     wrong or tells a person something wrong. ⬜ is new beside it: a sentence
     that reads badly while the behaviour and the fact stay right, fixed in
     passing or not at all, never counted by `Needs a fix`. Half of the last
     branch's 53 🟡 were true sentences about prose. Owner the skill's
     §*Findings format*; `agents/warden.md` §Report puts the one question per
     finding.
  4. The reopening is one and the run ends `capped` — the entry above.
  5. A fix pass owes code and a test. It writes no `phases/phase-N.md` and no
     `plan.md` row; the fix table in its hand-back is its record and
     `round_record.py close` writes the rest. Owner `agents/smith.md`.
  6. The draft pull request opens at the end of the build, before round 1, so
     the platform legs run beside the chain; three Windows-only defects
     arrived after round 12 on the last branch. Owner the skill's
     §*Orchestrator: the pull request opens before round 1, and a phase is
     re-run*; `docs/flow.md`'s order inside a ticket carries the step.
  7. A session that has compacted hands the next round to a fresh one, and
     the generated record is the handoff. Owner the same skill section.
  8. A moratorium on new parsed fields in `round-N.md` and new rows the
     ledger must carry, until the next minor release. This work adds a
     subcommand and a verdict word and no field. Owner the spec's §*What the
     record carries*.
  9. A hand-back's verification claim is a claim: before the orchestrator
     spawns the next phase it runs the closed phase's suite and the lint of
     its changed files itself and reads the output; the broad gate still runs
     once, after the rounds settle. Owner the same skill section as 6;
     `docs/review-handoff-protocol.md` gains §*After a phase — the hand-back's
     claim is re-run*.
  `tests/test_the_rules_have_one_owner.py` holds the same table as pins: the
  owner states each rule, every link names its owner, and a walk over `docs
  skills agents templates` holds the count rule's phrase to the owner and its
  links. Every changed sentence was seen red with the sentence stashed — 40
  mutations over the three owner files and 24 over the five linking carriers,
  none surviving. Every sentence that said the orchestrator writes a record
  cell now names the generator; the three that are about the reviewed-HEAD
  mark, which the orchestrator does write, were left true. (#161)
- **The warden's report carries the record's three tables in the record's own
  column headers, and a fix pass hands over a fix table.** `agents/warden.md`
  §Report asks for `## Verdicts`, `## Executed probes` and `## Deferred`
  beneath the findings prose, with `| # | Finding | Location | Verdict |
  Grounds |`, `| What was run | Result |` and `| Finding | Where it went | Who
  answers it |` — the generator's parser and the warden's headers are one
  constant, pinned across both files, so a finding that is not a row of the
  verdict table reaches no record and no orchestrator prose sits in a parsed
  cell. The two terminal lines are unchanged. `agents/smith.md` and
  `skills/implement/SKILL.md` §5 give the fix pass `## Fixes` with `| # |
  Verdict | Commit or grounds |`, one row per open finding — `fixed` with the
  commit, `answered` with the grounds, `deferred <home>` with the issue or
  the file — and `round_record.py close` applies it; the depth of a unit the
  pass added is measured by `close` from the diff rather than declared in the
  hand-back. `templates/sdd-round.md` says the record is generated by `new`
  and closed by `close`, keeps its comments as documentation of fields a
  generated record does not copy, and offers `deferred <home>` in the verdict
  vocabulary; `templates/sdd-phase.md`'s `Ran by` comment names the
  `--ran-by` value the generator writes. The reports themselves are saved to
  the session's scratch directory and not committed: the generated record is
  their durable form, and a second file per round would be one more file the
  checker had to learn to ignore. (#161)

## 0.8.0 — 2026-09-05

<!-- specs/1788472135-the-run-outlives-its-last-finding -->
- **A review run now has a floor as well as a ceiling, and a fix pass now
  has a bound on what it may create.** Three rounds, and five while a 🔴 is
  open, was a ceiling with nothing under it, so it got spent like a budget:
  #81 ran seven rounds and the last three found nothing that leaves the root
  and nothing that crashes. `docs/review-chain-spec.md` and
  `skills/code-review/SKILL.md` now state the floor — **stop when a round
  finds nothing that leaves the root and nothing that crashes** — and say
  where the rest of what that round found goes, which is deferred with a
  named answerer or an issue. The reviewer answers it in a line of its own
  the way it already answers `Needs a fix`, `agents/warden.md` carries that
  line in both the passage that explains it and the report format a reviewer
  copies from, and `round-N.md` gains a row of the same name:
  `| Loses a record or crashes | no |`, or `yes — <what>`. It is a second
  terminal condition rather than the first one reworded, and the two come
  apart — a round can need a fix and still stop the run — so the three files
  that called `Needs a fix` *the* answer the run ends on now call it one of
  two. **The verifying round is what the floor leaves standing**: a record
  that met the floor may be followed by one more, the round that reads the
  diff of the fixes that closed it, and a second one is the run carrying on
  past its own stopping rule.
  **The rounds the floor removes are the rounds that were reading what each
  fix pass created, which is why the second half ships in the same release.**
  Measured across four rounds of #82, three consecutive rounds found their
  finding inside the previous round's fixes, every time in the unit the fix
  added rather than in the fix itself — by construction the fix ships
  reviewed and the unit it added ships unreviewed, in one commit. The bound
  is **a fix pass may add a unit; that unit's fix may not**, stated in
  `skills/code-review/SKILL.md` and `agents/smith.md`, and `round-N.md`'s
  existing `New units` row now carries the depth of each entry —
  `unit (depth 1)`, entries separated by `;`. The depth goes per entry rather
  than in a row of its own because one fix pass can answer a finding in old
  code and a finding inside an earlier unit in the same breath, and one
  number for the round would be false of one of them. **Where a refused unit
  goes is written in the same sections as the rule**, one phase ahead of the
  check that refuses it, so no session meets *this unit may not exist* with
  nowhere to put it.
  **`chain_check.py` reads both rows at the pull request rather than leaving
  them for whoever is awake.** A missing floor row fails; an empty cell, a
  word that is neither answer, and `yes` with nothing after it fail on any
  record; and a `no` followed by two or more later round records fails,
  naming the exit. A `New units` entry with no depth fails, one at depth 2 or
  above fails with the two places the unit goes instead named in the message,
  and one carrying two units under a single `(depth N)` — the comma spelling
  the row used before the depth existed — fails as well. `none`, with or
  without a reason, stays an answer to `New units` as it was, and a trailing
  `;` on it no longer turns it into something else.
  **`Needs a fix` stops being a row nothing reads**, which is what keeps the
  bound above from refusing the one sequence the documents require. A
  verifying round that opens something is a finding round, so its own fixes
  need a reader, and that reader is a third record; the count therefore stops
  at the first later record whose `Needs a fix` says the run reopened. The
  row takes the floor's `no` / `yes — <what>` vocabulary and the same cutoff,
  and it is grandfathered whole rather than only when absent — it carried
  free text for three releases with nothing reading it, so a value written
  earlier was held to no vocabulary.
  **`docs/review-handoff-protocol.md` moves to draft 1.0**, with the floor
  row, the depth and the separator in `New units`, the depth's own adoption
  cutoff, and a section for the floor and what may follow a stopped round.
  **Older work items are not made red.** Both rules are keyed to the id of
  the work item that wrote them, the way `STRICT_FROM` and `SURFACE_FROM`
  already are: a record whose work item began before the cutoff prints
  instead of failing, because a merged record has no honest repair and a run
  that went past its floor can only be repaired by a round nobody can spawn
  now. A row that is present and malformed is refused at any age, since
  formatting is always the author's.
  **What no check can see, recorded rather than parsed away:** a depth
  declared wrong — `(depth 1)` on a unit that is really second-level. The
  rule is a declaration, and the verifying round reading the `New units`
  surface is what looks at it. `templates/config.md`'s list of what a
  `Record language` row does not govern grows by the new field name, the
  `depth` marker and the floor's `no` and `yes`, so a repository writing its
  records in another language is told which words stay English. (#110, #117)

<!-- specs/1788486395-the-roll-opens-the-next-log-with-no-body -->
- **A measurement that only meant something across versions was being written
  to the issue the next release deletes.** Two issues collect the same shape
  of comment — the rolling `flow-measurement` log, which
  `.github/scripts/roll_flow_measurement_issue.py` closes and replaces every
  time a release reaches `main`, and a durable ledger that is kept across
  versions — and `skills/verify/SKILL.md`'s "Measure the segment, and feed the
  flow log" named only the first. So a rate held against a previous version's
  baseline went where it would be discarded, which happened on 2026-09-04 and
  is what #136 opened for. The section now says which reading goes to which: a
  segment's own numbers to the rolling log, readings that span versions to the
  durable one. **A repository declares its durable log with a `flow-baseline`
  label** — the same lookup shape as the rolling one, a label rather than a
  number, and the same exactly-one-open invariant. A repository that never
  creates it is unaffected, because an absent label is the no-op it already
  was.
  **Zero open used to be one fact and is now two.** A repository that never
  measured and one whose log stopped both read zero, and only the second is a
  broken invariant. `gh issue list --label flow-measurement --state all` tells
  them apart for one call. A session that finds the second **names it and
  opens nothing**: two sessions finishing segments at the same moment would
  both read zero and both create, and the next release then fails on two or
  more, which is the same invariant broken from the other side.
  **Every rolling log used to be born empty.** The roll passed `--body ""`, so
  a new log said nothing about what it was for and carried no path back to the
  one it replaced. It now opens carrying the issue it rolls from, the version
  it closes on, and the durable ledger — found by the `flow-baseline` label
  rather than hardcoded, and left out of the sentence entirely where a
  repository has none.
  **The same create asks for this repository's index label and its `log:`
  milestone, and neither can fail a release.** A milestone is repository state
  that gets renamed and deleted, and `gh issue create` fails the whole call on
  a name it cannot resolve, while the invariant this script protects is the
  one-open rule that no milestone touches. The create is attempted with both,
  then with the label alone, then with neither, and each fallback writes into
  the body of the issue it opens what the attempt above it could not set — the
  body, because that is the artifact a person opens and a workflow log is not.
  A failed attempt re-reads the open-issue list before retrying, so a create
  that reported failure after it had actually landed ends the ladder instead
  of opening a second issue.
  **This repository's own durable log (`#51`) carries the new label**, so the
  0.9.0 log opens pointing at it without anything further being done by hand.
  (#136)

<!-- specs/1788491830-a-segments-record-says-what-it-cost -->
- **A segment's record said what it was asked, what it found and which commit
  it read, and never what ran it.** Every segment of two work items was
  metered this week and posted to the flow log, and not one of those readings
  can be attributed afterwards — they all ran on the same model, and that fact
  lived only in a session transcript. `templates/sdd-phase.md` and
  `templates/sdd-round.md` now carry a `| Ran by |` row, and
  `docs/review-handoff-protocol.md` (draft 1.1) carries it in the field table
  with its `Required` column answered.
  **The row names the agent AND the model**, joined by the word `on` —
  `specseal:smith on <model>`. Either half alone answers neither question the
  numbers raise: an agent without a model cannot be compared against another
  run of the same agent, and a model without an agent cannot be told apart
  from the orchestrating session's own turns. The joining `on` is a word
  rather than a punctuation mark on purpose, because a separator inside a code
  span splits the cell carrying it and that has bitten these records twice.
  **It is the spawning session's row, never the segment's own.** An agent is
  told what it is, so a value it writes about itself is the value it was told,
  and the model is a spawn-time argument the orchestrator chose —
  `agents/*.md` pins none. It is the reach-back `Fixes checked by` and the
  fix-surface rows already make. `skills/code-review/SKILL.md` and
  `skills/verify/SKILL.md` both say so, because they are read by different
  sessions at different moments.
  **`unknown — <why>` is an answer and a bare `unknown` is not**, in the shape
  `nobody — <why>` already has. A session spawning through another harness may
  genuinely have no name for a model, and a vocabulary offering only the
  confident answer gets the confident answer written whether or not it is
  true.
  **`chain_check.py` reads the row**, so it is enforceable rather than true
  only while somebody is awake. An absent row fails for work items begun on or
  after `RUNNER_FROM` and prints for older ones — the fourth cutoff of the
  shape `STRICT_FROM`, `SURFACE_FROM` and `FLOOR_FROM` already carry, because
  a merged record has no honest repair: nobody can recover what ran a segment
  whose session is over. A row that is present and unreadable is refused at
  any age, the split the fix-surface rows already make.
  (#137)

<!-- specs/1788501054-a-check-reports-clean-while-something-is-missing -->
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
  **The floor's count now stops at a record that wrote fixes, not only at
  one that reopened.** The walk read `Needs a fix`, which is the reviewer's
  answer to *what did I open*; the bound needs *were fixes written that owe a
  reader*, and the two come apart when the orchestrator fixes a 🟡 the
  reviewer said could be answered with grounds — because it ships, as a
  false count in a ledger fragment does. The row then reads `no` over fixes
  that exist, and the run had no terminal record any exit accepted: the
  reader after the `no` was a second uncounted record, and stopping at the
  `no` was refused both ways. Measured on this work item's own seventh
  round. The verdict column already carried the fact — it is what refuses
  `no fixes to check` beside `fixed` — and the walk reads it there now.
  ALLOW, one record wider in one sequence, and the cheaper mistake: the
  other way to satisfy the old walk was rewriting `fixed` to `answered`
  over fixes that exist. Three quiet rounds are still refused, because
  `answered` writes nothing.
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

## 0.7.0 — 2026-09-03

<!-- specs/1788445862-a-phase-hands-the-next-one-a-record -->
- **A build phase now leaves the same committed, per-segment record a review
  round already does, and both records now say what they were asked to do
  as well as what they found.** What a phase discovered used to reach the
  next phase only if the orchestrator retyped it into the next spawn prompt,
  and it went missing without a trace when it didn't: phase 4 of an earlier
  work item moved a rule out of `agents/smith.md` into an interim home, and
  phase 5 removed that interim home before the rule had actually reached
  anywhere else, deleting it from the repository with nothing recording that
  it had gone missing (#107, #121). New `templates/sdd-phase.md` mirrors
  `templates/sdd-round.md`'s shape for the build side: a field table
  carrying only `Phase` and `Commit` — a phase has no `Target SHA` to
  squash away and no `Pass` checkbox to answer — then `## What this phase
  was asked`, `## What this phase found`, and `## What this phase removes`
  (a table naming what left the tree and where it must land; `none` is a
  valid row, a blank table is not). `templates/sdd-plan.md`, `agents/smith.md`
  and `skills/implement/SKILL.md` are wired to it, so a spawned session
  writes `seal/specs/<work-item-id>/phases/phase-N.md` at each phase's close
  without having to be told twice.
  **Separately, neither a round record nor a phase record said what it was
  *asked* to do, only what it found.** #81's round 1 was the cheapest round
  measured — 7.6 minutes, 29 tool calls, one 🔴 and four 🟡 — because its
  spawn prompt named eight specific things to try to break, in order; that
  fact was recoverable only from a transcript. `templates/sdd-round.md`
  gains `## What this round was asked`, between the field table and the
  verdicts, and `skills/code-review/SKILL.md` instructs the orchestrator to
  copy the round-specific spawn content into it right after posting (#119).
  **Enforcement is a template blank plus a skill instruction, not a gate.**
  A `chain_check.py` refusal for a missing section was considered and set
  aside: it would need a red test, a stated failure direction, a prompt
  budget and a platform-honesty case for a mechanism that has shipped zero
  records yet to measure a cutoff against, and is revisitable once real
  phase records exist to learn from.
  **Two follow-on questions from #119 — naming which plugin version or
  commit ran a segment, and a `CONTRIBUTING.md` paragraph on the
  plugin-copy-in-force confusion — are explicitly out of scope here** and
  recorded as deferred, per the issue's own scoping, rather than silently
  dropped. (#121, #119)

<!-- specs/1788449488-measure-what-flow-finds -->
- **Measuring a smith or warden segment and logging what it found is now
  automatic, in every repository this plugin installs into, instead of a
  message a person had to remember to retype.** Issue #109: the instruction
  used to live only in one operator's own memory file, naming a fixed issue
  number that went stale twice. `skills/verify/SKILL.md` gains "Measure the
  segment, and feed the flow log" — after every segment, find this
  repository's open `flow-measurement`-labelled issue
  (`gh issue list --label flow-measurement --state open`) and post
  `session_cost.py`'s numbers to it; where no such issue is open (nearly
  every installed repository, today), the step is a no-op — nothing is
  measured, nothing is posted, nothing asks. A new
  `.github/scripts/roll_flow_measurement_issue.py`, wired into
  `close-issues-on-release.yml`, closes the current log and opens the next
  one — titled with the release's version bumped to the next minor — every
  time a release reaches `main`, so the log keeps growing without anyone
  opening the next issue by hand. This repository's own log (`#89`) is
  labelled as part of this change, so `0.8.0`'s issue opens on this
  repository's own next release without further action.
  **The rollover script retries once before treating "no issue open" as the
  invariant broken**, not on "more than one open": a search-index lag right
  after a label write can only ever undercount what is actually open, never
  overcount, so only a zero reading gets a second look. Found while building
  the label bootstrap in this same branch — `gh issue list` returned empty
  immediately after `gh issue edit --add-label`, while `gh issue view` in
  the same breath showed the label already applied.
  **Filed separately, out of this branch's scope: `agents/smith.md`'s
  mutation-testing instruction says to clear `tests/__pycache__` between
  mutations, and that is not the only cache a mutated module can leave
  behind** — a script loaded from `.github/scripts/` by path, the way this
  branch's own new tests load the file under test, caches its bytecode under
  `.github/scripts/__pycache__` instead, and a stale copy there survived one
  mutation's restore long enough to fail an unrelated later test run.
  `docs/flow.md`'s "While the flow runs" section — the instruction this work
  replaces — is deleted, and the two boxes it names as done (`#121 + #119`,
  `#109` itself) are ticked. (#109)

## 0.6.0 — 2026-09-03

<!-- specs/1788433011-every-spawn-prompt-is-retyped-from-memory -->
<!-- seal/specs/1788433011-every-spawn-prompt-is-retyped-from-memory/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **The rules every agent works under now live in one file the agent already
  has, instead of being retyped into each spawn prompt from memory.** Half of
  every prompt was identical to the last one, so a rule that failed to be
  recalled went missing with nothing recording that it had. It had already
  happened twice: one rule arrived at round 2 of a seven-round chain and
  round 1 ran without it, and another arrived at round 3 after two rounds had
  each rediscovered it. The new `agent-contract` skill is that file — sixteen
  numbered sections holding what is true of `smith`, `warden`, `scribe` and
  whichever agent is added next: how an exit code is read, what an agent must
  not run, what a spawn prompt may narrow and may not widen, which labels a
  report keeps apart, what reaching an agent in prose is worth, what an agent
  must not write, how a probe is named and how it drives git, that edits go
  through the `Edit` tool, how reads and runs are batched, what language the
  records are written in, where a `seal/…` path resolves, and the four method
  lessons the review chain paid for. **It arrives with nothing typed**: each
  agent's definition lists it under `skills:`, so it is injected at startup,
  before the agent's first tool call, and no agent resolves a path. A section
  number is never reused and never re-ordered, so a prompt can say *§3 is
  narrowed this round* and a round record still means the same thing when
  someone opens it six months later.
  **One thing you will see that is not an agent's behaviour.**
  `agent-contract` appears in the skill listing, because that listing is how
  the harness injects it. It is not a procedure to invoke: its frontmatter
  carries `user-invocable: false` and its description says it is injected
  into agents rather than run.
  **Each agent definition keeps only what is its own.** `agents/warden.md`
  keeps where it works — a `git clone --no-local` at the target SHA, with a
  `uv` venv because `pytest` is not installed for the system interpreter —
  its report format, the verifying round's re-derivation, and the records it
  must not write. `agents/smith.md` keeps the specification set, the design
  gate, the routing declaration, vertical slices, mutation-testing what it
  added, its hand-back and the 3+ Fix Rule. `agents/scribe.md` keeps
  resolving the original checkout, an absence carrying its search, and facts
  with coordinates and no verdicts. What each had been duplicating is gone
  from all three, and a definition that carries a section's own sentences
  again fails the suite rather than passing unnoticed.
  **`docs/review-handoff-protocol.md` stops being the interim home**, which
  it had named itself since it was written, and moves to draft 0.9. The
  section that carried those rules is a pointer at the contract and the
  definitions, and what stands in its place is the one rule that was always
  the document's own: a prompt carries what is specific to the round and
  nothing else.
  **The orchestrator is bound by the same contract**, and the two skills it
  reads — `implement` and `code-review` — say so. It never opens
  `agents/*.md`, so a contract reaching only the agents would have missed the
  party whose forgetting started this: the headline failure was an
  orchestrator breaking a rule it had put into every prompt it sent.
  `user-invocable: false` permits that load and does not oblige it, which is
  why the obligation is written where the orchestrator reads. (#107)

## 0.5.0 — 2026-09-03

<!-- specs/1788354065-the-tree-that-must-stay-clean-has-no-way-to-opt-in -->
- **A repository that must not carry the plugin's files in its tree can
  opt in: local mode keeps the whole root under the git directory.** The
  root lives at one of two places and the hooks read whichever exists, in
  order: `<repo>/seal/`, which is committed and is shared mode, then
  `seal/` under the common git directory (`git rev-parse --git-common-dir`),
  which is local mode — shared by every linked worktree of the clone, never
  a commit candidate, and needing no `.gitignore` line. There is no config
  key. Every hook that opens a file under the root resolves it the same
  way — the commit gate's declaration and the path its stop text tells you
  to write, the implementer notice, the review-history guard, the evidence
  advisor, the ledger migration and `evidence-check`'s defaults when the
  plugin's own copy runs (the copy `evidence-ci` vendors into `tools/`
  reads `<repo>/seal/` as before) — and the one sentence a session needs is
  in the `implement` skill and at the top of both agents: every `seal/…`
  path means `<repo>/seal/` where it exists and
  `$(git rev-parse --git-common-dir)/seal/` otherwise. What local mode
  gives up, stated in the README and in the root's own README: the
  pull-request checks read committed files, so CI cannot run them there,
  and a new machine or a re-clone starts empty. Switching is a move and a
  commit, documented under *Shared or local* in the README; export and
  import arrive with #81.
  **Nothing here writes to your tree without being asked. What arrives
  unasked, on its own line: first setup asks one more question, once —
  shared or local, shared first — in the batch the `implement` skill
  already asks, and a repository with `seal/` at either place is never
  asked.** Shared creates `<repo>/seal/` in the tree, which the routing
  commit carries, and writes the pull-request checks to
  `.github/workflows/hygiene.yml` from the new `templates/hygiene.yml`
  only when that file is absent — it clones the plugin at the release
  installed at setup and runs the chain check and the unverified-rows
  check. Local creates the root under the common git directory, installs
  nothing and touches nothing in the tree. The session-start migration is
  unchanged — a repository on the 0.3.x layout committed the plugin's files
  and is moved into `<repo>/seal/` — except that a repository whose root is
  already at either place is marked as moved, so a local-mode repository
  that later checks out a branch still carrying `.specseal/` is not moved
  into the tree it chose to keep clean.

<!-- specs/1788360817-the-pull-request-language-is-fixed-inside-a-skill -->
- **A repository can say what language its pull requests are written in,
  and the skill reads that instead of requiring English of everyone.** The
  new `seal/config.md` holds one markdown table in the shape `parity.md`
  already uses, and its first row is `Pull request language`. Where that row
  names a language, `commit-pr-convention` writes the commit subject, the
  commit body, the pull request title and the pull request body in it — all
  four, because a squash makes them one text. **No file and no row both mean
  English**, so a repository that says nothing behaves exactly as it did
  before, and nothing is created for it: the file is written by a repository
  that wants a non-default, from the new `templates/config.md`. The root is
  resolved the two-place way, `<repo>/seal/` then
  `$(git rev-parse --git-common-dir)/seal/`, so local mode carries a config
  too.
  **Three things the row deliberately does not reach**, stated in the skill
  and again in the template, because the person writing the config reads the
  second and never the first: the prefix vocabulary is not translated
  (`feat:` stays `feat:` — it is scanned in a log and parsed by tooling);
  branch names stay ASCII, since a branch name is typed into a shell and
  pasted into a URL; and the response language, what the session says to
  you, remains a person's own setting, because two people in one repository
  can want different answers there and the same one here.
  The translated body is now named for **its own** language rather than the
  body's — `pr.<lang>.md`, so an English repository keeps `pr.ko.md` and a
  Korean one keeps `pr.en.md`. Nothing in this repository is renamed: the
  name was under-specified rather than wrong.
  Nothing in `hooks/` reads the file, and that is a decision rather than an
  omission: judging what language a commit message is in means being wrong
  about names, identifiers and quoted English, and a gate that guesses stops
  a correct commit. The mechanism is the skill's text, as it already is for
  the prefix vocabulary.

<!-- specs/1788395377-the-release-guard-globs-one-place -->
- **The release guard looked in one place for a file two work items kept in
  another (issue #96).** `fold_ledger.py` refuses a release while any work
  item still has an open row in `evidence-todo.md` — a fact a reviewer
  verified that never reached the ledger — and it finds those files with
  `seal/specs/*/evidence-todo.md`. Two work items kept theirs one directory
  deeper, under `rounds/`, so the guard was blind to two of five. Nothing
  was hidden: both carried a `drained` line. What was gone is the meaning of
  the guard's silence for those two, and the next open row written there
  would have passed a release without a word. The four misplaced files move
  to the level `docs/review-handoff-protocol.md` names, where every other
  work item already keeps them, and a test pins the layout rather than the
  glob — the glob is one line and the layout is written by hand once per
  work item, so the layout is the half that drifts. Found by asking what the
  guard's glob actually reaches, during another work item's review round.

  **And the rule is now said where a session meets it.** The reminder
  `hooks/review-history-guard.py` prints after a review is posted names the
  two todo files at the work item's own level, spelled from the same base as
  the round record beside them, and `docs/review-chain-spec.md` says the same.
  The `code-review` skill says why: `round-N` is the only member of the set
  that is plural and unbounded, so it is the only one that gets a directory.
  The protocol already said where the files go, and the sentence a session
  actually reads at the moment it creates them did not.

<!-- specs/1788398967-local-modes-records-never-leave-the-clone -->
- **Local mode's records can be carried to another machine, and taking one
  in never overwrites what is already there.** Two new commands,
  `seal export` and `seal import`, on the Bash tool's PATH while the plugin
  is enabled. Local mode keeps the ledger and the work-item records under the
  common git directory, so a new machine or a re-clone starts with nothing —
  that is the mode's whole trade-off, and it now reads as *take a copy*
  rather than *lose it*.
  `seal export` writes the root, and only the root, to
  `seal-<repo>-<date>.zip` beside the clone, with a manifest naming the
  remote URL and the HEAD SHA at export. **The smith mark, the worktree
  choices, the review and parity marks, every lease and the export's own
  state sit beside the root**, so none of them travels: the export walks the
  root and nothing else, which is why the design requires the root to be its
  own directory. A symbolic link inside it is skipped and named rather than
  followed — the one way out of that structure.
  The zip lands beside the clone rather than in it, because the ordinary
  place to run the command is the repository root and an untracked zip there
  is one `git add -A` from committing the records local mode exists to keep
  out of the tree. `--output` overrides it and says so when the path is
  inside the tree.
  **`seal import` never overwrites and never asks.** A file that is not there
  is added; one that is there with the same bytes is left alone, so
  re-importing the same zip writes nothing at all; one that is there with
  different bytes gets the incoming copy beside it as
  `<name>.incoming<ext>` — `ledger/<id>.incoming.md` next to
  `ledger/<id>.md` — and the collision is listed. Which of a pair is right is
  a reading rather than a merge, and no answer the command could pick would
  avoid sometimes throwing work away. It names `evidence-check .` as the next
  step instead of running it and reporting a pass nobody read.
  It refuses, writing nothing, for a zip from another repository (with
  `--allow-other-repo` where the two are one repository under two spellings —
  ssh at one machine and https at another compare equal), for a member that
  would land outside the root, and where both roots already exist.
  `--into shared` or `--into local` creates the named mode's root, which is
  the second way to switch modes.
  **In shared mode `seal export` writes no zip.** The records are committed,
  so every clone and CI already have them, and a zip would be a second copy
  that nothing keeps current. It prints the path and the `mv` that switches
  to local mode, and exits 1 — so `seal export && cp seal-*.zip …` does not
  copy nothing and report success.
  Once per release, `seal export --check` prints one line — how many work
  items changed since the last export — and uploads nothing anywhere. Where
  the copy goes is the user's business. It counts work items only, so a
  change confined to `follow-up.md` reports 0; the line's wording is fixed by
  the design, and widening it is recorded as an open question rather than
  taken silently.
- **One claim was corrected by measuring it, and the correction is why the
  import is stricter than it was designed to be.** This work was planned
  around "`extractall` is the classic path-traversal sink". On the CPython
  the plugin ships on that is false: it already strips `..` and a leading `/`
  from a member's name, and writes a symbolic-link entry as an ordinary file.
  What actually disqualifies it is that it **overwrites**, and that it writes
  through a symbolic link in the destination. That second one is a real
  escape, the import's own writer had it too, and it is now refused before
  anything is written. The member-name validation was kept regardless: a
  defence that holds only while a standard-library sanitiser keeps its
  current shape is not one this plugin can claim.
- **Review then measured the same claim one level down and found it still too
  narrow.** The check that closed the escape walked every directory above a
  member and stopped short of the member itself, so a symbolic link named for
  the record was never looked at. A broken one reads as absent, so the file
  was treated as new and written straight through the link, outside the root,
  at exit 0 with nothing printed. The check now covers the leaf, and three
  documents that called the directory case the only way out say what was
  measured instead.
- **Review then found the same escape one name over, and it is closed at two
  levels.** A collision does not write to the member's name — it falls back to
  `<name>.incoming<ext>`, and the check that refuses links had never seen the
  fallback names. A broken link there read as absent, so the copy was written
  straight through it, outside the root, at exit 0 and printed as an ordinary
  collision. The sender of the zip chooses whether the collision happens at
  all, by sending bytes that differ. Every candidate name is now read as a
  link rather than as a file, and the write itself opens with a flag the
  kernel refuses to follow a link through — so a name that becomes a link
  after it was checked is refused too.
- **An import now refuses a zip that declares more than a root of records
  holds, and a zip whose data does not match its own checksums.** Each member is read whole, and the zip arrives from another
  machine, so its declared sizes are the sender's choice: a 408 KB file
  declaring 400 MB in one member wrote 419 MB and took as much memory, in
  0.2 s. A member is capped at 32 MB and an archive at 512 MB, and the total
  is summed before the manifest is parsed — that read is unbounded too, so a
  400 MB `manifest.json` used to take 400 MB of memory on its way to being
  rejected. A bad checksum was the other way in: a zip whose central directory
  is well formed and whose data is corrupt used to write the records before
  the corrupt one and then die on a traceback, which is a partial import from
  a zip that chose to be one.
- **Two smaller corrections.** A clone holding both roots is now refused
  however the import is asked, including with no `--into` flag — the case the
  specification and both READMEs describe was the one spelling that still
  wrote. And a repository with no commit yet records an empty SHA in the
  manifest rather than the four letters `HEAD`, which is what `git rev-parse`
  prints on its way to exiting 128.
- **The third round opened the half the first two never had, and found the
  same shape there.** Both earlier rounds read the import. `seal export`
  writes its zip to a temporary name first, so a failed write leaves no half
  archive — and that name is `seal-<repo>-<date>.zip.partial`, beside the
  clone, which anyone can predict. A symbolic link planted there took the
  manifest and every record outside the clone at exit 0, while the command
  printed `wrote <path>` for a path that was the link. The temporary name is
  now opened with the same flag the import writes with, and the zip's own name
  is read as a link rather than as a file — a check whose docstring claimed
  the import shared it, which is why the import's fix never visited it.
- **A zip can no longer end an import in a traceback.** Three ways in: a
  member the build cannot decompress, an encrypted member, and a corrupt
  manifest — the last one because the manifest was read before the data was
  checked. The checks now run in one order, largest question first: how many
  members, how many bytes, what the names are, whether the data reads, and
  only then what the manifest says. A member count is bounded too, because
  both size bounds count bytes and a zip of 300,000 empty members wrote
  300,002 files into the root at exit 0.
- **And a name that has to be a directory for the zip and is a file is
  refused before anything is written.** `os.makedirs` raised on it mid-write,
  leaving the records before it on disk. The sender corrupts nothing to reach
  it — two members named that way is enough — and the root's own contents
  raise it from the other side.
- **The fourth round found no way out of the root, and one thing the fix
  before it had broken.** Refusing to write through something at the export's
  temporary name also removed it — a link, a file somebody left, or a
  concurrent export's archive still being written, which loses that export the
  zip it was about to rename. The cleanup that removes a half-written archive
  is for a name this command created, and it now runs only for one.
- **A zip can no longer end an import in a traceback for a reason the
  filesystem gave, either.** The check for a name the zip needs as a directory
  asked whether it was a file, and a named pipe is not a file — it walked past
  and met the same crash. And nothing at all guarded the write loop: a
  directory in the root that cannot be written into, or a full disk, left a
  partial copy and a traceback. Both stop with a line of their own now, and
  the second says what is true — this command overwrites nothing, so running
  it again finishes the copy.
- **A zip from a later version of this format is told so.** The name checks
  ran first, and a later format is exactly what moves the names they read, so
  a zip declaring format 2 was answered as a malformed zip rather than as a
  build too old. The format field exists for no other day.
- **Two messages stopped sending people to the wrong place.** A clash inside
  the zip told a person to rename a file that was not on their machine, and
  the Korean README described that clash as always coming from their own clone.
- **The last round found no way out and no crash the change had caused, and
  one the change had walked past.** A manifest is another machine's file, and
  this build checked that it was an object and that its version number was one
  it reads — every other field was trusted to be the kind of thing it looked
  like. A manifest naming a commit but no time raised at the closing line,
  *after* every record was written: the person saw a Python traceback and exit
  1 for a copy that had succeeded, and exit 1 reads as nothing happened. Those
  fields are read as text or as absent now.
- **And a name that means the manifest to one check meant a record to
  another.** `manifest.json/` was exempt from the name rules as the manifest
  and outside the size bound as not-the-manifest, so it could declare any size
  at all. Both spellings answer to both checks now.
- **Three sentences and a table row that described something else.** Both
  READMEs said the import writes nothing when it stops, and the round before
  had added a stop that writes. The refusal for a zip from a later version of
  this format was in no document a person is pointed at. And the ledger row
  saying which bounds are read before the manifest was wrong a second time, in
  the same place.

<!-- specs/1788411058-the-mode-is-two-shell-lines-in-a-readme -->
- **Switching between shared and local mode is a command now, and a
  repository can say which mode it wants before the folder moves.** It was
  two shell lines in `README.md`'s *Shared or local* section — correct, and
  unfindable — and a repository arriving from the 0.3.x layout landed in
  shared without ever being asked, which put the people most likely to want
  local mode in the place least likely to tell them it was still available.
  `seal mode` prints where the root is, what `seal/config.md`'s new `Mode`
  row says it should be, and whether the two agree. `seal mode local` and
  `seal mode shared` switch; `seal mode --apply` switches to what an edited
  row says; `seal mode --check` writes nothing and exits non-zero on a
  disagreement, which the pull-request checks now run so the row cannot
  quietly become a document that lies.
  **The row is what the repository wants and the folder's location is what
  it has.** Nothing at runtime reads the row — every hook still resolves the
  root by looking for `<repo>/seal/` and then `<git-common-dir>/seal/` — so a
  gate can never be sent looking in a place with no folder. It has no default
  either: an absent row is filled in from where the folder actually is, which
  is an observation rather than an assumption, and is the state of every
  repository that has a `config.md` today.
  **Beyond the two shell lines it does what a `mv` cannot.** It refuses when
  the other mode's root already exists, refuses when the index carries a
  change under `seal/` or the workflow path, carries
  `.github/workflows/hygiene.yml` in and out, and writes the row so the file
  and the folder agree afterwards. It stages; you commit.
  **Carrying the workflow file is the part that is easy to mistake for
  tidiness.** Measured in a repository with no `seal/`: the two checks it
  runs fail in opposite directions — one goes red on every pull request
  forever for a repository that did the right thing, and the other goes green
  having examined nothing. Left behind, a switch to local turns the build red at the first of them.
  **The two directions do not cost the same, and the command says so before
  it acts.** Going to local takes the records out of the tree and every other
  clone loses them at the next pull, which is what `seal export` and `seal
  import` are for. Going to shared is the one to be sure about: the commit,
  not the move, is the point of no return, and until it lands
  `git reset -- :/seal :/.github/workflows/hygiene.yml` and then `seal mode
  local` walk the whole thing back.
  The rename runs first and every step after it is idempotent, so a stopped
  run — or a person who already ran the README's `mv` by hand — is finished
  by running the command again rather than refused. (#104)

<!-- specs/1788420760-a-language-row-that-governs-four-things -->
<!-- seal/specs/1788420760-a-language-row-that-governs-four-things/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **A repository can say what language this plugin writes in, and it is two
  answers rather than one.** The row that shipped as `Pull request language`
  governed four things — the commit subject and body, the pull request title
  and body — and everything else this plugin wrote stayed English whatever it
  said. So a team working in Korean got Korean pull requests and English
  specifications, which is a pull-request setting wearing a language
  setting's name. It is now `Commit and pull request language`, which is what
  it always governed, and it takes the review report posted to a pull request
  with it. A second row, `Record language`, governs the prose in the
  work-item records: the specification, the plan, the memo, the questions,
  the changelog fragment, the round records' cells, and a ledger row's claim
  and grounds.
  **The two are independent.** Setting one does not carry the other, because
  an absent row's default is what every repository had before that row
  existed, and a row inheriting another's value is not that. Three
  combinations, which are the three people want: everything English, the
  commits and pull requests in the team's language with the documents in
  English, and both.
  **Prose follows the rows and structure does not.** What stays English in
  every repository, whatever either row says: the commit prefix vocabulary,
  branch names, all code, and every string a checker reads literally — a
  round record's field names, its verdict vocabulary and its `Pass` checkbox,
  the `<!-- -->` markers, a `drained` line, and a ledger anchor's
  `path#unit@hash`. A translated field name is not a translation; it is a
  checker that stops reading. (#106)

<!-- specs/1788420761-the-settings-live-in-a-file-nobody-opens -->
<!-- seal/specs/1788420761-the-settings-live-in-a-file-nobody-opens/changelog.md
— gathered into `CHANGELOG.md` at the release. -->

- **`/specseal:config` shows what this repository decided for itself, and
  changes any of it.** Three rows live in `seal/config.md` — the language the
  commits and pull requests are written in, the language the records are
  written in, and which of the two places the root lives at — and until now
  the only way to see any of them was to open a file nobody has a reason to
  open. First setup asks its questions once and never again; this is how to
  ask them later.
  It shows rows that are absent as well as present, with the default and
  where it comes from, because a row a repository never set is the most
  likely one somebody wants to change. For the mode it runs `seal mode` and
  reports what that says — the folder, the row, and whether they agree —
  rather than reading the row itself, since a second reader is a second
  answer.
  **A change is routed to whatever owns that row.** A language row is only a
  row and is edited in place. The mode row moves a directory, stages a
  commit, and installs or removes the pull-request workflow, so the skill
  runs `seal mode` and reports that list rather than saying *done*. Before
  switching to shared it says what cannot be undone: the commit, not the
  move, is the point of no return. (#105)

## 0.4.0 — 2026-09-02

<!-- specs/1788326734-the-ledger-fragments-are-never-gathered -->
- **The ledger fragments fold into `map.md` at the release, and an open
  evidence-todo row refuses it.** A work item writes its evidence rows to
  `.specseal/map/<work-item-id>.md` so two branches never queue at one file,
  and nothing ever folded them back: the directory gained one file per work
  item forever and almost every pull request touched it. Release preparation
  now runs `.github/scripts/fold_ledger.py --version X.Y.Z` beside the
  changelog gather, in the same commit. It moves every fragment into
  `.specseal/map.md` under a `## X.Y.Z — <date>` heading, one `###` section
  per work item marked with `<!-- specs/<work-item-id> -->`, copies every row
  byte for byte, and removes the fragment. A row is a content anchor, so
  `evidence-check` reports the same thing before and after; measured on this
  repository's own ledger, 55 rows across six fragments all arrived. The same
  step refuses to run, naming the file, while any `specs/<id>/evidence-todo.md`
  in the tree has an open row: a row in a file with no `drained` line whose
  first cell does not begin with ✅. `--dry-run` prints and writes nothing;
  `--check` reports a fragment left behind or an open row, and the hygiene
  workflow runs it on every pull request into `main`. Both halves work on
  today's paths, so the root merge only re-points them. `CLAUDE.md`,
  `CONTRIBUTING.md`, both READMEs, `docs/branch-and-release.md`, the
  `implement` and `evidence-check` skills and the two templates no longer say
  a ledger fragment is never gathered.

<!-- specs/1788331011-two-roots-hold-three-lifetimes -->
- **Two roots become one, laid out by lifetime, and the opt-in is the
  folder.** `specs/<id>/` held a work item's documents and its review
  records, which die at different times, and `.specseal/` held the ledger,
  whose rows outlive the work item. Both now live under `seal/`:
  `seal/specs/<id>/` for the whole work item, `seal/ledger.md` and
  `seal/ledger/<id>.md` for the rows, `seal/follow-up.md` and
  `seal/parity.md` as they were, `seal/README.md` for the export rules. A
  repository is opted in when `seal/` exists at the root (or under `.git/`,
  the place local mode will use); `.specseal/` opts nothing in any more, and
  the throwaway opt-out is the file `.git/specseal-scratch`, which cannot be
  committed. **Behavior that writes to your tree without being asked,
  disclosed on its own line: at the first session start after updating, a
  repository with the old layout is moved once.** Every move is a staged
  `git mv`, `seal/README.md` is rewritten from the template, the ledger rows
  that cite a moved file are re-pointed with their hashes untouched, one
  line says what moved, and the person reviews `git diff --cached` and
  commits. That commit belongs to no work item, so inside a session the
  commit gate asks; `: '[no-review]'; git commit …` waives it for the one
  command, with `[no-parity]` beside it where `seal/parity.md` exists.
  Until that session start every gate is silent in that
  repository, because the signal it reads has moved. A tree with
  uncommitted changes under `.specseal/` or `specs/` is refused with a line
  saying to commit first and retried at the next clean start; a move that
  stopped resumes; a repository carrying `.specseal/scratch` is left alone;
  the once-per-repository marker is `~/.claude/specseal/root-migrated`. To move by hand instead, run the sequence in the README's *Coming up from
  0.3.x*: it creates `seal/specs`, then does one `git mv` per entry of
  `.specseal/` and per work item, removes the two emptied directories, and
  ends with `evidence-check --reverify .`, which re-points each row citing a
  moved file. Every gate, checker and release
  script reads the new paths; the `<!-- specs/<id> -->` markers in
  `CHANGELOG.md` and the ledger are unchanged; the chain check no longer
  judges a declaration that a pull request only renamed; `templates/map.md`
  and `templates/specseal-README.md` are `templates/ledger.md` and
  `templates/seal-README.md`. Nothing is deleted: a work item's directory
  lives until a later `settle` folds it.

## 0.3.0 — 2026-09-02

<!-- specs/1788272986-the-fixes-are-what-open-the-next-round -->
- **A round record names its fix surface, and the check refuses to lose it.**
  Ten regressions on one work item each traced to the fix that opened it, and
  the largest class — four of ten — was a fix that changed a unit's contract
  while not every place that contract reaches was revisited. The diff names
  the changed signature; only a search names the reach; a person reading the
  diff missed all four. So `round-N.md` carries two new rows, filled in when
  the fixes land by the session that already has the fix diff open:
  **`Contract changes`** — every unit whose signature, return arity, return
  type, or set of returnable values the round's fixes changed, each with the
  call sites it reaches (`unit → site, site`, units separated by `;`) — and
  **`New units`**, the top-level definitions and constants the fixes added.
  `chain_check.py` refuses a record without them and refuses a unit listed
  without its reach; `none` is an answer, with or without a reason. Records
  of work items begun before the rule landed print instead of failing — the
  same grandfathering `Fixes checked by` carries, keyed to a new
  `SURFACE_FROM` cutoff — so no merged record goes red. The verifying round
  treats what `New units` names as a finding surface (*is this correct*)
  rather than a verification surface, because a unit the fixes created has
  been reviewed by nobody: the one measured fix commit that created eight
  new units carried defects in four. The handoff protocol moves to draft
  0.7 with the two rows. (#57)

- **Four review-skill rules from the same measurement.** The comparison axes
  table gains a **security row** — who can reach the path and as whom, the
  trust of inputs at OS and process boundaries, whether each failure fails
  open or closed, what a crafted name, path, or payload reaches — because
  security was named in stage 2 and absent from the table, and the table is
  what makes an axis mandatory. The paste-ready-fix rule gains its second
  clause: **a fix touching an OS boundary states its assumed precondition**
  (path resolution, file modes, symlinks, subprocess working directory,
  encoding) — the first clause covers invented names, this covers unexamined
  premises. And two closings are refused in writing: **an enumeration over
  an unbounded domain is a recorded limit, not a closed finding**, and **a
  mutation score licenses *tested*, never *safe*** — stated where the number
  is reported, since three consecutive rounds each reported a perfect score
  and all three were rounds whose fixes opened findings. A third written
  rule, **a document claim gets a pin**, is what the new tests themselves
  practice: every new sentence above is pinned by
  `tests/test_the_fixes_name_their_surface.py` or
  `tests/test_review_axes.py`. (#57)

<!-- specs/1788276387-the-windows-step-never-reaches-its-guard -->
### Fixed

- The evidence-ci guard test resolves the interpreter on Windows: the bash
  step quoted `sys.executable` with backslashes, so the step failed before
  its guard ran and the Windows CI leg has been red since the test landed.
  (`1788276387-the-windows-step-never-reaches-its-guard`)

<!-- specs/1788277657-one-bar-misreads-two-of-the-three-segment-kinds -->
- **The per-segment acceptance bars are written rules, and one bar no longer
  misreads two of the three segment kinds.** The meter the handoff protocol
  points at (`session_cost.py`) had numbers and no rule about what they mean;
  the one figure that existed anywhere was a single acceptance bar on an
  issue, right for a reviewing segment and wrong for the other two. The
  protocol (draft 0.8, §After the run) now says it: a reviewing segment is
  judged on tools per turn **≥ 1.8** (measured range 1.29–1.89, the batched
  round at 1.89 the fastest); an implementing segment on **`repeats = 0`**
  and calls per deliverable, never on tools per turn — an edit-test loop is
  inherently serial (1.08–1.17 measured); a verifying segment is exempt. At
  very small rounds the ratio has few independent batches to rise on (a
  23-call round read 1.64 doing everything right), so the bar is a lens for
  rounds of ordinary size, never a refusal threshold — no gate fails a round
  on it. (#51)

- **A fix pass resumes the implementer instead of respawning it.** The
  code-review skill's orchestrator sections said when the verifying round
  runs and nothing about how the fixing session is obtained. Now they do:
  resume the session that built the branch — its context already holds the
  files, the tests, and the grounds — and spawn fresh only when that session
  no longer exists, with the handoff before round 1 as the price. Measured
  three times with no counterexample: fresh spawn 282 calls / 45 minutes
  (#33); resume 30 calls / 3.9 minutes (#29) and 26 calls / 5.2 minutes
  (the #57 chain). (#51)

- **Q1 of the meter work item is answered: the advisory stays at 1.2.** The
  script cannot tell a reviewer's transcript from an edit-test loop, so its
  threshold sits where it does not nag the serial case; the bars above are
  the orchestrator's instrument, applied knowing the segment kind.
  `session_cost.py` itself is unchanged. (#51)

<!-- specs/1788302682-the-release-check-never-watched-bin -->
- **The release check watches `bin/` now, and a test says which roots it
  watches.** The hygiene step that asks a pull request into `main` for a
  version bump filtered the diff through five roots — `skills/`, `agents/`,
  `hooks/`, `templates/`, `.claude-plugin/` — and `bin/` was not one of them,
  although the plugin loader puts `bin/` on the Bash tool's PATH while the
  plugin is enabled. A pull request fixing only a wrapper would have shipped
  without moving the version, which is the one way an update reaches nobody.
  `bin/` is in the pattern; `docs/branch-and-release.md` names it with the
  others; and `tests/test_the_release_check_watches_what_ships.py` classifies
  every tracked top-level entry as shipping or staying home, so the next
  `commands/` or `output-styles/` fails the suite until somebody decides,
  instead of falling out of the pattern the way `bin/` did. Nothing else that
  a user runs directly lives outside those roots: `install.sh` is run from a
  clone, never through the plugin. (#10)

<!-- specs/1788305134-the-reader-stops-where-it-need-not -->
- **The command reader stopped commits it did not need to stop, and once
  it stopped asking it answered where it should have refused.** A path the
  command wrote out for itself one segment earlier is a path the gate can
  read: `SB=/abs; git -C "$SB" commit` names `/abs`, and the gate's answer
  is byte-identical to the written-out form. Nothing this process cannot
  see is guessed at — `git -C "$WT"` from the environment, `$SB/r$n` in a
  loop, `$(pwd)` and `$1` all still reach the ask — because the substitution
  runs in FRONT of the test that refuses them rather than replacing it. A
  `((` inside a `${…}` word is a word to both paren models, so the heredoc
  below it opens and `echo ${x:-((} <<EOF / cd /target / EOF / git commit`
  is judged where the shell is rather than where the body says. A refused
  segment that carries no name — `fi`, `then echo hi`, a subshell — keeps
  the names the command has written, where every refusal used to empty
  them and `if …; then … fi` prompted for that alone. That aim was proven
  against bash rather than assumed, and the proof found 82 shapes it had
  opened: a body's SECOND statement arrived as a top-level assignment and
  bound, so `if false; then echo hi; SB=/three; fi; git -C "$SB"` answered
  `/three` where bash has `/one`; and `! for SB in …` passed as a simple
  command because only the first word met the reserved-word test. A stack
  of open bodies runs beside the name environment now, and a statement
  inside a body is forgotten rather than bound — a stack, because a
  multi-line `case` puts its arm pattern `a )` where a subshell's closer
  stands and an integer count took it for one. A call to a function the
  string itself defined empties the names it holds, an array assignment
  `SB=(x)` empties the name rather than binding `(x)`, and `((SB=…))`,
  `let` and `${SB:=…}` forget it. The differential that found all of this
  is in the tree as `tests/test_the_reader_agrees_with_bash.py`: whatever
  the reader answers, bash must answer the same, and a prompt is exempt.
  `agents/warden.md` and `agents/scribe.md` say how to write a scratch-repo
  probe that commits without raising the prompt.

<!-- specs/1788310269-the-implementer-leaves-a-mark -->
- **The routing declaration's third axis has a reader now.** `Implementation`
  said whether `smith` or the session builds a work item, and nothing looked at
  the answer again — a session could declare `smith`, build the whole item
  itself, and leave a record saying otherwise. Two hooks close that. When
  `smith` is spawned, a gate in the `pre-agent` group writes the checked-out
  branch name to `.git/specseal-implementer` and prints nothing, so it can
  neither deny nor ask. After a command that actually runs `git commit`, a
  reminder in the `post-bash` group prints one line naming the declaration
  where it answers `smith` and no mark stands for this branch — once per
  session per repository, never a decision, and silent when the mark stands,
  when the row is absent or unreadable, or when it answers `the session`. The
  commit gate's verdict is byte-identical with the row and without it. Both
  fail toward "no mark", which is toward a reminder: a mark gate that quietly
  stops running turns the notice on rather than off. A mark gate broken on
  disk leaves the worktree guard's verdict in the same group untouched, which
  is the objection issue #26 recorded against putting a second gate there,
  measured. `hooks/routing.py`, `templates/sdd-routing.md`, the README's gate
  table and `docs/review-chain-spec.md` no longer say the axis is read by
  nothing.

## 0.2.0 — 2026-09-01

<!-- specs/1788229400-every-branch-appends-to-the-same-two-files -->
- **Every branch appended to the same two files, and one of them broke at the
  merge.** Three branches ran in parallel on 2026-09-01, touched 34 files, and
  shared exactly one — `CHANGELOG.md`, in all three pairs. Nothing else
  overlapped at all, so parallel work was never what conflicted: appending to
  one three-line region was. The cost is when the conflict arrives, after the
  broad gate has run and before the pull request opens, where nothing may be
  edited — so resolving it buys a second run of the whole broad gate. Both
  registries are now written one fragment per work item, and no two work items
  share an id. **A changelog entry goes in `specs/<work-item-id>/changelog.md`**
  and `.github/scripts/gather_changelog.py --version X.Y.Z` concatenates the
  ungathered ones into a dated section at the release; `--check` reports any
  that never arrived, and the hygiene workflow runs it on every pull request
  into `main`, so a release cannot ship a change with no entry. Each gathered
  entry sits under an HTML comment naming its work item — invisible to a
  reader, and the only link from a released entry back to the work that
  produced it. Matching the text instead would have worked once: any later
  copy-edit to a released entry would make its fragment read as ungathered
  forever. `## Unreleased` is gone with the region it named. (#46)

- **A ledger coordinate names content, not a position.** A row cited
  `path/file.py:120-134`, and a line number moves for edits that have nothing
  to do with the claim — so inserting a line above a cited function left the
  row pointing at the wrong lines while still reporting OK. Everything built to
  manage that was compensation: the coordinate rotted, so the row was
  re-anchored, so whatever it was measured from reset, so a stamp was needed,
  so a squash orphaned the stamp.

  **A row now cites `path#unit@hash`**, and `path#unit>place@hash` where a
  claim rests on one statement inside a large unit. The unit is a function or
  class for code and a heading path for a document. `.py` is read with the
  stdlib `ast`; every other language falls to a rule that needs no parser and
  no dependency — the name followed by `(`, `{`, `=` or `:`, then the block to
  the next line at the same or lower indentation, which lands on a closing
  brace because that brace sits at the declaration's own indent.

  **An anchor degrades to DRIFTED, never to BROKEN.** The two cost different
  things: BROKEN says *go edit the ledger*, which is the bookkeeping this
  removes, and DRIFTED says *go re-read the claim*, which is the work the
  ledger is for. So only the unit can be BROKEN. A narrowing anchor whose
  place has changed widens back to its unit and reports DRIFTED — precision
  buys a smaller hash, never a new way to fail. Narrowing is an escape hatch
  rather than a habit: cite the unit, and reach past it only where whole-unit
  hashing has been measured to drift rows on unrelated edits.

  A document anchor is a heading rather than a sentence, because a sentence
  breaks on any rewording while a heading survives the prose beneath it being
  rewritten.

  **Behavior that writes to your tree without being asked, disclosed here on
  its own line: an existing 0.1.0 ledger migrates itself.** At the first
  session start after updating, in an opted-in repository, every `path:line`
  row is rewritten to the new form — stamps dropped, dates kept, and where
  git can produce the file at a row's old stamp, a cited range whose content
  changed since that commit is left loud rather than rewritten onto whatever
  sits at those lines now — and one line tells you what happened:
  *ledger migrated to anchor format (12 rows; 2 left…) — review the diff and
  commit*. `claude plugin update` is the whole of what you do. The write is
  deterministic, idempotent and all-or-nothing per row; the old text stays in
  git history; rows it cannot prove are left, named, and keep failing the
  ordinary check loudly (`OLD-FORMAT`, exit 2) rather than being guessed at.
  It runs once per repository, never over an uncommitted ledger file — the
  dirty check covers exactly the files it would rewrite, and a dirty one is
  skipped with one line and retried at the next clean session start. Fallback for CI or by hand: `bin/evidence-check --migrate .`, which
  the `OLD-FORMAT` line also names.

  **Two behaviours arrive without being asked for.** After a `git commit` in
  an opted-in repository, a broken anchor prints one advisory line in the
  terminal — the row, where its content went if that is provable, and the
  `--reverify` remedy. It never blocks, and it is silent when the ledger is
  clean or absent. And where a BROKEN row's content provably moved — renamed
  in place, or moved to another file, judged by content identity across a
  bounded repo-wide scan — the check names the destination, and
  `bin/evidence-check --reverify .` re-anchors it mechanically; a whole-file
  rename heals the same way. The hash covers the region under the
  anchor with trailing whitespace and blank lines removed, so a reformat is not
  a change; indentation is kept, because in Python a dedent moves a statement
  out of the block it belonged to.

  The verdicts follow from that. **BROKEN** where the anchor is gone, or where
  it resolves to several places and none of them holds the content the row
  recorded — where one of them does, that is the row's place and the run is
  clean. **DRIFTED** where the content under it changed. **OK** prints the
  region's current line numbers, for a reader to open. There is no baseline,
  no stamp and no commit SHA in any row, and the check calls git for nothing
  — the one exception is `--migrate`, which consults the old stamp's commit
  before it trusts a line number it is rewriting.

  **Re-verifying a row is recomputing its hash**, so it has a flag:
  `evidence-check --reverify` rewrites every resolvable row and names what it
  changed. It is deliberately separate from the check — one that refreshed what
  it was checking would report OK for ever — and it leaves a row whose anchor
  is gone alone, because that is the one row somebody has to look at.

  What this closes rather than manages: a stamp a squash can orphan, a row
  whose coordinate resolves while pointing at the wrong lines, a coordinate
  into a file newer than the baseline that could never drift, and a row that
  was stale the moment it landed because another branch changed the cited code
  and merged first. That last one had been recorded as unreachable; a content
  hash sees it on the first run, because there is no time window to look at.
  (#12, #14, #23, #31, #52, #56)

- **The evidence checker stops answering for files it never read.** Nine fixes
  from the fifth review round, each with a case that was seen failing against
  the unfixed code first.

  **A ledger nobody can read now fails the build.** A permissions failure, a
  directory named `.md`, an I/O error — all three used to be indistinguishable
  from an empty ledger, and the run printed all zeros and exited 0. The check
  reports the file as broken, `--migrate` counts it among the rows it left,
  and `--reverify` exits non-zero. Nothing about this is new behaviour anyone
  relied on: a green build over a ledger nothing checked is the state the
  `OLD-FORMAT` verdict exists to prevent.

  **A coordinate is now confined to the repository it is placed in.** A row
  spelling a path that climbs out of the tree — `../elsewhere/file.py#name` —
  was read from wherever it landed, and `--reverify` wrote back a hash of what
  it found there. It is refused in all three commands: broken in the check,
  left by `--migrate`, and untouched by `--reverify`. Whoever writes a ledger
  already has write access to the repository, so this crosses no boundary in
  an ordinary project; it matters where a repository is checked out but not
  trusted, because the plain check and the session-start migration both read
  what the ledger tells them to. Present since 0.1.0 in the `path:line` form,
  so this is a new guard rather than a repair. The containment test is against
  the checkout the row was placed in, not always the root, so a `--map` prefix
  still reaches its own checkout.

  **The ledger writer now follows a symlink and writes the file behind it.**
  A symlinked ledger used to be replaced by a regular file: the real ledger
  never updated, stayed stale, and the command reported success. The rename is
  still atomic, and the mode is carried over — every ledger was being demoted
  from 0644 to 0600, which git does not track outside the exec bit and which
  therefore never appeared in a diff.

  Following the link is a deliberate reversal, and it is the part of this
  entry worth arguing with. A writer that replaces the name it was given never
  writes outside the directory it was pointed at, and that is usually the
  behaviour preferred at a write boundary. It is traded here for the silent
  data loss above, on the grounds that the ledger path is the repository
  owner's own: `.specseal/map.md` and `.specseal/map/*.md`, in a tree whoever
  points them elsewhere can already write to. What would change the answer is
  a ledger path that is not owner-controlled — one taken from an environment
  variable, a command-line argument in a shared runner, or a checkout a
  session does not trust — and at that point the link should be replaced
  rather than followed.

  **The rule that decides what a declaration is now reports how sure it is,
  instead of being asked to be right.** For files this skill reads without a
  parser — everything that is not Python — a list of keywords used to settle
  whether a line declares a name or merely uses it, and that list was wrong in
  both directions at once. It refused two real declarations whose modifiers
  are statement keywords in another language, C#'s `public new void
  Render(int x)` and Swift's `case loading(String)`, reporting live code as
  broken. Letting them back in when nothing else survived then resurrected
  plain call statements, so a function moved to another file with
  `return render(y);` left behind read as though it were still there — and
  `--reverify` made that call site the row's permanent anchor.

  No list of keywords separates those two cases, so the answer stops being a
  list. The rule marks a candidate that survived only by being put back, and
  the two commands act on the mark rather than trying to tell declarations
  from calls themselves.

  - The check accepts such a place only where its content reconstructs the
    row's own recorded hash. Otherwise the unit is gone, and the answer is
    broken-with-the-destination-named — the same answer Python already got
    from its parser, and the one this path was missing.
  - `--reverify` refuses to write onto such a place at all, and prints why. It
    is the command that produces the hash, so it has no hash to compare
    against.
  - What that costs, stated: a declaration whose modifiers look like statement
    keywords and whose content changed in place is re-verified by hand. The
    command names the row rather than skipping it silently.

  A bare `render(1);` is refused on structure rather than vocabulary — nothing
  before the name, and the statement ends — which is kept alongside all of the
  above because it needs no evidence at all. Swift, Kotlin, Go, Ruby and Lua
  end no statement with a semicolon, so the same shape is treated as uncertain
  wherever it spans a single line, and the span is what keeps a real
  declaration out of it: `render() {` opens a block, `render(y)` does not.

  **A row citing a unit the rule is unsure of is written by hand, and the
  check now says how.** It names the place and the hash it holds, so recording
  it is a copy rather than a computation. `--migrate` refuses such a place the
  same way `--reverify` does, with one exception it can prove: where the old
  stamp's commit holds the cited lines unchanged, the person's own line
  numbers vouch for that place and the row migrates.

  **Every row the check calls broken or drifted gets a line back from
  `--reverify`.** Two paths used to answer with nothing at all — a Python unit
  that is gone with no provable destination, and a row whose narrowed claim
  went stale, which is the row the check literally ends with *re-verify*.
  Silence from a heal command reads as a heal that happened.

  **`--migrate` reads the file under the root it was given.** Run from a
  subdirectory, the proof that a cited line range had not moved since its
  stamp was read against a same-named file elsewhere in the repository: an
  untouched row was refused forever, and a row whose look-alike happened to
  match was rewritten and reported as proved.

  **A `--map` declaration no longer turns the rename scan off for local
  rows.** One declared prefix used to switch the scan off for every row the
  run could not place, so a purely local file rename lost both its
  `(moved?)` hint and its `--reverify` heal. A row whose prefix is not among
  the declared maps is a local row and keeps its scan. An unprefixed row in a
  repository declaring `.specseal/parity.md` or `--default-repo` stays
  undecidable — it may be citing the original repository, and nothing in the
  coordinate says which — so those rows keep the scan off, and the skill's
  Known limits now says that the loss is any move rather than a renamed
  directory, and that it costs the `--reverify` heal as well as the hint.

  **The migration that runs itself now prints the warning the typed command
  prints.** `--migrate` reports how many rows were rewritten without the
  since-the-stamp proof; the session-start hook dropped that count, so the
  path a person asked for warned and the path nobody asked for was silent —
  and it never asks twice.

  Known limits also gains two entries it was missing: a one-line constant is
  the most collidable of the boilerplate twins, since substituting the name
  leaves nothing but the value, and a nested `def` is anchored by its
  qualified name — `outer.inner` — with the short name alone resolving to
  nothing until `--reverify` re-anchors it.

- **Three more things the checker used to answer for without having read
  them.** Found reviewing the fixes above.

  **A row read through `--default-repo` is confined to that checkout.** Two of
  the three ways a coordinate is placed already refused a path that climbs out
  of the tree it names; the third did not, so a source file symlinked out of
  the checkout was read and reported clean.

  **`--reverify` stops answering a broken row with silence.** Where the check
  says a row is ambiguous and tells the reader to look, running the heal
  command printed nothing at all, which reads as a heal that happened. Every
  row it leaves alone now gets a line saying which row and why.

  **A declared `--map` prefix no longer affects rows that do not carry it.**
  The per-row test that replaced the per-run one was written with a term that
  could never fire, because a row carrying a declared prefix is resolved into
  the mapped checkout before the question is asked. The term is removed; the
  behaviour it was meant to produce was already there.

## 0.1.0 — 2026-09-01

- **The cost meter could not count above 1.00 tools per turn, and a day's
  conclusions were drawn from that floor.** `session_cost.py` counted a turn
  per `tool_use` block, so a message carrying three calls was three turns
  and the batching ratio was structurally pinned at ~1.00 — five runs of two
  agent types measured exactly 1.00, including a session that demonstrably
  batched. A turn is now one assistant **message** that carries at least one
  tool call, keyed by the message id (a message split across transcript rows
  is one turn; a transcript with no ids degrades to one turn per row — the
  old floor, never an inflated ratio). A message's tokens count once however
  many calls it carries, and model time runs from a turn's last result to
  the next turn's first call, so the wait between two calls issued together
  is no longer booked as thinking. The `batching` advisory stops claiming
  calls go out "one at a time" when the ratio is above 1. Readings taken
  with the old meter are not comparable to new ones: the same six
  transcripts that all read 1.00 read 1.08–1.89 recounted per message. (#29)

  Around the meter, three smaller things move what that measurement run
  established into the documents that outlive it. `docs/review-handoff-protocol.md`
  (now draft 0.6) gains **the handoff before round 1**: the coordinates-carry
  rule applied to the orchestrator→implementer handoff, each handed fact
  labelled executed / read / unverified — an unlabelled fact is an assertion
  nobody has opened, and one such fact (a count standing in for a claim)
  reached five documents before a review round found it false. The same
  section names `plan.md`'s Status column as the progress channel an
  orchestrator reads while an implementer runs — time since it last advanced
  is the stall signal — and finally points at the meter itself, which had
  sat unreferenced through a full day of measurements nobody took. And both
  agent contracts state the batching expectation the meter can now observe:
  independent reads and probes go out together, with the honest caveat that
  an edit-test loop is inherently serial and is not forced to fake a batch.

- **A review run ends with a round that reads the last set of fixes, and the
  record says who did.** A round's findings are closed after it ends, by
  whoever writes the fixes, and the round that follows is what opens them.
  Every round had one except the last, whose fixes were written by the
  session that then ticked `- [x] Pass` on its own record. Measured across
  two consecutive work items: the one round that ever looked at another
  round's fixes found **seven** defects inside them, and its own fixes then
  went in unread. (#33)

  Two changes, and they meet at one cell.

  A run now ends with a **verifying round** — spawned after the previous
  round's fixes are committed, targeted at the diff of those fixes rather
  than at the branch, and asking whether each closed finding is actually
  closed. **A round that opens nothing needing a fix does not consume the
  cap**, because the cap counts rounds that found something and a round that
  finds nothing is the loop having converged. The three-round and five-round
  numbers are unchanged. This is not the rule that a round has to find
  nothing: a 🟡 the smith answers with grounds has opened nothing needing a
  fix, and the run ends there.

  And `round-N.md` carries `| Fixes checked by |` beside `Pass`. `Pass` says
  the findings are closed; this says who opened the work that closed them.
  Three values and no others — `round-N` naming a LATER round, `no fixes to
  check`, or `nobody — <why>`. `chain_check.py` reads it on every record and
  refuses what the repository can contradict: a round naming itself, a
  checker git does not carry, a checker whose own `Target SHA` is the same
  commit as this record's or an ancestor of it — the number is later and the
  review is not — and `no fixes to check` beside a verdict that closed with a
  fix. Where either record's `Target SHA` names two commits — the row allows
  both when HEAD moved mid-review — the newest on each side is compared.

  A verdict cell is read by stripping markdown emphasis and matching the
  vocabulary against the START of the cell, so `**fixed** \`sha\`` counts as
  the fix it is whatever follows the word, while a long `answered` cell that
  mentions a fix made elsewhere still does not. The first version instead
  looked for where the commit began and cut there, which meant it had to
  recognise a commit: a seven-character abbreviation with no digit in it —
  about one in 959 — was not recognised, nothing was cut, and a blocking
  finding that had been properly closed read as still open.

  And `round-N.md` carries `| Needs a fix |`: whether this round opened
  anything that does. It is the reviewer's own answer, copied rather than
  re-derived from the verdict table, because a finding the implementer answers
  with grounds needs no fix and still ends the run. No check reads the row —
  it is there because the answer a run ends on had nowhere to live but a
  transcript. **Existing records are not migrated for this one**, unlike
  `Fixes checked by`: a reviewer who was never asked left no answer, and
  filling the cell in from the verdict table is the derivation the field
  exists to refuse.

  **`nobody — <why>` prints on every run, and fails in one place**: on the
  run's last record, beside a checked `Pass`. That pair is the review claiming
  to have passed while the fixes that closed its findings went unread.
  Anywhere else the cell only prints, because failing for an honest disclosure
  is what teaches people to write none.

  **Work items begun before this release are excused that refusal** and only
  print. The cutoff is the unix second already in a work item's directory
  name, compared against one constant, so nothing needs configuring: a fresh
  install is held to the rule everywhere, and a repository updating the plugin
  has exactly its existing items excused. A check whose first act is red on
  merged history nobody can honestly repair is a check people learn to skip.
  The way out for everything after the cutoff costs no round — one verifying
  round at the diff of those fixes.

  **Every existing round record needs the new row**, not only the newest.
  There is no fallback, for the reason `docs/review-handoff-protocol.md`
  gives for the `rounds/` move: the failure names the row and the three
  values it takes. Write `| Fixes checked by | round-N |` on each record
  whose fixes a later round opened, and `| Fixes checked by | nobody — <why> |`
  on the last one if nothing did.

- **The agent files say that file edits go through the `Edit` tool**, and
  they name both reasons rather than only the familiar one. An edit must be
  able to fail, which is why a shell substitution that misses its pattern is
  an unverified edit. And no Bash command line exists, so the commit gate has
  nothing to read.

  The second reason is what a session hit. The gate reads a heredoc body as
  shell, because a commit hidden in one used to walk straight past it, and
  two kinds of segment count. One has a commit in it: a command word of
  `git` with the `commit` subcommand, which a partial patch to a file
  carrying shell commands as test data can leave in command position, and
  which a document showing a waiver example carries on purpose. The other
  has no commit at all: a segment the reader cannot expand, so an `eval`
  argument holding a variable, a command substitution or a glob stops the
  session with no `git` in the body. Neither command commits anything, and
  the prompt reaches whoever is at the keyboard — in an unattended run,
  nobody. (#34)

  The gate is unchanged. Whether it should skip a heredoc body that is being
  written to a file rather than run is a separate decision, and it is
  recorded as an open question on the work item instead of being made here.

- **A change to a gate now answers for what it costs in interruptions.**
  `CONTRIBUTING.md` asked three things of one — a test seen red, a stated
  failure direction, platform honesty — and none of them was the price the
  change puts on whoever is at the keyboard. A fourth is added: say how many
  times the change stops to ask a person, and if it adds one, say why nothing
  cheaper reaches the same guarantee. It is the item a passing suite cannot
  report on, because nothing counts interruptions. (#43)

  The goal that budget is drawn against is now stated where a design is
  chosen rather than only where a procedure is followed. `implement` already
  carried the reasoning to every session that loads it, but a person deciding
  between two mechanisms reads the ticket and `CONTRIBUTING.md`, and neither
  said a prompt was a cost.

  Nothing changes for anyone installing the plugin. Both files are
  contributor-facing, and `install.sh` distributes only the marker block in
  `CLAUDE.md`, which keeps its size.

- **`writing-style` produced text that satisfied it and could not be read,
  and three things about the file explain why.** (#9)

  **The per-document sections looked complete.** Someone opening the file to
  write a PR body starts at that section, reads its table, and applies it.
  The line saying the sentence rules for their language apply too sits two
  hundred lines above, where they never went. Each of those sections now says
  it at the top: what follows adds to the sentence rules and never replaces
  them.

  **There was no way to notice the jargon was yours.** Every example was a
  word from somebody else's domain, so it read as somebody else's vocabulary
  — while the word learned from this codebase an hour ago already feels like
  ordinary language. A mechanical test replaces the judgment: if you first
  met the word here, in the code or in a policy document, it is jargon. The
  word class that actually leaks is named too, because a list never
  enumerates it.

  **Conversation with the user was not one of the kinds of writing.** It is
  the one written most, and the density that makes a PR body precise makes it
  unreadable. It now has a row in the opening table and a section of its own.

## 0.0.1 — 2026-08-31

- **Initial release.** An implement/review agent chain with hook enforcement,
  an evidence ledger with drift detection, and a tool-agnostic review handoff
  protocol.

  The gates ship opt-in: a repository is judged only once it says so, and
  every gate that cannot read its input fails toward asking rather than
  toward silence. `specs/` holds a work item's documents and
  `.specseal/` holds the ledger that points into the code.
