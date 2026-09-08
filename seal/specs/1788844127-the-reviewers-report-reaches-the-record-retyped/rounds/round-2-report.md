# 1788844127-the-reviewers-report-reaches-the-record-retyped — review round 2 (verifying)

Target SHA `ab62e6d`, PR #258, fix range `76e2f75..dd152e8`. This round reads
the diff of round 1's fixes and asks, for each verdict round 1 closed, whether
it is actually closed. It did not re-read the branch.

Round 1 closed six findings — three fixed, three answered — and the fixes
added four units. Two of those six hold as closed with nothing left to say.
Two hold with a correction beside them, and both corrections come from the
same place: **a measurement was right and the sentence written from it reaches
further than the measurement does.** The four new units were each seen red on
their own mutation, and ⬜ 6's class has exactly the two members the fix
closed.

Nothing here loses a record or crashes, and nothing here needs a fix in the
sense that ends a run. One 🟡 stands in `agents/warden.md`, which the smith may
answer with grounds; two ⬜ corrections sit in this work item's own records and
belong to the orchestrator's closing commit.

---

## 🟡 1 — closed, and the class is closed with it

Round 1 said a third reader of the round-record directory took directory
membership for record-ness. The fix filters `committed_records` through
`routing.round_number`, and the corpus the filter is measured against
reproduces exactly.

**[executed]** At `a50431b`, `git ls-tree` over the round-record pathspec
returns 204 paths: 151 records and 53 non-records, of which 20 are reports, 20
are round paragraphs and 13 are fix tables. That is the fixer's independent
measurement, digit for digit. At `ab62e6d` the same walk returns 206 paths and
54 non-records, the two extra being round 1's own record and report.

**[executed]** With the filter removed, `test_the_corpus_is_records_only`
fails and names 54 of 206 corpus paths, and **every other case in that module
still passes.** That is the finding's own claim reproduced from the other
side: the strays were never refused, they were counted.

**The class, enumerated by construction rather than carried.** I took every
site in the tree that lists the round-record directory or globs its names, and
asked of each how it decides what a record is. Nine, and I opened all nine.

| Reader | How it decides | State |
|---|---|---|
| `hooks/routing.py` `_ordered`, reached through `routing.rounds` | filters by `round_number` before sorting | correct; `hooks/review-history-guard.py` inherits it rather than selecting itself |
| `chain_check.py` `round_records` | filters by `round_number` | correct |
| `chain_check.py` `stray_records` | filters by `round_number`, at the work item's top level | correct |
| `round_record.py` `earlier_records` | filters by `round_number` | correct |
| `evidence_check.py` `record_files` | reads every `.md` and makes no record/non-record distinction at all | outside the class by construction — see below |
| `tests/test_the_reopening_is_one.py` `_real_records` | filters by `round_number` | correct, closed by #111 |
| `tests/test_chain_check_at_the_pull_request.py` `_real_records` | filters by `round_number` | correct, closed by #111 |
| `tests/test_a_finding_id_is_a_bare_integer.py` `committed_records` | filters by `round_number` | **this round 1's fix** |
| `tests/test_handoff_outlives_the_merge.py` | lists the work item's top level and asserts nothing there begins with the record prefix | correct, and deliberately wider — a report at the top level is a violation too |

There is no fourth wrong count. The one reader worth naming for the next
person who enumerates this class is `record_files`: it reads the round-record
directory and does **not** select by name, so on a literal reading it is a
counterexample to `skills/code-review/SKILL.md`'s *every reader of `rounds/`
selects records by name*. It is not one. That function makes no record /
non-record distinction, so it has no selection to get wrong — it reads every
markdown file under a work item on purpose, which is exactly why the reviewer
warning below exists.

**Verdict: fixed, and the class is closed.**

## 🟡 2 — the warning is right, and its one worked example points at the region the checker never reads

This is the block I am the first reviewer to work under, so I judged it by
following it and then measuring what it told me.

**Both escapes it names are exact.** `tests/test_no_real_identifiers.py`
carries `ALLOWED_USER_PATH` as the fixture user path the block spells, and
`evidence_check.py` carries `NOT_IN_TREE` as the marker string the block
spells, character for character. Neither is approximate, and both are what a
reviewer would otherwise have to go and find.

