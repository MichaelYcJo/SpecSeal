# Feature Specification: a fix of a fix twice sends the chain back to its framer

<!-- seal/specs/1791240747-a-fix-of-a-fix-twice-sends-the-chain-back-to-its-framer/spec.md — WHAT this work delivers and how we'll know.
The policy documents in docs/ outrank this file; cite them, don't restate. -->

Issue #823. In two 0.18.3 review chains a fix pass wrote code and the next
round's finding was a regression inside the code that fix pass had just
written, twice in a row, and nothing counted it. The 3+ Fix Rule fired once in
0.18.x, by hand. This work makes the count mechanical: the round-record
generator reads where a finding lands, names the first fix-of-a-fix in a run
and stops the fix passes at the second, and `chain-check` refuses a run that
went past the stop or resumed without a redrawn frame.

## Grounding

| Policy clause | What it fixes for this work |
|---|---|
| `CLAUDE.md` §*The goal a design is chosen against — verification that runs unattended*; `CLAUDE.md` §Safety, the 3+ Fix Rule | The rule here is the review chain's mechanical instance of *same bug, N failed fixes → stop, re-examine the architecture*. It fires from the records, so it fires when nobody is awake; the count is two rather than three because the first fix-of-a-fix is the signal and the second is its confirmation, and a third fix pass is what #814 and #801 each spent before anybody noticed |
| `docs/review-chain-spec.md` §*The review run has a bound, and an end*, the `stop regardless` row | Already says a round opening a new 🔴 *at the same site as the one it was closing* is the structure signal, whatever the count. Nothing reads it. This work is that row made readable: the site widened from a line to the top-level unit the previous fix pass created or changed, the severity widened from 🔴 to any finding that commissions a fix, and the count fixed at two |
| `docs/review-chain-spec.md` §*The cap bounds rounds, and not the fixes of the round it stopped* | Ownership is read off the records (`New units`), never judged. The same reading decides *lands in a unit the previous fix pass wrote*: a record's `New units` and its `Fix range`, nothing a person types |
| `docs/review-chain-spec.md` §*The reopening — one, and then the run is capped* | The exit shape to mirror: a terminal record whose open findings close `deferred <home>`, whose `Fixes checked by` reads `no fixes to check`, and a `chain:` label on the pull request. A refusal that names no exit is a wall |
| `docs/review-chain-spec.md` §*The last round verifies*, *A finding located in a record is a correction, not a round* | A finding whose `Location` is a record or a document never lands in a code unit, so it never counts here |
| `skills/code-review/orchestration.md` §*A fix pass adds the unit that pins it, and that unit ships unreviewed* | Depth 2 already refuses a fix-of-a-fix that ADDS a unit. This work closes the case that rule leaves open: a fix-of-a-fix that adds nothing, which is what both 0.18.3 chains wrote |
| `docs/round-record-spec.md` §*The fix surface*, §*The depth in `New units`* | The pattern a new parsed row follows: read on every record, a cutoff keyed to the id of the work item that added it, absent-before-the-cutoff prints, present-and-malformed fails at any age, the refusal names the exit |
| `docs/review-chain-spec.md` §*Two records, and what each of them says*, the 0.8.x moratorium on fields | The moratorium was for 0.8.x and is spent (`Fix range` and `Written late` arrived after it). What it still asks for holds: a new parsed field arrives with its checker arm, its template row, its protocol row, its cutoff, and a measurement saying a field is what is needed — the two chains in the ticket are that measurement |
| `skills/implement/orchestration.md` §*Orchestrator: which of these acts runs itself* | A new `###` under an `Orchestrator:` heading owes a row in the acts table, held from both sides by `tests/test_every_orchestrator_act_names_its_delivery.py` |
| `CONTRIBUTING.md` §*What a change to a gate must carry* | A test seen red, a stated failure direction, a prompt budget, platform honesty. All four are answered in this spec and owed again in the pull request body |
| `templates/config.md` §`Document line ceiling` (1000, `Over the ceiling | none`) | `docs/review-chain-spec.md` stood at 994 lines when framed and at 999 at the reframe. It cannot own this rule; it takes a link of at most three lines. `docs/round-record-spec.md` is at 994, so the sentence phase 5 rewrites there shrinks or holds its length |
| `docs/the-evidence-ledger.md` §*A released row is read again in the branch's fragment*; `docs/the-record-layout.md` §*A change writes fragments, never a shared file* | `seal/config.md` declares `Ledger frozen from 1790993141`, and this work item is above it. New rows go to `seal/ledger/1791240747-….md`; a released row whose anchor this work moves is re-read with `evidence-check --reverify --into`, never re-stamped in place |
| `docs/issues-and-milestones.md`, the `chain: capped` shape | A label puts the subject in the prefix and the verdict in the value. The stop's label is `chain: reframed` |

