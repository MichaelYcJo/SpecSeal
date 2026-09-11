# Round 2 — the verifying round

Target SHA `8b3146a4c89ced9a6bc6441b1f4a7222522cf294` · diff under review
`1d1b6e9..8b3146a`, round 1's fix pass and nothing else — 14 files,
+118 / −50. Reviewed in a `git clone --no-local` at the target SHA; nothing
was written in the working checkout except this file.

## What this round found, in one paragraph

**Every finding round 1 recorded as closed is closed, and the fix pass left
three things behind.** All four fixes hold under execution, including the one
that narrowed a case: the narrowing mirrors the tool's own grading exactly, it
still goes red on the defect it exists for, and the alternative it declined was
rightly declined. The three leavings are all cosmetic and all in prose the fix
pass itself wrote — an over-long line in a shipped template, a rewritten
comment that misstates the list it sits on, and one row of `round-1.md` that
says `answered` where the report it was generated from says the check was never
run. None of them is a defect a release would ship. **Nothing needs a fix, and
the sealer's spawn is what comes due.**

---

## The narrowed case is a faithful mirror of the tool, and it still goes red

**Location** — `tests/test_a_record_states_what_the_tree_has.py:1000-1001`,
against `skills/evidence-check/scripts/evidence_check.py:2442-2444`.

This is the item the handoff asked me to judge hardest, so I judged it three
ways and executed two of them.

**The partition is identical, not merely similar.** `main` computes
`refused = len(records) - drifted - external` and then returns 2 on `refused`
or a broken ledger anchor, and 1 on drift without `--strict`. The case's
filter — `f[0] not in ("DRIFTED", "EXTERNAL")` — partitions the same list on
the same two statuses. I checked what statuses can reach that list at all:
`check_records` appends the unreadable status, the not-in-tree status, and
whatever `check_text` returns that is not `OK`, which is `BROKEN`, `DRIFTED`
and `EXTERNAL`. So the case cannot drift away from `main` by meeting a status
neither of them thought about.

**Executed — the case still fails on the defect it was written for.** I removed
the `NAME NOT IN TREE` marker from `survivors.md:11` in the clone and re-ran
the case: unmutated **exit 0**, marker removed **1 failed** with the
`NOT-IN-TREE` finding in the assertion message. Restored from bytes kept before
the run and verified byte-identical, `__pycache__` cleared. This is the
demonstration the fix pass reports, re-run rather than taken.

**`CONTRIBUTING.md:57-81` asks four things of a change to a gate, and the
docstring answers the two that apply.** A test seen red — shown, above and by
the fix pass. A stated failure direction — the docstring says plainly that the
case now allows more, names what it stops catching (drift), names what stays
fatal (a name the tree lacks, a broken anchor), and gives the reason: a live
work item's branch is editing the very units its records stamp, so failing on
drift is red by construction. The prompt budget and platform honesty do not
apply to a pytest case that prompts nobody, and the docstring names all three
platforms anyway.

**The declined alternative was rightly declined.** Rewriting
`phases/phase-1.md:131` so the superseded hash leaves `path#unit@hash` form
would break the coordinate a reader opens, and re-stamping it would make the
sentence assert that the hash held before phase 1 and the hash held after it
are the same — which is the opposite of what the record says. I opened the line
and `overview.md:40` and both hold.

**The trade is the right one.** The case's own title is *records state nothing
the tree LACKS*, and a drifted anchor is a unit that still exists with changed
content — the tree does not lack it. What the case measures now is what its
name always claimed. What is genuinely lost is a drift finding on `main`, where
the branch is not live — and nothing else fails on that either, because CI runs
the checker without `--strict` and renders exit 1 as a warning. No gate goes
quieter than it already was.

## Finding 6 is closed, not half-closed

**Location** — `seal/ledger.md:275`, `:276`, `:277`, `:283`, `:284`, against
`seal/specs/1789081272-the-writer-of-the-contract-is-not-its-executor/phases/phase-4.md:6`.

The handoff asks whether `answered` is a closed finding's word here, given that
three of the five rows carry `Checked` 2026-09-11 with no note naming who read
them. It is, and the reason is checkable rather than a judgment.