**The defect is in the worked example.** The block says a name a paste-ready
fix proposes to add comes back as not in the tree, and then: *write the marker
on that line and it is exempt.* A paste-ready fix is a fenced block, and the
checker's `claim_lines` reads a fenced line as a quotation and never as a
claim — its own docstring gives that reason and adds that *a marker inside a
fence changes the fix somebody pastes.* So the one example the block works
through is the case that needs no marker, and the instruction sends the marker
into the block a smith will paste.

**[executed]** A probe record under this work item naming `a_totally_new_helper` in prose is refused, exit 2. <!-- NAME NOT IN TREE -->
The same invented name in backticks inside a fence is not read at all: 0
refused. The exposure is prose, and the block's example is the fence — and
the marker ending the line above is the block's own instruction applied where
it does work, since this report is scanned like any other tracked file.

Two smaller inaccuracies ride along. *Each compound identifier it finds* is
wider than `RECORD_NAME_RE`, which reads a backticked token carrying an
underscore and nothing else. And the identifier rule has a second half the
block does not mention — a real-looking domain outside the allowlist fails the
same module — which a report quoting a URL would meet with no warning.

Round 1's finding was *nothing warns the reviewer*, and that is answered: the
warning exists, it is in the section a reviewer reads, and it is pinned. What
is wrong is inside the answer, so it is this round's finding rather than a
reopening of round 1's. **Verdict: fixed; new finding 🟡 7 against the block
the fix wrote.**

## 🟡 3 — the measurement reproduces exactly, and the sentence drawn from it is wider than it

Round 1 asked for the report gate to move to `close`, which runs after the
record's own commit. The fix pass weighed it, ran it, and answered no.

**[executed]** I inserted round 1's paste-ready gate at `b76ce68`, after
`close`'s target check, and ran the module: **36 failed, 5 passed of 41.**
That is the fixer's number exactly, and the cause is the one it names — the
suite's own helper writes the report outside the repository and passes the
flag on purpose, so an unconditional gate refuses the runs the flag exists
for. The reasoning against the gate as round 1 wrote it holds.

**What does not hold is the sentence about what any surviving gate would
need.** `plan.md` says a gate that survives has to make the record carry the
path the generator read — a new field, a template section and a checker. A
gate conditioned on the conventional path actually holding a file needs none
of that:

**[executed]** the same insertion, wrapped in a test for a file at the
conventional path, at `b76ce68`: **41 passed, exit 0.** No new field, no
template section, no checker.

What that gate buys is narrower than what round 1 asked for. It catches the
failure round 1 named — a reviewer left the report at the convention and the
orchestrator committed the record without it — and it stays silent where the
report lived elsewhere, which is the case only a recorded path could reach. So
the residual is real and the decision to defer it may well be right. The
recorded ground for deferring it is what overstates: the cheap gate exists and
was not weighed. **Verdict: answered, with correction ⬜ 8 against the record
that holds the reasoning.**

## The four units the fixes added — each seen red on its own mutation

All four are depth 1, and I ran the mutations rather than reading the claim.

- Removing the filter from `committed_records` turns
  `test_the_corpus_is_records_only` red and nothing else in that module.
- Deleting the new block from `agents/warden.md` turns
  `test_the_warden_is_told_its_report_is_now_scanned_like_any_tracked_file`
  red, naming which of its four needles is gone.
- Reverting the report guard's directory lead turns
  `test_a_directory_at_the_report_path_is_refused_as_a_directory` red.
- Reverting the record guard's directory lead turns
  `test_a_directory_at_the_record_path_is_refused_as_a_directory` red.

Two mutations ran in one pass twice, and each failure named its own case, as
the fixer said. I also checked for the shape a sibling branch found — an input
that never reaches what the case claims to pin — and did not find it. The one
place it could have hidden is `run_new`, since a helper that always passed the
flag could never see the conventional path fire; that helper passes the flag
only when one is given, and says so in its docstring.

One note on the fourth case, offered as reading rather than as a defect. It
splits the file on the section heading and searches everything after it, so a
needle appearing in a later section would satisfy it. Here the report section
is the last one — the headings below it sit inside its own fenced blocks — so
the assertion is as narrow as it claims today, and would loosen only if a
section were added after it.

## ⬜ 6 — two instances, and there is no third

The cause the fix names is that the file test is false for two states and the
message named one. I enumerated every place in `round_record.py` that asks it:

- the report guard — fixed, and its refusal still carries the path, the
  document that fills it and the flag.
- the record guard in `close` — fixed, the second member, and it keeps the
  tail that says what the subcommand is for.
- `earlier_records` uses the same test as a filter with no message at all, so
  there is no message to be wrong. Skipping a directory named like a record is
  the right answer there.