## Scope

### In

**The reading.** `round_record.py new`, writing round K's record, reads the
record before it in the same run — round K-1's `Fix range` and `New units` —
and the verdict table of round K's report. A finding **lands in a unit the
previous fix pass created or changed** when all of these hold:

- its verdict is open when `new` writes the record (the same rows `close`
  will demand a fix-table row for);
- its `Location` resolves to a top-level Python unit at round K's
  `Target SHA`, through a reading that carries its own file: `path:line`,
  `path#unit` or `path::unit`, where `path` is a `.py` file the tree tracks
  at the target. A backticked or bare identifier with no path lands nowhere,
  whatever is written beside it — the reframe after round 3 removed that
  reading, and §*What round 3 moved* says why;
- that unit is named by round K-1's `New units`, or is present at both ends
  of round K-1's `Fix range` with a different AST between them
  (`ast.dump` of the top-level node, attributes excluded — a comment-only
  edit changes nothing a finding can regress on).

Prose files, module-level lines, a name with no path, a `Location` the reader
cannot place and a `Fix range` of zero commits land nowhere. A `Fix range` whose ends do not
resolve in the tree `new` runs in is refused at exit 2 naming the range: `new`
runs where `close` ran, and a tree without those commits is the wrong tree.

**The row.** `round-N.md` gains one parsed field, `| Fix of a fix | … |`,
written by `new` and read by `chain_check.py`. Three values and nothing else:

| Value | When |
|---|---|
| `no` | no open finding of this round lands in the previous fix pass's units — the value every round 1 and every record after a `second` starts the count at |
| `first — <finding> at <path#unit>, a unit round-<K-1>'s fixes <added \| changed>` | at least one lands, and no earlier record of this run reads other than `no`. Several landings are `;`-separated after the dash |
| `second — <the same>; the fix passes stop here and the work item goes back to its framer` | at least one lands, and one earlier record of this run already reads `first` |

A **run** is the records from round 1, or from the record after the last
`second`, up to and including the next `second`. The count is per run and
reads the rows as written.

**The stop.** On `second`, `new` prints a line of the shape `bound_line`
prints — `round-record: the fix passes stop here — …` — naming the finding,
the unit, the record whose fixes wrote it, and the exit below. The
orchestrator commissions no fix pass. The record's open findings close
`deferred the frame` through `close`, with the grounds naming the stop, so
`Fixes checked by` reads `no fixes to check` and `Pass` is ticked over a table
of deferrals, exactly as a capped record's is. The pull request is labelled
`chain: reframed`.

**The reframe.** The orchestrator spawns the framer again, with the run's
round records as its input — they are in the tree, so the prompt names them
and carries nothing else. The framer rewrites `plan.md` (new phase rows for
the redesign; closed phases keep their `Status` commit) and `spec.md` where
the scope moves, and adds one line at the foot of `spec.md`, under the
`Framed` line:

```
Reframed <date> by <who>, after round <N>.
```

`<who>` takes the two values the `Planning` row takes, as the `Framed` line
does; `<N>` is the number of the record that reads `second`. `plan.md` gains a
second `Approved <date> by <who>, when `smith` was spawned.` line when the
redesign is spawned. The redesign is built, and its first review round is a
finding round whose record starts the count at `no`; its `## Inherited
coordinates` already carry every `Location` of the stopped run, because
`inherited_rows` reads every earlier record.

**The generator's refusal.** `new` refuses to write a record after a `second`
while `spec.md`'s foot carries no `Reframed … after round <N>` line naming
that `second`'s round. Exit 2, nothing written, the line to add named.