**Executed against git.** `d950e8b` is dated **2026-09-11**, its diff touches
`seal/ledger.md` and exactly five rows, and those five are the same five the fix
pass re-dated — I compared the two diffs row by row. Its commit message states
what was done: *Each claim was re-read rather than re-pointed.* So 2026-09-11
is a true statement about a day somebody read the code, and `phase-4.md:6`
names the commit behind it.

`CLAUDE.md:118` asks the `Checked` column for a date and asks nothing of the
`Notes` cell. The two rows that contradicted themselves no longer do. A reader
wanting the signature has the commit, through the phase record. There is
nothing left in the finding to be half of.

## The seven unswept names are outside §12's class, and the comment around them is not

**Location** — `tests/test_the_records_can_be_carried_out_and_in.py:52-62`.

The fix pass's boundary is right. §12's class here is the one round 1 named:
*a new member joins an enumerated set, and the enumerations that name the set
have to be swept.* The set is the agent marks this branch added, the
enumerations are three — `tests/test_docs_line_wrap.py`'s `COVERED`,
`tests/test_one_word_one_meaning.py`'s `SEAL_SWEPT`, and `BESIDE_THE_ROOT` —
and all three are now swept. The seven names the fix pass enumerated and left
(`specseal-review-choice`, `specseal-implementer-notice`, `specseal-leases`,
`specseal-worktree-consent`, `specseal-mode-choice`, `specseal-mode-retry`,
`specseal-commit-choice`) sit under the git directory in hooks this branch
never opened, and nothing this work item did produced them. Widening a fix pass
into them would be a different work item. **No finding on the boundary.**

I also spot-checked the two lists the fix pass cleared rather than taking them.
`tests/test_broad_gate_rule.py:92`'s `CARRIERS` is four documents that must
state the broad gate's condition as a row, and
`tests/test_the_last_rounds_fixes_are_checked.py:916`'s is four documents that
must name the verifying round. Both are lists of rule-carrying documents, and
`agents/scribe.md` is absent from both for the same reason `agents/framer.md`
is: neither runs the chain or the gate. Cleared correctly.

What does not hold is the comment the fix pass wrote in place of the old one.
That is finding 16 below.

---

## The fix for finding 7 left a 118-column line in a shipped template

**Location** — `templates/sdd-routing.md:62`.

Finding 7's paste-ready fix re-wrapped three lines of the comment block and the
fourth line was left carrying what the rewrap pushed onto it:

    because the gate stops recognising the file and goes back to asking. A wrong answer here is never contradicted by

**Executed** — `templates/sdd-routing.md` measured at `1d1b6e9` and at
`8b3146a`: the longest line goes from **94 to 118** columns, and the 118 is
this line. Every other line of the block sits at or under 80.

Nothing goes red, and I checked why rather than assuming: `templates/` has
exactly one entry in `tests/test_docs_line_wrap.py`'s `COVERED`, and it is
`templates/config.md`. So the repository's own wrap check does not reach the
file that every work item copies.

## The rewritten `BESIDE_THE_ROOT` comment misstates the list it sits on

**Location** — `tests/test_the_records_can_be_carried_out_and_in.py:52` and
`:216`.

The fix pass replaced a comment that grouped the entries by arrival with one
that reads:

    # `docs/one-root-by-lifetime.md` names these.

**Executed** — `docs/one-root-by-lifetime.md` carries four `specseal-` names
in total: `specseal-planner` and `specseal-implementer` at `:111-112`,
`specseal-worktree-choice/` at `:113`, and `specseal-scratch` at `:583`. The
tuple holds seven. So the document names three of the seven, plus one name that
is not in the tuple at all. The old comment was imprecise about which entries
came from the document; the new one asserts that all of them do.

The docstring four lines down has the same shape. It now opens *Everything
`BESIDE_THE_ROOT` names sits beside the root* and then enumerates: *the two
agent marks, the choices, the two review marks, the opt-out and the lease.*
`specseal-worktree-choice` — *the choices* — is not in the tuple; the case
builds it separately at `:227` and appends it to the assertion loop by hand.
And `specseal-last-export.json` is in the tuple and in neither half of the
sentence. The old docstring described the case; the new one claims to
enumerate the constant, and does not.

