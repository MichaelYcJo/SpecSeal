# Round 1 report — 1790263216-the-older-statements-name-what-enforces-them (#565)

| Field | Value |
|---|---|
| Round | 1 |
| Target SHA | 2f24d6a4 |
| Range reviewed | `e9dfe623..2f24d6a4` (this work item's 19 commits) |
| Where it was read | a `git clone --no-local` of the worktree at 2f24d6a4, under the round's scratch directory |
| Reviewed by | specseal:warden on Opus 5.5 |

## How this round sampled

The contract is `spec.md` §*What a decision is* and `plan.md`. The smith's
hand-back was read in full and treated as claims. What was opened:

- **Every `nothing` line, all 12.** Each statement was dumped through
  `fold_check.py#numbered_statements`, its bold opening read, and the tree
  searched for a case that reads the rule, including a pin on the
  instruction a session follows.
- **A seeded random draw of 14 of the 75 decisions marked `read`**
  (`random.seed(565)`): D26, D27, D33, D61, D64, D68, D74, D77, D81, D82, D83,
  D91, D96, D101. Each target case was opened and its assertion read against
  the phase record's breaking edit.
- **Three more by choice**: D89 (the corrected statement), D45 and D84.
- **Seven mutations**, each restored from kept bytes, with `git status` of the
  clone empty afterwards.
- **Every named test target** (174 node ids from the 116 added lines) run in
  one command.
- **Every hunk that changes prose** rather than adding a line, to enumerate
  the third class.

## Findings from reading, confirmed by execution

### 1. D6 says `nothing` for a rule whose instruction is pinned, and its reason contradicts the workflow

`docs/the-evidence-ledger.md:148-150`. The bold rule is *When the shared
ledger or a release file conflicts, resolve it hunk by hunk and read both
sides*. The line says `nothing — a person's act`, and the reason ends *as a
leg allowed to fail*.

Two things are wrong with that.

- **The reason is false.** The `correction-check` step in
  `.github/workflows/hygiene.yml` (the step named *no merge on this branch
  dropped a correction the ledger had made*) has no `continue-on-error`, and
  no workflow in the tree carries one. The case whose name looks like the
  reason, `test_a9_the_leg_runs_the_check_and_is_allowed_to_fail`, asserts
  the opposite: its docstring says *Q2's default is that it blocks*, and it
  asserts `continue-on-error` is absent from the step. The phrase exists
  nowhere in the tree before this branch. It reads like a claim built from a
  test's name, which `spec.md` lists as wrong whatever the kind.
- **The case is wrong.** The instruction a person reads at the conflict is
  pinned. `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` holds
  *resolve it hunk by hunk and read both sides*, `--ours` and `--theirs` in
  both `CLAUDE.md` and `CONTRIBUTING.md`. The smith's own rule in phase 4 is
  *a rule a session follows takes the pin on the instruction it reads, where
  one exists*. The statement directly below this one, *Hunk by hunk has two
  halves*, already names the same module.

**Why it matters.** A reader of the policy is told a red correction-check leg
can be ignored. It cannot: it blocks the pull request.

Executed: CONTRIBUTING.md's *resolve it hunk by hunk and read both sides*
reworded, and the pin went red (1 failed). Restored.

### 2–4. Three more `nothing` lines have a pinned instruction, the same class as 1

The class is a rule a session follows whose instruction a case already pins,
given `nothing` anyway. It was enumerated over all 12 `nothing` lines, and
four of them belong to it: D6 above and these three.

- **D13, `docs/the-evidence-ledger.md:343-345`.** The bold rule is *A fold is
  not a work item, and it adds nothing to the ledger*. The reason says *no
  check reads a branch as a fold*, which is true, and it is not the only
  reader. `test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row`
  pins settle's *A fold opens no directory under `seal/specs/`*, and
  `test_the_skill_says_what_a_fold_does_to_the_ledger` pins *A fold appends
  nothing*. It also pins this statement's own bold sentence. Executed: the
  skill's sentence reworded, and the first went red.
- **D14, `docs/the-evidence-ledger.md:358-360`.** The bold rule is *A
  population floor over the records is replaced, never lowered*. The line
  says `nothing — no case reads it yet`, and that is false. The statement
  itself points at `skills/settle/SKILL.md` §3 for the three answers.
  `test_the_skill_names_the_floors_a_fold_has_to_answer` pins *population
  floor* and all three answers, and its docstring names the fourth answer,
  lowering, as the one excluded. Executed: *retire the case* reworded, and it
  went red. This line is one of the three the overview's *Not done* lists as
  case 4, so that list is one too long.
- **D32, `docs/round-record-spec.md:941-942`.** The bold rule is *A checker's
  own cases have to be able to fail*, and the statement says *the standing
  rule is the one `skills/agent-contract/SKILL.md` §15 states*. §15 is pinned:
  `test_each_section_holds_its_rule` holds *before it is committed as a case*.
  Executed: the phrase reworded, and the §15 case went red (1 failed, 15
  passed). The phase-2 argument, *a check cannot see whether somebody watched
  a case fail*, is about the act. The line is judged against the rule, and
  the instruction for the rule is read by a case.

**Why it matters.** The work item exists so that each line says what reads
the rule. A `nothing` line where a reading case exists hides that case from
the next session. For D14 it also puts a wrong row into the follow-up list.

**The other eight `nothing` lines hold up.** D7 and D63 (case 4), D37 and D90
(case 3), and D59, D67, D79 and D80 (case 1): no pin on their instruction was
found by searching `tests/` for the rule's own phrases, and each reason
matches its statement. D37's claim about `CAPPED_EXIT` and `DEPTH_EXIT` is
still true at `chain_check.py:784` and `round_record.py:2737`.

### 5. D33's target does not catch its bold rule's breaking edit

`docs/review-chain-spec.md:112`. The bold opening is *Three and five count
rounds.* (line 72). The line names `test_the_owner_states_the_rule` and
`test_every_link_names_the_owner`. Rule 13 there pins the third bold sentence,
*What decides between a fix and a home is who owns the unit now*, and not the
opening. Phase 3 says so itself and argues the pin is still the right target.
`spec.md` does not allow that: *the line is judged against the statement's
bold rule sentence*, and a target is right only when it catches the edit
that breaks that rule.

Executed: the opening was reworded to *Three and five bound the fixes a run
may write.*, and both targets stayed green (26 passed, exit 0). Restored.

**Why it matters.** This is the failure the work item's spec names, *a target
invented to avoid writing* case 4. The line claims coverage of a rule that
nothing holds. Of the 14 drawn decisions, this was the only one that failed.
The class was enumerated only as far as the sample reaches (see
`❓` below).

### 6. The rider-stamp correction's class is not closed: the release checklist still says a stamp names a commit

D89 corrected *two things point at those commits by SHA: the `Verified … at
<sha>` stamp …*, and phase 7 ran the survivor sweep to find other copies. The
sweep matches removed wording, so it found only copies that use the same
words. Two more carriers of the same false half say it in other words. Both
are in `docs/release-checklist.md`, which this branch edits:

- `docs/release-checklist.md:29-31`: *every `# RIDER:` carries a `Verified …
  at <sha>` stamp, a rebase orphans both*;
- `docs/release-checklist.md:261`: *the review records and rider stamps name
  the release branch's commits by SHA*.

`test_no_rider_stamp_names_a_commit` holds every stamp in the tree to a
content anchor. Executed: one stamp in `.github/scripts/fold_ledger.py` put
back into the old form, and the case went red. So both sentences are false
against the code, exactly as D89's was. Executed: `bin/survivor-check --range
e9dfe623..2f24d6a4` exits 0 over this range, which is why phase 7's sweep did
not reach them.

**Why it matters.** The release checklist is the procedure a person follows
at the merge button. Its grounds for *never squash* and *never rebase* now
rest partly on a mechanism that no longer exists. Both rules still hold,
because `Target SHA` alone carries them, so the fix removes the false half
and keeps the rule. These sentences predate the run. The orchestrator
applies the ownership test. The class was opened by this branch's D89
correction, which is why it is reported here.

### 7. D90's *A third reader* counts a reader that D89's correction removed (⬜)

`docs/branch-and-release.md:146`, and the docstring of the case that pins it,
`tests/test_the_release_tail_does_not_end_at_the_tag.py:188`: *The rule
already enumerated the rider stamps and the round records*. After D89, the
text before this statement names one SHA reader, not two. The overview's
*Not done* discloses it. The fact about the plugin directory stays right, so
this reads badly and is not a shipped defect. Rewording it means changing
`test_an_outside_directory_is_in_the_enumeration`'s needle in the same
commit.

### 8. Two phase records state things the tree contradicts (⬜, correction)

- `phases/phase-2.md:82` says *The 7 skips are cases that skip themselves;
  none is a target*. Executed with `-rs`: all 7 skips are parametrisations of
  D21's target `test_every_script_a_shipped_document_names_is_wrapped_or_classified`,
  for scripts no shipped document names. The case as a whole runs, so the
  target is valid. The sentence is wrong.
- `phases/phase-1.md:44`, D6's row, carries the same *allowed to fail* phrase
  as finding 1.

These are paperwork under `seal/specs/`. They are not counted in `Needs a
fix`.

## Class 3 — statements whose prose changed beyond the bold opening

Every prose hunk in `e9dfe623..2f24d6a4 -- docs` was read. Each change moves,
bolds or restates a sentence without changing its meaning: D18 (*are*
added), D35 (two sentences swapped), D42 (inner bold made italic), D82 (*the
first of them* spelled out, then rewrapped), D98/D107 (a sentence moved
first), and D17, D46, D52, D97, D100, D101, D109 and D110 (bolded in place).
The new restating sentences of D38, D48, D49, D50, D51, D81, D87, D91, D94,
D95 and D96 each say what their tables or headings already say.

The only meaning changes are the three the spec or Q1 permits. D89 was
corrected per Q1's lagging-document default. The one-root dependency
paragraph was corrected in both editions. The fold statement and the *29 of
the 101* sentence were rewritten per spec item 3. No finding in this class.

## What the other drawn decisions showed

Read: D26, D27, D61, D64, D68, D74, D77, D81, D82, D83, D91, D96 and D101. In
each, the target case plants or reads what the phase record's breaking edit
changes. D74's first target skips off POSIX (`posix_row_shell_or_skip`), and
its second target runs everywhere, so the pair holds.

Executed: D84 (a version above the running one written into a loaded skill
turns `test_no_loaded_file_names_a_version_at_or_above_the_running_one` red)
and D89 (above).

## Regression tests to plant

None. Every fix above repoints a line at a case that already exists, or
corrects prose. Finding 5's alternative, a pin on *Three and five count
rounds* added to `tests/test_the_rules_have_one_owner.py`'s `RULES`, would be
a new case. The spec rules that out of scope, so the fence below writes case
4 instead.

## Facts for the evidence ledger

None beyond what the branch's fragment carries. E1 was read against
`tests/test_both_editions_carry_the_same_folds.py#enforcement` and holds.

## Verdicts

| # | Finding | Location | Verdict | Grounds |
|---|---|---|---|---|
| 🟡 1 | D6's line says `nothing — a person's act` for a rule whose instruction is pinned, and its reason says the correction-check leg is allowed to fail, which the workflow and `test_a9_the_leg_runs_the_check_and_is_allowed_to_fail` contradict | `docs/the-evidence-ledger.md:148` | open | executed: the pin `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` goes red when CONTRIBUTING.md's instruction is reworded; read: no `continue-on-error` in any workflow |
| 🟡 2 | D13's line says `nothing` for a rule whose settle instruction is pinned | `docs/the-evidence-ledger.md:343` | open | executed: `test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row` red when the skill's sentence is reworded |
| 🟡 3 | D14's line says `no case reads it yet`, and a case reads settle's three answers | `docs/the-evidence-ledger.md:358` | open | executed: `test_the_skill_names_the_floors_a_fold_has_to_answer` red when *retire the case* is reworded |
| 🟡 4 | D32's line says `nothing — a session's act` for the rule the statement itself locates in the contract's §15, which is pinned | `docs/round-record-spec.md:941` | open | executed: `test_each_section_holds_its_rule` red (1 of 16) when §15's phrase is reworded |
| 🟡 5 | D33's targets pin the statement's third bold sentence, not its bold opening *Three and five count rounds* | `docs/review-chain-spec.md:112` | open | executed: the opening reworded to say the numbers bound fixes, both targets green (26 passed) |
| 🟡 6 | The release checklist still says rider stamps name commits by SHA, the half D89 corrected; the survivor sweep cannot see a differently-worded carrier | `docs/release-checklist.md:30` | open | also `docs/release-checklist.md:261`; executed: `test_no_rider_stamp_names_a_commit` red on an old-form stamp, and survivor-check exits 0 over the range |
| ⬜ 7 | D90's *A third reader* counts a reader D89's correction removed, and its pin's docstring still enumerates the rider stamps | `docs/branch-and-release.md:146` | open | disclosed in the overview's *Not done*; the fact about the plugin directory stays right; the pin is `tests/test_the_release_tail_does_not_end_at_the_tag.py:188` |
| ⬜ 8 | Phase records: phase 2 says the 7 skips are not targets, and they are D21's target parametrised; phase 1's D6 row repeats *allowed to fail* | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/phases/phase-2.md:82` | open | a correction to the run's paperwork; executed with `-rs` |
| 🟢 | The retrofit is complete: `fold-check` reads 136 statements, binds 136 at cutoff `0`, and holds 14 documents under the ceiling | `seal/config.md` | confirmed | executed at 2f24d6a4, with no flag and with `--shape-from 0`, both exit 0 |
| 🟢 | Every named test target is collected and passes | the 116 added `Enforced by:` lines | confirmed | executed: 174 node ids, 256 passed, 7 skipped, exit 0 (the skips are finding 8's) |
| 🟢 | The Korean edition carries byte-identical targets, and the editions case compares them | `docs/one-root-by-lifetime.ko.md` | confirmed | executed: the two editions' lines diff empty; the editions module passes; read: `enforcement` reads the span and value through the shape check's own functions |
| 🟢 | The ledger is true after the edits | `seal/ledger.md` | confirmed | executed: `bin/evidence-check .` 2094 ok, 0 drifted, 0 broken, exit 0 |
| ❓ | Whether the 58 `read` decisions this round did not open catch their breaking edits | `seal/specs/1790263216-the-older-statements-name-what-enforces-them/phases/` | ❓ out of verified scope | a sample of 14 found one failure (D33), so the class may hold more; a verifying round or the smith's fix pass answers it by the same test against each remaining row |

## Executed probes

| What was run | Result |
|---|---|
| `bin/fold-check` and `bin/fold-check --shape-from 0` at 2f24d6a4 | both exit 0; 136 statements read, the cutoff 0 binds 136; 14 documents held to 1000 lines, 0 listed |
| `bin/evidence-check .` | exit 0; 2094 ok, 0 drifted, 0 broken; 2 work items' records read, 0 refused |
| `bin/test` over the 174 node ids the added lines name | exit 0; 256 passed, 7 skipped; `-rs` shows all 7 as parametrisations of `test_every_script_a_shipped_document_names_is_wrapped_or_classified` for scripts no document names |
| `bin/test` over the editions, shape, ceiling, wrap and release-tail modules | exit 0; 103 passed |
| `bin/survivor-check --range e9dfe623..2f24d6a4` | exit 0; 81 removed sentences, none standing, so the checklist's reworded carriers are invisible to it |
| the Korean edition's `Enforced by:` lines compared with the English edition's | identical |
| M-a: D33's opening reworded to *Three and five bound the fixes a run may write.* | both targets green, 26 passed: the target does not catch it |
| M-b: CONTRIBUTING.md's *resolve it hunk by hunk and read both sides* reworded | `test_a8_both_rule_documents_say_what_to_do_at_the_conflict` red |
| M-c: settle's *A fold opens no directory under `seal/specs/`* reworded | `test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row` red |
| M-d: settle's *retire the case* reworded | `test_the_skill_names_the_floors_a_fold_has_to_answer` red |
| M-e: the contract's §15 phrase *before it is committed as a case* reworded | `test_each_section_holds_its_rule` red, 1 of 16 |
| M-f: the rider stamp in `.github/scripts/fold_ledger.py` put back to *Verified 2026-09-08 at 8f967708* | `test_no_rider_stamp_names_a_commit` red |
| M-g: a version *99.1.0* written into `skills/settle/SKILL.md` | `test_no_loaded_file_names_a_version_at_or_above_the_running_one` red |
| the broad gate (full suite, lint, typecheck) | not yet — the sealer's, after the rounds settle |

The mutations ran from one probe script in the round's scratch directory. It
drove `bin/test -p no:xdist` per mutation, restored each file from kept
bytes, asserted each restore, and left `git status --porcelain` in the clone
empty. The script and the clone were deleted before hand-over.

## Deferred

| Finding | Where it went | Who answers it |
|---|---|---|
| `CLAUDE.md` §*the merge method is fixed per direction* still says the rider stamp names a commit | already deferred by the smith: this work item's `survivors.md` row and the overview's *Not done* | the repository owner, whose file it is |
| The milestone description of `release: 0.15.3` says 101 | already deferred by the smith: `spec.md` §*The measured worklist* and the overview's *Not done* | the orchestrating session, which makes tracker posts |

## Paste-ready fixes

### 🟡 1 — `docs/the-evidence-ledger.md:148-150`, replacing the three `nothing` lines

```
Enforced by: tests/test_a_merge_cannot_silently_drop_a_correction.py::test_a8_both_rule_documents_say_what_to_do_at_the_conflict
```

### 🟡 2 — `docs/the-evidence-ledger.md:343-345`, replacing the three `nothing` lines

```
Enforced by: tests/test_settle_reads_before_it_removes.py::test_the_skill_says_a_fold_is_not_a_work_item_and_owes_no_range_row, tests/test_settle_reads_before_it_removes.py::test_the_skill_says_what_a_fold_does_to_the_ledger
```

### 🟡 3 — `docs/the-evidence-ledger.md:358-360`, replacing the three `nothing` lines

```
Enforced by: tests/test_settle_reads_before_it_removes.py::test_the_skill_names_the_floors_a_fold_has_to_answer
```

### 🟡 4 — `docs/round-record-spec.md:941-942`, replacing the two `nothing` lines

```
Enforced by: tests/test_the_agent_contract_holds_the_universal_rules.py::test_each_section_holds_its_rule
```

### 🟡 5 — `docs/review-chain-spec.md:112`, replacing the line (this document is not wrap-covered)

```
Enforced by: nothing — no case reads it yet. A pin on *Three and five count rounds* beside rule 13 in `tests/test_the_rules_have_one_owner.py` would; the ownership rule after it is held by `test_the_owner_states_the_rule` and `test_every_link_names_the_owner`.
```

With 🟡 1 to 🟡 5 applied, 106 lines name targets and 9 say `nothing`: 4 of
case 1 (D59, D67, D79, D80), 2 of case 3 (D37, D90) and 3 of case 4 (D7, D63,
D33). The overview's *Not done*, `questions.md` Q2, the changelog fragment
and phase 7's totals move with it.

### 🟡 6 — `docs/release-checklist.md:28-31` and `:260-262` (88 columns, covered)

```
      **Never rebase a work item's branch, for any reason** — every round
      record names its branch's commits by `Target SHA`, a rebase orphans
      them, and that is the class this repository has a patch release about.
```

```
green without a push. Press ***Create a merge commit***, never squash: the
review records name the release branch's commits by `Target SHA`, and a
squash discards them.
```

### ⬜ 7 — `docs/branch-and-release.md:146` with its pin, in one commit

```
**Another reader points at those commits now, and it is outside this
```

```
    """A8. The rule already named the round records' `Target SHA`, which this
    repository can repair. This reader cannot be repaired from here, which is
    the whole reason it is worth writing down."""
    rule = squash_rule()
    assert "Another reader points at those commits now" in rule, (
```

Needs a fix: yes — 🟡 1 to 🟡 6: four `nothing` lines whose case is wrong
(D6's also states a falsehood about the workflow), D33's target that does
not hold its rule, and the release checklist's two rider-stamp sentences

Loses a record or crashes: no

## Proof block

Files opened this round, at 2f24d6a4 in the clone unless marked:

- `seal/specs/1790263216-the-older-statements-name-what-enforces-them/`
  `spec.md`, `questions.md`, `survivors.md`, `routing.md`, `overview.md`
  (*Not done*), `changelog.md`, `phases/phase-1.md` to `phases/phase-7.md`
  (the decision tables and findings)
- the diff `e9dfe623..2f24d6a4` of every file under `docs/`, `tests/`,
  `seal/config.md` and `seal/ledger/`
- `skills/settle/scripts/fold_check.py` (the shape and target functions)
- `tests/test_both_editions_carry_the_same_folds.py` (the diff)
- `tests/test_a_merge_cannot_silently_drop_a_correction.py` (the A8 and A9
  cases)
- `tests/test_settle_reads_before_it_removes.py` (the skill pins)
- `tests/test_the_agent_contract_holds_the_universal_rules.py` (`PINS`)
- `tests/test_the_rules_have_one_owner.py` (`RULES`)
- `tests/test_arm_check.py` (the case list)
- `skills/verify/scripts/arm_check.py` (the docstring)
- `tests/test_a_rider_reaches_its_file.py` (the stamp cases)
- `tests/test_the_release_tail_does_not_end_at_the_tag.py` (the A8 case)
- `.github/workflows/hygiene.yml` (the correction-check step)
- `.github/scripts/fold_ledger.py` (the rider at line 273)
- `docs/release-checklist.md` (lines 24-34 and 255-266)
- `docs/branch-and-release.md` (lines 126-150)
- the target cases of D26, D27, D45, D61, D64, D68, D74, D77, D81, D82, D83,
  D91, D96 and D101
- in the worktree at 2f24d6a4: `seal/config.md` and `routing.md`