**The gate.** `chain_check.py` gains an arm `fix_of_a_fix`, read on every
record like `fix_surface` and `stopping_floor`, behind a cutoff
`REFRAME_FROM = 1791240747`:

| The record | The check |
|---|---|
| no `Fix of a fix` row, work item begun on or after the cutoff | **fails**, naming the row and what it buys |
| no row, work item begun before the cutoff (or with no timestamp prefix) | prints — the grandfathering `Fixes checked by` uses |
| a row that is empty, a bare `first` or `second`, or a word outside the three | **fails** on any record — formatting is the author's |
| the second non-`no` record of a run reads `first` | **fails** — the count says `second`, and a record that disagrees with its own run keeps the fix passes going |
| a third non-`no` record in one run | **fails**, naming the `second` it went past and the exit |
| a `second` record whose verdict table carries a fix word (`FIX_WORDS`) | **fails** — a fix pass ran after the stop |
| a record after a `second`, and `spec.md`'s foot carries no `Reframed … after round <N>` naming that `second` | **fails** — the run resumed on the frame it had just shown does not hold |
| the `Reframed` line's `<who>` disagrees with `routing.md`'s `Planning` row, or is the unfilled placeholder | **fails**, as the `Framed` line's does |

**The walks stop at the boundary.** The floor's two walks (`stopping_floor`
in the checker, `floor_and_fixes` in the generator's printed bound) and the
fix-of-a-fix count read a run, never the whole directory: a record after a
`second` is not a *later record* of any record at or before it. Without this
the redesign's own finding round and its verifying round would be the second
and third records after the stopped run's floor, and the gate would refuse
the redesign for existing. The round cap's prose count restarts the same way.

**`frame_mark` widens.** It reads the foot block — the trailing non-empty
lines that match the `Framed` shape or the `Reframed` shape — and requires the
`Framed` line among them. `templates/sdd-spec.md` still ends with the `Framed`
line; the `Reframed` line is written only by a reframe.

**The documents.** The rule's owner is a new `###` in
`skills/code-review/orchestration.md` under `## Orchestrator: the run ends
with a verifying round`, beside *The cap is a ceiling*: it states the rule,
its two-against-three relation to the 3+ Fix Rule, and the exit. Every other
carrier links to it in one sentence: `docs/review-chain-spec.md` (at most
three lines, beside the `stop regardless` row), `agents/framer.md` (the route
back now exists, from the chain and not from the builder; what a re-spawned
framer reads and writes), `agents/warden.md` (one sentence: report a finding
inside the previous fix pass's units at the severity found; the generator
counts it). The field itself is documented where fields are:
`docs/round-record-spec.md` (a section in the shape of §*The depth in `New
units`*), `docs/review-handoff-protocol.md`'s field table,
`templates/sdd-round.md`'s field row, `templates/config.md` §*What no row
governs* (`Fix of a fix`, `first`, `second`). The acts table in
`skills/implement/orchestration.md` gains the new heading's row;
`tests/test_the_rules_have_one_owner.py` gains the rule with its owner and
link carriers; `docs/issues-and-milestones.md` names `chain: reframed` beside
`chain: capped` in one sentence.

**The fragments.** `seal/specs/1791240747-…/changelog.md` and
`seal/ledger/1791240747-….md`; released rows whose anchors this work moves
are re-read into the fragment with `evidence-check --reverify --into`.

### What round 3 moved

The run's three rounds found one class three times, one reading apart each
time, and the reframe removes the reading rather than narrowing it a fourth
time.

| Round | The finding | The fix pass's answer |
|---|---|---|
| 1 (🟡 1) | a prose `Location` naming an identifier in backticks landed in a Python unit of any file the range touched | an extension list, `NAMES_A_FILE_RE`: beside a word that looks like a file, a backticked name is prose |
| 2 (🟡 1, 🟡 2) | a `bin/` wrapper, a `.cmd` and a `Makefile` were outside the list; a bare name landed although a second touched file carried it unchanged | the tree decides (`names_a_file` over `tracked_at`), and a bare name lands only where exactly one touched Python file defines it (`range_carriers`) |
| 3 (🟡 1) | a basename the tree holds twice, a path the fixes deleted and a path against a quote or an apostrophe resolve to nothing, so the cell reads as naming no file and its backticked name lands again | none — the record read `second` and the run stopped |