This costs nothing at runtime. What it costs is the next session that reads the
comment to decide whether a new file belongs in the list, follows the pointer,
and finds three of seven.

## One row of `round-1.md` says `answered` where the report says nobody ran it

**Location** — `rounds/round-1.md:47`, against `rounds/round-1-report.md`'s own
verdict table.

Row 15 is the broad gate. The report's verdict cell reads
**`❓ out of verified scope`** with *Not run* and the answerer named. The record
generated from it reads **`answered`**.

`answered` is the word for a finding closed on grounds. The broad gate was not
closed on grounds; it was not run, by rule. The new `Grounds` cell does carry
the answerer and the `Broad gate` field above still reads `not yet`, so the
state is reconstructible — but contract §4 asks that what was left unverified
not wear a settled verdict's word, and this is the one row in the table where
that matters. A correction rather than a fix: the location is under
`seal/specs/`, so `docs/review-chain-spec.md` §*The last round verifies* puts
it outside `Needs a fix`.

---

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 1 | `bin/evidence-check` exits 2 on seven `NOT-IN-TREE` refusals | `survivors.md:11`; `phases/phase-2.md:77`, `:133`, `:166`; `phases/phase-4.md:35`, `:36`, `:82` | answered | Executed at the target SHA, exit code read directly and never through a pipe: **exit 1**, records `0 refused · 1 drifted`, ledger `1121 ok · 0 drifted · 0 broken`. All seven markers present and each names the removed name it stands for. `test.yml:89-94` renders exit 1 as a warning |
| 2 | `test_a_person_answerable_row_reaches_the_report_in_full` cannot fail | `tests/test_a_question_says_who_can_answer_it.py:136` | answered | The assertion now pins the bullet's own literal, and `agents/framer.md:223` carries it verbatim. Executed: module green in a 160-passed run |
| 3 | `test_the_report_does_not_reduce_the_frame_to_counts` pins half of what it claims | `tests/test_a_question_says_who_can_answer_it.py:167` | answered | Same repair on the other half; `agents/framer.md:217` carries the literal. Executed, green |
| 4 | `BESIDE_THE_ROOT` does not carry `specseal-planner` | `tests/test_the_records_can_be_carried_out_and_in.py:53` | answered | The entry is present and the case builds seven files plus `specseal-worktree-choice`. Executed, green. The comment around it is finding 16 |
| 5 | The follow-up row sits outside its table | `seal/follow-up.md:65` | answered | The blank line is gone and the row rejoined the table — and the line that replaced it is finding 10's own deferral row, so one edit closed both. Read, and `tests/test_a_rider_reaches_its_file.py` executed green |
| 6 | Five ledger rows re-hashed with `Checked` left stale | `seal/ledger.md:275`, `:276`, `:277`, `:283`, `:284` | answered | All five read 2026-09-11. Executed against git: `d950e8b` is dated 2026-09-11, touches exactly those five rows, and its message states each claim was re-read. `phases/phase-4.md:6` names it |
| 7 | `the other two ship answered` is a miscount | `templates/sdd-routing.md:59` | answered | The sentence now names `Planning` beside this row and `Review` and `Destination` as the answered pair; the arithmetic is right. The rewrap it left behind is finding 15 |
| 8 | S10's acceptance row is the one place the deferral is not written | `spec.md:87` | answered | The row is struck through and carries **deferred to #350**, milestone 0.11.1, in the shape §Scope item 7 uses. Read |
| 9 | The `specseal-planner` tree line is one column out | `docs/one-root-by-lifetime.md:111`, `docs/one-root-by-lifetime.ko.md:109` | answered | Both editions now align the description column with the `specseal-implementer` line below. Read, both editions |
| 10 | `plan.md`'s third `Status` value has no home | `plan.md:96-104`, `templates/sdd-plan.md:93` | answered | A `seal/follow-up.md` row now carries the argument, both sides of it, and names the repository owner as answerer. Read; the schedulable-row cases executed green |
| 15 | The broad gate | `seal/config.md` `Broad gate` row | ❓ out of verified scope | Contract §2 makes it one act with one owner and `agents/sealer.md` is that owner. Not run, by rule, in either round. Answerer: the orchestrator, through the sealer spawn, which this report makes due |
| 16 | The fix for finding 7 left a 118-column line where the block wraps at 80, in a template every work item copies and no wrap check reaches | `templates/sdd-routing.md:62` | open | Executed: longest line 94 at `1d1b6e9`, 118 at `8b3146a`, and the 118 is the line the fix wrote. `templates/config.md` is the only `templates/` entry in `tests/test_docs_line_wrap.py`'s `COVERED` |
| 17 | The rewritten `BESIDE_THE_ROOT` comment sends a reader to a document that names three of its seven entries, and the docstring beside it enumerates a name the tuple lacks while omitting one it has | `tests/test_the_records_can_be_carried_out_and_in.py:52`, `:216` | open | Executed: `docs/one-root-by-lifetime.md` carries four `specseal-` names at `:111`, `:112`, `:113`, `:583`; the tuple holds seven. `specseal-worktree-choice` is built at `:227`, outside the tuple; `specseal-last-export.json` is in the tuple and in neither half of the docstring |
| 18 | Row 15 of the round record reads `answered` where the report it was generated from reads `❓ out of verified scope` — a settled verdict's word on the one check neither round ran | `rounds/round-1.md:47` | open | Read, both files at the target SHA. A correction under `seal/specs/`, so outside `Needs a fix` per `docs/review-chain-spec.md` §*The last round verifies* |

