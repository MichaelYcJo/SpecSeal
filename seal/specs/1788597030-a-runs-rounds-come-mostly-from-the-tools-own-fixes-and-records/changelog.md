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