- the work-item guard already says *is not a directory*, which is true of both
  states it refuses, and the reader typed that path themselves.

Outside the file, the only sibling with the same shape is in
`hooks/commit-review-gate.py`, and it already reasons about exactly this
ambiguity in place. **Two, not three, and both closed.**

## The depth-2 sentence is right

Depth 1 is a unit added by a fix answering a finding in code that predates the
run; depth 2 is one added by a fix answering a finding inside a depth-1 unit,
and it is refused. Round 1 has no fix pass before it, so every unit its fixes
add is depth 1 by construction — the four in its record are correctly marked.
From round 2 on, a fix answering something I found inside one of those four
could not add a unit to pin it; it would be deferred with a named answerer or
become an issue. Both halves match `skills/code-review/SKILL.md` §*A fix pass
may add a unit* and `templates/sdd-round.md`. I opened nothing inside those
four units, so the constraint does not bind this round.

## The broad gate

`not yet`, unchanged. Nothing this round opened needs a fix, so the one
full-suite run, the repository-wide lint and the typecheck are now due, and
they are the orchestrator's.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | a third reader of the round-record directory selects records by directory membership | `tests/test_a_finding_id_is_a_bare_integer.py:302` | answered | closed at `1e35d5d`. Executed — the corpus reproduces at 204/151/53 at `a50431b`, and removing the filter turns the new case red at 54 of 206 while every other case in the module stays green. The class is nine readers, enumerated by construction and all opened; there is no fourth |
| 🟡 2 | nothing warns the reviewer that its report is now scanned by the identifier rule and the evidence checker | `agents/warden.md:272` | answered | closed at `b76ce68`. Executed — both escapes the block names are the exact strings the two checkers carry. The block's own worked example is wrong, which is finding 7 below rather than a reopening of this one |
| 🟡 3 | nothing carries the report into the commit, and `close` was never weighed as the gate | `skills/code-review/SKILL.md:182` | answered | the gate as written is defeated by the flag. Executed — 36 failed, 5 passed of 41 with round 1's gate inserted at `b76ce68`, reproducing the fixer's measurement exactly. The residual stands; what the record says it would cost does not, which is finding 8 |
| ⬜ 4 | the acceptance row described the write as happening in the clone | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md:42` | answered | corrected at `dd152e8`; the row now matches `agents/warden.md`, which says the repository under review |
| ⬜ 5 | the spec said the clone rule needed no change | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/spec.md:60` | answered | corrected at `dd152e8`; the section now names the exception as the cost the chosen design pays |
| ⬜ 6 | a directory at the conventional path is refused as nothing being there | `skills/code-review/scripts/round_record.py:739` | answered | closed at `dd152e8`, both members. Executed — reverting either lead turns its own case red, and each refusal keeps the path and the convention. Enumerated: the class is two, and the two other sites that ask the same question are not members |
| 🟡 7 | the reviewer warning's one worked example sends the exemption marker into a fenced paste-ready fix, which the checker never reads and which a smith pastes | `agents/warden.md:286` | open | executed — a proposed name in prose is refused at `NOT-IN-TREE`, exit 2; the same name backticked inside a fence is not read at all, 0 refused. `claim_lines` reads a fence as a quotation and its docstring names the pasted-fix corruption as the reason |
| ⬜ 8 | the recorded ground for deferring the report gate says any surviving gate needs a new record field, a template section and a checker; a gate conditioned on the conventional path needs none of them | `seal/specs/1788844127-the-reviewers-report-reaches-the-record-retyped/plan.md:69` | open | executed at `b76ce68` — round 1's unconditional gate fails 36 of 41, and the same gate wrapped in a file test at the conventional path passes 41 of 41, exit 0. The narrower gate buys less, which is the honest ground for deferring; the cost sentence is what overstates. `overview.md:61` carries the same sentence |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the three changed modules, in a clone at `ab62e6d` | 81 passed, exit 0 |
| `git ls-tree` over the round-record pathspec at `a50431b`, `76e2f75` and `ab62e6d`, split by suffix | 204 / 151 records / 53 non-records (20 report, 20 asked, 13 fixes) at `a50431b`; 206 / 152 / 54 at both later commits |
| the id-corpus filter removed, `bin/test` over its own module and the report module | 2 failed of 39 — `test_the_corpus_is_records_only` naming 54 of 206, and the warden case; every other case in the id module green |
| the new block deleted from `agents/warden.md`, same run | `test_the_warden_is_told_its_report_is_now_scanned_like_any_tracked_file` red, naming the missing needle |
| both directory leads reverted, `bin/test` over the report module and the close module | 2 failed of 51, each case naming its own refusal string |
| round 1's paste-ready `close` gate inserted after the target check at `b76ce68`, `bin/test` over the close module | **36 failed, 5 passed**, exit 1 — the fixer's measurement reproduced |
| the same gate wrapped in a file test at the conventional report path, same commit, same module | **41 passed**, exit 0 |
| a probe record naming a proposed unit in prose, then the same name backticked inside a fence, through `evidence_check.py --strict --ledger` | prose refused at `NOT-IN-TREE`, exit 2; fenced name not read, 0 refused |
| `evidence_check.py --strict --ledger` at `ab62e6d` with the probe removed | 10 ok · 4 drifted · 0 broken · 0 external · 0 old-format; records arm 0 refused. The drift is the orchestrator's, taken at the closing commit |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| a gate in `close` that survives the flag, in either form — the narrow one measured here or the recorded path it would need | `overview.md` §*Not done*, unchanged by this round | the orchestrator |
| the four drifted ledger rows in this work item's fragment, and six unscoped | `seal/ledger/1788844127-the-reviewers-report-reaches-the-record-retyped.md` | the orchestrator, at the closing commit |
| `--asked` carrying the same defect `--report` had, and the two sibling files named in no shipped document | `questions.md` Q2 and Q3, opened by round 1 | the orchestrator |