## Executed probes

| What was run | Result |
|---|---|
| `bin/test` over the three changed modules at the target SHA, in the clone | **160 passed** |
| `bin/test` over `tests/test_docs_line_wrap.py`, `tests/test_a_rider_reaches_its_file.py`, `tests/test_one_word_one_meaning.py`, `tests/test_waiver_decided_at_start.py`, `tests/test_routing_is_recorded.py`, `tests/test_the_implementer_is_recorded.py` | **137 passed** |
| `bin/evidence-check` unscoped at the target SHA, exit code read directly, never through a pipe | ledger `1121 ok · 0 drifted · 0 broken`; records `0 refused · 1 drifted`; **exit 1**, which `test.yml:89-94` renders as a warning |
| `.github/scripts/rider_check.py` at the target SHA | `26 ok · 0 drifted`; **exit 0** |
| `uvx ruff check` and `uvx ruff format --check`, the three changed modules only | All checks passed · 3 files already formatted |
| Probe: one marker removed from `survivors.md:11`, the narrowed case re-run, the file restored from bytes kept before the run | unmutated **exit 0**; marker removed **1 failed**, `NOT-IN-TREE` in the assertion message. Restored byte-identical, `__pycache__` cleared |
| Statuses `check_records` can append, read out of `evidence_check.py:2233-2281` and compared to `main:2442-2444` | unreadable, not-in-tree, `BROKEN`, `DRIFTED`, `EXTERNAL` — the case's filter and `main`'s subtraction partition the same set |
| Longest line of `templates/sdd-routing.md` at `1d1b6e9` and at `8b3146a` | **94 → 118**, and the 118 is the line finding 7's fix wrote |
| The rows `d950e8b` touched in `seal/ledger.md`, against the five the fix pass re-dated | the same five, and `d950e8b` is dated **2026-09-11** |
| `specseal-` names carried by `docs/one-root-by-lifetime.md` | four, at `:111`, `:112`, `:113`, `:583` — against seven in `BESIDE_THE_ROOT` |
| New units and contract changes in `1d1b6e9..8b3146a` | no added `def`, `class` or module constant in `tests/`; no file under `skills/agent-contract/` touched. `New units: none` and `Contract changes: none` are honest |
| Broad gate — the full suite, the repository-wide lint, the typecheck | **not yet** — not run by this round and not this round's to run. `agents/sealer.md` is the owner, and this report leaving nothing open is what makes the sealer spawn due |

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| Whether `BESIDE_THE_ROOT` should reach the seven session-state names beside the root that no work item's mark produced | nowhere yet — judged outside §12's class for this run, since the branch opened none of those hooks. It is a coverage question about untouched code, not a leaving of this fix pass | the repository owner, if it is ever worth a work item |