Each answer decided, from the prose of the cell, whether a backticked name is
the finding's place or a mention beside its place. `docs/round-record-spec.md`
§*The depth in `New units`* already declines that kind of reading one section
above the field's own: *parsing code spans to tell any of the three apart is
the same enumeration over an unbounded domain*. Round 3's paste-ready fix is a
fourth heuristic of the same kind, and taking it would be the third fix pass
this rule exists to stop.

So the reading narrows to what carries its own file. A landing needs a `.py`
path, and a name with no path counts for nothing whatever stands beside it.
What that loses was measured by reading the committed records (`git grep` over
every `rounds/round-N.md` and its report at `v0.18.0`, `v0.18.1`, `v0.18.2`,
`v0.18.3` and this branch, the `Location` cell of every 🔴 and 🟡 row): of the
179 fix-owing rows at the three later tags and this branch, none carries a
backticked identifier without a `.py` path; of the 494 at `v0.18.0`, at most
seven distinct cells do, and the column split that counted them reads a
Grounds cell as a `Location` wherever a code span holds a pipe, so seven is
the ceiling and not the count. Both chains the rule exists for (#814, #801)
land through `path:line`. `questions.md` Q6 is the replay that turns the
ceiling into a count, and it is a measurement and not a person's.

What stays as it was: `location_units` keeps every reading it makes, because
the depth walk in `close` reads a bare name there and nothing in the three
rounds found it wrong; the `second` at round 3 was the generator counting a
landing `landings` should not have accepted, not the depth walk.

### Out, and why

- **Reading a bare name through what stands beside it.** Three readings in
  three rounds, each one false for a shape the one before had not met, each
  one decided from prose — §*What round 3 moved*. The reframe lands a bare
  name nowhere rather than deciding when it is prose. A reviewer who wants a
  finding counted writes the path, which `agents/warden.md` already asks for
  and now says in those words.
- **Refusing `new` for an open row whose `Location` has no path.** It would
  make a reviewer's prose a wall at the keyboard and spend the prompt budget
  the frame set at zero; the row reads `no`, the warden's instruction names
  the path, and the permissive direction is the one every unplaceable
  landing already takes.
- **A `Changed units` row.** `new` runs on the branch where `close` ran, so
  both ends of the previous `Fix range` resolve and the changed units are
  derived from git at the moment they are needed. A row would be a second
  statement of what the range already says, and after a squash the checker
  could re-verify neither; the `Fix of a fix` row names the unit and the
  round, which is what a reader opens.
- **Hunk-level overlap.** The grain is the top-level unit, as `New units` and
  the ledger's major level already are. It is coarse — `reverify` in
  `evidence_check.py` is some 600 lines, so any finding in it after any fix in
  it counts — and it is the grain that fired correctly on both chains in the
  ticket. A finer grain needs the diff at read time, which a squash removes.
- **Units two or more fix passes back.** The ticket says *the previous fix
  pass*, and the reason holds: round K is the verifying round of round K-1's
  fixes, so a finding in those units is the fix regressing; a finding in round
  K-2's units that round K-1 left alone is a miss by round K-1, which the
  verifying round's own rules already answer.
- **Prose units and record-located findings.** A finding in a document the
  fix pass rewrote is a correction (§*The last round verifies*), and `measure`
  skips prose whole. Both chains in the ticket were code.
- **Re-judging the row at the pull request.** `chain_check.py` reads the row
  as a declaration the generator wrote and counts declarations, as it does
  for the depth. After a squash the fix commits are gone, so nothing at the
  pull request can re-derive a landing.
- **`CLAUDE.md`'s 3+ Fix Rule line and `templates/claude-md-block.md`.** Both
  stay as they are. The relation is stated at the owner; `CLAUDE.md` restates
  rules by linking to their home, and the home does not exist until this work
  ships. A link from `CLAUDE.md` is a follow-up the owner can add in one line.
- **`agents/smith.md`'s 3+ Fix bullet.** It is about the builder's own loop
  inside one fix pass; the rule here is the orchestrator's, over rounds. The
  smith never decides it.
- **The git-dir framer mark (`hooks/implementer.py`'s `PLANNING_MARK`).** A
  local notice that CI never sees. The `Reframed` line in the tree is what the
  gate reads.
- **Reading `chain: reframed` anywhere.** `chain: capped` is read by the
  release seal (`tests/test_the_release_seal_is_drawn.py` S10) because a
  capped run ends with findings filed elsewhere; a reframed run ends normally
  through the redesign's rounds, so nothing needs to treat the label as a
  state. Nothing reads it, and the document that names it says so.
- **Automating the framer's re-spawn.** Spawning is the orchestrator's act
  (contract §6), written where the stop is stated. Under `Automation | yes`
  it asks nobody; under `no` the orchestrator may ask, which is that row's
  meaning and not this rule's.

## User scenarios & acceptance *(mandatory)*

| Scenario | Given / When / Then | Verifiable how |
|---|---|---|
| S1 — a quiet record | Given round K-1's `Fix range` changed unit `u` and added none, when round K's report has no open finding whose `Location` is inside `u`, then `new` writes `Fix of a fix \| no` | planted repository, `round-record new`, the row read back |
| S2 — the first landing | Given the same, when round K's report has an open 🟡 at `path:line` inside `u`, then the row reads `first — 🟡 N at path#u, a unit round-<K-1>'s fixes changed`, `new` prints nothing about a stop, and exit is the checker's | planted repository; the case seen red against the generator without the derivation |
| S3 — the second landing stops | Given round K-1 reads `first`, when round K's report lands again, then the row reads `second — …; the fix passes stop here and the work item goes back to its framer`, `new` prints the stop line naming the finding, the unit, round K-1 and the exit | planted repository; stdout read |
| S4 — a landing in a new unit | Given round K-1's `New units` names `v`, when round K's open finding is inside `v`, then the row reads `… a unit round-<K-1>'s fixes added` | planted repository |
| S5 — what does not land | A `Location` in a `.md` file, at module level, in a unit the range only re-commented (AST equal), or unresolvable; a `Fix range` of zero commits; a ⬜ row already closed in the report — each leaves the row at `no`. **After the reframe**, so does a backticked or bare identifier with no path, whatever stands beside it: alone (`` `u` ``, `` `u()` ``), beside a `.md` file, beside a `.py` file the range did not touch, beside a tracked file of any kind, beside a basename the tree holds twice, beside a path the tree does not hold, beside a quoted path or one followed by an apostrophe | planted repository, one parameter per shape; the alone shape and round 3's three shapes seen red against `round_record.py` at round 3's target `6ceb7d46`, where each reads `first` |
| S5b — what still lands | `` `mod.py:5` ``, `` `mod.py#u` ``, `` `mod.py::u` `` each land in `u` when the range changed it, with or without a tracked file of another kind named in the same cell | planted repository; the cases phase 1 and round 2's fix pass planted, kept |
| S6 — the unresolvable range | Given round K-1's `Fix range` names commits this tree does not carry, when `new` runs, then it refuses at exit 2 naming the range, and nothing is written | planted repository with the range typed |
| S7 — no record after the stop without a reframe | Given round K reads `second`, when `new` is asked for round K+1 and `spec.md`'s foot carries no `Reframed … after round K` line, then exit 2, nothing written, the line named; with the line, the record is written and its row reads `no` even if a finding lands in round K's units (round K wrote no fixes) | planted repository, both arms |
| S8 — the gate on the row | `chain_check.py`: absent row fails at or after `REFRAME_FROM` and prints before it; empty, bare `first`/`second`, or a fourth word fails at any age | planted repository, exit code read directly (§1) |
| S9 — the gate on the count | a second non-`no` record reading `first` fails; a third non-`no` record in one run fails naming the `second`; a `second` whose verdicts carry `fixed` fails; a record after a `second` with no `Reframed` line fails and with the line passes; a `Reframed` line whose `<who>` disagrees with `Planning` fails | planted repository, one case each, each seen red before the arm existed |
| S10 — the walks stop at the boundary | Given floor `no` at round K-1, `second` at K, and the redesign's rounds K+1 (closed on a fix) and K+2 (verifying, closed on a fix), then `stopping_floor` refuses nothing and `bound_line` for K+2 says nothing about round K-1's floor | planted repository; the same tree without the `second` row is refused, which is the red half |
| S11 — the foot still reads | A `spec.md` ending `Framed …` then `Reframed …` passes the frame arm; `templates/sdd-spec.md` still ends with the `Framed` line; a `Reframed` line placed above the `Framed` line is refused | planted files; the template read |
| S12 — the two chains of the ticket | Replaying the records of `1791180640` (#814) and `1791163980` (#801) at `v0.18.3` through the reading, with their fix ranges resolved from the pull request heads, gives `first` at round 2 and `second` at round 3 in both | an executed probe, recorded in `phases/phase-N.md` and the overview as `executed`; not a planted case, because CI carries no pull request heads for a squashed branch |
| S13 — the carriers | the acts table has the new heading's row and the test passes both ways; `tests/test_the_rules_have_one_owner.py` holds the rule with its owner and links; `templates/config.md`'s governs list carries `Fix of a fix`, `first`, `second` and `test_the_exclusion_list_holds_every_string_a_checker_matches` passes; `docs/review-chain-spec.md` is at or under 1000 lines | the named tests, and `wc -l` |
| S14 — the freeze | no file under `seal/releases/` and not `seal/ledger.md` changes; the fragment holds the new rows and any `Re-read ·` rows the moved anchors owe; `evidence-check --strict .` exits 0 | `git diff --stat origin/release/v0.19.0...HEAD -- seal/releases seal/ledger.md` empty; the checker's exit read directly |

## Data & interfaces

- **New field** `Fix of a fix` in `round-N.md`, between `New units` and
  `Needs a fix` (the template's order is the record's). Constants in
  `chain_check.py`: `FIX_OF_A_FIX`, `FOF_NO = "no"`, `FOF_FIRST = "first"`,
  `FOF_SECOND = "second"`, `REFRAME_FROM = 1791240747`, `REFRAME_RE`; the
  generator loads them from the checker as it loads every other label.
- **New reader** in `chain_check.py`: `fix_of_a_fix_count(value)` → 0, 1, 2
  or None, the one reading of the row for the arm, the generator's count and
  the generator's refusal. **New arm** `fix_of_a_fix(reader, root, rel,
  earlier, later)`; **new helper** `runs_of(records)` partitioning a work
  item's records at each `second`, used by `main` to hand `stopping_floor` and
  the new arm a run rather than the directory.
- **Generator**: `landings(reader, root, target, report_rows, previous)` in
  `round_record.py` deriving the row; `build` writes it; `new` prints the stop
  and refuses after an unreframed `second`; `floor_and_fixes` and
  `earlier_records`' callers read the current run. **After the reframe**
  `landings` keeps, of the pairs `location_units` returns, only those with a
  path, and the tree loses `names_a_file`, `range_carriers`, `CELL_WORD_RE`
  and `PATH_TAIL_RE` in `round_record.py` and `TRACKED_FILES` with the four
  bare-name cases in `tests/test_a_fix_of_a_fix_is_counted.py`, replaced by
  S5's one parametrized case and S5b's.
- **The foot of `spec.md`**: `Framed <date> by <who>, before the build.` then
  zero or more `Reframed <date> by <who>, after round <N>.` lines.
- **Verdict home** `deferred the frame` — no new word; `deferred <home>`
  already closes on any home.
- **Label** `chain: reframed`, applied by the orchestrator, read by nothing.
- **Failure direction: blocks more.** A run that writes a second fix-of-a-fix
  and keeps fixing is refused where it used to pass; a run that resumes
  without a redrawn frame is refused. What it lets through, stated: the first
  fix-of-a-fix still gets its fix pass, and a landing the reader cannot place
  (prose, module level, an unresolvable `Location`) counts as none — the
  permissive direction, chosen because the stop's cost is a framer segment
  and a miss costs exactly what today costs. **Prompt budget: zero.** The
  stop spawns an agent and asks nobody; a person meets it only in the record
  and the label. **Platform honesty:** git and the AST only; nothing here
  inspects a process.

## Open questions → questions.md

The judgments the tree answered and the three rows it could not are in
`questions.md`.

Framed 2026-10-06 by framer, before the build.
Reframed 2026-10-06 by framer, after round 3.