## Paste-ready fixes

🟡 7 — replace the evidence-checker paragraph in `agents/warden.md` §Report:

```markdown
The evidence checker reads every `.md` under a live work item and asks the
tree for each backticked name carrying an underscore that it finds in prose.
A name your report writes that the tree does not carry comes back
`NOT-IN-TREE`, and writing `NAME NOT IN TREE` on that prose line exempts the
line.

**A fenced block is already exempt, and marking one up corrupts it.** The
checker reads a fence as a quotation, which is why a paste-ready fix may
propose a unit that does not exist yet and say nothing — so the marker never
goes inside a fence, where the smith would paste it. Where you also name that
proposed unit in prose, the marker goes on the prose line and nowhere else.

The identifier rule has a second half as well: a real-looking domain outside
its allowlist fails the same module, so quote a URL only from a host that
allowlist already carries.
```

⬜ 8 — replace the cost sentence in `plan.md`, and the matching one in
`overview.md`:

```markdown
A gate that reaches every run has to make `new` record the path it read, which
is a new field in the record, a template section and a checker that reads it —
mechanism, and a fix pass adds none. A narrower gate needs none of that:
guarded on the conventional path actually holding a file, the same refusal
passes all 41 cases at `b76ce68`, because a run that passed the flag leaves
that path empty. It buys less — it cannot see a report written elsewhere and
never committed — and that, rather than the cost, is why it is deferred rather
than built here.
```

Needs a fix: no
Loses a record or crashes: no

---

## Proof

Files opened: `agents/warden.md`, `docs/review-handoff-protocol.md`,
`skills/code-review/SKILL.md`, `skills/code-review/scripts/round_record.py`,
`skills/code-review/scripts/chain_check.py`, `hooks/routing.py`,
`hooks/review-history-guard.py`, `skills/evidence-check/scripts/evidence_check.py`,
`skills/verify/scripts/unverified_check.py`, `skills/verify/scripts/session_cost.py`,
`.github/scripts/fold_ledger.py`, `bin/test`, `templates/sdd-round.md`,
`CHANGELOG.md`, `tests/test_a_finding_id_is_a_bare_integer.py`,
`tests/test_the_fixes_close_the_record.py`,
`tests/test_the_reviewers_report_reaches_the_record.py`,
`tests/test_the_reopening_is_one.py`,
`tests/test_chain_check_at_the_pull_request.py`,
`tests/test_handoff_outlives_the_merge.py`,
`tests/test_chain_hooks_hardening.py`, `tests/test_no_real_identifiers.py`,
and this work item's `spec.md`, `plan.md`, `overview.md`, `changelog.md`,
`rounds/round-1.md` and `rounds/round-1-report.md`.

Every probe above ran in a clone of this repository at the commit named beside
it, never in the branch's own work tree. Each mutated file was restored from
bytes kept before the mutation and the tree checked clean afterwards; the
probe record written under this work item was removed. The full suite,
repository-wide lint and typecheck were not run — they are the orchestrator's,
once, after the rounds settle.