## Paste-ready fixes

Finding 16 — `templates/sdd-routing.md:62`. Two lines in place of one; nothing
else in the block changes.

```
     because the gate stops recognising the file and goes back to asking.
     A wrong answer here is never contradicted by
```

Finding 17 — `tests/test_the_records_can_be_carried_out_and_in.py:50-52`, the
first three lines of the comment. Say which document names which, rather than
sending a reader to one that holds three of seven.

```python
# Session state that sits BESIDE the root under the common git directory.
# `docs/one-root-by-lifetime.md`'s tree diagram names the two agent marks and
# the opt-out; the review and parity marks, the export state and the lease are
# named where each is written. None may ever be in a zip, and the case that
# asserts it builds every one of them.
```

Finding 17 — `tests/test_the_records_can_be_carried_out_and_in.py:216-218`, the
docstring. Name what the tuple holds, and say that the choices directory is
built beside it.

```python
    """S2. Everything `BESIDE_THE_ROOT` names sits beside the root — the two
    agent marks, the two review marks, the opt-out, the export state and the
    lease — and the worktree choices directory is built beside them here.
    None of them belongs to another machine."""
```

Finding 18 — `rounds/round-1.md:47`, row 15's `Verdict` cell only. Restore the
word the report it was generated from uses.

```
| 15 | The broad gate — full suite, repository-wide lint, typecheck | `seal/config.md` `Broad gate` row | ❓ out of verified scope | contract §2 makes it one act with one owner and `agents/sealer.md` is that owner; the orchestrator spawns the sealer once this round settles, and the `Broad gate` cell is where the answer lands |
```

Needs a fix: no — all three of what this round opened are corrections owed at
the closing commit, none of them changes behaviour, and none is a defect a
release would ship. What comes due instead is the sealer spawn: contract §2's
one broad act, which neither round ran and neither round was allowed to.

Loses a record or crashes: no — nothing this round found leaves the root or
crashes, and nothing round 1 found did either. The one thing that ever failed a
CI job, finding 1, is fixed and the check now exits 1, which is a warning.

---

## Proof block

- opened — `rounds/round-1.md`, `rounds/round-1-report.md`, `overview.md`,
  `spec.md`, `survivors.md`, `phases/phase-1.md:120-145`, `phases/phase-2.md`,
  `phases/phase-4.md` (diffs and heads) · `tests/test_a_question_says_who_can_answer_it.py`,
  `tests/test_a_record_states_what_the_tree_has.py:940-1005`,
  `tests/test_the_records_can_be_carried_out_and_in.py:1-120` and `:205-270`,
  `tests/test_broad_gate_rule.py:92-135`,
  `tests/test_the_last_rounds_fixes_are_checked.py:916-945`,
  `tests/test_docs_line_wrap.py` (the `COVERED` entries) ·
  `skills/evidence-check/scripts/evidence_check.py:2230-2300` and `:2415-2480` ·
  `agents/framer.md:205-230` · `templates/sdd-routing.md:50-68` ·
  `seal/ledger.md:272-288`, `seal/follow-up.md:55-75` ·
  `docs/one-root-by-lifetime.md`, `docs/one-root-by-lifetime.ko.md` ·
  `CONTRIBUTING.md:57-120`, `CLAUDE.md:110-130` · `bin/test`,
  `bin/evidence-check` · `hooks/review-skill-gate.py`,
  `hooks/implementer-notice.py`, `hooks/session-lease.py`,
  `hooks/worktree_consent.py`, `hooks/mode-gate.py`,
  `hooks/commit-review-gate.py` (the marker-directory constants only)
- executed — the twelve rows of §*Executed probes*, every exit code read
  directly and never through a pipe
- read, not executed — the fix pass's own four mutation demonstrations, except
  the one I re-ran; its narrow `bin/test` over eight modules; the CI job
  results the handoff carried
- unverified — the broad gate, answerer the orchestrator through the sealer
  spawn
- probe — one script in the scratchpad, not in the tree: it removed one marker,
  ran one case, and restored the file from bytes kept before the run. The clone
  was deleted after the round. No worktree, branch, checkout or virtual
  environment was left behind, and nothing was written in the working checkout
  except this report.
